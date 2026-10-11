import sys, json
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    cdp=ctx.new_cdp_session(pg)
    for k in range(2):
        pid=pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d]; p.status='rate'; return p.id; }"%k)
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}",pid); pg.wait_for_timeout(1500); pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
        r=pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}"); y=r['y']+r['h']/2
        pg.evaluate("()=>{ window.__lt=[]; try{ new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime-window.__t0), Math.round(e.duration)]))).observe({entryTypes:['longtask']}); }catch(e){} window.__t0=performance.now(); }")
        pg.mouse.move(r['x']+12,y); pg.mouse.down()
        for i in range(1,21): pg.mouse.move(r['x']+12+(r['w']-24)*i/20,y); pg.wait_for_timeout(12)
        pg.evaluate("()=>{window.__t0=performance.now(); window.__lt=[];}"); pg.mouse.up()
        pg.wait_for_timeout(1600)
        cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':500}); cdp.send('Profiler.start')
        pg.wait_for_timeout(2100)
        prof=cdp.send('Profiler.stop')['profile']
        print('passe',k,'tâches longues (ms après le lever, durée) :',pg.evaluate("()=>window.__lt"))
        nodes={n['id']:n for n in prof['nodes']}; dts=prof.get('timeDeltas',[]); self={}
        for s,dt in zip(prof['samples'],dts):
            n=nodes[s]; cf=n['callFrame']; key=(cf['functionName'] or '(anonyme)', cf['lineNumber'], cf['url'][-22:]); self[key]=self.get(key,0)+dt/1000.0
        for kx,v in sorted(self.items(), key=lambda q:-q[1])[:9]: print('   %7.1f ms  %s  l.%s  %s'%(v,kx[0],kx[1],kx[2]))
    b.close()
