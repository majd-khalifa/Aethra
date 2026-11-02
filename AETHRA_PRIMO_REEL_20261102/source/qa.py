"""Inspect the actual encoded MP4, decode every frame, and make a review sheet.
Usage: python source/qa.py exports/<unique-version>.mp4
Requires numpy and Pillow; uses Remotion's own FFmpeg and FFprobe.
"""
import sys,json,subprocess,hashlib,io,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BIN=ROOT/'node_modules/@remotion/compositor-win32-x64-msvc'
video=(ROOT/sys.argv[1]).resolve()
out=ROOT/'qa'/video.stem
out.mkdir(parents=True,exist_ok=False)
probe=json.loads(subprocess.check_output([str(BIN/'ffprobe.exe'),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
(out/'ffprobe.json').write_text(json.dumps(probe,indent=2))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1080,1920)
assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
assert v['r_frame_rate']==v['avg_frame_rate']=='30/1'
assert int(v['nb_read_frames'])==int(v['nb_frames'])==600
assert abs(float(v['duration'])-20)<.00001
assert abs(float(probe['format']['duration'])-20)<.002
assert a['codec_name']=='aac' and int(a['sample_rate'])==48000 and int(a['channels'])==2
assert abs(float(a['duration'])-20)<.002
# Decode all picture frames. Small RGB proxy is only for analysis/contact sheet.
p=subprocess.Popen([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(video),'-an','-vf','scale=216:384','-pix_fmt','rgb24','-c:v','rawvideo','-f','image2pipe','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
count=0; luma=[]; diffs=[]; frames={}; prev=None
chosen=[0,30,75,105,135,165,195,215,230,252,267,279,300,330,365,395,418,440,460,480,500,530,565,599]
while True:
    buf=p.stdout.read(216*384*3)
    if not buf:break
    assert len(buf)==216*384*3
    im=np.frombuffer(buf,np.uint8).reshape(384,216,3)
    luma.append(float(im.mean()))
    if prev is not None:diffs.append(float(np.abs(im.astype(float)-prev).mean()))
    prev=im.astype(float)
    if count in chosen:frames[count]=Image.fromarray(im)
    count+=1
stderr=p.stderr.read().decode();p.wait()
assert p.returncode==0 and count==600 and not stderr.strip(),stderr
assert min(luma)>8,'Unexpected black or empty frame'
# Full-resolution proof frames, from the encoded output (never from source JSX).
for frame in [30,230,279,330,395,480,565]:
    subprocess.run([str(BIN/'ffmpeg.exe'),'-v','error','-ss',str(frame/30),'-i',str(video),'-frames:v','1',str(out/f'frame-{frame:04d}.png')],check=True)
sheet=Image.new('RGB',(6*236,4*422),'#302f39');d=ImageDraw.Draw(sheet)
for i,(f,im) in enumerate(frames.items()):
    x=(i%6)*236+10;y=(i//6)*422+10
    sheet.paste(im,(x,y));d.text((x,y+389),f'Frame {f:03d} / {f/30:.2f}s',fill='#fff0d8')
sheet.save(out/'contact-sheet.jpg',quality=94)
# Decode and inspect the actual AAC audio signal.
pcm=subprocess.check_output([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(video),'-vn','-f','wav','-acodec','pcm_s16le','-ac','2','-ar','48000','-'])
with wave.open(io.BytesIO(pcm),'rb') as w:
    samples=np.frombuffer(w.readframes(960000),dtype='<i2').astype(float).reshape(-1,2)/32768
peak=float(np.max(np.abs(samples))); rms=float(np.sqrt(np.mean(samples**2)))
assert peak<1 and rms>.005
loud=subprocess.run([str(BIN/'ffmpeg.exe'),'-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
(out/'loudness.txt').write_text(loud.stderr)
report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size,'frames_decoded':count,'duration_seconds':float(v['duration']),'dimensions':[1080,1920],'fps':30,'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'audio_codec':a['codec_name'],'audio_sample_rate':48000,'audio_channels':2,'decoded_audio_peak_dbfs':float(20*np.log10(peak)),'decoded_audio_rms_dbfs':float(20*np.log10(rms)),'min_frame_mean_rgb':min(luma),'frame_differences':diffs,'decode_errors':stderr,'technical_checks_pass':True,'visual_review_required':True,'release_approval':False}
(out/'technical-qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='frame_differences'},indent=2))
