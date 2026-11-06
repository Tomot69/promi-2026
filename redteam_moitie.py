#!/usr/bin/env python3
"""redteam_moitie.py — ⚑ v180a (Tom, C-237) : « planter, c'est tracer la PREMIÈRE MOITIÉ du trait, comme dans l'onboarding, et pas plus ».

Banc WebKit (banc_tom), au doigt, échelles 1 (430 × 932) et 0,79 (330 × 714), Promi et Chiche :
  A · lâché avant la moitié (50 → 150 pt) : rien n'est planté, la page + reste ouverte.
  B · tracé au-delà (50 → 235 pt) : le plein ne passe jamais le milieu (195) ; la parole est plantée quand le doigt arrive au milieu, avant le lever.
  C · la dalle naît au milieu du trait (± 2 pt) — et SA NAISSANCE EST CELLE DE L'ONBOARDING, image par image : la même transition, la même échelle à
      la première image (≤ 0,1), le même sommet (± 0,03), le même temps pour atteindre 0,8 (± 50 ms), le même départ du vol (± 50 ms), l'échelle 1 à l'arrivée.
  D · elle rejoint sa cellule sur la Toile (son centre à 4 pt de la cellule) ; la page + est fermée, la couche de la naissance retirée.
  E · la parole est enregistrée dans le stockage dans les 50 ms du trait (C-226).
  F · le Cercle ne change pas : son trait entier plante par l'ancien chemin, aucune naissance.
Rouge sur v179b (`--fichier=zz-v179b.html`).
"""
import sys, time, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
SONDE = """()=>{ if(window.__nd) return; window.__nd=[]; window.__dm=0; var t0=null, el=null;
  (function f(){ var e=document.querySelector('.onbv-dalle'); var d=window._ppDoigt; if(typeof d==='number') window.__dm=Math.max(window.__dm,d);
    if(e && e!==el){ el=e; t0=performance.now(); window.__nd=[]; window.__ndTr=e.style.transition; }
    if(el && el.isConnected){ var D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=el.getBoundingClientRect(), m=new DOMMatrix(getComputedStyle(el).transform);
      window.__nd.push({t:performance.now()-t0, s:Math.hypot(m.a,m.b), cx:(r.left+r.width/2-D.left)/k, cy:(r.top+r.height/2-D.top)/k}); }
    requestAnimationFrame(f); })(); }"""
def courbe(pg): return pg.evaluate("()=>window.__nd.slice()")
def cles(c):
    if not c: return None
    pic = max((x['s'] for x in c if x['t'] <= 700), default=0)
    t08 = next((x['t'] for x in c if x['s'] >= 0.8), None)
    vol = next((x['t'] for x in c if x['t'] > 700 and abs(x['cx'] - c[0]['cx']) + abs(x['cy'] - c[0]['cy']) > 1.5), None)
    return {'s0': round(c[0]['s'], 3), 'pic': round(pic, 3), 't08': None if t08 is None else round(t08), 'vol': None if vol is None else round(vol), 'fin': round(c[-1]['s'], 3), 'c0': (round(c[0]['cx'], 1), round(c[0]['cy'], 1)), 'n': len(c)}
def onboarding(b):
    ctx = B.contexte(b, onb=False, guide=False, vw=430, vh=932); pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(350); pg.keyboard.type('marcher', delay=15); pg.keyboard.press('Enter'); pg.wait_for_timeout(1900)
    pg.evaluate(SONDE)
    D = pg.evaluate("()=>{ var D=document.getElementById('device').getBoundingClientRect(), r=document.getElementById('onbTrait').getBoundingClientRect(); return (r.top-D.top)/(D.width/390); }")
    pts = [[x, D + pg.evaluate("x=>{ const c=window._onbTraitCotes, y=window._onde.onde(c.base,c.amp); return y(x); }", x)] for x in range(44, 212, 12)]
    B.glisse(pg, pts, pas=18, tenue=40); pg.wait_for_timeout(1900)
    c = courbe(pg); tr = pg.evaluate("()=>window.__ndTr"); ctx.close(); return c, tr
def ouvre_nature(pg, k):
    pg.evaluate("()=>{ try{window._peaufSortie&&_peaufSortie();closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(750); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k)
    for _ in range(50):
        pg.wait_for_timeout(120)
        if pg.evaluate("k=>{var s=document.getElementById('createSheet');return !!(s&&s.classList.contains('pp-'+k)&&!s.classList.contains('pp-choix')&&!s.classList.contains('acc-passe'))}", k): break
    pg.wait_for_timeout(1400)
def remplit(pg, k, txt):
    pg.evaluate("a=>{const f=document.getElementById(a[0]==='nuee'?'nName':'fTitle');f.value=a[1];f.dispatchEvent(new Event('input',{bubbles:true}));if(window._ppTout)_ppTout()}", [k, txt])
    for _ in range(60):
        if pg.evaluate("()=>{const e=window._ppInvite&&window._ppInvite.etat();return !!(e&&e.visible&&!e.sortie&&!e.descend)}"): break
        pg.wait_for_timeout(100)
    pg.wait_for_timeout(900)
def points(pg, xs):
    return pg.evaluate("xs=>{const e=_ppEcran(),y=_onde.onde(e.base,e.amp),D=document.getElementById('device').getBoundingClientRect(),k=D.width/390,r=document.getElementById('csTrameCv').getBoundingClientRect(),o=(r.top-D.top)/k;return xs.map(x=>[x,o+y(x)])}", xs)
def n_paroles(pg): return pg.evaluate("()=>promises.filter(p=>!p.draft).length")
REF = None
def un(b, k, vw, vh, nom):
    global REF
    T = '[%s · %s]' % (k, nom)
    ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F); pg.evaluate(SONDE)
    # A
    ouvre_nature(pg, k); remplit(pg, k, 'courir un marathon'); n0 = n_paroles(pg)
    B.glisse(pg, points(pg, [50, 80, 110, 150]), pas=18, tenue=380); pg.wait_for_timeout(1200)
    juge(T + ' A · lâché avant la moitié : rien n\'est planté, la page + reste ouverte', n_paroles(pg) == n0 and pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')"), 'paroles %d → %d' % (n0, n_paroles(pg)))
    # B
    pg.evaluate("()=>{ window.__dm=0; window.__plante=null; var n=promises.length; (function f(){ if(promises.length>n && !window.__plante){ window.__plante={t:performance.now(), doigt:window._ppDoigt, st:(localStorage.getItem('promi_state')||'').indexOf('courir un marathon')>=0}; } if(!window.__plante) requestAnimationFrame(f); })(); window.__leve=null; window.addEventListener('touchend',function(){ if(!window.__leve) window.__leve=performance.now(); },{capture:true,once:true}); }")
    pts = points(pg, [50, 80, 110, 140, 170, 195, 215, 235]); y195 = pts[5][1]
    B.glisse(pg, pts, pas=18, tenue=380); pg.wait_for_timeout(2900)
    pl = pg.evaluate("()=>window.__plante"); lv = pg.evaluate("()=>window.__leve"); dm = pg.evaluate("()=>window.__dm")
    juge(T + ' B · le plein ne passe jamais le milieu ; planté au milieu, avant le lever', dm <= 195.5 and pl and lv and pl['t'] < lv, 'doigt max %.1f · planté %s · levé %s' % (dm, pl and round(pl['t']), lv and round(lv)))
    c = courbe(pg); K = cles(c); tr = pg.evaluate("()=>window.__ndTr")
    juge(T + ' C · la dalle naît au milieu du trait (± 2 pt)', K and abs(K['c0'][0] - 195) <= 2 and abs(K['c0'][1] - y195) <= 2, 'naissance %s · trait (195, %.1f)' % (K and K['c0'], y195))
    R = REF
    okc = bool(K and R and tr == R['tr'] and K['s0'] <= 0.1 and abs(K['pic'] - R['k']['pic']) <= 0.03 and K['t08'] is not None and R['k']['t08'] is not None and abs(K['t08'] - R['k']['t08']) <= 50
               and K['vol'] is not None and R['k']['vol'] is not None and abs(K['vol'] - R['k']['vol']) <= 50 and abs(K['fin'] - pg.evaluate("()=>{ const c=window._cibleDalle(promises[promises.length-1].id); return c ? c.w/(window._naissanceW?window._naissanceW():c.w) : 1; }")) <= 0.03)   # v182a (C-237, C-247) : la dalle naît à la taille de l'onboarding et se pose à la taille de SA cellule (l'onboarding : sa cellule fait déjà sa taille, l'échelle y reste 1)
    juge(T + ' C · la naissance est celle de l\'onboarding, image par image', okc, 'page + %s · onboarding %s' % (K, R and R['k']))
    dern = c[-1] if c else None
    cib = pg.evaluate("()=>{ var p=promises[promises.length-1]; return window._cibleDalle?window._cibleDalle(p.id):null; }")
    ferme = pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('show') && !document.getElementById('ppNait')")
    dd = None if not (dern and cib) else max(abs(dern['cx'] - (cib['x'] + cib['w'] / 2)), abs(dern['cy'] - (cib['y'] + cib['h'] / 2)))
    juge(T + ' D · elle rejoint sa cellule sur la Toile ; la page + fermée, la couche retirée', dd is not None and dd <= 4 and ferme, 'écart %s pt · fermée %s' % (dd and round(dd, 1), ferme))
    juge(T + ' E · la parole est enregistrée au trait (C-226)', pl and pl['st'], pl)
    ctx.close()
def cercle(b):
    ctx = B.contexte(b); pg = B.ouvre(ctx, F); pg.evaluate(SONDE)
    ouvre_nature(pg, 'nuee'); remplit(pg, 'nuee', 'les voisins'); n0 = len(pg.evaluate("()=>Object.keys(NUE)"))
    pg.evaluate("()=>{ window.__vu=false; (function f(){ if(document.getElementById('ppNait')) window.__vu=true; requestAnimationFrame(f); })(); }")
    B.glisse(pg, points(pg, [40, 100, 160, 220, 280, 340, 372]), pas=18, tenue=380); pg.wait_for_timeout(2600)
    n1 = len(pg.evaluate("()=>Object.keys(NUE)")); vu = pg.evaluate("()=>window.__vu")
    juge('[nuee] F · le Cercle : trait entier, planté par l\'ancien chemin, aucune naissance', n1 == n0 + 1 and not vu, 'Cercles %d → %d · naissance %s' % (n0, n1, vu))
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    c, tr = onboarding(b); REF = {'k': cles(c), 'tr': tr}
    print('  onboarding :', REF['k'], tr)
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for k in ('promi', 'chiche'):
            try: un(b, k, vw, vh, nom)
            except Exception as e: juge('[%s %s] le chemin va au bout' % (k, nom), False, str(e)[:200])
    try: cercle(b)
    except Exception as e: juge('[nuee] le chemin va au bout', False, str(e)[:200])
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
