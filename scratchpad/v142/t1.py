import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b); pg=ouvre(ctx,F)
    print('dev',dev(pg),'promises',pg.evaluate("()=>promises.length"),'webdriver',pg.evaluate("()=>navigator.webdriver"), pg.erreurs)
    capture(pg,'scratchpad/v142/t1-accueil.png')
    pg.evaluate("()=>{try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle')}"); pg.wait_for_timeout(1500)
    T=['boire un verre','appeler Mamie','courir dimanche','ranger le garage','écrire à Paul','lire un livre','arroser','dormir tôt','cuisiner']
    for i,t in enumerate(T):
        plante(pg,t); pg.wait_for_timeout(2500)
        if i+1 in (1,2,3,4,6,9): capture(pg,'scratchpad/v142/t1-rit-%d.png'%(i+1)); print(i+1, pg.evaluate("()=>promises.length"))
    b.close()
