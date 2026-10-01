import sys; sys.argv=['banc_rendu.py']
import importlib.util, hashlib, json
spec=importlib.util.spec_from_file_location('b','banc_rendu.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
from playwright.sync_api import sync_playwright
SIG="""()=>{ const cv=document.createElement('canvas'); Toile.renderTo(cv,1,false); const c=window._renduComp; return {cle:Toile.cle(), g:c.graines.map(s=>[s.pid,Math.round(s.x*100)/100,Math.round(s.y*100)/100,Math.round(s.w*100)/100])}; }"""
with sync_playwright() as p:
    R=[]
    for run in range(2):
        br=p.webkit.launch(); ctx=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script(b.AMORCE); pg=ctx.new_page(); pg.goto(b.URL); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} }"); pg.evaluate(b.PILOTE)
        pg.evaluate("()=>{ Toile.setTheme('ramage'); }")
        pg.evaluate(b.POSE,['ramage',b.GRAINE,['ramage']]); s0=pg.evaluate(SIG)
        for _ in range(6): pg.evaluate("()=>window.__images(40)"); pg.wait_for_timeout(120)
        s1=pg.evaluate(SIG); R.append((s0,s1)); br.close()
    for i,n in ((0,'juste après la pose'),(1,'après 240 images')):
        a,c=R[0][i],R[1][i]; d=[(x,y) for x,y in zip(a['g'],c['g']) if x!=y]
        print(n,'clé',a['cle'],c['cle'],'graines',len(a['g']),'différentes',len(d), d[:3])
