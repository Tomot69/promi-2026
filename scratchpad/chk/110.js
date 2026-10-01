
(function(){
  var cle='';
  function peindre(){
    try{
      var sc=document.getElementById('studioScreen'); if(!sc||!sc.classList.contains('show')) return;
      var th=document.getElementById('st3thumb'); if(!th||!window.Toile||!Toile.dalleTrame) return;
      var pr=(typeof promises!=='undefined'?promises:[]).filter(function(p){return !p.draft && Toile.dalleAbs && Toile.dalleAbs(p.id);});
      if(!pr.length) return;                               /* sans dalle sur la Toile, le curseur d'avant reste */
      var clair=document.getElementById('device').classList.contains('light');
      var M=Toile.mondeCourant?Toile.mondeCourant():{};
      var k=[M.m,M.p,M.h,clair,pr[0].id].join('|');
      var cv=th.querySelector('canvas');
      if(cv && cle===k) return;
      /* ⚑ v29 — la silhouette est rendue par le moteur à 64 px, posée 1:1 (redteam_decoupe) */
      var src=window._rendDalle?window._rendDalle(pr[0].id, 64, 64, {courant:1}):null;   /* v30 · le curseur du Studio : le monde courant, exprès */
      if(!src) return;
      if(!cv){ cv=document.createElement('canvas'); th.appendChild(cv); }
      cv.width=72; cv.height=72; var g=cv.getContext('2d'); g.clearRect(0,0,72,72);
      window._poseUn(g, src, 36, 36);
      g.globalCompositeOperation='source-in';
      g.fillStyle=clair?'#201908':'#F7F0DE'; g.fillRect(0,0,72,72);
      g.globalCompositeOperation='source-over';
      th.classList.add('st3-dalle'); cle=k;
    }catch(_){}
  }
  setInterval(peindre, 400);
})();
