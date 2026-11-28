# -*- coding: utf-8 -*-
"""L0 (vraie app, 20 nov. 2026) — LES CINQ PIÈCES REPRISES (la cinquième, le moteur de la Pelote : lot 6) DU PROTOTYPE, TELLES QUELLES (Tom : « seuls le moteur, le tracé, les flaques et les
jetons sont repris, chacun derrière une interface typée »). Cet outil COPIE, octet pour octet, depuis le prototype (la racine du dépôt) :
  promi-moteur.js                        → promi/src/moteur/repris/promi-moteur.js
  variantes/trace-lettres.js + chemins    → promi/src/animation/repris/
  variantes/flaques.js                    → promi/src/animation/repris/
et écrit promi/src/repris.json (empreintes sha256). Un test (tests/unitaires/repris.test.ts) vérifie que les copies sont identiques à leur source :
on ne corrige jamais une copie ; une correction du moteur se fait dans le prototype, avec l'accord de Tom, puis on relance l'outil.
python3 outils/reprendre.py [--verifie]"""
import hashlib, json, os, sys, shutil
PIECES = {
  'promi-moteur.js': 'promi/src/moteur/repris/promi-moteur.js',
  'variantes/trace-lettres.js': 'promi/src/animation/repris/trace-lettres.js',
  'variantes/trace-chemins-gilbert.js': 'promi/src/animation/repris/trace-chemins-gilbert.js',
  'variantes/trace-chemins-atkinson.js': 'promi/src/animation/repris/trace-chemins-atkinson.js',
  'variantes/trace-chemins-promilate.js': 'promi/src/animation/repris/trace-chemins-promilate.js',
  'variantes/flaques.js': 'promi/src/animation/repris/flaques.js',
}
man, diff = {}, []
for src, dst in PIECES.items():
    b = open(src, 'rb').read(); h = hashlib.sha256(b).hexdigest()
    man[dst.replace('promi/src/', '')] = {'source': src, 'sha256': h, 'octets': len(b)}
    if not os.path.exists(dst) or open(dst, 'rb').read() != b:
        diff.append(dst)
        if '--verifie' not in sys.argv: os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst)
# ⚑ 3b (25 nov. 2026) — LES TRACÉS DES DOUZE PINCEAUX (lot-PINCEAU-data du prototype : les matières de la planche PLANCHE-DOUZE-TRAITS, posées
# sur l'onde du §2.1, base 560, amplitude 36) : des DONNÉES, pas du code — relevées telles quelles du prototype dans un JSON engendré, jamais retouché.
import re
_S = open('app.html', encoding='utf-8').read()
_m = re.search(r'<script id="lot-PINCEAU-data">\s*window\._PINCEAU_TRACES=(.*?);\s*window\._PINCEAU_META=(.*?);\s*</script>', _S, re.S)
_pin = {'traces': json.loads(_m.group(1)), 'meta': json.loads(_m.group(2))}
_dst = 'promi/src/animation/repris/pinceaux-traces.json'
_txt = json.dumps(_pin, ensure_ascii=False, separators=(',', ':')) + '\n'
man['animation/repris/pinceaux-traces.json'] = {'source': 'app.html#lot-PINCEAU-data', 'sha256': hashlib.sha256(_txt.encode('utf-8')).hexdigest(), 'octets': len(_txt.encode('utf-8'))}
if not os.path.exists(_dst) or open(_dst, encoding='utf-8').read() != _txt:
    diff.append(_dst)
    if '--verifie' not in sys.argv: os.makedirs(os.path.dirname(_dst), exist_ok=True); open(_dst, 'w', encoding='utf-8').write(_txt)
# ⚑ lot 6 (Tom, 28 nov. 2026 : « Oui, le reprendre ») — LA CINQUIÈME PIÈCE : LE MOTEUR DE LA PELOTE (lot-AURA-PELOTE-MOTEUR : le velours, ses
# îles, son semis, son peintre WebGL 2 ; il ne vit que dans le prototype). Le texte du bloc, octet pour octet (entre la balise et `</script>`),
# chargé par sa façade (promi/src/moteur/pelote.ts) et par elle seule.
_m2 = re.search(r'<script id="lot-AURA-PELOTE-MOTEUR">\n(.*?)</script>', _S, re.S)
_pel = _m2.group(1).encode('utf-8')
_dst2 = 'promi/src/moteur/repris/pelote-moteur.js'
man['moteur/repris/pelote-moteur.js'] = {'source': 'app.html#lot-AURA-PELOTE-MOTEUR', 'sha256': hashlib.sha256(_pel).hexdigest(), 'octets': len(_pel)}
if not os.path.exists(_dst2) or open(_dst2, 'rb').read() != _pel:
    diff.append(_dst2)
    if '--verifie' not in sys.argv: open(_dst2, 'wb').write(_pel)
txt = json.dumps(man, ensure_ascii=False, indent=1) + '\n'
f = 'promi/src/repris.json'
if not os.path.exists(f) or open(f, encoding='utf-8').read() != txt:
    diff.append(f)
    if '--verifie' not in sys.argv: open(f, 'w', encoding='utf-8').write(txt)
for k, v in man.items(): print('%-42s %s %7d o' % (k, v['sha256'][:12], v['octets']))
if '--verifie' in sys.argv and diff: print('DIFFÈRE :', diff); sys.exit(1)
