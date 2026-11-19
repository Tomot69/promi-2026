"""v207 §2 — combien de cartes demandées à l'ouvrier sont des DOUBLONS (même entrée exacte), et quand le cache est vidé, sur un parcours réel :
onboarding (prénom, parole, effacer, retaper), puis l'accueil et le guide."""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
PIEGE = r"""(()=>{ window.__DEM=[]; const W0=window.Worker; window.Worker=function(u,o){ const w=new W0(u,o); const pm=w.postMessage.bind(w);
  w.postMessage=function(m,t){ try{ if(m && m.A && m.kind!=='essai'){ let h=m.w*31+m.h; const A=m.A; for(let i=0;i<A.length;i+=3) h=(h*33+A[i])|0; h=h+'|'+JSON.stringify(m.traits).length; window.__DEM.push({t:Math.round(performance.now()), h:h, px:m.w*m.h}); } }catch(e){} return pm(m,t); }; return w; };
  (function f(){ const T=window.TraceLettres; if(!T){ setTimeout(f,50); return; } window.__RAZ=[]; let n=0; setInterval(()=>{ if(T._cacheN<n) window.__RAZ.push(Math.round(performance.now())); n=T._cacheN; }, 20); })(); })();"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV); ctx.add_init_script(PIEGE)
    pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(6000); B.attend_parole(pg)
    B.tap_sel(pg, '#onbPh [data-onb="parole"]'); pg.wait_for_timeout(800); pg.keyboard.type('lire', delay=60)
    for _ in range(4): pg.keyboard.press('Backspace'); pg.wait_for_timeout(60)
    pg.wait_for_timeout(3000); pg.keyboard.type('lire un livre', delay=50); pg.wait_for_timeout(4000)
    r = pg.evaluate("()=>({D:window.__DEM, raz:window.__RAZ, n:window.TraceLettres._cacheN, cache:Object.keys(window.TraceLettres._cache).length, etat:window.TraceLettres.ouvrierEtat})")
    b.close()
D = r['D']; vu = {}; dbl = 0; pxd = 0
for d in D:
    if d['h'] in vu: dbl += 1; pxd += d['px']
    vu[d['h']] = 1
print('demandes', len(D), '· distinctes', len(vu), '· doublons', dbl, '(%.0f %%)' % (100 * dbl / max(1, len(D))), '· remises à zéro du cache', len(r['raz']), '· cache', r['cache'], '·', r['etat'])
