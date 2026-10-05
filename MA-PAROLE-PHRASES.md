# MA-PAROLE-PHRASES.md — les phrases des murs de Ma Parole !

Extrait de l'app le 5 octobre 2026 (commit `94925d6`, v132), **mot pour mot** : chaque phrase est relevée deux fois — dans la source
(`lot-V104-MURS`, `window._murPhrases`) et à l'écran, montée au doigt sur un mur — et les deux relevés sont identiques. Rien n'a été
modifié dans l'app.

## Ce qu'il faut savoir avant de lire la liste

- **Il n'y a qu'UNE liste, de 21 phrases, pour tous les murs.** Aucun mur n'a ses phrases à lui, aucune phrase n'a de variante par écran,
  par thème ou par nature : la même phrase paraît quel que soit le mur touché.
- **Laquelle paraît dépend d'un compteur GLOBAL** (toutes zones confondues, gardé par personne) : le 1er mur touché montre la phrase 1,
  le 2e la phrase 2… jusqu'à la 21 ; ensuite une phrase au hasard parmi les 21, jamais la même deux fois de suite. Après 14 jours sans
  toucher un mur, le compteur repart à la phrase 1.
- **Les espaces avant « ! » et « ? » sont des espaces insécables** (elles le sont dans ce fichier aussi) ; les
  apostrophes sont typographiques (’) ; la phrase 4 finit par le caractère « … ».
- **Un mot porte l'orange de Ma Parole !** dans neuf phrases : « Ma Parole ! » lui-même (phrases 1, 2, 3, 6, 15) ou un seul mot
  (phrases 5, 7, 9, 17). Les douze autres sont d'une seule couleur.
- Abonné à Ma Parole ! : aucun mur, aucune phrase.

## Les écrans où elles apparaissent (les six murs)

| Mur | Écran | Ce qui est flouté et qu'on touche |
|---|---|---|
| A | Peaufiner d'une fiche | le bloc des réglages de Ma Parole ! (récurrence, rappel, « c'est important ? », la mémoire, la couleur) |
| B | Peaufiner de la page + | le même bloc, à la création |
| C | L'Aura | la rangée « Ce qu'on t'a tenu » |
| D | L'aide de l'Aura | les rubriques verrouillées |
| E | Les notifications | la mémoire des paroles en l'air et le choix de l'heure |
| F | Le Studio, sur un monde ou une palette verrouillés | les teintes, la vue, les points et le nom du panneau des palettes |

Chaque phrase ci-dessous peut donc paraître sur **A, B, C, D, E et F**.

⚠ L'affichage à l'écran a été relevé sur le mur A (les 21 phrases, une à une). Les murs B à F sont lus dans le code (la liste des
murs du lot) : ils appellent la même liste, mais leur contenu flouté est décrit d'après leurs sélecteurs, pas d'après une capture.

## Les 21 phrases

| N° | La phrase | Le mot en orange | Écrans |
|---|---|---|---|
| 1 | Eh non ! Mais avec Ma Parole !, oui. | Ma Parole ! | A · B · C · D · E · F |
| 2 | Toujours pas. Avec Ma Parole !, si. | Ma Parole ! | A · B · C · D · E · F |
| 3 | Je vois bien que ça te titille. Ma Parole ! lève tout ça. | Ma Parole ! | A · B · C · D · E · F |
| 4 | Tiens tiens, on dirait que ça commence à t’intéresser… | — | A · B · C · D · E · F |
| 5 | Tu connais déjà la solution, me semble-t-il. | solution | A · B · C · D · E · F |
| 6 | Tu sais où trouver Ma Parole ! maintenant. | Ma Parole ! | A · B · C · D · E · F |
| 7 | Je commence à connaître tes habitudes. | habitudes | A · B · C · D · E · F |
| 8 | Je crois qu’on commence à bien se connaître. | — | A · B · C · D · E · F |
| 9 | C’est sûr de sûr que tu ne veux pas essayer ? | essayer | A · B · C · D · E · F |
| 10 | Allons bon. Nous y voilà à nouveau. | — | A · B · C · D · E · F |
| 11 | Entre nous, tu sais très bien ce qu’il faudrait faire. | — | A · B · C · D · E · F |
| 12 | À ce stade, autant arrêter de négocier, non ? | — | A · B · C · D · E · F |
| 13 | Tu peux continuer. Je ne dirai rien. | — | A · B · C · D · E · F |
| 14 | Tu sais, je ne vais pas te juger. | — | A · B · C · D · E · F |
| 15 | Ma Parole ! aussi, ça peut durer longtemps. | Ma Parole ! | A · B · C · D · E · F |
| 16 | Je crois que tu essaies de me faire changer d’avis. | — | A · B · C · D · E · F |
| 17 | On pourrait presque appeler ça une tradition. | tradition | A · B · C · D · E · F |
| 18 | Tu commencerais presque à connaître le chemin. | — | A · B · C · D · E · F |
| 19 | On commence à avoir nos petites habitudes. | — | A · B · C · D · E · F |
| 20 | Je vais finir par croire que tu viens juste me voir. | — | A · B · C · D · E · F |
| 21 | On se dit directement à la prochaine ? | — | A · B · C · D · E · F |

## Ce qui n'est PAS une phrase de mur (pour mémoire, non modifié)

- Le bouton du Studio sur un monde verrouillé : « Adopte ce design — 2 € » (figé ; la source garde deux autres libellés que l'app
  n'affiche plus : « Nouvelle trame ? — 2 € », « Débloque-le — 2 € »).
- Les mots de la page de l'offre (« Avec Ma Parole ! », « Tu es Membre Ma Parole ! », « Retourne ta Toile », « Bon, allez d'accord ») et
  la porte des Réglages (« Ma Parole ! ») : ce ne sont pas des murs.
