import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]; init=sys.argv[2] if len(sys.argv)>2 else ''
with sync_playwright() as p:
    b=p.webkit.launch()
    for essai in range(3):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}"+init)
        ctx.add_init_script("document.addEventListener('DOMContentLoaded',function(){ var s=document.createElement('style'); s.textContent='#detailPoster,#detailPoster *{transition:none!important}'; document.head.appendChild(s); });")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
        r=pg.evaluate("""()=>new Promise(res=>{ const p=promises.filter(q=>q.title==='faire les crêpes')[0]; const out=[]; const t0=performance.now(); openDetail(p.id);
          const lit=(lab)=>{ const dp=document.getElementById('detailPoster'), q=document.getElementById('dptQui'); out.push(lab+' t'+Math.round(performance.now()-t0)+' show='+dp.classList.contains('show')+' op='+getComputedStyle(dp).opacity+' quiTop='+Math.round(q.getBoundingClientRect().top)+' bg='+getComputedStyle(dp).backgroundColor); };
          lit('sync'); let n=0; (function f(){ requestAnimationFrame(()=>{ const ch=new MessageChannel(); ch.port1.onmessage=()=>{ lit('img'+n); if(++n<6) f(); else res(out); }; ch.port2.postMessage(0); }); })(); })""")
        print(essai, ' | '.join(r)); ctx.close()
    b.close()
