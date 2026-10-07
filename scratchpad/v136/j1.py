import io
def patch(f, pairs):
    S=io.open(f,encoding='utf-8').read()
    for a,b in pairs:
        assert S.count(a)==1,(f,a[:60],S.count(a)); S=S.replace(a,b)
    io.open(f,'w',encoding='utf-8').write(S)
patch('redteam_decisions.py',[("""        D.append((nom, th, 'corps', TERRE, 'v8 (21 sept.) : la terre, dans les deux thèmes'))
        D.append((nom, th, 'echeance', AMANDE, 'Q269 (23 sept.) · Q299 : « TENUE » en amande'))
        D.append((nom, th, 'titre', CREME, 'v8 (21 sept.) : sur la terre, le texte passe crème'))""",
"""        # ⚑ v136 (Tom, 7 oct. 2026, C-059) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_decisions-avant-v136.py) :
        # « en clair, le corps d'une fiche tenue (Promi et Chiche) devient la crème #F7F0DE ; la terre reste en sombre ;
        #   la mention TENU en #00341A en clair ». La règle d'avant (« la terre, dans les deux thèmes », v8) ne vaut plus qu'en sombre.
        if th == 'dark':
            D.append((nom, th, 'corps', TERRE, 'v8 (21 sept.) + v136 : la terre, en sombre'))
            D.append((nom, th, 'echeance', AMANDE, 'Q269 (23 sept.) · Q299 : « TENUE » en amande sur la terre'))
            D.append((nom, th, 'titre', CREME, 'v8 (21 sept.) : sur la terre, le texte passe crème'))
        else:
            D.append((nom, th, 'corps', CREME, 'v136 (7 oct., C-059) : en clair, le corps d\\'une fiche tenue est la crème'))
            D.append((nom, th, 'echeance', '#00341A', 'v136 (7 oct., C-059) : la mention TENU en #00341A en clair'))
            D.append((nom, th, 'titre', ENCRE, 'v136 : sur la crème, le texte est à l\\'encre (17 sept.)'))""")])
patch('redteam_accueil.py',[("""            and abs(pu['w'] - 68) <= 1 and abs(pu['x'] - 161) <= 1 and abs(pu['y'] - 726) <= 1""",
"""            and abs(pu['w'] - 84) <= 1 and abs(pu['h'] - 84) <= 1 and abs(pu['x'] - 153) <= 1 and abs(pu['y'] - 718) <= 1   # ⚑ v136 (Tom, 7 oct. 2026, C-070) : le + agrandi d'environ 25 % — 84 pt (68 avant), centré dans la barre ; original : sauvegardes/redteam_accueil-avant-v136.py""")])
