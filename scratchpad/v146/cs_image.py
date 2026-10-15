import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
import numpy as np
from PIL import Image
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
def img(pg): return np.asarray(Image.open(io.BytesIO(B.capture(pg))).convert('RGB').resize((390, 844))).astype(int)[110:700]
def d(a, b): x = np.abs(a - b).sum(axis=2); return round(float((x > 12).mean()) * 100, 2), round(float(x.mean()), 2)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b)
    st = json.load(io.open('banc-etats/etat-5.json', encoding='utf-8')); st.pop('promi_theme', None)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
    pg = B.ouvre(ctx, F); pg.evaluate("()=>{ window._vivantOff=true; try{ setPremium(true); }catch(e){} }")
    for m in ('encre', 'touffe', 'mosaique', 'braille', 'ritournelle', 'chamade'):
        pg.evaluate("m=>Toile.setTheme(m)", m); pg.wait_for_timeout(2500)
        c1 = img(pg); pg.wait_for_timeout(700); c1b = img(pg)
        pg.evaluate("()=>window.setTheme('dark')"); pg.wait_for_timeout(1400); s1 = img(pg)
        pg.evaluate("()=>window.setTheme('light')"); pg.wait_for_timeout(1400); c2 = img(pg)
        pg.evaluate("()=>window.setTheme('dark')"); pg.wait_for_timeout(1400); s2 = img(pg)
        pg.evaluate("()=>window.setTheme('light')"); pg.wait_for_timeout(900)
        print('%-12s témoin clair/clair %s · clair avant/après un aller-retour %s · sombre/sombre %s' % (m, d(c1, c1b), d(c1, c2), d(s1, s2)), flush=True)
    b.close()
