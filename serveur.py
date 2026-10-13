#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
serveur.py — le serveur du prototype (v122, Tom, 3 oct. 2026).

« Remplace python3 -m http.server par un petit serveur qui envoie Cache-Control: no-store sur chaque fichier. »

Pourquoi : `http.server` n'envoie que `Last-Modified`. Safari met alors en cache « à l'heuristique » (≈ 10 % de l'âge du fichier) :
un `promi-moteur.js` vieux de 26 h restait en cache plus de deux heures pendant qu'`app.html` changeait — l'iPhone pouvait montrer un
mélange de versions. Ici, chaque réponse porte `Cache-Control: no-store` (et ni `Last-Modified` ni `ETag`) : rien n'est gardé.

`/version.json` rend le commit en cours (`git rev-parse --short HEAD`), et `"modifie": true` si l'arbre de travail a des changements
non commités — le relevé `?mesure=1` de l'Aura l'affiche, pour que Tom vérifie qu'il voit la dernière version.

Lancement (port 8752, en dur dans tous les outils ; écoute sur 0.0.0.0 pour l'iPhone) :
    python3 serveur.py
"""
import http.server, socketserver, subprocess, json, os, sys, re, hashlib

PORT = 8752
ICI = os.path.dirname(os.path.abspath(__file__))


def lot_et_moteur():
    """le lot écrit dans app.html (PROMI_VERSION.lot) et l'empreinte courte de promi-moteur.js, lus sur le disque"""
    lot, emp = '?', '?'
    try:
        # le bloc lot-V145-VERSION est posé juste avant lot-TOKENS-css (≈ 250 Ko dans le fichier) : on lit jusqu'à lui, pas les 4 000 premiers octets
        with open(os.path.join(ICI, 'app.html'), 'rb') as f: tete = f.read(600000).decode('utf-8', 'replace')
        m = re.search(r"PROMI_VERSION=\{lot:'([^']+)'", tete)
        if m: lot = m.group(1)
    except Exception: pass
    try:
        with open(os.path.join(ICI, 'promi-moteur.js'), 'rb') as f: emp = hashlib.sha1(f.read()).hexdigest()[:7]
    except Exception: pass
    return lot, emp


def version():
    try:
        h = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ICI, capture_output=True, text=True, timeout=5).stdout.strip()
        s = subprocess.run(['git', 'status', '--porcelain', '--', 'app.html', 'promi-moteur.js'], cwd=ICI, capture_output=True, text=True, timeout=5).stdout.strip()
        lot, emp = lot_et_moteur()
        return {'commit': h or '?', 'modifie': bool(s), 'lot': lot, 'moteur': emp}
    except Exception as e:
        return {'commit': '?', 'modifie': None, 'erreur': str(e)[:80]}


def ip_du_mac():
    # l'adresse du Mac sur le réseau local (elle CHANGE : .132 le 27 sept., .133 le 29) — lue à chaque lancement
    for cmd in (['ipconfig', 'getifaddr', 'en0'], ['ipconfig', 'getifaddr', 'en1']):
        try:
            ip = subprocess.run(cmd, capture_output=True, text=True, timeout=3).stdout.strip()
            if ip: return ip
        except Exception: pass
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('10.255.255.255', 1)); ip = s.getsockname()[0]; s.close(); return ip
    except Exception: return '(adresse introuvable : ipconfig getifaddr en0)'


class SansCache(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ICI, **k)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def send_header(self, cle, val):
        if cle.lower() in ('last-modified', 'etag'): return      # rien qui permette au navigateur de « revalider » un fichier gardé
        super().send_header(cle, val)

    def _envoie(self, corps, typ):
        self.send_response(200); self.send_header('Content-Type', typ); self.send_header('Content-Length', str(len(corps)))
        self.end_headers()
        if self.command != 'HEAD': self.wfile.write(corps)

    def _marque(self):
        """v145 (C-117) — la page et le moteur portent la version SERVIE : `app.html` reçoit le commit du moment (et « + » si l'arbre de
        travail est modifié) et l'empreinte du moteur, son `<script src>` prend cette empreinte en paramètre (aucun cache ne peut rendre un
        vieux moteur) ; `promi-moteur.js` déclare la sienne. La page compare : un mélange de versions se VOIT avec `?mesure=1`."""
        chemin = self.path.split('?')[0]
        if chemin == '/version.json':
            self._envoie(json.dumps(version()).encode('utf-8'), 'application/json'); return True
        if chemin in ('/app.html', '/'):
            try:
                with open(os.path.join(ICI, 'app.html'), 'rb') as f: corps = f.read()
            except Exception: return False
            v = version(); servi = (v.get('commit') or '?') + ('+' if v.get('modifie') else ''); emp = v.get('moteur') or '?'
            corps = corps.replace(b'__PROMI_SERVI__', servi.encode('utf-8'), 1).replace(b'__PROMI_MOTEUR__', emp.encode('utf-8'), 1)
            corps = corps.replace(b'<script src="promi-moteur.js"', b'<script src="promi-moteur.js?v=' + emp.encode('utf-8') + b'"', 1)
            self._envoie(corps, 'text/html; charset=utf-8'); return True
        if chemin == '/promi-moteur.js':
            try:
                with open(os.path.join(ICI, 'promi-moteur.js'), 'rb') as f: corps = f.read()
            except Exception: return False
            corps += b'\n;try{window.PROMI_MOTEUR_RECU="' + hashlib.sha1(corps).hexdigest()[:7].encode('utf-8') + b'";}catch(e){}\n'
            self._envoie(corps, 'text/javascript; charset=utf-8'); return True
        return False

    def do_GET(self):
        if self._marque(): return
        return super().do_GET()

    def do_POST(self):
        # v145 (C-112, R-B) — `/mesure` : ce que la page a mesuré SUR L'APPAREIL (avec `?mesure=1` : les images d'une plantation, d'un retrait,
        # d'un « tenir » ; ou une page de variantes) est gardé, une ligne par envoi, dans mesures/appareil.jsonl — avec l'adresse de l'appareil.
        if self.path.split('?')[0] != '/mesure':
            self.send_response(404); self.end_headers(); return
        try:
            n = min(int(self.headers.get('Content-Length') or 0), 200000); corps = self.rfile.read(n).decode('utf-8', 'replace')
            d = json.loads(corps); d['_de'] = self.client_address[0]
            os.makedirs(os.path.join(ICI, 'mesures'), exist_ok=True)
            with open(os.path.join(ICI, 'mesures', 'appareil.jsonl'), 'a', encoding='utf-8') as f: f.write(json.dumps(d, ensure_ascii=False) + '\n')
            self._envoie(b'{"ok":true}', 'application/json')
        except Exception as e:
            self.send_response(400); self.end_headers()

    def do_HEAD(self):
        if self._marque(): return
        return super().do_HEAD()

    def log_message(self, *a):
        pass


class Serveur(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    with Serveur(('0.0.0.0', PORT), SansCache) as s:
        print('Promi · commit %s · Cache-Control: no-store · écoute sur 0.0.0.0:%d' % (version()['commit'], PORT), flush=True)
        print('  sur ce Mac  : http://127.0.0.1:%d/app.html' % PORT, flush=True)
        print('  sur l\'iPhone (même Wi-Fi) : http://%s:%d/app.html' % (ip_du_mac(), PORT), flush=True)
        print('  Le serveur s\'arrête avec le Mac (extinction, fermeture de session) : relancer « python3 serveur.py ».', flush=True)
        try: s.serve_forever()
        except KeyboardInterrupt: pass
