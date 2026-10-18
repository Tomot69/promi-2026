# « l'instant après » (redteam_couleurs_ref, sombre) : de l'orange #DD4D23 sur un canevas ? v149 contre v150, plusieurs délais
import sys
from playwright.sync_api import sync_playwright
J = """(id)=>{ const out={}; document.querySelectorAll('#detailPoster canvas, #device canvas').forEach((c,i)=>{ if(!c.width||!c.height) return; const r=c.getBoundingClientRect(); if(r.width<10) return; let n=0,t=0; try{ const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; for(let k=0;k<d.length;k+=4*16){ if(d[k+3]<200) continue; t++; if(Math.abs(d[k]-221)<6&&Math.abs(d[k+1]-77)<6&&Math.abs(d[k+2]-35)<6) n++; } }catch(e){ return; } if(n) out[(c.id||c.className||('cv'+i))]=+(100*n/Math.max(1,t)).toFixed(1); }); return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in ('zz-av149.html', 'app.html'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}); ctx.add_init_script("try{localStorage.setItem('promi_theme','dark')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + f); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setTheme('dark')}catch(e){}}")
        pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},900);}}")
        for t in (1500, 3000, 5000):
            pg.wait_for_timeout(t - (0 if t == 1500 else (1500 if t == 3000 else 3000)))
            print(f, t, pg.evaluate("()=>{const p=promises.filter(q=>q.title==='faire les crêpes')[0]; return [p.status, window._instant||null]; }"), pg.evaluate(J))
        ctx.close()
    b.close()
