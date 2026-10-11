#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_trace.py — LA TRACE EST LA SURFACE RÉELLEMENT TOUCHÉE, FORMÉE SOUS LE DOIGT (v141, Tom, 10 oct. 2026, C-083 — RÉCIDIVE).

⚑ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_trace-avant-v141.py, qui exigeait l'étoile d'un appui et une trace
posée au lâcher le long du chemin tracé à l'écran). La décision qui le remplace :
« Retire l'étoile à huit branches et tout dessin géométrique. La trace est la surface réellement touchée par le doigt : l'union des zones de
contact lues à chaque image le long du chemin, les poils couchés dans le sens du mouvement. Elle se forme sous le doigt, en direct, pas au
lâcher. Un appui immobile creuse la forme du contact, sans motif. »

Au vrai doigt (CDP, horodaté, avec rayon de contact), Chromium sur carte graphique. La trace se lit SUR L'IMAGE (la tache de différence entre
la boule avec la trace et relissée, à la même vue : son axe, sa largeur, son centre) et dans ce que l'app déclare (`tracesGeo`).
  A · EN DIRECT : à mi-geste, doigt posé, la trace existe déjà ; au lâcher, rien ne s'y ajoute ;
  B · un glissement horizontal couche les poils sur son axe (≤ 25°), là où le doigt a fini (≤ 34 pt) ; un glissement oblique, sur le sien (≤ 30°) ;
  C · les deux traces n'ont pas le même axe (≥ 25°) ;
  D · la largeur du contact : rayon 5 pt contre 16 pt, la zone couchée est plus étendue (≥ 1,4 fois) ;
  E · un appui immobile (0,2 s, puis 1,6 s) : pendant l'appui le creux est là ; ensuite AUCUNE trace, aucun motif (ni arc, ni tache à l'image) ;
  F · plus d'étoile : aucun arc marqué « étoile », ni dans ce que l'app déclare, ni dans sa source.
Preuve : rouge sur l'état d'avant (python3 redteam_trace.py zz-av141.html).
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
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('geste_vu_pelote','1');localStorage.setItem('geste_vu_aura-apparait','1');}catch(e){}")
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
    A = geste(cx - 65, cy - 30, cx + 65, cy - 30)
    juge('A · EN DIRECT : à mi-geste, doigt posé, la trace existe déjà', (A.get('mi') or 0) >= 1, 'traces à mi-geste : %s' % A.get('mi'))
    juge('A · au lâcher, rien ne s\'y ajoute (elle s\'est formée sous le doigt)', (A.get('avant') or 0) >= 1 and A.get('apres') == A.get('avant'), 'avant le lâcher %s · au repos %s' % (A.get('avant'), A.get('apres')))
    okA = A.get('n', 0) >= 40
    juge('B · un glissement horizontal : les poils couchés sur son axe (≤ 25°), là où le doigt a fini (≤ 34 pt)', okA and ecart_angle(A['angle'], 0) <= 25 and math.hypot(A['cx'] - (cx + 65), A['cy'] - (cy - 30)) <= 34, court(A))
    B = geste(cx - 55, cy + 15, cx - 55 + 42, cy + 15 + 42)
    okB = B.get('n', 0) >= 40
    juge('B · un glissement oblique : sur le sien (45° ± 30), là où le doigt a fini (≤ 34 pt)', okB and ecart_angle(B['angle'], 45) <= 30 and math.hypot(B['cx'] - (cx - 13), B['cy'] - (cy + 57)) <= 34, court(B))
    juge('C · deux gestes, deux traces : leurs axes diffèrent d\'au moins 25°', okA and okB and ecart_angle(A['angle'], B['angle']) >= 25, 'axes %.0f° / %.0f°' % (A.get('angle', 0), B.get('angle', 0)))
    D1 = geste(cx - 65, cy - 30, cx + 65, cy - 30, r=5); D2 = geste(cx - 65, cy - 30, cx + 65, cy - 30, r=16)
    # la zone touchée est à peu près ronde (c'est le contact) : son « axe » ne dit pas sa largeur — on compare son ÉTENDUE (les pixels que la trace change)
    juge('D · la largeur du contact : rayon 5 pt contre 16 pt, la zone couchée est plus étendue (≥ 1,4 fois)', D1.get('n', 0) >= 40 and D2.get('n', 0) >= 1.4 * D1.get('n', 1), 'pixels changés %s / %s' % (D1.get('n'), D2.get('n')))
    E1 = appui(cx + 20, cy - 10, 11, 0.2); E2 = appui(cx + 20, cy - 10, 11, 1.6)
    juge('E · un appui immobile creuse (le creux est là pendant l\'appui long)', E2.get('creux') is True, 'creux : %s' % E2.get('creux'))
    juge('E · ensuite, aucune trace et aucun motif : ni arc, ni tache à l\'image (0,2 s et 1,6 s)', len(E1.get('geo') or []) == 0 and len(E2.get('geo') or []) == 0 and E1.get('n', 0) < 40 and E2.get('n', 0) < 40,
         'arcs %d / %d · pixels changés %s / %s' % (len(E1.get('geo') or []), len(E2.get('geo') or []), E1.get('n'), E2.get('n')))
    tous = (A.get('geo') or []) + (B.get('geo') or []) + (E1.get('geo') or []) + (E2.get('geo') or [])
    src = pg.evaluate("()=>{ let n=0; document.querySelectorAll('script').forEach(s=>{ const t=s.textContent||''; if(/\\._?a?\\.et\\s*=\\s*1/.test(t) || /_a\\.et=1/.test(t)) n++; }); return n; }")
    juge('F · plus d\'étoile : aucun arc marqué « étoile », ni déclaré ni dans la source', not any(a.get('et') for a in tous) and src == 0, 'arcs en étoile %d · source %d' % (sum(1 for a in tous if a.get('et')), src))
    juge('aucune erreur de page', not er, str(er[:2]))
    b.close()
print('\n%d/%d' % (ok, ok + len(ko)))
if ko: sys.exit(1)
