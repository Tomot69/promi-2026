# Attribue CHAQUE tâche longue (PerformanceObserver) à ses fonctions : l'horloge du profileur
# (µs, monotone) est recalée sur performance.now() de la page au démarrage du profil.
import os, json, collections
from playwright.sync_api import sync_playwright
LANCE = r"""async ([x0,y0,dx,n,pas])=>{ const t=document.querySelector('#auraScreen .au-prise');
  const o=(x)=>({pointerId:7,pointerType:'mouse',isPrimary:true,clientX:x,clientY:y0,bubbles:true,cancelable:true,buttons:1});
  t.dispatchEvent(new PointerEvent('pointerdown',o(x0)));
  for(let k=1;k<=n;k++){ await new Promise(r=>setTimeout(r,pas)); t.dispatchEvent(new PointerEvent('pointermove',o(x0+dx*k/n))); }
  t.dispatchEvent(new PointerEvent('pointerup',o(x0+dx))); return 1; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(os.environ.get('APP_AURA','http://127.0.0.1:8752/app.html')); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{window.__lt=[];try{new PerformanceObserver(l=>{l.getEntries().forEach(e=>window.__lt.push([e.startTime,e.duration]));}).observe({type:'longtask'});}catch(e){}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(1500)
    pre=os.environ.get('PRE_JS')
    if pre: print('SONDE :', pg.evaluate(pre))
    r=pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect();const d=document.getElementById('device').getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,sc:d.width/390};}")
    cdp=pg.context.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':500})
    cdp.send('Profiler.start'); t_page=pg.evaluate("()=>performance.now()"); pg.evaluate("()=>{window.__lt=[];}")
    for k in range(3):
        for _ in range(120):
            if pg.evaluate("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp;}"): break
            pg.wait_for_timeout(100)
        pg.evaluate(LANCE,[r['cx']-70*r['sc'],r['cy'],132*r['sc'],6,16]); pg.wait_for_timeout(6000)
    prof=cdp.send('Profiler.stop')['profile']; lt=pg.evaluate("()=>window.__lt")
    extra=pg.evaluate("()=>({bloques:window.__bloques?__bloques():null})")
    b.close()
nodes={n['id']:n for n in prof['nodes']}; par={}
for n in prof['nodes']:
    for c in n.get('children',[]): par[c]=n['id']
def nom(i):
    cf=nodes[i]['callFrame']; return '%s:%d' % (cf['functionName'] or '(anonyme)', cf['lineNumber']+1)
ts=[]; t=prof['startTime']
for sid,dt in zip(prof['samples'],prof['timeDeltas']):
    t+=dt; ts.append((t,sid,dt/1000.0))
off=prof['startTime']/1000.0 - t_page      # horloge profil (ms) - horloge page (ms), au démarrage
tot=collections.Counter()
for (tt,sid,dt) in ts: tot[nom(sid)]+=dt
T=sum(tot.values())
print('sonde :', extra)
print('frame (8917) : %.1f %% du temps échantillonné · peint : %.1f %% · verse : %.1f %%' % (
    100*sum(v for k,v in tot.items() if k.startswith('frame:8917'))/T,
    100*sum(v for k,v in tot.items() if k.startswith('peint:'))/T, 100*sum(v for k,v in tot.items() if k.startswith('verse:'))/T))
print('\n%d tâches longues > 50 ms' % len(lt))
for (st,du) in lt:
    if du<120: continue
    a=(st+off)*1000; z=(st+du+off)*1000
    inc=collections.Counter(); sel=collections.Counter()
    for (tt,sid,dt) in ts:
        if tt<a or tt>z: continue
        sel[nom(sid)]+=dt; seen=set(); i=sid
        while True:
            k=nom(i)
            if k not in seen: inc[k]+=dt; seen.add(k)
            if i not in par: break
            i=par[i]
    print('\n== tâche de %.0f ms à %.0f ms' % (du, st))
    print('   inclusif :', ', '.join('%s %.0f' % (k,v) for k,v in inc.most_common(10) if not k.startswith('(root)')))
    print('   propre   :', ', '.join('%s %.0f' % (k,v) for k,v in sel.most_common(6)))
