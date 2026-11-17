"""v207 §2 — le profil de `carte` : les demandes réelles capturées (WebKit), rejouées dans Chromium sous le profileur (temps propre par ligne du module)."""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
PIEGE = r"""(()=>{ window.__DEM=[]; const W0=window.Worker; window.Worker=function(u,o){ const w=new W0(u,o); const pm=w.postMessage.bind(w);
  w.postMessage=function(m,t){ try{ if(m && m.A && m.kind!=='essai') window.__DEM.push({A:Array.from(m.A), w:m.w, h:m.h, traits:m.traits, moves:m.moves}); }catch(e){} return pm(m,t); }; return w; }; })();"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV); ctx.add_init_script(PIEGE)
    pg = B.ouvre(ctx, sys.argv[1] if len(sys.argv) > 1 else 'app.html', attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(9000)
    D = pg.evaluate("()=>JSON.stringify(window.__DEM.filter(d=>d.traits))"); b.close()
    open('scratchpad/v206/demandes.json', 'w').write(D)
    c = p.chromium.launch(); pg = c.new_page(); pg.goto('http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js')
    pg.add_script_tag(url='http://127.0.0.1:8752/variantes/trace-lettres.js'); pg.wait_for_timeout(500)
    cdp = pg.context.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 100}); cdp.send('Profiler.start')
    t = pg.evaluate("(D)=>{ D=JSON.parse(D); const t0=performance.now(); for(let k=0;k<3;k++) for(const d of D) if(d.traits) TraceLettres._carte(new Uint8ClampedArray(d.A), d.w, d.h, JSON.parse(JSON.stringify(d.traits)), d.moves); return (performance.now()-t0)/3; }", D)
    prof = cdp.send('Profiler.stop')['profile']; c.close()
lignes = {}
for n in prof['nodes']:
    cf = n['callFrame']
    if 'trace-lettres' not in cf['url']: continue
    for pt in n.get('positionTicks', []): lignes[pt['line']] = lignes.get(pt['line'], 0) + pt['ticks']
tot = sum(lignes.values()) or 1
print('carte : %.0f ms pour %d demandes (Chromium)' % (t, len(json.loads(D))))
src = open('variantes/trace-lettres.js', encoding='utf-8').read().split('\n')
for l, k in sorted(lignes.items(), key=lambda x: -x[1])[:14]: print('%5.1f %%  l.%d  %s' % (100 * k / tot, l, src[l - 1].strip()[:110]))
