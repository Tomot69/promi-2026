import sys,io
from playwright.sync_api import sync_playwright
from PIL import Image
out=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for f in sys.argv[1:]:
        for th in ('light','dark'):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,reduced_motion='reduce')
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
            pg.evaluate("t=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} var d=document.getElementById('device'); if(d.classList.contains('light')!==(t==='light')){ try{ setLight(t==='light'); }catch(e){ d.classList.toggle('light',t==='light'); } } document.getElementById('souffleBtn').click(); }",th)
            pg.wait_for_timeout(3800); pg.evaluate("()=>{ try{ _aura.fige(true); }catch(e){} }"); pg.wait_for_timeout(350)
            im=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
            n=f.replace('.html','')+'-'+th; im.save('planche-v137/aura-%s.png'%n)
            # recadrage à 100 % : le bord gauche bas de la Pelote
            im.crop((int(60*3),int(250*3),int(60*3)+600,int(250*3)+600)).save('planche-v137/bord-%s.png'%n)
            ctx.close()
    b.close()
