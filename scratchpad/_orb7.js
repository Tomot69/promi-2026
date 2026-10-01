/* ⚑ UN LIQUIDE À L'INTÉRIEUR.
   Deux couches, et c'est tout le principe :
     LA COQUILLE  une trame fine, sourde, qui garde la sphère. Elle ne bouge pas.
     LE LIQUIDE   une masse DENSE et lumineuse, à l'intérieur, dont la forme est
                  donnée par des foyers mobiles (une métaballe : f(p) = Σ r²/d²).
                  On la voit à travers la coquille, et elle se déforme toute seule.
   Les quatre vues d'une ligne sont QUATRE INSTANTS du liquide, pas quatre angles :
   c'est le liquide qui bouge, la sphère reste en place.                           */
function metabille(p, F){
  var s=0;
  for(var i=0;i<F.length;i+=4){
    var dx=p[0]-F[i], dy=p[1]-F[i+1], dz=p[2]-F[i+2];
    var d2=dx*dx+dy*dy+dz*dz+1e-4;
    s+=F[i+3]*F[i+3]/d2;
  }
  return s;
}
/* les foyers, à l'instant t : ils dérivent lentement, comme une lampe */
function foyers(kind, t){
  var F=[], i, a;
  if(kind==='noyau'){
    for(i=0;i<3;i++){ a=t*0.9+i*2.1;
      F.push(0.30*Math.cos(a+i), 0.22*Math.sin(a*0.7+i*1.3), 0.26*Math.sin(a*1.1), 0.50); }
  } else if(kind==='lave'){
    for(i=0;i<5;i++){ a=t*0.8+i*1.26;
      F.push(0.42*Math.cos(a), -0.55+1.10*(((t*0.22+i*0.2)%1)), 0.42*Math.sin(a), 0.30); }
  } else if(kind==='maree'){
    for(i=0;i<7;i++){ a=i/7*6.2832;
      F.push(0.60*Math.cos(a), -0.34+0.16*Math.sin(t*1.2+a*2), 0.60*Math.sin(a), 0.44); }
    F.push(0,-0.42,0,0.60);
  } else if(kind==='tourbillon'){
    for(i=0;i<9;i++){ a=t*1.1+i*0.7; var h=-0.62+i*0.155;
      F.push(0.44*(1-Math.abs(h))*Math.cos(a), h, 0.44*(1-Math.abs(h))*Math.sin(a), 0.30); }
  }
  return F;
}
function semisLiquide(N, kind, t, seuil){
  var P=[];
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, r=Math.sqrt(Math.max(0,1-y*y)), ph=i*2.399963229728653;
    var prof=Math.cbrt((i*0.7548776662)%1);
    var p=[Math.cos(ph)*r*prof, y*prof, Math.sin(ph)*r*prof];
    if(metabille(p, foyers(kind,t)) > seuil) P.push(p);
  }
  return P;
}
window.addEventListener('load',function(){
  setTimeout(function(){
    var A_LIQ=atlasRond(rampe(CL_ESSENCE,14),[2.8,3.5,4.4],7,0.62,1.00);
    var A_COQ=atlasRond(rampe(CL_CREME,1),   [1.6,2.0,2.6],7,0.14,0.60);
    var A_LIQ2=atlasRond(rampe(CL_NUIT,10),  [2.8,3.5,4.4],7,0.62,1.00);
    var COQ_LISSE=semisTrame(78,0.060);
    var COQ_BOSSE=semisTrame(78,0.060);
    var O_BOSSE=[[1.0,2.6,2.1,1.7,0.4,1.4,0.9],[0.5,5.3,3.9,4.1,2.2,0.7,1.8]];
    var fLisse=formeCreux(reliefCreux([[1.0,1.2,1.1,1.0,0.5,0.9,1.4]],0.04),1.0);
    var fBosse=formeCreux(reliefCreux(O_BOSSE,0.15),1.0);
    var L=[
     {t:'Le noyau liquide', s:'Trois foyers qui dérivent : une masse lumineuse qui ondule au centre, vue à travers la coquille. <b>Quatre instants</b>, pas quatre angles.',
      k:'noyau', seuil:3.1, coq:fLisse, aL:A_LIQ},
     {t:'La lampe', s:'Cinq gouttes qui montent et retombent. La masse se sépare, se rejoint — c’est ce qui donne envie de rester à regarder.',
      k:'lave', seuil:2.1, coq:fLisse, aL:A_LIQ},
     {t:'La marée', s:'Le liquide occupe le bas et sa surface ondule. Une ligne de flottaison qui bouge — la sphère paraît <i>remplie</i>.',
      k:'maree', seuil:2.0, coq:fLisse, aL:A_LIQ},
     {t:'Le tourbillon', s:'Neuf foyers en hélice : le liquide s’enroule. Le mouvement se lit même à l’arrêt.',
      k:'tourbillon', seuil:2.0, coq:fLisse, aL:A_LIQ},
     {t:'La coquille bosselée', s:'La même mécanique, mais la coquille n’est plus lisse : elle a des <b>formes</b>, creusées vers l’intérieur. Toujours dans le cercle.',
      k:'noyau', seuil:3.1, coq:fBosse, aL:A_LIQ},
     {t:'En nuit', s:'Le liquide en bleu, mauve et crème — trois teintes. Plus calme, et plus lisible en petit.',
      k:'lave', seuil:2.1, coq:fBosse, aL:A_LIQ2}
    ];
    var G=document.getElementById('g');
    L.forEach(function(F){
      var fg=document.createElement('figure'); fg.className='bande';
      var row=document.createElement('div'); row.className='vues';
      for(var v=0;v<4;v++){
        var box=document.createElement('div'); box.className='vue';
        var cv=document.createElement('canvas'); box.appendChild(cv); row.appendChild(box);
        var t=v*1.55;
        /* la coquille d'abord, le liquide par-dessus : il est PLUS opaque, donc il
           gagne au tampon — c'est ce qui le fait voir à travers. */
        peint2(cv,{css:250, mode:'donne', pts:COQ_LISSE, forme:F.coq, atlas:A_COQ, niv:7,
                   teintes:[0], tailles:[1.5,1.9,2.4], R:0.37, lac:0.5, tan:0.26});
        var g=cv.getContext('2d'), im=g.getImageData(0,0,cv.width,cv.height);
        peint2(cv,{css:250, mode:'donne', pts:semisLiquide(40000,F.k,t,F.seuil),
                   forme:function(x,y,z){return [x,y,z];}, atlas:F.aL, niv:7,
                   teintes:new Array(F.aL===A_LIQ?14:10), tailles:[2.8,3.5,4.4],
                   R:0.37, lac:0.5, tan:0.26, iriK:2.6, iriP:1.5, iriM:2.2, garde:im});
      }
      fg.appendChild(row);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F.t+'</b>'+F.s; fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },700);
});
