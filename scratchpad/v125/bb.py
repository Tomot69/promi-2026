from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
    pg.wait_for_timeout(4000)
    print(pg.evaluate("""()=>{ const M=PeloteMoteur; let O=null; const f=M.peintGL; M.peintGL=function(c,o){O=o; return f(c,o)}; _aura.pelote(); M.peintGL=f;
      const A=O.atlas, NIVA=6, r=[]; const NS=A.length/NIVA;
      for(let t=0;t<NS/72;t++){ let sx=0, ss=0, sb=0, n=0, ex=[];
        for(let s=t*72;s<t*72+72;s++){ const T=A[s*NIVA+NIVA-1]; let x0=99,x1=-99,y0=99,y1=-99; T.rel.forEach((q,j)=>{ if(!T.al[j])return; x0=Math.min(x0,q[1]);x1=Math.max(x1,q[1]);y0=Math.min(y0,q[0]);y1=Math.max(y1,q[0]); });
          const e=Math.max(-x0,x1,-y0,y1); ss+=(2*e+1)**2; sb+=(x1-x0+1)*(y1-y0+1); n+=T.rel.length; if(s%24==3) ex.push([x0,y0,x1,y1].join(',')); }
        r.push({t, carre:Math.round(ss/72), boite:Math.round(sb/72), pixels:Math.round(n/72), ex:ex.slice(0,2)}); }
      return JSON.stringify(r); }"""))
    b.close()
