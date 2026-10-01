#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CHANTIER 56 — filet de securite de la liaison PHRASE -> FORMULAIRE (page +).

   La page + affiche une phrase touchable dont chaque mot-pastille (sens, qui,
   titre, quand) doit propager sa valeur au formulaire cache #promiForm. La
   liaison passe par dispatchEvent et des gardes `if(el)` (app.html ~l.4866-4946) :
   elle casse EN SILENCE si un id ou un selecteur cible change de nom. Aucune
   autre batterie ne l'attrape.

   Chaque controle exerce le VRAI chemin (clic sur la pastille, puis selection)
   et verifie que la valeur arrive au champ ATTENDU, par son id. Il TOMBE si ce
   champ est renomme. Un reset() re-rend la phrase proprement avant chaque mot,
   pour ne pas melanger l'etat d'un mot a l'autre.

       python3 redteam_phrase.py        attendu : 6/6

   MIS A JOUR (S3/Q28) : le controle « quand » ne verifie plus la liaison
   phrase -> echeance, qui n'existe plus. L'echeance vit dans Peaufiner.
"""
import os as _os
from playwright.sync_api import sync_playwright

_ICI = _os.path.dirname(_os.path.abspath(__file__))
def _url():
    for p in [_os.path.join(_ICI, 'app.html'), '/home/claude/app.html']:
        if _os.path.exists(p): return 'file://' + p
    import re as _re
    for f in sorted(_os.listdir(_ICI), reverse=True):
        if _re.match(r'promi-v\d+\.html$', f): return 'file://' + _os.path.join(_ICI, f)
    return 'file:///home/claude/app.html'

R = []
def t(n, ok, d=''): R.append((n, 'OK' if ok else 'KO', d))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(_url()); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    # ouvrir la page + en mode Promi
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const t=document.querySelector('#createSheet .tile[data-kind=promi]');if(t)t.click();}"); pg.wait_for_timeout(400)

    def reset():
        # blur d'un eventuel champ focus + re-rendu propre de la phrase
        pg.evaluate("()=>{try{if(document.activeElement)document.activeElement.blur();}catch(_){}if(window._phraseRendu)_phraseRendu();}")
        pg.wait_for_timeout(220)
    def clic(sel):
        pg.evaluate("s=>{const w=document.querySelector(s);if(w)w.click();}", sel)
        pg.wait_for_timeout(280)

    reset()
    t('la phrase est rendue (#csPhrase)', pg.evaluate("()=>!!document.getElementById('csPhrase')"))

    # --- SENS : la bascule doit ATTEINDRE la forme « demander » ---
    # La bascule a QUATRE formes (grammaire validée) : Je me promets → Je promets à →
    # Rachel, promets-moi → Promettez-moi. On la fait TOURNER jusqu'à « demander », quel
    # que soit le nombre de formes (on ne clique plus une seule fois).
    reset()
    dem = None
    def _demActif():
        return pg.evaluate("()=>{const b=document.querySelector('#csSens [data-sens=demander]');return b?b.classList.contains('on'):null;}")
    for _i in range(6):            # marge : couvre 4 formes + boucle, sans tourner à l'infini
        if _demActif() is True:
            dem = True; break
        clic('#csPhrase [data-ph=sens]')
    if dem is None:
        dem = _demActif()
    t('sens : la bascule atteint la forme « demander »', dem is True, 'demander actif=%r apres cycle' % dem)

    # --- QUI : .ph-o -> #fWho (espion input : robuste au jeton deja present) ---
    reset(); clic('#csPhrase [data-ph=qui]')
    # on attache un espion a #fWho par son id : si le champ est renomme,
    # l'attache echoue (att=False) ET le binding n'atteint plus rien -> KO.
    att = pg.evaluate("""()=>{const w=document.getElementById('fWho');
      if(!w)return false; window.__qv='__aucun__';
      w.addEventListener('input', function(){window.__qv=w.value;}, {capture:true, once:true});
      return true;}""")
    # la pastille « + » (ajout d'une personne) n'a pas de data-v : on prend la dernière VRAIE pastille
    v = pg.evaluate("()=>{const os=[...document.querySelectorAll('#csChoix .ph-o')].filter(x=>!x.dataset.add);const b=os[os.length-1];if(b){b.click();return b.dataset.v;}return null;}")
    pg.wait_for_timeout(200)
    spy = pg.evaluate("()=>window.__qv")
    t('qui : la phrase alimente #fWho', att is True and v is not None and spy == v,
      'attache=%r choix=%r recu=%r' % (att, v, spy))

    # --- QUAND : CONTROLE REECRIT (decision Tom, S3/Q28).
    #     L'echeance a QUITTE la phrase — elle descend en tete de Peaufiner, comme
    #     « dans une Nuee » avant elle. L'ancien controle verifiait la liaison
    #     phrase -> pastille '+ tard' : il est PERIME, exactement comme « sens » l'a ete.
    #     Le nouveau se place au niveau de la decision, en deux moities :
    #       1 · la phrase ne porte plus de creneau « quand » ;
    #       2 · l'echeance reste adressable PAR data-d, jamais par le texte affiche
    #           (c'est le piege documente de CLAUDE.md §8 : renommer « + tard » cassait
    #            la liaison en silence).
    reset()
    sans = pg.evaluate("()=>!document.querySelector('#csPhrase [data-ph=quand]')")
    #     La propriete exacte : AUCUNE pastille d'echeance ne doit etre adressable
    #     par son seul texte. Chacune porte une prise stable — data-d (le delai en
    #     jours) ou data-q (« un jour », qui n'a pas de delai). Ce controle TOMBE si
    #     une pastille est ajoutee sans prise, comme « un jour » l'a ete a une epoque.
    parD = pg.evaluate("""()=>{const cs=[...document.querySelectorAll('#dueChips .chip,#dfDueChips .chip')];
        if(!cs.length) return null;
        const nus = cs.filter(c=>!c.hasAttribute('data-d') && !c.hasAttribute('data-q'));
        return nus.length ? nus.map(c=>(c.textContent||'').trim()) : true;}""")
    t("quand : l'echeance a quitte la phrase et aucune pastille n'est adressable par son texte",
      sans is True and parD is True, 'phrase sans creneau=%r · pastilles sans prise=%r' % (sans, parD))

    # --- TITRE : #phIn -> #fTitle.value (en dernier : il laisse le focus) ---
    reset(); clic('#csPhrase [data-ph=titre]')
    val = 'RENDRE-LE-LIVRE-56'
    pg.evaluate("v=>{const i=document.getElementById('phIn');if(i){i.value=v;i.dispatchEvent(new Event('input',{bubbles:true}));}}", val)
    pg.wait_for_timeout(200)
    got = pg.evaluate("()=>{const t=document.getElementById('fTitle');return t?t.value:null;}")
    t('titre : la phrase alimente #fTitle', got == val, 'fTitle=%r' % got)

    t('aucune erreur JS', not er, str(er[:2]))
    b.close()

for n, s, d in R: print('%-48s %s  %s' % (n, s, d))
print('\n%d/%d' % (sum(1 for _, s, _ in R if s == 'OK'), len(R)))
