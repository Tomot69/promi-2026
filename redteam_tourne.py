#!/usr/bin/env python3
"""
redteam_tourne.py — UNE PHOTO SE TOURNE À DEUX DOIGTS, L'ANGLE EST MÉMORISÉ (v141, Tom, 10 oct. 2026 — C-098).

« La photo dans la bande d'une fiche, et la photo importée dans un dessin, se tournent à deux doigts. L'angle est mémorisé. »

Au vrai doigt (CDP, deux points de contact), Chromium :
  A · la bande d'une fiche (Promi) : deux doigts qui tournent de 30° autour de leur milieu → la photo a tourné de 30° (± 2°), sans changer de
      taille (± 4 %) ni quitter leur milieu (± 3 pt) ; à l'écran, les quarts de couleur ont tourné (pixels) ; la fiche refermée et rouverte,
      l'angle est là ; il est sur la parole (`photoCadre.a`), donc sauvegardé avec elle ; un pincement sans rotation ne tourne rien ;
  B · une photo importée dans un dessin : même geste → même angle (± 2°) ; POSER le garde ; le mode rouvert, il est là.
Preuve : rouge sur l'état d'avant (python3 redteam_tourne.py zz-av141.html).
"""
import sys, math
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
PHOTO = r"""()=>{ const c=document.createElement('canvas'); c.width=600; c.height=400; const g=c.getContext('2d'); [['#E00000',0,0],['#00B000',300,0],['#0000E0',0,200],['#E0E000',300,200]].forEach(q=>{ g.fillStyle=q[0]; g.fillRect(q[1],q[2],300,200); }); return c.toDataURL('image/png'); }"""
ETAT = "()=>{ try{ return window._photoCadre ? window._photoCadre.etat() : null; }catch(e){ return null; } }"
PIX = r"""([x,y])=>{ const cv=document.getElementById('dpTrameCv'), r=cv.getBoundingClientRect(); const g=cv.getContext('2d'), k=cv.width/r.width; const d=g.getImageData(Math.round((x-r.left)*k), Math.round((y-r.top)*k), 1, 1).data; return [d[0],d[1],d[2]]; }"""
def couleur(c):
    if c[0] > 150 and c[1] < 90 and c[2] < 90: return 'rouge'
    if c[0] < 90 and c[1] > 110 and c[2] < 90: return 'vert'
    if c[0] < 90 and c[1] < 90 and c[2] > 150: return 'bleu'
    if c[0] > 150 and c[1] > 150 and c[2] < 110: return 'jaune'
    return 'autre'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, has_touch=True)
    ctx.add_init_script("try{ if(!localStorage.getItem('promi_onb')){ localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9'); ['tenir','chiche','planter','bande','dessin'].forEach(g=>{localStorage.setItem('geste_v','143');localStorage.setItem('geste_vu_'+g,'1')}); } }catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} }")
    def T(typ, pts): cdp.send('Input.dispatchTouchEvent', {'type': typ, 'touchPoints': [{'x': x, 'y': y, 'id': i} for i, (x, y) in enumerate(pts)]})
    def tourne(cx, cy, r, deg, r1=None, n=14):
        """deux doigts de part et d'autre de (cx, cy), à r du milieu, qui tournent de `deg` (et s'écartent jusqu'à r1)"""
        r1 = r if r1 is None else r1
        def pts(u):
            a = math.radians(deg) * u; rr = r + (r1 - r) * u; return [(cx - rr * math.cos(a), cy - rr * math.sin(a)), (cx + rr * math.cos(a), cy + rr * math.sin(a))]
        P0 = pts(0); T('touchStart', [P0[0]]); T('touchStart', P0)
        for i in range(1, n + 1): T('touchMove', pts(i / n)); pg.wait_for_timeout(18)
        T('touchEnd', []); pg.wait_for_timeout(500)
    # ── A · la bande d'une fiche
    src = pg.evaluate(PHOTO)
    pg.evaluate("([t,s])=>{ try{closeAll()}catch(e){} const q=promises.find(p=>p.title===t); q.photo=s; delete q.photoCadre; openDetail(q.id); }", ['faire les crêpes', src]); pg.wait_for_timeout(3200)
    cx, cy, k = pg.evaluate("()=>{ const c=window._photoCentre||{x:195,y:150}; const cv=document.getElementById('dpTrameCv'), r=cv.getBoundingClientRect(), k=r.width/390; return [r.left+c.x*k, r.top+c.y*k, k]; }")
    e0 = pg.evaluate(ETAT) or {}
    tourne(cx, cy, 45, 0, 70); e1 = pg.evaluate(ETAT) or {}
    juge('A · un pincement sans rotation ne tourne rien', abs(e1.get('a', 9)) < 0.02 and e1.get('z', 0) > 1.3, 'angle %.3f rad · zoom %.2f' % (e1.get('a', 9), e1.get('z', 0)))
    tourne(cx, cy, 60, 30); e2 = pg.evaluate(ETAT) or {}
    juge('A · deux doigts qui tournent de 30° tournent la photo de 30° (± 2°)', abs(math.degrees(e2.get('a', 9)) - 30) <= 2, 'angle %.1f°' % math.degrees(e2.get('a', 9)))
    juge('A · sans changer sa taille (± 4 %) ni la décentrer (± 3 pt)', abs(e2.get('z', 0) / max(1e-6, e1.get('z', 1)) - 1) <= 0.04 and abs(e2.get('dx', 99) - e1.get('dx', 0)) <= 3 and abs(e2.get('dy', 99) - e1.get('dy', 0)) <= 3, 'zoom %.2f → %.2f · décalage (%.1f ; %.1f) → (%.1f ; %.1f)' % (e1.get('z', 0), e2.get('z', 0), e1.get('dx', 0), e1.get('dy', 0), e2.get('dx', 0), e2.get('dy', 0)))
    tourne(cx, cy, 60, 60); e3 = pg.evaluate(ETAT) or {}      # 30 + 60 = 90° : le quart rouge (haut gauche) passe en haut à droite
    c_hd = couleur(pg.evaluate(PIX, [cx + 22 * k, cy - 22 * k])); c_hg = couleur(pg.evaluate(PIX, [cx - 22 * k, cy - 22 * k]))
    juge('A · à l\'écran : tournée d\'un quart de tour, le quart rouge est en haut à droite, le bleu en haut à gauche (pixels)', abs(math.degrees(e3.get('a', 9)) - 90) <= 3 and c_hd == 'rouge' and c_hg == 'bleu', 'angle %.1f° · haut droite %s · haut gauche %s' % (math.degrees(e3.get('a', 9)), c_hd, c_hg))
    mem = pg.evaluate("()=>{ const q=promises.find(p=>p.title==='faire les crêpes'); return q.photoCadre ? q.photoCadre.a : null; }")
    pg.evaluate("()=>{ const q=promises.find(p=>p.title==='faire les crêpes'); closeAll(); setTimeout(()=>openDetail(q.id), 900); }"); pg.wait_for_timeout(4200); e4 = pg.evaluate(ETAT) or {}
    juge('A · l\'angle est mémorisé : sur la parole, et encore là quand la fiche est rouverte', mem is not None and abs(mem - e3.get('a', 9)) < 1e-6 and abs(e4.get('a', 9) - e3.get('a', 0)) < 1e-6, 'sur la parole %s · fiche rouverte %.3f' % (mem, e4.get('a', 9)))
    # ── B · une photo importée dans un dessin
    pg.evaluate("()=>{ try{closeAll()}catch(e){} const q=promises.find(p=>p.title==='nager le mardi'); delete q.dessin; setTimeout(()=>openDetail(q.id), 800); }"); pg.wait_for_timeout(3600)
    pg.evaluate("()=>{ window._dessin.ouvre(); }"); pg.wait_for_timeout(900)
    pg.evaluate("(s)=>{ window._dessin.ajoutePhoto(s); }", src); pg.wait_for_timeout(600)
    S = pg.evaluate("()=>{ const s=document.querySelector('#dessinMode .dz-surface').getBoundingClientRect(); return [s.left, s.top, s.width/390]; }")
    if not pg.evaluate("()=>{ const b=document.querySelector('#dessinMode [data-outil=photo]'); return !!(b&&b.getAttribute('aria-pressed')==='true'); }"):
        pg.evaluate("()=>{ const e=window._dessin.etat(); if(e && e.outil!=='photo'){ const b=document.querySelector('#dessinMode [data-outil=photo]'); if(b) b.click(); } }"); pg.wait_for_timeout(500)
    A = pg.evaluate("()=>window._dessin.photos()")
    if A:
        x, y = S[0] + A[0]['x'] * S[2], S[1] + A[0]['y'] * S[2]
        tourne(x, y, 34, 40); B = pg.evaluate("()=>window._dessin.photos()")
        juge('B · une photo du dessin : deux doigts qui tournent de 40° la tournent de 40° (± 2°)', bool(B) and abs(math.degrees(B[0].get('a', 9)) - 40) <= 2 and abs(B[0]['w'] / A[0]['w'] - 1) <= 0.05 and abs(B[0]['x'] - A[0]['x']) <= 3 and abs(B[0]['y'] - A[0]['y']) <= 3,
             'angle %.1f° · largeur %.1f → %.1f · centre (%.1f ; %.1f) → (%.1f ; %.1f)' % (math.degrees(B[0].get('a', 9)) if B else 0, A[0]['w'], B[0]['w'] if B else 0, A[0]['x'], A[0]['y'], B[0]['x'] if B else 0, B[0]['y'] if B else 0))
        pg.evaluate("()=>{ const b=document.querySelector('#dessinMode .dz-poser'); if(b) b.click(); }"); pg.wait_for_timeout(1200)
        d = pg.evaluate("()=>{ const q=promises.find(p=>p.title==='nager le mardi'); const L=(q.dessin&&q.dessin.poses)||[]; const t=L.filter(e=>e.img)[0]; return t?t.a:null; }")
        juge('B · POSER garde l\'angle (il est dans le dessin de la parole)', d is not None and B and abs(d - B[0]['a']) < 0.002, 'angle posé %s' % d)
        pg.evaluate("()=>{ window._dessin.ouvre(); }"); pg.wait_for_timeout(1000); C = pg.evaluate("()=>window._dessin.photos()")
        juge('B · le mode rouvert, la photo a toujours son angle', bool(C) and B and abs(C[0].get('a', 9) - B[0]['a']) < 0.002, 'angle %s' % (C and C[0].get('a')))
    else: juge('B · une photo est dans le dessin', False, 'aucune photo')
    b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
