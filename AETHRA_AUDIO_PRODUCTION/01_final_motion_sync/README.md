# AETHRA — Final motion-synchronized audio production

This production replaces only the audio of the existing 15-second AETHRA reel. The original H.264 visual stream is copied, not rendered or encoded again. All 450 video frames, packet payloads, packet timestamps and durations were verified against the source.

## Review and deliverables

- `AETHRA_FINAL_MOTION_SYNC_REEL.mp4`: 1080 × 1920, 30 fps, exactly 15 seconds; original H.264 picture with new 48 kHz stereo AAC audio.
- `AETHRA_FINAL_MOTION_SYNC_AUDIO.wav`: final stereo mix, 48 kHz / 24-bit PCM, exactly 720,000 samples per channel.
- `AETHRA_MUSIC_ONLY.wav`: music stem with the delivered automation and shared master gain.
- `AETHRA_SFX_ONLY.wav`: effects stem with its delivered reflections and shared master gain.
- `AETHRA_SOUND_CUE_SHEET.md`: 30 selected cues with zero-based frame numbers, seconds, anchors and rationale.
- `AETHRA_AUDIO_PRODUCTION_REPORT.md`: source identity, original-audio provenance, measured loudness, validation and practical review limits.
- `review.html`: video and stem player. Extract the ZIP and open locally, or use a local HTTP server. GitHub's HTML source view does not run the player.
- `source/`: editable JSON cue arrangement, synthesizer, verification script, tonal MIDI and a two-track REAPER project.
- `analysis/`: source/frame hashes, all-frame review boards, motion measurements, cue-sample audit, loudness and playback results.
- `SHA256SUMS.txt`: integrity checksums for all other files in this folder.

The sibling `../AETHRA_FINAL_MOTION_SYNC_PACKAGE.zip` contains this complete folder. It does not overwrite or include an altered copy of any previous export.

## Approved visual source

All four existing A/B/C/D exports were inspected and have identical H.264 streams and decoded frames. Version A was selected because the picture is identical across them:

[AETHRA_A_Viral_Beat.mp4 at the preserved source commit](https://github.com/majd-khalifa/Aethra/raw/acef1a62997cbf46a36237e2a5c92de39385ff53/AETHRA_VIDEO_EXPORTS/AETHRA_A_Viral_Beat.mp4)

Source file SHA-256: `1a07d91b9dff15587a65729551188be9675997a575e198e440a43ee19e2dc798`.

Identity assertions refer to this existing export. They do not assert identity to any earlier, unavailable historical render.

## Edit the arrangement

For a quick stem-level mix, open `source/AETHRA_AUDIO_ARRANGEMENT.rpp` in REAPER. Both tracks start at zero, use unity gain, and reference the two WAV stems in this folder. They recombine to the delivered PCM mix within three 24-bit quantization steps. Markers identify every cue. Media paths were checked; REAPER's GUI was not available for an application-level test.

`source/AETHRA_MUSIC_NOTES.mid` contains the tonal pad, mallet and bass notes at 120 BPM. The procedural percussion and effects are defined in Python, not in that MIDI file. MIDI is an editing aid; it does not contain the synthesized timbres.

For individual effects, edit `source/arrangement.json`: each cue has a `start_frame`, `end_frame`, `anchor_frame`, sound type, level, pitch and pan. At 30 fps and 48 kHz, every frame equals exactly 1,600 audio samples. Keep the source picture locked. The musical notes and synthesis envelopes are in `source/produce_audio.py`.

Back up the delivered files before making an intentional audio revision. From this folder:

```sh
python -m pip install -r source/requirements.txt
python source/produce_audio.py --source /path/to/AETHRA_A_Viral_Beat.mp4 --replace-generated
python source/verify_production.py --source /path/to/AETHRA_A_Viral_Beat.mp4
```

FFmpeg/ffprobe must be installed. Browser verification uses Playwright and Chromium at `/usr/bin/chromium`; adapt that executable path on another operating system. The managed runtime blocks `file://` browser navigation, so the verifier starts a temporary loopback HTTP server for its internal playback test. This is not a public download service.

Without `--replace-generated`, the producer refuses to replace existing outputs. It never modifies the source video. After revising cues or music, update the cue sheet/report, recheck the complete mix, then rebuild checksums and the review ZIP. Do not treat stale analysis files as validation of a revised production.

## Audio rights and review

All new music and effects are original procedural synthesis created for AETHRA. No external song, recording, sample pack, stock loop, reference audio or third-party audio asset was used. No sample-provider license or attribution is required for this generated audio. Existing visual-asset rights remain unchanged.

The Instagram reference could not be accessed under this runtime's network policy; its sound was not analyzed or copied. Physical phone-speaker/headphone review and the platform's eventual re-encode remain listening checks for the owner. The completed delivery includes objective signal checks and unmuted Chromium playback, not a claim of human listening approval.
