
/* ═══ LE BLOC DU CERCLE D'UNE NUÉE (Tom, 13 sept. 2026 : « donne-lui son bloc du Cercle, avec la rangée LA COULEUR comme les
   deux autres natures ») ═══
   La brique MÊME de la fiche (`_s2Briques.cercle`), cinq rangées, 384, encart à 147. Le Peaufiner d'une Nuée est en cotes
   absolues sur deux pages de 760 : le bloc se pose en PAGE 2, sous « Planter dans la Nuée » (46 + 68 + 16 = 130), et
   DISSOUDRE LA NUÉE passe dessous avec l'écart de la fiche entre le bloc et SUPPRIMER (104) : 130 + 384 + 104 = 618.
   ⚠ Cela DÉCALE DISSOUDRE du cadre 86 (124 → 618 en page 2) : ajout demandé, pas une dérive — même règle que LE TRAIT.
   Au Cercle payé, LA COULEUR ouverte grandit : DISSOUDRE se place sous la hauteur RENDUE du bloc. Ce n'est pas la boucle du §8
   (une cote mesurée sur elle-même) : DISSOUDRE ne change rien à la hauteur du bloc. Fermé, le bloc vaut 384 par sa règle. */
(function(){
  var PAGE=760, TOP=PAGE+130, ECART=104, BLOC=384;
  function P(e,k,v){ if(!e) return; if(e.style.getPropertyValue(k)===v && e.style.getPropertyPriority(k)==='important') return;
    e.style.setProperty(k,v,'important'); var l=(e.getAttribute('data-pose')||'').split(' ').filter(Boolean);
    if(l.indexOf(k)<0){ l.push(k); e.setAttribute('data-pose', l.join(' ')); } }
  function range(){ var b=document.getElementById('npCercle'); if(b && b.parentNode) b.parentNode.removeChild(b); }
  (window._rangeurs = window._rangeurs || []).push(range);
  function pose(ok){
    var dp=document.getElementById('detailPoster'), corps=document.getElementById('dpdCorps');
    var nuee=!!(dp && dp.classList.contains('show') && (dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')));
    var bloc=document.getElementById('npCercle');
    if(!ok || !nuee || !corps){ if(bloc) P(bloc,'display','none'); if(!nuee) range(); return; }
    if(!bloc || bloc.parentNode!==corps){ if(bloc) range();
      if(!window._s2Briques || !window._s2Briques.cercle) return;
      bloc=window._s2Briques.cercle(); bloc.id='npCercle'; corps.appendChild(bloc);
      try{ if(window._cerclePaye) window._cerclePaye(); }catch(_){} }
    P(bloc,'visibility','visible'); P(bloc,'display','block'); P(bloc,'position','absolute'); P(bloc,'left','24px'); P(bloc,'top',TOP+'px');
    [].forEach.call(bloc.querySelectorAll('.s2-reg,.s2-encart,.s2-lab,.s2-val,.s2-ctl,.s2-ctl *'), function(x){ P(x,'visibility','visible'); });
    var paye=document.getElementById('device').classList.contains('premium');
    var ouv=bloc.querySelector('.s2-couleur.s2-ouv');
    var ech=(bloc.getBoundingClientRect().height/(bloc.offsetHeight||1))||1;
    var h=(paye && ouv) ? Math.max(BLOC, bloc.offsetHeight) : BLOC;
    var diss=document.getElementById('npDiss'); if(diss) P(diss,'top',(TOP+h+ECART)+'px');
    var pied=document.getElementById('npPied'); if(pied){ var hp=parseFloat(pied.style.getPropertyValue('height'))||2*PAGE;
      var besoin=TOP+h+ECART+64+56; if(hp<besoin) P(pied,'height',besoin+'px'); }
  }
  function brancher(){ var f=window._nueePeaufiner; if(typeof f!=='function' || f._cercle) return typeof f==='function';
    var g=function(){ var r=f.apply(this, arguments); try{ pose(r===true); }catch(_){} return r; };
    g._cercle=true; window._nueePeaufiner=g; return true; }
  if(!brancher()){ var k=setInterval(function(){ if(brancher()) clearInterval(k); }, 200); }
  /* LA COULEUR s'ouvre au doigt : la page se recale aussitôt */
  document.addEventListener('click', function(ev){ if(ev.target.closest && ev.target.closest('#npCercle')) setTimeout(function(){ try{ window._nueePeaufiner(); }catch(_){} }, 0); }, true);   /* en capture : la rangée arrête le clic */
})();
