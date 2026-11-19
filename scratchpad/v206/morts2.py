import re, io, glob, collections
S = io.open('app.html', encoding='utf-8').read()
ext = ''
for f in glob.glob('*.py') + [x for x in glob.glob('*.js') if x != 'check.js'] + glob.glob('variantes/*.js') + [x for x in glob.glob('*.html') if not x.startswith('zz-') and x != 'app.html']:
    try: ext += io.open(f, encoding='utf-8').read() + '\n'
    except Exception: pass
motsX = collections.Counter(re.findall(r'[A-Za-z_$][\w$]*', ext))
def fin_corps(i):
    """i : l'index de '{' ; rend l'index de la '}' qui le ferme (sans gérer chaînes et commentaires : approximatif, vérifié à la main ensuite)"""
    d = 0
    for j in range(i, min(len(S), i + 200000)):
        c = S[j]
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: return j
    return -1
idx = collections.defaultdict(list)
for t in re.finditer(r'[A-Za-z_$][\w$]*', S): idx[t.group(0)].append(t.start())
res = []
for m in re.finditer(r'<script[^>]*>(.*?)</script>', S, re.S):
    a, b = m.start(1), m.end(1)
    for d in re.finditer(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{', S[a:b]):
        n = d.group(1); deb = a + d.start(); acc = a + d.end() - 1; fin = fin_corps(acc)
        if fin < 0: continue
        dehors = sum(1 for q in idx[n] if q < deb or q > fin)
        if dehors == 0 and motsX[n] == 0:
            res.append((S.count('\n', 0, deb) + 1, S.count('\n', 0, fin) + 1, n))
print(len(res))
for r in res: print(r)
