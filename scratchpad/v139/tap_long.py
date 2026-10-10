# une image longue (900 ms) entre l'appui et le lever : le toucher ouvre-t-il la fiche ? (Chromium, CDP, heures explicites)
import sys,time
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000); cdp=ctx.new_cdp_session(pg)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle'); document.getElementById(\"toileCv\").addEventListener(\"pointerdown\",function(){ if(!window.__bloque) return; var t=performance.now(); while(performance.now()-t<900){} });}"); pg.wait_for_timeout(3500)
    dv=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}"); n=0
    for bl in (False,True):
        for (x,y) in ((195,300),(100,420),(290,520)):
            pg.evaluate("(b)=>{window.__bloque=b}",bl); t=time.time()
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':dv[0]+x,'y':dv[1]+y}],'timestamp':t})
            cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[],'timestamp':t+0.08}); pg.wait_for_timeout(1800)
            e=pg.evaluate("()=>{const dp=document.getElementById('detailPoster'); const r=!!(dp&&dp.classList.contains('show')); try{closeAll()}catch(e){}; return r}"); pg.wait_for_timeout(600)
            print('image longue' if bl else 'sans', (x,y), 'fiche ouverte' if e else 'RIEN')
    b.close()
