# -*- coding: utf-8 -*-
"""⚑ v196 (Tom, 11 nov. 2026, C-259) — LES POINTS DU TRAIT PLAT SONT AUX ABSCISSES DE CEUX DE LA VAGUE.
Banc WebKit (banc_tom), échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79), fenêtre de Tom (PYTHONPATH=scratchpad/v190/fenetretom PROMI_ECHELLE=tom).
Le centre de chaque point est relevé AU DESSIN (chaque `arc` peint sur la vague `#v189Jonction` et sur le trait plat `#v195Plat`, rapporté en pt par la transformation du
canevas), puis rapporté à l'ÉCRAN par la place réelle des deux canevas (`getBoundingClientRect`).
  A · Promi (« faire les crêpes ») et un Chiche lancé à une seule personne (ses points) : autant de points sur le trait plat que sur la vague, à l'abscisse d'écran près (< 0,5 pt).
  B · les deux canevas commencent à la même abscisse d'écran (< 0,05 pt).
  C · aucune erreur de page.
`--sonde` décale le trait plat de 0,6 pt : A et B rougissent."""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B, banc_jonction as BJ
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
ECH = os.environ.get('PROMI_ECHELLE', '1')
VUE = {'1': (390, 844), '0,79': (330, 714), 'tom': (390, 651)}.get(ECH, (390, 844))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True); return ok
PIEGE = """()=>{ window.__arcs={v:[],p:[]}; const a=CanvasRenderingContext2D.prototype.arc; if(!a.__v196){ CanvasRenderingContext2D.prototype.arc=function(x,y,r,s,e){
  const c=this.canvas, q=c.id==='v189Jonction'?'v':(c.parentNode&&c.parentNode.id==='v195Plat'?'p':null);
  if(q && window.__arcs){ const m=this.getTransform(); window.__arcs[q].push({x:(m.a*x+m.c*y+m.e)/c.width, r:r}); }
  return a.apply(this, arguments); }; CanvasRenderingContext2D.prototype.arc.__v196=1; }
  const S=document.getElementById('v192Colle'); if(S) S.__k=''; window._jonctionRedessine(); }"""
LIT = """()=>{ const v=document.getElementById('v189Jonction'), p=document.querySelector('#v195Plat canvas'), rv=v.getBoundingClientRect(), rp=p.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  const A=window.__arcs; return {v:A.v.map(o=>(rv.left-dv.left+o.x*rv.width)/k), p:A.p.map(o=>(rp.left-dv.left+o.x*rp.width)/k), lv:(rv.left-dv.left)/k, lp:(rp.left-dv.left)/k}; }"""
CHICHE = """()=>{ const P=window._parts; const c=promises.find(p=>p.chiche && p.status!=='tenu' && !(P&&P.aPlusieurs(p)));
  if(!c){ const q=promises.find(p=>p.title==='réparer le vélo'); q.who='Marion'; q.avec=[]; q.parts={}; return q.id; } return c.id; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in ['promi', 'chiche']:
        ctx, pg = BJ.ouvre(b, F, nat, *VUE); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
        if nat == 'chiche':
            pid = pg.evaluate(CHICHE); pg.evaluate("id=>{ closeAll(); }", pid); pg.wait_for_timeout(400); pg.evaluate("id=>openDetail(id)", pid)
            for _ in range(30): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(50)
            pg.wait_for_timeout(500)
        pg.evaluate(PIEGE); pg.wait_for_timeout(300)
        if '--sonde' in sys.argv: pg.evaluate("()=>{ document.querySelector('#v195Plat canvas').style.setProperty('left','0.6px','important'); }")   # la sonde : le trait plat décalé de 0,6 pt
        L = pg.evaluate(LIT); v = sorted(set(round(x, 2) for x in L['v'])); pl = sorted(set(round(x, 2) for x in L['p']))   # un canevas redessiné pendant la relève compte ses points deux fois : on compare les ensembles
        juge('[%s · %s] des points sur la vague' % (ECH, nat), len(v) >= 3, len(v))
        juge('[%s · %s] autant de points sur le trait plat que sur la vague' % (ECH, nat), len(v) == len(pl), '%d / %d' % (len(pl), len(v)))
        dx = max([abs(a - c) for a, c in zip(v, pl)] or [99])
        juge('[%s · %s] A · chaque point plat à l’abscisse de son point de vague (< 0,5 pt)' % (ECH, nat), dx < 0.5, 'écart max %.3f pt · %s' % (dx, [round(x, 1) for x in pl]))
        juge('[%s · %s] B · les deux canevas commencent à la même abscisse' % (ECH, nat), abs(L['lv'] - L['lp']) < 0.05, '%.3f / %.3f' % (L['lv'], L['lp']))
        juge('[%s · %s] C · aucune erreur de page' % (ECH, nat), not err, err[:2])
        ctx.close()
    b.close()
print('\n%d/%d' % (sum(res), len(res)))
