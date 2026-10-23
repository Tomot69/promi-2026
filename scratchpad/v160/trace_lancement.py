import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src = open('redteam_toile_stable.py', encoding='utf-8').read()
exec(src.split('import json, io, glob, os')[1].split('ENTASSE =')[0].replace('def etat', 'import json, io, glob, os\ndef etat', 1), globals())
TR = """(()=>{ window.__tr=[]; var t0=performance.now(); var V;
  Object.defineProperty(window,'Toile',{configurable:true, get:function(){return V;}, set:function(x){ V=x; try{
    ['setTheme','sync','addPromi','resetView'].forEach(function(n){ var f=x[n]; if(!f||f.__tr) return; x[n]=function(){ var th0=''; try{th0=x.getTheme&&x.getTheme();}catch(_){}
      var st=(new Error()).stack.split('\\n').slice(1,4).map(function(l){ return l.replace(/^.*?(app\\.html|promi-moteur\\.js|zz[^:]*)/,'$1').replace(/\\?v=[^:]*/,'').slice(0,40); }).join(' < ');
      var r=f.apply(this,arguments); var c=''; try{ var L=window.Toile_lecture&&Toile_lecture(); c=L&&L.cible?L.cible.s.toFixed(3):'-'; }catch(_){}
      window.__tr.push(Math.round(performance.now()-t0)+' '+n+'('+(n==='setTheme'?arguments[0]:(arguments[0]||[]).length)+') '+th0+'→'+(x.getTheme&&x.getTheme())+' cible '+c+' · '+st); return r; }; x[n].__tr=1; }); }catch(_){ } } }); })();"""
with sync_playwright() as p:
    br = p.webkit.launch()
    for F in sys.argv[2:]:
        for k in range(int(sys.argv[1])):
            ctx = B.contexte(br, sombre=True, stockage=studio('halin')); pose_etat(ctx, etat(1)); ctx.add_init_script(TR); pg = B.ouvre(ctx, F, attente=7000)
            pg.wait_for_timeout(5000); v = pg.evaluate("()=>{var l=Toile_lecture(); return [l.vue.s.toFixed(3), l.graines.filter(g=>g.kind!=='gray').length, l.graines.length]}")
            print('==', F, k, v, flush=True)
            if v[0] != '5.000':
                for l in pg.evaluate("()=>window.__tr"): print('   ', l)
            ctx.close()
    br.close()
