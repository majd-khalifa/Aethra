# AETHRA × Primo — production status

> **STOPPED BY USER. Current character designs and illustration style are REJECTED.**
> This file is historical progress context, not approval or current instructions.
> The authoritative stop/resume handoff is `../PRODUCTION_HANDOFF.md`.
> No rendering, redesign, new scenes, authentication or runtime debugging may continue until a revised brief arrives.

Production date: 2026-11-02 (Asia/Damascus).

Working checkout: `C:\Users\MVJD\Desktop\Aethra\Aethra_Production`.
Branch: `codex/primo-syrian-reel`. No main merge or remote push.

## Ready for review

- Editable Remotion composition: `src/Reel.tsx`; reusable original vector character rigs and set art: `src/Art.tsx`.
- Exact 600-frame, 1080×1920, 30 FPS timeline, including eye roll, nonverbal sigh, room entrance, door close, peeling AETHRA LAB sticker, doorbell, groceries, family resolution, and three-second logo end card.
- Mother's supplied Syrian Arabic dialogue in joined RTL captions, with bundled Cairo Arabic font. No additional spoken dialect is introduced.
- New original 20-second music, Foley, and nonverbal synthetic breath; editable synthesis: `source/audio.py`; individual cue frames: `source/sound-cues.json`.
- Original Primo logo hash matches both read-only reference repository and supplied APK. Approved AETHRA logo matches the existing approved master byte for byte. See `qa/provenance.json`.
- TypeScript check passes. Studio preview loads without JavaScript page errors; see `qa/studio-preview.json`.

## Pending input / remaining production

The supplied APK (`com.primo.app`, version 1.0.0, build 3) is installed on Pixel_7 / emulator-5554. Onboarding and mandatory login are captured. Home, categories, products, search, cart, checkout, and confirmation have not yet been captured.

The user will enter credentials directly in the visible emulator. No credentials are requested in chat or stored in project files. Screenshot/UI inspection is paused until the user confirms login. No order has been prepared or submitted.

The current app scene is an interim onboarding reference, **not an approved browse/cart/confirmation sequence**. Replace it with authenticated footage before final rendering. An actual order requires the user's separate approval of exact items, item total, delivery fee, total price, address and payment method before submission. Published frames must exclude account, address and order-identifying data; preserve authentic UI layout and branding when masking personal fields.

The official Remotion browser download encountered repeated 20-second idle timeouts. A resumable download of the identical official Remotion-patched browser is in progress. Final MP4 rendering and encoded-output QA remain pending.

## Voice limitation

Authentic Syrian voice acting is unavailable in this environment. This is the authorized subtitle-led fallback with original music and Foley. AETHRA has no speech; her only vocal-like sound is a procedurally synthesized nonverbal exhale. No claim of human voice acting or dialect validation by a Syrian performer is made.

## Reproduction

Run `npm ci`, then `npm run dev` for Studio. Audio stems already exist; `source/audio.py` deliberately refuses to replace them. Use a new output name for each render. The final target is H.264/AAC, yuv420p, 48 kHz stereo, exactly 20 seconds / 600 frames. `source/qa.py` decodes and inspects the actual MP4 and generates an encoded-output contact sheet and technical JSON. It deliberately creates a new QA directory and refuses to overwrite an existing report set.

No final MP4 or final QA pass is claimed at this checkpoint. Do not commit as finished production until authentic app flow and output inspection are complete.
