
/* ═══════════════════════════════════════════════════════════════════════════════════════
   SECTION 2 · PEAUFINER — LA PAGE. Chaque réglage prend sa cote et son libellé dans
   PROMI-SPECIFICATIONS.md §5 (« Peaufiner Promi / Nuée / Chiche », « Le bloc du Cercle »).
   Aucune valeur n'est estimée : la liste part de 110, chaque réglage fait 64 (92 avec
   ligne de visibilité, 104 ou 118 pour une zone de texte), l'écart vaut 16.
   Aucun mot n'est inventé : les libellés sont ceux de l'inventaire, les valeurs viennent
   des données du Promi, les contrôles sont ceux de l'app, déplacés et non recréés.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  function $(s,r){ return (r||document).querySelector(s); }
  function el(t,c){ var e=document.createElement(t); if(c) e.className=c; return e; }
  /* la Nuée SE TESTE EN PREMIER : une fiche de Nuée peut garder la classe dp-chiche de la
     fiche précédente, et l'ordre inverse rendait les réglages d'un Chiche sous un titre de
     Nuée (constaté en capture, pas deviné). */
  function nat(dp){ return (dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) ? 'nuee'
    : (dp.classList.contains('dp-chiche') ? 'chiche' : 'promi'); }

  /* ── à qui la chose est visible. §6 : « tout ce qu'on ajoute à une promesse est vu par
       ceux qu'elle engage ». Les mots sont ceux de l'inventaire. ── */
  function destinataire(p){
    if(!p) return null;
    if(p.from && p.from!=='moi') return p.from;
    if(p.who && p.who!=='moi' && p.who!=='le groupe') return p.who;
    if(p.nuee && p.nuee!=='soi'){ try{ return NUE[p.nuee]||p.nuee; }catch(e){ return p.nuee; } }
    return null;
  }

  /* ── L'EMPRUNT D'UN CONTRÔLE DE L'APP. On note d'où il vient la première fois ; on l'y
       remet avant chaque reconstruction. Aucun contrôle n'est recréé, aucun n'est perdu. ── */
  function emprunte(id){
    var e = document.getElementById(id); if(!e) return null;
    if(!e._s2home) e._s2home = e.parentNode;
    e.setAttribute('data-s2host','1');
    return e;
  }
  function rentre(racine){
    if(!racine) return;
    racine.querySelectorAll('[data-s2host]').forEach(function(x){
      if(x._s2home && x._s2home !== x.parentNode){ try{ x._s2home.appendChild(x); }catch(_){ } }
    });
  }

  /* ── une brique de réglage (§3.3) ── */
  function reg(lab, val, o){
    o = o||{};
    var d = el('div','s2-reg'+(o.cls?(' '+o.cls):''));
    var haut = el('div','s2-haut');
    var l = el('div','s2-lab'); l.textContent = lab;
    var v = el('div','s2-val'); v.textContent = (val==null?'':val);
    haut.appendChild(l); haut.appendChild(v);
    if(o.vis){ d.appendChild(haut); var w=el('div','s2-vis'); w.textContent=o.vis; d.appendChild(w); }
    else { d.appendChild(l); d.appendChild(v); }
    if(o.hote){ var h=el('div','s2-ctl'); h.appendChild(o.hote); d.appendChild(h);
      d.addEventListener('click', function(ev){
        if(ev.target.closest && ev.target.closest('.s2-ctl')) return;
        d.classList.toggle('s2-ouv'); ev.stopPropagation(); }, true); }
    else if(o.act){ d.addEventListener('click', function(ev){ ev.stopPropagation(); o.act(); }, true); }
    return d;
  }
  /* ══ L'ÉCHÉANCE — LA LISTE UNIQUE (décision Tom, S3/Q28). ══
     Une seule liste partout, celle du sélecteur de la phrase : on la BRANCHE, on ne la
     recrée pas (c'est l'`opts` de _phraseChoix, l. ~5195).
       · « repousser » DISPARAÎT : on ne repousse pas, on change l'échéance. Sur une fiche
         le choix courant est simplement marqué ; en changer, c'est repousser.
       · « un jour » et « en l'air » valent toutes deux due = null mais restent DEUX
         valeurs distinctes : `enLair` est un drapeau séparé. Jamais fusionnées.
       · Sans choix explicite, AUCUNE pastille n'est active.
       · La liaison passe par data-q / data-d, JAMAIS par le libellé (CLAUDE.md §8). */
  var ECHEANCE = [
    {q:'jour',  mot:'un jour',            due:null, enLair:false},
    {q:'lair',  mot:'en l\u2019air',       due:null, enLair:true},
    {d:1,       mot:'demain'},
    {d:5,       mot:'5 jours'},
    {d:14,      mot:'2 semaines'},
    {d:30,      mot:'ce mois-ci'},
    {pick:1,    mot:'une date pr\u00e9cise\u2026'}
  ];
  function echeanceControle(){
    var box = document.getElementById('mgDueChips'); if(!box) return null;
    var p = (typeof cur!=='undefined') ? cur : null;
    /* quelle option est courante ? on lit la donnée, on ne devine pas — et sans choix
       explicite (aucune date, pas « en l'air »), rien n'est marqué. */
    function courante(o){
      if(!p) return false;
      if(p.dueISO) return !!o.pick;
      if(o.q==='lair') return !!p.enLair;
      if(o.q==='jour') return (p.due==null && !p.enLair && p.dueChoisi===true);
      return (o.d!=null && p.due===o.d && !p.enLair);
    }
    box.innerHTML = ECHEANCE.map(function(o){
      var prise = o.q ? (' data-q="'+o.q+'"') : (o.d!=null ? (' data-d="'+o.d+'"') : ' data-datepick="1"');
      return '<button type="button" class="s2-ech'+(courante(o)?' on':'')+'"'+prise+'>'+o.mot+'</button>';
    }).join('');
    box.querySelectorAll('button').forEach(function(b, i){
      b.addEventListener('click', function(ev){
        ev.stopPropagation();
        var o = ECHEANCE[i]; if(!o || !p) return;
        if(o.pick){ try{ var pk=document.querySelector('#csChoix [data-datepick], .ph-date');
          if(pk){ pk.click(); return; } }catch(_){}
          return; }
        p.due = (o.d!=null) ? o.d : null;
        p.enLair = !!o.enLair;
        p.dueChoisi = true;
        if(o.d!=null) p.status = 'encours';
        try{ if(window.syncAll) syncAll(); if(typeof queueSave==='function') queueSave(); }catch(_){}
        try{ renderDetail(); }catch(_){}
        try{ render(); }catch(_){}
      }, true);
    });
    return box;
  }

  /* ── une zone de texte (§3.4). Le mot d'invite est CELUI DU MOODBOARD : le champ des
       commentaires disait « écrire un commentaire… », l'inventaire dit « écris un mot… »
       sur les trois natures. On suit la référence, on n'invente pas. Noté en QUESTIONS. ── */
  function invite(hote, mot){ try{ if(hote && 'placeholder' in hote) hote.placeholder = mot; }catch(_){ } return hote; }
  function zone(lab, hote, vis, h104){
    var d = el('div','s2-reg s2-zone'+(h104?' s2-z104':''));
    var l = el('div','s2-lab'); l.textContent = lab; d.appendChild(l);
    if(hote){ hote.classList.add('s2-txt'); d.appendChild(hote); }
    if(vis){ var w=el('div','s2-vis'); w.textContent=vis; d.appendChild(w); }
    return d;
  }
  /* ── un bouton (§3.6) ── */
  function bouton(mot, creux, act){
    var b = el('div','s2-bouton'+(creux?' s2-creux':''));
    b.textContent = mot;
    if(act) b.addEventListener('click', function(ev){ ev.stopPropagation(); act(); }, true);
    return b;
  }
  /* ── LE BLOC DU CERCLE (§3.8). Les quatre réglages sont floutés et inertes : ils
       montrent ce que le Cercle ouvre, ils ne l'ouvrent pas. « LA MÉMOIRE » est le
       quatrième, comme dans les quatre écrans qui portent le bloc. ── */
  function cercle(){
    var c = el('div','s2-cercle');
    /* ⚑ L'ORDRE DE TOM (11 sept. 2026) : récurrence · rappels · importance · mémoire — la récurrence se comprend tout
       de suite et on en voit l'usage ; la mémoire, la plus abstraite, ne vend rien en tête de liste. */
    c.appendChild(reg('RÉCURRENCE', 'chaque semaine'));
    c.appendChild(reg('RAPPEL', 'la veille à 19:00'));
    c.appendChild(reg("C'EST IMPORTANT ?", '· ·· ···'));
    c.appendChild(reg('LA MÉMOIRE', 'réveille tes « en l’air »'));
    /* ⚑ Tom, 13 sept. : LA COULEUR, cinquième réglage du Cercle (lot-CERCLE-COULEUR porte le contrôle). */
    c.appendChild(window._regCouleur ? window._regCouleur(reg) : reg('LA COULEUR', ''));
    var e = el('div','s2-encart');
    var t = el('div','s2-enc-t'); t.textContent = '✦ Ma Parole !';
    var s = el('div','s2-enc-s'); s.textContent = 'importance, récurrence, rappels, mémoire';
    /* ⚑ Q201 (Tom, 11 sept.) : l'encart nomme l'OFFRE, pas son contenu — « ✦ Le Cercle », seul. Il ne périme pas quand
       le contenu bouge. Le sous-titre de contenu du §3.8 n'est plus posé. */
    e.appendChild(t);
    e.addEventListener('click', function(ev){ ev.stopPropagation();
      try{ var b=document.getElementById('openPlusTop'); if(b) b.click(); }catch(_){ } }, true);
    c.appendChild(e);
    return c;
  }

  /* ── L'ENTÊTE (§5) ── */
  function tete(titre, grand){
    var t = el('div','s2-tete'+(grand?' s2-tete-gd':''));
    var a = el('div','s2-titre'); a.textContent = titre||'';
    var f = el('div','s2-fermer'); f.textContent = '✕ FERMER';
    f.addEventListener('click', function(ev){ ev.stopPropagation();
      var c=document.querySelector('#detailPoster>.closeb'); if(c) c.click(); }, true);
    t.appendChild(a); t.appendChild(f);
    return t;
  }

  /* ── LA PAGE, nature par nature. L'ordre est celui de l'inventaire. ── */
  function bati(){
    var dp = document.getElementById('detailPoster');
    var corps = document.getElementById('dpdCorps');
    if(!dp || !corps) return;
    var n = nat(dp);
    var p = (typeof cur!=='undefined') ? cur : null;
    var estNuee = (n==='nuee');
    if(!estNuee && !p) return;

    var liste = corps.querySelector('.s2-liste');
    if(!liste){ liste = el('div','s2-liste'); corps.appendChild(liste); }
    /* TOUT nœud de l'app hébergé dans un réglage rentre chez lui avant qu'on vide la liste.
       Sans ça, innerHTML='' détruisait #dNote et #dCommentInput : la note et les
       commentaires disparaissaient dès le deuxième rendu (constaté en capture). */
    rentre(liste);
    liste.innerHTML = '';

    var titre = '';
    try{ titre = (document.getElementById('dptTitre')||{}).textContent || ''; }catch(_){}
    if(estNuee){ try{ titre = NUE[curNuee]||curNuee||''; }catch(_){ titre=''; } }
    liste.appendChild(tete(titre.trim()));

    var qui = destinataire(p);
    var mv = qui ? ('visible par '+qui) : 'privée — visible par toi seul';
    var mvs = qui ? ('visibles par '+qui) : 'privées — visibles par toi seul';

    if(estNuee){
      /* ── PEAUFINER NUÉE (§5) : description, membres, pièces jointes, commentaires,
           puis le bouton de plantation et la dissolution. Pas de bloc du Cercle : les
           deux écrans de Nuée n'en portent pas. ── */
      var nNom = ''; try{ nNom = NUE[curNuee]||curNuee||''; }catch(_){}
      liste.appendChild(zone('DESCRIPTION', emprunte('nqNote'),
                             'visible par tous les membres', true));
      var mem = '';
      try{ var L = (typeof NUEEMEM!=='undefined' && NUEEMEM[curNuee]) ? NUEEMEM[curNuee] : [];
           /* même règle : les non nommés, moi compris (voir le cadre 86) */
           mem = L.slice(0,2).join(' · ') + (L.length>2 ? (' · +'+(L.length-1)) : ''); }catch(_){}
      liste.appendChild(reg('MEMBRES', mem, {hote:(window._gensFiche ? window._gensFiche('nuee') : emprunte('nqMembers'))}));
      var nf = 0; try{ nf = (document.getElementById('dpFilesNuee')||{}).childElementCount||0; }catch(_){}
      liste.appendChild(reg('PIÈCES JOINTES', nf+' fichier'+(nf>1?'s':''),
        {cls:'s2-vis2', vis:'visibles par le Cercle', hote:emprunte('dpFilesNuee')}));
      liste.appendChild(zone('COMMENTAIRES', invite(emprunte('dCommentInput'),'écris un mot…'),
                             'visibles par les membres du Cercle', true));
      liste.appendChild(bouton('Planter un Promi dans le Cercle', false, function(){
        var b=document.getElementById('nqAddPromi'); if(b) b.click(); }));
      liste.appendChild(reg('DISSOUDRE LE CERCLE', '→', {act:function(){
        var b=document.getElementById('nqDissolve'); if(b) b.click(); }}));
      return;
    }

    var chiche = (n==='chiche');
    /* 1 · à qui */
    /* ⚑ UN PROMI « JE ME PROMETS » EST À SOI PAR DÉFINITION : pas de réglage « à qui » (Tom, 13 sept. 2026).
       Ailleurs, « à qui » et « avec » ouvrent le choix des personnes (lot-GENS) : on ajoute, on retire. */
    var aSoi = !chiche && !p.req && (!p.who || /^moi$/i.test(p.who));
    var _gh = function(k){ return window._gensFiche ? window._gensFiche(k) : emprunte('dWhoInput'); };
    if(!aSoi) liste.appendChild(reg(chiche?'À QUI JE LANCE':'À QUI', (p.who||'moi'),
      {hote:_gh('who')}));
    /* 2 · le compagnon d'un Chiche — vide, il prend le contour pointillé (§3.3) */
    if(chiche) liste.appendChild(reg('AVEC', (p.avec||'personne'),
      {cls:(p.avec?'':'s2-vide'), hote:_gh('avec')}));
    /* 3 · l'échéance — le même contrôle que la phrase, jamais un champ parallèle (§6) */
    var dd = ''; try{ dd = (document.getElementById('dDue')||{}).textContent||''; }catch(_){}
    dd = dd.replace(/^avant\s+/,'');   /* ⚑ v16 : le libellé dit déjà « AVANT » */
    liste.appendChild(reg('AVANT', dd, {hote:(function(){ var h=emprunte('mgDueChips');
      try{ echeanceControle(); }catch(_){ } return h; })()}));
    /* 4 · la Nuée — un Chiche n'en a pas dans l'inventaire */
    if(!chiche){
      var nn=''; try{ nn = p.nuee ? (NUE[p.nuee]||p.nuee) : 'aucune'; }catch(_){ nn='aucune'; }
      liste.appendChild(reg('DANS UN CERCLE', nn, {hote:emprunte('dNueeChips')}));
    }
    /* 5 · la note */
    liste.appendChild(zone('NOTE', emprunte('dNote'), mv));
    /* 6 · les pièces jointes */
    var nf2 = 0; try{ nf2 = (p.files&&p.files.length)||0; }catch(_){}
    liste.appendChild(reg('PIÈCES JOINTES', nf2+' fichier'+(nf2>1?'s':''),
      {cls:'s2-vis2', vis:mvs, hote:emprunte('dpFilesPromi')}));
    /* 7 · les commentaires */
    /* « visible par X · vous pouvez répondre » : les mots de l'inventaire, la cible du §6. */
    var cv = qui ? ('visible par '+qui+', qui peut y répondre')
                 : 'privé — personne d’autre ne le voit';
    liste.appendChild(zone('COMMENTAIRES', invite(emprunte('dCommentInput'),'écris un mot…'), cv, chiche));
    /* 8 · relancer — n'existe que sur la fiche, jamais sur la page + (§6) */
    var rb = document.getElementById('actRelance');
    /* la relance vise LA PERSONNE, jamais la Nuée : c'est la cible que l'app calcule déjà
       pour #actRelance. « RELANCER FAMILLE » était un contresens (constaté en capture). */
    var pers = (p.from && p.from!=='moi') ? p.from
             : ((p.who && p.who!=='moi' && p.who!=='le groupe') ? p.who : null);
    if(rb && rb.style.display!=='none' && pers)
      liste.appendChild(reg('RELANCER '+pers.toUpperCase(), '→', {act:function(){ rb.click(); }}));
    /* 9 · le bloc du Cercle */
    liste.appendChild(cercle());
    /* 10 · supprimer */
    var _rs=reg(chiche?'SUPPRIMER CE CHICHE':'SUPPRIMER CE PROMI', '',
      {act:function(){ if(window._v16SupprimerPromi) window._v16SupprimerPromi(p); }});
    _rs.classList.add('v16-danger'); liste.appendChild(_rs);
    /* v92 : Ramage prépare dès maintenant le départ de cette parole (la confirmation seule lui laissait 1,2 s pour 2 s de film) */
    try{ if(window._simPrepare && p && !p.draft){ var _pid=p.id; setTimeout(function(){ try{ window._simPrepare(null,[_pid]); }catch(_){ } },300); } }catch(_){ }
  }
  window._s2Bati = bati;
  /* ── LES BRIQUES, EXPOSÉES POUR LA PAGE + ──
     La page + porte le MÊME Peaufiner que la fiche : mêmes libellés, même ordre, mêmes
     cotes (§3.3, §3.4, §5). On expose les briques, on ne les duplique pas — une seule
     grammaire de réglage existe dans le produit, comme pour l'onde et pour la phrase. */
  window._s2Briques = {reg:reg, zone:zone, bouton:bouton, tete:tete, cercle:cercle,
                       emprunte:emprunte, rentre:rentre, invite:invite,
                       destinataire:destinataire, el:el};

  /* ── L'OUVERTURE. §6 : la barre est fixée en bas et ne bouge jamais ; les réglages
       défilent au-dessus d'elle. Rien ne monte, rien ne recouvre. ── */
  function ouvre(v){
    var dp = document.getElementById('detailPoster'); if(!dp) return;
    if(v){ bati(); dp.classList.add('s2-ouv'); dp.scrollTop = 0;
           var c=document.getElementById('dpdCorps'); if(c) c.scrollTop = 0; }
    else { dp.classList.remove('s2-ouv'); }
  }
  window._s2Ouvre = ouvre;

  function branche(){
    var tog = document.querySelector('#dpDetails .dpd-tog');
    if(!tog || tog._s2) return;
    tog._s2 = true;
    tog.addEventListener('click', function(ev){
      var dp = document.getElementById('detailPoster'); if(!dp) return;
      /* le rond Partager garde sa fonction : on ne le détourne pas */
      if(ev.target.closest && ev.target.closest('.dpd-part')) return;
      ouvre(!dp.classList.contains('s2-ouv'));
      ev.stopPropagation();
    }, true);
  }

  /* ── LES RÉGLAGES GÉNÉRAUX (§5) : l'encart du Cercle y était un DÉGRADÉ animé posé seul.
       L'inventaire le montre au centre d'un bloc de quatre réglages floutés. On construit le
       bloc autour de l'encart existant — il garde sa fonction (il ouvre Le Cercle). ── */
  function cercleReglages(){
    var enc = document.getElementById('openPlusTop'); if(!enc) return;
    if(enc.parentNode && enc.parentNode.classList.contains('s2-cercle')) return;
    var c = el('div','s2-cercle');
    enc.parentNode.insertBefore(c, enc);
    /* ⚑ v16 (Tom) : « les réglages du Cercle quittent les Réglages — ils appartiennent à un Promi,
       c'est le §5. Ils restent dans Peaufiner. » L'encart reste seul : il ouvre Le Cercle. */
    c.classList.add('v16-seul');
    c.appendChild(enc);
  }
  window._s2Reglages = cercleReglages;
  try{ cercleReglages(); }catch(e){}
  document.addEventListener('click', function(){ try{ cercleReglages(); }catch(e){} }, true);

  /* LE BRANCHEMENT. Première version : j'enveloppais window._ficheTout — il n'est JAMAIS
     appelé (la section 1 appelle sa fonction locale « tout », pas la globale). Résultat
     mesuré : le premier appui sur la barre ne faisait rien. On passe donc par un écouteur
     DÉLÉGUÉ sur le document, qui n'a besoin d'aucun branchement au bon moment, et on
     rebâtit la page après chaque pose de fiche en enveloppant _fichePose (lui, est appelé). */
  document.addEventListener('click', function(ev){
    var tg = ev.target.closest && ev.target.closest('#dpDetails .dpd-tog');
    if(!tg) return;
    if(ev.target.closest('.dpd-part')) return;   /* le rond Partager garde sa fonction */
    var dp = document.getElementById('detailPoster'); if(!dp) return;
    ouvre(!dp.classList.contains('s2-ouv'));
    ev.stopPropagation();
  }, true);
  var _pose = window._fichePose;
  window._fichePose = function(){
    var r = _pose ? _pose.apply(this, arguments) : undefined;
    try{ requestAnimationFrame(function(){
      var dp=document.getElementById('detailPoster');
      if(dp && dp.classList.contains('s2-ouv')) bati(); }); }catch(e){}
    return r;
  };
  try{ branche(); }catch(e){}
  /* fermer la fiche referme la page */
  document.addEventListener('click', function(ev){
    var c = ev.target.closest && ev.target.closest('#detailPoster>.closeb');
    if(c) ouvre(false);
  }, true);
})();
