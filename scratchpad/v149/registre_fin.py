# v149 : les lignes du registre — état, preuve, juge, lot (colonnes 4 à 7), par numéro
import io, re
S = io.open('CHANTIERS.md', encoding='utf-8').read()
L = S.split('\n')
MAJ = {
 'C-124': ('FAIT, EN ATTENTE DE TOM', "v149 : Promi, Chiche, Cercle en GRAS partout dans l'onboarding ; en sombre `#82AEF8`, `#FFB8D2`, `#C9A8F5` exacts ; en clair la teinte foncée à 3:1 sur `#DFCAA4` (`#4870B5` 3,08 · `#9D5E77` 3,05 · `#8262A9` 3,07 — Q538) ; « Le reste se découvre en traçant. » → « Tout le monde promet. Toi, tu tiens. », même place, rôle liste, tracé. v148 : « Promi planté ! » pas à pas, l'Atkinson −7 %.", "redteam_onb_mots 44/44 (15/42 sur v148), redteam_onboarding_texte, redteam_echelle_onboarding, redteam_onb_sorties", 'v149'),
 'C-139': ('VALIDÉ PAR TOM', "v149 : clos SANS invitation animée — « le chevron orange suffit » (Tom). Aucune invitation dans l'app ; la page de variantes reste pour mémoire.", None, 'v149'),
 'C-141': ('VALIDÉ PAR TOM', None, None, None),
 'C-143': ('VALIDÉ PAR TOM', None, None, None),
 'C-144': ('VALIDÉ PAR TOM', None, None, None),
 'C-146': ('VALIDÉ PAR TOM', None, None, None),
 'C-147': ('VALIDÉ PAR TOM', None, None, None),
 'C-148': ('VALIDÉ PAR TOM', None, None, None),
 'C-145': ('FAIT, EN ATTENTE DE TOM', "v149 (rouvert) : les deux phrases du guide encore 60 pt plus haut (centre 312 → 252,5) ; « Studio » × 1,11 (29 → 32,2 pt), couleurs inchangées (Q533 : en clair la teinte d'Ingénu assombrie à 3:1) ; mesuré sur le vrai premier lancement, clair et sombre : aucun pixel de dalle colorée sous leurs lignes, aucune icône, pas la zone nette (la dalle est à 369–519 pt ; en v148 la phrase descendait à ≈ 397). Capture : planche-v149/guide-deux-phrases.png.", "redteam_guide 87/88 (le rouge : Q534, les lobes du + au tirage), redteam_onb_mots, redteam_echelle_onboarding", 'v149'),
 'C-149': ('FAIT, EN ATTENTE DE TOM', "v149 (rouvert) : « garder de côté » à DROITE (bord droit à 24 pt, cote 708), jamais souligné, penché de 5,5° (skewX), visible pendant le tracé ; caché seulement quand un choix de la phrase est ouvert (Q540) ; actif / inactif comme en v148.", "redteam_garder 48/48 (39/48 sur v148)", 'v149'),
 'C-150': ('FAIT, EN ATTENTE DE TOM', "v149 : c'était le JUGE — un `closeAll` de script dans les 4 s d'un geste fait dans Peaufiner est refusé (C-134) : le juge appelle `_peaufSortie()` d'abord, et vérifie que la page + est bien fermée avant de la rouvrir.", "redteam_cercle_couleur 36/36", 'v149'),
 'C-151': ('FAIT, EN ATTENTE DE TOM', "v149 : un titre de deux lignes d'une carte d'Index rétrécit pas à pas (depuis la taille décidée, 24 pt) jusqu'à tenir dans sa boîte ET au-dessus de l'état — le plus petit pas qui tient (`_s4TitresAjuste`, relancé à chaque construction de la liste).", "redteam_titres_cartes 10/10 (6/10 sur v148)", 'v149'),
 'C-152': ('FAIT, EN ATTENTE DE TOM', "v149 : c'était le JUGE — `redteam_menu_plus` 4 touchait la pilule du Cercle avant qu'elle soit posée ; il attend deux lectures identiques de sa boîte. `redteam_flash` : 32/32 au calme en v148 ; sous charge (≥ 12) B2 rougit sur v148 comme sur v149.", "redteam_menu_plus 14/14", 'v149'),
 'C-153': ('FAIT, EN ATTENTE DE TOM', "v149 : le I du mot-marque de l'onboarding clignote du même code que l'accueil (`promiBlink 1.15s steps(1,end)`, même bleu dans chaque thème) sur les pages qui portent le mot-marque (prénom, parole, trait). « Promi planté ! » et le compte n'en portent pas (Q537).", "redteam_onb_mots 44/44", 'v149'),
 'C-154': ('FAIT, EN ATTENTE DE TOM', "v149 : la vague de création (le ruban de la page +) en `#291547`, la couleur de l'état « en cours » où entre toute parole plantée ; l'amande reste à la célébration (la fiche).", "redteam_ruban 36/36", 'v149'),
 'C-155': ('FAIT, EN ATTENTE DE TOM', "v149 : causes mesurées en WebKit — ① 440 ms de « signature » avant que la dalle grandisse : retirée, la dalle grandit dès l'image suivante, linéaire ; ② le lever et le clic recomposaient la page + qui s'en va (26–28 ms, puis 32 ms) : coupé pendant la plantation ; ③ le rideau naissait après l'instant et deux images longues (≈ 110 ms) : il démarre au lever. Lever de la page + 31 → 4 ms, première image 33 → 6 ms ; la Toile reçoit la parole après le départ.", "redteam_validation A, B, E (délais et vitesse jugés au calme seulement — charge 8 à 26 pendant le lot)", 'v149'),
 'C-156': ('FAIT, EN ATTENTE DE TOM', "v149 : ① le rideau part du bord bas du ruban (une seule matière), chaque colonne à vitesse constante, le haut du ruban sur le trait en ≈ 75–100 ms ; ② ma part seule : la vague amande sous le trait, aucun rideau, la parole reste en cours (Q541) ; ③ tout le monde a tracé : « Chacun a tracé sa part : « … » » dans le Fil (Q539) ; ④ `p.vuTenue` : la première ouverture rejoue le rideau, les suivantes non, rechargement compris (portage/SPEC-DONNEES §1.11). Aussi Q536 : plus rien de flou ni de transparent pendant le tracé (cinq nœuds, dont le titre).", "redteam_validation 25/25 (8/25 sur v148)", 'v149'),
}
n = 0
for i, l in enumerate(L):
    m = re.match(r'^\| (C-\d{3}) \|', l)
    if not m or m.group(1) not in MAJ: continue
    c = l.split(' | '); etat, preuve, juge, lot = MAJ[m.group(1)]
    # colonnes : 0 '| N°' · 1 date · 2 demande · 3 état · 4 preuve · 5 juge · 6 'lot |'
    if len(c) < 7: print('colonnes ?', m.group(1), len(c)); continue
    c[3] = etat
    if preuve: c[4] = preuve + ' ' + c[4]
    else: c[4] = 'v149 : validé par Tom. ' + c[4]
    if juge: c[5] = juge
    if lot: c[6] = lot + ' |'
    L[i] = ' | '.join(c); n += 1
io.open('CHANTIERS.md', 'w', encoding='utf-8').write('\n'.join(L)); print(n, 'lignes')
