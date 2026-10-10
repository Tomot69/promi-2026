from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    b=p.chromium.launch(); 
    for (x0,x1) in ((30,195),(195,360),(30,360),(120,300)):
        ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('geste_vu_tenir','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000); cdp=ctx.new_cdp_session(pg)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} openDetail(promises.find(q=>q.title==='faire les crêpes').id)}"); pg.wait_for_timeout(3000)
        P=pg.evaluate("([x0,x1])=>{var cv=document.getElementById('dpTrameCv'),t=cv.getAttribute('data-trait').split(','),r=cv.getBoundingClientRect(),f=window._onde.onde(+t[0],+t[1]),k=r.width/390,P=[];for(var x=x0;x<=x1;x+=8)P.push([r.left+x*k,r.top+f(x)*k]);return {P:P,t:t}}",[x0,x1])
        pts=P['P']; cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':pts[0][0],'y':pts[0][1]}]})
        for q in pts[1:]: cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':q[0],'y':q[1]}]}); pg.wait_for_timeout(25)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(2500)
        print((x0,x1),P['t'],'→',pg.evaluate("()=>promises.find(q=>q.title==='faire les crêpes').status")); ctx.close()
    b.close()
