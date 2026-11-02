"""Original procedural score and Foley. No recordings, loops or external music.
48 kHz / stereo / exactly 960,000 samples. Refuses to replace outputs.
"""
from pathlib import Path
import json, wave
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SR=48000
N=SR*20
rng=np.random.default_rng(20261102)
music=np.zeros((N,2)); sfx=music.copy(); cues=[]
def add(bus,t,x,gain=1,pan=0):
    start=round(t*SR); x=np.asarray(x)*gain
    end=min(N,start+len(x)); x=x[:end-start]
    bus[start:end,0]+=x*np.sqrt((1-pan)/2)
    bus[start:end,1]+=x*np.sqrt((1+pan)/2)
def tone(freq,dur,decay=7):
    t=np.arange(round(dur*SR))/SR
    return (np.sin(2*np.pi*freq*t)+.28*np.sin(2*np.pi*freq*2.01*t)+.09*np.sin(2*np.pi*freq*3.98*t))*np.exp(-decay*t)*np.minimum(t/.004,1)
def noise(dur):
    return rng.normal(0,1,round(dur*SR))
def cue(frame,name,x,gain=.2,pan=0):
    add(sfx,frame/30,x,gain,pan);cues.append(dict(frame=frame,seconds=frame/30,name=name))
# Light original pizzicato theme in D minor; warmer resolution to F major.
beat=60/112
notes=[74,77,81,77,76,74,69,72,74,77,79,81,77,76,74,69]
for i in range(38):
    t=i*beat
    if 7.15<t<9.3 or 13.5<t<14.5: continue
    midi=notes[i%len(notes)]
    add(music,t,tone(440*2**((midi-69)/12),.55,9),.13,(-1)**i*.22)
    if i%2==0:
        bass=[38,38,34,36][(i//8)%4]
        add(music,t,tone(440*2**((bass-69)/12),.65,5),.15)
    if i%2:
        t2=np.arange(6000)/SR
        add(music,t,noise(.125)*np.exp(-t2*45),.022,.4)
    if i%4==0:
        ts=np.arange(10000)/SR
        add(music,t,np.sin(2*np.pi*(85*ts-55*ts**2))*np.exp(-ts*28),.18,-.1)
# Quiet kitchen sizzle, clearly below captions and main cues.
ns=noise(6.8); ns=np.convolve(ns,np.ones(12)/12,mode='same')
add(sfx,0,ns,.018,-.5)
for f in [67,78,96]: cue(f,'controller button',tone(880,.045,80),.12,.45)
for f in [114,136]: cue(f,'football bounce',tone(105,.18,25),.42,.4)
cue(153,'comic woodblock reaction',tone(640,.18,38),.36)
cue(175,'second woodblock',tone(470,.17,32),.3)
# A nonverbal, synthesized breath exhale, not generated speech.
breath=noise(.65); breath=np.convolve(breath,np.ones(18)/18,mode='same')
bt=np.linspace(0,1,len(breath));breath*=np.sin(np.pi*bt)**1.5
cue(227,'AETHRA nonverbal sigh / synthesized breath',breath,.45,-.2)
for f in [243,253]: cue(f,'soft footstep',tone(130,.1,50),.25,-.2)
cue(266,'door closes',tone(74,.32,18)+tone(131,.32,30)*.3,.65,.35)
peel=noise(.36);peel=np.convolve(peel,np.ones(4)/4,mode='same')*np.linspace(.5,0,len(peel))
cue(272,'sticker peel',peel,.12,.3)
for f in [304,341,377]: cue(f,'phone tap',tone(1100,.055,90),.14,.3)
cue(398,'gentle phone chime',tone(1175,.3,14),.16,.25)
for f in [407,415,423]: cue(f,'fast clock tick',tone(1600,.035,100),.23)
cue(436,'doorbell first note',tone(784,.65,5),.34,.35)
cue(443,'doorbell second note',tone(622,.7,4),.32,.35)
cue(459,'grocery bag rustle',noise(.24)*np.linspace(.5,0,11520),.06,-.2)
for f,midi in [(476,77),(482,81),(488,84),(514,77),(520,81),(526,84)]:
    cue(f,'warm resolution chime',tone(440*2**((midi-69)/12),.8,5),.13)
mix=music+sfx
# Controlled fades; leave an audible natural tail before the final frame.
env=np.ones(N);env[:960]=np.linspace(0,1,960);env[-14400:]=np.linspace(1,0,14400)
mix*=env[:,None];music*=env[:,None];sfx*=env[:,None]
peak=np.max(np.abs(mix)); gain=min(.88/peak,1.4)
out=ROOT/'public/audio';out.mkdir(parents=True,exist_ok=True)
for name,data in [('music',music),('sfx',sfx),('final-mix',mix)]:
    p=out/(name+'.wav')
    if p.exists(): raise FileExistsError(p)
    pcm=(np.clip(data*gain,-1,1)*32767).astype('<i2')
    with wave.open(str(p),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
(ROOT/'source/sound-cues.json').write_text(json.dumps(cues,indent=2),encoding='utf-8')
print(json.dumps({'samples':N,'sample_rate':SR,'duration':N/SR,'peak_dbfs':float(20*np.log10(np.max(np.abs(mix*gain)))),'cues':len(cues)}))
