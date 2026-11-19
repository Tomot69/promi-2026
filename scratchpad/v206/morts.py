import re, io, glob, json, collections
S = io.open('app.html', encoding='utf-8').read()
# le texte de tout ce qui peut appeler l'app : l'app, le moteur, les variantes, les juges, les bancs
ext = ''
for f in glob.glob('*.py') + [x for x in glob.glob('*.js') if x != 'check.js'] + glob.glob('variantes/*.js') + [x for x in glob.glob('*.html') if not x.startswith('zz-') and x != 'app.html']:
    try: ext += io.open(f, encoding='utf-8').read() + '\n'
    except Exception: pass
blocs = [(m.start(1), m.group(1), m.group(0)[:80]) for m in re.finditer(r'<script[^>]*>(.*?)</script>', S, re.S)]
decl = re.compile(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(')
mots = collections.Counter(re.findall(r'[A-Za-z_$][\w$]*', S))
motsX = collections.Counter(re.findall(r'[A-Za-z_$][\w$]*', ext))
cand = []
for off, code, tete in blocs:
    for m in decl.finditer(code):
        n = m.group(1)
        if mots[n] == 1 and motsX[n] == 0:   # seule occurrence : sa déclaration
            ligne = S.count('\n', 0, off + m.start()) + 1
            cand.append((ligne, n))
print(len(cand)); print(cand[:80])
json.dump(cand, open('scratchpad/v206/morts.json', 'w'))
print('---- window.X = … jamais lus')
aff = collections.Counter(re.findall(r'window\.([A-Za-z_$][\w$]*)\s*=(?!=)', S))
mortsW = []
for n, k in aff.items():
    lus = mots[n] - k
    # une lecture peut être window.n, n( , typeof n … ; toutes comptées par mots[n]
    if lus <= 0 and motsX[n] == 0: mortsW.append(n)
print(len(mortsW), sorted(mortsW))
for n in ['_dalleReelle','halo','_haloPelote','_retireFondFlaques','_v186Gel','doigtsVeille','openCell','_poseNette','buildAura','_flaquePelote','_echoPelote','_couronnePelote','feedKeep','_e4Cercle']:
    print(n, mots[n], motsX[n])
