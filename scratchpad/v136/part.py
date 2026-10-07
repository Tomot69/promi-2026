from playwright.sync_api import sync_playwright
from PIL import Image
import sys
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light'); setPremium(true); closeAll(); openDetail(128);}"); pg.wait_for_timeout(2500)
    def partage(n):
        c=pg.evaluate("()=>{const e=[...document.querySelectorAll('#detailPoster #dpDetails [class*=part], #detailPoster .dpd-share, #detailPoster .dpd-part')].filter(x=>x.getBoundingClientRect().width>0)[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2, e.className]}")
        print('rond', c)
        pg.mouse.click(20+343,44+802); pg.wait_for_timeout(2800)
        print(n, pg.evaluate("()=>{const s=document.getElementById('shareScreen'); return [s.classList.contains('show'), [...s.querySelectorAll('canvas')].filter(c=>c.getBoundingClientRect().width>60).map(c=>[c.id,c.width,c.height]), (document.getElementById('shMode')||{}).textContent]}"))
        f='scratchpad/v136/part-%s.png'%n; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)
    partage('dalle')
    # une photo
    pg.evaluate("()=>{ const c=document.createElement('canvas'); c.width=300; c.height=400; const g=c.getContext('2d'); g.fillStyle='#c33'; g.fillRect(0,0,300,400); g.fillStyle='#fff'; g.fillRect(60,80,180,240); const p=promises.find(q=>q.id===128); p.photo=c.toDataURL('image/png'); closeAll(); openDetail(128); }"); pg.wait_for_timeout(2500); partage('photo')
    pg.evaluate("()=>{ const p=promises.find(q=>q.id===128); delete p.photo; closeAll(); openDetail(128); }"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>window._dessin.ouvre()"); pg.wait_for_timeout(400)
    pg.mouse.move(120,300); pg.mouse.down(); [pg.mouse.move(120+i*9,300+(i%6)*11) for i in range(22)]; pg.mouse.up(); pg.wait_for_timeout(200)
    pg.evaluate("()=>document.querySelector('#dessinMode [data-outil=poser]').click()"); pg.wait_for_timeout(1200); partage('dessin')
    P=Image.new('RGB',(3*400,844),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f).resize((390,844)),(i*400,0))
    P.save('scratchpad/v136/part.png'); b.close()
