from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5200)
        print(th,'AURA', pg.evaluate(r"""()=>{const out=[];
          document.querySelectorAll('#auraScreen .au-nb').forEach(n=>{const s=n.querySelector('svg'); if(!s) return;
            const a=s.querySelector('path'); const r=n.getBoundingClientRect();
            out.push({d:Math.round(r.width), ep:a?a.getAttribute('stroke-width'):null, filet:getComputedStyle(n).boxShadow.slice(0,30)});});
          return out.slice(0,2);}"""))
        pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}"); pg.wait_for_timeout(2600)
        print(th,'FICHE', pg.evaluate(r"""()=>{const out=[];
          document.querySelectorAll('#detailPoster canvas.kr-c').forEach(c=>{const r=c.getBoundingClientRect();
            out.push({d:Math.round(r.width), ep:Math.round(c.width*window.KR_LW/(c.width/r.width)), filet:getComputedStyle(c).boxShadow.slice(0,30)});});
          return out;}"""))
    b.close()
