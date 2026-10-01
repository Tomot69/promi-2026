# AUDIT — L'AURA ET LE CERCLE

> Mesuré le 3 septembre 2026 sur `app.html` servi en 8752, viewport 390 × 844, `device_scale_factor 2`,
> onboarding passé, dans les deux thèmes et **dans les deux modes** (`setPremium(false)` / `setPremium(true)`).
> Outil : `scratchpad/aura_audit.py` + relevés au navigateur. Trois écrans concernés :
> **`#auraScreen`** (450 nœuds), **`#auraHelp`** (12 cartes), **`#plusScreen`** (la page du Cercle).
>
> **Rien n'est supprimé par cet audit.** Il constate. Ce qui est mort est nommé pour être
> ressuscité ou enterré sciemment ; ce qui est vivant est nommé pour ne pas se perdre.

---

## A · L'INVENTAIRE DE L'AURA — vingt-et-un blocs, dans l'ordre du défilement

| # | nœud | ce qu'il porte aujourd'hui | gratuit | Cercle | état |
|---|---|---|---|---|---|
| 1 | `.closeb` | ✕ FERMER | ✓ | ✓ | vivant |
| 2 | `h2.scr-t` + `#auraInfoBtn` | « Aura » + le **i** qui ouvre `#auraHelp` | ✓ | ✓ | vivant |
| 3 | `.keyebrow` | « ta parole dans le temps » | ✓ | ✓ | vivant |
| 4 | `.k-intro` | `.lbl-free` « ton harmonie envers les autres » / `.lbl-prem` « votre harmonie, des deux côtés » | ✓ | ✓ | vivant, **bascule** |
| 5 | `#demoTg` | **Aperçu gratuit / Aperçu membre** — deux boutons de démonstration | ✓ | ✓ | vivant · *hors produit* |
| 6 | `#ringLeg` | « au centre · ce que je tiens » / « l'anneau · ce qu'on me tient » | — | ✓ | vivant |
| 7 | `#auraSeal` | le Noyau : anneau à 3 arcs, rayons, **le mot** (« solide ») + **HARMONIE** + **67 %** | ✓ | ✓ (2ᵉ anneau) | vivant |
| 8 | `.klegend` | tenues · en cours · à tenir | ✓ | ✓ | vivant |
| 9 | `#kCount` | **6 tenues · 6 en cours · 3 à tenir** | ✓ | ✓ | vivant |
| 10 | `#kDelta` | **« ↑ en hausse cette semaine »** / « ↓ à tenir » / « ± stable » | ✓ | ✓ | vivant |
| 11 | `#souffleLine` | la phrase d'accompagnement (4 formulations selon le taux) | ✓ | ✓ | vivant |
| 12 | `#kBalance` | barre **5 envers toi ⟷ 10 envers les autres** | ✓ | ✓ | vivant |
| 13 | `#kEquilibre` | curseur **toi 80 % ⟷ eux 33 %** + « tu portes un peu plus en ce moment » | — | ✓ | vivant |
| 14 | `#kLens` + `#kchart` + `#kxaxis` | **Évolution · Répartition · Composition** — le graphe | ✓ | ✓ | vivant |
| 15 | `#kBestNue` | **« ❃ le potager installée »** — *ta meilleure Nuée* | ✓ | ✓ | vivant · **cul-de-sac** |
| 16 | `#kessaims` | **par Nuée** : nom · N Promi · sparkline · **60 %** · « se tisse » · déplie la liste | — | ✓ | vivant |
| 17 | `#kpers` | **grille d'anneaux par personne** ; en Cercle, **deux** anneaux (toi / elle) | ✓ | ✓ | vivant |
| 18 | `.pp-leg` | légende « toi envers eux » / « eux envers toi » | — | ✓ | vivant |
| 19 | `#kTogether` | **6 promesses tenues qui vous lient** | — | ✓ | vivant |
| 20 | `#ksocial` | **la Pelote** : toi au centre, `MARION 100 %`, `ADRIEN 50 %`, `RACHEL 33 %` | voilé | ✓ | vivant |
| 21 | `#karmaCercle` | l'encart « Le Cercle — vois la parole qu'on te tient » | ✓ | masqué | vivant |

---

## B · CE QUI EST MORT — six blocs, et deux d'entre eux sont calculés pour rien

**Mesuré `display:none` ou `0 × 0` ou absent, dans les DEUX modes.** Ce n'est pas un
verrouillage du Cercle : passer premium ne les rend pas.

| nœud | ce qu'il portait | ce que c'est |
|---|---|---|
| **`#kEvolve`** | *l'évolution Nuée par Nuée*, 6 groupes, couleur + taux par Nuée | **ABSENT DU DOM.** `buildAura()` compose son `innerHTML` en entier et le jette : `if($('#kEvolve'))$('#kEvolve').innerHTML=…`. Le garde `if` masque la panne depuis. |
| **`#plusCta`** | le bouton d'achat historique du Cercle | **ABSENT DU DOM.** Son gestionnaire est écrit et inatteignable : `$('#plusCta').onclick=()=>{_premium=true; … toast('Le Cercle débloqué · Nuées illimitées')}`. |
| **`#kStats`** | **en cours · résolues · série** (6 · 9 · 5) | `display:none` en gratuit **et** en Cercle. La **série** n'existe nulle part ailleurs — elle est calculée (`streak`) et perdue. |
| **`#kLegend`** | la légende propre au graphe (en cours / tenues / à tenir) | `display:none` dans les deux modes. Le graphe n'a donc **aucune légende** : `#kchart` sort sans clef de lecture. |
| **`#kPct` / `.kbig`** | le **grand chiffre** en Fraunces | `display:none` posé **en dur dans le HTML**. Le % affiché vient d'ailleurs (`.ku-pct`, dans `#auraSeal`). Deux sources pour un seul chiffre. |
| **`.klabel`** | « de ta parole tenue » | `display:none` en dur. Le sous-titre du grand chiffre est parti avec lui. |

**Une commande promise sans porte** — `#auraHelp` annonce en gratuit **« Partager mon Noyau ·
Exporte une belle image de ton Noyau »**. Le mode existe bien côté partage
(`#shareScreen [data-mode=noyau]`, restauré au lot du partage), **mais l'Aura ne porte aucun
bouton de partage** : `#auraScreen [class*=share]` → **0 nœud**. C'est le même défaut que le
mode « Noyau seul » du partage, à l'envers : la fonction existe, la porte manque.

---

## C · LES HUIT RÈGLES ANTI-NOTATION, CONFRONTÉES À L'ÉCRAN

| règle | état | ce qui la viole, mesuré |
|---|---|---|
| 1 · **aucun chiffre attaché à une personne** | ❌ | `#ksocial` écrit `MARION 100 %`, `ADRIEN 50 %`, `RACHEL 33 %` — en **8 px**, sous chaque visage. `#kEquilibre` écrit `toi 80 %` / `eux 33 %`. |
| 2 · **un seul chiffre, le tien, global** | ❌ | il y en a **au moins sept** à l'écran : 67 % (Noyau), 6 · 6 · 3 (`#kCount`), 5 · 10 (`#kBalance`), 80/33 (`#kEquilibre`), 60 %/75 % (`#kessaims`), 3 × % (`#ksocial`), 6 (`#kTogether`). |
| 3 · **ce qui est mesuré à deux est symétrique** | ~ | la structure l'est (`toi` / `eux`), mais le **verdict** ne l'est pas : « tu portes un peu plus en ce moment » désigne un porteur et un porté. |
| 4 · **aucun agrégat par personne** | ❌ | `#kpers` donne un **mot par personne** (« rayonnante », « naissante ») ; `#ksocial` un **taux par personne** ; `#kessaims` un **taux par Nuée**. |
| 5 · **aucun tri par valeur** | ❌ | `#kBestNue` est un **superlatif** — *ta meilleure Nuée* — obtenu par `sort((a,b)=>keptOf(b)-keptOf(a))[0]`. Et dans `#ksocial`, **le rayon de la Pelote encode la valeur** : un classement dessiné, sans être écrit. |
| 6 · **aucun événement négatif notifié** | ✓ | rien ne notifie. Mais `#kDelta` **écrit** « ↓ à tenir » quand ça baisse : la mauvaise nouvelle est affichée, pas notifiée. |
| 7 · **grille d'anneaux, jamais liste de barres** | ❌ | `#kessaims` est **exactement une liste de barres** : une rangée par Nuée, une sparkline, un taux à droite. `#kchart` en mode *Composition* aussi. |
| 8 · **visible de toi seul** | ✓ | rien de l'Aura ne sort de l'appareil aujourd'hui — faute de porte de partage (§B). |

**Verdict :** six règles sur huit sont enfreintes, et **cinq le sont en GRATUIT**.
C'est bien le point de Tom : l'écran gratuit, tel qu'il est, **note**.

---

## D · LA LANGUE — ce qui s'écarte du §6 et du lexique

```
MOTS       « Ta meilleure Nuée » (superlatif)  ·  « Stats avancées » (page du Cercle)
           « Les graphs » (fiche d'aide)  ·  « % de parole tenue »  ·  « HARMONIE 67 % »
           « tu compares où ta parole tient le mieux » (fiche d'aide, en toutes lettres)
```

| écart | mesuré |
|---|---|
| **textes sous 12 px** | 10 nœuds. `#kLens` : **10 px** (Évolution / Répartition / Composition). `#ksocial` : **11 px** (initiales) et **8 px** (les taux). |
| **opacités sous 72 %** | `#auraInfoBtn` **0,42** · `.ku-pc` (le signe %) **0,55** · `.pl-note` **0,70**. |
| **hors des six faces** | `#auraInfoBtn` est en **Georgia italique 600**. |
| **dégradé** | `#karmaCercle` : `linear-gradient(135deg, #242A5E, #2A2352, …)`. `.tuto-fond` : quatre `radial-gradient` + un `linear-gradient` de fond, sur les trois écrans. `#plHeroCv` peint un dégradé. |
| **ombre portée** | `#karmaCercle` : `rgba(58,84,255,.3) 0 12px 34px`. `#buyMonth` : `box-shadow`. |
| **ombre de texte** | `.ku-pct` (le 67 %) porte **deux ombres décalées** — terracotta et bleu — pour un effet de relief. |
| **flou hors norme** | le §3.8 écrit **2,4 px**. `#ksocial` est à **`blur(6px)`**, `#auraHelp .ah-locked` à **`blur(7px)`**. |
| **débordement** | `.enh-voile` de la page du Cercle : **x −16, largeur 422** dans un appareil de 390 (le piège du §8 : un `.screen` ne coïncide pas avec `#device`). |
| **recouvrement** | le plateau est fixe, la liste défile **sous** lui sans être rognée : la courbe de `#kchart` se voit **au-dessus** du plateau. C'est le piège connu de l'enfant absolu d'un conteneur qui défile. |
| **césure** | en Cercle, `Par personne · toi et eux, dans les deux sens` **casse sur deux lignes et se chevauche**. |

---

## E · LA PAGE DU CERCLE — ce qu'elle vend

**Cinq arguments, tous écrits, aucun montré :**

```
⟷  La parole qu'on te tient   « En gratuit, tu vois ta parole envers les autres… »
◔  Rappels intelligents        « Promi te relance juste avant que ça glisse. »
✳  Nuées illimitées            « Autant de cercles que tu veux… »
◈  Stats avancées              « Ton harmonie dans le temps, par personne, par Nuée. »
◐  Toiles signature            « Thèmes et matières exclusives au Cercle. »
```

**Le prix, tel qu'il est écrit aujourd'hui :**

```
sous-titre   « Tout Promi pour 3,99 €/mois … Ou prends l'année : 29 €, soit près de cinq mois offerts. »
bouton 1     « Essayer 14 jours, puis 3,99 €/mois »           ← primaire
bouton 2     « Prendre l'année — 29 € · soit 2,42 €/mois · −39 % »   ← secondaire
note         « ou un design à l'unité — 1 €, ou 4 pour 3 € »   ← opacité 0,70
```

Trois défauts de vente :
1. **La forme interdite est en tête et la bonne est en bas.** « soit près de cinq mois offerts »
   est exactement ce que Tom interdit ; la forme demandée — `29 € · soit 2,42 €/mois · −39 %` —
   n'existe qu'en **sous-titre du bouton secondaire**.
2. **On dit, on ne montre pas.** Les cinq arguments sont du texte ; aucun ne fait **voir** ce
   qu'on n'a pas. Le §3.8 (voile 2,4 px + encart net) est la mécanique prévue pour ça — elle
   n'est employée **nulle part** sur cette page.
3. **Les cinq icônes** `⟷ ◔ ✳ ◈ ◐` sont des glyphes typographiques, hors langue du produit.

**Le logo Cercle vu par les autres.** Rien n'a été trouvé qui sorte de l'appareil : `✦` vit dans
`.st3-prem`, `.adv-pill`, `.set-cercle` et `#auraHelp .ah-badge.prem` — **tous des écrans à soi**.
Le partage est le seul écran où le §3.8 est interdit, et il n'en porte pas. **Rien à corriger de
ce côté ; c'est à ne pas perdre au moment de dessiner.**

---

## F · LES QUATRE PORTES DU CERCLE, ET CE QU'ELLES FONT

```
#karmaCercle       bas de l'Aura, en gratuit          setPremium(true) + toast + ouvre #plusScreen
#ahCercleCta       dans la fiche d'aide               ouvre #plusScreen
.adv-lock          récurrence & rappels, sur fiche    ouvre #plusScreen
#stLockCta         Studio, monde verrouillé           ouvre #plusScreen
```

⚠ **`#karmaCercle` OFFRE le Cercle avant de le vendre** : son gestionnaire appelle
`setPremium(true)` **puis** ouvre la page de vente. C'est une commodité de démonstration
restée dans le produit — même famille que `#demoTg` (« Aperçu gratuit / Aperçu membre »).
Les deux sont à trancher : ce sont des outils d'auteur, pas des commandes d'utilisateur.

---

## G · CE QUE L'AUDIT NE TRANCHE PAS

- **`#demoTg` et `#karmaCercle` sont-ils du produit ?** Ils permettent de voir l'écran des deux
  côtés sans payer. Aucun cadre ne les dessine. → à trancher au dessin.
- **La série (`streak`)** est calculée et jamais montrée. Elle est du vocabulaire de rendement
  (une série se casse) : à enterrer, sauf avis contraire.
- **`releve-S2` n'est pas au vert sur cette machine** — deux passages en série donnent
  `position 29 · style 0 · hors cadre 2`, et **le thème fautif change d'un passage à l'autre**
  (clair puis sombre) : le Peaufiner de la Nuée sort mesuré **0 × 0**, c'est-à-dire qu'il ne
  s'est pas ouvert à temps. **`style 0` dans les deux passages : la correction des sept
  libellés à 13 est bien en place.** Le reste est une course de construction dans le juge, pas
  une régression de l'app — mais c'est signalé, pas réglé.
