/* ⚑ LE DOIGT CREUSE FRANCHEMENT, ET LA TRACE RESTE.
   Chaque contact pousse la matière RADIALEMENT, dans tous les sens à partir du point
   touché — et fort : quarante-six pixels au cœur, sur un rayon de soixante-dix-huit.
   La matière FUIT, on voit le trou s'ouvrir.
   ⚠ ELLE GLISSE SUR LA SURFACE, elle ne quitte pas la boule : un point poussé au-delà
   de la silhouette est ramené dessus. C'est ce qui permet de creuser fort sans mordre
   le bord — la première version à 72/30 cassait la silhouette et on voyait un objet
   mordu, pas un objet qui encaisse.
   LA TRACE DURE : après le lâcher, exp(−t/1,35) — cinq secondes avant de disparaître.
   ET ELLE SE COMBLE QUAND ON LANCE : la matière qui file par-dessus la remplit,
   proportionnellement à la vitesse. On creuse, on lance, ça se rebouche. */
var IMP_R=78, IMP_A=46, IMP_TAU=1.35, IMP_MONTE=0.09, IMP_MAX=6, IMP_COMBLE=0.42;
function majImpacts(f,now,dt,aom){
  var L=f.__imp; if(!L||!L.length) return 0;
  var n=0;
  for(var i=0;i<L.length;i++){
    var m=L[i];
    if(m.tr===0) m.e=Math.min(1,(now-m.t0)/1000/IMP_MONTE);
    else {
      m.e=m.eRel*Math.exp(-(now-m.tr)/1000/IMP_TAU);
      /* ⚑ LE COMBLEMENT PAR LA VITESSE — on retranche, on ne remplace pas :
         un creux qu'on lance se rebouche d'autant plus vite qu'on lance fort. */
      m.comble=(m.comble||0)+IMP_COMBLE*aom*dt;
      m.e=Math.max(0,m.e-m.comble);
    }
    /* on ne jette que ce qui est LÂCHÉ ET ÉTEINT : un creux naissant vaut zéro à sa
       première image, le jeter là c'est ne jamais rien creuser. */
    if(m.tr===0 || m.e>0.02) L[n++]=m;
  }
  L.length=n;
  return n;
}
function dessineMasse(f,lac,tan,om){
  var GS=f.__masG; if(!GS) return;
  tampons(GS);
  var ATL=faitAtlas(f.__ink);
  var A=fabriqueMasse(), N=A.length/5, S=_seaux, cpt=_cpt;
  for(var z0=0;z0<cpt.length;z0++) cpt[z0]=0;
  var ret=Math.max(-LAG_MAX,Math.min(LAG_MAX,(om||0)*LAG_K));
  var LC=_lc, LS=_ls;
  for(var L=0;L<LAG_N;L++){ var a2=lac-ret*(L/(LAG_N-1)); LC[L]=Math.cos(a2); LS[L]=Math.sin(a2); }
  var CT=Math.cos(tan), ST=Math.sin(tan);
  var CX=MAS_BOX/2, CY=MAS_BOX/2, R=MAS_R, F=MAS_FOC, W=MAS_BOX*MAS_D, MARGE=13;
  var aom=Math.abs(om||0);
  var now=performance.now(), dt=Math.min(0.05,(now-(f.__tm||now))/1000); f.__tm=now;
  var nImp=majImpacts(f, now, dt, aom), IMPS=f.__imp;
  /* la silhouette, en pixels d'appareil : la matière glisse dessus, jamais dehors */
  var SIL=0;
  for(var zt=-1;zt<=1.0001;zt+=0.02){
    var xy=Math.sqrt(Math.max(0,1-zt*zt))*R, kk=F/(F-zt*R);
    if(xy*kk>SIL) SIL=xy*kk;
  }
  SIL*=MAS_D;
  var CXD=CX*MAS_D, CYD=CY*MAS_D;
  /* ⚑ LA TRAÎNÉE SUIT LE VRAI CHEMIN DU GRAIN — pas une direction reconstruite.
     On garde la position de l'image précédente et on tamponne LE LONG du segment
     réellement parcouru. Rotation, cisaillement du retard, poussée du doigt : tout y
     est, par construction. L'ancienne version orientait le grain sur la dérivée de la
     rotation SEULE — le doigt poussait la matière dans un sens et la traînée pointait
     dans un autre. C'était ça, l'effet plaqué. */
  var PR=f.__prev;
  if(!PR || PR.length<N*2){ PR=f.__prev=new Float32Array(N*2); f.__prevOK=false; }
  var ok=f.__prevOK;
  var saut=(aom>1.6?2:1);
  for(var i2=0;i2<N;i2++){
    var o=i2*5, t, lg=A[o+3], c=LC[lg], s=LS[lg];
    var X=A[o]*c+A[o+2]*s, Zs=-A[o]*s+A[o+2]*c;
    t=A[o+1]*CT-Zs*ST; var Z=A[o+1]*ST+Zs*CT, Y=t;
    var k=F/(F-Z*R);
    var zz=(Z+1)*0.5;
    var b=(zz*MAS_NS)|0; if(b>=MAS_NS)b=MAS_NS-1; if(b<0)b=0;
    var tr2=(zz*MAS_TR)|0; if(tr2>=MAS_TR)tr2=MAS_TR-1; if(tr2<0)tr2=0;
    var px=CXD+X*R*k*MAS_D, py=CYD+Y*R*k*MAS_D;
    for(var m2=0;m2<nImp;m2++){
      var im=IMPS[m2]; if(im.e<=0) continue;
      var ddx=px-im.x, ddy=py-im.y, d2=ddx*ddx+ddy*ddy;
      if(d2>im.r2) continue;
      var dd=Math.sqrt(d2); if(dd<0.5) continue;
      var u=1-dd/im.r, ff=u*(0.5+0.5*u);
      var pu=IMP_A*MAS_D*im.e*ff;
      px+=ddx/dd*pu; py+=ddy/dd*pu;
    }
    /* elle glisse sur la boule, elle n'en sort pas */
    var rx=px-CXD, ry=py-CYD, rr2=rx*rx+ry*ry;
    if(rr2>SIL*SIL){ var rn=SIL/Math.sqrt(rr2); px=CXD+rx*rn; py=CYD+ry*rn; }
    var j2=i2*2, dx=0, dy=0;
    if(ok){ dx=px-PR[j2]; dy=py-PR[j2+1]; }
    PR[j2]=px; PR[j2+1]=py;
    var xi=px|0, yi=py|0;
    if(xi<MARGE||yi<MARGE||xi>W-MARGE||yi>W-MARGE) continue;
    var idx=tr2*MAS_NS+b, p=cpt[idx]*5, T=S[idx];
    T[p]=xi; T[p+1]=yi;
    T[p+2]=((A[o+4]*GR_TAI+ (A[o+4]===0?0:0))|0);   /* placeholder, réécrit dessous */
    T[p+2]=((((i2*2654435761)>>>0)%GR_N)*GR_TAI + A[o+4])*MAS_NS + b;
    T[p+3]=dx; T[p+4]=dy;
    cpt[idx]++;
  }
  f.__prevOK=true;
  for(var h=0;h<MAS_TR;h++){
    var B=_tamp[h]; B.fill(0);
    for(var b2=0;b2<MAS_NS;b2++){
      var id2=h*MAS_NS+b2, n2=cpt[id2]; if(!n2) continue;
      var pas=(b2<3?2:1)*saut;
      var T2=S[id2];
      /* le tampon de la traînée : même dalle, deux niveaux plus sourde */
      var bTr=b2>=2?b2-2:0;
      for(var j=0;j<n2;j+=pas){
        var p2=j*5, si=T2[p2+2], sp=ATL[si];
        if(!sp) continue;
        var bas=T2[p2+1]*W+T2[p2], of=sp.off, va=sp.val, nn=sp.n, q2, o3, v;
        /* d'abord le chemin parcouru : des tampons ÉCHELONNÉS le long du segment */
        var ddx2=T2[p2+3], ddy2=T2[p2+4];
        var lon=Math.sqrt(ddx2*ddx2+ddy2*ddy2);
        if(lon>2.6){
          var nt=lon/2.6; if(nt>5)nt=5; nt=nt|0;
          var spT=ATL[si-b2+bTr];
          if(spT){
            var ofT=spT.off, vaT=spT.val, nT=spT.n;
            for(var q3=1;q3<=nt;q3++){
              var fr2=q3/(nt+1);
              var bx=(T2[p2]-ddx2*fr2)|0, by=(T2[p2+1]-ddy2*fr2)|0;
              if(bx<MARGE||by<MARGE||bx>W-MARGE||by>W-MARGE) continue;
              var bt=by*W+bx;
              for(q2=0;q2<nT;q2++){
                o3=bt+ofT[q2]; v=vaT[q2];
                if((v>>>24) > (B[o3]>>>24)) B[o3]=v;
              }
            }
          }
        }
        for(q2=0;q2<nn;q2++){
          o3=bas+of[q2]; v=va[q2];
          if((v>>>24) > (B[o3]>>>24)) B[o3]=v;
        }
      }
    }
  }
}
