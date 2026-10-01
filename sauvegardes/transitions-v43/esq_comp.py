# La composition d'Esquille à n paroles : éclats de promesse, éclats de matière, tailles. python3 esq_comp.py [n ...]
import sys, statistics as st
from playwright.sync_api import sync_playwright
NS=[int(a) for a in sys.argv[1:]] or [3,9,20,40]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("async()=>{ Toile.setTheme('esquille'); while(promises.filter(p=>!p.draft).length<48){ const q=Object.assign({},promises[0]); q.id=5000+promises.length; q.title='essai '+promises.length; promises.push(q);} await new Promise(r=>setTimeout(r,500)); }")
    for n in NS:
        c=pg.evaluate("async(n)=>{ const ids=promises.filter(p=>!p.draft).map(p=>p.id).slice(0,n); Toile.sync(ids); await new Promise(r=>setTimeout(r,3000)); Toile_liven(); await new Promise(r=>setTimeout(r,300)); return window._esqComp; }", n)
        ap,am=c['airesPromesse'],c['airesMatiere']
        print('%2d paroles → graines promesse %d · éclats de promesse %d · matière %d · aire promesse méd %d (min %d) · matière méd %d (max %d, min %d) · rapport méd %.1f · plaque couverte par les promesses %.0f %%' % (
            n, c['promesses'], c['eclatsPromesse'], c['matiere'], st.median(ap), min(ap), st.median(am) if am else 0, max(am) if am else 0, min(am) if am else 0, st.median(ap)/max(1,st.median(am) if am else 1), 100*sum(ap)/c['plaque']))
    b.close()
