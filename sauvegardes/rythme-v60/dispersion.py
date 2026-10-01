# Dispersion d'un monde : N arrivées/départs par le moteur, dans la même page.
import sys
from playwright.sync_api import sync_playwright
M=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 5
src=open('redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]; LIT=src.split('LIT = r"""')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme(m);}",M); pg.wait_for_timeout(3000)
    for k in range(N):
        pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='add'; const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }")
        pg.wait_for_timeout(3500); a=pg.evaluate(LIT); pg.wait_for_timeout(1500)
        pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='sync'; const P=window.eval('promises'); P.splice(P.findIndex(p=>p.id===97001),1); Toile.sync(P.filter(p=>!p.draft).map(p=>p.id)); }")
        pg.wait_for_timeout(3500); d=pg.evaluate(LIT); pg.evaluate("()=>{window.__arme=null;}"); pg.wait_for_timeout(1500)
        print(M, k, 'arrivée', a, 'départ', d, flush=True)
    b.close()
