"""v207 §2 — la carte nouvelle contre l'ancienne, bit pour bit, sur les demandes réelles capturées (scratchpad/v206/demandes.json) ; et leur temps.
WebKit et Chromium. Un seul écart (une valeur, ou D) : rouge."""
import json, hashlib
from playwright.sync_api import sync_playwright
D = open('scratchpad/v206/demandes.json').read()
JS = """(D)=>{ D=JSON.parse(D).filter(d=>d.traits); const out=[]; let ms=0;
  for(let k=0;k<3;k++){ const t0=performance.now(); for(const d of D){ const r=TraceLettres._carte(new Uint8ClampedArray(d.A), d.w, d.h, JSON.parse(JSON.stringify(d.traits)), d.moves);
      if(k===0){ const u=new Uint8Array(r.T.buffer); let h=0; for(let i=0;i<u.length;i++) h=(h*31+u[i])|0; out.push(h+':'+r.D); } } ms+=performance.now()-t0; }
  return {sig:out, ms:ms/3, n:D.length}; }"""
res = {}
with sync_playwright() as p:
    for nom, nav in (('webkit', p.webkit), ('chromium', p.chromium)):
        b = nav.launch()
        for ver, src in (('avant', 'sauvegardes/trace-lettres-avant-v207.js'), ('apres', 'variantes/trace-lettres.js')):
            pg = b.new_page(); pg.goto('http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js'); pg.add_script_tag(url='http://127.0.0.1:8752/' + src); pg.wait_for_timeout(300)
            res[(nom, ver)] = pg.evaluate(JS, D); pg.close()
        b.close()
for nom in ('webkit', 'chromium'):
    a, b_ = res[(nom, 'avant')], res[(nom, 'apres')]
    diff = sum(1 for x, y in zip(a['sig'], b_['sig']) if x != y)
    print('%-8s %d cartes · identiques %d/%d · %s · temps %.0f → %.0f ms (×%.2f)' % (nom, a['n'], a['n'] - diff, a['n'], '✅' if diff == 0 else '❌', a['ms'], b_['ms'], a['ms'] / max(1, b_['ms'])))
