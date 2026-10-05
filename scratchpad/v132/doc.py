import io
S=io.open('CLAUDE.md',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""### ⚑ v131 (5 oct. 2026) — LE COBALT REMPLACE TROPICAL BREEZE""",
"""### ⚑ v132 (5 oct. 2026) — LE DESSIN EST CONSTRUIT DANS L'APP. (Décisions Tom.) Ce bloc CORRIGE ce que les blocs v127 à v131 disent de l'outil de dessin.
> **« On ne fait plus de planche : on construit, et Tom juge au doigt sur iPhone. »** Choix : **effilé E2, symbole de couleur S2** (celui du
> Studio). **Les planches v130 et v131 sont ABANDONNÉES** (elles laissaient la surface coincée en haut et un vide dessous).
> **⚑ LA MISE EN PAGE DU MODE DESSIN** (`lot-V132-DESSIN`, fiches Promi, Chiche, Cercle et page +) : **la surface de dessin prend toute la
> place, du haut de l'écran jusqu'à la rangée d'outils ; la rangée A (PLUME · GOMME · ANNULER · COULEUR · POSER) est EN BAS, à portée de
> pouce ; tailles et couleurs se déploient juste AU-DESSUS d'elle et se replient dès le choix fait ; tout le reste de la fiche se retire ;
> l'encart du haut ne garde que son contour au trait fin ; tout revient à POSER ou à la sortie, sans fondu.** Le mode est une couche PLEINE
> posée dans `#device` : la fiche dessous n'est pas touchée (le retour est exact par construction). **Les paramètres sont en tête du lot**
> (`window._dessinParams` : `RANGEE_H` 44 · `MARGE_BAS` 34 · `MARGE_HAUT` 12 · `MARGE_COTE` 24 · `PAS_OUTIL` 58 · `POSER_L` 104 ·
> `ECART_DEPLOI` 8 · `TAILLES` 2,5 / 4,5 / 8 · `TAILLES_GOMME` 10 / 18 / 30 · `BANDE_RETRAIT` 7). La surface fait 390 × 754 pt.
> **⚑ UN DESSIN EST UNE LISTE DE TRAITS, JAMAIS UNE IMAGE** : `{fond, traits:[{c, t, g, pts}], poses, pose, masque}` — sur la parole
> (`p.dessin`, sauvegardé avec elle), sur le brouillon de la page + (`_phrase.dessin`, il suit la parole ou le Cercle à la plantation), ou par
> Cercle (`localStorage promi_dessins_cercle`). **Chaque trait garde SA couleur** (un hex) : un changement de palette ne touche que les traits
> à venir. `traits` = le dessin en cours (gardé si l'on sort) ; `poses` = ce que POSER a posé (la bande, la vue entière et le partage ne
> montrent que lui). **Après le premier POSER, le fond est fixé (plus d'onglet FOND) et les nouveaux traits ne prennent que les couleurs
> déjà présentes.** Le trait : plein, opaque, contours nets, effilé E2 (début +38 %, fin effilée sur le dernier quart), plus fin quand le
> geste est rapide (jusqu'à −28 %), la pression d'un stylet module la largeur, jamais sous 1 pt.
> **⚑ LE DESSIN REMPLACE LA DALLE OU LA PHOTO DANS LA BANDE** : une couche pleine (`canvas.dz-bande` : le fond du dessin puis ses traits, à
> l'échelle 1, calés EN HAUT) posée sur la bande, découpée à 7 pt au-dessus de l'axe du trait d'état. Le dessin est plus grand que la
> bande : la fiche en montre le haut ; **toucher la bande l'ouvre en entier (C-051, « Voir le dessin en entier »)**. Rien n'est relu ni
> retouché dans le canevas de la bande : « Retirer le dessin » rend la dalle. **Le masquage** (`button.dz-oeil`, coin bas gauche de la
> bande) est pour soi seul, mémorisé par fiche ; **un dessin masqué n'est jamais emporté dans un partage** (`window._dessinCase`, lu par la
> case du Folio). **Les entrées** : « Dessiner » en tête du menu du bouton photo, devenu COMPACT (33 pt, 4 pt entre deux, posé À GAUCHE du
> bouton) — sur la fiche, sur la page + (Promi, Chiche, Cercle : le bouton y ouvre le menu, plus l'import direct) et sur la fiche d'un
> Cercle, qui reçoit son bouton photo. La loi des points : seul le choix de taille (trois points) y échappe (§5).
> ⚠ **Trois pièges payés** : ① une couche ajoutée à `#detailPoster` sort en `display:none` (le crible) — on la déclare visible nommément ;
> ② `_dalleReelle` (dans `sharePlanche`) est du code MORT : la case du Folio passe par `_poseDalle` ; ③ le menu posé au-dessus du bouton
> passait sous le plateau dès quatre lignes.
> ⚠ **OUVERT** : il n'y a pas de bouton de SORTIE sans poser (Échap et la fermeture générale sortent en gardant le dessin en cours) — Q392.
> Juge : **`redteam_dessin.py`** (63 contrôles : couleurs figées sous trois palettes, masquage et partage, aucune superposition, retour exact
> après POSER, joignabilité et VoiceOver, les entrées) ; **cinq sondes** (`--sonde=couleurs|partage|superpose|retour|joignable`) fabriquent
> la version fautive, il y rougit à chaque fois. **C'est un geste : la validation de Tom sur iPhone est obligatoire.**
> **⚑ « CE QUE TU AS TENU » : LA PLUS RÉCENTE EN PREMIER** (corrige v131) — la parole qu'on vient de tenir se voit sans défiler.
> **⚑ SUR LE COBALT** : la phrase lilas de la page + d'un Promi (sombre) est **`#DAC3FF`** (`--c-lilas85`, la teinte de `#C4A2F5` éclaircie à
> 4,51:1 ; le jeton `--c-mauve75` y est remplacé, sur cet écran seulement) ; **« SUPPRIMER CE PROMI » est crème en sombre, encre en clair —
> `#DD4D23` est une couleur d'état et ne sert à rien d'autre** (C-015 reste ouvert pour les Réglages).

### ⚑ v131 (5 oct. 2026) — LE COBALT REMPLACE TROPICAL BREEZE""")
rep("""python3 redteam_entier.py      # 36 — v131 (C-051)""","""python3 redteam_dessin.py      # 63 — v132 (C-042) : le dessin dans l'app — couleurs figées (trois traits, trois palettes), masquage absent du partage, aucun outil
                               #   sur la surface, retour exact après POSER, joignabilité et VoiceOver, les entrées. Cinq sondes (--sonde=) : il y rougit.
python3 redteam_entier.py      # 36 — v131 (C-051)""")
io.open('CLAUDE.md','w',encoding='utf-8').write(S)
D=io.open('DESSIN-INVENTAIRE.md',encoding='utf-8').read()
D+="""
## v132 (5 oct. 2026) — CONSTRUIT DANS L'APP (`lot-V132-DESSIN`) ; les planches v130 et v131 sont abandonnées
- Choix de Tom : effilé **E2**, symbole **S2**. La surface prend tout l'écran jusqu'à la rangée, posée en bas ; les déploiements au-dessus
  d'elle ; le reste de la fiche se retire. Paramètres : `window._dessinParams`. Détail : bloc v132 de `CLAUDE.md`. Juge : `redteam_dessin.py`.
"""
io.open('DESSIN-INVENTAIRE.md','w',encoding='utf-8').write(D)
P=io.open('portage/A-INTEGRER.md',encoding='utf-8').read()
P+="""- **C-042 · le dessin (v132, construit dans le prototype)** : un dessin est une LISTE DE TRAITS (`{fond, traits:[{c, t, g, pts:[x,y,t,p…]}],
  poses, pose, masque}`), en points sur une surface de 390 × 754 — jamais une image ; chaque trait garde sa couleur ; `poses` est ce que
  POSER a posé. En Swift : `PKCanvasView` ne convient pas tel quel (couleurs figées, effilé E2, gomme qui rend le fond) — un rendu à soi
  (`Path` remplis), le même modèle de largeur (`largeurs` dans `lot-V132-DESSIN`). Mode dessin : la surface plein écran, la rangée en bas.
"""
io.open('portage/A-INTEGRER.md','w',encoding='utf-8').write(P)
Q=io.open('QUESTIONS.md',encoding='utf-8').read()
Q+="""

## LOT v132 — 5 octobre 2026 (les décisions vivent dans CHANTIERS.md : C-042, C-052, C-053, C-054)

- **Tranché par Tom** : E2 et S2 ; on construit le dessin dans l'app ; la surface plein écran, la rangée en bas (Q391 close) ; la liste de
  l'Aura, la plus récente en premier (Q390 close) ; « SUPPRIMER CE PROMI » en crème, la phrase lilas éclaircie à 4,5:1 → `#DAC3FF` (Q389 close).
- **Q392 — À TRANCHER (Tom)** : la SORTIE du mode dessin sans poser. Aucun bouton ne la porte (la rangée décidée n'en a pas, l'encart du
  haut n'a plus de texte) : aujourd'hui seuls Échap et la fermeture générale sortent, en gardant le dessin en cours. Sur iPhone, on ne sort
  donc que par POSER (ou ANNULER jusqu'au vide, puis POSER, qui ne pose rien).
- **Q393 — À VALIDER (Tom)** : en clair, « SUPPRIMER CE PROMI » passe à l'encre (pas à la crème, illisible sur le corps crème) ; les
  Réglages (« Supprimer mon compte ») gardent `#DD4D23` — C-015.
- **Q394 — À VALIDER (Tom)** : les tailles de la gomme (10 · 18 · 30 pt), le fond par défaut du dessin (le champ de la nature), les cinq
  fonds proposés (le champ, puis la palette), et le dessin d'un Cercle hors du partage (son Folio ne montre que ses Promi).
- **Q395 — À VALIDER (Tom)** : les cartes de l'Index et du Fil gardent la dalle (le dessin ne remplace que la bande).
"""
io.open('QUESTIONS.md','w',encoding='utf-8').write(Q)
E=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read()
old="\n## ⚑ À VALIDER SUR IPHONE — liste tenue à jour (ouverte en v123)"; assert E.count(old)==1
E=E.replace(old,"""- **v132 (5 oct.)** — **LE DESSIN EST CONSTRUIT** (`lot-V132-DESSIN`, C-042) : surface plein écran, rangée en bas, traits figés, masquage, vue entière, partage ; `redteam_dessin` 63/63, cinq sondes. Liste de l'Aura : la plus récente en premier (C-052). `#DAC3FF` (C-054), « Supprimer ce Promi » en crème (C-053). Q392–Q395.
"""+old)
for a,b in (("| v131 | « Ce que tu as tenu » : toutes les paroles tenues, l'Aura défile (C-052) |","| v131 | « Ce que tu as tenu » — *complété par la ligne v132 (la plus récente en premier)* (C-052) |"),
            ("| v131 | L'outil de dessin (C-042) : la mise en page corrigée — choisir E1/E2, S1/S2 |","| v131 | L'outil de dessin (C-042) — *remplacé par la ligne v132 (construit)* |")):
    assert E.count(a)==1,a; E=E.replace(a,b)
E=E.rstrip('\n')+"""
| v132 | **LE DESSIN (C-042) — un geste : validation au doigt obligatoire** | `redteam_dessin` 63/63, cinq sondes | la marche à suivre en cinq étapes du rapport v132 : dessiner sur une fiche Promi, tailles et couleurs, POSER, vue entière, masquer ; puis un Cercle et la page + ; la sortie sans poser (Q392) |
| v132 | « Ce que tu as tenu » : la plus récente en premier (C-052) | `redteam_reactif` 31/31 | tenir une parole : elle est la première de la liste, sans défiler |
| v132 | Sur le cobalt : la phrase de la page + en `#DAC3FF` (C-054), « SUPPRIMER CE PROMI » en crème (C-053) | `redteam_decisions` 85/85 | page + d'un Promi en sombre ; Peaufiner d'une fiche, tout en bas, en sombre et en clair (Q393) |
"""
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write(E)
print('docs ok')
