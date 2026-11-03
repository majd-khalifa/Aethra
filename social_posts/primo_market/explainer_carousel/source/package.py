"""Package the existing final assets, without rebuilding or changing the PNGs."""
from pathlib import Path
import hashlib
import io
import json
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'AETHRA_PRIMO_FIVE_SQUARE_SLIDES.zip'
MANIFEST = ROOT / 'SHA256SUMS.txt'
TOP_LEVEL = {'README.md', 'QA_REPORT.md', 'preview.html', 'contact_sheet.png', 'validation.json'}


def include(path):
    rel = path.relative_to(ROOT)
    return (path.is_file() and not any(part.startswith('.') or part == '__pycache__' for part in rel.parts)
            and path.suffix != '.pyc'
            and (rel.parts[0] in {'assets', 'source', 'exports'} or rel.as_posix() in TOP_LEVEL))


def main():
    report = json.loads((ROOT / 'validation.json').read_text())
    exports = sorted((ROOT / 'exports').glob('*.png'))
    assert len(exports) == len(report['slides']) == 5
    assert {p.relative_to(ROOT).as_posix() for p in exports} == {s['png'] for s in report['slides']}
    for slide in report['slides']:
        path = ROOT / slide['png']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == slide['sha256']
        with Image.open(path) as im:
            assert im.size == (1080, 1080)
            im.verify()
    files = sorted(p for p in ROOT.rglob('*') if include(p))
    MANIFEST.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n' for p in files))
    files.append(MANIFEST)
    prefix = 'AETHRA_PRIMO_FIVE_SQUARE_SLIDES/'
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            archive.write(path, prefix + path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {prefix + p.relative_to(ROOT).as_posix() for p in files}
        for path in files:
            assert hashlib.sha256(archive.read(prefix + path.relative_to(ROOT).as_posix())).digest() == hashlib.sha256(path.read_bytes()).digest()
        for path in exports:
            with Image.open(io.BytesIO(archive.read(prefix + path.relative_to(ROOT).as_posix()))) as im:
                assert im.size == (1080, 1080)
                im.verify()
    print(json.dumps({'zip': str(ARCHIVE), 'bytes': ARCHIVE.stat().st_size,
                      'sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                      'files': len(files), 'final_slides': 5, 'crc': 'passed', 'byte_integrity': 'passed'}, indent=2))


if __name__ == '__main__':
    main()
