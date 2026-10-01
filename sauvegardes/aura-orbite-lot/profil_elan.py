# L'IMAGE DE 267 ms PENDANT L'ÉLAN — dont 16 ms seulement pour le peintre de l'Orbite.
# Où part le reste ? On pose le profileur du navigateur (CDP, échantillon toutes les 0,5 ms)
# pendant trois lancers, on relève les tâches longues (PerformanceObserver) et chaque image de
# la boucle, puis on range le temps PROPRE de chaque fonction : nom, fichier, ligne dans app.html.
import os, json, collections
from playwright.sync_api import sync_playwright
LANCE = r"""async ([x0,y0,dx,n,pas,tenir])=>{ const t=document.querySelector('#auraScreen .au-prise');
  const o=(x)=>({pointerId:7,pointerType:'mouse',isPrimary:true,clientX:x,clientY:y0,bubbles:true,cancelable:true,buttons:1});
  t.dispatchEvent(new PointerEvent('pointerdown',o(x0)));
  if(tenir) await new Promise(r=>setTimeout(r,tenir));
  for(let k=1;k<=n;k++){ await new Promise(r=>setTimeout(r,pas)); t.dispatchEvent(new PointerEvent('pointermove',o(x0+dx*k/n))); }
  t.dispatchEvent(new PointerEvent('pointerup',o(x0+dx))); return performance.now(); }"""
ENREG = r"""async (ms)=>{ const out=[]; const t0=performance.now(); let k0=_aura.etat().tick;
  await new Promise(r=>{ function f(){ const e=_aura.etat();
      if(e.tick!==k0){ k0=e.tick; out.push([+(performance.now()).toFixed(1), +(e.dtReel*1000).toFixed(1), +(e.dernier||0).toFixed(1), +e.vlac.toFixed(3)]); }
      if(performance.now()-t0<ms) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(os.environ.get('APP_AURA', 'http://127.0.0.1:8752/app.html')); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{window.__lt=[];try{new PerformanceObserver(l=>{l.getEntries().forEach(e=>window.__lt.push([+e.startTime.toFixed(1),+e.duration.toFixed(1)]));}).observe({type:'longtask',buffered:true});}catch(e){}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(1500)
    r = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect();const d=document.getElementById('device').getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,sc:d.width/390};}")
    cdp = pg.context.new_cdp_session(pg)
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 500}); cdp.send('Profiler.start')
    pg.evaluate("()=>{window.__lt=[];}")
    images = []
    for k in range(3):
        for _ in range(120):
            if pg.evaluate("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp;}"): break
            pg.wait_for_timeout(100)
        t = pg.evaluate(LANCE, [r['cx'] - 70 * r['sc'], r['cy'], 132 * r['sc'], 6, 16, 0])
        images += [x + [k] for x in pg.evaluate(ENREG, 6000)]
    prof = cdp.send('Profiler.stop')['profile']
    lt = pg.evaluate("()=>window.__lt")
    b.close()

# le temps PROPRE de chaque fonction, sur toute la fenêtre des lancers
nodes = {n['id']: n for n in prof['nodes']}
selft = collections.Counter()
for sid, dt in zip(prof['samples'], prof['timeDeltas']):
    cf = nodes[sid]['callFrame']
    nom = cf['functionName'] or '(anonyme)'
    url = cf['url'].rsplit('/', 1)[-1] if cf['url'] else ''
    selft['%s  %s:%d' % (nom, url, cf['lineNumber'] + 1)] += dt / 1000.0
tot = sum(selft.values())
print('\nIMAGES LONGUES (> 50 ms) pendant les trois élans — [horloge ms, image ms, dont peintre ms, élan rad/s, lancer]')
for x in images:
    if x[1] > 50: print('  ', x)
print('\nTÂCHES LONGUES (> 50 ms) vues par le navigateur — [début ms, durée ms] :', lt)
print('\nTEMPS PROPRE, %d ms échantillonnés sur la fenêtre des lancers — les 18 premiers :' % tot)
for k, v in selft.most_common(18):
    print('   %7.1f ms  %5.1f %%   %s' % (v, 100 * v / tot, k))
json.dump({'images': images, 'lt': lt}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profil_elan.json'), 'w'))
