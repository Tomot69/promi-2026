# v153 C-125 — sonde : que fait le tracé des lettres dans l'onboarding, en WebKit (banc_tom) ?
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
HOOK = """()=>{ window.__TLlog=[]; const T=window.TraceLettres; const tr=T.trace; T.trace=function(c,ct,o){ const ctl=tr.apply(this,arguments); const rec={id:c.id||c.className, t0:performance.now(), o:Object.assign({},o||{}), frames:[]};
  window.__TLlog.push(rec); ctl.pret.then(()=>{ rec.duree=ctl.duree; rec.gl=ctl.glyphes.map(g=>[g.car,g.police,g.variante]); rec.tpret=performance.now()-rec.t0; });
  (function f(){ if(ctl.fini){ rec.tfin=performance.now()-rec.t0; return; } const e=ctl.etat?ctl.etat():null; rec.frames.push([Math.round(performance.now()-rec.t0), e?e.glyphe:-1]); requestAnimationFrame(f); })();
  return ctl; }; return !!T; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, onb=False, guide=True)
    pg = B.ouvre(ctx, attente=500)
    pg.wait_for_function("()=>!!window.TraceLettres", timeout=10000)
    pg.evaluate(HOOK)
    pg.wait_for_timeout(7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(9000)
    L = pg.evaluate("()=>window.__TLlog")
    for r in L:
        fr = r['frames']; gaps = [fr[i+1][0]-fr[i][0] for i in range(len(fr)-1)]
        # glyph changes per frame
        ch = [fr[i+1][1]-fr[i][1] for i in range(len(fr)-1)]
        print(r['id'], 'cps', r['o'].get('cps'), 'durée', round(r.get('duree') or 0), 'pret', round(r.get('tpret') or 0), 'fin', round(r.get('tfin') or 0), 'n', len(r.get('gl') or []))
        print('   polices', sorted(set((g[1], g[2]) for g in (r.get('gl') or []))))
        print('   images', len(fr), 'max écart', max(gaps) if gaps else 0, 'images où la lettre ne change pas', sum(1 for c in ch if c == 0), 'images à +1', sum(1 for c in ch if c == 1), 'à +2 ou plus', sum(1 for c in ch if c >= 2))
    print(pg.evaluate("()=>({ouvrier: !!window.TraceLettres._ouvrier, sup: window.TraceLettres.supMax, prep: window.TraceLettres.mesures.prep.slice(0,40).map(Math.round)})"))
    b.close()
