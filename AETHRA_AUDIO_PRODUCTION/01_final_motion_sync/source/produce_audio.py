"""Original procedural music and frame-aligned sound design. No sampled recordings.

Run: python source/produce_audio.py --source /path/to/AETHRA_A_Viral_Beat.mp4
Requires Python 3, NumPy, SciPy, FFmpeg. Original visual stream is copied only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import struct
import subprocess
import tempfile
import wave

import numpy as np
from scipy import ndimage, signal
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
ARR = json.loads((ROOT / 'source/arrangement.json').read_text())
SR = ARR['sample_rate']
N = int(ARR['duration_seconds'] * SR)
RNG = np.random.default_rng(ARR['seed'])
MUSIC_NOTES = []

def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)

def db(value):
    return 10 ** (value / 20)

def tgrid(duration):
    return np.arange(round(duration * SR)) / SR

def fade_env(length, attack=.005, release=.02):
    env = np.ones(length)
    a = min(length, max(1, round(attack * SR)))
    r = min(length, max(1, round(release * SR)))
    env[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    env[-r:] *= np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return env

def stereo(mono, pan=0):
    p = np.asarray(pan)
    angle = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.column_stack((mono * np.cos(angle), mono * np.sin(angle)))

def place(track, audio, seconds):
    start = round(seconds * SR)
    end = min(N, start + len(audio))
    if start < N and end > start:
        track[start:end] += audio[:end-start]

def filt(x, low=None, high=None, order=2):
    if low is not None and high is not None:
        sos = signal.butter(order, [low, high], btype='bandpass', fs=SR, output='sos')
    elif low is not None:
        sos = signal.butter(order, low, btype='highpass', fs=SR, output='sos')
    else:
        sos = signal.butter(order, high, btype='lowpass', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0)

def room(track, wet=.1):
    """Quiet crossfed, low-passed early reflections; no convolution assets."""
    result = track.copy()
    colored = filt(track, low=250, high=4500)
    for delay, gain, flip in [(.031,.48,True),(.047,.38,False),(.083,.28,True),(.127,.18,False),(.191,.1,True)]:
        d = round(delay * SR)
        reflected = colored[:-d, ::-1] if flip else colored[:-d]
        result[d:] += wet * gain * reflected
    return result

def music():
    pad = np.zeros((N, 2)); notes = np.zeros((N, 2)); bass = np.zeros((N, 2)); rhythm = np.zeros((N, 2))
    # Spacious, root-light extensions; the bass supplies the harmony in mono.
    chords = [(0,[62,69,73,76],38), (3,[59,66,69,73],35),
              (6,[55,62,66,69],43), (9,[57,64,66,71],45),
              (12,[62,66,69,76],38)]
    for start, chord, root in chords:
        duration = min(3.6, 15-start)
        t = tgrid(duration)
        envelope = fade_env(len(t), .24, .65)
        for i, note in enumerate(chord):
            f = hz(note)
            voice = (.78*np.sin(2*np.pi*f*t + .16*np.sin(2*np.pi*.17*t))
                     + .15*np.sin(2*np.pi*f*2*t) + .045*np.sin(2*np.pi*f*3*t))
            voice *= .012 * envelope * (.94+.06*np.sin(2*np.pi*.35*t+i))
            place(pad, stereo(voice, [-.42,.25,-.16,.4][i]), start)
            MUSIC_NOTES.append((start,duration,note,42,0))
        # Rounded sine bass with a little second harmonic for phone audibility.
        for offset, level in [(0,.045),(1.5,.031)]:
            if start+offset > 12.5:
                continue
            tb = tgrid(.63); f = hz(root)
            env = fade_env(len(tb), .014, .11) * np.exp(-tb*3.1)
            mono = (np.sin(2*np.pi*f*tb) + .22*np.sin(2*np.pi*f*2*tb)) * env * level
            place(bass, stereo(mono), start+offset+.02)
            MUSIC_NOTES.append((start+offset+.02,.63,root,64,2))
    motif = [(.25,74,.026,-.2),(.75,81,.023,.25),(1.25,78,.022,-.12),
             (2.0,76,.027,.12),(2.75,81,.018,.2),
             (3.75,78,.023,-.2),(4.25,73,.02,.25),(5.25,76,.022,-.12),
             (6.75,74,.023,-.2),(7.25,78,.019,.25),(8.5,81,.023,.1),
             (9.75,76,.023,-.18),(10.25,78,.02,.2),(11.25,83,.019,-.12),
             (12.0,81,.021,.18),(12.5,78,.018,-.18)]
    for start, note, level, pan in motif:
        t = tgrid(.62); f = hz(note)
        # A soft mallet: decaying low-index FM, slight inharmonic body, no hard square waves.
        env = np.exp(-t*7.2) * fade_env(len(t), .008, .14)
        x = (np.sin(2*np.pi*f*t + .7*np.exp(-t*18)*np.sin(2*np.pi*f*2*t))
             + .09*np.sin(2*np.pi*f*3.01*t)*np.exp(-t*14)) * env * level
        place(notes, stereo(x,pan), start)
        MUSIC_NOTES.append((start,.62,note,60,1))
    # Half-time pulse and sparse soft brushed hats. Stop rhythm ahead of the final logo.
    for start in np.arange(.5,12.6,1.0):
        t = tgrid(.17)
        f = 64+52*np.exp(-t*40)
        phase = 2*np.pi*np.cumsum(f)/SR
        x = (np.sin(phase)+.14*np.sin(phase*2))*np.exp(-t*26)*fade_env(len(t),.004,.04)*.044
        place(rhythm,stereo(x),float(start))
    for i,start in enumerate(np.arange(1.25,12.4,.5)):
        if i % 4 == 2:
            continue
        t=tgrid(.07); noise=filt(RNG.normal(size=len(t)),low=2800,high=6800)
        x=noise*np.exp(-t*55)*fade_env(len(t),.003,.02)*.008
        place(rhythm,stereo(x,(-1)**i*.18),float(start))
    # A quiet sustained tonic at the close; no final kick or trailer hit.
    t=tgrid(1.95); env=fade_env(len(t),.12,.55)*np.exp(-t*1.25)
    for note,amp,pan in [(62,.019,0),(69,.012,-.25),(76,.009,.25)]:
        place(notes,stereo(np.sin(2*np.pi*hz(note)*t)*env*amp,pan),13.033333333)
        MUSIC_NOTES.append((13.033333333,1.95,note,48,1))
    result = room(pad,.16)+room(notes,.2)+bass+rhythm
    result = filt(result,low=48,high=9500)
    return result

def tone(t,note,decay=16,brightness=.12):
    f=hz(note)
    x=np.sin(2*np.pi*f*t + .32*np.exp(-t*35)*np.sin(2*np.pi*f*2*t))
    x+=brightness*np.sin(2*np.pi*f*2.006*t)*np.exp(-t*18)
    return x*np.exp(-t*decay)*fade_env(len(t),.002,.014)

def effect(e):
    duration=(e['end_frame']-e['start_frame'])/ARR['fps']
    t=tgrid(duration); x=np.zeros(len(t)); kind=e['sound']; note=e['midi']; pan=e['pan']
    if kind in ['tap','tick','pop','cta']:
        decay={'tap':55,'tick':43,'pop':23,'cta':22}[kind]
        base=tone(t,note,decay,.08)
        noise=filt(RNG.normal(size=len(t)),low=650,high=4200)
        x=.68*base + .19*noise*np.exp(-t*125)*fade_env(len(t),.001,.008)
        if kind=='pop':
            phase=2*np.pi*np.cumsum(hz(note)*(.65+.35*np.exp(-t*35)))/SR
            x=.65*np.sin(phase)*np.exp(-t*25)*fade_env(len(t),.003,.02)
    elif kind=='confirm':
        x=.62*tone(t,note,20,.08)
        delay=round(.042*SR)
        if delay<len(t):
            x[delay:]+=.36*tone(t[:-delay],note+5,17,.06)
    elif kind in ['reveal','slide','wipe','expansion']:
        n=filt(RNG.normal(size=len(t)),low=550,high=4200 if kind=='wipe' else 2900)
        peak=(e['anchor_frame']-e['start_frame'])/30
        if peak<=0:
            peak=duration*.36
        env=np.exp(-.5*((t-peak)/max(.025,duration*.23))**2)*fade_env(len(t),.009,.026)
        shimmer=np.sin(2*np.pi*np.cumsum(np.linspace(hz(note)*.65,hz(note),len(t)))/SR)
        x=(.58*n+.15*shimmer)*env
        pan=np.linspace(.3,-.3,len(t)) if kind=='wipe' else np.linspace(-.2,pan,len(t))
        if kind=='expansion':
            x*=.8
    elif kind=='glass':
        x=(tone(t,note,7,.15)+.5*tone(t,note+7,9,.06))*.52
    elif kind=='data_rise':
        n=filt(RNG.normal(size=len(t)),low=900,high=3500)
        glide=np.sin(2*np.pi*np.cumsum(np.linspace(hz(note),hz(note+12),len(t)))/SR)
        x=.18*glide*np.sin(np.linspace(0,np.pi,len(t)))**2 + .1*n*fade_env(len(t),.03,.05)
        for offset,step in [(0,0),(1/30,2),(2/30,4)]:
            d=round(offset*SR)
            x[d:]+=.25*tone(t[:len(t)-d],note+step,22,.08)
    elif kind=='nodes':
        result=np.zeros((len(t),2))
        for offset,step,p in [(0,0,-.3),(.05,7,.3),(.1,4,0)]:
            d=round(offset*SR)
            if d<len(t):
                result[d:]+=stereo(tone(t[:len(t)-d],note+step,28,.06)*.7,p)
        return result*e['level']
    elif kind=='organize':
        n=filt(RNG.normal(size=len(t)),low=700,high=2500)
        x=.22*n*fade_env(len(t),.07,.12)
        for offset,step in [(0,0),(.16,2),(.31,4),(.49,7)]:
            d=round(offset*SR)
            if d<len(t):
                x[d:]+=.38*tone(t[:len(t)-d],note+step,30,.06)
    elif kind=='toggle':
        anchor=(e['anchor_frame']-e['start_frame'])/30
        env=np.exp(-.5*((t-anchor)/.045)**2)*fade_env(len(t),.01,.025)
        n=filt(RNG.normal(size=len(t)),low=380,high=2200)
        x=.35*n*env
        d=round(anchor*SR)
        x[d:]+=.65*tone(t[:len(t)-d],note,34,.08)
    elif kind=='resolve':
        for step,amp in [(0,.63),(7,.33),(14,.18)]:
            x+=amp*tone(t,note+step,3.2,.05)
        x*=fade_env(len(t),.012,.3)
    else:
        raise ValueError(kind)
    return stereo(x*e['level'],pan)

def pcm24(path,data):
    assert np.max(np.abs(data))<1
    # Deterministic triangular dither; half a 24-bit quantization step per component.
    dither=(RNG.random(data.shape)-RNG.random(data.shape))/8388607
    values=np.round(np.clip(data+dither,-1,.9999999)*8388607).astype('<i4')
    packed=values.view(np.uint8).reshape(-1,4)[:,:3].tobytes()
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(3);w.setframerate(SR);w.writeframes(packed)

def measure(path):
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af',
        'loudnorm=I=-15:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    return json.loads(re.findall(r'\{\s*"input_i".*?\}',r.stderr,re.S)[-1])

def limiter(mus,sfx,ceiling):
    total=mus+sfx
    overs=signal.resample_poly(total,4,1,axis=0)
    peaks=np.max(np.abs(overs).reshape(N,4,2),axis=(1,2))
    if np.max(peaks)<=ceiling:
        return mus,sfx,0.0
    nearby=ndimage.maximum_filter1d(peaks,size=481,mode='nearest')
    required=np.minimum(1,ceiling/np.maximum(nearby,1e-9))
    gains=np.empty(N);last=1.0;release=1-np.exp(-1/(SR*.075))
    for i,value in enumerate(required):
        last=min(value,last+(1-last)*release);gains[i]=last
    # Smooth the lookahead edge while retaining ample margin at the actual peak.
    gains=ndimage.gaussian_filter1d(gains,24)
    return mus*gains[:,None],sfx*gains[:,None],float(-20*np.log10(np.min(gains)))

def write_midi(path):
    def variable(n):
        parts=[n&127];n>>=7
        while n:parts.insert(0,(n&127)|128);n>>=7
        return bytes(parts)
    events=[(0,b'\xff\x51\x03'+(500000).to_bytes(3,'big'))]
    for start,duration,note,velocity,channel in MUSIC_NOTES:
        tick=round(start*960);end=round((start+duration)*960)
        events.extend([(tick,bytes([0x90+channel,note,velocity])),(end,bytes([0x80+channel,note,0]))])
    track=b'';last=0
    for tick,data in sorted(events,key=lambda x:x[0]):
        track+=variable(tick-last)+data;last=tick
    track+=b'\x00\xff\x2f\x00'
    path.write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(track))+track)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--replace-generated',action='store_true',help='Explicitly replace only this new production, never the source video')
    args=parser.parse_args();assert args.source.is_file()
    generated=['AETHRA_FINAL_MOTION_SYNC_REEL.mp4','AETHRA_FINAL_MOTION_SYNC_AUDIO.wav',
               'AETHRA_MUSIC_ONLY.wav','AETHRA_SFX_ONLY.wav']
    if not args.replace_generated and any((ROOT/name).exists() for name in generated):
        parser.error('Generated output already exists. Back it up, then use --replace-generated for an intentional audio revision.')
    assert args.source.resolve() != (ROOT/generated[0]).resolve()
    identities=json.loads((ROOT/'analysis/source_identity.json').read_text())
    assert hashlib.sha256(args.source.read_bytes()).hexdigest()==identities[ARR['source_file']]['file_sha256'], 'Unexpected visual source'
    mus=music();sfx=np.zeros((N,2));audit=[]
    for e in ARR['events']:
        x=effect(e);start=e['start_frame']*1600
        place(sfx,x,e['start_frame']/30)
        nonzero=np.flatnonzero(np.max(np.abs(x),axis=1)>1e-9)
        audit.append({'id':e['id'],'visual_frame':e['start_frame'],'anchor_frame':e['anchor_frame'],
                      'placement_sample':start,'first_audible_sample_threshold_1e_9':int(start+nonzero[0]),
                      'peak_sample':int(start+np.argmax(np.max(np.abs(x),axis=1))),
                      'duration_samples':len(x)})
        assert start==round(e['start_frame']/30*SR)
    sfx=room(filt(sfx,low=130,high=9500),.1)
    # Smooth SFX-triggered ducking: up to 2.8 dB; no rhythmic pump.
    activity=ndimage.maximum_filter1d(np.max(np.abs(sfx),axis=1),size=1201)
    activity=ndimage.gaussian_filter1d(activity,SR*.021)
    duck=1-(1-db(-2.8))*np.clip(activity/.055,0,1)
    mus*=duck[:,None]
    final_fade=fade_env(N,.022,.32)
    mus*=final_fade[:,None];sfx*=final_fade[:,None]
    with tempfile.TemporaryDirectory(prefix='aethra_sound_') as temp:
        test=Path(temp)/'meter.wav'
        wavfile.write(test,SR,(mus+sfx).astype(np.float32))
        before=measure(test);gain=db(ARR['target_lufs']-float(before['input_i']))
        mus*=gain;sfx*=gain
        reductions=[]
        for _ in range(3):
            mus,sfx,reduction=limiter(mus,sfx,db(ARR['working_peak_ceiling_db']))
            reductions.append(reduction)
            wavfile.write(test,SR,(mus+sfx).astype(np.float32))
            current=measure(test);delta=ARR['target_lufs']-float(current['input_i'])
            if abs(delta)<=.1:break
            if delta>1.5:raise RuntimeError('Unexpected mastering adjustment')
            mus*=db(delta);sfx*=db(delta)
    pcm24(ROOT/'AETHRA_MUSIC_ONLY.wav',mus)
    pcm24(ROOT/'AETHRA_SFX_ONLY.wav',sfx)
    pcm24(ROOT/'AETHRA_FINAL_MOTION_SYNC_AUDIO.wav',mus+sfx)
    write_midi(ROOT/'source/AETHRA_MUSIC_NOTES.mid')
    (ROOT/'analysis/cue_sample_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    metrics={name:measure(ROOT/name) for name in ['AETHRA_FINAL_MOTION_SYNC_AUDIO.wav','AETHRA_MUSIC_ONLY.wav','AETHRA_SFX_ONLY.wav']}
    metrics['mastering']={'target_lufs':ARR['target_lufs'],'true_peak_ceiling_db':ARR['true_peak_ceiling_db'],
                          'pre_normalization':before,'initial_gain_db':20*np.log10(gain),
                          'shared_stereo_linked_peak_control_reduction_db':reductions,
                          'stem_recombination':'The delivered post-automation/post-master-gain stems sum to the final PCM mix within independent 24-bit dither.'}
    video=ROOT/'AETHRA_FINAL_MOTION_SYNC_REEL.mp4'
    subprocess.run(['ffmpeg','-y' if args.replace_generated else '-n','-v','error','-i',str(args.source),'-i',str(ROOT/'AETHRA_FINAL_MOTION_SYNC_AUDIO.wav'),
        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000',
        '-map_metadata','-1','-movflags','+faststart','-t','15',str(video)],check=True)
    metrics['final_aac_in_mp4']=measure(video)
    assert abs(float(metrics['AETHRA_FINAL_MOTION_SYNC_AUDIO.wav']['input_i'])-ARR['target_lufs'])<=.3
    assert float(metrics['final_aac_in_mp4']['input_tp'])<=ARR['true_peak_ceiling_db']
    (ROOT/'analysis/loudness.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps({'pcm':metrics['AETHRA_FINAL_MOTION_SYNC_AUDIO.wav'],'aac':metrics['final_aac_in_mp4'],
                      'master_gain_db':20*np.log10(gain),'limiting_db':reductions},indent=2))
    print('Original music and 30 synchronized cues produced; video integrated with -c:v copy.')

if __name__=='__main__':main()
