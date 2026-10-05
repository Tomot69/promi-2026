from playwright.sync_api import sync_playwright
P=r"""()=>{ window.__g=[]; const f=Toile.dalleTrame; Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
 try{ const g=dcv.getContext('2d'), d=g.getImageData(0,0,dcv.width,dcv.height).data, H={}; let n=0; for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; n++; const q=(d[i]>>4)+','+(d[i+1]>>4)+','+(d[i+2]>>4); H[q]=(H[q]||0)+1; }
  const T=Object.entries(H).sort((a,b)=>b[1]-a[1]).slice(0,3).map(e=>e[0].split(',').map(v=>v*16+8).join('/')+':'+Math.round(100*e[1]/n)+'%'); window.__g.push(pid+' '+dcv.width+'x'+dcv.height+' '+T.join(' ')+' opts='+JSON.stringify(opts||{}).slice(0,90)+' monde='+JSON.stringify(monde||null)); }catch(e){} return r; }; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','dark')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); Toile.setTheme('mosaique');}"); pg.wait_for_timeout(2500); pg.evaluate(P)
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(2600)
    for l in pg.evaluate("()=>window.__g"): print(l[:260])
    b.close()
