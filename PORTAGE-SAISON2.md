# Portage des sept mondes saison 2 au contrat — feuille de route

Source des rendus : `Promi - Trois matières.dc.html` (classe `Component`), qui fait foi pour l'aspect.
Contrat : `uploads/CONTRAT-MONDE-2ddb6539.md`. Écarts : `uploads/MONDES-SAISON2-MANQUES.md`.
Modèle de portage : `promi-mondes.js` et `INTEGRATION-MONDES.md` (Esquille, Bobinette, Ritournelle, Madrure).

## Décisions tranchées (27 sept.)
1. **u = avg()** du moteur. Aucun W, aucun pixel, aucune renormalisation `k = W/300`.
   - Mondes contenus dans `dalleTrame` : lire l'unité sur le poids ou sur la distance à la graine voisine (contrat §5.2).
2. **Générateur : le LCG du contrat**, amorcé par la clé stable : `_dalleDeCle`, le nom de la Nuée, ou la position arrondie pour une cellule vide.
   - Les tirages changent : c'est accepté.
   - Aucun tirage ne doit venir d'une position calculée. À corriger : l'asymétrie d'arête de Guingois, les épines et la coupe des traits de Mascaret.
3. **Ordre, les plus légers d'abord :** Brouillamini → Chamade → Volubilis → Guingois → Chantourné → Mascaret → Ramage.
   - Mascaret et Ramage seront réécrits pour tenir le budget : cache des tracés, invalidé à la plantation, au changement de palette, de thème ou de semis, et à `_palLit`.
4. **Toile sans promesse :** la matière du monde, dense et belle, **jamais du papier nu**. C'est le premier écran vu.
   - Brouillamini à 97 % de papier est refusé : il faut une matière.
5. **Offre : deux gratuits, cinq au Cercle.** Proposition, que l'utilisateur doit trancher :
   - **Brouillamini** : la plus sage, lisible et joyeuse ; elle donne le principe de la dalle-forme sans le relief des autres.
   - **Chantourné** : discret, textile, élégant ; il montre qu'une matière peut porter la promesse.
   - Au Cercle : Ramage, Mascaret, Volubilis, Chamade, Guingois, les plus spectaculaires.
6. **Une Nuée compte comme une promesse.** Braille garde son nom. Halin existe depuis v49.
7. **Aucune promesse sans dalle, jamais.**
   - Mascaret : 2 sur 120 sans dalle.
   - Guingois : 14 sur 120 sans dalle.
   - À régler dans leur passe : chaque promesse a au moins un trait ou une case, avec son contour, son toucher et sa dalle seule.
8. `coeurs` est défini deux fois : **la seconde (l. 2398) est la bonne**. La première (l. 1054, ancien Chamade) est à supprimer.

## À faire pour chaque monde (checklist d'une passe)
- Signature `Rnom(now, x0, y0, x1, y1)`, inscrite au registre, avec sa déclaration **LIBRE** ou **contenu** / PER.
- Couleurs seulement par `cOf(s, now)`, `curPAL()` et la rampe `TH[monde]` (5 tons), plus `fondToile()`.
  - Aucune couleur écrite en dur : ni `#FFFFFF`, ni `#000`, ni l'objet `T` de la planche.
  - Toute « découpe » en couleur de papier est à remplacer par un tracé en pair-impair ou par `fondToile()`.
- Longueurs en fraction de u, y compris les pas d'échantillonnage et les marges.
- `contour(s)` : le contour réellement peint.
- `toucher(x, y)` : le test sur ce contour. C'est indispensable là où la dalle est déplacée : les fleurs de Volubilis, les cœurs de Chamade.
- `nature(s)`.
- `seule(s, …)` identique à la dalle sur la Toile.
  - Volubilis : le cœur de fleur doit être en papier, pas à 72 % de blanc.
  - Ramage : vérifier les recouvrements par les plumes de matière.
- **Arrivée et départ :** `env.trans`, `transDur`, et `now` seulement pour la transition.
  - La reconstruction doit être **locale**, limitée aux voisines, pour qu'une plantation ne recompose pas tout d'un coup.
  - Sinon, fondu entre l'ancien et le nouveau tracé, sur la durée du moteur.
- Mesurer à la méthode du contrat : dix canevas distincts, une relecture chacun, puis l'écran, en Chromium et en WebKit.
  - Budget : **≤ 16,7 ms**.
  - Attention au piège WebKit : un `clip()` par forme (§8).

## Coûts mesurés au départ (40 promesses, Chromium · WebKit, en ms)
- Ramage : 470 · 409
- Chantourné : 201 · 191
- Brouillamini : 38 · 61
- Mascaret : 489 · 349
- Volubilis : 16 · 11, plus 500 à 900 de construction par plantation
- Chamade : 54 · 75
- Guingois : 178 · 86, plus 90 à 180 de construction
