import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('scratchpad/v160/tom_versions.py').read().split('with sync_playwright')[0].split('FICHIERS')[0])
LIT = open('scratchpad/v160/tom_versions.py').read().split('LIT = """')[1].split('"""')[0]
with sync_playwright() as p:
    b = p.webkit.launch()
    for F in sys.argv[2:]:
        ctx = B.contexte(b, vw=390, vh=651, sombre=True, stockage={'promi_studio': json.dumps({'m': __import__('os').environ.get('MONDE','encre'), 'p': 'signal', 'h': 0, 'libre': True, 'acquis': {}})}); B.toile_pleine(ctx, int(sys.argv[1]))
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F, timeout=120000); pg.wait_for_timeout(11000)
        for k in range(6):
            if k: pg.reload(timeout=120000); pg.wait_for_timeout(11000)
            r = pg.evaluate(LIT); print('%-14s n=%s ouverture %d · vue s %s ox %s oy %s · écart mini %s · %s' % (F, sys.argv[1], k+1, r['s'], r['ox'], r['oy'], r['dmin'], [p[:2] for p in r['pos']]), flush=True)
        ctx.close()
    b.close()
