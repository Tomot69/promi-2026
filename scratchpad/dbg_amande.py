from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")
    pg.wait_for_timeout(2400)
    print(pg.evaluate(r"""()=>{
      const dp=document.getElementById('detailPoster'), dv=document.getElementById('device');
      const q=document.querySelector('.dpt-quand'), u=document.querySelector('.dpt-qui');
      return {dansDevice: dv?dv.contains(dp):null,
        passeExiste: typeof window._amandeSurSombre,
        faits: window._amandeSurSombre ? window._amandeSurSombre() : null,
        quand:q?{col:getComputedStyle(q).color, fill:getComputedStyle(q).webkitTextFillColor, inline:q.getAttribute('style')||'', amande:q.getAttribute('data-amande')}:null,
        qui:u?{col:getComputedStyle(u).color, fill:getComputedStyle(u).webkitTextFillColor, sombre:window._fondSombreSous(u)}:null};}"""))
    b.close()
