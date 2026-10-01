
/* ⚑ CHANTIER 63 — UNE SEULE FICHE PAR PERSONNE, QUEL QUE SOIT LE CHEMIN (Tom, 11 sept. 2026 : « on touche son nom ou son
   visage et on arrive sur la même fiche […] Si un endroit affiche une personne sans y mener, c'est un chemin manquant,
   pas une seconde fiche à créer »). Relevé au doigt (QUESTIONS.md Q195) : ces lignes écrivaient des personnes en toutes
   lettres, et un toucher n'y faisait rien —
     · la ligne « à qui » d'une fiche (#dptQui) : « À Rachel », « À Marion · avec Rachel », et sur une Nuée
       « Avec Rachel, Adrien, +3 » — depuis une Nuée, AUCUN chemin ne menait à ses membres ;
     · les membres dans le Peaufiner d'une Nuée (.np-val) : « Rachel · Adrien · +3 ».
   Désormais le nom touché mène à SA fiche : openPerson, le même chemin que les Noyaux de l'Aura et les disques d'une fiche
   (closeAll puis openPerson, comme le disque, l. 3356). Aucune forme neuve, aucun nœud ajouté : ces textes sont réécrits par
   leurs peintres ; le toucher lit LE MOT sous le doigt (caretRangeFromPoint) et ne l'accepte que s'il est une personne
   connue (peopleList) — jamais « moi », « le groupe », « +3 » ni « autres ». Un glissement n'ouvre rien, et la porte
   s'ouvre sur le clic, pas au lever du doigt : c'est la porte commune de lot-DALLE-PORTE (`_porteAuDoigt`), et sa raison.
   PAS ICI, et pourquoi :
     · les rangées « À QUI » / « AVEC » du Peaufiner d'un Promi — la rangée accueille le champ qui CHANGE le destinataire :
       un toucher y règle, il ne navigue pas ;
     · « toi » — le mode « moi » n'a pas de fiche (décision de produit, audit § B bis) ;
     · le nom ou le visage DANS une carte du Fil ou de l'Index — la carte entière ouvre sa parole (§5) : question Q195. */
(function(){ try{
  if(typeof window._porteAuDoigt !== 'function') return;
  function gens(){
    var L = []; try{ L = (typeof peopleList === 'function') ? peopleList() : []; }catch(e){}
    return L.filter(function(n){ n = (''+n).trim(); return n && n !== 'moi' && n !== 'le groupe' && !(typeof _isMe === 'function' && _isMe(n)); })
            .sort(function(a, b){ return b.length - a.length; });            /* le plus long d'abord : « Marie-Jo » avant « Marie » */
  }
  /* le nom sous le doigt : le nœud de texte et la position du caractère, puis la personne dont une occurrence
     (bornée par des non-lettres) couvre ce caractère */
  function nomSous(x, y, hote){
    var r = document.caretRangeFromPoint ? document.caretRangeFromPoint(x, y) : null;
    if(!r || !r.startContainer || r.startContainer.nodeType !== 3 || !hote.contains(r.startContainer)) return null;
    var t = r.startContainer.textContent, o = r.startOffset, L = gens();
    var lettre = /[A-Za-zÀ-ÖØ-öø-ÿ'’-]/;
    for(var i = 0; i < L.length; i++){
      var n = L[i], k = -1;
      while((k = t.indexOf(n, k + 1)) >= 0){
        var avant = k > 0 ? t.charAt(k - 1) : '', apres = t.charAt(k + n.length);
        if((avant && lettre.test(avant)) || (apres && lettre.test(apres))) continue;
        if(o >= k && o <= k + n.length) return n;
      }
    }
    return null;
  }
  window._porteAuDoigt('#dptQui, .np-val', function(h, x, y){
    var n = nomSous(x, y, h);
    if(!n || typeof window.openPerson !== 'function') return false;
    try{ if(typeof closeAll === 'function') closeAll(); }catch(_){}
    window.openPerson(n); return true;
  }, null);
}catch(e){} })();
