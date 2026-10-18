# la fin de l'onboarding en WebKit (Safari) : les lignes de « Tout le monde promet… » et leur alignement
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, onb=False, dsf=2); pg = B.ouvre(ctx)
    pg.wait_for_timeout(1500)
    r = pg.evaluate("""()=>{ if(!window._onbDemo) {} const f=document.createElement('div'); return !!document.getElementById('onbV'); }""")
    print('onboarding présent', r)
    b.close()
