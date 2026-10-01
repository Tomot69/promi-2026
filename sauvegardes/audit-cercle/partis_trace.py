# LE TRAIT ENTIER, VRAIMENT TRACÉ : on fait le geste sur la zone de tracé d'une Nuée (mode complet 0 → 390), puis on capture.
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True).new_page()
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
        try: pg.evaluate("()=>{ const n=document.getElementById('nName'); if(n){ n.value='Les voisins'; n.dispatchEvent(new Event('input',{bubbles:true})); } }")
        except Exception: pass
        z = pg.evaluate("()=>{ const c=document.getElementById('planterCvN'); const r=c.getBoundingClientRect(); return {x:r.left, y:r.top, w:r.width, h:r.height}; }")
        # le geste : de gauche à droite, en suivant la bande du trait (le peintre suit x, pas la précision en y)
        y = z['y'] + z['h'] * 0.52
        pg.mouse.move(z['x'] + 6, y); pg.mouse.down()
        for i in range(1, 41): pg.mouse.move(z['x'] + 6 + (z['w'] - 12) * i / 40.0, y + (8 if i % 2 else -8)); pg.wait_for_timeout(12)
        pg.mouse.up(); pg.wait_for_timeout(900)
        etat = pg.evaluate("()=>({ecran:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(','), zone:(()=>{const c=document.getElementById('planterCvN'); if(!c) return null; const r=c.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)];})()})")
        print(th, 'après le geste :', etat)
        if etat['zone'] and etat['zone'][0] > 20:
            t = pg.evaluate("""()=>{ const c=document.getElementById('planterCvN'), w=document.querySelector('#createSheet .pp-trace');
                const r=c.getBoundingClientRect(), rw=w&&w.checkVisibility()?w.getBoundingClientRect():null; return {x:r.left, y:r.top, w:r.width, h:(rw?rw.top-8:r.bottom)-r.top}; }""")
            pg.screenshot(path=os.path.join(OUT, '%s_trait_trace.png' % th), clip={'x': t['x'], 'y': t['y'], 'width': t['w'], 'height': max(60, t['h'])})
        else:
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_apres_geste.png' % th))
        pg.context.close()
    br.close()
