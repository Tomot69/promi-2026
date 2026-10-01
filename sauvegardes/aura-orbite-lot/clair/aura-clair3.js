/* ════════════════════════════════════════════════════════════════════════════
   lot-AURA-ORBITE — L'ÉCRAN AURA, RÉÉCRIT EN ENTIER · 10 septembre 2026
   ────────────────────────────────────────────────────────────────────────────
   Ce qu'il porte, de haut en bas, et rien d'autre (PLANCHE-VELOURS.html) :
     LA SPHÈRE    le velours, ses dalles dans le monde de LEUR plantation, et la
                  mémoire de la main. Aucun nom dessus : l'image se partage.
     LE MOT       il qualifie L'OBJET, dans le registre du rejeu. Ni note, ni verdict.
     LES NOYAUX   « toi » puis les personnes, §2.9 : piste neutre, trois arcs d'état,
                  l'image de la personne (sa photo si elle existe), le prénom.
     LA LÉGENDE   elle nomme les trois arcs — elle se déclare centrée.
     CE QUE TU AS TENU   les trois dernières paroles tenues, en vraies dalles.
     LE BOUTON    Partager mon Noyau.
   Les huit acquis de la sphère (ÉTAT DES LIEUX, clôture de l'Orbite) sont ici :
     la rotation lente qui ne s'arrête jamais · la prise au doigt dans tous les sens ·
     l'élan qui s'ADDITIONNE à la rotation lente (pas de reprise, donc pas de saccade) ·
     le toucher qui creuse, résiste et revient · la trace qui reste · le comblement du
     creux au lancer · le geste qui relisse · un toucher ouvre la personne, un
     glissement tourne.
   ⚑ LA DENSITÉ CÈDE, JAMAIS LE COMPORTEMENT. 110 000 poils est un plafond mesuré sur
   un Mac Intel. L'écran mesure lui-même le temps de chaque image : si la médiane
   dépasse une image à 60 Hz, il VISE un palier plus bas (110 000 → 90 000 → 75 000) — appliqué à
   l'ouverture suivante, jamais sous les yeux (voir `densite`).
   Aucun geste n'est retiré pour tenir le budget.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
  var M = window.OrbiteMoteur, SC = document.getElementById('auraScreen');
  if(!M || !SC || !window.Toile) return;

  /* ── LES COTES — planche ÷ 0,872 ; une cote se CALCULE, elle ne se mesure jamais
        sur elle-même (§8). ───────────────────────────────────────────────────── */
  var K = { bo:{x:47, y:89.4, d:296}, R:0.392,
            nx:{y:454, h:107}, mo:{y:633}, lgH:16, bt:{y:762, h:60}, motY:403.7, motL:18.9*1.25, marge:22,
            toi:{d:78, arc:8, ph:48}, pers:{d:58, arc:6, ph:36} };
  K.lgY = K.nx.y + K.nx.h + (K.mo.y - (K.nx.y + K.nx.h) - K.lgH) / 2;    /* 589 */
  K.Rpt = K.bo.d * K.R;                                                  /* 116 pt */
  /* ⚑ L'AIR DE LA COLONNE — deux valeurs, prises dans la planche, jamais à l'œil (voir `place`) :
     sous la phrase, l'air que la planche laissait sous UNE ligne (454 − 403,7 − 23,625) ; entre les
     autres blocs, le rythme de la planche — la légende y est centrée à 28 de chaque côté. */
  K.AIR_MOT = K.nx.y - (K.motY + K.motL);                                /* 26,675 */
  K.AIR = 28;
  K.PLI = 844;
  K.MOISSON = 6;                                                         /* deux rangées de trois (Q187) */
  /* ⚑ RÈGLE (Tom, 10 sept. — Q189) : LA SECONDE RANGÉE PARAÎT À PARTIR DE CINQ DALLES TENUES. En dessous,
     la première rangée seule : une rangée au tiers (3 + 1) dit « il en manque deux ». À cinq, le trou
     d'une case à droite est accepté (mesuré : il se voit à l'ouverture). */
  K.RANG2 = 5;
  K.PEAU_T = 0.7;                                                        /* provisoire — fixé à la mesure (Q182) */                                                           /* le bas de l'écran, à l'ouverture */

  /* ── LE SOL DIT LA NATURE ; LES ARCS DISENT L'ÉTAT. Menthe et terracotta ne servent
        qu'aux états, nulle part ailleurs. ─────────────────────────────────────── */
  var NAT = { promi:[58,84,255], chiche:[250,34,88], nuee:[138,92,240] };
  /* ⚑ LE THÈME CLAIR — SOL CLAIR, POIL SOMBRE (Tom, 10 sept. — Q182) : « le vrai négatif du thème sombre ;
     le champ garde sa couleur de nature, c'est la matière qui s'adapte au corps ». Le poil garde la couleur
     de nature ; la PEAU sous lui, que le peintre assombrit (× 0,64) pour qu'en sombre chaque poil se
     détache en clair, s'ÉCLAIRCIT en clair vers la TEINTE CLAIRE DE LA NATURE (PROMI-SPECIFICATIONS §1.2) :
     chaque poil s'y détache en sombre. La part de teinte (`K.PEAU_T`) se choisit À LA MESURE, contre le
     thème sombre : écart boule ↔ page, contour, lisibilité des îles. */
  var NAT_CLAIR = { promi:[0xCB,0xAA,0xFF], chiche:[0xFF,0xC0,0xA8], nuee:[0xD0,0xB0,0xFF] };
  var ETA = [['tenues','#2BE88C'], ['en cours','#8FA0FF'], ['à tenir','#F07A2E']];
  /* les cinq phrases de Tom — le registre du rejeu (ÉTAT DES LIEUX, § 7 des couleurs) */
  var MOTS = ['Rien de ce qui est ici n’a été dit à la légère.',
              'Tout ça, tu l’as dit. Et tu l’as fait.',
              'On ne dirait pas comme ça, mais c’est du solide.',
              'Il y en a, des paroles tenues.',
              'Et dire que tout ça, c’est toi.'];
  var VIDE = ['La première parole laissera sa trace ici.', 'Tout commence par une parole donnée.'];

  /* ── LES GESTES — les constantes de PLANCHE-AURA-SPHERE (5 septembre), validées.
        La rotation de repos : ⚑ UN TOUR EN 2 MINUTES (Tom, 10 septembre : « un peu trop lente —
        accélère-la à peine, qu'on sente que ça tourne en regardant quelques secondes, sans que ça
        devienne agité »). Elle était à 2 min 45 (5 sept.) ; 84 s avait été jugé trop vif. Au centre
        de la face la surface passe de 4,4 à 6,1 pt/s. C'est toujours le geste qui accélère.
        SENS : la planche donnait 0,011 rad/px pour une boule de 142 — un tour pour deux
        diamètres de doigt. On garde CE rapport sur la boule de l'écran (116 pt). ──── */
  var G = { AUTO:6.283185307/120, TANG:0.32, TANGMAX:1.15, TAU:0.55, VMAX:11, TAP:6,
            SENS:0.011*142/K.Rpt, MONTE:0.09, IMP_TAU:1.35, COMBLE:0.42, DOUBLE:350,
            TRACES:9, W:0.27, TOUR_TAU:1.1, BUDGET:16.7 };
  /* la pulpe, en points — les BORNES entre lesquelles le capteur tombe (planche) */
  var PULPE = { pouce:[46.4, 0.70], index:[30.0, 0.73] };

  /* ── les réglages du peintre, repris de la planche (`page`, `ecranAura`) ─────── */
  var FROISSE = (function(){
    var D=[[ 0.62, 0.31, 0.72],[-0.47, 0.83,-0.30],[ 0.18,-0.55, 0.81],
           [-0.79,-0.37, 0.49],[ 0.34, 0.88, 0.33],[ 0.71,-0.62,-0.33]];
    var Kk=[9.7,13.1,17.9,23.3,29.1,37.7], A=[0.0059,0.0041,0.0029,0.0019,0.0012,0.0007];
    var PH=[0.4,1.9,2.7,0.9,1.4,2.2], R=[];
    for(var i=0;i<D.length;i++) R.push([A[i], D[i][0]*Kk[i], D[i][1]*Kk[i], D[i][2]*Kk[i], PH[i]]);
    return R;
  })();
  var ENV = [1.0,0.0, 1.31,0.77,-1.05,0.4, -0.83,1.49,0.61,1.9], KN = 0.55;
  var KDENS = [4.7,5.3,4.1,0.6,1.9,1.1, 6.7,5.9,7.3,2.4,0.7,1.5];
  var PALIERS = [110000, 90000, 75000];
  var PXR = 620*0.438, MAG = 2.2;     /* l'échelle des îles, celle de la planche */

  function lsGet(k,d){ try{ var v=localStorage.getItem(k); return v==null?d:JSON.parse(v); }catch(e){ return d; } }
  function lsSet(k,v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
  function el(t,c,x){ var e=document.createElement(t); if(c) e.className=c; if(x!=null) e.textContent=x; return e; }
  function svg(t){ return document.createElementNS('http://www.w3.org/2000/svg', t); }

  /* ════════════════════════════════════════════════════════════════════════════
     LES VRAIES DONNÉES — c'est là que tout peut mentir : la planche avait un jeu
     de démonstration, l'app a des Promi réels.
     ════════════════════════════════════════════════════════════════════════════ */
  function tous(){ try{ return (typeof promises!=='undefined' && promises) || []; }catch(e){ return []; } }
  function estMoi(n){ try{ return typeof _isMe==='function' && _isMe(n); }catch(e){ return false; } }
  /* ce que JE promets : ni un gardé de côté, ni une demande, ni la parole d'un autre */
  function mesPromi(){ return tous().filter(function(p){ return p && !p.draft && !p.req && (!p.from || p.from==='moi'); }); }
  /* ⚑ L'ORDRE DES ÎLES EST CELUI OÙ ELLES SONT APPARUES — il ne se recalcule jamais.
     Le semis pousse par ACCRÉTION : l'île k dépend des k−1 précédentes. Trier par id
     ferait qu'une parole tenue aujourd'hui, plus ancienne en id qu'une autre, se
     glisse au milieu — et toutes les suivantes bougeraient. « Les anciennes ne bougent
     pas d'un pouce. » On garde donc l'ordre d'apparition, et les nouvelles s'ajoutent. */
  function ordreTenus(P){
    var T=P.filter(function(p){ return p.status==='tenu'; }), par={};
    T.forEach(function(p){ par[p.id]=p; });
    var O=lsGet('promi_orbite_ordre', []); if(!Array.isArray(O)) O=[];
    O=O.filter(function(id){ return par[id]; });
    T.filter(function(p){ return O.indexOf(p.id)<0; }).sort(function(a,b){ return a.id-b.id; })
     .forEach(function(p){ O.push(p.id); });
    lsSet('promi_orbite_ordre', O);
    return O.map(function(id){ return par[id]; });
  }
  function natureDe(p){ return p.chiche ? 'chiche' : (p.nuee ? 'nuee' : 'promi'); }
  /* la nature la plus présente parmi ce qui est TENU — ces comptes ne font que monter.
     Égalité : l'ordre du §3 (Promi, puis Chiche, puis Nuée). Zéro : bleu, la nature de
     base (tranché avec Tom). */
  function natureMaj(T){
    var c={promi:0, chiche:0, nuee:0}; T.forEach(function(p){ c[natureDe(p)]++; });
    var b='promi'; if(c.chiche>c[b]) b='chiche'; if(c.nuee>c[b]) b='nuee'; return b;
  }
  function parts(L){
    var t=0,e=0,r=0; L.forEach(function(p){ if(p.status==='tenu') t++; else if(p.status==='rate') r++; else e++; });
    var s=t+e+r; return s ? [t/s, e/s, r/s] : [0,0,0];
  }
  /* les personnes à qui JE promets — ordre alphabétique, jamais par valeur (§2.9) */
  function personnes(P){
    var m={};
    P.forEach(function(p){ (''+(p.who||'')).split(',').forEach(function(w){
      w=w.trim(); if(!w || w==='moi' || w==='le groupe' || estMoi(w)) return;
      (m[w]=m[w]||[]).push(p); }); });
    return Object.keys(m).sort(function(a,b){ return a.localeCompare(b,'fr'); })
                 .map(function(n){ return {nom:n, parts:parts(m[n])}; });
  }
  function donnees(){
    var P=mesPromi(), T=ordreTenus(P);
    return {P:P, T:T, n:T.length, nature:natureMaj(T), toi:parts(P), gens:personnes(P)};
  }
  function cleMonde(p){ var m=p.monde||{}; return p.id+'|'+m.m+'/'+m.p+'/'+m.h; }

  /* ⚑ UNE DALLE SE REND UNE FOIS (CLAUDE.md §4) — un cache par Promi et par monde.
     Toujours la vraie dalle du moteur, échelle 1, dans le monde de SA plantation. */
  var DALLES = {};
  function dalleDe(p){
    var k=cleMonde(p); if(DALLES[k]) return DALLES[k];
    var cv=document.createElement('canvas'), ok=false;
    try{ ok=window.Toile.dalleTrame(cv, p.id, 1, p.monde||undefined); }catch(e){}
    if(!ok || !cv.width) return null;
    return (DALLES[k]=cv);
  }

  /* ════════════════════════════════════════════════════════════════════════════
     L'ÉCRAN — bâti une fois, rempli à chaque ouverture
     ════════════════════════════════════════════════════════════════════════════ */
  var CAD, BO, CV, PRISE, MOT, INV, NX, LG, MO, GR, BT, D=null, FIN;
  function squelette(){
    if(CAD) return;
    SC.classList.add('au2');
    /* ⚠ L'OMBRE DE DALLE BOUGEAIT SUR UN ÉCRAN QUI NE LA MONTRE PLUS — ET ÇA FIGEAIT L'ÉLAN.
       Mesuré au profileur (10 sept.) : la boucle `frame` des écrans `.tuto-fond` (≈ l. 8917)
       écrit, À CHAQUE IMAGE, trois propriétés personnalisées (`--gx`, `--gy`, `--grot`) sur
       chaque écran visible. Elles S'HÉRITENT : toute l'arborescence de l'Aura — et les
       centaines de nœuds masqués de l'ancienne — recalculait son style à chaque image, pour
       animer un `::before` que ce lot MASQUE. Autant de temps propre que le peintre de la
       sphère, et des images de 50 à 67 ms pendant l'élan.
       ⚠ ET CE N'ÉTAIT PAS QUE L'AURA. Cette boucle tient pour « visible » tout élément dont
       `offsetParent` n'est pas nul — or un écran fermé n'est pas en `display:none`, il est
       glissé hors champ. Elle écrit donc sur LES DOUZE écrans `.tuto-fond`, fermés compris,
       à chaque image. Prouvé au profileur : avec ces écritures ignorées sur les écrans
       cachés, `frame` passe de 27 % à 1,6 % du temps (24 480 écritures en 20 s).
       On n'exempte QUE le geste fautif (§7) : ces trois écritures-là sont ignorées sur l'Aura,
       toujours (son `::before` est masqué), et sur les écrans CACHÉS DESSOUS, tant que l'Aura
       est ouverte. Hors de l'Aura, rien ne change ; aucune règle, aucune classe n'est touchée.
       (Le coût existe partout ailleurs dans l'app — hors lot, QUESTIONS Q180.) */
    try{
      [].forEach.call(document.querySelectorAll('.tuto-fond, #createSheet, #settingsScreen'), function(el){
        var _sp=el.style.setProperty;
        el.style.setProperty=function(p){
          if((p==='--gx'||p==='--gy'||p==='--grot') &&
             (el===SC || (SC.classList.contains('show') && !el.classList.contains('show')))) return;
          return _sp.apply(this, arguments);
        };
      });
      ['--gx','--gy','--grot'].forEach(function(p){ SC.style.removeProperty(p); });
    }catch(e){}
    CAD=el('div','au-cadre'); CAD.id='auCadre';
    /* il se DÉCLARE colonne qui défile (voir `place`) : le juge ne l'exempte que déclaré, qu'il tienne
       dans l'appareil et qu'il rogne — la même règle que la rangée glissante (data-glisse) */
    CAD.setAttribute('data-defile','1');
    BO=el('div','au-bo'); CV=el('canvas'); CV.id='auBoule'; BO.appendChild(CV);
    PRISE=el('div','au-prise'); BO.appendChild(PRISE); CAD.appendChild(BO);
    MOT=el('div','au-mot'); CAD.appendChild(MOT);
    INV=el('div','au-inv'); CAD.appendChild(INV);
    NX=el('div','au-nx'); NX.setAttribute('data-glisse','1'); CAD.appendChild(NX);
    LG=el('div','au-lg');
    ETA.forEach(function(e){ var s=el('span'), i=el('i'); i.style.background=e[1];
      s.appendChild(i); s.appendChild(document.createTextNode(e[0])); LG.appendChild(s); });
    CAD.appendChild(LG);
    MO=el('div','au-mo'); MO.appendChild(el('h3',null,'Ce que tu as tenu'));
    GR=el('div','au-gr'); MO.appendChild(GR); CAD.appendChild(MO);
    BT=el('div','au-bt','Partager mon Noyau'); BT.id='auPartage'; BT.setAttribute('role','button');
    /* la même porte que l'ancien #sealShare : le partage, en mode Noyau */
    BT.onclick=function(){ try{ if(typeof openShare==='function') openShare();
      var nb=document.querySelector('#shMode button[data-mode=noyau]'); if(nb) nb.click(); }catch(e){} };
    CAD.appendChild(BT);
    FIN=el('div','au-fin'); CAD.appendChild(FIN);
    SC.appendChild(CAD);
    gestesBoule(); gestesNoyaux();
  }

  /* l'image d'une personne — celle du produit : `_blobBg`, sa texture en soft-light,
     ou la VRAIE photo quand elle existe. C'est elle qui identifie, pas une couleur. */
  function visage(d, nom, moi){
    var w=el('div','au-vis'); w.style.width=w.style.height=d+'px';
    var ph = moi && typeof USER!=='undefined' && USER && USER.photo;
    if(ph){ w.style.background='center/cover url("'+ph+'")'; w.setAttribute('data-photo','1'); }
    else{
      var seed = moi ? ('u'+(typeof USER!=='undefined'&&USER?USER.seed:0)) : nom;
      try{ w.style.background=_blobBg(seed); }catch(e){}
      try{ if(typeof _NOISE==='string' && _NOISE){ var nz=el('div','au-grain');
        nz.style.backgroundImage='url('+_NOISE+')'; w.appendChild(nz); } }catch(e){}
    }
    return w;
  }
  /* un Noyau du §2.9 : piste neutre, trois arcs d'état (2,6 % de vide), l'image, le nom */
  function noyau(dia, ep, dph, pa, nom, moi){
    var w=el('div','au-n'+(moi?' au-moi':'')); w.setAttribute('data-qui', moi?'moi':nom);
    var box=el('div','au-nb'); box.style.width=box.style.height=dia+'px';
    var s=svg('svg'); s.setAttribute('viewBox','0 0 '+dia+' '+dia); s.setAttribute('width',dia); s.setAttribute('height',dia);
    var r=(dia-ep)/2, cx=dia/2, C=2*Math.PI*r;
    function arc(cls, col, frac, rot){
      var a=svg('circle'); a.setAttribute('cx',cx); a.setAttribute('cy',cx); a.setAttribute('r',r);
      a.setAttribute('fill','none'); a.setAttribute('stroke-width',ep); a.setAttribute('stroke-linecap','butt');
      a.setAttribute('class',cls); if(col) a.setAttribute('stroke',col);
      if(frac<1){ a.setAttribute('stroke-dasharray',(C*frac)+' '+(C*(1-frac)));
                  a.setAttribute('transform','rotate('+rot+' '+cx+' '+cx+')'); }
      s.appendChild(a);
    }
    arc('au-piste', null, 1, 0);
    var an=-90, GA=2.6;
    for(var z=0; z<3; z++){ var pc=pa[z]*100; if(pc>GA) arc('au-arc', ETA[z][1], (pc-GA)/100, an); an+=pc*3.6; }
    box.appendChild(s);
    var f=visage(dph, nom, moi); f.style.left=f.style.top=((dia-dph)/2)+'px'; box.appendChild(f);
    w.appendChild(box);
    w.appendChild(el('div','au-lb', moi?'toi':nom));
    return w;
  }
  function cellule(p){
    var c=el('div','au-c'), bx=el('div','au-bx'), cv=el('canvas');
    cv.setAttribute('data-pid', p.id); bx.appendChild(cv); c.appendChild(bx);
    c.appendChild(el('span', null, p.title||''));
    return c;
  }
  function parId(id){ var L=tous(); for(var i=0;i<L.length;i++) if(L[i].id===id) return L[i]; return null; }
  /* §4 règle 5 : on peint APRÈS insertion, et on repasse — 0, 60, 200, 600 ms */
  function peintMoisson(){
    if(!GR) return;
    [].forEach.call(GR.querySelectorAll('canvas[data-pid]'), function(cv){
      if(cv.__ok) return;
      var p=parId(+cv.getAttribute('data-pid')), s=p&&dalleDe(p); if(!s) return;
      cv.width=s.width; cv.height=s.height; cv.getContext('2d').drawImage(s,0,0); cv.__ok=1;
    });
  }
  /* combien de dalles tenues « Ce que tu as tenu » porte : trois, ou six dès la règle des cinq */
  function nbMoisson(){ return (D && D.T.length>=K.RANG2) ? K.MOISSON : 3; }
  function remplit(){
    D=donnees();
    var vide = D.P.length===0;
    CAD.classList.toggle('au-vide', vide);
    if(vide){
      INV.textContent=''; INV.appendChild(document.createTextNode(VIDE[0]));
      INV.appendChild(el('em', null, VIDE[1])); MOT.textContent='';
    } else {
      /* le mot se tire du NOMBRE de paroles tenues : il change en faisant plus, jamais
         au hasard d'une ouverture, et jamais en laissant filer */
      MOT.textContent = D.n>0 ? MOTS[D.n % MOTS.length] : VIDE[0]; INV.textContent='';
    }
    NX.textContent='';
    if(!vide){
      NX.appendChild(noyau(K.toi.d, K.toi.arc, K.toi.ph, D.toi, 'toi', true));
      var gp=el('div','au-gp');
      D.gens.forEach(function(g){ gp.appendChild(noyau(K.pers.d, K.pers.arc, K.pers.ph, g.parts, g.nom, false)); });
      NX.appendChild(gp); NX.scrollLeft=0;
    }
    GR.textContent='';
    /* ⚑ DEUX RANGÉES, PAS UNE (Tom, 10 sept. — Q187). Une seule rangée laissait 60 à 84 pt de fond NU sous
       ses libellés jusqu'au bas de l'écran : « ça dit c'est fini, et personne ne défilera ». On ne pose
       ni flèche, ni ombre, ni fondu : une rangée DE PLUS, que le bord de l'écran coupe, dit qu'il y a la
       suite — le même principe que la rangée des six qui défile (le disque coupé est l'affordance).
       Jusqu'à six dalles tenues, les plus récentes d'abord. */
    var L=D.T.slice(-nbMoisson()).reverse();
    L.forEach(function(p){ GR.appendChild(cellule(p)); });
    var sans = vide || !L.length;
    MO.classList.toggle('au-sans', sans);
    /* la légende n'est centrée entre deux voisins que s'ils sont là tous les deux */
    if(sans) LG.removeAttribute('data-centre-entre');
    else LG.setAttribute('data-centre-entre', '.au-nx|.au-mo h3');
    [0,60,200,600].forEach(function(t){ setTimeout(peintMoisson, t); });
    CAD.scrollTop=0; ORB.colK=''; place();
    publie();
  }

  /* ⚑ LA COLONNE SE CALCULE — HAUTEUR DU BLOC + AIR, JAMAIS UNE COTE FIGÉE (CLAUDE.md §8).
     Tom, 10 sept. : « sous le commentaire de la sphère, les disques sont trop près : ça ne respire
     pas » — la cinquième fois qu'un espacement revient. MESURÉ (boîtes et encre, cinq phrases, deux
     thèmes) : la planche posait les Noyaux à 454, calcul fait pour une phrase d'UNE ligne (27,3 pt
     d'air à l'encre). Deux des cinq phrases en font DEUX : l'air tombait à 3,7. Et les libellés des
     dalles touchaient le bouton (2,7 pt), dans tous les états.
     Tout ce qui est sous la phrase se DÉRIVE donc de son bas réel : les Noyaux = bas de la phrase +
     l'air de la planche ; la légende et « Ce que tu as tenu » suivent du même écart (28 de chaque
     côté, inchangé) ; le bouton = bas des libellés + 28. Ce qui dépasse l'écran DÉFILE sous le
     plateau : le cadre défile et ROGNE au bas du plateau (y 100) — la parade de l'Index (§8, « un
     enfant absolu d'un conteneur qui défile défile »). La sphère garde `touch-action:none` : un doigt
     posé sur elle la tourne, il ne fait pas défiler. */
  function place(){
    if(!CAD) return;
    var c;
    if(CAD.classList.contains('au-vide')) c={nx:K.nx.y, lg:K.lgY, mo:K.mo.y, bt:K.bt.y};
    else {
      var nx=K.motY+MOT.offsetHeight+K.AIR_MOT, d=nx-K.nx.y;
      c={nx:nx, lg:K.lgY+d, mo:K.mo.y+d};
      var bas = MO.classList.contains('au-sans') ? c.lg+K.lgH : c.mo+MO.offsetHeight;
      c.bt=Math.max(K.bt.y, bas+K.AIR);
      /* ⚑ JAMAIS COUPÉ PAR LE PLI (Tom, 10 sept. — Q186 : « un vrai défaut, pas un choix ») : à
         l'ouverture, le bouton est ENTIER avec sa marge (bas ≤ 844 − 22), ou FRANCHEMENT sous le pli
         (haut ≥ 844). Avec l'air de 28, il ne peut plus être entier dès qu'il y a des Noyaux : il
         tombe sous le pli, et on le découvre en défilant. Mesuré avant : coupé de 3,4 pt (une ligne)
         et à mi-hauteur de son libellé (deux lignes). */
      if(c.bt+K.bt.h > K.PLI-K.marge && c.bt < K.PLI) c.bt=K.PLI;
    }
    c.fin=c.bt+K.bt.h+K.marge;
    var k=[c.nx,c.lg,c.mo,c.bt,c.fin].map(function(v){ return v.toFixed(2); }).join('|');
    if(k===ORB.colK) return;                 /* on compare avant d'écrire (§8) */
    ORB.colK=k; ORB.col=c;
    [[NX,c.nx],[LG,c.lg],[MO,c.mo],[BT,c.bt],[FIN,c.fin-1]].forEach(function(a){
      a[0].style.setProperty('top', a[1].toFixed(2)+'px', 'important'); });
  }

  /* ════════════════════════════════════════════════════════════════════════════
     LA SPHÈRE
     ════════════════════════════════════════════════════════════════════════════ */
  var ORB = { iles:null, cleI:'', palier:Math.max(0, Math.min(PALIERS.length-1, lsGet('promi_orbite_palier',0)|0)),
              ms:[], frames:0, skip:0, pret:false, cede:0, dernier:0 };
  ORB.vise=ORB.palier;   /* le palier VISÉ par le régulateur — il s'applique à l'ouverture suivante (densite) */
  var V = { lac:2.9, tan:G.TANG, vlac:0, vtan:0, om:G.AUTO, lacAv:2.9, tau:G.TAU };
  var EMP = null, TVER = 0, ATTENTE = [];
  /* les caresses en attente s'inscrivent quand tout est au repos (voir `lacher`) */
  function inscrit(){
    if(!ATTENTE.length || DG.on || V.vlac || V.vtan || EMP) return;
    var av=TRACES;
    TRACES=TRACES.concat(ATTENTE).slice(-G.TRACES); ATTENTE=[]; TVER++;
    lsSet('promi_orbite_traces', TRACES); retouche(av, TRACES);
  }
  /* ⚑ UNE CARESSE SE RETOUCHE, ELLE NE REFAIT PAS TOUT LE CACHE. Mesuré au profileur : chaque
     inscription refaisait les 110 000 poils — relief `phi` compris, qui ne dépend pas des
     caresses — soit 240 à 340 ms d'image figée. On ne recalcule que les points proches des
     arcs qui entrent ou qui sortent (`OrbiteMoteur.retoucheTraces`). Les semis des autres
     paliers ne sont pas retouchés : on les INVALIDE, ils se referont entiers s'ils resservent
     — jamais avec des caresses périmées. */
  function retouche(av, nv){
    var S=semis();
    for(var N in SEMC) if(SEMC[N]!==S) SEMC[N].__stCle=null;
    if(!S.__st) return;
    var t0=performance.now(), n=M.retoucheTraces(S.__st, av, nv);
    ORB.retouche={points:n, ms:+(performance.now()-t0).toFixed(1)};
  }
  var TRACES = (function(){ var T=lsGet('promi_orbite_traces', []);
    if(!Array.isArray(T)) return [];
    return T.filter(function(g){ return g && g.a && g.d && g.a.length===3 && g.d.length===3 && isFinite(g.L); }).slice(-G.TRACES); })();

  var ATL=null;
  function atlas(){
    if(ATL) return ATL;
    var k=K.bo.d/620, T=[2.5*k, 4.4*k, 5.7*k, 7.3*k];
    return (ATL={a:M.atlasAlpha(M.GRAIN_POIL, T, M.ORI, M.NIVA, 0.15, 0.78, true, M.NVAR), t:T});
  }
  var SEMC={};
  function semis(){ var N=PALIERS[ORB.palier]; return SEMC[N] || (SEMC[N]=M.semisPavage(N, 77, 0.0, KDENS, 4, false, 0)); }
  /* la clé du cache ne porte PLUS les caresses : elles se retouchent en place (voir `retouche`) */
  function cleIles(){ if(ORB.iles) ORB.iles.cle='aura|'+ORB.cleI; }
  function iles(){
    var T=D.T, cle=T.map(cleMonde).join(',');
    if(ORB.iles && ORB.cleI===cle) return ORB.iles;
    var r=M.batIles(T.length, window.Toile.cols(), {pxr:PXR, mag:MAG, palette:window.Toile.getPalette(),
      /* ⚑ LA VRAIE DALLE DU PROMI. Elle occupe l'emprise que la planche taillait à son
         île (`g`, la cellule, en px CSS à l'échelle PXR/MAG) : son plus grand côté y est
         calé. La forme vient du moteur ; seule la TAILLE est réglée par l'île. */
      dalle:function(k, I, g){
        var s=dalleDe(T[k]); if(!s) return null;
        var cote=Math.max(s.width, s.height);
        return {cv:s, sx:s.width/2, sy:s.height/2, kk:cote/(g/(PXR/MAG)), monde:T[k].monde};
      }});
    ORB.iles=r; ORB.cleI=cle; cleIles();
    return r;
  }
  function empPour(E){
    return {c:E.c, ax:E.ax, a:E.a, el:E.el, dmax:E.dmax, p:E.p,
            biais:0.14, rho:0.085, ub:0.35, B:0.32, U:0.50};
  }
  function opts(){
    var A=atlas();
    return {css:K.bo.d, R:K.R, sol:ORB.solR||NAT[D.nature], tailles:A.t, atlas:A.a, semis:semis(),
            relief:FROISSE, env:ENV, kn:KN, lac:V.lac, tan:V.tan, pal:window.Toile.cols(),
            trame:ORB.sansIles?ilesVides():ORB.iles, libre:false, fond:'rgba(0,0,0,0)',
            velours:0, contre:0, duvet:0, grade:0, velours2:1, dresse:0,
            pousse:Math.min(1, D.n/34), traces:TRACES, peigneAxial:1, tracesIncr:1,
            emp:(EMP && EMP.p>=0.002) ? empPour(EMP) : null, peauVers:peauVers()};
  }
  /* pour la mesure seulement : une trame SANS île (`trame:null` fait lever le peintre — mesuré) */
  function ilesVides(){
    if(!ORB.ilesVides){ ORB.ilesVides=M.batIles(0, window.Toile.cols(), {pxr:PXR, mag:MAG,
        palette:window.Toile.getPalette(), dalle:function(){ return null; }});
      if(ORB.ilesVides) ORB.ilesVides.cle='aura|vide'; }
    return ORB.ilesVides;
  }
  function clair(){ var d=document.getElementById('device'); return !!(d && d.classList.contains('light')); }
  function peauVers(){
    if(!clair() || !D) return null;
    var c=NAT_CLAIR[D.nature]||NAT_CLAIR.promi, t=(ORB.peauT!=null)?ORB.peauT:K.PEAU_T;
    return t>0 ? [c[0],c[1],c[2],t] : null;
  }
  function mediane(L){ if(!L.length) return null; var s=L.slice().sort(function(a,b){return a-b;}); return s[s.length>>1]; }
  /* ⚑ LA DENSITÉ CÈDE — MAIS JAMAIS SOUS LES YEUX (Tom, 10 sept. : « il doit être imperceptible »).
     Un palier n'est PAS un sous-ensemble du précédent : c'est un AUTRE semis — la spirale dépend du
     nombre de poils, chaque poil change de place. Mesuré, même vue : 76 à 80 % des pixels changent
     d'un coup, et le premier passage à un palier refait le semis et le cache dans une seule image.
     Et il se déclenchait en plein élan. Une matière qui change sous le doigt parce que la machine
     peine, c'est le contraire de ce qu'on cherche.
     Le régulateur MESURE et VISE pendant qu'on regarde ; la vise est gardée (et d'une ouverture à
     l'autre), et elle s'applique quand l'écran se BÂTIT (`prepare`) — là où rien ne se voit.
     On ne décide que sur des images ordinaires : ni celle où le peintre refait son cache, ni celles
     où un doigt est posé (le contact a son coût). */
  function densite(ms, statique){
    if(statique){ ORB.skip=4; return; }
    if(ORB.skip>0){ ORB.skip--; return; }
    if(EMP) return;
    ORB.ms.push(ms); if(ORB.ms.length>90) ORB.ms.shift();
    ORB.frames++;
    if(ORB.ms.length<45) return;
    var med=mediane(ORB.ms.slice(-45)), N=PALIERS[ORB.palier], v;
    if(med>G.BUDGET){
      /* le palier le plus dense qui tiendrait le budget, au prorata des poils (banc_lent) */
      for(v=ORB.palier; v<PALIERS.length-1 && med*PALIERS[v]/N>G.BUDGET; v++);
    } else if(ORB.ms.length>=90 && ORB.palier>0){
      /* ⚠ ET ELLE REMONTE : si le palier du dessus, à ce prorata, tiendrait sous 15 ms. L'écart
         avec le seuil de descente (16,7) évite le va-et-vient. */
      v=(mediane(ORB.ms.slice(-90))*PALIERS[ORB.palier-1]/N<15) ? ORB.palier-1 : ORB.palier;
    } else if(ORB.ms.length>=90){ v=ORB.palier; } else return;
    if(v===ORB.vise) return;
    if(v>ORB.palier) ORB.cede++; else if(v<ORB.palier) ORB.remonte=(ORB.remonte||0)+1;
    ORB.vise=v; lsSet('promi_orbite_palier', v);
  }
  function actif(){ return SC.classList.contains('show'); }
  /* un autre écran PAR-DESSUS (le partage, l'aide, une personne) : on ne peint pas
     dessous. Ça se juge AU DOIGT — ce qui est vraiment au-dessus du centre de la sphère —
     jamais à la liste des écrans ouverts : une fiche restée ouverte SOUS l'Aura ne la
     couvre pas. Hors de la fenêtre on ne sait rien : on peint. */
  /* ⚠ ET ON NE LE DEMANDE QU'UNE IMAGE SUR SIX (~100 ms). `getBoundingClientRect` et
     `elementFromPoint` forcent le navigateur à mettre à jour styles et mise en page : à chaque
     image, dans la boucle, c'était payer au pire moment tout ce que le reste de l'app venait
     de salir. Un écran qui passe par-dessus met de toute façon plus de 100 ms à s'ouvrir. */
  var _couv=false, _couvN=0;
  function couvert(){
    if((_couvN++)%6) return _couv;
    return (_couv=couvertMesure());
  }
  function couvertMesure(){
    var r=CV.getBoundingClientRect(); if(!r.width) return false;
    var x=r.left+r.width/2, y=r.top+r.height/2;
    if(x<0||y<0||x>=window.innerWidth||y>=window.innerHeight) return false;
    var t=document.elementFromPoint(x, y);
    return !!t && !SC.contains(t);
  }
  function borne(t){ return Math.max(-G.TANGMAX, Math.min(G.TANGMAX, t)); }
  function majEmp(dt){
    if(!EMP) return;
    var now=performance.now();
    if(EMP.tr===0){ EMP.p=Math.min(1, (now-EMP.t0)/1000/G.MONTE); return; }
    /* on lâche : la matière encaisse et revient — et quand on LANCE, ce qui file
       par-dessus comble le creux, d'autant plus vite qu'on lance fort */
    var p=EMP.pRel*Math.exp(-(now-EMP.tr)/1000/G.IMP_TAU);
    EMP.comble+=G.COMBLE*V.om*dt;
    EMP.p=Math.max(0, p-EMP.comble);
    /* ⚠ ON NE LA RETIRE QUE QUAND ELLE EST INVISIBLE. À p = 0,02 elle était encore profonde de
       7 % (≈ 2 pt) et large de 0,11 rad : son retrait faisait un SAUT à la dernière image (Tom,
       10 sept. : « ça passe de trop loin encore déformé à net d'un coup »). À 0,002 elle ne fait
       plus que 0,4 pt, et ses effets se sont éteints avec elle (5 %, voir la part FE du peintre). */
    if(EMP.p<0.002) EMP=null;
  }
  var RAF=null, TP=0;
  function boucle(ts){
    if(!actif()){ RAF=null; TP=0; return; }
    RAF=requestAnimationFrame(boucle);
    /* ⚠ LE TEMPS RÉEL, JUSQU'À 100 ms PAR IMAGE. La planche bornait à 50 ms : sur un
       appareil qui peint à 130 ms, la rotation lente tombait au tiers de sa vitesse —
       le comportement cédait avec la densité. La borne ne sert qu'à ne pas sauter après
       une pause (onglet caché). */
    var dtR=TP ? (ts-TP)/1000 : 1/60, dt=Math.min(0.1, dtR); TP=ts;
    /* publié pour le juge : il lit le pas de temps de LA BOUCLE, pas le sien */
    ORB.tick=(ORB.tick||0)+1; ORB.dtReel=dtR;
    if(DG.on){
      V.om=Math.abs(V.lac-V.lacAv)/Math.max(dt,0.001); V.vlac=0; V.vtan=0;
    } else {
      /* ⚑ L'ÉLAN S'ÉTEINT, LA ROTATION LENTE NE S'ARRÊTE JAMAIS — et les deux
         S'ADDITIONNENT : il n'y a pas d'instant de reprise, donc pas de saccade. */
      var k=Math.exp(-dt/V.tau);
      V.vlac*=k; V.vtan*=k;
      if(Math.abs(V.vlac)<0.0008) V.vlac=0;
      if(Math.abs(V.vtan)<0.0008) V.vtan=0;
      if(!V.vlac && !V.vtan) V.tau=G.TAU;
      /* `fige` n'existe que pour le juge : comparer deux images à vue ÉGALE, sans que la
         rotation se mêle de la mesure. Le produit ne l'appelle jamais. */
      if(!ORB.fige){ V.lac+=(G.AUTO+V.vlac)*dt; V.tan=borne(V.tan+V.vtan*dt); }
      V.om=Math.sqrt((G.AUTO+V.vlac)*(G.AUTO+V.vlac)+V.vtan*V.vtan);
    }
    V.lacAv=V.lac;
    majEmp(dt);
    inscrit();
    if(!ORB.pret || couvert()) return;
    var S=semis(), av=S.__stCle, t0=performance.now();
    try{ M.peint(CV, opts()); }catch(e){ window._auraErreur=String(e&&e.stack||e); ORB.pret=false; return; }
    var ms=performance.now()-t0;
    ORB.dernier=ms; ORB.peints=(ORB.peints||0)+1;
    if(ORB.peints%30===0) place();
    densite(ms, S.__stCle!==av);
  }

  /* ── LE DOIGT ─────────────────────────────────────────────────────────────── */
  var DG={on:false, x:0, y:0, parc:0, hT:new Float64Array(16), hL:new Float64Array(16),
          hG:new Float64Array(16), hi:0, hn:0, tr0:null, trN:null, arcs:[], tap:0};
  function echelle(){ var d=document.getElementById('device'); var r=d?d.getBoundingClientRect():null;
    return r&&r.width ? r.width/390 : 1; }
  /* le point de la VUE sous le doigt (x à droite, y en bas, z vers nous), ou rien */
  function surBoule(cx, cy){
    var r=CV.getBoundingClientRect(); if(!r.width) return null;
    var R=r.width*K.R, x=(cx-(r.left+r.width/2))/R, y=(cy-(r.top+r.height/2))/R, q=x*x+y*y;
    return q>=1 ? null : [x, y, Math.sqrt(1-q)];
  }
  /* la vue ramenée dans l'objet — la transformation inverse de `peint` (prepEmp) */
  function versObjet(v){
    var cl=Math.cos(V.lac), sl=Math.sin(V.lac), ct=Math.cos(V.tan), st=Math.sin(V.tan);
    var zp=-v[1]*st+v[2]*ct, y=v[1]*ct+v[2]*st;
    return [v[0]*cl-zp*sl, y, v[0]*sl+zp*cl];
  }
  function nrm(v){ var m=Math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])||1; return [v[0]/m, v[1]/m, v[2]/m]; }
  function angle(a,b){ var d=a[0]*b[0]+a[1]*b[1]+a[2]*b[2]; return Math.acos(Math.max(-1, Math.min(1, d))); }
  /* une caresse est un ARC de grand cercle, au diamètre du doigt (0,27 rad) */
  function arc(a,b){ a=nrm(a); b=nrm(b); var d=a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    return {a:a, d:nrm([b[0]-d*a[0], b[1]-d*a[1], b[2]-d*a[2]]), L:angle(a,b), w:G.W, f:0.9}; }
  /* ⚑ LA TAILLE DE L'EMPREINTE SE CALCULE : a = demi-axe de la pulpe ÷ rayon de la
     boule. C'est le capteur qui tranche (largeur du contact) ; les pulpes du pouce et de
     l'index sont les BORNES. Sans capteur : le pouce. dmax / a = 0,58 (planche). */
  function doigt(e){
    var lo=PULPE.index[0]/K.Rpt, hi=PULPE.pouce[0]/K.Rpt, a=hi, elp=PULPE.pouce[1];
    if(e && e.pointerType==='touch' && e.width>4 && e.height>4){
      var s=echelle(), rx=Math.max(e.width,e.height)/2/s, ry=Math.min(e.width,e.height)/2/s;
      a=rx/K.Rpt; elp=Math.max(0.5, Math.min(1, ry/rx));
    }
    a=Math.max(lo, Math.min(hi, a));
    return {a:a, el:elp, dmax:0.58*a, ax:[0.62,-0.72,0]};
  }
  function relisse(){ var av=TRACES; TRACES=[]; ATTENTE=[]; TVER++; lsSet('promi_orbite_traces', []); retouche(av, TRACES); }
  function gestesBoule(){
    PRISE.addEventListener('pointerdown', function(e){
      DG.on=true; try{ PRISE.setPointerCapture(e.pointerId); }catch(_){}
      DG.x=e.clientX; DG.y=e.clientY; DG.parc=0; DG.hn=0; DG.hi=0; DG.arcs=[];
      V.vlac=0; V.vtan=0; V.tau=G.TAU;
      var v=surBoule(e.clientX, e.clientY);
      if(v){ var f=doigt(e);
        EMP={c:v, ax:f.ax, a:f.a, el:f.el, dmax:f.dmax, p:0, t0:performance.now(), tr:0, pRel:0, comble:0};
        DG.tr0=versObjet(v); DG.trN=DG.tr0;
      } else { DG.tr0=null; DG.trN=null; }
      e.preventDefault();
    });
    PRISE.addEventListener('pointermove', function(e){
      if(!DG.on) return;
      /* ⚠ L'HEURE DE L'ÉVÉNEMENT, PAS CELLE DU TRAITEMENT — et chacun des événements
         REGROUPÉS. Quand une image est lente, le navigateur livre plusieurs mouvements en
         un seul appel : horodatés au traitement, ils tombaient « au même instant », la
         vitesse sortait nulle et l'ÉLAN ÉTAIT PERDU. Sur un appareil lent, c'est le
         comportement qui aurait cédé — jamais permis. */
      var L=(e.getCoalescedEvents && e.getCoalescedEvents()) || [];
      if(!L.length) L=[e];
      var s=echelle();
      for(var c=0;c<L.length;c++){
        var ce=L[c], dx=(ce.clientX-DG.x)/s, dy=(ce.clientY-DG.y)/s;
        DG.x=ce.clientX; DG.y=ce.clientY; DG.parc+=Math.sqrt(dx*dx+dy*dy);
        /* le sens est celui du doigt : la surface qu'on touche suit la main */
        V.lac+=dx*G.SENS; V.tan=borne(V.tan-dy*G.SENS);
        DG.hT[DG.hi]=ce.timeStamp||e.timeStamp||performance.now(); DG.hL[DG.hi]=dx*G.SENS; DG.hG[DG.hi]=-dy*G.SENS;
        DG.hi=(DG.hi+1)%16; if(DG.hn<16) DG.hn++;
      }
      var v=surBoule(e.clientX, e.clientY);
      if(v){
        if(EMP && EMP.tr===0) EMP.c=v;
        var o=versObjet(v);
        if(!DG.tr0) DG.tr0=o;
        else if(angle(DG.tr0, o)>=0.6){ DG.arcs.push(arc(DG.tr0, o)); DG.tr0=o; }
        DG.trN=o;
      }
      e.preventDefault();
    });
    function lacher(e){
      if(!DG.on) return;
      DG.on=false;
      var now=(e && e.timeStamp) || performance.now();
      if(EMP && EMP.tr===0){ EMP.pRel=EMP.p; EMP.tr=now; }
      if(DG.parc<=G.TAP){
        /* un toucher : il creuse et revient. Deux touchers rapprochés : tout se relisse. */
        if(e && e.type==='pointerup' && now-DG.tap<G.DOUBLE){ relisse(); DG.tap=0; }
        else DG.tap=now;
        return;
      }
      DG.tap=0;
      /* l'élan : la vitesse des 90 dernières millisecondes, bornée */
      var sl=0, st=0, t0=now;
      for(var i=0;i<DG.hn;i++){ var j=(DG.hi-1-i+32)%16; if(now-DG.hT[j]>90) break; sl+=DG.hL[j]; st+=DG.hG[j]; t0=DG.hT[j]; }
      var dtt=(now-t0)/1000;
      if(dtt>0.012){ V.vlac=Math.max(-G.VMAX, Math.min(G.VMAX, sl/dtt));
                     V.vtan=Math.max(-G.VMAX, Math.min(G.VMAX, st/dtt)); }
      DG.elan={sl:sl, st:st, dtt:dtt, hn:DG.hn, now:now, der:DG.hT[(DG.hi+15)%16], vlac:V.vlac};
      /* la trace reste : le chemin que le doigt a parcouru SUR L'OBJET */
      if(DG.tr0 && DG.trN && angle(DG.tr0, DG.trN)>=0.08) DG.arcs.push(arc(DG.tr0, DG.trN));
      /* ⚠ ET ELLE S'INSCRIT AU REPOS, PAS AU LÂCHER. Une caresse oblige le peintre à refaire
         tout son cache — une image de ~300 ms. Inscrite au lâcher, elle tombait PILE quand
         l'élan est le plus fort : une saccade, exactement ce que l'acquis interdit (mesuré
         par le juge : une chute de vitesse en une image). On l'inscrit quand tout est
         revenu : doigt levé, élan éteint, creux refermé. C'est aussi ce que dit la planche —
         la forme revient, ce qui reste c'est le poil couché. */
      if(DG.arcs.length) ATTENTE=ATTENTE.concat(DG.arcs);
      DG.arcs=[]; DG.tr0=null; DG.trN=null;
    }
    PRISE.addEventListener('pointerup', lacher);
    PRISE.addEventListener('pointercancel', lacher);
  }
  /* un toucher ouvre la personne ; un glissement fait défiler la rangée, et n'ouvre rien */
  function gestesNoyaux(){
    var d0=null;
    NX.addEventListener('pointerdown', function(e){
      d0={x:e.clientX, y:e.clientY, n:e.target.closest?e.target.closest('.au-n'):null, sl:NX.scrollLeft}; });
    NX.addEventListener('pointercancel', function(){ d0=null; });
    NX.addEventListener('pointerup', function(e){
      if(!d0) return; var s=echelle(), n=d0.n;
      var dd=Math.sqrt(Math.pow(e.clientX-d0.x,2)+Math.pow(e.clientY-d0.y,2))/s + Math.abs(NX.scrollLeft-d0.sl)/s;
      d0=null;
      if(dd>G.TAP || !n) return;
      var q=n.getAttribute('data-qui');
      if(q && q!=='moi' && typeof openPerson==='function'){ window._auraOuvre=q; openPerson(q); }
    });
  }

  /* ⚑ UNE PAROLE DE PLUS : L'ORBITE FAIT UN TOUR pour présenter la dalle qu'on vient de
     poser. Le levier est le GESTE : c'est un élan, qui s'additionne à la rotation lente
     et s'y rend sans saccade. La vue qui centre une direction se calcule :
        lac = atan2(−c0, c2)     tan = atan2(c1, hypot(c0, c2))                      */
  function tourSiNeuf(){
    var vus=lsGet('promi_orbite_vus', null); lsSet('promi_orbite_vus', D.n);
    if(vus===null || D.n<=vus || !ORB.iles || !ORB.iles.derniere) return;
    var c=ORB.iles.derniere, lacT=Math.atan2(-c[0], c[2]), tanT=Math.atan2(c[1], Math.sqrt(c[0]*c[0]+c[2]*c[2]));
    var dl=((lacT-V.lac)%6.283185307+6.283185307)%6.283185307; if(dl<3.14159) dl+=6.283185307;
    V.tau=G.TOUR_TAU; V.vlac=dl/G.TOUR_TAU; V.vtan=(borne(tanT)-V.tan)/G.TOUR_TAU; ORB.tour=D.n;
  }

  function publie(){
    if(!D) return;
    window._auraComp = {
      vide:CAD.classList.contains('au-vide'), n:D.n, nature:D.nature, sol:NAT[D.nature],
      iles:D.T.map(function(p){ var m=p.monde||{}; return {pid:p.id, titre:p.title, monde:[m.m,m.p,m.h]}; }),
      ilesPeintes:ORB.iles ? ORB.iles.iles.filter(function(I){ return !!I.m; }).length : 0,
      derniere:(ORB.iles && ORB.iles.derniere) ? ORB.iles.derniere.slice() : null,
      toi:D.toi, gens:D.gens.map(function(g){ return {nom:g.nom, parts:g.parts}; }),
      moisson:D.T.slice(-nbMoisson()).reverse().map(function(p){ return p.id; }),
      mot:MOT.textContent, photoMoi:!!(typeof USER!=='undefined' && USER && USER.photo)
    };
  }
  window._aura = {
    etat:function(){ return {pret:ORB.pret, lac:V.lac, tan:V.tan, vlac:V.vlac, vtan:V.vtan, om:V.om,
      prise:DG.on, emp:EMP?{p:EMP.p, relache:EMP.tr>0, c:EMP.c, a:EMP.a}:null, traces:TRACES.length,
      attente:ATTENTE.length,
      tver:TVER, palier:PALIERS[ORB.palier], vise:PALIERS[ORB.vise], ms:mediane(ORB.ms), dernier:ORB.dernier,
      frames:ORB.frames, peints:ORB.peints||0, cede:ORB.cede, remonte:ORB.remonte||0,
      tick:ORB.tick||0, dtReel:ORB.dtReel||0, retouche:ORB.retouche||null,
      erreur:window._auraErreur||null, tour:ORB.tour||0, elan:DG.elan||null, col:ORB.col||null}; },
    relisse:relisse, K:K, G:G, PALIERS:PALIERS, MOTS:MOTS,
    /* pour le juge : poser la phrase i (null = celle des données) et recalculer la colonne */
    mot:function(i){ if(!CAD || CAD.classList.contains('au-vide')) return null;
      MOT.textContent = (i===null||i===undefined) ? (D.n>0 ? MOTS[D.n % MOTS.length] : VIDE[0])
                                                  : MOTS[((i|0)%MOTS.length+MOTS.length)%MOTS.length];
      place(); return MOT.textContent; },
    /* pour le juge : repartir d'un palier donné (0 = 110 000) et oublier les mesures */
    palier:function(i){ ORB.palier=ORB.vise=Math.max(0, Math.min(PALIERS.length-1, i|0)); ORB.ms=[]; ORB.skip=4; },
    /* pour la preuve : le cache RETOUCHÉ est-il celui qu'une reconstruction complète donnerait
       avec les mêmes caresses ? On copie, on reconstruit, on compare point par point. */
    verifie:function(){
      var S=semis(); if(!S.__st) return null;
      var A=S.__st, Q0=A.Q.slice(), P0=A.po.slice(), E0=A.ew.slice(), n0=A.n;
      var t0=performance.now(); S.__stCle=null; M.peint(CV, opts()); var ms=performance.now()-t0;
      var B=S.__st; if(B.n!==n0) return {n:[n0,B.n]};
      var df=0, dp=0, de=0, np=0, ne=0;
      for(var i=0;i<B.n;i++){
        for(var j=7;j<10;j++){ var d=Math.abs(Q0[i*10+j]-B.Q[i*10+j]); if(d>df) df=d; }
        var a=Math.abs(P0[i]-B.po[i]); if(a>dp) dp=a; if(a>1) np++;
        var b=Math.abs(E0[i]-B.ew[i]); if(b>de) de=b; if(b>1) ne++;
      }
      return {points:B.n, flux:df, poli:dp, poliHors1:np, main:de, mainHors1:ne, reconstruction_ms:+ms.toFixed(1)};
    },
    /* pour le juge : figer la vue, poser une vue — jamais appelés par le produit */
    fige:function(b){ ORB.fige=!!b; },
    /* pour la mesure du thème clair (Q182) : la part de teinte de la peau (null = celle décidée), et la
       boule SANS ses îles (le masque qui isole leur contraste) — jamais appelés par le produit */
    reglePeau:function(t){ ORB.peauT=(t===null||t===undefined)?null:+t; },
    /* pour la mesure (Q182) : la couleur du POIL du sol ([r,g,b], null = la nature) */
    regleSol:function(c){ ORB.solR=c?[c[0]|0,c[1]|0,c[2]|0]:null; var S=semis(); S.__stCle=null; },
    sansIles:function(b){ ORB.sansIles=!!b; var S=semis(); S.__stCle=null; },
    vue:function(l,t){ V.lac=+l; V.tan=borne(+t); V.lacAv=V.lac; V.vlac=0; V.vtan=0; }
  };

  function prepare(){
    ORB.pret=false;
    /* la vise du régulateur prend effet ICI, pendant que l'écran se bâtit — jamais sous les yeux */
    if(ORB.vise!==ORB.palier){ ORB.palier=ORB.vise; ORB.ms=[]; ORB.skip=4; }
    var E=[function(){ atlas(); }, function(){ semis(); }, function(){ iles(); },
           function(){ ORB.pret=true; tourSiNeuf(); publie(); }];
    var i=0;
    (function suite(){
      if(!actif()) return;
      try{ E[i](); }catch(e){ window._auraErreur=String(e&&e.stack||e); }
      i++; if(i<E.length) setTimeout(suite, 0);
    })();
  }
  function ouvre(){
    try{ squelette(); remplit(); prepare(); }catch(e){ window._auraErreur=String(e&&e.stack||e); }
    if(!RAF){ TP=0; RAF=requestAnimationFrame(boucle); }
  }
  /* on s'accroche à la classe `show` — un observateur QUI COMPARE AVANT D'AGIR (§8) */
  var _vu=SC.classList.contains('show');
  try{ new MutationObserver(function(){
      var s=SC.classList.contains('show'); if(s===_vu) return; _vu=s; if(s) ouvre();
    }).observe(SC, {attributes:true, attributeFilter:['class']}); }catch(e){}
  squelette();
  if(_vu) ouvre();
})();
