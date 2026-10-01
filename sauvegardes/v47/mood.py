# Le voile, mesuré : dans chaque téléphone du moodboard, l'alpha appliqué image par image pendant une plantation.
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1300,'height':900},device_scale_factor=1)
    er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:100]))
    pg.goto('http://127.0.0.1:8752/moodboard-celebration.html'); pg.wait_for_timeout(14000)
    print(pg.evaluate("()=>document.getElementById('etat').textContent"))
    r=pg.evaluate("""async()=>{ document.getElementById('pause').click(); await new Promise(r=>setTimeout(r,2500));
      const fr=[...document.querySelectorAll('iframe')]; const series=fr.map(()=>[]);
      document.getElementById('un').click(); const t0=performance.now();
      await new Promise(res=>{ function f(){ const e=performance.now()-t0; fr.forEach((x,i)=>{ const w=x.contentWindow; const c=w._celebration; series[i].push([Math.round(e), c? +((c.a||0.1)*(w._celebrationNiveau||0)).toFixed(3):0]); });
        if(e<1800) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
      return series.map(s=>s.filter((q,k)=>k%6===0).map(q=>q[0]+':'+q[1]).join(' ')); }""")
    for s in r: print(s)
    print('erreurs', er[:3])
    pg.screenshot(path='sauvegardes/v47/moodboard.png')
    b.close()
