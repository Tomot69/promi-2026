import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for url in sys.argv[1:]:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(3000)
        print(url); 
        for l in pg.evaluate("()=>[...document.querySelectorAll('#indexList .s4-carte')].map(c=>{const t=c.querySelector('.s4-et'), e=c.querySelector('.s4-eb'), ti=c.querySelector('.s4-ti'); return (ti?ti.textContent:'?').slice(0,22)+' | '+(t?t.textContent.trim().slice(0,22)+' '+getComputedStyle(t).color+' lis='+t.getAttribute('data-lis'):'-')+' | eb '+(e?getComputedStyle(e).color+' '+e.textContent.trim().slice(0,14):'-')+' | fond '+getComputedStyle(c).backgroundColor+' '+(c.getAttribute('data-etat')||'')})"): print('   ',l)
        ctx.close()
    b.close()
