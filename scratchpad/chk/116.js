
/* ⚑ v71 (Tom, 27 sept. 2026) — « UN MONDE NE DOIT PAS SE VERROUILLER SOUS LES YEUX DE QUELQU'UN QUI L'UTILISAIT. »
   Constaté avant : le Studio n'était PAS gardé. À la réouverture, tout le monde retombait sur Pochade · Ingénu · teinte 0,
   et `loadState` écrasait même `state.structure` par le monde courant (l. ≈ 7775). Chantourné ne se verrouillait donc pas :
   il DISPARAISSAIT, comme n'importe quel autre monde.
   Désormais : `promi_studio` garde {m, p, h, libre, acquis}.
     · m, p, h   le monde, la palette, la teinte — ce que le Studio porte (§5, « au Studio — global »)
     · libre     le monde était-il gratuit QUAND on l'a choisi (lu dans `_mondesCercle`, la seule liste)
     · acquis    les mondes débloqués (achetés, ou gardés par cette règle)
   À la réouverture : un monde choisi gratuit, devenu payant depuis, est ACQUIS — la personne le garde, et le rail le montre
   ouvert. Un monde payant choisi sous le Cercle, sans Cercle à la réouverture, n'est PAS rendu (fin d'abonnement : QUESTIONS · Q339). */
(function(){
  var CLE='promi_studio', T=window.Toile; if(!T||!T.setTheme) return;
  function lit(){ try{ return JSON.parse(localStorage.getItem(CLE)||'null'); }catch(_){ return null; } }
  function premium(){ var d=document.getElementById('device'); return !!(d&&d.classList.contains('premium')); }
  function payant(m){ return !!(window._mondesCercle&&window._mondesCercle[m]); }
  var s=lit(), pret=false;
  function ecrit(){ if(!pret) return; try{
    var m=T.curWorld(), a={}; Object.keys(_ownedDesigns||{}).forEach(function(k){ if(_ownedDesigns[k]) a[k]=1; });
    var av=lit()||{};
    /* `libre` ne se réécrit que si le monde CHANGE : un monde gardé reste « choisi gratuit » */
    var libre=(av.m===m && av.libre!=null) ? av.libre : !payant(m);
    localStorage.setItem(CLE, JSON.stringify({m:m, p:T.getPalette(), h:T.getHue(), libre:libre, acquis:a}));
  }catch(_){} }
  if(s){
    try{ Object.keys(s.acquis||{}).forEach(function(k){ _ownedDesigns[k]=true; }); }catch(_){}
    var m=s.m;
    /* ⚑ v73 (Tom, Q339) : « on ne reprend pas ce qui a été donné » — le monde qu'on utilisait reste acquis, qu'il ait été choisi
       gratuit (devenu payant depuis) ou choisi sous le Cercle (abonnement fini depuis). */
    if(m && payant(m) && !_ownedDesigns[m] && !premium()){ _ownedDesigns[m]=true; window._mondeGarde=m; }
    var rendu = m && (!payant(m) || _ownedDesigns[m] || premium());
    try{ if(rendu){ T.setTheme(m); if(typeof state!=='undefined'&&state) state.structure=m; } }catch(_){}
    try{ if(s.p) T.setPalette(s.p); if(s.h) T.setHue(s.h); }catch(_){}
    window._studioRelu={m:m, rendu:!!rendu, garde:window._mondeGarde||null};
  }
  ['setTheme','setPalette','setHue'].forEach(function(n){ var f=T[n]; if(!f||f.__v71) return;
    T[n]=function(){ var r=f.apply(this,arguments); ecrit(); return r; }; T[n].__v71=true; T[n].__orig=f; });
  /* v73 (Q339) — et si le Cercle prend fin pendant qu'on l'utilise, le monde affiché reste à la personne */
  if(typeof window.setPremium==='function' && !window.setPremium.__v73){ var sp=window.setPremium;
    window.setPremium=function(v){ if(!v){ try{ var w=T.curWorld(); if(payant(w) && !_ownedDesigns[w]){ _ownedDesigns[w]=true; window._mondeGarde=w; } }catch(_){} }
      var r=sp.apply(this,arguments); ecrit(); return r; }; window.setPremium.__v73=true; }
  pret=true; if(s) ecrit();
})();
