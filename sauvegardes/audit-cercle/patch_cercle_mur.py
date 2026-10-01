# LOT DU CERCLE — LE MUR, LES CHAMPS À TROIS LIGNES, LE CHEMIN (Tom, 11 sept. 2026, planche 3 validée avec ses révisions).
# Méthode CLAUDE.md §7 : chaque remplacement sous `assert S.count(old) == 1`. Les valeurs existantes se corrigent à LEUR
# source (un seul propriétaire, §7 « deux propriétaires ») ; tout ce qui est neuf va dans un bloc neuf en fin de fichier.
# Sauvegarde d'avant : sauvegardes/app-avant-cercle-mur.html (48b1a56b…).
import io, re, sys
F = 'app.html'
S = io.open(F, encoding='utf-8').read()
def remplace(old, new, quoi):
    global S
    n = S.count(old); assert n == 1, '%s : motif %s (%d occurrences)' % (quoi, 'absent' if n == 0 else 'multiple', n)
    S = S.replace(old, new); print('  ✓', quoi)

# ── 1 · LA BRIQUE cercle() — l'ordre de Tom, et l'encart qui ne porte que « ✦ Le Cercle » (Q201) ──
m = re.search(r'( {4}c\.appendChild\(reg\("C\'EST IMPORTANT \?", [^\n]*\)\);\n)( {4}c\.appendChild\(reg\(\'RÉCURRENCE\'[^\n]*\n)( {4}c\.appendChild\(reg\(\'RAPPEL\'[^\n]*\n)( {4}c\.appendChild\(reg\(\'LA MÉMOIRE\'[^\n]*\n)', S)
assert m and S.count(m.group(0)) == 1, 'cercle() : les quatre réglages introuvables'
ordre = ("    /* ⚑ L'ORDRE DE TOM (11 sept. 2026) : récurrence · rappels · importance · mémoire — la récurrence se comprend tout\n"
         "       de suite et on en voit l'usage ; la mémoire, la plus abstraite, ne vend rien en tête de liste. */\n")
S = S.replace(m.group(0), ordre + m.group(2) + m.group(3) + m.group(1) + m.group(4)); print('  ✓ cercle() : ordre')
remplace("    e.appendChild(t); e.appendChild(s);\n",
         "    /* ⚑ Q201 (Tom, 11 sept.) : l'encart nomme l'OFFRE, pas son contenu — « ✦ Le Cercle », seul. Il ne périme pas quand\n"
         "       le contenu bouge. Le sous-titre de contenu du §3.8 n'est plus posé. */\n"
         "    e.appendChild(t);\n", 'cercle() : encart « ✦ Le Cercle » seul')

# ── 2 · LES RÉGLAGES GÉNÉRAUX — le même ordre ──
m = re.search(r'\[\["C\'EST IMPORTANT \?", (\'[^\']*\')\], \[\'RÉCURRENCE\', \'chaque semaine\'\],\n(\s*)\[\'RAPPEL\', \'la veille à 19:00\'\], \[\'LA MÉMOIRE\', (\'[^\']*\')\]\]', S)
assert m and S.count(m.group(0)) == 1, 'cercleReglages() : tableau introuvable'
S = S.replace(m.group(0), "[['RÉCURRENCE', 'chaque semaine'], ['RAPPEL', 'la veille à 19:00'],\n%s[\"C'EST IMPORTANT ?\", %s], ['LA MÉMOIRE', %s]]" % (m.group(2), m.group(1), m.group(3)))
print('  ✓ cercleReglages() : ordre')

# ── 3 · LE PEAUFINER D'UNE NUÉE — P, le recentrage, et PIÈCES JOINTES aligné sur la fiche (à la source) ──
remplace("border:'2px solid '+encre, 'border-radius':(b.h/2)+'px',",
         "border:'2px solid '+encre,\n"
         "                /* ⚑ P (Tom, 11 sept. 2026, chantier 65) : un champ de TROIS LIGNES ET PLUS — libellé, texte, ligne de\n"
         "                   visibilité — prend le rayon 30 du grand panneau de la grammaire. Rayon = hauteur ÷ 2 y collait la 1re et la\n"
         "                   dernière ligne à la courbe (7,4 / 5,8 px ; la norme du champ à deux lignes est 12,9). */\n"
         "                'border-radius':(b.ph ? 30 : b.h/2)+'px',", 'Nuée : rayon 30 des champs à trois lignes')
remplace("'font-size':'18px', 'margin-top':'9px', 'line-height':'1.25',",
         "'font-size':'18px',\n"
         "                 /* ⚑ LE TEXTE DU MILIEU CENTRÉ ENTRE LE HAUT ET LE BAS DU CONTOUR (Tom, 11 sept.) : carte de 104, trait 2,\n"
         "                    dessin du texte 22 → son haut à 2 + (100 − 22) / 2 = 41 ; le libellé finit à 34 → 7 (était 9 : 41 / 37). */\n"
         "                 'margin-top':'7px', 'line-height':'1.25',", 'Nuée : texte du milieu centré')
remplace("      if(b.bas && !b.ph){ pose(B, {width:'100%'}); }\n",
         "      if(b.bas && !b.ph){ pose(B, {width:'100%'}); }\n"
         "      /* ⚑ CHANTIER 66 — PIÈCES JOINTES D'UNE NUÉE PREND LES PLACES DE CELLE D'UNE FICHE (un composant commun ne se\n"
         "         décline pas, CLAUDE §5) : libellé à 23, bas à 50,8 du haut de la carte, comme sur la fiche. Rangées collées en\n"
         "         haut, puis calées (mesuré). Avant : 14,8 / 60,3 — à 6,35 px de la courbe contre 12,9 sur la fiche. */\n"
         "      if(b.id === 'npFich'){ pose(el, {'align-content':'flex-start', 'padding-top':'17.5px'}); if(B) pose(B, {'margin-top':'9.3px'}); }\n",
         'Nuée : PIÈCES JOINTES aligné sur la fiche')

# ── 4 · LE BLOC NEUF ──
BLOC = open('sauvegardes/audit-cercle/bloc_cercle_mur.html', encoding='utf-8').read()
assert S.count('id="lot-CERCLE-MUR"') == 0, 'bloc déjà posé'
fin = S.rfind('</body>'); assert fin > 0
S = S[:fin] + BLOC + '\n' + S[fin:]
print('  ✓ bloc lot-CERCLE-MUR posé avant </body>')
io.open(F, 'w', encoding='utf-8').write(S)
print('écrit', F)
