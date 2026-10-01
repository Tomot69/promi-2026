
(function(){
  function people(){ try{ return (typeof window.peopleList==='function'?window.peopleList():[])
    .filter(function(n){return n && n.toLowerCase()!=='moi';}); }catch(_){ return []; } }
  window._nueePhraseRendu = function(){
    var nf=document.getElementById('nueeForm'); if(!nf) return;
    var box=document.getElementById('nueePhrase');
    if(!box){ box=document.createElement('div'); box.id='nueePhrase'; nf.insertBefore(box, nf.firstChild); }
    var nom=(document.getElementById('nName')||{}).value||'';
    var membres=(window.newNueeMembers||[]);
    var avec = membres.length ? membres.join(' · ') : (window._nueeMoiSeul ? 'Moi' : 'tout le monde');   /* §5 : « Moi » choisi = avec toi seulement */
    var pl=function(cle,txt,vide){ return '<span class="ph-m'+(vide?' ph-vide':'')+'" data-np="'+cle+'">'+txt+'</span>'; };
    /* LE VERBE EST UNE PASTILLE, comme sur les deux autres natures (§5 · Nuée · écriture :
       « Je lance une Nuée » Bricolage 700/29, crème sur #291547, rayon 18). Il était en
       texte nu — la ligne existait, la pastille non. */
    var _exN = window._ppExemple ? window._ppExemple('nuee') : 'le nom';
    var h='<span class="ph-b ph-b-fixe">Je lance un Cercle</span><br><em>nommé</em> '+pl('nom', nom||_exN, !nom)
      +'<br><em>avec</em> '+pl('avec', avec, !membres.length);
    box.innerHTML='<div class="ph-txt">'+h+'</div><div class="ph-choix" id="nueeChoix"></div>';
    box.querySelectorAll('[data-np]').forEach(function(el){ el.onclick=function(){ _nueeChoix(el.getAttribute('data-np'), el); }; });
  };
  window._nueeChoix = function(cle, el){
    var zone=document.getElementById('nueeChoix'); if(!zone) return;
    document.querySelectorAll('#nueePhrase .ph-m').forEach(function(x){ x.classList.toggle('ph-on', x===el); });
    if(cle==='nom'){
      var v=(document.getElementById('nName')||{}).value||'';
      zone.innerHTML='<div class="ph-lab">LE NOM DU CERCLE</div><input class="ph-in" id="nueeNomIn" placeholder="'+(window._ppExemple?window._ppExemple('nuee'):'Week-end à Marseille')+'…" value="'+v.replace(/"/g,'&quot;')+'">';
      var i=zone.querySelector('#nueeNomIn');
      i.oninput=function(){ var n=document.getElementById('nName'); if(n){ n.value=i.value; n.dispatchEvent(new Event('input',{bubbles:true})); }
        el.textContent=i.value||(window._ppExemple?window._ppExemple('nuee'):'le nom'); el.classList.toggle('ph-vide', !i.value); };
      i.onkeydown=function(e){ if(e.key==='Enter'){ e.preventDefault(); i.blur(); } };
      i.onblur=function(){ _nueePhraseRendu(); };
      setTimeout(function(){ try{i.focus();}catch(_){} },30);
    } else {
      /* ⚑ LE MÊME CHOIX QUE LE PROMI ET LE CHICHE (lot-GENS, 13 sept. 2026) — il était en pastilles nues,
         sans initiale, sans « + ajouter quelqu'un », sans croix, et passait sous Peaufiner. */
      if(window._gensNuee) window._gensNuee(zone);
    }
  };
  function go(){ try{ var cs=document.getElementById('createSheet'); if(cs && cs.getAttribute('data-kind')==='nuee') _nueePhraseRendu(); }catch(_){} }
  document.addEventListener('click', function(e){ var t=e.target&&e.target.closest?e.target.closest('#createSheet .tile[data-kind="nuee"]'):null; if(t) setTimeout(go,220); }, false);
  var cb=document.getElementById('createBtn'); if(cb) cb.addEventListener('click', function(){ setTimeout(go,320); });
})();
