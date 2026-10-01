
/* ⚑⚑ 24 SEPTEMBRE 2026 (Tom) — LE PARTAGE DE LA PELOTE : SEULE, OU DANS MON FOLIO.
   1 · Sur « Ma Toile », la Pelote ne s'ajoute plus (la rangée DANS L'IMAGE sort, et le
       drapeau ne peint plus rien : `lot-V14-TOILE` est retiré).
   2 · DANS MON FOLIO, LA PELOTE SE DÉPLACE AU DOIGT. Un APPUI LONG sur elle la prend ; on la
       fait glisser ; la planche se recompose autour, case par case, selon l'endroit visé.
       Elle garde ses quatre cases, rien ne se superpose, rien ne disparaît — c'est le
       mécanisme de réservation de `sharePlanche`, qui ne change pas : seul le coin haut-gauche
       du bloc (`shPelBR`, `shPelBC`) bouge.
       ⚠ LES DEUX GESTES SE DISTINGUENT : un doigt qui BOUGE de plus de 8 px avant la fin de
       l'appui ne prend rien — il glisse, et la Pelote reste où elle est. Seul un doigt IMMOBILE
       pendant 380 ms la prend. (L'ancien geste du Noyau, 260 ms, ne s'annulait pas au
       mouvement : c'est exactement le déplacement accidentel qu'on refuse.)
   3 · L'IMAGE PARTAGÉE EST L'APERÇU. Vérifié dans le code : `shareExport` n'avait que deux
       branches — `toile`, et SINON `paintPreview`, c'est-à-dire un aperçu de TOILE. Partager
       « Mon Folio » ou « Ma Pelote » envoyait donc une Toile. Et le pied de l'export
       (« Mon Promi » en haut, « promi.app » en bas) n'était plus celui de l'aperçu depuis le
       22 septembre. L'export passe maintenant par LES MÊMES PEINTRES que l'aperçu, et le
       mot-marque est relevé sur l'aperçu lui-même (police, taille, couleurs, place).
       ⚠ Et le canevas d'export ne se multiplie plus par la densité de l'écran : à 3840 × 3
       il faisait 74 millions de pixels — au-delà de ce qu'un iPhone accepte (16,7). */
(function(){
  function $(s,r){ return (r||document).querySelector(s); }

  /* ── 1 · la classe du sujet, pour la feuille de style ── */
  function classeSujet(){
    var sc=$('#shareScreen'); if(!sc) return;
    var t=(window.shareMode==='toile');
    if(sc.classList.contains('shc-toile')!==t) sc.classList.toggle('shc-toile',t);
  }

  /* ── 2 · LE GESTE ─────────────────────────────────────────────────── */
  var LONG=380, TOL=8;
  var tmr=null, pris=false, x0=0, y0=0, pid=null, raf=0, dernier=null;
  function cv(){ return document.getElementById('shCanvas'); }
  /* le point du doigt, dans les unités de la planche (les W × H de `sharePlanche`) */
  function local(e){
    var c=cv(), G=window._plancheComp&&window._plancheComp.grille; if(!c||!G) return null;
    var r=c.getBoundingClientRect(); if(!r.width) return null;
    return {x:(e.clientX-r.left)/r.width*G.W, y:(e.clientY-r.top)/r.height*G.H};
  }
  function surPelote(p){
    var B=window._plancheComp&&window._plancheComp.bloc; if(!B||!p) return false;
    var cx=B.x+B.w/2, cy=B.y+B.h/2;
    return Math.hypot(p.x-cx, p.y-cy) <= B.D/2*1.05;
  }
  function actif(){ return window.shareMode==='mosaic' && !!window.shPelote; }
  /* la case que vise le doigt : le CENTRE du bloc se pose au plus près du doigt */
  function cible(p){
    var G=window._plancheComp.grille, pas=G.cw+G.gap;
    var c=Math.max(0, Math.min(G.cols-2, Math.round((p.x-G.pad)/pas - 1)));
    var best=0, bd=1e9;
    for(var r=0; r<=G.maxR; r++){
      var yt=G.y0+(G.yRow[r]!==undefined?G.yRow[r]:G.yRow[G.yRow.length-1]+pas*(r-G.yRow.length+1));
      var h=(G.hRow[r]||G.cw)+G.gap+(G.hRow[r+1]||G.hRow[r]||G.cw);
      var d=Math.abs(yt+h/2-p.y); if(d<bd){ bd=d; best=r; }
    }
    return {r:best, c:c};
  }
  function rend(){ if(raf) return; raf=requestAnimationFrame(function(){ raf=0;
    try{ if(window.shareRender) window.shareRender(); }catch(_){} }); }
  function annule(){ if(tmr){ clearTimeout(tmr); tmr=null; } }

  document.addEventListener('pointerdown',function(e){
    annule(); if(!actif()) return;
    var z=document.getElementById('shPreviewArea'); if(!z||!z.contains(e.target)) return;
    var p=local(e); if(!surPelote(p)) return;
    pid=e.pointerId; x0=e.clientX; y0=e.clientY; dernier=p;
    tmr=setTimeout(function(){ tmr=null; pris=true;
      window._shPelPrise={x:dernier.x, y:dernier.y};
      try{ window._shGelCadrage=true; }catch(_){}
      try{ if(navigator.vibrate) navigator.vibrate(8); }catch(_){}
      var s=$('#shareScreen'); if(s) s.classList.add('sh-pel-prise');
      rend();
    }, LONG);
  }, true);

  document.addEventListener('pointermove',function(e){
    if(e.pointerId!==pid) return;
    if(tmr){
      /* avant la fin de l'appui : un doigt qui bouge GLISSE, il ne prend rien */
      if(Math.hypot(e.clientX-x0, e.clientY-y0)>TOL){ annule(); pid=null; }
      else dernier=local(e)||dernier;
      return;
    }
    if(!pris) return;
    var p=local(e); if(!p) return;
    window._shPelPrise={x:p.x, y:p.y};
    var t=cible(p);
    if(t.r!==window.shPelBR || t.c!==window.shPelBC){ window.shPelBR=t.r; window.shPelBC=t.c; }
    rend();
    e.preventDefault(); e.stopPropagation();
  }, true);

  function lache(e){
    if(e && pid!==null && e.pointerId!==pid) return;
    annule(); pid=null;
    if(!pris) return;
    pris=false; window._shPelPrise=null; window._shPlancheCache=null;
    try{ window._shGelCadrage=false; }catch(_){}
    var s=$('#shareScreen'); if(s) s.classList.remove('sh-pel-prise');
    rend();
  }
  document.addEventListener('pointerup',lache,true);
  document.addEventListener('pointercancel',lache,true);
  /* le défilement ne part pas avec la Pelote (l'aperçu est déjà en `touch-action:none`,
     c'est une ceinture en plus pour le panneau qui l'entoure) */
  document.addEventListener('touchmove',function(e){ if(pris && e.cancelable) e.preventDefault(); },{passive:false,capture:true});
  window._shPelGeste={LONG:LONG, TOL:TOL, pris:function(){ return pris; }};

  /* ── 3 · L'EXPORT EST L'APERÇU ────────────────────────────────────── */
  /* le mot-marque, relevé sur l'aperçu : police, taille, couleurs, place — à l'échelle */
  function marque(g, W, H){
    try{
      var wrap=document.getElementById('shWrap'), m=document.getElementById('shWordmark');
      if(!wrap||!m) return;
      var R=wrap.getBoundingClientRect(), r=m.getBoundingClientRect();
      if(!R.width||!r.width) return;
      var k=W/R.width, cs=getComputedStyle(m);
      var fs=parseFloat(cs.fontSize)*k;
      var fam=cs.fontFamily, st=cs.fontStyle, wt=cs.fontWeight;
      g.save(); g.setTransform(1,0,0,1,0,0);
      g.font=st+' '+wt+' '+fs+'px '+fam;
      try{ g.letterSpacing=(parseFloat(cs.letterSpacing)||0)*k+'px'; }catch(_){}
      g.textAlign='left'; g.textBaseline='middle';
      var x=(r.left-R.left)*k, y=(r.top-R.top+r.height/2)*k;
      var uvi=m.querySelector('.uvi'), corps=(m.textContent||'Promi');
      var avant=uvi?corps.slice(0,corps.length-uvi.textContent.length):corps;
      g.fillStyle=cs.color; g.fillText(avant,x,y);
      if(uvi){ g.fillStyle=getComputedStyle(uvi).color;
        g.fillText(uvi.textContent, x+g.measureText(avant).width, y); }
      g.restore();
    }catch(_){}
  }
  function exporte(){
    try{
      window.shareVis=(window.shLabels===undefined)?true:!!window.shLabels;
      var a=shFmtA(), base=3840, W, H;
      if(a<=1){ H=base; W=Math.round(base*a); } else { W=base; H=Math.round(base/a); }
      var dpr=Math.min(3,window.devicePixelRatio||1);
      var cvx=document.createElement('canvas'), g;
      if(window.shareMode==='mosaic'){
        /* la MÊME composition que l'aperçu, peinte plus fin (voir `sharePlanche`) */
        /* la taille de l'aperçu est celle que `shareRender` pose sur `#shWrap` (le zoom de
           l'aperçu est une transformation : il ne la change pas) */
        var wr=document.getElementById('shWrap');
        var Wp=(wr&&parseFloat(wr.style.width))||W/dpr, Hp=(wr&&parseFloat(wr.style.height))||H/dpr;
        sharePlanche(cvx, Wp, Hp, W/Wp); g=cvx.getContext('2d');
      } else if(window.shareMode==='pelote'){
        cvx.width=W; cvx.height=H;
        if(window._shPeintPelote) window._shPeintPelote(cvx);
        g=cvx.getContext('2d');
      } else {
        g=shSize(cvx, W/dpr, H/dpr); shareToile(g, W/dpr, H/dpr);
      }
      var Wc=cvx.width, Hc=cvx.height;
      g.setTransform(1,0,0,1,0,0);
      marque(g, Wc, Hc);
      try{ _shPreviewQR(g, Wc, Hc); }catch(_){}
      /* l'export a publié SA composition (à 3840) : on rend l'aperçu, sans quoi le geste
         de la Pelote lirait des cotes d'export */
      try{ window.shareRender(); }catch(_){}
      window._shDernierExport={mode:window.shareMode, W:Wc, H:Hc};
      cvx.toBlob(function(blob){ if(!blob) return;
        try{ var file=new File([blob],'mon-promi.png',{type:'image/png'});
          if(navigator.canShare&&navigator.canShare({files:[file]})){
            navigator.share({files:[file],title:'Mon Promi'}); return; } }catch(e){}
        try{ var link=document.createElement('a'); link.href=URL.createObjectURL(blob);
          link.download='mon-promi.png'; document.body.appendChild(link); link.click(); link.remove(); }catch(e){}
      },'image/png');
      return cvx;
    }catch(e){ return null; }
  }
  window._shExporteCanevas=exporte;
  function branche(){
    window.shareExport=exporte;
    var b=document.getElementById('shShareBtn');
    if(b && b.onclick!==exporte) b.onclick=exporte;
  }

  /* on ENVELOPPE `shareRender` (§8) */
  function enveloppe(){
    if(window._shRenderV15 || typeof window.shareRender!=='function') return;
    var f=window.shareRender;
    window.shareRender=function(){ classeSujet(); return f.apply(this,arguments); };
    window._shRenderV15=true;
  }
  function passe(){ enveloppe(); branche(); classeSujet(); }
  passe(); [400,1200,2600].forEach(function(t){ setTimeout(passe,t); });
})();
