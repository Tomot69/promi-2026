# Les bulles de Halin qui SAUTENT : à chaque image, la liste publiée (_halBulles) ; une bulle qui apparaît ou disparaît
# à plus de 40 % de sa taille de repos, ou dont la taille bondit de plus de 40 % d'une image à l'autre, est un saut.
import sys
from playwright.sync_api import sync_playwright
JS=r"""async (a)=>{ const L=[]; const t0=performance.now();
  if(a.op==='plante'){ const id=9000+Math.floor(Math.random()*999); promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); Toile.addPromi(id); }
  if(a.op==='retire'){ const P=promises.filter(p=>!p.draft); Toile.sync(P.slice(1).map(p=>p.id)); }
  await new Promise(r=>{ function f(){ L.push([Math.round(performance.now()-t0),(window._halBulles||[]).map(b=>[b.k,+b.t.toFixed(2)])]); if(performance.now()-t0<a.dur) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  return L; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('halin');}")
    pg.wait_for_timeout(4000)
    rest=pg.evaluate("()=>{const m={}; (window._halBulles||[]).forEach(b=>m[b.k]=b.t); return m;}")
    tot=0
    for op in ['plante','retire','plante']:
        L=pg.evaluate(JS,{'op':op,'dur':2600}); sauts=[]
        pg.wait_for_timeout(1500); apres=pg.evaluate("()=>{const m={}; (window._halBulles||[]).forEach(b=>m[b.k]=b.t); return m;}")
        for i in range(1,len(L)):
            a=dict(L[i-1][1]); b2=dict(L[i][1])
            for k in set(a)|set(b2):
                ref=max(rest.get(k,0),apres.get(k,0)) or max(a.get(k,0),b2.get(k,0)) or 1
                x,y=a.get(k,0),b2.get(k,0)
                if abs(y-x)>0.4*ref and ref>0.3: sauts.append((L[i][0],k[:18],x,y))
        rest=apres; tot+=len(sauts); print(op,'images',len(L),'bulles au repos',len(rest),'sauts',len(sauts),sauts[:8])
    print('TOTAL SAUTS',tot)
    b.close()
