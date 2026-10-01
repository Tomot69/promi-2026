from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{window.__kr=0; const f=window.drawKRing; window.drawKRing=function(){window.__kr++; return f.apply(this,arguments);};}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(400)
        for lab,js in (('fiche tenue',"()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}"),
                       ('fiche à tenir',"()=>{closeAll(); const p=promises.find(p=>p.status!=='tenu'&&!p.nuee&&!p.draft); if(p) openDetail(p.id);}")):
            pg.evaluate("()=>{window.__kr=0;}"); pg.evaluate(js); pg.wait_for_timeout(2200)
            print(th, lab, pg.evaluate(r"""()=>{
              const out={drawKRing:window.__kr, svg:[], canvas:[]};
              document.querySelectorAll('#detailPoster canvas').forEach(c=>{const r=c.getBoundingClientRect();
                if(r.width>10&&r.width<140) out.canvas.push({id:c.id||c.className, w:Math.round(r.width)});});
              document.querySelectorAll('#detailPoster svg').forEach(s=>{const r=s.getBoundingClientRect();
                if(r.width>10&&r.width<140) out.svg.push({cls:String(s.parentElement.className), w:Math.round(r.width), n:s.querySelectorAll('path,circle').length});});
              return out;}"""))
    b.close()
