# banc de l'animation « tenir une parole » : on trace le geste sur une fiche à tenir, et on relève chaque image (intervalle entre deux
# requestAnimationFrame, longues tâches), 4 s à partir du lever. Chromium GPU @3x (+ profil CPU) ou WebKit.
import sys, json, statistics
from playwright.sync_api import sync_playwright
MOTEUR = sys.argv[1] if len(sys.argv) > 1 else 'chromium'; URL = sys.argv[2] if len(sys.argv) > 2 else 'app.html'; N = int(sys.argv[3]) if len(sys.argv) > 3 else 3
PROFIL = '--profil' in sys.argv
SONDE = r"""()=>{ window.__im=[]; window.__lt=[]; let av=performance.now(); window.__go=true;
  (function f(t){ const n=performance.now(); window.__im.push([n, n-av]); av=n; if(window.__go) requestAnimationFrame(f); })();
  try{ new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([e.startTime,e.duration]))).observe({entryTypes:['longtask']}); }catch(e){} }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist']) if MOTEUR == 'chromium' else p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/' + URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    cdp = ctx.new_cdp_session(pg) if (MOTEUR == 'chromium' and PROFIL) else None
    tout = []
    for k in range(N):
        pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const p=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee)[0]; p.status='rate'; return p.id; }")
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1200)
        r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const b=e.getBoundingClientRect(); return {x:b.left,y:b.top,w:b.width,h:b.height}}")
        y = r['y'] + r['h'] / 2
        pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
        for i in range(1, 26):
            pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
        if cdp: cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 500}); cdp.send('Profiler.start')
        pg.evaluate(SONDE); t0 = pg.evaluate("()=>performance.now()")
        pg.mouse.up()
        if '--court' in sys.argv and cdp:
            pg.wait_for_timeout(170); prof = cdp.send('Profiler.stop')['profile']; nodes = {n['id']: n for n in prof['nodes']}; dts = prof.get('timeDeltas', []); par = {}
            for n in prof['nodes']:
                for c in n.get('children', []): par[c] = n['id']
            incl = {}
            for sid, dt in zip(prof.get('samples', []), dts):
                vus = set(); x = sid
                while x is not None:
                    cf = nodes[x]['callFrame']; key = '%s:%s' % (cf['functionName'] or '(anonyme)', cf['lineNumber'] + 1)
                    if key not in vus: vus.add(key); incl[key] = incl.get(key, 0) + dt / 1000.0
                    x = par.get(x)
            qs = {}
            for sid, dt in zip(prof.get('samples', []), dts):
                cf = nodes[sid]['callFrame']
                if cf['functionName'] in ('querySelectorAll', 'getBoundingClientRect', 'getClientRects', 'setProperty', 'getComputedStyle', 'elementFromPoint'):
                    x = par.get(sid); ch = []
                    while x is not None and len(ch) < 4:
                        c2 = nodes[x]['callFrame']; ch.append('%s:%s' % (c2['functionName'] or '(anonyme)', c2['lineNumber'] + 1)); x = par.get(x)
                    k2 = cf['functionName'] + ' ← ' + ' ← '.join(ch); qs[k2] = qs.get(k2, 0) + dt / 1000.0
            print('   APPELS DOM :', ' | '.join('%s %.1f' % a for a in sorted(qs.items(), key=lambda a: -a[1])[:8]))
            print('   LES 170 PREMIÈRES ms, CUMULÉ :', ' · '.join('%s %.0f' % a for a in sorted(incl.items(), key=lambda a: -a[1])[:60] if not a[0].startswith('(idle')))
            cdp = None
        pg.wait_for_timeout(4000)
        d = pg.evaluate("()=>{ window.__go=false; return {im:window.__im, lt:window.__lt, st:(typeof cur!=='undefined'&&cur)?cur.status:null, inst:window._instant}; }")
        if cdp:
            prof = cdp.send('Profiler.stop')['profile']; nodes = {n['id']: n for n in prof['nodes']}; self_t = {}
            dts = prof.get('timeDeltas', []); 
            for sid, dt in zip(prof.get('samples', []), dts):
                n = nodes[sid]; cf = n['callFrame']; key = '%s:%s' % (cf['functionName'] or '(anonyme)', cf['lineNumber'] + 1); self_t[key] = self_t.get(key, 0) + dt / 1000.0
            par = {}
            for n in prof['nodes']:
                for c in n.get('children', []): par[c] = n['id']
            incl = {}
            for sid, dt in zip(prof.get('samples', []), dts):
                vus = set(); x = sid
                while x is not None:
                    cf = nodes[x]['callFrame']; key = '%s:%s' % (cf['functionName'] or '(anonyme)', cf['lineNumber'] + 1)
                    if key not in vus: vus.add(key); incl[key] = incl.get(key, 0) + dt / 1000.0
                    x = par.get(x)
            print('   CUMULÉ (ms) :', ' · '.join('%s %.0f' % a for a in sorted(incl.items(), key=lambda a: -a[1])[:40] if not a[0].startswith('(')))
            top = sorted(self_t.items(), key=lambda a: -a[1])[:14]
            print('   profil (ms propres) :', ' · '.join('%s %.0f' % a for a in top))
        im = [(t - t0, dt) for t, dt in d['im'][1:]]
        longs = [(round(t), round(dt, 1)) for t, dt in im if dt > 16.7 + 1.5]
        dts = sorted(dt for _, dt in im)
        print('passe %d · état %s · instant %s · %d images · p50 %.1f · p95 %.1f · max %.1f · > 20 ms : %d · longues tâches : %s' % (k + 1, d['st'], d['inst'], len(im), dts[len(dts) // 2], dts[int(len(dts) * .95)], dts[-1], sum(1 for x in dts if x > 20), [(round(a - t0), round(c)) for a, c in d['lt']][:12]))
        print('   images > 18 ms (instant ms, durée) :', longs[:40])
        tout.append(im)
    print('erreurs', er)
    b.close()
