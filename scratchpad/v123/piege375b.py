import sys
from playwright.sync_api import sync_playwright
J=r"""([avant,apres])=>new Promise(async res=>{ const F=t=>promises.filter(q=>q.title===t)[0].id; const L=[]; 
  closeAll(); openDetail(F(avant)); await new Promise(r=>setTimeout(r,2200)); closeAll(); await new Promise(r=>setTimeout(r,700));
  const ids=['dptQui','dptQuand','dptTrace'], els=ids.map(i=>document.getElementById(i)), dp=document.getElementById('detailPoster'); const t0=performance.now();
  const st=()=>(new Error().stack||'').split('\n').slice(2,7).map(s=>s.trim().replace('http://127.0.0.1:8752/app.html','').slice(0,40)).join(' < ');
  const sp=CSSStyleDeclaration.prototype.setProperty, rp=CSSStyleDeclaration.prototype.removeProperty;
  CSSStyleDeclaration.prototype.setProperty=function(k,v,p){ const tr=document.getElementById('dptTrace'); const i=(tr&&tr.style===this)?2:els.findIndex(e=>e&&e.style===this); if(i>=0&&/color|display|visib|opac/.test(k)) L.push(((performance.now()-t0)|0)+' '+ids[i]+' SET '+k+'='+v+' @ '+st()); return sp.apply(this,arguments); };
  CSSStyleDeclaration.prototype.removeProperty=function(k){ const i=els.findIndex(e=>e&&e.style===this); if(i>=0&&/color|display/.test(k)) L.push(((performance.now()-t0)|0)+' '+ids[i]+' REMOVE '+k+' @ '+st()); return rp.apply(this,arguments); };
  els.forEach((e,i)=>{ if(!e) return; new MutationObserver(m=>m.forEach(x=>{ if(x.type==='attributes'&&x.attributeName==='style') return; L.push(((performance.now()-t0)|0)+' '+ids[i]+' MUT '+x.type+' '+(x.attributeName||'')+' → '+(x.type==='attributes'?e.getAttribute(x.attributeName):e.textContent.trim().slice(0,40))); })).observe(e,{attributes:true,childList:true,characterData:true,subtree:true}); });
  const lit=()=>ids.map(x=>document.getElementById(x)).map((e,i)=>e?ids[i].slice(3)+':'+e.textContent.trim().slice(0,14)+'/'+getComputedStyle(e).color.replace(/rgb|\s/g,'')+'~'+getComputedStyle(e).webkitTextFillColor.replace(/rgb|\s/g,'')+'~op'+getComputedStyle(e).opacity+'/'+getComputedStyle(e).display.slice(0,4)+'/'+(e.style.color||'-')+'/'+(e.getAttribute('data-lis')||'')+(e.getAttribute('data-ech')||''):'').join('  ');
  const mc=new MessageChannel(); let n=0; mc.port1.onmessage=()=>{ L.push(((performance.now()-t0)|0)+' ══ IMAGE op='+(+getComputedStyle(dp).opacity).toFixed(2)+' '+lit()); if(performance.now()-t0<1300) requestAnimationFrame(()=>mc.port2.postMessage(1)); else { CSSStyleDeclaration.prototype.setProperty=sp; CSSStyleDeclaration.prototype.removeProperty=rp; res(L); } };
  openDetail(F(apres)); requestAnimationFrame(()=>mc.port2.postMessage(1)); })"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); ctx.add_init_script("document.addEventListener('DOMContentLoaded',function(){ var s=document.createElement('style'); s.textContent='#detailPoster,#detailPoster *{transition:none!important}'; document.head.appendChild(s); });"); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t)}",sys.argv[1]); pg.wait_for_timeout(500)
    for k in range(5):
        L=pg.evaluate(J,[sys.argv[2],sys.argv[3]]); av=None; print('--- passe',k)
        for l in L:
            if 'IMAGE' in l:
                s=l.split('IMAGE')[1]
                if s==av: continue
                av=s
            if 'IMAGE' in l or ('dptTrace' in l): print(l[:260])
