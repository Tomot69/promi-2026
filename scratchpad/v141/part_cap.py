import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]; out=sys.argv[2]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')})}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    for k,sel in (('promi','!p.chiche'),('chiche','!!p.chiche')):
        pg.evaluate("()=>{ try{closeAll(); document.getElementById('shareScreen').classList.remove('show');}catch(e){} }"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{ var p=promises.find(p=>!p.draft&&!p.nuee&&!p.req&&(%s)); openDetail(p.id); }"%sel); pg.wait_for_timeout(1800)
        pg.evaluate("()=>window.ouvrirPartage()"); pg.wait_for_timeout(3500)
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path=out%k,clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]})
        print(k, pg.evaluate("()=>{const c=window._plancheComp; const cv=document.getElementById('shCanvas'); return [c&&c.cases, cv&&cv.getAttribute('data-planche'), cv&&[cv.clientWidth,cv.clientHeight]]}"))
    b.close()
