import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
st = json.load(io.open('scratchpad/v145/etats/etat-25.json', encoding='utf-8')); st.pop('promi_theme', None)
E = "try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); ctx.add_init_script(E); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8762/app.html'); pg.wait_for_timeout(8000)
    print(pg.evaluate("""()=>{ var o={}; document.querySelectorAll('canvas.mini-dalle').forEach(function(c){ var s=c.closest('.screen,.sheet,[id$=Screen],[id$=Sheet],#indexList,#feed')||c.parentNode; var k=(s.id||s.className||'?')+' '+c.width+'×'+c.height+' vis:'+(c.offsetParent?1:0); o[k]=(o[k]||0)+1; }); return o; }"""))
    # qui appelle peintMinis pendant une plantation, et combien de rendus de dalle
    pg.evaluate("""()=>{ window.__pm=[]; var f=window.peintMinis; window.peintMinis=function(r){ var t=performance.now(); var x=f.apply(this,arguments); window.__pm.push([Math.round(t-window.__t0), Math.round(performance.now()-t), (r&&r.id)||(r&&r.className)||'document', (new Error().stack||'').split('\\n').slice(1,4).join(' < ').replace(/http:\\/\\/[^ ]*app.html:/g,'L').slice(0,200)]); return x; };
      window.__rd=[]; var g=window._rendDalle; window._rendDalle=function(id,w,h,o){ var t=performance.now(); var x=g.apply(this,arguments); var d=performance.now()-t; if(d>3) window.__rd.push([Math.round(t-window.__t0), Math.round(d), id, w, h, o&&o.siPret?1:0]); return x; }; }""")
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{document.getElementById('fTitle').value='tenir bon';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(3200)
    pg.evaluate("()=>{ window.__pm.length=0; window.__rd.length=0; window.__t0=performance.now(); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(5000)
    r = pg.evaluate("()=>({pm:window.__pm, rd:window.__rd})")
    print('appels peintMinis :', len(r['pm'])); [print('  ', x) for x in r['pm'][:14]]
    print('rendus de dalle > 3 ms :', len(r['rd']), 'somme', sum(x[1] for x in r['rd']), 'ms'); [print('  ', x) for x in r['rd'][:25]]
    b.close()
