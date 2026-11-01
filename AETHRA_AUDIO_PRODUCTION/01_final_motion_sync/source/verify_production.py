"""Technical identity, audio safety and real-time Chromium playback checks."""
from pathlib import Path
import argparse
import asyncio
import hashlib
import json
import subprocess
import wave
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import numpy as np
from scipy import signal
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]

def probe(path,*extra):
    return json.loads(subprocess.check_output(['ffprobe','-v','error',*extra,'-of','json',str(path)]))

def wav_read(path):
    with wave.open(str(path),'rb') as w:
        metadata={'rate':w.getframerate(),'channels':w.getnchannels(),'sample_width':w.getsampwidth(),'frames':w.getnframes()}
        assert metadata=={'rate':48000,'channels':2,'sample_width':3,'frames':720000}
        b=np.frombuffer(w.readframes(w.getnframes()),dtype=np.uint8).reshape(-1,3).astype(np.int32)
        v=b[:,0]+(b[:,1]<<8)+(b[:,2]<<16)
        signed=(v^0x800000)-0x800000
        return signed.reshape(-1,2)/8388608.0,metadata

async def browser_check():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,
            args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
        page=await browser.new_page(viewport={'width':430,'height':932})
        # Managed Chromium blocks file:// navigation. Local HTTP is its supported test route.
        await page.goto(f'http://127.0.0.1:{server.server_port}/review.html')
        await page.wait_for_function('document.getElementById("reel").readyState >= 2')
        result=await page.evaluate('''async () => {
            const v=document.getElementById('reel');
            const ctx=new AudioContext();
            const source=ctx.createMediaElementSource(v), meter=ctx.createAnalyser();
            meter.fftSize=2048; source.connect(meter);meter.connect(ctx.destination);
            await ctx.resume(); const values=new Float32Array(meter.fftSize);
            let maxObservedRms=0;let samples=0;
            const timer=setInterval(()=>{meter.getFloatTimeDomainData(values);maxObservedRms=Math.max(maxObservedRms,Math.sqrt(values.reduce((a,b)=>a+b*b,0)/values.length));samples++;},40);
            await v.play();
            await new Promise((resolve,reject)=>{v.onended=resolve;v.onerror=()=>reject(new Error('Video playback failed'));setTimeout(()=>reject(new Error('Playback timeout')),22000);});
            clearInterval(timer);const quality=v.getVideoPlaybackQuality();
            return {ended:v.ended,duration:v.duration,currentTime:v.currentTime,width:v.videoWidth,height:v.videoHeight,
                decodedFrames:quality.totalVideoFrames,droppedFrames:quality.droppedVideoFrames,
                error:v.error ? v.error.message : null,muted:v.muted,volume:v.volume,
                audioContextState:ctx.state,maximumObservedAudioRms:maxObservedRms,meterSamples:samples};
        }''')
        await browser.close()
        server.shutdown();server.server_close()
        assert result['ended'] and result['error'] is None
        assert result['duration']==15 and (result['width'],result['height'])==(1080,1920)
        assert result['decodedFrames']==450
        assert not result['muted'] and result['maximumObservedAudioRms']>.01
        return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True)
    args=parser.parse_args();source=args.source;final=ROOT/'AETHRA_FINAL_MOTION_SYNC_REEL.mp4'
    report={'source_file':source.name,'video_checks':{},'audio_checks':{}}
    source_metadata=probe(source,'-show_streams','-show_format')
    metadata=probe(final,'-show_streams','-show_format')
    v=next(s for s in metadata['streams'] if s['codec_type']=='video')
    a=next(s for s in metadata['streams'] if s['codec_type']=='audio')
    assert len(metadata['streams'])==2
    assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],v['avg_frame_rate'],v['nb_frames'])==('h264',1080,1920,'30/1','30/1','450')
    assert v['duration']=='15.000000' and metadata['format']['duration']=='15.000000'
    assert a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2
    assert a['duration']=='15.000000' and a['start_time']=='0.000000' and v['start_time']=='0.000000'
    entries='packet=pts,dts,duration,size,flags,data_hash'
    source_packets=probe(source,'-select_streams','v:0','-show_packets','-show_entries',entries,'-show_data_hash','sha256')['packets']
    final_packets=probe(final,'-select_streams','v:0','-show_packets','-show_entries',entries,'-show_data_hash','sha256')['packets']
    assert len(source_packets)==450 and source_packets==final_packets
    annexb=subprocess.check_output(['ffmpeg','-v','error','-i',str(final),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','-'])
    identity=json.loads((ROOT/'analysis/source_identity.json').read_text())
    expected=identity[source.name]
    assert hashlib.sha256(annexb).hexdigest()==expected['video_annexb_sha256']
    hashes=subprocess.check_output(['ffmpeg','-v','error','-i',str(final),'-map','0:v:0','-an','-f','framemd5','-']).decode()
    rows=[x for x in hashes.splitlines() if not x.startswith('#')]
    frames=[x.split(',')[-1].strip() for x in rows]
    assert len(frames)==450 and frames==expected['decoded_frame_hashes']
    for name,info in identity.items():
        path=source.parent/name
        assert path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==info['file_sha256']
        assert info['video_annexb_sha256']==expected['video_annexb_sha256'] and info['decoded_frame_hashes']==frames
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(final),'-f','null','-'],capture_output=True,text=True)
    assert decoded.returncode==0 and not decoded.stderr.strip(),decoded.stderr
    report['video_checks']={'resolution':[1080,1920],'fps':'30/1','duration_seconds':15.0,'codec':'h264',
        'video_packets':450,'packet_payload_hashes_and_pts_dts_durations_identical':True,
        'decoded_frame_hashes_identical':450,'annexb_sha256':expected['video_annexb_sha256'],
        'all_four_original_exports_unchanged':True,'all_four_source_video_streams_identical':True,
        'full_decode_errors':0,'original_visual_stream_copied':True}
    mix,wm=wav_read(ROOT/'AETHRA_FINAL_MOTION_SYNC_AUDIO.wav')
    music,_=wav_read(ROOT/'AETHRA_MUSIC_ONLY.wav');sfx,_=wav_read(ROOT/'AETHRA_SFX_ONLY.wav')
    for ar in [mix,music,sfx]:assert np.max(np.abs(ar))<1 and np.isfinite(ar).all()
    error=float(np.max(np.abs(mix-music-sfx)));assert error<=3/8388608
    assert np.max(np.abs(mix[[0,-1]]))<2e-6
    mid=np.mean(mix,axis=1);stereo_rms=np.sqrt(np.mean(mix**2));mono_rms=np.sqrt(np.mean(mid**2))
    mono_change=float(20*np.log10(mono_rms/stereo_rms));assert mono_change>-3
    decoded_audio=subprocess.check_output(['ffmpeg','-v','error','-i',str(final),'-map','0:a:0','-t','15','-f','f32le','-ac','2','-ar','48000','-'])
    aac=np.frombuffer(decoded_audio,dtype='<f4').reshape(-1,2)
    assert len(aac)==720000
    # Exclude boundary padding; verify encoder delay was compensated in the MP4.
    x=np.mean(aac[48000:144000],axis=1);y=mid[48000:144000]
    correlation=signal.correlate(x,y,mode='full',method='fft')
    lags=signal.correlation_lags(len(x),len(y),mode='full');valid=np.abs(lags)<=1600
    lag=int(lags[valid][np.argmax(correlation[valid])]);assert abs(lag)<=48
    checkpoints={}
    for frame in [15,287,296,305,398]:
        start=frame*1600;end=start+4800
        value=float(np.corrcoef(aac[start:end].mean(axis=1),mid[start:end])[0,1])
        assert value>.9
        checkpoints[str(frame)]={'aac_pcm_correlation':value,'encoded_audio_has_correct_interval':True}
    metrics=json.loads((ROOT/'analysis/loudness.json').read_text())
    assert abs(float(metrics['final_aac_in_mp4']['input_i'])+15)<=.3
    assert float(metrics['final_aac_in_mp4']['input_tp'])<=-1.5
    arrangement=json.loads((ROOT/'source/arrangement.json').read_text());audit=json.loads((ROOT/'analysis/cue_sample_audit.json').read_text())
    assert len(audit)==len(arrangement['events'])==30
    for e,c in zip(arrangement['events'],audit):assert c['id']==e['id'] and c['placement_sample']==e['start_frame']*1600
    report['audio_checks']={'wav':wm,'duration_seconds':15.0,'pcm_clipped_samples':int(np.count_nonzero(np.abs(mix)>=1)),
        'stems_recombine_max_absolute_error':error,'stems_recombine_tolerance':'3 least significant 24-bit steps',
        'stereo_correlation':float(np.corrcoef(mix.T)[0,1]),'mono_fold_down_rms_change_db':mono_change,
        'aac_timeline_samples':len(aac),'aac_uncompensated_delay_samples':lag,
        'aac_sync_checkpoints':checkpoints,'all_30_cues_sample_aligned':True,
        'pcm_lufs':float(metrics['AETHRA_FINAL_MOTION_SYNC_AUDIO.wav']['input_i']),
        'aac_lufs':float(metrics['final_aac_in_mp4']['input_i']),
        'aac_true_peak_db':float(metrics['final_aac_in_mp4']['input_tp'])}
    report['browser_playback']=asyncio.run(browser_check())
    report['limitations']=['No physical Windows, iOS or Android device or Instagram re-encode was tested.',
        'Headless Chromium playback and signal measurements do not substitute for a human listening approval.',
        'The Instagram reference was inaccessible under the current allowed-host policy; it was not analyzed.',
        'REAPER project structure and media paths are provided, but REAPER itself is not installed for GUI testing.']
    report['files']={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in ROOT.iterdir() if p.suffix in ['.mp4','.wav']}
    (ROOT/'analysis/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'video':report['video_checks'],'audio':report['audio_checks'],'browser':report['browser_playback']},indent=2))

if __name__=='__main__':main()
