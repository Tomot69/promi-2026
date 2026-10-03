import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for f in sys.argv[1:]:
        ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light')}"); pg.wait_for_timeout(500)
        for i in range(3):
            r=pg.evaluate("""()=>new Promise(res=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; openDetail(p.id); const out=[]; const t0=performance.now();
              (function f(){ const e=document.getElementById('dptQuand'); if(e) out.push(((performance.now()-t0)|0)+':'+e.textContent.trim().slice(0,30)+':'+getComputedStyle(e).color+':'+(e.getAttribute('data-lis')||'')); if(performance.now()-t0<3000) setTimeout(f,150); else res([p.status, p.state, out.filter((x,i,a)=>i==0||x.split(':').slice(1).join()!=a[i-1].split(':').slice(1).join())]); })(); })""")
            print(f,i,r)
        ctx.close()
