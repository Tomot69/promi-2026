# -*- coding: utf-8 -*-
"""L0 (vraie app, 20 nov. 2026) — LES CINQ FACES DE LA VRAIE APP SONT CELLES DU PROTOTYPE, OCTET POUR OCTET.
Le prototype (app.html, le cahier des charges figé) embarque ses cinq faces en base64 dans ses @font-face. Cet outil les en sort TELLES QUELLES
(woff2) et écrit promi/src/design/polices.css avec LES MÊMES descripteurs (size-adjust, ascent/descent/line-gap-override, font-display) :
le même texte rend les mêmes pixels. Fichiers GÉNÉRÉS : on relance l'outil, on ne les retouche jamais.
python3 outils/polices_extraire.py [--verifie]"""
import re, io, sys, base64, hashlib, os
S = io.open('app.html', encoding='utf-8').read()
RE = re.compile(r"@font-face\{font-family:([A-Za-z]+);font-weight:(\d+);([^}]*?)src:url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)([^}]*)\}")
faces = RE.findall(S)
assert len(faces) == 5, 'le prototype doit porter exactement cinq faces (CLAUDE.md §6) : %d' % len(faces)
DOS = 'promi/src/design/polices'
sorties = {}
css = ['/* polices.css — GÉNÉRÉ par outils/polices_extraire.py depuis app.html (les cinq faces du prototype, octet pour octet). Ne pas retoucher. */']
for fam, poids, avant, b64, apres in faces:
    nom = '%s-%s.woff2' % (fam, poids)
    sorties[os.path.join(DOS, nom)] = base64.b64decode(b64)
    css.append("@font-face{font-family:%s;font-weight:%s;%ssrc:url('./polices/%s')%s}" % (fam, poids, avant, nom, apres))
sorties['promi/src/design/polices.css'] = ('\n'.join(css) + '\n').encode('utf-8')
diff = []
for f, b in sorties.items():
    av = open(f, 'rb').read() if os.path.exists(f) else None
    if av != b:
        diff.append(f)
        if '--verifie' not in sys.argv:
            os.makedirs(os.path.dirname(f), exist_ok=True); open(f, 'wb').write(b)
for f, b in sorties.items(): print('%-50s %7d o  %s' % (f, len(b), hashlib.sha256(b).hexdigest()[:12]))
if '--verifie' in sys.argv and diff: print('DIFFÈRE :', diff); sys.exit(1)
