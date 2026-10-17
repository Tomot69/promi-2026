import io, sys
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL = 'http://127.0.0.1:8752/app.html' + (sys.argv[1] if len(sys.argv) > 1 else '')
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True)
    pg = ctx.new_page(); err = []; pg.on('pageerror', lambda e: err.append(str(e)[:150])); pg.goto(URL); cdp = ctx.new_cdp_session(pg)
    ims = []
    def snap(n): ims.append((n, Image.open(io.BytesIO(pg.screenshot()))))
    for _ in range(80):
        pg.wait_for_timeout(50)
        if pg.evaluate("()=>!!document.querySelector('#onbV canvas.passage-flaques')"): break
    pg.wait_for_timeout(420); snap('arrivée')
    pg.wait_for_timeout(3500)
    prenom(pg, cdp); pg.wait_for_timeout(2500); parole(pg)
    pg.evaluate("()=>{ const i=document.getElementById('onbIn'); i.focus(); }"); pg.keyboard.type('m'); pg.wait_for_timeout(330); snap('trait')
    pg.keyboard.type('archer une heure', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
    trace(pg, cdp); pg.wait_for_timeout(960); snap('page part')
    pg.wait_for_timeout(5200); d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
    for i in range(3): toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(4500)
    toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(330); snap('compte')
    pg.wait_for_timeout(1800)
    pg.evaluate("()=>{ const t=document.querySelector('.onbv-compte .tard'); if(t) t.click(); }"); pg.wait_for_timeout(250); snap('compte part')
    pg.wait_for_timeout(700); snap('accueil')
    print('erreurs', err)
    w, h = ims[0][1].size; o = Image.new('RGB', (w * len(ims) + 20 * len(ims), h), (255, 255, 255))
    for i, (n, im) in enumerate(ims): o.paste(im, (i * (w + 20), 0))
    o = o.resize((o.width // 2, o.height // 2)); o.save('scratchpad/v148/onb_flaques.png'); print([n for n, _ in ims])
    b.close()
