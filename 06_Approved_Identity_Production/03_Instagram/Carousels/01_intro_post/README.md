# AETHRA — 01 / Arabic introductory carousel

Six 1080 × 1350 slides for Instagram and Facebook, in posting order `01` through `06`.

- `exports/`: six final PNGs, ready for carousel upload.
- `source/`: six editable SVGs with live Arabic/English text and embedded fonts.
- `contact_sheet.jpg`: preview assembled from the actual exported slides.
- `preview.html`: local gallery with links to each PNG and editable SVG.
- `content.ar.json`: Arabic text and deliberate headline/card line breaks.
- `caption.ar.txt` and `hashtags.txt`: suggested post copy.
- `assets/fonts/`: bundled typefaces and SIL Open Font License notices.
- `validation.json`: dimensions, font coverage, text bounds, and export hashes.
- `source_provenance.json`: reused repository assets and source hashes.

## Brand assets reused

The design adapts `03_Instagram/Templates/instagram_post_template_editable.svg`, preserving its 48 px frame, header/footer structure, 88 px content margin, outlined wordmark, and violet/lavender visual language. The services grid follows `03_Instagram/Posts_1080x1350/post_02_services_1080x1350.svg`. Cover and CTA composition follow the approved introduction and CTA posts. All colors come from `02_Design_System/design_tokens.json`.

The original stacked logo and symbol are embedded as unmodified vector geometry with uniform scaling. Slide 3 reuses the approved website hero inside an illustrative device frame, explicitly labeled **تصوّر توضيحي**. It is not presented as a completed client project. No testimonials, performance statistics, client names, published-product claims, or contact details are invented.

Arabic uses **IBM Plex Sans Arabic Regular/SemiBold**, continuing the companion typeface selected for the Aethra Reel. English uses Space Grotesk/Inter; structural labels use IBM Plex Mono. The Arabic fonts and license notices come from the official Google Fonts repository; Latin font files are copied from the existing approved brand package. Font files retain their license terms.

## Update text and export

Edit `content.ar.json`. `title_lines`, `subtitle_lines`, `body_lines`, and `card_lines` control deliberate line breaks. Slide 4's first six `card_lines` entries must still read as the corresponding `bullets` entry when joined; the seventh bullet is the full-width consulting row. Then run from this directory:

```sh
python build.py
python export.py
```

`build.py` uses the original approved template and brand assets elsewhere in this repository, so keep this folder in its existing location. `export.py` needs Python with Pillow, fonttools, Playwright, and Chromium at `/usr/bin/chromium`. It renders the SVGs directly; no external font requests or running web server are required. The managed command sandbox may require approval for Chromium startup.

For direct visual editing, open a file from `source/` in a vector editor and install the bundled fonts first if that editor ignores SVG-embedded fonts. Edit live text while preserving RTL direction. Direct SVG edits should be followed by `python export.py` only; running `build.py` regenerates SVGs from the JSON and replaces direct SVG edits. Recheck any longer copy for fit.

Open `preview.html` after downloading the folder to view the gallery. GitHub's source view does not execute HTML. Upload only the six final PNGs, in filename order; the contact sheet is a review image, not a seventh slide.

All pre-existing repository files and approved assets are left unchanged. The carousel is an introductory description of the offered services, not a portfolio of verified completed work.
