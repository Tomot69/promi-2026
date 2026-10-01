
/* LOT 6 — architecture flex-column (= le .ph du moodboard). Enveloppe le milieu
   (titre + cartes + formulaires) dans #csMid (qui défile), et ajoute la barre du
   bas #csBotBar (Peaufiner, fixe 62px ; vide sur le choix). Le haut cs-top et la
   barre du bas restent hors défilement. */
(function(){
  function build(){
    var cs=document.getElementById('createSheet'); if(!cs) return;
    var mid=document.getElementById('csMid');
    if(!mid){
      mid=document.createElement('div'); mid.id='csMid'; mid.className='cs-mid';
      var top=cs.querySelector('.cs-top');
      if(top && top.nextSibling) cs.insertBefore(mid, top.nextSibling); else cs.appendChild(mid);
    }
    /* déplacer les enfants « milieu » dans cs-mid, dans l'ordre */
    [].slice.call(cs.children).forEach(function(ch){
      if(ch===mid) return;
      var mv = (ch.id==='csQuest'||ch.id==='promiForm'||ch.id==='nueeForm'||ch.id==='draftForm'
                || (ch.classList&&(ch.classList.contains('tiles')||ch.classList.contains('pdots'))));
      if(mv) mid.appendChild(ch);
    });
    var bb=document.getElementById('csBotBar');
    if(!bb){
      bb=document.createElement('div'); bb.id='csBotBar';
      bb.innerHTML='<span class="cbb-lab">Peaufiner</span><span class="cbb-chev">▾</span>';
      bb.addEventListener('click',function(e){
        var k=cs.getAttribute('data-kind'); if(!k) return;
        var mt=document.getElementById(k==='draft'?'draftMoreBtn':'promiMoreBtn');
        if(mt) mt.click();
        var ex=document.getElementById(k==='draft'?'draftExtra':'promiExtra');
        setTimeout(function(){ var open=ex && ex.style.display!=='none' && getComputedStyle(ex).display!=='none'; bb.classList.toggle('open',!!open); },20);
        e.stopPropagation();
      });
    }
    cs.appendChild(bb); /* toujours dernier enfant (flex:0 0 62) */
  }
  if(document.readyState!=='loading') build(); else document.addEventListener('DOMContentLoaded',build);
  var cb=document.getElementById('createBtn');
  if(cb) cb.addEventListener('click',function(){ build(); });
  window._csBuildFlex=build;
})();
