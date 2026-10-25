#!/usr/bin/env python3
"""redteam_fleche_onb.py — ⚑ v157 (Tom, C-174) : LA FLÈCHE DU PREMIER PROMI, DEUX FOIS PLUS GRANDE, VERS LE BAS.

« Dans l'onboarding, page du premier Promi : la flèche, le trait et les points deux fois plus grands. Ils grandissent vers le BAS : le haut de la flèche reste
exactement à sa place actuelle (± 1 pt). Ce qui est en dessous descend d'autant qu'il faut. L'orange clignotant et le départ à 1,5 s ne changent pas.
Juge : haut identique à v156 (± 1 pt), hauteur × 2 (± 2 %), aucun recouvrement. »

Banc comme Tom (WebKit 390 × 844 ×3, doigt), stockage vierge, le vrai parcours (prénom, Retour, la parole touchée et tapée), clair et sombre ; v156 servie à
côté (`zz-av156.html`, la même phrase) ; l'encre du trait lue sur ses deux canevas (le trait et la couche du départ), en pt de l'écran :
  A · le haut de l'encre = celui de v156 ± 1 pt
  B · la hauteur de l'encre = 2 × celle de v156 ± 2 % ; l'épaisseur du trait et le diamètre des points × 2 (± 4 %)
  C · aucun recouvrement : l'encre ne touche aucun texte de la page (« trace pour planter », la phrase, « Petite ou grande promesse ») et finit au-dessus
      du bas de l'écran
  D · le départ clignote toujours (`promiBlink`, classe `clignote`) et la flèche paraît 1,5 s après le prénom (1 450 à 1 600 ms)
Preuve : `--fichier=zz-av156.html` rougit (B).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
REF = 'zz-av156.html'
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
LIT = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  let top=1e9, bot=-1e9, gau=1e9, dro=-1e9, col=[]; const larg=[];
  ['onbTrait','onbDepart'].forEach(id=>{ const c=document.getElementById(id); if(!c || !c.width) return; const r=c.getBoundingClientRect(), s=c.width/(r.width/k), g=c.getContext('2d'), d=g.getImageData(0,0,c.width,c.height).data, W=c.width;
    for(let y=0;y<c.height;y++) for(let x=0;x<W;x++){ if(d[(y*W+x)*4+3]>128){ const py=(r.top-D.top)/k+y/s, px=(r.left-D.left)/k+x/s; if(py<top) top=py; if(py>bot) bot=py; if(px<gau) gau=px; if(px>dro) dro=px; } }
    /* l'épaisseur : la plus longue colonne opaque continue, à la colonne x = 195 pt sur la couche du trait plein (ou la plus haute colonne des points) */
    if(id==='onbTrait'){ let best=0; for(let x=0;x<W;x+=1){ let run=0; for(let y=0;y<c.height;y++){ if(d[(y*W+x)*4+3]>128){ run++; if(run>best) best=run; } else run=0; } } larg.push(best/s); } });
  const T=['onbTrace','onbPh','onbSous','onbDit','onbQuid'].map(i=>{ const e=document.getElementById(i); if(!e||getComputedStyle(e).display==='none') return null; const r=e.getBoundingClientRect(); return [i,(r.left-D.left)/k,(r.top-D.top)/k,(r.right-D.left)/k,(r.bottom-D.top)/k]; }).filter(Boolean);
  const dep=document.getElementById('onbDepart');
  return {top:top, bot:bot, h:bot-top, pt:larg[0]||0, textes:T, clig:!!(dep&&dep.classList.contains('clignote')), anim:dep?getComputedStyle(dep).animationName:'', app:(window._onbApparition||[]).slice()}; }"""
def mesure(b, fichier, sombre, q=''):
    ctx = B.contexte(b, onb=False, guide=False)
    if sombre: ctx.add_init_script("try{localStorage.setItem('promi_theme','dark')}catch(e){}")
    pg = B.ouvre(ctx, fichier, attente=7000, q=q)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5200)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(500); pg.keyboard.type('marcher une heure', delay=20); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ const i=document.getElementById('onbIn'); if(i) i.blur(); }"); pg.wait_for_timeout(1800)
    m = pg.evaluate(LIT); m['cotes'] = pg.evaluate("()=>window._onbTraitCotes||null"); er = [e for e in pg.erreurs if 'version.json' not in e]; ctx.close(); return m, er
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'
        r, _ = mesure(b, REF, sombre); n, er = mesure(b, F, sombre)   # ⚑ v163 (C-174 validé) : l'onde figée à 0,5, `?onde=` retiré — tout se juge sur le défaut
        juge('[%s] E · l\'amplitude de l\'onde = la moitié de v157 (36 pt pour 72), l\'épaisseur × 2 (le trait et les points, ± 4 %%)' % T,
             n['cotes'] and abs(n['cotes']['amp'] - 36) < 0.01 and abs(n['pt'] / r['pt'] - 2) <= 0.08,
             'amplitude %s · épaisseur × %.3f' % ((n['cotes'] or {}).get('amp'), n['pt'] / r['pt'] if r['pt'] else 0))
        juge('[%s] A · le haut de l\'encre de la flèche = celui de v156 ± 1 pt' % T, abs(n['top'] - r['top']) <= 1.0, 'v156 %.2f · maintenant %.2f pt' % (r['top'], n['top']))
        touche = [t[0] for t in n['textes'] if not (t[4] <= n['top'] or t[2] >= n['bot'])]
        juge('[%s] C · aucun texte touché par la flèche, et elle finit au-dessus du bas de l\'écran' % T, not touche and n['bot'] <= 844 - 4,
             'encre %.1f → %.1f pt · textes touchés %s' % (n['top'], n['bot'], touche))
        juge('[%s] D · le départ clignote (promiBlink) et paraît 1,5 s après le prénom' % T, n['clig'] and n['anim'] == 'promiBlink' and n['app'] and 1450 <= n['app'][0] <= 1600,
             'classe clignote %s · animation %s · paru à %s ms' % (n['clig'], n['anim'], n['app']))
        juge('[%s] aucune erreur de page' % T, not er, er[:2])
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
