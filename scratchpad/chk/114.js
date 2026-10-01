
/* ⚑ v35 — la composition É = E + apostrophe, SÛRE : une passe au plus par image (jamais une par mutation) ; seul le texte
   réellement EN CAPITALES est composé ; un titre recomposé plus de 20 fois en 2 s (l'app le réécrirait en retour) est laissé
   tel quel plutôt que de boucler. La première écriture observait chaque mutation du document et a fait tourner une page à
   100 % du processeur pendant près de trois heures (redteam_ecrans, 24 sept.) : le compte « Nuées » sous l'Index. */
(function(){
  var SEL='.acc-plat .acc-mm.acc-mm.acc-mm, #createSheet#createSheet#createSheet .cs-mark, #dptNat#dptNat#dptNat#dptNat#dptNat, #indexSheet#indexSheet#indexSheet .scr-ti, #feedView#feedView#feedView .scr-ti, #shareScreen#shareScreen#shareScreen .scr-t, #auraScreen#auraScreen#auraScreen .scr-t:not(.ah-head), #settingsScreen#settingsScreen#settingsScreen h1.scr-ti, #auraHelp#auraHelp .scr-t.ah-head, #plusScreen #pcCadre .pc-h, #plusScreen#plusScreen>.enh>.pl-eb, .frame #privScreen#privScreen .scr-t, .frame #langScreen#langScreen .scr-t, .frame #aboutScreen#aboutScreen .scr-t, .frame #legalScreen#legalScreen .scr-t, #device #privScreen#privScreen .scr-t, #device #langScreen#langScreen .scr-t, #device #aboutScreen#aboutScreen .scr-t, #device #legalScreen#legalScreen .scr-t, #onbV .onbv-mm';
  function aComposer(el){
    var w=document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false), n, out=[];
    while((n=w.nextNode())){ var pa=n.parentNode;
      if(/[éÉ]/.test(n.nodeValue) && pa && !(pa.closest&&pa.closest('.v35-e')) && getComputedStyle(pa).textTransform==='uppercase') out.push(n); }
    return out;
  }
  function compose(el){
    var nodes=aComposer(el); if(!nodes.length) return;
    var t0=Date.now(); if(!el.__v35t || t0-el.__v35t>2000){ el.__v35t=t0; el.__v35n=0; }
    if(++el.__v35n>20) return;
    if(!el.getAttribute('aria-label')) el.setAttribute('aria-label', el.textContent);
    nodes.forEach(function(t){
      var parts=t.nodeValue.split(/[éÉ]/), frag=document.createDocumentFragment();
      parts.forEach(function(p,k){ if(p) frag.appendChild(document.createTextNode(p));
        if(k<parts.length-1){ var s=document.createElement('span'); s.className='v35-e'; s.textContent='E';
          var a=document.createElement('span'); a.className='v35-acc'; a.setAttribute('aria-hidden','true'); a.textContent='\u2019'; s.appendChild(a); frag.appendChild(s); } });
      t.parentNode.replaceChild(frag,t);
    });
  }
  function passe(){ try{ [].forEach.call(document.querySelectorAll(SEL), compose); }catch(e){} }
  var prevu=false;
  function demande(){ if(prevu) return; prevu=true; requestAnimationFrame(function(){ prevu=false; passe(); }); }
  function armer(){ passe(); try{ new MutationObserver(demande).observe(document.body,{childList:true,subtree:true,characterData:true}); }catch(e){} }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',armer); else armer();
  window._v35Accents=passe;
})();
