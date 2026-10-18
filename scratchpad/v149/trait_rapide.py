# redteam_trait « 70 pt rapide » : que se passe-t-il ? (même séquence, journal du clic « tenue »)
import sys; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
OU = open('redteam_trait.py', encoding='utf-8').read().split('OU = """')[1].split('"""')[0] if 'OU = """' in open('redteam_trait.py', encoding='utf-8').read() else None
exec(open('redteam_trait.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].split('def juge')[0])
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null; }"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx)
    plante(pg, 'rendre le livre'); plante(pg, 'réparer le vélo'); pg.wait_for_timeout(800)
    ids = pg.evaluate("()=>promises.map(p=>p.id)")
    pg.evaluate("""()=>{ window.__J=[]; const J=(m)=>window.__J.push([Math.round(performance.now()), m]);
      document.addEventListener('click', e=>{ const b=e.target.closest&&e.target.closest('#segStatus button'); if(b) J('clic capture '+b.dataset.st+' cur '+(typeof cur!=='undefined'&&cur?cur.id:null)+' st '+(cur?cur.status:null)); }, true);
      document.addEventListener('click', e=>{ const b=e.target.closest&&e.target.closest('#segStatus button'); if(b) J('clic bulle '+b.dataset.st+' cur '+(cur?cur.id:null)+' st '+(cur?cur.status:null)+' prevented '+e.defaultPrevented); }, false);
      document.addEventListener('touchend', ()=>J('touchend · traitDernier '+JSON.stringify(window._traitDernier)), true); }""")
    for k, (pid, pas) in enumerate(((ids[0], 100), (ids[1], 12))):
        pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(700)
        pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(1800)
        z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
        glisse(pg, [[200 + 70 * i / 10, y] for i in range(11)], pas=pas, tenue=380); pg.wait_for_timeout(3500)
        print(k, pg.evaluate("ids=>ids.map(i=>promises.find(p=>p.id===i).status)", ids), pg.evaluate("()=>window._traitDernier"))
    for j in pg.evaluate("()=>window.__J"): print(j)
    b.close()
