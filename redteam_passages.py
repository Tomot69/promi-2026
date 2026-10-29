#!/usr/bin/env python3
"""redteam_passages — v170d (Tom, C-203) : « le passage de l'étape du + à celle de Partager doit être EXACTEMENT le même qu'entre le Studio et le + : même
chorégraphie de flaques, mêmes durées, même façon dont la zone nette se referme puis s'ouvre ailleurs, et la flèche qui apparaît de la même manière ».

Image par image, dans la page, on relève l'état du guide (`data-guide`, l'eau `data-couv`, la zone nette `data-net`, la flèche `data-fleche`) :
  S  · le Studio touché puis refermé → l'étape du + ;
  c  · à l'étape du +, un toucher ailleurs → Partager ;
  b  · le + touché, puis un toucher ailleurs (le menu se ferme) → Partager ;
  a  · le +, une nature, la page + refermée par son X → Partager.
Pour chaque passage : ① les ÉTAPES — l'eau ne bouge pas (couverture ≥ 0,99 de bout en bout), la zone d'avant se referme d'un seul mouvement jusqu'à 0, puis
la zone suivante s'ouvre d'un seul mouvement jusqu'à 1, la flèche paraît avec elle ; ② les DURÉES — fermeture et ouverture de chaque passage + → Partager à
± 10 % de celles du passage Studio → + mesuré dans la même page ; ③ le flou démarre au plus 100 ms après le déclencheur (v169b) : il est déjà là.
Les durées se lisent sur l'horloge des images (une image de 100 ms s'y voit) : sous une charge > 4, un écart de durée est « NON JUGÉ » (C-137).
"""
import sys
from playwright.sync_api import sync_playwright
import banc_tom as B

F = 'app.html'
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)

SONDE = r"""(()=>{ window.__P=[]; window.__T=[];
  ['touchend','pointerup'].forEach(n=>window.addEventListener(n, e=>{ __T.push(performance.now()); }, true));
  function f(){ const g=document.getElementById('guide');
    __P.push([performance.now(), g?g.getAttribute('data-guide'):null, g?+(g.getAttribute('data-couv')||0):-1, g?+(g.getAttribute('data-net')||0):-1, g&&g.getAttribute('data-fleche')?1:0]);
    if(__P.length>6000) __P.splice(0,2000); requestAnimationFrame(f); } requestAnimationFrame(f); })();"""

def page(b, vw=390, vh=844):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=True)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__ini')){ sessionStorage.setItem('__ini','1'); localStorage.setItem('promi_theme','light'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}")
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    pg.evaluate(SONDE); return ctx, pg, er
def attend(pg, js, n=150, pas=100):
    for _ in range(n):
        v = pg.evaluate(js)
        if v: return v
        pg.wait_for_timeout(pas)
    return None
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
def tap_pt(pg, x, y):
    d = dev(pg); B.tap(pg, d[0] + x * d[2], d[1] + y * d[2], appareil=False)
def tap_sel(pg, sel):
    c = pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
    if c: B.tap(pg, c[0], c[1], appareil=False)
    return bool(c)
ETAPE = "q=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')===q && +g.getAttribute('data-net')>=0.999);}"

def passage(P, t0, depuis, vers):
    """le passage après t0 : la fermeture (net qui descend de ~1 à 0), puis l'ouverture (net de 0 à 1 sous l'étape `vers`) ; l'eau pendant tout ce temps"""
    L = [r for r in P if r[0] >= t0 - 20]
    i0 = next((i for i, r in enumerate(L) if r[3] < 0.999 and r[3] >= 0), None)          # la zone d'avant commence à se refermer
    if i0 is None: return None
    i1 = next((i for i in range(i0, len(L)) if L[i][3] <= 0.001), None)                  # fermée
    if i1 is None: return None
    i2 = next((i for i in range(i1, len(L)) if L[i][1] == vers and L[i][3] > 0.001), None)  # la suivante commence à s'ouvrir
    if i2 is None: return None
    i3 = next((i for i in range(i2, len(L)) if L[i][1] == vers and L[i][3] >= 0.999), None)
    if i3 is None: return None
    seg = L[i0:i3 + 1]
    mono_f = all(b[3] <= a[3] + 1e-6 for a, b in zip(L[i0:i1], L[i0 + 1:i1 + 1]))
    mono_o = all(b[3] >= a[3] - 1e-6 for a, b in zip(L[i2:i3], L[i2 + 1:i3 + 1]))
    ferme = L[i1][0] - L[i0 - 1 if i0 else i0][0]; ouvre = L[i3][0] - L[i2 - 1][0]; trou = L[i2 - 1][0] - L[i1][0]
    fl = next((r[0] for r in L[i2:] if r[4]), None)
    imgs = [b[0] - a[0] for a, b in zip(seg, seg[1:])]
    return {'debut': L[i0][0] - t0, 'ferme': ferme, 'trou': trou, 'ouvre': ouvre, 'couv_min': min(r[2] for r in seg), 'mono': mono_f and mono_o,
            'fleche': None if fl is None else fl - L[i2][0], 'pire': max(imgs or [0]), 'couv0': L[0][2]}

with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, ech in ((390, 844, '1'), (330, 714, '0,79')):
        ctx, pg, er = page(b, vw, vh)
        pg.evaluate("()=>{ _guide.attend(false); }")
        e = attend(pg, "()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&g.getAttribute('data-entier') ? _guide.etat() : null;}", 170)
        if not e: juge('[%s] le guide atteint le Studio' % ech, False); ctx.close(); continue
        pg.wait_for_timeout(700); tap_pt(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600)
        tS = pg.evaluate("()=>performance.now()"); tap_sel(pg, '#studioScreen .closeb')
        attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=0.999);}", 150)
        pg.wait_for_timeout(500)
        S = passage(pg.evaluate("()=>__P"), tS, 'studio', 'plus')
        ref = S
        print('  [%s] Studio → + : %s' % (ech, S), flush=True)
        juge('[%s] S · le passage Studio → + se lit (fermeture puis ouverture, l\'eau en place)' % ech, S and S['couv_min'] >= 0.99 and S['mono'], S)
        ctx.close()
        if not ref: continue
        for ch in ('c', 'b', 'a'):
            T = 'échelle %s · %s' % (ech, ch)
            ctx, pg, er = page(b, vw, vh)
            pg.evaluate("()=>{ _guide.attend(false); }")
            e = attend(pg, "()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&g.getAttribute('data-entier') ? _guide.etat() : null;}", 170)
            if not e: juge('[%s] le guide atteint le Studio' % T, False); ctx.close(); continue
            pg.wait_for_timeout(700); tap_pt(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600); tap_sel(pg, '#studioScreen .closeb')
            if not attend(pg, "()=>" + ETAPE.split('=>', 1)[1].replace('q', "'plus'"), 150): juge('[%s] l\'étape du +' % T, False); ctx.close(); continue
            pg.wait_for_timeout(900)
            if ch == 'c':
                t0 = pg.evaluate("()=>performance.now()"); tap_pt(pg, 200, 520)
            else:
                z = pg.evaluate("()=>_guide.etat().trou"); tap_pt(pg, z['x'], z['y'])
                attend(pg, "()=>{const c=document.getElementById('accChoix'); return !!(c&&c.classList.contains('ouvert'));}", 30, 50)
                eau = pg.evaluate("()=>{const g=document.getElementById('guide'); return g?+g.getAttribute('data-couv'):-1;}")
                menu = pg.evaluate("()=>{const p=document.querySelector('#accChoix .acc-pil'); if(!p) return null; const r=p.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!(h&&p.contains(h));}")
                juge('[%s] le + touché : l\'eau reste (comme au Studio), le menu des natures se touche par-dessus le flou' % T, eau >= 0.99 and menu, 'eau %s · menu joignable %s' % (eau, menu))
                pg.wait_for_timeout(1200)
                if ch == 'b':
                    t0 = pg.evaluate("()=>performance.now()"); tap_pt(pg, 200, 330)
                else:
                    tap_sel(pg, '.acc-pil[data-k=promi]'); attend(pg, "()=>document.getElementById('createSheet').classList.contains('show')", 60); pg.wait_for_timeout(1800)
                    t0 = pg.evaluate("()=>performance.now()"); tap_sel(pg, '#createSheet .closeb')
            attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='partage' && +g.getAttribute('data-net')>=0.999);}", 80, 100)
            pg.wait_for_timeout(400)
            P = pg.evaluate("()=>__P"); Q = passage(P, t0, 'plus', 'partage'); cg = B.charge()
            print('  [%s] + → Partager : %s' % (T, Q), flush=True)
            juge('[%s] ① mêmes étapes : l\'eau ne bouge pas, la zone du + se referme d\'un mouvement, celle de Partager s\'ouvre d\'un mouvement' % T, Q and Q['couv_min'] >= 0.99 and Q['mono'], Q and {k: Q[k] for k in ('couv_min', 'mono')})
            juge('[%s] ① la flèche paraît avec la zone, comme au passage Studio → +' % T, Q and ref['fleche'] is not None and Q['fleche'] is not None and abs(Q['fleche'] - ref['fleche']) <= 50, Q and '%s ms (Studio → + : %s ms)' % (Q['fleche'], ref['fleche']))
            for k in ('ferme', 'ouvre'):
                ok = Q and abs(Q[k] - ref[k]) <= 0.10 * ref[k]
                if Q and not ok and cg > 4: print('  ⚠ [%s] ② %s : %d ms contre %d ms — NON JUGÉ (charge %.0f)' % (T, k, Q[k], ref[k], cg), flush=True); continue
                juge('[%s] ② la %s dure comme au passage Studio → + (± 10 %%)' % (T, 'fermeture' if k == 'ferme' else 'ouverture'), ok, Q and '%d ms contre %d ms' % (Q[k], ref[k]))
            fl = Q and Q['couv0']
            juge('[%s] ③ le flou est là au déclencheur (≤ 100 ms : il ne part pas)' % T, Q and Q['couv0'] >= 0.99, 'couverture %s au déclencheur' % fl)
            juge('[%s] aucune erreur de page' % T, not [x for x in er if 'version.json' not in x], er[:2])
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
