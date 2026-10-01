/* ⚑ LA RÈGLE QUI MANQUAIT : LA CONVEXITÉ.
   Un contour est laid dès qu'il a une POINTE, une ÉPAULE ou un PINCEMENT — et toutes
   mes formes en avaient une. Une surface CONVEXE ne peut pas en produire : sa
   silhouette est toujours une courbe lisse, sans creux ni angle. Les huit qui suivent
   sont toutes convexes, et ne varient que par leur PROFIL et leur MATIÈRE. */
function pSuper(n){ return function(y){ var t=Math.abs(y);
  return Math.pow(Math.max(0,1-Math.pow(t,n)),1/n); }; }
function pOvoide(k){ return function(y){
  return Math.sqrt(Math.max(0,1-y*y))*(1+k*y)/(1+k*0.55); }; }
function pOblate(){ return function(y){ return Math.sqrt(Math.max(0,1-y*y)); }; }
function pCapsule(h){ return function(y){ var t=Math.abs(y);
  if(t<=h) return 1; var u=(t-h)/(1-h); return Math.sqrt(Math.max(0,1-u*u)); }; }
function pGalette(n){ return function(y){ var t=Math.abs(y);
  return Math.pow(Math.max(0,1-t*t),1/n); }; }
function formeP(prof, ep, lobes, lampl){
  return function(x,y,z){
    var rr=prof(y);
    if(lobes) rr*= 1+lampl*Math.cos(lobes*Math.atan2(z,x))*(1-y*y);
    /* ⚠ LE PROFIL EST LE RAYON, PAS UN FACTEUR. En écrivant x/h*rr*h = x*rr, je
       multipliais le profil par le rayon de la sphère : le profil se retrouvait
       ÉLEVÉ AU CARRÉ. D'où les pointes aux pôles et les flancs droits — la forme
       dessinée n'était jamais celle qu'on croyait. */
    var h=Math.sqrt(Math.max(1e-9,1-y*y));
    return [x/h*rr, y*ep, z/h*rr];
  };
}
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var A_ESS=atlasRond(rampe(CL_ESSENCE,14),[1.8,2.5,3.4],8,0.07,1.00);
    var A_CRE=atlasRond(rampe(CL_CREME,1),   [1.8,2.5,3.4],8,0.05,0.95);
    var A_NUIT=atlasRond(rampe(CL_NUIT,10),  [1.8,2.5,3.4],8,0.06,1.00);
    var SEM=semisCoeur(46000,0.40,2.2);
    var L=[
     {t:'Le squircle', s:'Une superellipse d’ordre 4, tournée : entre le cercle et le carré. Le contour le plus <i>tenu</i> — celui des icônes qu’on trouve belles sans savoir pourquoi.',
      f:formeP(pSuper(4),0.94), R:0.34, a:A_ESS, T:14, i:[3.0,1.6,2.4]},
     {t:'L’ovoïde', s:'L’œuf : une asymétrie douce, aucune pointe, une courbure qui varie sans à-coup. Il a un haut et un bas, donc une tenue.',
      f:formeP(pOvoide(0.30),1.00), R:0.33, a:A_ESS, T:14, i:[2.8,1.6,2.4]},
     {t:'L’oblate', s:'L’ellipsoïde pur, aplati. Le contour est une <b>ellipse exacte</b> — impossible à prendre en défaut. La plus sobre.',
      f:formeP(pOblate(),0.68), R:0.38, a:A_ESS, T:14, i:[3.2,1.5,2.6]},
     {t:'La galette', s:'Très plate, bord franc et rond. Vue de face c’est un disque, de biais une pastille épaisse. Elle tient en très petit.',
      f:formeP(pGalette(3.2),0.40), R:0.40, a:A_ESS, T:14, i:[3.4,1.4,3.0]},
     {t:'La capsule', s:'Un fût droit fermé par deux calottes. Silhouette de stade — deux droites, deux demi-cercles, rien d’autre.',
      f:formeP(pCapsule(0.42),1.02), R:0.32, a:A_ESS, T:14, i:[2.6,1.7,2.2]},
     {t:'Le galet à trois lobes', s:'Trois bosses de <b>huit pour cent</b> seulement : la forme reste convexe, le contour reste lisse, et pourtant elle n’est plus une boule.',
      f:formeP(pSuper(3),0.90,3,0.08), R:0.34, a:A_ESS, T:14, i:[3.0,1.6,2.6]},
     {t:'Le squircle en crème', s:'La même forme que la première, en matière sourde. Sans les reflets, c’est la <b>silhouette seule</b> qu’on juge.',
      f:formeP(pSuper(4),0.94), R:0.34, a:A_CRE, T:1, i:[0,0,0]},
     {t:'L’oblate en nuit', s:'Bleu, mauve, crème — trois teintes seulement. Plus calme que l’essence, et plus lisible en petit.',
      f:formeP(pOblate(),0.66), R:0.38, a:A_NUIT, T:10, i:[2.4,1.5,2.0]}
    ];
    var G=document.getElementById('g');
    L.forEach(function(F){
      var fg=document.createElement('figure'); fg.className='bande';
      var row=document.createElement('div'); row.className='vues';
      for(var v=0;v<4;v++){
        var box=document.createElement('div'); box.className='vue';
        var cv=document.createElement('canvas'); box.appendChild(cv); row.appendChild(box);
        peint2(cv,{css:250, mode:'donne', pts:SEM, forme:F.f, atlas:F.a,
                   teintes:new Array(F.T), tailles:[1.8,2.5,3.4], R:F.R,
                   lac:v*1.57, tan:0.26, iriK:F.i[0], iriP:F.i[1], iriM:F.i[2]});
      }
      fg.appendChild(row);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F.t+'</b>'+F.s; fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },900);
});
