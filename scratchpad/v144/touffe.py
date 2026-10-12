import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F=sys.argv[1]
ESP="""(function(){ window.__C=[]; var ce=document.createElement.bind(document); document.createElement=function(t){ var e=ce.apply(document,arguments); if((''+t).toLowerCase()==='canvas') window.__C.push(['canvas',Math.round(performance.now()),(new Error().stack||'').split('\\n').slice(2,4).map(s=>s.trim().slice(0,60)).join(' < ')]); return e; };
  var P=CanvasRenderingContext2D.prototype; ['fill','stroke','drawImage','fillRect'].forEach(function(n){ var f=P[n]; P[n]=function(){ window.__N=(window.__N||0)+1; return f.apply(this,arguments); }; });
  (function b(){ (window.__NF=window.__NF||[]).push([Math.round(performance.now()), window.__N||0]); window.__N=0; if(window.__NF.length>3000) window.__NF.shift(); requestAnimationFrame(b); })(); })();"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); ctx.add_init_script(ESP); pg=B.ouvre(ctx,F); pg.evaluate("()=>Toile.setTheme('touffe')"); pg.wait_for_timeout(1200)
    for t in ['rendre le livre','écrire à Lou','arroser le ficus','courir dimanche']: B.plante(pg,t)
    pg.wait_for_timeout(3500); pg.evaluate("()=>{ window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ window.__C.length=0; window.__t0=performance.now(); }"); B.tap_sel(pg,'.v16-oui'); pg.wait_for_timeout(2500)
    r=pg.evaluate("()=>({t0:window.__t0,C:window.__C,NF:window.__NF})"); t0=r['t0']
    NF=[(a-t0,n) for a,n in r['NF'] if 0<=a-t0<=2000]; gros=[(round(a),n,round(NF[i+1][0]-a) if i+1<len(NF) else 0) for i,(a,n) in enumerate(NF) if n>3000 or (i+1<len(NF) and NF[i+1][0]-a>40)]
    print(F,'· canevas créés :',[(c[1]-round(t0),c[2]) for c in r['C']][:8]); print('   images lourdes (instant, tracés, durée) :',gros[:14]); print('   tracés par image, médiane :',sorted(n for _,n in NF)[len(NF)//2])
    b.close()
