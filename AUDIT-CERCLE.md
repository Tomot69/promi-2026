# AUDIT — LE CERCLE, NŒUD PAR NŒUD, À L'ÉCRAN

> Mesuré le 11 septembre 2026 sur `app.html` **`48b1a56b6b4b58f425dbd7a84e0b9f1f`** (non modifié par cet audit), servi en
> 8752, viewport **430 × 932** (le `#device` sort exactement à 390 × 844 — CLAUDE §8), DPR 2, onboarding passé,
> **deux thèmes × deux modes** (gratuit / Cercle payé). La carte `sauvegardes/audit-cercle/carte-lecture.md` était une
> LECTURE du code : chaque ligne ci-dessous a été vue à l'écran ou mesurée, et la capture qui la prouve est nommée.
>
> **Outils** (tous dans `sauvegardes/audit-cercle/`) : `audit_ecran.py` (10 surfaces, 5 mondes du Studio, 7 portes,
> les achats et le rechargement — 83 captures) · `audit_complement.py` (le Peaufiner de la page +, un pinceau payant
> planté, le partage, la fiche d'une personne, un réglage touché) · `repro_etats.py` (les fuites d'état rejouées SEULES,
> sur page neuve, par les vrais boutons) · `analyse_audit.py` (chaque nœud visible contre le §6). Journaux entiers
> `*.log`, relevés `ecran/*.json`, notes de travail `constats-ecran.md`.
>
> **Rien n'est supprimé, rien n'est corrigé.** L'audit constate. Il porte du revenu : chaque commande est nommée pour
> ne pas se perdre au dessin.

---

## 0 · EN UNE PAGE

**Le Cercle tel qu'il est aujourd'hui ne peut pas être vendu.**

1. **En thème clair, la page du Cercle n'affiche ni ses prix ni ses boutons** — contraste **1,09** et **1,16**.
2. **Rien n'est payé, rien n'est gardé** : les deux achats et l'adoption à 1 € donnent tout, et tout se perd au rechargement.
3. **Quand le Cercle s'arrête, on garde le monde payant** — et on perd le monde gratuit qu'on avait choisi.
4. **Ce qu'on paie ne fait rien** : les quatre réglages, défloutés, sont inertes et portent des valeurs figées ; l'Aura
   (la Pelote) ne connaît pas le Cercle — zéro occurrence dans ses trois blocs.
5. **L'abonné est traité en prospect** : on lui revend l'essai, et le Studio lui sert « Adopte ce design — 1 € » sur Encre.
6. **La page du Cercle est l'ancienne, intacte** : « près de cinq mois offerts », le mois en premier, halo, glyphes,
   titre hors marge. Aucun des mots de Q165, aucune ligne de la planche du 3 septembre n'y est.

Ce qui tient : **le bloc du §3.8 sur le Peaufiner d'un Promi et d'un Chiche** (quatre réglages floutés à 2,4, encart net,
couleurs de la spec) ; **le partage ne porte aucun signe du Cercle** (Q113) ; **Éclats n'a aucune porte** (Q102).

---

## A · LES SURFACES, NŒUD PAR NŒUD

### A1 · La page du Cercle — `#plusScreen` (hors `#device`, sous `.frame`)
Captures `*_plus_cercleTopBtn_{haut,bas}.png`, `*_plus_openPlusTop_{haut,bas}.png`.

| nœud | ce qu'il porte | gratuit | Cercle | état mesuré |
|---|---|---|---|---|
| `.closeb` + plateau | « Le Cercle · ✕ FERMER » | ✓ | ✓ | vivant |
| `#plHeroCv` (688 × 344, affiché 390 × 195) | visuel : une tache + un anneau à rayons | ✓ | ✓ | **vide (0 % peint) si la page est ouverte par `#cercleTopBtn` en premier** (son gestionnaire, l. 3177, n'appelle pas `drawCercleHero`) ; dégradé |
| `.pl-eb` | « Le Cercle » | ✓ | ✓ | vivant |
| `.pl-h` | « Essaie tout, / sans t'engager. » | ✓ | ✓ | **x ≈ 6 : hors de la marge de 24** ; « sans t'engager » en bleu |
| `.pl-sub` | « Tout Promi pour **3,99 €/mois**, arrête quand tu veux. Ou prends l'année : **29 €**, soit près de cinq mois offerts. » | ✓ | ✓ | **forme de prix interdite** ; **en clair, les deux montants en gras sont invisibles** : rgb(231,229,223) sur #F4EEE1, **1,09** |
| `.pl-feat` × 5 | ⟷ La parole qu'on te tient · ◔ Rappels intelligents · ✳ Nuées illimitées · ◈ Stats avancées · ◐ Toiles signature | ✓ | ✓ | glyphes hors langue ; « ta » et « l'inverse » invisibles en clair (1,09) ; ⟷ à 2,10 en clair |
| `#buyMonth` (primaire) | « Essayer 14 jours, puis 3,99 €/mois » | ✓ | ✓ | **en clair : blanc sur crème, 1,16 — illisible** ; ombre portée rgba(58,84,255,.3) 0 12 30 |
| `#buyYear` (secondaire) | « Prendre l'année — 29 € · soit 2,42 €/mois · −39 % » | ✓ | ✓ | **en clair : « Prendre l'année — 29 € » à 1,09 — seul « soit 2,42 €/mois · −39 % » se lit** |
| `.pl-note` | « Sans engagement · annulable en 2 taps, à tout moment. » | ✓ | ✓ | vivant |
| `.pl-note` | « ou un design à l'unité — 1 €, ou 4 pour 3 € » | ✓ | ✓ | opacité **0,70** ; **aucun achat « 4 pour 3 » n'existe nulle part** |
| `#plusScreen`, `.enh-voile` | — | | | **x −16 → 406** (un `.screen` ne coïncide pas avec `#device`, §8) |

**Aucun cadre du moodboard ne dessine cette page.** Sa seule référence dessinée est la planche du 3 septembre
(`PLANCHE-AURA-TROIS-PARTIS.html`, captures `scratchpad/partis/09.png` et `10.png`), jamais intégrée.

### A2 · Le bloc du §3.8 — Peaufiner d'un Promi et d'un Chiche (`cercle()`, l. 16273)
Captures `*_peauf_promi.png`, `*_peauf_chiche.png`.

| nœud | gratuit | Cercle |
|---|---|---|
| 4 × `.s2-reg` — C'EST IMPORTANT ? · ·· ··· / RÉCURRENCE chaque semaine / RAPPEL la veille à 19:00 / LA MÉMOIRE réveille tes « en l'air » | floutés **2,4 px**, `pointer-events:none` — conforme | **défloutés, touchables, INERTES** : toucher RÉCURRENCE ne change rien (complément E) ; **valeurs figées, les mêmes sur tout Promi** |
| `.s2-encart` « ✦ Le Cercle / importance, récurrence, rappels, mémoire » | net, posé dessus, ouvre la page — conforme | masqué. (L'écart de 104 px avant « Supprimer » est la cote de l'inventaire, Q13 l. 556, présente aussi en gratuit — pas un trou. Une première lecture l'avait pris pour un vide laissé par l'encart : retiré.) |
| couleurs de l'encart | crème en sombre, encre en clair, texte dans la teinte de la nature — **conforme à la spec**. Mais **#AE86F2 sur crème = 2,42 ; #F2977A sur crème = 1,92** (voir §F, question) | — |
| toucher un réglage flouté | le doigt tombe sur l'encart → **ouvre la page de vente** | — |

**Pas de bloc sur une Nuée** (Q17, voulu — `*_peauf_nuee.png`). **Pas de bloc sur le Peaufiner de la page +** : ouvert
par sa vraie porte (`#csBotBar`), il porte À QUI · AVANT · DANS UNE NUÉE · NOTE · PIÈCES JOINTES, et rien du Cercle,
dans les deux thèmes et les deux modes (complément A, `*_pageplus_peauf_{haut,bas}.png`). Son CSS existe
(`#createSheet.pp-peauf .s2-cercle`) mais c'est une copie mécanique de celui de la fiche (QUESTIONS l. 1346) : rien
n'indique qu'il ait jamais été monté, et le moodboard ne dessine pas cet écran.

### A3 · Réglages — `#settingsScreen`, `#openPlusTop` (`cercleReglages()`, l. 16427)
Captures `*_reglages.png`, `repro_P4_*`.

| nœud | gratuit | Cercle |
|---|---|---|
| quatre réglages du bloc | floutés 2,4 — conforme | défloutés, inertes, valeurs figées |
| encart `#openPlusTop` | « ✦ Le Cercle / débloque tout Promi · essai 14 jours » — **pas le sous-titre du §3.8** ; ombre de texte rgba(20,8,40,.55) 0 1 10 (le halo) | **masqué** : « ✦ Membre du Cercle ✓ / tout Promi débloqué · merci », écrit par `setPremium(true)`, **n'est jamais vu par un abonné** |
| **après la fin du Cercle** | **« ✦ Membre du Cercle ✓ » s'affiche en GRATUIT** sur les réglages floutés — `setPremium(false)` ne rend jamais le texte (reproduit P4, deux thèmes) | — |
| `#resetApp` « Réinitialiser (test) · toile vide + 1… » | visible dans le produit — **et il DONNE le Cercle** (`setPremium(true)`, mesuré) | idem |

### A4 · Le Studio — `#studioScreen`, `#stLock`
Captures `*_studio_{terrazzo,gravure,sillons,encre}.png`, `repro_P1_*`, `repro_P3_*`.

| nœud | gratuit, monde payant | Cercle |
|---|---|---|
| la Toile, la palette | floutées — conforme au geste de Q105 bis | nettes |
| `#stLockBuy` | « Adopte ce design — 1 € » **au repos** (Q106 : au doigt seulement) ; **libellé tiré au hasard** parmi trois ; ombre de texte | masqué |
| `#stLockCta` | « Ou débloque-les tous / avec Le Cercle » — **Q117 non appliqué** (« ✦ Le Cercle / sillons, gravure, terrazzo », « Adopte Terrazzo — 1 € ») ; « avec Le Cercle » opacité 0,66 | masqué |
| `#stpNom` | « Terrazzo ✦ » — le ✦ sur le nom du monde | idem |
| **après un achat** (P1, deux thèmes) | — | **Studio rouvert : Encre VERROUILLÉ, flou, « Adopte ce design — 1 € » servi à un abonné** — `world-locked` et `stp-verrou` survivent |
| **après la fin du Cercle** (P3, deux thèmes) | **la Toile reste en Terrazzo, le Studio l'ouvre sans verrou** : le monde payant est gardé | — |
| **fin du Cercle sur un monde gratuit** (P5) | Mosaïque → **Encre** : `setPremium(false)` ne rétablit Encre QUE depuis mosaïque et pixel — la logique est **inversée** | — |

Huit portes de monde, **aucune pour Éclats** (Q102 tenu). **Aucun code couleur** de palette au Cercle
(`PLANCHE-STUDIO.html` : « Au Cercle, les quatre couleurs prennent leur code ») — dessiné, jamais intégré.

### A5 · L'Aura, son aide, la fiche d'une personne
- **L'Aura (la Pelote) n'a rien du Cercle.** Aucune porte, aucun second anneau, aucun graphe, aucune réciprocité ;
  `Cercle`, `premium`, `prem-only` : **0 occurrence** dans `lot-AURA-PELOTE`, `-CSS`, `-MOTEUR`. Après un achat, la page
  du Cercle ouvre… l'Aura (`#souffleBtn.onclick()`, l. 3134), où rien n'a changé. `*_aura.png`.
- **L'aide « i »** (`#auraHelp`) : badge « Avec le Cercle » en dégradé + ombre ; `#ahCercleCta` « Vois la parole qu'on te
  tient / en douceur · et ce qui circule entre vous » en **dégradé** (120° / 152°), **ombre portée**, **ombre de texte** ;
  six cartes sous **flou 7 px**, textes à **0,49 / 0,60** d'opacité. Elle décrit l'ancienne Aura (« Le double Noyau &
  la Pelote », « Les graphs par Nuée »…) — Q185. Masquée pour un abonné (l'encart), le reste demeure. `*_aura_aide.png`.
- **`#karmaCercle`, `#demoTg`** : 0 × 0 dans les quatre passages — morts avec l'ancienne Aura (Q176 confirmé).
- **La fiche d'une personne** : aucun mode Cercle ; **« comment ça évolue » n'existe plus, ni en gratuit ni au Cercle** —
  Q183 l'envoyait au Cercle, il n'est nulle part (complément D).

### A6 · L'accueil et le partage
- `#cercleTopBtn` (anneau + point, en tête, à gauche des Réglages) : **la porte la plus visible du produit** — elle mène à
  la page de vente, **abonné compris** (deux thèmes).
- **Partage, depuis une fiche et depuis le dock : aucun ✦, aucun « Cercle », aucun flou** (complément C). Q113 tient.

---

## B · CE QUE LE CERCLE DÉBLOQUE VRAIMENT — mesuré

| ce qui est vendu ou prévu | où | état |
|---|---|---|
| **Sillons · Gravure · Terrazzo** | Studio | **VIVANT** — le seul déblocage réel. Mais gardé à la fin (P3), et le verrou survit à l'achat (P1) |
| importance · récurrence · rappels · mémoire | Peaufiner, Réglages | **AFFICHAGE SEUL** : défloutés, inertes, valeurs figées (Q16 le disait : « un affichage, pas une fonction ») |
| « La parole qu'on te tient » / réciprocité / second anneau (§2.9) | Aura, Noyaux | **ABSENT** — la Pelote ne le connaît pas ; l'ancienne Aura qui le portait est masquée |
| graphes · évolution · « Nuée par Nuée » | Aura | **ABSENT** de l'Aura actuelle ; « comment ça évolue » retiré de la fiche d'une personne sans être reposé ailleurs |
| « Stats avancées » · « Rappels intelligents » · « Toiles signature » | page du Cercle | mots de l'ancienne page, retirés par Q165 — toujours à l'écran |
| « Nuées illimitées » | page du Cercle | **gratuites** (DECISIONS A11) — la page vend ce qui est offert |
| aide « i » floutée | Aura | décrit ce qui n'existe plus |
| « 300 dalles au Cercle » (spec §10.2) | Toile | absent |
| codes couleur de la palette | Studio (planche) | absent |

**Un abonné paie donc pour trois mondes, et pour rien d'autre qui fonctionne.**

---

## C · LES PORTES — touchées au point, dans les deux thèmes

| porte | gratuit | Cercle |
|---|---|---|
| `#cercleTopBtn` (accueil) | → page de vente (visuel vide si première porte) | **→ page de vente** |
| `#openPlusTop` (Réglages) | → page de vente | masquée |
| `.s2-encart` (Peaufiner Promi / Chiche) | → page de vente | masquée |
| un réglage flouté | → page de vente (le doigt tombe sur l'encart) | touchable, **ne fait rien** |
| `#ahCercleCta` (aide « i ») | → page de vente | masquée |
| `#stLockCta` (Studio, monde payant) | → page de vente | masquée (sauf P1 : resservie à tort) |
| `#stLockBuy` (Studio) | adopte le monde, **aucun débit** | masquée (sauf P1) |
| `#buyYear` / `#buyMonth` | **Cercle donné, aucun débit**, ouvre l'Aura | — |
| `#resetApp` | **Cercle donné** | — |
| `#karmaCercle`, `#demoTg`, `.nqh-cercle`, `#plusCta`, `#pplusBanner`, `#openPlus` | morts (0 × 0 ou absents) | — |

⚠ Limite dite : les portes ont été touchées **à la souris, au point de l'élément** (`elementFromPoint` puis clic), pas
au vrai doigt. Le balayage au doigt du 11 septembre (`sauvegardes/aura-trois/balayage_fantome.py`) couvrait déjà les
Réglages, le Studio et les Peaufiner : 0 écart doigt / souris. La page du Cercle elle-même n'y était pas.

---

## D · L'ARGENT — ce qui existe, ce qui se perdrait

**Rien n'est jamais débité, rien n'est gardé.** `isPremium` n'est pas écrit dans `localStorage` (clés présentes :
`promi_state`, `promi_theme`, `promi_monde`, `promi_sigdemo`, `promi_pelote_*`) ; `_ownedDesigns` non plus. Mesuré :
achat de l'année, du mois, adoption d'un monde → **tout est perdu au rechargement.** C'est attendu d'un prototype
(CHANTIERS 17 : paiement par feuille native, à venir ; 26 : avis juridique requis) — mais c'est à écrire, pas à supposer.

**Les six sources de revenu que l'app porte ou dessine — aucune ne doit se perdre au dessin :**

| # | source | prix | où | état |
|---|---|---|---|---|
| 1 | Le Cercle, à l'année | **29 € · soit 2,42 €/mois · −39 %** (forme de Tom) | page du Cercle | secondaire aujourd'hui, et mal écrit |
| 2 | Le Cercle, au mois | 3,99 €/mois, 14 jours d'essai | page du Cercle | primaire aujourd'hui |
| 3 | **un monde à l'unité** | **1 €** | Studio (`#stLockBuy`) | vivant, sans débit |
| 4 | **quatre mondes pour 3 €** | **3 €** | seulement la note de la page du Cercle | **aucun achat ne l'implémente** ; « quatre » alors qu'il n'y a que trois mondes payants (Q102) |
| 5 | **huit pinceaux à l'unité** | **0,50 € pièce** — « hors du Cercle » (PLANCHE-STUDIO) | page +, Peaufiner (`_PINCEAU_META`, l. 24009) | **choisir un pinceau payant ne coûte rien** ; aucun prix à la page +, « — 0,50 € » dans Peaufiner seulement. Et (hors Cercle) **aucun Promi ne garde son pinceau** : `window.promises` est indéfini (`let promises`, l. 2856) dans `lot-PINCEAU` l. 24234 — tâche à part |
| 6 | codes couleur au Cercle | (dans le Cercle) | PLANCHE-STUDIO seulement | non intégré |

**Le chiffre de −39 % est juste** : 29 / (3,99 × 12 = 47,88) = 0,606. « Près de cinq mois offerts » aussi
(18,88 / 3,99 = 4,7) — mais c'est la forme interdite.

---

## E · LES DÉFAUTS, DU PLUS GRAVE AU MOINS GRAVE — tous vus, tous reproductibles

| # | défaut | preuve |
|---|---|---|
| 1 | **Prix et boutons d'achat invisibles en thème clair** (1,09 / 1,16) | `light_*_plus_*.png`, `analyse_audit.log` |
| 2 | **Fin du Cercle : le monde payant reste** sur la Toile et s'ouvre au Studio sans verrou | `repro_P3_*` |
| 3 | **Fin du Cercle : un monde gratuit (Mosaïque, Pixel) est ramené à Encre** — logique inversée, l. 3119 | P5 |
| 4 | **Fin du Cercle : « ✦ Membre du Cercle ✓ » affiché en gratuit** | `repro_P4_*` |
| 5 | **Après l'achat, le Studio sert « Adopte ce design — 1 € » sur Encre à un abonné** | `repro_P1_*` |
| 6 | **L'abonné est renvoyé sur la page de vente** par la porte de l'accueil | `*_cercle_plus_cercleTopBtn_*` |
| 7 | **Ce qu'on paie ne fait rien** : réglages inertes et figés ; l'Aura ignore le Cercle ; l'achat mène à l'Aura | §B |
| 8 | **La page vend l'offert et le retiré** : Nuées illimitées (gratuites), Stats avancées, Rappels intelligents, Toiles signature, « près de cinq mois offerts » | A1 |
| 9 | **« Réinitialiser (test) » donne le Cercle**, visible dans le produit | A3 |
| 10 | **Interdits du §6** : dégradés (aide « i », visuel de la page), ombres portées (#buyMonth, #ahCercleCta, badge), ombres de texte (encarts Réglages et Studio), **flou 7 px** (aide), opacités 0,49 / 0,60 / 0,66 / 0,70, glyphes ⟷ ◔ ✳ ◈ ◐, titre hors marge | `analyse_audit.log` |
| 11 | **Visuel vide** si la page est ouverte d'abord par l'accueil | portes, héros 0 % |
| 12 | **Q106 et Q117 non appliqués** au Studio (prix au repos, libellé tiré au hasard, « Ou débloque-les tous ») | A4 |
| 13 | **« comment ça évolue »** retiré de la fiche d'une personne sans être reposé au Cercle (Q183) | complément D |
| 14 | l'encart des Réglages ne porte pas le sous-titre du §3.8 | A3 |

---

## F · LE BRIEF DE TOM, POINT PAR POINT

| consigne | aujourd'hui |
|---|---|
| **On voit quoi, jamais combien** | ✓ aucun compteur, aucun « il vous reste » — sur toutes les surfaces relevées. Mais la page du Cercle **dit** (cinq arguments écrits) et ne **montre** rien |
| **Réglages en place, floutés à 2,4, encart net dessus — la seule superposition** | ✓ Peaufiner Promi / Chiche, Réglages. ✗ aide « i » (flou 7, et un encart qui n'est pas celui du §3.8). ✗ page du Cercle : n'emploie pas la mécanique |
| **Aucun logo Cercle sur ce que les autres voient** | ✓ le partage n'en porte aucun (Q113). Les ✦ restants sont tous sur des écrans à soi (encarts, nom du monde au Studio) |
| **Quatre réglages** — importance, récurrence, rappels, mémoire | dessinés, jamais fonctionnels |
| **Trois mondes payants** | ✓ Sillons, Gravure, Terrazzo — le seul contenu vivant |
| **Les blocs d'Aura : graphes, évolution, réciprocité** | **n'existent pas dans l'Aura actuelle** (la Pelote) : ils sont à DESSINER dans l'Aura avant de pouvoir être montrés voilés sur la page |
| **Le chiffre d'harmonie, s'il revient** | absent de l'Aura actuelle (qui porte une phrase : « Rien de ce qui est ici n'a été dit à la légère. ») ; « harmonie 67 » est la forme de Q166, à confirmer |
| **29 € · soit 2,42 €/mois · −39 %, jamais « 2 mois offerts »** | ✗ la forme juste n'existe qu'en sous-titre du bouton secondaire, et elle est invisible en clair (sauf « soit 2,42 €/mois · −39 % ») ; « près de cinq mois offerts » en tête |

---

## G · CE QUE L'AUDIT NE TRANCHE PAS

> **⚠ En partie périmé (14 sept. 2026)** : bloc du Cercle à la page + posé, « 4 pour 3 € » gelé (Q206), codes couleur tranchés (Q213), réciprocité intégrée (Q215), « Réinitialiser (test) » retiré. Ce qui reste : `CHANTIERS.md` § « État au 14 septembre ».

- **L'encart du §3.8 en sombre** : la spec impose le texte dans la teinte de la dalle sur crème — #AE86F2 (2,42 de
  contraste), #F2977A sur un Chiche (1,92). CHANTIERS §10 dit « terracotta et mauve ne passent pas en texte sur fond
  clair ». Le moodboard fait foi, mais les deux règles se contredisent ici : **question à Tom.**
- **Le Peaufiner de la page + porte-t-il le bloc ?** La règle « un réglage vit là où vit ce qu'il règle » range
  importance, récurrence et rappels à la création ; le moodboard ne dessine pas cet écran.
- **« Quatre pour 3 € »** alors que trois mondes seulement sont payants ; les pinceaux sont-ils dans le Cercle
  (la planche du Studio les dit « hors du Cercle ») ; les codes couleur sont-ils au Cercle.
- **Ce que font les quatre réglages une fois payés** (la mémoire, les rappels, la récurrence) : ce sont des fonctions
  (CHANTIERS 18), pas du dessin.
- **Paiement réel** : feuille native, TTC, durée, reconduction dans l'encart (CHANTIERS 17), avis juridique (26).
