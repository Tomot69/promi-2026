import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for M in sys.argv[1:]:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
        pg.evaluate("(n)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} }",2)
        pg.evaluate("(m)=>{Toile.setTheme(m); Toile.sync([]); }",M); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{ Toile.sync(promises.slice(0,1).map(p=>p.id)); }"); pg.wait_for_timeout(60)
        a=pg.evaluate("()=>{var L=Toile_lecture(); return L.graines.filter(g=>g.kind!='gray').map(g=>[Math.round(g.w*10)/10, g.boite&&[g.boite.x0,g.boite.x1,g.boite.y0,g.boite.y1].map(Math.round)]);}")
        pg.wait_for_timeout(3500)
        z=pg.evaluate("()=>{var L=Toile_lecture(); return [L.vue.s, L.graines.filter(g=>g.kind!='gray').map(g=>[Math.round(g.w*10)/10, g.boite&&[g.boite.x0,g.boite.x1,g.boite.y0,g.boite.y1].map(Math.round)])];}")
        print(M,'à 60 ms',a,'| posée',z); ctx.close()
    b.close()
