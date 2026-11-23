# Défiler : la jonction (lot 3a-3) — à vérifier sur l'iPhone, dans l'app « Promi »

Pour chaque point : **tenu**, **non tenu** ou **non vu** (R4). ⚠ Une fiche ne défile que si sa parole porte des mots (comme le prototype), et la vraie app ne
sait pas encore en écrire (« Un mot… » et l'envoi : lot 3b, le suivant) ; ni ton état ni l'état embarqué n'en portent. **Ces points se vérifient donc avec le
3b** ; d'ici là ils sont jugés au banc seulement (`jonction.spec.ts`, au pixel contre le prototype).

1. **Défiler lentement vers le haut** : la vague monte jusqu'au bas du plateau, s'y couche à plat ; le trait plat se découvre sous elle, contigu, sans saut.
2. **Défiler d'un coup (l'élan), jusqu'au rebond du bas, puis revenir en haut d'un coup** : le trait reste accroché à plat sous le plateau, jamais au-dessus ni
   dessous ; revenue en haut, la fiche est exactement celle d'avant.
3. **Lâcher le défilement à mi-chemin** (la vague à demi sous le plateau) : la fiche glisse vers la place sûre la plus proche.
4. **Accrochée, poser le doigt sur le trait plat et glisser** : la fiche défile, rien ne se trace.
5. **« Les Mots »** : le titre se trace la première fois ; la liste (visage, nom, date, texte) du plus récent au plus ancien.
6. **Tenir sur une fiche à mots un peu défilée** : « Parole tenue ! » à la même place que sur une fiche sans mot ; défiler pendant que le vert est posé : il
   passe sous le plateau, jamais au-dessus.
7. **Le bouton photo** passe au-dessus du plateau quand la fiche défile (comme le prototype).
