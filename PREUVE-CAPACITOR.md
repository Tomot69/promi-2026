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
| Compilation pour l'iPhone de Tom | **bloquée** : la session du compte Apple de Tom dans Xcode a expiré (« Unable to log in with account »), Xcode ne peut pas créer le profil de `fr.autier.promi.preuve`. L'identité de signature (équipe B77VBMD9BF) est sur le Mac ; l'iPhone 16e est appairé, mode développeur activé. **Tom se reconnecte dans Xcode › Réglages › Comptes** (mot de passe : lui seul). |

## Les mesures (en attente de l'iPhone de Tom)

Cinq minutes d'usage, relevé allumé : la Toile sous quatre mondes (Mascaret compris), le tracé et le détracé (onboarding, guide), la genèse de la page +,
la Pelote, le défilement d'une fiche. Comparées au relevé Safari de Tom (`mesures/2026-11-15-1635.jsonl` et les précédents) par animation : p50, p95,
images de plus de 33 ms.

| Critère pour continuer | Résultat |
|---|---|
| Fluidité au moins égale à Safari, sur chaque animation | en attente |
| Rendu identique (polices, couleurs, flaques) | simulateur : polices chargées, onboarding vu à l'œil identique ; **pas comparé au pixel** (l'app est en plein écran, Safari a ses barres : l'échelle de l'appareil diffère) ; sur l'iPhone : en attente |
| Vibration ressentie à « tenir » | en attente |
| Notification reçue, app fermée | **tenu au simulateur** ; sur l'iPhone : en attente |

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

**En attente des mesures sur l'iPhone de Tom** : la fluidité (le critère qui décide) et la vibration ne se jugent que là. Ce qui est établi au simulateur :
la v205 s'emballe sans une ligne changée, compile en app iOS, ses polices se chargent, l'ouvrier du tracé y est prouvé, le relevé arrive au Mac, et une
notification locale arrive app fermée. Rien, à ce stade, ne contredit Capacitor ; rien ne le prouve encore sur la fluidité.
