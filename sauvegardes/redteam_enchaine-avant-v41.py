#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_enchaine.py — LE CONTRÔLE QUI ENCHAÎNE.

Chaque juge repart d'un état propre : il ferme tout, il ouvre UN écran, il mesure. Les
résidus vivent exactement là où personne ne regarde — entre deux écrans. On enchaîne donc
deux écrans, et on compare le second à LUI-MÊME ouvert proprement.

Un enchaînement est bon quand les trois sont vraies :
  1 · MÊMES CLASSES   le second écran ne porte aucune classe qui vienne du premier
  2 · MÊMES MOTS      rien n'est peint qui ne l'était pas quand on l'ouvre seul
  3 · RIEN DE PERDU   rien ne DISPARAÎT non plus (le mot-marque, le mot de trace…)

Usage :  python3 redteam_enchaine.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-56s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-56s KO  %s' % (nom, detail))


EMPREINTE = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const mots=[];
  document.querySelectorAll('body *').forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.3) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const t=(e.textContent||'').trim().replace(/\s+/g,' '); if(!t) return;
    const r=e.getBoundingClientRect(); if(r.width<5||r.height<5) return;
    const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
    if(x<-2||x>392||y<-2||y>846) return;
    mots.push(t.slice(0,30));});
  /* ⚠ ON NE COMPARE QUE LES ÉCRANS QUI SONT À L'ÉCRAN. Un poster fermé garde ses classes
     de nature (`dp-promi f-encours`) : elles ne peignent rien tant qu'il n'a pas `show`, et
     les comparer faisait crier le contrôle sur du vide. Ce qui compte, c'est ce qu'un
     écran VISIBLE porte. */
  const cls={};
  ['createSheet','detailPoster','indexSheet','feedView','device'].forEach(id=>{
    const h=document.getElementById(id);
    if(h && id!=='device'){ const c=getComputedStyle(h);
      const montre = h.classList.contains('show')||h.classList.contains('in');
      if(!montre || c.display==='none' || parseFloat(c.opacity)<0.05) return; }
    /* `gsN` est une graine de geste, tirée au hasard à chaque ouverture : la comparer n'a
       aucun sens. Tout le reste est comparé. */
    const e=document.getElementById(id);
    if(e) cls[id]=(e.className||'').split(' ').filter(Boolean).filter(c=>!/^gs\d+$/.test(c)).sort().join(' ');});
  return {mots:[...new Set(mots)], cls:cls};}"""

SCENES = {
  'toile':   "()=>{if(window.closeAll)closeAll();setView('toile');}",
  'pp_promi':"()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();"
             "setTimeout(()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();},600);}",
  'pp_chiche':"()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();"
             "setTimeout(()=>{const t=[...document.querySelectorAll('#createSheet .tile')][1];if(t)t.click();},600);}",
  'pp_peauf':"()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();"
             "setTimeout(()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();"
             "setTimeout(()=>{const x=document.querySelector('#createSheet #csBotBar,#createSheet .cbb-lab');if(x)x.click();},600);},600);}",
  'fiche':   "()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req&&p.status==='encours')[0].id);}",
  'fiche2':  "()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req&&p.status==='rate')[0].id);}",
  'fiche_peauf':"()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);"
             "setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();},900);}",
  'index':   "()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}",
  'fil':     "()=>{if(window.closeAll)closeAll();setView('fil');}",
}

# les enchaînements qui comptent : ceux qu'un utilisateur fait vraiment
CHAINES = [
    ('pp_peauf',    'pp_chiche'),   # j'ouvre Peaufiner, je change de nature
    ('pp_peauf',    'pp_promi'),
    ('fiche_peauf', 'fiche2'),      # j'ouvre Peaufiner, j'ouvre une autre fiche
    ('fiche_peauf', 'pp_promi'),
    ('index',       'fiche'),
    ('fil',         'fiche'),
    ('fiche',       'index'),
    ('pp_chiche',   'fiche'),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    def joue(cle, ms=2100):
        pg.evaluate(SCENES[cle]); pg.wait_for_timeout(ms)

    # la RÉFÉRENCE de chaque écran : ouvert seul, depuis la Toile
    ref = {}
    for cle in set([c for _, c in CHAINES]):
        joue('toile'); joue(cle)
        ref[cle] = pg.evaluate(EMPREINTE)

    for avant, apres in CHAINES:
        nom = '%s → %s' % (avant, apres)
        joue('toile'); joue(avant); joue(apres)
        e = pg.evaluate(EMPREINTE); r = ref[apres]
        sales = [k for k in e['cls'] if e['cls'][k] != r['cls'].get(k)]
        t('%s · mêmes classes' % nom, not sales,
          ' | '.join('%s : « %s » au lieu de « %s »' % (k, e['cls'][k], r['cls'].get(k)) for k in sales)[:150])
        neufs = [m for m in e['mots'] if m not in r['mots']]
        t('%s · rien en trop' % nom, not neufs, 'en trop : ' + ' · '.join(neufs[:6]))
        perdus = [m for m in r['mots'] if m not in e['mots']]
        t('%s · rien de perdu' % nom, not perdus, 'perdu : ' + ' · '.join(perdus[:6]))

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko:
    print('\nCE QUI NE MARCHE PAS :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
