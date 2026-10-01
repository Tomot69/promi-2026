# DIAG : que montre la page + à chaque étape du chemin de verif_integration (création → tuile → barre Peaufiner) ?
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'diag_pp')
OUTILS = open(os.path.join(D, 'verif_integration.py'), encoding='utf-8').read().split('OUTILS = r"""')[1].split('"""')[0]
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ETAT = """()=>{ const cs=document.getElementById('createSheet'); const t=[...document.querySelectorAll('#createSheet .tile')];
  return {show:cs.classList.contains('show'), classes:cs.className.slice(0,120), tuiles:t.length, tuile0:t[0]?t[0].textContent.trim().slice(0,40):null,
          barre:(()=>{const b=document.getElementById('csBotBar'); if(!b) return null; const r=b.getBoundingClientRect(); return {vis:b.checkVisibility(), y:Math.round(r.top), h:Math.round(r.height)};})(),
          liste:!!cs.querySelector('.s2-liste'), encart:!!cs.querySelector('.s2-encart'), couches:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')}; }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
    err = []; pg.on('pageerror', lambda e: err.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('light')"); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS)
    pg.evaluate(BASE); pg.wait_for_timeout(200)
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
    print('1 création :', pg.evaluate(ETAT)); pg.locator('#device').screenshot(path=os.path.join(OUT, '1_creation.png'))
    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
    print('2 tuile    :', pg.evaluate(ETAT)); pg.locator('#device').screenshot(path=os.path.join(OUT, '2_tuile.png'))
    pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar')
    print('   point de la barre :', pt)
    if pt: pg.mouse.click(pt['x'], pt['y'])
    pg.wait_for_timeout(1800)
    print('3 barre    :', pg.evaluate(ETAT)); pg.locator('#device').screenshot(path=os.path.join(OUT, '3_barre.png'))
    if err: print('erreurs JS :', err[:3])
    br.close()
