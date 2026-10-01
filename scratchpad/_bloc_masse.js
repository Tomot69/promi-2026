/* ⚑ LE GRAIN N'EST PLUS UN PIXEL. C'est un TAMPON.
   Le carré aligné sur la grille faisait « pixel Windows 98 », et c'était la technique
   qui l'imposait : putImageData n'écrit que des entiers. On dessine donc le grain
   UNE FOIS dans un petit canevas — rond, anticrénelé, bouts ronds — on lit ses pixels,
   et on les TAMPONNE dans le tampon. Le grain a une main ; le coût ne bouge pas.
   Mesuré (scratchpad/banc5.py), quatre toiles, l'intervalle réel entre deux images :
     carré au pixel   20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,67   64 000 → 16,67
     TAMPON DE GRAIN  20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,79   64 000 → 16,79
     drawImage         20 000 → 48,55 ms   34 000 → 80,35   48 000 → 112,49  64 000 → 151,11
   drawImage par grain est hors budget d'un facteur trois — c'est l'appel qui coûte,
   pas les pixels. Le tampon, lui, ne coûte rien de plus que le carré.
   LE TAMPON GARDE LE PLUS OPAQUE (et non « le dernier ») : deux grains qui se croisent
   ne s'effacent pas l'un l'autre, le plus présent gagne. */
var GR_TAI=3, GR_ELO=4, GR_ANG=12, GR_FORMES=1+(GR_ELO-1)*GR_ANG;   /* 37 formes */
var GR_EP=[1.5,2.2,3.1];              /* trois épaisseurs de grain — la main */
var GR_LG=[0,3.2,6.4,11.5];           /* l'étirement, en pixels d'appareil */
var _atlas=null, _atlasInk=null;
function faitAtlas(ink){
  if(_atlas && _atlasInk===ink) return _atlas;
  var att=(ink===ENCRE?0.78:1);
  var cv=document.createElement('canvas'); cv.width=32; cv.height=32;
  var g=cv.getContext('2d');
  var CR=parseInt(ink.substr(1,2),16), CG=parseInt(ink.substr(3,2),16), CB=parseInt(ink.substr(5,2),16);
  var base=CB<<16|CG<<8|CR;
  var A=[];
  for(var t=0;t<GR_TAI;t++)for(var sh=0;sh<GR_FORMES;sh++){
    var lg, an, ep=GR_EP[t];
    if(sh===0){ lg=0; an=0; }
    else { var e=1+(((sh-1)/GR_ANG)|0), a=(sh-1)%GR_ANG;
           lg=GR_LG[e]*(0.78+t*0.22); an=a/GR_ANG*Math.PI; }
    g.clearRect(0,0,32,32);
    g.strokeStyle='#fff'; g.fillStyle='#fff'; g.lineCap='round'; g.lineWidth=ep;
    g.beginPath();
    if(lg<0.5){ g.arc(16,16,ep/2,0,6.2832); g.fill(); }
    else { g.moveTo(16-Math.cos(an)*lg/2,16-Math.sin(an)*lg/2);
           g.lineTo(16+Math.cos(an)*lg/2,16+Math.sin(an)*lg/2); g.stroke(); }
    var d=g.getImageData(0,0,32,32).data;
    var x1=32,y1=32,x2=-1,y2=-1;
    for(var y=0;y<32;y++)for(var x=0;x<32;x++) if(d[(y*32+x)*4+3]>3){
      if(x<x1)x1=x; if(x>x2)x2=x; if(y<y1)y1=y; if(y>y2)y2=y; }
    if(x2<0){ x1=y1=16; x2=y2=16; }
    var w=x2-x1+1, h=y2-y1+1, msk=new Uint8Array(w*h);
    for(var yy=0;yy<h;yy++)for(var xx=0;xx<w;xx++) msk[yy*w+xx]=d[((y1+yy)*32+(x1+xx))*4+3];
    /* les sept niveaux de profondeur, pré-multipliés : une seule comparaison au tampon */
    for(var n=0;n<MAS_NS;n++){
      var q=(n+0.5)/MAS_NS;
      var mul=(MAS_A0+(MAS_A1-MAS_A0)*q*q)*att;
      var u=new Uint32Array(w*h);
      for(var i=0;i<w*h;i++){ var al=(msk[i]*mul)|0; u[i]= al>2 ? ((al&255)<<24|base) : 0; }
      A.push({w:w,h:h,ox:(16-x1)|0,oy:(16-y1)|0,u:u});
    }
  }
  _atlas=A; _atlasInk=ink; window._grainsAtlas=A.length;
  return A;
}
/* ⚑ LE DOIGT CREUSE, ET LE CRATÈRE SE REFERME.
   Chaque contact pousse la matière vers l'extérieur, autour de lui. Tant que le doigt
   est posé, le creux tient ; dès qu'on lâche, il se referme en exp(−t/0,28) — la
   matière encaisse et revient. Les contacts s'EMPILENT : on peut toucher ailleurs
   tout de suite, chaque point écarte à son tour, rien ne se fige jamais. */
var IMP_R=72, IMP_A=30, IMP_TAU=0.28, IMP_MONTE=0.10, IMP_MAX=6;
function majImpacts(f,now){
  var L=f.__imp; if(!L||!L.length) return 0;
  var n=0;
  for(var i=0;i<L.length;i++){
    var m=L[i];
    if(m.tr===0) m.e=Math.min(1,(now-m.t0)/1000/IMP_MONTE);
    else m.e=m.eRel*Math.exp(-(now-m.tr)/1000/IMP_TAU);
    if(m.e>0.02){ L[n++]=m; }
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
  var CX=MAS_BOX/2, CY=MAS_BOX/2, R=MAS_R, F=MAS_FOC, W=MAS_BOX*MAS_D, MARGE=9;
  /* l'étirement : il ne naît qu'à l'accélération. Au repos le plus rapide des grains
     parcourt 0,2 px par image — aucun étirement, aucun calcul. */
  var aom=Math.abs(om||0), etire=(aom>0.45);
  var vfac=aom*R*MAS_D/60;
  var nImp=majImpacts(f, performance.now()), IMPS=f.__imp;
  for(var i2=0;i2<N;i2++){
    var o=i2*5, t, lg=A[o+3], c=LC[lg], s=LS[lg];
    var X=A[o]*c+A[o+2]*s, Zs=-A[o]*s+A[o+2]*c;
    t=A[o+1]*CT-Zs*ST; var Z=A[o+1]*ST+Zs*CT, Y=t;
    var k=F/(F-Z*R);
    var zz=(Z+1)*0.5;
    var b=(zz*MAS_NS)|0; if(b>=MAS_NS)b=MAS_NS-1; if(b<0)b=0;
    var tr=(zz*MAS_TR)|0; if(tr>=MAS_TR)tr=MAS_TR-1; if(tr<0)tr=0;
    var px=(CX+X*R*k)*MAS_D, py=(CY+Y*R*k)*MAS_D;
    /* ⚑ LE CRATÈRE : la matière s'écarte du doigt, radialement, et revient */
    for(var m2=0;m2<nImp;m2++){
      var im=IMPS[m2], dx=px-im.x, dy=py-im.y, d2=dx*dx+dy*dy;
      if(d2>im.r2) continue;
      var dd=Math.sqrt(d2); if(dd<0.6) continue;
      var ff=1-dd/im.r; ff*=ff;
      var pu=IMP_A*MAS_D*im.e*ff;
      px+=dx/dd*pu; py+=dy/dd*pu;
    }
    px=px|0; py=py|0;
    if(px<MARGE||py<MARGE||px>W-MARGE||py>W-MARGE) continue;
    /* la forme : ronde au repos, étirée DANS LE SENS DU MOUVEMENT en accélérant.
       La direction vient de la dérivée exacte de la rotation, pas d'une différence
       de positions : (Zs, sin(tangage)·X). */
    var sh=0;
    if(etire){
      var vx=Zs, vy=ST*X, vn=Math.sqrt(vx*vx+vy*vy);
      var spd=vfac*vn*k;
      var e2=(spd/2.6)|0; if(e2>GR_ELO-1)e2=GR_ELO-1;
      if(e2>0){
        var an=Math.atan2(vy,vx); if(an<0)an+=3.14159265;
        var ab=(an/3.14159265*GR_ANG)|0; if(ab>=GR_ANG)ab=GR_ANG-1;
        sh=1+(e2-1)*GR_ANG+ab;
      }
    }
    var idx=tr*MAS_NS+b, p=cpt[idx]*3, T=S[idx];
    T[p]=px; T[p+1]=py; T[p+2]=(A[o+4]*GR_FORMES+sh)*MAS_NS+b;
    cpt[idx]++;
  }
  for(var h=0;h<MAS_TR;h++){
    var B=_tamp[h]; B.fill(0);
    for(var b2=0;b2<MAS_NS;b2++){
      var id2=h*MAS_NS+b2, n2=cpt[id2]; if(!n2) continue;
      /* le fond est plus clairsemé, et c'est juste : le lointain DOIT être plus rare */
      var pas=(b2<3?2:1);
      var T2=S[id2];
      for(var j=0;j<n2;j+=pas){
        var p2=j*3, sp=ATL[T2[p2+2]];
        if(!sp) continue;
        var x0=T2[p2]-sp.ox, y0=T2[p2+1]-sp.oy, sw=sp.w, sh2=sp.h, u=sp.u;
        if(x0<0||y0<0||x0+sw>=W||y0+sh2>=W) continue;
        for(var dy=0;dy<sh2;dy++){
          var row=(y0+dy)*W+x0, sr=dy*sw;
          for(var dx=0;dx<sw;dx++){
            var v=u[sr+dx];
            if(v!==0 && (v>>>24) > (B[row+dx]>>>24)) B[row+dx]=v;
          }
        }
      }
    }
  }
}
/* ⚑ LA MATIÈRE SE RETIRE SOUS UN PRÉNOM — et s'écarte devant un visage qui ÉMERGE.
   Les deux se font dans le tampon, en baissant l'octet d'alpha, avec un bord TRAMÉ :
   la matière s'éclaircit par raréfaction, jamais par voile. Puis on verse. */
function poseMatiere(f){
  var GS=f.__masG; if(!GS||!_tamp) return;
  var W=MAS_BOX*MAS_D, ox=(ORB_CX-MAS_BOX/2), oy=(ORB_CY-MAS_BOX/2), MG=3;
  var boites=f.__bo||(f.__bo=[]); boites.length=0;
  f.querySelectorAll('.orb').forEach(function(w){
    if(!w.__pos||!w.__nom) return;
    var lg=(w.__nom.__lg||58);
    boites.push({x:(w.__pos.x-ox+(62-lg)/2-MG)*MAS_D, y:(w.__pos.y-oy-MG)*MAS_D,
                 w:(lg+MG*2)*MAS_D, h:(18+MG*2)*MAS_D});
  });
  var devant=f.__dv||(f.__dv=[]); devant.length=0;
  f.querySelectorAll('.orb').forEach(function(w){
    if(!w.__pr) return;
    /* ⚑ IL SORT DE LA MATIÈRE. Plus il vient vers toi, plus la matière s'écarte de
       lui : au fond elle le recouvre presque entièrement, devant elle lui laisse la
       place. Ce n'est pas un calque qui s'allume, c'est un dégagement progressif. */
    var av=(w.__z+MAS_R)/(2*MAS_R); if(av<0)av=0; if(av>1)av=1;
    devant.push({x:(ORB_CX+w.__pr.x-ox)*MAS_D, y:(ORB_CY+w.__pr.y-oy)*MAS_D,
                 r:(w.__d/2+3)*MAS_D, z:w.__z, fa:0.12+0.80*(1-av)});
  });
  var DIT=13*MAS_D/2;
  for(var h=0;h<GS.length;h++){
    var B=_tamp[h];
    for(var i=0;i<boites.length && !window.__sansClairiere;i++){
      var b=boites[i], rd=b.h/2;
      var x1=Math.max(0,(b.x-DIT)|0), y1=Math.max(0,(b.y-DIT)|0);
      var x2=Math.min(W,(b.x+b.w+DIT)|0), y2=Math.min(W,(b.y+b.h+DIT)|0);
      var cxl=b.x+rd, cxr=b.x+b.w-rd, cyc=b.y+rd;
      for(var y=y1;y<y2;y++){
        var dyv=y-cyc, row=y*W;
        for(var x=x1;x<x2;x++){
          var dd;
          if(x<cxl){ var dxv=x-cxl; dd=Math.sqrt(dxv*dxv+dyv*dyv)-rd; }
          else if(x>cxr){ var dxr=x-cxr; dd=Math.sqrt(dxr*dxr+dyv*dyv)-rd; }
          else dd=Math.abs(dyv)-rd;
          if(dd>DIT) continue;
          var v=B[row+x]; if(!v) continue;
          var fa;
          if(dd<=0) fa=0.06;
          else { var hsh=((x*7+y*11)>>1)&3;
                 if(dd<=DIT*0.5) fa=(hsh?0.10:1); else fa=((hsh&1)?0.10:1); }
          if(fa===1) continue;
          B[row+x]=(v&0x00FFFFFF)|((((v>>>24)*fa)|0)<<24);
        }
      }
    }
    for(var j2=0;j2<devant.length;j2++){
      var q=devant[j2]; if(q.z>=f.__masZ[h]) continue;
      var rr=q.r, re=rr+DIT, re2=re*re;
      var ya=Math.max(0,(q.y-re)|0), yb=Math.min(W,(q.y+re)|0);
      var xa=Math.max(0,(q.x-re)|0), xb=Math.min(W,(q.x+re)|0);
      for(var y3=ya;y3<yb;y3++){
        var dy3=y3-q.y, row3=y3*W;
        for(var x3=xa;x3<xb;x3++){
          var dx3=x3-q.x, dq=dx3*dx3+dy3*dy3; if(dq>re2) continue;
          var v3=B[row3+x3]; if(!v3) continue;
          var fb;
          if(dq<=rr*rr) fb=q.fa;
          else { var h3=((x3*7+y3*11)>>1)&3; fb=(h3?q.fa:1); }
          if(fb===1) continue;
          B[row3+x3]=(v3&0x00FFFFFF)|((((v3>>>24)*fb)|0)<<24);
        }
      }
    }
    GS[h].putImageData(_imgs[h],0,0);
  }
}

