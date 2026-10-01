# SONDE : le mur de la fiche est-il là, dans les conditions EXACTES de verif_integration (contexte tactile, gratuit, fiche 126) ?
# App actuelle contre app d'avant ce lot, deux passages chacune : régression du lot, ou course de l'instrument ?
from playwright.sync_api import sync_playwright
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ETAT = """()=>{ const dp=document.getElementById('detailPoster'); const L=dp.querySelector('.s2-liste');
  return {show:dp.classList.contains('show'), ouv:dp.classList.contains('s2-ouv'), liste:!!L, regs:L?L.querySelectorAll(':scope > .s2-reg').length:0,
          cercle:!!dp.querySelector('.s2-cercle'), cercleDans:L?!!L.querySelector('.s2-cercle'):false, briques:!!(window._s2Briques&&window._s2Briques.cercle),
          seuil:window._seuilPilule||null, erreurs:(window.__err||[]).slice(0,3)}; }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for nom, url in (('actuelle a543', 'http://127.0.0.1:8752/app.html'), ('avant le lot 53aae647', 'http://127.0.0.1:8752/sauvegardes/app-avant-seuil-pilule.html')):
        for passage in (1, 2):
            ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
            err = []; pg.on('pageerror', lambda e: err.append(str(e)[:160]))
            pg.goto(url); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
            pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>openDetail(126)"); pg.wait_for_timeout(1400)
            pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}")
            for t in (300, 1700, 4000):
                pg.wait_for_timeout(t if t == 300 else t - (300 if t == 1700 else 1700))
                print('%-22s passage %d · +%4d ms  %s' % (nom, passage, t, pg.evaluate(ETAT)))
            if err: print('   erreurs JS :', err[:3])
            ctx.close()
    br.close()
