
/* ═══ LA COULEUR — CINQUIÈME RÉGLAGE DU CERCLE (Tom, 13 sept. 2026) ═══
   Où : Peaufiner d'une fiche (Promi, Chiche) et de la page +. Aux Réglages, la rangée montre seulement ce que le Cercle ouvre.
   Quoi : une des quatre couleurs de la palette du Studio (celle du monde de la dalle, figé à la plantation), ou un code libre.
   La donnée : p.dalle = {ci, lit, rgb?} — la couleur figée du lot précédent ; un code libre s'y ajoute en rgb, que le moteur lit.
   À la page +, le choix attend la plantation (window._couleurAPlanter) et s'efface quand la page + se rouvre.
   ⚠ La Nuée n'a pas de dalle à elle sur la Toile : question posée à Tom, rien n'est inventé ici. */
(function(){
  function hex(c){ return '#'+c.map(function(v){ v=Math.max(0,Math.min(255,Math.round(v))); return (v<16?'0':'')+v.toString(16); }).join('').toUpperCase(); }
  function lit(t){ t=String(t||'').trim().replace(/^#/,''); if(/^[0-9a-f]{3}$/i.test(t)) t=t.split('').map(function(x){return x+x;}).join('');
    if(!/^[0-9a-f]{6}$/i.test(t)) return null; return [parseInt(t.slice(0,2),16),parseInt(t.slice(2,4),16),parseInt(t.slice(4,6),16)]; }
  function mondeDe(p){ try{ if(p && p.monde) return p.monde; return window.Toile.mondeCourant(); }catch(_){ return null; } }
  function tons(p){ try{ var m=mondeDe(p)||{}; return window.Toile.tonsDe(m.p, m.h); }catch(_){ return []; } }
  function contexte(row){
    if(row && row.closest && row.closest('#createSheet')) return {plus:true, p:null};
    try{ var dp=row && row.closest && row.closest('#detailPoster');
      if(dp && (dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) && typeof curNuee!=='undefined' && curNuee)
        return {plus:false, p:null, nuee:curNuee}; }catch(_){}
    var p=(typeof cur!=='undefined')?cur:null; return {plus:false, p:p};
  }
  /* la couleur à montrer : ce qui est choisi, sinon la couleur figée de la dalle */
  function choixDe(ctx){
    if(ctx.plus) return window._couleurAPlanter||null;
    if(ctx.nuee) return (window.NUEDALLE||{})[ctx.nuee]||null;
    var p=ctx.p; if(!p||!p.dalle) return null; return p.dalle;
  }
  function rgbDe(ctx){
    var d=choixDe(ctx); if(!d) return null;
    if(d.rgb) return d.rgb;
    var T=tons(ctx.p); var c=T[d.ci]; if(!c) return null;
    if(ctx.plus || ctx.nuee || !(d.lit|0)) return c;
    try{ var s=window.Toile.colorOf(ctx.p.id); var m=/rgb\((\d+),(\d+),(\d+)\)/.exec(s||''); if(m) return [+m[1],+m[2],+m[3]]; }catch(_){}
    return c;
  }
  function applique(ctx, choix){
    if(ctx.plus){ var cs=document.getElementById('createSheet');
      window._couleurAPlanter=choix; choix.nat=(cs&&cs.getAttribute('data-kind')==='nuee')?'nuee':'promi'; }
    else if(ctx.nuee){ var ND=window.NUEDALLE||(window.NUEDALLE={}), an=ND[ctx.nuee];
      ND[ctx.nuee] = choix.rgb ? {ci:(an&&an.ci!=null)?an.ci:0, lit:0, rgb:choix.rgb, choisi:1} : {ci:choix.ci, lit:0, choisi:1};
      try{ window.Toile.refigeCouleurs(); }catch(_){}
      try{ if(typeof queueSave==='function') queueSave(); }catch(_){} }
    else if(ctx.p){
      var p=ctx.p, ci=(choix.ci!=null)?choix.ci:((p.dalle&&p.dalle.ci!=null)?p.dalle.ci:0);
      p.dalle = choix.rgb ? {ci:ci, lit:0, rgb:choix.rgb, choisi:1} : {ci:ci, lit:0, choisi:1};
      try{ window.Toile.refigeCouleurs(); }catch(_){}
      try{ if(typeof queueSave==='function') queueSave(); else if(typeof saveState==='function') saveState(); }catch(_){}
      setTimeout(function(){ try{ if(window.dpRefresh) window.dpRefresh(); }catch(_){} }, 60);
    }
    document.querySelectorAll('.s2-couleur').forEach(maj);
  }
  function maj(row){
    if(!row || !row.isConnected) return;
    var ctx=contexte(row), c=rgbDe(ctx), T=tons(ctx.p), d=choixDe(ctx);
    var v=row.querySelector('.s2-val'); if(!v) return;
    var mot = c ? hex(c) : 'au hasard';
    var sig = mot+'|'+T.map(hex).join(',')+'|'+(d?(d.rgb?'r':d.ci):'-');
    if(row.getAttribute('data-cc')===sig) return;
    row.setAttribute('data-cc', sig);
    v.innerHTML=''; if(c){ var pas=document.createElement('span'); pas.className='cc-pas'; pas.style.background=hex(c); v.appendChild(pas); }
    v.appendChild(document.createTextNode(mot));
    var bs=row.querySelectorAll('.cc-ton');
    bs.forEach(function(b,i){ var t=T[i]; b.hidden=!t; if(t) b.style.backgroundColor=hex(t);
      var on=!!(d && !d.rgb && d.ci===i); if(b.classList.contains('on')!==on) b.classList.toggle('on', on); });
    var inp=row.querySelector('.cc-code'); if(inp && document.activeElement!==inp) inp.value = (d&&d.rgb)?hex(d.rgb):'';
  }
  window._regCouleur=function(reg){
    var ctl=document.createElement('div'); ctl.className='cc-ctl';
    for(var i=0;i<4;i++){ (function(i){ var b=document.createElement('button'); b.type='button'; b.className='cc-ton'; b.setAttribute('data-ton',String(i));
      b.setAttribute('aria-label','couleur '+(i+1));
      b.addEventListener('click', function(ev){ ev.stopPropagation(); ev.preventDefault(); applique(contexte(row), {ci:i, lit:0}); }, true);
      ctl.appendChild(b); })(i); }
    var inp=document.createElement('input'); inp.type='text'; inp.className='cc-code'; inp.maxLength=7; inp.placeholder='code couleur';
    inp.setAttribute('autocomplete','off'); inp.setAttribute('spellcheck','false');
    function essai(){ var c=lit(inp.value); if(c) applique(contexte(row), {rgb:c}); }
    inp.addEventListener('input', function(ev){ ev.stopPropagation(); if(/^#?[0-9a-f]{6}$/i.test(inp.value.trim())) essai(); });
    inp.addEventListener('change', function(ev){ ev.stopPropagation(); essai(); });
    inp.addEventListener('keydown', function(ev){ ev.stopPropagation(); if(ev.key==='Enter'){ essai(); inp.blur(); } });
    ['click','pointerdown','mousedown','touchstart'].forEach(function(t){ inp.addEventListener(t, function(ev){ ev.stopPropagation(); }); });
    ctl.appendChild(inp);
    var row=reg('LA COULEUR', '', {hote:ctl, cls:'s2-couleur'});
    [0,60,200,600].forEach(function(ms){ setTimeout(function(){ maj(row); }, ms); });
    return row;
  };
  setInterval(function(){ try{ document.querySelectorAll('.s2-couleur').forEach(maj); }catch(_){} }, 500);
  /* la page + : le choix attend la plantation */
  function brancheToile(){
    if(!window.Toile || !window.Toile.addPromi || window.Toile.addPromi._cc) return false;
    var o=window.Toile.addPromi;
    var f=function(id){ var r=o.apply(this, arguments);
      try{ var ch=window._couleurAPlanter; if(ch && ch.nat!=='nuee' && id!=null && typeof promises!=='undefined'){
        var p=promises.find(function(q){ return q.id===id; });
        if(p){ var ci=(ch.ci!=null)?ch.ci:((p.dalle&&p.dalle.ci!=null)?p.dalle.ci:0);
          p.dalle = ch.rgb ? {ci:ci, lit:0, rgb:ch.rgb, choisi:1} : {ci:ci, lit:0, choisi:1};
          window._couleurAPlanter=null; window.Toile.refigeCouleurs();
          try{ if(typeof queueSave==='function') queueSave(); }catch(_){} } } }catch(_){}
      return r; };
    f._cc=true; window.Toile.addPromi=f; return true;
  }
  if(!brancheToile()){ var k=setInterval(function(){ if(brancheToile()) clearInterval(k); }, 200); }
  function veille(){
    var cs=document.getElementById('createSheet'); if(!cs){ setTimeout(veille, 300); return; }
    var ouverte=cs.classList.contains('show');
    new MutationObserver(function(){ var o=cs.classList.contains('show'); if(o===ouverte) return; ouverte=o;
      if(o){ window._couleurAPlanter=null; try{ window._nuesAvant=Object.keys(NUE); }catch(_){ window._nuesAvant=[]; } } }).observe(cs, {attributes:true, attributeFilter:['class']});
    /* une Nuée créée à la page + : la couleur choisie va à SA dalle, au moment où la Toile la plante (sync) */
    function brancheSync(){ if(!window.Toile || !window.Toile.sync || window.Toile.sync._cc) return !!(window.Toile&&window.Toile.sync);
      var o=window.Toile.sync; var f=function(){
        try{ var ch=window._couleurAPlanter; if(ch && ch.nat==='nuee' && window._nuesAvant && typeof NUE!=='undefined'){
          var neuves=Object.keys(NUE).filter(function(k){ return k!=='soi' && window._nuesAvant.indexOf(k)<0; });
          if(neuves.length){ var ND=window.NUEDALLE||(window.NUEDALLE={});
            neuves.forEach(function(k){ ND[k] = ch.rgb ? {ci:0, lit:0, rgb:ch.rgb, choisi:1} : {ci:ch.ci, lit:0, choisi:1}; });
            window._couleurAPlanter=null; } } }catch(_){}
        return o.apply(this, arguments); };
      f._cc=true; window.Toile.sync=f; return true; }
    if(!brancheSync()){ var k2=setInterval(function(){ if(brancheSync()) clearInterval(k2); }, 200); }
  }
  if(document.readyState!=='loading') veille(); else document.addEventListener('DOMContentLoaded', veille);
})();
