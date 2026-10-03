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
import http.server, socketserver, subprocess, json, os, sys

PORT = 8752
ICI = os.path.dirname(os.path.abspath(__file__))


def version():
    try:
        h = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ICI, capture_output=True, text=True, timeout=5).stdout.strip()
        s = subprocess.run(['git', 'status', '--porcelain', '--', 'app.html', 'promi-moteur.js'], cwd=ICI, capture_output=True, text=True, timeout=5).stdout.strip()
        return {'commit': h or '?', 'modifie': bool(s)}
    except Exception as e:
        return {'commit': '?', 'modifie': None, 'erreur': str(e)[:80]}


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

    def do_GET(self):
        if self.path.split('?')[0] == '/version.json':
            corps = json.dumps(version()).encode('utf-8')
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(corps)))
            self.end_headers(); self.wfile.write(corps); return
        return super().do_GET()

    def log_message(self, *a):
        pass


class Serveur(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    with Serveur(('0.0.0.0', PORT), SansCache) as s:
        print('Promi · http://127.0.0.1:%d/app.html · Cache-Control: no-store · commit %s' % (PORT, version()['commit']), flush=True)
        try: s.serve_forever()
        except KeyboardInterrupt: pass
