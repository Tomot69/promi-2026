import collections
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':500})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(1500)
    cdp.send('Profiler.start'); pg.evaluate("()=>{var k=null; for(var q in NUE){k=q;break;} closeAll(); openNueeDetail(k);}"); pg.wait_for_timeout(3500)
    prof=cdp.send('Profiler.stop')['profile']
    nodes={n['id']:n for n in prof['nodes']}; par={}
    for n in prof['nodes']:
        for c in n.get('children',[]): par[c]=n['id']
    tot=collections.Counter(); own=collections.Counter()
    for sid,d in zip(prof['samples'],prof['timeDeltas']):
        cf=nodes[sid]['callFrame']; own[(cf['functionName'] or '(anon)')+' l.'+str(cf['lineNumber']+1)]+=d/1000
        seen=set(); cur=sid
        while cur in nodes:
            cf=nodes[cur]['callFrame']; kk=(cf['functionName'] or '(anon)')+' l.'+str(cf['lineNumber']+1)
            if kk not in seen and 'app.html' in cf['url']: tot[kk]+=d/1000; seen.add(kk)
            cur=par.get(cur)
    print('propre', [(k,round(v)) for k,v in own.most_common(8)])
    print('total ', [(k,round(v)) for k,v in tot.most_common(20)])
    b.close()
