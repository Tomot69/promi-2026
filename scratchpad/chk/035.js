
/* FICHE au moodboard — DOM : texte « À TENIR », FERMER croix SVG, span Peaufiner,
   enveloppe du geste, carte message + pastilles (corps), Aura relogée sous
   Peaufiner, tracé de la fiche tenue. Hooké après _fichePose (idempotent). */
(function(){
  function el(t,c){var e=document.createElement(t);if(c)e.className=c;return e;}
  var SVG_REP='<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.7A8.5 8.5 0 0 1 12.5 3 8.38 8.38 0 0 1 21 11.5z"/></svg>';
  var SVG_NOTE='<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>';
  var SVG_FILE='<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M13 2v7h7"/></svg>';
  var SVG_PEOPLE='<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>';
  function rel(d){try{var s=(Date.now()-new Date(d).getTime())/1000;if(s<3600)return "à l'instant";if(s<172800)return 'hier';return Math.floor(s/86400)+' j';}catch(e){return '';}}
  window._lot7Fiche=function(){
    var dp=document.getElementById('detailPoster'); if(!dp) return;
    var atenir=dp.classList.contains('f-atenir'), tenue=dp.classList.contains('f-tenue'), encours=dp.classList.contains('f-encours');
    if(!atenir && !tenue && !encours) return;
    /* #5 garde-fou : une NUÉE jeune a aussi le statut f-encours, mais elle a son
       propre rendu (renderNueeDetail : membres, harmonie, fil). On ne lui plaque PAS
       le traitement de fiche Promi (« EN COURS », carte commentaire, geste). */
    if(dp.classList.contains('dp-nuee') || dp.classList.contains('dp-mode-nuee')) return;
    /* 1 · « À TENIR / TENUE / EN COURS » majuscules littérales (#5 : l'en-cours
       n'était pas géré → fiche cassée, sans structure ni bitonal). */
    /* ⚑ LA LIGNE D'ÉTAT D'UNE FICHE PORTE SON TEMPS — le mot d'état, puis « · », puis
       ce qu'il reste à savoir. Les six cadres de fiche l'écrivent tous ainsi :
           cadre 34/48  TENUE · 12 MARS          cadre 46  EN COURS · DEPUIS LE 4 AVRIL
           cadre 36     À TENIR · DIMANCHE       cadre 42  TENU À DEUX · 3 AOÛT
           cadre 44     À TENIR · DANS 2 JOURS   cadre 62  GARDÉ DE CÔTÉ · 2 AVRIL
       L'app n'écrivait que le mot. Pour « à tenir », le temps existe déjà et sort de
       `motDuTemps` — les mots sont ceux du produit (« dimanche », « demain », « 12 mars »).
       Pour une parole TENUE ou EN COURS, l'app ne garde AUCUNE DATE : elle n'a que des
       échéances en jours. On lit donc `p.leJour` quand il existe, et on n'écrit rien
       sinon — jamais une date fabriquée. ⚠ `leJour` est une donnée du Promi qui manquait ;
       le jeu de démonstration la porte, lue dans les cadres. À valider (QUESTIONS · Q81). */
    var q=document.getElementById('dptQuand');
    if(q){
      var mot = tenue ? 'TENUE' : (encours ? 'EN COURS' : 'À TENIR');
      var suite = '';
      try{
        var pq = (typeof cur!=='undefined') ? cur : null;
        if(pq && pq.leJour) suite = pq.leJour;
        else if(atenir && window.motDuTemps && pq){
          /* ⚠ `motDuTemps` COURT-CIRCUITE SUR L'ÉTAT : pour `status:'rate'` il rend
             « à tenir » et ne regarde jamais l'échéance. On lui repose donc la question
             sur l'échéance seule — mêmes mots, même table, aucune duplication. */
          var m0 = motDuTemps({due: pq.due, status: 'encours'});
          if(m0 && m0.mot && m0.mot!=='un jour' && m0.mot!=='à tenir') suite = m0.mot;
        }
      }catch(_){}
      q.textContent = mot + (suite ? (' · ' + ('' + suite).toUpperCase()) : '');
    }
    /* ⚑ L'EYEBROW D'UNE FICHE PORTE UNE CAPITALE, ET IL EST D'UN SEUL TON.
       Cadre 48 : « À moi », Bricolage 600 / 21, couleur d'état, UN seul nœud — pas de
       « à » pâle suivi d'un nom en gras. Les listes, elles, gardent la minuscule :
       le cadre 72 écrit « à moi », le cadre 76 aussi. C'est la fiche qui capitalise. */
    var qw=document.getElementById('dptQui');
    if(qw && typeof cur!=='undefined' && cur){
      var _m;
      if(cur.draft) _m='Gardé de côté';
      else {
        var _w=(cur.who||'').trim();
        _m = (!_w || _w.toLowerCase()==='moi') ? 'À moi' : (window._aQui ? window._aQui(_w,true) : ('À '+_w));
        /* ⚠ « · avec X » NE SE RÉPÈTE PAS. Cadre 42 « À Marion · avec Rachel » : le
           compagnon est un TIERS. Cadre 56 « À Marion » tout court, alors que la parole
           est TENUE À DEUX — c'est Marion elle-même qui l'a relevée. */
        if(cur.chiche && cur.avec && cur.avec!==_w) _m += ' · avec '+cur.avec;
      }
      if(qw.textContent!==_m) qw.textContent=_m;
    }
    /* 1b · titre long → 26px (le moodboard : court 34, long 26 sur deux lignes) */
    var titre=document.getElementById('dptTitre');
    if(titre){ titre.classList.remove('dpt-long');
      var lh=parseFloat(getComputedStyle(titre).lineHeight)||36;
      if(titre.offsetHeight > lh*1.5) titre.classList.add('dpt-long'); }
    /* 2 · FERMER = croix svg + mot */
    var cb=dp.querySelector('.closeb');
    if(cb && !cb.querySelector('svg'))
      cb.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round"><path d="M6 6 L18 18 M18 6 L6 18"/></svg><span>FERMER</span>';
    /* 3 · Peaufiner en span 17/800 */
    var tog=document.getElementById('dpdTog');
    if(tog && !tog.querySelector('.dpd-mot')){
      var arr=[]; tog.childNodes.forEach(function(n){if(n.nodeType===3 && n.textContent.trim())arr.push(n);});
      arr.forEach(function(n){n.textContent='';});
      var mot=el('span','dpd-mot'); mot.textContent='Peaufiner'; tog.insertBefore(mot, tog.firstChild);
    }
    /* 4 · enveloppe du geste (à tenir) */
    var tz=document.getElementById('tenirZone');
    var env=dp.querySelector('.geste-env');
    if((atenir||encours) && tz){ if(!env) env=el('div','geste-env'); if(tz.parentElement!==env) env.appendChild(tz); }
    /* 5 · corps : carte message + pastilles */
    var corps=document.getElementById('dpCorps');
    if(!corps){ corps=el('div'); corps.id='dpCorps'; }
    corps.innerHTML='';
    var msg=el('div'); msg.id='dpMsg';
    var head=el('div','dpm-head'), txt=el('div','dpm-txt');
    var last=(typeof cur!=='undefined'&&cur&&cur.comments&&cur.comments.length)?cur.comments[cur.comments.length-1]:null;
    if(last){ head.textContent=((last.by||'moi')+', '+rel(last.d)).toUpperCase(); txt.textContent=last.t; }
    else if(typeof cur!=='undefined'&&cur&&cur.note){ head.textContent='TA NOTE'; txt.textContent=cur.note; }
    else {
      /* #6 : PAS de commentaire, PAS de note — on ne demande pas de « répondre » à
         rien. Le bloc INVITE à écrire le premier mot : plus de faux en-tête ni de
         « réponds pour lancer l'échange ». */
      head.style.display='none'; txt.style.display='none';
    }
    /* ⚠ SANS POINTS DE SUSPENSION SUR LA FICHE. Le cadre 46 écrit « écris un mot », tout
       court ; les points appartiennent au champ COMMENTAIRES de Peaufiner (cadre 80), où
       ils marquent une saisie. Ici c'est une invitation, pas un champ. */
    var rep=el('div','dpm-rep'); rep.innerHTML=SVG_REP+'<span>'+(last?'répondre':'écris un mot')+'</span>';
    msg.appendChild(head); msg.appendChild(txt); msg.appendChild(rep); msg.appendChild(el('div','dpm-filet'));
    corps.appendChild(msg);
    var past=el('div'); past.id='dpPast';
    function pz(s,l){var d=el('div','dp-pz'); d.innerHTML=s+'<span>'+l+'</span>'; return d;}
    past.appendChild(pz(SVG_NOTE,'note'));
    past.appendChild(pz(SVG_FILE, String((typeof cur!=='undefined'&&cur&&cur.files&&cur.files.length)||1)));
    if(typeof cur!=='undefined'&&cur&&cur.nuee&&typeof NUE!=='undefined'&&NUE[cur.nuee]) past.appendChild(pz(SVG_PEOPLE, NUE[cur.nuee]));
    corps.appendChild(past);
    /* 6 · Les disques EN TÊTE DE CORPS (Décision Tom) : la rangée est visible à
       l'ouverture, juste sous la tête — elle n'est plus reléguée sous Peaufiner.
       (Placement fait dans mainKids ci-dessous, entre la tête et le corps.) */
    var aura=document.getElementById('dAura');
    /* 7 · tracé de la fiche tenue : LE VRAI GESTE (sa signature), pas un chemin
       générique. #4 : on écrivait ici un chemin HARDCODÉ qui écrasait cur.trace
       (les points réellement tracés au doigt, sauvés à la tenue). On rend le vrai
       tracé, normalisé dans le viewBox 300×62, en courbes quadratiques (CLAUDE §5). */
    var tr=document.getElementById('dpTrace');
    if(tenue && tr){
      var svg=tr.querySelector('svg'); if(svg) svg.setAttribute('viewBox','0 0 300 62');
      var path=tr.querySelector('path');
      if(path){
        var _tp=(typeof cur!=='undefined' && cur && cur.trace && cur.trace.length>1) ? cur.trace : null;
        if(_tp){
          var _xs=_tp.map(function(p){return p.x;}), _ys=_tp.map(function(p){return p.y;});
          var _x0=Math.min.apply(null,_xs), _x1=Math.max.apply(null,_xs);
          var _y0=Math.min.apply(null,_ys), _y1=Math.max.apply(null,_ys);
          var _lw=Math.max(1,_x1-_x0), _lh=Math.max(1,_y1-_y0);
          var _k=Math.min(280/_lw, 46/_lh);
          var _ox=10+(280-_lw*_k)/2, _oy=(62-_lh*_k)/2;
          var _PX=function(p){return (p.x-_x0)*_k+_ox;}, _PY=function(p){return (p.y-_y0)*_k+_oy;};
          var _d='M'+_PX(_tp[0]).toFixed(1)+','+_PY(_tp[0]).toFixed(1);
          for(var _i=1;_i<_tp.length;_i++){
            var _xc=(_PX(_tp[_i-1])+_PX(_tp[_i]))/2, _yc=(_PY(_tp[_i-1])+_PY(_tp[_i]))/2;
            _d+=' Q'+_PX(_tp[_i-1]).toFixed(1)+','+_PY(_tp[_i-1]).toFixed(1)+' '+_xc.toFixed(1)+','+_yc.toFixed(1);
          }
          _d+=' L'+_PX(_tp[_tp.length-1]).toFixed(1)+','+_PY(_tp[_tp.length-1]).toFixed(1);
          path.setAttribute('d', _d);
        } else if(!path.getAttribute('d')){
          /* aucune trace enregistrée (Promi importé/légataire) : chemin neutre discret */
          path.setAttribute('d','M20,44 C56,10 96,52 138,28 C176,6 220,46 278,20');
        }
        path.setAttribute('stroke-width','4.6');
      }
      corps.insertBefore(tr, corps.firstChild);
    }
    /* 8 · PEAUFINER FIXE — un seul écran continu :
         [dpMain : tête + corps + geste, remplit le 1er écran] · [barre COLLANTE (sticky top)]
         · [réglages EN DESSOUS]. La barre part du bas, colle en haut quand on descend,
         les réglages se découvrent sous elle. Rien ne remonte, rien ne recouvre. */
    var tete=document.getElementById('dpTete');
    var det=document.getElementById('dpDetails');       // enveloppe = la BARRE (dpdTog)
    var corpsDet=document.getElementById('dpdCorps');   // les RÉGLAGES
    var main=document.getElementById('dpMain');
    if(!main){ main=el('div'); main.id='dpMain'; }
    /* tête → DISQUES (visibles à l'ouverture) → corps → geste */
    var mainKids=[tete]; if(aura) mainKids.push(aura); mainKids.push(corps); if((atenir||encours) && env) mainKids.push(env);
    mainKids.forEach(function(e){ if(e) main.appendChild(e); });
    dp.appendChild(main);
    if(det) dp.appendChild(det);              // la barre Peaufiner (collante en haut)
    if(corpsDet) dp.appendChild(corpsDet);    // les réglages, EN DESSOUS de la barre
  };
  var orig=window._fichePose;
  window._fichePose=function(){ if(orig) orig.apply(this,arguments); try{ window._lot7Fiche(); }catch(e){} };
})();
