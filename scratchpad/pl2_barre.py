# l'air de la barre : libellés entre eux, contre le bord du panneau, icônes contre l'anneau du +
import json
from playwright.sync_api import sync_playwright
J=r"""(id)=>{const f=document.querySelector('[data-cadre="'+id+'"]');const F=f.getBoundingClientRect();
 const bar=f.querySelector('.barre');const B=bar.getBoundingClientRect();const bw=parseFloat(getComputedStyle(bar).borderLeftWidth);
 const ink=e=>{const rg=document.createRange();rg.selectNodeContents(e);const q=rg.getBoundingClientRect();return {t:e.textContent,x0:q.left-F.left,x1:q.right-F.left,y0:q.top-F.top,y1:q.bottom-F.top};};
 const L=[...f.querySelectorAll('.it .lb')].map(ink).sort((a,b)=>a.x0-b.x0);
 const I=[...f.querySelectorAll('.it svg')].map(s=>{const r=s.getBoundingClientRect();return {x0:r.left-F.left,x1:r.right-F.left,y0:r.top-F.top,y1:r.bottom-F.top};});
 const P=f.querySelector('.plus2').getBoundingClientRect();const cx=P.left-F.left+P.width/2,cy=P.top-F.top+P.height/2,R=P.width/2;
 const dc=b=>{const nx=Math.max(b.x0,Math.min(cx,b.x1)),ny=Math.max(b.y0,Math.min(cy,b.y1));return Math.hypot(nx-cx,ny-cy)-R;};
 const o={libelles:L.map(l=>[l.t,+(l.x1-l.x0).toFixed(1)])};
 o.entre=L.slice(1).map((l,i)=>[L[i].t+'↔'+l.t,+(l.x0-L[i].x1).toFixed(1)]);
 o.bord_gauche=+(L[0].x0-(B.left-F.left+bw)).toFixed(1); o.bord_droit=+((B.right-F.left-bw)-L[L.length-1].x1).toFixed(1);
 o.anneau=[...L.map(l=>['lib '+l.t,+dc(l).toFixed(1)]),...I.map((b,i)=>['icône '+i,+dc(b).toFixed(1)])];
 const rr=parseFloat(getComputedStyle(bar).borderTopLeftRadius)-bw, X0=B.left-F.left+bw, X1=B.right-F.left-bw, Y0=B.top-F.top+bw, Y1=B.bottom-F.top-bw;
 const libre=(x,y)=>{ const cx2=Math.min(Math.max(x,X0+rr),X1-rr), cy2=Math.min(Math.max(y,Y0+rr),Y1-rr); const d=Math.hypot(x-cx2,y-cy2); return (d>0? rr-d : Math.min(x-X0,X1-x,y-Y0,Y1-y)); };
 const coins=b=>Math.min(libre(b.x0,b.y0),libre(b.x1,b.y0),libre(b.x0,b.y1),libre(b.x1,b.y1));
 o.courbure=[...L.map(l=>['lib '+l.t,+coins(l).toFixed(1)]),...I.map((b,i)=>['icône '+i,+coins(b).toFixed(1)])];
 o.plus_panneau_air=[+((P.top-F.top)-Y0).toFixed(1),+(Y1-(P.bottom-F.top)).toFixed(1)];
 o.bas_libelles=+(B.bottom-F.top-bw-Math.max(...L.map(l=>l.y1))).toFixed(1);
 o.plus_panneau=[+((P.top-F.top)-(B.top-F.top+bw)).toFixed(1),+((B.bottom-F.top-bw)-(P.bottom-F.top)).toFixed(1)];o.plus_vs_icones=+((P.top+P.height/2)-(I.length?(f.querySelector('.it').getBoundingClientRect().top+f.querySelector('.it').getBoundingClientRect().height/2):0)).toFixed(1);o.icone_lib=I.map((b,i)=>+(L[i].y0-b.y1).toFixed(1));
 return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1700,'height':1000}); pg.goto("http://127.0.0.1:8752/PLANCHE-ACCUEIL-2.html"); pg.wait_for_timeout(2500)
    for i in ['B2-clair-repos','B2-sombre-repos']: print(i, json.dumps(pg.evaluate(J,i),ensure_ascii=False))
    b.close()
