#!/usr/bin/env python3
"""redteam_onb_toucher.py — ⚑ v175 (Tom, C-219) : L'ONBOARDING, LE TEXTE PART AU TOUCHER, SANS LATENCE.

« Quand on touche pour faire apparaître le texte suivant, il commence trop tard, et ça bugue un peu. Le tracé démarre dans l'image qui suit le toucher (16 ms au plus) :
le texte suivant est prêt AVANT le toucher. »

Banc comme Tom (WebKit, doigt), le vrai parcours jusqu'à « Promi planté ! », aux échelles 1 et 0,79 ; aux trois touchers de cette page :
  A · la plume part à l'image qui suit le toucher : le compte d'IMAGES (il ne dépend pas de la charge), lu dans la page (une boucle d'images, `ctl.etat()`) ;
  B · le texte est prêt avant le toucher : aucun calcul de lettre après lui (`TraceLettres.mesures` : ce qui vient du cache ne se recalcule pas) ;
  C · en millisecondes (≤ 34 ms, deux images d'iPhone au plus, à cause de l'horloge de la boucle) : au calme seulement, sinon NON JUGÉ (C-137) ;
  D · le bloc qui se place n'emporte pas l'encre à côté de son texte : le canevas du tracé reste sur sa ligne pendant le mouvement.
Preuve : `--fichier=zz-v175a.html` rougit (A : le tracé part 272 ms après le toucher, sur le `click`).
Le relevé dans Safari iOS se lit avec `?diag=1` (`attente` de `trace-fin`, `mesures/appareil.jsonl`).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', n, str(d)[:230]), flush=True)
SONDE = r"""(()=>{ window.__S={tou:[], cal:[], im:[]}; const T=window.TraceLettres, tr=T.trace; let actifs=[]; const cpt=()=>{ const m=T.mesures||{}; return {prep:(m.prep||[]).length, restes:(m.restes||[]).length, cache:m.cache||0, cacheR:m.cacheR||0}; };
  T.trace=function(e,c,o){ const ctl=tr.apply(this,arguments); if(!(o&&o.preparer)){ const r={ctl:ctl, t0:performance.now(), el:e, prem:null, tx:(e.textContent||'').slice(0,24)}; actifs.push(r); __S.cal.push(r); } return ctl; };
  window.addEventListener('touchend', e=>{ __S.tou.push({t:performance.now(), n:0, m:cpt()}); }, true);
  (function f(ts){ const n=performance.now(); __S.tou.forEach(x=>{ if(x.prem==null){ x.n++; (x.j=x.j||[]).push([Math.round(n-x.t), ts?Math.round(ts-x.t):null, actifs.map(r=>{ try{ const e=r.ctl.etat(); return [e.t, e.glyphe, (e.actives||[]).length]; }catch(_){ return 0; } })]); } });
    actifs.forEach(r=>{ let et=null; try{ et=r.ctl.etat&&r.ctl.etat(); }catch(_){ } if(r.prem==null && et && (et.t>0 || (et.actives&&et.actives.length))){ r.prem=n;
      const x=__S.tou[__S.tou.length-1]; if(x && x.prem==null && n>x.t){ x.prem=n; x.tx=r.tx; x.imgs=x.n; x.m2=cpt(); } }
      const cv=r.ctl.canevas;
      if(cv && cv.isConnected && r.prem!=null){ const a=cv.getBoundingClientRect(), b=r.el.getBoundingClientRect(), d=a.top-b.top; if(r.d0==null) r.d0=d; __S.im.push(Math.abs(d-r.d0)); } });
    actifs=actifs.filter(r=>!r.ctl.fini); requestAnimationFrame(f); })();
})();"""
def jusquau_titre(pg):
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1600)
    B.attend_parole(pg); B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(500)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(4500)
    z = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {l:(r.left-D.left)/k+0, t:(r.top-D.top)/k, k:1, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee'), L:r.left, T:r.top, K:k}; }")
    if not z or not z['dep'] or not z['arr']: return False
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0], z['t'] + a[1], z['l'] + (e[0] + 6), z['t'] + e[1]
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
    pg.wait_for_function("()=>{ const f=document.getElementById('onbFin'); return !!f; }", timeout=30000); pg.wait_for_timeout(5600)
    return bool(pg.evaluate("()=>!!document.getElementById('onbFin')"))
with sync_playwright() as p:
    b = p.webkit.launch(); print('fichier :', F, '· charge %.1f' % B.charge())
    for vw, vh, nom in ((390, 844, '1'), (330, 714, '0,79')):
        ctx = B.contexte(b, onb=False, guide=False, vw=vw, vh=vh); pg = B.ouvre(ctx, F, attente=7000); pg.evaluate(SONDE)
        if not jusquau_titre(pg): juge('[%s] le parcours va jusqu\'à « Promi planté ! »' % nom, False); ctx.close(); continue
        for i in range(3):
            for _ in range(60):
                if not pg.evaluate("()=>{ const f=_onbFinPas(); return f&&f.enCours; }"): break
                pg.wait_for_timeout(200)
            pg.wait_for_timeout(1400 if B.charge() < 8 else 3000)                       # le texte d'après se prépare après la fin du pas : un lecteur met plus longtemps
            B.tap(pg, 195, 300); pg.wait_for_timeout(1500)
            r = pg.evaluate("(i)=>{ const x=__S.tou[__S.tou.length-1]; return x?{ms:x.prem?x.prem-x.t:null, imgs:x.imgs, tx:x.tx, m:x.m, m2:x.m2, n:__S.tou.length, j:(x.j||[]).slice(0,5), fp:_onbFinPas()}:null; }", i)
            c = B.charge(); T = '[%s · toucher %d]' % (nom, i + 1)
            print('  ', T, {k: r[k] for k in ('ms', 'imgs', 'j')} if r else r, 'charge %.1f' % c, flush=True)
            juge(T + ' A · de l\'encre à l\'image qui suit le toucher (la sonde la lit une image après : ≤ 2)', r and r['imgs'] is not None and r['imgs'] <= 2, r and ('%s images · %s ms · %s' % (r['imgs'], r['ms'] and round(r['ms']), r['tx'])))
            if r and r['m'] and r['m2']:
                d = {k: r['m2'].get(k, 0) - r['m'].get(k, 0) for k in r['m2'] if isinstance(r['m2'].get(k), (int, float)) and k not in ('cache', 'cacheR')}
                juge(T + ' B · rien ne se calcule après le toucher (tout vient du cache)', not any(v > 0 for k, v in d.items() if k in ('prep', 'restes')), d)
            if c < 4: juge(T + ' C · ≤ 34 ms du toucher à la première image du tracé', r and r['ms'] is not None and r['ms'] <= 34, r and r['ms'])
            else: print('   %s C · NON JUGÉ (charge %.1f)' % (T, c), flush=True)
        ec = pg.evaluate("()=>{ const a=__S.im; return a.length?[a.length, Math.max(...a)]:[0,0]; }")
        juge('[%s] D · l\'encre reste sur sa ligne pendant que le bloc se place' % nom, ec[1] <= 2, ec)
        juge('[%s] aucune erreur de page' % nom, not [x for x in pg.erreurs if 'version.json' not in x], pg.erreurs[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
