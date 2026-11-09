import sys, io, re; sys.path.insert(0,'.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
S=io.open('redteam_jonction_fiche.py',encoding='utf-8').read()
ETAT=re.search(r'ETAT = """(.*?)"""',S,re.S).group(1); FORME=re.search(r'FORME = """(.*?)"""',S,re.S).group(1)
etat=sys.argv[1]; s=float(sys.argv[2]); xs=[int(x) for x in sys.argv[3].split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,'cercle'); ctx.add_init_script(BJ.AMORCE); pg=B.ouvre(ctx,'app.html',6000)
    pid=pg.evaluate(ETAT,['faire les crêpes','promi',etat,BJ.MOTS]); pg.evaluate("id=>{try{closeAll()}catch(e){} openDetail(id)}",pid)
    for _ in range(40): pg.evaluate("()=>window.__horloge(100)"); pg.wait_for_timeout(50)
    pg.evaluate("()=>{document.getElementById('detailPoster').scrollTop=1}"); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    G=pg.evaluate(FORME); print('s0',G['s0'],'mn',G['mn'])
    pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}",s); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
    im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); d=B.dev(pg); dpr=pg.evaluate("()=>devicePixelRatio"); k=d[4]
    for x in xs:
        i=x//2; print('x',x,'P',round(G['P'][i],2),'EN',round(G['EN'][i],2))
        X=int(round((d[0]+x*k)*dpr))
        print([ (round(((Y/dpr)-d[1])/k,2), im.getpixel((X,Y))) for Y in range(int((d[1]+108*k)*dpr), int((d[1]+122*k)*dpr))])
    im.crop((int((d[0]+300*k)*dpr),int((d[1]+95*k)*dpr),int((d[0]+390*k)*dpr),int((d[1]+135*k)*dpr))).resize((90*8,40*8),Image.NEAREST).save('scratchpad/v191/c_dbg.png')
    b.close()
