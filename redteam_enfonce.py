#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_enfonce.py — LE TOUCHER DE LA PELOTE (v139, Tom, 9 oct. 2026, C-083).

« L'empreinte suit la forme réelle du contact (taille et forme du doigt lues sur le toucher, radiusX/radiusY quand Safari les donne) ;
plus on appuie longtemps, plus ça s'enfonce : vite au début, puis de plus en plus lentement, jusqu'à une butée, comme une matière qui
durcit ; jamais de saut : la profondeur progresse à chaque image ; au relâcher, la fourrure revient lentement à sa forme. »

Au vrai doigt (CDP `Input.dispatchTouchEvent`, avec rayon de contact), Chromium sur carte graphique, vue figée :
  A · pendant 3 s d'appui, la profondeur (lue à chaque image : part de la butée, d = p^(2/3)) CROÎT à chaque image ;
  B · sa vitesse DÉCROÎT (fenêtres de 150 ms successives, chacune plus lente que la précédente ; au-delà de 1,5 s, où une
      fenêtre ne vaut plus qu'un pour cent, à 0,4 point près — le grain d'une image) ;
  C · aucun saut : le plus grand pas d'une image, ramené à 16,7 ms, ≤ 8 % de la butée (décidé ; la loi décidée en fait 5,6 %) ;
  D · une butée : à 3 s la profondeur dépasse 90 % et n'a pas dépassé 100 % ;
  E · à l'écran (pixels du canevas, par différence avec le repos) : le creux grandit de 0,15 s à 0,6 s puis à 2,5 s ;
  F · deux tailles de contact (rayons 7 pt et 16 pt) donnent deux empreintes différentes — au compte de pixels (≥ 30 % d'écart)
      et à la cote déclarée ;
  G · un contact allongé (rayons 16 × 8) donne une empreinte allongée (el ≤ 0,7), un contact rond une empreinte ronde (el ≥ 0,9) ;
  H · au relâcher, la fourrure revient LENTEMENT : 0,6 s après, le creux fait encore ≥ 25 % de sa profondeur ; à 5 s il n'y a plus rien ;
      et pendant le retour aucun saut non plus ;
  I · les constantes décidées (EN DUR) : ENF_TAU 0,60 s, RETOUR_TAU 0,60 s.
Preuve : sur `sauvegardes/app-avant-v139.html` il rougit (A/C : 32 % à la première image ; F : même empreinte ; H : retour en 0,15 s).
"""
import sys
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ENF_TAU, RETOUR_TAU, PAS_MAX = 0.60, 0.60, 0.08
ok = 0; ko = []
def plus_grand_pas(L, sens):
    # le pas d'une image, ramené à 16,7 ms ; deux relevés à moins de 12 ms l'un de l'autre sont une même image (le navigateur
    # rend parfois deux rappels coup sur coup) : on les réunit, sinon 4 ms d'écart gonflent le pas par quatre
    m = 0.0; i0 = 0
    for i in range(1, len(L)):
        dt = L[i][0] - L[i0][0]
        if dt < 12: continue
        m = max(m, sens * (L[i][1] - L[i0][1]) / dt * 16.7); i0 = i
    return m
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
SUIVI = r"""()=>{ window.__S=[]; window.__go=true; (function f(){ const e=_aura.etat().emp; __S.push([performance.now(), e?Math.pow(e.p,2/3):0, e?(e.relache?1:0):-1]); if(window.__go) requestAnimationFrame(f); })(); }"""
REPOS = r"""()=>{ _aura.pelote(); const c=document.getElementById('auBoule'); window.__repos=new Uint8ClampedArray(c.getContext('2d').getImageData(0,0,c.width,c.height).data); return c.width; }"""
DIFF = r"""()=>{ _aura.pelote(); const c=document.getElementById('auBoule'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data, a=window.__repos; let n=0,s=0; for(let i=0;i<d.length;i+=4){ if(!d[i+3]) continue; const e=Math.abs(d[i]-a[i])+Math.abs(d[i+1]-a[i+1])+Math.abs(d[i+2]-a[i+2]); if(e>24){ n++; s+=e; } } const k=c.width/296; return {n:n/(k*k), s:s/(k*k)}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('geste_vu_pelote','1');}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5000)
    cdp = ctx.new_cdp_session(pg)
    pg.evaluate("()=>{_aura.fige(true); _aura.vue(3.1,0.32)}"); pg.wait_for_timeout(600)
    bo = pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left+r.width*0.45, r.top+r.height*0.5]}")
    def pose(rx, ry, rot=0): cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': bo[0], 'y': bo[1], 'radiusX': rx, 'radiusY': ry, 'rotationAngle': rot, 'force': 1}]})
    def leve(): cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    def repos():
        pg.wait_for_function("()=>!_aura.etat().emp", timeout=20000); pg.wait_for_timeout(300); pg.evaluate("()=>{_aura.fige(true); _aura.vue(3.1,0.32)}"); pg.wait_for_timeout(300); pg.evaluate(REPOS)
    # ── A à D, H : un appui de 3 s, rayon 12, puis le retour ──
    repos(); pg.evaluate(SUIVI); pose(12, 12); pg.wait_for_timeout(3000); leve(); pg.wait_for_timeout(5200)
    S = pg.evaluate("()=>{ window.__go=false; return __S; }")
    app = [s for s in S if s[2] == 0]; ret = [s for s in S if s[2] == 1]
    juge('0 · l\'appui est suivi image par image', len(app) > 60, '%d images d\'appui, %d de retour' % (len(app), len(ret)))
    if len(app) > 10:
        t0 = app[0][0]; recul = sum(1 for i in range(1, len(app)) if app[i][1] <= app[i - 1][1])
        juge('A · la profondeur croît à chaque image pendant l\'appui', recul == 0 and app[0][1] < 0.15, '%d image(s) sans progrès sur %d · première image à %.1f %% de la butée' % (recul, len(app), 100 * app[0][1]))
        pas = max(plus_grand_pas(app, 1), app[0][1])
        juge('C · aucun saut : le plus grand pas d\'une image ≤ %.0f %% de la butée' % (100 * PAS_MAX), pas <= PAS_MAX, 'plus grand pas %.1f %% (ramené à 16,7 ms)' % (100 * pas))
        def a_t(ms):
            c = [s for s in app if s[0] - t0 <= ms]; return c[-1][1] if c else 0
        V = [a_t(150 * (k + 1)) - a_t(150 * k) for k in range(18)]
        juge('B · la vitesse d\'enfoncement décroît (fenêtres de 150 ms)', all(V[k + 1] < V[k] for k in range(9)) and all(V[k + 1] < V[k] + 0.004 for k in range(9, len(V) - 1)) and V[0] > 4 * V[6], ' · '.join('%.1f' % (100 * v) for v in V[:10]) + ' … % de la butée')
        juge('D · une butée : > 90 %% à 3 s, jamais au-delà de 100 %%', 0.90 < app[-1][1] <= 1.0, 'à 0,3 s %.0f %% · 1 s %.0f %% · 3 s %.1f %%' % (100 * a_t(300), 100 * a_t(1000), 100 * app[-1][1]))
    if len(ret) > 10:
        t1 = ret[0][0]; d0 = app[-1][1]
        def r_t(ms):
            c = [s for s in ret if s[0] - t1 <= ms]; return c[-1][1] if c else d0
        pr = plus_grand_pas([app[-1]] + ret, -1)
        juge('H · au relâcher la fourrure revient lentement : à 0,6 s le creux fait encore ≥ 25 %', r_t(600) >= 0.25 * d0, 'à 0,3 s %.0f %% · 0,6 s %.0f %% · 1,5 s %.0f %% de sa profondeur' % (100 * r_t(300) / d0, 100 * r_t(600) / d0, 100 * r_t(1500) / d0))
        juge('H · le retour n\'a pas de saut non plus', pr <= PAS_MAX, 'plus grand pas %.1f %%' % (100 * pr))
        juge('H · à 5 s il n\'y a plus de creux', pg.evaluate("()=>!_aura.etat().emp"))
    # ── E : à l'écran, le creux grandit ──
    repos(); pose(12, 12); N = []
    for ms in (150, 450, 1900): pg.wait_for_timeout(ms); N.append(pg.evaluate(DIFF))
    leve()
    juge('E · à l\'écran, le creux grandit avec la durée de l\'appui (0,15 s → 0,6 s → 2,5 s)', N[0]['s'] > 0 and N[1]['s'] > 1.15 * N[0]['s'] and N[2]['s'] > 1.1 * N[1]['s'], ' → '.join('%d px, somme %d' % (x['n'], x['s']) for x in N))
    # ── F, G : la forme du contact ──
    R = {}
    for nom, rx, ry, rot in (('petit', 7, 7, 0), ('grand', 16, 16, 0), ('allonge', 16, 8, 0)):
        repos(); pose(rx, ry, rot); pg.wait_for_timeout(1500); e = pg.evaluate("()=>_aura.etat().emp"); R[nom] = (pg.evaluate(DIFF), e); leve()
    n1, n2 = R['petit'][0]['n'], R['grand'][0]['n']; a1, a2 = R['petit'][1]['a'], R['grand'][1]['a']
    juge('F · deux tailles de contact donnent deux empreintes différentes (pixels : ≥ 30 % d\'écart)', n1 > 0 and n2 >= 1.3 * n1, 'rayon 7 pt : %d px changés · rayon 16 pt : %d px' % (n1, n2))
    juge('F · … et à la cote : le demi-axe suit le contact', a2 > 1.5 * a1, 'demi-axe %.3f contre %.3f rayon de boule' % (a1, a2))
    eg, ea = R['grand'][1].get('el'), R['allonge'][1].get('el')
    juge('G · un contact allongé (16 × 8) donne une empreinte allongée, un contact rond une empreinte ronde', eg is not None and ea is not None and ea <= 0.7 and eg >= 0.9, 'rond %s · allongé %s' % (eg, ea))
    Gd = pg.evaluate("()=>[_aura.G.ENF_TAU, _aura.G.RETOUR_TAU]")
    juge('I · l\'app déclare les constantes décidées (0,60 s · 0,60 s)', Gd == [ENF_TAU, RETOUR_TAU], str(Gd))
    juge('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:10]))
sys.exit(1 if ko else 0)
