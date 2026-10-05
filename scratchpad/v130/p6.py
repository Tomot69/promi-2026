import io
S=io.open('app.html',encoding='utf-8').read()
old="""  window._aura = {
    etat:function(){"""
new="""  window._aura = {
    /* v130 (C-049) : l'Aura AFFICHÉE se remet à l'état réel sans se rouvrir — ni ton neuf, ni souffle relancé */
    rafraichit:function(){ if(!actif()) return false; try{ remplit(); prepare(); }catch(e){ window._auraErreur=String(e&&e.stack||e); } return true; },
    etat:function(){"""
assert S.count(old)==1; S=S.replace(old,new)
lot = r'''<script id="lot-V130-REACTIF">
/* ⚑ v130 (C-049, Tom, 5 oct. 2026) — « Chaque écran doit refléter l'état réel immédiatement, sans recharger la page […] une seule
   source de vérité, et chaque écran qui s'y abonne. »
   LES DEUX CAUSES, mesurées par `redteam_reactif` (24/29 avant) :
   1 · L'AURA N'ÉTAIT BÂTIE QU'À SON OUVERTURE (`ouvre()`), et `closeAll()` ne lui retire pas `.show` (§8) : une parole tenue ou
       retirée depuis une fiche ouverte PAR-DESSUS elle la laissait telle quelle — la liste « Ce que tu as tenu » gardait une parole
       retirée, ou n'avait pas la parole qu'on venait de tenir. `syncAll` appelait l'ancien `buildAura`, qui ne peint plus cet écran.
   2 · LE FIL GARDAIT LES ÉVÉNEMENTS D'UNE PAROLE RETIRÉE : son journal (`FEED`) n'est pas la liste des paroles ; une carte y restait
       pour une parole qui n'existe plus.
   LA SOURCE DE VÉRITÉ est `promises` (et `NUE`). `window._paroles.signe()` en rend la signature ; `publie()` prévient les écrans
   abonnés, qui COMPARENT AVANT D'AGIR : un écran affiché se rebâtit, un écran fermé se rebâtit à son ouverture (c'était déjà le cas
   de l'Index et du Fil). `syncAll` publie ; et après chaque geste, si la signature a changé sans que personne n'ait publié, on publie
   (aucun chemin ne peut plus oublier). Rien ici ne touche un écran fermé : la plantation garde son rythme (v60). */
(function(){
  function signe(){ try{
      return promises.map(function(p){ return [p.id,p.status,p.title,p.nuee||'',p.draft?1:0,p.req?1:0,p.who||'',p.from||'',p.due||'',p.chiche?1:0,p.pending?1:0].join('\u0001'); }).join('\u0002')
        +'\u0003'+Object.keys(NUE).map(function(k){ return k+'='+NUE[k]; }).join('\u0002');
    }catch(e){ return ''; } }
  var AB=[], VU=signe();
  function abonne(nom, fn){ AB.push({nom:nom, fn:fn, s:VU}); }
  function publie(sauf){ var s=signe(); VU=s;
    AB.forEach(function(a){ if(a.s===s) return; a.s=s; if(sauf && sauf[a.nom]) return; try{ a.fn(); }catch(e){} }); }
  function vis(id){ var e=document.getElementById(id); return !!e && (e.classList.contains('show') || e.classList.contains('in')); }
  window._paroles={signe:signe, abonne:abonne, publie:publie};

  /* le Fil ne montre jamais une parole qui n'existe plus (le journal reste entier : une suppression annulée la rend) */
  var _bf=window.buildFeed;
  if(typeof _bf==='function') window.buildFeed=function(){
    var F0=FEED, r;
    try{ var ids={}; promises.forEach(function(p){ ids[p.id]=1; });
      FEED=F0.filter(function(f){ return f.pid==null || ids[f.pid]; }); }catch(e){ FEED=F0; }
    try{ r=_bf.apply(this,arguments); }finally{ FEED=F0; }
    return r; };

  abonne('index', function(){ if(vis('indexSheet') && typeof buildIndex==='function') buildIndex(); });
  abonne('fil',   function(){ if(vis('feedView') && typeof window.buildFeed==='function') window.buildFeed(); });
  abonne('aura',  function(){
    var sc=document.getElementById('auraScreen'); if(!sc || !sc.classList.contains('show')) return;      /* fermée : `ouvre()` la rebâtit */
    var n=0; (function essai(){
      if(window._tenirAnime && n++<240){ requestAnimationFrame(essai); return; }                           /* jamais pendant l'animation de « tenir » (v124) */
      try{ if(window._aura && window._aura.rafraichit) window._aura.rafraichit(); }catch(e){} })(); });
  abonne('cercle', function(){
    try{ if(typeof curNuee==='undefined' || !curNuee) return;
      var dp=document.getElementById('detailPoster'); if(!dp || !dp.classList.contains('show')) return;
      var att=promises.filter(function(p){ return !p.draft && !p.req && p.nuee===curNuee; });
      var li=[].slice.call(dp.querySelectorAll('.nf-item')), txt=li.map(function(e){ return e.textContent; }).join('\u0002');
      var juste = li.length===att.length && att.every(function(p){ return txt.indexOf(p.title)>=0; });
      if(!juste && typeof window.renderNueeDetail==='function') window.renderNueeDetail();                 /* on compare avant d'agir (§8) */
    }catch(e){} });

  var _sa=window.syncAll;
  if(typeof _sa==='function') window.syncAll=function(){ var r=_sa.apply(this,arguments); publie({index:1, fil:1}); return r; };
  /* le filet : un geste a changé les paroles et personne n'a publié */
  function veille(){ setTimeout(function(){ if(signe()!==VU) publie(); }, 0); }
  ['click','pointerup','touchend','keyup','change'].forEach(function(t){ document.addEventListener(t, veille, true); });
})();
</script>
</body>'''
assert S.count("</script>\n</body>")==1
S=S.replace("</script>\n</body>", "</script>\n"+lot)
io.open('app.html','w',encoding='utf-8').write(S)
