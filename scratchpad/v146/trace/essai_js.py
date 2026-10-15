# essai du module : états à mi-tracé, dernière image du canevas contre le texte statique (WebKit, 390 × 844, échelle 3)
import sys, io; sys.path.insert(0, '../../..')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
URL = 'http://127.0.0.1:8752/scratchpad/v146/trace/essai.html'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); err = []; pg.on('pageerror', lambda e: err.append(str(e))); pg.on('console', lambda m: err.append(m.text) if m.type == 'error' else None)
    pg.goto(URL); pg.wait_for_timeout(1200)
    pg.screenshot(path='essai-statique.png')
    r = pg.evaluate("""async()=>{ window.C={}; for(const id of ['t','p','g']){ C[id]=TraceLettres.trace(document.getElementById(id), null, {manuel:true}); await C[id].pret; }
      return Object.keys(C).map(k=>[k, C[k].duree, C[k].glyphes.length, C[k].glyphes.filter(g=>!g.variante).map(g=>g.car).join(''), C[k].glyphes.filter(g=>g.exception).map(g=>g.car).join('')]); }""")
    print(r, err)
    for f in (0.0, 0.31, 0.62, 0.999, 1.0):
        pg.evaluate("f=>{ for(const k in C) C[k].va(f); }", f); pg.wait_for_timeout(150); pg.screenshot(path='essai-%03d.png' % int(f * 100))
        print(f, pg.evaluate("()=>Object.keys(C).map(k=>JSON.stringify(C[k].etat())+' '+getComputedStyle(document.getElementById(k)).clipPath.slice(0,60))"))
    m = pg.evaluate("()=>{const m=TraceLettres.mesures.prep.slice().sort((a,b)=>a-b); return [m.length, m[m.length>>1], m[m.length-1]]}"); print('préparation (n, médiane, max ms)', m)
    a = np.asarray(Image.open('essai-statique.png').convert('RGB')).astype(int)
    for nom in ('essai-099.png', 'essai-100.png'):
        c = np.asarray(Image.open(nom).convert('RGB')).astype(int); d = np.abs(a - c).max(2); print(nom, 'contre statique : ≠0', int((d > 0).sum()), '>8', int((d > 8).sum()), 'max', int(d.max()))
    pg.evaluate("()=>{ for(const k in C) C[k].finir(); }"); pg.wait_for_timeout(150); pg.screenshot(path='essai-fin.png')
    f = np.asarray(Image.open('essai-fin.png').convert('RGB')).astype(int); print('texte posé contre statique :', int((np.abs(a - f).sum(2) > 0).sum()), pg.evaluate("()=>[document.querySelectorAll('canvas').length, document.getElementById('t').getAttribute('style')]"))
    # un tracé en temps réel, à x0,25 : le temps par image
    r = pg.evaluate("""async()=>{ TraceLettres.mesures.image.length=0; TraceLettres.mesures.prep.length=0; const c=TraceLettres.trace(document.getElementById('p'), null, {vitesse:0.25}); const t0=performance.now(); await c.fin;
       const im=TraceLettres.mesures.image.slice().sort((a,b)=>a-b), pr=TraceLettres.mesures.prep.slice().sort((a,b)=>a-b), q=(m,p)=>m[Math.min(m.length-1,Math.floor(m.length*p))];
       return {duree:performance.now()-t0, prevue:c.duree, images:im.length, image_p50:q(im,.5), image_p95:q(im,.95), image_max:im[im.length-1], prep_p50:q(pr,.5), prep_max:pr[pr.length-1]}; }""")
    print('temps réel ×0,25 :', r)
    print(err); b.close()
