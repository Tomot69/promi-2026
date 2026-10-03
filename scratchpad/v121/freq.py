from playwright.sync_api import sync_playwright
INIT="try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');Math.random=(function(){var s=20261002;return function(){s=(s*1664525+1013904223)%4294967296;return s/4294967296;};})();window.__tFige=null;var _pn=performance.now.bind(performance);performance.now=function(){return window.__tFige!=null?window.__tFige:_pn();};}catch(e){}"
JS="()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"
with sync_playwright() as p:
    b=p.webkit.launch()
    for url in ('app.html','zz-ref-v118.html'):
        r=[]
        for i in range(6):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); ctx.add_init_script(INIT)
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",'dark'); pg.wait_for_timeout(700)
            pg.evaluate(JS); pg.wait_for_timeout(5000)
            r.append(pg.evaluate("()=>getComputedStyle(document.getElementById('dptQui')).color")); ctx.close()
        print(url, r)
    b.close()
