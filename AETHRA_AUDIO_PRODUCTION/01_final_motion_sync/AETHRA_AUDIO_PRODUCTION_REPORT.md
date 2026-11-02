# AETHRA — Final audio production report

## Result and creative decisions

One new 15-second motion-synchronized soundtrack replaces the original audio. The existing visual stream is copied directly with FFmpeg `-c:v copy`. No visual frames, scene timing, typography, logos, color, aspect ratio or on-screen content were changed.

The final direction is restrained minimal electronic at 120 BPM: warm root-light extended chords, a muted mallet motif, a rounded low pulse and sparse brushed high-frequency detail. Voicings move through Dmaj9, Bm9, Gmaj9, A6/9 and Dadd9. Rhythm falls away before the final logo; a soft tonal resolution supports the closing hold. There is no large final impact.

Thirty selected sound cues follow the actual picture: the opening laptop materialization and cursor ring; the first confirmation; violet wipes; chart growth; website and phone entrances; app-node and success-disc reveals; data-row consolidation; automation toggle/rows and three separate checks; device expansion; and the final logo and CTA. The cue sheet distinguishes effect onset from a soft envelope's focus frame. No extra clicks, cursor presses, charts, screens or transitions were invented.

## Reference access

The supplied Instagram URL is outside this runtime's permitted outbound hosts. The reference could not be inspected or heard. No claim is made that its composition, recording or exact sonic sequence was analyzed. Production was based on the actual approved AETHRA export and the brief's general sound-to-motion principles.

## Source and visual lock

Source: `AETHRA_VIDEO_EXPORTS/AETHRA_A_Viral_Beat.mp4`, preserved GitHub commit `acef1a62997cbf46a36237e2a5c92de39385ff53`.

Source file SHA-256: `1a07d91b9dff15587a65729551188be9675997a575e198e440a43ee19e2dc798`.

All four current A/B/C/D source files were inspected. Each is 1080 × 1920, 30 fps, exactly 15 seconds, with 450 H.264 frames. All four share the same compressed visual stream and decoded frame hashes. There is no cleaner or higher-resolution alternative among those four; A was selected as an equivalent picture source.

Final/source H.264 Annex B SHA-256:

`4e92eca0632d5aaa36b345ec40f4cc9c843e86a01788a4a3174f7277d52524de`

Verification compares every video packet's SHA-256 payload hash, PTS, DTS, duration, size and flags: all 450 match. It also compares all 450 decoded-frame hashes: all match. The final stream starts at zero and retains the original 30/1 frame rate and 15-second duration. The assertion is identity to the above current source, not to any unavailable older render. All four original MP4 files remain byte-identical to their recorded source hashes.

All 450 source frames were decoded and inspected in five consecutive 90-frame review boards. Fine-frame views were used for the chart growth, data consolidation and automation sequence. The latter's completed states first appear at frames 287, 296 and 305. Review images are decoded thumbnails for analysis only and are never used to recreate the final picture.

## Mixing and synchronization

- 48 kHz stereo throughout, giving exactly 1,600 samples per video frame.
- Every selected cue's placement is an integer multiple of 1,600 samples; exact sample indices are retained in `analysis/cue_sample_audit.json`.
- Cue envelopes and levels vary by action: tactile click, soft pop, short filtered-air shift, connection tones, granular data glide and restrained final resolution.
- Approximately 31–191 ms of quiet, filtered early reflections supply depth without long tails masking subsequent cues.
- The music ducks by up to 2.8 dB around stronger SFX, using smooth automation. Music is filtered below 48 Hz; effects below 130 Hz. Upper bandwidth is controlled to avoid brittle high-frequency detail.
- Shared stereo-linked lookahead peak control applies the same gain to music and SFX, preserving stem recombination. The two mastering passes reduced the highest transients by approximately 1.51 dB and 0.15 dB.
- The delivered post-automation/post-master-gain stems sum to the final mix within three 24-bit least-significant steps, the tolerance introduced by independent triangular dither.
- Narrow stereo placement retains mono compatibility: measured L/R correlation is 0.9358; mono fold-down RMS changes by only −0.142 dB.
- AAC decoding/cross-correlation found **zero samples of uncompensated global delay**. Checks near frames 15, 287, 296, 305 and 398 correlate with the PCM mix at greater than 0.9999.

## Measured delivery

Target: −15 LUFS integrated, within ±0.3 LU, with a maximum permitted true peak of −1.5 dBTP. A more conservative −2.2 dBTP working ceiling leaves codec headroom.

| Asset | Integrated loudness | True peak | Format |
|---|---:|---:|---|
| Final PCM mix | −15.01 LUFS | −2.20 dBTP | 48 kHz / 24-bit stereo WAV |
| Encoded final MP4 audio | −15.03 LUFS | −2.20 dBTP | 48 kHz stereo AAC, requested 320 kb/s |
| Music stem | −16.81 LUFS | −3.40 dBTP | 48 kHz / 24-bit stereo WAV |
| SFX stem | −17.80 LUFS | −2.07 dBTP | 48 kHz / 24-bit stereo WAV |

The loudness values above are FFmpeg `loudnorm` **input** measurements of the actual delivered files. Its hypothetical normalized `output_*` fields are not delivery measurements. The short final mix measures 1.20 LU LRA; encoded AAC measures 1.10 LU LRA. Stem loudness is descriptive, not independently normalized, so unity-gain recombination remains valid.

Every WAV contains exactly 720,000 samples per channel / 15 seconds. There are no clipped PCM samples, non-finite values, hard opening/closing discontinuities or uncompensated audio offset. Both MP4 stream timelines and the container report exactly 15.000000 seconds. The final MP4 has one original H.264 video stream and one replacement AAC audio stream. No original soundtrack remains mapped into it.

## Playback and validation evidence

The complete final MP4 decodes with FFmpeg without errors. Headless Chromium played the actual output from start to finish at normal speed, unmuted, through a running Web Audio context. It decoded 450 frames, dropped zero frames, reported 1080 × 1920 and 15 seconds, and reached the end without media errors. The analyser observed nonzero audio during the playback test. This local HTTP test establishes runtime playback, not remote accessibility or physical Windows-phone compatibility.

Machine-readable evidence is retained in `analysis/verification.json`, `analysis/loudness.json`, `analysis/source_identity.json`, the frame review boards and the per-cue sample audit. Public GitHub accessibility is verified separately after upload by downloading and hashing the published files; no local-only test is treated as publication proof.

## Original audio provenance and commercial use

All musical notes, percussion, effects, reverberant reflections and automation were generated for this production from original oscillator/noise synthesis and deterministic code. No downloaded song, audio recording, sample, stock pack or third-party loop was used. The fixed random seed is `20261101`. NumPy 2.3.5, SciPy 1.17.0 and FFmpeg 7.1.5 were used.

The new audio was created for AETHRA's commercial social-media use. No third-party sound recording or sample license has been introduced, and no external sample-provider credit or royalty is required. Existing visual-asset rights are unchanged. No music, recording, exact composition or distinctive sound sequence was taken from the inaccessible Instagram reference.

Editable sources include the synthesis/production script, JSON sound-event arrangement, tonal MIDI and a portable two-track REAPER project. The MIDI contains tonal music notes, not the procedural percussion/SFX timbres. REAPER media paths are valid; its GUI was not installed for application testing.

## Remaining review limits

Physical Windows/iOS/Android devices, headphones, phone loudspeakers and Instagram's eventual transcoding were not available for direct listening tests. Objective measurements and unmuted Chromium playback are not human listening approval. The owner should audition the final MP4 for creative balance and acceptability before social publication. No automatic merge or social-media publication is part of this delivery.
