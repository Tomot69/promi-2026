
/* ⚑ v89 (Tom, 27 sept. 2026, Q347) — LES COMPTEURS.
   · UN SEUL COMPTEUR : ce qui attend un GESTE de moi — un Chiche lancé non relevé, un Promi qu'on me fait non accepté, une demande,
     une invitation à une Nuée, une moitié tracée qui attend la mienne. Il redescend quand j'ai agi, jamais parce que j'ai regardé.
   · LA PASTILLE d'une carte dit « pas encore vu » : elle s'efface quand on ouvre CETTE carte.
   · Une promesse à moi-même : rien. Un Promi planté dans une de mes Nuées : la pastille seulement. */
(function(){
  function pOf(id){ try{ return id==null?null:(promises.filter(function(x){ return x.id===id; })[0]||null); }catch(_){ return null; } }
  window._filAttend=function(f){ if(!f) return false; var p=pOf(f.pid);
    if(f.type==='chiche_recu') return true;
    if(f.type==='received') return !!(p&&p.pending);
    if(f.type==='invitation') return !f.fait;
    if(f.type==='moitie') return !f.fait && !!p && p.status!=='tenu' && p.status!=='kept';
    return false; };
  window._filAttente=function(){ var n=0; try{ (FEED||[]).forEach(function(f){ if(window._filAttend(f)) n++; }); }catch(_){}
    try{ if(typeof demandesEnAttente==='function') n+=demandesEnAttente().length; }catch(_){} return n; };
  function rafraichit(){ try{ if(typeof buildFeed==='function') buildFeed(); }catch(_){} try{ if(window._majFilDot) _majFilDot(); }catch(_){} try{ if(typeof updateFeedDot==='function') updateFeedDot(); }catch(_){} try{ if(typeof saveState==='function') saveState(); }catch(_){} }
  (function(){ var od=window.openDetail; if(typeof od==='function' && !od.__vu){ window.openDetail=function(id){ try{ (FEED||[]).forEach(function(f){ if(f.pid===id && f.unread) f.unread=false; }); }catch(_){} return od.apply(this, arguments); }; window.openDetail.__vu=true; } })();
  window._filVu=function(fid){ try{ var f=(FEED||[]).filter(function(x){ return x.id===fid; })[0]; if(f&&f.unread){ f.unread=false; try{ if(typeof saveState==='function') saveState(); }catch(_){} } }catch(_){} };
  window.filRejoindre=function(fid){ try{ var f=(FEED||[]).filter(function(x){ return x.id===fid; })[0]; if(!f||f.fait) return;
    var k=f.nuee, nom=f.nom||(NUE&&NUE[k])||'';
    if(k){ if(!NUE[k]) NUE[k]=nom; if(!NUEEMEM[k]) NUEEMEM[k]=[]; if(f.from&&NUEEMEM[k].indexOf(f.from)<0) NUEEMEM[k].push(f.from); }
    f.fait=true; f.unread=false; f.type='joined'; f.text='Tu as rejoint « '+nom+' »';
    try{ if(window.syncAll) syncAll(); }catch(_){} try{ if(typeof render==='function') render(); }catch(_){}
    rafraichit(); }catch(_){} };
  window.filTracer=function(fid){ try{ var f=(FEED||[]).filter(function(x){ return x.id===fid; })[0]; if(!f) return; f.unread=false; var p=pOf(f.pid); if(!p) return;
    if(window.setView) setView('toile'); if(window.openDetail) openDetail(p.id); }catch(_){} };
  /* une parole tenue depuis sa fiche (sa moitié tracée) : le compteur redescend */
  setInterval(function(){ try{ var d=document.getElementById('filDot'); if(!d) return; var on=window._filAttente()>0; if(d.classList.contains('on')!==on) d.classList.toggle('on',on);
    var c=document.getElementById('fdCount'); if(c){ var n=''+window._filAttente(); if(c.textContent!==n) c.textContent=n; } }catch(_){} }, 1000);
})();
