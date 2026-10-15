# §11 C-123 — le fond de l'onboarding en mouvement : une image toutes les 120 ms, à l'arrivée et à chaque passage d'étape
import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
import io as _io
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True"))
URL = 'http://127.0.0.1:8752/' + (sys.argv[1] if len(sys.argv) > 1 else 'app.html')
def film(pg, nom, n=14, pas=120):
    ims = []
    for i in range(n):
        ims.append(Image.open(_io.BytesIO(pg.screenshot())).convert('RGB').resize((130, 281))); pg.wait_for_timeout(pas)
    P = Image.new('RGB', (n * 134, 281), 'white')
    for i, im in enumerate(ims): P.paste(im, (i * 134, 0))
    P.save('scratchpad/v146/onbfilm-%s.png' % nom)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True); pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(URL); pg.wait_for_timeout(1200); film(pg, '0-arrivee', 16, 250)
    prenom(pg, cdp); pg.keyboard.press('Enter'); film(pg, '1-vers-parole'); saisie(pg); film(pg, '2-vers-trait', 10)
    trace(pg, cdp); pg.wait_for_timeout(1500); film(pg, '3-vers-fin', 18, 90)
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height*0.36];}"); toucher(cdp, pg, d[0], d[1]); film(pg, '4-vers-compte', 10)
    b.close()
