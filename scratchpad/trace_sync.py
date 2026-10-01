from playwright.sync_api import sync_playwright
PIEGE="""(()=>{ window.__tr=[]; const t0=performance.now(); let T=null;
  const arme=()=>{ if(!window.Toile||!Toile.sync||Toile.__p) return setTimeout(arme,5); Toile.__p=1;
    for(const f of ['sync','addPromi','setTheme','addNuee','addMember','reGray']){ const o=Toile[f]; Toile[f]=function(){ window.__tr.push([Math.round(performance.now()-t0),f,JSON.stringify([...arguments]).slice(0,80)]); return o.apply(this,arguments); }; } };
  arme(); })();"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for i in range(3):
        ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}"); ctx.add_init_script(PIEGE)
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
        tr=pg.evaluate("()=>window.__tr"); print('ouverture',i+1,len(tr)); [print('   ',x) for x in tr[:25]]
        ctx.close()
