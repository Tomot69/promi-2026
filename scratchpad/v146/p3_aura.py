# -*- coding: utf-8 -*-
import io
P = 'app.html'; S = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global S
    assert S.count(old) == n, (S.count(old), old[:100])
    S = S.replace(old, new)

# a · prepare() : quand tout est déjà prêt, les quatre étapes passent d'un trait, dans le geste
rep("""    var E=[function(){ atlas(); }, function(){ semis(); }, function(){ iles(); },
           function(){ PEL.pret=true; tourSiNeuf(); publie(); }];
    var i=0;
    (function suite(){""",
"""    var E=[function(){ atlas(); }, function(){ semis(); }, function(){ iles(); },
           function(){ PEL.pret=true; tourSiNeuf(); publie(); }];
    /* ⚑ v146 (C-135) — TOUT EST DÉJÀ PRÊT (la Pelote a été préparée au repos, `prechauffe`) : l'atlas, le semis et les îles sortent de
       leur mémoire, les quatre étapes passent D'UN TRAIT, dans le geste d'ouverture. Sinon (une ouverture avant que le repos ait pu
       préparer) : une étape par tâche, comme avant. */
    if(chaud()){ for(var q=0;q<E.length;q++){ try{ E[q](); }catch(e){ window._auraErreur=String(e&&e.stack||e); } } return; }
    var i=0;
    (function suite(){""")

# b · ouvre()
rep("""  function ouvre(){
    PEL.souffleT=-SOUFFLE.DEPART;           /* v117 : le souffle repart, 0,6 s après l'affichage */
    try{ nouveauSol(); }catch(_){}          /* ⚑ un ton neuf à chaque ouverture (Tom) */""",
"""  /* ⚑ v146 (C-135, Tom : « Quand on ouvre l'Aura, la place reste vide une à deux secondes avant que la Pelote paraisse. C'est un bug : il faut
     qu'elle soit là dès l'ouverture. ») — LA PELOTE EST PRÊTE AVANT QU'ON L'OUVRE, ET SA PREMIÈRE IMAGE EST PEINTE DANS LE GESTE.
     *Mesuré avant* (banc WebKit, 25 paroles dont 6 tenues) : première ouverture, première image 1,95 à 2,33 s après le toucher — le semis des
     poils (243 ms), l'atlas (188), les îles (459), le contexte graphique, ses shaders et l'envoi des poils (388 à 435), chacun dans SA tâche,
     derrière la liste « Ce que tu as tenu » (306) ; réouvertures : 0,80 à 0,93 s — « un ton neuf à chaque ouverture » refaisait les îles
     (104 à 291 ms) et l'état de chaque poil (237 à 395 ms) APRÈS le toucher.
     *La parade* : ① au repos (aucun toucher depuis 1,8 s, rien qui bouge, l'Aura fermée), `prechauffe` tire le ton de la PROCHAINE ouverture et
     prépare tout, une étape par tâche : atlas, semis, dalles des îles (une par tâche), îles, puis une image peinte dans le canevas fermé (le
     contexte graphique, les shaders et les poils sont alors sur la carte) ; ② à l'ouverture, plus rien n'est tiré ni calculé : `prepare` passe
     d'un trait et la première image est peinte DANS le geste ; ③ à la fermeture, après un changement de palette, de thème ou de paroles, ou
     quand le navigateur reprend le contexte graphique (le Studio), tout se re-prépare au repos suivant. Juge : redteam_aura_latence.py. */
  var PRE={sol:false, pret:false, enCours:false, tOuv:-1e9, tTouche:0, tGeste:0, ms:{}, n:0, latence:null, chaude:null};
  function chaud(){ try{ if(!ATL || !SEMC[PALIERS[PEL.palier]] || !PEL.iles || !D) return false;
      var F=fondSphere(); return PEL.cleI===(D.T.map(cleMonde).join(',')+'|'+[F[0]|0,F[1]|0,F[2]|0].join(',')); }catch(_){ return false; } }
  function peintUne(){ var _o=opts(); if(window._peloteMod){ try{ window._peloteMod(_o); }catch(_){} }
    if(!(M.peintGL && M.peintGL(CV, _o))) M.peint(CV, _o); PEL.peints=(PEL.peints||0)+1; }
  function calme(){
    try{ if(document.hidden || actif()) return false;
      var n=performance.now();
      if(n-PRE.tTouche<1800) return false;
      if(window._evol && window._evol()) return false;
      if(window._tenirAnime || window._tirageActive) return false;
      if(window._tEcran && n-window._tEcran<1200) return false;
      if(window._tMouv && n-window._tMouv<900) return false;
      var ob=document.getElementById('promiOnb'); if(ob && !ob.classList.contains('gone') && ob.offsetWidth>0) return false;   /* l'onboarding joue : on attend */
      if(document.getElementById('guide')) return false;
      return true; }catch(_){ return false; }
  }
  function prechauffe(){
    if(PRE.enCours || PRE.pret) return;
    PRE.enCours=true; PRE.ms={}; var dal=null, k=0, t0=performance.now();
    function chrono(nom, f){ var a=performance.now(); try{ f(); }catch(e){ window._auraErreur=String(e&&e.stack||e); } PRE.ms[nom]=Math.round(((PRE.ms[nom]||0)+performance.now()-a)*10)/10; }
    var E=[
      function(){ chrono('ton', function(){ if(!CAD) squelette(); if(!PRE.sol){ nouveauSol(); PRE.sol=true; } D=donnees(); }); },
      function(){ chrono('atlas', function(){ atlas(); }); },
      function(){ chrono('semis', function(){ applique(); semis(); }); },
      function(){ /* les dalles des îles, UNE par tâche (un rendu de dalle : 30 à 80 ms) — `iles` les retrouvera en mémoire */
        if(!dal) dal=(D&&D.T)?D.T.slice():[];
        if(k<dal.length){ var p=dal[k++]; chrono('dalles', function(){ dalleLisible(p); }); return true; } },
      function(){ chrono('iles', function(){ iles(); }); },
      function(){ chrono('carte', function(){ peintUne(); }); PRE.pret=true; PRE.n++; PRE.ms.total=Math.round(performance.now()-t0); }
    ], i=0;
    (function suite(){
      if(PRE.pret){ PRE.enCours=false; return; }
      /* on s'efface devant le doigt et devant tout ce qui bouge : la suite reprendra au repos suivant, là où elle s'est arrêtée */
      if(!calme()){ PRE.enCours=false; planifie(700); return; }
      var encore=false; try{ encore=!!E[i](); }catch(_){}
      if(!encore) i++;
      if(i<E.length) setTimeout(function(){ requestAnimationFrame(function(){ setTimeout(suite, 0); }); }, 0);   /* une image passe entre deux étapes */
      else PRE.enCours=false;
    })();
  }
  var _preT=0;
  function planifie(ms){ clearTimeout(_preT); _preT=setTimeout(function(){ if(PRE.pret || PRE.enCours) return; if(calme()) prechauffe(); else planifie(600); }, ms==null?900:ms); }
  function preInvalide(ton){ PRE.pret=false; if(ton) PRE.sol=false; planifie(1200); }
  try{ window._auraPreInvalide=function(){ preInvalide(false); }; }catch(_){}
  try{ ['touchstart','pointerdown','keydown','wheel'].forEach(function(t){ document.addEventListener(t, function(){ PRE.tTouche=performance.now(); }, {capture:true, passive:true}); }); }catch(_){}
  try{ var _sbG=document.getElementById('souffleBtn'); if(_sbG) ['touchstart','pointerdown'].forEach(function(t){ _sbG.addEventListener(t, function(){ if(!actif() && performance.now()-PRE.tGeste>400){ PRE.tGeste=performance.now(); PRE.latence=null; PRE.chaude=PRE.pret; } }, {capture:true, passive:true}); }); }catch(_){}
  function ouvre(){
    /* une ouverture passe DEUX fois ici (la classe `show`, puis la porte) : la seconde, dans la demi-seconde, n'a plus rien à faire */
    if(PEL.pret && performance.now()-PRE.tOuv<600) return;
    PRE.tOuv=performance.now();
    PEL.souffleT=-SOUFFLE.DEPART;           /* v117 : le souffle repart, 0,6 s après l'affichage */
    /* ⚑ un ton neuf à chaque ouverture (Tom) — v146 : il a pu être tiré D'AVANCE, au repos ; on ne le retire pas */
    if(PRE.sol){ PRE.sol=false; } else { try{ nouveauSol(); }catch(_){} }
    PRE.pret=false;""")
rep("""    try{ squelette(); remplit(); prepare(); }catch(e){ window._auraErreur=String(e&&e.stack||e); }
    if(!RAF){ TP=0; RAF=requestAnimationFrame(boucle); }
  }""",
"""    try{ squelette(); remplit(); prepare(); }catch(e){ window._auraErreur=String(e&&e.stack||e); }
    /* v146 (C-135) : prête → la première image est peinte ICI, dans le geste ; l'écran qui s'ouvre la porte déjà */
    if(PEL.pret){ try{ peintUne(); PRE.dansGeste=true; }catch(e){ window._auraErreur=String(e&&e.stack||e); } } else PRE.dansGeste=false;
    if(!RAF){ TP=0; RAF=requestAnimationFrame(boucle); }
  }""")

# c · la latence, lue à la première image (pour le juge et pour ?mesure=1)
rep("""    PEL.dernier=ms; PEL.peints=(PEL.peints||0)+1;
    if(PEL.peints%30===0) place();""",
"""    PEL.dernier=ms; PEL.peints=(PEL.peints||0)+1;
    if(PRE.latence===null && PRE.tGeste){ PRE.latence=Math.round(performance.now()-PRE.tGeste);
      try{ if(window._mesureNote) window._mesureNote('Aura : Pelote à '+PRE.latence+' ms'+(PRE.dansGeste?' (peinte dans le geste)':'')+' · préparée d’avance : '+(PRE.chaude?'oui':'non')+(PRE.ms.total?' ('+PRE.ms.total+' ms au repos)':''),
          {quoi:'aura', latence:PRE.latence, dansGeste:!!PRE.dansGeste, preparee:!!PRE.chaude, etapes:PRE.ms, palier:PALIERS[PEL.palier], carte:!!(M.glDispo&&M.glDispo())}); }catch(_){} }
    if(PEL.peints%30===0) place();""")

# d · les crochets : fermeture, palette, thème, paroles, contexte graphique
rep("""      var s=SC.classList.contains('show'); if(s===_vu) return; _vu=s; if(s) ouvre();
    }).observe(SC, {attributes:true, attributeFilter:['class']}); }catch(e){}
  squelette();
  if(_vu) ouvre();""",
"""      var s=SC.classList.contains('show'); if(s===_vu) return; _vu=s; if(s) ouvre(); else preInvalide(true);   /* v146 : fermée → la prochaine se prépare (un ton neuf) */
    }).observe(SC, {attributes:true, attributeFilter:['class']}); }catch(e){}
  squelette();
  if(_vu) ouvre(); else planifie(2200);   /* v146 (C-135) : après le démarrage, au premier repos */
  try{ document.addEventListener('visibilitychange', function(){ if(!document.hidden) planifie(1500); }); }catch(_){}
  try{ if(window._paroles && window._paroles.abonne) window._paroles.abonne(function(){ if(!actif()) preInvalide(false); }); }catch(_){}""")
rep("""        var c=_dv.classList.contains('light'); if(c===_cl) return;   /* on compare avant d'agir (§8) */
        _cl=c; reteint();""",
"""        var c=_dv.classList.contains('light'); if(c===_cl) return;   /* on compare avant d'agir (§8) */
        _cl=c; reteint(); if(!actif()) preInvalide(true);""")
rep("""  cv.addEventListener('webglcontextlost', function(e){ try{ e.preventDefault(); }catch(_){} _GL=null; }, false);""",
"""  cv.addEventListener('webglcontextlost', function(e){ try{ e.preventDefault(); }catch(_){} _GL=null; try{ if(window._auraPreInvalide) window._auraPreInvalide(); }catch(_){} /* v146 (C-135) : le contexte repris (le Studio) → la Pelote se re-prépare au repos */ }, false);""")

# e · l'état, pour le juge
rep("""    nouveauSol:nouveauSol,
    /* ⚑ LE PARTAGE DEMANDE LA PELOTE.""",
"""    nouveauSol:nouveauSol,
    /* v146 (C-135) — pour le juge et pour ?mesure=1 : où en est la préparation au repos, et la dernière latence lue */
    pre:function(){ return {pret:PRE.pret, enCours:PRE.enCours, sol:PRE.sol, n:PRE.n, ms:PRE.ms, latence:PRE.latence, dansGeste:!!PRE.dansGeste, chaude:PRE.chaude, calme:calme(), chaud:chaud()}; },
    prechauffe:function(){ planifie(0); },
    /* ⚑ LE PARTAGE DEMANDE LA PELOTE.""")

# f · ?mesure=1 : une note envoyée au Mac
rep("""    window._mesureImages=mesure;
  }""",
"""    window._mesureImages=mesure;
    /* v146 (C-135) : une mesure qui n'est pas un compte d'images (la latence de la Pelote) — affichée sur la marque et envoyée au Mac */
    window._mesureNote=function(texte, R){ try{ derniere=texte; pose2(); R=R||{}; R.version=V.marque(); R.etat=etatLu(); R.ua=navigator.userAgent; R.quand=new Date().toISOString();
        fetch('mesure', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(R), keepalive:true}).catch(function(){}); }catch(_){ } };
  }""")
io.open(P, 'w', encoding='utf-8').write(S)
print('ok')
