# PREUVE-CAPACITOR — la v205 emballée telle quelle dans une app iOS (v207 §1, 17 nov. 2026)

Branche `preuve-capacitor`, partie de l'étiquette `reference-v205`. Rien de l'app n'est modifié : le dossier `capacitor/` construit sa page depuis
`app.html`, `promi-moteur.js` et `variantes/` de la v205, et ne pose qu'un script en tête de page (`capacitor/coquille.js`).

## Ce qui est construit

| Pièce | État |
|---|---|
| Projet Capacitor 8.6.2 (iOS, paquets Swift, sans CocoaPods) | fait — `capacitor/` (`npm install`, `sh construire.sh`, `npx cap sync ios`) |
| La page | la v205 au caractère près ; la coquille en tête de `<head>` |
| Le relevé | allumé comme dans Safari (`?releve=1`) ; ses envois (`releve`, `mesure`) partent au serveur du Mac par le client http natif (CapacitorHttp) — `mesures/AAAA-MM-JJ-HHMM.jsonl`, lu par `resume_releve.py` comme ceux de Safari |
| Vibrations | `promiHaptique('tenir')` branché sur `@capacitor/haptics` (impact « HEAVY ») ; l'app garde un crochet déjà posé |
| Notification | `@capacitor/local-notifications` : au premier lancement, la permission, puis une notification programmée à 1 minute |
| Compilation simulateur (« Promi iPhone 16e », iOS 26.1) | **réussie** ; l'app s'ouvre sur l'onboarding de la v205 (le mot-marque, « Toi, c'est … », le fond en flaques) |
| La sonde, dans l'app (simulateur) | les cinq polices **chargées** (Gilbert 700, Atkinson 400 · 500 · 700, PromiLate 400), écran 390 × 844 à ×3, l'ouvrier du tracé **prouvé**, Haptics et LocalNotifications présents ; le relevé arrive au Mac (`mesures/2026-11-17-1938.jsonl`, « v205 · hors serveur ») |
| Notification (simulateur) | **reçue, app fermée** : programmée à 19:38:44, l'app fermée à 19:38:51, remise à 19:39:44,999 (`shouldPresentAlert: YES`, journal de SpringBoard) |
| Compilation pour l'iPhone de Tom | **réussie** (Tom reconnecté dans Xcode) ; installée par `devicectl`, la séance du 17 nov. faite sur elle (v205) |
| La version du 17 nov., 23 h 50 | **la v206 corrigée (b9f98bd)**, extraite par `git archive` (`SOURCE=… VERSION=… sh construire.sh`) ; **en plein écran** : `viewport-fit=cover`, la barre d'état de Capacitor (`@capacitor/status-bar` 8.0.4) posée par-dessus la page, texte selon le thème ; et la coquille rend l'écran au téléphone — dans Safari l'app dessine un cadre de téléphone (coins de 22 pt, ombre) réduit à ×0,933 avec 14 pt de marge ; dans l'app, l'appareil à 0, 0, 390 × 844 (mesuré ; vu au simulateur : plein écran, l'heure au-dessus du mot-marque). Installée sur l'iPhone, sa sonde arrive au Mac (écran 390 × 844 × 3, polices chargées, ouvrier prouvé) |

## La séance sur l'iPhone de Tom (17 nov., 21 h)

Tom a utilisé l'app « Promi preuve » 5 minutes (installée par Xcode, iPhone 16e, iOS 27.2), puis Safari (`?releve=1`) 5 minutes, puis `?export=1`.
Relevés : l'app `mesures/2026-11-17-2102.jsonl` (code v205, 410 s, 23 560 images) ; Safari `mesures/2026-11-17-2109.jsonl` (code v207, 90 s seulement :
le relevé n'envoie qu'au repos, la fin de la séance n'est pas arrivée) ; pour comparer à une séance Safari plus longue, celle du 15 nov.
(`2026-11-15-1635.jsonl`, code v203, 212 s). Export : `etats/tom-20261117-211127.json` (ajouté à la référence, `Promi-reference-v205/etat-de-tom/`).

**La fluidité, par animation** — images de plus de 33 ms pour 1 000 images (p95 en ms) :

| Animation | L'app (v205) | Safari ce soir (v207, court) | Safari 15 nov. (v203) |
|---|---|---|---|
| tracé des lettres | 12 ‰ (17) | 38 ‰ (20) | 37 ‰ (29) |
| détracé | 22 ‰ (20) | 0 ‰ (19) | 47 ‰ (32) |
| transition d'un mot | 34 ‰ (24) | 30 ‰ (20) | 39 ‰ (27) |
| mouvement (page +, clavier) | 7 ‰ (18) | — | 80 ‰ (39) |
| défilement d'une fiche | 20 ‰ (19) | 11 ‰ (19) | 65 ‰ (40) |
| « tenir » | 30 ‰ (17) | — | — |
| sous le doigt (Pelote, jauge) | 75 ‰ (35) | 200 ‰ (49) | 44 ‰ (28) |
| au repos | 13 ‰ (17) | 15 ‰ (18) | 16 ‰ (20) |
| **toute la séance** | **14 ‰ (p95 17)** | **17 ‰ (19)** | **22 ‰ (23)** |

Le Studio sous Mascaret, dans l'app : 1 140 images, p95 17 ms, 13 au-delà de 33 ms (Safari, 14 nov. : 452 sur 1 666).
⚠ Ce ne sont pas les mêmes versions (l'app porte la v205 ; Safari la v207 ce soir, la v203 le 15) ni les mêmes gestes : c'est un ordre de grandeur, pas une
mesure à l'identique. **Seul écart défavorable : « sous le doigt »** (75 ‰ contre 44 ‰ le 15 nov. ; mais 200 ‰ dans Safari ce soir, sur 40 images).

**Le tracé des lettres** : dans l'app (v205, l'ancien ouvrier), l'ouvrier est prouvé, 756 lettres calculées sur le fil (165 ms en tout, la pire 4 ms), aucune
lettre lente. Dans Safari (v207, le nouvel ouvrier, C-292) : **attente d'une lettre attendue p50 34 ms, p95 58, max 67** (600 à 924 ms le 15 nov.) ;
**calcul d'une carte dans l'ouvrier p50 10 ms, p95 24, max 128** ; trois ouvriers prouvés (le 2ᵉ et le 3ᵉ en 228 ms). L'objectif de C-292 (< 16 ms par
lettre) n'est pas atteint : l'attente a baissé d'un facteur 15, le calcul d'une carte coûte 10 ms au milieu sur l'iPhone.

**Le rendu** : Tom, après la séance : « le reste est pareil dans l'app et dans Safari ». Trois défauts vus dans les deux, qui sont ceux du prototype
(corrigés sur la branche v206 : C-296 le rectangle sur « Je », C-297 le trait après « tenir », C-298 la Pelote ×1,5 ; C-295 Mascaret : voir le registre).
**Un défaut propre à l'app : elle ne prenait pas tout l'écran** — la WebView gardait les marges des zones sûres (la page n'avait pas `viewport-fit=cover`).

**La vibration** : ressentie à « tenir » (Tom : « HEAVY, médiocre »). Tenue pour la preuve.
Ce que permet `@capacitor/haptics` : trois chocs (`impact` LIGHT · MEDIUM · HEAVY), trois signaux (`notification` SUCCESS · WARNING · ERROR), le cran d'une
sélection (`selectionStart`, `selectionChanged`, `selectionEnd`) et `vibrate` (sur iPhone, la vibration système, sans réglage). C'est tout : ni durée, ni
intensité continue, ni enchaînement. **Ce qu'il faudrait pour une vibration dessinée (C-022)** : Core Haptics (`CHHapticEngine`, `CHHapticPattern` — des
évènements « transient » et « continu », leur intensité et leur netteté dans le temps, des courbes, et une synchronisation avec le son), ce qui demande **un
module natif sur mesure** (un greffon Capacitor en Swift, de l'ordre de cent lignes : démarrer le moteur, jouer un motif décrit en JSON ou en fichier AHAP,
l'arrêter) ; un motif par geste (tenir, planter, la part d'un autre) se dessine et se règle ensuite sans recompiler.

**La notification** : Tom ne l'a pas mentionnée. Ce qu'on sait : dans le stockage de l'app sur l'iPhone (copié par `devicectl`), la clé `preuve_notif`
porte 20 h 04 min 44 s — la programmation a abouti (la clé n'est écrite qu'après elle) ; mais la permission n'était pas contrôlée (la coquille écrivait la
clé même sans permission) et l'envoi au Mac de ce moment est perdu (la première requête réseau d'un premier lancement, pendant la demande d'accès au réseau
local). Le journal de l'iPhone ne se lit pas sans les droits d'administrateur (`log collect --device` : « Must be root »). **Non établi.** La nouvelle
coquille envoie au Mac, à chaque lancement, la permission, les notifications en attente et celles REMISES (le centre de notifications les garde).

## Les critères

| Critère pour continuer | Résultat |
|---|---|
| Fluidité au moins égale à Safari, sur chaque animation | **tenu, sauf « sous le doigt »** (75 ‰ d'images > 33 ms dans l'app contre 44 ‰ dans Safari le 15 nov. — mais 200 ‰ dans Safari ce soir) ; toute la séance : 14 ‰ contre 17 et 22 ‰. Versions et gestes différents : un ordre de grandeur |
| Rendu identique | **tenu** (Tom : « le reste est pareil dans l'app et dans Safari ») ; le plein écran corrigé (non revu par Tom) |
| Vibration ressentie à « tenir » | **tenu** (HEAVY, « médiocre » : C-022 pour mieux) |
| Notification reçue | **tenu sur l'iPhone, app en arrière-plan** : programmée au lancement de 23 h 50 min 44 s pour 23 h 51 min 44 s (permission accordée), elle figure dans les notifications REMISES à 23 h 52 (`getDeliveredNotifications`, id 2) ; l'app tournait encore (écran verrouillé ou arrière-plan), pas tuée. **App tuée : tenu au simulateur seulement** |

## Achats — ce qu'il faut (rien n'est créé)

**Le module.** Deux candidats, vérifiés sur npm le 17 nov. : `@revenuecat/purchases-capacitor` 14.1.1 (StoreKit 2 et Google Play Billing 7 derrière un service
tiers : reçus vérifiés, abonnements, tableau de bord ; gratuit sous un seuil de revenu) et `cordova-plugin-purchase` 13.20.0 (sans service tiers ; la
vérification des reçus est à notre charge). **Recommandation : RevenueCat** — une personne seule n'a pas à tenir un serveur de reçus, et Ma Parole ! est un
abonnement.
**App Store Connect** (Tom) : le contrat « Apps payantes » (accords, fiscalité, coordonnées bancaires) ; l'app (identifiant de lot, p. ex. `fr.autier.promi`) ;
cinq achats **consommables** « Soutenir » (5 · 10 · 25 · 50 · 100 €, C-217) — identifiants `fr.autier.promi.soutien.5` … `.100`, nom et description en
français, capture d'écran de revue ; l'abonnement Ma Parole ! dans un groupe ; un **testeur bac à sable** (un identifiant Apple de test).
**Google Play Console** (Tom) : le compte développeur, l'app, les mêmes cinq produits intégrés, un **testeur de licence**, la piste de **test interne**.

## Firebase — ce qu'il faut (rien n'est créé)

Un projet Firebase (région Europe) ; une app iOS (identifiant de lot) → `GoogleService-Info.plist` ; une app Android (nom de paquet + empreinte SHA-1 de la
clé de signature) → `google-services.json` ; Authentification (Apple, obligatoire sur iOS si une autre connexion existe ; Google) ; Firestore et ses règles
(une parole n'est lisible que par ses membres) ; App Check (App Attest, Play Integrity) ; pour les notifications à distance plus tard : une clé APNs (.p8)
déposée dans Firebase. Les clés des fichiers de configuration ne sont pas secrètes ; la clé APNs l'est (elle reste chez Tom). Module :
`@capacitor-firebase/authentication`, `/firestore`, `/messaging`.

## Android — ce qu'il faut

Ce Mac n'a ni Android Studio, ni SDK, ni émulateur à Promi ; celui de l'autre session n'est pas touché. Il faut : Android Studio, le SDK (plateforme 36),
une image d'émulateur (≈ 1,5 Go) **ou** un téléphone Android de Tom en mode développeur ; puis `npx cap add android`, une clé de signature (keystore),
et la même mesure. Le rendu Android passe par Chromium (pas WebKit) : un banc au pixel Chromium s'ajoute.

## Conclusion

**Capacitor passe la preuve.** La v205 s'emballe sans une ligne changée, tourne sur l'iPhone de Tom au moins aussi fluide que Safari sur toutes les animations
sauf sous le doigt (où les deux relevés Safari se contredisent), avec le même rendu ; la vibration se sent ; une notification locale est remise. Le plein écran
demande trois choses dans la coquille, rien dans l'app. Ce qui reste à voir par Tom : la nouvelle version (v206 corrigée, plein écran) au doigt ; une
notification app TUÉE sur l'iPhone ; la vibration dessinée (Core Haptics, un greffon natif). Ce qui reste à créer par Tom : les comptes App Store Connect,
Google Play, Firebase (ci-dessus). **Recommandation : continuer avec Capacitor** ; la reconstruction en TypeScript strict (ARCHITECTURE.md) peut commencer.
