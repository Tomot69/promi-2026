# Départ scripté contre départ réel : la séquence image par image (instant, bloc qui bouge le plus).
import sys
from playwright.sync_api import sync_playwright
M=sys.argv[1] if len(sys.argv)>1 else 'gravure'
src=open('../../redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]
SEQ=r"""()=>{ const W=window; W.__fin=true; const T0=W.__T0; return W.__R.filter(r=>r[0]>=T0).map(r=>[Math.round(r[0]-T0), +r[1].toFixed(1)]); }"""
PL="()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme(m);}",M); pg.wait_for_timeout(3000)
    for cond in ['script','reel']:
        pg.evaluate(ENREG); pg.evaluate(PL); pg.wait_for_timeout(3500); pg.evaluate("()=>{window.__fin=true;}")
        if cond=='reel':
            pg.evaluate("()=>openDetail(97001)"); pg.wait_for_timeout(1800); pg.evaluate("()=>window._v16SupprimerPromi(cur)"); pg.wait_for_timeout(800)
            pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='sync';}")
            pg.mouse.click(*pg.evaluate("()=>{const r=document.querySelector('#v16Conf .v16-oui').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}"))
        else:
            pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='sync'; const P=window.eval('promises'); P.splice(P.findIndex(p=>p.id===97001),1); Toile.sync(P.filter(p=>!p.draft).map(p=>p.id));}")
        pg.wait_for_timeout(2500); s=pg.evaluate(SEQ); pg.evaluate("()=>{window.__arme=null;}")
        print(cond, [x for x in s if x[0]<900])
        if cond=='reel': pg.evaluate("()=>closeAll()")
        pg.wait_for_timeout(1500)
    b.close()
