/* ⚑ LA RÈGLE : ON DOIT POUVOIR TRACER UN CERCLE PARFAIT AUTOUR.
   Mes reliefs GONFLAIENT autant qu'ils creusaient : le contour partait dans tous les
   sens. Ici le relief ne fait QUE CREUSER — le rayon vaut 1 au repos et descend, il
   ne monte jamais. La silhouette est donc le cercle de rayon R, mordu par des creux
   doux. Contour mou, mais logique : il a une borne, et elle est ronde.
   Un filet crème rappelle ce cercle sur chaque vue.                                */
function reliefCreux(ondes, amp){
  return function(x,y,z){
    var s=0, tot=0;
    for(var i=0;i<ondes.length;i++){
      var h=ondes[i];
      s+=h[0]*Math.sin(h[1]*x+h[4])*Math.sin(h[2]*y+h[5])*Math.cos(h[3]*z+h[6]);
      tot+=h[0];
    }
    var u=0.5+0.5*(s/(tot||1));            /* 0 → 1 */
    return 1-amp*u;                        /* jamais au-dessus de 1 */
  };
}
function formeCreux(f, ep){
  return function(x,y,z){
    var rr=f(x,y,z), h=Math.sqrt(Math.max(1e-9,1-y*y));
    return [x/h*rr*h, y*rr*ep, z/h*rr*h];
  };
}
var O_DRAPE=[[1.0,6.3,0.6,0.5,0.2,1.4,0.9],[0.6,1.4,1.2,5.9,2.4,0.6,1.1]];
var O_DOUX =[[1.0,1.6,1.3,1.1,1.2,0.5,2.0],[0.5,3.1,2.4,2.0,0.4,1.9,0.7]];
var O_FORT =[[1.0,1.9,2.3,1.5,0.7,2.4,1.0],[0.7,4.3,1.1,3.1,2.7,1.8,0.4],
             [0.4,7.9,5.3,6.1,0.9,1.3,2.8]];
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var A_ESS=atlasRond(rampe(CL_ESSENCE,14),[2.0,2.7,3.6],8,0.08,1.00);
    var A_FIN=atlasRond(rampe(CL_CREME,1),   [1.6,2.2,3.0],8,0.06,1.00);
    var A_NUI=atlasRond(rampe(CL_NUIT,10),   [2.2,3.0,4.2],8,0.06,1.00);
    var A_DAL=atlasDalle(8,0.05,0.95);
    var L=[
     {t:'5 · Le drapé', s:'Des plis parallèles qui font le tour, en trame de lignes. Le relief ne fait que creuser : le contour reste le cercle.',
      o:{mode:'latitudes', n:56000, lignes:96, forme:formeCreux(reliefCreux(O_DRAPE,0.13),1.0),
         atlas:A_FIN, teintes:[0], tailles:[1.6,2.2,3.0], tan:0.28, dosCache:true}},
     {t:'6 · Le creux du doigt', s:'La surface s’enfonce sous le doigt et se plisse autour. Le creux est <b>dans</b> le cercle, par construction.',
      o:{mode:'fibo', n:48000, forme:formeCreux(reliefCreux(O_DOUX,0.10),1.0),
         creux:[0.58,0.30,0.74,0.92,0.30], atlas:A_ESS, teintes:new Array(14),
         tan:0.24, iriK:2.8, iriP:1.6, iriM:2.4, dosCache:true}},
     {t:'7 · La matière du monde', s:'Le grain est une <b>vraie dalle du moteur</b>. L’Aura change entièrement avec le Studio.',
      o:{mode:'fibo', n:34000, forme:formeCreux(reliefCreux(O_DOUX,0.12),1.0),
         atlas:A_DAL, teintes:[0], tailles:[3,4,6], tan:0.26}},
     {t:'8 · La nuée', s:'Pas une coquille : un <i>volume</i>. Les points occupent l’épaisseur, la densité décroît vers le bord — et le bord reste rond.',
      o:{mode:'volume', n:58000, forme:formeCreux(reliefCreux(O_DOUX,0.08),1.0),
         atlas:A_NUI, teintes:new Array(10), tan:0.28, iriK:1.8, iriP:1.2, iriM:1.6,
         tailles:[2.2,3.0,4.2]}},
     {t:'9 · Le relief fort', s:'Trois échelles de creux : de larges vallées, des rides, un grain. Le plus organique — et toujours inscrit dans le cercle.',
      o:{mode:'fibo', n:52000, forme:formeCreux(reliefCreux(O_FORT,0.17),1.0),
         atlas:A_ESS, teintes:new Array(14), tan:0.30, iriK:3.2, iriP:1.5, iriM:2.8}}
    ];
    var G=document.getElementById('g');
    L.forEach(function(F){
      var fg=document.createElement('figure'); fg.className='bande';
      var row=document.createElement('div'); row.className='vues';
      for(var v=0;v<4;v++){
        var box=document.createElement('div'); box.className='vue';
        var cv=document.createElement('canvas'); box.appendChild(cv); row.appendChild(box);
        var o={}; for(var k in F.o) o[k]=F.o[k];
        o.css=250; o.lac=v*1.57; o.R=0.37;
        peint2(cv,o);
        /* le cercle de repère : la borne, tracée */
        var g=cv.getContext('2d'), W=cv.width;
        g.strokeStyle='rgba(244,238,225,.22)'; g.lineWidth=2;
        g.beginPath(); g.arc(W/2,W/2,250*0.37*D,0,6.2832); g.stroke();
      }
      fg.appendChild(row);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F.t+'</b>'+F.s; fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },900);
});
