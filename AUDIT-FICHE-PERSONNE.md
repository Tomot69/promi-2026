# AUDIT — LA FICHE DE LA PERSONNE (`#personSheet`, `openPerson`)

> **10 septembre 2026.** Serveur 8752, viewport 430 × 932 (→ `#device` 390 × 844 exact), dsf 2, deux thèmes.
> App `a57f16aedee5ca615d82bd03438a9e25`. Outils : `sauvegardes/audit-fiche-personne/outils/` ; captures et inventaires
> mesurés : `sauvegardes/audit-fiche-personne/avant/`.
> **Rien n'est modifié par cet audit. Il constate.** Méthode (Q184, Tom) : *« on ne retire rien sans savoir ce qu'on
> perd »* — pour chaque nœud : ce qu'il dit, d'où il vient, qui d'autre le lit, ce que son retrait perd.
> Intention de Tom pour la suite : **« une surface soyeuse qui intrigue et attire »** — l'audit ne la dessine pas (§ G).

---

## A · CE QUE L'ÉCRAN MONTRE — nœud par nœud (Marion, sombre ; cotes en écran 390)

| # | Nœud | Ce qu'il dit | D'où il vient | Mesuré | Règle |
|---|---|---|---|---|---|
| 1 | plateau `.enh` + `#psName` + `.closeb` | « Marion » · ✕ FERMER | `lot-ENCART-HAUT` (l. 22285–22290), `lot-PLATEAU-PARTOUT` (l. 22541) | 24/40, 342 × 60, trait 2, rayon 30 ✓ · nom Bricolage **800** calculé | §5 ✓ · §6 ✗ **vérifié** : la cascade demande Bricolage **800**, seules 600 et 700 sont chargées, et `lot-POLICES` n'a rien posé en ligne sur `#psName` — un couple absent |
| 2 | `#psAva` | le visage (dégradé) | `_blobBg(name)` (l. 3399) | 44 × 44 à **x = 8** | grille : le plateau est à 24 |
| 3 | `#psSub` | « votre harmonie : rayonnante · ta parole : rayonnante » | `harmonyWord` (l. 6352 : ≥ 85 rayonnante, ≥ 65 solide, ≥ 40 installée, sinon naissante, « à tisser ») | Apfel 13, **alpha 0,60**, jusqu'à x = 382 | **INTERDIT 2** (Q184 ; AUDIT-AURA-CERCLE §C règle 1 : aucun mot de valeur pointé sur quelqu'un) · §6 opacité < 72 % · **« votre » / « ta » : vous et tu dans la même ligne** |
| 4 | `#psMirror` — l'anneau | les proportions tenu / en cours / à tenir | `karmaRing` / `drawKRing` (l. 6298) | 78 × 78 au centre | §2.9 : un anneau de personne fait 58, photo 36 — ici 78 sans visage |
| 5 | `#psMirror` — second anneau `.kr-eux`, `.ps-mleg`, `.ps-eq` (« toi NN % ⟷ eux NN % ») | ce que le Cercle ajoute | `openPerson` (l. 6312), CSS `.device.premium …` (l. 175, 1775, 1782) | **jamais visibles — même avec `#device.premium`** (et `.frame.premium`) | la fiche vit sous `.frame`, HORS de `#device` (mesuré : `deviceDansFrame` vrai, fiche hors de `#device`) : aucune règle `.device.premium` ne peut l'atteindre. **Une fonction du Cercle inatteignable.** Et `.ps-eq` porte deux pourcentages : règle 1 ✗ |
| 6 | `.ps-clab` + SVG `personSpark` | « COMMENT ÇA ÉVOLUE » + une courbe | `personSpark` (l. 6326) | trait **rgb(131,133,140), opacité 0,7** — gris neutre ; point #D0B0FF | **INTERDIT 1** (Q184, Q183 : la courbe va au Cercle) · §3 : **jamais de trait neutre ou gris** · ⚠ **sous deux Promi résolus, la courbe est INVENTÉE** (une rampe synthétique de sept points, sans donnée) |
| 7 | `.ps-leg3` | ● en cours ● tenues ● à tenir | `openPerson` | Apfel 13, #8FA0FF · #2BE88C · #F07A2E | la légende de l'anneau ; elle ne dit rien si l'anneau ne dit rien |
| 8 | `.grouplab` | « PROMESSES PARTAGÉES » | markup l. 2764–2769 | ApfelMid 13, **alpha 0,60** | §6 opacité < 72 % |
| 9 | ligne de compte `.b` | « 3 Promi échangés · 1 reçu · 2 donnés » | `openPerson` | Apfel 16, **opacité 0,65** · pour « moi » : **« 11 échangés · 11 reçus · 5 donnés »** (16 ≠ 11) | **INTERDIT 3** (Q184 ; §C règle 4 : aucun agrégat par personne ; règle 2 : un seul chiffre) · §6 opacité · le compte est faux sur « moi » |
| 10 | rangées `.row[data-id]` | titre · « à Marion · en cours » · › | `openPerson`, `bullet(p)` (l. 3285) | titre Apfel 15, sous-ligne 13, › à x = 374,8 | l'état est dit en MOT (« en cours », « tenue ») ; **vérifié au doigt** : la rangée « courir dimanche » ouvre sa fiche (#detailPoster), la fiche de la personne se ferme ✓ |
| 11 | les dalles des rangées `canvas.mini-dalle` | la vraie dalle du Promi | `bullet(p)` pose `data-mini` | **0,0 % de pixels peints à 0,3 · 0,9 · 2,5 s, dans les deux thèmes** | §4 règle 1 et règle 5 : **`openPerson` n'appelle jamais `peintMinis`** — les trois dalles sont des canevas vides |
| 12 | `#personSheet::before` | une grande forme floue | `.tuto-fond::before` (l. 99, 102 ; le « ghost-ink », commentaire l. 25144) | 743 × 666, opacité **0,09** (sombre) / **0,14** (clair) ; **elle BOUGE en permanence** — relevé toutes les 0,5 s : `--gx` 30,1 → 36,6 px, `--grot` 0,94 → 1,21° en 2 s | **vérifié** : c'est l'ombre de dalle (`--ghost-ink` posé par `setEl` → `ghostInk()`, l. 8938), animée par `frame()` — le **chantier 58** · §3 « la couleur qui gagne sa place » ✗ · **§4 règle 6 ✗ : une dalle en fond animé sur un écran qui montre des dalles** (la liste) |
| 13 | la boîte de la fiche | — | `.sheet` sous `.frame` | **−16, −16, 422 × 876** | le piège « un .screen ne coïncide pas avec #device » (§8) : la colonne de contenu part à **8**, le plateau à 24 |

Fond : `#16171B` en sombre, `#F4EEE1` en clair (correctif l. 11718 — « personSheet vit sous .frame »).

---

## A bis · L'INVENTAIRE COMPLET — chaque nœud, chaque valeur, gratuit ou Cercle, vivant ou mort

Relevé sur tous les descendants de `#personSheet`, visibles ou non (`outils/noeuds_fiche.py`, `avant/noeuds.json`),
pour Marion, Rachel, « moi » et une personne sans Promi, en gratuit puis en **Cercle FORCÉ** (une page jetée où l'on pose
ce qui manque pour que les règles `.device.premium` atteignent la fiche — c'est le seul moyen de voir le mode perdu).
Toutes les valeurs viennent d'`openPerson` (l. 6312) ; « vivant » = on peut le voir en usant de l'app aujourd'hui.

| Nœud | Valeur affichée (et d'où elle se calcule) | Gratuit / Cercle | Vivant / mort |
|---|---|---|---|
| `#psName` | le prénom (« moi » s'affiche « moi ») | gratuit | vivant |
| `#psAva` | ta photo pour « moi », sinon `_blobBg(prénom)` | gratuit | vivant |
| `#psSub` | « votre harmonie : » + `harmonyWord(allTrust)` · « ta parole : » + `harmonyWord(yourTrust)` — cinq mots possibles : rayonnante ≥ 85 %, solide ≥ 65, installée ≥ 40, naissante, « à tisser » (aucun résolu) ; allTrust = tenus / résolus des deux côtés, yourTrust = de ton côté | gratuit | vivant — **INTERDIT 2** |
| anneau « toi » `.kr-toi canvas` | proportions de TES Promi envers elle : en cours / tenus / ratés (yE, yT, yR) | gratuit | vivant |
| libellé « toi » `.kr-toi .kr-side` | « toi » | Cercle (visibility cachée en gratuit) | **mort** |
| anneau « eux » `.kr-eux` + libellé prénom | proportions de SES Promi envers toi (enc, tenu, rate) | Cercle | **mort** (porte absente, § B bis) |
| `.ps-mleg` | « toi envers eux » · « eux envers toi » | Cercle | **mort** |
| `.ps-eq` (seulement si les deux côtés ont un résolu) | « toi **NN %** ⟷ eux **NN %** », un repère sur une ligne, et une phrase : « le lien est réciproque ✿ » (écart < 10), « tu portes un peu plus », « ils portent un peu plus » — Rachel : « toi 50 % · eux 0 % · tu portes un peu plus » | Cercle | **mort** — et §C règle 1 (deux chiffres attachés à une personne) |
| `.ps-curve` « comment ça évolue » + SVG | la part tenue cumulée, Promi par Promi (132 × 30) ; **sous deux résolus : une rampe de 7 points calculée, pas des données** | **gratuit** (Q183 : Cercle) | vivant — **INTERDIT 1** |
| `.ps-leg3` | « en cours » · « tenues » · « à tenir » (#8FA0FF · #2BE88C · #F07A2E) | gratuit | vivant |
| `.grouplab` | « Promesses partagées » | gratuit | vivant |
| ligne de compte `#psList .b` | « N Promi échangés · N reçus · N donnés » — **pour « moi », « reçus » compte ce que TU as donné** (`from === 'moi'`) : 11 · 11 · 5 | gratuit | vivant — **INTERDIT 3** + faux |
| rangée `.row[data-id]` ×N | la dalle (`bullet`), le titre, `relLabel` (« à Marion », « de Marion → le groupe », « pour toi », **« à le groupe »** ✗), l'état (`STLAB` : en cours, tenue, à tenir), la Nuée | gratuit | vivant — toucher → sa fiche ✓ · **dalle jamais peinte** |
| la NATURE de chaque rangée | **rien** : « courir dimanche » et « le grand plongeoir » sont des **Chiche** (`a.chiche = true` au jeu de démonstration), « vider le composteur » aussi — la fiche les montre exactement comme des Promi | — | **absente** — §4 : « l'accent porte la nature » (pastille, libellé, contour, en framboise pour un Chiche) |
| état vide | « aucun Promi pour l'instant » | gratuit | vivant (personne sans Promi via une fiche) |
| mode « moi » entier | un anneau (66), la courbe, **toutes** tes paroles (11 rangées) sous « Promesses partagées » | gratuit | **mort** — aucune porte (§ B bis) |
| `.closeb` | « ✕ Fermer » | gratuit | vivant |
| `.grip` | — | — | **mort** (0 × 0) |
| `#psSpark`, `#psRing` | écrits s'ils existent | — | **mort** (n'existent pas) |
| `#personSheet::before` | l'ombre de dalle, animée | — | vivant — hors DA (§ A n° 12) |

---

## B · LES ENTRÉES ET LES VARIANTES (mesurées au doigt ou par l'appel)

- **La rangée de l'Aura** (« Marion », « Rachel ») → ouvre la fiche ✓ (`releve-aura`, famille 8).
- **Le disque d'une personne sur une fiche** (`.kring[data-p]`) → ouvre la fiche ✓ (Promi 126 → « Rachel »).
- **Le disque « toi » de l'Aura** → **n'ouvre rien** (`show:false`). Appelée directement, `openPerson('toi')` montre une
  personne nommée « toi », sans Promi, « votre harmonie : à tisser » — hors d'atteinte du doigt.
- **`openPerson('moi')`** → un seul anneau, onze rangées, et le compte faux du n° 9. Qui l'appelle ainsi : non trouvé.
- **Une personne sans Promi** → « aucun Promi pour l'instant », l'anneau et la courbe restent, « votre harmonie : à tisser ».
- **`ouvrirPersonne` et `renderPerson`** sont appelés (l. 4893–4905) et **n'existent nulle part**.

---

## B bis · LES PORTES ET LES COMMANDES — comme l'audit du partage (au doigt, `outils/portes_fiche.py`)

**Les portes — chaque appelant d'`openPerson`, et son hôte à l'écran :**
```
l. 28584  la rangée de l'Aura (.au-n)            VIVANTE   toi · Marion · Rachel au doigt — mais « moi » est ÉCARTÉ (q !== 'moi')
l. 3356   le disque d'une personne sur une fiche  VIVANTE   15 fiches sur les 30 premières en portent un (Rachel, Marion, Adrien)
l. 4900   #dAura .kring (la fiche)                VIVANTE   même rangée ; essaie d'abord ouvrirPersonne / renderPerson — inexistants
l. 6320   #ktoile (ancienne Aura)                 MORTE     le nœud n'existe plus
l. 6322   #ksocial (ancienne Aura)                MORTE     dans le DOM, invisible (Marion 100 %, Adrien 50 %, Rachel 33 % — les chiffres de §C)
l. 6510   #kpers (ancienne Aura)                  MORTE     dans le DOM, invisible
```
**Deux modes entiers sans porte :**
- **le mode « moi »** (`/^moi/` dans `openPerson` : un anneau, toutes tes paroles) — ses portes étaient dans l'ancienne
  Aura, mortes ; la nouvelle rangée l'écarte explicitement. Personne ne peut plus l'ouvrir.
- **le mode Cercle** (second anneau, légende « toi envers eux / eux envers toi », équilibre) — la porte existe (être
  abonné), mais la fiche vit hors de `#device` : ses règles `.device.premium` ne l'atteignent jamais (§ A n° 5).

**Les commandes — chaque chose touchable de la fiche (Marion), touchée :**
```
✕ FERMER          ferme la fiche                                    ✓
une rangée        ouvre la fiche de son Promi, ferme la personne    ✓
le visage         rien          le nom       rien                   (curseur « auto » : inertes, et rien ne le promet)
l'anneau          rien          la courbe    rien          la légende   rien
la poignée .grip  dans le markup, INVISIBLE (0 × 0)
glisser vers le bas depuis le haut          la fiche reste ouverte — aucun geste ne la ferme
```
Aucune commande n'est inatteignable ; c'est la fiche elle-même qui a perdu deux de ses modes.

---

## C · LES RÈGLES — ce que la fiche enfreint

| Règle | Où | Mesure |
|---|---|---|
| §C 1 — aucun chiffre ni mot de valeur attaché à une personne | n° 3, n° 5 | « rayonnante », « toi NN % ⟷ eux NN % » |
| §C 2 — un seul chiffre, le tien, global | n° 9 | trois chiffres par personne |
| §C 4 — aucun agrégat par personne | n° 3, n° 9 | un mot par personne, un compte par personne |
| Q183 — la courbe est au Cercle | n° 6 | montrée en gratuit |
| §3 — jamais de trait neutre ou gris | n° 6 | rgb(131,133,140) |
| §3 — la couleur qui gagne sa place | n° 12 | une forme qui ne dit rien |
| §4 règles 1 et 5 — la vraie dalle, peinte après insertion | n° 11 | trois canevas vides |
| §6 — aucune opacité sous 72 % sur un texte lisible | n° 3, 8, 9 | 0,60 · 0,60 · 0,65 |
| §6 — six faces seulement | n° 1 | Bricolage 800 calculé (à vérifier) |
| §2.9 — un anneau de personne : 58, photo 36, aucun mot d'état | n° 4 | 78, sans visage |
| §8 — un `.screen` ne coïncide pas avec `#device` | n° 13 | colonne à 8, plateau à 24 |
| la voix — tu, jamais vous | n° 3 | « votre » et « ta » |

---

## D · CE QUI EST MORT

- `#psSpark`, `#psRing` : écrits par `openPerson` « s'ils existent » — ils n'existent pas dans le markup.
- La boucle `drawSpk` après l'ouverture : `personSpark` rend un SVG, pas un `.spk` — elle ne dessine rien.
- Les règles `.device.light …` / `.device:not(.light) …` de la fiche (l. 11685, 11707) ne visent rien — la fiche est
  sous `.frame` (le commentaire l. 11718 le dit).
- Toutes les règles `.device.premium` de la fiche (n° 5) : la fonction du Cercle ne peut pas paraître.
- Un second canevas d'anneau `kr-c` de 0 × 0 à (−20, −44).
- Le CSS de la fiche est écrit deux fois (l. 1772–1801 et 1936–1968).

---

## E · CE QUE CHAQUE INTERDIT EMPORTE (la question de Q184)

- **La courbe (interdit 1).** En gratuit elle part au Cercle (Q183) : on n'y perd rien de vrai — sous deux Promi
  résolus elle est **inventée**. Au Cercle, elle est à redessiner : grise, et sans donnée, elle ne peut pas y aller telle quelle.
- **Les mots de valeur (interdit 2).** Seule ligne qui dise l'état de la relation en mots. L'anneau le dit déjà, sans
  mot (§2.9 : « aucun mot d'état »). **Le retrait ne perd rien que l'anneau ne dise.**
- **Le compte (interdit 3).** Les rangées portent déjà chaque Promi et son sens (« à Marion » / « de Marion »). Le compte
  n'ajoute que l'agrégat — et il est faux sur « moi ». **Le retrait ne perd que l'agrégat.**

---

## F · CE QU'AUCUN CADRE NE DESSINE

**Aucun moodboard ne dessine la fiche d'une personne.** Ni `MOODBOARD-VALEURS.md`, ni `ECARTS-MOODBOARD.md`, ni
`PARCOURS.md`. Le plus proche : `PROMI-SPECIFICATIONS` §2.9 (les Noyaux : anneau 58, arc 6, photo 36, prénom
Bricolage 600/13,5, aucun chiffre ni mot d'état, ordre jamais par valeur ; le Cercle ajoute un second anneau à +9) et
§2.10 (le visage) ; les cadres 18, 19, 21, 22 du moodboard H (« Ton harmonie envers elle, ton côté seulement »,
« on ne note pas six personnes d'un coup », « Personne ne peut savoir que quelqu'un ne paie pas »). La planche de
l'Aura ne fait que renvoyer à `openPerson`. **Comme le Studio, l'Aura et le partage : c'est de la conception, pas un portage.**

---

## G quater · INTÉGRÉ — 11 septembre 2026 (`lot-FICHE-PERSONNE`)

La planche 4 est dans l'app. **Chaque infraction de § C est sortie de l'écran** — le mot d'harmonie, les agrégats,
« comment ça évolue », l'équilibre et sa phrase, le second anneau, la ligne grise, l'ombre animée, les opacités sous 72 %,
« votre », la colonne à 8, Bricolage 800 — et le juge `releve-fiche-personne.py` le vérifie À L'ÉCRAN (pixels et doigt),
pas dans le DOM où l'ancienne fiche reste masquée. Le code de l'ancienne fiche reste dans le fichier (§9 : on ne nettoie
pas) mais **plus rien ne l'atteint** : `window.openPerson` est redéfinie, et tous les appelants passent par elle.

## G bis · LES PLANCHES — `PLANCHE-FICHE-PERSONNE.html`

Trois partis (A le velours · B le Noyau · C la Toile partagée), chacun en sombre, en clair et au Cercle, 390 × 844,
sphère et dalles rendues par l'app elle-même ; le **registre « rien ne se perd »** y reprend chaque ligne de § A bis et
dit ce qu'elle devient dans chaque parti. **Rien n'est intégré avant le choix de Tom.**

## G ter · TRANCHÉ PAR TOM (10 sept.) — ce qui reste · `PLANCHE-FICHE-PERSONNE-2.html`

Le nom, le visage, l'anneau sans chiffre (la forme de la liste : il compte TOUTE la liste), la liste des paroles
partagées — **Chiche compris** (le compagnon `avec` était ignoré : 2 rangées absentes au jeu de démonstration) — avec
leur état, leur date (`leJour`, quand elle existe), leur Nuée, et « + Planter un Promi » / « + Lancer un Chiche » (ce
dernier à valider). Tout le reste sort, sans remplacement. Planche : plein (Rachel) / vide (Nico) × deux thèmes. Q193.

## G · CE QUE L'AUDIT NE TRANCHE PAS — pour Tom

1. **La surface.** « Soyeuse, qui intrigue et attire » : ce que le produit a déjà de soyeux, c'est **le velours de
   la Pelote** — des vraies dalles sous une fourrure que le doigt peigne. Trois partis possibles, sans forme nouvelle :
   **(a)** la relation portée par la même matière — les Promi partagés avec cette personne, en îles sous le velours ;
   **(b)** la relation en Toile — les dalles partagées en pavage, comme la bande d'une Nuée ;
   **(c)** la fiche au plus sobre — plateau, visage, anneau du §2.9, et la liste avec ses vraies dalles enfin peintes.
   → à trancher au dessin.
2. **Ce qui reste en gratuit, ce qui va au Cercle** : le second anneau (§2.9, +9), la courbe (Q183), l'équilibre
   « toi ⟷ eux » (deux pourcentages : règle 1). → à trancher.
3. **Les mots sous le nom** : aucun mot de valeur ; faut-il une ligne, et laquelle (le moodboard n'en porte aucune) ? → à Tom.
4. **Les trois défauts qui ne sont pas des choix** — dalles jamais peintes, trait gris, colonne à 8, opacités, « votre » —
   se corrigent dans le lot, quel que soit le parti.
