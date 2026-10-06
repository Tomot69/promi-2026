# ÉTAT AU 30 SEPTEMBRE 2026 — CE QUI EST VRAI AUJOURD'HUI

> **Le document de référence du portage.** Engendré par `etat_generer.py` le 2026-10-07 depuis la source vivante : `PROMI-TOKENS.json` et l'app en marche (version 0.16). **Ne pas l'éditer à la main** : on corrige la source, puis on relance.
> Les valeurs de ce document priment sur tout autre document. `PROMI-SPECIFICATIONS.md`, `PARCOURS.md` et `MOODBOARD-VALEURS.md` sont des **archives** (valeurs antérieures au 16 septembre 2026) : ils disent la géométrie et l'intention d'août, jamais une couleur, une police ni un libellé à porter.

**Ordre des sources, en cas de doute :** ce document → `PROMI-TOKENS.json` (couleurs, polices) → `CONTRAT-MONDE.md` (ce qu'un monde doit faire) → `SPEC-JUGES.md` (les règles que les juges portent) → `CLAUDE.md` (méthode, pièges, décisions datées) → les moodboards (géométrie d'origine) → une mesure de l'app (jamais une référence).

## 1 · Le lexique — ce qui s'affiche, et sa clé interne

Les clés internes **ne changent jamais** quand un nom affiché change (décision du 30 sept. 2026, v106).

| Affiché | Clé interne | Genre, notes |
|---|---|---|
| Promi | `promi` | invariable : « trois Promi » — une promesse, une dalle |
| Chiche | `chiche` (`p.chiche`) | un défi lancé ; on LANCE un Chiche, on ne le plante pas |
| **Cercle** | `nuee` (`NUE`, `curNuee`, `.dp-nuee`…) | **masculin** : « un Cercle », « le Cercle ». Était « Nuée » jusqu'au 30 sept. |
| **Ma Parole !** | `ouvreCercle`, `.s2-cercle`, `isPremium`, `#plusScreen` | l'offre payante. Était « Le Cercle ». Espace insécable avant « ! » |
| gardé de côté | `draft` | « brouillon » est banni |
| Toile | `window.Toile` (promi-moteur.js) | le canevas des dalles, Voronoï pondéré |
| Fil | `#feedView` | le flux d'activité |
| Index | `#indexSheet` | la liste des Promi |
| Aura | `#auraScreen` | l'écran de progression (ex-« Karma ») |
| Pelote | `_aura` | la boule de l'Aura — « sphère » et « Orbite » sont bannis |
| Studio | `#studioScreen` | le monde et la palette |
| Peaufiner | `.s2-*`, `#dpDetails` | le tiroir de réglages d'une fiche |
| Folio | `#shMode [data-mode=mosaic]` | ce qu'on partage de ses dalles |
| Noyau | `.kring`, `.au-nb` | un anneau à trois arcs |

**Termes bannis** (écran, code, documents) : « tâche », « to-do », « objectif », « échéance » comme libellé, « valider », « urgent », « score », « brouillon », « Orbite », « la sphère », « Belle parole » comme bouton, « En replanter un ». On dit **tenir sa parole, tracer, planter, lancer**.

## 2 · Les couleurs — engendrées de `PROMI-TOKENS.json` (2026-09-20)

Un rôle vaut deux valeurs (mode clair · mode sombre). **Une règle CSS emploie la palette FIXE (`--c-*`), jamais un rôle** (un rôle inverserait en silence la crème et l'encre). Le portage Swift emploie les rôles (`Promi+Design.swift`).

| Rôle | Clair | Sombre |
|---|---|---|
| `fond` | `#F7F0DE` | `#050302` |
| `encre` | `#201908` | `#F7F0DE` |
| `surface` | `#F7EBD6` | `#211B05` |
| `surface-haute` | `#FAF4E8` | `#251F11` |
| `sous-texte` | `#6E6350` | `#928166` |
| `grip` | `#C8BAA4` | `#493D28` |
| `exception` | `#2B1020` | `#2B1020` |
| `crete` | `#0B4A2A` | `#0B4A2A` |
| `brun-encre` | `#43291C` | `#43291C` |
| `promi` | `#82AEF8` | `#82AEF8` |
| `chiche` | `#FFB8D2` | `#FFB8D2` |
| `nuee` | `#C9A8F5` | `#C9A8F5` |
| `garde-de-cote` | `#AE3929` | `#AE3929` |
| `tenu` | `#00341A` | `#00341A` |
| `tenu-clair` | `#00341A` | `#00341A` |
| `amande` | `#8FE08F` | `#8FE08F` |
| `a-tenir` | `#DD4D23` | `#DD4D23` |
| `en-cours` | `#291547` | `#291547` |
| `en-cours-clair` | `#291547` | `#291547` |
| `encre-sur-tenu` | `#00341A` | `#00341A` |
| `promi-clair` | `#C4A2F5` | `#C4A2F5` |
| `chiche-clair` | `#F5AC9E` | `#F5AC9E` |
| `nuee-clair` | `#E6D8FA` | `#E6D8FA` |
| `lilas` | `#E6D8FA` | `#E6D8FA` |
| `mauve-clair` | `#C9A8F5` | `#C9A8F5` |
| `corps-promi` | `#CFE5FE` | `#0E78F2` |
| `corps-chiche` | `#FFF4FC` | `#7C3F58` |
| `corps-nuee` | `#EEE4F8` | `#5D4978` |
| `corps-tenu` | `#2B1020` | `#2B1020` |
| `corps-a-tenir` | `#EFC3B9` | `#533336` |
| `corps-garde` | `#EFC3B9` | `#4B2D30` |
| `blanc` | `#FFFFFF` | `#FFFFFF` |
| `noir` | `#000000` | `#000000` |

**Les règles qui font lire ces couleurs** (décisions en vigueur) :
- **Le champ dit la nature, la ligne dit l'état.** Champ : Promi `#82AEF8` · Chiche `#FFB8D2` · Cercle `#C9A8F5` (le lilas est le CHAMP d'un Cercle, le violet `#291547` est ce qu'on pose dessus). Un champ blanc n'existe jamais.
- **Trois états, trois arcs, jamais plus** : à tenir `#DD4D23` · en cours `#291547` · tenu `#00341A`. Un état suit CE QUI EST PEINT SOUS LUI : sur la terre `#2B1020` d'une fiche tenue, le tenu passe à l'amande `#8FE08F` ; sur un fond clair il reste `#00341A`.
- **L'amande `#8FE08F`** ne peint que la célébration (la seconde dalle qui apparaît, se décale, disparaît) et la mention « TENU(E) ».
- **Tout suit le Studio (monde et palette), sauf l'Aura** (v34) : la Pelote et « Ce que tu as tenu » gardent le monde de plantation. Les ÉTATS ne suivent jamais rien.
- **Ingénu, la palette par défaut, dit la nature** (v17) : sous Ingénu seulement, un Promi est bleu, un Chiche rose, un Cercle lilas.
- **Un trait sur un aplat coloré se juge en ΔE (plancher 15), du texte sur un fond en luminance (seuil 42).**

## 3 · Les polices et les niveaux de texte — trois polices, cinq faces

| Famille | Pile CSS | Fichier | Licence |
|---|---|---|---|
| titre | `PromiLate,Gilbert,system-ui,sans-serif` | PromiLate-Regular.otf (Polices Promi/) | Police propre à Promi. |
| libelle | `Gilbert,system-ui,sans-serif` | Gilbert-Bold.woff2 | CC BY-SA 4.0 — Ogilvy & Mather / Type With Pride. Crédit obligatoire, glyphes non modifiables. |
| texte | `Atkinson,system-ui,sans-serif` | Atkinson-{Regular,Medium,Bold}.woff2 | SIL Open Font License 1.1 — Braille Institute of America. |
| marque | `PromiLate,Gilbert,system-ui,sans-serif` | PromiLate-Regular.otf (Polices Promi/) | Police propre à Promi. |

| Niveau | Famille | Graisse | Taille | Capitales | Opacité |
|---|---|---|---|---|---|
| titre | titre | 600 | 36 px | non | 1.0 |
| sous-titre | libelle | 700 | 22 px | oui | 1.0 |
| texte | texte | 400 | 16 px | non | 1.0 |
| accent | texte | 700 | 16 px | non | 1.0 |
| petit | texte | 400 | 14 px | non | 1.0 |
| meta | texte | 400 | 13 px | non | 0.65 |
| libelle | libelle | 700 | 15 px | oui | 1.0 |

Cinq faces embarquées et cinq seulement : **Gilbert 700 · Atkinson 400 / 500 / 700 · PromiLate 400**. Une graisse absente se reporte (table de `CLAUDE.md` §6). PromiLate n'a ni « ! » ni espace insécable : ils viennent de Gilbert. Rien sous 12 px ; aucune opacité sous 72 % sur un texte à lire. ⚠ Les tailles ont grandi en v96 (`size-adjust:112 %`) : l'air se mesure à l'ENCRE, jamais à la boîte.

## 4 · Les 20 mondes — engendrés de l'app en marche

Dans l'ordre du Studio. **« Semis »** : *constant* = les huit anciens (≈ 68 cellules, les paroles colorent des cellules) ; *grandit* = la Toile est faite de ses seules paroles (v35). Le semis est amorcé par la clé de la Toile (assainissement, 30 sept.) : même Toile à chaque ouverture. **Réglages** : ce que le monde déclare au moteur (`REGLAGES_MONDE`, promi-moteur.js).

| # | Affiché | Clé | Accès | Semis | Réglages déclarés |
|---|---|---|---|---|---|
| 1 | Pochade | `encre` | gratuit | constant | `ressort [0.838, 0.79, 0]`, `elanPlante`, `libre` |
| 2 | Touffe | `touffe` | gratuit | constant | `ressort [0.838, 0.79, 0]`, `elanPlante`, `libre` |
| 3 | Brouillamini | `brouillamini` | gratuit | grandit | — |
| 4 | Halin | `halin` | gratuit | grandit | `compagnons` |
| 5 | Esquille | `esquille` | gratuit | grandit | `finaleAuRepos`, `relaxLocal` |
| 6 | Tesselle | `mosaique` | gratuit | constant | `ressort [0.83, 0.78, 1]`, `grille`, `pasTrame 11` |
| 7 | Braille | `braille` | gratuit | constant | `ressort [0.83, 0.78, 1]`, `grille`, `pasTrame 9` |
| 8 | Buvard | `pixel` | gratuit | constant | `ressort [0.83, 0.78, 1]`, `grille`, `pasTrame 5` |
| 9 | Ramage | `ramage` | Ma Parole ! | grandit | `apercuPause ["_apOccupe", 120]`, `apercuFilm` |
| 10 | Guingois | `guingois` | Ma Parole ! | grandit | — |
| 11 | Chantourné | `chantourne` | Ma Parole ! | grandit | — |
| 12 | Volubilis | `volubilis` | Ma Parole ! | grandit | `apercuPause ["_volBouge", 60]`, `apercuPetit` |
| 13 | Madrure | `madrure` | Ma Parole ! | grandit | `ondeNoeuds`, `donneesPropres` |
| 14 | Chamade | `chamade` | Ma Parole ! | grandit | — |
| 15 | Ritournelle | `ritournelle` | Ma Parole ! | grandit | — |
| 16 | Bobinette | `bobinette` | Ma Parole ! | grandit | `relaxLocal` |
| 17 | Mascaret | `mascaret` | Ma Parole ! | grandit | — |
| 18 | Éclisse | `terrazzo` | Ma Parole ! | constant | `ressort [0.83, 0.78, 1]`, `libre` |
| 19 | Taille-douce | `gravure` | Ma Parole ! | constant | `ressort [0.83, 0.78, 1]`, `grille` |
| 20 | Houle | `sillons` | Ma Parole ! | constant | `grille`, `pasTrame 6` |

Le contrat d'un monde (ce qu'il reçoit, ce qu'il doit rendre, son budget) : `CONTRAT-MONDE.md`. Ce qui juge un monde au pixel : `banc_rendu.py` (20 mondes × Toile + 4 dalles × 3 tailles, référence `banc-rendu/ref/`). Éclats n'existe plus (retiré le 30 sept.).

## 5 · Les 24 palettes du Studio — engendrées de l'app en marche

Palette par défaut : **Ingénu** (clé `signal`). Quatre tons, dans l'ordre de leur poids (≈ 34 · 28 · 23 · 15 %).

| Nom | Clé | Tons |
|---|---|---|
| Ingénu | `signal` | `#82AEF8` · `#FFB8D2` · `#C9A8F5` · `#EFE3C7` |
| Primesautier | `primesautier` | `#FFD60A` · `#FF7AA2` · `#005F73` · `#FFF4C2` |
| Candide | `candide` | `#CDB4FF` · `#FFC8A2` · `#BDE0A8` · `#FFB5C8` |
| Gouailleur | `gouailleur` | `#9C4A1A` · `#E07A1F` · `#E9B824` · `#7D8B2E` |
| Alangui | `alangui` | `#C4A69F` · `#7D6A8A` · `#DDCBB0` · `#8C97AB` |
| Irascible | `irascible` | `#FF2D1A` · `#FF8A1C` · `#B80F2E` · `#2B0A0A` |
| Hurluberlu | `hurluberlu` | `#C8FF00` · `#7B2FF7` · `#FF3D9A` · `#2B1400` |
| Béat | `beat` | `#1F4FD1` · `#FFC21A` · `#FFFFFF` · `#E0673F` |
| Minaudier | `minaudier` | `#FF9FC8` · `#E0115F` · `#FFE0EC` · `#B5F2FF` |
| Chafouin | `chafouin` | `#A9B41F` · `#E6A3BE` · `#6C4675` · `#3FA7D6` |
| Frivole | `frivole` | `#FF71CE` · `#01CDFE` · `#05FFA1` · `#FFFB96` |
| Cajoleur | `cajoleur` | `#9FE6CF` · `#4B2B1F` · `#FFF0D4` · `#E23E57` |
| Allègre | `allegre` | `#1FB36A` · `#7EC8FF` · `#0E5E4A` · `#EFFBEA` |
| Lunatique | `lunatique` | `#2BC4C4` · `#D9A21B` · `#C2185B` · `#1E1B3A` |
| Flegmatique | `flegmatique` | `#CFE8FF` · `#6FA8DC` · `#4A5A6A` · `#FFB3A7` |
| Narquois | `narquois` | `#FF9A5A` · `#7A1FA2` · `#FFE8D6` · `#FF2F6D` |
| Truculent | `truculent` | `#FF3E00` · `#00E5FF` · `#5600D6` · `#F6FF00` |
| Pétulant | `petulant` | `#FF8A00` · `#6800E0` · `#00C85A` · `#FFAAC8` |
| Fantasque | `fantasque` | `#00FF8C` · `#E60073` · `#0040FF` · `#FFF7DE` |
| Fielleux | `fielleux` | `#1A1400` · `#5A3300` · `#FFE600` · `#B38F00` |
| Sibyllin | `sibyllin` | `#0A0A1F` · `#2A1B4D` · `#5E2CA5` · `#00E0FF` |
| Vénéneux | `veneneux` | `#140014` · `#4A0033` · `#FF007A` · `#C0C0C0` |
| Atrabilaire | `atrabilaire` | `#0A2E36` · `#1B6F80` · `#FF9E00` · `#F2F2F2` |
| Taciturne | `taciturne` | `#0B0D4F` · `#2A2AD4` · `#8F8CFF` · `#E4E2FF` |

## 6 · Ma Parole ! — l'offre

- **Prix** : 39 € / an (soit 3,25 €/mois) · ou 5,99 € par mois · essai 14 jours · un monde à l'unité 1 €. Sans engagement.
- **L'écran qui vend** : titre « MA PAROLE ! », sous-titre « Retourne ta Toile », bouton principal « Essayer 14 jours », option « Bon, allez d'accord — 39 € / an », en petit « ou 5,99 € par mois ».
- **Réglages** : la porte « Ma Parole ! » ouvre l'offre (ce n'est pas un mur) ; au payé « Tu es Membre Ma Parole ! », sans lien.
- **Ce qu'elle ouvre** : l'autre moitié de la Toile (ce qu'on te tient), la récurrence, le rappel à l'heure choisie, l'importance, la mémoire des paroles en l'air, la couleur de la dalle, douze mondes, les Cercles illimités.
- **Les murs** : un réglage réservé est flouté à **4,8 px**, sans explication (sauf le Studio, qui garde les siens). Au toucher, une phrase paraît au centre du mur (Gilbert, encre `#201908` sur clair, crème `#F7F0DE` sur sombre, ≤ 3 lignes, 1,4 s + 60 ms par caractère, entre 3 et 5,5 s). La toute première fois, l'offre s'ouvre à la fin de la lecture ; ensuite, un toucher pendant la lecture l'ouvre. Compteur global, remis à zéro après 14 jours sans mur.
- **Les 18 phrases, dans l'ordre** (puis au hasard sans répéter la précédente) :
  1. Eh non. Mais avec Ma Parole !, oui.
  2. La solution commence par Ma et finit par Parole !
  3. Toujours non. Ma Parole !, toujours oui.
  4. Je vois bien que ça te titille. Ma Parole ! aussi.
  5. Tiens tiens, on dirait que ça commence à t’intéresser…
  6. Tiens tiens. Vous ici.
  7. Tu sais où trouver Ma Parole ! maintenant.
  8. On maintient cette position officielle, alors ?
  9. Allons bon. Nous y voilà à nouveau.
  10. Entre nous, le mystère s’amenuise.
  11. Les pourparlers se prolongent, je vois.
  12. Tu peux continuer. Je tiens le registre.
  13. Ici, tout restera entre nous.
  14. Je commence à soupçonner une stratégie.
  15. On pourrait presque en faire une tradition.
  16. Regarde-nous, avec nos petites habitudes.
  17. Dis donc, tu viendrais presque pour moi.
  18. On se retrouve ici tout à l’heure ?

## 7 · Les notifications (v109–v110)

- Jamais au lancement. « **Je te le rappelle ?** · oui · pas besoin » paraît 1,9 s après la plantation d'une parole DATÉE (sous le plateau de l'accueil) ; la permission n'est demandée qu'après « oui ». Deux « pas besoin » d'affilée, puis plus rien. Elle part seule au bout de 12 s. Un « oui » vaut pour toutes les paroles datées.
- **Gratuit** : le mot de la veille d'une parole datée. **Ma Parole !** : la mémoire des paroles en l'air (une par semaine au plus), le choix de l'heure (8 h · midi · 19 h ; 19 h au gratuit). **Firebase** : l'envoi app fermée, tout ce qui vient d'une autre personne.
- **Les mots** : « Demain, c'est « {titre} ». » · « « {titre} » — Tu as promis ça à {Prénom}. Demain. » · « Ton Chiche à {Prénom} arrive demain. » · « « {titre} » — C'est aujourd'hui. » (à l'heure choisie, si la veille était passée à la plantation) · « « {titre} » flotte toujours. Un de ces jours ? »
- **Rien quand la date est passée.** Une notification par jour au plus. Aucune qui reproche, ni série, ni score.

## 8 · Les invariants du dessin — ce qui ne se négocie pas

- Une dalle est TOUJOURS la vraie dalle du moteur (`Toile.dalleTrame`), rendue à sa taille finale et posée 1 : 1 — jamais une image découpée, redimensionnée, un polygone, une photo.
- La bande haute d'une fiche porte la NATURE (et teinte sa dalle sur la rampe de la nature, Q30) ; nulle part ailleurs une dalle n'est teintée par sa nature (hors Ingénu).
- Un anneau (Noyau) a trois arcs au plus, jours de 3 px d'arc, filet crème de 1 px sur le seul bord extérieur quand il est posé sur du sombre.
- Les composants communs sont identiques partout : le geste (118 px, deux points, un trait), Peaufiner (62 px), « ✕ FERMER » en haut à droite, le plateau (342 × 60, trait 2, rayon 30).
- Grammaire des contours : trait 2 px, couleur du corps, rayon = hauteur ÷ 2 jusqu'à 94,5 px de haut, 30 au-delà.
- L'air entre deux textes ne se resserre jamais ; il se mesure à l'encre.
- Rien ne paraît une fraction de seconde (ouverture, fermeture, plantation).
- Un mouvement se calcule sur le temps réel (sauf Houle, par image, par décision).

---
*Engendré. Pour corriger : la source (`PROMI-TOKENS.json`, l'app, ou la partie écrite de `etat_generer.py`), puis relancer.*
