import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now()}));}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){} document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(6000)
    d=pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
    print(pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), st=document.getElementById('studioScreen'); const out={cls:st.className, murs:[], flous:[]};
      ['#stpTons','#stpVue','#stpDots','#stpLab','#stpPals','#st3pn','#stPanel','.st3-spec'].forEach(s=>{const e=st.querySelector(s); if(e){const r=e.getBoundingClientRect(); out.murs.push([s,Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)]);}});
      st.querySelectorAll('*').forEach(e=>{ const f=getComputedStyle(e).filter; if(f&&f.indexOf('blur')>=0){ const r=e.getBoundingClientRect(); if(r.width>4) out.flous.push([e.id||e.className, f, Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)]); } }); return JSON.stringify(out); }"""))
    pg.screenshot(path='scratchpad/v140/studio0.png',clip={'x':d['x'],'y':d['y'],'width':390,'height':844})
    b.close()
