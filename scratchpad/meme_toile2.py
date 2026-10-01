import sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
COMP="""()=>{ const r={}; promises.forEach(p=>{ const d=Toile.dalleAbs(p.id); if(d) r[p.title+'|'+p.who]=[Math.round(d.minx),Math.round(d.miny),Math.round(d.w),Math.round(d.h)]; }); return r; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); res=[]
    for i in range(2):
        ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(8000); R=[]
        for k in range(4): pg.reload(); pg.wait_for_timeout(8000); R.append(pg.evaluate(COMP))
        d=[sum(1 for t in R[0] if R[0][t]!=R[j].get(t)) for j in range(1,4)]
        print('contexte',i+1,': réouvertures 2,3,4 contre la 1re — dalles différentes',d,'sur',len(R[0])); res.append(R[-1]); ctx.close()
    b.close()
