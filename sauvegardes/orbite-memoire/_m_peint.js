/* ════════════════════════════════════════════════════════════════════════════
   LES TROIS PEINTRES — canvas 2D reel, aucune 3D, aucun shader.

   A · LA MEMOIRE DE LA MAIN   une matiere minerale, et le poli des gestes
   B · LE FIL                  le cumul des trajets d'un fil, et leur moire
   C · A, A FOND PERDU         le meme A, sans contour, plein cadre

   ⚑ COMMENT ON PEINT SANS DEGRADE, SANS OMBRE ET SANS TACHE SPECULAIRE.
   Chaque marque est UN APLAT FRANC, pris dans une rampe de vingt marches. Le
   volume ne vient donc pas d'un fondu : il vient DU NOMBRE de marques et de la
   marche que chacune prend. C'est la regle du moteur de la Toile, appliquee a
   la lettre — et c'est aussi ce qui empeche le « plastique ».
   ⚠ On garde LE PLUS OPAQUE au versement, jamais « le dernier pose » : acquis
   du lot precedent, ou cette seule ligne creait un degrade directionnel de
   49 contre 83 de luminance a couverture egale.
   ════════════════════════════════════════════════════════════════════════════ */

/* ── LE GRAIN MINERAL — une facette, pas un poil ──────────────────────────
   Un losange plat, legerement irregulier. C'est la forme qui dit « pierre
   tendre » plutot que « pelage » : des faces, des aretes, aucune pointe. */
function GRAIN_FACETTE(g,e,v){
  var s=(v||0)%3;
  var a=[[1.00,0.42],[0.86,0.55],[1.10,0.34]][s];
  var L=e*a[0], W=e*a[1];
  g.beginPath();
  g.moveTo(-L,0); g.lineTo(-L*0.18,-W); g.lineTo(L,0); g.lineTo(L*0.22,W);
  g.closePath(); g.fill();
}
/* le grain POLI : plus fin, plus long, couche — c'est le lustre d'un geste */
/* ⚠ ET LA TRACE DOIT ETRE UN LUSTRE, PAS UN CREUX. Premiere version : le
   grain poli etait si fin qu'il couvrait moins que la matiere brute — le fond
   passait entre les marques et la trace sortait SOMBRE. Or ce qui reste d'un
   geste, ce n'est pas un creux : c'est un lustre. On l'allonge sans
   l'amincir, et il couvre donc PLUS. */
function GRAIN_POLI(g,e,v){
  var s=(v||0)%3;
  var L=e*[1.72,1.90,1.58][s], W=e*[0.34,0.29,0.39][s];
  g.beginPath();
  g.moveTo(-L,0); g.lineTo(-L*0.10,-W); g.lineTo(L,0); g.lineTo(L*0.12,W);
  g.closePath(); g.fill();
}

/* ── LE VERSEMENT — on garde le plus opaque ─────────────────────────────── */
function m_verse(A,COL,L,n,B){
  var OF=A.__off, AL=A.__alp, ST=A.__sta;
  for(var i=0;i<n;i+=3){
    var t=L[i+1], a=ST[t], b2=ST[t+1], bas=L[i], col=COL[L[i+2]];
    for(var j=a;j<b2;j++){
      var o=bas+OF[j], v=(AL[j]|col)>>>0;
      if(v>B[o]) B[o]=v;
    }
  }
}

var M_ORI=28, M_NIV=6, M_NVAR=3;

/* ════════════════════════════════════════════════════════════════════════════
   A ET C — LA MATIERE MINERALE
   `o.plein` : false = une sphere posee dans le cadre (A)
               true  = la matiere occupe tout le cadre (C, a fond perdu)
   ════════════════════════════════════════════════════════════════════════════ */
function m_peintMatiere(cv,o){
  var CSS=o.css||620, DPR=Math.min(2,window.devicePixelRatio||1);
  var W=Math.round(CSS*DPR);
  cv.width=W; cv.height=W;
  cv.style.width=CSS+'px'; cv.style.height=CSS+'px';
  var g=cv.getContext('2d');
  g.fillStyle=o.fond||'#16171B'; g.fillRect(0,0,W,W);

  var R=W*(o.plein?1.02:0.472);
  var CX=W/2, CY=W/2;
  var P=o.semis, N=P.length/3, G=o.gestes, IL=o.iles||[];
  var COL=o.col, NCOL=o.ncol;

  /* le repere de la vue : on regarde l'objet legerement de trois quarts */
  var lac=o.lac==null?0.9:o.lac, tan=o.tan==null?0.26:o.tan;
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var LX=-0.44, LY=-0.62, LZ=0.65;                 /* la cle, en repere de vue */

  var off=cv.__off;
  if(!off||off.width!==W){ off=cv.__off=document.createElement('canvas');
    off.width=W; off.height=W; cv.__og=off.getContext('2d');
    cv.__im=cv.__og.createImageData(W,W);
    cv.__B=new Uint32Array(cv.__im.data.buffer); }
  var B=cv.__B; B.fill(0);

  var AF=lieTampons(o.atlasF,W), AP=lieTampons(o.atlasP,W);
  var TAI=o.tailles, NT=TAI.length;
  var LF=new Int32Array(N*3), LP=new Int32Array(N*3), nf=0, np=0;
  var MAR=MARCHES;

  for(var i=0;i<N;i++){
    var x=P[i*3], y=P[i*3+1], z=P[i*3+2];
    /* rotation de vue */
    var X=x*cl+z*sl, Zt=-x*sl+z*cl, Y=y*ct-Zt*st, Z=y*st+Zt*ct;
    if(Z<0) continue;                              /* le dos n'est pas visite */
    var px=(CX+X*R)|0, py=(CY+Y*R)|0;
    if(px<3||py<3||px>=W-3||py>=W-3) continue;

    /* ── LA LUMIERE : aucune tache, aucun fondu. Une marche, et c'est tout. */
    var dl=X*LX+Y*LY+Z*LZ; if(dl<0)dl=0;
    var lum=0.40+0.46*p074(dl)+0.16*Z*Z;
    /* le limbe : la matiere s'y voit de biais, elle rend moins — c'est ce qui
       dessine le contour SANS lisere lumineux (interdit : pas de speculaire) */
    lum*=0.55+0.45*Z;

    /* ── LE POLI DES GESTES ─────────────────────────────────────────────── */
    var po=G?m_poli(G,x,y,z):0;

    /* ── L'APPARTENANCE A UNE DALLE ─────────────────────────────────────── */
    var ci=0, dal=null;
    for(var k=0;k<IL.length;k++){
      var I=IL[k]; if(!I.m) continue;
      var dp=x*I.c[0]+y*I.c[1]+z*I.c[2];
      if(dp<0.93) continue;
      var u=x*I.e1[0]+y*I.e1[1]+z*I.e1[2];
      var v=x*I.e2[0]+y*I.e2[1]+z*I.e2[2];
      var tx=(u*I.kk+I.sx)|0, ty=(v*I.kk+I.sy)|0;
      if(tx<0||ty<0||tx>=I.mw||ty>=I.mh) continue;
      var mm=I.m[ty*I.mw+tx];
      if(mm){ ci=mm; dal=I; break; }
    }

    /* ⚑ LA CHROMA MONTE AVEC LE POLI — c'est ca, la trace qui reste.
       Pas un creux : la matiere travaillee est plus dense, donc plus saturee
       et d'un ton plus haut. On decale simplement de marche. */
    var mar=(lum*(MAR-4)+2.4+po*4.6)|0;
    if(mar<0)mar=0; if(mar>MAR-1)mar=MAR-1;

    /* ── LE SENS DE LA MARQUE ───────────────────────────────────────────── */
    var vx,vy,vz;
    if(po>0.12 && G){
      /* le geste couche la matiere dans SON sens */
      var gg=null, bd=9;
      for(var q=0;q<G.length;q++){
        var t2=Math.atan2(x*G[q].d[0]+y*G[q].d[1]+z*G[q].d[2],
                          x*G[q].a[0]+y*G[q].a[1]+z*G[q].a[2]);
        if(t2<0)t2=0; else if(t2>G[q].L)t2=G[q].L;
        var ct2=Math.cos(t2), st2=Math.sin(t2);
        var qx=G[q].a[0]*ct2+G[q].d[0]*st2, qy=G[q].a[1]*ct2+G[q].d[1]*st2,
            qz=G[q].a[2]*ct2+G[q].d[2]*st2;
        var d2=x*qx+y*qy+z*qz; if(d2>1)d2=1;
        var an2=Math.acos(d2);
        if(an2<bd){bd=an2;gg=G[q];}
      }
      if(gg){
        /* la tangente du geste au point courant */
        var tx2=gg.d[0]-(gg.d[0]*x+gg.d[1]*y+gg.d[2]*z)*x;
        var ty2=gg.d[1]-(gg.d[0]*x+gg.d[1]*y+gg.d[2]*z)*y;
        var tz2=gg.d[2]-(gg.d[0]*x+gg.d[1]*y+gg.d[2]*z)*z;
        var mt=Math.hypot(tx2,ty2,tz2)||1;
        vx=tx2/mt; vy=ty2/mt; vz=tz2/mt;
      }
    }
    if(vx===undefined){ var ve=m_veine(x,y,z); vx=ve[0]; vy=ve[1]; vz=ve[2]; }

    var fX=vx*cl+vz*sl, fZt=-vx*sl+vz*cl, fY=vy*ct-fZt*st;
    var ori=secteur(fX,fY,M_ORI)*M_NVAR+(i%M_NVAR);

    /* la taille : la matiere polie a un grain plus FIN */
    var tai=(Z*NT)|0; if(tai>=NT)tai=NT-1; if(tai<0)tai=0;
    if(po>0.35 && tai>0) tai--;
    var niv=((0.55+0.45*Z)*M_NIV)|0; if(niv>=M_NIV)niv=M_NIV-1; if(niv<0)niv=0;

    var idx=(tai*M_ORI*M_NVAR+ori)*M_NIV+niv;
    var bas=py*W+px, cc=ci*MAR+mar;
    if(po>0.30){ LP[np]=bas; LP[np+1]=idx; LP[np+2]=cc; np+=3; }
    else       { LF[nf]=bas; LF[nf+1]=idx; LF[nf+2]=cc; nf+=3; }
  }
  m_verse(AF,COL,LF,nf,B);
  m_verse(AP,COL,LP,np,B);
  cv.__og.putImageData(cv.__im,0,0);
  g.drawImage(off,0,0);
  return {n:(nf+np)/3};
}

/* ════════════════════════════════════════════════════════════════════════════
   B — LE FIL
   L'objet est le CUMUL des trajets d'un fil autour du Noyau. Ce qu'on voit
   n'est aucun fil en particulier : c'est le MOIRE qu'ils forment ensemble.
   Chaque Promi ajoute un trajet ; le trajet ne s'efface jamais.
   ⚠ Aucun degrade : chaque segment est d'un aplat pris dans la rampe.
   ════════════════════════════════════════════════════════════════════════════ */
function m_peintFil(cv,o){
  var CSS=o.css||620, DPR=Math.min(2,window.devicePixelRatio||1);
  var W=Math.round(CSS*DPR);
  cv.width=W; cv.height=W;
  cv.style.width=CSS+'px'; cv.style.height=CSS+'px';
  var g=cv.getContext('2d');
  g.fillStyle=o.fond||'#16171B'; g.fillRect(0,0,W,W);
  var R=W*0.455, CX=W/2, CY=W/2;
  var COL=o.col, MAR=MARCHES, NF=o.nfils, G=o.gestes;
  var lac=o.lac==null?0.9:o.lac, tan=o.tan==null?0.26:o.tan;
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  g.lineCap='butt'; g.lineJoin='round';

  for(var f=0;f<NF;f++){
    var s=f*131+7;
    /* un trajet = une geodesique inclinee, refermee sur elle-meme, qui frole
       le Noyau sans jamais y entrer : c'est le fil qui tourne autour de soi */
    var F=m_fil(f);
    var ci=(m_h(s*11+5)*(o.ncol-1)+1)|0;
    var PAS=260;
    var lw=(0.9+m_h(s*13+7)*0.8)*DPR;
    for(var i=0;i<PAS;i++){
      var t0=i/PAS*6.283185, t1=(i+1)/PAS*6.283185;
      var p0=m_pointFil(t0,F), p1=m_pointFil(t1,F);
      var A0=m_proj(p0,cl,sl,ct,st), A1=m_proj(p1,cl,sl,ct,st);
      if(A0[2]<0&&A1[2]<0) continue;              /* le dos ne se peint pas */
      /* la marche : la profondeur et le poli des gestes, rien d'autre */
      var zz=(A0[2]+A1[2])*0.5;
      var po=G?m_poli(G,p0[0],p0[1],p0[2]):0;
      var mar=(0.30+0.52*Math.max(0,zz))*(MAR-4)+2+po*3.4;
      mar=mar|0; if(mar<0)mar=0; if(mar>MAR-1)mar=MAR-1;
      var c=COL[ci*MAR+mar];
      g.strokeStyle='rgb('+(c&255)+','+((c>>8)&255)+','+((c>>16)&255)+')';
      g.lineWidth=lw*(0.55+0.45*Math.max(0,zz));
      g.beginPath();
      g.moveTo(CX+A0[0]*R, CY+A0[1]*R);
      g.lineTo(CX+A1[0]*R, CY+A1[1]*R);
      g.stroke();
    }
  }
  return {n:NF};
}
/* ⚑ UN FIL EST UN PETIT CERCLE SUR LA SPHERE, PAS UN GRAND.
   Premiere version : je construisais un point puis je le NORMALISAIS. Or
   normaliser un point du plan (e1,e2) rend toujours le meme GRAND cercle,
   quels que soient le rayon et l'aplatissement — tous les fils passaient donc
   par les deux memes poles et convergeaient en un point. On construit
   maintenant le cercle DIRECTEMENT sur la sphere : un axe, une hauteur, et le
   rayon qui va avec (c² + r² = 1). Des cercles de tailles et d'inclinaisons
   differentes : c'est ca, un echeveau. */
function m_fil(k){
  var s=k*131+7;
  var u=m_h(s*3+1)*2-1, ph=m_h(s*5+2)*6.283185, rr=Math.sqrt(Math.max(0,1-u*u));
  var n=[Math.cos(ph)*rr, u, Math.sin(ph)*rr];              /* l'axe du cercle */
  var hx=0,hy=1,hz=0; if(Math.abs(n[1])>0.9){hx=1;hy=0;}
  var e1=[n[1]*hz-n[2]*hy, n[2]*hx-n[0]*hz, n[0]*hy-n[1]*hx];
  var m1=Math.hypot(e1[0],e1[1],e1[2])||1; e1=[e1[0]/m1,e1[1]/m1,e1[2]/m1];
  var e2=[n[1]*e1[2]-n[2]*e1[1], n[2]*e1[0]-n[0]*e1[2], n[0]*e1[1]-n[1]*e1[0]];
  var c=(m_h(s*7+3)-0.5)*1.28;                              /* la hauteur */
  var r=Math.sqrt(Math.max(0.02,1-c*c));
  return {n:n,e1:e1,e2:e2,c:c,r:r};
}
function m_pointFil(t,F){
  var ct=Math.cos(t), st=Math.sin(t);
  return [F.c*F.n[0]+F.r*(F.e1[0]*ct+F.e2[0]*st),
          F.c*F.n[1]+F.r*(F.e1[1]*ct+F.e2[1]*st),
          F.c*F.n[2]+F.r*(F.e1[2]*ct+F.e2[2]*st)];
}
function m_proj(p,cl,sl,ct,st){
  var X=p[0]*cl+p[2]*sl, Zt=-p[0]*sl+p[2]*cl;
  return [X, p[1]*ct-Zt*st, p[1]*st+Zt*ct];
}
