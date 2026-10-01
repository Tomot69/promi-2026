# ⚑ LA RÉFÉRENCE DE L'ORBITE — validée par Tom, 9 septembre 2026

> *« enfin c'est correct merci. on garde ceci comme référence désormais. »*

**Ne pas repartir d'un autre état.** Tout lot futur part d'ici, et s'il s'en écarte
il doit pouvoir revenir : `cp sauvegardes/ORBITE-REFERENCE/*.js scratchpad/`.

## Ce qui fait cette référence, en une phrase
**Le moteur peint UNE Toile complète, et on l'ENROULE sur la sphère.** On n'assemble
plus rien : plus de dalle fabriquée, choisie, mise à l'échelle ou raccordée.

```
Toile.toilePleine   1054 x 1054, cellules de 72 px — la densite de l'app
projection          Lambert azimutale EQUIVALENTE (conserve les aires),
                    centree sur la direction de la vue (l'antipode passe derriere)
la fourrure         330 000 touffes de 3,1 px — couverture x11, un poil vaut le
                    quart d'un carreau de mosaique, donc il ne le brouille pas
cout                22 ms au cadre 620, 20 ms au cadre 470
```

## Les trois pièges qui ont coûté le plus, et qui sont ici résolus
1. **Assembler au lieu d'enrouler.** Dix lots perdus à améliorer un montage.
2. **Le point de fuite de Lambert sur la face visible** — un tourbillon au milieu.
3. **Le semis dimensionné pour des dalles trouées** alors que la Toile couvre tout :
   531 000 touffes, 67,6 ms.

## Ce qui reste ouvert au moment où on fige
- la boule est plus sombre et moins saturée que la Toile source ;
- la fourrure est un velours ras (le prix du dessin exact) ;
- 22 ms > 16,5 ms de plafond, à re-mesurer à la taille de l'app ;
- `toilePleine` sème avec `Math.random` : non déterministe sur la planche.
