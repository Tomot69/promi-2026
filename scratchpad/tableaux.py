# -*- coding: utf-8 -*-
"""LES TABLEAUX DE TRIPLETS — treize, en JS, jamais convertis.
   Ils ne sont écrits ni en hexadécimal ni en rgb() : les trois passes de la bascule ne
   pouvaient pas les voir. Ce sont eux qu'on voyait encore en ancienne identité — la sphère
   de l'Aura (SPECTRE), le fond de la Toile (GPIX·GBRA·GLI·GMOS·GENC·GLIGHT), le spectre
   des états (ETATS), les grappes de l'onboarding et de la page + (pal, cols, SIG).
   DEUX ÉTAGES : le lot du 16 septembre, puis celui du 17. Ils ont manqué les deux."""
import sys, io, re
sys.path.insert(0,'scratchpad')
from couleurs_lab import *
from table_palette import ANCRES as A16, transporte_w
from table2 import ANCRES as A17, EPINGLES, FIXES, transporte2
from bascule2 import carte

T17,_ = carte()
# ── étage 1 : le 16 septembre. Bleu, framboise, menthe et lilas y étaient INTACTS. ──
B16 = [(25,75,'orange'), (75,112,'creme'), (300,332,'mauve')]
INTACT16 = {'#3A54FF','#FA2258','#2BE88C','#8FA0FF','#D0B0FF','#E4CEFD','#06231A'}
def etage16(h):
    h=h.upper()
    if h=='#F07A2E': return '#DD4D23'
    if h in INTACT16: return h
    L,C,hh = lch(h)
    if C < 2: return h
    for a,b,nom in B16:
        if a<=hh<b: return transporte_w(h,*A16[nom])
    if 250<=hh<300: return transporte_w(h,*A16['encre']) if L<40 else h
    return h
# ── étage 2 : le 17 septembre ──
B17 = [(250,300,'bleu'),(300,332,'lilas'),(332,360,'framboise'),(0,25,'framboise'),
       (75,112,'creme'),(112,200,'menthe'),(200,250,'bleu')]
def etage17(h):
    h=h.upper()
    if h in T17: return T17[h]
    if h in FIXES or h in EPINGLES.values(): return h
    L,C,hh = lch(h)
    if C < 3: return h
    for a,b,nom in B17:
        if a<=hh<b: return transporte2(h,*A17[nom])
    return h
def neuve(h): return etage17(etage16(h))

if __name__=='__main__':
    S=io.open('app-identite.html',encoding='utf-8').read()
    st=[(m.start(),m.end()) for m in re.finditer(r'<style[^>]*>.*?</style>',S,re.S)]
    mk=bytearray(len(S))
    for a,b in st:
        for i in range(a,b): mk[i]=1
    pat=re.compile(r'\[\s*\[\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\](?:\s*,\s*\[\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\])+\s*\]')
    GARDE = ('SIGNAL','PALS')   # déjà remplacés par les vingt palettes du PDF
    hors=[]; n=0
    for m in list(pat.finditer(S))[::-1]:
        if mk[m.start()]: continue
        av=S[max(0,m.start()-60):m.start()]
        nom=re.search(r'([A-Za-z_$][\w$]*)\s*=\s*$',av)
        nom=nom.group(1) if nom else '?'
        if nom in GARDE: continue
        if 'var PALS' in av or 'cols:' in av[-12:]: continue
        bloc=m.group(0); avant=[]; apres=[]
        def rem(t):
            r,g,b=int(t.group(1)),int(t.group(2)),int(t.group(3))
            h=rgb2hex(r,g,b); nh=neuve(h); avant.append(h); apres.append(nh)
            nr,ng,nb=hex2rgb(nh); return f'[{nr},{ng},{nb}]'
        neufbloc=re.sub(r'\[\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\]',rem,bloc)
        if neufbloc!=bloc:
            S=S[:m.start()]+neufbloc+S[m.end():]; n+=1
        hors.append((S.count('\n',0,m.start())+1,nom,avant,apres))
    io.open('app-identite.html','w',encoding='utf-8').write(S)
    print(f"{n} tableaux convertis\n")
    for ln,nom,av,ap in sorted(hors):
        print(f"l.{ln:>6} {nom}")
        for a,b in zip(av,ap):
            mark='   ' if a==b else ' → '
            print(f"        {a}{mark}{b}" + ('' if a==b else f"   ΔE {de(a,b):.0f}"))
