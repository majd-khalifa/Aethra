"""Render actual 1080-square PNGs and verify source text, captures, bounds and QR."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import asyncio
import hashlib
import json
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from playwright.async_api import async_playwright
import zxingcpp

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'source/content.ar.json').read_text())
NS={'s':'http://www.w3.org/2000/svg'}

def norm(s):return ' '.join(s.split())

def check_copy(path,slide):
    tree=ET.parse(path);root=tree.getroot()
    assert root.attrib['width']==root.attrib['height']=='1080' and root.attrib['viewBox']=='0 0 1080 1080'
    texts={e.attrib['data-copy']:''.join(e.itertext()) for e in root.iter() if 'data-copy' in e.attrib}
    assert texts['title']==slide['title'] and texts['support']==slide['support']
    for i,item in enumerate(slide.get('bullets',[])):
        parts=[(k,v) for k,v in texts.items() if k.startswith(f'bullets.{i}.')]
        assert norm(' '.join(v for k,v in sorted(parts)))==norm(item),(path.name,item,parts)
    if 'body' in slide:
        assert norm(' '.join(v for k,v in sorted(texts.items()) if k.startswith('body.')))==norm(slide['body'])
    captures=[e for e in root.iter() if 'data-authentic-ui' in e.attrib]
    assert captures
    for e in captures:
        assert abs(float(e.attrib['width'])/float(e.attrib['height'])-576/1280)<1e-8
        assert 'filter' not in e.attrib and 'clip-path' not in e.attrib
        assert e.attrib['preserveAspectRatio']=='xMidYMid meet'
        assert e.attrib['href'].endswith('02_Primo_Authentic_Home.png') or e.attrib['href'].endswith('03_Primo_Authentic_Tea_Product_Details.png')
    qr=[e for e in root.iter() if e.attrib.get('data-download-qr')=='1']
    assert len(qr)==(1 if slide['id']==5 else 0)
    return {'copy':'exact match to Arabic JSON','authentic_screenshot_instances':len(captures),'screenshot_aspect_ratio':'preserved','screenshot_ui_redrawing':False,'download_qr_instances':len(qr)}

def source_integrity():
    manifest=json.loads((ROOT/'source/reference_manifest.json').read_text())
    for entry in manifest['images']:
        f=ROOT/entry['file'];assert f.stat().st_size==entry['bytes']
        assert hashlib.sha256(f.read_bytes()).hexdigest()==entry['sha256']
    chars={c for s in DATA['slides'] for value in [s['title'],s['support'],s.get('body',''),*s.get('bullets',[])] for c in value if '\u0600'<=c<='\u06ff'}
    for name in ['Cairo-Regular.ttf','Cairo-SemiBold.ttf','Cairo-Bold.ttf']:
        ft=TTFont(ROOT/'assets/fonts'/name);cmap=ft.getBestCmap();assert all(ord(c) in cmap for c in chars),(name,chars)
    return manifest

async def render():
    svgs=sorted((ROOT/'source').glob('slide_*.svg'));assert len(svgs)==5
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            if self.path.startswith('/__export__/'):
                name=self.path.rsplit('/',1)[-1]
                if name in [p.name for p in svgs]:
                    svg=(ROOT/'source'/name).read_text()
                    page=f'<!doctype html><html><head><meta charset="utf-8"><base href="/source/"><style>html,body{{margin:0;padding:0;width:1080px;height:1080px;overflow:hidden;background:#100D14}}svg{{display:block}}</style></head><body>{svg}</body></html>'.encode()
                    self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(page)));self.end_headers();self.wfile.write(page);return
            return super().do_GET()
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    export=ROOT/'exports';export.mkdir(exist_ok=True)
    report={'canvas':[1080,1080],'native_square':True,'reference_integrity':source_integrity(),'slides':[]}
    try:
        async with async_playwright() as pw:
            browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--force-color-profile=srgb'])
            page=await browser.new_page(viewport={'width':1080,'height':1080},device_scale_factor=1)
            failures=[];page.on('requestfailed',lambda r:failures.append(r.url))
            for svg,slide in zip(svgs,DATA['slides']):
                checks=check_copy(svg,slide)
                await page.goto(f'http://127.0.0.1:{server.server_port}/__export__/{svg.name}',wait_until='networkidle')
                await page.evaluate('document.fonts.ready')
                loaded=await page.evaluate('''async()=>{const counts=[];for(const s of ['700 58px Cairo','400 28px Cairo','600 30px "Cairo SemiBold"','600 16px "Space Grotesk SemiBold"'])counts.push((await document.fonts.load(s)).length);await document.fonts.ready;return counts.every(n=>n>0);}''')
                assert loaded
                bounds=await page.evaluate('''()=>Array.from(document.querySelectorAll('text[data-safe]')).map(t=>{const b=t.getBBox();return {text:t.textContent,x:b.x,y:b.y,width:b.width,height:b.height};})''')
                for b in bounds:
                    assert b['x']>=72-.1 and b['x']+b['width']<=1008+.1 and b['y']>=72-.1 and b['y']+b['height']<=1008+.1,(svg.name,b)
                name=svg.stem+'_1080x1080.png';out=export/name
                await page.screenshot(path=str(out),clip={'x':0,'y':0,'width':1080,'height':1080})
                with Image.open(out) as im:
                    assert im.size==(1080,1080);im.verify()
                decoded=zxingcpp.read_barcodes(Image.open(out))
                qr=[r.text for r in decoded if r.format==zxingcpp.BarcodeFormat.QRCode]
                assert qr==(['https://play.google.com/store/apps/details?id=com.primo.app'] if slide['id']==5 else []),(svg.name,qr)
                checks.update({'source':str(svg.relative_to(ROOT)),'png':str(out.relative_to(ROOT)),'size':[1080,1080],
                    'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'safe_text_bounds':bounds,'decoded_download_qrs':qr})
                report['slides'].append(checks);print('Exported and verified',name,flush=True)
            assert not failures,failures
            await browser.close()
    finally:server.shutdown();server.server_close()
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

def contact(report):
    tile=420;gap=24;top=104;row_h=456
    sheet=Image.new('RGB',(tile*3+gap*4,top+row_h*2+gap*2),'#100D16');draw=ImageDraw.Draw(sheet)
    font_path=str(ROOT/'assets/fonts/SpaceGrotesk-600.ttf');title=ImageFont.truetype(font_path,30);small=ImageFont.truetype(font_path,17)
    draw.text((24,20),'AETHRA × PRIMO / FIVE-SLIDE CAROUSEL',font=title,fill='#F7F3FB')
    draw.text((24,62),'1080 × 1080 · Original master · Authentic UI · QR verified',font=small,fill='#C6B4DC')
    labels=['01 / INTRODUCTION','02 / STORE OWNER','03 / AL-BAYAN INTEGRATION','04 / CUSTOMER BENEFITS','05 / DOWNLOAD']
    for i,s in enumerate(report['slides']):
        x=gap+(i%3)*(tile+gap)
        if i>=3:x+=222
        y=top+(i//3)*row_h
        with Image.open(ROOT/s['png']) as im:sheet.paste(im.convert('RGB').resize((tile,tile),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+2,y+428),labels[i],font=small,fill='#D7C5E9')
    sheet.save(ROOT/'contact_sheet.png')
    print('Contact sheet created from the five actual PNG exports.',flush=True)

if __name__=='__main__':contact(asyncio.run(render()))
