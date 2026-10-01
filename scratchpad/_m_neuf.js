/* ════════════════════════════════════════════════════════════════════════════
   LES NEUF CADRES — trois partis pris x trois pressions.
   Le grain est LE MEME partout (le fil, seul retenu) et la couleur aussi
   (creme sur encre). On ne fait varier que DE QUOI la matiere est faite et
   CE QU'ELLE FAIT quand on appuie. Une variable a la fois.
   ════════════════════════════════════════════════════════════════════════════ */
var EMP_BASE={ c:[-0.40,-0.26,0.88], ax:[0.62,-0.72,0.00],
               a:0.34, el:0.64, dmax:0.105, biais:0.14,
               rho:0.10, ub:0.30, B:0.55, U:1.10 };
function emp(p){ var o={}; for(var k in EMP_BASE)o[k]=EMP_BASE[k]; o.p=p; return o; }

var RANGS=[
 {id:'poussiere', h:'A · La poussière',
  d:'Des grains indépendants. Ce qu\'on lit, c\'est une <b>densité</b>. Sous le doigt, chaque grain suit la surface et se fait chasser vers l\'extérieur — chacun pour soi.',
  loi:'poussiere', relief:P_PEAU, tailles:[5.0,7.0,9.5],
  legs:['Au repos.','Effleurée — le plateau fait déjà un méreau net, petit.','Appuyée — le même méreau, deux fois plus large, et son bourrelet.']},
 {id:'fil', h:'B · Le fil',
  d:'Deux cents brins <b>continus</b> enroulés, dont la colatitude ondule. Ce qu\'on lit, c\'est un <b>bobinage</b> et une <b>tension</b>. Sous le doigt, un brin tendu n\'entre pas dans le creux : <b>il l\'enjambe</b>.',
  loi:'fil', relief:P_TRAME, tailles:[4.0,5.2,6.8],
  legs:['Au repos.','Effleurée — les cordes commencent à se tendre au-dessus du creux.','Appuyée — une toile tendue par-dessus le vide, et les brins se serrent au bord.']},
 {id:'pavage', h:'C · Le pavage',
  d:'Des dalles pleines séparées par des joints d\'encre — un Voronoï <b>pondéré</b> sphérique, la Toile fermée sur elle-même. Ce qu\'on lit, c\'est une <b>partition</b>. Sous le doigt, rien ne se disperse : les dalles fusionnent en un <b>sceau</b>.',
  loi:'pavage', relief:P_GLACE, tailles:[3.0,3.8,5.0],
  legs:['Au repos.','Effleurée — les dalles du contact s\'aplatissent d\'un bloc.','Appuyée — un sceau apposé dans la matière, les dalles serrées tout autour.']}
];

window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    /* ⚠ la copie du moteur vieillit en silence : on VERIFIE ce qu'elle sait faire */
    window.__moteur = !!(window.Toile && window.Toile.mondeCourant);
    var CR=[244,238,225];
    var SEM={};
    SEM.poussiere = semisPoussiere(30000);
    SEM.fil       = semisFil(200,170,0.20);
    SEM.pavage    = semisPavage(44000,210,0.0380);
    var ATL={};
    RANGS.forEach(function(r){
      ATL[r.id]=atlasForme(GRAIN_FIL, CR, r.tailles, ORI, 10, 0.05, 1.00);
    });
    var G=document.getElementById('g'), infos=[];
    RANGS.forEach(function(r){
      var sec=document.createElement('div'); sec.className='rang';
      sec.innerHTML='<h2>'+r.h+'</h2><p>'+r.d+'</p>';
      var gr=document.createElement('div'); gr.className='grille'; sec.appendChild(gr);
      G.appendChild(sec);
      [0,0.14,1.0].forEach(function(p,ci){
        var fg=document.createElement('figure');
        var box=document.createElement('div'); box.className='cadre';
        var cv=document.createElement('canvas'); cv.setAttribute('data-cad',r.id+'-'+ci);
        box.appendChild(cv); fg.appendChild(box);
        var fc=document.createElement('figcaption'); fc.innerHTML=r.legs[ci];
        fg.appendChild(fc); gr.appendChild(fg);
        var o={css:392, R:0.405, niv:10, tailles:r.tailles, atlas:ATL[r.id],
               semis:SEM[r.id], relief:r.relief, loi:r.loi, lac:2.9, tan:0.32,
               emp: p>0?emp(p):null, tension:0.88};
        infos.push(peint(cv,o));
      });
    });
    window.__infos=infos; window.__pret=true;
  },700);
});

