/* ⚑ CE QUE LA RÉFÉRENCE FAIT, ET QUE JE NE FAISAIS PAS.
   1 · PEU DE POINTS, BIEN ESPACÉS. On doit voir CHAQUE point. À quarante mille, la
       matière devient une bouillie et la trame disparaît. Ici : sept à douze mille.
   2 · UNE TRAME RÉGULIÈRE. Des lignes de latitude à espacement constant : ce sont
       elles qui, en se déformant sur le relief, dessinent la forme. Un semis
       Fibonacci, lui, ne dessine rien — c'est du bruit régulier.
   3 · UN DÉGRADÉ SIMPLE, en diagonale, du bleu clair au violet. Pas d'interférences :
       mes franges vertes hachaient la forme.
   4 · PAS DE CŒUR. C'est une coquille : le bord se densifie tout seul par la
       projection, et c'est ça qui fait le halo lumineux.
   5 · UN RELIEF DOUX ET LARGE, jamais une pointe.                                 */
/* la rampe de la référence : bleu clair lumineux → violet → rose. Éclaircie —
   la mienne était sourde, et c'est ce qui manquait le plus à l'œil. */
var CL_NUIT2=[[186,222,255],[132,178,255],[128,126,255],[176,118,244],[226,132,222]];
function semisTrame(lignes, pasArc){
  var P=[];
  for(var l=0;l<lignes;l++){
    var y=-1+2*(l+0.5)/lignes, r=Math.sqrt(Math.max(0,1-y*y));
    var nb=Math.max(4,Math.round(6.2832*r/pasArc));
    for(var i=0;i<nb;i++){
      var a=i/nb*6.2832+l*0.34;      /* le décalage évite les colonnes rigides */
      P.push([Math.cos(a)*r, y, Math.sin(a)*r]);
    }
  }
  return P;
}
window.addEventListener('load',function(){
  setTimeout(function(){
    var A_N=atlasRond(rampe(CL_NUIT2,16),[2.6,3.1,3.6],6,0.58,1.00);
    var A_C=atlasRond(rampe(CL_CREME,1), [2.6,3.0,3.4],6,0.30,1.00);
    var T1=semisTrame(74,0.062), T2=semisTrame(58,0.082), T3=semisTrame(92,0.050);
    var L=[
     {t:'La référence, au plus près', s:'Trame régulière, <b>9 400 points</b> bien espacés, relief doux à trois lobes, dégradé bleu → violet en diagonale. Le bord se densifie tout seul.',
      P:T1, f:formeP(pSuper(3.2),0.92,3,0.13), R:0.34, a:A_N, T:16, ra:[0.9,0.5], rb:true},
     {t:'Plus aéré', s:'Moins de lignes, points plus espacés : la trame respire et chaque point se compte.',
      P:T2, f:formeP(pSuper(3.2),0.92,3,0.13), R:0.34, a:A_N, T:16, ra:[0.9,0.5], rb:true},
     {t:'Plus dense', s:'Plus de lignes : on gagne en soie, on perd un peu en lisibilité du point.',
      P:T3, f:formeP(pSuper(3.2),0.92,3,0.13), R:0.34, a:A_N, T:16, ra:[0.9,0.5], rb:true},
     {t:'Quatre lobes', s:'Le même principe, quatre bosses au lieu de trois : plus calme, plus symétrique.',
      P:T1, f:formeP(pSuper(3.4),0.94,4,0.11), R:0.34, a:A_N, T:16, ra:[0.9,0.5], rb:true},
     {t:'L’oblate arrondie', s:'Sans lobes du tout : l’ellipsoïde pur, aplati. Le contour est une ellipse exacte — c’est celle que tu trouvais la moins pire.',
      P:T1, f:formeP(pOblate(),0.74), R:0.37, a:A_N, T:16, ra:[0.9,0.5], rb:true},
     {t:'Le creux du doigt', s:'La surface s’enfonce ; la trame se resserre autour du creux. C’est la trame qui montre la déformation.',
      P:T1, f:formeP(pSuper(3.2),0.92,3,0.13), R:0.34, a:A_N, T:16, ra:[0.9,0.5], rb:true,
      creux:[0.55,0.28,0.62,0.80,0.30]},
     {t:'En crème', s:'La même forme sans couleur : c’est la <b>silhouette et la trame seules</b> qu’on juge.',
      P:T1, f:formeP(pSuper(3.2),0.92,3,0.13), R:0.34, a:A_C, T:1}
    ];
    var G=document.getElementById('g');
    L.forEach(function(F){
      var fg=document.createElement('figure'); fg.className='bande';
      var row=document.createElement('div'); row.className='vues';
      for(var v=0;v<4;v++){
        var box=document.createElement('div'); box.className='vue';
        var cv=document.createElement('canvas'); box.appendChild(cv); row.appendChild(box);
        peint2(cv,{css:250, mode:'donne', pts:F.P, forme:F.f, atlas:F.a, niv:6,
                   teintes:new Array(F.T), tailles:[2.6,3.0,3.4], R:F.R,
                   lac:v*1.57, tan:0.22, rampe:F.ra, rampeBord:F.rb, creux:F.creux,
                   dosCache:true});
      }
      fg.appendChild(row);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F.t+'</b>'+F.s+' <i>— '+F.P.length.toLocaleString('fr')+' points.</i>';
      fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },700);
});
