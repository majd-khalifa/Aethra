"""Three independent original scores; editable JSON is the audio renderer's input."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def event(events,start,duration,sound,midi=60,level=.03,pan=0):
    if start>=19.6:return
    events.append({'start':round(start,8),'duration':round(min(duration,20-start),8),'sound':sound,
                   'midi':midi,'level':level,'pan':pan})

def score_a():
    bpm=108;beat=60/bpm;e=[]
    chords=[([55,59,62,66,69],43,'Gmaj9'),([57,62,64,67,71],45,'A9sus4'),
            ([54,57,61,64],42,'F#m7'),([59,62,66,69,73],47,'Bm9'),
            ([52,55,59,62,66],40,'Em9'),([57,61,67,71,78],45,'A13'),
            ([50,57,61,64,66],38,'Dmaj9'),([52,55,59,62,66],40,'Em9'),
            ([50,54,57,59,64],38,'D6/9')]
    harmony=[]
    for bar,(notes,root,name) in enumerate(chords):
        start=bar*4*beat;harmony.append({'start':start,'chord':name,'notes':notes,'bass':root})
        for i,n in enumerate(notes):
            event(e,start,4.3*beat,'A_pad',n,.0075,(-.32,.25,-.1,.35,0)[i])
        for off in [.5,1.75,2.75,3.5]:
            for i,n in enumerate(notes[1:]):event(e,start+off*beat,.31,'A_keys',n+12,.0105,(-1)**i*.23)
        if bar<8:
            for off,n,lev in [(0,root,.068),(.75,root+12,.036),(1.75,root+7,.045),(2.5,root,.057),(3.25,root+12,.04)]:
                event(e,start+off*beat,.28,'A_bass',n,lev)
            for off,lev in [(0,.086),(1.75,.057),(2.5,.071),(3.25,.046)]:event(e,start+off*beat,.16,'kick_a',level=lev)
            for off in [1,3]:event(e,start+off*beat,.13,'rim_a',level=.049,pan=.06)
            for j in range(8):
                off=j*.5+(.048 if j%2 else 0)
                event(e,start+off*beat,.065,'hat_a',level=.013 if j%2 else .010,pan=(-1)**j*.2)
            for off in [.84,2.84]:event(e,start+off*beat,.04,'shaker_a',level=.007,pan=-.2)
    # A swung four-note question with a different four-note response; not the old mallet line.
    hooks=[(0,[66,69,71,76]),(1,[74,73,69,66]),(2,[66,69,73,76]),(3,[78,76,74,71]),
           (4,[67,71,74,78]),(5,[76,73,71,69]),(6,[66,69,76,74]),(7,[67,66,64,62])]
    for bar,notes in hooks:
        for off,n,d in zip([.72,1.44,2.22,3.18],notes,[.23,.31,.23,.38]):
            event(e,(bar*4+off)*beat,d,'A_pluck',n,.041,(-1)**n*.18)
    for start,n,d in [(18.02,69,.28),(18.35,71,.3),(18.68,76,.35),(19.12,74,.86)]:
        event(e,start,d,'A_pluck',n,.036,.1)
    event(e,17.80,1.3,'A_bass',38,.038)
    return {'name':'TECH GROOVE','bpm':bpm,'meter':'4/4','seed':2101,'swing':'delayed off-eighths and syncopated bass/chord stabs',
            'character':'confident, tactile, warm and rhythmic','harmony':harmony,'events':e}

def score_b():
    bpm=96;beat=60/bpm;e=[]
    chords=[([55,59,62,66,69,73],43,'Gmaj9#11'),([52,55,59,62,66,69],40,'Em11'),
            ([48,52,55,59,62,66],36,'Cmaj9#11'),([50,54,57,59,64],38,'D6/9'),
            ([59,62,66,69,73],47,'Bm9'),([57,60,64,67,71],45,'Am9'),
            ([59,62,66,69,76],47,'Bm11'),([52,55,59,62,66],40,'Em9')]
    harmony=[]
    for bar,(notes,root,name) in enumerate(chords):
        start=bar*4*beat;harmony.append({'start':start,'chord':name,'notes':notes,'bass':root})
        for i,n in enumerate(notes):event(e,start,4.7*beat,'B_pad',n,.010,(-1)**i*(.15+.05*i))
        event(e,start,2.2,'B_bass',root,.047)
        # Pulse notes derive from this score's changing extended voicings, not A's melody.
        order=[0,2,4,1,3,2,4,1]
        for j,k in enumerate(order):
            n=notes[k%len(notes)]+12
            event(e,start+j*.5*beat,.37,'B_pulse',n,.018+bar*.0012,(-1)**j*.27)
        if bar>=1:
            for off in [0,2.5]:event(e,start+off*beat,.19,'kick_b',level=.048 if bar<4 else .059)
            for off in [.5,1.5,2.5,3.5]:event(e,start+off*beat,.08,'hat_b',level=.010,pan=(-1)**int(off*2)*.15)
        if bar>=3:
            event(e,start+3*beat,.21,'brush_b',level=.024,pan=.05)
    # A long, rising line followed by a descending answer, with airy sustained timbres.
    for start,n,d,pan in [(1.1,74,.75,-.22),(3.65,78,.85,.22),(5.7,83,.85,-.15),
                          (8.2,81,.9,.2),(10.5,78,1.1,-.1),(12.9,76,.9,.1),
                          (15.6,74,1.1,-.16),(17.8,71,.75,.16),(18.8,76,1.15,0)]:
        event(e,start,d,'B_glass',n,.024,pan)
    return {'name':'FUTURE PULSE','bpm':bpm,'meter':'4/4','seed':2202,'swing':'straight eighth pulse with a slowly evolving filter',
            'character':'expansive, luminous, thoughtful and steadily developing','harmony':harmony,'events':e}

def score_c():
    bpm=126;beat=60/bpm;e=[]
    chords=[([59,62,66,69,73],47,'Bm9'),([50,54,57,59,64],38,'D6/9'),
            ([57,61,64,71],45,'Aadd9'),([52,55,59,62],40,'Em7'),
            ([55,59,62,66,69],43,'Gmaj9'),([54,57,61,64],42,'F#m7'),
            ([59,62,66,69,73],47,'Bm9'),([57,59,64,69],45,'Asus2'),
            ([50,54,57,59,64],38,'D6/9'),([59,62,66,73],47,'Bmadd9')]
    harmony=[]
    for bar,(notes,root,name) in enumerate(chords):
        start=bar*4*beat;harmony.append({'start':start,'chord':name,'notes':notes,'bass':root})
        for i,n in enumerate(notes):event(e,start,4.2*beat,'C_pad',n,.006,(-1)**i*.2)
        for off in [.5,1.5,2.75]:
            for i,n in enumerate(notes[1:]):event(e,start+off*beat,.18,'C_chord',n+12,.011,(-1)**i*.2)
        for off,n in [(0,root),(.75,root+12),(1.5,root),(2.75,root+7),(3.5,root+12)]:
            event(e,start+off*beat,.21,'C_bass',n,.061)
        for off,lev in [(0,.083),(1.5,.058),(2.75,.070),(3.5,.042)]:event(e,start+off*beat,.14,'kick_c',level=lev)
        for off in [1,3]:event(e,start+off*beat,.12,'clap_c',level=.040,pan=-.05)
        for j in range(8):event(e,start+j*.5*beat,.045 if j%2==0 else .072,'hat_c',level=.010 if j%2==0 else .014,pan=(-1)**j*.15)
        if bar%2:
            for off in [2.25,2.5,2.75]:event(e,start+off*beat,.035,'hat_c',level=.007,pan=.2)
    motifs=[([71,74,78,81,78,76,73,74],0),([74,78,81,83,81,78,76,74],2),
            ([71,74,78,81,83,81,78,76],4),([73,76,81,78,76,74,73,71],6),
            ([74,78,81,83,81,78,76,73],8)]
    for pitches,bar in motifs:
        for off,n in zip([.0,.75,1.25,1.75,2.5,3.25,4.5,6.75],pitches):
            start=(bar*4+off)*beat
            if start<18.5:event(e,start,.18 if off!=6.75 else .32,'C_lead',n,.035,(-1)**n*.12)
    # A compact B-minor/add-nine coda rather than A's major cadence or B's suspended decay.
    for start,n,d in [(18.5,78,.2),(18.77,76,.2),(19.05,74,.25),(19.35,71,.62)]:
        event(e,start,d,'C_lead',n,.030,0)
    for n in [59,62,66,73]:event(e,18.95,.99,'C_pad',n,.010,0)
    return {'name':'MODERN ELECTRO','bpm':bpm,'meter':'4/4 plus a two-beat closing coda','seed':2303,
            'swing':'tight syncopated sixteenth-note electro with short call-and-response phrases',
            'character':'bright, youthful, crisp and energetic without a drop','harmony':harmony,'events':e}

def main():
    for key,score in [('A',score_a()),('B',score_b()),('C',score_c())]:
        # A short musical pocket around final branding; SFX are never moved to the beat.
        for e in score['events']:
            e['duration']=min(e['duration'],20-e['start'])
        score.update({'version':key,'sample_rate':48000,'duration_seconds':20,'target_lufs':-15.5,
                      'source_policy':'Independent new composition; no prior music recording, arrangement or melodic phrase is reused.'})
        score['events'].sort(key=lambda x:x['start'])
        path=ROOT/'source'/f'{key}_{score["name"].replace(" ","_")}.json'
        assert not path.exists(),'Preserve editable score; edit existing JSON rather than overwriting it'
        path.write_text(json.dumps(score,indent=2)+'\n')
        print(key,score['name'],score['bpm'],'BPM;',len(score['events']),'editable events')

if __name__=='__main__':main()
