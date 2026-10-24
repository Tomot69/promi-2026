import sys, collections; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
MONDE = sys.argv[1] if len(sys.argv) > 1 else 'guingois'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, 'app.html')
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200)
    for i in range(22):
        if pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')") == MONDE: break
        B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(1400)
    pg.wait_for_timeout(4000)
    x, y = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.getElementById('st3thumb'); const r=e.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }")
    cdp = ctx.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 200}); cdp.send('Profiler.start')
    B.glisse(pg, [[x + 100 * t / 40, y] for t in range(41)] + [[x + 100 - 200 * t / 60, y] for t in range(61)], pas=6); pg.wait_for_timeout(300)
    prof = cdp.send('Profiler.stop')['profile']
    nodes = {n['id']: n for n in prof['nodes']}; dt = collections.Counter()
    deltas = prof['timeDeltas']; samples = prof['samples']
    for s, d in zip(samples, deltas):
        f = nodes[s]['callFrame']; dt['%s:%d %s' % (f['url'].split('/')[-1].split('?')[0], f['lineNumber'] + 1, f['functionName'] or '(anon)')] += d / 1000
    tot = sum(dt.values()); print(MONDE, 'total %.0f ms' % tot)
    for k, v in dt.most_common(18): print('  %6.1f ms  %s' % (v, k))
    b.close()
