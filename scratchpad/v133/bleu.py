from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for n in ('',1,2,3,4,5):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'+('?bleu=%s'%n if n else '')); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); closeAll(); openDetail(promises.filter(q=>q.title==='nager le mardi')[0].id);}"); pg.wait_for_timeout(2600)
        print(n or 'défaut', pg.evaluate("()=>{const r=getComputedStyle(document.documentElement); return [getComputedStyle(document.getElementById('detailPoster')).backgroundColor, r.getPropertyValue('--c-orange-maparole-cobalt'), r.getPropertyValue('--c-lilas85'), (document.getElementById('bleuEtiq')||{}).textContent]}"))
        pg.screenshot(path=SC+'bleu-%s.png'%n, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(SC+'bleu-%s.png'%n); ctx.close()
    P=Image.new('RGB',(200*len(ims),422),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f).resize((195,422)),(i*200,0))
    P.save(SC+'bleus.png'); b.close()
