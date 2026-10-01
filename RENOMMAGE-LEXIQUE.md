# LE RENOMMAGE DU LEXIQUE — v106 (30 septembre 2026)

> **Décision Tom.** Deux changements, **les clés internes ne bougent pas** (`nuee`, `NUE`, `curNuee`, `.s2-cercle`,
> `ouvreCercle`, `isPremium`, `promi_murs`, les noms de lots) — seuls les noms AFFICHÉS changent, comme pour les mondes.
> 1 · **la Nuée devient un Cercle** (un groupe de gens autour de Promi et de Chiche).
> 2 · **le Cercle, l'offre payante, devient « Ma Parole ! »**.
> Formulations arrêtées : **Retourne ta Toile** (sous-titre de l'écran qui vend) · **Bon, allez d'accord** (bouton
> d'adhésion) · **Avec Ma Parole !** (partout où on nomme l'offre) · **Tu es Membre Ma Parole !** (Réglages).
> « Ma Parole ! » s'écrit avec une espace insécable avant le « ! » (comme la porte des Réglages, v105).

## 1 · Méthode du relevé

- **Source** : chaque chaîne JavaScript (échappements `é` décodés), chaque nœud de texte HTML, chaque `aria-label`,
  `placeholder`, `title` — commentaires exclus. `scratchpad/releve_lex.py` → 139 textes.
- **Contre-épreuve à l'écran** : l'app chargée (WebKit), Aura, offre et Réglages ouverts, tous les nœuds de texte du
  document, cachés compris — `scratchpad/tout_texte.py` : **zéro « Nuée » restant**. Balayage écran par écran, gratuit et
  payé (`scratchpad/balaye_lex.py`) : accueil, +, les trois pages +, Index, Fil, fiches et Peaufiner (Promi, Nuée), Aura,
  aide, Réglages, offre, Studio, Partager — zéro « Nuée », zéro « Cercle » au sens de l'offre.
- **Logique qui lit un libellé** : aucune (`=== 'Nuée'`, `indexOf`, regex) — vérifié. Seule dépendance : la table des
  largeurs de libellé des cartes (`W={'Promi':73,'Chiche':81,'Nuée':57}`, ×3) → **`'Cercle':76`** ajouté, mesuré police
  chargée (75,39 px, arrondi au-dessus comme les deux autres).

## 2 · L'offre → « Ma Parole ! » — ce qui a été posé

| Où | Avant | Après |
|---|---|---|
| Écran qui vend — plateau | Le Cercle | Ma Parole ! |
| Écran qui vend — grand titre | LE CERCLE | MA PAROLE ! (« PAROLE » en couleur, « ! » à l'encre, comme l'ancien « ! » de « Rejoins le Cercle ! ») |
| Écran qui vend — sous-titre | ta parole, et celle qu'on te tient | **Retourne ta Toile** |
| Écran qui vend — bouton principal | Essayer 14 jours › | **Essayer 14 jours ›** (v107 : l'essai reste) |
| Écran qui vend — option en dessous | ou le mois — 5,99 € | **Bon, allez d'accord — 39 € / an** (v107) |
| Réglages, payé | (porte cachée depuis v74) | **Tu es Membre Ma Parole !** — visible, sans lien |
| Aide de l'Aura — étiquette | Avec le Cercle | **Avec Ma Parole !** |
| Aide de l'Aura — encart (caché v104) | ✦ Le Cercle | ✦ Ma Parole ! |
| Aura — encart (caché v104) | ✦ Le Cercle | ✦ Ma Parole ! |
| Peaufiner — encart (caché v104) | ✦ Le Cercle | ✦ Ma Parole ! |
| Aura (ancien bloc karma) | Le Cercle | Ma Parole ! |
| Aura, ancienne ligne | ✦ Cercle — vois la réciprocité… | ✦ Ma Parole ! — vois la réciprocité… |
| Studio (caché v104) | Ou débloque-les tous · avec Le Cercle | … · Avec Ma Parole ! |
| Ancien verrou « Récurrence » | ✦ Récurrence & rappels · Le Cercle | ✦ Récurrence & rappels · Ma Parole ! |
| Ancienne page de l'offre (cachée) | Le Cercle / Le Cercle révèle l'inverse | Ma Parole ! / Ma Parole ! révèle l'inverse |
| Accueil, mot-marque (lecteur d'écran) | aria-label « Le Cercle » | « Ma Parole ! » |
| Phrases des murs | « Ma Parole ! » déjà | inchangées ; police **Gilbert** (était Atkinson 700) |

## 3 · Là où « Ma Parole ! » ne s'insère pas naturellement — trois formulations, (A) posée provisoirement

> ✅ **v107 (Tom) : les variantes A sont VALIDÉES** (Q355).
> ⚠ Sans ces changements, l'ancien « le Cercle » (l'offre) se serait lu comme un GROUPE : « ton Cercle » n'aurait plus
> voulu dire la même chose. (A) est donc posée pour ne rien laisser de faux à l'écran — **à valider**, QUESTIONS · Q355.

**P1 · le message après l'achat depuis l'Aura, et au déblocage** — *Le Cercle activé · Nuées illimitées* / *Le Cercle débloqué · Nuées illimitées*
- **A** · Tu es Membre Ma Parole ! · Cercles illimités *(posée)*
- **B** · C'est dit : Ma Parole ! · Cercles illimités
- **C** · Tope là — Ma Parole ! est à toi

**P2 · le message de bienvenue** — *Bienvenue dans le Cercle ✓ · tout Promi débloqué* (trois endroits)
- **A** · Tu es Membre Ma Parole ! ✓ · tout Promi débloqué *(posée — reprend la formule des Réglages)*
- **B** · Te voilà Membre Ma Parole ! ✓ · tout Promi débloqué
- **C** · Parole donnée ✓ · tout Promi débloqué

**P3 · aide de l'Aura, titre de carte** — *Les réglages du Cercle*
- **A** · Peaufiner, avec Ma Parole ! *(posée)*
- **B** · Les réglages de Ma Parole !
- **C** · Ce que Ma Parole ! peaufine

**P4 · aide de l'Aura, « Le double Noyau »** — *En activant ton Cercle, ton Noyau s'entoure de tes proches…*
- **A** · Avec Ma Parole !, ton Noyau s'entoure de tes proches… *(posée)*
- **B** · Dès que tu dis Ma Parole !, ton Noyau s'entoure de tes proches…
- **C** · Membre Ma Parole !, ton Noyau s'entoure de tes proches…

**P5 · ancienne page de l'offre (cachée aujourd'hui)** — *Thèmes et matières exclusives au Cercle.*
- **A** · Thèmes et matières, avec Ma Parole ! *(posée)*
- **B** · Des thèmes et des matières réservés à Ma Parole !
- **C** · Thèmes et matières que seule Ma Parole ! ouvre

## 4 · La Nuée → le Cercle — les accords qui cassaient (tous corrigés)

Le genre change (féminin → masculin). **Chaque phrase où l'accord cassait, et ce qui est posé :**

| Accord | Phrases |
|---|---|
| une → **un** | Un Cercle (tuile du +, pastille de l'accueil) · Dans un Cercle · Rechercher un Promi, un Cercle… · reprends un Cercle à la fois · Je lance un Cercle · ce que tu déposes dans un Cercle · DANS UN CERCLE · UN CERCLE T'ATTEND · Ou il ouvre un Cercle (tutoriel) · un Cercle permet (À propos) · un Cercle, et chacun y plante la sienne (sans porteur, §IDENTITE) |
| la → **le** · de la → **du** · à la → **au** | Lancer le Cercle · Trace pour lancer le Cercle · Dissoudre le Cercle · Tu as créé le Cercle · Planter (un Promi) dans le Cercle · visible(s) par le Cercle · présente le Cercle · Mettre le Cercle de côté · Partager le Cercle · Le nom du Cercle · Les Promi du Cercle · Promesses du Cercle · Aura du Cercle · Nom du Cercle · visibles par les membres du Cercle · selon le Cercle · + Ajouter un Promi au Cercle |
| ta / ma → **ton / mon** | Donne un nom à ton Cercle · Plante le premier Promi de ton Cercle → · Rejoins mon Cercle « … » (invitation) |
| cette / quelle / aucune → **ce / quel / aucun** | de quoi parle ce Cercle ? · renomme ou dissous ce Cercle · Ce Cercle (nom par défaut) · Dans quel Cercle · DANS QUEL CERCLE · aucun Cercle |
| adjectifs et participes | **Ton meilleur Cercle** (était Ta meilleure) · Le Cercle que tu honores le mieux ressort en premier — **celui** où (était celle) · Je lance un Cercle **nommé** · CERCLE **REJOINT** · 3 Cercles **offerts** · Cercles **illimités** (×3) · puis appuie sur Planter pour **le** créer · chacun de tes Cercles (était chacune de tes Nuées) · **Nouveau** Cercle (setHead, sans porteur) |
| sans accord | Par Cercle · Cercles · en Cercle · Promi en Cercle · Cercle · membres · déclinées Cercle par Cercle · N paroles · N Cercles · les mêmes Promi et Cercles · Promi, Toile, Cercle, Fil, Aura · chaque lien et chaque Cercle · par personne, par Cercle · sur chaque Promi, Chiche et Cercle · toile vide + 1 Cercle |

## 5 · Ce qui n'a PAS été fait, et ce qu'il faut savoir

- **PromiLate n'a pas de « ! »** (Tom, v108 : « ça va », gardé) (ni d'espace insécable — lu dans la table des caractères de l'OTF) : dans « MA PAROLE ! »
  (plateau et grand titre de l'offre), le « ! » vient de Gilbert, comme déjà dans la porte des Réglages. Il se voit.
- **v107 — l'essai revient en bouton principal** ; « Bon, allez d'accord — 39 € / an » prend l'option en dessous. L'offre au mois revient en petit
  sous les deux boutons (v108) : « ou 5,99 € par mois ».
- **« Brouillon de Cercle… »** (note d'un gardé de côté, `#dkNueeNote`, cachée) garde le mot banni « Brouillon » — antérieur.
- **Documents non touchés** : moodboards, planches, PARCOURS, SPECIFICATIONS, IDENTITE-VERBALE. Les commentaires du code
  gardent « Nuée » (interne). CLAUDE.md §2 est mis à jour.
- **Pas de dessin « Cercle »** : les titres restent en police (le titre de la fiche d'une Nuée l'était déjà).
