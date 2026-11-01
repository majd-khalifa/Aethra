# AETHRA — 20-second visual extension

## What changed before 15 seconds

**Nothing in the displayed picture.** Frames 0–449 of all three outputs have the same decoded-frame hashes as the approved 15-second source from PR #3. No scene, transition, frame rate, typography, wording, color layout, logo, aspect ratio or animation timing was rebuilt, cropped, stretched or slowed.

The existing picture was extracted with video stream copying and no audio. The concat step can repackage H.264 sequence headers; the preservation claim is backed by exact decoded-frame hashes for every original frame, rather than a claim that MP4 container bytes or every NAL header remain identical.

Source PR #3 commit: `169add7944f7b4c2bf484f44a0f2e37c6185943b`.

## What changed from 15 to 20 seconds

| Output frames | Time | Closing continuation |
|---|---|---|
| 450 | 15.000 s | Begin from the decoded pixels of original frame 449, retaining the complete closing invitation and CTA. |
| 450–513 | 15.000–17.100 s | Logo, wordmark, Arabic invitation, English support and CTA lift together by 24 pixels with a smooth eased path. |
| 487–527 | 16.233–17.567 s | A restrained travelling light follows the existing CTA border. It does not simulate a press or change text. |
| 513–582 | 17.100–19.400 s | The closing group settles six pixels to a final 18-pixel lift. |
| 582–599 | 19.400–19.967 s | Brief final reading hold, displayed through the 20-second endpoint. |

The new foreground is taken from the existing ending pixels. Its geometry is translated uniformly: no new font rendering, logo reconstruction, scaling, stretching or different brand treatment is introduced. Native near-white/lavender planes are restored only beneath the moving foreground. The original background remains stationary. The border light uses the existing near-white accent over the same purple CTA.

The extension is not a five-second freeze. Its source path moves over 4.4 seconds and includes one actual CTA-edge light; only the final 0.6 seconds form a stable reading hold. The encoded extension contains 145 distinct decoded frames. The original ending is not restructured before the 15-second boundary.

Only the 150 new closing frames are encoded with H.264 (x264 CRF 16, high profile, yuv420p, 30 fps). All three completed videos copy the same finished 600-frame picture stream. No new service, achievement, product, client, testimonial, promise or marketing claim appears.

## Identity and boundary verification

- Each final output has exactly 600 frames, 1080 × 1920, 30/1 fps, and a 20.000000-second timeline.
- Every original frame 0–449 matches the approved frame hash exactly.
- All 600 decoded frames match across A, B and C; their full H.264 elementary streams also have the same SHA-256.
- Shared picture SHA-256 (Annex B): `5cee718047970c65119cfd024abee9ae6dddadfb7b3d4668b99e9f831ed1657d`.
- The mean RGB difference across frame 449 → 450 is 0.952 on a 0–255 scale. The newly encoded tail involves an RGB/YUV conversion and compression; this is not a claim that its first new frame is pixel-identical to frame 449.
- Full-size closing frames and the contact sheet were inspected for logo proportions, unchanged Arabic shaping, retained wording, clipping, background seams and CTA alignment. No blocking visual defect was observed after the final composite correction.
- All outputs decode without errors and pass black-segment detection. Full real-time browser playback reaches all 600 frames.

This is **not complete visual identity to the 15-second original**: the outputs contain 150 additional frames. The preservation assertion applies specifically to the original 450-frame prefix.

Editable source: `source/build_picture.py`. Review: `analysis/closing_motion_contact_sheet.jpg`. Numerical evidence: `analysis/visual_extension.json`, `analysis/boundary_check.json`, `analysis/shared_picture_frame_hashes.json` and `analysis/verification.json`.
