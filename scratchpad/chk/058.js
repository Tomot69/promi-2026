
/* ═══════════════════════════════════════════════════════════════════════════════════════
   AUCUNE GRAISSE HORS DES FACES EMBARQUÉES.
   En navigateur, une graisse absente se substitue EN SILENCE — la plus proche, ou une
   oblique synthétique. **En Swift, elle casse.** Le prototype étant la spécification du
   portage, tout couple demandé doit exister en `@font-face`. Relevé sur l'app d'aujourd'hui
   (`redteam_polices.py`) : **7 couples absents, 359 éléments, tous les écrans.**

   LES SIX FACES EMBARQUÉES, ET ELLES SEULES :
       Fraunces 600 normal · Fraunces 600 italique
       Bricolage 600 · Bricolage 700
       Apfel 400 · ApfelMid 500                          (aucune italique)

   LA TABLE DE REPORT — chaque couple absent va sur le couple embarqué le plus proche,
   SANS CHANGER LA HIÉRARCHIE VISUELLE (ce qui était plus gras le reste, ce qui était plus
   léger le reste) :

       Apfel 500 · 600 · 700 · 800   →  ApfelMid 500   la graisse existe, dans la famille
                                                        qui la porte réellement ; rien de
                                                        plus gras n'est embarqué en Apfel
       Apfel 400 italique            →  Apfel 400      aucune italique en Apfel : l'oblique
                                                        était synthétique, elle disparaît
       ApfelMid 400                  →  Apfel 400      la graisse 400 existe, dans Apfel
       Bricolage 800                 →  Bricolage 700  la plus grasse embarquée
       Bricolage 400                 →  Bricolage 600  la plus légère embarquée

   ⚠ POURQUOI EN JAVASCRIPT, ET PAS DANS LE CSS. Le couple dépend de DEUX déclarations —
   la famille et la graisse — qui vivent rarement dans la même règle : réécrire
   « font-weight:800 → 700 » à l'aveugle enverrait un `Apfel 800` sur `Apfel 700`, tout
   aussi absent. Et le §9 de CLAUDE.md interdit de nettoyer le CSS (cinq tentatives, cinq
   échecs). On lit donc le couple CALCULÉ — le seul endroit où la cascade est déjà résolue —
   et on le ramène sur sa face. Une seule table, un seul endroit, et `redteam_polices.py`
   le vérifie à chaque passage.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  /* les faces embarquées, écrites une fois */
  var FACES = {
    'fraunces|600|normal':1, 'fraunces|600|italic':1,
    'gilbert|700|normal':1,
    'atkinson|400|normal':1, 'atkinson|500|normal':1, 'atkinson|700|normal':1,
    'bricolage|600|normal':1, 'bricolage|700|normal':1,
    'apfel|400|normal':1, 'apfelmid|500|normal':1
  };
  /* ⚑ v24 (Tom, 22 sept.) — TROIS POLICES, ET TROIS SEULEMENT. Bricolage et Apfel sont sorties
     avec Fraunces : en Swift elles n'existeraient pas, et les trois caractères qu'elles
     dessinaient encore (‹ › et →) tombent sur la police du système, comme ✕ ✦ ● le font déjà. */
  var NOTRE = {gilbert:1, atkinson:1, promilate:1};

  /* la table de report : famille demandée → [famille embarquée, graisse, style] */
  function report(fam, w, st){
    /* ⚑ 16 sept. 2026 — Gilbert Bold (une seule graisse) porte les sous-titres, les libellés
       et la navigation ; Atkinson Hyperlegible porte tout le texte, en 400 · 500 · 700.
       Aucune italique n'est embarquée dans ces deux familles : l'oblique était déjà
       synthétique en Apfel, et le report la retirait — il la retire pareillement ici. */
    if(fam === 'gilbert')  return ['Gilbert', 700, 'normal'];
    if(fam === 'atkinson'){
      if(st === 'italic') return ['Atkinson', 400, 'normal'];
      if(w >= 450)        return ['Atkinson', 500, 'normal'];   /* comme ApfelMid 500 hier : la hiérarchie ne bouge pas */
      return ['Atkinson', 400, 'normal'];
    }
    if(fam === 'fraunces' || fam === 'promilate') return ['PromiLate', 400, 'normal'];  /* v23 : Fraunces retirée */
    return null;
  }

  /* ⚑ on note ce qu'il y avait AVANT de l'écraser, et on le remet avant de relire :
     une autre passe (`pose()`, sur le Peaufiner d'une Nuée) écrit sur les mêmes propriétés. */
  function _garder(e){
    if(e.getAttribute('data-pol-av') !== null && e.getAttribute('data-pol-av') !== undefined) return;
    e.setAttribute('data-pol-av', JSON.stringify([
      e.style.getPropertyValue('font-family'), e.style.getPropertyPriority('font-family'),
      e.style.getPropertyValue('font-weight'), e.style.getPropertyPriority('font-weight'),
      e.style.getPropertyValue('font-style'),  e.style.getPropertyPriority('font-style')]));
  }
  function _rendre(e){
    var s = e.getAttribute('data-pol-av');
    e.style.removeProperty('font-family'); e.style.removeProperty('font-weight'); e.style.removeProperty('font-style');
    if(s == null) return;
    try{ var v = JSON.parse(s);
      if(v[0]) e.style.setProperty('font-family', v[0], v[1]);
      if(v[2]) e.style.setProperty('font-weight', v[2], v[3]);
      if(v[4]) e.style.setProperty('font-style',  v[4], v[5]);
    }catch(_){}
    e.removeAttribute('data-pol-av');
  }

  var PILE = {PromiLate:"PromiLate,Gilbert,system-ui,sans-serif",
              Gilbert:"Gilbert,system-ui,sans-serif",
              Atkinson:"Atkinson,system-ui,sans-serif"};

  /* ⚠ LA PASSE SE RELIT, ELLE NE FIGE PAS. Premier essai : on posait l'inline `!important`
     et on n'y revenait plus. Mais une passe peut tomber AVANT que le CSS ait fini de poser
     sa graisse : « Peaufiner » était lu à 400, reporté sur Bricolage 600, et l'inline
     empêchait ensuite le 700 que la feuille voulait — mesuré au contrat visuel,
     `fiche · peaufiner : 700 → 600`. **Une graisse figée trop tôt change la hiérarchie**,
     ce que ce lot interdit.
     Parade : pour un élément qu'on a DÉJÀ touché, on retire d'abord notre inline, on relit
     ce que la cascade dit VRAIMENT, puis on décide à nouveau. Si la feuille est revenue sur
     une face embarquée, on ne repose rien. Seuls les éléments marqués paient ce coût. */
  function passe(racine, debut, fin){
    try{
      var n = 0;
      var els = (racine instanceof NodeList) ? racine : (racine && racine.__l) ? racine.__l : (racine || document).querySelectorAll('*');
      for(var i=(debut||0);i<(fin!=null?Math.min(fin,els.length):els.length);i++){
        var e = els[i];
        /* ⚠ ON NE TOUCHE QUE CE QUI PORTE DU TEXTE. Un conteneur sans nœud de texte
           n'affiche aucune police : lui réécrire sa graisse ne change rien à l'écran et
           pollue le contrat visuel (mesuré : `.dpd-tog` conteneur, 400 → 600, alors que son
           libellé porte sa propre graisse). Même filtre que `redteam_polices.py`. */
        var aTexte = false;
        for(var q=0;q<e.childNodes.length;q++){
          var nd = e.childNodes[q];
          if(nd.nodeType === 3 && nd.nodeValue && nd.nodeValue.trim()){ aTexte = true; break; }
        }
        if(!aTexte){
          if(e.getAttribute && e.getAttribute('data-pol') === '1'){
            _rendre(e); e.removeAttribute('data-pol');
          }
          continue;
        }
        if(e.getAttribute && e.getAttribute('data-pol') === '1'){
          _rendre(e);
        }
        var c = getComputedStyle(e);
        var fam = (c.fontFamily||'').split(',')[0].replace(/["']/g,'').trim().toLowerCase();
        if(!NOTRE[fam]){ if(e.removeAttribute) e.removeAttribute('data-pol'); continue; }
        var w = parseInt(c.fontWeight,10)||400;
        var st = (c.fontStyle||'normal').indexOf('italic')>=0 ? 'italic' : 'normal';
        if(FACES[fam+'|'+w+'|'+st]){                             /* la feuille dit juste */
          if(e.removeAttribute) e.removeAttribute('data-pol');
          continue;
        }
        var r = report(fam, w, st); if(!r) continue;
        _garder(e);
        e.style.setProperty('font-family', PILE[r[0]], 'important');
        e.style.setProperty('font-weight', String(r[1]), 'important');
        e.style.setProperty('font-style', r[2], 'important');
        e.setAttribute('data-pol','1');
        n++;
      }
      return n;
    }catch(_){ return 0; }
  }
  window._polices = passe;

  /* ── QUAND. Après chaque rendu qui pose des nœuds, et après chaque doigt. On ne pose
       PAS d'observateur : le §8 de CLAUDE.md en donne la raison — un observateur dont la
       réaction modifie le DOM se réveille lui-même, et l'app rame. ── */
  /* ⚑ v59 (latences, Tom : « entre le clic sur + et le chargement de la page, ça accroche ») — mesuré au profileur : cette passe
     relisait le style calculé de TOUS les éléments du document, deux fois après chaque clic (+60 et +420 ms) et après chaque rendu,
     en plein milieu de la transition — jusqu'à 1,3 s de fil principal pendant une plantation. Elle se fait maintenant EN TÂCHE DE
     FOND : une seule passe à la fois (les demandes qui arrivent pendant qu'elle court la relancent une fois, à la fin), découpée
     par tranches de 6 ms dans les temps morts du navigateur. Ce qu'elle corrige (une graisse absente des faces embarquées) change
     à peine le dessin : le reporter de quelques centaines de ms ne se voit pas ; bloquer la transition, si. */
  var _enCours=false, _redemande=false;
  function _libre(fn){ if(window.requestIdleCallback) requestIdleCallback(fn,{timeout:700}); else setTimeout(function(){ fn({timeRemaining:function(){return 6;},didTimeout:true}); },40); }
  function passeFond(){
    if(_enCours){ _redemande=true; return; }
    _enCours=true; _redemande=false;
    var els=document.querySelectorAll('*'), i=0, _t0P=performance.now();
    (function tranche(){
      var t0=performance.now(), budget=5;
      while(i<els.length && performance.now()-t0<budget){ passe(els, i, i+40); i+=40; }
      if(i<els.length) setTimeout(tranche, 0);   /* tâches courtes enchaînées : on n'attend pas de temps mort (la Toile animée n'en laisse pas) */
      else { _enCours=false; window._policesDuree=Math.round(performance.now()-_t0P); window._policesN=els.length; if(_redemande) setTimeout(passeFond, 30); }
    })();
  }
  window._policesFond = passeFond;
  /* ⚑ v59 — LA PASSE VISIBLE : synchrone comme avant, mais sur ce qui est À L'ÉCRAN seulement — les écrans et feuilles
     ouverts, l'accueil. Les écrans fermés (glissés hors champ, jamais en display:none) faisaient l'essentiel des ~2 400
     éléments relus à chaque fois ; ils sont relus en tâche découpée, plus tard. */
  function visibles(){
    var dv=document.getElementById('device'), R=[], L=[];
    if(!dv) return L;
    [].forEach.call(dv.children, function(c){ if(!c.matches('.screen,.sheet,.poster,.feedview')) R.push(c); });
    [].forEach.call(document.querySelectorAll('.screen.show,.sheet.show,.poster.show,.feedview.in'), function(c){ R.push(c); });
    R.forEach(function(r){ L.push(r); [].push.apply(L, r.querySelectorAll('*')); });
    return L;
  }
  function passeVisible(){ if(window._policesFond && window._policesFond.__coupe) return; try{ var L=visibles(); passe({length:L.length, __l:L}); }catch(_){ } }
  function tard(){ var p=function(){ (window._apresMouvement||function(f){f();})(passeVisible); }; setTimeout(p, 60); setTimeout(p, 420); setTimeout(p, 900);
    setTimeout(function(){ (window._apresMouvement||function(f){f();})(function(){ (window._policesFond||passeFond)(); }); }, 1500); }   /* par window : un juge peut la couper pour prouver qu'il mord */
  document.addEventListener('click', tard, true);
  /* ⚠ `_ficheNuee`, `_nueePeaufiner` et `openEssaim` bâtissent leurs nœuds APRÈS les
     autres : sans eux, neuf éléments de la Nuée restaient hors face (mesuré). */
  ['_fichePose','_ppTout','_ficheTout','_ficheNuee','_nueePeaufiner','openEssaim',
   'openSheet','setView','shareRender','renderDetail']
    .forEach(function(nom){
      var f = window[nom];
      if(typeof f !== 'function') return;
      window[nom] = function(){ var r = f.apply(this, arguments); tard(); return r; };
    });
  if(document.readyState !== 'loading') tard();
  else document.addEventListener('DOMContentLoaded', tard);
  setTimeout(passeFond, 1200); setTimeout(passeFond, 2600);
})();
