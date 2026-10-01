/* ── LE PEINTRE : une orbite dans un cadre ────────────────────────────────── */
function peint(cv, o){
  var CSS=o.css||480, W=CSS*D;
  cv.width=W; cv.height=W;
  var g=cv.getContext('2d');
  var im=g.createImageData(W,W), B=new Uint32Array(im.data.buffer);
  var NIV=o.niv||8, TAI=o.tailles||[2.0,2.8,3.8], TN=o.teintes.length;
  var A=lieTampons(o.atlas,W);
  var R=CSS*(o.R||0.335)*D, FOC=o.foc||(R*4.6);   /* le relief gonfle jusqu'à 1,25 : la boule
                                                     doit tenir dans le cadre avec son relief */
  var CX=W/2, CY=W/2;
  var P=semis(o.mode, o.n, o);
  var lac=o.lac||0, tan=o.tan||0.34;
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var pts=[], i, t0=performance.now();
  for(i=0;i<P.length;i++){
    var x=P[i][0], y=P[i][1], z=P[i][2];
    /* LE RELIEF : le rayon suit une surface, pas une boule */
    var rr=o.relief?relief(x,y,z,o.relief):1;
    /* LE CREUX : une main a appuyé là, et la SURFACE s'est enfoncée */
    if(o.creux){
      var cx0=o.creux[0], cy0=o.creux[1], cz0=o.creux[2];
      var dd=Math.hypot(x-cx0,y-cy0,z-cz0);
      if(dd<o.creux[3]){ var u=1-dd/o.creux[3]; rr-=o.creux[4]*u*u*(3-2*u); }
    }
    /* la NORMALE de la surface déformée, par différences finies */
    var nx=x, ny=y, nz=z;
    if(o.relief){
      var e=0.02;
      var gx=(relief(x+e,y,z,o.relief)-relief(x-e,y,z,o.relief))/(2*e);
      var gy=(relief(x,y+e,z,o.relief)-relief(x,y-e,z,o.relief))/(2*e);
      var gz=(relief(x,y,z+e,o.relief)-relief(x,y,z-e,o.relief))/(2*e);
      nx=x*rr+gx*0.42; ny=y*rr+gy*0.42; nz=z*rr+gz*0.42;
      var nn=Math.hypot(nx,ny,nz)||1; nx/=nn; ny/=nn; nz/=nn;
    }
    var X=x*rr, Y=y*rr, Z=z*rr;
    /* la vue */
    var X2=X*cl+Z*sl, Z2=-X*sl+Z*cl, Y2=Y*ct-Z2*st; Z2=Y*st+Z2*ct;
    var NX=nx*cl+nz*sl, NZ2=-nx*sl+nz*cl, NY=ny*ct-NZ2*st; NZ2=ny*st+NZ2*ct;
    if(o.dosCache && NZ2<-0.05) continue;          /* on ne voit pas le dos */
    var k=FOC/(FOC-Z2*R);
    var px=(CX+X2*R*k)|0, py=(CY+Y2*R*k)|0;
    if(px<8||py<8||px>W-8||py>W-8) continue;
    /* LE NIVEAU : la profondeur */
    var zz=(Z2+1)*0.5, niv=(zz*NIV)|0; if(niv>=NIV)niv=NIV-1; if(niv<0)niv=0;
    /* LA TAILLE : plus près, plus gros */
    var tai=(zz*TAI.length)|0; if(tai>=TAI.length)tai=TAI.length-1; if(tai<0)tai=0;
    if(o.taiFixe!==undefined) tai=o.taiFixe;
    /* ⚑ LA TEINTE — LA FLAQUE D'ESSENCE.
       Elle ne vient pas de la position mais de l'ORIENTATION : l'angle entre la
       normale de la surface et le regard. Comme un film d'huile, la teinte tourne
       quand la surface se penche — bleu de face, mauve de trois quarts, menthe au
       ras du bord. Chaque point porte UN aplat de teinte : la variation naît du
       VOISINAGE, jamais d'un dégradé. */
    var ti=0;
    if(TN>1){
      var f=Math.abs(NZ2);
      /* deux termes : l'INCLINAISON (le bord vire) et l'ORIENTATION dans le plan
         (la face n'est pas d'un seul bleu — elle a des plaques). C'est ce qui fait
         la flaque : une teinte qui tourne avec la pente, pas avec la position. */
      var v=(o.iriPhase||0) + (o.iriK||3.1)*Math.pow(1-f,o.iriP||1.7)
            + (o.iriM||0)*(NX*0.74+NY*0.52);
      ti=((v*TN)|0)%TN; if(ti<0)ti+=TN;
    }
    var sp=A[(ti*TAI.length+tai)*NIV+niv];
    if(!sp) continue;
    pts.push(py*W+px, sp.n, ti*TAI.length*NIV+tai*NIV+niv);
  }
  /* le versement */
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
