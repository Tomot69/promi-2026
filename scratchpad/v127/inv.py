from playwright.sync_api import sync_playwright
JS=r"""(sel)=>{ const dv=document.getElementById('device').getBoundingClientRect(); const out=[]; document.querySelectorAll(sel).forEach(e=>{ const r=e.getBoundingClientRect(); if(r.width<8||r.height<8||r.width>380) return; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.1) return; if(r.left<dv.left-2||r.right>dv.right+2||r.top<dv.top||r.bottom>dv.bottom) return;
  out.push([e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+'.'+String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className).split(' ').slice(0,3).join('.'), Math.round(r.left-dv.left)+','+Math.round(r.top-dv.top)+' '+Math.round(r.width)+'×'+Math.round(r.height), cs.borderTopWidth+' '+cs.borderRadius, (e.textContent||'').trim().slice(0,22), e.querySelector('svg')?'svg':'' ].join(' | ')); }); return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(3000)
    print('== FICHE'); [print(x) for x in pg.evaluate(JS,'#detailPoster button, #detailPoster [role=button], #detailPoster .closeb, #detailPoster svg, #detailPoster [onclick]')]
    print(pg.evaluate("()=>{const e=document.querySelector('[id*=Photo],[class*=photo]'); return e?e.outerHTML.slice(0,900):''}"))
    print(pg.evaluate("()=>JSON.stringify(window._ondeFiche||window._onde||null)"))
    pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(3500)
    print('== STUDIO'); [print(x) for x in pg.evaluate(JS,'#studioScreen button, #studioScreen [role=button], #studioScreen [onclick], #studioScreen .stc-disq, #studioScreen [class*=disq], #studioScreen [class*=pal], #studioScreen [class*=orb]')][:0]
    b.close()
