import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image
F='app.html'; pre=sys.argv[1] if len(sys.argv)>1 else 'window._semisNeufToujours=true'; nom=sys.argv[2] if len(sys.argv)>2 else 't2'; monde=sys.argv[3] if len(sys.argv)>3 else 'ritournelle'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b); ctx.add_init_script(pre); pg=ouvre(ctx,F)
    pg.evaluate("(m)=>{try{setPremium(true)}catch(e){} Toile.setTheme(m)}",monde); pg.wait_for_timeout(1500)
    T=['boire un verre','appeler Mamie','courir dimanche','ranger le garage','écrire à Paul','lire un livre','arroser','dormir tôt','cuisiner']
    L=[]
    for i,t in enumerate(T):
        plante(pg,t); pg.wait_for_timeout(2500)
        if i+1 in (1,2,3,4,6,9): L.append(image(pg))
    W=Image.new('RGB',(400*6,844),'white')
    for i,im in enumerate(L): W.paste(im,(i*400,0))
    W.save('scratchpad/v142/%s.png'%nom); print(pg.erreurs)
    b.close()
