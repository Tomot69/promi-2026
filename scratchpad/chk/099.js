
/* ══════════════════════════════════════════════════════════════════════════════
   ⚑ 23 SEPTEMBRE 2026 (Tom) — LE VERT PROFOND NE SE LIT PAS SUR LE CHAMP PRUNE.

   « Les textes en vert sombre sur les Promi et Chiches tenus ne se lisent pas sur le
     nouveau pourpre sombre du fond. Tout ce qui est en vert sombre sur pourpre, tu le
     mets dans le vert amande. Mode clair comme sombre, puisque le fond pourpre ne
     change pas. Il faut aussi marquer TENUE en vert amande #8FE08F, un peu gras, pour
     signifier — en plus du trait complet — que c'est tenu. Ce vert amande est beau et
     rare, donc célèbre. »

   ⚠ CECI CORRIGE Q258 ET Q262, ET C'EST TOM QUI TRANCHE. Le 22 septembre : « l'amande
   ne peint jamais un état ». Le 23 : sur le champ prune, elle le peint — parce que le
   vert profond y est illisible (mesuré : #00341A sur #2B1020, Δlum 11,3 ; l'amande,
   Δlum 190,6). La règle qui en sort n'est pas « l'amande revient partout » : c'est
   « SUR UN FOND SOMBRE, LE TENU EST L'AMANDE » — la même doctrine que le §3, une
   marque suit ce qui est peint SOUS elle.

   ⚠ ET ON TRIE LES SURFACES, PAS LES RÈGLES (§8). On ne cherche pas les sélecteurs qui
   DÉCLARENT le vert profond — le fichier en a des dizaines et la plupart ne peignent
   rien. On parcourt le DOM, on lit la couleur CALCULÉE, on remonte au premier fond
   OPAQUE, et on ne touche qu'à ce qui est vraiment peint en vert profond sur du sombre.
   ══════════════════════════════════════════════════════════════════════════════ */
(function(){
  /* ⚑ v16 (Tom) : un texte d'état sur fond sombre passe CRÈME — l'amande ne peint que la célébration.
     Le nom reste (trois lectures le partagent) ; la valeur est la crème. */
  var TENU='#00341A', AMANDE='#F7F0DE', CRETE='#0B4A2A';
  function rgbDe(c){ var m=/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/.exec(c||'');
    if(!m) return null; if(m[4]!==undefined && +m[4]===0) return null;
    return [+m[1],+m[2],+m[3]]; }
  function lum(v){ return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]; }
  function hexDe(v){ return '#'+v.map(function(x){return x.toString(16).padStart(2,'0');}).join('').toUpperCase(); }
  /* le premier fond OPAQUE au-dessus de l'élément — jamais un sélecteur deviné */
  function fondSous(e){
    var p=e;
    while(p && p!==document.body){
      var v=rgbDe(getComputedStyle(p).backgroundColor);
      if(v) return v;
      p=p.parentElement;
    }
    return null;
  }
  window._fondSombreSous = function(e){ var v=fondSous(e); return !!(v && lum(v) < 90); };

  /* le seuil : 90 de luminance. La terre prune vaut 25,6 ; le brun du mode sombre 27,4 ;
     la crème 238,3 ; le corps clair d'un Promi 224,6. Aucune valeur du produit ne tombe
     près de 90 — le seuil ne tranche jamais un cas limite. */
  var VERTS = {'#00341A':1, '#0B4A2A':1};
  function passe(racine){
    var n = racine || document.getElementById('device'); if(!n) return 0;
    var faits=0;
    n.querySelectorAll('*').forEach(function(e){
      /* ⚠ PAS DE DRAPEAU « DÉJÀ FAIT ». Le peintre de la fiche repasse derrière nous et
         réécrit la couleur : un `data-amande` qui fait sortir tôt gèle la passe sur un état
         qui n'existe plus. On relit donc la couleur CALCULÉE à chaque fois — la passe se
         RELIT, elle ne fige pas (§6, la leçon de `lot-POLICES`). */
      /* ⚑ v23 — ET ELLE DÉFAIT CE QU'ELLE A FAIT. Elle ne le faisait pas : une fois la crème
         posée, `cs.color` n'est plus un VERT, la passe sort tout de suite, et l'inline
         `!important` SURVIT au changement de thème. Pris par `releve-S4` : le compte du Fil,
         peint en crème sur le plateau sombre, restait crème quand le plateau devenait crème —
         **Δlum 0,0, le chiffre disparaît**. C'est la parade de `lot-POLICES` (§6) et celle de
         la passe voisine (`data-lis`) : on note la valeur d'avant ET sa priorité, on relit la
         cascade, puis on décide — et on remet si l'on ne repeint pas. */
      if(e.getAttribute('data-amande')!=null){
        var _av=e.getAttribute('data-amande-av');
        /* ⚑ v29 (Q310, l'isolé n° 3) — ON NE DÉFAIT QUE CE QU'ON A FAIT. Si un peintre a réécrit la couleur depuis
           (la fiche suivante pose son état en ligne), la valeur notée est PÉRIMÉE : la remettre ramenait le vert
           d'une fiche tenue sur un Chiche « à relever », que la passe repeignait ensuite en crème. Mesuré dans
           l'ordre de releve-S1 : l'à-qui sortait crème au lieu de #DD4D23. On oublie la note, on ne touche à rien. */
        var _cur=rgbDe(e.style.getPropertyValue('color'));
        if(!_cur || hexDe(_cur)!==AMANDE.toUpperCase()){ e.removeAttribute('data-amande'); e.removeAttribute('data-amande-av'); _av=null; }
        else { e.style.removeProperty('color'); e.style.removeProperty('-webkit-text-fill-color'); }
        e.removeAttribute('data-amande');
        if(_av){ try{ var v=JSON.parse(_av);
          if(v[0]) e.style.setProperty('color', v[0], v[1]);
          if(v[2]) e.style.setProperty('-webkit-text-fill-color', v[2], v[3]); }catch(_){} }
        e.removeAttribute('data-amande-av');
      }
      var cs=getComputedStyle(e);
      if(cs.visibility==='hidden' || cs.display==='none') return;
      var c=rgbDe(cs.color); if(!c) return;
      if(!VERTS[hexDe(c)]) return;
      /* il faut du TEXTE à soi : on ne repeint pas un conteneur qui ne fait qu'hériter */
      var aDuTexte=false;
      for(var i=0;i<e.childNodes.length;i++){
        var k=e.childNodes[i];
        if(k.nodeType===3 && k.textContent.trim()){ aDuTexte=true; break; }
      }
      if(!aDuTexte) return;
      if(!window._fondSombreSous(e)) return;
      e.setAttribute('data-amande-av', JSON.stringify([
        e.style.getPropertyValue('color'), e.style.getPropertyPriority('color'),
        e.style.getPropertyValue('-webkit-text-fill-color'), e.style.getPropertyPriority('-webkit-text-fill-color')]));
      e.style.setProperty('color', AMANDE, 'important');
      e.style.setProperty('-webkit-text-fill-color', AMANDE, 'important');   /* §3 : les deux, toujours */
      e.setAttribute('data-amande','1');
      faits++;
    });
    return faits;
  }
  window._amandeSurSombre = passe;

  /* ⚑ « TENUE » EN AMANDE, UN PEU GRAS — la célébration, en plus du trait complet.
     On ne vise QUE le mot d'état, jamais la date qui le suit : `.dpt-quand` écrit
     « TENUE · 12 MARS » d'un seul tenant, on enveloppe donc le premier segment. */
  function marqueTenue(racine){
    /* ⚑ v16 (Tom) : « TENUE » ne se marque plus en amande — l'amande n'est que la célébration. */
    return;
    var n = racine || document.getElementById('device'); if(!n) return;
    n.querySelectorAll('.dpt-quand, .s4-et').forEach(function(e){
      if(e.getAttribute('data-tenue')==='1') return;
      var t=(e.textContent||'').trim();
      var m=/^(TENUE?S?|TENU À DEUX)(\s*·\s*)?([\s\S]*)$/i.exec(t);
      if(!m) return;
      if(!window._fondSombreSous(e)) return;
      var b=document.createElement('b');
      b.textContent=m[1];
      /* ⚠ « UN PEU GRAS » NE PEUT PAS ÊTRE UNE GRAISSE : Gilbert n'en a qu'UNE (§6), et le
         §6 interdit toute graisse hors des faces embarquées — un `font-weight:700` sur ce
         mot ne change donc rien à l'écran. On l'appuie autrement, et sans sortir des règles :
         une chasse un peu ouverte et 6 % de taille en plus. */
      b.style.cssText='font-weight:700;font-size:1.06em;color:'+AMANDE+';-webkit-text-fill-color:'+AMANDE+';letter-spacing:.06em';
      e.textContent='';
      e.appendChild(b);
      if(m[3]) e.appendChild(document.createTextNode((m[2]||' · ')+m[3]));
      e.setAttribute('data-tenue','1');
    });
  }
  window._marqueTenue = marqueTenue;

  /* ══ LE FILET CRÈME QUI CERNE UN DISQUE — PARTOUT, ET SUR LE NŒUD ══════════════
     Tom, 23 septembre : « les disques dans les fiches sur le fond pourpre, je dois avoir
     le liseré filet crème comme en pj ; c'est toujours pas fait malgré plusieurs demandes,
     pourquoi ne le fais-tu pas ? » — et : « en mode sombre il faut les filets crème autour
     des disques dans l'Aura aussi, car le fond est sombre marron ».
     LA RÉPONSE, mesurée : il ÉTAIT écrit, et il ne pouvait pas se voir.
       ① il était peint DANS le canevas, avant l'anneau — et l'anneau extérieur du Cercle
          (`oR = R + lw·0,74`) repasse dessus ;
       ② il était conditionné à la classe `#detailPoster.f-tenue`, or `drawKRing` est
          appelé 8 à 12 fois par ouverture et les premiers appels précèdent la pose de la
          classe : le dernier appel gagnait, et il décidait « pas de filet » (§8 — on ne lit
          jamais un état dans une classe qui n'est pas encore là).
     LA PARADE : le filet vit sur le NŒUD. Le bord extérieur d'un anneau EST le bord de sa
     boîte — l'arc d'une fiche s'arrête à 116 sur 117 (mesuré), et l'arc de l'Aura est à
     `r + arc/2 = dia/2`. Un `box-shadow` de 1,4 px cerne donc l'anneau au pixel, et
     AUCUNE passe de peinture ne peut le défaire. */
  /* ⚑ 23 SEPTEMBRE 2026, second tour (Tom) — « TU AS DES FILETS CRÈME TRONQUÉS PAR UN
     AUTRE ÉLÉMENT AU-DESSUS. » Il a raison, et ce n'est pas un élément : **c'est la boîte
     qui rogne**. Un `box-shadow` DÉBORDE de l'élément — donc toute rangée qui glisse
     (`.au-nx` en `overflow:auto hidden`, `.aura-track` sur la fiche) le coupe net. Mesuré
     en repeignant l'ombre en ROUGE PUR et en parcourant les 360° : **96,4 % du tour, un
     trou de 264 à 277°**, pile au sommet du plus grand disque. Rembourrer les rangées
     (essayé, mesuré) ne suffit pas et déplace la composition.
     LA PARADE : le filet ne déborde plus. L'anneau finit EXACTEMENT au bord de sa boîte
     (`R + lw/2 = W/2`, le poseur le garantit) — on peint donc le filet SUR ses 1,4 derniers
     pixels, DANS la boîte. Ce qui est dans la boîte ne peut être rogné par personne. */
  var FILET_PX=1.4;
  /* ⚠ 23 SEPTEMBRE 2026, cinquième écriture — CETTE PASSE EST LE SECOND PROPRIÉTAIRE DU
     FILET (§7) : `drawKRing` le trace déjà en dernier, au bord de SON anneau, et celle-ci
     repassait dessus au bord du CANEVAS. Les deux ne coïncident que chez le poseur de fiche
     (`R+lw/2 = W/2`) ; partout ailleurs elle remettait le jeu. Elle lit donc la cote que le
     peintre DÉCLARE (`data-filet`), et ne décide plus rien toute seule. */
  function filetCanevas(cv){
    try{
      var W=cv.width, g=cv.getContext('2d'); if(!g||!W) return;
      var sc=W/(cv.getBoundingClientRect().width||W), fw=FILET_PX*sc;
      var dehors=parseFloat((cv.getAttribute('data-filet')||'').split(',')[0]);
      var r = isFinite(dehors) ? Math.min(dehors+fw/2, W/2-fw/2) : (W/2-fw/2);
      g.save(); g.lineWidth=fw; g.strokeStyle=window._FILET_DOUX||'#F7F0DE'; g.lineCap='butt';
      g.beginPath(); g.arc(W/2, W/2, r, 0, 6.2832); g.stroke(); g.restore();
    }catch(_){ }
  }
  function filetSvg(n){
    try{
      var s=n.querySelector('svg'); if(!s) return;
      var vb=(s.getAttribute('viewBox')||'').split(/\s+/).map(Number);
      var D=(vb.length===4?vb[2]:n.getBoundingClientRect().width)||0; if(!D) return;
      var c=s.querySelector('circle.kr-filet');
      if(!c){ c=document.createElementNS('http://www.w3.org/2000/svg','circle');
        c.setAttribute('class','kr-filet'); s.appendChild(c); }
      c.setAttribute('cx', D/2); c.setAttribute('cy', D/2);
      c.setAttribute('r', D/2 - FILET_PX/2);
      c.setAttribute('fill','none'); c.setAttribute('stroke',window._FILET_DOUX||'#F7F0DE');
      c.setAttribute('stroke-width', FILET_PX);
    }catch(_){ }
  }
  function filets(racine){
    var n = racine || document.getElementById('device'); if(!n) return;
    n.querySelectorAll('canvas.kr-c, .au-nb').forEach(function(e){
      var r=e.getBoundingClientRect(); if(r.width<8) return;
      e.style.removeProperty('box-shadow');          /* l'ancien filet qui débordait */
      if(!window._fondSombreSous(e)){
        var v=e.querySelector && e.querySelector('circle.kr-filet'); if(v) v.remove();
        return;
      }
      /* ⚑ v18 (Tom) : plus de cercle complet — le filet vit sur chaque segment (drawKRing, lot-V16) */
      var _kf=e.querySelector && e.querySelector('circle.kr-filet'); if(_kf) _kf.remove();
    });
  }
  window._filetsDisques = filets;

  /* ══ LA PASTILLE D'UNE CARTE QUI ATTEND UN GESTE ═══════════════════════════════
     Tom, 23 septembre : « dans le Fil et dans l'Index, il faudrait une pastille pour
     signifier les cartes ou bandeaux nouveaux, en attente d'action etc — subtil et beau. »
     CE QU'ELLE DIT, et rien d'autre : *cette parole attend un geste de toi*. Le produit
     connaît déjà cet état — le Fil a son filtre « Ce qui attend un geste » — on ne fabrique
     donc aucune notion neuve (§9 : on n'invente pas une fonction).
     SA FORME : un disque de 9 px, la couleur de l'état qu'elle attend, cerné du même filet
     crème de 1,4 px que les disques. Pas de texte, pas de nombre, pas de halo — le §3 :
     un élément coloré ne reste que s'il porte du sens, et celui-là en porte un.
     ⚠ ON LIT L'ÉTAT DÉCLARÉ (`data-etat`), jamais la couleur peinte : une couleur se
     remesure, un état se déclare. Le libellé sert de repli quand l'attribut manque. */
  var ATTEND=/^(À TENIR|A TENIR|À RELEVER|A RELEVER|DEMANDÉ|DEMANDE|EN ATTENTE)/i;
  function pastilles(racine){
    var n = racine || document.getElementById('device'); if(!n) return;
    n.querySelectorAll('.s4-carte, .s4-bandeau, .fd-card').forEach(function(c){
      var et=c.querySelector('.s4-et'), dec=c.getAttribute('data-etat')||'';
      var t=(et&&et.textContent||'').trim();
      /* ⚑ v89 (Tom, Q347) — LA PASTILLE DIT « PAS ENCORE VU » (elle disait « attend un geste » ; le compteur du Fil porte désormais
         ce compte) : une carte du Fil déclare son non-vu (`data-nonvu`) ; une carte d'Index est non vue si une entrée du Fil de son
         Promi l'est. Elle s'efface quand on ouvre la carte. */
      var nvA=c.getAttribute('data-nonvu'), pidA=c.getAttribute('data-pid');
      var attend = nvA!=null ? nvA==='1' : (pidA!=null && (function(){ try{ return (FEED||[]).some(function(f){ return f.pid===+pidA && f.unread; }); }catch(_){ return false; } })());
      var p=c.querySelector(':scope > .s4-att');
      if(!attend){ if(p) p.parentNode.removeChild(p); return; }
      if(!p){ p=document.createElement('i'); p.className='s4-att'; c.appendChild(p); }
      var col='#DD4D23';
      p.style.cssText='position:absolute;top:10px;right:10px;z-index:4;width:9px;height:9px;'
        +'border-radius:50%;background:'+col+';box-shadow:0 0 0 1.4px #F7F0DE;pointer-events:none';
    });
  }
  window._pastillesAttente = pastilles;

  /* ── QUAND ON REPASSE. Un écran qui se rouvre reconstruit ses nœuds : les marques
        posées meurent avec eux, et `data-amande` repart à zéro. On repasse donc après
        chaque ouverture — en ENVELOPPANT les portes, jamais en observant une classe
        qui ne se retire pas (§8, le régulateur de la Pelote). */
  /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « DANS LES NUÉES BIEN REMPLIES, ÇA FAIT BUGUER
     L'AFFICHAGE EN HAUT DE L'ÉCRAN, SUPERPOSITIONS. » Mesuré sur « le potager » (9 Promi) :
     `#dpNueeFil` rendait à **y 0**, sur 862 de haut, pendant que l'encart (227), « Avec
     Rachel, Adrien, +3 » (351), le titre (381) et la méta (446) gardaient leurs cotes —
     les cartes passaient donc DESSOUS et tout se superposait.
     LA CAUSE : le poseur de cotes (`_ficheCotes`) place le fil à `yEtat + hauteur de la
     méta + 16,25` — mais le fil est BÂTI APRÈS lui. Au moment où il pose, `#dpNueeFil`
     n'existe pas encore, et plus rien ne le replace. C'est l'ordre, pas la cote.
     LA PARADE : on redemande les cotes une fois le fil bâti. `_ficheCotes` est idempotente
     (elle pose des valeurs absolues, elle ne cumule rien) — on peut la rappeler sans risque. */
  /* ⚠ ET ON NE RAPPELLE PAS LE POSEUR ENTIER. Essayé, mesuré : `_ficheCotes()` appelée
     sans son contexte renvoie toute la fiche hors de l'écran (tout à y ≥ 844). On replace
     LE SEUL NŒUD qui manque, à partir de ce qui est RENDU au-dessus de lui. */
  function recote(){
    try{
      var dp=document.getElementById('detailPoster');
      if(!dp || !dp.classList.contains('show')) return;
      /* ⚠ ON NE DEVINE PAS LE NOM DE LA CLASSE. La fiche d'une Nuée en porte plusieurs
         (`dp-nuee`, `dp-mode-nuee`…) selon le chemin d'ouverture — un premier jet testait
         `dp-nuee` et ne mordait jamais. On reconnaît l'écran à ce qu'il CONTIENT : un fil
         de Nuée bâti et visible. */
      var fil=document.getElementById('dpNueeFil'), qd=document.getElementById('dptQuand');
      if(!fil || !qd || !fil.querySelector('.nf-item, .nf-vide')) return;
      if(!qd.getBoundingClientRect().height) return;
      var rd=dp.getBoundingClientRect(), sc=(dp.clientWidth||390)/390;
      var rq=qd.getBoundingClientRect();
      if(!rq.height) return;
      var y=Math.round((rq.bottom-rd.top)/sc + 16.25);
      /* ⚠ ON NE REPLACE QUE CE QUE LE POSEUR N'A PAS PLACÉ. Un premier jet replaçait le fil
         à CHAQUE passage, à partir du rectangle rendu de la méta — et il décalait de 37 px
         les Nuées que le poseur avait bien servies (`redteam_nuee` : « ligne de fil 1 y,
         588 au lieu de 551 »). Le poseur a la cote de la planche ; nous n'avons que le
         rendu. On n'intervient donc QUE dans le cas cassé : le fil laissé à 0. */
      /* ⚠ ON N'INTERVIENT QUE SUR LE DÉFAUT, ET ON LE RECONNAÎT À SA FORME : le fil
         RECOUVRE la méta. Un premier jet replaçait le fil à chaque passage, à partir du
         rectangle rendu — et il décalait de 37 px les Nuées que le poseur avait bien
         servies (`redteam_nuee` : « ligne de fil 1 y, 588 au lieu de 551 »). Un second
         testait `top > 1` — mais sur une Nuée pleine le poseur écrit 30, une valeur
         « posée » et fausse. Le seul critère juste est le RECOUVREMENT. */
      /* ⚑ 22 SEPT. 2026 — LE FIL NE SUIVAIT PLUS LA MÉTA (attendu 502, mesuré 470 à 588).
         Ce passage mesurait la méta RENDUE — et il est appelé PENDANT L'ANIMATION D'ENTRÉE de la
         fiche : il lisait la méta en plein vol, posait le fil à une cote fausse, et n'était plus
         rappelé une fois la fiche posée. Le fil restait sur la méta (470 contre 487).
         LA COTE SE CALCULE, ELLE NE SE MESURE JAMAIS (§8) : on part de la cote DÉCLARÉE de la
         méta (celle que le poseur a écrite), plus sa hauteur et l'air de 16,25 — la formule
         même du poseur. Et à l'état défilé, le poseur a ses propres cotes (fil à 182) : on
         n'y touche pas. */
      if(window._nueeDefileEtat) return;
      var qTop=parseFloat(qd.style.top);
      if(!isFinite(qTop)) return;
      var _hq=13.75; try{ var _h=qd.offsetHeight; if(_h) _hq=_h; }catch(_){}
      y=Math.round(qTop + _hq + 16.25);
      if(Math.abs(parseFloat(fil.style.top||'0') - y) < 0.6) return;
      fil.style.setProperty('position','absolute','important');
      fil.style.setProperty('left','0','important');
      fil.style.setProperty('top', y+'px','important');
      fil.style.setProperty('width','390px','important');
      fil.style.setProperty('margin','0','important');
      fil.style.setProperty('padding','0','important');
      var mn=document.getElementById('dpMain');
      if(mn){ var h=Math.round(fil.getBoundingClientRect().height/sc);
        mn.style.setProperty('min-height', Math.max(760, y+h+30)+'px','important'); }
    }catch(_){ }
  }
  function repasseVraie(){ try{ recote(); passe(); marqueTenue(); filets(); pastilles(); }catch(_){ } }
  /* ⚑ v59 (latences) — appelée après CHAQUE `_ficheCotes`, `_fichePose`, `_s4Index` (des dizaines de fois à l'ouverture d'une
     fiche ou de l'Index) et après chaque clic, elle relisait à chaque fois le style calculé de tout l'appareil. Elle se fait
     maintenant UNE FOIS PAR IMAGE au plus, dans le rappel d'image — avant que l'image soit peinte : elle garde le dernier mot,
     sans flash possible. */
  var _rpDemande = false;
  function repasse(){ if(_rpDemande) return; _rpDemande = true; requestAnimationFrame(function(){ _rpDemande = false; repasseVraie(); }); }
  window._repasseSombre = repasseVraie;
  /* ⚠ DEUX PROPRIÉTAIRES POUR UNE MÊME PROPRIÉTÉ (§7) — ET ON L'A PAYÉ ICI.
     `data-amande` était bien posé, et la couleur revenait quand même au vert profond :
     `window._ficheCotes` (par `pose`) réécrit `color` ET `-webkit-text-fill-color` EN
     LIGNE, avec `important`, à chaque passage. Piégé au peintre (on enveloppe
     `setProperty` et on lit la pile), pas en relisant le code. La parade du §7 :
     UN propriétaire, et il a LE DERNIER MOT — on enveloppe donc `_ficheCotes`. */
  ['_ficheCotes','_fichePose','_s4Index'].forEach(function(nom){
    var f=window[nom]; if(typeof f!=='function') return;
    window[nom]=function(){ var r=f.apply(this,arguments); try{ repasse(); }catch(_){ } return r; };
  });
  ['openDetail','openNueeDetail','openPerson','closeAll'].forEach(function(nom){
    var f=window[nom]; if(typeof f!=='function') return;
    window[nom]=function(){ var r=f.apply(this,arguments);
      requestAnimationFrame(function(){ requestAnimationFrame(repasse); }); return r; };
  });
  document.addEventListener('click', function(){ requestAnimationFrame(function(){ requestAnimationFrame(function(){ (window._apresMouvement||function(f){f();})(repasse); }); }); }, true);
  if(document.readyState!=='loading') setTimeout(repasse, 900); else document.addEventListener('DOMContentLoaded', function(){ setTimeout(repasse,900); });
})();
