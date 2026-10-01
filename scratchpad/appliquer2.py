# -*- coding: utf-8 -*-
"""Applique la bascule du 17 septembre sur une COPIE — app-identite.html.
   Quatre passes, chacune comptée : les hexadécimaux, les triplets `--c-*-rgb`,
   les rgb()/rgba() littéraux du JS, et les cinq sites de l'encre profonde."""
import sys, io, re, shutil
sys.path.insert(0,'scratchpad')
from couleurs_lab import *
from bascule2 import carte

CIBLE = 'app-identite.html'
shutil.copyfile('app.html', CIBLE)
S = io.open(CIBLE, encoding='utf-8').read()
T,_ = carte()

# ── 1 · les hexadécimaux, partout ────────────────────────────────────────────────
n1 = 0
def rem(m):
    global n1
    h = m.group(0).upper()
    if h in T: n1 += 1; return T[h]
    return m.group(0)
S = re.sub(r'#[0-9a-fA-F]{6}\b', rem, S)

# ── 2 · les triplets `--c-*-rgb` : ils se RECALCULENT depuis leur jumeau ─────────
noms = dict(re.findall(r'(--c-[a-z0-9-]+?):(#[0-9A-Fa-f]{6})', S))
n2 = 0
def remrgb(m):
    global n2
    cle = m.group(1)
    h = noms.get(cle)
    if not h: return m.group(0)
    r,g,b = hex2rgb(h)
    neuf = f'{cle}-rgb:{r},{g},{b}'
    if neuf != m.group(0): n2 += 1
    return neuf
S = re.sub(r'(--c-[a-z0-9-]+?)-rgb:\s*\d+\s*,\s*\d+\s*,\s*\d+', remrgb, S)

# ── 3 · les rgb() / rgba() littéraux ─────────────────────────────────────────────
n3 = 0
def remlit(m):
    global n3
    r,g,b = int(m.group(2)), int(m.group(3)), int(m.group(4))
    h = rgb2hex(r,g,b)
    if h in T:
        n3 += 1
        nr,ng,nb = hex2rgb(T[h])
        return f'{m.group(1)}({nr},{ng},{nb}'
    return m.group(0)
S = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', remlit, S)

# ── 4 · L'ENCRE PROFONDE — cinq sites nommés, jamais les 40 autres #201908 ───────
#   Relevés dans sauvegardes/app-avant-PALETTE-16sept.html : c'est le FOND D'ÉCRAN sombre
#   (le `--ground` du device et les quatre remplissages de canevas). Le lot du 16 septembre
#   les avait fondus dans #201908 ; la planche les rend distincts (#120E05).
SITES = [
 ("--ground:#201908", "--ground:#120E05"),
 ("g.fillStyle=lightT?'#F7F0DE':'#201908'", "g.fillStyle=lightT?'#F7F0DE':'#120E05'"),
 ("g.fillStyle=(clair!=null?clair:isLightM())?'#F7F0DE':'#201908'",
  "g.fillStyle=(clair!=null?clair:isLightM())?'#F7F0DE':'#120E05'"),
 ("g.fillStyle=isLightM()?(window._shAllColored?'#DDD2B8':'#F1ECD9'):'#201908';g.fillRect(0,0,c.pw,c.ph)",
  "g.fillStyle=isLightM()?(window._shAllColored?'#DDD2B8':'#F1ECD9'):'#120E05';g.fillRect(0,0,c.pw,c.ph)"),
 ("g.fillStyle=isLightM()?(window._shAllColored?'#DDD2B8':'#F1ECD9'):'#201908';g.fillRect(0,0,pw,ph)",
  "g.fillStyle=isLightM()?(window._shAllColored?'#DDD2B8':'#F1ECD9'):'#120E05';g.fillRect(0,0,pw,ph)"),
]
n4 = 0
for vieux, neuf in SITES:
    v = vieux
    for k, nv in T.items():                 # les motifs sont écrits en valeurs D'AVANT
        v = v.replace(k, nv).replace(k.lower(), nv)
    if S.count(v) == 1:
        S = S.replace(v, neuf if v == vieux else
                      (lambda x: x)(neuf))
        n4 += 1
    else:
        print(f"  ⚠ site non unique ({S.count(v)}) : {vieux[:60]}")

io.open(CIBLE,'w',encoding='utf-8').write(S)
print(f"{n1} hexadécimaux · {n2} triplets --c-*-rgb · {n3} rgb() littéraux · {n4}/5 sites d'encre profonde")
