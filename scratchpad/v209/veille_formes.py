"""v209 (C-300) — la veille rebondit sur la forme réelle de l'écran : trois formes (encoche 16e, Dynamic Island 16 Pro, sans découpe SE), 2 h simulées × 5 graines
par la fonction de l'app (`_veilleSimule`, la même que l'écran). A : jamais dans la découpe (chaque segment entre deux rebonds) ; B : jamais hors de l'écran ;
C : les quatre coins atteints là où la géométrie le permet ; D : les deux côtés de la découpe touchés. --sonde : la découpe ignorée par la trajectoire (A doit rougir)."""
import sys, json
from playwright.sync_api import sync_playwright
SONDE = '--sonde' in sys.argv
W_LOGO = 140.0
FORMES = [('16e encoche', 390, 844, {'x': 114, 'y': 0, 'w': 162, 'h': 33}),
          ('16 Pro île', 402, 874, {'x': 138, 'y': 14, 'w': 126, 'h': 37}),
          ('SE sans découpe', 375, 667, None)]
ok = 0; tot = 0
def juge(c, m, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print(('  ✅ ' if c else '  ❌ ') + m + ('   ' + d if d else ''))
def coupe(p0, p1, E):
    # le segment p0→p1 entre-t-il dans l'intérieur ouvert de E ? (découpage de Liang-Barsky, avec une marge de 0,01 px)
    x0, y0 = p0; dx, dy = p1[0] - x0, p1[1] - y0; t0, t1 = 0.0, 1.0; m = 0.01
    for p, q in ((-dx, x0 - (E['x0'] + m)), (dx, (E['x1'] - m) - x0), (-dy, y0 - (E['y0'] + m)), (dy, (E['y1'] - m) - y0)):
        if p == 0:
            if q < 0: return False
        else:
            r = q / p
            if p < 0: t0 = max(t0, r)
            else: t1 = min(t1, r)
    return t0 < t1
with sync_playwright() as pw:
    b = pw.webkit.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932})
    pg.goto('http://127.0.0.1:8752/app.html?veille=600', wait_until='load'); pg.wait_for_timeout(4000)
    for nom, L, H, O in FORMES:
        print('— ' + nom)
        h = W_LOGO * 26.72 / 140
        res = []
        for g in (1, 2, 3, 4, 5):
            o = {'l': L, 'h': H, 'k': 1, 'ins': [0, 0, 0, 0], 'w': W_LOGO, 'h0': h, 'trace': True}
            if O and not SONDE: o['decoupe'] = O
            res.append(pg.evaluate('o=>window._veilleSimule(7200, %d, o)' % g, o))
        B = res[0]['bornes']
        E = None if not O else {'x0': O['x'] - W_LOGO, 'x1': O['x'] + O['w'], 'y0': O['y'] - h, 'y1': O['y'] + O['h']}
        dedans = 0; hors = 0; pts = []
        for r in res:
            tr = [[(B['x0'] + B['x1']) / 2, (B['y0'] + B['y1']) / 2, 'depart']] + r['trace']
            for a, c in zip(tr, tr[1:]):
                if E and coupe(a[:2], c[:2], E): dedans += 1
            for p in r['trace']:
                pts.append(p)
                if p[0] < -0.01 or p[1] < -0.01 or p[0] > L - W_LOGO + 0.01 or p[1] > H - h + 0.01: hors += 1
        juge(dedans == 0, 'A · jamais dans la découpe', '%d segments la traversent sur %d rebonds' % (dedans, sum(r['rebonds'] for r in res)))
        juge(hors == 0, "B · jamais hors de l'écran", '%d' % hors)
        coins = {'haut-gauche': (0, 0), 'haut-droit': (L - W_LOGO, 0), 'bas-gauche': (0, H - h), 'bas-droit': (L - W_LOGO, H - h)}
        for cn, (cx, cy) in coins.items():
            atteignable = not (E and (cx > E['x0'] and cx < E['x1'] and cy > E['y0'] and cy < E['y1']))
            dmin = min(max(abs(p[0] - cx), abs(p[1] - cy)) for p in pts)
            if atteignable: juge(dmin <= 2.0, 'C · coin %s atteint' % cn, 'au plus près %.1f pt' % dmin)
            else:
                # le coin est DANS la découpe agrandie du logo : la boîte de 140 pt ne tient pas à côté de la découpe
                ymin = min(p[1] for p in pts if (p[0] < 1 if 'gauche' in cn else p[0] > L - W_LOGO - 1)) if any((p[0] < 1 if 'gauche' in cn else p[0] > L - W_LOGO - 1) for p in pts) else None
                print('  ·  coin %s : HORS D\'ATTEINTE — le logo (%.0f pt) ne tient pas entre le bord et la découpe (%.0f pt) ; au plus haut contre ce bord : %s pt' % (cn, W_LOGO, O['x'], ('%.1f' % ymin) if ymin is not None else '—'))
        if E:
            cote = [p for p in pts if p[2] in ('oy', 'oc')]
            gauche = [p for p in cote if p[0] + W_LOGO / 2 < O['x'] + O['w'] / 2]; droite = [p for p in cote if p[0] + W_LOGO / 2 > O['x'] + O['w'] / 2]
            juge(len(gauche) > 0 and len(droite) > 0, 'D · rebonds sur la découpe, des deux côtés de son milieu', 'gauche %d, droite %d ; le haut du logo y est à %.1f pt (zone sûre : 47 / 62)' % (len(gauche), len(droite), O['y'] + O['h']))
    b.close()
print('\n  %s  %d / %d' % ('✅' if ok == tot else '❌', ok, tot))
