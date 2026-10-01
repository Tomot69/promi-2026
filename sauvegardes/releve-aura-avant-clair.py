#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-aura.py — LE JUGE DE L'AURA (l'Orbite portée dans l'app), deux thèmes.

Référence : PLANCHE-VELOURS.html, `ecranAura()` — gabarit 340 × 736, ramené à l'écran
de 390 × 844 (÷ 0,872). Les Noyaux sont au §2.9 de PROMI-SPECIFICATIONS.md, à la lettre.

HUIT FAMILLES DE CONTRÔLE
   1 · POSITIONS           écart > 3 px à la cote calculée
   2 · STYLES              police, graisse, taille, couleur, fond, trait
   3 · COLLISIONS          deux blocs qui se recouvrent
   4 · DÉBORDEMENTS        rien ne sort de l'appareil — la rangée des Noyaux se DÉCLARE
                           glissante (data-glisse) et n'est exemptée que SOUS CONDITION :
                           elle tient dans le cadre ET elle rogne (Q128 §3)
   5 · PRÉSENCE PEINTE     la sphère, ses îles, les arcs, les visages et les dalles
                           tenues sont LUS dans les pixels et le DOM — un bloc à la bonne
                           cote mais vide est un faux vert
   6 · DONNÉES             le sol calcule la nature MAJORITAIRE ; les dalles sortent dans
                           le monde de LEUR plantation ; « toi » prend la vraie photo
   7 · LES HUIT ACQUIS     joués au vrai pointeur, dans l'app — pas dans la planche
   8 · DENSITÉ             le palier tenu, et la preuve que la densité CÈDE sous un
                           processeur ralenti sans qu'aucun geste ne se perde

⚠ La matière RESPIRE (`dalleTrame` lit `performance.now()`) : aucune ÉGALITÉ de pixels
n'est exigée. Les égalités se lisent dans la COMPOSITION publiée (`window._auraComp`),
les pixels ne servent qu'à dire « peint / pas peint » et « a changé / est revenu », à
vue figée (`_aura.fige`) pour que la rotation ne se mêle pas de la mesure.

Usage :  python3 releve-aura.py [--verbose] [--injecte]
         --injecte : développement — injecte le bloc de scratchpad dans l'app intacte
"""
import base64, sys, os, io, json
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_AURA', "http://127.0.0.1:8752/app.html")
VERBOSE = '--verbose' in sys.argv
INJECTE = '--injecte' in sys.argv
TOL = 3
SP_AURA = os.environ.get('AURA_DEV', '/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/dcd8febe-cb8b-4dd6-a4f8-2c1646ff8fa4/scratchpad/aura')

# ⚑ LA ROTATION LENTE EST UNE DÉCISION, ÉCRITE ICI — jamais lue dans l'app : un juge qui prendrait
#   la vitesse que l'app déclare accepterait n'importe laquelle. Un tour en 2 minutes (Tom,
#   10 septembre 2026 : « un peu trop lente, accélère-la à peine »). Elle était à 2 min 45.
AUTO_DECIDE = 6.283185307 / 120
CREME, ENCRE = '#F4EEE1', '#16171B'
GRIS_S, GRIS_C = '#A8A396', '#6B6658'
ETA = ['#2BE88C', '#8FA0FF', '#F07A2E']
PISTE = {'dark': '#2A2C34', 'light': '#DED7C6'}
NAT_TEINTE = {'promi': 232, 'chiche': 345, 'nuee': 262}      # teinte HSL, en degrés

# ── LES COTES, calculées (planche ÷ 0,872 ; §2.9) ──────────────────────────────────
K = {'boule': (47, 89.4, 296, 296), 'mot': 403.7, 'nx': (24, 454, 107),
     'lg': 589, 'lgH': 16, 'mo': 633, 'bt': (24, 762, 342, 60), 'enh': (24, 40, 342, 60),
     'toi': (78, 8, 48), 'pers': (58, 6, 36), 'gapToi': 30, 'gapPers': 26}

MESURE = r"""(th)=>{
  const dv=document.getElementById('device').getBoundingClientRect(), sc=dv.width/390;
  const SC=document.getElementById('auraScreen');
  const G=e=>{ if(!e) return null; const r=e.getBoundingClientRect();
    return {x:(r.left-dv.left)/sc, y:(r.top-dv.top)/sc, w:r.width/sc, h:r.height/sc,
            b:(r.bottom-dv.top)/sc, r:(r.right-dv.left)/sc, vis:r.width>0&&r.height>0}; };
  const S=e=>{ if(!e) return null; const c=getComputedStyle(e);
    return {ff:c.fontFamily.split(',')[0].replace(/["']/g,'').trim(), fw:c.fontWeight, fs:parseFloat(c.fontSize),
            col:c.color, fill:c.webkitTextFillColor, op:+c.opacity, bg:c.backgroundColor, ls:c.letterSpacing,
            tt:c.textTransform, bw:c.borderTopWidth, bc:c.borderTopColor, br:c.borderTopLeftRadius}; };
  const q=s=>SC.querySelector(s), qa=s=>[...SC.querySelectorAll(s)];
  const out={};
  out.show=SC.classList.contains('show'); out.au2=SC.classList.contains('au2');
  out.fond=getComputedStyle(SC).backgroundColor;
  out.avant=getComputedStyle(SC,'::before').display;
  out.enh=G(q(':scope>.enh')); out.enhTxt=(q(':scope>.enh')||{}).textContent||'';
  out.boule=G(q('#auBoule')); out.mot={g:G(q('.au-mot')), s:S(q('.au-mot')), t:(q('.au-mot')||{}).textContent};
  out.inv={g:G(q('.au-inv')), t:(q('.au-inv')||{}).textContent};
  const nx=q('.au-nx'); out.nx={g:G(nx), glisse:nx&&nx.getAttribute('data-glisse'),
    ov:nx?getComputedStyle(nx).overflowX:null};
  out.noyaux=qa('.au-n').map(n=>{ const sv=n.querySelector('svg'), lb=n.querySelector('.au-lb'), vi=n.querySelector('.au-vis');
    const arcs=[...n.querySelectorAll('circle.au-arc')].map(c=>({col:c.getAttribute('stroke'), sw:+c.getAttribute('stroke-width')}));
    const pi=n.querySelector('circle.au-piste');
    return {qui:n.getAttribute('data-qui'), moi:n.classList.contains('au-moi'), col:G(n), svg:G(sv), lb:G(lb), lbs:S(lb),
            lbt:lb?lb.textContent:'', vis:G(vi), visBg:vi?getComputedStyle(vi).backgroundImage:'',
            photo:vi?vi.getAttribute('data-photo'):null, arcs:arcs,
            piste:pi?getComputedStyle(pi).stroke:null, pisteSw:pi?+pi.getAttribute('stroke-width'):0}; });
  const lg=q('.au-lg'); out.lg={g:G(lg), s:S(lg), centre:lg&&lg.getAttribute('data-centre-entre'),
    items:lg?[...lg.querySelectorAll('span')].map(s=>({t:s.textContent.trim(), c:getComputedStyle(s.querySelector('i')).backgroundColor})):[]};
  const h3=q('.au-mo h3'); out.h3={g:G(h3), s:S(h3), t:h3?h3.textContent:''};
  out.cells=qa('.au-c').map(c=>{ const cv=c.querySelector('canvas'), sp=c.querySelector('span'); let n=0;
    try{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; for(let i=3;i<d.length;i+=16) if(d[i]>20) n++; }catch(e){}
    const cs=cv?getComputedStyle(cv):null;
    return {cv:G(cv), bx:G(c.querySelector('.au-bx')), sp:G(sp), sps:S(sp), t:sp?sp.textContent:'', peint:n,
            op:cs?+cs.opacity:0, fi:cs?cs.filter:'', pid:cv?+cv.getAttribute('data-pid'):null}; });
  out.bt={g:G(q('.au-bt')), s:S(q('.au-bt')), t:(q('.au-bt')||{}).textContent};
  /* l'ancienne Aura : aucun enfant hérité ne doit se voir */
  out.herites=[...SC.children].filter(e=>!(e.classList.contains('enh')||e.classList.contains('enh-voile')||e.id==='auCadre'))
    .filter(e=>{ const r=e.getBoundingClientRect(); return r.width>0&&r.height>0&&getComputedStyle(e).display!=='none'; })
    .map(e=>e.tagName+(e.id?'#'+e.id:'.'+(''+e.className).split(' ')[0]));
  /* textes : encre pleine (§6), text-fill = color (§3), aucun chiffre ni % (l'Aura sans chiffre) */
  const txt=[]; qa('#auCadre *').forEach(e=>{
    const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim(); if(!t) return;
    const r=e.getBoundingClientRect(); if(!r.width||!r.height) return;
    let op=1; for(let n=e;n&&n!==SC;n=n.parentElement) op*=+getComputedStyle(n).opacity;
    const c=getComputedStyle(e); txt.push({t:t.slice(0,40), op:op, col:c.color, fill:c.webkitTextFillColor, fs:parseFloat(c.fontSize)}); });
  out.textes=txt;
  return out;
}"""

# collisions : les blocs porteurs, deux à deux ; la BOULE compte pour son disque, pas pour son canevas
COLL = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), sc=dv.width/390;
  const SC=document.getElementById('auraScreen'); const L=[];
  const add=(nom,e)=>{ if(!e) return; const r=e.getBoundingClientRect(); if(!r.width||!r.height) return;
    if(getComputedStyle(e).display==='none') return;
    L.push({nom:nom, x:(r.left-dv.left)/sc, y:(r.top-dv.top)/sc, r:(r.right-dv.left)/sc, b:(r.bottom-dv.top)/sc}); };
  const bo=document.getElementById('auBoule');
  if(bo){ const r=bo.getBoundingClientRect(), R=r.width*0.392, cx=r.left+r.width/2, cy=r.top+r.height/2;
    L.push({nom:'la boule', x:(cx-R-dv.left)/sc, y:(cy-R-dv.top)/sc, r:(cx+R-dv.left)/sc, b:(cy+R-dv.top)/sc}); }
  add('le plateau', SC.querySelector(':scope>.enh'));
  add('le mot', SC.querySelector('.au-mot')); add('le vide', SC.querySelector('.au-inv'));
  SC.querySelectorAll('.au-nb').forEach((e,i)=>add('noyau '+i, e));
  SC.querySelectorAll('.au-lb').forEach((e,i)=>add('prénom '+i, e));
  SC.querySelectorAll('.au-lg span').forEach((e,i)=>add('légende '+i, e));
  add('le titre', SC.querySelector('.au-mo h3'));
  SC.querySelectorAll('.au-bx canvas').forEach((e,i)=>add('dalle '+i, e));
  SC.querySelectorAll('.au-c span').forEach((e,i)=>add('libellé '+i, e));
  add('le bouton', SC.querySelector('.au-bt'));
  const nx=SC.querySelector('.au-nx'), nr=nx?nx.getBoundingClientRect():null;
  const vis=o=>!nr||!(o.nom.startsWith('noyau')||o.nom.startsWith('prénom'))||((o.r*sc+dv.left)>nr.left+1&&(o.x*sc+dv.left)<nr.right-1);
  const out=[];
  for(let i=0;i<L.length;i++) for(let j=i+1;j<L.length;j++){ const a=L[i], b=L[j];
    if(!vis(a)||!vis(b)) continue;
    const w=Math.min(a.r,b.r)-Math.max(a.x,b.x), h=Math.min(a.b,b.b)-Math.max(a.y,b.y);
    if(w>0.5&&h>0.5) out.push(a.nom+' × '+b.nom+' ('+w.toFixed(1)+' × '+h.toFixed(1)+')'); }
  return out; }"""

# débordements : rien ne sort de l'appareil — sauf DANS une rangée déclarée glissante
# qui, elle, tient dans le cadre ET rogne
# ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (Tom, 10 sept. — CLAUDE.md §8 : « si l'air rendu ne tient plus
#   dans l'écran, l'écran DÉFILE »). La colonne de l'Aura défile : un bloc qui dépasse VERS LE BAS
#   n'est pas un débordement s'il vit dans une colonne qui se DÉCLARE (`data-defile`), qui tient
#   elle-même dans l'appareil et qui ROGNE en hauteur — et s'il ne sort pas par les CÔTÉS.
#   Même règle que la rangée glissante, tournée d'un quart. Original : sauvegardes/releve-aura-avant-colonne.py
DEBORD = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), sc=dv.width/390;
  const SC=document.getElementById('auraScreen'), out=[];
  SC.querySelectorAll('#auCadre *').forEach(e=>{ const r=e.getBoundingClientRect();
    if(r.width<2||r.height<2) return;
    if(r.right<=dv.right+2&&r.left>=dv.left-2&&r.bottom<=dv.bottom+2&&r.top>=dv.top-2) return;
    const g=e.closest('[data-glisse]');
    if(g&&g!==e){ const gr=g.getBoundingClientRect(), ov=getComputedStyle(g).overflowX;
      if(gr.left>=dv.left-2&&gr.right<=dv.right+2&&(ov==='hidden'||ov==='auto'||ov==='scroll')) return; }
    const v=e.closest('[data-defile]');
    if(v&&v!==e&&r.left>=dv.left-2&&r.right<=dv.right+2){ const vr=v.getBoundingClientRect(), oy=getComputedStyle(v).overflowY;
      if(vr.top>=dv.top-2&&vr.bottom<=dv.bottom+2&&(oy==='hidden'||oy==='auto'||oy==='scroll')) return; }
    out.push((e.className&&e.className.baseVal===undefined?e.className:e.tagName)+' x '+((r.left-dv.left)/sc).toFixed(0)+'→'+((r.right-dv.left)/sc).toFixed(0)); });
  return out; }"""

# présence peinte de la BOULE : un disque plein, transparent autour, la teinte du sol
BOULE = r"""()=>{
  const cv=document.getElementById('auBoule'); if(!cv||!cv.width) return null;
  const W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data, c=W/2, R=W*0.392;
  let dedans=0, plein=0, dehors=0, vide=0; const H=[];
  for(let y=0;y<W;y+=3) for(let x=0;x<W;x+=3){ const r=Math.hypot(x-c,y-c), i=(y*W+x)*4;
    if(r<R*0.86){ dedans++; if(d[i+3]>200){ plein++;
        const R8=d[i]/255,G8=d[i+1]/255,B8=d[i+2]/255, mx=Math.max(R8,G8,B8), mn=Math.min(R8,G8,B8);
        if(mx-mn>0.18){ let h; if(mx===R8) h=((G8-B8)/(mx-mn))%6; else if(mx===G8) h=(B8-R8)/(mx-mn)+2; else h=(R8-G8)/(mx-mn)+4;
          h*=60; if(h<0) h+=360; H.push(h); } } }
    else if(r>R*1.10){ dehors++; if(d[i+3]<16) vide++; } }
  H.sort((a,b)=>a-b);
  return {plein:plein/Math.max(1,dedans), vide:vide/Math.max(1,dehors), teinte:H.length?H[H.length>>1]:null, n:H.length}; }"""

# pixels à vue figée : instantané, et part des pixels de la boule qui ont changé
SNAP = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__snap_'+nom]=
  cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); return cv.width; }"""
DIFF = r"""([a,b,zone])=>{ const A=window['__snap_'+a], B=window['__snap_'+b]; if(!A||!B||A.length!==B.length) return null;
  const W=Math.round(Math.sqrt(A.length/4)), c=W/2, R=W*0.392; let n=0, ch=0;
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){
    let dx=x-c, dy=y-c; if(zone){ dx=x-(c+zone[0]*R); dy=y-(c+zone[1]*R); if(Math.hypot(dx,dy)>zone[2]*R) continue; }
    else if(Math.hypot(dx,dy)>R*0.95) continue;
    const i=(y*W+x)*4; n++;
    if(Math.abs(A[i]-B[i])>3||Math.abs(A[i+1]-B[i+1])>3||Math.abs(A[i+2]-B[i+2])>3||Math.abs(A[i+3]-B[i+3])>3) ch++; }
  return ch/Math.max(1,n); }"""

# le retour de l'empreinte, IMAGE PEINTE PAR IMAGE PEINTE, enregistré dans la page (vue figée) :
# [ms depuis le départ, p de l'empreinte ou null, part de la zone changée depuis l'image
#  précédente, part de la zone qui diffère encore du repos]. S'arrête 6 images après le retrait.
REC_RETOUR = r"""([tx,ty])=>new Promise(res=>{
  const cv=document.getElementById('auBoule'), g=cv.getContext('2d'), W=cv.width, c=W/2, R=W*0.392;
  const zx=c+tx*R, zy=c+ty*R, zr=0.35*R, A=window.__snap_repos;
  const x0=Math.max(0,Math.floor(zx-zr)), y0=Math.max(0,Math.floor(zy-zr));
  const w=Math.min(W,Math.ceil(zx+zr))-x0, h=Math.min(W,Math.ceil(zy+zr))-y0;
  const dif=(a,i,b,j)=>Math.abs(a[i]-b[j])>3||Math.abs(a[i+1]-b[j+1])>3||Math.abs(a[i+2]-b[j+2])>3||Math.abs(a[i+3]-b[j+3])>3;
  const out=[]; let prev=null, lastP=-1, apres=0; const t0=performance.now();
  function tick(){
    const e=_aura.etat();
    if(e.peints!==lastP){ lastP=e.peints;
      const d=g.getImageData(x0,y0,w,h).data; let n=0, cP=0, cR=0, aP=0, aR=0;
      const amp=(a,i,b,j)=>(Math.abs(a[i]-b[j])+Math.abs(a[i+1]-b[j+1])+Math.abs(a[i+2]-b[j+2]))/3;
      for(let yy=0;yy<h;yy+=2) for(let xx=0;xx<w;xx+=2){
        if(Math.hypot(x0+xx-zx,y0+yy-zy)>zr) continue; n++;
        const i=(yy*w+xx)*4, j=((y0+yy)*W+x0+xx)*4;
        if(prev){ if(dif(d,i,prev,i)) cP++; aP+=amp(d,i,prev,i); }
        if(dif(d,i,A,j)) cR++; aR+=amp(d,i,A,j); }
      out.push([Math.round(performance.now()-t0), e.emp?e.emp.p:null, prev?cP/n:null, cR/n, prev?aP/n:null, aR/n]); prev=d;
      if(!e.emp && ++apres>=6) return res(out);
    }
    if(performance.now()-t0>20000) return res(out);
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})"""

# ⚠ UN LANCER SE JOUE DANS LA PAGE, CADENCÉ. Mesuré le 10 septembre : face à un fil
#   principal occupé à peindre, les `mouse.move` de Playwright arrivent à ~130 ms les uns des
#   autres, et le relâcher tombe 129 ms après le dernier — c'est un doigt qui s'ARRÊTE avant
#   de se lever. Il n'y a physiquement pas d'élan, et la fenêtre de 90 ms de la planche le dit
#   à juste titre. Un vrai lancer : des mouvements toutes les 16 ms, relâchés sans arrêt.
LANCE = r"""async ([x0,y0,dx,n,pas,tenir])=>{ const t=document.querySelector('#auraScreen .au-prise');
  const o=(x)=>({pointerId:7,pointerType:'mouse',isPrimary:true,clientX:x,clientY:y0,bubbles:true,cancelable:true,buttons:1});
  t.dispatchEvent(new PointerEvent('pointerdown',o(x0)));
  if(tenir) await new Promise(r=>setTimeout(r,tenir));
  for(let k=1;k<=n;k++){ await new Promise(r=>setTimeout(r,pas)); t.dispatchEvent(new PointerEvent('pointermove',o(x0+dx*k/n))); }
  t.dispatchEvent(new PointerEvent('pointerup',o(x0+dx)));
  return {t:performance.now(), elan:_aura.etat().elan}; }"""

# ⚠ ON LIT LE PAS DE TEMPS DE LA BOUCLE, PAS CELUI DE L'ÉCHANTILLONNEUR (CLAUDE.md §8, règle du
#   temps réel). Vécu : deux images de 130 ms lues comme une seule de 260 — le modèle appliquait UNE
#   décroissance là où la boucle en avait appliqué DEUX, et sortait une fausse saccade. Une ligne par
#   image de la boucle : [temps cumulé ms, lac, vlac, tan, dt réel s, ms du peintre, n° d'image,
#   images sautées, horloge ms]. Une image que l'échantillonneur a manquée n'est pas modélisée.
ENREG = r"""async (ms)=>{ const out=[]; const t0=performance.now(); let k0=_aura.etat().tick, tc=0;
  await new Promise(r=>{ function f(){ const e=_aura.etat();
      if(e.tick!==k0){ const s=e.tick-k0; k0=e.tick; tc+=e.dtReel*1000;
        out.push([tc, e.lac, e.vlac, e.tan, e.dtReel, e.dernier, e.tick, s, performance.now()-t0]); }
      if(performance.now()-t0<ms) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  return out; }"""


def hexa(c):
    if not c: return ''
    if c.startswith('#'): return c.upper()
    try:
        v = c[c.index('(') + 1:c.index(')')].split(',')
        return '#%02X%02X%02X' % tuple(int(float(x)) for x in v[:3])
    except Exception:
        return c


# ⚑ L'AIR DE LA COLONNE — DÉCIDÉ, EN DUR (le juge porte la décision, CLAUDE.md §7). Tom, 10 sept. :
#   « sous le commentaire de la sphère, les disques sont trop près : ça ne respire pas » — la cinquième
#   fois qu'un espacement revient. Les deux valeurs viennent de la planche, jamais de l'œil :
AIR_MOT = 26.675          # l'air que la planche laissait sous UNE ligne de phrase : 454 − 403,7 − 18,9 × 1,25
AIR_BLOC = 28.0           # le rythme de la colonne : la légende de la planche, centrée à 28 de chaque côté
LIGNE_MOT = 18.9 * 1.25   # une ligne de phrase (18,9 px, interligne 1,25)
AIR_MIN = 26.0            # plancher mesuré à l'encre / aux boîtes (l'air décidé, moins l'arrondi des glyphes)
PLI = 844.0               # le bas de l'écran à l'ouverture — Q186 (Tom) : le bouton y est ENTIER (avec sa marge)
MARGE_BAS = 22.0          #   ou FRANCHEMENT sous le pli, jamais coupé en deux
MOISSON = 6               # « Ce que tu as tenu » : jusqu'à six dalles, deux rangées (Tom, 10 sept. — Q187)
RANG2 = 5                 # RÈGLE (Tom — Q189) : la seconde rangée paraît à partir de CINQ tenues ; en dessous, trois au plus

# la colonne mesurée dans le repère du CADRE (pt d'écran 390, défilement compris)
AIRM = r"""()=>{ const cad=document.getElementById('auCadre'), cr=cad.getBoundingClientRect(), s=cr.width/390;
  const Y=(v)=>(v-cr.top)/s+cad.scrollTop, r=(e)=>e.getBoundingClientRect();
  const q=(x)=>document.querySelector('#auraScreen '+x), qa=(x)=>[...document.querySelectorAll('#auraScreen '+x)];
  const mot=q('.au-mot'), rg=document.createRange(); rg.selectNodeContents(mot); const L=[...rg.getClientRects()];
  const lib=qa('.au-c span').filter(e=>r(e).height>0), h3=q('.au-mo h3');
  return {texte:mot.textContent, lignes:new Set(L.map(x=>Math.round(x.top))).size, mot_bas:Y(Math.max(...L.map(x=>x.bottom))),
    disques:Y(Math.min(...qa('.au-nb').map(e=>r(e).top))), prenoms:Y(Math.max(...qa('.au-lb').map(e=>r(e).bottom))),
    lg_h:Y(r(q('.au-lg')).top), lg_b:Y(r(q('.au-lg')).bottom), h3:(h3&&r(h3).height)?Y(r(h3).top):null,
    lib:lib.length?Y(Math.max(...lib.map(e=>r(e).bottom))):null, bt_h:Y(r(q('.au-bt')).top), bt_b:Y(r(q('.au-bt')).bottom),
    cells:qa('.au-c').filter(e=>r(e).height>0).map(e=>[Y(r(e).top), Y(r(e).bottom)]),
    defil:cad.scrollHeight}; }"""
# à l'encre, sur l'image rendue : de la dernière ligne de pixels de la phrase à la première des disques
ENCRE_GAP = r"""async ([u,fond,yref])=>{ const im=new Image(); im.src=u; await im.decode();
  const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; const g=c.getContext('2d'); g.drawImage(im,0,0);
  const d=g.getImageData(0,0,c.width,c.height).data, W=c.width, s=W/390, x0=Math.round(24*s), x1=Math.round(366*s);
  const ink=(y)=>{ let n=0; for(let x=x0;x<x1;x++){ const i=(y*W+x)*4;
    if(Math.abs(d[i]-fond[0])+Math.abs(d[i+1]-fond[1])+Math.abs(d[i+2]-fond[2])>42 && ++n>=2) return true; } return false; };
  const yr=Math.round((yref+1)*s); let a=yr, b=yr; while(a>0 && !ink(a)) a--; while(b<c.height-1 && !ink(b)) b++;
  return (b-a)/s; }"""
# le cadre défilé jusqu'au bout : rien de lui ne doit se voir au-dessus du plateau
PROTEGE = r"""async ()=>{ const cad=document.getElementById('auCadre'); cad.scrollTop=cad.scrollHeight;
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, fautes=[];
  for(const [x,y] of [[8,20],[195,20],[382,20],[8,70],[382,70],[195,98]]){
    const e=document.elementFromPoint(dv.left+x*s, dv.top+y*s); if(e && e!==cad && cad.contains(e)) fautes.push([x,y,String(e.className||e.tagName)]); }
  /* et par construction : un cadre qui DÉFILE doit rogner au bas du plateau (y ≥ 100) */
  const cp=getComputedStyle(cad).clipPath||'', mt=/inset\(\s*([\d.]+)px/.exec(cp), clip=mt?+mt[1]:0;
  if(cad.scrollHeight>cad.clientHeight+1 && clip<99) fautes.push(['clip', clip, cp]);
  const enh=document.querySelector('#auraScreen .enh'), er=enh?enh.getBoundingClientRect():null, haut=cad.scrollTop;
  cad.scrollTop=0; await new Promise(r=>requestAnimationFrame(r));
  return {fautes:fautes, defile:haut/s, enh_y:er?(er.top-dv.top)/s:null}; }"""
POSE_MOT = r"""(i)=>{ if(window._aura && _aura.mot) return _aura.mot(i);
  const L=['Rien de ce qui est ici n’a été dit à la légère.','Tout ça, tu l’as dit. Et tu l’as fait.',
    'On ne dirait pas comme ça, mais c’est du solide.','Il y en a, des paroles tenues.','Et dire que tout ça, c’est toi.'];
  const m=document.querySelector('#auraScreen .au-mot'); if(i===null){ return m.textContent; } m.textContent=L[i]; return L[i]; }"""


def juge():
    pos, sty, coll, hors, peint, don, acq, den = [], [], [], [], [], [], [], []
    air = []          # ⚑ 9 · l'air de la colonne (Tom, 10 sept.)
    er = []
    VAL = []          # la valeur MESURÉE de chaque acquis — imprimée qu'il passe ou non
    import time as _tm
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if INJECTE:
            import subprocess
            subprocess.run(['python3', os.path.join(SP_AURA, 'fabrique.py')], check=True, capture_output=True)
            pg.add_style_tag(content=io.open(os.path.join(SP_AURA, 'aura.css'), encoding='utf-8').read())
            pg.add_script_tag(content=io.open(os.path.join(SP_AURA, 'moteur.js'), encoding='utf-8').read())
            pg.add_script_tag(content=io.open(os.path.join(SP_AURA, 'aura.js'), encoding='utf-8').read())

        def ouvre():
            pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250)
            pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(80):
                pg.wait_for_timeout(200)
                e = pg.evaluate("()=>window._aura?_aura.etat():null")
                if e and e['pret'] and e['frames'] > 12: break
            pg.wait_for_timeout(500)
            return pg.evaluate("()=>window._aura?_aura.etat():null")

        def attends(cond, ms=9000):
            t = 0
            while t < ms:
                if pg.evaluate(cond): return True
                pg.wait_for_timeout(100); t += 100
            return False

        def peintes(n=2):
            """attend n images RÉELLEMENT peintes après ce qu'on vient de faire — jamais un
               délai fixe : sur une machine chargée, une image recalculée arrive tard, et
               photographier avant, c'est mesurer l'image d'avant."""
            p0 = pg.evaluate("()=>_aura.etat().peints")
            attends("()=>_aura.etat().peints>=%d" % (p0 + n), 15000)

        def boule():
            r = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect();"
                            "const d=document.getElementById('device').getBoundingClientRect();"
                            "return {cx:r.left+r.width/2, cy:r.top+r.height/2, R:r.width*0.392, sc:d.width/390};}")
            return r

        if not pg.evaluate("()=>!!window._aura && !!document.getElementById('auCadre')"):
            print('❌  le bloc lot-AURA-ORBITE est absent de la page'); b.close(); return 99

        # ═══ 1 à 5 · LA GÉOMÉTRIE, LES STYLES, LA PRÉSENCE — deux thèmes ═══════════════
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
            e0 = ouvre()
            E = '[%s]' % ('sombre' if th == 'dark' else 'clair')
            m = pg.evaluate(MESURE, th)
            comp = pg.evaluate("()=>window._auraComp")
            if not m['show']: pos.append(E + " l'Aura ne s'ouvre pas"); continue
            fondAttendu = ENCRE if th == 'dark' else CREME
            encre = CREME if th == 'dark' else ENCRE
            gris = GRIS_S if th == 'dark' else GRIS_C
            if hexa(m['fond']) != fondAttendu: sty.append(E + ' fond %s au lieu de %s' % (hexa(m['fond']), fondAttendu))
            if m['avant'] != 'none': sty.append(E + " l'ombre de dalle de .tuto-fond::before est encore peinte")
            for h in m['herites']: coll.append(E + ' nœud de l\'ancienne Aura encore visible : ' + h)
            g = m['enh']
            if not g or max(abs(g['x']-K['enh'][0]), abs(g['y']-K['enh'][1]), abs(g['w']-K['enh'][2]), abs(g['h']-K['enh'][3])) > TOL:
                pos.append(E + ' le plateau %s au lieu de %s' % (g and (round(g['x']), round(g['y']), round(g['w']), round(g['h'])), K['enh']))
            if 'Aura' not in m['enhTxt'] or 'FERMER' not in m['enhTxt'].upper():
                pos.append(E + ' le plateau ne porte plus « Aura » et « ✕ FERMER »')
            g = m['boule']
            if not g or max(abs(g['x']-K['boule'][0]), abs(g['y']-K['boule'][1]), abs(g['w']-K['boule'][2])) > TOL:
                pos.append(E + ' la sphère %s au lieu de %s' % (g and (round(g['x'],1), round(g['y'],1), round(g['w'])), K['boule']))
            vide = comp['vide']
            if not vide:
                g = m['mot']['g']
                if not g or abs(g['y']-K['mot']) > TOL or abs(g['x']-24) > TOL:
                    pos.append(E + ' le mot à %s au lieu de (24, %.1f)' % (g and (round(g['x']), round(g['y'],1)), K['mot']))
                s = m['mot']['s']
                if s['ff'] != 'Bricolage' or s['fw'] != '700' or abs(s['fs']-18.9) > 0.3 or hexa(s['col']) != encre:
                    sty.append(E + ' le mot : %s %s %.1f %s' % (s['ff'], s['fw'], s['fs'], hexa(s['col'])))
                # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (Tom, 10 sept.) : la rangée n'est plus attendue à 454 en
                #   dur — elle se DÉRIVE du bas réel de la phrase (1 ou 2 lignes) + l'air de la planche, et la
                #   légende et « Ce que tu as tenu » suivent. Original : sauvegardes/releve-aura-avant-colonne.py
                gm = m['mot']['g']; lignes = max(1, round(gm['h'] / LIGNE_MOT)) if gm else 1
                exp_nx = K['mot'] + lignes * LIGNE_MOT + AIR_MOT
                exp_lg = exp_nx + K['nx'][2] + AIR_BLOC
                exp_mo = exp_lg + K['lgH'] + AIR_BLOC
                g = m['nx']['g']
                if not g or abs(g['y']-exp_nx) > TOL or abs(g['x']-K['nx'][0]) > TOL or abs(g['h']-K['nx'][2]) > TOL:
                    pos.append(E + ' la rangée des Noyaux %s au lieu de y %.1f (phrase de %d ligne(s) + %.3f)' % (g and (round(g['x']), round(g['y'],1), round(g['h'])), exp_nx, lignes, AIR_MOT))
                if m['nx']['glisse'] != '1': hors.append(E + ' la rangée ne se déclare pas glissante (data-glisse)')
                N = m['noyaux']
                if not N or not N[0]['moi'] or N[0]['lbt'] != 'toi':
                    pos.append(E + ' « toi » n\'est pas le premier Noyau')
                bases = []
                for i, n in enumerate(N):
                    d, arc, ph = K['toi'] if n['moi'] else K['pers']
                    if not n['svg'] or abs(n['svg']['w']-d) > 0.6: pos.append(E + ' Noyau %s : diamètre %s au lieu de %d' % (n['qui'], n['svg'] and round(n['svg']['w'],1), d))
                    if n['vis'] and abs(n['vis']['w']-ph) > 0.6: pos.append(E + ' Noyau %s : visage %.1f au lieu de %d' % (n['qui'], n['vis']['w'], ph))
                    if n['pisteSw'] != arc: sty.append(E + ' Noyau %s : trait %s au lieu de %d' % (n['qui'], n['pisteSw'], arc))
                    if hexa(n['piste']) != PISTE[th]: sty.append(E + ' Noyau %s : piste %s au lieu de %s (NEUTRE)' % (n['qui'], hexa(n['piste']), PISTE[th]))
                    for a in n['arcs']:
                        if a['col'].upper() not in ETA: sty.append(E + ' Noyau %s : arc %s hors des trois états' % (n['qui'], a['col']))
                    ls = n['lbs']; fwA, fsA = ('700', 14) if n['moi'] else ('600', 13.5)
                    if ls['ff'] != 'Bricolage' or ls['fw'] != fwA or abs(ls['fs']-fsA) > 0.2:
                        sty.append(E + ' prénom %s : %s %s %.1f' % (n['qui'], ls['ff'], ls['fw'], ls['fs']))
                    if n['lb'] and n['svg'] and abs(n['lb']['y'] - n['svg']['b'] - 11) > 1:
                        pos.append(E + ' prénom %s : %.1f px sous l\'anneau au lieu de 11' % (n['qui'], n['lb']['y']-n['svg']['b']))
                    if n['lb']: bases.append(n['lb']['b'])
                    if i > 0 and N[i-1]['col'] and n['col']:
                        ga = n['col']['x'] - N[i-1]['col']['r']
                        ref = K['gapToi'] if i == 1 else K['gapPers']
                        if abs(ga-ref) > 1: pos.append(E + ' écart avant %s : %.1f au lieu de %d' % (n['qui'], ga, ref))
                if bases and max(bases)-min(bases) > 0.6: pos.append(E + ' les prénoms ne sont pas sur la même ligne de base (%.1f)' % (max(bases)-min(bases)))
                g, s = m['lg']['g'], m['lg']['s']
                if not g or abs(g['y']-exp_lg) > TOL or abs(g['h']-K['lgH']) > 1: pos.append(E + ' la légende %s au lieu de y %.1f' % (g and (round(g['y'],1), round(g['h'],1)), exp_lg))
                if [x['t'] for x in m['lg']['items']] != ['tenues', 'en cours', 'à tenir']: sty.append(E + ' la légende ne nomme pas les trois arcs')
                if [hexa(x['c']) for x in m['lg']['items']] != ETA: sty.append(E + ' la légende : pastilles %s' % [hexa(x['c']) for x in m['lg']['items']])
                if hexa(s['col']) != gris: sty.append(E + ' la légende : couleur %s au lieu de %s' % (hexa(s['col']), gris))
                if comp['moisson']:
                    if m['lg']['centre'] != '.au-nx|.au-mo h3': pos.append(E + ' la légende ne se déclare pas centrée (data-centre-entre)')
                    if g and m['h3']['g'] and N:
                        ha = g['y'] - max(n['lb']['b'] for n in N if n['lb'])
                        hb = m['h3']['g']['y'] - g['b']
                        if abs(ha-hb) > 1: pos.append(E + ' la légende n\'est pas centrée : %.1f au-dessus, %.1f en dessous' % (ha, hb))
                    g, s = m['h3']['g'], m['h3']['s']
                    if not g or abs(g['y']-exp_mo) > TOL: pos.append(E + ' « Ce que tu as tenu » à %s au lieu de %.1f' % (g and round(g['y'],1), exp_mo))
                    if m['h3']['t'] != 'Ce que tu as tenu': sty.append(E + ' le titre : « %s »' % m['h3']['t'])
                    if s['tt'] != 'uppercase' or s['fw'] != '700' or abs(s['fs']-13) > 0.2 or hexa(s['col']) != gris:
                        sty.append(E + ' le titre : %s %s %.1f %s' % (s['tt'], s['fw'], s['fs'], hexa(s['col'])))
                    # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (Tom, Q187) : trois dalles → jusqu'à six, deux rangées.
                    #   Original : sauvegardes/releve-aura-avant-colonne.py
                    att = min(MOISSON, comp['n']) if comp['n'] >= RANG2 else min(3, comp['n'])
                    if len(m['cells']) != att: pos.append(E + ' %d dalles tenues au lieu de %d (%d tenues ; seconde rangée dès %d)' % (len(m['cells']), att, comp['n'], RANG2))
                    for c in m['cells']:
                        if not c['cv'] or c['cv']['w'] > 101.5 or c['cv']['h'] > 64.5: pos.append(E + ' une dalle tenue sort de sa boîte : %s' % (c['cv'] and (round(c['cv']['w']), round(c['cv']['h']))))
                        if c['peint'] < 30: peint.append(E + ' la dalle tenue « %s » n\'est PAS peinte (%d)' % (c['t'], c['peint']))
                        if c['op'] != 1 or c['fi'] not in ('none', ''): peint.append(E + ' la dalle « %s » porte un voile ou un filtre (§4 règle 3)' % c['t'])
                        if c['sps']['fs'] < 12: sty.append(E + ' libellé sous 12 px (§6)')
            else:
                if not m['inv']['g'] or not m['inv']['g']['vis']: pos.append(E + ' l\'état vide n\'a pas sa phrase')
            # le bouton : 28 sous les libellés des dalles (ou sous la légende sans dalles), jamais plus haut que 762
            exp_bt = K['bt'][1]
            if not vide and comp['moisson'] and [c for c in m['cells'] if c['sp']]:
                exp_bt = max(K['bt'][1], max(c['sp']['b'] for c in m['cells'] if c['sp']) + AIR_BLOC)
            elif not vide:
                exp_bt = max(K['bt'][1], exp_lg + K['lgH'] + AIR_BLOC)
            if not vide and exp_bt + K['bt'][3] > PLI - MARGE_BAS and exp_bt < PLI:
                exp_bt = PLI        # Q186 : jamais coupé par le pli — il tombe franchement dessous
            g, s = m['bt']['g'], m['bt']['s']
            if not g or max(abs(g['x']-K['bt'][0]), abs(g['y']-exp_bt), abs(g['w']-K['bt'][2]), abs(g['h']-K['bt'][3])) > TOL:
                pos.append(E + ' le bouton %s au lieu de (24, %.1f, 342, 60)' % (g and (round(g['x']), round(g['y'],1), round(g['w']), round(g['h'])), exp_bt))
            if m['bt']['t'] != 'Partager mon Noyau': sty.append(E + ' le bouton : « %s »' % m['bt']['t'])
            if s['bw'] != '2px' or hexa(s['bc']) != encre or s['br'] != '30px':
                sty.append(E + ' le bouton : trait %s %s rayon %s (grammaire : 2 px, couleur du corps, h/2)' % (s['bw'], hexa(s['bc']), s['br']))
            # ═══ 9 · L'AIR DE LA COLONNE — les CINQ phrases, aux boîtes ET à l'encre ═══════════════
            #   Un contrôle d'air qui ne regarde que des paires de TEXTES ne voit pas une phrase qui
            #   touche une rangée de disques : ici, chaque bloc de la colonne, texte ou non.
            if not vide:
                fondRGB = [22, 23, 27] if th == 'dark' else [244, 238, 225]
                sous, rec = [], {}
                for i in range(5):
                    pg.evaluate(POSE_MOT, i); pg.wait_for_timeout(250)
                    a = pg.evaluate(AIRM)
                    g1 = a['disques'] - a['mot_bas']; sous.append((a['lignes'], g1))
                    if g1 < AIR_MIN: air.append(E + ' « %s » (%d ligne(s)) : %.1f pt entre la phrase et les disques (air décidé %.1f)' % (a['texte'][:28], a['lignes'], g1, AIR_MOT))
                    g2, g3 = a['lg_h'] - a['prenoms'], (a['h3'] - a['lg_b']) if a['h3'] is not None else None
                    if g2 < AIR_MIN or (g3 is not None and (g3 < AIR_MIN or abs(g2 - g3) > 1)):
                        air.append(E + ' « %s » : légende à %.1f sous les prénoms, %s au-dessus du titre' % (a['texte'][:28], g2, g3 is not None and round(g3, 1)))
                    if a['lib'] is not None and a['bt_h'] - a['lib'] < AIR_MIN:
                        air.append(E + ' « %s » : %.1f pt entre les libellés des dalles et le bouton' % (a['texte'][:28], a['bt_h'] - a['lib']))
                    # Q186 · à l'ouverture (défilement 0), le bouton est ENTIER avec sa marge ou ABSENT
                    visible = max(0.0, min(a['bt_b'], PLI) - max(a['bt_h'], 100.0))
                    if not (visible <= 0.5 or a['bt_b'] <= PLI - MARGE_BAS + 0.5):
                        air.append(E + ' « %s » : le bouton est COUPÉ par le bas de l\'écran à l\'ouverture — %.1f pt visibles sur 60' % (a['texte'][:28], visible))
                    # Q187 · LE FOND NU TRAHIT : à l'ouverture, s'il y a plus d'une rangée de dalles, le bord de
                    #   l'écran doit en COUPER une — sinon, sous les derniers libellés, du vide qui dit « c'est fini ».
                    if len(a['cells']) > 3:
                        if not any(c0 < PLI < c1 for c0, c1 in a['cells']):
                            bas = max(c1 for c0, c1 in a['cells'] if c1 <= PLI) if [1 for c0, c1 in a['cells'] if c1 <= PLI] else None
                            air.append(E + ' « %s » : à l\'ouverture, aucune dalle n\'est coupée par le bord — %s pt de fond nu sous la dernière rangée' % (a['texte'][:28], bas is not None and round(PLI - bas, 1)))
                    elif i == 0:
                        VAL.append(('composition %s' % E, '%d dalle(s) tenue(s) seulement : une seule rangée, rien à couper au pli — une question de COMPOSITION (Q188), pas d\'affordance' % len(a['cells'])))
                    if a['defil'] < a['bt_b'] + 20:
                        air.append(E + ' « %s » : le bouton n\'est pas atteignable en entier (fin du défilement %.0f, bas du bouton %.0f)' % (a['texte'][:28], a['defil'], a['bt_b']))
                    if i in (0, 1):   # à l'encre, sur l'image rendue — une phrase de deux lignes, une d'une
                        u = 'data:image/png;base64,' + base64.b64encode(pg.query_selector('#device').screenshot()).decode()
                        gi = pg.evaluate(ENCRE_GAP, [u, fondRGB, a['mot_bas']])
                        rec[a['lignes']] = gi
                        if gi < AIR_MIN: air.append(E + ' à l\'encre, « %s » : %.1f pt entre la phrase et les disques' % (a['texte'][:28], gi))
                    rec.setdefault('lib', a['bt_h'] - a['lib'] if a['lib'] is not None else None); rec['defil'] = a['defil'] - 844
                g1s = [x[1] for x in sous]
                if max(g1s) - min(g1s) > 1.5: air.append(E + ' l\'air sous la phrase dépend du nombre de lignes : %s' % ', '.join('%d l. %.1f' % x for x in sous))
                pr = pg.evaluate(PROTEGE)
                if pr['fautes']: air.append(E + ' défilé jusqu\'en bas, le cadre se voit au-dessus du plateau : %s' % pr['fautes'])
                if pr['enh_y'] is None or abs(pr['enh_y'] - 40) > 1: air.append(E + ' défilé, le plateau a bougé (y %s)' % pr['enh_y'])
                pg.evaluate(POSE_MOT, None); pg.wait_for_timeout(200)
                VAL.append(('air %s' % E, 'phrase → disques : %s · à l\'encre %s · libellés → bouton %.1f · la colonne défile de %.0f pt'
                            % (' · '.join('%d l. %.1f' % x for x in sous), ' · '.join('%s l. %.1f' % (k, v) for k, v in rec.items() if isinstance(k, int)),
                               rec['lib'] or -1, pr['defile'])))
            for t in m['textes']:
                if t['op'] < 0.72: sty.append(E + ' « %s » : opacité %.2f sous 72 %% (§6)' % (t['t'], t['op']))
                if t['fill'] != t['col']: sty.append(E + ' « %s » : -webkit-text-fill-color ≠ color (§3)' % t['t'])
                if t['fs'] < 12: sty.append(E + ' « %s » : %.1f px, sous 12 (§6)' % (t['t'], t['fs']))
                if '%' in t['t'] or t['t'].strip().replace(',', '').replace('.', '').isdigit():
                    sty.append(E + ' « %s » : un chiffre sur l\'Aura (l\'Aura sans chiffre, 10 sept.)' % t['t'])
            for c in pg.evaluate(COLL): coll.append(E + ' ' + c)
            for d in pg.evaluate(DEBORD): hors.append(E + ' ' + d)
            # ── présence peinte ──
            bo = pg.evaluate(BOULE)
            if not bo or bo['plein'] < 0.95: peint.append(E + ' la sphère n\'est pas pleine (%s)' % (bo and round(bo['plein'], 3)))
            if bo and bo['vide'] < 0.97: peint.append(E + ' le canevas n\'est pas transparent autour de la boule (%.3f)' % bo['vide'])
            if bo and bo['teinte'] is not None:
                ta = NAT_TEINTE[comp['nature']]; dt = min(abs(bo['teinte']-ta), 360-abs(bo['teinte']-ta))
                if dt > 22: peint.append(E + ' le sol est à %.0f° pour une nature %s (%d°)' % (bo['teinte'], comp['nature'], ta))
            if comp['ilesPeintes'] != comp['n']: peint.append(E + ' %d îles peintes pour %d paroles tenues' % (comp['ilesPeintes'], comp['n']))
            for n in m['noyaux']:
                if not n['visBg'] or n['visBg'] == 'none': peint.append(E + ' le visage de %s n\'a pas d\'image' % n['qui'])
            if VERBOSE: print(E, 'etat', json.dumps(e0)[:300])

        # ═══ 6 · LES VRAIES DONNÉES ════════════════════════════════════════════════════
        pg.evaluate("(t)=>setTheme(t)", 'dark'); pg.wait_for_timeout(300)
        pg.evaluate("""()=>{ window.__sauve=promises.map(p=>({p:p, s:p.status, c:p.chiche, n:p.nuee, d:p.draft, m:p.monde}));
                              window.__photo=USER.photo; }""")
        def restaure():
            pg.evaluate("""()=>{ (window.__sauve||[]).forEach(o=>{ o.p.status=o.s; o.p.chiche=o.c; o.p.nuee=o.n; o.p.draft=o.d; o.p.monde=o.m; });
                                 USER.photo=window.__photo; try{Toile.setPalette('signal');}catch(e){} }""")
        MIENS = "promises.filter(p=>!p.draft&&!p.req&&(!p.from||p.from==='moi')&&p.status==='tenu')"
        for nat, js in (('chiche', "p.chiche=true;"), ('nuee', "p.chiche=false; p.nuee=p.nuee||'famille';")):
            pg.evaluate("()=>{ %s.forEach(p=>{ %s }); }" % (MIENS, js))
            ouvre()
            c = pg.evaluate("()=>window._auraComp"); bo = pg.evaluate(BOULE)
            if c['nature'] != nat: don.append('nature majoritaire %s au lieu de %s' % (c['nature'], nat))
            if bo and bo['teinte'] is not None:
                dt = min(abs(bo['teinte']-NAT_TEINTE[nat]), 360-abs(bo['teinte']-NAT_TEINTE[nat]))
                if dt > 22: don.append('sol %s : teinte peinte %.0f° au lieu de ~%d°' % (nat, bo['teinte'], NAT_TEINTE[nat]))
            restaure()
        # égalité : Promi l'emporte (ordre du §3) ; zéro tenu : bleu
        pg.evaluate("()=>{ %s.forEach(p=>{ p.status='encours'; }); }" % MIENS)
        ouvre(); c = pg.evaluate("()=>window._auraComp")
        if c['n'] != 0 or c['nature'] != 'promi': don.append('à zéro parole tenue : n=%s, nature %s au lieu de promi (bleu)' % (c['n'], c['nature']))
        restaure()
        # le monde de la plantation : la plus récente passe en braille / océan
        pid = pg.evaluate("()=>{ const T=%s; const q=T[T.length-1]; q.monde={m:'braille',p:'ocean',h:0}; return q.id; }" % MIENS)
        ouvre(); c = pg.evaluate("()=>window._auraComp")
        il = [x for x in c['iles'] if x['pid'] == pid]
        if not il or il[0]['monde'][:2] != ['braille', 'ocean']: don.append('l\'île du Promi %s ne porte pas son monde de plantation : %s' % (pid, il and il[0]['monde']))
        col = pg.evaluate("""(pid)=>{ const cv=document.querySelector('#auraScreen .au-bx canvas[data-pid="'+pid+'"]'); if(!cv) return null;
            const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; const OC=[[74,176,196],[58,110,196],[122,206,180],[168,140,224]],
            SI=[[208,176,255],[58,84,255],[240,122,46],[143,160,255]]; let o=0,s=0;
            for(let i=0;i<d.length;i+=4){ if(d[i+3]<200) continue; const P=[d[i],d[i+1],d[i+2]];
              const dm=L=>Math.min(...L.map(c=>Math.hypot(c[0]-P[0],c[1]-P[1],c[2]-P[2]))); if(dm(OC)<dm(SI)) o++; else s++; }
            return {ocean:o, signal:s}; }""", pid)
        if not col or col['ocean'] <= col['signal']: don.append('la dalle tenue %s ne sort pas dans la palette de SA plantation (océan) : %s' % (pid, col))
        restaure()
        # le Studio change de palette : les dalles déjà plantées ne bougent pas
        # (⚠ on ROUVRE d'abord : la composition publiée est celle de la DERNIÈRE ouverture —
        #  la lire après une restauration, c'est comparer un état périmé)
        ouvre()
        m0 = [x['monde'] for x in pg.evaluate("()=>window._auraComp")['iles']]
        pg.evaluate("()=>{try{Toile.setPalette('ocean');}catch(e){}}"); ouvre()
        m1 = [x['monde'] for x in pg.evaluate("()=>window._auraComp")['iles']]
        if m0 != m1: don.append('changer de palette au Studio a changé le monde des dalles déjà plantées')
        restaure()
        # la vraie photo
        pg.evaluate("""()=>{ const c=document.createElement('canvas'); c.width=c.height=8; const g=c.getContext('2d');
                             g.fillStyle='#C0392B'; g.fillRect(0,0,8,8); USER.photo=c.toDataURL(); }""")
        ouvre()
        ph = pg.evaluate("()=>{const v=document.querySelector('#auraScreen .au-moi .au-vis');return v?{bg:getComputedStyle(v).backgroundImage.slice(0,30),p:v.getAttribute('data-photo')}:null;}")
        if not ph or 'data:image' not in ph['bg'] or ph['p'] != '1': don.append('« toi » ne prend pas la vraie photo : %s' % ph)
        restaure()
        # l'état vide
        pg.evaluate("()=>{ promises.forEach(p=>{ p.draft=true; }); }")
        ouvre(); m = pg.evaluate(MESURE, 'dark'); bo = pg.evaluate(BOULE)
        if not (m['inv']['g'] and m['inv']['g']['vis']) or 'La première parole' not in (m['inv']['t'] or ''):
            don.append('l\'état vide ne porte pas sa phrase')
        if m['nx']['g'] and m['nx']['g']['vis']: don.append('l\'état vide montre encore les Noyaux')
        if not bo or bo['plein'] < 0.95: peint.append('[vide] la sphère vide n\'est pas pleine — elle doit être belle à zéro')
        restaure()

        # ═══ 7 · LES HUIT ACQUIS — joués au vrai pointeur, dans l'app ═══════════════════
        #   le thème des acquis : sombre par défaut ; THEME_ACQUIS=light pour les rejouer en clair
        TH_A = os.environ.get('THEME_ACQUIS', 'dark')
        pg.evaluate("(t)=>setTheme(t)", TH_A); pg.wait_for_timeout(300)
        ouvre(); pg.wait_for_timeout(600)
        G = pg.evaluate("()=>_aura.G")
        attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan;}", 12000)
        # 1 · la rotation lente, qui ne s'arrête jamais
        a = pg.evaluate("()=>_aura.etat().lac"); pg.wait_for_timeout(2000); b1 = pg.evaluate("()=>_aura.etat().lac")
        v1 = (b1 - a) / 2.0
        VAL.append(('1 · rotation lente', '%.4f rad/s sur 2 s (décidé %.4f, un tour en 2 min)' % (v1, AUTO_DECIDE)))
        if abs(G['AUTO'] - AUTO_DECIDE) > 1e-6: acq.append('1 · l\'app déclare %.4f rad/s au lieu de la vitesse décidée %.4f' % (G['AUTO'], AUTO_DECIDE))
        if not (0.6 * AUTO_DECIDE < v1 < 1.6 * AUTO_DECIDE): acq.append('1 · la rotation lente : %.4f rad/s au lieu de %.4f' % (v1, AUTO_DECIDE))
        bb = boule(); cx, cy, sc = bb['cx'], bb['cy'], bb['sc']
        # 2 · la prise au doigt, dans tous les sens
        for nom, dx, dy in (('droite', 60, 0), ('bas', 0, 40), ('diagonale', -45, -30)):
            e0 = pg.evaluate("()=>_aura.etat()")
            pg.mouse.move(cx, cy); pg.mouse.down()
            for k in range(1, 13):
                pg.mouse.move(cx + dx * sc * k / 12, cy + dy * sc * k / 12); pg.wait_for_timeout(40)
            e1 = pg.evaluate("()=>_aura.etat()")
            pg.wait_for_timeout(200); pg.mouse.up(); pg.wait_for_timeout(150)
            dl, dt_ = e1['lac'] - e0['lac'], e1['tan'] - e0['tan']
            wl, wt = dx * G['SENS'], -dy * G['SENS']
            okl = (abs(dx) < 1 and abs(dl) < 0.06) or (abs(dx) >= 1 and dl * wl > 0 and abs(dl - wl) < 0.25 * abs(wl) + 0.05)
            okt = (abs(dy) < 1 and abs(dt_) < 0.02) or (abs(dy) >= 1 and dt_ * wt > 0 and abs(dt_ - wt) < 0.25 * abs(wt) + 0.03)
            VAL.append(('2 · prise, %s' % nom, 'Δlac %+.3f (attendu %+.3f) · Δtan %+.3f (attendu %+.3f)' % (dl, wl, dt_, wt)))
            if not (okl and okt): acq.append('2 · la prise (%s) : Δlac %.3f (attendu %.3f), Δtan %.3f (attendu %.3f)' % (nom, dl, wl, dt_, wt))
            attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp;}", 12000)
        # 3 · l'élan, qui se rend à la rotation lente SANS SACCADE — un vrai lancer (LANCE)
        la3 = pg.evaluate(LANCE, [cx - 70 * sc, cy, 132 * sc, 6, 16, 0])
        # 6,5 s : parti de VMAX, l'élan passe sous sa coupure en 4,3 à 5,2 s (planche)
        rec = pg.evaluate(ENREG, 6500)
        if VERBOSE: print('   élan au lâcher', la3['elan'])
        v = [r[2] for r in rec]
        if not rec or v[0] < 1.0: acq.append('3 · l\'élan : vitesse au lâcher %.2f rad/s (attendu > 1)' % (v[0] if v else -1))
        mont = all(rec[i+1][1] > rec[i][1] for i in range(len(rec)-1))
        dec = all(v[i+1] <= v[i] + 1e-9 for i in range(len(v)-1))
        # ⚑ UNE SACCADE EST UNE RUPTURE DE VITESSE, PAS UNE IMAGE LONGUE. Première rédaction :
        #   « la vitesse ne chute pas de plus de 10 % en une image » — elle prenait une image de
        #   100 ms (ramasse-miettes, une minuterie de l'app) pour une saccade, alors que 100 ms
        #   de temps réel s'étaient bel et bien écoulées et que la vitesse suivait sa loi. La
        #   règle de l'acquis est la CONTINUITÉ : chaque vitesse suit v·exp(−Δt/0,55) sur le
        #   temps réellement écoulé (borné à 100 ms comme la boucle). Une remise brutale à zéro
        #   ou à la rotation lente s'en écarte, et c'est elle qu'on prend. La plus longue image
        #   de l'élan est publiée à part : une image longue se voit, elle ne se cache pas.
        import math
        saut, lg, lgp, manq = 0.0, 0.0, 0.0, 0
        for i in range(len(v) - 1):
            dtb = rec[i+1][4]                       # le pas de LA BOUCLE pour cette image
            if dtb * 1000 > lg: lg, lgp = dtb * 1000, (rec[i+1][5] or 0)
            if rec[i+1][7] != 1: manq += 1; continue   # image manquée : on ne modélise pas
            if v[i] < 0.002: continue
            att = v[i] * math.exp(-min(0.1, dtb) / G['TAU'])
            saut = max(saut, abs(v[i+1] - att) - (0.03 * v[i] + 0.002))
        den_elan = ('plus longue image pendant l\'élan : %.0f ms (dont peintre %.1f ms), %d image(s) non échantillonnée(s)'
                    % (lg, lgp, manq))
        if not mont: acq.append('3 · l\'élan : la sphère s\'est arrêtée ou a reculé')
        if not dec: acq.append('3 · l\'élan : la vitesse d\'élan remonte')
        if saut > 0: acq.append('3 · l\'élan : une SACCADE — la vitesse s\'écarte de sa loi de %.3f rad/s' % saut)
        tail = [r for r in rec if r[8] > rec[-1][8] - 1000]
        if len(tail) > 5:
            vt = (tail[-1][1] - tail[0][1]) / ((tail[-1][8] - tail[0][8]) / 1000)
            if not (0.6 * AUTO_DECIDE < vt < 1.6 * AUTO_DECIDE) or tail[-1][2] != 0:
                acq.append('3 · après l\'élan : %.4f rad/s (élan %.4f) au lieu de la rotation lente %.4f' % (vt, tail[-1][2], AUTO_DECIDE))
        _tz = next((r[8] for r in rec if r[2] == 0), None)
        VAL.append(('3 · élan', 'au lâcher %.2f rad/s · éteint à %s s · puis %s rad/s · écart max à la loi %.4f rad/s · %s'
                    % (v[0] if v else -1, ('%.1f' % (_tz / 1000)) if _tz else '—',
                       ('%.4f' % vt) if len(tail) > 5 else '—', max(saut, 0), den_elan)))
        # 4 · le toucher qui creuse, résiste, et revient — à vue figée
        attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp;}", 12000)
        # ⚠ la référence est l'objet NEUF : les glissements des tests 2 et 3 ont eux-mêmes
        #   laissé des caresses, et un relissage efface TOUT — on ne pourrait jamais y revenir
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); const e=_aura.etat(); window.__vue=[e.lac,e.tan];}")
        peintes(3); pg.evaluate(SNAP, 'repos'); peintes(2); pg.evaluate(SNAP, 'repos2')
        # ⚠ la pulpe se CALCULE pour cette boule : a = 46,4 pt / 116 pt = 0,40, et la cuvette
        #   (2/π)·asin(a/r) porte jusqu'à trois fois a (1,2 rad). La zone témoin est donc
        #   posée HORS de portée (1,31 rad), sinon on mesure la cuvette et on la prend pour
        #   du bruit.
        tx, ty = -0.40, -0.30
        pg.mouse.move(cx + tx * bb['R'], cy + ty * bb['R']); pg.mouse.down(); pg.wait_for_timeout(250)
        p1 = pg.evaluate("()=>_aura.etat().emp"); pg.evaluate(SNAP, 'doigt')
        pg.wait_for_timeout(700); p2 = pg.evaluate("()=>_aura.etat().emp")
        pg.mouse.up()
        loc = pg.evaluate(DIFF, ['repos', 'doigt', [tx, ty, 0.35]]); far = pg.evaluate(DIFF, ['repos', 'doigt', [0.5, 0.5, 0.2]])
        bruit = pg.evaluate(DIFF, ['repos', 'repos2', [tx, ty, 0.35]])
        if bruit is None: acq.append('4 · la mesure elle-même a échoué (deux instantanés au repos incomparables)')
        if not p1 or p1['p'] < 0.99: acq.append('4 · le toucher ne creuse pas (p = %s à 250 ms)' % (p1 and round(p1['p'], 3)))
        if not p2 or abs(p2['p'] - 1) > 1e-6: acq.append('4 · le creux ne RÉSISTE pas : p = %s à 950 ms (il doit tenir son plateau)' % (p2 and p2['p']))
        if loc is None or loc < 0.10 or loc < 4 * max(far or 0, bruit or 0, 0.005): acq.append('4 · le creux ne se voit pas : %.3f sous le doigt, %.3f hors de portée (bruit %.3f)' % (loc or -1, far or -1, bruit or -1))
        # ⚑ LE RETOUR EST CONTINU JUSQU'AU BOUT (Tom, 10 sept. : « la dernière étape avant que la
        #   sphère ne redevienne lisse saute — ça passe de trop loin encore déformé à net d'un coup »).
        #   On enregistre DANS LA PAGE chaque image peinte du retour (vue figée), et on mesure le
        #   PAS d'une image à la suivante EN AMPLITUDE : l'écart moyen, en niveaux (0–255), sur la
        #   zone du doigt. LE DERNIER PAS — de la dernière image où l'empreinte existe à la première
        #   image lisse — ne doit pas dépasser 3 fois la médiane des 10 pas qui le précèdent
        #   (plancher 0,5 niveau). Un retour fini est un retour dont la dernière marche ressemble
        #   aux autres.
        #   ⚠ PAS EN PART DE PIXELS : la première écriture comptait les pixels qui changent. Un
        #   retour lisse en change déjà beaucoup, d'un rien, à chaque image (médiane 17 %) — et le
        #   saut de l'ancienne version (44 %) passait dessous. Prouvé : ce contrôle-là était VERT
        #   sur la version fautive. Celui-ci mord (voir l'ÉTAT DES LIEUX, 4 quater).
        seq4 = pg.evaluate(REC_RETOUR, [tx, ty])
        if os.environ.get('RETOUR_DUMP'): io.open(os.environ['RETOUR_DUMP'], 'w', encoding='utf-8').write(repr(seq4))
        ok = bool(seq4) and seq4[-1][1] is None
        _i0 = next((k for k, r in enumerate(seq4) if r[1] is None), None)
        _d4 = (seq4[_i0][0] / 1000.0) if _i0 is not None else -1
        saut4 = seq4[_i0][4] if _i0 else None
        _av = sorted(r[4] for r in seq4[max(1, (_i0 or 0) - 10):(_i0 or 0)] if r[4] is not None)
        med4 = _av[len(_av) // 2] if _av else 0
        #   ET UN PLAFOND ABSOLU : 1 niveau. La règle relative seule ne prenait la version fautive
        #   qu'à 3,5 fois la médiane pour un seuil à 3 — un contrat à marge mince oscille. Le
        #   dernier pas EST l'écart au repos qui restait : au-delà d'un niveau, on l'enlève visible.
        if saut4 is None or saut4 > min(1.0, max(0.5, 3 * med4)):
            acq.append('4 · le retour SAUTE à la fin : la dernière image change la zone de %.2f niveaux en moyenne (les 10 pas d\'avant : médiane %.2f) — déformé → lisse d\'un coup'
                       % (saut4 if saut4 is not None else -1, med4))
        peintes(3); pg.evaluate(SNAP, 'revenu')
        rev = pg.evaluate(DIFF, ['repos', 'revenu', [tx, ty, 0.35]])
        _av0 = [r for r in seq4[:_i0]] if _i0 else seq4
        _pas = [_av0[int(k * (len(_av0) - 1) / 5)] for k in range(6)] if len(_av0) >= 6 else _av0
        VAL.append(('4 · retour', 'écart au repos (niveaux) : ' + ' → '.join('%.1f' % r[5] for r in _pas)
                    + ' → lisse · DERNIER PAS %.2f niveau (médiane des 10 d\'avant %.2f) · %d images · empreinte retirée à %.2f s'
                    % (saut4 if saut4 is not None else -1, med4, len(seq4), _d4)))
        VAL.append(('4 · toucher', 'p %.3f à 250 ms, %.3f à 950 ms · sous le doigt %.1f %% des pixels changent, hors de portée %.2f %%, bruit %.2f %% · revenu ≈ %.1f s après le lâcher, écart au repos %.2f %%'
                    % ((p1 or {}).get('p', -1), (p2 or {}).get('p', -1), 100 * (loc or 0), 100 * (far or 0), 100 * (bruit or 0), _d4, 100 * (rev or 0))))
        if not ok: acq.append('4 · le creux ne revient pas en 9 s')
        elif rev is None or rev > max(0.02, 2 * (bruit or 0)): acq.append('4 · la matière n\'est pas revenue : %.3f des pixels diffèrent encore' % (rev or -1))
        # 5 · la trace qui reste
        n0 = pg.evaluate("()=>_aura.etat().traces")
        pg.mouse.move(cx - 0.5 * bb['R'], cy + 0.1 * bb['R']); pg.mouse.down()
        for k in range(1, 21): pg.mouse.move(cx - 0.5 * bb['R'] + k * 0.05 * bb['R'], cy + 0.1 * bb['R']); pg.wait_for_timeout(35)
        pg.wait_for_timeout(150); pg.mouse.up()
        # la caresse s'inscrit AU REPOS (doigt levé, élan éteint, creux refermé) — jamais au
        # lâcher, où refaire le cache ferait une saccade
        a1 = pg.evaluate("()=>_aura.etat().attente")
        attends("()=>_aura.etat().traces>%d" % n0, 15000)
        n1 = pg.evaluate("()=>_aura.etat().traces")
        if a1 < 1: acq.append('5 · la caresse n\'est pas mise en attente au lâcher (%s)' % a1)
        ls = pg.evaluate("()=>{try{return JSON.parse(localStorage.getItem('promi_orbite_traces')||'[]').length;}catch(e){return -1;}}")
        if n1 != n0 + 1: acq.append('5 · la trace : %d caresse(s) avant, %d après (une de plus attendue)' % (n0, n1))
        if ls != n1: acq.append('5 · la trace n\'est pas gardée (localStorage %s, mémoire %s)' % (ls, n1))
        attends("()=>!_aura.etat().emp", 15000)
        pg.evaluate("()=>_aura.vue(window.__vue[0],window.__vue[1])"); peintes(3)
        pg.evaluate(SNAP, 'trace')
        tr = pg.evaluate(DIFF, ['repos', 'trace', None])
        VAL.append(('5 · trace', 'en attente au lâcher : %s · %d → %d caresse(s), gardée(s) : %s · au repos, %.1f %% des pixels portent la caresse'
                    % (a1, n0, n1, ls, 100 * (tr or 0))))
        if tr is None or tr < 0.01: acq.append('5 · la trace ne se voit pas au repos : %.4f des pixels' % (tr or -1))
        # 7 · le geste qui relisse tout — deux touchers rapprochés
        pg.mouse.click(cx + 0.3 * bb['R'], cy + 0.3 * bb['R']); pg.wait_for_timeout(120)
        pg.mouse.click(cx + 0.3 * bb['R'], cy + 0.3 * bb['R'])
        n2 = pg.evaluate("()=>_aura.etat().traces")
        if n2 != 0: acq.append('7 · deux touchers rapprochés ne relissent pas (%d caresses restent)' % n2)
        attends("()=>!_aura.etat().emp", 15000)
        pg.evaluate("()=>_aura.vue(window.__vue[0],window.__vue[1])"); peintes(3)
        pg.evaluate(SNAP, 'relisse')
        rl = pg.evaluate(DIFF, ['repos', 'relisse', None])
        VAL.append(('7 · relisse', 'deux touchers à 120 ms : %d caresse restante · écart à l\'objet neuf %.3f %% des pixels' % (n2, 100 * (rl or 0))))
        if rl is None or rl > max(0.01, 2 * (bruit or 0)): acq.append('7 · relissé, le velours n\'est pas revenu à neuf : %.4f des pixels' % (rl or -1))
        pg.evaluate("()=>_aura.fige(false)")
        # 6 · le comblement du creux au lancer
        def vie(lance):
            attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp;}", 12000)
            # le même geste dans les deux cas : on appuie 300 ms (le creux à fond), puis on
            # lâche sur place — ou on LANCE (six pas de 14 pt toutes les 16 ms)
            r = pg.evaluate(LANCE, [cx, cy, 84 * sc if lance else 0, 6 if lance else 0, 16, 300])
            attends("()=>!_aura.etat().emp", 20000)
            return (pg.evaluate("()=>performance.now()") - r['t']) / 1000.0
        va, vb = vie(False), vie(True)
        VAL.append(('6 · comblement', 'le creux vit %.2f s lâché sur place, %.2f s lancé (%.0f %%)' % (va, vb, 100 * vb / max(va, 1e-6))))
        if not (vb < 0.6 * va): acq.append('6 · le lancer ne comble pas : %.2f s sans lancer, %.2f s en lançant' % (va, vb))
        # 8 · un toucher ouvre la personne, un glissement tourne
        attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp;}", 12000)
        pers = pg.evaluate("""()=>{const n=document.querySelector('#auraScreen .au-gp .au-n'); if(!n) return null;
            const r=n.querySelector('.au-nb').getBoundingClientRect(); return {qui:n.getAttribute('data-qui'), x:r.left+r.width/2, y:r.top+r.height/2};}""")
        if not pers: acq.append('8 · aucune personne dans la rangée pour tester le toucher')
        else:
            pg.evaluate("()=>{window._auraOuvre=null;}")
            pg.mouse.move(pers['x'], pers['y']); pg.mouse.down(); pg.mouse.move(pers['x'] + 30 * sc, pers['y'], steps=6); pg.mouse.up()
            pg.wait_for_timeout(300)
            _g8 = pg.evaluate("()=>window._auraOuvre")
            if _g8: acq.append('8 · un GLISSEMENT sur la rangée a ouvert une personne')
            pg.mouse.click(pers['x'], pers['y']); pg.wait_for_timeout(700)
            o = pg.evaluate("()=>({qui:window._auraOuvre, sheet:!!document.querySelector('#personSheet.show')})")
            if o['qui'] != pers['qui'] or not o['sheet']: acq.append('8 · un toucher sur %s n\'ouvre pas sa personne : %s' % (pers['qui'], o))
            pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(300)
            pg.evaluate("()=>{window._auraOuvre=null;}")
            la = pg.evaluate("()=>_aura.etat().lac")
            pg.mouse.move(cx - 40 * sc, cy); pg.mouse.down(); pg.mouse.move(cx + 40 * sc, cy, steps=10); pg.mouse.up()
            lb = pg.evaluate("()=>_aura.etat().lac")
            if lb - la < 0.3 or pg.evaluate("()=>window._auraOuvre"): acq.append('8 · un glissement sur la sphère ne tourne pas (Δ %.3f) ou ouvre quelqu\'un' % (lb - la))
            VAL.append(('8 · personne', 'toucher sur « %s » → ouvre « %s », fiche %s · glissement de 30 pt sur la rangée → %s · glissement de 80 pt sur la sphère → Δlac %.2f rad, personne d\'ouvert'
                        % (pers['qui'], o['qui'], 'affichée' if o['sheet'] else 'ABSENTE', ('ouvre « %s »' % _g8) if _g8 else 'n\'ouvre rien', lb - la)))
        # la croissance : une parole de plus, l'Orbite fait UN TOUR pour l'amener au centre
        c = pg.evaluate("()=>window._auraComp")
        if c['n'] > 0:
            pg.evaluate("(n)=>localStorage.setItem('promi_orbite_vus', JSON.stringify(n-1))", c['n'])
            e = ouvre()
            if not e or e['tour'] != c['n']: acq.append('la croissance : l\'Orbite ne fait pas son tour (%s)' % (e and e['tour']))
            attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan;}", 12000)
            z = pg.evaluate("""()=>{ const e=_aura.etat(), c=_auraComp.derniere; if(!c) return null;
                const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan);
                const Zt=-c[0]*sl+c[2]*cl; return c[1]*st+Zt*ct; }""")
            if z is None or z < 0.85: acq.append('la croissance : après le tour, la dernière dalle n\'est pas face à toi (z = %s)' % z)
            VAL.append(('croissance', 'une parole de plus → tour %s · la dernière dalle finit face à toi, z = %.3f' % (e and e['tour'], z if z is not None else -1)))

        # ═══ 8 · LA DENSITÉ ═════════════════════════════════════════════════════════════
        e = pg.evaluate("()=>_aura.etat()")
        den_info = 'palier %s · médiane %s ms · %d images · %s' % (e['palier'], e['ms'] and round(e['ms'], 2), e['frames'], den_elan)
        if e['ms'] is None: den.append('aucune image mesurée')
        # ⚑ SOUS UN PROCESSEUR RALENTI ×6, LE RÉGULATEUR DÉCIDE DE CÉDER — MAIS RIEN NE CHANGE SOUS
        #   LES YEUX (Tom, 10 sept. : « il doit être imperceptible »). CONTRAT RÉÉCRIT au niveau de la
        #   décision : l'ancien exigeait que le palier DESCENDE pendant qu'on regarde. Or un palier est
        #   un autre semis — tous les poils changent de place d'un coup (76 à 80 % des pixels mesurés)
        #   — et il se déclenchait en plein élan. Désormais : le régulateur VISE plus bas (la décision
        #   est prise et gardée), le palier peint ne bouge pas d'une image tant que l'Aura est ouverte,
        #   et la vise s'applique à la réouverture. Les gestes, eux, restent — comme avant.
        #   Original : sauvegardes/releve-aura-avant-regulateur.py.
        cdp = pg.context.new_cdp_session(pg)
        pg.evaluate("()=>_aura.palier(0)")
        cdp.send('Emulation.setCPUThrottlingRate', {'rate': 6})
        c0 = e['cede']
        # chaque image peinte sous ×6 : quel palier ? jusqu'à 2 s APRÈS la décision (un changement
        # différé d'une image ou deux serait tout aussi visible)
        vus = pg.evaluate("""(ms)=>new Promise(res=>{ const P=new Set(), t0=performance.now(), c0=_aura.etat().cede; let td=0;
            (function f(){ const e=_aura.etat(), t=performance.now(); P.add(e.palier);
              if(!td && e.cede>c0) td=t;
              if((td && t-td>2000) || t-t0>ms) return res(Array.from(P)); requestAnimationFrame(f); })(); })""", 22000)
        e2 = pg.evaluate("()=>_aura.etat()")
        la = e2['lac']; pg.wait_for_timeout(1500); lb = pg.evaluate("()=>_aura.etat().lac")
        pg.mouse.move(cx - 30 * sc, cy); pg.mouse.down(); pg.mouse.move(cx + 30 * sc, cy, steps=6)
        lc = pg.evaluate("()=>_aura.etat().lac"); pg.mouse.up()
        vus += [pg.evaluate("()=>_aura.etat().palier")]
        cdp.send('Emulation.setCPUThrottlingRate', {'rate': 1})
        vus = sorted(set(vus), reverse=True)
        vise = e2.get('vise')
        if e2['cede'] <= c0: den.append('sous ×6, le régulateur n\'a pas décidé de céder (vise %s, médiane %s ms)' % (vise, e2['ms']))
        if vus != [110000]: den.append('sous ×6, le palier a changé SOUS LES YEUX : %s — tous les poils changent de place d\'un coup' % vus)
        if not vise or vise >= 110000: den.append('sous ×6, aucune vise plus basse n\'est gardée (vise %s)' % vise)
        if lb <= la: den.append('sous ×6, la rotation lente s\'est arrêtée — le COMPORTEMENT a cédé')
        if lc - lb < 0.1: den.append('sous ×6, le doigt ne tourne plus la sphère — le COMPORTEMENT a cédé')
        # la vise prend effet à la réouverture, pendant que l'écran se bâtit
        e3 = ouvre() or {}
        if vise and e3.get('palier') != vise: den.append('à la réouverture, le palier (%s) n\'a pas pris la vise (%s)' % (e3.get('palier'), vise))
        den_info += ' · sous ×6 : palier peint %s pendant qu\'on regarde, vise %s, %d décision(s) · à la réouverture : palier %s' % (
            '/'.join(str(x) for x in vus), vise, e2['cede'], e3.get('palier'))
        pg.evaluate("()=>{_aura.palier(0); try{localStorage.removeItem('promi_orbite_palier');}catch(e){}}")

        if er: peint.append('ERREURS JS : ' + ' | '.join(er[:3]))
        b.close()

    print("\n═══ L'AURA — l'Orbite dans l'app, deux thèmes ═══\n")
    tot = 0
    for nom, lst in (('écarts de position > 3 px', pos), ('écarts de style', sty), ('collisions', coll),
                     ('débordements', hors), ('présence peinte', peint), ('données', don),
                     ('les huit acquis', acq), ('densité', den), ('air de la colonne', air)):
        print('%-28s %d' % (nom, len(lst))); tot += len(lst)
        if lst and (VERBOSE or len(lst) <= 40):
            for l in lst: print('   ', l)
    print('\nLES VALEURS MESURÉES — acquis joués en thème %s' % ('sombre' if TH_A == 'dark' else 'clair'))
    for k, x in VAL: print('   %-20s %s' % (k, x))
    print('\n' + den_info)
    print('\n%s' % ('✅  L\'AURA AU VERT' if tot == 0 else '❌  %d ÉCARTS' % tot))
    return tot


if __name__ == '__main__':
    sys.exit(0 if juge() == 0 else 1)
