# Le MOUVEMENT DU CHAMP de Madrure, image par image (sa composition, §7 — pas les pixels) : écart moyen |Δφ| (en bandes)
# sur 600 points fixes de la Toile, entre deux images. Un saut = une image > 3 × la médiane de ses voisines.
# python3 champ_mad.py [--webkit] [--depart]
import sys, statistics as st
from playwright.sync_api import sync_playwright
WK='--webkit' in sys.argv; DEP='--depart' in sys.argv
JS=r"""async (a)=>{ Toile.setTheme('madrure'); await new Promise(r=>setTimeout(r,3000)); const cv=document.getElementById('toileCv');
 const pts=[]; for(let i=0;i<20;i++) for(let j=0;j<30;j++) pts.push([ (i+0.5)/20*390, (j+0.5)/30*800 ]);
 function lit(){ const C=cv.__madC; if(!C||!C.r||!C.r.phi) return null; return pts.map(p=>C.r.phi(p[0],p[1])); }
 Toile_liven(); await new Promise(r=>setTimeout(r,1500)); const src0=JSON.stringify(window._madGPU); let prev=lit(); const out=[]; const t0=performance.now();
 if(a.dep){ const ids=promises.filter(p=>!p.draft).map(p=>p.id); Toile.sync(ids.slice(1)); } else { promises.push(Object.assign({},promises[0],{id:9999,title:'essai de plantation',nuee:null})); Toile.addPromi(9999); }
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; const cur=lit(); let s=0; if(cur&&prev) for(let i=0;i<cur.length;i++) s+=Math.abs(cur[i]-prev[i]);
   out.push([Math.round(e), +(s/pts.length).toFixed(3)]); prev=cur; if(e<3200) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return {out:out, gpu:window._madGPU||null, src0:src0}; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(args=[] if WK else ['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    R=pg.evaluate(JS,{'dep':DEP}); b.close()
d=R['out']; v=[q for _,q in d]; sauts=[]
for i in range(1,len(v)):
    vo=[v[j] for j in range(max(1,i-3),min(len(v),i+4)) if j!=i]; med=st.median(vo) if vo else 0
    if v[i]>0.05 and v[i]>3*max(med,0.005): sauts.append((d[i][0],v[i],round(med,3)))
fin=max([t for t,q in d if q>0.002] or [0])
print('avant:', R['src0']); print('madrure', 'départ' if DEP else 'arrivée', 'webkit' if WK else 'chromium-gpu', '| GPU', R['gpu'] is not None, '| images', len(d), '| max Δφ', max(v), '| fin', fin, 'ms | sauts', sauts)
print('   ', ' '.join('%d:%s'%(t,q) for t,q in d[::4]))
