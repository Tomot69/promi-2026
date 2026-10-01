
/* ⚑ v83 (Tom) — PENDANT L'ONBOARDING, LA TOILE S'ÉCARTE DES ÉLÉMENTS : le mot-marque, la phrase, les pastilles, la zone où tracer.
   Relevé toutes les 250 ms tant que l'onboarding est actif ; transmis seulement s'il change (§8 : comparer avant d'agir) ; rendu vide à la fin. */
(function(){ var dernier='';
  setInterval(function(){ try{ var dev=document.getElementById('device'), cv=document.getElementById('toileCv'); if(!dev||!cv||!window.Toile||!Toile.ecarte) return;
    var rects=[]; if(dev.classList.contains('onb-actif')){ var cr=cv.getBoundingClientRect(); if(!cr.width) return; var sx=cv.clientWidth/cr.width, sy=cv.clientHeight/cr.height;
      [].forEach.call(document.querySelectorAll('#onbV .onbv-a'), function(e){ var cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05) return;
        var r=e.getBoundingClientRect(); if(!r.width||!r.height) return; rects.push({x:Math.round((r.left-cr.left)*sx), y:Math.round((r.top-cr.top)*sy), w:Math.round(r.width*sx), h:Math.round(r.height*sy)}); }); }
    var k=JSON.stringify(rects); if(k===dernier) return; dernier=k; Toile.ecarte(rects); }catch(_){ } }, 250);
})();
