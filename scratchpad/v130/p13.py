import io
S=io.open('app.html',encoding='utf-8').read()
old="""    var encre  = corpsEncre();
    var choisi = window.promiPinceau(null);"""
new="""    var encre  = (nat==='promi') ? '#201908' : corpsEncre();   /* v130 (C-050) : le corps d'un Promi est pastel dans les deux thèmes (crème, Tropical Breeze) — l'encre */
    var choisi = window.promiPinceau(null);"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
