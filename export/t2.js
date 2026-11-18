const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const out={};
for(const w of [360,390,1024,1280,1440]){const p=await b.newPage({viewport:{width:w,height:900}});const errs=[];
p.on('console',m=>{if(['error','warning'].includes(m.type()))errs.push(m.text())});p.on('pageerror',e=>errs.push('JS '+e.message));p.on('requestfailed',r=>errs.push('FAIL '+r.url()));
await p.goto('http://127.0.0.1:8765/');await p.waitForTimeout(1500);
const root=w>=1280?'.v-d':'.v-m';
out[w]=await p.evaluate(r=>({docW:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,vis:getComputedStyle(document.querySelector(r)).display,
 agenda:document.querySelector(r+' [data-agenda-link]').innerText.replace(/\s+/g,' '),cds:[...document.querySelectorAll(r+' [data-countdown]')].map(e=>e.textContent),ls:document.querySelector(r+' [data-lastsunday]').textContent,
 broken:[...document.querySelectorAll(r+' img')].filter(i=>i.complete&&i.naturalWidth===0&&i.loading!=='lazy').map(i=>i.src),h:document.documentElement.scrollHeight}),root);
// interactions
await p.click(root+' [data-tier="access"]');const t=await p.evaluate(r=>[...document.querySelectorAll(r+' [id*="tier-"]')].map(e=>e.id+':'+!e.hidden).join(' '),root);
await p.click(root+' [data-zona-tab="ocio"]');const z=await p.evaluate(r=>[...document.querySelectorAll(r+' [data-zona-panel]')].filter(e=>!e.hidden).map(e=>e.id).join(),root);
const pl=await p.$(root+' [data-zona-panel="ocio"] [data-place]');let po='none';if(pl){await pl.click();po=await p.evaluate(e=>{const id=e.getAttribute('aria-controls');return id+':'+!document.getElementById(id).hidden},pl);}
await p.click(root+' [data-flip="1"][aria-expanded]');await p.waitForTimeout(900);const f=await p.evaluate(r=>document.querySelector(r+' [data-flip-card="1"]').style.transform,root);
await p.click(root+' nav a[href*="llegar"]');await p.waitForTimeout(1200);const sy=await p.evaluate(()=>scrollY);
out[w].inter={t,z,po,f,sy,errs};
if(w==390||w==1440)await p.screenshot({path:'full'+w+'.png',fullPage:true});
await p.close();}
console.log(JSON.stringify(out,null,1));await b.close()})()
