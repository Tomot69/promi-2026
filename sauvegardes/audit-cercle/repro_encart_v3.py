# REPRO v3 : le CLIC seul. Le Peaufiner de la page + est ouvert UNE fois (chemin vérifié par diag_pp.py), puis l'encart du mur
# est touché 20 fois dans la même page ; entre deux essais, le « par-dessus » est refermé. App actuelle contre app d'avant le lot.
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
OUTILS = open(os.path.join(D, 'verif_integration.py'), encoding='utf-8').read().split('OUTILS = r"""')[1].split('"""')[0]
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ESPION = """()=>{ if(window.__esp) return; window.__esp=1; window.__vu=[];
  ['mousedown','mouseup','click'].forEach(t=>window.addEventListener(t, ev=>{ const x=ev.target; window.__vu.push(t+':'+(x&&x.closest&&x.closest('.s2-encart')?'encart':(x&&(x.id||String(x.className).split(' ')[0])))); }, true)); }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for nom, url in (('actuelle', 'http://127.0.0.1:8752/app.html'), ('avant le lot', 'http://127.0.0.1:8752/sauvegardes/app-avant-seuil-pilule.html')):
        for th in ('light', 'dark'):
            ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
            pg.goto(url); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS); pg.evaluate(ESPION)
            pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
            pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
            pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar')
            if pt: pg.mouse.click(pt['x'], pt['y'])
            pg.wait_for_timeout(1800)
            res, rates = [], []
            for k in range(20):
                pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart')
                if not pt: res.append('·'); continue                      # encart introuvable : pas un essai de clic
                pg.evaluate("()=>{ window.__enc=document.querySelector('#createSheet .s2-encart'); window.__vu=[]; }")
                pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(700)
                e = pg.evaluate("()=>window.__V.etat()")
                bon = e['ps_show'] and e['dessus'] and e['pp_peauf']
                res.append('✓' if bon else '✗')
                if not bon: rates.append(pg.evaluate("()=>({detache: window.__enc ? !window.__enc.isConnected : null, vu: window.__vu.join(' ')})") | {'recoit': pt['recoit'], 'couches': e['couches']})
                pg.evaluate("()=>{ const p=document.getElementById('plusScreen'); p.classList.remove('show'); p.classList.remove('cercle-dessus'); }"); pg.wait_for_timeout(400)
            print('%-13s %-5s %s   (%d ✓ / %d essais)' % (nom, th, ''.join(res), res.count('✓'), len([r for r in res if r != '·'])))
            for r in rates[:4]: print('      raté :', r)
            ctx.close()
    br.close()
