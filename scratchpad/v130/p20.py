import io
S=io.open('redteam_couleurs_ref.py',encoding='utf-8').read()
old="""                    if cle[1] == 'dark' and re.search(r'detailPoster|createSheet', k) and va and vr:"""
new="""                    if cle[1] == 'dark' and cle[0] in E8_ECRANS and va and vr:"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    def compare_tout(A, B):"""
new="""    # E8 — les écrans qui montrent le corps sombre d'un Promi (fiche Promi non tenue, son Peaufiner, un gardé de côté, la page + d'un Promi,
    #      l'instant, qui part d'une fiche à tenir) ; les mêmes noms qu'en tête de redteam_air
    E8_ECRANS = ('fiche à tenir', 'fiche en cours', 'gardé de côté', 'page +', 'Peaufiner', "l'instant arrive", "l'instant referme", "l'instant après")
    def compare_tout(A, B):"""
assert S.count(old)==1; S=S.replace(old,new)
old="""En sombre, sur un nœud de `detailPoster` ou de `createSheet` et là seulement :"""
assert S.count(old)==1; S=S.replace(old,"""En sombre, sur les écrans qui montrent ce corps (`E8_ECRANS`) et là seulement :""")
old="""E7 ombre crème en sombre %d' % (exceptions['E1'], exceptions['E3'], exceptions['E4'], exceptions['E5'], exceptions['E6'], exceptions['E7']))"""
assert S.count(old)==1; S=S.replace(old,"""E7 ombre crème en sombre %d · E8 Tropical Breeze et son encre (v130) %d' % (exceptions['E1'], exceptions['E3'], exceptions['E4'], exceptions['E5'], exceptions['E6'], exceptions['E7'], exceptions['E8']))""")
io.open('redteam_couleurs_ref.py','w',encoding='utf-8').write(S)
