
(function(){
  function phraseHasContent(){ try{ var Pp=window._phrase||{};
    var ft=document.getElementById('fTitle'); if(ft && ft.value && ft.value.trim()) return true;
    if(Pp.titre && (''+Pp.titre).trim()) return true;
    if(Pp.quand && Pp.quand!=='un jour') return true;
    if(typeof selNuee!=='undefined' && selNuee) return true;
    if(Pp.qui && Pp.qui!=='Moi' && Pp.qui!=='tout le monde') return true;
    return false; }catch(e){ return false; } }
  function nueeHasContent(){ try{ var n=document.getElementById('nName'); return !!(n && n.value && n.value.trim()); }catch(e){ return false; } }
  window._majGardeCote=function(){ try{
    var cs=document.getElementById('createSheet'); if(!cs) return;
    var k=cs.getAttribute('data-kind');
    var gcP=document.getElementById('gcPromi'), gcN=document.getElementById('gcNuee');
    /* ⚑ v16 : sur un gardé de côté REPRIS, le lien créait un second brouillon (l'ancien restait) — il sort. */
    var _rep = (window._brouillonRepris!=null);
    if(gcP) gcP.style.display=(k==='promi' && phraseHasContent() && !_rep) ? 'inline-flex' : 'none';
    if(gcN) gcN.style.display=(k==='nuee' && nueeHasContent() && !_rep) ? 'inline-flex' : 'none';
  }catch(e){} };
  function quandToDue(q){ return {'demain':1,'5 jours':5,'2 semaines':14,'ce mois-ci':30,'un jour':30}[q]||30; }
  window._gardeCote=function(kind){ try{
    var np, titre='';
    if(kind==='nuee'){
      var nm=((document.getElementById('nName')||{}).value||'').trim(); if(!nm) return; titre=nm;
      np=P(nm,'le groupe',30,2,'encours',null,'moi'); np.draft=true; np.dk='nuee';
      try{ np.nueeMembers=(window.newNueeMembers||[]).slice(); }catch(_){}
    } else {
      var Pp=window._phrase||{};
      titre=((Pp.titre||(document.getElementById('fTitle')||{}).value||'')+'').trim();
      var w=(Pp.qui&&Pp.qui!=='tout le monde')?Pp.qui:'moi';
      var nu=(typeof selNuee!=='undefined'&&selNuee)||null;
      np=P(titre||'(sans titre)',w,quandToDue(Pp.quand),2,'encours',nu,'moi'); np.draft=true; np.dk=nu?'innuee':'solo';
      np.phraseSens=Pp.sens||'faire';
      try{ var _n=document.getElementById('fNote'); if(_n&&_n.value.trim()) np.note=_n.value.trim(); }catch(_){}
    }
    try{ if(typeof computeBox==='function'){ computeBox(); if(typeof box!=='undefined'&&box){ np.x=box.x+box.w/2; np.y=box.y+box.h/2; np.tx=np.x; np.ty=np.y; } } }catch(_){}
    promises.push(np);
    (window._toileDefer=window._toileDefer||[]).push((function(np){return function(){try{if(window.Toile&&window.Toile.addPromi)window.Toile.addPromi(np.id);}catch(e){}};})(np));
    try{ var _q=window._toileDefer; window._toileDefer=null; _q.forEach(function(fn){try{fn();}catch(_){}}); }catch(_){}
    try{ if(typeof feedAdd==='function') feedAdd('added','Tu as gardé « '+(titre||np.title)+' » de côté',{pid:np.id}); }catch(_){}
    try{ if(typeof toast==='function') toast('gardé de côté — dans l\'Index'); }catch(_){}
    try{ if(typeof selNuee!=='undefined') selNuee=null; window._phrase={sens:'faire',qui:'Moi',titre:'',quand:'un jour'}; var ft=document.getElementById('fTitle'); if(ft)ft.value=''; }catch(_){}
    try{ if(typeof closeAll==='function') closeAll(); }catch(_){}
    try{ if(typeof render==='function') render(); if(typeof caption==='function') caption(); if(window.syncAll) window.syncAll(); }catch(_){}
  }catch(e){} };
  /* REPRISE : rouvrir un brouillon dans la PAGE +, dans son état, prêt à planter. */
  window.reprendreBrouillon=function(p){ try{
    if(!p) return;
    var cs=document.getElementById('createSheet'); if(!cs) return;
    /* ⚑ ON REPREND UN GARDÉ DE CÔTÉ — et l'écran doit le dire (cadres 26/27).
       `window._ppGarde` était LU par les cotes de la page + (`e.garde`) et POSÉ nulle part :
       l'écran de reprise sortait donc avec l'aplat de nature d'une page + ordinaire, et
       SANS sa ligne « GARDÉ DE CÔTÉ · RIEN N'EST PROMIS ». Les deux défauts n'en font
       qu'un — vu au duo, deux thèmes. Un gardé de côté n'a pas d'aplat (Q83 : rien n'a été
       promis, donc rien n'est posé), et il porte son mot. On pose le drapeau ici, à
       l'endroit unique qui reprend un brouillon. */
    window._ppGarde = true;
    var nature=(p.dk==='nuee')?'nuee':'promi';
    try{ if(typeof closeAll==='function') closeAll(); }catch(_){}
    try{ if(typeof selNuee!=='undefined') selNuee=(p.dk==='innuee'&&p.nuee)?p.nuee:null; }catch(_){}
    if(nature==='nuee'){
      try{ window.newNueeMembers=(p.nueeMembers||[]).slice(); }catch(_){}
      var nn=document.getElementById('nName'); if(nn) nn.value=p.title||'';
    } else {
      var dueQ={1:'demain',5:'5 jours',14:'2 semaines',30:'ce mois-ci'}[p.due]||'un jour';
      window._phrase={sens:(p.phraseSens||'faire'),qui:(p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:'Moi',titre:(p.title||''),quand:dueQ};
      var ft=document.getElementById('fTitle'); if(ft) ft.value=p.title||'';
      var fn=document.getElementById('fNote'); if(fn) fn.value=p.note||'';
    }
    /* on marque le brouillon repris : planter le CONVERTIT (retire le draft) */
    window._brouillonRepris=p.id;
    var pf=document.getElementById('promiForm'), nf=document.getElementById('nueeForm'), df=document.getElementById('draftForm');
    if(pf)pf.style.display=(nature==='promi')?'block':'none';
    if(nf)nf.style.display=(nature==='nuee')?'block':'none';
    if(df)df.style.display='none';
    try{ createKind=nature; }catch(_){}
    if(typeof openSheet==='function') openSheet(cs);
    try{ if(window._csBuildFlex)window._csBuildFlex(); }catch(_){}
    try{ cs.setAttribute('data-kind',nature); if(nature==='promi'&&selNuee)cs.classList.add('cs-nuee'); else cs.classList.remove('cs-nuee');
      document.querySelectorAll('#createSheet .tile').forEach(function(x){x.classList.toggle('on',x.dataset.kind===nature);});
      if(typeof buildCreateNuees==='function')buildCreateNuees();
      if(nature==='promi'){ if(window._phraseRendu)window._phraseRendu(); } else { if(window._nueePhraseRendu)window._nueePhraseRendu(); }
      if(window.renderCsDalle)window.renderCsDalle();
    }catch(_){}
    setTimeout(function(){ try{
      if(nature==='promi' && window._phrase){ window._phrase.titre=(p.title||''); if(window._phraseRendu)window._phraseRendu(); }
      if(window._csVersPhrase)window._csVersPhrase();
      if(window._majGardeCote)window._majGardeCote();
    }catch(_){}},140);
  }catch(e){} };
  document.addEventListener('click',function(e){ var b=e.target&&e.target.closest?e.target.closest('.garde-cote'):null; if(b){ e.preventDefault(); e.stopPropagation(); window._gardeCote(b.dataset.gc||'promi'); } },true);
  document.addEventListener('input',function(e){ if(e.target&&(e.target.id==='fTitle'||e.target.id==='nName')){ try{ if(window._majGardeCote)window._majGardeCote(); }catch(_){}} },true);
  function _wrapPhraseGC(){ var o=window._phraseRendu; if(o&&!o._gc){ window._phraseRendu=function(){ var r=o.apply(this,arguments); try{ requestAnimationFrame(window._majGardeCote); }catch(_){} return r; }; window._phraseRendu._gc=true; } }
  if(document.readyState!=='loading') _wrapPhraseGC(); else document.addEventListener('DOMContentLoaded',_wrapPhraseGC);
  var _cb=document.getElementById('createBtn'); if(_cb) _cb.addEventListener('click',function(){ window._brouillonRepris=null; _wrapPhraseGC(); setTimeout(function(){try{if(window._majGardeCote)window._majGardeCote();}catch(_){}},200); });
  /* PLANTER un brouillon repris = le CONVERTIR : on retire l'ancien brouillon après
     que le nouveau Promi/Nuée est planté (sinon doublon), et on réconcilie la Toile. */
  ['addPromi','addNuee'].forEach(function(id){ var bb=document.getElementById(id); if(bb) bb.addEventListener('click',function(){
    if(window._brouillonRepris==null) return; var rid=window._brouillonRepris; window._brouillonRepris=null;
    setTimeout(function(){ try{
      var i=-1; for(var j=0;j<promises.length;j++){ if(promises[j].id===rid){ i=j; break; } }
      if(i>=0){ promises.splice(i,1);
        try{ if(window.Toile&&window.Toile.sync){ var ids=promises.filter(function(p){return !p.draft;}).map(function(p){return p.id;}); window.Toile.sync(ids); } }catch(_){}
        if(typeof render==='function')render(); if(typeof caption==='function')caption(); if(window.syncAll)window.syncAll(); }
    }catch(_){} }, 120);
  }); });
})();
