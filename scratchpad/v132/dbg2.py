from playwright.sync_api import sync_playwright
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; p.dessin={v:1,w:390,h:754,fond:'#12FF34',pose:true,masque:false,traits:[],poses:[{c:'#201908',t:8,g:0,pts:[60,200,0,-1,200,260,200,-1,330,180,400,-1]}]}; openDetail(p.id); window.__n=0; const f=window._dessinCase; window._dessinCase=function(id){ window.__n++; return f(id); };}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>window.ouvrirPartage()"); pg.wait_for_timeout(2800)
    print(pg.evaluate("()=>({appels:window.__n, mode:(typeof shareMode!=='undefined'?shareMode:'?'), cvs:[...document.querySelectorAll('canvas')].filter(c=>{const r=c.getBoundingClientRect(); return r.width>60&&r.top<800&&r.bottom>60&&getComputedStyle(c).visibility!=='hidden'}).map(c=>c.id+' '+(c.closest('.screen,.sheet,[id$=Screen]')||{}).id+' '+c.width+'x'+c.height)})"))
    pg.screenshot(path=SC+'partage.png', clip={'x':20,'y':44,'width':390,'height':844}); b.close()
