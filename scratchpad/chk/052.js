
/* ═══════════════════════════════════════════════════════════════════════════════════════
   SECTION 4 · LE MOTEUR DES CARTES ET DES BANDEAUX.
   Rien n'est estimé. La géométrie de la carte est celle du moodboard, relevée dans ses
   propres chemins SVG (cadres 72, 74 et les cartes isolées) :

       échelle    = hauteur de la carte / 600
       base       = LA HAUTEUR DE TRAIT FIGÉE À LA PLANTATION × échelle   (§2.5)
       amplitude  = 13 × largeur / 173                                    (§3.9)
       boîte      = ⌊ base + amplitude + 20 ⌋
       épaisseur  = 5.5 × largeur / 173 · points r = 3,2 × l/173 tous les 11 × l/173

   Vérifié sur les trois tailles du document : 165 × 198, 106 × 133, 173 × 208 — la boîte
   retombe sur 135 / 97 / 141, les valeurs des tableaux, au pixel près.
   L'onde, l'amorce, le chevron et les points viennent de `window._onde` : une seule
   formule d'onde existe dans le produit (§2.1), on l'appelle, on ne la duplique pas.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  if(!window._onde) return;
  var O=window._onde;
  var NATCOL=O.NATCOL, NATCLAIR=O.NATCLAIR, NATTRAIT=O.NATTRAIT||O.NATCLAIR, TERRA=O.TERRA, MENTHE=O.MENTHE;
  /* ⚠ 23 SEPTEMBRE 2026 — UNE CARTE DU FIL MANQUAIT, ET LA CONSOLE NE DISAIT RIEN.
     `etatEvenement` appelle `etatTrait('tenu', l)` quand l'événement est une parole tenue.
     `etatTrait` vit dans l'IIFE de l'onde ; ici elle n'existe pas — `ReferenceError`, et
     la carte est perdue en silence. Mesuré : `_filComp` déclare **5** entrées, le Fil n'en
     peignait que **4** ; la manquante est p127 (« Marion a relevé · courir dimanche »), la
     SEULE dont l'événement porte `etat:'tenue'`. C'est le piège du §8 — une aide partagée
     entre deux blocs se prend sur `window._onde`, jamais par portée. */
  var etatTrait=O.etatTrait||function(k,l){ return NATTRAIT.promi; };

  /* ═══ Q93 · QUAND LA DALLE ET LE CHAMP SE RENCONTRENT, C'EST LE CHAMP QUI CÈDE ═══
     Décision Tom, 29 août 2026. Le §3 l'emporte : **jamais de ton sur ton, nulle part**.
     Mais le §4 reste entier — **aucune teinture hors bande haute** : la dalle porte le
     MONDE, on n'y touche pas. C'est donc **la couleur du champ** qui bouge.

     POURQUOI IL LE FAUT : la couleur d'une dalle est tirée au hasard par le moteur
     (`cc()`, code de la Toile — intouchable, §9). Pour le même id 125, `dalleTrame` rend
     tantôt lavande [209,176,255], tantôt **[57,84,255] — le bleu du champ**. Une carte
     d'Index sur deux sortait alors avec une dalle invisible ; mesuré au duo sur la carte
     « planter un arbre », en clair comme en sombre, et sur le bandeau du Fil.

     COMMENT : on ne change que la LUMINOSITÉ, dans l'espace HSL — la teinte et la
     saturation de la nature ne bougent pas d'un degré, la carte reste bleue, framboise ou
     mauve. On s'écarte de la dalle jusqu'à dégager le seuil du §3 (42), et pas au-delà :
     dès que l'écart est tenu, on s'arrête. Bornes 0,10–0,90 pour ne jamais tomber sur un
     noir ni un blanc. Si la borne est atteinte avant le seuil, on prend ce qu'on peut —
     et c'est toujours mieux que l'invisible. */
  function _lum(r,v,b){ return 0.2126*r + 0.7152*v + 0.0722*b; }
  function _hex2rgb(h){ h=(h||'').replace('#',''); if(h.length===3) h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
    var n=parseInt(h,16); return [(n>>16)&255,(n>>8)&255,n&255]; }
  function _rgb2hsl(r,v,b){ r/=255;v/=255;b/=255;
    var mx=Math.max(r,v,b), mn=Math.min(r,v,b), h=0, s=0, l=(mx+mn)/2, d=mx-mn;
    if(d){ s = l>0.5 ? d/(2-mx-mn) : d/(mx+mn);
      h = mx===r ? ((v-b)/d+(v<b?6:0)) : mx===v ? ((b-r)/d+2) : ((r-v)/d+4); h/=6; }
    return [h,s,l]; }
  function _hsl2rgb(h,s,l){ if(!s) { var g=Math.round(l*255); return [g,g,g]; }
    function f(p,q,t){ if(t<0)t+=1; if(t>1)t-=1;
      if(t<1/6) return p+(q-p)*6*t; if(t<1/2) return q;
      if(t<2/3) return p+(q-p)*(2/3-t)*6; return p; }
    var q = l<0.5 ? l*(1+s) : l+s-l*s, p = 2*l-q;
    return [Math.round(f(p,q,h+1/3)*255), Math.round(f(p,q,h)*255), Math.round(f(p,q,h-1/3)*255)]; }
  /* la luminosité MOYENNE des pixels opaques d'une dalle — c'est ce que l'œil voit. */
  function _lumDalle(src){ try{
    /* ⚑ v29 — une dalle du moteur DÉCLARE sa clarté moyenne (même échantillonnage) : on la lit (redteam_decoupe) */
    if(src && src.__dalleInfo) return src.__dalleInfo.lum;
    var g=src.getContext('2d'); if(!g) return null;
    var d=g.getImageData(0,0,src.width,src.height).data, n=0, s=0;
    for(var i=0;i<d.length;i+=4*11){ if(d[i+3]>200){ n++; s+=_lum(d[i],d[i+1],d[i+2]); } }
    return n>40 ? s/n : null; }catch(_){ return null; } }
  /* ⚑ LA DÉCISION SE PUBLIE (CLAUDE.md §7 : on compare la COMPOSITION, pas les pixels d'un
     canevas qui respire). `_cede` porte « luminosité du champ, luminosité de la dalle,
     écart obtenu » ; le peintre le pose sur le canevas, et le contrôle lit ça. */
  function champCede(natCol, src, cv){
    function note(Lc,Ld){ try{ if(cv) cv.setAttribute('data-cede',
      Math.round(Lc)+','+Math.round(Ld)+','+Math.round(Math.abs(Lc-Ld))); }catch(_){} }
    var Ld = _lumDalle(src); if(Ld===null){ try{ if(cv) cv.removeAttribute('data-cede'); }catch(_){} return natCol; }
    var c = _hex2rgb(natCol), Lc = _lum(c[0],c[1],c[2]);
    if(Math.abs(Lc-Ld) >= 42){ note(Lc,Ld); return natCol; }   /* le seuil est déjà tenu */
    var hsl = _rgb2hsl(c[0],c[1],c[2]);
    /* ⚠ 23 SEPTEMBRE 2026 (Tom) — « LA DALLE MANQUE À GAUCHE. » Elle était là, et on ne la
       voyait pas : le champ n'avait cédé QUE VERS LE HAUT. `sens` partait de `Lc >= Ld` et ne
       revenait jamais — sur le Chiche (`#FFB8D2`, l 86 %, s 100 %) le plafond de clarté est
       atteint à l 90 % et la luminosité plafonne à 216 : contre une dalle rose à 201, l'écart
       s'arrêtait à **15,2** là où le §3 en demande 42. Vers le BAS le même champ atteint 42
       sans peine, en restant le rose du Chiche (teinte et saturation gardées, Q93).
       ON ESSAIE DONC LES DEUX SENS, et on garde le premier qui passe ; si aucun ne passe, le
       meilleur des deux — jamais le plus mauvais par défaut. */
    function pousse(sens){
      var l=hsl[2], best=null, bd=-1;
      for(var k=0;k<90;k++){
        l = Math.max(0.06, Math.min(0.94, l + sens*0.01));
        var q = _hsl2rgb(hsl[0], hsl[1], l), d = Math.abs(_lum(q[0],q[1],q[2]) - Ld);
        if(d>bd){ bd=d; best=q; }
        if(d >= 42) return {c:q, d:d, ok:true};
        if(l<=0.06 || l>=0.94) break;
      }
      return {c:best, d:bd, ok:false};
    }
    var haut=pousse(1), bas=pousse(-1);
    var pris = haut.ok && bas.ok ? ((Lc>=Ld)?haut:bas)      /* les deux passent : on garde le sens d'origine */
             : haut.ok ? haut : bas.ok ? bas
             : (haut.d>=bas.d ? haut : bas);                /* aucun : le meilleur des deux */
    var f = pris.c;
    note(_lum(f[0],f[1],f[2]), Ld);
    return 'rgb('+f[0]+','+f[1]+','+f[2]+')';
  }
  window._champCede = champCede;
  var CREME='#F7F0DE', ENCRE='#201908';
  var CORPS={promi:'#183759',chiche:'#351A2D',nuee:'#1B1426'};   /* §1.3 · corps de carte */

  function light(){ var d=document.getElementById('device');
    return !!(d&&d.classList.contains('light')); }

  /* ── §2.5 · LA HAUTEUR DE TRAIT. Elle n'est JAMAIS recalculée ici : on demande à la
       fiche la sienne, avec le même moteur (`window._ficheEcran`). Un faux poster suffit —
       `ecran()` ne lit que les classes de nature. C'est la garantie du §4 : la carte et la
       fiche portent exactement la même composition. ── */
  function faussePoster(nat){
    return {classList:{contains:function(c){
      if(c==='dp-chiche') return nat==='chiche';
      if(c==='dp-nuee'||c==='dp-mode-nuee') return nat==='nuee';
      return false; }}};
  }
  function etatPromi(p){
    var nat = p.chiche ? 'chiche' : (p.nuee && p.nueeFiche ? 'nuee' : 'promi');
    var e = window._ficheEcran(faussePoster(nat), p);
    return e;
  }
  /* une Nuée n'est pas un Promi : sa fiche a ses propres cotes (§5, « Nuée · avec des
     Promi » base 232, « Nuée · vide » base 282, mode complet). */
  function etatNuee(nb){
    var l=light();
    return {nat:'nuee', light:l, natCol:NATCOL.nuee, base:(nb?232:282), amp:(nb?36:44),
            mode:'complet', aplat:true, col:NATTRAIT.nuee,
            colTexte:(l?window._NATTXT.nuee:NATCLAIR.nuee)};
  }

  /* ── LA GÉOMÉTRIE D'UNE CARTE ── */
  function geo(w,h,base_fiche,fige){
    /* §2.5 · LA HAUTEUR DE TRAIT EST BORNÉE — plancher 196, plafond 344. Les fiches du
       moodboard portent des valeurs hors de cette échelle (376 pour « Promi · tenue »,
       372 pour « Chiche · tenu à deux ») : ce sont des cotes d'ÉCRAN, posées à la main sur
       844 px de haut. Reportées telles quelles sur une carte de 133, elles mangeaient le
       titre — constaté au duo, « méditer le… » coupé en plein mot, l'état par-dessus. Les
       bases relevées dans les cartes du moodboard tiennent toutes dans [204, 348] : on
       borne donc à la règle du §2.5, qui EST la règle d'une hauteur de trait. */
    /* ⚑ LA BORNE NE MORD QUE SUR UNE BASE EMPRUNTÉE À LA FICHE. Depuis que chaque Promi
       porte SA hauteur de trait figée à la plantation (§2.5, `p.ht`), il n'y a plus rien à
       corriger : la valeur est déjà une cote de CARTE. La borne reste — elle protège le
       titre quand on retombe sur la base d'une fiche (376, 372) — mais elle laisse passer
       une hauteur figée. Sans cela « le potager » sortait à 145 au lieu de 147 : sa
       hauteur est 347, trois pixels au-dessus d'un plafond qui ne le visait pas. */
    if(!fige){
      if(base_fiche>344) base_fiche=344;
      if(base_fiche<196) base_fiche=196;
    }
    var s=h/600, k=w/173;
    var base=base_fiche*s, amp=13*k;
    var boite=Math.floor(base+amp+20);
    var dh=Math.round(base-amp-13.7*(h/198));
    if(dh<10) dh=10;
    var dw=Math.floor(1.2*dh);
    if(dw>w-8){ dw=w-8; dh=Math.round(dw/1.2); }
    return {w:w,h:h,base:base,amp:amp,boite:boite,ep:5.5*k,r:3.2*k,esp:11*k,
            dalle:{x:Math.floor((w-dw)/2), y:Math.round(0.0455*h), w:dw, h:dh}};
  }

  /* ── LE TRAIT D'UNE CARTE (§2.6) — même grammaire que la fiche, à l'échelle. ── */
  function peintCarte(cv,g2,e,id){
    var W=g2.w, H=g2.h, dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
    cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
    cv.style.width=W+'px'; cv.style.height=H+'px';
    var g=cv.getContext('2d'); if(!g) return;
    g.setTransform(dpr,0,0,dpr,0,0); g.clearRect(0,0,W,H);
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';
    /* ⚠ ET SUR SA PROPRE LARGEUR. `onde` normalisait par `W` = 390, la largeur d'une
       FICHE : sur une carte de 165, l'abscisse n'atteignait jamais que t = 0,42 — on ne
       voyait donc que les deux cinquièmes de la courbe, étirés sur toute la carte.
       C'est ce qui plaçait le creux à x = 68 au lieu de 41. */
    var y=O.onde(g2.base,g2.amp,1,W);        /* §3.9 · une CARTE fait UNE période, sur SA largeur */
    /* le chemin de l'onde, à la largeur de la carte : on rejoue la Bézier du §2.1 avec
       per = 1 (§3.9), soit quatre segments d'un quart de période. */
    function chemin(a,b){
      var seg=W/4, xs=[a], x=Math.ceil(a/seg)*seg;
      while(x<b-0.5){ xs.push(x); x+=seg; } xs.push(b);
      var d=function(t){ return y(t+0.5)-y(t-0.5); };
      g.moveTo(xs[0],y(xs[0]));
      for(var i=0;i<xs.length-1;i++){ var p0=xs[i],p1=xs[i+1],hh=(p1-p0)/3;
        g.bezierCurveTo(p0+hh, y(p0)+d(p0)*hh, p1-hh, y(p1)-d(p1)*hh, p1, y(p1)); }
    }
    /* 1 · l'aplat de nature, borné en bas par l'onde — TOUJOURS. « Un champ blanc, ça ne
       doit jamais exister » (décision Tom du 29 août) : un gardé de côté garde son champ,
       c'est SA MATIÈRE qui manque, et son pointillé qui le dit.
       ⚠ ON REND LA DALLE D'ABORD. L'aplat ne peut céder que s'il sait à quoi il se compare,
       et une dalle se rend UNE FOIS (CLAUDE.md §4) : la source servira au dessin plus bas. */
    var _src=null, _o=null;
    if(!e.sansMatiere && id!==null && id!==undefined && window.Toile && Toile.dalleAbs && Toile.dalleAbs(id)){
      /* ⚑ v18 · Q297 (Tom) : sous Ingénu, la dalle est recalée sur la rampe de SA nature (le champ l'est aussi).
         ⚑ v29 — c'est le MOTEUR qui la peint recalée (`opts.rampe`), à la taille de la carte (redteam_decoupe). */
      _o={monde:undefined,   /* ⚑ v34 : le monde et la palette du Studio (Tom) */
          rampe:(window._ingenuRampe?window._ingenuRampe(id):null)||undefined};
      try{ _src=window._rendDalle(id, g2.dalle.w*dpr, g2.dalle.h*dpr, _o); }catch(_){ _src=null; }
    }
    if(e.aplat!==false){ g.beginPath(); chemin(0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath();
      g.fillStyle=(_src?champCede(e.natCol,_src,cv):e.natCol); g.fill(); }
      /* ⚑ LE CHAMP SE DÉCLARE — « un champ blanc n'existe jamais » (décision Tom, 29 août).
         Un contrôle au pixel ne peut pas trancher partout : sur une Nuée VIDE, les graines
         du §10.6 sont crème DANS LES DEUX THÈMES, et elles tombent pile sur la couleur du
         corps. Ce sont pourtant de la MATIÈRE posée sur un champ mauve, pas un champ nu.
         Le peintre, lui, sait ce qu'il a versé : il l'écrit. C'est la doctrine du §7 —
         on compare la COMPOSITION, pas la peinture. */
      try{ cv.setAttribute('data-champ', (_src?champCede(e.natCol,_src,cv):e.natCol)); }catch(_){}
    /* 2 · LA MATIÈRE. Une photo REMPLACE la dalle partout où cette matière s'affiche
         (Q53, décision Tom) : même cadrage centré, mêmes cotes — sinon la promesse aurait
         deux visages. À défaut de photo, la vraie dalle du moteur, NON TEINTÉE : dans une
         liste elle porte le MONDE, jamais la nature (CLAUDE.md §4, Q30 bis). */
    /* ⚑ Q74 · LA ZONE DE MATIÈRE EST PUBLIÉE — MAIS SEULEMENT SI ON EN A PEINT.
       Un gardé de côté n'a pas de dalle (Q83, décision Tom du 29 août : il ne pose rien
       sur la Toile, parce que rien n'a été promis — le cadre 74 qui lui en dessine une
       est une erreur, voir ECARTS-MOODBOARD § 0 bis.2). Déclarer sa boîte quand même
       masquait 72 × 60 px pour rien : un masque SANS matière dessous, exactement ce que
       le § 8 bis interdit. On efface d'abord, on ne déclare qu'après avoir dessiné. */
    try{ cv.removeAttribute('data-matiere'); cv.removeAttribute('data-matiere-base'); }catch(_){}
    var _matOK=false;
    var _nl0=(cv.parentNode&&cv.parentNode.querySelector('.s4-natlab')), _decl=null;
    if(e.mosa && e.mosa.length>1 && window._petiteToile){ var _ym=1e9; for(var _xx=0;_xx<=W;_xx+=4){ _ym=Math.min(_ym,y(_xx)); }
      _matOK=window._petiteToile(g,{x:8,y:8,w:W-16,h:_ym-14},{x:0,y:0,w:(_nl0?10+(function(el){ var W={'Promi':73,'Chiche':81,'Nuée':57,'Cercle':76};   /* ⚑ 20 sept. : PromiLate 13 px, relevées police chargée (Gilbert 12 donnait 54·60·51) */ return el ? (W[(el.textContent||'').trim()] || Math.ceil(el.offsetWidth)) : 0; })(_nl0)+4:0),h:36},e.mosa);
      var _PR=(window._ptRects||[]); if(_matOK&&_PR.length){ var _x0=1e9,_y0=1e9,_x1=-1e9,_y1=-1e9; _PR.forEach(function(r){_x0=Math.min(_x0,r[0]);_y0=Math.min(_y0,r[1]);_x1=Math.max(_x1,r[0]+r[2]);_y1=Math.max(_y1,r[1]+r[3]);});
        cv.setAttribute('data-matieres', JSON.stringify(_PR)); _decl={x:_x0,y:_y0,w:_x1-_x0,h:_y1-_y0}; } }
    else if(window._photoDansBoite && window._photoDansBoite(g, g2.dalle, id)) { _matOK=true; }
    else if(_src){
      try{ var b0=g2.dalle, _nl=(cv.parentNode&&cv.parentNode.querySelector('.s4-natlab')), _dx=Math.max(0,(_nl?10+(function(el){ var W={'Promi':73,'Chiche':81,'Nuée':57,'Cercle':76};   /* ⚑ 20 sept. : PromiLate 13 px, relevées police chargée (Gilbert 12 donnait 54·60·51) */ return el ? (W[(el.textContent||'').trim()] || Math.ceil(el.offsetWidth)) : 0; })(_nl)+8:0)-b0.x)   /* ⚠ la largeur du libellé est une COTE (Bricolage 700/12, relevée police chargée), jamais une mesure au moment de peindre : la police n'y est pas encore, le mot mesurait 53 au lieu de 64,5 et la dalle passait 3,5 px dessous (§8) */, b=((b0.w-_dx) >= b0.w*0.5) ? {x:b0.x+_dx,y:b0.y,w:b0.w-_dx,h:b0.h} : (function(){ var _dy=Math.max(0,38-b0.y); return {x:b0.x,y:b0.y+_dy,w:b0.w,h:Math.max(12,b0.h-_dy)}; })(),   /* ⚠ carte étroite (3 par ligne, 106 de large) : le libellé mangeait la largeur, la dalle n'était plus peinte (releve-S4, mesuré) — elle descend sous lui */ _pd=window._poseDalle(g,id,b.x,b.y,b.w,b.h,_o), dw=_pd?_pd.w:0, dh=_pd?_pd.h:0;   /* ⚑ v29 — à sa taille, 1:1 */
        if(!_pd) throw 0;
        _matOK=true; _decl={x:Math.round(b.x+(b.w-dw)/2),y:Math.round(b.y+(b.h-dh)/2),w:Math.round(dw),h:Math.round(dh)};   /* Q213 : la boîte DÉCLARÉE est celle qu'on a peinte, à droite du libellé */
      }catch(_){}
    }
    if(_matOK){ try{ cv.setAttribute('data-matiere',
        [(_decl||g2.dalle).x,(_decl||g2.dalle).y,(_decl||g2.dalle).w,(_decl||g2.dalle).h].join(','));
      cv.setAttribute('data-matiere-base', W+','+H); }catch(_){} }
    /* 3 · la ligne (§2.6) : la couleur d'état, jamais celle de la nature (§2.1 bis). */
    var col=e.col, ep=g2.ep, rr=g2.r, esp=g2.esp, mid=W/2;
    g.strokeStyle=col; g.fillStyle=col; g.lineWidth=ep; g.lineCap='round'; g.lineJoin='round';
    function plein(a,b){ g.beginPath(); chemin(a,b); g.stroke(); }
    function points(x0){ for(var x=x0;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x),rr,0,6.2832); g.fill(); } }
    if(e.mode==='complet'){ plein(0,W); }
    else if(e.mode==='duo'){ var gp=4*(W/173); plein(0,mid-gp); plein(mid+gp,W); }
    else if(e.mode==='points'){ var cx=W*0.11;
      O.ruban(g,y,-W*0.03, cx+ep*0.6, ep*2.2, ep*0.15); g.fill();
      O.chevron(g,y,cx,col,ep); points(cx+esp*1.3); }
    else { plein(0,mid); O.chevron(g,y,mid,col,ep); points(mid+esp); }
    try{ cv.setAttribute('data-peint','1'); }catch(_){}
  }

  /* ── LES MOTS. Aucun n'est inventé : ils viennent du moodboard (cadres 72 à 77) pour
       l'état, et de l'app pour les noms propres. ── */
  function motEtat(p,e){
    if(p.draft) return 'GARDÉ DE CÔTÉ';
    if(p.status==='tenu') return (p.chiche&&p.avec)?'TENU À DEUX':'TENUE';
    if(p.chiche && p.status!=='rate') return 'LANCÉ';
    if(p.status==='rate') return 'À TENIR';
    return 'EN COURS';
  }
  /* ⚑ LE BANDEAU DU FIL DIT L'ÉVÉNEMENT, PAS L'ÉTAT COURANT DU PROMI.
     Ce n'est pas une déduction : la planche le prouve sur le MÊME Promi.
       cadre 56 · la fiche de « le grand plongeoir »  →  TENU À DEUX · 3 AOÛT, trait menthe
       cadre 76 · le bandeau du même Promi            →  À RELEVER, trait #F5AC9E, la moitié
     Un journal enregistre ce qui s'est passé, pas où en est la chose aujourd'hui. Sans
     cette règle, aucun jeu de données ne peut satisfaire les deux cadres à la fois : le
     Fil et les fiches se contrediraient, quoi qu'on fasse.
     L'événement porte donc sa NATURE, sa COULEUR et son MOT — tous lus dans le cadre,
     aucun inventé — et le bandeau les préfère à ceux du Promi quand ils existent. */
  function etatEvenement(s, e, p){
    var l=light(), nat=s.nat||e.nat;
    var col = s.etat==='tenue'  ? etatTrait('tenu', l)   /* ⚑ 21 sept. : l'amande n'est plus un état */
            : s.etat==='atenir' ? TERRA
            : NATTRAIT[nat];
    return {nat:nat, light:l, natCol:NATCOL[nat], base:e.base, amp:e.amp,
            mode:(s.mode||'complet'), aplat:true, col:col,
            colTexte:(l?(window._NATTXT[nat]||NATCOL[nat]):col)};
  }
  function motEvenement(s, p){
    if(s.mot) return s.mot;
    if(s.nat==='nuee' && p && p.nuee){
      var nom=(typeof NUE!=='undefined'&&NUE[p.nuee])||p.nuee;
      var n=promises.filter(function(q){ return q.nuee===p.nuee && !q.draft; }).length;
      return (''+nom).toUpperCase()+' · '+n+' PROMI';
    }
    return null;
  }

  function motQui(p){
    if(p.draft) return 'gardé de côté';
    var w=(p.who||'').trim();
    if((!w || w.toLowerCase()==='moi') && p.from && p.from!=='moi') return 'de '+p.from;   /* une promesse reçue */
    if(!w || w.toLowerCase()==='moi') return 'à moi';
    return window._aQui ? window._aQui(w) : 'à '+w;
  }

  /* ═══ L'INDEX (§5 « Index 2 par ligne » / « Index 3 par ligne ») ═══
     Le crible est posé ENTRÉE PAR ENTRÉE : on relit les blocs que `buildIndex` vient
     d'écrire, on en garde l'ordre, le filtre et le tri — et on repose la présentation.
     On ne réécrit pas la logique de l'app, on porte son écran. */
  function densite(){ return (window._s4Trois===true) ? 3 : 2; }
  window._s4Index=function(){ try{
    var sh=document.getElementById('indexSheet'), li=document.getElementById('indexList');
    if(!sh||!li) return;
    /* LA LISTE D'ENTRÉES SE MÉMORISE — MAIS SEULEMENT QUAND `buildIndex` VIENT DE PARLER.
       ⚠ LE CACHE AVALAIT LE FILTRE. Une recherche sans résultat fait écrire à `buildIndex`
       un « Rien ici » et AUCUN `.ix-bloc` : je lisais alors zéro bloc, je gardais les 28
       entrées d'avant et je les reposais — la recherche ne filtrait plus rien (CASSE A6).
       « Zéro entrée » est une réponse, pas une absence de réponse. */
    if(window._s4Frais){
      window._s4Entrees=[].slice.call(li.querySelectorAll('.ix-bloc')).map(function(b){
        return b.hasAttribute('data-nuee') ? {nuee:b.getAttribute('data-nuee')}
                                           : {id:+b.getAttribute('data-id')}; });
      window._s4Vide = li.innerHTML;
      window._s4Frais = false;
    }
    var ent=window._s4Entrees||[];
    if(!ent.length){
      if(window._s4Vide && /ix-empty/.test(window._s4Vide)) li.innerHTML=window._s4Vide;
      return;
    }
    var l=light(), n=densite();
    var CW = (n===3)?106:165, CH=(n===3)?133:198, RAD=(n===3)?11:17;
    var GX = (n===3)?[24,142,260]:[24,201], PAS=(n===3)?145:210;
    var FEB=(n===3)?8.0:12.4, FTI=(n===3)?12.9:20.0, FET=(n===3)?6.4:10.0;
    var PADX=(n===3)?7:12, TXW=(n===3)?90:140;
    var DY_EB=(n===3)?14:10.5, DY_TI=(n===3)?11:17;
    var BAS_TI=(n===3)?15:24, BAS_ET=(n===3)?8:12;
    var h='<div class="s4-grille" style="height:'+(Math.ceil(ent.length/GX.length)*PAS+40)+'px"></div>';
    li.innerHTML=h;
    var gr=li.querySelector('.s4-grille');
    ent.forEach(function(b,i){
      var e, p=null, id=null, eb, et, titre;
      if(b.nuee){
        var k=b.nuee;
        var mem=(typeof NUEEMEM!=='undefined'&&NUEEMEM[k])||[];
        var lp=promises.filter(function(q){return q.nuee===k&&!q.draft;});
        e=etatNuee(lp.length);
        id=lp.length?lp[lp.length-1].id:null; e.mosa=lp.map(function(q){return q.id;});   /* ⚑ Q213 : la carte d'une Nuée porte TOUTES ses dalles, en petite Toile (`_petiteToile`) */
        titre=(typeof NUE!=='undefined'&&NUE[k])||k;
        /* « avec +4 » est le mot du moodboard ; sans membre il n'en donne aucun — on
           reprend alors celui de l'app (`buildIndex`, l.3399 : « perso »). Rien d'inventé. */
        eb=mem.length?('avec +'+mem.length):'perso';
        var _nt=lp.filter(function(q){return q.status==='tenu';}).length;
        /* ⚠ « TENU » S'ACCORDE — cadre 72 « 1 TENU », cadre 10 de `promi-nuee-toile`
           « 3 TENUS ». La carte sortait « 3 TENU ». (« PROMI » reste invariable, §2.) */
        et=lp.length+' PROMI · '+_nt+' TENU'+(_nt>1?'S':'');
        /* ⚑ UNE NUÉE SANS AUCUN PROMI EST UN GARDÉ DE CÔTÉ : elle est nommée, pas plantée.
           Le cadre 74 l'écrit ainsi — « gardé de côté · l'atelier du samedi · GARDÉ DE
           CÔTÉ » — et non « perso · 0 PROMI · 0 TENU ». Les deux mots sont ceux du cadre,
           et ce sont déjà ceux d'un Promi gardé de côté (`motQui`, `motEtat`). */
        if(!lp.length){ et='AUCUNE PAROLE';   /* ⚑ Q213 (Tom, 13 sept.) : une Nuée vide reste une Nuée — c'est un contenant. Le mot est « AUCUNE PAROLE » sur la carte (« ENCORE AUCUNE PAROLE » déborde de ses 140 px : 180, mesuré), « ENCORE AUCUNE PAROLE » sur la fiche. La suite du bloc (pointillé, trait en points) est levée. */
          /* ⚑ ET ELLE N'A PAS D'APLAT. « Rien n'est promis, donc il n'y a pas de champ » —
             c'est déjà la règle d'un Promi gardé de côté (section 1, `e.aplat = false` ;
             page +, cadre 27). Le cadre 74 la montre appliquée à une Nuée : « l'atelier du
             samedi » y est un rectangle de corps nu `#1B1426`, pointillé mauve autour,
             trait en amorce et points — pas le champ mauve plein que l'app peignait. */
          /* ⚑ ELLE GARDE SON CHAMP MAUVE (décision Tom du 29 août). Q83 le disait déjà :
             « sa carte d'Index garde le champ de nature en pointillé, SANS MATIÈRE ». Le
             pointillé et le trait en points disent qu'elle n'est pas plantée ; la couleur,
             elle, ne se retire jamais. Le cadre 74, qui la dessine sur le corps nu, est une
             erreur de la même famille que les cadres clairs au trait invisible. */
          e.aplat=true; e.sansMatiere=true; }
      } else {
        id=b.id;
        p=promises.filter(function(q){return q.id===id;})[0];
        if(!p) return;
        e=etatPromi(p); titre=p.title||''; eb=motQui(p); et=motEtat(p,e);
        /* ⚑ UNE CARTE À TENIR PORTE SON DÉLAI — cadre 72 : « À TENIR · 2 J ».
           Les autres états n'en portent pas (« TENUE », « EN COURS », « LANCÉ »,
           « TENU À DEUX »), et c'est le cadre qui le dit, pas une règle inventée :
           un délai ne se lit que sur ce qui reste à faire. Le mot est celui du produit,
           « J » comme le moodboard l'abrège. */
        if(p.status==='rate' && p.due!=null && !isNaN(+p.due) && +p.due>0)
          et += ' · ' + (Math.round(+p.due)<=1 ? 'DEMAIN' : Math.round(+p.due) + ' JOURS');   /* ⚑ v16 : « 2 J » était du jargon */
      }
      /* ⚑ §2.5 · LA HAUTEUR DU TRAIT EST FIGÉE À LA PLANTATION — c'est une cote du PROMI,
         pas de son état. L'app la déduisait de la fiche : les six cartes du cadre 72
         sortaient à 145 · 118 · 108 · 118 · 118 · 145 là où la planche donne
         135 · 107 · 147 · 99 · 123 · 131, et tout le contenu glissait de 10 à 20 px.
         Les deux cadres de l'Index se recoupent au pixel — 2 par ligne (échelle 198/600)
         et 3 par ligne (133/600) redonnent la MÊME hauteur figée, à 1,5 px près. */
      var _ht = b.nuee ? (window.NUEHT && NUEHT[b.nuee]) : (p && p.ht);
      var g2=geo(CW,CH, _ht||e.base, !!_ht);
      var col=GX[i%GX.length], row=Math.floor(i/GX.length);
      var fond = l ? CREME : CORPS[e.nat];
      var encre = l ? ENCRE : CREME;
      var d=document.createElement('div');
      d.className='s4-carte';
      /* la carte DIT ce qu'elle est. L'ancien bloc portait ses classes (`.vif`, `.menthe`,
         `.nuee`) et les outils s'en servaient pour ouvrir une fiche ; la carte porte la
         même information en attributs — rien de neuf, le même renseignement. */
      d.setAttribute('data-nat', e.nat);
      d.setAttribute('data-etat', b.nuee ? 'nuee'
        : (p&&p.draft) ? 'garde'
        : (p&&p.status==='tenu') ? 'tenue'
        : (p&&p.status==='rate') ? 'atenir'
        : (p&&p.chiche) ? 'lance' : 'encours');
      d.style.cssText='left:'+GX[i%GX.length]+'px;top:'+(row*PAS)+'px;width:'+CW+'px;height:'+CH+'px;'
        +'border-radius:'+RAD+'px;background:'+fond+';';
      /* ⚑ LE POINTILLÉ D'UN GARDÉ DE CÔTÉ EST **DEDANS** — `outline-offset:-2px`, comme
         le cadre 74 l'écrit : « outline:2px dashed #291547; outline-offset:-2px ».
         Sans l'offset, le trait se pose À L'EXTÉRIEUR de la carte et tout le pourtour
         se décale de 2 px. Et il vaut AUSSI pour une Nuée gardée de côté — le cadre 74
         entoure « l'atelier du samedi » du même pointillé, en mauve. */
      var _gardeC = (p && p.draft) ||
        false;   /* Q213 : le pointillé d'un gardé de côté ne vaut plus pour une Nuée vide */
      if(_gardeC){ d.style.outline='2px dashed '+e.natCol; d.style.outlineOffset='-2px'; }
      var yEb=Math.round(g2.boite-DY_EB), yTi=yEb+DY_TI;
      d.innerHTML='<canvas></canvas>'+'<div class="s4-natlab" style="position:absolute;left:10px;top:10px;z-index:3;height:22px;padding:0 9px;border-radius:11px;background:#F7F0DE;color:'+window._nt(e.natCol)+';-webkit-text-fill-color:'+window._nt(e.natCol)+';font-family:var(--f-marque);font-weight:400;font-synthesis:none;font-size:13px;line-height:22px;letter-spacing:0">'+({'#FFB8D2':'Chiche','#C9A8F5':'Cercle'}[String(e.natCol).toUpperCase()]||'Promi')+'</div>'   /* ⚑ Q213 : la nature se LIT, le code couleur ne suffit pas */
        +'<div class="s4-eb" style="left:'+PADX+'px;top:'+yEb+'px;width:'+TXW+'px;font-size:'+FEB+'px;'
          +'color:'+e.colTexte+';-webkit-text-fill-color:'+e.colTexte+'">'+_esc(eb)+'</div>'
        +'<div class="s4-ti" style="left:'+PADX+'px;top:'+yTi+'px;width:'+TXW+'px;'
          +'height:'+Math.max(0,(CH-BAS_TI-yTi))+'px;font-size:'+FTI+'px;line-height:1;'
          +'color:'+encre+';-webkit-text-fill-color:'+encre+'">'+_esc(titre)+'</div>'
        +'<div class="s4-et" style="left:'+PADX+'px;bottom:'+BAS_ET+'px;width:'+TXW+'px;font-size:'+FET+'px;'
          +'color:'+e.colTexte+';-webkit-text-fill-color:'+e.colTexte+'">'+_esc(et)+'</div>';
      gr.appendChild(d);
      /* ⚠ LE TITRE NE TOUCHE JAMAIS L'ÉTAT (CASSE.md, signalé deux fois par Tom). La boîte
         du titre s'arrête à `CH − BAS_TI`, un pixel au-dessus du mot d'état : elle tient UNE
         ligne. Dès qu'un titre passe à deux — « planter un arbre », « le grand plongeoir » —
         la seconde ligne débordait et se peignait SUR « TENUE » / « TENU À DEUX ». Le cadre
         le fait aussi ; c'est un défaut de dessin, pas une règle (le §3 des cartes donne une
         boîte, et un texte ne sort pas de sa boîte).
         ON NE DÉPLACE RIEN : les cartes dont le titre tient déjà gardent leur composition au
         pixel. On rétrécit seulement CE titre-là, d'un point à la fois, jusqu'à ce qu'il
         rentre — même logique que « la plus petite des deux » de la phrase de la page +
         (§2.8). Plancher 11 px : le §6 interdit plus petit. */
      /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « DES CARTES QUI BUGUENT : QUAND LE TEXTE EST TROP
         LONG IL EST TRONQUÉ EN BAS. » La boucle était écrite, et elle ne peignait RIEN :
         elle posait `t.style.fontSize` SANS `important`, et une règle postérieure
         (`#device .s4-ti{font-size:24px!important}`) la battait. Le titre restait à 24 et
         sa seconde ligne se faisait rogner par `overflow:hidden`. C'est le piège du §8 —
         « la taille qu'on LIT n'est écrite par aucune règle » — et il se paie à l'identique
         ici. Mesuré : « planter un arbre » rendait 33 px de haut pour 48 de texte.
         ⚠ ET ON MESURE APRÈS CHAQUE PAS : `scrollHeight` ne bouge que si la taille a
         VRAIMENT changé. Sans `important`, la boucle tournait huit fois pour rien. */
      (function(t, fs){
        if(!t) return;
        /* ⚑ v102 — l'interligne est 1 : l'encre déborde de la boîte, et depuis v96 de 0,072 × taille de plus de chaque côté ; la boucle le
           compte, sinon un titre « tient » dans sa boîte et son encre touche l'état (« faire les crêpes » : 11 d'air au lieu de 39). */
        var _sup=function(){ return 2*0.072*fs*(((window._echTexte||1)-1)/0.12); };
        for(var k=0; k<10 && t.scrollHeight + _sup() > t.clientHeight + 1 && fs > 11; k++){
          fs -= 1; t.style.setProperty('font-size', fs + 'px', 'important');
        }
      })(d.querySelector('.s4-ti'), FTI);
      peintCarte(d.querySelector('canvas'), g2, e, id);
      if(b.nuee){ var kk=b.nuee;
        d.onclick=function(){ openEssaim(kk); }; }
      else { var ii=id; d.onclick=function(){ openDetail(ii); }; }
    });
  }catch(err){} };

  /* ═══ LE FIL (§5 « Fil », §3.10) ═══ */
  window._s4Fil=function(){ try{
    var fv=document.getElementById('feedView'), li=document.getElementById('feedList');
    if(!fv||!li) return;
    var items=[].slice.call(li.querySelectorAll('.fd-item'));
    if(!items.length) return;
    var l=light();
    var W=358, H=128, X=16, PAS=140, CX=143;
    var gr=document.createElement('div');
    gr.className='s4-grille'; gr.style.height=(items.length*PAS+40)+'px';
    var lus=items.map(function(it){
      var pid=it.getAttribute('data-pid'), nk=it.getAttribute('data-nuee');
      var tx=it.querySelector('.fd-tx'), tt=it.querySelector('.fd-t');
      /* ⚠ LES ACTIONS DU FIL SE RELÈVENT ET SE REPOSENT — ELLES NE SE PERDENT PAS.
         Le Fil est le SEUL endroit d'où l'on tient une parole sans ouvrir de fiche. */
      var actes=[].slice.call(it.querySelectorAll('[data-keep],[data-post],[data-releve],[data-react],[data-rejoindre],[data-tracer]'))
        .map(function(a){
          var q = a.hasAttribute('data-keep') ? 'keep'
                : a.hasAttribute('data-post') ? 'post'
                : a.hasAttribute('data-releve') ? 'releve'
                : a.hasAttribute('data-rejoindre') ? 'rejoindre'
                : a.hasAttribute('data-tracer') ? 'tracer' : 'react';
          return {quoi:q, fid:+(a.getAttribute('data-'+q)||0),
                  mot:(a.textContent||'').trim(), fort:a.classList.contains('fd-acc')||q==='keep'||q==='releve'||q==='rejoindre'||q==='tracer'};});
      return {pid:pid?+pid:null, nk:nk, actes:actes, fid:(it.getAttribute('data-fid')!=null?+it.getAttribute('data-fid'):null), nonvu:it.classList.contains('unread'), type:it.getAttribute('data-type')||'',
              texte:tx?(tx.textContent||'').trim():'', quand:tt?(tt.textContent||'').trim():''};
    });
    li.innerHTML=''; li.appendChild(gr);
    var yCur=0;
    /* ⚑ Q75 · LE REPOS EST CELUI DU CADRE 76 — cinq bandeaux nus, de 140 en 140.
       La rangée « TENIR · REPORTER » est un AJOUT VALIDÉ, HORS INVENTAIRE (CLAUDE.md §5) :
       elle ne compte dans la hauteur QUE pour le bandeau qu'un appui maintenu a déplié. */
    var nAutrui = 0;
    var OUV = window._filGeste || null;
    var cleF = function(F,i){ return F.pid!==null ? ('p'+F.pid) : (F.nk ? ('n'+F.nk) : ('i'+i)); };
    /* LA COMPOSITION DU FIL EST PUBLIÉE (CLAUDE.md §7 : on compare la composition, pas la
       peinture). Sans elle, un contrôle ne peut pas savoir QUEL bandeau porte « TENIR » :
       les `.fd-item` d'où viennent les actes sont détruits par la passe elle-même, et au
       repos aucune rangée n'est à l'écran. */
    window._filComp = lus.map(function(F,i){
      return {cle:cleF(F,i), pid:F.pid, nk:F.nk, rang:i,
              actes:F.actes.map(function(A){ return {quoi:A.quoi, mot:A.mot, fort:A.fort}; })};
    });
    window._filOuvert = OUV;
    gr.style.height=(lus.reduce(function(a,F,i){
      return a+PAS+((F.actes.length && cleF(F,i)===OUV)?62:0);},0)+40)+'px';
    lus.forEach(function(F,i){
      var p=F.pid!==null?promises.filter(function(q){return q.id===F.pid;})[0]:null;
      var e, id=null, titre, ev, et, vis=false;
      if(p){ e=etatPromi(p); id=p.id; titre=p.title||'';
        /* la ligne 2 porte LE TITRE, la ligne 1 l'événement : on retire du texte de l'app
           le titre entre guillemets, on n'écrit pas une phrase à la place. */
        /* ⚠ 21 sept. — L'APOSTROPHE CASSAIT LE RETRAIT. La classe [^«»"'] s'arrête sur la
           première apostrophe : « t'apprendre à nager » ne perdait que « t' », et la ligne
           sortait « Tu as tenu apprendre à nager » » avec un guillemet orphelin. On retire
           ce qui est ENTRE GUILLEMETS FRANÇAIS, du « au », sans rien supposer du contenu. */
        ev=F.texte.replace(/«[^»]*»/,'').replace(/[:\u00b7]\s*$/,'').replace(/\s*:\s*$/,'').replace(/\s+/g,' ').trim();
        if(!ev) ev=motQui(p);
        /* ⚑ LA PASTILLE DE VISAGE SUIT L'ÉVÉNEMENT, PAS LE PROMI. C'est la même règle que
           tout le reste du bandeau (voir `etatEvenement`) : le Fil est un journal.
           Elle se lisait sur `p.from`, c'est-à-dire sur QUI A PROMIS. Mesuré sur le cadre
           76 : les trois entrées qui nomment quelqu'un — « Marion te lance un chiche »,
           « Adrien a planté », « Marion a relevé » — portent toutes une pastille ; l'app
           n'en montrait qu'UNE, celle d'« Adrien a planté », parce que les deux autres
           portent sur des Promi dont le `from` est « moi ». */
        var _dq = null;
        try{ var _f0=(window.FEED||[]).filter(function(z){ return z.pid===F.pid; })[0];
             if(_f0) _dq=_f0.from; }catch(_){}
        if(!_dq) _dq = p.from;
        vis = !!(_dq && (''+_dq).trim() && (''+_dq).trim().toLowerCase()!=='moi');
        et=motEtat(p,e)+(F.quand?(' · '+F.quand.toUpperCase()):'');
        /* l'événement passe devant l'état courant (voir `etatEvenement`) */
        var EV=null;
        try{ EV=(window.FEED||[]).filter(function(z){ return z.pid===F.pid; })[0]; }catch(_){}
        if(EV && EV.ev){ e=etatEvenement(EV.ev, e, p);
          var mo=motEvenement(EV.ev, p); if(mo) et=mo; }
      } else if(F.nk){
        var lp=promises.filter(function(q){return q.nuee===F.nk&&!q.draft;});
        e=etatNuee(lp.length); id=lp.length?lp[lp.length-1].id:null; e.mosa=lp.map(function(q){return q.id;});
        titre=(typeof NUE!=='undefined'&&NUE[F.nk])||F.nk; ev=F.texte; vis=true;
        var _nt=lp.filter(function(q){return q.status==='tenu';}).length;
        /* ⚠ « TENU » S'ACCORDE — cadre 72 « 1 TENU », cadre 10 de `promi-nuee-toile`
           « 3 TENUS ». La carte sortait « 3 TENU ». (« PROMI » reste invariable, §2.) */
        et=lp.length+' PROMI · '+_nt+' TENU'+(_nt>1?'S':'');
      } else {
        /* ⚑ v21 — SANS PROMI RÉSOLU, ON N'AFFICHE PAS LE TEXTE BRUT DU JOURNAL : le titre est ce
           qui est entre guillemets, l'événement ce qui le précède (sinon « Rachel a planté « …
           s'écrivait en titre, guillemet orphelin compris). */
        var _mG=(F.texte||'').match(/«\s*([^»]*?)\s*»/);
        /* ⚠ LE TRAIT PORTE LA TEINTE CLAIRE DANS LES DEUX THÈMES (§2.1 bis). Je le peignais
           en couleur PLEINE en thème clair : posé sur un champ de la même couleur pleine,
           il disparaissait — Δ 1 de luminosité, mesuré. C'est exactement le défaut que les
           cadres clairs du moodboard portent, et que le document interdit. Le TEXTE, lui,
           vit sur le corps : il garde sa bascule de thème. */
        e=etatNuee(0);
        if(F.type!=='invitation'){ e.nat='promi'; e.natCol=NATCOL.promi;   /* v89 (Q347) : une invitation reçue est une Nuée (que je n'ai pas encore) */
        e.col=NATTRAIT.promi; e.colTexte=(l?window._NATTXT.promi:NATCLAIR.promi); e.base=262; e.amp=36; }
        titre=_mG?_mG[1]:F.texte; ev=_mG?(F.texte||'').slice(0,_mG.index).replace(/\s*:\s*$/,'').trim():''; et=F.quand?F.quand.toUpperCase():'';
      }
      var fond = l ? CREME : CORPS[e.nat];
      var encre = l ? ENCRE : CREME;
      var d=document.createElement('div');
      d.className='s4-carte';
      d.style.cssText='left:'+X+'px;top:'+yCur+'px;width:'+W+'px;height:'+H+'px;'
        +'border-radius:22px;background:'+fond+';';
      d.innerHTML='<canvas></canvas>'+'<div class="s4-natlab" style="position:absolute;left:10px;top:10px;z-index:3;height:22px;padding:0 9px;border-radius:11px;background:#F7F0DE;color:'+window._nt(e.natCol)+';-webkit-text-fill-color:'+window._nt(e.natCol)+';font-family:var(--f-marque);font-weight:400;font-synthesis:none;font-size:13px;line-height:22px;letter-spacing:0">'+({'#FFB8D2':'Chiche','#C9A8F5':'Cercle'}[String(e.natCol).toUpperCase()]||'Promi')+'</div>'
        +'<div class="s4-ev" style="left:145px;top:16px;width:197px;height:28px;'
          +'color:'+e.colTexte+';-webkit-text-fill-color:'+e.colTexte+'">'
          +(vis?('<span class="s4-vis" style="background:'+e.natCol+'">'+_visSvg(26)+'</span>'):'')
          +'<span class="s4-nom">'+_esc(ev)+'</span></div>'
        +'<div class="s4-ti" style="left:145px;top:50px;width:197px;height:42px;font-size:20px;'
          +'line-height:1.04;color:'+encre+';-webkit-text-fill-color:'+encre+'">'+_esc(titre)+'</div>'
        +'<div class="s4-et" style="left:145px;top:98px;width:197px;font-size:11px;'
          +'color:'+e.colTexte+';-webkit-text-fill-color:'+e.colTexte+'">'+_esc(et)+'</div>';
      gr.appendChild(d);
      /* ⚑ v89 (Q347) — la pastille « pas encore vu » : elle s'efface quand on OUVRE CETTE CARTE, jamais quand on ouvre le Fil */
      d.setAttribute('data-nonvu', F.nonvu ? '1' : '0');   /* la pastille (`_pastillesAttente`) le lit */
      /* ⚑ 23 SEPTEMBRE 2026, second tour (Tom) — « RENDS-LUI SA TAILLE D'ORIGINE, REMONTE-LE,
         ET AU-DELÀ DE DEUX LIGNES COUPE AVEC DES POINTS DE SUITE. JAMAIS DE RÉDUCTION DE TAILLE. »
         Au tour précédent je rétrécissais le titre (18 et 22 px au lieu de 24) : c'était l'inverse
         de la demande. **La taille ne bouge plus du tout.**
         LES ESPACES DE LA CARTE NE BOUGENT PAS : l'événement fait 28 de haut, **6** jusqu'au titre,
         le titre finit à **92**, **6** jusqu'à l'état (98). Ce qui bouge, c'est LE HAUT — le titre
         grandit vers le haut depuis 92, et l'événement monte avec lui, jusqu'à **8 px du bord**
         (le plancher de la carte). La boîte passe donc de **42 à 50** : à 24 px, deux lignes font
         49,92 — elles y tiennent pile.
         AU-DELÀ, ON COUPE : `-webkit-line-clamp:2` pose les points de suite à la fin de la
         deuxième ligne. Rien ne déborde, rien ne rétrécit.
         ⚠ UNE CARTE À UNE LIGNE NE BOUGE PAS D'UN PIXEL : `h` part de 42, `top` retombe à 50,
         l'événement à 16 — les cotes d'origine, par construction. */
      (function(carte){
        var t=carte.querySelector('.s4-ti'), ve=carte.querySelector('.s4-ev');
        if(!t) return;
        var BAS=92, GAP=6, HEV=28, HAUT_MIN=8, H0=42, LH=1.04, MAXL=2;
        var fs=parseFloat(getComputedStyle(t).fontSize)||24;
        /* 1 · combien de lignes le titre demande-t-il ? on mesure SANS borne */
        t.style.setProperty('display','block','important');
        t.style.setProperty('height','auto','important');
        t.style.removeProperty('-webkit-line-clamp');
        var voulu=Math.ceil(t.scrollHeight)||0, ligne=fs*LH;
        var n=Math.max(1, Math.round(voulu/ligne));
        /* 2 · la boîte grandit VERS LE HAUT, deux lignes au plus */
        var h=Math.max(H0, Math.ceil(Math.min(n,MAXL)*ligne));
        h=Math.min(h, BAS-HAUT_MIN-GAP-HEV);
        t.style.setProperty('height',h+'px','important');
        t.style.setProperty('top',(BAS-h)+'px','important');
        if(ve) ve.style.setProperty('top',Math.max(HAUT_MIN,(BAS-h)-GAP-HEV)+'px','important');
        /* 3 · au-delà de deux lignes : points de suite, JAMAIS de réduction */
        t.style.setProperty('display','-webkit-box','important');
        t.style.setProperty('-webkit-box-orient','vertical');
        t.style.setProperty('-webkit-line-clamp',''+MAXL);
        t.style.setProperty('overflow','hidden','important');
        try{ carte.setAttribute('data-titre-cote',[voulu,h,BAS-h,Math.round(fs),Math.min(n,MAXL)].join(',')); }catch(_){}
      })(d);
      /* ⚑ LE NOMBRE DE L'ENTÊTE DU FIL COMPTE LES GESTES QUI VIENNENT D'AILLEURS.
         Le cadre 76 écrit **4** au-dessus de **CINQ** bandeaux ; ni le document ni le
         moodboard ne disent ce qu'il compte. Le plus sobre qui rende 4 : les quatre
         entrées qui portent quelqu'un d'autre — Marion, Adrien, Rachel, Marion — contre
         la cinquième, « à moi · planter un arbre ». C'est ce que l'app dit d'elle-même
         quand le Fil est vide : *« les gestes de tes proches apparaîtront ici. »*
         L'app écrivait `FEED.length`, soit 5. À VALIDER (QUESTIONS · Q79). */
      if(ev && ev.trim().toLowerCase() !== 'à moi') nAutrui++;
      peintBandeau(d.querySelector('canvas'), e, id);
      if(p){ var ii=p.id; d.onclick=function(){ setView('toile'); openDetail(ii); }; }
      else if(F.nk){ var kk=F.nk; d.onclick=function(){ setView('toile'); openEssaim(kk); }; }
      if(F.fid!=null){ (function(dd,fid){ var o=dd.onclick; dd.onclick=function(evt){ try{ if(window._filVu) window._filVu(fid); dd.setAttribute('data-nonvu','0'); var nv=dd.querySelector(':scope > .s4-att'); if(nv) nv.remove(); }catch(_){} if(o) return o.call(this,evt); }; })(d,F.fid); }
      yCur += PAS;
      /* LE GESTE, sous le bandeau. Pastille d'action du §3.5. Le bandeau reste celui du
         moodboard — 358 × 128, trois boîtes fixes — on n'y touche pas. */
      /* l'appui maintenu déplie la rangée de CE bandeau ; un toucher bref ouvre sa fiche.
         On garde le `onclick` posé plus haut : on l'annule seulement si l'appui a duré. */
      if(F.actes.length){
        (function(cle,carte){
          var tmr=null, longue=false;
          var arme=function(ev){ longue=false; if(ev && ev.button) return;
            tmr=setTimeout(function(){ longue=true; tmr=null;
              window._filGeste = (window._filGeste===cle) ? null : cle;
              /* ⚠ ON REBÂTIT PAR `buildFeed`, JAMAIS PAR `_s4Fil` SEUL. `_s4Fil` lit les
                 `.fd-item` de l'app puis fait `li.innerHTML=''` : il DÉTRUIT sa propre
                 source. Rappelé seul, il sort par son garde « aucun .fd-item » et rien ne
                 se déplie. Mesuré : `_filGeste` posé, zéro rangée à l'écran. */
              try{ if(window.buildFeed) window.buildFeed(); else window._s4Fil(); }catch(_){}
            }, 480); };
          var desarme=function(){ if(tmr){ clearTimeout(tmr); tmr=null; } };
          carte.addEventListener('pointerdown', arme);
          carte.addEventListener('pointerup', desarme);
          carte.addEventListener('pointerleave', desarme);
          carte.addEventListener('pointercancel', desarme);
          carte.addEventListener('pointermove', function(e){
            if(tmr && (Math.abs(e.movementX)>3||Math.abs(e.movementY)>3)) desarme(); });
          carte.addEventListener('click', function(e){
            if(longue){ longue=false; e.stopPropagation(); e.preventDefault(); } }, true);
        })(cleF(F,i), d);
      }
      if(F.actes.length && cleF(F,i)===OUV){
        var barre=document.createElement('div');
        barre.className='s4-actes';
        barre.style.cssText='position:absolute;left:'+(X+16)+'px;top:'+(yCur-12)+'px;'
          +'height:50px;display:flex;align-items:center;gap:12px;z-index:3';
        F.actes.forEach(function(A){
          var t=document.createElement('button');
          t.className='s4-acte'+(A.fort?' fort':'');
          t.textContent=A.mot;
          t.style.cssText='height:50px;border-radius:25px;padding:0 19px;box-sizing:border-box;'
            +'font-family:var(--f-libelle);font-weight:700;font-size:16px;'
            +'line-height:1;cursor:pointer;background:transparent;'
            +(A.fort ? ('border:3px solid '+e.col+';color:'+e.col+';-webkit-text-fill-color:'+e.col)
                     : ('border:0;color:'+e.colTexte+';-webkit-text-fill-color:'+e.colTexte));
          t.onclick=function(ev){ ev.stopPropagation();
            window._filGeste = null;   /* l'ajout se referme dès qu'il a servi */
            try{
              if(A.quoi==='keep') feedKeep(A.fid);
              else if(A.quoi==='post') feedPostpone(A.fid);
              else if(A.quoi==='releve') feedReleve(A.fid);
              else if(A.quoi==='rejoindre'){ if(window.filRejoindre) filRejoindre(A.fid); }
              else if(A.quoi==='tracer'){ if(window.filTracer) filTracer(A.fid); }
              else if(A.quoi==='react'){ feedReacted[A.fid]=!feedReacted[A.fid]; buildFeed(); }
              if(window.syncAll) syncAll();
            }catch(_){}
          };
          barre.appendChild(t);
        });
        gr.appendChild(barre);
        yCur += 62;
      }
    });
    /* ⚑ v89 (Tom, Q347) — LE compteur de l'app : ce qui attend un geste de moi (il remplace « les gestes d'autrui », Q79) */
    if(window._filAttente) nAutrui = window._filAttente();
    window._filAutrui = nAutrui;
    try{ var _fc=document.getElementById('fdCount');
      if(_fc && _fc.textContent !== ''+nAutrui) _fc.textContent = ''+nAutrui; }catch(_){}
  }catch(err){} };

  /* ── §3.10 · LE TRAIT DU BANDEAU EST VERTICAL. Même onde, tournée d'un quart de tour :
       x(t) = base − mont·t − a·sin(2π·t), base = 0,34 × largeur, per = 1, amp = 13,5.
       Relevé dans le cadre 76 : plein 0 → 64 puis des points r 3,4 tous les 13 quand une
       moitié manque ; plein 0 → 128 quand la parole est entière. ── */
  function peintBandeau(cv,e,id){
    var W=143, H=128, dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
    cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
    cv.style.width=W+'px'; cv.style.height=H+'px';
    var g=cv.getContext('2d'); if(!g) return;
    g.setTransform(dpr,0,0,dpr,0,0); g.clearRect(0,0,W,H);
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';
    /* ⚠ LES TROIS COEFFICIENTS SONT RELEVÉS SUR LE CADRE 76, PAS DÉDUITS. Le chemin de la
       planche est `M121.0 0 L118.7 5.3 … L116.8 128.0` — 24 segments de 5,333. En résolvant
       sur ses extrêmes (x = 111,5 à u = 0,25 ; x = 126,2 à u = 0,75) : **base 121,0 ·
       montée 4,3 · amplitude de sinus 8,425 · période 1**. L'app portait `0.34 × 358 =
       121,72` et `amp 13,5` (d'où 4,59 et 8,37) — proche, mais pas la planche. Et ces
       trois-là ne suivent PAS `mont = 0,34·amp / a = 0,62·amp` : 4,3 donnerait amp 12,65,
       8,425 donnerait 13,59. Le bandeau du Fil a ses propres coefficients ; on les copie. */
    var bx=121.0, mont=4.3, a=8.425;
    var x=function(t){ var u=Math.max(0,Math.min(1,t/H));
      return bx - mont*u - a*Math.sin(2*Math.PI*u); };
    function trace(y0,y1){ g.beginPath(); g.moveTo(x(y0),y0);
      for(var yy=y0;yy<=y1;yy+=2) g.lineTo(x(yy),yy); g.lineTo(x(y1),y1); }
    /* même règle qu'une carte d'Index : la dalle d'abord, le champ cède ensuite (Q93). */
    var _srcF=null;
    if(id!==null && id!==undefined && window.Toile && Toile.dalleTrame){
      /* ⚑ v29 — rendue par le moteur À LA TAILLE de sa boîte (110 × 80), recalée par lui sur la rampe Q297 */
      var _oF={monde:undefined,   /* ⚑ v34 : le monde et la palette du Studio (Tom) */
               rampe:(window._ingenuRampe?window._ingenuRampe(id):null)||undefined};
      try{ _srcF=window._rendDalle(id, 110*dpr, 80*dpr, _oF); }catch(_){ _srcF=null; }
    }
    if(e.aplat!==false){ trace(0,H); g.lineTo(0,H); g.lineTo(0,0); g.closePath();
      g.fillStyle=(_srcF?champCede(e.natCol,_srcF,cv):e.natCol); g.fill(); }
      /* ⚑ LE CHAMP SE DÉCLARE — « un champ blanc n'existe jamais » (décision Tom, 29 août).
         Un contrôle au pixel ne peut pas trancher partout : sur une Nuée VIDE, les graines
         du §10.6 sont crème DANS LES DEUX THÈMES, et elles tombent pile sur la couleur du
         corps. Ce sont pourtant de la MATIÈRE posée sur un champ mauve, pas un champ nu.
         Le peintre, lui, sait ce qu'il a versé : il l'écrit. C'est la doctrine du §7 —
         on compare la COMPOSITION, pas la peinture. */
      try{ cv.setAttribute('data-champ', (_srcF?champCede(e.natCol,_srcF,cv):e.natCol)); }catch(_){}
    /* Q53 · la photo remplace aussi la matière du bandeau, à la cote de sa dalle. */
    /* ⚑ Q74 · LA ZONE DE MATIÈRE EST PUBLIÉE. Un comparateur doit pouvoir l'exclure :
       la matière est engendrée et respire avec `performance.now()`, elle ne se compare
       jamais au pixel (CLAUDE.md § 8 bis). On déclare la boîte, on ne masque rien de plus. */
    try{ cv.setAttribute('data-matiere','5,40,110,80');   /* Q213 : la dalle descend sous le libellé */
         cv.setAttribute('data-matiere-base','143,128'); }catch(_){}
    var _nlF=(cv.parentNode&&cv.parentNode.querySelector('.s4-natlab'));
    if(e.mosa && e.mosa.length>1 && window._petiteToile){ var _xm=1e9; for(var _yy=0;_yy<=H;_yy+=4){ _xm=Math.min(_xm,x(_yy)); }
      window._petiteToile(g,{x:6,y:6,w:_xm-12,h:H-12},{x:0,y:0,w:(_nlF?10+(function(el){ var W={'Promi':73,'Chiche':81,'Nuée':57,'Cercle':76};   /* ⚑ 20 sept. : PromiLate 13 px, relevées police chargée (Gilbert 12 donnait 54·60·51) */ return el ? (W[(el.textContent||'').trim()] || Math.ceil(el.offsetWidth)) : 0; })(_nlF)+4:0),h:36},e.mosa); }
    else if(window._photoDansBoite && window._photoDansBoite(g, {x:5,y:19,w:110,h:89}, id)) { /* posée */ }
    else if(_srcF){
      try{ window._poseUn(g, _srcF, 5+110/2, 40+80/2);   /* ⚑ v29 — 1:1 */
      }catch(_){}
    }
    g.strokeStyle=e.col; g.fillStyle=e.col; g.lineWidth=7; g.lineCap='round'; g.lineJoin='round';
    if(e.mode==='complet'||e.mode==='duo'){ trace(0,H); g.stroke(); }
    else { trace(0,H/2); g.stroke();
      for(var yy=77;yy<H;yy+=13){ g.beginPath(); g.arc(x(yy),yy,3.4,0,6.2832); g.fill(); } }
    /* la passe est finie : on le dit. Une sonde attend CE marqueur, pas un délai. */
    try{ cv.setAttribute('data-peint','1'); }catch(_){}
  }

  function _visSvg(d){
    var x0=(d/2-0.30*d).toFixed(2), x1=(d/2+0.30*d).toFixed(2), ye=(0.98*d).toFixed(2);
    return '<svg viewBox="0 0 '+d+' '+d+'" xmlns="http://www.w3.org/2000/svg">'
      +'<circle cx="'+(d/2)+'" cy="'+(0.78*d/2).toFixed(2)+'" r="'+(0.19*d).toFixed(2)+'" fill="#F7F0DE"/>'
      +'<path d="M'+x0+' '+ye+' A'+(0.30*d).toFixed(2)+' '+(0.27*d).toFixed(2)+' 0 0 1 '+x1+' '+ye
      +' Z" fill="#F7F0DE"/></svg>';
  }

  /* ── LA MISE EN SCÈNE : l'écran plein s'arme quand la feuille s'ouvre, et se désarme
       quand elle se ferme. On COMPARE L'ÉTAT AVANT D'AGIR (CLAUDE.md §8, le
       MutationObserver qui s'auto-déclenche). ── */
  function armer(){
    var dev=document.getElementById('device');
    var sh=document.getElementById('indexSheet'), fv=document.getElementById('feedView');
    if(!dev) return;
    var ixOn = !!(sh && sh.classList.contains('show'));
    var flOn = !!(fv && fv.classList.contains('in') && getComputedStyle(fv).display!=='none');
    var veut = ixOn || flOn;
    if(dev.classList.contains('s4-plein')!==veut) dev.classList.toggle('s4-plein',veut);
    if(sh && sh.classList.contains('s4')!==ixOn) sh.classList.toggle('s4',ixOn);
    if(fv && fv.classList.contains('s4')!==flOn) fv.classList.toggle('s4',flOn);
  }
  window._s4Armer=armer;

  /* les libellés du moodboard : « Rechercher », rien de plus. */
  function libelles(){
    var a=document.getElementById('ixSearch'), b=document.getElementById('fdSearch');
    if(a&&a.placeholder!=='Rechercher') a.placeholder='Rechercher';
    if(b&&b.placeholder!=='Rechercher') b.placeholder='Rechercher';
    var c=document.getElementById('fdCount');
    if(c){ var n=0;
      /* le compte est celui que `_s4Fil` vient de composer (les gestes d'autrui) ;
         `FEED.length` n'est qu'un secours tant que la grille n'est pas bâtie. */
      try{ n = (window._filAutrui!=null) ? window._filAutrui : (FEED||[]).length; }catch(_){}
      if(c.textContent!==''+n) c.textContent=n;
      c.style.setProperty('display','inline-block','important'); }
  }

  var _biOrig=window.buildIndex;
  if(typeof _biOrig==='function'){
    window.buildIndex=function(){ var r=_biOrig.apply(this,arguments);
      window._s4Frais = true;
      try{ libelles(); armer(); window._s4Index(); }catch(_){}
      return r; };
    try{ buildIndex=window.buildIndex; }catch(_){}
  }
  var _bfOrig=window.buildFeed;
  if(typeof _bfOrig==='function'){
    window.buildFeed=function(){ var r=_bfOrig.apply(this,arguments);
      try{ libelles(); armer(); window._s4Fil(); }catch(_){}
      return r; };
    try{ buildFeed=window.buildFeed; }catch(_){}
  }
  var _svOrig=window.setView;
  if(typeof _svOrig==='function'){
    window.setView=function(v){ var r=_svOrig.apply(this,arguments);
      try{ armer(); setTimeout(armer,60); setTimeout(armer,420); }catch(_){}
      return r; };
    try{ setView=window.setView; }catch(_){}
  }
  var _oiOrig=window.ouvrirIndex;
  if(typeof _oiOrig==='function'){
    window.ouvrirIndex=function(){ var r=_oiOrig.apply(this,arguments);
      try{ armer(); setTimeout(armer,60); setTimeout(function(){ armer(); window._s4Index(); },380); }catch(_){}
      return r; };
  }
  var _caOrig=window.closeAll;
  if(typeof _caOrig==='function'){
    window.closeAll=function(){ var r=_caOrig.apply(this,arguments);
      try{ setTimeout(armer,60); setTimeout(armer,420); }catch(_){}
      return r; };
    try{ closeAll=window.closeAll; }catch(_){}
  }
  document.addEventListener('click',function(){ setTimeout(armer,80); setTimeout(armer,440); },true);
  /* ⚑ v21 — `s4` (toute la mise en page des deux écrans jumeaux) arrivait par minuteur, une image après l'ouverture :
     la recherche du Fil paraissait 40 ms dans son ANCIENNE forme (Atkinson 34 px). On arme à l'instant de l'ouverture. */
  try{ ['indexSheet','feedView'].forEach(function(id){ var el=document.getElementById(id); if(el)
    new MutationObserver(function(){ armer(); }).observe(el,{attributes:true,attributeFilter:['class','style']}); }); }catch(_){}
})();
