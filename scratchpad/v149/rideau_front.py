# C-156 : image par image après le lever, la matière amande (ruban + rideau) sur trois colonnes : son haut et son front bas. Un seul mouvement :
# le front ne remonte jamais et ne s'arrête pas ; le haut redescend sur le trait. WebKit, banc_tom.
import sys, os, json; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
print('charge', os.popen('sysctl -n vm.loadavg').read().strip())
SUIT = r"""()=>{ window.__R=[]; const D=()=>document.getElementById('device').getBoundingClientRect();
  document.addEventListener('touchend',()=>{ window.__lev=performance.now(); },{capture:true});
  function lit(cv, X){ if(!cv) return null; const r=cv.getBoundingClientRect(), d=D(), k=d.width/390, s=cv.width/(r.width/k), top=(r.top-d.top)/k; const g=cv.getContext('2d'); const out=[];
    for(const x of X){ const col=g.getImageData(Math.round(x*s),0,1,cv.height).data; let a0=-1,a1=-1; for(let j=0;j<cv.height;j++){ const a=col[j*4+3], gg=col[j*4+1]; if(a>128 && gg>180){ if(a0<0) a0=j; a1=j; } } out.push(a0<0?null:[+(top+a0/s).toFixed(1), +(top+a1/s).toFixed(1)]); } return out; }
  (function f(){ if(window.__lev){ const t=performance.now()-window.__lev; if(t<1100){ window.__R.push([Math.round(t), lit(document.getElementById('tenirRuban'),[60,195,330]), lit(document.getElementById('tenirMaree'),[60,195,330])]); } } requestAnimationFrame(f); })(); }"""
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = contexte(b); pg = ouvre(ctx, F)
    plante(pg, 'rendre le livre'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3000)
    pg.evaluate(SUIT)
    z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(1500)
    R = pg.evaluate("()=>window.__R")
    for t, rb, mr in R[:40]:
        def u(rb, mr, i):
            a = rb[i] if rb else None; m = mr[i] if mr else None
            haut = min([v[0] for v in (a, m) if v] or [None]) if (a or m) else None
            bas = max([v[1] for v in (a, m) if v] or [None]) if (a or m) else None
            return '%s→%s' % (haut, bas)
        print('%+5d  ' % t + '   '.join(u(rb, mr, i) for i in range(3)), ' [ruban]' if rb else '', ' [rideau]' if mr else '')
    b.close()
