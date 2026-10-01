
/* ═══ LE TRAIT (§7, §9.2/9.3) — la frontière entre le champ de nature et le corps.
   Un composant : sinus 1,5 période + montée 0,34×A vers la droite · ma moitié pleine
   0→195px puis guide en cercles Ø9 tous les 18px · chevron à la jonction · amorce
   effilée 0→42 · couleur = ÉTAT (à tenir orange, tenu menthe) sinon teinte claire de
   nature · hauteur = 344 − 32×(éléments remplis), plancher 196. Sur une fiche TENUE,
   c'est le vrai cur.trace (la signature), pas la vague générique. Wrappé try/catch :
   s'il échoue, la fiche n'est pas cassée. */
(function(){
  var NS='http://www.w3.org/2000/svg';
  function el(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);return e;}
  function comp(p){ var c=1; /* le titre compte toujours */
    if(p.who&&p.who!=='moi'&&p.who!=='le groupe')c++;
    if(p.from&&p.from!=='moi')c++;
    if(p.due!=null||p.dueISO)c++;
    if(p.note&&(''+p.note).trim())c++;
    if(p.avec)c++;
    if(p.nuee&&p.nuee!=='soi')c++;
    return c; }
  /* ═══ LE BANDEAU (Promi/Chiche) peint SUR LE CANVAS dpTrameCv — SYNCHRONE (pas de <image>
     dataURL async qui « flashait » sans dalle). Aplat plein-cadre NATURE + VRAIE dalle centrée
     NON TEINTÉE (Toile.dalleTrame, échelle 1 — CLAUDE.md §4) + vague/guide couleur d'état. On
     garde le canvas à sa place (le mot-marque reste au-dessus, comme toujours) et on annule le
     délavage (masque + screen + opacité) posé par les vieilles règles. ═══ */
  window._ficheTrait=function(){ try{
    var dp=document.getElementById('detailPoster'); if(!dp||!dp.classList.contains('show')) return;
    var chiche=dp.classList.contains('dp-chiche'), nuee=dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee');
    /* La NUÉE a une structure séparée (#dpNuee) et garde SA bande (cluster mauve, _ficheDalle). */
    if(nuee) return;
    var p=(typeof cur!=='undefined')?cur:null;
    if(!p||p.draft) return;                               /* un gardé de côté rouvre la page +, pas une fiche */
    var cv=document.getElementById('dpTrameCv'); if(!cv) return;
    /* un ancien calque SVG (versions précédentes) traîne ? on le retire. */
    var oldsvg=document.getElementById('dpTrait'); if(oldsvg&&oldsvg.parentNode) oldsvg.parentNode.removeChild(oldsvg);
    var natCol  = chiche?'#FFB8D2':'#82AEF8';             /* APLAT plein = la NATURE (spec §1.1) */
    /* ⚑ §2.1 bis, 18 sept. 2026 — MÊME CORRECTION QU'AILLEURS, sur un peintre plus ancien que
       la passe du jour avait manqué : ce `natLight` peint LE TRAIT de l'onde (voir `etat`
       ci-dessous). Les teintes claires sont mortes sur un champ pastel — Δlum 1,6 et 5,0 ;
       on prend les compagnons sombres, ceux de NATTRAIT. */
    var natLight= chiche?'#3D0F23':'#022140';             /* teinte du TRAIT (spec §2.1bis) = 2e teinte dalle */
    /* L'ÉTAT VIT DANS LA LIGNE : chiche lancé → teinte dalle (jamais terracotta) ; à tenir →
       orange ; tenu → menthe ; en cours → teinte claire nature. */
    var chicheLance = chiche && !p.avec, etat;
    if(chicheLance)           etat = natLight;
    else if(p.status==='rate')etat = '#DD4D23';
    else if(p.status==='tenu')etat = '#8FE08F';
    else                      etat = natLight;
    var W=390;
    var waveY = Math.max(196, Math.min(344, 344 - 32*comp(p)));
    var dy = waveY - 250.6;   /* décale la courbe EXACTE de #44 à la hauteur de composition */
    var H = Math.round(waveY + 60);
    var posterW = dp.clientWidth || 390, sc = posterW/W;
    var dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    cv.width = Math.round(posterW*dpr); cv.height = Math.round(H*sc*dpr);
    cv.style.width = posterW+'px';
    /* annuler le délavage (les vieilles règles !important) — inline !important gagne */
    cv.style.setProperty('height',(H*sc)+'px','important');
    cv.style.setProperty('opacity','1','important'); cv.style.setProperty('filter','none','important');
    cv.style.setProperty('mix-blend-mode','normal','important');
    cv.style.setProperty('-webkit-mask','none','important'); cv.style.setProperty('mask','none','important');
    cv.style.setProperty('position','absolute','important'); cv.style.setProperty('top','0','important'); cv.style.setProperty('left','0','important');
    /* le canvas porte un background d'état (menthe/orange) posé par de vieilles règles : il
       transparaît sous la vague. On le rend transparent → le corps (nature, §1.3) apparaît. */
    cv.style.setProperty('background','transparent','important');
    var g=cv.getContext('2d'); if(!g) return;
    g.setTransform(dpr*sc,0,0,dpr*sc,0,0);
    g.clearRect(0,0,W,H);
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';
    function yy(v){ return v+dy; }
    /* ── 1 · L'APLAT plein-cadre NATURE : bord bas = la vague (comme le fill du #44) ── */
    g.beginPath(); g.moveTo(0,0); g.lineTo(0,yy(262));
    g.bezierCurveTo(21.67,yy(254.44),43.33,yy(233.06),65,yy(232.23));
    g.bezierCurveTo(86.67,yy(231.40),108.33,yy(243.56),130,yy(257.01));
    g.bezierCurveTo(151.67,yy(270.47),173.33,yy(282.63),195,yy(281.80));
    g.bezierCurveTo(216.67,yy(280.97),238.33,yy(267.14),260,yy(252.03));
    g.bezierCurveTo(281.67,yy(236.91),303.33,yy(223.08),325,yy(222.25));
    g.bezierCurveTo(346.67,yy(221.42),368.33,yy(240.31),390,yy(247.04));
    g.lineTo(390,0); g.closePath(); g.fillStyle=natCol; g.fill();
    /* ── 2 · LA DALLE centrée, VRAIE et NON TEINTÉE (cotes #44 : 141×118 @124,88), opacité 1,
       jamais au-dessus de y=88, jamais à moins de 12px de la vague. Du moteur, synchrone. ── */
    if(window.Toile&&Toile.dalleAbs&&Toile.dalleAbs(p.id)){
      var bx=124,by=88,bw=141,bh=118, maxB=waveY-12; if(by+bh>maxB) bh=Math.max(56,maxB-by);
      /* LA DALLE PORTE LE MONDE, JAMAIS SA NATURE (CLAUDE.md §4, moodboard §8 « c'est exactement
         la dalle que la promesse posera sur la Toile, même forme, même palette »). La teinture
         par nature (#C4A2F5 / #F5AC9E) posée au lot précédent était une FAUTE : la §1.2 de la
         spec décrit le monde par DÉFAUT du moodboard, pas une teinture à appliquer. On dessine
         la VRAIE dalle du moteur, telle quelle : opacité 1, aucun voile, aucun mélange (§2.7).
         ⚑ v29 — rendue à la taille de sa boîte, posée 1:1 (redteam_decoupe). */
      window._poseDalle(g, p.id, bx, by, bw, bh);
    }
    /* ── 3 · LA FRONTIÈRE : tenue = signature (cur.trace) ; tenu sans trace = rien de plus ;
       sinon vague (moitié pleine) + chevron + guide, couleur d'état. ── */
    var tenue = (p.status==='tenu') && p.trace && p.trace.length>1;
    if(tenue){
      var xs=p.trace.map(function(q){return q.x;}), ys=p.trace.map(function(q){return q.y;});
      var x0=Math.min.apply(null,xs),x1=Math.max.apply(null,xs),y0=Math.min.apply(null,ys),y1=Math.max.apply(null,ys);
      var swt=Math.max(1,x1-x0), sht=Math.max(1,y1-y0), k=Math.min(342/swt, 60/sht);
      var ox=24+(342-swt*k)/2, oy=waveY-30;
      g.strokeStyle=etat; g.lineWidth=6; g.lineCap='round'; g.lineJoin='round';
      g.beginPath(); g.moveTo((p.trace[0].x-x0)*k+ox,(p.trace[0].y-y0)*k+oy);
      for(var i=1;i<p.trace.length;i++){ g.lineTo((p.trace[i].x-x0)*k+ox,(p.trace[i].y-y0)*k+oy); }
      g.stroke();
    } else if(p.status!=='tenu'){
      g.strokeStyle=etat; g.lineWidth=10; g.lineCap='round'; g.lineJoin='round';
      g.beginPath(); g.moveTo(0,yy(262));
      g.bezierCurveTo(21.67,yy(254.44),43.33,yy(233.06),65,yy(232.23));
      g.bezierCurveTo(86.67,yy(231.40),108.33,yy(243.56),130,yy(257.01));
      g.bezierCurveTo(151.67,yy(270.47),173.33,yy(282.63),195,yy(281.80));
      g.stroke();
      g.save(); g.translate(195,yy(281.80)); g.rotate(Math.atan2(-0.83,21.67));
      g.beginPath(); g.moveTo(-7,-10); g.lineTo(6,0); g.lineTo(-7,10); g.lineWidth=6; g.stroke(); g.restore();
      var CIRC=[[213,278.6],[231,270.7],[249,259.6],[267,247.2],[285,235.6],[303,226.9],[321,222.5],[339,223.3],[357,228.8],[375,237.9]];
      g.fillStyle=etat; CIRC.forEach(function(pt){ g.beginPath(); g.arc(pt[0],yy(pt[1]),4.5,0,7); g.fill(); });
    }
  }catch(e){} };
  /* dpTrameCv n'est plus le bandeau POUR PROMI/CHICHE (dalle dans #dpTrait). On garde le
     peintre d'origine POUR LA NUÉE seulement (sa bande cluster mauve vit toujours dans
     dpTrameCv, structure séparée #dpNuee). */
  try{ var _origFD=window._ficheDalle;
    window._ficheDalle=function(){ var dp=document.getElementById('detailPoster');
      if(dp&&(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'))){ return _origFD&&_origFD.apply(this,arguments); }
      /* Promi/Chiche : rien à peindre ici, la dalle est dans #dpTrait */ };
  }catch(_){}
  /* ORDRE — posé au Temps 2 (voir _ficheOrdre plus bas). */
  window._ficheOrdre=window._ficheOrdre||function(){};
  /* branche sur le rendu de fiche, après le reste */
  var orig=window._fichePose;
  window._fichePose=function(){ if(orig) orig.apply(this,arguments); try{ requestAnimationFrame(function(){ requestAnimationFrame(function(){ window._ficheTrait(); window._ficheOrdre(); }); }); }catch(e){} };
  var origD=window.dpRefresh;
  if(origD){ window.dpRefresh=function(){ origD.apply(this,arguments); try{ window._ficheTrait(); window._ficheOrdre(); }catch(e){} }; }
})();
