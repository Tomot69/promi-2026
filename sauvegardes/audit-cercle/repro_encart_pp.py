# REPRO : l'encart du mur de la PAGE + ouvre-t-il le Cercle par-dessus ? 6 fois par thème, app actuelle contre app d'avant le lot.
# Chemin exact de verif_integration (clic souris au point de l'encart, 80 % de sa largeur), avec le nom de ce que le doigt touche.
import os
from playwright.sync_api import sync_playwright
OUTILS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verif_integration.py'), encoding='utf-8').read().split('OUTILS = r"""')[1].split('"""')[0]
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch()
    for nom, url in (('actuelle', 'http://127.0.0.1:8752/app.html'), ('avant le lot', 'http://127.0.0.1:8752/sauvegardes/app-avant-seuil-pilule.html')):
        for th in ('light', 'dark'):
            res = []
            ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
            pg.goto(url); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS)
            for k in range(12):
                pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
                pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
                pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar')
                if pt: pg.mouse.click(pt['x'], pt['y'])
                pg.wait_for_timeout(1800)
                pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart')
                pg.evaluate("()=>{ window.__enc=document.querySelector('#createSheet .s2-encart'); window.__vu=[]; if(!window.__mdw){ window.__mdw=1;"
                            " ['mousedown','mouseup','click'].forEach(t=>window.addEventListener(t, ev=>{ const x=ev.target; window.__vu.push(t+':'+(x&&x.closest&&x.closest('.s2-encart')?'encart':(x&&(x.id||String(x.className).split(' ')[0])))); }, true)); } }")
                if pt: pg.mouse.click(pt['x'], pt['y'])
                pg.wait_for_timeout(1000); e = pg.evaluate("()=>window.__V.etat()")
                diag = pg.evaluate("()=>({detache: window.__enc ? !window.__enc.isConnected : 'pas d encart', vu: window.__vu.join(' ')})")
                bon = e['ps_show'] and e['dessus'] and e['pp_peauf']
                res.append('✓' if bon else '✗(%s · détaché %s · %s)' % (pt and pt['recoit'], diag['detache'], diag['vu']))
                pg.evaluate("()=>{ try{ window._cercleDessus && document.getElementById('plusScreen').classList.remove('show','cercle-dessus'); }catch(e){} }")
            print('%-13s %-5s %s' % (nom, th, ' '.join(res)))
            ctx.close()
    br.close()
