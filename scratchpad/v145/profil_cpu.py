"""profil CPU (Chromium, CDP) d'une plantation sur Toile remplie : temps propre par fonction. usage : profil_cpu.py monde n"""
import sys, json, io, collections; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
m, n = sys.argv[1], int(sys.argv[2])
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = B.contexte(b, sombre=('sombre' in sys.argv)); B.toile_pleine(ctx, n); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }", m); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{document.getElementById('fTitle').value='tenir bon';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(3200)
    cdp = ctx.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 200}); cdp.send('Profiler.start')
    pg.evaluate("()=>{ document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(2600)
    prof = cdp.send('Profiler.stop')['profile']; b.close()
nodes = {x['id']: x for x in prof['nodes']}; dt = prof['timeDeltas']; self_t = collections.Counter()
for s, d in zip(prof['samples'], dt):
    cf = nodes[s]['callFrame']; self_t[(cf['functionName'] or '(anonyme)', cf['url'].split('/')[-1][:18], cf['lineNumber'] + 1)] += d / 1000.0
tot = sum(self_t.values()); print('total échantillonné : %.0f ms sur 2,6 s' % tot)
for k, v in self_t.most_common(22): print('  %6.0f ms  %-26s %s:%d' % (v, k[0][:26], k[1], k[2]))
