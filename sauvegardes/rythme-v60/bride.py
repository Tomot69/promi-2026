# Un mouvement dépend-il de la charge ? Même arrivée/départ (moteur, Toile semée), processeur bridé ×1 puis ×N (CDP).
import sys
from playwright.sync_api import sync_playwright
MONDES=sys.argv[1].split(','); BR=[float(x) for x in (sys.argv[2] if len(sys.argv)>2 else '1,3').split(',')]
APP=next((a.split('=')[1] for a in sys.argv if a.startswith('--app=')),'app.html')
src=open('redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]; LIT=src.split('LIT = r"""')[1].split('"""')[0]
SEME="let s=777; Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; "
with sync_playwright() as p:
    b=p.webkit.launch() if '--webkit' in sys.argv else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    for m in MONDES:
        for br in BR:
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
            pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(9000)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
            pg.evaluate("m=>{ "+SEME+"Toile.setTheme(m); }", m); pg.wait_for_timeout(3000)
            cdp.send('Emulation.setCPUThrottlingRate',{'rate':br}); pg.wait_for_timeout(1000)
            pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='add'; const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }")
            pg.wait_for_timeout(int(4000*max(1,br/1.5))); a=pg.evaluate(LIT); pg.wait_for_timeout(1500)
            pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='sync'; const P=window.eval('promises'); P.splice(P.findIndex(p=>p.id===97001),1); Toile.sync(P.filter(p=>!p.draft).map(p=>p.id)); }")
            pg.wait_for_timeout(int(4000*max(1,br/1.5))); d=pg.evaluate(LIT)
            print('%-11s ×%g  arrivée %5d ms %3d im · départ %5d ms %3d im' % (m, br, a['duree'], a['images'], d['duree'], d['images']), flush=True)
            ctx.close()
    b.close()
