"""Verify picture identity, approved SFX, stem sums, safety, sync and full playback."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import asyncio
import hashlib
import json
import subprocess
import numpy as np
from scipy import signal
from playwright.async_api import async_playwright
from render_audio import pcm_read,SR,N,NAMES

ROOT=Path(__file__).resolve().parents[1]

def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def framehashes(p):
    output=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-an','-f','framemd5','-']).decode()
    return [x.split(',')[-1].strip() for x in output.splitlines() if not x.startswith('#')]
def video_hash(p):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','-'])
    return hashlib.sha256(data).hexdigest()

async def browser_check():
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            if self.path.startswith('/__playback__'):
                key=self.path.split('__playback__')[1].split('.')[0]
                if key in NAMES:
                    body=f'<html><video id="{key}" controls playsinline preload="auto" src="/AETHRA_20S_{key}_{NAMES[key]}.mp4"></video></html>'.encode()
                    self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
            return super().do_GET()
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    results={}
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
            for key in NAMES:
                # One fresh element per export avoids counting preloaded frames from other players.
                page=await browser.new_page(viewport={'width':430,'height':932})
                await page.goto(f'http://127.0.0.1:{server.server_port}/__playback__{key}.html')
                await page.wait_for_function(f'document.getElementById("{key}").readyState>=2')
                result=await page.evaluate('''async key=>{
                    const v=document.getElementById(key);
                    const ctx=new AudioContext();const source=ctx.createMediaElementSource(v),meter=ctx.createAnalyser();meter.fftSize=2048;source.connect(meter);meter.connect(ctx.destination);await ctx.resume();
                    const buf=new Float32Array(meter.fftSize);let maximumAudioRms=0,sampled=0;
                    const timer=setInterval(()=>{meter.getFloatTimeDomainData(buf);maximumAudioRms=Math.max(maximumAudioRms,Math.sqrt(buf.reduce((a,b)=>a+b*b,0)/buf.length));sampled++;},40);
                    await v.play();await new Promise((r,j)=>{v.onended=r;v.onerror=()=>j(new Error('Media failed'));setTimeout(()=>j(new Error('Timeout')),27000);});
                    clearInterval(timer);const q=v.getVideoPlaybackQuality();const result={duration:v.duration,width:v.videoWidth,height:v.videoHeight,ended:v.ended,error:v.error?v.error.message:null,decodedFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,muted:v.muted,maximumAudioRms,sampled};await ctx.close();return result;
                }''',key)
                print('Browser metrics:',key,json.dumps(result),flush=True)
                assert result['duration']==20 and (result['width'],result['height'])==(1080,1920)
                assert result['ended'] and result['error'] is None and result['decodedFrames']==600
                assert result['maximumAudioRms']>.01 and not result['muted']
                results[key]=result;print('Unmuted full browser playback passed:',key,flush=True)
                await page.close()
            await browser.close()
    finally:server.shutdown();server.server_close()
    return results

def main():
    report={'versions':{},'shared_checks':{}}
    ref=ROOT/'source/approved_reference'
    source_manifest=json.loads((ref/'manifest.json').read_text())
    for name,info in source_manifest['files'].items():
        assert (ref/name).stat().st_size==info['bytes'] and hashlib.sha256((ref/name).read_bytes()).hexdigest()==info['sha256']
    reference=json.loads((ROOT/'source/approved_reference/source_identity.json').read_text())['AETHRA_A_Viral_Beat.mp4']['decoded_frame_hashes']
    intermediate=ROOT/'source/SHARED_20S_PICTURE.mp4'
    picture_hashes=framehashes(intermediate if intermediate.exists() else ROOT/'AETHRA_20S_A_TECH_GROOVE.mp4')
    assert len(picture_hashes)==600 and picture_hashes[:450]==reference
    common,raw=pcm_read(ROOT/'AETHRA_20S_APPROVED_SFX_COMMON.wav')
    approved,old_raw=pcm_read(ROOT/'source/approved_reference/AETHRA_SFX_15S_APPROVED.wav')
    assert common.shape==(960000,2) and raw[:len(old_raw)]==old_raw
    assert np.array_equal(common[:720000],approved)
    identities=[];music_arrays={};loud=json.loads((ROOT/'analysis/loudness.json').read_text())
    for key,name in NAMES.items():
        path=ROOT/f'AETHRA_20S_{key}_{name}.mp4';p=probe(path)
        assert p['format']['duration']=='20.000000' and len(p['streams'])==2
        v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio')
        assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],v['avg_frame_rate'],v['nb_frames'],v['duration'])==('h264',1080,1920,'30/1','30/1','600','20.000000')
        assert a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000' and a['duration']=='20.000000'
        assert a['start_time']=='0.000000' and v['start_time']=='0.000000'
        frames=framehashes(path);assert frames==picture_hashes
        picture=video_hash(path);identities.append(picture)
        decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],capture_output=True,text=True)
        assert decoded.returncode==0 and not decoded.stderr.strip()
        black=subprocess.run(['ffmpeg','-hide_banner','-i',str(path),'-an','-vf','blackdetect=d=0.001:pix_th=0.02','-f','null','-'],capture_output=True,text=True,check=True)
        assert 'black_start:' not in black.stderr
        mix,raw_mix=pcm_read(ROOT/f'AETHRA_20S_{key}_FINAL_MIX.wav');music,_=pcm_read(ROOT/f'AETHRA_20S_{key}_MUSIC_ONLY.wav')
        assert mix.shape==music.shape==(960000,2)
        assert np.array_equal(mix,music+common),'Stems must sum sample exactly'
        float_mix=mix.astype(float)/8388608;float_music=music.astype(float)/8388608
        assert np.max(np.abs(float_mix))<1 and np.max(np.abs(float_music))<1
        mono=float_mix.mean(axis=1);rms=np.sqrt(np.mean(float_mix**2));mono_db=float(20*np.log10(np.sqrt(np.mean(mono**2))/rms))
        assert mono_db>-3
        windows=np.sqrt(np.mean(mono.reshape(-1,480)**2,axis=1));assert np.min(windows[5:-5])>1e-5
        aac_bytes=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-t','20','-f','f32le','-ac','2','-ar','48000','-'])
        aac=np.frombuffer(aac_bytes,dtype='<f4').reshape(-1,2);assert len(aac)==960000
        x=aac[48000:144000].mean(axis=1);y=mono[48000:144000]
        corr=signal.correlate(x,y,method='fft');lags=signal.correlation_lags(len(x),len(y));mask=np.abs(lags)<=1600
        lag=int(lags[mask][np.argmax(corr[mask])]);assert abs(lag)<=48
        checkpoints={}
        for frame in [15,287,296,305,398,487,582]:
            i=frame*1600;j=i+4800;value=float(np.corrcoef(aac[i:j].mean(axis=1),mono[i:j])[0,1]);assert value>.98
            checkpoints[str(frame)]=value
        metrics=loud['versions'][key]['aac_in_mp4'];assert float(metrics['input_tp'])<=-1.5 and abs(float(metrics['input_i'])+15.5)<=.2
        music_arrays[key]=float_music[::48].mean(axis=1)
        report['versions'][key]={'frames':600,'duration':20.0,'size':[1080,1920],'fps':'30/1','video_annexb_sha256':picture,
            'decoded_frame_identity_to_shared_picture':True,'original_450_frames_preserved':True,
            'full_decode_errors':0,'black_segments':0,'wav_samples':960000,'wav_bit_depth':24,
            'stems_recombine_sample_exactly':True,'clipped_pcm_samples':0,'audio_gap_10ms_windows_excluding_50ms_fades':0,
            'stereo_correlation':float(np.corrcoef(float_mix.T)[0,1]),'mono_fold_down_change_db':mono_db,
            'aac_uncompensated_delay_samples':lag,'aac_pcm_sync_correlations':checkpoints,
            'aac_lufs':float(metrics['input_i']),'aac_true_peak_db':float(metrics['input_tp'])}
        print('Identity, complete decode, audio safety and sync passed:',key,flush=True)
    assert len(set(identities))==1
    correlations={}
    for a,b in [('A','B'),('A','C'),('B','C')]:
        r=float(np.corrcoef(music_arrays[a],music_arrays[b])[0,1]);assert abs(r)<.5;correlations[a+b]=r
    levels=[x['aac_lufs'] for x in report['versions'].values()]
    report['shared_checks']={'identical_20s_h264_streams':True,'picture_sha256':identities[0],
        'first_450_decoded_frames_bit_identical_to_approved_picture':True,
        'approved_15s_sfx_pcm_bit_identical':True,'original_30_cues_unchanged':True,'new_cues':2,
        'music_pairwise_waveform_correlations_at_1khz':correlations,
        'music_scores_have_different_tempi_harmonies_melodies_and_rhythms':True,
        'aac_loudness_spread_lu':max(levels)-min(levels)}
    report['browser_playback']=asyncio.run(browser_check())
    report['limitations']=['Physical phones, Windows playback hardware, headphones and Instagram transcoding were not tested.',
        'Signal measurements and unmuted browser playback are not human listening approval.',
        'REAPER project media paths were checked; REAPER GUI is not installed.']
    (ROOT/'analysis/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('All three complete 20-second versions verified.',flush=True)

if __name__=='__main__':main()
