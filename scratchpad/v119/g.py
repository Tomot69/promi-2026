#!/usr/bin/env python3
# g.py MOTIF [fichier] [avant] [apres] [max] — contextes d'un motif (regex), avec numéro de ligne
import re, io, sys
pat = sys.argv[1]; f = sys.argv[2] if len(sys.argv) > 2 else 'app.html'
a = int(sys.argv[3]) if len(sys.argv) > 3 else 120; b = int(sys.argv[4]) if len(sys.argv) > 4 else 160
mx = int(sys.argv[5]) if len(sys.argv) > 5 else 12
S = io.open(f, encoding='utf-8').read(); n = 0
for m in re.finditer(pat, S):
    n += 1
    if n > mx: continue
    l = S.count('\n', 0, m.start()) + 1
    print('── l.%d  ' % l + S[max(0, m.start()-a):m.end()+b].replace('\n', '⏎'))
print('== %d occurrence(s)' % n)
