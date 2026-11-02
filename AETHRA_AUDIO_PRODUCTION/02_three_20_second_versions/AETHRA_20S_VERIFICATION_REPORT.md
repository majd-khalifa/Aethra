# AETHRA — Three 20-second versions: verification report

## Format and picture preservation

All three MP4s are exactly 20.000000 seconds, 1080 × 1920, 30/1 FPS, 600 H.264 frames, with one 48 kHz stereo AAC audio stream. Video and audio timelines both start at zero. All three have identical H.264 elementary streams and decoded frame hashes.

Shared H.264 Annex B SHA-256: `5cee718047970c65119cfd024abee9ae6dddadfb7b3d4668b99e9f831ed1657d`.

Every original frame 0–449 matches the approved PR #3 picture exactly. Only frames 450–599 are additional. Complete 20-second identity to the 15-second original is not claimed. The visual-extension report documents the exact continuation and the RGB/YUV encoding boundary. Every output passes full FFmpeg decoding and black-segment detection.

## Strict approved-SFX preservation

The common 20-second SFX WAV begins with the exact 4,320,000 PCM bytes from the approved 15-second SFX WAV: 720,000 stereo frames, 48 kHz, 24-bit. Source and extended-prefix SHA-256 are both `6081265208a684af16930c1ea1948a808eb9981437b8bc8e4584ec0c89a9f9e4`.

This is byte-level preservation of all 30 effects: timing, identity, envelope, pitch, relative balance and character. The original waveform is not resynthesized, moved, normalized, limited, ducked or faded. Only two quieter new closing cues are added after 15 seconds, at frames 487 and 582. The identical common SFX stem is mixed at unity gain into A, B and C. All processing for masking and peak headroom affects music only.

Every final mixed WAV equals its delivered music WAV plus that common SFX WAV **sample-exactly**, without a separate output limiter or master gain changing the SFX. The reference-asset manifest was checked against the copied source dependencies. Original source files outside this new production remain untouched.

## Audio measurements

Target integrated loudness: −15.5 LUFS within ±0.2 LU. True-peak ceiling: −1.5 dBTP. The conservative music-only headroom system targets approximately −1.85 dBTP before AAC encoding. Values below are `loudnorm` input measurements of delivered files, not its proposed normalized output values.

| Version | PCM mix LUFS | AAC LUFS | AAC true peak | PCM LRA | Mono fold-down change | AAC delay |
|---|---:|---:|---:|---:|---:|---:|
| A | -15.47 | -15.48 | -1.85 dBTP | 3.90 LU | -0.037 dB | 0 samples |
| B | -15.54 | -15.53 | -1.85 dBTP | 2.70 LU | -0.074 dB | 0 samples |
| C | -15.51 | -15.51 | -1.77 dBTP | 2.00 LU | -0.018 dB | 0 samples |

The AAC loudness spread across all three versions is 0.05 LU. Every final WAV has exactly 960,000 samples per channel, 48 kHz, 24-bit stereo. No clipped PCM samples or non-finite signals were found. No silent 10 ms windows were found when excluding the first/last 50 ms intended fades. Mono fold-down stays comfortably within the −3 dB test bound.

AAC decoding/cross-correlation finds zero uncompensated delay. Correlation with the PCM mix was checked at frames 15, 287, 296, 305, 398, 487 and 582 for every version; all pass a 0.98 correlation bound. Original cue placement is unchanged because the common stem is a sample-exact prefix copy, not a new placement of reconstructed cues.

Smooth music-only ducking provides up to 5.5 dB of normal SFX space, with additional linked music-only peak headroom as needed. The common effects are never adjusted. The peak controller can temporarily reduce music more at strong SFX transients; exact diagnostic gain reductions are retained in `analysis/loudness.json`.

## Actual playback

Each actual final export was played at normal speed from beginning to end in a fresh Chromium player through a local HTTP server, unmuted, with a running Web Audio analyser.

| Version | End reached | Decoded frames | Dropped frames | Duration | Audio observed |
|---|---|---:|---:|---:|---|
| A | True | 600 | 0 | 20.000 s | Yes, analyser maximum RMS 0.3419 |
| B | True | 600 | 0 | 20.000 s | Yes, analyser maximum RMS 0.3590 |
| C | True | 600 | 0 | 20.000 s | Yes, analyser maximum RMS 0.3111 |

The local playback check proves runtime playback. GitHub delivery is verified separately by downloading the published MP4s and ZIP, checking their HTTP status, byte sizes, SHA-256 hashes and ZIP member contents. No local preview or workspace path is presented as proof of public delivery.

## Independent composition and rights

Three independently authored scores use different note sequences, harmonic schedules, tempi (108/96/126 BPM), rhythmic forms, synthesis timbres and codas. Pairwise music waveform correlations are AB 0.0685, AC 0.0127, BC 0.0122. These show distinct signals and supplement the editable scores; signal correlation does not prove creative quality or copyright originality.

All new compositions, percussion and two additional effects use original deterministic oscillator/noise synthesis. No third-party sound recording, song, stock loop, sample pack or copied composition is used. The previously approved SFX are reused under the user’s explicit instruction. Existing visual rights are unchanged. No additional third-party audio license or sample-provider attribution is introduced.

## Preservation and limitations

The GitHub blob API accepted individual media files but rejected the standalone 52.6 MB and compact 49.9 MB ZIP payloads with HTTP 422 (`input was too large to process`). This was a size limit, not an authentication denial. Both local archives and all completed media remain preserved. The standalone ZIP is not committed. Delivery uses GitHub's generated repository ZIP, which contains this complete production folder plus the existing repository files. Its CRC and every new production member are checked against the committed/local SHA-256 manifest after download. No Git transport authentication retry, media regeneration or downgrade is used to resolve the archive limit.

PR #1 video assets, PR #2 carousel assets, PR #3 audio-production assets, original brand files and existing main are preserved. The new delivery is confined to `AETHRA_AUDIO_PRODUCTION/02_three_20_second_versions/`. A new review branch and draft PR are used; nothing is merged or posted to social media.

Physical Windows/iOS/Android hardware, phone loudspeakers, headphones and Instagram transcoding were not tested. Technical measurements and unmuted Chromium playback are not human listening approval. REAPER media paths were checked; its GUI was not installed. The owner should audition all three actual outputs before selecting the final music.

Evidence: `analysis/verification.json`, `analysis/loudness.json`, `analysis/sfx_preservation.json`, `analysis/shared_picture_frame_hashes.json`, `analysis/visual_extension.json`, `analysis/boundary_check.json` and the closing contact sheet.
