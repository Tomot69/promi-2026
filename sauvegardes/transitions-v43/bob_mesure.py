# Bobinette : une arrivée et un départ. Par image : combien d'arcs se retissent ; sur toute la transition : combien d'arcs
# DIFFÉRENTS ont été retissés, combien l'ont été PLUS D'UNE FOIS (le scintillement), et leur distance à la dalle (en pas de trame).
import sys, statistics as st
from playwright.sync_api import sync_playwright
JS=r"""async (a)=>{ const L=[]; const t0=performance.now();
  if(a.op==='plante'){ const id=9000+Math.floor(Math.random()*999); promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); Toile.addPromi(id); }
  if(a.op==='retire'){ promises.pop(); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id)); }
  await new Promise(r=>{ function f(){ const A=window._bobAnim||{n:0,cles:[],dist:[]}; L.push([Math.round(performance.now()-t0),A.n,A.cles,A.dist]); if(performance.now()-t0<a.dur) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  return L; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('bobinette');}")
    pg.wait_for_timeout(3500)
    for op in ['plante','retire']:
        L=pg.evaluate(JS,{'op':op,'dur':2800})
        vus={}; prec=set()
        for t,n,cles,dist in L:
            cur=set(cles)
            for k in cur-prec: vus[k]=vus.get(k,0)+1
            prec=cur
        D=[d for _,_,_,ds in L for d in ds]
        print(op,'| arcs retissés',len(vus),'| plusieurs fois',sum(1 for v in vus.values() if v>1),
              '| distance médiane',st.median(D) if D else '-','max',max(D) if D else '-',
              '| par image (max)',max(n for _,n,_,_ in L), '| profil', [(t,n) for t,n,_,_ in L][::8])
        pg.wait_for_timeout(1500)
    b.close()
