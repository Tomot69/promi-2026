# Halin : la taille des bulles (en jours), au repos et pendant les mouvements — les plus grosses, et quand.
from playwright.sync_api import sync_playwright
JS=r"""async (a)=>{ const L=[]; const t0=performance.now();
  if(a.op==='plante'){ const id=9000+Math.floor(Math.random()*999); promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); Toile.addPromi(id); }
  if(a.op==='retire'){ promises.pop(); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id)); }
  await new Promise(r=>{ function f(){ (window._halBulles||[]).forEach(b=>L.push([Math.round(performance.now()-t0), b.a/(b.j*b.j), b.k, b.l/b.j, b.x, b.y])); if(performance.now()-t0<a.dur) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  return L; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('halin');}")
    pg.wait_for_timeout(3500)
    for op in ['repos','plante','retire','plante','retire']:
        L=pg.evaluate(JS,{'op':op,'dur':2600})
        v=sorted(x[1] for x in L)
        top=sorted(L,key=lambda x:-x[1])[:3]
        print(op,'| bulles-images',len(L),'| médiane %.2f'%v[len(v)//2] if v else '', '| max %.2f'%v[-1] if v else '', '| plus grosses (aire, longueur en jours)',[(x[0],round(x[1],2),round(x[3],2),int(x[4]),int(x[5])) for x in top])
        pg.wait_for_timeout(1200)
    b.close()
