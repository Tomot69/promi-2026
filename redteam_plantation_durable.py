#!/usr/bin/env python3
"""redteam_plantation_durable.py — v177 (Tom, 1er nov. 2026, C-226) : UNE PAROLE PLANTÉE NE SE PERD JAMAIS.

« Une perte de données n'est jamais acceptable. » Planter (clavier ouvert, puis fermé ; Promi, Chiche, Cercle), recharger 0, 100 et 500 ms après le trait : la parole est là, en mémoire et
dans le stockage ; elle est écrite AU MOMENT du trait, avant toute suite (lue dans la même tâche). Plus le cas qui a perdu « N » : un second onglet de l'app resté ouvert. 20 essais par cas.
Le banc est `banc-durable.html` (l'app dans un cadre, le vrai `fin()` du trait, à la souris : c'est le même chemin) ; il tourne à l'identique en WebKit (ici) et dans Safari iOS :
  xcrun simctl openurl <udid> "http://127.0.0.1:8752/banc-durable.html?n=20"     puis     python3 redteam_plantation_durable.py --lire
`--lire` juge ce que Safari iOS a envoyé au Mac (mesures/appareil.jsonl). `--fichier=zz-v176.html` : rouge (écrite trop tard, le second onglet efface). `--n=` : essais par cas.
"""
import sys, json, time
from playwright.sync_api import sync_playwright
ARG = dict(a[2:].split('=', 1) for a in sys.argv[1:] if '=' in a)
N = int(ARG.get('n', 20)); F = ARG.get('fichier', 'app.html')
def juge(R):
    ok = True
    for r in R:
        b = r['err'] == 0 and r['la'] == r['essais'] and r['ecrite'] == r['essais'] and r['essais'] > 0 and r['geste'] == r['essais']
        ok = ok and b; print('  %s %-58s %d/%d là · %d/%d écrites au trait · %d erreurs · %s min' % ('✅' if b else '❌', r['cas'], r['la'], r['essais'], r['ecrite'], r['essais'], r['err'], r.get('min')), flush=True)
    print('\n  %s %d / %d' % ('✅' if ok and R else '❌', sum(r['la'] for r in R), sum(r['essais'] for r in R))); sys.exit(0 if ok and R else 1)
if 'lire' in ' '.join(sys.argv):
    L = [json.loads(l) for l in open('mesures/appareil.jsonl', encoding='utf-8') if '"durable' in l]
    i = max((k for k, x in enumerate(L) if x.get('quoi') == 'durable-fin'), default=len(L)); j = max((k for k, x in enumerate(L[:i]) if x.get('quoi') == 'durable-fin'), default=-1)
    R = [x for x in L[j + 1:i + 1] if x.get('quoi') == 'durable']; print('redteam_plantation_durable — relevé envoyé par', (R or [{}])[0].get('ua')); juge(R)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); print('redteam_plantation_durable — %s, WebKit, %d essais par cas' % (F, N), flush=True)
    pg.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg.goto('http://127.0.0.1:8752/banc-durable.html?n=%d&app=%s%s' % (N, F, ('&cas=' + ARG['cas']) if 'cas' in ARG else ''))
    t0 = time.time()
    while not pg.evaluate("()=>window.__fini===true") and time.time() - t0 < 14000: pg.wait_for_timeout(5000)
    R = pg.evaluate("()=>window.__res"); b.close()
juge(R)
