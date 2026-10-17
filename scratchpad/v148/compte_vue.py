import io, sys
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
URL = 'http://127.0.0.1:8752/' + F
PROBE = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const L=Toile_lecture(); const g=L.graines.find(x=>x.kind!=='gray'); const y=g?g.y*L.vue.s+L.vue.oy:null;
  const cv=document.getElementById('toileCv'); const r=cv.getBoundingClientRect(); const hit=y!=null?document.elementsFromPoint(D.left+195*k, D.top+(y+(r.top-D.top)/k)*k).slice(0,4).map(e=>e.id||String(e.className).slice(0,24)):null;
  return {y:y, toileTop:(r.top-D.top)/k, hit:hit, vois:(Toile.voisinesEtat?Toile.voisinesEtat().length:null)}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); pg.wait_for_timeout(2500); parole(pg); saisie(pg); pg.wait_for_timeout(600)
    trace(pg, cdp); pg.wait_for_timeout(5200); d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
    print('fin', pg.evaluate(PROBE))
    for i in range(4):
        toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 120 * d[2]); pg.wait_for_timeout(4500)
    pg.wait_for_timeout(1500); print('compte', pg.evaluate(PROBE)); pg.screenshot(path='scratchpad/v148/compte_%s.png' % F.split('.')[0])
    b.close()
