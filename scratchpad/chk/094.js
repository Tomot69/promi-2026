
/* ⚑ 5 · LE RETOUR DU MENU COULEUR (Tom, 18 septembre 2026).
   « Quand on ouvre les couleurs, on ne peut plus revenir au menu de base clair/sombre. »
   Le panneau s'ouvre par la classe `stp-pals` sur `#studioScreen` ; on la retire, c'est tout.
   ⚠ On ne recrée rien et on ne déplace rien : on AJOUTE un bouton dans `#stpPals`, et il
   n'existe qu'une fois (on compare avant d'agir, §8). */
(function(){
  function pose(){
    try{
      var pl=document.getElementById('stpPals'); if(!pl) return;
      if(pl.querySelector('.stp-retour')) return;
      var b=document.createElement('button');
      b.className='stp-retour'; b.type='button';
      b.setAttribute('aria-label','Revenir au menu');
      b.innerHTML='\u2190 Retour';
      b.onclick=function(ev){ ev.stopPropagation();
        var s=document.getElementById('studioScreen'); if(s) s.classList.remove('stp-pals'); };
      pl.insertBefore(b, pl.firstChild);
    }catch(e){}
  }
  function armer(){ pose();
    try{ new MutationObserver(pose).observe(document.body,{childList:true,subtree:true}); }catch(e){}
    document.addEventListener('click', function(){ setTimeout(pose,120); }, true);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',armer); else armer();
  window._studioRetour = pose;
})();
