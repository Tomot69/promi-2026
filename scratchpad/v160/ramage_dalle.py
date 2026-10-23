import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, 'app.html')
    r = pg.evaluate("""()=>{ try{ setPremium(true); }catch(e){} const pr=promises.filter(p=>!p.draft && Toile.dalleAbs(p.id)); const id=pr[0].id, M=Toile.mondeCourant(), out=[];
      for(const m of ['ramage','guingois','mascaret','chantourne','encre']) for(const s of [64,32,16,64]){ const t=performance.now(); const c=window._rendDalle(id, s, s, {monde:{m:m,p:M.p,h:M.h}}); out.push(m+' '+s+' : '+(performance.now()-t).toFixed(0)+' ms'+(c?'':' (rien)')); }
      return out; }""")
    print('\n'.join(r)); b.close()
