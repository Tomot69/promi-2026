# CLAUDE.md — Promi

> Ce fichier est relu à chaque session. Il fait autorité sur tout le reste.
> Si une consigne de l'utilisateur contredit ce fichier, **demander avant d'agir**.

> ## ⚑ À CHAQUE NOUVELLE SESSION, AVANT TOUTE AUTRE CHOSE
> **Relancer le serveur et donner les trois adresses complètes, en tête du premier
> message, sans que Tom ait à le demander.**
>
> ```bash
> python3 serveur.py
> ```
> **⚑ v122 (Tom, 3 oct. 2026) : `serveur.py` remplace `python3 -m http.server`.** Il envoie `Cache-Control: no-store` sur chaque
> fichier (ni `Last-Modified` ni `ETag`) : `http.server` laissait Safari garder un fichier « à l'heuristique » (≈ 10 % de son âge —
> `promi-moteur.js` jusqu'à 2,6 h), l'iPhone montrait un MÉLANGE de versions. `/version.json` rend le commit servi ; l'Aura avec
> `?mesure=1` l'affiche en tête du relevé (« version : f1fc823 + modifs non commitées »). Même port, écoute sur 0.0.0.0.
> **⚑ v123 : au lancement il affiche l'adresse iPhone en clair** (l'IP du Mac, relue à chaque fois) — et **il s'arrête avec le Mac**
> (extinction, fermeture de session) : à chaque session, vérifier `lsof -nP -iTCP:8752 -sTCP:LISTEN` et le relancer.
>
> - `http://127.0.0.1:8752/app.html`
> - `http://127.0.0.1:8752/promi-moodboard-H.html`
> - `http://127.0.0.1:8752/promi-nuee-toile.html`
> - iPhone, sur le même réseau : `http://192.168.1.133:8752/app.html` — ⚠ l'adresse du Mac CHANGE (.132 le 27 sept.,
>   .133 le 29) : la relire à chaque session avec `ipconfig getifaddr en0`
>   (Tom, 27 sept. 2026 : le serveur écoute sur `0.0.0.0` pour le téléphone ; sur le Mac, les outils gardent `127.0.0.1`.)
>
> **`127.0.0.1`, jamais `localhost`** — il bascule en https et échoue.
> **Le port est 8752** : c'est celui que tous les outils (`redteam_*.py`, `releve-*.py`,
> `scratchpad/cap_*.py`) portent en dur. Un serveur sur un autre port ne les sert pas.
> Vérifier d'abord qu'il ne tourne pas déjà : `lsof -nP -iTCP:8752 -sTCP:LISTEN`
> (attention, le processus s'appelle **`Python`** avec une majuscule — un `grep python`
> ne le voit pas, et on en relance un pour rien).

> **⚑ CE QUI EST VRAI AUJOURD'HUI : `ETAT-30-SEPTEMBRE-2026.md`.** (Assainissement, Tom, 30 sept. 2026.)
> Engendré depuis la source vivante par `etat_generer.py` — on corrige la source, jamais le document.
> **L'ordre des sources, en cas de doute :** `ETAT-30-SEPTEMBRE-2026.md` → `PROMI-TOKENS.json` (couleurs,
> polices) → `CONTRAT-MONDE.md` (un monde) → `SPEC-JUGES.md` (les règles que portent les juges) → ce fichier
> (méthode, pièges, décisions datées) → les moodboards (géométrie d'origine) → une mesure de l'app.
> **Une mesure prise sur l'app ne fait JAMAIS référence** — elle constate un état, elle ne le valide pas
> (c'est ainsi que le panneau du geste de la fiche est resté à 176 px / rayon 0 pendant que la page + était
> corrigée à 118 / 26).
> **`PROMI-SPECIFICATIONS.md`, `PARCOURS.md` et `MOODBOARD-VALEURS.md` sont des ARCHIVES** : ils décrivent
> août 2026 — géométrie et intention d'origine, jamais une couleur, une police ni un libellé à porter.
> Les moodboards (`promi-moodboard-H.html`, `MOODBOARD-parcours.html`, `promi-nuee-toile.html`) restent la
> référence de la GÉOMÉTRIE d'un écran ; leurs couleurs et leurs polices sont celles d'août.

> **⚑ DANS CE FICHIER, LES BLOCS DATÉS « ⚑ » EN TÊTE D'UNE SECTION CORRIGENT CE QUI LES SUIT.** Le socle des
> §3 à §6 a été repris le 30 sept. pour dire les valeurs d'aujourd'hui ; ce qui est resté d'avant porte
> la mention *(historique)*. Ce fichier nomme **« Nuée »** ce que l'app affiche **« Cercle »** (la clé interne
> reste `nuee`), et **« le Cercle »** (au sens de l'offre) ce qu'elle affiche **« Ma Parole ! »** (v106) :
> dans les blocs datés d'avant le 30 sept., lire « Nuée » = un Cercle, « le Cercle » = l'offre.

---

## 1. Ce qu'est Promi

Une application mobile française pour **tenir sa parole**. On y « plante » des
promesses — les **Promi** — qui deviennent des dalles colorées sur une **Toile**
personnelle. On tient sa parole par un **geste tracé au doigt**, pas par une case
à cocher.

Ce n'est **pas** une to-do list. Toute décision qui la rapproche d'un gestionnaire
de tâches est à rejeter, même si elle est fonctionnellement pratique.

**Public visé :** grand public, usage social et affectif. L'app doit provoquer une
émotion, pas de l'efficacité.

---

## 2. Vocabulaire — invariable

| Mot | Sens | Notes |
|---|---|---|
| **Promi** | une promesse, une dalle | invariable au pluriel : « trois Promi » |
| **dalle** | la forme colorée d'un Promi sur la Toile | synonyme de Promi |
| **Toile** | le canevas principal, Voronoï pondéré | **ne jamais modifier son code** |
| **Cercle** | un collectif de Promi (groupe, projet) — **affiché « Cercle » depuis le 30 sept. 2026 (v106)**, anciennement « Nuée » | **masculin** : « un Cercle », « le Cercle ». Clés internes inchangées (`nuee`, `NUE`, `curNuee`) — `RENOMMAGE-LEXIQUE.md` |
| **Brouillon** | un Promi non encore planté | |
| **Fil** | le flux d'activité | |
| **Aura** | l'écran de progression et d'analyse | anciennement « Karma » |
| **Studio** | le sélecteur de monde graphique | |
| **Ma Parole !** | l'abonnement payant — **anciennement « Le Cercle »** (v106) | « Avec Ma Parole ! » · « Tu es Membre Ma Parole ! » · « Retourne ta Toile » · bouton « Bon, allez d'accord ». Espace insécable avant « ! ». Clés internes inchangées (`ouvreCercle`, `.s2-cercle`, `isPremium`) |
| **Peaufiner** | le tiroir de réglages, en bas de chaque fiche | |
| **Index** | la liste complète des Promi | |
| **Pelote** | la boule de l'Aura — le sol, les îles, la fourrure | **« sphère » et « Orbite » sont morts** |
| **Folio** | ce qu'on partage quand on partage SES DALLES — la planche des dalles, une case par Promi | « Mon Folio » au partage ; **« mes dalles » reste le nom de la Toile** |
| **planter** | créer un Promi | |
| **tenir** | honorer sa parole | |

**Termes bannis** — ne jamais les employer, même en interne :
« Belle parole » comme bouton · « En replanter un » · « Dire un mot » comme gros
bouton · « tâche » · « to-do » · « objectif » · « échéance » comme libellé de champ ·
**« valider »** · **« urgent »** · **« score »** · **« brouillon »** · **« Orbite »** · **« la sphère »** (23 sept. 2026 : la boule de l'Aura s'appelle **la Pelote** ; « Orbite » est un nom fossile du système planétaire abandonné, retiré des écrans, du code et des documents).
On dit **tenir sa parole**, **tracer**, **planter**, **lancer**. Un « brouillon » est un
**gardé de côté**. (Liste complétée par Tom, 18 août 2026.)

### Un mot qui manque — on écrit le plus sobre, et on avance

**Le mot du moodboard d'abord**, toujours. Mais s'il n'existe **nulle part** — ni moodboard,
ni `PROMI-SPECIFICATIONS.md`, ni l'app — **on n'attend plus** : on écrit **le mot le plus
sobre possible, dans le lexique du produit**, on le note dans `QUESTIONS.md` avec la mention
**« à valider »**, et on continue. (Décision Tom, 18 août 2026.) Cela ne lève pas
l'interdiction d'inventer une FONCTION ni de trancher un point de produit : ça ne vaut que
pour un mot manquant.

---

## 3. Les couleurs — la règle des trois tons

Un écran de fiche porte **toujours trois couleurs distinctes** :

1. **La dalle** — sa couleur propre, issue du monde et de la palette choisis au Studio
2. **Le champ** — la couleur de la NATURE (Promi, Chiche, Cercle) — jamais l'état
3. **Le trait** — il porte l'ÉTAT (à tenir, en cours, tenu), et se juge en ΔE sur le champ

*(Repris le 30 sept. 2026 : l'ancienne formulation « le fond = l'état » est morte depuis la direction Horizon — le champ dit
la nature, la ligne dit l'état.)*

### ⚑ v139 (9 oct. 2026) — RETOURS DE TOM SUR IPHONE : LA PELOTE (CONTOUR FRANC, OMBRE, TOUCHER), LE CRÈME DES FICHES, LA PHOTO AU PINCEMENT, LES PHOTOS DANS LE DESSIN, LE +, LA MAIN QUI TRACE, RITOURNELLE. (Décisions Tom.) Ce bloc CORRIGE v136–v138 (la Pelote), v136 (le +, le corps clair des fiches) et E1 (la main, « Revoir les gestes »).
> **Q426 : les DEUX rangées aux Réglages** — « Revoir la présentation » (`#replayPres`, elle relance la présentation) et « Revoir les gestes »
> (`#replayOnb`, elle efface les drapeaux). Q427 : rien de plus. Q428 validée. **E2 n'est pas commencé.**
> **⚑ LA PELOTE (C-083). ① LE CONTOUR EST UNE LIMITE FRANCHE** : rien au-delà du rayon de la boule (116 pt, `E.R`), un seul pixel de lissage — dans la
> passe de composition (`FS2` : `t=clamp(uR0−r+0,5)`, le corps plein partout en deçà) et dans le peintre de secours (découpe en disque après
> la composition). **Le repli de couleur de v137–v138 (vis-à-vis intérieur, table `cv.__bd`) est RETIRÉ** avec la frange qu'il corrigeait.
> ⚠ **Il n'y avait pas de « dernier bord net » dans l'historique** : mesurée sur l'opacité, la frange faisait 6,25 pt en v136, 4,25 en v138 (jusqu'à
> 7,5 : des poils de longueurs différentes) ; c'est la couleur sombre des poils de profil qui la faisait paraître nette en v136 — et c'était
> le liseré. Aujourd'hui : 0,5 pt, et ΔE 0,9 à 2,3 entre le bord et l'intérieur (pas de liseré). **La silhouette fait donc 116 pt, plus 121** (Q430).
> **② L'OMBRE REVIENT, dans les deux thèmes** (`#auPeloteOmbre`, `lot-V139-OMBRE-css`) : la géométrie de v121 (104,429 × 16,245), l'encre à 0,10 en
> clair, la crème à 0,105 en sombre, à 386,224 (la place de la composition B remontée de 5 pt avec le bas de la silhouette). **C'est la SEULE
> exception de la liste blanche de `redteam_volume`** (deux dégradés, pas un de plus). Ni halo, ni liseré, ni couronne.
> **③ LE TOUCHER** : la PROFONDEUR suit `q(t) = 1 − 1/(1 + t/0,60)²` (`G.ENF_TAU`) — sa vitesse ne fait que décroître dès la première image
> (5,6 % de la butée par image à 60 i/s ; l'ancienne loi en prenait 26 à 32 % à la première), elle tend vers la butée ; la pression est `p = q^1,5`
> (`d = dmax × p^(2/3)`). Au relâcher `q` décroît en 0,60 s (`G.RETOUR_TAU` ; 0,15 avant). On rappuie au même endroit : on repart de la
> profondeur en cours. **Le comblement par la rotation AMORTIT (`× e^(−comblement / COMBLE_K)`, 0,08), il ne retranche plus** : retranché, la
> profondeur tombait à zéro d'un coup (un pas de 15 %). **La forme du contact** : `radiusX`, `radiusY`, `rotationAngle` du toucher quand
> Safari les donne (`TCH`, lus sur `touchstart` / `touchmove`), sinon `width` / `height` du pointeur ; le demi-axe vaut `DOIGT_K` (2,2) × le
> rayon du contact, borné à [0,16 ; 0,46] rayon de boule — avant, borné entre l'index et le pouce (0,26–0,40), un vrai contact tombait
> toujours sur la borne basse : deux doigts donnaient la même empreinte. `?mesure=1` écrit le contact lu (pour étalonner `DOIGT_K` sur l'iPhone).
> ⚠ Une seule empreinte à la fois : toucher AILLEURS pendant qu'un creux revient le retire d'un coup (Q432).
> Juges : **`redteam_enfonce.py`** (14 : la profondeur croît à chaque image, sa vitesse décroît, aucun pas > 8 %, butée, deux tailles de contact
> → deux empreintes, contact allongé → empreinte allongée, retour lent ; 6/14 sur l'état d'avant) ; `redteam_bord` (+ F, la limite franche,
> par les deux chemins) ; `redteam_halo` et `redteam_volume` réécrits ; `releve-aura` acquis 4 (la loi en dur).
> ⚠ **Deux pièges** : ① `destination-in` avec le `fillStyle` laissé par le peintre (transparent) EFFACE TOUT — le secours ne peignait plus rien et
> l'ancien contrôle du bord était VERT (ΔE 0,0 entre deux zones vides) : c'est le contrôle neuf de la frange qui l'a pris ; ② deux relevés
> `requestAnimationFrame` à 4 ms l'un de l'autre gonflent un « pas par image » par quatre : on réunit les relevés à moins de 12 ms.
> **⚑ LE CRÈME DES FICHES EN CLAIR (C-084)** : le corps (sous le trait) et l'encart du haut passent de `#F7F0DE` à **`#EAD9B9`** (le fond de
> l'Index, `--c-creme90-2` ; `lot-V139-CREME-css`), dans les fiches seulement. **Les cartes du fil d'un Cercle et la carte du mot, qui étaient à
> `#E9D8B7`, passent en échange à `#F7F0DE`** (la paire de la page du Fil) : sinon elles se confondaient avec le corps. Mesuré sur `#EAD9B9` :
> encre 12,56:1 · tenu `#00341A` 10,04:1 · crête 7,46:1 · **à tenir `#DD4D23` 2,93:1 (3,58 avant)** · tous les ΔE d'état > 66. La page + ne bouge pas.
> **⚑ LA PHOTO D'UNE FICHE SE CADRE AU DOIGT (C-085, `lot-V139-CADRE`)** : deux doigts zooment dans le rapport de leur écart (1:1), le point sous
> leur milieu y reste ; un doigt déplace (la photo le rattrape après 10 pt) ; z de 0,3 à 8. Le cadrage vit sur ce qui porte la photo
> (`p.photoCadre = {z, dx, dy, n}`, points de l'écran 390 ; `_phrase.photoCadre` sur la page +, il suit la photo à la plantation) et se
> sauvegarde avec la parole. **Sans geste, la photo garde sa boîte ; cadrée, elle se dessine entière** (elle peut remplir tout le haut).
> Un toucher sans glisser ouvre toujours la photo en entier ; là, **le bouton « Enregistrer la photo »** (la feuille de partage du téléphone
> quand elle prend un fichier, sinon un téléchargement). Un Cercle ne porte pas de photo. ⚠ « Le partage le respecte » : une photo n'est
> jamais dans une image partagée (v137) — rien à respecter aujourd'hui (Q434). Juge : **`redteam_cadre.py`** (22, au vrai doigt ; 8/21 avant).
> **⚑ LE DESSIN (C-086)** : ① **les tailles : plume 2 · 6 · 14, gomme 8 · 18 · 36**, et les trois points du choix à l'échelle (1 pt pour 1 pt) ;
> ② **des photos dans le dessin** : le cinquième disque de la rangée, PHOTO (`PAS_OUTIL` 58 → 46). Une photo importée est UN ÉLÉMENT DE LA LISTE,
> à son rang parmi les traits : `{img, x, y, w, h}`. PHOTO choisie, un doigt déplace la photo touchée, deux doigts changent sa taille ;
> toucher de nouveau le disque en importe d'autres ; ANNULER la retire comme un trait ; POSER la pose avec le reste (la bande et la vue
> entière la montrent). **Le partage du dessin N'EMPORTE PAS les photos importées** (v137 : « jamais une photo importée ») — `entier(d, k, true)` ;
> à trancher par Tom (Q435). Juges : **`redteam_dessin_photo.py`** (15), `redteam_dessin` (les valeurs, six outils).
> **⚑ LE + DE L'ACCUEIL FAIT 60 pt** (84 en v136 ; C-087) : 12 pt d'air jusqu'au contour de la barre, même centre, l'anneau garde ses 13,5,
> le disque fait 33, la croix 27 de large (82 % du disque, 46 % avant), à 3 pt de l'anneau.
> **⚑ LA MAIN FANTÔME TRACE (C-074, Q429)** : × 1,5 (`GRAND`), 1,6 s pour le trajet d'un trait (`TRAJET`), trois passages (`TOURS`). `montrer(id,
> cible, chemin, trace)` : `trace = {de, col, ep, pointille}` — un trait plein, opaque, qui grandit sous le doigt et s'efface quand la main
> part. Pour « tenir » et « chiche » : la seconde moitié du trait (les pointillés de la fiche deviennent pleins), à la couleur de l'état.
> ⚠ **En E1 la main s'arrêtait au milieu du trait (30 → 195) : au vrai doigt ce tracé-là ne tient PAS la parole** (mesuré : 30 → 195 et
> 195 → 360 laissent « à tenir » ; 30 → 360 et 120 → 300 tiennent). Elle va maintenant jusqu'au bout.
> **⚑ RITOURNELLE (C-088), DEUX CAUSES NOMMÉES. ① « Trop zoomée »** : dans les douze mondes « faits de leurs seules paroles » (`_NEUFS`), à une
> parole UNE cellule couvrait tout l'écran (Ritournelle et Bobinette n'y peignaient plus rien), à trois ou six les coulées débordaient.
> **Tant que la Toile compte moins de `SEMIS_NEUF_MIN` = 9 paroles et Cercles, elle garde le semis constant des autres mondes** (cellules
> vides autour, recul cadré) ; à neuf elle redevient la Toile faite de ses seules paroles (v34) — elle se ressème une fois à ce passage.
> Les aperçus du Studio gardent la règle d'origine ; le banc de rendu et le rythme (19 paroles) ne changent pas. **Ce point AMENDE v34.**
> **② « Toucher une dalle n'ouvre pas sa fiche »** : la durée du toucher (700 ms au plus) était comptée à l'heure du TRAITEMENT (`Date.now()`).
> Sous Ritournelle une image peut durer plus d'une seconde (1,15 s au banc WebKit @3x) : tombée entre l'appui et le lever, elle faisait jeter
> le toucher. On compare maintenant les heures des deux ÉVÉNEMENTS (`e.timeStamp`). Juge : `redteam_toucher` (+ trois contrôles Ritournelle :
> 1 et 3 paroles, et trois touchers avec une image de 900 ms entre l'appui et le lever — 0 sur 3 avant).
> ⚠ **La main de la page + aussi s'arrêtait au milieu : au vrai doigt 30 → 195 ne plante pas** ; elle va jusqu'au bout pour les trois natures.
> **Trouvé en composant la planche, corrigé** : sur un Chiche TENU en clair, la ligne de phrase restait crème (la couleur de la terre, v124) sur le
> corps clair de v136 — « , t’es pas chiche de » était invisible, seul le prénom (repeint par la passe de lisibilité) se lisait. Posé à la source.
> ⚠ **Un outil de capture qui ferme une fiche et en ouvre une autre dans la même tâche ne voit pas la phrase complète** (elle n'est posée qu'à la
> première) : entre `closeAll()` et `openDetail()`, une vraie pause. Ce n'est pas un défaut du produit (mesuré avec 0,9 s : toutes justes).
> **La main part quand l'écran change sous elle** (trois passages lents durent près de dix secondes : elle continuait de tracer l'ancien trajet
> sur la fiche suivante). ⚠ **`redteam_air` pose maintenant les drapeaux `geste_vu_*`** : la main et son tracé, qui paraissent et s'effacent,
> faisaient perdre jusqu'à 81 paires au relevé (le sombre, premier thème passé). Référence REFIGÉE (716 paires ; les 690 communes : aucune
> resserrée de plus d'un point ; neuves : la rangée « Revoir la présentation », et la fiche à tenir en sombre que la main cachait en E1).
> **Au registre, sans rien construire** : la façade animée (C-089, reportée à Swift) ; le prix de Ma Parole ! (C-090, décision de Tom).

### ⚑ E1 (10 oct. 2026) — LES GESTES APPRIS EN SITUATION : LA MAIN FANTÔME. (ENGAGEMENT.md E1, corrigé par A1, A2, A3 ; C-074.)
> **Fait, et arrêté là : E2 et E2bis viennent sur l'ordre de Tom.** Q421 (R6 reste rouge jusqu'à E2) et Q422 (R3 = le cadre de la Pelote ; les
> chiffres de la légende relèvent de C-036) sont tranchées.
> **⚑ UN SEUL COMPOSANT, `window.GesteFantome`** (`lot-E1-GESTES`) : `montrer(idGeste, elementCible, chemin)` · `oublier(idGeste)` ·
> `oublierTout()` · `inventaire()` · `etat()`. La main paraît après **600 ms** sans toucher sur l'écran concerné, joue le geste **deux fois
> au plus** (**900 ms** de pause), part **au premier toucher** n'importe où ; le drapeau `geste_vu_<id>` est posé **dès l'apparition** ;
> **un seul geste par passage sur un écran** (le suivant attend le prochain toucher).
> **⚑ CE QUI PRIME** : A2 — la main est **au trait plein, opaque, à l'encre du mode** (encre `#201908` sur fond crème en clair, crème sur
> seiche en sombre), **sans aucun fondu** : elle paraît et disparaît en une image ; elle porte `data-eng`. Le mouvement est écrit en
> JavaScript (un `transform` par image), jamais une transition ni une animation CSS — sinon A2 rougit. A1 — la couche `#gesteFantome` est
> posée dans `#device`, AU-DESSUS de l'écran, `pointer-events:none` : rien sur la Toile, aucune dalle ne bouge. « Réduire les animations » :
> la main immobile au départ du geste, avec une flèche du trajet.
> **⚑ L'INVENTAIRE (dans le lot, `GESTES`)** — dix BRANCHÉS : `tenir` (fiche d'un Promi pas encore tenu : le trait suit l'onde déclarée par
> `#dpTrameCv[data-trait]`) · `chiche` · `planter` (page +, onde de `_ppEcran()`) · `pelote` (Aura) · `noyau` (Partager, quand `shNoyau`) ·
> `fil` (appui maintenu sur un bandeau) · `studio-monde` puis `studio-couleur` · `bande` (photo ou dessin dans la bande) · `dessin` (surface
> vide du mode dessin). Quatre RECENSÉS, non branchés, avec leur raison : **`aura-apparait` (réservé à E2bis, ne pas le brancher avant)**,
> `pelote-folio`, `toile-pince`, `fiche-cercle-defile`. Un geste neuf = une ligne dans `GESTES` et sa mise en situation dans le juge.
> **⚑ « REVOIR LES GESTES »** : la rangée `#replayOnb` des Réglages (l'ancienne « Revoir la présentation ») efface les drapeaux `geste_vu_*`
> et **ne relance plus la présentation** — aucune autre entrée, rien au Studio. `redteam_onboarding` O19 réécrit (original en sauvegarde).
> **Juges** : **`redteam_gestes.py`** (116 contrôles : pour chaque geste branché, apparition, A2, A1, drapeau, départ d'elle-même, départ au
> toucher, absente après rechargement, de retour après le rejeu au doigt ; mouvement réduit ; sombre ; la Toile inchangée ; captures dans
> `planche-e1/` ; `--sonde` rougit A2 ; `--seul=<id>`) ; **`redteam_engagement`** : A2 est ARMÉ sur la main affichée (10/11, R6 rouge).
> ⚠ **Trois pièges du lot** : ① le Studio et le partage mettent plusieurs secondes à se bâtir : un juge qui attend 4 s y croit la main
> absente ; ② le Studio garde `.show` (§8) : « ouvrir les Réglages » depuis lui touche le Studio ; ③ **tout juge ouvre l'app sur un stockage
> neuf : la main paraît donc dans SES captures** (Aura, fiche, page +) pendant ses quatre premières secondes.

### ⚑ E0 (9 oct. 2026) — LE CHANTIER D'ENGAGEMENT : LES GARDE-FOUS. (`ENGAGEMENT.md` ; LES AMENDEMENTS A1 À A7, EN FIN DE DOCUMENT, PRIMENT.)
> **Le document est à la racine ; E0 est fait, seul (C-073). E1 n'est pas commencé.** Les lots : C-073 à C-081 ; **Délier : C-082** (C-027 ne
> porte plus que le relevé). Ordre (A7) : E0 → E1 → E2 et E2bis → E3 → **point d'arrêt** → E4 → E5 → E6A → validation de Tom → E6B.
> **Trois conventions posées en E0, à tenir dans tous les lots E** : ① tous les textes du chantier vivent dans **`window.TEXTES_ENGAGEMENT`**
> (`lot-ENGAGEMENT-TEXTES`, vide en E0), marqués `/* TEXTE PROVISOIRE — Tom */` ; ② **tout élément créé par le chantier porte `data-eng`** —
> c'est sur eux que le juge vérifie A2 (opacité 1 sur eux et leurs ancêtres, aucun fondu, aucune animation, aucun texte à demi transparent) ;
> ③ **aucun texte à l'impératif** (A3) : les textes provisoires du document qui en contiennent se réécrivent avant d'entrer dans l'objet.
> **`redteam_engagement.py` passe à la fin de CHAQUE lot E** (Chromium, serveur du projet) : R1 lexique (la liste = les termes bannis du §2 +
> badge, série, streak, niveau, classement, points, bravo, félicitations, record ; « échéance » y reste tant que l'app ne l'affiche pas —
> le juge le constate et le dit) et A3 · R2 absence et temps · R3 aucun chiffre dans le cadre de la Pelote · R4 (inactif avant E3) · R5 aucune
> clé nouvelle au stockage après trois « tenir » · R6 une sortie visible à chaque étape de l'onboarding · R7 aucun âge (« dans N jours » est un
> horizon, en liste blanche) · A2. **`--sonde` fait rougir R1, A3, R2, R3, R5, R7 et A2.** État à la naissance : 8/9 — **R6 ROUGE** (le
> prénom, la parole et le trait, le message de fin n'ont aucune sortie visible ; E2 refait l'onboarding avec « Plus tard » — Q421).
> **`redteam_verrou_onboarding.py`** : stockage vierge → l'onboarding s'affiche ; terminé par son vrai chemin ; deux rechargements → il ne
> revient pas ; 9/9 (`--sonde` retire le verrou : rouge). ⚠ Le message de fin n'accepte le toucher qu'après ses quatre secondes (v21) :
> un parcours automatique qui touche trop tôt le croit bloqué.

### ⚑ v138 (9 oct. 2026) — LE BORD DE LA PELOTE SUR LES DEUX RENDUS ; C-072 ; LE CHANTIER D'ENGAGEMENT INSCRIT. (Décisions Tom.)
> **Q416, Q417, Q418 validées** (le réglage « Mention sur un dessin partagé », sa place, la mention au-dessus du logo ; « à » et « avec »
> fusionnés dans les Chiche).
> **⚑ LE PEINTRE DE SECOURS (SANS WEBGL 2) A LA MÊME CORRECTION DU BORD (C-002)** — « pour que les deux rendus soient identiques ». Après sa
> composition, une passe remplace, au-delà de 0,90 R, la couleur de chaque pixel par celle de son vis-à-vis intérieur (même loi que `FS2` :
> repli autour de 0,92 R, fondu 0,90 → 0,93 R, opacité gardée) ; la table (cible, source, poids) est calculée une fois par taille (`cv.__bd`) ;
> le masque du corps plein va jusqu'à R (0,972 avant). **`redteam_bord` passe par les DEUX chemins** (`--gl`, `--secours` ; le secours est
> forcé par `window._peloteGL=false`, et le juge vérifie quel chemin a peint) : 16/16 ; le secours rougit sur l'état d'avant (6/8).
> **⚑ C-072 — « LE LANCER NE COMBLE PAS » FLOTTAIT À CAUSE DU JUGE.** La fin du creux était lue par `attends` (une question à la page toutes
> les 100 ms, depuis Python) puis par un second aller-retour : 0,4 à 0,7 s mesurées à ± 0,1 s, avec le même retard ajouté aux deux durées —
> le rapport remontait vers son seuil. La fin se lit maintenant DANS la page, à l'image près, trois passes, médiane (53 %, 57 %, 45 % sur
> trois relevés). **Le seuil (60 %) n'est pas touché, le produit non plus.** C'est le §8 : un instrument dont la cadence ne dépend pas de ce
> qu'il mesure ne mesure rien.
> **⚑ LE CHANTIER D'ENGAGEMENT EST AU REGISTRE (C-073 à C-081 : E0, E1, E2, E2bis, E3, E4, E5, E6A, E6B) avec les amendements A1 à A7 du chef
> de chantier, qui PRIMENT sur ENGAGEMENT.md.** À ne jamais reperdre : A1 — ni onde sur les dalles voisines ni menthe de célébration en E3 ;
> A2 — aucune transparence ni fondu (main fantôme au trait plein, phrase d'accueil opaque) ; A3 — aucun texte à l'impératif ; A4 — la liste
> interdite de R1 = le lexique du §2 ; A5 — fil par personne sans épaisseur cumulée ; A6 — E2bis, l'interface se dévoile ; A7 — l'ordre, et
> le point d'arrêt après E3. ⚠ **E0 N'EST PAS EXÉCUTÉ : `ENGAGEMENT.md` n'est pas arrivé** (Q420) ; rien n'a été inventé à sa place.

### ⚑ v137 (8 oct. 2026) — PLUS AUCUN EFFET AUTOUR DE LA PELOTE ; LES CHICHE ; LE PARTAGE DU DESSIN. (Décisions Tom.) Ce bloc CORRIGE v136, et v114 à v126 pour la Pelote.
> **⚑ DÉCISION DE TOM, 8 OCT. 2026 : PLUS AUCUN EFFET AUTOUR DE LA PELOTE.** Ni halo, ni ombre, ni couronne, ni flaque, ni liseré. **Le halo et
> l'ombre de la Pelote SORTENT de la liste blanche des exceptions : il ne reste que le flou des murs de Ma Parole !.** « La Pelote est le seul
> volume » (v114) est MORT : `redteam_volume` a une liste blanche VIDE (réécrit), le peintre du halo, sa trame et les règles `.au-halo`,
> `.au-ombre`, `.au-flaque` sont RETIRÉS du code.
> **⚑ LE LISERÉ DU BORD PART (C-002).** Cause : au bord les poils sont vus de profil et s'empilent, le poil y couvre le corps ; et le corps
> s'effaçait de 0,972 à 1,012 R, une frange à demi transparente qui prenait la couleur de la page. Parade, dans la passe de composition de
> la carte graphique (`FS2`) : **au-delà de 0,92 R la COULEUR d'un pixel est celle de son vis-à-vis à l'intérieur** (même angle, rayon replié
> autour de 0,92 R), fondu de 0,90 à 0,93 R ; **le corps reste plein jusqu'à R** et finit au même endroit (1,012 R) — la silhouette ne bouge
> pas (`redteam_contour`, `redteam_plein` verts). Juge : **`redteam_bord.py`** (ΔE CIELAB médian par secteur entre la bande 111,3–115,6 pt
> et l'intérieur 101,6–108,9 pt, ≤ 5 en dur ; quatre palettes × deux thèmes × trois ouvertures : 0,2 à 0,6 ; 3/8 sur l'état d'avant).
> ⚠ **Trois faits de mesure** : ① la silhouette fait 121 pt, la BOULE 116 (`E.R`) — « les derniers 8 % » se comptent sur la boule ; ② dans
> la part déjà opaque (106–112 pt) il n'y avait AUCUN liseré avant (ΔE 0,5) : il vivait tout entier dans la frange ; ③ le peintre de
> secours (sans WebGL 2) garde l'ancien bord (Q419).
> **⚑ LES CHICHE PRENNENT L'EXPRESSION COURANTE (Q412 ; les formes nommées des Promi sont VALIDÉES)** : à soi « T’es pas chiche de » · lancé
> « Marion, t’es pas chiche de » · à plusieurs « Marion et Rachel, vous êtes pas chiches de » (« … + x personnes » au-delà de trois) · reçu
> « Marion me dit : t’es pas chiche de ». « À » et « avec » font une seule liste de personnes interpellées (Q417). `redteam_phrase_fiche` 74.
> Mesuré à l'encre, sans rien changer : la phrase complète ne resserre pas l'air (phrase → titre 5,5 pt avant comme après ; 5,3 sur deux lignes).
> **⚑ LE PARTAGE DU DESSIN (C-068).** « Seul un dessin se partage, jamais une photo importée. L'image partagée porte par défaut la mention de la
> nature et le logo en bas à gauche. Un réglage, dans les Réglages, masque la mention. Le logo est toujours là. Un dessin masqué pour soi
> n'est jamais partagé. » Le rond Partager d'une fiche (Promi, Chiche, Cercle) dont le dessin est posé et non masqué partage LE DESSIN,
> entier, rendu de ses traits (`window._dessinPartage`, peint en tête de `sharePlanche`) : son fond, puis en bas à gauche le logo « Promi »
> (PromiLate) et, au-dessus, la mention (Gilbert, capitales), à l'encre ou à la crème selon le fond ; ni mot-marque du haut ni QR
> (`#shareScreen.sh-dessin`, `window._shDessinSeul`). Le réglage : rangée `#setMention` du groupe « Partager » des Réglages
> (`lot-V137-MENTION`, `promi_dessin_mention` : '0' = masquée) — elle lit le GESTE (aux Réglages un toucher ne produit pas toujours de
> `click`, mesuré en WebKit). Sans dessin, ou masqué : Mon Folio réduit, la case rend la DALLE — une photo n'y est jamais (elle ne vit
> que dans la bande de la fiche). Juge : **`redteam_partage_dessin.py`** (34 ; 8/34 avant). Mots à valider : Q416, Q418.
> **Q414** : Ramage, Mascaret, Chamade et Volubilis restent hors de l'ampleur ; rien n'est refigé. **C-011** : Tom vérifie, parade gardée.

### ⚑ v136 (7 oct. 2026) — LA FICHE TENUE EN CLAIR ; LA PHRASE COMPLÈTE ; LE PLEIN ÉCRAN DÈS LA PAGE + ; LE + ; L'AMPLEUR. (Décisions Tom.) Ce bloc CORRIGE v135, v124 (Q269) et v8 là où ils disent autre chose.
> **⚑ EN CLAIR, LE CORPS D'UNE FICHE TENUE (PROMI ET CHICHE) EST LA CRÈME `#F7F0DE`, comme toutes les fiches en clair (C-059). LA TERRE `#2B1020`
> NE VAUT PLUS QU'EN SOMBRE.** En clair la crête verte dit « tenu » et **la mention TENU est au vert d'état `#00341A`** (l'amande est illisible
> sur la crème) ; l'encre reste l'encre. Où ça vit : `lot-V7-CORPS-TENU` (tout le bloc sous `:not(.light)`), le poseur de la fiche (`encre`,
> `_colQd`), `_surTerre()`. Mesuré sur la crème (ΔE CIELAB, seuil 15) : crête `#0B4A2A` 73,1 · arc tenu 80,3 · arc en cours 93,5 · arc à
> tenir 81,7 ; la mention `#00341A` : 12,27:1. « Sur la terre, le tenu est l'amande, en clair aussi » (Q269, v124) est donc MORT en clair.
> **⚑ LA PHRASE COMPLÈTE DANS LES FICHES PROMI ET CHICHE (C-069, `lot-V136-PHRASE`, `window._phraseFiche`)** — dans les fiches seulement,
> jamais dans le Fil ni l'Index, jamais sur un Cercle. La ligne « À moi » / « À Rachel » disparaît : `#dptQui` porte le reste de la phrase,
> **le titre reste seul dans `#dptTitre`, le plus grand texte de la fiche**. Les formes sont celles de la page + : « Je me promets de » ·
> « Je promets à Rachel de » · « Je promets à Rachel, Marion et Nico de » · au-delà de TROIS « Je promets à Rachel, Marion + 4 personnes de »
> (toucher « + x personnes » déroule la liste, la phrase s'allonge, le titre descend) · reçue « Rachel me promet de » · demandée « Rachel,
> promets-moi de » / « promettez-moi de » · Chiche « À Marion · avec Rachel · chiche de » · « Chiche de » · reçu « Marion me lance : chiche
> de » (mot manquant, à valider — Q412). « de » s'élide (« d'aller »). ⚠ Tom citait « Je te promets de… », « Je vous promets de… » : ces
> formes ne nomment personne — j'ai pris celles de la page +, qui nomment (Q412). Juge : **`redteam_phrase_fiche.py`** (56 ; 36/56 avant).
> **⚑ LE PLEIN ÉCRAN DÈS LA PAGE + (C-067)** : toucher le dessin ou la photo dans la bande de la page + l'affiche en entier, un second
> toucher rend la page telle quelle. ⚠ Sur la page +, c'est `#promiForm` qui est sous le doigt dans la bande. `redteam_entier` 44 (38 avant).
> **⚑ LE + DE L'ACCUEIL FAIT 84 pt** (68 avant, × 1,235 ; C-070), centré au même point : il occupe la hauteur intérieure de la barre.
> **Son anneau n'a plus de filet** (il l'avait gardé en v135).
> **⚑ AUTOUR DE LA PELOTE IL N'Y A PLUS RIEN — NI HALO NI OMBRE (C-002, C-071). Ce point CORRIGE v114 à v126 (halo, ombre, flaque).**
> Tom, 7 oct. : « Les contours ça fait flou, pas net ; le halo c'est une mauvaise idée en fait. […] Enlève tout ce qu'il y a comme effet
> autour de la Pelote pour le moment, ne masque pas, supprime. » `#auPeloteHalo` et `#auPeloteOmbre` **ne sont plus créés** ; la colonne de
> l'Aura garde les cotes B (la place de l'ombre reste vide). ⚠ Le code du peintre du halo (`halo()`, `window._haloPelote`) et les règles
> `.au-halo` / `.au-ombre` restent dans le fichier, MORTS : plus rien ne les appelle. **« La Pelote est le seul volume » (v114) reste la
> règle de `redteam_volume` : rien d'autre ne reçoit de halo ni d'ombre — elle non plus, pour le moment.** Les « points subtils, épars »
> que Tom évoquait ne sont PAS construits (ce serait une seconde exception à la loi des points, §5) : C-071 reste ouvert.
> Ce qui avait été isolé avant : halo, ombre, UN canevas de carte graphique — aucune couche en double. Reste, mesuré et non touché :
> LE LISERÉ DU BORD (sur les 8 derniers pour cent du rayon la fourrure prend une autre couleur que l'intérieur, ΔE 15 à 31,
> `scratchpad/v136/limbe.py`) — c'est le poil lui-même ; un essai (fondre le corps vers le poil au bord) n'a rien changé : RETIRÉ (Q413).
> Juges réécrits : **`redteam_halo`** (10 contrôles : aucun nœud, l'anneau 125–150 pt et la place de l'ombre sont le fond de la page au
> niveau près ; 2/10 sur l'état d'avant), `releve-aura` (plus de cote d'ombre), `redteam_corps` 5 (aucun halo).
> **⚑ L'AMPLEUR À MI-FORCE (C-062) : Esquille 0,3 · Ritournelle 0,3 · Halin 0,3 · Brouillamini 1,5 · Bobinette 0,3.** « Une arrivée de dalle
> jusqu'à 15 % plus longue est acceptée » : Halin +13 %, Brouillamini +13 %, les trois autres 0 % (`redteam_rythme`, ± 15 % à l'arrivée
> pour eux). Dehors : Guingois (+35 %), Chantourné (+38 %) ; Mascaret, Chamade, Volubilis (banc de rendu, accord de Tom attendu) ; **Ramage
> (C-066)**. L'ampleur se lit sur le monde CHOISI (`_ampMonde`), et d'un monde neuf à l'autre la Toile se ressème si l'ampleur est en jeu.
> **⚑ C-066 — L'ÉCART DE GUINGOIS AU BANC VENAIT DE L'AMPLEUR DE RAMAGE (v135).** Ce fichier disait « depuis avant ce lot » : c'était FAUX
> (mesure prise sur une référence salie). Prouvé en retirant Ramage seul : Guingois revient au pixel. Le mécanisme n'est pas nommé ;
> Ramage est retiré de l'ampleur. `banc_rendu` : 280/280 au pixel.
> **⚑ LA GRILLE ANTI-COERCITION DE TOM EST EN TÊTE DU §12** (six questions, six risques cumulés).
> ⚠ **NON FAIT : le partage du dessin (C-068)** — mention de la nature, logo, réglage, photo jamais partagée : rien n'est construit.

### ⚑ v135 (6 oct. 2026) — PLUS AUCUN FILET ; LE SYMBOLE DU BOUTON PHOTO ; LES CONTRADICTIONS TRANCHÉES ; L'AMPLEUR À MI-FORCE. (Décisions Tom.) Ce bloc CORRIGE v114 (le filet de la terre), v133, v134 et le §3 là où ils disent autre chose.
> **« La vérité est ce que Tom voit à l'écran. »** Quatre contradictions tranchées : **la Pelote fait un tour en 100 s** (`2π/100`, comme
> l'app et `releve-aura` ; ce fichier écrivait 120) ; **le fond sombre est la seiche `#050302`** dans le rôle `fond` des jetons (JSON, CSS,
> Swift — ils portaient encore `#100D0B`) ; **un design se vend 2 €** (l'écran de l'offre disait « 1 €, ou 4 pour 3 € » : « 4 pour 3 € »
> est RETIRÉ, Tom ne l'a pas redécidé) ; **l'aide de l'Aura et « À propos » disent l'app d'aujourd'hui** (« la plus récente en premier » ;
> « Les sous-titres et les libellés sont en Gilbert », « Les titres, eux, sont en PromiLate. »).
> **⚑ PLUS AUCUN FILET, NULLE PART (C-059).** « Retire le filet autour des disques et des Noyaux, et celui sous le trait et la crête, en clair
> comme en sombre. L'exception de v114 tombe. » `window._sansFilet` rend toujours vrai. Mesuré sans filet (ΔE CIELAB, seuil 15 de
> `redteam_tonsurton`) : sur la terre `#2B1020`, crête `#0B4A2A` 51,3 (Δlum 35,4) · arc tenu `#00341A` 44,6 (Δlum 16,2) · **arc en cours
> `#291547` 24,0 (Δlum 6,0)** — le plus faible, au-dessus du seuil ; sur la seiche, 31,8 à 40,7. `redteam_filets` : liste blanche VIDE.
> ⚠ **Le fond d'un Promi tenu n'a PAS changé** : Promi et Chiche tenus sont déjà identiques (terre, deux thèmes) ; un Cercle n'a pas
> d'état « tenu » (corps ordinaire). « Ce n'est pas le bon fond » attend de savoir lequel (Q407).
> **⚑ LE BOUTON PHOTO PORTE LE CADRE TRAVERSÉ D'UN TRAIT (C-060, choix C)** — fiche, page +, fiche d'un Cercle, deux thèmes ; VoiceOver
> inchangé. (L'appareil de l'avatar, aux Réglages, reste : il parle bien d'une photo.)
> **⚑ SUR `#0E78F2`, LES LIBELLÉS LILAS DU PEAUFINER D'UNE FICHE PROMI SONT `#F4EEFF`** comme la phrase de la page + (Q403 tranchée) —
> mesurés à l'écran : `#C4A2F5` y faisait 1,97:1. « Ma Parole ! » y reste `#FED0C3` (Tom juge sur l'iPhone).
> **⚑ LA PAGINATION DES MONDES AU STUDIO EST UNE RANGÉE DE BARRETTES** (10 × 4, la courante 18 × 4), plus des points : la loi des points.
> **⚑ LE MENU DES PALETTES « VIDE » (C-011) — LA CAUSE N'EST PAS NOMMÉE.** La capture de Tom (reçue en cours de lot) montre les 24 pastilles
> réduites à des points, le nom sans son style, la jauge sans hauteur : dans le panneau, les règles de BASE (`.st3-p`, `.st3-orb`, `.st3-q`,
> `.st3-pn`, `.st3-spec`) n'avaient pas pris. Non reproduit (WebKit et Chromium, trois tailles de fenêtre, vingt mondes, gratuit et payé,
> trois ouvertures). **Parade** : `#studioScreen #stpPals` porte en propre tout ce dont une pastille, le nom et la jauge ont besoin.
> `redteam_palettes` (58) compte les teintes PEINTES de chaque pastille sur la capture (`--sonde=vide` : il rougit).
> **⚑ L'AMPLEUR À MI-FORCE, SOUS TROIS MONDES SEULEMENT (C-062)** — `_AMP_MI` dans le moteur : à l'ampleur stable de chaque parole (titre et
> personne) s'ajoute `force × (−0,07 + 0,40·u⁴)` : **Esquille 0,3 · Ritournelle 0,3 · Ramage 0,6**. Elle se recalcule au changement de monde.
> Tom en demandait dix. **Sept sont RETIRÉS, avec leur raison mesurée** : Halin, Guingois, Chantourné, Brouillamini — elle allongeait
> l'arrivée d'une dalle de 11 à 38 % (`redteam_rythme` : le rythme validé ne dérive pas) ; Mascaret, Chamade, Volubilis — sous elle le banc
> de rendu ne retrouvait plus sa référence (mondes déclarés « instables »), et Volubilis n'y répond pas (ses formes ont leur taille propre).
> Arbitrage de Tom : Q411. La taille ne porte toujours aucun sens. `banc_rendu` est refigé pour ces trois mondes, et eux seuls.
> ⚠ **`banc_rendu` : Guingois diffère de la référence DEPUIS AVANT ce lot** (vu avec le moteur de v134 ; le banc n'avait pas tourné depuis
> v130) ; Chantourné aussi quand on le passe seul ; Volubilis ne se répète pas d'une passe à l'autre — non refigés, ouverts (C-066).
> **⚑ LA GRILLE ANTI-COERCITION EST AU §12** (reconstituée ; les six critères et les six risques de Tom manquent — Q406).
> Juge neuf : **`redteam_lexique.py`** — termes bannis (liste du §2, en dur) et loi des points, à l'écran, 34 écrans × 2 thèmes × gratuit et
> Ma Parole ! ; dette nommée `lexique-dette.json` (la pastille du Fil `#filDot`, les pastilles de la légende de l'Aura) ; deux sondes.

### ⚑ v134 (6 oct. 2026) — LE CORPS SOMBRE D'UN PROMI EST `#0E78F2`, DÉFINITIF. (Décision Tom.) Ce bloc CORRIGE ce que les blocs v133, v131 et v130 disent de ce bleu.
> **« Tom a choisi #0E78F2, en connaissance de cause. »** Fiche Promi et page + d'un Promi, en sombre (jetons `--c-cobalt50`, `--p-corps-promi` ;
> JSON = CSS = Swift). **`?bleu=` est RETIRÉ.** `#1A52F0`, `#273CEB`, `#8ACBE8`, `#335382` sont morts pour ce rôle.
> **⚑ EXCEPTION NOMMÉE, décidée par Tom : le texte posé sur ce corps reste crème `#F7F0DE` — 3,70:1. Les petites mentions y sont sous
> 4,5:1, par décision.** Aucun juge ne doit « corriger » ce texte, aucune passe de lisibilité ne doit le repeindre.
> **Les deux dérivés suivent ce bleu, même teinte, éclaircis jusqu'à leur seuil** (méthode du v133, validée) : **« Ma Parole ! » = `#FED0C3`**
> (l'orange `#FB4C0D`, OKLCH h 36°, à 3,01:1 ; il ne garde qu'un quart de sa chroma) ; **la phrase lilas de la page + = `#F4EEFF`**.
> ⚠ **4,5:1 EST HORS D'ATTEINTE sur ce bleu en éclaircissant : le blanc pur n'y fait que 4,21:1.** La phrase lilas est portée au niveau
> de la crème (3,71:1), teinte gardée (h 302°) — Q403, à valider. ⚠ `window._teinte.ajuste` ASSOMBRIT dès que le fond dépasse 0,18 de
> luminance (ce bleu : 0,20) : appelée telle quelle elle rendait `#621600` et `#1C0035`. Les deux valeurs sont donc des jetons, calculées
> hors de l'app (`scratchpad/v134/bleu.py` : OKLCH, clarté montée, chroma réduite quand la couleur sort du gamut).
> **Les états sur ce corps, mesurés, rien retouché** (ΔE CIELAB · Δlum · contraste) : **à tenir `#DD4D23` 126,2 · 1,7 · 1,03:1** — le trait
> orange a la CLARTÉ du corps, c'est sa teinte seule qui le sépare (Q216 : un trait se juge en ΔE, seuil 15) ; en cours `#291547` 56,8 ·
> 77,4 · 3,86:1 ; tenu `#00341A` 97,2 · 67,2 · 3,31:1 ; trait Promi `#022140` 62,4 · 3,85:1 ; bande `#82AEF8` contre corps 36,1 · 1,88:1.
> **Le dossier de portage est écrit : `portage/`** (dix documents, C-021) — lecture et extraction, aucun changement du produit.

### ⚑ v133 (6 oct. 2026) — LES DIX-HUIT PHRASES DES MURS ; LE BLEU PROVISOIRE ; LE MODE DESSIN RÉGLÉ ; LE MENU DES PALETTES. (Décisions Tom.) Ce bloc CORRIGE les blocs v131 et v132 qui le suivent.
> **⚑ LES PHRASES DES MURS DE MA PAROLE ! SONT DIX-HUIT, RÉÉCRITES PAR TOM (C-063)** — mot pour mot, dans l'ordre, même rotation (v104). Elles
> vivent dans `lot-V104-MURS` (`TEXTES` : la phrase, puis SES mots en orange, cherchés dans l'ordre). **Dans chaque phrase, seuls les mots
> listés prennent l'orange de Ma Parole ! ; « ! » n'apparaît que dans « Ma Parole ! ».** `redteam_murs` (28) et `redteam_maparole` (14) portent
> le texte et les mots EN DUR. Les 21 phrases d'avant : `MA-PAROLE-PHRASES.md` (histoire).
> **⚑ LE CORPS SOMBRE D'UN PROMI EST PROVISOIREMENT `#1A52F0`** (C-050 : « sur son iPhone, #273CEB tire nettement au violet »). **`?bleu=1…5`**
> (`lot-V133-BLEU`) le pose en direct : 1 `#1560E8` · 2 `#1A52F0` · 3 `#2046F2` · 4 `#273CEB` · 5 `#0A5CF5` ; la valeur s'écrit au bas de
> l'écran ; Tom choisit, puis on fige et on RETIRE le paramètre. « Ma Parole ! » sur ce corps (3:1) et la phrase lilas de la page + (4,5:1)
> en sont DÉRIVÉES par `_teinte.ajuste` (au défaut : `#FF9F84`, `#E8DAFF`). Le mur lit le bleu par `window._bleuPromi()`.
> **⚑ LE MODE DESSIN (C-042, C-056, C-061)** — ① **un ✕ dans le contour de l'encart, à l'emplacement de « ✕ FERMER », sort sans poser** ; le
> dessin en cours est gardé ; « Quitter le dessin » ; c'est le seul nœud admis sur la surface. ② `ECART_DEPLOI` **16** ; **la rangée est
> centrée dans sa zone basse** : `MARGE_HAUT` 12 = `MARGE_BAS` 12, comptés jusqu'au bord bas utile (`SECU_BAS` 34) — la surface fait
> **390 × 742**. ③ **Les couleurs du dessin sont dans Ma Parole !** : sans elle, l'encre du mode sur le champ de la nature ; le panneau COULEUR
> est un MUR (`.dz-mur`, flou 4,8 px, rien ne s'y choisit, la phrase monte dessus, devant le mode — `#murPhrase.sur-dessin`) ; l'offre qui
> s'ouvre fait sortir du mode (dessin gardé). `redteam_dessin` 79, huit sondes.
> **⚑ LE MENU DES PALETTES DU STUDIO (C-057) — la cause** : `#studioScreen` ne perd jamais `.show` (§8) ; à chaque ouverture `buildStudio`
> rebâtit la rangée, le NOM (`#st3pn`) et la jauge, et `posePals` ne retirait du panneau que l'ancienne rangée et l'ancienne jauge : deux
> noms, et la rangée neuve rangée APRÈS le vieux. Il retire maintenant les trois et les repose dans l'ordre grille · nom · jauge.
> **Primesautier est la première pastille** (l'ordre des autres inchangé). Juge : **`redteam_palettes.py`** (deux thèmes, deux ouvertures,
> les 24 pastilles touchées une à une ; 22/32 sur l'état d'avant).
> **« Importer une image » devient « Importer une photo »** (C-060 ; le symbole du bouton attend le choix de Tom, `planche-v133/symboles`).
> ⚠ **OUVERTS** : la Toile sourde au doigt sous certains mondes n'est PAS reproduite (C-058, `redteam_toucher` 21/21, Q396) ; « le bas des
> fiches en clair » n'a rien changé — les trois corps sont déjà identiques en clair, aucun filet n'y est peint (C-059, Q397) ; la
> diversité des tailles : le coefficient de variation ne baisse pas avec le nombre de dalles (C-062, Q402).

### ⚑ v132 (5 oct. 2026) — LE DESSIN EST CONSTRUIT DANS L'APP. (Décisions Tom.) Ce bloc CORRIGE ce que les blocs v127 à v131 disent de l'outil de dessin.
> **« On ne fait plus de planche : on construit, et Tom juge au doigt sur iPhone. »** Choix : **effilé E2, symbole de couleur S2** (celui du
> Studio). **Les planches v130 et v131 sont ABANDONNÉES** (elles laissaient la surface coincée en haut et un vide dessous).
> **⚑ LA MISE EN PAGE DU MODE DESSIN** (`lot-V132-DESSIN`, fiches Promi, Chiche, Cercle et page +) : **la surface de dessin prend toute la
> place, du haut de l'écran jusqu'à la rangée d'outils ; la rangée A (PLUME · GOMME · ANNULER · COULEUR · POSER) est EN BAS, à portée de
> pouce ; tailles et couleurs se déploient juste AU-DESSUS d'elle et se replient dès le choix fait ; tout le reste de la fiche se retire ;
> l'encart du haut ne garde que son contour au trait fin ; tout revient à POSER ou à la sortie, sans fondu.** Le mode est une couche PLEINE
> posée dans `#device` : la fiche dessous n'est pas touchée (le retour est exact par construction). **Les paramètres sont en tête du lot**
> (`window._dessinParams` : `RANGEE_H` 44 · `MARGE_BAS` 34 · `MARGE_HAUT` 12 · `MARGE_COTE` 24 · `PAS_OUTIL` 58 · `POSER_L` 104 ·
> `ECART_DEPLOI` 8 · `TAILLES` 2,5 / 4,5 / 8 · `TAILLES_GOMME` 10 / 18 / 30 · `BANDE_RETRAIT` 7). La surface fait 390 × 754 pt.
> **⚑ UN DESSIN EST UNE LISTE DE TRAITS, JAMAIS UNE IMAGE** : `{fond, traits:[{c, t, g, pts}], poses, pose, masque}` — sur la parole
> (`p.dessin`, sauvegardé avec elle), sur le brouillon de la page + (`_phrase.dessin`, il suit la parole ou le Cercle à la plantation), ou par
> Cercle (`localStorage promi_dessins_cercle`). **Chaque trait garde SA couleur** (un hex) : un changement de palette ne touche que les traits
> à venir. `traits` = le dessin en cours (gardé si l'on sort) ; `poses` = ce que POSER a posé (la bande, la vue entière et le partage ne
> montrent que lui). **Après le premier POSER, le fond est fixé (plus d'onglet FOND) et les nouveaux traits ne prennent que les couleurs
> déjà présentes.** Le trait : plein, opaque, contours nets, effilé E2 (début +38 %, fin effilée sur le dernier quart), plus fin quand le
> geste est rapide (jusqu'à −28 %), la pression d'un stylet module la largeur, jamais sous 1 pt.
> **⚑ LE DESSIN REMPLACE LA DALLE OU LA PHOTO DANS LA BANDE** : une couche pleine (`canvas.dz-bande` : le fond du dessin puis ses traits, à
> l'échelle 1, calés EN HAUT) posée sur la bande, découpée à 7 pt au-dessus de l'axe du trait d'état. Le dessin est plus grand que la
> bande : la fiche en montre le haut ; **toucher la bande l'ouvre en entier (C-051, « Voir le dessin en entier »)**. Rien n'est relu ni
> retouché dans le canevas de la bande : « Retirer le dessin » rend la dalle. **Le masquage** (`button.dz-oeil`, coin bas gauche de la
> bande) est pour soi seul, mémorisé par fiche ; **un dessin masqué n'est jamais emporté dans un partage** (`window._dessinCase`, lu par la
> case du Folio). **Les entrées** : « Dessiner » en tête du menu du bouton photo, devenu COMPACT (33 pt, 4 pt entre deux, posé À GAUCHE du
> bouton) — sur la fiche, sur la page + (Promi, Chiche, Cercle : le bouton y ouvre le menu, plus l'import direct) et sur la fiche d'un
> Cercle, qui reçoit son bouton photo. La loi des points : seul le choix de taille (trois points) y échappe (§5).
> ⚠ **Trois pièges payés** : ① une couche ajoutée à `#detailPoster` sort en `display:none` (le crible) — on la déclare visible nommément ;
> ② `_dalleReelle` (dans `sharePlanche`) est du code MORT : la case du Folio passe par `_poseDalle` ; ③ le menu posé au-dessus du bouton
> passait sous le plateau dès quatre lignes.
> ⚠ **OUVERT** : il n'y a pas de bouton de SORTIE sans poser (Échap et la fermeture générale sortent en gardant le dessin en cours) — Q392.
> Juge : **`redteam_dessin.py`** (63 contrôles : couleurs figées sous trois palettes, masquage et partage, aucune superposition, retour exact
> après POSER, joignabilité et VoiceOver, les entrées) ; **cinq sondes** (`--sonde=couleurs|partage|superpose|retour|joignable`) fabriquent
> la version fautive, il y rougit à chaque fois. **C'est un geste : la validation de Tom sur iPhone est obligatoire.**
> **⚑ « CE QUE TU AS TENU » : LA PLUS RÉCENTE EN PREMIER** (corrige v131) — la parole qu'on vient de tenir se voit sans défiler.
> **⚑ SUR LE COBALT** : la phrase lilas de la page + d'un Promi (sombre) est **`#DAC3FF`** (`--c-lilas85`, la teinte de `#C4A2F5` éclaircie à
> 4,51:1 ; le jeton `--c-mauve75` y est remplacé, sur cet écran seulement) ; **« SUPPRIMER CE PROMI » est crème en sombre, encre en clair —
> `#DD4D23` est une couleur d'état et ne sert à rien d'autre** (C-015 reste ouvert pour les Réglages).

### ⚑ v131 (5 oct. 2026) — LE COBALT REMPLACE TROPICAL BREEZE ; LA LISTE DE L'AURA EST COMPLÈTE ; VOIR UNE PHOTO EN ENTIER. (Décisions Tom.) Ce bloc CORRIGE le bloc v130 qui le suit.
> **⚑ LE CORPS SOMBRE D'UN PROMI EST LE COBALT ÉLECTRIQUE `#273CEB`** (jeton `--c-cobalt50` ; fiche Promi et page + d'un Promi, en sombre).
> **Tropical Breeze `#8ACBE8` est ÉCARTÉ** (« trop proche du bleu du champ »). **Le texte posé dessus redevient crème `#F7F0DE`** (6,30:1) :
> plus rien ne déclare un corps pastel, la passe `lot-V130-TROPICAL` est COUPÉE (ses portes restent, inertes). Mesuré : états contre le corps
> (ΔE CIELAB, seuil 15) — à tenir 141,9 · en cours `#291547` 72,9 · tenu 128,8 · trait Promi `#022140` 87,2 ; bande `#82AEF8` contre corps
> ΔE 76,3. **« Ma Parole ! » sur ce corps : `#FF8664`** (`--c-orange-maparole-cobalt`, la teinte OKLCH de `#FB4C0D`, h 36°, éclaircie jusqu'à
> 3,02:1 — `#FF7A55` n'y fait que 2,79:1) ; Chiche et Cercle gardent `#FF7A55`. La phrase lit le premier fond opaque sous le mur
> (`.sur-cobalt`). `redteam_maparole` porte les TROIS valeurs, `redteam_murs` 26/26. ⚠ Non retouché, mesuré : la phrase de la page + (lilas
> `#C4A2F5`) fait 3,35:1 sur le cobalt (3,85:1 sur l'ancien `#335382`) ; « SUPPRIMER CE PROMI » en `#DD4D23` y fait 1,76:1.
> **⚑ « CE QUE TU AS TENU » MONTRE TOUTES LES PAROLES TENUES, dans l'ordre chronologique, l'Aura défilant (C-052 — remplace Q187 : trois
> dalles, six dès cinq tenues).** La parole qu'on vient de tenir est la DERNIÈRE. `redteam_reactif` 31 contrôles (réécrit).
> **⚑ VOIR UNE PHOTO EN ENTIER (C-051, `lot-V131-ENTIER`).** Toucher la bande d'une fiche quand elle porte une PHOTO (jamais la dalle) l'ouvre
> en entier, par-dessus tout l'appareil, sur un fond PLEIN — la seiche, sans transparence, ni ombre, ni fondu ; l'image entière (`contain`) :
> on y voit ce que la bande recadrait. Un nouveau toucher, ✕ ou `closeAll` referme. La bande s'annonce « Voir la photo en entier » (rôle de
> commande) seulement quand elle porte une photo. Le dessin viendra avec l'outil (`source()`). **Trois faits à ne pas reperdre** : ① c'est
> `#dpMain` (la colonne) qu'on touche dans la bande, pas le canevas ; ② « dans la bande » se lit sur ce qui est PEINT (le canevas est opaque
> jusqu'à l'onde) ; ③ **« la fiche est intacte » se juge sur le RENDU** (place, couleur, police, texte de chaque nœud) : l'attribut `style`
> est réécrit par les passes de l'app à chaque toucher, la racine retire au sort `gsN` et `--ghost-ink`, l'invite du geste respire.
> Juge : **`redteam_entier.py`** (36 contrôles, au vrai doigt ; 16/36 sur v130).
> **⚑ C-048 — LA « DALLE À 3,11 % » ÉTAIT DU JUGE.** Reproduite en boucle (cinquante passages sur la copie de v130) : chaque prise est une
> dalle rendue avec une RAMPE (`opts.rampe`, Q30) — l'ombre des carreaux prend le ton sombre de la rampe, à plus de 48 du ton dominant. Ce
> sont ses couleurs. `redteam_decoupe` G2 ne compte plus une couleur qui tombe sur la rampe déclarée.
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — la mise en page corrigée par Tom** : **Promi et Chiche, tout reste à sa place** —
> les trois lignes ne descendent pas ; seule la rangée bouge, à **16 pt sous le trait** ; tailles et couleurs se déploient sous elle (le
> panneau des couleurs est compacté à 114 pt pour finir au-dessus de « À Rachel » : 383 → 497, le texte à 503). **Cercle : rien ne
> disparaît**, tout descend d'un bloc (166 pt sur la planche) et passe sous le bandeau Peaufiner, comme en défilant. Toujours aucun outil
> dans la bande. ⚠ Gardé de v129, non révoqué : en mode dessin les disques d'une fiche Promi et le plateau s'effacent (contour seul).

### ⚑ v130 (5 oct. 2026) — TROIS RÉCIDIVES NOMMÉES ; TROPICAL BREEZE ; LE MODE DESSIN NE RECOUVRE JAMAIS LA BANDE. (Décisions Tom.)
> **⚑ UNE DALLE SEULE EST ENGENDRÉE, JAMAIS DÉCOUPÉE DANS LA TOILE (C-048 — récidive, « interdit, définitivement, dans le prototype comme
> dans Swift »).** *Pourquoi c'est revenu* : ce n'est pas un retour récent — depuis v29, pour les cinq mondes à trame (Buvard, Braille,
> Tesselle, Taille-douce, Houle), `dalleTrame` peignait la Toile AUTOUR de la dalle puis rognait au pixel sur sa cellule : un polygone à
> bords en marches, avec les éclats des voisines (mesuré : 1,2 à 3,5 % de pixels d'une autre dalle). `redteam_decoupe` ne piégeait que les
> appels (`drawImage`, `getImageData`…) des ÉCRANS, pas ce que le moteur faisait en lui-même. *La parade* : chaque peintre de trame saute
> les graines qui ne sont pas la dalle demandée (`_cibleDalle`), et le masque au pixel ne s'applique plus à ces mondes (`_ENGENDRE`).
> *Le juge* : `redteam_decoupe`, famille **G2** — sur la fiche, l'Index, le Fil, la fiche d'un Cercle et son fil (défilé compris), en clair
> et en sombre, une dalle rendue seule ne porte pas plus de 0,3 % de pixels d'une autre couleur que la sienne ; rouge sur v129.
> *La règle* : **un peintre de monde reçoit la dalle à peindre et n'engendre qu'elle ; rogner un rendu plus large est une découpe, même
> à l'intérieur du moteur.**
> **⚑ LA DOUBLE ZONE DE LA PELOTE (C-002 — récidive).** *Pourquoi* : le Studio ouvre d'autres contextes WebGL ; le navigateur retire
> celui de la Pelote ; à l'ouverture suivante `_glInit` créait un canevas NEUF et l'ancien `#auBouleGL` restait dans la page, figé, sous
> le nouveau — un second contour. `redteam_zone` n'ouvrait jamais le Studio. *La parade* : `peintGL` retire l'ancien canevas (et tout
> `#auBouleGL` orphelin) avant de poser le neuf. *Le juge* : `redteam_zone`, contrôle C — Aura, Studio (contexte perdu), Studio, Aura ;
> il n'y a que `auBoule` et UN `auBouleGL`. *La règle* : **un canevas qu'on remplace se RETIRE ; un juge passe par le chemin de
> l'utilisateur (les écrans qu'il traverse entre deux ouvertures), pas seulement par l'écran jugé.**
> **⚑ LES ÉCRANS REFLÈTENT L'ÉTAT RÉEL TOUT DE SUITE (C-049 — régression).** Deux causes mesurées : ① l'Aura n'était bâtie qu'à son
> ouverture (`ouvre()`), et `closeAll()` ne lui retire pas `.show` (§8) : tenir ou retirer depuis une fiche ouverte par-dessus elle la
> laissait telle quelle ; `syncAll` appelait l'ancien `buildAura`, qui ne peint plus cet écran ; ② le Fil gardait les événements d'une
> parole retirée (son journal n'est pas la liste des paroles). **Une seule source de vérité : `promises` ; `window._paroles`
> (`signe`, `abonne`, `publie`) ; l'Index, le Fil, l'Aura et le fil du Cercle s'y abonnent et comparent avant d'agir** (`lot-V130-REACTIF`) ;
> `syncAll` publie ; après chaque geste, une signature qui a changé sans publication est publiée (aucun chemin ne peut l'oublier).
> ⚠ L'Aura attend la fin de l'animation de « tenir » (v124) : elle est alors sous la fiche. Juge : **`redteam_reactif.py`** (planter,
> tenir, retirer par les vrais boutons ; 30 contrôles ; 25/30 sur v129). ⚠ La liste « Ce que tu as tenu » reste bornée à trois dalles,
> six dès cinq tenues (Q187) — les plus récentes d'abord.
> **⚑ LE CORPS SOMBRE D'UN PROMI EST TROPICAL BREEZE `#8ACBE8`** (Pantone 13-4307 TPG, relevé par Tom sur son échantillon ; remplace
> `#335382`) — fiche Promi et page + d'un Promi, en sombre. **Le texte posé dessus passe à l'encre `#201908`** (9,79:1) : titre, à-qui,
> échéance, mention du trait (posés à la source, par le poseur de la fiche), et tout le reste par un seul propriétaire
> (`lot-V130-TROPICAL` : texte < 4,5:1 ou contour < 3:1 sur ce fond → l'encre ; il passe dans la micro-tâche de la mutation, avant
> l'image). Jeton `--c-tropical78`. ⚠ **Le résolveur d'état de la fiche sert aussi aux cartes de l'Index et du Fil** (corps resté sombre) :
> il DÉCLARE le corps pastel (`e.corpsPastel`), c'est le poseur de la fiche qui en tire l'encre. Mesuré : états sur ce corps — à tenir
> ΔE 103, en cours 76, tenu 70 (seuil 15) ; **bande `#82AEF8` contre corps : ΔE (CIELAB) 28,5 — au-dessus du seuil du ton sur ton (15) —
> mais ΔE00 13,1 et Δlum 17,6** : c'est le trait qui les sépare. Aucune des deux couleurs n'a été retouchée.
> ⚠ **Deux pièges du lot** : ① **une passe accrochée à un `MutationObserver` ne lit jamais les styles dans la micro-tâche de la
> mutation** — chaque `getComputedStyle` y force le recalcul des styles de tout le document (la première image d'une fiche passait de
> 450 à 600 ms) ; elle se demande pour l'image qui vient (`requestAnimationFrame`, avant la peinture). ② **le Peaufiner a SON corps** :
> celui d'une fiche Promi TENUE est Tropical alors que la fiche est terre — « sur quel fond suis-je » se lit sur le premier fond opaque
> sous le nœud (`window._tropicalSous`), jamais sur une classe de la fiche.
> **Juges réécrits au niveau de la décision** (originaux dans `sauvegardes/*-avant-v130.py`) : `redteam_flash_etat` (la première image à
> l'encre, plus à la crème), `redteam_murs` contrôle 9 (la phrase suit le fond du mur), `redteam_decisions`, `redteam_couleurs_ref` (E8).
> ⚠ **OUVERT (Q386)** : « Ma Parole ! » ne tient pas 3:1 sur Tropical (`#FB4C0D` : 1,9:1) — `redteam_murs` 25/26, rouge par décision à prendre.
> `banc_rendu` REFIGÉ : les 60 images de dalles des cinq mondes à trame ont changé (c'est la correction) ; les 220 autres sont au pixel.
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — cinquième principe : AUCUNE SUPERPOSITION SUR L'ESPACE DE DESSIN.** Tom retient la
> rangée A, sous la bande. Ni rangée, ni menu de tailles, ni couleurs dans la bande : la page se réorganise. Promi et Chiche : les trois
> lignes du bas descendent (36 pt sur la planche), espacements gardés ; la rangée est sous le trait avec un écart franc (24 pt proposé) ;
> tailles et couleurs se déploient SOUS la rangée. Cercle : tout est masqué sous la bande sauf le titre. Tout revient à POSER ou à la sortie.

### ⚑ v129 (4 oct. 2026) — L'ONBOARDING, TEXTE FIGÉ ; « CERCLE » CENTRÉ ; LE MODE DESSIN LIBÈRE L'ÉCRAN. (Décisions Tom.)
> **La dernière diapositive (C-006), quatre paragraphes, mot pour mot** : « C’est planté. » · « Ton premier Promi, ta première dalle sur ta
> Toile. Plus qu’à le tenir. » · « Primo, un Promi, c’est ta parole donnée. Deuxio, un Chiche, c’est un coup de culot. Tertio, un Cercle,
> c’est tout cela à la fois, mais à plusieurs. » · « Le reste se découvre en traçant. La suite t’appartient. » **« Deuxio » est le seul
> mot penché : 3°** (`.onbv-deux`, `skewX(-3deg)`), même police, même graisse, même couleur. La taille et la disposition des voisines sont
> validées. `redteam_onboarding` porte le texte EN DUR (`TEXTE_FIN`) et l'inclinaison (O22 : 3° ± 0,5, aucune autre).
> **« CERCLE » dans son encart (C-046) — la cause n'était ni la police ni la ligne de base** : une règle de v100
> (`#detailPoster.dp-mode-nuee #dptNat{translate:none}`) retirait au Cercle le recentrage de v97 (+2,65), pour rendre à `redteam_nuee` sa
> cote d'avant. L'encre du mot est maintenant à la même hauteur pour les trois natures (58,7 → 81,3, milieu 70). Juge :
> **`redteam_motmarque.py`** (l'ENCRE, pas la boîte ; ± 0,5 pt ; 0/4 avant). `redteam_nuee` : la cote du mot passe de 52 à 55,7.
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — quatrième principe : LE MODE DESSIN LIBÈRE L'ÉCRAN.** Les disques et leurs noms
> disparaissent : la place va aux réglages du dessin. L'encart du haut (nature, ✕ FERMER) est masqué : il n'en reste que le CONTOUR, au
> trait fin, sans fond ni texte — jamais une transparence. Tout revient à POSER ou à la sortie du mode.
> **C-031** : Volubilis, Guingois, Ramage et Esquille restent immobiles au repos dans le prototype — REPORTÉ au portage Swift.
> **`redteam_couleurs_ref` (C-047)** : les « 2 écarts » de v128 étaient du JUGE — une mini-dalle du fil d'un Cercle défilé, peinte à la
> demande, était vide côté référence au moment du relevé (« ΔE 99 » face à rien). Un canevas vide d'un seul côté est compté et listé
> (« non peints »), dans les deux sens ; il n'est plus comparé à rien.
> **C-045 — le trait de validation personnalisé** : concept seul, `TRAIT-PERSONNALISE-CONCEPT.md` ; rien n'est construit.

### ⚑ v128 (4 oct. 2026) — L'ONBOARDING (TEXTE, VOISINES VIDES) ; LE DESSIN REMPLACE LA DALLE ; QUATRE MONDES ONT LEUR MOUVEMENT. (Décisions Tom.)
> **L'onboarding, dernière diapositive (C-006)** : « Ça y est. » · « Ton premier Promi, ta première dalle sur ta Toile. » (le texte d'avant
> v125) · « Un Promi, ta parole donnée. Un Chiche, un défi lancé. Un Cercle, une parole à plusieurs voix. » · « Le reste se trace. »
> (qui prend la place de « Le reste se découvre à ton rythme. »). **Les voisines ne sont PAS colorées** : des cellules vides, rendues comme
> celles de la vraie Toile, à leur taille de v127 (`Toile.voisines`, la teinte ne vient que sur `couleur:true`, que personne ne demande).
> **C-043** : l'onboarding en Gilbert est une décision de Tom (message joint au lot v127, 4 oct. 2026).
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — trois principes** : ① **le dessin REMPLACE la dalle ou la photo dans la bande** —
> jamais par-dessus, ni sur un Promi, ni sur un Chiche, ni sur les dalles d'un Cercle ; la bande montre UNE chose à la fois (la dalle, la
> photo ou le dessin) ; masquer le dessin fait revenir la dalle ; ② **le menu du bouton photo est compact** — la géométrie de la pastille
> `.chip` (32,5 px de haut), 4 px entre deux (8 avant) ; ③ **« Dessiner » est en tête du menu**, sur la fiche et sur la page +.
> **⚑ LA VIE AU REPOS** : `_VIV_PLEIN` (une cloche pleine : le mouvement se voit 1 à 2 s, plus seulement son milieu — Houle, Éclisse) ; la
> QUEUE (420 ms après un mouvement, la boucle tourne, l'image d'avant rendue à chaque image : les ressorts convergent sans se voir —
> Bobinette) ; **quatre mouvements écrits dans le peintre** : Chamade (le cœur bat), Chantourné (le médaillon tourne à peine), Brouillamini
> (la dalle pivote sur sa graine), Mascaret (la lame glisse) — des tracés repeints sous une transformation, jamais une image déplacée ; le
> calque de repos est sauté pendant le mouvement. **Seize mondes bougent ; quatre restent immobiles : Volubilis, Guingois, Ramage, Esquille.**

### ⚑ v126 (4 oct. 2026) — LE REGISTRE DES CHANTIERS ; L'AURA FIGÉE (B) ; LA TOILE VIT AU REPOS ; LE CREUX DU DOIGT SUR LA CARTE. (Décisions Tom.)
> **⚑ `CHANTIERS.md` EST LE REGISTRE — quatre règles** (Tom : « Tom perd des demandes d'un lot à l'autre, et ça s'arrête maintenant ») :
> **① un numéro (C-001…) n'est jamais supprimé ni réutilisé ; ② seul Tom valide ou abandonne un chantier ; ③ toute nouvelle demande
> reçoit un numéro AVANT le moindre travail ; ④ chaque rapport finit par le tableau des chantiers non validés.** États : OUVERT · EN COURS ·
> FAIT, EN ATTENTE DE TOM · VALIDÉ PAR TOM · REPORTÉ (raison, lot visé) · ABANDONNÉ PAR TOM. Juge : **`redteam_registre.py`** (sans
> navigateur ; rougit sur une copie amputée d'une ligne). Le carnet d'avant (chantiers 1 à 78) : `CARNET-CHANTIERS-ARCHIVE.md` — là où ce
> fichier écrit « chantier 59 », « CHANTIERS.md, chantier prioritaire », c'est lui.
> **⚑ LA SÉRIE DE JUGES, ALLÉGÉE (C-030).** À chaque lot, une série COURTE : les juges des chantiers touchés, plus **six sentinelles —
> `redteam_couleurs_ref` · `redteam_decisions` · `redteam_joignable` · `redteam_ecrans` · `redteam_volume` · `redteam_registre`**. La série
> COMPLÈTE tourne **un lot sur trois, et avant tout refigeage**. Un juge lent réduit son échantillon dans la série courte
> (`redteam_corps --n=20`, `redteam_zone --n=12`, `redteam_vivant --duree=70 --mondes=…`). Ce qui touche le moteur garde `banc_rendu` et
> `redteam_rythme`.
> **⚑ L'AURA EST FIGÉE SUR LA COMPOSITION B (C-005).** Cotes en points 390 × 844, haut → bas de chaque bloc, phrase de deux lignes :
> ```
> plateau 40 → 100 · Pelote (silhouette) 132,53 → 374,53 · ombre 391,22 → 407,45 · « PARTAGER MA PELOTE » 435,47 → 495,47
> phrase 515,59 → 566,56 (une ligne : 541,07) · Noyaux 582,77 → 689,77 · légende 709,05 → 733,30 · chiffres 752,02 → 782,02
> « ce que tu as tenu » 800,52        — 62 pt d'air sous les chiffres
> ```
> Dans le code : `_CMP=[14,12,12]` (face à v124), ombre `K.ombre.y` 391,224 · `K.G2` 22 · `K.AIR_MOT` 18,71 − 2,5 · `K.nx.y` 444,061.
> `?aura=` est retiré. **`releve-aura.py` porte ces cotes EN DUR (`COTES_B`, ± 0,5 pt)** — la dette de 36 écarts est soldée ; la preuve :
> `--sonde-cote` (le bouton à +0,6 pt) rougit. Son acquis 7 épingle le souffle (`_peloteMod`) : **on compare au même angle ET au même
> souffle** (il rendait 6,8 %, 12,6 %, 43,6 % ou 47,9 % selon l'instant). Sa sonde d'encre cherchait encore le brun en sombre (0,0 pt).
> **⚑ LA TOILE VIT AU REPOS (C-028).** Avant : aucun des vingt mondes ne bougeait au repos (mesuré, 24 s chacun) ; le seul mouvement sans
> parole était le FRÉMISSEMENT de toute la Toile au retour sur l'accueil (`liven`). Depuis v126 (`promi-moteur.js`, `_vivTire`) : toutes
> les 5 à 15 s (tiré au hasard, compté de la fin d'un mouvement), UNE dalle (70 %) ou DEUX bougent 1 à 2 s par les voies du frémissement
> (place, étirement, tour, poids de matière), en cloche, au quart de son amplitude ; un seul minuteur entre deux mouvements, la boucle
> d'images arrêtée ; rien si l'écran est couvert, en arrière-plan, sous « Réduire les animations », ou dans les 5 s d'un toucher.
> **Douze mondes vivent** ; **huit restent immobiles** faute de manière (`_VIV_NON` : Volubilis, Guingois, Mascaret, Ramage — rien ne
> bouge par cette voie ; Madrure, Chantourné — seul le titre bougeait ; Chamade, Éclisse — le mouvement gagnait toute la Toile) : C-031.
> Juge : **`redteam_vivant.py`** (3 min par monde ; `--fixe` rougit). ⚠ Mesuré à la naissance : environ une fois sur dix la dalle ne revient pas
> exactement à l'image d'avant (0,1 à 1 % des pixels : Touffe, Tesselle, Bobinette, Taille-douce) ; sous Houle un intervalle de 25 s. Le juge les
> prend : c'est le produit qui varie (§7), pas l'instrument.
> **⚑ LE CREUX DU DOIGT EST SUR LA CARTE GRAPHIQUE (C-029).** `contact()` est porté ligne pour ligne dans le shader (plateau, cuvette en
> asin, bourrelet, cloche ; place, normale par la pente, peigne couché, ombre du fond) ; l'empreinte arrive en uniformes. Banc WebKit,
> doigt posé et glissé : p50 17 ms, p95 20 à 25 ms selon la passe — la cible de 22 est au bord du banc, qui plafonne à 19–20 sans rien peindre (25–42 en v125, 156–175 avant) ; ΔE00 moyen 0,7 contre le peintre. Juge :
> **`redteam_pelote_doigt.py`** (`--temoin` : le contact par le processeur, il rougit). **Le rendu par les poils, pas par une texture :
> accepté par Tom.** Mesure de Tom, iPhone 16e (`b116538`) : 220 000 poils, p50 17 ms, p95 25 ms, 54–56 images/s.
> **⚑ LE GESTE DE COULEUR DU STUDIO (C-010) — la cause** : `touch-action:pan-y` sur `#stBg` (posé par le glissement de monde) ; un doigt
> qui part à la VERTICALE ou en diagonale est repris par le navigateur (`pointercancel`, plus aucun `pointermove`). Le juge partait
> toujours à l'horizontale ; à la souris il n'y a pas de `touch-action`. **Un geste au doigt se prouve dans TOUTES les directions.**
> Parade : au doigt, le geste se lit sur `touchmove` (non passif, annulé dès qu'il est armé). `redteam_studio_geste` 22/22 (16/22 avant).
> **⚑ RAMAGE, L'ONDE RONDE (C-009) — OUVERT.** Déclencheur mesuré : l'ARRIVÉE d'une plume. Le film de la pousse est un disque (Worker,
> état d'arrivée) posé sur le plumage de l'état d'avant : anneau de liserés au bord, puis 5 à 16 % des pixels sautent hors du disque à la
> dernière image. Trois essais (canevas processeur, papier et plumage borné de l'image d'ouverture) n'ont rien supprimé : le moteur est
> rendu tel quel. `redteam_ramage_onde.py` est ROUGE (le défaut).
> **L'onboarding (C-006)** : le concept est sur la DERNIÈRE diapositive ; son fond est un fragment de Toile posé par le moteur — la
> nouvelle parole et des voisines qui ne sont à personne (`Toile.sync(ids + voisines)`, rien n'est sauvegardé ; `terminer` rend la Toile
> à la seule parole plantée). `?voisines=4|7|10` ; 7 en attendant le choix de Tom.

### ⚑ v127 (4 oct. 2026) — L'ONBOARDING, RAMAGE SANS DISQUE, LE RETOUR EXACT DE LA VIE AU REPOS. (Décisions Tom.)
> **L'onboarding, dernière diapositive (C-006, C-043).** La dalle de la nouvelle parole garde la taille et la place d'avant v126 (à l'image,
> clair : 158,7 × 155,0 pt à (131–133 ; 570–571), 14 710 pt²). **Les voisines ne sont PAS des paroles** : ce sont sept cellules vides du
> semis, dépliées par le peintre à 0,62 et teintes d'un ton de la palette (`Toile.voisines(7, {…})`, `Toile.voisines(0)` les rend au vide).
> ⚠ Mesuré : en faire des paroles recadrait la vue (zoom 2 → 1) puis, même sans recadrage, leur poids POUSSAIT la dalle principale de 10 pt.
> ⚠ Seul Pochade (le monde du premier lancement) les peint. `?voisines=` est retiré. **Tout le texte courant de l'onboarding est en Gilbert**
> (écrit en minuscules, tel quel — exception à « Gilbert en capitales », décidée par Tom) ; 20 px entre deux phrases, 33 sous « Ça y est. ».
> **Ramage (C-009) : LE DISQUE DE LA POUSSE EST SUPPRIMÉ** — c'était un effet posé sur la Toile. La plume arrive D'UN COUP, en une image
> (`window._ramFilmOff` par défaut ; `_ramFilmOn` rend le film, pour comparer). ⚠ Sous Ramage, une plume qui arrive redessine tout le plumage
> (27 % des pixels) : pousser « le long de ses traits » demanderait de le recalculer à chaque image. Juge : `redteam_ramage_onde` (réécrit).
> **La vie au repos (C-028) — LE RETOUR EST EXACT** : au tirage la Toile entière est gardée telle qu'elle est peinte (`_vivGarde`), et rendue
> pixel pour pixel à la dernière image (`_vivRendre`) si rien d'autre n'a changé (`_vivSigne`). Ce n'est ni une dalle ni un fragment : la
> Toile entière, 1:1, sur elle-même. **Le titre ne bouge jamais** pendant un mouvement de repos. Juge : **`redteam_retour.py`** (cent
> mouvements et plus, 0 pixel ; rouge sur v126). ⚠ **Un mouvement qui ne déplace que le TITRE n'est pas un mouvement de matière** : trois des
> « douze » de v126 (Bobinette, Esquille, Brouillamini) n'avaient que lui (Bobinette est réparé, les deux autres sont immobiles) — le juge comptait les pixels du titre.
> **Les mondes (C-031)** : `_VIV_CLOS` (hors de la cellule de la dalle tirée, l'image d'avant est rendue à chaque image : le mouvement ne
> gagne jamais la Toile) et `_VIV_GR` (la graine tirée est prêtée au monde à sa place du moment, le temps de le peindre). **Douze mondes
> bougent** : Pochade, Touffe, Tesselle, Braille, Buvard, Houle, Taille-douce, Halin, Ritournelle, Bobinette, + Madrure et Éclisse (v127).
> **Huit sont immobiles, à écrire dans leur propre peintre : Volubilis, Guingois, Mascaret, Ramage, Chantourné, Brouillamini, Chamade,
> Esquille** (Chamade et Esquille essayés par la graine prêtée : à-coups, mouvement hors tirage — retirés).

### ⚑ v124 (3 oct. 2026) — L'AURA REMONTÉE ENCORE ; « PARTAGER MA PELOTE » ET « GARDER TA TOILE » EN COULEUR ; TENIR EST FLUIDE. (Décisions Tom.)
> **Q378 tranchée : la fluidité passe avant la densité.** Six paliers : 220 000 · 180 000 · 150 000 · **110 000 · 90 000 · 75 000**. À
> 110 000 et en dessous, le poil reprend l'épaisseur et le reflet de la densité 1 (`reglePoil`, l'atlas est refait) — jamais sous les yeux.
> **L'Aura (en points)** : Pelote → ombre −4 · ombre → bouton −4 · bouton → phrase −4 · phrase → ses disques −4 ; la phrase passe de 19,4 à
> **20,4 px**. Ombre 405,224 · bouton 449,47 · phrase 541,6 · Noyaux 620,8 · **les chiffres finissent à 820,0 : 24 pt d'air sous eux à
> 390 × 844** (objectif : 20). ⚠ La hauteur de la phrase se lit EXACTE (`getBoundingClientRect`), plus par `offsetHeight` (arrondi : un
> demi-point d'air selon le nombre de lignes).
> **⚑ « PARTAGER MA PELOTE »** : PromiLate 15 px, capitales écrites telles quelles, chasse 0 — la hauteur de capitale des phrases du trait
> (10,67). La grammaire du bouton ne bouge pas. **Sa couleur** (`texteBouton`, `nouveauTexte`) : un ton de la palette du Studio tiré à
> chaque ouverture, jamais celui des poils ni celui du corps, **≥ 3:1** face au fond, jamais kaki ; sinon l'encre du mode. Juge :
> **`redteam_bouton.py`** (50 ouvertures × 4 palettes). ⚠ L'encre du clair `#201908` est dans la plage du kaki (h 87°, L 0,21) : le repli
> décidé n'est pas un tirage, la règle du kaki juge les teintes TIRÉES.
> **⚑ « GARDER TA TOILE »** (Réglages, `#compteCard .k`) : Atkinson 700 ; un ton de la palette **retiré à chaque retour sur la page**
> (`lot-V124-GARDER`), **≥ 4,5:1** (texte courant), jamais kaki, sinon l'encre du mode. « Revenir sur la page » ne se lit pas dans `.show`
> (les Réglages ne la perdent jamais) : c'est le point au milieu de l'écran qui redevient le leur. Juge : **`redteam_garder_toile.py`**.
> ⚠ Sous Ingénu en clair, aucun ton pastel ne tient 4,5:1 sur la crème : le texte y est toujours à l'encre.
> **⚑ TENIR UNE PAROLE — LA SACCADE, NOMMÉE.** Ce n'est pas un mouvement : deux changements d'état (amande 1 000 ms, puis « juste après »),
> et à chacun le fil principal restait bloqué 400 à 580 ms — ① deux rendus de dalle à des tailles neuves (dont la fiche tenue ordinaire,
> peinte 40 ms avant d'être recouverte par l'instant) ; ② la passe des polices sur tout le document (340–400 ms) ; ③ la passe de
> lisibilité et huit reprises par minuteries. **Parades** (`_instantTenue`, `lot-V124-FLUIDE`, `lot-V124-FLUIDE-POSE`) : l'instant est armé
> en phase de CAPTURE du clic ; ses deux dalles sont rendues À L'AVANCE quand la fiche à tenir est posée (`prechauffe`) ; pendant
> l'animation (`window._tenirAnime`) aucune passe de tout le document (`_apresMouvement` attend), la pose complète de la fiche passe APRÈS
> (`_tenirApres`), son contenu se remplit dans une image calme (`_tenirCorps`) ; les couleurs se posent à la source (sur la terre : texte
> crème, tenu en amande — Q269, en clair aussi ; le mot-marque à l'encre du plateau) ; cadence : `requestAnimationFrame`. Juge :
> **`redteam_fluide.py`** — 20 animations, travail du fil principal par image lu dans la trace Chromium (GPU, @3x) : la plus longue
> 19,8 ms, p95 5,6 ms (avant : 322 ms, 82 images au-delà de 20 ms).
> ⚠ **L'intervalle entre deux `requestAnimationFrame` ne juge pas une saccade au banc** : page au repos, il donne déjà p95 18,3 ms et un
> maximum de 26,7 ms. On mesure le TRAVAIL par image (les `RunTask` entre deux `AnimationFrame::Render`).

### ⚑ v123 (3 oct. 2026) — LA PELOTE : DENSITÉ 3, UN CORPS D'UNE AUTRE TEINTE, L'OMBRE CRÈME EN SOMBRE ; L'AURA REMONTÉE ; Q375. (Décisions Tom.)
> **Densité 3 et halo 3 RETENUS — ce sont des constantes** (`REG` : ×2, poil ×0,7, reflet adouci ; ΔE00 14 au ras, 0,12 D). **`?densite`,
> `?halo` et les niveaux 4 et 5 sont RETIRÉS.** Paliers du régulateur : 220 000 → 180 000 → 150 000. Mesuré (Chromium GPU @3x, ce Mac) :
> peinture 31,8 ms à 220 000 → le régulateur vise 150 000 ; `?mesure=1` dit le palier visé. **Corps sombre du Cercle `#5D4978` : validé.**
> **⚑ LE CORPS** : la peau sous les poils (et le plein de v120) prend **une AUTRE teinte de la palette du Studio, jamais celle des poils**,
> tirée au hasard à chaque ouverture avec le sol (`nouveauCorps`, `corps()`, option `corps` du peintre → `peau(…, CORPS)`). Elle tient
> **ΔE00 ≥ 15 face au sol ET à chaque marche de sa rampe de velours** (c'est la rampe qu'on voit, pas le sol nu), et **n'est jamais kaki**
> (sinon le ton suivant ; à défaut, la teinte écartée en clarté ; dernier recours crème ou seiche). Juge : **`redteam_corps.py`** (50
> ouvertures × 4 palettes ; le verdict vient de la peau PEINTE `__po` et de la marche de rampe la plus peinte). ⚠ Le bac de couleur le plus
> fréquent d'une Pelote est un MÉLANGE poil + corps : il ne dit pas la teinte du poil.
> **⚑ L'OMBRE EN SOMBRE EST UNE ELLIPSE CRÈME** (renverse v119) : même géométrie qu'en clair, crème 0,105 → ΔE00 5,05 (décidé 4 à 6) ;
> la flaque n'est plus affichée ni peinte.
> **L'Aura (en points)** : plateau → haut du halo −6 (10,7 → **4,7** : il ne touche pas) · Pelote → ombre −6 · ombre → bouton −6 · bouton →
> phrase −6 · phrase → ses disques −3. `K.bo.y` 105,532 · ombre 409,224 · bouton 457,47 · phrase 553,6 · Noyaux 634,3 · **les chiffres
> finissent à 833,5 : entiers sans défiler à 390 × 844**. `redteam_halo` : un seul niveau, 23 contrôles ; sa marge de 8 sous le plateau
> (jamais une décision) est remplacée par la cote décidée (4,5 ± 0,5).
> **⚑ Q375 — LA PREMIÈRE IMAGE D'UNE FICHE, trois causes** : ① les cotes n'étaient posées que deux images après l'ouverture (`_fichePose`
> pose maintenant aussi tout de suite) ; ② sur la terre d'une fiche tenue, le poseur écrivait l'à-qui en `#00341A` et la passe de
> lisibilité le repeignait crème (deux propriétaires : la crème est posée à la source) ; ③ **la passe de lisibilité retirait une couleur
> qu'elle n'avait plus écrite** (celle du poseur de la fiche suivante) — elle compare avant de retirer. Juge : `redteam_flash_etat.py`,
> contrôle 3 (6/10 avant, 10/10). ⚠ **Un relevé pris DANS un `requestAnimationFrame` passe avant les autres rappels de la même image :
> il lit un état qui ne sera jamais peint. On lit APRÈS l'image (une tâche postée depuis le rappel, `MessageChannel`).**
> **`redteam_couleurs_ref`** : un canevas sans id se nomme par le TEXTE de sa ligne, plus par son rang (la « mini-dalle instable » de v122
> était le juge : sur une liste qui défile le rang [3] n'était pas la même ligne des deux côtés). 0 écart, E7 = l'ombre crème.

### ⚑ v125 (3 oct. 2026) — LA PELOTE PASSE À LA CARTE GRAPHIQUE ; LE HALO PREND LA COULEUR DU CORPS ; LES TEXTES DE PALETTE NE SONT JAMAIS NOIRS. (Décisions Tom.)
> **⚑ LA PELOTE N'EST PLUS RECALCULÉE À CHAQUE IMAGE.** Cause nommée (iPhone 16e : 187 ms par image, 5 images/s) : `peint` repassait en
> JavaScript sur chaque poil (rotation, projection, lumière, marche de couleur) puis recopiait son tampon pixel par pixel. `peintGL`
> (`PeloteMoteur`, WebGL 2) envoie l'état des poils UNE FOIS à la carte graphique ; elle fait la rotation, la projection, la lumière du
> velours (le souffle compris) et pose le tampon de chaque poil — un POINT par poil, seuls les pavés tournés vers l'œil. Ce sont les
> mêmes poils aux mêmes pixels (ΔE00 moyen 0,3 contre le peintre, 98 % des pixels ≤ 2) : pas de texture plaquée, donc ni couture ni pôle.
> Banc WebKit : 141 → 17 ms au p50, 7 → 58 images/s. **Trois mesures à ne pas reperdre :** ① recopier le canevas de la carte dans le
> canevas 2D à chaque image coûte 6 à 20 ms en WebKit — on AFFICHE le canevas de la carte (`#auBouleGL`, posé sur `#auBoule`), et
> `#auBoule` n'est rempli qu'à la demande (`getContext('2d')` appelé de l'extérieur, `_aura.pelote()`) ; ② le coût est celui des SOMMETS,
> pas des pixels (220 000 rectangles de quatre sommets : 21–26 ms ; un point par poil, pavés visibles seuls : 17) ; ③ le carré du point
> se cale sur la boîte du tampon, pas sur le pixel du poil (le tampon part d'un côté). **Le toucher** : le contact (l'empreinte) reste
> CALCULÉ par `peint` (`seulementEtat`), pour les seuls poils qu'il déplace ; ils sont retirés de la passe fixe (un octet par poil) et
> dessinés par une seconde passe. Banc WebKit, doigt posé et glissé : 156–175 → 25–42 ms par image (Q383 : le calcul du contact reste
> au processeur). Sans WebGL 2, `peint` peint, comme avant.
> Le régulateur juge l'IMAGE sous la carte graphique (ce qu'elle dure au-delà de 8 ms), plus le temps de JavaScript ; la première
> fois que la carte est là, il repart de 220 000. `?mesure=1` écrit « rendu : CARTE GRAPHIQUE » et son cadre se tient au BAS de l'écran
> (il couvrait la Pelote) — `redteam_mesure.py`.
> **⚑ « LA DOUBLE ZONE » DERRIÈRE LA PELOTE ÉTAIT LE HALO LUI-MÊME** (mesuré : rien d'autre ne peint là ; `_flaquePelote` et
> `#auPeloteFlaque`, morts depuis v123, sont retirés) : presque blanc, plein jusqu'à 35° sous l'horizontale puis coupé en 10° — deux
> épaules, le bord d'un second disque. Le fondu du quart inférieur part de l'horizontale (45°, en S). **Le halo prend la teinte du
> corps** tiré à l'ouverture (clarté écartée du fond si elle ne peut pas faire une lumière : ΔE00 < 42). Juges : `redteam_zone.py`
> (30 ouvertures × 2 thèmes), `redteam_corps.py` 5.
> **⚑ LE CORPS NE SE VOIT JAMAIS SEUL** : les poils sont translucides, il compte pour un TIERS de la couleur rendue (32,5 %). Le tirage
> écarte maintenant la couleur RENDUE (2/3 poil, 1/3 corps) de ΔE00 ≥ 14 face à l'ouverture d'avant, jamais le même sol ni le même corps
> deux fois de suite (`promi_pelote_vue`) : la boule change de ΔE00 14–17 (médiane) d'une ouverture à l'autre, contre 6–15.
> **⚑ UNE TEINTE DE PALETTE QUI DOIT SE LIRE GARDE SA TEINTE** (`window._teinte.ajuste`) : OKLCH, la clarté seule bouge jusqu'au
> contraste (3:1 « PARTAGER MA PELOTE », 4,5:1 « Garder ta Toile », 5:1 visé pour les mots de l'onboarding). **Plus de repli sur
> l'encre** ; un ton qui en devient kaki est écarté, puis sorti du kaki par la chroma. Juges réécrits : `redteam_bouton` 5,
> `redteam_garder_toile` 3 (originaux dans `sauvegardes/`).
> **L'Aura — composition A appliquée, B et C par `?aura=B|C` (à l'œil, à retirer au choix de Tom)** : face à v124, Pelote → ombre −10,
> bouton → phrase −8, phrase → disques −8 ; ombre 395,224 · bouton 439,47 · disques 456,06 · 50 pt d'air sous les chiffres (794 / 844).
> ⚠ **Les cotes ne sont PAS figées : elles le seront, ici et dans `releve-aura`, quand Tom aura choisi.**
> **L'onboarding** : Promi, Chiche, Cercle en couleur de leur nature (`.onbv-nat`) ; 33 pt (1,5 interligne) entre « Ça y est. » et son
> paragraphe ; le concept (deux phrases de Tom) sur la première diapositive (Q382, à valider).
> **Q379** : le travail remis après « tenir » part en morceaux (`_tenirMorceaux`, `_enFond` : une tâche par morceau, une image entre
> deux) : la plus longue tâche après l'animation passe de 77 à 22 ms — `redteam_fluide` 5.

### ⚑ v122 (3 oct. 2026) — LES COULEURS : LE CACHE, LES DÉCISIONS, L'ORANGE DE MA PAROLE !, LE FLASH. (Décisions Tom.)
> **Ce que Tom voyait sur l'iPhone et que la mesure ne voyait pas : le CACHE de Safari** (voir `serveur.py` en tête). Mesuré : à
> l'écran rendu, v121 = v118 sur toutes les fiches, la page + et l'Index, deux thèmes.
> **La règle : chaque couleur porte la DERNIÈRE décision de Tom ; sans décision, sa valeur de v118** (`578ec80`). Juges :
> `redteam_couleurs_ref.py` (contre v118, exceptions nommées E1–E6) et **`redteam_decisions.py`** (79 décisions EN DUR, chacune avec
> sa source, contre l'écran rendu). **Les seuls écarts à v118 sont des décisions** : en sombre, les libellés d'état « à tenir » sont
> CRÈME (Q290) dès la première image — sur la fiche (« trace pour tenir » était `#F3E7D1`) ET sur les cartes de l'Index, du Fil et
> d'une personne (elles restaient `#DD4D23` : la passe de lisibilité ne les atteignait pas).
> **⚑ L'ORANGE DE MA PAROLE ! EST UN JETON À LUI SEUL** : `--orange-maparole` (posé sur `#murPhrase`, lu par `#murPhrase .mp` et rien
> d'autre) = `--c-orange-maparole` `#FB4C0D`, et `--c-orange-maparole-corps` `#FF7A55` sur les trois corps sombres de Peaufiner
> (`#murPhrase.sur-corps`). Ces deux valeurs n'existent NULLE PART ailleurs (`redteam_maparole.py` : source, 36 écrans × 2 thèmes, la
> phrase au doigt). Les jetons `--c-orange56-mur` / `--c-orange66-mur` de v121 sont retirés.
> **⚑ Q374 — LE FLASH ORANGE, NOMMÉ : deux propriétaires.** Le poseur de la fiche peignait « à tenir » en `#DD4D23` dans les deux thèmes ;
> la passe de lisibilité (`data-lis`, Q290) le repeignait crème en sombre, puis le poseur repassait (orange 400 ms, crème 476, orange
> 727, crème 1095). La crème est maintenant posée À LA SOURCE (`e.colTexte`, comme pour « en cours »). Juge : `redteam_flash_etat.py`
> (20 ouvertures, chaque image et une capture à la première).
> **L'Aura (§3, en points) :** plateau → silhouette −11 · Pelote → ombre (et flaque) −15 · ombre → « Partager ma Pelote » −12 · bouton →
> phrase −12 ; tout ce qui suit remonte d'autant (−50 au total). `K.bo.y` 111,532 · ombre 421,224 · flaque 405,347 · bouton 475,47 ·
> phrase 577,6 · `K.G2_OMBRE` 38 · `K.G2` 44. Le halo au niveau 3 commence à 110,7, le plateau finit à 100 : ils ne se touchent pas.
> ⚠ **Au niveau 5 (`?halo=5`), le halo monte à 101,4 : 1,4 pt du plateau.**

### ⚑ v121 (3 oct. 2026) — LES COULEURS DE v118. (Décision Tom.) Ce bloc CORRIGE le bloc v120 qui le suit.
> **Erreur de référence au lot v120** : la bonne référence est le commit **`578ec80` (v118)**, servi avec son moteur — pas « avant v116 ».
> **Tom garde le nouveau sombre : la seiche, dans les pages comme sur la Toile** (`--c-brun09 → --c-seiche10` en sombre, rendu tel quel).
> Toutes les couleurs de tous les écrans sont celles de v118 ; seules différences admises : la Pelote pleine (v120), l'Aura remontée,
> le halo, l'orange des murs (ci-dessous) et les violations retirées (§5). Juge : **`redteam_couleurs_ref.py`**, repointé sur 578ec80 —
> styles calculés, couleurs des canevas, et **les dalles rendues seules** (bande haute, cartes), rendues par le moteur de façon
> synchrone, à horloge figée et hasard réamorcé (relues à l'écran, v118 contre elle-même donnait ΔE 12 : la respiration et l'ordre
> des tirages). ⚠ Un flash du produit, présent dans v118 aussi : à l'ouverture d'une fiche « à tenir » en sombre, l'à-qui, l'échéance
> et « trace pour tenir » passent parfois une à deux secondes à l'encre du clair (orange) avant la crème.
> **L'Aura remonte** : l'ombre de 6 (453,224 → 447,224 ; flaque 437,347 → 431,347), l'écart sous l'ombre 56 → **50** (`K.G2_OMBRE`),
> tout ce qui suit de 12 (« Partager ma Pelote » 525,47 → 513,47 ; la phrase 639,59 → 627,59 ; …). Sous le bouton, l'air reste 56.
> **Le halo** : par défaut le niveau **3** (ΔE00 14 au ras, 0,12 D) ; `?halo=1…5` = 6/0,08 · 10/0,10 · 14/0,12 · 18/0,14 · 24/0,16 D.
> Il a son canevas, SOUS la boule (`#auPeloteHalo`, 330 × 330 centré) : au-delà de 0,12 D il sortait du canevas de la boule (demi-côté
> 148). Sa trame se dose en niveaux de COULEUR (± 2,75 sur le canal qui bouge le plus), pas d'opacité. Juges : `redteam_halo` (cinq
> niveaux, 91), `redteam_contour --halo=N`, `redteam_souffle` (« au-delà » = 0,12 D).
> **L'orange des murs** : `#FB4C0D` partout, sauf sur les trois corps sombres de Peaufiner (Promi, Chiche, Cercle) : **`#FF7A55`**, le même
> orange (OKLCH h 36,4°) éclairci jusqu'à 3 : 1 sur les TROIS (3,02 · 3,02 · 3,04 ; `#FF7954` ne tenait 3 : 1 que sur le plus sombre).
> Jeton `--c-orange66-mur` ; la phrase sait qu'elle est posée sur un corps (`.sur-corps`). `redteam_murs` 26/26. Q373 tranchée.
> **Repris de v119 (§5), un à la fois** : « garder de côté » (Q370, `redteam_garder` 18/18) puis les violations retirées (ombres de texte
> de « ✕ FERMER », du mot-marque et du badge, ombre dure et éclat du bouton d'achat ; dette du volume 304 → 290).

### ⚑ v120 (2 oct. 2026) — RETOUR EN ARRIÈRE. (Décision Tom.) Ce bloc CORRIGE les blocs v116 à v118 qui le suivent. *(v121 : sa référence « avant v116 » était FAUSSE — les couleurs sont celles de v118, seiche comprise : bloc ci-dessus)*
> **v119 est ANNULÉ** (`git revert bd156ae`, l'historique reste). **La casse du Studio, nommée :** le Zzz activé au premier lancement
> (`BOUTON_POSE=true`, hors navigateur piloté) — la nuit, l'app passait en sombre quel que soit le choix, les disques SOMBRE / CLAIR
> ne changeaient plus rien à l'écran (le choix n'était appliqué « qu'au changement d'écran », et le thème restait celui de la nuit)
> et le disque allumé contredisait le choix. ⚠ Aucun juge ne pouvait le voir : sous navigateur piloté le Zzz ne s'allumait pas.
> **⚑ LE Zzz EST COUPÉ PARTOUT, ET LA PASSE DE NUIT AVEC, JUSQU'À NOUVEL ORDRE** (`COUPE=true` dans `lot-V118-ZZZ` : ni thème de
> nuit, ni cran de nuit, quels que soient le réglage mémorisé, `?zzz=1` ou `?nuit=1`). `redteam_nuit` est donc ROUGE par décision.
> **⚑ HORS DE LA TOILE, LES COULEURS SONT CELLES D'AVANT v116** (référence : `sauvegardes/app-avant-v116.html`) — textes, fonds, corps,
> filets, pilules, anneaux, en clair et en sombre. **Le fond des pages sombres est le brun `#201908`**, plus la seiche (la
> substitution `--c-brun09 → --c-seiche10` de `lot-V116-SEICHE-css` est retirée). Exceptions, et seulement celles-là : la Toile en
> sombre garde l'encre de seiche (c'est le moteur qui la peint) ; le fond de la Toile en clair reste à plat ; l'orange des murs.
> Juge : **`redteam_couleurs_ref.py`** (styles calculés et échantillons de canevas, 36 écrans × 2 thèmes, contre la référence servie
> avec son moteur d'alors ; un écran pris en écart est repris sur une page fraîche avant d'être cru).
> **⚑ LA PELOTE EST PLEINE** : l'intérieur est opaque, toujours — alpha 255 en retrait de 4 % de D, aux deux thèmes, à tous les
> paliers. La peau n'était opaque que là où la fourrure couvrait son bloc à 98 % (alpha jusqu'à 57 au palier réduit) : on pose sous
> elle la même peau rendue opaque, bornée par un disque plein jusqu'à 0,972 R, fondu jusqu'à 1,012 R. Juge : **`redteam_plein.py`**.
> **Le halo et l'ombre de v119 sont repris tels quels** (`lot-V119-PELOTE`, `window._haloPelote`, `window._flaquePelote`) : le ton le
> plus clair de la rampe, décroissance exponentielle (ΔE00 7 au ras, 2,9 à 0,04 D, rien au-delà de 0,08 D), plein du côté éclairé,
> presque nul sur le quart inférieur, tramé au grain de l'app, respiration ± 20 % avec le souffle ; l'ombre : encre 0,10 en clair, en
> sombre une flaque de lumière dont l'ombre est le creux (aucune ombre crème). Écho, couronne de fibres et halo flou restent REFUSÉS ;
> D (un trait par parole tenue) reste EXCLU DÉFINITIVEMENT. L'écho de v118 est retiré ; la lumière du velours reste DANS le peintre.
> **Deux réglages à l'œil, par l'adresse, jamais mémorisés** : `?densite=1|2|3` (densité ×1, ×1,5, ×2 ; poil ×1, ×0,8, ×0,7 ; reflet
> adouci à 2 et 3) et `?halo=1|2|3` (ΔE00 au ras 6, 10, 14 ; étendue 0,08, 0,10, 0,12 D). Tom choisit sur l'iPhone.
> **L'orange des mots des murs est `#FB4C0D`** (jeton `--c-orange56-mur`). ⚠ **OUVERT (Q373)** : il n'atteint pas 3 : 1 sur cinq des
> huit fonds de mur (2,27 sur les trois corps sombres, 2,65 et 2,78 sur les corps clairs du Promi et du Cercle) — `redteam_murs` 25/26.
> **Non repris de v119** (le lot s'est arrêté au §4) : « garder de côté » (Q370) et les violations visibles (« ✕ FERMER », badge,
> bouton d'achat).

### ⚑ v118 (2 oct. 2026) — LE Zzz : LA NUIT, L'APP SE REPOSE. (Décision Tom.) *(COUPÉ en v120 — bloc ci-dessus)*
> **La raison : c'est l'ÉBLOUISSEMENT qui compte, pas la teinte** — on baisse la lumière des neutres clairs, on ne colore rien ; et
> **aucune permission de localisation** n'est demandée : le soleil se calcule (NOAA) aux coordonnées de RÉFÉRENCE du fuseau horaire
> de l'appareil ; fuseau inconnu : 22 h – 7 h.
> ```
> premier lancement              thème CLAIR, Zzz ACTIVÉ   (remplace Q301 : le thème ne suit plus celui du téléphone)
> clair + Zzz activé             du coucher du soleil + 1 h au lever : SOMBRE DE NUIT ; au lever, retour au clair
> clair + Zzz désactivé          toujours clair
> sombre + Zzz activé            le CRAN DE NUIT du coucher + 1 h au lever ; le jour, sombre ordinaire
> sombre + Zzz désactivé         sombre ordinaire
> ```
> **Un changement de thème ne se fait JAMAIS sous les yeux** : seulement au changement d'écran ou au retour au premier plan, et sans
> fondu. Les deux choix sont mémorisés (`promi_theme` = le CHOIX, `promi_zzz`).
> **Le cran de nuit** : seuls les NEUTRES CLAIRS (les jetons `--c-creme*` et `--c-blanc*` clairs — texte et surfaces crème) baissent
> d'un cran, **ΔL OKLCH = −0,06, teinte conservée** (crème `#F7F0DE` → `#E3DCCA`). Les natures, les états, les dalles et l'amande ne
> bougent pas, AU HEX PRÈS. Contraste du texte ≥ 7 : 1 (mesuré 14,2). **Aucun filtre de couleur, aucun voile.**
> **Le bouton : « Zzz »** — écrit exactement ainsi (Z majuscule, zz minuscules), même si ses voisins sont en capitales ; au Studio,
> au milieu de la ligne SOMBRE / AVEC TEXTE, avec la grammaire de ses voisins ; VoiceOver « Mode nuit, activé / désactivé ».
> ⚠ **v118 : LE BOUTON N'EST PAS POSÉ** — la ligne ne reçoit pas un troisième disque sans déplacer ses voisins (56 entre les paires,
> il en faudrait 84 : `planche-v118/planche-zzz.png`). Tant qu'il manque, le Zzz ne s'active pas seul (`BOUTON_POSE` dans
> `lot-V118-ZZZ`) : on ne livre pas un réglage qu'on ne peut pas éteindre. Essai : `?zzz=1` l'active (mémorisé), `?nuit=1` simule la nuit.
> Juge : **`redteam_nuit.py`** (heures d'almanach en dur, second calcul indépendant, bascule en direct = rouge).

### ⚑ v118 — LA PELOTE : L'ÉCHO DÉCALÉ *(retiré en v120 : halo et ombre de v119)* ; « PARTAGER MA PELOTE » SOUS L'OMBRE ; D EST EXCLU DÉFINITIVEMENT. (Décisions Tom.)
> **L'écho (Q368 → A)** : une copie PLATE de la silhouette (rayon 121), décalée de 11, dans un autre ton de la palette (le ton
> dominant + 2 ; le suivant s'il se confond avec la page, ΔE < 15). Aucun flou, aucun dégradé. Il entre dans la liste blanche
> NOMINATIVE de la Pelote (`.au-echo`, `window._echoPelote`, `lot-V118-PELOTE`) : `redteam_volume --sonde=echo` rougit si on le pose
> sur une dalle. **D (un trait par parole tenue) est EXCLU DÉFINITIVEMENT : c'est un compteur visuel qui croît avec l'action — la
> grille l'interdit.** Ne jamais le reproposer.
> **Le bouton (Q367)** : juste sous l'ombre, à **G2 = 56** du bas de l'ombre (525,5 → 585,5) ; la phrase et ce qui suit se placent
> ensuite, l'ENCRE de la phrase à 56 sous le bouton. L'ombre garde ses 60 pt, l'air ne se reprend pas. La colonne se lit : la Pelote ·
> l'ombre · le bouton · la phrase · les Noyaux · la légende et ses chiffres · ce que tu as tenu · ce qu'on t'a tenu.
> **`?mesure=1`** affiche, dans l'Aura, le temps par image (p50, p95) respiration active puis coupée — le diagnostic du Studio ne se
> lance plus que sur un nom de monde (`?mesure=madrure`).

### ⚑ v118 — LE FOND DE LA TOILE EST À PLAT, EN CLAIR AUSSI : `#DFCAA4`. (Tom.) Le dégradé `#E6D1AE → #D8C29A` est retiré
> (`_fondVif` rend une couleur) ; son entrée est soldée dans `volume-dette.json`. Le sombre était à plat depuis v116 (`#050302`).

### ⚑ v118 — LA DALLE D'ORIGINE DANS LA BANDE HAUTE (Q365 tranchée) ; LES MOTS DU MENU PHOTO (Q366) ; 2 € LE DESIGN.
> Avec « La dalle d'origine », la bande haute d'une fiche prend la COULEUR d'origine — **sauf si elle passe sous le seuil du ton sur
> ton face au champ (ΔE 15) : alors seulement, la rampe de Q30** (`window._origineBande`, `lot-V118-ORIGINE` ; juge `redteam_origine.py`).
> Le menu : « Importer une image » · « La dalle d'origine » · « La dalle du Studio » · « Retirer la photo ».
> Un design s'adopte à **2 €** (« Adopte ce design — 2 € ») ; les blocs datés d'avant écrivent 1 €.

### ⚑ v118 — CE QUI SE TOUCHE EST JOIGNABLE (`redteam_joignable.py`). Tout élément interactif se prouve par `elementFromPoint` à son
> centre ; tout gestionnaire n'appelle que des fonctions qui existent, et n'est posé que sur un nœud qui existe. La dette de naissance
> est NOMMÉE (`joignable-dette.json`). Q363 tranchée : le code des chemins de saisie remplacés est retiré (JS ; le CSS ne se nettoie pas).

### ⚑ v116 (1er oct. 2026) — LE MODE SOMBRE EST L'ENCRE DE SEICHE. (Décision Tom, série 4 adoptée, descendue de 2 %.) *(v121 : TOM LA GARDE, pages comprises — le retour au brun de v120 était une erreur de référence)*
> Fond `#050302` (OKLCH L 0,101, h 54,8° — la teinte y est plus juste qu'à L 0,12 : Δh +5° contre +13°), cellules vides L 0,136–0,161
> (h 40–56°), dalle neutre d'Ingénu en sombre `#1F1611`, grain léger ; **jamais bleu**. Le moteur la peint (rampes, `_fondVifDesc` plat,
> `renderTo`, `fondToile`, aperçus, noir et blanc, `cOf`) ; les pages sombres la prennent par `--c-brun09` en sombre (`lot-V116-SEICHE-css`,
> jetons `--c-seiche10`, `--c-seiche21`). Le clair ne bouge pas.

### ⚑ v116 — LA PELOTE : PLUS DE COURONNE, L'OMBRE AU PLUS PRÈS. (Tom : « les poils qui dépassent font des fils cheap ».)
> **Rien ne dépasse jamais du contour** (`redteam_contour.py`). La couronne de v115 est retirée. L'ombre reste, **centrée à 0,04 D sous la
> silhouette** (0,20 D la faisait flotter et sortait « Partager ma Pelote » du pli : il finit à 840,6). La respiration attend son option
> (planche v116 : la lumière du velours, le contre-jour au bord, les tenus qui se dressent — toutes dans le contour).

### ⚑ v116 — « + AJOUTER QUELQU'UN » GARDE SA LIGNE. La liste des profils défile dans son propre espace (`.gn-liste`), le bouton est
> dessous, 16 d'air, page + et fiche (`redteam_ajouter.py`). Sur un choix ouvert, l'onde de la page + monte à 28 sous le plateau :
> base 144, amplitude 16 ; trace 184, phrase 228 (étaient 196 / 22 / 236 / 280).

### ⚑ v115 — LE KAKI EST BORNÉ : teinte OKLCH 78°–140°, chroma 0,015–0,10 ET luminance 0,20–0,80. (Décision Tom : « le crème et
> les jaunes vifs ne sont pas du kaki ».) On ne touche à AUCUNE palette (Q360) : c'est le juge qui a été corrigé. **L'encre de Touffe,
> en sombre, est neutre : `#F4F2F0`** (`_tfInkTouffe`, Touffe seul ; l'encre du produit `_tfInk` reste celle des autres mondes ; le
> clair ne change pas). Coupables restants mesurés : `planche-sombre/kaki-coupables.png` (34 couleurs).

### ⚑ 30 SEPTEMBRE 2026 (v114) — JAMAIS DE KAKI. (Règle absolue, décision Tom.)
> **Est kaki toute couleur dont la teinte OKLCH est comprise entre 78° et 140° avec une chroma ≥ 0,015.** C'est interdit sur
> **toute dalle et toute matière vide produite par l'app** : palette par défaut, palettes proposées, teintes dérivées. **Seule
> exception : la couleur mère que l'utilisateur choisit lui-même dans la jauge** — et même alors, aucune teinte dérivée ne doit
> entrer d'elle-même dans cette plage. Juge : **`redteam_kaki.py`** (source · rendu des 20 mondes clair/sombre · planches), seuils
> en dur. ⚠ **Mesuré le 30 sept. : l'app VIOLE la règle aujourd'hui** — le fond de la Toile (`_fondVifDesc`, h 80–85), les rampes
> des vides d'Encre et de Braille, le crème dalle d'Ingénu `#EFE3C7` (h 88) et 15 palettes sur 24. Et le brun `#201908` lui-même
> est à h 87 (hors périmètre : c'est une page, pas une dalle). **Et un mélange peut y faire entrer ce qui n'y est pas** : l'encre
> de Touffe `#F6F1E7` (h 84,6, C 0,014) composée en sRGB sur un brun passe à C 0,015–0,016 — c'est ce qui a viré au kaki.

### ⚑ v115 — LA PELOTE : UNE COURONNE DE FIBRES, PAS UN HALO ; L'ESPACEMENT SE MESURE SUR SA SILHOUETTE. (Décision Tom.)
> **Le halo flou est abandonné.** La Pelote porte une **couronne de fibres folles** (`window._couronnePelote`, `lot-V115-PELOTE`) :
> des poils qui s'échappent de la silhouette jusqu'à **0,12 D au plus**, dans les couleurs de SES fibres (`rampeVelours`), de plus en
> plus rares en s'éloignant, deux fois moins sur le quart inférieur ; **ΔE00 6–12 avec le fond dans l'anneau 0–0,04 D** (dosée par le
> calcul, cible 8,5 ; mesuré 6,6–11,6 sur 4 palettes × 2 thèmes). **Elle seule respire** : ±15 % d'étendue et de densité, 10 s (4 s
> d'expansion, 6 s de retour, sinus), 0,6 s après l'affichage complet ; en pause hors écran / en arrière-plan ; « Réduire les
> animations » → immobile à mi-cycle. **Ombre** : centre à 0,20 D sous la boule, 0,45 D × 0,07 D, 0,10, encre du mode ; **aucune en
> sombre** (sa place reste réservée). **L'espacement se mesure sur la SILHOUETTE, jamais sur le halo** : G1 (plateau → silhouette) =
> G2 (bas de l'ombre → bloc suivant) = 2 × K.AIR = 56. Juges : `redteam_couronne.py`, `redteam_volume.py` (couronne en liste blanche).

### ⚑ 30 SEPTEMBRE 2026 (v114) — LA PELOTE EST LE SEUL VOLUME DE L'APP. (Exception de loi, décision Tom.)
> **Elle seule porte un halo et une ombre, nulle part ailleurs.** Halo : sa couleur (`solEffectif`), 0,10 au plus au bord, nul à
> 0,25 × D au-delà, 0,04 au plus sur le quart inférieur. Ombre : ellipse ≤ 55 % × 10 % de D, ≤ 0,12, encre du mode (jamais un noir
> pur), à 6–8 % de D sous la boule. Le haut visible du halo est à l'air de la colonne (`K.AIR` 28) sous le plateau.
> **Liste blanche NOMINATIVE : `lot-V114-PELOTE-css` (#auPeloteHalo, #auPeloteOmbre).** Tout halo, ombre floue ou dégradé ailleurs
> est refusé par **`redteam_volume.py`** (statique ; la dette d'avant la règle — 305 occurrences, dont le fond de la Toile — est
> NOMMÉE dans `volume-dette.json`, elle se solde, elle ne grandit jamais).

### ⚑ 30 SEPTEMBRE 2026 (v114) — LE FILET DU TRAIT : UNE SEULE EXCEPTION, NOMINATIVE.
> Plus aucun filet crème sous le trait, sous la flèche ni autour des disques (v113) — **SAUF sur la terre `#2B1020` d'une fiche
> tenue**, dans les deux thèmes : la crête `#0B4A2A` n'y est qu'à **Δlum 15,7** de la terre, c'est le filet qui la rend lisible.
> Il y est EXIGÉ. `redteam_filets.py` le piège dans le canevas (le crème adouci `rgba(247,240,222,.55)`) et l'a en liste
> blanche nominative (« fiche tenue »), jamais par tolérance.

### Les couleurs signal — la nature de la chose regardée

Chaque nature a SA couleur signal. Elle ne dépend jamais du contenu (§4). **Valeurs d'aujourd'hui**
(repris le 30 sept. 2026 ; la source est `PROMI-TOKENS.json`, reproduite dans `ETAT-30-SEPTEMBRE-2026.md` §2) :

```
LES NATURES — le CHAMP                    LES ÉTATS — la LIGNE (un anneau : trois arcs, jamais plus)
bleu      #82AEF8   un Promi              à tenir   #DD4D23   partout
rose      #FFB8D2   un Chiche             en cours  #291547   (clair sur fond sombre : #A77CF7)
lilas     #C9A8F5   un Cercle             tenu      #00341A   (sur la terre #2B1020 : l'amande #8FE08F)
violet    #291547   trait et texte posés sur le lilas d'un Cercle
amande    #8FE08F   la célébration seule (et la mention « TENU(E) »)
```

*(historique — jusqu'au 16 sept. : bleu #3A54FF · framboise #FA2258 · mauve #291547 Nuée · menthe #2BE88C tenu.
Les blocs datés qui suivent racontent chaque bascule.)*

> **⚑ 22 SEPTEMBRE 2026 — UN ANNEAU NE PORTE QUE TROIS ARCS.**
> (Décision Tom. *« Un anneau ne peut avoir que trois arcs : à tenir, en cours, tenu. S'il y en a
> davantage, le système est cassé. »*)
>
> **D'OÙ VENAIENT LES SEGMENTS EN TROP, MESURÉ** (`scratchpad/anneaux.py`) : le lot de la
> réciprocité (Q215, 14 sept.) peignait **deux moitiés** — à gauche ce que tu tiens, à droite ce
> qu'on te tient — soit 3 états × 2 moitiés = **jusqu'à six arcs**. Relevé : « toi » 6, Marion 5,
> Rachel 4. **Et pour Adrien et Nico, seule la moitié DROITE existait** : leur anneau ne montrait
> que ce qu'ON te tient, présenté comme si c'était ta parole. C'est là qu'était la logique cassée.
>
> **L'ANNEAU PORTE MAINTENANT LES TROIS ÉTATS DE CE QUI SE PROMET ENTRE VOUS, DANS LES DEUX SENS,
> UNE FOIS.** On concatène les LISTES avant d'en faire des parts : la pondération se fait par le
> **nombre de paroles**, jamais à parts égales entre les deux directions. La réciprocité garde sa
> rangée « Ce qu'on t'a tenu ».
>
> ⚠ **ET LE VOILE D'OPACITÉ QUITTE LES ARCS.** Le `opacity:.5` du gratuit portait sur la moitié
> droite : c'est LUI qui délavait les trois couleurs d'état sur la capture. Les couleurs rendues
> sont désormais **exactement** `#DD4D23` · `#291547` · `#00341A`, et leurs claires en sombre.
>
> **⚑ L'AMANDE `#8FE08F` NE PEINT QUE L'ANIMATION DE CÉLÉBRATION.** *« Quand une parole est tenue,
> une seconde dalle apparaît sous la première, de la même forme, en vert amande. Elle se décale,
> puis disparaît. L'amande ne peint jamais un état, ni un arc, ni un texte, ni une valeur claire. »*
> Balayé sur 8 écrans × 2 thèmes (`scratchpad/amande.py`) : **0 surface en amande hors animation**.
> Les deux dernières étaient le verbe de la phrase (repli, passé à la nature) et l'icône « Les
> Noyaux » de l'aide, qui dépeint des arcs et porte donc les valeurs d'état.
>
> **⚑ LE SOL DE LA SPHÈRE GARDE LA COULEUR DE LA PALETTE, PAS SEULEMENT SA TEINTE.** Il prenait
> bien le ton dominant — mais les deux transformations de Q210 écrasaient sa chroma :
> ```
> le ton dominant        C* 41,6
> × SOL_CLAIR 0,38       C* 18,8
> + 39 % vers le crème   C*  6,4     ← la teinte survit, la COULEUR non
> ```
> On garde la CLARTÉ (c'est elle qui rend les îles lisibles) et **on RESSATURE à 0,72 × la chroma
> du ton dominant** — exactement ce que fait déjà la rampe de velours. ⚠ **Et la ressaturation va
> dans `solEffectif`, pas dans `fondSphere`** : c'est LE POIL qui fait la couleur de la sphère, pas
> la peau ; posée sur la peau seule, elle ne bougeait rien sur une palette peu chromatique.

> **⚑ 21 SEPTEMBRE 2026 (soir) — LE PAYSAGE D'UNE FICHE, ET LES ÉTATS QUI BASCULENT.**
> (Moodboard des correspondances **v8** + décisions Tom. **Corrige les deux blocs qui suivent.**)
>
> **1 · L'AMANDE N'EST PAS LA VALEUR CLAIRE DE « TENU ».** *« Ma consigne était fausse. Elle sert
> uniquement à l'animation de célébration : une seconde forme de la dalle apparaît sous la
> première, se décale, puis disparaît — en vert amande. Rien d'autre. »*
> Le « tenu » a donc **sa** claire, comme l'« en cours » : **`#33BA6C`**, obtenue par le MÊME
> transport que le couple validé (`#291547` → `#A77CF7` : ΔL +49, ΔC +34, teinte gardée) — et,
> comme lui, **à ΔE 60 de son plein**. ΔE aux trois natures : **102 · 92 · 90**.
>
> **2 · LES ÉTATS BASCULENT AVEC CE QUI EST PEINT SOUS EUX.**
> ```
> à tenir    #DD4D23  partout — il se lit des deux côtés (Δlum 65 / 65)
> en cours   #291547 sur fond clair   ·  #A77CF7 sur fond sombre
> tenu       #00341A sur fond clair   ·  #33BA6C sur fond sombre
> ```
> La colonne de l'Aura (légende, arcs des Noyaux) est posée **sur la page** : elle bascule.
> L'anneau du **+** de l'accueil est posé **sur la barre sombre**, dans les deux thèmes : il
> garde les claires. C'est la même règle, appliquée à deux fonds différents.
> ⚠ **Et un état qui bascule se REPEINT quand le thème change** : `eta()` est lue à la
> construction. Sans repeinture, un changement de thème laisse les valeurs de l'ancien mode.
>
> **3 · LE PAYSAGE D'UNE FICHE TENUE (v8).** L'ocre est abandonné, le brun `#6B4630` aussi.
> ```
> terre    #2B1020   prune sombre — le SOL d'une fiche, dans les deux thèmes
> crête    #0B4A2A   la ligne d'horizon, posée sur la terre  (ΔE 51,3 · Δlum 35,4)
> anneau   #00341A   5 px, CERNÉ D'UN FILET CRÈME #F7F0DE de 1,4 px
> ```
> **Le filet n'est pas un ornement, il est la condition de lisibilité** : le vert profond n'est
> qu'à **ΔE 44,6 · Δlum 16,2** de la terre ; le filet crème est à **Δlum 217,3**.
> Sur la terre (L* 8,9) le texte passe **crème** (15,42 : 1) et les marques d'état prennent le
> **clair de « tenu »** `#33BA6C` (Δlum 128,8).

> **⚑ 21 SEPTEMBRE 2026 — LE JAUNE SORT, ET LE CLAIR D'« EN COURS » EST UN VIOLET.**
> (Décision Tom : *« Le jaune sort. C'était ma consigne, elle était mauvaise. #FFD447 a été retiré
> en v6, il ne doit revenir nulle part. »* **Corrige le bloc du 20 septembre qui suit.**)
>
> ```
> en cours          #291547   le champ plein — inchangé
> en cours, clair   #A77CF7   le violet que le jeu PORTAIT DÉJÀ : --c-mauve63
> ```
> **Rien de neuf n'entre dans la palette** : `--c-mauve63` y était. Mesuré : **ΔE 30 du lilas
> Nuée, 41 du bleu Promi, 58 du rose Chiche**, Δlum 113 au pire fond sombre.
>
> **⚠ ET LA RÈGLE QUE J'AVAIS ÉCRITE ÉTAIT FAUSSE.** « Le clair d'un état est la valeur qu'il
> remplace » marchait pour l'amande, par coïncidence ; elle ramenait ici une couleur **retirée**.
> **La règle juste : le clair d'un état est de LA FAMILLE de son état, et il s'écarte des trois
> natures d'au moins ΔE 25.**
>
> **⚠ ET LA DIRECTION BLEU-VIOLET EST FERMÉE, C'EST MESURÉ.** Entre le bleu Promi (h 277) et le
> lilas (h 308) il n'y a que **31°** : dans le registre du produit (L* 70-84, C* 45-62) l'écart au
> lilas n'y dépasse **jamais 24**. Le seul bleu-violet qui passe ΔE 25 tombe à **ΔE 3 à 11 du
> périwinkle #8FA0FF** — la valeur que la v6 avait retirée. Une teinte décalée vers le rouge-violet
> passe, mais à ΔE 25 du lilas **on est déjà dans le magenta** ; garder la teinte et descendre en
> clarté donne le même écart **en restant un violet**. C'est ce qui a été retenu.
>
> **⚑ LES AVATARS DES NOYAUX PIOCHENT DANS L'IDENTITÉ SEULE.** `_BPAL` = les quatre tons de la
> palette d'identité, et rien d'autre : **un visage ne porte jamais un état.**
>
> **⚑ ET TON VISAGE NE CHANGE PLUS À CHAQUE OUVERTURE.** `USER.seed` était `(Math.random()*1e9)|0`,
> jamais sauvegardé — exactement le défaut de `cc()` corrigé le 13 septembre sur les dalles. Même
> parade, même ordre : **la graine sauvegardée d'abord ; sinon dérivée d'une clé stable (le nom),
> jamais d'un id ni d'une horloge ; et on l'enregistre.** (`_grainePropre`, `promi_graine`.)
> ⚠ **Et c'est une DÉCLARATION de fonction, pas une affectation** : `USER` est construit 960 lignes
> plus haut dans le même bloc — seule une déclaration est hissée.
>
> **⚑ LE SOL DE LA SPHÈRE SE DÉCALE JUSQU'À SE DÉTACHER DE LA PAGE.** *« Si le sol ne se détache
> pas assez de la page, il se décale jusqu'à passer le seuil. »* Seuil : **42**, celui du §3 — déjà
> le plancher du contour dans le juge de l'Aura. **Le décalage garde la teinte** (on mélange vers le
> blanc ou vers le noir, jamais vers une autre couleur) et **s'éloigne du côté où l'on est déjà**.
> ⚠ **On vise 44, pas 42, et la marge est MESURÉE** : le garde-fou agit sur la COULEUR, ce qu'on
> voit est le RENDU, que la fourrure assombrit — il en coûte jusqu'à 0,7. Balayé sur les 21 palettes
> × 2 thèmes : **0 sous le seuil sur 42 mesures**, la plus faible Taciturne sombre à **43,0** (elle
> était à **10,4** sans garde-fou). Sonde : `scratchpad/balaye20.py`.

> **⚑ 20 SEPTEMBRE 2026 — LE MOODBOARD DES CORRESPONDANCES v7 FAIT FOI.**
> (Décision Tom, sur la planche v7 + son message. **Il remplace le bloc du 17 septembre qui suit, gardé pour l'histoire.**)
>
> **1 · L'ENCRE DU MODE CLAIR EST ARRÊTÉE À `#201908`, ET LE PRINCIPE D'ÉCHANGE DE LA v4 EST
> ABANDONNÉ** — *« un fond et une encre n'ont pas les mêmes contraintes »*. Le fond du mode
> sombre descend donc à **`#100D0B`** (« café noir subtil ») ; l'encre du clair ne bouge plus.
> Contraste mesuré : **15,34 : 1** sur la crème, exactement le 15,3 annoncé.
>
> **2 · LES TROIS BRUNS S'ÉTAGENT** — et la marche du bas a été creusée à la demande de Tom :
> ```
> encre du clair   #201908   L*  9,2    le texte du mode clair
> brun encre       #43291C   L* 19,5    trait et texte sur champ lilas  (était #3A241A, L* 16,7)
> brun surface     #6B4630   L* 33,4    corps d'une fiche tenue
> ```
> Marches : **10,3** puis **13,9** de L* (avec `#3A241A` la première ne valait que 7,5).
> Le **violet quitte le rôle d'encre** (le brun encre le prend, 6,62 : 1 sur le lilas) et le
> **vert quitte le rôle de surface** (le brun surface le prend — c'est la surface qui manquait
> au §3, Q217 : *« déclarée, pas encore employée »*). Sur le brun surface, crème Δlum **163,9**,
> amande **124,7**, encre 51,0 seulement : **l'encre s'inverse**, le corps d'une fiche tenue
> porte du crème et ses marques d'état l'amande, **dans les deux thèmes** (une surface
> d'exception ne bascule pas).
>
> **3 · « EN COURS » ET « TENU » DEVIENNENT SOMBRES, ET CHACUN GAGNE SA VALEUR CLAIRE.**
> ```
> en cours    #291547   (violet Promi, retenu)     ·  son clair : #FFD447
> tenu        #00341A   (vert profond)             ·  son clair : #8FE08F  (l'amande)
> à tenir     #DD4D23   inchangé — il lit dans les deux modes
> ```
> **Pourquoi il faut les deux :** le trait borne le CHAMP et le CORPS. Sur `#100D0B`, `#291547`
> et `#00341A` donnent **Δlum 15 et 26** — la moitié basse du trait s'éteint. L'amande le
> faisait déjà pour le tenu ; **il manquait l'équivalent pour l'en cours.**
> **Ce clair n'est pas inventé : c'est, dans les deux cas, LA VALEUR QUE L'ÉTAT REMPLACE.**
> L'amande `#8FE08F` était le « tenu » du 17 septembre ; le jaune `#FFD447` était l'« en cours ».
> Mesuré sur `#100D0B` : jaune **Δlum 197,5 · ΔE 108,5** · amande **187,4 · 94,1**. Et aucune
> collision : le jaune est à ΔE 109 du lilas, 114 du bleu, 80 du rose.
> ⚠ **Un transport fidèle du violet vers le clair était impossible** : `#291547` et le lilas
> Nuée `#C9A8F5` ont **exactement la même teinte** (309,4° contre 308,3°) — le transport donnait
> `#B9B0FF`, à **ΔE 8** du lilas, c'est-à-dire la Nuée.
>
> **4 · OÙ ÇA VIT DANS LE CODE.** Les deux clairs passent par les bascules `-txt` qui existaient
> déjà : `:root` = sombre (l'amande, le jaune), `.light` = clair (`#00341A`, `#291547`). Une
> règle qui peint un **aplat** prend la valeur fixe ; une règle qui peint une **marque d'état**
> prend le `-txt`. ⚠ **Et une marque suit CE QUI EST PEINT SOUS ELLE, pas le thème** : les
> pastilles de légende de l'Aura sont posées sur un plateau `#201908` **dans les deux modes** —
> elles gardent l'amande et le jaune en clair aussi.
>
> **5 · LA PALETTE PAR DÉFAUT EST LA PALETTE D'IDENTITÉ** — « Signal », vingt-et-unième et
> première du rail : bleu `#82AEF8` · rose `#FFB8D2` · lilas `#C9A8F5` · **crème dalle
> `#EFE3C7`** en quatrième (*« c'est une surface, pas un état, aucune règle ne s'y oppose »*).
> Primesautier reste dans les vingt. `_BPAL`, qui teinte les avatars des Noyaux, perd ses deux
> reliquats `#B586F6` et `#8CBCFD` et prend les quatre tons d'identité.

> **⚑ 17 SEPTEMBRE 2026 — LA PALETTE CHANGE DE VALEURS, ET LA NUÉE CHANGE DE RÔLE.**
> (Décision Tom, sur sa **planche des correspondances** et le **PDF des vingt palettes du Studio** —
> les deux font foi et remplacent les valeurs ci-dessous.) **Le bloc du 16 septembre qui suit reste
> pour l'histoire ; c'est celui-ci qui vaut.**
>
> ```
> LES NATURES — le champ dit la nature
>   bleu Promi      #3A54FF → #82AEF8
>   rose Chiche     #FA2258 → #FFB8D2
>   lilas Nuée      #D0B0FF → #C9A8F5     ⚑ C'EST LE CHAMP D'UNE NUÉE (voir ci-dessous)
> LES ÉTATS — la ligne dit l'état
>   à tenir         #DD4D23              (inchangé depuis le 16 sept.)
>   en cours        #8FA0FF → #FFD447     le périwinkle passe au JAUNE
>   tenu            #2BE88C → #8FE08F
> FONDS, ENCRE, SURFACES
>   fond clair      #F7F0DE              (inchangé)
>   fond sombre     #201908              (inchangé) — et c'est l'encre du mode clair
>   violet Nuée     #291547              ⚑ TRAIT ET TEXTE SUR CHAMP LILAS (voir ci-dessous)
>   encre profonde  #120E05              le FOND D'ÉCRAN sombre — distinct du fond du mode
>   vert profond    #06231A → #00341A     corps d'une fiche tenue, surface d'exception
>   orange d'origine          → #F07A2E   accent secondaire, célébration
>   crème panneau   #F3E7D1 · crème bordure #E4D7BB · crème dalle #EFE3C7
>   gris texte sombre #A2947C · gris chaud clair #6E6350 · lavande pâle #E6D8FA
> ```
>
> **⚑ LA NUÉE : LE LILAS EST LE CHAMP, LE VIOLET EST CE QU'ON POSE DESSUS.** (Tom, 17 sept. 2026 :
> *« Les trois natures sont des pastels : la Nuée ne peut pas être la seule avec un champ sombre.
> Et le violet garde son rôle — il est au lilas ce que l'encre est au bleu et au rose. »*)
> **C'est un échange de RÔLE, pas une valeur qui bouge.** Ce document écrivait l'inverse — « mauve
> #291547 une Nuée », et la table des corps de fiche donnait la bande d'une Nuée en violet.
> **Lire désormais : bande et champ d'une Nuée = lilas `#C9A8F5` ; trait et texte posés dessus =
> violet `#291547`.** Le corps clair (`#F3E9FE`) et le corps sombre (`#1B1426`) ne bougent pas.
> ⚠ **La barre Peaufiner d'une Nuée n'est PAS posée sur son champ** : elle prend le corps mauve
> `#291547` (chantier G), dans les deux thèmes — son texte y reste crème (Δlum 79,7 ; le violet y
> donnerait 0). Mesuré, pas supposé.
>
> **⚑ LE TEXTE POSÉ SUR UN CHAMP PASSE À L'ENCRE `#201908`.** (Tom, 17 sept. 2026.) Les champs sont
> devenus pastels : le crème y tombe à **Δlum 12,9** sur le Chiche et **24,2** sur le Promi, là où le
> §3 exige 42. Avec l'encre : **72,8** et **61,6**. Ça vise le mot-marque, le ✕ FERMER, la barre
> Peaufiner, **tout ce qui se pose sur un champ**. Contrôlé par `scratchpad/sonde_champ.py`, qui ne
> devine aucun sélecteur : il remonte au premier fond opaque depuis chaque texte.
> ⚠ **Le revers n'est PAS réglé :** le texte écrit **en couleur de nature sur le corps crème** tombe
> lui aussi sous 42 (31 textes mesurés, mode clair seulement) — QUESTIONS · **Q221**.
>
> **⚑ LES VINGT PALETTES DU STUDIO REMPLACENT LES DIX.** Quinze claires, cinq sombres, l'ordre
> C1 ≈ 34 % → C2 ≈ 28 % → C3 ≈ 23 % → C4 ≈ 15 %. Primesautier · Candide · Gouailleur · Alangui ·
> Irascible · Hurluberlu · Béat · Minaudier · Chafouin · Frivole · Cajoleur · Allègre · Lunatique ·
> Flegmatique · Narquois · Fielleux · Sibyllin · Vénéneux · Atrabilaire · Taciturne.
> **⚑ 23 SEPT. 2026 — TROIS DE PLUS, ET LA GRILLE SE FERME** (Tom : *« il reste la place pour trois
> palettes »*) : **Truculent** `#FF3E00 #00E5FF #5600D6 #F6FF00` · **Pétulant** `#FF8A00 #6800E0
> #00C85A #FFAAC8` · **Fantasque** `#00FF8C #E60073 #0040FF #FFF7DE` — pop, fluo, posées avec les
> claires (avant Fielleux). 24 pastilles = **quatre rangées de six**. Mesurées comme les autres
> (ΔE 2000) : écart interne **48,3 · 38,0 · 28,5** (le jeu : 13,0 à 37,8) ; distance à la plus
> proche **17,1 · 17,8 · 16,6** (le jeu : 9,2 à 20,7, médiane 16,9) ; entre elles **20,5 à 23,5**.
> Garde-fou du sol repassé : **0 sous 42 sur 48 mesures**. Q278. Leur nom paraît
> sous la rangée, en Gilbert 12 px capitales (vingt noms sous des orbes de 40 px ne tiendraient qu'en
> 9 px — sous le plancher du §6). Défaut : ~~**Primesautier**~~ *(historique — le défaut est **Ingénu**, clé `signal`, depuis v17 : voir §4)*, à la place de « Signal ».
>
> **⚑ ET CE QU'AUCUNE PASSE HEXADÉCIMALE NE VOIT : LES TABLEAUX DE TRIPLETS.** 47 tableaux `[r,g,b]`
> en JavaScript — `NAT` (la Pelote), `SPECTRE`, `GPIX·GBRA·GLI·GMOS·GENC·GLIGHT` (les
> rampes de fond de la Toile), `SIG`, `ETATS`, `KC`, les grappes. Ils portaient encore l'ancienne
> identité **un mois après sa bascule** : c'est ce qu'on voyait « sur la sphère et sur les dalles ».
> **Une bascule de palette se termine par un audit qui cherche chaque ancienne valeur en hexadécimal,
> EN TRIPLET et en `rgb()`** — sans quoi la conversion est fausse et paraît juste.

> **⚑ LA PALETTE A CHANGÉ DE VALEURS LE 16 SEPTEMBRE 2026 — AUCUNE SYMBOLIQUE N'A BOUGÉ.**
> (Décision Tom, avec sa planche des deux modes.) *« Chaque couleur garde son rôle, seule sa
> valeur bouge. »* Cinq mouvements, et deux entrantes :
>
> ```
> l'orange      #F07A2E → #DD4D23   même fonction d'accent, pastilles et états.
>                                   ⚠ À ÉVITER POUR DU TEXTE (mesuré : Δlum 42 sur la crème,
>                                   43 sur le brun — il est AU seuil, jamais au-dessus).
> le clair      #F4EEE1 → #F7F0DE   le FOND du mode clair
> le mauve      #8A5CF0 → #291547   symbolique inchangée (mais il est devenu SOMBRE, L* 12)
> le brun       (entrant) #201908   le fond du mode SOMBRE — c'est l'encre du mode clair :
>                                   les deux modes s'échangent, rien d'autre ne bouge
> le vert       (entrant) #00341A   surface d'exception — DÉCLARÉE, pas encore employée
>                                   (aucune surface ne lui a été donnée : QUESTIONS · Q217)
> ```
>
> **Les dérivés suivent leur ancre**, transportés en CIELAB : la teinte suit en plein, la
> clarté et la chroma à proportion de la proximité (sans ce poids, le corps sombre « à tenir »
> #2E1C13 tombait à L* 1 — noir). **Trois valeurs sont des ajustements EXPLICITES, pas des
> transports**, parce que le fond sombre est devenu brun et le mauve très sombre :
> `#2E1C13 → #401E17` (corps sombre « à tenir », ΔE au fond 15,1 → 16,6) ·
> `#2A1912 → #3A1B15` (gardé de côté, 13,3 → 14,7) ·
> `#271B45 → #1B1426` (corps sombre d'une carte de Nuée : il tombait à **ΔE 6,2 de son propre
> champ** — descendre en clarté ne suffit pas à teinte égale, il faut SOURDIR ; on prend donc
> le corps sombre de Nuée que ce document donne déjà).
>
> **⚠ DEUX RÔLES SOUS UNE MÊME VALEUR — #12142A.** Le fichier l'employait pour « le CORPS DU
> THÈME — #F4EEE1 en clair, #12142A en sombre » (plateaux, recherche, tri, Langue,
> Confidentialité, Cercle, partage) **et** pour le corps de fiche d'un Promi. Le premier est un
> FOND : il est passé au brun. Le second est une NATURE : il n'a pas bougé. **On sépare au
> sélecteur, jamais à la valeur.**
>
> **⚠ CE QUE LA NOUVELLE VALEUR A CASSÉ, ET QUI EST OUVERT.** La ligne « à tenir » posée sur un
> champ PLEIN de nature tombe sous le seuil du §3 : **Δ14 sur le champ Promi** (elle était à
> Δ51), **Δ21 sur le champ Chiche** (elle était à 58). Mesuré sur la fiche, la carte d'Index, le
> bandeau du Fil et l'instant, dans les deux thèmes — `redteam_tonsurton` le prend 8 fois.
> **Ce n'est ni un bug de juge ni une erreur de bascule : c'est la valeur décidée qui rencontre
> la règle des 42.** En ΔE l'orange reste franc sur le bleu (140) ; c'est la LUMINANCE qui
> manque. Rien n'a été touché : QUESTIONS · **Q216**.

### ⚑ 23 SEPTEMBRE 2026 (v34) — TOUT SUIT LE STUDIO, SAUF L'AURA. (Décision Tom — elle RENVERSE le « figé à la création » ci-dessous.)
> *« Tout suit le Studio — le Fil, l'Index, la Toile, la Toile du Cercle, les fiches, la page +, Partager. Ils prennent le monde
> et la palette sélectionnés. Seule exception : l'Aura. La Pelote et la liste sous « Ce que tu as tenu » gardent le monde et la
> couleur de plantation. »* Dans le moteur, le monde de plantation n'est plus le défaut de `dalleTrame` : il se DEMANDE
> (4ᵉ argument explicite, ou `opts.plantation`) — seule l'Aura le fait. La palette qui décide d'Ingénu est celle du Studio
> (`_ingenuRampe(id, haut, plantation)`). Juges réécrits au niveau de la décision : `redteam_decoupe` famille H,
> `redteam_dalle_figee` D (originaux `sauvegardes/*-avant-v34.py`). Les ÉTATS, eux, ne suivent toujours rien.

### ⚑ 27 SEPTEMBRE 2026 (v61) — UN MOUVEMENT DE MONDE SUIT L'HORLOGE. EXCEPTION : HOULE.
> (Décision Tom.) *« Ce n'est pas un changement de rythme : à 60 images par seconde, rien ne bouge. C'est ce qui garantit que
> la durée validée tient sur un iPhone lent. »* Tesselle, Braille, Buvard, Éclisse, Taille-douce rejoignent Pochade et Touffe :
> leur ressort est calculé sur le temps (`1 − 0,83^dt`, `1 − 0,78^dt` = 0,17 et 0,22 à 16,67 ms). Les mondes neufs (Madrure,
> Halin, Esquille, Ritournelle, Bobinette) intègrent le temps VRAI en sous-pas de 1/60 s (ils plafonnaient à 50 ms et
> comptaient toute image de plus de 100 ms pour 1/60 s). Un redémarrage de la boucle fait toujours UN pas (`frame._redem`).
> **⚑ EXCEPTION ÉCRITE — HOULE (`sillons`) RESTE PAR IMAGE** : elle tourne à ~30 i/s sur la page validée ; à l'horloge elle
> deviendrait plus rapide que ce que Tom a validé. Elle s'étire sous charge, par décision. `redteam_rythme` le vérifie.
> **Ce qui a bougé à 60 i/s, et seulement ça : Halin, −105 ms à l'arrivée, −147 au départ** — ses propres accrocs (images de
> 100 ms et plus) lui faisaient perdre du temps en v60. Tous les autres : identiques (A/B, pages fraîches, vrai GPU).
> ⚠ **Madrure a deux chemins** : le GPU (Chrome, iPhone) et un SECOURS processeur (construction par tranches) quand WebGL refuse
> (`failIfMajorPerformanceCaveat`) — c'est ce que tous les bancs mesuraient jusqu'ici. **Un banc Chromium se lance avec le vrai
> GPU** (`--use-angle=metal --enable-gpu --ignore-gpu-blocklist`) ; WebKit l'a déjà.

### ⚑ 30 SEPTEMBRE 2026 (v102) — L'AGRANDISSEMENT DES TEXTES (v96) : PERTES D'AIR ASSUMÉES, AVEC LEURS VALEURS.
> (Décision Tom : *« On accepte la perte d'air. Ne fais pas défiler la page +, et n'agrandis aucun bloc à hauteur fixe. Ces écrans ont été
> composés pour tenir en un écran, et quelques pixels valent mieux qu'un défilement sur l'écran où l'on plante. »*) Mesuré à l'ENCRE
> contre la référence d'avant v96 (`sauvegardes/air-encre-avant-v96.json`) ; ces écarts sont VOULUS — ne pas les « corriger » :
> ```
> rail du pinceau (règle du mi-chemin)   page + : consigne → rail −8,5 · rail → barre −10,5
>                                        page + d'une Nuée : phrase → rail −10 · rail → barre −13   (vu à l'œil : lisible, rien ne se touche)
>                                        gardé de côté : mot → rail −6 · rail → « garder » −7 · rail → barre −8 · « garder » → barre −4
> cartes de l'Index et du Fil            sur-titre → titre, titre → état : −3 à −4 (un titre passé à deux lignes : « faire les crêpes »)
> cartes du Peaufiner d'une Nuée         libellé → aide −2,7 · aide → note −3,2 · note → libellé suivant −4
> tête du Peaufiner                      titre → « LE TRAIT » −3 · « ✕ FERMER » → valeur −2
> Réglages                               une rangée → la suivante −2 à −3,5 · « ✦ Le Cercle » → « Le Studio » −3
> Partager                               « Ma Toile · Story » → « Inviter » −3,5
> plateaux                               « ✕ FERMER » → tri (Index, Fil) −1,5
> ```
> **Décisions, pas des dérives** : le titre du Fil (−3,6, recentrage v97), l'aide de l'Aura (−4,1) et la page + d'un Chiche / d'une Nuée
> (−3) — même recentrage des titres ; les valeurs des Réglages (−1,5, v98). **Rendu, lui** (v101–v102) : colonnes des fiches, de
> l'instant et de la Nuée, cartes du fil d'une Nuée, consigne et phrase de la page +.

### ⚑ 30 SEPTEMBRE 2026 (v104) — LES MURS DU CERCLE : UN FLOU, PAS D'EXPLICATION, UNE PHRASE QUI MONTE.
> **⚑ v105 (Tom, le même jour) — LA PHRASE EST REPRISE :** plus de plateau (*« pas dans la DA, ça fait bon marché »*) ; elle s'affiche **au
> centre du mur touché, sur le flou, seule** — pas d'encart, pas de bandeau, pas de fond, pas de cadre ; **en gros** (34 px, réduite jusqu'à
> tenir en **trois lignes** et dans la hauteur visible du mur), **encre `#201908` sur clair, crème `#F7F0DE` sur sombre**, une seule taille ;
> elle reste **le temps d'être lue** (1,4 s + 60 ms par caractère, entre 3 et 5,5 s) puis s'efface ; la toute première fois l'offre s'ouvre
> à la fin de cette lecture. Le flou : **4,8 px partout** (Aura, aide, Réglages, les trois Peaufiner) — *« on ne donne pas ce qu'on vend »* ;
> **le Studio garde le sien** (*« on doit voir le monde pour avoir envie de l'acheter »*). La porte des Réglages s'appelle **« Ma Parole ! »**.
> **« Arranger la Toile » est SUPPRIMÉ** (v105, Tom : *« on n'en veut pas »*) — la pastille, l'icône, la fonction, la feuille ; le moteur
> de la Toile est rendu à l'identique.
> (Décision Tom.) *« Les encarts qui disent LE CERCLE disparaissent. Un réglage verrouillé est simplement flouté, sans explication. Quand
> on touche un mur, une phrase monte du bas et reste. Ensuite, toucher n'importe où ouvre la page de l'offre. Sauf la toute première
> fois : la page s'ouvre automatiquement. »* Et : *« deux fois plus flou — on veut plutôt illisible »* → **un seul flou pour tous les
> murs du gratuit : 4,8 px**, **SAUF LE STUDIO, qu'on ne touche pas** (ses flous et son « Adopte ce design — 1 € » restent).
> Les 21 phrases (lot-V104-MURS, `window._murPhrases`) s'enchaînent dans l'ordre sur un compteur **GLOBAL** (`promi_murs`, toutes zones,
> par personne), puis au hasard sans répéter la précédente ; remise à zéro après 14 jours sans mur (Q352, à valider). **« Ma Parole ! »**
> est le nom neuf de l'offre — **seules ces phrases l'emploient** (renommage complet : un lot à venir) ; il y porte l'orange d'accent
> secondaire, le reste de la phrase la couleur d'accent. La porte des Réglages (« ✦ Le Cercle ») n'est pas un mur : elle reste.

### ⚑ 29 SEPTEMBRE 2026 (v98) — UNE TOILE TIENT UN NOMBRE ILLIMITÉ DE PAROLES, ANCIENS MONDES COMPRIS. (Décision Tom.)
> *« Une parole qui n'apparaît pas est inacceptable — la décision v35 valait pour l'aspect, pas pour perdre des paroles. »* Les huit anciens
> gardent leur semis constant TANT QU'IL Y A UNE CELLULE VIDE ; plein, `sync` ajoute une cellule (`_celluleEnPlus`). Leur aspect ne change
> qu'au-delà (~50 paroles). **Les titres sur la Toile s'effacent quand la dalle n'a pas 48 px à l'écran** — on zoome pour lire (Tom : « illisibles
> à 200-500, c'est normal ; vérifie qu'ils disparaissent proprement »). Banc : `scratchpad/infini.py`, `ligne500.py` (WebKit).

### ⚑ 23 SEPTEMBRE 2026 (v35) — INCOHÉRENCE ASSUMÉE : LE SEMIS QUI GRANDIT NE VAUT QUE POUR LES QUATRE MONDES NEUFS.
> (Décision Tom, qui **corrige** le bloc v34 ci-dessous : « c'était une exception pour les quatre neufs seulement ».)
> **Pochade, Tesselle, Touffe, Braille, Buvard, Houle, Taille-douce, Éclisse** gardent le semis CONSTANT d'origine
> (≈ 68 cellules, les promesses colorent des cellules du semis, le recul cadre les colorées) et leur aspect d'origine.
> **Esquille, Bobinette, Ritournelle, Madrure** ont une Toile faite de ses seules promesses.
> **La raison** : les huit anciens ont été dessinés, réglés et validés sur le semis constant (leurs taches, fleurs et
> éclats se règlent sur l'écart entre graines — à 6 promesses la Touffe faisait des fleurs énormes) ; les quatre neufs ont
> été conçus pour une Toile qui grandit (PDF « la toile grandit »).
> **Ce que ça coûte, et il faut le savoir :** changer de FAMILLE au Studio ressème la Toile (`setTheme` → `sync`) ; une
> dalle peinte dans un monde de l'autre famille (l'Aura, qui garde le monde de plantation) est calculée sur le semis EN
> PLACE, pas sur celui de sa famille ; la rampe des îles de la Pelote dépend du semis en place (0,85 / 1,4).
> Où ça vit : `_NEUFS`, `_semisNeuf()`, `_semisDe`, `Toile.semisNeuf()`.

### ⚑ 23 SEPTEMBRE 2026 (v34) — LE SEMIS GRANDIT AVEC LES PROMESSES. (Décision Tom.)
> *« Une Toile à six promesses a six cellules, pas quarante dont trente-quatre seraient vides. »* Mesuré avant : **68 graines
> à 6, 20 et 40 promesses** — un semis fixe dont les cellules se coloraient, cadré par le recul. Désormais la Toile est faite
> de ses promesses et de ses Nuées (`sync`, `addPromi`, `_auVide` : une graine neuve au plus grand vide, tirée de
> `Toile.cle()`), vue entière. **Seule la Toile SANS promesse garde le semis de graines du §10.6.** Conséquences : la matière
> d'un monde ne peut plus se régler sur l'écart entre graines (`env.uMat`, unité fixe — CONTRAT-MONDE §15.6) ; presque toutes
> les cellules touchent le bord, leur dalle s'arrête au bord de la Toile. `Toile.graines()` rend le compte.

### ⚑ LA FRONTIÈRE STUDIO / ÉTAT — ce qui suit la palette, et ce qui ne la suit jamais

> **Décision Tom, 20 septembre 2026.** *« La sphère rejoint ce qui suit la palette du Studio,
> avec les dalles de la Toile et la Toile de l'écran du Cercle. Son sol prend la palette. Mais
> les dalles gardent leur monde et leur couleur de plantation […]. Une dalle est figée à sa
> création, partout où elle paraît. Et la légende, les arcs des Noyaux et les traits d'état ne
> suivent jamais le Studio. Ce sont des états : le vert n'est « tenu » que parce qu'il est
> toujours vert. »*

**Trois familles, et elles ne se mélangent pas :**

```
SUIT LE STUDIO — ce sont des SURFACES
   la Toile · la Toile de l'écran du Cercle · LE SOL DE LA SPHÈRE (le ton dominant, C1)

FIGÉ À LA CRÉATION — ⚑ RÉDUIT PAR v34 (23 sept.) À L'AURA SEULE : les ÎLES de la Pelote et les dalles de
   « Ce que tu as tenu » gardent le monde et la couleur de plantation. PARTOUT AILLEURS (Toile, Index, Fil, fiches,
   page +, Partager, Toile du Cercle) la dalle suit le Studio. *(historique : « partout où elle paraît »)*

NE SUIT JAMAIS RIEN — ce sont des ÉTATS, et un état qui change cesse d'être un signal
   la légende de l'Aura · les arcs des Noyaux · les traits et les libellés d'état
```

**Comment on le VÉRIFIE, et c'est une mesure, pas une lecture :** on rend l'écran sous deux
palettes très éloignées et **on regarde ce qui bouge**. Ce qui doit suivre bouge, le reste est
identique au pixel. Relevé le 20 septembre, Signal contre Irascible contre Allègre :
le sol bouge de **ΔE 42 et 33** ; les pastilles, les arcs et les empreintes des dalles rendent
**une seule valeur distincte sur trois palettes**. Sonde : `scratchpad/frontiere.py`.

**⚠ CE QUE LA DÉCISION COÛTE, ET IL FAUT LE SAVOIR AVANT DE TOUCHER AU SOL.** L'écart boule ↔
page n'est plus une constante : il devient une **conséquence de la palette**. Balayé sur huit
palettes (`scratchpad/balaye_sol.py`), en mode sombre il va de **10,4** (Taciturne) à **156,2**
(Primesautier) — sous les deux palettes les plus sombres, **la boule se fond dans la page**.
La calibration de Q210 (`SOL_CLAIR` 0,38, `SOL_CREME` 0,39, plancher des îles ΔE 15) avait été
mesurée sur le bleu de la nature : elle ne garantit plus rien sur les vingt autres palettes.

> **⚑ 23 SEPTEMBRE 2026 — SUR UN FOND SOMBRE, LE TENU EST L'AMANDE.** (Décision Tom, elle
> **corrige** les blocs du 22 septembre.) *« Les textes en vert sombre sur les Promi et Chiches
> tenus ne se lisent pas sur le pourpre du fond. Tout ce qui est en vert sombre sur pourpre, tu
> le mets dans le vert amande — mode clair comme sombre, puisque le fond pourpre ne change pas. »*
> Mesuré : `#00341A` sur la terre `#2B1020` → **Δlum 11,3** ; l'amande `#8FE08F` → **190,6**.
> **Ce n'est pas « l'amande revient partout »** — c'est la doctrine du §3 appliquée : une marque
> suit **ce qui est peint SOUS elle**. Sur un fond clair, le tenu reste `#00341A`.
> **Et « TENUE » se marque en amande** — *« ce vert amande est beau et rare, donc célèbre »*.
> ⚠ **« Un peu gras » ne peut pas être une graisse** : Gilbert n'en a qu'une (§6). On appuie par
> la chasse et la taille, jamais par un `font-weight` qui ne peindrait rien.
>
> **⚑ 21 SEPTEMBRE 2026 (v18, Tom) — LE FILET NE SUIT QUE LE BORD EXTÉRIEUR DE CHAQUE SEGMENT, ET S'INTERROMPT DANS
> LES ÉCARTS. 1 px.** Jamais le bord intérieur, jamais les bouts, jamais un cercle continu — partout où un disque paraît,
> l'anneau du + compris (segments nets, plus de fondu). Les paragraphes qui suivent décrivent l'état d'avant. QUESTIONS · Q298.
> **Et la mention TENU est en amande** (« TENUE », « TENU À DEUX · 3 AOÛT ») : c'est l'autre usage de l'amande, avec la célébration.
>
> **⚑ ET UN FILET CRÈME CERNE CE QUI EST SOMBRE SUR DU SOMBRE.** Un filet de **1,4 px `#F7F0DE`**
> cerne **tout anneau posé sur un fond sombre** (la terre d'une fiche dans les deux thèmes, le brun
> du mode sombre dans l'Aura) **et court sous le trait d'une parole tenue**, à la jonction de la
> crête `#0B4A2A` et de la terre — mesuré Δlum **15,7**, sous le seuil du §3.
> **⚑ 23 SEPTEMBRE 2026, CINQUIÈME ÉCRITURE — LE FILET SE COLLE AU BORD DE L'ANNEAU, PAS À CELUI
> DE SA BOÎTE.** (Tom : *« il y a un écart — sur le Noyau autour du + de l'accueil, et partout
> ailleurs. Il cerne le bord, sans jeu. »*) **Deux fois la même faute : une cote calculée sur une
> géométrie qui n'est pas celle de l'objet.** ① l'`outline-offset:3px` du **+** avait été pris sur
> `.dhero::before{inset:-3px}`, la règle GÉNÉRALE — mais sur l'accueil `#device .acc-barre
> #createBtn::before{inset:0!important}` gagne : offset **0**. ② `drawKRing` posait le sien à `W/2`,
> le bord du CANEVAS ; avec les constantes globales l'anneau s'arrête à **0,4069·W** — mesuré sur un
> Noyau de 104 : **8,2 px de jeu**, ramenés à **0,5**. Le filet suit désormais le bord PEINT
> (`_krDehors`), borné au canevas.
> ⚠ **Et la passe `_filetsDisques` était un SECOND PROPRIÉTAIRE** (§7) : elle repassait au bord du
> canevas après le peintre. Elle lit maintenant la cote que le peintre **déclare** (`data-filet`).
> **Les Noyaux SVG (`.au-nb`) ne bougent pas** : leur filet est à `D/2 − 0,7`, l'arc finit à `D/2`
> — jeu **−1,4**, il occupe les 1,4 derniers pixels de l'anneau. Zéro jeu, et il reste DANS la
> boîte, seule écriture qui survive à `.au-nx`. Sonde : `scratchpad/s26/disques.py`.
>
> > ⚠ **Le filet d'un anneau vit sur le NŒUD, jamais dans le canevas** : peint dans le canevas il se
> fait recouvrir par la passe suivante, et il ne peut pas dépendre d'une CLASSE (`drawKRing` est
> appelé 8 à 12 fois par ouverture, les premiers appels précèdent la pose de la classe). Le bord
> extérieur d'un anneau EST le bord de sa boîte : un `box-shadow` le cerne au pixel.

### Les fonds, l'encre et les surfaces (repris le 30 sept. 2026)

```
#F7F0DE   crème            le FOND du mode clair
#100D0B   café noir        le FOND du mode sombre (v7, 20 sept.)
#201908   brun             l'ENCRE du mode clair (15,34 : 1 sur la crème)
#43291C   brun encre       trait et texte sur un champ lilas
#2B1020   terre (prune)    le SOL d'une fiche tenue, dans les deux thèmes ; crête #0B4A2A
les natures et les états : voir « Les couleurs signal » ci-dessus — un ÉTAT ne peint jamais un fond
```
*(historique — la table qui était ici, « menthe #2BE88C tenue · #3A54FF création · periwinkle en cours · #201908 fond
sombre », est morte : elle mélangeait des natures et des états sous le titre « fond ».)*

> **⚑ TOUT PASSE PAR LE JEU — `PROMI-TOKENS.json`.** (Tom, 16 septembre 2026 : *« Centralise
> tout : un jeu de couleurs nommées avec variantes claire et sombre, et une extension de styles
> pour qu'aucune vue n'appelle une police ou un hexadécimal en dur. C'est ce qui servira au
> portage Swift. »*) **Trois fichiers, et ils se régénèrent, ils ne s'écrivent pas :**
>
> ```
> PROMI-TOKENS.json      la source unique — 28 rôles, 7 niveaux de texte, 234 couleurs fixes
> app.html · lot-TOKENS-css   le bloc que l'app lit — mêmes valeurs, engendré depuis le JSON
> Promi+Design.swift     l'extension de styles du portage — engendrée depuis le même JSON
> ```
>
> **DEUX NIVEAUX DE VARIABLES, ET L'ORDRE COMPTE :**
> `--c-*` la palette **FIXE**, une valeur par couleur : **c'est ce que les règles emploient**.
> `--p-*` les **RÔLES**, qui basculent avec le mode : c'est ce que le portage Swift emploie.
> **Une règle ne doit JAMAIS employer un rôle à la place d'une valeur fixe** : le produit peint
> souvent la crème en mode sombre et l'encre en mode clair (`.acc-plat` en donne l'exemple), et
> un rôle les inverserait — en silence, sur des dizaines d'écrans.
>
> Contrôlé par **`redteam_tokens.py`** (19 contrôles, sans navigateur) : les valeurs décidées
> sont écrites EN DUR dans le juge, les deux modes s'échangent vraiment, **aucune couleur en dur
> dans un `<style>`** (0 sur 3 292), aucune police appelée en dur, et le JSON, le bloc CSS et
> l'extension Swift disent la même chose.

### Les corps de fiche — la bande porte la NATURE, jamais l'état (direction Horizon)

> **⚠ RÈGLE CORRIGÉE (décision Tom, direction Horizon — le moodboard `promi-moodboard-H.html`
> fait foi et remplace l'ancienne règle « couleur d'état pleine »).**
> **La bande haute porte la couleur de la NATURE, jamais celle de l'état.**
> Promi **bleu #82AEF8** · Chiche **rose #FFB8D2** · Cercle **lilas #C9A8F5** — quelle que
> soit l'échéance *(valeurs d'aujourd'hui ; en août : #3A54FF · #FA2258 · #8A5CF0)*. **L'état vit dans la LIGNE (le trait), et nulle part ailleurs.** Raison : si
> la bande virait à l'orange quand l'échéance approche, la nature disparaîtrait de l'écran au
> moment où elle compte le plus. Le champ dit la nature, la ligne dit l'état — c'est la loi de
> tout le document, sans exception. **La célébration** (repris le 30 sept. 2026, décision v8 du 21 sept.) :
> quand une parole est tenue, une seconde dalle de la même forme apparaît sous la première, en
> **amande #8FE08F**, se décale, puis disparaît ; la fiche tenue a pour sol la **terre #2B1020**.
> *(historique — août : « le champ entier passe au menthe ».)*

Une fiche a **deux tons**. La **zone haute** (la bande) est en **couleur de NATURE pleine**.
Le **corps**, celui qui porte le contenu, est **plus clair**. C'est la respiration de la fiche :
la matière en haut, la parole en bas. Ce n'est **ni un voile ni un dégradé — deux aplats
francs**. La dalle du haut reste **nette, opacité 1**.

```
                bande (nature)   corps clair   corps sombre     (PROMI-TOKENS.json, repris le 30 sept. 2026)
Promi           #82AEF8          #CFE5FE       #0D1F33
Chiche          #FFB8D2          #FFF4FC       #201221
Cercle          #C9A8F5          #EEE4F8       #1B1426
tenue           (sa nature)      terre #2B1020 dans les deux thèmes — texte crème, marques d'état en amande
```
> **⚑ v122 — CE TABLEAU ÉTAIT FAUX SUR DEUX COLONNES** (mesuré à l'écran, v118 comme aujourd'hui) : le corps CLAIR d'une fiche est la
> **crème `#F7F0DE`** (Tom, Q221 : *« sur le corps crème »*) — `#CFE5FE` · `#FFF4FC` · `#EEE4F8` sont des jetons qui ne peignent pas
> le corps ; le corps SOMBRE est celui de v113 (Q358) : **`#335382` · `#7C3F58` · `#5D4978`** (le Cercle : valeur posée par v113, pas
> une citation de Tom).
> **⚑ v131 — le corps sombre d'un PROMI est le cobalt `#273CEB`, texte crème (Tropical Breeze, v130, est écarté) ; Chiche et Cercle ne bougent pas.**

**Le contenu du corps passe en encre** (le moodboard le pose en blanc sur couleur
pleine ; sur un corps clair ce serait illisible). **Tout texte posé sur un champ pastel passe à
l'encre `#201908`** (17 sept. : mot-marque, ✕ FERMER, barre Peaufiner). Les valeurs rgba ci-dessous
sont *(historique)* — l'encre d'alors était `#06231A` ; elles vivent aujourd'hui dans le jeu de jetons :

```
texte du corps              #06231A (ou l'encre de l'état)
fond de la carte message    rgba(6,35,26,.1)    (au lieu de rgba(255,255,255,.15))
filet sous la carte         rgba(6,35,26,.2)    (au lieu de rgba(255,255,255,.24))
contour des pastilles       rgba(6,35,26,.26)   (au lieu de rgba(255,255,255,.34))
panneau du geste            rgba(6,35,26,.1)    (au lieu de rgba(255,255,255,.14))
filet de la barre           rgba(6,35,26,.24)   (au lieu de rgba(255,255,255,.3))
```

**La zone haute et ses éléments — mot-marque, FERMER — portent l'encre `#201908` sur le champ pastel**
(17 sept. ; en août : blanc sur couleur pleine). Le bitonal est **la seule exclusion** au
« moodboard à la lettre » pour la fiche : tout le reste (structure, hauteurs,
tailles, carte message, pastilles, tracé) tombe à zéro.

### ⚑ UN TRAIT SUR UN APLAT COLORÉ SE JUGE EN ΔE, PAS EN LUMINANCE — Q216, tranché

> **Décision Tom, 18 septembre 2026 :** *« Juge en ΔE, pas en Δlum, comme le §7 le fait déjà pour
> la Pelote. Sur un aplat coloré, c'est l'écart de couleur qui compte. »*

**Le seuil de 42 en LUMINANCE garde son objet — du TEXTE sur un fond.** Il ne vaut plus pour une
LIGNE posée sur un aplat de couleur : là, le plancher est **ΔE 15** (celui de la Pelote, §7).

**Pourquoi, et c'est mesuré, pas supposé.** Depuis que les champs sont pastels, **aucune ligne d'état
n'atteint 42 en luminance sur aucun champ** — et elles se voient toutes :

```
                    Δlum      ΔE                          Δlum      ΔE
  à tenir / Promi   18,0    107,8      à tenir / Chiche   29,2     67,5
  tenu    / Promi   11,7     87,2      tenu    / Chiche    0,5     78,3
  en cours/ Promi   15,7    114,0      à tenir / Nuée     21,5     93,4
```

**Le cas qui tranche, relevé sur l'image rendue** (`redteam_tonsurton`, les deux thèmes) : le trait
menthe `#8FE08F` d'une parole tenue sur le champ rose `#FFB8D2` d'un Chiche — **Δlum 0, ΔE 78,3**.
Même clarté exacte, teintes opposées. On le voit sans effort sur toute capture de l'Index ; un seuil
de luminance seul l'aurait déclaré ton sur ton.
**La luminance n'est pas abandonnée : elle est REPORTÉE à côté**, parce qu'elle attrape autre chose —
un trait juste en teinte mais noyé en clarté. Elle ne fait plus échouer seule.

### Les traits *(historique — remplacé)*

*Repris le 30 sept. 2026.* La règle qui était ici — « la teinte de la dalle décalée de 150°, saturation 55 % » — et
son « point ouvert » sont **morts** : depuis la direction Horizon **le trait porte l'ÉTAT** (à tenir, en cours, tenu),
et, posé sur un champ plein, il prend **la teinte SOMBRE de sa nature** (`NATTRAIT`, §2.1 bis corrigé ci-dessous).
Il se juge en **ΔE ≥ 15** sur son champ (Q216).

### ⚑ §2.1 bis CORRIGÉ — SUR UN CHAMP PASTEL, LA TEINTE QUI SE LIT EST SOMBRE

> **Décision Tom, 18 septembre 2026 :** *« Les teintes claires du §2.1 bis sont mortes — Δlum 1,6 sur
> le Promi, 5,0 sur le Chiche. Ce sont des compagnons dessinés pour des champs saturés qui n'existent
> plus. Recalcule-les sur les champs pastel. »*

**La règle ne bouge pas : le trait posé sur un champ plein porte une TEINTE DE SA NATURE, jamais la
couleur pleine du champ. Ce qui change, c'est le sens de l'écart.** Sur un champ saturé, la teinte
qui se lisait était plus CLAIRE ; sur un champ pastel, elle est plus SOMBRE.

```
            champ       avant  →  après       Δlum            ΔE
  Promi     #82AEF8   #C4A2F5  →  #022140    1,6 → 58,3    24,2 → 61,2
  Chiche    #FFB8D2   #F5AC9E  →  #3D0F23    5,0 → 69,6    21,8 → 69,8
  Nuée      #C9A8F5   #C9A8F5  →  #291547      0 → 61,8       0 → 62,3
```

**LA NUÉE MONTRAIT DÉJÀ LA RÉPONSE** — sa « teinte claire » était le VIOLET, un ton sombre. Et sa
valeur déclarée était `#C9A8F5`, **c'est-à-dire le champ lui-même** : le trait d'une Nuée avait
exactement la couleur du fond qu'il traverse.

⚠ **DEUX RÔLES VIVAIENT SOUS UN SEUL NOM.** `NATCLAIR` servait **le trait** (les deux thèmes) **et**
les libellés posés sur le corps SOMBRE. Le second a toujours besoin d'une teinte claire ; le premier,
de l'inverse. **On sépare au NOM, jamais à la valeur** — `NATTRAIT` est né, `NATCLAIR` garde les
libellés. C'est le même piège que `#12142A` au §3 et que les deux propriétaires du §7.

### Le trait sur le champ — TRANCHÉ (Tom, 18 août 2026)

**Le trait posé sur un champ plein porte TOUJOURS la teinte claire de la nature, jamais sa
couleur pleine** — c'est le §2.1 bis de `PROMI-SPECIFICATIONS.md`, et il fait loi.

**Les cadres clairs du moodboard qui peignent le trait en couleur pleine sont une ERREUR DE
DESSIN, pas une règle.** Vu en clair : le trait y prend exactement la couleur de l'aplat et
**disparaît**. Ce n'était donc pas une question ouverte (ancienne Q4) — c'était un défaut
du moodboard, et le document avait raison contre lui.

**Le seuil est celui du §3 : 42 de luminosité entre le trait et le champ qui le porte.**
Il vaut pour TOUS les traits du produit — fiche, page +, carte d'Index, bandeau du Fil,
encart de Nuée, l'instant — et il est contrôlé par `redteam_tonsurton.py`.

**Une Nuée** prend la teinte de **sa dernière dalle plantée** — ses traits
changent à chaque nouveau Promi.

### La règle de la couleur qui gagne sa place

**Un élément coloré ne reste que s'il porte du SENS ou une ACTION.** S'il ne fait que
décorer, il dégage — même s'il est joli. (Ex. lot 17 : l'anneau Aura reste, sa couleur
DIT quelque chose — proportions tenu/en cours/à tenir ; le rose des boutons commenter/
joindre est parti, il ne disait rien.) Corollaire du cadre **ÉVIDENT → SIMPLE → BEAU** :
un écran se lit d'un coup d'œil ; beau ≠ chargé ; un seul trait coloré qui sert vaut mieux
que cinq qui bruitent.

> **⚠ UN CHAMP BLANC N'EXISTE JAMAIS.** (Décision Tom, 29 août 2026, **sans exception**.)
> **Le champ porte toujours sa couleur pleine de nature** — bleu `#82AEF8` pour un Promi,
> rose `#FFB8D2` pour un Chiche, lilas `#C9A8F5` pour un Cercle *(valeurs d'aujourd'hui)* — **dans les deux thèmes
> et sur TOUS les écrans** : fiche, page +, carte d'Index, bandeau du Fil, Nuée, **gardé de
> côté**. **La dalle se pose dessus, jamais à la place.**
> **Ce qui manque à un gardé de côté, c'est la MATIÈRE, jamais la couleur** — Q83 le disait
> dans la même phrase : *« sa carte d'Index garde le champ de nature en pointillé, sans
> matière »*. Les cadres qui le dessinent sur le corps nu (26/27, 74) sont des erreurs de
> dessin, de la même famille que les cadres clairs au trait invisible.
> Contrôlé par **`redteam_champ.py`** : au-dessus du trait, aucun pixel ne porte une couleur
> de corps, aucun champ n'est transparent, et **chaque peintre DÉCLARE ce qu'il a versé**
> (`data-champ`) — seul juge possible sur une Nuée vide, dont les graines crème du §10.6
> tombent pile sur la couleur du corps.

### Interdits absolus sur les couleurs

- **Jamais de trait neutre ou gris.** Un filet sans couleur est un défaut.
- **Jamais de ton sur ton.** Un TEXTE sur un fond : écart de luminosité ≥ 42. Un TRAIT ou une matière sur un aplat
  coloré : ΔE ≥ 15 (Q216, §7).
- `-webkit-text-fill-color` doit **toujours** valoir la même chose que `color` —
  sinon le texte se peint dans la couleur du fond.
- Une marque suit **ce qui est peint sous elle**, pas le thème : sur la terre `#2B1020` d'une fiche tenue, le texte
  passe crème et le tenu en amande ; sur un champ pastel, le texte passe à l'encre `#201908`.
  *(historique : « #06231A sur menthe, #FFFFFF sur orange » — plus aucun aplat d'état n'existe.)*

---

## 4. Les dalles — règles absolues

**L'IDENTITÉ EN HAUT, LA DIVERSITÉ EN BAS.** La **bande du haut** porte l'identité
de la chose qu'on regarde — c'est une **couleur signal**, elle ne dépend JAMAIS du
contenu : une fiche de **Cercle** a une bande **lilas**, un **Promi** une bande **bleue**, un **Chiche** une bande
**rose** *(valeurs du §3 ; en août : mauve, bleu, et « Brouillon » terracotta — le gardé de côté porte le champ de sa nature, sans matière)*. Le **fil**, lui, porte les Promi, et
**chaque Promi garde son monde** (dalles variées — c'est ce qui le rend vivant, comme
la v592). Les deux règles cohabitent : la bande de Nuée est donc mauve même si ses Promi
sont d'autres mondes ; les dalles du fil restent leurs vraies dalles. Idem sur la
**page + Nuée** : la bande de création est mauve.

> **⚠ L'IDENTITÉ D'UN CERCLE (lilas aujourd'hui, mauve en août) PORTE SUR LA TEINTE, JAMAIS SUR LA FORME.** La bande d'une
> Nuée montre de **vraies dalles du moteur** (`Toile.dalleTrame`), **teintées mauve**
> — jamais des polygones/hexagones reconstruits. Reconstruire une forme de dalle est
> une violation frontale de la règle 1 (c'est l'erreur du lot 15, corrigée au lot 16).

> **⚠ LA DALLE PORTE LE MONDE. L'ACCENT PORTE LA NATURE.** (Décidé lot 25, vaut pour
> les trois natures — Promi, Chiche, Nuée.) Une **dalle n'est JAMAIS teintée par sa
> nature** dans les **listes** (Index, Fil) ni sur la **Toile** : la dalle appartient
> au **monde** choisi au Studio, jamais à la nature — c'est la diversité des dalles qui
> rend la Toile vivante, pas une couleur par catégorie. La **nature se lit à l'ACCENT** :
> pastille, libellé, contour, badge — **en framboise pour un Chiche**, bleu pour un Promi,
> mauve pour une Nuée. Sur la **Toile : rien**, on n'y touche pas (interdit §9).
> **Seule exception (déjà actée) : la BANDE HAUTE d'une fiche** est teintée par la nature
> — c'est là que l'identité s'affirme. Fiche de Cercle lilas, fiche Chiche rose, fiche
> Promi bleue *(août : mauve, framboise, bleu)*. Cette exception ne s'étend PAS aux listes ni à la Toile.

> **⚠ Q30 · LA TEINTURE EST BORNÉE À LA BANDE HAUTE.** (Décision Tom, 18 août 2026.)
> **Dans la bande haute d'une fiche et dans le champ de la page + — et NULLE PART
> AILLEURS — la dalle prend la palette de sa nature** (§1.2 de `PROMI-SPECIFICATIONS.md` :
> trois teintes par nature). Ce n'est pas une règle nouvelle : c'est **l'exception déjà
> prévue ci-dessus** — la bande haute est teintée par la nature, c'est là que l'identité
> s'affirme — poussée jusqu'à la dalle qu'elle porte.
> **Pourquoi c'est obligatoire là :** une dalle bleue sur un champ bleu est un **bug**, pas
> un parti pris. Mesuré sur les huit cadres à champ `#3A54FF` de la page + : écart de
> luminosité **16 en médiane**, là où le seuil est **42** (§3). Après remappage sur la
> rampe du §1.2 : **109**. Zéro ton sur ton dans la bande haute, sans exception.
> **Pourquoi c'est interdit partout ailleurs :** dans l'**Index**, le **Fil**, la **Toile**
> et l'**encart d'une Nuée**, la dalle garde **le monde, et rien d'autre**. Une dalle
> teintée dans une liste serait **un classement par nature** — exactement ce que le produit
> refuse. La règle du §4 (« LA DALLE PORTE LE MONDE, L'ACCENT PORTE LA NATURE ») reste
> entière : la teinture ne l'entame pas, elle vit dans son exception.
> **LA FORME NE BOUGE JAMAIS** — c'est toujours la vraie dalle du moteur (règle 1
> ci-dessus) ; on ne remappe que la LUMINOSITÉ sur les trois teintes de la nature. Aucun
> polygone n'est reconstruit.

> **⚠ LE VIDE EST UN DÉFAUT DU PLANCHER — PAS UN DÉFAUT GÉNÉRAL.**
> (Décision Tom, 19 août 2026, **corrigeant une première formulation trop large**.)
> **Ne remplis pas le champ partout. Lis ce paragraphe en entier avant de toucher au sujet.**
>
> **Ce qui est normal :** une fiche et une page + gardent **la boîte du §2.7** — dalle
> centrée, couleur de nature autour. C'est le moodboard, et il a raison. Relevé sur
> `promi-nuee-toile.html` : l'espace entre le bas des dalles et le trait est **correctement
> occupé jusqu'à trois éléments** (cadres 0 à 6).
>
> **Ce qui est un défaut :** **au PLANCHER**, un bandeau de couleur nue se creuse **dans les
> ventres de l'onde** (cadres 8 et 10 de la planche, « Quatre » et « Sept »). Là, la matière
> doit **descendre jusqu'à la vague, épouser ses creux**, et ne jamais laisser de couleur nue
> entre elle et le trait — découpée par le chemin de l'onde, la nature dessous.
>
> **Pourquoi c'est propre au plancher, et où chercher ailleurs :** au plancher, `base` cesse
> de descendre pendant que le NOMBRE d'éléments continue de monter. La Toile d'une Nuée tire
> sa taille de ce nombre : ses dalles rapetissent, la vague ne bouge plus, le vide se creuse.
> Sur une fiche et sur la page +, la boîte de la dalle est **calculée à partir de la base**
> (`dh = base − amp − 100`) : le rapport entre la matière et la vague ne se dégrade jamais.
> **Mesuré, pas supposé** — `scratchpad/mesure_vide.py`, deux thèmes, tous les écrans.
> Planchers : **196** pour une fiche et pour la page + (§2.5), **176** pour une Nuée (§9).
> Aucune base de fiche n'atteint le sien (262 · 372 · 376) ; la page + l'atteint sur un
> **choix ouvert** ; une Nuée l'atteint **à partir de quatre éléments**.
>
> **Trois exclusions, validées par Tom :** l'**instant** (la couleur du champ y EST le sujet —
> en couverture, le menthe disparaît ; Q58 **clos**), un **gardé de côté** (pas d'aplat, donc
> pas de champ à remplir), une fiche **à photo** (la photo remplace la matière et doit rester
> sous l'entête, Q53 ; Q57 **clos**).
> **Deux corollaires :** la bande haute **teinte** sa dalle (Q30, §4 ci-dessous — la fiche ne
> l'appliquait pas), et le **mot-marque a deux encres** (§10.6 généralisé : il suit ce qui est
> peint sous lui, crème ou encre, jamais un troisième ton ; Q59).

> **⚠ UNE NUÉE SE LANCE EN TRAÇANT LE TRAIT ENTIER.** (Décision Tom, 19 août 2026.)
> Pas une moitié : **0 → 390**, le **mode complet** du §2.6 — celui d'une parole tenue.
> Une Nuée n'est promise à personne ; **personne ne vient à sa rencontre**, donc une
> demi-courbe n'aurait aucun sens. Trait entier donné = ni chevron, ni points : plus rien ne
> manque. Un Promi et un Chiche gardent leur moitié — là, l'autre trace la sienne.

> **⚠ UN SEMIS EST DÉTERMINISTE — ET UNE DALLE SE REND UNE FOIS.** (Exigence Tom, 19 août 2026.)
> **1 · Même Nuée, même semis.** À chaque ouverture, dans les deux thèmes, sur n'importe quel
> appareil : **quelle dalle occupe quelle case, et où**, ne change jamais. Une Toile qui
> changerait de composition entre deux ouvertures ne serait plus la Toile de CETTE Nuée.
> Un placement se tire donc des **ids** et du nombre d'éléments — **jamais** de `Math.random`,
> jamais d'une horloge, jamais de la taille du canevas (les cotes sont en écran 390).
> Contrôlé par `scratchpad/semis_determin.py` : 3 ouvertures × 2 thèmes × 2 densités de pixels.
> **Ce qui RESPIRE, et qu'il ne faut pas confondre avec le semis :** `Toile.dalleTrame` rend
> la matière avec `performance.now()`, et il **recadre au plus juste sur l'alpha** — le format
> de la dalle bouge donc d'un rendu à l'autre, partout dans le produit. **Un contrôle qui
> compare les PIXELS, ou le rectangle peint, mesure la respiration du monde, pas le semis** —
> mesuré : 3 empreintes distinctes sur 3, sur douze configurations. On compare **la case**.
> **2 · Une dalle se rend une fois, pas une fois par case.** `dalleTrame` refait l'attribution
> pondérée **pixel par pixel**. L'appeler par case d'une grille, à chaque repeinte, a fait
> ramer l'app au point que `redteam_toile` **n'a pas rendu la main pendant dix minutes**, deux
> fois de suite — et que `releve-S5` a sorti un rouge sur un canevas pas fini de peindre.
> **Un cache par id, le temps de la passe** : mêmes pixels, un seul calcul. **Cette règle vaut
> pour tout rendu en grille** — elle reviendra sur l'Index et le Fil dès qu'ils afficheront
> beaucoup de dalles.

> **⚑ UNE DALLE EST FIGÉE À SA PLANTATION — POSÉ LE 4 septembre 2026 (feu vert Tom).**
> Un Promi porte `monde = {m:design, p:palette, h:teinte}`, figé par la fabrique `P()` au
> moment où il est planté. **`dalleTrame(cv, id, k, monde)` prend un 4ᵉ argument facultatif** :
> absent, elle se comporte exactement comme avant ; présent, elle peint la dalle dans le monde
> de SA plantation. Elle sauve et restaure `theme`, `palKey`, `hueShift` **et `_palLit`** —
> ce dernier est un **mémo** de la palette calculée : sans l'invalider à l'aller la palette de
> l'appelant fuit dans la dalle, sans le restaurer au retour celle de la dalle fuit dans la
> Toile. **`Toile.mondeCourant()`** rend `{m,p,h}` en lecture seule.
> **Les Promi d'avant ce lot** prennent le monde courant, figé à ce moment
> (`window._figeMondesManquants()`, idempotente) : **rien n'est tiré de leur date.**
> Preuve : `scratchpad/preuve_monde.py` — quatre contrats, dont **aucune fuite**.
> **Câblé depuis le 13 septembre** : les peintres de l'Index, du Fil, de la Pelote et de l'écran qui vend passent le
> monde de plantation en 4ᵉ argument (voir le paragraphe suivant).
>
> **⚑ ET SA COULEUR AUSSI — posé le 13 septembre 2026 (feu vert Tom, Q213, pour cette raison seule).**
> La couleur d'une dalle était **tirée au hasard à chaque chargement** (`cc()`, `Math.random`) : une dalle
> n'avait aucune identité stable. Un Promi porte maintenant `dalle = {ci, lit}` — l'emplacement dans la palette et
> la nuance —, figé par `_dalleFigee(vivant)` au moment où `Toile.addPromi` le relie (la couleur que la Toile
> vient de tirer, loin de ses voisines). Un Promi sans `dalle` (jeu de démonstration, sauvegarde ancienne) la
> reçoit de **son titre et sa personne** (`_dalleDeCle`) — **jamais de l'id**, qui change d'un chargement à
> l'autre sur le jeu (chantier 71). `tones()` la respecte à chaque passe. **Les peintres des cartes (Index, Fil)
> reçoivent le monde de plantation** en 4ᵉ argument. Contrôlé par `redteam_dalle_figee.py`.
> **Une Nuée a SA dalle** (Tom, 13 sept. 2026) : `Toile.sync()` plante une dalle par Nuée nommée (`kind:'nuee'`), sa couleur est
> figée par Nuée (`NUEDALLE[clé]`, tirée de son nom), et le code du Cercle y passe — jamais sur ses Promi. Avant, `sync` l'effaçait à
> chaque plantation : une Nuée de neuf paroles était invisible sur la Toile. Contrôlé par `redteam_nuee_dalle.py`.
>
> **⚠ Ce que ce paragraphe disait avant, et qui était vrai jusqu'au 4 septembre :**
> On a longtemps cru l'inverse. **C'est faux :** un Promi ne porte **aucun champ de monde**
> (`Object.keys(p)` n'en a pas), et `theme`, `palKey`, `hueShift` sont **trois variables de
> module, globales**. La même dalle repeinte dans trois mondes donne trois remplissages
> différents — 4289 · 3963 · 1912 sur la dalle 125, boîte et tons compris
> (`scratchpad/monde_fige.py`). **Changer de monde au Studio repeint TOUTE la Toile, les
> anciennes dalles comprises.**
> *(Décision prise depuis : le monde est figé le 4 septembre, la couleur le 13 — paragraphes ci-dessus.)*

> **⚑ 21 SEPTEMBRE 2026 — L'EXCEPTION INGÉNU : DANS LA PALETTE PAR DÉFAUT, LA COULEUR D'UNE DALLE DIT SA NATURE.**
> (Décision Tom.) La palette par défaut s'appelle **Ingénu** (ex-« Avenant », ex-« Signal » ; clé `signal`) et garde ses
> quatre tons : bleu `#82AEF8` · rose `#FFB8D2` · lilas `#C9A8F5` · crème dalle `#EFE3C7`. **Sous Ingénu seulement,
> un Promi est bleu, un Chiche rose, une Nuée lilas, et le crème dalle peint les cellules neutres** (les cellules
> colorées qui ne portent aucune parole). *« La couleur ne ment plus, elle dit la vérité. »*
> **C'est une exception au « la dalle porte le monde, l'accent porte la nature » — elle ne vaut QUE pour Ingénu.**
> Sous toute autre palette, la dalle garde sa couleur figée (`p.dalle.ci`), qui n'est pas effacée : elle revient telle
> quelle dès qu'on quitte Ingénu. Où ça vit : `cOf()` (la seule décision de teinte du moteur) lit `s.nat`, posé par
> `_dalleFigee`. **Les douze autres palettes qui portent une couleur signal restent telles quelles** : choisir une
> palette est un geste délibéré. QUESTIONS · Q292, Q297.

1. **Toujours la vraie dalle du moteur**, rendue par `Toile.dalleTrame(canvas, id, 1)`.
   Jamais un polygone, jamais un hexagone, jamais une photo, jamais une approximation.
   La bande de Nuée n'y échappe pas : ce sont de vraies dalles, seulement **teintées**
   mauve (la teinte porte l'identité, pas une forme inventée).
2. **⚑ v29 (Tom, 23 sept. 2026) — UNE DALLE SE REND À SA TAILLE FINALE ET SE POSE 1:1.** Jamais rendue
   à la taille de la Toile puis agrandie, réduite, rognée, relue en pixels ; jamais une photo ; jamais un
   morceau de Toile. On passe par **`window._poseDalle(g, id, x, y, w, h, o)`** (ou `_rendDalle` + `_poseUn`) :
   le moteur rend la dalle au `k` de la boîte, et depuis v29 **`k` agrandit aussi les pas de trame
   (`UK`)** — la même dalle à 40 px et à 200 px est la même image. Ce que les appelants retouchaient
   (Q30, Q297, chantier 59) est peint PAR LE MOTEUR (`opts.rampe`, `opts.decale`) ; ce qu'ils relisaient,
   le moteur le DÉCLARE (`cv.__dalleInfo`). Contrôlé à chaque lot qui touche une dalle par
   **`redteam_decoupe.py`**. Le contrat d'un monde : **`CONTRAT-MONDE.md`**.
   *(Avant v29 : « l'échelle est toujours 1 » — les valeurs ≥ 6 cassaient les mondes à trame, dont les pas
   étaient en pixels. C'est `UK` qui a levé la contrainte.)*
3. **La dalle est au premier plan.** `opacity: 1`, `filter: none`,
   `mix-blend-mode: normal`, `z-index` supérieur au voile de couleur.
   Le voile est le `background` du bloc, jamais un calque par-dessus.
4. **Aucun filtre, aucun voile, aucun masque** ne passe devant une dalle.
5. **Peindre après insertion.** Les canevas ne sont mesurables qu'une fois
   disposés : relancer `peintMinis()` à 0, 60, 200 et 600 ms.
6. **Jamais de dalle en fond animé** sur un écran qui montre des dalles de
   référence.

**Sujet contre ambiance — la nuance qui clôt le débat (lot 2B).** Les règles 3, 4
et 6 visent la **dalle-sujet** : celle qu'on montre et qu'on référence (dalle de
fiche, de tuile, de partage). Elle est à **opacité 1, sans voile ni masque, jamais**.
Un **fond d'ambiance** — une dalle décorative derrière un contenu qui **n'est pas
elle** (ex. la trame de la page +, où le sujet est **la phrase**) — **peut porter un
masque** : là, la **lisibilité du contenu prime**. Ne pas confondre les deux, ne pas
rouvrir le débat : sur la page +, la trame reste masquée (décidé au lot 2B).

**Les vingt mondes** (repris le 30 sept. 2026 — la table vivante, avec clés, accès, famille de semis et réglages
déclarés, est dans `ETAT-30-SEPTEMBRE-2026.md` §4, engendrée de l'app) :
gratuits — Pochade · Touffe · Brouillamini · Halin · Esquille · Tesselle · Braille · Buvard
Ma Parole ! — Ramage · Guingois · Chantourné · Volubilis · Madrure · Chamade · Ritournelle · Bobinette · Mascaret · Éclisse · Taille-douce · Houle
*(historique : « les huit mondes — Encre · Mosaïque · Touffe · Braille · Pixel / Cercle — Terrazzo · Gravure · Sillons ».
Les clés internes gardent ces anciens noms : `encre`, `mosaique`, `pixel`, `terrazzo`, `gravure`, `sillons`.)*

> **⚑ ÉCLATS EST RETIRÉ DU CODE** (assainissement, 30 sept. 2026) — il ne paraissait déjà plus au Studio depuis Q102.
> **⚠ ÉCLATS N'EXISTE PAS AU STUDIO.** (Décision Tom, 29 août 2026 — Q102.) Ce fichier en
> listait **neuf**. `PROMI-SPECIFICATIONS §10.4` écrit l'inverse, noir sur blanc :
> *« `RD = {pixel, braille, sillons, gravure, mosaique, encre, terrazzo, touffe}`.
> **Éclats n'existe pas.** »* — et l'app ne le montre nulle part (`order` en compte huit).
> **Son code est conservé** (`WL`, `_lockW` le connaissent) ; **il n'apparaît pas au Studio.**
> Ne pas le remettre dans un rail « parce qu'il est dans la table ».

---

## 5. Les composants communs

Ces éléments sont **identiques sur tous les écrans**. Ne jamais en créer une
variante locale.

| Composant | Règle |
|---|---|
| **Le geste** | 118 px de haut, deux points, un trait. Toujours **entier**, jamais rogné ni superposé. Le trait part **du centre du rond gauche**, pas du doigt. Courbes quadratiques, jamais de segments droits. |
| **Peaufiner** | 62 px, en bas de chaque fiche. Même typographie, même filet, même place. Porte l'icône de partage à droite. |
| **✕ Fermer** | En haut à droite, `top: 50px`, avec le texte `FERMER`. |
| **Le mot-marque** | « Promi » en **PromiLate**, dans le plateau, haut à gauche *(historique : Fraunces 20 px)*. |
| **« Moi »** | Toujours **premier** de la liste des destinataires, avec son avatar dégradé. Dans une Nuée : « tout le monde » passe devant, « Moi » ensuite. |
| **Les boutons ronds** | Partager, commenter, joindre : **icône seule**, jamais de texte à côté. |

> **⚠ §13 · SUR UNE FICHE DE NUÉE, PEAUFINER NE S'OUVRE QU'EN TOUCHANT SA BARRE.**
> **Partout ailleurs c'est l'inverse.** C'est la règle unique du produit, et le document
> prévient : *« sans cette exception écrite, le comportement sera implémenté comme les autres
> écrans »*. Sur cette page, **le doigt qui descend fait défiler LE FIL, pas les réglages** :
> l'encart, les Noyaux, le titre remontent et disparaissent sous le trait, les Promi prennent
> toute la place, et il ne reste qu'une bande de Toile de **114 px** (base 58, amplitude 16).
> **Cet état est une CLASSE que le code pose, jamais une géométrie qu'il vient de produire**
> — c'est le piège du §8, payé deux fois sur la page +.
> **C'est aussi la butée du défilement, pas une valeur de la formule :** un contrôle qui
> vérifie `base = max(176, 460 − 86 n)` doit l'EXCLURE, sinon il le compte comme une erreur.
> Et **la Toile qu'on y voit est LA MÊME, simplement remontée** — jamais une seconde
> composition.

### ⚑ LA GRAMMAIRE DES TRAITS ET DES CONTOURS — UNE SEULE RÈGLE

> **Décision Tom, 2 septembre 2026.** *« Dans toute l'app revoir les traits et contours pour
> ne pas créer de décalages visuels avec les autres éléments, et que le cadre paraisse plus
> marqué que le reste — le reste s'y adapte donc. »*

**Trait de 2 px, couleur du corps, rayon = hauteur ÷ 2.** Relevé sur l'app et sur le Studio,
écran par écran : la règle existait déjà presque partout.

```
le plateau        342 × 60   trait 2   rayon 30      (= h ÷ 2)
la recherche      270 × 52   trait 2   rayon 26      (= h ÷ 2)
le tri             52 × 52   trait 2   rayon 26      (= h ÷ 2)
le sélecteur      167 × 44   trait 2   rayon 22      (= h ÷ 2)
Peaufiner         342 × 62   trait 2   rayon 31      (= h ÷ 2)
Inviter/Partager  168 × 62   trait 2   rayon 31      (= h ÷ 2)
le disque          44 × 44   trait 2   rayon 50 %
le grand panneau  342 × 253  trait 2   rayon 30      un panneau, pas une pilule
```

**Le cadre ne se soustrait pas : c'est le reste qui monte jusqu'à lui.** Quatre familles
s'en écartaient et faisaient paraître le plateau « à part » alors qu'il était le seul à la
règle — les sept rangées des Réglages à **3 px / rayon 22**, le tri du Fil et les boutons de
l'Aura dans une **seconde crème** (`231,229,223` au lieu de `244,238,225`), les rangées
d'Arranger avec un filet de **1 px à 13 %** large de **346 dans un cadre de 342**, et les
cinq pastilles du Cercle à **1 px / rayon 10** dans un bleu qui n'est la couleur d'aucun
autre contour. Contrôlé par un balayage qui vérifie les trois cotes sur dix écrans.

> **⚑ UN JOUR D'ANNEAU SE DONNE EN PIXELS D'ARC, JAMAIS EN POURCENTAGE DU TOUR.**
> (Tom, 23 septembre 2026 : *« les espaces entre les segments sont inégaux et irréguliers —
> uniformisé partout, net, espace logique parfait entre tous, sans fioriture »*.)
> **Le jour vaut 3 px d'arc, et il se convertit par anneau** (`3/r` en radians). Donné en ANGLE,
> le même écart sort inégal d'un disque à l'autre : 0,8 % du tour faisait **1,00 px** sur « Toi »
> (Ø 78) et **0,76** sur une personne (Ø 58).
> **n arcs, n jours identiques, le jour centré sur midi** — pas d'ouverture supplémentaire en
> haut, pas de fondu entre deux segments (l'anneau d'une fiche en avait un de 3 % du tour : deux
> grammaires pour un même objet, c'est la fioriture qu'on refuse).
> ⚠ **Et un seul état ne peut pas faire 360° PILE** : un arc SVG dont le départ et l'arrivée sont
> le MÊME point **ne dessine rien**. On laisse un dixième de degré, sinon un Noyau qui n'a qu'un
> état sort SANS ANNEAU.
>
> **⚑ LA PILULE CÈDE À 94,5 DE HAUT — rayon 30 au-delà.** (Tom, 11 septembre 2026, QUESTIONS · Q203.)
> *« La loi du §2 tient là où elle a du sens, et cède seulement là où elle produit un défaut. »* Au-delà d'une certaine
> hauteur, rayon = hauteur ÷ 2 **mange le texte** : la courbe vient serrer le début de la première et de la dernière ligne
> (NOTE de 118 en pilule : encre à 6,3 du contour ; à 163 la courbe coupe la ligne). **Le seuil est MESURÉ, pas un nombre
> de lignes** : 94,5 est la hauteur où la pilule la plus serrée à deux rangées passe sous l'air d'un champ ouvert au rayon
> 30 (C = 15,19, mesuré sur l'encre). **Donc : h ≤ 94,5 → rayon h ÷ 2 ; h > 94,5 → rayon 30** — c'est le « grand panneau »
> du tableau ci-dessus, qui était déjà la règle. Un seul propriétaire dans l'app : `rayon()` (`lot-CERCLE-MUR`,
> `window._seuilPilule`) ; les juges portent 94,5 EN DUR (§7).

### ⚑ LA LOI DES POINTS (Tom, 4 oct. 2026, v128 — C-044)
> **« Les points disent qu'il manque quelque chose : une moitié de trait, un mot, un engagement. Ils ne servent jamais à autre chose.
> Exception nominative : les trois petits points du choix de taille de l'outil de dessin. »**

### ⚑ v127 — LA LOI DES POINTS : UNE SEULE EXCEPTION, NOMINATIVE — LE CHOIX DE TAILLE DE L'OUTIL DE DESSIN (C-042)
> (Décision Tom, 4 oct. 2026.) *« Au second toucher sur la plume ou la gomme, trois petits points côte à côte, de taille croissante, à
> l'encre du mode. Inscris dans CLAUDE.md l'exception nominative à la loi des points : seul ce choix de taille y échappe. »*
> **Seul le choix de taille de la plume et de la gomme porte des points** ; nulle part ailleurs un point ne sert de commande ni de repère.
> Le texte de la loi : bloc ci-dessus (dicté par Tom en v128). L'outil n'est pas construit : planche `planche-v127/dessin-*`, en attente de son choix.

### ⚑ UN RÉGLAGE VIT LÀ OÙ VIT CE QU'IL RÈGLE

> **Décision Tom, 31 août 2026. Née du pinceau, elle vaut pour tout réglage à venir.**

**LE STUDIO NE PORTE QUE CE QUI EST VRAIMENT GLOBAL.** Ce qui appartient à **une** parole se
choisit **là où cette parole se fait** — jamais dans un écran de préférences.

Le test est simple et il se pose avant d'ajouter quoi que ce soit au Studio :
**est-ce que ce réglage a un sens différent d'un Promi à l'autre ?** Si oui, il n'a rien à
faire au Studio, quelle que soit la commodité.

```
AU STUDIO — global               le monde · la palette · l'écran (sombre/clair) · le texte
À LA PAGE +, à la création       ce qui appartient au Promi qu'on plante
DEPUIS LA FICHE, dans Peaufiner  on le reprend — Promi, Nuée, gardé de côté
```

**Le cas qui a fondé la règle — LE PINCEAU.** Le choix du trait avait été posé au Studio :
il s'appliquait donc **à toutes les fiches d'un coup**, ce qui interdisait exactement ce que
le produit veut — donner son trait à *ce* Promi, à *cette* Nuée. Il est passé à la **page +**,
à la création, et se reprend **depuis Peaufiner, haut de liste**.

**Corollaire de dessin, et il est grand :** un écran qui perd un réglage perd aussi ce qui
n'était là que pour le montrer. Le trait du §2.1 n'existait au Studio que pour porter le
pinceau qu'on essayait ; sans lui, **l'onde disparaît et la Toile prend tout l'écran**.
Ne pas garder une forme par habitude quand sa raison d'être est partie.

---

### ⚑ UN AJOUT VALIDÉ, HORS INVENTAIRE — et comment on l'écrit

> **Décision Tom, 20 août 2026. Elle clôt Q75.**

La méthode du portage est « **écrire chaque écran depuis son inventaire** ». Elle a un angle
mort : **un écran peut porter une FONCTION que son cadre ne montre pas.** Le moodboard dessine
un écran **au repos** — il ne dessine pas ce qu'un doigt fait apparaître.

**On ne supprime jamais une fonction parce que le cadre ne la montre pas.** On la sort du
repos, et on l'écrit comme **ajout validé, hors inventaire** :

1. **Le repos est celui du cadre**, au pixel. Rien de l'ajout n'y paraît, et l'ajout ne
   décale **aucune** cote du cadre.
2. **L'ajout apparaît AU BESOIN**, sur un geste, et il se referme.
3. **Il est nommé dans `ETAT-DES-LIEUX.md`** — ce qu'il est, ce qui le déclenche, et la
   décision qui l'a validé. Sans cette ligne, le portage suivant le prendra pour un résidu
   et le supprimera.
4. **Son contrat de test vise le GESTE, jamais le repos.** Un contrôle qui exige l'ajout
   visible au repos contredit le cadre : il se réécrit au niveau de la décision (§7).

**Le cas qui a fondé la règle — LE FIL.** Le **cadre 76** montre cinq bandeaux nus, 358 × 128,
de 140 en 140 : **aucune rangée « TENIR · REPORTER »**. Mais le Fil est **le seul endroit d'où
l'on tient une parole sans ouvrir une fiche**, et cette fonction ne se perd pas. Donc : le
bandeau au repos est **exactement celui du cadre**, et **le geste apparaît au besoin** —
un **appui maintenu** sur le bandeau déplie sa rangée, un toucher bref ouvre sa fiche.
Cet ajout est **validé, hors inventaire**.

---

## 6. La typographie

```
Gilbert Bold          sous-titres, libellés, navigation — EN CAPITALES        700
Atkinson Hyperlegible tout le texte                                    400 · 500 · 700
PromiLate             titres d'écran, mot-marque « Promi », phrases du trait  400   (18 sept. ; seule graisse)
```
*(Repris le 30 sept. 2026 : **trois polices, cinq faces**, rien d'autre — Fraunces, Bricolage et Apfel sont retirées
depuis le 22 sept. Les blocs datés qui suivent en racontent l'histoire ; les sept niveaux vivent dans `PROMI-TOKENS.json`.)*

> **⚑ 18 SEPTEMBRE 2026 — LES TITRES SONT LA POLICE PromiLate** (`Polices Promi/PromiLate-Regular.otf`,
> jeton `--f-marque`, `lot-TITRES-POLICE`). Elle remplace les huit dessins ci-dessous (Q234). 27 px (cap 18,9),
> 29 sur la page + ; une seule graisse, `font-synthesis:none`. Aussi les phrases d'action DU TRAIT, et rien d'autre.
> Le bloc suivant reste pour l'histoire.
>
> **⚑ 17 SEPTEMBRE 2026 — LES TITRES NE SONT PLUS UNE POLICE : CE SONT HUIT DESSINS.**
> (Décision Tom, assumée : *« huit dessins, pas une police. Si un écran change de nom un jour, il
> faudra un nouveau dessin — c'est le prix, et il est acceptable. »*) Faute de fichier de fonte,
> les titres sont **vectorisés depuis la planche du lexique** (`~/Downloads/promi-lexique.png`) :
> **Promi · Le studio · L'aura · Fil · Index · Partager · Toile · Noyau**.
>
> **UN SEUL `<path>` PAR MOT, `fill:currentColor`, AUCUN BITMAP.** Le dessin suit donc toutes les
> règles de couleur déjà posées, sans en ajouter une. **Seule exception : « Promi » a DEUX chemins**
> — le mot, et son **« i »**, qui garde sa couleur d'accent. Le « i » est reconnu **à sa place**
> (tout contour dont le bord gauche passe 0,82 × la largeur), jamais à un indice.
>
> **DEUX CHOSES À NE JAMAIS REPERDRE, si on refait la vectorisation :**
> · **on suréchantillonne le NIVEAU DE GRIS avant de seuiller.** L'anticrénelage de la source porte
>   l'information sous-pixel ; le jeter d'abord donne un escalier. C'est ce qui fait tenir une source
>   de 760 px à **0,34 px d'écart moyen au bord, à 2×** — sous le pixel.
> · **le marching squares doit être ORIENTÉ** (l'encre toujours à gauche du sens de marche), sinon le
>   chaînage rend des fragments : **50 contours pour « Promi » au lieu de 8**.
> Outil : `scratchpad/vecto_lexique.py`. Planche : `planche-lexique.html`.
>
> **LE DESSIN SE MET À L'ÉCHELLE SUR LA HAUTEUR DE CAPITALE, et cette cote est DÉCLARÉE** (§8 : une
> cote se calcule, elle ne se mesure jamais). Relevé police chargée : Gilbert 27 → **18,9** ·
> Fraunces 27 → 18,9 · Fraunces 29 → **20,3**. Au premier jet je lisais `fontSize` au moment de
> poser : le mot-marque de l'accueil sortait à **28 px au lieu de 119**.
> ⚠ **Et la cote se pose EN LIGNE avec `important`** : les plateaux portent des règles d'icône
> (`.acc-plat svg{width:22px}`) qui écrasent l'attribut `width` d'un SVG.
> ⚠ **On MASQUE le texte d'origine, on ne le supprime jamais** : `.ti-x` porte le dernier caractère
> et il CLIGNOTE sur « Réglages ». Rien ne se perd (§5).
>
> **SIX TITRES SUR HUIT SONT POSÉS** (`lot-TITRES-DESSINS`) : le mot-marque de l'accueil et celui de
> la page +, l'Index, le Fil, Partager, Le studio, L'aura. **« Toile » et « Noyau » n'ont aucun titre
> d'écran à eux aujourd'hui** — ils n'existent que dans « Arranger la Toile », « Ma Toile » et les
> libellés de l'Aura. Leurs dessins sont prêts et attendent une place. **Les titres restants (Nuée,
> Réglages, La langue, La confidentialité) gardent Gilbert** : la planche ne les porte pas, et le §9
> interdit d'inventer une forme.
>
> **⚑ LES DEUX POLICES ONT CHANGÉ LE 16 SEPTEMBRE 2026** (Tom, avec sa planche du lexique).
> **Gilbert Bold** — *Type With Pride*, Ogilvy & Mather — porte les **sous-titres, les libellés
> et la navigation, en capitales**. **CC BY-SA 4.0 : le crédit est OBLIGATOIRE dans l'écran
> « à propos », et les glyphes ne peuvent pas être modifiés.** **Atkinson Hyperlegible Next** —
> Braille Institute of America, SIL OFL 1.1, libre — porte **tout le texte**. ~~**Les titres
> gardent Fraunces**~~ *(historique — remplacée par PromiLate le 18 sept., retirée le 22)*.
>
> **LES SEPT NIVEAUX** (ils vivent dans `PROMI-TOKENS.json`, et nulle part ailleurs) :
> ```
> titre        PromiLate 400  36 px     (était Fraunces 600 — historique)
> sous-titre   Gilbert  700   22 px   CAPITALES
> texte        Atkinson 400   16 px
> accentué     Atkinson 700   16 px
> petit texte  Atkinson 400   14 px
> métadonnée   Atkinson 400   13 px   opacité .65
> libellé      Gilbert  700   15 px   CAPITALES
> ```
>
> **MESURÉ AVANT DE BASCULER, parce que Tom l'a demandé :**
> · **la barre du bas, cinq entrées à 12 px en capitales.** Gilbert est plus ÉTROIT que ce qui
>   était là : STUDIO **40,50** px contre 45,83 · AURA 29,83 contre 33,45 · INDEX 34,31 contre
>   37,17 · FIL 18,47 contre 17,94. L'air entre STUDIO et AURA **monte de 14,36 à 18,84 px**.
>   Ce n'était donc pas serré — ça respire mieux qu'avant.
> · **le plancher de 12 px tient.** À **13 px**, la hauteur d'x RENDUE d'Atkinson est de **7 px**
>   — exactement celle d'Apfel et d'ApfelMid. À 12 px, 6 px de part et d'autre. La métadonnée
>   réelle « tenu · il y a 2 jours · Quentin » passe de 163,39 à **167,97 px** (+2,8 %).
>   Rien ne perd en hauteur d'œil ; **le §6 n'a pas à bouger**.
>
> **⚠ LES MÉTRIQUES DES FACES NEUVES SONT CALÉES SUR CELLES QU'ELLES REMPLACENT.** Sans cela le
> changement de police déplace les cotes : la boîte de Gilbert fait 1,250 em là où Bricolage
> fait 1,188 — **9 paires de textes resserrées de 1 à 2 px**, mesurées par `redteam_air`, dont
> la phrase d'un gardé de côté. `ascent-override` / `descent-override` / `line-gap-override`
> dans le `@font-face` les font coïncider **à toutes les tailles employées** (relevé de 11,5 à
> 29 px : zéro écart). **Aucun glyphe n'est touché** — la licence de Gilbert l'interdit ; ce
> sont des métriques de mise en page, pas des dessins.
>
> **⚠ ET LA GRAISSE NE CHANGE PAS NON PLUS.** L'ancienne table écrasait Apfel 500·600·700·800
> sur ApfelMid 500, faute de plus gras dans la famille. Atkinson EMBARQUE un 700 : rendue telle
> quelle, la table aurait mis en gras tout ce qui demandait 700 dans la feuille (mesuré : le
> libellé du geste et les pastilles, 500 → 700). **Atkinson 500 reçoit donc tout ce que
> ApfelMid 500 recevait** ; la face 700 ne sert qu'au niveau « accentué », demandé nommément.
> **Seule exception, et elle est inévitable : Gilbert n'a qu'une graisse.** Ce qui était
> Bricolage 600 passe en Gilbert 700 — le contrat visuel le voit, c'est attendu.
>
> **⚑ 22 SEPTEMBRE 2026 — IL N'Y A PLUS QUE TROIS POLICES : Gilbert, Atkinson, PromiLate.**
> (Décision Tom. *« En Swift elles n'existeront pas : autant le voir maintenant que pendant le
> portage. »*) **Fraunces, Bricolage Grotesque et Apfel Grotezk sont RETIRÉES** — six faces,
> **161,9 Ko**, et leurs crédits avec elles. Les piles sont `PromiLate,Gilbert,system-ui`,
> `Gilbert,system-ui`, `Atkinson,system-ui`.
>
> **⚠ ET LA NOTE QUI ÉTAIT ICI ÉTAIT FAUSSE.** Elle disait que Bricolage et Apfel restaient pour
> `✕`, `✦`, `→`, `←` et `●`. **Mesuré** (CDP `CSS.getPlatformFontsForNode`, qui rend les polices
> de plateforme et le NOMBRE de glyphes peints, 11 écrans × 2 thèmes) :
> ```
> ✕ ✦ ●   viennent DÉJÀ du système (Zapf Dingbats, 40 glyphes) — jamais de Bricolage ni d'Apfel
> ‹ ›     Bricolage en peignait 60 : le Studio et les rangées des Réglages
> →       Apfel en peignait 6 : « CHOISIR → » de la page +
> ```
> Ces trois caractères tombent maintenant sur la police du système, **comme ✕ ✦ ● le faisaient
> déjà**. Relevé après le retrait : la HAUTEUR du glyphe ne bouge que de **+9 %** (elle passe de
> 82-84 % à 89-92 % de la hauteur de capitale du texte voisin) ; c'est la CHASSE qui s'élargit —
> `→` +51 %, `‹ ›` +81 à +84 % —, et la seule boîte qui grandit est « CHOISIR → », de **124,1 à
> 129,6** px à x 42. Rien à reprendre : les chevrons étaient sous-dimensionnés, ils se lisent
> mieux. Sondes : `scratchpad/polices_rendues.py`, `scratchpad/chevrons.py`.
>
> **⚠ LA PREMIÈRE FAMILLE DÉCIDE — une liste d'égalités en rate toujours une.** Une police
> s'appelle de dix façons : `Bricolage,system-ui,sans-serif`, `'Bricolage',-apple-system,…`,
> `'Bricolage Grotesque',Bricolage,…`, `'Fraunces',Bricolage,serif`, l'attribut SVG
> `font-family="…"`, le raccourci `font:700 13px/1 Bricolage,…`, la clé d'objet JS
> `{'font-family':'…'}`, et `g.font` sur un canevas. **Au premier essai, 217 appels avaient
> survécu** — les avatars d'une Nuée, tout l'onboarding, le grand chiffre de l'Aura. On lit donc
> la PREMIÈRE famille de la liste, jamais la liste entière. ⚠ **Et un `@font-face` n'est pas une
> vue** : y poser `font-family:var(--f-titre)` DÉTRUIT la face (une custom property n'y est pas
> valide) — les six faces d'origine ont disparu en silence au premier passage, Fraunces tombant
> sur Georgia.

**Tailles minimales :** rien en dessous de 12 px. Aucune opacité sous 72 % sur du
texte lisible.

> **⚠ AUCUNE GRAISSE HORS DES FACES EMBARQUÉES.** (Lot du 19 août 2026.)
> En navigateur, une graisse absente se substitue **en silence** — la plus proche, ou une
> oblique synthétique. **En Swift, elle casse.** Le prototype étant la spécification du
> portage, tout couple demandé doit exister en `@font-face`.
> **Cinq faces depuis le 22 septembre 2026, et cinq seulement :**
>
> ```
> Gilbert 700                                      sous-titres, libellés, navigation
> Atkinson 400 · Atkinson 500 · Atkinson 700       tout le texte
> PromiLate 400                                    titres d'écran, mot-marque, phrases du trait
> ```
>
> **LA TABLE DE REPORT :** `gilbert` toute graisse → **Gilbert 700** (il n'en a qu'une) ·
> `atkinson` italique → **Atkinson 400** (aucune italique embarquée), ≥ 450 → **Atkinson 500**,
> sinon **400** · `fraunces` et `promilate` → **PromiLate 400**. Les familles retirées n'ont plus
> de report : elles ne sont plus demandées nulle part (`redteam_polices` : 0 couple absent).
>
> **⚠ ET IL A FALLU CORRIGER `lot-POLICES` LUI-MÊME.** Il retirait son propre style en ligne
> avant de relire la cascade — mais `pose()`, sur le Peaufiner d'une Nuée, écrit sur LES MÊMES
> propriétés. Tant que la feuille demandait « Bricolage 600 », la face existait et le lot ne
> touchait à rien ; avec « Gilbert 600 », qui n'existe pas, il reportait, posait, puis
> **détruisait l'inline de `pose()` au passage suivant** — 22 éléments retombaient sur la police
> héritée (`.np-bas` rendu en Atkinson 14, boîte 18, au lieu de Gilbert 14, boîte 17 : trois
> paires de textes resserrées). **C'est le piège « deux propriétaires pour une même propriété »
> du §7, et la parade est celle de la sonde : on note la valeur d'avant — et sa priorité — avant
> d'écrire, et on la remet avant de relire** (`data-pol-av`).
>
> **LA TABLE DE REPORT** — chaque couple absent va sur le plus proche embarqué, **sans
> changer la hiérarchie visuelle** :
>
> ```
> Apfel 500 · 600 · 700 · 800  →  ApfelMid 500    la graisse existe, dans la famille qui la porte
> Apfel 400 italique           →  Apfel 400       l'oblique était synthétique
> ApfelMid 400                 →  Apfel 400       la graisse 400 existe, dans Apfel
> Bricolage 800                →  Bricolage 700   la plus grasse embarquée
> Bricolage 400                →  Bricolage 600   la plus légère embarquée
> ```
>
> Contrôlé par **`redteam_polices.py`**, qui lit les `@font-face` du fichier — si on embarque
> une face, le contrôle la connaît au passage suivant, sans qu'on touche au test.
> **Appliqué par le bloc `lot-POLICES`, en JavaScript et pas en CSS** : le couple dépend de
> DEUX déclarations qui vivent rarement dans la même règle (réécrire « 800 → 700 » à
> l'aveugle enverrait un `Apfel 800` sur `Apfel 700`, tout aussi absent), et le §9 interdit
> de nettoyer le CSS. **La passe se RELIT, elle ne fige pas** : sur un élément déjà touché
> elle retire d'abord son propre inline, relit ce que la cascade dit vraiment, puis décide.
> Sans quoi une graisse lue trop tôt reste gelée et **la hiérarchie change** — mesuré :
> « Peaufiner » figé à 600 au lieu de 700.
> ⚠ **Le document écrit « Apfel 500 » à plusieurs endroits** (§5, §12). C'est la graisse
> voulue, mais ce couple n'existe pas : c'est `ApfelMid 500`. Voir QUESTIONS.md · Q68.

---

## 7. Méthode de patch — obligatoire

### Avant toute modification

1. Lire le code existant **avant** de le modifier. Ne jamais deviner.
2. Vérifier qu'une règle CSS s'applique réellement : le fichier contient
   **2 400 règles dont 54 % sont mortes**. Une déclaration peut être écrasée
   par une règle postérieure sans que ce soit visible.

### La méthode

```python
# Toujours ce motif, jamais un replace aveugle
assert S.count(old) == 1, "motif absent ou multiple"
S = S.replace(old, new)
```

### Après toute modification

```bash
# 1 · vérifier la syntaxe JS
python3 -c "import re,io; S=io.open('app.html',encoding='utf-8').read();
io.open('check.js','w',encoding='utf-8').write(''.join(m.group(1)
for m in re.finditer(r'<script[^>]*>(.*?)</script>',S,re.S)))"
node --check check.js

# 2 · les batteries
python3 redteam_ecrans.py     # 142 contrôles — la principale
python3 redteam.py            # 15
python3 redteam2.py           # 10
python3 redteam3.py           # 18
python3 redteam_demande.py    # 19
python3 redteam_toile.py      # 16
python3 redteam_geste.py      # 13
python3 redteam_verbe.py      # 6 — la phrase montre TOUJOURS son verbe + bascule
python3 redteam_filets.py     # 0 filet parasite — AUCUN trait horizontal hors moodboard
python3 redteam_vide.py       # 61 — UN ÉCRAN N'EST JAMAIS VIDE, en enchaînant les écrans
python3 redteam_air.py        # 391 paires — L'AIR ENTRE LES TEXTES ne se resserre jamais
python3 redteam_champ.py      # 32 — UN CHAMP BLANC N'EXISTE JAMAIS, il porte toujours sa nature
python3 redteam_gens.py       # 38 — le choix des personnes, AU DOIGT (ajout · croix · « + ajouter » · au-dessus de Peaufiner)
python3 redteam_tuiles.py     # 64 — l'écran des choix de la page +, AU DOIGT : la tuile touchée ouvre SA nature
python3 redteam_dalle_figee.py # 4 — une dalle garde sa couleur et son monde (par titre, jamais par id)
python3 redteam_reperage.py   # 16 — Promi · Chiche · Nuée lisibles sur chaque carte et ligne ; Nuée = petite Toile
python3 redteam_nuee_entree.py # 24 — « Planter dans la Nuée », dernière ligne du fil, au doigt ; la règle du trait tient
python3 redteam_accueil.py    # 22 — l'accueil B : plateau, barre 5 entrées, le + sur place, portes cachées fermées, dalles atteignables
python3 redteam_zoom.py       # 16 — le dézoom tient, planter ne reprend pas la vue, recadrer (rond et double toucher)
python3 redteam_cercle_couleur.py # 34 — LA COULEUR, 5e réglage du Cercle : bloc 384/encart 147, ton de palette et code libre jusqu'à la Toile, page + à la plantation
python3 redteam_tokens.py      # 19 — LE JEU FAIT AUTORITÉ : les valeurs décidées, les deux modes qui s'échangent,
                               #      zéro couleur et zéro police en dur dans les <style>, JSON = bloc CSS = Swift.
                               #      Sans navigateur : il ne flotte pas, et il se passe en une seconde.
python3 redteam_studio_geste.py # 13 — LE GESTE DE COULEUR DU STUDIO, au vrai doigt (CDP) :
                               #      appui 480 ms, horizontale = teinte, verticale = palette,
                               #      on revient exactement d'où l'on vient (Q125), et le
                               #      glissement de MONDE garde la main. Constantes en dur.
python3 redteam_apercus.py     # 8 — UN APERÇU DE TOILE PORTE TOUJOURS DE LA MATIÈRE COLORÉE :
                               #     le fond du Studio, les cinq mondes gratuits, et la DEUXIÈME
                               #     ouverture (buildStudio repeint sans `_shAllColored`, et le
                               #     semis juste est accroché à `.show`, que #studioScreen ne perd
                               #     jamais). On compte les pixels FRANCS ET FROIDS — un seuil de
                               #     saturation seul compte les crèmes et passe au vert sur un
                               #     écran mort. Plancher PAR MONDE, relevé sur la référence.
python3 redteam_nuee_dalle.py  # 38 — (+ un Promi planté dans une Nuée a sa dalle reliée) — une Nuée a SA dalle sur la Toile (au doigt, après plantation, couleur figée) et son bloc du Cercle ; sa couleur ne touche pas ses Promi
python3 redteam_rythme.py      # LE RYTHME D'UN MONDE NE DÉRIVE PAS (Tom, 26 sept.) — 13 mondes, arrivée et départ, par le
                               #   moteur ET par le vrai chemin, contre les valeurs EN DUR de la version validée (v60) :
                               #   fin du mouvement dans le moteur (tous à l'horloge depuis v61) ; HOULE = EXCEPTION, par image,
                               #   on juge ses images ; + cadence ≥ 60 %. Lancé avec le VRAI GPU (sans lui, Madrure prend son
                               #   chemin de secours). `--bride=3` prouve que la durée ne dépend pas de la charge.
                               #   Seul (≈ 8 min ; --sans-reel ≈ 4). ⚑ DANS LA SÉRIE À CHAQUE LOT QUI TOUCHE UN MONDE OU UNE LATENCE.
python3 redteam_decoupe.py     # UNE DALLE N'EST JAMAIS UNE IMAGE DÉCOUPÉE (Tom, 23 sept.) — piège drawImage/
                               #   getImageData/putImageData/createPattern/toDataURL à l'exécution, 19 écrans × 2 thèmes,
                               #   six familles (découpe · redimension · pixels · fragment de Toile · motif · PHOTO).
                               #   Échoue sur toute ligne NOUVELLE ; la dette de naissance (24 lignes) est SOLDÉE en v29,
                               #   `decoupe-dette.json` est vide. À PASSER À CHAQUE LOT QUI TOUCHE UNE DALLE.
                               #   Le contrat d'un monde : CONTRAT-MONDE.md.
python3 redteam_flash.py       # 32 — RIEN NE PARAÎT UNE FRACTION DE SECONDE (Tom, 30 sept. : « la deuxième fois qu'ils
                               #   reviennent »). Image par image, WebKit ET Chromium, au doigt : l'ouverture, le + → les trois
                               #   natures, planter les trois. Premier plan (grille 6×11, opacité ≥ .12) : aucune couche < 800 ms
                               #   ni au début ni à la fin, jamais l'ancien chrome ; la page + paraît COMPOSÉE dès sa première
                               #   image (nature, plateau à l'encre finale, phrase à sa mise en page finale) ; une plantation
                               #   COUPE, la page + ne reprend pas son aspect d'avant. Prouvé : 9/32 sur app-avant-v103b.
                               #   ⚑ À PASSER À CHAQUE LOT QUI TOUCHE UNE OUVERTURE, UNE FERMETURE OU UN MINUTEUR DE COMPOSITION.
python3 banc_rendu.py          # 280 images AU PIXEL — LE BANC DE RENDU DE RÉFÉRENCE (assainissement, 30 sept.) : 20 mondes × Toile
                               #   (clair, sombre, sans titres) + 4 dalles × 3 tailles ; hasard amorcé, horloge et images pilotées.
                               #   `--deux` prouve le déterminisme, `--figer` pose la référence (banc-rendu/ref/). C'est lui qui juge
                               #   le portage. ⚑ À PASSER À CHAQUE LOT QUI TOUCHE LE MOTEUR OU UN MONDE.
python3 redteam_notifs.py      # 36 — LES NOTIFICATIONS (v109), WebKit, permission simulée : jamais au lancement ; « Je te le rappelle ? »
                               #   à la plantation d'une parole DATÉE, demande seulement après « oui » ; deux « pas besoin » puis plus rien ;
                               #   RIEN QUAND LA DATE EST PASSÉE ; les mots EN DUR ; une par jour ; « C'est aujourd'hui » à l'heure choisie ; la page (mur Ma Parole !).
python3 redteam_volume.py      # AUCUN VOLUME, NULLE PART (v137 : la liste blanche de la Pelote est VIDE ; v114 : « le seul volume ») — statique : halo, ombre floue, dégradé ;
                               #   la dette de naissance est nommée (volume-dette.json). --sonde pose un halo sur une dalle : il rougit.
python3 redteam_kaki.py        # JAMAIS DE KAKI (v114) — OKLCH h 78–140°, C ≥ 0,015 : source, rendu des 20 mondes, planches (--planche=).
                               #   ⚠ ROUGE à la naissance sur l'app : la règle est posée, la correction attend la décision de Tom.
python3 redteam_clavier.py     # LE CLAVIER S'OUVRE AU GESTE (v114) — statique : un focus() différé hors du geste ; le Cercle exigé
                               #   synchrone ; les différés connus sont nommés (audit v114). Rougi sur sauvegardes/app-avant-v114.html.
python3 redteam_contour.py     # RIEN NE DÉPASSE DE LA SILHOUETTE DE LA PELOTE (v116). Rougi sur app-avant-v116 (la couronne).
python3 redteam_ajouter.py     # « + AJOUTER QUELQU'UN » GARDE SA LIGNE (v116) — aucun profil dessous, le bouton au-dessus de la barre.
python3 redteam_suggestions.py # LES SUGGESTIONS DE LA PAGE + (v115) — phrases 1 et 2 fixes, puis tirage SANS REMISE gardé d'une ouverture à l'autre.
python3 redteam_marges.py      # LES PHRASES SUGGÉRÉES (v115) — marge droite = gauche, retour à la ligne plutôt que réduction, même mise en
                               #   page à 390, 375 et sur un profil iPhone (appareil réduit). ≈ 15 min. Rougi sur app-avant-v115 (123 défauts).
python3 redteam_pilules.py     # LES TROIS PILULES DU + SE LISENT (v115) — ≥ 4,5 : 1, deux thèmes.
python3 redteam_murs.py        # 26 — LES MURS DU CERCLE (v104–v105), au doigt, deux thèmes : aucun encart, flou 4,8 px ; la phrase
                               #   POSÉE SUR LE FLOU (centrée dans le mur, sans fond ni trait, ≤ 3 lignes, une taille, encre/crème),
                               #   le temps d'être lue (3 à 5,5 s) puis elle s'efface ; la 1re fois l'offre s'ouvre à la fin de la
                               #   lecture ; pendant qu'elle est là un toucher n'importe où ouvre l'offre ; compteur GLOBAL, 21 phrases
                               #   EN DUR puis hasard sans répétition, 14 jours, rien au Cercle payé. 20/26 sur app-avant-v105.
python3 redteam_partage_fiche.py # 48 — v117 : le rond Partager d'une fiche (Promi, Chiche, Cercle), au doigt ET à la souris, WebKit
                               #   + Chromium : Mon Folio réduit à cette parole, sans Pelote ; l'image = Mon Folio réduit à la main ;
                               #   le choix d'avant rendu à la fermeture, jamais sauvegardé. 12/30 sur app-avant-v117b.
python3 redteam_photo_menu.py  # 18 — v117 : le bouton photo d'une fiche ouvre « Importer une image » (sélecteur du système) et
                               #   « La dalle d'origine » ; par défaut la dalle suit le Studio ; l'option se tient sur la fiche et au
                               #   partage (pixels, horloge figée) ; la page + garde l'import direct. 6/8 sur app-avant-v117b.
python3 redteam_joignable.py   # v118 — CE QUI SE TOUCHE EST JOIGNABLE : elementFromPoint au centre de chaque élément interactif, 38 écrans ;
                               #   chaque gestionnaire n'appelle que des fonctions qui existent, sur un nœud qui existe. Dette nommée
                               #   (joignable-dette.json), inventaire écrit (joignable-inventaire.md). Rougit sur app-avant-v117b
                               #   (bouton photo recouvert, ouvrirPartage). ≈ 2 min.
python3 redteam_origine.py     # 64 — v118 (Q365) : avec « La dalle d'origine », la bande haute porte la couleur d'origine, sauf ton sur
                               #   ton (ΔE < 15, en dur) → rampe de Q30. Rougit sur app-avant-v118 et avec --sonde.
python3 redteam_nuit.py        # 34 — v118, LE Zzz : six cas, almanach en dur (Paris, juin et décembre), fuseau inconnu, aucune bascule
                               #   sous les yeux, cran de nuit au hex près. --sonde (bascule en direct) rougit.
                               #   ⚠ 33/34 tant que le bouton « Zzz » n'est pas posé (ligne « premier lancement : Zzz activé »).
                               #   ⚠ v120 : LE Zzz EST COUPÉ — ce juge est ROUGE par décision, jusqu'à nouvel ordre.
python3 redteam_phrase_fiche.py # 56 — v136 (C-069) : chaque cas produit sa phrase (en dur), le titre est le plus grand texte, « + x personnes » se déroule au doigt, le Fil, l'Index et le Cercle sont sans phrase. 36/56 sur l'état d'avant.
python3 redteam_lexique.py     # 3 — v135 (C-065) : aucun terme banni affiché, aucun point nouveau hors de l'exception du dessin (dette : lexique-dette.json). --sonde=terme|point : il rougit.
python3 redteam_palettes.py    # 58 (v135 : trois ouvertures, les teintes PEINTES de chaque pastille, la pagination en barrettes) — v133 (C-057) : le menu des palettes du Studio, deux thèmes, deux ouvertures, les 24 pastilles touchées une à une ;
                               #   l'ordre en dur, Primesautier en tête. Rougit sur l'état d'avant (22/32).
python3 redteam_toucher.py     # 21 — v133 (C-058) : vingt mondes, trois dalles touchées au vrai doigt : la fiche de la bonne parole s'ouvre.
                               #   ⚠ VERT sur l'état d'avant : le défaut de Tom n'est pas reproduit.
python3 redteam_dessin.py      # 79 (v133 : ✕ de sortie, 16 pt, rangée centrée, mur des couleurs ; sondes quitter, centre, mur) — v132 (C-042) : le dessin dans l'app — couleurs figées (trois traits, trois palettes), masquage absent du partage, aucun outil
                               #   sur la surface, retour exact après POSER, joignabilité et VoiceOver, les entrées. Cinq sondes (--sonde=) : il y rougit.
python3 redteam_entier.py      # 36 — v131 (C-051) : toucher une photo dans la bande l'ouvre en entier (fond seiche plein, image entière) ; un toucher, ✕ ou
                               #   closeAll referme, la fiche intacte ; une dalle n'ouvre rien ; VoiceOver. Au vrai doigt. Rougit sur v130 (16/36).
python3 redteam_reactif.py     # 31 (v131 : la liste de l'Aura = TOUTES les tenues) — v130 (C-049) : planter, tenir, retirer par les vrais boutons ; l'Index, le Fil, la liste de l'Aura et le fil du Cercle
                               #   sont à jour à l'image suivante, complets — écran resté affiché, ou ouvert ensuite. Rougit sur v129 (25/30).
python3 redteam_motmarque.py   # 4 — v129 (C-046) : l'encre du mot de la nature (PROMI, CHICHE, CERCLE) est à la même hauteur dans son encart, ± 0,5 pt,
                               #   clair et sombre (capture @3x). Rougit sur sauvegardes/app-avant-v129.html (0/4 : CERCLE 2,7 pt trop haut).
python3 redteam_retour.py      # v127 (C-028) — LE RETOUR EXACT : 105 mouvements de repos forcés sur 15 mondes, 0 pixel d'écart au retour (égalité stricte,
                               #   canevas entier, WebKit) ; les mouvements ont bien lieu. Rougit sur la version de v126 (Touffe). ≈ 10 min, seul.
python3 redteam_fluide.py      # 5 — v124, TENIR EST FLUIDE : 20 animations, aucune image au-delà de 20 ms de travail du fil principal, p95 ≤ 16,7 ms
                               #   (trace Chromium, vrai GPU, @3x) ; la durée (1 000 ms) et les deux états. Rougit sur app-avant-v124 (2/5). ≈ 3 min.
python3 redteam_bouton.py      # 33 — v124, « PARTAGER MA PELOTE » : PromiLate 15 px, capitale = celle du trait ; couleur de la palette ≠ poils ≠ corps,
                               #   ≥ 3:1, jamais kaki, 50 ouvertures × 4 palettes. Rougit sur app-avant-v124 (26/33).
python3 redteam_garder_toile.py # 29 — v124, « Garder ta Toile » : gras, teinte retirée à chaque retour (20 × 2 palettes × 2 thèmes), ≥ 4,5:1. 15/29 avant.
python3 redteam_corps.py       # 25 — v123, LE CORPS DE LA PELOTE : 50 ouvertures × 4 palettes — ΔE00 ≥ 15 face au poil (rampe et image), jamais kaki,
                               #   jamais le ton du sol, tiré au hasard. Lu sur la peau PEINTE. Rougit sur app-avant-v123 (16/25). ≈ 25 min.
python3 redteam_registre.py    # 6 — v126, SENTINELLE : aucun chantier ne disparaît de CHANTIERS.md (numéros sans trou, aucun perdu depuis les commits passés,
                               #   états de la liste). Sans navigateur. Rougit sur une copie amputée d'une ligne.
python3 redteam_vivant.py      # v126 (C-028) : la Toile vit au repos — 3 min par monde, douze mondes vivent, huit immobiles ; intervalle ≥ 5 s, jamais
                               #   périodique, ≤ 2 dalles, ≤ 4 % de la Toile, retour à l'image d'avant, boucle arrêtée entre deux. ≈ 65 min ; --duree= --mondes= --fixe.
python3 redteam_pelote_doigt.py # 7 — v126 (C-029) : sous le doigt, image p95 ≤ 22 ms (banc WebKit), ΔE00 ≤ 2 contre le peintre, aucun poil au processeur. --temoin rougit.
python3 redteam_ramage_onde.py # v126 (C-009) : ⚠ ROUGE — le saut d'ensemble à la fin de l'arrivée d'une plume (5 à 16 % ; décidé ≤ 2 %). Le défaut est ouvert.
python3 redteam_mesure.py      # 10 — v125 : `?mesure=1` ne décale rien, son cadre ne couvre pas la Pelote. Rougit sur l'état d'avant (8/10).
python3 redteam_zone.py        # 8 — v125 : rien ne peint derrière la Pelote hors halo et ombre ; le halo n'a pas de second bord (≤ 30 % en 6°).
                               #   30 ouvertures × 2 thèmes (≈ 4 min). Rougit sur l'état d'avant (B, deux thèmes).
python3 redteam_decisions.py   # 79 — v122 : CHAQUE DÉCISION DE COULEUR DE TOM (en dur, avec sa source) contre l'écran rendu — fiches Promi,
                               #   Chiche, Cercle, page +, Index, deux thèmes. Rougit sur app-avant-v122 (77/79).
python3 redteam_maparole.py    # v122 : #FB4C0D et #FF7A55 n'existent QUE dans la phrase des murs (« Ma Parole ! ») — source, rendu, au doigt.
                               #   --statique (sans navigateur) ; --sonde rougit. Rougit sur app-avant-v122.
python3 redteam_flash_etat.py  # 10 — v123 (Q375) : + la première image d'une fiche porte SON état (six enchaînements, lus après l'image) · v122 (Q374) : aucune image orange sur l'à-qui, l'échéance et « trace pour tenir » d'une fiche à tenir en
                               #   sombre, 20 ouvertures, capture à la première image. Rougit sur app-avant-v122 (1/4).
python3 redteam_couleurs_ref.py # v121 — LES COULEURS SONT CELLES DE v118 (commit 578ec80, servi avec son moteur) : styles calculés, canevas et
                               #   dalles rendues seules (synchrones, horloge figée), 36 écrans × 2 thèmes. Exceptions nommées en dur (Toile
                               #   entière, orange des murs, Pelote et halo, violations retirées). Rougit sur app-avant-v121 (480 écarts : le brun
                               #   à la place de la seiche). ≈ 15 min, SEUL, simulateur éteint.
python3 redteam_plein.py       # 75 — v120, LA PELOTE EST PLEINE : alpha 255 en retrait de 4 % de D, deux thèmes, chaque palier, quatre palettes,
                               #   trois densités ; la silhouette n'a pas bougé. Rougit sur app-avant-v120 (36 rouges).
python3 redteam_enfonce.py     # 14 — v139 (C-083) : le toucher de la Pelote, au vrai doigt avec rayon de contact : la profondeur croît à chaque image, sa vitesse décroît, aucun saut, butée, deux tailles de contact → deux empreintes, retour lent. 6/14 sur l'état d'avant.
python3 redteam_cadre.py       # 22 — v139 (C-085) : la photo d'une fiche se cadre au pincement (1:1) et au glissement, mémorisée ; « Enregistrer la photo » en plein écran ; fiche Promi, Chiche, page +. 8/21 avant.
python3 redteam_dessin_photo.py # 15 — v139 (C-086) : plume 2 · 6 · 14, points à l'échelle ; photos importées dans le dessin (déplacer, pincer, poser), jamais emportées au partage.
python3 redteam_gestes.py      # 116 — E1 (C-074) : la main fantôme, geste par geste (apparition, A2, A1, drapeau, rechargement, « Revoir les gestes » au doigt, mouvement réduit). ≈ 25 min ; --seul=<id> ; --sonde rougit.
python3 redteam_engagement.py  # E0 (C-073) — la grille du chantier d'engagement : R1 lexique + A3 (aucun impératif), R2, R3, R4 (inactif avant E3), R5, R6, R7, A2. À PASSER À LA FIN DE CHAQUE LOT E. --sonde : il rougit. ⚠ 8/9 à la naissance : R6 rouge jusqu'à E2.
python3 redteam_verrou_onboarding.py # 9 — E0 : stockage vierge → l'onboarding s'affiche ; terminé ; deux rechargements → il ne revient pas. --sonde : il rougit.
python3 redteam_bord.py        # 8 — v137 (C-002) : la Pelote n'a pas de liseré — ΔE médian ≤ 5 entre la bande du bord et l'intérieur voisin, quatre palettes × deux thèmes × trois ouvertures (@3x). 3/8 sur l'état d'avant.
python3 redteam_partage_dessin.py # 34 — v137 (C-068) : une photo n'est jamais dans l'image partagée ; un dessin porte le logo en bas à gauche, avec et sans la mention (réglage au doigt) ; un dessin masqué n'est jamais emporté. 8/34 avant.
python3 redteam_halo.py        # 10 — v136 (C-071), RÉÉCRIT : AUTOUR DE LA PELOTE IL N'Y A QUE LA PAGE — aucun nœud de halo ni d'ombre, l'anneau 125–150 pt et la place de l'ombre
                               #   sont le fond de la page (@3x, deux thèmes), le bouton à 435,47. 2/10 sur l'état d'avant. Original : sauvegardes/redteam_halo-avant-v136.py.
python3 redteam_garder.py      # 18 — v119 (Q370), repris en v121 : « garder de côté » garde le titre et la personne de la phrase, au doigt.
python3 redteam_souffle.py     # v117 (Q364 → A) : la Pelote respire par la lumière du velours — rien ne change au-delà de la
                               #   silhouette ; sommet à 4,6 s et retour à 10,6 s APRÈS LA PREMIÈRE IMAGE (horloge réelle) ;
                               #   immobile avec Réduire les animations. Rougit sur app-avant-v117b.
```

**Aucune livraison si une batterie régresse.**

> ### ⚑ CHAQUE LOT SE TERMINE PAR UN COMMIT — ET LE HASH FIGURE DANS LE RAPPORT
> **Décision Tom, 1er octobre 2026.** Le dossier est un dépôt git depuis ce jour (branche `main`, premier commit
> « État au 1er oct. 2026 — v117 »). **Chaque lot se termine par un commit « vNNN — résumé »**, et **son hash figure
> dans le rapport de livraison. Un rapport sans hash n'est pas livré.**
> Avant de commiter : `git status` (rien d'inattendu), et `find . -type f -size +10M -not -path './.git/*'` — git ne
> sait pas filtrer par taille, un fichier neuf de plus de 10 Mo se nomme dans `.gitignore`. Les planches, les captures
> et les images de `scratchpad/` et de `sauvegardes/` ne sont pas versionnées (`.gitignore` en donne la liste).

> **⚠ LES BATTERIES SE PASSENT EN SÉRIE, JAMAIS TOUTES EN PARALLÈLE.** (Mesuré, 20 août 2026.)
> Douze Playwright lancés d'un coup font ramer la machine, et **les rouges qu'on lit alors
> sont faux** : boîtes à 0 × 0, « 0 pastille trouvée », classes d'un écran qui bavent sur le
> suivant. Relevé : `champs` 11/21, `pastilles` 8/12, `enchaine` 17/24, `tonsurton` 23/26,
> `fonctions` 20/22 — **et 22/22, 12/12, 24/24, 26/26, 22/22 en les repassant une par une,
> sans toucher à une ligne.** C'est le même piège que le §8 (« l'app rame, les captures
> échouent ») : un contrôle qui mesure une machine saturée ne mesure pas le produit.
> **Deux ou trois à la fois au maximum.** Un rouge apparu dans une passe parallèle se
> reconfirme en série avant d'être cru.

> ### ⚠ UN CONTRÔLE QUI ENCODE UNE RÈGLE ABANDONNÉE SE MET À JOUR AU NIVEAU DE LA DÉCISION
> **Jamais en modifiant le comportement pour le faire passer.** (Décision Tom, 18 août 2026,
> à la livraison de la section 4.)
>
> Une batterie est un contrat. Mais un contrat peut être **périmé** : il arrive qu'un
> contrôle vérifie une règle que le produit a **abandonnée** depuis. Trois cas déjà vus —
> « sens », « quand », et « **seuls les urgents ont un aplat** », qui supposait que l'état
> vivait dans le FOND du bloc d'Index. **Il vit dans la LIGNE** : le champ dit la nature, la
> ligne dit l'état — c'est la loi du produit (§3). Le contrôle était périmé, pas l'écran.
>
> **La marche à suivre, dans cet ordre :**
> 1. **Nommer la règle** que le contrôle encode, et **la décision** qui l'a remplacée.
>    S'il n'y a pas de décision écrite, il n'y a pas de contrôle périmé : c'est une régression.
> 2. **Réécrire le contrôle au niveau de la nouvelle règle** — même intention, nouveau nœud,
>    nouvelle propriété. « Seuls les urgents ont un aplat » est devenu « aucune carte n'est
>    peinte d'une couleur d'état ». Le contrôle continue de protéger la même chose.
> 3. **Garder la version d'origine** à côté (`sauvegardes/redteam_*-avant-S*.py`).
> 4. **Le dire dans la livraison**, en propres termes : *j'ai réécrit un contrat de test*.
>
> **UNE BISSECTION NE VAUT QUE SI CHAQUE CORRECTIF EST RÉTABLI EN ENTIER.** (Décision Tom,
> 18 août 2026.) Un correctif en trois morceaux — une règle, un champ, un libellé — rétabli
> pour un tiers seulement **innocente un coupable**. Vécu : le retrait de « URGENT » faisait
> passer la section 2 de 0 à 212 écarts ; je n'ai rétabli que le réglage de Peaufiner, pas le
> champ du formulaire ni le mode de la Toile, et j'ai conclu qu'il n'y était pour rien. J'ai
> ensuite cherché ailleurs pendant cinq mesures. **On réapplique dans l'ordre, un correctif
> entier à la fois, et on mesure après chacun** — jamais par bissection sur des suspects.
>
> **⚠ UN CONTRÔLE QUI COMPTE DES PIXELS SUR UN CANEVAS MESURE LA RESPIRATION DU MONDE.**
> (Décision Tom, 19 août 2026.) `Toile.dalleTrame` anime la matière avec `performance.now()`
> **et recadre au plus juste sur l'alpha** : ni les pixels ni même le format d'une dalle ne
> se répètent d'un rendu à l'autre. **Un contrôle bâti dessus flotte, et son flottement n'est
> ni le hasard ni les polices : c'est le TEMPS.** Trois l'ont fait pendant tout le projet —
> « Mes Promi : les intitulés restent », « le % s'affiche », « le % porte la double encre ».
> **La parade : comparer LA COMPOSITION, pas la peinture.** L'app publie ce qu'elle vient de
> composer — `window._plancheComp`, `window._noyauSig`, `window._sigEncres`,
> `window._nueeSemis` — et le contrôle lit ça. La règle protégée ne bouge pas ; c'est le nœud
> visé qui devient le bon. Les trois sont stables sur trois passages depuis.
>
> ### ⚠ QUAND UN CORRECTIF NE TIENT PAS, CHERCHER QUI D'AUTRE ÉCRIT LA MÊME PROPRIÉTÉ
> **Décision Tom, 3 septembre 2026. Le motif est revenu QUATRE FOIS en deux jours.**
>
> **Corriger une seule passe ne suffit jamais quand deux passes écrivent la même chose.**
> Deux propriétaires se défont l'un l'autre selon le moment ; le symptôme ressemble à du
> flottement temporel, et on perd des heures à durcir la mauvaise passe.
>
> ```
> echelle() / etatsDeCarte()   un inline retiré par celui qui ne l'avait pas écrit
> #shMode                       repris dans #shcSujet par l'ancien lot du partage
> #shcBarre                     posée à 700 par un lot, à 746 par l'autre
> enteteLisible / encreUn       le second repeignait le plateau par-dessus le premier
> ```
>
> **Ce que ça a coûté à chaque fois :** sur `etatsDeCarte`, TROIS correctifs successifs —
> rendre la passe idempotente, envelopper le moteur de l'Index, poser un observateur de
> largeur — et aucun ne pouvait rien, puisque le défaut était dans la passe d'à côté. Sur
> le partage, deux sondes de contrôle ont été **avalées par le conflit** et m'ont fait
> croire pendant trois essais qu'un contrat ne mordait plus.
>
> **La marche à suivre :**
> 1. **Piéger le peintre, ne pas relire le code.** On enveloppe `style.setProperty` sur le
>    nœud et on journalise la pile d'appels. Le plateau vide de la page + a été trouvé en
>    une minute par là, après une demi-heure de lecture stérile.
> 2. **Nommer UN propriétaire, et lui donner LE DERNIER MOT.** L'ordre d'appel suffit
>    souvent : `etatsDeCarte()` déplacée de la tête à la fin de `echelle()` a réglé seule ce
>    que trois correctifs n'avaient pas su faire.
> 3. **N'exempter que le geste fautif, jamais le traitement.** Sortir `.s4-et` de tout
>    `echelle()` a fait passer `releve-S4` de 0 à 34 écarts : le plancher ne s'appliquait
>    plus. On saute le RETRAIT, pas la décision.
> 4. **Une sonde qui « n'est pas prise » peut être avalée, pas manquée.** Vérifier qu'elle
>    s'applique vraiment — mesurer le nœud — avant d'accuser le contrôle.

> ### ⚠ UN CONTRAT RÉÉCRIT SE PROUVE CONTRE UN VRAI DÉFAUT — SINON IL NE MESURE PLUS RIEN
> **Décision Tom, 2 septembre 2026, née du lot du pinceau.**
>
> Réécrire un contrôle au niveau de la décision ne suffit pas : **il faut prouver qu'il mord
> encore.** Un contrôle réécrit qui ne trouve plus rien peut être juste — ou éteint. Les deux
> se ressemblent exactement dans un rapport vert.
>
> **La marche à suivre : on fabrique le défaut que le contrôle est censé attraper, on le pose
> dans l'app, on relance, et on vérifie qu'il est PRIS.** Puis on retire la sonde.
>
> **Le cas qui a fondé la règle.** `releve-S3` vérifie que rien ne déborde du cadre. La rangée
> du pinceau la faisait rougir 112 fois — son rail fait 1070 de large dans un conteneur en
> `overflow:hidden` de 390. J'ai réécrit le contrôle pour qu'il « confirme AU DOIGT », comme le
> §8 le prescrit pour les recouvrements : rouge à zéro, tout paraissait réglé. **Le contrôle
> était mort.** `.frame` rogne tout : **rien n'est jamais visible hors de l'appareil**, donc
> `elementFromPoint` ne trouve jamais rien, quel que soit le débordement. Prouvé avec une sonde
> de 150 px posée à x 300 dans un cadre de 390, sans ancêtre rogné : **zéro prise**. La bonne
> réécriture exempte ce qui se DÉCLARE (`data-glisse`, la rangée glissante de Q128 §3) et
> **sous condition** — le conteneur doit tenir dans le cadre ET rogner ; la même sonde est
> alors prise sur les 28 cadres.
>
> **Corollaire : le piège du §8 a une portée.** « Un débordement se confirme au doigt » vaut
> pour les recouvrements **DANS** la page, où un ancêtre rogné peut mentir. À la **frontière de
> l'appareil**, c'est le rectangle qui dit vrai — sur un vrai téléphone il n'y a pas de `.frame`
> pour rattraper ce qui sort.

> ### ⚑ LA COMPOSITION PUBLIÉE EST UN POINTEUR, JAMAIS UN VERDICT (assainissement, 30 sept. 2026)
> Deux règles de ce fichier semblaient se contredire : « on lit la composition publiée » (`_plancheComp`, `_noyauSig`…, pour ne pas
> mesurer la respiration d'un canevas) et « un juge qui lit la valeur qu'il vérifie ne vérifie rien ». **Elles se lisent ensemble :**
> une composition publiée par l'app sert à TROUVER où regarder (quel bandeau, quel bloc, quelle case) ; le VERDICT vient de ce qui est
> réellement peint ou écrit — les pixels (par différence, horloge figée), le tracé piégé (`fillText`, `drawImage` sur le canevas), le
> DOM rendu — ou d'une valeur décidée écrite en dur. Réécrits sur ce principe le 30 sept. : `redteam_toile` (le % et ses encres au
> tracé), `redteam_geste` (le Noyau lu sur l'image, sa place comparée au doigt), `redteam_pelote_partage` (le recouvrement sur les
> vrais `drawImage`), `redteam_zoom` (le rond lu à l'écran). Les règles que portent les juges : `SPEC-JUGES.md` (engendré).

> ### ⚠ UN JUGE QUI LIT LA VALEUR QU'IL VÉRIFIE NE VÉRIFIE RIEN
> **Décision Tom, 10 septembre 2026.** Vécu au portage de la Pelote : le juge comparait la vitesse de
> rotation à `_aura.G.AUTO` — la valeur que l'app DÉCLARE. Changer la vitesse dans l'app changeait donc
> la cible avec : il aurait accepté n'importe quelle vitesse. **Une valeur décidée s'écrit EN DUR dans
> le juge** (`AUTO_DECIDE = 2π/100` — un tour en 100 s ; ⚑ v135, Tom : « 100 s, comme dans l'app » ; ce fichier écrivait 2π/120 —, avec la décision qui la fixe), et le juge vérifie AUSSI que l'app
> déclare bien cette valeur. Vaut pour toute cote, toute durée, toute couleur : le juge porte la
> décision, l'app la respecte — jamais l'inverse.
>
> ### ⚠ UN CONTRÔLE QUI NE PREND PAS LA VERSION FAUTIVE NE VAUT RIEN
> **Décision Tom, 10 septembre 2026.** Vécu le même jour : le retour de l'empreinte SAUTAIT à la
> fin (déformé → lisse d'un coup). J'ai écrit un contrôle du « dernier pas » — et avant de juger la
> correction, je l'ai passé sur la version FAUTIVE : **il était vert.** Il comptait la **part des
> pixels qui changent** d'une image à l'autre ; or un retour lisse en change déjà beaucoup, d'un
> rien, à chaque image (médiane 17 %), et le saut (44 %) passait dessous. **Une part de pixels ne
> voit pas une AMPLITUDE.** Réécrit en écart moyen, en niveaux : la version fautive est prise à
> 8,45 niveaux, la corrigée passe à 0,46.
> **La règle : tout contrôle neuf se passe D'ABORD sur la version fautive, et il doit y ROUGIR —
> avant de servir à valider quoi que ce soit.** Le défaut que Tom a vu est la sonde : si le
> contrôle ne le prend pas, c'est le contrôle qui est faux, pas la correction qui est juste. Et
> **choisir la grandeur qui a la forme du défaut** : un saut est une amplitude, un débordement une
> position, une traîne une durée — pas un comptage qui les mélange.

> ### ⚠ UNE DALLE SE LIT PAR SA TEINTE — UN SEUIL DE LUMINANCE SEUL MENT DANS LES DEUX SENS
> **Décision Tom, 10 septembre 2026, au juge de la Pelote :** *« Deux couleurs de même clarté et de teintes
> opposées se distinguent parfaitement ; un seuil de luminance seul déclarera illisible ce qui se lit et lisible
> ce qui ne se lit pas. »* Mesuré sur les îles de la sphère, à vue figée : une dalle ORANGE sur la sphère bleue
> se lit franchement à **21,7** d'écart de luminosité ; une dalle pâle en clair ne se lit presque plus à
> **22,6** — l'ordre est inversé. En écart de COULEUR (ΔE, CIELAB, couleurs moyennes au cœur de l'île, avec et
> sans elle) : **84 contre 11**. Et le 42 du §3 aurait condamné une dalle blanche parfaitement lisible (25 à 39).
> **La règle :** la lisibilité d'une matière colorée — une dalle, une île — se mesure en **ΔE** ; le seuil de
> luminance du §3 garde son objet (un TRAIT sur un aplat) et ne se transpose pas. **Un critère de luminance peut
> s'AJOUTER** — il attrape autre chose : une dalle juste en teinte mais noyée en clarté. Plancher de la Pelote :
> **ΔE 15** (Q192). **Corollaire de l'instrument :** chaque objet se mesure LÀ OÙ LE MOTEUR LE POSE, jamais dans
> un masque seuillé — le masque fragmente l'objet pâle, un filtre de taille en jette les morceaux, et le plus
> illisible sort de la mesure par construction (voir la ligne du §8).

> **Ce qui reste interdit :** desserrer un seuil, retirer un contrôle, ou changer le
> comportement de l'app pour faire passer un test. Un simple **changement de nom de nœud**
> (`.ix-bloc` → `.s4-carte`) ne relève pas de cette procédure : c'est un renommage,
> l'intention est intacte — on le note, on ne délibère pas.

> ### ⚠ UN CONTRÔLE QUI PREND UN DÉFAUT ALÉATOIRE N'EST PAS INSTABLE — IL FAIT SON TRAVAIL
> **Décision Tom, 11 septembre 2026 :** *« un contrôle qui prend un défaut aléatoire une fois sur trois n'est pas
> instable, il fait son travail. Un relancer vert ne l'annule pas. »* Né du chantier 59 : la couleur d'une dalle est
> tirée au hasard à chaque chargement (`cc()`, `Math.random`), et quand le tirage tombe près du sol de la sphère la
> dalle ne se lit plus. `releve-aura` le prend en nommant la dalle — mesuré : **6 chargements sur 10** portent au moins
> une dalle sous le plancher (ΔE 15) ; dans la série du 11 septembre, « planter un arbre » à ΔE 12,2.
> **La règle :** quand le rouge nomme un défaut RÉEL que le produit tire au hasard, **le rouge est le résultat** ; le
> vert d'un nouveau chargement dit seulement que le tirage est tombé ailleurs. On ne l'écrit jamais « reconfirmé
> vert » : on écrit **« défaut du chantier n, pris à ce passage »**, et le défaut reste ouvert jusqu'à sa correction.
> **Ce que ce n'est pas — la distinction à faire AVANT de relancer :** le paragraphe suivant vise un INSTRUMENT qui
> oscille (il mesure la respiration d'un canevas, pas un défaut : le dessin est juste, c'est la sonde qui flotte). Ici
> c'est le PRODUIT qui varie, et le contrôle le voit. **Le test :** le rouge nomme-t-il une chose fausse à l'écran, qu'on
> peut regarder ? Si oui, c'est un défaut, aléatoire ou non — relancer ne sert qu'à mesurer sa fréquence.

> **⚠ Contrôles à seuil de pixels non déterministes (comme la convention Toile).**
> Deux contrôles Playwright échantillonnent un **canevas animé** et **oscillent** — un
> échec isolé ne prouve **rien**, il faut relancer :
> - `redteam_toile` — « Mes Promi intitulés » (width/police) : oscille 14↔16/16.
> - `redteam_geste` — « **l'anneau est peint à sa nouvelle place** » : sonde pixel sur le
>   **fond Toile animé de l'écran Partage** (shCanvas, échantillons à 1,3 s). Oscille
>   12↔13/13. **12/13 se reconfirme en relançant ; deux échecs de suite ne suffisent PAS
>   à conclure à une régression** (le dessin de l'anneau, lui, est correct — sonde isolée
>   +1513 stable). *À réécrire :* comparer l'anneau à sa propre référence, comme pour la
>   Toile, au lieu d'un seuil absolu. Voir `CHANTIERS.md`.

### ⚑ 30 SEPTEMBRE 2026 (v114) — TOUTE PLANCHE SE FAIT EN deviceScaleFactor 3. (Décision Tom.)
> C'est la densité de l'iPhone. Une planche @2x (ou redimensionnée) ne montre ni le grain, ni le bord d'un volume, ni un filet
> d'un pixel. Le recadrage « à 100 % » d'une planche = 1 pixel d'image pour 1 pixel d'écran @3x.

### Vérification visuelle Playwright

```python
viewport = {'width': 390, 'height': 844}
device_scale_factor = 2
pg.wait_for_timeout(6800)   # minimum après navigation
pg.evaluate("()=>{var o=document.getElementById('promiOnb');
  if(o){o.classList.add('gone');o.style.display='none';}}")   # passer l'onboarding
```

Pour vérifier une couleur peinte dans un canevas, **échantillonner les pixels** —
c'est la seule méthode fiable :

```javascript
const d = g.getImageData(0,0,c.width,c.height).data;
for(let i=3; i<d.length; i+=300) if(d[i]>10) n++;
```

---

## 8. Les pièges connus — les relire avant de déboguer

| Symptôme | Cause réelle |
|---|---|
| Une règle CSS « ne marche pas » | Une règle postérieure l'écrase. Chercher **toutes** les occurrences du sélecteur. |
| Le texte est invisible | `-webkit-text-fill-color` diffère de `color`. |
| La dalle est délavée | `opacity` ou `filter` posé par une règle groupée avec `.tracant`. |
| La dalle est polygonale | `dalleTrame` appelé avec une échelle > 1. |
| Un canevas est vide | `peintMinis` appelé avant que le canevas soit disposé. |
| L'app rame, les captures échouent | Un `MutationObserver` qui s'auto-déclenche : la fonction observée modifie une classe, ce qui réveille l'observateur. **Toujours comparer l'état avant d'agir.** |
| Un bloc ne bouge pas | Le CSS ne déplace pas les blocs. Réordonner le DOM en JavaScript. |
| `cur` est nul | Sur une fiche de Nuée, c'est `curNuee` qui porte le groupe. |
| Un sélecteur ne correspond à rien | `personSheet` vit sous `.frame`, pas sous `.device`. |
| Le scroll est bloqué | Un `position: sticky` avec `bottom: 0` qui change de position en s'ouvrant. |
| Une règle `position`/`max-width`/`z-index` ignorée sur un enfant **direct** de `#createSheet` | `#createSheet>*:not(#csTrameCv):not(.closeb):not(.pd-drift)` (≈ l.9017) impose `position:relative;z-index:1;max-width:84%` — spécificité 2 id / 2 classes, bat un `#createSheet .x`. **Parade :** `!important` sur `position/top/left/max-width`, comme le fait déjà `.closeb` (l.9163). |
| Un canevas **sort du cadre par la droite** dès qu'on le range dans un bloc | **`#tenirCv`, le canevas du geste.** La section 1 le cloue en `width:390px!important · max-width:none` dans un `#tenirZone` en `position:absolute · left:0 · width:390` (≈ l. 14095). `left:0` se lit dans son **bloc englobant** : tant que c'est `#detailPoster` (padding 0), il part de x = 0 et tout va bien. Dès qu'un conteneur **positionné** (`position:relative/absolute`) ou **padé** de Peaufiner ou de la page + devient son ancêtre positionné, le canevas de 390 px repart de l'origine de CE bloc — mesuré à **x = 27, dépassement 27 px** — et « rien ne déborde » passe au rouge, un élément par thème. **Un correctif `box-sizing:border-box` empire**, il resserre la boîte sans toucher au canevas. **Parade : ne jamais faire entrer `#tenirZone` dans un conteneur de réglages.** Le geste reste là où la section 1 l'a posé. Voir QUESTIONS.md · S2/Q12. |
| **Un balai « hors inventaire » emporte un élément vivant** | **LE CRIBLE EN BLOC — deux fois.** Masquer une FAMILLE d'éléments (`#addPromi, #addNuee, …`, `#promiForm>*:not(…)`) emporte toujours quelque chose qu'un doigt ouvre : `#addPromi` est le bouton où mène la bascule du geste, `#csChoix` est le panneau des trois cadres « Choix ouvert ». `redteam_verbe` est tombé de 6/6 à 4/6 les deux fois. **Toute règle de balayage se vérifie ÉLÉMENT PAR ÉLÉMENT avant d'être posée** — on énumère les nœuds de CET écran, jamais un conteneur, jamais une famille. |
| **Une cote mesurée sur elle-même fait osciller l'écran** | **LA COTE SE CALCULE, ELLE NE SE MESURE JAMAIS SUR ELLE-MÊME — deux fois.** Décider d'une hauteur d'après une hauteur rendue crée une boucle : `choixOuvert()` testait `#csChoix.height > 40`, les cotes du §5 passaient ses éléments en absolu, le panneau retombait à 0, « ouvert » devenait faux, les cotes revenaient au repos, les éléments repassaient en flux, il remontait. Le mot de trace était relevé à 236 **et** la phrase à 392 dans le même passage. **L'état est la classe que le code pose** (`.ouvert`), jamais la géométrie qu'il vient de produire. |
| Un panneau qu'un geste ouvre fait **osciller** l'écran d'une passe à l'autre | **Un état ne se lit JAMAIS dans la hauteur rendue du panneau.** Sur la page +, `choixOuvert()` testait `#csChoix.height > 40` : dès que les cotes du §5 passent ses éléments en absolu, le panneau retombe à 0 de haut → « ouvert » devient faux → les cotes reviennent au repos → les éléments repassent en flux → il remonte. Le mot de trace était mesuré à 236 **et** la phrase à 392 dans le même relevé. **La classe posée par le code (`.ouvert`) EST l'état** — la géométrie ne l'est jamais. |
| La phrase de la page + sort trop grosse, toujours large de 342 | **L'estimation du §2.8 est la règle, la mesure navigateur n'est qu'un garde-fou.** C'est l'estimation `Σ(car × taille × 0,53) + 32/pastille + 11/écart` qui a composé le moodboard : elle redonne 29 · 29 · 31 · 36 · 35 · 33 · 29 · 30 au caractère près. La mesure seule remplit toujours les 342 px. **On prend la plus petite des deux** : l'estimation compose, la mesure empêche une ligne de casser (et une ligne qui passe à la ligne décale tout de 32 px, §2.5). |
| Un geste n'ouvre plus rien après un « nettoyage » d'écran | **Un crible posé EN BLOC casse ce qu'un geste ouvre.** Porter un écran depuis son inventaire veut dire : *ce que le §5 ne liste pas ne se peint pas*. Mais cette règle vaut pour **l'état AU REPOS de l'écran courant**, jamais pour les panneaux qu'un doigt déplie — qui sont eux-mêmes **des écrans de l'inventaire** (« Choix ouvert · écrire un mot / choisir une personne / l'échéance », cadres 18 à 23 ; les contrôles dépliés de Peaufiner). Fermer un conteneur d'un coup (`#promiForm>*:not(…)`, `#csPhrase>*:not(…)`) ferme aussi `#csChoix` : `redteam_verbe` tombe de 6/6 à 4/6 sur « la bascule mène à un vrai bouton » (`vis:false`, mesuré, deux thèmes). **La liste des nœuds autorisés se construit PAR ÉCRAN, nœud par nœud — jamais par conteneur.** C'est ainsi que Peaufiner a donné 7 sur 9 en un lot : la liste y était bâtie élément par élément depuis le §5. Voir QUESTIONS.md · S3. |
| **On grossit un texte et l'écran se resserre partout** | **UNE COTE DÉRIVÉE N'EST PAS UN ESPACE — C'EST « HAUTEUR DU BLOC + AIR ».** Monter une taille ne déplace aucun `top` : c'est la HAUTEUR qui grandit, vers le bas, et l'air se mange en silence dans toutes les cotes calculées pour l'ancienne taille. Aucun relevé de POSITIONS ne peut le voir. Vécu : l'à-qui passé de 21 à 23 a fait tomber `à qui → titre` de **6,9 à 4,7 px sur les cinq états de fiche**, et l'état de 12,5 à 13,5 a mangé 1,1 px sous chaque fiche et chaque Nuée. **La parade : écrire la cote dans la bonne unité** — `yTitre = yQui + quiFs × 1,10 + 6,9` redonne le 30 du moodboard à 21 px et garde l'air à 23. Contrôlé par **`redteam_air.py`**, qui mesure l'ESPACE RÉEL entre deux blocs de texte (bas de A → haut de B) sur 36 écrans et refuse tout resserrement. |
| **Un écran sort vide, ou porte les blocs d'un autre** | **RIEN NE SURVIT À `closeAll` — NI CE QU'UN ÉCRAN MASQUE, NI CE QU'IL POSE, NI CE QU'IL BÂTIT.** Trois couches, et il a fallu les trois. **1 ·** un `display:none` en ligne survit à l'écran qui l'a posé → on le marque (`data-masque`) et `closeAll` le rend. **2 ·** les propriétés posées en ligne survivent aussi : le Peaufiner d'une Nuée clouait `#dpdCorps` en `display:block!important; position:absolute; z-index:30`, et le tiroir d'origine (« le potager », MEMBRES, PIÈCES) se peignait **par-dessus le titre de la fiche suivante, tiroir fermé** → `pose()` note ce qu'il écrit (`data-pose`), `closeAll` retire exactement ça. **3 ·** les nœuds bâtis survivent → un écran qui bâtit **inscrit son rangeur** dans `window._rangeurs`, que `closeAll` passe tous. Contrôlé par **`redteam_vide.py`**, qui **enchaîne** les écrans sans recharger — les autres batteries ouvrent chaque écran sur une page fraîche et ne peuvent pas le voir (mesuré : 28/61 sur la version fautive, 61/61 après). |
| **Un nœud neuf est « masqué » alors qu'il est en `display:block`** | **LE CRIBLE D'UNE AUTRE SECTION.** À l'ouverture du Peaufiner, le poster prend `s2-ouv` — le crible de la SECTION 2, écrit pour une fiche de **promesse** : il passe en `visibility:hidden` tout ce que SON inventaire ne liste pas. Les cartes d'une Nuée n'y sont pas : mesurées à `display:block` **et** invisibles, sur les quatre écrans. **Parade : ne pas toucher au crible** (il protège sa section) — **déclarer les nouveaux nœuds visibles, nommément**. Un crible se pose nœud par nœud, et se lève de même. Voir QUESTIONS.md · Q66. |
| **Une cote de fond survit au moteur qui l'a remplacée** | **UNE BANDE FIGÉE.** `.device #detailPoster.dp-nuee::before` clouait la zone haute d'une Nuée à **232,67 px**, valeur d'un lot antérieur au moteur géométrique. Invisible tant que la boîte du champ était plus haute ; **elle dépasse dès que le champ se réduit** (114 px à l'état défilé → 118 px de rectangle à bord franc sous la vague). **Parade : la faire suivre la boîte, pas la supprimer** — elle est le fond sur lequel le canevas se pose. Variable `--nuee-bande`. |
| **Un `:not(#id)` pèse l'id qu'il contient** | **`#settingsScreen > :not(#stTrameCv){width:auto!important;max-width:none!important}`** compte **DEUX ids** — celui du sélecteur et celui du `:not`. Il bat donc `#device .enh`, qui n'en a qu'un, **à `!important` égal**. Le plateau retombait en largeur automatique dans un parent `flex`, donc à la largeur de son contenu ; le titre rétrécissait pour tenir, ce qui rétrécissait encore la boîte : **342 → 242,7 → 209,4**, titre **27 → 19**, d'une passe à l'autre. **Parade : la géométrie se pose EN LIGNE avec `important`** (ce que fait déjà `.closeb`), avec des CONSTANTES du §5 — jamais une mesure, sinon la boucle revient. |
| **Un `display:contents` ne cache rien** | `#shTray`, l'ancien tiroir du partage, est en `display:contents` : **il n'existe pas pour la mise en page**, donc le masquer ne masque pas ses enfants — ils remontent dans le flux du parent. `#shNyPctRow` (« % d'harmonie ») flottait ainsi **sur le plateau du titre**, à y 58 → 87, opacité 0,34, qu'aucune règle de rangement ne pouvait atteindre. **Chercher les orphelins d'un écran refondu par leur POSITION, jamais par leur conteneur.** |
| **Un balayage de collisions annonce « 0 » sur des cadres qu'il n'a pas regardés** | **`document.elementsFromPoint` travaille en coordonnées de FENÊTRE.** Une planche fait plusieurs milliers de pixels de haut : **les cadres hors de la fenêtre rendent une liste VIDE**, donc aucun recouvrement, jamais — et l'outil sort un vert parfait. Trouvé le 3 septembre 2026 en essayant de prouver une AUTRE correction : deux textes superposés à dessein dans un cadre du bas **n'étaient pas pris**. **Tous les « 0 recouvrement » antérieurs de ce projet sont donc PARTIELS.** **Parade : on amène chaque cadre dans la fenêtre** (`scroll_into_view_if_needed`) **avant de l'interroger, cadre par cadre** ; et un point hors `[0,innerWidth]×[0,innerHeight]` se déclare **« non confirmé »**, jamais « pas de collision ». Corollaire : **une marque posée sur sa surface n'est pas un recouvrement** (une dalle peinte sur la frise, un visage dans son anneau) — on n'exempte QUE la containment géométrique, et seulement sur un canevas ou un SVG ; un texte qui **déborde** d'un canevas reste pris. Preuve : `scratchpad/preuve_collisions.py`. |
| **`getBoundingClientRect` ignore le rognage d'un ancêtre** | Un balayage de collisions comptait un recouvrement de **48 × 17** entre le mot-marque de l'aperçu de partage et le sélecteur de sujet. Il n'y en avait aucun : la zone est en `overflow:hidden`, et `elementFromPoint` au centre du mot-marque rendait `shMode`. **Un contrôle de recouvrement ou de débordement se confirme AU DOIGT** (`elementFromPoint` / `elementsFromPoint`), jamais au rectangle seul. Corollaire : le vrai défaut, lui, était ailleurs — l'aperçu était **rogné de 65 px en bas**, parce que `shareRender()` le centrait pour l'ANCIENNE zone. |
| **Un padding ne fusionne pas, une marge si** | Aux Réglages, l'écart entre le plateau et le premier bloc valait **28** : le `margin-bottom:28` de l'encart **fusionnait** avec le `margin-top:18` de `.grouplab` (marges adjacentes, le plus grand gagne). Remplacé par un `padding-top:28`, il ne fusionne plus : 28 + 18 = **46**, et le bloc tombait à 146 au lieu de 128. **Un espace repris en padding se calcule en retirant la marge du premier bloc** (ici 10 + 18). Même famille que « une cote dérivée n'est pas un espace ». |
| **Un enfant absolu d'un conteneur qui défile DÉFILE** | Trois écrans sont leur propre conteneur de défilement (`#auraScreen`, `#auraHelp`, `#plusScreen`) : leur plateau part avec le doigt, et **✕ FERMER avec lui**. `position:fixed` n'y change rien (l'ancêtre transformé devient le bloc englobant). **La parade validée est celle de l'Index :** le conteneur qui défile COMMENCE sous le plateau (`#indexList{top:212px}`) et rogne — rien ne peut monter plus haut. Sans quoi le contenu remonte **dans la bande au-dessus du plateau** (mesuré aux Réglages : « RÉCURRENCE · chaque semaine » à y 9, « ✦ Le Cercle » à y 33). |
| Idem sur un enfant **direct** de `#shareScreen` | `#shareScreen>*:not(#shareToileBg)` (≈ l.102) — même piège de spécificité. Même parade `!important`. |
| La phrase de la page + cesse d'alimenter un champ après un simple changement de **libellé** | La liaison phrase→formulaire cible ses champs par id (`#fTitle`, `#fWho`, `#csSens`) **mais aussi par le TEXTE affiché** : le mot **quand** cherche la pastille d'échéance par son libellé `+ tard` (présent dans `#dueChips` ET `#dfDueChips`, ≈ l.4938), pas par un id. Renommer le libellé casse la liaison **en silence**. Couvert par `redteam_phrase.py` (chantier 56). |

| **Une carte d'Index a la vague d'une FICHE** | `onde(base,amp)` cloue **période 1,5** (§2.1, une fiche) et **normalise par 390**, la largeur d'une fiche. Une CARTE veut **période 1, sur SA largeur** (§3.9). Appelée telle quelle sur une carte de 165, l'abscisse n'atteint que t = 0,42 : on voit deux cinquièmes de la courbe, étirés sur toute la carte — creux à x = 68 au lieu de 41, **écart médian 2,85 px**. `onde` prend deux paramètres facultatifs, `per` et `larg` ; sans eux, la fiche ne bouge pas. |
| **Une cote de fond se voit dès que la vague monte** | `--nuee-bande` est le fond DERRIÈRE le canevas d'une Nuée. Le canevas n'est opaque que **jusqu'à l'onde** : au-delà du point le plus HAUT de la vague, la bande se voit là où le corps commence. Mesuré : boîte 256, vague à 140 → **116 px de mauve à bord franc**. La borner au **minimum de l'onde**, jamais à la boîte. |
| **Un bloc posé à `left:0` dans un `.screen` sort rogné de 16 px** | **UN `.screen` NE COÏNCIDE PAS AVEC `#device`.** Mesuré le 30 août 2026 : `#studioScreen` et `#shareScreen` font **422 px** de large et commencent **16 px à gauche ET 16 px au-dessus** de l'appareil. Les cotes du document sont en écran **390 × 844** : posées à `left:0` dans un `.screen`, elles manquent 16 px à droite — le champ et la barre du Studio sortaient rognés. **Aucun relevé de positions ne peut le voir** : le dump divise par l'échelle (`dev.width/390`) et le décalage disparaît dans la division. **Parade : poser UN CADRE de 390 × 844 mesuré sur `#device`** (`dx = (device.left − screen.left) / (device.width/390)`, idem en y) et ranger tout dedans — les cotes redeviennent celles du document, sans un seul `calc()`. C'est ce que font `#stcCadre` et `#shcCadre`. ⚠ Sur `#shareScreen`, s'ajoute le piège de spécificité de la ligne suivante : `!important` obligatoire sur `position/left/top`. |
| **Une mise en page posée par un lot est défaite sans qu'on y touche** | **LE MOTEUR DE L'ÉCRAN SE REDIMENSIONNE LUI-MÊME.** `shareRender()` pose une taille en ligne sur `#shWrap` ; `buildStudio()` reconstruit `#studioBody`. Un lot qui ne repose sa mise en page **qu'aux événements du doigt** perd la main dès qu'une de ces fonctions est appelée d'ailleurs. Mesuré : après un `shareRender()` extérieur, le canevas repassait de **218 × 388 à 341 × 607** et le geste du Noyau tombait à côté — `redteam_geste` de 13/13 à 12/13, sur un contrôle (« l'aimant de la ligne du QR ») qui ne ressemble pas du tout à sa cause. **Parade : ENVELOPPER la fonction** (`var _f=window.shareRender; window.shareRender=function(){var r=_f.apply(this,arguments); requestAnimationFrame(reposer); return r;};`), jamais se contenter d'écouter. Même motif pour un libellé qu'un rotateur réécrit au hasard (`#stBuyTx`) : un `MutationObserver` **qui compare avant d'agir**. |
| **Un comparateur d'images ment sur deux points** | **1 · Il redimensionne.** `.frame` se met à l'échelle pour tenir dans la fenêtre : à un viewport de 390 × 844, `#device` sort à **363,87 px**. Capturer là et remonter à 390 met chaque glyphe entre deux pixels — aucun écran ne peut tomber à zéro. **430 × 932 donne `#device` exactement 390 × 844.** **2 · Il capture trop tôt.** Le compte de nœuds visibles se stabilise AVANT que tout soit peint : à 2 000 ms, une fiche sort sans sa dalle ni sa barre Peaufiner. Il faut un **plancher de temps** ET deux relevés identiques. **Avant d'accuser le dessin, on vérifie l'instrument.** |
| **Un `data-` posé par un peintre est lu par un autre** | `#dpTrameCv` est partagé par la fiche et la Nuée. Une base d'échelle (`data-matiere-base`) laissée par un autre peintre faisait sortir la zone de matière d'une Nuée à **59 px de haut au lieu de 194**. **Une boîte et sa base s'écrivent ensemble, d'un seul geste**, ou pas du tout. |
| **Un écran rouvert n'est plus celui de la première fois — et rien ne rougit** | **⚑ `#studioScreen` ET `#auraScreen` NE PERDENT JAMAIS LEUR CLASSE `.show`.** (Nommé le 22 sept. 2026, après la TROISIÈME fois qu'elle casse quelque chose.) `closeAll()` les ferme autrement — en les glissant hors champ — mais la classe reste posée. **Tout ce qui est accroché à un `MutationObserver` sur `.show` ne se réveille donc QU'UNE FOIS, au tout premier passage.** Les trois : ① le régulateur de densité de la Pelote n'appliquait jamais sa vise (seul un rechargement la faisait mordre) ; ② l'anneau des Noyaux ; ③ le semis du Studio — `buildStudio` repeint `#stBg` sans `_shAllColored`, `poseToile(true)` devait réparer, et ne rejouait jamais : **première ouverture juste, toutes les suivantes à 14 cellules colorées sur 72**. **Parades, dans cet ordre :** on n'observe JAMAIS une classe sans avoir vérifié qu'elle se RETIRE (une mesure, pas une lecture : `classList.contains('show')` après `closeAll`) ; ce qui doit se rejouer à chaque ouverture s'accroche à la FONCTION qui ouvre (on l'ENVELOPPE, §8) et non à un état ; et ce qui doit s'appliquer « quand personne ne regarde » s'accroche à `closeAll` et à `visibilitychange`. ⚠ **Et le symptôme ne ressemble jamais à sa cause** : un écran qui sort à moitié peint la deuxième fois, un réglage qui « ne prend qu'au rechargement ». Devant l'un des deux, chercher la classe AVANT le reste. |
| **Une animation fige tout le produit, alors qu'elle ne dessine que sur un écran** | **`offsetParent` NON NUL NE VEUT PAS DIRE VISIBLE.** Un écran fermé n'est pas en `display:none` : il est **glissé hors champ** (`translateY(100%)`, opacité 0) et **garde son `offsetParent`**. Toute boucle qui filtre « les écrans visibles » sur ce critère **écrit sur tout le produit**. Vécu le 10 septembre 2026 : `frame()` (ombre de dalle, ≈ l. 8917) écrit trois variables CSS **héritées** sur les **douze** écrans `.tuto-fond`, fermés compris, à chaque image — et sa propre lecture d'`offsetParent` à l'image suivante force le recalcul de style de milliers de nœuds cachés. **27 % du fil principal**, partout dans l'app ; l'élan de l'Aura en sortait figé (images de 267 ms). **Parade : un écran est visible s'il porte `.show`** (la classe que le code pose, §8 — jamais une géométrie). **Et au profileur, le temps de mise en page est attribué à la fonction qui LIT** (`offsetParent`, `getBoundingClientRect`), pas à celle qui a sali : chercher l'écriture ailleurs. → CHANTIERS.md, chantier prioritaire. |
| **Une mesure de dalles perd justement la plus illisible** | **UN MASQUE FRAGMENTE UN OBJET PÂLE, ET UN FILTRE DE TAILLE EN JETTE LES MORCEAUX.** Le juge de la Pelote retrouvait les dalles dans un masque « avec − sans » (seuil 12) et ne gardait que les composantes de 300 cellules : une dalle bleue sur bleu s'y découpe en morceaux de 1 à 274 cellules — **la dalle la plus illisible sortait de la mesure**, et « la plus faible » rapportée était la suivante (10 sept. 2026, Q192). **Parade : mesurer chaque objet LÀ OÙ LE MOTEUR LE POSE** (son centre, recoupé avec ce que l'app publie), jamais le retrouver dans un masque. **Et une dalle se lit par sa TEINTE** : la luminance confond l'orange qui se lit (Δlum 18) et le bleu sur bleu qui ne se lit pas (13) ; l'écart de couleur (ΔE, CIELAB) les sépare — 84 contre 9. |
| **Une porte s'ouvre et se referme aussitôt — au doigt seulement** | **LE CLIC FANTÔME.** Après un toucher, le navigateur synthétise mousedown / mouseup / click **au point du doigt, APRÈS `touchend`**. Une porte qui ouvre au lever du doigt (`pointerup`) ouvre AVANT ce clic — et le clic tombe sur ce qui vient de s'ouvrir : `#scrim`, dont le clic referme tout. Vécu le 11 sept. 2026 : la porte des dalles de l'Aura (`openDetail(139)` → clic sur `#scrim` → rien d'ouvert) **et la porte des Noyaux de l'Aura, d'origine** — sur un téléphone, toucher un Noyau n'ouvrait rien de visible. **Les juges jouaient à la SOURIS : à la souris ce clic arrive sur l'élément de départ, tout est vert.** **Parades :** une porte s'ouvre sur le `click` (le lever du doigt l'arme : même élément, sous le seuil) — `_porteAuDoigt` de lot-DALLE-PORTE ; et `lot-CLIC-FANTOME` avale un clic issu d'un toucher qui tombe sur une COUCHE OUVERTE PENDANT LE GESTE (sa couche `.show` n'était pas ouverte quand le doigt s'est posé) — jamais un clic de souris ni de script, jamais un clic sur une couche déjà ouverte. ⚠ Une première écriture comparait l'élément touché à l'élément cliqué : elle aurait avalé un vrai toucher sur un bouton redessiné sous le doigt, et aucune série (souris) ne l'aurait vu — **un garde se borne à la forme exacte du défaut**. **Toute porte se prouve AUSSI au vrai doigt** (`Input.dispatchTouchEvent`, contexte `has_touch`) : `sauvegardes/aura-trois/doigt_defile.py` (une porte), `balayage_fantome.py` (tout un écran, doigt contre souris). |
| **Un composant réutilisé sort sans sa mise en page** | **SON CSS EST RATTACHÉ À `#device`, ET LA FEUILLE VIT SOUS `.frame`.** La carte d'Index (lot-S4) est stylée par `#device .s4-carte` ; la fiche d'une personne vit sous `.frame`, hors de `#device` (le §8 le dit déjà pour `personSheet`). Ses vraies cartes, bâties par le moteur de l'Index, s'y **empilaient en colonne à x = 0**, sans aucune erreur (11 sept. 2026). **Parade : re-rattacher LES MÊMES VALEURS au conteneur qui accueille le composant, et l'écrire** — si le composant change à sa source, il doit changer là aussi. Et un moteur enfermé dans un lot se réutilise par SA porte publique (`_s4Index`, prêtée le temps d'un appel, tout rendu à l'identique) — jamais par une copie de la carte. |
| **Un bouton intercepté casse tout ce qui l'ouvre par programme** | **UN CLIC SCRIPTÉ N'EST PAS UN DOIGT.** Le + de l'accueil ouvre maintenant les trois natures sur place ; intercepter TOUT clic sur `#createBtn` a fait tomber `redteam_vide`, `pastilles`, `gens`, `tuiles` et fait planter `aveugle` (13 sept. 2026) — ils ouvrent la page + par `createBtn.click()`. **Parade :** un comportement de geste ne vise que `ev.isTrusted` ; un appel par script garde le chemin d'avant. Et **une commande déplacée garde ses gestionnaires** : on DÉPLACE `#createBtn`, `#filBtn`… dans le nouveau chrome, on ne les recrée jamais. |
| **Un libellé posé sur un canevas se mesure trop tôt** | **LA POLICE N'EST PAS ENCORE LÀ QUAND LA CARTE SE PEINT.** Le libellé « Promi » d'une carte d'Index mesurait **53** au moment de `peintCarte` et **64,5** ensuite : la dalle, décalée d'après la première mesure, passait 3,5 px SOUS le libellé (§4). Et en densité « 3 par ligne » (carte de 106), le décalage mangeait toute la largeur : **la dalle n'était plus peinte du tout** — seul `releve-S4` l'a vu. **Parades :** la largeur d'un libellé est une COTE relevée police chargée (Promi 65 · Chiche 72 · Nuée 60), jamais une mesure au moment de peindre (§8, « la cote se calcule ») ; sur une carte étroite la dalle descend sous le libellé. ⚠ Et **un peintre déclare la boîte qu'il a VRAIMENT peinte** (`data-matiere`, `data-matieres` pour une petite Toile) : la boîte d'avant décalage restait déclarée, et un contrôle qui ne lit que la déclaration ne voit pas une dalle écrasée à 0 — `redteam_reperage` compte donc aussi les pixels. |
| **On trie 41 règles à la main, et 37 ne peignaient rien** | **UNE RÈGLE QUI DÉCLARE UNE COULEUR NE LA PEINT PAS FORCÉMENT — ON TRIE LES SURFACES, JAMAIS LES RÈGLES.** Vécu le 17 septembre 2026 en finissant l'échange de rôle de la Nuée : **41 règles CSS déclaraient un aplat en `#291547`**, et il a fallu décider pour chacune si elle peignait un CHAMP ou un ACCENT — un tri long, à l'œil, sur 41 sélecteurs. **En mesurant le RENDU plutôt que les règles : quatre surfaces.** Les 37 autres étaient écrasées par une règle postérieure ou par le JS — le §7 le dit depuis le début (« 2 400 règles dont 54 % sont mortes »), mais on l'oublie dès qu'on lit une feuille de style. **Parade : on parcourt le DOM écran par écran, on lit le `backgroundColor` CALCULÉ, et on ne garde que ce qui se peint** (`scratchpad/surfaces_mauve.py`). Le tri tombe alors de 41 décisions à 4, et chacune se regarde vraiment. ⚠ **Et une classification automatique se trompe** : « grande surface qui porte du contenu = champ » sortait la barre Peaufiner en CHAMP et ratait qu'elle EST un champ pour une autre raison (elle porte la couleur de champ de sa nature sur les deux autres). **Le critère se décide à l'œil, la mesure ne fait que réduire la liste.** |
| **Un écran sort VIDE, et la console ne dit RIEN** | **UNE FONCTION ENFERMÉE DANS UNE IIFE, APPELÉE DEPUIS UNE AUTRE, SORT EN `ReferenceError` — ET LE `try/catch` DU MOTEUR L'AVALE.** Vécu le 17 septembre 2026 : un traducteur de couleur `_nt()` posé dans l'IIFE de `NATCOL`, appelé par les deux peintres de carte, qui vivent dans un AUTRE bloc. **L'Index sortait vide — zéro carte — sans une seule erreur en console**, parce que son moteur enveloppe chaque carte dans un `try/catch`. ⚠ **Et la sonde était VERTE** : elle mesurait le contraste des textes présents, et il n'y en avait plus aucun. **Seule la CAPTURE l'a vu.** **Parades :** une aide partagée entre deux blocs se pose sur `window`, jamais dans une IIFE — et **tout lot qui touche à un peintre se termine par une capture REGARDÉE**, plus un comptage du nombre d'éléments rendus (`#indexList .s4-carte` → 12, pas 0). Un contrôle qui ne compte que la qualité de ce qui est peint ne voit pas l'absence. |
| **Une flèche a un trait qui lui sort par la pointe** | **UN BOUT ROND DÉPASSE DE LA MOITIÉ DE SA LARGEUR.** Un trait qui s'arrête AU point d'arrivée le déborde de `lineWidth/2` quand `lineCap` vaut `round` — et si ce point est la POINTE d'un chevron, le trait sort par le V. Vécu le 23 sept. 2026 sur les deux flèches de la page + : le ruban du trait finissait à `cx + ep·0,6`, c'est-à-dire exactement où `chevron` pose sa pointe (`6·k`, `k = ep/10`) ; et la flèche d'invite du §2.4 finissait à `B` avec un cap de 4,5, donc 2,25 px au-delà de sa propre tête. **Parade : le trait s'arrête EN DEÇÀ** — sous les branches arrière du V pour le premier, de `lineWidth/2` pour le second — et c'est son bout rond qui vient tomber pile là où la tête se referme. |
| **On change de police et tous les textes auto-dimensionnés rétrécissent** | **UNE CONSTANTE DE LARGEUR MOYENNE EST CELLE D'UNE POLICE, PAS UNE LOI.** Le §2.8 estime une ligne par `Σ(caractères × taille × 0,53)`, et **0,53 a été relevé sur la police de la planche**. Depuis Gilbert (16 sept.), le coefficient réel est **0,44** (mesuré sur les mots réels, `scratchpad/coef_phrase.py`) : l'estimation sur-contraignait de 20 %, et la phrase de la page + sortait à **25 px là où la planche en compose 35**. Rien dans le code ne le disait ; seul l'œil de Tom l'a vu (« quand on avait l'ancienne police c'était pas aussi petit justement »). **Parade : toute constante qui traduit des CARACTÈRES en PIXELS se remesure au changement de police** — et on cherche ses sœurs (le 32 par pastille et le 11 par écart, eux, sont des px : ils ne bougent pas). |
| **Un filet posé en `box-shadow` est tronqué, et rien ne le recouvre** | **UNE OMBRE DÉBORDE DE L'ÉLÉMENT — DONC TOUTE BOÎTE QUI ROGNE LA COUPE.** `elementsFromPoint` ne trouve rien par-dessus (normal, rien n'y est) : c'est la RANGÉE qui clipe. `.au-nx` et `.aura-track` portent `overflow:auto hidden` parce qu'elles glissent. Mesuré en repeignant l'ombre **en rouge pur** et en parcourant les 360° : **96,4 % du tour, trou de 264 à 277°**, au sommet du plus grand disque. Rembourrer la rangée ne suffit pas (90,0 → 94,7 %) et déplace la composition. **Parade : ce qui doit cerner se peint DANS la boîte, et par le peintre lui-même, en DERNIER** — l'anneau finit exactement au bord de son canevas (`R + lw/2 = W/2`), le filet occupe ses 1,4 derniers pixels. Ce qui est dans la boîte ne peut être rogné ; ce que le peintre trace en dernier ne peut être recouvert par lui-même. ⚠ Et une passe EXTÉRIEURE qui peint dans un canevas est effacée au rendu suivant (mesuré : 0 % du tour). |
| **Deux titres à la même taille en pixels n'ont pas la même taille à l'œil** | **LA TAILLE EN PIXELS NE DIT RIEN SANS LA POLICE.** Mesuré à 27 px, police chargée : **PromiLate** cap 19,9 et « Réglages » large de **163,8** ; **Gilbert** cap 18,9 et large de **101,7** — une fois et demie plus étroit. Un relevé qui compare des `font-size` conclut « tous pareils » là où l'œil voit deux familles. **Parade : comparer la HAUTEUR DE CAPITALE et la LARGEUR RENDUES** (`measureText`, `actualBoundingBox*`), jamais la seule cote déclarée. |
| **Un texte auto-dimensionné reste coupé, et la boucle qui devait le réduire « tourne »** | **ELLE POSE SANS `important`.** Le titre d'une carte d'Index rétrécit tant qu'il déborde — `t.style.fontSize = fs+'px'` — mais `#device .s4-ti{font-size:24px!important}`, posée plus bas, gagne : la boucle tourne huit fois, `scrollHeight` ne bouge jamais, et le titre reste coupé (mesuré : « planter un arbre » rendait 33 px de haut pour 48 de texte). C'est « la taille qu'on LIT n'est écrite par aucune règle » (ligne plus bas), vu de l'autre bord : ici c'est NOTRE écriture qui est écrasée. **Parade : `setProperty(..., 'important')`, et vérifier que la mesure bouge d'un pas à l'autre.** |
| **Un bloc bâti après le poseur reste à y 0 et recouvre l'entête** | **L'ORDRE, PAS LA COTE.** Le fil d'une Nuée est placé par `_ficheCotes` — mais il est BÂTI APRÈS elle : sur une Nuée pleine il rendait à **y 0** sur 862 de haut, sous l'encart, le titre et la méta (mesuré sur 9 Promi). ⚠ **Et les deux parades évidentes sont fausses** : rappeler le poseur entier sans son contexte renvoie toute la fiche hors de l'écran (tout à y ≥ 844) ; tester « le `top` n'est pas posé » non plus (le poseur écrit 30, une valeur posée ET fausse). **Le seul critère juste est LA FORME DU DÉFAUT — le recouvrement** : on n'intervient que si le bloc passe au-dessus du bas de ce qui le précède. Un juge le confirme : `redteam_nuee` doit rester à son chiffre d'avant. |
| **Une sonde d'air « à l'encre » rend 0 sur une phrase, et 28 sur la suivante** | **ELLE PART DANS L'ENCRE.** Une sonde qui remonte puis descend depuis une cote jusqu'au premier pixel peint rend **0 si la cote tombe déjà sur de l'encre** — et c'est ce qui arrive quand on lui donne le bas d'une **boîte de ligne** : le **jambage** d'un « g » ou d'un « p » descend dessous. Vécu le 22 sept. 2026 : `ENCRE_GAP` rendait 0,0 pt sous « …à la légère. », 28,0 sous la phrase d'à côté, dans les deux thèmes — un faux rouge parfaitement reproductible, donc crédible. **Parade : sortir de l'encre par le bas AVANT de scanner** (0,0 → 26,5). Même famille que « un contrôle qui compte des pixels mesure la respiration du monde » : avant d'accuser le dessin, on vérifie l'instrument. |
| **Un balayage de couleurs ne voit pas un écran FERMÉ, même en `display:block`** | **UN ÉCRAN FERMÉ EST GLISSÉ HORS CHAMP** (§8, `translateY(100%)`), et un balayage qui filtre sur `visibility`/`display`/`opacity` le garde — tandis qu'un balayage qui filtre sur le rectangle de l'appareil le PERD. Vécu le 22 sept. : la dernière surface en amande du produit vivait dans l'aide de l'Aura, **à y 1603**. Les balayages d'avant, qui n'ouvraient pas cet écran, la déclaraient absente. **Parade : on OUVRE chaque écran, un par un, et on borne au rectangle de `#device`** — jamais « tous les nœuds du document ». |
| **Une bascule de palette paraît faite, et l'ancienne identité reste** | **UNE COULEUR PEUT VIVRE EN TRIPLET JS — `[58,84,255]` — ET AUCUNE PASSE TEXTUELLE NE LA VOIT.** Ni `#3A54FF`, ni `rgb(58,84,255)` : trois chiffres dans un tableau. **47 tableaux** en portaient : `NAT` (la Pelote), `SPECTRE`, `GPIX·GBRA·GLI·GMOS·GENC·GLIGHT` (les rampes de fond de la Toile), `SIG`, `ETATS`, `KC`, les grappes de l'onboarding et de la page +. Ils ont traversé **deux** lots de palette intacts, et c'est ce qu'on voyait « encore sur la sphère et sur les dalles ». ⚠ Et le motif `[[r,g,b],…]` n'en attrape que la moitié : **30 triplets vivent SEULS** (`nuee:[41,21,71]`, `var mauve=[…]`), il faut une seconde passe. **Parade : une bascule se TERMINE par un audit qui cherche chaque ancienne valeur sous SES TROIS FORMES — hexadécimal, triplet, `rgb()`.** Sans cet audit, la conversion est fausse et paraît juste. |
| **Une dalle change de couleur sans que personne ne l'ait repeinte** | **DEUX VOLEURS DE COULEUR.** 1 · `cc()` tirait la couleur au hasard à chaque chargement (corrigé : couleur figée, §4). 2 · **la réserve de l'onboarding n'est jamais vidée** : `Toile.reserve()` n'est posée que par l'onboarding, et `applyReserve` éclaircit ensuite au ton le plus clair de la palette (le lilas en Signal) **toute dalle qui passe sous ses anciens textes**, pour toujours. Vécu le 13 sept. 2026 : une fois la couleur figée, 2 à 4 dalles par chargement sortaient encore lilas, à des places différentes. **Parade :** la réserve n'éclaircit plus une dalle reliée à un Promi (`bs.pid==null`) **ni une dalle de Nuée** (`kind:'nuee'`, qui n'a pas de `pid` — elle sortait lilas puis bleue, pris par `redteam_nuee_dalle`). ⚠ Et un contrôle qui compare des Promi d'un chargement à l'autre les compare **par titre et personne, jamais par id** : les ids du jeu de démonstration changent (chantier 71) — le premier juge de ce lot comparait deux Promi différents. |
| **Au doigt, la tuile « Un Chiche » ouvre un Promi — à la souris tout est juste** | **UN ANCIEN CARROUSEL ÉCOUTE ENCORE LE DOIGT.** L'écran des choix de la page + (`pp-choix`) empile les trois tuiles, mais le carrousel horizontal d'origine (≈ l. 8805) écoutait toujours `touchstart`/`touchend` : au lever du doigt, `up()` rejouait `goTo(cur)` — la tuile d'AVANT —, l'écran passait à la phrase de cette nature SOUS le doigt, et le clic synthétisé tombait sur le geste. Vécu le 13 sept. 2026 : **sur un téléphone on ne pouvait pas lancer un Chiche depuis le +, et après une Nuée la tuile Promi gardait `data-kind="nuee"`.** Aucune batterie ne le voyait : **elles jouaient toutes à la souris.** Pris au piège par `scratchpad/acc_chiche_piege.py`. **Parade :** le carrousel ne s'arme pas sur `pp-choix`, et un toucher qui ne franchit pas le seuil ne change jamais de tuile. **Toute porte, tout choix se prouve AU DOIGT** (`Input.dispatchTouchEvent`, contexte `has_touch`) — `redteam_tuiles.py`, `redteam_gens.py`. ⚠ Au-delà d'environ 10 px de déplacement, ni Chromium ni iOS ne font un toucher : un contrat « qui glisse de 20 px » ne juge pas un toucher. |
| **On grossit un jeton de taille et RIEN ne bouge** | **UN JETON DÉCLARÉ N'EST PAS UN JETON CÂBLÉ.** `--t-titre-taille`, `--t-sous-titre-taille` et `--t-libelle-taille` sont déclarés dans `lot-TOKENS-css` — et ils ont **ZÉRO consommateur** : `var(--t-…-taille)` n'apparaît nulle part dans les 32 000 lignes. Le bloc `:root{--t-sous-titre-taille:27px;--t-libelle-taille:18px}` du lot des neuf points ne peignait donc **rien** ; le facteur ×1,217 n'a agi que par les règles explicites posées à côté (43 · 36 · 33 · 28 · 24). **Parade : avant de changer un jeton, compter ses consommateurs** (`grep -c "var(--jeton)"`). Un jeton à zéro consommateur se câble ou se laisse — on ne le repose pas en croyant peindre. (Le JSON garde ses sept niveaux : c'est le câblage qui manque, et il compte pour le portage Swift.) |
| **La taille qu'on LIT n'est écrite par aucune règle** | **`echelle()` EST LE PLANCHER DU §6, ET IL ÉCRIT EN LIGNE.** Mesuré aux Réglages : les libellés rendaient **13 px** alors qu'aucune règle du fichier ne dit 13 — le CSS les pose à **11,5** (`#device #settingsScreen .s2-cercle .s2-lab`, 2 ids + 2 classes, `important`) et `echelle()` (≈ l. 23533) les relève au plancher de 13, **inline, `important`, avec `data-ech`**. Un correctif écrit à 2 ids + 1 classe ne peint alors rien, et il le fait **en silence** : `.grouplab` (qui n'avait pas de règle forte) bougeait, `.s2-lab` et `.k` non. **Parade : piéger le peintre** (§7, on enveloppe `setProperty` et on lit la pile — 1 202 écritures de « 13px » trouvées en une passe), **corriger LA SOURCE** à une spécificité qui la bat (id doublé), et **ne jamais toucher au plancher lui-même** — le monter globalement avait resserré 156 paires d'air. |
| **Une capture d'élément sort ENTIÈREMENT NOIRE** | **LE NŒUD PORTE UNE ANIMATION.** `locator.screenshot()` sur un élément qui joue une animation CSS infinie (ici l'éclat qui traverse le bouton d'achat) rend une image **noire de bout en bout** — libellé compris. Rien n'est cassé dans le produit : vécu le 12 sept. 2026, les pixels du canevas sous-jacent étaient justes (moyenne 188/182/228, zéro pixel transparent), et j'ai d'abord conclu à un défaut de dessin. **Parade : ne jamais croire une capture d'élément sur un nœud animé — MESURER les pixels** (`getImageData` sur le canevas, ou la couleur moyenne du nœud), **et recapturer le CONTENEUR** (un `clip` sur la page entière) plutôt que l'élément. Même famille que « un comparateur d'images ment sur deux points » : avant d'accuser le dessin, on vérifie l'instrument. |

| **Un ancien écran paraît une fraction de seconde — et revient après chaque correction** | **UN ÉCRAN QUI SE COMPOSE PAR MINUTEURS SE MONTRE AVANT D'ÊTRE FINI.** (v103, 30 sept. 2026, la deuxième fois.) Trois formes mesurées image par image : ① **à l'ouverture**, une règle qui cache l'ancien chrome vit 37 000 lignes plus bas — le navigateur PEINT avant de la lire (`.topbar`, `.footer` 250 à 400 ms en WebKit) → la règle se double dans `<head>` ; ② **entre le + et la nature**, la page + était montrée dès sa nature posée, puis se composait sous l'œil (champ à +240, phrase par `arme` à +60/+340, encre du plateau à +120/+420 ; et `pose()` refusait de bâtir le plateau d'une feuille cachée) → elle reste cachée jusqu'à 450 ms après le DERNIER déclencheur et deux images identiques, plateau bâti ; son fondu d'entrée est retiré (Chromium y montrait la feuille telle qu'il l'avait peinte la dernière fois) ; ③ **à la plantation**, la page + reprenait son aspect d'avant (~100 ms) avant de glisser → on COUPE. **Deux images identiques ne prouvent rien : entre deux minuteurs, rien ne bouge.** Et **le voile d'un écran caché est un état lui aussi** : il grisait l'accueil pendant l'attente. Juge : `redteam_flash.py`. |
| **Un toucher sur le Peaufiner ne déclenche rien — à la souris tout marche** | **LE PEAUFINER NE PRODUIT AUCUN `click` AU DOIGT** (v104, mesuré en WebKit) : ses propres écouteurs annulent la fin du geste, le navigateur ne synthétise pas de clic. Un écouteur de `click` n'y voit donc JAMAIS un toucher. **Parade : lire le toucher lui-même** — appui puis lever sans glisser (`pointerdown`/`pointerup`, < 10 px, < 600 ms) — et avaler le clic qui pourrait suivre. Et un réglage flouté est en `pointer-events:none` : le doigt ne l'atteint pas, **un mur se reconnaît à sa GÉOMÉTRIE** (le point tombe dans son rectangle). |
| **On retire une fonction et l'app ne démarre plus — `node --check` est vert** | **UNE FONCTION SUR PLUSIEURS LIGNES, RETIRÉE PAR SA PREMIÈRE.** (v105, retrait d'Arranger.) `targets()` faisait huit lignes ; en retirant la première, les sept autres sont restées au niveau du script — des instructions VALIDES (`if(mode==='inspi')…`), que `node --check` accepte, mais qui lèvent `mode is not defined` au chargement : le script s'arrête, `let theme` n'est jamais initialisé, et TOUT l'app tombe (`Cannot access 'theme' before initialization`). **Parade : après un retrait, charger la page et lire `pageerror`** (`scratchpad/errs.py`), pas seulement la syntaxe ; et comparer la structure à la sauvegarde (la ligne qui suit la fonction retirée doit être celle qui la suivait). |
| **Arranger « marche » et rien ne bouge** | **L'ANCIEN CALQUE.** `targets()` rangeait `promises[].x/y`, que seul l'ancien SVG de `render()` lisait ; la Toile du moteur (les graines) l'ignorait. Une fonction qui écrit dans un calque que plus personne n'affiche paraît vivante au code et morte à l'écran : **on le mesure en regardant ce qui est PEINT (les graines, `Toile_graines`), jamais ce que la fonction écrit.** |
| **Un monde tient 60 i/s au banc Chromium, et rame sur l'iPhone** | **UN DÉCOUPAGE (`clip()`) SE PAIE À CHAQUE TRACÉ SUR LE MOTEUR DE SAFARI — ET CHROMIUM NE LE DIT PAS.** (v38, 24 sept. 2026.) Le coin arrondi de la Toile vivante était un `g.clip()` posé dans `frame()` avant la matière : en **WebKit** (CoreGraphics, le moteur de l'iPhone), Touffe passait de **51 à 205 ms par image** (154 ms pour un coin !), Taille-douce de 33 à 56 ; en Chromium, 14 ms et 5 ms seulement. Chromium headless peint le canevas en logiciel (Skia) et n'y fait presque pas payer un clip. **Parades :** ① on ne découpe pas la matière — on la peint, puis on repeint le FOND autour de la forme (pair-impair : un rectangle et la forme) ; ② **toute mesure de rendu se fait AUSSI en WebKit** (`p.webkit.launch()`, installé ; pas de bridage CPU : on mesure ×1) — un banc Chromium seul valide ce que l'iPhone ne tiendra pas. Outils : `sauvegardes/perf-v38/`. |
| **Un monde tient 60 i/s au banc Chromium, et rame sur l'iPhone** | **UN DÉCOUPAGE (`clip()`) SE PAIE À CHAQUE TRACÉ SUR LE MOTEUR DE SAFARI — ET LE BANC CHROMIUM NE LE DIT PAS.** (v38, 24 sept. 2026.) Le coin arrondi de la Toile vivante était un `g.clip()` posé dans `frame()` avant la matière : en **WebKit** (le moteur de Safari, donc de l'iPhone), Touffe passait de **51 à 205 ms par image — 154 ms pour un coin** —, Taille-douce de 33 à 56 ; en Chromium, 14 et 5 ms seulement (il peint le canevas en logiciel, Skia, et n'y fait presque pas payer un clip). **Parades :** ① ne pas découper la matière : la peindre, puis repeindre le FOND autour de la forme (pair-impair : un rectangle et la forme) ; ② **toute mesure de rendu se fait AUSSI en WebKit** (`p.webkit.launch()`, installé ; pas de bridage CPU, on mesure à ×1) — un banc Chromium seul valide ce que l'iPhone ne tiendra pas. Outils : `sauvegardes/perf-v38/`, CONTRAT-MONDE §8.4. |
| **Une dalle rendue « à sa taille » coûte dix fois plus, ou la Toile exportée sort petite dans un coin** | **v29, 23 sept. 2026.** ① `dalleTrame` cherchait la graine de chaque pixel parmi TOUTES les graines : à 200 px, 1,9 s pour une dalle Pixel. Parade exacte : ne passer que les graines qui PEUVENT gagner (\|t−k\| < 2·Rmax + w_k − w_t), et, par pixel, s'arrêter à la première qui ne peut plus (tri). ② `renderTo(cv, ech)` : six mondes font `setTransform(DPR…)` — si `ech ≠ DPR` la Toile se peint à la mauvaise densité ; `DPR = ech` le temps du rendu. ③ Un cache de rendu qui expire à l'horloge refait 120 ms de dalle à chaque toucher et fait perdre des touchers (`redteam_gens`, `redteam_verbe`) : la clé porte tout ce dont l'image dépend (taille, options, monde, thème, boîte de la cellule, couleur), rien d'autre ne l'expire. |
| **Un cache se reconstruit à CHAQUE image, et l'app gèle au moment de planter** | **UNE SIGNATURE DE CACHE PRISE SUR UN ÉTAT QUI BOUGE SE RECONSTRUIT À CHAQUE IMAGE.** (Tom, 23 sept. 2026.) Le cache de Madrure signait le semis (positions de repos, poids) — juste en apparence : à la plantation, le moteur fait GRANDIR la dalle et relâche toute la Toile pendant ~1 s, poids et positions changent à chaque image. Mesuré : **25 constructions pour une seule plantation** (×1) ; à ×4, **une par image, 830 ms chacune — 12 s figées**. Aucun banc « à semis fixe » ne pouvait le voir. **Parades :** tant que la signature d'une surface change d'une image à l'autre, on repeint l'état d'avant ; on reconstruit quand elle est POSÉE (deux images identiques), et on relance le moteur pour qu'il le voie ; la construction elle-même se fait PAR TRANCHES, l'ancien état restant affiché (v33 : ×4, pire image 450 ms au lieu de 1,4 s de gel). **Devant tout cache à signature : mesurer le nombre de constructions PENDANT une plantation, pas sur un semis au repos.** Et une signature se prend à la précision que l'œil voit (½ px), jamais au 1/16 : un relâchement qui converge sans fin la change encore dix images plus tard. |
| **Un titre rétrécit chez Tom, jamais au banc** | **DEUX UNITÉS DANS UNE MÊME COMPARAISON.** `ajusteTitres` comparait `scrollWidth` (pixels de MISE EN PAGE) à une place lue par `getBoundingClientRect` (pixels d'ÉCRAN, mise à l'échelle comprise). Au banc, l'appareil est à l'échelle 1 ; dans une fenêtre plus petite que le téléphone (le panneau de l'app de Tom), il est réduit — mesuré à 0,72 : Index, Réglages, L'aura à 23 px au lieu de 35 · 29 · 30. **Parade : ramener toute mesure à l'unité du titre** (`r.width / offsetWidth`) ; et **passer un banc à une échelle ≠ 1** (viewport 300 × 650) dès qu'une boucle compare des largeurs. |
| **Une page tourne à 100 % du processeur pendant des heures** | **UN OBSERVATEUR DU DOCUMENT QUI RÉÉCRIT DU TEXTE.** Le composeur des É (v35) observait chaque mutation du `body` et réécrivait le compte « Nuées » sous l'Index — que l'app réécrit à son tour : ping-pong sans fin, `redteam_ecrans` bloqué 2 h 46. **Parades :** une passe au plus par image (`requestAnimationFrame`), ne toucher que ce qui en a besoin (ici, le texte réellement en capitales), et un plafond par nœud (20 réécritures en 2 s → on renonce). **Et une série de batteries se lance avec une limite de temps par batterie** : un blocage ne doit jamais geler toute la série sans que personne le voie. |
| **Un régulateur mesure, vise… et n'applique JAMAIS** | **LA CLASSE QU'ON OBSERVE NE SE RETIRE JAMAIS.** Le régulateur de densité de la Pelote appliquait sa vise dans `prepare()`, appelé quand `#auraScreen` GAGNE `.show`. Or **`closeAll()` ne retire pas cette classe** : l'observateur ne se réveillait plus jamais, et la vise n'était appliquée **de toute la séance**. Mesuré : sous bridage ×8, vise 75 000, palier resté 110 000 ; à la réouverture, toujours 110 000. Le seul chemin qui la faisait mordre était le RECHARGEMENT, par le stockage — d'où « il descend et garde le palier ». **Parades :** on n'observe pas une classe sans avoir vérifié qu'elle se RETIRE ; et ce qui doit s'appliquer « quand personne ne regarde » s'accroche au moment où l'on QUITTE (on ENVELOPPE `closeAll`, §8) et à `visibilitychange`, jamais à l'ouverture seule. **Corollaire :** on ne persiste que ce qui a été APPLIQUÉ — persister la vise laissait un pic de trois secondes empoisonner tous les chargements suivants. |
| **Un flou de 2,4 px sur un trait de 6 px n'est pas un flou, c'est un halo** | **L'INSTRUMENT EST FAUX, PAS L'INTENTION.** Le voile du gratuit floutait la moitié droite des Noyaux de l'Aura : sur un bloc large (`.au-gr2`) ça floute ; sur un ARC de 6 px ça double sa largeur et pose une auréole sur le fond, entre les disques. `overflow:hidden` n'y peut rien — le halo est DANS le dessin, pas en dehors (et le lot avait justement posé `overflow:visible` « pour que le flou ne se coupe pas »). **Parade : garder le signal, changer le moyen, et prendre le moyen QUI EXISTE DÉJÀ SUR CET ÉCRAN** — `#ksocial` et `.ah-locked` disent « c'est le Cercle » avec une opacité (.5 et .6). On ne remplace jamais une décision écrite par une invention ; on lui emprunte son autre forme. |
| **Un contrôle d'air reste vert pendant que l'air disparaît** | **⚑ ON MESURE TOUJOURS L'ENCRE, JAMAIS LA BOÎTE** (Tom, 30 sept. 2026 : *« la trouvaille la plus importante du lot »*). `redteam_air` mesurait le rectangle des ÉLÉMENTS : l'agrandissement des faces (v96, `size-adjust:112%`) a grossi l'encre DANS des boîtes qui ne bougeaient pas — **609 paires resserrées, et il n'a pas rougi une fois** ; la fiche de Nuée est passée à 0 d'air sous « Avec » au vert. **Parade : l'air se mesure entre les rectangles du TEXTE** (`Range.selectNodeContents(e).getBoundingClientRect()`, ascendantes et descendantes de la police) — jamais `e.getBoundingClientRect()`. Même piège sous un autre nom : un juge qui dit « à l'encre » et lit une boîte (`redteam_nuee_entree` lisait le bas des Noyaux sur leur boîte, pas sur l'encre de leurs noms — 2 px de faux). Et **un juge ne voit que les écrans qu'il ouvre** : `redteam_air` en ouvrait 19 sur 34 ; un écran qui garde `.show` (Studio, Partager, l'Aura, son aide) se fait mesurer à la place du suivant si le juge ne repart pas d'un état vierge. |
| **Une preuve est verte sur un monde qui n'existe plus** | **UN `// commentaire` GLISSÉ DANS UNE FONCTION ÉCRITE SUR UNE LIGNE commente la fin de la ligne** — le bloc entier ne se charge plus, la fabrique du monde est absente, et le moteur retombe sans rien dire. Vécu en v72 : « Ramage vivant = 0 pixel d'écart » alors que Ramage n'existait plus. **Parade : après CHAQUE patch, `node --check` sur chaque `<script>` séparément** (un seul fichier joint peut encore passer), et une preuve relève aussi ce qu'elle a mesuré (le nombre de tracés, l'état), pas seulement l'écart. ⚠ **Revenu le jour même (v74), et cette fois `node --check` ne pouvait RIEN voir** : le commentaire avait avalé une affectation (`_vS = …`), la ligne restait syntaxiquement juste, et le calque net n'était jamais posé. **Règle : dans une ligne de code existante, on n'écrit JAMAIS `//` — seulement `/* … */`.** |
| **Le même dessin, peint en deux fois, sort différent — en Chromium seulement** | **CHROMIUM SUR GPU ANTICRÉNÈLE UN MÊME TRACÉ SELON L'ENDROIT OÙ IL VIDE SON LOT.** Mesuré en v72 : un plumage peint d'un bloc, puis par tranches (une relecture de pixel entre deux) → 7,3 % des pixels différents, sur les BORDS seulement ; WebKit : 0. **Avant d'accuser un calque ou une construction par tranches, mesurer ce témoin** — sinon on cherche un défaut de contenu qui n'existe pas. |
| **Un bouton est visible et ne prend pas le doigt** | **UN FRÈRE AU MÊME `z-index`, VENU APRÈS, LE RECOUVRE.** (v117) Le bouton photo d'une fiche vivait dans un nid à `z-index:2` ; `#dpMain`, frère suivant, aussi : au centre du rond, `elementFromPoint` rendait `dpMain`. Le bouton était injoignable au doigt depuis sa naissance — et tous les juges l'ouvraient par `.click()`. **Parade : toute porte se prouve au point du doigt** (`elementFromPoint` au centre, puis un vrai toucher), jamais par un clic scripté. |
| **Un menu posé dans un nid de taille nulle sort à 0 px de large** | **`max-width:100%` d'une règle générale y vaut 0.** (v117) Le nid du bouton photo est un porte-à-faux 0 × 0 (§8, il ne se mesure pas) ; ce qu'on y pose hérite d'un `max-width` relatif à lui. Parade : `max-width:none` nommément sur ce qu'on y pose. |
| **Le rond Partager de la barre Peaufiner ne réagit pas — même à la souris** | **LA BARRE NE PRODUIT AUCUN `click`, ni au doigt (v104) ni à la souris (mesuré v117).** On lit le geste (`pointerdown` → `pointerup` sans glisser, < 10 px, < 600 ms), pour TOUS les pointeurs, et l'`onclick` se dédoublonne. |
| **Une animation ralentit sous charge alors qu'elle « suit le temps »** | **UN PAS BORNÉ À 0,1 s PAR IMAGE N'EST PAS LE TEMPS RÉEL.** (v117) Le souffle de la Pelote avançait du `dt` de la rotation (borné à 0,1 s) : en WebKit, où une image coûte 150 à 250 ms, son sommet tombait à 8,2 s au lieu de 4,6. La borne de la rotation sert à ne pas SAUTER ; un cycle qui doit durer 10 s prend le temps réel, borné seulement après une pause (0,5 s). |

> ### ⚠ UN ESPACEMENT QUI REVIENT POUR LA CINQUIÈME FOIS — CE QUI DOIT L'EMPÊCHER, ET LE CONTRÔLE QUI LE PREND
> **Décision Tom, 10 septembre 2026 : « c'est la quatrième fois qu'un espacement revient, ça ne doit plus
> arriver. »** Vécu sur l'Aura portée : la planche posait les Noyaux à **454**, calcul fait pour une phrase
> d'UNE ligne (27,3 pt d'air à l'encre). Deux des cinq phrases en font **DEUX** : l'air tombait à **3,7**.
> Et les libellés des dalles touchaient le bouton (**2,7** pt) dans tous les états — la planche l'avait déjà.
> **C'est le piège « une cote dérivée n'est pas un espace » (tableau ci-dessus), en plus sournois : le
> texte n'a pas grossi, il a passé à la ligne selon SES MOTS.** Aucun relevé fait sur une seule phrase
> ne pouvait le voir.
> **Les trois règles :**
> 1. **Sous un texte qui peut passer à la ligne, aucune cote n'est figée** : elle se dérive de son BAS
>    RÉEL + l'air (`place()` de l'Aura). Et l'air vient de la planche ou du rythme déclaré de l'écran,
>    jamais de l'œil.
> 2. **Un contrôle d'air couvre CHAQUE PAIRE DE BLOCS, texte ou non** — une phrase contre une rangée de
>    disques, des libellés contre un bouton. `redteam_air.py` ne mesure que des paires de textes : il
>    ne pouvait pas le voir. **Et il se joue sur TOUS les contenus qu'un bloc peut prendre** (les cinq
>    phrases), **aux boîtes ET à l'encre sur l'image rendue** (`releve-aura.py`, famille 9).
> 3. **Si l'air rendu ne tient plus dans l'écran, l'écran DÉFILE** (sous le plateau, qui rogne) — on ne
>    reprend jamais l'air pour faire tenir.

> ### ⚠ UNE SONDE DÉFAIT EXACTEMENT CE QU'ELLE A FAIT — ET UN INSTRUMENT NOMME CE QUI RATE
> **Décision Tom, 10 septembre 2026 : « une sonde qui modifie l'app doit défaire ce qu'elle a fait, sinon
> elle contamine tout ce qui suit. »** Vécu sur la preuve des contrats de l'Aura (`preuve_contrats.py`),
> trois fois dans la même passe — pas d'une passe à l'autre (chaque passe ouvre une page neuve) :
> 1. **Défaire ≠ retirer.** La sonde qui déplaçait la légende se « défaisait » par `removeProperty('top')`.
>    Or la cote était AUSSI écrite par l'app (`place()`, en ligne, `important`) : le retrait l'effaçait, la
>    légende retombait sur l'ancienne cote figée du CSS, et l'app ne la réécrivait pas (elle compare SA clé,
>    pas le DOM). **Une sonde note la valeur d'avant — et sa priorité — et la remet.**
> 2. **Remettre ≠ rétablir.** La sonde de la phrase remettait le texte, mais la colonne ne se recalcule qu'au
>    passage suivant de `place()` (jusqu'à 30 images) : entre les deux, les contrôles suivants mesuraient une
>    colonne décalée. **Après avoir remis, on force le recalcul** (`_aura.mot(null)`).
> 3. **Poser puis mesurer en deux appels laisse passer une image** : l'app se recalcule entre les deux et
>    avale la sonde — le contrat paraît éteint. **Sonde et mesure dans la même tâche.**
> **Et un instrument qui ne garde que ce qu'il filtre est aveugle** : une passe a donné « 1 contrat à
> reprendre » sans que je puisse dire lequel — mon filtre n'imprimait que la légende et le verdict, et le
> journal complet n'était pas gardé. **Le verdict NOMME les contrats qui ratent, et chaque passe garde son
> journal entier.** C'est le piège déjà payé deux fois : un contrôle qui passe au vert sans dire ce qu'il a
> mesuré (voir « un juge qui lit la valeur qu'il vérifie », §7).

> ### ⚑ SUR UN OBJET QUI TOURNE, ON COMPARE À L'ANGLE, JAMAIS À L'INSTANT
> **Décision Tom, 10 septembre 2026 : « sur un objet qui tourne, une mesure prise au même instant ne compare
> pas le même endroit. On mesure à l'angle, jamais au temps. »** Deux images d'un objet qui tourne, prises à
> deux moments, ne montrent pas le même lieu : comparer leurs pixels compare deux endroits différents — le
> contrôle peut passer au vert sur un défaut qui demeure, ou rougir sur un état parfait. **Une comparaison de
> pixels se prend à la même VUE** : rotation figée, vue remise au même angle (`_aura.fige(true)`,
> `_aura.vue(lac, tan)`) — ce que font déjà dans `releve-aura.py` le toucher, le retour, la trace et le
> relissage. **Une mesure qui ne lit pas de pixels** (une durée, un état — l'acquis 6, le comblement, mesure la
> vie du creux) **n'a pas d'angle à caler.** Vaut pour tout ce qui bouge : la Pelote, la Toile qui respire, un
> canevas animé. (Vérifié le 10 septembre : aucun faux vert de cette espèce n'a été trouvé dans le juge ; la
> règle est posée pour qu'il n'y en ait jamais.)

> ### ⚠ UN INSTRUMENT QUI RALENTIT AVEC LA MACHINE FABRIQUE DES FAUX CHANTIERS
> **Constaté le 12 septembre 2026 : DEUX chantiers du carnet, ouverts sur des mesures qui ne tenaient pas.**
>
> | Le chantier | Ce que je croyais mesurer | Ce que je mesurais |
> |---|---|---|
> | **n° 75** — la page + rend des hauteurs nulles en sombre | un défaut du produit, « antérieur au lot » | **mes propres Playwright concurrents.** Machine au repos : 6/6 sur QUATRE versions, dont celle sur laquelle j'avais « prouvé » que le défaut préexistait. Et 8/8 sous bridage CPU ×1 à ×10. |
> | **n° 73** — l'élan de la sphère tombe à 0 dès 100 ms par image | le produit qui perd l'élan sous charge | **mon lancer, joué dans la page et cadencé par `setTimeout`** — qui se dilate avec le bridage. Le DOIGT ralentissait avec la machine : 100 ms de balayage devenus 474 ms, livrés en UN mouvement. Au doigt CDP horodaté : 11 rad/s à ×1 comme à ×10, sur les deux versions. |
>
> **La règle : un instrument dont la cadence dépend du fil principal qu'il mesure ne mesure rien.** `setTimeout`,
> `requestAnimationFrame`, `page.mouse.move`, une seconde batterie qui tourne à côté — tous se dilatent avec la
> charge. **Un geste s'injecte par le CDP, avec un horodatage explicite par événement**
> (`Input.dispatchMouseEvent`, `Input.dispatchTouchEvent`) : il part du processus navigateur, donc sa vitesse ne
> dépend pas de la page. Et **une batterie qui rougit se repasse SEULE avant d'écrire quoi que ce soit** — le §7 le
> disait déjà pour les rouges ; il vaut aussi, et surtout, pour les CHANTIERS qu'on en tire.
>
> **Corollaire, et c'est la moitié utile de l'histoire : corriger l'instrument n'efface pas toujours le défaut, il
> le déplace.** Le n° 75 a disparu ; le n° 73 est devenu plus précis ET plus grave — l'élan ne dépend pas de la
> charge mais de **l'écart entre deux `pointermove`** (0,00 rad/s dès 120 ms d'écart, sur neuf essais), parce que la
> fenêtre était figée à 90 ms. **Quand une mesure s'effondre, on ne referme pas le dossier : on cherche la grandeur
> qui a la forme du défaut** (§7, « choisir la grandeur qui a la forme du défaut »).
>
> **Et Chromium peut CACHER le défaut de la cible.** Il regroupe les mouvements (`getCoalescedEvents`) et rend le
> paquet avec les horodatages d'origine. **Safari n'a pas cette API** : sur iOS, l'app ne voit qu'un mouvement par
> appel. Toute mesure de geste destinée à l'iPhone se fait donc **regroupement éteint**
> (`PointerEvent.prototype.getCoalescedEvents = function(){ return []; }`) — sans quoi on valide un comportement
> que le téléphone n'aura pas.

> ### ⚑ UN MOUVEMENT SE CALCULE SUR LE TEMPS RÉEL, JAMAIS SUR LE COMPTE D'IMAGES
> **Décision Tom, 10 septembre 2026, au portage de la Pelote.** Trois défauts de la même famille,
> invisibles sur le Mac du banc — on ne les aurait trouvés que sur un téléphone lent :
>
> | Symptôme | Cause | Parade |
> |---|---|---|
> | **L'élan est perdu quand les images ralentissent** | les mouvements du doigt horodatés à leur TRAITEMENT (`performance.now()`) : livrés groupés après une image lente, ils tombent « au même instant », la vitesse sort nulle | l'heure de l'ÉVÉNEMENT (`e.timeStamp`) et chacun des événements regroupés (`e.getCoalescedEvents()`) |
> | **La rotation ralentit quand les images ralentissent** | le pas de temps borné à 50 ms par image : à 130 ms par image, la rotation tombait au tiers | le temps réel ; la borne (100 ms) ne sert qu'à ne pas sauter après une pause |
> | **Une saccade au lâcher** | un travail lourd (le cache du peintre refait) déclenché pile quand l'élan est le plus fort | différer le travail lourd à un moment calme — la caresse s'inscrit au repos (Q171) |
>
> **La règle :** une vitesse, une décroissance, une durée se calculent sur le temps écoulé — jamais sur
> « une image = 16 ms ». **Et un juge qui mesure un mouvement lit le pas de temps de LA BOUCLE**, pas
> celui de son propre échantillonneur : les deux ne tombent pas toujours dans la même image (vécu : deux
> images de 130 ms lues comme une seule de 260 — une fausse saccade). **Corollaire :** Playwright ne sait
> pas lancer — face à un fil principal occupé, ses `mouse.move` arrivent à ~130 ms les uns des autres, le
> relâcher 129 ms après le dernier : un doigt qui s'arrête. Un lancer se joue DANS la page, cadencé.

**Noms de variables à connaître :**
`NUE` (table des noms de Nuée) · `curNuee` (clé de la Nuée ouverte) ·
`promises` (tous les Promi) · `Toile.dalleTrame` · `peintMinis` ·
`_teinteDalle` · `_fichePose` · `_ficheDalle`

---

## 8 bis. LE CONTRAT VISUEL — la règle qui prime sur toutes les autres

Le design de Promi est le fruit de **plusieurs centaines d'itérations**. Chaque
taille, chaque couleur, chaque marge a été arbitrée. **Rien n'est arbitraire.**

### Ne jamais réécrire — seulement patcher

**Interdit absolu :**
- réécrire un écran « proprement »
- refactoriser le CSS ou le JS
- remplacer un composant par une version « équivalente »
- normaliser des valeurs qui paraissent incohérentes

Si une valeur paraît étrange (un `-66px`, un `1.6px`, un `.42`), **elle est
étrange pour une raison**. Ne pas l'arrondir, ne pas la « corriger ».

### Le contrôle obligatoire

Avant et après chaque lot :

```bash
python3 releve-design.py
```

Le script relève **148 propriétés sur 26 éléments dans 6 configurations** et
compare à `design-reference.json`.

```
✅  AUCUN ÉCART. Le design est intact.        → on peut livrer
❌  N ÉCARTS avec la référence                 → régression, corriger
❌  N COULEURS FAUTIVES                        → un trait neutre est apparu
```

**Un écart non demandé par le lot est une régression.** Le corriger avant de
livrer, ou expliquer précisément pourquoi il était inévitable.

Après un lot **validé par l'utilisateur** :

```bash
python3 releve-design.py --figer
```

### Ce que le script ne voit pas

Il ne vérifie ni le placement relatif, ni les superpositions, ni le rendu réel
des dalles. **Les captures avant/après restent obligatoires.**

### ⚑ CE QUE « ZÉRO ÉCART » VEUT DIRE — LA MATIÈRE EST EXCEPTÉE

> **Décision Tom, 20 août 2026. Elle fait loi et elle définit la cible de tout le
> portage.** Elle clôt Q74.

**« Zéro écart » veut dire zéro sur la GÉOMÉTRIE, les MOTS, les COULEURS et les FORMES.
La MATIÈRE est exceptée.**

**Pourquoi, et ce n'est pas une facilité.** Une Toile est **engendrée par le moteur** —
graines, poids, monde tiré au Studio — et elle respire avec `performance.now()`. La planche,
elle, l'a **tracée à la main**, cadre par cadre. Les deux **ne peuvent pas coïncider**, et
**on n'abandonne pas le moteur** (§9 : « ne jamais toucher au code de la Toile », « les
formes viennent du moteur »). Sur une fiche de Nuée, où le champ occupe les deux tiers de
l'écran, la mesure donne **87 à 100 % de pixels différents** — et aucune correction de dessin
n'y changera un point.

**Ce que ça oblige :** **un comparateur exclut la zone de matière et mesure tout le reste.**
Il ne desserre rien ailleurs — hors de cette zone, la cible reste **zéro**, pas « peu ».
`scratchpad/duo_pixel.py` porte le masque ; `redteam_formes.py` compare la courbe peinte à
la loi extraite du cadre.

**Ce que ça n'autorise PAS :**
- **masquer plus que la matière.** La zone exclue se **déclare et se mesure** — le masque est
  publié dans le relevé, en pixels, avec sa part de l'écran. Un masque qui grandit pour faire
  baisser un chiffre est une fraude.
- **excepter la matière ailleurs que dans le comparateur pixel.** Une dalle reste soumise à
  tout le reste : sa **boîte**, sa **place**, sa **couleur de champ**, son **échelle 1**, la
  règle des trois tons, le seuil 42. C'est la peinture INTÉRIEURE de la dalle qui est exceptée,
  jamais ce qui l'entoure ni ce qui la cadre.
- **s'en servir pour un écran sans dalle.** L'Index, le Fil, la page +, Peaufiner et l'instant
  gardent des zones de matière **petites** : hors d'elles, zéro.

### ⚑ LA SECONDE EXCEPTION — LE DESSIN DES GLYPHES

> **Décision Tom, 29 août 2026. Elle clôt Q80 et se lit avec celle de la matière.**

**« Zéro écart » veut dire zéro HORS MATIÈRE et HORS GLYPHE.**

**Pourquoi.** La planche est composée en **Hanken Grotesk** et **Bricolage Grotesque**
(Google Fonts, variables). L'app porte ses **faces embarquées** — **aujourd'hui cinq : Gilbert 700, Atkinson
400 · 500 · 700, PromiLate 400** (repris le 30 sept. ; en août : Apfel, ApfelMid, Bricolage, Fraunces) — et le **§6 les
impose** : aucune graisse hors d'elles, parce qu'en Swift une face absente ne se substitue pas, elle casse. `Hanken Grotesk` **n'est pas**
`Apfel` : c'est une autre fonte, que la planche a prise comme doublure — le document la
transcrit d'ailleurs partout en « Apfel 500 ». **Les dessins de glyphes ne peuvent donc pas
coïncider, quoi qu'on corrige.**

**Ce qui, lui, doit coïncider, et que les juges mesurent à zéro : LA BOÎTE DU TEXTE** —
sa place, sa taille, sa graisse, sa couleur, et son mot. Rien n'est desserré : c'est le
DESSIN de la lettre qui est excepté, jamais ce qui la porte ni ce qui l'entoure.

**Ce que ça oblige :** l'app déclare ses boîtes de texte (`window._zonesTexte()`) comme elle
déclare sa matière, et le comparateur rend **deux chiffres** — « écart » (hors matière) et
« hors glyphe » (hors matière ET hors boîtes de texte). Les deux masques sont **peints sur
l'image de diff** : matière en bleu sourd, texte en vert sourd. Un masque qui grandit se voit.

**Et si un écran ne peut pas atteindre zéro hors matière et hors glyphe, on le DIT, avec la
raison mesurée.** Pas de pourcentage présenté comme une livraison, pas de « classé mais pas
corrigé ».

---

## 9. Ce qu'il ne faut jamais faire

- **Toucher au code de la Toile.** Elle est validée et fragile. Aucune
  modification sans demande explicite.
- **Nettoyer le CSS.** Cinq tentatives, cinq échecs documentés. L'ordre des
  769 règles du dernier bloc est significatif ; toute suppression casse le rendu.
  Voir `ETAT-DES-LIEUX.md § dette technique`.
- **Inventer une forme, un mot, ou une phrase.** C'est la faute la plus grave.
  **Les formes viennent du moteur** (`Toile.dalleTrame`) — jamais un polygone, un
  hexagone, un glyphe reconstruit. **Les mots et les phrases viennent de l'utilisateur
  ou du moodboard** — jamais un libellé, une nature de texte (« parole », « tout le
  monde s'y engage »…) ou une tournure inventée. **Si tu ne trouves pas, tu demandes.**
- **Inventer pendant un lot de correction.** Un lot corrige ce qui est décrit,
  rien d'autre. Les éléments d'identité arrivent par moodboard.
- **Rendre visible quelque chose qui était masqué, sans chercher pourquoi il l'était.**
  **C'est la vraie leçon du portage.** Un élément masqué peut être une **décision**, pas un
  oubli — et le porter au moodboard, c'est alors ressusciter ce que le produit avait
  enterré. Vécu : le réglage **« URGENT »** était masqué par `#createSheet .f-duo
  .field:has(#urgSeg){display:none}` avec, trois lignes plus haut, le commentaire
  *« Urgent supprimé (décision : on garde Important, comme la fiche) »*. Je l'ai remonté
  dans Peaufiner en le prenant pour un oubli de portage. **Avant de démasquer un élément :
  chercher la règle qui le masque, lire le commentaire qui l'accompagne, et grepper
  `QUESTIONS.md` et `DECISIONS.md` sur son nom.** Si rien n'explique le masquage, demander.
- **Livrer sans avoir vérifié.** Si le résultat n'est pas conforme, le dire.
  Une livraison fausse coûte plus qu'un tour perdu.
- **Enchaîner plusieurs chantiers dans un lot.** Un lot = un écran = un
  avant/après.

---

## 10. Le ton des réponses

L'utilisateur travaille en français, écrit vite, avec des fautes de frappe, et
dicte parfois à la voix. Il a une tolérance faible pour les régressions et pour
les affirmations non vérifiées.

- Annoncer ce qui a été **mesuré**, avec les chiffres.
- Dire clairement ce qui n'a **pas** été fait.
- Ne jamais prétendre qu'une chose est corrigée sans l'avoir vue.
- **Une question par tour, pas plus.** Quand une règle du projet suffit à trancher,
  l'appliquer sans attendre la réponse, noter le choix dans la livraison — l'utilisateur
  corrigera s'il n'est pas d'accord. Ne poser une question que pour un vrai fork non
  couvert par une règle.
- **Le test « ÉVIDENT »** après chaque écran : quelqu'un qui ne connaît pas l'app
  comprend-il en une seconde ce qu'il doit faire ? Si non, ce n'est pas fini — même si
  c'est beau.

---

## 11. Dégradation adaptative — note de portage (Tom, 30 sept. 2026 — rien à implémenter)

Dégradation adaptative — principe, à étalonner. Raison : iOS 26 fixe le plancher système à l'iPhone 11. Promi n'ajoute aucun plancher : l'app tourne sur tout appareil supporté et sa qualité s'adapte, pour que personne ne soit exclu et que personne ne subisse une Toile qui saccade. Ce qui fait tenir une parole ne se négocie jamais. Seul l'ornement se dégrade, du moins visible au plus visible.
Ne se dégrade jamais : le geste (tous les coalescedTouches traités, le trait rendu dans la trame du toucher, en pleine résolution) · les couleurs (hex exacts, aucune quantification) · la lisibilité (texte natif, contrastes, tailles, Dynamic Type) · la composition de la Toile (toutes les dalles présentes, positions identiques) · VoiceOver.
Peut se dégrader : le nombre de dalles animées, les transitions de navigation, la complexité des mondes, la densité de la Pelote (le régulateur actuel, de 110 000 à 75 000 poils, en est le modèle). L'ordre, les paliers et les seuils seront fixés par mesure Instruments sur appareil, au premier lot Toile du portage. Aucun chiffre n'est décidé à ce jour : n'en invente pas, n'en implémente pas.

---

## 12. La grille anti-coercition (le texte de Tom : 7 oct. 2026, v136 — C-065)

> **⚑ LA GRILLE, MOT POUR MOT (Tom, 7 oct. 2026, v136 — C-065). Elle fait loi ; les règles reconstituées qui la suivent n'en sont que le détail.**
>
> **« Une seule réponse "oui" bloque la mécanique :**
>
> 1. **Produit-elle un état visible "rompu", "raté" ou "en retard" ?**
> 2. **Un état accumulé perd-il de la valeur par inaction ?**
> 3. **Met-elle en évidence les manquements de la personne ?**
> 4. **La récompense est-elle à la fois annoncée et proportionnelle à l'action ?**
> 5. **Si on expliquait son fonctionnement exact, la personne agirait-elle autrement ?**
> 6. **La réparation d'un état dégradé est-elle payante ou publicitaire ?**
>
> **Six risques cumulés : notification au calendrier de l'éditeur plutôt qu'à la disponibilité · rythme imposé plutôt que choisi · captation
> active par défaut · plus de gestes pour désactiver que pour activer · redemande d'un choix déjà fait · relance, urgence, compte à rebours,
> culpabilisation.**
>
> **La grille s'applique à la structure d'une mécanique, jamais à son nom. »**

### Les règles reconstituées (v135) — le détail, sous la grille
> Trente-deux règles reconstituées à partir des décisions écrites (les huit règles anti-notation de `AUDIT-AURA-CERCLE.md` §C, la « ligne
> rouge » de `BRIEF-ETUDE-PSYCHO.md`, `DECISIONS.md` A1, Q347, Q368, v104, v109), telles que `portage/REGLES.md` §A les porte, avec pour
> chacune ses sources, sa vérification et son juge. Juge des mots : **`redteam_lexique.py`** (termes bannis, loi des points).

**A1 · Ce n'est pas un gestionnaire de tâches**
- **R-001** · Toute décision qui rapproche Promi d'un gestionnaire de tâches est rejetée, même si elle est pratique.
- **R-002** · On tient sa parole par un geste tracé au doigt, jamais par une case à cocher ni par une touche.
- **R-003** · L'échéance n'est jamais obligatoire : « un jour » est une réponse valable, et aucun bouton « ajouter une échéance » n'existe.
- **R-004** · La création est une phrase dont les mots se touchent, pas un formulaire.
- **R-005** · On ne défait pas une parole tenue.
- **R-006** · Aucun réglage « urgent » : l'urgence n'existe pas dans le produit.

**A2 · Rien ne note, rien ne classe**
- **R-007** · Aucune carte, aucun corps, aucun fond n'est peint d'une couleur d'état : l'état vit dans la ligne.
- **R-008** · Dans une liste et sur la Toile, une dalle n'est jamais teintée par sa nature : ce serait un classement par nature.
- **R-009** · Pas de score, pas de points, pas de badges, pas de série.
- **R-010** · Aucun compteur visuel ne croît avec l'action.
- **R-011** · Aucun chiffre, aucun mot de valeur, aucun agrégat n'est attaché à une personne.
- **R-012** · Aucun tri par valeur, aucun superlatif.
- **R-013** · Ce qui se mesure à deux est symétrique : aucun verdict ne désigne un porteur et un porté.
- **R-014** · Des anneaux, jamais une liste de barres.
- **R-015** · L'Aura ne porte que trois chiffres — tenues, en cours, à tenir — sous la légende, et aucun pourcentage.
- **R-016** · Rien ne recule jamais : aucune grandeur dessinée ne décroît parce que le temps passe.
- **R-017** · Les mots du Noyau ne sont jamais un reproche, et leur échelle est monotone.
- **R-018** · Un seul compteur dans l'app : celui du Fil, et il ne redescend que quand on a agi.
- **R-019** · L'état reste un signal fixe : il ne suit ni la palette, ni le monde, ni le thème.

**A3 · Les notifications**
- **R-020** · Aucune demande de permission au lancement.
- **R-021** · « Je te le rappelle ? · oui · pas besoin » ne paraît qu'après la plantation d'une parole DATÉE ; la permission n'est demandée qu'après « oui ».
- **R-022** · Deux « pas besoin » d'affilée, puis plus jamais la question.
- **R-023** · Rien quand la date est passée.
- **R-024** · Une notification par jour au plus.
- **R-025** · Les mots des notifications sont ceux-là, au caractère près.
- **R-026** · Aucun événement négatif n'est notifié.

**A4 · Les murs de Ma Parole !**
- **R-027** · Un réglage réservé est flouté à 4,8 px, sans encart, sans cadenas, sans explication.
- **R-028** · Au toucher d'un mur, une phrase paraît seule sur le flou, le temps d'être lue, puis s'efface.
- **R-029** · L'offre ne s'ouvre seule que la toute première fois ; ensuite elle ne s'ouvre que si l'on touche pendant la lecture.
- **R-030** · Les phrases des murs sont les dix-huit de Tom, dans l'ordre, puis au hasard sans répéter la précédente ; le compteur est global et se remet à zéro après quatorze jours sans mur.
- **R-031** · Rien de tout cela chez un membre : aucun mur, aucune phrase.
- **R-032** · On ne livre pas un réglage qu'on ne peut pas éteindre.

**Trois tensions connues, qui ne sont pas des règles** (détail dans `portage/REGLES.md`) : « un seul chiffre, pas de pourcentage » face aux
trois chiffres de l'Aura (v95) et à la liste « Ce que tu as tenu » qui s'allonge (v131) ; « Ton meilleur Cercle » face à « aucun
superlatif » ; « REPORTER » dans le Fil face à « rien ne reproche ».
