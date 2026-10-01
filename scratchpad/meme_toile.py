import sys,json
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
COMP="""()=>{ const r={}; promises.forEach(p=>{ const d=Toile.dalleAbs(p.id); if(d) r[p.title+'|'+p.who]=[Math.round(d.minx*10)/10,Math.round(d.miny*10)/10,Math.round(d.w*10)/10,Math.round(d.h*10)/10]; });
  return {g:Toile.graines(), d:r}; }"""
out=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for i in range(3):
        ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(9000)
        a=pg.evaluate(COMP)
        pg.reload(); pg.wait_for_timeout(9000)   # la même personne rouvre l'app (état gardé)
        c=pg.evaluate(COMP)
        out.append((a,c)); ctx.close()
    b.close()
def diff(x,y): return [k for k in x['d'] if x['d'].get(k)!=y['d'].get(k)]
print('graines', [o[0]['g'] for o in out])
print('ouverture 1 vs 2 vs 3 (neuves) : dalles différentes', len(diff(out[0][0],out[1][0])), len(diff(out[0][0],out[2][0])), 'sur', len(out[0][0]['d']))
print('réouverture (même personne) : dalles différentes', [len(diff(o[0],o[1])) for o in out])
