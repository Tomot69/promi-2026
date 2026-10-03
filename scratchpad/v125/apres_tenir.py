# §7 — les tâches longues APRÈS l'animation « tenir » (de 1,7 s à 3,5 s après le lever) : durée, instant, et la fonction JS qui pèse le plus
import sys, json
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for k in range(3):
        pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d %% Math.min(3,L.length)]; p.status='rate'; return p.id; }" % k)
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
        r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}")
        y = r['y'] + r['h'] / 2
        pg.evaluate("()=>{ window.addEventListener('mouseup', ()=>{ performance.mark('lever'); }, {capture:true, once:true}); }")
        pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
        for i in range(1, 26):
            pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
        b.start_tracing(page=pg, categories=['toplevel', 'devtools.timeline', 'disabled-by-default-devtools.timeline', 'blink.user_timing', 'v8'])
        pg.wait_for_timeout(60); pg.mouse.up(); pg.wait_for_timeout(3900)
        ev = json.loads(b.stop_tracing().decode('utf-8'))['traceEvents']
        m = [e for e in ev if e.get('name')=='lever' and 'ts' in e][0]; pid_, tid, t0 = m['pid'], m['tid'], m['ts']
        T = sorted(((e['ts']-t0)/1000, e.get('dur',0)/1000, e) for e in ev if e.get('name')=='RunTask' and e.get('ph')=='X' and e.get('pid')==pid_ and e.get('tid')==tid and e.get('dur',0)>12000)
        print('passe', k+1)
        for ts, du, e in T:
            if ts < -50: continue
            # les appels de fonction dans la tâche
            fn = sorted(((x.get('dur',0)/1000, (x.get('args',{}).get('data',{}) or {}).get('functionName','?'), (x.get('args',{}).get('data',{}) or {}).get('lineNumber')) for x in ev if x.get('name') in ('FunctionCall','TimerFire','EvaluateScript','FireAnimationFrame','Layout','UpdateLayoutTree','EventDispatch','Paint','PrePaint') and x.get('pid')==pid_ and x.get('tid')==tid and e['ts']<=x.get('ts',0)<=e['ts']+e['dur'] and x.get('dur',0)>4000), reverse=True)[:4]
            noms = sorted(((x.get('dur',0)/1000, x.get('name')) for x in ev if x.get('pid')==pid_ and x.get('tid')==tid and x.get('ph')=='X' and e['ts']<=x.get('ts',0)<=e['ts']+e['dur'] and x.get('dur',0)>4000 and x.get('name') in ('Layout','UpdateLayoutTree','Paint','PrePaint','Layerize','Commit','ParseHTML','MinorGC','MajorGC','V8.GC_SCAVENGER')), reverse=True)[:3]
            print('   à %5d ms : %5.1f ms   %s   %s' % (ts, du, ' · '.join('%s l.%s %.0f' % (n, l, d_) for d_, n, l in fn), ' · '.join('%s %.0f' % (n, d_) for d_, n in noms)))
    b.close()
