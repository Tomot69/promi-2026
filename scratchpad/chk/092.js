
/* ⚑ 3.9 — ON LANCE UN CHICHE, ON NE LE PLANTE PAS (choix Tom, 17 septembre 2026 · défaut D3).
   Le Chiche partage `#planterZone` et `#addPromi` avec le Promi : le mot du geste et le bouton
   étaient ceux du Promi, contre le lexique du §2. Rien n'est déplacé ni recréé — on suit la
   nature posée sur `#createSheet`.
   ⚠ UN OBSERVATEUR QUI COMPARE AVANT D'AGIR (§8) : `applyForms`, `setHead` et le carrousel
   reposent `data-kind` sans cesse ; écrire sans comparer réveillerait l'observateur en boucle.
   Mesuré : « Lancer le Chiche » 118 px, « glisse pour lancer → » 127,7 px, dans 342. */
(function(){
  var MOTS = {
    promi : {lab:'glisse pour planter \u2192', cta:'Planter le Promi'},
    chiche: {lab:'glisse pour lancer \u2192',  cta:'Lancer le Chiche'}
  };
  function pose(){
    try{
      var cs=document.getElementById('createSheet'); if(!cs) return;
      var k=cs.getAttribute('data-kind');
      var m=MOTS[k==='chiche'?'chiche':'promi'];
      /* le Promi en mode « demander » garde SON bouton (« Demander ce Promi ») : on ne
         touche au CTA que lorsqu'il porte l'un des deux mots qu'on gère. */
      var lab=document.getElementById('planterLab');
      if(lab && lab.textContent!==m.lab) lab.textContent=m.lab;
      var b=document.getElementById('addPromi');
      if(b){ var t=(b.textContent||'').trim();
        if((t===MOTS.promi.cta || t===MOTS.chiche.cta) && t!==m.cta) b.textContent=m.cta; }
    }catch(e){}
  }
  function armer(){
    var cs=document.getElementById('createSheet'); if(!cs){ setTimeout(armer,300); return; }
    try{ new MutationObserver(pose).observe(cs,{attributes:true,attributeFilter:['data-kind']}); }catch(e){}
    pose();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',armer);
  else armer();
  window._voixChiche = pose;
})();
