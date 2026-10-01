/* ── LA PLANCHE ───────────────────────────────────────────────────────────── */
var EMP={ c:[-0.36,-0.22,0.91], ax:[0.62,-0.72,0.00],
          a:0.42, el:0.62, dmax:0.245, biais:0.14,
          /* ⚠ U EST UN GLISSEMENT EN RADIANS, PAS UN COEFFICIENT LIBRE.
             A 1,85 avec dmax 0,215, la matiere glissait de 0,40 rad — vingt-trois
             degres, un quart de l'hemisphere visible. Les dalles ne se tassaient
             pas : elles se MELANGEAIENT, et le contact sortait en pluie de traits
             de toutes les couleurs. Le refoulement d'une pulpe vaut le volume
             chasse divise par la circonference, soit d x a / 2 = 0,039 rad. On
             prend 0,12 — un peu plus que le physique pour que ca se voie, pas
             assez pour brouiller la partition. */
          rho:0.085, ub:0.35, B:0.32, U:0.50 };
function emp(p){var o={};for(var k in EMP)o[k]=EMP[k];o.p=p;return o;}

/* le froisse : trois bandes, toutes >= 9 tours SUR LES TROIS AXES */
var FROISSE=[[0.030,11.3,12.7,10.9,0.4,1.1,2.2],
             [0.017,21.7,19.3,22.1,1.9,0.3,1.4],
             [0.008,37.1,34.3,35.9,0.7,2.4,1.0]];
/* l'enveloppe : basse frequence, elle module l'AMPLITUDE — pas la forme */
var ENV=[0.10,0.90,1.7,1.3,1.9,0.4,1.9,0.8,1.7];
var KDENS=[4.7,5.3,4.1,0.6,1.9,1.1,  6.7,5.9,7.3,2.4,0.7,1.5];

window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]); }catch(e){}
  setTimeout(function(){
    window.__moteur=!!(window.Toile && window.Toile.mondeCourant);
    /* ⚑ LE GRAIN SE MESURE SUR LE CADRE, PAS EN PIXELS ABSOLUS.
       L'atlas etait en pixels CSS fixes : sur un cadre de 200 px, le meme
       grain devenait trois fois plus gros par rapport a la boule, et les
       petits formats sortaient empatés. Un atlas par taille de cadre. */
    /* LES POILS. L'atlas est en ALPHA seule : la couleur se compose au
       versement. Et il se mesure sur le CADRE — en pixels absolus, le meme poil
       est trois fois plus gros sur un cadre de 200 px que sur un de 620. */
    /* ⚑ DES MECHES, PLUS DES BRINS. A 4,2-7,2 le poil fait 7 a 13 px sur un
       cadre de 620 : c'est un duvet ras, pas une fourrure qu'on a envie
       d'ecraser. On allonge d'un tiers.
       Le cout n'est PAS proportionnel : le banc dit qu'un poil coute 0,108 µs
       dont seulement 0,042 de pixels — les deux tiers sont le passage dans la
       boucle. Allonger n'enfle que la part « pixels ». On compense par un semis
       un peu moins dense : moins de touffes, mais chacune couvre plus, donc la
       fourrure est PLUS fournie a l'oeil pour un budget egal. */
    /* ⚑ LA LONGUEUR DU POIL EST FIXEE PAR LE PAS DE LA TRAME, PAS PAR LE GOUT.
       Un poil porte UNE couleur sur toute sa longueur : il etale donc la
       couleur de sa racine. A 9,7 px il ecrase un carreau de mosaique (11 px)
       et un pois de braille (9 px) — mesure a l'ecran : a pas reel, la grille
       de mosaique DISPARAISSAIT.
       On l'ecrit comme une regle : le poil doit valoir au plus le TIERS du pas
       du motif. Pas le plus fin, 5 px (pixel) ; le plus gros, 11 (mosaique).
       ⚠ MAIS LE PAS N'EST PAS CELUI DE LA DALLE : c'est celui qu'on LIT sur
       la sphere. Mesure a l'ecran : a `mag` 2,7 une cellule montre 5 a 7
       carreaux — exactement ce que montre la Toile ; a pas reel elle en montre
       une vingtaine, et le motif devient du bruit. Le grossissement etait donc
       JUSTE, et je l'avais accuse a tort. Ce qui n'allait pas, c'est le
       CONTOUR (voir _p_peint.js). On revient a 2,7, et la longueur reprend le
       fluffy — un tiers du pas lu, soit ~8 px. */
    /* ⚠ ET LA TOILE EST MAINTENANT A SON ECHELLE : un carreau de mosaique fait
       11 px a l'ecran, un pois de braille 9. Le poil doit donc valoir au plus
       leur tiers — 3,7 px — sinon il les etale et le dessin se perd. C'est un
       velours ras, pas une fourrure longue : c'est le prix du dessin exact. */
    /* ⚑ LES POILS REDEVIENNENT LONGS — c'est le premier dividende du
       changement de parti. Ils avaient ete ramenes a 3,1 px pour ne pas
       ETALER la trame d'une dalle : un poil porte une seule couleur sur toute
       sa longueur, et a 8 px il brouillait un carreau de 11. Il n'y a plus de
       trame a preserver. Une ile fait 0,2 radian — cent fois un poil : il peut
       donc etre long sans rien detruire. On repart a 6 / 8 / 10. */
    /* ⚑ QUATRE LONGUEURS, ET LA PREMIERE EST LA TONTE.
       Idee de Tom : le sol en poil long et soyeux, LES DALLES EN RASE. Une
       zone tondue dans un pelage se lit d'un coup d'oeil — c'est du relief,
       pas un aplat de couleur — et le rase montre sa couleur BEAUCOUP mieux,
       puisqu'il y a moins de brins qui se recouvrent pour la moyenner.
       Index 0 = la tonte (les dalles). Index 1 a 3 = le pelage, par profondeur. */
    var TAI0=[3.4,7.6,10.2,13.0], ATLC={};
    function atlasPour(css){
      if(ATLC[css]) return ATLC[css];
      var k=css/620, T=[TAI0[0]*k,TAI0[1]*k,TAI0[2]*k,TAI0[3]*k];
      ATLC[css]={a:atlasAlpha(GRAIN_POIL,T,ORI,NIVA,0.20,1.00,true,NVAR), t:T};
      return ATLC[css];
    }
    /* le joint est presque nul : c'est LA FORME DE LA DALLE qui decoupe le vide */
    /* ⚑ LE JOINT EST CONSTANT — c'est ce qui fait une Toile.
       0,016 rad, soit environ 4 % du diametre d'une dalle : le meme filet
       partout, comme entre deux dalles de la Toile. Avant, c'est la silhouette
       de la dalle qui creusait le joint, donc il variait du simple au triple.
       45 000 candidats : 36 450 poils peints sur les mondes pleins. MESURE au
       banc sur un ecran de 390 px, sphere en rotation : mediane 16,40 ms,
       9e decile 17,00, UNE image au-dessus de 20 ms sur 144. C'est le plafond
       honnete des 60 images par seconde pour ce grain-la. */
    /* ⚑ 440 000 POILS — et ils tiennent parce qu'ils poussent EN TOUFFES.
       Un poil isole coute 0,108 microseconde, dont seulement 0,042 de pixels :
       les deux tiers sont le passage dans la boucle. Quatre poils partant de la
       meme racine ne paient qu'UN passage — chaque poil supplementaire revient
       donc a 0,042. Et une fourrure pousse en touffes, pas en brins isoles.
       Mesure au banc, ecran 390 px, sphere en rotation :
          110 010 touffes = 440 040 poils   mediane 16,60 ms
          ZERO image au-dessus de 20 ms sur 144.
       Le dos n'est ni peint ni visite : tout est sur la face qu'on voit. */
    var NC0=700000;
    /* ⚑ 77 CELLULES, ET C'EST MESURE, PAS ESTIME.
       `scratchpad/compte_dalles.html` plante jusqu'a saturation et compte : la
       Toile a 54 cellules a 390 x 620, soit une dalle de 66,9 px de cote. La
       surface d'une sphere de meme ecran vaut 345 237 px2 ; a taille de dalle
       egale il en faut donc 77 — dont une trentaine visibles de face, comme un
       ecran de Toile. J'en avais 61. */
    /* ⚑ LA SYNCHRO : monde ET palette viennent du Studio, et la trame se
       rebatit a chaque changement. La sphere suit la Toile, toujours. */
    var TRC={}, SEMC={}, LIB={};
    function monde(m,pal){
      try{ if(m) Toile.setTheme(m); if(pal) Toile.setPalette(pal); }catch(e){}
      var cle=(m||Toile.getTheme())+'/'+(pal||Toile.getPalette());
      if(!TRC[cle]){ TRC[cle]=bat_trames([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]); TRC[cle].cle=cle; }
      var T=TRC[cle];
      /* ⚑ CHAQUE MONDE VISE LA MEME DENSITE DE POILS.
         Un monde creux (gravure, 26 % de matiere dans le rectangle inscrit)
         peignait deux fois moins de poils qu'un monde plein — l'Orbite y
         sortait terne, alors que ce qu'on veut voir c'est SA TRAME, pas sa
         penurie. On seme donc en proportion inverse du remplissage, plafonne a
         trois fois pour ne pas exploser le calcul du pavage. */
      if(!SEMC[cle]){
        /* ⚑ LE SEMIS SE DIMENSIONNE SUR LE REMPLISSAGE DU MONDE.
           Depuis que l'entre-dalles reste vide, le nombre de tampons peints
           depend de la trame : encre en donne 180 000 quand gravure en donne
           58 000 pour le meme semis. On vise donc ~110 000 tampons — le plafond
           mesure des 60 images par seconde — en semant a l'inverse du
           remplissage, borne pour que la construction reste tenable. */
        var fac=Math.min(3.2, 1/Math.max(0.18, T.plein));
        /* les quatre mondes ancres sur la Toile gardent un repere commun ;
           les quatre autres portent l'angle de leur graine */
        var mm=(m||Toile.getTheme());
        var tourne=!(mm==='braille'||mm==='mosaique'||mm==='pixel'||mm==='sillons');
        /* LIBRE : les trois mondes qui debordent de leur cellule sur la Toile */
        LIB[cle]=(mm==='encre'||mm==='terrazzo'||mm==='touffe');
        /* ⚑ 155 000 TOUFFES = 620 000 POILS. Depuis que les points qui ne
           peignent rien sont supprimes du semis (compaction), la boucle ne
           visite plus que de la matiere : le banc donne 161 156 touffes a
           15,30 ms. On vise donc 155 000, pas 112 000. */
        /* ⚠ on descend de 155 000 a 118 000 touffes visees : chaque touffe
           couvre 1,8 fois plus de pixels qu'avant. A budget egal, la fourrure
           est plus fournie — c'est la longueur qui fait la masse, pas le
           nombre. Le chiffre se reconfirme au banc (scratchpad/cap_banc.py). */
        /* ⚑ DEPUIS QUE LA TOILE EST ENROULEE, IL N'Y A PLUS DE VIDE.
           On semait a l'inverse du remplissage de la dalle — 400 000 a 800 000
           candidats — parce que la plupart tombaient dans le vide entre les
           marques et ne peignaient rien. Maintenant la Toile couvre toute la
           boule : CHAQUE candidat peint. Mesure : 531 000 touffes peintes sur
           gravure, 67,6 ms l'image. On vise donc directement le nombre voulu. */
        /* ⚑ ET ON RECUPERE LE BUDGET EN DEFINITION. A 155 000 touffes de 3,7 px
           la couverture n'est que de 3,8 fois : chaque poil etale sa couleur sur
           un carreau de 11 px et le dessin se brouille. L'image ne coutant plus
           que 11,7 ms (le plafond est a 16,5), on double la densite et on
           raccourcit encore : la couverture passe a onze fois, et un poil ne
           vaut plus qu'un quart de carreau. */
        /* ⚑ PLUS FOURNI. A 330 000 touffes, les mondes a trame CREUSE —
           mosaique et braille, ou la matiere ne couvre que la moitie d'une
           cellule — laissent voir le fond entre les marques et la boule parait
           maigre. On monte a 520 000 : la couverture passe de onze a dix-sept
           fois sur les mondes pleins, et les creux se remplissent. */
        var nsem=520000;
        /* le joint : l'ecart au deuxieme site sous lequel on ne peint plus.
           C'est le filet de la Toile, et les coins s'y arrondissent. */
        /* pixel cale son bord sur une grille — c'est tout son dessin */
        var gril=(mm==='pixel')?0.044:0;
        /* ⚑ LE FILET DE LA TOILE EST CELUI DU MOTIF, PAS UN FILET EN PLUS.
           On posait 0,017 rad de joint « comme entre deux dalles de la Toile ».
           Or sur la Toile il n'y en a AUCUN : les cellules sont jointives, et
           l'espace qu'on voit est la gouttiere de la trame elle-meme (2 px sur
           11 en mosaique, le vide entre deux pois en braille). Ce joint-la
           ajoutait 4,5 px de noir a l'ecran AUTOUR de chaque dalle : c'est lui
           qui faisait lire des plaques separees au lieu d'une Toile. */
        SEMC[cle]=semisPavage(nsem,77,0.0035,KDENS,4,tourne,gril);
      }
      /* ⚑ ET MAINTENANT QUE LE SEMIS EXISTE, ON PEINT UNE DALLE PAR CELLULE.
         L'ordre compte : le semis se dimensionne sur le remplissage du monde
         (T.plein), qu'on tire d'un premier jeu de dalles ; les dalles PAR
         CELLULE, elles, ont besoin des cellules. On fait donc les deux, dans
         cet ordre, et c'est le second jeu qui sert au rendu.
         PXR de reference = CSS x R / mag, pour le grand cadre (620). */
      /* ⚑ ON N'ASSEMBLE PLUS RIEN : ON ENROULE LA TOILE.
         PXR de reference = CSS x R, sans grossissement : la Toile est alors a
         SON ECHELLE sur la boule — une cellule de 72 px reste une cellule de
         72 px, un carreau de mosaique fait 11 px, un pois de braille 9. */
      if(!TRC[cle+'|env']){
        var PXRREF=620*0.425;
        var Tc=null; try{ Tc=bat_toile(PXRREF); }catch(e){}
        TRC[cle+'|env']=Tc||T; TRC[cle+'|env'].cle=cle+'|env';
      }
      var TT=TRC[cle+'|env'];
      return {tr:TT, pal:Toile.cols(), cle:cle+'|env', sem:SEMC[cle], libre:LIB[cle]};
    }
    var G=document.getElementById('g'), infos=[];
    function cadre(hote,css,opt,leg){
      var fg=document.createElement('figure');
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); cv.setAttribute('data-cad',opt.id);
      box.appendChild(cv); fg.appendChild(box);
      var fc=document.createElement('figcaption'); fc.innerHTML=leg; fg.appendChild(fc);
      hote.appendChild(fg);
      var AT=atlasPour(css);
      var o={css:css,R:opt.R||0.425,tailles:AT.t,atlas:AT.a,semis:opt.M.sem,relief:FROISSE,
             env:ENV,lac:opt.lac===undefined?2.9:opt.lac,tan:0.32,
             pal:opt.M.pal,trame:opt.M.tr,emp:opt.emp,nu:opt.nu,fond:opt.fond,
             tflux:opt.tflux||0, libre:opt.M.libre,
             /* ⚑ LE BUG QUI A COUTE UNE LIVRAISON. `cadre()` recopie a la main
                les options qu'elle connait — et rien d'autre. Mes reglages de
                variation (velours, contre, duvet, grade, dresse) n'arrivaient
                donc JAMAIS au peintre : les huit cadres etaient identiques AU
                PIXEL PRES, verifie apres coup. Tom l'a vu avant moi.
                ⚠ Regle : quand on ajoute une option a un peintre, on verifie
                que deux reglages differents donnent deux IMAGES differentes.
                Un cadre qui ne bouge pas est un cadre qui ne prouve rien. */
             velours:opt.velours||0, contre:opt.contre||0,
             duvet:opt.duvet||0, grade:opt.grade||0, dresse:opt.dresse||0,
             mag:opt.mag||2.7};
      cv.__opt=o;                     /* sonde : de quoi rechronometrer une image */
      infos.push(peint(cv,o));
    }
    function rang(titre,texte,cls){
      var s=document.createElement('div'); s.className='rang';
      s.innerHTML=(titre?'<h2>'+titre+'</h2>':'')+(texte?'<p>'+texte+'</p>':'');
      var gr=document.createElement('div'); gr.className=cls; s.appendChild(gr);
      G.appendChild(s); return gr;
    }

    /* ⚑ L'ORBITE-FOURRURE : un semis de points, une palette, des iles.
       Plus de Toile a enrouler, plus de pavage a assembler. Le semis ne sert
       plus qu'a porter les touffes ; ses cellules ne colorent plus rien. */
    var SEM=null, ORB={};
    function orbite(n,pal,opt){
      opt=opt||{};
      var cle=n+'/'+(pal||'signal')+'/'+(opt.r||'');
      if(ORB[cle]) return ORB[cle];
      try{ if(pal) Toile.setPalette(pal); }catch(e){}
      if(!SEM){
        /* ⚠ JOINT NUL. Le filet entre cellules dessinait le pavage DANS le
           pelage. Il n'y a plus de pavage : la fourrure est continue. */
        /* un poil de 10 px couvre trois fois plus qu'un de 3 : on redescend
           le semis d'autant, sinon on paie trois fois pour rien. */
        /* ⚑ CE QUI NE PAIE RIEN — MESURE, NE PAS Y REVENIR.
           Affiner les touffes a coute cinq points de luminance (44,4 -> 39,5).
           J'ai cru compenser en densifiant : 190 000 -> 280 000 touffes, soit
           +47 % de calcul... et 38,6 de luminance, c'est-a-dire RIEN. La
           couverture etait deja saturee : ce qui plafonne la clarte, ce n'est
           pas le nombre de poils, c'est LA RAMPE (le sol part de 0,46 et les
           deux dernieres marches sont reservees aux reflets). On revient donc
           a 190 000, et la clarte se traitera dans la couleur. */
        SEM=semisPavage(230000,77,0.0,KDENS,4,false,0);
      }
      var o2={}; for(var q9 in opt)o2[q9]=opt[q9];
      o2.pxr=620*0.472; o2.palette=pal||Toile.getPalette();
      var T=batIles(n, Toile.cols(), o2);
      return (ORB[cle]={tr:T, pal:Toile.cols(), cle:cle, sem:SEM, libre:false});
    }
    /* le reglage retenu : lustre de fibre, contre-jour, limbe duveteux,
       grading, et les iles qui se dressent. */
    /* `dresse` sort : une dalle n'est plus en relief, elle est TONDUE. */
    /* le lustre et le contre-jour reviennent, mais DOUX : a 1,15 ils
       ajoutaient a eux seuls des bandes claires et sombres, c'est-a-dire
       exactement ce qu'on cherche a supprimer. */
    var LUX={velours:0.80, contre:0.70, duvet:1, grade:0.9, dresse:0, R:0.472};
    function av(n,pal,opt){
      var o={M:orbite(n,pal,opt)};
      for(var q in LUX) o[q]=LUX[q];
      return o;
    }

    var rH=rang('L’Orbite — la fourrure d’abord, les îles dedans',
      'L’état de repos n’est plus le vide : c’est le peigné. Chaque Promi est une île dans '+
      'la matière. La densité croît par accrétion, jamais par subdivision.','duo');
    var h0=av(0); h0.id='f-zero';
    cadre(rH,620,h0,'<b>Zéro Promi.</b> Le vrai test : si elle n’est pas belle vide, tout le reste tombe.');
    var h30=av(30); h30.id='f-hero';
    cadre(rH,620,h30,'<b>Trente Promi.</b> Trente îles accrétées dans la même fourrure.');

    var rC=rang('La croissance, par accrétion',
      'Zéro, une, cinq, trente. La fourrure ne se subdivise jamais : elle se peuple.','tri');
    [[0,'<b>0</b> — le peigné seul'],
     [1,'<b>1</b> — la première île'],
     [5,'<b>5</b> — la grappe commence'],
     [30,'<b>30</b> — la grappe tient la boule']].forEach(function(z){
      var o=av(z[0]); o.id='c-'+z[0]; cadre(rC,400,o,z[1]);
    });

    var rP=rang('Trois palettes du Studio',
      'Le sol prend la famille de la palette, les îles en prennent les couleurs.','tri');
    [['signal','Signal'],['braise','Braise'],['ocean','Océan']].forEach(function(z){
      var o=av(14,z[0]); o.id='p-'+z[0]; cadre(rP,400,o,'<b>'+z[1]+'</b>');
    });

    var rS=rang('L’épreuve du partage',
      'À 200 px. Si ça ne tient pas là, ça ne tient pas dans une image partagée.','tri');
    [[0,'<b>0</b>'],[5,'<b>5</b>'],[30,'<b>30</b>']].forEach(function(z){
      var o=av(z[0]); o.id='s-'+z[0]; cadre(rS,200,o,z[1]);
    });

    window.__infos=infos; window.__pret=true;
  },800);
});
