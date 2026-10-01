/* ── LA PLANCHE ───────────────────────────────────────────────────────────── */
/* ⚑ LA TAILLE DE L'EMPREINTE SE CALCULE, ELLE NE SE CHOISIT PAS.
   `a` est le demi-grand axe du contact, en FRACTION DU RAYON DE LA BOULE. Il
   etait a 0,42 : l'empreinte faisait donc 84 % du diametre de l'Orbite — un
   doigt aussi large que la boule. Ce n'est pas une question de gout, c'est une
   cote, et elle se derive :

     ecran            390 pt de large pour 71,5 mm   =>  5,455 pt / mm
     la boule         R = 0,438 x 390                =>  170,8 pt de rayon
     pulpe de pouce   17 x 12 mm  => demi-axes 8,5 et 6,0 mm  => 46,4 et 32,7 pt
     pulpe d'index    11 x  8 mm  => demi-axes 5,5 et 4,0 mm  => 30,0 et 21,8 pt

   soit, rapporte au rayon :  POUCE a = 0,272, el = 0,70
                              INDEX a = 0,176, el = 0,73
   Le pouce couvre donc 27 % du diametre de l'Orbite, l'index 18 %. C'est ce
   qu'on voit quand on pose vraiment le doigt sur un ecran.

   ⚑ ET C'EST LE CAPTEUR QUI TRANCHE, PAS UNE CONSTANTE. Un `Touch` porte
   `radiusX`, `radiusY` et `rotationAngle` : l'app lit la pulpe REELLE et pose
   a = radiusX / R (en points), el = radiusY / radiusX, l'axe a l'angle donne.
   Les deux jeux ci-dessous sont les BORNES entre lesquelles ca tombe — c'est
   a ca qu'ils servent, et c'est pour ca qu'ils sont derives et pas reglages.
   La profondeur suit la largeur : une meme pression sur une pulpe plus petite
   enfonce plus, mais pas au point de percer — on garde dmax / a = 0,58, le
   rapport de la version precedente. */
var DOIGTS={
  pouce:{ a:0.272, el:0.70, dmax:0.158 },
  index:{ a:0.176, el:0.73, dmax:0.102 }
};
var EMP={ c:[-0.36,-0.22,0.91], ax:[0.62,-0.72,0.00],
          a:0.272, el:0.70, dmax:0.158, biais:0.14,
          /* ⚠ U EST UN GLISSEMENT EN RADIANS, PAS UN COEFFICIENT LIBRE.
             A 1,85 avec dmax 0,215, la matiere glissait de 0,40 rad — vingt-trois
             degres, un quart de l'hemisphere visible. Les dalles ne se tassaient
             pas : elles se MELANGEAIENT, et le contact sortait en pluie de traits
             de toutes les couleurs. Le refoulement d'une pulpe vaut le volume
             chasse divise par la circonference, soit d x a / 2 = 0,039 rad. On
             prend 0,12 — un peu plus que le physique pour que ca se voie, pas
             assez pour brouiller la partition. */
          rho:0.085, ub:0.35, B:0.32, U:0.50 };
function emp(p,doigt){var o={};for(var k in EMP)o[k]=EMP[k];
  if(doigt&&DOIGTS[doigt]){var D9=DOIGTS[doigt];o.a=D9.a;o.el=D9.el;o.dmax=D9.dmax;}
  o.p=p;return o;}

/* le froisse : trois bandes, toutes >= 9 tours SUR LES TROIS AXES */
/* ⚑ SIX ONDES PLANES OBLIQUES — plus aucun axe, plus aucune grille.
   Les directions sont prises sur une spirale de Fibonacci et les normes sont
   irrationnelles entre elles : rien ne se repete, rien ne s'aligne. Amplitude
   totale divisee par deux : Tom veut « simple, beau et subtil », et le relief
   n'a pas a se voir — il n'est la que pour accrocher la lumiere rasante. */
var FROISSE=(function(){
  var D=[[ 0.62, 0.31, 0.72],[-0.47, 0.83,-0.30],[ 0.18,-0.55, 0.81],
         [-0.79,-0.37, 0.49],[ 0.34, 0.88, 0.33],[ 0.71,-0.62,-0.33]];
  var K=[ 9.7, 13.1, 17.9, 23.3, 29.1, 37.7];
  /* ⚑ ON GARDE LES SIX A INCLINAISON EGALE, ET ON BAISSE TOUT.
     A x K est l'inclinaison que l'onde donne a la fibre, et les six valaient
     0,12 chacune. Essai fait et MESURE : faire monter A x K avec K (pour que
     le bas du spectre cesse de faire des taches) sort un QUADRILLAGE de pois
     pales — des qu'une frequence domine, on lit sa periode. Six ondes de meme
     inclinaison se somment en bruit, une seule se lit comme un motif. Donc on
     ne touche pas a la REPARTITION : on divise l'ENSEMBLE par deux, et c'est
     le degrade qui reprend la main sur le grain. */
  var A=[0.0059,0.0041,0.0029,0.0019,0.0012,0.0007];
  var PH=[0.4,1.9,2.7,0.9,1.4,2.2], R=[];
  for(var i=0;i<D.length;i++)
    R.push([A[i], D[i][0]*K[i], D[i][1]*K[i], D[i][2]*K[i], PH[i]]);
  return R;
})();
/* l'enveloppe : deux ondes obliques, basse frequence. Elle module l'AMPLITUDE
   du relief — jamais la forme, et jamais sur un axe. */
/* ⚑ L'ENVELOPPE S'ADOUCIT. A 0,22 + 0,78 elle faisait varier l'amplitude du
   relief de un a cinq : de grands plateaux clairs a bord franc, qu'on lit
   comme des FACETTES sous une lumiere uniforme. De un a deux suffit — la
   matiere respire sans se decouper. */
/* ⚑ ET FINALEMENT L'ENVELOPPE DISPARAIT. Meme a 0,74 + 0,26 elle laissait des
   TACHES RONDES PALES, grandes comme un cinquieme de la boule : sa frequence
   est de l'ordre de la boule elle-meme, donc tout ce qu'elle peut produire est
   une tache. Elle etait la pour « faire respirer la matiere » — mais la
   respiration se lit dans le grain, pas dans des nuages, et ces nuages
   passaient DEVANT le degrade qu'on venait de poser. Amplitude nulle : la
   fourrure est uniforme, et la seule variation large de la boule est la
   lumiere. */
var ENV=[1.0,0.0, 1.31,0.77,-1.05,0.4, -0.83,1.49,0.61,1.9];
/* ⚑ LA NORMALE QUI ECLAIRE N'EST PAS LA DIRECTION QUI PEIGNE.
   A 2,5, le relief inclinait la normale de chaque poil de vingt degres : deux
   poils voisins ne tombaient pas sur la meme marche, et la surface sortait en
   POIVRE ET SEL — des tirets noirs sur du violet, ce qui n'est pas un velours,
   c'est du gravier. La lumiere doit varier LENTEMENT (c'est ca, un degrade) et
   le grain doit venir du SENS du poil, pas de son ton. On separe : la normale
   d'eclairage redevient presque celle de la sphere, la direction du peigne ne
   bouge pas. */
var KN=0.55;
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
    /* ⚑ UN VELOURS, PAS UNE FOURRURE. Le pelage etait long (jusqu'a 13 px sur
       un cadre de 620) : ca fait une bete, pas une matiere. Un velours est
       DENSE ET RAS — et le ras durcit la silhouette, parce qu'un poil court
       deborde moins du contour. Divise par deux et demi.
       Index 0 = LA COUPE DES DALLES ; 1 a 3 = le velours, par profondeur.
       Le rapport entre les deux tombe de 3,8 a 2,3 : une dalle n'est plus une
       INCLUSION posee dessus, c'est LE MEME VELOURS, coupe plus court. */
    /* ⚑ ET LE POIL S'ALLONGE POUR REDEVENIR UN POIL.
       A 1,9-5,5 sur un cadre de 620, une meche fait moins de quatre pixels de
       long pour un demi-pixel d'epaisseur : a cette taille elle ne se lit plus
       comme un BRIN, elle se lit comme un GRAIN — et une matiere en grains est
       du daim, pas de la fourrure. La delicatesse d'un pelage vient de ce que
       l'oeil suit chaque brin sur quelques pixels et voit qu'ils vont tous a
       peu pres dans le meme sens. On allonge d'un tiers ; l'epaisseur, elle,
       est deja au plancher d'un demi-pixel et ne bouge pas. Les meches se
       recouvrent donc davantage, ce qui augmente aussi la couverture. */
    var TAI0=[2.5,4.4,5.7,7.3], ATLC={};
    function atlasPour(css){
      if(ATLC[css]) return ATLC[css];
      var k=css/620, T=[TAI0[0]*k,TAI0[1]*k,TAI0[2]*k,TAI0[3]*k];
      ATLC[css]={a:atlasAlpha(GRAIN_POIL,T,ORI,NIVA,0.15,0.78,true,NVAR), t:T};
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
             env:ENV,kn:KN,lac:opt.lac===undefined?2.9:opt.lac,tan:0.32,
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

      /* ⚑ ON NE RECOPIE PLUS A LA MAIN — C'EST LA MEME FAUTE, DEUX FOIS.
         La premiere fois, `velours`, `contre`, `duvet`, `grade` et `dresse`
         n'arrivaient jamais au peintre : huit cadres identiques au pixel pres.
         Je l'ai « corrige » en ajoutant CES cinq noms a la liste. La faute
         etait la liste elle-meme : au lot suivant, `traces` et `six` sont
         tombes dans le meme trou — « marque » et « relisse » sont sortis
         identiques a 0,00 %, et LES SIX PAR LA MATIERE N'ONT JAMAIS ETE
         APPLIQUES, sans une seule erreur.
         On recopie donc TOUT ce que l'appelant a pose et que `o` ne porte pas
         encore. Une option nouvelle arrive au peintre sans qu'on y pense. */
      for(var _k in opt){
        if(_k==='id'||_k==='M') continue;
        if(o[_k]===undefined) o[_k]=opt[_k];
      }
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
        /* un poil deux fois et demie plus court couvre d'autant moins :
           on reseme pour garder la matiere PLEINE. */
        /* ⚑ 110 000 — ET C'EST LE VRAI PLAFOND, MESURE EN ROTATION LENTE.
           ⚠ J'AVAIS CONCLU FAUX. Mon premier relevé donnait deux régimes :
           360 000 au repos (image gardée, 0,00 ms) et 110 000 en mouvement.
           Ça supposait un état IMMOBILE — et il n'existe pas : la rotation
           lente est acquise depuis le début du chantier, l'Orbite tourne
           toujours. Un chiffre mesuré sur un état qui n'existe pas ne vaut
           rien. Conclusion retirée.
           Remesure, `scratchpad/banc_lent.py`, rotation permanente au rythme du
           produit (un tour en ~50 s, 0,0021 rad par image), 80 images par
           palier, dans le vrai #auraScreen avec tout l'écran autour :
             160 000 x1,00   mediane 21,30 ms   80 images sur 80 au-dessus de 20
             130 000 x1,00   mediane 18,30 ms    4 sur 80
             110 000 x1,00   mediane 16,20 ms    2 sur 80   <- le plafond
             110 000 x1,70   mediane 21,30 ms   80 sur 80
              90 000 x1,70   mediane 18,30 ms    0 sur 80
              75 000 x1,90   mediane 17,30 ms    0 sur 80, mais 0,23 % d'encre
           ⚑ ET GROSSIR LE BRIN NE RACHETE PAS LA DENSITE. La couverture vaut
           N x surface du brin, donc en theorie oui — mais le cout suit la
           MEME loi : a 110 000 x 1,70 on retrouve la matiere de 160 000 et on
           en paie exactement le prix (21,3 ms les deux fois). Il n'y a pas de
           repas gratuit de ce cote-la.
           Reste 110 000 a taille normale : 16,20 ms de mediane, 0,05 % du
           disque encore a l'encre, et au zoom 2 la matiere tient — un peu plus
           grenue qu'a 160 000, imperceptible a la taille reelle (342 px).
           ⚠ Mesure sur un Mac, dans la vraie page : c'est un PLAFOND HAUT, pas
           une garantie. A reconfirmer sur appareil. */
        SEM=semisPavage(110000,77,0.0,KDENS,4,false,0);
      }
      var o2={}; for(var q9 in opt)o2[q9]=opt[q9];
      o2.pxr=620*0.438; o2.palette=pal||Toile.getPalette();
      var T=batIles(n, Toile.cols(), o2);
      return (ORB[cle]={tr:T, pal:Toile.cols(), cle:cle, sem:SEM, libre:false,
                        derniere:T.derniere});
    }
    /* le reglage retenu : lustre de fibre, contre-jour, limbe duveteux,
       grading, et les iles qui se dressent. */
    /* `dresse` sort : une dalle n'est plus en relief, elle est TONDUE. */
    /* le lustre et le contre-jour reviennent, mais DOUX : a 1,15 ils
       ajoutaient a eux seuls des bandes claires et sombres, c'est-a-dire
       exactement ce qu'on cherche a supprimer. */
    /* ⚑ UN ECLAIRAGE SIMPLE. Le lustre de fibre (Kajiya-Kay) pose une BANDE
       claire perpendiculaire au peignage : sur un velours peigne en volutes,
       ces bandes se croisent et ajoutent leur propre motif. C'est joli en
       mouvement, c'est du bruit sur une image fixe. On le garde tres bas — il
       ne doit plus que TIEDIR la matiere, pas la dessiner. */
    /* ⚑ ON COUPE TOUT CE QUI POSE UN MOTIF. Le lustre de fibre dessine des
       bandes, le contre-jour dessine un anneau : sur une image fixe ce sont
       deux motifs de plus, et Tom a raison — ca complexifie. Il ne reste que
       la matiere et un degrade presque invisible. */
    var LUX={velours:0.0, contre:0.0, duvet:0, grade:0, velours2:1, dresse:0, R:0.438};
    function av(n,pal,opt){
      var o={M:orbite(n,pal,opt)};
      for(var q in LUX) o[q]=LUX[q];
      return o;
    }

    /* ════════════════════════════════════════════════════════════════════
       ⚑ L'ORBITE DANS SA PAGE — c'est la qu'elle se juge, pas isolee.
       L'ecran Aura fait 390 x 844. Le mot-marque « Aura » est en haut a
       gauche ; c'est de LUI que vient la lumiere, suggeree. La sphere se pose
       dessous, et le fond ne change pas.
       ════════════════════════════════════════════════════════════════════ */
    function page(hote,opt,leg){
      var fg=document.createElement('figure');
      var ec=document.createElement('div'); ec.className='ecran';
      var ti=document.createElement('div'); ti.className='ecTitre'; ti.textContent='Aura';
      var bo=document.createElement('div'); bo.className='ecBoule';
      var cv=document.createElement('canvas'); cv.setAttribute('data-cad',opt.id);
      bo.appendChild(cv); ec.appendChild(ti); ec.appendChild(bo);
      fg.appendChild(ec);
      var fc=document.createElement('figcaption'); fc.innerHTML=leg; fg.appendChild(fc);
      hote.appendChild(fg);
      var AT=atlasPour(340);
      var o={css:340,R:opt.R||0.438,tailles:AT.t,atlas:AT.a,semis:opt.M.sem,relief:FROISSE,
             env:ENV,kn:KN,lac:(opt.lac===undefined?2.9:opt.lac),
             tan:(opt.tan===undefined?0.32:opt.tan),
             pal:opt.M.pal,trame:opt.M.tr,libre:opt.M.libre,
             fond:'#16171B'};
      for(var _k in opt){ if(_k==='id'||_k==='M')continue; if(o[_k]===undefined)o[_k]=opt[_k]; }
      cv.__opt=o;
      infos.push(peint(cv,o));
    }

    /* ── LES GESTES, LES SIX ─────────────────────────────────────────────
       Neuf caresses, deterministes. Et six personnes dont la proximite se lit
       DANS LA MATIERE : `k` de 0 a 1, c'est le cumul des paroles tenues avec
       elle. Leur POSITION n'encode rien — elles sont posees a intervalle egal.
       Rien ne recule jamais : une matiere ne se desature pas. */
    var TRACES=m_gestes(9,17);
    var SIX=(function(){
      var L=[], K=[0.95,0.72,0.55,0.38,0.22,0.10];
      for(var i=0;i<6;i++){
        var a=i/6*6.283185+0.4, u=Math.cos(a)*0.62, w=Math.sin(a)*0.62;
        var v=Math.sqrt(Math.max(0,1-u*u-w*w));
        /* dans le repere de la VUE puis ramene dans l'objet — le piege paye
           trois fois : « face a nous » ne veut rien dire en repere d'objet. */
        var cl=Math.cos(2.9), sl=Math.sin(2.9), ct=Math.cos(0.32), st=Math.sin(0.32);
        var zp=-w*st+v*ct, y2=w*ct+v*st;
        L.push({c:[u*cl-zp*sl, y2, u*sl+zp*cl], v:[u,w,v], r:0.20, k:K[i]});
      }
      return L;
    })();

    /* ⚑ AUCUNE TRACE AU REPOS. Neuf caresses gravees en permanence sur la
       sphere, ca n'a pas de sens : au repos l'objet est NEUF, uniforme, et
       c'est cette uniformite qui donne envie d'y toucher. La trace n'existe
       que parce qu'on vient de le toucher — elle appartient a la sequence du
       doigt, pas a l'etat de repos. */
    /* ⚑ LES TRACES REVIENNENT AU REPOS — et cette fois elles ont un sens.
       Retirees le matin meme, a raison : c'etaient des GRAVURES posees au
       hasard, qui cassaient l'uniformite d'un objet neuf. Ce n'est plus la
       meme chose : une caresse ne creuse plus rien, elle COUCHE le poil dans
       son sens (voir `champPoil`). L'objet au repos porte donc ses traces, et
       on doit voir SANS TOUCHER que quelqu'un s'en est occupe.
       Une Orbite neuve, elle, n'en a aucune : personne ne l'a encore touchee. */
    function av2(n,pal,extra){
      var o=av(n,pal);
      o.six=SIX;
      o.pousse=Math.min(1,n/34);
      /* ⚑ LA MAIN DOIT SE VOIR AU REPOS — ET UNE CARESSE EST LARGE.
         `m_gestes` donne des arcs de 0,055 a 0,13 rad, soit trois a sept
         degres : c'est un ONGLE, pas une pulpe. La pulpe d'un pouce couvre
         0,27 rad (§ de l'empreinte, mesure sur l'ecran). A cette largeur-la
         une caresse ne se voyait pas, et c'etait pourtant la seule chose que
         personne d'autre n'a. On elargit les arcs au diametre du doigt et on
         monte ce qu'ils ont poli. */
      o.traces=[];
      if(n){
        var _G=m_gestes(Math.min(7,1+(n/5|0)),17);
        for(var _t=0;_t<_G.length;_t++){
          _G[_t].w=0.115+_G[_t].w*1.35;
          _G[_t].f=Math.min(1,0.62+_G[_t].f*0.55);
        }
        o.traces=_G;
      }
      if(extra) for(var q in extra) o[q]=extra[q];
      return o;
    }

    /* ── L'ECRAN AURA ──────────────────────────────────────────────────── */
    var rP=rang('L’écran Aura',
      'La sphère dans sa page. Le mot-marque <b>Aura</b> est en haut à gauche — et c’est de lui '+
      'que vient la lumière, <b>suggérée</b> : aucune source, aucun reflet, aucun liseré. '+
      'Un seul dégradé, mesuré du coin haut-gauche au coin bas-droit : <b>161 → 53</b> de '+
      'luminance, un facteur trois, sans une marche visible.','tri');
    var pv=av2(0);  pv.id='pg-vide';   page(rP,pv,'<b>Vide.</b>');
    var pc=av2(5);  pc.id='pg-cinq';   page(rP,pc,'<b>5 Promi.</b>');
    var pt=av2(30); pt.id='pg-trente'; page(rP,pt,'<b>30 Promi.</b>');

    /* ════════════════════════════════════════════════════════════════════
       ⚑ L'ECRAN AURA COMPLET — LE PARTI DE TOM, ECRIT EN ENTIER.
       La sphere ne porte plus que le velours, ses dalles, et la memoire de la
       main. QUI EST QUI se lit DESSOUS, en anneaux du §2.9 : une piste a la
       couleur de la nature, un arc menthe, un visage, un prenom. C'est la
       qu'on lit la relation ; la sphere, elle, redevient une image — et une
       image sans nom dessus, donc PARTAGEABLE.
       ════════════════════════════════════════════════════════════════════ */
    var K872=0.872;                       /* le document est en 390, le gabarit en 340 */
    /* ⚑ L'AVATAR DU PRODUIT, BRANCHE TEL QUEL.
       ⚠ J'avais RETIRE SANS REMPLACER : en enlevant la couleur de nature des
       visages (elle etait arbitraire), il ne restait que six silhouettes grises
       identiques — en theme sombre elles disparaissaient, et on ne distinguait
       plus personne. C'est pourtant a ca que sert cette rangee.
       La reponse existe deja dans l'app : `avatarHTML` / `_blobBg` — une vraie
       PHOTO si elle existe, sinon l'IMAGE ABSTRAITE generee, deterministe a
       partir du nom, avec sa palette `_BPAL` et sa texture de bruit en
       soft-light. On la reprend a l'identique, hachage compris : deux personnes
       differentes n'ont jamais la meme image, et la meme personne a toujours la
       sienne. C'est ca qui identifie quelqu'un — pas une couleur de nature. */
    var _BPAL=['#3A54FF','#8fa0ff','#D0B0FF','#b98cff','#F07A2E','#5f78ff'];
    function _hashN(s){var h=2166136261; s=''+s;
      for(var i=0;i<s.length;i++){h^=s.charCodeAt(i); h=(h*16777619)>>>0;} return h;}
    function _blobBg(seed){
      var h=_hashN(seed)>>>0, L=[];
      for(var i=0;i<4;i++){
        var hx=Math.imul(h,((i*2+1)*2654435761)>>>0)>>>0;
        var x=8+(hx%84), y=8+((hx>>>7)%84), sp=38+((hx>>>14)%34);
        var col=_BPAL[(hx>>>3)%_BPAL.length];
        L.push('radial-gradient(circle at '+x+'% '+y+'%,'+col+' 0%,transparent '+sp+'%)');
      }
      var base=_BPAL[(h>>>11)%_BPAL.length];
      return L.join(',')+',radial-gradient(circle at 50% 50%,'+base+' 0%,'+base+' 100%)';
    }
    var _NOISE=(function(){try{
      var c=document.createElement('canvas'); c.width=c.height=96;
      var g=c.getContext('2d'), im=g.createImageData(96,96), d=im.data;
      for(var i=0;i<d.length;i+=4){var v=140+Math.random()*115;
        d[i]=d[i+1]=d[i+2]=v; d[i+3]=Math.random()*24;}
      g.putImageData(im,0,0); return c.toDataURL();
    }catch(e){return '';}})();
    function visage(d,nom,photo){
      var w=document.createElement('div');
      w.style.cssText='width:'+d+'px;height:'+d+'px;border-radius:999px;overflow:hidden;'+
        'position:relative;'+
        (photo?('background:center/cover url('+photo+')'):('background:'+_blobBg(nom)));
      if(!photo && _NOISE){
        var nz=document.createElement('div');
        nz.style.cssText='position:absolute;inset:0;background:url('+_NOISE+');'+
          'background-size:88px 88px;opacity:.5;mix-blend-mode:soft-light;border-radius:inherit';
        w.appendChild(nz);
      }
      return w;
    }
    /* ⚑ TROIS ARCS PAR NOYAU — ce sont EUX que la legende nomme.
       Un seul arc menthe ne pouvait pas porter une legende a trois entrees. */
    /* `nom` est a la fois LE LIBELLE et LA GRAINE de l'avatar ; `photo` est la
       vraie photo si la personne en a une. `piste` est la piste de l'anneau —
       NEUTRE : une personne n'a pas de nature (§2.9 corrige). */
    function noyauUI(dia,ep,dph,piste,parts,nom,gros,photo){
      /* piste = teinte de la nature, arc = menthe, part = ce qui est tenu */
      var w=document.createElement('div'); w.className='n'+(gros?' moi':'');
      var box=document.createElement('div');
      box.style.cssText='position:relative;width:'+dia+'px;height:'+dia+'px';
      var s=document.createElementNS('http://www.w3.org/2000/svg','svg');
      s.setAttribute('viewBox','0 0 '+dia+' '+dia);
      s.setAttribute('width',dia); s.setAttribute('height',dia);
      s.style.cssText='position:absolute;left:0;top:0';
      var r=(dia-ep)/2, cx=dia/2, C=2*Math.PI*r;
      function arc(col,frac,rot){
        var a=document.createElementNS('http://www.w3.org/2000/svg','circle');
        a.setAttribute('cx',cx); a.setAttribute('cy',cx); a.setAttribute('r',r);
        a.setAttribute('fill','none'); a.setAttribute('stroke',col);
        a.setAttribute('stroke-width',ep); a.setAttribute('stroke-linecap','butt');
        if(frac<1){ a.setAttribute('stroke-dasharray',(C*frac)+' '+(C*(1-frac)));
                    a.setAttribute('transform','rotate('+rot+' '+cx+' '+cx+')'); }
        s.appendChild(a);
      }
      arc(piste,1,0);                          /* la piste, neutre */
      var an9=-90, GA=2.6;
      for(var z9=0;z9<parts.length;z9++){
        var pc9=parts[z9]*100;
        if(pc9>GA) arc(ETA[z9][1],(pc9-GA)/100,an9);
        an9+=pc9*3.6;
      }
      box.appendChild(s);
      var f=visage(dph,nom,photo);
      f.style.position='absolute'; f.style.left=((dia-dph)/2)+'px'; f.style.top=((dia-dph)/2)+'px';
      box.appendChild(f);
      w.appendChild(box);
      var lb=document.createElement('div'); lb.className='lb'; lb.textContent=nom;
      w.appendChild(lb);
      return w;
    }
    /* ⚠ SECOND TELESCOPAGE, ET LA REPONSE EST FRANCHE : CETTE COULEUR ETAIT
       ARBITRAIRE. Je l'avais ecrite a la main dans ce tableau, sans regle
       derriere — ce n'etait la Nuee de personne. Une personne n'est ni un Promi
       ni un Chiche : elle n'a pas de nature, donc elle n'a pas de couleur de
       nature. Le visage passe au NEUTRE (l'encre ou la creme du theme), et il
       ne reste de colore que ce qui porte du sens : les arcs d'etat.
       ⚠ Meme probleme sur LA PISTE de l'anneau : le §2.9 la veut « teinte de la
       nature », ce qui n'existe pas pour une personne. Elle passe au neutre
       aussi, et c'est un point a trancher. */
    var GENS=[['Rachel',0.82],['Malik',0.64],['Jo',0.55],
              ['Inès',0.41],['Sacha',0.30],['Nour',0.22]];
    /* ⚠ LES IDS DOIVENT EXISTER DANS LA TOILE SYNCHRONISEE. La planche fait
       `Toile.sync([1..20])` : un id hors de cette liste rend un canevas VIDE,
       en silence — cinq dalles sur six manquaient. */
    /* ⚑ LE MONDE DE LA PLANTATION, CABLE. Un Promi porte {m,p,h}, fige par sa
       fabrique au moment ou il est plante (lot du 4 septembre). `dalleTrame`
       prend ce 4e argument depuis ce jour-la — il n'avait JAMAIS ete cable, et
       les six dalles sortaient toutes dans le monde courant. C'est une regle du
       produit, pas un detail : la diversite des dalles est ce qui rend la Toile
       vivante. */
    var MONDES_P=['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons'];
    var MOISSON=[['planter un arbre',3,'touffe'],['nager le mardi',7,'sillons'],
                 ['appeler Mamie',11,'braille'],['le grand plongeoir',14,'mosaique'],
                 ['courir dimanche',17,'gravure'],['l’atelier du samedi',19,'encre']];
    /* ⚑ LE REGISTRE EST CELUI DU REJEU : un clin d'oeil complice, jamais un
       bilan, jamais une description de la matiere. Mes cinq phrases decrivaient
       l'objet — c'etait un inventaire, pas une voix. */
    var MOTS=['Rien de ce qui est ici n’a été dit à la légère.',
              'Tout ça, tu l’as dit. Et tu l’as fait.',
              'On ne dirait pas comme ça, mais c’est du solide.',
              'Il y en a, des paroles tenues.',
              'Et dire que tout ça, c’est toi.'];
    /* ⚑ L'ANNEAU — LA SEULE MESURE DE L'ECRAN, ET ELLE NE SE LIT PAS EN
       CHIFFRES. Trois arcs autour de la sphere : tenues, en cours, a tenir.
       Aucune valeur lisible, aucun pourcentage, aucun mot d'etat sur l'arc —
       c'est LA LEGENDE qui nomme les trois, en dessous. */
    var ETA=[['tenues','#2BE88C'],['en cours','#8FA0FF'],['à tenir','#F07A2E']];
    function anneau(d,parts){
      var s=document.createElementNS('http://www.w3.org/2000/svg','svg');
      s.setAttribute('viewBox','0 0 '+d+' '+d);
      var r=d/2-3.2, C=2*Math.PI*r, ang=-90, GAP=2.4;   /* 2,4 % de vide entre deux arcs */
      for(var i=0;i<parts.length;i++){
        var pc=parts[i]*100; if(pc<=GAP) continue;
        var a=document.createElementNS('http://www.w3.org/2000/svg','circle');
        a.setAttribute('cx',d/2); a.setAttribute('cy',d/2); a.setAttribute('r',r);
        a.setAttribute('fill','none'); a.setAttribute('stroke',ETA[i][1]);
        a.setAttribute('stroke-width',5); a.setAttribute('stroke-linecap','butt');
        a.setAttribute('stroke-dasharray',(C*(pc-GAP)/100)+' '+(C*(100-pc+GAP)/100));
        a.setAttribute('transform','rotate('+ang+' '+(d/2)+' '+(d/2)+')');
        s.appendChild(a); ang+=pc*3.6;
      }
      return s;
    }
    function ecranAura(hote,opt,theme,leg,vide){
      var fg=document.createElement('figure');
      var ec=document.createElement('div'); ec.className='ec2 '+theme;
      var cr='#F4EEE1';
      var ti=document.createElement('div'); ti.className='t'; ti.textContent='Aura';
      ec.appendChild(ti);
      var bo=document.createElement('div'); bo.className='bo';
      var cv=document.createElement('canvas'); cv.setAttribute('data-cad',opt.id);
      bo.appendChild(cv); ec.appendChild(bo);
      /* ⚠ L'ANNEAU AUTOUR DE LA SPHERE SORT. Il faisait DOUBLON avec le Noyau
         « toi » juste en dessous : deux anneaux a trois arcs qui disent la meme
         chose. Le mien porte mon visage et vit dans la rangee des six, il a sa
         place ; celui de la sphere cerclait un objet qui n'est pas moi. */

      if(vide){
        /* ⚑ L'ETAT VIDE — deux phrases suffisent. Pas d'injonction, pas de
           point d'exclamation : le velours nu est deja beau, la phrase ne fait
           que dire ce qui peut y arriver. */
        var iv=document.createElement('div'); iv.className='inv';
        iv.innerHTML='La première parole laissera sa trace ici.'+
          '<em>Tout commence par une parole donnée.</em>';
        ec.appendChild(iv);
      } else {
        /* ⚠ LE MOT QUALIFIE L'OBJET, JAMAIS LA PERSONNE. Ni note, ni verdict :
           « ta parole est solide » est un jugement sur quelqu'un, et le chiffre
           d'harmonie etait une valeur qui DESCEND par inaction. Les deux
           sortent. Ce qui reste dit ce que la sphere EST devenue. */
        var mt=document.createElement('div'); mt.className='mot';
        mt.textContent=opt.mot||MOTS[0];
        ec.appendChild(mt);

        /* les six : piste et visage NEUTRES — une personne n'a pas de nature */
        var NEU=(theme==='clair')?'#DED7C6':'#2A2C34';
        var PHOTO_MOI=null;   /* pas de photo dans le jeu de demonstration */
        var nx=document.createElement('div'); nx.className='nx';
        nx.setAttribute('data-glisse','1');   /* elle defile : voir la CSS */
        nx.appendChild(noyauUI(68,7,42,NEU,[0.58,0.27,0.15],'toi',1,PHOTO_MOI));
        var gp=document.createElement('div'); gp.className='gp';
        for(var i=0;i<GENS.length;i++){
          var t9=GENS[i][1], e9=(1-t9)*0.62;
          gp.appendChild(noyauUI(51,5,31,NEU,[t9,e9,1-t9-e9],GENS[i][0],0,null));
        }
        nx.appendChild(gp); ec.appendChild(nx);

        /* ⚑ LA LEGENDE DESCEND SOUS LA RANGEE DES SIX. C'est le seul endroit du
           produit ou le code couleur s'explique, et elle nomme LES ARCS DES
           NOYAUX — qui sont juste au-dessus d'elle, et les memes que partout
           ailleurs. Au-dessus de la rangee elle ne nommait rien de precis. */
        var lg=document.createElement('div'); lg.className='lg';
        /* elle se declare centree : le juge de l'air verifie les deux ecarts */
        lg.setAttribute('data-centre-entre','.nx|.mo h3');
        for(var e2=0;e2<ETA.length;e2++){
          var sp=document.createElement('span');
          sp.innerHTML='<i style="background:'+ETA[e2][1]+'"></i>'+ETA[e2][0];
          lg.appendChild(sp);
        }
        ec.appendChild(lg);

        var mo=document.createElement('div'); mo.className='mo';
        /* ⚠ LE LEXIQUE DU TITRE ETAIT FAUX. « Tes paroles tenues » ne couvre ni
           les Chiche ni les Nuees, alors qu'ils sont la. « Ce que tu as tenu »
           englobe les trois natures sans en nommer aucune. */
        var h3=document.createElement('h3'); h3.textContent='Ce que tu as tenu';
        mo.appendChild(h3);
        var gr=document.createElement('div'); gr.className='gr';
        for(var m=0;m<3;m++){
          var c=document.createElement('div'); c.className='c';
          var bx=document.createElement('div'); bx.className='bx';
          var dc=document.createElement('canvas');
          dc.setAttribute('data-moisson',MOISSON[m][1]);
          dc.setAttribute('data-monde',MOISSON[m][2]);
          bx.appendChild(dc); c.appendChild(bx);
          var sp2=document.createElement('span'); sp2.textContent=MOISSON[m][0]; c.appendChild(sp2);
          gr.appendChild(c);
        }
        mo.appendChild(gr); ec.appendChild(mo);
      }
      /* ⚑ LA PORTE MANQUANTE. L'aide l'annonce en gratuit, le mode existe cote
         partage — l'Aura n'avait toujours pas son bouton. */
      var bt=document.createElement('div'); bt.className='bt';
      bt.textContent='Partager mon Noyau'; ec.appendChild(bt);

      fg.appendChild(ec);
      var fc=document.createElement('figcaption'); fc.innerHTML=leg; fg.appendChild(fc);
      hote.appendChild(fg);
      var AT=atlasPour(258);
      /* ⚠ L'ANNEAU NE DOIT PAS TOUCHER LA SPHERE. A R = 0,438 le velours
         arrivait au ras des arcs : ca se lisait comme un cerclage, et le
         moindre poil qui deborde salissait l'arc. On rentre la boule — l'air
         entre les deux fait que l'anneau se lit comme une mesure POSEE AUTOUR,
         pas comme un contour de l'objet. */
      /* ⚑ ET LE SOL SE CALCULE, IL NE SE CHOISIT PAS. ⚠ Sur les deux captures
         precedentes il sortait MAUVE — pas parce que la Nuee dominait, mais
         parce qu'aucun calcul n'etait branche : le sol prenait la couleur de la
         palette du Studio. Le jeu de demonstration ne contient QUE des Promi
         (`Toile.sync` ne plante que ca, une Nuee ne nait que de `addNuee`, que
         la planche n'appelle jamais). La nature la plus presente est donc
         PROMI, et le sol doit etre BLEU. */
      var NAT_MAJ={promi:[58,84,255], chiche:[250,34,88], nuee:[138,92,240]};
      var o={css:258,R:0.392,sol:NAT_MAJ[opt.nature||'promi'],
             tailles:AT.t,atlas:AT.a,semis:opt.M.sem,relief:FROISSE,
             env:ENV,kn:KN,lac:2.9,tan:0.32,pal:opt.M.pal,trame:opt.M.tr,libre:opt.M.libre,
             fond:(theme==='clair')?'#F4EEE1':'#16171B'};
      for(var _k in opt){ if(_k==='id'||_k==='M'||_k==='mot')continue; if(o[_k]===undefined)o[_k]=opt[_k]; }
      cv.__opt=o;
      infos.push(peint(cv,o));
      if(vide) return;
      var dl=ec.querySelectorAll('canvas[data-moisson]');
      function peintMoisson(){
        for(var q=0;q<dl.length;q++){
          var d9=dl[q], b9=d9.parentNode.getBoundingClientRect();
          if(!b9.width) continue;
          d9.width=176; d9.height=112;
          var mn=d9.getAttribute('data-monde');
          try{ Toile.dalleTrame(d9, +d9.getAttribute('data-moisson'), 1,
                 mn?{m:mn, p:Toile.getPalette(), h:0}:undefined); }catch(e){}
        }
      }
      peintMoisson(); setTimeout(peintMoisson,120); setTimeout(peintMoisson,420);
    }
    var rA=rang('L’écran Aura, en entier',
      'La sphère en haut : <b>le velours, ses dalles dans leur monde d’origine, et la '+
      'mémoire de la main</b> — rien d’autre. Elle ne dit plus qui est qui, et c’est ce qui '+
      'la rend <b>partageable</b> : aucun nom dessus, indéchiffrable pour un inconnu. '+
      'Dessous, les <b>Noyaux du §2.9</b> — piste à la teinte de la nature, arc menthe, '+
      'visage, prénom. C’est <b>là</b> qu’on lit la relation, sans deviner. Plus bas, '+
      '<b>la moisson</b> : ce qu’on a tenu, en vraies dalles du moteur.','duo');
    var a1=av2(24); a1.id='a-sombre'; a1.mot=MOTS[1];
    ecranAura(rA,a1,'sombre','<b>Thème sombre.</b>');
    var a2=av2(24); a2.id='a-clair'; a2.mot=MOTS[3];
    ecranAura(rA,a2,'clair','<b>Thème clair.</b>');

    var rV=rang('L’état vide — et il doit donner envie',
      'Zéro Promi. <b>Le velours nu est déjà beau</b> : c’est le test décisif, un objet qui '+
      'n’est beau qu’à trente est refusé. La phrase ne commande rien et ne s’exclame pas — '+
      'elle dit seulement ce qui peut arriver à cette matière.','duo');
    var v1=av2(0); v1.id='v-sombre'; ecranAura(rV,v1,'sombre','<b>Vide, sombre.</b>',1);
    var v2=av2(0); v2.id='v-clair';  ecranAura(rV,v2,'clair','<b>Vide, clair.</b>',1);

    /* ── UN PROMI DE PLUS : L'ORBITE TOURNE UNE FOIS ──────────────────────
       ⚑ LE LEVIER EST LE GESTE, PAS LE RENDU. Quand une parole est tenue,
       l'Orbite fait UN TOUR pour presenter la dalle qu'on vient de poser. Ce
       n'est pas un effet : c'est ce qui rend la croissance visible, parce
       qu'aucune variable globale continue ne le peut (un trente-quatrieme de
       quoi que ce soit est invisible).
       La vue qui centre une direction c se calcule, elle ne se cherche pas :
         lac = atan2(-c0, c2)      tan = atan2(c1, hypot(c0, c2))
       On le verifie en repassant c par la transformation directe — elle doit
       rendre (0, 0, 1) a 1e-6 pres. */
    function vueVers(c){
      return {lac:Math.atan2(-c[0], c[2]),
              tan:Math.atan2(c[1], Math.hypot(c[0], c[2]))};
    }
    var rG=rang('Une parole de plus — l’Orbite tourne une fois',
      'Le critère : <b>on doit voir qu’une parole s’est ajoutée, d’un coup d’œil</b>. '+
      'La dalle qu’on vient de planter se pose du côté qu’on regarde, puis <b>l’objet fait '+
      'un tour</b> pour l’amener au centre. Les anciennes ne bougent pas d’un pouce — '+
      'rien ne recule jamais.','tri');
    var g5=av2(5);  g5.id='c-cinq'; page(rG,g5,'<b>Cinq paroles tenues.</b>');
    var g6=av2(6);  g6.id='c-six';  page(rG,g6,'<b>La sixième est plantée.</b> Elle est déjà du bon côté.');
    var g7=av2(6);  g7.id='c-tour';
    var _vv=vueVers(g7.M.derniere||[0,0,1]);
    g7.lac=_vv.lac; g7.tan=_vv.tan;
    page(rG,g7,'<b>Après le tour.</b> L’Orbite l’a amenée au centre.');

    /* ⚠ LA RANGEE DES EPIS EST SUPPRIMEE. Verdict de Tom : « ca fait des
       signes BMW, ni beau ni comprehensible » — et la vraie raison n'est pas
       l'execution : UNE MATIERE NE SAIT PAS DIRE UN NOM. Un epi ne peut pas
       etre « Rachel ». Les six et le Noyau vivent maintenant SOUS la sphere,
       en anneaux lisibles (§2.9). */

    /* ── LA COULEUR DE L'ORBITE — LA NATURE, ET RIEN QUE LA NATURE ──────
       ⚠ TELESCOPAGE CORRIGE. Le sol disait « a qui » avec menthe, terracotta et
       mauve. Sur le MEME ecran, le menthe disait donc « tenu » dans un anneau et
       « a toi » sur la sphere : une couleur signal qui dit deux choses, ce que
       la grammaire du §3 interdit. Le produit a deux systemes et ils sont
       clairs — LE CHAMP DIT LA NATURE, LA LIGNE DIT L'ETAT.
       Le sol prend donc les couleurs de NATURE : bleu si ce sont surtout des
       Promi, framboise si ce sont surtout des Chiche, mauve si c'est surtout en
       Nuee. Il dit CE QU'ON PROMET, pas a qui. Menthe et terracotta ne servent
       plus qu'aux etats, nulle part ailleurs.
       Et il reste monotone : ces comptes ne font que monter, aucun ne nomme un
       manquement, aucun ne bouge quand on ne fait rien. */
    var NATURES={ promi:[58,84,255], chiche:[250,34,88], nuee:[138,92,240] };
    var rE=rang('La couleur de l’Orbite — ce que tu promets',
      'Le <b>sol</b> — la fourrure qui couvre toute la sphère — prend la couleur de la '+
      '<b>nature</b> la plus présente : <b>bleu</b> si ce sont surtout des Promi, '+
      '<b>framboise</b> surtout des Chiche, <b>mauve</b> surtout en Nuée. Il dit '+
      '<b>ce qu’on promet</b>, jamais à qui — et <b>menthe et terracotta restent aux '+
      'états</b>, nulle part ailleurs. Les dalles, elles, gardent le monde de leur '+
      'plantation : le sol n’est pas une dalle.','tri');
    var e1=av2(0,null,{sol:NATURES.promi});  e1.id='e-promi-0';
    page(rE,e1,'<b>Bleu, à vide.</b> Surtout des Promi.');
    var e2=av2(0,null,{sol:NATURES.chiche}); e2.id='e-chiche-0';
    page(rE,e2,'<b>Framboise, à vide.</b> Surtout des Chiche.');
    var e3=av2(0,null,{sol:NATURES.nuee});   e3.id='e-nuee-0';
    page(rE,e3,'<b>Mauve, à vide.</b> Surtout en Nuée.');

    var rE2=rang('Les mêmes, à trente Promi',
      'Le sol change de teinte ; les dalles ne bougent pas — chacune reste dans le monde '+
      'et la couleur de sa plantation.','tri');
    var f1=av2(30,null,{sol:NATURES.promi});  f1.id='e-promi-30';  page(rE2,f1,'<b>Bleu, à 30.</b>');
    var f2=av2(30,null,{sol:NATURES.chiche}); f2.id='e-chiche-30'; page(rE2,f2,'<b>Framboise, à 30.</b>');
    var f3=av2(30,null,{sol:NATURES.nuee});   f3.id='e-nuee-30';   page(rE2,f3,'<b>Mauve, à 30.</b>');

    /* ── LA TAILLE DU DOIGT, DANS LA PAGE, A L'ECHELLE ─────────────────── */
    var rDo=rang('Le doigt, à sa taille réelle, dans la page',
      'La pulpe se mesure : <b>17 × 12 mm</b> pour un pouce, <b>11 × 8 mm</b> pour un index. '+
      'Sur un écran de 390 pt (71,5 mm) et une Orbite de 170,8 pt de rayon, ça fait un contact '+
      'de <b>27 %</b> du diamètre pour le pouce et de <b>18 %</b> pour l’index. '+
      'C’est le capteur qui tranche — <code>Touch.radiusX / radiusY</code> — les deux valeurs '+
      'ci-dessous sont les bornes. Le cercle blanc est la pulpe, posée par-dessus, à l’échelle.','tri');
    var q0=av2(30); q0.id='q-repos'; page(rDo,q0,'<b>Au repos.</b>');
    var q1=av2(30,null,{emp:emp(1.0,'pouce'),pulpe:'pouce'}); q1.id='q-pouce';
    page(rDo,q1,'<b>Pouce</b> — 17 × 12 mm, soit 27 % du diamètre.');
    var q2=av2(30,null,{emp:emp(1.0,'index'),pulpe:'index'}); q2.id='q-index';
    page(rDo,q2,'<b>Index</b> — 11 × 8 mm, soit 18 % du diamètre.');

    /* ── LE COEUR DU CONCEPT : LA DEFORMATION, EN TROIS TEMPS ───────────── */
    var rD=rang('Le cœur du concept — la matière cède, résiste, et revient',
      'La déformation est réelle sur le moment. Puis la forme sphérique revient : '+
      '<b>la silhouette n’est jamais abîmée</b>. Ce qui reste n’est pas un creux — c’est le '+
      'poil couché : un lustré, une chroma qui a monté, un grain orienté.','tri');
    var d1=av2(30); d1.id='d-repos';
    cadre(rD,400,d1,'<b>Au repos.</b> Neuf caresses déjà dans la matière.');
    var d2=av2(30,null,{emp:emp(1.0)}); d2.id='d-doigt';
    cadre(rD,400,d2,'<b>Sous le doigt.</b> La matière cède — mais elle résiste : le creux est un plateau, pas un trou.');
    var d3=av2(30,null,{emp:emp(0.10)}); d3.traces=m_gestes(1,17); d3.id='d-apres';
    cadre(rD,400,d3,'<b>Deux secondes après.</b> La forme est revenue. La trace, elle, reste.');

    /* ── ET LE GESTE QUI REMET TOUT A NEUF ──────────────────────────────── */
    var rN=rang('Tout relisser',
      'Un geste remet le velours à neuf, toutes les traces effacées. C’est ce qui rend le '+
      'peignage <b>sans conséquence</b> : on peut jouer sans rien salir.','duo');
    var n1=av2(30); n1.traces=m_gestes(3,17); n1.id='n-marque';
    cadre(rN,470,n1,'<b>Marqué.</b> Neuf caresses.');
    var n2=av(30); n2.six=SIX; n2.traces=[]; n2.id='n-neuf';
    cadre(rN,470,n2,'<b>Relissé.</b> Le même objet, remis à neuf.');

    /* ── LA CROISSANCE ──────────────────────────────────────────────────── */
    var rC=rang('Le velours, et les dalles taillées dedans',
      'Une dalle n’est pas une inclusion posée dessus : c’est <b>le même velours</b>, coupé '+
      'plus court, dans la couleur et le monde de sa plantation.','tri');
    [[0,'<b>Vide.</b> Le test décisif.'],[5,'<b>5 Promi.</b>'],[30,'<b>30 Promi.</b>']].forEach(function(z){
      var o=av2(z[0]); o.id='v-'+z[0]; cadre(rC,400,o,z[1]);
    });

    var rG=rang('','','duo');
    var g1=av2(0); g1.id='g-vide';
    cadre(rG,620,g1,'<b>À vide, en grand.</b> Le velours seul, et la mémoire de neuf gestes.');
    var g2=av2(30); g2.id='g-plein';
    cadre(rG,620,g2,'<b>Trente Promi, en grand.</b>');

    var rS=rang('L’épreuve du partage — 200 px','','tri');
    [[0,'<b>0</b>'],[5,'<b>5</b>'],[30,'<b>30</b>']].forEach(function(z){
      var o=av2(z[0]); o.id='p-'+z[0]; cadre(rS,200,o,z[1]);
    });

    window.__infos=infos; window.__pret=true;
  },800);
});
