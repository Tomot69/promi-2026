# -*- coding: utf-8 -*-
"""LOT IDENTITÉ — 17 septembre 2026. Applique la planche des correspondances à app.html.
   Rien n'est deviné : les 234 couleurs du jeu suivent la famille de leur NOM (posée le
   16 sept. depuis le contexte) ; les 111 couleurs qui ne vivent qu'en JS suivent une
   BANDE DE TEINTE, déclarée ici et imprimée dans le rapport."""
import sys, io, re, json, collections
sys.path.insert(0,'scratchpad')
from couleurs_lab import *
from table2 import table as _t2, ANCRES, EPINGLES, FIXES, transporte2

# ── LES BANDES DE TEINTE — pour ce qui ne vit qu'en JS ────────────────────────────
#  (borne haute exclue ; l'app pose ses bleus vers h 294 et ses mauves vers h 305)
BANDES = [(250,300,'bleu'), (300,332,'lilas'), (332,360,'framboise'), (0,25,'framboise'),
          (25,75,None),     # l'orange « à tenir » ne bouge pas
          (75,112,'creme'), (112,200,'menthe'), (200,250,'bleu')]
# ── CE QU'ON NE TOUCHE JAMAIS ────────────────────────────────────────────────────
INTOUCHABLE = {
 '#4285F4','#34A853','#FBBC05','#EA4335',        # les quatre de Google — une marque tierce
 '#FFFFFF','#000000','#FFF','#000',
}
GRIS_PUR = lambda h: (lambda r: r[0]==r[1]==r[2])(hex2rgb(h))
CHROMA_MINI = 3.0     # sous cette chroma, une couleur n'a pas de teinte à transporter

def carte():
    T = {k.upper():v.upper() for k,v in _t2().items()}
    S = io.open('app.html',encoding='utf-8').read()
    st=[(m.start(),m.end()) for m in re.finditer(r'<style[^>]*>.*?</style>',S,re.S)]
    mk=bytearray(len(S))
    for a,b in st:
        for i in range(a,b): mk[i]=1
    horsjeu=collections.Counter()
    for m in re.finditer(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b',S):
        if mk[m.start()]: continue
        h=m.group(0).upper()
        if len(h)==4: h='#'+''.join(c*2 for c in h[1:])
        horsjeu[h]+=1
    hb={}
    for h in horsjeu:
        if h in T or h in FIXES or h in INTOUCHABLE or GRIS_PUR(h): continue
        L,C,hh = lch(h)
        if C < CHROMA_MINI: continue
        anc=None
        for a,b,nom in BANDES:
            if a<=hh<b: anc=nom; break
        if not anc: continue
        hb[h]=transporte2(h,*ANCRES[anc])
    T.update(hb)
    for h in list(T):
        if T[h]==h: del T[h]
    return T, hb

if __name__=='__main__':
    T,hb=carte()
    print(f"{len(T)} couleurs basculées, dont {len(hb)} qui ne vivent qu'en JS\n")
    print("### LES COULEURS QUI NE VIVENT QU'EN JS (bandes de teinte)")
    for h in sorted(hb,key=lambda x:lch(x)[2]):
        print(f"   {h} → {hb[h]}   ΔE {de(h,hb[h]):5.1f}  h {lch(h)[2]:6.1f}→{lch(hb[h])[2]:6.1f}")
