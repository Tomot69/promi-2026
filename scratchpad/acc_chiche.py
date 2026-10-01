from playwright.sync_api import sync_playwright
ST="()=>{const s=document.getElementById('createSheet');const v=document.querySelector('#csPhrase .ph-b');return [s.dataset.kind,s.className,window.createKind,window._phrase&&window._phrase.sens,v&&v.innerText]}"
with sync_playwright() as p:
    b=p.chromium.launch()
    for mode in ['doigt','souris']:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=(mode=='doigt'))
        pg=ctx.new_page(); pg.goto("http://127.0.0.1:8752/app.html"); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        cdp=ctx.new_cdp_session(pg)
        for kind in ['chiche','nuee','promi','chiche']:
            if mode=='doigt': pg.locator('#createBtn').tap()
            else: pg.locator('#createBtn').click()
            pg.wait_for_timeout(1500)
            bb=pg.locator('#createSheet .tile[data-kind=%s]'%kind).first.bounding_box()
            x,y=bb['x']+bb['width']/2,bb['y']+bb['height']/2
            if mode=='doigt':
                cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
                pg.wait_for_timeout(80)
                cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            else: pg.mouse.click(x,y)
            pg.wait_for_timeout(2200)
            print(mode,kind,pg.evaluate(ST))
            pg.screenshot(path='scratchpad/acc_ch_%s_%s.png'%(mode,kind))
            pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(900)
        ctx.close()
    b.close()
