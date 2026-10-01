
/* ⚑ v74 (Tom, 27 sept. 2026) — « quand on a payé, le lien vers la page du Cercle n'existe plus ». Sous le Cercle, rien n'ouvre plus la
   page qui VEND : ni le mot-marque de l'accueil, ni les verrous, ni un bandeau. Une seule garde, sur la fonction qui ouvre (toutes
   les portes y passent) et, en filet, sur l'écran lui-même (quelques anciennes portes posent `.show` directement). L'achat fait
   DEPUIS la page ne la ferme pas (la classe ne change pas). Le mot-marque perd son rôle de bouton. */
(function(){
  function membre(){ var d=document.getElementById('device'); return !!(d&&d.classList.contains('premium')); }
  var f=window.ouvreCercle; if(typeof f==='function' && !f.__v74){ window.ouvreCercle=function(){ if(membre()) return; return f.apply(this,arguments); }; window.ouvreCercle.__v74=true; }
  var ps=document.getElementById('plusScreen'), avant=ps?ps.classList.contains('show'):false;
  if(ps) new MutationObserver(function(){ var s=ps.classList.contains('show'); if(s===avant) return; avant=s; if(s && membre()){ ps.classList.remove('show'); avant=false; } }).observe(ps,{attributes:true,attributeFilter:['class']});
  function mm(){ var m=document.querySelector('.acc-plat .acc-mm'); if(!m) return; if(membre()){ if(m.getAttribute('role')==='button'){ m.removeAttribute('role'); m.setAttribute('data-role-av','button'); } }
    else if(m.getAttribute('data-role-av')){ m.setAttribute('role','button'); m.removeAttribute('data-role-av'); } }
  var d=document.getElementById('device'), pv=d?d.classList.contains('premium'):false;
  if(d) new MutationObserver(function(){ var v=d.classList.contains('premium'); if(v===pv) return; pv=v; mm(); }).observe(d,{attributes:true,attributeFilter:['class']});
  setTimeout(mm,1500);
})();
