/* ════════════════════════════════════════════════════════════════════════════
   LE MOTEUR DES PLANCHES — le même que la version animée :
   des tampons pré-rendus, versés dans un tampon de pixels, un putImageData.
   Rien n'est dessiné avec drawImage : mesuré hors budget d'un facteur trois.
   Tout ce qui suit est donc TENABLE à 60 images par seconde.
   ════════════════════════════════════════════════════════════════════════════ */
var D=2;                         /* pixels d'appareil par pixel CSS */

/* ── L'ATLAS : un grain, N teintes, 3 tailles, 8 niveaux de profondeur ────── */
function atlasRond(teintes, tailles, NIV, a0, a1){
  var cv=document.createElement('canvas'); cv.width=40; cv.height=40;
  var g=cv.getContext('2d'), A=[];
  for(var t=0;t<teintes.length;t++){
    var rgb=teintes[t];
    for(var s=0;s<tailles.length;s++){
      var ep=tailles[s];
      g.clearRect(0,0,40,40);
      g.fillStyle='#fff'; g.beginPath(); g.arc(20,20,ep/2,0,6.2832); g.fill();
      var d=g.getImageData(0,0,40,40).data;
      var x1=40,y1=40,x2=-1,y2=-1;
      for(var y=0;y<40;y++)for(var x=0;x<40;x++) if(d[(y*40+x)*4+3]>3){
        if(x<x1)x1=x; if(x>x2)x2=x; if(y<y1)y1=y; if(y>y2)y2=y; }
      if(x2<0){x1=y1=20;x2=y2=20;}
      var w=x2-x1+1, h=y2-y1+1, ox=20-x1, oy=20-y1;
      for(var n=0;n<NIV;n++){
        var q=(n+0.5)/NIV, mul=a0+(a1-a0)*q*q;
        A.push(fabTampon(d,40,x1,y1,w,h,ox,oy,mul,rgb));
      }
    }
  }
  return A;
}
function fabTampon(dat,src,x1,y1,w,h,ox,oy,mul,rgb){
  var Wd=0; /* rempli plus tard par lieTampons */
  var offs=[], vals=[];
  for(var y=0;y<h;y++)for(var x=0;x<w;x++){
    var al=(dat[((y1+y)*src+(x1+x))*4+3]*mul)|0;
    if(al>3){ offs.push([y-oy,x-ox]); vals.push(al); }
  }
  return {rel:offs, al:vals, rgb:rgb};
}
/* on lie les tampons à la largeur du tampon de destination */
function lieTampons(A,W){
  for(var i=0;i<A.length;i++){
    var t=A[i]; if(t.off && t.W===W) continue;
    var n=t.rel.length, off=new Int32Array(n), val=new Uint32Array(n);
    for(var j=0;j<n;j++){
      off[j]=t.rel[j][0]*W+t.rel[j][1];
      val[j]=(((t.al[j]&255)<<24)|((t.rgb[2]&255)<<16)|((t.rgb[1]&255)<<8)|(t.rgb[0]&255))>>>0;
    }
    t.off=off; t.val=val; t.n=n; t.W=W;
  }
  return A;
}
/* ── LA TEINTE : une rampe FRANCHE, jamais un dégradé ─────────────────────── */
function rampe(cles, n){
  /* cles = [[r,g,b], ...] ; on rend n teintes réparties, chacune un APLAT.
     ⚠ n=1 ou une seule clé : i/(n-1) vaut 0/0. On sort avant. */
  if(n<=1 || cles.length===1) return [cles[0].slice()];
  var out=[];
  for(var i=0;i<n;i++){
    var t=i/(n-1)*(cles.length-1), k=Math.min(cles.length-2,t|0), f=t-k;
    out.push([Math.round(cles[k][0]+(cles[k+1][0]-cles[k][0])*f),
              Math.round(cles[k][1]+(cles[k+1][1]-cles[k][1])*f),
              Math.round(cles[k][2]+(cles[k+1][2]-cles[k][2])*f)]);
  }
  return out;
}
var CL_CREME=[[244,238,225]];
var CL_ESSENCE=[[58,84,255],[138,92,240],[143,160,255],[43,232,140],[58,84,255]];
var CL_NUIT   =[[58,84,255],[138,92,240],[244,238,225]];

/* ── LE RELIEF : le rayon n'est plus constant ─────────────────────────────── */
function relief(x,y,z,R){
  var s=0;
  for(var i=0;i<R.length;i++){
    var h=R[i];
    s+=h[0]*Math.sin(h[1]*x+h[4])*Math.sin(h[2]*y+h[5])*Math.cos(h[3]*z+h[6]);
  }
  return 1+s;
}
/* ── LA SEMENCE : où sont les points ──────────────────────────────────────── */
function semis(mode,N,par){
  var P=[], i, fr=function(v){return v-Math.floor(v);};
  if(mode==='fibo'){
    for(i=0;i<N;i++){
      var y=1-2*(i+0.5)/N, rr=Math.sqrt(Math.max(0,1-y*y)), ph=i*2.399963229728653;
      P.push([Math.cos(ph)*rr, y, Math.sin(ph)*rr]);
    }
  } else if(mode==='fils'){
    var F=par.fils||30, M=Math.round(N/F), T=par.tours||[9,11,8,12,10,7,13];
    for(var k=0;k<F;k++){
      var d1=(par.dev||0.34)*(2*fr(k*0.618033988)-1), d2=fr(k*0.754877666)*6.2832;
      var ax=Math.sin(d1)*Math.cos(d2), ay=Math.cos(d1), az=Math.sin(d1)*Math.sin(d2);
      var p1x=-az, p1z=ax, pn=Math.hypot(p1x,p1z)||1; p1x/=pn; p1z/=pn;
      var p2x=ay*p1z, p2y=az*p1x-ax*p1z, p2z=-ay*p1x;
      var Nn=T[k%T.length], ph2=fr(k*0.414213562)*6.2832;
      for(i=0;i<M;i++){
        var s=i/M, yy=1-2*s, r2=Math.sqrt(Math.max(0,1-yy*yy));
        var th=s*Nn*6.2832+ph2, c=Math.cos(th)*r2, s3=Math.sin(th)*r2;
        P.push([ax*yy+p1x*c+p2x*s3, ay*yy+p1z*0+p2y*s3, az*yy+p1z*c+p2z*s3]);
      }
    }
  } else if(mode==='latitudes'){
    var L=par.lignes||46;
    for(var l=0;l<L;l++){
      var yy2=-1+2*(l+0.5)/L, r3=Math.sqrt(Math.max(0,1-yy2*yy2));
      var nb=Math.max(6,Math.round(N/L*r3*1.5));
      for(i=0;i<nb;i++){
        var a=i/nb*6.2832+l*0.7;
        P.push([Math.cos(a)*r3, yy2, Math.sin(a)*r3]);
      }
    }
  } else if(mode==='volume'){
    for(i=0;i<N;i++){
      var y3=1-2*(i+0.5)/N, r4=Math.sqrt(Math.max(0,1-y3*y3)), p3=i*2.399963229728653;
      /* ⚠ LA PROFONDEUR NE DOIT PAS SUIVRE L'INDICE. Corrélée à la spirale de
         Fibonacci, elle dessinait une ÉTOILE de rayons au centre — un artefact, pas
         une matière. Deux irrationnels différents, et l'étoile disparaît. */
      var prof=0.55+0.45*fr(i*0.7548776662+fr(i*0.2360679775)*0.5);
      var tw=fr(i*0.3819660113)*6.2832;           /* et on tord l'azimut */
      var ca=Math.cos(p3+tw*0.18), sa=Math.sin(p3+tw*0.18);
      P.push([ca*r4*prof, y3*prof, sa*r4*prof]);
    }
  }
  return P;
}
