
/* ═══════════════════════════════════════════════════════════════════════════════════════
   SECTION 5 · LE MOTEUR DE L'INSTANT.
   Trois écrans, une seule fiche. Les cotes sont celles du §5 ; le trait est relevé dans les
   chemins du moodboard (cadres 96, 98, 100) :

     · l'autre moitié arrive   champ NATURE · orange plein 0 → 195 + chevron ·
                               MENTHE plein 195 → 268 (l'autre trace) · points orange dès 213
     · le trait se referme     champ MENTHE PLEIN · trait ENCRE plein 0 → 390
     · juste après             champ NATURE · trait MENTHE plein 0 → 390

   base = 300, amplitude = 44, boîte SVG = 384 — les trois cadres, sans exception.
   L'onde vient de `window._onde` : une seule formule d'onde existe dans le produit.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  if(!window._onde || !window._ficheTrait) return;
  var O=window._onde, W=390;
  var CREME='#F7F0DE', ENCRE='#201908', MENTHE='#8FE08F', TERRA='#DD4D23';

  window._instant = null;        /* null · 'arrive' · 'referme' · 'apres' */
  window._instantX = 268;        /* où en est l'autre moitié (cadre 96 : 268) */

  /* ── LES TROIS ÉCRANS (§5) — les cotes se lisent, elles ne se déduisent pas. ── */
  function inv(nom, nat){
    var natCol=O.NATCOL[nat]||O.NATCOL.promi;
    /* ⚑ v29 (Tom, Q310) : « L'amande ne s'applique qu'au fond sombre — sur fond clair le tenu reste #00341A, la règle
       du 23 septembre prime sur v18. » Les TEXTES de l'instant sont posés sur le corps : clair en mode clair. */
    var _clair=!!(document.getElementById('device')&&document.getElementById('device').classList.contains('light'));
    var TXT=_clair?'#00341A':MENTHE;
    if(nom==='arrive') return {
      nat:nat, base:300, amp:36, boite:384, champ:natCol, encreHaut:CREME,
      dalle:{x:105,y:91,w:180,h:150},
      trait:{mode:'arrive', col:TERRA},
      trace:{y:388, mot:'l’autre part arrive', col:TXT},
      aura:{y:432, y2:442}, qui:{y:559, col:TERRA}, titre:{y:590}, quand:null};   /* ⚑ v102 : +2 · +3 — l'encre agrandie (v96) des noms des Noyaux et de l'à-qui mangeait l'air du cadre 96 */
    if(nom==='referme') return {
      nat:nat, base:300, amp:36, boite:384, champ:MENTHE, encreHaut:ENCRE,
      dalle:{x:81,y:88,w:228,h:190},
      trait:{mode:'complet', col:ENCRE},
      trace:null, aura:null, qui:null, titre:null, quand:null};
    return {                                              /* juste après (cadre 100) */
      nat:nat, base:300, amp:36, boite:384, champ:natCol, encreHaut:CREME,
      dalle:{x:105,y:91,w:180,h:150},
      trait:{mode:'complet', col:MENTHE},
      trace:null, aura:{y:388, y2:398}, qui:{y:515, col:TXT}, titre:{y:546},
      quand:{y:614, col:TXT}};   /* ⚑ v102 : +2 · +3 · +6 — mêmes airs à l'encre que le cadre 100 avant l'agrandissement (v96) */
  }

  function nature(dp){
    return dp.classList.contains('dp-chiche')?'chiche'
      :((dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'))?'nuee':'promi');
  }
  function armable(){
    var dp=document.getElementById('detailPoster');
    if(!dp||!dp.classList.contains('show')) return null;
    if(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) return null;
    if(!window._instant) return null;
    return dp;
  }

  /* ═══ LE TRAIT DE L'INSTANT ═══ */
  function trait(dp, E, p){
    var cv=document.getElementById('dpTrameCv'); if(!cv) return;
    var y=O.onde(E.base,E.amp), H=E.boite;
    var posterW=dp.clientWidth||W, sc=posterW/W, dpr=Math.max(2,Math.min(3,window.devicePixelRatio||2));
    cv.width=Math.round(posterW*dpr); cv.height=Math.round(H*sc*dpr);
    cv.style.width=posterW+'px';
    cv.style.setProperty('height',(H*sc)+'px','important');
    cv.style.setProperty('opacity','1','important');  cv.style.setProperty('filter','none','important');
    cv.style.setProperty('mix-blend-mode','normal','important');
    cv.style.setProperty('-webkit-mask','none','important'); cv.style.setProperty('mask','none','important');
    cv.style.setProperty('position','absolute','important');
    cv.style.setProperty('top','0','important'); cv.style.setProperty('left','0','important');
    cv.style.setProperty('background','transparent','important');
    var g=cv.getContext('2d'); if(!g) return;
    g.setTransform(dpr*sc,0,0,dpr*sc,0,0); g.clearRect(0,0,W,H);
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';

    /* 1 · L'APLAT. Sur « le trait se referme » il est MENTHE, et c'est la seule exception
         du produit : l'état prend toute la place, une seconde. */
    g.beginPath(); O.chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath();
    g.fillStyle=E.champ; g.fill();

    /* 2 · LA DALLE — la vraie, celle du moteur (§4.1), non teintée, opacité 1. Elle se
         recompose PLUS GRANDE à l'instant où la parole est tenue : 228 × 190 au lieu de
         180 × 150 (cadres 98 contre 96 et 100). */
    if(p && window.Toile && Toile.dalleTrame){
      try{ if(Toile.dalleAbs && Toile.dalleAbs(p.id)){
        /* ⚠ L'INSTANT NE REMPLIT PAS SON CHAMP — et c'est voulu. La décision du 19 août
           (« la matière remplit tout le champ ») nomme les fiches, la page + et la Nuée.
           L'instant est la SEULE exception du produit, celle où LA COULEUR DU CHAMP est le
           sujet : « le champ entier passe au menthe une seconde, la dalle se recompose plus
           grande, le mot tombe » (§6 du moodboard). Essayé et mesuré : en couverture, la
           matière recouvre jusqu'au pourtour du cadre et LE MENTHE DISPARAÎT — le juge de la
           section 5 l'a relevé, deux thèmes, rgb(192,182,244) au lieu du menthe. La dalle
           garde donc ses trois boîtes d'inventaire, et c'est leur rapport (228 contre 180)
           qui porte la recomposition. Voir QUESTIONS.md · Q58. */
        /* ⚠ ET ELLE EST TEINTÉE, comme toute dalle de BANDE HAUTE (Q30, décision Tom du
           18 août). L'instant peignait la sienne telle que le moteur la rend — or ce moteur
           tire sa couleur au hasard (`cc()`) : mesuré, le même id sort tantôt lavande
           [209,176,255], tantôt [57,84,255], c'est-à-dire LE BLEU DU CHAMP. Une passe sur
           deux, la dalle de l'instant disparaissait, et `releve-S5` le relevait en toutes
           lettres : « le centre a exactement la couleur du champ ». Même appel que la fiche
           et la page + — un seul site de teinture dans le produit. La forme ne bouge pas. */
        /* ⚑ v29 — la teinture de Q30 peinte PAR LE MOTEUR, la dalle rendue à la taille de sa boîte, posée 1:1 */
        var b=E.dalle;
        window._poseDalle(g, p.id, b.x, b.y, b.w, b.h, (E.nat&&window._ppRampe)?{rampe:window._ppRampe(E.nat)}:undefined);
      } }catch(_){}
    }

    /* 3 · LA LIGNE (§2.6). */
    var ep=10, rr=4.5, esp=18, mid=W/2;
    g.lineWidth=ep; g.lineCap='round'; g.lineJoin='round';
    /* ⚑ LE PINCEAU SUR LA FICHE — la matière remplace le plein, jamais la COURBE.
       Le trait de `p` est celui qu'on lui a donné, à la page + ou dans Peaufiner : jamais
       un réglage global (Q128). Les douze tracés de la planche sont posés sur l'onde du
       §2.1 ; `_matiereTrait` reporte leur ligne moyenne sur CELLE-CI et découpe à la même
       abscisse. « Plein » est le trait d'aujourd'hui, mot pour mot. */
    function plein(col,a,b){
      var m = null;
      try{ m = window.promiPinceau ? window.promiPinceau(p) : 'Plein'; }catch(_){ m='Plein'; }
      if(m && m !== 'Plein' && window._matiereTrait &&
         window._matiereTrait(g, m, E.base, E.amp, a, b, col)) return;
      g.strokeStyle=col; g.beginPath(); O.chemin(g,y,a,b); g.stroke(); }
    if(E.trait.mode==='complet'){ plein(E.trait.col,0,W); }
    else {
      /* ma moitié est donnée : plein 0 → 195, le milieu exact (§2.6). */
      plein(E.trait.col,0,mid);
      O.chevron(g,y,mid,E.trait.col,ep);
      /* les points disent ce qui manque — ils restent de MA couleur (cadre 96). */
      g.fillStyle=E.trait.col;
      for(var x=mid+esp;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x),rr,0,6.2832); g.fill(); }
      /* et par-dessus, la moitié de l'autre, en menthe, jusqu'où elle est arrivée. */
      var xa=window._instantX;
      if(typeof xa==='number' && xa>mid) plein(MENTHE, mid, Math.min(W,xa));
    }
    /* ⚑ ET CE PEINTRE-CI DÉCLARE AUSSI — c'est LUI qui tient le canevas pendant l'instant.
       Deux peintres pour un même canevas : sans cette ligne, la déclaration de
       `_ficheTrait` restait affichée alors que l'instant avait tout repeint. Le motif du
       jour, une cinquième fois. */
    try{ var _c=document.getElementById('dpTrameCv');
      if(_c) _c.setAttribute('data-trait', [E.base, E.amp, E.trait.col, E.trait.mode].join(',')); }catch(_){}
  }

  /* ═══ LES COTES DE L'INSTANT ═══ */
  /* Marque ce qu'il pose — même règle que le Peaufiner d'une Nuée, voir `lot-RIEN-NE-SURVIT`. */
  function pose(el,css){ if(!el) return;
    var v = (el.getAttribute('data-pose')||'').split(' ').filter(Boolean);
    for(var k in css){ el.style.setProperty(k,css[k],'important');
      if(v.indexOf(k) < 0) v.push(k); }
    el.setAttribute('data-pose', v.join(' ')); }
  /* ⚑ ON MARQUE CE QU'ON MASQUE (CLAUDE.md §8). Un `display:none` posé en ligne par un
     écran survit à tous les suivants : `closeAll` ne sait pas le défaire, et une règle de
     feuille ne peut pas le battre. Marqué, il se rend — voir `_rendMasques`. */
  function cache(el){ if(!el) return; pose(el,{display:'none'}); el.setAttribute('data-masque','1'); }

  function cotes(dp, E, p){
    var nom=window._instant;
    /* ⚠ L'ENCRE DU CORPS N'EST PAS CELLE DU CHAMP. Sur le champ plein, le mot-marque et
       ✕ FERMER restent crème (encre sur le champ menthe du cadre 99). Dans le CORPS, qui
       est crème en thème clair, le titre et les deux mots de l'instant passent à l'ENCRE
       — sans quoi ils se peignent dans la couleur du fond. Constaté au duo : le titre
       « faire les crêpes » avait disparu du cadre 101 clair. */
    var dev=document.getElementById('device');
    var clair=!!(dev&&dev.classList.contains('light'));
    var encreCorps = clair ? ENCRE : CREME;
    dp.classList.toggle('inst-arrive', nom==='arrive');
    dp.classList.toggle('inst-referme', nom==='referme');
    dp.classList.toggle('inst-apres', nom==='apres');

    /* l'entête (§3.1) : le mot-marque et ✕ FERMER passent à l'encre sur le champ menthe. */
    var mm=document.getElementById('dptNat'), cb=dp.querySelector('.closeb');
    pose(mm,{color:E.encreHaut,'-webkit-text-fill-color':E.encreHaut});
    if(cb){ pose(cb,{color:E.encreHaut,'-webkit-text-fill-color':E.encreHaut});
      [].forEach.call(cb.querySelectorAll('*'),function(x){
        pose(x,{color:E.encreHaut,'-webkit-text-fill-color':E.encreHaut}); }); }

    /* les deux mots du cadre 98. Ils viennent du moodboard ; le prénom vient du Promi. */
    var t1=document.getElementById('instTenue'), t2=document.getElementById('instSous');
    if(!t1){ t1=document.createElement('div'); t1.id='instTenue'; dp.appendChild(t1); }
    if(!t2){ t2=document.createElement('div'); t2.id='instSous'; dp.appendChild(t2); }
    if(nom==='referme'){
      var qui=(p&&((p.from&&p.from!=='moi')?p.from:((p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:''))) || '';
      pose(t1,{color:encreCorps,'-webkit-text-fill-color':encreCorps});
      pose(t2,{color:encreCorps,'-webkit-text-fill-color':encreCorps});
      t1.textContent='tenue.';
      t2.textContent = qui ? (qui+' vient de tracer sa moitié. Le dessin existe.')
                           : 'Le dessin existe.';
    }

    /* le mot de l'instant (cadre 96) */
    var tr=document.getElementById('dptTrace');
    if(E.trace){ pose(tr,{display:'block', top:E.trace.y+'px', left:'24px', width:'342px',
                          color:E.trace.col, '-webkit-text-fill-color':E.trace.col}); 
      if(tr) tr.textContent=E.trace.mot; }
    else cache(tr);

    /* les Noyaux (§2.9) : le tien Ø78, une personne Ø58, 10 px plus bas. */
    var au=document.getElementById('dAura');
    if(E.aura) pose(au,{display:'block', position:'absolute', left:'24px', top:E.aura.y+'px',
                        width:'342px', height:'auto', margin:'0', padding:'0', background:'none'});
    else cache(au);

    var qi=document.getElementById('dptQui'), ti=document.getElementById('dptTitre'),
        qd=document.getElementById('dptQuand');
    if(E.qui) pose(qi,{display:'block', top:E.qui.y+'px', 'font-size':'21px',
                       color:E.qui.col, '-webkit-text-fill-color':E.qui.col});
    else cache(qi);
    if(E.titre) pose(ti,{display:'block', top:E.titre.y+'px', 'font-size':'38px',
                         color:encreCorps, '-webkit-text-fill-color':encreCorps});
    else cache(ti);
    if(E.quand){ pose(qd,{display:'block', top:E.quand.y+'px',
                          color:E.quand.col, '-webkit-text-fill-color':E.quand.col});
      /* « TENUE À DEUX · À L'INSTANT » — les mots du cadre 101.
         ⚠ MAIS « À DEUX » NE SE DIT QUE S'ILS SONT DEUX. Vu à l'œil sur le passage d'usage :
         un Promi « à moi », un seul Noyau à l'écran, et la ligne annonçait « TENUE À DEUX ».
         Le cadre 101 montre une parole tenue AVEC QUELQU'UN — c'est son cas, pas une
         formule. Quand la promesse est à soi, on écrit le mot que l'app emploie déjà pour
         cet état (`STLAB.tenu`), rien de plus : aucun mot n'est inventé, on retire celui
         qui ne s'applique pas. */
      if(qd){
        var aDeux = !!(p && ((p.from && p.from !== 'moi') ||
                             (p.who && p.who !== 'moi' && p.who !== 'le groupe')));
        var motT = 'tenue';
        try{ if(typeof STLAB !== 'undefined' && STLAB.tenu) motT = STLAB.tenu; }catch(_){ }
        qd.textContent = (aDeux ? 'TENUE À DEUX' : motT.toUpperCase()) + ' · À L\u2019INSTANT';
      } }
    else cache(qd);

    /* aucune zone de message pendant l'instant : le cadre n'en porte pas. */
    cache(document.getElementById('dpCorps'));
    /* LE GESTE SORT — et il faut le sortir EN JAVASCRIPT. La section 1 lui pose un
       `display:block!important` EN LIGNE : une règle de feuille, même en !important, ne
       peut pas la battre. Constaté au relevé — `.geste-env @0,228 390×118` encore visible
       sur les trois cadres, qui n'en portent aucun. */
    cache(dp.querySelector('.geste-env'));
  }

  /* ── ON ENVELOPPE, ON NE RÉÉCRIT PAS. La fiche ordinaire garde son moteur ; l'instant
       prend la main le temps qu'il dure, et le rend. ── */
  var _traitOrig=window._ficheTrait, _cotesOrig=window._ficheCotes;
  window._ficheTrait=function(){
    var dp=armable();
    if(!dp) return _traitOrig.apply(this,arguments);
    var p=(typeof cur!=='undefined')?cur:null;
    try{ trait(dp, inv(window._instant, nature(dp)), p); }catch(e){}
  };
  window._ficheCotes=function(){
    var dp=armable();
    if(!dp){ var d2=document.getElementById('detailPoster');
      if(d2){ d2.classList.remove('inst-arrive','inst-referme','inst-apres'); }
      return _cotesOrig.apply(this,arguments); }
    var p=(typeof cur!=='undefined')?cur:null;
    /* la fiche ordinaire pose d'abord tout ce qui ne change pas (l'entête, la barre
       Peaufiner, les Noyaux) ; l'instant ne repose QUE ce que son cadre déplace. */
    try{ _cotesOrig.apply(this,arguments); }catch(e){}
    try{ cotes(dp, inv(window._instant, nature(dp)), p); }catch(e){}
  };

  /* ── LA MISE EN SCÈNE. « Une seconde, pas plus » : le champ menthe dure 1 000 ms, puis
       le champ revient à sa nature et l'écran « juste après » reste. ── */
  function rejoue(){
    try{ if(window._ficheCotes) _ficheCotes(); }catch(_){}
    try{ if(window._ficheTrait) _ficheTrait(); }catch(_){}
  }
  /* §4.5 · ON PEINT APRÈS INSERTION. `Toile.dalleTrame` peut rendre un canevas vide tant
     que le monde n'est pas prêt : une seule passe laissait le champ nu — constaté au duo,
     « juste après » en thème clair, dalle absente alors que le juge la voyait. On rejoue
     donc à 0, 60, 200 et 600 ms, exactement comme `peintMinis`. */
  function rejoueTard(){ rejoue();
    [60,200,600].forEach(function(ms){ setTimeout(function(){
      if(window._instant) rejoue(); },ms); }); }
  window._instantJoue=function(nom){ window._instant=nom||null; rejoueTard(); };
  window._instantTenue=function(){
    var dp=document.getElementById('detailPoster');
    if(!dp||!dp.classList.contains('show')) return;
    if(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) return;
    window._instant='referme'; rejoueTard();
    setTimeout(function(){ if(window._instant==='referme'){ window._instant='apres'; rejoueTard(); } },1000);
  };
  /* le déclencheur RÉEL : le geste qui se referme passe par le bouton « Tenue » du
     sélecteur d'état (l. 4604). On écoute ce nœud-là, pas une famille. */
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('#segStatus button[data-st="tenu"]');
    if(!b) return;
    setTimeout(function(){ try{ window._instantTenue(); }catch(_){} },40);
  },true);
  /* la fiche se ferme : l'instant est fini. */
  var _cd=window.closeAll;
  if(typeof _cd==='function'){
    window.closeAll=function(){ window._instant=null; return _cd.apply(this,arguments); };
    try{ closeAll=window.closeAll; }catch(_){}
  }
  var _od=window.openDetail;
  if(typeof _od==='function'){
    window.openDetail=function(){ window._instant=null; return _od.apply(this,arguments); };
    try{ openDetail=window.openDetail; }catch(_){}
  }
})();
