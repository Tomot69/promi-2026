from playwright.sync_api import sync_playwright
JS="()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"
Q="""()=>{const e=document.getElementById('csTrameCv'); const g=e.getContext('2d'), W=e.width,H=e.height, d=g.getImageData(0,0,W,H).data, h={}; let n=0; for(let i=0;i<d.length;i+=4*7){ if(d[i+3]<250) continue; n++; const q=d[i]+','+d[i+1]+','+d[i+2]; h[q]=(h[q]||0)+1; }
 return {W,H, vis:getComputedStyle(e).opacity+'/'+getComputedStyle(e).display, bg:getComputedStyle(document.getElementById('createSheet')).backgroundColor, champ:e.getAttribute('data-champ'), mat:e.getAttribute('data-matiere'), dom:Object.entries(h).sort((a,b)=>b[1]-a[1]).slice(0,6).map(a=>a[0]+' '+(100*a[1]/n).toFixed(0)+'%'), nat:(()=>{const f=document.getElementById('dptNat');return f?getComputedStyle(f).color:''})()}}"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for url in ('app.html','zz-ref-v116.html'):
        for th in ('dark','light'):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(600)
            pg.evaluate(JS); pg.wait_for_timeout(3000); print(url,th,pg.evaluate(Q))
            pg.screenshot(path='scratchpad/v120/plus-%s-%s.png'%(url[:6],th),clip={'x':20,'y':44,'width':390,'height':844}); ctx.close()
    b.close()
