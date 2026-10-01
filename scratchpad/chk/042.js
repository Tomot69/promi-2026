
/* Calcule la hauteur de cale : vp − hauteur des réglages, pour que le scroll amène
   la barre Peaufiner pile au bord haut (elle s'y colle), réglages entièrement dessous. */
(function(){
  function tail(){
    var mid=document.getElementById('csMid'); if(!mid) return;
    var cs=document.getElementById('createSheet'); var kind=cs?cs.getAttribute('data-kind'):null;
    var bar=document.getElementById('csBotBar');
    var extra=document.getElementById(kind==='draft'?'draftExtra':'promiExtra');
    var sp=document.getElementById('csPeaufTail');
    if(!sp){ sp=document.createElement('div'); sp.id='csPeaufTail'; sp.setAttribute('aria-hidden','true'); }
    if(sp.parentElement!==mid) mid.appendChild(sp);
    if(!bar||!extra||!kind){ sp.style.height='0px'; return; }
    var vp = mid.clientHeight - bar.offsetHeight;
    var need = Math.max(0, vp - extra.offsetHeight);
    sp.style.height = need+'px';
  }
  window._csPeaufTail=tail;
  var cb=document.getElementById('createBtn'); if(cb) cb.addEventListener('click',function(){ [250,600,1000].forEach(function(t){setTimeout(tail,t);}); });
  document.addEventListener('click',function(e){
    if(e.target&&e.target.closest&&e.target.closest('#createSheet .tile')) [300,700].forEach(function(t){setTimeout(tail,t);});
  }, false);
})();
