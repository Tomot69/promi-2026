# Les trois dalles payantes, prises SUR L'ÉCRAN QUI VEND lui-même (ce sont littéralement les dalles du produit,
# rendues par Toile.dalleTrame dans les mondes Sillons / Gravure / Terrazzo). 98x98 css → 196 px à DPR 2.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
        pg.wait_for_timeout(2600)
        info = pg.evaluate("""()=>({ ouvert: document.getElementById('plusScreen').classList.contains('show'),
            sans: !!window._vendSans, noms: [...document.querySelectorAll('#plCadre .plv-nom')].map(e=>e.textContent.trim()),
            dal: [...document.querySelectorAll('#plCadre .plv-dal')].map(e=>{const r=e.getBoundingClientRect();return {w:r.width,h:r.height};}) })""")
        R[th] = info; print(th, info['ouvert'], info['sans'], info['noms'], info['dal'])
        for k, nom in enumerate(info['noms'] or []):
            el = pg.locator('#plCadre .plv-dal').nth(k)
            el.screenshot(path=os.path.join(OUT, '%s_dalle_%s.png' % (th, nom.lower().replace('é','e'))))
        if info['ouvert']: pg.locator('#plCadre').screenshot(path=os.path.join(OUT, '%s_vend_actuel.png' % th))
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'dalles.json'), 'w'), ensure_ascii=False, indent=1)
