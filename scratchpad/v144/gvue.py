# le guide, vu en Chromium (il rend le flou d'arrière-plan) : installation et glissement arrêtés à intervalles réguliers
import sys, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from PIL import Image
import banc_tom as B
sombre='--sombre' in sys.argv
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=B.contexte(b, sombre=sombre); pg=B.ouvre(ctx)
    for t in ['rendre le livre','écrire à Lou','arroser le ficus']: B.plante(pg,t)
    pg.wait_for_timeout(2500); ims=[]
    pg.evaluate("()=>{ _guide.montre('studio'); }"); pg.wait_for_timeout(120)
    for ms in (0,450,900,1350,1800):
        pg.evaluate("ms=>_guide.figeA(ms)",ms); pg.wait_for_timeout(350); ims.append(('installation %d ms'%ms, Image.open(io.BytesIO(B.capture(pg)))))
    for ms in (0,300,600,900,1200):
        pg.evaluate("ms=>_guide.figeGlisse(ms)",ms); pg.wait_for_timeout(350); ims.append(('glissement %d ms'%ms, Image.open(io.BytesIO(B.capture(pg)))))
    print(pg.evaluate("()=>JSON.stringify(_guide.etat())"), pg.erreurs)
    w,h=ims[0][1].size; s=0.5; W=int(w*s); H=int(h*s); P=Image.new('RGB',(W*5+40,H*2+30),(250,250,250))
    for i,(n,im) in enumerate(ims): P.paste(im.resize((W,H)),(10+(i%5)*(W+5),10+(i//5)*(H+10)))
    P.save('scratchpad/v144/gvue-%s.png'%('sombre' if sombre else 'clair')); b.close()
