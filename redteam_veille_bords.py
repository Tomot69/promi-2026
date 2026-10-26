#!/usr/bin/env python3
"""redteam_veille_bords.py — ⚑ v166 (Tom, C-181 §4) : LA VEILLE REBONDIT SUR L'ÉCRAN DE L'APP ; ELLE PART À 120 s ; 61,2 pt/s.

« Ses bords sont ceux de l'ÉCRAN DE L'APP, pas de la page du navigateur : sur iPhone l'écran visible ; sur ordinateur, quand l'app est montrée dans un cadre de
téléphone simulé, les bords de CE cadre, jamais les marges de la page autour. Le logo rebondit sur le conteneur racine de l'app. Vérifie sur mon état, à
390 × 651 sur iPhone ET dans le cadre simulé sur ordinateur. Juge : encre aux 4 bords du conteneur de l'app à ± 1 pt ; départ à 120 s ; vitesse. »
(v163 : l'encre au bord VISIBLE ± 1 pt ; les flaques de 350 ms — gardées.) Original : sauvegardes/redteam_veille_bords-avant-v166.py.

Banc WebKit, `?veille=2` pour les bords. Le logo est posé (boucle d'images arrêtée) sur chacune de ses quatre bornes ; l'ENCRE est lue sur l'image (pixels qui
diffèrent du fond de la veille, DANS la couche) et comparée au bord du conteneur de l'app à l'écran (`#device`, recoupé avec la zone visible) :
  A · haut, bas, gauche, droite : l'encre à 1 pt au plus du bord de l'app (pas plus loin, pas au-delà) — l'état de Tom (390 × 651), le cadre simulé d'un
      ordinateur (1440 × 900), 430 × 932 (échelle 1), 330 × 714 (≈ 0,79) ; et la couche de la veille ne déborde pas de l'app ;
  B · l'entrée et la sortie passent par `_passageFlaques` en 350 ms (± 30) chacune ;
  C · sans `?veille` (veille rallumée sur le banc) : elle part entre 119,5 et 121,5 s après le dernier toucher, pas avant ;
  D · la vitesse lue sur le logo : 61,2 pt/s (± 2 %), en points de l'app.
`--vite` saute C. Preuve : `--fichier=zz-v165.html` rougit (A : la page entière ; C : 60 s ; D : 60 pt/s).
"""
import sys, io, glob, json, time; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
PIEGE = """(()=>{ window.__pf=[]; let f; Object.defineProperty(window,'_passageFlaques',{configurable:true, get:()=>f ? function(h,o){ window.__pf.push([o&&o.mode, o&&o.duree]); return f.apply(this, arguments); } : f, set:v=>{ f=v; }}); })();"""
APP = """()=>{ const r=document.getElementById('device').getBoundingClientRect(), vv=visualViewport; const x0=Math.max(r.left, vv.offsetLeft), y0=Math.max(r.top, vv.offsetTop),
  x1=Math.min(r.right, vv.offsetLeft+vv.width), y1=Math.min(r.bottom, vv.offsetTop+vv.height); const c=document.getElementById('promiVeille'), q=c?c.getBoundingClientRect():null;
  return {app:[x0,y0,x1,y1], k:r.width/390, couche:q?[q.left,q.top,q.right,q.bottom]:null}; }"""
def encre(pg, vw, A, logo):
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); k = im.size[0] / vw; px = im.load()
    X0, Y0, X1, Y1 = [int(round(v * k)) for v in A]
    fond = px[X1 - 3, Y0 + 3]; xs = []; ys = []   # un coin de l'app : jamais sous le logo posé au milieu d'un bord
    for yy in range(max(0, Y0 - 4), min(im.size[1], Y1 + 4)):
        for xx in range(max(0, X0 - 4), min(im.size[0], X1 + 4)):
            q = px[xx, yy]
            if sum(abs(a - b) for a, b in zip(q, fond)) > 120 and sum(abs(a - b) for a, b in zip(q, logo)) < 140 and X0 <= xx < X1 and Y0 <= yy < Y1: xs.append(xx); ys.append(yy)   # l'encre du logo, jamais le bord du cadre
    return (min(xs) / k, max(xs + [0]) / k + 1 / k, min(ys) / k, max(ys + [0]) / k + 1 / k) if xs else None
def bords(pg, T, vw):
    v = pg.evaluate("()=>_veille()") or {}
    if not v.get('active'): juge('[%s] la veille a démarré' % T, False, v); return
    pg.evaluate("()=>{ window.__raf=window.requestAnimationFrame; window.requestAnimationFrame=function(){ return 0; }; }"); pg.wait_for_timeout(250)
    G = pg.evaluate(APP); A = G['app']; Bn = v['bornes']; C = v['cadre']; mx = (Bn['x0'] + Bn['x1']) / 2; my = (Bn['y0'] + Bn['y1']) / 2
    cq = G['couche']; deb = (max(A[0] - cq[0], cq[2] - A[2], A[1] - cq[1], cq[3] - A[3]) if cq else 99)
    juge('[%s] A · la couche de la veille couvre l\'app, et rien autour (± 1 px)' % T, cq is not None and abs(deb) <= 1, 'app %s · couche %s' % ([round(t, 1) for t in A], cq and [round(t, 1) for t in cq]))
    for nom, x, y, bord in (('haut', mx, Bn['y0'], 2), ('bas', mx, Bn['y1'], 3), ('gauche', Bn['x0'], my, 0), ('droite', Bn['x1'], my, 1)):
        pg.evaluate("a=>{ const c=document.querySelector('#promiVeille canvas'); c.style.transform='translate('+a[0]+'px,'+a[1]+'px)'; }", [x, y]); pg.wait_for_timeout(120)
        lg = v.get('couleur') or (v.get('couleurs') or ['#F7F0DE'])[-1]; lgc = tuple(int(lg[i:i + 2], 16) for i in (1, 3, 5))
        e = encre(pg, vw, A, lgc); cible = (A[0], A[2], A[1], A[3])[bord]
        d = None if not e else ((e[bord] - cible if bord in (0, 2) else cible - e[bord]) / G['k'])
        juge('[%s] A · l\'encre touche le bord %s de l\'app (≤ 1 pt)' % (T, nom), d is not None and -0.4 <= d <= 1.0,
             'encre %s · bord %.1f · écart %s pt' % (e and [round(t, 1) for t in e], cible, d if d is None else round(d, 2)))
    pg.evaluate("()=>{ window.requestAnimationFrame=window.__raf; }"); pg.wait_for_timeout(200)
def vitesse(pg, T):
    P = pg.evaluate("""()=>new Promise(ok=>{ const c=()=>document.querySelector('#promiVeille canvas'); const rd=()=>{ const m=/translate\\(([-\\d.]+)px, *([-\\d.]+)px/.exec(c().style.transform||''); return m?[+m[1],+m[2]]:null; };
      const L=[]; let t0=performance.now(); (function f(){ const p=rd(); if(p) L.push([performance.now()-t0, p[0], p[1]]); if(performance.now()-t0<1500) requestAnimationFrame(f); else ok(L); })(); })""")
    k = pg.evaluate(APP)['k']; best = None
    for i in range(len(P) - 1):   # le plus long morceau sans rebond (la direction ne change pas)
        for j in range(len(P) - 1, i, -1):
            dx = P[j][1] - P[i][1]; dy = P[j][2] - P[i][2]; dt = P[j][0] - P[i][0]
            seg = [P[m + 1][1] - P[m][1] for m in range(i, j)]; segy = [P[m + 1][2] - P[m][2] for m in range(i, j)]
            if dt > 400 and (all(s >= 0 for s in seg) or all(s <= 0 for s in seg)) and (all(s >= 0 for s in segy) or all(s <= 0 for s in segy)):
                v = (dx * dx + dy * dy) ** 0.5 / dt * 1000 / k
                if best is None or dt > best[1]: best = (v, dt)
                break
        if best and best[1] > 900: break
    gap = max([P[i + 1][0] - P[i][0] for i in range(len(P) - 1)] or [0])
    if gap > 100:   # la boucle de la veille borne son pas à 0,1 s : une image plus longue ralentit le logo — une cadence, jugée au calme seulement (C-137)
        print('  ·  NON JUGÉ (une image de %d ms, charge %.1f) — [%s] D · la vitesse : %s pt/s' % (gap, B.charge(), T, best and round(best[0], 2)), flush=True); return
    juge('[%s] D · la vitesse lue sur le logo : 61,2 pt/s (± 2 %%)' % T, best is not None and abs(best[0] - 61.2) <= 1.22, 'v %s pt/s sur %s ms (plus longue image %d ms)' % (best and round(best[0], 2), best and round(best[1]), gap))
with sync_playwright() as p:
    b = p.webkit.launch()
    L = [f for f in sorted(glob.glob('etats/tom-*.json')) if json.loads(json.load(io.open(f, encoding='utf-8')).get('ls', {}).get('promi_state', '{}') or '{}').get('promises')]
    CAS = []
    if L: CAS.append(('Tom ' + L[-1].split('/')[-1], None))
    else: juge("l'état exporté de Tom existe", False, 'aucun')
    CAS += [('ordinateur 1440×900 (cadre simulé)', (1440, 900, False)), ('430×932', (430, 932, True)), ('330×714', (330, 714, True))]
    for T, w in CAS:
        if w is None:
            ctx, d = B.contexte_tom(b, L[-1]); vw = int((d.get('ecran') or {}).get('largeur') or 390)
        else:
            vw, vh, mob = w
            ctx = B.contexte(b, vw=vw, vh=vh) if mob else b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=2)
            if not mob: ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true}); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_rappel_n','9'); }catch(e){}")
        ctx.add_init_script(PIEGE); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F + '?veille=2', timeout=180000); pg.wait_for_timeout(6000)
        if T.startswith('Tom') or T.startswith('ordinateur'): vitesse(pg, T)   # avant les bords : ils arrêtent la boucle d'images
        bords(pg, T, vw)
        if w is None or w[2]:
            B.tap(pg, vw / 2, (w[1] if w else 651) / 2)
        else:
            pg.mouse.click(vw / 2, w[1] / 2)
        pg.wait_for_timeout(800)
        pf = pg.evaluate("()=>window.__pf")
        ok = any(m == 'couvre' and abs((dd or 0) - 350) <= 30 for m, dd in pf) and any(m == 'ouvre' and abs((dd or 0) - 350) <= 30 for m, dd in pf)
        juge('[%s] B · l\'entrée et la sortie en flaques, 350 ms chacune' % T, ok, pf)
        ctx.close()
    if not VITE:   # C · le départ, sans ?veille : la veille rallumée sur le banc
        ctx = B.contexte(b); ctx.add_init_script("try{ localStorage.removeItem('promi_veille_off'); }catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000)
        R = pg.evaluate("()=>window._veilleRegle && [_veilleRegle.DELAI, _veilleRegle.VITESSE]")
        juge('C · la règle déclarée : 120 s, 61,2 pt/s', R == [120000, 61.2], R)
        t0 = None; dep = None; tf = time.time() + 140
        while time.time() < tf:
            v = pg.evaluate("()=>{ const v=_veille(); return [v.active, v.calme, v.coupee]; }")
            if v[2]: juge('C · la veille n\'est pas coupée sur ce banc', False, v); break
            if v[0]: dep = v[1] if dep is None else dep; break
            pg.wait_for_timeout(500)
        cal = pg.evaluate("()=>{ const v=_veille(); return v.depuis; }")
        juge('C · sans toucher, elle part à 120 s (± 1,5 s), pas avant', dep is not None and 119500 <= (dep - cal) <= 121500, 'calme au départ %s ms (depuis %s ms)' % (dep, cal))
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
