#!/usr/bin/env python3
# verif.py [fichier] — syntaxe de CHAQUE <script> (node --check) puis chargement de la page dans deux moteurs : pageerror
import re, io, subprocess, os, sys
from playwright.sync_api import sync_playwright
f = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
ICI = os.path.dirname(os.path.abspath(__file__)); S = io.open(f, encoding='utf-8').read(); bad = 0
for i, m in enumerate(re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', S, re.S)):
    t = os.path.join(ICI, '_c.js'); io.open(t, 'w', encoding='utf-8').write(m.group(1))
    r = subprocess.run(['node', '--check', t], capture_output=True, text=True)
    if r.returncode: bad += 1; print('script', i, 'l.%d' % (S.count('\n', 0, m.start()) + 1), r.stderr[:400])
r = subprocess.run(['node', '--check', 'promi-moteur.js'], capture_output=True, text=True)
if r.returncode: bad += 1; print('moteur', r.stderr[:400])
print('syntaxe : %d script(s) fautif(s)' % bad)
with sync_playwright() as p:
    for nom in ('webkit', 'chromium'):
        b = getattr(p, nom).launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}); er = []
        pg.on('pageerror', lambda e: er.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/' + f); pg.wait_for_timeout(6000)
        pg.evaluate('()=>{var o=document.getElementById("promiOnb");if(o){o.classList.add("gone");o.style.display="none";}}')
        for js in ["()=>{const p=promises.filter(q=>!q.draft&&!q.req&&!q.nuee)[0]; openDetail(p.id);}", "()=>{closeAll(); document.getElementById('createBtn').click();}", "()=>{closeAll(); document.getElementById('souffleBtn').click();}", "()=>{closeAll(); document.getElementById('openStudio2').click();}", "()=>{closeAll(); document.getElementById('settingsBtn').click();}", "()=>{closeAll(); openEssaim('potager');}"]:
            try: pg.evaluate(js)
            except Exception as e: er.append('évaluation : ' + str(e)[:160])
            pg.wait_for_timeout(1200)
        print('%-8s pageerror : %s' % (nom, er if er else 'aucune')); b.close()
sys.exit(1 if bad else 0)
