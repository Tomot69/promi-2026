import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
MONDES = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mondes=')), 'ramage,mascaret,chantourne,guingois').split(',')
ESPION = """()=>{ window.__on=false; window.__A=[]; const T=Toile, ap=T.apercuImage; const P=CanvasRenderingContext2D.prototype;
  window.__op={fill:0,stroke:0,drawImage:0,autre:0,n:0}; let dans=false;
  ['fill','stroke','drawImage','putImageData','getImageData'].forEach(n=>{ const f=P[n]; P[n]=function(){ if(!dans||!window.__on) return f.apply(this,arguments); const t=performance.now(); const r=f.apply(this,arguments); const k=(n in window.__op)?n:'autre'; window.__op[k]+=performance.now()-t; window.__op.n++; return r; }; });
  T.apercuImage=function(){ const t=performance.now(); dans=true; let r; try{ r=ap.apply(this,arguments); } finally{ dans=false; } if(window.__on) window.__A.push(performance.now()-t); return r; };
  window.__D=[]; let av=performance.now(); (function f(t){ if(window.__on) window.__D.push(t-av); av=t; requestAnimationFrame(f); })(performance.now()); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25)
    if '--temoin' in sys.argv: ctx.add_init_script("Object.defineProperty(window,'_apDoigt',{get:function(){return false},set:function(){},configurable:true});")
    pg = B.ouvre(ctx, F); print('TÉMOIN (avant)' if '--temoin' in sys.argv else 'NOUVEAU', 'listeners:', pg.evaluate("()=>!!document.getElementById('studioScreen')"))
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200); pg.evaluate(ESPION); vus = []
    for i in range(22):
        m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m in vus: break
        vus.append(m)
        if m in MONDES:
            pg.wait_for_timeout(4000)
            x, y = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.getElementById('st3thumb'); const r=e.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }")
            ch = B.charge()
            pg.evaluate("()=>{ window.__A=[]; window.__D=[]; for(const k in window.__op) window.__op[k]=0; window.__on=true; }"); pg.wait_for_timeout(1500)
            R0 = pg.evaluate("()=>{ window.__on=false; return {A:window.__A, D:window.__D, op:window.__op}; }"); A0=sorted(R0['A']); D0=sorted(R0['D'])
            if False: print('%-11s AU REPOS · apercuImage n=%d p50 %.1f max %.1f · images p50 %.1f max %.1f' % (m, len(A0), A0[len(A0)//2] if A0 else 0, A0[-1] if A0 else 0, D0[len(D0)//2] if D0 else 0, D0[-1] if D0 else 0), flush=True)
            pg.evaluate("()=>{ window.__A=[]; window.__D=[]; for(const k in window.__op) window.__op[k]=0; window.__on=true; }")
            B.glisse(pg, [[x + 100 * t / 40, y] for t in range(41)] + [[x + 100 - 200 * t / 60, y] for t in range(61)], pas=6); pg.wait_for_timeout(300)
            R = pg.evaluate("()=>{ window.__on=false; return {A:window.__A, D:window.__D, op:window.__op}; }")
            A = sorted(R['A']); D = sorted(R['D'])
            q = lambda L, f: L[int(f * (len(L) - 1))] if L else 0
            print('%-11s charge %.1f · apercuImage n=%d p50 %.1f p95 %.1f max %.1f ms · images p50 %.1f p95 %.1f max %.1f · >34 ms : %d · ops %s' % (m, ch, len(A), q(A, .5), q(A, .95), q(A, 1), q(D, .5), q(D, .95), q(D, 1), sum(1 for v in D if v > 34), {k: round(v, 1) for k, v in R['op'].items()}), flush=True)
        B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(1400)
    b.close()
