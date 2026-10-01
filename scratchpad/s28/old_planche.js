 var n=act.length;
 var cols=n<=6?2:(n<=12?3:(n<=24?4:5));
 var pad=W*0.075, gap=W*0.028;
 var cw=(W-pad*2-gap*(cols-1))/cols;
 /* Le Noyau occupe DEUX CASES SUR DEUX : on reserve un bloc, les Promi se
    rangent autour dans l'ordre, sans trou ni recouvrement. */
 var ny=!!window.shNoyau, nyIdx=-1, skip={};
 if(ny&&cols>=2){
  var nyR=(window.shNyBR===undefined?1:window.shNyBR);
  var nyC=(window.shNyBC===undefined?0:window.shNyBC);
  /* pendant la transition, la case RESERVEE reste l'ancienne jusqu'a
     mi-course : les dalles ne sautent qu'une fois, pas deux. */
  var mix=(window.shNyMix===undefined?1:window.shNyMix);
  /* la reservation suit la case d'arrivee des le depart : chaque dalle
     glisse d'elle-meme vers sa nouvelle place (voir _pos plus bas). */
  var r0=Math.max(0,nyR), c0=Math.max(0,Math.min(cols-2,nyC));
  nyIdx=r0*cols+c0;
  skip[(r0)*cols+c0]=1; skip[(r0)*cols+c0+1]=1;
  skip[(r0+1)*cols+c0]=1; skip[(r0+1)*cols+c0+1]=1;
 }
 var cases=n+(ny?4:0);
 var rows=Math.ceil(cases/cols);
 var lab=Math.max(7,Math.round(cw*0.115));
 var chh=cw+lab*2.3;
 var totH=rows*chh+gap*(rows-1);
 var y0=Math.max(pad,(H-totH)/2);
 g.textAlign='center'; g.textBaseline='alphabetic';
 /* les cases occupees par le bloc, AVANT et APRES le deplacement : chaque
    dalle glisse de l'une a l'autre au lieu de sauter. */
 function _slots(rr,cc){var sk={};
  if(!ny)return sk;
  var a=Math.max(0,rr), b2=Math.max(0,Math.min(cols-2,cc));
  sk[a*cols+b2]=1; sk[a*cols+b2+1]=1;
  sk[(a+1)*cols+b2]=1; sk[(a+1)*cols+b2+1]=1; return sk;}
 var skA=(window.shNyBR0===undefined)?skip:_slots(window.shNyBR0,window.shNyBC0);
 var skB=_slots((window.shNyBR===undefined?1:window.shNyBR),
                (window.shNyBC===undefined?0:window.shNyBC));
 function _pos(sk,idx){var s2=0,k2=0;
  while(k2<=idx){while(sk[s2])s2++; if(k2===idx)return s2; s2++; k2++;}
  return s2;}
 var slot=0;
 for(var i=0;i<n;i++){
  while(skip[slot])slot++;                    /* on enjambe le bloc du Noyau */
  var p=act[i];
  var sA=_pos(skA,i), sB=_pos(skB,i);
  var xA=pad+(sA%cols)*(cw+gap), yA=y0+Math.floor(sA/cols)*(chh+gap);
  var xB=pad+(sB%cols)*(cw+gap), yB=y0+Math.floor(sB/cols)*(chh+gap);
  var m2=(window.shNyMix===undefined?1:window.shNyMix);
  var x=xA+(xB-xA)*m2, y=yA+(yB-yA)*m2;
  slot++;
  var rot=0; /* les cases se rangent a leur place logique, sans decalage */
  var col=COL[p.status]||COL.encours;
  var tile=_dalleReelle(p.id);
  g.save(); g.translate(x+cw/2,y+cw/2); g.rotate(rot);
  if(tile){ /* on respecte les proportions de la matiere, sans cadre ni contour */
   var rr=Math.min(cw/tile.width,cw/tile.height);
   var dw=tile.width*rr, dh=tile.height*rr;
   g.drawImage(tile,-dw/2,-dh/2,dw,dh);
  } else { /* repli sans polygone : une forme molle dans la couleur de l'etat */
   var rd=cw*0.44; g.beginPath();
   g.moveTo(0,-rd);
   g.bezierCurveTo(rd*0.72,-rd*1.02,rd*1.04,-rd*0.42,rd*0.94,rd*0.16);
   g.bezierCurveTo(rd*0.86,rd*0.78,rd*0.32,rd*1.04,-rd*0.14,rd*0.96);
   g.bezierCurveTo(-rd*0.74,rd*0.86,-rd*1.04,rd*0.34,-rd*0.92,-rd*0.22);
   g.bezierCurveTo(-rd*0.82,-rd*0.76,-rd*0.42,-rd*0.98,0,-rd);
   g.closePath(); g.fillStyle=col; g.fill();
  }
  g.restore();
  if(window.shLabels===false)continue;
  var t=(p.title||'').trim(); if(t.length>26)t=t.slice(0,25)+'\u2026';
  g.fillStyle=ink; g.globalAlpha=.82;
  g.font='500 '+lab+'px Atkinson,Apfel,system-ui,sans-serif';
  g.fillText(t,x+cw/2,y+cw+lab*1.5);
  g.globalAlpha=1;
  _comp.push({id:p.id, mot:t, x:Math.round(x), y:Math.round(y),
              cw:Math.round(cw), lab:Math.round(lab*10)/10});
 }
 window._plancheComp={n:_comp.length, mots:_comp.map(function(c){return c.mot;}),
                      cases:_comp, noyau:!!ny};
 /* le Noyau dans son bloc : deux cases sur deux, gouttiere comprise */
 if(ny&&nyIdx>=0){
  var nr=Math.floor(nyIdx/cols), nc=nyIdx%cols;
  var bx=pad+nc*(cw+gap), by=y0+nr*(chh+gap);
  /* le Noyau, lui, glisse en continu entre les deux cases */
  if(mix<1&&window.shNyBR0!==undefined){
   var bx0=pad+Math.max(0,Math.min(cols-2,window.shNyBC0))*(cw+gap);
   var by0=y0+Math.max(0,window.shNyBR0)*(chh+gap);
   var bx1=pad+Math.max(0,Math.min(cols-2,window.shNyBC))*(cw+gap);
   var by1=y0+Math.max(0,window.shNyBR)*(chh+gap);
   bx=bx0+(bx1-bx0)*mix; by=by0+(by1-by0)*mix;
  }
  var bw=cw*2+gap;
  /* le bloc fait deux cases de HAUT : sa hauteur vaut chh*2+gap, pas bw.
     En centrant sur bw le Noyau remontait — une case porte son libelle. */
  var bh=chh*2+gap;
  var D=Math.round(Math.min(bw,bh)*0.86);
  try{
   var host=document.createElement('div');
   host.innerHTML=karmaRing(0,0,0,Math.round(D/2),null);
   var kc=host.querySelector('canvas');
   if(kc){
    var tt=0,ee=0,rr2=0;
    for(var q=0;q<act.length;q++){var st2=act[q].status;
     if(st2==='tenu')tt++; else if(st2==='rate')rr2++; else ee++;}
    host.innerHTML=karmaRing(ee,tt,rr2,Math.round(D/2),null);
    kc=host.querySelector('canvas');
    document.body.appendChild(host);
    host.style.cssText='position:fixed;left:-9999px;top:0;opacity:0;pointer-events:none';
    if(typeof drawKRing==='function')drawKRing(kc);
    g.drawImage(kc,bx+(bw-D)/2,by+(bh-D)/2,D,D);
    if(window.shChiffre){
     var tot2=Math.max(1,tt+ee+rr2), pc=Math.round(100*tt/tot2);
     _sigBloc(g,pc,bx+bw/2,by+bh/2,D,ink);
    }
    host.parentNode.removeChild(host);
   }
  }catch(e){}
 }
