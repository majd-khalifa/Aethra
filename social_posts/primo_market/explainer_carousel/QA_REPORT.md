# Final carousel QA

Status: final assets exported for owner review; visual approval is pending.

| Check | Result |
| --- | --- |
| Deliverable count | Exactly five final PNGs and five editable SVGs |
| Canvas | All five sources and final exports are native 1080 × 1080, 1:1; no portrait-to-square crops |
| Original inputs | All three supplied PNGs readable; archive CRC and original SHA-256 values verified |
| Art direction | Approved poster's dark studio, chrome podium, red/violet ribbons and AETHRA × Primo branding retained consistently |
| Logos | Original poster header pixels preserved; all five exported header cores match exactly, maximum RGB difference 0 |
| Real Primo UI | Full authentic Home and tea Details screenshots used; source files unchanged; aspect ratios preserved, no screen redraw or retouch |
| Arabic | All five full-size rendered slides manually inspected for connected glyphs, RTL reading, line breaks, contrast and alignment; bundled Cairo fonts cover all Arabic copy |
| Safe area | All live text bounding boxes fall within a 72 px inset; complete logos and CTA remain safely inside the canvas |
| Slide 3 | Names Al-Bayan Al-Souri and a compatible store accounting system, explains price/quantity sync and reduced repeated entry; diagram uses labels and authentic Primo UI rather than fabricated accounting screens |
| Audience benefits | Slide 2 covers the store owner; slide 4 covers the ordinary customer |
| CTA placement | Final download CTA and QR only on slide 5; no QR detected in slides 1–4 |
| QR destination | Decodes from the final slide at 1080, 540 and 360 px to the owner's exact Google Play URL |
| Contact sheet | Assembled from the five actual final PNGs |

Evidence: `validation.json`, `source/reference_manifest.json`, `source/logo_pixel_proof.json`, `source/qr_export_proof.json` and `source/asset_provenance.json`.

The authentic screenshots include their original product names, prices, system status bars and small UI labels. These have deliberately been preserved. They are visual references, not a claim that a historical displayed price is current. The main explanatory copy is kept larger for carousel reading.

No clipping, broken Arabic glyphs or missing assets were found in the final rendered slides. Slide 3 is the most text-dense slide, so its supplied full-size PNG is the appropriate review file. Google Play availability and cross-device physical-camera scanning were not tested; the final QR payload was independently verified digitally. Integration copy follows the owner's supplied product description; it does not imply independently tested compatibility with every accounting product.
