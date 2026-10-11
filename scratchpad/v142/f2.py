# C-102 : qu'est-ce qui tourne juste après « tenir » ? — sans profileur : on journalise closeAll / openDetail / l'état de _tenirAnime et les longues tâches
import sys, json
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 20))
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("""()=>{ window.__j=[]; window.__lt=[]; const J=(n,x)=>window.__j.push([Math.round(performance.now()-(window.__t0||0)), n, x||'']);
      ['closeAll','openDetail','renderDetail','syncAll','saveState'].forEach(n=>{ const f=window[n]; if(typeof f!=='function') return; window[n]=function(){ J(n, (new Error().stack||'').split('\\n').slice(2,5).map(s=>s.trim().slice(0,60)).join(' < ')); return f.apply(this,arguments); }; });
      let v=window._tenirAnime; Object.defineProperty(window,'_tenirAnime',{get(){return v}, set(x){ if(x!==v) J('_tenirAnime='+x, (new Error().stack||'').split('\\n').slice(2,4).map(s=>s.trim().slice(0,70)).join(' < ')); v=x; }, configurable:true});
      let w=window._instant; Object.defineProperty(window,'_instant',{get(){return w}, set(x){ if(x!==w) J('_instant='+x); w=x; }, configurable:true});
      try{ new PerformanceObserver(l=>{ l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime),Math.round(e.duration)])); }).observe({entryTypes:['longtask']}); }catch(e){} }""")
    pire = []
    for k in range(N):
        pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d %% Math.min(3,L.length)]; p.status='rate'; return p.id; }" % k)
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
        r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}"); y = r['y'] + r['h'] / 2
        pg.evaluate("()=>{ document.getElementById('tenirCv').addEventListener('pointerup', ()=>{ window.__t0=performance.now(); window.__j.length=0; window.__lt.length=0; }, {capture:true, once:true}); }")
        pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
        for i in range(1, 26): pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
        pg.wait_for_timeout(60); pg.mouse.up(); pg.wait_for_timeout(3600)
        d = pg.evaluate("()=>({j:window.__j.slice(), lt:window.__lt.map(e=>[e[0]-Math.round(window.__t0),e[1]])})")
        lt = [e for e in d['lt'] if e[0] > -30]; m = max([e[1] for e in lt] or [0]); pire.append(m)
        print('passe %2d · tâches > 50 ms : %s' % (k + 1, lt))
        if m > 120:
            for e in d['j']: print('      ', e)
    print('pires :', pire)
    b.close()
