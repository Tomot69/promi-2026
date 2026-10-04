# Houle au repos : chronologie — la boucle tourne-t-elle hors tirage, et l'image change-t-elle ?
from playwright.sync_api import sync_playwright
JS=r"""async (S)=>{ const cv=document.getElementById('toileCv'); const o=document.createElement('canvas'); o.width=cv.width>>1; o.height=cv.height>>1; const g=o.getContext('2d',{willReadFrequently:true});
 const lit=()=>{ g.drawImage(cv,0,0,o.width,o.height); return g.getImageData(0,0,o.width,o.height).data; }; const dif=(a,b)=>{ let n=0; for(let i=0;i<a.length;i+=4) if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>24) n++; return +(100*n/(a.length/4)).toFixed(3); };
 let ref=lit(), prev=ref; const t0=performance.now(), out=[]; let jl=Toile.vivant.journal().length;
 while(performance.now()-t0<S*1000){ await new Promise(r=>setTimeout(r,100)); const d=lit(), t=((performance.now()-t0)/1000).toFixed(1), a=dif(d,prev), b=dif(d,ref), bo=Toile.vivant.boucle(), J=Toile.vivant.journal(); let ev=''; if(J.length!==jl){ jl=J.length; ev=' TIRAGE n='+J[J.length-1].n+' d='+J[J.length-1].d; }
   if(a>0||bo||ev) out.push(t+'s Δimage '+a+' Δrepos '+b+(bo?' boucle':'')+ev); prev=d; }
 return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} Toile.setTheme('sillons');}"); pg.wait_for_timeout(6000)
    for l in pg.evaluate(JS, 50): print(l)
    b.close()
