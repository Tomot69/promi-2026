import sys,io
from playwright.sync_api import sync_playwright
from PIL import Image
pal=sys.argv[1] if len(sys.argv)>1 else 'signal'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,reduced_motion='reduce'); ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_pelote_palier','0')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("([t,p])=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); try{Toile.setPalette(p)}catch(e){} closeAll(); document.getElementById('souffleBtn').click();}",[th,pal]); pg.wait_for_timeout(2000)
        for _ in range(30):
            pg.evaluate("()=>{try{_aura.fige(true);_aura.vue(0.6,0.35);_aura.pelote()}catch(e){}}"); pg.wait_for_timeout(1200)
            if pg.evaluate("()=>{const c=document.getElementById('auBoule'); const d=c.getContext('2d').getImageData(c.width>>1,c.height>>1,1,1).data; return d[3]>250}"): break
        pg.wait_for_timeout(1500); print(th, pg.evaluate("()=>JSON.stringify([_aura.corps(), _aura.etat().palier])"))
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')); ctx.close()
    W,H=ims[0].size; o=Image.new('RGB',(2*W,H)); o.paste(ims[0],(0,0)); o.paste(ims[1],(W,0)); o.save('scratchpad/v123/vue-%s.png'%pal); o.crop((0,250,2*W,1300)).save('scratchpad/v123/vue-%s-c.png'%pal)
    b.close()
