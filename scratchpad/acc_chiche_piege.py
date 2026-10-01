from playwright.sync_api import sync_playwright
TRAP=r"""()=>{window._J=[];const cs=document.getElementById('createSheet');const sa=cs.setAttribute.bind(cs);
cs.setAttribute=function(k,v){if(k==='data-kind')_J.push('data-kind='+v+' @'+(new Error().stack.split('\n')[2]||'').trim().slice(0,90));return sa(k,v);};
['touchstart','touchend','click'].forEach(t=>document.addEventListener(t,e=>{const el=e.target.closest&&e.target.closest('.tile');_J.push(t+' sur '+(el?el.dataset.kind:(e.target.id||e.target.className||e.target.tagName)));},true));
const tr=cs.querySelector('.tiles-track');new MutationObserver(()=>_J.push('track.transform='+tr.style.transform)).observe(tr,{attributes:true,attributeFilter:['style']});
new MutationObserver(()=>_J.push('class='+cs.className)).observe(cs,{attributes:true,attributeFilter:['class']});}"""
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    pg=ctx.new_page(); pg.goto("http://127.0.0.1:8752/app.html"); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    cdp=ctx.new_cdp_session(pg)
    pg.locator('#createBtn').tap(); pg.wait_for_timeout(1500)
    pg.evaluate(TRAP)
    bb=pg.locator('#createSheet .tile[data-kind=chiche]').first.bounding_box(); x,y=bb['x']+bb['width']/2,bb['y']+bb['height']/2
    print('chiche tuile', bb)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]}); pg.wait_for_timeout(80)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(1500)
    print('\n'.join(pg.evaluate("()=>_J")))
    print('elementFromPoint', pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);return e&&(e.id||e.className)}",[x,y]))
    b.close()
