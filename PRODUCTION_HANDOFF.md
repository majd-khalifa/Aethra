# AETHRA × Primo — stopped production handoff

**Status: STOPPED BY USER — awaiting a completely revised creative brief.**

**CURRENT CHARACTER DESIGNS AND ILLUSTRATION STYLE: REJECTED.** They are retained only as a historical work checkpoint. They are not approved references, style guides, character models, or a starting point for further art without the user's revised direction. Do not render, redesign, generate scenes, resume Android testing, or submit orders from this checkpoint.

Saved on 2026-11-02 (Asia/Damascus). Branch: `codex/primo-syrian-reel`. No merge into main. The commit containing this handoff preserves unfinished work; it is not a production approval or final delivery.

## Exact locations

- Working repository: `C:\Users\MVJD\Desktop\Aethra\Aethra_Production`
- Editable Remotion project: `C:\Users\MVJD\Desktop\Aethra\Aethra_Production\AETHRA_PRIMO_REEL_20261102`
- Local Primo read-only reference: `D:\MAJD Files\Projects\Collage Projects\Production_Ready_Projects\Primo`
- Additional read-only reference checkout used earlier: `C:\Users\MVJD\.codex\tmp\primo-reference-20261102`, repository `majd-khalifa/Primo-market`, revision `c5595dcca76d37a16b18e3210934fe9af53cee3f`.

All paths below are relative to `AETHRA_PRIMO_REEL_20261102` unless stated otherwise.

## Work preserved

| File / directory | Purpose and approval status |
|---|---|
| `src/Root.tsx`, `src/index.ts` | Registers composition `AethraPrimo`: 1080 × 1920, 30 FPS, 600 frames. Timeline metadata preserved, no final MP4 rendered. |
| `src/Reel.tsx` | Editable family story, scene timing, captions, door sticker, app montage, time jump, arrival and end card. **Current visual execution rejected.** |
| `src/Art.tsx` | Original SVG character rigs, home backgrounds and props. **All current character designs and illustration style rejected.** Preserve for history only. |
| `src/captions.json` | Supplied Syrian mother's dialogue in timed caption JSON. Arabic words remain joined; direction is RTL. No Syrian voice acting recorded. |
| `src/PrimoUI.tsx` | Unfinished React reconstruction of source-supported Home, Product Details, Cart, Checkout and order-history success state. Fictional, explicitly labeled demo data; no authentication or API integration. **Not authenticated app footage, not pixel-verified, not approved production art.** |
| `src/material-icons.json`, `src/style.css` | Material glyph codes, original Cairo font weights, RTL styling and local font declarations. |
| `SOURCE_UI_MAP.md` | Maps Home, Categories, Products, Product Details, Cart, Checkout, confirmation behavior, navigation, theme and assets to the actual Flutter source. Identifies which screens are reconstructed and which standalone screens are not shown. |
| `public/brand/` | Unmodified original Primo logo and approved original AETHRA horizontal logo. These verified brand assets remain valid; rejection of the character style does not reject or alter the brand masters. |
| `public/primo/`, `public/fonts/` | Byte-identical original product/category imagery, Cairo fonts and existing Material icon font read from the reference. No Primo build was run in the local D: reference. |
| `public/audio/` | Original 20-second stereo `music.wav`, `sfx.wav`, `final-mix.wav` (48 kHz, 16-bit PCM). Existing draft soundtrack; not final creative approval. |
| `source/audio.py`, `source/sound-cues.json` | Editable procedural music/Foley synthesis and frame-numbered cue sheet. Audio producer refuses to overwrite existing stems. |
| `public/app/`, `qa/apk-*.png`, `qa/app-*.png`, `qa/*.xml` | Earlier pre-authentication onboarding/login/setup captures. Preserved as historical references. No credentials were entered by the agent, no authenticated screen was captured, and these images are not used by the current app montage. |
| `qa/provenance.json`, `qa/recreated-ui-assets.json` | Original asset hashes, earlier APK metadata, and source asset verification. APK itself is not included. |
| `qa/local-reference-before.json` | Read-only baseline hashes of local reference source/assets and selected metadata. No private file contents, API configuration values, credentials or tokens are stored in this inventory. |
| `qa/studio-preview.png`, `qa/studio-preview.json` | Earlier Studio preview and zero-page-error check. Historical only: they predate the last UI/eye-animation edits and show the **rejected** illustration style. They are not final visual QA. |
| `source/qa.py` | Prepared encoded-MP4 validation, all-frame decode, audio checks and review-sheet generation. It has not validated a final Reel because no final Reel exists. |
| `source/preview.cjs` | Historical Studio preview helper; uses local Edge for preview checks, not the Remotion rendering browser. |
| `source/resume-browser.cjs`, `source/install_official_browser.py` | Recovery helpers for the official Remotion browser download. Download is preserved in ignored `node_modules`; not installed or CRC-verified at stop. Do not run now. |
| `package.json`, `package-lock.json`, `remotion.config.ts`, `tsconfig.json` | Pinned dependencies and render configuration. Output overwrite is disabled. |

## Preserved timeline (zero-based frames)

| Frames | Time | Draft story content |
|---|---|---|
| 0–59 | 0–2 s | Mother urgently needs lunch ingredients. |
| 60–149 | 2–5 s | Older son gaming; younger son playing football; mother's continuing subtitles. |
| 150–209 | 5–7 s | Mother's exasperated second line. |
| 210–284 | 7–9.5 s | AETHRA eye roll, nonverbal sigh, room entry, door closes, AETHRA LAB sticker peels. |
| 285–404 | 9.5–13.5 s | Source-verified UI reconstruction montage with demo groceries and confirmation behavior. |
| 405–434 | 13.5–14.5 s | Comedic clock/time transition. |
| 435–509 | 14.5–17 s | Doorbell, groceries, mother's relief, peaceful family. |
| 510–599 | 17–20 s | Original Primo logo, requested Arabic ending and approved AETHRA production credit. |

The source is preserved exactly as an unfinished draft, apart from explicit rejection/stop documentation. No further visual approval should be inferred from this timeline.

## Dependencies and environment

- Windows / PowerShell; Node.js `24.13.0`, npm `11.6.2`.
- Remotion packages `4.0.540`, React / React DOM `19.3.1`, TypeScript `5.9.3`; lockfile included. Run `npm ci` only after production is explicitly resumed.
- Official `remotion-dev/skills` Agent Skills installed globally under `C:\Users\MVJD\.agents\skills`.
- FFmpeg `n7.1` and FFprobe supplied by `node_modules/@remotion/compositor-win32-x64-msvc`; they were not originally on the system PATH.
- Python used: `C:\Users\MVJD\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`, with NumPy and Pillow for the audio/QA helpers.
- Official render-browser archive: ignored `node_modules/.remotion/chrome-headless-shell/chromium-headless-shell-win-x64-158.0.8127.2.zip`, 137,435,497 bytes at stop. It has **not** been extracted, CRC-checked or marked installed. Previous automatic downloads stalled; resumable download helper is preserved. Do not treat file size as integrity verification.
- `node_modules`, browser cache and build output are excluded from Git. Approved source assets and editable work are included. No APK, keystore, token or credential is committed.

## Verification and limitations

Earlier TypeScript and ESLint checks passed during development. Checkpoint validation results are saved in `qa/checkpoint-verification.json`. Original logo and copied UI asset hashes were verified. The local Primo project was only read during this source-reference phase; its inventoried source/asset files are checked against the saved baseline.

**No final MP4, final visual inspection, playback QA, codec/frame-count validation or release approval exists for this commercial.** The historical preview is the rejected style. Remotion browser installation and final rendering remain incomplete. No order was submitted. No further login, emulator or runtime debugging is authorized.

Authentic Syrian voice acting was unavailable. The draft uses the supplied Syrian Arabic subtitles, original music/Foley and a synthesized nonverbal exhale for the daughter. The UI montage is reconstructed from source, uses fictional prices/address/order values, and is visibly labeled. It is not an authenticated capture or a verified live product offer.

## Resume only after the revised creative brief

1. Read this handoff and the new brief. Confirm the feature branch and preserve this checkpoint.
2. Treat current characters, backgrounds and illustration direction as rejected. Establish the new art direction from the revised instructions, not from `Art.tsx` or the old preview.
3. Reuse original brand masters, verified UI assets, source mapping, story timings or audio only to the extent consistent with the new brief. The Primo reference stays read-only; no authentication or runtime testing unless separately authorized later.
4. After explicit resumption, restore dependencies with `npm ci`; use `npm run dev` to open Studio. The previous `http://localhost:3000/AethraPrimo` server has been stopped.
5. Complete the official browser installation if needed. Render only when the new direction and instructions authorize it, to a **new unique filename**, keeping overwrite disabled.
6. Inspect the actual encoded output using `source/qa.py` and visual/audio review. Update reports with fresh evidence; old preview and checks do not approve revised work.

**Execution stops after the checkpoint commit/push report. Await the user's revised creative brief.**
