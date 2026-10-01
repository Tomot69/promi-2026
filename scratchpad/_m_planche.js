/* ════════════════════════════════════════════════════════════════════════════
   LA PLANCHE — trois concepts, chacun a vide, a cinq, a trente.
   L'ETAT VIDE EST LE TEST DECISIF : s'il n'est pas deja beau, le concept tombe.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var NSEM=150000, TAI0=[2.6,3.4,4.4];

function neuf(){ return document.createElement('canvas'); }

window.addEventListener('load',function(){
  setTimeout(bat, 700);
});

function palette(){
  var pal;
  try{ pal=Toile.cols(); }catch(e){ pal=[[208,176,255],[58,84,255],[240,122,46],[143,160,255]]; }
  /* ⚑ LE SOL EST UNE MATIERE, PAS UNE COULEUR DE PALETTE.
     La ceramique crue et la pierre tendre ne sont pas vives : elles sont
     PROFONDES. On prend la famille de la palette, on la tient a une luminance
     moyenne et a une saturation modeste — et c'est LE GRAIN qui la fera vivre,
     pas la saturation. Les dalles, elles, gardent la palette pleine. */
  var hs=0,hc=0,ss=0,i;
  for(i=0;i<pal.length;i++){
    var h=m_r2h(pal[i]);
    hs+=Math.sin(h[0]*6.283185); hc+=Math.cos(h[0]*6.283185); ss+=h[1];
  }
  var hm=Math.atan2(hs,hc)/6.283185; if(hm<0)hm+=1;
  var cols=[ m_versLum(hm, Math.min(0.42,(ss/pal.length)*0.55), 112) ];
  var CIB=[64,158,196,96];
  for(i=0;i<pal.length;i++){
    var q=m_r2h(pal[i]);
    cols.push(m_versLum(q[0], Math.min(0.96,Math.max(0.58,q[1]*1.5)), CIB[i%CIB.length]));
  }
  return cols;
}

/* les dalles : de VRAIES dalles du moteur, chacune dans le monde de sa
   plantation — acquis du chantier precedent, on ne le refait pas. */
var MONDES=['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons'];
function iles(n,cols,PXR){
  var IL=[], k, dpr=Math.min(2,window.devicePixelRatio||1);
  if(n<=0) return {iles:[], col:cols, ncol:cols.length};
  /* accretion : la grappe grandit, elle ne se subdivise pas */
  var C=[-0.10,-0.14,0.985];
  var _cl=Math.cos(0.9), _sl=Math.sin(0.9), _ct=Math.cos(0.26), _st=Math.sin(0.26);
  var _zp=-C[1]*_st+C[2]*_ct, _y=C[1]*_ct+C[2]*_st;
  C=[C[0]*_cl-_zp*_sl, _y, C[0]*_sl+_zp*_cl];
  var R=0.20;
  IL.push({c:C, r:R});
  for(k=1;k<n;k++){
    var pose=null;
    for(var t=0;t<200&&!pose;t++){
      var a=IL[(m_h(k*17+t*7+1)*IL.length)|0];
      var hx=0,hy=1,hz=0; if(Math.abs(a.c[1])>0.9){hx=1;hy=0;}
      var e1=[a.c[1]*hz-a.c[2]*hy, a.c[2]*hx-a.c[0]*hz, a.c[0]*hy-a.c[1]*hx];
      var m1=Math.hypot(e1[0],e1[1],e1[2])||1; e1=[e1[0]/m1,e1[1]/m1,e1[2]/m1];
      var e2=[a.c[1]*e1[2]-a.c[2]*e1[1], a.c[2]*e1[0]-a.c[0]*e1[2], a.c[0]*e1[1]-a.c[1]*e1[0]];
      var an=m_h(k*53+t*11+5)*6.283185, dd=R*(2.0+m_h(k*29+t*13+2)*0.5);
      var cd=Math.cos(dd), sd=Math.sin(dd), ca=Math.cos(an), sa=Math.sin(an);
      var p=[a.c[0]*cd+(e1[0]*ca+e2[0]*sa)*sd,
             a.c[1]*cd+(e1[1]*ca+e2[1]*sa)*sd,
             a.c[2]*cd+(e1[2]*ca+e2[2]*sa)*sd];
      var mp=Math.hypot(p[0],p[1],p[2])||1; p=[p[0]/mp,p[1]/mp,p[2]/mp];
      var ok=true;
      for(var j=0;j<IL.length;j++){
        var dp=p[0]*IL[j].c[0]+p[1]*IL[j].c[1]+p[2]*IL[j].c[2];
        if(dp>1)dp=1;
        if(Math.acos(dp)<R*1.78){ok=false;break;}
      }
      if(ok) pose=p;
    }
    if(!pose) break;
    IL.push({c:pose, r:R*(0.90+m_h(k*97+11)*0.24)});
  }
  /* on peint chaque dalle avec le moteur, dans une vraie cellule */
  var cnt={}, BR=[], MAG=2.1;
  for(k=0;k<IL.length;k++){
    var gg=IL[k].r*2*PXR/MAG*0.74;
    var P=m_cellule(gg, k*7919+31);
    var cvd=neuf(), ok2=false;
    try{ ok2=Toile.dalleGeneree(cvd,{monde:MONDES[(m_h(k*13+5)*8)|0],
          palette:Toile.getPalette(), poly:P, site:[0,0], sp:gg*1.05,
          ci:(m_h(k*29+3)*4)|0, lit:(k*3)%5, ang:m_h(k*47+9)*Math.PI,
          tone:[1.0,0.76,1.24,0.88,1.12][k%5], pad:10}); }catch(e){}
    if(!ok2||!cvd.width){ BR.push(null); continue; }
    var d=cvd.getContext('2d').getImageData(0,0,cvd.width,cvd.height).data;
    for(var q=0;q<d.length;q+=4){ if(d[q+3]<24)continue;
      var q5=((d[q]>>3)<<10)|((d[q+1]>>3)<<5)|(d[q+2]>>3);
      cnt[q5]=(cnt[q5]||0)+1; }
    BR.push({w:cvd.width,h:cvd.height,d:d,sx:cvd.__site[0]*dpr,sy:cvd.__site[1]*dpr,kk:PXR/MAG*dpr});
  }
  var cles=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a];}).slice(0,200);
  var IDX={};
  for(k=0;k<cles.length;k++){var v=+cles[k];IDX[v]=cols.length;
    cols.push([((v>>10)&31)*8+4,((v>>5)&31)*8+4,(v&31)*8+4]);}
  function proche(v){
    if(IDX[v]!==undefined)return IDX[v];
    var r=((v>>10)&31)*8+4,gg2=((v>>5)&31)*8+4,b=(v&31)*8+4,best=1,bd=1e9;
    for(var z=1;z<cols.length;z++){
      var dr=cols[z][0]-r,dg=cols[z][1]-gg2,db=cols[z][2]-b,dd2=dr*dr+dg*dg+db*db;
      if(dd2<bd){bd=dd2;best=z;} }
    return (IDX[v]=best);
  }
  for(k=0;k<BR.length;k++){
    var B=BR[k]; if(!B){IL[k].m=null;continue;}
    var m=new Uint8Array(B.w*B.h), pp=0;
    for(var j2=0;j2<B.d.length;j2+=4,pp++){
      if(B.d[j2+3]<24)continue;
      m[pp]=proche(((B.d[j2]>>3)<<10)|((B.d[j2+1]>>3)<<5)|(B.d[j2+2]>>3)); }
    IL[k].m=m; IL[k].mw=B.w; IL[k].mh=B.h; IL[k].sx=B.sx; IL[k].sy=B.sy; IL[k].kk=B.kk;
  }
  for(k=0;k<IL.length;k++){
    var c=IL[k].c, hx2=0,hy2=1,hz2=0; if(Math.abs(c[1])>0.9){hx2=1;hy2=0;}
    var ax=c[1]*hz2-c[2]*hy2, ay=c[2]*hx2-c[0]*hz2, az=c[0]*hy2-c[1]*hx2;
    var am=Math.hypot(ax,ay,az)||1; ax/=am;ay/=am;az/=am;
    IL[k].e1=[ax,ay,az];
    IL[k].e2=[c[1]*az-c[2]*ay, c[2]*ax-c[0]*az, c[0]*ay-c[1]*ax];
  }
  return {iles:IL, col:cols, ncol:cols.length};
}
function m_cellule(g,graine){
  var S=[], rnd=(function(s){s=(s*2654435761)>>>0;return function(){
    s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};})(graine);
  var i,j,k,q;
  for(j=-2;j<=2;j++)for(i=-2;i<=2;i++)
    S.push([i*g+(rnd()-.5)*g*0.46, j*g+(rnd()-.5)*g*0.46]);
  var bi=0,bd=1e9;
  for(q=0;q<S.length;q++){var d=Math.hypot(S[q][0],S[q][1]);if(d<bd){bd=d;bi=q;}}
  var Si=S[bi],R=g*6,P=[[Si[0]-R,Si[1]-R],[Si[0]+R,Si[1]-R],[Si[0]+R,Si[1]+R],[Si[0]-R,Si[1]+R]];
  for(j=0;j<S.length&&P.length>2;j++){
    if(j===bi)continue;
    var Sj=S[j],nx=Si[0]-Sj[0],ny=Si[1]-Sj[1],nm=Math.hypot(nx,ny);
    if(nm<1e-9)continue; nx/=nm;ny/=nm;
    var dec=((Si[0]+Sj[0])/2)*nx+((Si[1]+Sj[1])/2)*ny, Q=[], m=P.length;
    for(k=0;k<m;k++){
      var a=P[k],b=P[(k+1)%m], da=a[0]*nx+a[1]*ny-dec, db=b[0]*nx+b[1]*ny-dec;
      if(da>=0)Q.push(a);
      if((da>=0)!==(db>=0)){var t=da/(da-db);Q.push([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]);} }
    P=Q;
  }
  var O=[]; for(k=0;k<P.length;k++)O.push([P[k][0]-Si[0],P[k][1]-Si[1]]);
  return O;
}

function bat(){
  var G=document.getElementById('g');
  var DPR=Math.min(2,window.devicePixelRatio||1);
  var SEM=m_semis(NSEM);
  var ATL={};
  function atlas(css){
    if(ATL[css]) return ATL[css];
    var k=css/620, T=[TAI0[0]*k*DPR,TAI0[1]*k*DPR,TAI0[2]*k*DPR];
    ATL[css]={t:T,
      f:atlasAlpha(GRAIN_FACETTE,T,M_ORI,M_NIV,0.42,1.00,true,M_NVAR),
      p:atlasAlpha(GRAIN_POLI,   T,M_ORI,M_NIV,0.62,1.00,true,M_NVAR)};
    return ATL[css];
  }

  function rang(t,x,cls){
    var s=document.createElement('div'); s.className='rang';
    s.innerHTML=(t?'<h2>'+t+'</h2>':'')+(x?'<p>'+x+'</p>':'');
    var gr=document.createElement('div'); gr.className=cls; s.appendChild(gr);
    G.appendChild(s); return gr;
  }
  function cadre(hote,css,fn,opt,leg){
    var fg=document.createElement('figure');
    var box=document.createElement('div'); box.className='cadre';
    var cv=neuf(); cv.setAttribute('data-cad',opt.id);
    box.appendChild(cv); fg.appendChild(box);
    var fc=document.createElement('figcaption'); fc.innerHTML=leg; fg.appendChild(fc);
    hote.appendChild(fg);
    var AT=atlas(css);
    opt.css=css; opt.tailles=AT.t; opt.atlasF=AT.f; opt.atlasP=AT.p; opt.semis=SEM;
    cv.__opt=opt;
    try{ fn(cv,opt); }catch(e){ console.error(e); }
  }

  var COLS=palette();
  var PXR=620*0.472;
  var JEU={};
  function jeu(n){
    if(JEU[n]) return JEU[n];
    var cols=COLS.slice();
    var r=iles(n,cols,PXR);
    return (JEU[n]={iles:r.iles, col:r.col.map(function(c){return null;}), src:r.col, ncol:r.col.length});
  }
  function rampe(src,grade){
    var COL=[];
    for(var c=0;c<src.length;c++){
      var RP=rampeCouleur(src[c]);
      for(var m=0;m<MARCHES;m++) COL.push(pack(RP[m]));
    }
    return COL;
  }

  /* ── A ───────────────────────────────────────────────────────────────── */
  var rA=rang('A · La mémoire de la main',
    'Une matière minérale — entre la céramique crue et la pierre tendre. Le geste ne creuse '+
    'pas : <b>il polit</b>. Là où la main est passée, le grain s’affine, se couche dans le sens '+
    'du geste, et la chroma monte d’un ton. La forme reste un cercle parfait, quelle que soit '+
    'l’histoire des gestes.','tri');
  [[0,'<b>Vide.</b> Le test décisif.'],[5,'<b>5 Promi.</b>'],[30,'<b>30 Promi.</b>']].forEach(function(z){
    var J=jeu(z[0]);
    cadre(rA,400,m_peintMatiere,{id:'a-'+z[0], gestes:m_gestes(9,17),
      iles:J.iles, col:rampe(J.src), ncol:J.ncol},z[1]);
  });

  var rA2=rang('','','duo');
  var J30=jeu(30);
  cadre(rA2,620,m_peintMatiere,{id:'a-grand', gestes:m_gestes(9,17),
    iles:J30.iles, col:rampe(J30.src), ncol:J30.ncol},
    '<b>A, en grand.</b> Trente Promi et neuf gestes.');
  var J0=jeu(0);
  cadre(rA2,620,m_peintMatiere,{id:'a-vide-grand', gestes:m_gestes(9,17),
    iles:J0.iles, col:rampe(J0.src), ncol:J0.ncol},
    '<b>A, à vide, en grand.</b> Aucun Promi — seulement la matière et neuf gestes.');

  /* ── B ───────────────────────────────────────────────────────────────── */
  var rB=rang('B · Le fil',
    'L’objet est le <b>cumul des trajets d’un fil</b> autour du Noyau. Aucun trajet n’est '+
    'lisible seul : ce qu’on voit est le <b>moiré</b> qu’ils forment ensemble. Un Promi ajoute '+
    'un trajet, et un trajet ne s’efface jamais.','tri');
  [[7,'<b>Vide.</b> Le fil de départ, seul.'],[12,'<b>5 Promi.</b>'],[37,'<b>30 Promi.</b>']].forEach(function(z,ix){
    cadre(rB,400,m_peintFil,{id:'b-'+ix, nfils:z[0], gestes:m_gestes(9,17),
      col:rampe(COLS), ncol:COLS.length},z[1]);
  });
  var rB2=rang('','','duo');
  cadre(rB2,620,m_peintFil,{id:'b-grand', nfils:37, gestes:m_gestes(9,17),
    col:rampe(COLS), ncol:COLS.length},'<b>B, en grand.</b> Trente Promi.');
  cadre(rB2,620,m_peintFil,{id:'b-vide-grand', nfils:7, gestes:m_gestes(9,17),
    col:rampe(COLS), ncol:COLS.length},'<b>B, à vide, en grand.</b>');

  /* ── C ───────────────────────────────────────────────────────────────── */
  var rC=rang('C · A, à fond perdu',
    'La même matière que A, <b>sans contour</b> : elle occupe l’écran d’un bord à l’autre. '+
    'Sept des douze refus portaient sur le bord entre l’objet et le fond — il faut savoir si '+
    'le supprimer règle le problème au lieu de le résoudre.','tri');
  [[0,'<b>Vide.</b>'],[5,'<b>5 Promi.</b>'],[30,'<b>30 Promi.</b>']].forEach(function(z){
    var J=jeu(z[0]);
    cadre(rC,400,m_peintMatiere,{id:'c-'+z[0], plein:true, gestes:m_gestes(9,17),
      iles:J.iles, col:rampe(J.src), ncol:J.ncol},z[1]);
  });
  var rC2=rang('','','duo');
  cadre(rC2,620,m_peintMatiere,{id:'c-grand', plein:true, gestes:m_gestes(9,17),
    iles:J30.iles, col:rampe(J30.src), ncol:J30.ncol},'<b>C, en grand.</b>');
  cadre(rC2,620,m_peintMatiere,{id:'c-vide-grand', plein:true, gestes:m_gestes(9,17),
    iles:J0.iles, col:rampe(J0.src), ncol:J0.ncol},'<b>C, à vide, en grand.</b>');

  /* ── L'EPREUVE DU PARTAGE ────────────────────────────────────────────── */
  var rS=rang('L’épreuve du partage — 200 px',
    'Si ça ne tient pas là, ça ne tient pas dans une image partagée.','tri');
  cadre(rS,200,m_peintMatiere,{id:'s-a', gestes:m_gestes(9,17),
    iles:J30.iles, col:rampe(J30.src), ncol:J30.ncol},'<b>A</b>');
  cadre(rS,200,m_peintFil,{id:'s-b', nfils:37, gestes:m_gestes(9,17),
    col:rampe(COLS), ncol:COLS.length},'<b>B</b>');
  cadre(rS,200,m_peintMatiere,{id:'s-c', plein:true, gestes:m_gestes(9,17),
    iles:J30.iles, col:rampe(J30.src), ncol:J30.ncol},'<b>C</b>');

  window.__pret=true;
}
})();
