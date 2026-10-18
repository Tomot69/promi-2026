# C-155 : du lever du doigt à la première image de l'animation — tenir (le rideau) et planter (la page + qui part, la dalle qui arrive). WebKit, banc_tom.
import sys, os, json; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
print('charge', os.popen('sysctl -n vm.loadavg').read().strip())
SUIT = r"""()=>{ window.__ev=[]; const t0=performance.now(); const E=(n)=>window.__ev.push([Math.round(performance.now()-t0), n]);
  document.addEventListener('touchend', ()=>{ window.__lev=performance.now(); E('LEVER'); }, {capture:true});
  const dp=document.getElementById('detailPoster'), cs=document.getElementById('createSheet');
  new MutationObserver(L=>L.forEach(m=>m.addedNodes.forEach(n=>{ if(n.id) E('+'+n.id); }))).observe(dp,{childList:true});
  new MutationObserver(L=>L.forEach(m=>m.addedNodes.forEach(n=>{ if(n.id) E('+'+n.id+' (page+)'); }))).observe(cs,{childList:true});
  let ci=dp.className, cc=cs.className;
  new MutationObserver(()=>{ const n=dp.className; const a=n.split(' ').filter(x=>!ci.split(' ').includes(x)), r=ci.split(' ').filter(x=>!n.split(' ').includes(x)); ci=n; if(a.length||r.length) E('fiche +['+a+'] -['+r+']'); }).observe(dp,{attributes:true,attributeFilter:['class']});
  new MutationObserver(()=>{ const n=cs.className; const a=n.split(' ').filter(x=>!cc.split(' ').includes(x)), r=cc.split(' ').filter(x=>!n.split(' ').includes(x)); cc=n; if(a.length||r.length) E('page+ +['+a+'] -['+r+']'); }).observe(cs,{attributes:true,attributeFilter:['class']});
  const _mr=window._mareeReleve; window._mareeReleve=function(g,cv,t,u){ if(!window.__m1 && u>0.001){ window.__m1=1; E('RIDEAU u>0 (t '+Math.round(t)+')'); } if(!window.__m9 && u>0.99){ window.__m9=1; E('RIDEAU en bas'); } if(_mr) try{_mr.apply(this,arguments);}catch(e){} };
  const bp=document.getElementById('addPromi'); if(bp && bp.onclick && !bp.__m){ const o=bp.onclick; bp.onclick=function(){ const t=performance.now(); const r=o.apply(this,arguments); E('clic addPromi : '+(performance.now()-t).toFixed(1)+' ms'); return r; }; bp.__m=1; }
  const dc=document.getElementById('csTrameCv'); let tr0=''; (function h(){ if(dc){ const s=getComputedStyle(dc); const v=s.transform+'|'+s.filter.slice(0,30); if(v!==tr0){ tr0=v; if(window.__lev) E('dalle : '+v); } } if(performance.now()-t0<9000) requestAnimationFrame(h); })();
  const ad=Toile.addPromi; Toile.addPromi=function(){ E('Toile.addPromi'); return ad.apply(this,arguments); };
  let dern=performance.now(); (function f(){ const n=performance.now(); if(window.__lev && n-dern>24) E('image longue '+Math.round(n-dern)+' ms'); dern=n; if(n-t0<9000) requestAnimationFrame(f); })();
  const r0=window._ruban; let rs=''; (function g(){ try{ const s=JSON.stringify(window._ruban.etat()); if(s!==rs){ rs=s; E('ruban '+s); } }catch(e){} if(performance.now()-t0<9000) requestAnimationFrame(g); })(); }"""
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = contexte(b); pg = ouvre(ctx, F)
    plante(pg, 'rendre le livre'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
    pg.evaluate(SUIT)
    z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(3500)
    ev = pg.evaluate("()=>window.__ev"); L = next(t for t, n in ev if n == 'LEVER')
    print('TENIR (temps depuis le lever)'); [print('  %+5d  %s' % (t - L, n)) for t, n in ev if t >= L - 30][:40]
    # planter
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'arroser les tomates'); pg.wait_for_timeout(600)
    pg.evaluate(SUIT)
    z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[40 + 200 * i / 10, y] for i in range(11)], pas=30, tenue=0); pg.wait_for_timeout(3000)
    ev = pg.evaluate("()=>window.__ev"); L = next((t for t, n in ev if n == 'LEVER'), None)
    print('PLANTER (temps depuis le lever)'); [print('  %+5d  %s' % (t - L, n)) for t, n in ev if L is not None and t >= L - 30][:40]
    b.close()
