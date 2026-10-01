# Audit — la réciprocité sur l'Aura (chantier 79, 14 sept. 2026)

> Tom : « Un abonné ne gagne rien sur l'Aura, alors que « L'autre moitié de ta Toile » est le premier argument de l'écran
> qui vend. On vend quelque chose qui n'existe pas. » Audit d'abord, planches ensuite, rien d'intégré.

## 1. Ce qu'on vend

Écran qui vend (`app.html` ≈ l. 29997), premier argument : **« L'autre moitié de ta Toile — ce que tes proches tiennent
envers toi »**, sous le titre « ta parole, et celle qu'on te tient ».

## 2. Ce que l'Aura montre aujourd'hui (gratuit = payant, mesuré)

La sphère (tes dalles), la phrase, les Noyaux (toi + chaque personne à qui TU promets, arcs tenues / en cours / à tenir),
« Ce que tu as tenu », Partager. **Tout est dans un seul sens : ta parole.** Rien ne change avec le Cercle.

## 3. Ce que la spécification a déjà dessiné

- **§2.9 Les Noyaux** : « Le Cercle ajoute un **second anneau** à +9 px, épaisseur 0,7 × ». C'est l'élément de la
  réciprocité, déjà écrit : il n'est ni tranché dans sa lecture, ni construit. (Proposition non tranchée dans
  `ETAT-DES-LIEUX` : « les anneaux des personnes ne se doublent pas ».)
- Mêmes règles que l'anneau d'aujourd'hui : piste neutre, arcs = les trois états, aucun chiffre, aucun mot d'état.

## 4. Les données dont on dispose

Un Promi porte `who` (à qui), `from` (de qui), `nuee`, `chiche` / `chicheEtat` / `avec`, `req` (une demande), `status`.

| Source de « ce qu'on te tient » | Champ | Dans le jeu de démonstration |
|---|---|---|
| Un proche te promet, à toi | `from = X`, `who = moi` | **aucun** |
| Un Chiche tenu à deux (l'autre a tenu sa moitié) | `chiche`, `chicheEtat = releve`, `avec` | « le grand plongeoir » (Marion, tenu) · « courir dimanche » (lancé, pas relevé) |
| Un proche promet à une Nuée dont tu es membre | `from = X`, `nuee`, `NUEEMEM` | 4 : Rachel « reprendre l'arrosage » (à tenir) · Adrien « récupérer les plants » (tenu), « semer les radis » (à tenir) · Marion « vider le composteur » (Chiche relevé, en cours) |
| Une demande que tu as faite (« promets-moi ») | `req` | aucune |
| Le Fil | `FEED` (`received`, `kept`) | 5 événements, dont « Marion a relevé » |

**Donc on peut calculer, sans rien inventer**, pour chaque personne : ses paroles envers toi (à toi, à deux, à ta Nuée),
réparties en tenues / en cours / à tenir — exactement la matière d'un second anneau.

## 5. Ce que ça suppose côté produit — à trancher

1. **Qui compte comme « envers toi »** : seulement ce qu'on te promet à toi ? ou aussi la moitié tenue d'un Chiche, et
   ce qu'on promet à une Nuée dont tu es ?  *(Recommandation : les trois — sinon le jeu est vide, et un vrai utilisateur
   aussi pendant longtemps.)*
2. **Qui déclare qu'une parole envers toi est tenue** : celui qui la tient (son geste) — l'app ne peut que le recevoir.
   Dans le prototype il n'y a pas de serveur : la donnée est locale, simulée par le jeu.
3. **Les personnes de la rangée** : aujourd'hui, celles à qui TU promets. Une personne qui ne te promet rien en retour
   a un second anneau vide ; une personne qui te promet sans que tu lui promettes n'apparaît pas. Faut-il l'ajouter ?
4. **Ton Noyau** : son second anneau = tout ce qu'on te tient, toutes personnes confondues.
5. **La sphère** : « l'autre moitié de ta Toile » peut aussi se lire littéralement — la face cachée de la sphère porterait
   les dalles de ce qu'on te tient. Plus fort, mais c'est du moteur de la Pelote : à part, si on le veut.
6. **Le gratuit** voit-il le second anneau voilé (comme les réglages du Cercle), ou rien ?

## 6. Planche

`planche-79/PLANCHE-79.html` — la rangée des Noyaux dans les deux thèmes : aujourd'hui · A (second anneau du §2.9, lu
avec les données du jeu) · B (A + « Ce qu'on t'a tenu » sous « Ce que tu as tenu »). Les chiffres sortent du jeu.
