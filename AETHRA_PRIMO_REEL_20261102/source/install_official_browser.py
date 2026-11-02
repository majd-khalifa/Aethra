"""Install only the official Remotion browser downloaded by resume-browser.cjs.
Validates archive CRC and executable version before marking cache ready.
No alternate browser or render executable override is used.
"""
from pathlib import Path
import zipfile,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
cache=ROOT/'node_modules/.remotion/chrome-headless-shell'
archive=cache/'chromium-headless-shell-win-x64-158.0.8127.2.zip'
assert archive.stat().st_size==137435497,'Official archive download is not complete'
target=cache/'win64'
assert not target.exists(),'Do not overwrite a browser installation'
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None,'Archive CRC failure'
 for name in z.namelist():
  resolved=(target/name).resolve()
  assert resolved.is_relative_to(target.resolve()),'Unsafe zip member'
 z.extractall(target)
exe=target/'chrome-headless-shell-win64/chrome-headless-shell.exe'
assert exe.is_file()
version=subprocess.check_output([str(exe),'--version'],text=True).strip()
assert '158.0.8127.2' in version,version
script="const p=require('path');const b=require(p.resolve('node_modules/@remotion/renderer/dist/browser/BrowserFetcher.js'));process.stdout.write(b.getExpectedVersion({version:null,chromeMode:'headless-shell',platform:'win64'}));"
marker=subprocess.check_output(['node','-e',script],cwd=ROOT,text=True)
(cache/'VERSION').write_text(marker,encoding='utf-8')
(ROOT/'qa/official-browser.json').write_text(json.dumps({'source':'https://remotion.media/chromium-headless-shell-win-x64-158.0.8127.2.zip?clear','bytes':archive.stat().st_size,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'crc_verified':True,'executable_version':version,'remotion_cache_marker':marker,'renderer_browser_executable_override':False},indent=2))
print(version,'installed in the standard Remotion cache')
