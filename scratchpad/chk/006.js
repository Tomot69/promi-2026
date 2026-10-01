
/* === page + : carousel par transform (dots + swipe au doigt) === */
(function(){
  function initCreatePlus(){
    var sheet=document.getElementById('createSheet'); if(!sheet)return;
    var viewport=sheet.querySelector('.tiles');
    var track=sheet.querySelector('.tiles-track');
    var tiles=[].slice.call(sheet.querySelectorAll('.tile'));
    var dots=[].slice.call(sheet.querySelectorAll('#kbars .pdot'));
    if(!track||!tiles.length)return;
    var N=tiles.length, cur=0;
    function applyForms(k){
      var pf=sheet.querySelector('#promiForm'),nf=sheet.querySelector('#nueeForm'),df=sheet.querySelector('#draftForm');
      /* Chiche = nature : sa création réutilise LE MÊME formulaire que le Promi (phrase,
         geste, réglages). Le sens est verrouillé sur 'chiche' ; le Promi garde la
         bascule ⇄ (faire/demander). */
      if(pf)pf.style.display=(k==='promi'||k==='chiche')?'block':'none';
      if(nf)nf.style.display=(k==='nuee')?'block':'none';
      if(df)df.style.display=(k==='draft')?'block':'none';
      try{if(k)window.createKind=k;}catch(e){}
      try{
        if(k==='chiche'){ window._csSens='chiche'; if(window._phrase)window._phrase.sens='chiche'; }
        else if(k==='promi'){ if(window._phrase && window._phrase.sens==='chiche'){ window._phrase.sens='faire'; window._phrase.faireAutre=false; window._phrase.qui='Moi'; window._csSens='faire'; } }
        if((k==='promi'||k==='chiche') && window._phraseRendu) window._phraseRendu();
        /* la dalle se re-teinte au signal de la nature (chiche→framboise via le tint map +
           _dalleDerive qui lit createKind) — sans ce rappel, la dalle gardait le monde (lilas). */
        if(window.renderCsDalle){ setTimeout(window.renderCsDalle,20); setTimeout(window.renderCsDalle,240); }
        /* « dans une Nuée » : sorti de la phrase, il vit EN HAUT de Peaufiner (Promi ET
           Chiche peuvent être dans une Nuée). Masqué quand on vient d'une Nuée (déjà connue). */
        if(k==='promi'||k==='chiche'){
          var _fn=sheet.querySelector('#promiForm .f-nuee'), _pe=sheet.querySelector('#promiExtra');
          if(_fn&&_pe){ if(_fn.parentNode!==_pe) _pe.insertBefore(_fn,_pe.firstChild);
            _fn.style.display=(typeof selNuee!=='undefined'&&selNuee)?'none':''; }
        }
      }catch(_){}
    }
    function setActive(i){
      cur=Math.max(0,Math.min(N-1,i));
      tiles.forEach(function(t,k){t.classList.toggle('on',k===cur);});
      dots.forEach(function(d,k){d.classList.toggle('on',k===cur);});
      applyForms(tiles[cur].dataset.kind);
      try{var _cs=document.getElementById('createSheet');if(_cs)_cs.setAttribute('data-kind',tiles[cur].dataset.kind);}catch(e){}
    }
    function goTo(i,anim){
      i=Math.max(0,Math.min(N-1,i));
      track.classList.toggle('drag',!anim);
      track.style.transform='translateX('+(-i*100)+'%)';
      setActive(i);
    }
    dots.forEach(function(d,i){ d.addEventListener('click',function(){ goTo(i,true); }); });
    /* cliquer une TUILE la sélectionne (→ setActive → applyForms). Sans ça, seule la
       Nuée (handler dédié) et le Promi (défaut) basculaient ; le Chiche restait sans
       formulaire. Le carrousel gère les trois natures de façon uniforme. */
    tiles.forEach(function(t,i){ t.addEventListener('click',function(){ goTo(i,true); }); });
    /* swipe au doigt / souris */
    var x0=null,base=0,drag=false,moved=false,vw=0;
    /* ⚑ LE CHICHE SE PERDAIT AU DOIGT (13 sept. 2026, CLAUDE §8). Sur l'écran des choix (`pp-choix`) les tuiles sont
       EMPILÉES : il n'y a rien à faire glisser. Et un toucher n'est pas un glissement : au lever du doigt, `up()`
       rejouait `goTo(cur)` — la tuile d'AVANT —, l'écran passait à la phrase de cette nature sous le doigt, et le
       clic synthétisé tombait sur le geste au lieu de la tuile. Seul un vrai glissement change de tuile. */
    function down(e){ if(sheet.classList.contains('pp-choix')) return; x0=(e.touches?e.touches[0].clientX:e.clientX); base=-cur*100; drag=true; moved=false; vw=viewport.clientWidth||1; track.classList.add('drag'); }
    function move(e){ if(!drag)return; var cx=(e.touches?e.touches[0].clientX:e.clientX); var d=cx-x0; if(Math.abs(d)>4)moved=true; var pct=base+(d/vw)*100; pct=Math.max(-(N-1)*100-12,Math.min(12,pct)); track.style.transform='translateX('+pct+'%)'; if(e.cancelable&&moved)e.preventDefault(); }
    function up(e){ if(!drag)return; drag=false; var cx=(e.changedTouches?e.changedTouches[0].clientX:e.clientX); var d=cx-x0; var thr=vw*0.18; var ni=cur; if(d<-thr)ni=cur+1; else if(d>thr)ni=cur-1;
      if(ni===cur){ track.classList.remove('drag'); track.style.transform='translateX('+(-cur*100)+'%)'; return; }
      goTo(ni,true); }
    viewport.addEventListener('mousedown',down); window.addEventListener('mousemove',move); window.addEventListener('mouseup',up);
    viewport.addEventListener('touchstart',down,{passive:true}); viewport.addEventListener('touchmove',move,{passive:false}); window.addEventListener('touchend',up);
    /* importance */
    var seg=sheet.querySelector('#impSeg');
    if(seg){ window.createImportance='normal';
      seg.querySelectorAll('.is').forEach(function(bt){bt.addEventListener('click',function(){
        seg.querySelectorAll('.is').forEach(function(x){x.classList.remove('on');});
        bt.classList.add('on'); window.createImportance=bt.dataset.imp;});});
    }
    goTo(0,false);
  }
  if(document.readyState!=='loading')initCreatePlus();
  else document.addEventListener('DOMContentLoaded',initCreatePlus);
})();
