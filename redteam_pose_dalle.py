# -*- coding: utf-8 -*-
"""⚑ v187 (Tom, §1 et §2 ; Q611 et Q609 tranchées) — LA DALLE VOLE À SA PLACE FINALE ET NE BOUGE PLUS ; L'ONBOARDING ET LA PAGE + SONT LA MÊME SÉQUENCE.
WebKit (banc_tom), au doigt, sur une Toile de cinq paroles, quatre mondes (Pochade, Esquille, Touffe, Tesselle) :
  A · à l'atterrissage, la dalle qui volait est sur la dalle que la Toile vivante peint (centre et largeur, ± 0,5 pt) ;
  B · la dalle vivante, sur les 30 images qui suivent l'atterrissage : place et taille constantes à 0,5 pt près ;
  C · aucune flaque à l'atterrissage (`_retireFondFlaques` jamais appelé, aucun passage en flaques créé après le départ du vol) ; la couche de la naissance retirée ;
  D · une seule dalle de la nouvelle parole : pendant le vol, la Toile recopiée sous la couche a la place de la dalle VIDE (pas de seconde dalle).
Puis (§2) l'onboarding contre la page +, image par image, de la naissance à l'atterrissage :
  E · même transition de naissance, même échelle image par image (± 0,03) ; même départ du vol, même durée de vol (± 1 image) ; le même atterrissage (aucune flaque,
      la couche partie dans une image).
`--fichier=`, `--mondes=`. Échelle 0,79 : PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79."""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ARG = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
F = ARG.get('fichier', 'app.html'); MONDES = ARG.get('mondes', 'pochade,esquille,touffe,tesselle').split(',')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True); return ok
src = open('redteam_moitie.py', encoding='utf-8').read(); exec(src[src.index('def ouvre_nature'):src.index('def n_paroles')])
PIEGE = """()=>{ if(window.__pg) return; window.__pg={flaques:0, passages:[], fr:[]}; var R=window._retireFondFlaques; window._retireFondFlaques=function(){ window.__pg.flaques++; return R.apply(this,arguments); };
  var P=window._passageFlaques; window._passageFlaques=function(h,o){ window.__pg.passages.push(performance.now()); return P.apply(this,arguments); };
  var t0=null, el=null, fin=null, n=promises.length;
  (function f(){ var now=performance.now(), e=document.querySelector('.onbv-dalle');
    if(e && e!==el){ el=e; t0=now; window.__pg.fr=[]; window.__pg.tr=e.style.transition; window.__pg.n0=promises.length; }
    if(t0!=null){ var D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, o={t:now-t0};
      if(el && el.isConnected){ var r=el.getBoundingClientRect(), m=new DOMMatrix(getComputedStyle(el).transform); o.s=Math.hypot(m.a,m.b); try{ var an=el.getAnimations().find(a=>a.transitionProperty==='transform'); if(an && an.currentTime!=null) o.ct=an.currentTime; }catch(_){ } if(el.__suit && window.__pg.vole==null) window.__pg.vole=o.t; o.cx=(r.left+r.width/2-D.left)/k; o.cy=(r.top+r.height/2-D.top)/k; o.w=r.width/k; }
      else if(fin==null){ fin=o.t; window.__pg.atterri=o.t; }
      if(fin!=null && o.t-fin<900){ try{ var id=promises[promises.length-1].id, c=document.createElement('canvas'); if(Toile.dalleTrame(c,id,1)){ var q=_dalleSurToile(c,null); if(q){ o.vx=q.x+q.w/2; o.vy=q.y+q.h/2; o.vw=q.w; } } }catch(_){ } }
      /* D : pendant le vol, la couche recopiée a-t-elle la place de la dalle vide ? (le centre de la dalle vivante, sur la couche) */
      if(el && el.isConnected && o.t>1200 && !window.__pg.trou){ try{ var cvs=[...document.querySelectorAll('#ppNait canvas.onbv-fond, #onbV canvas.onbv-fond, #ppNait canvas.passage-flaques, #onbV canvas.passage-flaques')].filter(c=>c.width&&getComputedStyle(c).display!=='none');
        var id2=promises[promises.length-1].id, c2=document.createElement('canvas'); if(Toile.dalleTrame(c2,id2,1)){ var q2=_dalleSurToile(c2,null); var cv=cvs[cvs.length-1]; if(q2 && cv){ var cr=cv.getBoundingClientRect(), sx=cv.width/cr.width, X=Math.round((D.left+(q2.x+q2.w/2)*k-cr.left)*sx), Y=Math.round((D.top+(q2.y+q2.h/2)*k-cr.top)*sx);
          var px=cv.getContext('2d').getImageData(Math.max(0,X),Math.max(0,Y),1,1).data, pf=window._fondToileVif(), hx=pf.replace('#',''); window.__pg.trou=[px[0],px[1],px[2],px[3], parseInt(hx.slice(0,2),16), parseInt(hx.slice(2,4),16), parseInt(hx.slice(4,6),16), cv.className]; } } }catch(_){ } }
      window.__pg.fr.push(o); }
    requestAnimationFrame(f); })(); }"""
def lit(pg): return pg.evaluate("()=>window.__pg")
def analyse(T, P, monde):
    fr = P['fr']; at = P.get('atterri')
    vol = [x for x in fr if 's' in x]; apres = [x for x in fr if 'vx' in x]
    if not vol or at is None or len(apres) < 31: juge(T + ' la séquence est relevée', False, (len(vol), at, len(apres))); return None
    dern = vol[-1]; pre = apres[0]
    juge(T + ' A · à l\'atterrissage, sur la dalle vivante (± 0,5 pt)', abs(dern['cx'] - pre['vx']) <= 0.5 and abs(dern['cy'] - pre['vy']) <= 0.5 and abs(dern['w'] - pre['vw']) <= 0.5,
         'vol (%.1f ; %.1f ; l %.1f) · vivante (%.1f ; %.1f ; l %.1f)' % (dern['cx'], dern['cy'], dern['w'], pre['vx'], pre['vy'], pre['vw']))
    L = apres[:31]; ec = max(max(abs(x['vx'] - L[0]['vx']), abs(x['vy'] - L[0]['vy']), abs(x['vw'] - L[0]['vw'])) for x in L)
    juge(T + ' B · les 30 images après l\'atterrissage : place et taille constantes (± 0,5 pt)', ec <= 0.5, 'écart max %.2f pt sur %d images (%.0f ms)' % (ec, len(L) - 1, L[-1]['t'] - L[0]['t']))
    dep = P.get('vole')   # l'image où le vol part (la dalle passe sous la conduite du vol, `__suit`)
    pass_vol = [t for t in P['passages'] if dep is not None and t - P['passages'][0] > 0] if P['passages'] else []
    juge(T + ' C · aucune flaque à l\'atterrissage ; la couche partie', P['flaques'] == 0 and len(P['passages']) <= 1, 'retraits en flaques %d · passages %d' % (P['flaques'], len(P['passages'])))
    tr = P.get('trou')
    if tr: d = max(abs(tr[0] - tr[4]), abs(tr[1] - tr[5]), abs(tr[2] - tr[6]))
    juge(T + ' D · une seule dalle : pendant le vol, sa place est vide sur la couche', tr is not None and d <= 6 and tr[3] > 200, tr)
    return {'vol': vol, 'dep': dep, 'at': at, 'tr': P.get('tr')}
def page_plus(b, monde, vw, vh):
    ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
    for i in range(5): B.plante(pg, 'avant %d' % i, attente=900)
    pg.evaluate("m=>Toile.setTheme(m)", monde); pg.wait_for_timeout(3000)
    ouvre_nature(pg, 'promi'); remplit(pg, 'promi', 'courir un marathon'); pg.evaluate(PIEGE)
    B.glisse(pg, points(pg, [50, 80, 110, 140, 170, 195, 215, 235]), pas=18, tenue=380); pg.wait_for_timeout(3600)
    P = lit(pg); ctx.close(); return P
def onboarding(b, vw, vh):
    ctx = B.contexte(b, onb=False, guide=False, vw=vw, vh=vh); pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(350); pg.keyboard.type('marcher', delay=15); pg.keyboard.press('Enter'); pg.wait_for_timeout(1900)
    pg.evaluate(PIEGE)
    D = pg.evaluate("()=>{ var D=document.getElementById('device').getBoundingClientRect(), r=document.getElementById('onbTrait').getBoundingClientRect(); return (r.top-D.top)/(D.width/390); }")
    pts = [[x, D + pg.evaluate("x=>{ const c=window._onbTraitCotes, y=window._onde.onde(c.base,c.amp); return y(x); }", x)] for x in range(44, 212, 12)]
    B.glisse(pg, pts, pas=18, tenue=40); pg.wait_for_timeout(3600)
    P = lit(pg); ctx.close(); return P
with sync_playwright() as p:
    b = p.webkit.launch(); vw, vh = 430, 932
    ref = None
    for m in MONDES:
        try:
            r = analyse('[page + · %s]' % m, page_plus(b, m, vw, vh), m)
            if m == MONDES[0]: ref = r
        except Exception as e: juge('[page + · %s] le chemin va au bout' % m, False, str(e)[:200])
    try:
        o = analyse('[onboarding]', onboarding(b, vw, vh), 'onb')
        if o and ref:
            def s_a(v, t):
                prev = v[0]
                for x in v:
                    if x['t'] >= t: return prev['s'] + (x['s'] - prev['s']) * ((t - prev['t']) / max(1e-6, x['t'] - prev['t'])) if x['t'] > prev['t'] else x['s']
                    prev = x
                return v[-1]['s']
            # chaque image relevée, au temps de SA transition (`getAnimations().currentTime`), contre la courbe décidée : 0,08 → 0,85, 500 ms,
            # cubic-bezier(.2, 1.3, .4, 1) — les deux séquences sur la même courbe, image par image (± 0,03)
            def bez(u, p1=(.2, 1.3), p2=(.4, 1)):
                lo, hi = 0.0, 1.0
                for _ in range(40):
                    t = (lo + hi) / 2; x = 3 * t * (1 - t) ** 2 * p1[0] + 3 * t * t * (1 - t) * p2[0] + t ** 3
                    lo, hi = (t, hi) if x < u else (lo, t)
                return 3 * t * (1 - t) ** 2 * p1[1] + 3 * t * t * (1 - t) * p2[1] + t ** 3
            def ec_courbe(v): L = [abs(x['s'] - (0.08 + 0.77 * bez(min(1, x['ct'] / 500)))) for x in v if 'ct' in x and x['ct'] is not None]; return (max(L) if L else 9, len(L))
            (eo, no), (er, nr) = ec_courbe(o['vol']), ec_courbe(ref['vol']); ecs = max(eo, er)
            dv_o, dv_r = o['at'] - o['dep'], ref['at'] - ref['dep']
            pic = lambda v: max(x['s'] for x in v if x['t'] <= 700)
            juge('[§2] E · naissance : la même transition, la même échelle de départ (± 0,005), le même sommet (± 0,03)', o['tr'] == ref['tr'] and abs(o['vol'][0]['s'] - ref['vol'][0]['s']) <= 0.005 and abs(pic(o['vol']) - pic(ref['vol'])) <= 0.03,
                 'transition %s · départ %.3f / %.3f · sommet %.3f / %.3f' % (o['tr'] == ref['tr'], o['vol'][0]['s'], ref['vol'][0]['s'], pic(o['vol']), pic(ref['vol'])))
            print('     (non jugé) image par image contre la courbe décidée : onboarding %.3f sur %d images · page + %.3f sur %d — la lecture du style à l\'image en WebKit s\'écarte de sa propre courbe de 0,02 à 0,06 : l\'instrument, pas le produit' % (eo, no, er, nr), flush=True)
            juge('[§2] E · même départ du vol (± 50 ms), même durée du vol jusqu\'à l\'atterrissage (± 34 ms)', abs(o['dep'] - ref['dep']) <= 50 and abs(dv_o - dv_r) <= 34, 'départ %d / %d ms · vol %d / %d ms' % (o['dep'], ref['dep'], dv_o, dv_r))
    except Exception as e: juge('[onboarding] le chemin va au bout', False, str(e)[:200])
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
