import sys, json
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
REL="""()=>{ const D=document.getElementById('device').getBoundingClientRect(), st=document.getElementById('studioScreen'); const out={cls:st.className.replace('screen s-studio ',''), flous:[], murs:[]};
      st.querySelectorAll('*').forEach(e=>{ const f=getComputedStyle(e).filter; if(f&&f.indexOf('blur')>=0){ const r=e.getBoundingClientRect(); if(r.width>4) out.flous.push([e.id||e.className, Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)]); } });
      const m=document.getElementById('murPhrase'); if(m){ const r=m.getBoundingClientRect(); out.phrase=[Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height), getComputedStyle(m).display, m.className, m.textContent.slice(0,30)]; } return JSON.stringify(out); }"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now()}));}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500); cdp=ctx.new_cdp_session(pg)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){} document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(6000)
    d=pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
    def tap(x,y):
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':d['x']+x,'y':d['y']+y}]}); pg.wait_for_timeout(60); cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    def glisse():
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':d['x']+320,'y':d['y']+300}]})
        for i in range(1,11): pg.wait_for_timeout(16); cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':d['x']+320-i*24,'y':d['y']+300}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(1500)
    for k in range(12):
        glisse(); c=pg.evaluate("()=>document.getElementById('studioScreen').className")
        if 'world-locked' in c or 'stp-verrou' in c: break
    print(k, pg.evaluate(REL)); pg.wait_for_timeout(2500)
    pg.screenshot(path='scratchpad/v140/st-a.png',clip={'x':d['x'],'y':d['y'],'width':390,'height':844})
    n=0
    for (x,y,nom) in ((75,620,'tons'),(195,670,'libellés'),(120,724,'disques'),(195,782,'barrettes')):
        pg.wait_for_timeout(6500)   # la phrase d'avant s'efface
        pg.evaluate("()=>{ try{ var s=document.getElementById('cercleScreen'); if(s&&s.classList.contains('show')) closeAll(); }catch(e){} }")
        tap(x,y); pg.wait_for_timeout(700); n+=1
        print(nom, pg.evaluate(REL)); pg.screenshot(path='scratchpad/v140/st-%d.png'%n,clip={'x':d['x'],'y':d['y'],'width':390,'height':844})
    b.close()
