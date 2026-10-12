import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
OU = open('redteam_deplace.py', encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx); B.plante(pg,'rendre le livre'); pg.wait_for_timeout(1500)
    G=pg.evaluate(OU); g=list(G.values())[0]; B.tap(pg,g[0],g[1]); pg.wait_for_timeout(1200)
    print(pg.evaluate("()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [700,740,770,790,810,830].map(y=>{ const e=document.elementFromPoint(d.left+150*k,d.top+y*k); return y+':'+(e&&(e.id||e.className)); }) }"))
    for y in (790,):
        B.tap(pg,150,y); pg.wait_for_timeout(900); print(y, pg.evaluate("()=>document.getElementById('detailPoster').className"))
    b.close()
