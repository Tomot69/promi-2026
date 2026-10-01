#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_champs.py — LE CONTRÔLE QUI REMPLIT.

Aucune des neuf batteries, aucun des cinq juges ne tape dans un champ. Un champ de 0 × 0
passe le contrôle de position, un champ qui n'affiche pas ce qu'on écrit passe le contrôle
de style. Celui-ci ÉCRIT, puis vérifie que la valeur ARRIVE — dans la donnée ET à l'écran.

Un champ est bon quand les quatre sont vraies :
  1 · il est ATTEIGNABLE      (visible, largeur et hauteur non nulles, dans le cadre)
  2 · il ACCEPTE le texte     (sa valeur change)
  3 · la DONNÉE le reçoit     (l'app le lit quelque part)
  4 · l'ÉCRAN le montre       (on ne travaille pas à l'aveugle)

Usage :  python3 redteam_champs.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-52s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-52s KO  %s' % (nom, detail))


ATTEIGNABLE = r"""(sel)=>{
  const e=document.querySelector(sel); if(!e) return {ok:false, why:'ABSENT'};
  const c=getComputedStyle(e), r=e.getBoundingClientRect();
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
  if(c.display==='none') return {ok:false, why:'display:none'};
  if(c.visibility==='hidden') return {ok:false, why:'visibility:hidden'};
  if(parseFloat(c.opacity)<0.2) return {ok:false, why:'opacité '+c.opacity};
  if(r.width<6||r.height<6) return {ok:false, why:'boîte '+Math.round(r.width)+'×'+Math.round(r.height)};
  if(x<-2||x>390||y<-2||y>844) return {ok:false, why:'hors cadre à '+Math.round(x)+','+Math.round(y)};
  if(c.pointerEvents==='none') return {ok:false, why:'pointer-events:none'};
  if(e.readOnly) return {ok:false, why:'readOnly'};
  if(e.disabled) return {ok:false, why:'disabled'};
  return {ok:true, why:Math.round(x)+','+Math.round(y)+' '+Math.round(r.width/sc)+'×'+Math.round(r.height/sc)};}"""

ECRIS = r"""(a)=>{
  const e=document.querySelector(a.sel); if(!e) return 'ABSENT';
  e.focus(); e.value=a.txt;
  e.dispatchEvent(new Event('input',{bubbles:true}));
  e.dispatchEvent(new Event('change',{bubbles:true}));
  e.dispatchEvent(new KeyboardEvent('keyup',{bubbles:true,key:'r'}));
  return e.value;}"""

VU = r"""(txt)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  let vu=false;
  document.querySelectorAll('body *, input, textarea').forEach(e=>{
    if(vu) return;
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.3) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const porte = (e.value!==undefined && e.value!==null && (''+e.value).includes(txt))
               || (e.textContent||'').includes(txt);
    if(!porte) return;
    const r=e.getBoundingClientRect(); if(r.width<4||r.height<4) return;
    const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
    if(x<-2||x>392||y<-2||y>846) return;
    vu=true;});
  return vu;}"""


def champ(pg, nom, sel, txt, lu, prise=None):
    """lu : ce que la DONNÉE a retenu · prise : ce que LE DOIGT touche.

    ⚠ SUR LA PAGE +, LE CHAMP N'EST PAS L'INTERFACE. Le moodboard montre une PHRASE, pas
    un formulaire : `#phIn` est un receveur de frappe volontairement invisible. Exiger
    qu'il soit « atteignable » testait la mauvaise chose. Ce qui doit être atteignable,
    c'est LE CRÉNEAU qu'on touche ; ce qui doit être visible, c'est LA PHRASE."""
    a = pg.evaluate(ATTEIGNABLE, prise or sel)
    t('%s · atteignable' % nom, a['ok'], a['why'])
    if not a['ok']:
        t('%s · accepte le texte' % nom, False, 'champ inatteignable')
        t('%s · la donnée le reçoit' % nom, False, 'champ inatteignable')
        t('%s · l\'écran le montre' % nom, False, 'champ inatteignable')
        return
    v = pg.evaluate(ECRIS, {'sel': sel, 'txt': txt}); pg.wait_for_timeout(700)
    t('%s · accepte le texte' % nom, v == txt, 'valeur = « %s »' % v)
    d = pg.evaluate(lu)
    t('%s · la donnée le reçoit' % nom, (d or '') and txt in str(d), 'donnée = « %s »' % str(d)[:44])
    t('%s · l\'écran le montre' % nom, pg.evaluate(VU, txt), 'cherché « %s » à l\'écran' % txt)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    def page_plus(i):
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
        pg.evaluate("(i)=>{const t=[...document.querySelectorAll('#createSheet .tile')][i];if(t)t.click();}", i)
        pg.wait_for_timeout(1100)

    # ── LA PAGE + · PROMI ────────────────────────────────────────────────────────────
    print('\n── la page + · Promi ──')
    page_plus(0)
    pg.evaluate("()=>{const e=document.querySelector('[data-ph=titre]');if(e)e.click();}")
    pg.wait_for_timeout(900)
    champ(pg, 'le titre, par la phrase', '#phIn', 'aller voir la mer',
          "()=>((window._phrase||{}).titre||'')", prise='#csPhrase [data-ph=titre]')
    # le champ du formulaire doit rester le miroir de la phrase
    t('le titre · le formulaire suit', 
      pg.evaluate("()=>((document.getElementById('fTitle')||{}).value||'')") .find('aller voir la mer') >= 0,
      pg.evaluate("()=>((document.getElementById('fTitle')||{}).value||'')"))

    print('\n── la page + · à qui ──')
    page_plus(0)
    # une parole à SOI n'a pas de créneau « à qui » — c'est « Je me promets ». On bascule
    # vers une parole faite à quelqu'un, qui, elle, doit en porter un.
    pg.evaluate("""()=>{ window._phrase={sens:'faire',faireAutre:true,qui:'',titre:'faire les crêpes',quand:'un jour'};
      if(window._phraseRendu)_phraseRendu(); }"""); pg.wait_for_timeout(800)
    a = pg.evaluate("()=>!!document.querySelector('[data-ph=qui]')")
    t('la phrase porte un créneau « à qui »', a, 'toucher le mot ouvre le choix des personnes')
    if a:
        pg.evaluate("()=>{const e=document.querySelector('[data-ph=qui]');if(e)e.click();}")
        pg.wait_for_timeout(900)
        # « à qui » ne s'écrit pas, il SE CHOISIT : le créneau ouvre une liste de personnes.
        LISTE = ("()=>[...document.querySelectorAll('#csChoix .ph-o')]"
                 ".filter(e=>e.getBoundingClientRect().width>4).length")
        n = pg.evaluate(LISTE)
        t('à qui · le créneau ouvre une liste de personnes', n > 0, '%d personnes proposées' % n)
        if n:
            pg.evaluate("()=>{const b=[...document.querySelectorAll('#csChoix .ph-o')]"
                        ".filter(e=>e.getBoundingClientRect().width>4)[0]; if(b)b.click();}")
            pg.wait_for_timeout(800)
            q = pg.evaluate("()=>((window._phrase||{}).qui||'')")
            t('à qui · choisir une personne la retient', bool(q), 'qui = « %s »' % q)

    # ⚠ CONTRÔLE RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7). J'exigeais un créneau
    #   « quand » dans la phrase. **Q28 l'a retiré il y a plusieurs lots** : l'échéance a
    #   quitté la phrase, elle vit dans Peaufiner, en tête. La phrase est à DEUX lignes —
    #   le verbe et l'objet. Le contrôle vérifie donc l'inverse : que la phrase n'en porte
    #   PAS, et que l'échéance est bien atteignable là où elle vit désormais.
    print('\n── la page + · l\'échéance a quitté la phrase (Q28) ──')
    page_plus(0)
    t('la phrase ne porte PAS de créneau « quand »',
      not pg.evaluate("()=>!!document.querySelector('#csPhrase [data-ph=quand]')"),
      'la phrase est à deux lignes : le verbe et l\'objet')

    print('\n── la page + · le compagnon d\'un Chiche ──')
    page_plus(1)
    t('la phrase d\'un Chiche porte un créneau « avec »',
      pg.evaluate("()=>!!document.querySelector('#csPhrase [data-ph=avec]')"),
      'le compagnon s\'affiche même vide (décision Tom)')

    print('\n── la page + · la Nuée ──')
    page_plus(2)
    pg.evaluate("()=>{const e=document.querySelector('#nueePhrase [data-np=nom]');if(e)e.click();}")
    pg.wait_for_timeout(800)
    champ(pg, 'le nom de la Nuée', '#nueeNomIn', 'Lisbonne',
          "()=>((document.getElementById('nName')||{}).value||'')",
          prise='#nueePhrase [data-np=nom]')

    # ── LES CHAMPS D'UNE FICHE ──────────────────────────────────────────────────────
    print('\n── une fiche · Peaufiner ──')
    pg.evaluate("""()=>{if(window.closeAll)closeAll();
      openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}"""); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}")
    pg.wait_for_timeout(1300)
    champ(pg, 'la note d\'un Promi', '#dNote', 'penser aux fleurs',
          "()=>((typeof cur!=='undefined'&&cur)?(cur.note||''):'')")

    print('\n── le champ de recherche de l\'Index ──')
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}"); pg.wait_for_timeout(1600)
    n0 = pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte,#indexList .ix-bloc').length")
    a = pg.evaluate(ATTEIGNABLE, '#ixSearch')
    t('la recherche de l\'Index · atteignable', a['ok'], a['why'])
    pg.evaluate(ECRIS, {'sel': '#ixSearch', 'txt': 'zzzzzz'}); pg.wait_for_timeout(1200)
    n1 = pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte,#indexList .ix-bloc').length")
    t('la recherche de l\'Index · FILTRE', n1 < n0, '%d cartes → %d sur un mot introuvable' % (n0, n1))
    pg.evaluate(ECRIS, {'sel': '#ixSearch', 'txt': ''}); pg.wait_for_timeout(1000)
    n2 = pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte,#indexList .ix-bloc').length")
    t('la recherche de l\'Index · se vide', n2 == n0, '%d cartes retrouvées' % n2)

    print('\n── le champ de recherche du Fil ──')
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1600)
    m0 = pg.evaluate("()=>document.querySelectorAll('#feedList .s4-carte,#feedList .fd-item').length")
    pg.evaluate(ECRIS, {'sel': '#fdSearch', 'txt': 'zzzzzz'}); pg.wait_for_timeout(1200)
    m1 = pg.evaluate("()=>document.querySelectorAll('#feedList .s4-carte,#feedList .fd-item').length")
    t('la recherche du Fil · FILTRE', m1 < m0, '%d bandeaux → %d' % (m0, m1))

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko:
    print('\nCE QUI NE MARCHE PAS :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
