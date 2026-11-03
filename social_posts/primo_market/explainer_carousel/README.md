# AETHRA × Primo — five-slide square carousel

Five finished PNGs are exported for visual review, each designed directly on a **1080 × 1080** canvas. This deliverable continues the owner's approved square campaign poster. Owner approval of the new carousel is pending.

## Final files

| Slide | Content | Export |
| --- | --- | --- |
| 1 | What is Primo Market? | `exports/slide_01_what_is_primo_1080x1080.png` |
| 2 | Benefits for the store owner | `exports/slide_02_store_owner_1080x1080.png` |
| 3 | Al-Bayan Al-Souri and compatible accounting systems | `exports/slide_03_al_bayan_integration_1080x1080.png` |
| 4 | Benefits for the customer | `exports/slide_04_customer_benefits_1080x1080.png` |
| 5 | Android download and verified Google Play QR | `exports/slide_05_download_1080x1080.png` |

- `contact_sheet.png`: overview made from the five actual final PNGs.
- `preview.html`: local gallery of those same PNGs. Keep it beside the folders when opening it in a browser.
- `source/slide_*.svg`: editable SVG compositions with live Arabic text and embedded fonts. Referenced images remain in `assets/`; keep the full folder together.
- `source/content.ar.json`: Arabic text and slide order.
- `QA_REPORT.md`, `validation.json`, and the source proof JSON files: visual and technical checks.
- `SHA256SUMS.txt`: checksums of the packaged project files.
- `AETHRA_PRIMO_FIVE_SQUARE_SLIDES.zip`: complete review and editing package. Extract it before editing.

## Original references and branding

All three original PNGs were extracted from the owner's `AETHRA_PRIMO_THREE_ORIGINAL_REFERENCES.zip`, decoded successfully and checked against SHA-256 hashes. They are preserved unchanged under `assets/references/`.

The approved 1080-square poster is the primary visual master. Final slides retain its chrome stage, red and violet ribbons, dark studio and original AETHRA × Primo header. The complete header logos are copied from the original poster pixels, without redrawing. The final PNG header regions match those pixels exactly; see `source/logo_pixel_proof.json`.

The Home and tea Details screens are the authentic supplied screenshots. They are placed in full, at their original aspect ratio, with uniform scaling and whole-phone rotation only. Their UI, prices and products have not been recreated or retouched. Small interface text remains part of the original screenshots; the carousel's explanatory Arabic text is separately editable.

The empty stage background is an AI-assisted cleanup of the approved poster, removing its original foreground objects and text so the five new square layouts can be composed. No generated app UI is used. See `source/asset_provenance.json` for all source details. The standalone PNGs in `assets/brand/` are unchanged repository reference assets; rendered logos use the owner's approved poster instead.

## Update the text or layout

Run these commands from this directory in a Python environment with Chromium installed:

```sh
python -m pip install -r source/requirements.txt
python source/build.py
python source/export.py
python source/package.py
```

`build.py` uses Pillow with RAQM support for Arabic text measurement. `export.py` uses Playwright with `/usr/bin/chromium`, serves the project on an ephemeral loopback HTTP port and waits for the bundled fonts before exporting. Change the Chromium executable path in that script if your system installs it elsewhere. A managed environment may require browser execution approval.

Edit Arabic strings in `source/content.ar.json`, then run the two scripts above. If changing `title`, also update its corresponding `title_lines`; if changing slide 3's `body`, keep `body_lines` consistent. The export script checks rendered SVG strings against the JSON and fails on missing text or unsafe text bounds. Layout coordinates, line wrapping and original-image placements are in `source/build.py`. Building again replaces the five generated SVGs, so preserve any manual SVG edits before rebuilding.

Bundled Cairo and Space Grotesk fonts include their OFL licenses in `assets/fonts/`. SVG support differs across illustration tools; the supplied PNGs are the verified rendering. For matching text edits, use the export script and bundled fonts.

## QR and verification

The official target supplied by the owner is:

`https://play.google.com/store/apps/details?id=com.primo.app`

Only slide 5 contains a download CTA and QR. The QR was independently decoded from the **final exported slide**, including 540 px and 360 px preview copies, to this exact URL. No QR was detected in the first four final slides. The live Google Play listing was not fetched; verification confirms the encoded destination, not store availability.

If intentionally updating the QR, edit `source/make_qr.py`, regenerate it with `python source/make_qr.py`, and export and scan the finished fifth slide again. Do not change the official target without the owner's instruction.

This task does not publish to social media or change repository history. Existing video deliverables and unrelated project files are preserved.
