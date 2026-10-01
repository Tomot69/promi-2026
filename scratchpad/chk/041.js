
/* La barre Peaufiner et les réglages passent DANS le scroller (csMid) : barre en
   sticky top, réglages juste après. On scrolle pour révéler, rien ne recouvre. */
(function(){
  function lift(){
    var mid=document.getElementById('csMid'), bar=document.getElementById('csBotBar');
    if(!mid||!bar) return;
    if(bar.parentElement!==mid) mid.appendChild(bar);
    ['promiExtra','draftExtra'].forEach(function(id){
      var e=document.getElementById(id); if(e && e.parentElement!==mid) mid.appendChild(e);
    });
  }
  if(document.readyState!=='loading') lift(); else document.addEventListener('DOMContentLoaded',lift);
  var cb=document.getElementById('createBtn'); if(cb) cb.addEventListener('click',function(){ setTimeout(lift,150); });
  /* clic sur la barre : on fait défiler les réglages en vue (au lieu d'un tiroir) */
  document.addEventListener('click',function(e){
    var bar=e.target&&e.target.closest?e.target.closest('#csBotBar'):null; if(!bar) return;
    var mid=document.getElementById('csMid'); if(!mid) return;
    setTimeout(function(){ try{ mid.scrollTo({top:mid.scrollHeight,behavior:'smooth'}); }catch(_){ mid.scrollTop=mid.scrollHeight; } },20);
  }, false);
})();
