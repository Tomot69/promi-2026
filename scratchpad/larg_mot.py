from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(5000)
    print(pg.evaluate(r"""()=>{const M=document.querySelector('#auraScreen .au-mot');
      const cs=getComputedStyle(M), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
      const c=document.createElement('canvas').getContext('2d');
      const out=[];
      for(const fs of [18.9,19.5,20,20.5,21]){
        c.font=cs.fontWeight+' '+fs+'px '+cs.fontFamily;
        const L=(window._aura&&_aura.MOTS)||[M.textContent];
        out.push([fs, L.map(t=>Math.round(c.measureText(t).width))]);}
      return {boite:Math.round(M.getBoundingClientRect().width/s), essais:out};}"""))
    b.close()
