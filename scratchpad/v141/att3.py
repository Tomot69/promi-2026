from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("""window.__J=[]; var iv=setInterval(function(){ try{ if(!window.Toile||!Toile.plantOne||Toile.plantOne.__w) return; var f=Toile.plantOne; Toile.plantOne=function(){ var s=f.apply(this,arguments); try{ window.__J.push(['plant', s&&Math.round(s.x), s&&Math.round(s.y), Math.round(performance.now())]); }catch(e){} return s; }; Toile.plantOne.__w=1; }catch(e){} },5);
      setInterval(function(){ try{ var g=Toile_lecture().graines.filter(function(g){return g.kind!=='gray'&&g.y>660}).map(function(g){return [g.pid,Math.round(g.x),Math.round(g.y)]}); if(g.length) window.__J.push(['bas',JSON.stringify(g),Math.round(performance.now())]); }catch(e){} },400);""")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light');}"); pg.wait_for_timeout(2500)
    J=pg.evaluate("()=>window.__J")
    pl=[j for j in J if j[0]=='plant']; print(len(pl),'plantations ; sous 649 :',[j for j in pl if j[2] and j[2]>649][:6])
    seen=None
    for j in J:
        if j[0]=='bas' and j[1]!=seen: seen=j[1]; print(j[2], j[1][:300])
    b.close()
