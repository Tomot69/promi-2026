import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src = open('redteam_toile_stable.py', encoding='utf-8').read()
exec(src.split('import json, io, glob, os')[1].split('with sync_playwright')[0].replace('def etat', 'import json, io, glob, os\ndef etat', 1), globals())
exec(src.split('GEO = """')[0].split('res = []')[0].split('PAGES =')[0][-1:] )
GEO = src.split('GEO = """')[1].split('"""')[0]; POSE = src.split('POSE = """')[1].split('"""')[0]
def pose(pg):
    n = 0
    for _ in range(48):
        pg.wait_for_timeout(250); n = n + 1 if pg.evaluate(POSE) else 0
        if n >= 3: return
JR = """(()=>{ window.__jr=[]; var t0=performance.now(), der=''; var id=setInterval(function(){ try{ if(!window.Toile_lecture) return; var l=Toile_lecture(), c=l.cible;
  var e=(c?c.s.toFixed(2):'-')+'/'+(window._vueMain?'M':'')+(l.graines.filter(g=>g.kind!=='gray').length)+'/'+(window.Toile_state?Toile_state().theme:'')+'/'+l.graines.length+'/'+l.W+'x'+l.H;
  if(e!==der){ window.__jr.push(Math.round(performance.now()-t0)+':'+e); der=e; } if(performance.now()-t0>7000) clearInterval(id); }catch(_){ } }, 30); })();"""
with sync_playwright() as p:
    br = p.webkit.launch()
    st = etat(5); S0 = json.loads(st['promi_state'])
    for q in S0['promises']: q['place'] = [0, 0]
    st['promi_state'] = json.dumps(S0)
    import os
    if os.path.exists('scratchpad/v160/x-repare.json'): ls = json.load(open('scratchpad/v160/x-repare.json'))
    else:
        ctx = B.contexte(br, sombre=True, stockage=studio('mascaret')); pose_etat(ctx, st); pg = B.ouvre(ctx, 'app.html'); pose(pg); pg.wait_for_timeout(1500)
        ls = pg.evaluate("()=>{var o={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);o[k]=localStorage.getItem(k);}return o;}"); ctx.close(); json.dump(ls, open('scratchpad/v160/x-repare.json','w'))
    for F in sys.argv[1:]:
        ctx = B.contexte(br, sombre=True); pose_etat(ctx, ls); ctx.add_init_script(JR); pg = B.ouvre(ctx, F); pose(pg)
        for k in range(2):
            if k: pg.reload(timeout=180000); pg.wait_for_timeout(7000); pose(pg)
            g = pg.evaluate(GEO); L = pg.evaluate("()=>window.__jr||[]"); L.append('veille %s · main %s · redemandé %s' % tuple(pg.evaluate("()=>{ var a=window._cadrageLancement||0, m=!!window._vueMain; Toile_autoView(); return [a, m, Toile_lecture().cible.s.toFixed(3)]; }")))
            print('%-14s ouverture %d · vue %s · journal %s' % (F, k + 1, [round(x, 2) for x in g['v']], L), flush=True)
        ctx.close()
    br.close()
