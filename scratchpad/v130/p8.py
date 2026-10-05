import io
S=io.open('redteam_reactif.py',encoding='utf-8').read()
old="""    pg.wait_for_timeout(ANIME_TENIR); e=lire(); juge("""
new="""    t0=pg.evaluate("()=>performance.now()")
    pg.wait_for_function("()=>!window._tenirAnime", timeout=ANIME_MAX); dt=pg.evaluate("(t)=>performance.now()-t", t0)
    ok("tenir · l'animation rend la main en moins de %d ms"%ANIME_MAX, dt<ANIME_MAX, '%d ms'%dt)
    e=lire(); juge("""
assert S.count(old)==1; S=S.replace(old,new)
old="""ANIME_TENIR = 1100                                     # l'animation de « tenir » dure 1 000 ms (v124), en dur"""
new="""ANIME_MAX = 3000                                       # l'amande (1 000 ms, v124) puis « juste après » : la fiche couvre l'Aura ; borne en dur"""
assert S.count(old)==1; S=S.replace(old,new)
S=S.replace("""    # l'Aura est SOUS la fiche pendant l'animation de « tenir » (1 000 ms, décidé v124 : aucun travail pendant elle) :
    # elle doit être juste à l'image qui suit la fin de l'animation — donc avant qu'on puisse la revoir.""","""    # l'Aura est SOUS la fiche pendant l'animation de « tenir » (décidé v124 : aucun travail pendant elle) :
    # elle doit être juste à l'image qui suit la fin de l'animation — donc avant qu'on puisse la revoir.""")
io.open('redteam_reactif.py','w',encoding='utf-8').write(S)
