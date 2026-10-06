# TEXTES — les chaînes de Promi, mode d'emploi et trous

> Compagnon de `portage/TEXTES.json`. Extrait de `app.html` et de `promi-moteur.js` le 6 octobre 2026 (arbre de travail après le
> commit `ceac9ac` « v133 », modifications v134 non commitées comprises). **Lecture et extraction seulement** : aucun mot n'a été
> écrit pour ce document, aucun navigateur n'a été lancé — ce qui suit est lu dans la SOURCE, pas relevé à l'écran.

## 1 · Comment lire la table

`TEXTES.json` = `{ "_meta": …, "textes": { "<clé>": { … } } }`. **330 clés, 967 chaînes** (une clé peut porter des
variantes et une liste).

| Champ | Ce qu'il porte |
|---|---|
| `fr` | le texte exact, au caractère près |
| `ou` | l'écran et l'endroit |
| `source` | `app.html:ligne (bloc)` — le bloc est le `lot-…` qui contient la ligne ; « HTML statique » = le balisage d'origine (lignes 2541–2836) |
| `variantes` | pluriels, accords, états, valeurs par défaut, sous-titres |
| `gabarit` | la chaîne à trous ; les trous sont entre accolades : `À {personne}`, `Avec {a}, {b}, +{n}`, `{n} PROMI · {t} TENU(S)` |
| `voiceover` | le libellé du lecteur d'écran (les `aria-label` du prototype) |
| `liste` | les éléments d'une liste ordonnée (suggestions, mondes, palettes, phrases des murs…) |
| `regle` | la règle de tirage, d'accord ou d'affichage |
| `casse` | ce que l'écran affiche quand la feuille de style change la casse de la source |
| `etat` | **présent seulement si la chaîne n'est pas sûre d'être affichée aujourd'hui** (section 4) |

**Les clés** sont stables et hiérarchiques : `onb.*` · `accueil.*` · `plus.*` · `trait.*` · `fiche.*` · `peauf.*` · `cercle.*` · `index.*` ·
`carte.*` · `fil.*` · `aura.*` · `studio.*` · `partage.*` · `reglages.*` · `notifs.*` · `offre.*` · `murs.phrases` · `dessin.*` · `photo.*` ·
`dialogue.*` · `message.*` · `apropos.*`. Un élément de liste se désigne par son rang : `murs.phrases[3]` = `liste[2]`.

**Les caractères — à ne jamais « normaliser » :**
- apostrophe typographique `’` (U+2019) presque partout ; **quelques chaînes de la source portent l'apostrophe droite `'`**
  (« une parole qu'on donne », « C'EST IMPORTANT ? », « aujourd'hui », « à l'instant ») : elles sont recopiées telles quelles — à
  harmoniser sur décision, pas en silence ;
- **« Ma Parole ! » porte TOUJOURS une espace insécable (U+00A0) avant « ! »** ; dans les phrases des murs, l'espace avant « ? » est
  insécable aussi ; « Toi, c’est … ? » (onboarding) et « Qu’est-ce que tu promets ? » également ;
- ailleurs, l'espace avant « ? » et « : » est une espace ORDINAIRE dans la source (« qui ? », « Je te le rappelle ? », « Supprimer ce
  Promi ? ») — recopié tel quel ;
- les guillemets « » sont suivis et précédés d'une espace ordinaire ; points de suspension = le caractère `…` ;
- « touche‑le » (aides de la page +) porte un trait d'union insécable U+2011 ; « 3,25 €/⁠mois » porte U+2060 après la barre ;
- « Promi » est invariable ; « Cercle » est masculin (clé interne `nuee`) ; l'offre est « Ma Parole ! ».

**Les mots en capitales.** Beaucoup de libellés sont écrits en capitales DANS la source (« À QUI », « PIÈCES JOINTES », « TENUE ») :
ils sont recopiés ainsi. D'autres sont en bas de casse dans la source et montés en capitales par la feuille de style (la barre
STUDIO · AURA · INDEX · FIL, les phrases du trait, « CE QUE TU AS TENU ») : `fr` donne la source, `casse` dit ce que l'écran affiche
quand `CLAUDE.md` ou un juge le fixe. Voir le trou T2.

## 2 · Le nombre de clés par écran

| Écran | clés | chaînes | à confirmer |
|---|---|---|---|
| Commun | 10 | 19 | 0 |
| Onboarding | 21 | 22 | 2 |
| Accueil et barre | 19 | 25 | 5 |
| Page + | 54 | 200 | 6 |
| Échéances | 1 | 8 | 0 |
| Le pinceau (LE TRAIT) | 2 | 14 | 0 |
| Le trait (phrases) | 12 | 14 | 2 |
| Fiches | 15 | 36 | 2 |
| Mots du temps | 2 | 17 | 0 |
| L’instant | 3 | 5 | 0 |
| Peaufiner (fiche) | 15 | 35 | 1 |
| Le Cercle | 19 | 41 | 4 |
| Index | 7 | 25 | 1 |
| Cartes (Index et Fil) | 4 | 19 | 0 |
| Fil | 9 | 56 | 1 |
| Aura et son aide | 15 | 35 | 2 |
| Fiche d’une personne | 5 | 8 | 1 |
| Studio | 14 | 81 | 4 |
| Partager | 18 | 50 | 0 |
| Réglages | 20 | 40 | 2 |
| Vie privée | 2 | 10 | 0 |
| La langue | 1 | 4 | 1 |
| Légal | 1 | 2 | 0 |
| À propos | 7 | 29 | 0 |
| Notifications | 11 | 17 | 0 |
| Offre Ma Parole ! | 10 | 28 | 1 |
| Murs de Ma Parole ! | 1 | 19 | 0 |
| Mode dessin | 13 | 23 | 0 |
| Menu photo | 5 | 6 | 0 |
| Dialogues | 5 | 21 | 0 |
| Messages | 6 | 7 | 0 |
| Anciens écrans | 3 | 51 | 3 |
| **Total** | **330** | **967** | **38** |

## 3 · Les TROUS (⚠) — ce que la source ne donne pas

| N° | Trou |
|---|---|
| T1 | **Aucune variante « vous » de l'interface.** Le prototype tutoie partout. Seules formes plurielles trouvées : « promettez-moi » (verbe de la page +) et les suggestions « A / B » (« t’emmener voir la mer / vous emmener voir la mer »). |
| T2 | **La casse AFFICHÉE n'est pas relevée** (aucun navigateur lancé). Pour chaque libellé en bas de casse dans la source, vérifier à l'écran s'il paraît en capitales (`text-transform`) : la barre, les phrases du trait, les titres de l'Aura, « sombre / clair », « avec texte », « Poser », « Trait / Fond », « encore aucune parole ». |
| T3 | **Les dates relatives n'ont pas de règle.** « DEPUIS LE 4 AVRIL », « 3 AOÛT », « PAS ENCORE RELEVÉ » sont des DONNÉES du jeu de démonstration (`leJour`) ; « il y a 2 h », « hier », « récemment » sont posées à la main dans le Fil. Seules règles écrites : `temps.mots` (échéance → mot) et « À TENIR · DEMAIN / · {n} JOURS » sur une carte. Aucun « DANS 2 JOURS » dans la source. |
| T4 | **VoiceOver est presque vide.** Le prototype ne porte un libellé que sur une vingtaine d'éléments (champ `voiceover`). Rien pour : le + de l'accueil, les cinq entrées de la barre, les cartes de l'Index et du Fil, les Noyaux, la Pelote, les réglages de Peaufiner, les disques du Studio, les pastilles de palette, les dalles. Le Zzz (« Mode nuit, activé / désactivé ») n'est donné que par `CLAUDE.md`. |
| T5 | **Aucun texte légal** : Conditions d'utilisation et Politique de confidentialité affichent « Bientôt disponible. ». |
| T6 | **Aucun crédit pour PromiLate** dans À propos ; le texte dit « Les titres sont en Gilbert », écrit avant PromiLate. |
| T7 | **Messages d'erreur : deux seulement** (« Copie impossible ici », « indisponible ici »). Rien pour : réseau, achat refusé ou annulé, restauration d'achat, connexion Apple / Google échouée, import de photo refusé, permission de notification refusée. |
| T8 | **Achat** : aucun texte de confirmation, de fin d'essai, de renouvellement ni de « Restaurer mes achats » (exigé par l'App Store). |
| T9 | **États vides** : aucun texte trouvé pour un Index vide, un Fil vide, une recherche sans résultat. (Toile vide : `accueil.vide.*`, à confirmer ; Aura vide : `aura.vide`.) |
| T10 | **Accords restés au féminin** (restes de « Nuée ») : « aucune » comme valeur de DANS UN CERCLE, « « {nom} » dissoute ». Et « {personne} tracera sa part si **elle** ose » : le pronom est en dur. À valider par Tom. |
| T11 | **Aide de l'Aura** : « Tes paroles tenues, dans l’ordre où tu les as tenues » — depuis v132 la liste montre la plus récente en premier. À valider. |
| T12 | **La feuille « Inviter »** (note « 3 Cercles offerts… », `#shInviteNote`) n'a pas été relevée au-delà du texte d'invitation `partage.invitation`. |
| T13 | **Partager · DANS L'IMAGE** : « La Pelote » est sûre ; « Promitteurs », « Disques », « Harmonie chiffrée », « Jauge équilibre » viennent du HTML statique d'août — lesquels restent affichés n'est pas établi. |
| T14 | **Descriptions des mondes et des pinceaux** : présentes dans les tables (`studio.mondes.descriptions`, `pinceau.noms`), leur affichage n'est pas établi. Douze mondes sur vingt n'ont de description que dans `STRUCT` (toutes y sont, v33). |
| T15 | **Le Zzz est COUPÉ** (v120) : son libellé « Zzz » et ses annonces viennent de `CLAUDE.md`, pas du code affiché. |
| T16 | **Le gardé de côté sur la page +** (`plus.garde.*`) et **les demandes** (`fiche.demande`, « Demandes » des menus de tri) : chemins d'août, vivants ou non — à confirmer. |
| T17 | **Menus de tri de l'Index et du Fil** : lus dans le HTML statique ; « Manquées », « En suspens », « Demandes », « Mes proches » sont des mots d'août, non recoupés avec un juge. |
| T18 | **Le mot « Noyau »** survit dans « Belle série — partage ton Noyau » (`fil.serie`) alors que la boule s'appelle la Pelote. |

## 4 · À CONFIRMER (peut-être morte)

Chaînes lues dans la source mais dont l'affichage aujourd'hui n'est pas sûr (HTML d'origine, encarts cachés depuis v104, chemins
remplacés). **Aucune n'est à porter sans vérification à l'écran.**

| Clé | Texte (début) | État | Source |
|---|---|---|---|
| `onb.concept.titre` | Ici, c’est Promi. Et ça veut dire quelque chose. | à confirmer (peut-être morte) | app.html:36307 (lot-ONB-V20) |
| `onb.concept.texte` | Un Promi, c’est ta parole. Un Chiche, celle que tu lances à quelqu’un. | à confirmer (peut-être morte) | app.html:36308 (lot-ONB-V20) |
| `accueil.vide.titre` | Ta Toile n’attend que toi | à confirmer (peut-être morte) | app.html:2553 (HTML statique) |
| `accueil.vide.texte` | Plante ton premier Promi — touche le + | à confirmer (peut-être morte) | app.html:2553 (HTML statique) |
| `accueil.vide.nudge` | chaque parole tenue devient une dalle | à confirmer (peut-être morte) | app.html:2553 (HTML statique) |
| `accueil.ancien.sousTitre` | la Toile attend | à confirmer (peut-être morte) | app.html:2546 (HTML statique) |
| `accueil.ancien.motMarqueVO` | Ma Parole ! | à confirmer (peut-être morte) | app.html:2548 (HTML statique) |
| `plus.garde.phrase` | Je garde une idée | à confirmer (peut-être morte) | app.html:13378 (da3-draft-phrase-js) |
| `plus.garde.titreVide` | le titre | à confirmer (peut-être morte) | app.html:13378 (da3-draft-phrase-js) |
| `plus.garde.pour` | pour | à confirmer (peut-être morte) | app.html:13379 (da3-draft-phrase-js) |
| `plus.garde.quand` | y revenir un jour | à confirmer (peut-être morte) | app.html:13376 (da3-draft-phrase-js) |
| `plus.garde.champ` | CE QUE TU GARDES | à confirmer (peut-être morte) | app.html:13388 (da3-draft-phrase-js) |
| `plus.garde.champInvite` | une idée, un projet… | à confirmer (peut-être morte) | app.html:13388 (da3-draft-phrase-js) |
| `trait.vo.boutonOuTrait` | trait ou bouton | à confirmer (peut-être morte) | app.html:4589 (script principal) |
| `trait.vo.mettreDeCote` | Trace pour mettre de côté | à confirmer (peut-être morte) | app.html:2591 (HTML statique) |
| `fiche.ancien.paroleTenue` | PAROLE TENUE | à confirmer (peut-être morte) | app.html:6153 (script principal) |
| `peauf.mp.encart` | ✦ Ma Parole ! | à confirmer (peut-être morte) | app.html:16240 (lot-S2-peaufiner) |
| `cercle.etat.extras` |   ·  une note  ·  {n} fichier(s)  ·  {n} mot(s) | à confirmer (peut-être morte) | app.html:5777 (script principal) |
| `cercle.peauf.planter` | Planter un Promi dans le Cercle | à confirmer (peut-être morte) | app.html:16306 (lot-S2-peaufiner) |
| `cercle.dissoudre.ancien` | Dissoudre le Cercle ? | à confirmer (peut-être morte) | app.html:3662 (script principal) |
| `cercle.invitation` | Rejoins mon Cercle « {nom} » sur Promi — nos Promi, tenus ensemble. ht | à confirmer (peut-être morte) | app.html:3660 (script principal) |
| `index.onglets` | Récent | à confirmer (peut-être morte) | app.html:2642 (HTML statique) |
| `fil.serie` | Belle série — partage ton Noyau | à confirmer (peut-être morte) | app.html:6906 (script principal) |
| `aura.encartMP` | ✦ Ma Parole ! | à confirmer (peut-être morte) | app.html:30067 (lot-AURA-PELOTE) |
| `aura.aide.encartMP` | ✦ Ma Parole ! | à confirmer (peut-être morte) | app.html:33269 (lot-HUIT) |
| `personne.legende` | en cours | à confirmer (peut-être morte) | app.html:31076 (lot-PERSONNE-AVEC) |
| `studio.mondes.descriptions` | taches d’encre abstraites, une par dalle | à confirmer (peut-être morte) | app.html:2896 (script principal) |
| `studio.zzz` | Zzz | COUPÉ (v120) — le Zzz est coupé partout jusqu’à nouvel ordre ; libellés donnés par CLAUDE.md, non relevés dans le code | CLAUDE.md v118 (lot-V118-ZZZ) |
| `studio.ancien.debloque` | Ou débloque-les tous | à confirmer (peut-être morte) | app.html:2774 (HTML statique) |
| `studio.ancien.paletteTeinte` | Palette · Teinte | à confirmer (peut-être morte) | app.html:6661 (script principal) |
| `reglages.reinitTest` | Réinitialiser (test) | outil de test du prototype — à ne pas porter | app.html:2766 (HTML statique) |
| `reglages.langue` | Langue | masqué (`hidden`) dans le prototype | app.html:2767 (HTML statique) |
| `langue.page` | La langue | à confirmer (peut-être morte) | app.html:2733 (HTML statique) |
| `offre.ancienne` | Essaie tout, sans t'engager. | à confirmer (peut-être morte) | app.html:2783 (HTML statique) |
| `mort.ancienOnboarding` | Tes promesses, tenues. | à confirmer (peut-être morte) | app.html:7886 (HTML statique, `#promiOnb`) |
| `mort.ancienneAura` | ta parole dans le temps | à confirmer (peut-être morte) | app.html:2696 (HTML statique) |
| `mort.ancienFormulaire` | Le Promi | à confirmer (peut-être morte) | app.html:2580 (HTML statique) |
| `fiche.demande` | En attente de ta parole | à confirmer (peut-être morte) | app.html:4131 (script principal) |

## 5 · Ce qui a été laissé hors de la table, et pourquoi

- **Le jeu de démonstration** (titres des Promi « faire les crêpes », « planter un arbre », noms « Rachel », « Marion »…) : ce sont des
  données, pas des chaînes de l'app.
- **Le cadre `?mesure=1`** (« MESURE DE LA PELOTE — ne touche à rien… ») et « Réinitialiser (test) » : outils du prototype.
- **Les 21 phrases des murs de v132** : remplacées en v133 par les dix-huit de `murs.phrases` (`MA-PAROLE-PHRASES.md` les garde pour l'histoire).
- **Les termes bannis** (`CLAUDE.md` §2) ne figurent que dans la section 4, pour qu'on sache d'où ils viendraient : « En replanter un »,
  « Belle parole », « Brouillon de Cercle… ».
- **Le texte de la licence SIL OFL 1.1** (anglais, long) : il est dans `app.html:35833`, à embarquer tel quel.

## 6 · Comment ça a été vérifié

Chaque `fr`, chaque variante et chaque élément de liste non composé a été recherché **à l'identique** dans la source décodée
(`\uXXXX`, entités HTML) : les seuls non retrouvés sont des chaînes COMPOSÉES par le code (« 9 PROMI · 3 TENUS », « TENUE · À
L’INSTANT ») ou réparties sur un saut de ligne — elles portent un `gabarit` ou une note. Les phrases des murs, les suggestions, le
texte d'À propos, les noms des mondes, des palettes et des pinceaux sont **extraits par programme**, jamais recopiés à la main.
Le JSON se vérifie par `python3 -c "import json;json.load(open('portage/TEXTES.json'))"`.
