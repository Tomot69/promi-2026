from playwright.sync_api import sync_playwright
from PIL import Image
clip={'x':20,'y':44,'width':390,'height':844}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(3000); pg.screenshot(path='scratchpad/v127/vu-fiche.png',clip=clip)
    pg.evaluate("()=>{document.querySelector('.ph-photo-btn').click()}"); pg.wait_for_timeout(900); pg.screenshot(path='scratchpad/v127/vu-menu.png',clip=clip)
    print(pg.evaluate("()=>{const m=document.querySelector('.ph-menu,[class*=ph-menu]'); return m?m.outerHTML.slice(0,1500):'pas de menu'}"))
    pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(3500); pg.screenshot(path='scratchpad/v127/vu-studio.png',clip=clip)
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3500); pg.screenshot(path='scratchpad/v127/vu-plus.png',clip=clip)
    b.close()
ims=[Image.open('scratchpad/v127/vu-%s.png'%n).resize((390,844)) for n in ('fiche','menu','studio','plus')]
Q=Image.new('RGB',(390*4,844)); [Q.paste(a,(390*i,0)) for i,a in enumerate(ims)]; Q.save('scratchpad/v127/vu-quad.png')
