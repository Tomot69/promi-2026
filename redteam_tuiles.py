#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_tuiles.py — L'ÉCRAN DES CHOIX, AU DOIGT : la tuile touchée ouvre SA nature.

Né le 13 sept. 2026 (AUDIT-ACCUEIL § 2, CLAUDE §8) : au doigt, « Un Chiche » ouvrait un Promi, et après une Nuée la tuile
Promi laissait `data-kind="nuee"`. À la souris tout était juste — et toutes les batteries jouaient à la souris.

Chaque tuile est touchée au VRAI DOIGT (CDP `Input.dispatchTouchEvent`, contexte tactile), dans des ordres qui changent
la tuile d'avant, avec trois doigts : immobile, qui tremble de 6 px, qui glisse de 10 px en diagonale (au-delà, ni Chromium ni iOS ne font un toucher — mesuré : aucun clic à 20 px). Après le toucher :
  · `#createSheet[data-kind]` = la nature touchée
  · la feuille porte `pp-<nature>` et plus `pp-choix`
  · le verbe de la phrase est celui de la nature (Promi « Je me promets » · Chiche « Chiche » · Nuée « Je lance une Nuée »)
Et la souris reste juste (témoin). Deux thèmes.

Preuve (§7) : `APP_TUILES=http://127.0.0.1:8752/sauvegardes/app-avant-lot-chiche-doigt.html python3 redteam_tuiles.py`
doit ROUGIR.
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_TUILES', "http://127.0.0.1:8752/app.html")
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []
VERBE = {'promi': 'Je me promets', 'chiche': 'Chiche', 'nuee': 'Je lance un Cercle'}
ORDRES = [['chiche', 'nuee', 'promi', 'chiche'], ['nuee', 'chiche', 'nuee', 'promi']]
DOIGTS = {'immobile': (0, 0), 'tremble 6 px': (6, 3), 'glisse 10 px': (7, 7)}


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-58s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-58s KO  %s' % (nom, detail))


ETAT = r"""()=>{const s=document.getElementById('createSheet');
  const v=s.classList.contains('pp-nuee')?document.querySelector('#nueePhrase .ph-b, #nueePhrase [data-np=verbe], #nueePhrase'):document.querySelector('#csPhrase .ph-b');
  return {kind:s.dataset.kind, cls:[...s.classList].filter(c=>/^pp/.test(c)), verbe:v?(v.innerText||'').trim().split('\n')[0]:''};}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        for mode in ['doigt', 'souris']:
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=(mode == 'doigt'))
            pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(600)
            cdp = ctx.new_cdp_session(pg)
            doigts = DOIGTS if mode == 'doigt' else {'clic': (0, 0)}
            for dnom, (dx, dy) in doigts.items():
                for ordre in ORDRES:
                    for k, nat in enumerate(ordre):
                        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(600)
                        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1300)
                        bb = pg.locator('#createSheet .tile[data-kind=%s]' % nat).first.bounding_box()
                        x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
                        if mode == 'doigt':
                            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
                            if dx or dy:
                                for i in (1, 2, 3):
                                    cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x + dx * i / 3, 'y': y + dy * i / 3}]})
                            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
                        else:
                            pg.mouse.click(x, y)
                        pg.wait_for_timeout(1500)
                        e = pg.evaluate(ETAT)
                        bon = e['kind'] == nat and ('pp-' + nat) in e['cls'] and 'pp-choix' not in e['cls'] and e['verbe'].startswith(VERBE[nat])
                        t('[%s · %s · %s] %s après %s' % ('clair' if th == 'light' else 'sombre', mode, dnom, nat, '→'.join(ordre[:k]) or 'rien'),
                          bon, 'data-kind %s · %s · verbe « %s »' % (e['kind'], ' '.join(e['cls']), e['verbe'][:24]))
            ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
