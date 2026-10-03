import sys
from playwright.sync_api import sync_playwright
J="""()=>[...document.querySelectorAll('.nf-item')].map(it=>{const c=it.querySelector('canvas.nf-d'); const t=(it.textContent||'').trim().slice(0,12); if(!c||!c.width) return t+':-'; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,h={};let n=0; for(let i=0;i<d.length;i+=16){ if(d[i+3]<250) continue; n++; const k=(d[i]>>4)+','+(d[i+1]>>4)+','+(d[i+2]>>4); h[k]=(h[k]||0)+1;} const top=Object.entries(h).sort((a,b)=>b[1]-a[1])[0]; return t+':'+(top?top[0]:'vide');}).join(' | ')"""
DEF="()=>{closeAll(); openEssaim('potager'); var n=0; (function essai(){ try{ if(window._nueeDefile) window._nueeDefile(true); }catch(e){} if(++n<6) setTimeout(essai,400); })();}"
with sync_playwright() as p:
    b=p.webkit.launch()
    for k in range(6):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+sys.argv[1]); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t)}",'dark' if k%2 else 'light'); pg.wait_for_timeout(600)
        pg.evaluate(DEF); 
        for w in (2200,900,900,1500):
            pg.wait_for_timeout(w); print(k, w, pg.evaluate(J)[:330])
        ctx.close()
