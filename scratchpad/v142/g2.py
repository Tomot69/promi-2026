import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter, ImageStat
import io as _io
def net(pg):
    im=Image.open(_io.BytesIO(capture(pg))).convert('L').resize((390,844)); e=im.filter(ImageFilter.FIND_EDGES).crop((20,120,370,700)); return round(ImageStat.Stat(e).mean[0],2)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b); pg=ouvre(ctx)
    for t in ['boire un verre','appeler Mamie','courir dimanche']: plante(pg,t)
    pg.wait_for_timeout(1500); print('net au départ', net(pg))
    pg.evaluate("()=>{ _guide.montre('studio'); }"); pg.wait_for_timeout(2600); print('guide v142', net(pg))
    for nom,js in [('sans masque',"f.style.webkitMaskImage='none';f.style.maskImage='none'"),('sans découpe',"f.style.webkitClipPath='none';f.style.clipPath='none'"),('masque remis, sans découpe',"f.style.webkitMaskImage=window.__m;f.style.maskImage=window.__m"),('découpe rect',"f.style.webkitMaskImage='none';f.style.maskImage='none';f.style.clipPath='path(nonzero, \"M0 0H390V844H0Z\")';f.style.webkitClipPath=f.style.clipPath"),('découpe inset',"f.style.clipPath='inset(0 0 300px 0)';f.style.webkitClipPath=f.style.clipPath"),('polygon',"f.style.clipPath='polygon(0 0, 390px 0, 390px 500px, 0 700px)';f.style.webkitClipPath=f.style.clipPath")]:
        pg.evaluate("()=>{ const f=document.getElementById('guideFlou'); if(!window.__m) window.__m=f.style.maskImage||f.style.webkitMaskImage; "+js+"; }"); pg.wait_for_timeout(500); print(nom, net(pg), pg.evaluate("()=>{const f=document.getElementById('guideFlou'), c=getComputedStyle(f); return [c.clipPath.slice(0,40), (c.webkitMaskImage||c.maskImage).slice(0,40), c.backdropFilter||c.webkitBackdropFilter]}"))
    capture(pg,'scratchpad/v142/g2.png'); b.close()
