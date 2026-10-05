from playwright.sync_api import sync_playwright
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} promises.forEach(p=>{ if(!p.draft&&!p.req&&(!p.from||p.from==='moi')) p.status='tenu'; }); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(3000)
    print(pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); const C=document.getElementById('auCadre'); const r=(s)=>{const e=document.querySelector('#auraScreen '+s); if(!e) return null; const b=e.getBoundingClientRect(); return [Math.round(b.top-dv.top),Math.round(b.bottom-dv.top)]}; return {n:[...document.querySelectorAll('#auraScreen .au-mo .au-c span')].map(e=>e.textContent), mo:r('.au-mo'), gr:r('.au-gr'), mo2:r('.au-mo2')||r('.au-zone2'), defile:[C.scrollHeight, C.clientHeight], err:window._auraErreur}}"))
    pg.evaluate("()=>{const C=document.getElementById('auCadre'); C.scrollTop=C.scrollHeight;}"); pg.wait_for_timeout(1200)
    pg.screenshot(path=SC+'aura-bas.png',clip={'x':20,'y':44,'width':390,'height':844})
    b.close()
