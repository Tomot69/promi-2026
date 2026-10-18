import io, re
p='CHANTIERS.md'; S=io.open(p,encoding='utf-8').read()
def etat(c, nouvel, ajout):
    global S
    L=[l for l in S.split('\n') if l.startswith('| %s |'%c)]
    assert len(L)==1, c
    cols=L[0].split('|')
    cols[4]=' %s '%nouvel
    cols[5]=' '+ajout+' '+cols[5].strip()+' '
    S=S.replace(L[0], '|'.join(cols))
for c in ('C-141','C-143','C-144','C-146','C-147','C-148'):
    etat(c, 'VALIDÉ PAR TOM', '**v149 (17 oct.) : validé par Tom sur iPhone (« le reste a l\'air ok »).**')
etat('C-139','VALIDÉ PAR TOM','**v149 : clos SANS invitation animée — Tom n\'en a choisi aucune ; le chevron orange du départ suffit.**')
for c in ('C-124','C-145','C-149'):
    etat(c, 'EN COURS', '**v149 : rouvert par Tom (retours iPhone sur v148).**')
for c in ('C-150','C-151','C-152'):
    etat(c, 'EN COURS', '**v149 : à corriger ou juge remis au niveau (décision de Tom en fin de v148).**')
neuf = [
 ('C-153','17 oct. · v149 §1',"« Le I de PROMI clignote aussi dans l'onboarding » : dès la page « Toi, c'est … ? », puis sur TOUTES les pages de l'onboarding, le PROMI en PromiLate en haut à gauche a son I qui clignote, exactement comme sur l'accueil : même bleu, même rythme, même code."),
 ('C-154','17 oct. · v149 §5',"« La vague de création : la couleur de l'état » : la vague sous le trait quand on lance une parole depuis la page + prend la couleur de l'état dans lequel entre la parole (« à tenir » ou « en cours ») ; l'amande est réservée à la célébration ; elle ne saccade pas."),
 ('C-155','17 oct. · v149 §6',"« La saccade après le lever du doigt » : à la création comme à la validation ; si le trait est complet au lever, l'animation part dans l'image suivante, sans attente de confirmation ; le travail lourd (enregistrement, Toile, Fil) après le départ de l'animation."),
 ('C-156','17 oct. · v149 §7',"« La validation : un seul mouvement, et le cas à plusieurs » : tenue d'un coup → le rideau part directement du trait, sans vague intermédiaire ; ma part sans être la dernière → seulement la vague sous le trait, en amande, pas de rideau, la fiche reste en cours ; tout le monde a tracé → une entrée dans le Fil de chacun ; première ouverture de chaque participant après ce moment → le rideau descend sous ses yeux, ensuite directement tenue ; « déjà vu » par personne et par parole (portage, modèle de données)."),
]
for n,d,t in neuf:
    assert '| %s |'%n not in S
    S=S.replace('\n| C-152 |', '\n| C-152 |',1)
lignes=S.split('\n'); i=max(k for k,l in enumerate(lignes) if l.startswith('| C-152 |'))
for j,(n,d,t) in enumerate(neuf):
    lignes.insert(i+1+j, '| %s | %s | %s | EN COURS | — | — | v149 |'%(n,d,t))
io.open(p,'w',encoding='utf-8').write('\n'.join(lignes))
