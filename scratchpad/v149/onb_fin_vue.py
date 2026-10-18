# C-153 : à « Promi planté ! » et au compte, où est le mot-marque ? (capture + état)
import io, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL='http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True); pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); saisie(pg); pg.wait_for_timeout(600); trace(pg, cdp); pg.wait_for_timeout(5600)
    E = "()=>{ const v=document.getElementById('onbV'), mm=v&&v.querySelector('.onbv-mm'); if(!mm) return null; const c=getComputedStyle(mm), r=mm.getBoundingClientRect(); const ch=[]; let e=mm; while(e&&e!==document.body){ const s=getComputedStyle(e); ch.push((e.id||e.className)+':'+s.display+'/'+s.visibility+'/'+s.opacity); e=e.parentElement; } return {r:[r.left,r.top,r.width,r.height], vis:mm.style.visibility, tr:mm.style.transform, ch:ch.slice(0,4)}; }"
    print(pg.evaluate(E)); pg.screenshot(path='scratchpad/v149/onb_fin.png')
    toucher(cdp, pg, 195, 260); pg.wait_for_timeout(3500); print(pg.evaluate(E))
    for _ in range(3): toucher(cdp, pg, 195, 260); pg.wait_for_timeout(3500)
    print(pg.evaluate(E)); pg.screenshot(path='scratchpad/v149/onb_compte.png'); b.close()
