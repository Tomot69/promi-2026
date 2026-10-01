
/* LOT 4 · Peaufiner descend tout en bas de la fiche (moodboard). Le CSS ne
   déplace pas les blocs : on réordonne le DOM. On garde Peaufiner + son tiroir
   solidaires (le toggle lit box=t.nextElementSibling). */
(function(){
  function place(formId, btnId, extraId){
    var f=document.getElementById(formId), b=document.getElementById(btnId), e=document.getElementById(extraId);
    if(!f||!b) return;
    f.appendChild(b); if(e) f.appendChild(e);
  }
  function go(){ try{ place('promiForm','promiMoreBtn','promiExtra'); place('draftForm','draftMoreBtn','draftExtra'); }catch(_){}}
  if(document.readyState!=='loading') go(); else document.addEventListener('DOMContentLoaded',go);
  var cb=document.getElementById('createBtn'); if(cb) cb.addEventListener('click',function(){ setTimeout(go,90); });
})();
