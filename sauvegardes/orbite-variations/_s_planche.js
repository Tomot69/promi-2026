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
    var TAI0=[1.8,2.4,3.1], ATLC={};
    function atlasPour(css){
      if(ATLC[css]) return ATLC[css];
      var k=css/620, T=[TAI0[0]*k,TAI0[1]*k,TAI0[2]*k];
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
    var M0=monde('encre','signal');

    /* ════════════════════════════════════════════════════════════════════
       LES VARIATIONS — on part de la reference et on ajoute une chose a la
       fois. Le temoin est toujours a gauche : sans lui on ne juge rien.
       ════════════════════════════════════════════════════════════════════ */
    var NOM={encre:'Encre',mosaique:'Mosaïque',touffe:'Touffe',braille:'Braille',
             pixel:'Pixel',terrazzo:'Terrazzo',gravure:'Gravure',sillons:'Sillons',
             signal:'Signal',terre:'Terre',ocean:'Océan',braise:'Braise',
             aurore:'Aurore',nuit:'Nuit',foret:'Forêt',lavande:'Lavande',
             agrume:'Agrume',ardoise:'Ardoise'};
    var VA=[
      ['ref',   {},
       '<b>A · la référence</b> — ce qu’on a validé. Le témoin.'],
      ['vel',   {velours:1.0},
       '<b>B · le lustre de fibre</b> — la clarté suit le SENS DU POIL, pas seulement la normale. '+
       'Le reflet d’un cylindre est une bande, pas une tache : elle glisse quand la boule tourne. '+
       'C’est ce qui rend un velours hypnotique.'],
      ['con',   {velours:1.0, contre:1.0},
       '<b>C · + le contre-jour</b> — un poil est translucide : éclairé par derrière, sa pointe s’allume. '+
       'C’est le liseré qu’on regarde en premier sur toute photo de fourrure.'],
      ['duv',   {velours:1.0, contre:1.0, duvet:1},
       '<b>D · + le limbe duveteux</b> — au bord, le poil est vu de profil, donc plus long. '+
       'Un contour net dit « calcul » ; effiloché, il dit « fourrure ».'],
      ['gra',   {velours:1.0, contre:1.0, duvet:1, grade:1.0},
       '<b>E · + le grading</b> — clé chaude, ombre froide. Aucun objet réel n’est éclairé neutre, '+
       'et l’œil lit ce couple comme « vrai » avant de nommer la forme. Cuit dans la rampe : coût nul.'],
      ['fort',  {velours:1.5, contre:1.4, duvet:1, grade:1.6},
       '<b>F · tout, poussé</b> — la même chose à 150 %. Pour voir où est le trop.'],
      ['dre',   {velours:1.0, contre:1.0, duvet:1, grade:1.0, dresse:1},
       '<b>G · LES PROMI TENUS SE DRESSENT</b> — la proposition que je défends. '+
       'Sur la Toile, 58 % des cellules sont grises : enroulées telles quelles, ça donne un '+
       'globe gris avec des confettis, et le sujet disparaît. Ici le pelage d’une dalle plantée '+
       'est plus long : elle se tient <b>plus haut</b> que le fond, la lumière rasante l’accroche, '+
       'sa silhouette déborde sur le gris. Ni la couleur ni le dessin ne changent — on lui donne '+
       'du <b>relief</b>. Ce qu’on a tenu est littéralement ce qu’on touche.'],
      ['dre2',  {velours:1.2, contre:1.2, duvet:1, grade:1.2, dresse:2},
       '<b>H · le relief poussé</b> — le même parti pris, deux fois plus marqué.']
    ];
    var M1=monde('mosaique','signal');
    var rV=rang('Rendre la boule irrésistible — une chose à la fois',
      'Le dessin ne bouge pas : c’est la même Toile enroulée. Seule la LUMIÈRE change.','tri');
    VA.forEach(function(v){
      var o={id:'v-'+v[0],M:M1};
      for(var q in v[1]) o[q]=v[1][q];
      cadre(rV,400,o,v[2]);
    });

    var rW=rang('Sur trois autres mondes, réglage E',
      'Encre, touffe, gravure — pour vérifier que ça tient partout.','tri');
    [['encre','signal'],['touffe','terre'],['gravure','ocean']].forEach(function(m){
      cadre(rW,400,{id:'w-'+m[0],M:monde(m[0],m[1]),
        velours:1.0,contre:1.0,duvet:1,grade:1.0},'<b>'+NOM[m[0]]+'</b>');
    });

    var rP=rang('Et en petit — l’épreuve du partage',
      'À 200 px, réglage E. Si ça ne tient pas là, ça ne tient pas dans une image partagée.','tri');
    [['mosaique','signal'],['braille','ocean'],['pixel','braise']].forEach(function(m){
      cadre(rP,200,{id:'s-'+m[0],M:monde(m[0],m[1]),
        velours:1.0,contre:1.0,duvet:1,grade:1.0},'<b>'+NOM[m[0]]+'</b>');
    });

    window.__infos=infos; window.__pret=true;
  },800);
});
