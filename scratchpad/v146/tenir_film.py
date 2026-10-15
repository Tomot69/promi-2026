# §14 — l'instant « tenir » en images : une parole plantée, sa fiche, le trait tracé au doigt, une image toutes les 100 ms
import sys, io as _io; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'; TH = sys.argv[2] if len(sys.argv) > 2 else 'light'; NOM = sys.argv[3] if len(sys.argv) > 3 else 'tenir'
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null; }"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b, sombre=(TH == 'dark')); pg = ouvre(ctx, F)
    plante(pg, 'rendre le livre'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2500)
    z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380)
    ims = []
    for i in range(30): ims.append(Image.open(_io.BytesIO(pg.screenshot())).convert("RGB").resize((130, 281))); pg.wait_for_timeout(40)
    P = Image.new('RGB', (10 * 134, 3 * 285), 'white')
    for i, im in enumerate(ims): P.paste(im, ((i % 10) * 134, (i // 10) * 285))
    P.save('scratchpad/v146/%s-%s.png' % (NOM, TH)); print(pg.evaluate("()=>promises[promises.length-1].status"))
    b.close()
