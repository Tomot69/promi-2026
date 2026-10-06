from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light');}"); pg.wait_for_timeout(500)
    for nom,js in [('promi-tenu','openDetail(125)'),('chiche-tenu','openDetail(129)'),('pp-promi',0),('pp-chiche',1),('pp-cercle',2)]:
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(500)
        if isinstance(js,int):
            pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
            for k in range(3): pg.evaluate("(i)=>{const t=document.querySelectorAll('#createSheet .tile')[i]; if(t) t.click();}", js); pg.wait_for_timeout(500)
            pg.wait_for_timeout(1500)
        else: pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(3000)
        f=SC+'cl3-%s.png'%nom; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
    P=Image.new('RGB',(400*len(ims),844),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f).resize((390,844)),(i*400,0))
    P.save(SC+'clair3.png'); b.close()
