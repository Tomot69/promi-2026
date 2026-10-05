import io
S=io.open('redteam_couleurs_ref.py',encoding='utf-8').read()
old="""  E7  v123 §2 : en sombre, l'ombre de la Pelote"""
new="""  E8  v130 (Tom, 5 oct. 2026) : le corps sombre d'un Promi #335382 devient Tropical Breeze #8ACBE8 (fiche Promi, page + d'un Promi),
      et ce qui est posé dessus passe à l'encre #201908. En sombre, sur un nœud de `detailPoster` ou de `createSheet` et là seulement :
      ① #335382 → #8ACBE8 (la même propriété) ; ② une couleur de texte, de contour ou de tracé → l'encre #201908. Rien d'autre.
  E7  v123 §2 : en sombre, l'ombre de la Pelote"""
assert S.count(old)==1; S=S.replace(old,new)
old="""exceptions = {'E1': 0, 'E3': 0, 'E4': 0, 'E5': 0, 'E6': 0, 'E7': 0}"""
assert S.count(old)==1; S=S.replace(old,"""exceptions = {'E1': 0, 'E3': 0, 'E4': 0, 'E5': 0, 'E6': 0, 'E7': 0, 'E8': 0}""")
old="""                    ecarts.append((cle, k, pr_, va, vr))
            for k, c in a['c'].items():"""
new="""                    if cle[1] == 'dark' and re.search(r'detailPoster|createSheet', k) and va and vr:
                        if '51, 83, 130' in vr and va == vr.replace('51, 83, 130', '138, 203, 232'): exceptions['E8'] += 1; continue          # ① le corps
                        if pr_ in ('color', 'tfill', 'bT', 'bR', 'bB', 'bL', 'fill', 'stroke', 'outline') and va == 'rgb(32, 25, 8)': exceptions['E8'] += 1; continue   # ② l'encre
                    ecarts.append((cle, k, pr_, va, vr))
            for k, c in a['c'].items():"""
assert S.count(old)==1; S=S.replace(old,new)
old="""print('exceptions nommées : E1 Toile entière %d canevas · E3 orange des murs %d · E4 Pelote et halo %d · E5 violations retirées %d · E6 trace crème (Q374) %d · E7 ombre crème en sombre %d' % (exceptions['E1"""
assert S.count(old)==1
i=S.index(old); j=S.index('\n',i); print(S[i:j][-200:])
io.open('redteam_couleurs_ref.py','w',encoding='utf-8').write(S)
