
/* ===== PEAUFINER — fiche de Nuée (lot 19, chantier G) =====
   _lot7Fiche pose la structure « barre → réglages EN DESSOUS » pour le Promi mais
   SAUTE la Nuée (elle a son propre rendu). Résultat : sur la Nuée, dpdCorps (les
   réglages) restait DANS la barre → à l'ouverture ils REMONTAIENT. Ici on applique la
   même règle universelle : on sort dpdCorps de la barre pour le poser en FRÈRE, juste
   après elle. La barre reste en bas, les réglages se découvrent SOUS elle. Rien ne
   remonte, rien ne recouvre. */
(function(){
  function peaufinerNuee(){ try{
    var dp=document.getElementById('detailPoster'); if(!dp) return;
    if(!dp.classList.contains('dp-nuee') && !dp.classList.contains('dp-mode-nuee')) return;
    var det=document.getElementById('dpDetails');    // la BARRE (dpdTog)
    var corps=document.getElementById('dpdCorps');   // les RÉGLAGES
    if(!det || !corps) return;
    var tete=document.getElementById('dpTete');
    var fil=document.getElementById('dpNueeFil');
    var main=document.getElementById('dpMain');
    if(!main){ main=document.createElement('div'); main.id='dpMain'; }
    /* contenu PRINCIPAL (header + fil) dans dpMain : il porte le min-height de remplissage
       (comme le Promi), pour que la barre tombe en bas et les réglages passent sous le pli. */
    [tete, fil].forEach(function(e){ if(e && e.parentNode!==main) main.appendChild(e); });
    /* ordre final, enfants directs du poster : dpMain → BARRE → réglages */
    dp.appendChild(main);
    dp.appendChild(det);
    dp.appendChild(corps);
    /* réglages toujours dépliés en flux sous la barre (révélés au défilement, comme le
       Promi) : pas de max-height:0 qui les cacherait une fois sortis de la barre. */
    corps.style.maxHeight='none';
  }catch(_){} }
  var of=window.renderNueeDetail;
  if(of){ window.renderNueeDetail=function(){ var r=of.apply(this,arguments);
    peaufinerNuee(); setTimeout(peaufinerNuee,60); setTimeout(peaufinerNuee,280); return r; }; }
  window._peaufinerNuee=peaufinerNuee;
})();
