"""Render editable SVGs with correct Arabic shaping and inspect text bounds."""
from pathlib import Path
import asyncio,json,hashlib,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
async def main():
 files=sorted((ROOT/'source').glob('slide_*.svg'));assert len(files)==6
 content=json.loads((ROOT/'content.ar.json').read_text())
 arabic={c for c in json.dumps(content,ensure_ascii=False) if '\u0600'<=c<='\u06ff'}
 for font in ['IBMPlexSansArabic-SemiBold.ttf','IBMPlexSansArabic-Regular.ttf']:
  cmap=TTFont(ROOT/'assets/fonts'/font).getBestCmap()
  assert all(ord(c) in cmap for c in arabic),'Arabic glyph missing in '+font
 for slide,source in zip(content['slides'],files):
  root=ET.parse(source).getroot()
  copy={t.get('data-copy-key'):''.join(t.itertext()) for t in root if t.get('data-copy-key')}
  for field in ['title_lines','subtitle_lines','body_lines']:
   for j,text in enumerate(slide.get(field,[])):assert copy[f'{field}.{j}']==text
  for field in ['support','footer','cta']:
   if field in slide:assert copy[field]==slide[field]
  for j,text in enumerate(slide.get('bullets',[])):
   if 'card_lines' in slide and j<6:
    parts=[copy[f'card_lines.{j}.{k}'] for k in range(len(slide['card_lines'][j]))]
    assert ' '.join(parts)==text
   else:assert copy[f'bullets.{j}']==text
 report={'canvas':[1080,1350],'slides':[],'source_copy_check':'all titles, bodies, bullet items, footers and CTAs match content.ar.json','arabic_glyph_coverage':'all source Arabic characters covered in both Arabic fonts','sources':'editable SVG with embedded fonts; content.ar.json'}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1080,'height':1350},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for source in files:
   ET.parse(source)
   await page.set_content('<html><head><meta charset="utf-8"><style>html,body{margin:0;width:1080px;height:1350px;overflow:hidden;background:#FCFBFF}</style></head><body>'+source.read_text()+'</body></html>',wait_until='load')
   for font in ["600 64px 'IBM Plex Sans Arabic'","400 40px 'IBM Plex Sans Arabic'","600 76px 'Space Grotesk'","500 16px 'IBM Plex Mono'","500 36px Inter"]:await page.evaluate('(s)=>document.fonts.load(s)',font)
   await page.evaluate('document.fonts.ready')
   info=await page.evaluate('''()=>({fonts:document.fonts.check("600 64px 'IBM Plex Sans Arabic'")&&document.fonts.check("400 40px 'IBM Plex Sans Arabic'"),bounds:Array.from(document.querySelectorAll('body > svg > text')).map(t=>{let b=t.getBBox();return {text:t.textContent,x:b.x,y:b.y,width:b.width,height:b.height,key:t.getAttribute('data-copy-key')}})})''')
   assert info['fonts']
   bad=[b for b in info['bounds'] if b['x']<63 or b['x']+b['width']>1015 or b['y']<63 or b['y']+b['height']>1290]
   if bad:raise RuntimeError(source.name+' has out-of-safe-area text: '+json.dumps(bad,ensure_ascii=False))
   out=ROOT/'exports'/(source.stem+'_1080x1350.png')
   await page.screenshot(path=str(out),type='png',animations='disabled')
   with Image.open(out) as im:assert im.size==(1080,1350)
   report['slides'].append({'source':str(source.relative_to(ROOT)),'png':str(out.relative_to(ROOT)),'size':[1080,1350],'safe_area_check':'passed','text_bounds':info['bounds'],'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
   print('Exported',out.name,'with Arabic fonts and safe-area checks',flush=True)
  assert not errors,errors
  await browser.close()
 # Preview is assembled from actual final PNGs.
 w,h,gap,top=510,638,30,100
 contact=Image.new('RGB',(3*w+4*gap,2*h+3*gap+top+66),'#F2EDFF');d=ImageDraw.Draw(contact)
 f=ImageFont.truetype(str(ROOT/'assets/fonts/SpaceGrotesk-600.ttf'),28)
 body=ImageFont.truetype(str(ROOT/'assets/fonts/Inter-500.ttf'),17)
 d.text((30,22),'AETHRA / FIRST INTRODUCTORY CAROUSEL',font=f,fill='#171327')
 d.text((30,62),'6 slides · 1080 × 1350 · Arabic first · Approved violet / lavender identity',font=body,fill='#615B73')
 for n,item in enumerate(report['slides']):
  with Image.open(ROOT/item['png']) as im:thumb=im.convert('RGB').resize((w,h),Image.Resampling.LANCZOS)
  x=gap+(n%3)*(w+gap);y=top+gap+(n//3)*(h+gap+24)
  contact.paste(thumb,(x,y));d.text((x+4,y+h+7),f'{n+1:02d} / 06',font=body,fill='#615B73')
 contact.save(ROOT/'contact_sheet.jpg',quality=95,subsampling=0)
 report['contact_sheet']='contact_sheet.jpg'
 (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('Contact sheet and validation.json saved',flush=True)

if __name__=='__main__':asyncio.run(main())
