# AETHRA — Three complete 20-second reels

Three independent original music directions share **one identical 20-second picture** and **one common approved-SFX stem**. The original 450 picture frames and the approved first 15 seconds of SFX remain unchanged. Only the closing five seconds and two quiet complementary ending cues are new.

## Final review files

| Version | Video | Final mixed WAV | Music-only WAV |
|---|---|---|---|
| A — Tech Groove, 108 BPM | `AETHRA_20S_A_TECH_GROOVE.mp4` | `AETHRA_20S_A_FINAL_MIX.wav` | `AETHRA_20S_A_MUSIC_ONLY.wav` |
| B — Future Pulse, 96 BPM | `AETHRA_20S_B_FUTURE_PULSE.mp4` | `AETHRA_20S_B_FINAL_MIX.wav` | `AETHRA_20S_B_MUSIC_ONLY.wav` |
| C — Modern Electro, 126 BPM | `AETHRA_20S_C_MODERN_ELECTRO.mp4` | `AETHRA_20S_C_FINAL_MIX.wav` | `AETHRA_20S_C_MUSIC_ONLY.wav` |

`AETHRA_20S_APPROVED_SFX_COMMON.wav` is the shared effects stem. All seven final WAVs are 48 kHz / 24-bit stereo and exactly 20 seconds. Each video is H.264 / AAC stereo, 1080 × 1920, 30 fps, 600 frames, exactly 20.000 seconds.

Use the [complete GitHub repository ZIP](https://github.com/majd-khalifa/Aethra/archive/refs/heads/media/aethra-three-20s-reels.zip) for one downloadable package. It contains the existing repository files plus this entire production folder. After extraction, open `AETHRA_AUDIO_PRODUCTION/02_three_20_second_versions/review.html` to compare at the same playback volume. GitHub's source view does not execute HTML. For browser environments that restrict local files, serve this extracted folder through a local HTTP server.

The standalone `AETHRA_20S_COMPLETE_PACKAGE.zip` was preserved in the production runtime but is not committed: GitHub's blob API rejected its payload size with HTTP 422. All final MP4s, seven WAVs, editable inputs, scripts and reports are committed individually and included in GitHub's generated repository archive. Two reproducible picture intermediates and Python caches are excluded from version control; the original locked picture, endpoint pixels and build code remain included. No video or audio was regenerated to resolve the packaging limit.

## Reports

- `AETHRA_20S_VISUAL_EXTENSION_REPORT.md`: exact before/after-15-second changes and frame-identity proof.
- `AETHRA_20S_SOUND_CUE_SHEET.md`: all 30 approved cues and the two new closing cues.
- `AETHRA_20S_MUSIC_COMPARISON.md`: independent composition choices and the recommended version.
- `AETHRA_20S_VERIFICATION_REPORT.md`: format, frame hashes, SFX preservation, loudness, sync and playback evidence.
- `analysis/`: machine-readable verification, sample-preservation proof, frame hashes and closing-motion contact sheet.
- `SHA256SUMS.txt`: hashes of all other committed files in this folder. ZIP integrity and every production member's hash are verified separately after downloading GitHub's generated archive.

## Editable sources

Each `source/A_TECH_GROOVE.json`, `B_FUTURE_PULSE.json`, and `C_MODERN_ELECTRO.json` is an independent score with explicit notes, durations, instrument choices, levels, pan, harmony and tempo. Edit these JSON files to revise individual notes. The renderer reads them directly; no previous music is mixed or reused.

`source/render_audio.py` contains original oscillator/noise synthesis, music-only ducking and music-only headroom control. The approved SFX are copied as PCM samples without level changes or processing. Three tonal MIDI files support musical editing; they do not contain synthesized timbres, percussion or SFX. The JSON/Python scores are the authoritative full arrangements.

Open a corresponding `.rpp` file in REAPER for a portable two-track stem session with 32 cue markers. Music and SFX start at zero at unity gain. They recombine sample-exactly to that version's final mixed WAV. Media paths were checked; REAPER's GUI was not installed for application testing.

`source/build_picture.py` makes only the new five-second close and appends it to the copied 15-second picture. Its generated `source/SHARED_20S_PICTURE.mp4` is the one picture used for every final export. That file and `source/CLOSING_CONTINUATION_5S.mp4` are reproducible intermediates, not packaged source inputs; the audio renderer builds them automatically if needed. Verification can use final A as its canonical picture when intermediates are absent. `source/approved_reference/` contains the existing locked picture without its old soundtrack, the exact approved 15-second SFX file, endpoint pixels and original cue/frame references. These copied source dependencies make the package self-contained. Do not alter them. Their provenance and hashes are in `manifest.json`.

## Intentional revisions

Back up the delivered folder first. Install Python dependencies and FFmpeg/ffprobe. From this folder:

```sh
python -m pip install -r source/requirements.txt
# After editing a score JSON:
python source/render_audio.py --replace-generated
python source/verify_versions.py
```

To revise only the new closing motion, edit `source/build_picture.py`, run it with `--replace-generated`, then re-render the audio/video exports and verify again. The original 450 frames are copied, not rebuilt. `compose_scores.py` documents how the three initial independent scores were authored; it refuses to overwrite existing editable JSON. Do not run it to update an edited score.

The generated-output replacement flags are limited to this new production. No prior 15-second export is overwritten. Browser validation requires Playwright and Chromium; the script currently selects `/usr/bin/chromium`. The test uses a temporary loopback HTTP server, not a public preview or download service. Adapt the Chromium executable path when validating on another platform.

After any revision, update the affected reports and rebuild checksums/ZIP. Old measurements are not validation of edited media.

## Rights and practical review limits

All three new compositions, synthesized instruments, percussion and two new ending effects were created for AETHRA without third-party recordings, loops, samples or reference music. The approved SFX are reused as authorized in the brief. No additional third-party sound license is introduced; existing visual rights remain unchanged.

Technical validation includes real-time unmuted Chromium playback, not physical phone/headphone listening or Instagram transcoding. The owner should audition the three alternatives before choosing one for social publication. This package does not imply music approval, automatic PR merge or social posting.
