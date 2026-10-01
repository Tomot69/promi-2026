# Insère le chapitre du lot en TÊTE d'ETAT-DES-LIEUX.md (juste sous le titre), motif assert == 1.
# Refuse si un marqueur ⟦…⟧ reste dans le brouillon : on n'écrit pas un chapitre à trous.
import io, os, re, sys, shutil
ICI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(ICI, '..', '..'))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, 'etat_brouillon.md')
ETAT = os.path.join(APP, 'ETAT-DES-LIEUX.md')
ch = io.open(SRC, encoding='utf-8').read().strip() + '\n\n---\n\n'
trous = re.findall(r'⟦[^⟧]*⟧', ch)
assert not trous, 'marqueurs non remplis : %s' % trous
S = io.open(ETAT, encoding='utf-8').read()
tete = '# ÉTAT DES LIEUX\n\n'
assert S.count(tete) == 1, 'titre absent ou multiple'
# la sauvegarde : nommée par le 2e argument (défaut : celle du lot), et JAMAIS écrasée
SAUV = os.path.join(APP, 'sauvegardes', sys.argv[2] if len(sys.argv) > 2 else 'ETAT-DES-LIEUX-avant-aura-orbite.md')
assert not os.path.exists(SAUV), 'la sauvegarde existe déjà, on ne l\'écrase pas : %s' % SAUV
shutil.copy(ETAT, SAUV)
S = S.replace(tete, tete + ch, 1)
io.open(ETAT, 'w', encoding='utf-8').write(S)
print('chapitre inséré en tête ; sauvegarde :', os.path.relpath(SAUV, APP))
