# qui écrit le `top` du mot du trait de la page + ? (WebKit ; jusqu'à une ouverture à 4 lignes)
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
PIEGE = r"""(function(){ var o=CSSStyleDeclaration.prototype.setProperty; window.__W=[];
  CSSStyleDeclaration.prototype.setProperty=function(n,v,p){ try{ if(n==='top' && this.__mot){ window.__W.push([Math.round(performance.now()), v, (new Error().stack||'').split('\n').slice(1,4).map(s=>s.replace(/https?:\/\/[^ ]*\//,'').slice(0,90)).join(' | ')]); } }catch(e){} return o.call(this,n,v,p); };
  var mo=new MutationObserver(function(){ var t=document.querySelector('#createSheet .pp-trace'); if(t && !t.style.__mot){ t.style.__mot=1; } }); document.addEventListener('DOMContentLoaded',function(){ mo.observe(document.body,{childList:true,subtree:true}); }); })();"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for essai in range(8):
        ctx=B.contexte(b); ctx.add_init_script(PIEGE); pg=B.ouvre(ctx)
        B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=chiche]'); pg.wait_for_timeout(3500)
        r=pg.evaluate("()=>{ const e=_ppEcran(), tr=document.querySelector('#createSheet .pp-trace'); return [e.nl, e.base, tr.style.top]; }")
        if r[0]==4:
            print(r); [print('  ', w) for w in pg.evaluate("()=>window.__W")[-14:]]; ctx.close(); break
        ctx.close()
    b.close()
