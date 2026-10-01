# AUDIT — L'ACCUEIL (la Toile) · 13 septembre 2026

> app.html `e4c2d41a…`, **aucune ligne modifiée**. Tout est mesuré à l'exécution, deux thèmes, écran 390 × 844
> (viewport 430 × 932, `#device` exactement 390 × 844), gestes injectés par le CDP (§8).
> Sondes : `scratchpad/accueil_audit.py` (inventaire, écouteurs, commandes, zone libre, atteinte, pincement),
> `accueil_audit2.py` (friction, Toile pleine à 30 et 60), `acc_chiche.py` + `acc_chiche_piege.py` (le défaut au doigt),
> `acc_ixfil.py` (Index et Fil). Relevés bruts : `scratchpad/accueil_audit.json`, `accueil_audit2.json`, `acc_ixfil.json`.

## 1 · Les commandes — ce qui est vivant, ce qui ouvre quoi

| Nœud | Place (x·y·l·h) | Déclencheur | Ouvre | État |
|---|---|---|---|---|
| `#brandBtn` « Promi » | 22·62·177·65 | clic | **`sigmode`** sur tout l'appareil, gardé en `localStorage` | ⚠ **mode sans porte** (§ 3) |
| `#promiI` le « i » | 130·54 | — | clignote ; passe `.on` si un Promi est dû sous 1 jour | vivant, décoratif |
| `#subtitle` | 22·108·177·19 | — | « la Toile vit • 15 Promi vivants » / « la Toile attend » | vivant |
| `#cercleTopBtn` (cible) | 266·62·45·45 | clic | `#plusScreen` — le Cercle | vivant |
| `#settingsBtn` | 323·62·45·45 | clic | `#settingsScreen` — Réglages | vivant, **seule porte** des Réglages |
| `#viewSwitch` « Toile » | 269·126·47·35 | clic | rien (on y est déjà) | ⚠ inerte |
| `#viewSwitch` « Index » | 318·126·47·35 | clic (capture) | `#indexSheet` + scrim, puis le sélecteur **revient sur Toile à 240 ms** | ⚠ un sélecteur qui n'en est pas un |
| `#stage` / `#toileCv` | plein écran | toucher bref (< 700 ms, < 14 px) | la fiche de la dalle (`openDetail`) · une Nuée → `openEssaim` | vivant |
| `#stage` | plein écran | **appui long 480 ms** | `#studioScreen` | ⚠ **porte cachée**, doublon du Studio |
| `#toileCv` | plein écran | 1 doigt : glisser · 2 doigts : pincer | la vue (§ 4) | vivant |
| `#sidelabel` | 23·391 (vertical) | — | « LA TOILE · 15 » | redondant avec `#subtitle` |
| `#cap` | — | — | vidé à chaque `caption()` | **mort** |
| `#toileEmpty` | — | — | l'état « Ta Toile n'attend que toi » quand 0 Promi | vivant (non vu ici, 15 Promi) |
| `#studioBtn` | 47·746·44·44 | clic | `#studioScreen` | vivant |
| `#souffleBtn` « Aura » | 107·746·44·44 | clic | `#auraScreen` | vivant |
| `#createBtn` « + » | 167·740·56·56 | clic | `#createSheet` sur l'écran des choix (`pp-choix`) | vivant |
| `#filBtn` « Fil » | 239·746·44·44 | clic (document, capture) | `setView('fil')` → `#feedView.in`, `.v-fil` | vivant |
| `#filDot` | 269·749·9·9 | — | pastille terracotta : non lus + demandes en attente | vivant |
| `#shareBtn` | 299·746·44·44 | clic | `#shareScreen` | vivant |
| `#cellCard` (Tenue · Reporter · Gérer ›) | 75·249·240·131 | — | `openCell()` **n'est appelée nulle part** | **mort**, polices Arial, mots bannis (« brouillon », « échéance ») — ne pas le supprimer (§9), ne pas le ressusciter |

**Rien d'inatteignable** hors `#cellCard` : chaque fonction de l'accueil a au moins une porte visible. Deux portes cachées
(appui long → Studio, mot-marque → `sigmode`) et une animation d'amorce (`promi_sigdemo` : au premier lancement,
le `sigmode` s'allume 1,25 s tout seul) — aucune n'est nommée dans l'app.

## 2 · Planter — la friction mesurée

- **Deux touchers** jusqu'à la phrase, pour les trois natures : `+` → écran « Qu'est-ce que tu promets ? »
  (trois tuiles 358 × 174 à y 246 · 436 · 626) → tuile → phrase.
- ⚑ **DÉFAUT RÉEL, AU DOIGT SEULEMENT — la tuile « Un Chiche » ouvre un Promi.**
  Souris : Chiche → `pp-chiche`, verbe « Chiche » (4/4). Doigt (CDP et `tap` Playwright, deux méthodes) :
  Chiche → `pp-promi`, verbe « Je me promets » ; et après une Nuée, la tuile Promi laisse `data-kind="nuee"`.
  **Pris au piège** (`acc_chiche_piege.py`) : le carrousel HORIZONTAL d'origine (l. 8805-8811) écoute toujours
  `touchstart`/`touchend`. Au lever du doigt, `up()` rejoue `goTo(cur)` — la tuile d'AVANT — donc
  `data-kind=promi`, l'écran passe à la phrase **sous le doigt**, et le clic synthétisé tombe sur `planterCv`
  au lieu de la tuile. C'est la famille « le clic fantôme » (§8). **Sur un téléphone, on ne peut pas lancer un
  Chiche depuis le `+`.** Aucune batterie ne le voit : elles jouent à la souris.
- Le `+` pèse **56 px** contre 44 pour ses voisins : il n'est pas le centre de l'écran, il est un bouton parmi cinq.

## 3 · Les infractions à la DA et au CLAUDE.md

| # | Où | Mesuré | Règle |
|---|---|---|---|
| 1 | `.tc` ×2, `.dctrl` ×4 | trait **1 px**, rayon **16** sur 45 et 44 | §5 grammaire : 2 px, couleur du corps, disque = rayon 50 % |
| 2 | `#viewSwitch` | 102 × 41, trait 1 px, rayon 10 ; boutons rayon 10 | §5 : rayon = h ÷ 2 |
| 3 | `#createBtn` | trait 1 px, fond translucide + **`backdrop-filter: blur(12px)`** | §4 règle 4 : aucun filtre devant une dalle |
| 4 | `.dctrl`, `.tc` | même `blur(12px)` sur les deux thèmes | idem |
| 5 | `.stage-fade-b` (390 × 150, z 20) · `.stage-fade-t` (200 × 210) | voiles `--surf` 55 % par-dessus le canevas | §4 règles 3-4 : aucun voile devant une dalle |
| 6 | anneau du `+` | tenu en **`#D0B0FF`** (lilas), + dessiné en `#D0B0FF` | §3 : tenu = **menthe `#2BE88C`** ; `#D0B0FF` n'est dans aucune palette signal |
| 7 | libellés du dock | **ApfelMid 10 px** | §6 : rien sous 12 px |
| 8 | `#sidelabel` | 10 px, **opacité 0,7** ; tourné à `left:-2px`, « LA » rogné sur la capture de Tom | §6 : ≥ 12 px, ≥ 72 % |
| 9 | icône Réglages | trait **`#55576c`** | §3 : jamais de trait neutre ou gris |
| 10 | mot-marque | « Promi » en **Bricolage 44/700**, « i » bleu | §5 : Fraunces, 20 px (le `sigmode` seul le passe en Fraunces) |
| 11 | tout le haut | aucun plateau ; les autres écrans portent le plateau 342 × 60 à 24·40, trait 2, rayon 30 | DA du produit (Studio, Réglages, Index, Fil) |
| 12 | `#subtitle` sur la Toile | aucune réserve : au zoom et Toile pleine (60), le titre passe **sur les dalles et sur leurs libellés** — capture `scratchpad/acc_plein_60.png` | §3 ton sur ton ; `Toile.reserve` n'est posée que par l'onboarding |
| 13 | icônes `#cercleTopBtn` (une cible) et `#settingsBtn` (un disque à trois rayons) | ni l'une ni l'autre ne se lit | test ÉVIDENT (§10) |
| 14 | `updatePulse()` | variable `urgent` | §2 terme banni « même en interne » — noté, pas un renommage à faire dans un lot d'écran |

## 4 · La Toile manipulable — le zoom

**Le moteur** (l. 8277-8282, `cp()`, boucle l. 7764-7774) : pincement de **0,4 à 5** ; au repos la boucle ramène
sous **0,48**. En dessous de 1, la Toile entière reste dans l'écran et se déplace librement ; au-dessus, ses bords
restent collés aux bords de l'écran. **À 1, aucun déplacement possible.**

**Atteinte de chaque dalle, à chaque zoom** — calcul exact : `Toile.hit` est pur, on émule chaque vue admissible
(13 × 13 cadrages dans la borne de `cp()`), on garde un point de la dalle qui (a) tombe sur la zone libre — où
`elementFromPoint` rend `#toileCv`, relevée tous les 4 px — et (b) où `hit` rend BIEN cette dalle.

| Toile | zooms testés | dalles | inatteignables |
|---|---|---|---|
| jeu de démonstration (15), clair et sombre | 0,4 · 0,48 · 0,6 · 0,7 · 0,8 · 0,9 · 1 · 1,25 · 1,5 · 2 · 3 · 5 | 15 | **0 à tous les zooms** |
| pleine, 30 | 0,48 → 5 | 30 | **0** |
| pleine, 60 | 0,48 → 5 | 60 | **0** |

La zone libre fait **86,3 %** de l'écran. Au-delà de 1, il faut glisser (à 5 : 54 des 60 dalles demandent un
déplacement) — c'est attendu. **La marge est ce qui protège ce résultat** : toute planche qui ajoute du chrome se
repasse dans ce calcul avant d'être retenue.

**Au doigt (CDP, pincement réel)** :

| Moment | Vue mesurée |
|---|---|
| pincement 300 → 60 px | s 0,40 |
| relâché, 1,5 s | s 0,40 — **tient** |
| glisser | s 0,40, ox 129 → 54 — **tient** |
| une dalle touchée au dézoom | sa fiche s'ouvre (`#detailPoster`) ✔ |
| fiche fermée | s **0,48** — ressort de 0,40 à 0,48 (deux bornes différentes) |
| aller au Fil et revenir | s 0,48 — tient |
| `Toile.sync()` (appelée par toute plantation) | s **1** — le cadrage automatique reprend la main |
| pincement avant | s 5 — tient |

Deux défauts de tenue : **le ressort 0,40 → 0,48** et **la vue qui revient à 1 après une plantation** (voulu par
`autoView`, « la vue recule d'un cran », mais contraire à « qu'on puisse dézoomer et que ça tienne »). Et **aucun
geste pour revenir au cadrage** après un zoom : il faut pincer en sens inverse.

## 5 · Index et Fil — ce que la fusion coûte, mesuré

Les deux écrans ont **le même haut, au pixel** : titre Bricolage 27 à 52·57, compte, ✕ FERMER à 264·63, recherche
270 × 52 et tri 52 × 52 à y 116, liste à **y 204**, deux thèmes.

- **Ce qui tient** : un sélecteur **à la place du titre**, dans le plateau (« Index · Fil »), ne coûte **0 px** — la
  liste reste à 204. Un sélecteur **sous la recherche** (celui de la grammaire, 44 de haut, 12 d'air au-dessus, la liste gardant ses 36) coûte **56 px** de liste.
- **La barre** : à 12 px, « Index · Fil » mesure 67,6 et « Partager » 64. Dans la barre à cinq places (70 d'entraxe) il reste **4,2 px d'air** entre eux — **la barre à cinq ne tient pas avec ce mot**. Elle passe à trois entrées (Partager monte au plateau) : elle se simplifie, mais par obligation.
- **Ce que ça libère** : le `#viewSwitch` du haut (102 × 41) disparaît, avec son bouton « Toile » inerte.
- **Ce que ça ne fait pas tout seul** : l'Index n'est plus dans la barre depuis longtemps — il vit en haut. Fusionner ne
  retire donc aucune entrée de la barre ; c'est la longueur du mot qui en retire une (ci-dessous).
- **Ce qui complique, dans le code** : l'Index est une **feuille** (`#indexSheet.show` + scrim), le Fil une **vue**
  (`#feedView` + `.in` + `.v-fil`, la Toile passe en `display:none` à 380 ms, `_majSelFil` masque le sélecteur en
  ligne). Deux conteneurs, deux mécaniques d'ouverture, deux menus de tri différents (Index : tri · Fil : 4 tris +
  8 filtres). Le sélecteur basculerait entre les deux conteneurs existants — pas de fusion de code — mais chaque
  bascule passe par `closeAll`, ses rangeurs et les inline du §8. Et **la pastille du Fil** doit vivre à deux
  endroits : sur le bouton de la barre, et sur l'onglet « Fil ».

## 6 · Ce qui ne doit pas se perdre

Réglages (seule porte : `#settingsBtn`) · le Cercle (`#cercleTopBtn`, et d'autres portes ailleurs — chantier 74) ·
la pastille du Fil · l'anneau de proportions du `+` (il DIT quelque chose) · l'état vide `#toileEmpty` · le toucher
d'une dalle et d'une Nuée · le pincement et le glisser · le compte des Promi vivants.
À trancher, pas à perdre en silence : le `sigmode` et l'appui long → Studio.
