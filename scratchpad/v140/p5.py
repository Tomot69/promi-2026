import io
S=io.open('app.html',encoding='utf-8').read()
o="""#device#device .acc-barre #createBtn svg{width:38.5px!important;height:38.5px!important}
"""
assert S.count(o)==1
S=S.replace(o,o+"""/* ⚑ v140 (Tom, 10 oct. 2026, C-087) — « Agrandis la zone autour du + (le disque intérieur), en gardant l'épaisseur de l'anneau. S'il manque de
   la place, la barre du bas grandit en hauteur pour garder au moins 12 pt d'air au-dessus et au-dessous de l'anneau. Rien d'autre ne bouge. »
   Le disque passe de 33 à 45 pt ; l'anneau garde ses 13,5 ; le diamètre extérieur fait donc 72 (60 en v139). La barre passe de 88 à 100 de
   haut (730 → 830 ; 736 → 824 avant), six points de chaque côté : 12 pt d'air entre l'anneau et le bord intérieur de son contour. Le centre
   du +, la croix (27 de large) et les quatre entrées restent où ils étaient à l'écran (leur cote dans la barre descend de 6). */
#device#device #accBarre.acc-barre{top:730px!important;height:100px!important;border-radius:50px!important}
#device#device .acc-barre .dctrl{top:22.5px!important}
#device#device .acc-barre #createBtn,#device#device .acc-barre #createBtn.dhero{left:133px!important;top:12px!important;width:72px!important;height:72px!important}
""")
io.open('app.html','w',encoding='utf-8').write(S)
