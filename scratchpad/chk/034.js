
/* LOT 5 · Au démarrage on repart en CHOIX : on retire le data-kind pré-forcé
   (promi) par les hooks d'ouverture, on masque phrase/panneau, on désélectionne
   les cartes. Le clic sur une carte (plus-sel-js) repose data-kind + affiche le
   formulaire : le fond vire, la phrase apparaît en dessous. Les cartes restent
   au-dessus — le choix est atteignable en remontant. */
(function(){
  function csEl(){return document.getElementById('createSheet');}
  function repeinsGrappe(){ try{ if(window._peintGrappe) [0,60,200].forEach(function(t){ setTimeout(window._peintGrappe,t); }); }catch(_){}}
  function midEl(){ return document.getElementById('csMid'); }
  function tailEl(mid){ var t=document.getElementById('csTail'); if(!t){ t=document.createElement('div'); t.id='csTail'; t.setAttribute('aria-hidden','true'); t.style.height='0px'; } if(t.parentNode!==mid && mid) mid.appendChild(t); return t; }
  function choix(){
    var c=csEl(); if(!c) return;
    c.removeAttribute('data-kind');
    c.classList.remove('cs-nuee'); /* repart hors Nuée (phrase sans « tout le monde / dans »). */
    ['promiForm','nueeForm','draftForm'].forEach(function(id){var f=document.getElementById(id); if(f) f.style.display='none';});
    /* moodboard ph-0 : « Un Promi » pré-sélectionné (carte bleu plein) sur l'encre. */
    var t=c.querySelectorAll('.tile'); for(var i=0;i<t.length;i++) t[i].classList.toggle('on', t[i].dataset.kind==='promi');
    ['promiForm','nueeForm','draftForm'].forEach(function(id){var f=document.getElementById(id); if(f) f.style.minHeight='';});
    var mid=midEl(); if(mid){ tailEl(mid).style.height='0px'; mid.scrollTop=0; }
    repeinsGrappe();
  }
  /* Au choix d'une nature : le milieu (cs-mid) défile pour caler le formulaire en
     tête (le haut cs-top et la barre du bas restent fixes, hors défilement).
     Titre+cartes passent hors écran par le haut, on les retrouve en remontant.
     Un talon garantit la marge de défilement. */
  function versPhrase(){
    var c=csEl(); if(!c) return;
    var k=c.getAttribute('data-kind'); if(!k) return;
    var mid=midEl(); if(!mid) return;
    /* le Chiche réutilise le formulaire du Promi (même création) — sans ça le glissement
       ciblait draftForm (caché) et Chiche ne basculait jamais vers l'écran de création. */
    var form=document.getElementById((k==='promi'||k==='chiche')?'promiForm':(k==='nuee'?'nueeForm':'draftForm'));
    repeinsGrappe();
    if(!form) return;
    tailEl(mid).style.height='0px'; /* plus de talon : le formulaire remplit le viewport */
    requestAnimationFrame(function(){
      /* bug (a) : la phrase remplit l'écran. Hauteur du viewport calculée de façon
         fiable (fiche − cs-top − barre du bas), pas via mid.clientHeight (instable). */
      var top=c.querySelector('.cs-top'), bb=document.getElementById('csBotBar');
      var vp = c.clientHeight - (top?top.offsetHeight:210) - (bb?bb.offsetHeight:62);
      form.style.minHeight = vp+'px';
      requestAnimationFrame(function(){
        try{ form.scrollIntoView({behavior:'smooth',block:'start'}); }
        catch(_){ mid.scrollTop=Math.max(0,form.offsetTop); }
      });
    });
  }
  window._csVersPhrase=versPhrase; /* pour re-caler après assignation d'une Nuée */
  var cb=document.getElementById('createBtn');
  /* ⚑ v21 : une ouverture qui vient d'une NATURE de l'accueil ne repasse pas par le choix (elle effaçait la nature posée) */
  if(cb) cb.addEventListener('click',function(){ var _n=window._accNature; setTimeout(function(){ if(!_n) choix(); },130); });
  document.addEventListener('click',function(e){
    var t=e.target && e.target.closest ? e.target.closest('#createSheet .tile') : null;
    if(t) setTimeout(versPhrase,110);
  }, false);
})();
