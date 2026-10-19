import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx); pg.emulate_media(reduced_motion='reduce'); B.plante(pg,'rendre le livre')
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
    f=lambda: pg.evaluate("""()=>{ const dp=document.getElementById('detailPoster'), o=[]; dp.querySelectorAll('*').forEach(e=>{ const c=getComputedStyle(e); const v=+c.opacity; if(v>0.02&&v<0.98&&c.visibility!=='hidden'&&c.display!=='none'&&e.getBoundingClientRect().width>2) o.push((e.id||e.className||e.tagName)+':'+v+':'+c.transitionDuration+':'+c.transitionProperty); }); return o; }""")
    print('avant', f())
    z=pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
    y=z[1]+z[3]*0.45; B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380)
    for t in (50,300,1500): pg.wait_for_timeout(t); print(t, f())
    b.close()
