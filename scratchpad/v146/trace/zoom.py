# zoom.py — quelques glyphes en grand, pour relire un chemin de près :  python3 zoom.py gilbert "eft" [nom-de-sortie]
import sys, planche, chemins as C
from fontTools.ttLib import TTFont
from PIL import Image
cle = sys.argv[1]; chars = sys.argv[2]; P = C.POLICES[cle]; f = TTFont(P['fichier']); cm = f.getBestCmap(); upm = f['head'].unitsPerEm
mi = int(round((getattr(f['OS/2'], 'sxHeight', 0) or upm * 0.5) / 2))
planche.CW, planche.CH, planche.ECH = 500, 600, 0.6
cells = []
for ch in chars:
    g = C.analyse(f, ch, cm[ord(ch)], mi, upm, C.CORRECTIONS[cle].get(ch, {})); g['av'] = 0
    for V in 'hb': cells.append(planche.cellule(ch, g, V, mi, upm))
cols = 4; out = Image.new('RGB', (cols * 500, ((len(cells) + cols - 1) // cols) * 600), 'white')
for i, c in enumerate(cells): out.paste(c, ((i % cols) * 500, (i // cols) * 600))
nom = sys.argv[3] if len(sys.argv) > 3 else 'zoom.png'; out.save(nom); print(nom, out.size)
