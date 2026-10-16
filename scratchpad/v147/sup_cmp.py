from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3)
    ctx.add_init_script("try{ localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); }catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{ var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} var s=document.createElement('style'); s.textContent='#device > *:not(.tlx){visibility:hidden!important}'; document.head.appendChild(s); }")
    for sm in (4, 2):
        for k, fr in enumerate((0.25, 0.45, 0.65, 0.85)):
            pg.evaluate("""async (a)=>{ const [sm, fr, k]=a; TraceLettres.supMax=sm; TraceLettres._cache={}; const d=document.createElement('div'); d.className='tlx'; d.style.cssText='position:absolute;left:12px;top:'+(60+k*120)+'px;width:370px;font:500 27px/32px Atkinson,system-ui;color:#291547;background:transparent';
              d.textContent='gé tf hm Quid'; document.getElementById('device').appendChild(d); const c=TraceLettres.trace(d,null,{cps:50, manuel:true}); await c.pret; c.va(fr); }""", [sm, fr, k])
        pg.wait_for_timeout(300)
        dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width];}")
        pg.screenshot(path='scratchpad/v147/sup%d.png' % sm, clip={'x': dv[0], 'y': dv[1] + 50, 'width': dv[2], 'height': 500})
        pg.evaluate("()=>{ document.querySelectorAll('.tlx').forEach(e=>{ try{ e.__trace&&e.__trace.stop(); }catch(_){} e.remove(); }); document.querySelectorAll('#device > canvas').forEach(c=>{ if(!c.id) c.remove(); }); }")
    b.close()
