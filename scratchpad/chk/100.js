
(function(){
  /* ── 2 · la porte ── */
  function porte(){
    var mm=document.querySelector('.acc-plat .acc-mm');
    if(!mm || mm.getAttribute('data-porte')==='cercle') return;
    mm.setAttribute('data-porte','cercle');
    mm.setAttribute('role','button');
    mm.setAttribute('aria-label','Ma Parole !');
    /* ⚠ UNE PORTE S'OUVRE SUR LE `click` (§8, le clic fantôme) : au doigt, le lever arme
       le clic sur le même élément, et `lot-CLIC-FANTOME` fait le reste. On arrête la
       propagation pour que le clic ne redescende pas sur le plateau. */
    mm.addEventListener('click', function(ev){
      ev.stopPropagation();
      try{ if(window.ouvreCercle) window.ouvreCercle(); }catch(_){}
    });
  }
  /* ── 3 · le titre ── le cadre est bâti par `bati()` du lot qui vend ; on repasse
       derrière lui, et on COMPARE AVANT D'AGIR (§8, l'observateur qui s'auto-déclenche). */
  function titre(){
    var h=document.querySelector('#plusScreen #pcCadre .pc-h'); if(!h) return;
    var h1=h.querySelector('.pc-h1'), h2=h.querySelector('.pc-h2'), h3=h.querySelector('.pc-h3');
    if(h1 && h1.textContent!=='MA ') h1.textContent='MA ';
    if(h2 && h2.textContent!=='PAROLE') h2.textContent='PAROLE';
    if(h3 && h3.textContent!=='\u00a0!') h3.textContent='\u00a0!';
  }
  function passe(){ porte(); titre(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',passe); else passe();
  [120,400,900,1800].forEach(function(t){ setTimeout(passe,t); });
  try{ new MutationObserver(passe).observe(document.body,{childList:true,subtree:true}); }catch(_){}
  window._v12=passe;
})();
