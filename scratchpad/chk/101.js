
(function(){
  /* ── 5 · CE QUI EST ÉCRIT SUR UN CORPS SOMBRE SE LIT ───────────────────────
     Tom : « « Au groupe · avec Adrien », « TENU » et les textes sur la terre passent en
     amande #8FE08F quand c'est tenu, en clair sinon. Là on ne les lit pas. »
     MESURÉ, fiche par fiche, en remontant au premier fond OPAQUE sous chaque texte :
        Chiche non tenu, sombre · corps #201221
           « trace pour tenir »        #291547   Δlum **6,8**
           « Au groupe · avec Adrien » #291547   Δlum **6,8**
           « LANCÉ »                   #291547   Δlum **6,8**
        Chiche TENU, sombre · terre #2B1020
           « À Marion », « TENU À DEUX »  #8FE08F   Δlum 178,0  — déjà juste
        Les mêmes en mode CLAIR, sur le corps crème : Δlum 211 — rien à corriger.
     LE DÉFAUT EST DONC : le violet « en cours » sur un corps sombre, et lui seul. Le
     terracotta « à tenir », lui, tient déjà (Δlum 82,5 sur le même corps) : **on ne repeint
     que ce qui tombe sous le 42 du §3**, jamais un signal qui se lit.
     LA VALEUR DE REMPLACEMENT SUIT CE QUI EST PEINT SOUS ELLE (§3) : **amande #8FE08F si la
     parole est tenue, crème #F7F0DE sinon**. « Tenue » se lit sur le rendu, jamais sur une
     classe posée trop tard : c'est la TERRE #2B1020 — le paysage d'une fiche tenue (v8) —
     ou un `data-etat="tenue"` déclaré par le peintre d'une carte.
     ⚠ ELLE SE RELIT, ELLE NE FIGE PAS (le piège de `lot-POLICES`, §6) : on retire d'abord
     notre propre inline, on relit ce que la cascade dit vraiment, puis on décide. */
  var AMANDE='#8FE08F', CREME='#F7F0DE', TERRE=[43,16,32], SEUIL=42;
  function col3(v){ if(!v) return null; var t=String(v).trim();
    if(t.charAt(0)==='#'){ t=t.slice(1); if(t.length===3) t=t[0]+t[0]+t[1]+t[1]+t[2]+t[2];
      if(t.length<6) return null; var n=parseInt(t.slice(0,6),16); return [(n>>16)&255,(n>>8)&255,n&255]; }
    var m=t.match(/[\d.]+/g); return (m&&m.length>=3)?[+m[0],+m[1],+m[2]]:null; }
  function lum(c){ return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
  function fondOpaque(el){ var n=el;
    while(n && n.nodeType===1){ var b=getComputedStyle(n).backgroundColor, c=col3(b);
      var a=b.match(/rgba?\([^)]*?,\s*([\d.]+)\)/);
      if(c && (!a || parseFloat(a[1])>0.85)) return c;
      n=n.parentNode; }
    return null; }
  function estTenu(el, fond){
    if(fond && Math.abs(fond[0]-TERRE[0])+Math.abs(fond[1]-TERRE[1])+Math.abs(fond[2]-TERRE[2])<14) return true;
    try{ if(el.closest('[data-etat="tenue"]')) return true; }catch(_){}
    try{ if(el.closest('.f-tenue,.dp-tenue')) return true; }catch(_){}
    return false; }
  function passe(racine){
    var n = racine || document.getElementById('device'); if(!n) return 0;
    var pris=0;
    /* ⚠ `.s4-ev` PORTE UN VISAGE : il a des enfants, donc la règle « seulement les feuilles »
       le sautait, et repeindre son `.s4-nom` ne changeait pas la couleur qu'on lit sur LUI.
       Les quatre blocs de texte d'une carte sont donc visés NOMMÉMENT — c'est le peintre qui
       leur pose une couleur, c'est sur eux qu'il faut la corriger. */
    n.querySelectorAll('#detailPoster *, .s4-carte *, .s4-carte>.s4-ev, .s4-carte>.s4-eb, .s4-carte>.s4-et, .s4-carte>.s4-ti').forEach(function(el){
      var nomme=/^s4-(ev|eb|et|ti)\b/.test(String(el.className||''));
      if(el.children.length && !nomme) return;
      var t=(el.textContent||''); if(!t.trim()) return;
      var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return;
      /* on rend d'abord ce qu'on avait posé, puis on relit la cascade */
      if(el.getAttribute('data-lis')!=null){
        el.style.removeProperty('color'); el.style.removeProperty('-webkit-text-fill-color');
        el.removeAttribute('data-lis'); }
      var cs=getComputedStyle(el);
      if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) return;
      var c=col3(cs.webkitTextFillColor||cs.color); if(!c) return;
      var f=fondOpaque(el); if(!f) return;
      if(Math.abs(lum(c)-lum(f)) >= SEUIL) return;         /* il se lit : on n'y touche pas */
      var v = (lum(f)<128 ? CREME : '#201908');   /* ⚑ v16 : crème sur le sombre, tenu compris */
      el.style.setProperty('color', v, 'important');
      el.style.setProperty('-webkit-text-fill-color', v, 'important');
      el.setAttribute('data-lis', v); pris++;
    });
    /* ⚠ UN CONTOUR AUSSI SE LIT. Le bouton « écris un mot » est cerné du violet
       « en cours » : sur le corps sombre d'un Chiche, Δlum 6,8 — la commande disparaît. Un
       texte lisible dans une boîte invisible reste un défaut ; on traite les deux ensemble. */
    n.querySelectorAll('#detailPoster *').forEach(function(el){
      var cs=getComputedStyle(el);
      var bw=parseFloat(cs.borderTopWidth)||0; if(bw<1) return;
      if(cs.borderTopStyle==='none'||cs.visibility==='hidden'||cs.display==='none') return;
      var r=el.getBoundingClientRect(); if(r.width<8||r.height<8) return;
      if(el.getAttribute('data-lisb')!=null){ el.style.removeProperty('border-color'); el.removeAttribute('data-lisb');
        cs=getComputedStyle(el); }
      var c=col3(cs.borderTopColor); if(!c) return;
      var f=fondOpaque(el.parentNode||el); if(!f) return;
      if(Math.abs(lum(c)-lum(f)) >= SEUIL) return;
      var v = (lum(f)<128 ? CREME : '#201908');   /* ⚑ v16 : crème sur le sombre, tenu compris */
      el.style.setProperty('border-color', v, 'important');
      el.setAttribute('data-lisb', v); pris++;
    });
    return pris; }
  window._lisibiliteCorps = passe;
  /* ⚑ L'ENCART DE L'INDEX — le titre a grossi, les deux lignes se recalculent.
     `.ix-count` est un ENFANT de `.scr-ti` : sa cote est relative AU TITRE, pas au plateau.
     Mesuré avant : titre à 104,5 sur 33,9 (bas 138,4), compte à 135,5 — **2,9 px de
     recouvrement**. On partage la hauteur du plateau : air de 6 entre les deux, le reste
     également en haut et en bas. Tout se dérive des hauteurs RENDUES (§8). */
  function encartIndex(){
    var p=document.querySelector('#indexSheet .enh'); if(!p) return;
    var t=p.querySelector('.scr-ti'); if(!t) return;
    var c=t.querySelector('.ix-count'); if(!c) return;
    var H=p.clientHeight; if(H<40) return;   /* la boîte INTÉRIEURE : le plateau porte un trait de 2 */
    var ht=t.getBoundingClientRect().height, hc=c.getBoundingClientRect().height;
    /* ⚑ v89 (Tom, Q347) — le compte est retiré : le titre SEUL se centre à l'encre (capitale), comme FERMER. */
    if(ht>=6 && hc<4){ try{
      var s9=(p.getBoundingClientRect().height/p.offsetHeight)||1, x9=document.createElement('canvas').getContext('2d'), c9=getComputedStyle(t);
      x9.font=c9.fontSize+' '+c9.fontFamily; var m9=x9.measureText('I'), lh9=ht/s9, em9=(m9.fontBoundingBoxAscent||0)+(m9.fontBoundingBoxDescent||0);
      if(em9>0){ var he9=(lh9-em9)/2+((m9.fontBoundingBoxAscent||0)-(m9.actualBoundingBoxAscent||0)), cap9=(m9.actualBoundingBoxAscent||0)+(m9.actualBoundingBoxDescent||0);
        var v9=Math.round((H-cap9)/2-he9)+'px'; if(t.style.top!==v9) t.style.setProperty('top',v9,'important'); p.setAttribute('data-encart','seul,'+v9); }
    }catch(_){} return; }
    if(ht<6||hc<4) return;
    /* ⚠ LE COMPTE NE DESCEND PAS : `redteam_air` l'a pris tout de suite. En centrant les deux
       lignes dans le plateau, le compte passait de 135,5 à 140 — et l'air jusqu'à la première
       carte se resserrait de **4,5** sur les quatre écrans d'Index. Or ce qui est SOUS le
       plateau ne bouge pas (§8 : l'air ne se resserre jamais). Le compte garde donc sa cote
       d'origine (49,5 du haut intérieur) et c'est LE TITRE qui remonte pour lui laisser ses 6
       px d'air. Avant le lot il n'en avait que **1,4** : les deux lignes se touchaient. */
    var AIR=6, BAS_COMPTE=49;
    var haut=Math.round(BAS_COMPTE-(ht+AIR));
    if(haut<4){ haut=4; AIR=Math.max(2, Math.round(BAS_COMPTE-ht-haut)); }
    /* ⚑ v20 (Tom, 22 sept.) — « Index est trop bas dans son encart : recentre-le. » Le titre a grossi
       (35) : on CENTRE LE BLOC À L'ENCRE — du haut de la capitale d'« Index » au bas du compte —
       dans la boîte intérieure du plateau. Les deux décalages d'encre se CALCULENT sur les métriques
       de la police (canevas), jamais sur l'image. L'air de 6 entre les deux lignes ne bouge pas. */
    /* ⚑ v21 (Tom, 22 sept.) — « le compte colle au titre ; descends-le, l'air mesuré à l'encre ».
       À l'encre, l'air titre → compte valait celui du bord (16,5) : la ligne ne se détachait pas
       d'un titre de 35. Il passe à 22 (boîtes : 6 → 11,5), le bloc reste centré. */
    AIR = 11.5;
    try{
      var sc4=(p.getBoundingClientRect().height/p.offsetHeight)||1, cx=document.createElement('canvas').getContext('2d');
      var ct=getComputedStyle(t), cc=getComputedStyle(c);
      cx.font=ct.fontSize+' '+ct.fontFamily; var mT=cx.measureText('I');
      var lhT=ht/sc4, emT=(mT.fontBoundingBoxAscent||0)+(mT.fontBoundingBoxDescent||0);
      var hautEncre=(lhT-emT)/2 + ((mT.fontBoundingBoxAscent||0)-(mT.actualBoundingBoxAscent||0));
      cx.font=cc.fontSize+' '+cc.fontFamily; var mC=cx.measureText(c.textContent||'0');
      var lhC=hc/sc4, emC=(mC.fontBoundingBoxAscent||0)+(mC.fontBoundingBoxDescent||0);
      var basEncre=(lhC-emC)/2 + (mC.fontBoundingBoxAscent||0) + (mC.actualBoundingBoxDescent||0);
      var bloc=(lhT+AIR) + basEncre - hautEncre;               /* du haut d'encre du titre au bas d'encre du compte */
      if(emT>0 && emC>0 && bloc>0){ haut=Math.round((H-bloc)/2 - hautEncre); }
    }catch(_){}
    var vt=haut+'px', vc=Math.round(ht+AIR)+'px';
    if(t.style.top!==vt) t.style.setProperty('top',vt,'important');
    if(c.style.top!==vc) c.style.setProperty('top',vc,'important');
    try{ p.setAttribute('data-encart',[H,ht,hc,haut,AIR].map(function(x){return Math.round(x*10)/10;}).join(',')); }catch(_){}
  }
  window._encartIndex=encartIndex;
  function tard(){ [0,120,420,900].forEach(function(t){ setTimeout(function(){ try{ passe(); encartIndex(); }catch(_){} }, t); }); }
  /* on ENVELOPPE les peintres, on ne se contente pas d'écouter (§8) */
  ['openDetail','setTheme','openEssaim','ouvrirIndex','buildFeed','_s4Fil','_s4Index'].forEach(function(nom){
    try{ var f=window[nom]; if(typeof f!=='function') return;
      window[nom]=function(){ var r=f.apply(this,arguments); tard(); return r; }; }catch(_){}
  });
  try{ var fb=document.getElementById('filBtn'); if(fb) fb.addEventListener('click', tard); }catch(_){}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',tard); else tard();
})();
