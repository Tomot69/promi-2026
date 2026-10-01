
/* ⚑ UNE DALLE TENUE MÈNE À SA FICHE (Tom, 11 sept. 2026 : « Toucher une dalle doit ouvrir sa fiche. Une dalle est une
   parole tenue — on doit pouvoir y aller. »). Relevé avant ce bloc : les dalles de « Ce que tu as tenu » (Aura) et de
   « Tenu ensemble » (fiche d'une personne) n'avaient AUCUN gestionnaire de toucher.
   · La porte est openDetail(id) — celle de la carte d'Index et du bandeau du Fil. L'écran d'où l'on vient reste dessous
     et ✕ y ramène (mesuré depuis l'Aura : scrim, detailPoster, auraScreen → ✕ → auraScreen).
   · Un glissement n'ouvre rien : le toucher se juge comme celui des Noyaux de l'Aura — déplacement du doigt PLUS
     défilement de la colonne, ramenés à l'écran 390, sous G.TAP (6 pt).
   · ⚠ ON OUVRE SUR LE « click », PAS AU LEVER DU DOIGT. Mesuré au vrai doigt (événements tactiles) : ouvrir sur
     pointerup, c'est ouvrir AVANT le clic que le navigateur synthétise après un toucher ; ce clic tombait sur #scrim, qui
     refermait tout — openDetail(139) appelé, fiche disparue. À la souris ce clic arrive sur la cellule : le juge à la
     souris était vert, le doigt non. Le lever du doigt ARME la porte, le clic qui suit l'ouvre.
   · Écouteurs délégués : les deux écrans rebâtissent leurs cellules à chaque ouverture. Rien d'autre ne change — ni la
     cellule, ni son dessin, ni la sphère (un toucher sur la sphère reste la caresse).
   · `window._porteAuDoigt(SEL, ouvre, colonneDe)` est la porte commune — reprise par lot-CHEMINS-PERSONNE. */
(function(){ try{
  window._porteAuDoigt = function(SEL, ouvre, colonneDe){
    function echelle(){ var d = document.getElementById('device'); return d ? (d.getBoundingClientRect().width / 390) || 1 : 1; }
    function seuil(){ try{ return (window._aura && _aura.G && _aura.G.TAP) || 6; }catch(e){ return 6; } }
    var d0 = null, arme = null;
    document.addEventListener('pointerdown', function(e){
      var c = e.target && e.target.closest ? e.target.closest(SEL) : null;
      arme = null;
      if(!c){ d0 = null; return; }
      var col = colonneDe ? colonneDe(c) : null;
      d0 = {c:c, x:e.clientX, y:e.clientY, id:e.pointerId, st:col ? col.scrollTop : 0, col:col};
    }, true);
    document.addEventListener('pointercancel', function(){ d0 = null; arme = null; }, true);
    document.addEventListener('pointerup', function(e){
      if(!d0 || e.pointerId !== d0.id) return;
      var o = d0; d0 = null;
      var c = e.target && e.target.closest ? e.target.closest(SEL) : null;
      if(c !== o.c) return;
      var s = echelle();
      var dd = Math.sqrt(Math.pow(e.clientX - o.x, 2) + Math.pow(e.clientY - o.y, 2)) / s
             + (o.col ? Math.abs(o.col.scrollTop - o.st) / s : 0);
      if(dd <= seuil()) arme = {c:c, x:e.clientX, y:e.clientY, t:Date.now()};
    }, true);
    document.addEventListener('click', function(e){
      var a = arme; arme = null;
      if(!a || Date.now() - a.t > 800) return;
      var c = e.target && e.target.closest ? e.target.closest(SEL) : null;
      if(c !== a.c) return;
      if(ouvre(c, a.x, a.y)){ e.stopPropagation(); e.preventDefault(); }
    }, true);
  };
  function pidDe(c){
    var v = c.getAttribute('data-pid');
    if(!v){ var cv = c.querySelector('canvas[data-pid]'); v = cv && cv.getAttribute('data-pid'); }
    return v ? +v : null;
  }
  window._porteAuDoigt('#auraScreen .au-c, #auraScreen .au-c2, #psCadre .ps-c', function(c){
    var id = pidDe(c);
    if(id == null || typeof window.openDetail !== 'function') return false;
    window.openDetail(id); return true;
  }, function(c){ return c.closest('#auCadre, .ps-col'); });
}catch(e){} })();
