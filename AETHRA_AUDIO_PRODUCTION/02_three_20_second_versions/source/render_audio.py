"""Render three independent scores while preserving approved SFX PCM exactly."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
import tempfile
import wave
import numpy as np
from scipy import signal, ndimage
from scipy.io import wavfile

ROOT=Path(__file__).resolve().parents[1]
SR=48000;N=960000
NAMES={'A':'TECH_GROOVE','B':'FUTURE_PULSE','C':'MODERN_ELECTRO'}

def db(x):return 10**(x/20)
def hz(n):return 440*2**((n-69)/12)
def env(n,attack=.004,release=.03):
    a=np.ones(n);i=min(n,max(1,round(attack*SR)));r=min(n,max(1,round(release*SR)))
    a[:i]*=np.sin(np.linspace(0,np.pi/2,i))**2;a[-r:]*=np.cos(np.linspace(0,np.pi/2,r))**2
    return a
def stereo(x,p=0):
    angle=(np.clip(p,-1,1)+1)*np.pi/4
    return np.column_stack((x*np.cos(angle),x*np.sin(angle)))
def filt(x,lo=None,hi=None):
    cutoff=[lo,hi] if lo and hi else (lo or hi)
    return signal.sosfilt(signal.butter(2,cutoff,btype='bandpass' if lo and hi else ('highpass' if lo else 'lowpass'),fs=SR,output='sos'),x,axis=0)
def place(target,x,start):
    i=round(start*SR);end=min(N,i+len(x))
    if i<end:target[i:end]+=x[:end-i]

def pcm_read(path):
    with wave.open(str(path),'rb') as w:
        assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(SR,2,3)
        raw=w.readframes(w.getnframes())
    b=np.frombuffer(raw,np.uint8).reshape(-1,3).astype(np.int32)
    v=b[:,0]+(b[:,1]<<8)+(b[:,2]<<16);v=(v^0x800000)-0x800000
    return v.reshape(-1,2),raw

def pcm_write(path,integers):
    assert integers.max()<8388608 and integers.min()>=-8388608
    b=np.ascontiguousarray(integers,dtype='<i4').view(np.uint8).reshape(-1,4)[:,:3].tobytes()
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(3);w.setframerate(SR);w.writeframes(b)

def quantize(x,rng):
    assert np.max(np.abs(x))<1
    return np.rint(x*8388608+rng.random(x.shape)-rng.random(x.shape)).astype(np.int32)

def common_sfx():
    path=ROOT/'source/approved_reference/AETHRA_SFX_15S_APPROVED.wav'
    reference=json.loads((ROOT/'source/approved_reference/manifest.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==reference['files'][path.name]['sha256'],'Approved SFX reference changed'
    approved,raw=pcm_read(path)
    assert approved.shape==(720000,2)
    tail=np.zeros((240000,2));rng=np.random.default_rng(2404)
    # Only two complementary new cues. The original 720,000 frames are never synthesized or processed.
    t=np.arange(round(.43*SR))/SR
    noise=filt(rng.normal(size=len(t)),lo=1100,hi=3300)
    shimmer=np.sin(2*np.pi*hz(86)*t)*np.exp(-t*11)
    light=(noise*.035*np.sin(np.linspace(0,np.pi,len(t)))**2+shimmer*.025)*env(len(t),.018,.12)
    i=487*1600-720000;tail[i:i+len(t)]+=stereo(light,.16)
    t=np.arange(round(.43*SR))/SR
    resolve=(np.sin(2*np.pi*hz(74)*t)+.42*np.sin(2*np.pi*hz(81)*t))*np.exp(-t*10)*env(len(t),.008,.13)*.038
    i=582*1600-720000;tail[i:i+len(t)]+=stereo(resolve)
    extended=np.vstack([approved,quantize(tail,rng)])
    path=ROOT/'AETHRA_20S_APPROVED_SFX_COMMON.wav';pcm_write(path,extended)
    ints,new_raw=pcm_read(path)
    assert new_raw[:len(raw)]==raw and np.array_equal(ints[:720000],approved)
    audit={'approved_pcm_bytes':len(raw),'approved_pcm_sha256':hashlib.sha256(raw).hexdigest(),
           'extended_prefix_sha256':hashlib.sha256(new_raw[:len(raw)]).hexdigest(),
           'original_15s_pcm_bit_identical':True,'original_30_cues_unchanged':True,
           'new_cues':[{'frame':487,'seconds':487/30,'description':'Quiet airy glint follows the first visible CTA edge light.'},
                       {'frame':582,'seconds':19.4,'description':'Soft tonal settle accompanies the end of the closing group movement.'}]}
    (ROOT/'analysis/sfx_preservation.json').write_text(json.dumps(audit,indent=2)+'\n')
    return extended.astype(np.float64)/8388608

def synth(e,rng,bpm):
    sound=e['sound'];t=np.arange(max(1,round(e['duration']*SR)))/SR;f=hz(e['midi']);x=np.zeros(len(t))
    if sound.endswith('_pad'):
        style=sound[0];attack={'A':.12,'B':.28,'C':.08}[style]
        for detune,weight in [(-.035,.25),(0,.5),(.035,.25)]:
            frequency=f*2**(detune/12)
            x+=weight*(np.sin(2*np.pi*frequency*t)+.13*np.sin(2*np.pi*frequency*2*t)+.035*np.sin(2*np.pi*frequency*3*t))
        if style=='B':x*=.64+.36*(.5+.5*np.sin(2*np.pi*(bpm/60)*2*t-.4))
        x*=env(len(t),attack,min(.5,e['duration']/3))
    elif sound=='A_keys':
        x=(np.sin(2*np.pi*f*t)+.16*np.sin(2*np.pi*f*3*t)+.035*np.sin(2*np.pi*f*5*t))*np.exp(-t*9)*env(len(t),.005,.035)
    elif sound=='A_pluck':
        for k in range(1,13):x+=np.sin(2*np.pi*f*k*t+.07*k)/(k**1.55)*np.exp(-t*(4.4+k*1.3))
        x*=env(len(t),.004,.04)
    elif sound=='B_pulse':
        phase=2*np.pi*f*t+.13*np.sin(2*np.pi*2.8*t)
        for k in range(1,9):x+=np.sin(phase*k)/(k**1.8)*np.exp(-t*k*2.2)
        x*=np.exp(-t*3.8)*env(len(t),.015,.085)
    elif sound=='B_glass':
        x=(np.sin(2*np.pi*f*t+.22*np.sin(2*np.pi*f*1.5*t)*np.exp(-t*3))+.10*np.sin(2*np.pi*f*3.001*t))*np.exp(-t*2.4)*env(len(t),.035,.18)
    elif sound in ['C_lead','C_chord']:
        # Band-limited narrow pulse, with partial envelopes instead of harsh discontinuities.
        for k in range(1,9):x+=np.sin(np.pi*k*.32)/k*np.sin(2*np.pi*f*k*t)*np.exp(-t*k*(1.9 if sound=='C_lead' else 4.0))
        x*=1.25*np.exp(-t*5.0)*env(len(t),.004,.028)
    elif sound.endswith('_bass'):
        style=sound[0]
        harmonics={'A':[1,.28,.11,.035],'B':[1,.12,.035,0],'C':[1,.30,.16,.05]}[style]
        for k,a in enumerate(harmonics,1):x+=a*np.sin(2*np.pi*f*k*t)
        x*=np.exp(-t*(7.5 if style=='C' else (5 if style=='A' else 1.5)))*env(len(t),.009,.055)
    elif sound.startswith('kick_'):
        base={'a':71,'b':66,'c':79}[sound[-1]]
        phase=2*np.pi*np.cumsum(base+48*np.exp(-t*45))/SR
        x=(np.sin(phase)+.16*np.sin(phase*2))*np.exp(-t*27)*env(len(t),.003,.035)
    elif sound=='rim_a':
        noise=filt(rng.normal(size=len(t)),lo=850,hi=4000)
        x=(.4*noise*np.exp(-t*65)+.44*np.sin(2*np.pi*1170*t)*np.exp(-t*80)+.17*np.sin(2*np.pi*790*t)*np.exp(-t*70))*env(len(t),.001,.018)
    elif sound=='clap_c':
        noise=filt(rng.normal(size=len(t)),lo=900,hi=6000)
        amplitude=np.exp(-t*39)
        for d in [.008,.016]:amplitude+=.45*np.exp(-np.maximum(t-d,0)*85)*(t>=d)
        x=noise*amplitude*.65*env(len(t),.001,.025)
    elif sound=='brush_b':
        x=filt(rng.normal(size=len(t)),lo=1200,hi=5000)*np.exp(-t*20)*env(len(t),.009,.05)
    elif sound.startswith('hat_') or sound=='shaker_a':
        high={'a':6800,'b':5700,'c':7800}.get(sound[-1],6500)
        x=filt(rng.normal(size=len(t)),lo=2800,hi=high)*np.exp(-t*(65 if sound.endswith('c') else 48))*env(len(t),.002,.015)
    else:raise ValueError(sound)
    return stereo(x*e['level'],e['pan'])

def music(score):
    rng=np.random.default_rng(score['seed']);dry=np.zeros((N,2));bass=np.zeros((N,2))
    for e in score['events']:
        # Preserve a clean musical pocket for the existing final branding SFX.
        percussion=e['sound'].startswith(('kick','rim','clap','hat','brush','shaker'))
        if percussion and 12.9<e['start']<13.45:continue
        x=synth(e,rng,score['bpm']);place(bass if '_bass' in e['sound'] or e['sound'].startswith('kick') else dry,x,e['start'])
    dry=filt(dry,lo=100,hi=8200);bass=filt(bass,lo=48,hi=1400)
    colored=filt(dry,lo=430,hi=4400)
    reflection={'A':[(.023,.10),(.071,.075),(.144,.045)],
                'B':[(.047,.16),(.131,.13),(.281,.095),(.463,.045)],
                'C':[(.019,.085),(.063,.06),(.127,.035)]}[score['version']]
    for delay,gain in reflection:
        d=round(delay*SR);dry[d:]+=colored[:-d,::-1]*gain
    result=np.tanh((dry+bass)*1.12)/1.12
    result*=env(N,.018,.38)[:,None]
    return result

def measure(path):
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af',
        'loudnorm=I=-15.5:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    return json.loads(re.findall(r'\{\s*"input_i".*?\}',r.stderr,re.S)[-1])

def protect_music(music,sfx,over_sfx):
    # Preserve every SFX sample. Any peak intervention attenuates only the music.
    over_music=signal.resample_poly(music,4,1,axis=0)
    ceiling=db(-1.85)
    positive=over_music>=0
    margin=np.where(positive,ceiling-over_sfx,ceiling+over_sfx)
    bounds=margin/np.maximum(np.abs(over_music),1e-12)
    required=np.minimum(1,np.min(bounds.reshape(N,4,2),axis=(1,2)))
    required=np.clip(required,0,1)
    if np.min(required)>.99999:return music,0.0
    required=ndimage.minimum_filter1d(required,size=1153,mode='nearest')
    gains=np.empty(N);last=1.;release=1-np.exp(-1/(SR*.09))
    for i,g in enumerate(required):last=min(g,last+(1-last)*release);gains[i]=last
    gains=ndimage.gaussian_filter1d(gains,24)
    return music*gains[:,None],float(-20*np.log10(max(gains.min(),1e-6)))

def midi(path,score):
    def vlq(n):
        b=[n&127];n>>=7
        while n:b.insert(0,(n&127)|128);n>>=7
        return bytes(b)
    tempo=round(60_000_000/score['bpm']);ev=[(0,b'\xff\x51\x03'+tempo.to_bytes(3,'big'))]
    rate=480*score['bpm']/60
    for e in score['events']:
        if not e['sound'].startswith(('A_','B_','C_')):continue
        i=round(e['start']*rate);end=round((e['start']+e['duration'])*rate)
        ev.extend([(i,bytes([0x90,e['midi'],70])),(end,bytes([0x80,e['midi'],0]))])
    data=b'';last=0
    for tick,b in sorted(ev,key=lambda x:x[0]):data+=vlq(tick-last)+b;last=tick
    data+=b'\x00\xff\x2f\x00';path.write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(data))+data)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--replace-generated',action='store_true');args=parser.parse_args()
    allnames=[f'AETHRA_20S_{k}_{v}.mp4' for k,v in NAMES.items()]
    assert args.replace_generated or not any((ROOT/n).exists() for n in allnames),'Use --replace-generated for an intentional revision of these new outputs'
    if not (ROOT/'source/SHARED_20S_PICTURE.mp4').exists():
        subprocess.run([sys.executable,str(ROOT/'source/build_picture.py'),'--replace-generated'],check=True)
    sfx=common_sfx();over_sfx=signal.resample_poly(sfx,4,1,axis=0)
    activity=ndimage.maximum_filter1d(np.max(np.abs(sfx),axis=1),size=961)
    activity=ndimage.gaussian_filter1d(activity,SR*.028)
    duck=1-(1-db(-5.5))*np.clip(activity/.16,0,1)
    sfx_int,_=pcm_read(ROOT/'AETHRA_20S_APPROVED_SFX_COMMON.wav')
    report={'common_sfx':measure(ROOT/'AETHRA_20S_APPROVED_SFX_COMMON.wav'),'versions':{}}
    for key,name in NAMES.items():
        score=json.loads((ROOT/'source'/f'{key}_{name}.json').read_text())
        bed=music(score)*duck[:,None]
        with tempfile.TemporaryDirectory(prefix='aethra20_mix_') as temp:
            meter=Path(temp)/'mix.wav'
            wavfile.write(meter,SR,(bed+sfx).astype(np.float32))
            initial=measure(meter);gain=db(score['target_lufs']-float(initial['input_i']))
            max_reduction=0
            for iteration in range(7):
                delivered,reduction=protect_music(bed*gain,sfx,over_sfx)
                wavfile.write(meter,SR,(delivered+sfx).astype(np.float32))
                m=measure(meter);delta=score['target_lufs']-float(m['input_i'])
                max_reduction=max(max_reduction,reduction)
                print(key,'mix pass',iteration+1,'LUFS',m['input_i'],'music gain dB',round(20*np.log10(gain),2),flush=True)
                if abs(delta)<=.08:break
                # Only music gain changes. Original SFX are never turned down or normalized.
                gain*=db(delta*1.6)
            assert abs(float(m['input_i'])-score['target_lufs'])<=.2
        rng=np.random.default_rng(score['seed']+500)
        music_int=quantize(delivered,rng);mix_int=music_int+sfx_int
        music_path=ROOT/f'AETHRA_20S_{key}_MUSIC_ONLY.wav';mix_path=ROOT/f'AETHRA_20S_{key}_FINAL_MIX.wav'
        pcm_write(music_path,music_int);pcm_write(mix_path,mix_int)
        video=ROOT/f'AETHRA_20S_{key}_{name}.mp4'
        subprocess.run(['ffmpeg','-y' if args.replace_generated else '-n','-v','error','-i',str(ROOT/'source/SHARED_20S_PICTURE.mp4'),'-i',str(mix_path),
            '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-t','20','-map_metadata','-1','-movflags','+faststart',str(video)],check=True)
        pcm_metrics=measure(mix_path);aac_metrics=measure(video)
        assert float(aac_metrics['input_tp'])<=-1.5,(key,aac_metrics)
        report['versions'][key]={'name':name,'bpm':score['bpm'],'music_gain_db':float(20*np.log10(gain)),
            'music_only_peak_control_max_reduction_db':max_reduction,'mix_wav':pcm_metrics,
            'aac_in_mp4':aac_metrics,'music_wav':measure(music_path),
            'approved_sfx_processing':'none; original PCM samples and all 30 cue timings retained exactly'}
        midi(ROOT/'source'/f'{key}_{name}.mid',score)
        (ROOT/'analysis/loudness.json').write_text(json.dumps(report,indent=2)+'\n')
        print('Completed',key,name,'AAC',aac_metrics['input_i'],'LUFS;',aac_metrics['input_tp'],'dBTP',flush=True)
    print('Three independent original compositions delivered over one unchanged common SFX stem.',flush=True)

if __name__=='__main__':main()
