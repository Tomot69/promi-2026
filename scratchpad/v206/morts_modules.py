"""v207 §3 — le code mort des modules repris : une fonction déclarée dont le nom n'apparaît nulle part hors de son propre corps (le module, l'app, les juges, les
bancs, les pages). Les IIFE nommées (`(function f(){…})()`) sont écartées."""
import re, io, glob, collections
F = ['variantes/trace-lettres.js', 'variantes/flaques.js']
tout = ''
for f in glob.glob('*.py') + glob.glob('*.html') + glob.glob('variantes/*.js') + glob.glob('*.js'):
    if f.startswith('zz-') or f == 'check.js': continue
    try: tout += io.open(f, encoding='utf-8').read() + '\n'
    except Exception: pass
for f in F:
    S = io.open(f, encoding='utf-8').read(); idx = collections.defaultdict(list)
    for t in re.finditer(r'[A-Za-z_$][\w$]*', S): idx[t.group(0)].append(t.start())
    ailleurs = collections.Counter(re.findall(r'[A-Za-z_$][\w$]*', tout.replace(S, '')))
    for d in re.finditer(r'(\(\s*)?\bfunction\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{', S):
        if d.group(1): continue
        n = d.group(2); i = d.end() - 1; dep = 0
        for j in range(i, len(S)):
            if S[j] == '{': dep += 1
            elif S[j] == '}':
                dep -= 1
                if dep == 0: break
        dehors = sum(1 for q in idx[n] if q < d.start() or q > j)
        if dehors == 0 and ailleurs[n] == 0: print(f, S.count('\n', 0, d.start()) + 1, n, '(%d lignes)' % (S.count('\n', d.start(), j) + 1))
    # les propriétés publiques TL.x / Flaques.x jamais lues ailleurs
    for m in sorted(set(re.findall(r'\b(?:TL|F|Flaques)\.([A-Za-z_$][\w$]*)\s*=(?!=)', S))):
        if len(idx[m]) <= 1 and ailleurs[m] == 0: print(f, 'propriété jamais lue :', m)
