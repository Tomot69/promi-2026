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
    var TAI0=[4.6,6.2,8.0], ATLC={};
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
        var nsem=Math.round(Math.min(1100000, Math.max(260000, 118000/(0.29*Math.max(0.12,T.plein)))));
        /* le joint : l'ecart au deuxieme site sous lequel on ne peint plus.
           C'est le filet de la Toile, et les coins s'y arrondissent. */
        /* pixel cale son bord sur une grille — c'est tout son dessin */
        var gril=(mm==='pixel')?0.044:0;
        SEMC[cle]=semisPavage(nsem,77,0.017,KDENS,4,tourne,gril);
      }
      return {tr:T, pal:Toile.cols(), cle:cle, sem:SEMC[cle], libre:LIB[cle]};
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

    var r1=rang('','','duo');
    cadre(r1,620,{id:'hero',M:M0},
      'Au repos. Monde <b>Encre</b>, palette <b>Signal</b> — ce que le Studio donne par défaut.');
    cadre(r1,620,{id:'hero-pouce',M:M0,emp:emp(1.0)},
      'Le pouce appuyé à fond. La matière cède, et les poils se couchent avec elle.');

    var r2=rang('Les huit mondes du Studio',
      'Chaque cellule est <b>une vraie dalle du moteur</b> — <code>Toile.dalleTrame</code>, '+
      'échelle 1, sa forme, sa matière, ses couleurs. Ce n’est pas une imitation de la Toile : '+
      'c’est la Toile, fermée sur elle-même. Changer de monde au Studio change l’Orbite du même '+
      'geste.','deux');
    var NOM={encre:'Encre',mosaique:'Mosaïque',touffe:'Touffe',braille:'Braille',
             pixel:'Pixel',terrazzo:'Terrazzo',gravure:'Gravure',sillons:'Sillons',
             signal:'Signal',terre:'Terre',ocean:'Océan',braise:'Braise'};
    ['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons']
    .forEach(function(m){
      var M=monde(m,'signal');
      cadre(r2,470,{id:'m-'+m,M:M}, '<b>'+NOM[m]+'</b>');
    });

    var r3=rang('Et la palette suit aussi',
      'Même monde, quatre palettes. Les teintes ne sont pas reconstruites de mon côté : ce sont '+
      'celles que le moteur a réellement peintes dans ses dalles.','quatre');
    ['signal','terre','ocean','braise'].forEach(function(k){
      var M=monde('mosaique',k);
      cadre(r3,300,{id:'p-'+k,M:M}, '<b>'+NOM[k]+'</b>');
    });

    var M1=monde('encre','signal');
    var r4=rang('Le doigt s’enfonce',
      'Le fond plat est prouvé en pixels : un cœur où rien ne bouge, là où une cloche creuse dès '+
      'le centre. Hors du contact, un poinçon plat sur un solide mou enfonce en '+
      '<b>(2/π)·asin(a/r)</b> — une cuvette large, qui vaut encore un tiers à deux fois le '+
      'rayon. C’est elle qui fait céder la matière.','trois');
    [[0.10,'À peine posé.'],[0.40,'À mi-pression.'],[1.0,'Appuyé à fond.']].forEach(function(z){
      cadre(r4,400,{id:'pr-'+z[0],M:M1,emp:emp(z[0])},z[1]);
    });

    var r5=rang('Ce que ça donne en petit',
      'La contrainte du partage : une silhouette à relief fin disparaît à 200 px. Une mosaïque de '+
      'dalles, non.','trio-petit');
    cadre(r5,200,{id:'pt-1',M:M1},'200 px, Encre.');
    cadre(r5,200,{id:'pt-2',M:monde('braille','ocean')},'200 px, Braille · Océan.');
    cadre(r5,200,{id:'pt-3',M:monde('touffe','terre')},'200 px, Touffe · Terre.');

    window.__infos=infos; window.__pret=true;
  },800);
});
