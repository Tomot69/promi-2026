#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_trace.py — L'EMPREINTE SUIT LE VRAI GESTE (v140, Tom, 10 oct. 2026, C-083).

« Quand le doigt glisse, les poils se couchent dans le sens et sur le trajet réels du doigt, avec la largeur de son contact. Plus de
tampon identique à chaque fois. Un appui sans glisser couche les poils en étoile autour du point. Juge : deux trajets différents laissent
deux traces différentes, alignées sur leur direction. »

Au vrai doigt (CDP `Input.dispatchTouchEvent`, horodaté, avec rayon de contact), Chromium sur carte graphique. Le doigt s'arrête avant de
se lever (pas d'élan) ; la trace se lit SUR L'IMAGE : pixels du canevas de la Pelote, à la même vue, avec la trace puis relissée — la
tache de différence donne son axe (analyse en composantes principales), sa longueur, sa largeur et son centre.
  A · un trajet horizontal de 130 pt : la trace est alignée sur lui (≤ 20°), centrée sur lui (≤ 30 pt), longue d'au moins 60 % du trajet ;
  B · un trajet oblique de 60 pt, ailleurs : aligné sur LUI (≤ 25°), centré sur lui ;
  C · les deux traces diffèrent : la longue fait au moins 1,5 fois la courte, et leurs axes diffèrent d'au moins 25° ;
  D · la largeur du contact : le même trajet au rayon 5 pt et au rayon 16 pt laisse deux largeurs (≥ 20 % d'écart) ;
  E · un appui sans glisser : une étoile — huit branches qui partent du point vers l'extérieur, réparties sur le tour (≥ 6 octants),
      et à l'image une tache ronde (allongement ≤ 1,6) centrée sur le point (≤ 14 pt) ;
  F · deux appuis (0,2 s et 1,6 s) ne laissent pas le même tampon : l'étoile du long est plus grande (≥ 20 %).
Preuve : rouge sur l'état d'avant (python3 redteam_trace.py zz-av140.html).
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
        """glisse de (x0,y0) à (x1,y1), s'arrête, se lève ; rend la tache mesurée"""
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x0, y0, r), 'timestamp': T[0]})
        n = 18
        for i in range(1, n + 1):
            T[0] += duree / n; pg.wait_for_timeout(int(1000 * duree / n))
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, r), 'timestamp': T[0]})
        pg.wait_for_timeout(int(1000 * tenue)); T[0] += tenue
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]})
        return mesure()
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
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]}); pg.wait_for_timeout(700)   # au-delà du double toucher
        return mesure()
    cx, cy = bo
    # ── A · un trajet horizontal de 130 pt, par le haut de la boule ──
    A = geste(cx - 65, cy - 30, cx + 65, cy - 30)
    okA = A.get('n', 0) >= 40
    juge('A · trajet horizontal de 130 pt : une trace alignée (≤ 20°), centrée (≤ 30 pt), longue (≥ 78 pt)', okA and ecart_angle(A['angle'], 0) <= 20 and math.hypot(A['cx'] - cx, A['cy'] - (cy - 30)) <= 30 and A['long'] >= 78,
         str({k: round(v, 1) for k, v in A.items() if k != 'geo' and v is not None}))
    # ── B · un trajet oblique de 60 pt, en bas à gauche ──
    B = geste(cx - 55, cy + 15, cx - 55 + 42, cy + 15 + 42)
    okB = B.get('n', 0) >= 40
    juge('B · trajet oblique de 60 pt, ailleurs : une trace alignée sur lui (45° ± 25), centrée sur lui (≤ 30 pt)', okB and ecart_angle(B['angle'], 45) <= 25 and math.hypot(B['cx'] - (cx - 34), B['cy'] - (cy + 36)) <= 30,
         str({k: round(v, 1) for k, v in B.items() if k != 'geo' and v is not None}))
    juge('C · deux trajets, deux traces : la longue ≥ 1,5 × la courte, axes écartés de ≥ 25°', okA and okB and A['long'] >= 1.5 * B['long'] and ecart_angle(A['angle'], B['angle']) >= 25,
         'longueurs %.0f / %.0f pt · axes %.0f° / %.0f°' % (A.get('long', 0), B.get('long', 0), A.get('angle', 0), B.get('angle', 0)))
    # ── D · la largeur du contact ──
    D1 = geste(cx - 65, cy - 30, cx + 65, cy - 30, r=5); D2 = geste(cx - 65, cy - 30, cx + 65, cy - 30, r=16)
    juge('D · la largeur du contact : rayon 5 pt contre 16 pt, deux largeurs (≥ 20 % d\'écart)', D1.get('n', 0) >= 40 and D2.get('n', 0) >= 40 and D2['large'] >= 1.2 * D1['large'], 'largeurs %.1f / %.1f pt' % (D1.get('large', 0), D2.get('large', 0)))
    # ── E, F · l'appui sans glisser ──
    E1 = appui(cx + 20, cy - 10, 11, 0.2); E2 = appui(cx + 20, cy - 10, 11, 1.6)
    def etoile(t):
        g = [a for a in (t.get('geo') or []) if a.get('et')]
        if len(g) < 6: return None
        # dans l'objet : le centre est la moyenne des départs ; chaque branche s'en éloigne ; on compte les octants autour du centre
        c = [sum(a['a'][i] for a in g) / len(g) for i in range(3)]; m = math.sqrt(sum(v * v for v in c)); c = [v / m for v in c]
        e1 = [c[1], -c[0], 0.0]; m = math.sqrt(sum(v * v for v in e1)) or 1; e1 = [v / m for v in e1]
        e2 = [c[1] * e1[2] - c[2] * e1[1], c[2] * e1[0] - c[0] * e1[2], c[0] * e1[1] - c[1] * e1[0]]
        octs = set(); dehors = 0
        for a in g:
            da = math.acos(max(-1, min(1, sum(a['a'][i] * c[i] for i in range(3))))); db = math.acos(max(-1, min(1, sum(a['b'][i] * c[i] for i in range(3)))))
            if db > da: dehors += 1
            v = [a['b'][i] - a['a'][i] for i in range(3)]; an = math.atan2(sum(v[i] * e2[i] for i in range(3)), sum(v[i] * e1[i] for i in range(3)))
            octs.add(int(((an + math.pi) / (math.pi / 4)) % 8))
        return {'branches': len(g), 'dehors': dehors, 'octants': len(octs), 'rayon': max(a['L'] for a in g) * 116}
    e1 = etoile(E1); e2 = etoile(E2)
    juge('E · un appui sans glisser : une étoile (8 branches vers l\'extérieur, ≥ 6 octants)', bool(e2) and e2['branches'] == 8 and e2['dehors'] == 8 and e2['octants'] >= 6, str(e2))
    juge('E · à l\'image : une tache ronde (allongement ≤ 1,6) centrée sur le point (≤ 14 pt)', E2.get('n', 0) >= 40 and E2['long'] <= 1.6 * max(1, E2['large'] * 1.25) and math.hypot(E2['cx'] - (cx + 20), E2['cy'] - (cy - 10)) <= 14,
         str({k: round(v, 1) for k, v in E2.items() if k != 'geo' and v is not None}))
    juge('F · deux appuis (0,2 s et 1,6 s), deux tampons : l\'étoile du long est plus grande (≥ 20 %)', bool(e1) and bool(e2) and e2['rayon'] >= 1.2 * e1['rayon'] and E2.get('n', 0) > E1.get('n', 0), 'rayons %s / %s pt · pixels %s / %s' % (e1 and round(e1['rayon'], 1), e2 and round(e2['rayon'], 1), E1.get('n'), E2.get('n')))
    juge('aucune erreur de page', not er, str(er[:2]))
    b.close()
print('\n%d/%d' % (ok, ok + len(ko)))
if ko: sys.exit(1)
