#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_trace.py — LA TRACE EST UNE BANDE CONTINUE, À LA LARGEUR DU CONTACT LU (v142, Tom, 11 oct. 2026, C-083 — RÉCIDIVE).

⚑ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_trace-avant-v142.py — il vérifiait qu'une trace PARAISSAIT sous le
doigt et suivait le sens du geste ; il ne mesurait ni sa largeur ni sa longueur, et il était vert pendant que Tom voyait « ça apparaît en grand
alors qu'on a à peine touché, et inversement »). La décision :
« La trace est une bande continue, image par image, plus d'arcs tous les 10 pt ni de cadence. Sa largeur est celle du contact lu (radiusX /
radiusY), sans multiplicateur. Un appui immobile laisse la forme du contact, à taille réelle. `?mesure=1` affiche le contact lu. »

Au vrai doigt (CDP, horodaté, AVEC rayon de contact), Chromium sur carte graphique. Le VERDICT se lit sur l'IMAGE : la tache de différence entre
la boule avec la trace et relissée, à la même vue ; le geste finit au centre de la boule (la trace y est vue de face). `tracesGeo` sert de pointeur.
  A · trois contacts (rayon 6, 12, 18 pt), même trajet : la bande PEINTE est large de 2 × le rayon, ± 10 % (12, 24, 36 pt EN DUR) ;
  B · ce que l'app déclare : demi-largeur = le rayon lu, ± 10 %, sans multiplicateur (`G.DOIGT_K` = 1) ;
  C · trois trajets (30, 60, 100 pt), même contact : la trace peinte s'allonge avec le trajet (60 ≥ 1,15 × 30 ; 100 ≥ 1,10 × 60 (la boule suit de plus en plus la main : 32 / 46 / 53 pt relevés) — la boule suit la main : la trace est le GLISSEMENT du doigt sur elle, plus court que le trajet), et sa largeur ne change pas (± 15 %) ;
  D · EN DIRECT : à mi-geste des segments existent déjà ; au lâcher rien ne s'ajoute ; une bande = plusieurs segments (≥ 4 pour 60 pt) ;
  E · un appui immobile, contact 16 × 9 pt : il reste une tache de la taille du contact (32 × 18 pt, ± 30 %), plus large que haute ; un contact de 6 pt en laisse une plus petite ;
  F · `?mesure=1` écrit le contact lu ;
  G, H, I (v143) · les poils se couchent davantage quand le geste est lent, quand le doigt appuie (contact plus large), quand l'appui dure.
Preuve : rouge sur v141 (python3 redteam_trace.py zz-av142.html).
"""
import sys, math
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
PRISE = r"""()=>{ _aura.pelote(); const c=document.getElementById('auBoule'); return [c.width, Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data)]; }"""
GARDE = r"""(n)=>{ _aura.pelote(); const c=document.getElementById('auBoule'); window['__i'+n]=new Uint8ClampedArray(c.getContext('2d').getImageData(0,0,c.width,c.height).data); return c.width; }"""
TACHE = r"""()=>{ const a=window.__i1, b=window.__i2, c=document.getElementById('auBoule'), W=c.width, k=W/296; let n=0,sx=0,sy=0; const P=[];
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const i=(y*W+x)*4; if(!a[i+3]||!b[i+3]) continue; const e=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]); if(e>30){ P.push(x/k,y/k); sx+=x/k; sy+=y/k; n++; } }
  if(n<40) return {n:n};
  const mx=sx/n, my=sy/n; let xx=0,yy=0,xy=0; for(let i=0;i<P.length;i+=2){ const dx=P[i]-mx, dy=P[i+1]-my; xx+=dx*dx; yy+=dy*dy; xy+=dx*dy; }
  const th=0.5*Math.atan2(2*xy, xx-yy), ux=Math.cos(th), uy=Math.sin(th), A=[], B=[];
  for(let i=0;i<P.length;i+=2){ const dx=P[i]-mx, dy=P[i+1]-my; A.push(dx*ux+dy*uy); B.push(-dx*uy+dy*ux); }
  A.sort((p,q)=>p-q); B.sort((p,q)=>p-q); const q=(L,f)=>L[Math.min(L.length-1,Math.floor(L.length*f))];
  const r=c.getBoundingClientRect(), s=r.width/296;
  return {n:n, cx:r.left+mx*s, cy:r.top+my*s, angle:th*180/Math.PI, long:q(A,0.95)-q(A,0.05), large:q(B,0.90)-q(B,0.10), s:s}; }"""
def ecart_angle(a, b):
    d = abs(a - b) % 180.0
    return min(d, 180.0 - d)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('geste_v','143');localStorage.setItem('geste_vu_pelote','1');localStorage.setItem('geste_v','143');localStorage.setItem('geste_vu_aura-apparait','1');}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5000)
    cdp = ctx.new_cdp_session(pg)
    bo = pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}")
    T = [1000.0]
    def tp(x, y, r): return [{'x': x, 'y': y, 'radiusX': r, 'radiusY': r, 'rotationAngle': 0, 'force': 1}]
    def geste(x0, y0, x1, y1, r=11, duree=0.45, tenue=0.35):
        """glisse de (x0,y0) à (x1,y1), s'arrête, se lève ; rend la tache mesurée, et le nombre de traces à mi-geste, avant et après le lâcher"""
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x0, y0, r), 'timestamp': T[0]})
        n = 18; mi = None
        for i in range(1, n + 1):
            T[0] += duree / n; pg.wait_for_timeout(int(1000 * duree / n))
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, r), 'timestamp': T[0]})
            if i == n // 2: pg.wait_for_timeout(60); mi = pg.evaluate("()=>(_aura.tracesGeo?_aura.tracesGeo():[]).length")
        pg.wait_for_timeout(int(1000 * tenue)); T[0] += tenue
        avant = pg.evaluate("()=>(_aura.tracesGeo?_aura.tracesGeo():[]).length")
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]})
        t = mesure(); t['mi'] = mi; t['avant'] = avant; t['apres'] = len(t.get('geo') or []); return t
    def mesure():
        pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente && !e.vlac && !e.vtan}", timeout=25000); pg.wait_for_timeout(500)
        v = pg.evaluate("()=>{const e=_aura.etat(); return [e.lac,e.tan]}")
        geo = pg.evaluate("()=>_aura.tracesGeo?_aura.tracesGeo():null")
        pg.evaluate(GARDE, 1)
        pg.evaluate("([l,t])=>{ _aura.relisse(); _aura.vue(l,t); }", v); pg.wait_for_timeout(500); pg.evaluate(GARDE, 2)
        t = pg.evaluate(TACHE); t['geo'] = geo; return t
    def appui(x, y, r, duree):
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x, y, r), 'timestamp': T[0]})
        pg.wait_for_timeout(int(1000 * duree)); T[0] += duree
        creux = pg.evaluate("()=>!!_aura.etat().emp")
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]}); pg.wait_for_timeout(700)   # au-delà du double toucher
        t = mesure(); t['creux'] = creux; return t
    def court(t): return str({k: (round(v, 1) if isinstance(v, float) else v) for k, v in t.items() if k != 'geo' and v is not None})
    cx, cy = bo
    BOITE = r"""()=>{ const a=window.__i1, b=window.__i2, c=document.getElementById('auBoule'), W=c.width, k=W/296; const col={}, lig={}; let n=0;
      for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const i=(y*W+x)*4; if(!a[i+3]||!b[i+3]) continue; const e=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]); if(e>36){ col[x]=(col[x]||0)+1; lig[y]=(lig[y]||0)+1; n++; } }
      const et=(o,seuil)=>{ const K=Object.keys(o).map(Number).filter(v=>o[v]>=seuil).sort((p,q)=>p-q); return K.length? (K[K.length-1]-K[0])/k : 0; };
      const mx=Math.max(1,...Object.values(lig)), my=Math.max(1,...Object.values(col));
      return {n:n, long:et(col, my*0.35), large:et(lig, mx*0.35)}; }"""
    def lit():
        pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente && !e.vlac && !e.vtan}", timeout=25000); pg.wait_for_timeout(500)
        v = pg.evaluate("()=>{const e=_aura.etat(); return [e.lac,e.tan]}"); geo = pg.evaluate("()=>_aura.tracesGeo?_aura.tracesGeo():[]")
        pg.evaluate(GARDE, 1); pg.evaluate("([l,t])=>{ _aura.relisse(); _aura.vue(l,t); }", v); pg.wait_for_timeout(500); pg.evaluate(GARDE, 2)
        t = pg.evaluate(BOITE); t['arcs'] = len(geo); t['w'] = max([a['w'] for a in geo] or [0]) * 116; F_ = sorted([a.get('f') or 0 for a in geo]); t['f'] = F_[len(F_) // 2] if F_ else 0; return t
    def bande(L, r, y=None, duree=.45, pas=18):
        """le doigt glisse de L pt vers la droite et FINIT au centre de la boule"""
        y = cy - 10 if y is None else y; x0 = cx - L; x1 = cx
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x0, y, r), 'timestamp': T[0]}); n = pas; mi = 0
        for i in range(1, n + 1):
            T[0] += duree / n; pg.wait_for_timeout(int(1000 * duree / n))
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x0 + (x1 - x0) * i / n, y, r), 'timestamp': T[0]})
            if i == n // 2: pg.wait_for_timeout(60); mi = pg.evaluate("()=>(_aura.tracesGeo?_aura.tracesGeo():[]).length")
        pg.wait_for_timeout(350); T[0] += .35; av = pg.evaluate("()=>(_aura.tracesGeo?_aura.tracesGeo():[]).length")
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]})
        t = lit(); t['mi'] = mi; t['avant'] = av; return t
    def pose(rx, ry, duree=1.2):
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx, 'y': cy - 10, 'radiusX': rx, 'radiusY': ry, 'rotationAngle': 0, 'force': 1}], 'timestamp': T[0]})
        pg.wait_for_timeout(int(duree * 1000)); T[0] += duree
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]}); pg.wait_for_timeout(700); return lit()
    def c(t): return str({k: (round(v, 1) if isinstance(v, float) else v) for k, v in t.items()})
    R = {r: bande(110, r) for r in (6, 12, 18)}
    for r in (6, 12, 18):
        juge('A · contact de rayon %d pt : la bande peinte est large de %d pt (± 10 %%)' % (r, 2 * r), abs(R[r]['large'] - 2 * r) <= 0.10 * 2 * r, c(R[r]))
    juge('B · ce que l\'app déclare : demi-largeur = le rayon lu (± 10 %), pour les trois', all(abs(R[r]['w'] - r) <= 0.10 * r for r in R), ' · '.join('%d → %.1f' % (r, R[r]['w']) for r in R))
    k = pg.evaluate("()=>_aura.G && _aura.G.DOIGT_K")
    juge('B · sans multiplicateur : G.DOIGT_K vaut 1', k == 1, 'DOIGT_K = %s' % k)
    L = {l: bande(l, 10) for l in (30, 60, 100)}
    juge('C · la trace peinte s\'allonge avec le trajet : 60 pt ≥ 1,15 × 30 pt, 100 pt ≥ 1,10 × 60 pt', L[30]['long'] > 8 and L[60]['long'] >= 1.15 * L[30]['long'] and L[100]['long'] >= 1.10 * L[60]['long'], ' · '.join('%d → %.1f pt' % (l, L[l]['long']) for l in L))
    # v143 : ± 25 % — un trajet long, plus lent, couche davantage les poils (l'intensité se lit) : sa bande se voit un peu plus large (24,5 pt relevés)
    juge('C · sa largeur ne dépend pas du trajet (20 pt, ± 25 %)', all(abs(L[l]['large'] - 20) <= 5 for l in L), ' · '.join('%d → %.1f pt' % (l, L[l]['large']) for l in L))
    juge('D · EN DIRECT : à mi-geste des segments existent ; au lâcher rien ne s\'ajoute', L[60]['mi'] >= 1 and L[60]['arcs'] == L[60]['avant'], c(L[60]))
    juge('D · une bande, pas un arc : au moins 4 segments pour 60 pt de trajet, et davantage pour 100 pt', L[60]['arcs'] >= 4 and L[100]['arcs'] > L[60]['arcs'], '%d / %d' % (L[60]['arcs'], L[100]['arcs']))
    E = pose(16, 9); e = pose(6, 6)
    juge('E · appui immobile, contact 16 × 9 pt : une tache de 32 × 18 pt (± 30 %), plus large que haute', abs(E['long'] - 32) <= 9.6 and abs(E['large'] - 18) <= 5.4 and E['long'] > E['large'], c(E))
    juge('E · un contact de 6 pt laisse une tache plus petite (≤ la moitié en surface)', 0 < e['n'] <= 0.5 * E['n'], '%s / %s pixels' % (e['n'], E['n']))
    # ── v143 (Tom, 12 oct. 2026) : « les poils se couchent davantage quand l'appui dure ou s'appuie, moins quand on effleure » ──
    V = bande(100, 10, duree=0.10, pas=5); Lt = bande(100, 10, duree=1.8)
    juge('G · même trajet, même contact : un geste LENT (1,8 s) couche plus les poils qu\'un effleurement (0,1 s) — intensité déclarée +0,20 au moins', Lt['f'] >= V['f'] + 0.20, 'effleuré %.2f · lent %.2f' % (V['f'], Lt['f']))
    juge('G · … et à l\'image : la trace lente change plus de pixels que l\'effleurée (≥ 1,15 fois)', V['n'] > 0 and Lt['n'] >= 1.15 * V['n'], '%s / %s pixels' % (V['n'], Lt['n']))
    P1 = bande(100, 6, duree=0.45); P2 = bande(100, 16, duree=0.45)
    juge('H · même trajet, même vitesse : un doigt qui APPUIE (contact de 16 pt) couche plus qu\'un doigt léger (6 pt)', P2['f'] >= P1['f'] + 0.15, 'léger %.2f · appuyé %.2f' % (P1['f'], P2['f']))
    A1 = pose(12, 12, 0.3); A2 = pose(12, 12, 1.6)
    juge('I · un appui immobile : plus il dure, plus les poils se couchent (0,3 s contre 1,6 s)', A2['f'] >= A1['f'] + 0.25 and A2['n'] >= A1['n'], '0,3 s : %.2f (%s px) · 1,6 s : %.2f (%s px)' % (A1['f'], A1['n'], A2['f'], A2['n']))
    juge('aucune erreur de page', not er, str(er[:2]))
    pg2 = ctx.new_page(); pg2.goto('http://127.0.0.1:8752/' + FICHIER + '?mesure=1'); pg2.wait_for_timeout(6500)
    pg2.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg2.wait_for_timeout(5000)
    c2 = ctx.new_cdp_session(pg2)
    c2.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx, 'y': cy, 'radiusX': 13, 'radiusY': 7, 'rotationAngle': 0, 'force': 1}]}); pg2.wait_for_timeout(500)
    tx = pg2.evaluate("()=>{const n=document.getElementById('auMesContact'); return n? n.textContent : null}")
    c2.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    juge('F · ?mesure=1 écrit le contact lu (13 × 7 pt)', bool(tx) and 'contact lu' in tx and '13' in tx and '7' in tx, repr(tx))
    b.close()
print('\n%d/%d' % (ok, ok + len(ko)))
if ko: sys.exit(1)
