import io
S=io.open('CLAUDE.md',encoding='utf-8').read()
old="""### ⚑ v129 (4 oct. 2026) — L'ONBOARDING, TEXTE FIGÉ ; « CERCLE » CENTRÉ ; LE MODE DESSIN LIBÈRE L'ÉCRAN. (Décisions Tom.)"""
new="""### ⚑ v130 (5 oct. 2026) — TROIS RÉCIDIVES NOMMÉES ; TROPICAL BREEZE ; LE MODE DESSIN NE RECOUVRE JAMAIS LA BANDE. (Décisions Tom.)
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
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — cinquième principe : AUCUNE SUPERPOSITION SUR L'ESPACE DE DESSIN.** Tom retient la
> rangée A, sous la bande. Ni rangée, ni menu de tailles, ni couleurs dans la bande : la page se réorganise. Promi et Chiche : les trois
> lignes du bas descendent (36 pt sur la planche), espacements gardés ; la rangée est sous le trait avec un écart franc (24 pt proposé) ;
> tailles et couleurs se déploient SOUS la rangée. Cercle : tout est masqué sous la bande sauf le titre. Tout revient à POSER ou à la sortie.

### ⚑ v129 (4 oct. 2026) — L'ONBOARDING, TEXTE FIGÉ ; « CERCLE » CENTRÉ ; LE MODE DESSIN LIBÈRE L'ÉCRAN. (Décisions Tom.)"""
assert S.count(old)==1; S=S.replace(old,new)
old="""                bande (nature)   corps clair   corps sombre     (PROMI-TOKENS.json, repris le 30 sept. 2026)
Promi           #82AEF8          #CFE5FE       #0D1F33"""
assert S.count(old)==1
old2="""le corps SOMBRE est celui de v113 (Q358) : **`#335382` · `#7C3F58` · `#5D4978`** (le Cercle : valeur posée par v113, pas
> une citation de Tom)."""
assert S.count(old2)==1; S=S.replace(old2, old2+"""
> **⚑ v130 — le corps sombre d'un PROMI est `#8ACBE8` (Tropical Breeze), texte à l'encre ; Chiche et Cercle ne bougent pas.**""")
old3="""python3 redteam_motmarque.py   # 4 — v129 (C-046)"""
assert S.count(old3)==1; S=S.replace(old3, """python3 redteam_reactif.py     # 30 — v130 (C-049) : planter, tenir, retirer par les vrais boutons ; l'Index, le Fil, la liste de l'Aura et le fil du Cercle
                               #   sont à jour à l'image suivante, complets — écran resté affiché, ou ouvert ensuite. Rougit sur v129 (25/30).
"""+old3)
io.open('CLAUDE.md','w',encoding='utf-8').write(S)
