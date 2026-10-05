from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(3000)
    for l in pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('detailPoster'); const f=(e,d)=>{const r=e.getBoundingClientRect(), c=getComputedStyle(e); return '  '.repeat(d)+e.tagName+'#'+e.id+'.'+String(e.className).slice(0,30)+' y'+Math.round(r.top-dv.top)+'→'+Math.round(r.bottom-dv.top)+' pos='+c.position+' z='+c.zIndex+' of='+c.overflowY+' disp='+c.display}; const out=[]; [...P.children].forEach(e=>{ out.push(f(e,0)); if(e.id==='dpMain') [...e.children].forEach(k=>{ if(k.getBoundingClientRect().height>0) out.push(f(k,1)); }); }); return out}"): print(l[:150])
    b.close()
