import sys, os; sys.path.insert(0,'.')
import banc_tom as B
src=open('redteam_validation.py',encoding='utf-8').read()
exec(src[src.index('ZONE ='):src.index('\n',src.index('ZONE ='))]) if 'ZONE =' in src else None
import re
g={}
for nom in ('FLOUS','TIENT','ZONE','SUIT'):
    m=re.search(r'^%s = (r?""".*?"""|".*?")$'%nom, src, re.S|re.M)
    if m: g[nom]=eval(m.group(1))
FL2=g['FLOUS'].replace("return [e.id||'', c.filter, c.opacity];","return [e.id||(e.tagName+'.'+String(e.className).slice(0,50)), c.filter, c.opacity];")
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx,F)
    B.plante(pg,'rendre le livre'); pid=pg.evaluate("()=>promises[promises.length-1].id")
    pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(700); pg.evaluate("id=>openDetail(id)",pid); pg.wait_for_timeout(2800)
    av=set(pg.evaluate(FL2)); z=pg.evaluate(g['ZONE'],'tenirZone')
    pg.evaluate(g['TIENT'],[[list(B.pt(pg,200+4*i,z[1]+z[3]*0.45)) for i in range(11)]]); pg.wait_for_timeout(700)
    print(F,[x for x in pg.evaluate(FL2) if x not in av])
    b.close()
