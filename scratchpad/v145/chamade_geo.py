import sys, json, re, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
src = io.open('banc_rendu.py', encoding='utf-8').read()
GRAINE = int(re.search(r'^GRAINE\s*=\s*(\d+)', src, re.M).group(1)); T_FIGE = float(re.search(r'^T_FIGE\s*=\s*([\d.]+)', src, re.M).group(1))
AMORCE = re.search(r'AMORCE = """(.*?)""" % GRAINE', src, re.S).group(1) % GRAINE
PILOTE = re.search(r'PILOTE = """(.*?)""" % T_FIGE', src, re.S).group(1) % T_FIGE
POSE = re.search(r'POSE = """(.*?)"""', src, re.S).group(1)
if '--oublie' in sys.argv: POSE = POSE.replace('window.__amorce(graine); Toile.setTheme(monde);', 'window.__amorce(graine); try{ window._chaOublie&&window._chaOublie(); }catch(e){} Toile.setTheme(monde);'); assert '_chaOublie' in POSE
RENDU = re.search(r'RENDU = """(.*?)"""', src, re.S).group(1)
KS = [0.5, 1, 2]; PAROLES = [['promi', 'nager le mardi'], ['chiche', 'courir dimanche'], ['tenu', 'planter un arbre'], ['cercle', 'arroser les tomates']]
N = 4
out = []
with sync_playwright() as p:
    for passe in range(N):
        b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2); ctx.add_init_script(AMORCE)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} }")
        pg.evaluate(PILOTE)
        rel = []
        for essai in range(2):
            pg.evaluate(POSE, ['chamade', GRAINE, ['chamade', 'esquille']])
            for _ in range(6): pg.evaluate("()=>window.__images(40)"); pg.wait_for_timeout(120)
            vive = pg.evaluate("()=>JSON.stringify(window._chaComp||null)")
            r = pg.evaluate(RENDU, ['chamade', T_FIGE, KS, PAROLES])
            apres = pg.evaluate("()=>JSON.stringify(window._chaComp||null)")
            rel.append({'vive': vive, 'apres': apres, 'fnv': {k: (v or {}).get('fnv') for k, v in r.items()}})
        out.append(rel); print(passe, [(len(json.loads(x['vive'])['centres']) if x['vive'] != 'null' else None, x['fnv'].get('toile-clair'), x['fnv'].get('toile-sombre')) for x in rel], flush=True)
        b.close()
json.dump(out, io.open('scratchpad/v145/chamade_geo.json', 'w', encoding='utf-8'))
ref = out[0][1]
for i in range(N):
    for e in range(2):
        x = out[i][e]; a = json.loads(ref['vive'])['centres']; c = json.loads(x['vive'])['centres']
        da = {t[0]: t for t in a}; d = [(t, da.get(t[0])) for t in c if da.get(t[0]) != t]
        fd = [k for k in x['fnv'] if x['fnv'][k] != ref['fnv'].get(k)]
        print('passe', i, 'essai', e, ': géométrie vive ≠ réf sur', len(d), 'cœurs', d[:3], '· images ≠', len(fd), fd[:4], '· vive==apres', x['vive'] == x['apres'])
