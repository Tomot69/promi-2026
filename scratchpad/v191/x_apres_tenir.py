import sys, io; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=sys.argv[1]; long_=('--long' in sys.argv); defile=('--defile' in sys.argv)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F,6000)
    pid=pg.evaluate("""a=>{ const p=promises.find(x=>x.title==='faire les crêpes'); p.status='encours'; delete p.parts; p.ech={iso:'2026-10-29',due:-11}; p.due=-11;
       if(a) p.title='jcicjccjc j jcjcu j jkvlvg ghkfufuguxuxuxucuxuxuxuxuxuxuxuxuxuxuxuxuxuxuxuxuxucuccgggggg';
       p.comments=[{t:'Bien vu, je te suis.',by:'Marion',d:'2026-11-09T09:00:00Z',vu:false}]; try{saveState(true)}catch(e){} closeAll(); openDetail(p.id); return p.id; }""", long_)
    pg.wait_for_timeout(3500)
    if defile:
        for _ in range(10):
            for s in (40,80,120,160,200,160,120,80,40,0): pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}",s); pg.wait_for_timeout(60)
        pg.wait_for_timeout(800)
    z=pg.evaluate("()=>{ const c=document.getElementById('tenirZone'), r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
    yy=z[1]+z[3]*0.45; B.glisse(pg,[[30+33*i,yy] for i in range(11)],pas=60,tenue=380); pg.wait_for_timeout(4500)
    st=pg.evaluate("id=>promises.find(x=>x.id===id).status",pid)
    B.tap_sel(pg,'#detailPoster > .enh .closeb'); pg.wait_for_timeout(1500)
    sh=pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
    print(F,'long' if long_ else 'court','defile' if defile else '', '| statut',st,'| fiche encore ouverte après X :',sh, pg.erreurs[:2])
    b.close()
