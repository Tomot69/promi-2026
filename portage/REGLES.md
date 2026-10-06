# RÈGLES — ce que Promi s'interdit, ses lois de dessin, son lexique

> Établi le 6 oct. 2026, lot v134. Chaque règle est **vérifiable** : un énoncé, la façon de la vérifier (quoi mesurer, sur quoi, quel seuil), la décision qui la fonde, et le juge du prototype qui la porte quand il existe.
> Rien n'est inventé. Ce qui n'a pas été trouvé est marqué **⚠ TROU** et repris en fin de document.
> Les valeurs citées sont dans `portage/JETONS.json`. « — » dans la colonne du juge : aucun juge ne porte la règle.

Forme d'une règle :

> **R-000 · Énoncé.**
> *Vérifier* : la mesure, son objet, son seuil. · *Décision* : qui, quand, où. · *Juge* : le script du prototype.

---

## A · LA GRILLE ANTI-COERCITION

**⚠ TROU : la grille n'est écrite nulle part comme une liste.** `CLAUDE.md` (bloc v118) dit seulement : « D est EXCLU DÉFINITIVEMENT : c'est un compteur visuel qui croît avec l'action — **la grille l'interdit** », sans donner la grille. Le mot « coercition » n'apparaît dans aucun document du dépôt. Ce qui existe par écrit, et dont cette section est reconstituée :

- **les « huit règles anti-notation »**, dont le seul énoncé trouvé est le tableau de `AUDIT-AURA-CERCLE.md` §C (3 sept. 2026), repris par `QUESTIONS.md` (Q166, Q184) et `AUDIT-PELOTE.md` — **⚠ TROU : leur texte d'origine et leur date de décision ne sont pas dans les sources lues** ;
- « la ligne rouge » de `BRIEF-ETUDE-PSYCHO.md` (l.23-24, l.169) ;
- `DECISIONS.md` A1 ;
- des décisions datées de `CLAUDE.md` et de `QUESTIONS.md` (Q347, v104, v109, v118).

### A1 · Ce n'est pas un gestionnaire de tâches

**R-001 · Toute décision qui rapproche Promi d'un gestionnaire de tâches est rejetée, même si elle est pratique.**
*Vérifier* : revue de chaque fonction nouvelle contre R-002 à R-012 ; aucune n'en enfreint une. · *Décision* : `CLAUDE.md` §1 ; `DECISIONS.md` A1 (« Décidé ») ; `BRIEF-ETUDE-PSYCHO.md` l.49. · *Juge* : —

**R-002 · On tient sa parole par un geste tracé au doigt, jamais par une case à cocher ni par une touche.**
*Vérifier* : aucun contrôle de type case, interrupteur ou bouton ne fait passer une parole à « tenue » sur une fiche ; le tracé est un glissement, pas un toucher (le Fil garde « TENIR · REPORTER » sur appui maintenu : ajout validé hors inventaire, `CLAUDE.md` §5). · *Décision* : `CLAUDE.md` §1 ; `DECISIONS.md` A1 « On ne coche pas, on trace » ; moodboard H (« un glissement, pas une touche »). · *Juge* : `redteam_geste.py`

**R-003 · L'échéance n'est jamais obligatoire : « un jour » est une réponse valable, et aucun bouton « ajouter une échéance » n'existe.**
*Vérifier* : une parole se plante sans date ; aucune chaîne « ajouter une échéance » ; le mot « échéance » n'est le libellé d'aucun champ (R-089). · *Décision* : `DECISIONS.md` A1 (rejeté, verbatim de Tom : « c'est ça qui donne trop crm to do list tache à remplir »). · *Juge* : —

**R-004 · La création est une phrase dont les mots se touchent, pas un formulaire.**
*Vérifier* : la page + ne montre ni onglets ni champs empilés au repos ; elle montre une phrase. · *Décision* : `DECISIONS.md` A2. · *Juge* : `redteam_verbe.py`, `redteam_phrase.py`

**R-005 · On ne défait pas une parole tenue.**
*Vérifier* : aucune commande ne ramène une parole tenue à un autre état. · *Décision* : `promi-moodboard-H.html`, note du cadre 22-23 (« un effacement obligerait à notifier qu'on retire quelque chose de donné — un événement négatif notifié, interdit par les règles anti-notation »). · *Juge* : — · **⚠ TROU** : la règle n'est reprise dans aucun document de décision daté.

**R-006 · Aucun réglage « urgent » : l'urgence n'existe pas dans le produit.**
*Vérifier* : aucun réglage, tri ou libellé « urgent » à l'écran. · *Décision* : commentaire du code « Urgent supprimé (décision : on garde Important, comme la fiche) », rappelé par `CLAUDE.md` §9 ; « urgent » banni (Tom, 18 août 2026). · *Juge* : — · ⚠ `app.html:2869` garde un mode de tri interne `urgence` (code d'origine) : à ne pas porter.

### A2 · Rien ne note, rien ne classe

**R-007 · Aucune carte, aucun corps, aucun fond n'est peint d'une couleur d'état : l'état vit dans la ligne.**
*Vérifier* : sur chaque carte d'Index, bandeau du Fil et fiche, la couleur de fond rendue n'est aucune de `#DD4D23`, `#291547`, `#00341A`. · *Décision* : Tom, direction Horizon ; `CLAUDE.md` §7 (« aucune carte n'est peinte d'une couleur d'état », contrat réécrit le 18 août 2026). · *Juge* : `redteam_ecrans.py`, `redteam_champ.py`

**R-008 · Dans une liste et sur la Toile, une dalle n'est jamais teintée par sa nature : ce serait un classement par nature.**
*Vérifier* : Index, Fil, Toile, encart d'un Cercle — la couleur d'une dalle vient du monde et de la palette, pas de `promi/chiche/cercle` (hors Ingénu, R-037). · *Décision* : Tom, 18 août 2026 (Q30) : « exactement ce que le produit refuse » ; `CLAUDE.md` §4. · *Juge* : `redteam_decoupe.py` (famille H), `redteam_reperage.py`

**R-009 · Pas de score, pas de points, pas de badges, pas de série.**
*Vérifier* : aucune chaîne ni aucun compteur de jours consécutifs, de points ou de niveau ; le mot « score » est banni (R-088). · *Décision* : `BRIEF-ETUDE-PSYCHO.md` l.23-24 (« pas de série à ne pas briser sous peine de perdre, pas de compte à rebours culpabilisant, pas de score »), l.169 (« on refuse points, badges, séries ») ; `DECISIONS.md` A1. · *Juge* : —

**R-010 · Aucun compteur visuel ne croît avec l'action.**
*Vérifier* : aucun élément graphique dont le nombre, la longueur ou la taille augmente à chaque parole tenue (l'option D, « un trait par parole tenue » autour de la Pelote, est exclue définitivement et ne se repropose pas). · *Décision* : Tom, 2 oct. 2026 (v118, Q368). · *Juge* : — · ⚠ Voir la tension T-1 en fin de section.

**R-011 · Aucun chiffre, aucun mot de valeur, aucun agrégat n'est attaché à une personne.**
*Vérifier* : sous un visage ou un Noyau, ni pourcentage, ni taux, ni mot d'harmonie (« rayonnante », « naissante ») ; rien de tel sur la fiche d'une personne. · *Décision* : règles anti-notation 1 et 4 (`AUDIT-AURA-CERCLE.md` §C) ; `QUESTIONS.md` l.5509-5516 (Tom : la fiche de la personne). · *Juge* : `redteam_ecrans.py` (« seuls les trois chiffres permis », v95)

**R-012 · Aucun tri par valeur, aucun superlatif.**
*Vérifier* : aucune liste ordonnée par taux de parole tenue ; aucune chaîne « meilleur(e) ». · *Décision* : règle anti-notation 5 (`AUDIT-AURA-CERCLE.md` §C). · *Juge* : — · ⚠ `RENOMMAGE-LEXIQUE.md` §4 garde « Ton meilleur Cercle » parmi les chaînes accordées en v106 : à vérifier à l'écran (voir T-2).

**R-013 · Ce qui se mesure à deux est symétrique : aucun verdict ne désigne un porteur et un porté.**
*Vérifier* : aucune phrase du type « tu portes un peu plus ». · *Décision* : règle anti-notation 3. · *Juge* : —

**R-014 · Des anneaux, jamais une liste de barres.**
*Vérifier* : l'Aura ne porte aucune rangée « nom + barre + taux ». · *Décision* : règle anti-notation 7. · *Juge* : —

**R-015 · L'Aura ne porte que trois chiffres — tenues, en cours, à tenir — sous la légende, et aucun pourcentage.**
*Vérifier* : dans `#auraScreen`, les seuls nombres rendus sont ces trois-là (PromiLate 29, encre de la page) ; aucun « % » ; masqués dans l'Aura vide. · *Décision* : v95 (29 sept. 2026), `ETAT-DES-LIEUX.md:9768-9773`. · *Juge* : `redteam_ecrans.py`, `releve-aura.py` · ⚠ La règle anti-notation 2 dit « un seul chiffre, le tien, global » : voir T-1.

**R-016 · Rien ne recule jamais : aucune grandeur dessinée ne décroît parce que le temps passe.**
*Vérifier* : aucune distance, aucun rayon, aucune taille liée à une personne ne diminue sans action de l'utilisateur. · *Décision* : 9 sept. 2026, `AUDIT-PELOTE.md` l.60-68 (« un compte à rebours dessiné en rond et pointé vers une personne »). · *Juge* : —

**R-017 · Les mots du Noyau ne sont jamais un reproche, et leur échelle est monotone.**
*Vérifier* : les cinq mots (rayonnante ≥ 85 · solide 65-84 · installée 40-64 · naissante < 40 · à tisser) ; le plus bas dit « ça commence ». · *Décision* : Tom, Q165 bis (« on le garde, si aucun ne blesse »). · *Juge* : — · ⚠ Ces mots ne s'attachent qu'à soi (R-011).

**R-018 · Un seul compteur dans l'app : celui du Fil, et il ne redescend que quand on a agi.**
*Vérifier* : le compteur du Fil compte ce qui attend un geste de moi ; il ne baisse pas à la simple ouverture ; ni l'Index ni l'accueil n'affichent « N paroles · M Cercles » ; une promesse à soi-même ne produit ni compteur ni pastille. · *Décision* : Tom, 27 sept. 2026 (Q347), mots validés le 28 sept. · *Juge* : — · C-036 reste OUVERT dans `CHANTIERS.md`.

**R-019 · L'état reste un signal fixe : il ne suit ni la palette, ni le monde, ni le thème.**
*Vérifier* : rendre un écran sous deux palettes éloignées ; légende de l'Aura, arcs des Noyaux, traits et libellés d'état sont identiques au pixel. · *Décision* : Tom, 20 sept. 2026 (« le vert n'est “tenu” que parce qu'il est toujours vert »). · *Juge* : `redteam_decisions.py`

### A3 · Les notifications

**R-020 · Aucune demande de permission au lancement.**
*Vérifier* : au premier lancement, aucune invite du système. · *Décision* : v109 (30 sept. 2026) ; `ETAT` §7. · *Juge* : `redteam_notifs.py`

**R-021 · « Je te le rappelle ? · oui · pas besoin » ne paraît qu'après la plantation d'une parole DATÉE ; la permission n'est demandée qu'après « oui ».**
*Vérifier* : l'invite paraît 1,9 s après la plantation, sous le plateau de l'accueil, part seule après 12 s ; rien pour une parole sans date. · *Décision* : v109-v110. · *Juge* : `redteam_notifs.py`

**R-022 · Deux « pas besoin » d'affilée, puis plus jamais la question.**
*Vérifier* : après deux refus consécutifs, planter une parole datée ne montre plus l'invite. · *Décision* : v109. · *Juge* : `redteam_notifs.py`

**R-023 · Rien quand la date est passée.**
*Vérifier* : une parole dont l'échéance est dépassée ne programme et n'émet aucune notification. · *Décision* : v109 (`ETAT` §7 : « Aucune qui reproche, ni série, ni score »). · *Juge* : `redteam_notifs.py`

**R-024 · Une notification par jour au plus.**
*Vérifier* : sur vingt-quatre heures, le journal des envois compte au plus une entrée ; la mémoire des paroles en l'air, une par semaine au plus. · *Décision* : v109. · *Juge* : `redteam_notifs.py`

**R-025 · Les mots des notifications sont ceux-là, au caractère près.**
*Vérifier* : « Demain, c'est « {titre} ». » · « Tu as promis ça à {Prénom}. Demain. » · « Ton Chiche à {Prénom} arrive demain. » · « C'est aujourd'hui. » · « « {titre} » flotte toujours. Un de ces jours ? » · *Décision* : v109-v110 ; `SPEC-JUGES.md` §3. · *Juge* : `redteam_notifs.py`

**R-026 · Aucun événement négatif n'est notifié.**
*Vérifier* : aucune notification ne signale une baisse, un retard, un retrait. · *Décision* : règle anti-notation 6. · *Juge* : —

### A4 · Les murs de Ma Parole !

**R-027 · Un réglage réservé est flouté à 4,8 px, sans encart, sans cadenas, sans explication.**
*Vérifier* : `filter: blur(4.8px)` sur le réglage ; aucun bloc « Ma Parole ! » ne l'accompagne. Le Studio garde ses propres flous. · *Décision* : Tom, 30 sept. 2026 (v104-v105 : « on ne donne pas ce qu'on vend »). · *Juge* : `redteam_murs.py`

**R-028 · Au toucher d'un mur, une phrase paraît seule sur le flou, le temps d'être lue, puis s'efface.**
*Vérifier* : centrée dans le mur, sans fond ni cadre, ≤ 3 lignes, une taille (34 px, réduite s'il le faut), encre `#201908` en clair et crème `#F7F0DE` en sombre ; durée 1,4 s + 60 ms par caractère, bornée à [3 ; 5,5] s. · *Décision* : Tom, v105 (« pas de plateau : ça fait bon marché »). · *Juge* : `redteam_murs.py`

**R-029 · L'offre ne s'ouvre seule que la toute première fois ; ensuite elle ne s'ouvre que si l'on touche pendant la lecture.**
*Vérifier* : premier mur → l'offre s'ouvre à la fin de la lecture ; murs suivants → rien sans toucher. · *Décision* : Tom, v104. · *Juge* : `redteam_murs.py`

**R-030 · Les phrases des murs sont les dix-huit de Tom, dans l'ordre, puis au hasard sans répéter la précédente ; le compteur est global et se remet à zéro après quatorze jours sans mur.**
*Vérifier* : la liste de `ETAT` §6 ; un seul compteur pour tous les murs. · *Décision* : Tom, 5 oct. 2026 (v133, C-063) ; Q352. · *Juge* : `redteam_murs.py` · ⚠ `SPEC-JUGES.md` §2 écrit encore « 21 phrases ».

**R-031 · Rien de tout cela chez un membre : aucun mur, aucune phrase.**
*Vérifier* : avec Ma Parole !, aucun flou de mur, aucun déclenchement. · *Décision* : v104. · *Juge* : `redteam_murs.py`

**R-032 · On ne livre pas un réglage qu'on ne peut pas éteindre.**
*Vérifier* : tout comportement automatique a sa commande visible ; sinon il ne s'active pas seul. · *Décision* : v118 (le Zzz sans bouton). · *Juge* : `redteam_nuit.py` (rouge par décision : le Zzz est coupé depuis v120)

### Tensions à trancher (elles ne sont pas des règles)

- **T-1 · ⚠ TROU.** La règle anti-notation 2 (« un seul chiffre, le tien, global ») et `DECISIONS.md` A1 (« pas de pourcentage, pas de “3 sur 5 tenus” ») ne s'accordent pas avec l'Aura d'aujourd'hui, qui porte trois chiffres (v95), ni avec la liste « Ce que tu as tenu », qui montre toutes les paroles tenues et s'allonge (v131). Aucune décision ne dit laquelle prime.
- **T-2 · ⚠ TROU.** « Ton meilleur Cercle » figure dans le relevé v106 ; la règle 5 l'interdit. Non vérifié à l'écran.
- **T-3 · ⚠ TROU.** Le Fil permet de « REPORTER » (ajout validé, 20 août) : sa compatibilité avec « rien ne reproche » n'est écrite nulle part.

---

## B · LES LOIS DU DESSIN

### B1 · La couleur

**R-033 · Un écran de fiche porte toujours trois couleurs distinctes : la dalle, le champ, le trait.**
*Vérifier* : sur chaque fiche, couleur dominante de la dalle ≠ champ ≠ trait (ΔE ≥ 15 deux à deux). · *Décision* : `CLAUDE.md` §3 (repris le 30 sept. 2026). · *Juge* : `redteam_tonsurton.py`

**R-034 · Le champ dit la nature, la ligne dit l'état — sans exception.**
*Vérifier* : bande haute et champ = `#82AEF8` / `#FFB8D2` / `#C9A8F5` selon la nature, quels que soient l'état et le thème ; le trait porte l'état. · *Décision* : Tom, direction Horizon. · *Juge* : `redteam_decisions.py`, `redteam_champ.py`

**R-035 · Un champ blanc n'existe jamais.**
*Vérifier* : au-dessus du trait, aucun pixel d'une couleur de corps, aucun champ transparent, sur tous les écrans et dans les deux thèmes ; un gardé de côté garde le champ de sa nature, sans matière. · *Décision* : Tom, 29 août 2026, « sans exception » (Q101, Q83). · *Juge* : `redteam_champ.py`

**R-036 · La dalle porte le monde, l'accent porte la nature.**
*Vérifier* : dans l'Index, le Fil et sur la Toile, la nature se lit à un libellé, une pastille, un contour — jamais à la teinte de la dalle. · *Décision* : lot 25 ; `CLAUDE.md` §4. · *Juge* : `redteam_reperage.py`

**R-037 · Exception : sous Ingénu seulement, la couleur d'une dalle dit sa nature.**
*Vérifier* : palette `signal` → Promi bleu, Chiche rose, Cercle lilas, cellules neutres crème dalle `#EFE3C7` ; sous toute autre palette, la dalle reprend sa couleur figée. · *Décision* : Tom, 21 sept. 2026 (Q292, Q297). · *Juge* : `redteam_dalle_figee.py`

**R-038 · Exception : dans la bande haute d'une fiche et le champ de la page +, et nulle part ailleurs, la dalle prend la rampe de sa nature.**
*Vérifier* : écart de luminosité dalle / champ ≥ 42 dans la bande ; la forme reste celle du moteur. Avec « La dalle d'origine », la couleur d'origine tient sauf si ΔE < 15 face au champ. · *Décision* : Tom, 18 août 2026 (Q30) ; v118 (Q365). · *Juge* : `redteam_origine.py`

**R-039 · Tout suit le Studio (monde et palette), sauf l'Aura.**
*Vérifier* : Toile, Index, Fil, fiches, page +, Partager, Toile d'un Cercle changent avec le Studio ; les îles de la Pelote et « Ce que tu as tenu » gardent le monde et la couleur de plantation. · *Décision* : Tom, 23 sept. 2026 (v34). · *Juge* : `redteam_decoupe.py` (H), `redteam_dalle_figee.py`

**R-040 · Jamais de ton sur ton.**
*Vérifier* : un texte sur son fond, écart de luminosité ≥ 42 ; un trait ou une matière sur un aplat coloré, ΔE (CIELAB) ≥ 15. · *Décision* : `CLAUDE.md` §3 ; Tom, 18 sept. 2026 (Q216). · *Juge* : `redteam_tonsurton.py` · Exceptions nommées : `JETONS.json › couleurs.exceptions` (texte crème sur `#0E78F2`, 3,70:1).

**R-041 · Jamais de trait neutre ou gris.**
*Vérifier* : tout filet rendu a une chroma non nulle et vient du jeu ; aucun trait horizontal hors de la liste du moodboard. · *Décision* : `CLAUDE.md` §3. · *Juge* : `redteam_filets.py`, `releve-design.py`

**R-042 · Jamais de kaki.**
*Vérifier* : aucune dalle ni matière vide produite par l'app n'a une couleur en OKLCH h 78-140°, C 0,015-0,10, L 0,20-0,80 — source, rendu des vingt mondes en clair et en sombre. Seule exception : la couleur mère choisie dans la jauge. · *Décision* : Tom, 30 sept. 2026 (v114), bornes v115. · *Juge* : `redteam_kaki.py` (⚠ rouge à la naissance : 34 couleurs coupables recensées, Q360 — « on ne touche à aucune palette »)

**R-043 · Un anneau ne porte que trois arcs : à tenir, en cours, tenu.**
*Vérifier* : au plus trois arcs, dans `#DD4D23`, `#291547`, `#00341A`, sans opacité ; les deux sens (ce que tu tiens, ce qu'on te tient) sont concaténés avant le calcul des parts, pondérés par le nombre de paroles. · *Décision* : Tom, 22 sept. 2026. · *Juge* : `redteam_decisions.py` (anneau)

**R-044 · Les jours d'un anneau valent 3 px d'arc, tous égaux, le premier centré sur midi.**
*Vérifier* : n arcs, n jours ; jour = 3 / r radians par anneau ; aucun fondu entre segments ; un état seul laisse 0,1° ouvert. · *Décision* : Tom, 23 sept. 2026. · *Juge* : —

**R-045 · L'amande `#8FE08F` ne peint que la célébration et la mention « TENU(E) ».**
*Vérifier* : balayage de tous les écrans ouverts un à un, bornés à l'appareil : aucune surface, aucun arc, aucun autre texte en amande — hors le tenu posé sur la terre `#2B1020`. · *Décision* : Tom, 22 et 23 sept. 2026. · *Juge* : `redteam_decisions.py`

**R-046 · `#DD4D23` est une couleur d'état et ne sert à rien d'autre.**
*Vérifier* : aucun bouton, aucune alerte, aucune action de suppression en `#DD4D23` (« SUPPRIMER CE PROMI » : crème en sombre, encre en clair). · *Décision* : Tom, 5 oct. 2026 (v132, C-053). · *Juge* : `redteam_decisions.py` · ⚠ C-015 reste ouvert pour les Réglages.

**R-047 · L'orange de « Ma Parole ! » n'existe que dans les mots des murs.**
*Vérifier* : `#FB4C0D`, `#FF7A55`, `#FED0C3` n'apparaissent nulle part ailleurs, ni dans la source ni à l'écran. · *Décision* : Tom, v122. · *Juge* : `redteam_maparole.py`

**R-048 · Une marque suit ce qui est peint sous elle, pas le thème.**
*Vérifier* : sur la terre d'une fiche tenue, texte crème et tenu en amande dans les deux thèmes ; sur un champ pastel, texte à l'encre `#201908`. · *Décision* : Tom, 17 et 23 sept. 2026. · *Juge* : `redteam_decisions.py`

**R-049 · Une teinte de palette qui doit se lire garde sa teinte : seule sa clarté bouge.**
*Vérifier* : « PARTAGER MA PELOTE » ≥ 3:1, « Garder ta Toile » ≥ 4,5:1, même teinte OKLCH que le ton tiré, jamais kaki, jamais de repli sur l'encre. · *Décision* : Tom, v125. · *Juge* : `redteam_bouton.py`, `redteam_garder_toile.py`

**R-050 · La couleur du texte et son remplissage sont toujours la même valeur.**
*Vérifier* : (prototype) `-webkit-text-fill-color` = `color` ; (Swift) un seul attribut de couleur par texte. · *Décision* : `CLAUDE.md` §3. · *Juge* : —

### B2 · La dalle et la matière

**R-051 · Une dalle est engendrée, jamais découpée.**
*Vérifier* : le peintre d'un monde reçoit la dalle à peindre et n'engendre qu'elle, à sa taille finale, posée 1:1 ; aucune image recadrée, redimensionnée ou relue ; une dalle rendue seule porte ≤ 0,3 % de pixels d'une autre couleur que la sienne. · *Décision* : Tom, 23 sept. (v29) et 5 oct. 2026 (v130, C-048 : « interdit, définitivement, dans le prototype comme dans Swift »). · *Juge* : `redteam_decoupe.py` (G2), `banc_rendu.py`

**R-052 · Jamais un polygone, un hexagone ou une forme reconstruite à la place d'une dalle.**
*Vérifier* : toute dalle affichée sort du peintre du monde. · *Décision* : `CLAUDE.md` §4 règle 1, §9. · *Juge* : `redteam_decoupe.py`

**R-053 · La dalle-sujet est à opacité 1, sans filtre, sans voile, sans masque, au premier plan.**
*Vérifier* : sur une dalle de fiche, de tuile, de partage : opacité 1, aucun calque par-dessus. Un fond d'ambiance (la trame de la page +) peut être masqué. · *Décision* : `CLAUDE.md` §4 règles 3-4 (lot 2B). · *Juge* : `releve-design.py`

**R-054 · Une dalle garde son identité : sa couleur et son monde de plantation sont figés, tirés de son titre et de sa personne, jamais d'un identifiant ni d'une horloge.**
*Vérifier* : recharger trois fois ; par titre et personne, même emplacement de palette et même nuance. · *Décision* : Tom, 4 et 13 sept. 2026 (Q213). · *Juge* : `redteam_dalle_figee.py`

**R-055 · Un semis est déterministe : même Toile, même composition, à chaque ouverture, dans les deux thèmes.**
*Vérifier* : trois ouvertures × deux thèmes × deux densités : quelle dalle occupe quelle case ne change pas. On compare la case, jamais les pixels. · *Décision* : Tom, 19 août 2026. · *Juge* : `banc_rendu.py --deux`

**R-056 · Aucune parole ne disparaît de la Toile, quel que soit leur nombre.**
*Vérifier* : à 500 paroles, chacune a sa cellule ; les titres s'effacent sous 48 px de dalle. · *Décision* : Tom, 29 sept. 2026 (v98). · *Juge* : —

**R-057 · La Pelote est le seul volume : nulle part ailleurs un halo, une ombre floue ou un dégradé.**
*Vérifier* : statique — aucun flou d'ombre, aucun dégradé, aucun halo hors de la Pelote ; rien ne dépasse de sa silhouette ; elle est pleine (alpha 255 en retrait de 4 % de D). · *Décision* : Tom, 30 sept. 2026 (v114) ; v116 ; v120. · *Juge* : `redteam_volume.py`, `redteam_contour.py`, `redteam_plein.py`, `redteam_halo.py`

**R-058 · Les écrans reflètent l'état réel à l'image suivante : une seule source de vérité, la liste des paroles.**
*Vérifier* : planter, tenir, retirer par les vrais boutons ; Index, Fil, Aura, fil du Cercle sont à jour sans rouvrir ; le Fil ne montre jamais une parole retirée. · *Décision* : Tom, 5 oct. 2026 (v130, C-049). · *Juge* : `redteam_reactif.py`

### B3 · Les contours, les composants, les réglages

**R-059 · Tout contour : trait 2 px, couleur du corps, rayon = hauteur ÷ 2 ; au-delà de 94,5 de haut, rayon 30.**
*Vérifier* : les trois cotes sur chaque cadre de chaque écran. · *Décision* : Tom, 2 et 11 sept. 2026 (Q203). · *Juge* : `redteam_cercle_couleur.py` et les relevés de section

**R-060 · Les composants communs sont identiques partout.**
*Vérifier* : plateau 342 × 60 à 24 / 40 ; « ✕ FERMER » en haut à droite (haut 50) ; Peaufiner 62, en bas de chaque fiche ; le geste, 118 de haut, deux points, un trait, toujours entier ; « Moi » premier des destinataires (« tout le monde » devant lui dans un Cercle) ; boutons ronds en icône seule. · *Décision* : `CLAUDE.md` §5. · *Juge* : `redteam_ecrans.py`, `releve-design.py`

**R-061 · Un réglage vit là où vit ce qu'il règle.**
*Vérifier* : le Studio ne porte que le global (monde, palette, écran sombre ou clair, texte) ; ce qui appartient à une parole (le pinceau) se choisit à la page + et se reprend dans Peaufiner. Test : « ce réglage a-t-il un sens différent d'un Promi à l'autre ? ». · *Décision* : Tom, 31 août 2026. · *Juge* : —

**R-062 · Sur la fiche d'un Cercle, Peaufiner ne s'ouvre qu'en touchant sa barre ; le doigt qui descend fait défiler le fil.**
*Vérifier* : glisser vers le bas sur une fiche de Cercle fait défiler ; état défilé : bande de 114 (base 58, amplitude 16). · *Décision* : §13 des spécifications, repris par `CLAUDE.md` §5. · *Juge* : `redteam_nuee.py`

**R-063 · Un Cercle se lance en traçant le trait entier ; un Promi et un Chiche gardent leur moitié.**
*Vérifier* : le tracé d'un Cercle va de 0 à 390. · *Décision* : Tom, 19 août 2026. · *Juge* : `redteam_nuee_entree.py`

**R-064 · Ce qui se touche est joignable, et se prouve au doigt.**
*Vérifier* : au centre de chaque élément interactif, l'élément sous le doigt est lui-même ou un descendant ; toute porte est essayée par un vrai toucher, dans toutes les directions pour un geste. · *Décision* : v118 ; v126 (C-010). · *Juge* : `redteam_joignable.py`

### B4 · Le temps

**R-065 · Rien ne paraît une fraction de seconde.**
*Vérifier* : image par image, à l'ouverture, entre le + et la nature, à la plantation : aucune couche de premier plan ne vit moins de 800 ms ; un écran paraît composé dès sa première image ; une plantation coupe. · *Décision* : Tom, 30 sept. 2026 (v103). · *Juge* : `redteam_flash.py`, `redteam_flash_etat.py`

**R-066 · Un changement de thème ne se fait jamais sous les yeux.**
*Vérifier* : seulement au changement d'écran ou au retour au premier plan, sans fondu. · *Décision* : Tom, 2 oct. 2026 (v118). · *Juge* : `redteam_nuit.py` · ⚠ Le Zzz est coupé depuis v120 ; la règle reste écrite.

**R-067 · Un mouvement se calcule sur le temps réel, jamais sur le compte d'images — sauf Houle.**
*Vérifier* : la fin du mouvement d'un monde à ± max(100 ms, 8 %) des valeurs de `SPEC-JUGES.md` §1, sous charge comme au repos ; Houle se juge en images. · *Décision* : Tom, 10 et 27 sept. 2026 (v61). · *Juge* : `redteam_rythme.py`

**R-068 · Tenir une parole est fluide.**
*Vérifier* : pendant l'animation (1 000 ms), aucune image au-delà de 20 ms de travail du fil principal, p95 ≤ 16,7 ms. · *Décision* : Tom, v124. · *Juge* : `redteam_fluide.py`

**R-069 · La Toile vit au repos, et revient exactement à l'image d'avant.**
*Vérifier* : toutes les 5 à 15 s, une ou deux dalles bougent 1 à 2 s ; 0 pixel d'écart au retour ; rien sous « Réduire les animations », écran couvert ou dans les 5 s d'un toucher ; le titre ne bouge pas. · *Décision* : Tom, v126-v128 (C-028). · *Juge* : `redteam_vivant.py`, `redteam_retour.py` · Quatre mondes restent immobiles (Volubilis, Guingois, Ramage, Esquille) : reporté au portage (C-031).

**R-070 · Le clavier s'ouvre dans le geste, jamais en différé.**
*Vérifier* : la prise de focus d'un champ a lieu dans le gestionnaire du toucher. · *Décision* : v114. · *Juge* : `redteam_clavier.py`

### B5 · Les points, le dessin

**R-071 · LA LOI DES POINTS — « Les points disent qu'il manque quelque chose : une moitié de trait, un mot, un engagement. Ils ne servent jamais à autre chose. »**
*Vérifier* : tout motif en points ou en pointillé à l'écran correspond à un manque (moitié de trait non tracée, mot non écrit, gardé de côté) ; aucun point ne sert de commande, de repère ni d'ornement. · *Décision* : Tom, 4 oct. 2026 (v128, C-044), texte dicté. · *Juge* : —

**R-072 · Exception nominative à la loi des points : les trois petits points du choix de taille de l'outil de dessin.**
*Vérifier* : au second toucher sur la plume ou la gomme, trois points côte à côte, de taille croissante, à l'encre du mode ; aucun autre point-commande dans l'app. · *Décision* : Tom, 4 oct. 2026 (v127). · *Juge* : `redteam_dessin.py`

**R-073 · En mode dessin, rien ne se superpose à la surface, sauf le ✕ de sortie.**
*Vérifier* : la surface (390 × 742) va du haut de l'écran à la rangée d'outils ; rangée en bas, déploiements 16 pt au-dessus d'elle, repliés dès le choix fait ; seul le ✕ « Quitter le dessin » (dans le contour de l'encart) la recouvre ; tout revient à POSER ou à la sortie, sans fondu. · *Décision* : Tom, v130 (cinquième principe), v132, v133 (C-056). · *Juge* : `redteam_dessin.py` (`--sonde=superpose`, `--sonde=quitter`)

**R-074 · Un dessin est une liste de traits, jamais une image.**
*Vérifier* : le modèle stocké est `{fond, traits:[{c, t, g, pts}], poses, pose, masque}` ; aucun bitmap n'est sauvegardé. · *Décision* : Tom, 5 oct. 2026 (v132). · *Juge* : `redteam_dessin.py`

**R-075 · Chaque trait garde sa couleur ; après le premier POSER, le fond est fixé et les nouveaux traits ne prennent que les couleurs déjà présentes.**
*Vérifier* : trois traits sous trois palettes : leurs couleurs ne changent pas au changement de palette. · *Décision* : Tom, v132. · *Juge* : `redteam_dessin.py` (`--sonde=couleurs`)

**R-076 · Le dessin remplace la dalle ou la photo dans la bande : la bande montre une chose à la fois.**
*Vérifier* : dalle, photo ou dessin, jamais deux ; la couche s'arrête 7 pt au-dessus de l'axe du trait d'état ; « Retirer le dessin » rend la dalle ; les cartes de l'Index et du Fil gardent la dalle. · *Décision* : Tom, v128, v132 ; Q395 validée. · *Juge* : `redteam_dessin.py`

**R-077 · Un dessin masqué n'est jamais emporté dans un partage.**
*Vérifier* : masquer, partager : la case du Folio montre la dalle. · *Décision* : Tom, v132. · *Juge* : `redteam_dessin.py` (`--sonde=partage`)

**R-078 · Sans Ma Parole !, on dessine à l'encre du mode sur le champ de la nature ; les teintes sont un mur.**
*Vérifier* : panneau COULEUR flouté à 4,8 px, la phrase des murs monte dessus. · *Décision* : Tom, v133 (C-061). · *Juge* : `redteam_dessin.py` (`--sonde=mur`)

**R-079 · Toucher une photo ou un dessin dans la bande l'ouvre en entier, sur un fond plein ; une dalle n'ouvre rien.**
*Vérifier* : fond seiche opaque, image entière, sans ombre ni fondu ; un toucher ou ✕ referme ; VoiceOver « Voir la photo en entier ». · *Décision* : Tom, v131 (C-051). · *Juge* : `redteam_entier.py`

### B6 · Le texte

**R-080 · L'air entre deux textes se mesure à l'encre, jamais à la boîte, et ne se resserre pas.**
*Vérifier* : écart entre les rectangles du TEXTE (ascendantes et descendantes), contre la référence, tolérance 0,6 px ; sous un texte qui peut passer à la ligne, aucune cote n'est figée. · *Décision* : Tom, 10 et 30 sept. 2026. · *Juge* : `redteam_air.py`, `releve-aura.py` · Pertes d'air voulues : bloc v102.

**R-081 · Aucun texte sous 12 px ; aucune opacité sous 72 % sur un texte à lire.**
*Vérifier* : sur tous les écrans, taille calculée ≥ 12 et opacité effective ≥ 0,72. · *Décision* : `CLAUDE.md` §6. · *Juge* : — · ⚠ le niveau « meta » du jeu est à 0,65.

**R-082 · Trois polices, cinq faces ; aucune graisse hors d'elles.**
*Vérifier* : tout couple famille / graisse demandé est l'un de Gilbert 700, Atkinson 400 / 500 / 700, PromiLate 400. · *Décision* : Tom, 22 sept. 2026. · *Juge* : `redteam_polices.py`, `redteam_tokens.py`

**R-083 · Gilbert s'écrit en capitales (sous-titres, libellés, navigation) ; PromiLate ne porte que les titres d'écran, le mot-marque et les phrases du trait.**
*Vérifier* : par texte, la famille rendue et la casse. Exception : l'onboarding, en Gilbert minuscules. · *Décision* : Tom, 16-18 sept. 2026 ; v127. · *Juge* : `redteam_onboarding`

**R-084 · Le crédit de Gilbert figure dans l'écran « à propos », et ses glyphes ne sont pas modifiés.**
*Vérifier* : la mention « Gilbert — Type With Pride, Ogilvy & Mather, CC BY-SA 4.0 » est à l'écran ; le fichier de police est celui d'origine. · *Décision* : Tom, 16 sept. 2026. · *Juge* : —

**R-085 · Aucune couleur ni aucune police en dur dans une vue : tout passe par le jeu.**
*Vérifier* : statique — zéro hexadécimal et zéro nom de police hors du fichier de jetons. · *Décision* : Tom, 16 sept. 2026. · *Juge* : `redteam_tokens.py` (46/46 le 6 oct. 2026)

**R-086 · Le mot de la nature est à la même hauteur dans son encart pour les trois natures.**
*Vérifier* : encre de PROMI, CHICHE, CERCLE de 58,7 à 81,3 (milieu 70), ± 0,5 pt. · *Décision* : v129 (C-046). · *Juge* : `redteam_motmarque.py`

**R-087 · Les cotes de l'Aura sont figées sur la composition B, à ± 0,5 pt.**
*Vérifier* : `JETONS.json › espacements.aura.cotesB`. · *Décision* : Tom, 4 oct. 2026 (v126, C-005). · *Juge* : `releve-aura.py`

---

## C · LE LEXIQUE

### C1 · Le vocabulaire

| Affiché | Sens | Clé interne | Règle d'écriture |
|---|---|---|---|
| **Promi** | une promesse, une dalle | `promi` | invariable : « trois Promi » |
| **dalle** | la forme colorée d'un Promi sur la Toile | — | « mes dalles » reste le nom de la Toile |
| **Chiche** | un défi lancé | `chiche` | on LANCE un Chiche, on ne le plante pas |
| **Cercle** | un collectif de Promi | `nuee`, `NUE`, `curNuee` | masculin ; était « Nuée » jusqu'au 30 sept. 2026 |
| **Ma Parole !** | l'offre payante | `ouvreCercle`, `.s2-cercle`, `isPremium` | espace insécable avant « ! » ; était « Le Cercle » |
| **gardé de côté** | un Promi pas encore planté | `draft` | « brouillon » est banni |
| **Toile** | le canevas des dalles | `Toile` | majuscule |
| **Fil** | le flux d'activité | `#feedView` | |
| **Index** | la liste des Promi | `#indexSheet` | |
| **Aura** | l'écran de progression | `#auraScreen` | ex-« Karma » |
| **Pelote** | la boule de l'Aura | `_aura` | « sphère » et « Orbite » sont morts |
| **Noyau** | un anneau à trois arcs | `.kring`, `.au-nb` | |
| **Studio** | le choix du monde et de la palette | `#studioScreen` | |
| **Peaufiner** | le tiroir de réglages d'une fiche | `.s2-*` | |
| **Folio** | ce qu'on partage de ses dalles | — | « Mon Folio » |
| **planter** · **tenir** · **tracer** · **lancer** | créer un Promi · honorer sa parole · faire le geste · créer un Chiche ou un Cercle | | |

Sources : `CLAUDE.md` §2 ; `ETAT-30-SEPTEMBRE-2026.md` §1 ; `RENOMMAGE-LEXIQUE.md` (v106, Tom, 30 sept. 2026).

### C2 · Règles vérifiables sur les chaînes

Objet de la vérification, sauf mention : **toute chaîne affichée ou lue par VoiceOver** (textes, libellés d'accessibilité, invites, notifications), nœuds cachés compris.

**R-088 · Aucune chaîne ne contient un terme banni.**
*Vérifier* : recherche insensible à la casse de : « tâche », « to-do » (et « todo »), « objectif », « valider » (et ses formes), « urgent », « score », « brouillon », « Orbite », « sphère », « Nuée », « Karma ». · *Décision* : `CLAUDE.md` §2 (liste complétée par Tom, 18 août 2026 ; « Orbite » et « la sphère » le 23 sept. ; « Nuée » remplacée le 30 sept.). · *Juge* : relevé v106 (`scratchpad/tout_texte.py` : zéro « Nuée ») ; aucun juge permanent · ⚠ Dette connue : « Brouillon de Cercle… » (`#dkNueeNote`, cachée), `RENOMMAGE-LEXIQUE.md` §5.

**R-089 · « échéance » n'est jamais le libellé d'un champ.**
*Vérifier* : aucune étiquette de champ ou de réglage ne vaut « échéance ». · *Décision* : `CLAUDE.md` §2. · *Juge* : —

**R-090 · Trois boutons n'existent pas : « Belle parole », « En replanter un », et « Dire un mot » en gros bouton.**
*Vérifier* : aucune commande ne porte ces libellés. · *Décision* : `CLAUDE.md` §2. · *Juge* : —

**R-091 · « Promi » est invariable.**
*Vérifier* : aucune occurrence de « Promis » comme pluriel du nom (expression : nombre ou déterminant pluriel suivi de « Promis »). · *Décision* : `CLAUDE.md` §2. · *Juge* : —

**R-092 · « Cercle » est masculin.**
*Vérifier* : aucune occurrence de « une Cercle », « la Cercle », « cette Cercle », « ta Cercle », « ma Cercle », « quelle Cercle », « aucune Cercle » ; les participes s'accordent au masculin (« CERCLE REJOINT », « Cercles illimités »). · *Décision* : Tom, 30 sept. 2026 (v106) ; table des accords, `RENOMMAGE-LEXIQUE.md` §4. · *Juge* : relevé v106

**R-093 · « Ma Parole ! » s'écrit avec une espace insécable avant le « ! », deux majuscules.**
*Vérifier* : toute occurrence correspond à `Ma Parole !` (ou `MA PAROLE !` en capitales) ; aucune espace ordinaire, aucun « Ma Parole! ». · *Décision* : Tom, v105-v106. · *Juge* : `redteam_maparole.py`, `redteam_murs.py`

**R-094 · L'offre ne s'appelle jamais « le Cercle », et un Cercle ne s'appelle jamais « Nuée ».**
*Vérifier* : « Cercle » à l'écran désigne toujours un groupe ; les formules de l'offre sont « Avec Ma Parole ! », « Tu es Membre Ma Parole ! », « Retourne ta Toile », « Bon, allez d'accord ». · *Décision* : Tom, 30 sept. 2026 (v106-v107, Q355). · *Juge* : relevé v106

**R-095 · On plante un Promi, on lance un Chiche et un Cercle, on tient sa parole, on trace.**
*Vérifier* : aucun « planter un Chiche », aucun « créer / ajouter une promesse », aucun « terminer », « cocher », « accomplir ». · *Décision* : `CLAUDE.md` §2 ; `IDENTITE-VERBALE.md` (D3, Tom, 17 sept. 2026). · *Juge* : — · ⚠ `RENOMMAGE-LEXIQUE.md` §4 garde « Planter (un Promi) dans le Cercle » et « appuie sur Planter pour le créer » : planter y vise le Promi.

**R-096 · « Zzz » s'écrit exactement ainsi.**
*Vérifier* : Z majuscule, zz minuscules, même entre des voisins en capitales ; VoiceOver « Mode nuit, activé / désactivé ». · *Décision* : Tom, 2 oct. 2026 (v118). · *Juge* : `redteam_nuit.py` · ⚠ coupé depuis v120.

**R-097 · Les noms de monde et de palette sont ceux du Studio, accents compris.**
*Vérifier* : vingt mondes (`ETAT` §4) et vingt-quatre palettes (`JETONS.json › palettes`) ; les clés internes gardent les anciens noms et ne s'affichent jamais. · *Décision* : `ETAT` §4-§5. · *Juge* : `redteam_palettes.py`

**R-098 · Les libellés d'accessibilité décidés sont ceux-là.**
*Vérifier* : « Voir la photo en entier » · « Voir le dessin en entier » · « Quitter le dessin » · « Dessiner sur ce Cercle » · « Mode nuit, activé / désactivé ». · *Décision* : v118, v131, v132, v133. · *Juge* : `redteam_entier.py`, `redteam_dessin.py`

**R-099 · Le registre : aucune injonction, aucun point d'exclamation hors du nom « Ma Parole ! ».**
*Vérifier* : hors « Ma Parole ! », aucune chaîne ne contient « ! ». · *Décision* : `IDENTITE-VERBALE.md`, en-tête (registre demandé, tranché par Tom le 17 sept. 2026). · *Juge* : — · **⚠ TROU** : écrit pour les trois natures de la page + ; son extension à toute l'app n'est pas décidée, et l'offre a porté « Rejoins le Cercle ! ».

**R-100 · Un mot qui manque : le mot du moodboard d'abord ; à défaut le plus sobre du lexique, noté « à valider ».**
*Vérifier* : toute chaîne nouvelle a une source (moodboard, décision) ou une entrée « à valider » au registre. · *Décision* : Tom, 18 août 2026. · *Juge* : `redteam_registre.py` (pour le registre des chantiers)

---

## TROUS

1. **⚠ TROU : la grille anti-coercition n'est écrite nulle part.** Elle n'est que citée (« la grille l'interdit », v118). La section A est une reconstitution.
2. **⚠ TROU : les huit règles anti-notation** n'ont pas de texte d'origine ni de date de décision dans les sources lues ; seul le tableau d'audit du 3 sept. 2026 les énonce. La règle 8 (« visible de toi seul ») est contredite par le partage de la Pelote (v114-v124) : non tranché.
3. **⚠ TROU : T-1** — « un seul chiffre » et « pas de pourcentage » face aux trois chiffres de l'Aura (v95) et à la liste « Ce que tu as tenu » qui s'allonge (v131).
4. **⚠ TROU : T-2** — « Ton meilleur Cercle » (relevé v106) face à « aucun superlatif ».
5. **⚠ TROU : T-3** — « REPORTER » dans le Fil.
6. **⚠ TROU : R-005** (« on ne défait pas une parole tenue ») n'est écrite que dans une note du moodboard.
7. **⚠ TROU : aucun juge permanent ne porte les termes bannis** ni les accords (R-088 à R-095) : seuls des relevés ponctuels (v106).
8. **⚠ TROU : aucun juge ne porte** la loi des points (R-071), le jour d'anneau de 3 px (R-044), les tailles minimales de texte (R-081), ni « un réglage vit là où vit ce qu'il règle » (R-061).
9. **⚠ TROU : R-099** — la portée du registre « aucun point d'exclamation ».
10. **⚠ TROU : `SPEC-JUGES.md` §2 écrit « 21 phrases »** ; elles sont dix-huit depuis v133.
11. **⚠ TROU : `redteam_kaki.py` est rouge** (34 couleurs, quinze palettes sur vingt-quatre mesurées en v114) et Q360 interdit de toucher aux palettes : la règle R-042 n'est pas tenue par l'app.
12. **⚠ TROU : le Zzz** (R-066, R-096) est coupé « jusqu'à nouvel ordre » : à porter ou non, non décidé.
