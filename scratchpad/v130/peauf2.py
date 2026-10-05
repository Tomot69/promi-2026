from playwright.sync_api import sync_playwright
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{closeAll();const p=promises.filter(q=>q.title==='planter un arbre')[0];openDetail(p.id);}"); pg.wait_for_timeout(2000)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(2000)
    pg.screenshot(path=SC+'peauf1.png',clip={'x':20,'y':44,'width':390,'height':844})
    pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(900)
    pg.screenshot(path=SC+'peauf2.png',clip={'x':20,'y':44,'width':390,'height':844})
    b.close()
from PIL import Image
a=Image.open(SC+'peauf1.png'); c=Image.open(SC+'peauf2.png'); P=Image.new('RGB',(800,844),(255,255,255)); P.paste(a,(0,0)); P.paste(c,(410,0)); P.save(SC+'peauf.png')
