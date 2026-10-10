# planche-1 : référence d'avant v114 et nouveau rendu, clair et sombre, GL et secours ; + images par seconde
import sys
from playwright.sync_api import sync_playwright
INIT="try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin','aura-apparait'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});%s}catch(e){}"
with sync_playwright() as p:
    b=p.webkit.launch()
    for f,sec in (('zz-av114.html',0),('app.html',0),('app.html',1)):
        for th in ('light','dark'):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
            ctx.add_init_script(INIT%(th,'window._peloteGL=false;' if sec else ''))
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(7000)
            info=pg.evaluate("()=>{try{_aura.fige(true);_aura.vue(0.3,0.2);}catch(e){} var c=document.getElementById('auBouleGL')||document.getElementById('auBoule'); var r=c.getBoundingClientRect(); return {gl:!!document.getElementById('auBouleGL'),r:[r.left,r.top,r.width,r.height]}}")
            pg.wait_for_timeout(1500); r=info['r']
            pg.screenshot(path='scratchpad/v140/P1-%s-%d-%s.png'%(f.replace('.html',''),sec,th),clip={'x':r[0]-10,'y':r[1]-10,'width':r[2]+20,'height':r[3]+40})
            print(f,sec,th,info)
            if f=='app.html' and not sec:
                fps=pg.evaluate("""async()=>{ _aura.fige(false); var T=[],t0=performance.now(),l=t0; await new Promise(function(ok){ function f(t){ T.push(t-l); l=t; if(t-t0<6000) requestAnimationFrame(f); else ok(); } requestAnimationFrame(f); }); T=T.slice(5).sort(function(a,b){return a-b}); return {n:T.length, p50:T[T.length>>1], p95:T[(T.length*0.95)|0], ips:1000*T.length/T.reduce(function(a,b){return a+b},0), et:(_aura.etat?_aura.etat().palier:null)}; }""")
                print('  ips',fps)
            ctx.close()
    b.close()
