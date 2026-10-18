# v150 : le registre AVANT tout travail — validations de Tom, chantiers rouverts, deux numéros neufs (C-157, C-158)
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
for c in ('C-153','C-145','C-155','C-156'):
    etat(c, 'VALIDÉ PAR TOM', '**v150 (18 oct.) : validé par Tom sur iPhone.**')
etat('C-154', 'EN COURS', "**v150 : validé par Tom SAUF la couleur — la vague de création passe à l'orange de « à tenir » #DD4D23 (« une parole créée passe à tenir »).**")
for c, quoi in (('C-149', "« Garder de côté » 4 pt plus bas (0,6 mm) ; l'inclinaison est validée"), ('C-124', "« Tout le monde promet. Toi, tu tiens parole. », alignée à droite ; « La suite t'appartient. » centrée ; le reste de l'onboarding est validé"), ('C-126', "en sombre, toute la flèche du premier Promi, trait compris, en orange #FB4C0D comme en clair")):
    etat(c, 'EN COURS', '**v150 : rouvert par Tom — %s.**' % quoi)
neuf = [
 ('C-157','18 oct. · v150 §2',"« Pages + seulement : TRACE POUR PLANTER et LANCER » : ne pas toucher aux fiches ; dans les pages + du Promi et du Chiche, le texte « TRACE POUR PLANTER » (Promi) et celui qui contient « LANCER » (Chiche) descendent de 6 à 9 pt (1 à 1,5 mm) pour s'aligner sur la flèche, et se décalent de 3 pt (0,5 mm) vers la droite pour ne pas coller à la flèche."),
 ('C-158','18 oct. · v150 §4',"« La phrase des pages + du Chiche et du Cercle » : page + du Chiche, seule la phrase (de « À qui ose… » à « … avec qui en est ? ») remonte de 10 pt (1,7 mm) ; le choix du trait et « Garder de côté » ne bougent pas ; page + du Cercle, sa phrase prend EXACTEMENT la même hauteur et le même placement que celle du Chiche après ce déplacement."),
]
lignes=S.split('\n'); i=max(k for k,l in enumerate(lignes) if l.startswith('| C-156 |'))
for j,(n,d,t) in enumerate(neuf):
    assert not any(l.startswith('| %s |'%n) for l in lignes)
    lignes.insert(i+1+j, '| %s | %s | %s | EN COURS | — | — | v150 |'%(n,d,t))
io.open(p,'w',encoding='utf-8').write('\n'.join(lignes)); print('ok')
