# v151 : le registre AVANT tout travail — validations de Tom, chantiers rouverts, deux numéros neufs (C-159, C-160)
import io
p='CHANTIERS.md'; S=io.open(p,encoding='utf-8').read()
def etat(c, nouvel, ajout):
    global S
    L=[l for l in S.split('\n') if l.startswith('| %s |'%c)]
    assert len(L)==1, c
    cols=L[0].split('|')
    cols[4]=' %s '%nouvel
    cols[5]=' '+ajout+' '+cols[5].strip()+' '
    S=S.replace(L[0], '|'.join(cols))
etat('C-158', 'VALIDÉ PAR TOM', "**v151 (18 oct.) : validé par Tom sur iPhone (les 17 pt sur la page + du Cercle compris).**")
etat('C-126', 'EN COURS', "**v151 : la flèche orange en sombre est validée par Tom ; rouvert — en sombre, « TRACE POUR PLANTER » n'est plus vert : une couleur claire de la palette, la crème #F7F0DE (décision du chef de chantier), 4,5:1 au moins sur son fond réel ; le clair ne change pas.**")
etat('C-124', 'EN COURS', "**v151 : la fin de l'onboarding (deux lignes alignées à droite) est validée par Tom (Q546) ; rouvert — en sombre, Primo, Deuxio, Tertio prennent le même bleu qu'en clair (sous 3:1 : le bleu Promi #82AEF8) ; « La suite t'appartient. » descend de 6 à 12 pt, toujours centrée.**")
etat('C-154', 'EN COURS', "**v151 : rouvert par Tom — la vague de création revient au violet #291547 : une parole créée est « en cours » ; l'orange de v150 reposait sur une prémisse fausse.**")
etat('C-157', 'EN COURS', "**v151 : rouvert par Tom — dans les pages + du Promi et du Chiche (et du Cercle s'il porte le même texte), « TRACE POUR … » passe en orange #FB4C0D comme la flèche, clair et sombre ; « trace ta moitié » suit (Q545) ; NE PAS TOUCHER AUX FICHES ; la règle de l'orange s'étend : le départ d'une action ET son libellé.**")
etat('C-149', 'EN COURS', "**v151 : rouvert par Tom — « Garder de côté » encore 1 mm (6 pt) plus bas dans les trois pages + ; inclinaison inchangée ; ni le bord de l'écran ni la barre du bas.**")
neuf = [
 ('C-159','18 oct. · v151 §8',"« Rejouer l'onboarding : le texte s'adapte » : quand on rejoue l'onboarding et que la Toile a déjà des dalles, la parole plantée n'est plus la première ; dès que la Toile compte au moins une dalle avant cette plantation, le texte devient, mot pour mot : « PROMI planté ! » « Une nouvelle dalle sur ta Toile, félicitations. Plus qu'à le tenir. » ; le reste de la chorégraphie ne change pas ; chaque autre mention de « premier », « première », « premiers » dans l'onboarding suit la même règle."),
 ('C-160','18 oct. · v151 §2 (Q544)',"« L'échéance compte enfin les jours » : l'échéance est une date comparée à aujourd'hui, dans Swift ET dès maintenant dans le prototype ; une parole dont l'échéance est dépassée et qui n'est pas tenue passe « à tenir » ; recalcul au lancement et à chaque retour au premier plan ; paramètre de test ?jour=+N."),
]
lignes=S.split('\n'); i=max(k for k,l in enumerate(lignes) if l.startswith('| C-158 |'))
for j,(n,d,t) in enumerate(neuf):
    assert not any(l.startswith('| %s |'%n) for l in lignes)
    lignes.insert(i+1+j, '| %s | %s | %s | EN COURS | — | — | v151 |'%(n,d,t))
io.open(p,'w',encoding='utf-8').write('\n'.join(lignes)); print('ok')
