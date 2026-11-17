"""v207 §2 — le coût d'une carte de lettre : les vraies demandes à l'ouvrier (onboarding : prénom, puis la page de la parole), rejouées sur le fil, chronométrées."""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
PIEGE = r"""(()=>{ window.__DEM=[]; const W0=window.Worker; window.Worker=function(u,o){ const w=new W0(u,o); const pm=w.postMessage.bind(w);
  w.postMessage=function(m,t){ try{ if(m && m.A && m.kind!=='essai') window.__DEM.push({t:performance.now(), w:m.w, h:m.h, n:m.traits.length, m:JSON.parse(JSON.stringify({A:Array.from(m.A), w:m.w, h:m.h, traits:m.traits, moves:m.moves}))}); }catch(e){} return pm(m,t); }; return w; }; })();"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV); ctx.add_init_script(PIEGE)
    pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(9000)
    r = pg.evaluate("""()=>{ const D=window.__DEM, T=window.TraceLettres, out=[];
      for(const d of D){ const A=new Uint8ClampedArray(d.m.A); const t0=performance.now(); for(let k=0;k<3;k++) T._carte(A,d.m.w,d.m.h,JSON.parse(JSON.stringify(d.m.traits)),d.m.moves); out.push([(performance.now()-t0)/3, d.w*d.h, d.n]); }
      return {n:D.length, ms:out, dt:D.length?D[D.length-1].t-D[0].t:0}; }""")
    b.close()
ms = sorted(x[0] for x in r['ms']); px = sorted(x[1] for x in r['ms'])
q = lambda L, f: L[min(len(L) - 1, int(f * len(L)))] if L else None
print('demandes', r['n'], 'sur %.0f ms' % r['dt'], '· carte (WebKit, fil) p50 %.1f ms p95 %.1f max %.1f · somme %.0f ms' % (q(ms, .5), q(ms, .95), ms[-1], sum(ms)), '· pixels (×sup²) p50', q(px, .5), 'max', px[-1])
