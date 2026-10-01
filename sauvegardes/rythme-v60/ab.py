# A/B : la même arrivée et le même départ (moteur, Toile semée, vrai GPU), dans N pages fraîches par version.
# Donne la fin VISIBLE (pixels) et la fin de la BOUCLE du moteur (Toile_state().running).
import sys, statistics as st
from playwright.sync_api import sync_playwright
MONDES=sys.argv[1].split(','); VERS=sys.argv[2].split(','); N=int(sys.argv[3]); WK='--webkit' in sys.argv
src=open('redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]; LIT=src.split('LIT = r"""')[1].split('"""')[0]
SEME="let s=777; Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; "
BOUCLE=r"""()=>{ const W=window; W.__b=null; const t0=performance.now(); (function f(){ if(performance.now()-t0>6000) return; if(!Toile_state().running && performance.now()-t0>50){ W.__b=Math.round(performance.now()-t0); return; } requestAnimationFrame(f); })(); }"""
with sync_playwright() as p:
    b=p.webkit.launch() if WK else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    R={}
    for m in MONDES:
        for v in VERS:
            for k in range(N):
                pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
                pg.goto('http://127.0.0.1:8752/'+v); pg.wait_for_timeout(9000)
                pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
                pg.evaluate("m=>{ "+SEME+"Toile.setTheme(m); }", m); pg.wait_for_timeout(3000)
                pg.evaluate(ENREG); pg.evaluate(BOUCLE); pg.evaluate("()=>{window.__arme='add'; const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }")
                pg.wait_for_timeout(4000); a=pg.evaluate(LIT); ba=pg.evaluate("()=>window.__b"); pg.wait_for_timeout(1000)
                pg.evaluate(ENREG); pg.evaluate(BOUCLE); pg.evaluate("()=>{window.__arme='sync'; const P=window.eval('promises'); P.splice(P.findIndex(p=>p.id===97001),1); Toile.sync(P.filter(p=>!p.draft).map(p=>p.id)); }")
                pg.wait_for_timeout(4000); d=pg.evaluate(LIT); bd=pg.evaluate("()=>window.__b")
                R.setdefault((m,v),[]).append((a['duree'],ba,d['duree'],bd,a['images'],d['images']))
                print('%-11s %-20s arrivée vue %5d boucle %5s im %3d · départ vue %5d boucle %5s im %3d' % (m, v, a['duree'], ba, a['images'], d['duree'], bd, d['images']), flush=True)
                pg.close()
    b.close()
    print('— médianes')
    for (m,v),L in R.items(): print('%-9s %-20s' % (m,v), [int(st.median([x[i] for x in L if x[i] is not None])) for i in range(6)])
