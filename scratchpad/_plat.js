/* ════════════════════════════════════════════════════════════════════════════
   SIX FORMES QUI NE SONT PAS UNE PLANÈTE.
   Ce que l'orbite doit dire, et rien d'autre :
     · ton NOYAU au centre           · SIX personnes autour
     · le RAYON dit la date de la dernière parole tenue
     · la COULEUR dit la Nuée        · l'ARC dit les trois états
   Tout le reste est ouvert.
   ════════════════════════════════════════════════════════════════════════════ */
var BLEU='#3A54FF', MAUVE='#8A5CF0', TERRA='#F07A2E', MENTHE='#2BE88C',
    PERI='#8FA0FF', CREME='#F4EEE1', ENCRE='#16171B', LILAS='#E4CEFD';
/* Maman 1 j · Adrien 3 · Marion 12 · Rachel 28 · Léa 62 · Nico 150 */
var GENS=[
 {n:'Maman', j:1,   col:MAUVE, arc:[.86,.14,.00], lune:1},
 {n:'Adrien',j:3,   col:BLEU,  arc:[.62,.23,.15], lune:1},
 {n:'Marion',j:12,  col:MAUVE, arc:[.80,.20,.00], lune:0},
 {n:'Rachel',j:28,  col:TERRA, arc:[.34,.33,.33], lune:1},
 {n:'Léa',   j:62,  col:TERRA, arc:[.55,.30,.15], lune:0},
 {n:'Nico',  j:150, col:BLEU,  arc:[.70,.18,.12], lune:0}
];
function tDate(j){ return Math.log(1+j)/Math.log(1+180); }   /* 0 = hier, 1 = six mois */
function dalleImg(pid,px){
  var c=document.createElement('canvas'); c.width=px*2; c.height=px*2;
  try{ window.Toile && Toile.dalleTrame(c,pid,1); }catch(e){}
  return c;
}
function visage(g,x,y,d,fond,arc){
  g.fillStyle=fond; g.beginPath(); g.arc(x,y,d/2,0,6.2832); g.fill();
  if(arc){ var a=-Math.PI/2, C=[MENTHE,PERI,TERRA];
    g.lineWidth=d*0.17;
    for(var i=0;i<3;i++){ if(arc[i]<=0)continue;
      var a2=a+arc[i]*6.2832; g.strokeStyle=C[i];
      g.beginPath(); g.arc(x,y,d/2+d*0.13,a,a2); g.stroke(); a=a2; } }
  g.fillStyle=CREME;
  g.beginPath(); g.arc(x,y-d*0.11,d*0.135,0,6.2832); g.fill();
  g.beginPath(); g.ellipse(x,y+d*0.30,d*0.215,d*0.20,0,Math.PI,0); g.fill();
}
function nom(g,x,y,t,col){ g.fillStyle=col||CREME;
  g.font='600 13.5px Bricolage,sans-serif'; g.textAlign='center'; g.fillText(t,x,y); }

/* ── 1 · LA TOILE ─────────────────────────────────────────────────────────── */
function pToile(g,W,H,D){
  var cx=W/2, cy=H*0.44;
  /* le fond : de vraies dalles du moteur, semées */
  for(var i=0;i<64;i++){
    var a=i*2.3999, r=(40+((i*137)%230))*D;
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.86, s=(16+((i*53)%22))*D;
    if(Math.hypot(x-cx,(y-cy))<74*D) continue;
    g.globalAlpha=0.13+0.10*((i%5)/5);
    g.drawImage(dalleImg((i%9)+1, s), x-s/2, y-s/2, s, s);
  }
  g.globalAlpha=1;
  GENS.forEach(function(p,i){
    var a=i/6*6.2832-0.6, r=(86+tDate(p.j)*116)*D;
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.84, d=(52-tDate(p.j)*20)*D;
    var s=d*1.9;
    g.globalAlpha=0.9; g.drawImage(dalleImg(((i*3)%9)+1, s), x-s/2, y-s/2, s, s);
    g.globalAlpha=1;
    visage(g,x,y,d,p.col,p.arc);
    nom(g,x,y+d*0.92+14*D,p.n);
  });
  visage(g,cx,cy,88*D,BLEU,[.72,.16,.12]);
}
/* ── 2 · L'ONDE ───────────────────────────────────────────────────────────── */
function pOnde(g,W,H,D){
  var y0=H*0.46, A=64*D;
  var f=function(t){ return y0 + A*Math.sin(t*1.5*6.2832)*Math.sin(Math.PI*t); };
  g.strokeStyle=PERI; g.lineWidth=3*D; g.beginPath();
  for(var t=0;t<=1.001;t+=0.004){ var x=24*D+(W-48*D)*t;
    if(t===0) g.moveTo(x,f(t)); else g.lineTo(x,f(t)); }
  g.stroke();
  visage(g,24*D,f(0),74*D,BLEU,[.72,.16,.12]);
  GENS.forEach(function(p){
    var t=0.14+tDate(p.j)*0.80, x=24*D+(W-48*D)*t, y=f(t), d=(46-tDate(p.j)*16)*D;
    visage(g,x,y,d,p.col,p.arc);
    nom(g,x,y+d*0.92+13*D,p.n);
  });
}
/* ── 3 · LA SPIRALE ───────────────────────────────────────────────────────── */
function pSpirale(g,W,H,D){
  var cx=W/2, cy=H*0.46;
  g.strokeStyle='rgba(143,160,255,.34)'; g.lineWidth=2*D; g.beginPath();
  for(var t=0;t<=1.001;t+=0.002){ var a=t*4.6*6.2832*0.34, r=(62+t*164)*D;
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.86;
    if(t===0) g.moveTo(x,y); else g.lineTo(x,y); }
  g.stroke();
  GENS.forEach(function(p){
    var t=tDate(p.j), a=t*4.6*6.2832*0.34, r=(62+t*164)*D;
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.86, d=(50-t*18)*D;
    visage(g,x,y,d,p.col,p.arc); nom(g,x,y+d*0.92+13*D,p.n);
  });
  visage(g,cx,cy,84*D,BLEU,[.72,.16,.12]);
}
/* ── 4 · LES CERNES ───────────────────────────────────────────────────────── */
function pCernes(g,W,H,D){
  var cx=W/2, cy=H*0.46;
  for(var k=1;k<=5;k++){
    g.strokeStyle='rgba(244,238,225,'+(0.06+0.05*(5-k))+')'; g.lineWidth=1.6*D;
    g.beginPath(); g.ellipse(cx,cy,(58+k*36)*D,(58+k*36)*D*0.86,0,0,6.2832); g.stroke();
  }
  GENS.forEach(function(p,i){
    var t=tDate(p.j), r=(58+ (1+t*4.2)*36)*D, a=(i*1.34+0.5);
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.86, d=(50-t*18)*D;
    visage(g,x,y,d,p.col,p.arc); nom(g,x,y+d*0.92+13*D,p.n);
  });
  visage(g,cx,cy,84*D,BLEU,[.72,.16,.12]);
}
/* ── 5 · LE TISSAGE ───────────────────────────────────────────────────────── */
function pTissage(g,W,H,D){
  var cx=W/2, cy=H*0.46;
  GENS.forEach(function(p,i){
    var a=i/6*6.2832-0.4, t=tDate(p.j), r=(84+t*128)*D;
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.84;
    /* le fil : sa DENSITÉ dit l'harmonie (la part tenue) */
    var brins=Math.round(3+p.arc[0]*11);
    for(var b=0;b<brins;b++){
      var o=(b-brins/2)*1.9*D;
      g.strokeStyle=p.col; g.globalAlpha=0.10+0.36*p.arc[0];
      g.lineWidth=1*D; g.beginPath();
      g.moveTo(cx+Math.cos(a+1.5708)*o, cy+Math.sin(a+1.5708)*o);
      g.lineTo(x+Math.cos(a+1.5708)*o*0.5, y+Math.sin(a+1.5708)*o*0.5);
      g.stroke();
    }
    g.globalAlpha=1;
    var d=(48-t*16)*D;
    visage(g,x,y,d,p.col,p.arc); nom(g,x,y+d*0.92+13*D,p.n);
  });
  visage(g,cx,cy,84*D,BLEU,[.72,.16,.12]);
}
/* ── 6 · LE CHAMP ─────────────────────────────────────────────────────────── */
function pChamp(g,W,H,D){
  var cx=W/2, cy=H*0.46;
  GENS.forEach(function(p,i){
    var a=i/6*6.2832+0.3, t=tDate(p.j), r=(88+t*118)*D;
    var x=cx+Math.cos(a)*r, y=cy+Math.sin(a)*r*0.84;
    /* le halo : sa DENSITÉ dit l'harmonie */
    var n=Math.round(30+p.arc[0]*150);
    for(var k=0;k<n;k++){
      var b=k*2.3999, rr=(6+38*Math.sqrt((k*0.6180339)%1))*D;
      g.fillStyle=p.col; g.globalAlpha=0.05+0.30*(1-rr/(44*D));
      g.fillRect(x+Math.cos(b)*rr, y+Math.sin(b)*rr, 2.4*D, 2.4*D);
    }
    g.globalAlpha=1;
    var d=(46-t*15)*D;
    visage(g,x,y,d,p.col,p.arc); nom(g,x,y+d*0.92+13*D,p.n);
  });
  visage(g,cx,cy,84*D,BLEU,[.72,.16,.12]);
}
window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var L=[
     ['La Toile','Chacun occupe sa <b>dalle</b>, le Noyau la sienne au centre. Le fond est semé des vraies dalles du moteur. L’Aura devient une Toile — le vocabulaire du produit, littéralement.',pToile],
     ['L’onde','Une seule courbe traverse l’écran : <b>le trait du geste</b>. Le Noyau est à son origine, les six sont posés dessus. Plus on est loin, plus la parole est vieille.',pOnde],
     ['La spirale','Le temps s’enroule. On part du Noyau, on s’éloigne : <b>une seule ligne</b> à suivre, et la lecture est immédiate.',pSpirale],
     ['Les cernes','Des anneaux comme un tronc coupé : chaque cerne est une tranche de temps. On lit la distance d’un coup d’œil.',pCernes],
     ['Le tissage','Un <b>fil</b> part du Noyau vers chacun. Sa longueur dit la date, <b>le nombre de brins dit l’harmonie</b> — plus tu tiens, plus le lien est épais.',pTissage],
     ['Le champ','Chacun porte un <b>halo de matière</b> dont la densité dit l’harmonie. Rien ne relie : c’est la matière autour de chacun qui parle.',pChamp]
    ];
    var G=document.getElementById('g'), D=2;
    L.forEach(function(F){
      var fg=document.createElement('figure');
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); cv.width=390*D; cv.height=470*D;
      box.appendChild(cv); fg.appendChild(box);
      var g=cv.getContext('2d');
      g.fillStyle=ENCRE; g.fillRect(0,0,cv.width,cv.height);
      F[2](g,cv.width,cv.height,D);
      var fc=document.createElement('figcaption');
      fc.innerHTML='<b>'+F[0]+'</b>'+F[1]; fg.appendChild(fc); G.appendChild(fg);
    });
    window.__pret=true;
  },900);
});
