import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx, 10); pg=B.ouvre(ctx, 'app.html', attente=7000)
    print('n', pg.evaluate("()=>promises.filter(p=>!p.draft).length"), 'prenom', pg.evaluate("()=>localStorage.getItem('promi_prenom')"))
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.getElementById('settingsBtn').click(); }"); pg.wait_for_timeout(1500)
    print('reglages', pg.evaluate("()=>document.getElementById('settingsScreen').classList.contains('show')"))
    pg.evaluate("()=>{ const e=document.getElementById('replayOnb'); e.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(400)
    print(B.tap_sel(pg, '#replayOnb')); pg.wait_for_timeout(4200)
    print(pg.evaluate("()=>{ const o=document.getElementById('promiOnb'), v=document.getElementById('onbV'); return {onb:o&&o.className, v:!!v, ph:document.getElementById('onbPh')&&document.getElementById('onbPh').textContent, dit:document.getElementById('onbDit')&&document.getElementById('onbDit').textContent, trait:document.getElementById('onbTrait')&&document.getElementById('onbTrait').style.display}; }"))
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(4500)
    print(pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); return c?{disp:c.style.display, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee'), ph:document.getElementById('onbPh').textContent}:null; }"))
    pg.screenshot(path='scratchpad/v151/rejeu_dbg.png'); b.close()
