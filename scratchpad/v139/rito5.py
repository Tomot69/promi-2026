import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch()
    for monde in (sys.argv[2] if len(sys.argv)>2 else 'ritournelle,bobinette,encre').split(','):
      for n in (1,3,19):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
        pg.evaluate("([m,n])=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} if(n<19){var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){}} Toile.setTheme(m); Toile.sync(promises.map(p=>p.id));}",[monde,n]); pg.wait_for_timeout(2500)
        r=pg.evaluate("""()=>new Promise(res=>{ const T=[]; let av=performance.now(), t0=av; (function f(t){ T.push(t-av); av=t; if(t-t0<4000) requestAnimationFrame(f); else { T.sort((a,b)=>a-b); res({n:T.length, p50:+T[T.length>>1].toFixed(1), p95:+T[Math.floor(T.length*.95)].toFixed(1), max:+T[T.length-1].toFixed(1), tourne:Toile.vivant.boucle()}); } })(av); })""")
        # coût d'un rendu forcé
        c=pg.evaluate("()=>{ const t=performance.now(); for(let i=0;i<3;i++){ try{Toile.kick&&Toile.kick()}catch(e){} } return 0}")
        print(monde,n,r); ctx.close()
    b.close()
