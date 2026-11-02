"""Adapt the existing approved AETHRA SVG post template into six editable Arabic slides."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,copy,base64,html,hashlib,re

ROOT=Path(__file__).resolve().parent
BRAND=ROOT.parents[2]
TEMPLATE=BRAND/'03_Instagram/Templates/instagram_post_template_editable.svg'
TOKENS=BRAND/'02_Design_System/design_tokens.json'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
colors=json.loads(TOKENS.read_text())['color']
C={k:v['value'] for k,v in colors.items()}
W=C['surface'];I=C['ink'];V=C['violet-primary'];D=C['violet-deep'];S=C['violet-soft'];L=C['lavender-tint'];B=C['lavender-border'];M=C['muted-ink']
content=json.loads((ROOT/'content.ar.json').read_text())
FONTS=[('IBM Plex Sans Arabic',400,'IBMPlexSansArabic-Regular.ttf'),('IBM Plex Sans Arabic',600,'IBMPlexSansArabic-SemiBold.ttf'),('Space Grotesk',600,'SpaceGrotesk-600.ttf'),('Inter',500,'Inter-500.ttf'),('IBM Plex Mono',500,'IBMPlexMono-500.ttf')]

def make_fonts():
 return '\n'.join("@font-face{font-family:'%s';font-style:normal;font-weight:%s;src:url(data:font/ttf;base64,%s) format('truetype');}"%(fam,weight,base64.b64encode((ROOT/'assets/fonts'/filename).read_bytes()).decode()) for fam,weight,filename in FONTS)

FONT_CSS=make_fonts()
def r(x,y,w,h,fill='white',radius=16,stroke=B,sw=1.5):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x,y,xx,yy,color=B,width=2):return f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
def path(d,color=V,width=3,fill='none'):return f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"/>'
def circ(x,y,rr,fill):return f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{fill}"/>'

def tx(text,x,y,size=40,color=I,weight=400,rtl=True,anchor=None,family=None,key=None):
 anchor=anchor or 'start'
 family=family or ('IBM Plex Sans Arabic' if rtl else 'Inter')
 attrs=f' x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" direction="{"rtl" if rtl else "ltr"}"'
 if key:attrs+=f' data-copy-key="{key}"'
 # Bidi isolate Latin names inside Arabic sentences; keep live, editable text.
 pieces=re.split(r'(Aethra|UI/UX|Android & iOS|PowerPoint)',text)
 spans=[]
 for p in pieces:
  if p in ['Aethra','UI/UX','Android & iOS','PowerPoint']:
   spans.append(f'<tspan font-family="{"Space Grotesk" if p=="Aethra" else "Inter"}" font-weight="{"600" if p=="Aethra" else "500"}" direction="ltr" unicode-bidi="isolate">{html.escape(p)}</tspan>')
  else:spans.append(html.escape(p))
 return '<text'+attrs+' style="unicode-bidi:plaintext">'+''.join(spans)+'</text>'

def title(lines,y,size=64,color=I):return ''.join(tx(s,992,y+i*size*1.3,size,color,600,key=f'title_lines.{i}') for i,s in enumerate(lines))
def logo(name,x,y,width):
 source=BRAND/'01_Logo'/name;root=ET.fromstring(source.read_text());vb=[float(v) for v in root.get('viewBox').split()]
 h=width*vb[3]/vb[2];inner=''.join(ET.tostring(n,encoding='unicode') for n in root)
 # Keep original path coordinates and original viewBox. Only uniform scaling is applied.
 return f'<svg x="{x}" y="{y}" width="{width}" height="{h}" viewBox="{root.get("viewBox")}">{inner}</svg>'

def icon(kind,x,y,size=1,color=D):
 s=''
 if kind=='plan':s=r(-22,-26,44,52,'none',6,color,3)+line(-11,-10,10,-10,color,3)+line(-11,1,10,1,color,3)+line(-11,12,3,12,color,3)
 elif kind=='grid':s=''.join(r(a,b,18,18,'none',4,color,3) for a,b in [(-22,-22),(5,-22),(-22,5),(5,5)])
 elif kind=='code':s=path('M-10,-17 L-26,0 L-10,17 M10,-17 L26,0 L10,17 M4,-25 L-4,25',color,3)
 elif kind=='book':s=path('M0,-15 Q-20,-27 -30,-16 V24 Q-10,16 0,27 Q10,16 30,24 V-16 Q20,-27 0,-15 Z M0,-15 V27',color,3)
 elif kind=='deck':s=r(-29,-21,58,39,'none',5,color,3)+line(0,18,0,30,color,3)+line(-16,30,16,30,color,3)+line(-17,-8,10,-8,color,3)+line(-17,4,3,4,color,3)
 elif kind=='phone':s=r(-16,-29,32,58,'none',7,color,3)+line(-5,20,5,20,color,3)
 elif kind=='web':s=r(-29,-21,58,42,'none',6,color,3)+line(-29,-7,29,-7,color,3)+circ(-19,-14,2,color)+circ(-11,-14,2,color)
 elif kind=='chat':s=path('M-28,-20 H28 V17 H-8 L-24,30 V17 H-28 Z',color,3)+line(-15,-5,15,-5,color,3)+line(-15,6,5,6,color,3)
 elif kind=='check':s=path('M-18,0 L-4,14 L21,-16',color,4)
 return f'<g transform="translate({x},{y}) scale({size})">{s}</g>'

def base(slide,dark=False):
 original=ET.parse(TEMPLATE).getroot()
 for child in list(original):
  if child.tag.endswith('text'):original.remove(child)
 for style in list(original.iter('{'+NS+'}style')):
  style.text=FONT_CSS
 parts=[]
 for child in original:
  node=copy.deepcopy(child)
  if dark:
   for e in node.iter():
    for attr in ['fill','stroke']:
     value=e.get(attr)
     if value==W:e.set(attr,I)
     elif value==I:e.set(attr,W)
     elif value==B:e.set(attr,C['ink-border'])
     elif value in ['#F2EAFF',L]:e.set(attr,C['ink-elevated'])
  parts.append(ET.tostring(node,encoding='unicode'))
 header=tx(slide['category'],992,97,15,S if dark else D,500,False,'end','IBM Plex Mono')
 footer=tx('AETHRA',80,1265,15,W if dark else I,500,False,'start','IBM Plex Mono')
 footer+=tx(f'{int(slide["id"][:2]):02d} / 06',995,1267,16,S if dark else M,500,False,'end','IBM Plex Mono')
 return ''.join(parts)+header+footer

def devices():
 # Reuse the approved website application SVG inside a simple device frame.
 source=BRAND/'04_Brand_Applications/Website/website_desktop_hero_1440x900.svg'
 doc=ET.parse(source).getroot();inner=''.join(ET.tostring(n,encoding='unicode') for n in doc if not n.tag.endswith('defs'))
 # Original website uses the same canonical gradient id present in the parent template.
 art=r(94,645,410,300,W,20,B)+r(110,663,378,242,'white',9,B)+f'<svg x="111" y="664" width="376" height="239" viewBox="0 0 1440 900">{inner}</svg>'
 art+=path('M76,947 H522 L504,963 H94 Z',I,2,I)
 art+=r(391,784,137,257,I,23,I)+r(399,792,121,240,'white',17,'white')+r(431,800,57,10,I,5,I)
 art+=r(409,831,101,70,L,8,L)+r(420,845,75,7,V,3,V)+r(420,863,53,5,S,3,S)
 for j in range(3):art+=r(410,916+j*29,97,21,L,5,L)+circ(423,926+j*29,5,V)+r(437,921+j*29,55,4,M,2,M)
 art+=tx('تصوّر توضيحي',300,1102,25,M,400,True,'middle')
 return art

def draw(s):
 n=int(s['id'][:2]);dark=n==5;out=base(s,dark)
 if n==1:
  out+=r(88,176,904,430,'white',18,B)
  out+='<polygon points="750,176 992,176 992,606 590,606" fill="'+L+'"/>'
  out+=logo('SVG/aethra_lockup_stacked_color_light.svg',270,190,540)
  out+=title(s['title_lines'],722,76)
  out+=''.join(tx(x,992,830+i*75,56,I,400,key=f'subtitle_lines.{i}') for i,x in enumerate(s['subtitle_lines']))
  out+=r(88,1040,904,106,L,14,B)+tx(s['support'],540,1103,34,D,400,True,'middle',key='support')
  out+=tx('اسحب للتعرّف على خدماتنا',992,1190,26,M,400)
 elif n==2:
  out+=title(s['title_lines'],235,62)
  icons=['code','plan','grid','code','book','deck']
  for j,text in enumerate(s['bullets']):
   yy=400+j*105
   out+=r(88,yy,904,87,'white' if j%2 else L,14,B)
   out+=r(914,yy+19,50,50,'white',12,B)+icon(icons[j],939,yy+44,.55)
   out+=tx(text,890,yy+56,40,I,400,key=f'bullets.{j}')
   out+=tx(f'{j+1:02d}',120,yy+51,17,D,500,False,'start','IBM Plex Mono')
  out+=r(88,1070,904,112,D,16,D)+tx(s['footer'],540,1136,32,'white',600,True,'middle',key='footer')
 elif n==3:
  out+=title(s['title_lines'],235,64)
  out+=''.join(tx(x,992,419+i*55,36,M,400,key=f'body_lines.{i}') for i,x in enumerate(s['body_lines']))
  out+=devices()
  for j,text in enumerate(s['bullets']):
   yy=630+j*104
   out+=circ(965,yy-14,19,L)+icon('check',965,yy-14,.36)
   out+=tx(text,922,yy,33,I,400,key=f'bullets.{j}')
 elif n==4:
  out+=title(s['title_lines'],260,84)
  icons=['grid','phone','web','grid','book','deck']
  for j,lines in enumerate(s['card_lines']):
   xx=548 if j%2==0 else 88;yy=350+(j//2)*220
   out+=r(xx,yy,444,200,L if j==0 else 'white',16,V if j==0 else B)
   out+=r(xx+356,yy+22,62,56,'white' if j==0 else L,12,B)+icon(icons[j],xx+387,yy+50,.63)
   for k,text in enumerate(lines):
    lat=text in ['UI/UX','Android & iOS']
    out+=tx(text,xx+416,yy+119+k*46,36,D if lat else I,500 if lat else 400,not lat,'end' if lat else 'start', 'Inter' if lat else None,key=f'card_lines.{j}.{k}')
   out+=tx(f'{j+1:02d}',xx+24,yy+54,15,D,500,False,'start','IBM Plex Mono')
  out+=r(88,1025,904,78,I,14,I)+icon('chat',947,1064,.5,S)+tx(s['bullets'][6],895,1076,35,W,400,key='bullets.6')
  out+=tx(s['footer'],992,1172,28,M,400,key='footer')
 elif n==5:
  out+=title(s['title_lines'],280,78,W)
  for j,text in enumerate(s['bullets']):
   yy=420+j*137
   out+=line(88,yy+47,992,yy+47,C['ink-border'],1.5)
   out+=circ(962,yy-15,23,C['ink-elevated'])+icon('check',962,yy-15,.5,S)
   out+=tx(text,907,yy,38,W,400,key=f'bullets.{j}')
   out+=tx(f'{j+1:02d}',105,yy-6,16,S,500,False,'start','IBM Plex Mono')
  out+=tx(s['footer'],540,1180,31,S,400,True,'middle',key='footer')
 elif n==6:
  out+=logo('SVG/aethra_symbol_color.svg',778,174,215)
  out+=title(s['title_lines'],514,83)
  out+=''.join(tx(x,992,790+i*64,40,M,400,key=f'body_lines.{i}') for i,x in enumerate(s['body_lines']))
  out+=r(88,971,904,142,D,16,D)+tx(s['cta'],540,1060,44,W,600,True,'middle',key='cta')
  out+=tx(s['support'],540,1174,29,I,500,False,'middle','Inter',key='support')
 desc=' '.join(s['title_lines'])
 return f'<svg xmlns="{NS}" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1350" viewBox="0 0 1080 1350" role="img" aria-labelledby="title desc"><title id="title">{html.escape(desc)}</title><desc id="desc">AETHRA introductory carousel, slide {n} of 6. Editable live text and vector artwork adapted from the approved Instagram template.</desc>'+out+'</svg>'

def main():
 assert len(content['slides'])==6
 for s in content['slides']:
  target=ROOT/'source'/('slide_'+s['id']+'.svg');target.write_text(draw(s));ET.parse(target)
  print('Built',target.name)
 provenance={'template':str(TEMPLATE.relative_to(BRAND)),'template_sha256':hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),'tokens':str(TOKENS.relative_to(BRAND)),'tokens_sha256':hashlib.sha256(TOKENS.read_bytes()).hexdigest(),'logo_sources':['01_Logo/SVG/aethra_lockup_stacked_color_light.svg','01_Logo/SVG/aethra_symbol_color.svg'],'illustration_source':'04_Brand_Applications/Website/website_desktop_hero_1440x900.svg','note':'Illustrative device mockup, not a completed client project.'}
 (ROOT/'source_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
