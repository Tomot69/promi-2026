
/* ════════════════════════════════════════════════════════════════════════════
   lot-AURA-PELOTE — L'ÉCRAN AURA, RÉÉCRIT EN ENTIER · 10 septembre 2026
   ────────────────────────────────────────────────────────────────────────────
   Ce qu'il porte, de haut en bas, et rien d'autre (PLANCHE-VELOURS.html) :
     LA SPHÈRE    le velours, ses dalles dans le monde de LEUR plantation, et la
                  mémoire de la main. Aucun nom dessus : l'image se partage.
     LE MOT       il qualifie L'OBJET, dans le registre du rejeu. Ni note, ni verdict.
     LES NOYAUX   « toi » puis les personnes, §2.9 : piste neutre, trois arcs d'état,
                  l'image de la personne (sa photo si elle existe), le prénom.
     LA LÉGENDE   elle nomme les trois arcs — elle se déclare centrée.
     CE QUE TU AS TENU   les trois dernières paroles tenues, en vraies dalles.
     LE BOUTON    Partager ma Pelote.
   Les huit acquis de la sphère (ÉTAT DES LIEUX, clôture de la Pelote) sont ici :
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
  var M = window.PeloteMoteur, SC = document.getElementById('auraScreen');
  if(!M || !SC || !window.Toile) return;

  /* ── LES COTES — planche ÷ 0,872 ; une cote se CALCULE, elle ne se mesure jamais
        sur elle-même (§8). ───────────────────────────────────────────────────── */
  var K = { bo:{x:47, y:89.4, d:296}, R:0.392,
            nx:{y:454, h:107}, mo:{y:633}, lgH:24.25, lgINK:0, cptH:30, cptAIR:16, cptINK:-3.5,   /* v97 (Tom, iPhone : « la bande des chiffres est trop près de la légende — écarte-les, et descends « Partager ma Pelote » en conséquence ») : 10 → 16 */   /* v95 : relevé sur l'image rendue (WebKit, deux thèmes) : 30,9 au-dessus du groupe, 34,4 en dessous → −3,5 */   /* v95 : la rangée des chiffres (PromiLate 29, interligne 30) et son air sous la légende */   /* ⚑ 20 sept. (Tom) : la légende grossit — 13 → 15 px, le niveau « libellé » du §6. `lgY` se RECALCULE, l'air reste égal des deux côtés (27 et 27, contre 28 et 28 à 13 px). */ bt:{y:762, h:60}, motY:394.08, motL:19.4*1.25, marge:22,
            /* ⚑ 22 sept. (Tom) : « les disques sont trop fins partout ». L'arc passe de 8 à 12
               sur « toi » et de 6 à 9 sur une personne — la moitié en plus, comme sur les fiches.
               Le diamètre et la photo ne bougent pas : c'est l'ANNEAU qui s'épaissit, vers l'intérieur. */
            toi:{d:78, arc:12, ph:48}, pers:{d:58, arc:9, ph:36} };
  /* ⚑ 22 SEPTEMBRE 2026 (Tom) — « L'AIR AU-DESSUS ET EN DESSOUS DOIT ÊTRE ÉGAL, À L'ENCRE. »
     La boîte, elle, est centrée par construction — elle l'a toujours été. Mais l'ENCRE ne
     tombe pas au milieu de sa boîte de ligne : Gilbert s'y pose légèrement bas, et les trois
     blocs de la bande n'ont pas le même interligne. Mesuré à 30 px, sur l'image rendue, dans
     les deux thèmes : 30,5 au-dessus, 28,0 en dessous — l'encre est 1,25 px trop bas.
     `lgINK` est donc une COTE DÉCLARÉE, comme les largeurs de libellé du §8 : elle se relève
     une fois, police chargée, et elle s'écrit ici. Elle ne se mesure jamais à l'exécution —
     sinon la cote se mesurerait sur elle-même, et l'écran oscillerait (§8). */
  /* ⚑ 23 sept. — la légende est repassée à 19,4 px : l'écart d'encre se remesure (31,5 / 34,0
     à lgINK −1,25), il vaut donc −0,5 (mesuré : −1,25 donne 31,5 / 34,0 et 0 donne 33,5 / 32,0 — le zéro est entre les deux). */
  /* ⚑ 23 sept., second tour — LE VOISIN DU BAS N'EST PLUS UN TITRE, C'EST LE BOUTON.
     `lgINK` corrige l'écart entre la BOÎTE et l'ENCRE ; il valait −0,5 contre un titre de
     moisson. Contre le bouton, mesuré sur l'image rendue avec l'air de 28 des deux côtés :
     **36,5 au-dessus, 31,0 en dessous** — le contour du bouton commence plus haut dans sa
     boîte que l'encre d'un titre. On rend les 5,5 : l'air de BOÎTE au-dessus vaut 28 − 6, celui
     d'en dessous reste 28, et l'ENCRE tombe égale des deux côtés. C'est la demande de Tom du
     22 septembre, appliquée au nouveau voisin. */
  K.lgINK = -6;
  K.lgY = K.nx.y + K.nx.h + (K.mo.y - (K.nx.y + K.nx.h) - K.lgH) / 2 + K.lgINK;
  K.Rpt = K.bo.d * K.R;                                                  /* 116 pt */
  /* ⚑ L'AIR DE LA COLONNE — deux valeurs, prises dans la planche, jamais à l'œil (voir `place`) :
     sous la phrase, l'air que la planche laissait sous UNE ligne (454 − 403,7 − 23,625) ; entre les
     autres blocs, le rythme de la planche — la légende y est centrée à 28 de chaque côté. */
  /* ⚑ 23 sept. — L'AIR EST LE MÊME AU-DESSUS ET EN DESSOUS DE LA PHRASE (Tom). Il ne se
     déduit plus de la planche : il EST la cote, et c'est `motY` qui s'en déduit
     (353,4 = bas de la boule ; 353,4 + 37,5 = 390,9). 37,5 est la valeur qui laisse la rangée
     des Noyaux à 454 pour une phrase d'une ligne — la cote de la planche, inchangée. */
  /* ⚑ ET L'ÉGALITÉ SE JUGE À L'ENCRE (Tom, 22 sept.), pas aux boîtes : Gilbert se pose haut
     dans sa boîte de ligne. Mesuré sur l'image rendue, les deux thèmes : 34,0 au-dessus,
     39,0 en dessous — l'encre est 2,5 px trop haut. `MOT_INK` est donc une COTE DÉCLARÉE :
     la boîte descend de 2,5 et l'air du dessous en rend autant, pour que la rangée des Noyaux
     reste à 454. Air à l'encre après : 36,5 / 36,5. */
  K.MOT_INK = 2.5;
  K.AIR_MOT = 38.18 - K.MOT_INK;
  K.BOULE_BAS = K.bo.y + K.bo.d/2 + K.bo.d*K.R;                          /* 353,4 — la BOULE, pas sa boîte */
  K.AIR = 28;
  K.PLI = 844;
  K.MOISSON = 6;                                                         /* deux rangées de trois (Q187) */
  /* ⚑ RÈGLE (Tom, 10 sept. — Q189) : LA SECONDE RANGÉE PARAÎT À PARTIR DE CINQ DALLES TENUES. En dessous,
     la première rangée seule : une rangée au tiers (3 + 1) dit « il en manque deux ». À cinq, le trou
     d'une case à droite est accepté (mesuré : il se voit à l'ouverture). */
  K.RANG2 = 5;
  /* ⚑ FIXÉ À LA MESURE (Tom, 10 sept. — Q182, « A », puis « rattrape le 93 sans toucher aux dalles, trois
     essais ») : la peau part ENTIÈREMENT (t = 1) vers la teinte claire de la nature, elle-même tirée à 60 %
     vers le crème du corps. Mesuré contre le sombre (même page) : boule ↔ page 85 (sombre 72–76 ; A seul
     93–96), contour 95, dalles aussi lisibles qu'en sombre. Les 9 points au-dessus de 76 sont ASSUMÉS :
     un excès de présence, pas une dissolution. */
  /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « ON VOIT LA LUMIÈRE À TRAVERS ». C'ÉTAIT ICI, ET C'EST LE
     MODE CLAIR. À t = 1, la peau ne gardait RIEN de la couleur du lieu : elle partait
     entièrement vers le crème. Le poil clair est sombre (palette × SOL_CLAIR) — on avait donc
     des fibres sombres sur un fond CRÈME, et entre elles c'est la page qu'on croyait voir.
     Mesuré, mode clair : p05 58 · p95 233, une étendue de 175 sur 255. À 0,78 la peau garde un
     cinquième de la couleur du lieu : l'étendue tombe à 160 et le pelage redevient une matière,
     pas une hachure. En dessous (0,50 essayé, regardé) le grain disparaît et la boule sort
     lisse — la peau doit rester PLUS CLAIRE que le poil, seulement moins loin. */
  K.PEAU_T = 0.78;
  K.PEAU_CREME = 0.6;                                                           /* le bas de l'écran, à l'ouverture */

  /* ── LE SOL DIT LA NATURE ; LES ARCS DISENT L'ÉTAT. Menthe et terracotta ne servent
        qu'aux états, nulle part ailleurs. ─────────────────────────────────────── */
  var NAT = { promi:[130,174,248], chiche:[255,184,210], nuee:[201,168,245] };
  /* ⚑ LE THÈME CLAIR — SOL CLAIR, POIL SOMBRE (Tom, 10 sept. — Q182) : « le vrai négatif du thème sombre ;
     le champ garde sa couleur de nature, c'est la matière qui s'adapte au corps ». Le poil garde la couleur
     de nature ; la PEAU sous lui, que le peintre assombrit (× 0,64) pour qu'en sombre chaque poil se
     détache en clair, s'ÉCLAIRCIT en clair vers la TEINTE CLAIRE DE LA NATURE (PROMI-SPECIFICATIONS §1.2) :
     chaque poil s'y détache en sombre. La part de teinte (`K.PEAU_T`) se choisit À LA MESURE, contre le
     thème sombre : écart boule ↔ page, contour, lisibilité des îles. */
  var NAT_CLAIR = { promi:[0xCB,0xAA,0xFF], chiche:[0xFF,0xC0,0xA8], nuee:[0xD0,0xB0,0xFF] };
  /* ⚑ 21 sept. — c'était encore [0xF4,0xEE,0xE1] = #F4EEE1, le fond clair d'AVANT le
     16 septembre. Il sert à tirer le sol de la sphère vers le crème en mode clair :
     une valeur périmée y décalait la couleur du sol à chaque rendu. (§8, les triplets.) */
  var CREME = [0xF7,0xF0,0xDE];                                          /* le fond clair (§3) */
  /* ⚑ 21 SEPTEMBRE 2026 (Tom) — LES TROIS ÉTATS DE L'AURA BASCULENT AVEC LE THÈME.
     « Les arcs des Noyaux et la légende portent encore les anciennes couleurs. Ils doivent
       porter les valeurs d'état v7 : à tenir #DD4D23, en cours #291547, tenu #00341A.
       En mode clair, ce sont les profondes. »
     La colonne de l'Aura est posée SUR LA PAGE, pas sur un plateau : en clair elle porte donc
     les valeurs PROFONDES, en sombre leurs claires. C'est la règle du §3 — une marque suit ce
     qui est peint SOUS elle — et c'est pour ça que l'anneau du + de l'accueil, lui, garde les
     claires dans les deux thèmes : il est posé sur la barre sombre.
     ⚠ LE VERMILLON NE BASCULE PAS : il se lit des deux côtés (Δlum 65 sur la crème, 65 sur
     le fond sombre). C'est déjà ce que dit `--c-orange53-txt`, qui vaut #DD4D23 en sombre. */
  /* ⚑ 22 sept. (Tom) : UNE SEULE TABLE. Les trois valeurs, dans les deux thèmes. */
  var ETAT3 = [['tenues','#00341A'], ['en cours','#291547'], ['à tenir','#DD4D23']];
  function eta(){ return ETAT3; }
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
  var G = { AUTO:6.283185307/100, /* ⚑ UN TOUR EN 100 s (Tom, 12 sept.). */ TANG:0.32, TANGMAX:1.15, TAU:0.55, VMAX:11, TAP:6,
            SENS:0.011*142/K.Rpt, MONTE:0.09, IMP_TAU:1.35, COMBLE:0.42,
            /* ⚑ LA LOI DE CONTACT D'UNE BALLE ANTISTRESS (Tom, 18 sept. 2026 : « plus de raideur, un retour plus net ;
               une vraie boule molle, avec un peu de résistance agréable »). La loi d'avant — MONTE, IMP_TAU —
               enfonçait jusqu'au fond en 0,09 s et remontait en τ 1,35 s (≈ 8 s avant de disparaître) : une
               mousse à mémoire, « un plastique qui s'affaisse ». Maintenant la matière CÈDE vite puis RÉSISTE
               (deux constantes : 62 % en τ 0,05 s, le reste en τ 0,50 s), s'enfonce moins (profondeur 0,46 ×
               la pulpe au lieu de 0,58), et REPOUSSE le doigt parti en τ 0,15 s — creux effacé en ≈ 0,95 s.
               MONTE et IMP_TAU restent déclarés : ils ne servent plus qu'à l'histoire. */
            CEDE:0.62, CEDE_TAU:0.05, RESISTE_TAU:0.50, PROF:0.46, REPOUSSE_TAU:0.15,
            /* ⚠ un retour plus rapide saute plus loin d'une image à l'autre : l'empreinte se retire à p 0,0004
               (creux à 0,5 % de sa profondeur) au lieu de 0,002 — sinon le dernier pas dépassait 1 niveau (mesuré 1,23). */
            EMP_FIN:0.0004, DOUBLE:350,
            TRACES:48, W:0.27,   /* ⚑ v21 : 9 → 48 — un glissement couche le poil à chaque pas, les 9 dernières effaçaient la trace */ TOUR_TAU:1.1, BUDGET:16.7 };
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
    var O=lsGet('promi_pelote_ordre', []); if(!Array.isArray(O)) O=[];
    O=O.filter(function(id){ return par[id]; });
    T.filter(function(p){ return O.indexOf(p.id)<0; }).sort(function(a,b){ return a.id-b.id; })
     .forEach(function(p){ O.push(p.id); });
    lsSet('promi_pelote_ordre', O);
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
                 .map(function(n){ return {nom:n, parts:parts(m[n]), liste:m[n]}; });
  }
  /* ⚑ CE QU'ON TE TIENT (Q215, Tom 14 sept.) — ce qu'une personne te promet à toi, sa moitié d'un Chiche relevé avec toi, ce
     qu'elle promet à une de tes Nuées. Celui qui tient déclare, tu reçois : on lit son état, on ne le décide jamais. */
  function envers(){
    var out=[];
    tous().forEach(function(p){ if(!p || p.draft || p.req) return;
      var de=(p.from && p.from!=='moi' && !estMoi(p.from)) ? p.from : null;
      var aMoi=(!p.who || p.who==='moi' || estMoi(p.who));
      if(de && (aMoi || (p.nuee && typeof NUE!=='undefined' && NUE[p.nuee]))) out.push({nom:de, p:p});
      else if(!de && p.chiche && p.chicheEtat==='releve' && p.avec && !estMoi(p.avec)) out.push({nom:p.avec, p:p});
    });
    return out;
  }
  /* ⚑ LA RANGÉE : qui te promet sans que tu lui promettes y entre aussi (Q215 · 3). ORDRE ALPHABÉTIQUE, jamais par valeur. */
  function gensRecip(P, E){
    /* ⚑ 22 SEPTEMBRE 2026 (Tom) — UN ANNEAU NE PEUT AVOIR QUE TROIS ARCS : à tenir, en cours,
       tenu. « S'il y en a davantage, le système est cassé. »
       CE QUI PRODUISAIT LES SEGMENTS EN TROP, mesuré (`scratchpad/anneaux.py`) : le lot de la
       réciprocité (Q215, 14 sept.) peignait DEUX MOITIÉS — à gauche `parts` (ce que tu tiens
       envers la personne), à droite `recu` (ce qu'elle te tient) — soit 3 états × 2 moitiés =
       jusqu'à SIX arcs. Relevé : « toi » 6, Marion 5, Rachel 4. Et pour Adrien et Nico, seule
       la moitié DROITE existait : leur anneau ne disait que ce qu'ON te tient, présenté comme
       si c'était ta parole. C'est ça, la logique cassée.
       CE QU'ON FAIT : l'anneau porte LES TROIS ÉTATS DE CE QUI SE PROMET ENTRE VOUS, dans les
       deux sens, UNE FOIS. On concatène les LISTES avant d'en faire des parts — la pondération
       se fait donc par le NOMBRE de paroles, jamais à parts égales entre les deux directions.
       La réciprocité ne se perd pas : elle garde sa rangée « Ce qu'on t'a tenu » (Q215). */
    var m={}, lst={}; personnes(P).forEach(function(g){ m[g.nom]=g.parts; lst[g.nom]=g.liste||[]; });
    var r={}; E.forEach(function(x){ if(x.nom==='le groupe') return; (r[x.nom]=r[x.nom]||[]).push(x.p); });
    return Object.keys(m).concat(Object.keys(r).filter(function(n){ return !m[n]; }))
      .sort(function(a,b){ return a.localeCompare(b,'fr'); })
      .map(function(n){
        var tout=(lst[n]||[]).concat(r[n]||[]);
        return {nom:n, parts:tout.length?parts(tout):null, recu:r[n]?parts(r[n]):null, nRecu:(r[n]||[]).length};
      });
  }
  function donnees(){
    var P=mesPromi(), T=ordreTenus(P), E=envers();
    var RT=E.filter(function(x){ return x.p.status==='tenu'; }).map(function(x){ return x.p; }).sort(function(a,b){ return a.id-b.id; });
    return {P:P, T:T, n:T.length, nature:natureMaj(T), toi:parts(P), gens:gensRecip(P,E), recu:E.length?parts(E.map(function(x){ return x.p; })):null, RT:RT};
  }
  function cleMonde(p){ var m=p.monde||{}; return p.id+'|'+m.m+'/'+m.p+'/'+m.h; }

  /* ⚑ UNE DALLE SE REND UNE FOIS (CLAUDE.md §4) — un cache par Promi et par monde.
     Toujours la vraie dalle du moteur, échelle 1, dans le monde de SA plantation. */
  var DALLES = {};
  function dalleDe(p){
    var k=cleMonde(p); if(DALLES[k]) return DALLES[k];
    var cv=document.createElement('canvas'), ok=false;
    /* ⚑ v29 — le moteur rend aussi SES pixels (`donnees`) : la Pelote en tisse une fourrure, elle ne les relit pas */
    try{ ok=window.Toile.dalleTrame(cv, p.id, 1, p.monde||undefined, {donnees:true}); }catch(e){}
    if(!ok || !cv.width) return null;
    return (DALLES[k]=cv);
  }

  /* ⚑ CHANTIER 59 — SEULE LA TEINTE CÈDE. Décision Tom (10 sept.) : « la mémoire du monde est préservée,
     seule la teinte cède, et ça ne touche que les dalles concernées » ; précisée le 12 sept. : « remplacer
     la couleur par une autre du même monde ».
     LE DÉFAUT : la couleur d'une dalle est tirée au hasard par le moteur (`cc()`, `Math.random`) ; quand le
     tirage tombe près du sol de la sphère, la dalle ne se lit plus. Mesuré par `releve-aura` : « planter un
     arbre » à ΔE 12,3 (sombre) et 12,4 (clair), plancher 15 — et 6 chargements sur 10 portent au moins une
     dalle sous le plancher (Q192, CHANTIERS n° 59).
     CE QU'ON NE TOUCHE PAS : ni le moteur de la Toile (§9 — `cc()` est son code), ni le sol, ni la mémoire
     du Promi (`p.monde` reste ce qu'il était, la Toile de l'accueil ne bouge pas d'un pixel).
     CE QU'ON FAIT : sur la dalle DÉJÀ RENDUE, on remappe la teinte sur une autre couleur DE SA PALETTE —
     celle du Studio, donc du même monde — en gardant la CLARTÉ de chaque pixel. La forme ne bouge pas (§4),
     les strates du motif vivent dans la clarté : c'est l'idiome de Q30, qui remappe déjà la luminosité dans
     la bande haute d'une fiche.
     POURQUOI L'ÉCART SE MESURE EN TEINTE SEULE : ΔE = √(ΔL² + Δa² + Δb²) ≥ √(Δa² + Δb²). L'écart de teinte
     est donc un PLANCHER pour le ΔE, quelle que soit la lumière que le peintre met sur l'île — et cette
     lumière, on ne la connaît pas au moment où la dalle est rendue. On vise plus haut que le plancher
     (`DE_VISE`) parce que la fourrure moyenne et, en clair, la peau désature : la marge est mesurée, pas
     devinée (voir `sauvegardes/ch59/`).
     ⚠ CE N'EST QUE SUR LA SPHÈRE. La moisson (« Ce que tu as tenu ») garde la dalle telle quelle : elle
     n'est posée sur aucun sol de nature, donc elle n'a rien à céder. */
  /* ⚑ LE PLANCHER DU MASQUE N'EST PAS CELUI DE L'ÉCRAN — ET EN CLAIR IL N'EST PAS ATTEIGNABLE.
     Le juge mesure à l'écran, après le peintre. Entre le masque et l'écran, le rapport a une médiane de
     0,96 dans les deux thèmes (30 couples chacun) mais il descend à 0,20 en sombre et 0,36 en clair : c'est
     la lumière que le peintre met à l'endroit de l'île. En SOMBRE, le plancher du juge suffit — mesuré,
     0 dalle sous le plancher sur 18 chargements, contre 7 sur 8 avant.
     En CLAIR il faudrait viser 15 / 0,36 ≈ 42, et LA PALETTE D'UN MONDE NE LE PERMET PAS : ses quatre
     couleurs sont lilas, bleu, terracotta, pervenche — trois d'entre elles sont de la famille du sol
     (bleu-violet), et la seule assez loin est le TERRACOTTA, que le §3 interdit sur une dalle (c'est « à
     tenir », et la légende de l'écran est juste dessous). Essayé avec un plancher à 42 : la boucle tourne
     ses quatre tours à chaque ouverture, les cinq îles cèdent, et rien ne converge (masques 9,6 à 29,4).
     On garde donc LE PLANCHER DU JUGE, et le reste est déclaré : c'est le lavage de la peau pâle, la
     question ouverte Q182 — pas le tirage de la couleur.
     ⚑ ET LA TEINTE NE CÈDE QU'EN SOMBRE. Mesuré : en clair, faire céder la teinte au plancher du juge fait
     passer le compte de 4 chargements fautifs sur 8 (sans rien faire) à 6 sur 8. Ce n'est pas un hasard :
     le rapport masque→écran y va de ×0,18 à ×6,97 — l'instrument n'y prédit rien, donc il ne peut pas
     piloter une correction. Un instrument dont on a MESURÉ qu'il mentait ne décide de rien (CLAUDE §8 :
     « avant d'accuser le dessin, on vérifie l'instrument »). En clair, on ne touche donc à aucune dalle,
     et le défaut reste ouvert, nommé, avec son chiffre. */
  var DE_PLANCHER=15, DE_VISE=32, DE_ESSAIS=3;
  /* ⚑ 14 sept. (résidu du sombre) : le masque décide, et l'écran peut en rendre ×0,48 — une dalle à 28 sur le masque sortait à
     13,7 à l'écran. La cession se déclenche donc sous 15 / 0,48 ≈ 31 sur le masque, et vise 32. Le juge garde SON plancher, 15. */
  var DE_DECLENCHE=31;
  function plancher(){ return DE_DECLENCHE; }
  function _lin(v){ v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4); }
  function _fl(t){ return t>0.008856?Math.pow(t,1/3):7.787*t+16/116; }
  function _lab(r,g,b){ r=_lin(r); g=_lin(g); b=_lin(b);
    var X=(0.4124*r+0.3576*g+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g+0.0722*b, Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883;
    var fx=_fl(X), fy=_fl(Y), fz=_fl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; }
  function _fi(t){ var t3=t*t*t; return t3>0.008856?t3:(t-16/116)/7.787; }
  function _o255(v){ v=v<=0.0031308?12.92*v:1.055*Math.pow(Math.max(0,v),1/2.4)-0.055;
    return v<0?0:(v>1?255:Math.round(v*255)); }
  function _rgb(L,a,b){ var fy=(L+16)/116, fx=fy+a/500, fz=fy-b/200;
    var X=_fi(fx)*0.95047, Y=_fi(fy), Z=_fi(fz)*1.08883;
    return [_o255(3.2406*X-1.5372*Y-0.4986*Z), _o255(-0.9689*X+1.8758*Y+0.0415*Z), _o255(0.0557*X-0.2040*Y+1.0570*Z)]; }
  /* ⚑ LE SOL EST MESURÉ SUR LA SPHÈRE, PAS DÉDUIT DU DOCUMENT (12 sept.). Première écriture : la teinte
     claire du §1.2 (`NAT_CLAIR`) mélangée au crème par `K.PEAU_CREME`, soit ~[228,211,237]. FAUX — mesuré
     sur la sphère SANS ses îles, à la vue du juge (`sauvegardes/ch59/`, sonde `sol_reel.py`) :
        sombre  [67, 86, 211]   (la nature [130,174,248], que la fourrure assombrit un peu)
        clair   [133, 141, 243] (la NATURE éclaircie vers le crème, PAS la teinte claire du §1.2)
     Le facteur du clair se lit dans la mesure, canal par canal : 0,403 · 0,370 · 0,400 → `SOL_CREME`.
     Conséquence du modèle faux : en clair le garde-fou ne se déclenchait JAMAIS (0 dalle cédée sur 8
     chargements) et 6 dalles restaient sous le plancher.
     ⚑ REMESURÉ APRÈS Q210 (le poil du clair s'assombrit, la peau va au crème) : sol clair **[100, 106, 156]**
     — soit `solEffectif()` tiré vers le crème par 0,351 · 0,359 · 0,461, toujours ≈ 0,39. Le modèle ne change
     donc que de POINT DE DÉPART : il part du poil effectif, pas de la nature pleine. */
  /* ⚑ Q210 · LE SOL DU CLAIR S'ASSOMBRIT, LA PEAU VA AU CRÈME (Tom, 12 sept. : « si aucune couleur de la
     palette n'est assez loin du sol pâle, c'est le sol qu'il faut changer, pas les dalles qu'il faut
     tordre »). C'est l'inversion annoncée en Q182 — sol clair, poil sombre — posée EN DEGRÉ, et le degré
     est mesuré : `sauvegardes/q210/balaye_sol.py`, 5 pages, 25 îles, la métrique du juge.
        poil            boule↔page (décidé 85±8)   îles sous le plancher ΔE 15
        ×1,00 (livré)          84,4 ✓                    5 / 25   (la plus faible 5,0)
        ×0,80 + crème          89,8 ✓                    4 / 25   (8,2)   ← ne règle rien
        ×0,50 + crème         110,8 ✗                    1 / 25   (12,4)
        ×0,44 + crème         113,5 ✗                    0 / 25   (15,8)  ← marge trop mince
        ×0,38 + crème         116,3 ✗                    0 / 25   (18,1)  ← RETENU
        ×0,32 + crème         119,0 ✗                    0 / 25   (20,5)
     On prend LE PLUS FAIBLE assombrissement qui tienne avec une vraie marge : à ×0,38 la plus faible île
     du clair est à 18,1, soit la marge du SOMBRE (16 à 20 sur le même instrument) — c'est exactement le
     critère relatif que le juge porte (« les dalles du clair pas moins lisibles qu'en sombre »).
     ⚠ CE QUE ÇA COÛTE, ET QUI EST LA DÉCISION DE TOM : l'écart boule ↔ page passe de 84 à 116. La valeur
     85 était celle de A2 — la version que cette décision REMPLACE — et le juge la porte en dur : elle est
     donc recentrée sur la nouvelle décision (§7, « un contrôle qui encode une règle abandonnée se met à
     jour au niveau de la décision »), tolérance ±8 inchangée, contour ≥ 42 inchangé, plancher 15 inchangé.
     Aucun seuil n'est desserré : une cote à deux bords est recentrée, deux planchers tiennent mieux qu'avant.
     ⚠ Le poil garde SA TEINTE : c'est une multiplication, pas un mélange vers l'encre — la nature reste
     lisible dans la couleur (§3, le champ porte sa nature). */
  var SOL_CLAIR=0.38;
  /* ⚑ 20 SEPTEMBRE 2026 (Tom) — LE SOL PREND LA PALETTE DU STUDIO.
     « La sphère rejoint ce qui suit la palette du Studio, avec les dalles de la Toile et la
       Toile de l'écran du Cercle. Son sol prend la palette. »
     ON PREND LE TON DOMINANT, C1 — ≈ 34 % de la Toile, celui qu'on y voit le plus : c'est
     par lui que la sphère « rejoint ». `Toile.cols()` rend la palette DÉJÀ décalée par la
     jauge de teinte, donc le sol suit aussi le geste de couleur du Studio.

     ⚠ ET VOICI LA FRONTIÈRE, QU'ON NE FRANCHIT PAS :
       · LE SOL suit le Studio — c'est une SURFACE, comme la Toile.
       · LES ÎLES ne le suivent pas : ce sont les dalles tenues, peintes dans LEUR monde et
         LEUR couleur de plantation (§4 — « une dalle est figée à sa création », partout où
         elle paraît : sur la sphère comme sous « Ce que tu as tenu »).
       · LA LÉGENDE, LES ARCS DES NOYAUX ET LES TRAITS D'ÉTAT ne le suivent JAMAIS. Ce sont
         des ÉTATS : le vert n'est « tenu » que parce qu'il est TOUJOURS vert. Un état qui
         changerait avec le Studio cesserait d'être un signal.

     ⚠ `natureMaj` ne colore plus rien — elle ne servait qu'ici. On la GARDE : elle est
     publiée dans `D.nature`, et rien ne s'invente en la supprimant (§9). */
  /* ⚑ 23 SEPTEMBRE 2026, second tour (Tom) — « LA PELOTE SUIT LA PALETTE DU STUDIO — BIEN.
     MAIS ELLE DOIT TIRER AU HASARD PARMI LES QUATRE TONS DE CETTE PALETTE, ET CHANGER À CHAQUE
     OUVERTURE DE L'AURA, COMME LA TOILE DE L'ÉCRAN DU CERCLE. »
     Le sol prenait C1, le ton dominant, et lui seul. Il prend maintenant l'un des QUATRE, tiré
     à l'ouverture. Ce n'est pas la règle des dalles (§4 : une dalle est figée à sa plantation) —
     le sol n'est pas une dalle, c'est une SURFACE, et les surfaces suivent le Studio (§3, la
     frontière Studio / état). Le garde-fou du §3 (écart ≥ 42 à la page) s'applique au ton tiré
     comme il s'appliquait au dominant : il est en aval, dans `ecarteDeLaPage`. */
  var SOL_IDX = 0;
  function solPalette(){
    try{ var c=window.Toile.cols();
      if(c && c.length){ var t=c[Math.max(0,Math.min(SOL_IDX, c.length-1))] || c[0];
        if(t) return [t[0]|0, t[1]|0, t[2]|0]; } }catch(e){}
    return NAT.promi;   /* avant que le moteur soit là */
  }
  /* ⚠ UN TIRAGE INVALIDE LES DEUX CACHES : le semis (le poil porte la couleur du sol) et les
     îles (le sol entre dans leur clé). Sans ça la Pelote garde l'ancienne couleur à l'écran. */
  function nouveauSol(){
    var n=4; try{ var c=window.Toile.cols(); if(c&&c.length) n=c.length; }catch(_){}
    SOL_IDX = (Math.random()*n)|0;
    try{ var S2=semis(); if(S2) S2.__stCle=null; }catch(_){}
    PEL.iles=null; PEL.cleI='';
    return SOL_IDX;
  }
  /* ⚑ 21 SEPTEMBRE 2026 (Tom) — LE GARDE-FOU. « Si le sol ne se détache pas assez de la
     page, il se décale jusqu'à passer le seuil. »
     LE DÉFAUT, MESURÉ AVANT : depuis que le sol suit la palette, l'écart boule ↔ page va de
     10,4 (Taciturne) à 156,2 (Primesautier) en mode sombre — sous les deux palettes les plus
     sombres la boule se fond dans la page.
     LE SEUIL EST CELUI DU §3 : 42. Ce n'est pas un nombre neuf — c'est déjà le plancher que
     le juge de l'Aura porte pour le contour du limbe (`CONTOUR_MIN`).
     LE DÉCALAGE GARDE LA TEINTE : on mélange vers le blanc ou vers le noir, jamais vers une
     autre couleur — la palette reste reconnaissable, elle s'éclaircit ou s'assombrit.
     ON S'ÉLOIGNE DU CÔTÉ OÙ L'ON EST DÉJÀ ; et si ce côté ne peut pas y arriver (un sol
     presque noir sur une page noire), on passe de l'autre. */
  /* LE SEUIL EST 42 (§3) — MAIS ON VISE 44, ET LA MARGE EST MESURÉE. Le garde-fou agit sur la
     COULEUR du sol ; ce qu'on voit est le RENDU, que la fourrure assombrit un peu. Balayé sur
     les 21 palettes, il en coûte jusqu'à 0,7 de luminosité (Taciturne, mode sombre : visé 42,
     rendu 41,3). On vise donc 44 pour que LE RENDU tienne 42 — même méthode que SOL_CLAIR et
     SOL_CREME de Q210, dont le degré se lit dans la mesure et pas dans le document. */
  var ECART_PAGE=44;
  function _lum(c){ return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
  function pageCouleur(){ return clair() ? [0xF7,0xF0,0xDE] : [0x10,0x0D,0x0B]; }
  function versBlanc(c,t){ return [c[0]+(255-c[0])*t, c[1]+(255-c[1])*t, c[2]+(255-c[2])*t]; }
  function versNoir(c,t){ return [c[0]*(1-t), c[1]*(1-t), c[2]*(1-t)]; }
  function ecarteDeLaPage(s){
    var p=_lum(pageCouleur()), l=_lum(s);
    if(Math.abs(l-p)>=ECART_PAGE) return s;
    var haut=p+ECART_PAGE, bas=p-ECART_PAGE;
    var peutHaut=(haut<=255), peutBas=(bas>=0);
    var versLeHaut = (l>=p) ? peutHaut : !peutBas;   /* on s'éloigne du côté où l'on est déjà */
    var r;
    if(versLeHaut && peutHaut){ var t=(haut-l)/(255-l||1); r=versBlanc(s,Math.max(0,Math.min(1,t))); }
    else if(peutBas){ var u=1-(bas/(l||1)); r=versNoir(s,Math.max(0,Math.min(1,u))); }
    else return s;
    return [Math.round(r[0]),Math.round(r[1]),Math.round(r[2])];
  }
  function solEffectif(){
    var p=solPalette(), s=p;
    if(clair()){
      s=[Math.round(p[0]*SOL_CLAIR), Math.round(p[1]*SOL_CLAIR), Math.round(p[2]*SOL_CLAIR)];
      /* ⚑ 22 sept. — ET ON RESSATURE. C'est le POIL qui fait la couleur de la sphère, pas la
         peau : sans ceci, la chroma du sol tombait de 41,6 à 6,4 et la sphère sortait grise
         quelle que soit la palette (Tom : « elle n'est pas aux couleurs de la palette »). On
         garde la CLARTÉ de Q210 — c'est elle qui rend les îles lisibles — et on rend la
         couleur, comme le fait déjà la rampe de velours. */
      s=ressature(s, p);
    }
    return ecarteDeLaPage(s);
  }
  var SOL_CREME=0.39;
  /* les deux couleurs d'état qu'une dalle ne portera jamais (§3) — menthe « tenu », terracotta « à tenir » */
  var ETAT_MENTHE=null, ETAT_TERRA=null;
  function _prochede(t, e){ if(!e) return false;
    return Math.sqrt((t[0]-e[0])*(t[0]-e[0])+(t[1]-e[1])*(t[1]-e[1])+(t[2]-e[2])*(t[2]-e[2]))<24; }
  /* ⚑ 22 SEPTEMBRE 2026 (Tom) — « LA SPHÈRE N'EST PAS AUX COULEURS DE LA PALETTE ».
     Elle l'était pourtant : `solEffectif()` prend bien le ton dominant. CE QUI LA DÉCOLORAIT,
     mesuré pas à pas sur le bleu #82AEF8 (C1 de la palette d'identité) :
         le ton dominant        C* 41,6
         × SOL_CLAIR 0,38       C* 18,8
         + 39 % vers le crème   C*  6,4     ← la teinte survit, la COULEUR non
     Les deux transformations sont celles de Q210, et elles servent à quelque chose : la
     CLARTÉ qu'elles donnent est ce qui rend les îles lisibles en mode clair. On garde donc
     la clarté, et ON RESSATURE — c'est exactement ce que fait déjà la rampe de velours
     (« on monte la clarté de moitié moins, et on RESSATURE »). La cible est 0,72 × la chroma
     du ton dominant : un SOL, pas une affiche. */
  function _lchDe(c){
    var L=_lab(c[0],c[1],c[2]); return [L[0], Math.sqrt(L[1]*L[1]+L[2]*L[2]), Math.atan2(L[2],L[1])];
  }
  function _deLch(L,C,h){ return _rgb(L, C*Math.cos(h), C*Math.sin(h)); }
  var SOL_SAT=0.72;
  function ressature(s, ref){
    try{
      var a=_lchDe(s), b=_lchDe(ref), cible=b[1]*SOL_SAT;
      if(!(cible>a[1])) return s;
      var out=_deLch(a[0], cible, a[2]);
      /* le gamut peut mordre : on redescend jusqu'à ce que l'aller-retour tienne */
      for(var k=0;k<6;k++){ var v=_lchDe(out); if(Math.abs(v[1]-cible)<2 && Math.abs(v[0]-a[0])<2) break;
        cible*=0.88; out=_deLch(a[0], cible, a[2]); }
      return out;
    }catch(e){ return s; }
  }
  function fondSphere(){
    var s=PEL.solR || solEffectif();
    if(clair()){
      var m=[s[0]+(CREME[0]-s[0])*SOL_CREME, s[1]+(CREME[1]-s[1])*SOL_CREME, s[2]+(CREME[2]-s[2])*SOL_CREME];
      return m;   /* la ressaturation est faite en amont, dans solEffectif */
    }
    return s;
  }
  /* ⚑ v7 — c'étaient encore #2BE88C et #F07A2E, la palette d'AVANT le 16 sept. (§8, les triplets). */
  ETAT_MENTHE=_lab(0x8F,0xE0,0x8F); ETAT_TERRA=_lab(0xDD,0x4D,0x23);
  var LISIBLES={};
  /* ⚑ LE GARDE-FOU NE PEUT PAS SE LIRE SUR LA DALLE SEULE — MESURÉ, ET C'EST LA LEÇON DE CE CHANTIER.
     Deux critères essayés sur la dalle rendue, avant le peintre, et tous deux jetés sur la mesure :
       ① l'écart de couleur (ΔE) entre la dalle et le sol : le rapport entre cet écart et celui qu'on
          MESURE À L'ÉCRAN va de ×0,06 à ×13 (30 couples par thème, `sauvegardes/ch59/mesure_plancher.py`).
          Une dalle à 48,8 du sol sort à 5,0 à l'écran ; une autre à 23,8 sort à 26,4. Il ne prédit rien.
       ② la part PLEINE de la dalle (le vide se peint en sol) : le tiers le moins lisible remplit 65 %,
          le tiers le plus lisible 68 %. Aucune corrélation.
     CE QUI MANQUAIT : dans `batIles`, chaque pixel de dalle transparent garde l'indice 0 du masque — et
     l'indice 0 EST LE SOL (`if(o.sol){ TCOL[0]=o.sol; }` dans le peintre). Une île est donc un MÉLANGE de
     la dalle et du sol, dans la proportion que son masque décide. On mesure donc la lisibilité LÀ OÙ LE
     PEINTRE LA FABRIQUE : sur le masque, sol compris (`lisibiliteIle`), après `batIles` — et on fait céder
     la teinte des seules îles qui restent sous le plancher, en reconstruisant. C'est la règle du §8 :
     l'état est ce que le code produit, jamais ce qu'on en déduit. */
  function dalleLisible(p){
    var src=dalleDe(p); if(!src) return null;
    /* ⚑ v18 · Q297 (Tom) : « une île bleue sur un sol bleu doit rester lisible ». Sous Ingénu, la couleur d'une
       île DIT SA NATURE : la faire céder vers une autre couleur de la palette mentirait (mesuré : un Promi
       sortait kaki). Le recalage de sa clarté sur la rampe de SA nature remplace donc la cession. Sur une COPIE :
       le cache des dalles sert aussi « Ce que tu as tenu », posé sur la page, qui n'a rien à céder. */
    if(window._ingenuTeinte && (((p.monde||{}).p)||'signal')==='signal'){
      /* LA HAUTEUR DE RAMPE SE CHOISIT CONTRE LE SOL RÉELLEMENT TIRÉ (le sol de la Pelote l'est au hasard, décision
         Tom) : parmi quelques hauteurs, celle dont l'île s'écarte le plus du sol, en ΔE, sur le masque. Même idée
         que le chantier 59 — mais sur l'axe de la CLARTÉ de sa nature, jamais vers une autre couleur. */
      var _F=fondSphere(), _ki=cleMonde(p)+'|ingenu|'+[_F[0]|0,_F[1]|0,_F[2]|0].join(','); if(LISIBLES[_ki]) return LISIBLES[_ki];
      var _SO=_lab(_F[0],_F[1],_F[2]), _best=null, _bd=-1;
      /* ⚠ EN CLAIR, LE MASQUE NE PRÉDIT PAS L'ÉCRAN (mesuré au chantier 59 : ×0,06 à ×13) : la peau pâle y lave
         l'île et le sol y est assombri. On y garde une hauteur FIXE, mesurée à l'écran par releve-aura : 1,8. */
      /* en sombre : la hauteur la plus PROCHE de la couleur de nature qui atteint la visée du chantier 59 (DE_VISE,
         sur le masque) — pas l'écart maximal : le clair doit rester aussi lisible que le sombre (Tom, 10 sept.) */
      var _vu=false;
      /* ⚑ v29 — chaque hauteur est PEINTE PAR LE MOTEUR (`opts.rampe`), qui déclare aussi son Lab moyen
         (même échantillonnage, un pixel sur quatre) : plus aucune copie retouchée ni relue ici. */
      (clair() ? [1.8] : [1.1,0.85,1.4,0.65,1.8,0.45,2.3]).forEach(function(h){ if(_vu) return;
        var c=document.createElement('canvas'), _rp=window._ingenuRampe?window._ingenuRampe(p.id, h, true):null;   /* v34 : la Pelote garde sa plantation */
        try{ if(!_rp || !window.Toile.dalleTrame(c, p.id, 1, p.monde||undefined, {rampe:_rp, donnees:true}) || !c.__dalleInfo || !c.__dalleInfo.lab) return;
          var _lb=c.__dalleInfo.lab;
          var de=Math.sqrt(Math.pow(_lb[0]-_SO[0],2)+Math.pow(_lb[1]-_SO[1],2)+Math.pow(_lb[2]-_SO[2],2));
          if(de>_bd){ _bd=de; _best=c; } if(de>=DE_VISE){ _bd=de; _best=c; _vu=true; } }catch(_){ } });
      if(!_best) return src;
      try{ PEL.ingenu=PEL.ingenu||{}; PEL.ingenu[p.title||p.id]=Math.round(_bd*10)/10; }catch(_){ }
      return (LISIBLES[_ki]=_best);
    }
    var F=fondSphere(), rang=(CEDE[cleMonde(p)]||0);
    var cle=cleMonde(p)+'|'+[F[0]|0,F[1]|0,F[2]|0].join(',')+'|'+rang;
    if(LISIBLES[cle]!==undefined) return LISIBLES[cle];
    if(!rang) return (LISIBLES[cle]=src);
    PEL.ch59=PEL.ch59||{};
    /* ⚑ v29 — ce que la dalle remplit et son Lab moyen, DÉCLARÉS par le moteur (`__dalleInfo`) : plus relus ici */
    var _In=src.__dalleInfo; if(!_In || !_In.lab || !(_In.plein>0)) return (LISIBLES[cle]=src);
    var n=1, i;
    /* ⚑ CE QUE LA DALLE REMPLIT VRAIMENT. Dans `batIles`, un pixel de dalle TRANSPARENT garde l'indice 0
       du masque — donc il se peint EN SOL. Une dalle clairsemée donne donc une île faite surtout de sol,
       illisible quelle que soit sa couleur. On le mesure avant de croire que la teinte est la cause. */
    var plein=_In.plein;
    var mL=_In.lab[0], ma=_In.lab[1], mb=_In.lab[2], SO=_lab(F[0],F[1],F[2]);
    /* les couleurs DE SA PALETTE, rangées par écart de teinte au sol : le rang dit laquelle on prend.
       Jamais une couleur inventée (§9) — c'est le monde du Studio qui les fournit. */
    var PAL=[]; try{ PAL=window.Toile.cols()||[]; }catch(_){ }
    var CH=[];
    for(i=0;i<PAL.length;i++){
      var c=PAL[i]; if(!c) continue;
      var rr=c[0], gg=c[1], bb=c[2];
      if(typeof c==='string'){ var m=c.match(/\d+/g); if(m){ rr=+m[0]; gg=+m[1]; bb=+m[2]; }
        else { var h=c.replace('#',''); if(h.length===3) h=h.charAt(0)+h.charAt(0)+h.charAt(1)+h.charAt(1)+h.charAt(2)+h.charAt(2);
               rr=parseInt(h.substr(0,2),16); gg=parseInt(h.substr(2,2),16); bb=parseInt(h.substr(4,2),16); } }
      var t=_lab(rr,gg,bb);
      /* ⚑ NI MENTHE NI TERRACOTTA. Vu à la capture (`sauvegardes/ch59/apres_dark.png`, première version) :
         la couleur la plus éloignée du sol bleu EST le terracotta de la palette — trois îles sur cinq y
         passaient, et la légende « ● à tenir » est juste dessous, dans la même couleur. La sphère se mettait
         à parler le langage des ÉTATS (§3 : les couleurs d'état ne servent qu'aux états). Tom a déjà tranché
         ce choix pour l'accent de l'écran qui vend : « exclus menthe et terracotta, prends la plus saturée
         des autres ». On l'applique ici : un état ne se dit jamais par une dalle. */
      if(_prochede(t, ETAT_MENTHE) || _prochede(t, ETAT_TERRA)) continue;
      CH.push({a:t[1], b:t[2], d:Math.sqrt((t[1]-SO[1])*(t[1]-SO[1])+(t[2]-SO[2])*(t[2]-SO[2]))});
    }
    if(!CH.length){ PEL.ch59[p.id]={titre:p.title, cede:false, sansPalette:true}; return (LISIBLES[cle]=src); }
    CH.sort(function(x,y){ return y.d-x.d; });
    var ch=CH[(rang-1)%CH.length], ca=ch.a, cb=ch.b;
    /* la palette ne porte peut-être pas d'écart suffisant : on pousse la teinte SUR SA PROPRE DIRECTION,
       jamais sur une couleur inventée — c'est la même teinte, plus franche. */
    var vx=ca-SO[1], vy=cb-SO[2], vm=Math.sqrt(vx*vx+vy*vy)||1;
    if(vm<DE_VISE){ ca=SO[1]+vx/vm*DE_VISE; cb=SO[2]+vy/vm*DE_VISE; vm=DE_VISE; }
    /* le remappage : chaque pixel garde sa CLARTÉ et son écart de teinte au centre du nuage —
       ⚑ v29 : PEINT PAR LE MOTEUR (`opts.decale`, la même formule), plus aucun pixel reposé ici */
    var out=document.createElement('canvas');
    try{ if(!window.Toile.dalleTrame(out, p.id, 1, p.monde||undefined, {decale:{a:ca, b:cb}, donnees:true})) return (LISIBLES[cle]=src); }
    catch(_){ return (LISIBLES[cle]=src); }
    PEL.ch59[p.id]={titre:p.title, plein:+plein.toFixed(3), cede:true, rang:rang,
                    vers:[+ca.toFixed(1),+cb.toFixed(1)], apres:+vm.toFixed(1)};
    return (LISIBLES[cle]=out);
  }

  /* ⚑ LA LISIBILITÉ D'UNE ÎLE, LÀ OÙ LE PEINTRE LA FABRIQUE. Le masque d'une île donne, pixel par pixel,
     l'indice de sa couleur dans la table de `batIles` — et l'indice 0 est LE SOL. La couleur moyenne d'une
     île est donc le mélange de sa dalle et du sol dans la proportion de son masque, et c'est CE mélange
     que le juge mesure à l'écran (ΔE des couleurs moyennes, avec l'île et sans elle). */
  function lisibiliteIle(R, k){
    var I=R.iles[k]; if(!I||!I.m) return null;
    var C=R.col||[], F=fondSphere(), n=0, sL=0, sa=0, sb=0, q, idx, c, l;
    for(q=0;q<I.m.length;q++){
      idx=I.m[q]; c=(idx===0)?F:C[idx]; if(!c) continue;
      l=_lab(c[0],c[1],c[2]); n++; sL+=l[0]; sa+=l[1]; sb+=l[2];
    }
    if(!n) return null;
    var S=_lab(F[0],F[1],F[2]);
    return {dE:Math.sqrt((sL/n-S[0])*(sL/n-S[0])+(sa/n-S[1])*(sa/n-S[1])+(sb/n-S[2])*(sb/n-S[2])),
            sol:0};
  }

  /* ════════════════════════════════════════════════════════════════════════════
     L'ÉCRAN — bâti une fois, rempli à chaque ouverture
     ════════════════════════════════════════════════════════════════════════════ */
  var CAD, BO, CV, PRISE, MOT, INV, NX, LG, CPT, MO, GR, BT, D=null, FIN;
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
    eta().forEach(function(e){ var s=el('span'), i=el('i'); i.style.background=e[1];
      s.appendChild(i); s.appendChild(document.createTextNode(e[0])); LG.appendChild(s); });
    CAD.appendChild(LG);
    /* ⚑ v95 (Tom, 28 sept. : « Le compteur quitte l'accueil et va dans l'Aura, sous la légende, en PromiLate. Trois chiffres seulement,
       alignés sur les trois couleurs de la légende : tenues, en cours, à tenir. Rien d'autre ») — chaque chiffre est centré sous SON
       entrée de légende ; la colonne le range dans `place()`, l'air suit (rien n'est à une cote figée) */
    CPT=el('div','au-cpt'); eta().forEach(function(){ CPT.appendChild(el('span')); }); CAD.appendChild(CPT);
    MO=el('div','au-mo'); MO.appendChild(el('h3',null,'Ce que tu as tenu'));
    GR=el('div','au-gr'); MO.appendChild(GR); CAD.appendChild(MO);
    /* ⚑ CE QU'ON T'A TENU (Q215) — le miroir de « Ce que tu as tenu ». En gratuit : visible, flouté à 2,4 px, l'encart net
       posé dessus. On voit qu'il existe une autre moitié, jamais ce qu'elle contient. */
    MO2=el('div','au-mo2'); MO2.appendChild(el('h3',null,'Ce qu’on t’a tenu'));
    var z2=el('div','au-zone2'); GR2=el('div','au-gr2'); z2.appendChild(GR2);
    ENC2=el('div','au-enc2'); ENC2.setAttribute('role','button'); ENC2.appendChild(el('span',null,'✦ Ma Parole !'));
    ENC2.addEventListener('click', function(ev){ ev.stopPropagation(); try{ var pl=document.getElementById('plusScreen'); if(pl) pl.classList.add('show'); }catch(_){} });
    z2.appendChild(ENC2); MO2.appendChild(z2); CAD.appendChild(MO2);
    BT=el('div','au-bt','Partager ma Pelote'); BT.id='auPartage'; BT.setAttribute('role','button');
    /* la même porte que l'ancien #sealShare : le partage, en mode Noyau */
    BT.onclick=function(){ try{
      /* ⚑ 22 SEPTEMBRE 2026 (Tom) — « Partager mon Noyau ne fait rien ». Mesuré : la page
         Partager S'OUVRAIT BIEN (`shareShow: true`, mode « Le Noyau » sélectionné) — mais
         `#auraScreen` NE PERD JAMAIS sa classe `show` (c'est le même défaut que le régulateur
         de densité du 20 septembre, §8). L'Aura restait donc par-dessus, et à l'écran il ne se
         passait rien. On la ferme avant d'ouvrir — son observateur fait le reste. */
      SC.classList.remove('show');
      if(typeof openShare==='function') openShare();
      var nb=document.querySelector('#shMode button[data-mode=pelote]');
      if(nb) nb.click();
      [60,240,600].forEach(function(d){ setTimeout(function(){
        try{ var s=document.getElementById('shareScreen');
             if(s && !s.classList.contains('show')) s.classList.add('show');
             var n2=document.querySelector('#shMode button[data-mode=pelote]');
             if(n2 && !n2.classList.contains('on')) n2.click(); }catch(_){}
      }, d); });
    }catch(e){} };
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
  function noyau(dia, ep, dph, pa, nom, moi, recu){
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
    /* ⚑ LES DEUX MOITIÉS (Tom, 14 sept. 2026 — le §2.9 corrigé) : à GAUCHE ce que tu tiens envers la personne, à DROITE ce
       qu'elle te tient. La grammaire du trait : ta moitié à gauche, celle de l'autre à droite. Les deux partent de midi, en
       miroir, séparées par un JOUR de 6 px en haut et en bas. Une moitié absente ne se peint pas — ni piste, ni vide.
       Mesuré : « seulement lui → moi » ne se superpose jamais à « seulement moi → lui » (IoU 0,01). */
    /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « LES ESPACES ENTRE LES SEGMENTS SONT INÉGAUX ET IRRÉGULIERS.
       UNIFORMISÉ PARTOUT, NET, ESPACE LOGIQUE PARFAIT ENTRE TOUS, SANS FIORITURE. »
       Deux défauts, et ils se cumulaient :
         ① le jour valait 0,8 % DU TOUR, donc un ANGLE : sur « Toi » (Ø 78) il faisait 1,0 px
            d'arc, sur une personne (Ø 58) 0,76. Un même écart demandé sort donc inégal d'un
            disque à l'autre. Il est maintenant donné EN PIXELS D'ARC et converti par anneau :
            le même trou se voit partout, quel que soit le diamètre.
         ② l'anneau commençait à `g` et finissait à `360 − g`, un reliquat des deux moitiés du
            14 septembre : le jour du HAUT valait 2g + le jour du dernier arc, les autres le
            jour seul. Il n'y a plus d'ouverture de midi — n arcs, n jours identiques, et le
            jour est CENTRÉ sur midi pour que la coupure tombe à un endroit qui se comprend. */
    var JOUR_PX=3, g=0, TOT=180, GA=0;
    function pt(a){ var t=(a-90)*Math.PI/180; return (cx+r*Math.cos(t)).toFixed(2)+' '+(cx+r*Math.sin(t)).toFixed(2); }
    function seg(par, a0, a1, col, cls){ if(a1-a0<=0.3) return; var e=svg('path');
      e.setAttribute('d','M'+pt(a0)+' A'+r+' '+r+' 0 '+((a1-a0)>180?1:0)+' 1 '+pt(a1)); e.setAttribute('fill','none');
      e.setAttribute('stroke',col); e.setAttribute('stroke-width',ep); e.setAttribute('stroke-linecap','butt'); e.setAttribute('class',cls); par.appendChild(e); return e; }
    function somme(x){ return x ? (x[0]+x[1]+x[2]) : 0; }
    function anneau(par, parts){
      var n=[0,1,2].filter(function(z){ return parts[z]>0; }).length;
      /* ⚑ 22 sept. (Tom) : « les écarts entre les segments doivent être beaucoup plus courts ».
         2,6 % du tour → 0,8 % : l'anneau se lit comme un anneau, pas comme trois tirets. */
      /* ⚠ ET UN SEUL ÉTAT NE PEUT PAS FAIRE 360° PILE : un arc SVG dont le départ et l'arrivée
         sont le MÊME point ne dessine RIEN. Le jour d'avant valait 2g, il cachait le cas ;
         Nico, qui n'a qu'un état, sortait sans anneau. On laisse un dixième de degré. */
      var TOUR=360, GJ=(n>1?JOUR_PX/r*180/Math.PI:0.1), a=GJ/2;
      for(var z=0; z<3; z++){ var v=parts[z]; if(v<=0) continue;
        var e=seg(par, a, a+v*TOUR-GJ, eta()[z][1], 'au-arc');
        if(e){ try{ e.setAttribute('data-z',z); }catch(_){} }
        a+=v*TOUR; }
    }
    function moitie(par, parts, cote){
      var n=[0,1,2].filter(function(z){ return parts[z]>0; }).length, a=(cote==='d') ? g : 360-g;
      for(var z=0; z<3; z++){ var v=parts[z]; if(v<=0) continue; var L=v*TOT-(n>1?GA:0);
        if(cote==='d'){ var _s1=seg(par, a, a+L, eta()[z][1], 'au-arc'); try{_s1.setAttribute('data-z',z);}catch(_){} a+=v*TOT; } else { var _s2=seg(par, a-L, a, eta()[z][1], 'au-arc'); try{_s2.setAttribute('data-z',z);}catch(_){} a-=v*TOT; } }
    }
    /* ⚑ 22 sept. — UN SEUL ANNEAU, TROIS ARCS AU PLUS. Les deux moitiés du 14 septembre
       donnaient jusqu'à six segments (voir `gensRecip`). Le tour entier, trois états, un jour
       entre deux arcs voisins — et plus aucun voile d'opacité : les couleurs rendues sont
       EXACTEMENT les trois valeurs décidées. */
    if(somme(pa)>0) anneau(s, pa);
    if(recu && somme(recu)>0) w.setAttribute('data-recu','1');
    box.appendChild(s);
    var f=visage(dph, nom, moi); f.style.left=f.style.top=((dia-dph)/2)+'px'; box.appendChild(f);
    w.appendChild(box);
    w.appendChild(el('div','au-lb', moi?'Toi':nom));   /* ⚑ 22 sept. (Tom) : « toi » prend une majuscule */
    return w;
  }
  var MO2=null, GR2=null, ENC2=null;
  /* le voile suit le Cercle : une classe que le code pose (§8), comparée avant d'écrire */
  function voile(){ if(!CAD) return; var dv=document.getElementById('device'); var v=!(dv && dv.classList.contains('premium'));
    if(CAD.classList.contains('au-voile')!==v) CAD.classList.toggle('au-voile', v); }
  try{ var _dv=document.getElementById('device'); if(_dv) new MutationObserver(voile).observe(_dv,{attributes:true,attributeFilter:['class']}); }catch(_){}
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
    [].forEach.call(CAD.querySelectorAll('.au-gr canvas[data-pid], .au-gr2 canvas[data-pid]'), function(cv){
      if(cv.__ok) return;
      /* ⚑ v29 — rendue à la taille de SA boîte et affichée à cette taille exacte : ni agrandie par le CSS, ni réduite
         (redteam_decoupe, famille G) */
      var p=parId(+cv.getAttribute('data-pid')), bx=cv.parentNode; if(!p||!bx) return;
      var dpr=Math.min(2,window.devicePixelRatio||1), bw=bx.clientWidth||64, bh=bx.clientHeight||64;
      var s=window._rendDalle?window._rendDalle(p.id, bw*dpr, bh*dpr, {monde:p.monde||undefined}):null; if(!s) return;
      /* ⚑ v32 — EN LIGNE AVEC `important` : la règle `.au-bx canvas{width:auto!important;height:auto!important;max-height:64px}`
         écrasait ces deux cotes, et une dalle rendue un peu SOUS sa boîte (la seconde passe de `_rendDalle` accepte 5 %)
         était étirée par le plafond — 3 % mesuré sur les mondes neufs, 4,9 % possibles sur Encre (redteam_decoupe, G). */
      cv.width=s.width; cv.height=s.height; cv.style.setProperty('width',(s.width/dpr)+'px','important'); cv.style.setProperty('height',(s.height/dpr)+'px','important');
      cv.style.setProperty('max-width','none','important'); cv.style.setProperty('max-height','none','important');   /* sinon une dalle un peu plus large que sa boîte est tassée d'un seul côté */
      cv.getContext('2d').drawImage(s,0,0); cv.__ok=1;
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
      NX.appendChild(noyau(K.toi.d, K.toi.arc, K.toi.ph, D.toi, 'toi', true, D.recu));
      var gp=el('div','au-gp');
      D.gens.forEach(function(g){ gp.appendChild(noyau(K.pers.d, K.pers.arc, K.pers.ph, g.parts, g.nom, false, g.recu)); });
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
    GR2.textContent='';
    var L2=D.RT.slice(-3).reverse(); L2.forEach(function(p){ var c2=cellule(p); c2.className='au-c2'; GR2.appendChild(c2); });
    MO2.classList.toggle('au-sans', vide || !L2.length);
    voile();
    var sans = vide || !L.length;
    MO.classList.toggle('au-sans', sans);
    /* la légende n'est centrée entre deux voisins que s'ils sont là tous les deux */
    if(sans) LG.removeAttribute('data-centre-entre');
    /* ⚑ 23 sept., second tour : le bouton s'intercale entre la légende et la moisson.
       La légende est donc centrée entre les Noyaux et LE BOUTON — c'est la déclaration qui
       change, et le juge la suit sans qu'on touche à son code (§7). */
    else LG.setAttribute('data-centre-entre', '.au-nx|#auPartage|'+(K.lgINK-K.cptINK)+'|.au-cpt');   /* v95 : le bloc centré est le GROUPE « légende + chiffres » (4e champ : ce qui le ferme) */
    [0,60,200,600].forEach(function(t){ setTimeout(peintMoisson, t); });
    CAD.scrollTop=0; PEL.colK=''; place();
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
  /* v95 — les trois nombres, la même lecture que les anneaux (`parts`) ; chacun centré sous son entrée de légende (sa position vient de la
     légende, jamais du chiffre : pas de boucle) ; on compare avant d'écrire (§8) */
  function comptes(){ if(!CPT||!LG) return; try{
    var t=0,e=0,r=0; mesPromi().forEach(function(p){ if(p.status==='tenu') t++; else if(p.status==='rate') r++; else e++; });
    var v=[t,e,r], S=CPT.children, L=LG.children;
    for(var i=0;i<S.length&&i<L.length;i++){ var s=''+v[i]; if(S[i].textContent!==s) S[i].textContent=s;
      var x=(L[i].offsetLeft+L[i].offsetWidth/2).toFixed(1)+'px'; if(S[i].style.left!==x) S[i].style.left=x; } }catch(_){} }
  function place(){
    if(!CAD) return;
    try{ reteintSiBesoin(); }catch(e){}   /* ⚑ 21 sept. : les états suivent le thème, quel que soit le chemin */
    /* ⚑ 23 SEPTEMBRE 2026, second tour (Tom) — « LE BOUTON DE PARTAGE REMONTE SOUS LA
       LÉGENDE — EN BAS DE PAGE, PERSONNE N'Y VA. REPRENDS LES ESPACES DE TOUTE LA COLONNE. »
       MESURÉ AVANT : le bouton tombait à **y 1045**, soit **201 px sous le pli** — il fallait
       faire défiler toute la moisson pour le découvrir.
       LA COLONNE SE RELIT DONC DANS CET ORDRE : la Pelote · la phrase · les Noyaux · la
       légende · **le bouton** · ce que tu as tenu · ce qu'on t'a tenu. Chaque bloc garde
       l'air de la planche (`K.AIR` = 28), et rien n'est à une cote figée : tout se dérive du
       bas réel de ce qui précède (§8, « une cote dérivée n'est pas un espace »).
       ⚠ LA RÈGLE DU PLI (Q186) SORT AVEC LUI : elle poussait le bouton À 844 pour qu'il ne
       soit pas coupé en deux. Le bouton est maintenant à mi-hauteur d'écran ; appliquée ici,
       elle le renverrait sous le pli — c'est-à-dire exactement le défaut qu'on corrige. */
    var c;
    if(CAD.classList.contains('au-vide')){
      c={nx:K.nx.y, lg:K.lgY, bt:K.lgY+K.lgH+K.AIR};
      c.mo=c.bt+K.bt.h+K.AIR;
    } else {
      var nx=K.motY+MOT.offsetHeight+K.AIR_MOT, d=nx-K.nx.y;
      /* l'air AU-DESSUS de la légende vaut K.AIR, comme celui en dessous : la colonne garde
         un rythme unique (28) de la rangée des Noyaux jusqu'à la moisson. */
      c={nx:nx, lg:nx + K.nx.h + K.AIR + K.lgINK};
      c.cpt = c.lg + K.lgH + K.cptAIR;                   /* v95 : les trois chiffres, tout près de leur légende */
      c.bt = c.cpt + K.cptH + K.AIR + K.cptINK;          /* le bouton, sous les chiffres : l'air À L'ENCRE est égal au-dessus du groupe « légende + chiffres » et en dessous */
      c.mo = c.bt + K.bt.h + K.AIR;                      /* puis « ce que tu as tenu » */
      var bas = MO.classList.contains('au-sans') ? c.mo : c.mo+MO.offsetHeight;
      /* la seconde rangée suit la première du même air (28) */
      c.mo2 = bas + K.AIR; if(MO2 && !MO2.classList.contains('au-sans')) bas = c.mo2 + MO2.offsetHeight;
      c.finBas = bas;
    }
    c.fin=(c.finBas!=null?c.finBas:(c.mo+K.AIR))+K.marge;
    if(c.mo2==null) c.mo2=c.mo;
    if(c.cpt==null) c.cpt=c.lg;
    comptes();
    var k=[c.nx,c.lg,c.cpt,c.mo,c.mo2,c.bt,c.fin].map(function(v){ return v.toFixed(2); }).join('|');
    if(k===PEL.colK) return;                 /* on compare avant d'écrire (§8) */
    PEL.colK=k; PEL.col=c;
    [[NX,c.nx],[LG,c.lg],[CPT,c.cpt],[MO,c.mo],[MO2,c.mo2],[BT,c.bt],[FIN,c.fin-1]].forEach(function(a){ if(!a[0]) return;
      a[0].style.setProperty('top', a[1].toFixed(2)+'px', 'important'); });
  }

  /* ════════════════════════════════════════════════════════════════════════════
     LA SPHÈRE
     ════════════════════════════════════════════════════════════════════════════ */
  /* ⚑ LES CLÉS DE STOCKAGE CHANGENT DE NOM AVEC L'OBJET — ET CE QUI ÉTAIT GARDÉ SUIT.
     Renommer sans migrer aurait effacé les caresses inscrites sur la Pelote et le palier de
     densité déjà réglé. On recopie une fois, puis on oublie l'ancien nom. */
  try{ ['traces','palier','vus','ordre'].forEach(function(k){
    var nv='promi_pelote_'+k, av='promi_orbite_'+k;
    if(localStorage.getItem(nv)===null){ var v=localStorage.getItem(av);
      if(v!==null){ localStorage.setItem(nv,v); localStorage.removeItem(av); } } }); }catch(_){}
  var PEL = { iles:null, cleI:'', palier:Math.max(0, Math.min(PALIERS.length-1, lsGet('promi_pelote_palier',0)|0)),
              ms:[], frames:0, skip:0, pret:false, cede:0, dernier:0 };
  PEL.vise=PEL.palier;   /* le palier VISÉ par le régulateur — il s'applique à l'ouverture suivante (densite) */
  var V = { lac:2.9, tan:G.TANG, vlac:0, vtan:0, om:G.AUTO, lacAv:2.9, tau:G.TAU };
  var EMP = null, TVER = 0, ATTENTE = [];
  /* les caresses en attente s'inscrivent quand tout est au repos (voir `lacher`) */
  function inscrit(){
    if(!ATTENTE.length || DG.on || V.vlac || V.vtan || EMP) return;
    var av=TRACES;
    TRACES=TRACES.concat(ATTENTE).slice(-G.TRACES); ATTENTE=[]; TVER++;
    retouche(av, TRACES);   /* v21 : plus de stockage — la Pelote redevient lisse à chaque ouverture */
  }
  /* ⚑ UNE CARESSE SE RETOUCHE, ELLE NE REFAIT PAS TOUT LE CACHE. Mesuré au profileur : chaque
     inscription refaisait les 110 000 poils — relief `phi` compris, qui ne dépend pas des
     caresses — soit 240 à 340 ms d'image figée. On ne recalcule que les points proches des
     arcs qui entrent ou qui sortent (`PeloteMoteur.retoucheTraces`). Les semis des autres
     paliers ne sont pas retouchés : on les INVALIDE, ils se referont entiers s'ils resservent
     — jamais avec des caresses périmées. */
  function retouche(av, nv){
    var S=semis();
    for(var N in SEMC) if(SEMC[N]!==S) SEMC[N].__stCle=null;
    if(!S.__st) return;
    var t0=performance.now(), n=M.retoucheTraces(S.__st, av, nv);
    PEL.retouche={points:n, ms:+(performance.now()-t0).toFixed(1)};
  }
  /* ⚑ v21 (Tom, 22 sept.) — « quand on ferme et rouvre l'Aura, elle redevient lisse » : les caresses ne se
     gardent plus d'une ouverture à l'autre (elles venaient du stockage local). */
  var TRACES = [];

  var ATL=null;
  function atlas(){
    if(ATL) return ATL;
    /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « PLUS VELUE, UNIFORMÉMENT DENSE, DOUX COMME DU PELAGE DE
       LAPIN, LIMITE BOULE ANTISTRESS ». LE POIL ÉTAIT TROP COURT : à 2,5·k sur un canevas de
       592, un brin faisait 2 à 3 pixels — un GRAIN DE SABLE, pas une fibre. Agrandi ×1,6, les
       brins se recouvrent, le limbe s'effiloche et la silhouette cesse d'être un cercle net.
       Mesuré à vue figée, mode clair : le « piquant » (écart-type local 3×3 de la luminance,
       `scratchpad/velu3.py`) tombe de 11,93 à 6,93, l'étendue p05→p95 de 175 à 160.
       ⚠ CE QUE ÇA COÛTE, ET C'EST LE PLAFOND : 13,8 → 17,0 ms par image. Ce sont les PIXELS
       ÉCRITS qui dominent maintenant, plus le travail par poil — mesuré : à nombre de pixels
       égal, 60 000 poils longs coûtent comme 110 000 courts (18,3 contre 18,0). Le régulateur
       descend donc d'un palier (110 000 → 90 000) : à 1,6 de long, la couverture reste
       1,31 fois celle d'avant. ×2,2 donnait un pelage franchement plus beau et 35 ms : refusé. */
    var k=K.bo.d/620*1.6, T=[2.5*k, 4.4*k, 5.7*k, 7.3*k];   /* ESSAI B : le poil est TROIS FOIS trop court */
    return (ATL={a:M.atlasAlpha(M.GRAIN_POIL, T, M.ORI, M.NIVA, 0.15, 0.78, true, M.NVAR), t:T});
  }
  var SEMC={};
  function semis(){ var N=PALIERS[PEL.palier]; return SEMC[N] || (SEMC[N]=M.semisPavage(N, 77, 0.0, KDENS, 4, false, 0)); }
  /* la clé du cache ne porte PLUS les caresses : elles se retouchent en place (voir `retouche`) */
  function cleIles(){ if(PEL.iles) PEL.iles.cle='aura|'+PEL.cleI; }
  /* quelles dalles doivent céder leur teinte, et au rang de quelle couleur de leur palette */
  var CEDE={};
  function poseIles(T){
    return M.batIles(T.length, window.Toile.cols(), {pxr:PXR, mag:MAG, palette:window.Toile.getPalette(),
      /* ⚑ LA VRAIE DALLE DU PROMI. Elle occupe l'emprise que la planche taillait à son
         île (`g`, la cellule, en px CSS à l'échelle PXR/MAG) : son plus grand côté y est
         calé. La forme vient du moteur ; seule la TAILLE est réglée par l'île. */
      dalle:function(k, I, g){
        var s=dalleLisible(T[k]); if(!s) return null;
        var cote=Math.max(s.width, s.height);
        return {cv:s, sx:s.width/2, sy:s.height/2, kk:cote/(g/(PXR/MAG)), monde:T[k].monde};
      }});
  }
  function iles(){
    var T=D.T, F=fondSphere();
    /* ⚑ LE SOL ENTRE DANS LA CLÉ. Sans lui, changer de thème ne rebâtissait pas les îles : la teinte
       cédée restait celle décidée contre l'ANCIEN sol, et en clair rien ne cédait jamais. */
    var cle=T.map(cleMonde).join(',')+'|'+[F[0]|0,F[1]|0,F[2]|0].join(',');
    if(PEL.iles && PEL.cleI===cle) return PEL.iles;
    /* ⚑ CHANTIER 59 · ON BÂTIT, ON MESURE, ON FAIT CÉDER, ON REBÂTIT — et jamais plus de `DE_ESSAIS`
       tours. À chaque tour, une île encore sous le plancher prend la couleur SUIVANTE de sa palette
       (rangée par écart de teinte au sol). Les masques sont déjà en mémoire : un tour ne coûte que la
       requantification de `batIles`, pas un rendu de dalle ni une image. */
    var r=poseIles(T), tours=0, det=[], avant=1e9;
    for(tours=0; !clair() && tours<DE_ESSAIS; tours++){
      var reste=0, marque=[];
      for(var k=0;k<r.iles.length && k<T.length;k++){
        var L=lisibiliteIle(r, k); if(!L) continue;
        if(L.dE < plancher()){ marque.push(cleMonde(T[k])); reste++; }
      }
      det.push(reste);
      /* ⚑ UN TOUR QUI NE GAGNE RIEN EST LE DERNIER. Sans cette sortie, en clair la boucle rebâtissait les
         îles quatre fois à chaque ouverture sans jamais faire descendre le compte (restes [5,5,5,5]) :
         du travail pur, sur un écran dont l'élan est déjà le chantier 73. */
      if(!reste || reste>=avant) break;
      avant=reste;
      for(var w=0;w<marque.length;w++) CEDE[marque[w]]=(CEDE[marque[w]]||0)+1;
      r=poseIles(T);
    }
    PEL.ch59mesure={tours:tours, restes:det, plancher:plancher(), clair:clair(),
      iles:T.map(function(p,k){ var L=lisibiliteIle(r,k);
        return {titre:p.title, dE:L?+L.dE.toFixed(1):null, rang:CEDE[cleMonde(p)]||0}; })};
    PEL.iles=r; PEL.cleI=cle; cleIles();
    return r;
  }
  function empPour(E){
    return {c:E.c, ax:E.ax, a:E.a, el:E.el, dmax:E.dmax, p:E.p,
            biais:0.14, rho:0.085, ub:0.35, B:0.32, U:0.50};
  }
  function opts(){
    var A=atlas();
    return {css:K.bo.d, R:K.R, sol:PEL.solR||solEffectif(), tailles:A.t, atlas:A.a, semis:semis(),
            relief:FROISSE, env:ENV, kn:KN, lac:V.lac, tan:V.tan, pal:window.Toile.cols(),
            trame:PEL.sansIles?ilesVides():PEL.iles, libre:false, fond:'rgba(0,0,0,0)',
            velours:0, contre:0, duvet:0, grade:0, velours2:1, dresse:0,
            pousse:Math.min(1, D.n/34), traces:TRACES, peigneAxial:1, tracesIncr:1,
            emp:(EMP && EMP.p>=G.EMP_FIN) ? empPour(EMP) : null, peauVers:peauVers()};
  }
  /* pour la mesure seulement : une trame SANS île (`trame:null` fait lever le peintre — mesuré) */
  function ilesVides(){
    if(!PEL.ilesVides){ PEL.ilesVides=M.batIles(0, window.Toile.cols(), {pxr:PXR, mag:MAG,
        palette:window.Toile.getPalette(), dalle:function(){ return null; }});
      if(PEL.ilesVides) PEL.ilesVides.cle='aura|vide'; }
    return PEL.ilesVides;
  }
  function clair(){ var d=document.getElementById('device'); return !!(d && d.classList.contains('light')); }
  function peauVers(){
    if(!clair() || !D) return null;
    /* ⚑ Q210 : la peau va AU CRÈME DU CORPS (§1.3), plus à la teinte claire tirée à 60 % (A2). C'est la
       moitié claire de l'inversion, et elle rend à la boule une partie de ce que le poil sombre lui prend :
       mesuré, elle ramène l'écart boule ↔ page de 123,7 à 116,3 sans rien coûter aux îles (18,0 → 18,1). */
    var c=PEL.peauC||[CREME[0], CREME[1], CREME[2]],
        t=(PEL.peauT!=null)?PEL.peauT:K.PEAU_T;
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
    if(statique){ PEL.skip=4; return; }
    if(PEL.skip>0){ PEL.skip--; return; }
    if(EMP) return;
    PEL.ms.push(ms); if(PEL.ms.length>90) PEL.ms.shift();
    PEL.frames++;
    if(PEL.ms.length<45) return;
    var med=mediane(PEL.ms.slice(-45)), N=PALIERS[PEL.palier], v;
    if(med>G.BUDGET){
      /* le palier le plus dense qui tiendrait le budget, au prorata des poils (banc_lent) */
      for(v=PEL.palier; v<PALIERS.length-1 && med*PALIERS[v]/N>G.BUDGET; v++);
    } else if(PEL.ms.length>=90 && PEL.palier>0){
      /* ⚠ ET ELLE REMONTE : si le palier du dessus, à ce prorata, tiendrait sous 15 ms. L'écart
         avec le seuil de descente (16,7) évite le va-et-vient. */
      v=(mediane(PEL.ms.slice(-90))*PALIERS[PEL.palier-1]/N<15) ? PEL.palier-1 : PEL.palier;
    } else if(PEL.ms.length>=90){ v=PEL.palier; } else return;
    if(v===PEL.vise) return;
    if(v>PEL.palier) PEL.cede++; else if(v<PEL.palier) PEL.remonte=(PEL.remonte||0)+1;
    /* ⚑ Q237 (Tom, 20 sept.) : « une sphère qui s'appauvrit définitivement après un pic est
       un défaut ». On NE PERSISTE PLUS LA VISE : un pic de quelques secondes écrivait le
       palier bas dans le stockage et le chargement suivant démarrait dessus, sans retour
       possible de la séance. Le stockage n'enregistre plus que ce qui a été APPLIQUÉ
       (voir `applique()`), c'est-à-dire ce que la machine a vraiment eu besoin de faire. */
    PEL.vise=v;
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
    if(EMP.tr===0){ var tt=(now-EMP.t0)/1000;
      EMP.p=Math.min(1, 1-G.CEDE*Math.exp(-tt/G.CEDE_TAU)-(1-G.CEDE)*Math.exp(-tt/G.RESISTE_TAU)); return; }
    /* on lâche : la matière encaisse et revient — et quand on LANCE, ce qui file
       par-dessus comble le creux, d'autant plus vite qu'on lance fort */
    var p=EMP.pRel*Math.exp(-(now-EMP.tr)/1000/G.REPOUSSE_TAU);
    EMP.comble+=G.COMBLE*V.om*dt;
    EMP.p=Math.max(0, p-EMP.comble);
    /* ⚠ ON NE LA RETIRE QUE QUAND ELLE EST INVISIBLE. À p = 0,02 elle était encore profonde de
       7 % (≈ 2 pt) et large de 0,11 rad : son retrait faisait un SAUT à la dernière image (Tom,
       10 sept. : « ça passe de trop loin encore déformé à net d'un coup »). À 0,002 elle ne fait
       plus que 0,4 pt, et ses effets se sont éteints avec elle (5 %, voir la part FE du peintre). */
    if(EMP.p<G.EMP_FIN) EMP=null;
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
    PEL.tick=(PEL.tick||0)+1; PEL.dtReel=dtR;
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
      if(!PEL.fige){ V.lac+=(G.AUTO+V.vlac)*dt; V.tan=borne(V.tan+V.vtan*dt); }
      V.om=Math.sqrt((G.AUTO+V.vlac)*(G.AUTO+V.vlac)+V.vtan*V.vtan);
    }
    V.lacAv=V.lac;
    majEmp(dt);
    inscrit();
    if(!PEL.pret || couvert()) return;
    var S=semis(), av=S.__stCle, t0=performance.now();
    try{ M.peint(CV, opts()); }catch(e){ window._auraErreur=String(e&&e.stack||e); PEL.pret=false; return; }
    var ms=performance.now()-t0;
    PEL.dernier=ms; PEL.peints=(PEL.peints||0)+1;
    if(PEL.peints%30===0) place();
    densite(ms, S.__stCle!==av);
  }

  /* ── LE DOIGT ─────────────────────────────────────────────────────────────── */
  /* ⚑ `hD` — LE PAS DE TEMPS DE CHAQUE MOUVEMENT (chantier 73). Sans lui, un SEUL mouvement dans la
     fenêtre ne donne aucune vitesse : on n'a qu'un instant, pas une durée. Or c'est le cas normal sur
     un appareil lent — mesuré au bridage ×4, ×6, ×10 : tout le balayage arrive en UN mouvement, et la
     vitesse sortait nulle. Chaque entrée porte donc l'écart à l'événement qui la précède (le toucher
     compris), et la vitesse se calcule sur la somme de ces pas — juste avec un échantillon comme avec cinq. */
  var DG={on:false, x:0, y:0, parc:0, hT:new Float64Array(16), hL:new Float64Array(16),
          hG:new Float64Array(16), hD:new Float64Array(16), tPrev:0,
          hi:0, hn:0, tr0:null, trN:null, arcs:[], tap:0};
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
    return {a:a, el:elp, dmax:G.PROF*a, ax:[0.62,-0.72,0], capteur:!!(e && e.pointerType==='touch' && e.width>4 && e.height>4)};
  }
  /* ⚑ v96 (Tom, 29 sept. : « la forme de l'empreinte doit s'adapter à ce qui touche […] les traces ne sont ni assez réactives, ni
     crédibles, ni cohérentes avec le geste — du micro-réglage, pas une refonte ») — l'empreinte suit, PENDANT l'appui : ① sa taille et son
     allongement, lus en continu sur la surface de contact (un doigt qui s'aplatit s'élargit) ; ② son orientation, celle du geste (le sens
     où le doigt glisse, projeté sur la boule) ; ③ glisser étire l'empreinte dans le sens du geste (le poil se couche en traînée). Lissé : rien
     ne tressaute. Sans capteur (souris), la taille reste celle du pouce ; l'orientation suit quand même le geste. */
  function empSuit(e, v){
    if(!EMP || EMP.tr!==0 || !v) return;
    var f=doigt(e), k=0.35;
    if(EMP.el0==null) EMP.el0=EMP.el;
    if(f.capteur){ EMP.a+=(f.a-EMP.a)*k; EMP.el0+=(f.el-EMP.el0)*k; EMP.dmax=G.PROF*EMP.a; }
    var el0=EMP.el0, dx=e.clientX-(EMP.lx==null?e.clientX:EMP.lx), dy=e.clientY-(EMP.ly==null?e.clientY:EMP.ly), m=Math.sqrt(dx*dx+dy*dy);
    if(m>1.5){ var s=echelle(), R0=14*s, v3=surBoule(e.clientX+dx/m*R0, e.clientY+dy/m*R0);
      if(v3){ var t=nrm([v3[0]-v[0], v3[1]-v[1], v3[2]-v[2]]), a0=EMP.ax, q=0.45; EMP.ax=nrm([a0[0]+(t[0]-a0[0])*q, a0[1]+(t[1]-a0[1])*q, a0[2]+(t[2]-a0[2])*q]); }
      EMP.lx=e.clientX; EMP.ly=e.clientY; EMP.gl=Math.min(1, (EMP.gl||0)+m/(40*s)); }
    else EMP.gl=Math.max(0, (EMP.gl||0)-0.08);
    EMP.el=Math.max(0.5, el0*(1-0.28*(EMP.gl||0)));   /* en glissant, jusqu'à 0,72 × l'allongement du contact */
  }
  function relisse(){ var av=TRACES; TRACES=[]; ATTENTE=[]; TVER++; lsSet('promi_pelote_traces', []); retouche(av, TRACES); }
  function gestesBoule(){
    PRISE.addEventListener('pointerdown', function(e){
      DG.on=true; try{ PRISE.setPointerCapture(e.pointerId); }catch(_){}
      DG.x=e.clientX; DG.y=e.clientY; DG.parc=0; DG.hn=0; DG.hi=0; DG.arcs=[]; DG.px=e.clientX; DG.py=e.clientY; DG.pas=0;
      DG.tPrev=(e.timeStamp||performance.now());
      V.vlac=0; V.vtan=0; V.tau=G.TAU;
      var v=surBoule(e.clientX, e.clientY);
      if(v){ var f=doigt(e);
        EMP={c:v, ax:f.ax, a:f.a, el:f.el, el0:f.el, dmax:f.dmax, p:0, t0:performance.now(), tr:0, pRel:0, comble:0, lx:e.clientX, ly:e.clientY, gl:0};
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
        var te=ce.timeStamp||e.timeStamp||performance.now();
        DG.hT[DG.hi]=te; DG.hD[DG.hi]=Math.max(1, te-(DG.tPrev||te)); DG.tPrev=te;
        DG.hL[DG.hi]=dx*G.SENS; DG.hG[DG.hi]=-dy*G.SENS;
        DG.hi=(DG.hi+1)%16; if(DG.hn<16) DG.hn++;
      }
      var v=surBoule(e.clientX, e.clientY);
      /* ⚑ v21 — LE POIL SE COUCHE SOUS LE DOIGT, DANS LE SENS DU GESTE. Glisser fait tourner la boule : le point
         touché reste le même point de l'objet, et l'arc « départ → arrivée » sortait presque nul — rien ne
         s'inscrivait. On pose donc, tous les ~20 px de geste, un arc AU POINT TOUCHÉ, orienté comme le doigt. */
      if(v){ DG.pas=(DG.pas||0);
        var _dx=e.clientX-(DG.px==null?e.clientX:DG.px), _dy=e.clientY-(DG.py==null?e.clientY:DG.py);
        DG.pas+=Math.sqrt(_dx*_dx+_dy*_dy)/s;
        if(DG.pas>=20){ var _m=Math.sqrt(_dx*_dx+_dy*_dy)||1, _R=24*s;
          var _v2=surBoule(e.clientX+_dx/_m*_R, e.clientY+_dy/_m*_R);
          if(_v2){ var _g=arc(versObjet(v), versObjet(_v2)); _g.L=Math.max(_g.L, G.W); DG.arcs.push(_g); }
          DG.pas=0; }
        DG.px=e.clientX; DG.py=e.clientY; }
      if(v){
        if(EMP && EMP.tr===0){ EMP.c=v; empSuit(e, v); }
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
        else { DG.tap=now;
          /* ⚑ v21 — et LÀ OÙ ON LA TOUCHE, LE POIL SE COUCHE ET RESTE COUCHÉ (un arc au diamètre du doigt) */
          try{ var _s=echelle(), _v=surBoule(DG.x, DG.y), _w=surBoule(DG.x, DG.y+24*_s);
            /* inscrite AU LÂCHER (pas au repos) : au repos, le lustre paraissait d'un coup au moment où le creux
               finissait de se refermer — un saut. Un toucher n'a pas d'élan à saccader, et la retouche est locale. */
            if(_v && _w){ var _a=arc(versObjet(_v), versObjet(_w)); _a.L=Math.max(_a.L, G.W);
              var _av=TRACES; TRACES=TRACES.concat([_a]).slice(-G.TRACES); TVER++; retouche(_av, TRACES); } }catch(_){}
        }
        DG.px=null; DG.py=null; DG.pas=0;
        return;
      }
      DG.px=null; DG.py=null; DG.pas=0;
      DG.tap=0;
      /* ⚑ CHANTIER 73 — LA FENÊTRE DE L'ÉLAN SUIT LA CADENCE RÉELLE (12 sept. 2026).
         Elle était figée à **90 ms** : c'est cinq mouvements à 60 images par seconde, donc une
         hypothèse de MACHINE RAPIDE déguisée en durée — exactement ce que le §8 interdit
         (« un mouvement se calcule sur le temps réel, jamais sur le compte d'images »).
         MESURÉ au bridage CPU du CDP, lancer joué dans la page, 6 mouvements cadencés, 3 essais
         par palier (`sauvegardes/ch73/elan_sous_charge.py`) : les mouvements arrivent à **58, 90
         et 148 ms** d'écart à ×4, ×6 et ×10 ; le dernier tombe donc HORS de la fenêtre, la boucle
         rompt au premier tour, `t0` reste `now`, `dtt` vaut 0, et la vitesse reste **NULLE** —
         **0,00 rad/s aux neuf essais**, contre 11 rad/s à ×1. L'élan était perdu sur un appareil
         lent, et c'est le PRODUIT, pas le juge : le juge lance déjà dans la page, cadencé.
         CE QUE LA FENÊTRE PROTÉGEAIT, et qu'on garde : un doigt qui S'ARRÊTE avant de lâcher ne
         lance pas. Mais ça ne se mesure pas sur la même grandeur — c'est l'attente entre le
         DERNIER mouvement et le lâcher, rapportée à la cadence qu'on vient d'observer.
         ET LA VITESSE SE PREND SUR LA DURÉE DES MOUVEMENTS, pas jusqu'au lâcher : sinon une image
         lente entre le dernier mouvement et le lâcher divise la vitesse par ce temps mort. */
      var der=DG.hn?DG.hT[(DG.hi-1+16)%16]:now;
      var ec=[], jj;
      for(jj=1; jj<DG.hn && jj<5; jj++){
        var ta=DG.hT[(DG.hi-jj+16)%16], tb=DG.hT[(DG.hi-jj-1+16)%16];
        if(ta>tb) ec.push(ta-tb);
      }
      ec.sort(function(x,y){ return x-y; });
      var cad=ec.length?ec[ec.length>>1]:16;
      var FEN=Math.max(90, 3*cad);          /* jamais MOINS que les 90 ms d'origine */
      var sl=0, st=0, dt=0, nEch=0;
      if(now-der<=FEN){
        for(var i=0;i<DG.hn;i++){ var j=(DG.hi-1-i+32)%16; if(der-DG.hT[j]>FEN) break;
          sl+=DG.hL[j]; st+=DG.hG[j]; dt+=DG.hD[j]; nEch++; }
      }
      var dtt=dt/1000;
      if(dtt>0.012){ V.vlac=Math.max(-G.VMAX, Math.min(G.VMAX, sl/dtt));
                     V.vtan=Math.max(-G.VMAX, Math.min(G.VMAX, st/dtt)); }
      DG.elan={sl:sl, st:st, dtt:dtt, hn:DG.hn, now:now, der:der, vlac:V.vlac,
               cadence:cad, fenetre:FEN, echant:nEch, attente:+(now-der).toFixed(1), pas:+dt.toFixed(1)};
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

  /* ⚑ UNE PAROLE DE PLUS : L'PELOTE FAIT UN TOUR pour présenter la dalle qu'on vient de
     poser. Le levier est le GESTE : c'est un élan, qui s'additionne à la rotation lente
     et s'y rend sans saccade. La vue qui centre une direction se calcule :
        lac = atan2(−c0, c2)     tan = atan2(c1, hypot(c0, c2))                      */
  function tourSiNeuf(){
    var vus=lsGet('promi_pelote_vus', null); lsSet('promi_pelote_vus', D.n);
    if(vus===null || D.n<=vus || !PEL.iles || !PEL.iles.derniere) return;
    var c=PEL.iles.derniere, lacT=Math.atan2(-c[0], c[2]), tanT=Math.atan2(c[1], Math.sqrt(c[0]*c[0]+c[2]*c[2]));
    var dl=((lacT-V.lac)%6.283185307+6.283185307)%6.283185307; if(dl<3.14159) dl+=6.283185307;
    V.tau=G.TOUR_TAU; V.vlac=dl/G.TOUR_TAU; V.vtan=(borne(tanT)-V.tan)/G.TOUR_TAU; PEL.tour=D.n;
  }

  function publie(){
    if(!D) return;
    window._auraComp = {
      vide:CAD.classList.contains('au-vide'), n:D.n, nature:D.nature, sol:NAT[D.nature],
      iles:D.T.map(function(p){ var m=p.monde||{}; return {pid:p.id, titre:p.title, monde:[m.m,m.p,m.h]}; }),
      ilesPeintes:PEL.iles ? PEL.iles.iles.filter(function(I){ return !!I.m; }).length : 0,
      derniere:(PEL.iles && PEL.iles.derniere) ? PEL.iles.derniere.slice() : null,
      toi:D.toi, recu:D.recu, gens:D.gens.map(function(g){ return {nom:g.nom, parts:g.parts, recu:g.recu}; }),
      onTaTenu:D.RT.slice(-3).reverse().map(function(p){ return p.id; }),
      moisson:D.T.slice(-nbMoisson()).reverse().map(function(p){ return p.id; }),
      mot:MOT.textContent, photoMoi:!!(typeof USER!=='undefined' && USER && USER.photo)
    };
  }
  /* ⚑ v21 — à chaque ouverture de l'Aura, la Pelote redevient lisse */
  try{ var _sb=document.getElementById('souffleBtn'); if(_sb) _sb.addEventListener('click', function(){ try{ relisse(); }catch(_){} }, true); }catch(_){}
  window._aura = {
    etat:function(){ return {pret:PEL.pret, lac:V.lac, tan:V.tan, vlac:V.vlac, vtan:V.vtan, om:V.om,
      prise:DG.on, emp:EMP?{p:EMP.p, relache:EMP.tr>0, c:EMP.c, a:EMP.a}:null, traces:TRACES.length,
      attente:ATTENTE.length,
      tver:TVER, palier:PALIERS[PEL.palier], vise:PALIERS[PEL.vise], ms:mediane(PEL.ms), dernier:PEL.dernier,
      frames:PEL.frames, peints:PEL.peints||0, cede:PEL.cede, remonte:PEL.remonte||0,
      tick:PEL.tick||0, dtReel:PEL.dtReel||0, retouche:PEL.retouche||null,
      erreur:window._auraErreur||null, tour:PEL.tour||0, elan:DG.elan||null, col:PEL.col||null,
      ch59:PEL.ch59||null, ch59seuils:[DE_PLANCHER, DE_VISE], ch59mesure:PEL.ch59mesure||null}; },
    relisse:relisse, K:K, G:G, PALIERS:PALIERS, MOTS:MOTS,
    /* pour le juge : poser la phrase i (null = celle des données) et recalculer la colonne */
    mot:function(i){ if(!CAD || CAD.classList.contains('au-vide')) return null;
      MOT.textContent = (i===null||i===undefined) ? (D.n>0 ? MOTS[D.n % MOTS.length] : VIDE[0])
                                                  : MOTS[((i|0)%MOTS.length+MOTS.length)%MOTS.length];
      place(); return MOT.textContent; },
    /* pour le juge : repartir d'un palier donné (0 = 110 000) et oublier les mesures */
    palier:function(i){ PEL.palier=PEL.vise=Math.max(0, Math.min(PALIERS.length-1, i|0)); PEL.ms=[]; PEL.skip=4; },
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
    fige:function(b){ PEL.fige=!!b; },
    /* pour la mesure du thème clair (Q182) : la part de teinte de la peau (null = celle décidée), et la
       boule SANS ses îles (le masque qui isole leur contraste) — jamais appelés par le produit */
    reglePeau:function(t){ PEL.peauT=(t===null||t===undefined)?null:+t; },
    /* pour la mesure (Q182) : la couleur VERS laquelle la peau s'éclaircit ([r,g,b], null = la teinte claire §1.2) */
    reglePeauC:function(c){ PEL.peauC=c?[c[0]|0,c[1]|0,c[2]|0]:null; },
    /* pour la mesure (Q182) : la couleur du POIL du sol ([r,g,b], null = la nature) */
    regleSol:function(c){ PEL.solR=c?[c[0]|0,c[1]|0,c[2]|0]:null; var S=semis(); S.__stCle=null; },
    sansIles:function(b){ PEL.sansIles=!!b; var S=semis(); S.__stCle=null; },
    vue:function(l,t){ V.lac=+l; V.tan=borne(+t); V.lacAv=V.lac; V.vlac=0; V.vtan=0; },
    /* le ton du sol : lequel des quatre, et en tirer un neuf (pour le juge et pour le partage) */
    sol:function(){ return {idx:SOL_IDX, rgb:solPalette()}; },
    nouveauSol:nouveauSol,
    /* ⚑ LE PARTAGE DEMANDE LA PELOTE. On peint DANS `CV` — `opts()` lit ses cotes — puis
       l'appelant recopie. On ne rappelle PAS `ouvre()` : un partage ne retire pas un ton neuf. */
    pelote:function(){
      try{ if(!PEL.pret){ squelette(); remplit(); prepare(); }
           /* ⚠ LE PEINTRE EXIGE LA TRAME. Sans îles, `M.peint` lève `Cannot read properties of
              null (reading 'dl')` — mesuré : la Pelote sortait NOIRE dans le partage tant que
              l'Aura n'avait pas été ouverte une fois. On les bâtit avant de peindre. */
           if(!PEL.iles) iles();
           M.peint(CV, opts()); PEL.peints=(PEL.peints||0)+1; }catch(e){ window._auraErreur=String(e&&e.stack||e); }
      return CV; }
  };

  /* ⚑ Q237 — LA VISE S'APPLIQUE, ET ELLE S'APPLIQUE AILLEURS QU'À L'OUVERTURE.
     MESURÉ AVANT DE TOUCHER : `prepare()` ne tournait QU'À L'OUVERTURE de l'écran, et
     `#auraScreen` NE PERD JAMAIS sa classe `show` — `closeAll()` la laisse. L'observateur
     ne se réveillait donc jamais une seconde fois : la vise était calculée à chaque image
     et **n'était jamais appliquée** de toute la séance. Le seul chemin qui la faisait
     mordre était le RECHARGEMENT de la page, par le stockage — d'où « il garde le palier ».
     Relevé : bridage ×8 → vise 75 000, palier resté 110 000 ; réouverture → palier 110 000.
     La règle de Q186 ne bouge pas — « jamais sous les yeux ». On applique donc au moment
     où l'on QUITTE l'Aura, et quand l'onglet passe en arrière-plan. */
  function applique(){
    if(PEL.vise===PEL.palier) return false;
    PEL.palier=PEL.vise; PEL.ms=[]; PEL.skip=4;
    lsSet('promi_pelote_palier', PEL.palier);
    return true;
  }
  function prepare(){
    PEL.pret=false;
    /* la vise du régulateur prend effet ICI, pendant que l'écran se bâtit — jamais sous les yeux */
    applique();
    var E=[function(){ atlas(); }, function(){ semis(); }, function(){ iles(); },
           function(){ PEL.pret=true; tourSiNeuf(); publie(); }];
    var i=0;
    (function suite(){
      if(!actif()) return;
      try{ E[i](); }catch(e){ window._auraErreur=String(e&&e.stack||e); }
      i++; if(i<E.length) setTimeout(suite, 0);
    })();
  }
  function ouvre(){
    try{ nouveauSol(); }catch(_){}          /* ⚑ un ton neuf à chaque ouverture (Tom) */
    try{ squelette(); remplit(); prepare(); }catch(e){ window._auraErreur=String(e&&e.stack||e); }
    if(!RAF){ TP=0; RAF=requestAnimationFrame(boucle); }
  }
  /* ⚠ `#auraScreen` NE PERD JAMAIS sa classe `show` (§8, le défaut payé trois fois) :
     l'observateur ne se réveille qu'une fois par chargement. La porte de l'Aura, elle, est
     traversée à chaque ouverture — on s'y accroche AUSSI, et `ouvre()` compare avant d'agir. */
  try{ var _sb=document.getElementById('souffleBtn');
    if(_sb) _sb.addEventListener('click', function(){ try{ ouvre(); }catch(_){} }, false); }catch(_){}
  /* on s'accroche à la classe `show` — un observateur QUI COMPARE AVANT D'AGIR (§8) */
  var _vu=SC.classList.contains('show');
  try{ new MutationObserver(function(){
      var s=SC.classList.contains('show'); if(s===_vu) return; _vu=s; if(s) ouvre();
    }).observe(SC, {attributes:true, attributeFilter:['class']}); }catch(e){}
  squelette();
  if(_vu) ouvre();

  /* ⚑ Q237 · LES DEUX MOMENTS OÙ PERSONNE NE REGARDE LA SPHÈRE.
     1 · on quitte l'Aura — `closeAll` est le passage obligé, on l'ENVELOPPE (§8 : on
         enveloppe la fonction, on ne se contente pas d'écouter) ;
     2 · l'onglet passe en arrière-plan.
     Dans les deux cas on applique la vise ET on rebâtit, pour que le semis du nouveau
     palier soit prêt avant le prochain regard. Le changement de palier refait tout le
     semis (76 à 80 % des pixels) : c'est précisément pour cela qu'il se fait ici. */
  function auRetrait(){
    try{ if(applique()) prepare(); }catch(e){}
  }
  /* ⚑ 21 sept. — LES ÉTATS BASCULENT AVEC LE THÈME, DONC ILS SE REPEIGNENT QUAND IL CHANGE.
     `eta()` est lue À LA CONSTRUCTION de la légende et des arcs ; sans ceci, un changement de
     thème laissait les valeurs de l'ancien mode (mesuré : les profondes en sombre). On ne
     rebâtit pas l'écran — on repeint les trois pastilles et les arcs, en place. */
  var _clAv=null;
  function reteintSiBesoin(){ var c=clair(); if(c===_clAv) return; _clAv=c; reteint(); }
  function reteint(){
    try{
      var E=eta(), i=0;
      SC.querySelectorAll('.au-lg i').forEach(function(p){ if(E[i]) p.style.background=E[i][1]; i++; });
      SC.querySelectorAll('.au-nb path.au-arc').forEach(function(p){
        var z=p.getAttribute('data-z'); if(z!=null && E[+z]) p.setAttribute('stroke', E[+z][1]);
      });
    }catch(e){}
  }
  try{
    var _dv=document.getElementById('device');
    if(_dv){ var _cl=_dv.classList.contains('light');
      new MutationObserver(function(){
        var c=_dv.classList.contains('light'); if(c===_cl) return;   /* on compare avant d'agir (§8) */
        _cl=c; reteint();
      }).observe(_dv,{attributes:true,attributeFilter:['class']}); }
  }catch(e){}
  window._auraReteint=reteint;
  /* ⚑ 20 sept. — LE SOL SUIT LA PALETTE, DONC LA FOURRURE SE REPEINT QUAND ELLE CHANGE.
     La couleur du sol n'est PAS dans la clé de cache du peintre (`S.__stCle`) : c'est
     pourquoi `regleSol` la remet à null. On fait pareil au changement de palette — et on
     ENVELOPPE `onPaletteChange` (§8 : on enveloppe la fonction, on ne se contente pas
     d'écouter), parce que le moteur l'appelle de trois endroits. */
  try{
    var _opc=window.onPaletteChange;
    window.onPaletteChange=function(){
      var r = (typeof _opc==='function') ? _opc.apply(this, arguments) : undefined;
      try{ for(var N in SEMC) if(SEMC[N]) SEMC[N].__stCle=null; }catch(e){}
      return r;
    };
  }catch(e){}
  try{
    var _ca=window.closeAll;
    if(typeof _ca==='function'){
      window.closeAll=function(){ var r=_ca.apply(this,arguments); try{ auRetrait(); }catch(e){} return r; };
    }
  }catch(e){}
  try{ document.addEventListener('visibilitychange', function(){ if(document.hidden) auRetrait(); }); }catch(e){}
  window._auraApplique = auRetrait;
})();

