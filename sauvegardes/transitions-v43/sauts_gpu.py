# LA FORME DU DÉFAUT « ÇA SAUTE » : une AMPLITUDE (§7). Pour chaque image après le geste, écart moyen (niveaux 0-255,
# sur la Toile réduite à 1/4) avec l'image précédente, et l'heure de l'image. Un saut = une image dont l'écart dépasse
# 3 × la médiane de ses 6 voisines ET 1,5 niveau. La fin = la dernière image qui change encore (> 0,15).
# python3 sauts.py monde [--depart] [--webkit] [--duree=3500]
import sys, json, statistics as st
from playwright.sync_api import sync_playwright
M=[a for a in sys.argv[1:] if not a.startswith('--')][0]; WK='--webkit' in sys.argv; DEP='--depart' in sys.argv
DUR=int(([a.split('=')[1] for a in sys.argv if a.startswith('--duree=')] or ['3500'])[0])
JS=r"""async (a)=>{ Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,3000));
 const cv=document.getElementById('toileCv'); const w=Math.round(cv.width/4), h=Math.round(cv.height/4);
 const c=document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d',{willReadFrequently:true});
 function img(){ x.drawImage(cv,0,0,w,h); return x.getImageData(0,0,w,h).data; }
 let prev=img(); const out=[]; const t0=performance.now();
 if(a.dep){ const ids=promises.filter(p=>!p.draft).map(p=>p.id); Toile.sync(ids.slice(1)); } else Toile.addPromi(null);
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; const cur=img(); let s=0; for(let i=0;i<cur.length;i+=4) s+=Math.abs(cur[i]-prev[i])+Math.abs(cur[i+1]-prev[i+1])+Math.abs(cur[i+2]-prev[i+2]);
   out.push([Math.round(e), +(s/(cur.length/4*3)).toFixed(2)]); prev=cur; if(e<a.dur) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return {out:out, gpu:window._madGPU||null}; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(args=[] if WK else ['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    R=pg.evaluate(JS,{'m':M,'dur':DUR,'dep':DEP}); b.close(); d=R['out']; print('GPU', R['gpu'])
v=[q for _,q in d]; sauts=[]
for i in range(1,len(v)):
    vo=[v[j] for j in range(max(1,i-3),min(len(v),i+4)) if j!=i]
    med=st.median(vo) if vo else 0
    if v[i]>1.5 and v[i]>3*max(med,0.1): sauts.append((d[i][0],v[i],round(med,2)))
fin=max([t for t,q in d if q>0.15] or [0])
print(M,'départ' if DEP else 'arrivée','webkit' if WK else 'chromium','| images',len(d),'| max',max(v),'| fin du mouvement',fin,'ms | sauts',sauts)
print('   série', ' '.join('%d:%s'%(t,q) for t,q in d[50:110]))
