from playwright.sync_api import sync_playwright
from PIL import Image
import sys
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
URL=sys.argv[1] if len(sys.argv)>1 else 'app.html'; TAG=sys.argv[2] if len(sys.argv)>2 else 'ap'
OUV=[('promi',"openDetail(promises.filter(q=>q.title==='nager le mardi')[0].id)"),('chiche',"openDetail(promises.filter(q=>q.chiche&&!q.done&&!q.draft)[0].id)"),('cercle',"openEssaim('potager')")]
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+URL); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light'); setPremium(true)}"); pg.wait_for_timeout(500)
    for nom,js in OUV:
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(400); pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(2600)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1800)
        info=pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect();
          const pt=(x,y)=>{ let e=document.elementFromPoint(D.left+x,D.top+y); while(e&&e!==document.body){ const c=getComputedStyle(e).backgroundColor; if(c!=='rgba(0, 0, 0, 0)') return (e.id||e.className.toString().slice(0,30))+' '+c; e=e.parentElement;} };
          const t=(x,y)=>{ const e=document.elementFromPoint(D.left+x,D.top+y); return e? (e.id||e.className.toString().slice(0,20))+' '+getComputedStyle(e).color+' b:'+getComputedStyle(e).borderTopColor+' '+getComputedStyle(e).borderTopWidth:null };
          return {f200:pt(385,200), f400:pt(385,400), f600:pt(385,600), f800:pt(385,820), t:[t(60,300),t(60,420),t(60,560)]} }""")
        print(nom, info)
        f=SC+'cl2-%s-%s.png'%(TAG,nom); pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
    P=Image.new('RGB',(400*len(ims),844),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f).resize((390,844)),(i*400,0))
    P.save(SC+'clair2-%s.png'%TAG); b.close()
