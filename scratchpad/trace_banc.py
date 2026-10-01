import sys; sys.argv=['banc_rendu.py']
import importlib.util
spec=importlib.util.spec_from_file_location('b','banc_rendu.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
from playwright.sync_api import sync_playwright
PIEGE="""(()=>{ window.__tr=[]; const arme=()=>{ if(!window.Toile||!Toile.sync||Toile.__p) return setTimeout(arme,5); Toile.__p=1;
    for(const f of ['sync','addPromi','setTheme','addNuee','addMember','reGray','setPalette','setHue']){ const o=Toile[f]; Toile[f]=function(){ window.__tr.push([window.__vt!=null?'V':'R',f,JSON.stringify([...arguments]).slice(0,40),(new Error().stack||'').split('\\n').slice(1,3).join(' < ').slice(0,160)]); return o.apply(this,arguments); }; } }; arme(); })();"""
with sync_playwright() as p:
    for run in range(2):
        br=p.webkit.launch(); ctx=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script(b.AMORCE); ctx.add_init_script(PIEGE)
        pg=ctx.new_page(); pg.goto(b.URL); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} window.__tr=[]; }")
        pg.evaluate(b.PILOTE)
        neufs=pg.evaluate("()=>{ const r=[]; for(const m of ['brouillamini']){ Toile.setTheme(m); if(Toile.semisNeuf()) r.push(m); } return r; }")
        for essai in range(2):
            pg.evaluate(b.POSE,['brouillamini',b.GRAINE,neufs])
            for _ in range(6): pg.evaluate("()=>window.__images(40)"); pg.wait_for_timeout(120)
        tr=pg.evaluate("()=>window.__tr"); print('RUN',run,'neufs',neufs); [print('  ',x) for x in tr]
        br.close()
