
(function(){
  var W=390;
  function $(s,r){return (r||document).querySelector(s);}
  function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}

  /* ⚠ DÉFAUT 1 DE L'AUDIT — LE MODE NOYAU N'A PAS DE PORTE. `#sealShare` ouvre le partage
     puis cherche `#shMode button[data-mode=pelote]` : ce bouton n'existe nulle part. On le
     CRÉE, dans `#shMode`, à côté des deux autres — le gestionnaire de `#shMode` le prend
     alors en charge sans qu'on touche à une ligne de son code. */
  function bouton_noyau(){
    var m=$('#shMode'); if(!m) return;
    if(m.querySelector('[data-mode="noyau"]')) return;
    var b=document.createElement('button');
    b.setAttribute('data-mode','noyau');
    b.textContent='Le Noyau';
    m.appendChild(b);
    /* le gestionnaire d'origine est posé bouton par bouton : on le rejoue pour le neuf */
    b.onclick=function(){
      try{
        window.shareMode='noyau';
        var np=document.getElementById('shNoyauParts'); if(np) np.style.removeProperty('display');
        $$('#shMode button').forEach(function(x){x.classList.toggle('on',x===b);});
        var sc=$('#shareScreen'); if(sc) sc.classList.add('shc-noyau');
        if(window.shareRender) shareRender();
      }catch(e){}
    };
    $$('#shMode button').forEach(function(x){
      if(x===b) return;
      var av=x.onclick;
      x.onclick=function(e){
        var sc=$('#shareScreen'); if(sc) sc.classList.remove('shc-noyau');
        if(av) return av.call(this,e);
      };
    });
  }

  /* ⚠ DÉFAUT 2 — LE SUR-MESURE NE POUVAIT PAS ATTEINDRE LA 4K QU'IL AUTORISE.
     `shCustomClamp` borne à 3840 mais désactive les `+` à 2160. On enveloppe la fonction
     et on rétablit l'état des deux boutons sur la vraie borne. */
  function borne4k(){
    if(!window.shCustomClamp || window.shCustomClamp.__4k) return;
    var f=window.shCustomClamp;
    window.shCustomClamp=function(){
      var r=f.apply(this,arguments);
      try{
        var a=(window.shCW||1080)/(window.shCH||1920);
        var bW=$('#shCustom .sh-step button[data-d="w+"]');
        var bH=$('#shCustom .sh-step button[data-d="h+"]');
        if(bW) bW.disabled=(window.shCW>=3840 || a>=2.5);
        if(bH) bH.disabled=(window.shCH>=3840 || a<=0.42);
      }catch(e){}
      return r;
    };
    window.shCustomClamp.__4k=true;
  }

  /* ⚠ DÉFAUT 5 — DEUX LIBELLÉS « FORMAT » À LA SUITE. Le premier coiffe `#shNoyauParts` :
     il doit dire ce que le Noyau montre. On corrige le MOT, on ne touche pas au nœud. */
  function libelle(){
    var np=$('#shNoyauParts'); if(!np) return;
    var l=np.previousElementSibling;
    if(l && l.classList && l.classList.contains('sh-lab') && /^\s*Format\s*$/.test(l.textContent||''))
      l.textContent='Ce qu’il montre';
  }

  function bati(){
    var sc=$('#shareScreen'), cd=$('#shcCadre');
    if(!sc||!cd) return false;

    if(!$('#shcSujet')){
      var su=document.createElement('div'); su.id='shcSujet';
      cd.appendChild(su);
    }
    if(!$('#shcPeaufiner')){
      var pf=document.createElement('div'); pf.id='shcPeaufiner';
      pf.innerHTML='<div class="shp-t">Peaufiner</div><div class="shp-c">›</div>';
      pf.onclick=function(e){ e.stopPropagation(); sc.classList.toggle('shc-ouvert'); };

      /* ⚠ UN TAP AILLEURS REFERME — LA FONCTION EXISTAIT, ELLE S'ÉTAIT PERDUE.
         L'ancien écran la portait (`redteam.py` la contrôlait sous ce nom même) ; la
         refonte l'a laissée tomber, et le tiroir ne se refermait plus qu'en retouchant
         la barre. Mesuré : un tap sur l'aperçu laissait `shc-ouvert` posé. Le §5 le dit
         pour tout le produit — une refonte RESTAURE, elle ne déplace pas. */
      sc.addEventListener('click', function(e){
        if(!sc.classList.contains('shc-ouvert')) return;
        var pile = document.getElementById('shcPile');
        if(pile && pile.contains(e.target)) return;   /* on règle, on ne referme pas */
        if(pf.contains(e.target)) return;             /* la barre a son propre geste */
        sc.classList.remove('shc-ouvert');
      }, false);
      cd.appendChild(pf);
    }
    /* LE SUJET vit dehors : on lui donne le vrai `#shMode`, on ne le recopie pas
       ⚠ SAUF DEPUIS LA REFONTE « L'IMAGE EST L'ÉCRAN » (2 septembre 2026), où le sujet
       descend dans le panneau : c'est LA LIGNE qui dit où l'on en est, au repos. Ce lot-ci
       reprenait `#shMode` à chaque passe et le remettait dehors — deux propriétaires pour
       un même nœud, et la rangée « LE SUJET » du panneau sortait VIDE, mesurée. Comme le
       clic sur un bouton du sujet n'était alors plus dans `#shcPile`, le garde « un tap
       ailleurs referme » refermait le panneau : choisir « Le Noyau » le faisait disparaître.
       Un seul propriétaire, et c'est le lot qui a décidé où le nœud vit. */
    var su2=$('#shcSujet'), m=$('#shMode');
    var plein = sc.classList.contains('sh-plein');
    if(!plein && su2 && m && m.parentNode!==su2){ su2.appendChild(m); m.className='';
      m.style.cssText='display:flex;gap:8px;width:100%;background:none;border:0;padding:0'; }
    return true;
  }

  /* les cotes — calculées, marge basse 36 */
  var Y_SUJET=600, Y_PEAUF=674, Y_BARRE=746;
  function pose(){
    if(!bati()) return;
    bouton_noyau(); borne4k(); libelle();
    /* ⚠ ET CE LOT S'ARRÊTE DÈS QUE LA REFONTE « L'IMAGE EST L'ÉCRAN » EST EN PLACE.
       Les deux posaient les MÊMES cotes — `#shcPeaufiner`, `#shcBarre`, `#shPreviewArea` —
       avec des valeurs différentes : celui-ci l'aperçu à 120 × 450, l'autre l'écran entier.
       Selon le moment, l'un gagnait ou l'autre. Vu à la sonde : la barre mesurée à 700 dans
       un relevé direct et à 746 dans la passe de `redteam` au même instant du parcours —
       c'est cette instabilité qui avalait la sonde du contrôle de recouvrement.
       Un seul propriétaire : le lot qui a décidé de la mise en page. */
    if($('#shareScreen') && $('#shareScreen').classList.contains('sh-plein')) return;
    var su=$('#shcSujet'), pf=$('#shcPeaufiner'), ba=$('#shcBarre'), pa=$('#shPreviewArea');
    if(su) su.style.top=Y_SUJET+'px';
    if(pf) pf.style.top=Y_PEAUF+'px';
    if(ba){ ba.style.top=Y_BARRE+'px'; ba.style.bottom='auto'; ba.style.height='62px'; }
    if(pa){ pa.style.top='120px'; pa.style.height='450px'; pa.style.bottom='auto'; }
    $$('#shMode button').forEach(function(b){ b.style.cssText=''; });
    centreApercu();
  }

  /* ⚠ L'APERÇU ÉTAIT COUPÉ DE 65 PX EN BAS. `shareRender()` pose la taille ET la place de
     `#shWrap` EN LIGNE (`left`, `top`), centrées pour l'ANCIENNE zone d'aperçu. Ce lot a
     déplacé la zone à 120 → 570 ; le calcul, lui, n'a pas suivi. Mesuré :

         zone d'aperçu    120 → 570   (450 de haut)
         image            220 → 635   (415 de haut, posée à top:100 dans la zone)
         → 100 px de vide en haut, 65 px de l'image rognés en bas

     Ce que l'image perd en bas, c'est SON MOT-MARQUE (§5 : « Promi » à 15 px dans les
     images partagées) — le sujet même de l'écran, coupé.

     ⚠ ET L'INSTRUMENT MENTAIT SUR LA MOITIÉ DU DIAGNOSTIC. `getBoundingClientRect` ignore
     le rognage d'un ancêtre : le mot-marque se lit à y 608 → 625, pile sur le sélecteur
     de sujet (600 → 644), et un balayage de collisions le compte comme un recouvrement de
     48 × 17. Il n'en est rien — la zone est en `overflow:hidden`, et `elementFromPoint` au
     centre du mot-marque rend `shMode`. **Avant d'accuser le dessin, on vérifie
     l'instrument** (§8) : le recouvrement était faux, le rognage était vrai.

     La parade est celle du §8 : on ENVELOPPE, on ne se contente pas d'écouter — ce que ce
     lot fait déjà plus bas pour `shareRender`. */
  function centreApercu(){
    var pa=$('#shPreviewArea'), w=$('#shWrap');
    if(!pa||!w) return;
    var zh = pa.clientHeight, h = w.offsetHeight;
    if(!zh || !h) return;
    var t = Math.max(0, Math.round((zh - h) / 2));
    if(w.style.top !== t + 'px') w.style.top = t + 'px';
  }

  [0,140,420,900,1800,3200,5000].forEach(function(d){ setTimeout(pose,d); });

  /* ⚠ §8 · UNE MISE EN PAGE POSÉE PAR UN LOT EST DÉFAITE SANS QU'ON Y TOUCHE. Le lot
     « feuille » repose sa pile de son côté et reprend `#shMode` : mesuré, le sélecteur
     revenait à 0 × 0 hors de `#shcSujet` quelques centaines de millisecondes après.
     Envelopper `shareRender` ne suffit pas — il n'est pas le seul chemin. On observe donc
     l'écran, et on repose SI ET SEULEMENT SI le sélecteur en est sorti : sans cette
     comparaison, l'observateur se réveille lui-même (le piège du §8). */
  try{
    var _sc=document.getElementById('shareScreen');
    if(_sc){
      new MutationObserver(function(){
        var m=document.getElementById('shMode'), su=document.getElementById('shcSujet');
        if(!m||!su) return;
        if(m.parentNode===su) return;          /* rien n'a bougé : on ne réveille rien */
        pose();
      }).observe(_sc,{childList:true,subtree:true});
    }
  }catch(_){}
  document.addEventListener('click',function(){ setTimeout(pose,90); },true);
  if(window.shareRender && !window.shareRender.__sst){
    var f=window.shareRender;
    window.shareRender=function(){ var r=f.apply(this,arguments);
      requestAnimationFrame(pose); return r; };
    window.shareRender.__sst=true;
  }
  window._partageSansTrait=pose;
  window._partageSonde=function(){
    var sc=$('#shareScreen');
    return {
      trait:  !!($('#shcTrait') && getComputedStyle($('#shcTrait')).display!=='none'),
      sujet:  $$('#shcSujet #shMode button').map(function(b){return b.textContent;}),
      noyau:  !!$('#shMode [data-mode="noyau"]'),
      peaufiner: !!$('#shcPeaufiner'),
      ouvert: sc?sc.classList.contains('shc-ouvert'):null
    };
  };
})();
