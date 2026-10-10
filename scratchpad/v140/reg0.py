import io
S=io.open('CHANTIERS.md',encoding='utf-8').read()
assert 'C-091' not in S
L=[
"| C-091 | 10 oct. · v140 §4 | « Un seul bouton Enregistrer, partout » : une icône seule, sans texte, discrète, la même partout où l'on peut enregistrer — photo en plein écran, dessin en plein écran, la Toile (pour enregistrer son image), et partout ailleurs où c'est possible. Elle remplace le texte « Enregistrer la photo ». VoiceOver : « Enregistrer ». Même grammaire que les icônes de fiche. Lister dans le rapport tous les endroits où elle apparaît. | OUVERT | v140 : inscrit. | — | v140 |",
"| C-092 | 10 oct. · v140 §7 | « Le Studio : la phrase du mur au mauvais endroit » : quand on touche une zone floutée du Studio (le choix des palettes, avec son texte), la phrase de Ma Parole ! apparaît en haut de l'écran au lieu d'apparaître sur la zone floutée, en bas. Elle doit paraître sur le flou touché, lisible. Vérifier tous les murs du Studio. | OUVERT | v140 : inscrit. | — | v140 |",
"| C-093 | 10 oct. · v140 §0 | « Le dessin est collaboratif entre les personnes d'un Promi, d'un Chiche ou d'un Cercle » : l'écrire dans portage/SPEC-DONNEES et SPEC-ECRANS (traits de chacun, ordre, synchronisation, signalement), à construire avec Firebase. | OUVERT | v140 : inscrit. | — | portage (Firebase) |",
]
S=S.rstrip('\n')+'\n'+'\n'.join(L)+'\n'
io.open('CHANTIERS.md','w',encoding='utf-8').write(S)
