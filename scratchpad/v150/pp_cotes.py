# les cotes des pages + (Promi, Chiche, Cercle), clair : la phrase (boîte et encre), le mot du trait, le rail du pinceau, « garder de côté ». WebKit.
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
LIT = r"""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const cs=document.getElementById('createSheet');
  const bx=e=>{ if(!e) return null; const s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden') return null; const r=e.getBoundingClientRect(); if(!r.width) return null; return [+((r.left-D.left)/k).toFixed(1), +((r.top-D.top)/k).toFixed(1), +((r.right-D.left)/k).toFixed(1), +((r.bottom-D.top)/k).toFixed(1)]; };
  const ink=e=>{ if(!e) return null; const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); if(!r.width) return null; return [+((r.left-D.left)/k).toFixed(1), +((r.top-D.top)/k).toFixed(1), +((r.right-D.left)/k).toFixed(1), +((r.bottom-D.top)/k).toFixed(1)]; };
  const ph=[...cs.querySelectorAll('#csPhrase, #nueePhrase')].find(e=>getComputedStyle(e).display!=='none' && e.getBoundingClientRect().height>0);
  const tx=ph&&ph.querySelector('.ph-txt');
  return {nat:cs.className.match(/pp-(promi|chiche|nuee)/)&&cs.className.match(/pp-(promi|chiche|nuee)/)[1], phrase:ph?ph.id:null, boite:bx(ph), encre:ink(tx), texte:tx?tx.textContent.replace(/\s+/g,' ').slice(0,80):null,
    trace:bx(cs.querySelector('.pp-trace')), traceTxt:(cs.querySelector('.pp-trace')||{}).textContent, rail:bx(document.getElementById('csPinceau')), garder:bx(cs.querySelector('.pp-garder')), fs:tx?getComputedStyle(tx.querySelector('.ph-l,.ph-m,span')||tx).fontSize:null}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); out = {}
    for nat in ('promi', 'chiche', 'nuee'):
        ctx = B.contexte(b); pg = B.ouvre(ctx, F)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
        r = pg.evaluate(LIT); out[nat] = r; print(json.dumps(r, ensure_ascii=False)); ctx.close()
    b.close()
    if len(sys.argv) > 2: json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False)
