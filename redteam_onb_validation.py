"""⚑ v199 (Tom, §1 URGENT) — LA VALIDATION DU PREMIER PROMI DE L'ONBOARDING, IMAGE PAR IMAGE.
« À la fin de l'animation de validation du premier Promi, il y a un sursaut et un décalage, et la dalle se dédouble. »
LA CAUSE (v199, présente depuis v183b donc dans v196) : la dalle rendue au trait déclarait la boîte de sa cellule NAISSANTE (`cel`) ; `_dalleSurToile` lisait la
croissance de la cellule comme un déplacement et visait ≈ 126 pt à côté : la dalle volait vers une fausse place, la couche de la Toile d'avant y laissait son trou
(la vraie dalle visible dessus : deux dalles), puis la cible relue en fin de vol la faisait glisser de 100 pt d'un coup.
Relevé à CHAQUE image (requestAnimationFrame, dans la page) du trait à l'atterrissage, la place finale lue sur un rendu de la Toile vivante :
 A · une seule dalle : le trou de la couche (la place de la dalle vivante cachée) est sur la dalle vivante (± 3 pt), à chaque image où la couche est là ;
 B · aucun décalage : la dalle qui vole reste sur la droite de son départ à sa place finale (± 6 pt), à chaque image du vol ;
 C · aucun sursaut : posée à sa place (± 1,5 pt) à la dernière image avant l'atterrissage, et la dalle vivante au même endroit à l'image d'après (± 1,5 pt) ;
 D · la même chose que v196 hors de cela : la dalle naît (taille, place) comme en v196 (± 1 pt) — `--ref=zz-v196.html`.
`--fichier=`, échelles par PYTHONPATH (scratchpad/v186/echelle079, scratchpad/v190/fenetretom). Rouge sur v196 (A, B)."""
import sys, json, math; sys.path.insert(0, '.')
src = open('redteam_onb_ordre.py').read(); ns = {}; exec(src[:src.index('def premier_parcours')], ns); B = ns['B']
from playwright.sync_api import sync_playwright
ARG = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
F = ARG.get('fichier', 'app.html'); REF = ARG.get('ref', 'zz-v196.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, d), flush=True)
PIEGE = """()=>{ const f=window._fondVivant; if(f && !f.__j){ window._fondVivant=function(){ const c=f.apply(this,arguments); window.__viv=c; return c; }; window._fondVivant.__j=1; }
 const a=window._atterrit; if(a && !a.__j){ window._atterrit=function(){ window.__tAtt=performance.now(); return a.apply(this,arguments); }; window._atterrit.__j=1; }
 window.__fr=[]; const D=document.getElementById('device');
 function f2(){ const R=D.getBoundingClientRect(), k=R.width/(D.offsetWidth||390); const dc=document.querySelector('.onbv-dalle'); let d=null;
   if(dc && dc.parentNode){ const r=dc.getBoundingClientRect(); d=[(r.left-R.left)/k,(r.top-R.top)/k,r.width/k,r.height/k]; }
   const fo=document.querySelector('.onbv-fond'); const cv=!!(fo && fo.parentNode && getComputedStyle(fo).display!=='none');
   const h=window.__viv && window.__viv.r ? [window.__viv.r.x,window.__viv.r.y,window.__viv.r.w,window.__viv.r.h] : null;
   window.__fr.push({t:performance.now(), d:d, couche:cv, trou:h}); if(window.__fr.length<900) requestAnimationFrame(f2); }
 requestAnimationFrame(f2); }"""
VIVANT = """()=>{ const np=promises[promises.length-1]; const lc=document.createElement('canvas'); if(!Toile.dalleTrame(lc, np.id, 1)) return null; const r=window._dalleSurToile(lc, null); return r?[r.x,r.y,r.w,r.h]:null; }"""
def passe(b, fichier):
    ctx, pg = ns['debut'](b, fichier, 390, 844, False)
    pg.keyboard.press('Enter'); ns['attend'](pg, "()=>{ const q=(window.__tr||[]).filter(x=>x.id==='onbPh')[0]; return q&&q.t1>0; }", 9000)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(450); pg.keyboard.type('marcher une heure', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter')
    ns['attend'](pg, "()=>{ const t=document.getElementById('onbTrait'); return t&&getComputedStyle(t).display!=='none'; }", 3000); pg.wait_for_timeout(1500)
    Y = pg.evaluate(ns['RECTS'])['onbTrait'][1]
    pts = [[x, Y + pg.evaluate("x=>{ const c=window._onbTraitCotes, y=window._onde.onde(c.base,c.amp); return y(x); }", x)] for x in range(44, 212, 12)]
    pg.evaluate(PIEGE); B.glisse(pg, pts, pas=18, tenue=40)
    ns['attend'](pg, "()=>!!window.__tAtt", 6000); pg.wait_for_timeout(700)
    fr = pg.evaluate("()=>window.__fr"); tA = pg.evaluate("()=>window.__tAtt"); fin = pg.evaluate(VIVANT)
    err = [e for e in pg.erreurs if 'version.json' not in e]; ctx.close()
    return fr, tA, fin, err
def c(r): return (r[0] + r[2] / 2, r[1] + r[3] / 2)
with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_onb_validation — %s (réf. %s), charge %.1f, échelle %s' % (F, REF, B.charge(), __import__('os').environ.get('PROMI_ECHELLE', '1')))
    fr, tA, fin, err = passe(b, F)
    vol = [x for x in fr if x['d'] and x['t'] < tA]
    juge('aucune erreur de page', not err, err[:2])
    juge('la dalle a volé et s\'est posée (images relevées)', fin is not None and len(vol) >= 10 and tA, '%d images · place vivante %s' % (len(vol), fin and [round(v, 1) for v in fin]))
    if fin and vol:
        cf = c(fin)
        trous = [math.dist(c(x['trou']), cf) for x in fr if x['couche'] and x['trou'] and x['t'] >= vol[0]['t'] + 250 and x['t'] < tA]
        juge('A · une seule dalle : le trou de la couche est sur la dalle vivante (± 3 pt), à chaque image', trous and max(trous) <= 3, 'écart max %.1f pt sur %d images' % (max(trous) if trous else -1, len(trous)))
        # la droite du départ (première image du vol, quand la dalle part de sa naissance) à la place finale
        dep = next((x for x in vol if x['d'][2] > 90), vol[0]); a0 = c(dep['d'])
        def ecart(q):
            ax, ay = a0; bx, by = cf; px, py = q; L = math.dist(a0, cf) or 1
            return abs((bx - ax) * (ay - py) - (ax - px) * (by - ay)) / L
        hors = [ecart(c(x['d'])) for x in vol if x['t'] >= dep['t']]
        juge('B · aucun décalage : la dalle reste sur la droite de son départ à sa place finale (± 6 pt), à chaque image du vol', hors and max(hors) <= 6, 'écart max %.1f pt sur %d images' % (max(hors) if hors else -1, len(hors)))
        der = vol[-1]; dpos = math.dist(c(der['d']), cf); pas_v = math.dist(c(vol[-1]['d']), c(vol[-2]['d'])) if len(vol) > 1 else 0
        juge('C · aucun sursaut : de la dernière image du vol à la dalle vivante, un pas pas plus grand que le dernier pas du vol (ou ≤ 1,5 pt), la taille ± 2 pt', dpos <= max(1.5, pas_v + 0.5) and abs(der['d'][2] - fin[2]) <= 2, 'pas à l\'atterrissage %.1f pt · dernier pas du vol %.1f pt · largeur %.1f' % (dpos, pas_v, abs(der['d'][2] - fin[2])))
        apres = [x for x in fr if x['t'] > tA]
        juge('C · à l\'atterrissage, la dalle qui volait part dans la même image (plus de dalle volante après)', apres and all(not x['d'] for x in apres[1:]), '%d images après' % len(apres))
    if REF and REF != F:
        fr2, tA2, fin2, _ = passe(b, REF)
        def palier(F_):   # la naissance posée : 700 ms après la première image de la dalle (sa croissance dure 500 ms, le vol part à 808 ms)
            L = [x for x in F_ if x['d']]; t1 = L[0]['t'] if L else 0
            return min(L, key=lambda x: abs(x['t'] - (t1 + 700)))['d'] if L else None
        n1, n2 = palier(fr), palier(fr2)
        juge('D · la naissance est celle de %s : la dalle posée sur le trait, 700 ms après sa naissance, avant le vol (centre ± 1,5 pt, largeur ± 4 pt : la cellule naissante, relevée au trait)' % REF, n1 and n2 and math.dist(c(n1), c(n2)) <= 1.5 and abs(n1[2] - n2[2]) <= 4, '%s / %s' % (n1 and [round(v, 1) for v in n1], n2 and [round(v, 1) for v in n2]))
        juge('D · la place finale est celle de %s (± 1 pt)' % REF, fin and fin2 and max(abs(u - v) for u, v in zip(fin, fin2)) <= 1.0, '%s / %s' % ([round(v, 1) for v in fin] if fin else None, [round(v, 1) for v in fin2] if fin2 else None))
    b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
