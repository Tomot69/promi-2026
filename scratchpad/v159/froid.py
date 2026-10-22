import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_toile_stable.py').read().split('res = []')[1].split('with sync_playwright()')[0].replace('def juge','def _j'))
A=sys.argv[1]; Bf=sys.argv[2]; MOND=sys.argv[3].split(','); NS=[int(x) for x in sys.argv[4].split(',')]
mauvais=0
with sync_playwright() as p:
    br=p.webkit.launch()
    for vw,vh in ((390,692),(430,932)):
        for n in NS:
            for m in MOND:
                G=[]
                for F in (A,Bf):
                    ctx=B.contexte(br, vw=vw, vh=vh, stockage={}); B.toile_pleine(ctx,n); ctx.add_init_script("try{ if(!sessionStorage.getItem('__m')){ sessionStorage.setItem('__m','1'); localStorage.setItem('promi_studio', JSON.stringify({m:'%s',p:'signal',h:0,libre:true,acquis:{}})); } }catch(e){}" % m); pg=B.ouvre(ctx,F,attente=7000); pose(pg); G.append(pg.evaluate(GEO)); ctx.close()
                d,k=ecart(G[0],G[1]); mauvais+=k; print(('❌ ' if k else '✅ ')+'%dx%d · %d · %s · %s'%(vw,vh,n,m,d), flush=True)
    br.close()
print('écarts', mauvais)
