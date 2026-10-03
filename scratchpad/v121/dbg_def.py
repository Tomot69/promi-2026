from playwright.sync_api import sync_playwright
JS="()=>{closeAll(); openEssaim('potager'); var n=0; (function essai(){ try{ if(window._nueeDefile) window._nueeDefile(true); }catch(e){} if(++n<6) setTimeout(essai,400); })();}"
Q="""()=>{const dv=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('canvas')].filter(c=>{const r=c.getBoundingClientRect(); const cs=getComputedStyle(c); return r.width>8&&r.height>8&&r.bottom>dv.top&&r.top<dv.bottom&&r.right>dv.left&&r.left<dv.right&&cs.display!=='none'&&cs.visibility!=='hidden'&&+cs.opacity>0.05;}).map(c=>{const r=c.getBoundingClientRect(); let dom=''; try{const g=c.getContext('2d'),d=g.getImageData(0,0,c.width,c.height).data,h={}; let n=0; for(let i=0;i<d.length;i+=4*13){ if(d[i+3]<250) continue; n++; const q=d[i]+','+d[i+1]+','+d[i+2]; h[q]=(h[q]||0)+1;} dom=Object.entries(h).sort((a,b)=>b[1]-a[1]).slice(0,3).map(a=>a[0]+' '+(100*a[1]/n).toFixed(0)+'%').join(' | ');}catch(e){dom='?'} return (c.id||c.className||c.parentElement.id)+' '+Math.round(r.top-dv.top)+'..'+Math.round(r.bottom-dv.top)+' '+c.width+'×'+c.height+' :: '+dom+' :: parent '+(c.parentElement.id||c.parentElement.className)});}"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for url in ('app.html','zz-ref-v118.html'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');Math.random=(function(){var s=20261002;return function(){s=(s*1664525+1013904223)%4294967296;return s/4294967296;};})();}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(700)
        pg.evaluate(JS); pg.wait_for_timeout(7000)
        print('==',url); [print('  ',x[:260]) for x in pg.evaluate(Q)]
        pg.screenshot(path='scratchpad/v121/def-%s.png'%url[:6],clip={'x':20,'y':44,'width':390,'height':844}); ctx.close()
    b.close()
