import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 14
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} window.__lt=[]; new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime), Math.round(e.duration)]))).observe({entryTypes:['longtask']}); }")
    cdp=ctx.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':1000})
    for k in range(N):
        pid=pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d %% Math.min(3,L.length)]; p.status='rate'; return p.id; }"%k)
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}",pid); pg.wait_for_timeout(1500); pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
        r=pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}"); y=r['y']+r['h']/2
        pg.evaluate("()=>{window.__lt=[]; window.__t0=performance.now();}"); cdp.send('Profiler.start')
        pg.mouse.move(r['x']+12,y); pg.mouse.down()
        for i in range(1,21): pg.mouse.move(r['x']+12+(r['w']-24)*i/20,y); pg.wait_for_timeout(12)
        pg.mouse.up(); pg.wait_for_timeout(3600)
        prof=cdp.send('Profiler.stop')['profile']
        lt=[x for x in pg.evaluate("()=>window.__lt.map(e=>[e[0]-Math.round(window.__t0),e[1]])") if x[1]>=100]
        if lt:
            print('passe',k,'tâches ≥ 100 ms :',lt)
            nodes={n['id']:n for n in prof['nodes']}; par={}
            for n in prof['nodes']:
                for c in n.get('children',[]): par[c]=n['id']
            self={}
            for s,dt in zip(prof['samples'],prof.get('timeDeltas',[])):
                n=nodes[s]; cf=n['callFrame']; key=(cf['functionName'] or '(anonyme)', cf['lineNumber']); self[key]=self.get(key,0)+dt/1000.0
                # et l'ancêtre nommé le plus haut dans app.html
            for kx,v in sorted(self.items(), key=lambda q:-q[1])[:7]:
                if kx[0] not in ('(idle)','(program)'): print('   %7.1f ms  %s  l.%s'%(v,kx[0],kx[1]))
    print('fini',F); b.close()
