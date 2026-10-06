import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
C=lit('CLAUDE.md')
a=C[C.index("> **⚑ L'AMPLEUR À MI-FORCE SOUS DIX MONDES (C-062)**"):C.index("> **⚑ LA GRILLE ANTI-COERCITION EST AU §12**")]
C=C.replace(a,"""> **⚑ L'AMPLEUR À MI-FORCE, SOUS SIX MONDES (C-062)** — `_AMP_MI` dans le moteur : à l'ampleur stable de chaque parole (titre et personne)
> s'ajoute `force × (−0,07 + 0,40·u⁴)` : Esquille, Ritournelle 0,3 · Ramage 0,6 · Mascaret, Volubilis 1 · Chamade 1,5. Elle se recalcule au
> changement de monde. **Halin, Guingois, Chantourné et Brouillamini en sont RETIRÉS : elle y allongeait l'arrivée d'une dalle de 11 à 38 %
> (`redteam_rythme`), et le rythme validé ne dérive pas — arbitrage de Tom (Q411).** Madrure, Bobinette et les huit anciens ne bougent pas.
> La taille ne porte toujours aucun sens. `banc_rendu` est refigé pour ces six mondes, et eux seuls.
> ⚠ **`banc_rendu` : Guingois et Chantourné diffèrent de la référence DEPUIS AVANT ce lot** (vu avec le moteur de v134 ; le banc n'avait pas
> tourné depuis v130) — non refigés, ouverts (C-066).
""")
a="> **⚑ LA PAGINATION DES MONDES AU STUDIO EST UNE RANGÉE DE BARRETTES**"; i=C.index(a); j=C.index("> **⚑ L'AMPLEUR À MI-FORCE, SOUS SIX MONDES",i)
C=C[:i]+"""> **⚑ LA PAGINATION DES MONDES AU STUDIO EST UNE RANGÉE DE BARRETTES** (10 × 4, la courante 18 × 4), plus des points : la loi des points.
> **⚑ LE MENU DES PALETTES « VIDE » (C-011) — LA CAUSE N'EST PAS NOMMÉE.** La capture de Tom (reçue en cours de lot) montre les 24 pastilles
> réduites à des points, le nom sans son style, la jauge sans hauteur : dans le panneau, les règles de BASE (`.st3-p`, `.st3-orb`, `.st3-q`,
> `.st3-pn`, `.st3-spec`) n'avaient pas pris. Non reproduit (WebKit et Chromium, trois tailles de fenêtre, vingt mondes, gratuit et payé,
> trois ouvertures). **Parade** : `#studioScreen #stpPals` porte en propre tout ce dont une pastille, le nom et la jauge ont besoin.
> `redteam_palettes` (58) compte les teintes PEINTES de chaque pastille sur la capture (`--sonde=vide` : il rougit).
"""+C[j:]
ecrit('CLAUDE.md',C)
L=lit('CHANTIERS.md').rstrip('\n').split('\n')
def maj(n,etat,preuve,juge,vise):
    for i,l in enumerate(L):
        if l.startswith('| %s |'%n):
            c=l.split(' | '); assert len(c)==7; c[3]=etat; c[4]=preuve; c[5]=juge; c[6]=vise+' |'; L[i]=' | '.join(c); return
    raise Exception(n)
maj('C-011','EN COURS','v135 : la capture est arrivée en cours de lot — 24 pastilles réduites à des points, nom sans style, jauge sans hauteur : les règles de base des pastilles n’avaient pas pris dans le panneau. CAUSE NON NOMMÉE : non reproduit (WebKit, Chromium, trois tailles de fenêtre, vingt mondes, gratuit et payé). Parade posée : le panneau porte en propre le style des pastilles, du nom et de la jauge. La pagination des mondes (les vrais « points ») est passée en barrettes. Le juge compte les teintes peintes (sonde `vide`).','redteam_palettes 58/58','Tom vérifie ; sinon : sur quel appareil, après quel geste')
maj('C-062','EN COURS','v135 : `_AMP_MI` (force × (−0,07 + 0,40·u⁴)) sous SIX mondes — Esquille, Ritournelle 0,3 · Ramage 0,6 · Mascaret, Volubilis 1 · Chamade 1,5. RETIRÉE sous Halin, Guingois, Chantourné, Brouillamini : elle allongeait l’arrivée d’une dalle de 11 à 38 % (redteam_rythme) — arbitrage de Tom (Q411). Bobinette : mesuré 0,46 / 0,57, non touché. Tableau des CV au rapport ; planches `planche-v135/tailles-1`, `-2` (faites avec les dix).','redteam_rythme · banc_rendu (refigé pour les six)','attend Q411')
L.append("| C-066 | 7 oct. · trouvé en v135 | `banc_rendu` : Guingois et Chantourné diffèrent de la référence depuis AVANT v135 (constaté avec le moteur de v134 ; le banc n'avait pas tourné depuis v130). À nommer : instabilité du banc sous ces deux mondes, ou changement de rendu non refigé (v128, mouvements écrits dans le peintre de Chantourné ?). | OUVERT | v135 : `python3 banc_rendu.py --monde=guingois` et `--monde=chantourne` rouges sur l'état d'avant le lot ; non refigés. | banc_rendu | v136 |")
ecrit('CHANTIERS.md','\n'.join(L)+'\n')
Q=lit('QUESTIONS.md').rstrip('\n')+'''
- **Q411 — OUVERTE (C-062)** : sous Halin, Guingois, Chantourné et Brouillamini, l'ampleur allonge l'arrivée d'une dalle (Halin 2 526 ms pour
  2 270 ± 181 ; Brouillamini 1 941 pour 1 742 ± 139 ; Guingois 2 326 pour 1 722 ± 137 ; Chantourné 2 317 pour 1 677 ± 134). Retirée sous ces
  quatre. Tom accepte-t-il une arrivée plus longue pour y gagner en variété, ou reste-t-on au rythme validé ?
- **Q408 — MISE À JOUR** : la capture du Studio est arrivée ; la cause reste non nommée, une parade est posée (C-011).
'''
ecrit('QUESTIONS.md',Q)
E=lit('ETAT-DES-LIEUX.md')
E=E.replace("| v135 | Le Studio : la pagination en barrettes ; le menu des palettes (C-011, non reproduit) | `redteam_palettes` 58/58 | ouvrir, fermer, rouvrir, ouvrir le menu en sombre : si le menu est vide, une capture d'écran envoyée autrement (elles n'arrivent pas dans le message) |","| v135 | Le Studio : le menu des palettes (C-011, cause non nommée, parade posée) ; la pagination en barrettes | `redteam_palettes` 58/58 | refaire le chemin de la capture (sombre, Ramage, ouvrir le menu) : les 24 pastilles et la jauge ; s'il revient vide : sur quel appareil, après quel geste |")
E=E.replace("sous Esquille, Halin, Brouillamini, Ramage, Guingois, Chantourné, Volubilis, Chamade, Ritournelle, Mascaret, avec vingt paroles et plus","sous Esquille, Ritournelle, Ramage, Mascaret, Volubilis, Chamade, avec vingt paroles et plus (Halin, Guingois, Chantourné, Brouillamini : retirée, Q411)")
ecrit('ETAT-DES-LIEUX.md',E)
P=lit('portage/A-INTEGRER.md').replace("- **Moteur** : `_AMP_MI` — ampleur à mi-force sous dix mondes (SPEC-RENDU §a) ; le banc de rendu est refigé pour eux.","- **Moteur** : `_AMP_MI` — ampleur à mi-force sous SIX mondes (Esquille, Ritournelle, Ramage, Mascaret, Volubilis, Chamade ; SPEC-RENDU §a) ; le banc de rendu est refigé pour eux. Guingois et Chantourné diffèrent de la référence du banc depuis avant v135 (C-066).")
ecrit('portage/A-INTEGRER.md',P)
