# REPRO : depuis le mur de la PAGE +, encart → écran qui vend par-dessus → « Prendre l'année ». L'achat a-t-il lieu ?
# verif_integration l'a raté une fois (clair) sur l'app de l'écran refait. Deux causes possibles, qu'on sépare :
#   · l'encart est rebâti sous le doigt (chantier 70) → l'écran qui vend ne s'ouvre pas, l'achat n'a pas de bouton ;
#   · le bouton, DÉPLACÉ dans le cadre par ce lot, ne répond pas.
# Pour chaque essai : l'écran qui vend était-il ouvert AVANT le toucher d'achat ? l'encart a-t-il été détaché ? l'achat a-t-il eu
# lieu ? App du lot contre app d'avant le lot, 10 essais par thème (une page neuve par essai : un achat rend abonné).
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
OUTILS = open(os.path.join(D, 'verif_integration.py'), encoding='utf-8').read().split('OUTILS = r"""')[1].split('"""')[0]
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch()
    for nom, url in (('écran refait 8b3c8cb1', 'http://127.0.0.1:8752/app.html'), ('avant le lot a543d1e1', 'http://127.0.0.1:8752/sauvegardes/app-avant-vend-planche.html')):
        for th in ('light', 'dark'):
            res, notes = [], []
            for k in range(10):
                ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
                for essai in range(2):
                    try: pg.goto(url, timeout=90000); break
                    except Exception: pass
                pg.wait_for_timeout(6800)
                pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
                pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS)
                pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
                pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
                pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar')
                if pt: pg.mouse.click(pt['x'], pt['y'])
                pg.wait_for_timeout(1800)
                pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart'); pg.wait_for_timeout(250); pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart')
                if not pt: res.append('·'); ctx.close(); continue       # le Peaufiner de la page + ne s'est pas ouvert : pas un essai
                pg.evaluate("()=>{ window.__enc=document.querySelector('#createSheet .s2-encart'); }")
                pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(1000)
                avant = pg.evaluate("()=>({ouvert: document.getElementById('plusScreen').classList.contains('show'), detache: window.__enc ? !window.__enc.isConnected : null})")
                pg.evaluate("()=>{const s=document.getElementById('plusScreen'); s.scrollTop=s.scrollHeight;}"); pg.wait_for_timeout(400)
                pb = pg.evaluate("(s)=>window.__V.point(s)", '#buyYear'); pg.wait_for_timeout(250); pb = pg.evaluate("(s)=>window.__V.point(s)", '#buyYear')
                if pb: pg.mouse.click(pb['x'], pb['y'])
                pg.wait_for_timeout(1300); e = pg.evaluate("()=>window.__V.etat()")
                bon = e['premium'] and not e['ps_show'] and e['pp_peauf']
                res.append('✓' if bon else '✗')
                if not bon: notes.append({'écran qui vend ouvert avant l’achat': avant['ouvert'], 'encart détaché': avant['detache'], 'le doigt sur « Prendre l’année »': pb and pb['recoit'], 'abonné': e['premium'], 'couches': e['couches']})
                ctx.close()
            print('%-22s %-5s %s   (%d ✓ / %d essais)' % (nom, th, ''.join(res), res.count('✓'), len([r for r in res if r != '·'])))
            for n in notes: print('      raté :', n)
    br.close()
