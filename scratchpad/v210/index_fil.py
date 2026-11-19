"""v210 C-301 — l'Index contre le Fil, au pixel, dans la bande du haut (0 → 180 pt : l'encart, la recherche, le tri), hors titre.
python3 scratchpad/v210/index_fil.py [--fichier=] [--css=coquille.css]  (deux thèmes, échelles 1 et 0,79)"""
import sys, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image, ImageChops
F = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
CSS = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--css=')), None)
TIT = r"""()=>{ const dev=document.getElementById('device').getBoundingClientRect(); const s=document.querySelector('#indexSheet.show, #feedView.in, #feedView[style*=block]');
 const t=[...document.querySelectorAll('#indexSheet .enh-t, #feedView .enh-t')].filter(e=>e.getBoundingClientRect().width>0 && e.getBoundingClientRect().top<dev.top+dev.height*0.2);
 return t.map(e=>{const r=e.getBoundingClientRect(); return [r.left-dev.left, r.top-dev.top, r.right-dev.left, r.bottom-dev.top];}); }"""
ok = 0; tot = 0
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in ((430, 932), (330, 714)):
        for th in ('clair', 'sombre'):
            ctx = B.contexte(b, sombre=(th == 'sombre'), vw=vw, vh=vh); B.toile_pleine(ctx, 10)
            if CSS: ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent=%r;document.head.appendChild(s);});" % open(CSS).read())
            pg = B.ouvre(ctx, F); ims = {}; tits = []
            for nom, js in (('index', "()=>ouvrirIndex()"), ('fil', "()=>document.getElementById('filBtn').click()")):
                pg.evaluate("()=>{ try{closeAll();}catch(e){} }"); pg.wait_for_timeout(800); pg.evaluate(js); pg.wait_for_timeout(2800)
                tits += pg.evaluate(TIT)
                dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
                k = dev[2] / 390
                png = pg.screenshot(clip={'x': dev[0], 'y': dev[1], 'width': dev[2], 'height': 180 * k})
                ims[nom] = Image.open(io.BytesIO(png)).convert('RGB')
            a, c = ims['index'], ims['fil']; s = a.width / dev[2]
            d = ImageChops.difference(a, c).convert('L').point(lambda v: 255 if v > 24 else 0)
            from PIL import ImageDraw
            dr = ImageDraw.Draw(d)
            m = 2 * s; dr.rectangle([0, 0, d.width, m], fill=0); dr.rectangle([0, 0, m, d.height], fill=0); dr.rectangle([d.width - m, 0, d.width, d.height], fill=0)   # le bord de l'écran (2 pt) : la feuille de l'Index et la vue du Fil ne sont pas l'encart
            for x0, y0, x1, y1 in tits: dr.rectangle([x0 * s - 2, y0 * s - 2, x1 * s + 2, y1 * s + 2], fill=0)
            n = sum(1 for v in d.getdata() if v); part = n / (d.width * d.height) * 100
            tot += 1; bon = n == 0; ok += bon
            print('%s %dx%d %-6s  pixels différents hors titre : %d (%.3f %%)' % ('✅' if bon else '❌', vw, vh, th, n, part))
            if not bon: d.save('scratchpad/v210/index_fil-%d-%s.png' % (vw, th)); a.save('scratchpad/v210/if-index-%d-%s.png' % (vw, th)); c.save('scratchpad/v210/if-fil-%d-%s.png' % (vw, th))
            ctx.close()
    b.close()
print('  %d / %d' % (ok, tot))
