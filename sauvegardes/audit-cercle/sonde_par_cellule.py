# LA VOIE VRAIE : UN RENDU DU MOTEUR PAR CELLULE, DÉCOUPÉ SUR SON VRAI POLYGONE.
# C'est la procédure de dalleTrame, appliquée à un semis engendré. Question : combien ça coûte ?
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile8.html'
Q=r"""(n)=>{
  const W=346,H=206,dpr=Math.min(2,window.devicePixelRatio||1);
  const PAL=window.Toile.cols()||[];
  const MONDES=['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo'];
  const A=document.createElement('canvas'); A.width=Math.round(W*dpr); A.height=Math.round(H*dpr);
  window.Toile.preview(A,'encre',W,H);
  const tpl=(A.__c.seeds.filter(s=>s.kind!=='gray')[0])||A.__c.seeds[0];
  const gc=Math.max(5,Math.round(Math.sqrt(n*W/H))), gr=Math.max(4,Math.round(n/gc));
  const cw=W/gc, ch=H/gr, S=[];
  for(let r=0;r<gr;r++) for(let c=0;c<gc;c++){
    const s={}; for(const k in tpl) s[k]=tpl[k];
    s.x=cw*(c+.5)+(Math.random()-.5)*cw*.7; s.y=ch*(r+.5)+(Math.random()-.5)*ch*.7;
    s.tx=s.x; s.ty=s.y; s.px=null; s.py=null; s.w=0; s.wt=0; s.t0=-99999; s.gc=null;
    s.kind='promi'; s.ci=(Math.random()*PAL.length)|0; s.c=PAL[s.ci]; S.push(s);
  }
  /* le POLYGONE d'une cellule : la boîte coupée par les bissectrices avec les voisins.
     C'est la règle du moteur (germe le plus proche, poids nuls) — pas une approximation. */
  function coupe(poly, ax, ay, bx, by){
    /* garde le demi-plan plus proche de a que de b */
    const mx=(ax+bx)/2, my=(ay+by)/2, dx=bx-ax, dy=by-ay;
    const out=[];
    for(let i=0;i<poly.length;i++){
      const p=poly[i], q=poly[(i+1)%poly.length];
      const dp=(p[0]-mx)*dx+(p[1]-my)*dy, dq=(q[0]-mx)*dx+(q[1]-my)*dy;
      if(dp<=0) out.push(p);
      if((dp<0&&dq>0)||(dp>0&&dq<0)){ const t=dp/(dp-dq); out.push([p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t]); }
    }
    return out;
  }
  function polyDe(k){
    let poly=[[0,0],[W,0],[W,H],[0,H]];
    const a=S[k];
    for(let j=0;j<S.length && poly.length>2;j++){
      if(j===k) continue;
      const b=S[j];
      if(Math.hypot(b.x-a.x,b.y-a.y)>70) continue;     /* au-delà, la bissectrice ne coupe plus la cellule */
      poly=coupe(poly,a.x,a.y,b.x,b.y);
    }
    return poly;
  }
  const cible=document.createElement('canvas'); cible.width=Math.round(W*dpr); cible.height=Math.round(H*dpr);
  const G=cible.getContext('2d'); G.setTransform(dpr,0,0,dpr,0,0);
  const t0=performance.now();
  let tPoly=0, tRend=0, tPose=0, rendus=0;
  const MOND=S.map(()=>MONDES[(Math.random()*MONDES.length)|0]);
  for(let k=0;k<S.length;k++){
    let t=performance.now();
    const poly=polyDe(k); tPoly+=performance.now()-t;
    if(poly.length<3) continue;
    let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
    poly.forEach(p=>{ if(p[0]<x0)x0=p[0]; if(p[0]>x1)x1=p[0]; if(p[1]<y0)y0=p[1]; if(p[1]>y1)y1=p[1]; });
    const pad=6, bw=Math.ceil(x1-x0+2*pad), bh=Math.ceil(y1-y0+2*pad);
    if(bw<2||bh<2) continue;
    t=performance.now();
    /* ⚑ ON NE PASSE QUE LES VOISINS. Seuls eux décident de la frontière de la cellule (c'est déjà le critère
       du polygone), et comme on DÉCOUPE ensuite sur ce polygone, ce qui se passe au-delà n'a aucun effet :
       le résultat est identique, le clone passe de 308 germes à une douzaine. */
    const vois=[];
    for(let j=0;j<S.length;j++){ if(Math.hypot(S[j].x-S[k].x,S[j].y-S[k].y)<=70){
      const o={}; for(const q in S[j]) o[q]=S[j][q]; o.x=S[j].x-(x0-pad); o.y=S[j].y-(y0-pad); o.tx=o.x; o.ty=o.y; vois.push(o); } }
    const cv=document.createElement('canvas'); cv.width=Math.round(bw*dpr); cv.height=Math.round(bh*dpr);
    cv.__c={seeds:vois, th:MOND[k], pw:bw, ph:bh};
    window.Toile.repaint(cv); tRend+=performance.now()-t; rendus++;
    t=performance.now();
    G.save(); G.beginPath();
    poly.forEach((p,i)=>{ if(i) G.lineTo(p[0],p[1]); else G.moveTo(p[0],p[1]); });
    G.closePath(); G.clip();
    G.drawImage(cv, x0-pad, y0-pad, bw, bh);
    G.restore(); tPose+=performance.now()-t;
  }
  const total=performance.now()-t0;
  const d=cible.getContext('2d').getImageData(0,0,cible.width,cible.height).data;
  let peints=0,nn=0; for(let i=3;i<d.length;i+=64){ nn++; if(d[i]>10) peints++; }
  return {germes:S.length, rendus, polygones:Math.round(tPoly), rendus_ms:Math.round(tRend), pose:Math.round(tPose),
          total:Math.round(total), couverture:+(100*peints/nn).toFixed(1)}; }"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('light')"); pg.wait_for_timeout(500)
    for n in (100, 300, 500):
        print('  ', json.dumps(pg.evaluate(Q, n), ensure_ascii=False))
    br.close()
