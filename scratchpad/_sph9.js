/* ════════════════════════════════════════════════════════════════════════════
   UNE SEULE SPHÈRE — l'assemblage de ce que Tom a validé, tour après tour.
     · LE CENTRE EST À TON NOYAU      la matière s'y raréfie (sa demande)
     · LE CONTOUR EST ROND            le relief ne fait QUE creuser (sa demande)
     · LE GRAIN EST UNE DALLE         du moteur, échelle 1, peinte dans l'encre
                                      de l'écran (teinte tranchée par lui)
     · LE RAYON DIT LA DATE           jamais composé
     · LE CISAILLEMENT                les bandes glissent (« c'est juste »)
     · LE CREUX DU DOIGT              (« les cratères sont beaux »)
   Plus de variantes : une proposition, montrée dans le cadre de l'écran.
   ════════════════════════════════════════════════════════════════════════════ */
var BLEU='#3A54FF', MAUVE='#8A5CF0', TERRA='#F07A2E', MENTHE='#2BE88C',
    PERI='#8FA0FF', CREME='#F4EEE1', ENCRE='#16171B';
var GENS=[
 {n:'Maman', j:1,   col:MAUVE, arc:[.86,.14,.00], a:0.62},
 {n:'Adrien',j:3,   col:BLEU,  arc:[.62,.23,.15], a:1.85},
 {n:'Marion',j:12,  col:MAUVE, arc:[.80,.20,.00], a:3.02},
 {n:'Rachel',j:28,  col:TERRA, arc:[.34,.33,.33], a:4.10},
 {n:'Léa',   j:62,  col:TERRA, arc:[.55,.30,.15], a:5.16},
 {n:'Nico',  j:150, col:BLEU,  arc:[.70,.18,.12], a:6.00}
];
function tDate(j){ return Math.log(1+j)/Math.log(1+180); }
/* l'atlas : la FORME de la dalle du moteur, peinte dans l'encre de l'écran */
function atlasDalleEncre(ink, NIV, a0, a1){
  var gros=document.createElement('canvas'); gros.width=56; gros.height=56;
  var pt=document.createElement('canvas'), A=[], PX=[3,4,5];
  var rgb=(parseInt(ink.substr(5,2),16)<<16)|(parseInt(ink.substr(3,2),16)<<8)|parseInt(ink.substr(1,2),16);
  for(var d=0;d<8;d++){
    try{ window.Toile && Toile.dalleTrame(gros, d+1, 1); }catch(e){}
    for(var s=0;s<PX.length;s++){
      var px=PX[s]; pt.width=px; pt.height=px;
      var gp=pt.getContext('2d'); gp.clearRect(0,0,px,px); gp.drawImage(gros,0,0,px,px);
      var dat=gp.getImageData(0,0,px,px).data;
      for(var n=0;n<NIV;n++){
        var q=(n+0.5)/NIV, mul=a0+(a1-a0)*q*q, offs=[], vals=[], o=px>>1;
        for(var y=0;y<px;y++)for(var x=0;x<px;x++){
          var al=(dat[(y*px+x)*4+3]*mul)|0;
          if(al>3){ offs.push([y-o,x-o]); vals.push(al); }
        }
        A.push({rel:offs, al:vals, rgb:[rgb&255,(rgb>>8)&255,(rgb>>16)&255]});
      }
    }
  }
  return A;
}
function visage(g,x,y,d,fond,arc){
  g.fillStyle=fond; g.beginPath(); g.arc(x,y,d/2,0,6.2832); g.fill();
  if(arc){ var a=-Math.PI/2, C=[MENTHE,PERI,TERRA]; g.lineWidth=d*0.16;
    for(var i=0;i<3;i++){ if(arc[i]<=0)continue; var a2=a+arc[i]*6.2832;
      g.strokeStyle=C[i]; g.beginPath(); g.arc(x,y,d/2+d*0.12,a,a2); g.stroke(); a=a2; } }
  g.fillStyle=CREME;
  g.beginPath(); g.arc(x,y-d*0.11,d*0.135,0,6.2832); g.fill();
  g.beginPath(); g.ellipse(x,y+d*0.30,d*0.215,d*0.20,0,Math.PI,0); g.fill();
}
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var D=2, W=390*D, H=470*D, R=152*D, CX=W/2, CY=H*0.47;
    var A_SOMBRE=atlasDalleEncre(CREME,7,0.10,0.86);
    var A_CLAIR =atlasDalleEncre(ENCRE,7,0.10,0.72);
    var TR=semisTrame(84,0.056);
    var fRond=formeCreux(reliefCreux([[1.0,2.2,1.8,1.5,0.4,1.3,0.9],
                                      [0.5,4.6,3.4,3.8,2.1,0.6,1.7]],0.14),1.0);
    function orbite(cv, opt){
      var g=cv.getContext('2d');
      g.fillStyle=opt.clair?CREME:ENCRE; g.fillRect(0,0,W,H);
      /* la matière */
      var tmp=document.createElement('canvas');
      peint2(tmp,{css:390, mode:'donne', pts:TR, forme:fRond,
                  atlas:opt.clair?A_CLAIR:A_SOMBRE, niv:7, teintes:[0],
                  tailles:[3,4,5], R:0.39, lac:opt.lac, tan:0.24,
                  creux:opt.creux, dosCache:true});
      /* la matière se retire au centre — le centre est à ton Noyau */
      var iw=tmp.width, im=tmp.getContext('2d').getImageData(0,0,iw,iw);
      var B=new Uint32Array(im.data.buffer), C=iw/2, r0=76*D, r1=r0+30*D;
      for(var y=0;y<iw;y++){ var dy=y-C, row=y*iw;
        for(var x=0;x<iw;x++){ var dx=x-C, d2=dx*dx+dy*dy;
          if(d2>r1*r1) continue;
          if(d2<=r0*r0) B[row+x]=0;
          else if(((x*7+y*11)>>1)&3) B[row+x]=0; } }
      tmp.getContext('2d').putImageData(im,0,0);
      g.drawImage(tmp, CX-iw/2, CY-iw/2);
      /* les six : le RAYON dit la date */
      /* ⚠ ILS ÉTAIENT TROP GROS ET TROP AU CENTRE : empilés, ils se recouvraient et
         les noms se marchaient dessus. Ils vivent dans la COURONNE dégagée, entre le
         Noyau et la coquille — et à la taille des §2.9, pas au double. */
      var vus=GENS.map(function(p){
        var t=tDate(p.j), a=p.a+opt.lac, r=(104+t*44)*D;
        var z=Math.sin(a*0.83), k=1.32/(1.32-z*0.30);
        return {x:CX+Math.cos(a)*r*k, y:CY+Math.sin(a)*r*0.74*k,
                d:(30-t*9)*D*k, z:z, p:p};
      }).sort(function(a,b){return a.z-b.z;});
      vus.forEach(function(v){
        visage(g,v.x,v.y,v.d,v.p.col,v.p.arc);
        g.fillStyle=opt.clair?ENCRE:CREME;
        g.font='600 '+(12*D)+'px Bricolage,sans-serif'; g.textAlign='center';
        g.fillText(v.p.n, v.x, v.y+v.d*0.66+13*D);
      });
      /* ton Noyau, toujours devant */
      visage(g,CX,CY,74*D,BLEU,[.72,.16,.12]);
    }
    var L=[
     ['Au repos','Coquille de <b>vraies dalles du moteur</b> peintes dans l’encre, contour rond (le relief ne fait que creuser), et <b>le centre dégagé</b> : ton Noyau et les six y vivent sans rien devant.',{lac:0.4}],
     ['Un quart de tour','Le rayon de chacun dit <b>la date de sa dernière parole tenue</b> — Maman hier au plus près, Nico à cinq mois au plus loin.',{lac:2.0}],
     ['Le doigt a creusé','La surface s’enfonce là où on a appuyé. Le creux se referme en trois secondes et demie.',{lac:0.4, creux:[0.68,0.34,0.60,0.90,0.30]}],
     ['En clair','La même, sur crème. La matière passe en encre, les disques ne bougent pas.',{lac:1.2, clair:true}]
    ];
    var G=document.getElementById('g');
    L.forEach(function(F){
      var fg=document.createElement('figure');
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); cv.width=W; cv.height=H;
      box.appendChild(cv); fg.appendChild(box);
      orbite(cv,F[2]);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F[0]+'</b>'+F[1]; fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },900);
});
