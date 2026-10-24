# Audit des boutons et des options — écran par écran

**Date :** 24 octobre 2026, lot v162, C-186.
**Méthode :** lecture du code de `app.html` (copie de travail : commit `6238e8a` plus les modifications non commitées du lot v162) et de `joignable-inventaire.md`. Aucune modification de l'app, aucun navigateur, aucun banc.
**Non vérifié :** rien n'a été joué au doigt. Les retours d'écran, les gestionnaires absents et les effets « sans effet » sont lus dans le code, pas constatés à l'écran. Chaque cas douteux est marqué « non vérifié ». Les numéros de ligne renvoient à `app.html`.

Comment lire les tableaux : une ligne par bouton ou option. « — » veut dire rien à signaler. La recommandation commence toujours par l'un des cinq verbes : garder, fusionner, déplacer, renommer, supprimer.

---

## 1 · Accueil

On y arrive à l'ouverture de l'app, ou en fermant la plupart des écrans. Le plateau et la barre sont posés par `lot-ACCUEIL` (l. 34125).

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Mot-marque « Promi » (`span.acc-mm`) | Ouvre Ma Parole ! (`ouvreCercle`, l. 36000). Sans effet pour un membre (l. 38748). | Réglages « Ma Parole ! », les murs | — | Rien ne montre que c'est un bouton. VoiceOver dit « Ma Parole ! » alors que l'écran montre « Promi ». Le mot-marque des autres écrans n'ouvre rien. | Supprimer cette porte invisible, ou la montrer |
| `#shareBtn` (icône Partager, 44 × 44) | `openShare()` (l. 7879). La page s'ouvre sur le dernier sujet choisi, sans remise à zéro. | Rond Partager des fiches, « Partager ma Pelote » | — | Icône de 28 px et trait 2 ici ; 22 px et trait 2,6 sur la fiche (l. 6454) | Garder ; rouvrir toujours sur « Ma Toile » ; une seule icône |
| `#settingsBtn` (icône curseurs) | Ouvre les Réglages (l. 3304) | — | — | Même famille d'icône que le ⇅ de l'Index, que Tom appelle déjà « le bouton Réglages » (connu) | Garder |
| Toucher une dalle | Ouvre sa fiche (ou celle du Cercle) 260 ms après le lever, le temps de détecter un double toucher (l. 7005) | — | — | — | Garder |
| Double toucher | Recadre la Toile (l. 7004) | Rond « recadrer » | — | — | Garder |
| Rond « recadrer » (`#accRecadre`) | Recadre ; ne paraît que si la main a déplacé la vue (l. 34264) | Double toucher | — | Libellé VoiceOver en minuscule | Garder |
| Pincer, glisser | Zoom et déplacement de la vue. Au recul maximal, plateau, barre et recadrer deviennent intouchables (`lot-ZOOM-V46`). | — | Au recul maximal, aucun bouton : il faut pincer ou toucher deux fois | — | Garder |
| Appui de 0,8 s sur une dalle | Déplace la dalle (moteur). Inactif sous Ritournelle (`_TIRE_NON`, l. 8161). | — | Sous Ritournelle le geste ne fait rien, sans le dire | Le geste dépend du monde | Garder |
| `#studioBtn` STUDIO | Ouvre le Studio (l. 3320) | Réglages « Le Studio » | — | Libellés de la barre en Atkinson (l. 34078) ; le §6 veut la navigation en Gilbert capitales | Garder |
| `#souffleBtn` AURA | Ouvre l'Aura (l. 3313) | — | — | Comme STUDIO | Garder |
| `#createBtn` + | Au doigt : ouvre ou ferme le menu des trois natures (l. 34214) | — | — | — | Garder |
| Menu du + : Un Cercle, Un Chiche, Un Promi | Ouvre la page + de la nature choisie (l. 34164-34224) | Écran des tuiles de la page + (devenu inaccessible au doigt) | Un toucher hors du menu le ferme sans arrêter le toucher : sur une dalle, il ouvrirait aussi sa fiche (non vérifié) | Sous-titres « à quelqu'un, ou à toi / un défi lancé / un groupe, un projet » ; les tuiles disent « une parole qu'on donne / tu oses le lancer / on s'y met ensemble » | Garder |
| `#filBtn` FIL et sa pastille `#filDot` | Ouvre le Fil (l. 6523). La pastille dit qu'une parole attend un geste. | — | — | Un point : dette nommée de la loi des points | Garder |
| `#indexBtn` INDEX | Ouvre l'Index (l. 34156) | — | — | — | Garder |
| Bandeau `#accRappel` « Garder ta Toile · Plus tard » | Revient après chaque « Plus tard » : 5, 10 puis 20 paroles, ou 3, 7 puis 14 jours, puis encore, sans fin (l. 38597-38620) | Réglages « Garder ta Toile », panneau du compte de l'onboarding | « Garder ta Toile » mène à Apple et Google, non branchés (voir 27) | Contraire au §12 (« redemande d'un choix déjà fait »), même si c'est une décision de v52 | Supprimer la relance après le deuxième refus (à trancher) |
| Question « Je te le rappelle ? oui · pas besoin » | Après la plantation d'une parole datée ; deux refus et plus jamais (l. 39400) | — | — | Conforme à v109 | Garder |
| Toile vide « … touche le + » | Texte seul (l. 2704) | — | — | Impératif (A3) | Renommer (tourner sans impératif) |
| Code mort | `#accLigne` masqué mais son minuteur tourne (l. 34235) ; `#cercleTopBtn`, `#brandBtn` dans une barre masquée ; minuteur d'appui de 480 ms qui ne fait plus rien (l. 6958) ; `#enrToile` bien retiré (l. 40680) | — | — | — | Supprimer |

## 2 · Page + d'un Promi

On y arrive par le menu du +, par « + Planter un Promi » sur la fiche d'une personne, ou par « + Planter dans le Cercle ».

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme la page (l. 3240). La phrase écrite est perdue, sans avertissement. | — | Rien n'est gardé de côté | — | Garder |
| Bouton photo `.ph-photo-btn` | Menu : Dessiner, Importer une photo (l. 40442) | — | — | Contour 1,5 px à 42 %, fond translucide, flou de 3 px (l. 20767) : hors de la grammaire des contours et de la règle « pas de flou hors des murs » | Garder ; contour plein de 2 px, sans flou |
| Le trait `#planterZone` | Plante (moitié du trait) | — | Tracé sans titre : `promiRequis` vibre et met le focus sur un champ masqué (l. 8981) ; aucun retour visible lu dans le code (non vérifié) | L'onboarding, lui, ouvre la saisie quand on trace sans parole | Garder ; ouvrir la saisie du titre comme l'onboarding |
| « Je me promets » (⇄) | Fait tourner le sens : à soi → « Je promets à … » → « promets-moi » (l. 5642) | — | — | — | Garder |
| Le quoi (texte en pointillés) | Ouvre la saisie ; deux pastilles « DÉJÀ PROMIS » remplissent le champ | Les suggestions qui tournent | L'exemple en pointillés n'est pas repris si l'on trace sans écrire (non vérifié) | — | Garder |
| Le à qui (« qui ? ») | Ouvre le choix des personnes, « Moi » en tête (l. 33791) | Peaufiner « À QUI » | — | Dans Peaufiner la liste n'a pas « Moi » (l. 33852), contraire au §5 | Fusionner : un seul choix, avec « Moi » |
| « + ajouter quelqu'un », la zone en pointillés, le + orange | Ajoute un nom (24 lettres au plus) | — | — | Écrit en bas de casse ; la fiche d'une personne écrit « + Planter un Promi » | Garder |
| Rail du pinceau : Plein, Coulé, Peigné, Sec | Choisit le trait de cette parole (l. 25856) | Peaufiner « LE TRAIT » | Douze pastilles bâties, le rail est en `overflow:hidden` et aucun code ne le fait glisser : les huit traits payants ne se voient pas (non vérifié au doigt) | Quatre pastilles visibles ici (390 pt), trois dans Peaufiner (298 pt). Le prix « — 0,50 € » n'est écrit que dans Peaufiner. | Garder, rendre le rail glissant ou n'afficher que les quatre libres |
| « garder de côté » | Inactif tant que rien n'a changé ; actif, enregistre la page et la ferme (`lot-V162-GARDER`, l. 41822) | Anciens boutons masqués `#gcPromi`, `#gcNuee` | — | Inactif, il reste visible et ne fait rien | Garder |
| `#csBotBar` (barre « Peaufiner ▾ ») | Ouvre le Peaufiner de la page + (l. 18651) — voir 5 | — | — | Pas d'icône Partager (exception écrite au §3.2, contraire au §5) | Garder |
| Écran des trois tuiles « CHOISIR → » | Ne paraît plus au doigt depuis le menu du + ; seulement en repli du guide (l. 41089) | Menu du + | — | Sous-titres différents de ceux du menu du + | Supprimer |
| Code mort | `#draftForm`, `#planterZoneD`, `#addDraft` ; les choix `'nuee'` et `'quand'` de `_phraseChoix` | — | — | — | Supprimer |

## 3 · Page + d'un Chiche

Ce qui diffère du Promi.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| « qui ose ? » | Choix de la personne défiée | Peaufiner « À QUI JE LANCE » | — | Trois noms pour la même case : « qui ose ? », « QUI TU DÉFIES » (titre du panneau), « À QUI JE LANCE » | Renommer : un seul mot |
| « Chiche » | Porte `data-ph="sens"` mais ne fait rien (`if(P.sens==='chiche') return`, l. 5641) | — | Paraît touchable, ne fait rien | Le « Je me promets » du Promi, au même rang, se touche | Supprimer la prise (texte inerte) |
| « qui en est ? » | Choix des compagnons | Peaufiner « AVEC » | — | — | Garder |
| Le trait | Lance (moitié du trait) | — | — | Mot du trait « trace pour lancer », mais VoiceOver dit « Trace pour planter » | Renommer le libellé VoiceOver |

## 4 · Page + d'un Cercle

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Le nom du Cercle | Saisie du nom | — | Sans nom, un « garder de côté » l'enregistre « (sans titre) » | — | Garder |
| « tout le monde » | Choix des membres, « tout le monde » puis « Moi » en tête (`_nueeChoix`, l. 13658) | Peaufiner « MEMBRES » et « INVITER → » | — | Ces deux rangées de Peaufiner n'ont ni « tout le monde » ni « Moi » | Fusionner |
| Bouton photo | Propose « Importer une photo » | — | Un Cercle ne porte pas de photo : ce qu'elle devient au lancement n'est pas lu (non vérifié) | La fiche d'un Cercle ne propose que « Dessiner » | Supprimer « Importer une photo » ici |
| Le trait `#planterZoneN` | Lance le Cercle (trait entier) | — | — | — | Garder |
| « Je lance un Cercle » | Aucun gestionnaire | — | — | — | Garder (texte) |

## 5 · Peaufiner de la page +

On y arrive par `#csBotBar`. Promi : À QUI, AVEC, AVANT, DANS UN CERCLE, NOTE, PIÈCES JOINTES. Cercle : MEMBRES, INVITER, LES PROMI DU CERCLE.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme toute la page + (`peaufTete`, l. 18515) | — | La phrase est perdue | Sur une fiche, le X de Peaufiner ferme aussi la fiche entière | Garder |
| À QUI, AVEC | Mêmes choix que la phrase | Les mots de la phrase | — | Sans « Moi » (§5) | Supprimer (la phrase suffit) |
| AVANT (2 j · 5 j · 2 sem · + tard) | Pose l'échéance (`#dueChips`, l. 3368) | — | Une pastille choisie ne se défait pas : plus de retour à « un jour » ; ni « en l'air » ni date précise. Le code du calendrier n'est jamais atteint (l. 5724). | Fiche : « +2 j / +1 sem. / +1 mois / aujourd'hui » ; Fil : « +1 j / +3 j / +1 sem ». « demain » vaut 2 j ici (l. 5857), 1 j ailleurs (l. 14105). | Renommer : un seul vocabulaire, avec « un jour » et une date |
| INVITER → (Cercle) | Ancien champ `#nInvite` | « + ajouter quelqu'un », MEMBRES | — | — | Supprimer |
| LES PROMI DU CERCLE | Un champ `#nFirst`, sans son + ni la touche Retour (l. 9030) | — | Ce qu'on y tape n'est jamais ajouté | — | Supprimer |
| LE TRAIT | Absent de ce Peaufiner | Rail du pinceau de la page | — | Présent dans le Peaufiner d'une fiche | Garder (le rail est sur la page) |

## 6 · Un gardé de côté rouvert

On y arrive en touchant une carte en pointillés « GARDÉ DE CÔTÉ » dans l'Index (la fonction de reprise, l. 9529, enveloppée l. 41884). Il n'existe pas d'écran « tout ce que j'ai gardé de côté » (connu) : seulement ces cartes et le filtre « Gardés de côté » de l'Index.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Mention « GARDÉ DE CÔTÉ · RIEN N'EST PROMIS » | Texte (l. 18349) | — | — | — | Garder |
| Bouton photo | Absent (refusé si `_ppGarde`) | — | — | Présent sur la page + ordinaire | Garder |
| « garder de côté » | Met à jour le même gardé de côté (v162) | — | — | — | Garder |
| Le trait | Plante, puis retire l'ancien gardé de côté (l. 14184) | — | les deux drapeaux de reprise (l. 3280, 14180) ne sont remis à zéro que par le + de l'accueil : rouvert puis fermé par le X, la page + suivante ouverte depuis une personne ou un Cercle resterait en mode reprise (non vérifié) | — | Garder ; remettre à zéro à la fermeture |
| Supprimer | N'existe pas | — | On ne peut pas retirer un gardé de côté | La fiche a « Supprimer ce Promi » | Garder la page, ajouter « Supprimer » dans son Peaufiner (à trancher) |
| X | Ramène à l'accueil | — | On ne revient pas à l'Index d'où l'on vient | — | Garder ; revenir à l'Index |
| Nature | Restaurée par la nature enregistrée avec le gardé de côté (v162) | — | Un Chiche gardé de côté avant v162 se rouvre en Promi (l. 14148) | — | Garder |

## 7 · Fiche d'un Promi (à tenir, en cours, tenue, l'instant)

On y arrive par une dalle de la Toile, une carte de l'Index, du Fil, d'une personne ou du fil d'un Cercle.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X (`lot-V157-CROIX`) | Retire `.show` de la fiche (l. 3240), sans passer par `closeAll` | Le voile, qui appelle `closeAll` | Retour à l'accueil, quelle que soit l'origine (Index, Fil, personne) : `openDetail` a fermé l'écran d'avant (l. 3882). Seule l'Aura reste dessous. | — | Garder ; revenir à l'écran d'origine |
| Bouton photo | Ouvre le menu photo (voir 11) | — | — | Contour 1,5 px translucide et flouté (l. 20767). Une photo posée change l'icône en flèche de retour (l. 20903), alors que le toucher ouvre toujours le menu. | Garder ; une seule icône, contour de 2 px |
| Le trait `#tenirZone` | Tient la parole (60 pt d'avancée). À plusieurs : trace sa part ; un toucher sur la seconde moitié ouvre la liste des noms (l. 41364). | TENIR du Fil (voir 15) | Trait d'une parole où je ne suis pas tenant : non vérifié | — | Garder |
| Toucher pendant le vert (`_tenirVite`) | Fait remonter le vert ; le toucher est avalé (l. 41773) | — | — | Aucun signe visible (décision) | Garder |
| Disques `#dAura .kring` | Ferment la fiche, ouvrent celle de la personne après 240 ms (l. 5219). L'appel tenté d'abord, `ouvrirPersonne`, n'existe pas (mort connu). | Noms de la phrase, Noyaux de l'Aura | La fiche de la personne ne ramène pas à la fiche du Promi | — | Garder ; ouvrir la personne par-dessus la fiche |
| Noms de la phrase `.nom-lien` | Ouvrent la fiche de la personne (l. 41161) | Disques | Même absence de retour | — | Garder |
| « + x personnes » | Déroule la liste (l. 40656) | — | Rien pour la replier | — | Garder |
| « Un mot… » `#cm5Ligne` | Ouvre la saisie, envoie, montre les mots et « 3 mots » (`lot-V145-COMM`) | COMMENTAIRES de Peaufiner, même `p.comments` | — | « Un mot… » ici, « écris un mot… » et COMMENTAIRES dans Peaufiner | Fusionner : garder cette ligne seule |
| Barre Peaufiner `#dpdTog` | Ouvre et ferme Peaufiner (l. 16992) | Le glissement vers le bas | — | — | Garder |
| Rond Partager `span.dpd-part` | Partage Mon Folio réduit à cette parole, ou le dessin s'il est posé et montré (l. 39641) | `#shareBtn`, « Partager ma Pelote » | Le X de Partager ramène à l'accueil (non vérifié) | Icône seule, conforme ; dessin différent de celui du plateau | Garder |
| Toucher la bande haute | Photo ou dessin en entier (l. 40019) ; rien sur une dalle | — | — | Rien n'indique que la bande se touche | Garder |
| Cadrage de la photo au doigt | Pincer, glisser, tourner à deux doigts ; mémorisé (`lot-V139-CADRE`) | — | Aucun geste ne rend le cadrage d'origine (`remet()` existe, l. 40546, sans bouton) | — | Garder |
| Œil `button.dz-oeil` | Masque le dessin pour soi | — | — | 34 × 34, trait de 1 px, sans zone de 44 | Garder ; contour de 2 px, zone de 44 |

## 8 · Fiche d'un Chiche (lancé, reçu)

Mêmes éléments que le Promi. Ce qui diffère :

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Phrase | « Marion, t'es pas chiche de », « Marion me dit : t'es pas chiche de » ; les noms se touchent | — | — | — | Garder |
| Le trait (Chiche lancé) | Les tenants sont les personnes interpellées, pas moi (l. 41280) | — | Ce que fait mon propre tracé : non vérifié | — | Garder |
| Peaufiner « À QUI JE LANCE » sur un Chiche reçu | Rangée affichée sans garde « reçu » (l. 16912) | — | Une parole d'un autre devient modifiable (non vérifié) | Faux libellé : je ne l'ai pas lancé | Supprimer sur un Chiche reçu |

## 9 · Fiche d'un Cercle (normale, défilée, vide)

On y arrive par la dalle du Cercle sur la Toile, ou par l'Index.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Comme sur la fiche d'un Promi | — | — | — | Garder |
| Bouton « Dessiner sur ce Cercle » | Ouvre un menu à un seul choix, « Dessiner » (plus « Retirer le dessin » s'il y en a un) (l. 40430) | — | Un toucher de trop | Le nœud est partagé : son libellé VoiceOver n'est jamais remis à « Photo » et le relevé le trouve sur une fiche de Promi (l. 40448). La page + d'un Cercle dit « Photo ». | Renommer à chaque pose ; ouvrir le dessin directement |
| Cartes du fil `.nf-item` | Ferment le Cercle et ouvrent la fiche du Promi (l. 6104) | — | Le X de cette fiche ne ramène pas au Cercle (non vérifié) | Mots d'état en casse mêlée : « à tenir », « en cours » en minuscules ; « TENU », « CHICHE RELEVÉ » en capitales | Garder ; une seule casse |
| « Un mot… » | Mots du Cercle, dans `promi_cercle_mots` (l. 42039) ; absente sur un Cercle vide (Q511) | COMMENTAIRES du Peaufiner du Cercle (qui ne marche pas, voir 10) | Un Cercle vide ne reçoit pas de mot | — | Garder |
| « + Planter dans le Cercle » `#nfAdd` | Ouvre la page + d'un Promi pour ce Cercle (l. 9553) | Le même nœud est déplacé dans Peaufiner (l. 21670) | Plante un Promi seulement, jamais un Chiche | Un + dans un rond ; « + Planter un Promi » de la fiche d'une personne a le + dans le texte | Garder |
| Barre Peaufiner, rond Partager | Peaufiner du Cercle ; partage | `#nfPart` « Partager le Cercle », absent de l'écran (code mort, l. 6028) | — | — | Garder ; supprimer `#nfPart` |

## 10 · Peaufiner d'un Promi, d'un Chiche, d'un Cercle

On y arrive par la barre Peaufiner d'une fiche. Ordre lu dans le code — Promi : X, LE TRAIT, COMMENTAIRES, (À QUI), AVANT, DANS UN CERCLE, NOTE, PIÈCES JOINTES, (RELANCER), bloc Ma Parole !, SUPPRIMER. Chiche : À QUI JE LANCE et AVEC, sans DANS UN CERCLE. Cercle : X et nom, LE TRAIT, COMMENTAIRES, DESCRIPTION, MEMBRES, PIÈCES JOINTES, Planter, bloc Ma Parole !, DISSOUDRE.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X `.s2-fermer` (Promi, Chiche) | Clique le X de la fiche (l. 16841) : ferme toute la fiche | Barre et glissement vers le bas (ferment Peaufiner seul) | Ramène à la Toile. C-134 dit « plus jamais la Toile depuis Peaufiner » ; le garde de v146 ne surveille que `closeAll`. | — | Garder ; fermer Peaufiner seul (à trancher) |
| X `#npFermer` (Cercle) | Même chose (l. 21388) | Idem | Idem | Deux propriétaires : `pose()` lui réécrit Atkinson 13 px (l. 21564), `lot-V157-CROIX` le repose toutes les 400 ms | Garder ; un seul propriétaire |
| LE TRAIT (`#dpTraitReg`, `#npTrait`) | Choisit le pinceau de la parole (l. 26046) | Rail de la page + | Les traits payants s'appliquent sans payer (aucun garde trouvé ; « on essaie d'abord, on paie ensuite », Q128, mais rien ne fait payer ensuite) | Payants en pointillé avec « — 0,50 € » (l. 26029) au lieu du mur flouté. Le Cercle : carte de 118 au rail ouvert ; la fiche : rangée de 64 qui se déplie. | Garder ; mettre les payants derrière le mur |
| COMMENTAIRES (Promi, Chiche) | Entrée → `_addComment` (l. 3495) | « Un mot… » | — | Hauteur 118 (Promi), 104 (Chiche) | Supprimer (fusion avec « Un mot… ») |
| COMMENTAIRES (Cercle) | Même champ ; `cur` vaut `null` sur un Cercle (l. 9517), `_addComment` sort | « Un mot… » du Cercle | Le mot tapé n'est enregistré nulle part | Deux magasins pour les mots d'un Cercle | Supprimer |
| À QUI / À QUI JE LANCE, AVEC | Choix des personnes (`_gensFiche`) | Les noms de la phrase | — | Sans « Moi » (§5) ; faux libellé sur un Chiche reçu (voir 8) | Garder |
| AVANT | Pastilles d'échéance (l. 16749) | — | « une date précise… » clique `.ph-date`, qui n'existe que sur la page + (l. 16778) : sans effet sur une fiche (non vérifié) | Vocabulaire différent de la page + et du Fil | Renommer : un seul vocabulaire |
| DANS UN CERCLE (Promi) | Pastilles des Cercles | — | — | Absente sur un Chiche, alors qu'un Cercle porte des Chiche | Garder (à trancher pour le Chiche) |
| NOTE / DESCRIPTION | Écrit la note ; Cercle : `NUENOTE`, sans enregistrement explicite (l. 9549, non vérifié) | — | — | Deux noms selon la nature | Garder |
| PIÈCES JOINTES (Promi, Chiche) | Déplie la liste (l. 16928) | — | Le message dit « appuie sur + », mais le + `#dpPlusPromi` vit hors de la rangée (l. 2825) et n'est relevé nulle part : on ne peut pas joindre de fichier | — | Garder ; poser le + dans la rangée |
| PIÈCES JOINTES `#npFich` (Cercle) | Aucun gestionnaire trouvé | — | Inerte | La rangée de la fiche se déplie | Garder ; la brancher |
| RELANCER [nom] | Compte une relance et écrit « Tu as relancé X » dans le Fil (l. 3491, 16931) | — | — | La relance est un risque nommé de la grille §12 | Supprimer (à trancher) |
| Bloc Ma Parole ! (RÉCURRENCE, RAPPEL, C'EST IMPORTANT ?, LA MÉMOIRE, LA COULEUR) | Mur flouté à 4,8 px, phrase puis offre (voulu, v104) | — | — | « C'EST IMPORTANT ? » a pour valeur « · ·· ··· » : des points comme échelle (l. 16820), contre la loi des points | Garder ; remplacer les points par un mot |
| SUPPRIMER CE PROMI / CE CHICHE | Feuille « Supprimer · Garder », puis « Annuler » pendant 5 s (l. 37115) | `#actDel`, caché | — | Le bouton « Supprimer » de la feuille est orange `#DD4D23`, une couleur d'état (l. 36777) | Garder |
| DISSOUDRE LE CERCLE `#npDiss` | Aucun gestionnaire trouvé (grep) | `#nqDissolve`, caché | Inerte | Même dessin que SUPPRIMER ; l'ancien chemin écrit « « X » dissoute » au féminin (l. 37221) | Garder ; le brancher avec la feuille de confirmation |
| MEMBRES `#npMemb` | Déplie le choix des personnes (l. 21381) | — | — | — | Garder |
| Glissement vers le bas | Rend la fiche (l. 41500) | La barre | — | — | Garder |

## 11 · Menu du bouton photo

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Dessiner | Ouvre le mode dessin (l. 40434) | — | — | Reste « Dessiner » quand un dessin est déjà posé | Garder |
| Importer une photo | Sélecteur du système ; la photo remplace le dessin, qui est perdu (Q439) | Outil PHOTO du dessin, qui fait l'inverse (il ajoute la photo au dessin) | — | Deux « photo » aux effets opposés | Garder |
| La dalle d'origine / La dalle du Studio | Bascule la dalle de la bande (l. 39553) | — | Efface aussi la photo, sans le dire | — | Garder |
| Retirer la photo / Retirer le dessin | Retire (l. 39558, 40432) | — | — | « Retirer le dessin » est en fin de liste, « Dessiner » en tête | Garder |
| Le menu | Se ferme au toucher dehors | — | — | Pastilles de 33 pt de haut (l. 40097), sous la cible de 44 | Garder ; cibles de 44 |

## 12 · Mode dessin

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| PLUME, GOMME | Choisit l'outil ; un second toucher ouvre les tailles | — | — | — | Garder |
| Tailles (trois points) | Fin, moyen, gros, cibles de 44 | — | — | Exception nommée de la loi des points | Garder |
| ANNULER | Retire le dernier trait ; désactivé, contour pointillé | — | — | Pointillé employé pour « inactif », hors de la loi des points | Garder ; inactif en trait plein atténué |
| COULEUR (TRAIT, FOND) | Choix des couleurs ; mur sans Ma Parole ! (l. 40332) | — | Voulu | Conforme aux autres murs | Garder |
| PHOTO | Ajoute ou déplace une photo dans le dessin | « Importer une photo » du menu | — | Icône paysage et soleil, pas le cadre traversé de C-060 | Renommer « Ajouter une photo », une seule icône |
| POSER | Pose le dessin, retire la photo de la bande | — | — | — | Garder |
| ✕ « Quitter le dessin » | Sort sans poser, garde le dessin en cours (l. 40309) | Échap | — | Croix SVG de 18 px, hors du X unique de `lot-V157-CROIX` | Garder ; passer au X de V157 |

## 13 · Vue en entier d'une photo ou d'un dessin

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X `.ev-x` | Ferme (l. 40028) | Tout toucher ailleurs ferme aussi | — | Conforme | Garder |
| Enregistrer `.ev-garde` | Feuille du téléphone, sinon téléchargement (l. 39990) | — | — | Icône seule, conforme ; Partager n'a pas cette icône (C-091) | Garder |

## 14 · Index

On y arrive par INDEX de la barre. C'est une feuille.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme la feuille (l. 3240) | — | — | Le Fil se ferme par `#fdClose` (`setView`) ; le X est à (316, 82) ici, à (322, 70) dans le Fil | Garder ; même mécanisme, même place |
| Recherche `#ixSearch` | Filtre au texte (l. 3484) | — | — | À y 170 ici, 142 dans le Fil | Garder |
| ⇅ `#ixTriBtn` | Ouvre le menu (l. 4373) | — | Connu : un toucher hors du panneau ne le referme pas (le code de la l. 4396 le referme pourtant ; la cause n'a pas été trouvée à la lecture) | Connu : nom et icône ambigus, Tom l'appelle « le bouton Réglages » | Renommer (icône et libellé explicites) |
| TRIER : Récents, À tenir en premier, Par personne, Par Cercle | Trie (l. 4384) | — | Choisir deux fois « Par personne » change l'ordre sans le dire (l. 9662) | Le Fil n'a pas « À tenir en premier » | Garder |
| NE MONTRER QUE : Tout, En suspens, Manquées, Promi, Cercles, Gardés de côté, Demandes | Filtre (l. 3738) | « Gardés de côté » et les cartes en pointillés (connu) | — | « Manquées » nomme une faute (contraire au §12 et au commentaire l. 4366) ; le Fil dit « À tenir ». « Promi » inclut les Chiche ; pas de filtre « Chiche ». | Renommer « Manquées » en « À tenir » |
| QUADRILLAGE : Deux, Trois, Quatre par ligne | Pose `ixCols` (l. 4622) | Le pincement (l. 4649) | Sans effet : l'Index ne lit que `_s4Trois` (l. 19717), que l'app ne pose jamais. La grille reste à deux par ligne. | « Quatre » n'existe dans aucune décision | Supprimer, ou le brancher |
| Repère « • » de l'option choisie | Un point | — | — | Loi des points | Renommer le signe |
| Carte d'un Promi ou d'un Chiche | Ouvre la fiche (l. 19863) | — | Fermée, la fiche ramène à l'accueil, pas à l'Index | — | Garder ; revenir à l'Index |
| Carte en pointillés « GARDÉ DE CÔTÉ » | Rouvre la page + (voir 6) | — | Voir 6 | — | Garder |
| Carte d'un Cercle | Ouvre la fiche du Cercle | — | Même retour à l'accueil | — | Garder |
| Pastille « pas encore vu » `.s4-att` | Point orange `#DD4D23` cerné de crème (l. 35841) | — | — | Couleur d'état pour un « non vu », point hors de la loi, liseré | Renommer le signe |

## 15 · Fil

On y arrive par FIL de la barre. C'est une vue, pas une feuille.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X `#fdClose` | Revient à la Toile (l. 3481) | — | — | Voir l'Index | Garder ; aligner |
| Recherche `#fdSearch` | Filtre au texte (l. 3487) | — | — | Plateau 28 pt plus haut que dans l'Index | Garder |
| ⇅ `#fdTriBtn` | Ouvre le menu (l. 4510) ; un toucher dehors le referme | — | — | Même dessin que l'Index, comportement différent (connu) | Renommer (comme l'Index) |
| TRIER : Récents, Par personne, Par Cercle | Bascule seulement la marque `.on` (l. 4516) ; le Fil ne lit que `fdSortMode`, posé par des pastilles cachées | Pastilles cachées `#fdSort` | Sans effet | L'Index trie vraiment | Supprimer, ou le brancher |
| NE MONTRER QUE (huit options) | `_filtrerFil` cherche des `.fd-item` (l. 4479) que la version actuelle du Fil a déjà remplacés par des cartes `.s4-carte` | « Ce qui attend un geste » et « Demandes » appliquent le même test (l. 4483, 4485) | Sans effet d'après le code | Libellés différents de l'Index (« À tenir » / « Manquées », « Mes Promi », « Mes proches ») | Supprimer, ou le réécrire |
| Pastilles cachées `#fdSort` (Récent, Personne, Cercle, Gardés de côté) | Seule vraie source du tri ; masquées (l. 967) | Le menu TRIER | — | Connu | Fusionner avec TRIER |
| Toucher une carte | Ouvre la fiche ou le Cercle, marque l'entrée vue (l. 20059) | — | Fermée, la fiche ramène à l'accueil, pas au Fil | — | Garder ; revenir au Fil |
| Appui maintenu de 480 ms | Déplie les actes de la carte (l. 20071) | — | — | Seul geste caché de l'app pour agir | Garder |
| Acte TENIR | `feedKeep` (l. 7140) : passe la parole à « tenu » d'un toucher, sans trait ni parts ; puis, au 2e et au 5e, le message « Belle série — partage ton Noyau » | Le trait de la fiche | — | Contraire au §1 (« un geste tracé, pas une case à cocher »), à C-115 (les parts) ; « série » est un terme banni, et le message est un compteur qui croît | Supprimer (le remplacer par TRACER, qui ouvre la fiche) |
| Acte REPORTER | Repousse : +1 j, +3 j, +1 sem | Peaufiner AVANT | — | Troisième vocabulaire de l'échéance | Renommer |
| Actes RELEVER, REJOINDRE, TRACER | Relever un Chiche, rejoindre un Cercle, ouvrir la fiche pour tracer | — | — | — | Garder |
| Réaction « ✧ bravo » | Bascule une réaction (l. 7123) | — | — | « bravo » est banni (R1) ; caché derrière l'appui, les juges ne le voient pas | Supprimer |
| Écouteur de `#feedView` (l. 7178) | Ouvre une fiche sur un `.fd-item` | Le toucher des cartes | Mort : il n'y a plus de `.fd-item` à l'écran | — | Supprimer |

## 16 · Fiche d'une personne

On y arrive par les Noyaux de l'Aura, les disques d'une fiche et les noms touchables. Ni l'Index, ni le Fil, ni la page + n'y mènent.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme la feuille | — | Retour à l'Aura si l'on vient de l'Aura, à l'accueil si l'on vient d'une fiche | — | Garder ; revenir à l'écran d'origine |
| Cellules « Tenu ensemble » `.ps-c` | Ouvrent la fiche (l. 32356) | Les mêmes paroles tenues reparaissent dans les cartes dessous | Retour à l'accueil | — | Fusionner : une seule des deux listes |
| Cartes « Ce que tu partages avec … » | Les cartes de l'Index, ouvrent la fiche | — | Retour à l'accueil | Sans ligne d'état : la même carte diffère de celle de l'Index | Garder |
| « + Planter un Promi », « + Lancer un Chiche » (167 × 62) | Page + avec la personne déjà choisie | — | Voir le mode reprise du gardé de côté (6) | Le + est dans le texte ; « + Planter dans le Cercle » a un + dans un rond ; le + de l'accueil est un disque | Garder ; une seule écriture des « planter » |

## 17 · Aura et aide de l'Aura

On y arrive par AURA de la barre ; l'aide par le « i » du plateau.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme (l. 3240) | — | — | — | Garder |
| « i » `#auraInfoBtn` (20 × 20, zone 44) | Ouvre l'aide ; son X ramène à l'Aura (l. 8827) | — | — | Seul écran de l'app avec une aide | Garder |
| La Pelote `.au-prise` | Toucher, caresse, lancer : creux et trace, aucune navigation | — | L'aide promet « Touche une île pour la revoir » (l. 34523) : aucun gestionnaire trouvé | — | Garder ; retirer la phrase de l'aide, ou brancher l'île |
| « PARTAGER MA PELOTE » `#auPartage` | Ferme l'Aura, ouvre Partager sur « Ma Pelote » (l. 30990) ; le sujet reste ensuite | `#shareBtn`, rond des fiches | Le X de Partager ramène à l'accueil, pas à l'Aura | Pilule texte, quand Partager est une icône partout ailleurs | Garder ; revenir à l'Aura |
| Noyau d'une personne | Ouvre sa fiche (l. 31833), l'Aura reste dessous | Disques des fiches, noms | — | — | Garder |
| Noyau « Toi » | Ne fait rien (l. 31844) | — | Le plus grand disque est une cible vide | — | Garder, sans prise visible (à trancher) |
| Légende, trois chiffres | Affichage | — | — | Pastilles de 20 px : dette nommée de la loi des points | Garder |
| Dalles de « Ce que tu as tenu » | Ouvrent la fiche ; le X ramène à l'Aura (l. 32398) | — | — | — | Garder |
| « Ce qu'on t'a tenu » | Mur flouté en gratuit ; ouvre la fiche pour un membre | — | Voulu | — | Garder |
| Code mort | « ✦ Ma Parole ! » de l'Aura et `#ahCercleCta`, masqués, ouvrent l'offre en direct (l. 30989, 34537) | — | — | — | Supprimer |

## 18 · Studio

On y arrive par STUDIO de la barre, ou par « Le Studio » des Réglages.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme (l. 3240) | — | Venu des Réglages, on revient à l'accueil. Pendant une phrase de mur, toucher le X ouvre Ma Parole ! au lieu de fermer (l. 39255). | — | Garder ; exclure le X du « toucher n'importe où » |
| Glissement horizontal | Change de monde | Barrettes | — | — | Garder |
| Barrettes de pagination | Change de monde (l. 22885) ; grisées et intouchables sur un monde payant (l. 22645) | Glissement | Sur un monde payant, seul le glissement fait sortir | — | Garder ; actives aussi sur un monde payant |
| Les quatre tons `#stpTons` | Les quatre ouvrent le même panneau des palettes (l. 22871) | Entre eux | — | Une pastille de couleur se lit comme « choisir ce ton » | Fusionner en un seul déclencheur |
| Sombre, clair | Thème global (`setTheme`, l. 22827) | — | Flouté et intouchable sur un monde payant (l. 22644) : un réglage gratuit pris dans le mur | — | Garder ; le sortir du mur |
| Avec texte, sans texte | Écrit `state.labels`, enregistré (l. 4001) | « Le texte des dalles » de Partager écrit la même variable (l. 9198) | Même mur | — | Garder |
| Panneau des 24 palettes | Choisit la palette, nom sous la grille | Geste vertical | — | — | Garder |
| « ← Retour » | Referme le panneau des palettes (l. 34829) | — | — | Zone de 34 pt, sous les 44 de l'app | Garder ; zone de 44 |
| Noir et blanc `.stp-nb` | Bascule globale ; la jauge dose alors le noir et blanc (l. 35064) | — | — | 34 × 34, icône seule | Garder ; zone de 44 |
| Jauge et sa dalle | Règle la teinte (ou le dosage du noir et blanc) ; zone de 56 pt | Geste horizontal | — | — | Garder |
| Geste de couleur (appui 480 ms, glisser) | Horizontal = teinte, vertical = palette (l. 35365) ; reste actif sur un monde payant où le panneau des palettes est un mur (non vérifié) | Jauge, panneau | — | Rien ne l'annonce | Garder ; le couper sur un monde payant |
| « Adopte ce design — 2 € » | Ouvre « Avant d'acheter » (voir 27) | — | Voir 27 | Le Studio dit « monde », le bouton « design » ; le libellé tournant (l. 8839) est écrasé par un libellé fixe (l. 23190) | Renommer en « monde » |
| Murs (panneau, palettes, Toile floutée) | Phrase, puis l'offre par-dessus (l. 39146) | — | Voulu | Flou de 2,4 et 1,4 px ici, 4,8 ailleurs (décision « le Studio garde le sien ») | Garder |
| Code mort | « Ou débloque-les tous » `#stLockCta`, masqué (l. 39058) | — | — | — | Supprimer |

## 19 · Partager

On y arrive par trois chemins : le plateau de l'accueil, le rond de la barre Peaufiner d'une fiche, « Partager ma Pelote ».

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme ; `openShare` a déjà tout fermé : retour à l'accueil (depuis une fiche : non vérifié) | — | Depuis l'Aura ou une fiche, l'écran d'origine est perdu | — | Garder ; revenir à l'écran d'origine |
| Barre « Ma Toile · Story » `#shcPeaufiner` | Ouvre et ferme le panneau des choix (l. 25081) | — | — | Elle joue le rôle de Peaufiner sans en porter le nom | Garder |
| Sujet : Ma Toile, Mon Folio, Ma Pelote | Choisit l'image (`shareMode`) | — | — | Le sujet dépend du chemin : l'accueil reprend le dernier, la fiche impose Mon Folio et rend le choix d'avant, l'Aura impose Ma Pelote et ne rend rien | Garder ; un seul comportement |
| « La Pelote » dans Mon Folio | Appui de 380 ms : déplace la Pelote dans la planche | — | — | — | Garder |
| Quels Promi (fenêtre « Afficher · masquer ») | Masque des paroles de l'image | — | — | — | Garder |
| Format : Plein écran, Story, Post carré, Paysage, Édito, Définir | Taille de l'image ; « Définir » règle largeur et hauteur au pas de 120 | — | — | Mots anglais, réglages techniques | Supprimer « Définir » |
| Le fond de l'image : Sombre, Clair | `_sealDark` (l. 8836) ; sans effet sur Ma Toile, qui suit le thème de l'app depuis v143 (l. 7430) ; sombre par défaut | Thème du Studio | Sans effet pour un des trois sujets | — | Supprimer sur Ma Toile |
| Le texte des dalles : Avec, Sans texte | Écrit `shLabels` et aussi `state.labels` (l. 9198) : le choix du partage change le réglage global de la Toile et du Studio, et il est enregistré | Studio « avec / sans texte » | — | — | Garder ; ne plus toucher au réglage global |
| QR | Montre ou masque le QR (l. 8821) | — | — | — | Garder (à trancher) |
| Mot-marque `#shBadge` | Un toucher bascule un style « Signature » caché (l. 9162) que Tom a retiré (l. 36460) | — | — | Option cachée | Supprimer la bascule |
| Glissement vertical sur l'écran | Bascule `sh-haut`, ignoré en plein écran (l. 23495) | — | — | — | Supprimer (geste mort) |
| « Inviter » `#shInviteBtn` | Partage le texte « …3 Cercles offerts pour toi et pour moi » (l. 7880) | Réglages « Inviter sur Promi » (clique ce bouton, l. 9203) | — | Deux noms ; l'offre « 3 Cercles offerts » n'est expliquée nulle part | Renommer : un seul nom |
| « Partager » `#shShareBtn` | Exporte l'image puis la feuille du téléphone | — | — | — | Garder |

## 20 · Réglages

On y arrive par l'icône des Réglages du plateau. Groupes : Toi, (Ma Parole !, Le Studio, Revoir la présentation), Partager, App, Données, Compte, Légal, puis « Supprimer mon compte ».

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme (l. 3240) | — | — | — | Garder |
| Avatar `#setAva` | Ouvre le sélecteur de photo (l. 3309) | — | — | — | Garder |
| Retirer la photo `#setDelPhoto` | Retire, puis « Annuler » pendant 5 s (l. 37209) | — | — | — | Garder |
| Prénom `#setNameInput` | Champ, enregistré à la sortie (l. 3311) | — | — | Zone de 45 × 35 au relevé, sous 44 de haut | Garder ; zone de 44 |
| « Ma Parole ! · débloque tout Promi · essai 14 jours » `#openPlusTop` | Ferme tout, ouvre l'offre (l. 3343) | Mot-marque de l'accueil, murs | Retour à l'accueil, pas aux Réglages | Grande carte de 90 de haut, la seule ; ses deux couleurs (`#A77CF7`, `#E08370`) ne sont des couleurs d'aucun autre libellé (le sous-titre est masqué en v105, l. 32507) | Garder ; revenir aux Réglages |
| « Le Studio · visuels & humeurs › » `#openStudio2` | Ouvre le Studio (l. 3361) | STUDIO de la barre | Retour à l'accueil | Cinquième nom du Studio (« visuels & humeurs ») | Supprimer (la barre y mène déjà), ou renommer |
| « Revoir la présentation · rejouer › » | Rejoue l'onboarding ; lit le geste (l. 40560) | — | — | — | Garder |
| « Réinitialiser (test) » `#resetApp` | Masqué (l. 34585) | — | — | — | Supprimer (code de test) |
| « Inviter sur Promi › » `#setInvite` | Clique le bouton « Inviter » de Partager (l. 9203) | « Inviter » de Partager | — | Deux noms | Garder ; un seul nom |
| « Mention sur un dessin partagé · affichée › » | Bascule la mention ; lit le geste (l. 40586) | — | — | Une bascule écrite comme une porte (« › ») ; Notifications aussi porte « › » mais ouvre une page | Déplacer vers Partager (« un réglage vit là où vit ce qu'il règle » ; c'est pourtant une décision de v137, à trancher) |
| « Langue » `#langCard` | Masquée (l. 36737) : l'écran de la langue est inaccessible | — | — | — | Supprimer, ou la montrer (à trancher) |
| « Notifications › » `#notifCard` | Ouvre la page des notifications (l. 39456) ; trois gestionnaires successifs, le dernier en capture gagne | — | — | Ancienne bascule `#notifTog` masquée | Garder |
| « Vie privée · privé & partagé › » `#privCard` | Ouvre Vie privée (l. 3442) ; le libellé « Confidentialité » est réécrit en « Vie privée » (l. 37214) | — | Le X de Vie privée ramène à l'accueil (voir 21) | Écran et libellé « Vie privée », Légal dit « Politique de confidentialité » | Garder |
| « Sauvegarde locale » | Affichage seul (l. 7908) | — | — | Rangée de même dessin qu'un bouton | Garder |
| « Réinitialiser mes données · effacer › » | Feuille « Effacer · Garder », puis effacement différé de 5 s (l. 37200) | Vie privée « Tout effacer », « Supprimer mon compte » | — | — | Fusionner les trois effacements en un |
| « Garder ta Toile › » `#compteCard` | Ouvre le panneau du compte (l. 37189) | Bandeau de l'accueil | Apple et Google ne sont pas branchés (voir 27) | — | Garder |
| « Se déconnecter › » `#logoutCard` | Feuille, puis appelle `promiDeconnexion` (absente, mort connu), ferme et affiche « À bientôt » (l. 37192) | — | Ne fait rien ; visible même sans compte (le compte n'est jamais « fait », l. 38541) | — | Supprimer tant qu'il n'y a pas de compte |
| « Conditions d'utilisation › », « Politique de confidentialité › » | Ouvrent la même page « Légal », « Bientôt disponible » (l. 37152) | Entre elles | Page vide | — | Garder (à remplir) |
| « À propos › » | Ouvre la page À propos (l. 37198) | — | — | — | Garder |
| « Supprimer mon compte » | Feuille, puis efface tout le stockage et recharge (l. 37124) | Vie privée « Tout effacer » (même effet exact) | — | En orange `#DD4D23`, une couleur d'état (C-015, ouvert) | Fusionner avec « Tout effacer » |
| Remarque | Depuis v137, « aux Réglages un toucher ne produit pas toujours de click » : seules deux rangées lisent le geste ; les autres attendent un `click` (non vérifié au doigt) | — | — | — | Garder ; à vérifier au doigt |

## 21 · Vie privée

On y arrive par « Vie privée » des Réglages.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme (l. 3240) | — | Ramène à l'accueil, pas aux Réglages | Notifications, Légal et À propos ramènent aux Réglages (l. 37146, 39444) | Garder ; revenir aux Réglages |
| Cinq rangées d'information (Tes Promi, Tes Promi perso, Ce que tu partages, Compte, Traceurs) | Affichage | — | — | « synchronisé pour tes proches » : aucune synchronisation n'existe encore | Garder (texte à revoir avec Firebase) |
| « Exporter mes données · copier › » | Copie le JSON dans le presse-papier (l. 3448) | — | — | Copie, pas un fichier | Garder |
| « Tout effacer · effacer › » | Feuille, puis vide tout le stockage et recharge (l. 37203) | « Supprimer mon compte », « Réinitialiser mes données » | — | Valeur en orange d'état ; rangées sans contour, 54 de haut, quand les Réglages ont des pilules de 64 | Fusionner |

## 22 · Notifications

On y arrive par « Notifications › » des Réglages (`lot-V109-NOTIFS`).

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ramène aux Réglages (l. 39444) | — | — | — | Garder |
| « Mes paroles datées » (bascule) | Un mot la veille ; demande la permission à l'activation | Question « Je te le rappelle ? » | — | — | Garder |
| « Mes paroles en l'air · de temps en temps, une douce relance » | Mur de Ma Parole ! ; payé : une notification par semaine au plus | — | Voulu | « relance » : un risque nommé du §12 | Renommer (« de temps en temps, un mot ») |
| « L'heure » | Mur ; payé : tourne entre 8 h, midi, 19 h | — | Voulu | Trois valeurs seulement, au toucher, sans liste | Garder |
| « Ce qu'on me lance · bientôt » | Bascule éteinte, sans prise | — | Rangée sans effet | — | Garder (attend Firebase) |
| Dessin des rangées | — | — | — | Trait de 3 px et rayon 22 : hors de la grammaire des contours (2 px, rayon = hauteur ÷ 2), alors que les Réglages y ont été remis | Garder ; contour de 2 px |

## 23 · Légal (Conditions, Politique de confidentialité)

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ramène aux Réglages (l. 37146) | — | — | — | Garder |
| Contenu | « Bientôt disponible. » | Les deux rangées mènent à la même page | Page vide | Le panneau du compte dit « tu acceptes les Conditions et la Politique », soulignées mais sans lien | Garder (à remplir) |

## 24 · À propos

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ramène aux Réglages | — | — | — | Garder |
| Lien creativecommons.org | Ouvre la licence de Gilbert, hors de l'app | — | — | Cible de 30 × 19 | Garder |
| « Lire la licence (SIL OFL 1.1) » | Déplie le texte de la licence | — | — | — | Garder |

## 25 · Langue

Inaccessible : la rangée « Langue » est masquée (l. 36737). L'écran (`#langScreen`, `buildLang`) reste dans le code. Recommandation : supprimer, ou montrer la rangée (à trancher).

## 26 · Ma Parole ! (l'offre)

On y arrive par le mot-marque de l'accueil, par « Ma Parole ! » des Réglages, ou à la fin d'une phrase de mur. Page reconstruite par `lot-CERCLE-TOILE` (l. 33350). Les anciens textes (« Rappels intelligents — Promi te relance… », « Stats avancées ») sont masqués (l. 32715) : ils ne sont pas à l'écran.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| X | Ferme. Ouverte par les murs, l'offre est posée par-dessus et le X rend l'écran d'origine ; ouverte par l'accueil ou les Réglages, tout a été fermé avant : retour à l'accueil (l. 3321, 32662) | — | Depuis les Réglages, retour à l'accueil | Trois retours différents selon la porte | Garder ; un seul comportement |
| « Essayer 14 jours › » `#buyMonth` | Sans compte : « Avant d'acheter » (voir 27). Puis membre tout de suite, « Tu es Membre Ma Parole ! » et ouverture de l'Aura (l. 3360). | « Bon, allez d'accord » | — | L'essai et l'achat font exactement la même chose ; après l'achat on arrive sur l'Aura, sans raison lisible | Garder ; revenir à l'écran d'origine |
| « Bon, allez d'accord — 39 € / an » `#buyYear` | Même effet | « Essayer 14 jours » | — | — | Garder |
| « ou 5,99 € par mois » | Texte seul | — | Le prix du mois s'affiche sans aucun moyen de le choisir | — | Garder (à trancher : un bouton ou le retirer) |
| Code mort | Quatre portes masquées ouvrent l'offre en direct : `#cercleTopBtn`, `#stLockCta`, celle de l'Aura, `#ahCercleCta` | — | — | — | Supprimer |

## 27 · Encarts d'achat et de compte

`lot-ACHAT-SANS-COMPTE` (l. 2989) et le panneau du compte de l'onboarding (l. 38382).

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Encart « Avant d'acheter » : Continuer avec Apple, Continuer avec Google, Acheter sans compte | Les trois achètent : ils ferment l'encart puis relancent le toucher d'achat (l. 3001) | Entre eux | Aucune sortie qui n'achète pas, ni X, ni toucher dehors | Tous les autres encarts ont un « Plus tard » qui renonce | Garder ; ajouter une sortie sans achat |
| Encart « Garder ton achat » : Apple, Google, Plus tard | Compte ou renonce | Réglages « Garder ta Toile » | — | — | Garder |
| Panneau « Garder ta Toile » (onboarding, Réglages, bandeau) : Apple, Google, Plus tard | Note `demande-apple` ou `demande-google` et appelle `promiConnexion`, qui n'existe pas (l. 38410) | — | Apple et Google ne font rien : le compte n'est jamais « fait » (l. 38541), donc tout achat repasse par « Avant d'acheter » et « Se déconnecter » reste visible | — | Garder (attend Firebase) |
| Ligne « En continuant, tu acceptes les Conditions et la Politique » | Soulignées, sans lien | — | Mène à rien ; les pages disent « Bientôt disponible » | — | Garder (lien à poser) |
| Feuille de confirmation « Supprimer · Garder » | Partout où l'on supprime ou efface (l. 37060) | — | — | Bouton d'action orange `#DD4D23` (couleur d'état) | Garder |
| Bandeau « … · Annuler » (5 s) | Défait une suppression | — | — | — | Garder |

## 28 · Onboarding

Premier lancement, ou « Revoir la présentation ». Prénom → parole → trait → « Promi planté ! » → panneau du compte. Le « Plus tard » de l'onboarding est retiré (v144, exception nommée de R6) ; le panneau du compte garde le sien.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| « Toi, c'est … ? » et la phrase | Un toucher ouvre la saisie (l. 37927) | — | — | — | Garder |
| → `#onbSuite` | Passe à l'étape suivante ; Retour fait de même | — | — | Le + qui confirme un nom sur la page + est orange ; ce → ne l'est pas | Garder |
| Le trait `#onbTrait` | Plante la première parole ; tracé sans parole, la saisie s'ouvre | Le trait de la page + (qui, lui, ne l'ouvre pas) | — | — | Garder |
| « Promi planté ! » : quatre touchers n'importe où | Font paraître les paragraphes, puis le panneau du compte (l. 38245) | — | — | Rien n'indique qu'il faut toucher (non vérifié à l'écran) | Garder |
| Panneau du compte | Voir 27 | — | — | — | Garder |

## 29 · Guide de fin de parcours

`lot-V141-GUIDE` (l. 40824). Une seule fois après l'onboarding ; « Revoir la présentation » le rejoue.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Zone nette du Studio | Ouvre le Studio (l. 41006) | STUDIO de la barre | — | — | Garder |
| Toucher ailleurs, à l'étape du Studio | Réécrit la phrase du Studio, autant de fois qu'on touche (l. 41007) | — | La seule sortie est d'ouvrir le Studio ; l'app quittée, le guide reprend au lancement suivant | Décision de Tom (C-146), sans « Plus tard » (v144) ; à rapprocher du §12 (« rythme imposé ») | Garder (à trancher) |
| Zone nette du + | Ouvre le menu des trois natures (l. 41088) | Le + | — | — | Garder |
| Toucher ailleurs, à l'étape du + | Finit le guide | — | — | — | Garder |

## 30 · Veille

`lot-V161-VEILLE`, après 60 s sans toucher.

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Un toucher n'importe où | Quitte la veille, rend l'écran exact, n'actionne rien dessous | — | — | — | Garder |

## 31 · Les murs de Ma Parole ! (sur tous les écrans)

| Bouton ou option | Ce qu'il fait | Doublon | Cul-de-sac | Écart avec son équivalent | Recommandation |
|---|---|---|---|---|---|
| Un réglage flouté (Aura, Peaufiner, dessin, Notifications, Studio) | Phrase posée sur le flou, puis l'offre ; la première fois elle s'ouvre seule (voulu, v104) | — | — | Flou de 4,8 px partout, sauf au Studio (2,4 et 1,4, décision) | Garder |
| Un toucher pendant la phrase | Ouvre l'offre, où qu'il tombe, X compris (l. 39255) | — | Au Studio, on ne peut pas fermer l'écran pendant 3 à 5,5 s | Décision de v104 ; le X fait exception à « ✕ Fermer » | Garder ; exclure le X (à trancher) |
| Traits payants du pinceau | Pas de mur : pointillé et prix, et ils s'appliquent sans payer (voir 10) | — | — | Seule offre payante hors du mur | Garder ; les mettre derrière le mur |

---

## Les 10 points les plus importants

1. **TENIR depuis le Fil tient une parole d'un toucher.** Fil, appui maintenu sur une carte : `feedKeep` (l. 7140) passe la parole à « tenu » sans trait et sans les parts des autres, puis affiche « Belle série — partage ton Noyau » au 2e et au 5e ; la réaction s'appelle « ✧ bravo ». C'est contraire au §1, à C-115 et au lexique. Recommandation : supprimer TENIR (TRACER, qui ouvre la fiche, suffit), supprimer « bravo » et le message.

2. **L'encart « Avant d'acheter » n'a aucune sortie qui n'achète pas.** Studio (« Adopte ce design ») et Ma Parole ! (les deux boutons) : Apple, Google et « Acheter sans compte » achètent tous les trois (l. 3001), sans X ni toucher dehors. Recommandation : garder l'encart, ajouter « Plus tard » qui renonce.

3. **Les menus ⇅ de l'Index et du Fil font beaucoup moins que ce qu'ils affichent.** Fil : TRIER ne pose aucune variable lue (l. 4516), NE MONTRER QUE cherche des éléments qui n'existent plus (l. 4479). Index : QUADRILLAGE est sans effet (l. 19717). S'y ajoutent les deux points connus : le nom et l'icône ambigus (« le bouton Réglages »), et la fermeture qui diffère entre l'Index et le Fil. Recommandation : renommer le bouton, supprimer ou brancher chaque option morte.

4. **Quatre rangées de Peaufiner ne font rien ou perdent ce qu'on y met.** DISSOUDRE LE CERCLE et PIÈCES JOINTES du Cercle n'ont aucun gestionnaire ; COMMENTAIRES du Cercle sort sans rien enregistrer (`cur` nul, l. 3495, 9517) ; PIÈCES JOINTES d'un Promi renvoie à un + absent (l. 9458). Sur la page + d'un Cercle, LES PROMI DU CERCLE n'ajoute rien. Recommandation : brancher DISSOUDRE et les pièces jointes, supprimer les deux autres.

5. **Fermer ne ramène presque jamais d'où l'on vient.** Une fiche ouverte depuis l'Index, le Fil, une personne ou un Cercle ramène à l'accueil (`closeAll`, l. 3882) ; Partager, Vie privée, le Studio et Ma Parole ! ouverts depuis les Réglages ou l'Aura aussi ; le X de Peaufiner ferme toute la fiche (l. 16841). Seules l'Aura et trois sous-pages des Réglages rendent l'écran d'avant. Recommandation : garder le X, lui faire rendre l'écran d'origine partout.

6. **On commente à deux endroits, avec trois noms.** Fiches : la ligne « Un mot… » et COMMENTAIRES de Peaufiner écrivent dans la même liste ; « Un mot… », « écris un mot… », « mots » ; pour un Cercle, deux magasins différents, et le second ne marche pas. Recommandation : fusionner, garder la ligne « Un mot… » seule.

7. **Le compte et l'effacement : des doublons et des rangées inertes.** Réglages et Vie privée : « Réinitialiser mes données », « Tout effacer » et « Supprimer mon compte » (les deux derniers font exactement la même chose) ; « Se déconnecter » est visible sans compte et ne fait rien ; Apple et Google ne sont pas branchés ; Conditions et Politique disent « Bientôt disponible » ; Vie privée ramène à l'accueil. Recommandation : fusionner les trois effacements, supprimer « Se déconnecter » tant qu'il n'y a pas de compte.

8. **Les traits payants du pinceau échappent à toutes les règles de Ma Parole !.** Page + et Peaufiner : huit traits sur douze sont hors de vue (rail sans glissement), et ceux qu'on atteint s'appliquent sans payer (aucun garde, l. 25856, 26151). Ils sont signalés par un pointillé et « — 0,50 € » au lieu du mur. Recommandation : garder les traits, les mettre derrière le mur, rendre le rail glissant.

9. **Un même rôle porte des noms différents d'un écran à l'autre.** L'échéance a trois vocabulaires (page + « 2 j / 5 j / 2 sem / + tard », fiche « +2 j / +1 sem. / +1 mois », Fil « +1 j / +3 j / +1 sem ») et plus de retour possible à « un jour ». La case du défié s'appelle « qui ose ? », « QUI TU DÉFIES », « À QUI JE LANCE ». Le Studio s'appelle aussi « design » et « visuels & humeurs ». « Inviter » et « Inviter sur Promi ». Recommandation : renommer, un mot par rôle.

10. **Plusieurs choix vont contre la grille anti-coercition (§12).** Le bandeau « Garder ta Toile » revient sans fin après chaque « Plus tard » (l. 38597) ; RELANCER [nom] dans Peaufiner ; « Manquées » dans l'Index ; « une douce relance » dans les notifications ; et un toucher pendant une phrase de mur, X compris, ouvre l'offre. Recommandation : supprimer RELANCER et la relance sans fin, renommer « Manquées » et « relance », exclure le X des murs — à trancher par Tom, certains sont des décisions écrites.

Également vus, hors des dix : le choix « Avec / Sans texte » de Partager change le réglage global de la Toile (l. 9198) ; « Le fond de l'image » est sans effet sur Ma Toile ; le libellé « Dessiner sur ce Cercle » passe sur les fiches de Promi ; le « Chiche » de la phrase paraît touchable et ne fait rien ; le bouton photo, l'œil du dessin, « ← Retour » et « Noir et blanc » du Studio sont hors de la grammaire des contours ou sous 44 pt.

## Non vérifié

- Tout ce qui précède est lu dans le code ; rien n'a été joué au doigt ni à l'écran.
- Les retours d'écran (X de Partager depuis une fiche, fiche ouverte depuis le fil d'un Cercle) peuvent dépendre du garde de Peaufiner (v146).
- Le menu de l'Index qui ne se referme pas au toucher dehors : constaté par Tom ; le code (l. 4396) semble le refermer, la cause n'est pas trouvée.
- L'absence de gestionnaire sur `#npDiss` et `#npFich` vient d'une recherche dans le fichier, sans essai.
- L'effet d'un tracé sans titre sur la page +, d'une photo importée sur la page + d'un Cercle, de « une date précise » dans Peaufiner.
- Le geste de couleur du Studio sur un monde payant.
- Les cotes de l'inventaire qui se superposent (cartes du Fil à 548 et 596, rangées des Réglages toutes à y 472, NOTE et SUPPRIMER de Peaufiner) : instrument ou écran, non tranché.
- Le risque « un toucher ne produit pas toujours de click aux Réglages » (v137) pour les rangées qui n'écoutent que `click`.
