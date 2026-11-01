#!/usr/bin/env python3
"""redteam_guide_phrase.py — ⚑ v175 (Tom, C-203) : LA PHRASE DU STUDIO PARAÎT AVEC SA FLÈCHE, COMME CELLES DU + ET DE PARTAGER.

« La phrase du Studio arrive trop tard. Elle doit paraître EN MÊME TEMPS que sa flèche, comme les phrases du + et de Partager. Juge : écart entre le début de la phrase et la
naissance de la flèche, identique (±50 ms) sur les trois étapes. »

Banc comme Tom (WebKit, doigt), échelles 1 et 0,79. Image par image, DANS la page :
  · le début de la phrase = la première image où la plume a avancé (`ctl.etat().t > 0`) sur le texte `#guidePhrase` ;
  · la naissance de la flèche = la première image où de l'encre orange est peinte sur `#guideFleche` (lue sur le canevas, pas sur un attribut) ;
  A · sur chacune des trois étapes : l'écart mesuré, et les trois écarts à ± 50 ms de leur médiane ; B · chaque étape : au plus 150 ms d'écart absolu.
Les durées sont en temps réel : sous une charge > 4 elles se lisent en images ; un rouge sous charge se rejoue au calme (C-137).
Preuve : `--fichier=zz-v175a.html` rougit (la phrase du Studio après sa flèche).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', n, str(d)[:230]), flush=True)
SONDE = r"""(()=>{ window.__G={}; const T=window.TraceLettres, tr=T.trace; let ctl=null;
  T.trace=function(e,c,o){ const r=tr.apply(this,arguments); if(!(o&&o.preparer) && e && e.id==='guidePhrase'){ ctl=r; } return r; };
  (function f(){ const n=performance.now(), g=document.getElementById('guide'), q=g&&g.getAttribute('data-guide'), et=g&&(q==='studio'||q==='plus'||q==='partage')?q:null;
    if(et){ const X=__G[et]||(__G[et]={ph:null, fl:null, net:null}); const v=+(g.getAttribute('data-net')||0);
      if(X.net==null && v>0.001) X.net=n;
      if(X.ph==null && ctl && !ctl.fini){ let t=-1; try{ t=ctl.etat().t; }catch(_){ } if(t>0) X.ph=n; }
      if(X.fl==null){ const c=document.getElementById('guideFleche'); let bo=null; try{ bo=JSON.parse(g.getAttribute('data-fleche')||'null'); }catch(_){ }
        if(c && bo && bo.boite){ const k=c.width/390, b=bo.boite, x=Math.max(0,Math.floor(b[0]*k)), y=Math.max(0,Math.floor(b[1]*k)), w=Math.ceil(b[2]*k), h=Math.ceil(b[3]*k); const d=c.getContext('2d').getImageData(x,y,w,h).data; for(let i=3;i<d.length;i+=16) if(d[i]>128){ X.fl=n; break; } } } }
    requestAnimationFrame(f); })(); })();"""
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
def tap_pt(pg, x, y):
    d = dev(pg); B.tap(pg, d[0] + x * d[2], d[1] + y * d[2], appareil=False)
def tap_sel(pg, sel):
    c = pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
    if c: B.tap(pg, c[0], c[1], appareil=False)
    return bool(c)
def attend(pg, js, n=170, pas=100):
    for _ in range(n):
        v = pg.evaluate(js)
        if v: return v
        pg.wait_for_timeout(pas)
    return None
ETAPE = "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='%s' && +g.getAttribute('data-net')>=0.999);}"
with sync_playwright() as p:
    b = p.webkit.launch(); print('fichier :', F, '· charge %.1f' % B.charge())
    for vw, vh, nom in ((390, 844, '1'), (330, 714, '0,79')):
        ctx = B.contexte(b, False, onb=True, guide=False, vw=vw, vh=vh); pg = B.ouvre(ctx, F, attente=6500)
        pg.evaluate(SONDE); pg.evaluate("()=>{ try{ closeAll(); }catch(e){} _guide.prepare&&_guide.prepare(); }"); pg.wait_for_timeout(9000)   # l'onboarding prépare la phrase à sa fin (v175) : le temps qu'il laisse
        pg.evaluate("()=>{ _guide.attend(false); }")
        e = attend(pg, "()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&+g.getAttribute('data-net')>=0.999 ? _guide.etat() : null;}")
        if not e: juge('[%s] le guide atteint le Studio' % nom, False); ctx.close(); continue
        pg.wait_for_timeout(900); tap_pt(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600); tap_sel(pg, '#studioScreen .closeb')
        attend(pg, ETAPE % 'plus'); pg.wait_for_timeout(1200)
        tap_pt(pg, 200, 520)
        attend(pg, ETAPE % 'partage'); pg.wait_for_timeout(1200)
        G = pg.evaluate("()=>__G"); print('  ', nom, G, 'charge %.1f' % B.charge(), flush=True); E = {}
        for et in ('studio', 'plus', 'partage'):
            x = G.get(et) or {}
            E[et] = None if (x.get('ph') is None or x.get('fl') is None) else x['ph'] - x['fl']
            juge('[%s] %s : le début de la phrase et la naissance de la flèche se lisent, ≤ 150 ms d\'écart' % (nom, et), E[et] is not None and abs(E[et]) <= 150, E[et] if E[et] is None else '%+.0f ms' % E[et])
        v = [x for x in E.values() if x is not None]
        if len(v) == 3:
            m = sorted(v)[1]; juge('[%s] les trois écarts à ± 50 ms' % nom, max(v) - min(v) <= 100 and all(abs(x - m) <= 50 for x in v), {k: round(x) for k, x in E.items()})
        else: juge('[%s] les trois écarts à ± 50 ms' % nom, False, E)
        juge('[%s] aucune erreur de page' % nom, not [x for x in pg.erreurs if 'version.json' not in x], pg.erreurs[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
