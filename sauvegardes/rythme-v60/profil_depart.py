# Profil du vrai départ (fiche → Supprimer → Oui) : ce qui tourne sur le fil pendant les 700 ms qui suivent le « Oui ».
import collections, sys
from playwright.sync_api import sync_playwright
M=sys.argv[1] if len(sys.argv)>1 else 'gravure'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':200})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme(m);}",M); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ openDetail(97001); }"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{ window._v16SupprimerPromi(cur); }"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ window.__L=[]; new PerformanceObserver(l=>{ for(const e of l.getEntries()) window.__L.push([Math.round(e.startTime-window.__t0),Math.round(e.duration)]); }).observe({type:'longtask'}); window.__t0=performance.now(); }")
    xy=pg.evaluate("()=>{ const r=document.querySelector('#v16Conf .v16-oui').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]; }")
    cdp.send('Profiler.start'); pg.evaluate("()=>{window.__t0=performance.now();}"); pg.mouse.click(*xy); pg.wait_for_timeout(900)
    prof=cdp.send('Profiler.stop')['profile']
    print('tâches longues (début, durée) :', pg.evaluate("()=>window.__L"))
    nodes={n['id']:n for n in prof['nodes']}; parent={}
    for n in prof['nodes']:
        for c in n.get('children',[]): parent[c]=n['id']
    tot=collections.Counter(); self=collections.Counter()
    T=prof['startTime']; ech=[]
    for sid,d in zip(prof['samples'],prof['timeDeltas']):
        T+=d; ech.append((T,sid,d))
    t0=ech[0][0]
    # la tâche du clic : échantillons non inactifs consécutifs au début
    ech=[e for e in ech if nodes[e[1]]['callFrame']['functionName']!='(idle)']
    lim=float(sys.argv[2]) if len(sys.argv)>2 else 1e9
    for T,sid,d in ech:
        if (T-t0)/1000>lim: continue
        n=nodes[sid]['callFrame']; self[(n['functionName'] or '(anon)')+' l.'+str(n['lineNumber']+1)]+=d/1000
        seen=set(); cur=sid
        while cur in nodes:
            cf=nodes[cur]['callFrame']; kk=(cf['functionName'] or '(anon)')+' l.'+str(cf['lineNumber']+1)
            if kk not in seen and 'app.html' in cf['url']: tot[kk]+=d/1000; seen.add(kk)
            cur=parent.get(cur)
    print('propre', [(k,round(v)) for k,v in self.most_common(10)])
    print('total ', [(k,round(v)) for k,v in tot.most_common(22)])
    b.close()
