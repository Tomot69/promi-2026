# les vidéos ralenties du lot v146 (au quart de la vitesse réelle) — Chromium, 390 × 844, l'enregistrement de Playwright (webm)
import sys, os, shutil, glob; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True"))
B = 'http://127.0.0.1:8752/'
QUOI = sys.argv[1:] or ['guide', 'maree', 'onboarding', 'trace']
def ctx_v(b, nom, init=None):
    d = 'scratchpad/v146/vid-' + nom; shutil.rmtree(d, ignore_errors=True)
    c = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True, record_video_dir=d, record_video_size={'width': 390, 'height': 844})
    if init: c.add_init_script(init)
    return c, d
def garde(c, d, nom):
    c.close(); f = glob.glob(d + '/*.webm')
    if f: shutil.move(f[0], 'planche-v146/videos/%s.webm' % nom); print(nom, 'ok')
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    if 'guide' in QUOI:
        c, d = ctx_v(b, 'guide'); pg = c.new_page(); pg.goto(B + 'promi-guide-variantes.html?flaques=1'); pg.wait_for_timeout(26000); garde(c, d, 'C-094-guide-flaques-quart')
    if 'maree' in QUOI:
        c, d = ctx_v(b, 'maree', "try{if(!sessionStorage.getItem('a')){sessionStorage.setItem('a','1');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');}}catch(e){}")
        pg = c.new_page(); pg.goto(B + 'app.html?mareeLent=4'); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} const q=promises.filter(x=>!x.draft&&x.status!=='tenu'&&!x.nuee&&(!x.from||/^moi$/i.test(x.from)))[0]; closeAll(); openDetail(q.id); }"); pg.wait_for_timeout(2600)
        z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        cdp = c.new_cdp_session(pg); y = z[1] + z[3] * 0.45
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': 200, 'y': y}]}); pg.wait_for_timeout(400)
        for i in range(1, 16): cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': 200 + 160 * i / 15, 'y': y}]}); pg.wait_for_timeout(40)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(12500); garde(c, d, 'C-118-tenir-maree-quart')
    if 'onboarding' in QUOI:
        c, d = ctx_v(b, 'onb'); pg = c.new_page(); pg.goto(B + 'app.html?onbLent=4'); pg.wait_for_timeout(6500); cdp = c.new_cdp_session(pg)
        prenom(pg, cdp); parole(pg); saisie(pg); trace(pg, cdp); pg.wait_for_timeout(13000)
        toucher(cdp, pg, 195, 300); pg.wait_for_timeout(6500); garde(c, d, 'C-123-onboarding-voisines-quart')
    if 'trace' in QUOI:
        c, d = ctx_v(b, 'trace'); pg = c.new_page(); pg.goto(B + 'promi-trace-lettres.html'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ const x=document.querySelector('[data-vitesse=\"0.25\"]'); if(x) x.click(); }"); pg.wait_for_timeout(300)
        r = pg.evaluate("()=>{ const t=[...document.querySelectorAll('*')].find(x=>x.children.length===0&&/toucher pour tracer/i.test(x.textContent)); const f=t?(t.closest('[role=button],button,.cadre,figure,section,div')||t):null; if(!f) return null; f.scrollIntoView({block:'center'}); const q=(f.parentElement||f).getBoundingClientRect(); return [q.left+q.width/2, q.top+q.height/2]; }")
        if r: pg.mouse.click(r[0], r[1])
        pg.wait_for_timeout(24000); garde(c, d, 'C-125-trace-lettres-quart')
    b.close()
