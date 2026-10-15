# v146 — le guide DANS L'APP : rejoué (?guide=1), états arrêtés, capture ; compare l'accueil flouté d'avance à l'accueil réel
import sys, io, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
import numpy as np
th = sys.argv[1] if len(sys.argv) > 1 else 'clair'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre=(th == 'sombre')); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx)
    net = Image.open(io.BytesIO(B.capture(pg))).convert('RGB')
    # l'image repeinte (avant flou), comparée à l'accueil réel
    u = pg.evaluate("()=>window._guide.image().then(c=>c.toDataURL('image/png'))")
    import base64; rec = Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGB')
    a = np.asarray(net.resize((390, 844), Image.LANCZOS)).astype(int); r = np.asarray(rec).astype(int); d = np.abs(a - r).sum(axis=2)
    print('accueil repeint contre accueil réel : écart moyen %.1f niveaux (somme des trois canaux) · %.1f %% de pixels à plus de 60' % (d.mean(), (d > 60).mean() * 100))
    for (nom, y0, y1) in (('plateau', 36, 104), ('toile', 110, 700), ('barre', 706, 814)): print('   %s : écart moyen %.1f' % (nom, d[y0:y1].mean()))
    cote = Image.new('RGB', (390 * 2 + 20, 844), (60, 60, 60)); cote.paste(net.resize((390, 844)), (0, 0)); cote.paste(rec, (410, 0)); cote.save('scratchpad/v146/guide-repeint-%s.png' % th)
    pg.evaluate("()=>window._guide.montre('studio', true)"); pg.wait_for_timeout(1600)
    print('état', json.dumps(pg.evaluate("()=>window._guide.etat()"))[:400]); ims = []
    for ms in (120, 320, 620, 950, 1250): pg.evaluate("m=>window._guide.figeA(m)", ms); pg.wait_for_timeout(200); ims.append(Image.open(io.BytesIO(B.capture(pg))).convert('RGB'))
    for q, ms in (('studio', 250), ('studio', 480), ('studio', 700), ('plus', 300), ('plus', 700)): pg.evaluate("a=>window._guide.figeNet(a[0], a[1])", [q, ms]); pg.wait_for_timeout(250); ims.append(Image.open(io.BytesIO(B.capture(pg))).convert('RGB'))
    W = Image.new('RGB', (5 * (ims[0].width + 30), 2 * (ims[0].height + 30)), (40, 40, 40))
    for i, im in enumerate(ims): W.paste(im, ((i % 5) * (im.width + 30), (i // 5) * (im.height + 30)))
    W.save('planche-v146/PLANCHE-4-guide-app-%s.png' % th); W.resize((W.width // 4, W.height // 4)).save('scratchpad/v146/pl4app-%s.png' % th)
    print('erreurs', pg.__dict__['erreurs'][:3]); b.close()
