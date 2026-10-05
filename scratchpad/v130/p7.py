import io
S=io.open('redteam_reactif.py',encoding='utf-8').read()
old="""    e=lire(); juge('tenir · Aura restée affichée', e, 'Aura', True, 'tenu')"""
new="""    # l'Aura est SOUS la fiche pendant l'animation de « tenir » (1 000 ms, décidé v124 : aucun travail pendant elle) :
    # elle doit être juste à l'image qui suit la fin de l'animation — donc avant qu'on puisse la revoir.
    pg.wait_for_timeout(ANIME_TENIR); e=lire(); juge('tenir · Aura restée affichée', e, 'Aura', True, 'tenu')"""
assert S.count(old)==1; S=S.replace(old,new)
old="""MOISSON_PETIT, MOISSON_GRAND, SEUIL = 3, 6, 5          # Q187, en dur"""
assert S.count(old)==1; S=S.replace(old, old+"\nANIME_TENIR = 1100                                     # l'animation de « tenir » dure 1 000 ms (v124), en dur")
io.open('redteam_reactif.py','w',encoding='utf-8').write(S)
