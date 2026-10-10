import sys
from playwright.sync_api import sync_playwright
out=sys.argv[1]; files=sys.argv[2:]
with sync_playwright() as p:
    b=p.webkit.launch()
    for f in files:
        for th in ('light','dark'):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}"%th)
            pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:150])); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
            pg.evaluate("(th)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} var d=document.getElementById('device'); if(th=='light'){ if(!d.classList.contains('light')&&window.setLight) try{setLight(true)}catch(e){} } closeAll(); document.getElementById('souffleBtn').click();}",th); pg.wait_for_timeout(7000)
            info=pg.evaluate("()=>{try{_aura.fige(true);_aura.vue(0.3,0.2);}catch(e){} var d=document.getElementById('device'); var c=document.getElementById('auBouleGL')||document.getElementById('auBoule'); var r=c.getBoundingClientRect(); return {light:d.classList.contains('light'),gl:!!document.getElementById('auBouleGL'),r:[r.left,r.top,r.width,r.height], et:(window._aura&&_aura.etat)?JSON.stringify(_aura.etat().palier):''}}")
            pg.wait_for_timeout(1500)
            r=info['r']; nm='%s/pel-%s-%s.png'%(out,f.replace('.html',''),th)
            pg.screenshot(path=nm,clip={'x':r[0]-10,'y':r[1]-10,'width':r[2]+20,'height':r[3]+40})
            print(f,th,info,er[:2])
            ctx.close()
    b.close()
