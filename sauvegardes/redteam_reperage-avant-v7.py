#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_reperage.py — LIRE LA NATURE, ET UNE NUÉE EST UNE PETITE TOILE (Q213, Tom 13 sept. 2026).

  1 · CHAQUE CARTE D'INDEX ET CHAQUE LIGNE DU FIL PORTE SA NATURE — « Promi », « Chiche » ou « Nuée », en
      Bricolage 700, en haut à gauche, et le mot est CELUI DE LA NATURE (lu sur `data-nat` / la couleur du champ)
  2 · RIEN NE PASSE DEVANT UNE DALLE (§4) — la boîte de la dalle déclarée (`data-matiere`) ne croise pas le
      libellé ; au pixel, le coin du libellé est bien le libellé (`elementFromPoint`)
  3 · UNE NUÉE PLEINE EST UNE PETITE TOILE — sa carte appelle `_petiteToile` avec TOUS ses Promi et Chiche
  4 · UNE NUÉE VIDE EST UNE NUÉE — « AUCUNE PAROLE », pas « GARDÉ DE CÔTÉ », sans pointillé
  5 · L'INDEX COMPTE COMME L'ACCUEIL — « N paroles · N Nuées », N paroles = Promi et Chiche plantés, N Nuées = toutes

Deux thèmes. Preuve (§7) : `APP_REP=http://127.0.0.1:8752/sauvegardes/app-avant-lot-index-fil.html` doit ROUGIR.
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_REP', "http://127.0.0.1:8752/app.html")

# ⚑ LA POLICE DU LIBELLÉ DE NATURE — écrite ici, avec la décision qui la fixe (Tom, 16 septembre
#   2026 : « Sous-titres, libellés et navigation : Gilbert Bold, en capitales »). La RÈGLE ne bouge
#   pas — « chaque carte lit sa nature », même mot, même graisse, même coin ; seule la FAMILLE
#   change. Le juge porte la décision, l'app la respecte (§7).
#   Version d'avant : sauvegardes/redteam_reperage-avant-PALETTE-16sept.py
POLICE_NATURE = 'Gilbert'      # était 'Bricolage' jusqu'au 16 septembre 2026
ok = [0]; ko = []
MOT = {'promi': 'Promi', 'chiche': 'Chiche', 'nuee': 'Nuée'}


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-62s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-62s KO  %s' % (nom, detail))


LABELS = r"""(racine)=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;
 const COL={'#FA2258':'chiche','#8A5CF0':'nuee','#3A54FF':'promi'};
 return [...document.querySelectorAll(racine+' .s4-carte')].map(c=>{
   const l=c.querySelector('.s4-natlab'); const cv=c.querySelector('canvas'); const C=c.getBoundingClientRect();
   const champ=(cv&&cv.getAttribute('data-champ'))||'';
   let nat=c.dataset.nat||null;
   const o={titre:((c.querySelector('.s4-ti')||{}).textContent||'').trim().slice(0,22), nat, champ, et:((c.querySelector('.s4-et')||{}).textContent||'').trim()};
   if(!l){ o.label=null; return o; }
   const L=l.getBoundingClientRect(), cs=getComputedStyle(l);
   o.label=l.textContent.trim(); o.ff=cs.fontFamily.split(',')[0]; o.fw=cs.fontWeight;
   o.lx=(L.left-C.left)/k; o.ly=(L.top-C.top)/k; o.lw=L.width/k; o.lh=L.height/k;
   /* une dalle seule déclare SA boîte ; une petite Toile déclare chacune de ses dalles (`data-matieres`) */
   let boites=[]; try{ boites=JSON.parse(cv.getAttribute('data-matieres')||'null')||[]; }catch(e){}
   if(!boites.length){ const m=(cv&&cv.getAttribute('data-matiere')||'').split(',').map(Number); if(m.length===4) boites=[m]; }
   const cx=(r)=>!(r[0] >= o.lx+o.lw || r[0]+r[2] <= o.lx || r[1] >= o.ly+o.lh || r[1]+r[3] <= o.ly);
   o.croise = boites.some(cx);
   /* ⚠ LA DÉCLARATION NE SUFFIT PAS : une dalle écrasée à 0 de large se DÉCLARE quand même. On compte au pixel, dans
      chaque boîte déclarée, les pixels opaques qui s'écartent du champ — la version fautive (3 par ligne) en avait zéro. */
   let peints=0;
   try{ const g=cv.getContext('2d'), kk=cv.width/parseFloat(cv.style.width), ch=(cv.getAttribute('data-champ')||'').replace('#','');
     const F=[parseInt(ch.slice(0,2),16),parseInt(ch.slice(2,4),16),parseInt(ch.slice(4,6),16)];
     boites.forEach(r=>{ if(r[2]<2||r[3]<2) return; const d=g.getImageData(Math.round(r[0]*kk),Math.round(r[1]*kk),Math.max(1,Math.round(r[2]*kk)),Math.max(1,Math.round(r[3]*kk))).data;
       for(let i=0;i<d.length;i+=16){ if(d[i+3]>200 && (isNaN(F[0]) || Math.abs(d[i]-F[0])+Math.abs(d[i+1]-F[1])+Math.abs(d[i+2]-F[2])>40)) peints++; } }); }catch(e){}
   o.nb = peints >= 20 ? boites.length : 0; o.peints=peints;
   c.scrollIntoView({block:'center'}); const L2=l.getBoundingClientRect();
   const h=document.elementFromPoint(L2.left+3,L2.top+L2.height/2); o.auDoigt=!!h&&(h===l||l.contains(h));
   return o;});}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        T = 'clair' if th == 'light' else 'sombre'
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);}", th)
        pg.wait_for_timeout(600)
        pg.evaluate("""()=>{window._pt=[]; const o=window._petiteToile; if(o) window._petiteToile=function(g,A,L,ids){ window._pt.push(ids.slice()); return o.apply(this,arguments); };}""")
        pg.evaluate("()=>{closeAll();ouvrirIndex()}"); pg.wait_for_timeout(2800)
        ix = pg.evaluate(LABELS, '#indexList')
        mal = [c['titre'] for c in ix if not c['label'] or c['label'] != MOT.get(c['nat'], '?') or c['ff'] != POLICE_NATURE or c['fw'] != '700' or c['lx'] > 16 or c['ly'] > 16]
        t('[%s] 1 · Index : chaque carte lit sa nature' % T, ix and not mal, '%d cartes · fautives : %s' % (len(ix), mal[:4]))
        cr = [c['titre'] for c in ix if c.get('label') and (c['croise'] or not c['auDoigt'])]
        t('[%s] 2 · Index : rien devant une dalle, libellé au doigt' % T, ix and not cr and all(c.get('label') for c in ix), 'fautives : %s' % cr[:4])
        att = pg.evaluate("()=>Object.keys(NUE).map(k=>[k,promises.filter(q=>q.nuee===k&&!q.draft).map(q=>q.id)])")
        pleines = [(k, ids) for k, ids in att if len(ids) > 1]
        vus = pg.evaluate("()=>window._pt||[]")
        bon = all(any(sorted(v) == sorted(ids) for v in vus) for k, ids in pleines) and len(pleines) > 0
        t('[%s] 3 · une Nuée pleine est une petite Toile (tous ses ids)' % T, bon, '%d Nuée(s) pleine(s) · appels %s' % (len(pleines), [len(v) for v in vus]))
        vide = pg.evaluate("""()=>{const vides=Object.keys(NUE).filter(k=>!promises.some(q=>q.nuee===k&&!q.draft)).map(k=>NUE[k]);
            return [...document.querySelectorAll('#indexList .s4-carte')].filter(c=>vides.indexOf(((c.querySelector('.s4-ti')||{}).textContent||'').trim())>=0)
              .map(c=>({et:(c.querySelector('.s4-et')||{}).textContent,eb:(c.querySelector('.s4-eb')||{}).textContent,etat:c.dataset.etat,outline:c.style.outlineStyle}));}""")
        t('[%s] 4 · une Nuée vide est une Nuée' % T, vide and all(v['et'].strip() == 'AUCUNE PAROLE' and 'gard' not in (v['eb'] or '').lower() and v['outline'] != 'dashed' for v in vide), str(vide))
        cpt = pg.evaluate("""()=>{const n=promises.filter(p=>!p.req&&!p.draft).length,m=Object.keys(NUE).length;
            return {lu:(document.getElementById('ixCount')||{}).textContent, attendu:n+' parole'+(n>1?'s':'')+' · '+m+' Nuée'+(m>1?'s':'')};}""")
        t('[%s] 5 · l\'Index compte « N paroles · N Nuées »' % T, cpt['lu'] == cpt['attendu'], '%s (attendu %s)' % (cpt['lu'], cpt['attendu']))
        # ⚠ ET EN DENSITÉ « 3 PAR LIGNE » : la carte fait 106 de large, le libellé en mange 83 — la dalle n'y était
        #   plus peinte, et seul releve-S4 l'a vu. On y rejoue le contrat 2, et on exige une matière déclarée.
        pg.evaluate("()=>{window._s4Trois=true;closeAll();ouvrirIndex()}"); pg.wait_for_timeout(2800)
        ix3 = pg.evaluate(LABELS, '#indexList')
        cr3 = [c['titre'] for c in ix3 if c.get('label') and (c['croise'] or not c['auDoigt'] or (not c.get('nb') and not any(m in c['et'] for m in ('AUCUNE PAROLE', 'GARDÉ'))))]   # une Nuée vide, un gardé de côté : sans matière par définition
        t('[%s] 2 · Index 3 par ligne : dalle peinte, rien devant elle' % T, ix3 and not cr3 and all(c.get('label') for c in ix3), 'fautives : %s' % cr3[:4])
        pg.evaluate("()=>{window._s4Trois=false;}")
        pg.evaluate("()=>{closeAll();setView('fil')}"); pg.wait_for_timeout(2800)
        fil = pg.evaluate(LABELS, '#feedList')
        malf = []
        for c in fil:
            natc = {'#FA2258': 'chiche', '#8A5CF0': 'nuee'}.get((c['champ'] or '').upper(), None)
            # le champ du Fil peut céder en clarté (champCede) : on lit la teinte dominante
            if not c['label'] or c['ff'] != POLICE_NATURE or c['lx'] > 16 or c['ly'] > 16: malf.append(c['titre'])
        t('[%s] 1 · Fil : chaque ligne lit sa nature, à gauche' % T, fil and not malf, '%d lignes · fautives : %s' % (len(fil), malf[:4]))
        crf = [c['titre'] for c in fil if c.get('label') and (c['croise'] or not c['auDoigt'])]
        t('[%s] 2 · Fil : rien devant une dalle, libellé au doigt' % T, fil and not crf and all(c.get('label') for c in fil), 'fautives : %s' % crf[:4])
        pg.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
