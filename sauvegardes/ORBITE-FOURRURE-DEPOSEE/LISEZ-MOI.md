# ⚑ L'ORBITE-FOURRURE — DÉPOSÉE, 9 septembre 2026

**Ce n'est pas un abandon : c'est un dépôt.** Décision de Tom — on explore trois autres
pistes, et si aucune ne convainc, **on revient ici**. Ne pas supprimer.

## Comment y revenir
```bash
cp sauvegardes/ORBITE-FOURRURE-DEPOSEE/_o_*.js scratchpad/
cp sauvegardes/ORBITE-FOURRURE-DEPOSEE/PLANCHE-FOURRURE.html .
python3 scratchpad/bust.py PLANCHE-FOURRURE.html
```

## Ce qu'elle vaut, mesuré
```
luminance moyenne      147,7      (cible 90-110 : au-dessus)
dispersion basse freq.  15,2 %    (etait 43,9 % avant le correctif du versement)
cout                   10 a 25 ms selon le cadre
```

## Ce qu'elle a apporté, et qui vaut pour TOUTE suite
1. **`verse()` doit garder LE PLUS OPAQUE, jamais « le dernier posé ».** L'alpha d'un brin est
   fort à la racine et faible à la pointe ; avec un peignage directionnel, une moitié de
   l'objet sortait à 49 de luminance et l'autre à 83, à couverture et éclairage égaux.
   Un seul test (`if(v>B[o])`) : dispersion 44 % → 15 %, luminance 82 → 148.
2. **Un écart-type pixel par pixel sur une matière granuleuse mesure LE GRAIN**, pas
   l'uniformité. Réduire l'image à 40×40 avant de mesurer.
3. **On pilote la luminance PERÇUE, jamais la clarté HSL.** Le bleu ne pèse que 11 % : une
   clarté 0,46 sur un bleu-violet donne une luminance perçue de 54.
4. **Un bleu-violet ne peut pas être à la fois clair et saturé.** Mur de colorimétrie.
5. **Une dalle est figée à sa plantation** — `Toile.dalleGeneree` la peint dans son monde.
6. Trois pièges de repère payés trois fois : **une direction « face à nous » s'écrit dans le
   repère de la VUE, jamais de l'objet.**
