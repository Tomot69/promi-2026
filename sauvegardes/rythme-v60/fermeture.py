# La fermeture d'une fiche fait-elle bouger la Toile, sans aucune parole qui part ?
import sys
from playwright.sync_api import sync_playwright
sys.argv=[sys.argv[0]]; exec(open('../../redteam_rythme.py').read().split('def centre')[0].split("ENREG = ")[0])
src=open('../../redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]
REC=r"""()=>{ const W=window; W.__fin=true; return W.__R.map(r=>[Math.round(r[0]-W.__R[0][0]), +r[1].toFixed(2)]); }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
    for m in ['gravure','sillons','terrazzo']:
        pg.evaluate("m=>Toile.setTheme(m)",m); pg.wait_for_timeout(3000)
        pg.evaluate("()=>{ openDetail(promises.filter(p=>!p.draft)[2].id); }"); pg.wait_for_timeout(2000)
        pg.evaluate(ENREG); pg.wait_for_timeout(300); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1500)
        R=pg.evaluate(REC); mv=[r for r in R if r[1]>0.5]
        print(m,'fermeture seule :', len(mv),'images qui bougent', mv[:3], mv[-2:])
    b.close()
