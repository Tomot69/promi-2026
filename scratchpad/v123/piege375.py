from playwright.sync_api import sync_playwright
J=r"""()=>new Promise(async res=>{ const F=t=>promises.filter(q=>q.title===t)[0].id; const L=[]; 
  closeAll(); openDetail(F('planter un arbre')); await new Promise(r=>setTimeout(r,2200)); closeAll(); await new Promise(r=>setTimeout(r,700));
  const el=document.getElementById('dptQui'), dp=document.getElementById('detailPoster'); const t0=performance.now();
  const sp=CSSStyleDeclaration.prototype.setProperty; CSSStyleDeclaration.prototype.setProperty=function(k,v,p){ if(this===el.style&&/color/.test(k)){ L.push(((performance.now()-t0)|0)+' set '+k+'='+v+' '+(p||'')+' @ '+(new Error().stack||'').split('\n').slice(1,5).map(s=>s.trim().slice(0,70)).join(' < ')); } return sp.apply(this,arguments); };
  new MutationObserver(m=>m.forEach(x=>L.push(((performance.now()-t0)|0)+' mut '+x.target.id+' '+x.attributeName+' → '+(x.target.getAttribute(x.attributeName)||'').slice(0,110)))).observe(dp,{attributes:true,attributeFilter:['class']});
  new MutationObserver(m=>m.forEach(x=>L.push(((performance.now()-t0)|0)+' mut dptQui '+x.attributeName+' → '+(el.getAttribute(x.attributeName)||'').slice(0,160)))).observe(el,{attributes:true});
  L.push('avant: '+getComputedStyle(el).color+' cls '+dp.className.slice(0,120));
  openDetail(F('faire les crêpes')); L.push(((performance.now()-t0)|0)+' apres openDetail sync: '+getComputedStyle(el).color);
  let n=0; (function f(){ L.push(((performance.now()-t0)|0)+' rAF '+getComputedStyle(el).color+' show='+dp.classList.contains('show')+' op='+getComputedStyle(dp).opacity); if(++n<14) requestAnimationFrame(f); else setTimeout(()=>{CSSStyleDeclaration.prototype.setProperty=sp; res(L)},900); })(); })"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light')}"); pg.wait_for_timeout(500)
    for l in pg.evaluate(J): print(l[:420])
