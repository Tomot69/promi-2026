/* ── LES DIX, deuxième série ──────────────────────────────────────────────── */
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var A_CREME  = atlasRond(rampe(CL_CREME,1),    [2.0,2.8,3.8], 8, 0.05, 0.95);
    var A_FIN    = atlasRond(rampe(CL_CREME,1),    [1.5,2.1,2.9], 8, 0.06, 1.00);
    var A_ESS    = atlasRond(rampe(CL_ESSENCE,14), [2.0,2.8,3.8], 8, 0.08, 1.00);
    var A_ESSFIN = atlasRond(rampe(CL_ESSENCE,18), [1.5,2.1,2.9], 8, 0.08, 1.00);
    var A_NUIT   = atlasRond(rampe(CL_NUIT,10),    [2.2,3.0,4.2], 8, 0.06, 1.00);
    var A_DALLE  = atlasDalle(8,0.05,0.95);
    var C5=contourDalle(5,360), C2=contourDalle(2,360);

    var DIX=[
     {t:'Le galet',
      s:'Un profil dessiné, tourné autour de son axe. La silhouette <b>est</b> la courbe — rien ne peut être bancal. Le point de départ de tout le reste.',
      o:{mode:'fibo', n:52000, forme:forme('galet',{ep:0.86}), atlas:A_CREME, teintes:[0],
         lac:0.4, tan:0.26}},

     {t:'L’onde de Promi, en volume',
      s:'Le profil n’est plus abstrait : c’est <b>la courbe du geste</b> — deux bosses, jamais un segment — tournée autour de son axe. La silhouette de l’Aura devient le trait qu’on trace pour tenir sa parole.',
      o:{mode:'fibo', n:52000, forme:forme('onde',{ep:1.02}), atlas:A_ESS, teintes:new Array(14),
         lac:0.9, tan:0.20, iriK:2.8, iriP:1.6, iriM:2.4, R:0.34}},

     {t:'La dalle, donnée en volume',
      s:'La silhouette est le <b>contour d’une vraie dalle du moteur</b>, relevé au pixel et épaissi. Vue de face, l’Aura est une dalle ; vue de biais, un galet. Ça n’appartient qu’à Promi.',
      o:{mode:'fibo', n:52000, forme:forme('dalle',{contour:C5, ep:0.50}), atlas:A_CREME,
         teintes:[0], lac:0.0, tan:0.03, R:0.40}},

     {t:'La dalle en essence',
      s:'La même, en reflets. Le contour franc de la dalle contre une matière qui vire — c’est le contraste qu’on cherchait.',
      o:{mode:'fibo', n:52000, forme:forme('dalle',{contour:C2, ep:0.54}), atlas:A_ESS,
         teintes:new Array(14), lac:0.5, tan:0.06, iriK:3.0, iriP:1.5, iriM:2.6, R:0.38}},

     {t:'Le lobe',
      s:'Une harmonique <b>pure</b> d’ordre cinq : cinq bosses régulières, une symétrie exacte. Composée, pas subie.',
      o:{mode:'fibo', n:54000, forme:forme('galet',{ep:0.92, lobes:5, lampl:0.20}),
         atlas:A_ESSFIN, teintes:new Array(18), lac:0.7, tan:0.28,
         iriK:3.2, iriP:1.5, iriM:2.8, tailles:[1.5,2.1,2.9], R:0.34}},

     {t:'Le sillon',
      s:'La trame du monde <i>sillons</i>, portée par la forme : des lignes de latitude serrées dans les creux. La densité dit le relief, aucune ombre.',
      o:{mode:'latitudes', n:56000, lignes:104, forme:forme('galet',{ep:0.88, lobes:7, lampl:0.11}),
         atlas:A_FIN, teintes:[0], lac:1.2, tan:0.30, tailles:[1.5,2.1,2.9], dosCache:true}},

     {t:'La lentille',
      s:'Très aplatie, vue de biais. La forme la plus <i>graphique</i> des dix : un disque qui a de l’épaisseur, et qui capte la lumière sur sa tranche.',
      o:{mode:'fibo', n:52000, forme:forme('lentille',{ep:0.42}), atlas:A_ESS,
         teintes:new Array(14), lac:0.3, tan:0.42, iriK:3.4, iriP:1.4, iriM:3.0, R:0.40}},

     {t:'La goutte',
      s:'Un profil de goutte, à symétrie de révolution. Elle a un haut et un bas — donc une <i>tenue</i>, ce qu’une boule n’a jamais.',
      o:{mode:'fibo', n:52000, forme:forme('goutte',{ep:1.0}), atlas:A_ESS,
         teintes:new Array(14), lac:1.6, tan:0.16, iriK:2.6, iriP:1.7, iriM:2.2, R:0.32}},

     {t:'Le creux, sur une forme juste',
      s:'Le doigt enfonce la <b>surface</b> du galet. La silhouette tient : c’est une chose souple qu’on presse, pas une sphère qu’on abîme.',
      o:{mode:'fibo', n:52000, forme:forme('galet',{ep:0.88}), creux:[0.62,0.30,0.60,0.86,0.30],
         atlas:A_ESS, teintes:new Array(14), lac:0.2, tan:0.24,
         iriK:2.8, iriP:1.6, iriM:2.4, dosCache:true}},

     {t:'La matière du monde, sur la dalle',
      s:'Le grain est une <b>vraie dalle</b>, la silhouette est <b>une autre dalle</b>. Tout l’objet est fait de la Toile — et il change entièrement avec le Studio.',
      o:{mode:'fibo', n:34000, forme:forme('dalle',{contour:C5, ep:0.52}), atlas:A_DALLE,
         teintes:[0], tailles:[3,4,6], lac:0.0, tan:0.03, R:0.40}}
    ];

    var G=document.getElementById('g'), infos=[];
    DIX.forEach(function(p,i){
      var fg=document.createElement('figure');
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); box.appendChild(cv); fg.appendChild(box);
      var fc=document.createElement('figcaption'); fg.appendChild(fc); G.appendChild(fg);
      var r=peint2(cv,p.o); infos.push(r);
      fc.innerHTML='<b>'+(i+1)+' · '+p.t+'</b>'+p.s
        +' <i>— '+r.n.toLocaleString('fr')+' points, '+r.ms+' ms.</i>';
    });
    window.__infos=infos; window.__pret=true;
  },1000);
});
