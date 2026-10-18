import sys; sys.argv=['x']
exec(open('redteam_pages_plus.py',encoding='utf-8').read().split('with sync_playwright() as p:')[0])
from PIL import ImageChops
with sync_playwright() as p:
    b = p.webkit.launch()
    for nature in (0, 1):
        ia, ta = fiche(b, REF, nature, False); ic, tc = fiche(b, REF, nature, False)
        d = ImageChops.difference(ia, ic).convert('L'); pts = [(i % d.width, i // d.width) for i, v in enumerate(d.getdata()) if v > 0]
        print('v149 contre v149', nature, len(pts), pts[:12])
        ic2, _ = fiche(b, F, nature, False)
        d = ImageChops.difference(ia, ic2).convert('L'); pts = [(i % d.width, i // d.width, v) for i, v in enumerate(d.getdata()) if v > 0]
        print('v149 contre v150', nature, len(pts), pts[:12])
    b.close()
