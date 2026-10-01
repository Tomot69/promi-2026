
/* LOT 5 · Point 1 — grappe rendue par le moteur (Toile.dalleTrame, échelle 1),
   EXACTEMENT la disposition POS du bandeau de _ficheDalle. Repeinte après
   insertion (0/60/200/600 ms) car un canevas n'est mesurable qu'une fois disposé. */
(function(){
  /* LOT 6 : la grappe = N dalles positionnées aux left/top/width EXACTS du
     fichier (par écran). Chaque dalle = un <canvas class="cs-dalle"> absolu,
     rendu net par le moteur (Toile.dalleTrame, échelle 1), opacité 1, sans voile. */
  var LAYOUTS={
    choix:[[27,17,2],[59,29,26],[44,56,12]],  /* ph-0 : 3 dalles */
    phrase:[[24,22,34]]                          /* ph-1/2/3 : 1 dalle */
  };
  /* ── #2 (lot 17) : LA DALLE QUI NAÎT ──────────────────────────────────────────
     La zone haute de la page + montre la dalle du Promi en train de naître : une
     VRAIE dalle du moteur (forme + matière du monde actif, via Toile.dalleTrame —
     sûr, aucune mutation de la Toile), RE-TEINTÉE à une couleur FRAÎCHE de la palette
     réelle du monde, et RÉGÉNÉRÉE à chaque mot rempli de la phrase (forme + couleur
     changent avec la graine). On voit sa parole prendre forme, en direct.
     NB (choix noté) : la cellule EXACTE d'un Promi n'existe qu'une fois planté (elle
     dépend de la Toile physique, qu'on ne touche pas) ; l'aperçu prend donc une vraie
     forme de dalle du monde et une couleur du monde — fidèle, net, vivant. */
  window._seedPhrase=function(){ var t='';
    try{ var ft=document.getElementById('fTitle'); if(ft)t+=(ft.value||''); }catch(e){}
    try{ if(window._phrase){ t+='|'+(window._phrase.qui||'')+'|'+(window._phrase.quand||''); } }catch(e){}
    var h=2166136261; for(var i=0;i<t.length;i++){ h^=t.charCodeAt(i); h=Math.imul(h,16777619); }
    return (h>>>0)||1; };
  /* la couleur du MONDE ACTIF : la plus vive de sa palette réelle (déterministe,
     ne dépend PAS de la phrase). C'est la matière choisie au Studio. */
  window._couleurMondeVive=function(){
    var pal=[]; try{ pal=(window.Toile&&Toile.cols&&Toile.cols())||[]; }catch(_){}
    /* Toile.cols() rend des TABLEAUX [r,g,b] ; on gère aussi hex / 'r,g,b'. */
    function rgb(x){ if(!x)return null;
      if(Array.isArray(x))return [x[0]|0,x[1]|0,x[2]|0];
      x=(''+x).trim();
      if(x.charAt(0)==='#'){ var h=x.slice(1); if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2]; return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)]; }
      var m=x.match(/(\d+)[,\s]+(\d+)[,\s]+(\d+)/); return m?[+m[1],+m[2],+m[3]]:null; }
    var best=null,bs=-1;
    pal.forEach(function(x){ var c=rgb(x); if(!c)return; var mx=Math.max(c[0],c[1],c[2]),mn=Math.min(c[0],c[1],c[2]);
      var l=(mx+mn)/2, sat=(mx===mn)?0:(mx-mn)/(255-Math.abs(mx+mn-255)), score=sat*(1-Math.abs(l-150)/210);
      if(score>bs){bs=score;best=c;} });
    return best ? ('rgb('+best[0]+','+best[1]+','+best[2]+')') : '#82AEF8'; };
  window._dalleNaissante=function(){ try{
    var cs=document.getElementById('createSheet'); if(!cs) return;
    var _knd=cs.getAttribute('data-kind');
    if(_knd!=='promi'&&_knd!=='chiche') return;   /* Promi et Chiche génèrent une dalle ; Nuée/Brouillon portent leur identité */
    var wrap=document.getElementById('csGrappe'); if(!wrap) return;
    var W=wrap.clientWidth|0, H=wrap.clientHeight|0; if(W<40||H<40) return;
    if(!window.Toile||!Toile.dalleTrame) return;
    var ids=[]; try{ ids=promises.filter(function(q){return !q.draft&&!q.req;}).map(function(q){return q.id;}); }catch(_){}
    if(!ids.length) return;
    var seed=window._seedPhrase();
    /* la FORME : une vraie dalle du moteur (change avec la graine) */
    /* ⚑ v29 — la dalle qui naît est rendue par le moteur À SA TAILLE (0,62 W × 0,84 H, au plus ×1,7 de sa
       taille de Toile), la teinte posée 1:1, puis posée 1:1 (redteam_decoupe) */
    var dpr2=Math.max(2,Math.min(3,window.devicePixelRatio||2));
    var _idN=ids[seed % ids.length], _DN=Toile.dalleAbs&&Toile.dalleAbs(_idN); if(!_DN||!_DN.w) return;
    var base=window._rendDalle(_idN, Math.min(W*0.62, _DN.w*1.7)*dpr2, Math.min(H*0.84, _DN.h*1.7)*dpr2, {courant:1});   /* v30 · la dalle qui NAÎT : le monde où elle sera plantée */
    if(!base||!base.width) return;
    /* la COULEUR : celle du MONDE ACTIF, FIXE — elle ne varie PAS d'un mot à l'autre
       (une couleur au hasard ne dit rien ; la couleur est la matière choisie au Studio,
       comme n'importe quelle dalle de la Toile). On prend la couleur la plus vive de la
       palette réelle du monde — stable, sans graine. Seule la FORME dit « ce Promi-là ». */
    /* le Chiche teinte sa dalle qui naît au SIGNAL (framboise), pas à la couleur du monde
       — comme la Nuée en mauve. Le Promi garde la couleur de son monde. */
    var _kN=null; try{ var _csN=document.getElementById('createSheet'); _kN=_csN&&_csN.getAttribute('data-kind'); }catch(_){}
    var col=(_kN==='chiche')?'#FFB8D2':window._couleurMondeVive();
    var src=base;
    if(col){ var t=document.createElement('canvas'); t.width=base.width; t.height=base.height;
      var tc=t.getContext('2d'); if(tc){ tc.drawImage(base,0,0);
        tc.globalCompositeOperation='color'; tc.fillStyle=col; tc.fillRect(0,0,t.width,t.height);
        /* Chiche : la dalle framboise sur une bande framboise serait du ton-sur-ton
           (invisible). On remonte sa luminance (voile rose clair, uniquement sur ses
           pixels) pour qu'elle ressorte — comme la dalle claire de la Nuée sur sa bande. */
        if(_kN==='chiche'){ tc.globalCompositeOperation='source-atop'; tc.fillStyle='rgba(255,183,208,.42)'; tc.fillRect(0,0,t.width,t.height); }
        tc.globalCompositeOperation='destination-in'; tc.drawImage(base,0,0); src=t; } }
    /* rendu net, entier, taille native (1:1 pixel écran), centré dans la zone haute */
    wrap.innerHTML='';
    var cv=document.createElement('canvas'); cv.className='cs-dalle';
    cv.width=Math.round(W*dpr2); cv.height=Math.round(H*dpr2);
    cv.style.width=W+'px'; cv.style.height=H+'px'; cv.style.position='absolute'; cv.style.left='0'; cv.style.top='0';
    cv.style.setProperty('opacity','1','important'); cv.style.setProperty('filter','none','important');
    var g=cv.getContext('2d'); if(!g) return; g.setTransform(dpr2,0,0,dpr2,0,0); g.clearRect(0,0,W,H);
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';
    var dw=src.width/dpr2, dh=src.height/dpr2, oy=Math.round((H-dh)*0.46);   /* présente, sans exagérer — déjà à sa taille */
    /* la bande est traitée en CSS (navy profond, plus sombre que le bleu de nature) :
       n'importe quelle dalle du monde y ressort. La dalle garde sa couleur de monde. */
    g.shadowColor='rgba(0,0,0,.22)'; g.shadowBlur=14; g.shadowOffsetY=7;
    window._poseUn(g, src, W/2, oy + dh/2);
    wrap.appendChild(cv);
  }catch(e){} };
  function _wrapPhraseDN(){ var o=window._phraseRendu; if(o&&!o._dn){ window._phraseRendu=function(){ var r=o.apply(this,arguments); try{ if(window._dalleNaissante)requestAnimationFrame(window._dalleNaissante); }catch(e){} return r; }; window._phraseRendu._dn=true; } }

  window._peintGrappe=function(){try{
    var cs=document.getElementById('createSheet'); var k=cs?cs.getAttribute('data-kind'):null;
    /* #2 : sur la phrase d'un PROMI, la zone haute montre la DALLE QUI NAÎT (fraîche,
       monde actif), pas la dalle d'un Promi existant. */
    if(k==='promi'||k==='chiche'){
      /* on efface la grappe de l'écran de choix (dalles du monde) : la zone haute ne
         montre que la DALLE QUI NAÎT (framboise pour chiche). Sans ça, des dalles
         parasites du monde restaient par-dessus. */
      try{ var _wg=document.getElementById('csGrappe'); if(_wg){ var _cd=_wg.querySelectorAll('.cs-dalle'); for(var _j=0;_j<_cd.length;_j++)_cd[_j].remove(); } }catch(_){}
      if(window._dalleNaissante)window._dalleNaissante(); return;
    }
    var wrap=document.getElementById('csGrappe'); if(!wrap) return;
    var LAY = k ? LAYOUTS.phrase : LAYOUTS.choix;
    var have=wrap.querySelectorAll('.cs-dalle');
    while(have.length>LAY.length){ wrap.removeChild(have[have.length-1]); have=wrap.querySelectorAll('.cs-dalle'); }
    while(have.length<LAY.length){ var d=document.createElement('canvas'); d.className='cs-dalle'; wrap.appendChild(d); have=wrap.querySelectorAll('.cs-dalle'); }
    var W=wrap.clientWidth|0, H=wrap.clientHeight|0; if(W<40||H<40) return;
    var dpr=Math.min(2,window.devicePixelRatio||1);
    var ids=[]; try{ ids=promises.filter(function(q){return !q.draft&&!q.req;}).slice(0,LAY.length).map(function(q){return q.id;}); }catch(_){}
    for(var i=0;i<LAY.length;i++){
      var cv=have[i], L=LAY[i];
      cv.style.position='absolute'; cv.style.left=L[0]+'%'; cv.style.top=L[1]+'%'; cv.style.width=L[2]+'%';
      var id = ids.length ? ids[i%ids.length] : null; if(!id) continue;
      /* ⚑ v29 — rendue par le moteur à la largeur de sa place, le canevas prend SA taille : posée 1:1 */
      var wpx=W*L[2]/100, t2=null;
      try{ t2=window._rendDalle(id, wpx*dpr, 1e5, {courant:1}); }catch(_){ continue; }   /* v30 · page + : le monde courant, exprès */ if(!t2) continue;
      cv.width=t2.width; cv.height=t2.height; cv.style.width=(t2.width/dpr)+'px'; cv.style.height=(t2.height/dpr)+'px';
      var g=cv.getContext('2d'); if(!g) continue; g.setTransform(1,0,0,1,0,0); g.clearRect(0,0,cv.width,cv.height);
      g.globalAlpha=1; g.drawImage(t2,0,0);
    }
  }catch(e){}};
  function peins(){ try{ _peintGrappe(); }catch(_){}}
  var cb=document.getElementById('createBtn');
  if(cb) cb.addEventListener('click',function(){ _wrapPhraseDN(); [0,60,200,600].forEach(function(t){ setTimeout(peins,t); }); });
  window.addEventListener('resize',peins);
  /* la dalle se régénère à chaque frappe du TITRE (le qui/quand passent par le
     chooser → _phraseRendu, déjà hooké). Rendu SVG léger : « en direct » sans coût Toile. */
  document.addEventListener('input',function(e){ if(e.target&&e.target.id==='fTitle'){ try{ if(window._dalleNaissante)window._dalleNaissante(); }catch(_){}} },true);
})();
