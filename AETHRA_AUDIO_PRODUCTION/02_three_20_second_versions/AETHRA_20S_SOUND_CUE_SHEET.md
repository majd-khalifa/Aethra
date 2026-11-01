# AETHRA — 20-second sound cue sheet

Frame numbers are zero based at 30 FPS. Every frame is exactly 1,600 samples at 48 kHz. All three versions use the same SFX file at unity gain, untrimmed and unprocessed.

## Original 0–15 seconds: all 30 approved cues preserved

The first 720,000 stereo samples of `AETHRA_20S_APPROVED_SFX_COMMON.wav` are bit-identical to the approved `AETHRA_SFX_ONLY.wav` from PR #3. This preserves the complete waveform: cue identities, onsets, pitch, envelopes, relative levels, early reflections and original master automation. No cue is regenerated, retimed, pitch-shifted, normalized or ducked. All ducking and peak protection affect music only.

| Cue | Original start frame | Seconds | Original anchor | Dry end frame | Approved visual event |
|---|---:|---:|---:|---:|---|
| 01 | 1 | 0.033333 | 1 | 7 | Opening Arabic question fades in above the blueprint |
| 02 | 6 | 0.200000 | 10 | 13 | Laptop materializes over the blueprint |
| 03 | 15 | 0.500000 | 15 | 19 | Cursor click ring appears on the laptop UI |
| 04 | 24 | 0.800000 | 24 | 33 | Headline switches and purple check badge appears below the laptop |
| T1 | 51 | 1.700000 | 53 | 56 | Diagonal violet scene wipe |
| 05 | 54 | 1.800000 | 54 | 65 | First stacked AETHRA logo and solutions line fade up |
| T2 | 87 | 2.900000 | 89 | 92 | Diagonal violet scene wipe |
| 06 | 91 | 3.033333 | 91 | 100 | Dashboard cards appear and six chart bars rise left to right |
| 07 | 100 | 3.333333 | 100 | 108 | Small YOUR WORK / YOUR WAY badge appears below the dashboard |
| T3 | 132 | 4.400000 | 134 | 137 | Diagonal violet scene wipe |
| 08 | 136 | 4.533333 | 136 | 143 | Website laptop interface and websites/apps title reveal |
| 09 | 145 | 4.833333 | 150 | 156 | Phone slides into place beside the laptop |
| 10 | 159 | 5.300000 | 159 | 166 | IN SYNC confirmation pill appears below the two devices |
| T4 | 177 | 5.900000 | 179 | 182 | Diagonal violet scene wipe |
| 11 | 181 | 6.033333 | 181 | 188 | Three app nodes fade onto the triangular connection paths |
| 12 | 188 | 6.266667 | 188 | 197 | Purple success disc appears between the linked nodes |
| T5 | 222 | 7.400000 | 224 | 227 | Diagonal violet scene wipe |
| 13 | 226 | 7.533333 | 226 | 246 | Loose data strips converge into the search/list panel |
| 14 | 246 | 8.200000 | 246 | 253 | ALL IN ONE PLACE pill fades in under the organized list |
| T6 | 267 | 8.900000 | 269 | 272 | Diagonal violet scene wipe |
| 15 | 271 | 9.033333 | 277 | 282 | Automation toggle and three task rows fade/slide into place |
| 16 | 287 | 9.566667 | 287 | 292 | Request received row gains its purple check |
| 17 | 296 | 9.866667 | 296 | 301 | Message sent row gains its purple check |
| 18 | 305 | 10.166667 | 305 | 310 | Task completed row gains its purple check |
| T7 | 321 | 10.700000 | 323 | 326 | Diagonal violet scene wipe |
| 19 | 325 | 10.833333 | 340 | 360 | Laptop and phone expand together from a small composite to full size |
| 20 | 325 | 10.833333 | 325 | 337 | Mail card and round success badge emerge with the composite devices |
| T8 | 387 | 12.900000 | 389 | 392 | Diagonal violet scene wipe |
| 21 | 391 | 13.033333 | 391 | 449 | Final AETHRA logo and Arabic invitation fade up |
| 22 | 398 | 13.266667 | 398 | 407 | Final purple contact CTA fades in below the invitation |

The untouched prior cue sheet is retained as `source/approved_reference/APPROVED_15S_SOUND_CUE_SHEET.md` for reference. Its old music description is historical; that music is not used in these versions.

## New closing motion: two quiet complementary cues

| Frame | Seconds | Length | New motion | Sound |
|---:|---:|---:|---|---|
| 487 | 16.233333 | 0.430 s | First visible travelling light on the existing CTA edge | Low-level airy digital glint with a short D6 shimmer |
| 582 | 19.400000 | 0.430 s | The original closing group completes its gentle settle | Soft D5/A5 tonal resolution, substantially quieter than the approved main logo accent |

These sounds reinforce actual new motion. There is no invented click, button press, screen state, service or claim. No additional effects are added to the final reading hold.

## Musical alignment

A uses 108 BPM swung syncopation, B a 96 BPM eighth-note pulse and C 126 BPM electro syncopation. The original SFX stay off-grid wherever required by the picture. Each score reduces percussion around 12.9–13.45 seconds, and the music bus makes smooth space around actual SFX transients. No old cue is moved to land on a musical beat.
