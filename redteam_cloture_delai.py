#!/usr/bin/env python3
"""redteam_cloture_delai — v169b (Tom, C-203 §1) : « la phrase de clôture et le flou qui l'annonce arrivent avec une latence inutile ».

Cible, EN DUR : le flou commence à se déployer AU PLUS 100 ms après le déclencheur, et la zone nette de Partager, avec sa flèche, est ouverte AU PLUS
800 ms après. Trois chemins (et une variante de b) :
  a  · le +, une nature, puis la page + refermée par son X — déclencheur : la fin de la fermeture (la page + sortie de l'écran) ;
  a+ · le +, une nature, une parole PLANTÉE (la page + se referme d'elle-même, la Toile bouge) — même déclencheur ;
  b  · le +, puis un toucher ailleurs 1,6 s plus tard (le menu se ferme) — déclencheur : le toucher ;
  b' · le +, puis un toucher ailleurs 0,4 s plus tard (pendant que l'eau se retire) — déclencheur : le toucher ;
  c  · un toucher ailleurs que le + — déclencheur : le toucher (le flou est déjà là : il « commence » quand la zone du + commence à se refermer).
Mesure DANS LA PAGE, image par image (une boucle requestAnimationFrame posée avant l'app, l'heure des touchers lue sur l'événement). Deux échelles :
390 × 844 (1) et 330 × 714 (0,79), WebKit, au doigt. Chaque délai est rapporté ; la charge du Mac aussi (C-137 : au-dessus de 4, un rouge de quelques
images se rejoue avant d'être cru). `--fichier=zz-v169.html` : rouge (la clôture attendait le calme de la Toile, 400 ms, puis 1,4 s de couverture).
"""
import os, sys
from playwright.sync_api import sync_playwright
import banc_tom as B

F = 'app.html'
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
D_FLOU, D_ZONE = 100, 800                      # ms — les cibles de Tom, en dur
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
def charge():
    try: return float(os.popen('sysctl -n vm.loadavg').read().split()[1])
    except Exception: return 0.0

SONDE = r"""(()=>{ window.__J=[]; window.__T=[];
  ['touchend','pointerup'].forEach(n=>window.addEventListener(n, e=>{ __T.push(performance.now()); }, true));
  function f(){ const g=document.getElementById('guide'), cs=document.getElementById('createSheet'), d=document.getElementById('device');
    let sh=0; if(cs && d){ const r=cs.getBoundingClientRect(), D=d.getBoundingClientRect(), c=getComputedStyle(cs);
      sh = (cs.classList.contains('show') || (c.display!=='none' && c.visibility!=='hidden' && +c.opacity>0.01 && r.top < D.bottom-1 && r.bottom > D.top+1)) ? 1 : 0; }
    __J.push([performance.now(), g?g.getAttribute('data-guide'):null, g?+(g.getAttribute('data-couv')||0):-1, g?+(g.getAttribute('data-net')||0):-1, g&&g.getAttribute('data-fleche')?1:0, sh]);
    if(__J.length>4000) __J.splice(0,1000); requestAnimationFrame(f); } requestAnimationFrame(f); })();"""

def page(b, vw, vh):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=True)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__ini')){ sessionStorage.setItem('__ini','1'); localStorage.setItem('promi_theme','light'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}")
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    return ctx, pg, er
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
def jusqu_au_plus(pg):
    pg.evaluate("()=>{ _guide.attend(false); }")
    e = attend(pg, "()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&g.getAttribute('data-entier') ? _guide.etat() : null;}", 170)
    if not e: return False
    pg.wait_for_timeout(700); tap_pt(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600)
    tap_sel(pg, '#studioScreen .closeb')
    return bool(attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=1);}", 150))

def delais(J, t0, chemin):
    """J : [t, guide, couv, net, fleche, feuille] par image. Rend (t du déclencheur, délai du flou, délai de la zone)."""
    if chemin == 'a':                                     # la fin de la fermeture : la première image, après t0, où la page + n'est plus à l'écran
        tr = next((r[0] for r in J if r[0] > t0 and r[5] == 0), None)
    else: tr = t0
    if tr is None: return None, None, None
    av = [r for r in J if r[0] <= tr]; ap = [r for r in J if r[0] > tr]
    prev = av[-1][2] if av else -1
    flou = None
    # ⚑ v170d (Tom, C-203 : « le passage du + à Partager exactement comme celui du Studio au + ») — l'eau ne se retire plus quand on touche le + : au
    #   déclencheur le flou est DÉJÀ là (couverture ≥ 0,99) — il « commence » à 0 ms. Original : sauvegardes/redteam_cloture_delai-avant-v170d.py
    if chemin != 'c' and prev >= 0.99: flou = 0.0
    for r in ap:
        if flou is not None: break
        if (chemin == 'c' and r[1] not in ('plus',)) or (chemin != 'c' and r[2] > max(prev, 0) + 0.001): flou = r[0] - tr; break
        prev = r[2] if r[2] >= 0 else prev
    zone = next((r[0] - tr for r in ap if r[1] == 'partage' and r[3] >= 0.999 and r[4]), None)
    # la plus longue image entre le déclencheur et le départ du flou (une image longue = du travail sur le fil principal, pas une attente)
    fen = [r[0] for r in J if tr - 20 <= r[0] <= tr + (flou or 0) + 1]
    delais.image = max([b - a for a, b in zip(fen, fen[1:])] or [0])
    return tr, flou, zone

with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, ech in ((390, 844, '1'), (330, 714, '0,79')):
        for ch in ('c', 'a', 'a+', 'b', "b'"):
            T = 'échelle %s · %s' % (ech, ch)
            ctx, pg, er = page(b, vw, vh)
            if not jusqu_au_plus(pg):
                juge('[%s] le guide atteint l\'étape du +' % T, False); ctx.close(); continue
            pg.evaluate(SONDE); pg.wait_for_timeout(700)
            if ch == 'c':
                tap_pt(pg, 200, 520)
            else:
                z = pg.evaluate("()=>_guide.etat().trou"); tap_pt(pg, z['x'], z['y'])
                attend(pg, "()=>{const c=document.getElementById('accChoix'); return !!(c&&c.classList.contains('ouvert'));}", 30, 50)
                if ch in ('a', 'a+'):
                    pg.wait_for_timeout(1600); tap_sel(pg, '.acc-pil[data-k=promi]')
                    attend(pg, "()=>document.getElementById('createSheet').classList.contains('show')", 60)
                    pg.wait_for_timeout(1800)
                    if ch == 'a': tap_sel(pg, '#createSheet .closeb')
                    else:
                        pg.evaluate("()=>{document.getElementById('fTitle').value='marcher au bord du lac';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}")
                        tap_sel(pg, '#addPromi') or pg.evaluate("()=>document.getElementById('addPromi').click()")
                        pg.evaluate("()=>__T.push(performance.now())")
                else:
                    pg.wait_for_timeout(1600 if ch == 'b' else 400); tap_pt(pg, 200, 330)
            t0 = pg.evaluate("()=>__T[__T.length-1]||0")
            attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='partage' && +g.getAttribute('data-net')>=1);}", 80, 100)
            pg.wait_for_timeout(300)
            J = pg.evaluate("()=>__J"); tr, fl, zo = delais(J, t0, 'a' if ch in ('a', 'a+') else ('c' if ch == 'c' else 'b'))
            cg = charge()
            juge('[%s] le flou commence ≤ %d ms après le déclencheur' % (T, D_FLOU), fl is not None and fl <= D_FLOU, '%s ms (plus longue image %d ms ; charge %.1f)' % (None if fl is None else round(fl), round(getattr(delais, 'image', 0)), cg))
            juge('[%s] la zone nette de Partager et sa flèche ouvertes ≤ %d ms' % (T, D_ZONE), zo is not None and zo <= D_ZONE, '%s ms (charge %.1f)' % (None if zo is None else round(zo), cg))
            juge('[%s] aucune erreur de page' % T, not [x for x in er if 'version.json' not in x], er[:2])
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
