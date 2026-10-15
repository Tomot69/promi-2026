import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
INSTR = """()=>{ const M=window.PeloteMoteur; window.__L={ev:[], t0:0};
  const env=(o,n)=>{ const f=o[n]; if(typeof f!=='function') return; o[n]=function(){ const a=performance.now(); try{ return f.apply(this,arguments); } finally { window.__L.ev.push([n, +(a-window.__L.t0).toFixed(1), +(performance.now()-a).toFixed(1)]); } }; };
  ['atlasAlpha','semisPavage','batIles','peintGL','peint'].forEach(n=>env(M,n));
  const dt=Toile.dalleTrame; let nd=0, td=0; Toile.dalleTrame=function(){ const a=performance.now(); try{ return dt.apply(this,arguments); } finally { nd++; td+=performance.now()-a; window.__L.dalles=[nd, +td.toFixed(1)]; } };
  document.addEventListener('touchstart', e=>{ window.__L.t0=performance.now(); window.__L.ev=[]; window.__L.dalles=[0,0]; nd=0; td=0; window.__L.p0=(window._aura&&_aura.etat)?_aura.etat().peints:0; window.__L.vu=null; window.__L.images=[];
    let n=0; (function f(){ const t=performance.now()-window.__L.t0; n++; let p=0; try{ p=_aura.etat().peints; }catch(e){}
      const sc=document.getElementById('auraScreen'), ouv=sc&&sc.classList.contains('show')&&sc.getBoundingClientRect().top<400;
      if(ouv && window.__L.ouv==null) window.__L.ouv=+t.toFixed(1);
      if(p>window.__L.p0 && window.__L.vu==null){ window.__L.vu=+t.toFixed(1); window.__L.nimg=n; }
      if(t<5000 && window.__L.vu==null) requestAnimationFrame(f); })(); }, true); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx)
    pg.evaluate("()=>{ promises.slice(0,6).forEach(p=>{ p.status='tenu'; p.keptAt=Date.now(); }); try{ syncAll(); }catch(e){} }"); pg.wait_for_timeout(1500)
    pg.evaluate(INSTR)
    print('etat', pg.evaluate("()=>{ try{ const e=_aura.etat(); return {peints:e.peints, palier:e.palier, gl:PeloteMoteur.glDispo&&PeloteMoteur.glDispo()}; }catch(e){ return String(e); } }"))
    for k in range(1, 6):
        pg.evaluate("()=>{ window.__L.ouv=null; }")
        B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(3800)
        L = pg.evaluate("()=>window.__L")
        ev = L['ev']; tot = {}
        for n, t, d in ev:
            if t < (L['vu'] or 9e9) + 5: tot.setdefault(n, [0, 0.0]); tot[n][0] += 1; tot[n][1] += d
        print('ouverture %d : écran ouvert à %s ms · PREMIÈRE IMAGE DE PELOTE à %s ms (image n° %s) · avant elle : %s · dalles rendues %s' % (k, L.get('ouv'), L.get('vu'), L.get('nimg'), {n: [v[0], round(v[1], 1)] for n, v in tot.items()}, L.get('dalles')), flush=True)
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(1200)
    print(pg.__dict__['erreurs'][:2]); b.close()
