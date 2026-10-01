# -*- coding: utf-8 -*-
"""LA TABLE DE BASCULE — quatre ancres décidées par Tom, leurs dérivés transportés.
   Le transport : la TEINTE suit l'ancre en plein ; la clarté et la chroma ne la suivent
   qu'à proportion de la proximité (poids w = 1 − |ΔL_dérivé| / 40). Sans ce poids, un corps
   sombre dérivé de l'orange (#2E1C13, L*12) tombait à L*1 — noir."""
import sys; sys.path.insert(0,'scratchpad')
from couleurs_lab import *

ANCRES = {
 'creme' : ('#F4EEE1','#F7F0DE'),
 'encre' : ('#16171B','#201908'),
 'orange': ('#F07A2E','#DD4D23'),
 'mauve' : ('#8A5CF0','#291547'),
}

def transporte_w(derive, av, ap, portee=40.0):
    Ld,Cd,hd = lch(derive); La,Ca,ha = lch(av); Lb,Cb,hb = lch(ap)
    r0,g0,b0 = hex2rgb(derive)
    if r0==g0==b0: return derive.upper()   # un gris PUR n'a pas de teinte à transporter : il reste tel quel
    w = max(0.0, 1.0 - abs(Ld-La)/portee)
    L = max(0.0, min(100.0, Ld + (Lb-La)*w))
    C = max(0.0, Cd + (Cb-Ca)*w)
    h = (hd + (hb-ha)) % 360
    r,g,b = lab2rgb(*lch2lab(L,C,h)); k=1.0
    while (min(r,g,b)<-0.5 or max(r,g,b)>255.5) and k>0.02:
        k-=0.04; r,g,b=lab2rgb(*lch2lab(L,C*k,h))
    return rgb2hex(r,g,b)

# ── les familles, nommées à la main depuis l'inventaire (contexte lu dans app.html) ──
CREME = """#F3EFE6 #E7E5DF #ECE6D9 #F7F3EA #EFEADC #F4EFE6 #E8E0D0 #C9C4B4 #C7C0B2
#EFE9DC #EAE3D4 #F0EEE8 #E7E4DB #DBD0BA #E7DFCE #DED7C6 #F3EDE1 #C9C2B4 #EDECE7 #BDBAB4
#CDC6B8 #BDB6A8 #EDEAE2 #F2F0E9 #E4DAC6 #E2D8C4 #D4C8AF #FAF3E5 #FFFAEF #F4EBDB #FCF6EA
#F7EFE0 #E0CFB6 #EADFCE #DCCBB2 #CDB894 #FDFBF6 #EAD9A0
#6E685C #A8A396 #9A9384 #6B6658 #B3A78F #4A463C #4A4740 #6F6B64 #7A7263 #6B6353 #8A7E70 #A79C8E""".split()

# les surfaces sombres et les gris de sous-texte : ils suivent l'encre, qui passe du bleu-noir au brun
ENCRE = """#141519 #101218 #2C2D3A #121216 #17181F #1C1D22 #0F1013 #2A2C34
#1A1A26 #1C1C28 #12131A #23242A #14141C #0E0E18 #1D1E25 #1A1A1E #12141B #0E0F14 #14161D
#131319 #0C0D11 #0A0B10
#83858C #A8ABBC #5D636D #9294A0 #8F8A9A #3A3C4C #3C3E50 #6B6878 #A6A9B4 #9A9DB0 #8C8E99
#3A3C42 #5C5E66 #6F737D #9B94A6 #6A6C72 #42444D #6A6F7A #8A8F99 #8B8A94 #7E83A0 #8B90A6
#8A8AA0 #55576C #55556A #54566A
#E9ECF5 #CFD3DB #EFF1FB #E7EAF6 #E2E6F4 #EDF0FA #E7EAF4 #ECECF0 #F2F2F6 #F5F6FA""".split()

# les dérivés de l'accent : terracotta du gardé de côté, pêches du Chiche, corps sombres
ORANGE = """#B8552B #C0533A #F2977A #C25A2E #F0663C #C2461F #E39170 #B4522A #F0A07E
#C4562F #B4552F #8F4326 #FFC0A8 #F1DBCF #2E1C13 #2A1912 #3A2A22 #2E211A
#241913 #1A1815 #1C1A17 #1A1613 #14130F #F6DCC4 #FFE0CF #FFE2D2 #F7EDE7 #F1E4DB #D8B0A0
#F4D9C8 #F0C9B6 #FBE7D8 #F6C6A0""".split()

INTACT = """#3A54FF #FA2258 #2BE88C #8FA0FF #E4CEFD #06231A #FFFFFF #FFF #000000 #000
#D0B0FF #CBAAFF #DCE1FF #4285F4 #34A853 #FBBC05 #EA4335 #FF5A5A
#D98A4A #C8682E #E0A23C #B5762F #A85C32 #CAA07A #D49A5E #F0C9A0 #E59CA6 #A9C5A0 #C9B8E0
#9FC0D8 #E6B8C2 #8FC83E #4FC0B0 #DCCB46 #A85FB0 #4F9AD8 #7BCB56 #C9D050 #23407A #3F6FA0
#88A8C8 #CFDAE6 #5A86B0 #B1C3D6 #2C5286 #9A6B5E #2C6FAE #2C7A5B""".split()

def table():
    T={}
    for a,b in [(ANCRES['creme'][0],ANCRES['creme'][1])]: pass
    T[ANCRES['creme'][0]]  = ANCRES['creme'][1]
    T[ANCRES['encre'][0]]  = ANCRES['encre'][1]
    # ⚑ LE FOND DU MODE EST LA VALEUR DONNÉE, PAS UN TRANSPORT. L'app a DEUX crèmes de fond
    #   (#F4EEE1 la surface, le fond du device) et DEUX encres de fond (#16171B, #0B0C12).
    #   Tom écrit « le clair devient #F7F0DE — fond du mode clair » et « le fond du mode sombre
    #   devient ce brun » : les quatre vont donc sur les deux valeurs, sans transport.
    T['#EFEAE0'] = ANCRES['creme'][1]
    T['#0B0C12'] = ANCRES['encre'][1]
    T['#0E0F12'] = ANCRES['encre'][1]   # « LE CORPS D'ÉCRAN (§1.3) : en sombre » — c'est LE fond qu'on voit
    T[ANCRES['orange'][0]] = ANCRES['orange'][1]
    T[ANCRES['mauve'][0]]  = ANCRES['mauve'][1]
    for h in CREME:  T[h]=transporte_w(h,*ANCRES['creme'])
    for h in ENCRE:  T[h]=transporte_w(h,*ANCRES['encre'])
    for h in ORANGE: T[h]=transporte_w(h,*ANCRES['orange'])
    for h in INTACT: T.pop(h,None)
    return T

if __name__=='__main__':
    T=table()
    print(f"{len(T)} couleurs basculées\n")
    for fam,lst in [('ANCRES',[ANCRES[k][0] for k in ANCRES]),('CRÈME',CREME),('ENCRE',ENCRE),('ORANGE',ORANGE)]:
        print(f"### {fam}")
        for h in lst:
            if h in T:
                print(f"   {h} → {T[h]}   ΔE {de(h,T[h]):5.1f}   L* {lch(h)[0]:5.1f}→{lch(T[h])[0]:5.1f}  h {lch(h)[2]:6.1f}→{lch(T[h])[2]:6.1f}")
        print()
