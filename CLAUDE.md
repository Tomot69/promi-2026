# CLAUDE.md — Promi

> Ce fichier est relu à chaque session. Il fait autorité sur tout le reste.
> Si une consigne de l'utilisateur contredit ce fichier, **demander avant d'agir**.

> ## ⚑ PORTE DE QUALITÉ — RÈGLE PERMANENTE (Tom, 22 oct. 2026, C-178). ELLE S'APPLIQUE À CHAQUE LOT ET PASSE AVANT TOUT LE RESTE.
> *Pourquoi* : v159 a AGGRAVÉ la Toile sur l'iPhone de Tom (dès l'ouverture, les dalles écrasées et superposées). « Un lot qui casse ce qui marchait
> n'est pas livré. »
> **Un lot n'est « livré » que si les six conditions sont remplies. Sinon : écrire « NON LIVRÉ » et pourquoi, ne PAS commiter sur main, et demander.**
> - **A1 · NON-RÉGRESSION.** Avant de commiter, servir la version précédente à côté (`git show <hash>:app.html > zz-vNNN.html`) et comparer, sur les
>   mêmes chemins, tout ce que le lot peut toucher. Tout ce qui était bon avant l'est encore, au pixel ou à la mesure. Une seule régression = non livré.
> - **A2 · L'ÉTAT RÉEL DE TOM.** Le banc rejoue AUSSI l'état exporté de Tom (`?export=1` → `etats/tom-*.json`, `banc_tom.contexte_tom`), pas seulement
>   des jeux de test. Un défaut que Tom voit et que le banc ne voit pas : le banc a tort.
> - **A3 · ÉCHELLE DE SAFARI.** Toute mesure de mise en page à l'échelle 1 ET à l'échelle 0,79 (Safari iPhone : fenêtre 330 × 714 ou 390 × 692).
> - **A4 · MISE EN PAGE.** Pour tout élément d'interface touché, mesures à l'appui, clair et sombre, clavier ouvert et fermé, contenu court et long :
>   rien ne déborde de son cadre ni de l'écran, aucun texte coupé ou caché ; aucun recouvrement ; les espacements de l'échelle (aucun inventé, aucune
>   ligne qui saute) ; un texte remplit sa largeur : aucune ligne anormalement courte, sauf la dernière.
> - **A5 · PÉRIMÈTRE.** On ne touche que ce que le lot demande. Tout ce que Tom a déclaré bon est GELÉ. Si une correction exige de toucher autre chose :
>   s'arrêter et demander.
> - **A6 · HONNÊTETÉ.** Un point non reproduit, non mesuré ou non jugé est écrit comme tel, jamais « réglé ».
> Le rapport de chaque lot commence par le tableau A1 à A6, « tenu » ou « non tenu ».

> ## ⚑ LES COULEURS DE TOM — RÈGLE PERMANENTE (Tom, 26 oct. 2026, C-204). ELLE PASSE AVANT TOUTE RÈGLE DE CONTRASTE DE CE FICHIER.
> **Les couleurs de Tom ne se modifient JAMAIS sans sa demande : ni assombries, ni éclaircies, ni dérivées pour le contraste. Quand il dit « la
> palette par défaut », ce sont EXACTEMENT ses valeurs. Si une couleur paraît trop peu lisible, on le DIT dans le rapport, avec une capture, et
> on attend : on ne change rien.** (`window._teinte.ajuste` et toute dérivée « jusqu'à 3:1 » ne servent plus à poser une couleur nouvelle sans
> sa demande ; les dérivées déjà en place sont listées dans le rapport de v166 et attendent sa décision.)

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
> **⚑ v145 : la page porte SA version** (écrite par le serveur au moment de la servir) : `…/app.html?mesure=1` affiche « v145 · commit » en haut de
> tous les écrans, l'état de l'appareil, et envoie au Mac les images de chaque plantation (`mesures/appareil.jsonl`). ⚠ Le processus s'appelle
> `Python` : `pkill -f "python3 serveur.py"` ne le trouve pas — on le tue par `lsof -nP -iTCP:8752 -sTCP:LISTEN -t`.
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
| **Ma Parole !** | l'abonnement payant — **anciennement « Le Cercle »** (v106) ; **les exceptions nommées au « ! » : « Ma Parole ! », « Promi planté ! » (v146), « Parole tenue ! » et « Défi relevé ! » (v148, C-144), « Étoffe ta Toile, et partage-la ! » (v165, C-203)** | « Avec Ma Parole ! » · « Tu es Membre Ma Parole ! » · « Retourne ta Toile » · bouton « Bon, allez d'accord ». Espace insécable avant « ! ». Clés internes inchangées (`ouvreCercle`, `.s2-cercle`, `isPremium`) |
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

## 2 bis. LA RÈGLE DE TÊTE DU DESIGN (Tom, 14 oct. 2026 — C-130). Elle passe avant toutes les règles de design qui suivent.

> **« RIEN DE CHEAP, RIEN DE BORING, TOUT ARTY. Chaque transition, chaque texte, chaque apparition est dessiné. Est refusé d'office : tout ce qui
> « arrive d'un coup » ; le flou, le dégradé ou le fondu comme moyen d'apparition ; toute forme géométrique parfaite qui se translate ; tout texte noir
> sur blanc sans hiérarchie. JAMAIS de contour ni de liseré autour des lettres, nulle part. Avant de livrer, une question : est-ce qu'un illustrateur le
> signerait ? »**
> Le vocabulaire posé en v146 pour l'appliquer : **les flaques** (`variantes/flaques.js` — une matière qui naît dans des creux tirés au hasard, grossit,
> se rejoint, se vide ; bord net, aucun dégradé) ; **le tracé des lettres** (`variantes/trace-lettres.js`, C-125, à brancher après l'accord de Tom) ;
> **la découpe** d'une ligne de texte de gauche à droite, au rythme du tracé, en attendant lui.

## 3. Les couleurs — la règle des trois tons

Un écran de fiche porte **toujours trois couleurs distinctes** :

1. **La dalle** — sa couleur propre, issue du monde et de la palette choisis au Studio
2. **Le champ** — la couleur de la NATURE (Promi, Chiche, Cercle) — jamais l'état
3. **Le trait** — il porte l'ÉTAT (à tenir, en cours, tenu), et se juge en ΔE sur le champ

*(Repris le 30 sept. 2026 : l'ancienne formulation « le fond = l'état » est morte depuis la direction Horizon — le champ dit
la nature, la ligne dit l'état.)*

### ⚑ v163b (25 oct. 2026) — LES CORRECTIONS DE L'AUDIT DES BOUTONS (AUDIT-BOUTONS.md, C-186). (Décisions du chef de chantier.)
> Chaque point cite le numéro de l'audit ; ce que l'audit marquait « non vérifié » a été joué au doigt avant d'être touché.
> **⚑ C-189 (audit 15, point 1) — UNE PAROLE NE SE TIENT QUE PAR LE TRAIT.** L'acte TENIR du Fil est retiré (TRACER ouvre la fiche, REPORTER reste) ; `feedKeep`, son
> message du 2e et du 5e tenu et la réaction ✧ sont retirés avec leur code ; la carte de la Toile (`openCell`, jamais appelée) ne tient plus rien. **Les seuls chemins
> qui écrivent « tenu »** : le sélecteur d'état de la fiche (`#segStatus`, que seul le trait actionne) et la dernière part tracée (`lot-V145-PARTS`). Juge : **`redteam_tenu_trait.py`**.
> **Ce point CORRIGE le §5 (« un ajout validé, hors inventaire — le Fil, le seul endroit d'où l'on tient une parole sans ouvrir une fiche ») : l'appui
> maintenu déplie toujours la rangée du bandeau, mais elle porte TRACER (qui ouvre la fiche) et REPORTER.** `redteam_fonctions` remis au niveau (original en sauvegarde).
> **⚑ C-190 (audit 27, point 2)** : « Avant d'acheter » porte « Plus tard » (`.tard-non`, le dessin de « Garder ton achat ») et se ferme au toucher dehors — sans
> rien acheter (`ferme('__non')` : ni `valideAchat`, ni second encart). Juge : **`redteam_avant_acheter.py`**.
> **⚑ C-191 (audit 14, 15, point 3) — LES MENUS ⇅** : le Fil trie (`fdSortMode` posé par TRIER) et filtre (`_filTrieFiltre`, sur les cartes de `_s4Fil`, qui portent
> maintenant `data-pid`) ; `#fdSort` retiré ; QUADRILLAGE retiré de l'Index (le pincement reste) ; « Manquées » → « À tenir » ; le repère de l'option choisie est une
> barrette (14 × 4, comme la pagination du Studio). ⚠ `fd-terra` est la terre d'une parole TENUE : il ne dit pas « à tenir ». Juge : **`redteam_tri_menus.py`**.
> Le bouton ⇅ : deux propositions en capture (le mot « TRIER », trois traits qui raccourcissent) — Tom choisit (Q582).
> **⚑ C-192 (audit 5, 8, 10, point 4) — PEAUFINER** : DISSOUDRE LE CERCLE et PIÈCES JOINTES d'un Cercle branchés au GESTE (`lot-V163B-PEAUF` ; feuille « Dissoudre … ? »,
> annulation, « « X » dissous ») ; le + des pièces jointes d'un Promi DANS la rangée (44 pt) ; COMMENTAIRES retiré partout (les cartes du Cercle remontent de 120 :
> DESCRIPTION 244, MEMBRES 364, PIÈCES JOINTES 444, « + Planter » 552, le bloc Ma Parole ! 630) ; INVITER, LES PROMI DU CERCLE, À QUI, AVEC retirés du Peaufiner de la
> page + (la phrase les porte) ; « À QUI JE LANCE » absent sur un Chiche reçu. Juge : **`redteam_peauf_rangees.py`**.
> **⚑ C-193 (audit, point 5) — FERMER RAMÈNE D'OÙ L'ON VIENT** (`lot-V163B-PILE`, hors du moteur) : l'ORIGINE se lit au doigt, à `pointerdown` — l'écran sous le centre
> de l'appareil (ni `.show`, ni l'ordre des enveloppes d'`openDetail`) ; une destination ouverte dans la seconde empile {origine, destination} ; son X (`.closeb`,
> `[data-close]`) la ferme puis rend l'origine par sa propre porte (l'Index et le Fil à leur défilement). Un doigt sur l'accueil, ou une porte ouverte par script,
> vide la pile. Le X de Peaufiner ferme Peaufiner seul (`ouvre(false)`, `_s2Ouvre(false)`, `peaufOuvre(false)`). La page + qui se ferme remet `_brouillonRepris` et
> `_ppGarde` à zéro. Trouvé (déjà en v162) : les cellules « Tenu ensemble » d'une personne ne s'ouvraient pas au doigt — elles répondent au geste. Juge :
> **`redteam_pile_retour.py`** (« redteam_retour » est le juge de C-028). ⚠ Un juge qui touche une carte du fil d'un Cercle attend la pose : le fil change de
> géométrie après un défilement et « + Planter » colle sur la carte.
> **⚑ C-194 (audit 7, 9, 10, point 6)** : la ligne « Un mot… » est le seul endroit pour commenter ; un seul magasin pour un Cercle (`promi_cercle_mots`) — l'autre chemin
> (COMMENTAIRES, `_addComment`, `cur` nul sur un Cercle) n'a jamais rien enregistré : rien à migrer.
> **⚑ C-195 (audit 20, 21, 27, point 7)** : UN « Tout effacer » aux Réglages (feuille, 5 s pour annuler, `localStorage.clear()`) ; « Se déconnecter » seulement avec un
> compte (posé en `!important` : une règle des Réglages l'emportait) ; l'action des feuilles de confirmation à l'encre du mode, pleine, en gras. Juge : **`redteam_tout_effacer.py`**.
> **⚑ C-196 (audit 2, 10, 31, point 8)** : le rail du pinceau défile (page +, Peaufiner d'une fiche, d'un Cercle ; `touch-action:pan-x`, marge de 24 au bout) ; un trait
> de Ma Parole ! est un MUR (`.pc-mur`, flou 4,8 px, dans `murs()`) : plus de « — 0,50 € », plus de pointillé, plus d'application sans payer. Juge : **`redteam_pinceau_rail.py`**.
> ⚠ Les glissés de `banc_tom` ne font défiler aucun conteneur et WebKit mobile n'a pas de molette : le juge lit le débordement, `touch-action` et `scrollLeft`.
> **⚑ C-197 (audit 3, 5, 10, 15, 19, 20, point 9) — UN MOT PAR RÔLE** : l'échéance « demain · 1 sem. · 1 mois · une date… · un jour » (la phrase, `#dueChips`, `ECHEANCE`
> de la fiche — le calendrier s'y ouvre enfin —, REPORTER du Fil : demain · 1 sem. · 1 mois) ; « demain » = 1 jour partout ; « qui ose ? » ; « Inviter » ; la rangée
> « Le Studio » des Réglages retirée. **C-198 (audit 18, 31, point 10)** : pendant une phrase de mur, le X ferme, jamais l'offre ; au Studio, Sombre/Clair et
> Avec/Sans texte sortent du mur, les barrettes restent actives. **C-199** : petites corrections (voir CHANTIERS). Juge : **`redteam_audit_v163.py`**.
> ⚠ **Sur le panneau du Studio, le mur n'est plus que la part floutée : la phrase se pose au-dessus des réglages libres** (du haut du panneau au haut de
> `#stpLab`, 576 → 646 pt mesuré), jamais sur eux ; palettes ouvertes, leur panneau les recouvre (`libreStudio` répond non sur lui — trouvé en jugeant :
> 10 touchers sur 20 sans phrase). ⚠ La dette de la loi des points s'est vue : « · ·· ··· » (Q410, v135) était hors de l'écran ; COMMENTAIRES retiré, la
> liste remonte de 120 et la montre — inscrite dans `lexique-dette.json` avec sa source, rien d'inventé (Q583).
> **Contrats remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v163b.py`) : `redteam_echeance`, `redteam_peaufiner` (les pastilles de
> C-197), `redteam_nuee` (C-192 : cartes −120, COMMENTAIRES absent), `redteam_fonctions` (C-189), `redteam_dessin` G (le X de C-173), `redteam_murs_toucher`,
> `redteam_studio_tom`, `redteam_studio_mur` (C-198 : rouges sur v163a), `redteam_part` (C-184 : le trait à 10 × 1,15 — il rougissait depuis v163a, sa série ne
> l'avait pas passé), `redteam_couleurs_ref` (E22, E23), `redteam_air` (le Studio s'ouvre par la barre si `#openStudio2` manque).

### ⚑ v168 (27 oct. 2026) — LA FLÈCHE DU GUIDE EN GOUTTE (C-205, variante C). (Décisions Tom.) Ce bloc CORRIGE v167 (la forme de la flèche du guide).
> **Validés par Tom : C-181 (la veille repart à 60 s), C-203 §2 (la phrase 2 au cobalt).**
> **⚑ C-205 — LE DÉPART DE LA PAGE + EST LA RÉFÉRENCE, ET IL NE CHANGE PAS** (Tom : « ça reste, et c'est la référence ») : le ruban orange qui part épais du bord
> gauche (22,7 pt visibles au bord) et s'effile en 1,95 pt sous le chevron. **Les fiches ne changent pas non plus** (le trait, le départ de la seconde moitié, le trait
> tenu : v167 au pixel). **Seules les flèches du guide** (Studio, +, Partager) prennent la forme C : **la goutte** — le profil de l'amorce de la page + étiré sur le
> corps de la flèche, fermé côté queue en goutte (elle naît fine et s'arrondit sur ses 28 premiers pour cent) : 17,6 pt au plus large, à 17 pt de la queue ; 11,4 pt
> à 45 pt ; 6,4 pt à 65 pt ; puis la pointe (`_onde.chevron`). Rien d'autre ne change : 96,3 pt d'encre, la courbe douce (5 pt), la place (la pointe 1 pt dans la
> zone nette), l'orange, le clignotement calé sur le I (fixe en mouvement réduit), en flaques avec la zone. ⚠ Le brief disait « le plus large = l'épaisseur du trait »
> et « plus fin au départ » : la forme que Tom a désignée l'emporte (22,7 pt au bord). Page de variantes : `promi-fleches-variantes.html` (fonds réels, sans la couche
> du trait, `variantes/fleches/`). Juge : `redteam_guide_fleche` G remis au niveau (la goutte ; original en sauvegarde ; rouge sur v167 : 81/93). Preuve A1 :
> `scratchpad/v168/a1.py` — fiches et pages + à v167 servie à côté, au pixel, deux thèmes, deux échelles (la dalle muette, le hasard réamorcé à l'ouverture de la
> page + : sans cela la phrase suggérée change et toute la page avec).
> ⚠ **TROUVÉ PAR LA SÉRIE : `redteam_volume` rougissait depuis v167 (208 « volumes nouveaux », tous anciens)** — `lot-V167-DOIGTS`, posé en tête de `<head>`, volait
> l'attribution du `<style>` sans id qui le suit (le piège de v145 : un `<script id>` avant un `<style>` sans id). Le script ne peut pas bouger (il doit passer avant
> tout écouteur) : le juge rend « (hors bloc) » après un script posé AVANT tout bloc nommé (original : `sauvegardes/redteam_volume-avant-v168.py`) ; vert sur v167
> et v168, la sonde rougit. ⚠ `redteam_guide` : trois rouges de cadence (une image de 29 à 34 ms) — la même pire image sur v167 servie à côté, sous la même charge
> (4,1 à 5,9) : NON JUGÉ (C-137).

### ⚑ v167 (27 oct. 2026) — RETOURS iPHONE DE TOM SUR v166 : LA FLÈCHE DU GUIDE REFAITE, LA PHRASE 2 AU COBALT, LA VEILLE QUI NE PARTAIT PAS. (Décisions Tom.) Ce bloc CORRIGE v166 (la flèche, la couleur de la phrase 2, la veille à 120 s).
> **Validés par Tom : C-203 pour le reste (zones nettes, phrase 2, Partager facultatif). Q587 accepté pour l'instant : le « À » composé — Tom redessine lui-même
> PromiLate, il devra y dessiner le « À ». C-204 (la liste des couleurs dérivées) et Q588 (« t'appartient. » en clair) : Tom tranche après ses testeurs — RIEN TOUCHÉ.**
> **⚑ C-203 §1 — LA FLÈCHE DU GUIDE EST LE DÉBUT DE TRAIT DE LA PAGE + D'UN NOUVEAU PROMI** (Tom : « moches, trop courtes, s'arrêtent net, la fin plate est laide ») :
> le trait plein du tracé en cours (épaisseur 10 × `_TRAIT_K` = 13 pt, bouts ronds) et la pointe `_onde.chevron` ; **30 pt plus longue qu'en v166** (l'encre fait 96,3 pt
> de la queue à la pointe) ; **le bout arrière est ARRONDI** (le bout rond du trait, comme un trait qui commence ; plus de ruban effilé) ; **le corps est légèrement
> courbe** (une parabole régulière de 5 pt de flèche sur la corde, `chemin` sur y(x)) ; **elle CLIGNOTE en orange `#FB4C0D`, au rythme et par le code du I de PROMI**
> (`promiBlink 1.15s steps(1,end)`, la classe `.clignote` sur `#guideFleche`, son `currentTime` recopié sur celui de l'animation du I de l'accueil : même phase —
> un délai négatif ne la calait pas, mesuré 750 à 920 ms d'écart) ; fixe sous « Réduire les animations ». La pointe se pose 1 pt EN DEDANS du bord de la zone nette
> (la zone respire de ± 0,8 pt : à 0 elle sortait de 2,3 pt). Le reste de v166 tient (vers l'icône, rien de recouvert, en flaques avec la zone). **Exception NOMMÉE
> de A2 : le canevas de la flèche ne porte plus `data-eng` — c'est le seul élément du guide qui s'anime, par décision de Tom.** Juge : `redteam_guide_fleche.py`
> remis au niveau (93 : la longueur, le bout rond, la courbure, le clignotement en phase avec le I, rien recouvert ; fixe en mouvement réduit ; original en sauvegarde).
> **⚑ C-203 §2 — LA PHRASE 2 « Le reste s'explore à ton rythme. » : entièrement PromiLate, UNE couleur, le cobalt `#0E78F2`** (la couleur des mots-clés du guide),
> dans les deux thèmes ; sa place ne change pas (centre 422 pt). Juge : `redteam_guide_cloture` remis au niveau (original en sauvegarde).
> **⚑ C-181 §3 — LA VEILLE NE PARTAIT PAS SUR L'iPHONE. LE DÉLAI REPASSE À 60 s.** *La cause, reproduite sur l'état de Tom (WebKit, vrai chemin)* : la veille comptait les
> doigts posés par ses propres écouteurs `pointerdown` / `pointerup` ; or le gestionnaire des murs de Ma Parole ! (`lot-V104-MURS`), posé AVANT elle sur `window` en
> capture, appelle `stopImmediatePropagation()` sur le `pointerup` d'un toucher sur un mur (le Peaufiner d'une fiche, l'Aura, les Réglages…) : la veille ne voyait
> jamais le doigt se lever, elle le croyait posé POUR TOUJOURS et ne partait plus de la séance. *Corrigé* : un compteur de doigts posé TOUT EN HAUT de la page
> (`lot-V167-DOIGTS`, dans `<head>`, `window.__doigts`) — ses écouteurs passent avant tout autre ; il se vide aussi au `touchend` sans doigt restant, au `mouseup`
> et quand la page passe en arrière-plan ; la veille lit ce compteur (`_veille().doigts` ; `doigtsVeille` garde l'ancien, pour comparer). Aucun faux toucher fabriqué par
> l'app n'a été trouvé (les évènements non fiables tracés : aucun). *La règle* : **un compteur d'état du doigt se pose AVANT tout écouteur qui peut arrêter la
> propagation — sinon le premier `stopImmediatePropagation` le fige.** ⚠ Les touchers de `banc_tom` ne produisent AUCUN évènement de pointeur : un juge de ce défaut
> envoie de vrais `PointerEvent`. Juge : **`redteam_veille_depart.py`** (l'état de Tom, WebKit, veille rétablie, sans `?veille` : départ à 60 s ± 1 s après le dernier
> toucher sur cinq écrans — l'accueil, une fiche et un mur de son Peaufiner, l'Index, le Fil, l'Aura ; rouge sur v166). Contrat remis : `redteam_veille_bords` C (60 s).
> **Contrats remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v167.py`) : `redteam_guide_fleche` (la forme, le clignotement), `redteam_guide_cloture`
> (la phrase 2 au cobalt), `redteam_veille_bords` C (60 s), `redteam_guide` A2 (la flèche, exception nommée, `promiBlink` seul). Preuves sur v166 servie à côté : `redteam_veille_depart` 0/5,
> `redteam_guide_fleche` 69/93.

### ⚑ v166 (26 oct. 2026) — RETOURS iPHONE DE TOM SUR v165 : LES COULEURS EXACTES, LA FLÈCHE DU GUIDE, LA PHRASE 2, LA VEILLE SUR L'APP. (Décisions Tom.)
> **Validés par Tom : C-203 pour le reste, Q585, Q586. C-204 (la règle des couleurs) : en tête de ce fichier.**
> **⚑ C-165 — « T'APPARTIENT. » AUX COULEURS EXACTES DE LA PALETTE PAR DÉFAUT** : `#82AEF8` · `#FFB8D2` · `#C9A8F5` · `#EFE3C7`, en clair comme en sombre, dans l'ordre ;
> les dérivées du clair de v163 (`#476FB4` · `#9B5D75` · `#8161A8` · `#796E55`) sont retirées. ⚠ Mesuré, rien changé (C-204) : en clair, sur le fond de l'onboarding
> `#DEC8A3`, les lettres tiennent 1,0 à 1,4:1 (la crème ne se distingue presque pas). Juge : `redteam_appartient` (A : le style calculé au hex près ; A2 : l'encre lue ;
> le 3:1 n'est plus un critère, il est écrit ; original en sauvegarde).
> **⚑ C-203 §2 — UNE FLÈCHE ORANGE VERS CHAQUE ICÔNE** (Studio, +, Partager) : le dessin du départ de la page + au repos (`_onde.ruban` de 2,2 × à 0,15 × l'épaisseur,
> puis `_onde.chevron`, ep = 10 × `_TRAIT_K`), posé sur l'axe phrase → icône ; l'encre de sa pointe s'arrête au bord de la zone nette ; `#FB4C0D`, fixe. Elle vit
> sur son canevas (`#guideFleche`, ×3) ; la scène des flaques la peint (`Scene.fleche`) : elle naît en flaques avec `net(u)` et ne se voit que sous l'eau (elle part
> avec elle). `#guide[data-fleche]` déclare sa pointe et son angle (un pointeur, pas un verdict). Juge : **`redteam_guide_fleche.py`** (80).
> **⚑ C-203 §3 — LA PHRASE 2** : entièrement en PromiLate (le dessin des mots-clés : capitales), une couleur, l'encre du mode (`#201908` · `#F7F0DE`), à sa place
> (centre 422 pt) ; PromiLate n'a pas de « À » : composé comme l'É de v35, l'apostrophe de PromiLate retournée en accent grave (Q587). Pendant elle, trois zones
> nettes en flaques — Aura, Index, Fil — aux règles des autres (`Scene.zones` / `Scene.ajoute` : plusieurs zones ouvertes par le même `net(u)` ; à droite et à
> gauche, 0,8 pt avant l'icône voisine) ; elles restent ouvertes pendant que l'eau se retire ; pas de flèche. Partager n'est jamais obligatoire (les trois chemins,
> Partager touché et non). Juge : `redteam_guide_cloture` remis au niveau (original en sauvegarde).
> **⚑ C-181 §4 — LA VEILLE** : départ après **120 s** (`?veille=` reste) ; **61,2 pt/s** ; ses bords sont ceux de l'APP : `#device` à l'écran, recoupé avec la zone
> visible et les zones sûres (`cadre()`). *La cause, mesurée sur l'état de Tom (390 × 651)* : l'app y est réduite à 0,7466 (x 49,4 → 340,6, y 10,4 → 640,5) ;
> la veille couvrait toute la zone visible et rebondissait sur ses bords, hors de l'app sur les quatre côtés ; sur un ordinateur, sur la fenêtre entière. Le fond, le
> coin, les couleurs : inchangés. Juge : **`redteam_veille_bords.py`** réécrit (l'état de Tom, le cadre simulé 1440 × 900, 430 × 932, 330 × 714 ; le départ à 120 s ; la
> vitesse lue sur le logo, NON JUGÉE si une image dépasse 100 ms — la boucle borne son pas à 0,1 s ; original en sauvegarde).
> **`variantes/flaques.js`** : `grille`, `cheminZone` (la zone principale passe par le même chemin, au pixel près), `ajoute`, `zones`, `fleche`.
> ⚠ **TROUVÉ PAR A1 (v165 servie à côté), CORRIGÉ** : `redteam_guide_retour` C rougissait sur v166 (16/16 sur v165, même charge) — la copie de l'écran prise à la
> fermeture du Studio différait de 1 % de l'écran final : le canevas de la flèche (×3, 1170 × 2532) était EFFACÉ EN ENTIER à chaque image de la scène, et ce
> coût décalait la copie pendant que la Toile se posait encore. La flèche n'efface et ne repeint plus que SA boîte, et seulement quand son état change
> (vide · en flaques · pleine) : 16/16 deux fois. *La règle* : **un canevas de la taille de l'écran ne s'efface pas à chaque image pour un dessin qui n'en occupe
> qu'un coin.**

### ⚑ v165 (26 oct. 2026) — LA CLÔTURE DU GUIDE ; LE TITRE « PARTAGER » STABLE. (Décisions Tom.)
> **Validé par Tom : v164b (le trait × 1,3, TRIER, Ramage, C-202, C-200).** L'image isolée de 86 ms sous Ramage : notée, à rejouer au calme.
> **⚑ C-203 — LA CLÔTURE DU GUIDE** (`lot-V141-GUIDE`) : après l'étape du +, deux phrases de Tom, mot pour mot — **« Étoffe ta Toile, et partage-la ! »** puis
> **« Le reste s’explore à ton rythme. »** (impératifs et « ! » : EXCEPTIONS NOMMÉES, comme la phrase du Studio — `TEXTES_ENGAGEMENT.imperatifVoulu`,
> `redteam_engagement` VOULU). **Elle n'est pas contrainte.** La phrase 1 arrive dans tous les cas : (a) le + touché et quelque chose créé — au retour sur
> l'accueil, la page + fermée ou la parole plantée (état `apres-plus`) ; (b) le + touché puis ailleurs, le menu se ferme ; (c) ailleurs que le + — sa zone se
> referme, celle de Partager s'ouvre. Flou en flaques sauf autour de l'icône de Partager (`cible('partage')` : marge 4 à 10 pt, s'arrête 0,8 pt avant l'icône des
> Réglages, 5 pt en deçà du plateau, `dansPlateau`) ; « Toile » au bleu de « commence », « partage-la » au lilas de « monde » (Q586), PromiLate, tracées, aucun
> contour. Partager touché : il s'ouvre par-dessus le guide, à sa fermeture la phrase 2 ; ailleurs : la phrase 2. La phrase 2 au centre (422 pt), sans zone
> nette ; un toucher ou 3 s, et les flaques se vident (`finCloture`) ; `promi_guide` « 1 » : le guide ne revient plus. **Trouvé (chemin b) : au doigt, toucher
> ailleurs ne refermait pas le menu des natures** (WebKit ne fabrique pas de `click` sur la Toile vide, la règle de Q578) — le geste lui-même est lu
> (`touchend`, `pointerup` hors toucher). Juge : **`redteam_guide_cloture.py`** (130 : les trois chemins, Partager touché ou non, la zone lue sur l'eau,
> la fin, le lancement suivant ; clair et sombre ; 390 × 844 et 330 × 714). Contrats remis : `redteam_guide` 4.6 (le vidage jugé à la fin de la clôture),
> `redteam_engagement` (VOULU) — originaux `sauvegardes/*-avant-v165.py`.
> **⚑ Q585 — LE TITRE « PARTAGER »** : `ajusteTitres` mesurait la place sur la largeur de `.closeb` lue à l'instant — avant ou après que `lot-V157-CROIX` l'ait
> posée en zone de 44 pt, le titre rétrécissait plus ou moins, puis ne se remesurait plus (la clé ne portait pas le X) : 32 ou 35 px (et Réglages 34 ou 27).
> La place du X entre dans la clé ; le titre s'arrête 4 pt avant la zone de toucher du X. Mesuré : Partager 32 px, Réglages 34, Index 35, L'aura 35, Fil 31,
> six ouvertures chacun, aux deux échelles.
> **Q584** : rien (le texte de la Toile vide attend Tom).

### ⚑ v164b (25 oct. 2026) — LE TRAIT FIGÉ À × 1,3 ; TRIER ; RAMAGE AU STUDIO ; willReadFrequently ; LES HUIT POINTS DE L'AUDIT. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v164a (les paliers) et v163a (`?trait=`).
> **⚑ C-184 — FIGÉ** (Tom : « Je garde le palier ×1,3. Fige-le et retire ?trait=. ») : `window._TRAIT_K = 1,3`, plus aucun paramètre d'adresse. Les juges qui comparent à
> une version d'avant (v149, v162) posent `window.__TRAIT_BANC` par un script d'amorce (`redteam_pages_plus`), rien d'autre ne le pose. Points × 1,15 (min(K ; 1,15)).
> Contrats remis (originaux `sauvegardes/*-avant-v164b.py`) : `redteam_trait_k` (le défaut seul, ×1,3), `redteam_photo_trait`, `redteam_part` (K 1,3), `redteam_pages_plus`.
> **⚑ C-191 (Q582 → A) — TRIER** (`lot-V164B-TRIER-css`) : dans l'Index et le Fil, le mot « TRIER » seul, Gilbert 15 pt (la police des libellés, qui n'a que des capitales),
> à l'encre du mode (`#201908` clair, crème sombre), ni contour, ni fond, ni ombre, ouvert ou fermé ; la zone de toucher est le créneau de 52 × 52 pt (≥ 44), invisible.
> **⚑ C-175 (Q581) — RAMAGE AU STUDIO** : la silhouette de la jauge de Ramage est préparée à l'ACCUEIL, au repos (`lot-V20-STUDIO-AURA`, `prepare`) — après 8 s sans toucher
> ET 8 s sans changement de monde ni de palette (sans la seconde condition, le banc de rendu, à temps piloté, changeait Guingois : 14 images ; dans une page normale, mesuré,
> un rendu de Ramage ne change ni graines, ni cellules, ni une dalle de Guingois — la cause au banc n'est pas nommée). Hors de la même famille de semis (un ancien monde →
> Ramage ressème la Toile), elle ne peut pas être prête : au Studio elle attend 5,2 s de calme, hors des 5 s qui suivent l'arrivée. Volubilis reste gelé.
> Juge : **`redteam_ramage_jauge.py`** (D Mascaret, T l'état de Tom, E Pochade ; aucun rendu ni image > 50 ms dans les 5 s, au calme ; v164a rouge : 260 à 714 ms à 3,3 s).
> **⚑ C-202 — willReadFrequently, hors moteur** : les deux sites de l'app que Chrome signalait — les mini-dalles (`peintMinis`, relues par `_teinteDalle`) prennent l'option
> (rendu identique, mesuré au pixel en WebKit et Chromium) ; l'atlas des poils de la Pelote (`atlasAlpha`) NON : l'option y CHANGE le tracé des traits (mesuré, deux
> moteurs) — on y dessine comme avant, chaque tampon est recopié 1:1 dans un canevas fait pour être relu (copie exacte, mesurée). Le troisième avertissement vient du moteur
> (les canevas de `dalleTrame`) : non touché.
> **⚑ Q583** : « en l'air » reste tel quel (La Mémoire, Notifications).
> **⚑ C-200 — LES HUIT POINTS DE L'AUDIT** : ① le bandeau « Garder ta Toile » s'arrête au deuxième « Plus tard » (`promi_rappel_non`, `promi_rappel_fin` ; les refus d'avant
> comptent), la rangée des Réglages reste ; ② « RELANCER [nom] » retiré (la rangée du Peaufiner, `#actRelance`, son écriture « Tu as relancé… » dans le Fil) ;
> ③ Notifications : « de temps en temps, un mot » ; ④ le mot « Promi » de l'accueil n'ouvre plus Ma Parole ! (`lot-V12-js`, la porte n'est plus posée) ; ⑤ « ou 5,99 € par
> mois » retiré (C-090) ; ⑥ « Plante ton premier Promi — touche le + » retiré de la Toile vide, Q584 (ton texte) — ⚠ ce bloc est masqué sur l'accueil d'aujourd'hui ;
> ⑦ « Mention sur un dessin partagé » quitte les Réglages pour le panneau du Partage (« MENTION SUR UN DESSIN PARTAGÉ : Affichée · Masquée », `#shMentionRow`, même
> réglage `promi_dessin_mention`) ; ⑧ l'écran « La langue » (caché) et son code supprimés. Juge : **`redteam_v164b.py`** (31, au doigt ; 8/31 sur v164a).
> Contrat remis : `redteam_partage_dessin` C (la rangée dans le Partage ; original en sauvegarde).
> Contrat remis aussi : `redteam_decoupe` H (la préparation des silhouettes — `silhouettesAuRepos` — sort par son peintre ; elle rougissait déjà sur v164a,
> le juge n'était pas dans les séries récentes ; sonde : une dalle peinte dans un autre monde par un autre chemin est prise).
> **Série (un à la fois ; charge 3 à 158, l'autre session) — rouges classés** : `redteam_croix` (Partager à 0,79, intermittent préexistant : Q585) ; `toile_stable` T
> (une réouverture à 2,5–9,8 pt sous forte charge, v164a de même) ; `notifs` 7 (l'heure de passage : à 23 h le rappel de la veille est passé — 36/36 rejoué), 2a/2c
> une fois (36/36 rejoué deux fois) ; `tokens` (20 couleurs, 2 polices en dur — identiques sur v163b et v164a) ; `dessin` I (depuis v147). Ramage au Studio, sur
> l'état de Tom : une image de 86 ms une fois sur cinq passages (charge 3,5), non reproduite au calme (trois sondes : aucune image > 34 ms ; le juge : 29 ms) —
> NON NOMMÉE.

### ⚑ v164a (25 oct. 2026) — LE TRAIT : DES PALIERS QUI SE VOIENT ; LE BOUTON PHOTO NE TOUCHE PLUS LE TRAIT. (Décisions Tom.) Ce bloc CORRIGE v163a (C-184 : 1,10 · 1,15 · 1,20).
> **⚑ C-184 — « AUCUNE DIFFÉRENCE ENTRE 1,10, 1,15 ET 1,20 »** : le facteur s'APPLIQUAIT (lu au pixel avec `?mesure=1`, `lot-V164-TRAIT-MESURE` : au bas de l'écran,
> le facteur, l'épaisseur déclarée et l'épaisseur LUE sur le canevas) — les trois traits faisaient 11 · 11,5 · 12 pt : l'écart ne se voyait pas. **Paliers
> `?trait=1.3` · `1.5` · `1.8`** (plafond 2), défaut 1,15 en attendant le choix de Tom : trait plein 13 · 15 · 18 pt (lu 13,7 · 16 · 19), ruban de départ lu
> 21,7 · 25 · 30, flèche d'invite 5,9 · 6,8 · 8,1 pt. **Les points du trait non tracé ne grossissent plus** (Tom : « déjà limite un poil trop gros ») : × 1,15 au plus,
> Ø 10,4 pt (`window._TRAIT_PTS` = min(K ; 1,15) : sous 1,15 ils suivent le facteur, `?trait=1` rend ceux d'avant v162). Le mot du trait et ce qui est dessous descendent du même pas — sur la fiche ⌈28·(K − 1,05)⌉/2 (22 en v163a :
> mesuré, il manquait 0,3 à 1,7 pt d'air flèche → mot aux paliers neufs ; à 1,15 le pas reste 1,5) ; pages + inchangé. Juge : `redteam_trait_k` (paliers neufs).
> **⚑ C-201 — LE BOUTON PHOTO (changer la photo ou le dessin) ÉTAIT POSÉ SUR LES POINTILLÉS.** *Deux causes* : ① il se plaçait à un écart fixe d'UN point de l'onde
> (x 349), alors que l'onde monte ou descend sous lui et que le trait épaissit ; ② il n'était pas reposé quand la page + se recompose (mesuré à 0,79 : l'onde
> remontée de 32 pt, le bouton resté 23 pt dans les pointillés). *Corrigé* (`poseBouton`, `window._hautBoutonPhoto`) : sa cote est le plus haut de l'onde sous
> toute sa largeur, moins l'épaisseur du trait au facteur appliqué, moins 8 pt d'air, moins sa zone de toucher ; une veille par image le repose dès que l'onde de
> l'écran change. Juge : **`redteam_photo_trait.py`** (3 pages + et 4 fiches × 4 facteurs × 2 échelles ; l'encre du trait LUE sur le canevas sous le bouton, ≥ 1 pt d'air).

### ⚑ v163a (25 oct. 2026) — « T'APPARTIENT. » LETTRE À LETTRE, LE TRAIT RÉGLABLE, LA VEILLE AUX BORDS, LE GARDÉ DE CÔTÉ VISIBLE, LE SYMBOLE « RECADRER », LE MENU DE TRI QUI SE REFERME. (Décisions Tom.)
> **Validés par Tom (v162) : C-174 (l'onde à 0,5 : `?onde=` est retiré, figé), C-183, C-166, C-149 (garder de côté), C-185, C-175 sous Chantourné, Guingois, Mascaret (gelés).**
> **⚑ C-165 — « T'APPARTIENT. » : UNE COULEUR PAR LETTRE**, dans l'ordre de la palette de base (comme « Studio » au guide) — sombre `#82AEF8` · `#FFB8D2` · `#C9A8F5` ·
> `#EFE3C7` ; clair `#476FB4` · `#9B5D75` · `#8161A8` · `#796E55` (≥ 3:1 sur le VRAI fond de l'onboarding `#DEC8A3`, pas le `#DFCAA4` du guide) ; la ponctuation garde le ton
> de la lettre d'avant ; « La suite » ne change pas. Juge : **`redteam_appartient.py`** (lettre par lettre, deux échelles ; rouge sur v162). `redteam_mots_sombre` confie
> ces lettres à ce juge (son « fond » tombait sur la lettre voisine).
> **⚑ C-184 (récidive) — `?trait=<facteur>`** (par rapport à la taille d'avant v162), **défaut 1,15** : trait, points, pointe, flèche d'invite des pages +, des fiches, de
> l'instant et d'un Cercle ; pas l'onboarding. **Le mot du trait et tout ce qui est dessous descendent du même pas** (fiche `e.dyTrait` = ⌈22·(K − 1,05)⌉/2 — v164 : ⌈28·(K − 1,05)⌉/2 ; pages +
> `--pp-dyt` = ⌈14·(K − 1,05)⌉/2 pt : la phrase, le rail du pinceau, « garder de côté » à 718 + ce pas) — l'air flèche → mot ≥ v162. Juge : **`redteam_trait_k.py`**
> (A les épaisseurs piégées, B l'air lu sur l'image, C aucun recouvrement neuf ni débordement, à 430 × 932 et 330 × 714 ; D l'onboarding au pixel).
> Contrats remis : `redteam_garder` J (718 + le pas), `redteam_pages_plus` (servi sous `?trait=1`) — originaux `sauvegardes/*-avant-v163.py`. **Tom choisit 1,10 · 1,15 · 1,20, puis on fige.**
> **⚑ C-181 §3 — LA VEILLE** : l'encre du logo se lit sur les **pixels peints** (plus `measureText`, dont la boîte dépassait l'encre : 1,3 pt au banc) ; entrée et sortie en
> flaques **350 ms**. ⚠ Au banc (390 × 651, 430 × 932, 330 × 714) l'encre touche les quatre bords à 0,3 pt : le défaut de l'iPhone n'est PAS reproduit, la cause écrite
> est probable, non prouvée. Juge : **`redteam_veille_bords.py`** (15 ; rouge sur v162).
> **⚑ C-149 suite — LE GARDÉ DE CÔTÉ DANS L'INDEX** : pointillé de **3 pt**, `#291547` en clair, `#A77CF7` en sombre (la couleur de la nature s'y confondait avec le
> champ) ; le champ reste plein. **Q579** : toucher « gardé de côté — dans l'Index » ouvre l'Index filtré (`ixFiltre='brouillons'`). Juge : **`redteam_garde_index.py`** ;
> `redteam_couleurs_ref` E21.
> **⚑ C-188 — LE SYMBOLE « RECADRER »** (`lot-V163-RECADRE`) : plus d'encart ni de fond — les quatre coins, **22 pt d'encre** (svg 29), encre du mode, zone de **44 pt**
> invisible, en bas à droite (encre à 12 pt de la barre, bord droit à 24 pt) ; il **naît en flaques** (300 ms) quand la vue bouge sous la main, **part en flaques** après
> **4 s** sans toucher, revient au déplacement suivant ; recadré, il part ; le double toucher reste. Juge : **`redteam_recadre_bouton.py`** (16). Le symbole : capture, Tom juge.
> **⚑ Q578 — LE MENU DE TRI** : au doigt, WebKit ne fabrique un `click` que sur un nœud « cliquable » ; le fond du menu de l'Index (et ses options !) n'avaient aucun
> écouteur : un écouteur VIDE posé sur `#ixMenu`/`#fdMenu` les rend cliquables, l'écouteur d'origine décide ; un toucher dans le panneau ne referme plus rien (Fil
> compris). Juge : **`redteam_menu_tri.py`** (8 ; 4/8 sur v162). *La règle* : **un écouteur délégué au document ne reçoit pas de clic au doigt sur un nœud qui n'en a pas.**
> **⚑ C-175 (§6) — RAMAGE AU STUDIO : NON RÉGLÉ.** Q580 ne vise pas Ramage (son aperçu ≈ 0) ; sous le doigt p95 18 ms ; à l'arrivée, le seul bloc est la silhouette de
> la jauge (231 à 519 ms, 3 s après) — Q581. Mesuré sous une charge de 15 à 30 : non jugé au calme.
> ⚠ **Les glissés de `banc_tom` sont des TouchEvent créés en JavaScript : ils ne font défiler AUCUN conteneur** (sur aucune version) — un juge de défilement lit le
> débordement, `touch-action` et `scrollLeft` ; le geste réel se regarde sur l'iPhone.

### ⚑ v161 (24 oct. 2026) — LA VEILLE (C-181). (Décision Tom.)
> **`lot-V161-VEILLE`** (en fin de page) : après 60 s sans aucun toucher (`?veille=N` pour les juges), sauf pendant une saisie (un champ a la main) ou un geste
> (un doigt posé) : fond plein `#050302`, PROMI seul (PromiLate, une boîte de 140 × 40 pt : l'encre 140 × 27 centrée — c'est la boîte qui rebondit), 60 pt/s,
> rebonds sur les zones sûres (59 · 34 · 8 pt), la couleur suivante de la palette du Studio à chaque rebond (un ton sous 3:1 sur le fond sauté), l'amande
> `#8FE08F` au coin exact (2 pt), l'angle 45° ± 2 à 3° tiré à chaque rebond ; aucun coin dans la première minute ni dans la minute qui suit un coin
> (`?coin=1` en force un entre 60 et 90 s). La trajectoire est calculée par ÉVÉNEMENTS (le prochain bord) — la même fonction sert l'écran et
> `window._veilleSimule` : 30 × 2 h, un coin toutes les 16,6 min, aucun avant 108 s. Le logo est un canevas peint UNE fois par couleur, déplacé par
> `transform` (jamais `fillText` dans la boucle). Entrée et sortie en flaques (`_passageFlaques` couvre / ouvre). Un toucher la quitte, rend l'écran exact et
> n'actionne rien (propagation arrêtée, le clic qui suit avalé 800 ms). Wake Lock : demandé au premier toucher, redemandé au retour au premier plan, relâché
> à 10 min de veille ; Swift : `isIdleTimerDisabled` (portage/SPEC-ECRANS). « Réduire les animations » : le logo fixe au centre.
> ⚠ **LA VEILLE EST COUPÉE SUR LES BANCS** (navigateur piloté, ou `promi_veille_off` posé par `banc_tom`) sauf `?veille=` : un juge qui reste plus de 60 s
> sans toucher ne la voit jamais. Juge **`redteam_veille`** (16 ; rouge sur v160c).

### ⚑ v160c (23 oct. 2026) — Q574 (LE STUDIO REND LA VUE), C-180 (LA PAROLE LONGUE), C-175 (RAMAGE AU STUDIO). (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v160 (C-180 « non livré ») et v159 (`lot-V159-VUE`, reposé en partie).
> **Validé par Tom : C-177 (« plus aucune dalle superposée »).** Q574, Q576 tranchées ; Q573, Q575 (et Q577) : un lot « moteur » à part, après les testeurs — **on ne touche
> pas au moteur d'ici là.**
> **⚑ Q574 — `lot-V159-VUE` REPOSÉ, SA PARTIE « STUDIO » SEULE, ET UNE SESSION DU STUDIO** : le Studio ouvert, la vue est TENUE — `window._vueMain` et
> `window._recadreDemande` sont des ACCESSEURS (la synchronisation d'un ressemis écrivait « vue libre, recadrage demandé » et recadrait aussitôt pour le monde
> traversé) ; refermé, elle est rendue : même genre de cadrage qu'à l'ouverture → la vue d'avant, au point près ; un autre genre choisi → recadrée et suivie
> (v159). Hors du Studio, plus aucun recadrage au changement de monde (reposé tel quel, il suivait les changements de monde du banc de rendu : 81 images
> sur 280). ⚠ Recadrer parce que les GRAINES ont bougé (le ressemis, Q573) est faux : Esquille à 1 parole sautait de 202 pt (5 → 1,173). Mesuré : plus aucun saut
> de vue après le Studio (Terrazzo : 55 à 112 pt avant) ; `redteam_toile_stable` M 85/100, les 15 rouges = Q573 (graines à 0,9–1,3 pt) et Q575.
> **⚑ C-180 — LA PAROLE LONGUE** (`composeParole`, onboarding) : composée ligne par ligne dans un cadre fixe (342 pt) — coupe aux espaces, chaque ligne remplie
> (seule la dernière courte), un mot trop long coupé à la largeur, chaque ligne `white-space:nowrap` ; la même coupe clavier ouvert et fermé ; > 3 lignes →
> 35 → 22 px ; à 22 px autant de lignes que la place au-dessus de « Petite ou grande promesse » et du trait ; au-delà, COUPE PROPRE : « Je me promets d’appeler
> … » puis la fin de la parole (la parole entière est gardée). **Q576 : le champ n'a plus de limite** (80 avant, un reste). Juge **`redteam_parole_longue`**
> (144 ; rouge sur v159 : 42/72).
> **⚑ C-175 (B2) — RAMAGE AU STUDIO** : sa silhouette de jauge est un bloc de 237 à 308 ms (son premier rendu de la séance) qui tombait pendant l'arrivée ; elle
> attend 3 s sans toucher (la préparer sur l'accueil au repos, essayé : son premier rendu laisse un état dans le moteur, le banc de rendu changeait sous Guingois — retiré). Arrivée : 246 ms (au calme, v160b) → 22 à 65 ms ; le bloc tombe
> sur un Studio immobile. Juge **`redteam_studio_arrivee`** (rouge sur v160b). **Guingois, Mascaret, Chantourné : NON CORRIGÉS** — le coût est l'image de
> l'aperçu (moteur) ; repeindre une image sur deux n'a rien gagné (le moteur rattrape le temps écoulé : chaque image coûte plus) — essai retiré (Q577).
> ⚠ Volubilis (gelé) : 2,9 s d'un bloc à l'arrivée ; Tesselle : une image de 200 ms au repos — signalés, non touchés.
> ⚠ **Halin à 1 parole au mauvais cadrage (1,163)** : 0 sur 24 isolé, 3 fois sur 4 dans les longues séries, en v160b comme en v160c — non jugé au calme (charge
> 5,7 à 10,3), cause non nommée, rien corrigé.

### ⚑ v160 (23 oct. 2026) — C-177 : LES DALLES ENTASSÉES ÉTAIENT DANS LES DONNÉES DE TOM ; UNE COURSE AU LANCEMENT ; L'EXPORT DE L'ÉTAT ; LA PORTE DE QUALITÉ. (Décisions Tom.) Ce bloc CORRIGE v159 (`lot-V159-VUE` est RETIRÉ depuis v160a) et v146 (C-124, la place de la parole de l'onboarding).
> **⚑ C-179 — `?export=1`** : à l'ouverture, l'app envoie au serveur du Mac (réseau local seulement) tout son stockage et l'écran → `etats/tom-<date>.json`
> (hors git) ; `banc_tom.contexte_tom(b, chemin)` le rejoue (sa fenêtre, sa densité, son thème ; `echelle=1` pour 430 × 932). ⚠ Le serveur s'arrête avec le
> Mac : un envoi fait pendant qu'il est arrêté se perd (le message « État envoyé au Mac » paraît quand même) ; ⚠ le dernier fichier n'est pas toujours le bon
> (un onglet vide exporte une Toile vide) : le juge prend le dernier QUI PORTE DES PAROLES.
> **⚑ C-177 — LA CAUSE ÉTAIT DANS LES DONNÉES.** Sur l'état de Tom : six paroles sur sept à la MÊME place, [0.42, 0.74], écrite en dur par l'onboarding depuis
> v146 et redonnée à chaque parole par l'onboarding rejoué ; le moteur rend chaque parole « à la cellule vide la plus proche de sa place » → six dalles collées
> (écart mini 1,3 à 5,5 pt) dans les neuf versions de v152 à v160a. *Corrigé hors du moteur* : `window._reparePlaces` (à la relecture de l'état et avant chaque
> enregistrement ; aussi `promi_nueplace`) efface une place hors de [0, 1], non numérique ou à (0, 0), et, entre deux places de la même famille à moins de
> 0,003, garde celle de la plus ancienne parole ; le moteur en choisit une autre et la note lui-même. L'onboarding ne donne [0.42, 0.74] que si aucune dalle
> ne l'a déjà (premier lancement : inchangé). *La règle* : **une valeur enregistrée se vérifie avant d'être écrite et à la relecture ; quand un défaut survit à
> l'annulation du code, on cherche dans les données, pas dans le code.**
> **⚑ C-177 — LA SECONDE CAUSE, UNE COURSE AU LANCEMENT** : les paroles sont synchronisées par un minuteur de 320 ms (`app.html` ≈ l. 8505) et le monde relu
> par `lot-V71-REOUVERTURE` (30 000 lignes plus bas) ; quand la page met plus de 320 ms à se lire, les paroles sont cadrées dans le monde par défaut, puis le monde
> change sans recadrage : sous les douze mondes « faits de leurs seules paroles », la vue d'ouverture tirait au hasard entre deux cadrages (v160a : 3 à 4 fois
> sur 8 le mauvais ; dalles déplacées jusqu'à 267 pt d'une ouverture à l'autre). La synchronisation (toujours à 320 ms) attend le monde relu (`_studioRelu`,
> 3 s au plus). Les huit anciens mondes et Ritournelle : identiques à v160a ; Esquille sort son cadrage serré (v160a : toujours celui du monde par défaut).
> ⚠ Non expliqué : 1 fois sur 28, Halin à 1 parole sort à 1,163. ⚠ **Un recadrage « quand la Toile se pose » est FAUX** (essayé, retiré) : `autoView` n'est
> pas le même au placement et au repos (Pochade 5 : 1,191 → 1,199 ; Halin : ses cellules compagnes) — il déplaçait des cadrages validés.
> **⚠ Une Toile chargée en temps réel n'est pas comparable au pixel** d'un fichier à l'autre : un simple commentaire ajouté (aucun code) change l'image une
> fois sur deux à 25 paroles. Au pixel : `banc_rendu` (horloge pilotée). Juges : **`redteam_toile_stable` étendu** (T l'état de Tom à deux échelles, X données
> abîmées, S Toile saine, M 20 mondes × {1, 5, 9, 25, 50} ; T 0/6 sur v160a), `redteam_onb_rejeu` E (rouge sur v160a).
> **⚑ C-180 (B3) — LA PAROLE LONGUE DE L'ONBOARDING EST COMPOSÉE LIGNE PAR LIGNE** (`composeParole`) : en cours, non livré dans ce lot. Le champ garde 80
> caractères au plus (existant, sans décision écrite).

### ⚑ v162b (24 oct. 2026) — LOT MOTEUR, AUTORISATION EXCEPTIONNELLE DE TOM : RAMAGE SANS ROSACE, LE STUDIO AU DOIGT. (Décisions Tom.)
> **⚑ C-187 — RAMAGE N'EST PLUS UNE ROSACE** (`_parure`, Ramage seul ; le Worker du film en reçoit le texte) : chaque œil tire de SA clé une forme (trois
> harmoniques), un tourbillon (plumes courbes, sens et force tirés), des bandes décalées, un cœur ovale irrégulier (angle d'or ± 0,03, rayon, taille et nombre
> de feuilles variés). Déterministe : la même Toile d'une ouverture à l'autre. Banc de rendu : 14 images de Ramage changent, les 266 autres au pixel (la
> référence de Ramage n'est PAS refigée : Tom juge d'abord). Avant : `sauvegardes/promi-moteur-avant-v162b.js`.
> **⚑ C-175 (Q577) — LE DOIGT SUR LE STUDIO** (`_apDoigt`, posé par l'app sur `#studioScreen`, levé 400 ms après) : sous Ramage, Mascaret, Chantourné,
> Guingois (`_AP_GESTE`), aucun événement NEUF de l'aperçu et aucune préparation de Ramage pendant le geste. Gain partiel, mesuré à charge égale (non calme) ;
> la cause restante est nommée (la scène d'une transition d'aperçu est reconstruite à chaque image, jamais gardée — Q580). **Non réglé.**

### ⚑ v162a (24 oct. 2026) — L'ONDE RÉGLABLE, LE TRAIT × 1,05, LA PHRASE DU CERCLE, « GARDER DE CÔTÉ » QUI GARDE, LE FOND DU TRI, LE GUIDE APRÈS LE STUDIO, L'AUDIT DES BOUTONS. (Décisions Tom.)
> **Validés par Tom : C-180, C-174 (la taille de la flèche), Esquille, Éclisse, le tracé des lettres hors onboarding. C-182 : Tom valide de nouveau son premier
> Promi — cause inconnue, aucune correction ; le relevé d'erreurs ne vit plus que derrière `?diag=1`.**
> **⚑ C-174 — `?onde=0…1`** règle l'amplitude de l'onde du premier Promi (onboarding seul), défaut 0,5 ; le haut de l'encre ne bouge pas. Tom choisit.
> **⚑ C-184 — LE TRAIT × 1,05, ET RIEN D'AUTRE** (`lot-V162-TRAIT`, `window._TRAIT_K`) : épaisseur, points, pointe et flèche d'invite des pages +, des fiches,
> de l'instant et du trait d'un Cercle ; l'onboarding inchangé. Juge : **`redteam_trait_105.py`** (les valeurs de dessin piégées, rapport 1,05 ± 0,005).
> **⚑ C-183 — LA PHRASE DE LA PAGE + DU CERCLE 10 pt PLUS BAS** (`_dyP` −31) ; elle ne touche ni « garder de côté » ni la barre (`redteam_pages_plus`).
> **⚑ C-149, RÉCIDIVE — « GARDER DE CÔTÉ » GARDE L'ÉTAT ENTIER DE LA PAGE +** (`lot-V162-GARDER`) : la cause, l'ancien chemin `#addDraft` (titre seul, ni nature,
> ni personnes, ni Cercle ; sans titre, rien). Le gardé de côté est dans l'Index (« GARDÉ DE CÔTÉ »), sa carte rouvre la page + dans sa nature et son état
> (`p.brouillon`). Il n'existe pas d'écran « Tout ce que j'ai gardé de côté » (Q579). **Trouvé en jugeant (dès v152) : un second rendu de la phrase d'un Chiche
> vidait son titre (« Chiche de … ») — la coupe ne vide plus jamais un titre.** Juge : **`redteam_garder_reprise.py`** (3 natures, avec et sans personnes, l'app
> rouverte ; rouge sur v161).
> **⚑ C-185 — LE TRI DU FIL ET DE L'INDEX (⇅, que Tom appelle « Réglages ») NE FAIT PLUS PASSER LE FOND AU BRUN** : `.ix-menu::before` posait l'encre du mode
> à 60 % sur toute la page, et le panneau une ombre portée (un volume) — retirés. Juge : **`redteam_tri_fond.py`**. Q578 : l'Index ne referme pas ce menu au
> toucher hors du panneau (déjà en v161).
> **⚑ C-166, RÉCIDIVE — LE GUIDE APRÈS LE STUDIO, SUR LE CHEMIN DE L'ONBOARDING** : la signature du fond est la Toile réelle (graines et vue) ; sous le Studio,
> le moteur ne prépare le fond qu'à la vue × 1 (**`Toile.renderTo(…, {vue:true})` ne porte pas un zoom ≠ 1 sous plusieurs mondes — moteur, non corrigé** ; or
> après « Promi planté ! » la vue est à × 2) ; dès que le Studio commence à se refermer, l'écran réel est copié et flouté ; le flou commence à quitter le
> Studio dans son dernier 15 % de course, l'étape du + attend qu'il soit sorti (C-172), 240 + 400 ms. Juge : **`redteam_guide_retour.py`** (rouge sur v161).
> **⚑ C-186 — `AUDIT-BOUTONS.md`** : écran par écran, rien changé.
> **⚑ C-181 (v161b-2 §3) — LA VEILLE AUX VRAIS BORDS** : elle couvre la fenêtre visible (`visualViewport`, zones sûres), le logo rebondit à son ENCRE
> (140 × 27 pt × l'échelle), le fond est celui de la Toile du thème, chaque couleur tient 3:1 (sinon ajustée, l'amande aussi) ; coins 0,3 à 0,5 % du temps,
> aux trois fenêtres (430 × 932, 330 × 714, 390 × 651). Juge : `redteam_veille` (33).

### ⚑ v159 (22 oct. 2026) — LES DALLES QUI « NE SONT PLUS À LEUR PLACE » (LA VUE D'UN AUTRE MONDE), NET DÈS LA VALIDATION DU PAIEMENT, LA SILHOUETTE DE LA JAUGE PRÉPARÉE AU REPOS, LA PAROLE LONGUE DE L'ONBOARDING. (Décisions Tom et chef de chantier.)
> **Validés par Tom : C-173, C-176, C-170 (« Garder ton achat »). Q568 tranchée (chef de chantier). Q569 reportée à Swift (portage/DETTE.md E-18). Le point d'arrêt tient : pas d'E4.**
> **⚑ C-177 — CE QUI BOUGE EN REVENANT À LA TOILE EST LA VUE, PAS LES DALLES.** Mesuré (banc comme Tom, 20 mondes × 5 et 25 paroles × sept pages) : les
> graines ne bougent jamais. Un changement de monde au Studio ne recalculait pas le cadrage automatique : la Toile glissait, à la fermeture, vers la CIBLE
> d'un autre monde (les mondes « faits de leurs seules paroles » se cadrent serré à moins de neuf paroles) — Éclisse à 5 paroles après Bobinette et
> Ritournelle : zoom 1,19 → 1,68, les dalles décalées de 112 à 267 pt. Présent tel quel en v152 (le moteur n'a pas changé depuis v147). *Corrigé hors du
> moteur* (`lot-V159-VUE`) : quand le GENRE de cadrage change (ancien · serré · semis neuf · Ritournelle) et que la vue n'est pas celle de la main
> (`_vueMain`), la cible est recalculée, puis suivie pendant que les graines se posent (jamais sous le Studio) ; au lancement aussi (la cible était prise
> avant que les graines soient posées : 1,9 pt). *La règle* : **une cible de vue calculée pour un monde n'est jamais gardée pour un autre ; un juge de
> géométrie compare la Toile À L'ÉCRAN (graine × vue), pas les seules graines.** « S'empilent » tel quel : non reproduit (Q571). Juge :
> **`redteam_toile_stable.py`** (sept pages, dont le Studio en aller-retour qui croise les familles de semis ; 1 pt à l'écran ; rouge sur v158 : 112 pt).
> **⚑ C-177, LA SECONDE CAUSE EST DANS LE MOTEUR — NON CORRIGÉE (Q573)** : à neuf paroles et plus, un aller-retour au Studio qui traverse les deux familles de
> semis ressème la Toile ; chaque parole reprend `p.place` (une seule place, réécrite par l'autre famille, datée de la plantation), puis le relâchement la
> pose ailleurs : Ramage à 25 paroles, 15 à 56 pt (v158 aussi). Une place par famille notée hors du moteur ne ramène qu'à 15 pt (le relâchement ne revient
> pas au même point) : essai retiré. `redteam_toile_stable` peut y rougir par intermittence (80/80 à la passe complète de v159 ; pris trois fois sur Ramage en cours de lot).
> **⚑ C-170 (complément) — DÈS LA VALIDATION DU PAIEMENT, TOUT EST NET** (le toucher qui achète, sur « Avant d'acheter ») : `valideAchat` (les couches
> floutées partent, le verrou du monde tombe d'un coup — sans fondu de filtre —, l'hôte des encarts n'a plus de voile, l'encart sort sur l'image nette,
> le déverrouillage ne passe plus par l'aperçu flouté). Avant : le flou en flaques reste. Juge : **`redteam_achat_valide.py`** (10 ; rouge sur v158).
> **⚑ C-175 (suite)** : la silhouette de la jauge (un bloc de 50 à 490 ms 1,2 s après l'arrivée sur un monde, pendant que l'aperçu bouge) est PRÉPARÉE AU
> REPOS sur l'accueil, une par tâche (la règle des tâches de fond de v143), pour les mondes de la famille de semis en place — Ramage et Volubilis jamais
> (Q569). Non jugé au calme. Juge : `redteam_studio_saccade` E.
> **⚑ Q568 — AU-DELÀ DE TROIS LIGNES, LA PAROLE DE L'ONBOARDING SE RÉDUIT** (35 px, un pas d'1 px à la fois, 22 au plus bas ; l'interligne et la chasse
> suivent) ; « Petite ou grande promesse » reste ; rien sur le trait ; le → garde sa place libre. Juge : `redteam_suite_libelle` D (rouge sur v158 : la
> parole moyenne passait déjà à quatre lignes et « Petite… » recouvrait la consigne). Q572 : la parole de cinq lignes descend à 23 px.

### ⚑ v158 (21 oct. 2026) — RETOURS iPHONE DE TOM SUR v157 : LE X À LA TAILLE DU X D'« INDEX », PLUS AUCUN FLOU SUR « GARDER TON ACHAT », LE STUDIO SANS SACCADE SOUS LA JAUGE, LE → QUI NE RECOUVRE PLUS LA CONSIGNE. (Décisions Tom.) Ce bloc CORRIGE v157 (C-173 : la taille du X calculée page par page).
> **Validés par Tom : C-172, C-174, C-171. Q565 acceptée (PromiLate n'a qu'une graisse). Le point d'arrêt tient : pas d'E4.**
> **⚑ C-173, RÉCIDIVE — LE MÊME X PARTOUT, À LA TAILLE EXACTE DU X DE « INDEX »** (35 px, lue sur le titre de l'Index, `window._tailleX`), PromiLate, la couleur
> de rôle du titre de sa barre, seule la place change (à droite, centré sur les capitales du titre), zone de 44 × 44. *La cause* : v157 calculait la taille page
> par page et la DIVISAIT PAR L'ÉCHELLE de l'appareil alors que la capitale était déjà en pixels CSS — dans Safari (≈ 0,8) le X sortait 22 à 27 % trop gros ; le
> juge tournait à l'échelle 1. *Les règles* : **une taille de texte se pose en pixels CSS, jamais divisée par l'échelle de l'appareil ; un juge de taille tourne
> AUSSI à l'échelle de Safari (330 × 714 : ≈ 0,79) ; une capture d'élément se cale sur des pixels entiers (WebKit rééchantillonne un cadre fractionnaire).**
> Juge : `redteam_croix` réécrit (original `sauvegardes/redteam_croix-avant-v158.py`).
> **⚑ C-170, RÉCIDIVE — « GARDER TON ACHAT » : PLUS AUCUN FLOU NI VOILE.** *La cause trouvée dans le code* (le chemin de l'iPhone n'est pas reproduit, Q570) : le
> Studio net n'était pris que si un sondage (un point à 40 % de la hauteur) tombait sur le Studio ; sinon l'encart retombait, sans rien dire, sur le voile noir à
> 50 % de son hôte et sur l'image de la Toile de l'ACCUEIL. *Corrigé* : le Studio ouvert suffit ; jamais de fond flouté ni de voile pour le second encart ; à son
> ouverture, `purgeFlou` retire toute couche floutée de l'achat (un passage en flaques qui porte une image floutée le DÉCLARE : `data-flou`). *La règle* (la même
> que C-172) : **un état se demande à son propriétaire, il ne se devine pas à un point sondé — et un repli ne retombe jamais sur ce qu'on vient d'interdire.**
> Juge : **`redteam_achat_net.py`** (15 ; D pose exprès la situation qui trompait v157 : rouge sur v157).
> **⚑ C-175 — LE STUDIO SACCADE** : trois causes, toutes du travail fait pendant le geste : la teinte appliquée à chaque mouvement du doigt (→ une fois par image) ;
> les trames des écrans CACHÉS derrière le Studio repeintes à chaque cran de teinte (→ elles attendent la fermeture du Studio, une par tâche, sans doigt) ; la
> dalle de la jauge refaite à chaque cran et à chaque arrivée sur un monde (→ gardée par monde, refaite au calme). **Non jugé au calme** (charge 10 à 128).
> Restes : `repaintWorld` du moteur (720 ms à l'arrivée sur Volubilis), Touffe sous la jauge (Q569). Juge : **`redteam_studio_saccade.py`** (comptes de travail,
> durées au calme ; rouge sur v157).
> **⚑ C-176 (Q567) — LE BOUTON → DE L'ONBOARDING prend la place libre la plus proche** (lue sur les lignes réelles des textes, 6 pt d'air), jamais sous la consigne ;
> le texte ne bouge pas. Une parole de cinq lignes fait déborder la page entière (déjà en v156) : Q568. Juge : **`redteam_suite_libelle.py`**.

### ⚑ v157 (21 oct. 2026) — REPRISE APRÈS v154–v156 : LE STUDIO NET DERRIÈRE LE SECOND ENCART, « DESIGN DÉBLOQUÉ » EN AMANDE, LE + DU GUIDE APRÈS LE STUDIO FERMÉ, UN SEUL « X », LA FLÈCHE DE L'ONBOARDING × 2. (Décisions Tom.) Ce bloc CORRIGE v156 (C-170 : « le second encart floute le Studio de son instant »).
> **Validés par Tom : C-094 (le moment du flou du Studio), C-169 (la flèche à 1,5 s), C-170 (le fond de l'encart d'achat), C-167, C-168. Le point d'arrêt tient : pas d'E4.**
> **⚑ C-170 (suite) — APRÈS L'ACHAT, LE STUDIO EST NET DERRIÈRE LE SECOND ENCART** (« Garder ton achat ») : aucun fond, aucun voile ; le panneau naît et part en
> flaques sur l'image NETTE du Studio (`netStudio`, option `net` de `_onbCompte`). Le premier encart garde son flou en flaques. Juge : `redteam_achat_fond` D, E
> (l'écran avec l'encart = l'écran sans lui, au pixel, au-dessus du panneau, le Studio figé ; original : `sauvegardes/redteam_achat_fond-avant-v157.py`).
> **⚑ C-171 — « Design débloqué ✓ » EN AMANDE `#8FE08F`** (la célébration ; 10,2:1 sur le fond du toast `#281F10`). Juge : `redteam_achat_fond` F.
> **⚑ C-172 — LE + DU GUIDE N'ARRIVE QU'APRÈS LE STUDIO FERMÉ.** *La cause* : le guide décidait « de retour sur l'accueil » par un sondage — un point de l'écran (45 %
> de la hauteur) qui ne tombe sur aucun écran, et la Toile au repos ; rien ne demandait si le Studio était fermé. Le chemin de l'iPhone n'a pas été reproduit
> (Q566). *La correction* : `studioFerme()` dans `lot-V141-GUIDE` — jamais l'accueil tant que le Studio porte `.show` ou n'est pas sorti de l'écran. *La règle* :
> **un état se demande à son propriétaire (le Studio est-il fermé ?), il ne se devine pas à un point sondé.** Juge : **`redteam_guide_studio.py`** (7 ; C rougit sur v156).
> **⚑ C-173 — PARTOUT, « × FERMER » EST UN SEUL « X »** : PromiLate (400 : une seule graisse, Q565), hauteur = la hauteur de capitale du titre de sa barre (± 1 pt),
> couleur du titre, pleine opacité, zone de 44 × 44 pt centrée sur l'encre, en face du titre. **Un seul propriétaire : `lot-V157-CROIX`** (le glyphe vit dans son
> `span.x157-g`, posé en absolu ; une veille de 400 ms repose la croix si un autre propriétaire réécrit son style — le Peaufiner — ou si le titre change de taille ;
> `aria-label="Fermer"`). ⚠ **`lot-POLICES` réécrit le style en ligne du `span` à chaque passage** (même police, même graisse : sans conflit) — un juge qui efface la
> croix le fait par une règle de VISIBILITÉ, pas par sa couleur en ligne. Juge : **`redteam_croix.py`** (34 écrans × 2 thèmes : aucun « FERMER », l'encre du X lue
> sur l'image contre la capitale du titre, la couleur, la zone prise à ses quatre coins).
> **⚑ C-174 — LA FLÈCHE DU PREMIER PROMI × 2, VERS LE BAS** : épaisseur, chevron, points (rayon et pas) et amplitude × 2 ; la base de l'onde reposée pour que le
> haut de l'encre reste au même pixel (671,5 pt) ; le canevas 118 → 236 ; rien n'est dessous. Juge : **`redteam_fleche_onb.py`** (12 ; v156 servie à côté ; rougit sur v156).
> **Trouvé, non changé (Q567, identique sur v156)** : clavier ouvert, le bouton → recouvre la fin de « trace pour planter ».
> **Contrats remis au niveau** (originaux : `sauvegardes/*-avant-v157.py`) : `redteam_achat_fond` (le second encart : le Studio net, plus le flou), `redteam_onboarding`
> O7 (la zone du trait de l'onboarding 236 pt, plus 118). **La flaque qui fait naître ce trait s'arrête au bas de l'écran** (sinon elle prenait l'image de la Toile
> au-delà, vide : `redteam_transitions_onb` T2). `redteam_tenir` G et `redteam_fluide` : **non jugés** (charge jamais sous 4 pendant le lot ; 671 au pire — l'émulateur
> d'une autre session).

### ⚑ v156 (21 oct. 2026) — RETOURS iPHONE DE TOM SUR v155 : LE FLOU DU STUDIO ENCORE PLUS TÔT, LA FLÈCHE À 1,5 s, L'ENCART D'ACHAT SUR LA TOILE DU STUDIO. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v155 (C-094 : 350 ms ; C-169 : 1 s).
> **Validés par Tom : C-167, C-168, C-169 sur les fiches. Q562, Q563 acceptées (chef de chantier).**
> **⚑ C-094 — LE FLOU DE LA PHRASE DU STUDIO : 250 ms DE CALME** (600 → 350 → 250 ; `ATTENTE = GD.ATTENTE − 350`). Juges : `redteam_guide` (0,20 à 0,85 s), `redteam_transitions_onb` T6.
> **⚑ C-169 — DANS L'ONBOARDING, LA FLÈCHE ET « TRACE POUR PLANTER » PARAISSENT 1,5 s APRÈS LA VALIDATION DU PRÉNOM** (1 s en v155) ; rien d'autre ne change.
> Juge : `redteam_depart_orange` (1 500 ± 50 ms).
> **⚑ C-170 (rouvert, Q564) — L'ENCART D'ACHAT FLOUTE LA TOILE DU STUDIO.** *La cause* : l'encart « Avant d'acheter » naissait en flaques depuis `imageToile()`, la copie de la
> Toile de l'ACCUEIL — sous le Studio elle n'est pas repeinte (la cause de v155) : l'ancienne Toile ; son « flou » n'était qu'un voile. *Aujourd'hui* : devant le Studio, l'encart
> floute `#stBg` (le monde et la couleur affichés, `Flaques.floute` 4,8), préparé au doigt posé sur « Adopte ce design » ; ce flou paraît EN FLAQUES (1,1 s, gardé sous le panneau,
> `#achatFond`) et s'en va de même ; le second encart (« Garder ton achat ») floute le Studio de son instant. Juge : **`redteam_achat_fond.py`** (49 ; les douze mondes payants).
> **⚑ C-171 (trouvé en jugeant) — LE TOAST NE PREND PLUS LE DOIGT** : « Design débloqué ✓ » se posait sur « Plus tard » du second encart (3,2 s sans réponse) ; le texte d'un
> toast laisse passer le toucher, ses boutons le prennent (`lot-V156-TOAST-css`).
> **Contrats remis au niveau** (originaux : `sauvegardes/*-avant-v156.py`) : `redteam_guide`, `redteam_transitions_onb` (T2 : 2,7 s ; T6), `redteam_depart_orange`.

### ⚑ v155 (21 oct. 2026) — RETOURS iPHONE DE TOM SUR v154 : LE FLOU DU STUDIO PLUS TÔT, LE VERT À 2,15 s, LA ZONE DU CURSEUR DE COULEUR, LE DÉPART ORANGE ET CLIGNOTANT, PLUS RIEN NE CLIGNOTE SOUS « RÉDUIRE LES ANIMATIONS », LE DÉVERROUILLAGE SANS IMAGE PÉRIMÉE. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v154 (C-167 : 2 400 ms) et v144–v148 (le guide : 0,6 s de calme).
> **Validés par Tom : C-166, la réduction des animations (v154 §4), la mention (v154 §5). C-125 : Tom le juge au prochain lot — on n'y touche pas.**
> **⚑ C-094 — LE FLOU DE LA PHRASE DU STUDIO COMMENCE 250 ms PLUS TÔT** : 350 ms de calme au lieu de 600 (`ATTENTE = GD.ATTENTE − 250`) ; le reste de la séquence
> garde ses durées. Juges remis au niveau : `redteam_guide` (le moment, 0,30 à 0,95 s), `redteam_transitions_onb` T6 (0,15 à 0,95 s).
> **⚑ C-167 — LE VERT À 2 150 ms** (`_tenirRegle.AMANDE`), le toucher qui le fait remonter reste. **La phrase de validation est déjà centrée** : son encre, lue sur
> les pixels de la nappe, a son centre à 194,5–194,7 pt pour 195 (Promi, Chiche, un Promi d'un Cercle ; clair, sombre ; dans la hauteur visible de Safari) —
> rien changé. Juges : `redteam_tenir_presse` (2 000–2 450 ms), **`redteam_centre_validation.py`** (± 1 pt, 8/8) ; `redteam_fluide`, `redteam_tenir` E remis au niveau.
> **⚑ C-168 — LA DALLE DE LA JAUGE DES COULEURS S'ATTRAPE** : sa zone tactile fait 56 × 56 pt (un pseudo-élément transparent de la dalle, `lot-V155-CURSEUR-css`),
> son dessin ne change pas ; attrapée dans sa zone, elle ne saute plus sous le doigt (l'écart est gardé, en teinte comme en noir et blanc). Aucun élément
> touchable n'y tombe (dernière rangée de pastilles à 737 pt, la zone commence à 754). Juge : **`redteam_curseur_couleur.py`** (12 ; 3/12 sur v154).
> **⚑ C-169 — LE DÉPART DU TRAIT EST ORANGE `#FB4C0D`, LA POINTE ET LE TRAIT DE DÉPART**, partout, deux thèmes, tous pinceaux : l'amorce (fiche, page +) ; sur une fiche
> à moitié tracée, les 43 derniers pt du trait avant la pointe du milieu (Q563) ; ma part à plusieurs ; sur la page +, la part tirée pendant le geste (signée,
> elle reprend sa couleur). **Onboarding** : « trace pour planter » et la flèche paraissent **1 s après Retour sur le prénom**, avant la parole (tracée sans parole :
> la saisie s'ouvre, Q562) ; le départ est peint sur SA couche (`#onbDepart`, sans toucher) qui porte **l'animation même du I, `promiBlink`, calée sur sa phase**,
> jusqu'au premier toucher sur le trait, puis orange fixe. **Le clignotement n'existe que dans l'onboarding** (chef de chantier). ⚠ Un juge qui LIT l'orange du départ
> de l'onboarding attend la phase pleine (opacité 1). Juge : **`redteam_depart_orange.py`** (34).
> **⚑ Q561 (chef de chantier) — « RÉDUIRE LES ANIMATIONS » : PLUS RIEN NE CLIGNOTE** : le I de PROMI (accueil, onboarding, titres) et le départ de l'onboarding restent
> fixes. Les règles du I portaient `promiBlink` en `!important` à deux id, hors condition : `lot-V154-REDUIT-css` les coupe à trois id.
> **⚑ C-170 — DÉVERROUILLER UN MONDE PAYANT : JAMAIS UNE IMAGE PÉRIMÉE.** *La cause, mesurée* : sous le Studio, la boucle de la Toile ne peint pas (`frame()` saute tant que
> `#studioScreen` porte `.show`) ; `setTheme` changeait le monde mais `#toileCv` gardait l'IMAGE DE L'ANCIEN MONDE jusqu'à la première image après la fermeture (0,5 s) —
> le Studio qui glisse la découvrait ; et le flou du verrou partait par un fondu de filtre (1,4 → 0 px en 0,34 s). *Corrigé à la source* (`lot-V155-DEVERROUILLE`) :
> tout changement de monde ou de palette sous le Studio rend la Toile de l'accueil par le moteur (`Toile.renderTo`, vue de l'écran), à la fin du passage ou au plus
> tard quand le Studio se referme — jamais pendant qu'on feuillette (l'aperçu saccaderait) ; au déverrouillage, l'aperçu flouté s'ouvre EN FLAQUES (700 ms) sur le monde
> net ; le `setTheme` attend la fin du passage (sous Volubilis il bloque 2 s). *La règle* : **une surface qui ne se peint pas quand elle est couverte garde une image
> périmée ; elle se rend AVANT d'être découverte.** Juge : **`redteam_deverrouille.py`** (25 : les douze mondes payants).
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v155.py`) : `redteam_guide` et `redteam_transitions_onb` (C-094 : le
> moment 350 ms ; T2 : la flèche naît 1 s après le prénom), `redteam_tenir` E, `redteam_fluide`, `redteam_tenir_presse` (2 150 ms), `redteam_onboarding` O7 (le départ se lit
> aussi sur sa couche `#onbDepart`), `redteam_onboarding_texte` (l'orange du départ lu à la phase pleine), `redteam_onb_sorties` (« trace pour planter » sur la page
> de la parole), `redteam_pages_plus` (la fiche identique à v149 HORS du départ orange de la seconde moitié, 140 → 200 pt, qui doit y être orange).

### ⚑ v154 (20 oct. 2026) — RETOURS iPHONE DE TOM SUR v153 : LE TRACÉ À 40 CAR/S SANS ONDE, LE FOND DU GUIDE APRÈS LE STUDIO, LE VERT 400 ms DE PLUS, « RÉDUIRE LES ANIMATIONS » PARTOUT. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v153 (C-125 : 22 car/s, une lettre à la fois, R3) et v144 (C-111 : l'amande à 2 000 ms).
> **Validés par Tom : C-164, C-163, la réduction des animations (C-077), Q554, Q557.**
> **⚑ C-125 — LE DÉBIT ET LA DURÉE D'UNE LETTRE SONT SÉPARÉS** (`variantes/trace-lettres.js`) : une lettre PART tous les 1000/cps ms — **40 car/s par
> défaut** (`?cps=` le règle ; une espace compte 0,4 ; `?tlv=0.05` ralentit tout) ; chacune se trace en **70 à 90 ms** selon la longueur de son chemin
> (au moins quatre images à 60 Hz ; jamais plus de 3 × 1000/cps − 1) ; **au plus trois lettres en cours, strictement de gauche à droite**, la suivante
> commence avant la fin de la précédente, jamais avant elle (`etat().actives`). **L'« onde » que Tom voyait était la règle R3** (chaque lettre partait là
> où la précédente avait fini, en alternant haut et bas) : **R3 EST RETIRÉE**, chaque lettre prend son tracé naturel (« h » quand elle l'a). La finition de
> v153 (bout plat, coins, ergots, alpha borné) ne bouge pas. Juge : `redteam_trace_lettres` (46 : ④ aucune onde ; ⑪ le temps de plume, pas à pas d'1 ms,
> et sur les pixels trois fronts séparés ; ⑦ ⑧ le débit et les images par lettre À L'ÉCRAN — jugés sous une charge de 4 seulement ; 38/46 avec le module de
> v153). Capture ×0,05 : `scratchpad/v154/trace-x005.png`.
> **⚑ C-166 — AU RETOUR DU STUDIO, LE FOND FLOUTÉ DU GUIDE EST CELUI DE LA TOILE RÉELLE.** Il était pris une fois, au lancement du guide. Sous le Studio,
> dès que le monde ou la palette ont changé et ne bougent plus depuis 900 ms (aucun doigt depuis 600 ms), la Toile est **rendue par le moteur** dans la vue
> de l'écran (`Toile.renderTo(…, {vue:true})`) — **sous le Studio, le canevas de l'accueil (`#toileCv`) n'est PAS repeint : le relire donne l'ancien
> monde** — puis floutée dans un Worker (le flou de `Flaques.floute`, à l'identique) ; l'étape du + attend ce fond (1,95 s au plus). Sans changement, rien
> n'est recalculé : le fond est le même au pixel. ⚠ **Sous le Studio la Toile tourne toujours (`Toile_state().running` reste vrai : elle porte ses
> aperçus)** — un garde « la Toile posée » n'y passe jamais. `window._guideFlou`. Juge : **`redteam_guide_fond.py`** (12 ; 8/12 sur v153).
> **⚑ C-167 — LE VERT DE « PAROLE TENUE ! » RESTE 400 ms DE PLUS** (`_tenirRegle.AMANDE` 2 000 → **2 400**), pour toutes les phrases de validation (Promi,
> Chiche, la part, le rideau rejoué). **Décision du chef de chantier : un toucher n'importe où pendant ce temps fait remonter le vert tout de suite et mène
> à la fiche tenue** (`window._tenirVite`) — lu 300 ms après le lever et tant que le vert n'a pas commencé de remonter ; **le toucher est AVALÉ** (rien
> dessous ne s'ouvre ; Q560). Sans toucher, le retour se fait seul. R4 (l'invariance) reste vert. Juge : **`redteam_tenir_presse.py`** (7 ; 1/7 sur v153).
> Contrats remis au niveau (originaux : `sauvegardes/*-avant-v154.py`) : `redteam_fluide` (2 400 ms, l'animation jusqu'à 3 100), `redteam_tenir` E (2,5 à 3,2 s).
> **⚑ §4 — « RÉDUIRE LES ANIMATIONS » : PROMI SUIT LE RÉGLAGE DE L'iPHONE POUR TOUTE L'APP, SANS INTERRUPTEUR.** Vérifié : guide, onboarding (ni tracé ni
> passage en flaques), tenir (E3), la vie au repos, le souffle de la Pelote. **Deux mouvements y échappaient — l'anneau du + qui tourne (`heroSpin`) et les
> nappes de la carte « Ma Parole ! » (`cercleBlobs`) : posés sur `::before` / `::after`, que la règle générale `*{animation:none!important}` NE TOUCHE PAS**
> (`*` ne sélectionne pas les pseudo-éléments) — arrêtés par `lot-V154-REDUIT-css`. Le I de PROMI clignote encore : ce n'est pas un mouvement (Q561).
> **§5 (réponse à Tom, rien changé) — « Mention sur un dessin partagé »** : l'image d'un dessin partagé porte en bas à gauche le logo « Promi » et, au-dessus,
> la nature (« PROMI », « CHICHE », « CERCLE ») ; désactivée, la nature disparaît de l'image, le logo reste toujours (v137, C-068).

### ⚑ v153 (20 oct. 2026) — LE CLAVIER APRÈS LE PRÉNOM, LE TRACÉ DES LETTRES (RÉCIDIVE), « T'APPARTIENT. » EN COULEUR, L'ENTOURAGE DU +, PUIS E3. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v147 (C-125 : 40 à 60 car/s) et v151–v152 (Q548 pour « t'appartient. »).
> **⚑ C-164 — LE PRÉNOM VALIDÉ, LE CLAVIER SE FERME** (le champ perd le focus) ; la page de la parole ne trace ses textes qu'une fois le clavier
> ENTIÈREMENT redescendu (`apresClavier` : la hauteur de `visualViewport` revenue et stable 160 ms ; 1,6 s au plus ; sans clavier, rien n'attend). La
> parole se saisit en touchant la phrase (Q557). ⚠ **Un juge d'onboarding qui tape la parole touche d'abord la phrase** (`[data-onb="parole"]`) : sans
> cela il tape dans le vide. Juge : **`redteam_clavier_onb.py`** (clavier simulé : `visualViewport` descend et remonte comme sur iOS ; 6/6 ; 3/6 sur v152).
> **⚑ C-125, RÉCIDIVE — LE TRACÉ DES LETTRES À 22 CARACTÈRES PAR SECONDE** (Tom : « 20 à 25 au départ, réglable ») : `?cps=N` (5 à 80) la règle, `?tlv=0.05`
> la ralentit pour regarder — jamais mémorisés ; la vitesse vit dans le module (`TL.defauts.cps`), l'app ne la passe plus. *La cause du « pof »* : le module
> traçait bien, mais à 50 car/s une lettre durait ≈ 20 ms, une image à 60 Hz. *Et les éclats* : au coin haut-droit du « g » d'Atkinson (la panse revient au
> fût tracé d'abord), la bissectrice coupait l'encre en triangles — à une FERMETURE en angle (> 40°) entre deux traits COURBES, le premier tracé garde
> toute sa largeur et sa tête biseautée se dévoile d'une coupe plate avant lui ; un trait droit garde sa priorité ; un TOURNANT (fin d'un trait, départ
> du suivant) garde la coupe en onglet. La rampe d'opacité d'un pixel est bornée à deux sous-pixels de chemin. Toutes les autres lettres des deux polices :
> identiques au pixel à v152 (planches `scratchpad/v153/planche-*.png`). *La règle* : **un tracé se juge en temps réel sur l'écran (combien de temps
> chaque lettre est EN COURS), pas seulement pas à pas ; et un coin se regarde lettre par lettre.** Juge : `redteam_trace_lettres` ⑦ à ⑩.
> **⚑ C-165 — « T'APPARTIENT. » EN COULEUR** : `#0E78F2` en clair, `#82AEF8` en sombre (`.onbv-app`) ; « La suite » ne change pas (crème en sombre, Q548).
> **⚑ C-163 (Q553) — AUTOUR DU +, LA ZONE NETTE DU GUIDE VA DE 4 À 10 pt** (7 ± 3 ; « Tom refuse le rond ») ; le Studio garde 6 à 10.
> **⚑ E3 (C-077, A1 prime)** : le moment « tenir » est le rideau validé. **R4 est ACTIF** (`redteam_tenir_e3 --r4`, appelé par `redteam_engagement`) : deux
> paroles qui diffèrent sur tout donnent la même séquence, lue sur les pixels du rideau ; la borne de 1 000 ms vaut pour le MOUVEMENT (lever → rideau à la
> barre ≈ 670 ms), l'instant posé garde ses 2 s (Q554). **`window.promiHaptique(nom)`** (`lot-E3-HAPTIQUE`) : vide, appelé avec 'tenir' au lever ; Safari
> iOS ne vibre pas, Core Haptics au portage (C-022). **« Réduire les animations » : la fiche passe TENUE d'un coup — ni rideau, ni instant, ni fondu.**
> Tâches longues pendant la séquence : jugées au calme seulement. **PUIS POINT D'ARRÊT : Tom fait repasser ses deux testeurs ; rien ne démarre avant son
> retour, pas d'E4.**

### ⚑ v152 (19 oct. 2026) — DERNIERS RETOURS DE TOM, CLÔTURE DE LA SÉRIE : « ENCHANTÉ » RETIRÉ, LES MOTS COLORÉS EN SOMBRE. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v151 (l'échelle : la ligne « texte ») et v147 (C-124 §4, la première ligne de la page du prénom).
> **Validés par Tom (« tout a l'air ok ») : C-154, C-157, C-149, C-159, C-160 ; C-124 et C-126 pour le reste. Q547 : l'orange du libellé gardé partout
> (vu et validé). Q549 close. Décisions du chef de chantier : Q548 (« La suite t'appartient. » reste crème en sombre), Q550 (« félicitations » dans la
> phrase de Tom seulement, exception nommée), Q551 (REPORTER compte depuis aujourd'hui quand l'échéance est passée).**
> **⚑ C-124 §1 — LA PAGE DU PRÉNOM : « [Prénom], donc. »**, mot pour mot ; « Enchanté. » est supprimé ; la ligne ne bouge pas (184 pt), « Quid d'un Promi à
> toi-même ? » et « Petite ou grande promesse, elle compte. » ne changent pas. Juge : `redteam_onb_sorties` (textes en dur).
> **⚑ C-162 — LA RÈGLE (Tom) : TOUT MOT COLORÉ EN CLAIR EST COLORÉ AUSSI EN SOMBRE, dans l'onboarding comme dans les phrases du guide — même rôle, même
> famille de couleur. En sombre, chaque couleur prend sa variante claire de la palette, au moins 3:1 sur le fond sombre : bleu → `#82AEF8`, rose →
> `#FFB8D2`, lilas → `#C9A8F5` ; les lettres de « Studio » leurs équivalents clairs.** L'inventaire, relevé page par page, clair contre sombre : seuls
> quatre mots sortaient crème, tous dans la phrase du + du guide — Promi, Chiche, Cercle et « commence » (`phraseHTML` ne les colorait qu'en clair) ; ils
> prennent `#82AEF8` · `#FFB8D2` · `#C9A8F5` · `#82AEF8`. Déjà colorés : les natures de l'onboarding, le I de PROMI, « PROMI » de « Promi planté ! »,
> Primo · Deuxio · Tertio (`#0E78F2`, 4,7:1 — validé en v151, gardé), « monde », les lettres de « Studio ». **Deux exceptions NOMMÉES, des décisions
> écrites : « trace pour planter » (crème en sombre, Tom v151 C-126 §5) et « La suite t'appartient. » (crème en sombre, Q548).** Un mot ajouté demain
> à l'onboarding ou au guide tombe sous la règle. Juge : **`redteam_mots_sombre.py`** (inventaire RELEVÉ, pas écrit ; le contraste sur le fond lu sur
> l'image ; 33 ; 29/33 sur v151).
> **L'échelle de v151 vaut, sauf la ligne « texte » : « [Prénom], donc. » (sans « Enchanté. »).**
> **⚑ C-161 — `redteam_peaufiner` intermittent sur v151 : EXPLIQUÉ PAR LA CHARGE.** Le diff v150 → v151 ne touche pas Peaufiner ; rejoué sous la même
> charge, v152 7/7 verts (charge 6 à 18) et v150 3/3 en alternance ; les trois rouges de v151 étaient trois délais différents, sous une charge de 34 à 83.
> Pas jugé au calme (la charge n'est jamais descendue sous 4 pendant ce lot).
> **⚑ LA SÉRIE DE v152 — NON JUGÉE AU CALME** : le Mac a redémarré pendant le lot et l'autre session (émulateur Android, simulateur iOS) a tenu la charge
> entre 6 et 700. Passés un à un : les juges des chantiers touchés et les sentinelles (19 + `redteam_guide` deux fois + `redteam_peaufiner` six fois) — verts,
> sauf `redteam_onboarding_texte` C-123 (une durée, non jugée) et `redteam_guide` 10.2 (les lobes de la zone du +, 7,8–8,0 % pour 8 %, sur v151 aussi :
> C-163, ouvert). Les 127 autres juges : **NON JUGÉ**, ligne par ligne dans `scratchpad/v152/serie-complete.txt`. **`redteam_air` : non jugé, pas refigé.**
> **Contrat de test remis au niveau** (original : `sauvegardes/redteam_guide-avant-v152.py`) : `redteam_guide` — « en sombre, la crème pour toute la
> phrase » devient la règle de C-162 (texte crème ; « commence » et Promi `#82AEF8`, Chiche `#FFB8D2`, Cercle `#C9A8F5`, en dur) ; rouge sur v151.
> **Archive : `sauvegardes/app-cloture-v152.html`.**

### ⚑ v151 (18 oct. 2026) — RETOURS iPHONE DE TOM SUR v150, PUIS CLÔTURE DE LA SÉRIE : LA VAGUE REVIENT AU VIOLET, L'ÉCHÉANCE EST UNE DATE, LE LIBELLÉ DU DÉPART EN ORANGE, « GARDER DE CÔTÉ » À 718, L'ONBOARDING EN SOMBRE, LE REJEU DE L'ONBOARDING. (Décisions Tom.) Ce bloc CORRIGE v150 (C-154 la couleur, C-149 la cote, §0 « le prototype ne recompte pas les jours ») et v146/v148 (la règle de l'orange).
> **Validés par Tom : C-158 (les phrases des pages + du Chiche et du Cercle, les 17 pt du Cercle compris), C-126 (la flèche orange en sombre), la fin de
> l'onboarding (deux lignes alignées à droite). Q545 : oui, « trace ta moitié » suit « trace pour planter ». Q546 : oui, deux lignes alignées à droite.**
> **⚑ C-154 — LA VAGUE DE CRÉATION REVIENT AU VIOLET `#291547`** : une parole créée est « en cours » (l'orange de v150 reposait sur une prémisse fausse).
> **⚑ C-160 (Q544) — L'ÉCHÉANCE EST UNE DATE, COMPARÉE À AUJOURD'HUI** (`lot-V151-ECHEANCE`, `window._echeance`) : `p.ech = {iso:'AAAA-MM-JJ', due}` ;
> `p.due` (les jours qui restent, lu par tous les écrans) n'en est plus que la conséquence, recomptée au lancement et à chaque retour au premier plan
> (`visibilitychange`, `pageshow`) ; une parole « en cours » dont l'échéance est passée passe « à tenir » (`echeancesDepassees`, qui recompte d'abord).
> Les écrivains d'échéance (page +, Peaufiner, REPORTER) n'ont pas été réécrits : ils écrivent toujours `due` en jours depuis aujourd'hui, et la date se
> pose à l'enregistrement (`saveState` enveloppé) dès que `due` diffère de `p.ech.due` ; une date choisie au calendrier (`dueISO`) EST l'échéance.
> **REPORTER depuis une échéance passée compte depuis aujourd'hui** (« +3 j » = dans trois jours) **et la parole redevient « en cours »** (`_fpost`
> enveloppé, la carte de la Toile `#ccPushOpts` aussi). **`?jour=+N`** avance aujourd'hui de N jours pour la page, jamais mémorisé. Une parole sans date
> (« un jour », « en l'air ») ne passe jamais « à tenir ». Juge : **`redteam_echeance.py`** (11 ; 4/11 sur v150). Swift : une `Date` (portage/SPEC-DONNEES §1.12).
> ⚠ La vérification de version (v145) recharge, au retour au premier plan, une page dont le commit diffère du serveur (arbre de travail modifié pendant
> un lot) : sa requête annulée remonte comme une « erreur de page » en WebKit — ce n'est pas une faute de la page (les juges l'écartent nommément).
> **⚑ C-157 — LE MOT DU TRAIT DES PAGES + EN ORANGE `#FB4C0D`** (« trace pour planter », « trace ta moitié », « trace pour lancer » ; le Cercle porte le
> même texte : même traitement), clair et sombre, au repos comme pendant le geste (le terracotta du doigt posé est retiré : un seul orange). **Les fiches
> ne bougent pas** (`#dptTrace`). ⚠ **Mesuré, par décision : 1,23:1 sur le corps du Promi `#0E78F2`, 2,27:1 sur ceux du Chiche et du Cercle** (Q547).
> **⚑ LA RÈGLE DE L'ORANGE, ÉTENDUE (Tom, v151) : `#FB4C0D` (`--c-orange-depart`) marque LE DÉPART D'UNE ACTION ET SON LIBELLÉ, et rien d'autre** —
> le signe + de l'accueil, le + qui valide un nom, le départ de la flèche du trait (fiches, pages +, onboarding), et le libellé « trace pour … » des
> pages + ; la même valeur reste celle de « Ma Parole ! » dans les murs (deux jetons, deux rôles). Juges : `redteam_maparole` (le libellé admis),
> `redteam_couleurs_ref` E20, `redteam_pages_plus`.
> **⚑ C-149 — « GARDER DE CÔTÉ » À 718 pt** (712 + 6) dans les trois pages + ; l'inclinaison ne change pas ; son encre finit à 22,6 pt de la barre du bas et
> 22,1 pt du bord droit ; **le rail du pinceau ne bouge toujours pas** (compensation −10).
> **⚑ C-126 §5 — EN SOMBRE, « TRACE POUR PLANTER » (onboarding) EST CRÈME `#F7F0DE`** : mesuré 17,5:1 sur son fond réel `#0B0908` — **c'était déjà le cas
> en v150, en WebKit comme en Chromium** (`--onb-ink`) : rien n'a été changé ; le clair garde `#00341A`. Si Tom le voit vert sur l'iPhone, une capture.
> **⚑ C-124 §6 — EN SOMBRE, PRIMO, DEUXIO, TERTIO DANS LE BLEU DU CLAIR `#0E78F2`** (4,7:1 sur le fond réel : le bleu Promi n'était pas nécessaire) ;
> « La suite t'appartient. », nommé à part, garde la crème (Q548). **§7 — « La suite t'appartient. » 9 pt plus bas** (18 pt au-dessus d'elle en tout,
> `calc(9px*var(--onbe) + 9px)`), toujours centrée ; l'air jusqu'aux dalles reste large (123,5 pt mesuré).
> **⚑ C-159 — REJOUER L'ONBOARDING : LE TEXTE S'ADAPTE.** Dès que la Toile compte au moins une dalle avant cette plantation (une parole non gardée de
> côté, ou un Cercle nommé : `sync` plante une dalle par Cercle), « Ton premier Promi, ta première dalle sur ta Toile. Plus qu'à le tenir. » devient,
> mot pour mot : **« Une nouvelle dalle sur ta Toile, félicitations. Plus qu'à le tenir. »** (le titre « PROMI planté ! » ne change pas, ni la chorégraphie).
> Au premier lancement la Toile est vidée (`obResetData`) : le texte d'origine. Les autres mentions de « premier / première » de l'onboarding : aucune
> (cette phrase porte les deux). **Exception NOMMÉE à R1 (ENGAGEMENT) : « félicitations », dans cette phrase de Tom et aucune autre** (`BLANCHE_R1`).
> Juge : **`redteam_onb_rejeu.py`** (10 ; 8/10 sur v150 : B et C rouges).
> **⚑ LES EXCEPTIONS NOMMÉES AU « ! » — LA LISTE COMPLÈTE, INCHANGÉE : « Ma Parole ! » (v106), « Promi planté ! » (v146), « Parole tenue ! » et « Défi
> relevé ! » (v148, C-144).** Espace insécable avant « ! ». Partout ailleurs, pas de « ! » (la phrase du rejeu n'en porte pas).
> **⚑ L'ÉCHELLE TYPOGRAPHIQUE DE L'ONBOARDING ET DU GUIDE — L'ÉTAT DE v151** (v148 + v149 + v150 + v151 ; `--ech-*`) — un RÔLE = une taille :
> ```
> titre         PromiLate 52 pt — « PROMI » de « Promi planté ! » (#82AEF8 en sombre) ; sa suite « planté ! » 42 pt
> phrase        Gilbert 35 pt / 66 — la phrase de promesse (« Toi, c'est … ? », « Je me promets de … »)
> texte         Atkinson 500, 25 pt / 30 — « [Prénom], donc. Enchanté. », « Quid… », « Petite ou grande promesse, elle compte. »
> liste         Atkinson 500, 22,3 pt / 26 — « Ton premier Promi… » (au rejeu : « Une nouvelle dalle… »), Primo, Deuxio, Tertio,
>               « Tout le monde promet. Toi, tu tiens parole. » (alignée à droite, deux lignes égales)
> natures       Atkinson 700 — Promi, Chiche, Cercle : sombre #82AEF8 · #FFB8D2 · #C9A8F5 ; clair #4870B5 · #9D5E77 · #8262A9 (3:1 sur #DFCAA4)
> mot-clé       PromiLate 25 pt — Primo, Deuxio (penché 3°), Tertio : #0E78F2 dans les deux thèmes (v151)
> mot de fin    PromiLate 32 pt — « La suite t'appartient. », centrée, 18 pt au-dessus d'elle (9 v148 + 9 v151) ; cobalt en clair, crème en sombre
> consigne      PromiLate 19 pt — « trace pour planter » : #00341A en clair, crème en sombre
> guide         Atkinson 700, 29 pt / 42 — les deux phrases du guide ; leurs mots-clés (« monde », « commence ») en PromiLate 29 pt
> guide-studio  PromiLate 32,2 pt — « Studio » (× 1,11, v149), lettre à lettre aux tons d'Ingénu
> ```
> Juge : `redteam_echelle_onboarding`. Couleurs et cotes de v151 : `redteam_onb_mots` (52 ; §6 et §7 rouges sur v150).
> **⚑ LA SÉRIE COMPLÈTE DE CLÔTURE (18–19 oct., 20 h 31 → 3 h 11, 145 juges, un à la fois, `scratchpad/v151/serie.txt`)** : **115 verts, 30 rouges, tous
> classés.** ① Rejoués seuls : verts sur v151 ou même rouge sur v150 — `ajout_personne` D, `clair_sombre` B (le témoin clair/clair diffère aussi),
> `deplace` (Bobinette), `origine`, `part`, `partage_toile`, `ritournelle` F, `validation` C : la charge (5 à 184, la session ENTRE). ② Des durées sous une
> charge ≥ 4, **NON JUGÉES** (C-137) : `aura_latence`, `evol`, `fluide` (C-102), `pelote_doigt`, `rythme`, `souffle`, `tenir` G ; `guide` : un tirage de
> flaques trop rond (lobes 7,8 % pour 8 %), pris à ce passage. ③ Connus ou par décision, comme en v148 : `contraste_trait` (Q514, Q528 ; 98/248 verts,
> 20 en v148), `dessin` I, `dessin_photo` 7, `kaki` (C-017), `nuit` (Zzz coupé), `photo`, `ramage_onde` (C-009), `vivant` (Tesselle), `releve-S1`/`S4`/`S5`/
> `moodboard` (S4 : 39 écarts, 45 en v148). ④ **Non attribué : `redteam_peaufiner`, 3 rouges sur 8 en v151, 0 sur 6 en v150 (C-161, ouvert).**
> **`redteam_air` : NON JUGÉ, PAS REFIGÉ** — il a tourné sous une charge de 10,8 → 6,3 ; 64 paires de la référence toujours non retrouvées (les mêmes qu'en
> v149 : « garder de côté » à droite, C-151, les dates), aucune paire resserrée sur ses écrans. `banc_rendu` : au pixel.
> **Archive avant Swift : `sauvegardes/app-cloture-v151.html`** (l'app à la clôture de la série ; son moteur est celui du commit).
> **Contrats de test remis au niveau** (originaux : `sauvegardes/*-avant-v151.py`) : `redteam_ruban` (B : `#291547`), `redteam_garder` (J : 718),
> `redteam_pages_plus` (C-149 : 10 pt sous v149 ; C-157 : l'orange ; il rouvre les deux pages jusqu'à deux compositions comparables — le hasard semé ne
> suffisait pas), `redteam_onb_mots` (§5, §6, §7), `redteam_couleurs_ref` (E20), `redteam_maparole` (le libellé du départ), `redteam_engagement` (R1 : la
> phrase de Tom).

### ⚑ v150 (18 oct. 2026) — PETIT LOT : LA VAGUE DE CRÉATION EN ORANGE, LE MOT DU TRAIT DES PAGES +, « GARDER DE CÔTÉ » 4 pt PLUS BAS, LA PHRASE DU CHICHE ET DU CERCLE, LA FIN DE L'ONBOARDING, LA FLÈCHE SOMBRE. (Décisions Tom.) Ce bloc CORRIGE v149 (C-154 la couleur, C-149 la cote, C-124 la phrase de fin) et v147 (C-126 en sombre).
> **Validés par Tom : C-153, C-145, C-155, C-156 ; C-154 sauf la couleur ; le reste de l'onboarding. Q537, Q538, Q541, Q543 : appliquées telles quelles
> (pas de mot-marque sur « Promi planté ! » ni au compte ; les trois couleurs du clair ; 520 + 320 ms ; rien de changé au contraste).**
> **⚑ « EN COURS » ET « À TENIR », CE QUE FAIT LE CODE (réponse à Tom, rien n'est changé)** : toute parole plantée entre `status:'encours'` ; elle passe
> SEULE à `'rate'` (« à tenir ») quand son échéance est dépassée (`due < 0`), au lancement de l'app (`echeancesDepassees`, 3,4 s) ; REPORTER (le Fil)
> la remet en cours ; tenir la fait tenue ; le sélecteur d'état de la fiche est caché (0 × 0). ⚠ **Le prototype ne recompte pas les jours** (`due` reste
> celui de la plantation) : hors jeu de démonstration, une parole n'y devient jamais « à tenir » — à porter dans Swift (une date, pas un compte).
> **⚑ C-154 — LA VAGUE DE CRÉATION (le ruban de la page +) PREND L'ORANGE DE « À TENIR », `#DD4D23`** (Tom : « une parole créée passe à tenir ») ;
> jamais l'orange d'action `#FB4C0D`. La fiche garde l'amande. Juge : `redteam_ruban` B.
> **⚑ C-157 — PAGES + SEULEMENT : le mot du trait de la page + d'un Promi (« trace pour planter », « trace ta moitié ») et d'un Chiche (« trace pour
> lancer ») descend de 7,5 pt et va 3 pt à droite** (aligné sur la queue de la flèche, sans la toucher) ; le Cercle ne bouge pas ; **les fiches sont
> identiques au pixel à v149**. Juge : **`redteam_pages_plus.py`** (v149 servie à côté, hasard semé).
> **⚑ C-149 — « GARDER DE CÔTÉ » À 712 pt (708 + 4)** dans les trois pages + ; l'inclinaison (5,5°) est validée.
> **⚑ C-158 — LA PHRASE DE LA PAGE + D'UN CHICHE REMONTE DE 10 pt ; CELLE D'UN CERCLE SE POSE EXACTEMENT SUR ELLE** (l'encre de la première ligne à
> la même hauteur, même boîte : −41 pt — un Cercle a par défaut une ligne de moins, ses cotes sont 32 pt plus bas). **Le rail du pinceau ne bouge pas** :
> il se place comme si ni la phrase (`_ppDyPhrase`) ni « garder de côté » (−4) n'avaient bougé.
> **⚑ LA BASCULE DES LIGNES (trouvée en composant la capture, corrigée)** : la taille de la phrase dépend du nombre de lignes (34 à quatre, 30 à cinq) et
> le nombre de lignes de la taille ; pour certaines phrases tirées (« faire le Mont Blanc »), 34 donne cinq lignes et 30 en donne quatre — la passe
> recommencée basculait encore, et le mot du trait restait à la cote de l'autre composition, sur les points (v149 : 1 ouverture sur 8 ; v150 avant
> correction : 3 sur 8). Une troisième passe garde la taille et repose tout (`cotes.__fige`). *La règle* : **une mise en page qui dépend d'un résultat
> qui dépend d'elle se FIGE à la deuxième bascule, elle ne recommence pas.** Juge : `redteam_pages_plus` (dix ouvertures).
> **⚑ C-124 — « Tout le monde promet. Toi, tu tiens parole. »**, alignée à DROITE, en deux lignes égales (`text-wrap:balance` : « … promet. / Toi, tu
> tiens parole. ») ; **« La suite t'appartient. » CENTRÉE**. Juge : `redteam_onb_mots`.
> **⚑ C-126 — EN SOMBRE AUSSI, TOUTE LA FLÈCHE DU PREMIER PROMI (la traîne, l'amorce, la part tracée) EN `#FB4C0D`** ; les points non tracés gardent la
> couleur du mode. Juge : `redteam_onboarding_texte` (aucun pixel crème au départ du trait, en sombre).
> ⚠ **`redteam_air` n'est pas refigé** (série complète au prochain lot, v151) : l'air est intact sauf 16 paires resserrées, toutes demandées — le mot du
> trait vers la phrase (Promi 58 → 50,5 ; Chiche 59 → 41,5 ; **Cercle 58 → 17 pt**) et « garder de côté » vers la barre (58,8 → 54,8) ; 64 paires de v149
> toujours non retrouvées (C-149 à droite, C-151, dates). Sous la charge du Mac (17 à 1 019, la session ENTRE) : `redteam_couleurs_ref` (1 écart sur
> « l'instant après », identique sur v149 au banc direct), `redteam_decisions` (le champ du Cercle, 102/102 rejoué seul) et `redteam_joignable` (le
> Cercle défilé, comme en v149) ont rougi une fois.
> **Contrats de test remis au niveau** (originaux : `sauvegardes/*-avant-v150.py`) : `redteam_ruban` (B : `#DD4D23`), `redteam_garder` (J : 712),
> `redteam_onb_mots`, `redteam_onboarding_texte`, `redteam_onboarding`, `redteam_onb_sorties` (la phrase de fin), `redteam_validation` (la durée du
> haut du ruban jugée au calme seulement).

### ⚑ v149 (18 oct. 2026) — RETOURS iPHONE DE TOM SUR v148 : LE I QUI CLIGNOTE DANS L'ONBOARDING, LES NATURES EN GRAS, « TOUT LE MONDE PROMET. TOI, TU TIENS. », LES PHRASES DU GUIDE PLUS HAUT, LA VAGUE DE CRÉATION À LA COULEUR DE L'ÉTAT, L'ANIMATION DANS L'IMAGE QUI SUIT LE LEVER, LA VALIDATION À PLUSIEURS, « GARDER DE CÔTÉ » À DROITE. (Décisions Tom.) Ce bloc CORRIGE v148 (C-149 « garder de côté », C-145 la place des phrases, C-148 le ruban à la validation, C-124 les natures) et v147 (C-118 le départ du rideau).
> **Validés par Tom : C-141, C-143, C-144, C-146, C-147, C-148. C-139 clos sans invitation animée (le chevron orange suffit). Tranchées : Q513 (le trait du Chiche
> et du Cercle à 2,5:1, fonds inchangés — `redteam_contraste_trait`, `SEUIL_NAT`), Q533 (en clair, les lettres de « Studio » à la teinte d'Ingénu assombrie
> jusqu'à 3:1), Q536 (plus de flou ni de fondu en bas de fiche pendant le tracé).**
> **⚑ C-153 — LE I DE PROMI CLIGNOTE DANS L'ONBOARDING** : même animation, même code, même bleu que le I de l'accueil (`promiBlink 1.15s steps(1,end)`), sur
> chaque page qui porte le mot-marque en haut à gauche (prénom, parole, trait). « Promi planté ! » et le compte n'en portent pas (le titre PROMI, v146) — Q537.
> **⚑ C-124 — PROMI, CHICHE, CERCLE DANS L'ONBOARDING : EN GRAS PARTOUT (Atkinson 700) ; en sombre EXACTEMENT `#82AEF8` · `#FFB8D2` · `#C9A8F5` ; en clair la
> teinte foncée jusqu'à 3:1 sur `#DFCAA4` : `#4870B5` (3,08) · `#9D5E77` (3,05) · `#8262A9` (3,07)** (`natCol`, `_teinte.ajuste`). **« Le reste se découvre
> en traçant. » devient « Tout le monde promet. Toi, tu tiens. »**, mot pour mot, même place, rôle « liste » (22,3 pt), tracé. Juge : **`redteam_onb_mots.py`**
> (44 ; 15/42 sur v148).
> **⚑ C-145 — LES DEUX PHRASES DU GUIDE REMONTENT ENCORE DE 60 pt (centre 312 → 252, ± 4) ; « Studio » × 1,11 (29 → 32,2 pt, rôle « guide-studio » de
> l'échelle), couleurs inchangées ; aucune ne recouvre une dalle colorée, une icône ni la zone nette** — mesuré ligne de texte par ligne sur le vrai premier
> lancement (la dalle de la première parole est à 369–519 pt ; en v148 la phrase descendait à ≈ 397 et la touchait). Juges : `redteam_guide` (centre ± 4,
> Studio, recouvrement), `redteam_onb_mots` (le recouvrement en sombre), `redteam_echelle_onboarding`.
> **⚑ C-154 — LA VAGUE DE CRÉATION (le ruban de la page +) PREND LA COULEUR DE L'ÉTAT OÙ ENTRE LA PAROLE : « en cours », `#291547`** (toute parole plantée
> entre « en cours » ; `ETAT_COL` du ruban). **L'amande ne peint que la célébration** (la fiche). Juge : `redteam_ruban` B.
> **⚑ C-155 — LE LEVER DU DOIGT : L'ANIMATION PART DANS L'IMAGE SUIVANTE. *Les causes, mesurées en WebKit* : ① la plantation attendait 440 ms une
> « signature » (deux ombres) avant de grandir — retirée : la dalle grandit dès l'image suivante, LINÉAIRE (320 ms) ; ② le lever recomposait la page + qui
> s'en va (`_ppTout`, 26 à 28 ms) et le clic la recomposait encore 60 ms après (`arme` → `tout`, 32 ms) — plus rien ne la recompose pendant `_tirageActive` ;
> ③ le rideau naissait dans le rappel d'image de l'instant, après lui et deux images longues (premier mouvement ≈ 110 ms après le lever) — il démarre AU LEVER
> (`_maree.tot()`, appelé par le clic « tenue »), son horloge avec lui, la phrase s'écrit dans la nappe quand l'instant l'a posée (`phrase()`).** Mesuré : le
> gestionnaire du lever de la page + 31 → 4 ms ; première image 33 → 6 ms ; la Toile reçoit la parole après le départ (+346 ms). *La règle* : **au lever, on
> part ; ce qui recompose ce qui s'en va ne tourne plus.**
> **⚑ C-156 — LA VALIDATION** : ① tenue d'un coup (seul ou la dernière part) : **le rideau part du BORD BAS DU RUBAN tel qu'il est peint au lever**
> (`_ruban.bas()` → `N.S`) — le ruban et le rideau sont une seule matière ; chaque colonne descend à vitesse constante jusqu'au front validé ; le haut du
> ruban redescend sur le trait À LA VITESSE DU RIDEAU (≈ 75–100 ms), puis le ruban s'en va sous lui. *La cause de la « vague intermédiaire »* : le rideau
> partait sous le ruban (51 pt) et n'en sortait qu'après ≈ 80 ms, pendant que le haut du ruban redescendait seul. ② ma part, sans être la dernière : seulement
> la vague amande sous le trait (`PART_TIENT` 520 ms, puis elle se resserre en 320 ms à vitesse constante), aucun rideau, la fiche reste « en cours ».
> ③ tout le monde a tracé : une entrée dans le Fil, « Chacun a tracé sa part : « … » » (Q539). ④ **`p.vuTenue = {nom: date ISO}`** (`lot-V149-VALIDATION`,
> `window._vuTenue`) : posé pour celui qui trace la dernière part ; à la PREMIÈRE ouverture de chacun des autres, le rideau descend sous ses yeux
> (`_maree.revoir`), puis sa clé est écrite ; ensuite la fiche s'ouvre directement tenue (portage/SPEC-DONNEES §1.11). Juge : **`redteam_validation.py`**
> (25 ; 8/25 sur v148).
> **⚑ C-149 — « GARDER DE CÔTÉ » : À DROITE (son bord droit à 24 pt, cote 708), JAMAIS SOULIGNÉ, PENCHÉ DE 5,5° (skewX, comme « Deuxio »), visible aussi
> pendant le tracé ; caché seulement quand un choix de la phrase est ouvert (la liste des personnes le recouvrirait — Q540).** Actif / inactif : v148.
> Juge : `redteam_garder` J, K (48 ; 39/48 sur v148).
> **⚑ C-150, C-151, C-152 (trouvés par la série de v148)** : C-150 était le juge (un `closeAll` refusé dans les 4 s d'un geste dans Peaufiner, C-134 :
> `_peaufSortie()` d'abord) ; **C-151 : les titres de deux lignes des cartes de l'Index rétrécissent jusqu'à tenir au-dessus de l'état** (`_s4TitresAjuste`,
> le plus petit pas qui tient, la taille décidée de 24 pt comme départ) — juge **`redteam_titres_cartes.py`** (10 ; 6/10 sur v148) ; C-152 était le juge
> (`redteam_menu_plus` touchait la pilule avant qu'elle soit posée).
> **⚑ TROUVÉ PAR LA SÉRIE ET EN REGARDANT, CORRIGÉ** : ① **Q536 n'était réglé qu'à moitié** — la règle d'août `#detailPoster.tracant` floute CINQ nœuds
> (`#dpTrameCv`, `#dpTete`, `#dAura`, `#dpPromiBody`, `#dpDetails`) ; la sonde, en Chromium, n'en avait vu que deux : la phrase et le titre restaient flous
> au doigt posé en WebKit. Les cinq sont rendus nets (`redteam_validation` Q). ② **`#instTenue` n'existe pas encore au lever** (l'instant le crée une image
> plus tard) : la nappe partie au lever ne le trouvait jamais et la phrase de validation manquait — elle le cherche à chaque image tant qu'il manque
> (`redteam_tenir` H). ③ **un drapeau trop large** : sauter la recomposition de la page + tant que `_tirageActive` (levé 1,5 s) laissait une page +
> rouverte juste après une plantation sans sa mise en page (`redteam_part` C, D) — un drapeau étroit, `_ppPart`, levé au départ, baissé à la coupe.
> ④ **une transition CSS commence à son point de départ** : la première image après le lever montrait la dalle à l'échelle 1 — la transition part une
> image en avance (délai −17 ms). ⑤ **à mi-descente le front gardait la forme de l'onde** (11 pt d'écart) : il s'aplanit dans le premier quart vers une
> ligne partie du point le plus bas du ruban (chaque colonne ne fait que descendre). ⑥ `redteam_contraste_trait` lisait la nature de la page + comme « ? »
> (seuil 3 au lieu de 2,5). *La règle* : **un état « pendant le geste » se regarde au doigt posé, en WebKit — pas sur une sonde Chromium au repos.**
> ⚠ **`redteam_air` n'est PAS refigé** (la règle : série complète avant tout refigeage) : l'air est intact sur 774 paires ; 64 paires ne sont plus
> retrouvées, toutes nées des décisions (« garder de côté » à droite : 32 ; titres des cartes, C-151 : 24) et des dates du Peaufiner (8, C-018).
> ⚠ **Le Mac a tourné à une charge de 8 à 720 tout le lot** (la session ENTRE : émulateur, simulateur, `parcours`) : aucune cadence jugée ;
> `redteam_flash` B1/B2, `redteam_trait` « tenir rapide », `redteam_joignable` (Cercle défilé) rougissent par moments sous cette charge — v148 aussi,
> à la même charge ; à rejouer au calme.
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v149.py`) : `redteam_guide` (centre 252 ± 4, Studio, Q533,
> le recouvrement ; les zones de netteté évitent la nouvelle place de la phrase), `redteam_ruban` (B : `#291547` à la page +), `redteam_garder` (G sans
> soulignement, J, K), `redteam_tenir` (G : le départ se lit au bord bas du ruban), `redteam_echelle_onboarding` (« guide-studio »), `redteam_onboarding_texte`, `redteam_onb_sorties`, `redteam_onboarding` (la phrase
> de fin), `redteam_contraste_trait` (Q513), `redteam_cercle_couleur` (C-150), `redteam_menu_plus` (C-152).

### ⚑ v148 (16 oct. 2026) — CLÔTURE DE LA SÉRIE : LES RONDS ORANGE RETIRÉS, LA PHRASE DE VALIDATION AU « ! », LE RIDEAU À VITESSE CONSTANTE, LE RUBAN AMANDE, LES CARTES EN CONSTRUCTION DE FICHE, « GARDER DE CÔTÉ », « PROMI PLANTÉ ! » PAS À PAS, LES TRANSITIONS EN FLAQUES, LES PHRASES DU GUIDE, L'ORDRE DU GUIDE. (Décisions Tom.) Ce bloc CORRIGE v147 (l'échelle, C-141 « cellule par cellule », le guide « toucher ailleurs fait avancer », C-118 l'épaississement), v146 (« Promi planté ! » et le reste au toucher, la marée) et v144 (le guide).
> **Validés par Tom : C-088 (Ritournelle), C-094 (le guide en flaques, « flou ok »), C-116 (les commentaires), C-129 (pas d'emoji), C-135 (la Pelote tout de
> suite), C-142 (le menu du +, « parfait » : on fige) ; et, dans l'onboarding, le flou et l'arrivée douce des encarts à leur place (« top de top, on garde ») :
> ON N'Y TOUCHE PLUS.**
> **⚑ EXCEPTIONS NOMMÉES AU « ! » — LA LISTE COMPLÈTE : « Ma Parole ! » (v106), « Promi planté ! » (v146), « Parole tenue ! » et « Défi relevé ! » (v148,
> C-144 : les phrases de validation de « tenir »).** Espace insécable avant « ! ». Partout ailleurs, pas de « ! ».
> **⚑ C-143 — LES DEUX RONDS ORANGE DE SIGNATURE SONT RETIRÉS PARTOUT** (fiche, page +, trois natures, deux thèmes). *La cause* : le canevas du geste
> (`#tenirCv`, `#planterCv`) peignait encore les deux points de guidage du geste d'origine ; sur la fiche une règle le posait à `opacity:0 !important` — mais
> **dans WebKit l'animation `tenirPouls` l'emporte sur ce `!important`** : sur l'iPhone les ronds pulsaient, Chromium ne les montrait pas. Les peintres ne les
> peignent plus, l'animation est coupée. Le chevron orange du départ (C-133) reste. Juge : **`redteam_ronds.py`** (WebKit ; rouge sur v147).
> *La règle* : **un `!important` ne bat pas une animation CSS dans WebKit — on retire la cause (le dessin), jamais on ne la cache.**
> **⚑ C-139 — AUCUNE INVITATION ANIMÉE DANS L'APP tant que Tom n'a pas choisi** (le chevron suffit). `promi-invite-variantes.html` ne montre plus que
> l'invitation (la fiche du cadre ne reçoit plus le doigt : Tom voyait la validation) : **A, les POINTS du chemin s'allument ; B, la FLÈCHE avance et trace
> devant elle** (44 pt). `redteam_ronds` E : la bande du trait ne bouge pas au repos (7 s).
> **⚑ C-144 — LA PHRASE DE VALIDATION** : centrée sur sa ligne ; « Parole tenue ! », « Défi relevé ! » (`TEXTES_ENGAGEMENT.tenir`) ; la nappe la porte au milieu.
> **⚑ C-118 — LE RIDEAU DESCEND À VITESSE CONSTANTE.** *La cause* : deux mouvements bout à bout — le trait s'épaississait (12 → 46 pt en 160 ms), puis le
> rideau partait en ease-in-out et restait caché sous le trait épaissi jusqu'à ≈ 300 ms (« il s'arrête puis repart ») ; et l'horloge partait à la pose
> d'un canevas de 1170 × 2532 alloué dans la même image (le premier pas sautait). *Aujourd'hui* : un seul mouvement, le front part du bas du trait dès la
> première image, vitesse constante jusqu'à la barre (700 ms), canevas alloué à l'avance, horloge à la première image peinte ; la remontée ne change pas.
> Juge : `redteam_tenir` G, H (régularité image par image ; jugée au calme seulement, C-137).
> **⚑ C-148 — LE RUBAN AMANDE** (`lot-V148-RUBAN`) : plus de rectangle (le fond de la zone du geste est transparent, A2) ; un ruban PLEIN `#8FE08F` qui suit
> l'onde du trait, 94 pt d'épaisseur (80 % des 118 d'avant), bords légèrement irréguliers (0,4 à 3,5 pt) ; il naît en 200 ms et se retire en 240 ms ; le mot
> du trait n'est jamais coupé en deux. Juge : **`redteam_ruban.py`** (WebKit ; rouge sur v147).
> **⚑ C-147 — LES CARTES DE L'INDEX, DU FIL ET DU FIL D'UN CERCLE SONT CONSTRUITES COMME LA FICHE, DANS LES DEUX THÈMES** : corps `#0E78F2` · `#7C3F58` ·
> `#5D4978`, la terre `#2B1020` d'une tenue, l'état crème (« TENUE » en amande). Dans `lot-S4` : `light()` rend toujours faux pour une carte ; le résolveur
> d'état de la fiche répond « sombre » pour une fausse fiche (`__carte`). ⚠ **Le trait d'une carte tient donc les mêmes contrastes que la fiche : Chiche et
> Cercle IMPOSSIBLES à 3:1 face aux deux fonds (Q513), l'orange « à tenir » à 1,03 sur le cobalt (Q514), la crête d'une tenue sur la terre à 1,68 (Q528)** —
> `redteam_contraste_trait` est rouge PAR DÉCISION À PRENDRE.
> **⚑ C-149 — LA PAGE +** : les phrases « se retourne » sont retirées partout (« Un Chiche se lance, il ne se retourne pas » et l'aide du sens) ; « Garder de
> côté » est visible, ACTIF seulement quand la page a changé depuis son ouverture (une personne ajoutée, une modification — `window._garderEtat`, la page se
> signe à l'ouverture) ; inactif : non souligné, sa teinte rapprochée du corps (30 %, sans transparence), il ne fait rien. Juge : `redteam_garder` E–I.
> **⚑ C-124 — LA PAGE DU PREMIER PROMI ET « PROMI PLANTÉ ! »** : l'Atkinson de l'onboarding −7 % (texte 27 → 25 pt, liste 24 → 22,3) ; « Promi planté ! »
> PAS À PAS (`finPas`, `window._onbFinPas`) — au départ le titre SEUL, la parole et ses voisines plus haut (centre 647 pt, comme v146) ; chaque toucher : le
> texte remonte et les dalles descendent du même mouvement (la loi de la vue, 133 ms), puis le paragraphe suivant se trace dans la place faite —
> « Ton premier Promi… plus qu'à le tenir. » (à la taille des suivants), Primo · Deuxio · Tertio, puis « Le reste se découvre en traçant. » et « La suite
> t'appartient. » (9 pt plus bas) ; 22 pt d'air entre le texte et les dalles à chaque pas ; les dalles finissent à 722 pt (738 en v147, −16) ; un quatrième
> toucher mène au compte. ⚠ **Un juge qui traverse l'onboarding touche quatre fois** (`data-onb-reste` = 1, 2, 3 puis « fini »).
> **⚑ C-141 — LES TRANSITIONS DE L'ONBOARDING SONT EN FLAQUES** (`window._passageFlaques` : le moteur du guide, `Flaques.Scene` — 12 à 20 germes, naissances
> étalées, ponts ; mode « ouvre » : une couverture se troue en flaques ; « couvre » : la page suivante naît en flaques par-dessus). **Plus de balayage, plus
> de fondu, plus de glissement, rien d'un coup** : ① l'arrivée sur le prénom : le voile s'ouvre en flaques (1,1 s ; v147 : cellule par cellule) ; ② le trait
> du premier Promi naît en flaques à la première lettre (700 ms) ; ③ la page du trait est recouverte en flaques par la Toile d'avant (620 ms ; v147 : un
> fondu) ; ④ « Promi planté ! » est recouvert en flaques (650 ms ; v147 : un BALAYAGE de droite à gauche) pendant que le panneau du compte naît en flaques
> à sa place (800 ms ; v147 : il glissait du bas) ; ⑤ le panneau du compte est recouvert en flaques (500 ms), puis l'écran entier s'ouvre en flaques sur
> l'accueil (900 ms), les voisines parties et la vue recadrée SOUS la couverture ; ⑥ l'arrivée douce des encarts : inchangée (validée). Juge :
> **`redteam_transitions_onb.py` réécrit** (image par image, le passage rejoué : ≥ 3 trous séparés à 8–45 % ouverts ; rouge sur v147).
> **⚑ C-145 — LES PHRASES DU GUIDE** : en GRAS (Atkinson 700), 29 pt (27 × 1,07), interligne 1,45 (42 pt), mots-clés PromiLate 29 ; « monde » `#8363AA` en
> clair, `#C9A8F5` en sombre (le rose de v147 ne se lisait pas — Q518) ; aucun contour ; tracées (les chemins médians de l'Atkinson 500 couvrent le gras :
> vu à l'image, deux thèmes).
> **⚑ C-146 — L'ORDRE DU GUIDE** : au lancement, le flou du Studio ; **tant que le Studio n'a jamais été ouvert, toucher ailleurs montre le RAPPEL — la phrase
> du Studio, écrite de nouveau, mot pour mot — et seulement lui, autant de fois qu'on touche** ; jamais l'étape ni la phrase du + avant le Studio (v144 : toucher
> ailleurs y menait) ; le Studio ouvert puis refermé, avec ou sans changement → le flou et l'invitation vers le +. **L'app quittée à l'étape du Studio : le
> guide reprend au lancement suivant** (`promi_guide` = « studio » ; « 1 » dès que le Studio est ouvert). Juge : **`redteam_ordre_guide.py`** (rouge sur v147).
> **⚑ L'ÉCHELLE (C-138) — CE BLOC REMPLACE CELLE DE v147** (`lot-V147-ECHELLE-css`, variables `--ech-*`) — un RÔLE = une taille, sur toutes les pages :
> ```
> titre        PromiLate 52 pt — « PROMI » de « Promi planté ! » ; sa suite « planté ! » 42 pt
> phrase       Gilbert 35 pt / 66 — la phrase de promesse (« Toi, c'est … ? », « Je me promets de … »)
> texte        Atkinson 500, 25 pt / 30 — « [Prénom], donc. Enchanté. », « Quid… », « Petite ou grande promesse, elle compte. »
> liste        Atkinson 500, 22,3 pt / 26 — « Ton premier Promi… », Primo, Deuxio, Tertio, « Le reste se découvre en traçant. »
> mot-clé      PromiLate 25 pt — Primo, Deuxio, Tertio ; 32 pt pour « La suite t'appartient. »
> consigne     PromiLate 19 pt — « trace pour planter »
> guide        Atkinson 700, 29 pt / 42 — les deux phrases du guide ; leurs mots-clés (« monde », « Studio », « commence ») en PromiLate 29 pt
> ```
> Juge : `redteam_echelle_onboarding` (neuf rôles).
> **LA RÈGLE DE L'ORANGE (v146, rappelée)** : `#FB4C0D` marque les points de départ d'une action et rien d'autre (le + de l'accueil, le + qui valide un nom, le
> départ de la flèche) ; la même valeur reste celle de « Ma Parole ! » dans les murs (deux jetons, deux rôles). Les ronds orange de signature, qui n'étaient
> pas un départ, sont retirés (C-143).
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v148.py`) : `redteam_tenir` (G, H), `redteam_garder` (E à I),
> `redteam_transitions_onb` (réécrit), `redteam_guide` (le rappel au lieu d'avancer ; la phrase en gras, 29 pt, « monde » lilas), `redteam_echelle_onboarding`,
> `redteam_onb_sorties` (« fin » = le titre seul), `redteam_onboarding` (quatre touchers), `redteam_decisions` (les cartes, deux thèmes), `redteam_couleurs_ref`
> (E19 : les cartes).
> **⚑ TROUVÉ PAR LA SÉRIE COMPLÈTE (§13), CORRIGÉ** : ① **à « Promi planté ! », 2 voisines au lieu de 6** — la zone où on les choisit était le quart bas de
> l'écran (`haut:0.76`) ; la parole remontée à 647 (§9.3) n'en laissait presque rien : elle commence maintenant 0,115 écran au-dessus de la parole ;
> ② **`redteam_decoupe` ne reconnaissait plus le moteur depuis v145** : le serveur sert `promi-moteur.js?v=<empreinte>`, et la pile n'était lue que sur
> `promi-moteur.js:` — les appels du moteur retombaient sur une ligne d'`app.html` (6 « lignes nouvelles ») ; et il ne connaissait pas le peintre des îles
> de la Pelote (`dalleLisible`) appelé par la préparation au repos (C-135). *La règle* : **un juge qui lit une pile d'appels lit aussi l'URL avec sa
> requête** — une empreinte de cache ne doit pas changer ce qu'il attribue.
> ③ **le rail du pinceau sautait** (`redteam_flash`, rouge sur v148, vert sur v147) : il se place à mi-chemin de la phrase et de « garder de côté » ; le
> lien, visible dès l'ouverture depuis C-149, se cache pendant un tracé (`pp-cours`) : le rail sautait vers 760 puis revenait — il garde la cote fixe du lien
> (708) pendant le tracé ; ④ **après une plantation validée, le ruban rendait le mot « trace pour… » 640 ms plus tard**, la page + encore là : il reste
> découpé jusqu'à la fermeture ; ⑤ **la nature choisie se défaisait après une plantation** (`redteam_trait`, 9/10 sur v148, 10/10 sur v147) : à l'ouverture
> de la page + le minuteur des trois natures (130 ms) passait APRÈS un toucher de tuile fait pendant le rendu de la dalle (≈ 0,65 s d'un bloc) — un toucher
> est prioritaire sur un minuteur ; en v147 il passait de justesse avant. Le minuteur ne remet plus la page sur les natures si une tuile a été touchée
> depuis l'ouverture. *La règle* : **un minuteur qui « remet à zéro » vérifie qu'aucun geste n'est arrivé depuis qu'il a été posé.**
> ⑥ **pendant le rideau de « tenir », la nappe forçait le calcul des styles de toute la page DANS sa fonction d'image** (17 à 200 ms, 20 à 30 tâches sur
> 20 « tenir », lu dans la trace `redteam_fluide --qui` ; 1 à 2 sur v147) : `fillText` sur un canevas du DOCUMENT force ce calcul, et depuis la vitesse
> constante (C-118) la phrase s'écrit dès la première image. Elle s'écrit maintenant UNE fois dans un petit canevas hors du document et chaque image la
> pose 1:1 sous la découpe (même boîte au pixel, centre à 0,1 pt, encre de bord +5 % : l'anticrénelage). Après : 0 tâche de ce genre. ⚠ Les écritures de
> style sur `#detailPoster` à chaque image (≈ 415 par « tenir ») sont les MÊMES en v147 et v148 : le calcul des styles reste à chaque image, rendu par
> le navigateur. *La règle* : **sur un canevas du document, `fillText` et `ctx.font` forcent le calcul des styles — jamais dans une boucle d'images.**
> **Contrats périmés remis au niveau des décisions (originaux : `sauvegardes/*-avant-v148.py`)** : `redteam3` (C-105 : le thème de l'app change l'image
> partagée ; les boutons de thème du partage ne sont plus à l'écran depuis v143), `redteam_formes` et `redteam_nuee` (C-140 : le trait du Chiche `#130208`,
> du Cercle `#0A0415` ; C-116 : COMMENTAIRES en tête du Peaufiner d'un Cercle), `redteam_studio_tom` (C-130 : la phrase sur la Toile floutée sans contour),
> `redteam_reactif` (un DÉLAI d'attente de 3 s, l'instant « tenir » en dure 2,7 depuis C-111), `redteam_noms` (le mot « d'hier » daté d'il y a 36 h ne
> l'était qu'après midi : 24 h), `redteam_onboarding_texte` (C-124 §8, §9).
> **Rouges déjà sur v147 (rejoués sur `zz-av147.html`, mêmes valeurs), non traités dans ce lot** : `redteam_photo` (l'en-tête d'une fiche Chiche sur une
> photo : Δ 39 pour 42), `redteam_dessin` I et `redteam_dessin_photo` 7, `redteam_cercle_couleur` 6 (C-150), les titres de deux lignes rognés sur les
> cartes de l'Index (C-151) ; rouges par décision : `redteam_kaki` (C-017), `redteam_nuit` (le Zzz coupé), `redteam_contraste_trait` (Q513, Q514, Q528).

### ⚑ v147 (15–16 oct. 2026) — RETOURS iPHONE DE TOM SUR v146 : LA MAIN SUPPRIMÉE, LA TOILE VIDE, LE TRAIT DU CERCLE, L'ONBOARDING (TEXTES, ÉCHELLE, COULEURS, TRANSITIONS, TRACÉ), LE GUIDE EN VRAIES FLAQUES, TENIR EN RIDEAU, COMMENTER DEPUIS LA FICHE, LE MENU DU +. (Décisions Tom.) Ce bloc CORRIGE v146 (§4 le guide, §11 l'onboarding, §14 tenir), v145 §7 (« ni compteur »), v144 et E1 (la main).
> **Validés par Tom : C-112, C-115, C-122, C-132, C-133, C-134.** **C-137 (plus jamais de vidéo) : en tête du §7.**
> **⚑ C-139 — LA MAIN EST SUPPRIMÉE PARTOUT** (« une main n'est pas dans la direction artistique ») : `lot-E1-GESTES` est retiré (code, réglages, drapeaux
> `geste_vu_*`, `redteam_gestes`) ; « Revoir les gestes » des Réglages rejoue la présentation. L'invitation à tracer qui la remplacera : deux variantes à
> choisir, RIEN D'INTÉGRÉ — **`promi-invite-variantes.html`** (A « Le fil qui s'allume », B « Le départ qui avance » ; `variantes/invite-etat.js`).
> Juge : **`redteam_sans_main.py`** (aucune main nulle part, ni nœud, ni code, ni clé).
> **⚑ C-136 — LA TOILE VIDE COLORÉE AU CHARGEMENT, LA CAUSE** : un minuteur de 420 ms de l'onboarding d'AVANT v20 (`obFill(OB_FILL_AUTH)`, « toute la Toile
> colorée ») partait encore et coloriait les 69 cellules ; si le jeu de démonstration était posé, l'insertion progressive survivait au vidage. Le minuteur
> est retiré ; **sur un vrai téléphone sans sauvegarde, le jeu de démonstration ne se pose plus du tout** (il ne sert qu'aux bancs, `navigator.webdriver`).
> Juge : **`redteam_toile_vide.py`** (30 chargements).
> **⚑ C-140 — LE TRAIT DU CERCLE, DU CHICHE, DU PROMI** : la teinte du trait sur un champ (`NATTRAIT`) passe au plus sombre de sa nature (Promi `#022140`,
> Chiche `#130208`, Cercle `#0A0415`) ; les cartes et le Cercle DÉCLARENT leur trait (`data-trait`). Juge : **`redteam_contraste_trait.py`** (3:1 contre le
> champ ET contre le corps). ⚠ **ROUGE PAR DÉCISION À PRENDRE** : aucune couleur ne tient 3:1 à la fois sur le champ pastel et sur les corps sombres
> (`#5D4978`, `#7C3F58`, `#0E78F2`) — mesuré, détail en QUESTIONS ; et l'orange « à tenir » `#DD4D23` porte l'ÉTAT (§3) : il n'est pas changé.
> **⚑ C-124 — L'ONBOARDING, LES MOTS DE TOM** : « [Prénom], donc. Enchanté. » · « Quid d'un Promi à toi-même ? » · « Petite ou grande promesse, elle compte. » ;
> la ligne du prénom reste à sa hauteur, ce qui suit descend de 16 à 24 pt. « Promi planté ! » : le bloc arrive plus bas et plus espacé puis MONTE à sa place
> (1,1 s) ; son texte en Atkinson, +12,5 % (24 → 27 pt), ne recouvre plus les dalles du bas ; dans CE texte seulement, Promi, Chiche, Cercle en gras (couleur gardée).
> **⚑ C-138 — UNE SEULE ÉCHELLE POUR L'ONBOARDING ET LE GUIDE** (`lot-V147-ECHELLE-css`, variables `--ech-*` ; « si tu grossis une page, tu grossis celles
> d'avant et d'après ») — un RÔLE = une taille, sur toutes les pages :
> ```
> titre        PromiLate 52 pt — « PROMI » de « Promi planté ! » ; sa suite « planté ! » 42 pt
> phrase       Gilbert 35 pt / 66 — la phrase de promesse (« Toi, c'est … ? », « Je me promets de … »)
> texte        Atkinson 500, 27 pt / 32 — « [Prénom], donc. Enchanté. », « Quid… », « Petite ou grande… », la phrase de ton de la fin, la phrase du guide
> liste        Atkinson 500, 24 pt / 28 — les lignes de la fin (Primo…)
> mot-clé      PromiLate 27 pt — Primo, Deuxio, Tertio ; « monde », « Studio », « commence » ; 32 pt pour « La suite t'appartient. »
> consigne     PromiLate 19 pt — « trace pour planter »
> ```
> ⚠ La phrase du guide passe de 34 à 27 pt (la même échelle) — Q. Le texte de l'onboarding passe de Gilbert (v127) à Atkinson (le brief : « texte en Atkinson »).
> Juge : **`redteam_echelle_onboarding.py`** (même rôle = même taille, page par page).
> **⚑ C-126 — LA PAGE DU PREMIER PROMI, EN CLAIR, À LA LETTRE** : tout le départ de la flèche (chevron et traîne) en orange `#FB4C0D`, « trace pour planter » en
> `#00341A`, les points non tracés en noir `#000000` ; le sombre ne change pas.
> **⚑ C-141 — LES TRANSITIONS DE L'ONBOARDING** (`lot-V147-TRANSITIONS`, `_voileCellules`, `Toile_cellules` et `Toile_voisinesEtat` — lecture seule) :
> ① l'arrivée sur le prénom : le fond de la Toile plein, puis la Toile NAÎT cellule par cellule depuis le milieu (1,1 s, quand le démarrage a fini — trois
> images de moins de 25 ms), puis le mot-marque et « Toi, c'est … ? » s'écrivent ; ② les voisines se résorbent une à une (85 ms d'écart) PENDANT que ③ la page
> descend d'un bloc et passe derrière la barre qui monte (plus rien n'est masqué en une image) et ④ le plateau descend, la barre monte (0,8 s, des aplats), la
> vue reprend son cadrage pendant ce temps ; puis le guide (0,6 s de calme). Juge : **`redteam_transitions_onb.py`** (image par image ; ⚠ les durées ne se
> jugent qu'au calme, C-137).
> **⚑ C-125 — LE TRACÉ DES LETTRES EST BRANCHÉ PAR DÉFAUT** sur tous les textes de l'onboarding et du guide (`?trace=0` le coupe). Défauts corrigés (dents du g,
> fente du é, barres du t et du f, bosses des fûts). **La carte d'une lettre se calcule dans un Worker** (le fil principal ne fait que dessiner la lettre ;
> la plume attend sa lettre si elle n'est pas prête) ; suréchantillonnage ×2 au plus ; un cache par lettre. Mesuré au banc (27 pt ×3) : une image de 143 à
> 194 ms PAR LETTRE avant, 8 ms au plus après (WebKit). Polices tracées : Gilbert, PromiLate, Atkinson (`variantes/trace-chemins-*.js`).
> **⚑ C-094, 3e RÉCIDIVE — LE GUIDE EN VRAIES FLAQUES.** *La cause* : le juge de v146 demandait une zone « légèrement imparfaite » (recouvrement 0,90 à 0,988 avec
> une ellipse) — un rond à peine bosselé : c'est le rond que Tom a vu ; rien ne comptait les germes, les naissances, les ponts, ni ne bornait la zone. *Posé*
> (`variantes/flaques.js`) : des MÉTABALLES à noyau borné — 12 à 20 germes au hasard, naissances étalées sur les 40 premiers %, vitesses différentes, bord ondulé
> de 15 à 25 % qui change en grandissant, un pont qui naît entre deux flaques voisines avant qu'elles se touchent ; le temps est remappé pour que l'eau monte
> régulièrement (le noyau en 1/d² couvrait tout à mi-chemin, puis plus rien) ; 38 → 4 ms de calcul par image. La zone nette : 4 à 6 flaques nées DANS la boîte,
> une marge de 6 à 10 pt (lobes francs), plafonnée à droite du Studio avant l'Aura, ronde autour du + (son bouton est rond), toujours 5 pt en deçà du contour
> arrondi de la barre ; elle respire ; elle se referme à l'envers. La phrase monte de 60 pt ; « monde » en rose `#FFB8D2` ; « Studio » lettre à
> lettre aux quatre tons d'Ingénu dans l'ordre (bleu, rose, lilas, crème dalle). ⚠ **En clair ces couleurs, posées telles quelles, ne se lisent pas sur
> l'accueil flouté (rose 1,01:1, crème 1,26:1)** : le §7 du brief dit « tu ne la changes pas, tu me montres une capture » — Q. Juge : **`redteam_guide.py`
> complété** (germes, naissances, ponts, marge, le contour de la barre par sa FORME, aucun pixel net hors zone, respiration ; la cadence au calme seulement).
> **⚑ C-118 — TENIR : UN RIDEAU** (`lot-V146-MAREE`) : une seule nappe qui descend, au front irrégulier dessiné, plus des flaques séparées ; le reste de v146
> tient (~2 s, rien entre le trait et le vert, à plat). Juge : `redteam_tenir.py`.
> **⚑ C-116 — COMMENTER DEPUIS LA FICHE** : la ligne « Un mot… » est sur TOUTE fiche Promi et Chiche (et celle d'un Cercle, Q511), sans encart (un filet sous
> elle quand elle est ouverte) ; **le nombre de mots paraît s'il y en a, discret, sans pastille** (« 2 mots » ; corrige v145 « ni compteur ») ; dans Peaufiner,
> COMMENTAIRES est tout en haut, juste après le trait. Juge : `redteam_commentaires.py` (B et H réécrits).
> **⚑ C-142 — LE MENU DU +** : encarts 338 × 68 (× 1,09), pas 81, texte 24, aide 14 (deux lignes égales si elle ne tient pas — `text-wrap:balance`), Promi,
> Chiche, Cercle en PromiLate 25 en capitales. Juge : **`redteam_menu_plus.py`** (14 ; 6/14 sur v146 ; texte agrandi d'iOS simulé par les TAILLES, pas par un zoom).
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v147.py`) : `redteam_guide`, `redteam_commentaires` (B, H),
> `redteam_part` (le juge attend le clavier et le « + » posé — sous charge il tapait dans le vide), `redteam_tenir` (C), `redteam_trait`, `redteam_engagement`,
> `redteam_onboarding`, `redteam_onb_sorties` ; `redteam_gestes` est RETIRÉ avec la main.

### ⚑ v146 (14 oct. 2026) — RETOURS DE TOM SUR v145 : LE GUIDE EN FLAQUES, LES FICHES SOMBRES EN CLAIR, TENIR EN MARÉE, RITOURNELLE À 75 %, L'ONBOARDING, LES NOMS, AUCUN EMOJI. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v136 et v141 (le corps clair des fiches), v145 (Ritournelle, le guide, tenir, les initiales des parts, « Un mot… » absent d'un Cercle), v140 (Enregistrer sur l'accueil).
> **Validé par Tom : C-117 (la marque de version).**
> **⚑ C-130, LA RÈGLE DE TÊTE DU DESIGN : voir le §2 bis.**
> **⚑ L'ORANGE `#FB4C0D` (jeton `--c-orange-depart`, Swift `orangeDepart`) MARQUE LES POINTS DE DÉPART D'UNE ACTION, ET RIEN D'AUTRE : le + de l'accueil
> (son signe seul), le + qui valide un nom, le départ de la flèche du trait (le chevron, sur TOUTES les fiches, deux thèmes, tous les pinceaux ; page +,
> onboarding). La même valeur reste celle de « Ma Parole ! » dans les murs (`--orange-maparole`) : deux jetons, deux rôles.**
> **⚑ EXCEPTION NOMMÉE AU « ! » : « Promi planté ! »** (fin de l'onboarding, 11.4), à côté de « Ma Parole ! ». Espace insécable avant « ! ».
> **⚑ §8 (C-132, C-133) — TOUTES LES FICHES PRENNENT EN CLAIR EXACTEMENT LEUR VERSION SOMBRE** (Promi `#0E78F2`, Chiche `#7C3F58`, Cercle `#5D4978`) : planter,
> tenir, tenue, reçue, à plusieurs ; la page + et le Peaufiner sont la fiche. **« En clair, le corps des fiches est la crème `#F7F0DE` » (v136, v141) est
> MORT.** Où ça vit : `lot-V146-THEME` (`_ficheClair()` rend toujours faux, `_clairPour(el)`, `_enSombre(f)`), les sélecteurs `.light` ont reçu
> `:not(:where(#detailPoster…,#createSheet…,.th-sombre…))` et les sélecteurs du sombre un jumeau `.light … :where(…)` (outil `scratchpad/v146/p8_theme_css.py`,
> 647 et 426 sélecteurs), 37 variables reposées sur la fiche (`lot-V146-FICHE-SOMBRE-css`). Juge : **`redteam_fiches_theme.py`** (81 ; 22/79 sur v145).
> ⚠ **Une règle `.light` écrite après v146 doit porter ce `:not(:where(…))` si elle ne vaut pas pour la fiche.**
> **⚑ §1 (C-122) — AJOUTER UNE PERSONNE : la zone en pointillés EST le champ** (un champ caché `#gnSaisie` garde le clavier ; plus d'encart) ; un « + » orange,
> gras, haut comme une capitale du texte saisi, paraît au premier caractère et valide (Retour aussi) ; la ligne reste au-dessus du clavier (`visualViewport`).
> Juge : **`redteam_ajout_personne.py`** (122 ; 27/102 sur v145).
> **⚑ §2 (C-131) — LA MÊME TOILE EN CLAIR ET EN SOMBRE.** Cause trouvée : `reGray` / `reGrayStudio` retiraient les gris AU HASARD au changement de thème
> (le rang du gris est maintenant gardé, `_grisRang`). Le moodboard H est statique (43 paires identiques) ; la dalle différente que Tom a vue venait de la
> page des variantes de tenir de v145 (deux sessions). Juge : **`redteam_clair_sombre.py`** (24, tableau `planche-v146/clair-sombre.md`).
> **⚑ §3 (C-135) — LA PELOTE PARAÎT DANS L'IMAGE OÙ L'AURA S'OUVRE** : tout est préparé au repos (atlas, semis, ton, dalles des îles, îles, carte graphique) ;
> mesuré 1 436 ms → 108 ms à la première ouverture, 324–564 → 39 ms ensuite. Juge : **`redteam_aura_latence.py`**.
> **⚑ §4 (C-094, 2e RÉCIDIVE) — LE GUIDE EST FAIT DE FLAQUES.** *Cause* : « la demande portait sur une matière vivante, aléatoire et ciblée ; la livraison a été
> une découpe géométrique trop large qui se déplace ». L'accueil est flouté À L'AVANCE (`Flaques.floute`, 4,8) ; un masque dessiné à chaque image (relief tiré
> au hasard, niveau d'eau, contour net) : la couverture 1,4 s, l'entourage légèrement imparfait serré sur le Studio (puis le +), 0,7 s, qui se referme sur
> lui-même — jamais de translation —, la fin en flaques qui se vident. La phrase : 34 px, sans contour, mots-clés en PromiLate (« monde », « Studio » ;
> « commence »), en clair #291547 et #0E78F2. `lot-V141-GUIDE` réécrit ; vue au quart : `promi-guide-variantes.html?flaques=1`. Juge : **`redteam_guide.py`
> réécrit** (60). ⚠ L'entourage (10 ms de calcul) se prépare AVANT la couverture, et l'étape passe à l'image suivante : sinon une image de 15 à 21 ms.
> **⚑ §5–§7** : le + de l'accueil, son signe en orange ; « Enregistrer la Toile » retiré de l'accueil (on enregistre par Partager) ; les noms sous les icônes
> de l'accueil en `#022140` en clair (en sombre : la crème, `#022140` y ferait 1,27:1 — Q).
> **⚑ §9 (C-134) — PEAUFINER RESTE OUVERT.** Un choix s'applique sur place ; on sort par un glissement vers le bas (la fiche se découvre au-dessus du panneau) ;
> plus jamais la Toile depuis Peaufiner : `lot-V146-PEAUFINER` refuse une fermeture générale née d'un geste dans Peaufiner (4 s), sauf supprimer / dissoudre ;
> chaque refus est gardé et part au Mac avec `?mesure=1` (le chemin de Tom n'a PAS été reproduit au banc). Juge : **`redteam_peaufiner.py`** (19 ; 13/19 sur v145).
> **⚑ §10 (C-088 rouvert) — RITOURNELLE : DE 1 À 9 PAROLES, CHAQUE COULÉE VISIBLE À 75 % ET LES COULÉES COUVRENT 75 % DE L'ÉCRAN** : chaque coulée bute contre
> un cadre (`RIT_CADRE`, la zone plateau → barre et 6 pt autour), une parole seule est peinte (le bug du « texte qui flotte »), la part d'une coulée se
> resserre jusqu'à neuf paroles puis s'ouvre progressivement (`_ritPart`), vue à l'échelle 1, aucune graine sous la barre, deux graines ne se confondent
> plus (`_ecarte`). Juge : **`redteam_ritournelle.py` réécrit** (63, 1 à 15 paroles). **Q496 : sous Ritournelle, l'appui long ne déplace plus une dalle**
> (`_TIRE_NON`) — une coulée se centre sur sa cellule, la poser sous le doigt changerait le cadrage.
> **⚑ §11 (C-123, C-124) — L'ONBOARDING** : à « Promi planté ! », la Toile d'avant se retire en flaques et les voisines naissent une à une (le moteur :
> `vt0`, `_voisF` — elles poussent, les cellules autour s'écartent) ; les textes grossis (28 px, 80 % de la phrase), violet `#291547` en clair ; le message
> de fin en lignes courtes, mots-clés en PromiLate, au-dessus des dalles ; le reste vient au toucher (découpe provisoire ; `?trace=1` : le tracé). §12 :
> « trace pour planter » en `#00341A` en clair. Juge : **`redteam_onboarding_texte.py`** (42).
> **⚑ §14 (C-118) — TENIR EN MARÉE** (`lot-V146-MAREE`) : le trait vert s'épaissit et devient le haut d'une nappe du même vert, qui descend EN FLAQUES jusqu'à
> la barre (640 ms), porte « Parole tenue. » à l'encre, puis remonte en flaques à 2 s ; le champ garde sa nature, la dalle sa taille. `?mareeLent=4`.
> ⚠ La couche ajoutée à `#detailPoster` doit se déclarer visible en `!important` (le crible). Juge : **`redteam_tenir.py`** (28).
> **⚑ §15 (C-128, C-116) — LES NOMS** (`window._noms`) : entier s'il tient, sinon 6 lettres et « . », prolongé jusqu'à la lettre qui distingue ; un nom se
> touche (au GESTE : la fiche ne produit pas de `click` au doigt). Les mots : texte = nom = 16 px, visage rond sans cerclage, date sobre. **Q487 : initiales
> sous les parts TRACÉES seulement. Q486 : dans un Cercle, chaque membre engagé (`avec`) a sa part.** « Un mot… » aussi sur la fiche d'un Cercle, au-dessus
> de « + Planter dans le Cercle » (`promi_cercle_mots`). **La règle vaut aussi pour la phrase de la fiche (les noms s'y touchent), le sur-titre des cartes de
> l'Index et la ligne du Fil (`_noms.texte` : coupés seulement s'ils ne tiennent pas ; les noms des cartes ne se touchent pas, Q512).** Juges : **`redteam_noms.py`**
> (21), `redteam_commentaires` (28), `redteam_part` (55).
> **⚑ §16 (C-129) — AUCUN EMOJI** : filtrés à l'entrée, au collage et à l'enregistrement, sans message (`lot-V146-EMOJI`, `window._sansEmoji`). Juge : **`redteam_emoji.py`**.
> **⚑ TROUVÉ EN FIN DE LOT, PAR LA SÉRIE (corrigé, juges posés) :** ① **la ligne « Un mot… » d'un Cercle vit DANS le bloc collant de « + Planter »** (`#cmCale`,
> `_comm.pose(…, {dans})`) : posée dans la fiche qui défile, elle partait avec le fil et recouvrait ses cartes (pris par `redteam_joignable`) ; **un Cercle
> sans parole n'a pas la ligne** (16 pt seulement : elle recouvrait l'état et poussait « + Planter » sous le bandeau ; Q511) ; **le nom d'un Cercle n'est
> jamais abrégé** (la règle des noms vaut pour les pseudos). Juges : `redteam_cercle_tom` (+2), `redteam_noms` (+2). ② **Le bandeau Peaufiner n'est pas un
> mur** : le test du mur acceptait « tout ce qui est dans la même fiche » — une rangée réservée passée sous le bandeau faisait monter une phrase au toucher
> du bandeau et, la toute première fois, l'offre s'ouvrait seule. Juge : `redteam_peaufiner` F (+2). ③ **Le garde de C-134 refuse aussi un `closeAll` de
> SCRIPT** dans les 4 s d'un geste fait dans Peaufiner : **un juge qui ferme tout après Peaufiner appelle d'abord `window._peaufSortie()`** (sinon la fiche
> suivante s'ouvre sous un Peaufiner resté ouvert — `redteam_fiches_theme`, `redteam_gens` y ont perdu des contrôles). ④ **Le résolveur d'état de la
> fiche (`_ficheEcran`) sert aussi les CARTES** (Index, Fil, fiche d'une personne, par une « fausse fiche » sans nœud) : depuis C-132 il répondait
> « sombre » pour elles aussi — en clair, leurs libellés d'état sortaient à l'encre au lieu de l'orange et du violet (pris par `redteam_couleurs_ref`).
> Il ne force le sombre que pour un vrai nœud (la fiche, la page +). ⑤ **Le « + » qui valide un nom ne prend plus le focus** : le champ le perdait
> 30 ms à chaque toucher (clavier qui clignote, lettres perdues) — `redteam_ajout_personne` (+ « le champ ne perd jamais le focus »).
> ⑥ **La préparation de la Pelote au repos (C-135) suit la règle des tâches de fond de v143 : jamais dans les 6 s qui suivent « tenir »** — elle
> repartait ~3,2 s après le lever, par étapes de 240 à 306 ms (un toucher y attendait 0,3 s ; `redteam_fluide` 5 : 306–491 ms → 30 ms).
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v146.py`) : `redteam_onboarding` (le texte de 11.4, les
> mots-clés en PromiLate, deux touchers), `redteam_onb_sorties`, `redteam_maparole` (C : le corps sombre en clair aussi), `redteam_murs`, `redteam_tonsurton`
> (à « referme » le champ garde sa nature, le trait passe à l'amande), `redteam_couleurs_ref` (E13 : en clair les fiches et la page + se comparent à la
> référence sombre ; E14 : l'orange du départ ; E15 : les noms de la barre), `redteam_volume`, `redteam_decisions`, `redteam_guide`, `redteam_ritournelle`,
> `redteam_deplace`, `redteam_cercle_tom`, `redteam_gens`. `banc_rendu` refigé pour Ritournelle seul (§10) : les 266 autres images au pixel.

### ⚑ v145 (13 oct. 2026) — RETOURS DE TOM SUR IPHONE (« RIEN NE CHANGE ») : LA VERSION QUE VOIT L'iPHONE, LA TOILE REMPLIE, RITOURNELLE RENDUE À SON CADRAGE D'AVANT. (Décisions Tom et chef de chantier.) Ce bloc CORRIGE v139 à v144 (Ritournelle) et v144 (la fluidité de la Toile, C-112).
> **Validés par Tom sur iPhone : C-110 (la main seulement sur une fiche à tenir, à 3 s), C-113 (la Pelote fluide sous le doigt). Q473, Q474 acceptées.**
> **⚑ LA RÈGLE DU LOT (R-B) : « LA VÉRITÉ, C'EST L'iPHONE DE TOM. » Quand Tom dit « rien ne change » et que le banc dit « corrigé », le banc a tort.
> Avant toute discussion on cherche : ① l'iPhone sert-il la nouvelle version ? ② le banc reproduit-il L'ÉTAT de Tom — une Toile PLEINE, son monde,
> sa palette, son thème ? Les deux ont été sautés : Ritournelle « corrigée » trois fois, la Toile « fluide » deux fois.**
> **⚑ §1 — LA MARQUE DE VERSION EST ÉCRITE DANS LA PAGE (C-117).** *Ce qui manquait* : `?mesure=1` demandait le commit AU SERVEUR — une page restée
> en mémoire dans Safari affichait donc le commit du jour sur un code de la veille ; la marque ne prouvait rien. `serveur.py` écrit maintenant,
> AU MOMENT DE SERVIR `app.html`, le commit (et « + » si l'arbre de travail est modifié) et l'empreinte du moteur dans `window.PROMI_VERSION`
> (`lot-V145-VERSION`) ; le `<script src>` du moteur prend son empreinte en paramètre (aucun cache ne peut rendre un vieux moteur) et
> `promi-moteur.js` déclare la sienne (`PROMI_MOTEUR_RECU`) : un mélange se VOIT. Avec `?mesure=1`, une pastille en haut de TOUS les écrans :
> **« v145 · <commit> »**, puis l'état réel de l'appareil (« 25 paroles · 2 Cercles · encre · signal · clair ») ; sans rien demander, au retour au
> premier plan, **si le serveur sert un autre commit que celui de la page, la page se RECHARGE**. Il n'y a ni service worker ni manifeste ;
> chaque réponse porte `Cache-Control: no-store`. **Le lot (`lot:'v145'`) s'écrit à la main dans `lot-V145-VERSION` au début de chaque lot.**
> **⚑ LA PAGE MESURE SES PROPRES IMAGES ET LES ENVOIE AU MAC.** Avec `?mesure=1`, chaque plantation, retrait ou « tenir » compte les images des
> 3,6 s qui suivent (au-delà de 20 ms, de 33,4 ms, la plus longue), l'affiche sur la pastille et l'envoie à `serveur.py` (`POST /mesure` →
> `mesures/appareil.jsonl`, hors du dépôt). **La fluidité se lit sur le vrai téléphone, sans inspecteur ni réglage : c'est LA preuve de C-112.**
> **⚑ §2 — LA TOILE REMPLIE (C-112, RÉCIDIVE).** *Pourquoi le juge de v144 était vert* : `redteam_evol` plante TROIS paroles sur une Toile vide.
> Sur une Toile de 25 paroles relue de la sauvegarde (`banc_tom.toile_pleine`, `banc-etats/etat-10|25|50.json`) : à chaque plantation, `syncAll`
> repeignait les vignettes du Fil et de l'Index FERMÉS (`peintMinis`) ; **la dalle qui grandit change de cellule à chaque image, sa vignette
> n'est donc jamais « prête »** : elle était rendue de nouveau à chaque passage (37 à 66 ms), et le passage se redemandait à chaque image tant
> que la Toile bougeait — 25 passages, 48 rendus, 1,2 s de travail pendant l'apparition ; puis `_teinterFil` relisait les 25 canevas d'une
> traite (jusqu'à 780 ms sous Ritournelle). Et ces vignettes-là ne sont même jamais montrées (le Fil ouvert est rebâti par `lot-S4`).
> *Corrigé* : ① `syncAll` ne refait vignettes et teintes QUE pour la liste qu'on voit (une liste fermée se rebâtit à son ouverture) ; ② un
> passage de vignettes attend la fin du mouvement (`window._minisAttend`, sur `_evol()`), ses reprises ne repassent que sur ce qui reste, une
> dalle par tâche, jamais sous un doigt ; ③ la largeur d'un titre de la Toile n'est plus remesurée à chaque image (`_mes`, mêmes valeurs). ④ la passe
> de lisibilité attend 400 ms APRÈS la fin du mouvement (4,2 s au plus ; un toucher la laisse passer tout de suite) : la vue se recadre encore
> quand la dalle est posée, et sous Ritournelle la passe (23 ms) tombait dans ce recadrage.
> *La règle* : **un juge de fluidité tourne sur une Toile REMPLIE, relue de la sauvegarde ; et ce qu'on ne voit pas ne se peint pas pendant
> qu'on regarde autre chose.** Juge : **`redteam_pleine.py`** (les COMPTES de rendus pendant le mouvement — ils ne dépendent pas de la charge
> de la machine — puis les durées, jugées seulement au calme ; rouge sur v144).
> ⚠ **RESTE OUVERT (Q476)** : sur une Toile presque vide (trois paroles), sous Touffe, une image de 108 à 117 ms au RETRAIT, une passe sur deux
> (`redteam_evol` 31/32 ces passes-là) : la Toile se repeint entière, le coût est dans le tracé (aucun rappel au-delà de 18 ms). À 25 et 50 paroles
> le retrait sous Touffe est passé de 34–35 images longues à 5–6. En sombre, Ritournelle et Brouillamini peignent encore lourd à 25–50 paroles.
> ⚠ **CE MAC EST PARTAGÉ** : une autre session (projet ENTRE) y lance `swift test` et un simulateur iPhone 17 — c'est « le simulateur qui se
> rallumait » de v144. **On ne l'éteint pas** ; une mesure de cadence attend le calme (`banc_tom.charge()` < 4) ou se déclare « non jugée ».
> ⚠ **`banc_tom.plante()` (clic scripté sur la tuile) GARDE LE CHICHE après un Chiche** : 46 Chiche sur 50 paroles « Promi ». Pour une Toile de
> plusieurs natures : **`banc_tom.plante_doigt()`** (le +, puis la pilule de la nature — le vrai chemin).
> **⚑ §3 — RITOURNELLE : LE CADRAGE D'AVANT C-088 REVIENT TEL QUEL, ET C-088 EST CLOS.** (Tom : « Je préférais presque l'effet arty bien zoomé :
> remets-le et clôture ce sujet. ») Les cotes de remplissage de v140 à v144 (55 %, 67,5 %, 85 %), le semis constant sous neuf paroles, les
> cellules vides cachées et le cadrage sur la matière **ne valent plus pour Ritournelle** : sa Toile est faite de ses seules paroles DÈS LA
> PREMIÈRE, vue entière — le cadrage d'E1 (commit `c8f4571`). Dans le moteur : `_NEUF_TOUJOURS={ritournelle:1}` (une ligne ; tout le code de
> v140–v144 dépendait de « semis constant », il devient inerte pour elle). **Les onze autres mondes de la famille gardent la règle de v139**
> (semis constant sous `SEMIS_NEUF_MIN` = 9). Preuve : mêmes graines qu'E1 servie à côté (± 1 pt — E1 lui-même varie d'un point d'une passe à
> l'autre), écart de pixels dans le bruit d'E1 contre E1 ; planche `planche-v145/PLANCHE-ritournelle-e1-v145.png`. Juge :
> **`redteam_ritournelle.py` réécrit** (original : `sauvegardes/redteam_ritournelle-avant-v145.py`). ⚠ **À UNE SEULE PAROLE, Ritournelle ne
> peint RIEN** (une cellule couvre l'écran) : c'était vrai en E1, c'est rendu tel quel, et signalé à Tom (Q480). **On ne revient plus sur ce
> cadrage sauf si Tom le demande.**
> ⚠ **CONSÉQUENCE : SOUS RITOURNELLE, DÉPLACER UNE DALLE (C-101) NE TIENT PLUS À MOINS DE NEUF PAROLES** — dans une Toile faite de ses seules paroles les
> cellules se partagent l'écran et reprennent leur équilibre (`redteam_deplace` 16/18 : les deux contrôles de Ritournelle). À dix paroles, code de
> v144 : la dalle finit à 97 pt du doigt sous Ritournelle, 34 sous Esquille, 8 sous Pochade — **le juge de v142 ne plantait que trois paroles : il n'a
> jamais jugé « déplacer » dans un vrai semis neuf.** Non corrigé, signalé à Tom (Q496).
> **⚑ §6 — À PLUSIEURS : LA RÈGLE DE LA PART (C-115, `lot-V145-PARTS`, `window._parts`).** Quand une parole engage PLUSIEURS personnes, la seconde
> moitié du trait est divisée en autant de parts que de personnes qui doivent tenir (14 pt entre deux). **Une part tracée est pleine, à la
> couleur de l'état tenu (la crête `#0B4A2A`) ; une part non tracée est un trait FIN (2,5 pt), continu, dans la teinte de la nature — jamais de
> pointillés.** La fiche — et sa dalle, sa carte d'Index, son bandeau du Fil — **ne passe à « tenu » qu'à la DERNIÈRE part**. Jusqu'à quatre
> personnes : l'initiale de chacune sous sa part ; au-delà : « 3 SUR 6 », couché le long du trait. Toucher la seconde moitié du trait ouvre la
> liste des noms, avec la date de chaque part. **Une parole à une seule personne ne change pas.** La consigne reprend les phrases de v144 :
> « trace pour tenir » si MA part reste, sinon « à Rachel de tracer sa part » / « à chacun de tracer sa part ». La main fantôme ne paraît à
> plusieurs que si ma part reste à tracer. **Qui doit tenir (`_parts.tenants`)** : Chiche lancé → ceux à qui on le lance et ceux avec qui on le
> fait ; Chiche reçu → moi et ceux avec qui on me le lance ; Promi demandée → ceux à qui on la demande ; Promi reçue → celui qui me la promet ;
> Promi que je fais → moi, même à plusieurs destinataires, même dans un Cercle. Données : **`p.parts = {nom: date ISO}`**.
> **⚑ PLANTER À PLUSIEURS = UNE SEULE PAROLE** (`who` = les prénoms séparés par `', '`) : la page + en plantait une PAR destinataire.
> ⚠ Le prototype n'a pas de réseau : **`?parts=1`** permet, dans la liste des noms, de tracer la part d'un autre en touchant son nom.
> Juge : **`redteam_part.py`** (55 : deux, trois et cinq personnes, tous les ordres, la couleur lue sur l'image, l'Index, la sauvegarde ;
> `--sonde` 8/11 ; 2/8 sur v144). ⚠ Trois pièges du juge : sous l'onde le canevas est TRANSPARENT (on lit l'alpha, pas une couleur de fond) ; une
> initiale se trouve juste sous sa part (la fenêtre de lecture reste à ± 7,5 pt de l'axe) ; le geste a besoin de `tenue=380`, comme `redteam_trait`.
> **⚑ §7 — LA LIGNE « UN MOT… » (C-116, `lot-V145-COMM`, `window._comm`).** *L'état des lieux de v144* : les commentaires existaient (`p.comments`)
> mais le champ « écris un mot » de la fiche ne répondait pas au toucher, un commentaire s'y superposait à son auteur, la liste n'était
> affichée nulle part, et une parole reçue « à tenir » ou tenue n'avait aucune ligne. *Posé* : sur toute fiche Promi ou Chiche REÇUE, sur une
> parole en cours, et dès qu'un commentaire existe — **une ligne en bas de la fiche, toujours visible (342 × 56 à y 692, contour 3 px à l'encre
> du corps), qui ouvre la saisie au toucher** ; au-dessus, le dernier commentaire sur une ligne ; la ligne touchée, les commentaires se lisent
> sous le trait, du plus ancien au plus récent, « PRÉNOM · date » puis le texte. **Ni compteur, ni pastille, ni relance (§12).** Le texte
> « Un mot… » est PROVISOIRE (texte à écrire par Tom). ⚠ **Pas sur la fiche d'un Cercle** (« + Planter dans le Cercle » y tient le bas, C-096).
> Juge : **`redteam_commentaires.py`** (26 ; `--sonde` 6/26 ; 2/8 sur v144). ⚠ Quatre pièges payés : `#dpMain` (frère suivant, z-index 2)
> recouvrait la ligne → z-index 3 ; un `display` posé en ligne ne se cache que par la VISIBILITÉ ; le contour prenait la couleur d'état
> (orange sur « à tenir ») → toujours l'encre du corps (C-053) ; les couleurs d'une fiche se gardent dans une `WeakMap`, jamais sur la parole.
> **⚑ §4, §5 — TENIR (C-118) ET LE GUIDE (C-094) : DEUX PAGES DE VARIANTES, RIEN N'EST INTÉGRÉ.** (R-D : « design d'abord, jouable sur l'iPhone, Tom
> choisit ».) **`promi-tenir-variantes.html`** — A « La marée », B « Le fil », C « Le double » ; Promi et Chiche, clair et sombre, ×1 et ×¼ ;
> la fiche y est REDESSINÉE dans un canevas depuis les cotes relevées sur l'app (`variantes/tenir-donnees.js`, `scratchpad/v145/donnees_tenir.py`)
> et la vraie dalle du moteur (une image rendue à sa taille). **`promi-guide-variantes.html`** — A « Les nappes », B « La buée », C « Le
> courant ». *La technique du guide, à garder* : **aucun `backdrop-filter`** ; l'accueil est flouté À L'AVANCE à trois intensités (2,4 · 4,8 ·
> 9,6 pt) ; une matière (des formes à bord doux) est dessinée à chaque image dans un canevas à la résolution 1 et sert de MASQUE aux trois
> images : la zone nette est l'ABSENCE de matière, il n'y a donc ni sur-intensité là où deux zones se recouvrent, ni disque plus clair. Au
> banc WebKit : le dessin coûte 0 à 1 ms par image. Les deux pages envoient leur mesure d'images au Mac (`/mesure`). **L'app joue encore
> l'instant de v144 et le guide de v144.**
> **⚑ §8 — CHAMADE AU BANC DE RENDU (C-114), LA CAUSE.** La FORME d'un cœur est gardée par clé et reprise tant que sa taille ne s'écarte pas de
> 3 % (`_loc`) : le premier rendu qui la demande fixe la taille de référence, les suivants la mettent à l'échelle. Ce que le banc obtenait
> dépendait donc de ce qui avait été rendu AVANT (la pose précédente, une vignette de fond partie pendant le démarrage) — 2 ou 3 résultats
> d'une passe à l'autre, alors que les graines, la clé de la Toile, le hasard et la géométrie vive étaient identiques. `window._chaOublie`
> (porte du moteur pour le banc seul) vide ces mémoires avant chaque pose ; `window._vivantOff` coupe la vie au repos pendant le banc.
> **Cinq passes de suite : identiques.** La référence de Chamade est REFIGÉE (14 images, elle seule : 11 différaient — Toile ≈ 3 000 pixels,
> dalles 1 à 3 912 ; les 266 autres images sont au pixel). *Écarté en chemin* : les graines, la vie au repos seule, le budget de coût
> (`_chCout`), les mondes précédents. ⚠ La PREMIÈRE pose d'une page varie encore quand Chamade est le premier monde posé (un reste du
> démarrage en temps réel, non nommé) ; le banc ne retient un monde qu'après deux poses identiques. *La règle* : **un cache à tolérance rend
> un rendu dépendant de son passé — un banc au pixel le vide avant de mesurer.**
> **C-102 (`redteam_fluide`) : EXPLIQUÉ, NON TRAITÉ.** v144 et v145 passés l'un après l'autre sur le même banc : 4/6 et 4/6 puis 5/6 — ce lot n'y change rien.
> ① une tâche de 36 à 56 ms à ≈ 2,76 s après le lever, 4 fois sur 20 : un morceau de la pose de la fiche tenue (`_tenirMorceaux`), quand plus rien ne
> bouge ; ② 0 à 2 images de 21 à 28 ms sur ≈ 6 500 (première image de l'instant, ou passage à « juste après »). `--qui` nomme les tâches. L'instant en
> trois états sera remplacé par la variante choisie (C-118) : la règle des 20 ms se rejuge à l'intégration.
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v145.py`) : `redteam_ritournelle` (réécrit) ·
> `redteam_toucher` (Ritournelle : autant de cellules que de paroles) · `redteam_engagement` R5 (la troisième parole tenue est une des miennes :
> « courir dimanche », lancé à deux, n'est plus tenu par mon seul tracé) · `banc_rendu` (Chamade refigé, `_chaOublie`, `_vivantOff`).
> ⚠ **Un `<script id="lot-…">` posé avant un `<style>` sans id lui VOLE l'attribution de `redteam_volume`** (208 « volumes nouveaux » : la
> dette est rangée par lot) : `lot-V145-VERSION` est posé juste avant `lot-TOKENS-css`.

### ⚑ v144 (12 oct. 2026) — RETOURS DE TOM SUR IPHONE : LA FLUIDITÉ (LA TOILE QUI ÉVOLUE, LA PELOTE SOUS LE DOIGT), LA MAIN SEULEMENT SUR UNE FICHE À TENIR, RITOURNELLE PLUS PRÈS, TENIR PLUS LENT, LE GUIDE. (Décisions Tom.) Ce bloc CORRIGE v143 (le guide, Ritournelle, la main, la trace) et E1 (l'inventaire des gestes), E0 (R6).
> **Validés par Tom sur iPhone : le partage de la Toile (C-105), la barre (C-106), le trait de 60 pt (C-107), la trace de la Pelote. Q466, Q468, Q470 acceptées.
> Q465 : au neutre — « À RACHEL DE TRACER SA PART » / « À CHACUN DE TRACER SA PART ».**
> **⚑ LA MAIN FANTÔME NE PARAÎT QUE SUR UNE FICHE À TENIR (PROMI OU CHICHE), POUR LE GESTE DE TENIR — NULLE PART AILLEURS, DÉFINITIVEMENT (C-110).** Ni au
> Studio, ni sur l'Aura, ni sur la page +, ni au Fil, ni à Partager, ni en mode dessin, ni sur la bande, ni sur le trait de l'onboarding. L'inventaire
> (`GesteFantome.inventaire()`) ne porte plus que `tenir` et `chiche` ; les huit autres gestes d'E1 et les quatre recensés sont RETIRÉS — ne pas en
> rebrancher. Elle paraît **3 s après le toucher qui ouvre la fiche** (`INACTIF_FICHE` 3 000 ; mesuré 3,1 à 3,2 s). Juge : **`redteam_gestes.py` réécrit**
> (27 ; 13/27 sur v143 ; original d'E1 : `sauvegardes/redteam_gestes-avant-v144.py`).
> **⚑ UN TRAVAIL QUI N'EST PAS LE MOUVEMENT NE TOURNE PAS PENDANT LE MOUVEMENT — UN SEUL GARDE, `window._evol()` (C-112).** *Ce qui faisait saccader la Toile
> quand une dalle arrive ou part*, mesuré sur banc_tom (WebKit), planter puis retirer, cinq mondes : ① **`_boiteSerre`** (la boîte des cellules des
> paroles, v141) coûtait 32 à 63 ms dans l'image où la dalle doit paraître, et sous Ritournelle elle était recalculée À CHAQUE IMAGE de l'apparition
> (`boitesNeuves` → `autoView` : 21 appels, 870 ms — une régression de v142) : elle ne compare plus un point qu'aux graines qui peuvent le prendre,
> elle est gardée tant que places et poids finaux n'ont pas changé, et le recadrage passe au plus toutes les 220 ms (puis une dernière fois quand la
> dalle a fini de grandir) ; ② deux tâches de fond parties 400 ms après le toucher, AVANT que la Toile ait commencé à bouger — leur garde ne regardait
> que « la Toile tourne-t-elle » (une dalle de la collection, 36 à 59 ms ; le réchauffage du cache, jusqu'à 126 ms) ; ③ la passe de lisibilité
> (`repasse`, 18 à 105 ms) et la passe des polices (tranches de 5 à 22 ms). `_evol()` est vrai du toucher qui plante ou retire (`_tEvol`, posé au clic
> et par `Toile.addPromi` / `sync` / `removePromi`) jusqu'à la fin du mouvement ; les tâches de fond attendent 4 s après (`_evolRecente`) ; les passes
> attendent la fin (2,6 s au plus) quand c'est la Toile qu'on regarde (`_toileVue()`). Le guide pose le même garde pendant ses deux transitions.
> ⚠ **Deux pièges payés en posant ce garde** : ① il ne vaut que pour CE mouvement-là (il part de `_tEvol` et tombe au premier toucher suivant) — écrit
> « vrai dès que la Toile bouge », il retardait la composition de la page + (`redteam_flash` B1, B2 : elle ne paraissait plus à temps) et l'ouverture
> des fiches ; ② **on ne retarde PAS `window._apresMouvement` au nom de `_evol()`** : Ramage passe par cette porte, la retarder changeait ce qu'il rend
> (`banc_rendu`, 14 images).
> Juge : **`redteam_evol.py`** (le TRAVAIL de chaque rappel pendant le mouvement ; rouge sur v143). *La règle* : **avant d'accuser un monde, chronométrer
> chaque rappel de la page pendant le mouvement (`scratchpad/v144/toile.py`) ; et un garde de tâche de fond part du TOUCHER, pas du mouvement.**
> ⚠ Reste, nommé et non corrigé : sous Touffe, un retrait repeint la Toile trois fois vers 0,5 s (67 à 139 ms par image ; une seule en v140).
> **⚑ LA PELOTE SOUS LE DOIGT (C-113).** *La cause* : depuis v141–v142 chaque mouvement du doigt recalculait les poils voisins DANS l'écouteur
> `pointermove` (4 à 20 ms) et les renvoyait à la carte graphique à l'image suivante. Les segments attendent maintenant dans `FILE` ; ils sont inscrits
> en une fois, JUSTE APRÈS une image, dans leur propre tâche (le calcul tient alors entre deux images), au plus une fois toutes les 66 ms (la cadence
> s'espace jusqu'à 300 ms si l'image qui suit dépasse 20 ms). La trace se forme toujours sous le doigt. ⚠ Essai fait et mesuré, à ne pas refaire :
> l'inscrire DANS le rappel d'image ajoute son coût à la peinture (18 à 32 images lentes sur une caresse de 2,3 s).
> **⚑ RITOURNELLE, ENCORE PLUS PRÈS (C-088).** Une parole → sa dalle à **65–70 %** de la largeur (67,5 visés) ; deux et trois → ensemble à **80–90 %**
> (85 visés), de la largeur ou, empilées, de la hauteur de la zone ; à partir de quatre : inchangé. ⚠ Trouvé : juste après une plantation la vue
> restait cadrée sur les CELLULES (une dalle à 53 %, 67 % seulement après avoir rouvert l'app) — le recadrage repasse quand la dalle est posée.
> `redteam_ritournelle` (37/37, cibles remontées ; original : `sauvegardes/redteam_ritournelle-avant-v144.py`).
> **⚑ LE MOMENT « TENIR » DURE LE DOUBLE (C-111).** L'instant amande (« Parole tenue. » / « Défi relevé. ») reste **2 000 ms** (1 000 avant), Promi comme
> Chiche (`window._tenirRegle.AMANDE`) ; « juste après » vient ensuite, la pose complète 700 ms plus tard — du lever à la fiche tenue : 2,7 s (1,7
> avant). `redteam_fluide` porte 2 000 en dur (original : `sauvegardes/redteam_fluide-avant-v144.py`).
> **⚑ LE GUIDE D'ACCUEIL (C-094) — CE BLOC REMPLACE CE QUE v143 DIT DE SON MOUVEMENT.** ① **Le Studio à sa taille normale** ; le + garde + 10 %.
> ② **« Plus tard » est RETIRÉ, du guide comme de l'onboarding — « le parcours est court, on ne le passe pas » : EXCEPTION NOMMÉE DE R6**
> (`TEXTES_ENGAGEMENT.sansPlusTard`, portée par `redteam_engagement` et `redteam_onb_sorties`). Le panneau du compte garde son « Plus tard » (c'est le
> refus du compte). Toucher ailleurs fait AVANCER le guide (du Studio au + ; au +, il se retire). ③ **La suite de l'onboarding** : l'accueil posé, le
> flou commence **0,6 s** plus tard (`ATTENTE` ; mesuré 0,66 à 0,70 s), **d'un seul mouvement** : les six formes partent ENSEMBLE, même durée
> (**1,8 s**), même courbe douce presque régulière (`cubic-bezier(0.33,0.12,0.67,0.88)`) ; **elles RESTENT** (v143 les remplaçait par une couche
> unique : le flou sautait à cet instant). ④ **Du Studio au +, pas de saut** : la zone nette est une LOUPE (`#guideLoupe` : une fenêtre ronde à bord
> doux qui montre une copie nette des cinq entrées de la barre, au-dessus du flou) ; elle glisse du Studio au + en **1,2 s** (`GLISSE` ; un `transform`
> par image sur deux nœuds, formules exactes), les six formes se réorganisent autour (par `transform`), puis la phrase du + paraît. **Le Studio touché
> s'ouvre PAR-DESSUS le flou** (`#guide` est sous les écrans, z-index 69) : refermé, avec ou sans choix, la loupe glisse de même. `?guide=1`,
> `&gfige=900`, `&getape=plus`, `&gglisse=600`. Juge : **`redteam_guide.py`** remis au niveau (57 ; original : `sauvegardes/redteam_guide-avant-v144.py`).
> ⚠ Trois faits du lot : le calque de la loupe ne fait que la bande de la barre (à 390 × 844 ×3 sa première peinture coûtait une image de 130 ms) ;
> les formes se recouvrent en permanence, le flou y est plus fort que 4,8 px (flou d'un flou) ; dans Safari le flou ne se VOIT qu'à partir de 0,5 s.
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v144.py`) : `redteam_gestes` (réécrit) · `redteam_guide` ·
> `redteam_ritournelle` · `redteam_fluide` · `redteam_onb_sorties` (aucun « Plus tard », aucune main) · `redteam_engagement` (R6 : l'exception nommée).

### ⚑ v143 (12 oct. 2026) — RETOURS DE TOM SUR IPHONE : RITOURNELLE, LE PARTAGE DE LA TOILE, LA BARRE, LE TRAIT DE 60 pt, TENIR, LE GUIDE REFAIT, LA MAIN, LA PELOTE. (Décisions Tom.) Ce bloc CORRIGE v142 (Ritournelle, le guide, la trace, C-102) et v141 (le trait parti du milieu).
> **Q457 validée (les lettres cernées sur la Toile floutée). Q459, Q462, Q464 acceptées. Q463 : un Chiche lancé à soi dit « TRACE POUR LANCER ».**
> **⚑ SAFARI N'A PAS `requestIdleCallback` — TOUT CE QUI « ATTEND UN TEMPS MORT » Y TOURNE PAR SIMPLE MINUTERIE (C-102, RÉCIDIVE).** *Pourquoi
> `redteam_fluide` ne le voyait pas* : il tourne sous Chromium, qui a `requestIdleCallback`. Sur le banc WebKit, au vrai doigt, deux tâches de
> fond tombaient en plein dans l'animation de « tenir » : la collection de l'écran qui vend (`fond(j)`, une dalle de 80 à 90 ms, à 620,
> 1 070 et 1 500 ms après le lever) et le réchauffage du cache des dalles (`rechauffe`, 75 à 100 ms, à 1 700 ms). Elles attendent maintenant
> un VRAI calme : 3 s sans aucun toucher (le lever compris), jamais pendant « tenir » ni dans les 6 s qui suivent. **La tâche du lever ne pose
> plus rien** (les cotes et le trait de l'instant : 10 à 19 ms dans la tâche du `touchend`) : l'instant se pose à l'image suivante, les cotes
> dans une image, le trait dans la suivante — de même au passage à « juste après » ; le contenu déjà rempli à 320 ms n'est pas refait à la
> fin ; les deux poses différées d'une fiche passent une par image, la passe de lisibilité après elles. Mesuré (banc WebKit, 4 passes) :
> travail compté dans les 1,8 s après le lever **196 à 281 ms → 57 à 60 ms** ; plus long rappel **100 ms (185 ms d'image) → 16 ms** ; la
> tâche du lever **17 à 24 ms → 3 à 5 ms**. *La règle* : **une tâche de fond se garde elle-même (aucun toucher, aucune animation) — elle ne
> compte pas sur le navigateur ; et la fluidité d'un geste se mesure AUSSI en WebKit** (`scratchpad/v143/profil.py` : chaque rappel chronométré).
> ⚠ Reste : une tâche de 17 à 49 ms à 1,77 s (`_fichePoseBase`, après l'animation, rien ne bouge) — C-102 reste EN ATTENTE DE TOM sur l'iPhone.
> **⚑ §1 — RITOURNELLE, LES CIBLES EN DUR (C-088, RÉCIDIVE).** Dans la zone visible (y 100 → 710) : **une parole → sa dalle entière, centrée, 50 à
> 60 % de la largeur (55 visés), des bords de cellules vides autour, aucune cellule vide entière ; deux et trois → ensemble 70 à 85 % (78 visés ;
> empilées, la même cible sur la hauteur de la zone) ; quatre → trois cellules vides entières au plus ; six → cinq au plus.** *Pourquoi c'est
> revenu* : v142 obtenait « aucune cellule vide » en ne PEIGNANT plus les cellules vides — les dalles, seules sur un aplat, étaient cadrées à
> 80 à 94 % ; et sans aucune parole la Toile n'était plus peinte du tout (**c'est « le fond de l'onboarding tout noir »** : l'onboarding
> rejoué sous Ritournelle, en sombre). **Toutes les cellules sont de nouveau peintes** ; le cadrage se fait sur la matière publiée
> (`cadreMatiere`, `_boiteMatiere`) aux fractions ci-dessus, 80 % de la hauteur au plus ; jusqu'à trois paroles, sous le cadrage de départ
> seulement, les cellules vides qui tiendraient ENTIÈRES dans la zone ne sont pas peintes (`videsCaches`) — celles que les bords coupent
> restent. Juge : **`redteam_ritournelle.py` réécrit** (37 ; 24/37 sur v142), captures annotées. *La règle* : **« un peu de Toile autour »
> s'obtient par le cadrage, jamais en effaçant la Toile ; et un juge de cadrage tient des CHIFFRES (une largeur en pour-cent), pas « entier ».**
> **⚑ §2 — L'IMAGE PARTAGÉE DE LA TOILE EST LA TOILE AFFICHÉE (C-105).** *La cause* : `Toile.renderTo` rendait « la Toile entière, sans cadrage »
> (vue 1), sur un autre fond (`#EFE2C5` pour `#DFCAA4`), le monde « au repos », et **dans le thème de `_sealDark` — sombre par défaut, réglé
> par des boutons (`#sealTheme`) qui ne sont plus à l'écran** : une app claire partageait une Toile sur fond noir, dézoomée. `renderTo(cv, ech,
> clair, {vue:true})` (le partage, Enregistrer) rend COMME L'ÉCRAN : la vue du moment, le fond de la Toile, le monde vivant, le thème de
> l'app ; `_rtCible` y reste posé (les calques de Touffe se bâtissent à la densité du rendu). Sans l'option (banc de rendu, aperçus) rien ne
> change. Juge : **`redteam_partage_toile.py`** (vingt mondes, l'image que le vrai bouton produit, comparée au canevas de l'accueil).
> **⚑ §3 — LA BARRE (C-106).** *La cause* : chaque entrée faisait 90 pt pour des centres à 54 pt — STUDIO (x 25 → 115) et AURA (79 → 169) se
> chevauchaient de 36 pt, AURA au-dessus : la moitié droite du mot STUDIO ouvrait l'Aura (de même INDEX / FIL). Chaque entrée fait 54 pt,
> toute la hauteur de la barre. Juge : **`redteam_barre.py`** (cinquante touchers répartis sur ce qu'on VOIT de chaque entrée ; sur v142 :
> 17 sur 25 pour STUDIO, 13 sur 25 pour INDEX).
> **⚑ §4 — UN TRAIT NE COMPTE QU'À 60 pt (C-107).** `window._traitRegle.MIN` = 60 : l'avancée du doigt, de là où il s'est posé au plus loin où il
> est allé, en points de l'appareil — pour TENIR comme pour PLANTER. Les voies d'avant sont RETIRÉES (deux tiers du trait, la moitié de la
> zone, « parti du milieu il faut aller presque au bout », et **« un geste lent de plus de six points », qui validait un doigt posé**).
> Juge : **`redteam_trait.py`** (11 ; sur v142 un geste lent de 30 pt tenait la parole). **Geste : Tom valide sur iPhone.**
> **⚑ §6 — LE GUIDE D'ACCUEIL, REFAIT (C-094).** **Le moment** : l'accueil entièrement posé (onboarding refermé, Toile au repos, aucun doigt), puis
> 1,2 s de calme (`ATTENTE`). **La technique, dictée par Tom** : le rayon du flou n'est jamais animé ; six FORMES à bord doux (un dégradé
> radial en masque, posé une fois) portent le flou des murs (4,8 px) et grandissent PAR `transform`, courbe ease-in-out, jusqu'à se rejoindre
> en 1,6 s — c'est le navigateur qui anime, la page n'écrit rien image par image ; puis UNE couche floutée les remplace. Ce qui reste net est
> une COPIE de l'entrée (style calculé, pseudo-éléments rendus par de vrais nœuds), au-dessus du flou, agrandie de 15 % (Studio) ou 10 % (+) ;
> l'original est caché le temps du guide. La phrase paraît à 1,15 s, une fois le fond flouté sous elle. **« Choisis d’abord le monde qui te
> ressemble, au Studio. » : un impératif VOULU par Tom — exception NOMMÉE de A3** (`TEXTES_ENGAGEMENT.imperatifVoulu`, portée en dur par
> `redteam_engagement` et `redteam_guide`). **Exception NOMMÉE de A2** : les six formes, et elles seules, portent une transition CSS sur
> `transform`. **L'étape du + vient TOUJOURS ensuite** (Studio refermé avec ou sans choix, ou toucher ailleurs pendant l'étape du Studio :
> le flou reste, l'entrée nette change) ; seul « Plus tard » arrête tout ; à l'étape du +, toucher ailleurs finit. `?guide=1`,
> `&gfige=800`, `&getape=plus`. Juge : **`redteam_guide.py` réécrit** (moment, technique, les chemins, images ≤ 16,7 ms : pire 4 à 5 ms).
> ⚠ Entre 0,6 et 1,2 s, les formes se recouvrent : le flou y est un peu plus fort (flou d'un flou), puis la couche unique le remet à 4,8 px.
> **⚑ §7 — LA MAIN FANTÔME (C-109).** Au banc, par un vrai premier lancement (onboarding, guide, fiche), elle paraît 2,1 à 2,25 s après le toucher
> qui ouvre la fiche, par les trois chemins du guide. *Ce qui l'empêchait sur un téléphone déjà utilisé* : ① le drapeau `geste_vu_tenir`
> (posé depuis E1) survit aux versions ; ② il était posé DÈS L'APPARITION — un toucher dans le dixième de seconde la retirait pour toujours ;
> ③ « Revoir la présentation » ne rendait pas les gestes. **Le drapeau se pose à la fin du PREMIER PASSAGE** (corrige E1) ; faire le geste
> soi-même le pose ; les drapeaux du trait sont oubliés une fois (`geste_v` = 143) ; « Revoir la présentation » et `?guide=1` rendent tous
> les gestes.
> **⚑ §8 — LA PELOTE (C-083).** **L'intensité d'un segment de trace se LIT** (`intensite`) : la lenteur du doigt (60 pt/s et moins : 1 ; 500 et
> plus : 0), l'appui (la force si elle VARIE — un écran sans capteur rend 0 ou 1 tout le temps ; sinon la taille du contact, 7 pt → 0,
> 16 pt → 1), la durée d'un appui immobile (0,2 s → 1,2 s) : `f` de 0,25 à 1 (0,9 constant avant). Sans capteur (une souris), la largeur
> est celle d'un pouce — le seul nombre qui ne soit pas lu. `redteam_trace` : + G, H, I (17 ; 13/17 sur v142). Le corps : tableau
> `scratchpad/v143/corps.txt` (24 palettes × 2 thèmes × 10 ouvertures).
> ⚠ **La frontière entre deux entrées de la barre passe au milieu de CE QU'ON VOIT d'elles** (le mot STUDIO finit à 96, l'icône d'AURA commence
> à 110 : la zone de STUDIO va jusqu'à 102 et passe devant) — au milieu de leurs centres (97), deux touchers sur cinquante tombaient à côté.
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v143.py`) : `redteam_ritournelle`, `redteam_guide`
> (réécrits) · `redteam_gestes` (le drapeau à la fin du premier passage) · `redteam_engagement` (A3 : l'exception nommée, en dur) ·
> `redteam_volume` (le bord doux des formes du guide : deux masques, bornés) · `redteam_trace` (+ G, H, I) · `redteam_decisions` et
> `scratchpad/v122/zones.py` (C-103). ⚠ **Un juge qui veut la main fantôme CACHÉE pose aussi `geste_v` = 143** (sans lui l'app oublie une fois
> les drapeaux du trait : `redteam_air` y a perdu 104 paires) ; `banc_tom.contexte` le fait.
> **Aussi** : les phrases de trace, cas par cas (C-108) — un Chiche lancé à plusieurs disait « RACHEL, MARION TRACERA SA PART SI ELLE OSE » :
> « chacun tracera sa part s’il ose » (mot manquant, à valider) ; C-103 : `redteam_decisions` lit le champ que le peintre DÉCLARE s'il est
> réellement peint (0,3 % du canevas au moins), plus un pixel à (6 ; 6) — 89/89 trois fois.

### ⚑ v142 (11 oct. 2026) — SIX RÉCIDIVES, UNE CAUSE COMMUNE : LES JUGES NE VOYAIENT PAS CE QUE TOM VOIT ; DÉPLACER UNE DALLE. (Décisions Tom.) Ce bloc CORRIGE v141, v140 et v139 là où ils disent autre chose.
> **Q450, Q453, Q456 acceptées ; Q454 close ; Q455 validée (les poils couchés) ; Q452 : le É de « MOITIÉ » est composé en PromiLate (le composeur
> de v35 : E + l'apostrophe en accent ; `.pp-trace` est dans sa liste, et le mot n'est écrit que s'il change — le piège de v46).**
> **⚑ LA RÈGLE DU LOT, QUI DEVIENT LA RÈGLE : POUR TOUT POINT VISUEL, LA PREUVE EST PRISE COMME TOM LA VOIT — `banc_tom.py` : WebKit, 390 × 844,
> échelle 3, évènements tactiles (touchstart, touchmove, touchend), par le chemin réel depuis l'accueil.** *Pourquoi six juges étaient verts sur
> des défauts que Tom voyait* — trois écarts entre le banc et son iPhone, mesurés : ① **sous navigateur piloté (`navigator.webdriver`) l'app
> garde le jeu de démonstration ; sur un téléphone la Toile part VIDE et l'état est relu** (`loadState`) — une Toile d'une parole plantée par
> l'app, puis rouverte, n'avait jamais été jugée ; ② **à 390 × 844 l'appareil est RÉDUIT (× 0,933 ; ≈ 0,82 dans Safari sur l'iPhone)** — les
> juges tournaient à 430 × 932, échelle 1 : tout ce qui dépend de la réduction leur échappait (un `position:sticky` borné en points d'écran,
> une cote comparée dans deux unités) ; ③ **ils passaient par un raccourci** (`openDetail()`, `.click()`, la souris) au lieu du chemin. `banc_tom`
> masque `webdriver`, plante par l'app, touche au doigt. ⚠ Playwright-WebKit ne rend pas `backdrop-filter` dans ses captures et n'émet pas
> d'évènements de pointeur sur `touchscreen.tap` : un flou se juge sur l'image en Chromium (à 390 × 844) et se REGARDE dans le Safari du
> simulateur. **⚠ Le simulateur ouvert sur Promi charge la machine (backboardd à 49 %) et fausse toute mesure de cadence : on le ferme avant
> de mesurer** (`xcrun simctl shutdown all`).
> **⚑ §2 — LA TRACE DE LA PELOTE EST UNE BANDE CONTINUE, À LA LARGEUR DU CONTACT LU (C-083, RÉCIDIVE).** *Pourquoi c'est revenu* : v141 posait UN arc
> par « zone », au plus un toutes les 360 ms, long comme l'empreinte et large de 0,12 à 0,42 rad par un rapport au pouce (× 2,2) : ni sa
> longueur ni sa largeur n'étaient celles du geste ; son juge vérifiait qu'une trace PARAISSAIT et suivait le sens, pas sa taille. *Aujourd'hui* :
> à chaque mouvement (dès 0,035 rad, 4 pt de boule) le point de la boule sous le doigt est relié au précédent par un segment large du contact
> lu (`radiusX` / `radiusY`, en travers du geste), **`G.DOIGT_K` = 1** (le 2,2 disparaît ; bornes 0,035–0,60 rayon, pour écarter une lecture
> absurde) ; le creux prend la même taille ; **un appui immobile laisse la forme du contact, à taille réelle** (`poseContact`, au lâcher) ;
> `?mesure=1` écrit « contact lu : 13 × 7 pt ». Mesuré sur l'image : contacts de 6, 12, 18 pt → bandes de 12, 23, 35 pt ; trajets de 30, 60,
> 100 pt → 32, 45, 54 pt (la boule suit la main : la trace est le GLISSEMENT du doigt sur elle). **`retoucheTraces` ne compare plus les poils
> retouchés qu'aux traces VOISINES** (un arc n'agit qu'à moins de sa largeur) : 12 → 4,7 ms par inscription, cadence sous le doigt p95 20–21 ms.
> Juge : **`redteam_trace.py` réécrit** (13 ; 2/13 sur v141). `redteam_enfonce` relisse entre deux appuis (il mesurait par-dessus la marque d'avant).
> *La règle* : **une trace se juge sur sa TAILLE peinte, contre la taille du geste — jamais sur sa seule présence.**
> **⚑ §3 — LE GUIDE DE FIN DE PARCOURS (C-094, RÉCIDIVE).** 0,8 s de calme ; le flou naît en **six taches à bord courbe** (dix rayons inégaux reliés par
> des courbes : `clip-path:path()`), qui grandissent et se rejoignent, **1,8 s** (`INSTALLE`) ; **net sur l'icône du Studio ET le mot STUDIO,
> agrandis de 15 %** — « Vingt mondes pour une seule Toile. Le tien est au Studio. » ; la toucher ouvre le Studio ; **l'étape du + n'arrive
> qu'après le Studio VU ouvert puis refermé** ; net sur le + et son encart, **agrandis de 10 %** — « Promi, Chiche ou Cercle : tout commence par
> ce +. ». Le trou est un masque FIXE (une image vectorielle), l'agrandissement est posé en ligne sur le vrai bouton et rendu à la fin.
> L'horloge de l'installation part à la PREMIÈRE IMAGE rendue (partie à la pose, une page occupée mangeait le début : 1,42 s vues). `?guide=1` le rejoue ; `&gfige=600` l'arrête à cet instant, `&getape=plus` montre la seconde étape (pour le regarder dans Safari).
> *Pourquoi c'est revenu* : le juge vérifiait que le masque GRANDISSAIT et que l'icône était nette — ni la forme (des zones à bord franc),
> ni la durée, ni le mot STUDIO, ni la taille de l'agrandissement. Juge : **`redteam_guide.py` réécrit** (51 ; travail par image lu dans la
> trace : pire 4 à 6 ms). ⚠ **Chromium rogne un flou d'arrière-plan à la BOÎTE de sa découpe** : ses captures d'installation montrent un bord
> droit qui n'existe pas dans Safari — les captures de l'installation se prennent au simulateur (`PLANCHE-3-guide-*-safari.png`).
> ⚠ Sur une Toile vide (peu de contraste) le flou ne se VOIT que là où il y a des contours : le plateau, la barre, les dalles.
> **⚑ §4** : la main paraît **1,5 s** après que la fiche est prête (`INACTIF_FICHE` ; mesuré : 1,3 s après la fin de l'ouverture, 1,8 après son
> début) ; son dessin est une silhouette simple (un tracé, intérieur d'une couleur, contour épais) ; après « tenir », **une seule ligne :
> « Parole tenue. » (Promi), « Défi relevé. » (Chiche)** — `TEXTES_ENGAGEMENT.tenir`, `#instTenue` à 40 px, `#instSous` vidé.
> **⚑ §5 — LA FICHE D'UN CERCLE OUVERTE DEPUIS LA TOILE (C-096, RÉCIDIVE).** *Pourquoi c'est revenu* : WebKit borne un `position:sticky` au bas de la
> zone visible comptée en points d'ÉCRAN quand l'ancêtre est réduit par `transform` — à 390 × 844 le bandeau s'arrêtait à 703 au lieu de 760 ;
> le juge ouvrait la fiche par `openDetail` à l'échelle 1. Parade : l'écart est MESURÉ et rendu (`--colle`, `lot-V142-CERCLE`) ; le fil a une
> hauteur minimale (748 − son haut). Juge : **`redteam_cercle_tom.py`** (16 ; 6/16 sur v141), par la dalle du Cercle touchée sur la Toile.
> **⚑ §6 — « DISSOUDRE LE CERCLE » EST LE DESSIN DE « SUPPRIMER CE PROMI »** (corbeille, 13 px capitales, aucun encart). *Pourquoi c'est revenu* : la
> règle CSS de v141 était battue par un style EN LIGNE `!important` posé par `pose()` — le juge lisait la règle, pas le rendu. Posé à la source.
> *La règle* : **un style en ligne `!important` bat toute feuille ; ce qu'un poseur écrit se corrige dans le poseur.**
> **⚑ §7 — RITOURNELLE (C-088, RÉCIDIVE).** Cibles sur la zone VISIBLE (plateau → barre) : **1 à 3 paroles : seulement ces dalles, aucune cellule vide,
> même en partie ; à 4 : deux ou trois au plus ; ensuite peu** (`_videsVus` : 0 jusqu'à 3, 2 à 4–5, 3 à 6–7, 4 à 8 ; à 9 la Toile de ses
> seules paroles, v34). Sous Ritournelle les cellules vides non montrées ne sont PAS PEINTES, et la vue cadre la MATIÈRE publiée par le
> peintre (`window._ritBoites`, `_boiteMatiere`), 80 % de la largeur à une parole, 94 % au-delà. **La place d'une parole est GARDÉE**
> (`p.place=[x/W, y/H]`, `NUEPLACE` pour un Cercle) : à la réouverture, `sync` replantait au hasard et dispersait les paroles.
> *Pourquoi c'est revenu* : le juge de v141 semait par `Toile.sync` sous navigateur piloté ; par le vrai chemin (planter, rouvrir) la dalle
> faisait 44 % de la largeur. Juge : **`redteam_ritournelle.py` réécrit** (13 ; 5/13 sur v141), par `banc_tom`, rechargement compris.
> **⚑ §8 — LES MURS DU STUDIO (C-100, RÉCIDIVE).** *Ce qui empêchait le toucher* : ① la Toile floutée d'un monde de Ma Parole ! (`#stBg`) n'était PAS un
> mur — on la touchait, rien ; ② un toucher tactile attendait le clic fabriqué par le navigateur, qui arrivait parfois avant le minuteur du
> mur et ouvrait l'offre (1 sur 20). Les murs lisent `touchstart` / `touchend` et répondent tout de suite ; la Toile floutée est un mur (du
> bas du plateau au haut du bouton d'achat ou du panneau) ; la phrase y est **cernée** (`.sur-toile` : un contour de 9 px à la couleur du
> fond du mode — sur une matière colorée floutée l'encre seule ne se lisait pas ; à valider, Q457) ; pendant la lecture le nom du monde et
> les réglages du panneau se retirent. Juge : **`redteam_studio_tom.py`** (14 ; 10/14 sur v141).
> **⚑ §9** : « Supprimer mon compte » est la dernière ligne des Réglages (C-104). **§1** : sous Ingénu les poils et le corps de la Pelote sont tirés
> parmi les trois natures et leurs voisines, jamais les crèmes (`ingenu()`) ; en clair le poil garde la teinte de la nature, clarté OKLCH bornée à
> **0,50** (`ING_L` ; à 0,60 les dalles de la Pelote passaient sous le plancher ΔE 15 — pris par `releve-aura`), chroma × 1,5 dans le gamut.
> ⚠ La couleur RENDUE de la boule est un mélange du poil et du corps : `releve-aura` admet une teinte sur l'arc entre les deux tons déclarés.
> **⚑ §11 — DÉPLACER UNE DALLE (C-101).** Un appui de **0,8 s** sans bouger (8 pt de jeu) sur une dalle l'attrape : elle grossit à peine (7 % d'une
> cellule, aucune ombre), sa graine suit le doigt, les voisines se réorganisent (`relax`) ; au lâcher sa place est écrite (`p.place`,
> `NUEPLACE`) et **la cellule vide la plus proche prend celle qu'elle quitte** (comme à la réouverture — sans cela la dalle « sautait » de
> 28 pt au rechargement) ; la vue appartient à la main dès la prise (aucun recadrage) ; jamais sous la barre. Un toucher bref ouvre toujours
> la fiche ; un glissé sans attendre déplace la vue. `Toile_tire()`, `Toile_tireRegle`, `Toile_vueLue()` (pointeurs pour les juges).
> Juge : **`redteam_deplace.py`** (45, cinq mondes, par `banc_tom` ; 5/9 sur v141). **C'est un geste : Tom valide sur iPhone.**
> **⚑ LA PLACE GARDÉE ET LE BANC DE RENDU.** Une place ne vaut que DANS LA FAMILLE de semis où elle a été prise (`p.place=[x/W, y/H, 1]` pour un monde
> fait de ses seules paroles) : notée sous le semis constant, elle regroupait les graines d'un monde neuf (Esquille : des dalles deux fois plus
> petites). Et une dalle garde, d'un monde à l'autre de sa famille, le décalage du monde où elle a été plantée : `banc_rendu` juge une Toile
> NEUVE, il **oublie les places avant chaque pose** (sans cela cinq mondes différaient ; prouvé : place désactivée, 280/280).
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v142.py`) : `redteam_trace`, `redteam_guide`,
> `redteam_ritournelle` (réécrits) · `releve-aura` acquis 4 (un toucher immobile laisse UNE marque) et la teinte rendue (entre le ton du sol et
> celui du corps) · `redteam_vide` (`#instSous` n'est plus obligatoire) · `redteam_gestes` (1 500 ms sur une fiche, main de 39 pt) ·
> `redteam_toucher` (le « vrai départ » simulé oublie les places) · `redteam_enfonce` (relisse entre deux appuis) · `banc_rendu` (oublie les places).
> **Deux juges étaient rouges depuis un lot précédent, sans que la série d'alors les ait passés** : `redteam_nuee_dalle` (le bloc du Cercle à 750
> depuis v141, C-096 : la cote « au-delà de 760 » est remise à niveau) et `redteam_bouton` (il comparait le bouton au mot du trait, grandi à
> 19 px en v140 : la valeur décidée du bouton, 10,67, est portée en dur). `redteam_air` : référence REFIGÉE (les deux paires de la seconde ligne
> de l'instant, retirée par décision).
> **⚑ §10 — C-102 RESTE OUVERT, ET LE CONSTAT CHANGE.** Machine au calme, v140, v141 et l'app d'aujourd'hui donnent tous **4/6** à `redteam_fluide`
> (cinq à six images de 20 à 29 ms au lever et vers 1 025 ms ; des tâches de 50 à 65 ms après l'animation). **Le diff v140 → v141 n'ajoute
> rien** : les tâches de 249 à 979 ms relevées en v141 venaient de la charge (le simulateur ouvert). Le « 6/6 » de v140 n'est pas retrouvé non
> plus. Seule `passeVisible` a été découpée (tranches de 5 ms dans les 4,5 s qui suivent). **6/6 trois fois de suite n'est pas atteint : 5/6, 4/6, 5/6 en fin de lot** (trois images de 20 à 85 ms au lever du doigt sur vingt animations ; une fois, une tâche de plus de 33 ms après l'animation).

### ⚑ v140 (10 oct. 2026) — LA FOURRURE D'AVANT LES ESSAIS ; LA TRACE DU VRAI GESTE ; DESSIN ↔ PHOTO ; L'ICÔNE ENREGISTRER ; LE + ; RITOURNELLE ; LE MUR DU STUDIO ; E2 ET E2bis. (Décisions Tom.) Ce bloc CORRIGE v139 (la Pelote, le +, Ritournelle, le dessin partagé), v120–v123 (la densité 3) et E1 / v129 (l'onboarding).
> **Q434 : rien à faire. Q435 : un dessin part ENTIER, photos importées comprises (« c'est une composition ») ; seule une photo posée seule dans la
> bande ne se partage jamais. Q437 : remplacé (Ritournelle, plus bas). Le dessin est COLLABORATIF (C-093) : écrit dans `portage/SPEC-DONNEES` §5 bis
> et `SPEC-ECRANS`, à construire avec Firebase — rien n'est construit.**
> **⚑ LA FOURRURE DE LA PELOTE (C-083, RÉCIDIVE « trop rase »). LA RÈGLE : LA FOURRURE EST CELLE D'AVANT LES ESSAIS DE HALO — DENSITÉ ×1 (110 000 →
> 90 000 → 75 000), POIL ×1, REFLET D'ORIGINE, POINTES LIBRES AU BORD. On ne touche plus ni à sa densité ni à l'épaisseur du poil pour régler autre
> chose (un bord, un halo, une cadence) : c'est `redteam_fourrure.py` qui la tient.** Référence : `sauvegardes/app-avant-v114.html`.
> *Pourquoi elle avait perdu sa longueur* : ① v120–v123, la « densité 3 » (`REG` : deux fois plus de poils, chacun ×0,7 d'épaisseur, reflet
> adouci) — des poils si fins qu'ils ne se lisent plus un à un : un aplat ; ② v139, la limite franche au rayon de la boule coupait net les
> pointes (jusqu'à 5 pt). *Ce qui est posé* : `REG={facteur:1, epaisseur:1, doux:false}` ; dans `FS2` le corps est plein jusqu'au rayon de la
> boule, et au-delà **les pointes** dessinent la silhouette (contour moyen 120,5 pt, de 118 à 124). Deux précautions mesurées sur des essais :
> la masse des poils de profil au-delà du corps est à demi transparente (un anneau pâle) → son opacité est resserrée (0,30 → 0,62) ; et ces
> pointes prennent la couleur de l'intérieur (poil SUR corps), sinon elles font un anneau d'une autre couleur (le corps a une autre teinte que
> le poil, v123). Le peintre de secours suit la même loi (une passe sur la couronne). Rien autour, sauf l'ombre, revenue à 391,224.
> Banc WebKit, carte graphique : p50 17 ms, p95 21 à 22 ms, 57 images/s à 110 000 poils. Juges : **`redteam_fourrure.py`** (réglages en dur,
> contour au-delà de la boule et dentelé, pas d'anneau, rien autour ; 9/9, 5/9 sur l'état d'avant — ⚠ son contrôle B, le grain, ne sépare pas
> les deux états : ce sont A, C et D qui mordent) ; `redteam_bord` F réécrit (des pointes sans frange pâle) ; `redteam_halo` (anneau 127–150).
> **⚑ L'EMPREINTE SUIT LE VRAI GESTE (C-083).** *La cause du « tampon »* : un arc de 24 pt était posé tous les 20 pt AU POINT TOUCHÉ — or la boule
> suit la main, ce point est toujours le même point de l'objet : dix arcs empilés, la même marque quel que soit le geste ; et un toucher posait
> toujours le même arc vers le bas. *Aujourd'hui* : le chemin du doigt est RELEVÉ à l'écran (un point tous les 8 pt, avec la largeur du contact) ;
> au lâcher la trace est posée le long de ce chemin, rapporté à la boule telle qu'elle est à cet instant — seize arcs au plus, chacun dans le
> sens du geste, large comme le contact (0,27 rad pour un pouce, de 0,12 à 0,42). **Un appui sans glisser pose une ÉTOILE** : huit branches du
> point vers l'extérieur ; leur longueur suit la taille du contact et la profondeur atteinte. `_aura.tracesGeo()` pour les juges. Juge :
> **`redteam_trace.py`** (8 : deux trajets, deux traces alignées et centrées sur eux, la longue ≥ 1,5 × la courte, la largeur suit le contact,
> l'étoile, deux appuis deux tampons ; 2/8 avant). ⚠ La trace paraît au REPOS (doigt levé, élan éteint), pas sous le doigt : c'est la règle
> de la saccade (v124). **Geste : Tom valide sur iPhone.**
> **⚑ DESSIN ↔ PHOTO : L'UN REMPLACE L'AUTRE (C-086, C-085).** *La cause de la « bande parasite »* : le dessin posé et la photo vivaient ensemble ;
> la couche du dessin recouvrait la photo, mais elle s'arrête 7 pt au-dessus de l'axe du trait (`BANDE_RETRAIT`) — dans cette lisière on voyait
> la photo ; et après un dessin, une photo importée restait dessous, invisible. **Poser un dessin retire la photo de la bande ; importer une
> photo retire le dessin posé (`window._photoImportee`)** — il n'en reste rien. ⚠ C'est un remplacement : le dessin (ou la photo) remplacé est
> PERDU (Q439). Les points de taille : **une cible de 44 pt chacun** (`CIBLE`), le point fait le diamètre du trait + 3 (`POINT_PLUS`) ; **le
> gros pinceau fait 22 pt** (2 · 6 · 22). Juge : **`redteam_remplace.py`** (18 : dessin → photo → dessin → photo, la bande comparée au pixel à
> la photo seule ; 8/18 avant).
> **⚑ UNE SEULE ICÔNE « ENREGISTRER » (C-091)** — la flèche qui descend dans son socle (le miroir de Partager), sans texte, VoiceOver
> « Enregistrer ». Où : ① la vue en entier d'une photo ; ② la vue en entier d'un dessin (`.ev-garde`) ; ③ le plateau de l'accueil, à gauche de
> Partager (`#enrToile`, `lot-V140-ENREGISTRER`) : l'image de la Toile rendue par le moteur (`Toile.renderTo`, 1170 × 2532), jamais une capture.
> Pas ailleurs : Partager a déjà son bouton, qui ouvre la feuille du téléphone (Q440).
> **⚑ LE + DE L'ACCUEIL (C-087)** : le disque passe de 33 à **45 pt**, l'anneau garde 13,5 → 72 pt ; **la barre fait 100 pt de haut (710 → 810 ; 716 → 804 avant)**,
> 12 pt d'air au-dessus et au-dessous de l'anneau ; le centre du + (y 760), la croix et les quatre entrées restent où ils étaient à l'écran.
> ⚠ La cote de la barre se lit sur le RENDU : la règle de base dit 736, une règle plus tardive la pose à 716 — j'avais d'abord écrit 730 et déplacé
> la barre de 14 pt (pris par `redteam_accueil`). ⚠ `redteam_accueil` 7 est ROUGE : la dalle « semer les radis » est plantée sous la barre
> (centre à 745) ; au zoom de départ elle n'était atteignable que par une lisière de 3 pt, que la barre plus haute recouvre (Q449).
> **⚑ RITOURNELLE, LE ZOOM DE DÉPART (C-088) — AMENDE v139.** Sous les douze mondes « faits de leurs seules paroles », tant qu'ils gardent le semis
> constant (moins de 9 paroles) : ① la parole neuve prend la cellule libre LA PLUS PROCHE des paroles déjà là (la première : du milieu du
> champ dégagé), sans décalage (`plantOne`) — tirées au hasard, deux paroles tombaient aux deux bouts de la Toile ; ② la vue cadre les dalles
> colorées avec 0,8 cellule de marge pour une parole, 1,25 dès deux (une dalle colorée pèse plus qu'une cellule vide : sa matière déborde
> d'une cellule), et un plafond de zoom de 3,6 (1,3 et 2 ailleurs) (`autoView`, `_serre`). ⚠ « Une dalle entière » se juge sur les PIXELS de sa
> matière : ni la zone que le toucher lui attribue (`Toile.hit`) ni la boîte de sa cellule (`dalleAbs`) ne la valent (389 pt de « boîte » pour
> 180 pt peints). `redteam_toucher` lit les couleurs des dalles sur la capture. Une parole : une dalle entière
> et un peu autour ; deux, trois, quatre : toutes entières, peu de cellules vides ; à neuf, la Toile faite de ses seules paroles.
> **⚑ LE MUR DU STUDIO (C-092)** — *la cause* : le panneau flouté du Studio est fait de quatre murs en bandes (tons 54 pt, libellés 19, disques 44,
> barrettes 4) ; la phrase se centrait dans la bande touchée, et une bande de moins de 40 pt la renvoyait sur l'appareil entier — au milieu
> de l'écran, sur le nom du monde. **Au Studio le mur est le PANNEAU** (la réunion de ses bandes floutées). Et le panneau des palettes, ouvert
> sur un monde de Ma Parole !, est lui-même un mur, flouté (2,4 px) : il recouvrait les quatre zones, qui restaient les murs. Juge :
> **`redteam_studio_mur.py`** (9 : sept zones touchées au doigt ; 3/9 avant). ⚠ Son amorce doit porter `decouvert:1`, sinon c'est « la toute
> première fois » et l'offre s'ouvre seule.
> **⚑ E2 — LE PREMIER PROMI (C-075) ET E2bis — L'INTERFACE SE DÉVOILE (C-076).** `lot-E2`, `ENGAGEMENT-E2.md` (le tableau garder / supprimer /
> remplacer, les textes, ce que chaque point est devenu). Après le prénom : **le principe** (un bouton, « Plus tard ») → **la VRAIE page +**
> (Promi à soi, une phrase fantôme parmi trois, un toucher la remplit ; ni Peaufiner, ni pinceau, ni photo, ni retournement, ni « garder de
> côté ») → la plantation réelle → **la fiche**, une ligne dessous, la main accompagne le trait → tenir → **la dernière ligne**, un toucher
> ferme, `ob_fini`, puis le compte. « Plus tard » à chaque étape : un toucher, tout est affiché, rien n'est redemandé. **L'écran « parole et
> trait » de l'onboarding, sa plantation simulée et le message de fin de v129 (« Primo… Deuxio… Tertio… ») ne sont plus joués.** « Revoir la
> présentation » rejoue le principe seul. Textes PROVISOIRES dans `TEXTES_ENGAGEMENT.e2`, sans impératif.
> **« TRACE POUR TENIR » et le trait** : le mot passe de 15 à **19 px** (fiche et page +), les points à tracer de Ø 9 à **Ø 12**, en
> grandissant vers le haut (`margin-top` négatif, centre des points remonté de 1,5) — rien ne bouge dessous.
> **E2bis** : `promi_devoile` (`{index, aura, studio, fil}` ou `'tout'`) ; la barre ne porte que ce qui est déjà apparu, chaque entrée À SA
> PLACE DÉFINITIVE, le fond (`#accBarreFond`) s'étire jusqu'à elle : le + seul → l'Index à la première plantation → l'Aura au premier tenu (la
> main la désigne : `aura-apparait` est BRANCHÉ) → le Studio au premier retour sur l'accueil après l'Aura, avec une ligne → le Fil à la
> première parole adressée ou reçue. Rien ne disparaît ; rangée « Tout afficher » aux Réglages. **Qui n'a pas fait ce parcours voit tout,
> comme avant** (le dévoilement commence au bouton du principe).
> Juges : **`redteam_e2.py`** (53 : le parcours au vrai doigt, clair et sombre, les quatre « Plus tard », R6, A2, A3, E2bis) ;
> `redteam_engagement` 11/11 (**R6 est VERT**, il passe par `redteam_e2 --r6`) ; `redteam_verrou_onboarding` réécrit (9/9) ;
> `redteam_onboarding` passe la main à `redteam_e2` ; `redteam_gestes` (onze gestes branchés).
> ⚠ **Du principe au premier tenu : 2 touchers et 2 TRAITS** (planter est un trait, tenir en est un autre) — la consigne disait « 1 trait » (Q442).
> ⚠ **Trois pièges du lot** : ① la main « planter » se montrait sur la pastille VIDE, partait au toucher qui la remplit, et ne revenait plus
> (son drapeau était posé) : elle attend que la phrase porte ses mots ; ② une ligne posée dans `#device` passe SOUS une fiche (z-index 80) ;
> ③ une pastille sur deux lignes a un creux au milieu de sa boîte : un juge touche son premier rectangle (`getClientRects()[0]`).
> **Contrats de test RÉÉCRITS au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v140.py`) : `redteam_bord` F (des pointes, plus
> une limite franche) · `redteam_halo` (anneau 127–150, ombre à 391,2) · `releve-aura` (palier haut 110 000) · `redteam_dessin`,
> `redteam_dessin_photo` (22 pt, cibles de 44 pt, le partage emporte les photos) · `redteam_cadre` 7 (l'icône, plus le texte) · `redteam_accueil`
> (anneau 72, barre 710 → 810) · `redteam_toucher` (Ritournelle : chaque dalle entière et vue de près, plus « un cinquième de l'écran ») ·
> `redteam_engagement` R6 · `redteam_verrou_onboarding` · `redteam_gestes` (planter avec un titre, l'Aura qui paraît) · `redteam_onboarding`
> (remplacé ; il garde les aides que les deux précédents importent). `redteam_air` : référence REFIGÉE (720 paires ; les seules resserrées :
> le mot de trace de la page +, 5 pt vers le haut, comme demandé ; ancienne : `sauvegardes/air-reference-avant-v140.json`).
> ⚠ **Un juge qui devient un relais garde ce que d'autres importent** : `redteam_engagement` et `redteam_verrou_onboarding` font `from
> redteam_onboarding import …` — le relais, importé, lançait E2 et sortait : les deux juges rendaient « 53/53 », le chiffre d'un autre.
> **Trouvé en E2, corrigé** : ① après « tenir », la fiche disait « à moi » au lieu de sa phrase (l'instant réécrit la ligne, la signature
> `data-phrase` restait : on compare aussi le texte affiché) ; ② sur l'instant, un titre de DEUX lignes était recouvert par « TENUE · À
> L'INSTANT » (cote figée pour une ligne : elle descend de ce que le titre prend en plus).

### ⚑ v141 (10 oct. 2026) — RETOURS DE TOM SUR IPHONE : TROIS RÉCIDIVES (LA PELOTE, RITOURNELLE, LE MUR DU STUDIO), L'ONBOARDING D'AVANT v140, LE GUIDE DE FIN DE PARCOURS. (Décisions Tom.) Ce bloc CORRIGE v139, v140 (qui n'a pas de bloc ici), E2 / E2bis et v136 (C-084) là où ils disent autre chose.
> **Q439, Q441, Q442, Q445 validées. Q444 sans objet (E2bis est remplacé). Q449 : on ne plante plus de dalle sous la barre du bas.**
> **⚑ LA PELOTE (C-083, RÉCIDIVE). ① LE BORD EST CELUI DU PEINTRE D'AVANT v114** (`sauvegardes/app-avant-v114.html`) : les pointes telles que le
> peintre les pose, avec L'OPACITÉ DE LEUR TAMPON. *Pourquoi c'est revenu* : les deux peintres (canevas, carte graphique) posent les poils de
> la même façon (un tampon par poil, le plus opaque gagne) — ce n'est pas eux qui différaient, c'est ce que la COMPOSITION ajoutait après :
> la limite franche (v139), puis l'opacité des pointes resserrée et recolorée (v140). Tout cela est retiré. Restent : le corps opaque (v120),
> qui s'efface de **0,98 à 1,05 R** (à R → 1,012 R il faisait une marche : la frange se lisait comme un anneau pâle derrière un bord net),
> et la correction de COULEUR de v137–v138 (au-delà de 0,92 R, la couleur du vis-à-vis intérieur) — le corps est d'une autre teinte que le
> poil depuis v123, la peau d'avant v114 était de la couleur du poil. ⚠ Deux essais faits et vus, à ne pas refaire : le corps qui prend la
> teinte du poil au bord (anneau SOMBRE), les pointes à la couleur « poil sur corps » avec leur opacité (anneau PÂLE).
> **② LES POILS DU BORD SE COUCHENT DANS LE SENS OÙ LA PELOTE TOURNE** (`tour()`, `o.tour`, `uTour` ; du milieu du rayon — rien — au bord — tout ;
> 0,18 à la rotation de repos, jusqu'à 0,9 sur un lancer ; rien, vue figée). **③ L'ÉTOILE ET TOUT DESSIN GÉOMÉTRIQUE SONT RETIRÉS** : un appui ne
> pose plus AUCUNE trace, et au fond du creux les poils gardent leur sens (le peigne rayonnant convergeait sur un point). **④ LA TRACE EST LA
> SURFACE RÉELLEMENT TOUCHÉE, FORMÉE SOUS LE DOIGT** : tous les 10 pt de geste, la zone de contact du moment reçoit un arc de sa longueur, couché
> dans le sens où le doigt va, inscrit AUSSITÔT ; une zone de contact = UN arc (le dernier). Plus rien n'est posé au lâcher.
> *La règle* : **sur la Pelote, on ne corrige jamais un bord par l'opacité ; et une trace ne se dessine pas après coup, elle s'inscrit pendant le geste.**
> Juges : `redteam_trace` (réécrit : en direct, sans étoile), `redteam_bord`, `redteam_fourrure`.
> **⚑ RITOURNELLE (C-088, RÉCIDIVE — « trop dézoomé »).** Cibles sur 390 pt : **une parole → sa dalle ≥ 60 % de la largeur ; deux, trois, quatre →
> toutes entières ; au plus deux cellules vides entièrement visibles jusqu'à quatre paroles.** *Pourquoi c'est revenu* : v140 cadrait les
> GRAINES avec une marge ; une marge autour de points ne dit rien de la taille des dalles (50 % de la largeur à une parole ; 5 et 7 cellules
> vides entières à trois et quatre). Le moteur cadre maintenant la boîte des CELLULES des paroles à leur poids final (`_boiteSerre`), à 118 %
> de la largeur pour une parole, 100 % au-delà, entre le plateau et la barre ; l'amas des paroles monte plutôt qu'il ne s'étale.
> *La règle* : **un cadrage se calcule sur ce qu'on voit (la cellule), jamais sur des graines.** Juge : **`redteam_ritournelle.py`**.
> **⚑ Q449 — PLUS DE DALLE SOUS LA BARRE.** `plantOne` : borne basse = la barre (710) moins une dalle (0,87 cellule). *La cause du rouge* : une
> cellule REPLIÉE (une dalle partie) était reprise d'abord, sans passer par la zone dégagée (plantations mesurées à 716, 730, 815).
> **⚑ LE MUR DU STUDIO (C-100, RÉCIDIVE — « une fois sur quatre »).** *La cause* : le mur était fait de QUATRE BANDES (54, 19, 44 et 4 pt) ; entre
> elles et autour, le panneau n'était pas un mur. Le mur est LE PANNEAU (`#stpBas`). *Pourquoi les juges ne le voyaient pas* : ils touchaient
> le centre de chaque bande, sans glisser. *La règle* : **un mur est la surface qu'on voit floutée, pas la liste de ses éléments ; un juge de
> toucher répartit ses points sur toute la zone et fait glisser le doigt de quelques points.** Juge : **`redteam_murs_toucher.py`** (huit murs,
> vingt touchers chacun, 20 sur 20). Le bouton « Adopte ce design » n'est pas un mur. **Q447** : pendant la lecture d'une phrase sur le
> panneau des palettes, ses pastilles se retirent (`.mur-lu`).
> **⚑ L'ONBOARDING DE v140 EST RETIRÉ (C-075) : celui d'avant v140 revient EN ENTIER, mot pour mot** (prénom → parole → trait → message de fin →
> compte). `lot-E2` (le script) n'existe plus ; l'étape « principe » et ses textes non plus. Gardé de v140 : la main fantôme sur le trait
> (`onb-trait`), le mot de trace à 19 px, **« Plus tard » à chaque étape — en haut à droite, 12 px (le plancher du §6), sans soulignement**.
> « Toi, c'est ? » : la zone dégagée de la phrase prend toute la largeur. Juge : **`redteam_onb_sorties.py`** (textes EN DUR ; `--r6`).
> **⚑ LE GUIDE DE FIN DE PARCOURS REMPLACE E2bis (C-094 ; C-076 est abandonné par lui).** La barre est complète dès le départ. Une seule fois
> (`promi_guide`), 0,8 s après l'arrivée sur l'accueil d'un parcours COMPLET : un flou (`backdrop-filter:blur(4.8px)`, la valeur des murs) dont
> le MASQUE grandit par zones (1,5 s), net sur l'icône du Studio (× 1,2) — « Chacun sa matière. La tienne est au Studio. » ; la toucher ouvre
> le Studio ; au retour, net sur le + (× 1,1) — « Tout le reste part d'ici. » ; le toucher ouvre les trois natures. Toucher ailleurs ou
> « Plus tard » le dissout ; « Revoir la présentation » le rejoue ; mouvement réduit : posé d'un coup. `lot-V141-GUIDE`,
> `TEXTES_ENGAGEMENT.guide`. **C'est, avec les murs, le seul flou de l'app.** Juge : **`redteam_guide.py`**.
> **⚑ LE CRÈME DES FICHES (C-084) : `#EAD9B9` est RETIRÉ** (« trop beige ») — corps et encarts reprennent `#F7F0DE`, les cartes du fil d'un Cercle
> `#E9D8B7`. **Deux tons clairs dans l'app, pas trois.**
> **⚑ LA PAGE + ET LE TRAIT (C-095)** : « TRACE TA MOITIÉ » à quelqu'un, « TRACE POUR PLANTER » à soi. La main : × 1,3, contour doublé vers
> l'intérieur ; **sur une fiche elle part du MILIEU et suit les points, posés SUR l'onde — et le geste de tenir part aussi du milieu** (il
> faut alors aller presque au bout). Après « tenir » : **« C'est tenu. »** (avant : « Le dessin existe. »).
> **⚑ LA FICHE D'UN CERCLE (C-096)** : « + Planter dans le Cercle » reste la dernière ligne du fil mais se tient à 12 pt au-dessus du bandeau
> (`position:sticky`), le fil défile dessous ; dans Peaufiner il est sous COMMENTAIRES (672, 342 × 62, son + dans son rond), le reste
> remonte de 140 ; « Dissoudre le Cercle » n'a plus d'encart.
> **Aussi** : le partage d'une parole seule — une colonne, la case à 56 % de la largeur, centrée à 44 % de la hauteur (C-097) ; une photo se
> TOURNE à deux doigts, bande d'une fiche (`photoCadre.a`) et photo d'un dessin (`a`) — `redteam_tourne.py` (C-098) ; le bouton recadrer
> porte quatre coins, à 12 pt au-dessus de la barre (C-099). **Au registre, sans rien construire : déplacer une dalle sur sa Toile (C-101, v142).**
> ⚠ **PromiLate n'a pas de capitale accentuée : le É de « TRACE TA MOITIÉ » tombe sur la police suivante.**
> ⚠ **Deux juges flottent, inscrits au registre sans que le produit ait été retouché** : `redteam_fluide` (C-102 : des tâches de 249 à 979 ms après
> « tenir » sur trois passes sur quatre ; v140, dans la même série : 6/6 ; cause non nommée) et `redteam_decisions` sur le champ du Cercle (C-103 :
> il lit un pixel fixe où une dalle passe selon le tirage). **Le message de fin de l'onboarding** : la vue amène la première dalle à sa place d'avant
> (`Toile.vueVers`), puisqu'elle ne se plante plus sous la barre. `banc_rendu` et `redteam_air` sont REFIGÉS (places des dalles ; textes changés).

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

> ### ⚑ C-137 — RÈGLE PERMANENTE : PLUS JAMAIS DE VIDÉO (Tom, 15 oct. 2026, v147). Elle passe avant toute autre règle de travail.
> - **Aucune vidéo, aucun enregistrement ralenti, aucun GIF.** Ni dans les rapports, ni dans les lots, **même si un ancien brief en demande** :
>   cette règle les remplace (les vidéos demandées par les blocs v145 et v146 sont mortes).
> - **Tom regarde le mouvement lui-même sur son iPhone**, par les paramètres de ralenti (`?flaques=1`, `?mareeLent=4`, le curseur de vitesse de
>   `promi-trace-lettres.html`, etc.). **Le rapport donne le lien et le paramètre, rien d'autre.**
> - **Captures fixes : seulement quand une preuve ne peut pas se dire en chiffres. Trois au plus par lot, jamais une planche de huit images.**
> - **Un seul rapport, dans la réponse.** Pas de .md joint qui le répète.
> - **Mesures de cadence : seulement quand la charge du Mac est sous 4** (`sysctl -n vm.loadavg`). Au-dessus, on les reporte et on le dit en une ligne.
> - Les tailles et les espacements se donnent en pt.

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
python3 redteam_pleine.py      # v145 (C-112, RÉCIDIVE) : une Toile de 25 paroles relue de la sauvegarde (banc_tom.toile_pleine) — planter puis retirer : les COMPTES de rendus de vignettes pendant le mouvement (indépendants de la charge), le Fil et l'Index à jour ensuite ; les durées ne sont jugées qu'au calme (charge < 4). --port=8762 : rouge sur v144 (20/29).
python3 redteam_part.py        # 55 — v145 (C-115) : la règle de la part — 2, 3 et 5 personnes, tous les ordres ; part tracée pleine et verte, non tracée fine à la teinte de la nature (lu sur l'image), tenue seulement à la dernière ; initiales, « k SUR n », la liste au toucher du trait, la sauvegarde, l'Index. --sonde : il rougit. 2/8 sur v144.
python3 redteam_commentaires.py # 26 — v145 (C-116) : la ligne « Un mot… » sur une fiche reçue, joignable au doigt, la saisie, l'envoi, l'ordre du plus ancien au plus récent avec nom et date, la sauvegarde, aucun compteur ; clair et sombre. --sonde : il rougit. 2/8 sur v144.
python3 redteam_evol.py        # v144 (C-112, C-113) : la Toile quand une dalle arrive ou part (cinq mondes, planter puis retirer) et la Pelote sous le doigt — le travail de chaque rappel pendant le mouvement (≤ 20 ms), le recadrage qui ne passe plus à chaque image, l'écouteur du doigt qui ne recalcule plus un poil. --mondes=. Rouge sur v143.
python3 redteam_barre.py       # 7 — v143 (C-106) : cinquante touchers au vrai doigt sur ce qu'on voit de chaque entrée de la barre, chacun ouvre sa page ; les zones voisines ne se chevauchent pas. --n=20. Rouge sur v142 (STUDIO 17 sur 25).
python3 redteam_trait.py       # 11 — v143 (C-107) : un trait ne compte qu'à 60 pt — 30 pt refusé, doigt posé refusé, 70 pt lent et 70 pt rapide acceptés, pour tenir et pour planter ; la main montre plus de 60 pt. Rouge sur v142.
python3 redteam_partage_toile.py # 42 — v143 (C-105) : sous les vingt mondes, l'image que le vrai bouton produit (Enregistrer, Partager) est la Toile affichée : mêmes dalles, mêmes places, même cadrage, mêmes couleurs. Planche des écarts. --mondes=.
python3 banc_tom.py             # (un module, pas un juge) v142 — LE BANC « COMME TOM » : WebKit, 390 × 844, échelle 3, doigt, webdriver masqué, Toile vide, plantation par l'app. Tout juge d'un point visuel passe par lui.
python3 redteam_deplace.py     # 45 — v142 (C-101) : déplacer une dalle — appui 0,8 s, elle suit le doigt, place gardée après rechargement, jamais sous la barre, un toucher bref ouvre toujours la fiche ; cinq mondes. 5/9 sur v141 (--mondes=pochade).
python3 redteam_cercle_tom.py  # 16 — v142 (C-096) : la fiche d'un Cercle ouverte en touchant sa dalle sur la Toile : bandeau tout en bas, « + Planter » 12 pt au-dessus, le fil défile dessous ; « Dissoudre » sans encart. 6/16 sur v141.
python3 redteam_studio_tom.py  # 14 — v142 (C-100) : les murs du Studio au vrai toucher tactile WebKit, chemin réel, chaque zone floutée, 20 sur 20, phrase lisible. 10/14 sur v141.
python3 redteam_e2.py          # 53 — E2 et E2bis (v140, C-075, C-076) : le premier parcours au vrai doigt, stockage vierge (principe → vraie page + → trait → fiche → trait → dernière ligne → compte), clair et sombre ; les quatre « Plus tard » ; R6, A2, A3 ; la barre qui se dévoile. --r6, --vite. ≈ 6 min. ⚑ À PASSER À LA FIN DE CHAQUE LOT E.
python3 redteam_fourrure.py    # 9 — v140 (C-083) : LA FOURRURE D'AVANT LES ESSAIS — réglages en dur (densité ×1, poil ×1), pointes au-delà de la boule, pas d'anneau, rien autour. 5/9 sur l'état d'avant.
python3 redteam_trace.py       # 8 — v140 (C-083) : l'empreinte suit le vrai geste — deux trajets, deux traces alignées ; la largeur du contact ; l'étoile d'un appui. 2/8 avant.
python3 redteam_remplace.py    # 18 — v140 (C-086, C-085) : dessin → photo → dessin → photo sur la même fiche, sans reste (la bande au pixel). 8/18 avant.
python3 redteam_studio_mur.py  # 9 — v140 (C-092) : au Studio la phrase du mur paraît sur le panneau flouté, pour chacune des sept zones. 3/9 avant.
python3 redteam_guide.py       # v141 (C-094) : le guide de fin de parcours — stockage vierge, parcours complet au doigt, clair et sombre : flou 0,8 s après l'arrivée, seul le Studio net, puis le + ; toucher ailleurs, « Plus tard », rechargement, mouvement réduit, rejeu. --vite.
python3 redteam_onb_sorties.py # 27 — v141 (C-075) : l'onboarding d'avant v140, mot pour mot (textes en dur), « Plus tard » à chaque étape (12 px, sans soulignement), plus d'étape « principe », la main sur le trait. --r6 pour redteam_engagement.
python3 redteam_murs_toucher.py # 8 — v141 (C-100) : huit murs, vingt touchers répartis sur toute la zone floutée, doigt qui glisse : 20 sur 20. --seul=.
python3 redteam_ritournelle.py # 12 — v141 (C-088) : une parole ≥ 60 % de la largeur ; 2, 3, 4 entières ; au plus deux cellules vides entières. WebKit.
python3 redteam_tourne.py      # 8 — v141 (C-098) : une photo se tourne à deux doigts (bande d'une fiche, dessin), l'angle est mémorisé.
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
python3 redteam_ronds.py       # 40 — v148 (C-143) : aucun rond orange de signature (WebKit : l'animation battait l'opacité nulle), le chevron reste, aucune invitation animée (7 s). Rouge sur v147.
python3 redteam_ruban.py       # 36 — v148 (C-148) : plus de rectangle au seuil ; un ruban amande plein qui suit l'onde, 75–85 % de 118 pt, bords légèrement irréguliers ; le mot jamais coupé. WebKit. Rouge sur v147.
python3 redteam_ordre_guide.py # 26 — v148 (C-146) : au lancement le Studio ; trois touchers ailleurs = trois rappels (la phrase du Studio réécrite), jamais le + avant le Studio ; reprise au lancement ; Studio refermé avec ou sans changement → le +. Rouge sur v147.
python3 redteam_validation.py  # 25 — v149 (C-155, C-156) : du lever à la fiche tenue — seul, la dernière part, ma part seule (aucun rideau), tout le monde a tracé (le Fil,
                               #   « déjà vu »), première et seconde ouverture, rechargement ; la création (la dalle grandit dès l'image suivante) ; Q536 (rien de flou au doigt posé). WebKit. 8/25 sur v148.
python3 redteam_onb_mots.py    # 44 — v149 (C-153, C-124, C-145) : le I qui clignote (même code que l'accueil), Promi/Chiche/Cercle (couleur, gras) à chaque page, la ligne
                               #   « Tout le monde promet. Toi, tu tiens. », la phrase du guide sans recouvrement — clair et sombre, vrai parcours. 15/42 sur v148.
python3 redteam_titres_cartes.py # 10 — v149 (C-151) : un titre de deux lignes d'une carte d'Index n'est ni rogné ni collé à l'état, le plus petit pas qui tient. 6/10 sur v148.
python3 redteam_pages_plus.py  # 35 — v150 (C-157, C-158, C-149) : les pages + contre v149 servie à côté (hasard semé) — le mot du trait, la phrase, le rail,
                               #   « garder de côté » ; les fiches identiques au pixel ; la bascule des lignes sur dix ouvertures. Rouge sur v149.
python3 redteam_echeance.py    # 11 — v151 (C-160) : l'échéance est une date — planter « 5 j », ?jour=+30 → « à tenir » ; REPORTER au doigt depuis le Fil → « en cours » ;
                               #   tracer → « tenue » ; le retour au premier plan recompte ; « un jour » jamais « à tenir » ; ?jour jamais mémorisé. WebKit. 4/11 sur v150.
python3 redteam_clavier_onb.py  # 6 — v153 (C-164) : clavier simulé (visualViewport descend/remonte comme sur iOS) — après le prénom, plus de focus ; le premier tracé APRÈS le clavier redescendu ; sans clavier, rien n'attend. 3/6 sur v152.
python3 redteam_tenir_e3.py    # 6 — v153 (E3, C-077) : R4 (deux paroles qui diffèrent sur tout, même séquence lue sur les pixels du rideau ; durées au calme), le crochet promiHaptique, « Réduire les animations » (tenue d'un coup, sans fondu), tâches longues (au calme). --r4 pour redteam_engagement. 2/6 sur v152.
python3 redteam_mots_sombre.py  # 33 — v152 (C-162) : tout mot coloré en clair dans l'onboarding et le guide l'est aussi en sombre, ≥ 3:1 sur le fond lu sur l'image ; inventaire relevé ; deux exceptions nommées. WebKit. 29/33 sur v151.
python3 redteam_guide_fond.py  # 12 — v154 (C-166) : au retour du Studio (monde et palette changés au doigt), le fond flouté du guide = la Toile réelle
                               #   (≤ 0,2 % à plus de 6 niveaux), préparé SOUS le Studio ; sans changement, le même au pixel. WebKit. 8/12 sur v153.
python3 redteam_tenir_presse.py # 7 — v154 (C-167) : le vert remonte 2,25–2,7 s après le lever ; un toucher à 1,3 s le fait remonter tout de suite, avalé
                               #   (Peaufiner ne s'ouvre pas) ; un toucher à 100 ms ne presse rien. Lu sur les pixels du rideau. 1/7 sur v153.
python3 redteam_centre_validation.py # 8 — v155 (C-167) : la phrase de validation, lue sur les pixels de la nappe, centrée à ± 1 pt (Promi, Chiche, Cercle ; clair, sombre ; Safari réduit).
python3 redteam_curseur_couleur.py # 12 — v155 (C-168) : la dalle de la jauge s'attrape à 20 pt de son centre (cinq directions, sans saut), en noir et blanc aussi ; les voisins répondent. 3/12 sur v154.
python3 redteam_depart_orange.py # 34 — v155 (C-169, Q561) : pointe ET trait de départ orange sur les fiches à moitié tracées, les pages + (trois natures, deux thèmes) et l'onboarding ;
                               #   la flèche 1 000 ± 50 ms après le prénom ; le départ clignote avec le I (promiBlink, en phase) jusqu'au premier toucher ; rien ailleurs ; réduit : fixe.
python3 redteam_deverrouille.py  # 25 — v155 (C-170) : les douze mondes payants déverrouillés au doigt sur une Toile pleine : passage en flaques, aucun flou intermédiaire ;
                               #   la Toile de l'accueil déjà dans le nouveau monde à la fermeture du Studio, jamais l'image d'avant. --n=.
python3 redteam_achat_net.py   # 15 — v158 (C-170) : le vrai chemin d'achat sans compte, fenêtre de Safari ; aucune couche floutée ni voile au second encart, son entrée nette, la netteté locale de l'écran ; D : la situation qui trompait v157 (rouge sur v157).
python3 redteam_studio_saccade.py # 18 — v158 (C-175) : la jauge du Studio sous Mascaret, Touffe, Madrure, Houle — le travail compté pendant le glissé (teinte ≤ 1/image, aucune trame cachée, la dalle de la jauge) ; durées au calme. Rouge sur v157.
python3 redteam_suite_libelle.py # 21 — v158 (C-176) : le → de l'onboarding ne touche aucune ligne de texte, clavier ouvert et fermé ; les pages + ; la parole de cinq lignes rouge par décision (Q568).
python3 redteam_guide_studio.py # 7 — v157 (C-172) : deux designs choisis au Studio, aucune image du + tant qu'il est ouvert ; refermé, le + arrive ; la situation qui trompait le sondage, posée exprès. C rougit sur v156.
python3 redteam_croix.py       # 269 — v157 (C-173) : 34 écrans × 2 thèmes — aucun « FERMER » ; l'encre du X (lue sur l'image) = capitale du titre ± 1 pt ; sa couleur ; zone 44 × 44 prise à ses coins. ≈ 7 min.
python3 redteam_fleche_onb.py  # 12 — v157 (C-174) : contre v156 servie à côté — le haut de l'encre au même pt, hauteur × 2, rien de touché, le départ clignote à 1,5 s.
python3 redteam_achat_fond.py  # 49 (v157 : + D, E le second encart sur le Studio NET ; F « Design débloqué » en amande) — v156 (C-170, C-171) : l'encart d'achat ouvert depuis les douze mondes payants du Studio floute la Toile du Studio (pas l'accueil), en flaques,
                               #   préparé au toucher ; le second encart aussi ; « Plus tard » répond. Rouge sur v155.
python3 redteam_onb_rejeu.py   # 10 — v151 (C-159) : le rejeu de l'onboarding (Réglages, au doigt) sur une Toile d'une et de dix dalles dit le texte de Tom ; Toile vide → le texte
                               #   d'origine ; le reste de la chorégraphie inchangé (trois touchers). WebKit. 8/10 sur v150.
python3 redteam_decoupe.py     # ⚑ v148 : il reconnaît le moteur servi avec son empreinte (`promi-moteur.js?v=…`, depuis v145 ses appels retombaient sur une ligne d'app.html) et le peintre des îles de la Pelote (`dalleLisible`, appelé par la préparation au repos de l'Aura, C-135).
python3 redteam_veille.py      # 16 — v161 (C-181) : la veille — départ (jamais en saisie ni en geste), l'écran exact au retour sans rien actionner, une couleur par rebond, l'amande au coin seul et aucun coin avant 60 s, le logo dans l'écran, le verrou à 10 min, réduire les animations, 30 × 2 h simulées, coupée sur le banc. ≈ 5 min ; --vite.
python3 redteam_guide_fleche.py   # 80 — v166 (C-203 §2) : la flèche orange vers le Studio, le + et Partager — orange, axe vers l'icône ± 10°, aucun recouvrement, pointe au bord de la zone nette, fixe, partie à la phrase 2 ; deux thèmes, deux échelles.
python3 redteam_veille_depart.py # 5 — v167 (C-181 §3) : l'état de Tom, WebKit, sans ?veille : la veille part à 60 s ± 1 s après le dernier toucher (vrais PointerEvent) sur l'accueil, une fiche + un mur du Peaufiner, l'Index, le Fil, l'Aura. Rouge sur v166.
python3 redteam_guide_cloture.py # 130 — v165 (C-203) : la clôture du guide — chemins a, b, c, Partager touché ou non, la zone nette lue sur l'eau, la fin, le lancement suivant ; deux thèmes, deux échelles.
python3 redteam_v164b.py        # 31 — v164b : TRIER (Index, Fil, deux thèmes) et les huit points de C-200, au doigt. 8/31 sur v164a.
python3 redteam_ramage_jauge.py  # v164b (Q581) : la silhouette de Ramage prête à l'accueil ; aucun rendu ni image > 50 ms dans les 5 s après l'arrivée (au calme). Rouge sur v164a.
python3 redteam_photo_trait.py  # 56 — v164a (C-201) : le bouton photo et sa zone de toucher au-dessus de l'encre du trait (lue sur le canevas), 3 pages + et 4 fiches, ×1,15 à ×1,8, échelles 1 et 0,79.
python3 redteam_trait_k.py      # v164a (C-184) : `?trait=` 1,3 · 1,5 · 1,8 et le défaut (v163a : 1,10 · 1,15 · 1,20) — épaisseurs × K/1,05, l'air flèche → mot ≥ v162 (lu sur l'image), aucun recouvrement neuf, 430 × 932 et 330 × 714 ; l'onboarding au pixel. ≈ 20 min.
python3 redteam_veille_bords.py # 15 — v163a (C-181) : l'encre du logo au bord visible ± 1 pt, quatre bords, trois fenêtres ; flaques 350 ms. Rouge sur v162.
python3 redteam_garde_index.py  # 6 — v163a (C-149, Q579) : le pointillé 3 pt #291547 / #A77CF7 lu sur l'image ; le message ouvre l'Index filtré. Rouge sur v162.
python3 redteam_recadre_bouton.py # 16 — v163a (C-188) : le symbole seul, 22 pt, sa place, sa zone de 44, naissance et départ en flaques, 4 s, le double toucher.
python3 redteam_menu_tri.py     # 8 — v163a (Q578) : un toucher hors du menu ⇅ le referme (Index et Fil), dans le panneau non, une option agit. 4/8 sur v162.
python3 redteam_appartient.py   # 12 — v163a (C-165) : « t'appartient. » lettre par lettre, chaque couleur ΔE ≤ 12 et ≥ 3:1, deux thèmes, deux échelles. Rouge sur v162.
python3 redteam_tenu_trait.py   # 7 — v163b (C-189) : une parole ne se tient que par le trait — aucun TENIR au Fil, aucune réaction ✧, les seuls écrivains de « tenu ».
python3 redteam_avant_acheter.py # 4 — v163b (C-190) : « Avant d'acheter » a « Plus tard » et se ferme au toucher dehors, sans rien acheter.
python3 redteam_tri_menus.py    # 7 — v163b (C-191) : le Fil trie et filtre au doigt, plus de #fdSort ni de QUADRILLAGE, « À tenir », le repère en barrette. 2/7 sur v162.
python3 redteam_peauf_rangees.py # 12 — v163b (C-192) : Dissoudre et Pièces jointes branchés au doigt, COMMENTAIRES et les rangées en double retirés.
python3 redteam_pile_retour.py  # 10 — v163b (C-193) : le X rend l'écran d'où l'on vient (Index, Fil, personne, Cercle, Réglages, Aura), Peaufiner seul. 1/10 sur v162.
python3 redteam_tout_effacer.py # 10 — v163b (C-195) : un « Tout effacer » (feuille, 5 s), « Se déconnecter » avec un compte seulement, l'action à l'encre.
python3 redteam_pinceau_rail.py # 8 — v163b (C-196) : le rail défile (débordement, pan-x, scrollLeft), les traits payants sont un mur.
python3 redteam_audit_v163.py   # 24 — v163b (C-194, C-197, C-198, C-199) : les mots d'un rôle, les murs du Studio, les petites corrections de l'audit. 1/24 sur v162.
python3 redteam_parole_longue.py # 144 — v160c (C-180) : la parole longue de l'onboarding, 1 à 6 lignes, 40 lettres, 260 et 500 caractères, deux échelles, deux thèmes, clavier ouvert et fermé. Rouge sur v159.
python3 redteam_studio_arrivee.py # 3 — v160c (C-175) : à l'arrivée sur Ramage, aucun rendu de la silhouette ; elle vient au calme ; Pochade inchangé. Rouge sur v160b.
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
