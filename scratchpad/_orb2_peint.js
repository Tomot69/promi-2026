/* ── LE PEINTRE, version « forme composée » ───────────────────────────────── */
function peint2(cv, o){
  var CSS=o.css||480, W=CSS*D;
  cv.width=W; cv.height=W;
  var g=cv.getContext('2d');
  /* ⚑ ON PEUT PEINDRE PAR-DESSUS UNE COUCHE DÉJÀ POSÉE : le tampon garde le plus
     opaque, donc une couche plus lumineuse (le liquide) traverse une couche sourde
     (la coquille) sans l'effacer. C'est ce qui donne « vu à travers ». */
  var im=o.garde||g.createImageData(W,W), B=new Uint32Array(im.data.buffer);
  var NIV=o.niv||8, TAI=o.tailles||[2.0,2.8,3.8], TN=o.teintes.length;
  var A=lieTampons(o.atlas,W);
  var R=CSS*(o.R||0.355)*D, FOC=o.foc||(R*5.0), CX=W/2, CY=W/2;
  var P=(o.mode==='donne')?o.pts:semis(o.mode, o.n, o), F=o.forme;
  var lac=o.lac||0, tan=o.tan||0.30;
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var pts=[], i, t0=performance.now(), e=0.014;
  for(i=0;i<P.length;i++){
    var x=P[i][0], y=P[i][1], z=P[i][2], prof=P[i].length>3?P[i][3]:1;
    var hn=Math.hypot(x,y,z)||1;
    var p=F(x/hn,y/hn,z/hn);
    if(prof<0.999){ p=[p[0]*prof,p[1]*prof,p[2]*prof]; }
    else if(hn<0.999){ p=[p[0]*hn,p[1]*hn,p[2]*hn]; }   /* le semis en volume */
    /* le CREUX : la surface s'enfonce, elle ne pousse pas des points */
    if(o.creux){
      var dd=Math.hypot(p[0]-o.creux[0],p[1]-o.creux[1],p[2]-o.creux[2]);
      if(dd<o.creux[3]){ var u=1-dd/o.creux[3], f2=u*u*(3-2*u);
        var nn0=Math.hypot(p[0],p[1],p[2])||1;
        p=[p[0]*(1-o.creux[4]*f2/nn0), p[1]*(1-o.creux[4]*f2/nn0), p[2]*(1-o.creux[4]*f2/nn0)];
      }
    }
    /* LA NORMALE, par deux tangentes de la surface — exacte pour la forme composée */
    var hh=Math.sqrt(Math.max(1e-6,1-y*y));
    var a0=Math.atan2(z,x);
    var pa=F(Math.cos(a0+e)*hh, y, Math.sin(a0+e)*hh);
    var y2=Math.max(-0.999,Math.min(0.999,y+e)), h2=Math.sqrt(Math.max(1e-6,1-y2*y2));
    var pb=F(Math.cos(a0)*h2, y2, Math.sin(a0)*h2);
    var ux=pa[0]-p[0], uy=pa[1]-p[1], uz=pa[2]-p[2];
    var vx=pb[0]-p[0], vy=pb[1]-p[1], vz=pb[2]-p[2];
    var nx=uy*vz-uz*vy, ny=uz*vx-ux*vz, nz=ux*vy-uy*vx;
    var nl=Math.hypot(nx,ny,nz)||1; nx/=nl; ny/=nl; nz/=nl;
    if(nx*p[0]+ny*p[1]+nz*p[2]<0){ nx=-nx; ny=-ny; nz=-nz; }
    var X=p[0], Y=p[1], Z=p[2];
    var X2=X*cl+Z*sl, Z2=-X*sl+Z*cl, Y2=Y*ct-Z2*st; Z2=Y*st+Z2*ct;
    var NX=nx*cl+nz*sl, NZ2=-nx*sl+nz*cl, NY=ny*ct-NZ2*st; NZ2=ny*st+NZ2*ct;
    if(o.dosCache && NZ2<-0.03) continue;
    var k=FOC/(FOC-Z2*R);
    var px=(CX+X2*R*k)|0, py=(CY+Y2*R*k)|0;
    if(px<8||py<8||px>W-8||py>W-8) continue;
    var zz=(Z2+1)*0.5, niv=(zz*NIV)|0; if(niv>=NIV)niv=NIV-1; if(niv<0)niv=0;
    var tai=(zz*TAI.length)|0; if(tai>=TAI.length)tai=TAI.length-1; if(tai<0)tai=0;
    if(o.taiFixe!==undefined) tai=o.taiFixe;
    var ti=0;
    if(TN>1){
      if(o.rampe){
        /* ⚑ UNE RAMPE DIRECTIONNELLE, PAS DES FRANGES. La référence n'a pas
           d'interférences : elle a UN passage du bleu clair au violet, en diagonale.
           Mes franges d'iridescence hachaient la forme et la rendaient illisible. */
        var t=0.5+0.5*(X2*o.rampe[0]+Y2*o.rampe[1]);
        if(o.rampeBord) t=t*0.72+0.28*(1-Math.abs(NZ2));
        ti=(t*TN)|0; if(ti<0)ti=0; if(ti>=TN)ti=TN-1;
      } else {
        var f=Math.abs(NZ2);
        var v=(o.iriPhase||0)+(o.iriK||3.0)*Math.pow(1-f,o.iriP||1.6)+(o.iriM||0)*(NX*0.74+NY*0.52);
        ti=((v*TN)|0)%TN; if(ti<0)ti+=TN;
      }
    }
    var sp=A[(ti*TAI.length+tai)*NIV+niv];
    if(!sp) continue;
    pts.push(py*W+px, 0, ti*TAI.length*NIV+tai*NIV+niv);
  }
  for(i=0;i<pts.length;i+=3){
    var sp2=A[pts[i+2]], bas=pts[i], of=sp2.off, va=sp2.val;
    for(var j=0;j<sp2.n;j++){
      var oo=bas+of[j], vv=va[j];
      if((vv>>>24) > (B[oo]>>>24)) B[oo]=vv;
    }
  }
  g.putImageData(im,0,0);
  return {n:pts.length/3, ms:+(performance.now()-t0).toFixed(1)};
}
