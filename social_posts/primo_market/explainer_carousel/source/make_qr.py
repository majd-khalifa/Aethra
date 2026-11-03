"""Create and independently decode the owner's official Google Play QR target."""
from pathlib import Path
import json
import qrcode
import qrcode.image.svg
from PIL import Image
import zxingcpp

ROOT=Path(__file__).resolve().parents[1]
URL='https://play.google.com/store/apps/details?id=com.primo.app'

def main():
    target=ROOT/'assets/qr';target.mkdir(parents=True,exist_ok=True)
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,box_size=8,border=4)
    qr.add_data(URL);qr.make(fit=True)
    qr.make_image(fill_color='black',back_color='white').save(target/'google_play_qr.png')
    qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(target/'google_play_qr.svg')
    im=Image.open(target/'google_play_qr.png').convert('RGB')
    result=zxingcpp.read_barcode(im)
    assert result is not None and result.text==URL
    report={'target':URL,'decoded':result.text,'payload_matches_owner_confirmed_official_url':True,
            'format':str(result.format),'dimensions':list(im.size),'quiet_zone_modules':4,
            'error_correction':'Q','live_google_play_listing_http_checked':False,
            'status':'QR asset verified; final-slide placement and scan must be checked after layout export.'}
    (target/'qr_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
