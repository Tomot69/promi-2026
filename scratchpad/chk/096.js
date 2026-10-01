
/* ⚑ v89 (Tom, Q348) — le bouton noir et blanc, dans l'encart des palettes. L'état vit dans `window._promiNB` (lu par le moteur, cOf) et
   se garde (promi_nb). On ne recrée rien : on AJOUTE un nœud à `#stpPals`, une fois (on compare avant d'agir).
   ⚑ v90 (Tom, 28 sept. : « pas de double jauge ») — la jauge noir et blanc n'existe plus à part : bouton allumé, c'est LA JAUGE DU BAS
   (`.st3-spec`, la teinte) qui devient la jauge noir et blanc — son dégradé passe du ton franc au fond, son curseur dose `j`. Éteint,
   elle redevient la teinte, curseur à la teinte du monde. La jauge est reconstruite par `buildStudio` : on l'écoute par délégation
   (capture sur le document), jamais sur le nœud. */
(function(){
  var LSg=function(k){ try{ return localStorage.getItem(k); }catch(_){ return null; } }, LSs=function(k,v){ try{ localStorage.setItem(k,v); }catch(_){ } };
  var nb=window._promiNB={ on: LSg('promi_nb')==='1', j: (function(){ var v=parseFloat(LSg('promi_nb_j')); return isFinite(v)?Math.max(0,Math.min(1,v)):0.3; })() };
  function redessine(){ try{ if(window.Toile&&Toile.redraw) Toile.redraw(); }catch(_){ } try{ if(window.onPaletteChange) window.onPaletteChange(); }catch(_){ } }
  function jauge(){ var sp=document.getElementById('st3spec'), th=document.getElementById('st3thumb'); if(!sp||!th) return;
    if(sp.classList.contains('nb')!==nb.on) sp.classList.toggle('nb', nb.on);
    var h=0; try{ h=((window.Toile&&Toile.mondeCourant&&Toile.mondeCourant().h)||0)/360; }catch(_){ }
    var l=((nb.on?nb.j:Math.max(0,Math.min(1,h)))*100)+'%'; if(th.style.left!==l) th.style.left=l; }
  function etat(b){ var v=nb.on?'true':'false'; if(b.getAttribute('aria-pressed')!==v) b.setAttribute('aria-pressed', v); jauge(); }
  function pose(){ try{
    var pl=document.getElementById('stpPals'); if(!pl) return; var b=pl.querySelector('.stp-nb');
    if(!b){ b=document.createElement('button'); b.type='button'; b.className='stp-nb'; b.setAttribute('aria-label','Noir et blanc');
      b.onclick=function(ev){ ev.stopPropagation(); nb.on=!nb.on; LSs('promi_nb', nb.on?'1':'0'); etat(b); redessine(); };
      pl.appendChild(b); }
    etat(b);
  }catch(_){ } }
  /* le doigt sur la jauge, bouton allumé : il dose le noir et blanc, et la teinte n'est pas touchée */
  var tient=null;
  function x2j(sp,cx){ var r=sp.getBoundingClientRect(); return Math.max(0,Math.min(1,(cx-r.left)/Math.max(1,r.width))); }
  function regle(sp,cx){ nb.j=x2j(sp,cx); LSs('promi_nb_j', String(nb.j)); jauge(); redessine(); }
  document.addEventListener('pointerdown', function(e){ if(!nb.on) return; var sp=e.target&&e.target.closest&&e.target.closest('#st3spec'); if(!sp) return;
    e.stopImmediatePropagation(); tient=e.pointerId; try{ sp.setPointerCapture(e.pointerId); }catch(_){ } regle(sp,e.clientX); }, true);
  document.addEventListener('pointermove', function(e){ if(tient==null||e.pointerId!==tient) return; var sp=document.getElementById('st3spec'); if(!sp) return; e.stopImmediatePropagation(); regle(sp,e.clientX); }, true);
  ['pointerup','pointercancel'].forEach(function(t){ document.addEventListener(t, function(e){ if(tient==null||e.pointerId!==tient) return; tient=null; e.stopImmediatePropagation(); }, true); });
  function armer(){ pose(); try{ new MutationObserver(function(){ var pl=document.getElementById('stpPals'); if(pl&&!pl.querySelector('.stp-nb')) pose(); else { var sp=document.getElementById('st3spec'); if(sp&&sp.classList.contains('nb')!==nb.on) jauge(); } }).observe(document.body,{childList:true,subtree:true}); }catch(_){ } }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',armer); else armer();
})();
