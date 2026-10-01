/* ⚑ UN CŒUR, PAS UNE COQUILLE. Les points ne sont plus tous sur la peau : une part
   occupe l'intérieur, de plus en plus dense vers le centre. La masse a un centre de
   gravité — c'est ce qui manquait, et c'est ce qui la rend lisible en rotation. */
function semisCoeur(N, part, serre){
  var P=[], fr=function(v){return v-Math.floor(v);};
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, rr=Math.sqrt(Math.max(0,1-y*y)), ph=i*2.399963229728653;
    var x=Math.cos(ph)*rr, z=Math.sin(ph)*rr, d=1;
    if(fr(i*0.7548776662)<part){
      /* dans le volume : la puissance concentre vers le centre */
      d=Math.pow(fr(i*0.3819660113+0.11), serre);
      d=0.16+0.84*d;
    }
    P.push([x*d, y*d, z*d, d]);
  }
  return P;
}
/* les disques du produit, posés sur l'orbite */
function disques(g,W,R,CX,CY,lac,tan,liste){
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var vus=liste.map(function(p){
    var a=p.th+lac, x=Math.cos(a)*p.r, z=Math.sin(a)*p.r, y=p.y*p.r;
    var Z=-x*sl+z*cl, X=x*cl+z*sl, Y=y*ct-Z*st; Z=y*st+Z*ct;
    var k=1.9/(1.9-Z);
    return {x:CX+X*R*k, y:CY+Y*R*k, d:p.d*k*0.86, z:Z, col:p.col};
  }).sort(function(a,b){return a.z-b.z;});
  vus.forEach(function(v){
    g.save();
    g.fillStyle=v.col; g.beginPath(); g.arc(v.x,v.y,v.d/2,0,6.2832); g.fill();
    g.strokeStyle='#2BE88C'; g.lineWidth=v.d*0.16;
    g.beginPath(); g.arc(v.x,v.y,v.d/2-v.d*0.08,-1.4,3.1); g.stroke();
    /* le visage §2.10, simplifié */
    g.fillStyle='#F4EEE1';
    g.beginPath(); g.arc(v.x,v.y-v.d*0.11,v.d*0.135,0,6.2832); g.fill();
    g.beginPath(); g.ellipse(v.x,v.y+v.d*0.30,v.d*0.215,v.d*0.20,0,Math.PI,0); g.fill();
    g.restore();
  });
}
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var A_ESS=atlasRond(rampe(CL_ESSENCE,14),[1.9,2.6,3.5],8,0.07,1.00);
    var A_CRE=atlasRond(rampe(CL_CREME,1),   [1.9,2.6,3.5],8,0.05,0.95);
    var SEM=semisCoeur(46000,0.42,2.2);
    var FORMES=[
      {t:'L’onde de Promi', f:forme('onde',{ep:1.02}), R:0.33, a:A_ESS, T:14, iri:[2.8,1.6,2.4]},
      {t:'Le galet',        f:forme('galet',{ep:0.88}), R:0.35, a:A_ESS, T:14, iri:[3.0,1.6,2.4]},
      {t:'La goutte',       f:forme('goutte',{ep:1.0}), R:0.31, a:A_ESS, T:14, iri:[2.6,1.7,2.2]},
      {t:'La lentille',     f:forme('lentille',{ep:0.44}), R:0.39, a:A_ESS, T:14, iri:[3.4,1.4,3.0]},
      {t:'Le lobe (cinq)',  f:forme('galet',{ep:0.92,lobes:5,lampl:0.20}), R:0.34, a:A_ESS, T:14, iri:[3.2,1.5,2.8]}
    ];
    var G=document.getElementById('g');
    FORMES.forEach(function(F){
      var fg=document.createElement('figure'); fg.className='bande';
      var row=document.createElement('div'); row.className='vues';
      for(var v=0;v<5;v++){
        var box=document.createElement('div'); box.className='vue';
        var cv=document.createElement('canvas'); box.appendChild(cv); row.appendChild(box);
        peint2(cv,{css:230, mode:'donne', pts:SEM, n:0, forme:F.f, atlas:F.a,
                   teintes:new Array(F.T), tailles:[1.9,2.6,3.5], R:F.R,
                   lac:v*1.256, tan:0.26, iriK:F.iri[0], iriP:F.iri[1], iriM:F.iri[2]});
      }
      fg.appendChild(row);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F.t+'</b>cinq vues d’un même tour — c’est la rotation qui donne le volume.';
      fg.appendChild(fc); G.appendChild(fg);
    });
    /* deux grandes, avec les disques posés dessus */
    var LISTE=[
      {th:0.4,y:0.30,r:0.92,d:34,col:'#8A5CF0'},{th:1.5,y:-0.20,r:0.98,d:30,col:'#3A54FF'},
      {th:2.6,y:0.10,r:0.86,d:32,col:'#F07A2E'},{th:3.6,y:-0.42,r:0.94,d:28,col:'#8A5CF0'},
      {th:4.7,y:0.44,r:0.90,d:27,col:'#3A54FF'},{th:5.6,y:-0.06,r:1.00,d:31,col:'#F07A2E'}
    ];
    [[0,'L’onde, habitée'],[1,'Le galet, habité']].forEach(function(q){
      var F=FORMES[q[0]];
      var fg=document.createElement('figure'); fg.className='grande';
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); box.appendChild(cv); fg.appendChild(box);
      peint2(cv,{css:520, mode:'donne', pts:SEM, n:0, forme:F.f, atlas:F.a,
                 teintes:new Array(F.T), tailles:[2.2,3.0,4.0], R:F.R,
                 lac:0.7, tan:0.26, iriK:F.iri[0], iriP:F.iri[1], iriM:F.iri[2]});
      var g=cv.getContext('2d');
      disques(g, cv.width, 520*F.R*D, cv.width/2, cv.width/2, 0.7, 0.26, LISTE);
      /* ton Noyau, au centre et toujours devant */
      var C2=cv.width/2, RN=52;
      g.fillStyle='#3A54FF'; g.beginPath(); g.arc(C2,C2,RN,0,6.2832); g.fill();
      g.strokeStyle='#2BE88C'; g.lineWidth=RN*0.17;
      g.beginPath(); g.arc(C2,C2,RN*0.91,-1.5,3.4); g.stroke();
      g.fillStyle='#F4EEE1';
      g.beginPath(); g.arc(C2,C2-RN*0.21,RN*0.26,0,6.2832); g.fill();
      g.beginPath(); g.ellipse(C2,C2+RN*0.58,RN*0.42,RN*0.38,0,Math.PI,0); g.fill();
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+q[1]+'</b>ton Noyau au centre, six disques dans la matière. C’est ce qui partira dans une image.';
      fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },900);
});
