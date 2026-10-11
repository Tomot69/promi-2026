# qui fait la longue tâche après « tenir » ? — profil d'échantillonnage (CDP Profiler), mêmes gestes que redteam_fluide
import sys, json, io
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 12))
SRC = io.open(F if F.startswith('zz-') or F=='app.html' else F, encoding='utf-8').read().split('\n')
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    cdp = ctx.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 500})
    pg.evaluate("""()=>{ window.__lt=[]; try{ new PerformanceObserver(l=>{ l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime),Math.round(e.duration)])); }).observe({entryTypes:['longtask']}); }catch(e){} }""")
    for k in range(N):
        pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d %% Math.min(3,L.length)]; p.status='rate'; return p.id; }" % k)
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
        r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}"); y = r['y'] + r['h'] / 2
        pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
        for i in range(1, 26): pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
        pg.evaluate("()=>{window.__lt.length=0; window.__t0=performance.now()}"); cdp.send('Profiler.start'); pg.wait_for_timeout(60)
        pg.mouse.up(); pg.wait_for_timeout(3600)
        prof = cdp.send('Profiler.stop')['profile']; lt = pg.evaluate("()=>window.__lt.map(e=>[e[0]-Math.round(window.__t0),e[1]])")
        longues = [e for e in lt if e[1] > 120]
        print('passe %d : tâches longues %s' % (k + 1, lt))
        if not longues: continue
        nodes = {n['id']: n for n in prof['nodes']}; par = {}
        for n in prof['nodes']:
            for c in n.get('children', []): par[c] = n['id']
        t = prof['startTime']; cnt = {}
        for s, dt in zip(prof['samples'], prof['timeDeltas']):
            t += dt; n = nodes[s]; cf = n['callFrame']
            if cf['functionName'] in ('(idle)', '(program)', '(garbage collector)') and cf['functionName'] != '(garbage collector)': continue
            # la pile, du plus profond au plus haut
            pile = []; q = s
            while q in nodes and len(pile) < 9:
                c = nodes[q]['callFrame']; 
                if c['functionName'] not in ('(root)',): pile.append('%s@%d' % (c['functionName'] or '(anonyme)', c['lineNumber'] + 1))
                q = par.get(q)
            cle = ' < '.join(pile[:7]); cnt[cle] = cnt.get(cle, 0) + dt
        for cle, v in sorted(cnt.items(), key=lambda x: -x[1])[:10]: print('   %6.1f ms  %s' % (v / 1000.0, cle[:420]))
    b.close()
