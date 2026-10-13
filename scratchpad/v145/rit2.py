import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
import numpy as np
GRAINE = "(function(){ var a=20261013; Math.random=function(){ a|=0; a=a+0x6D2B79F5|0; var t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; })();"
T = ['rendre le livre', 'écrire à Lou', 'arroser le ficus', 'courir dimanche']
def toile(pg):
    """la zone de Toile (y 105 → 700) de la capture, en tableau"""
    im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); k = im.height / 844.0
    return np.asarray(im.crop((0, int(105 * k), im.width, int(700 * k)))).astype(int)
res = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for nom, port in (('e1', 8761), ('v145', 8752)):
        ctx = B.contexte(b); ctx.add_init_script(GRAINE)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:%d/app.html' % port); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{ try{ Toile.setTheme('ritournelle'); }catch(e){} }"); pg.wait_for_timeout(1500)
        for i, t in enumerate(T):
            B.plante(pg, t); pg.wait_for_timeout(3000)
            g1 = pg.evaluate("()=>Toile_graines()"); a1 = toile(pg); pg.wait_for_timeout(3000); g2 = pg.evaluate("()=>Toile_graines()"); a2 = toile(pg)
            res[(nom, i + 1)] = (g2, a2)
            print(nom, i + 1, 'graines', g2, '· même version, 3 s plus tard :', int((np.abs(a1 - a2).max(axis=2) > 8).sum()), 'px', flush=True)
        ctx.close()
    b.close()
for n in (1, 2, 3, 4):
    d = np.abs(res[('e1', n)][1] - res[('v145', n)][1]).max(axis=2)
    print('%d parole(s) : E1 contre v145 : %d px au-delà de 8 niveaux ; graines identiques : %s' % (n, int((d > 8).sum()), res[('e1', n)][0] == res[('v145', n)][0]))
