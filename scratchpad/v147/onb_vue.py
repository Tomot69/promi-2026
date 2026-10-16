"""captures de l'onboarding, page par page (pour regarder) : python3 scratchpad/v147/onb_vue.py DOSSIER [light|dark]"""
import io, sys, re
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; TH = sys.argv[2] if len(sys.argv) > 2 else 'light'
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL = 'http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True, color_scheme='dark' if TH == 'dark' else 'light')
    if TH == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto(URL)
    T = [400, 800, 1200, 1600, 2000, 2600, 3200, 4500, 6000]; prev = 0
    for t in T: pg.wait_for_timeout(t - prev); prev = t; pg.screenshot(path='%s/a-arrivee-%04d.png' % (OUT, t))
    cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); pg.wait_for_timeout(1500); pg.screenshot(path='%s/b-prenom-fait.png' % OUT)
    parole(pg); pg.wait_for_timeout(800); pg.screenshot(path='%s/c-parole.png' % OUT)
    saisie(pg); pg.wait_for_timeout(800); pg.screenshot(path='%s/d-trait.png' % OUT)
    trace(pg, cdp)
    for t in (400, 1200, 2000, 2800, 3600, 5000): pg.wait_for_timeout(400 if t == 400 else 800 if t < 3700 else 1400); pg.screenshot(path='%s/e-fin-%04d.png' % (OUT, t))
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
    toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(6000); pg.screenshot(path='%s/f-reste.png' % OUT)
    toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(1500); pg.screenshot(path='%s/g-compte.png' % OUT)
    pg.evaluate("()=>{ const t=document.querySelector('.onbv-compte .tard'); if(t) t.click(); }")
    prev = 0
    for t in (150, 400, 550, 700, 900, 1300, 2200, 3000, 3800, 5000): pg.wait_for_timeout(t - prev); prev = t; pg.screenshot(path='%s/h-sortie-%04d.png' % (OUT, t))
    print('erreurs', er[:3]); b.close()
