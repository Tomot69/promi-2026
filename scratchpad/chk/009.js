(function(){try{
var st={t:0};
var BX=52,BY=84,BR=3;
/* ⚑ CHANTIER 58 — 12 septembre 2026. UN ÉCRAN EST VISIBLE S'IL PORTE LA CLASSE QUE LE CODE POSE,
   JAMAIS PAR SA GÉOMÉTRIE (CLAUDE.md §8).
   Cette boucle tenait pour visible tout élément dont `offsetParent` n'est pas nul. Or un écran fermé
   n'est PAS en `display:none` : il est glissé hors champ (`transform:translateY(100%)`, opacité 0) et
   il GARDE son `offsetParent`. Elle écrivait donc `--gx`, `--gy`, `--grot` — trois propriétés
   personnalisées, donc HÉRITÉES — sur les DOUZE écrans, fermés compris, à chaque image ; et sa propre
   lecture d'`offsetParent` à l'image suivante forçait le recalcul de style de milliers de nœuds cachés.
   Mesuré au profileur (CDP, échantillon 0,5 ms) pendant l'Aura : 27 % du temps du fil principal, autant
   que tout le peintre de la sphère, 24 480 écritures en 20 s ; 1,6 % en ignorant les écrans cachés.
   Vécu : l'élan de l'Aura figé par des images de 267 ms. Le coût existait PARTOUT — Toile, Fil, Index,
   fiches — pas seulement sur l'Aura, que `lot-AURA-PELOTE` protégeait déjà à sa façon.
   ⚠ « .show » SEUL AURAIT ÉTEINT L'OMBRE SUR LE FIL. Vérifié avant d'écrire la parade, écran par écran
   et dans les deux thèmes (`sauvegardes/ch58/equivalence_show.py`) : `#feedView` est VISIBLE sans porter
   `.show` — il s'ouvre avec la classe `.in` et `display:''`, et l'app le lit elle-même comme ça
   (`fv.classList.contains('in') && getComputedStyle(fv).display!=='none'`, ≈ l. 19208). D'où les DEUX
   classes ci-dessous : ce sont les deux états que le code pose, et rien n'est déduit d'une géométrie. */
function ouvert(e){ return e.classList.contains('show') || e.classList.contains('in'); }
function frame(){
  var all=document.querySelectorAll('.tuto-fond, #createSheet, #settingsScreen');var vis=false;
  for(var i=0;i<all.length;i++){if(ouvert(all[i])){vis=true;break;}}
  if(vis){st.t+=0.0016;var x=BX*Math.sin(st.t*1.0)*Math.cos(st.t*0.37);var y=BY*Math.sin(st.t*0.63);var rot=BR*Math.sin(st.t*0.5);
    for(var j=0;j<all.length;j++){var e=all[j];if(ouvert(e)){e.style.setProperty('--gx',x.toFixed(2)+'px');e.style.setProperty('--gy',y.toFixed(2)+'px');e.style.setProperty('--grot',rot.toFixed(3)+'deg');}}
    requestAnimationFrame(frame);
  }else{setTimeout(frame,350);}
}
window._ombreOuvert=ouvert;   /* pour la preuve : le juge lit la même règle que la boucle */
requestAnimationFrame(frame);
}catch(e){}})();