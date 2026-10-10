import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    d=pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()"); cl={'x':d['x'],'y':d['y'],'width':390,'height':844}
    pg.screenshot(path='scratchpad/v140/vue-accueil.png',clip=cl)
    pg.evaluate("()=>document.getElementById('shareBtn').click()"); pg.wait_for_timeout(5000)
    pg.screenshot(path='scratchpad/v140/vue-partage.png',clip=cl)
    print(pg.evaluate("()=>[].map.call(document.querySelectorAll('#shareScreen button, #shareScreen [role=button]'),function(b){var r=b.getBoundingClientRect(); return r.width?[b.id||b.className, Math.round(r.left-%f), Math.round(r.top-%f), Math.round(r.width), Math.round(r.height), (b.textContent||'').trim().slice(0,24)]:null}).filter(Boolean)"%(d['x'],d['y'])))
    b.close()
