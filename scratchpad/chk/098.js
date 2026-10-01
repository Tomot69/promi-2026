
/* ══ LE GESTE DE COULEUR AU DOIGT, SUR LA TOILE DU STUDIO ═══════════════════════════════
   Tom, 20 septembre 2026 : « on avait un geste au toucher sur la Toile prévisualisée — on
   restait appuyé vers le haut, le bas, la gauche, la droite pour faire varier la palette.
   C'est perdu. Retrouve-le, en plus de la jauge. »

   ⚠ CE N'ÉTAIT PAS PERDU : CE N'AVAIT JAMAIS ÉTÉ ÉCRIT. Q135 le disait noir sur blanc —
   « le geste de couleur au doigt — presser une dalle ou un ton et traîner, avec la
   sensibilité des réglages de Photos (Q125) — n'est pas implémenté. La planche le dessine ;
   le code ne l'a pas. » C'est donc ce lot-là, et il suit Q125 à la lettre.

   Q125 · LA SENSIBILITÉ : « la couleur suit le doigt au DÉPLACEMENT, sans accélération, sur
   toute la course. Un petit mouvement fait un petit changement ; un grand mouvement continue
   de suivre au lieu de buter ; on revient exactement d'où l'on vient en refaisant le chemin
   à l'envers. » Donc : la valeur se calcule depuis l'ORIGINE du geste, jamais en cumulant —
   un cumul ne revient jamais exactement d'où il vient.

   LES DEUX AXES, ET RIEN N'EST INVENTÉ : ce sont les deux réglages que le Studio porte déjà.
     · horizontal → LA TEINTE   `Toile.setHue`     — ce que fait la jauge, qui reste
     · vertical   → LA PALETTE  `Toile.setPalette` — ce que fait le rail des vingt
   Course : 390 px (la largeur de l'appareil) pour un tour de teinte complet ; 48 px par
   palette. Les deux sont des constantes, jamais une mesure (§8).

   ⚠ IL NE PREND PAS LA PLACE DU GLISSEMENT DE MONDE. Celui-ci part dès 34 px d'horizontale ;
   le geste de couleur demande un APPUI MAINTENU de 480 ms — la même valeur que l'appui long
   d'origine de l'app (≈ l. 6687), pas un nombre neuf. Quand il s'arme, on envoie un
   `pointercancel` au panneau : le glissement de monde écoute cet événement et se désarme
   proprement. On ne touche pas à son code (§9, on ne réécrit pas, on patche).
   ══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  var MAINTIEN = 480;     /* ms — l'appui long de l'app */
  var COURSE   = 390;     /* px pour 360° de teinte : la largeur de l'appareil */
  var PAS_PAL  = 48;      /* px par palette */
  var MOT = 'reste appuyé pour changer de couleur';   /* QUESTIONS · à valider */

  function T(){ try{ return window.Toile; }catch(e){ return null; } }
  function $(s){ return document.querySelector(s); }

  var sur=false, arme=false, t0=0, x0=0, y0=0, hue0=0, pal0=0, cles=[], pid=null, minu=null;

  function invite(on){
    try{
      var sc=document.getElementById('studioScreen'); if(!sc) return;
      var el=document.getElementById('stpInvC');
      if(!el){ el=document.createElement('div'); el.id='stpInvC'; el.textContent=MOT; sc.appendChild(el); }
      /* sous le nom du monde, au même endroit que l'autre invite */
      var inv=document.getElementById('stpInv')||sc.querySelector('.st3-hint');
      if(inv){ var r=inv.getBoundingClientRect(), rs=sc.getBoundingClientRect();
               el.style.top=(r.top-rs.top+22)+'px'; }
      else el.style.top='60%';
      el.classList.toggle('on', !!on);
    }catch(e){}
  }

  function surLaToile(t){
    try{
      if(!t || !t.closest) return false;
      if(t.closest('.st3-bottom,.st3-dots,.st3-p,.st3-spec,.closeb,.studio-toggles,#stpHaut,#stpBas,#stpPals,#stpVue,#stpDots,#stLockBuy,#stLockCta')) return false;
      var sc=document.getElementById('studioScreen');
      return !!(sc && sc.contains(t));
    }catch(e){ return false; }
  }

  function armer(){
    var t=T(); if(!t||!sur) return;
    arme=true;
    try{ hue0 = (typeof t.getHue==='function') ? (+t.getHue()||0) : (window._stHue||0); }catch(e){ hue0=0; }
    try{ cles = Object.keys(t.palettes()); pal0 = Math.max(0, cles.indexOf(t.getPalette())); }catch(e){ cles=[]; pal0=0; }
    invite(true);
    /* le glissement de monde se désarme sur pointercancel — on le lui envoie, sans toucher à son code */
    try{
      var sc=document.getElementById('studioScreen');
      if(sc) sc.dispatchEvent(new PointerEvent('pointercancel',{bubbles:true,pointerId:pid||1}));
    }catch(e){}
  }

  function suivre(e){
    if(!arme) return;
    var t=T(); if(!t) return;
    var dx=e.clientX-x0, dy=e.clientY-y0;
    /* la teinte suit le doigt, sans accélération, et revient exactement (Q125) */
    var h=((hue0 + dx*(360/COURSE)) % 360 + 360) % 360;
    try{ t.setHue(h); }catch(_){}
    if(cles.length){
      var k=Math.round(dy/PAS_PAL);
      /* ⚑ v35 (Tom) — « chaque monde doit paraître dans la palette choisie » : bornée, la liste de 24 palettes à 48 px le pas
         (1 152 px) ne se parcourait pas d'un glissement — depuis Ingénu on n'atteignait ni Atrabilaire ni Taciturne. Elle est
         CIRCULAIRE : toute palette est à 12 pas au plus, dans un sens ou dans l'autre ; on revient toujours d'où l'on vient (Q125). */
      var n=cles.length, i=((pal0 + k) % n + n) % n;
      try{ if(t.getPalette()!==cles[i]) t.setPalette(cles[i]); }catch(_){}
    }
    /* on repeint la Toile du Studio, comme le fait la jauge */
    try{ var bg=document.getElementById('stBg'); if(bg) t.repaint(bg); }catch(_){}
    /* le nom de la palette suit, s'il est là */
    try{ var pn=document.getElementById('st3pn'); var ps=T().palettes();
         var cur=T().getPalette(); if(pn&&ps[cur]) pn.textContent=ps[cur].name; }catch(_){}
    try{ e.preventDefault(); }catch(_){}
  }

  function fin(){
    if(minu){ clearTimeout(minu); minu=null; }
    if(arme) invite(false);
    sur=false; arme=false; pid=null;
  }

  document.addEventListener('pointerdown', function(e){
    var sc=document.getElementById('studioScreen');
    if(!sc || !sc.classList.contains('show')) return;
    if(!surLaToile(e.target)) return;
    sur=true; arme=false; pid=e.pointerId; x0=e.clientX; y0=e.clientY; t0=Date.now();
    if(minu) clearTimeout(minu);
    minu=setTimeout(function(){ minu=null;
      /* il faut être RESTÉ appuyé : un doigt qui a déjà glissé a fait autre chose */
      if(sur && !arme) armer();
    }, MAINTIEN);
  }, true);

  document.addEventListener('pointermove', function(e){
    if(!sur) return;
    if(!arme){
      /* tant que l'appui n'est pas mûr, un vrai glissement annule le geste de couleur :
         c'est le glissement de monde, et il garde la main */
      var dx=Math.abs(e.clientX-x0), dy=Math.abs(e.clientY-y0);
      if(dx>12 || dy>12){ if(minu){clearTimeout(minu);minu=null;} sur=false; }
      return;
    }
    suivre(e);
  }, true);

  ['pointerup','pointercancel','pointerleave'].forEach(function(t){
    document.addEventListener(t, function(e){ if(arme&&t==='pointercancel') return; fin(); }, true);
  });

  window._studioGesteCouleur = { MAINTIEN:MAINTIEN, COURSE:COURSE, PAS_PAL:PAS_PAL,
                                 arme:function(){return arme;}, mot:MOT };
})();
