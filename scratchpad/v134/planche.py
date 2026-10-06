from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html?bleu=3'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); setPremium(false);}"); pg.wait_for_timeout(500)
    print('étiquette ?bleu= :', pg.evaluate("()=>!!document.getElementById('bleuEtiq')"), pg.evaluate("()=>getComputedStyle(document.documentElement).getPropertyValue('--c-cobalt50')"))
    def cap(n): f=SC+'b134-%s.png'%n; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
    pg.evaluate("()=>{closeAll(); openDetail(126);}"); pg.wait_for_timeout(3000); cap('atenir')
    pg.evaluate("()=>{closeAll(); openDetail(128);}"); pg.wait_for_timeout(3000); cap('encours')
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
    c=pg.evaluate("()=>{const q=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)').getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
    pg.evaluate("()=>localStorage.setItem('promi_murs',JSON.stringify({n:2,t:Date.now(),der:1,decouvert:1}))"); pg.touchscreen.tap(*c); pg.wait_for_timeout(1100); cap('mur')
    pg.evaluate("()=>{window._murBaisse&&_murBaisse(); closeAll(); document.getElementById('createBtn').click();}"); pg.wait_for_timeout(900)
    for k in range(3): pg.evaluate("()=>{const t=document.querySelectorAll('#createSheet .tile')[0]; if(t) t.click();}"); pg.wait_for_timeout(500)
    pg.wait_for_timeout(1800); cap('plus')
    W,H=1170,2532; P=Image.new('RGB',(4*W+5*60,H+120),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f),(60+i*(W+60),60))
    P.save('planche-v134/bleu.png'); P.resize((1290,int(P.height*1290/P.width))).save('planche-v134/bleu-tel.png'); b.close()
