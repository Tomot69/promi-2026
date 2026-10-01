import sys; sys.argv=['banc_rendu.py']
import importlib.util
spec=importlib.util.spec_from_file_location('b','banc_rendu.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
from playwright.sync_api import sync_playwright
SIG="""()=>{ const cv=document.createElement('canvas'); Toile.renderTo(cv,1,false); const c=window._renduComp; return c.graines.map(s=>[s.pid,Math.round(s.x*100)/100,Math.round(s.y*100)/100]); }"""
POSE_SIG="""(a)=>{ const [monde,graine,neufs]=a; const autre = neufs.indexOf(monde)>=0 ? 'encre' : 'esquille';
  Toile.setTheme(autre); window.__amorce(graine); Toile.setTheme(monde);
  const cv=document.createElement('canvas'); Toile.renderTo(cv,1,false); return window._renduComp.graines.map(s=>[s.pid,Math.round(s.x*100)/100,Math.round(s.y*100)/100]); }"""
with sync_playwright() as p:
    R=[]
    for run in range(2):
        br=p.webkit.launch(); ctx=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script(b.AMORCE); pg=ctx.new_page(); pg.goto(b.URL); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} }"); pg.evaluate(b.PILOTE)
        a=pg.evaluate(POSE_SIG,['ramage',b.GRAINE,['ramage']]); c=pg.evaluate(POSE_SIG,['ramage',b.GRAINE,['ramage']])
        print('run',run,'même page, pose 1 vs pose 2 :', sum(1 for x,y in zip(a,c) if x!=y)); R.append(a); br.close()
    print('entre deux pages :', sum(1 for x,y in zip(R[0],R[1]) if x!=y), R[0][:2], R[1][:2])
