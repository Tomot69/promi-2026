from playwright.sync_api import sync_playwright
from PIL import Image
clip={'x':20,'y':44,'width':390,'height':844}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; openDetail(p.id);}"); pg.wait_for_timeout(3000); pg.screenshot(path='scratchpad/v127/vu-chiche.png',clip=clip)
    pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(3000); pg.screenshot(path='scratchpad/v127/vu-cercle.png',clip=clip)
    print(pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('#detailPoster *')].filter(e=>e.children.length===0&&/TRACE|LANCE|Avec|AVEC/.test(e.textContent||'')).slice(0,6).map(e=>{const r=e.getBoundingClientRect(); return e.className+' '+e.id+' '+(e.textContent||'').slice(0,30)+' y'+Math.round(r.top-dv.top)+' h'+Math.round(r.height)})}"))
    pg.evaluate("()=>{setTheme('dark')}"); pg.wait_for_timeout(2500); pg.screenshot(path='scratchpad/v127/vu-cercle-d.png',clip=clip)
    b.close()
ims=[Image.open('scratchpad/v127/vu-%s.png'%n).resize((390,844)) for n in ('chiche','cercle','cercle-d')]
Q=Image.new('RGB',(390*3,844)); [Q.paste(a,(390*i,0)) for i,a in enumerate(ims)]; Q.save('scratchpad/v127/vu-tri.png')
