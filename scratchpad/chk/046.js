
/* marque la fiche « jeune » (≤1 Promi) et ajoute un mot d'invite sous le fil. */
(function(){
  function maj(){ try{
    var fil=document.getElementById('dpNueeFil'); if(!fil) return;
    var items=fil.querySelectorAll('.nf-item'); var jeune=items.length<=1;
    fil.classList.toggle('nf-jeune', jeune);
    var inv=fil.querySelector('.nf-invite');
    if(jeune){ if(!inv){ inv=document.createElement('div'); inv.className='nf-invite'; fil.appendChild(inv); }
      inv.textContent = items.length? 'Plante le Promi suivant →' : 'Plante le premier Promi de ton Cercle →'; }
  }catch(_){} }
  var of=window.renderNueeDetail;
  if(of){ window.renderNueeDetail=function(){ var r=of.apply(this,arguments); setTimeout(maj,40); setTimeout(maj,260); return r; }; }
  document.addEventListener('click', function(e){ if(e.target&&e.target.closest&&e.target.closest('#dpNueeFil,#detailPoster')) setTimeout(maj,120); }, false);
})();
