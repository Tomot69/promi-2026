from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for (x0,x1) in ((30,195),(30,360)):
        ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('geste_vu_planter','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000); cdp=ctx.new_cdp_session(pg)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })(); }"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{ try{ window._phrase.title='essai du trait'; var f=document.getElementById('fTitle'); if(f){ f.value='essai du trait'; f.dispatchEvent(new Event('input',{bubbles:true})); } }catch(e){} }"); pg.wait_for_timeout(600)
        n0=pg.evaluate("()=>promises.length")
        P=pg.evaluate("([x0,x1])=>{var e=window._ppEcran(), cv=document.getElementById('csTrameCv'), r=cv.getBoundingClientRect(), f=window._onde.onde(e.base,e.amp), k=r.width/390, P=[]; for(var x=x0;x<=x1;x+=8) P.push([r.left+x*k, r.top+f(x)*k]); return P}",[x0,x1])
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':P[0][0],'y':P[0][1]}]})
        for q in P[1:]: cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':q[0],'y':q[1]}]}); pg.wait_for_timeout(25)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(2500)
        print((x0,x1),'paroles',n0,'→',pg.evaluate("()=>promises.length"), pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')")); ctx.close()
    b.close()
