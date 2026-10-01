
(function(){
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function pastille(inp){
    var box = inp.closest && inp.closest('#csPhrase, #nueePhrase, #draftPhrase');
    return box ? box.querySelector('.ph-m.ph-on') : null;
  }
  function peint(inp){
    var m = pastille(inp); if(!m) return;
    var v = inp.value || '';
    var cible = m.querySelector('.ph-mot') || m;
    var h = v ? (esc(v) + '<i class="ph-caret"></i>') : '<i class="ph-caret"></i>\u2026';
    if(cible.innerHTML !== h) cible.innerHTML = h;
  }
  window._curseurPeint = peint;
  var NON = /^(date|time|datetime-local|month|week|range|checkbox|radio|file|color|button|submit|hidden)$/i;
  document.addEventListener('focusin', function(e){
    var t = e.target; if(!t || !t.matches) return;
    if(t.matches('.ph-in')){ peint(t); try{ if(window._ppTout) window._ppTout(); }catch(_){} return; }
    if(t.matches('input[placeholder], textarea[placeholder]') && !NON.test(t.type || '')){
      if(!t.hasAttribute('data-ph0')) t.setAttribute('data-ph0', t.getAttribute('placeholder') || '');
      if(t.getAttribute('placeholder') !== '\u2026') t.setAttribute('placeholder', '\u2026');
    }
  }, true);
  document.addEventListener('focusout', function(e){
    var t = e.target;
    if(t && t.hasAttribute && t.hasAttribute('data-ph0')){ t.setAttribute('placeholder', t.getAttribute('data-ph0')); t.removeAttribute('data-ph0'); }
  }, true);
  document.addEventListener('input', function(e){
    var t = e.target; if(t && t.matches && t.matches('.ph-in')) peint(t);
  }, false);
  /* les exemples tournent d'une page + à la suivante */
  document.addEventListener('click', function(e){
    if(e.target && e.target.closest && e.target.closest('#createBtn')) window._ppExIx = (window._ppExIx == null) ? 0 : window._ppExIx + 1;
  }, true);
})();
