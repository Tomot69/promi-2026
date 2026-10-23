"""v160c (B2, C-175) — au Studio, monde par monde : l'arrivée (2,5 s), le repos (3 s), un glissé de la jauge. Durées d'image et temps passé
dans chaque fonction qui peint (aperçus, moteur, dalle de la jauge). Usage : python3 studio_profil.py [fichier] [mondes,…]"""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
VOULUS = sys.argv[2].split(',') if len(sys.argv) > 2 else None
ESPION = """()=>{ window.__on=null; window.__P={};
  function enr(nom, t){ if(!window.__on) return; const P=window.__P[window.__on]||(window.__P[window.__on]={f:{}, d:[]}); const e=P.f[nom]||(P.f[nom]=[0,0,0]); e[0]++; e[1]+=t; e[2]=Math.max(e[2],t); }
  function env(o, n, nom){ const f=o&&o[n]; if(typeof f!=='function'||f.__p) return; o[n]=function(){ const t=performance.now(); try{ return f.apply(this,arguments); } finally{ enr(nom, performance.now()-t); } }; o[n].__p=1; }
  ['apercuImage','apercuCompose','apercuPrepare','apercuPrepareProchain','repaintWorld','renderTo','repaint','setTheme','setHue','setPalette','dalleTrame'].forEach(n=>env(Toile, n, n));
  env(window, '_rendDalle', '_rendDalle'); env(window, '_poseDalle', '_poseDalle'); env(window, 'buildStudio', 'buildStudio');
  let av=performance.now(); (function f(t){ if(window.__on){ const P=window.__P[window.__on]||(window.__P[window.__on]={f:{}, d:[]}); P.d.push(t-av); } av=t; requestAnimationFrame(f); })(performance.now()); }"""
def resume(P):
    if not P: return 'rien'
    d = sorted(P['d']); p95 = d[int(0.95 * (len(d) - 1))] if d else 0
    f = sorted(P['f'].items(), key=lambda kv: -kv[1][1])[:4]
    return 'images %d · p95 %.0f · max %.0f · >50 ms : %d · %s' % (len(d), p95, d[-1] if d else 0, sum(1 for v in d if v > 50), ' · '.join('%s ×%d %.0f ms (max %.0f)' % (k, v[0], v[1], v[2]) for k, v in f))
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); }"); pg.evaluate(ESPION)
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(3500)
    vus = []
    for i in range(22):
        m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m in vus: break
        vus.append(m)
        if VOULUS is None or m in VOULUS:
            pg.evaluate("m=>{ window.__on=m+'·repos'; }", m); pg.wait_for_timeout(3000)
            x, y = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.getElementById('st3thumb'); const r=e.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }")
            pg.evaluate("m=>{ window.__on=m+'·jauge'; }", m)
            B.glisse(pg, [[x + 100 * t / 40, y] for t in range(41)] + [[x + 100 - 200 * t / 60, y] for t in range(61)], pas=6); pg.wait_for_timeout(600)
            pg.evaluate("()=>{ window.__on=null; }")
        nxt = '?'
        pg.evaluate("()=>{ window.__on='__arrivee'; }")
        B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(2500)
        m2 = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        pg.evaluate("m=>{ window.__P[m+'·arrivée']=window.__P['__arrivee']; delete window.__P['__arrivee']; window.__on=null; }", m2)
    P = pg.evaluate("()=>window.__P")
    print('charge', B.charge())
    for m in vus:
        if VOULUS is not None and m not in VOULUS: continue
        for ph in ('arrivée', 'repos', 'jauge'): print('%-12s %-8s %s' % (m, ph, resume(P.get(m + '·' + ph))), flush=True)
    b.close()
