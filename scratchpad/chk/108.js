
/* ⚑ v20 · LES EXEMPLES QUI TOURNENT (Tom, 22 sept. 2026) — listes de Tom, mot pour mot
   (apostrophes typographiques). Première ouverture d'un type : le premier de la liste ;
   ensuite, un tirage. Nuée : on tire d'abord une CATÉGORIE, puis un nom dedans — les
   mariages sont nombreux, ils ne doivent pas écraser le reste. Un tirage PAR OUVERTURE. */
(function(){
  var L={"soi": ["me coucher le jour même", "finir ce livre avant d’en ouvrir trois", "apprendre enfin le nom de mes voisins", "faire la sieste sans culpabiliser", "arroser mes plantes avant qu’elles m’en veuillent", "prendre des nouvelles avant d’avoir une raison", "me garder une soirée pour moi", "trouver un nouveau hobby", "adopter un animal à la SPA", "retourner voir cet endroit que j’ai adoré", "commencer sans attendre le bon moment", "m’engager pour cette cause", "apprendre à jouer d’un instrument"], "demander": ["m’écrire quand tu es chez toi", "me prévenir si j’ai quelque chose entre les dents", "ne jamais parler comme sur Linkédine", "me dire si je commence à dire « ça fait sens »", "me dire si je commence à dire « disruptif »", "me dire si je commence à parler de « synergies »", "me partager ta recette", "me prévenir quand tu auras changé d’avis", "me dire si je deviens comme mes parents", "me rappeler cette histoire quand on sera vieux", "me rappeler de ne pas devenir raisonnable"], "chiche": ["dire oui pour une fois", "te baigner fin octobre", "te lever pour voir le soleil se lever", "dormir à la belle étoile", "choisir une ville au hasard", "partir demain matin", "faire cette chose qu’on n’a jamais faite", "nous faire confiance et voir où ça mène", "dire oui sans demander pourquoi", "faire le Mont Blanc", "te mettre à la salsa", "monter un groupe", "prendre un cours de trapèze", "courir notre premier marathon", "apprendre une nouvelle langue", "apprendre à jouer d’un instrument", "faire un trek de plusieurs jours", "apprendre à naviguer"]}, NU={"projets": ["Week-end à Marseille", "La coloc", "Le club de lecture", "Le club de running", "Les 42 kilomètres", "L’apéro qu’on repousse depuis mars", "La maison qu’on veut construire", "Notre tour du monde", "Le voyage qu’on repousse", "Notre premier festival", "La maison de campagne", "Le projet qu’on mijote depuis deux ans"], "road": ["Le road trip des parkings de supermarché", "Le road trip en Meuse", "Le road trip des plus beaux ronds-points", "Le road trip des zones pavillonnaires", "Le road trip des sous-préfectures", "Le road trip des ZAC", "Le road trip des zones commerciales", "Le road trip des aires de repos"], "mariages": ["Le mariage de Philippine et Pascal", "Le mariage de Huguette et Jean-Roch", "Le mariage de Blandine et Bruno-Stanislas", "Le mariage de Nadine et Bernard-Guy", "Le mariage de Monique et Didier-Régis", "Le mariage de Chantal et Jean-Guy", "Le mariage de Fabienne et Thierry-Alain", "Le mariage de Corinne et Michel-Régis", "Le mariage de Raymonde et Gérard-Yves", "Le mariage de Gisèle et Rodolphe", "Le mariage de Huguette et Mireille", "Le mariage de Ginette et Gisèle", "Le mariage de Jean-Roch et Jean-Guy", "Le mariage de Didier-Régis et Rodolphe", "Le mariage de Bruno-Stanislas et Pascal", "Le mariage de Thierry-Alain et Bernard-Guy", "Le mariage de Michel-Régis et Gérard-Yves", "Le mariage de Jean-Noël et Alain-Gilbert"]};
  window._ppExemplesListes={L:L, NU:NU};
  /* pour les juges : oublier le tirage de l'ouverture en cours (les scènes s'enchaînent sans refermer la page +) */
  window._ppExempleRaz=function(){ choix={}; };
  var choix={};
  function cpt(t){ try{ return +(localStorage.getItem('promi_ex_'+t)||0); }catch(e){ return 0; } }
  function inc(t){ try{ localStorage.setItem('promi_ex_'+t, ''+(cpt(t)+1)); }catch(e){} }
  function tire(a){ return a[Math.floor(Math.random()*a.length)]; }
  window._ppExemple=function(t){
    /* la phrase se rend aussi page + FERMÉE (au chargement) : ça n'est pas une ouverture */
    var cs0=document.getElementById('createSheet');
    if(cs0 && !cs0.classList.contains('show')) return t==='nuee' ? NU.projets[0] : (L[t]||[''])[0];
    if(choix[t]) return choix[t];
    var n=cpt(t), v;
    if(t==='nuee'){ v = n ? tire(NU[tire(Object.keys(NU))]) : NU.projets[0]; }
    else { var a=L[t]||['']; v = n ? tire(a) : a[0]; }
    inc(t); choix[t]=v; return v;
  };
  /* une nouvelle ouverture de la page + = un nouveau tirage */
  var cs=document.getElementById('createSheet');
  if(cs){ var ouv=cs.classList.contains('show');
    new MutationObserver(function(){ var o=cs.classList.contains('show'); if(o===ouv) return; ouv=o; if(o) choix={}; })
      .observe(cs,{attributes:true,attributeFilter:['class']}); }
})();
