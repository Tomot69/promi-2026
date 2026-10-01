
/* ⚑ LOT FICHE-PERSONNE — voir le commentaire du style. `openPerson` est redéfinie ici ; elle garde le correctif
   `avec` (lot-PERSONNE-AVEC) et ne remplit plus rien de l'ancienne fiche. */
(function(){ try{
  /* ⚑ 21 sept. — posée sur la page comme celle de l'Aura : elle bascule (§3). */
  function _cl(){ try{return !!document.querySelector('#device.light,.device.light,.frame.light');}catch(e){return false;} }
  var MENTHE='#00341A', PERI='#291547', TERRA='#DD4D23';   /* ⚑ 22 sept. : les trois, sans bascule */
  function $i(id){ return document.getElementById(id); }
  function el(t,c,x){ var e=document.createElement(t); if(c) e.className=c; if(x!=null) e.textContent=x; return e; }
  function clair(){ var d=$i('device'), f=document.querySelector('.frame');
    return !!((d&&d.classList.contains('light'))||(f&&f.classList.contains('light'))); }
  /* les paroles partagées : où la personne est « à qui », « de qui » OU « avec » (le compagnon d'un Chiche) */
  function paroles(nom){ try{ return promises.filter(function(p){ return p && !p.draft && (p.who===nom||p.from===nom||p.avec===nom); }); }catch(e){ return []; } }
  function parts(L){ var n=L.length, t=0, e=0, r=0;
    L.forEach(function(p){ if(p.status==='tenu') t++; else if(p.status==='encours') e++; else r++; });
    return n ? [t/n, e/n, r/n] : [0,0,0]; }
  /* ── LE NOYAU (§2.9) — piste neutre, arcs d'état à bout franc, l'image de la personne au centre ── */
  function noyau(nom, pp){
    var w=el('div','ps-ny'), d=58, lw=6, r=(d-lw)/2, C=2*Math.PI*r, nb=pp.filter(function(v){return v>0;}).length;
    var s='<svg viewBox="0 0 58 58" width="58" height="58"><circle cx="29" cy="29" r="'+r+'" fill="none" stroke="'+(clair()?'#E0D0B2':'#372D1E')+'" stroke-width="'+lw+'"/>';
    var a=0, cols=[MENTHE,PERI,TERRA];
    pp.forEach(function(f,i){ if(f<=0) return; var l=f*C-(nb>1?2:0);
      s+='<circle class="ps-arc" data-part="'+i+'" cx="29" cy="29" r="'+r+'" fill="none" stroke="'+cols[i]+'" stroke-width="'+lw+'" stroke-dasharray="'+l.toFixed(2)+' '+(C-l).toFixed(2)+'" stroke-dashoffset="'+(-a).toFixed(2)+'" transform="rotate(-90 29 29)"/>';
      a+=f*C; });
    w.innerHTML=s+'</svg>';
    var v=el('div','ps-vis'), moi=(typeof _isMe==='function')&&_isMe(nom);
    if(moi && typeof USER!=='undefined' && USER && USER.photo) v.style.background='center/cover url("'+USER.photo+'")';
    else { try{ v.style.background=_blobBg(moi?('u'+USER.seed):nom); }catch(e){} }
    w.appendChild(v); return w;
  }
  function legende(){ var g=el('div','ps-lg');
    [['tenues',MENTHE],['en cours',PERI],['à tenir',TERRA]].forEach(function(q){ var s=el('span'), i=el('i'); i.style.background=q[1];
      s.appendChild(i); s.appendChild(document.createTextNode(q[0])); g.appendChild(s); }); return g; }
  /* ── LES VRAIES CARTES DE L'INDEX — le moteur du lot S4 (`_s4Index`) est prêté le temps d'un appel : il bâtit
     dans `#indexList` ; on lui prête ce nom pour la boîte de la fiche, puis on rend TOUT à l'identique (l'id, les
     entrées, le cache). Aucune variante locale de la carte (§5). ── */
  var MOTS_ETAT=/^(TENUE?S?|TENU À DEUX|À TENIR|EN COURS|LANCÉ|RELEVÉ|À RELEVER|GARDÉ DE CÔTÉ|DEMANDÉ|EN ATTENTE)$/i;
  function cartes(box, L){
    if(!L.length || typeof window._s4Index!=='function') return 0;
    var vraie=$i('indexList'), sE=window._s4Entrees, sF=window._s4Frais, sV=window._s4Vide;
    try{
      if(vraie) vraie.id='indexList-prete'; box.id='indexList';
      window._s4Entrees=L.map(function(p){ return {id:p.id}; }); window._s4Frais=false;
      window._s4Index();
    }finally{
      box.id='psCartes'; if(vraie) vraie.id='indexList';
      window._s4Entrees=sE; window._s4Frais=sF; window._s4Vide=sV;
    }
    /* la ligne du bas : L'ÉTAT N'EST PLUS ÉCRIT — le trait le dit (Tom) ; on garde le temps quand l'app le sait,
       et la Nuée de la parole (l'Index, qui range ces paroles sous leur Nuée, n'a jamais eu à l'écrire) */
    var cs=[].slice.call(box.querySelectorAll('.s4-carte')), bas=0;
    cs.forEach(function(c,i){ var p=L[i], et=c.querySelector('.s4-et'); if(!p) return;
      c.setAttribute('data-pid', p.id);
      if(et){ var seg=(et.textContent||'').split(' · ').map(function(s){return s.trim();}).filter(function(s){ return s && !MOTS_ETAT.test(s); });
        if(p.nuee){ var nn=(typeof NUE!=='undefined' && NUE[p.nuee]) || p.nuee; seg.push(String(nn).toUpperCase()); }
        et.textContent=seg.join(' · '); }
      bas=Math.max(bas, c.offsetTop+c.offsetHeight); });
    return bas;
  }
  /* ── LES DEUX GESTES — la page +, la personne DÉJÀ choisie (le modèle : openCreateForNuee) ── */
  function planter(nom, chiche){
    try{
      var cs=$i('createSheet'); if(!cs) return;
      try{ selNuee=null; }catch(_){}
      window.createKind = chiche ? 'chiche' : 'promi';
      var pf=$i('promiForm'), nf=$i('nueeForm'), df=$i('draftForm');
      if(pf) pf.style.display='block'; if(nf) nf.style.display='none'; if(df) df.style.display='none';
      openSheet(cs);
      try{ if(window._csBuildFlex) window._csBuildFlex(); }catch(_){}
      cs.setAttribute('data-kind', window.createKind); cs.classList.remove('cs-nuee');
      [].forEach.call(cs.querySelectorAll('.tile'), function(x){ x.classList.toggle('on', x.dataset.kind===window.createKind); });
      var qui=function(){
        window._csSens = chiche ? 'chiche' : 'faire';
        if(window._phrase){ window._phrase.sens = chiche ? 'chiche' : 'faire'; window._phrase.faireAutre=false; window._phrase.qui=nom; }
        window.newWhoSel=[nom]; var fw=$i('fWho'); if(fw) fw.value=nom;
      };
      qui();
      try{ if(typeof buildCreateNuees==='function') buildCreateNuees(); if(typeof buildWhoChips==='function') buildWhoChips(); }catch(_){}
      try{ if(window._phraseRendu) window._phraseRendu(); if(window.renderCsDalle){ window.renderCsDalle(); setTimeout(window.renderCsDalle,240); }
           if(window._csColorLabels) window._csColorLabels(); }catch(_){}
      setTimeout(function(){ try{ if(window._csVersPhrase) window._csVersPhrase(); qui(); if(window._phraseRendu) window._phraseRendu(); }catch(_){} }, 140);
    }catch(e){}
  }
  /* ── LA FICHE ── */
  function rangeFiche(){ var c=$i('psCadre'); if(c && c.parentNode) c.parentNode.removeChild(c); }
  (window._rangeurs = window._rangeurs || []).push(rangeFiche);
  /* le cadre se pose sur #device, dans le repère de la fiche, transformation d'ouverture retirée */
  function poser(sh, cad){
    var dv=$i('device'); if(!dv||!sh||!cad) return;
    var rd=dv.getBoundingClientRect(), rs=sh.getBoundingClientRect(), s=rd.width/390||1, tx=0, ty=0;
    try{ var m=new DOMMatrix(getComputedStyle(sh).transform); tx=m.m41; ty=m.m42; }catch(_){}
    cad.style.setProperty('left', ((rd.left-rs.left)/s + tx + sh.scrollLeft)+'px', 'important');
    cad.style.setProperty('top',  ((rd.top -rs.top )/s + ty + sh.scrollTop )+'px', 'important');
  }
  window.openPerson = function openPerson(nom){
    if(!nom) return;
    var sh=$i('personSheet'); if(!sh) return;
    var nm=$i('psName'); if(nm){ nm.textContent=nom; nm.style.setProperty('font-weight','700','important'); }
    openSheet(sh);                       /* closeAll passe ici, et son rangeur retire le cadre d'avant */
    try{ sh.scrollTop=0; }catch(_){}
    var L=paroles(nom), T=L.filter(function(p){ return p.status==='tenu'; });
    var cad=el('div'); cad.id='psCadre'; cad.setAttribute('data-fiche', nom);
    var col=el('div','ps-col'); col.setAttribute('data-defile','1');
    var pile=el('div','ps-pile'); col.appendChild(pile); cad.appendChild(col); sh.appendChild(cad);
    var pp=parts(L), n=noyau(nom, pp); n.style.left='24px'; n.style.top='124px'; pile.appendChild(n);
    if(L.length){ var g=legende(); g.style.left='100px'; g.style.top='145px'; pile.appendChild(g); }
    var y=124+58+32;
    if(T.length){
      var h=el('div','ps-h','Tenu ensemble'); h.style.left='24px'; h.style.top=y+'px'; pile.appendChild(h); y+=30;
      T.forEach(function(p,i){ var c=el('div','ps-c'); c.style.left=(24+(i%3)*117)+'px'; c.style.top=(y+Math.floor(i/3)*101)+'px';
        c.setAttribute('data-pid', p.id);
        var bx=el('div','ps-bx'), cv=document.createElement('canvas');
        /* dans le monde de SA plantation — ⚑ v29 : rendue à la taille de sa boîte (105 × 56), affichée 1:1 */
        try{ var _dp=Math.min(2,window.devicePixelRatio||1), _s=window._rendDalle(p.id, 105*_dp, 56*_dp);   /* ⚑ v34 : la fiche d'une personne suit le Studio (Tom) */
             if(_s){ cv.width=_s.width; cv.height=_s.height; cv.style.setProperty('width',(_s.width/_dp)+'px','important'); cv.style.setProperty('height',(_s.height/_dp)+'px','important'); cv.style.setProperty('max-width','none','important'); cv.style.setProperty('max-height','none','important');   /* ⚑ v32 : en ligne, important — même défaut que « Ce que tu as tenu » */
                     cv.getContext('2d').drawImage(_s,0,0); } }catch(_){}
        bx.appendChild(cv); c.appendChild(bx); c.appendChild(el('span',null,p.title||'')); pile.appendChild(c); });
      y+=Math.ceil(T.length/3)*101-12+32;
    }
    if(L.length){
      var h2=el('div','ps-h','Ce que tu partages avec '+nom); h2.style.left='24px'; h2.style.top=y+'px'; pile.appendChild(h2); y+=30;
      var box=el('div','ps-cartes'); box.id='psCartes'; box.style.top=y+'px'; pile.appendChild(box);
      var b=cartes(box, L); box.style.height=b+'px'; y+=b;
    }
    var bt=Math.max(760, y+28); if(bt+62>822 && bt<844) bt=844;     /* entiers à l'ouverture, ou franchement sous le pli */
    [['+ Planter un Promi',false,24],['+ Lancer un Chiche',true,199]].forEach(function(q){
      var e=el('div','ps-bt',q[0]); e.setAttribute('role','button'); e.setAttribute('data-geste', q[1]?'chiche':'promi');
      e.style.left=q[2]+'px'; e.style.top=bt+'px';
      e.onclick=function(){ planter(nom, q[1]); }; pile.appendChild(e); });
    pile.style.height=(bt+62+22)+'px';
    poser(sh, cad);
    var k=0; (function repose(){ poser(sh, cad); if(++k<40) requestAnimationFrame(repose); })();
    /* LA COMPOSITION EST PUBLIÉE (§7 : on compare la composition, pas la peinture) */
    window._ficheComp={nom:nom, ids:L.map(function(p){return p.id;}), tenues:T.map(function(p){return p.id;}), parts:pp};
  };
}catch(e){} })();
