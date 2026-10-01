import sys, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
M=sys.argv[1]; DEP='--depart' in sys.argv
JS=r"""async (a)=>{ Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,3000)); const cv=document.getElementById('toileCv');
 const u0=cv.toDataURL(); if(a.dep){ const ids=promises.filter(p=>!p.draft).map(p=>p.id); Toile.sync(ids.slice(1)); } else Toile.addPromi(null);
 await new Promise(r=>requestAnimationFrame(r)); await new Promise(r=>requestAnimationFrame(r)); return [u0, cv.toDataURL()]; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    u=pg.evaluate(JS,{'m':M,'dep':DEP}); b.close()
a,bb=[Image.open(io.BytesIO(base64.b64decode(x.split(',')[1]))).convert('RGB') for x in u]
d=ImageChops.difference(a,bb).convert('L').point(lambda v:255 if v>20 else 0)
w,h=a.size; s=Image.new('RGB',(w*3//2,h//2),'white'); s.paste(a.resize((w//2,h//2)),(0,0)); s.paste(bb.resize((w//2,h//2)),(w//2,0)); s.paste(d.convert('RGB').resize((w//2,h//2)),(w,0)); s.save('premiere_%s.png'%M)
