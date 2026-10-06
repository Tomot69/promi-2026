import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
G=r"""()=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(); const kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height; const out=[];
  for(let y=dv.top+120;y<dv.bottom-140;y+=10) for(let x=dv.left+10;x<dv.right-10;x+=10){ let h=null; try{ h=Toile.hit((x-r.left)*kx,(y-r.top)*ky); }catch(e){} out.push(h&&h.pid!=null?h.pid:0); } return out; }"""
PINCE=r"""([d0,d1])=>new Promise(res=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
  const ev=(t,id,x)=>cv.dispatchEvent(new PointerEvent(t,{pointerId:id,pointerType:'touch',isPrimary:id===11,clientX:x,clientY:cy,bubbles:true,cancelable:true}));
  ev('pointerdown',11,cx-d0/2); ev('pointerdown',12,cx+d0/2); let i=0; (function f(){ i++; const d=d0+(d1-d0)*i/14; ev('pointermove',11,cx-d/2); ev('pointermove',12,cx+d/2); if(i<14) setTimeout(f,16); else { ev('pointerup',11,cx-d/2); ev('pointerup',12,cx+d/2); setTimeout(res,1800); } })(); })"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} }")
    clip={'x':30,'y':170,'width':370,'height':560}
    for m in (sys.argv[1].split(',') if len(sys.argv)>1 else ['encre','ramage','volubilis','guingois','chamade','madrure']):
        pg.evaluate("(m)=>{closeAll(); try{Toile_recadre()}catch(e){} Toile.setTheme(m);}", m); pg.wait_for_timeout(5000)
        a=Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L'); ha=pg.evaluate(G); v0=pg.evaluate("()=>Toile.vue()")
        pg.evaluate(PINCE,[120,230]); c=Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L'); hc=pg.evaluate(G); v1=pg.evaluate("()=>Toile.vue()")
        d=ImageChops.difference(a,c).point(lambda v:255 if v>24 else 0); img=100*sum(1 for v in d.getdata() if v)/(d.size[0]*d.size[1]); hit=100*sum(1 for x,y in zip(ha,hc) if x!=y)/len(ha)
        print('%-11s échelle %.2f → %.2f · l\'IMAGE change sur %4.1f %% · la carte du toucher change sur %4.1f %%'%(m, v0['s'], v1['s'], img, hit), flush=True)
    b.close()
