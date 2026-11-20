# -*- coding: utf-8 -*-
"""L0 (20 nov. 2026) — L'ÉTAT DE TOM, RELU SUR SON iPHONE. L'app « Promi preuve » (fr.autier.promi.preuve, le prototype emballé) garde son
état dans le stockage de sa WebView ; cet outil le copie par `devicectl` (l'iPhone branché ou sur le même réseau, appairé à ce Mac), le décode
(WebKit : table ItemTable, valeurs en UTF-16) et l'écrit au format d'un export du prototype : etats/tom-<date>-preuve.json (hors dépôt).
python3 outils/etat_iphone.py [--app=fr.autier.promi.preuve] [--appareil=<identifiant devicectl>]"""
import json, os, sqlite3, subprocess, sys, tempfile, datetime
APP = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--app=')), 'fr.autier.promi.preuve')
APPAREIL = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--appareil=')), '9DC7D3E2-75F8-56AD-8015-2F4498E9B8BD')
def dc(*a):
    return subprocess.run(['xcrun', 'devicectl', 'device', *a, '--device', APPAREIL, '--domain-type', 'appDataContainer', '--domain-identifier', APP],
                          capture_output=True, text=True, check=True).stdout
liste = dc('info', 'files', '--subdirectory', 'Library/WebKit/WebsiteData/Default')
chemin = next(l.split()[0] for l in liste.splitlines() if l.split() and l.split()[0].endswith('LocalStorage/localstorage.sqlite3'))
d = tempfile.mkdtemp()
for suf in ('', '-shm', '-wal'):
    subprocess.run(['xcrun', 'devicectl', 'device', 'copy', 'from', '--device', APPAREIL, '--domain-type', 'appDataContainer', '--domain-identifier', APP,
                    '--source', 'Library/WebKit/WebsiteData/Default/' + chemin + suf, '--destination', os.path.join(d, 'ls.sqlite3' + suf)],
                   capture_output=True, check=suf != '')
ls = {k: (v.decode('utf-16-le') if isinstance(v, (bytes, bytearray)) else v) for k, v in sqlite3.connect(os.path.join(d, 'ls.sqlite3')).execute('select key, value from ItemTable')}
quand = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
f = 'etats/tom-%s-preuve.json' % quand
json.dump({'quand': quand, 'source': '%s, stockage de la WebView copié par devicectl' % APP, 'ls': ls}, open(f, 'w'), ensure_ascii=False)
st = json.loads(ls.get('promi_state', '{"promises":[]}'))
print(f, '·', len(st['promises']), 'parole(s) :', ', '.join(p.get('title', '?') for p in st['promises']))
