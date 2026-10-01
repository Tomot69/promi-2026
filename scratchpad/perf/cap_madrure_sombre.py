# Madrure : la Toile (accueil) et l'aperçu du Studio, ouvert trois fois ; version donnée en argument.
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
APP=sys.argv[1]; TAG=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme('madrure');}"); pg.wait_for_timeout(3500)
    r=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
    clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}
    pg.screenshot(path='scratchpad/perf/_a.png',clip=clip); ims.append(Image.open('scratchpad/perf/_a.png').convert('RGB'))
    for k in range(3):
        pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ const d=[...document.querySelectorAll('#studioBody .st3-dot')]; d[6]&&d[6].click(); }"); pg.wait_for_timeout(3500)
        pg.screenshot(path='scratchpad/perf/_a.png',clip=clip); ims.append(Image.open('scratchpad/perf/_a.png').convert('RGB'))
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(900)
    W,H=ims[0].size; out=Image.new('RGB',(W*len(ims),H))
    for i,im in enumerate(ims): out.paste(im,(i*W,0))
    out.resize((W*len(ims)//2,H//2)).save('scratchpad/perf/madrure_%s.png'%TAG); b.close()
