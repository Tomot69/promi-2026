import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');['tenir','chiche','planter','bande'].forEach(g=>localStorage.setItem('geste_vu_'+g,'1'));}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+sys.argv[1]); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} openDetail(promises.find(p=>p.title==='le grand plongeoir').id)}"); pg.wait_for_timeout(3000)
    print(pg.evaluate("()=>{const q=document.getElementById('dptQui'); return {html:q.innerHTML.slice(0,400), style:q.getAttribute('style'), col:getComputedStyle(q).color, enfants:[].map.call(q.querySelectorAll('*'),e=>[e.tagName,e.className,e.getAttribute('style'),getComputedStyle(e).color, getComputedStyle(e).webkitTextFillColor,e.getAttribute('data-lis')])}}"))
    b.close()
