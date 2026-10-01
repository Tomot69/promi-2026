# Le tableau des valeurs, recopié TEL QUEL depuis les journaux du juge — jamais retapé.
#   python3 table_valeurs.py JOURNAL_SOMBRE JOURNAL_CLAIR
# Prend, dans chaque journal, le DERNIER bloc « LES VALEURS MESURÉES » (jusqu'à la ligne « palier »)
# et le verdict qui suit. Refuse si un bloc manque ou si le verdict n'est pas vert.
import io, sys

def bloc(chemin):
    L = io.open(chemin, encoding='utf-8').read().splitlines()
    i = max(k for k, l in enumerate(L) if 'LES VALEURS MESURÉES' in l)
    out = [L[i]]
    for l in L[i + 1:]:
        out.append(l)
        if l.startswith('palier'): break
    verdict = next(l for l in L[i:] if '✅' in l or '❌' in l)
    assert '✅' in verdict, '%s : %s' % (chemin, verdict)
    return out + [verdict]

for nom, ch in zip(('SOMBRE', 'CLAIR'), sys.argv[1:3]):
    print('```')
    for l in bloc(ch): print(l)
    print('```')
