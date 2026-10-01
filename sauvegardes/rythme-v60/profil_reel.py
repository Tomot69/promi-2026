import collections, sys
from playwright.sync_api import sync_playwright
M=sys.argv[1] if len(sys.argv)>1 else 'encre'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':200})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme(m);}",M); pg.wait_for_timeout(3000)
    pg.mouse.click(*pg.evaluate("()=>{const r=document.getElementById('createBtn').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(600)
    pg.mouse.click(*pg.evaluate("()=>{const r=document.querySelector('#accChoix .acc-pil[data-k=promi]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ const t=document.getElementById('fTitle'); t.value='mesure du rythme'; t.dispatchEvent(new Event('input',{bubbles:true})); }")
    z=pg.evaluate("()=>{ const r=document.getElementById('planterZone').getBoundingClientRect(); return [r.left, r.top+r.height/2, r.width]; }")
    pg.mouse.move(z[0]+12,z[1]); pg.mouse.down()
    for i in range(1,26): pg.mouse.move(z[0]+12+(z[2]-24)*i/25, z[1]); pg.wait_for_timeout(12)
    pg.mouse.up(); pg.wait_for_timeout(650)
    cdp.send('Profiler.start'); pg.wait_for_timeout(1000)
    prof=cdp.send('Profiler.stop')['profile']
    nodes={n['id']:n for n in prof['nodes']}; parent={}
    for n in prof['nodes']:
        for c in n.get('children',[]): parent[c]=n['id']
    tot=collections.Counter(); self=collections.Counter()
    for sid,d in zip(prof['samples'],prof['timeDeltas']):
        n=nodes[sid]['callFrame']; self[(n['functionName'] or '(anon)')+' l.'+str(n['lineNumber']+1)]+=d/1000
        seen=set(); cur=sid
        while cur in nodes:
            cf=nodes[cur]['callFrame']; kk=(cf['functionName'] or '(anon)')+' l.'+str(cf['lineNumber']+1)
            if kk not in seen and 'app.html' in cf['url']: tot[kk]+=d/1000; seen.add(kk)
            cur=parent.get(cur)
    print('propre', [(k,round(v)) for k,v in self.most_common(10)])
    print('total ', [(k,round(v)) for k,v in tot.most_common(18)])
    b.close()
