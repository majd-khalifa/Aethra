"""Build five native 1080-square editable SVGs from original campaign references."""
from pathlib import Path
from html import escape
import base64
import json
from PIL import ImageFont

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'source/content.ar.json').read_text())
MASTER='../assets/references/01_Approved_AETHRA_Primo_Square_Poster.png'
HOME='../assets/references/02_Primo_Authentic_Home.png'
DETAIL='../assets/references/03_Primo_Authentic_Tea_Product_Details.png'
SLUGS=['what_is_primo','store_owner','al_bayan_integration','customer_benefits','download']

def font_file(weight):
    return ROOT/'assets/fonts'/({400:'Cairo-Regular.ttf',600:'Cairo-SemiBold.ttf',700:'Cairo-Bold.ttf'}[weight])

def width(text,size,weight=600):
    font=ImageFont.truetype(str(font_file(weight)),size)
    return font.getlength(text,direction='rtl',language='ar')

def wrap(text,max_width,size,weight=600):
    if width(text,size,weight)<=max_width:return [text]
    words=text.split();candidates=[]
    for i in range(1,len(words)):
        first=' '.join(words[:i]);second=' '.join(words[i:])
        a=width(first,size,weight);b=width(second,size,weight)
        if max(a,b)<=max_width:candidates.append((abs(a-b)+(60 if b>a else 0),first,second))
    if candidates:
        _,first,second=min(candidates);return [first,second]
    lines=[];line=''
    for word in text.split():
        proposed=(line+' '+word).strip()
        if line and width(proposed,size,weight)>max_width:
            lines.append(line);line=word
        else:line=proposed
    if line:lines.append(line)
    return lines

def ar(text,x,y,size=30,weight=600,fill='#F8F5FB',anchor='start',key=None,extra=''):
    family='Cairo SemiBold' if weight==600 else 'Cairo'
    attrs=f' data-copy="{escape(key)}"' if key else ''
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" direction="rtl" unicode-bidi="plaintext" text-anchor="{anchor}" data-safe="1"{attrs} {extra}>{escape(text)}</text>'

def en(text,x,y,size=16,fill='#D2C4E4',anchor='start',extra=''):
    return f'<text x="{x}" y="{y}" font-family="Space Grotesk SemiBold" font-size="{size}" font-weight="600" fill="{fill}" text-anchor="{anchor}" direction="ltr" data-safe="1" {extra}>{escape(text)}</text>'

def fonts():
    specs=[('Cairo',400,'Cairo-Regular.ttf'),('Cairo SemiBold',600,'Cairo-SemiBold.ttf'),
           ('Cairo',700,'Cairo-Bold.ttf'),('Space Grotesk SemiBold',600,'SpaceGrotesk-600.ttf')]
    css=''
    for family,weight,name in specs:
        data=base64.b64encode((ROOT/'assets/fonts'/name).read_bytes()).decode()
        css+=f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/ttf;base64,{data}) format('truetype');}}"
    return '<style>'+css+'text{font-kerning:normal;text-rendering:optimizeLegibility}</style>'

DEFS='''
<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".40" stop-color="#FAFAFC"/><stop offset=".62" stop-color="#C2BFCA"/><stop offset=".84" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DDD5E7"/></linearGradient>
<linearGradient id="frameSteel" x1="0" y1="0" x2="1" y2=".4"><stop stop-color="#EDC1C8"/><stop offset=".15" stop-color="#E8E5EB"/><stop offset=".42" stop-color="#5C5660"/><stop offset=".70" stop-color="#211C26"/><stop offset="1" stop-color="#AF8CE0"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#312935" stop-opacity=".88"/><stop offset=".35" stop-color="#17131D" stop-opacity=".94"/><stop offset="1" stop-color="#100D14" stop-opacity=".94"/></linearGradient>
<linearGradient id="glassEdge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#B9A5CC" stop-opacity=".70"/><stop offset=".4" stop-color="#786681" stop-opacity=".2"/><stop offset="1" stop-color="#BE929B" stop-opacity=".48"/></linearGradient>
<linearGradient id="violetRed" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#A87CF5"/><stop offset=".7" stop-color="#A87CF5"/><stop offset="1" stop-color="#D95163"/></linearGradient>
<linearGradient id="headerH" gradientUnits="userSpaceOnUse" x1="265" x2="815"><stop stop-color="white" stop-opacity="0"/><stop offset=".045" stop-color="white"/><stop offset=".955" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
<linearGradient id="headerV" gradientUnits="userSpaceOnUse" x1="0" x2="0" y1="8" y2="136"><stop stop-color="white" stop-opacity="0"/><stop offset=".0625" stop-color="white"/><stop offset=".9375" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
<mask id="headerMaskH" maskUnits="userSpaceOnUse"><rect x="265" y="8" width="550" height="128" fill="url(#headerH)"/></mask>
<mask id="headerMaskV" maskUnits="userSpaceOnUse"><rect x="265" y="8" width="550" height="128" fill="url(#headerV)"/></mask>
<filter id="titleDepth" x="-10%" y="-30%" width="120%" height="170%"><feDropShadow dx="0" dy="2" stdDeviation="1" flood-color="#000000" flood-opacity=".85"/></filter>
<filter id="shadow" x="-35%" y="-25%" width="170%" height="160%"><feDropShadow dx="0" dy="11" stdDeviation="10" flood-color="#000000" flood-opacity=".85"/></filter>
<filter id="redGlow" x="-45%" y="-30%" width="190%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="floorShadow" x="-35%" y="-100%" width="170%" height="300%"><feGaussianBlur stdDeviation="8"/></filter>
<marker id="flowArrow" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M1 1 L7 5 L1 9" fill="none" stroke="#B48BF8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>
'''

def header():
    # Original poster pixels, including both complete approved logos. No regenerated logo art.
    return f'<g transform="translate(0 52)" data-brand-source="approved-master-pixels"><g mask="url(#headerMaskH)"><g mask="url(#headerMaskV)"><image href="{MASTER}" x="0" y="0" width="1080" height="1080"/></g></g></g>'

def sprite(vb,x,y,w,h,rounded=0):
    node=f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" preserveAspectRatio="xMidYMid meet" overflow="hidden" data-brand-source="approved-master-pixels"><image href="{MASTER}" width="1080" height="1080" x="0" y="0"/></svg>'
    if rounded:
        ident=f'spriteClip{int(x)}{int(y)}'
        node=f'<defs><clipPath id="{ident}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rounded}"/></clipPath></defs><g clip-path="url(#{ident})">{node}</g>'
    return node

def phone(key,x,y,screen_w,angle=0):
    h=screen_w*1280/576;pad=12;w=screen_w+pad*2;total_h=h+pad*2
    href=HOME if key=='home' else DETAIL
    cx=x+w/2;cy=y+total_h/2
    parts=[f'<ellipse cx="{cx:.3f}" cy="877" rx="{w*.49:.3f}" ry="12" fill="#08060C" opacity=".8" filter="url(#floorShadow)"/>',
           f'<g transform="rotate({angle} {cx:.4f} {cy:.4f})" data-phone="{key}">',
           f'<rect x="{x-2}" y="{y-2}" width="{w+4:.4f}" height="{total_h+4:.4f}" rx="32" fill="none" stroke="#C63848" stroke-width="5" opacity=".32" filter="url(#redGlow)"/>',
           f'<rect x="{x}" y="{y}" width="{w:.4f}" height="{total_h:.4f}" rx="29" fill="#0B090F" stroke="url(#frameSteel)" stroke-width="5" filter="url(#shadow)"/>',
           f'<rect x="{x+5}" y="{y+5}" width="{w-10:.4f}" height="{total_h-10:.4f}" rx="24" fill="#0C0A10" stroke="#6C5D72" stroke-opacity=".75" stroke-width=".8"/>',
           # The ENTIRE original screenshot is fit at its native aspect ratio, with no mask/filter or retouching.
           f'<image href="{href}" x="{x+pad}" y="{y+pad}" width="{screen_w}" height="{h:.8f}" preserveAspectRatio="xMidYMid meet" data-authentic-ui="{key}" data-source-aspect="576/1280"/>',
           f'<path d="M{x+17} {y+5} H{x+w-23}" stroke="#FFFFFF" stroke-opacity=".72" stroke-width="1.4" stroke-linecap="round"/>',
           f'<path d="M{x-1} {y+34} V{y+total_h-36:.3f}" stroke="#E76C75" stroke-opacity=".8" stroke-width="1.5"/>',
           '</g>']
    return ''.join(parts)

def features(slide,x=592,y=382,w=412,h=96,gap=14,size=30):
    out=''
    for i,text in enumerate(slide['bullets']):
        yy=y+i*(h+gap)
        lines=wrap(text,w-64,size)
        assert len(lines)<=2,(slide['id'],text,lines)
        out+=f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="18" fill="url(#glass)" stroke="url(#glassEdge)" stroke-width=".85"/>'
        out+=f'<path d="M{x+23} {yy+1.5} H{x+w-23}" stroke="#D6C4E8" stroke-width=".65" opacity=".19"/>'
        out+=f'<rect x="{x+w-9}" y="{yy+28}" width="2" height="{h-56}" rx="1" fill="#AD85EE" opacity=".7"/>'
        out+=en(f'{i+1:02d}',x+20,yy+h/2+5,14,fill='#B5A0CD')
        line_height=min(40,size*1.35)
        baseline=yy+h/2+size*.3-(len(lines)-1)*line_height/2
        for j,line in enumerate(lines):out+=ar(line,x+w-25,baseline+j*line_height,size,600,key=f'bullets.{i}.{j}')
    return out

def common(slide):
    out=f'<image href="../assets/art/approved_campaign_empty_stage.png" width="1080" height="1080" preserveAspectRatio="xMidYMid meet"/>'
    out+=header()
    if slide['id']==5:
        out+=ar(slide['title'],540,235,58,700,fill='url(#chrome)',anchor='middle',key='title',extra='filter="url(#titleDepth)"')
        out+=ar(slide['support'],540,292,28,600,anchor='middle',key='support')
    else:
        out+=ar(slide['title'],1004,235,58,700,fill='url(#chrome)',key='title',extra='filter="url(#titleDepth)"')
        out+=ar(slide['support'],1004,292,28,400,key='support')
        out+='<path d="M908 318 H1004" stroke="url(#violetRed)" stroke-width="2" stroke-linecap="round"/>'
    return out

def integration(slide):
    out=''
    for j,line in enumerate(slide['body_lines']):out+=ar(line,1004,337+j*37,26,600,fill='#E4DAEC',key=f'body.{j}')
    out+=phone('home',119,448,180)
    out+=f'<rect x="503" y="401" width="501" height="122" rx="22" fill="url(#glass)" stroke="url(#glassEdge)" stroke-width="1.2" data-concept-only="store-accounting-system"/>'
    out+=ar('البيان السوري',978,447,32,700)
    out+=ar('ونظام المحاسبة المتوافق',978,488,23,400,fill='#D0BFE0')
    out+='<path d="M492 460 C415 460 405 514 345 554" fill="none" stroke="#A87EF0" stroke-width="2.3" marker-end="url(#flowArrow)"/>'
    out+='<circle cx="422" cy="481" r="4" fill="#CCACEF"/><circle cx="384" cy="522" r="3" fill="#CF5867"/>'
    out+=features(slide,x=500,y=550,w=504,h=78,gap=10,size=25)
    out+=en('Primo Market',221,916,21,fill='#F6EFFC',anchor='middle',extra='filter="url(#titleDepth)"')
    return out

def download(slide):
    out=phone('home',112,447,176,-7)
    out+='<rect x="331" y="347" width="418" height="418" rx="32" fill="none" stroke="#E33B4A" stroke-width="7" opacity=".40" filter="url(#redGlow)"/>'
    out+='<rect x="334" y="350" width="412" height="412" rx="30" fill="#F8F7FA" stroke="url(#frameSteel)" stroke-width="7" filter="url(#shadow)"/>'
    out+='<rect x="346" y="362" width="388" height="388" rx="21" fill="#FFFFFF"/>'
    out+='<image href="../assets/qr/google_play_qr.png" x="360" y="376" width="360" height="360" image-rendering="pixelated" data-download-qr="1"/>'
    out+=sprite('220 148 239 222',805,480,188,174,rounded=43)
    out+=ar('امسح الرمز للتحميل',540,823,30,700,anchor='middle',extra='filter="url(#titleDepth)"')
    # Preserve the original approved Android/package pills as complete, unaltered poster elements.
    out+='<defs><clipPath id="originalFooterPills"><rect x="203" y="925" width="328" height="67" rx="34"/><rect x="557" y="925" width="323" height="67" rx="34"/></clipPath></defs>'
    out+=f'<g clip-path="url(#originalFooterPills)" data-brand-source="approved-master-pixels"><image href="{MASTER}" x="0" y="-40" width="1080" height="1080"/></g>'
    return out

def footer(i):
    return en(f'{i:02d} / 05',76,1002,16)+en('AETHRA × PRIMO',1004,1002,16,anchor='end')

def main():
    assert DATA['canvas']['width']==DATA['canvas']['height']==1080
    assert len(DATA['slides'])==5 and [s['id'] for s in DATA['slides'] if s['download_cta']]==[5]
    for i,slide in enumerate(DATA['slides'],1):
        out=common(slide)
        if i==1:out+=phone('home',92,427,190,-3)+phone('details',328,392,206,3)+features(slide)
        elif i==2:out+=phone('details',143,323,238,-3)+features(slide,x=502,y=375,w=502,h=96,gap=14,size=30)
        elif i==3:out+=integration(slide)
        elif i==4:out+=phone('home',112,345,228,-3)+phone('details',390,504,156,3)+features(slide)
        else:out+=download(slide)
        if i<5:out+=footer(i)
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080" role="img" aria-label="{escape(slide["title"])}">{fonts()}<defs>{DEFS}</defs>{out}</svg>'
        name=f'slide_{i:02d}_{SLUGS[i-1]}.svg';(ROOT/'source'/name).write_text(svg)
        print('Built',name)

if __name__=='__main__':main()
