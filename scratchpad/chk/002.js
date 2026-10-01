
/* ⚑ v111 (Tom, 30 sept. 2026) — « Dans un Cercle, le fond contraste déjà avec la flèche en mode sombre. Supprime dès maintenant
   les filets de la fiche et de la page +. » Le filet crème (sous le trait, et sur les segments des disques) n'existait que pour
   compenser un manque de contraste ; sur la fiche et la page + d'un Cercle il n'en manque pas. Une seule exception, nommée, lue par
   les trois peintres (le trait de la fiche, le trait de la page +, les disques). */
window._sansFiletCercle=function(el){ try{ return !!(el && el.closest && el.closest('#detailPoster.dp-nuee, #detailPoster.dp-mode-nuee, #createSheet[data-kind="nuee"], #createSheet.pp-nuee')); }catch(_){ return false; } };
