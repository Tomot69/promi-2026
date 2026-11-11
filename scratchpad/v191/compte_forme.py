import sys, io; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=sys.argv[1]; S=float(sys.argv[2]) if len(sys.argv)>2 else 0
PIEGE="""(()=>{ window.__gid={n:0,px:0}; const o=CanvasRenderingContext2D.prototype.getImageData; CanvasRenderingContext2D.prototype.getImageData=function(x,y,w,h){ if(w*h>200000){ window.__gid.n++; window.__gid.px+=w*h; } return o.apply(this,arguments); }; })();"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,'cercle'); ctx.add_init_script(PIEGE); pg=B.ouvre(ctx,F,6000)
    pid=pg.evaluate("""()=>{ const p=promises.find(x=>x.title==='faire les crêpes'); p.status='encours'; delete p.parts; p.ech={iso:'2026-10-29',due:-11}; p.due=-11;
       p.title='jcicjccjc j jcjcu j jkvlvg ghkfufuguxuxuxucuxuxuxuxuxuxuxuxuxuxuxuxuxuxuxuxuxucuccgggggg';
       p.comments=[{t:'Bien vu, je te suis.',by:'Marion',d:'2026-11-09T09:00:00Z',vu:false}]; try{saveState(true)}catch(e){} closeAll(); openDetail(p.id); return p.id; }""")
    pg.wait_for_timeout(3500)
    for s in (60,120,160,120,60,S): pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}",s); pg.wait_for_timeout(200)
    pg.wait_for_timeout(800); a=pg.evaluate("()=>Object.assign({},window.__gid)")
    z=pg.evaluate("()=>{ const c=document.getElementById('tenirZone'), r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
    yy=z[1]+z[3]*0.45; B.glisse(pg,[[30+33*i,yy] for i in range(11)],pas=60,tenue=380); pg.wait_for_timeout(4500)
    c=pg.evaluate("()=>Object.assign({},window.__gid)"); st=pg.evaluate("id=>promises.find(x=>x.id===id).status",pid)
    print(F,'s finale',S,'| défilement : %d lectures (%.1f Mpx) | tenir : %d lectures (%.1f Mpx) | statut %s | scrollTop pendant/après %s' % (a['n'],a['px']/1e6,c['n']-a['n'],(c['px']-a['px'])/1e6,st, pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")))
    b.close()
