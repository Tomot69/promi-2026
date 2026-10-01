import collections, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':200})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{window.__LT=[]; new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__LT.push([Math.round(e.startTime-(window.__t0||0)),Math.round(e.duration)]);}).observe({type:'longtask'});}")
    cdp.send('Profiler.start'); T0=pg.evaluate("()=>{window.__t0=performance.now(); return performance.timeOrigin+window.__t0;}"); pg.evaluate("()=>{ var k=null; for(var q in NUE){k=q;break;} closeAll(); openNueeDetail(k);}"); pg.wait_for_timeout(2500)
    prof=cdp.send('Profiler.stop')['profile']
    print('tâches longues (début, durée) :', pg.evaluate("()=>window.__LT"))
    nodes={n['id']:n for n in prof['nodes']}; par={}
    for n in prof['nodes']:
        for c in n.get('children',[]): par[c]=n['id']
    T=prof['startTime']; E=[]
    for sid,d in zip(prof['samples'],prof['timeDeltas']): T+=d; E.append((T,sid))
    # plus longue suite d'échantillons non inactifs
    best=(0,0,0); i=0
    while i<len(E):
        if nodes[E[i][1]]['callFrame']['functionName']=='(idle)': i+=1; continue
        j=i
        while j+1<len(E) and nodes[E[j+1][1]]['callFrame']['functionName']!='(idle)': j+=1
        if E[j][0]-E[i][0]>best[0]: best=(E[j][0]-E[i][0],i,j)
        i=j+1
    LT=pg.evaluate("()=>window.__LT"); a,dd=sorted(LT,key=lambda x:-x[1])[0]
    # repère du profil : premier échantillon = début du profil ; on aligne sur la 1re tâche longue (début 0)
    base=E[0][0]
    for k in range(len(E)):
        if nodes[E[k][1]]['callFrame']['functionName']!='(idle)': base=E[k][0]; break
    i=next(k for k in range(len(E)) if (E[k][0]-base)/1000>=a); j=max(k for k in range(len(E)) if (E[k][0]-base)/1000<=a+dd)
    dur=(E[j][0]-E[i][0]); print('la plus longue tâche longue : début %d, %d ms' % (a,dd))
    tot=collections.Counter()
    for k in range(i,j+1):
        cur=E[k][1]; seen=set()
        while cur in nodes:
            cf=nodes[cur]['callFrame']; kk=(cf['functionName'] or '(anon)')+' l.'+str(cf['lineNumber']+1)
            if kk not in seen and 'app.html' in cf['url']: tot[kk]+=1; seen.add(kk)
            cur=par.get(cur)
    n=j-i+1; print([(k,round(v*dur/1000/n)) for k,v in tot.most_common(22)])
    b.close()
