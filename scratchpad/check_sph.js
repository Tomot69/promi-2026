
var state={structure:'encre'};
function cc(){return [200,180,255];}
function render(){}

/* ══════════════════════════════════════════════════════════════════════
   LA PLANCHE — trois partis pour l'Aura, une page pour le Cercle.
   Aplats francs. Les dalles viennent du moteur (Toile.dalleTrame, k=1).
   ══════════════════════════════════════════════════════════════════════ */
var MENTHE='#2BE88C', TERRA='#F07A2E', PERI='#8FA0FF',
    BLEU='#3A54FF', MAUVE='#8A5CF0', FRAMB='#FA2258',
    CREME='#F4EEE1', ENCRE='#16171B';

/* le jeu de la planche : les gens, par ordre alphabétique, JAMAIS par valeur */
var GENS=[
  {n:'Adrien', piste:BLEU,  toi:[.62,.23,.15], eux:[.55,.30,.15]},
  {n:'Marion', piste:MAUVE, toi:[.80,.20,.00], eux:[.70,.20,.10]},
  {n:'Rachel', piste:TERRA, toi:[.34,.33,.33], eux:[.40,.35,.25]}
];
var NUEES=[{n:'le potager',piste:MAUVE,p:[.60,.28,.12],pid:4},
           {n:'la course',  piste:BLEU, p:[.72,.18,.10],pid:5},
           {n:'la maison',  piste:TERRA,p:[.45,.30,.25],pid:6}];

function el(tag,cls,css,txt){var n=document.createElement(tag);
  if(cls)n.className=cls; if(css)n.style.cssText=css;
  if(txt!=null)n.textContent=txt; return n;}

/* ── L'ANNEAU ────────────────────────────────────────────────────────────
   piste pleine (teinte de la nature) + arcs des trois états, bout franc.
   Aucun dégradé : trois aplats d'arc, posés bout à bout.               */
function anneau(cv,d,lw,parts,piste,second){
  var D=3; cv.width=d*D; cv.height=d*D; cv.style.width=d+'px'; cv.style.height=d+'px';
  var g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.clearRect(0,0,d*D,d*D);
  var cx=d*D/2, cy=d*D/2, R=((d-lw)/2 - (second?(9+lw*0.7):0))*D;
  var cols=[MENTHE,PERI,TERRA];
  function ring(r,w,segs){
    /* ⚑ UN ANNEAU EST FAIT DE LA MÊME MATIÈRE QUE LA SPHÈRE — des grains RONDS, au
       même pas, de tailles inégales comme elle. Ce n'est pas un décor plaqué sur un
       trait : c'est la sphère qui se resserre en cercle.
       ⚠ IL ÉTAIT EN CARRÉS ALIGNÉS, comme la sphère l'était : quand la matière est
       passée au grain rond, l'anneau est resté en pixels — et le défaut des « trois
       langages » revenait par l'autre bout. Le grain se décide à UN seul endroit
       (MAS_GRAIN, GR_EP) et tout le produit le suit. */
    var pas=MAS_GRAIN*D;
    var rangs=Math.max(2,Math.round(w*D/pas));
    for(var ri=0;ri<rangs;ri++){
      var rr=r - w*D/2 + pas*0.5 + ri*(w*D-pas)/Math.max(1,rangs-1);
      var n=Math.max(8,Math.round(6.2832*rr/pas));
      for(var i=0;i<n;i++){
        var t=i/n, a=-Math.PI/2 + t*6.2832;
        var col=piste, acc=0;
        for(var s=0;s<segs.length;s++){ acc+=segs[s];
          if(t<acc){ if(segs[s]>0) col=cols[s]; break; } }
        /* la taille du grain varie, comme dans la sphère : trois épaisseurs,
           tirées d'un hachage stable de sa place sur l'anneau. */
        var hh=((i*2654435761)>>>0)%3;
        g.fillStyle=col;
        g.beginPath();
        g.arc(cx+rr*Math.cos(a), cy+rr*Math.sin(a), GR_EP[hh]*D/2/MAS_D*1.05, 0, 6.2832);
        g.fill();
      }
    }
  }
  ring(R,lw,parts);
  if(second) ring(R+(9+lw*0.7)*D, lw*0.7, second);
  return {cx:cx/D,cy:cy/D,R:R/D};
}

/* ── LE VISAGE — §2.10, silhouette crème sur couleur de nature ───────── */
function visage(d,fond){
  var i='vc'+(visage._n=(visage._n||0)+1);
  var s='<svg width="'+d+'" height="'+d+'" viewBox="0 0 '+d+' '+d+'">'
   +'<defs><clipPath id="'+i+'"><circle cx="'+(d/2)+'" cy="'+(d/2)+'" r="'+(d/2)+'"/></clipPath></defs>'
   +'<g clip-path="url(#'+i+')">'
   +'<circle cx="'+(d/2)+'" cy="'+(d/2)+'" r="'+(d/2)+'" fill="'+fond+'"/>'
   +'<circle cx="'+(d/2)+'" cy="'+(0.78*d/2)+'" r="'+(0.19*d)+'" fill="'+CREME+'"/>'
   +'<path d="M'+(d/2-0.30*d)+' '+(0.98*d)+' A '+(0.30*d)+' '+(0.27*d)+' 0 0 1 '
     +(d/2+0.30*d)+' '+(0.98*d)+' Z" fill="'+CREME+'"/></g></svg>';
  return s;
}

/* ── LE TRAIT — deux points, une courbe quadratique. Jamais de segment. ── */
function trait(cv,w,h,o){
  o=o||{}; var D=2; cv.width=w*D; cv.height=h*D;
  cv.style.width=w+'px'; cv.style.height=h+'px';
  var g=cv.getContext('2d'); g.setTransform(D,0,0,D,0,0); g.clearRect(0,0,w,h);
  var r=7, x0=r+1, x1=w-r-1, mid=(o.mid===undefined?h/2:o.mid),
      amp=(o.amp===undefined?16:o.amp), per=(o.per===undefined?1.5:o.per);
  function courbe(y0,sens,col,ep){
    g.lineWidth=ep||3; g.lineCap='round'; g.strokeStyle=col;
    var N=64, pts=[];
    for(var i=0;i<=N;i++){var t=i/N,x=x0+(x1-x0)*t;
      pts.push([x, y0 + sens*amp*Math.sin(t*per*6.2832)*Math.sin(Math.PI*t)]);}
    g.beginPath(); g.moveTo(pts[0][0],pts[0][1]);
    for(var j=1;j<pts.length-1;j++){
      var mx=(pts[j][0]+pts[j+1][0])/2, my=(pts[j][1]+pts[j+1][1])/2;
      g.quadraticCurveTo(pts[j][0],pts[j][1],mx,my);}
    g.quadraticCurveTo(pts[N-1][0],pts[N-1][1],pts[N][0],pts[N][1]); g.stroke();
    return pts;
  }
  var A=courbe(mid,1,o.col||PERI,3);
  var B=o.double? courbe(mid,-1,o.col2||MAUVE,3) : null;
  g.fillStyle=o.col||PERI;
  g.beginPath(); g.arc(x0,mid,r,0,6.2832); g.fill();
  g.beginPath(); g.arc(x1,mid,r,0,6.2832); g.fill();
  cv.__A=A; cv.__B=B; cv.__mid=mid;
  return A;
}

/* ── LA VRAIE DALLE ──────────────────────────────────────────────────── */
function dalle(pid,px){
  var c=document.createElement('canvas'); c.width=px*2; c.height=px*2;
  c.style.cssText='width:'+px+'px;height:'+px+'px;display:block';
  try{ window.Toile && Toile.dalleTrame(c,pid,1); }catch(e){}
  return c;
}

/* ── LE CADRE ────────────────────────────────────────────────────────── */
function cadre(theme){
  var f=el('div','fr '+(theme==='lt'?'lt':'dk'));
  f.__ink = theme==='lt'? ENCRE : CREME;
  f.__fond= theme==='lt'? CREME : ENCRE;
  return f;
}
function plateau(f,titre){
  var p=el('div','plat');
  p.appendChild(el('div','t',null,titre));
  p.appendChild(el('div','c',null,'✕ FERMER'));
  f.appendChild(p); return p;
}
function eb(f,x,y,txt,col){ var n=el('div','eb',
  'left:'+x+'px;top:'+y+'px;'+(col?'color:'+col:''), txt); f.appendChild(n); return n;}
function txt(f,cls,x,y,w,fs,fw,t,extra){
  var n=el('div',cls,'left:'+x+'px;top:'+y+'px;width:'+w+'px;font-size:'+fs+'px;'
    +(fw?'font-weight:'+fw+';':'')+(extra||''), t);
  f.appendChild(n); return n;}
function bouton(f,y,t,plein,col,ink){
  var b=el('div','btn'+(plein?' plein':''),'top:'+y+'px;'
    +(plein?'background:'+col+';color:'+ink+';':''));
  b.appendChild(el('span',null,null,t)); f.appendChild(b); return b;}
function legPos(f,y,ink){
  var n=el('div','eb','left:24px;top:'+y+'px;width:342px;text-align:center;line-height:19px;'
    +'text-transform:none;letter-spacing:.10em',
    'dedans, ce que tu tiens · dehors, ce qu’on te tient');
  f.appendChild(n); return n;}
function legende(f,x,y){
  var L=el('div','leg','left:'+x+'px;top:'+y+'px');
  [['tenues',MENTHE],['en cours',PERI],['à tenir',TERRA]].forEach(function(p){
    var s=el('span'); s.appendChild(el('i',null,'background:'+p[1]));
    s.appendChild(document.createTextNode(p[0])); L.appendChild(s);});
  f.appendChild(L); return L;}

/* la grille d'anneaux — JAMAIS une rangée de barres, JAMAIS un tri par valeur */
function grille(f,y,d,gens,cercle,ink,centre){
  var n=gens.length, ecart=26, tot=n*d+(n-1)*ecart, x0=(390-tot)/2;
  gens.forEach(function(p,i){
    var x=x0+i*(d+ecart);
    var box=el('div',null,'left:'+x+'px;top:'+y+'px;width:'+d+'px;height:'+d+'px');
    var cv=document.createElement('canvas');
    cv.style.cssText='position:absolute;left:0;top:0';
    box.appendChild(cv); f.appendChild(box);
    anneau(cv,d,Math.round(d*0.104),p.toi||p.p,p.piste, null);
    var vd=Math.round(d*0.62), vx=x+(d-vd)/2, vy=y+(d-vd)/2;
    var v=el('div',null,'left:'+vx+'px;top:'+vy+'px;width:'+vd+'px;height:'+vd+'px');
    if(centre==='dalle') v.appendChild(dalle(p.pid||1,vd));
    else v.innerHTML=visage(vd,p.piste);
    f.appendChild(v);
    txt(f,'bg600',x-14,y+d+11,d+28,13.5,600,p.n,'text-align:center;color:'+ink);
  });
}

/* ════════ UNE SEULE SOURCE : anneau, chiffre et mot ════════ */
var PARTS={tenu:62,encours:24,rate:14};
function partsArc(){var t=PARTS.tenu+PARTS.encours+PARTS.rate;
  return [PARTS.tenu/t,PARTS.encours/t,PARTS.rate/t];}
function harmonieVal(){return Math.round(100*PARTS.tenu/(PARTS.tenu+PARTS.rate));}
function harmonyWord(p){if(p==null)return 'à tisser';
  if(p>=85)return 'rayonnante'; if(p>=65)return 'solide';
  if(p>=40)return 'installée'; return 'naissante';}
function couleurHarmonie(){var v=harmonieVal(); return v>=65?MENTHE:(v>=40?PERI:TERRA);}

/* ════════ LE MONDE D'ALORS ════════ */
var _mc='encre', _cache={};
function dalleDans(pid,px,m,p){
  var c=document.createElement('canvas'); c.width=px*2; c.height=px*2;
  c.style.cssText='width:'+px+'px;height:'+px+'px;display:block;'
    +'opacity:1;filter:none;mix-blend-mode:normal;position:relative;z-index:2';
  var k=pid+'|'+(m||'-')+'|'+(p||'-')+'|'+px;
  try{
    if(_cache[k]){c.getContext('2d').drawImage(_cache[k],0,0);return c;}
    if(m&&m!==_mc){Toile.setTheme(m);_mc=m;}
    if(p&&Toile.setPalette)Toile.setPalette(p);
    Toile.dalleTrame(c,pid,1);
    var s=document.createElement('canvas'); s.width=c.width; s.height=c.height;
    s.getContext('2d').drawImage(c,0,0); _cache[k]=s;
  }catch(e){}
  return c;
}
function dalle(pid,px){return dalleDans(pid,px,null,null);}

/* ════════════════════════════════════════════════════════════════════════════
   L'ORBITE EN 3D — un système planétaire vu de biais.
     LE RAYON       la date de la dernière parole tenue. Inchangé.
     LE PLAN        inclinaison et noeud tirés du NOM : stables, jamais d'une valeur.
     LA PERSPECTIVE plus loin dans la profondeur = plus petit. Ce n'est pas un rang :
                    la taille apparente change à chaque seconde.
     LA VITESSE     la même pour tous. LA LUNE : binaire. LA COULEUR : la Nuée.
   ════════════════════════════════════════════════════════════════════════════ */
/* nd = le noeud · inc = l'inclinaison · ph = la phase — COMPOSÉS, en degrés.
   Trois plans presque couchés (Maman, Marion, Rachel) se croisent près du centre ;
   deux plans redressés (Léa, Nico) balaient large ; Adrien coupe en travers.
   Les phases sont décalées pour qu'aucun alignement régulier ne se produise. */
var ORBITE=[
  {n:'Maman',  piste:MAUVE, arc:[.86,.14,.00], bouge:true,  j:1,   nd:214, inc:26, ph:118},
  {n:'Adrien', piste:BLEU,  arc:[.62,.23,.15], bouge:true,  j:3,   nd:118, inc:56, ph:250},
  {n:'Marion', piste:MAUVE, arc:[.80,.20,.00], bouge:false, j:12,  nd:250, inc:34, ph:22 },
  {n:'Rachel', piste:TERRA, arc:[.34,.33,.33], bouge:true,  j:28,  nd:  6, inc:30, ph:196},
  {n:'Léa',    piste:TERRA, arc:[.55,.30,.15], bouge:false, j:62,  nd:302, inc:58, ph:74 },
  {n:'Nico',   piste:BLEU,  arc:[.70,.18,.12], bouge:false, j:150, nd: 46, inc:60, ph:308}
];
/* le tour dure 2 min 12 : assez lent pour qu'aucun mouvement ne se remarque,
   assez pour que la scène ait changé si on la laisse. */
/* ⚠ 132 s, c'était trop lent pour être VU : 0,024 px par image, la scène paraissait
   figée — et le moindre frémissement de prénom devenait alors le seul mouvement de
   l'écran. À 84 s un anneau avance de 0,038 px par image : toujours calme, mais la
   scène a visiblement changé quand on y revient. */
/* 122 sortait par la gauche (x = 3) et passait sous « solide » (y = 454).
   116 à 268 est la borne mesurée : boîte 20 · 138 → 353 · 444. */
/* ⚑ UN SEUL FOYER POUR TOUTE LA SCÈNE — 340. C'est la sphère qui l'a imposé.
   À deux foyers (180 pour les six, 620 pour la matière) un anneau au premier plan
   sortait de la silhouette : mesuré, 25 px dehors. Ce n'était pas un défaut de
   dessin, c'était l'incohérence des deux projections — avec UN foyer, un corps qui
   est DANS la sphère se projette DANS la silhouette, toujours.
   Ce que ça coûte : le rapport de profondeur passe de 3,43 à ~2,0. Ce que ça rend :
   les six sont vraiment dedans, et c'est la règle. La profondeur, désormais, ce
   n'est plus la taille toute seule — c'est la matière qui VOILE ce qui s'enfonce. */
var ORB_CX=195, ORB_CY=272, ORB_T=240000, ORB_RMIN=80, ORB_RMAX=118, ORB_JMAX=180;
/* ⚑ ON SÉPARE LE TEMPS ET LE POINT DE VUE — et c'est ce qui rend la sphère prenable.
   Jusqu'ici un seul nombre faisait tout : les six avançaient sur leur orbite ET la
   matière tournait, au même rythme. Impossible d'y poser un doigt : tourner l'objet
   aurait fait avancer le temps.
     LE TEMPS      les six voyagent sur leur orbite — un tour en 4 min. C'est la donnée.
     LE POINT DE VUE  l'objet entier tourne sur lui-même — 84 s au repos, et le doigt
                   le prend. Il ne touche à AUCUNE donnée : il change où on est placé.
   La vue est deux angles (lacet, tangage) appliqués à TOUT — matière et personnes —
   avant la projection. C'est ce qui garantit qu'on regarde un seul objet. */
var VUE_T=165000;                      /* le tour de la vue au repos : 2 min 45.
                                          Lente, contemplative. C'est le GESTE qui
                                          accélère, pas elle. */
var VUE_AUTO=6.2832/(VUE_T/1000);      /* rad/s — la rotation lente qui ne s'arrête jamais */
var VUE_TANG=0.36;                     /* le tangage de repos : la sphère vue de biais */
var VUE_SENS=0.0110;                   /* un pixel de doigt = 0,011 rad. 330 px ≈ un tour */
var VUE_TAU=0.55;                      /* l'élan s'éteint en exp(−t/0,55) */
var VUE_VMAX=11;                       /* on borne le lancer : au-delà, c'est illisible */
var VUE_TANGMAX=1.15;                  /* on ne bascule pas par-dessus le pôle */
var TAP_SEUIL=6;                       /* au-delà de 6 px, ce n'est plus un toucher */
/* ⚑ LA MATIÈRE EST ENTRAÎNÉE. Six classes de retard, prises sur la LATITUDE dans le
   repère du flux : l'équateur traîne, les pôles suivent. C'est le cisaillement d'un
   fluide, pas d'un maillage. Il ne coûte rien : six cosinus par image, et un index
   par point. Au repos il vaut 0,4 px — on ne le voit pas ; au lancer, 12°. */
var LAG_N=6, LAG_K=0.045, LAG_MAX=0.22;
/* ⚑ LA DÉRIVE — CE QUI MANQUAIT AU REPOS.
   Sans doigt, la sphère tournait d'un bloc : belle, et morte. Une masse vivante ne
   tourne pas d'un bloc — elle se CISAILLE. Chaque bande de latitude glisse ici à sa
   propre allure, en permanence, et le motif se recompose sans fin.
   ⚠ ELLE OSCILLE, ELLE NE S'ACCUMULE PAS. Une dérive cumulative décorrélerait les
   bandes au bout de quelques minutes : les fils se perdraient et la sphère finirait
   en bruit uniforme. Ici chaque bande va et revient, sur des périodes premières entre
   elles (37 à 97 s) : la structure ne se défait jamais, et pourtant on ne voit jamais
   deux fois le même dessin.
   Ce n'est pas un effet posé sur la matière : c'est la matière qui a une vie propre.
   Coût : six sinus par image. */
var DER_AMP=[0.00,0.052,0.086,0.104,0.078,0.038];   /* radians — l'équateur glisse le plus */
var DER_PER=[1,   37000, 53000, 71000, 89000, 97000];
var DER_PH =[0,   0.8,   2.3,   4.1,   5.5,   1.7];
/* et le TANGAGE respire : ±0,028 rad sur 83 s. La silhouette n'est jamais tout à
   fait la même — sans que rien ne se déplace assez vite pour se remarquer. */
var TAN_AMP=0.028, TAN_PER=83000;
/* ⚠ LE FOYER FAIT TOUT. À 420 un anneau qui passait derrière gardait 88 % de sa
   taille : on voyait un cercle, pas une sphère. À 170 il tombe à 42 % et double
   au premier plan — l'écart se SENT. Mesuré et publié dans le relevé. */
/* ⚠ L'ARC DU NOYAU DOUBLE (13 → 26) SANS QUE LE DIAMÈTRE BOUGE.
   anneau() trace à R = (d − lw)/2, donc le bord EXTÉRIEUR reste à d/2 = 45 :
   tout l'ajout mange le centre. Le creux tombe de 64 à 38 — le visage suit,
   48 → 34 (écart au §2.10, conséquence directe de l'épaisseur demandée). */
/* ⚠ L'ARC S'AMINCIT PAR L'INTÉRIEUR. anneau() trace à R = (d − lw)/2 : le bord
   EXTÉRIEUR reste à 45 quoi qu'il arrive, donc passer de 26 à 18 rend 8 px au
   CREUX (19 → 27 de rayon intérieur) et le visage retrouve sa place : 27 → 40. */
var TOI_D=90, TOI_ARC=18, TOI_VIS=40, PERS_D=36, PERS_ARC=7, FOC=270;
/* ⚠ L'ARC D'UNE PERSONNE PASSE DE 4 À 7, ET CE N'EST PAS UN CAPRICE : à 4 px, le
   grain n'a la place que de deux rangs de points et l'anneau disparaît. La matière
   impose son épaisseur minimale — c'est le prix de l'unité des trois matières.
   Le diamètre suit à peine (32 → 34) pour que le visage garde sa place. */

/* ════════════════════════════════════════════════════════════════════════════
   LA MASSE — LA SPHÈRE EST UN TISSU DE TRAJECTOIRES.

   Le volume ne vient PAS de six anneaux : six objets ne feront jamais une sphère,
   quelle que soit la finition. Il vient de la DENSITÉ — trois mille traits courts,
   répartis sur la sphère et tournant avec elle.

   CE QUI APPARTIENT À PROMI, et ce n'est pas un habillage : chaque trait est un
   MORCEAU DE GRAND CERCLE — le même genre de chemin que parcourent les six.
   La sphère est le tissu de tous les chemins ; six d'entre eux portent un visage.
   Elle ne dit rien d'autre, et elle n'a rien d'autre à dire : c'est vivant.

   LA TECHNIQUE EST MESURÉE AVANT D'ÊTRE DESSINÉE (scratchpad/banc.py) :
     un beginPath + un stroke PAR TRAIT   4000 traits → 1,17 ms · pire 16,4 ms (image perdue)
     des POINTS en fillRect               4000 traits → 0,73 ms
     ⚑ SEAUX DE PROFONDEUR, un seul chemin et un seul stroke par seau
                                          4000 traits → 0,25 ms · pire 0,60 ms
   Sept seaux : la profondeur est quantifiée en SEPT NIVEAUX FRANCS, pas fondue en
   dégradé. Un seau = une opacité, une épaisseur, un chemin, un stroke.
   ════════════════════════════════════════════════════════════════════════════ */
var MAS_FILS=36, MAS_PTS=1750, MAS_DEV=0.34;
var MAS_R=142, MAS_FOC=270, MAS_NS=7, MAS_BOX=344, MAS_TILT=0.36;
/* sept niveaux FRANCS de profondeur : une opacité, une taille. Pas un dégradé. */
/* ⚠ LA MATIÈRE EST LE DÉCOR, PAS LE SUJET. Des dalles à pleine opacité, la sphère
   devenait un camouflage : la palette du monde entrait en concurrence avec les
   couleurs d'état des six, et le terracotta de la matière est LE MÊME que « à tenir ».
   On la retient — 0,04 à 0,55 — et la profondeur s'éteint plus vite : le limbe
   redevient le bord de la boule, et les six redeviennent le sujet. */
var MAS_A0=0.05, MAS_A1=0.74, MAS_P0=0.92, MAS_P1=2.05;
/* LE GRAIN — le pas et la taille du point. La sphère ET les anneaux s'en servent :
   c'est le seul endroit où la matière du produit se décide. */
var MAS_GRAIN=1.75, MAS_PT=1.45;
var GR_EP=[1.5,2.2,3.1];   /* l'épaisseur du grain d'un ANNEAU (la sphère, elle, a ses dalles) */
/* ⚑ QUATRE TRANCHES DE PROFONDEUR, ET C'EST CE QUI MET LES SIX *DEDANS*.
   Une seule toile sous tout le monde et les anneaux flotteraient DESSUS.
   La sphère est tranchée en quatre dalles de profondeur ; chaque tranche prend
   le MÊME z-index que lui donnerait la formule des anneaux (20 + z/10), donc
   un anneau qui s'enfonce PASSE DERRIÈRE la matière et se fait voiler, et un
   anneau qui vient vers toi passe devant. La tranche la plus proche reste sous
   ton Noyau (40) : rien ne passe jamais devant toi. */
var MAS_TR=4;
var MAS_SPLIT=0.70, MAS_ZMAX=0;
var MAS_D=2;      /* la finesse de la toile de matière, en pixels par pixel CSS */
var _mas=null, _seaux=null, _cpt=null;
var _lc=new Float32Array(LAG_N), _ls=new Float32Array(LAG_N);
/* les tours de chaque fil — choisis, pas tirés : deux fils au même nombre de tours
   se superposeraient en moiré régulier. */
/* trente-six nombres de tours, tous premiers entre eux deux à deux autant que
   possible : deux fils au même nombre se superposeraient en moiré régulier. */
var MAS_TOURS=[9,11,8,12,10,7,13,9,11,8,12,10,7,13,9,14,8,11,10,12,7,9,13,
               15,8,10,12,7,11,9,13,14,8,12,10,9];
function fabriqueMasse(){
  if(_mas) return _mas;
  var xs=[], fr=function(x){return x-Math.floor(x);};
  /* l'axe du monde — celui autour duquel s'enroulent les fils.
     Ce n'est PAS l'axe de rotation : c'est ce décalage qui donne le balayage
     oblique au lieu d'un empilement de parallèles. */
  var fx=0.30, fy=0.90, fz=0.32, fn=Math.sqrt(fx*fx+fy*fy+fz*fz);
  fx/=fn; fy/=fn; fz/=fn;
  var e1x=fy, e1y=-fx, e1z=0, en=Math.sqrt(e1x*e1x+e1y*e1y)||1; e1x/=en; e1y/=en;
  var e2x=fy*e1z-fz*e1y, e2y=fz*e1x-fx*e1z, e2z=fx*e1y-fy*e1x;
  for(var k=0;k<MAS_FILS;k++){
    /* ⚑ UN FIL, ENROULÉ D'UN PÔLE À L'AUTRE — et POINTILLÉ.
       Un point posé sur un chemin dit encore le chemin : quinze fils enroulés,
       quinze axes légèrement déviés, ils se croisent sans se superposer. C'est ce
       croisement qui fait le VOLUME, et la densité qui fait la sphère. */
    var d1=MAS_DEV*(2*fr(k*0.6180339887+0.17)-1), d2=fr(k*0.7548776662+0.41)*6.2832;
    var cd=Math.cos(d1), sd=Math.sin(d1), c2=Math.cos(d2), s2=Math.sin(d2);
    var ax=fx*cd+(e1x*c2+e2x*s2)*sd,
        ay=fy*cd+(e1y*c2+e2y*s2)*sd,
        az=fz*cd+(e1z*c2+e2z*s2)*sd;
    var p1x=-az, p1y=0, p1z=ax, pn=Math.sqrt(p1x*p1x+p1z*p1z)||1;
    p1x/=pn; p1z/=pn;
    var p2x=ay*p1z-az*p1y, p2y=az*p1x-ax*p1z, p2z=ax*p1y-ay*p1x;
    var N=MAS_TOURS[k%MAS_TOURS.length], ph=fr(k*0.4142135624)*6.2832;
    for(var i=0;i<=MAS_PTS;i++){
      var s=i/MAS_PTS;
      /* y RÉGULIER, pas l'angle : les tours s'étagent à hauteur égale et se
         resserrent d'eux-mêmes aux pôles, comme un fil qu'on enroule à la main. */
      var y=1-2*s, rr=Math.sqrt(Math.max(0,1-y*y));
      var th=s*N*6.2832+ph, c=Math.cos(th)*rr, s3=Math.sin(th)*rr;
      var X=ax*y+p1x*c+p2x*s3, Y=ay*y+p1y*c+p2y*s3, Z=az*y+p1z*c+p2z*s3;
      /* ⚠ ON CREUSE DES VIDES. Une répartition régulière est morte, même quand elle
         tourne — la même leçon que sur les six orbites. Quatre ondes qui se croisent
         serrent des paquets et effacent des zones : la sphère respire au lieu
         d'être une grille. */
      var v=0.50+0.26*Math.sin(7.10*X+1.70)*Math.cos(6.30*Y-0.60)
                +0.20*Math.sin(8.40*Z+2.20)+0.14*Math.cos(9.90*X-7.10*Y+0.40);
      /* la classe de RETARD, prise sur la latitude dans le repère du flux :
         l'équateur traîne le plus, les pôles suivent. Différentielle, comme un fluide. */
      if(v>0.36){
        var lat=Math.abs(ax*X+ay*Y+az*Z);
        var lg=Math.min(LAG_N-1,Math.max(0,Math.round((1-lat)*(LAG_N-1))));
        /* ⚑ LA TAILLE DU GRAIN VARIE, et pas au hasard : elle suit une quatrième
           onde, plus serrée que celles qui creusent les vides. Des paquets de gros
           grains, des zones de poussière fine. Une matière régulière est morte,
           même quand elle tourne. */
        var vt=Math.sin(11.3*X+2.1)*Math.cos(9.7*Y-1.4)+0.7*Math.sin(13.1*Z+0.6);
        var tl=vt<-0.35?0:(vt<0.55?1:2);
        xs.push(X,Y,Z,lg,tl);
      }
    }
  }
  _mas=new Float32Array(xs);
  var n=_mas.length/5;
  _seaux=[]; for(var b=0;b<MAS_NS*MAS_TR;b++) _seaux.push(new Float32Array(n*5));
  _cpt=new Int32Array(MAS_NS*MAS_TR);
  window._masCombien=n;
  return _mas;
}
/* ⚠ LA TECHNIQUE EST MESURÉE AVANT D'ÊTRE DESSINÉE — et le premier banc mesurait
   LE MAUVAIS CHIFFRE : le canevas 2D EMPILE les ordres, il ne les exécute pas.
   Le temps d'appel n'est pas le temps de peinture. Le second banc mesure
   l'INTERVALLE RÉEL ENTRE DEUX IMAGES (scratchpad/banc3.py), et il est net :
     traits    2 400 → 16,9 ms   6 500 → 25,2 ms   13 000 → 50,4 ms
     points   13 000 → 17,4 ms  26 000 → 18,4 ms
   Le coût d'un TRAIT est dans son NOMBRE, pas dans sa longueur (60 000 px de
   couverture coûtent 59 ms en 15 000 morceaux, 20 ms en 940). Un point ne coûte
   presque rien. La sphère est donc POINTILLÉE — et un point posé sur un chemin
   dit encore le chemin. */
var _tamp=null, _imgs=null, _nTr=0, _nGr=0;
window._compteTr=function(){return {trainees:_nTr, grains:_nGr};};
function tampons(GS){
  if(_tamp && _tamp.length===GS.length && _imgs[0].width===MAS_BOX*MAS_D) return;
  _tamp=[]; _imgs=[];
  for(var i=0;i<GS.length;i++){
    var im=GS[i].createImageData(MAS_BOX*MAS_D, MAS_BOX*MAS_D);
    _imgs.push(im); _tamp.push(new Uint32Array(im.data.buffer));
  }
}
function argb(hex,a){
  var r=parseInt(hex.substr(1,2),16), g=parseInt(hex.substr(3,2),16), b=parseInt(hex.substr(5,2),16);
  return ((a&255)<<24)|((b&255)<<16)|((g&255)<<8)|(r&255);
}
/* ⚑ LE GRAIN N'EST PLUS UN PIXEL. C'est un TAMPON.
   Le carré aligné sur la grille faisait « pixel Windows 98 », et c'était la technique
   qui l'imposait : putImageData n'écrit que des entiers. On dessine donc le grain
   UNE FOIS dans un petit canevas — rond, anticrénelé, bouts ronds — on lit ses pixels,
   et on les TAMPONNE dans le tampon. Le grain a une main ; le coût ne bouge pas.
   Mesuré (scratchpad/banc5.py), quatre toiles, l'intervalle réel entre deux images :
     carré au pixel   20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,67   64 000 → 16,67
     TAMPON DE GRAIN  20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,79   64 000 → 16,79
     drawImage         20 000 → 48,55 ms   34 000 → 80,35   48 000 → 112,49  64 000 → 151,11
   drawImage par grain est hors budget d'un facteur trois — c'est l'appel qui coûte,
   pas les pixels. Le tampon, lui, ne coûte rien de plus que le carré.
   LE TAMPON GARDE LE PLUS OPAQUE (et non « le dernier ») : deux grains qui se croisent
   ne s'effacent pas l'un l'autre, le plus présent gagne. */
/* ⚑ LE GRAIN EST UNE DALLE. UNE VRAIE, DU MOTEUR.
   La sphère est faite de la même matière que la Toile : un seul langage sur tout le
   produit, et l'Aura change d'aspect quand on change de monde au Studio.
   La mécanique ne bouge pas — c'est l'atlas de tampons qui change de contenu :
   on rend HUIT dalles du moteur (Toile.dalleTrame, échelle 1, jamais plus) dans un
   canevas de 56, on les réduit à trois tailles minuscules, on lit leurs pixels, et
   on les tamponne. Même mécanique, même coût. `drawImage` par grain reste hors
   budget d'un facteur trois — mesuré, on n'y revient pas.
   ⚠ LA DALLE GARDE SES COULEURS : ce n'est plus une encre, c'est la matière du monde.
   Seule son ALPHA est multipliée par le niveau de profondeur. */
/* ⚑ LA MÊME DALLE, DEUX TEINTES POSSIBLES — et je les livre toutes les deux.
     'monde'  la dalle garde SES couleurs. C'est la Toile, littéralement.
     'encre'  on ne garde que sa FORME, peinte dans l'encre de l'écran.
   Dans les deux cas c'est la vraie dalle du moteur, et dans les deux cas l'Aura
   change quand on change de monde — mais l'une change de COULEUR, l'autre de FORME.
   Mon avis, mesuré et regardé, est écrit dans la planche. */
var MAS_TEINTE='encre';   /* TRANCHÉ (Tom) : on garde la FORME de la dalle, peinte dans
                             l'encre de l'écran. Le terracotta d'un monde est exactement
                             « à tenir » — la matière ne doit pas parler le langage des états. */
var GR_TAI=3, GR_PX=[3,4,6];          /* trois tailles de dalle, en pixels d'appareil */
var GR_IDS=[1,2,3,4,5,6,7,8];         /* huit dalles : de quoi ne jamais voir de motif */
var GR_N=GR_IDS.length;
var _atlasCache={};
var _TG=[Math.tan(Math.PI/24),Math.tan(3*Math.PI/24),Math.tan(5*Math.PI/24),
         Math.tan(7*Math.PI/24),Math.tan(9*Math.PI/24),Math.tan(11*Math.PI/24)];
function faitAtlas(ink,teinte,monde){
  teinte=teinte||MAS_TEINTE;
  var m=monde||null;
  if(!m){ try{ m=window.Toile&&Toile.mondeCourant?Toile.mondeCourant():null; }catch(e){} }
  var cle=ink+'|'+teinte+'|'+(m?m.m+'/'+m.p+'/'+m.h:'?')+'|'+MAS_BOX+'/'+MAS_D;
  if(_atlasCache[cle]) return _atlasCache[cle];
  var att=(ink===ENCRE?0.86:1);
  var Wd=MAS_BOX*MAS_D;
  var encreRGB=(parseInt(ink.substr(5,2),16)<<16)|(parseInt(ink.substr(3,2),16)<<8)|parseInt(ink.substr(1,2),16);
  var gros=document.createElement('canvas'); gros.width=56; gros.height=56;
  var petit=document.createElement('canvas');
  var A=[];
  for(var d=0;d<GR_N;d++){
    /* LA VRAIE DALLE DU MOTEUR, à l'échelle 1 — jamais un polygone reconstruit */
    /* LA VRAIE DALLE, DANS LE MONDE DEMANDÉ — quatrième argument du moteur */
    try{ window.Toile && Toile.dalleTrame(gros, GR_IDS[d], 1, m||undefined); }catch(e){}
    for(var t=0;t<GR_TAI;t++){
      var px=GR_PX[t];
      petit.width=px; petit.height=px;
      var gp=petit.getContext('2d');
      gp.clearRect(0,0,px,px);
      gp.imageSmoothingEnabled=true;
      gp.drawImage(gros,0,0,px,px);
      var dat=gp.getImageData(0,0,px,px).data;
      for(var n=0;n<MAS_NS;n++){
        var q=(n+0.5)/MAS_NS;
        var mul=(MAS_A0+(MAS_A1-MAS_A0)*q*q*q)*att;   /* la profondeur s'éteint vite */
        var offs=[], vals=[];
        var ox=px>>1, oy=px>>1;
        for(var y=0;y<px;y++)for(var x=0;x<px;x++){
          var i4=(y*px+x)*4, al=(dat[i4+3]*mul)|0;
          if(al>3){ offs.push((y-oy)*Wd+(x-ox));
            var rgb = teinte==='encre' ? encreRGB
                    : ((dat[i4+2]<<16)|(dat[i4+1]<<8)|dat[i4]);
            vals.push((((al&255)<<24)|rgb)>>>0); }
        }
        A.push({n:offs.length, off:new Int32Array(offs), val:new Uint32Array(vals)});
      }
    }
  }
  _atlasCache[cle]=A;
  window._grainsAtlas=A.length;
  return A;
}
/* ⚑ LE DOIGT CREUSE FRANCHEMENT, ET LA TRACE RESTE.
   Chaque contact pousse la matière RADIALEMENT, dans tous les sens à partir du point
   touché — et fort : quarante-six pixels au cœur, sur un rayon de soixante-dix-huit.
   La matière FUIT, on voit le trou s'ouvrir.
   ⚠ ELLE GLISSE SUR LA SURFACE, elle ne quitte pas la boule : un point poussé au-delà
   de la silhouette est ramené dessus. C'est ce qui permet de creuser fort sans mordre
   le bord — la première version à 72/30 cassait la silhouette et on voyait un objet
   mordu, pas un objet qui encaisse.
   LA TRACE DURE : après le lâcher, exp(−t/1,35) — cinq secondes avant de disparaître.
   ET ELLE SE COMBLE QUAND ON LANCE : la matière qui file par-dessus la remplit,
   proportionnellement à la vitesse. On creuse, on lance, ça se rebouche. */
var IMP_R=66, IMP_A=34, IMP_TAU=1.35, IMP_MONTE=0.09, IMP_MAX=6, IMP_COMBLE=0.42;
function majImpacts(f,now,dt,aom){
  var L=f.__imp; if(!L||!L.length) return 0;
  var n=0;
  for(var i=0;i<L.length;i++){
    var m=L[i];
    if(m.tr===0) m.e=Math.min(1,(now-m.t0)/1000/IMP_MONTE);
    else {
      m.e=m.eRel*Math.exp(-(now-m.tr)/1000/IMP_TAU);
      /* ⚑ LE COMBLEMENT PAR LA VITESSE — on retranche, on ne remplace pas :
         un creux qu'on lance se rebouche d'autant plus vite qu'on lance fort. */
      m.comble=(m.comble||0)+IMP_COMBLE*aom*dt;
      m.e=Math.max(0,m.e-m.comble);
    }
    /* on ne jette que ce qui est LÂCHÉ ET ÉTEINT : un creux naissant vaut zéro à sa
       première image, le jeter là c'est ne jamais rien creuser. */
    if(m.tr===0 || m.e>0.02) L[n++]=m;
  }
  L.length=n;
  return n;
}
function dessineMasse(f,lac,tan,om){
  var GS=f.__masG; if(!GS) return;
  tampons(GS);
  var ATL=faitAtlas(f.__ink, f.__teinte, f.__monde);
  var A=fabriqueMasse(), N=A.length/5, S=_seaux, cpt=_cpt;
  for(var z0=0;z0<cpt.length;z0++) cpt[z0]=0;
  var ret=Math.max(-LAG_MAX,Math.min(LAG_MAX,(om||0)*LAG_K));
  var LC=_lc, LS=_ls, tms=performance.now();
  for(var L=0;L<LAG_N;L++){
    /* la dérive propre de la bande + le retard dû au geste : les deux s'ajoutent */
    var der=DER_AMP[L]*Math.sin(tms/DER_PER[L]*6.2832+DER_PH[L]);
    var a2=lac+der-ret*(L/(LAG_N-1));
    LC[L]=Math.cos(a2); LS[L]=Math.sin(a2);
  }
  var tanR=tan+TAN_AMP*Math.sin(tms/TAN_PER*6.2832);
  var CT=Math.cos(tanR), ST=Math.sin(tanR);
  var CX=MAS_BOX/2, CY=MAS_BOX/2, R=MAS_R, F=MAS_FOC, W=MAS_BOX*MAS_D, MARGE=13;
  var aom=Math.abs(om||0);
  var now=performance.now(), dt=Math.min(0.05,(now-(f.__tm||now))/1000); f.__tm=now;
  var nImp=majImpacts(f, now, dt, aom), IMPS=f.__imp;
  /* la silhouette, en pixels d'appareil : la matière glisse dessus, jamais dehors */
  var SIL=0;
  for(var zt=-1;zt<=1.0001;zt+=0.02){
    var xy=Math.sqrt(Math.max(0,1-zt*zt))*R, kk=F/(F-zt*R);
    if(xy*kk>SIL) SIL=xy*kk;
  }
  SIL*=MAS_D;
  var CXD=CX*MAS_D, CYD=CY*MAS_D;
  /* ⚑ LA TRAÎNÉE SUIT LE VRAI CHEMIN DU GRAIN — pas une direction reconstruite.
     On garde la position de l'image précédente et on tamponne LE LONG du segment
     réellement parcouru. Rotation, cisaillement du retard, poussée du doigt : tout y
     est, par construction. L'ancienne version orientait le grain sur la dérivée de la
     rotation SEULE — le doigt poussait la matière dans un sens et la traînée pointait
     dans un autre. C'était ça, l'effet plaqué. */
  var PR=f.__prev;
  if(!PR || PR.length<N*2){ PR=f.__prev=new Float32Array(N*2); f.__prevOK=false; }
  var ok=f.__prevOK;
  /* ⚑ EN PLEINE ROTATION, ON EN DESSINE MOINS — et personne ne peut le voir.
     Un grain qui file porte en plus jusqu'à trois tampons de traînée : le coût
     triple exactement au moment où il faut de la marge. À cette vitesse l'œil ne
     résout plus une dalle, il voit un flux. Un sur deux au-delà d'une rotation par
     seconde, un sur trois au-delà de deux et demie. La densité perçue ne bouge pas :
     chaque dalle restante traîne. */
  var saut=(aom>2.5?3:(aom>1.0?2:1));
  _nTr=0; _nGr=0;
  for(var i2=0;i2<N;i2++){
    var o=i2*5, t, lg=A[o+3], c=LC[lg], s=LS[lg];
    var X=A[o]*c+A[o+2]*s, Zs=-A[o]*s+A[o+2]*c;
    t=A[o+1]*CT-Zs*ST; var Z=A[o+1]*ST+Zs*CT, Y=t;
    var k=F/(F-Z*R);
    var zz=(Z+1)*0.5;
    var b=(zz*MAS_NS)|0; if(b>=MAS_NS)b=MAS_NS-1; if(b<0)b=0;
    var tr2=(zz*MAS_TR)|0; if(tr2>=MAS_TR)tr2=MAS_TR-1; if(tr2<0)tr2=0;
    var px=CXD+X*R*k*MAS_D, py=CYD+Y*R*k*MAS_D;
    for(var m2=0;m2<nImp;m2++){
      var im=IMPS[m2]; if(im.e<=0) continue;
      var ddx=px-im.x, ddy=py-im.y, d2=ddx*ddx+ddy*ddy;
      if(d2>im.r2) continue;
      var dd=Math.sqrt(d2); if(dd<0.5) continue;
      var u=1-dd/im.r, ff=u*(0.5+0.5*u);
      /* ⚑ LA POUSSÉE S'ÉTEINT EN APPROCHANT DU LIMBE. La première version RABATTAIT
         les points sur la silhouette : ils s'y empilaient et laissaient une BAIE
         vide — un objet mordu, pas un objet qui encaisse. Ici, plus un grain est
         près du bord, moins il se laisse pousser : la matière fuit à l'intérieur de
         la boule, et la boule reste ronde. */
      var qx=px-CXD, qy=py-CYD, qr=Math.sqrt(qx*qx+qy*qy);
      var marge=(SIL-qr)/(26*MAS_D); if(marge<0)marge=0; if(marge>1)marge=1;
      var pu=IMP_A*MAS_D*im.e*ff*marge;
      px+=ddx/dd*pu; py+=ddy/dd*pu;
    }
    var j2=i2*2, dx=0, dy=0;
    if(ok){ dx=px-PR[j2]; dy=py-PR[j2+1]; }
    PR[j2]=px; PR[j2+1]=py;
    var xi=px|0, yi=py|0;
    if(xi<MARGE||yi<MARGE||xi>W-MARGE||yi>W-MARGE) continue;
    var idx=tr2*MAS_NS+b, p=cpt[idx]*5, T=S[idx];
    T[p]=xi; T[p+1]=yi;
    /* ⚑ LA PROFONDEUR JOUE AUSSI SUR LA TAILLE DE LA DALLE, et c'est ce qui rend le
       volume. En crème sur encre, la luminosité suffisait à dire le relief ; une
       dalle terracotta sur encre a bien moins d'écart, et la sphère s'aplatissait.
       Devant, la dalle monte d'un cran ; au fond, elle en descend un. Le limbe
       redevient un bord, et le devant vient vers toi. */
    var tl=A[o+4]+(b>=5?1:(b<=1?-1:0)); if(tl<0)tl=0; if(tl>GR_TAI-1)tl=GR_TAI-1;
    T[p+2]=((((i2*2654435761)>>>0)%GR_N)*GR_TAI + tl)*MAS_NS + b;
    T[p+3]=dx; T[p+4]=dy;
    cpt[idx]++;
  }
  f.__prevOK=true;
  for(var h=0;h<MAS_TR;h++){
    var B=_tamp[h]; B.fill(0);
    for(var b2=0;b2<MAS_NS;b2++){
      var id2=h*MAS_NS+b2, n2=cpt[id2]; if(!n2) continue;
      /* ⚑ LE LOINTAIN EST PLUS RARE, ET C'EST JUSTE. Les deux niveaux les plus
         lointains sont à un vingtième d'opacité : une dalle sur trois. Les deux
         suivants, une sur deux. Devant, toutes. La sphère y gagne même en volume —
         le fond DOIT être plus clairsemé que le devant. */
      var pas=(b2<2?3:(b2<4?2:1))*saut;
      var T2=S[id2];
      /* le tampon de la traînée : même dalle, deux niveaux plus sourde */
      var bTr=b2>=2?b2-2:0;
      for(var j=0;j<n2;j+=pas){
        var p2=j*5, si=T2[p2+2], sp=ATL[si];
        if(!sp) continue;
        _nGr++;
        var bas=T2[p2+1]*W+T2[p2], of=sp.off, va=sp.val, nn=sp.n, q2, o3, v;
        /* d'abord le chemin parcouru : des tampons ÉCHELONNÉS le long du segment */
        var ddx2=T2[p2+3], ddy2=T2[p2+4];
        var l2=ddx2*ddx2+ddy2*ddy2;
        /* ⚑ LA TRAÎNÉE — RÉÉCRITE, PARCE QU'ELLE N'ARRIVAIT PAS À L'ÉCRAN.
           Prouvé en pixels sur l'image rendue (scratchpad/preuve_geste.py) : pendant
           une rotation, la longueur moyenne des suites allumées valait 5,33 dans le
           sens du mouvement contre 5,41 en travers. AUCUNE anisotropie — donc aucune
           traînée. Deux causes, toutes les deux dans ce bloc :
             1 · LE PAS ÉTAIT CALCULÉ, LE NOMBRE ÉTAIT PLAFONNÉ. À pleine vitesse un
                 grain parcourt ~57 px par image ; quatre tampons répartis dessus, ce
                 sont quatre points isolés tous les 14 px, pas un fil.
                 Maintenant le PAS est fixe (2,5 px) et c'est la LONGUEUR DESSINÉE qui
                 est bornée (34 px) : on dessine la FIN du chemin, dense.
             2 · LE TAMPON GARDE LE PLUS OPAQUE, et je peignais la traînée DEUX NIVEAUX
                 PLUS SOURDE : dans une sphère dense, elle passait sous n'importe quel
                 grain et ne se voyait jamais. Sa tête est maintenant au MÊME niveau
                 que son grain ; c'est la queue qui s'éteint, cran par cran. */
        if(l2>4.0){
          var lon=Math.sqrt(l2);
          var lmax=lon>34?34:lon;
          var nt=(lmax/2.5)|0; if(nt>12)nt=12;
          if(nt>0){
            _nTr+=nt;
            var dalle=(((si/MAS_NS)|0)/GR_TAI)|0;
            var kx=-ddx2/lon*2.5, ky=-ddy2/lon*2.5;
            for(var q3=1;q3<=nt;q3++){
              var niv=b2-((q3*3/nt)|0); if(niv<0)niv=0;
              var spT=ATL[dalle*GR_TAI*MAS_NS+niv];
              if(!spT) continue;
              var bx=(T2[p2]+kx*q3)|0, by=(T2[p2+1]+ky*q3)|0;
              if(bx<MARGE||by<MARGE||bx>W-MARGE||by>W-MARGE) continue;
              var bt=by*W+bx, ofT=spT.off, vaT=spT.val, nT=spT.n;
              for(q2=0;q2<nT;q2++){
                o3=bt+ofT[q2]; v=vaT[q2];
                if((v>>>24) > (B[o3]>>>24)) B[o3]=v;
              }
            }
          }
        }
        for(q2=0;q2<nn;q2++){
          o3=bas+of[q2]; v=va[q2];
          if((v>>>24) > (B[o3]>>>24)) B[o3]=v;
        }
      }
    }
  }
}

/* ⚑ LA MATIÈRE SE RETIRE SOUS UN PRÉNOM — et s'écarte devant un visage qui ÉMERGE.
   Les deux se font dans le tampon, en baissant l'octet d'alpha, avec un bord TRAMÉ :
   la matière s'éclaircit par raréfaction, jamais par voile. Puis on verse. */
function poseMatiere(f){
  var GS=f.__masG; if(!GS||!_tamp) return;
  var W=MAS_BOX*MAS_D, ox=(ORB_CX-MAS_BOX/2), oy=(ORB_CY-MAS_BOX/2), MG=3;
  var boites=f.__bo||(f.__bo=[]); boites.length=0;
  f.querySelectorAll('.orb').forEach(function(w){
    if(!w.__pos||!w.__nom) return;
    var lg=(w.__nom.__lg||58);
    boites.push({x:(w.__pos.x-ox+(62-lg)/2-MG)*MAS_D, y:(w.__pos.y-oy-MG)*MAS_D,
                 w:(lg+MG*2)*MAS_D, h:(18+MG*2)*MAS_D});
  });
  var devant=f.__dv||(f.__dv=[]); devant.length=0;
  f.querySelectorAll('.orb').forEach(function(w){
    if(!w.__pr) return;
    /* ⚑ IL SORT DE LA MATIÈRE. Plus il vient vers toi, plus la matière s'écarte de
       lui : au fond elle le recouvre presque entièrement, devant elle lui laisse la
       place. Ce n'est pas un calque qui s'allume, c'est un dégagement progressif. */
    var av=(w.__z+MAS_R)/(2*MAS_R); if(av<0)av=0; if(av>1)av=1;
    devant.push({x:(ORB_CX+w.__pr.x-ox)*MAS_D, y:(ORB_CY+w.__pr.y-oy)*MAS_D,
                 r:(w.__d/2+3)*MAS_D, z:w.__z, fa:0.12+0.80*(1-av)});
  });
  var DIT=13*MAS_D/2;
  for(var h=0;h<GS.length;h++){
    var B=_tamp[h];
    for(var i=0;i<boites.length && !window.__sansClairiere;i++){
      var b=boites[i], rd=b.h/2;
      var x1=Math.max(0,(b.x-DIT)|0), y1=Math.max(0,(b.y-DIT)|0);
      var x2=Math.min(W,(b.x+b.w+DIT)|0), y2=Math.min(W,(b.y+b.h+DIT)|0);
      var cxl=b.x+rd, cxr=b.x+b.w-rd, cyc=b.y+rd;
      for(var y=y1;y<y2;y++){
        var dyv=y-cyc, row=y*W;
        for(var x=x1;x<x2;x++){
          var dd;
          if(x<cxl){ var dxv=x-cxl; dd=Math.sqrt(dxv*dxv+dyv*dyv)-rd; }
          else if(x>cxr){ var dxr=x-cxr; dd=Math.sqrt(dxr*dxr+dyv*dyv)-rd; }
          else dd=Math.abs(dyv)-rd;
          if(dd>DIT) continue;
          var v=B[row+x]; if(!v) continue;
          var fa;
          if(dd<=0) fa=0.06;
          else { var hsh=((x*7+y*11)>>1)&3;
                 if(dd<=DIT*0.5) fa=(hsh?0.10:1); else fa=((hsh&1)?0.10:1); }
          if(fa===1) continue;
          B[row+x]=(v&0x00FFFFFF)|((((v>>>24)*fa)|0)<<24);
        }
      }
    }
    for(var j2=0;j2<devant.length;j2++){
      var q=devant[j2]; if(q.z>=f.__masZ[h]) continue;
      var rr=q.r, re=rr+DIT, re2=re*re;
      var ya=Math.max(0,(q.y-re)|0), yb=Math.min(W,(q.y+re)|0);
      var xa=Math.max(0,(q.x-re)|0), xb=Math.min(W,(q.x+re)|0);
      for(var y3=ya;y3<yb;y3++){
        var dy3=y3-q.y, row3=y3*W;
        for(var x3=xa;x3<xb;x3++){
          var dx3=x3-q.x, dq=dx3*dx3+dy3*dy3; if(dq>re2) continue;
          var v3=B[row3+x3]; if(!v3) continue;
          var fb;
          if(dq<=rr*rr) fb=q.fa;
          else { var h3=((x3*7+y3*11)>>1)&3; fb=(h3?q.fa:1); }
          if(fb===1) continue;
          B[row3+x3]=(v3&0x00FFFFFF)|((((v3>>>24)*fb)|0)<<24);
        }
      }
    }
    GS[h].putImageData(_imgs[h],0,0);
  }
}

function rayonDe(j){
  return ORB_RMIN + (ORB_RMAX-ORB_RMIN)*Math.log(1+j)/Math.log(1+ORB_JMAX);
}
function cleAlpha(n){
  var s=n.toLowerCase().normalize('NFD').replace(/[^a-z]/g,'')+'aaa';
  var v=function(c){return Math.max(0,Math.min(25,c.charCodeAt(0)-97));};
  return v(s[0])*676+v(s[1])*26+v(s[2]);
}
/* la base 3D du plan de l'orbite : deux vecteurs orthonormés */
function basePlan(inc,noeud){
  var ci=Math.cos(inc), si=Math.sin(inc), cn=Math.cos(noeud), sn=Math.sin(noeud);
  return {u:[cn,sn,0], v:[-sn*ci,cn*ci,si]};
}
function point3(r,th,B){
  var c=Math.cos(th), s=Math.sin(th);
  return [r*(c*B.u[0]+s*B.v[0]), r*(c*B.u[1]+s*B.v[1]), r*(c*B.u[2]+s*B.v[2])];
}
/* ⚠ ON BORNE L'ÉCHELLE. Sans bornes, un anneau au premier plan atteignait 129 px —
   presque ton Noyau (90) : la hiérarchie que tu voulais s'effondrait, et la boîte
   sortait du cadre. Bornée à [0,52 · 1,92], la profondeur reste franche et rien
   ne dépasse jamais ton Noyau. */
function projete(P){ var k=Math.max(0.60,Math.min(1.95,FOC/(FOC-P[2])));
  return {x:P[0]*k, y:P[1]*k, k:k}; }
/* LA VUE — lacet puis tangage, appliqués à tout ce qui est dans la sphère. */
function vue(P,lac,tan){
  var c=Math.cos(lac), s=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var X=P[0]*c+P[2]*s, Z=-P[0]*s+P[2]*c;
  var Y=P[1]*ct-Z*st; Z=P[1]*st+Z*ct;
  return [X,Y,Z];
}
function bornTangage(t){ return Math.max(-VUE_TANGMAX,Math.min(VUE_TANGMAX,t)); }

/* ⚠ AUCUN ANNEAU NE PASSE JAMAIS DEVANT TON NOYAU.
   Ce n'est PAS une question de z-index : une orbite trop inclinée TRAVERSE le centre
   à l'écran. On cherche donc, pour chaque personne, la plus grande inclinaison qui
   dégage ton anneau sur SOIXANTE-DOUZE positions du tour, et on garde celle-là. */
function inclinaisonTenable(r, noeud, incVoulue){
  var Rtoi=TOI_D/2, rr=PERS_D/2, MARGE=7;
  /* LA ZONE INTERDITE, c'est TOUT TON NOYAU : l'anneau ET le mot « toi » dessous.
     Une première version ne dégageait que l'anneau — et un prénom, ou un anneau qui
     passait bas, venait recouvrir « toi ». Le contrôle l'a pris. */
  for(var inc=incVoulue; inc>=0; inc-=0.02){
    var B=basePlan(inc,noeud), ok=true;
    for(var s=0;s<96;s++){
      var P3=point3(r, s/96*6.2832, B);
      /* ⚠ LA RÈGLE A CHANGÉ, ET C'EST CE QUI FAIT LA SPHÈRE.
         Interdire tout recouvrement du centre obligeait les orbites à le CONTOURNER :
         personne ne passait jamais derrière, tout le monde restait à côté — un cercle.
         Ce qui est interdit, c'est de passer DEVANT. Derrière, c'est le sujet :
         ton Noyau la masque, franchement. On ne teste donc que la moitié AVANT. */
      if(P3[2] < 0) continue;
      var p=projete(P3);
      var rad=rr*p.k, d=Math.hypot(p.x,p.y);
      /* 1 · l'anneau NI SA LUNE ne touchent le tien. La lune tourne à rad + 9 du
         centre de la personne et fait 5 de rayon : son enveloppe est rad + 14.
         Sans elle, un point terracotta passait devant ton Noyau — pris par le contrôle. */
      if(d < Rtoi + rad + 11 + MARGE){ ok=false; break; }
      /* 2 · SON prénom non plus — il est posé VERS L'EXTÉRIEUR, jamais vers toi,
             mais on le vérifie quand même : c'est la règle, pas une intention. */
      var ux=p.x/(d||1), uy=p.y/(d||1), nd=rad+17;
      var N={x1:p.x+ux*nd-31, x2:p.x+ux*nd+31, y1:p.y+uy*nd-9, y2:p.y+uy*nd+9};
      var nx=Math.max(N.x1,Math.min(0,N.x2)), ny=Math.max(N.y1,Math.min(0,N.y2));
      if(Math.hypot(nx,ny) < Rtoi + MARGE){ ok=false; break; }
    }
    if(ok) return inc;
  }
  return 0;
}
var _plan=null;
function placeOrbite(){
  if(_plan) return _plan;
  _plan = ORBITE.map(function(p){
    /* ⚠ LES PLANS SONT COMPOSÉS À LA MAIN, plus tirés de l'alphabet.
       L'alphabet répartissait les orbites régulièrement — et une constellation
       régulière est morte, même quand elle tourne. On choisit les noeuds, les
       inclinaisons et les phases pour que les chemins se croisent, se resserrent et
       laissent des vides. LE RAYON, LUI, RESTE LA DATE : la seule chose qu'on ne
       compose pas. */
    var noeud=p.nd*Math.PI/180;
    var voulue=p.inc*Math.PI/180;
    var r=rayonDe(p.j);
    return {p:p, r:r, noeud:noeud, th0:p.ph*Math.PI/180,
            inc:inclinaisonTenable(r,noeud,voulue)};
  });
  /* ⚑ LA BORNE DE LA CALOTTE AVANT, MESURÉE — pas supposée.
     Un anneau atteint au plus r·sin(inc) en profondeur. La calotte qui voile
     commence DIX PIXELS AU-DESSUS de ce maximum : un trait ne peut donc jamais
     voiler un anneau qui est devant lui. */
  MAS_ZMAX=0;
  _plan.forEach(function(q){ MAS_ZMAX=Math.max(MAS_ZMAX, q.r*Math.abs(Math.sin(q.inc))); });
  MAS_SPLIT=Math.min(0.97,(MAS_ZMAX+10)/MAS_R);
  window._masBorne={zmax:+MAS_ZMAX.toFixed(1), split:+(MAS_SPLIT*MAS_R).toFixed(1)};
  return _plan;
}

/* ════════════════════════════════════════════════════════════════════════════
   LA TRAÎNÉE — l'idée forte de ce lot.
   On ne voyait pas le VOLUME parce qu'on ne voyait pas les CHEMINS : six objets
   bougeaient, le cerveau n'avait rien à reconstruire. Chaque personne traîne
   maintenant un arc de SA PROPRE ORBITE derrière elle — une trace, pas un filet :
     · elle s'affine et s'efface en s'éloignant de l'anneau ;
     · sa LARGEUR suit la perspective : fine au loin, large au premier plan ;
     · elle est peinte SOUS ton Noyau, donc elle DISPARAÎT derrière lui et
       reprend de l'autre côté — c'est ça qui dit la profondeur, mieux que la taille ;
     · elle porte la couleur de la NUÉE, comme la piste de l'anneau.
   La lune en a une aussi, minuscule : un point qui traîne dit qu'il tourne ;
   un point posé ne dit rien.
   ════════════════════════════════════════════════════════════════════════════ */
/* la traînée DIT un chemin, elle ne se regarde pas : courte, sourde, presque effacée */
var TRACE_LONG=0.085, TRACE_N=20, TRACE_NIV=6;
/* ⚑ LA TRAÎNÉE COÛTAIT PLUS CHER QUE LA SPHÈRE — et je ne l'aurais jamais deviné.
   Profilé : la masse 1,94 ms en moyenne, 2,10 au pire, sur 12 900 points.
   La traînée, 0,27 ms en moyenne — et **20,3 ms au pire**. C'était elle, les douze
   images perdues, pas la sphère. Deux causes, deux correctifs :
     1 · sa toile faisait 390 × 844 (1,3 million de pixels effacés à chaque image)
         alors que tout ce qu'elle dessine tient dans la sphère → 344 × 344.
     2 · elle appelait stroke() UNE FOIS PAR SEGMENT — 200 fois par image. Le banc
         l'avait dit : le coût d'un trait est dans son NOMBRE. Les segments sont
         maintenant groupés par niveau d'opacité : 6 strokes par personne au lieu
         de 20, et 3 pour sa lune au lieu de 12. */
/* ⚠ ON NE RÉALLOUE PLUS RIEN À CHAQUE IMAGE. Les tableaux de segments étaient
   recréés soixante fois par seconde : le ramasse-miettes rendait une image à 20 ms
   environ une fois sur cent cinquante. Ils vivent maintenant à côté de la fonction. */
var _seg=null, _lune=null;
function dessineTraces(f,u){
  var cv=f.__trace; if(!cv) return;
  var g=cv.getContext('2d');
  var CX=MAS_BOX/2, CY=MAS_BOX/2;
  g.setTransform(2,0,0,2,0,0);
  g.clearRect(0,0,MAS_BOX,MAS_BOX);
  g.lineCap='butt';
  var i, n;
  var LAC=f.__lac||0, TAN=(f.__tan===undefined?VUE_TANG:f.__tan);
  /* ⚑ LA TRAÎNÉE NAÎT DE L'ACCÉLÉRATION, ET DE RIEN D'AUTRE.
     Au repos il n'y en a aucune : l'orbite met quatre minutes, une trace n'y dirait
     rien et ne ferait que du bruit. Plus on lance fort, plus elle s'étire —
     PROPORTIONNELLEMENT. Et elle est EFFILOCHÉE : chaque pas est dispersé d'un cran
     par un hachage stable, et son opacité saute — un fil qui se défait, pas un arc. */
  var EL=Math.max(0,Math.min(1,(Math.abs(f.__om||0)-VUE_AUTO)/3.2));
  if(!_seg){ _seg=[]; for(n=0;n<TRACE_NIV;n++) _seg.push([]); _lune=[[],[],[]]; }
  var seg=_seg;
  f.querySelectorAll('.orb').forEach(function(w){
    var B=basePlan(+w.dataset.inc,+w.dataset.noeud), th0=+w.dataset.th0;
    /* la traînée suit LE MÊME rayon que l'anneau, retour d'ouverture compris :
       sinon elle décrocherait du chemin réel pendant la seconde et demie. */
    var r=retourOuverture(w, +w.dataset.r, f.__ms===undefined?1e9:f.__ms);
    var col=w.dataset.piste, kmoy=0;
    if(EL<=0.02) return;               /* au repos, AUCUNE traînée */
    for(n=0;n<TRACE_NIV;n++) seg[n].length=0;
    for(i=0;i<TRACE_N;i++){
      var f1=i/TRACE_N*EL, f2=(i+1)/TRACE_N*EL;
      var a=projete(vue(point3(r, th0+(u-f1*TRACE_LONG)*6.2832, B), LAC, TAN));
      var b=projete(vue(point3(r, th0+(u-f2*TRACE_LONG)*6.2832, B), LAC, TAN));
      var t=1-i/TRACE_N;
      /* ⚑ L'IDÉE — ET C'EST UNE SOUSTRACTION : LA TRAÎNÉE S'ÉTEINT DERRIÈRE.
         Chaque pas est éclairé par sa PROFONDEUR : vif quand il vient vers toi,
         presque nul quand il s'enfonce. Comme une comète. La moitié arrière du
         chemin ne se dessine plus, elle se devine. */
      var prof=Math.max(0.10, Math.min(1, 0.5 + a.k*0.42));
      var hz=((i*2654435761)>>>0)%97/97;
      var al=Math.pow(t,2.3)*0.34*prof*EL*(0.45+0.75*hz);
      var lv=Math.min(TRACE_NIV-1, Math.max(0, Math.round(al/0.30*(TRACE_NIV-1))));
      /* l'effilochage : chaque pas glisse d'un cran hors de la ligne */
      var ex=(hz-0.5)*3.4*t, ey=((((i*40503)>>>0)%89/89)-0.5)*3.4*t;
      seg[lv].push(CX+a.x+ex, CY+a.y+ey, CX+b.x+ex, CY+b.y+ey);
      kmoy+=a.k;
    }
    kmoy/=TRACE_N;
    g.strokeStyle=col;
    for(n=0;n<TRACE_NIV;n++){
      var A=seg[n]; if(!A.length) continue;
      g.globalAlpha=0.34*EL*n/(TRACE_NIV-1);
      g.lineWidth=Math.max(0.4, PERS_ARC*kmoy*0.52*(0.35+0.65*n/(TRACE_NIV-1)));
      g.beginPath();
      for(i=0;i<A.length;i+=4){ g.moveTo(A[i],A[i+1]); g.lineTo(A[i+2],A[i+3]); }
      g.stroke();
    }
    /* la traînée de la lune : neuf pas, minuscule, trois niveaux */
    if(w.dataset.lune==='1'){
      var pr=projete(vue(point3(r, th0+u*6.2832, B), LAC, TAN)), d=PERS_D*pr.k;
      var L=_lune; L[0].length=0; L[1].length=0; L[2].length=0;
      for(var k=0;k<9 && EL>0.02;k++){
        var b1=(u-k/12*0.055)*6*6.2832+th0, R=d/2+7;
        var b2=(u-(k+1)/12*0.055)*6*6.2832+th0;
        L[k<3?2:(k<6?1:0)].push(CX+pr.x+R*Math.cos(b1), CY+pr.y+R*Math.sin(b1),
                                CX+pr.x+R*Math.cos(b2), CY+pr.y+R*Math.sin(b2));
      }
      g.strokeStyle=TERRA;
      for(n=0;n<3;n++){
        var M=L[n]; if(!M.length) continue;
        g.globalAlpha=0.85*(n+1)/3;
        g.lineWidth=Math.max(0.5,3.4*pr.k*(n+1)/3);
        g.beginPath();
        for(i=0;i<M.length;i+=4){ g.moveTo(M[i],M[i+1]); g.lineTo(M[i+2],M[i+3]); }
        g.stroke();
      }
    }
  });
  g.globalAlpha=1;
}

/* ⚑ LE DOIGT — deux gestes, un seul capteur.
   UN TOUCHER ouvre la fiche de la personne. UN GLISSEMENT tourne la sphère.
   On ne peut pas mettre l'écoute sur chaque anneau : le doigt part souvent d'un
   anneau et le glissement serait mangé. On pose donc UNE surface transparente sur
   la sphère, on mesure la distance parcourue, et on tranche À LA LEVÉE :
   au-delà de six pixels c'était une rotation, en deçà c'était un toucher — et on
   cherche alors qui est sous le doigt, le plus proche du regard d'abord. */
function prise(f){
  var cap=el('div','prise','left:'+(ORB_CX-MAS_BOX/2)+'px;top:'+(ORB_CY-MAS_BOX/2)+'px;'
    +'width:'+MAS_BOX+'px;height:'+MAS_BOX+'px;z-index:60;touch-action:none;cursor:grab');
  f.appendChild(cap);
  /* ⚠ AUCUNE ALLOCATION PENDANT LE GESTE. Un objet par mouvement de doigt, ce sont
     quatre-vingts objets par seconde jetés au ramasse-miettes — mesuré : une image à
     25,8 ms au milieu d'une rotation. L'historique est un anneau de nombres, écrit
     en place, jamais réalloué. */
  var px=0, py=0, parcouru=0, HN=16;
  var hT=new Float64Array(HN), hL=new Float64Array(HN), hG=new Float64Array(HN), hi=0, hn=0;
  function angle(e){ return {x:e.clientX, y:e.clientY}; }
  cap.addEventListener('pointerdown',function(e){
    /* ⚠ L'ÉTAT D'ABORD, LA CAPTURE ENSUITE. setPointerCapture peut lever — et si
       elle lève en premier, `f.__prise` n'est jamais posé : plus aucun geste ne
       fonctionne, sans une seule erreur visible à l'écran. Mesuré : le toucher ne
       partait pas du tout, et le contrôle disait « rien » sur les trois cas. */
    f.__prise=true;
    try{ cap.setPointerCapture(e.pointerId); }catch(err){} f.__vlac=0; f.__vtan=0; parcouru=0; hn=0; hi=0;
    var p=angle(e); px=p.x; py=p.y; cap.style.cursor='grabbing';
    /* ⚑ CHAQUE CONTACT CREUSE. Ils s'EMPILENT — on peut toucher ailleurs tout de
       suite, le creux précédent est encore en train de se refermer. Six au plus ;
       au-delà, le plus vieux sort. Rien ne se fige jamais. */
    var r=cap.getBoundingClientRect();
    if(!f.__imp) f.__imp=[];
    if(f.__imp.length>=IMP_MAX) f.__imp.shift();
    f.__creux={x:(p.x-r.left)*MAS_D, y:(p.y-r.top)*MAS_D, r:IMP_R*MAS_D,
               r2:IMP_R*MAS_D*IMP_R*MAS_D, t0:performance.now(), tr:0, e:0, eRel:0, comble:0};
    f.__imp.push(f.__creux);
    e.preventDefault();
  });
  cap.addEventListener('pointermove',function(e){
    if(!f.__prise) return;
    var p=angle(e), dx=p.x-px, dy=p.y-py; px=p.x; py=p.y;
    parcouru += Math.hypot(dx,dy);
    /* le sens est celui du doigt : la surface qu'on touche suit la main. */
    f.__lac = (f.__lac||0) + dx*VUE_SENS;
    f.__tan = bornTangage((f.__tan===undefined?VUE_TANG:f.__tan) - dy*VUE_SENS);
    hT[hi]=performance.now(); hL[hi]=dx*VUE_SENS; hG[hi]=-dy*VUE_SENS;
    hi=(hi+1)%HN; if(hn<HN) hn++;
    if(f.__creux){ var rc=cap.getBoundingClientRect();
      f.__creux.x=(p.x-rc.left)*MAS_D; f.__creux.y=(p.y-rc.top)*MAS_D; }
    e.preventDefault();
  });
  function lacher(e){
    if(!f.__prise) return;
    f.__prise=false; cap.style.cursor='grab';
    /* on lâche : le creux se referme en exp(−t/0,28) — la matière encaisse et revient */
    if(f.__creux){ f.__creux.eRel=f.__creux.e; f.__creux.tr=performance.now(); f.__creux=null; }
    if(parcouru<=TAP_SEUIL){ toucher(f,e); f.__vlac=0; f.__vtan=0; return; }
    /* L'ÉLAN : la vitesse des quatre-vingt-dix dernières millisecondes, bornée. */
    var now=performance.now(), sl=0, st=0, t0=now;
    for(var i=0;i<hn;i++){
      var j=(hi-1-i+HN*2)%HN;
      if(now-hT[j]>90) break;
      sl+=hL[j]; st+=hG[j]; t0=hT[j];
    }
    var dtt=(now-t0)/1000;
    if(dtt>0.012){
      f.__vlac=Math.max(-VUE_VMAX,Math.min(VUE_VMAX, sl/dtt));
      f.__vtan=Math.max(-VUE_VMAX,Math.min(VUE_VMAX, st/dtt));
    }
  }
  cap.addEventListener('pointerup',lacher);
  cap.addEventListener('pointercancel',lacher);
  return cap;
}
/* qui est sous le doigt ? le plus proche du regard gagne. */
function toucher(f,e){
  var F=f.getBoundingClientRect();
  var x=e.clientX-F.left, y=e.clientY-F.top, best=null, bz=-1e9;
  /* ⚠ ON NE TOUCHE PAS QUELQU'UN À TRAVERS TON NOYAU. Il est au premier plan quoi
     qu'il arrive ; une personne qui passe dessous est INVISIBLE. Ouvrir sa fiche
     depuis un doigt posé sur ton propre visage serait incompréhensible. */
  if(Math.hypot(x-ORB_CX,y-ORB_CY) <= TOI_D/2) return;
  f.querySelectorAll('.orb').forEach(function(w){
    if(!w.__pr) return;
    var cx=ORB_CX+w.__pr.x, cy=ORB_CY+w.__pr.y;
    if(Math.hypot(cx-ORB_CX,cy-ORB_CY) < TOI_D/2 - w.__d/2 + 4) return;   /* cachée */
    /* ⚑ LA ZONE TOUCHABLE DÉBORDE L'ANNEAU DE 14 px. Un anneau au fond fait 25 px :
       viser un disque de 12 px de rayon au doigt, sur un objet qui tourne, c'est
       s'y reprendre. On vise large, et LE PLUS PROCHE DU REGARD GAGNE — c'est ce qui
       rend le débordement sans danger quand deux personnes se croisent. */
    if(Math.hypot(x-cx,y-cy) <= w.__d/2 + 14 && w.__z>bz){ bz=w.__z; best=w; }
  });
  if(best) ouvrePersonne(best.dataset.qui);
}
/* ⚠ SUR LA PLANCHE, `openPerson` N'EXISTE PAS — c'est une fonction de l'app.
   On la remplace ici par une trace visible, et on le DIT : le branchement se fera
   au lot d'intégration. Le geste, lui, est réel et mesuré. */
function ouvrePersonne(n){
  window._dernierTouche=n;
  var b=document.getElementById('tapEcho');
  if(b){ b.textContent='toucher → openPerson(« '+n+' »)'; b.style.opacity='1';
    clearTimeout(b.__t); b.__t=setTimeout(function(){b.style.opacity='0';},1600); }
}

function orbite(f,ink){
  placeOrbite();                       /* la borne de la calotte est mesurée ici */
  /* ⚑ DEUX TOILES POUR LA MASSE, ET C'EST CE QUI MET LES SIX *DEDANS*.
     Une seule toile sous tout le monde et les anneaux flotteraient DESSUS.
     Ici la moitié arrière est peinte SOUS eux (z 4) et la calotte avant PAR-DESSUS
     (z 36) : un anneau qui s'enfonce passe derrière la matière, et se voile.
     La calotte reste sous ton Noyau (z 40) — rien ne passe jamais devant toi. */
  function toileMasse(z){
    var m=document.createElement('canvas');
    m.width=MAS_BOX*MAS_D; m.height=MAS_BOX*MAS_D;
    m.style.cssText='position:absolute;left:'+(ORB_CX-MAS_BOX/2)+'px;top:'+(ORB_CY-MAS_BOX/2)
      +'px;width:'+MAS_BOX+'px;height:'+MAS_BOX+'px;z-index:'+z+';pointer-events:none';
    m.dataset.role='masse';
    f.appendChild(m); return m.getContext('2d');
  }
  /* le z-index d'une tranche est CELUI QUE LA FORMULE DES ANNEAUX LUI DONNERAIT :
     20 + z/10, avec z le milieu de la tranche. Les six et la matière sont rangés
     par la même règle — c'est la seule façon d'être vraiment DEDANS. */
  f.__masG=[]; f.__masZ=[];
  for(var _t=0;_t<MAS_TR;_t++){
    var zmid=(-1+(_t+0.5)*2/MAS_TR)*MAS_R;
    f.__masZ.push(zmid);
    f.__masG.push(toileMasse(Math.round(20+zmid/10)));
  }
  /* la toile des traînées : SOUS tout le monde, et sous ton Noyau */
  var tc=document.createElement('canvas');
  tc.width=MAS_BOX*2; tc.height=MAS_BOX*2;
  tc.style.cssText='left:'+(ORB_CX-MAS_BOX/2)+'px;top:'+(ORB_CY-MAS_BOX/2)+'px;'
    +'width:'+MAS_BOX+'px;height:'+MAS_BOX+'px;z-index:30;pointer-events:none';
  f.appendChild(tc); f.__trace=tc;
  /* TON NOYAU — épaissi : 96 / arc 14. Toujours au premier plan. */
  var box=el('div',null,'left:'+(ORB_CX-TOI_D/2)+'px;top:'+(ORB_CY-TOI_D/2)+'px;'
    +'width:'+TOI_D+'px;height:'+TOI_D+'px;z-index:40');
  var cv=document.createElement('canvas'); cv.style.cssText='position:absolute;left:0;top:0';
  cv.dataset.forme='anneau'; cv.dataset.rayon=(TOI_D/2);
  box.appendChild(cv); f.appendChild(box);
  anneau(cv,TOI_D,TOI_ARC,partsArc(),BLEU,null);
  var vd=TOI_VIS;
  var v=el('div',null,'left:'+(ORB_CX-vd/2)+'px;top:'+(ORB_CY-vd/2)+'px;'
    +'width:'+vd+'px;height:'+vd+'px;z-index:41');
  v.innerHTML=visage(vd,BLEU); f.appendChild(v);
  /* ⚠ LE MOT « toi » EST RETIRÉ, et ce n'est pas un oubli.
     Il occupe la bande juste sous ton Noyau — exactement là où passe une personne
     qui arrive par le bas. Le garder obligeait à pousser l'orbite minimale de 78 à
     106 px, c'est-à-dire à GROSSIR l'orbite que tu venais de me demander de resserrer.
     Et il ne dit rien qu'on ne voie déjà : tu es au centre, tu es le plus gros, tu as
     ton visage. C'est « ce qui est petit peut disparaître ». */

  /* LES PERSONNES — 48 / arc 4, amincis pour que la hiérarchie saute aux yeux */
  /* ⚑ LE VISAGE RENTRE DANS L'ANNEAU — il était posé DESSUS. §2.9 donne 36 dans 58,
     soit 0,62 du diamètre ; on était à 0,94, et l'anneau n'était plus qu'un liseré
     autour d'un disque plein. Avec 22 dans 36, le bord intérieur de l'arc est à 11
     et le visage à 11 : la matière de l'anneau est ENTIÈREMENT visible, et c'est elle
     qu'on voit d'abord — pas un pastille de couleur. */
  var VD=22;
  placeOrbite().forEach(function(q){
    var p=q.p;
    var w=el('div','orb','width:'+PERS_D+'px;height:'+PERS_D+'px');
    w.dataset.role='pers';
    w.dataset.r=q.r; w.dataset.inc=q.inc; w.dataset.noeud=q.noeud; w.dataset.th0=q.th0;
    w.dataset.qui=p.n;
    var c=document.createElement('canvas'); c.style.cssText='position:absolute;left:0;top:0';
    c.dataset.forme='anneau'; c.dataset.rayon=(PERS_D/2);
    w.appendChild(c); f.appendChild(w);
    anneau(c,PERS_D,PERS_ARC,p.arc,p.piste,null);
    var fa=el('div',null,'position:absolute;pointer-events:none;left:'+((PERS_D-VD)/2)+'px;top:'+((PERS_D-VD)/2)+'px;'
      +'width:'+VD+'px;height:'+VD+'px');
    fa.innerHTML=visage(VD,p.piste); w.appendChild(fa);
    w.dataset.piste=p.piste;
    if(p.bouge){
      w.dataset.lune='1';
      var mo=el('div','lune','position:absolute;width:9px;height:9px;border-radius:50%;'
        +'background:'+TERRA);
      w.appendChild(mo);
    }
    /* ⚠ LE PRÉNOM NE SUBIT AUCUNE PERSPECTIVE : droit, 13,5 px, toujours.
       Il est posé HORS de la boîte mise à l'échelle, pour ne jamais être déformé. */
    var nm=el('div','bg600 orbnom','font-size:13.5px;text-align:center;width:62px;'
      +'color:'+ink+';pointer-events:none', p.n);
    nm.dataset.role='nom';
    f.appendChild(nm);
    w.__nom=nm;
    /* la clairière se taille sur LE MOT, pas sur la boîte : « Léa » ne creuse pas
       autant que « Marion ». Mesuré une fois, au montage. */
    setTimeout(function(){ try{
      var sp=document.createElement('span');
      sp.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;'
        +'font:600 13.5px "Bricolage Grotesque",sans-serif';
      sp.textContent=p.n; document.body.appendChild(sp);
      nm.__lg=Math.min(62,sp.offsetWidth+4); document.body.removeChild(sp);
    }catch(e){} },0);
  });
  prise(f);          /* le capteur du doigt, posé en dernier : il est au-dessus */
  return f;
}

/* la pose : chacun sur son orbite, à la même vitesse angulaire */
/* ⚑ LE RETOUR VERS LE CENTRE — UNE FOIS, À L'OUVERTURE.
   Ce que le rejeu avait trouvé et qui restait vrai : quand tu reviens sur l'Aura après
   avoir tenu, la personne concernée RENTRE. Une seule fois, une seconde et demie, et
   l'écran se repose — ici Maman, la parole tenue hier. Son rayon part de celui qu'elle
   avait AVANT (seize jours) et rejoint le sien. Lissage d'ordre 5 : aucun à-coup. */
var OUV_MS=1500, OUV_QUI='Maman';
function retourOuverture(w,R,ms){
  if(w.dataset.qui!==OUV_QUI || ms>=OUV_MS) return R;
  var k=1-ms/OUV_MS, e=k*k*k*(k*(k*6-15)+10);
  var avant=ORB_RMIN+(ORB_RMAX-ORB_RMIN)*Math.log(1+16)/Math.log(1+ORB_JMAX);
  return R + (avant-R)*e;
}
function orbitePose(f,u,ms){
  f.__u=u;      /* la phase courante : un contrôle doit pouvoir REJOUER la même */
  if(ms!==undefined) f.__ms=ms;
  f.querySelectorAll('.orb').forEach(function(w){
    var r=retourOuverture(w, +w.dataset.r, f.__ms===undefined?1e9:f.__ms);
    var B=basePlan(+w.dataset.inc, +w.dataset.noeud);
    var th=+w.dataset.th0 + u*6.2832;
    var P=vue(point3(r,th,B), f.__lac||0, f.__tan===undefined?VUE_TANG:f.__tan);
    var pr=projete(P);
    var d=PERS_D*pr.k;                       /* la perspective : plus loin = plus petit */
    w.style.width=d+'px'; w.style.height=d+'px';
    w.style.left=(ORB_CX+pr.x-d/2)+'px';
    w.style.top =(ORB_CY+pr.y-d/2)+'px';
    w.style.zIndex=String(Math.round(20+P[2]/10));   /* toi restes à 40 : toujours devant */
    var c=w.querySelector('canvas'); if(c){c.style.width=d+'px'; c.style.height=d+'px';}
    var fa=w.children[1]; if(fa){var vd=22*pr.k;
      fa.style.width=vd+'px'; fa.style.height=vd+'px';
      fa.style.left=((d-vd)/2)+'px'; fa.style.top=((d-vd)/2)+'px';
      var sv=fa.querySelector('svg'); if(sv){sv.setAttribute('width',vd); sv.setAttribute('height',vd);} }
    var mo=w.querySelector('.lune');
    /* la lune tourne à SA vitesse — six tours quand l'orbite en fait un */
    if(mo){ var b=(u*6)*6.2832+(+w.dataset.th0), R=d/2+7;
      mo.style.left=(d/2+R*Math.cos(b)-4.5)+'px';
      mo.style.top =(d/2+R*Math.sin(b)-4.5)+'px'; }
    /* ⚠ LE PRÉNOM PART VERS L'EXTÉRIEUR, le long du rayon — jamais entre la personne
       et toi. Posé dessous, il venait recouvrir ton Noyau chaque fois qu'elle passait
       au-dessus. Il reste DROIT et à TAILLE FIXE : aucune perspective. */
    w.__pr=pr; w.__d=d; w.__z=P[2];
    /* ⚠ UN PRÉNOM SANS SON ANNEAU EST UN BUG. Quand une personne passe DERRIÈRE ton
       Noyau, il la masque — franchement, c'est la règle. Son prénom, lui, est posé
       vers l'extérieur et resterait seul à flotter. Il s'efface avec elle. */
    if(w.__nom){
      var cache = (P[2]<0) && (Math.hypot(pr.x,pr.y) < TOI_D/2 - d/2 + 4);
      /* ⚑ LES PRÉNOMS S'EFFACENT QUAND ÇA TOURNE VITE, ET REVIENNENT QUAND ÇA SE POSE.
         En pleine rotation ils sont illisibles de toute façon, et le placement — qui
         cherche un créneau libre — les envoyait loin de leur anneau : on voyait six
         mots errer autour de la sphère. Ils partent au-delà d'une demi-rotation par
         seconde et reviennent en même temps que le calme. C'est aussi ce qui fait
         que l'objet « se repose » : la sphère s'arrête, les noms se rallument. */
      var vv=Math.abs(f.__om||0);
      var op=Math.max(0,Math.min(1,1-(vv-0.5)/1.8));
      w.__nom.style.opacity = cache ? '0' : String(op);
    }
  });
  dessineMasse(f, f.__lac||0, f.__tan===undefined?VUE_TANG:f.__tan, f.__om||0);
  dessineTraces(f,u);
  /* le CALCUL du placement reste à quatre fois par seconde : il est coûteux et n'a
     aucune raison d'être refait à chaque image. */
  /* ⚠ LE PLACEMENT DOIT SUIVRE LA VUE, PAS SEULEMENT LE TEMPS. Depuis que le temps
     et le point de vue sont séparés, l'orbite avance en quatre minutes : le déclencheur
     d'origine ne rejouait le placement que toutes les 0,45 s — et pendant une rotation
     au doigt les prénoms restaient plantés loin derrière leur anneau. On le rejoue
     aussi dès que la vue a tourné d'un degré. */
  var dvue=Math.abs((f.__lac||0)-(f.__lacNp||0))+Math.abs((f.__tan||0)-(f.__tanNp||0));
  if(f.__np===undefined || Math.abs(u-f.__np)>0.0019 || dvue>0.019){
    f.__np=u; f.__lacNp=f.__lac||0; f.__tanNp=f.__tan||0; placeNoms(f);
  }
  /* mais le MOUVEMENT du prénom se fait à CHAQUE image : il GLISSE vers sa cible au
     lieu d'y sauter. Douze pour cent par image = il y est en 0,4 s, sans qu'on voie
     jamais ni un départ ni une arrivée. */
  f.querySelectorAll('.orb').forEach(function(w){
    if(!w.__cible||!w.__pos||!w.__nom) return;
    /* et AUCUN PAS NE DÉPASSE 1,2 px : sous ce seuil un déplacement ne se voit pas.
       Un glissement proportionnel seul faisait un premier pas de 4,3 px — le seul
       moment encore perceptible. Le transit dure plus longtemps ; il ne se voit plus. */
    var dx=w.__cible.x1-w.__pos.x, dy=w.__cible.y1-w.__pos.y;
    var d=Math.hypot(dx,dy);
    /* ⚠ ET LE PLAFOND DU GLISSEMENT SUIT LA VITESSE DE LA VUE. À 1,2 px par image,
       un prénom mettait quatre secondes à rattraper son anneau après un lancer : on
       voyait six mots ramper derrière la sphère. Au repos le plafond reste 1,2 —
       c'est lui qui rend le déplacement invisible ; dès que la vue tourne plus vite
       que sa rotation lente, il s'ouvre en proportion et le prénom colle à l'anneau. */
    /* ⚠ ET AU-DELÀ D'UNE DEMI-ROTATION PAR SECONDE, LE PRÉNOM NE GLISSE PLUS : il
       COLLE. Le glissement n'existe que pour rendre invisible un déplacement de
       repos ; en pleine rotation il ne fait que traîner le mot derrière son anneau,
       et on a vu « Léa » passer sur ton Noyau. */
    var vit=Math.abs(f.__om||0);
    if(vit>0.5){ w.__pos.x=w.__cible.x1; w.__pos.y=w.__cible.y1; }
    else {
      var plaf=1.2+Math.max(0,vit-VUE_AUTO)*22;
      if(d>0.01){ var pas=Math.min(d, Math.max(d*0.06, 0.04), plaf);
        w.__pos.x += dx/d*pas; w.__pos.y += dy/d*pas; }
    }
    w.__nom.style.left=w.__pos.x+'px';
    w.__nom.style.top =w.__pos.y+'px';
  });
  poseMatiere(f);         /* la matière est versée en DERNIER */
}

/* ⚠ LE PLACEMENT DES PRÉNOMS — un vrai problème, et je l'ai d'abord raté.
   Posés bêtement vers l'extérieur, ils se recouvraient entre eux et recouvraient les
   anneaux : le premier dessin en 3D était illisible sur la moitié gauche.
   Ce n'est PAS un cas de profondeur : deux anneaux qui se croisent, c'est le sujet ;
   deux NOMS qui se croisent, c'est une faute.
   On place donc chaque nom par ESSAIS, en commençant par les personnes les plus
   proches du regard : huit directions autour de son anneau, on garde la première qui
   ne touche ni un anneau, ni un nom déjà posé. Si aucune ne convient — ça arrive —
   on garde la position extérieure : le nom reste attaché au bon anneau, c'est ce qui
   compte le plus. */
function placeNoms(f){
  var NW=62, NH=18, MG=4;
  var gens=[].slice.call(f.querySelectorAll('.orb')).filter(function(w){return w.__pr;});
  gens.sort(function(a,b){return b.__z-a.__z;});          /* les plus près d'abord */
  var anneaux=gens.map(function(w){
    /* on évite l'ANNEAU, pas la lune : elle fait huit tours quand l'orbite en fait
       un, aucun placement fixe ne peut l'esquiver. Et il n'y a rien à esquiver —
       le nom est au-dessus d'elle (z 45) : elle passe DERRIÈRE, elle ne cache rien.
       Élargir le rayon pour elle a fait pire : 30 recouvrements au lieu de 3, parce
       que plus aucune position ne convenait et que le repli s'appliquait partout. */
    return {x:ORB_CX+w.__pr.x, y:ORB_CY+w.__pr.y, r:w.__d/2+6};});
  var poses=[];
  /* le COÛT d'une position : la surface qu'elle recouvre. Zéro = parfaite. */
  var coût=function(b){
    var c=0;
    var rond=function(x,y,r){
      var px=Math.max(b.x1,Math.min(x,b.x2)), py=Math.max(b.y1,Math.min(y,b.y2));
      var d=Math.hypot(px-x,py-y);
      return d<r ? (r-d)*(r-d) : 0;
    };
    for(var i=0;i<anneaux.length;i++) c+=rond(anneaux[i].x,anneaux[i].y,anneaux[i].r);
    c += rond(ORB_CX,ORB_CY,TOI_D/2+6) * 4;        /* ton Noyau pèse quatre fois */
    for(var k=0;k<poses.length;k++){var p=poses[k];
      var ox=Math.min(b.x2,p.x2)-Math.max(b.x1,p.x1);
      var oy=Math.min(b.y2,p.y2)-Math.max(b.y1,p.y1);
      if(ox>0&&oy>0) c += ox*oy*3;                 /* un nom sur un nom pèse trois fois */
    }
    return c;
  };
  gens.forEach(function(w){
    if(!w.__nom) return;
    var cx=ORB_CX+w.__pr.x, cy=ORB_CY+w.__pr.y, R=w.__d/2+13;
    var dd=Math.hypot(w.__pr.x,w.__pr.y)||1;
    var a0=Math.atan2(w.__pr.y/dd, w.__pr.x/dd);
    /* ⚠ TRENTE-DEUX ESSAIS, ET ON GARDE LE MOINS MAUVAIS.
       Une première version essayait huit directions et, si aucune n'allait, se rabattait
       AVEUGLÉMENT vers l'extérieur — d'où treize noms l'un sur l'autre. Maintenant on
       évalue chaque candidat par la SURFACE qu'il recouvre, et on garde le minimum :
       la position parfaite quand elle existe, la moins mauvaise sinon. */
    /* ⚠ TRENTE-DEUX ESSAIS NE SUFFISAIENT PLUS. Avec la sphère, les six se
       resserrent (l'enveloppe est passée de 175 à 163) et « Nico » finissait sur un
       anneau, trois fois, à 0 % du tour — pris par le contrôle. On élargit la
       recherche : SOIXANTE candidats, trois couronnes, vingt directions. */
    var best=null, bestCoût=1e9;
    for(var t=0;t<3;t++)for(var i=0;i<20;i++){
      var a=a0+(i%2?1:-1)*Math.floor(i/2)*0.34;
      var rr2=R+NH/2+4+t*15;
      var x=cx+Math.cos(a)*(rr2+NW/2*Math.abs(Math.cos(a))*0.55);
      var y=cy+Math.sin(a)*rr2;
      var b={x1:x-NW/2,x2:x+NW/2,y1:y-NH/2,y2:y+NH/2};
      if(b.x1<8||b.x2>382||b.y1<108||b.y2>444) continue;
      var c=coût(b) + t*3 + Math.floor(i/2)*1.2;   /* on préfère près, et vers l'extérieur */
      if(c<bestCoût){bestCoût=c; best=b;}
      if(bestCoût===0 && i===0 && t===0) break;
    }
    if(!best){
      var x2=Math.max(8+NW/2,Math.min(382-NW/2,cx+w.__pr.x/dd*(R+14)));
      var y2=Math.max(108+NH/2,Math.min(444-NH/2,cy+w.__pr.y/dd*(R+14)));
      best={x1:x2-NW/2,x2:x2+NW/2,y1:y2-NH/2,y2:y2+NH/2};
    }
    /* ⚑ L'HYSTÉRÉSIS — C'EST ICI QU'ÉTAIT LE SACCADE, ET NULLE PART AILLEURS.
       Mesuré : la boucle rAF est parfaite (16,67 ms, écart-type 0,06 ms, aucune image
       au-delà de 20 ms) et une image coûte 0,37 ms. Mais un anneau n'avançait que de
       0,024 px par image — invisible — pendant que CHAQUE PRÉNOM SAUTAIT 46 FOIS EN
       DIX SECONDES, jusqu'à 112,6 px d'un coup : le placement au moindre coût
       BASCULAIT d'un créneau à l'autre au moindre frémissement. Le seul mouvement
       visible de l'écran était un nom qui se téléporte.
       On garde donc le créneau courant tant qu'un autre ne fait pas MIEUX DE BEAUCOUP. */
    /* ⚠ mais l'hystérésis ne doit pas garder un créneau DEVENU MAUVAIS : une marge
       fixe laissait « Nico » finir sur un anneau (12 × 16 px, pris par le contrôle).
       On réévalue le créneau courant à chaque passe : s'il ne recouvre plus rien on
       le garde, sinon on ne change que pour NETTEMENT mieux. */
    /* LA RÈGLE, FINALE : on garde le créneau courant TANT QU'IL EST PARFAIT — il ne
       recouvre rien — et on prend le meilleur dès qu'il cesse de l'être. C'est ce qui
       tue les 46 sauts par nom : ils venaient de bascules entre créneaux ÉGALEMENT
       bons. Un créneau parfait n'est jamais abandonné ; un créneau qui se dégrade est
       remplacé tout de suite, et le glissement rend le changement invisible. */
    if(w.__slot && coût(w.__slot) <= 0.5) best = w.__slot;
    else w.__slot = best;
    poses.push(best);
    w.__cible = best;                     /* la CIBLE ; la position, elle, glisse */
    if(!w.__pos) w.__pos={x:best.x1,y:best.y1};
    w.__nom.style.zIndex='45';
  });
}
/* pour le contrôle : les prénoms À LEUR CIBLE, sans le transit. Un prénom qui GLISSE
   peut croiser un anneau pendant une demi-seconde — c'est un déplacement, pas un
   recouvrement au repos. Le contrôle doit juger l'état posé, et il doit le dire. */
window._nomsALaCible=function(){
  document.querySelectorAll('.fr .orb').forEach(function(w){
    if(!w.__cible||!w.__pos) return;
    w.__pos.x=w.__cible.x1; w.__pos.y=w.__cible.y1;
    if(w.__nom){ w.__nom.style.left=w.__pos.x+'px'; w.__nom.style.top=w.__pos.y+'px'; }
  });
  /* ⚠ ET ON REPEINT LA MATIÈRE. La clairière est peinte SOUS le prénom là où il
     était ; poser le prénom à sa cible sans repeindre laisserait le trou à l'ancienne
     place — et le contrôle mesurerait des points sous le mot qui n'y sont pas en
     vrai. Trouvé exactement comme ça : 6,6 % relevés sous « Maman » alors que
     l'écran, lui, est propre. */
  document.querySelectorAll('.fr').forEach(function(f){
    if(!f.__masG) return;
    dessineMasse(f, f.__lac||0, f.__tan===undefined?VUE_TANG:f.__tan, 0); poseMatiere(f);
  });
};
window._orbitePhase=function(u){
  document.querySelectorAll('.fr').forEach(function(f){orbitePose(f,u);});
};

/* ════════ LA MOISSON ════════ */
var EPOQUES=[{m:'terrazzo',p:'signal',n:12},{m:'mosaique',p:'terre',n:22},
             {m:'encre',p:'signal',n:43}];
function moissonListe(){var o=[],k=0;
  EPOQUES.forEach(function(e){for(var i=0;i<e.n;i++){o.push({pid:(k%9)+1,m:e.m,p:e.p});k++;}});
  return o;}
function moisson(f,y,depuis,combien){
  var L=moissonListe(), s=44, pas=50, cols=7;
  for(var i=0;i<combien&&depuis+i<L.length;i++){
    var d=L[depuis+i], cx=24+(i%cols)*pas, cy=y+Math.floor(i/cols)*pas;
    var w=el('div',null,'left:'+cx+'px;top:'+cy+'px;width:'+s+'px;height:'+s+'px;z-index:2');
    w.dataset.role='moisson'; w.appendChild(dalleDans(d.pid,s,d.m,d.p)); f.appendChild(w);}
}

/* ════════ LE REJEU — DOUZE phrases, tirées au hasard ════════ */
/* les sept retenues, plus cinq neuves au même calibre : le clin d'oeil qu'un ami
   ferait en souriant. Aucune description, aucun constat, aucune poésie. */
var PHRASES=['Tu l’avais dit.','Et tu l’as fait.','Personne n’en doutait.','Voilà.',
  'Comme prévu.','Évidemment.','Parole tenue.',
  'C’est bien toi.','Comme d’habitude.','Tu ne t’es pas fait prier.',
  'On n’en attendait pas moins.','Tiens donc.'];
function instant(theme,phrase){
  var f=cadre(theme);
  f.style.background=MENTHE; f.style.color='#06231A';
  var p=el('div','plat'); p.appendChild(el('div','t',null,'Aura'));
  p.appendChild(el('div','c',null,'✕ FERMER')); f.appendChild(p);
  var w=el('div',null,'left:100px;top:132px;width:190px;height:190px');
  w.appendChild(dalleDans(5,190,'mosaique','terre')); f.appendChild(w);
  txt(f,'bg700',24,388,342,64,700,'tenue.',
    'letter-spacing:-.04em;line-height:64px;color:#06231A');
  /* la phrase respire : 20 → 38 px sous le titre */
  txt(f,'bg600',24,490,342,20,600,phrase,'line-height:26px;color:#06231A');
  txt(f,'ap',24,760,342,14,400,'lève le doigt pour revenir',
    'text-align:center;color:#06231A;opacity:.80');
  return f;
}

/* ════════════════ L'AURA ════════════════ */
function auraHaut(theme){
  var f=cadre(theme), ink=f.__ink;
  plateau(f,'Aura');
  orbite(f,ink);
  txt(f,'bg700',24,448,342,64,700,harmonyWord(harmonieVal()),
    'text-align:center;letter-spacing:-.04em;line-height:74px');
  var hw=el('div',null,'left:24px;top:534px;width:342px;'
    +'display:flex;align-items:baseline;justify-content:center;gap:12px');
  var lb=el('span','eb',null,'harmonie'); lb.style.position='static';
  var nb=el('span','mark',null,String(harmonieVal()));
  nb.style.cssText='position:static;font-size:34px;line-height:34px;letter-spacing:-.01em;color:'
    +couleurHarmonie();
  hw.appendChild(lb); hw.appendChild(nb); f.appendChild(hw);
  legende(f,79,594);                 /* 26 px d'air au-dessus, 33 en dessous */
  eb(f,24,644,'tout ce que tu as tenu');
  moisson(f,688,0,21);               /* 27 px sous le titre, au lieu de 11 */
  return f;
}
function auraBas(theme){
  var f=cadre(theme);
  plateau(f,'Aura');
  eb(f,24,132,'tout ce que tu as tenu');
  moisson(f,164,21,56);
  bouton(f,700,'Partager mon Noyau');
  return f;
}

function pose(row,frame,cap){
  var fg=document.createElement('figure'); fg.appendChild(frame);
  var fc=document.createElement('figcaption'); fc.innerHTML=cap; fg.appendChild(fc);
  document.getElementById(row).appendChild(fg);
}
function tableau(id,lignes,entetes){
  var h='<table class="mots"><tr>'+entetes.map(function(e){return '<th>'+e+'</th>';}).join('')+'</tr>';
  h+=lignes.map(function(l){return '<tr>'+l.map(function(c){return '<td>'+c+'</td>';}).join('')+'</tr>';}).join('');
  document.getElementById(id).innerHTML=h+'</table>';
}

window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize();
       window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    var vif=auraHaut('dk'); vif.dataset.vif='1';
    pose('rowVif', vif, '<b>vivant — prends-le au doigt</b> · vue 84 s, orbites 4 min');
    for(var i=0;i<4;i++){
      var f=auraHaut(i<3?'dk':'lt');
      pose('rowSuite', f, (i/4*100).toFixed(0)+' % du tour');
      f.__lac=i/4*6.2832; f.__tan=VUE_TANG;
      orbitePose(f, i/4);
    }
    var e1=auraHaut('dk'); pose('rowEcran', e1, 'le haut · <b>sombre</b>');
    e1.__lac=0.82; e1.__tan=VUE_TANG; orbitePose(e1,0.13);
    var e2=auraHaut('lt'); pose('rowEcran', e2, 'le haut · clair');
    e2.__lac=0.82; e2.__tan=VUE_TANG; orbitePose(e2,0.13);
    pose('rowEcran', auraBas('dk'), 'le bas — <b>les époques</b>');
    /* ⚑ LES DEUX TEINTES, CÔTE À CÔTE, MÊME PHASE, MÊME VUE. */
    [['encre','la <b>forme</b> de la dalle dans l’encre — <b>retenu</b>'],
     ['monde','la dalle garde <b>ses couleurs</b> — écarté : elle aplatit la sphère']]
    .forEach(function(t){
      var g=auraHaut('dk'); g.__teinte=t[0];
      pose('rowTeinte', g, t[1]);
      g.__lac=0.42; g.__tan=VUE_TANG; orbitePose(g,0);
    });
    /* ⚑ QUATRE MONDES, LA MÊME SPHÈRE. */
    [['encre','signal'],['mosaique','terre'],['braille','signal'],['sillons','terre']]
      .forEach(function(w){
        var g=auraHaut('dk'); g.__monde={m:w[0],p:w[1],h:0};
        pose('rowMondes', g, w[0]);
        g.__lac=0.42; g.__tan=VUE_TANG; orbitePose(g,0);
      });
    document.getElementById('avisTeinte').innerHTML=
      '<p class="pr">Dans les deux cas c’est <b>la vraie dalle du moteur</b>, à l’échelle 1, '
     +'et dans les deux cas <b>l’Aura change quand on change de monde</b> — mais l’une change '
     +'de <b>couleur</b>, l’autre de <b>forme</b>. Ce que je mesure, et que je dis franchement : '
     +'la teinte du monde <b>aplatit la sphère</b> (la palette du monde n’a pas l’écart de '
     +'luminosité de la crème sur l’encre, donc le limbe cesse d’être un bord) et son '
     +'<b>terracotta est exactement « à tenir »</b> — la matière se met à parler le langage des '
     +'états. Le cadre vivant, en haut, est en <b>teinte du monde</b> parce que c’est ce que tu '
     +'as demandé ; si tu me suis, je bascule tout sur la forme.</p>';
    [PHRASES[0],PHRASES[7],PHRASES[11]].forEach(function(p,i){
      pose('rowPh', instant('dk',p), (i?'':'<b>elle ouvre la série</b> · ')+'« '+p+' »'); });

    document.getElementById('avisPhrases').innerHTML =
      '<p class="pr">Les <b>douze</b>, tirées au hasard, une par rejeu. <b>« Tu l’avais dit. » '
     +'ouvre la série.</b> Et la phrase respire : <b>20 → 38 px</b> sous « tenue. ».</p><pre>'
     +PHRASES.map(function(p,i){return (i+1)+' · '+p;}).join('\n')+'</pre>';

    tableau('mesure',[
      ['la masse','36 fils · <b>42 045 points</b> · 4 tranches','le volume vient de la densité, pas des six'],
      ['la technique','tampon Uint32 + putImageData','<b>fillRect plafonnait à 13 000</b> sur l’écran complet'],
      ['l’image au repos','16,67 → 16,72 ms · écart-type 0,06','<b>60 images par seconde</b>, 0 à 1 perdue sur 300'],
      ['l’image au doigt','16,85 ms · 95e centile 16,80','2 images > 20 ms sur 457'],
      ['l’élan','éteint en 4,3 à 5,2 s','un lancer franc fait <b>un tour complet</b>'],
      ['les deux gestes','seuil 6 px','toucher → openPerson · glissement → rotation'],
      ['le retard de la matière','6 classes · 0,045 rad par rad/s','0,4 px au repos, 12° au lancer'],
      ['l’anneau','même grain que la sphère','<b>une seule matière sur l’écran</b>'],
      ['le visage','22 dans 36 (§2.9 : 0,62)','il RENTRE dans l’anneau, il n’est plus posé dessus'],
      ['ton Noyau','rang 40, les six vont à 32','<b>0 recouvert</b> sur 9 points, 72 positions × 4 vues'],
      ['la silhouette','167,0 contre une enveloppe de 166,0','<b>0 sortie sur 432</b> — ils sont dedans'],
      ['la profondeur','25,4 → 61,8 px · rapport <b>2,44</b>',''],
      ['l’encre sous un mot','0,26 à 0,75 %','seuil 1 % · clairière coupée : 6 sur 6 sont pris']
    ],['ce que c’est','la valeur','ce qu’on en lit']);

    window._verifOrbite=function(){
      var out=[], f=document.querySelectorAll('.fr')[0];
      var fr=f.getBoundingClientRect();
      /* ⚑ CE CONTRÔLE A ÉTÉ RÉÉCRIT AU NIVEAU DE LA DÉCISION — et la version d'avant
         est gardée dans sauvegardes/. LA RÈGLE N'A PAS CHANGÉ : rien ne passe devant
         ton Noyau. C'est sa GARANTIE qui a changé de nature.
         AVANT : la géométrie. On cherchait, pour chaque personne, l'inclinaison qui
         dégage ton Noyau sur 72 positions — et ça tenait parce que le point de vue
         était fixe.
         MAINTENANT le doigt tourne l'objet dans tous les sens : n'importe qui peut
         être amené sur l'axe du regard, et AUCUNE inclinaison ne peut l'empêcher.
         Tom l'a écrit lui-même : « quelqu'un de proche est près du centre, donc
         partiellement masqué par ton Noyau, et c'est juste ».
         APRÈS : l'ordre de tracé. Ton Noyau est à 40, une personne à 20 + z/10, donc
         au plus 32. On mesure donc DEUX choses, et elles sont plus dures que l'ancienne :
           1 · aucun anneau n'atteint jamais le rang de ton Noyau, sur 72 positions
               ET quatre points de vue ;
           2 · au doigt, sur neuf points de son disque, c'est bien LUI qu'on touche. */
      var toi=f.querySelector('[data-forme=anneau]');
      var Rtoi=+toi.dataset.rayon, rangMax=0, lac0=f.__lac||0;
      for(var vv=0;vv<4;vv++){
        f.__lac=lac0+vv*1.5708; f.__tan=VUE_TANG+(vv%2?0.5:-0.35);
        for(var s=0;s<72;s++){
          orbitePose(f, s/72);
          [].forEach.call(f.querySelectorAll('.orb'),function(w){
            var z=+w.style.zIndex||0; if(z>rangMax) rangMax=z;
            if(z>=40) out.push('à u='+(s/72).toFixed(3)+' un anneau atteint le rang de ton Noyau (z='+z+')');
          });
        }
      }
      f.__lac=lac0; f.__tan=VUE_TANG; orbitePose(f,0);
      /* la confirmation AU DOIGT : neuf points du disque de ton Noyau */
      var toiR=f.querySelector('[data-forme=anneau]').getBoundingClientRect();
      var tcx=toiR.left+toiR.width/2, tcy=toiR.top+toiR.height/2, RR=toiR.width/2-3;
      var couvert=0;
      for(var a9=0;a9<9;a9++){
        var an=a9/9*6.2832, rr9=(a9?RR*0.72:0);
        var X9=tcx+rr9*Math.cos(an), Y9=tcy+rr9*Math.sin(an);
        if(X9<0||Y9<0||X9>innerWidth||Y9>innerHeight){ couvert=-1; break; }
        var top=document.elementsFromPoint(X9,Y9)[0];
        if(top && !(top===toi || toi.parentNode.contains(top) ||
            (top.closest && top.closest('[data-role=pers]')===null && top.tagName!=='DIV')))
          { /* rien */ }
        if(top && top.closest && top.closest('[data-role=pers]')) couvert++;
      }
      /* la profondeur, mesurée : de combien un anneau grossit-il en s'approchant ? */
      var mn=1e9, mx=0, boite={x1:1e9,x2:-1e9,y1:1e9,y2:-1e9};
      for(var s2=0;s2<72;s2++){
        orbitePose(f, s2/72);
        [].forEach.call(f.querySelectorAll('.orb canvas'),function(c){
          var r=c.getBoundingClientRect();
          if(r.width<mn)mn=r.width; if(r.width>mx)mx=r.width;
          boite.x1=Math.min(boite.x1,r.left-fr.left); boite.x2=Math.max(boite.x2,r.right-fr.left);
          boite.y1=Math.min(boite.y1,r.top-fr.top);   boite.y2=Math.max(boite.y2,r.bottom-fr.top);
        });
      }
      /* ⚑ LA SILHOUETTE DE LA SPHÈRE, ET L'ENVELOPPE DES SIX. On MESURE que les
         personnes sont DEDANS — sur 72 positions, anneau et lune compris. */
      var sil=0;
      for(var zt=-1;zt<=1.0001;zt+=0.005){
        var xy=Math.sqrt(Math.max(0,1-zt*zt))*MAS_R, kk=MAS_FOC/(MAS_FOC-zt*MAS_R);
        sil=Math.max(sil,xy*kk);
      }
      var env=0, dehors=0;
      for(var s3=0;s3<72;s3++){
        orbitePose(f, s3/72);
        [].forEach.call(f.querySelectorAll('.orb'),function(w){
          if(!w.__pr) return;
          var e=Math.hypot(w.__pr.x,w.__pr.y)+w.__d/2+11*w.__pr.k;
          env=Math.max(env,e); if(e>sil) dehors++;
        });
      }
      orbitePose(f,0);
      return {ecarts:out.slice(0,6), total:out.length, rangMax:rangMax, couvert:couvert,
              silhouette:+sil.toFixed(1), enveloppe:+env.toFixed(1), dehors:dehors,
              petit:mn.toFixed(1), gros:mx.toFixed(1), rapport:(mx/mn).toFixed(2),
              boite:[boite.x1,boite.y1,boite.x2,boite.y2].map(Math.round).join(' · ')};
    };
    /* ⚑ COMBIEN FAUT-IL TOURNER POUR ATTEINDRE N'IMPORTE QUI ?
       Une personne est ATTEIGNABLE quand une part de sa zone touchable sort du
       disque de ton Noyau. On balaie 180 points de vue, on note pour chacun et pour
       chaque personne la rotation qu'il faut encore faire, et on rend le PIRE cas —
       puis on le convertit en course de doigt (VUE_SENS) et en secondes. */
    window._acces=function(){
      var f=document.querySelectorAll('.fr')[0];
      var lac0=f.__lac, tan0=f.__tan, N=180;
      var gens=[].slice.call(f.querySelectorAll('.orb'));
      var vu=gens.map(function(){return [];});
      for(var i=0;i<N;i++){
        f.__lac=i/N*6.2832; f.__tan=VUE_TANG; orbitePose(f,0);
        gens.forEach(function(w,gi){
          var d=Math.hypot(w.__pr.x,w.__pr.y);
          vu[gi].push(d + w.__d/2 + 14 > TOI_D/2 + 4);
        });
      }
      f.__lac=lac0; f.__tan=tan0; orbitePose(f,0);
      var pire=0, quiPire='', partVue=[];
      gens.forEach(function(w,gi){
        var v=vu[gi], n=v.length, vus=0, trou=0;
        for(var i2=0;i2<n;i2++){
          if(v[i2]) vus++;
          if(!v[i2]){ var d2=0; while(d2<n && !v[(i2+d2)%n]) d2++;
            if(d2>trou) trou=d2; }
        }
        partVue.push({qui:w.dataset.qui, part:Math.round(100*vus/n), trou:trou});
        if(trou>pire){ pire=trou; quiPire=w.dataset.qui; }
      });
      var deg=pire/N*360, px=deg*Math.PI/180/VUE_SENS;
      return {pire_degres:+deg.toFixed(1), pire_qui:quiPire,
              course_doigt_px:Math.round(px), secondes:+(px/600).toFixed(2),
              detail:partVue};
    };
    /* ⚑ LE CRATÈRE : on le creuse, on lâche, et on chronomètre sa fermeture. */
    window._crat=function(x,y){return new Promise(function(res){
      var f=document.querySelectorAll('.fr[data-vif]')[0];
      if(!f.__imp) f.__imp=[];
      var m={x:x*MAS_D,y:y*MAS_D,r:IMP_R*MAS_D,r2:IMP_R*MAS_D*IMP_R*MAS_D,
             t0:performance.now(),tr:0,e:0,eRel:0};
      f.__imp.push(m); f.__creux=m;
      setTimeout(function(){
        m.eRel=m.e; m.tr=performance.now(); f.__creux=null;
        var t0=m.tr, seuils={}, cibles=[0.5,0.1,0.02];
        (function tick(){
          var t=(performance.now()-t0)/1000;
          cibles.forEach(function(c){ if(seuils[c]===undefined && m.e<=c) seuils[c]=+t.toFixed(2); });
          if(seuils[0.02]!==undefined) res({montee:IMP_MONTE, demi:seuils[0.5],
                                            dixieme:seuils[0.1], referme:seuils[0.02],
                                            ampMax:Math.round(IMP_A)});
          else requestAnimationFrame(tick);
        })();
      }, 400);
    });};
    window.__pret=true;
  },1800);

  var t0=null, tp=null;
  function boucle(ts){
    if(t0===null){t0=ts; tp=ts;}
    var dt=Math.min(0.05,(ts-tp)/1000); tp=ts;
    if(window.__pret && !window.__fige){
      var u=((ts-t0)%ORB_T)/ORB_T;
      document.querySelectorAll('.fr[data-vif]').forEach(function(f){
        if(f.__lac===undefined){f.__lac=0; f.__tan=VUE_TANG; f.__vlac=0; f.__vtan=0;}
        var om;
        if(f.__prise){
          /* doigt posé : la vue est celle que la main vient d'écrire. La vitesse
             instantanée sert au cisaillement de la matière, rien d'autre. */
          om=(f.__lac-(f.__lacAv||f.__lac))/Math.max(dt,0.001);
          f.__vlac=0; f.__vtan=0;
        }else{
          /* ⚑ L'ÉLAN S'ÉTEINT, LA ROTATION LENTE NE S'ARRÊTE JAMAIS.
             Les deux s'ADDITIONNENT : on ne « rend pas la main » à un moment
             précis — il n'y a pas de reprise, donc pas de saccade à la reprise. */
          var k=Math.exp(-dt/VUE_TAU);
          f.__vlac*=k; f.__vtan*=k;
          if(Math.abs(f.__vlac)<0.0008) f.__vlac=0;
          if(Math.abs(f.__vtan)<0.0008) f.__vtan=0;
          f.__lac += (VUE_AUTO+f.__vlac)*dt;
          f.__tan  = bornTangage(f.__tan + f.__vtan*dt);
          om=VUE_AUTO+f.__vlac;
        }
        f.__lacAv=f.__lac;
        /* la vitesse vue par la matière est LISSÉE : un à-coup de doigt ne doit pas
           faire claquer le cisaillement. */
        f.__om=(f.__om||0)*0.82+om*0.18;
        orbitePose(f,u,ts-t0);
      });
    }
    requestAnimationFrame(boucle);
  }
  requestAnimationFrame(boucle);
});
