# -*- coding: utf-8 -*-
"""LA BASCULE DU 17 SEPTEMBRE — la planche des correspondances fait foi.
   ⚠ Sa colonne « avant » est celle de l'app AVANT le 16 septembre. Six lignes ont donc été
   RECHAÎNÉES : on part de la valeur que le lot du 16 leur a donnée, on va à la cible.

   Le transport : la TEINTE suit l'ancre EN PLEIN (une teinte n'a pas d'échelle) ; la clarté
   et la chroma ne la suivent qu'à proportion de la proximité en clarté (w = 1 − |ΔL|/45).
   Le §3 vit dans les CLARTÉS : les déplacer à l'aveugle casserait tous les seuils de 42."""
import sys; sys.path.insert(0,'scratchpad')
from couleurs_lab import *
import json, re, collections

# ── LES ANCRES ───────────────────────────────────────────────────────────────────
#  nom          valeur DANS L'APP AUJOURD'HUI → cible de la planche
ANCRES = {
 'bleu'      : ('#3A54FF', '#82AEF8'),   # le champ d'un Promi
 'framboise' : ('#FA2258', '#FFB8D2'),   # le champ d'un Chiche
 'lilas'     : ('#D0B0FF', '#C9A8F5'),   # le champ d'une Nuée
 'encours'   : ('#8FA0FF', '#FFD447'),   # la ligne « en cours »
 'menthe'    : ('#2BE88C', '#8FE08F'),   # la ligne « tenu »
 'lavande'   : ('#E4CEFD', '#E6D8FA'),   # la teinte très claire du lilas
 'creme'     : ('#F6F1E3', '#F3E7D1'),   # les plateaux et les cartes
 'orangeor'  : ('#B33638', '#F07A2E'),   # l'orange d'origine — accent, célébration
}
# ── LES ÉPINGLES — une valeur décidée, jamais un transport ───────────────────────
EPINGLES = {
 '#06231A':'#00341A',   # vert profond — corps d'une fiche tenue, surface d'exception
 '#89857E':'#A2947C',   # gris texte sombre
 '#6D685C':'#6E6350',   # gris chaud clair
 '#EAE7DC':'#E4D7BB',   # crème bordure — filets, contours
 '#EFE8D6':'#EFE3C7',   # crème dalle
}
# ── CE QUI NE BOUGE PAS ──────────────────────────────────────────────────────────
FIXES = {'#DD4D23','#F7F0DE','#201908','#291547','#FFFFFF','#000000','#00341A','#F07A2E'}

# ── QUELLE FAMILLE SUIT QUELLE ANCRE ─────────────────────────────────────────────
#  la famille est celle du NOM du jeton (--c-bleu45 → « bleu ») : elle a été posée le
#  16 septembre depuis le contexte lu dans app.html, elle n'est pas devinée ici.
FAM = {
 'bleu':'bleu', 'ton':'bleu',           # les corps sombres d'un Promi et la navy
 'framboise':'framboise',
 'mauve':'lilas',
 'menthe':'menthe',
 'creme':'creme', 'beige':'creme',
 'orange':None, 'brun':None, 'noir':None, 'blanc':None, 'periwinkle':'encours',
}
# les bleus périwinkle de l'app suivent « en cours », pas le champ d'un Promi : ils
# sont les dérivés de #8FA0FF, et la planche l'envoie au jaune.
ENCOURS = {'#8FA0FF'}   # ⚠ VÉRIFIÉ dans app.html : SEUL #8FA0FF porte « en cours »
# (`.ring-leg .rl-in`, la légende de l'anneau de l'Aura, et le rôle `en-cours` du jeu).
# Les six autres bleus pâles (--c-bleu60·62·67·80·83·85) sont du TEXTE et des voiles :
# les envoyer au jaune avec « en cours » les faisait bouger de ΔE 140.

def transporte2(derive, av, ap, portee=45.0):
    Ld,Cd,hd = lch(derive); La,Ca,ha = lch(av); Lb,Cb,hb = lch(ap)
    r0,g0,b0 = hex2rgb(derive)
    if r0==g0==b0: return derive.upper()          # un gris PUR n'a pas de teinte
    w = max(0.0, 1.0 - abs(Ld-La)/portee)
    L = max(0.0, min(100.0, Ld + (Lb-La)*w))
    h = (hd + (hb-ha)) % 360                       # la teinte suit EN PLEIN
    ratio = (Cb/Ca) if Ca > 2 else 1.0
    C = max(0.0, Cd * (1.0 + (ratio-1.0)*w))
    r,g,b = lab2rgb(*lch2lab(L,C,h)); k=1.0
    while (min(r,g,b)<-0.5 or max(r,g,b)>255.5) and k>0.02:
        k-=0.04; r,g,b=lab2rgb(*lch2lab(L,C*k,h))
    return rgb2hex(r,g,b)

def table():
    J=json.load(open('PROMI-TOKENS.json'))
    T={}
    for nom,(a,b) in ANCRES.items(): T[a.upper()]=b.upper()
    T.update({k.upper():v.upper() for k,v in EPINGLES.items()})
    for k,v in J['palette_fixe'].items():
        v=v.upper()
        if v in FIXES or v in T: continue
        if v in ENCOURS: T[v]=transporte2(v,*ANCRES['encours']); continue
        f=re.match(r'--c-([a-z]+)',k).group(1)
        anc=FAM.get(f)
        if not anc: continue
        T[v]=transporte2(v,*ANCRES[anc])
    for h in FIXES: T.pop(h,None)
    return T

if __name__=='__main__':
    T=table(); J=json.load(open('PROMI-TOKENS.json'))
    inv=collections.defaultdict(list)
    for k,v in J['palette_fixe'].items(): inv[v.upper()].append(k)
    print(f"{len(T)} couleurs basculées\n")
    fam=collections.defaultdict(list)
    for v,n in T.items():
        noms=inv.get(v,['(hors jeu)'])
        f=re.match(r'--c-([a-z]+)',noms[0]).group(1) if noms[0]!='(hors jeu)' else 'hors'
        fam[f].append((v,n,noms[0]))
    for f in sorted(fam):
        print(f"### {f}")
        for v,n,nm in sorted(fam[f],key=lambda x:lch(x[0])[0]):
            print(f"   {v} → {n}   ΔE {de(v,n):5.1f}  L* {lch(v)[0]:5.1f}→{lch(n)[0]:5.1f}  "
                  f"h {lch(v)[2]:6.1f}→{lch(n)[2]:6.1f}   {nm}")
        print()
