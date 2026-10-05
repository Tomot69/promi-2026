# pour chaque monde : le fil d'un Cercle et une carte d'Index — la dalle seule est-elle une vraie dalle ?
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
M='encre touffe brouillamini halin esquille mosaique braille pixel ramage guingois chantourne volubilis madrure chamade ritournelle bobinette mascaret terrazzo gravure sillons'.split()
if len(sys.argv)>1: M=sys.argv[1].split(',')
F=sys.argv[2] if len(sys.argv)>2 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','dark')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:120])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ims=[]
    for m in M:
        pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m);}", m); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(3200)
        a=pg.screenshot(clip={'x':20,'y':44+60,'width':390,'height':700}); open('scratchpad/v130/md-%s.png'%m,'wb').write(a)
        ims.append(Image.open('scratchpad/v130/md-%s.png'%m).resize((195,350)))
    b.close()
n=len(ims); cols=10; rows=(n+cols-1)//cols
Q=Image.new('RGB',(195*cols,350*rows)); [Q.paste(a,(195*(i%cols),350*(i//cols))) for i,a in enumerate(ims)]; Q.save('scratchpad/v130/mondes.png'); print(' '.join(M))
