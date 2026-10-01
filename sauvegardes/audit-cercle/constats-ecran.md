# LE CERCLE — CONSTATS À L'ÉCRAN (notes de travail, 11 sept. 2026, session 458111e3)
App `48b1a56b6b4b58f425dbd7a84e0b9f1f`. Outil `audit_ecran.py` (430 × 932, DPR 2 → #device 390 × 844). Captures :
`ecran/<thème>_<mode>_<surface>.png`. Chaque ligne ci-dessous a été VUE sur la capture nommée — pas lue dans le code.
Les chiffres (couleurs, tailles) viennent de `analyse_audit.py` une fois le relevé fini.

## Vu, confirmé
1. **Page du Cercle (#plusScreen) = l'ancienne page, intacte.** `*_plus_*_haut/bas.png`. Titre « Essaie tout, sans
   t'engager. » à x ≈ 6 (hors de la marge de 24) ; grande tache en fond (#plHeroCv) ; « soit près de cinq mois offerts » ;
   mois en primaire, année en secondaire ; halo lumineux sous « Essayer 14 jours » ; cinq glyphes ⟷ ◔ ✳ ◈ ◐ ;
   « Stats avancées », « Toiles signature », « Rappels intelligents » ; « ou un design à l'unité — 1 €, ou 4 pour 3 € ».
2. **EN CLAIR, LA PAGE DU CERCLE N'AFFICHE NI SES PRIX NI SES BOUTONS.** `light_gratuit_plus_openPlusTop_haut/bas.png` :
   « 3,99 €/mois » et « 29 € » (les <b> du sous-titre), « ta » et « l'inverse » : crème sur crème. Bouton « Essayer 14
   jours, puis 3,99 €/mois » : texte crème sur fond crème. Bouton « Prendre l'année — 29 € » : idem ; seul « soit 2,42
   €/mois · −39 % » (bleu) se lit. Contours des boutons presque invisibles.
3. **Un abonné est renvoyé sur la même page de vente** (« Essayer 14 jours… ») par #cercleTopBtn et #openPlusTop.
   `dark_cercle_plus_cercleTopBtn_haut.png`.
4. **« ✦ Membre du Cercle ✓ / tout Promi débloqué · merci » s'affiche en GRATUIT** sur les réglages floutés dès que le
   Cercle a été actif une fois puis retiré (`light_gratuit_reglages.png`, passage qui suit `dark_cercle`). Cause lue
   l. 3132 : `setPremium(true)` réécrit l'encart, `setPremium(false)` ne le rend jamais. Chez un vrai abonné l'encart est
   masqué (`cerclePaye`) : la mention n'est JAMAIS vue par celui à qui elle s'adresse.
5. **Réglages, gratuit :** encart « ✦ Le Cercle / débloque tout Promi · essai 14 jours » (pas le sous-titre du §3.8) ;
   texte de l'encart avec un halo en sombre (`dark_gratuit_reglages.png`). « Réinitialiser (test) — toile vide + 1… »
   visible dans le produit.
6. **Abonné : les quatre réglages défloutés sont inertes et portent des valeurs figées** (« · ·· ··· », « chaque
   semaine », « la veille à 19:00 », « réveille tes « en l'air » »), identiques d'un Promi à l'autre. (CORRIGÉ : l'écart
   de 104 px avant « Supprimer ce Promi » est la cote de l'inventaire, Q13 — présente en gratuit aussi, pas un trou.) `dark_cercle_peauf_promi.png`,
   `*_cercle_reglages.png`. → l'abonné paie pour quatre réglages qui ne règlent rien.
7. **Peaufiner Promi / Chiche, gratuit : le bloc du §3.8 est conforme à l'œil** (quatre réglages floutés, encart net,
   crème en sombre / encre en clair, texte dans la teinte de la nature — #FFC0A8 sur un Chiche en clair).
8. **Peaufiner d'une Nuée : aucun bloc du Cercle** (Q17, voulu). `dark_gratuit_peauf_nuee.png`.
9. **Studio, monde payant (Terrazzo, Gravure), gratuit :** Toile et palette floutées ; « Adopte ce design — 1 € » AU REPOS
   (Q106 : au doigt seulement), texte avec un halo en sombre ; « Ou débloque-les tous / avec Le Cercle » (Q117 non
   appliqué : « ✦ Le Cercle / sillons, gravure, terrazzo », « Adopte Terrazzo — 1 € ») ; « avec Le Cercle » gris pâle.
   Abonné : Terrazzo ouvert, aucun signe. `*_studio_terrazzo.png`, `*_studio_gravure.png`.
10. **Aide « i » de l'Aura :** badge « Avec le Cercle » + encart #ahCercleCta « Vois la parole qu'on te tient / en douceur ·
    et ce qui circule entre vous » en DÉGRADÉ bleu-orange-rose avec halo ; cartes du dessous floutées bien au-delà de 2,4.
    Décrit l'ancienne Aura (Q185). `*_aura_aide.png`.
11. **L'Aura (l'Orbite) n'a rien du Cercle** : aucune porte, aucun second anneau, aucun graphe — 0 occurrence de
    « Cercle » / `premium` dans les trois blocs `lot-AURA-ORBITE`. `dark_gratuit_aura.png`.
12. **Fiche d'une personne : aucun mode Cercle** (un seul anneau). « comment ça évolue » : à confirmer (complément D).
13. **Page + :** le rail du pinceau montre les payants en pointillé, sans prix au repos. Le Peaufiner de la page + n'a
    pas été ouvert par le premier passage (mauvaise porte : `.dpd-tog` au lieu de `#csBotBar`) → complément A.
    Lecture du code : `peaufBati` n'y accroche AUCUN bloc du Cercle (CSS présent, montage absent).
14. **Accueil :** #cercleTopBtn (anneau + point) en tête, à côté des Réglages : porte directe vers la page de vente.

## Relevé chiffré (analyse_audit.py, juge corrigé : dégradé / canevas / texte recouvert NON JUGÉS)
- page du Cercle, clair : « 29 € », « 3,99 €/mois », « ta », « l'inverse », #buyYear : rgb(231,229,223) sur #F4EEE1,
  **contraste 1,09** ; #buyMonth : blanc sur #F4EEE1, **1,16**. #plusScreen et .enh-voile : x −16 → 406 (le piège §8).
  #buyMonth : ombre portée rgba(58,84,255,.3) 0 12 30. « ou un design à l'unité » : opacité 0,70.
- encart du §3.8 en sombre : #AE86F2 sur crème **2,42** (Promi, Réglages) ; #F2977A sur crème **1,92** (Chiche) —
  CE SONT LES VALEURS DE LA SPEC (§3.8, tables l. 2479 / 2622). Conflit spec ↔ lisibilité : question.
- Réglages : texte de l'encart avec ombre de texte rgba(20,8,40,.55) 0 1 10 (le halo) ; Studio : #stBuyTx, .sc-t,
  .sc-s, flèches avec la même ombre ; « avec Le Cercle » opacité 0,66.
- aide « i » : #ahCercleCta en dégradé (120° / 152°) + ombre portée ; badge « Avec le Cercle » dégradé + ombre ;
  #ahLocked **flou 7 px** ; textes à 0,49 / 0,60 d'opacité ; illustrations en dégradés radiaux.

## Portes et achats (audit_ecran.py + audit_complement.py + repro_etats.py)
- #cercleTopBtn → page de vente, **aussi pour un abonné** (2 thèmes) ; visuel du haut VIDE (0 % peint) quand c'est la
  première porte de la séance (A9 : le gestionnaire n'appelle pas drawCercleHero).
- #openPlusTop, .s2-encart, #ahCercleCta, #stLockCta → page de vente en gratuit ; masqués pour un abonné.
- réglage flouté touché en gratuit : le doigt tombe sur l'encart → page de vente. Abonné : touché, rien ne change.
- #karmaCercle : 0 × 0 partout (mort). **#resetApp « Réinitialiser (test) » donne le Cercle** (premium=true).
- **#buyYear / #buyMonth : premium=true, AUCUN débit, ouvre l'Aura (qui n'a rien du Cercle), perdu au rechargement.**
- **#stLockBuy (1 €) : monde adopté, aucun débit, perdu au rechargement** (owned [] et monde encre après reload).
- **P1 reproduit (page neuve, vrais boutons) : gratuit sur Terrazzo → débloque-les tous → Prendre l'année → Studio
  rouvert : Encre VERROUILLÉ, « Adopte ce design — 1 € » servi à un abonné.** Classes world-locked + stp-verrou.
- P2 (Encre verrouillé après Terrazzo, en gratuit) NON reproduit sur page neuve : artefact de mon enchaînement.
- Studio : « eclats » n'a aucune porte (8 mondes, conforme Q102).
- Partage (fiche et dock) : aucun ✦, aucun « Cercle », aucun flou — Q113 tenu.
- Page + : Peaufiner ouvert par #csBotBar → À QUI · AVANT · DANS UNE NUÉE · NOTE · PIÈCES JOINTES ; **aucun bloc du
  Cercle** (le CSS existe, copie mécanique de la fiche — QUESTIONS l. 1346 ; le moodboard ne dessine pas cet écran).
- Fiche d'une personne : « comment ça évolue » ABSENT en gratuit ET au Cercle (Q183 le mettait au Cercle : il n'est nulle part).
- **Pinceau : aucun Promi ne garde son pinceau** (gratuit ou payant) — `window.promises` indéfini (`let promises`,
  l. 2856) dans lot-PINCEAU l. 24234. Hors Cercle → tâche à part. Choisir un payant ne coûte rien, aucun prix à la page +.

## Revenu hors de la carte (trouvé à la lecture, à confirmer au complément B)
- **8 pinceaux à 0,50 € pièce** (`_PINCEAU_META`, l. 24009 : Tressé, Frangé, Doublé, Fendu, Cranté, Vrillé, Semé,
  Perlé ; 4 libres). « — 0,50 € » écrit dans Peaufiner (l. 24353, 24521). Aucun paiement dans le code : choisir suffit ?
- **Designs à l'unité : 1 €, ou 4 pour 3 €** (page du Cercle) ; l'adoption à 1 € (`#stLockBuy`) ne débite rien, ne
  persiste pas (à confirmer par les achats).
- **Codes couleur de la palette au Cercle** : PLANCHE-STUDIO (« Au Cercle, les quatre couleurs prennent leur code »),
  absent de l'app.
