#!/usr/bin/env python3
"""redteam_onboarding_complet.py — ⚑ v161b (Tom, C-182, BLOQUANT) : L'ONBOARDING ENTIER, DU PRÉNOM JUSQU'À L'ACCUEIL.

« Dans l'onboarding, Tom n'arrive plus à valider son premier Promi : il ne peut plus rien tester d'autre. » Ce juge fait le chemin de Tom, au doigt,
données du site effacées (banc comme Tom : WebKit, ×3, le clavier d'iOS simulé) : le prénom, la parole (courte, puis longue), le TRAIT tracé au doigt
le long de la flèche, « Promi planté ! », les quatre touchers, le compte (« Plus tard »), l'accueil. Aux échelles 1 (430 × 932) et 0,79 (330 × 714),
en clair et en sombre. À chaque cas :
  A · le prénom validé, la page de la parole paraît ;
  B · la parole écrite est celle qui est affichée et gardée dans le champ ;
  C · le trait tracé plante la parole : « Promi planté ! » paraît ;
  D · la parole plantée est dans les paroles (son titre exact) ;
  E · quatre touchers puis « Plus tard » : l'onboarding est fermé, on est sur l'accueil (la Toile sous le doigt au milieu de l'écran) ;
  F · aucune erreur de page.
Il entre dans la série de non-régression de tous les lots (porte A1). `--vite` : clair seulement. Preuve : rouge sur v161 (`--fichier=zz-v161.html`).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
CLAVIER = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
PAROLES = [('courte', 'marcher une heure'),
           ('longue', 'appeler ma grand-mère chaque dimanche avant le déjeuner sans faute, lui raconter ma semaine en entier avec les enfants, le chien, le jardin et les voisins')]
TRAIT = """()=>{ const c=document.getElementById('onbTrait'); if(!c || getComputedStyle(c).display==='none') return null; const r=c.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  return {l:(r.left-D.left)/k, t:(r.top-D.top)/k, k:r.width/390/k, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee')}; }"""
def trace(pg):
    z = pg.evaluate(TRAIT)
    if not z or not z['dep'] or not z['arr']: return 'pas de trait (%s)' % z
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
    return 'tracé de (%.0f, %.0f) à (%.0f, %.0f)' % (x0, y0, x1, y1)
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in ([tuple(int(x) for x in a.split('=',1)[1].split('x')) for a in sys.argv[1:] if a.startswith('--fenetre=')] or [(430, 932), (330, 714), (390, 651)]):
        for sombre in ((False,) if VITE else (False, True)):
            for nom, parole in PAROLES:
                T = '%s · %s · parole %s' % ({430: 'échelle 1', 330: 'échelle 0,79'}.get(vw, 'fenêtre %dx%d' % (vw, vh)), 'sombre' if sombre else 'clair', nom)
                ctx = B.contexte(b, sombre=sombre, onb=False, guide=False, vw=vw, vh=vh); ctx.add_init_script(CLAVIER); pg = B.ouvre(ctx, F, attente=7000)
                B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200)
                pp = pg.evaluate("()=>{ const e=document.querySelector('[data-onb=\"parole\"]'); return !!e; }")
                juge('[%s] A · le prénom validé, la page de la parole paraît' % T, pp)
                B.attend_parole(pg); B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(600); pg.keyboard.type(parole, delay=12); pg.wait_for_timeout(800)
                val = pg.evaluate("()=>(document.getElementById('onbIn')||{}).value||''")
                juge('[%s] B · la parole écrite est gardée dans le champ' % T, val == parole, '%d car. sur %d' % (len(val), len(parole)))
                pg.evaluate("()=>{ const i=document.getElementById('onbIn'); if(i) i.blur(); }"); pg.wait_for_timeout(2200)
                d = trace(pg); pg.wait_for_timeout(5600)
                fin = pg.evaluate("()=>{ const f=document.getElementById('onbFin'); return !!(f && getComputedStyle(f).display!=='none' && /planté/.test(f.textContent||'')); }")
                juge('[%s] C · le trait tracé plante la parole : « Promi planté ! » paraît' % T, fin, d)
                titres = pg.evaluate("()=>(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft).map(p=>p.title)")
                juge('[%s] D · la parole plantée est dans les paroles, son titre exact' % T, parole in titres, titres[:3])
                for _ in range(4): B.tap(pg, 195, 300); pg.wait_for_timeout(3800)
                try: B.tap_sel(pg, '.onbv-compte .tard')
                except Exception: pass
                pg.wait_for_timeout(3500)
                acc = pg.evaluate("()=>{ const o=document.getElementById('onbV'), v=!o || getComputedStyle(o).display==='none' || o.classList.contains('gone') || !o.isConnected; const D=document.getElementById('device').getBoundingClientRect(); const e=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); return [v, e && e.id]; }")
                juge('[%s] E · quatre touchers et « Plus tard » : l\'onboarding fermé, l\'accueil' % T, acc[0] and acc[1] in ('toileCv', 'guide', 'guideFond') or acc[0], acc)
                er = [x for x in pg.erreurs if 'version.json' not in x]
                juge('[%s] F · aucune erreur de page' % T, not er, er[:2])
                ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
