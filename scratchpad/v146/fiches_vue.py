import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
nom = sys.argv[1] if len(sys.argv) > 1 else 'p8'
ims = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
        ids = pg.evaluate("()=>({promi:(promises.find(p=>!p.chiche&&p.status!=='tenu'&&p.who==='moi')||{}).id, chiche:(promises.find(p=>p.chiche)||{}).id, autre:(promises.find(p=>!p.chiche&&p.who!=='moi')||{}).id})")
        L = []
        for k in ('promi', 'chiche', 'autre'):
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("i=>openDetail(i)", ids[k]); pg.wait_for_timeout(2600); L.append(Image.open(io.BytesIO(B.capture(pg))).convert('RGB'))
        # Peaufiner d'une fiche
        B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1500); L.append(Image.open(io.BytesIO(B.capture(pg))).convert('RGB'))
        # la page +
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600); B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600); L.append(Image.open(io.BytesIO(B.capture(pg))).convert('RGB'))
        ims[sombre] = L; ctx.close()
    b.close()
n = len(ims[False]); w, h = ims[False][0].size
P = Image.new('RGB', (n * (w + 30), 2 * h + 30), (90, 90, 90))
for r, s in enumerate((False, True)):
    for i, im in enumerate(ims[s]): P.paste(im, (i * (w + 30), r * (h + 30)))
P.resize((P.width // 4, P.height // 4)).save('scratchpad/v146/%s-fiches.png' % nom)
import numpy as np
for i in range(n):
    a = np.asarray(ims[False][i]).astype(int); c = np.asarray(ims[True][i]).astype(int); d = (np.abs(a - c).sum(axis=2) > 24).mean() * 100
    print(['fiche Promi', 'fiche Chiche', 'fiche à quelqu\'un', 'Peaufiner', 'page +'][i], ': %.1f %% de pixels différents entre clair et sombre' % d)
