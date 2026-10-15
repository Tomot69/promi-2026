import sys, io, base64; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
def img(u): return Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGB')
def compare(a, b):
    a = a.resize((78, 169), Image.BOX); b = b.resize((78, 169), Image.BOX); d = ImageChops.difference(a, b); px = list(d.getdata())
    return round(sum(sum(p) for p in px) / (3.0 * len(px)), 1), round(100 * sum(1 for p in px if max(p) > 40) / float(len(px)), 1)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    for t in ('arroser le figuier', 'écrire à Lou', 'réparer le vélo'): plante(pg, t)
    pg.evaluate("()=>{ try{setPremium(true)}catch(e){} const f=Toile.renderTo; window.__rts=[]; Toile.renderTo=function(cv){ const r=f.apply(this,arguments); try{ window.__rts.push([performance.now()|0, cv.width, cv.height, cv.toDataURL('image/png')]); }catch(e){} return r; }; }")
    for m in ('touffe', 'encre', 'touffe'):
        pg.evaluate("(m)=>{ try{closeAll()}catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(4200)
        ecran = img(pg.evaluate("()=>document.getElementById('toileCv').toDataURL('image/png')"))
        pg.evaluate("()=>{ window.__rts=[]; }"); t0 = pg.evaluate("()=>performance.now()|0")
        tap_sel(pg, '#shareBtn'); pg.wait_for_timeout(3500)
        R = pg.evaluate("()=>window.__rts")
        print(m, '— rendus du moteur après le toucher sur Partager :', [(r[0] - t0, r[1], r[2], compare(ecran, img(r[3]))) for r in R])
        if R: img(R[0][3]).resize((316, 684)).save('scratchpad/v146/partage-%s-premier.png' % m); img(R[-1][3]).resize((316, 684)).save('scratchpad/v146/partage-%s-dernier.png' % m); ecran.resize((316, 684)).save('scratchpad/v146/partage-%s-ecran.png' % m)
        pg.evaluate("()=>{ try{ const s=document.getElementById('shareScreen'); const x=s&&s.querySelector('.closeb'); if(x) x.click(); }catch(e){} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
    b.close()
