
/* ⚑ L'ACCUEIL, DIRECTION B (Q212 · Q213, Tom 13 sept. 2026). On DÉPLACE les commandes de l'app, jamais on ne les recrée :
   leurs gestionnaires suivent. Plateau : « Promi » (Fraunces 27, le i bleu), « N paroles · N Nuées », Partager, Réglages
   (le Cercle vit dans les Réglages : porte « ✦ Le Cercle » vérifiée au doigt). Barre : Studio · Aura | + | Index · Fil. */
(function(){
  var ICO={
    studio:'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M7 11 L14 9 L16 15 L11 20 L6 17 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M18 8 L25 10 L26 17 L20 19 L17 13 Z" fill="currentColor"/><path d="M13 20 L20 21 L19 26 L13 26 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    aura:'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><circle cx="16" cy="16" r="10" stroke="currentColor" stroke-width="2"/><path d="M16 16 L16 8 A8 8 0 0 1 23.4 19 Z" fill="currentColor"/></svg>',
    index:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><rect x="4.5" y="5" width="10" height="22" rx="3"/><rect x="17.5" y="5" width="10" height="22" rx="3"/><path d="M4.5 14 Q7 12 9.5 14 T14.5 14 M17.5 14 Q20 12 22.5 14 T27.5 14" stroke-linecap="round"/></svg>',
    fil:'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M16 6.4 C11.6 6.4 9.4 9.2 9.4 13.2 C9.4 18.6 7.6 20.4 7.6 20.4 L24.4 20.4 C24.4 20.4 22.6 18.6 22.6 13.2 C22.6 9.2 20.4 6.4 16 6.4 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M13.6 23.4 A2.6 2.6 0 0 0 18.4 23.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    share:'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M16 20 L16 7 M16 7 L11.5 11.5 M16 7 L20.5 11.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.5 15 L8.5 25 L23.5 25 L23.5 15" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    regl:'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 11 H8.6 M15.4 11 H27 M5 21 H17.6 M24.4 21 H27" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="11" r="3.4" stroke="currentColor" stroke-width="2"/><circle cx="21" cy="21" r="3.4" stroke="currentColor" stroke-width="2"/></svg>'
  };
  function icone(el, svg){ if(!el) return; var o=el.querySelector('svg'); var t=document.createElement('span'); t.innerHTML=svg; var n=t.firstChild;
    if(o) el.replaceChild(n,o); else el.insertBefore(n, el.firstChild); }
  function poser(){
    var dv=document.getElementById('device'); if(!dv || document.getElementById('accPlat')) return;
    /* le mode signature : plus de porte, et plus d'état gardé */
    try{ localStorage.setItem('promi_sig','0'); localStorage.setItem('promi_sigdemo','1'); }catch(_){}
    dv.classList.remove('sigmode'); var bb=document.getElementById('brandBtn'); if(bb) bb.classList.remove('sig-on');
    /* le plateau */
    var pl=document.createElement('div'); pl.id='accPlat'; pl.className='acc-plat';
    pl.innerHTML='<span class="acc-mm">Prom<i>i</i></span><span class="acc-ligne" id="accLigne"></span>';
    dv.appendChild(pl);
    ['shareBtn','settingsBtn'].forEach(function(id){ var b=document.getElementById(id); if(b){ pl.appendChild(b); } });
    icone(document.getElementById('shareBtn'), ICO.share); icone(document.getElementById('settingsBtn'), ICO.regl);
    /* la barre */
    var br=document.createElement('div'); br.id='accBarre'; br.className='acc-barre'; dv.appendChild(br);
    var ix=document.createElement('div'); ix.className='dctrl'; ix.id='indexBtn'; ix.setAttribute('role','button');
    ix.innerHTML=ICO.index+'<span class="l">Index</span>';
    ix.onclick=function(){ try{ if(window.quitteVues) quitteVues(); window.ouvrirIndex(); }catch(_){} };
    ['studioBtn','souffleBtn','createBtn'].forEach(function(id){ var b=document.getElementById(id); if(b) br.appendChild(b); });
    br.appendChild(ix);
    var fb=document.getElementById('filBtn'); if(fb) br.appendChild(fb);
    icone(document.getElementById('studioBtn'), ICO.studio); icone(document.getElementById('souffleBtn'), ICO.aura); icone(fb, ICO.fil);
    /* le + s'ouvre sur place */
    var ch=document.createElement('div'); ch.id='accChoix'; ch.className='acc-choix';
    ch.innerHTML='<div class="acc-pil" data-k="nuee" style="top:0;background:#C9A8F5;color:#291547">Un Cercle<small>un groupe, un projet</small></div>'
      +'<div class="acc-pil" data-k="chiche" style="top:74px;background:#FFB8D2">Un Chiche<small>un défi lancé</small></div>'
      +'<div class="acc-pil" data-k="promi" style="top:148px;background:#82AEF8">Un Promi<small>à quelqu’un, ou à toi</small></div>';
    dv.appendChild(ch);
    /* ⚑ v103 (Tom : « des flashs entre le + et le choix de la nature ») — la page + était montrée dès que sa NATURE
       était posée ; mais elle se compose ensuite sur trois ou quatre images (le champ, la phrase coupée en pastilles, le
       mot-marque du plateau). Vu image par image : un plateau vide, un champ crème, la phrase d'un seul bloc. Elle reste
       cachée jusqu'à ce que sa composition ne bouge plus deux images de suite (plafond 1 s). */
    function revele(s){ if(!s || !s.classList.contains('acc-passe') || s._revele) return; s._revele=true;
      var t0=performance.now(), avant=null, pareil=0;
      function sig(){ try{ var ph=document.getElementById('csPhrase'), cv=document.getElementById('csTrameCv'), mk=s.querySelector('.cs-mark');
        var r=''; if(ph) ph.querySelectorAll('*').forEach(function(e){ var q=e.getBoundingClientRect(); if(q.width) r+=Math.round(q.left)+','+Math.round(q.top)+','+Math.round(q.width)+';'; });
        return (s.className)+'|'+(cv&&cv.getAttribute('data-champ'))+'|'+(mk?Math.round(mk.getBoundingClientRect().width)+(mk.innerHTML.length):'')+'|'+r; }catch(_){ return String(Math.random()); } }
      /* et le plateau doit se LIRE : son mot-marque et FERMER recevaient leur encre d'une passe plus tardive (encreUn,
         ~130 ms après la page + montrée) — crème sur crème, le plateau paraissait vide. On demande l'encre au MÊME
         propriétaire (encreUn) juste avant de montrer : une seule décision, prise plus tôt. */
      (function pas(){ var g=sig(); pareil = (g===avant) ? pareil+1 : 0; avant=g;
        /* ⚠ et chaque ouverture ou clic de tuile relance la composition par des MINUTEURS — arme à +60 et +340 ms, le
           champ (renderCsDalle) à +240, la passe du plateau (encre) à +120 et +420 : on attend 450 ms après le DERNIER,
           sinon on montre un état que le suivant défait (vu : la phrase du Promi, un champ crème, un plateau vide, puis
           la phrase du Chiche). Deux images identiques ne suffisent pas : entre deux minuteurs, rien ne bouge. */
        if((pareil>=2 && performance.now()-(s._dernierClic||0)>450 && s.querySelector('.enh')) || performance.now()-t0>1000){ try{ if(window._encrePlateau) window._encrePlateau('createSheet'); }catch(_){} s.classList.remove('acc-passe'); s._revele=false; return; }
        requestAnimationFrame(pas); })(); }
    ch.querySelectorAll('.acc-pil').forEach(function(pi){ pi.addEventListener('click', function(ev){
      ev.stopPropagation(); ch.classList.remove('ouvert');
      var k=pi.getAttribute('data-k');
      var _cs0=document.getElementById('createSheet'); if(_cs0){ _cs0.classList.add('acc-passe'); _cs0._dernierClic=performance.now(); }   /* ⚑ 14 sept. : on ne montre pas les tuiles au passage */
      window._accPasse=true; window._accNature=k; try{ document.getElementById('createBtn').click(); }catch(_){} window._accPasse=false; window._accNature=null;
      /* la tuile se choisit une fois la page + posée — trop tôt après un vrai toucher, le choix ne prenait pas (mesuré) */
      /* ⚠ ET ON ATTEND UN ÉTAT STABLE : pour Promi, la page + paraît « formée » un instant (`pp pp-promi`), puis l'app la remet
         sur l'écran des tuiles 60 ms plus tard et efface la nature (mesuré). On ne s'arrête qu'après deux relevés justes. */
      /* ⚑ v21 : on n'attend plus les minuteurs d'`arme()` (+60 / +340 ms après chaque clic) — on l'appelle tout de
         suite ; et la nature n'est tenue pour posée que si la page + la PORTE (`pp` + `pp-<nature>`, sans `pp-choix`) :
         avec un simple `data-kind`, la boucle pouvait s'arrêter AVANT que l'écran des tuiles soit posé, et la page +
         restait sur les tuiles (vu en chronologie). */
      try{ if(window._ppArme) window._ppArme(); }catch(_){}
      var essai=0, bons=0, dernier=-1e9; (function choisit(){ essai++; var s=document.getElementById('createSheet'), t=document.querySelector('#createSheet .tile[data-kind='+k+']');
        if(!s) return;
        /* la PHRASE aussi doit porter la nature : le premier clic de tuile pose `pp-chiche` sans passer la phrase en Chiche */
        var _sens=(window._phrase||{}).sens, phraseOk = k==='chiche' ? _sens==='chiche' : (k==='promi' ? _sens!=='chiche' : true);
        var mauvais = s.classList.contains('pp-choix') || s.getAttribute('data-kind')!==k || !s.classList.contains('pp-'+k) || !phraseOk;
        if(mauvais && t && performance.now()-dernier>250){ dernier=performance.now(); s._dernierClic=dernier; t.click(); try{ if(window._ppArme) window._ppArme(); }catch(_){} bons=0;
          /* on relit TOUT DE SUITE : si la nature est posée, la page + se montre sans attendre le relevé suivant */
          var _s2=(window._phrase||{}).sens, _ok2 = k==='chiche' ? _s2==='chiche' : (k==='promi' ? _s2!=='chiche' : true);
          if(_ok2 && s.getAttribute('data-kind')===k && s.classList.contains('pp') && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix')) revele(s); }   /* v103 : revele attend que la composition ne bouge plus */
        else if(!mauvais) bons++; else bons=0;
        /* ⚑ v21 (Tom) : « après le + et une nature, une latence, et l'ancienne interface passe ». Mesuré : l'écran des
           tuiles restait 0,9 à 1 s à l'écran — cette boucle attendait deux relevés stables de 150 ms en 150 ms. Elle
           interroge maintenant toutes les 30 ms, et la page + reste INVISIBLE tant que sa nature n'est pas posée. */
        if(bons>=1) revele(s);          /* montrée dès que la nature est posée… */
        if(essai<60 && (bons<2 || essai<34)) setTimeout(choisit, 30); else revele(s); })();   /* …et surveillée encore ~1 s */
    }); });
    ligne();
  }
  /* le + ouvre les trois natures sur place ; un second toucher, ou un toucher ailleurs, les referme */
  window.addEventListener('click', function(ev){
    var cb=ev.target && ev.target.closest && ev.target.closest('#createBtn');
    var ch=document.getElementById('accChoix');
    /* ⚠ SEUL UN VRAI TOUCHER ouvre les natures sur place : un appel par script (`createBtn.click()`) ouvre la page + comme
       avant — sans quoi tout ce qui ouvre la création par programme (les batteries en tête) tombait sur les pastilles. */
    if(cb && ev.isTrusted && !window._accPasse && ch && cb.closest('#accBarre')){
      ev.stopPropagation(); ev.preventDefault();
      ch.classList.toggle('ouvert'); return;
    }
    if(ch && ch.classList.contains('ouvert') && !(ev.target.closest && ev.target.closest('#accChoix'))) ch.classList.remove('ouvert');
  }, true);
  /* la ligne : « N paroles · N Nuées » — la même que l'Index (Q213) */
  function ligne(){ try{ var el=document.getElementById('accLigne'); if(!el) return;
    var n=promises.filter(function(p){return !p.req&&!p.draft;}).length, m=(typeof NUE!=='undefined')?Object.keys(NUE).length:0;
    var t=n+' parole'+(n>1?'s':'')+' · '+m+' Cercle'+(m>1?'s':''); if(el.textContent!==t) el.textContent=t; }catch(_){} }
  window._accLigne=ligne;
  try{ var _cap=window.caption; if(typeof caption==='function'){ var w=function(){ var r=_cap.apply(this,arguments); ligne(); return r; }; window.caption=w; } }catch(_){}
  setInterval(ligne, 1500);
  if(document.readyState!=='loading') poser(); else document.addEventListener('DOMContentLoaded', poser);
  [300,1200].forEach(function(t){ setTimeout(poser,t); });
  try{ (window._rangeurs=window._rangeurs||[]).push(function(){ var ch=document.getElementById('accChoix'); if(ch) ch.classList.remove('ouvert'); }); }catch(_){}
})();
