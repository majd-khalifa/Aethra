"""Append a native five-second closing continuation; never encode the first 450 frames."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'source/approved_reference'
WIDTH,HEIGHT=1080,1920

def ease(x):
    x=np.clip(x,0,1)
    return x*x*x*(10+x*(-15+6*x))

def prepare():
    reference=json.loads((REF/'manifest.json').read_text())
    for name in ['ending_frame_449.png','LOCKED_15S_PICTURE.mp4']:
        assert hashlib.sha256((REF/name).read_bytes()).hexdigest()==reference['files'][name]['sha256'],'Approved reference changed'
    base=np.array(Image.open(REF/'ending_frame_449.png').convert('RGB')).astype(np.float32)
    palette=np.array([[251,250,255],[242,237,255],[237,231,254]],dtype=np.float32)
    fits=[]
    for index in [1,2]:
        points=[]
        for y in range(700,1690,5):
            if 1360<y<1550:continue
            matches=np.flatnonzero(np.max(np.abs(base[y]-palette[index]),axis=1)<=1)
            if len(matches)>30:
                edge=int(matches[0])
                if edge>290:points.append((y,edge))
        y,x=np.array(points).T
        model=np.polyfit(y,x,1)
        residual=x-np.polyval(model,y)
        good=np.abs(residual-np.median(residual))<4
        model=np.polyfit(y[good],x[good],1)
        fits.append(model)
    yy,xx=np.mgrid[:HEIGHT,:WIDTH]
    plate=np.broadcast_to(palette[0],base.shape).copy()
    for model,color in zip(fits,palette[1:]):
        signed=xx-np.polyval(model,yy)
        alpha=np.clip(signed+.5,0,1)*(yy<1700)
        plate=plate*(1-alpha[...,None])+color*alpha[...,None]
    # Only actual foreground pixels are moved. No text, logo or raster geometry is redrawn.
    selection=np.zeros((HEIGHT,WIDTH),dtype=bool)
    selection[520:1540,145:935]=True
    mask=selection & (np.min(base,axis=2)<220)
    mask=ndimage.binary_dilation(mask,iterations=6)
    mask=ndimage.gaussian_filter(mask.astype(np.float32),.8)
    foreground=base*mask[...,None]
    cleared=base*(1-mask[...,None])+plate*mask[...,None]
    return base,(foreground,mask,cleared),{'background_palette':palette.astype(int).tolist(),'plane_edge_fits_x_from_y':[x.tolist() for x in fits]}

def shifted(layer,offset):
    integer=int(np.floor(offset));fraction=offset-integer
    return np.roll(layer,integer,axis=0)*(1-fraction)+np.roll(layer,integer+1,axis=0)*fraction

def frame(base,layer,number):
    t=number/30
    offset=-24*ease(t/2.1) if t<=2.1 else -24+6*ease((t-2.1)/2.3)
    foreground,mask,cleared=layer
    if number==0:
        result=base.copy()
    else:
        moved_mask=shifted(mask,offset)
        result=cleared*(1-moved_mask[...,None])+shifted(foreground,offset)
    # One quiet travelling edge light on the existing CTA, never a press or a copy change.
    progress=(t-1.2)/1.4
    if 0<progress<1:
        y1=int(1367+offset);y2=int(1524+offset)
        y,x=np.mgrid[y1:y2,166:914]
        cx,cy,half_w,half_h,radius=540,1445+offset,370,75,22
        qx=np.abs(x-cx)-(half_w-radius);qy=np.abs(y-cy)-(half_h-radius)
        distance=np.hypot(np.maximum(qx,0),np.maximum(qy,0))+np.minimum(np.maximum(qx,qy),0)-radius
        edge=np.exp(-.5*((distance+1.5)/1.2)**2)
        streak=np.exp(-.5*((x-(190+700*progress))/80)**2)
        alpha=edge*streak*np.sin(np.pi*progress)**2*.48
        region=result[y1:y2,166:914]
        result[y1:y2,166:914]=region*(1-alpha[...,None])+np.array([252,251,255])*alpha[...,None]
    return np.clip(np.rint(result),0,255).astype(np.uint8),float(offset)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--replace-generated',action='store_true');args=parser.parse_args()
    picture=ROOT/'source/SHARED_20S_PICTURE.mp4'
    tail=ROOT/'source/CLOSING_CONTINUATION_5S.mp4'
    assert args.replace_generated or (not picture.exists() and not tail.exists()),'Use --replace-generated for an intentional revision of only these new generated picture files'
    base,layer,metadata=prepare()
    cmd=['ffmpeg','-y' if args.replace_generated else '-n','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-',
         '-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-profile:v','high','-level:v','5.0',
         '-bf','2','-g','150','-video_track_timescale','15360','-movflags','+faststart',str(tail)]
    encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    selected={0,9,30,37,48,63,78,90,114,132,149};thumbs=[];motion=[]
    for n in range(150):
        pixels,offset=frame(base,layer,n);encoder.stdin.write(pixels.tobytes())
        motion.append({'output_frame':450+n,'seconds':15+n/30,'foreground_y_translation_px':offset})
        if n in selected:thumbs.append((450+n,Image.fromarray(pixels).resize((216,384))))
    encoder.stdin.close();assert encoder.wait()==0
    concat=ROOT/'source/picture_concat.txt'
    concat.write_text("file 'approved_reference/LOCKED_15S_PICTURE.mp4'\nfile 'CLOSING_CONTINUATION_5S.mp4'\n")
    subprocess.run(['ffmpeg','-y' if args.replace_generated else '-n','-v','error','-f','concat','-safe','0','-i',str(concat),'-map','0:v:0',
                    '-c:v','copy','-an','-movflags','+faststart',str(picture)],check=True)
    metadata['motion']=motion
    metadata['new_motion']=[{'start_frame':450,'end_frame':513,'description':'Original logo, invitation and CTA gently lift together by 24 pixels; exact proportions and original text are retained.'},
                            {'start_frame':487,'end_frame':528,'description':'A soft travelling edge light follows the existing purple CTA border; there is no press or new claim.'},
                            {'start_frame':513,'end_frame':582,'description':'The closing group settles six pixels to a final 18-pixel lift.'},
                            {'start_frame':582,'end_frame':599,'description':'Brief final stable reading hold (0.6 seconds), not a five-second freeze.'}]
    (ROOT/'analysis/visual_extension.json').write_text(json.dumps(metadata,indent=2)+'\n')
    sheet=Image.new('RGB',(216*4,414*3),'#e6e6ed');draw=ImageDraw.Draw(sheet)
    font_path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    font=ImageFont.truetype(str(font_path),13) if font_path.exists() else ImageFont.load_default()
    for i,(n,im) in enumerate(thumbs):
        x=i%4*216;y=i//4*414;sheet.paste(im,(x,y));draw.text((x+5,y+389),f'F{n:03d} | {n/30:.3f}s',font=font,fill='#171327')
    sheet.save(ROOT/'analysis/closing_motion_contact_sheet.jpg',quality=94)
    print('One shared picture created: 450 original frames plus 150 new closing frames.')

if __name__=='__main__':main()
