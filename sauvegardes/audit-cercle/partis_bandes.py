# Découpe des quatre bandes de trait, aux cotes RELEVÉES SUR LES IMAGES (pas devinées) :
#   gratuit (canevas 362 css = 724 px) : la dalle finit ~470, les points culminent ~495, la flèche descend ~630, le mot ~660
#   cercle  (canevas 472 css = 944 px) : la dalle finit ~690, le trait ~715 → ~835, les anneaux ~880
# On garde toute la largeur (390 css) : le trait va d'un bord à l'autre, c'est son sujet.
import os
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partis')
COUPE = {'gratuit': (480, 648), 'cercle': (700, 856)}
for th in ('dark', 'light'):
    for cle, (y0, y1) in COUPE.items():
        s = os.path.join(D, '%s_trame_%s.png' % (th, cle)); im = Image.open(s)
        b = im.crop((0, y0, im.width, y1)); d = os.path.join(D, '%s_bande_%s.png' % (th, cle)); b.save(d)
        print('%-6s %-8s %s %dx%d → %dx%d' % (th, cle, os.path.basename(d), im.width, im.height, b.width, b.height))
