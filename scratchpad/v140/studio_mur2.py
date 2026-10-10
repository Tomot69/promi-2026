import sys, json
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
REL="""()=>{ const D=document.getElementById('device').getBoundingClientRect(), st=document.getElementById('studioScreen'); const out={cls:st.className, flous:[]};
      st.querySelectorAll('*').forEach(e=>{ const f=getComputedStyle(e).filter; if(f&&f.indexOf('blur')>=0){ const r=e.getBoundingClientRect(); if(r.width>4) out.flous.push([e.id||e.className, f, Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)]); } });
      const m=document.getElementById('murPhrase'); if(m){ const r=m.getBoundingClientRect(); out.phrase=[Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height), getComputedStyle(m).display, getComputedStyle(m).opacity, m.textContent.slice(0,30)]; } return JSON.stringify(out); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now()}));}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){} document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(6000)
    d=pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
    pg.touchscreen.tap(d['x']+75,d['y']+620); pg.wait_for_timeout(1500)
    print('après toucher des tons', pg.evaluate(REL))
    pg.screenshot(path='scratchpad/v140/studio1.png',clip={'x':d['x'],'y':d['y'],'width':390,'height':844})
    pg.touchscreen.tap(d['x']+250,d['y']+640); pg.wait_for_timeout(1200)
    print('après toucher du panneau', pg.evaluate(REL))
    pg.screenshot(path='scratchpad/v140/studio2.png',clip={'x':d['x'],'y':d['y'],'width':390,'height':844})
    b.close()
