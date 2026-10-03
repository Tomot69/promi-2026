from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/zz-av125.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); document.getElementById('souffleBtn').click();}")
    pg.wait_for_timeout(4000)
    print(pg.evaluate("""()=>{ const M=PeloteMoteur; let O=null; const f=M.peint; M.peint=function(c,o){O=o; return f(c,o)}; _aura.pelote(); M.peint=f;
      const r={};
      for(const n of [220000,110000,75000]){ const c=document.createElement('canvas'); const o=Object.assign({},O,{sansPeau:true}); if(n!==220000){ continue; }
        M.peint(c,o); const W=c.width, d=c.getContext('2d').getImageData(0,0,W,W).data; let t=0, vide=0, part=0, sa=0;
        for(let y=0;y<W;y++) for(let x=0;x<W;x++){ if(Math.hypot(x-W/2,y-W/2)>W*0.36) continue; const a=d[(y*W+x)*4+3]; t++; if(a===0) vide++; else if(a<250) part++; sa+=1-a/255; }
        r[n]={pixels:t, 'sans poil %':+(vide/t*100).toFixed(1), 'poil translucide %':+(part/t*100).toFixed(1), 'part du corps dans la couleur %':+(sa/t*100).toFixed(1)}; }
      return JSON.stringify(r)+' n='+(O.n||'')+' cles '+Object.keys(O).join(','); }"""))
    b.close()
