from pathlib import Path
import hashlib,json,zipfile,subprocess
root=Path(__file__).resolve().parents[1]
repo=root.parent
reference=Path('C:/Users/MVJD/.codex/tmp/primo-reference-20261102')
apk=Path('C:/Users/MVJD/Desktop/Primo_References/primo-reference.apk')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primo=root/'public/brand/primo-original.png'
aethra=root/'public/brand/aethra-approved.png'
with zipfile.ZipFile(apk) as z:
    logo=z.read('assets/flutter_assets/assets/images/logo.png')
    apk_logo_hash=hashlib.sha256(logo).hexdigest()
assert sha(primo)==sha(reference/'Primo/assets/images/logo.png')==apk_logo_hash
assert sha(aethra)==sha(repo/'06_Approved_Identity_Production/01_Logo/PNG/aethra_lockup_horizontal_color_light_1024.png')
data={
 'apk':{'path':str(apk),'sha256':sha(apk),'bytes':apk.stat().st_size,'package':'com.primo.app','versionName':'1.0.0','versionCode':3,'minSdk':24,'targetSdk':36,'activity':'com.primo.app.MainActivity','included_in_repository':False},
 'primo_reference':{'repository':'majd-khalifa/Primo-market','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=reference,text=True).strip(),'tracked_status':subprocess.check_output(['git','status','--short'],cwd=reference,text=True).strip()},
 'brands':[{'file':str(primo.relative_to(root)),'sha256':sha(primo),'unchanged_from_repo_and_apk':True},{'file':str(aethra.relative_to(root)),'sha256':sha(aethra),'unchanged_from_approved_master':True}],
 'screens':[{'file':str(p.relative_to(root)),'sha256':sha(p),'source':'adb screencap, supplied unmodified APK on Pixel_7 emulator','edited':False} for p in sorted((root/'public/app').glob('*.png'))],
 'voice':'No authenticated Syrian actor available; subtitle-led version, original music and procedural Foley. Daughter has only synthesized nonverbal sigh.'
}
(root/'qa/provenance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(data,ensure_ascii=False,indent=2))
