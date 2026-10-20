import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
JS="""async ()=>{ const tc=document.getElementById('toileCv'), D=document.getElementById('device').getBoundingClientRect(), q=tc.getBoundingClientRect(), kk=D.width/390;
 const a=document.createElement('canvas'); a.width=390; a.height=844; const ax=a.getContext('2d'); ax.drawImage(tc,(q.left-D.left)/kk,(q.top-D.top)/kk,q.width/kk,q.height/kk);
 const r=document.createElement('canvas'); const ok=Toile.renderTo(r, tc.width/ (q.width/kk), null, {vue:true});
 const b=document.createElement('canvas'); b.width=390; b.height=844; const bx=b.getContext('2d'); bx.drawImage(r,(q.left-D.left)/kk,(q.top-D.top)/kk,q.width/kk,q.height/kk);
 const fa=Flaques.floute(a,4.8), fb=Flaques.floute(b,4.8); const A=fa.getContext('2d').getImageData(0,0,390,844).data, Bd=fb.getContext('2d').getImageData(0,0,390,844).data;
 let m=0,n=0; for(let i=0;i<A.length;i++){const e=Math.abs(A[i]-Bd[i]); if(e>m)m=e; if(e>2)n++;}
 return {ok, tcw:tc.width, rw:r.width, qw:q.width/kk, max:m, hors:n, theme:Toile.mondeCourant()}; }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for m in ('encre','touffe','tesselle','pixel'):
        ctx=B.contexte(b); pg=B.ouvre(ctx); pg.evaluate("m=>{try{Toile.setTheme(m)}catch(e){}}", m); pg.wait_for_timeout(3500)
        print(m, pg.evaluate(JS)); ctx.close()
    b.close()
