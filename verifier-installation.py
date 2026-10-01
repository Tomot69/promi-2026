#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VERIFIER L'INSTALLATION — a lancer en tout premier.

       python3 verifier-installation.py

   Il controle que tout est en place et le dit en francais.
   Aucune connaissance technique requise pour lire le resultat.
"""
import os, sys, subprocess

VERT   = '\033[92m'
ROUGE  = '\033[91m'
JAUNE  = '\033[93m'
GRAS   = '\033[1m'
FIN    = '\033[0m'

def ok(m):    print('  %s✓%s  %s' % (VERT, FIN, m))
def ko(m):    print('  %s✗%s  %s' % (ROUGE, FIN, m))
def note(m):  print('  %s·%s  %s' % (JAUNE, FIN, m))

problemes = []

print('\n%sVÉRIFICATION DE L\'INSTALLATION%s\n' % (GRAS, FIN))

# ── 1 · les fichiers ──────────────────────────────────────────
print('%s1 · Les fichiers%s' % (GRAS, FIN))

DOCS = ['CLAUDE.md','PROMI-PRESENTATION.md','ETAT-DES-LIEUX.md','DECISIONS.md',
        'PARCOURS.md','DESIGN-MESURE.md','VERIFIER.md','FICHIERS.md']
TESTS = ['redteam_ecrans.py','redteam.py','redteam2.py','redteam3.py',
         'redteam_demande.py','redteam_toile.py','redteam_geste.py']

for f in DOCS:
    if os.path.exists(f): ok(f)
    else: ko('%s — MANQUANT' % f); problemes.append('document %s' % f)

if os.path.exists('app.html'):
    taille = os.path.getsize('app.html') // 1024
    ok('app.html  (%d Ko)' % taille)
    if taille < 800:
        ko('  ⚠ le fichier semble trop petit — est-ce le bon ?')
        problemes.append('app.html suspect')
else:
    ko('app.html — MANQUANT')
    if os.path.exists('promi-v592.html'):
        note('  → promi-v592.html est là. Renommez-le en app.html :')
        note('     mv promi-v592.html app.html')
    problemes.append('app.html manquant')

manquants = [f for f in TESTS if not os.path.exists(f)]
if not manquants: ok('les 7 batteries de tests')
else:
    ko('batteries manquantes : %s' % ', '.join(manquants))
    problemes.append('batteries')

if os.path.exists('releve-design.py'): ok('releve-design.py')
else: ko('releve-design.py — MANQUANT'); problemes.append('releve-design')

if os.path.exists('design-reference.json'): ok('design-reference.json')
else: note('design-reference.json absent — il sera créé au premier relevé')

# ── 2 · les outils ────────────────────────────────────────────
print('\n%s2 · Les outils%s' % (GRAS, FIN))

v = sys.version_info
if v >= (3, 8): ok('Python %d.%d' % (v.major, v.minor))
else: ko('Python %d.%d — il en faut au moins 3.8' % (v.major, v.minor)); problemes.append('python')

try:
    import playwright
    ok('Playwright installé')
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); b.close()
        ok('Chromium fonctionne')
    except Exception as e:
        ko('Chromium ne démarre pas')
        note('  → lancez :  python3 -m playwright install chromium')
        problemes.append('chromium')
except ImportError:
    ko('Playwright absent')
    note('  → lancez :  python3 -m pip install playwright')
    note('     puis  :  python3 -m playwright install chromium')
    problemes.append('playwright')

try:
    r = subprocess.run(['node','--version'], capture_output=True, text=True, timeout=10)
    if r.returncode == 0: ok('Node %s' % r.stdout.strip())
    else: raise Exception()
except Exception:
    ko('Node absent')
    note('  → téléchargez-le sur nodejs.org, ou :  brew install node')
    problemes.append('node')

# ── 3 · le verdict ────────────────────────────────────────────
print('\n%s3 · Verdict%s' % (GRAS, FIN))

if not problemes:
    print('\n  %s%sTOUT EST EN PLACE.%s\n' % (GRAS, VERT, FIN))
    print('  Vous pouvez lancer le lot zéro. Collez dans Claude Code')
    print('  le contenu du fichier  LOT-ZERO.md\n')
else:
    print('\n  %s%s%d PROBLÈME(S) À RÉGLER%s\n' % (GRAS, ROUGE, len(problemes), FIN))
    for p in problemes: print('    · %s' % p)
    print('\n  Suivez les indications ci-dessus, puis relancez :')
    print('    python3 verifier-installation.py\n')
    sys.exit(1)
