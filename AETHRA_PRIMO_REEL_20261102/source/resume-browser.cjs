// Download the identical official Remotion-patched browser with a longer idle
// allowance on slow connections. This does not select a different render browser.
const https=require('node:https');const fs=require('node:fs');
const path=require('node:path');const {pipeline}=require('node:stream/promises');
const dest=path.resolve('node_modules/.remotion/chrome-headless-shell/chromium-headless-shell-win-x64-158.0.8127.2.zip');
const url='https://remotion.media/chromium-headless-shell-win-x64-158.0.8127.2.zip?clear';
const start=fs.existsSync(dest)?fs.statSync(dest).size:0;
function get(u){return new Promise((resolve,reject)=>{const req=https.get(u,{headers:start?{Range:`bytes=${start}-`}:{}},res=>{if(res.statusCode>=300&&res.statusCode<400&&res.headers.location){res.resume();get(new URL(res.headers.location,u)).then(resolve,reject);return;}if(![200,206].includes(res.statusCode)){reject(new Error(String(res.statusCode)));return;}resolve(res);});req.on('error',reject);req.setTimeout(180000,()=>req.destroy(new Error('180-second idle timeout')));});}
(async()=>{const res=await get(url);console.log('Official browser download',res.statusCode,res.headers['content-range']||res.headers['content-length']);const output=fs.createWriteStream(dest,{flags:res.statusCode===206?'a':'w'});let last=0;res.on('data',()=>{const size=fs.existsSync(dest)?fs.statSync(dest).size:0;if(size-last>10_000_000){console.log('Downloaded bytes:',size);last=size;}});await pipeline(res,output);console.log('Download completed:',fs.statSync(dest).size);})().catch(e=>{console.error(e);process.exit(1)});
