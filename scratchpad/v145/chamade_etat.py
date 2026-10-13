import sys, json, re, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
src = io.open('banc_rendu.py', encoding='utf-8').read()
ns = {}; exec(src.split("def passe(")[0].split("import sys, os")[0], ns) if False else None
import importlib.util
# on réutilise AMORCE, PILOTE, POSE du banc sans le lancer
m = re.search(r'^GRAINE\s*=\s*(\d+)', src, re.M); GRAINE = int(m.group(1)); T_FIGE = float(re.search(r'^T_FIGE\s*=\s*([\d.]+)', src, re.M).group(1))
AMORCE = re.search(r'AMORCE = """(.*?)""" % GRAINE', src, re.S).group(1) % GRAINE
PILOTE = re.search(r'PILOTE = """(.*?)""" % T_FIGE', src, re.S).group(1) % T_FIGE
POSE = re.search(r'POSE = """(.*?)"""', src, re.S).group(1)
out = []
with sync_playwright() as p:
    for passe in range(3):
        b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2); ctx.add_init_script(AMORCE)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} }")
        avant = pg.evaluate("()=>({now:performance.now(), n:promises.length, ids:promises.map(p=>p.id).join(','), places:promises.filter(p=>p.place).length, alea:Math.random()})")
        pg.evaluate(PILOTE)
        pg.evaluate(POSE, ['chamade', GRAINE, ['chamade', 'esquille']])
        for _ in range(6): pg.evaluate("()=>window.__images(40)"); pg.wait_for_timeout(120)
        e = pg.evaluate("()=>({g:Toile_graines().map(s=>s.join(':')).join(' | '), cle:(Toile.cle?Toile.cle():null), n:Toile.graines?Toile.graines():null})")
        out.append((avant, e)); print(passe, 'avant pilote :', {k: (round(v, 1) if isinstance(v, float) else (v[:40] if isinstance(v, str) else v)) for k, v in avant.items()}, '· clé', e['cle'], '· graines', e['n'], flush=True)
        b.close()
for i in range(1, 3):
    a, c = out[0][1]['g'].split(' | '), out[i][1]['g'].split(' | ')
    d = [(x, y) for x, y in zip(a, c) if x != y]; print('passe 0 contre', i, ':', len(a), len(c), 'graines ;', len(d), 'différentes', d[:6])
