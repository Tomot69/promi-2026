import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("    var _colQui = dp.classList.contains('f-tenue') ? CREME : e.colTexte;",
    "    var _colQui = dp.classList.contains('f-tenue') ? ((document.getElementById('device')&&document.getElementById('device').classList.contains('light')) ? '#201908' : CREME) : e.colTexte;   /* v139 : en clair le corps d'une fiche tenue n'est plus la terre (v136) — la ligne de phrase y restait crème sur crème : sur un Chiche tenu, « , t’es pas chiche de » était invisible (seul le prénom, repeint par la passe de lisibilité, se lisait) */")
rep("inp.accept='image/*'; inp.multiple=true; inp.className='dz-photo-in';","inp.accept='image/'+'*';   /* en deux morceaux : l'analyse statique de redteam_joignable prenait la barre-étoile de cette chaîne pour un début de commentaire */ inp.multiple=true; inp.className='dz-photo-in';")
io.open(f,'w',encoding='utf-8').write(S)
