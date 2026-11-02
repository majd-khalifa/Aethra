"""Read-only source-to-production asset verification and icon map generation."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
REF=Path('D:/MAJD Files/Projects/Collage Projects/Production_Ready_Projects/Primo/frontend/Primo')
icons=Path('C:/flutter/packages/flutter/lib/src/material/icons.dart').read_text()
names=['person','person_outline','notifications_none_rounded','arrow_back_rounded','favorite_border_outlined','search','home_rounded','shopping_cart_outlined','receipt_long','receipt_long_outlined','widgets_outlined','add','remove','delete_outline','location_on','check_circle','radio_button_unchecked','local_shipping','storefront_outlined','shopping_bag_outlined','schedule_rounded','arrow_forward','star_rate','edit_note_rounded','qr_code_2_rounded','filter_list_rounded']
mapping={name:int(re.search(r'\b'+name+r'\s*=\s*IconData\(\s*0x([a-f0-9]+)',icons).group(1),16) for name in names}
(ROOT/'src/material-icons.json').write_text(json.dumps(mapping,indent=2))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assets=[]
for p in (ROOT/'public/primo').glob('*'):
 source=REF/'assets/images'/p.name
 assert sha(p)==sha(source)
 assets.append({'asset':str(p.relative_to(ROOT)),'source':str(source.relative_to(REF)),'sha256':sha(p),'byte_identical':True})
for p in (ROOT/'public/fonts').glob('Cairo*'):
 assert sha(p)==sha(REF/'assets/fonts'/p.name)
assets.append({'asset':'public/brand/primo-original.png','source':'assets/images/logo.png','sha256':sha(ROOT/'public/brand/primo-original.png'),'byte_identical':sha(ROOT/'public/brand/primo-original.png')==sha(REF/'assets/images/logo.png')})
(ROOT/'qa/recreated-ui-assets.json').write_text(json.dumps(assets,indent=2))
print('Verified original UI imagery/fonts; mapped',len(mapping),'Material icon glyphs.')
