
/* ═══════════════════════════════════════════════════════════════════════════════════════
   S1-B · LE MOTEUR GÉOMÉTRIQUE (PROMI-SPECIFICATIONS.md §2 et §4) + LES COTES (§5).
   Rien n'est estimé : l'onde vient de la formule, les cotes de l'inventaire.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  var W=390;
  var NATCOL ={promi:'#82AEF8',chiche:'#FFB8D2',nuee:'#C9A8F5'};   /* §1.1 */
  var NATCLAIR={promi:'#C4A2F5',chiche:'#F5AC9E',nuee:'#C9A8F5'};  /* §1.2 — les LIBELLÉS sur un corps SOMBRE */
  /* ⚑ §2.1 bis — LE TRAIT SUR UN CHAMP PLEIN, repris le 18 septembre 2026 (Tom).
     « Les teintes claires du §2.1 bis sont mortes : Δlum 1,6 sur le Promi et 5,0 sur le Chiche.
       Ce sont des compagnons dessinés pour des champs saturés qui n'existent plus. »
     ⚠ DEUX RÔLES VIVAIENT SOUS UN SEUL NOM. `NATCLAIR` servait le TRAIT (les deux thèmes) ET les
       libellés posés sur le corps sombre. Le second a besoin d'une teinte CLAIRE ; le premier, sur
       un champ devenu pastel, a besoin de l'inverse. On sépare au nom, jamais à la valeur.
     LA NUÉE MONTRAIT DÉJÀ LA RÉPONSE : sa « teinte claire » est le VIOLET, un ton SOMBRE — et sa
       valeur ici était #C9A8F5, c'est-à-dire LE CHAMP LUI-MÊME : le trait d'une Nuée avait la
       couleur du fond qu'il traverse.
     Mesuré, trait contre son champ :
        Promi   #C4A2F5 → #022140   Δlum 1,6 → 58,3   ΔE 24,2 → 61,2
        Chiche  #F5AC9E → #3D0F23   Δlum 5,0 → 69,6   ΔE 21,8 → 69,8
        Nuée    #C9A8F5 → #291547   Δlum 0   → 61,8   ΔE  0   → 62,3 */
  var NATTRAIT={promi:'#022140',chiche:'#3D0F23',nuee:'#43291C'};
  var TERRA='#DD4D23', MENTHE='#8FE08F', CREME='#F7F0DE', ENCRE='#201908';
  /* ⚑ v7 — LES DEUX ÉTATS SOMBRES ET LEURS CLAIRS. Le trait borne le champ et le corps :
     sur un corps sombre il prend le clair, sur un corps clair il prend le sombre. */
  /* ⚑ 21 sept. (Tom) : « l'amande n'est PAS la valeur claire de tenu. Elle sert uniquement
   à l'animation de célébration. » Le « tenu » a donc SA claire, comme l'« en cours » :
   #33BA6C — même transport que le couple validé (ΔL +49, ΔC +34, teinte gardée), et
   ΔE 60 de son plein, exactement comme #291547 → #A77CF7. */
/* ⚑ 21 sept. — LE PAYSAGE D'UNE FICHE TENUE (moodboard v8, Tom). Le corps est LA TERRE,
   prune sombre #2B1020 ; la ligne d'horizon est LA CRÊTE #0B4A2A. Ni l'une ni l'autre ne
   bascule : la terre est une surface d'exception. Mesuré — crête sur terre ΔE 51,3 (plancher
   15, §3 corrigé) ; crête sur les trois champs ΔE 77 · 81 · 86. */
/* ⚑ 22 SEPTEMBRE 2026 (Tom) — TROIS VALEURS D'ÉTAT, EXACTEMENT CELLES-LÀ, PARTOUT.
   « Aucune teinte dérivée, aucun calcul, aucune transformation. » Les deux CLAIRES que
   j'avais construites (#33BA6C, #A77CF7) sortent : c'étaient des dérivées.
   TENUCLAIR et ENCOURSCLAIR restent DÉCLARÉES, égales à leur pleine, pour que le code qui
   les appelle n'ait pas à changer de forme — et pour qu'on voie qu'il n'y a plus qu'une valeur. */
var TENU='#00341A', TENUCLAIR='#00341A', CRETE='#0B4A2A', TERRE='#2B1020', AMANDE='#8FE08F', ENCOURS='#291547', ENCOURSCLAIR='#291547';
/* ⚑ v29 (Tom, Q310) — UN TEXTE D'ÉTAT « EN COURS » : #291547 sur un fond clair, la CRÈME sur un fond sombre (Q290.3).
   Posé ici, à la source, pour les trois textes ensemble : sans cela une passe de lisibilité retirait l'inline en sombre
   et le mot du trait héritait d'une SECONDE crème (#F3E7D1, la crème de panneau) — l'isolé de Q310. */
var CREMEETAT='#F7F0DE';
  function etatTrait(k,light){return light?(k==='encours'?ENCOURS:TENU):(k==='encours'?ENCOURSCLAIR:TENUCLAIR);}

  /* ── §2.1 · L'ONDE. Un seul sinus, 1,5 période, plus une montée vers la droite. ── */
  /* ⚑ LA PÉRIODE N'EST PAS LA MÊME SUR UNE FICHE ET SUR UNE CARTE.
     §2.1 : une fiche fait **1,5** période sur ses 390 px. §3.9 : une carte en fait **1**.
     `onde` clouait 1,5 pour tout le monde, et `peintCarte` l'appelait tel quel : la vague
     d'une carte d'Index était celle d'une fiche, comprimée. Mesuré sur le cadre 72,
     carte 1 (« planter un arbre ») — la loi contre ce que l'app peignait :

         x        2    38    74   110   146   158
         loi   102,3  94,4  98,6 106,8 104,3 100,9      min à x=41, max à x=124
         app   102,0  96,0  94,0  98,0 104,0 105,5      min à x=68, max à x=165

     écart médian **2,85 px**, maximal **9,25** — un trait à la bonne place avec la
     mauvaise courbe, exactement ce que le §4 bis annonçait.
     On ajoute un troisième paramètre, par défaut 1,5 : la fiche ne bouge pas d'un pixel. */
  function onde(base,amp,per,larg){ if(per==null) per=1.5; if(!larg) larg=W;
    var mont=amp*0.34, a=amp*0.62;
    return function(x){ var t=Math.max(0,Math.min(1,x/larg)); return base - mont*t - a*Math.sin(2*Math.PI*per*t); }; }
  function pente(y){ return function(x){ return y(x+0.5)-y(x-0.5); }; }
  /* Bézier cubique, un segment par quart de période, tangentes exactes du sinus. */
  function chemin(g,y,x0,x1){ var seg=W/6, xs=[x0], k=Math.ceil(x0/seg)*seg, d=pente(y), i;
    while(k<x1-0.5){ xs.push(k); k+=seg; } xs.push(x1);
    g.moveTo(xs[0],y(xs[0]));
    for(i=0;i<xs.length-1;i++){ var a=xs[i],b=xs[i+1],h=(b-a)/3;
      g.bezierCurveTo(a+h, y(a)+d(a)*h, b-h, y(b)-d(b)*h, b, y(b)); } }
  /* §2.3 · L'amorce effilée : la courbe décalée perpendiculairement de ±épaisseur/2. */
  function ruban(g,y,x0,x1,e0,e1){ var n=44, haut=[], bas=[], d=pente(y), i;
    for(i=0;i<=n;i++){ var x=x0+(x1-x0)*i/n, e=(e0+(e1-e0)*(i/n))/2, dd=d(x), L=Math.sqrt(1+dd*dd);
      haut.push([x-dd/L*e, y(x)+e/L]); bas.push([x+dd/L*e, y(x)-e/L]); }
    g.beginPath(); g.moveTo(haut[0][0],haut[0][1]);
    for(i=1;i<haut.length;i++) g.lineTo(haut[i][0],haut[i][1]);
    for(i=bas.length-1;i>=0;i--) g.lineTo(bas[i][0],bas[i][1]);
    g.closePath(); }
  function chevron(g,y,cx,col,ep){ var ang=Math.atan2(y(cx+8)-y(cx-8),16), k=ep/10;
    g.save(); g.translate(cx,y(cx)); g.rotate(ang);
    g.beginPath(); g.moveTo(-7*k,-10*k); g.lineTo(6*k,0); g.lineTo(-7*k,10*k);
    g.lineWidth=6*k; g.lineCap='round'; g.lineJoin='round'; g.strokeStyle=col; g.stroke(); g.restore(); }

  /* ── LE VIDE EST UN DÉFAUT DU PLANCHER (décision Tom corrigée, 19 août 2026) ──
     ⚠ LIRE CECI AVANT DE TOUCHER À `champ()` OU À `couvre()`.
     La première formulation — « la matière remplit tout le champ, PARTOUT » — était trop
     large, et je l'ai appliquée trop large. **Relevé sur `promi-nuee-toile.html` :
     l'espace entre le bas des dalles et le trait est CORRECTEMENT OCCUPÉ jusqu'à trois
     éléments** (cadres 0 à 6). Le vide n'apparaît qu'à partir de « Quatre », c'est-à-dire
     **dès que le trait touche son plancher** : là, un bandeau de couleur nue se creuse dans
     les ventres de l'onde (mesuré sur les cadres 8 et 10 de la planche).
     LA RAISON, et elle dit où chercher ailleurs : au plancher, `base` cesse de descendre
     pendant que le NOMBRE d'éléments continue de monter. La Toile d'une Nuée tire sa taille
     de ce nombre (`sp = √(W·H/n)`) : ses dalles rapetissent, la vague ne bouge plus, le vide
     se creuse. Sur une fiche et sur la page +, au contraire, la boîte de la dalle est
     CALCULÉE À PARTIR DE LA BASE (`dh = base − amp − 100`) : le rapport entre la matière et
     la vague ne se dégrade jamais, quelle que soit la base. C'est pour ça que le défaut est
     propre à la Nuée — et pour ça qu'on ne remplit qu'AU PLANCHER.
     `champ()` et `couvre()` restent le moyen ; ce qui change, c'est QUAND on s'en sert. ── */
  /* ── LA MATIÈRE REMPLIT LE CHAMP, AU PLANCHER ──
     La matière — la dalle, ou la Toile d'une Nuée — va DU HAUT DE L'ÉCRAN jusqu'à LA VAGUE
     qui la borne en bas. Jamais une bande à mi-hauteur laissant un large vide de couleur de
     nature au-dessus de l'onde. C'est la règle déjà écrite pour l'encart d'une Nuée
     (PROMI-SPECIFICATIONS.md §10.7 : « le masque est le champ lui-même, jamais un rectangle :
     la Toile passe sous le bandeau en haut et se termine sur la vague en bas, jamais sur une
     ligne droite ») — elle vaut PARTOUT : fiches, page +, Nuée, dans les deux thèmes.
     Le champ garde sa couleur de nature DESSOUS : là où la matière ne couvre pas — les coins,
     le pourtour de la silhouette, les creux du monde — on voit la nature, jamais du vide.
     ⚠ Les cadres du moodboard qui montrent une dalle centrée sur un large vide sont une
     ERREUR DE DESSIN (notée dans ECARTS-MOODBOARD.md), pas une règle. */
  /* LE FOND DU CHAMP — le point le plus BAS de l'onde. La matière descend jusque-là ;
     ce qui dépasse est découpé par le chemin de l'onde, jamais par une ligne droite.
     ⚠ Essayé et rejeté : borner la matière au point le plus HAUT de l'onde
     (`base − 0.62 × amp`, la ligne des graines du §10.7). La silhouette de la dalle remonte
     alors et laisse RÉAPPARAÎTRE le vide de couleur de nature au-dessus de la vague — très
     exactement ce que la décision du 19 août interdit. Mesuré au duo, deux thèmes. */
  function fondChamp(y){ var m=0,x; for(x=0;x<=W;x+=2){ var v=y(x); if(v>m) m=v; } return m; }
  /* le masque : le champ lui-même — tout ce qui est AU-DESSUS de l'onde, et rien d'autre. */
  function champ(g,y,dessine){ g.save();
    g.beginPath(); chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath(); g.clip();
    try{ dessine(fondChamp(y)); }catch(_){ }
    g.restore(); }
  /* la couverture : la source remplit la boîte du champ sans se déformer, centrée. `k` la
     recompose plus grande (l'instant d'une parole tenue, §6 du moodboard). */
  /* ⚑ v29 — LA COUVERTURE SANS AGRANDISSEMENT : `couvreId` demande au moteur la dalle À LA TAILLE qui couvre le
     champ, et la pose 1:1 au centre (redteam_decoupe). `couvre(src)` reste pour les appelants qui n'ont pas d'id. */
  function couvreId(g,id,H2,k,o){ var D=window.Toile&&Toile.dalleAbs&&Toile.dalleAbs(id); if(!D||!D.w) return null;
    k=k||1; var T=g.getTransform(), sx=Math.hypot(T.a,T.b)||1, r=D.h/D.w;
    /* ⚑ v55 (Tom : « Madrure — les dalles des fiches apparaissent trop grosses, elles prennent tout le tour de l'écran ») —
       couvrir le champ, pour un monde qui remplit, c'est de la MATIÈRE qui s'étend ; pour Madrure, la dalle est un ŒIL : le
       couvrir, c'était le grossir jusqu'à déborder de l'écran. Madrure se pose dans sa boîte, centrée, comme ailleurs. */
    try{ if(Toile.getTheme&&Toile.getTheme()==='madrure'){ var bw=W*k*0.56, bh=H2*k*0.62, cvm=window._rendDalle(id, bw*sx, bh*sx, o); if(!cvm) return null;
      window._poseUn(g, cvm, W/2, H2*0.5); return cvm; } }catch(_m){}
    var tw=Math.max(W*k, H2*k/r)*1.04;
    var cv=window._rendDalle(id, tw*sx, tw*r*sx*1.6, o); if(!cv) return null;
    if(cv.height/sx < H2*k){ cv=window._rendDalle(id, tw*sx*(H2*k)/(cv.height/sx)*1.02, 1e5, o)||cv; }
    window._poseUn(g, cv, W/2, H2/2); return cv; }
  function couvre(g,src,H2,k){ if(!src||!src.width) return;
    if(typeof src==='object' && src.__id!=null) return couvreId(g, src.__id, H2, k, src.__o);
    k=k||1; var r=src.height/src.width, dw=W*k, dh=W*k*r;
    if(dh<H2*k){ dh=H2*k; dw=H2*k/r; }
    /* centrée sur la boîte du champ : elle déborde en haut ET en bas, et c'est le chemin
       de l'onde qui la borne — la matière touche donc la vague sur toute la largeur. */
    g.drawImage(src, (W-dw)/2, (H2-dh)/2, dw, dh); }

  /* ── §5 · L'ÉCRAN : quel inventaire s'applique à ce Promi ? base et amp sont figés
       par écran (§2.4 bis) ; ils ne se déduisent pas, ils se lisent. ── */
  function ecran(dp,p){
    var light=!!(document.getElementById('device')||{classList:{contains:function(){return false;}}}).classList.contains('light');
    var n = dp.classList.contains('dp-chiche')?'chiche'
          : ((dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'))?'nuee':'promi');
    /* §2.1 bis — DEUX couleurs, à ne pas confondre :
       · LE TRAIT est posé SUR le champ plein. Il prend toujours la TEINTE CLAIRE de la
         nature, « dans les deux thèmes » : la couleur pleine y serait du ton sur ton. C'est
         aussi ce que fait le code de référence §4 (`c = CLAIR[nat]`).
       · LES LIBELLÉS (à-qui, état, mot de trace) sont posés sur le CORPS. L'inventaire §5
         les donne en teinte claire en sombre, en couleur PLEINE de la nature en clair.
       Les cadres clairs du moodboard peignent le trait en couleur pleine : c'est le cas que
       §2.1 bis interdit explicitement — on suit le document. Voir QUESTIONS.md S1-B/Q4. */
    var clair = NATTRAIT[n];                       /* le trait, dans les deux thèmes (§2.1 bis) */
    var clairTexte = light ? (window._NATTXT[n]||NATCOL[n]) : NATCLAIR[n];   /* les libellés, sur le corps */
    /* ⚑ LE TRAIT DESCEND DE 24 — LA DALLE RESPIRE. Décision Tom, 2 septembre 2026 :
       « par défaut il faut abaisser le niveau du trait pour agrandir l'espace de
       visualisation de la ou des dalles (selon nombre d'éléments sous le trait) […] tu as
       de l'espace sous le trait ».
       MESURÉ, la place libre entre le dernier élément et la barre Peaufiner, par état :

           à tenir 133 · Promi tenu 91 et 56 · Chiche tenu 97 · en cours 36 · Chiche 36

       Le pire cas commande : **+24**, qui laisse encore 12 px sur les états « en cours »,
       les plus chargés (ils portent `.dpm-rep` en plus). Un delta plus large tiendrait sur
       une fiche à tenir et écraserait une fiche en cours — et le §8 interdit de dériver
       cette cote d'une mesure, qui la ferait osciller. C'est donc une constante, prise sur
       le minimum, et la zone de dalle passe de 226 à 250 px. */
    var e={nat:n, light:light, natCol:NATCOL[n], clair:clair, clairTexte:clairTexte,
           aplat:true, mode:'moitie', base:286, amp:36, trace:null,
           /* 2 · UN CRAN PLUS GROS (décision Tom, 29 août) — « À Rachel », le titre et la
                ligne d'état sont ce que la fiche raconte. Un cran, pas plus : 21→23,
                38→42, 12,5→13,5. Vaut pour toutes les fiches et toutes les natures. */
           quiFs:23, titreFs:42, etatFs:13.5};
    var tenu = p && p.status==='tenu';
    var chiche = (n==='chiche'), duo = chiche && p && p.avec;
    var aMot = !!(p && p.note && (''+p.note).trim()) || !!(p && p.comments && p.comments.length);
    if(p && p.draft){                                   /* Gardé de côté (§5) */
      /* ⚠ UN CHAMP BLANC N'EXISTE JAMAIS — décision Tom, 29 août 2026, sans exception.
         « Le champ porte toujours sa couleur pleine de nature. Bleu pour un Promi,
         framboise pour un Chiche, mauve pour une Nuée. Dans les deux thèmes, sur tous les
         écrans. La dalle se pose dessus, jamais à la place. »
         J'avais lu Q83 de travers : « un gardé de côté n'a pas de DALLE » ne dit rien du
         CHAMP — et Tom l'écrivait dans la même phrase, « sa carte d'Index garde le champ de
         nature en pointillé, SANS MATIÈRE ». Ce qui manque à un gardé de côté, c'est la
         matière, jamais la couleur. Ce qui le distingue : son trait en points, et le vide
         là où la dalle se poserait. */
      e.aplat=true; e.sansMatiere=true;
      e.mode='points'; e.col=NATCOL[n]; e.colTexte=(light?(window._NATTXT[n]||NATCOL[n]):NATCOL[n]); e.noyaux=false;
      e.trace = (n==='promi')?'trace pour planter':'trace pour lancer';
      e.qui='Gardé de côté';
    } else if(duo && tenu){                             /* Chiche · tenu à deux */
      e.base=396; e.amp=36; e.mode='duo'; e.col=CRETE; e.colTexte=TENUCLAIR;   /* 372 + 24 · la crête sur la terre */
    } else if(tenu){                                    /* Promi · tenue / Avec commentaires */
      e.mode='complet'; e.col=CRETE; e.colTexte=TENUCLAIR;   /* la crête sur la terre */
      if(aMot){ e.base=286; e.amp=36; e.carte=true; } else { e.base=400; e.amp=36; }  /* +24 */
    } else if(chiche && !duo){                          /* Chiche · lancé — rien n'est dû */
      /* ⚑ v29 (Tom, Q310) : « LANCÉ » suit la règle des états, comme un Promi en cours. Le trait garde sa nature. */
      e.col=clair; e.colTexte=(light?ENCOURS:CREMEETAT); e.trace=(p&&p.who?p.who:'elle')+' tracera sa part si elle ose';
    } else if(p && p.status==='rate'){                  /* à tenir · Chiche relevé */
      /* ⚑ 22 sept. (Tom) : « à tenir » s'écrit #DD4D23, dans les deux thèmes — il tombait
         à l'encre en mode clair. Mesuré : Δlum 65 sur la crème, il s'y lit. */
      e.col=TERRA; e.colTexte=TERRA; e.trace='trace pour tenir';
      if(duo) e.quiFs=21;   /* le duo suivait 19, il suit 21 — même cran */
    } else {                                            /* en cours */
      /* ⚑ 22 sept. (Tom) : le LIBELLÉ d'état s'écrit #291547 — c'est un état qui paraît.
         Le TRAIT, lui, garde la teinte de la nature : sur une fiche « en cours » il est à
         moitié tracé, et c'est l'autre qui viendra le finir (§2.6) — ce n'est pas un état. */
      e.col=clair; e.colTexte=(light?ENCOURS:CREMEETAT); e.trace='trace pour tenir'; e.champ=true;
    }
    /* §2.4 bis · la boîte SVG. §2.7 · la dalle : centrée, jamais au-dessus de 88,
       jamais à moins de 12 du trait. */
    /* LE PLANCHER (§2.5) : la borne basse de la base d'une fiche de promesse. C'est LUI qui
       dit si la matière doit remplir le champ (voir la doctrine près de `champ()`). */
    e.plancher = 196; e.auPlancher = (e.base <= e.plancher);
    e.boite = e.base + e.amp + 40;
    /* ⚑ LA DALLE COMMENCE SOUS LE PLATEAU — 124, PAS 88. Signalé par Tom, capture à
       l'appui : « les dalles apparaissent superposées et sous le bandeau du titre et
       ✕ fermer ; elles sont tronquées et cachées car elles passent dessous ».
       Il avait raison au pixel : la dalle démarrait à **88** et le plateau descend à
       **100** — douze pixels de matière passaient dessous PAR CONSTRUCTION, sur toutes
       les fiches. Le 88 datait d'un temps où l'entête n'était pas une boîte.
       Elle démarre donc à **124** : le bas du plateau plus 24 d'air, le pas du produit
       (le padding du plateau vaut 26). Sa hauteur se recalcule d'autant — c'est une cote
       DÉRIVÉE, pas une constante à côté, sinon elle mordrait sur l'onde. */
    var dh = Math.min(300, (e.base-e.amp) - 124 - 12);
    e.dalle = {h:dh, w:Math.min(320, Math.floor(1.2*dh)), y:124};
    e.dalle.x = Math.floor((W - e.dalle.w)/2);
    /* §5 · les cotes dérivées, relevées sur les 14 inventaires :
       noyau « toi » = boîte + 4 · un noyau de personne 10 px plus bas ·
       le premier bloc texte 124 px sous les noyaux · à-qui +36 s'il y a un mot de trace ·
       titre +30 · état = bas du titre + 26,3. */
    /* ═══ TROIS CORRECTIONS DE DESSIN — décision Tom, 29 août 2026, TOUTES LES FICHES ═══
       1 · LE MOT DU GESTE REMONTE. Il était posé 124 px SOUS les Noyaux ; sa place est
           entre LE TRAIT et les disques, centré. « Sous les disques il n'a plus de sens —
           le geste appartient au trait. » L'ordre devient : trait · mot du geste · disques ·
           à-qui · titre · état. Le mot garde son `text-align:center` (posé plus bas).
       3 · SANS MOT DU GESTE, LE BLOC REMONTE. Sur une fiche tenue il n'y a pas de mot, et
           l'air entre le bas de la vague et les disques était de ~60 px (la vague descend au
           plus bas à `base + 0,62·amp`, la boîte vaut `base + amp + 40`). On resserre de 24,
           pas plus : il reste ~35 px d'air. */
    /* ⚑ LE RYTHME SOUS LE TRAIT SE MESURE DEPUIS LE TRAIT, JAMAIS DEPUIS LA BOÎTE.
       Décision Tom, 3 septembre 2026 : « des problèmes de mise en page sous le trait dans
       les fiches — trace pour tenir trop loin du trait. Harmonise partout. Jamais de
       mauvaises mises en page, de superpositions. »

       LA CAUSE, MESURÉE : tout était posé sur `boite` = base + amp + 40. Ces 40 px sont le
       PADDING DE LA BOÎTE SVG, pas un écart de dessin — et le point bas de l'onde est bien
       plus haut. D'où un trou de **65 px d'encre** entre la vague et le mot du geste, le
       plus grand écart de l'écran, pour le lien le plus serré qui soit : le mot NOMME le
       geste juste au-dessus de lui.

       LE POINT BAS DE L'ONDE EST EXACT, il ne se mesure pas : y(t) atteint son maximum en
       t = 1/2, où sin(3πt) = −1 — une seule fois sur [0,1]. Donc
           yBas = base − amp·0,34·0,5 + amp·0,62 = base + 0,45·amp
       Vérifié : base 286, amplitude 36 → 302,2 ; relevé à l'écran, 302.

       LE RYTHME, DEUX VALEURS ET PAS UNE DE PLUS :
           26  entre deux BLOCS   (le trait, le mot, les disques, l'état, les commentaires)
           20  dans le BLOC DE LA PROMESSE  (à qui · titre)
       Relevé d'encre avant : 65 · 27 · 22,5 · 15 · 30 · 31,5 — un trou et quatre valeurs.
       Après : 26 · 26 · 26 · 20 · 26 · 26. */
    /* ⚠ ET C'EST L'ENCRE DU TRAIT QUI COMPTE, PAS L'ENVELOPPE DU GESTE. Mesuré :
       `#tenirZone` occupe 244 → 362 — les 118 px du §5 — pour un tracé dont l'encre
       s'arrête à `yBas + ép/2` ≈ 307. Cinquante-cinq pixels de marge vide sous le dessin,
       et c'est CELLE-LÀ qui repoussait le mot, pas le trait. Le §5 protège le GESTE —
       « toujours entier, jamais rogné ni superposé » : c'est son TRACÉ qu'on ne recouvre
       pas. Sa marge de touche reste au-dessus en z-index (4 contre 2) : le doigt continue
       d'atteindre le geste, rien ne lui est volé. */
    e.yBas = e.base + 0.45 * e.amp;      /* le point bas de l'onde, exact */
    e.yEncre = e.yBas + 5;               /* + la demi-épaisseur : le bas de l'encre du trait */
    if(e.noyaux===false){ e.yTrace = Math.round(e.yEncre + 25); e.yQui = e.yTrace + 36; }
    else if(e.trace){ e.yTrace = Math.round(e.yEncre + 25);   /* 26 d'encre sous LE TRACÉ */
                      e.yNoyau = e.yTrace + 44;             /* 19 px de texte + 26 d'air */
                      e.yQui   = e.yNoyau + 128 + Math.round(window._encreSup(14).bas + window._encreSup(e.quiFs).haut); }   /* 102 de disques + 26 d'air — ⚑ v102 : + ce que l'agrandissement ajoute à l'encre du nom des Noyaux et de l'à-qui */
    else { e.yNoyau = Math.round(e.yEncre + 27); /* sans mot du geste, les disques suivent */
           e.yQui   = e.yNoyau + 128 + Math.round(window._encreSup(14).bas + window._encreSup(e.quiFs).haut); }
    /* ⚠ L'AIR NE SE FIGE PAS, IL SE CALCULE — décision Tom, 29 août 2026 (soir).
       « Tu as grossi les textes sans reprendre les écarts. » Le 30 du §5 n'est pas un espace :
       c'est **la hauteur du bloc à-qui + l'air**. À 21 px, Bricolage 600 rend 23,1 de haut,
       donc l'air vaut 30 − 23,1 = **6,9**. Passer l'à-qui à 23 sans toucher au 30 a mangé
       2,2 px sur les CINQ états de fiche — mesuré, deux thèmes : 6,9 → 4,7.
       On garde donc l'AIR, et la cote suit la taille. À 21 la formule redonne 30 au dixième :
       le moodboard ne bouge pas, il est seulement écrit dans la bonne unité. */
    /* l'air du bloc de la promesse : 20 d'encre entre l'à-qui et le titre (il valait 15).
       La cote reste écrite dans la bonne unité — « hauteur du bloc + air » — pour qu'une
       taille qui monte ne mange pas l'espace (§8). */
    e.airQui = 11.9;
    e.yTitre = Math.round((e.yQui + e.quiFs*1.10 + e.airQui + window._encreSup(e.quiFs).bas + window._encreSup(e.titreFs).haut)*10)/10;   /* ⚑ v102 : l'air se garde À L'ENCRE — l'agrandissement (v96) avait mangé 6 px ici (7,2 → 1,2) */
    return e;
  }
  window._ficheEcran=ecran;
  /* LES PRIMITIVES DE L'ONDE, exposées pour la SECTION 3 : la page + trace exactement la
     même onde que la fiche (§2.1). On expose, on ne duplique pas — une seule formule d'onde
     existe dans le produit, et c'est celle-ci. */
  /* LE VISAGE (§2.10), exposé lui aussi : cercle de diamètre d, fond = couleur de nature,
     silhouette crème. Une seule construction du visage existe dans le produit. */
  window._visageSvg=function(d, natCol){
    var x0=(d/2-0.30*d).toFixed(2), x1=(d/2+0.30*d).toFixed(2), ye=(0.98*d).toFixed(2);
    return '<span class="pp-visage" style="width:'+d+'px;height:'+d+'px;background:'+natCol+'">'
      +'<svg viewBox="0 0 '+d+' '+d+'" xmlns="http://www.w3.org/2000/svg">'
      +'<circle cx="'+(d/2)+'" cy="'+(0.78*d/2).toFixed(2)+'" r="'+(0.19*d).toFixed(2)+'" fill="#F7F0DE"/>'
      +'<path d="M'+x0+' '+ye+' A'+(0.30*d).toFixed(2)+' '+(0.27*d).toFixed(2)+' 0 0 1 '+x1+' '+ye+' Z" fill="#F7F0DE"/>'
      +'</svg></span>';
  };
  /* ═══ §10.6 · L'ENTÊTE SUIT CE QUI EST PEINT SOUS LUI ═══
     La spécification pose déjà la règle, pour la Toile vide d'une Nuée : « la Toile vide
     étant crème dans les deux thèmes, le mot “Nuée” et “✕ FERMER” passent à l'encre #201908
     — sinon c'est blanc sur blanc ; dès qu'un Promi est planté, le champ redevient mauve et
     ils repassent en crème ». Depuis que LA MATIÈRE REMPLIT LE CHAMP (décision Tom du
     19 août), ce cas n'est plus propre à la Nuée : n'importe quel monde clair peut passer
     sous le mot-marque. On lit donc LE PIXEL RÉELLEMENT PEINT sous chaque élément d'entête
     et on prend, des deux encres du produit, celle qui s'en écarte le plus. Jamais un
     troisième ton : crème #F7F0DE ou encre #201908, comme le §10.6 le dit. */
  /* la couleur déclarée sous le point (x, y), en cotes d'écran 390 : [r,g,b,alpha] */
  function couleurSous(cv, x, y){
    var R0=cv.__matRect;
    if(R0 && cv.__matLum!=null && x>=R0.x && x<=R0.x+R0.w && y>=R0.y && y<=R0.y+R0.h){ var l=cv.__matLum; return [l,l,l,255]; }
    var t=(cv.getAttribute('data-trait')||'').split(','), ch=cv.getAttribute('data-champ');
    if(+t[0]>0 && ch){ var u=Math.max(0,Math.min(1,x/W)), b=+t[0], a=+t[1]||0;
      var yo=b - a*0.34*u - a*0.62*Math.sin(2*Math.PI*1.5*u);
      if(y<yo){ var c=_hex2rgb3(ch); if(c) return [c[0],c[1],c[2],255]; } }
    return [0,0,0,0];
  }
  function _hex2rgb3(s){ s=(s||'').trim(); var m=s.match(/^#([0-9a-f]{6})$/i); if(m){ var n=parseInt(m[1],16); return [(n>>16)&255,(n>>8)&255,n&255]; }
    m=s.match(/\d+(\.\d+)?/g); return (m&&m.length>=3)?[+m[0],+m[1],+m[2]]:null; }
  function enteteLisible(cvId, hote, sel){
    function rend(el){ el.style.removeProperty('color'); el.style.removeProperty('-webkit-text-fill-color');
      [].forEach.call(el.querySelectorAll('*'),function(q){ q.style.removeProperty('color');
        q.style.removeProperty('-webkit-text-fill-color'); q.style.removeProperty('stroke'); }); }
    try{
      var cv=document.getElementById(cvId); if(!cv||!cv.width) return;
      /* ⚠ UN CANEVAS NON AFFICHÉ GARDE SES PIXELS. Sur l'écran des trois choix, #csTrameCv est en
         display:none mais porte encore le champ de la nature d'avant : ✕ passait en crème sur crème
         (12 sept. 2026). Rien n'est peint dessous : on rend les éléments à leur feuille. */
      if(!cv.getClientRects().length || (hote.classList && hote.classList.contains('pp-choix'))){
        (sel||[]).forEach(function(s){ [].forEach.call(hote.querySelectorAll(s), function(el){
          if(!(el.closest && el.closest('.enh'))) rend(el); }); });
        return;
      }
      var g=cv.getContext('2d'); if(!g) return;
      var dev=document.getElementById('device'); if(!dev) return;
      var dr=dev.getBoundingClientRect(); var sc=dr.width/W; if(!sc) return;
      var k=cv.width/W;
      (sel||[]).forEach(function(s){
        [].forEach.call(hote.querySelectorAll(s), function(el){
          /* ⚠ UN ÉLÉMENT POSÉ DANS LE PLATEAU N'EST PAS SUR LA MATIÈRE — Q155.
             Cette passe lit le pixel du CANEVAS sous l'élément. C'était juste tant que
             l'entête était posé à nu sur le champ. Depuis que le plateau est l'entête de
             toute l'app (loi 1), il y a un APLAT OPAQUE entre les deux : le canevas dit
             bleu, le mot est en fait sur du crème, et la passe le peint en crème sur
             crème. Mesuré sur la page + : « Promi » et « ✕ FERMER » à rgb(247,240,222)
             sur un plateau rgb(247,240,222), écart de luminosité 0 — le plateau paraissait
             vide. C'est le même défaut que Q152 sur la fiche, la même cause, la même
             correction. L'encre d'un plateau est l'affaire de `encreUn`, qui suit le CORPS ;
             cette passe-ci ne juge que ce qui est posé sur la matière. */
          if(el.closest && el.closest('.enh')) return;
          var c=getComputedStyle(el); if(c.display==='none'||c.visibility==='hidden') return;
          var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return;
          var x=(r.left+r.width/2-dr.left)/sc, y=(r.top+r.height/2-dr.top)/sc;
          if(x<0||y<0||x*k>=cv.width||y*k>=cv.height) return;
          /* ⚑ v29 — PLUS AUCUN PIXEL RELU SOUS LE TEXTE (redteam_decoupe, famille C : le champ porte une dalle).
             Ce qui est peint sous le point se lit dans ce que le peintre a DÉCLARÉ : la dalle posée (sa boîte réelle,
             sa clarté déclarée par le moteur), sinon l'aplat de nature au-dessus de l'onde, sinon rien. */
          var d=couleurSous(cv, x, y);
          /* RIEN DE PEINT DESSOUS — un gardé de côté n'a pas de champ : on REND l'élément à
             sa règle de feuille. Sans ce retour, l'encre posée sur l'écran précédent restait
             en ligne (`!important`) et suivait l'écran suivant : « FERMER » et le mot-marque
             sortaient à Δ2 sur le corps sombre du cadre 27, mesuré. */
          if(d[3]<200){ rend(el); return; }
          var L=0.2126*d[0]+0.7152*d[1]+0.0722*d[2];
          var enc=(L>140)?ENCRE:CREME;
          el.style.setProperty('color',enc,'important');
          el.style.setProperty('-webkit-text-fill-color',enc,'important');
          [].forEach.call(el.querySelectorAll('*'),function(q){
            q.style.setProperty('color',enc,'important');
            q.style.setProperty('-webkit-text-fill-color',enc,'important');
            if(q.tagName==='svg'||q.tagName==='path'||q.tagName==='line')
              q.style.setProperty('stroke',enc,'important'); });
        });
      });
    }catch(_){ }
  }
  window._enteteLisible=enteteLisible;
  window._onde={onde:onde, chemin:chemin, ruban:ruban, chevron:chevron, W:W,
                fondChamp:fondChamp, champ:champ, couvre:couvre, entete:enteteLisible,
                NATCOL:NATCOL, NATCLAIR:NATCLAIR, NATTRAIT:NATTRAIT, TERRA:TERRA, MENTHE:MENTHE,
                TENU:TENU, TENUCLAIR:TENUCLAIR, CRETE:CRETE, TERRE:TERRE, AMANDE:AMANDE, ENCOURS:ENCOURS, ENCOURSCLAIR:ENCOURSCLAIR, etatTrait:etatTrait,
                CREME:CREME, ENCRE:ENCRE};

  /* ═══ LE TRAIT (§2.6) — l'aplat de nature, la vraie dalle du moteur, puis la ligne. ═══ */
  window._ficheTrait=function(){ try{
    var dp=document.getElementById('detailPoster'); if(!dp||!dp.classList.contains('show')) return;
    if(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) return;   /* §3 Nuée : plus bas */
    var p=(typeof cur!=='undefined')?cur:null; if(!p) return;
    var cv=document.getElementById('dpTrameCv'); if(!cv) return;
    var e=ecran(dp,p), y=onde(e.base,e.amp), H=e.boite, i;
    var posterW=dp.clientWidth||W, sc=posterW/W, dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
    cv.width=Math.round(posterW*dpr); cv.height=Math.round(H*sc*dpr);
    cv.style.width=posterW+'px';
    cv.style.setProperty('height',(H*sc)+'px','important');
    cv.style.setProperty('opacity','1','important');  cv.style.setProperty('filter','none','important');
    cv.style.setProperty('mix-blend-mode','normal','important');
    cv.style.setProperty('-webkit-mask','none','important'); cv.style.setProperty('mask','none','important');
    cv.style.setProperty('position','absolute','important'); cv.style.setProperty('top','0','important'); cv.style.setProperty('left','0','important');
    cv.style.setProperty('background','transparent','important');
    var g=cv.getContext('2d'); if(!g) return;
    g.setTransform(dpr*sc,0,0,dpr*sc,0,0); g.clearRect(0,0,W,H);
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';

    /* 1 · L'APLAT plein-cadre de NATURE, borné en bas par l'onde. Un gardé de côté n'en a pas. */
    if(e.aplat){ g.beginPath(); chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath();
      g.fillStyle=e.natCol; g.fill(); }
      /* ⚑ LE CHAMP SE DÉCLARE — « un champ blanc n'existe jamais » (décision Tom, 29 août).
         Un contrôle au pixel ne peut pas trancher partout : sur une Nuée VIDE, les graines
         du §10.6 sont crème DANS LES DEUX THÈMES, et elles tombent pile sur la couleur du
         corps. Ce sont pourtant de la MATIÈRE posée sur un champ mauve, pas un champ nu.
         Le peintre, lui, sait ce qu'il a versé : il l'écrit. C'est la doctrine du §7 —
         on compare la COMPOSITION, pas la peinture. */
      try{ cv.setAttribute('data-champ', e.natCol); }catch(_){}

    /* 2 · LA DALLE — la vraie, celle du moteur, NON TEINTÉE : elle porte le monde, jamais la
         nature (CLAUDE.md §4). Opacité 1, aucun voile, aucun mélange (§2.7).
         ⚠ ELLE GARDE SA BOÎTE. Le remplissage plein champ est réservé au PLANCHER (voir la
         doctrine au-dessus de `champ()`), et **aucune base de fiche n'atteint le sien** :
         l'inventaire du §5 donne 262, 372 et 376, le plancher du §2.5 est 196. Mesuré sur
         les huit écrans de la section 1, deux thèmes : `e.auPlancher` est faux partout.
         La condition reste écrite, et elle mordra d'elle-même si une base descend un jour. */
    /* ⚑ v29 — la dalle n'est plus rendue à k = 1 puis agrandie : `src` porte l'id, et le moteur la rend plus bas
       À LA TAILLE de sa boîte (ou de la couverture), avec la rampe de Q30 peinte par lui (redteam_decoupe). */
    var src={__id:p.id, __o:null, width:1};
    /* ⚠ LA MATIÈRE, ELLE, RESTE ABSENTE D'UN GARDÉ DE CÔTÉ (Q83 : rien n'a été promis, donc
       rien n'est posé sur la Toile). C'est la matière qui manque, jamais la couleur du
       champ — voir la note de `ecran()` sur `sansMatiere`. */
    cv.__matRect=null; cv.__matLum=null;   /* v29 · la matière déclarée ne survit pas à l'écran d'avant */
    if(!e.sansMatiere && window.Toile&&Toile.dalleAbs&&Toile.dalleAbs(p.id)){
      /* ⚠ LA TEINTURE N'EST PAS RÉSERVÉE AU PLANCHER — Q30 dit « dans la bande haute d'une
         fiche », pas « quand la matière remplit le champ ». Bornée à `auPlancher`, elle ne
         mordait sur AUCUNE fiche (le commentaire ci-dessus le dit lui-même : « faux
         partout »), et la dalle boîtée restait celle du moteur, non teintée.
         CE QUE ÇA COÛTAIT, mesuré : `Toile.dalleTrame` rend le MÊME id 125 tantôt lavande
         [209,176,255], tantôt bleu [57,84,255] — deux valeurs qui alternent d'un chargement
         à l'autre. Une fois sur deux la dalle sortait donc **bleue sur le champ bleu
         #82AEF8**, écart de luminosité ≈ 0 là où le seuil du §3 est 42 : la fiche était
         vide à l'œil. Trois passages du duo ont donné trois couleurs — lavande, bleu, orange.
         C'est exactement le rouge tournant que Q60 décrivait (« un état de fiche qui changeait
         à chaque tirage de dalle »), et c'est aussi ce qui rend la teinture DÉTERMINISTE :
         remappée sur la rampe du §1.2, la dalle ne dépend plus du tirage du moteur.
         LA FORME NE BOUGE PAS — seule la luminosité est remappée (CLAUDE.md §4, règle 1).
         Restent exclues, comme avant : un gardé de côté (pas d'aplat, Q83) et une fiche à
         photo (Q53). */
      if(e.aplat && !(p&&p.photo)){
        try{ if(window._ppRampe) src.__o={rampe:window._ppRampe(e.nat)}; }catch(_){}
      }
      if(e.aplat && e.auPlancher && !(p&&p.photo)){
        /* Q30 · LA TEINTURE EST BORNÉE À LA BANDE HAUTE — et la bande haute d'une fiche EN
           EST UNE : « dans la bande haute d'une fiche et dans le champ de la page +, et
           NULLE PART AILLEURS, la dalle prend la palette de sa nature » (CLAUDE.md §4,
           décision Tom du 18 août). La fiche ne l'appliquait pas ; tant que la dalle tenait
           dans une petite boîte au milieu du champ, ça ne se voyait pas. Depuis que LA
           MATIÈRE REMPLIT LE CHAMP, une dalle bleue occupe tout un champ framboise —
           « une dalle bleue sur un champ bleu est un bug, pas un parti pris ». On remappe
           donc la LUMINOSITÉ sur les trois teintes de la nature ; LA FORME NE BOUGE PAS,
           c'est toujours la vraie dalle du moteur. Même appel que la page + : un seul site
           de teinture dans le produit. */
        /* (la teinture est déjà passée juste au-dessus, pour les deux cas) */
        champ(g,y,function(H2){ var _cF=couvre(g,src,H2); cv.__matRect={x:0,y:0,w:W,h:H2};
          cv.__matLum=(_cF&&_cF.__dalleInfo)?_cF.__dalleInfo.lum:null; });
      } else {
        var _rF=window._poseDalle(g, p.id, e.dalle.x, e.dalle.y, e.dalle.w, e.dalle.h, src.__o||undefined);
        cv.__matRect=_rF?{x:_rF.x,y:_rF.y,w:_rF.w,h:_rF.h}:null; cv.__matLum=(_rF&&_rF.cv.__dalleInfo)?_rF.cv.__dalleInfo.lum:null;
      }
      /* ⚑ Q74 · LA ZONE DE MATIÈRE EST PUBLIÉE, en unités d'écran 390 du canevas.
         Au plancher la matière occupe tout le champ ; sinon, sa boîte. */
      /* ⚠ LA BASE S'ÉCRIT AVEC LA BOÎTE, TOUJOURS. `#dpTrameCv` est partagé par la fiche
         et la Nuée ; il traînait une base « 390,844 » posée par un autre peintre, et la
         zone de matière d'une Nuée sortait à 59 px de haut au lieu de 194 — un masque
         faux, donc un écart compté à tort. Deux attributs, un seul geste. */
      try{ cv.setAttribute('data-matiere', (e.aplat && e.auPlancher && !(p&&p.photo))
        ? ['0','0',W,H].join(',')
        : [e.dalle.x,e.dalle.y,e.dalle.w,e.dalle.h].join(','));
        cv.setAttribute('data-matiere-base', W+','+H); }catch(_){}
    }

    /* 3 · LA LIGNE (§2.6) : ma moitié 0→195 · complet 0→390 · duo 0→191 et 199→390 ·
         rien de tracé = amorce effilée puis des points. Points = cercles Ø9 tous les 18 px. */
    var col=e.col, ep=10, rr=4.5, esp=18, mid=W/2;
    g.strokeStyle=col; g.fillStyle=col; g.lineWidth=ep; g.lineCap='round'; g.lineJoin='round';
    /* ⚑ LE PINCEAU — la matière du trait de CETTE promesse (Q128), jamais un réglage
       global. Elle remplace le PLEIN et l'AMORCE ; la courbe ne bouge pas. Les douze
       tracés de la planche sont posés sur l'onde du §2.1 (base 560, amplitude 36, vérifié
       à 0,05 px) : `_matiereTrait` reporte leur ligne moyenne sur celle de CETTE fiche et
       découpe à la même abscisse. Le chevron et les points restent ceux du §2.6 — ils
       disent ce qui MANQUE, et cela ne dépend pas du pinceau.
       ⚠ `_matiereTrait` repeint `fillStyle` : on le rend à la couleur d'état avant les
       points, sinon ils sortiraient dans la teinte du dernier remplissage. */
    var _pin='Plein';
    try{ _pin = window.promiPinceau ? window.promiPinceau(p) : 'Plein'; }catch(_){}
    function mat(a,b){ return _pin!=='Plein' && window._matiereTrait &&
      window._matiereTrait(g, _pin, e.base, e.amp, a, b, col); }
    function plein(a,b){ if(mat(a,b)) return; g.beginPath(); chemin(g,y,a,b); g.stroke(); }
    function points(x0){ g.fillStyle=col;
      for(var x=x0;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x),rr,0,6.2832); g.fill(); } }
    /* ⚑ 23 SEPTEMBRE 2026 (Tom) — UN FILET CRÈME SOUS LE TRAIT D'UNE PAROLE TENUE.
       « Sous le trait vert on ne voit pas la différence entre le vert sombre et le pourpre
       du fond en dessous : rajoute un filet liseré fin crème, même épaisseur que ceux
       autour des disques ; partout sous le trait, à la jonction, ça suit le trait. »
       Mesuré : la crête #0B4A2A sur la terre #2B1020, Δlum 15,7 — sous le seuil du §3.
       Le filet crème y est à Δlum 217,3. Il fait 1,4 px, comme celui des disques, et il
       SUIT la courbe : on restroke le même chemin, décalé vers le bas d'une demi-épaisseur
       de trait plus une demi-épaisseur de filet. Il n'est posé QUE sous la crête — c'est
       la seule jonction où deux sombres se touchent. */
    /* ⚑ 23 SEPTEMBRE 2026, second tour (Tom) — « LE CHICHE : IL LUI FAUT LE MÊME FILET
       CRÈME SOUS LE TRAIT QUE LA FICHE PROMI — SANS LUI C'EST DU TON SUR TON ILLISIBLE. »
       Le filet était conditionné à UNE COULEUR (`col === CRETE`), c'est-à-dire à un SEUL
       cas — la crête d'une parole tenue. Or le défaut est celui du §3, pas celui d'une
       couleur : **deux sombres qui se touchent**. Mesuré en mode sombre, sur l'image rendue :
           crête #0B4A2A sur la terre #2B1020      Δlum 15,7   (le cas déjà traité)
           Chiche #3D0F23 sur son corps #201221    Δlum  4,1   ← rien, le trait disparaît
           Promi  #022140 sur son corps #0D1F33    Δlum  0,0   ← le même défaut, invisible
       LA CONDITION DEVIENT DONC UNE MESURE, et c'est la loi du §3 : le filet paraît dès que
       le trait est à moins de **42** de luminosité du corps qui le porte. En mode clair le
       corps est crème : l'écart est énorme, aucun filet ne paraît — par construction.
       ⚠ LE CORPS SE LIT SUR LE RENDU, jamais sur une classe : c'est le premier fond OPAQUE
       au-dessus du canevas, et l'état n'est pas encore posé quand le peintre passe (§8). */
    function _lum3(c){ return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
    function _col3(v){ if(!v) return null;
      var t=String(v).trim();
      if(t.charAt(0)==='#'){ t=t.slice(1); if(t.length===3) t=t[0]+t[0]+t[1]+t[1]+t[2]+t[2];
        if(t.length<6) return null; var n=parseInt(t.slice(0,6),16);
        return [(n>>16)&255,(n>>8)&255,n&255]; }
      var m=t.match(/[\d.]+/g); return (m&&m.length>=3)?[+m[0],+m[1],+m[2]]:null; }
    var _corps=(function(){ try{
        var n=cv.parentNode;
        while(n && n.nodeType===1){ var b=getComputedStyle(n).backgroundColor;
          var a=b.match(/rgba?\([^)]*?,\s*([\d.]+)\)/);
          if(_col3(b) && (!a || parseFloat(a[1])>0.85)) return _col3(b);
          n=n.parentNode; }
      }catch(_){ } return null; })();
    var _tc=_col3(col);
    var _filetVoulu = ((_corps && _tc) ? (Math.abs(_lum3(_tc)-_lum3(_corps)) < 42) : (col === CRETE)) && !(window._sansFiletCercle && window._sansFiletCercle(cv));
    try{ cv.setAttribute('data-filet-trait', _filetVoulu?'1':'0'); }catch(_){}
    if(_filetVoulu){
      /* ⚑ v36 (Tom) — « trop marqué, trop épais, trop vif : c'est une aide subtile, pas un élément » : 0,8 px au lieu
         de 1,4, le crème adouci des filets. Et il ne court que sous ce qui est TRACÉ — sous la moitié non tracée il
         surchargeait ; il est peint AVANT le trait, jusque sous la flèche, qui le recouvre (il passait par-dessus). */
      var _f=0.8, _dy=ep/2 + _f/2;
      function _yb(x){ return y(x) + _dy; }
      g.save(); g.strokeStyle=window._FILET_DOUX||'#F7F0DE'; g.lineWidth=_f; g.lineCap='butt';
      if(e.mode==='complet'){ g.beginPath(); chemin(g,_yb,0,W); g.stroke(); }
      else if(e.mode==='duo'){ g.beginPath(); chemin(g,_yb,0,mid-4); g.stroke();
                          g.beginPath(); chemin(g,_yb,mid+4,W); g.stroke(); }
      /* ⚑ v76 (Tom) — « le liseret dépasse le trait en passant au-dessus : il faut l'arrêter avant ». Il finissait sous la pointe du
         chevron, dans le V ; et sur le ruban effilé des pointillés il gardait un décalage fixe de ep/2 — il se détachait du ruban quand
         celui-ci s'amincit. Il suit maintenant le BORD du ruban (comme la page +) et s'arrête derrière le V (branches arrière à
         cx − 0,7·ep, bout rond 0,3·ep) ; sous un trait plein, juste avant la branche basse (mid − 0,45·ep), qui prend le relais. */
      else if(e.mode==='points'){ var _cxF=W*0.11, _x0=-W*0.03, _x1=_cxF-ep*0.15, _e0=ep*2.2, _e1=ep*0.15, _nn=88; g.beginPath();
        for(var _i=0;_i<=_nn;_i++){ var _x=_x0+(_x1-_x0)*_i/_nn; if(_x>_cxF-ep-4) break; var _e=(_e0+(_e1-_e0)*_i/_nn)/2+_f/2,
            _dd=(y(_x+0.5)-y(_x-0.5)), _L=Math.sqrt(1+_dd*_dd), _px=_x-_dd/_L*_e, _py=y(_x)+_e/_L;
          if(_i===0) g.moveTo(_px,_py); else g.lineTo(_px,_py); }
        g.stroke(); }
      else { g.beginPath(); chemin(g,_yb,0,mid-ep*0.45-4); g.stroke(); }   /* v82 : 1 mm de plus */
      g.restore();
    }
    if(e.mode==='complet'){ plein(0,W); }
    else if(e.mode==='duo'){ plein(0,mid-4); plein(mid+4,W); }
    else if(e.mode==='points'){ var cx=W*0.11;
      /* ⚑ 23 sept. — le trait ne sort plus PAR la pointe du chevron (Q267) */
      if(!mat(-W*0.03, cx-ep*0.15)){ ruban(g,y,-W*0.03, cx-ep*0.15, ep*2.2, ep*0.15); g.fill(); }
      chevron(g,y,cx,col,ep); points(cx+esp*1.3); }
    else { plein(0,mid); chevron(g,y,mid,col,ep); points(mid+esp); }
    /* ⚑ LE PEINTRE DÉCLARE SA COMPOSITION (doctrine du §7). Un contrôle qui veut savoir de
       quelle couleur est la ligne doit l'échantillonner sur le canevas — et pour cela
       connaître L'ONDE. `releve-S5` la codait en dur (base 300, amplitude 44) : dès que
       l'instant n'a pas ces cotes, la sonde lit à côté du trait et rend `null`, ou pire,
       attrape la couleur du champ. Mesuré : six écarts, « la ligne n'est pas menthe (null) »
       et « pas à l'encre (menthe) ». On ne compare pas la peinture, on lit la composition. */
    try{ cv.setAttribute('data-trait', [e.base, e.amp, col, e.mode].join(',')); }catch(_){}
  }catch(err){} };

  /* ═══ LES COTES (§5) — chaque bloc à sa cote absolue. ═══ */
  function pose(el,css){ if(!el) return; for(var k in css) el.style.setProperty(k,css[k],'important'); }

  /* ═══ LES NOYAUX (§2.9 + §2.10) ═══
     DEUX DÉFAUTS CONSTATÉS À L'ŒIL, moodboard à côté (cadres 44/48/52) :
     1 · l'ANNEAU ne remplissait que 80 % de sa boîte — `drawKRing` trace son cercle à
         `KR_R = .33` de la largeur du canevas et l'épaissit de `KR_LW = .14`, soit un
         diamètre peint de 0,80 × la boîte : 63 px là où le §2.9 demande 78. Le juge, lui,
         mesurait la BOÎTE (78 ✓) : il validait un anneau trop petit.
         Correctif : on garde le composant de l'app et on lui passe, LE TEMPS DE L'APPEL, la
         géométrie du §2.9 — diamètre 78 épaisseur 8 (58 / 6 pour une personne) — puis on
         REND les constantes globales telles quelles (l'Aura et _sigBloc n'y voient rien).
     2 · le VISAGE (§2.10), absent de l'app, est posé au centre : tête et épaules calculées. */
  function noyaux(au, natCol){
    if(!au) return;
    au.querySelectorAll('.kring').forEach(function(k){
      var moi = k.classList.contains('kring-moi');
      /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « JE VEUX LES DISQUES DE LA MÊME ÉPAISSEUR DANS
         L'AURA ET DANS LES FICHES, PARTOUT OÙ ILS APPARAISSENT, TOUJOURS PAREIL. »
         L'épaisseur a été montée le 22 septembre (8 → 12, 6 → 9) — mais SEULEMENT dans
         l'Aura (`K.toi.arc` / `K.pers.arc`). Ici elle était restée à 8 et 6 : le même
         objet portait deux cotes, et une troisième dans `window.KR_LW` (0,21). Une seule
         valeur désormais, la cote de l'Aura. */
      var D   = moi ? 78 : 58, EP = moi ? 12 : 9, d = moi ? 48 : 36;
      var w = k.querySelector('.kr-wrap'); if(!w) return;
      /* — l'anneau, à la géométrie du §2.9 — */
      var cv = w.querySelector('.kr-c');
      if(cv && typeof drawKRing==='function'){
        var vr=window.KR_R, vlw=window.KR_LW;
        try{
          var px=Math.round(D*3);                    /* de la résolution : l'anneau reste net */
          if(cv.width!==px){ cv.width=px; cv.height=px; }
          cv.style.setProperty('width',D+'px','important');
          cv.style.setProperty('height',D+'px','important');
          window.KR_R=(D-EP)/2/D; window.KR_LW=EP/D;
          /* ⚑ UN NOYAU SANS RIEN À DIRE N'EST PAS GRIS. §3 : « Jamais de trait neutre ou
             gris. Un filet sans couleur est un défaut. » `drawKRing` peint l'anneau vide
             en `rgba(163,170,196,.34)` — un gris. Le cadre 0 de `promi-nuee-toile`, sur une
             Nuée SANS AUCUN PROMI, l'écrit en `#C9A8F5` : la teinte claire de la nature.
             On la lui passe ; lui seul sait quoi peindre quand il n'y a rien à compter. */
          cv.setAttribute('data-vide', natCol || '');
          drawKRing(cv);
        }catch(_){ }
        finally{ window.KR_R=vr; window.KR_LW=vlw; }
      }
      /* — le visage (§2.10) — */
      var v = w.querySelector('.s1b-visage');
      if(!v){ v=document.createElement('div'); v.className='s1b-visage'; w.appendChild(v); }
      var x0=(d/2-0.30*d).toFixed(2), x1=(d/2+0.30*d).toFixed(2), ye=(0.98*d).toFixed(2);
      v.style.setProperty('width',d+'px','important'); v.style.setProperty('height',d+'px','important');
      v.style.setProperty('background',natCol,'important');
      v.innerHTML='<svg viewBox="0 0 '+d+' '+d+'" xmlns="http://www.w3.org/2000/svg">'
        +'<circle cx="'+(d/2)+'" cy="'+(0.78*d/2).toFixed(2)+'" r="'+(0.19*d).toFixed(2)+'" fill="#F7F0DE"/>'
        +'<path d="M'+x0+' '+ye+' A'+(0.30*d).toFixed(2)+' '+(0.27*d).toFixed(2)+' 0 0 1 '+x1+' '+ye+' Z" fill="#F7F0DE"/></svg>';
    });
  }
  window._ficheCotes=function(){ try{
    var dp=document.getElementById('detailPoster'); if(!dp||!dp.classList.contains('show')) return;
    if(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) return;
    var p=(typeof cur!=='undefined')?cur:null; if(!p) return;
    var e=ecran(dp,p), main=document.getElementById('dpMain'); if(!main) return;
    var encre = e.light ? ENCRE : CREME;
    /* ⚑ v7 — LE CORPS D'UNE FICHE TENUE EST LE BRUN SURFACE #6B4630, dans les DEUX thèmes
       (Tom, 20 sept. 2026 : c'est la surface qui manquait au vert, Q217). Sur un aplat
       sombre l'encre s'inverse (§3) : le texte passe crème et les libellés d'état prennent
       l'amande. Mesuré sur #6B4630 : crème Δlum 163,9 · amande 124,7 · encre 51,0 seulement.
       ⚠ Ces couleurs se posent EN LIGNE avec important (`pose`) : aucune règle CSS ne peut
       les corriger après coup — c'est le piège du §8, et c'est ici qu'il faut écrire. */
    /* ⚑ 21 sept. — sur la TERRE (L* 8,9) le texte passe crème (15,42:1) et les marques
       d'état prennent le CLAIR de « tenu » #33BA6C (Δlum 128,8). L'amande n'est plus un
       état : elle ne sert qu'à l'animation de célébration. */
    if(dp.classList.contains('f-tenue')){ encre = CREME; e.colTexte = TENUCLAIR; }

    /* le mot-marque dit la NATURE regardée (§5) : « Promi », « Chiche », « Nuée ». L'app
       n'écrivait jamais « Chiche » (table NAT, l.5409) — une fiche de Chiche s'annonçait
       « Promi ». Les trois mots sont ceux du vocabulaire (CLAUDE.md §2), rien d'inventé. */
    var mm=document.getElementById('dptNat');
    if(mm) mm.textContent = (e.nat==='chiche') ? 'Chiche' : (e.nat==='nuee' ? 'Cercle' : 'Promi');

    /* le mot de trace : un bloc à part, créé une fois. */
    var tr=document.getElementById('dptTrace');
    if(e.trace){ if(!tr){ tr=document.createElement('div'); tr.id='dptTrace'; main.appendChild(tr); }
      tr.textContent=e.trace;
      pose(tr,{display:'block', top:e.yTrace+'px', color:e.colTexte, '-webkit-text-fill-color':e.colTexte,
               'text-align': (e.noyaux===false?'left':'center')});
    } else if(tr){ pose(tr,{display:'none'}); }

    noyaux(document.getElementById('dAura'), e.natCol);

    /* les Noyaux (§2.9) — le bloc « toi » commence à boîte + 4. */
    var aura=document.getElementById('dAura');
    if(aura){ if(e.noyaux===false){ pose(aura,{display:'none'}); }
      else pose(aura,{display:'block', position:'absolute', left:'24px', top:e.yNoyau+'px',
                      width:'342px', height:'auto', margin:'0', padding:'0', background:'none'}); }

    /* à-qui · titre · état */
    var qui=document.getElementById('dptQui'), ti=document.getElementById('dptTitre'), qd=document.getElementById('dptQuand');
    /* ⚠ LE MOT D'ÉTAT D'UN CHICHE (CASSE C5) : « LANCÉ », pas « EN COURS ». Les trois mots
       sont ceux des cadres 72 à 77 ; la fiche et la carte d'Index se contredisaient. */
    if(qd && e.nat==='chiche'){
      var duo2 = !!(p && p.avec);
      var motC = (p && p.status==='tenu') ? (duo2 ? 'TENU À DEUX' : 'TENUE')
               : (p && p.status==='rate') ? 'À RELEVER' : 'LANCÉ';
      /* le temps s'écrit aussi sur un Chiche — cadre 42 « TENU À DEUX · 3 AOÛT »,
         cadre 52 « LANCÉ · PAS ENCORE RELEVÉ ». */
      qd.textContent = motC + ((p && p.leJour) ? (' · '+(''+p.leJour).toUpperCase()) : '');
    }
    pose(qui,{top:e.yQui+'px', color:e.colTexte, '-webkit-text-fill-color':e.colTexte, 'font-size':e.quiFs+'px'});
    pose(ti ,{top:e.yTitre+'px', color:encre, '-webkit-text-fill-color':encre, 'font-size':e.titreFs+'px'});
    /* ⚠ UN CRAN, SAUF SI LA LIGNE CASSE. Le cran du 29 août (38 → 42) fait passer « le grand
       plongeoir » à DEUX lignes là où le cadre 56 le tient sur une : « ça doit rester
       respirant ». On redescend donc d'un point à la fois jusqu'à ce que le titre tienne sur
       une ligne, plancher 38 — la valeur d'avant le cran. Un titre court garde son cran
       entier ; un titre long n'est jamais plus mal loti qu'avant. Même logique que la carte
       d'Index et que la phrase de la page + : « on prend la plus petite des deux ». */
    if(ti){ var _sc=(dp.clientWidth||W)/W, _fs=e.titreFs;
      while(_fs > 38 && ti.getBoundingClientRect().height/_sc > _fs*1.35){
        _fs -= 1; pose(ti, {'font-size':_fs+'px'}); }
      /* ⚑ v46 (Tom) — UN TITRE LONG TIENT SUR DEUX LIGNES, TROIS AU PLUS, PUIS POINTS DE SUITE. Au plancher de 38 il
         prenait quatre lignes et plus, et passait sous Peaufiner. Un titre court n'est pas touché ; ce qui suit se place
         sur la hauteur réelle du titre (hTitre, plus bas). Ce qu'on a tapé n'est pas modifié : seul l'affichage. */
      var _lg = function(){ var lh = parseFloat(getComputedStyle(ti).lineHeight) || _fs*1.02; return Math.round((ti.getBoundingClientRect().height/_sc) / lh); };
      var _long = (p && p.title) ? String(p.title) : (ti.getAttribute('data-long') || ti.textContent);   /* le titre entier fait foi, jamais l'affichage tronqué */
      if(!ti.querySelector('*') && ti.textContent !== _long) ti.textContent = _long;
      ti.style.setProperty('overflow-wrap','anywhere','important');
      if(_lg() > 2){
        var _ok = false;
        for(var _lim = 2; _lim <= 3 && !_ok; _lim++) for(var _f2 = _fs; _f2 >= 24; _f2--){ pose(ti, {'font-size':_f2+'px'}); if(_lg() <= _lim){ _fs = _f2; _ok = true; break; } }
        if(!_ok && !ti.querySelector('*')){ _fs = 24; pose(ti, {'font-size':'24px'});
          var _lo = 0, _hi = _long.length;
          while(_lo < _hi){ var _md = (_lo + _hi + 1) >> 1; ti.textContent = _long.slice(0, _md).replace(/\s+$/, '') + '\u2026'; if(_lg() <= 3) _lo = _md; else _hi = _md - 1; }
          ti.textContent = _long.slice(0, _lo).replace(/\s+$/, '') + '\u2026'; }
      }
      e.titreFs = _fs; }
    var hTitre = ti ? Math.round(ti.getBoundingClientRect().height/((dp.clientWidth||W)/W)) : Math.round(e.titreFs*1.02);
    /* ⚠ ET ON NE RESSERRE PAS SOUS LE TITRE. J'avais ramené cet écart de 30 à 26 d'encre
       « pour harmoniser » — mais Tom a dit « en cours est TROP PROCHE de la ligne du
       dessus » : le corriger en le rapprochant encore aurait été le contraire de ce qui
       est demandé. `redteam_air` l'a d'ailleurs refusé, dix paires à −4. On garde les 30.
       Le rythme du bas (30 · 31,5) est plus large que celui du haut (26 · 27) : c'est une
       hiérarchie, pas un défaut — serré autour du geste, ample autour de la lecture. */
    var yEtat = Math.round(e.yTitre + hTitre + 26.3);
    /* ⚑ v18 (Tom) — « L'AIR ENTRE LE BAS DU TITRE ET LA LIGNE D'ÉTAT DOIT RESTER LE MÊME, UNE LIGNE OU DEUX.
       MESURE À L'ENCRE. » Mesuré à l'encre : ce n'est pas le nombre de lignes qui changeait l'air, c'est le
       JAMBAGE de la dernière ligne (34,5 sans jambage, 21 à 26 avec un g, un p, un q). La cote partait de la
       BOÎTE du titre. On descend donc l'état de la profondeur d'encre de la dernière ligne sous sa ligne de
       base : l'air à l'encre est le même pour tous les titres. */
    try{ var _jb = (ti && window._jambageDernier) ? window._jambageDernier(ti) : 0; yEtat += Math.round(_jb/((dp.clientWidth||W)/W)) + Math.ceil(window._encreSup(e.titreFs).bas); }catch(_j){}   /* ⚑ v102 : jambage ou pas, l'encre du titre descend de ce que l'agrandissement (v96) lui ajoute — 26,3 était l'air d'avant */
    /* et l'accent d'une capitale (« À », « É ») monte l'encre de la ligne d'état : on le compte aussi */
    try{ if(qd && window._accentHaut) yEtat += Math.round(window._accentHaut(qd, e.etatFs||13.5)); }catch(_a){}
    /* ⚑ v18 (Tom) : la mention TENU est en AMANDE — « TENUE », « TENU À DEUX · 3 AOÛT » (v6 : l'amande porte la
       mention TENU et la célébration). Posée ICI, par le peintre : une règle de feuille perdait contre la passe du
       sombre, qui repeint en crème ce qu'elle trouve en vert profond. */
    var _colQd = (p && p.status==='tenu') ? '#8FE08F' : e.colTexte;
    pose(qd,{top:yEtat+'px', color:_colQd, '-webkit-text-fill-color':_colQd,
             'font-size':(e.etatFs||13.5)+'px'});
    e.yEtat=yEtat; e.hEtat = qd ? Math.round(qd.getBoundingClientRect().height/((dp.clientWidth||W)/W)) : 15;

    /* la zone de message. Trois cas, et trois seulement, dans l'inventaire :
       · « en cours » → LE CHAMP (§3.7) 342×66 rayon 33 contour 3, à état + 42 ;
       · « avec commentaires » → LA CARTE 342×76 rayon 22, fond de carte d'Index (§1.3),
         posée à 23 px sous le titre ;
       · partout ailleurs → rien. Une fiche « à tenir » n'a pas de zone de message. */
    var corps=document.getElementById('dpCorps'), msg=document.getElementById('dpMsg');
    var CARTE={promi:'#183759',chiche:'#351A2D',nuee:'#1B1426'};
    if(e.champ){
      /* même règle : le 42 du §3.7 vaut « hauteur de l'état (12,5 × 1,1 = 13,75) + 28,25
         d'air ». L'état passé à 13,5 mangeait 1,1 px sur le champ de message. */
      /* ⚠ IDEM ICI : on ne resserre pas. Ces 31,5 d'encre sont l'air du bas de la fiche. */
      pose(corps,{display:'block', top:Math.round(yEtat + (e.etatFs||13.5)*1.10 + 28.25 + window._encreSup(e.etatFs||13.5).bas)+'px',   /* ⚑ v102 : + l'encre agrandie de l'état */
                  height:'66px'});
      pose(msg,{height:'66px','border-radius':'33px', border:'3px solid '+e.colTexte,
                background:'transparent', color:encre, '-webkit-text-fill-color':encre});
      /* le chevron « → » du §3.7 est un ::after de la ligne : il hérite de SA couleur, pas
         de celle de la carte. Sans ça il restait vert sombre, illisible. */
      var rep=msg&&msg.querySelector('.dpm-rep');
      pose(rep,{color:encre, '-webkit-text-fill-color':encre});
    } else if(e.carte){
      pose(corps,{display:'block', top:Math.round(e.yTitre+hTitre+23)+'px', height:'76px'});
      pose(msg,{height:'76px','border-radius':'22px', border:'0',
                background:(e.light?'#E9D8B7':CARTE[e.nat]), color:encre, '-webkit-text-fill-color':encre});
    } else if(corps){ pose(corps,{display:'none'}); }

    /* LE GESTE, entier (118 px), calé sur le bas de la boîte du trait : le doigt trace là où
       l'onde passe. Aucun bloc d'inventaire n'occupe cette bande. Sur une parole déjà tenue
       ou un gardé de côté, il n'y a plus rien à tracer. */
    var ge=dp.querySelector('.geste-env');
    if(ge) pose(ge,{display:(p.status==='tenu'||e.noyaux===false)?'none':'block',
                    top:(e.boite-118)+'px', height:'118px'});
  }catch(err){} };

  /* ═══════════════════════════════════════════════════════════════════════════════════
     LA NUÉE (§5 · « Nuée · avec des Promi » et « Nuée · vide »). Même grammaire que les
     autres fiches — aplat de nature, onde, Noyaux, phrase — mais la zone haute porte LES
     DALLES DE SES PROMI, pas une dalle unique, et le corps porte ses cartes.
     trait : base 232 amp 36 (avec des Promi) · base 282 amp 44 (vide) · mode complet.
     ═══════════════════════════════════════════════════════════════════════════════════ */
  function nueeCourante(){
    try{ if(typeof curNuee!=='undefined' && curNuee) return curNuee; }catch(_){}
    return null;
  }
  function promisDeNuee(k){
    try{ return promises.filter(function(p){ return !p.draft && p.nuee===k; }); }catch(_){ return []; }
  }
  function encre0(clair){ return clair ? ENCRE : CREME; }
  window._ficheNuee=function(){ try{
    var dp=document.getElementById('detailPoster'); if(!dp||!dp.classList.contains('show')) return;
    if(!(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'))){
      /* ⚑ LA HAUTEUR D'UNE NUÉE NE SURVIT PAS À LA FICHE SUIVANTE.
         Le fil d'une Nuée défile : `#dpMain` porte sa hauteur en `min-height !important`
         (voir plus bas, « le fil défile »). Rien ne la retirait. Mesuré : on ouvre le
         potager, on le ferme, on ouvre une fiche de Promi — `#dpMain` reste à **1092**
         au lieu de 760, le poster passe à 1176 de haut, et la barre Peaufiner, collante,
         **tombe à y = 1092, hors de l'écran**. La fiche perd sa barre, en silence.
         (Après « l'atelier », vide : 885 — même défaut, 125 px.)
         Les batteries ne le voyaient pas : elles ouvrent une fiche sur une page fraîche.
         C'est le duo, écran après écran, qui l'a sorti — la barre manquait en clair,
         parce que le pas clair vient après le pas sombre, Nuée comprise. */
      var mn0=document.getElementById('dpMain');
      if(mn0 && mn0.style.getPropertyValue('min-height')) mn0.style.removeProperty('min-height');
      var f00=document.getElementById('dpNueeFil');
      if(f00 && getComputedStyle(f00).display!=='none') f00.style.setProperty('display','none','important');
      return;
    }
    var k=nueeCourante(); var liste=k?promisDeNuee(k):[];
    var light=document.getElementById('device').classList.contains('light');
    var natCol=NATCOL.nuee, col=NATTRAIT.nuee, colTexte= light?window._NATTXT.nuee:NATCLAIR.nuee;
    /* ═══ §9 · LA HAUTEUR DU TRAIT — RÈGLE PROPRE À LA FICHE DE NUÉE ═══
       Une fiche de promesse compte ses éléments en LIGNES DE PHRASE, à 32 px :
       base = max(196, 344 − 32(n−1)). Une fiche de Nuée les compte en LIGNES DE FIL, à
       86 px — 74 de hauteur plus 12 d'écart. D'où un pas différent, pour la même idée :

           base = max(176, 460 − 86 n)     n = Promi ET Chiche de la Nuée · amplitude 40

       n = 0 → 460 : le trait est au plus bas de tout le produit, la Toile occupe 435 px.
       Chaque Promi ou Chiche le fait MONTER de 86 px — la hauteur de la ligne qu'il ajoute.
       Plancher 176 : au-delà de trois, le trait ne monte plus, le défilement prend le relais.
       ⚠ L'app portait `232 / 282` et une amplitude de `36 / 44` : deux valeurs qui ne
       viennent d'aucune règle. La fiche de Nuée n'avait jamais été portée. */
    /* ⚑ Q213 · LA RÈGLE NE CHANGE PAS — `n` compte les LIGNES DU FIL, et « Planter dans la Nuée » en est une (la dernière).
       Tom : « c'est le contenu qui s'organise sous elle, jamais l'inverse ». Vide : n = 1, le trait passe de 460 à 374 ;
       pleine : le plancher (176) tient déjà. Mesuré : tous les écarts de la fiche identiques à avant, pleine et vide. */
    var nFil = liste.length + 1;
    /* ═══ §9 · LES DEUX ÉTATS, ET DEUX SEULEMENT ═══
       · POSÉ   — `base = max(176, 460 − 86 n)`, amplitude 40 : la fiche telle qu'elle s'ouvre.
       · DÉFILÉ — **base 58, amplitude 16** : ce n'est PAS une valeur de la formule, c'est
                  LA BUTÉE HAUTE DU DÉFILEMENT. Le champ s'y réduit à une bande de 114 px,
                  juste assez pour que la Toile reste présente sans occuper l'écran.
       ⚠ Le §12 écrit « amplitude = 40 » en tête de l'écran défilé : c'est un report du
         gabarit des autres écrans. Sa boîte de Toile, elle, est donnée à **114** dans le
         tableau — et 58 + 16 + 40 = 114, quand 58 + 40 + 40 ferait 138. Le §9 a raison,
         le tableau le confirme, l'entête se trompe. Noté dans QUESTIONS.md · Q64. */
    var defile = !!window._nueeDefileEtat;
    var basePose = Math.max(176, 460 - 86*nFil);
    var base = defile ? 58 : basePose, amp = defile ? 16 : 40;
    var boite = base + amp + 40, y=onde(base,amp);
    /* ⚑ LA BANDE DE SECOURS SUIT LE HAUT DE LA VAGUE, PAS LA BOÎTE.
       Elle est le fond DERRIÈRE le canevas (§ `lot-NUEE-BANDE`) ; on ne la supprime pas.
       Mais le canevas n'est opaque que jusqu'à L'ONDE, et l'onde est une courbe : au-delà
       de son point le plus HAUT, le canevas laisse voir la bande là où le corps devrait
       commencer. Mesuré sur le potager (base 176, amplitude 40) : la boîte vaut 256, la
       vague culmine à 140 — soit **116 px de mauve à bord franc** sous la vague, une bande
       que le cadre 10 de `promi-nuee-toile` n'a pas, et qui pesait 100 % de différence sur
       les ordonnées 180 à 240 du duo.
       On la borne donc au minimum de l'onde : au-dessus, le canevas couvre tout ; au-
       dessous, c'est le corps. Un seuil, pas une suppression. */
    try{
      var mn = boite;
      for(var _q=0; _q<=64; _q++){ var _v = y(W*_q/64); if(_v < mn) mn = _v; }
      dp.style.setProperty('--nuee-bande', Math.max(0, Math.floor(mn))+'px');
    }catch(_){ }

    /* — le champ, peint sur dpTrameCv comme pour les autres fiches — */
    var cv=document.getElementById('dpTrameCv');
    if(cv){
      var posterW=dp.clientWidth||W, sc=posterW/W, dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
      cv.width=Math.round(posterW*dpr); cv.height=Math.round(boite*sc*dpr);
      cv.style.width=posterW+'px';
      cv.style.setProperty('height',(boite*sc)+'px','important');
      ['opacity:1','filter:none','mix-blend-mode:normal','background:transparent','position:absolute','top:0','left:0']
        .forEach(function(d){ var i=d.indexOf(':'); cv.style.setProperty(d.slice(0,i), d.slice(i+1), 'important'); });
      cv.style.setProperty('-webkit-mask','none','important'); cv.style.setProperty('mask','none','important');
      var g=cv.getContext('2d');
      if(g){
        /* ⚑ v100 — LA BANDE SE PEINT PAR UNE FONCTION, publiée (`window._nueeBande`) : la reprise des dalles sautées au budget
           ne repeint QU'ELLE. Repeindre par `_ficheNuee` reposait toute la fiche 2,5 à 3,4 s après l'ouverture — un toucher sur
           « Planter dans la Nuée » tombait à côté (redteam_nuee_entree 5), et le Peaufiner ouvert rebasculait de constructeur
           (releve-S2). Le corps est celui d'avant, tel quel. */
        var _peintBande=function(){
        g.setTransform(dpr*sc,0,0,dpr*sc,0,0); g.clearRect(0,0,W,boite);
        g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';
        g.beginPath(); chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath();
        g.fillStyle=natCol; g.fill();
        /* ⚑ LE CHAMP SE DÉCLARE (voir la note des autres peintres) — c'est ICI que ça
           compte le plus : sur une Nuée VIDE, les graines crème du §10.6 recouvrent le champ
           et tombent pile sur la couleur du corps. Un contrôle au pixel ne peut pas trancher ;
           le peintre, lui, sait qu'il a versé du mauve. */
        try{ cv.setAttribute('data-champ', natCol); }catch(_){}
        /* les dalles des Promi de la Nuée, aux trois emplacements de l'inventaire.
           Ce sont de VRAIES dalles du moteur, non teintées : chaque Promi garde son monde
           (§2.7 « une Nuée porte les dalles de tous ses Promi, de palettes différentes »). */
        /* ═══ LA TOILE D'UNE NUÉE — LA RÈGLE DU MOTEUR, PAS TROIS EMPLACEMENTS FIGÉS ═══
           §10.7 : « le masque est le champ lui-même, jamais un rectangle : la Toile passe
           sous le bandeau en haut et se termine sur la vague en bas, jamais sur une ligne
           droite ». §11 : **la densité est constante, c'est LA VUE qui zoome** —
           `sp = √(W·H / n)`. Peu de dalles, on est près et elles sont grandes ; beaucoup, on
           s'éloigne et elles rapetissent. C'est la formule du générateur, reprise telle
           quelle : elle donne à la fois la TAILLE des dalles et LEUR NOMBRE à l'écran.

           ⚠ CE QUI ÉTAIT LÀ, ET POURQUOI ÇA NE POUVAIT PAS TENIR. Le code portait trois
           emplacements en dur — `[[30,96,108,86],[150,88,118,94],[278,100,92,74]]` — relevés
           sur le cadre 58, à une base de 232/282. Ils ne dépendaient NI du nombre d'éléments
           NI de la hauteur du champ. Depuis que la base suit le §9 (460 · 374 · 288 · 202 ·
           176), la boîte du champ va de 540 à 256 : les mettre à l'échelle d'un facteur
           unique les chassait hors cadre à faible n — **mesuré : à 1 Promi, 125 abscisses
           sur 125 sans la moindre matière**, le champ entièrement nu. Et les laisser en
           absolu creusait 155 px de vide à n = 1. Aucun des deux ne marche : ce n'est pas
           une échelle qui manquait, c'est LA RÈGLE.

           LES FORMES RESTENT CELLES DU MOTEUR (`Toile.dalleTrame`, échelle 1) — c'est la
           règle 1 du §4, et rien ici ne la touche. Ce qui change est le PLACEMENT, et il
           n'est plus une valeur devinée : il vient de `sp`. Le décalage de chaque dalle est
           tiré de SON ID, jamais d'un hasard : deux rendus de la même Nuée sont identiques.
           Le recouvrement de 1,35 fait que les dalles SE TOUCHENT — §10.5 : « les mondes se
           rencontrent en s'effilochant, jamais en se coupant ». Voir QUESTIONS.md · Q62. */
        (function(){
          /* ═══ §10.6 · L'ÉTAT VIDE — LE SEMIS DE GRAINES ═══
             « La Toile sans promesse est semée de graines grises — `seedGray()` du prototype
             — rendues par le moteur du monde, dans ses tons neutres. […] Sur le champ mauve
             d'une Nuée on emploie les tons crème (`GLIGHT`), DANS LES DEUX THÈMES : les gris
             sombres du prototype y feraient des trous noirs. »
             AUCUNE FORME N'EST INVENTÉE : ce sont de VRAIES dalles du moteur, prises sur la
             Toile de l'utilisateur, **recolorées** à plat dans les cinq tons `GLIGHT` — la
             même mécanique que la teinture mauve d'une bande de Nuée, déjà dans le produit.
             Une graine n'est pas un Promi : le §10.6 le dit — « douze graines : c'est une
             densité de semis, pas un plafond ; il ne préjuge de rien, et surtout pas du
             nombre de Promi ». Elles occupent donc le champ à la densité ordinaire.
             ⚠ Le mot-marque et ✕ FERMER passent à l'encre par eux-mêmes : `_enteteLisible`
             lit le pixel crème peint dessous et choisit l'encre (§10.6, Q59). Rien à coder. */
          var GRAINES=['#FDEBCD','#FAF3E5','#F8E2C2','#FEEED4','#FAE6C7'];
          var vide=!liste.length, semence=liste;
          if(vide){
            try{ semence=promises.filter(function(q){ return !q.draft; }).slice(0,5); }catch(_){ semence=[]; }
            if(!semence.length) return;      /* rien à semer : le champ reste nu, faute de moteur */
          }
          /* §9 · « La Toile qu'on y voit est LA MÊME, simplement remontée de
             `base_posé − 58` : jamais une seconde composition. » On compose donc TOUJOURS
             sur le champ posé, et on translate — le semis ne change pas d'un état à l'autre. */
          var yPose = defile ? onde(basePose,36) : y;
          var monte = defile ? (fondChamp(y) - fondChamp(yPose)) : 0;
          var H2=fondChamp(yPose);
          /* §10.6 · LA DENSITÉ DU SEMIS NE COMPTE PAS LES PROMI. Le document le dit en toutes
             lettres pour la Nuée vide : « douze graines : c'est une DENSITÉ DE SEMIS, pas un
             plafond. Le nombre est choisi pour que le champ soit occupé sans être chargé ; il
             ne préjuge de rien, et surtout pas du nombre de Promi que la Nuée accueillera. »
             Douze graines sur le champ d'une Nuée vide (390 × 435) donnent un pas naturel de
             √(390 × 435 / 12) = 119 px. On sème donc À CETTE DENSITÉ, et jamais moins d'une
             graine par Promi ; les dalles de la Nuée tournent sur les emplacements.
             ⚠ POURQUOI PAS `sp = √(W·H/n)` SEUL, qui est pourtant la formule du §11 : parce
             que le n du §11 est le nombre de GRAINES, pas le nombre de Promi. Pris pour le
             second, il donne UNE seule graine à 1 Promi — une dalle étirée sur 390 × 392,
             cinq fois sa taille native, dont la matière du monde part en bouillie. Relevé au
             duo contre le cadre 2 de la planche, qui montre au contraire un braille NET sur
             tout le champ. La densité du §10.6 remet le facteur d'agrandissement à 2,2. */
          var SP0=Math.sqrt(390*435/12);
          var nMin=Math.max(1, Math.round(W*H2/(SP0*SP0)));   /* la densité, pas un quadrillage arrondi */
          var nD=Math.max(liste.length, nMin);
          var sp=Math.sqrt(W*H2/nD);
          var cols=Math.max(1,Math.round(W/sp)), rows=Math.max(1,Math.round(H2/sp));
          /* ⚠ `k` est déjà la CLÉ de la Nuée dans la fonction englobante : le compteur de
             cases s'appelle `kc`, sinon il l'ombre et `window._nueeSemis.cle` publie un
             numéro de case à la place du nom du groupe. */
          var cw=W/cols, ch=H2/rows, kc=0;
          g.save();
          g.beginPath(); chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath(); g.clip();
          g.translate(0, monte);          /* §9 · la même Toile, simplement remontée */
          /* ⚠ UNE DALLE SE REND UNE FOIS, PAS UNE FOIS PAR CASE. `dalleTrame` refait
             l'attribution pondérée PIXEL PAR PIXEL (voir son code) : l'appeler pour chacune
             des neuf à douze cases, à chaque repeinte, et `_ficheNuee` étant rejoué deux fois
             par pose, l'app s'est mise à ramer au point que `redteam_toile` ne rendait plus
             la main (dix minutes, deux fois). On garde donc le rendu par id, le temps de la
             passe : mêmes pixels, un seul calcul. C'est le piège du §12 de CLAUDE.md. */
          /* ═══ LE SEMIS EST DÉTERMINISTE — ET IL EST OBSERVABLE ═══
             (Exigence Tom, 19 août 2026.) **Même Nuée, même semis : à chaque ouverture, dans
             les deux thèmes, et sur n'importe quel appareil.** Une Toile qui changerait de
             composition entre deux ouvertures ne serait plus la Toile de CETTE Nuée.
             Rien ici ne tire au hasard : le pas vient du nombre d'éléments et de la hauteur
             du champ, le décalage de chaque dalle vient de SON ID et de sa case. Aucun
             `Math.random`, aucune horloge.
             ⚠ CE QUI RESPIRE, ET QUI N'EST PAS LE SEMIS : `Toile.dalleTrame` rend la matière
             du monde avec `performance.now()` — les mondes animés ne redonnent jamais deux
             fois exactement les mêmes pixels. C'est le moteur, c'est vrai partout dans le
             produit, et ce n'est PAS la composition. Un contrôle qui compare les PIXELS d'une
             ouverture à l'autre mesure donc la respiration du monde, pas le semis : il faut
             comparer LE SEMIS, qu'on publie ici pour ça. */
          var _semis=[];
          var _cache={};
          /* ⚑ v100 (Tom : « deux à trois secondes où l'app se fige et où un toucher tombe à côté ») — LE BUDGET, comme Mascaret,
             Chamade et Ramage (v98) : une passe rend au plus ~40 ms de dalles neuves ; au-delà, une case dont la dalle n'est pas
             prête est sautée (le semis ne bouge pas : quelle dalle, quelle case ne dépend pas d'elle) et la bande se repeint à
             l'image suivante. Mesuré avant : ~40 dalles de 20 à 80 ms dans UNE tâche à la 1re ouverture d'une Nuée. */
          var _saute=0, _manque=[]; window._budgetTache();
          /* le rendu d'une case sautée, EXACTEMENT le chemin de `dalleDe` sans budget — fait plus tard, une dalle par tâche */
          function _faire(id, bw, bh, sx, vide){ var D=window.Toile&&Toile.dalleAbs&&Toile.dalleAbs(id); if(!D||!D.w||!window._rendDalle) return;
            if(vide){ window._rendDalle(id, bw*sx, bh*sx); return; }
            var rD=D.h/D.w, tw=Math.max(bw, bh/rD)*1.02, c1=window._rendDalle(id, tw*sx, tw*rD*sx*1.6);
            if(c1 && c1.height<bh*sx) window._rendDalle(id, tw*sx*bh*sx/c1.height*1.02, 1e5); }
          /* ⚑ v29 — la dalle d'une case se rend À LA TAILLE DE LA CASE (semée : elle y tient ; étalée : elle la
             couvre), puis se pose 1:1 (redteam_decoupe). Une taille par case, toutes égales : un rendu par id. */
          function dalleDe(id, ton, bw, bh, vide){
            var sx=Math.hypot(g.getTransform().a,g.getTransform().b)||1;
            var cle=id+'|'+(ton||'')+'|'+Math.round(bw*sx)+'x'+Math.round(bh*sx)+'|'+(vide?1:0);
            if(_cache[cle]!==undefined) return _cache[cle];
            var cv2=null, D=window.Toile&&Toile.dalleAbs&&Toile.dalleAbs(id);
            if(D&&D.w&&window._rendDalle){
              var _lent=window._budgetTache()>40, _op=_lent?{siPret:1}:undefined;
              if(vide){ cv2=window._rendDalle(id, bw*sx, bh*sx, _op); if(!cv2&&_lent){ _saute++; _manque.push([id,bw,bh,sx,vide]); return null; } }
              else { var rD=D.h/D.w, tw=Math.max(bw, bh/rD)*1.02; cv2=window._rendDalle(id, tw*sx, tw*rD*sx*1.6, _op);
                     if(!cv2&&_lent){ _saute++; _manque.push([id,bw,bh,sx,vide]); return null; }
                     if(cv2 && cv2.height<bh*sx){ var _c3=window._rendDalle(id, tw*sx*bh*sx/cv2.height*1.02, 1e5, (window._budgetTache()>40)?{siPret:1}:undefined);
                       if(!_c3&&window._budgetTache()>40){ _saute++; _manque.push([id,bw,bh,sx,vide]); return null; } cv2=_c3||cv2; } }
            }
            var ok=!!(cv2&&cv2.width);
            if(ok && ton){
              /* la teinte d'une graine se pose sur une COPIE 1:1 — le rendu du moteur reste en cache, intact */
              var cp=document.createElement('canvas'); cp.width=cv2.width; cp.height=cv2.height;
              cp.getContext('2d').drawImage(cv2,0,0); cv2=cp;
              /* la graine : la FORME du moteur, le TON du §10.6. `source-in` garde l'alpha
                 de la dalle et remplace la couleur — une graine est un ton neutre, pas une
                 matière de monde ; c'est ce que montre le cadre 0 de la planche. */
              var gx=cv2.getContext('2d');
              if(gx){ gx.globalCompositeOperation='source-in';
                      gx.fillStyle=ton; gx.fillRect(0,0,cv2.width,cv2.height);
                      gx.globalCompositeOperation='source-over'; }
            }
            /* ⚠ ET SURTOUT PAS DE TEINTURE MAUVE ICI — essayé le 29 août, RETIRÉ le même jour.
               `CLAUDE.md §4` écrit que la bande d'une Nuée montre « de vraies dalles, seulement
               teintées mauve » ; j'ai cru la bande fautive parce que « le potager » y montrait
               une dalle ORANGE et une BLEUE. C'était moi qui lisais mal : le cadre 10 de
               `promi-nuee-toile.html` — la planche qui FAIT FOI pour la Nuée — porte lui-même
               un carré orange hachuré, une tache rose et des lignes bleues, et sa page l'écrit
               en titre : « elle porte maintenant SES DALLES, rendues par le vrai moteur de la
               Toile — LES NEUF MONDES du Studio ». Le champ d'une Nuée montre donc les mondes,
               non teintés. Teintée, la bande sortait délavée, presque blanche — mesuré au duo.
               La phrase du §4 vise la BANDE HAUTE d'une fiche de Nuée dans l'ancien dessin, pas
               ce champ-ci. Voir QUESTIONS.md · Q94. */
            return (_cache[cle]= ok?cv2:null);
          }
          for(var r=0;r<rows;r++) for(var c=0;c<cols;c++){
            var p=semence[kc % semence.length];
            var ton=vide ? GRAINES[kc % GRAINES.length] : null;
            kc++;
            /* ⚑ v59 (Tom : « dans la bande haute d'une fiche de Nuée, sous Madrure, les anneaux sont encore très grands ») — une
               dalle de Madrure est l'ŒIL du nœud, pas une matière qui s'étale : agrandie jusqu'à remplir sa case (1,35), elle
               sortait trois fois plus grosse que sur la Toile. Elle garde sa taille relative d'œil — un peu plus de la moitié de
               sa case —, posée sur le champ, comme la fiche d'une parole la pose dans sa boîte (v55). */
            var _oeil = (typeof Toile!=='undefined' && Toile.getTheme && Toile.getTheme()==='madrure');   /* les graines d'une Nuée vide aussi */
            var f0 = _oeil ? 0.58 : (vide ? 1.15 : 1.35);
            var src=dalleDe(p.id, ton, cw*f0, ch*f0, vide); if(!src) continue;
            /* le décalage vient de l'id — déterministe, jamais Math.random */
            var j=((p.id*2654435761)>>>0) ^ ((r*73856093 ^ c*19349663)>>>0);
            var dx=(((j&255)/255)-0.5)*cw*0.34, dy=((((j>>8)&255)/255)-0.5)*ch*0.34;
            /* LE RECOUVREMENT — 1,35 quand la Toile porte des Promi : les dalles SE
               TOUCHENT (§10.5, « les mondes se rencontrent en s'effilochant, jamais en se
               coupant »), et le champ n'a pas de trou.
               UNE GRAINE, ELLE, EST SEMÉE, PAS ÉTALÉE : le cadre 0 de la planche montre des
               taches crème NETTEMENT SÉPARÉES, avec du mauve entre elles. On l'inscrit donc
               dans sa case (1,15, ajustée par le DEDANS) au lieu de l'y étaler. La densité
               reste celle du §10.6 : douze cases sur le champ d'une Nuée vide — relevé. */
            var f = _oeil ? 0.58 : (vide ? 1.15 : 1.35);
            var bw=cw*f, bh=ch*f;
            var bx=c*cw+(cw-bw)/2+dx, by=r*ch+(ch-bh)/2+dy;
            /* semée : elle tient dans sa case · étalée : elle la remplit — déjà à sa taille, posée 1:1 */
            var _ps=window._poseUn(g, src, bx+bw/2, by+bh/2), dw=_ps.w, dh=_ps.h;
            /* LA CASE est le semis : quelle dalle, à quelle place, dans quelle boîte. Elle
               ne doit RIEN devoir ni à l'horloge ni à l'appareil.
               LE RECT PEINT, lui, est la case ajustée au format de la dalle — et ce format
               RESPIRE : `dalleTrame` recadre au plus juste sur l'alpha, que la matière
               animée fait bouger d'un rendu à l'autre. Il est publié pour le voir, jamais
               pour être comparé. */
            _semis.push({id:p.id, r:r, c:c,
                         bx:Math.round(bx*100)/100, by:Math.round(by*100)/100,
                         bw:Math.round(bw*100)/100, bh:Math.round(bh*100)/100,
                         peint:{x:Math.round((bx+(bw-dw)/2)*100)/100,
                                y:Math.round((by+(bh-dh)/2)*100)/100,
                                w:Math.round(dw*100)/100, h:Math.round(dh*100)/100}});
          }
          g.restore();
          /* ⚑ Q74 · LA ZONE DE MATIÈRE EST PUBLIÉE. Sur une Nuée, la matière remplit tout
             le champ, borné par l'onde : la boîte est donc le champ entier. */
          try{ cv.setAttribute('data-matiere', ['0','0',W,H2].join(','));
               cv.setAttribute('data-matiere-base', W+','+boite); }catch(_){}
          /* publié pour le juge : la composition, en coordonnées d'écran 390 */
          window._nueeSemis={cle:k, n:liste.length, vide:vide, base:base, amp:amp,
                             cols:cols, rows:rows, sp:Math.round(sp*100)/100, cases:_semis};
          /* ⚑ v100 — des cases sautées au budget : la bande se repeint à l'image suivante, tant que c'est la même Nuée ouverte */
          window._nueeSemis.sautees=_saute;
          /* ⚠ ON NE REPOSE PAS LA FICHE À CHAQUE IMAGE : `_ficheNuee` repose tout (50 à 190 ms en WebKit) — rappelée tant qu'il
             manquait une case, elle l'était 20 fois (1 s mesurée). Les dalles manquantes se rendent une par tâche, une image
             entre chacune ; la bande n'est repeinte qu'UNE fois, quand tout est prêt. */
          if(_saute){ var _kN=k, _M=_manque.slice(), _ouv=function(){ var _dp=document.getElementById('detailPoster');
              return typeof curNuee!=='undefined' && curNuee===_kN && _dp && _dp.classList.contains('show'); };
            window._nueeReprise=(window._nueeReprise||0)+1; var _jeton=window._nueeReprise;
            (function suite(){ requestAnimationFrame(function(){ setTimeout(function(){
              if(_jeton!==window._nueeReprise || !_ouv()) return;
              if(_M.length){ var a=_M.shift(); try{ _faire(a[0],a[1],a[2],a[3],a[4]); }catch(_){ } suite(); return; }
              try{ if(window._nueeBande) window._nueeBande(); }catch(_){ } }, 0); }); })(); }
        })();
        g.strokeStyle=col; g.lineWidth=10; g.lineCap='round'; g.lineJoin='round';
        g.beginPath(); chemin(g,y,0,W); g.stroke();
        };
        window._nueeBande=_peintBande; _peintBande();
      }
    }

    /* — les cotes — */
    var encre = light?ENCRE:CREME;
    var mm=document.getElementById('dptNat'); if(mm) mm.textContent='Cercle';
    /* §12 · les Noyaux d'une Nuée sont à `boîte − 29`, pas à `boîte + 4` comme sur une
       fiche de promesse. Relevé sur les vingt écrans de l'inventaire, sans exception :
       540 → 511 · 454 → 425 · 368 → 339 · 282 → 253 · 256 → 227. Tout le reste en découle,
       au pixel : à-qui = +124, titre = +30, méta = +65, et la première ligne du fil à
       méta + 30 — ce qui redonne 674 · 588 · 502 pour n = 1, 2, 3, et 476 pour n ≥ 4. */
    /* ⚑ v101 (Tom : « zéro espace sous “Avec”, ça se voit tout de suite. Le moodboard date d'avant l'agrandissement des textes :
       c'est lui qui est périmé ») — LA COLONNE SE DÉRIVE DE L'ENCRE, PAS DES COTES DE LA PLANCHE. Depuis v96 (`size-adjust:112%`
       sur Gilbert et Atkinson), les lignes sont plus hautes à taille égale : « Avec » déborde de 3 px au-dessus de sa boîte et
       finit à boîte + 23, le titre commence 7 px au-dessus de la sienne et finit à + 44, l'état commence 2 px au-dessus. Les airs
       d'avant l'agrandissement — trait → Noyaux 11, Noyaux → « Avec » 19, « Avec » → titre 5, titre → état 22 (mesurés à l'encre,
       redteam_nuee_entree) — donnent : « Avec » = Noyaux + 125 (+124 laissait 18), titre = « Avec » + 23 + 5 + 7 = + 35 (+30 laissait 0),
       état = titre + 44 + 22 + 2 = + 68 (+65 laissait 19). Tout ce qui suit (le fil, l'invitation) dérive déjà de l'état. */
    var yN=boite-29, yQui=yN+127, yTitre=yQui+35;   /* v102 : +127 et non +125 — l'air se prend sous l'ENCRE du nom des Noyaux (« Toi »), pas sous leur boîte : 18 avant v96 */
    var aura=document.getElementById('dAura');
    /* Les Noyaux d'une Nuée (§5) : le tien, puis CELUI DE LA NUÉE. L'app ne construisait pas
       cette rangée sur une fiche de Nuée — on la bâtit avec SES composants (karmaRing,
       drawKRing), pas avec des formes reconstruites. */
    var vieux = aura && aura.querySelector('.aura-track');
    if(vieux && vieux.getAttribute('data-nk')!==k){ vieux.parentNode.removeChild(vieux); vieux=null; }
    if(aura && !vieux && typeof karmaRing==='function'){
      var cpt=function(l,s){ return l.filter(function(q){return q.status===s;}).length; };
      var tous=[]; try{ tous=promises.filter(function(q){return !q.draft;}); }catch(_){}
      var nom=(typeof NUE!=='undefined'&&NUE[k])?NUE[k]:k;
      var tr=document.createElement('div'); tr.className='aura-track'; tr.setAttribute('data-nk',k);
      tr.innerHTML='<div class="kring kring-moi"><div class="kr-wrap">'
        + karmaRing(cpt(tous,'encours'),cpt(tous,'tenu'),cpt(tous,'rate'),78)
        + '</div><div class="kr-n">Toi</div></div>'
        + '<div class="kring" data-nuee="'+nom+'"><div class="kr-wrap">'
        + karmaRing(cpt(liste,'encours'),cpt(liste,'tenu'),cpt(liste,'rate'),58)
        + '</div><div class="kr-n">'+nom+'</div></div>';
      aura.insertBefore(tr, aura.firstChild);
      try{ tr.querySelectorAll('.kr-c').forEach(function(c){ drawKRing(c); }); }catch(_){}
    }
    if(aura) pose(aura,{display:'block', position:'absolute', left:'24px', top:yN+'px',
                        width:'342px', height:'auto', margin:'0', padding:'0', background:'none'});
    noyaux(aura, natCol);
    var qui=document.getElementById('dptQui'), ti=document.getElementById('dptTitre'), qd=document.getElementById('dptQuand');
    /* ⚑ LE MOT DE LA LIGNE « À QUI » D'UNE NUÉE VIENT DES CADRES 58 ET 60 :
           « Avec Rachel, Adrien, +3 »        — deux nommés, puis le reste, MOI COMPRIS
           « Avec toi seulement »             — quand la Nuée n'a aucun membre (cadre 60)
       L'app écrivait « avec le groupe » : c'est la valeur du champ `who` d'un Promi de
       Nuée, pas le mot de l'écran. Et le cadre écrit le tout d'un seul ton, sans pâle ni
       gras — le §5 lui donne Bricolage 600 / 19, couleur de la nature claire.
       « +3 » compte les membres restants ET moi : 4 membres nommés, deux affichés,
       il reste Léa, Nico et moi. C'est ce que recoupe l'Index avec son « avec +4 »
       (les quatre autres que moi). */
    if(qui){
      var _mem=(typeof NUEEMEM!=='undefined' && NUEEMEM[k]) || [];
      var _reste=_mem.length-1;                     /* les non nommés, moi compris */
      qui.textContent = _mem.length
        ? ('Avec ' + _mem.slice(0,2).join(', ') + (_reste>0 ? (', +'+_reste) : ''))
        : 'Avec toi seulement';
    }
    pose(qui,{top:yQui+'px', color:colTexte, '-webkit-text-fill-color':colTexte, 'font-size':'19px'});
    pose(ti ,{top:yTitre+'px', color:encre, '-webkit-text-fill-color':encre, 'font-size':'38px'});
    var sc2=(dp.clientWidth||W)/W;
    var hT = ti ? Math.round(ti.getBoundingClientRect().height/sc2) : 39;
    /* §12 · la méta d'une Nuée est à TITRE + 65, une valeur de l'inventaire, pas une mesure :
       730−665 · 644−579 · 558−493 · 472−407 · 446−381 — 65 sur les vingt écrans. Mesurée
       (`hT + 26,3`), elle sortait à 62 sur un nom d'une ligne, et tout le fil descendait de
       3 px avec elle. Un titre de DEUX lignes reprend la mesure : elle ne peut pas mordre. */
    var yEtat=Math.round(yTitre + (hT>50 ? hT+29.2 : 68));   /* v101 : 22 à l'encre sous le titre (le titre de deux lignes aussi : sa dernière ligne finit à boîte + 5,2) */
    /* ⚠ SA TAILLE AUSSI (13 sept. 2026) : sans elle, la ligne gardait les 13,5 d'une fiche ouverte avant, ou
       prenait les 13 du plancher à froid. 13,5 : le cran de la décision du 29 août, « toutes les natures ». */
    pose(qd,{top:yEtat+'px', color:colTexte, '-webkit-text-fill-color':colTexte, 'font-size':'13.5px'});
    var hE = qd ? Math.round(qd.getBoundingClientRect().height/sc2) : 15;
    /* le fil de la Nuée : ses cartes commencent 30 px sous la ligne d'état (§5).
       Sur une Nuée vide, c'est l'invitation qui prend la place, à état + 44. */
    /* LA CARTE DU FIL porte le Promi EN RÉDUCTION : sa dalle, SON TRAIT, sa couleur d'état
       (§5, cadre 58). Ce n'est pas un rectangle de champ plus un trait à côté : c'est UN SEUL
       SVG de 103 × 74, où l'onde borne le champ mauve à droite et porte la ligne d'état.
       Les valeurs ne sont pas estimées : elles sont RELEVÉES sur le cadre 58 puis retrouvées
       par la formule du §2.1 — base = 86, per = 1 (§3.9), amp = 8,6 (soit bien les « 13 ×
       échelle » du §3.9 pour une carte réduite à 74 de haut). Le plein va de 0 à 37, la
       moitié exacte (§2.6), puis des points r 2,6 tous les 10 px ; sur une parole tenue le
       trait est complet, 0 → 74. */
    (function(){
      var f=document.getElementById('dpNueeFil'); if(!f) return;
      var H=74, LX=103, BASE=86, AMP=8.6, PER=1, EP=5, R=2.6, ESP=10, N=24;
      var mont=AMP*0.34, aa=AMP*0.62;
      function xx(u){ return BASE - mont*u - aa*Math.sin(2*Math.PI*PER*u); }
      var chemin='M'+xx(0).toFixed(1)+' 0';
      for(var i=1;i<=N;i++) chemin+='L'+xx(i/N).toFixed(1)+' '+(H*i/N).toFixed(1);
      var _rang = -1;
      f.querySelectorAll('.nf-item').forEach(function(it){
        _rang++;
        var _p = liste[_rang] || null;
        var tenu = it.classList.contains('nf-menthe');
        /* le trait de la carte est posé SUR le champ plein : teinte claire dans les deux
           thèmes (§2.1 bis), sinon c'est du mauve sur mauve. */
        var col = tenu ? etatTrait('tenu', light)        /* ⚑ 21 sept. : l'amande n'est plus un état · 22 sept. : `light` est un BOOLÉEN — `light()` levait une TypeError, avalée par le try/catch : tout le reste du poseur sautait (fil, état défilé) dès qu'une carte était tenue */
                : it.classList.contains('nf-ocre') ? TERRA
                : NATTRAIT.nuee;
        var fin = tenu ? N : Math.round(N*0.5);
        var d='M'+xx(0).toFixed(1)+' 0';
        for(var j=1;j<=fin;j++) d+='L'+xx(j/N).toFixed(1)+' '+(H*j/N).toFixed(1);
        /* ⚑ v36 (Tom) — DANS LA FICHE DE NUÉE SEULEMENT, EN SOMBRE SEULEMENT : un liseré très fin, du crème adouci des
           filets, À DROITE du trait (sinon le trait sombre ne se distingue plus du corps), et seulement le long de ce qui
           est tracé — jamais sur la moitié qui ne l'est pas. */
        var lis='';
        if(!light){ var OFF=EP/2+0.4, dl='M'+(xx(0)+OFF).toFixed(1)+' 0';
          for(var jl=1;jl<=fin;jl++) dl+='L'+(xx(jl/N)+OFF).toFixed(1)+' '+(H*jl/N).toFixed(1);
          lis='<path d="'+dl+'" stroke="'+(window._FILET_DOUX||'#F7F0DE')+'" stroke-width="0.8" stroke-linecap="butt"/>'; }
        var pts='';
        if(!tenu){ for(var y=47; y<H-R; y+=ESP)
          pts+='<circle cx="'+xx(y/H).toFixed(1)+'" cy="'+y+'" r="'+R+'" fill="'+col+'"/>'; }
        var old=it.querySelector('.s1b-fil-trait'); if(old) old.parentNode.removeChild(old);
        var w=document.createElement('div'); w.className='s1b-fil-trait';
        w.innerHTML='<svg width="'+LX+'" height="'+H+'" fill="none">'
          +'<path d="'+chemin+'L0 '+H+'L0 0Z" fill="'+NATCOL.nuee+'"/>'
          +'<path d="'+d+'" stroke="'+col+'" stroke-width="'+EP+'" stroke-linecap="round"/>'+lis+pts+'</svg>';
        it.insertBefore(w, it.firstChild);
        /* l'eyebrow porte L'ÉTAT (§5 : « TENU », « À TENIR »), pas le mot du temps. Les mots
           sont ceux de l'app (STLAB) : rien d'inventé, seulement le bon champ. */
        var em=it.querySelector('.nf-tx em');
        if(em){ var st = tenu ? 'tenu' : (it.classList.contains('nf-ocre') ? 'rate' : 'encours');
          var lab = (typeof STLAB!=='undefined' && STLAB[st]) ? STLAB[st] : st;
          /* ⚠ UNE NUÉE PORTE LES DEUX, ET LA LIGNE DOIT LE DIRE. Un Chiche dans une Nuée
             sortait « en cours » — le mot d'un Promi. **Le moodboard écrit sa nature** :
             relevé au cadre « Le fil, après défilement » de `promi-nuee-toile.html`,
             « CHICHE LANCÉ » et « CHICHE RELEVÉ ». Ce sont ces mots-là, pas les miens.
             Un Chiche relevé ou tenu est RELEVÉ ; sinon il est LANCÉ. */
          /* ⚠ C'EST `chicheEtat` QUI DIT S'IL EST RELEVÉ, pas l'état de la parole.
             La ligne se lisait sur `tenu || status==='rate'` : « vider le composteur à
             deux », relevé mais pas encore tenu, sortait « CHICHE LANCÉ » là où le cadre 10
             de `promi-nuee-toile` écrit « CHICHE RELEVÉ ». Relever un chiche, c'est
             l'accepter — c'est un fait du Chiche, pas de la parole. */
          if(_p && _p.chiche)
            lab = (_p.chicheEtat === 'releve' || tenu || _p.status === 'rate')
                  ? 'CHICHE RELEVÉ' : 'CHICHE LANCÉ';
          /* ⚠ ET « TENU », PAS « TENUE ». Le fil d'une Nuée porte des Promi, pas des
             paroles : le cadre 10 écrit « TENU · monter la serre avant les gelées ».
             `STLAB.tenu` vaut « tenue » — le mot de la fiche, où le sujet est la parole. */
          if(lab === 'tenue' || lab === 'TENUE') lab = 'TENU';
          em.textContent = lab; }
      });
    })();

    /* §9 · le pas entre deux lignes est TOUJOURS 12 px, sans exception : la première ligne
       tombe à méta + 30, et de là tout s'enchaîne (86 = 74 + 12). Pour n ≤ 3 la dernière
       ligne s'arrête ainsi à 12 px de la barre (748 pour une barre à 760) ; à partir de 4,
       trois lignes tiennent entières et LA QUATRIÈME DÉPASSE SOUS LA BARRE de 26 px —
       c'est ce dépassement qui dit qu'il y en a d'autres. Il est VOULU, pas subi. */
    /* ═══ §12 · L'ÉTAT DÉFILÉ — ses cotes se LISENT, elles ne se déduisent pas ═══
       L'encart, les Noyaux et l'à-qui « remontent et disparaissent sous le trait » (§13) ;
       il ne reste qu'une bande de Toile, le nom, la méta, et le fil qui prend toute la
       place. L'entête et le titre rapetissent : Fraunces 23 au lieu de 27, Bricolage 26 au
       lieu de 38 — c'est l'inventaire, relevé sur les deux écrans du §12. */
    if(defile){
      var tete=document.getElementById('dpTete');
      /* ⚑ LE PLATEAU NE BOUGE PAS AVEC LE DÉFILEMENT (loi 1) — et il tient ses deux textes.
         Ces deux lignes reposaient le mot-marque en `position:absolute; left:24; top:20;
         font-size:23` et le FERMER à `top:20` : les cotes de l'entête d'AVANT le plateau,
         posé à nu. Depuis la loi 1, les deux vivent DANS le plateau, en flex
         `space-between`. Rendre le mot-marque absolu le sortait du flux : le plateau se
         retrouvait avec un seul enfant en flux, et `space-between` collait le FERMER À
         GAUCHE, par-dessus le mot. Mesuré : « Nuée » à 50/62 et « ✕ FERMER » à 52/64,
         `elementFromPoint` au centre du mot rendant `closeb` — le mot était recouvert.
         C'est `redteam_nuee` qui le voyait, sous le nom « Nuée ⨯ ✕ Fermer », et je l'ai
         longtemps pris pour un rouge antérieur de juge. C'était un vrai défaut d'écran.
         Le §13 continue de faire remonter l'encart, les Noyaux et le titre : eux seuls
         appartiennent au défilement. */
      pose(document.getElementById('dAura'), {display:'none'});
      pose(document.getElementById('dptQui'), {display:'none'});
      var tiD=document.getElementById('dptTitre'), qdD=document.getElementById('dptQuand');
      /* ⚑ v101 — mêmes airs à l'encre qu'avant l'agrandissement v96 : titre dès 95, état 8 dessous, fil 31 sous l'état
         (98 · 136 · 182 laissaient 6 et 30 : le titre de 26 finit désormais à boîte + 30, l'état commence à boîte − 2). */
      pose(tiD,{display:'block', position:'absolute', left:'24px', top:'100px', width:'342px',
                'font-size':'26px', 'letter-spacing':'-.03em',
                color:encre0(light), '-webkit-text-fill-color':encre0(light)});
      pose(qdD,{display:'block', position:'absolute', left:'24px', top:'140px',
                color:colTexte, '-webkit-text-fill-color':colTexte});
      var filD=document.getElementById('dpNueeFil');
      if(filD){ pose(filD,{position:'absolute', left:'0', top:'187px', width:'390px',
                           margin:'0', padding:'0'});
        var hD=Math.round(filD.getBoundingClientRect().height/((dp.clientWidth||W)/W));
        var mnD=document.getElementById('dpMain');
        if(mnD) mnD.style.setProperty('min-height', Math.max(844, 187+hD+30)+'px','important');
      }
      window._nueeSemisCotes={tete:20, titre:100, meta:140, fil:187};
      return;
    }
    /* ⚠ L'AIR SOUS L'ÉTAT SUIT SA HAUTEUR (même règle que la fiche, décision Tom du 29 août
       au soir). Le 30 du §9 vaut « hauteur de l'état (12,5 × 1,1 = 13,75) + 16,25 d'air » ;
       l'état passé à 13,5 mangeait 1,1 px sur la première carte du fil. On garde l'air. */
    var _hQd = 13.75;
    try{ if(qd){ var _rq=qd.getBoundingClientRect(); if(_rq.height) _hQd=_rq.height/sc2; } }catch(_){}
    var fil=document.getElementById('dpNueeFil'), yFil=Math.round(yEtat + _hQd + 16.25 + window._encreSup(13.5).bas);   /* v102 : + l'encre agrandie de l'état */
    if(fil){ pose(fil,{position:'absolute', left:'0', top:yFil+'px',
                       width:'390px', margin:'0', padding:'0'});
      /* le fil défile : #dpMain doit porter sa hauteur, sinon la barre Peaufiner (collante)
         recouvre les dernières cartes au lieu de les laisser passer dessous. */
      var hFil=Math.round(fil.getBoundingClientRect().height/sc2);
      var mn=document.getElementById('dpMain');
      if(mn) mn.style.setProperty('min-height', Math.max(760, yFil+hFil+30)+'px', 'important');
    }
  }catch(err){} };

  /* ═══ §13 · LE DÉFILEMENT — RÈGLE UNIQUE DANS LE PRODUIT ═══
     « Sur la fiche d'une Nuée, LE DOIGT QUI DESCEND FAIT DÉFILER LE FIL, pas les réglages.
     L'encart, les Noyaux, le titre et la méta remontent et disparaissent sous le trait ; les
     Promi et les Chiche prennent toute la place, et il n'en reste qu'une bande de Toile en
     haut. […] Conséquence directe : SUR CETTE PAGE, PEAUFINER NE S'OUVRE QU'EN TOUCHANT SA
     BARRE. Partout ailleurs c'est l'inverse. Sans cette exception écrite, le comportement
     sera implémenté comme les autres écrans. »
     L'état est une CLASSE que le code pose, jamais une géométrie qu'il vient de produire —
     c'est le piège du §8 de CLAUDE.md, payé deux fois sur la page +. */
  var _defSeuil = 8;                     /* le doigt a bougé : on est défilé */
  window._nueeDefile = function(v){
    var av = !!window._nueeDefileEtat, ap = !!v;
    if(av === ap) return;                /* on ne repeint que sur un VRAI changement */
    window._nueeDefileEtat = ap;
    /* `_ficheTout` et non `_ficheNuee` seul : c'est lui qui rejoue AUSSI `_enteteLisible`,
       et l'entête doit reprendre son encre — sur la bande de 114 px, le mot-marque se
       retrouve posé sur la matière, pas sur l'aplat (§10.6 généralisé, Q59). */
    try{ (window._ficheTout || window._ficheNuee)(); }catch(_){}
  };
  (function(){
    function surFiche(){
      var dp=document.getElementById('detailPoster');
      return !!(dp && dp.classList.contains('show')
                && (dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')));
    }
    function lu(){
      if(!surFiche()) return;
      var dp=document.getElementById('detailPoster');
      var mn=document.getElementById('dpMain');
      var t=Math.max(dp?dp.scrollTop:0, mn?mn.scrollTop:0);
      window._nueeDefile(t > _defSeuil);
    }
    ['scroll','touchmove','wheel'].forEach(function(ev){
      document.addEventListener(ev, lu, true);
    });
    /* la fiche se rouvre POSÉE : l'état ne survit pas à une fermeture. */
    var _ca=window.closeAll;
    if(typeof _ca==='function'){
      window.closeAll=function(){ var r=_ca.apply(this,arguments);
        try{ window._nueeDefileEtat=false; }catch(_){} return r; };
      try{ closeAll=window.closeAll; }catch(_){}
    }
  })();

  /* on se branche APRÈS le peintre précédent : la référence est résolue à l'appel. */
  var _pose=window._fichePose;
  function tout(){ try{ window._ficheTrait(); window._ficheCotes(); window._ficheNuee();
      var dp=document.getElementById('detailPoster');
      if(dp && dp.classList.contains('show'))
        enteteLisible('dpTrameCv', dp, ['#dptNat','.closeb']);
    }catch(e){} }
  window._ficheTout=tout;
  window._fichePose=function(){ if(_pose) _pose.apply(this,arguments);
    try{ requestAnimationFrame(function(){ requestAnimationFrame(function(){ tout(); tout(); }); }); }catch(e){} };
  var _ref=window.dpRefresh;
  if(_ref){ window.dpRefresh=function(){ _ref.apply(this,arguments); tout(); }; }
  var _rn=window.renderNueeDetail;
  if(_rn){ window.renderNueeDetail=function(){ var r=_rn.apply(this,arguments);
    try{ requestAnimationFrame(function(){ requestAnimationFrame(tout); }); }catch(e){} return r; }; }
  var _on=window.openNueeDetail;
  if(_on){ window.openNueeDetail=function(){ var r=_on.apply(this,arguments);
    /* ⚠ UNE NUÉE OUVERTE APRÈS UNE FICHE EN GARDAIT LES RESTES (12 sept. 2026) : la classe de nature
       (`dp-chiche`), la zone du mot et des pièces (#dpCorps, peinte derrière le plateau) et le rond
       photo. Ouverte à froid, elle n'a rien de tout ça : on la rend identique. `data-masque` les
       rend à `closeAll`, la fiche suivante les retrouve. */
    try{ var _dp=document.getElementById('detailPoster');
      if(_dp){ _dp.classList.remove('dp-promi','dp-chiche','dp-draft','dp-innuee');
        [document.getElementById('dpCorps'), _dp.querySelector(':scope > .ph-photo-nid')].forEach(function(n){
          if(n && n.style.getPropertyValue('display') !== 'none'){
            n.style.setProperty('display','none','important'); n.setAttribute('data-masque','1'); } }); } }catch(e){}
    /* ⚠ OUVERTE DEPUIS UNE FICHE VISIBLE (le disque « le potager »), la Nuée gardait le titre du Promi et
       n'avait pas de fil : `closeAll` retire `show` et on le remet dans la même tâche, donc l'observateur
       qui pose la fiche (il compare avant/après) ne voit rien. On la pose nous-mêmes. */
    try{ requestAnimationFrame(function(){
      try{ if(window._fichePose) _fichePose(); }catch(_){}
      try{ if(window._ficheDalle) _ficheDalle(); }catch(_){} }); }catch(e){}
    try{ requestAnimationFrame(function(){ requestAnimationFrame(function(){ tout(); setTimeout(tout,120); }); }); }catch(e){} return r; }; }
  ['resize','orientationchange'].forEach(function(ev){ window.addEventListener(ev,tout); });
})();
