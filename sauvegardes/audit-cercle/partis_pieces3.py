# Le TRAIT ENTIER (zone de tracé d'une Nuée, mode complet) rogné au-dessus des mots ; et les ANNEAUX découpés un par un.
import json, os
from PIL import Image
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()")
        for i in range(15):
            pg.wait_for_timeout(200)
            if pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-choix')"): break
        for e in range(5):
            pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')].find(x=>x.dataset.kind==='nuee'); var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(800)
            if pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('pp-choix')"): break
        pg.wait_for_timeout(900)
        m = pg.evaluate("""()=>{ const c=document.getElementById('planterCvN'), t=document.querySelector('#createSheet .pp-trace');
            const r=c.getBoundingClientRect(), rt=t?t.getBoundingClientRect():null; return {x:r.left, y:r.top, w:r.width, h:(rt?rt.top-8:r.bottom)-r.top}; }""")
        pg.screenshot(path=os.path.join(OUT, '%s_trait_entier.png' % th), clip={'x': m['x'], 'y': m['y'], 'width': m['w'], 'height': m['h']})
        print(th, 'trait entier :', round(m['w'] / 2), 'x', round(m['h'] / 2))
        pg.context.close()
    br.close()
# les anneaux, découpés d'après les cotes relevées (pieces2.json)
P = json.load(open(os.path.join(OUT, 'pieces2.json')))
for th in ('dark', 'light'):
    a = P['%s · encours' % th]['anneaux']; bo = a['boite']
    im = Image.open(os.path.join(OUT, '%s_anneaux_encours.png' % th)); k = im.width / bo[2]
    for ring in a['anneaux']:
        if not ring['vis']: continue
        nom = (ring['p'] or 'toi').lower()
        x0 = max(0, (ring['r'][0] - bo[0] - 8) * k); x1 = min(im.width, (ring['r'][0] - bo[0] + ring['r'][2] + 8) * k)
        y0 = max(0, (ring['r'][1] - bo[1] - 4) * k); y1 = min(im.height, (ring['r'][1] - bo[1] + ring['r'][3] + 30) * k)
        im.crop((int(x0), int(y0), int(x1), int(y1))).save(os.path.join(OUT, '%s_anneau_%s.png' % (th, nom)))
        print(th, 'anneau', nom, '→', int(x1 - x0), 'x', int(y1 - y0))
