const {chromium}=require('C:/Users/MVJD/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const page=await browser.newPage({viewport:{width:1500,height:1100}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://localhost:3000/AethraPrimo',{waitUntil:'networkidle',timeout:60000});
 await page.screenshot({path:'qa/studio-preview.png'});
 fs.writeFileSync('qa/studio-preview.json',JSON.stringify({url:page.url(),title:await page.title(),errors},null,2));
 console.log(await page.locator('body').innerText());
 await browser.close();
})();
