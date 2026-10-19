import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, stockage={'promi_prenom':'Camille'}); B.toile_pleine(ctx, 10); pg=B.ouvre(ctx, 'app.html', attente=7000)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.getElementById('settingsBtn').click(); }"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const e=document.getElementById('replayOnb'); e.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(400)
    B.tap_sel(pg, '#replayOnb'); pg.wait_for_timeout(4200)
    st="()=>{ const a=document.activeElement; return {ph:document.getElementById('onbPh').textContent.slice(0,40), dit:document.getElementById('onbDit').textContent, actif:a&&(a.id||a.tagName), trait:document.getElementById('onbTrait').style.display, inp:document.getElementById('onbIn').value}; }"
    print(pg.evaluate(st))
    print(B.tap_sel(pg, '#onbPh')); pg.wait_for_timeout(600); print(pg.evaluate(st))
    pg.keyboard.type('marcher une heure', delay=25); pg.wait_for_timeout(300); print(pg.evaluate(st)); pg.keyboard.press('Enter'); pg.wait_for_timeout(4500)
    print(pg.evaluate(st)); pg.screenshot(path='scratchpad/v151/rejeu_dbg2.png'); b.close()
