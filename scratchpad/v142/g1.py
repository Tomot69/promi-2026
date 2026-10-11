import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image
import io as _io, time
with sync_playwright() as p:
    b=p.webkit.launch()
    for sombre in (False,True):
        ctx=contexte(b,sombre=sombre); pg=ouvre(ctx)
        for t in ['boire un verre','appeler Mamie','courir dimanche']: plante(pg,t)
        pg.wait_for_timeout(1500)
        for quoi in ('studio','plus'):
            pg.evaluate("(q)=>{ window.__g0=performance.now(); _guide.montre(q); }",quoi); L=[]
            for cible in (60,600,1200,1900):
                while pg.evaluate("()=>performance.now()-window.__g0")<cible: pg.wait_for_timeout(15)
                L.append((pg.evaluate("()=>Math.round(performance.now()-window.__g0)"), Image.open(_io.BytesIO(capture(pg))).convert('RGB').resize((390,844))))
            print(quoi, [t for t,_ in L], pg.evaluate("()=>{const c=document.getElementById(document.getElementById('guide').getAttribute('data-guide')==='studio'?'studioBtn':'createBtn'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [Math.round(r.width/k*10)/10, Math.round(r.height/k*10)/10, c.style.transform, JSON.stringify(_guide.etat().trou)]}"))
            W=Image.new('RGB',(400*4,844),'white')
            for i,(t,im) in enumerate(L): W.paste(im,(i*400,0))
            W.save('scratchpad/v142/g1-%s-%s.png'%(quoi,'s' if sombre else 'c'))
            pg.evaluate("()=>{ const g=document.getElementById('guide'); if(g) g.remove(); _guide.finir(); }"); pg.wait_for_timeout(800)
        ctx.close()
    b.close()
