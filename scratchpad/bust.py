#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ANTI-CACHE — on horodate chaque <script src> d'une planche.

⚠ `python3 -m http.server` n'envoie AUCUN Cache-Control. Le navigateur applique
alors sa fraicheur heuristique et NE REDEMANDE MEME PAS le fichier : on edite un
module, le serveur est a jour (verifie en curl), et l'ecran montre l'ancien.
C'est arrive deux fois sur ce projet — la premiere fois le 5 septembre, ou j'ai
cherche le bug dans le code pendant que c'etait le cache.

La parade : l'URL change quand le fichier change. On colle ?v=<mtime> a chaque
src local. A relancer apres toute edition de module.
"""
import io, os, re, sys, time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIBLES = sys.argv[1:] or ['PLANCHE-PAVAGE.html']

for nom in CIBLES:
    p = os.path.join(RACINE, nom)
    S = io.open(p, encoding='utf-8').read()
    n = 0
    def stamp(m):
        global n
        chemin = m.group(1).split('?')[0]
        f = os.path.join(RACINE, chemin.lstrip('/'))
        if not os.path.exists(f):
            return m.group(0)
        n += 1
        return '<script src="%s?v=%d"></script>' % (chemin, int(os.path.getmtime(f)))
    S = re.sub(r'<script src="(/[^"]+)"></script>', stamp, S)
    # et le document lui-meme ne doit pas etre garde
    if 'http-equiv="Cache-Control"' not in S:
        S = S.replace('<meta charset="utf-8">',
                      '<meta charset="utf-8">\n<meta http-equiv="Cache-Control" content="no-store">', 1)
    io.open(p, 'w', encoding='utf-8').write(S)
    print('%-28s %d scripts horodates' % (nom, n))
