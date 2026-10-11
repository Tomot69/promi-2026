import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
import importlib.util, io
src=io.open('redteam_ritournelle.py',encoding='utf-8').read().split("TITRES = [")[0].split("res = []")[1]
Y0,Y1=102,708
exec("res=[]"+src)
from PIL import Image
T=['boire un verre','appeler Mamie','courir dimanche','ranger le garage','écrire à Paul','lire un livre','faire les crêpes','planter un arbre','réparer le vélo']
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx,F)
    pg.evaluate("()=>{try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle')}"); pg.wait_for_timeout(1500)
    for i,t in enumerate(T):
        B.plante(pg,t); pg.wait_for_timeout(3200); n=i+1
        if n in (1,2,3,4,6,9):
            pg.reload(); pg.wait_for_timeout(7500)
            im=B.image(pg); TT=taches(im); D=[t for t in TT if t[2]]; V=[t for t in TT if not t[2]]
            ent=[t for t in V if t[0][0]>1 and t[0][1]<388 and t[0][2]>Y0 and t[0][3]<Y1-2]
            if D:
                x0=min(t[0][0] for t in D); x1=max(t[0][1] for t in D); y0=min(t[0][2] for t in D); y1=max(t[0][3] for t in D)
                print(n,'dalles',len(D),'union %d×%d (%.0f %% de la largeur) centre (%.0f, %.0f)'%(x1-x0,y1-y0,(x1-x0)/3.9,(x0+x1)/2,(y0+y1)/2),'· vides',len(V),'dont entières',len(ent), [t[0] for t in D][:4], flush=True)
            B.capture(pg,'planche-v143/rit-%s-%d.png'%(F.replace('.html',''),n))
    b.close()
