from playwright.sync_api import sync_playwright
import sys
ON = len(sys.argv)>1
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script(("window._ramFilmOn=true;" if ON else "")+"try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(6000)
    print(pg.evaluate("()=>[Toile.getTheme(), Toile.count&&Toile.count(), document.getElementById('toileCv').width]"))
    pg.screenshot(path='scratchpad/v127/ram-0.png', clip={'x':20,'y':44,'width':390,'height':844})
    pg.evaluate("()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'essai v127',nuee:null})); Toile.addPromi(97001); }")
    for i,t in enumerate((60,200,400,800,1500,3000)):
        pg.wait_for_timeout(t if i==0 else t-(60,200,400,800,1500,3000)[i-1]); pg.screenshot(path='scratchpad/v127/ram-%d.png'%(i+1), clip={'x':20,'y':44,'width':390,'height':844})
    b.close()
from PIL import Image, ImageChops
ims=[Image.open('scratchpad/v127/ram-%d.png'%i).convert('RGB') for i in range(7)]
for i in range(1,7):
    d=ImageChops.difference(ims[i-1],ims[i]).convert('L').point(lambda v:255 if v>12 else 0); bb=d.getbbox(); n=sum(1 for v in d.getdata() if v)
    print(i, round(100*n/(d.width*d.height),1), bb)
Q=Image.new('RGB',(390*4,844)); [Q.paste(ims[k].resize((390,844)),(390*j,0)) for j,k in enumerate((0,1,3,6))]; Q.save('scratchpad/v127/ram-quad%s.png'%('-on' if ON else ''))
