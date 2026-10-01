/* ════════════════════════════════════════════════════════════════════════════
   LES TROIS SEMIS — ce sont TROIS PARTIS PRIS, pas trois rendus.
   Un point ne peut pas etre a la fois un grain libre, un maillon de fil, et
   une cellule d'un pavage. Chacun porte SA loi de contact.
   ════════════════════════════════════════════════════════════════════════════ */
function fr(v){return v-Math.floor(v);}
var GOLD=2.399963229728653;

/* ── A · LA POUSSIERE ─────────────────────────────────────────────────────
   N grains independants. Ce qu'on lit : une DENSITE. */
function semisPoussiere(N){
  var P=new Float64Array(N*3);
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, r=Math.sqrt(Math.max(0,1-y*y)), a=i*GOLD;
    P[i*3]=Math.cos(a)*r; P[i*3+1]=y; P[i*3+2]=Math.sin(a)*r;
  }
  return {P:P, n:N, brins:null};
}

/* ── B · LE FIL ───────────────────────────────────────────────────────────
   K brins CONTINUS enroules autour de la boule. Ce qu'on lit : un BOBINAGE.
   Le chemin d'un brin n'est pas un grand cercle : sa colatitude ONDULE
   (l'onde de Promi, portee sur la sphere) — nu tours entiers, donc le brin
   se referme sur lui-meme. C'est ce qui fait les noeuds et les moires. */
function semisFil(K,M,amp){
  var P=new Float64Array(K*M*3), brins=[], NU=[2,3,3,5,5,7,4,6];
  for(var k=0;k<K;k++){
    /* l'axe du brin : reparti sur la sphere par deux irrationnels */
    var t=fr(k*0.6180339887), u2=fr(k*0.7548776662);
    var cz=1-2*(t+0.5/K), sr=Math.sqrt(Math.max(0,1-cz*cz)), az=u2*TAU;
    var ax=[sr*Math.cos(az), cz, sr*Math.sin(az)];
    /* deux vecteurs du plan du brin */
    var h=Math.abs(ax[1])<0.9?[0,1,0]:[1,0,0];
    var e1=[ax[1]*h[2]-ax[2]*h[1], ax[2]*h[0]-ax[0]*h[2], ax[0]*h[1]-ax[1]*h[0]];
    var m1=Math.hypot(e1[0],e1[1],e1[2]); e1=[e1[0]/m1,e1[1]/m1,e1[2]/m1];
    var e2=[ax[1]*e1[2]-ax[2]*e1[1], ax[2]*e1[0]-ax[0]*e1[2], ax[0]*e1[1]-ax[1]*e1[0]];
    var nu=NU[k%NU.length], ph=fr(k*0.4142135624)*TAU, am=amp*(0.55+0.9*fr(k*0.3819660113));
    brins.push([k*M, M]);
    for(var i=0;i<M;i++){
      var th=i/M*TAU;
      var co=am*Math.sin(nu*th+ph);          /* L'ONDE : la colatitude respire */
      var sc=Math.cos(co), sa=Math.sin(co);
      var cx=Math.cos(th+ph*0.13), sx=Math.sin(th+ph*0.13);
      var j=(k*M+i)*3;
      P[j]  = sc*(e1[0]*cx+e2[0]*sx) + sa*ax[0];
      P[j+1]= sc*(e1[1]*cx+e2[1]*sx) + sa*ax[1];
      P[j+2]= sc*(e1[2]*cx+e2[2]*sx) + sa*ax[2];
    }
  }
  return {P:P, n:K*M, brins:brins};
}

/* ── C · LE PAVAGE ────────────────────────────────────────────────────────
   Un Voronoi PONDERE spherique. Ce qu'on lit : une PARTITION.
   C'est la Toile — meme loi, meme diagramme de puissance — fermee sur
   elle-meme. Les poids varient, donc les cellules aussi : des grandes et des
   petites, comme sur une vraie Toile, jamais une grille.

   ⚑ ET LA MATIERE EST DANS LES CELLULES, PAS DANS LES COUTURES.
   Ma premiere version ne gardait que les coutures : ca donnait un GLOBE
   FILAIRE — vu et revu, et vide. Sur la Toile, c'est l'inverse : chaque dalle
   est PLEINE, et ce sont les joints qui sont en encre. On garde donc tout ce
   qui n'est pas sur une couture, et chaque cellule porte SON ton — c'est cette
   mosaique de tons qui rend une Toile lisible en petit, la ou une poussiere
   n'est plus qu'un gris.

   ⚠ On ne calcule ce nuage QU'UNE FOIS : la partition ne bouge pas, seule la
   vue tourne. Le cout par image redevient celui de la poussiere. */
function semisPavage(NC,M,joint){
  var S=new Float64Array(M*3), Wt=new Float64Array(M);
  for(var k=0;k<M;k++){
    var y=1-2*(k+0.5)/M, r=Math.sqrt(Math.max(0,1-y*y)), a=k*GOLD;
    var jx=(fr(k*0.7548776662)-0.5)*0.34, jy=(fr(k*0.3819660113)-0.5)*0.34;
    var x=Math.cos(a)*r+jx, yy=y+jy, z=Math.sin(a)*r+jx*0.6;
    var m=Math.hypot(x,yy,z)||1;
    S[k*3]=x/m; S[k*3+1]=yy/m; S[k*3+2]=z/m;
    /* LE POIDS : c'est lui qui fait la Toile. Sans lui, toutes les cellules
       ont la meme taille et on retombe sur un ballon de football — c'est
       exactement ce que la premiere version donnait. Le rayon d'une cellule
       vaut ici 0,245 rad ; l'ecart des poids doit etre du meme ordre pour que
       des grandes et des petites cohabitent vraiment. */
    Wt[k]=(fr(k*0.2360679775)-0.5)*0.34
         +(fr(k*0.6180339887)-0.5)*0.16;
  }
  var P=new Float64Array(NC*3), CEL=new Int32Array(NC), n=0;
  for(var i=0;i<NC;i++){
    var cy=1-2*(i+0.5)/NC, cr=Math.sqrt(Math.max(0,1-cy*cy)), ca=i*GOLD;
    var px=Math.cos(ca)*cr, py=cy, pz=Math.sin(ca)*cr;
    var d1=9, d2=9, k1=-1;
    for(var k2=0;k2<M;k2++){
      var dp=px*S[k2*3]+py*S[k2*3+1]+pz*S[k2*3+2];
      if(dp>1)dp=1; if(dp<-1)dp=-1;
      var dd=Math.acos(dp)-Wt[k2];
      if(dd<d1){ d2=d1; d1=dd; k1=k2; } else if(dd<d2){ d2=dd; }
    }
    if(d2-d1<joint) continue;                 /* LE JOINT : de l'encre, pas de la matiere */
    P[n*3]=px; P[n*3+1]=py; P[n*3+2]=pz; CEL[n]=k1; n++;
  }
  /* LE TON D'UNE CELLULE — un aplat par cellule, jamais un degrade */
  /* ⚠ UN APLAT, JAMAIS UN DEGRADE : le ton se prend sur CINQ marches. Une
     valeur continue par cellule donnait des taches molles ; cinq marches
     donnent une mosaique, et c'est la mosaique qui se lit en petit. */
  var TON=new Float64Array(M), MAR=[0.42,0.58,0.72,0.86,1.00];
  for(var q=0;q<M;q++) TON[q]=MAR[(fr(q*0.7548776662+fr(q*0.4142135624)*0.37)*5)|0];
  return {P:P.subarray(0,n*3), n:n, brins:null, cel:CEL.subarray(0,n), ton:TON};
}
