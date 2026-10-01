from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(pg.evaluate(r"""()=>{const out=[];
      document.querySelectorAll('#device svg,#device path,#device circle,#device rect').forEach(e=>{
        const f=(e.getAttribute('fill')||'').toUpperCase(); if(f!=='#8FE08F') return;
        const r=e.getBoundingClientRect(); const cs=getComputedStyle(e);
        let p=e,ch=[]; for(let i=0;i<5&&p;i++,p=p.parentElement) ch.unshift((p.tagName||'').toLowerCase()+(p.id?'#'+p.id:'')+(p.className&&typeof p.className==='string'?'.'+p.className.trim().split(/\s+/).join('.'):(p.className&&p.className.baseVal?'.'+p.className.baseVal:'')));
        out.push({ch:ch.join(' > '), w:Math.round(r.width), h:Math.round(r.height), y:Math.round(r.top), vis:cs.visibility, op:cs.opacity, ecran:(e.closest('.screen')||{}).id});});
      return out;}"""))
    b.close()
