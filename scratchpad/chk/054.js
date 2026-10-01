
/* ═══════════════════════════════════════════════════════════════════════════════════════
   LA PHOTO — le moteur.
   · elle REMPLACE la dalle : même boîte, recadrée au centre (couverture), opacité 1 ;
   · elle est BORNÉE PAR L'ONDE en bas, comme la Toile d'une Nuée l'est déjà ;
   · l'aplat de nature reste DESSOUS : si la photo ne couvre pas tout, on voit la couleur
     de nature, jamais du vide ;
   · le mot-marque et ✕ FERMER restent lisibles par-dessus (voir `_photoVoile`).
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  if(!window._onde) return;
  var O=window._onde, W=390;

  /* ── où en est la photo de cette promesse ? ── */
  function laPhoto(p){ try{ return (p && p.photo) ? p.photo : null; }catch(_){ return null; } }
  var _cache={};
  function image(src, quand){
    if(!src) return null;
    if(_cache[src] && _cache[src].complete) return _cache[src];
    if(!_cache[src]){ var im=new Image(); im.onload=function(){ try{ quand&&quand(); }catch(_){}} ;
      im.src=src; _cache[src]=im; }
    return _cache[src].complete ? _cache[src] : null;
  }

  /* ── LA PEINTURE. On dessine dans la boîte de la dalle, en COUVERTURE (recadrage au
       centre), après avoir découpé au chemin de l'onde : rien ne dépasse en bas. ── */
  window._photoPeint=function(g, e, p, base, amp, boite){
    var src=laPhoto(p); if(!src) return false;
    var im=image(src, function(){ try{ if(window._ficheTrait)_ficheTrait();
                                       if(window._ppTrait)_ppTrait(); }catch(_){} });
    if(!im) return false;
    var b=e.dalle; if(!b) return false;
    var y=O.onde(base,amp);
    g.save();
    /* le découpage : tout ce qui est AU-DESSUS de l'onde, et rien d'autre. */
    g.beginPath(); O.chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath(); g.clip();
    /* la couverture : on remplit la boîte sans déformer, on recadre au centre. */
    var r=im.width/im.height, br=b.w/b.h, sw, sh, sx, sy;
    if(r>br){ sh=im.height; sw=im.height*br; sx=(im.width-sw)/2; sy=0; }
    else    { sw=im.width;  sh=im.width/br;  sx=0; sy=(im.height-sh)/2; }
    g.globalAlpha=1; g.globalCompositeOperation='source-over';
    g.drawImage(im, sx,sy,sw,sh, b.x,b.y,b.w,b.h);
    /* ⚠ AUCUN VOILE. J'en avais posé un pour protéger l'entête — il dessinait une bande
       sombre à bord franc sur la photo, visible et laide, et la photo « ne se superpose à
       rien ». Il était surtout INUTILE : la boîte de la dalle commence à **y = 88** (§2.7)
       et l'entête vit à **y = 38** (§3.1). La photo ne l'atteint jamais : le mot-marque et
       ✕ FERMER restent posés sur l'aplat de NATURE, dont l'encre est déjà arbitrée.
       Ce n'est pas une supposition — `redteam_photo.py` le mesure sur une photo très claire
       ET sur une photo très sombre, seuil 42. Voir QUESTIONS.md Q53. */
    g.restore();
    return true;
  };

  /* ── LE BOUTON. Sa cote suit L'ONDE, pas la boîte : `y(x)` au droit du bouton, moins un
       écart constant. Le trait monte, descend, ondule — l'écart ne change pas. ── */
  var ECART=52;                      /* du sommet du bouton au trait, sous son point */
  function poseBouton(hote, p, base, amp, rejoue){
    if(!hote) return;
    /* ⚠ JAMAIS DE BOUTON PHOTO SUR UN GARDÉ DE CÔTÉ — et on le refuse ICI, à la source.
       Les cadres 26/27 n'en portent pas, et sans aplat (Q83) le rond perd son fond : il
       sort en cercle vide. Refusé plus haut seulement, il revenait quand même — le nid
       bâti par la page + du tour précédent survivait, et une repasse le remontrait. Un
       garde posé au seul endroit qui CRÉE le nœud ne peut pas être contourné. */
    if(window._ppGarde && hote && hote.id === 'createSheet'){
      hote.querySelectorAll('.ph-photo-nid, .ph-photo-btn').forEach(function(n){
        n.style.setProperty('display','none','important'); });
      return;
    }
    var nid=hote.querySelector(':scope > .ph-photo-nid');
    if(!nid){ nid=document.createElement('div'); nid.className='ph-photo-nid'; hote.appendChild(nid); }
    hote.querySelectorAll('.ph-photo-btn').forEach(function(n){ n.style.removeProperty('display'); });
    var b=nid.querySelector('.ph-photo-btn');
    if(!b){
      b=document.createElement('button');
      b.type='button'; b.className='ph-photo-btn';
      b.setAttribute('aria-label','Photo');
      nid.appendChild(b);
      var inp=document.createElement('input');
      inp.type='file'; inp.accept='image/*'; inp.className='ph-photo-in';
      nid.appendChild(inp);
      b._in=inp;
      inp.onchange=function(){
        var f=inp.files && inp.files[0]; if(!f) return;
        var rd=new FileReader();
        rd.onload=function(){ try{ var q=b._p; if(q){ q.photo=rd.result; }
          _cache[rd.result]=null; rejoue && rejoue(); }catch(_){} };
        rd.readAsDataURL(f); inp.value='';
      };
      b.onclick=function(ev){ ev.stopPropagation();
        var q=b._p;
        /* une photo est déjà là : le MÊME bouton la retire et rend la dalle. */
        if(q && q.photo){ q.photo=null; rejoue && rejoue(); return; }
        try{ inp.click(); }catch(_){}
      };
    }
    b._p=p;
    /* ⚠ ET PAS SUR UN GARDÉ DE CÔTÉ. C'est ICI que le nid se montre — la ligne qui suit
       reposait `display:block !important` APRÈS le garde du haut, et le rond revenait :
       le refus n'a de valeur qu'à l'endroit qui montre, pas seulement à celui qui crée. */
    if(window._ppGarde && hote && hote.id === 'createSheet'){
      nid.style.setProperty('display','none','important'); return; }
    nid.style.setProperty('display','block','important');
    var aPhoto=!!laPhoto(p);
    b.innerHTML = aPhoto
      /* revenir à la dalle : le signe du retour, pas un mot */
      ? '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 5 L4 9 L8 13" '
        +'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        +'<path d="M4 9 h9 a6 6 0 0 1 6 6 v1" stroke="currentColor" stroke-width="2" '
        +'stroke-linecap="round"/></svg>'
      /* poser une photo : l'appareil, dessiné, jamais un glyphe emprunté */
      : '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        +'<rect x="3" y="6.5" width="18" height="13" rx="3" stroke="currentColor" stroke-width="2"/>'
        +'<path d="M8.5 6.5 L10 4h4l1.5 2.5" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
        +'<circle cx="12" cy="13" r="3.2" stroke="currentColor" stroke-width="2"/></svg>';
    b.style.setProperty('color', '#F7F0DE', 'important');
    try{ var dev=document.getElementById('device');
      if(dev && dev.classList.contains('light') && !aPhoto)
        b.style.setProperty('color', '#201908', 'important'); }catch(_){}
    /* la cote : l'onde au droit du bouton (x = 366 − 17 = 349), moins l'écart. */
    var y=O.onde(base,amp);
    b.style.setProperty('top', Math.round(y(349) - ECART) + 'px', 'important');
    b.style.setProperty('left', (W - 24 - 34) + 'px', 'important');
    b.style.setProperty('right', 'auto', 'important');
  }
  window._photoBouton=poseBouton;

  /* ═══ Q53 · LA PHOTO DANS UNE LISTE ═══
     « La photo remplace la matière de la promesse PARTOUT où cette matière s'affiche —
     même cadrage centré, mêmes cotes que la dalle. Sinon la promesse aurait deux visages. »
     (Décision Tom, 18 août 2026.) Rend `true` si une photo a été posée dans la boîte. */
  window._photoDansBoite=function(g, boite, id){
    try{
      if(id===null||id===undefined||!boite) return false;
      var q=(typeof promises!=='undefined')?promises.filter(function(x){return x.id===id;})[0]:null;
      var src=laPhoto(q); if(!src) return false;
      var im=image(src, function(){ try{ if(window.buildIndex)buildIndex();
                                         if(window.buildFeed)buildFeed(); }catch(_){} });
      if(!im) return false;
      var r=im.width/im.height, br=boite.w/boite.h, sw,sh,sx,sy;
      if(r>br){ sh=im.height; sw=im.height*br; sx=(im.width-sw)/2; sy=0; }
      else    { sw=im.width;  sh=im.width/br;  sx=0; sy=(im.height-sh)/2; }
      g.save(); g.globalAlpha=1; g.globalCompositeOperation='source-over';
      g.drawImage(im, sx,sy,sw,sh, boite.x,boite.y,boite.w,boite.h);
      g.restore();
      return true;
    }catch(_){ return false; }
  };
  window._photoRange=function(hote){ try{ var n=(hote||document).querySelector('.ph-photo-nid');
    if(n) n.style.setProperty('display','none','important'); }catch(_){} };

  /* ═══ LA FICHE ═══ */
  var _tOrig=window._ficheTrait;
  if(typeof _tOrig==='function'){
    window._ficheTrait=function(){
      var r=_tOrig.apply(this,arguments);
      try{
        var dp=document.getElementById('detailPoster');
        if(!dp||!dp.classList.contains('show')) return r;
        if(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) return r;
        /* ⚠ PAS DE BOUTON PENDANT L'INSTANT. Les cadres 96 à 101 n'en portent aucun : le
           moment où la parole se referme ne se règle pas, il se regarde. Sans cette porte,
           le bouton s'y posait et la section 5 tombait à 4 écarts. */
        if(window._instant){ window._photoRange(dp); return r; }
        var p=(typeof cur!=='undefined')?cur:null; if(!p) return r;
        var e=window._ficheEcran(dp,p);
        var cv=document.getElementById('dpTrameCv'); if(!cv) return r;
        var g=cv.getContext('2d'); if(!g) return r;
        /* on se remet dans le repère de l'écran, comme `_ficheTrait` l'a laissé */
        var posterW=dp.clientWidth||W, sc=posterW/W;
        var dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
        g.setTransform(dpr*sc,0,0,dpr*sc,0,0);
        window._photoPeint(g, e, p, e.base, e.amp, e.boite);
        poseBouton(dp, p, e.base, e.amp, function(){
          try{ if(window._ficheTrait)_ficheTrait(); if(window._ficheCotes)_ficheCotes(); }catch(_){} });
      }catch(_){}
      return r;
    };
  }

  /* ═══ LA PAGE + ═══ */
  var _pOrig=window._ppTrait;
  if(typeof _pOrig==='function'){
    window._ppTrait=function(){
      var r=_pOrig.apply(this,arguments);
      try{
        var cs=document.getElementById('createSheet');
        if(!cs||!cs.classList.contains('show')) return r;
        var e=window._ppEcran?window._ppEcran():null; if(!e) return r;
        /* sur la page +, la promesse n'existe pas encore : la photo se pose sur le
           brouillon de phrase, et suivra la promesse à la plantation. */
        var p=(window._phrase=window._phrase||{});
        var cv=document.getElementById('csTrameCv'); if(!cv) return r;
        var g=cv.getContext('2d'); if(!g) return r;
        var shW=cs.clientWidth||W, sc=shW/W;
        var dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
        g.setTransform(dpr*sc,0,0,dpr*sc,0,0);
        /* ⚠ PAS DE BOUTON PHOTO SUR UN GARDÉ DE CÔTÉ. Les cadres 26/27 n'en portent pas, et
           il n'a nulle part où se poser : sans aplat (Q83), le rond perd son fond et sort en
           cercle vide — vu au duo, thème clair. Rien n'est promis, il n'y a pas encore de
           matière à remplacer. */
        if(e.garde){ window._photoRange(cs); return r; }
        window._photoPeint(g, e, p, e.base, e.amp, e.boite);
        poseBouton(cs, p, e.base, e.amp, function(){
          try{ if(window._ppTout)_ppTout(); else if(window._ppTrait)_ppTrait(); }catch(_){} });
      }catch(_){}
      return r;
    };
  }

  var _toutOrig=window._ppTout;
  if(typeof _toutOrig==='function'){
    window._ppTout=function(){ var r=_toutOrig.apply(this,arguments);
      try{ if(window._ppTrait) _ppTrait(); }catch(_){}
      return r; };
    try{ _ppTout=window._ppTout; }catch(_){}
  }
  /* et à l'ouverture de la page +, le trait est peint par l'app avant que nos crochets
     n'aient servi : on repasse une fois, à la main. */
  document.addEventListener('click',function(e){
    if(e.target.closest && (e.target.closest('#createBtn') || e.target.closest('#createSheet .tile'))){
      [120,420,900].forEach(function(ms){ setTimeout(function(){
        try{ if(window._ppTrait) _ppTrait(); }catch(_){} }, ms); });
    }
  },true);

  /* LA PHOTO SUIT LA PROMESSE À LA PLANTATION : ce qu'on a posé sur la page + devient la
     matière du Promi planté. Sans ça, la photo se perdrait au moment du geste. */
  var _add=window.addPromise || null;
  document.addEventListener('click',function(){
    try{
      var ph=(window._phrase||{}).photo; if(!ph) return;
      var derniers=(typeof promises!=='undefined')?promises:[];
      var d=derniers[derniers.length-1];
      if(d && !d.photo && !d.req){ d.photo=ph; }
    }catch(_){}
  },true);
})();
