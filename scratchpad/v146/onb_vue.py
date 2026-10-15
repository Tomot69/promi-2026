# §11 — les étapes de l'onboarding, en clair et en sombre (capture de chaque étape + les boîtes des textes)
import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True"))
TH = sys.argv[1] if len(sys.argv) > 1 else 'light'; URL = 'http://127.0.0.1:8752/' + (sys.argv[2] if len(sys.argv) > 2 else 'app.html')
BOX = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const out={}; ['onbDit','onbPh','onbSous','onbTrace','onbFin','onbSuite'].forEach(i=>{ const e=document.getElementById(i); if(!e) return; const c=getComputedStyle(e); if(c.display==='none') return; const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); out[i]={b:[(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k].map(v=>Math.round(v)), fs:c.fontSize, col:c.color, f:c.fontFamily.split(',')[0]}; }); return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, color_scheme='dark' if TH == 'dark' else 'light')
    if TH == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    def cap(n): pg.screenshot(path='scratchpad/v146/onb-%s-%s.png' % (TH, n)); print(n, pg.evaluate(BOX))
    cap('1-prenom'); prenom(pg, cdp); cap('2-prenom-saisi'); parole(pg); cap('3-parole'); saisie(pg); cap('4-trait'); trace(pg, cdp)
    for t in (300, 800, 1500, 2600, 6000): pg.wait_for_timeout(t - (0 if t == 300 else 0)); 
    cap('5-fin'); b.close()
