# « garder de côté » : sa boîte et son encre, contre le bord droit de l'écran et le haut de la barre du bas (Peaufiner) — trois pages +, deux thèmes
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch()
    for s in (False, True):
        ctx=B.contexte(b, sombre=s); pg=B.ouvre(ctx, F)
        for k in ('promi','chiche','nuee'):
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(400)
            B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=%s]'%k); pg.wait_for_timeout(3000)
            print('sombre' if s else 'clair ', k, pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), K=D.width/390;
              const g=document.querySelector('#createSheet .pp-garder'), bb=document.getElementById('csBotBar'), rl=document.getElementById('csPinceau');
              const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [+((r.left-D.left)/K).toFixed(1), +((r.top-D.top)/K).toFixed(1), +((r.right-D.left)/K).toFixed(1), +((r.bottom-D.top)/K).toFixed(1)]; };
              const rg=document.createRange(); rg.selectNodeContents(g); const ri=rg.getBoundingClientRect();
              return {garder:R(g), encre:[+((ri.left-D.left)/K).toFixed(1), +((ri.top-D.top)/K).toFixed(1), +((ri.right-D.left)/K).toFixed(1), +((ri.bottom-D.top)/K).toFixed(1)], barre:R(bb), rail:R(rl)}; }"""))
        ctx.close()
    b.close()
