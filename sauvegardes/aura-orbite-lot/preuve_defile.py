# Les deux contrôles réécrits pour la colonne qui défile, PROUVÉS contre de vrais défauts (CLAUDE §7) :
# `DEBORD` (rien ne sort de l'appareil, sauf dans une colonne déclarée qui tient et rogne) et
# `PROTEGE` (défilé jusqu'au bout, rien du cadre au-dessus du plateau). Le code testé est CELUI DU JUGE,
# importé, jamais recopié. Chaque sonde est posée sur une page fraîche.
#   python3 preuve_defile.py URL
import sys, importlib.util, os
from playwright.sync_api import sync_playwright
APP = '/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'   # le projet (le script vit hors de lui)
sp = importlib.util.spec_from_file_location('juge_aura', os.path.join(APP, 'releve-aura.py'))
J = importlib.util.module_from_spec(sp); sp.loader.exec_module(J)
URL = sys.argv[1]

SONDES = [
    ('telle quelle', None, 'passe'),
    ('le cadre ne se déclare plus (data-defile retiré)',
     "()=>document.getElementById('auCadre').removeAttribute('data-defile')", 'DEBORD'),
    ('le cadre ne rogne plus (overflow visible)',
     "()=>{const s=document.createElement('style');s.textContent='#device #auraScreen.au2 .au-cadre{overflow:visible!important}';document.head.appendChild(s);}", 'DEBORD'),
    ('un bloc sort par le CÔTÉ, dans la colonne',
     "()=>{const d=document.createElement('div');d.style.cssText='position:absolute;left:300px;top:500px;width:150px;height:20px;background:red';document.getElementById('auCadre').appendChild(d);}", 'DEBORD'),
    ('le cadre défile SANS rogner sous le plateau (clip-path retiré)',
     "()=>{const s=document.createElement('style');s.textContent='#device #auraScreen.au2 .au-cadre{clip-path:none!important}';document.head.appendChild(s);}", 'PROTEGE'),
]
ok = True
with sync_playwright() as p:
    b = p.chromium.launch()
    print('%-62s %-8s %-8s %s' % ('', 'DEBORD', 'PROTEGE', 'verdict'))
    for nom, js, attendu in SONDES:
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>12)"): break
        pg.wait_for_timeout(500)
        pg.evaluate(J.POSE_MOT, 0); pg.wait_for_timeout(300)      # la phrase de deux lignes : la colonne la plus longue
        if js: pg.evaluate(js); pg.wait_for_timeout(300)
        # la sonde s'applique-t-elle VRAIMENT ? on mesure le nœud avant d'accuser le contrôle (§7)
        et = pg.evaluate("()=>{const c=document.getElementById('auCadre'), s=getComputedStyle(c); return 'défile %s · overflowY %s · clip %s · déclaré %s'.replace('%s',c.scrollHeight>c.clientHeight+1).replace('%s',s.overflowY).replace('%s',s.clipPath).replace('%s',c.hasAttribute('data-defile'));}")
        d = pg.evaluate(J.DEBORD); pr = pg.evaluate(J.PROTEGE)
        prises = {'DEBORD': bool(d), 'PROTEGE': bool(pr['fautes'])}
        if attendu == 'passe': bon = not prises['DEBORD'] and not prises['PROTEGE']
        else: bon = prises[attendu]
        ok &= bon
        print('%-62s %-8s %-8s %s' % (nom, 'PRIS' if prises['DEBORD'] else '—', 'PRIS' if prises['PROTEGE'] else '—',
              ('✅ ' if bon else '❌ ') + ('passe' if attendu == 'passe' else 'défaut %s' % ('pris' if bon else 'NON PRIS — contrat éteint'))))
        print('      état obtenu :', et)
        if not bon: print('      DEBORD', d[:3], '· PROTEGE', pr)
        pg.close()
    b.close()
print('\n%s' % ('✅  les deux contrôles réécrits mordent' if ok else '❌  un contrôle ne mord pas'))
sys.exit(0 if ok else 1)
