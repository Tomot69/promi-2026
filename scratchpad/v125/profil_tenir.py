import sys, json, collections
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    cdp = ctx.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 200})
    pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[0]; p.status='rate'; return p.id; }")
    pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
    r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}")
    y = r['y'] + r['h'] / 2
    pg.evaluate("()=>{ const fa=window._tenirApres; window._tenirApres=function(){ window.__ta=performance.now(); const r=fa.apply(this,arguments); window.__tb=performance.now(); return r; }; }")
    pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
    for i in range(1, 26):
        pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
    pg.wait_for_timeout(60); pg.mouse.up(); pg.wait_for_timeout(1300)
    cdp.send('Profiler.start'); pg.wait_for_timeout(1500); prof = cdp.send('Profiler.stop')['profile']
    print(pg.evaluate("()=>[window.__ta, window.__tb, window.__tb-window.__ta]"))
    nodes = {n['id']: n for n in prof['nodes']}; par = {}
    for n in prof['nodes']:
        for c in n.get('children', []): par[c] = n['id']
    self_ = collections.Counter(); incl = collections.Counter()
    dts = prof['timeDeltas']
    for s, dt in zip(prof['samples'], dts):
        n = nodes[s]; cf = n['callFrame']; self_[(cf['functionName'] or '(anonyme)', cf['lineNumber'])] += dt
        vus = set(); x = s
        while x in nodes:
            cf = nodes[x]['callFrame']; k = (cf['functionName'] or '(anonyme)', cf['lineNumber'])
            if k not in vus: incl[k] += dt; vus.add(k)
            x = par.get(x)
            if x is None: break
    print('— temps propre'); 
    for k, v in self_.most_common(14): print('  %6.1f ms  %s l.%s' % (v/1000, k[0], k[1]))
    print('— temps inclus')
    for k, v in incl.most_common(26): print('  %6.1f ms  %s l.%s' % (v/1000, k[0], k[1]))
    b.close()
