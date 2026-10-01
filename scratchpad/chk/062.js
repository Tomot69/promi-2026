
/* ⚑ Q74 · L'APP DÉCLARE OÙ EST SA MATIÈRE — en coordonnées d'écran 390 × 844.
   « Zéro écart » veut dire zéro sur la géométrie, les mots, les couleurs et les formes ;
   la matière est exceptée, parce qu'elle est ENGENDRÉE par le moteur et respire avec
   `performance.now()`, là où la planche l'a tracée à la main (CLAUDE.md § 8 bis).
   Un comparateur exclut donc cette zone — et rien d'autre. Elle se déclare et se mesure :
   `_zonesMatiere()` rend la liste des rectangles ET leur part de l'écran, pour qu'un
   relevé puisse l'imprimer. Un masque qui grandit se voit.
   Les boîtes viennent des passes de peinture elles-mêmes (`data-matiere`), jamais d'une
   estimation : bandeau du Fil, carte d'Index, trait de fiche, Toile d'une Nuée. */
(function(){
  /* ⚑ LES BOÎTES DE TEXTE, DÉCLARÉES DE LA MÊME FAÇON — et pour la même raison.
     La planche est composée en **Hanken Grotesk** et **Bricolage Grotesque** (Google
     Fonts, variables) ; l'app porte ses SIX FACES EMBARQUÉES — Apfel, ApfelMid, Bricolage
     (statiques), Fraunces (CLAUDE.md §6, qui interdit toute graisse hors de ces six).
     `Hanken Grotesk` N'EST PAS `Apfel` : c'est une autre fonte, que la planche a prise
     comme doublure — le document la transcrit d'ailleurs partout en « Apfel 500 ».
     Les DESSINS DE GLYPHES ne peuvent donc pas coïncider au pixel, quoi qu'on corrige,
     exactement comme la matière. Ce qui, lui, DOIT coïncider : la BOÎTE du texte — sa
     place, sa taille, sa couleur, son mot — et c'est ce que mesurent les juges de section.
     On déclare donc ces boîtes pour qu'un comparateur puisse dire les deux chiffres. */
  window._zonesTexte=function(){
    var dev=document.getElementById('device'); if(!dev) return {zones:[],part:0};
    var D=dev.getBoundingClientRect(), sc=D.width/390;
    var z=[];
    [].slice.call(document.querySelectorAll('#device *')).forEach(function(e){
      if(['CANVAS','SVG','IMG','SCRIPT','STYLE'].indexOf(e.tagName)>=0) return;
      var propre=false;
      /* ⚠ UN CHAMP DE SAISIE PORTE DES GLYPHES SANS AVOIR DE NŒUD TEXTE. `#ixSearch` et
         `#fdSearch` affichent « Rechercher » par leur `placeholder` : ils n'ont aucun
         enfant de type 3, et la boîte n'était donc pas déclarée. Mesuré : « ⌕ Rechercher »
         comptait en entier comme un écart de dessin sur l'Index et sur le Fil, alors que
         c'est exactement le cas que l'exception vise — Hanken Grotesk contre Apfel. */
      if(e.tagName==='INPUT' || e.tagName==='TEXTAREA'){
        propre = !!((e.value && (''+e.value).trim()) ||
                    (e.placeholder && (''+e.placeholder).trim()));
      } else {
        for(var i=0;i<e.childNodes.length;i++){
          var n=e.childNodes[i];
          if(n.nodeType===3 && n.nodeValue && n.nodeValue.trim()){ propre=true; break; }
        }
      }
      if(!propre) return;
      var st=getComputedStyle(e);
      if(st.display==='none'||st.visibility==='hidden'||parseFloat(st.opacity)<0.05) return;
      var r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return;
      var x0=Math.max(0,(r.left-D.left)/sc-1), y0=Math.max(0,(r.top-D.top)/sc-1);
      var x1=Math.min(390,(r.right-D.left)/sc+1), y1=Math.min(844,(r.bottom-D.top)/sc+1);
      if(x1-x0<1||y1-y0<1) return;
      z.push([x0,y0,x1-x0,y1-y0]);
    });
    var vus=0;
    for(var y=0;y<844;y+=2) for(var x=0;x<390;x+=2){
      for(var i=0;i<z.length;i++){ var q=z[i];
        if(x>=q[0]&&x<q[0]+q[2]&&y>=q[1]&&y<q[1]+q[3]){ vus++; break; } }
    }
    return {zones:z.map(function(q){ return q.map(function(v){ return Math.round(v*10)/10; }); }),
            part: Math.round(1000*vus/(195*422))/10};
  };

  window._zonesMatiere=function(){
    var dev=document.getElementById('device'); if(!dev) return {zones:[],part:0};
    var D=dev.getBoundingClientRect(), sc=D.width/390;
    var z=[];
    /* ⚠ ON NE COMPTE QUE CE QUI EST À L'ÉCRAN, ET ON ROGNE. Une feuille fermée garde ses
       canevas, simplement poussés hors cadre (mesuré : les cartes d'Index à y = 1028 pendant
       qu'une fiche est ouverte). Les compter faisait dire au masque « 100 % de l'écran ». */
    var pousse=function(x,y,w,h){
      var x0=Math.max(0,x), y0=Math.max(0,y);
      var x1=Math.min(390,x+w), y1=Math.min(844,y+h);
      if(x1-x0<1 || y1-y0<1) return;
      z.push([x0,y0,x1-x0,y1-y0]);
    };
    [].slice.call(document.querySelectorAll('canvas[data-matiere]')).forEach(function(cv){
      var st=getComputedStyle(cv);
      if(st.display==='none'||st.visibility==='hidden'||parseFloat(st.opacity)<0.05) return;
      var r=cv.getBoundingClientRect(); if(r.width<2||r.height<2) return;
      /* les unités de `data-matiere` : la base déclarée s'il y en a une (voir
         `promiTrame`), sinon la taille CSS du canevas. */
      var base=(cv.getAttribute('data-matiere-base')||'').split(',').map(Number);
      var cw = (base.length===2 && base[0]>0) ? base[0] : (parseFloat(cv.style.width)||r.width/sc);
      var ch = (base.length===2 && base[1]>0) ? base[1] : (parseFloat(cv.style.height)||r.height/sc);
      var k=(r.width/sc)/cw, k2=(r.height/sc)/ch;
      var p=cv.getAttribute('data-matiere').split(',').map(Number);
      if(p.length!==4 || isNaN(p[0])) return;
      pousse((r.left-D.left)/sc + p[0]*k, (r.top-D.top)/sc + p[1]*k2, p[2]*k, p[3]*k2);
    });
    /* la Toile pleine page : elle N'EST que de la matière — mais seulement quand on la voit.
       On le demande au navigateur, sous le doigt, plutôt que de le déduire de classes. */
    var tc=document.getElementById('toileCv');
    if(tc){ var st=getComputedStyle(tc);
      if(st.display!=='none' && st.visibility!=='hidden'){
        /* `elementsFromPoint` rend TOUTE la pile, y compris ce qui est DESSOUS : trouver
           la Toile dedans ne dit pas qu'on la voit. Elle est visible seulement si tout ce
           qui la précède est un de ses ANCÊTRES — sinon c'est une feuille par-dessus.
           Mesuré : sans ce test, le masque disait « 100 % de l'écran » sur l'Index, sur une
           fiche et sur une Nuée, la Toile restant sous la feuille ouverte. */
        var pile=document.elementsFromPoint(D.left+D.width/2, D.top+D.height*0.55);
        var i0=pile.indexOf(tc);
        var nu = i0>=0 && pile.slice(0,i0).every(function(e){ return e.contains(tc); });
        if(nu){ var r=tc.getBoundingClientRect();
          pousse((r.left-D.left)/sc,(r.top-D.top)/sc,r.width/sc,r.height/sc); } } }
    /* la part de l'écran, mesurée sur une grille — les rectangles peuvent se recouvrir */
    var vus=0;
    for(var y=0;y<844;y+=2) for(var x=0;x<390;x+=2){
      for(var i=0;i<z.length;i++){ var q=z[i];
        if(x>=q[0]&&x<q[0]+q[2]&&y>=q[1]&&y<q[1]+q[3]){ vus++; break; } }
    }
    return {zones:z.map(function(q){ return q.map(function(v){ return Math.round(v*10)/10; }); }),
            part: Math.round(1000*vus/(195*422))/10};
  };
})();
