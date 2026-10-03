from playwright.sync_api import sync_playwright
import sys
T={'à tenir':'faire les crêpes'}
Q="()=>['dptNat','dptQui','dptTitre','dptQuand','dptTrace'].map(i=>{const e=document.getElementById(i); return e?getComputedStyle(e).color.replace(/rgb\\(|\\)| /g,''):'-'}).join(' | ')+' || corps '+getComputedStyle(document.getElementById('detailPoster')).backgroundColor"
with sync_playwright() as p:
    b=p.webkit.launch()
    for url in ('app.html','zz-ref-v118.html'):
        for nom,ti in T.items():
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');Math.random=(function(){var s=20261002;return function(){s=(s*1664525+1013904223)%4294967296;return s/4294967296;};})();window.__tFige=null;var _pn=performance.now.bind(performance);performance.now=function(){return window.__tFige!=null?window.__tFige:_pn();};}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(600)
            pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}",ti)
            r=[]
            for w in (700,1500,2500,4000,6000,9000):
                pg.wait_for_timeout(w if not r else 1200); r.append(pg.evaluate(Q))
            print(url[:10],'%-9s'%nom, ' → '.join(sorted(set(r),key=r.index)))
            if nom=='à tenir': pg.screenshot(path='scratchpad/v120/fiche-%s.png'%url[:6],clip={'x':20,'y':44,'width':390,'height':844})
            ctx.close()
    b.close()
