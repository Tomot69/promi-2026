#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_vide.py — LE BANDEAU DE COULEUR NUE ENTRE LA MATIÈRE ET LE TRAIT.

On ne suppose pas : on lit les pixels. Pour chaque abscisse du champ, on part de JUSTE
AU-DESSUS du trait et on remonte tant que le pixel est EXACTEMENT la couleur de nature de
l'écran. La hauteur ainsi parcourue est le vide à cette abscisse. On rend le pire et la
médiane, écran par écran, dans les deux thèmes.

Seuil retenu : au-delà de **24 px** de couleur nue sur la moitié de la largeur, le bandeau
se voit — c'est celui des cadres 8 et 10 de `promi-nuee-toile.html`.
"""
import sys
from playwright.sync_api import sync_playwright
APP = "http://127.0.0.1:8752/app.html"

SONDE = r"""(a)=>{
  const cv=document.getElementById(a.cv); if(!cv||!cv.width) return null;
  const g=cv.getContext('2d'); const larg=parseFloat(cv.style.width); if(!larg) return null;
  const k=cv.width/larg, W=390;
  const N=a.nat.replace('#',''); const NC=[parseInt(N.slice(0,2),16),parseInt(N.slice(2,4),16),parseInt(N.slice(4,6),16)];
  const lire=(x,y)=>{ if(x<0||y<0||x*k>=cv.width||y*k>=cv.height) return null;
    const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
    return d[3]>200?[d[0],d[1],d[2]]:null; };
  const nu=p=>p && Math.abs(p[0]-NC[0])+Math.abs(p[1]-NC[1])+Math.abs(p[2]-NC[2])<=12;
  const amp=a.amp, base=a.base, per=1.5, mont=amp*0.34, aa=amp*0.62;
  const y=x=>{const t=Math.min(1,Math.max(0,x/W));return base-mont*t-aa*Math.sin(2*Math.PI*per*t);};
  /* LE VIDE, C'EST L'ÉCART ENTRE LE BAS DE LA MATIÈRE ET LE TRAIT — pas la couleur nue en
     général. À chaque abscisse : on descend depuis le haut du champ, on retient le DERNIER
     pixel de matière (ni la couleur de nature, ni rien au-delà du trait), et on mesure ce
     qui reste jusqu'au trait. Une abscisse SANS matière du tout ne compte pas : elle est
     hors de la silhouette, et le §4 dit qu'on y voit la nature — c'est voulu. */
  const v=[]; let sans=0;
  for(let x=8;x<W-8;x+=3){
    const bas=Math.round(y(x))-8;             /* 8 = la moitié de l'épaisseur du trait + marge */
    let dernier=-1;
    for(let yy=2; yy<=bas; yy++){ const p=lire(x,yy); if(p && !nu(p)) dernier=yy; }
    if(dernier<0){ sans++; continue; }        /* pas de matière ici : hors silhouette */
    v.push(bas-dernier);
  }
  if(!v.length) return {pire:0, med:0, n:0, large:0, sans:sans};
  v.sort((p,q)=>p-q);
  return {pire:v[v.length-1], med:v[Math.floor(v.length/2)], n:v.length,
          large:v.filter(h=>h>24).length, sans:sans};}"""

def mesure(pg, cv, base, amp, nat):
    return pg.evaluate(SONDE, {'cv': cv, 'base': base, 'amp': amp, 'nat': nat})

def ligne(nom, r, plancher, remplit=True):
    """`remplit` : cet écran est-il CENSÉ remplir son champ ?
    Une fiche ou une page + hors plancher garde la BOÎTE du §2.7 — dalle centrée, nature
    autour. C'est le moodboard, et Tom l'a confirmé : le vide n'est un défaut qu'AU
    PLANCHER. On mesure quand même, mais on ne le compte comme défaut que là où la matière
    doit descendre jusqu'à la vague."""
    if not r:
        print('%-30s  non mesurable' % nom); return
    if not remplit:
        drap = 'boîte'
    else:
        drap = 'VIDE' if (r['n'] and r['med'] > 24 and r['large'] > r['n'] / 2) else '  ok'
    print('%-30s  pire %-4d médiane %-4d  >24px %d/%d  hors silhouette %-3d  %s   %s'
          % (nom, r['pire'], r['med'], r['large'], r['n'], r['sans'], drap, plancher))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        print('\n══ %s ══' % th)
        # ── LES FICHES ──
        etats = pg.evaluate("""()=>({
          encours:(promises.filter(p=>!p.draft&&!p.req&&!p.chiche&&p.status==='encours')[0]||{}).id,
          atenir :(promises.filter(p=>!p.draft&&!p.req&&p.status==='rate')[0]||{}).id,
          tenue  :(promises.filter(p=>!p.draft&&p.status==='tenu')[0]||{}).id,
          chiche :(promises.filter(p=>p.chiche)[0]||{}).id})""")
        for nom, pid in etats.items():
            if pid is None: continue
            pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid); pg.wait_for_timeout(1300)
            e = pg.evaluate("""()=>{const dp=document.getElementById('detailPoster');
              const e=window._ficheEcran(dp,cur);
              return {base:e.base,amp:e.amp,nat:e.natCol,pl:e.plancher,au:e.auPlancher};}""")
            ligne('fiche · %s' % nom, mesure(pg, 'dpTrameCv', e['base'], e['amp'], e['nat']),
                  'base %d / plancher %d%s' % (e['base'], e['pl'], '  ← AU PLANCHER' if e['au'] else ''),
                  remplit=e['au'])
        # ── LA PAGE + ──
        for i, nat in ((0, 'Promi'), (1, 'Chiche'), (2, 'Nuée')):
            pg.evaluate("()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();}")
            pg.wait_for_timeout(800)
            pg.evaluate("(i)=>{const x=[...document.querySelectorAll('#createSheet .tile')][i];if(x)x.click();}", i)
            pg.wait_for_timeout(1100)
            e = pg.evaluate("""()=>{const e=window._ppEcran?window._ppEcran():null; if(!e) return null;
              return {base:e.base,amp:e.amp,nat:window._onde.NATCOL[e.nat],pl:e.plancher,au:e.auPlancher};}""")
            if not e: continue
            ligne('page + · %s' % nat, mesure(pg, 'csTrameCv', e['base'], e['amp'], e['nat']),
                  'base %d / plancher %d%s' % (e['base'], e['pl'], '  ← AU PLANCHER' if e['au'] else ''),
                  remplit=e['au'])
        # la page + AU PLANCHER : un choix ouvert (base 196, amplitude 22)
        pg.evaluate("""()=>{const z=document.getElementById('csChoix');
          if(z){z.classList.add('ouvert'); if(!z.children.length){const d=document.createElement('div');
            d.textContent=' '; z.appendChild(d);} }
          if(window._ppTout)_ppTout();}"""); pg.wait_for_timeout(900)
        e = pg.evaluate("""()=>{const e=window._ppEcran?window._ppEcran():null; if(!e) return null;
          return {base:e.base,amp:e.amp,nat:window._onde.NATCOL[e.nat],pl:e.plancher,au:e.auPlancher};}""")
        if e:
            ligne('page + · choix ouvert', mesure(pg, 'csTrameCv', e['base'], e['amp'], e['nat']),
                  'base %d / plancher %d%s' % (e['base'], e['pl'], '  ← AU PLANCHER' if e['au'] else ''))
        pg.evaluate("""()=>{const z=document.getElementById('csChoix'); if(z)z.classList.remove('ouvert');
          if(window.closeAll)closeAll();}"""); pg.wait_for_timeout(400)
        # ── LA FICHE DE NUÉE, de 1 à 7 Promi ──
        for n in (1, 2, 3, 4, 5, 7):
            pg.evaluate("""(n)=>{ if(window.closeAll)closeAll();
              const k=Object.keys(NUE)[0];
              // on ramène la Nuée à n éléments : on retire les siens, puis on en repose n
              /* ⚠ ON NE FABRIQUE PAS DE PROMESSES : on RE-RATTACHE de vraies promesses à la
                 Nuée. Une promesse inventée porte un id que la Toile ne connaît pas,
                 `dalleTrame` échoue, et le champ sort vide — on mesure alors un vide qui
                 n'existe pas (relevé : « 1 Promi · médiane 350 », un pur artefact). */
              promises.forEach(q=>{ if(q.nuee===k) q.nuee=null; });
              promises.filter(q=>!q.draft&&!q.nuee).slice(0,n).forEach(q=>{ q.nuee=k; });
              openEssaim(k);}""", n)
            pg.wait_for_timeout(1700)
            e = pg.evaluate("""()=>{const k=(typeof curNuee!=='undefined')?curNuee:null;
              const l=k?promises.filter(q=>q.nuee===k&&!q.draft).length:0;
              const base=Math.max(176,460-86*l);
              return {base:base, amp:40, nat:'#8A5CF0', n:l};}""")
            ligne('Nuée · %d Promi' % e['n'], mesure(pg, 'dpTrameCv', e['base'], e['amp'], e['nat']),
                  'base %d / plancher 176%s' % (e['base'], '  ← AU PLANCHER' if e['base'] <= 176 else ''))
    b.close()
