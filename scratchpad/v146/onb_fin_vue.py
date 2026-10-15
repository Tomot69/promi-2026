# §11 — le message de fin : au repos, puis après le toucher ; clair et sombre ; et l'étape de la parole
import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True"))
URL = 'http://127.0.0.1:8752/' + (sys.argv[2] if len(sys.argv) > 2 else 'app.html'); TH = sys.argv[1] if len(sys.argv) > 1 else 'light'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True)
    if TH == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); parole(pg); pg.screenshot(path='scratchpad/v146/onbt-%s-1-parole.png' % TH); saisie(pg); pg.screenshot(path='scratchpad/v146/onbt-%s-2-trait.png' % TH)
    trace(pg, cdp); pg.wait_for_timeout(4200); pg.screenshot(path='scratchpad/v146/onbt-%s-3-fin.png' % TH)
    print(pg.evaluate("()=>{ const f=document.getElementById('onbFin'); const D=document.getElementById('device').getBoundingClientRect(); const r=f.getBoundingClientRect(); return {top:r.top-D.top, bas:r.bottom-D.top, dalles:f.getAttribute('data-place'), e:getComputedStyle(f).getPropertyValue('--onbe')}; }"))
    toucher(cdp, pg, 195, 300); pg.wait_for_timeout(6000); pg.screenshot(path='scratchpad/v146/onbt-%s-4-reste.png' % TH)
    print(pg.evaluate("()=>document.getElementById('onbV').getAttribute('data-onb-reste')"))
    b.close()
