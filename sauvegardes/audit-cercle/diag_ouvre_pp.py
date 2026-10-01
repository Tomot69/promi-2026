# DIAG : où s'arrête l'ouverture de la page + dans verif_64 ? Une capture et les classes après chaque étape.
import os
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bandeau')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ETAT = """()=>{ const cs=document.getElementById('createSheet'); const t=[...cs.querySelectorAll('.tile')]; const b=document.getElementById('csBotBar');
  return {classes:cs.className, tuiles:t.map(x=>[x.dataset.kind, x.checkVisibility(), x.classList.contains('on')]), barre:b?[b.checkVisibility(), Math.round(b.getBoundingClientRect().height)]:null,
          enh:!!(cs.querySelector(':scope > .enh')||{checkVisibility:()=>false}).checkVisibility(), kind:cs.getAttribute('data-kind')}; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("(t)=>setTheme(t)", 'dark'); pg.wait_for_timeout(300)
    pg.evaluate(BASE); pg.wait_for_timeout(200)
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
    print('1 création :', pg.evaluate(ETAT)); pg.locator('#device').screenshot(path=os.path.join(OUT, 'diag_1.png'))
    print('   la tuile 0 et ce que le script clique :', pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); return [t&&t.dataset.kind, t&&t.textContent.trim().slice(0,40), b&&(b.className+' « '+b.textContent.trim().slice(0,30)+' »')]; }"))
    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
    print('2 tuile    :', pg.evaluate(ETAT)); pg.locator('#device').screenshot(path=os.path.join(OUT, 'diag_2.png'))
    br.close()
