
(function(){
  function $(s,r){ return (r||document).querySelector(s); }
  function $$(s,r){ return [].slice.call((r||document).querySelectorAll(s)); }
  function range(b){ if(!b || b.getAttribute('data-hors')==='1') return;
    b.setAttribute('data-hors','1'); b.style.setProperty('display','none','important');
    b.classList.remove('on'); b.setAttribute('aria-hidden','true'); b.tabIndex=-1; }

  /* ── 4 · « PROMITTEURS » NE FAIT RIEN ICI, IL SORT ──────────────────────
     VÉRIFIÉ DANS LE CODE, pas supposé : `_sealParts.prometteurs` n'est lu que par
     `renderSeal` — le peintre de l'ancien mode « Le Noyau », retiré du partage. Ni
     `sharePlanche` (le Folio) ni `shareToile` ne le regardent. Il ne peint donc rien,
     dans aucun des trois sujets. Il sort. */
  /* ── 5 · « LE MOT-MARQUE · Bricolage / Signature » SORT AUSSI (Tom : décidé depuis
     longtemps). On MASQUE, on ne détruit pas — `#shWmBri` porte `class="on"` et d'autres
     passes le relisent (§9 : aucune fonction ne disparaît). */
  var HORS_REG = ['LE MOT-MARQUE'];

  /* ── 2 · LE BOUTON « La Pelote » ───────────────────────────────
     Il vaut pour LES DEUX sujets où la Pelote peut s'inviter :
       · Mon Folio — elle prend la place de QUATRE cases, les dalles se rangent autour ;
       · Ma Toile  — la Toile est DÉCOUPÉE autour d'elle (voir `lot-V14-TOILE`).
     Sur « Ma Pelote » il disparaît : elle EST le sujet. */
  function boutonPelote(){
    $$('#shNoyauParts [data-p], #sealParts [data-p]').forEach(function(b){
      if(b.getAttribute('data-p')==='prometteurs') range(b); });
    var r=$('#shNoyauParts'); if(!r) return;
    if(r.querySelector('[data-pel]')) return;
    var b=document.createElement('button');
    b.setAttribute('data-pel','1'); b.textContent='La Pelote';
    b.classList.toggle('on', !!window.shPelote);
    b.onclick=function(){
      window.shPelote=!window.shPelote;
      b.classList.toggle('on', !!window.shPelote);
      try{ if(window.shareRender) window.shareRender(); }catch(_){}
    };
    r.appendChild(b);
  }

  function reglages(){
    var pi=$('#shcPile'); if(!pi) return;
    $$('.shc-reg', pi).forEach(function(c){
      var l=c.querySelector('.l'); if(!l) return;
      var t=(l.textContent||'').trim();
      if(HORS_REG.indexOf(t)>=0 && c.getAttribute('data-hors')!=='1'){
        c.setAttribute('data-hors','1'); c.style.setProperty('display','none','important'); }
      if(t==='DANS L’IMAGE') c.setAttribute('data-img','1');
    });
    /* la rangée « Le logo » de la feuille d'origine suit le même sort */
    var wm=$('#shWmRow'); if(wm && wm.getAttribute('data-hors')!=='1'){
      wm.setAttribute('data-hors','1'); wm.style.setProperty('display','none','important');
      var lb=wm.previousElementSibling;
      if(lb && /logo/i.test(lb.textContent||'')) lb.style.setProperty('display','none','important'); }
  }

  function passe(){ try{ boutonPelote(); reglages(); }catch(e){} }
  window._v14=passe;
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',passe); else passe();
  [150,600,1400,2600].forEach(function(t){ setTimeout(passe,t); });
  try{ var sb=document.getElementById('shareBtn');
    if(sb) sb.addEventListener('click',function(){ [120,600,1400].forEach(function(t){ setTimeout(passe,t); }); }); }catch(_){}
  /* ⚠ l'observateur ne vise QUE le panneau, et il se met en sourdine pendant sa propre
     écriture — sinon il se réveille lui-même (§8). */
  (function(){ var mo=null, dedans=false;
    function arme(){ var pi=$('#shcPile'); if(!pi||mo) return;
      mo=new MutationObserver(function(){ if(dedans) return; dedans=true;
        try{ passe(); } finally { setTimeout(function(){ dedans=false; },0); } });
      mo.observe(pi,{childList:true,subtree:true}); }
    [300,1200,2400].forEach(function(t){ setTimeout(arme,t); });
  })();
})();
