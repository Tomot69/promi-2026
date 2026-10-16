import io, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL='http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); pg.wait_for_timeout(2500); parole(pg); saisie(pg); pg.wait_for_timeout(600); trace(pg, cdp)
    for t in (1500, 3000, 4500, 7000):
        pg.wait_for_timeout(1500 if t < 7000 else 2500)
        print(t, pg.evaluate("()=>{ const f=document.getElementById('onbFin'); if(!f) return null; const D=document.getElementById('device').getBoundingClientRect(), r=f.getBoundingClientRect(); return {top:f.style.top, tr:f.style.transform, h:f.offsetHeight, bas:r.bottom-D.top, place:f.getAttribute('data-place'), onbe:f.style.getPropertyValue('--onbe'), monte:f.getAttribute('data-monte')}; }"))
    pg.screenshot(path='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/6a98bbcb-8923-46df-9238-4fc6e5ddf3f2/scratchpad/onb/fin-mes.png')
    b.close()
