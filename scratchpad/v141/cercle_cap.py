import sys
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; out=sys.argv[2]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')})}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    cles=pg.evaluate("()=>Object.keys(NUE).filter(k=>k!=='soi').map(k=>[k,promises.filter(p=>p.nuee===k).length])"); print(cles)
    ims=[]
    def cap():
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='/tmp/c.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append(Image.open('/tmp/c.png').convert('RGB').resize((390,844)))
    for cle in [c[0] for c in sorted(cles,key=lambda c:c[1])][:1]+[c[0] for c in sorted(cles,key=lambda c:-c[1])][:1]:
        pg.evaluate("(k)=>{closeAll();openEssaim(k);}",cle); pg.wait_for_timeout(3000); cap()
        print(cle, pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(); const B=s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)]}; return {add:B('#nfAdd'), peauf:B('#dpDetails'), fil:B('#nueeFil')||B('.nf-liste'), tog:B('#dpDetails .dpd-tog')};}"))
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1800); cap()
        pg.evaluate("()=>{const e=document.getElementById('nqDissolve'); if(e) e.scrollIntoView({block:'end'});}"); pg.wait_for_timeout(700); cap()
    P=Image.new('RGB',(len(ims)*400,844),'white')
    for i,im in enumerate(ims): P.paste(im,(i*400,0))
    P.save(out); b.close()
