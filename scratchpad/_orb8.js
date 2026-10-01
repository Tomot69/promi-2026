/* ⚑ CE QUI CHANGE TOUT : LE CENTRE APPARTIENT À TON NOYAU.
   La matière ne doit RIEN y mettre — sinon les disques deviennent illisibles. Elle
   se retire donc au centre, en se raréfiant (jamais un voile), et laisse la place à
   ton Noyau et aux six qui gravitent. La sphère est une COURONNE de matière.
   ⚑ ET LES COULEURS SONT CELLES DE L'APP — plus d'essence inventée.
   ⚠ Une réserve que je pose : le menthe et le terracotta sont les couleurs des ÉTATS
   (tenu / à tenir). En les mettant dans la matière, on met l'état partout. Les rampes
   qui les emploient sont donc données, mais signalées.                              */
var R_NUEE  =[[138,92,240],[228,206,253],[244,238,225]];              /* mauve → lilas → crème */
var R_PROMI =[[58,84,255],[143,160,255],[244,238,225]];               /* bleu → periwinkle → crème */
var R_CHAUD =[[240,122,46],[250,34,88],[138,92,240]];                 /* terracotta → framboise → mauve */
var R_TERRE =[[240,122,46],[244,238,225],[138,92,240]];               /* terracotta → crème → mauve */
function atlasCarre(teintes, tailles, NIV, a0, a1){
  var A=[], Wd=0;
  for(var t=0;t<teintes.length;t++){
    var rgb=teintes[t];
    for(var s=0;s<tailles.length;s++){
      var px=tailles[s];
      for(var n=0;n<NIV;n++){
        var q=(n+0.5)/NIV, mul=a0+(a1-a0)*q*q;
        var offs=[], vals=[], o=px>>1;
        for(var y=0;y<px;y++)for(var x=0;x<px;x++){ offs.push([y-o,x-o]); vals.push((255*mul)|0); }
        A.push({rel:offs, al:vals, rgb:rgb});
      }
    }
  }
  return A;
}
/* la matière se retire au centre, par RARÉFACTION — comme la clairière des prénoms */
function degageCentre(cv, rayon, dith){
  var W=cv.width, g=cv.getContext('2d');
  var im=g.getImageData(0,0,W,W), B=new Uint32Array(im.data.buffer);
  var C=W/2, r2=rayon*rayon, re=(rayon+dith)*(rayon+dith);
  for(var y=0;y<W;y++){
    var dy=y-C, row=y*W;
    for(var x=0;x<W;x++){
      var dx=x-C, d2=dx*dx+dy*dy; if(d2>re) continue;
      var v=B[row+x]; if(!v) continue;
      var fa;
      if(d2<=r2) fa=0;
      else { var h=((x*7+y*11)>>1)&3; fa=(h?0:1); }
      B[row+x]= fa? v : 0;
    }
  }
  g.putImageData(im,0,0);
}
/* ton Noyau et les six, au centre */
function centre(cv, R){
  var g=cv.getContext('2d'), C=cv.width/2;
  var L=[[0.62,-0.72,26,'#8A5CF0'],[1.7,0.30,22,'#3A54FF'],[2.7,-0.24,24,'#F07A2E'],
         [3.7,0.62,20,'#8A5CF0'],[4.6,-0.50,19,'#3A54FF'],[5.5,0.14,23,'#F07A2E']];
  L.forEach(function(p){
    var x=C+Math.cos(p[0])*R*0.62, y=C+Math.sin(p[0])*R*0.62*0.74+p[1]*R*0.20, d=p[2];
    g.fillStyle=p[3]; g.beginPath(); g.arc(x,y,d,0,6.2832); g.fill();
    g.strokeStyle='#2BE88C'; g.lineWidth=d*0.30;
    g.beginPath(); g.arc(x,y,d*0.86,-1.4,2.6); g.stroke();
    g.fillStyle='#F4EEE1';
    g.beginPath(); g.arc(x,y-d*0.20,d*0.26,0,6.2832); g.fill();
    g.beginPath(); g.ellipse(x,y+d*0.56,d*0.42,d*0.38,0,Math.PI,0); g.fill();
  });
  var RN=R*0.30;
  g.fillStyle='#3A54FF'; g.beginPath(); g.arc(C,C,RN,0,6.2832); g.fill();
  g.strokeStyle='#2BE88C'; g.lineWidth=RN*0.20;
  g.beginPath(); g.arc(C,C,RN*0.89,-1.5,3.2); g.stroke();
  g.fillStyle='#F4EEE1';
  g.beginPath(); g.arc(C,C-RN*0.21,RN*0.26,0,6.2832); g.fill();
  g.beginPath(); g.ellipse(C,C+RN*0.58,RN*0.42,RN*0.38,0,Math.PI,0); g.fill();
}
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var TR=semisTrame(80,0.058), TRa=semisTrame(58,0.082);
    var f0=formeCreux(reliefCreux([[1.0,1.3,1.1,1.0,0.5,0.9,1.4]],0.05),1.0);
    var fB=formeCreux(reliefCreux([[1.0,2.6,2.1,1.7,0.4,1.4,0.9],[0.5,5.3,3.9,4.1,2.2,0.7,1.8]],0.15),1.0);
    var L=[
     {t:'Pixel · Nuée', s:'Grain <b>carré</b>, mauve → lilas → crème. Le centre est dégagé : ton Noyau et les six s’y lisent sans rien devant.',
      a:atlasCarre(rampe(R_NUEE,12),[3,4,5],7,0.16,1.00), T:12, P:TR, f:f0},
     {t:'Pixel · Promi', s:'Le même grain, bleu → periwinkle → crème. La famille du Promi.',
      a:atlasCarre(rampe(R_PROMI,12),[3,4,5],7,0.16,1.00), T:12, P:TR, f:f0},
     {t:'Pixel · chaud', s:'Terracotta → framboise → mauve. <b>⚠ le terracotta est « à tenir »</b> : la matière se met à parler le langage des états.',
      a:atlasCarre(rampe(R_CHAUD,12),[3,4,5],7,0.16,1.00), T:12, P:TR, f:f0},
     {t:'Pixel · terre', s:'Terracotta → crème → mauve : la crème au milieu casse la lecture d’état, et c’est le plus proche de ce que tu trouvais intéressant.',
      a:atlasCarre(rampe(R_TERRE,14),[3,4,5],7,0.16,1.00), T:14, P:TR, f:f0},
     {t:'Ajouré · Nuée', s:'Beaucoup moins de points, plus gros : on voit à travers, et les disques passent devant sans lutter.',
      a:atlasCarre(rampe(R_NUEE,12),[4,5,6],7,0.20,1.00), T:12, P:TRa, f:f0},
     {t:'Surface bosselée · terre', s:'La coquille a des formes creusées, toujours dans le cercle. Le relief se lit dans la trame.',
      a:atlasCarre(rampe(R_TERRE,14),[3,4,5],7,0.16,1.00), T:14, P:TR, f:fB}
    ];
    var G=document.getElementById('g');
    L.forEach(function(F){
      var fg=document.createElement('figure'); fg.className='bande';
      var row=document.createElement('div'); row.className='vues';
      for(var v=0;v<3;v++){
        var box=document.createElement('div'); box.className='vue';
        var cv=document.createElement('canvas'); box.appendChild(cv); row.appendChild(box);
        peint2(cv,{css:290, mode:'donne', pts:F.P, forme:F.f, atlas:F.a, niv:7,
                   teintes:new Array(F.T), tailles:[3,4,5], R:0.40,
                   lac:v*2.09, tan:0.26, rampe:[0.85,0.55], rampeBord:true, dosCache:true});
        degageCentre(cv, 290*0.40*D*0.56, 26);
        centre(cv, 290*0.40*D);
      }
      fg.appendChild(row);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F.t+'</b>'+F.s; fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },800);
});
