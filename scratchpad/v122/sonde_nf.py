import sys
from playwright.sync_api import sync_playwright
J="""()=>[...document.querySelectorAll('.nf-item')].map(it=>{const c=it.querySelector('canvas.nf-d'); const t=(it.textContent||'').trim().slice(0,22); if(!c||!c.width) return t+' : -'; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,h={};let n=0; for(let i=0;i<d.length;i+=16){ if(d[i+3]<250) continue; n++; const k=(d[i]>>4)+','+(d[i+1]>>4)+','+(d[i+2]>>4); h[k]=(h[k]||0)+1;} const top=Object.entries(h).sort((a,b)=>b[1]-a[1]).slice(0,2).map(a=>a[0]+':'+Math.round(100*a[1]/n)); return t+' : '+it.className.replace('nf-item','')+' : '+top.join(' ');})"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for f in sys.argv[1:]:
      for k in range(2):
        ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); closeAll(); openEssaim('potager'); setTimeout(()=>{try{window._nueeDefile(true)}catch(e){}},500)}"); pg.wait_for_timeout(3500)
        print(f,k); [print('   ',x) for x in pg.evaluate(J)]; ctx.close()
