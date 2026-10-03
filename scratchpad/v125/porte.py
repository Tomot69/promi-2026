from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/zz-av125.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    info = pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); const c=(b.closest('button,[role=button],.acc-b,a')||b); const r=c.getBoundingClientRect(); return {id:c.id, cls:c.className, tag:c.tagName, x:r.left+r.width/2, y:r.top+r.height/2}}""")
    print(info)
    for i in range(6):
        pg.touchscreen.tap(info['x'], info['y']); pg.wait_for_timeout(2500)
        print(i, pg.evaluate("()=>JSON.stringify({sol:_aura.sol(), corps:_aura.corps&&_aura.corps()})")[:200])
        r = pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); const r=x.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}")
        pg.touchscreen.tap(r[0], r[1]); pg.wait_for_timeout(1200)
    b.close()
