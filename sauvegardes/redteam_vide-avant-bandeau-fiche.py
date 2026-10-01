#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_vide.py — UN ÉCRAN N'EST JAMAIS VIDE.

Ce contrôle-ci manquait, et c'est le plus grave qui manquait. Les neuf batteries et les cinq
juges ouvrent CHAQUE ÉCRAN SUR UNE PAGE FRAÎCHE : ils ne peuvent pas voir ce qu'un écran
laisse derrière lui. Or c'est le mécanisme le plus fréquent du produit — un `display:none`
posé EN LIGNE (le seul moyen de battre les cotes des sections, elles aussi en ligne) survit
à `closeAll`, et l'écran suivant en hérite.

Il a frappé quatre fois : la classe `dp-nuee`, le `min-height` d'une Nuée, les cartes de son
Peaufiner — et, le pire, **`#dpTrameCv` masqué par le Peaufiner d'une Nuée**. Après lui,
toute fiche sortait SANS CHAMP : le canevas était peint (10 821 pixels, mesuré) et jamais
affiché. Dans une passe complète, la moitié des captures étaient blanches.

CE QUE FAIT CE CONTRÔLE : il ENCHAÎNE les écrans, comme un doigt, sans jamais recharger la
page — deux tours, deux thèmes — et après chacun il vérifie que l'écran porte ce qu'il DOIT
porter : son entête, son champ PEINT, son titre, son état, sa barre. Un écran qui perd un
élément obligatoire fait échouer.

Usage :  python3 redteam_vide.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

import os
# de quoi passer le contrôle sur une sauvegarde : APP_VIDE=http://…/app_casse.html
APP = os.environ.get('APP_VIDE', "http://127.0.0.1:8752/app.html")
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-46s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-46s KO  %s' % (nom, detail))


# ── ce que chaque écran DOIT porter. `canvas:` = présent, visible ET peint. ─────────────
# Ce qu'un écran ne doit JAMAIS porter : les nœuds bâtis par un autre.
# ⚠ ET LE TIROIR DE LA NUÉE PAR-DESSUS UNE FICHE. Le défaut que Tom a photographié n'était
#   pas les cartes bâties (`.np-carte`) mais le contenu D'ORIGINE de `#dpdCorps` — « le
#   potager », DESCRIPTION, MEMBRES, PIÈCES, « Planter un Promi dans la Nuée » — laissé
#   visible en `position:absolute; z-index:30` par-dessus le champ, la dalle et le titre.
#   On l'interdit nommément : sur une fiche, aucun nœud du tiroir de Nuée ne se voit.
AILLEURS = ['#dpdCorps .np-carte', '#dpdCorps .np-tete', '#nfAdd', '#nqAddPromi',
            '#dpdCorps .s2-titre', '#dpdCorps .s2-bouton', '#dpdCorps .s2-fermer']
FICHE = {'sel': ['.dpt-nat', '#detailPoster>.closeb', '#dptQui', '#dptTitre', '#dptQuand', '#dpdTog'],
         'canvas': ['#dpTrameCv'], 'interdits': AILLEURS}
PPLUS = {'sel': ['#createSheet .cs-mark', '#createSheet .closeb', '#csPhrase'],
         'canvas': ['#csTrameCv'], 'interdits': AILLEURS}
NUEE  = {'sel': ['.dpt-nat', '#detailPoster>.closeb', '#dptQui', '#dptTitre', '#dptQuand', '#dpdTog'],
         'canvas': ['#dpTrameCv'], 'interdits': AILLEURS}
LISTE = lambda ent: {'sel': [ent + ' .scr-ti', ent + ' .ix-srch'], 'canvas': [],
                     'compte': (ent + ' .s4-carte', 4), 'interdits': AILLEURS}
INST  = {'sel': ['.dpt-nat', '#detailPoster>.closeb', '#dptTitre', '#dpdTog'],
         'canvas': ['#dpTrameCv'], 'interdits': AILLEURS}
# ⚠ « LE TRAIT SE REFERME » N'A PAS DE TITRE, et c'est le cadre 98 qui le dit : il porte
#   « tenue. » et la phrase, rien d'autre. Exiger `#dptTitre` là aurait fait échouer un
#   écran juste — et c'est le genre d'exigence fausse qui use un contrôle jusqu'à ce qu'on
#   cesse de le croire. On demande donc ce que CE cadre porte.
INST_REFERME = {'sel': ['.dpt-nat', '#detailPoster>.closeb', '#instTenue', '#instSous', '#dpdTog'],
                'canvas': ['#dpTrameCv'], 'interdits': AILLEURS}

ECRANS = [
 ('fiche tenue',   FICHE, "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche à tenir', FICHE, "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours',FICHE, "()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche chiche',  FICHE, "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('gardé repris',  PPLUS, "()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"),
 ('page +',        PPLUS, "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('Peaufiner',     {'sel': ['#dpdTog', '#dpdCorps'], 'canvas': [], 'compte': ('#detailPoster .s2-reg', 4)},
                          "()=>{closeAll(); const p=promises.filter(q=>!q.draft)[0]; openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('Index',         LISTE('#indexSheet'), "()=>{closeAll(); setView('toile'); ouvrirIndex();}"),
 ('Fil',           LISTE('#feedView'),   "()=>{closeAll(); setView('fil');}"),
 ('Nuée',          NUEE,  "()=>{closeAll(); openEssaim('potager');}"),
 ('Nuée vide',     NUEE,  "()=>{closeAll(); openEssaim('atelier');}"),
 ('Peaufiner Nuée',{'sel': ['#npNom', '#dpdTog'], 'canvas': [], 'compte': ('#dpdCorps .np-carte', 4)},
                          "()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ("l'instant arrive",  INST, "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);}}"),
 ("l'instant referme", INST_REFERME, "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('referme');}catch(e){}},900);}}"),
 ("l'instant après",   INST, "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},900);}}"),
]

MESURE = r"""(cfg)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const manque=[];
  const vu=e=>{ if(!e) return false; const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return false;
    const r=e.getBoundingClientRect();
    if(r.width<4||r.height<4) return false;
    if(r.bottom<dev.top-1||r.top>dev.bottom+1) return false;
    return true; };
  (cfg.sel||[]).forEach(s=>{ const e=document.querySelector(s);
    if(!e) manque.push(s+' ABSENT');
    else if(!vu(e)) { const c=getComputedStyle(e); const r=e.getBoundingClientRect();
      manque.push(s+' invisible ('+c.display+'/'+c.visibility+'/'+c.opacity
                  +' '+Math.round(r.width)+'×'+Math.round(r.height)
                  +(e.style.getPropertyValue('display')?' inline:'+e.style.getPropertyValue('display'):'')+')'); }
    /* ⚠ « vide » veut dire SANS RIEN — pas sans nœud texte. Une barre de recherche porte
       un `<input>` à `placeholder` : aucun texte propre, et pourtant elle montre son mot. */
    else if((e.textContent||'').trim()==='' && !e.querySelector('svg,canvas,input,textarea'))
      manque.push(s+' VIDE (aucun mot)'); });
  (cfg.canvas||[]).forEach(s=>{ const e=document.querySelector(s);
    if(!e){ manque.push(s+' ABSENT'); return; }
    if(!vu(e)){ const c=getComputedStyle(e);
      manque.push(s+' invisible ('+c.display+'/'+c.visibility
                  +(e.style.getPropertyValue('display')?' inline:'+e.style.getPropertyValue('display'):'')+')'); return; }
    let n=0; try{ const g=e.getContext('2d');
      const d=g.getImageData(0,0,e.width,e.height).data;
      for(let i=3;i<d.length;i+=4*53) if(d[i]>200) n++; }catch(_){}
    if(n<200) manque.push(s+' PAS PEINT ('+n+' pixels)'); });
  if(cfg.compte){ const n=[...document.querySelectorAll(cfg.compte[0])].filter(vu).length;
    if(n<cfg.compte[1]) manque.push(cfg.compte[0]+' : '+n+' au lieu de '+cfg.compte[1]+' au moins'); }
  /* ⚠ UN ÉCRAN VIDE N'EST PAS LE SEUL DÉFAUT D'ENCHAÎNEMENT : IL Y A AUSSI L'ÉCRAN
     ENCOMBRÉ. Vu à l'œil, pas ici — une fiche portait, par-dessus son titre, les cartes du
     Peaufiner d'une Nuée. Ce contrôle vérifiait qu'un écran GARDE ses éléments ; il ne
     vérifiait pas qu'il ne porte pas ceux d'un AUTRE. Les deux sont le même mécanisme —
     ce qu'un écran laisse derrière lui — donc le même contrôle. */
  (cfg.interdits||[]).forEach(s=>{ const n=[...document.querySelectorAll(s)].filter(vu).length;
    if(n) manque.push(s+' : '+n+' nœud(s) d\'un autre écran'); });
  /* ⚠ L'INVARIANT DU TIROIR : son corps ne se voit QUE s'il est déplié. Un `#dpdCorps`
     visible tiroir fermé, c'est le tiroir peint par-dessus l'écran — quel que soit le
     chemin qui y a mené. On vérifie l'état, pas l'itinéraire. */
  const _c = document.getElementById('dpdCorps'), _d = document.getElementById('dpDetails');
  if(_c && vu(_c)){
    const ouvert = (_d && _d.classList.contains('ouvert'))
      || (document.getElementById('detailPoster')||{classList:{contains:()=>false}}).classList.contains('s2-ouv');
    if(!ouvert) manque.push('#dpdCorps visible alors que le tiroir est FERMÉ');
  }
  return manque;}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                "if(o){o.classList.add('gone');o.style.display='none';}}")
    for tour in (1, 2):
        for th in ('dark', 'light'):
            print('\n══ tour %d · thème %s ══' % (tour, th))
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for nom, cfg, js in ECRANS:
                pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
                try: pg.evaluate(js)
                except Exception as e:
                    t('%s [%s]' % (nom, th), False, 'mise en scène : %s' % e); continue
                # ⚠ ON ATTEND QUE L'ÉCRAN SOIT POSÉ, PAS UN DÉLAI. Un panneau qui s'ouvre
                #   (le Peaufiner) met un temps variable à bâtir ses réglages : mesuré à
                #   2 600 ms fixes, le contrôle a sorti un faux rouge « .s2-reg : 0 » sur
                #   une passe et 61/61 sur la suivante, sans qu'une ligne bouge. Un contrôle
                #   qui flotte ne vaut rien — on attend DEUX relevés identiques du nombre de
                #   nœuds visibles, avec un plancher de temps, comme le fait le duo.
                pg.wait_for_timeout(2000)
                prec, stable = None, 0
                for _ in range(20):
                    pg.wait_for_timeout(250)
                    n = pg.evaluate("()=>[...document.querySelectorAll('#device *')]"
                                    ".filter(e=>{const r=e.getBoundingClientRect();"
                                    "return r.width>4&&r.height>4;}).length")
                    stable = stable + 1 if n == prec else 0
                    prec = n
                    if stable >= 2: break
                pg.wait_for_timeout(300)
                m = pg.evaluate(MESURE, cfg)
                t('%s [%s]' % (nom, th), not m, ' · '.join(m[:3]))
    t('aucune erreur JS', not er, ' · '.join(er[:2]))
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko:
    print('\nÉCRANS QUI PERDENT UN ÉLÉMENT OBLIGATOIRE :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
