# -*- coding: utf-8 -*-
"""L0 (vraie app, 20 nov. 2026) — LES QUATRE PIÈCES REPRISES DU PROTOTYPE, TELLES QUELLES (Tom : « seuls le moteur, le tracé, les flaques et les
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
txt = json.dumps(man, ensure_ascii=False, indent=1) + '\n'
f = 'promi/src/repris.json'
if not os.path.exists(f) or open(f, encoding='utf-8').read() != txt:
    diff.append(f)
    if '--verifie' not in sys.argv: open(f, 'w', encoding='utf-8').write(txt)
for k, v in man.items(): print('%-42s %s %7d o' % (k, v['sha256'][:12], v['octets']))
if '--verifie' in sys.argv and diff: print('DIFFÈRE :', diff); sys.exit(1)
