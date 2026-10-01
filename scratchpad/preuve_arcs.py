import os
from playwright.sync_api import sync_playwright
URL=os.environ.get('APP_AURA')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(5000)
    print(pg.evaluate("""()=>{const out=[];document.querySelectorAll('#auraScreen .au-nb').forEach(n=>{
      const s=n.querySelector('svg'); if(!s) return;
      out.push({qui:(n.parentElement.querySelector('.au-lb')||{}).textContent,
        arcs:[...s.querySelectorAll('circle,path')].map(e=>[e.getAttribute('stroke-width'), e.getAttribute('stroke')])});});
      const lg=document.querySelector('#auraScreen .au-lg');
      return {n:out.slice(0,2), lgH: lg?lg.getBoundingClientRect().height:null, lgFs: lg?getComputedStyle(lg).fontSize:null, KR:window.KR_LW};}"""))
    b.close()
