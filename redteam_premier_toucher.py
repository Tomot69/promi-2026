# -*- coding: utf-8 -*-
"""⚑ v193 (Tom, C-263 : « le geste ne prend plus le trait du premier coup : il faut s'y reprendre à deux fois, dans les fiches »).
Banc WebKit (banc_tom) ; échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79) et la fenêtre de Tom (PYTHONPATH=scratchpad/v190/fenetretom
PROMI_ECHELLE=tom). Promi et Chiche. VINGT TRACÉS DE SUITE, chacun sur une parole à tenir (remise « en cours » entre deux) :
  1 à 10   au repos, sans défilement ;
  11 à 20 après un aller-retour de défilement, juste avant le toucher (50 ms) : un sur deux LENT (le doigt suit, s'arrête à 0 à 3 pt du haut — c'est ce que laisse
           un doigt qui remonte sans aller jusqu'au bout), un sur deux LANCÉ (l'élan d'iOS, 3 000 pt/s, × 0,998 par ms, jusqu'en haut).
Chaque tracé part du trait (le point du doigt est lu sur l'écran : `elementFromPoint` y rend la zone du geste) et, au premier toucher, la parole est TENUE.
Puis aucune couche d'affichage sur le trait ne prend le doigt (seule la zone du geste). La latence lever → première image de la célébration (la nappe) se relève ;
elle n'est jugée (< 1 image, 16,7 ms) que la machine au calme (charge < 4). Rouge sur v192 (la zone coupée dès 0,25 pt de défilement)."""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
NATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['promi', 'chiche'])
N = next((int(a.split('=', 1)[1]) for a in sys.argv[1:] if a.startswith('--n=')), 20)
ECH = os.environ.get('PROMI_ECHELLE', '1')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-110s %s' % ('✅' if ok else '❌', nom, str(d)[:300]), flush=True); return ok
TITRE = {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}
REMET = """a=>{ var p=promises.find(x=>x.title===a[0]); p.status='encours'; delete p.parts; delete p.vuTenue; if(a[1]){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; p.who='Adrien'; }
  try{ closeAll(); }catch(_){ } openDetail(p.id); return p.id; }"""
def trajet(v0, s_dep, sens, smax):
    out = []; s = s_dep; v = v0 / 1000.0
    while v > 0.02 and len(out) < 90:
        s = s + sens * v * 16.7; v *= 0.998 ** 16.7; s = max(0, min(smax, s)); out.append(round(s, 2))
        if s in (0, smax): break
    return out
with sync_playwright() as p:
    b = p.webkit.launch()
    charge = B.charge()
    for nat in NATS:
        ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 6000)
        pg.evaluate("""()=>{ window.__LEV=0; window.__MAR=0; document.addEventListener('touchend', ()=>{ window.__LEV=performance.now(); window.__MAR=0; }, true);
          var o=window._mareeReleve; window._mareeReleve=function(){ if(window.__LEV && !window.__MAR) window.__MAR=performance.now(); if(o) return o.apply(this, arguments); }; }""")
        pris = []; lat = []; couches = []
        for i in range(N):
            pid = pg.evaluate(REMET, [TITRE[nat], nat == 'chiche']); pg.wait_for_timeout(1400)
            mode = 'repos'
            if i >= N // 2:
                smax = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }")
                if i % 2:
                    mode = 'lent'; bout = (i % 4) * 1.0   # 1 ou 3 pt du haut
                    for s in [smax * j / 20 for j in range(21)] + [smax * (20 - j) / 20 for j in range(21)] + [bout]:
                        pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s); pg.wait_for_timeout(16)
                else:
                    mode = 'lancé'
                    for s in trajet(3000, 0, 1, smax) + trajet(3000, smax, -1, smax):
                        pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s); pg.wait_for_timeout(16)
                pg.wait_for_timeout(50)
            # le trait, lu sur l'écran : l'onde déclarée, en cotes de l'appareil, moins le défilement
            G = pg.evaluate("""()=>{ const c=document.getElementById('dpTrameCv'), d=document.getElementById('detailPoster'), t=(c.getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0], +t[1]), s=d.scrollTop;
              const r=document.getElementById('device').getBoundingClientRect(), k=r.width/390, X=[30,60,120,200,300];
              const sous=X.map(x=>{ const e=document.elementFromPoint(r.left+x*k, r.top+(y(x)-s)*k); return e ? (e.id||e.className||e.tagName)+'' : null; });
              return {s:s, y:X.map(x=>y(x)-s), sous:sous}; }""")
            couches.append(all(e in ('tenirZone', 'tenirCv') for e in G['sous']) or G)
            pts = pg.evaluate("s=>{ const c=document.getElementById('dpTrameCv'), t=(c.getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0], +t[1]); const P=[]; for(let i=0;i<=11;i++){ const x=30+30*i; P.push([x, y(x)-s]); } return P; }", G['s'])
            B.glisse(pg, pts, pas=40, tenue=380); pg.wait_for_timeout(2600)
            st = pg.evaluate("id=>promises.find(x=>x.id===id).status", pid)
            pris.append(st == 'tenu' or (i, mode, round(G['s'], 2), st, G['sous'][:2]))
            l = pg.evaluate("()=>window.__MAR && window.__LEV ? window.__MAR-window.__LEV : null")
            if l is not None: lat.append(round(l, 1))
        ko = [x for x in pris if x is not True]
        juge('[%s · %s] %d tracés de suite (%d au repos, %d après un aller-retour lent ou lancé) : chacun pris au premier toucher' % (ECH, nat, N, N // 2, N - N // 2), not ko, (len(ko), ko[:4]))
        kc = [x for x in couches if x is not True]
        juge('[%s · %s] sur le trait, au point du doigt, seule la zone du geste prend le doigt (aucune couche d\'affichage)' % (ECH, nat), not kc, kc[:2])
        if charge < 4: juge('[%s · %s] latence lever → première image de la célébration < 16,7 ms (%d relevés)' % (ECH, nat, len(lat)), lat and max(lat) < 16.7, lat)
        else: print('  ⏸  [%s · %s] latence NON JUGÉE (charge %.1f) : %s' % (ECH, nat, charge, lat), flush=True)
        juge('[%s · %s] aucune erreur de page' % (ECH, nat), not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
