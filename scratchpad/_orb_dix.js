/* ── LES DIX ──────────────────────────────────────────────────────────────── */
var A_CREME  = atlasRond(rampe(CL_CREME,1),    [2.0,2.8,3.8], 8, 0.05, 0.95);
var A_CREME2 = atlasRond(rampe(CL_CREME,1),    [1.6,2.2,3.0], 8, 0.06, 1.00);
var A_ESSENCE= atlasRond(rampe(CL_ESSENCE,14), [2.0,2.8,3.8], 8, 0.08, 1.00);
var A_ESS_FIN= atlasRond(rampe(CL_ESSENCE,18), [1.5,2.1,2.9], 8, 0.08, 1.00);
var A_NUIT   = atlasRond(rampe(CL_NUIT,10),    [2.2,3.0,4.2], 8, 0.06, 1.00);

/* les reliefs : [amplitude, fx, fy, fz, px, py, pz] */
var R_ONDE  = [[0.14,2.1,1.7,1.3,0.4,1.1,2.2],[0.09,3.7,2.9,2.3,1.9,0.3,1.4]];
var R_GOUTTE= [[0.26,1.0,1.0,1.0,0.9,2.1,0.2],[0.10,2.6,2.2,1.8,1.4,0.7,2.6]];
var R_PLIS  = [[0.11,6.3,0.6,0.5,0.2,1.4,0.9],[0.07,1.4,1.2,5.9,2.4,0.6,1.1]];
var R_DOUX  = [[0.08,1.6,1.3,1.1,1.2,0.5,2.0]];
var R_FORT  = [[0.20,1.9,2.3,1.5,0.7,2.4,1.0],[0.13,4.3,1.1,3.1,2.7,1.8,0.4],
               [0.07,7.9,5.3,6.1,0.9,1.3,2.8]];

var DIX=[
 {t:'Le relief',
  s:'La surface n’est plus une boule : trois ondes la gonflent et la creusent. Le contour lui-même ondule.',
  o:{mode:'fibo', n:52000, relief:R_ONDE, atlas:A_CREME, teintes:[0], lac:0.5, tan:0.30}},

 {t:'La flaque d’essence',
  s:'Même relief, mais la teinte suit l’<i>orientation</i> de la surface : bleu de face, mauve de trois quarts, menthe au ras du bord. Quatorze aplats francs, aucun dégradé.',
  o:{mode:'fibo', n:52000, relief:R_ONDE, atlas:A_ESSENCE, teintes:new Array(14),
     lac:0.5, tan:0.30, iriK:3.0, iriP:1.6, iriM:2.2}},

 {t:'La goutte',
  s:'Un relief franc — une masse qui pend et se creuse. On voit une chose souple, pas une planète.',
  o:{mode:'fibo', n:52000, relief:R_GOUTTE, atlas:A_ESSENCE, teintes:new Array(14),
     lac:1.9, tan:0.22, iriK:2.2, iriP:1.9, iriM:3.1, R:0.30}},

 {t:'La membrane',
  s:'Des lignes de latitude, serrées : c’est la <i>densité</i> qui dessine le pli, pas l’ombre. La matière se lit comme un tissu tendu.',
  o:{mode:'latitudes', n:56000, lignes:70, relief:R_PLIS, atlas:A_CREME2, teintes:[0],
     lac:0.8, tan:0.36, tailles:[1.6,2.2,3.0], dosCache:true}},

 {t:'Le drapé',
  s:'Des plis serrés qui font le tour, en lignes. La <i>densité</i> se resserre dans les creux — c’est elle qui dit le relief, pas une ombre.',
  o:{mode:'latitudes', n:56000, lignes:96, relief:R_PLIS, atlas:A_ESS_FIN, teintes:new Array(18),
     lac:2.4, tan:0.30, iriK:2.8, iriP:1.5, iriM:3.2, tailles:[1.5,2.1,2.9], dosCache:true}},

 {t:'Le creux du doigt',
  s:'Une main a appuyé : la <b>surface</b> s’enfonce et se plisse autour, elle ne se contente pas d’écarter des points.',
  o:{mode:'fibo', n:52000, relief:R_DOUX, creux:[0.55,0.35,0.76,0.95,0.34],
     atlas:A_ESSENCE, teintes:new Array(14), lac:0.15, tan:0.26, iriK:2.6, iriP:1.6, iriM:2.4, dosCache:true}},

 {t:'La matière du monde',
  s:'Le grain n’est plus un point mais une <b>vraie dalle du moteur</b>, sur surface déformée. L’Aura change d’aspect avec le Studio.',
  o:{mode:'fibo', n:34000, relief:R_ONDE, atlas:null, dalle:true, teintes:[0],
     lac:0.5, tan:0.30}},

 {t:'La nuée',
  s:'Pas de surface : un <i>volume</i>. Les points occupent l’épaisseur, le contour se dissout. Elle n’a plus de bord.',
  o:{mode:'volume', n:58000, relief:R_DOUX, atlas:A_NUIT, teintes:new Array(10),
     lac:1.1, tan:0.30, iriK:1.8, iriP:1.2, iriM:1.6, tailles:[2.2,3.0,4.2], R:0.30}},

 {t:'Le relief fort',
  s:'Trois échelles d’onde superposées : de grandes bosses, des rides, un grain. C’est le plus <i>organique</i> des dix.',
  o:{mode:'fibo', n:56000, relief:R_FORT, atlas:A_ESS_FIN, teintes:new Array(18),
     lac:2.9, tan:0.34, iriK:3.4, iriP:1.4, iriM:3.6, tailles:[1.5,2.1,2.9], R:0.30}},

 {t:'La face seule',
  s:'On ne peint que la <b>moitié tournée vers toi</b> : plus de dos qui transparaît, une peau franche. La plus <i>tactile</i>.',
  o:{mode:'fibo', n:54000, relief:R_ONDE, atlas:A_ESSENCE, teintes:new Array(14),
     lac:0.5, tan:0.30, iriK:3.0, iriP:1.6, iriM:2.8, dosCache:true}}
];

/* ── LA DALLE : un atlas fait des vraies dalles du moteur ─────────────────── */
function atlasDalle(NIV,a0,a1){
  var gros=document.createElement('canvas'); gros.width=56; gros.height=56;
  var pt=document.createElement('canvas');
  var A=[], PX=[3,4,6];
  for(var d=0;d<8;d++){
    try{ window.Toile && Toile.dalleTrame(gros, d+1, 1); }catch(e){}
    for(var s=0;s<PX.length;s++){
      var px=PX[s]; pt.width=px; pt.height=px;
      var gp=pt.getContext('2d'); gp.clearRect(0,0,px,px); gp.drawImage(gros,0,0,px,px);
      var dat=gp.getImageData(0,0,px,px).data;
      for(var n=0;n<NIV;n++){
        var q=(n+0.5)/NIV, mul=a0+(a1-a0)*q*q;
        var offs=[], vals=[], ox=px>>1, oy=px>>1;
        for(var y=0;y<px;y++)for(var x=0;x<px;x++){
          var al=(dat[(y*px+x)*4+3]*mul)|0;
          if(al>3){ offs.push([y-oy,x-ox]); vals.push(al); }
        }
        A.push({rel:offs, al:vals, rgb:[244,238,225]});
      }
    }
  }
  return A;
}

window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var A_DALLE=atlasDalle(8,0.05,0.95);
    var G=document.getElementById('g'), infos=[];
    DIX.forEach(function(p,i){
      var fg=document.createElement('figure');
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); box.appendChild(cv); fg.appendChild(box);
      var fc=document.createElement('figcaption');
      fg.appendChild(fc); G.appendChild(fg);
      var o=p.o;
      if(o.dalle){ o.atlas=A_DALLE; o.teintes=[0]; o.tailles=[3,4,6]; }
      var r=peint(cv,o);
      infos.push(r);
      fc.innerHTML='<b>'+(i+1)+' · '+p.t+'</b>'+p.s
        +' <i>— '+r.n.toLocaleString('fr')+' points, peints en '+r.ms+' ms.</i>';
    });
    window.__infos=infos; window.__pret=true;
  },900);
});
