
/* ⚑⚑ 23 SEPTEMBRE 2026, second tour (Tom) — ON NE PARTAGE PLUS SON NOYAU, ON PARTAGE SA PELOTE.
   « Le Noyau porte des proportions de paroles tenues : le partager, c'est partager son score —
   exactement ce que le produit refuse partout ailleurs. Il sort du partage. Ce qu'on partage,
   c'est la Pelote. Belle, abstraite, indéchiffrable pour un inconnu — c'est ce qui la rend
   partageable. »
   CE QUE CE BLOC FAIT, POINT PAR POINT :
     1 · LE SUJET perd « Le Noyau » et gagne « Ma Pelote » ;
     2 · la rangée « LE NOYAU » (masqué / posé / taille) sort du panneau avec lui ;
     3 · des six commandes de « CE QU'IL MONTRE » il ne reste que **Promitteurs** : « Harmonie
         chiffrée », « Jauge équilibre » et « Disques » sont des MESURES, « Noyau » sort avec le
         Noyau, et le sixième désignait l'ANCIENNE couronne à rayons, retirée ;
     4 · la catégorie est renommée **« DANS L'IMAGE »** et remonte en DEUXIÈME position, avec
         LE SUJET et QUELS PROMI — les trois choix d'affichage passent devant les cinq réglages
         techniques (format, fond, mot-marque, QR, texte des dalles) ;
     5 · la Pelote se compose SEULE : le fond choisi, la Pelote au centre, le mot-marque, le QR
         si on le veut. Pas de Toile derrière elle — c'est la superposition que Tom a vue, et
         elle n'a pas lieu d'exister : la Pelote EST le sujet, pas un bijou posé sur un fond.
   ⚠ TROIS LIBELLÉS PROPOSÉS pour « CE QU'IL MONTRE » (QUESTIONS · Q283) : **DANS L'IMAGE** ·
   **CE QU'ON VOIT** · **CE QUE L'IMAGE PORTE**. J'ai posé le premier, le plus sobre. */
(function(){
  function $(s,r){ return (r||document).querySelector(s); }
  function $$(s,r){ return [].slice.call((r||document).querySelectorAll(s)); }

  /* ── 1 · LE SUJET : « Le Noyau » → « Ma Pelote » ── */
  /* ⚠ IL Y A PLUSIEURS `#shMode` DANS LA PAGE — mesuré : `document.querySelectorAll('#shMode
     button')` en rend quatre alors que `querySelector('#shMode')` n'en voit qu'un. Un `$('#shMode')`
     ne nettoie donc qu'UNE des rangées, et « Le Noyau » reste à l'écran. On vise l'ATTRIBUT,
     partout dans le document, jamais un id qu'on croit unique. */
  function sujet(){
    /* ⚠ ON MASQUE, ON NE DÉTRUIT PAS — et c'est LA condition pour que ça tienne. Mesuré :
       retiré du DOM, « Le Noyau » **revient 2,5 s plus tard** ; `pose()` (lot du 12 septembre)
       rappelle `bouton_noyau()`, dont le garde est « si le bouton existe déjà, ne rien faire ».
       En le laissant en place, masqué, ce garde joue POUR nous : le créateur ne recrée rien, et
       aucune fonction ne disparaît (§9). */
    $$('[data-mode="noyau"]').forEach(function(ny){
      if(ny.getAttribute('data-hors')==='1') return;
      ny.setAttribute('data-hors','1');
      ny.style.setProperty('display','none','important');
      ny.classList.remove('on');
      ny.setAttribute('aria-hidden','true'); ny.tabIndex=-1; });
    if(window.shareMode==='noyau'){ window.shareMode='toile';
      try{ var t=$('[data-mode="toile"]'); if(t) t.click(); }catch(_){} }
    var rangs=$$('#shMode, [id=shMode]');
    if(!rangs.length) return;
    var m=rangs[rangs.length-1];
    if(m.querySelector('[data-mode="pelote"]')) return;
    var b=document.createElement('button');
    b.setAttribute('data-mode','pelote'); b.textContent='Ma Pelote';
    m.appendChild(b);
    b.onclick=function(){
      try{
        window.shareMode='pelote';
        $$('#shMode button').forEach(function(x){ x.classList.toggle('on', x===b); });
        var sc=$('#shareScreen'); if(sc){ sc.classList.remove('shc-noyau'); sc.classList.add('shc-pelote'); }
        if(window.shareRender) window.shareRender();
      }catch(e){}
    };
    $$('#shMode button').forEach(function(x){ if(x===b) return;
      var av=x.onclick;
      x.onclick=function(e){ var sc=$('#shareScreen'); if(sc) sc.classList.remove('shc-pelote');
        if(av) return av.call(this,e); };
    });
  }

  /* ── 3 · LES MESURES SORTENT ── on retire NOMMÉMENT, jamais une famille (§8) */
  var HORS=['noyau','pelote','disques'];       /* data-p */
  var HORS_TOG=['pct','bal'];                  /* data-tog : harmonie chiffrée, jauge équilibre */
  function mesures(){
    function range(b){ if(b.getAttribute('data-hors')==='1') return;
      b.setAttribute('data-hors','1'); b.style.setProperty('display','none','important');
      b.classList.remove('on'); b.setAttribute('aria-hidden','true'); b.tabIndex=-1; }
    $$('#shNoyauParts [data-p], #sealParts [data-p]').forEach(function(b){
      if(HORS.indexOf(b.getAttribute('data-p'))>=0) range(b); });
    $$('#shNoyauParts [data-tog], #sealParts [data-tog]').forEach(function(b){
      if(HORS_TOG.indexOf(b.getAttribute('data-tog'))>=0) range(b); });
    try{ if(window._sealParts){ window._sealParts.noyau=false; window._sealParts.pelote=false;
           window._sealParts.disques=false; } }catch(_){}
  }

  /* ── 4 · L'ORDRE DU PANNEAU ── les choix d'affichage devant les réglages techniques */
  var ORDRE=['LE SUJET','DANS L’IMAGE','QUELS PROMI',
             'LE FORMAT','LE FOND DE L’IMAGE','LE MOT-MARQUE','LE QR','LE TEXTE DES DALLES'];
  function panneau(){
    var pi=$('#shcPile'); if(!pi) return;
    var regs=$$('.shc-reg', pi); if(!regs.length) return;
    regs.forEach(function(c){
      var l=c.querySelector('.l'); if(!l) return;
      var t=(l.textContent||'').trim();
      if(t==='CE QU’IL MONTRE' || t==="CE QU'IL MONTRE"){ l.textContent='DANS L’IMAGE'; }
      if(t==='LE NOYAU'){ c.setAttribute('data-hors','1'); }
    });
    /* la rangée du Noyau sort du flux, elle n'est pas détruite (§9 : rien ne disparaît) */
    $$('.shc-reg[data-hors]', pi).forEach(function(c){ c.style.display='none'; });
    /* on réordonne : on déplace des nœuds, on n'en recrée aucun (§8) */
    var par={}; $$('.shc-reg', pi).forEach(function(c){
      var l=c.querySelector('.l'); if(l) par[(l.textContent||'').trim()]=c; });
    var note=$('#shcNote', pi);
    /* ⚠ ON COMPARE AVANT D'AGIR (§8, le `MutationObserver` qui s'auto-déclenche). Au premier
       jet je réinsérais les huit rangées à chaque passage : chaque `insertBefore` mutait le DOM,
       l'observateur se réveillait, et la page ne rendait plus la main. On ne déplace QUE si
       l'ordre rendu diffère de l'ordre voulu. */
    var actuel=$$('.shc-reg', pi).filter(function(c){ return c.style.display!=='none'; })
                 .map(function(c){ var l=c.querySelector('.l'); return l?(l.textContent||'').trim():''; });
    var voulu=ORDRE.filter(function(n){ return !!par[n]; });
    if(actuel.join('|')===voulu.join('|')) return false;
    voulu.forEach(function(nom){ pi.insertBefore(par[nom], note||null); });
    return true;
  }

  function passe(){ try{ sujet(); mesures(); return panneau(); }catch(e){ return false; } }
  window._v13Partage=passe;
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',passe); else passe();
  [150,600,1400].forEach(function(t){ setTimeout(passe,t); });
  try{ var sb=document.getElementById('shareBtn'); if(sb) sb.addEventListener('click',function(){ setTimeout(passe,120); setTimeout(passe,600); }); }catch(_){}
  /* l'observateur ne vise QUE le panneau du partage, et il se met en sourdine pendant sa
     propre écriture — sans quoi il se réveille lui-même (§8). */
  var _mo=null, _dedans=false;
  function arme(){
    var pi=$('#shcPile'); if(!pi || _mo) return;
    _mo=new MutationObserver(function(){ if(_dedans) return; _dedans=true;
      try{ passe(); }finally{ setTimeout(function(){ _dedans=false; },0); } });
    _mo.observe(pi,{childList:true});
  }
  [300,1000,2000].forEach(function(t){ setTimeout(arme,t); });
  /* ⚠ LE BOUTON « Le Noyau » SE RECRÉE TOUT SEUL. Le lot du 12 septembre le pose sur ses
     propres minuteries : le retirer une fois ne suffit pas — mesuré, il revenait à côté de
     « Ma Pelote ». On veille sur `#shMode` et on le retire dès qu'il reparaît, en comparant
     avant d'agir pour ne pas se réveiller soi-même (§8). */
  (function(){
    var mo=null, dedans=false;
    function veille(){
      var m=$('#shMode'); if(!m || mo) return;
      mo=new MutationObserver(function(){ if(dedans) return;
        var ny=m.querySelector('[data-mode="noyau"]'); if(!ny) return;
        dedans=true; try{ ny.parentNode.removeChild(ny); sujet(); }
        finally{ setTimeout(function(){ dedans=false; },0); } });
      mo.observe(m,{childList:true});
    }
    [200,800,1600,3000].forEach(function(t){ setTimeout(veille,t); });
  })();

  /* ── 5 · LA COMPOSITION DE LA PELOTE ──────────────────────────────────
     Le fond de l'image (le réglage existant), la Pelote au centre à **0,78 du petit côté**, le
     mot-marque à sa place, le QR si on le veut. Rien d'autre — pas de Toile dessous, pas de
     libellé, pas de chiffre. « Indéchiffrable pour un inconnu », c'est le cahier des charges. */
  function fondImage(){
    try{ var d=(typeof _sealDark!=='undefined') ? _sealDark : true;
      return d ? '#100D0B' : '#F7F0DE'; }catch(_){ return '#100D0B'; }
  }
  function peintPelote(cv, Wp, Hp){
    var g=cv.getContext('2d'); if(!g) return false;
    g.setTransform(1,0,0,1,0,0);
    g.fillStyle=fondImage(); g.fillRect(0,0,cv.width,cv.height);
    var src=null; try{ src=window._aura && window._aura.pelote ? window._aura.pelote() : null; }catch(_){}
    if(!src || !src.width) return false;
    var cote=Math.min(cv.width, cv.height)*0.78;
    var k=cote/Math.max(src.width, src.height);
    var dw=src.width*k, dh=src.height*k;
    g.drawImage(src, (cv.width-dw)/2, (cv.height-dh)/2, dw, dh);
    return true;
  }
  window._shPeintPelote=peintPelote;

  /* on ENVELOPPE `shareRender` (§8 : le moteur de l'écran se redimensionne lui-même) */
  function enveloppe(){
    if(window._shRenderV13 || typeof window.shareRender!=='function') return;
    var f=window.shareRender;
    window.shareRender=function(){
      var r=f.apply(this,arguments);
      try{
        if(window.shareMode==='pelote'){
          var cv=document.getElementById('shCanvas');
          if(cv) peintPelote(cv);
          try{ var g=cv.getContext('2d'); if(window._shPreviewQR) window._shPreviewQR(g, cv.width, cv.height); }catch(_){}
        }
      }catch(e){}
      return r;
    };
    window._shRenderV13=true;
  }
  enveloppe(); setTimeout(enveloppe,400); setTimeout(enveloppe,1200);
})();
