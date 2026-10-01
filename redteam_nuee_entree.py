#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_nuee_entree.py — « PLANTER DANS LA NUÉE », LA DERNIÈRE LIGNE DU FIL (Q213, Tom 13 sept. 2026). AU DOIGT.

  (v106 : la Nuée s'affiche « Cercle » — le texte attendu est « Planter dans le Cercle »)
  1 · L'ENTRÉE EST LÀ, AU REPOS — sur une Nuée vide et sur une Nuée pleine, « Planter dans la Nuée », visible au doigt
  2 · UNE SEULE PLACE — pleine : 12 sous la dernière carte (le pas du fil) ; vide : 16 sous l'état (l'écart de la
      première carte). « Une même entrée ne se déplace pas selon l'état. »
  3 · LA RÈGLE DU TRAIT NE BOUGE PAS — base = max(176, 460 − 86 n), n = lignes du fil, l'entrée comprise :
      vide → 374, pleine → 176 (valeurs EN DUR, §7)
  4 · LES ÉCARTS DE LA FICHE NE SE RESSERRENT PAS — trait→Noyaux 11 · Noyaux→« Avec… » 19 · →titre 5 · titre→état 22
      (pleine : état→carte 1 16 · entre cartes 12), à 1,5 près, deux thèmes
  5 · LE TOUCHER OUVRE LA PAGE + DANS CETTE NUÉE — au doigt (CDP)
  6 · « ENCORE AUCUNE PAROLE » sur la fiche d'une Nuée vide

Preuve (§7) : `APP_NE=http://127.0.0.1:8752/sauvegardes/app-avant-lot-nuee-entree.html` doit ROUGIR.
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_NE', "http://127.0.0.1:8752/app.html")
ok = [0]; ko = []
ECARTS = [11, 18, 5, 22]             # v102 : sous les Noyaux, l'air se mesure sous l'ENCRE de leurs noms (18 avant v96), plus sous leur boîte (19) — original sauvegardes/redteam_nuee_entree-avant-v102.py             # relevés sur la fiche avant le lot (scratchpad/nuee_ecarts.py) — la décision : ne pas resserrer
BASE = {'vide': 374, 'pleine': 176}   # max(176, 460 − 86 n), n = lignes du fil (entrée comprise)


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-60s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-60s KO  %s' % (nom, detail))


J = r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;
 const Y=v=>(v-D.top)/k;
 const vis=e=>{if(!e)return false;const c=getComputedStyle(e);const r=e.getBoundingClientRect();return c.display!=='none'&&c.visibility!=='hidden'&&r.height>2&&+c.opacity>.05;};
 const encre=e=>{const rg=document.createRange();rg.selectNodeContents(e);return rg.getBoundingClientRect();};
 const cv=document.getElementById('dpTrameCv'); const boite=cv?parseFloat(cv.style.height):null;
 const B=[];
 if(boite) B.push(['trait',Y(D.top+(boite-40)*k),Y(D.top+(boite-40)*k)]);
 const au=document.getElementById('dAura'); if(vis(au)){const r=au.getBoundingClientRect(); let bas=r.bottom; au.querySelectorAll('.kr-n').forEach(n=>{ if(vis(n)){ const e2=encre(n); if(e2.bottom>0) bas=Math.max(bas,e2.bottom);} }); B.push(['Noyaux',Y(r.top),Y(bas)]);}   /* v102 : le bas des Noyaux est l'ENCRE de leurs noms */
 ['dptQui','dptTitre','dptQuand'].forEach(id=>{const e=document.getElementById(id);if(vis(e)){const r=encre(e);B.push([id,Y(r.top),Y(r.bottom)]);}});
 const cartes=[...document.querySelectorAll('#dpNueeFil .nf-item')].filter(vis).map(e=>{const r=e.getBoundingClientRect();return [Y(r.top),Y(r.bottom)];});
 const a=document.getElementById('nfAdd'); let ent=null;
 if(a&&vis(a)&&a.closest('#dpNueeFil')){const r=a.getBoundingClientRect(); ent={y0:Y(r.top),y1:Y(r.bottom),txt:(a.textContent||'').trim()};}
 const qd=document.getElementById('dptQuand');
 return {blocs:B, cartes, ent, base:boite?boite-80:null, etat:qd?(qd.textContent||'').trim():''};}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);}", th)
        pg.wait_for_timeout(600)
        cdp = ctx.new_cdp_session(pg)
        for etat, cle in [('vide', 'atelier'), ('pleine', 'potager')]:
            pg.evaluate("(k)=>{closeAll();openEssaim(k);}", cle); pg.wait_for_timeout(2800)
            r = pg.evaluate(J)
            e = r['ent']
            t('[%s · %s] 1 · « Planter dans la Nuée » est là, au repos' % (T, etat), bool(e) and e['txt'] == 'Planter dans le Cercle', str(e))
            if etat == 'vide':
                qd = [x for x in r['blocs'] if x[0] == 'dptQuand']
                air = (e['y0'] - qd[0][2]) if (e and qd) else None
                t('[%s · vide] 2 · 16 sous l\'état' % T, air is not None and abs(air - 16) <= 1.5, 'air %s' % (round(air, 1) if air is not None else '—'))
                t('[%s · vide] 6 · « ENCORE AUCUNE PAROLE »' % T, r['etat'].lower() == 'encore aucune parole', r['etat'])
            else:
                air = (e['y0'] - r['cartes'][-1][1]) if (e and r['cartes']) else None
                t('[%s · pleine] 2 · 12 sous la dernière carte' % T, air is not None and abs(air - 12) <= 1.5, 'air %s' % (round(air, 1) if air is not None else '—'))
                pas = [round(r['cartes'][i + 1][0] - r['cartes'][i][1], 1) for i in range(len(r['cartes']) - 1)]
                qd = [x for x in r['blocs'] if x[0] == 'dptQuand']
                a1 = r['cartes'][0][0] - qd[0][2] if (qd and r['cartes']) else None
                t('[%s · pleine] 4 · état→carte 16, entre cartes 12' % T, a1 is not None and abs(a1 - 16) <= 1.5 and all(abs(x - 12) <= 1.5 for x in pas), 'état→carte %s · pas %s' % (round(a1, 1) if a1 else '—', sorted(set(pas))))
            t('[%s · %s] 3 · la règle du trait : base %d' % (T, etat, BASE[etat]), r['base'] is not None and abs(r['base'] - BASE[etat]) <= 1.5, 'base %s' % r['base'])
            bl = sorted(r['blocs'], key=lambda x: x[1])
            airs = [round(bl[i + 1][1] - bl[i][2], 1) for i in range(min(4, len(bl) - 1))]
            t('[%s · %s] 4 · trait→Noyaux→Avec→titre→état : %s' % (T, etat, ECARTS), len(airs) == 4 and all(abs(a - c) <= 1.5 for a, c in zip(airs, ECARTS)), 'mesuré %s' % airs)
            # 5 · au doigt
            if e:
                pg.evaluate("()=>{const a=document.getElementById('nfAdd'); a.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(500)
                pt = pg.evaluate("()=>{const r=document.getElementById('nfAdd').getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return {x:r.left+r.width/2,y:r.top+r.height/2,dessus:!!h&&(h.id==='nfAdd'||!!h.closest('#nfAdd'))};}")
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pt['x'], 'y': pt['y']}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
                pg.wait_for_timeout(1600)
                o = pg.evaluate("()=>{const s=document.getElementById('createSheet');return {ouvert:s.classList.contains('show'),nuee:(typeof selNuee!=='undefined')?selNuee:null,cs:s.classList.contains('cs-nuee')};}")
                t('[%s · %s] 5 · au doigt, la page + s\'ouvre dans « %s »' % (T, etat, cle), pt['dessus'] and o['ouvert'] and o['nuee'] == cle, 'au doigt %s · %s' % (pt['dessus'], o))
            else:
                t('[%s · %s] 5 · au doigt, la page + s\'ouvre dans « %s »' % (T, etat, cle), False, 'pas d\'entrée')
            pg.evaluate("()=>{closeAll(); const d=document.getElementById('detailPoster'); if(d) d.scrollTop=0; const m=document.getElementById('dpMain'); if(m) m.scrollTop=0;}"); pg.wait_for_timeout(600)
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
