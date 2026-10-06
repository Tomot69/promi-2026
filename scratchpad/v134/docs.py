import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
C=lit('CLAUDE.md'); a="### ⚑ v133 (6 oct. 2026) — LES DIX-HUIT PHRASES DES MURS"; assert C.count(a)==1
B='''### ⚑ v134 (6 oct. 2026) — LE CORPS SOMBRE D'UN PROMI EST `#0E78F2`, DÉFINITIF. (Décision Tom.) Ce bloc CORRIGE ce que les blocs v133, v131 et v130 disent de ce bleu.
> **« Tom a choisi #0E78F2, en connaissance de cause. »** Fiche Promi et page + d'un Promi, en sombre (jetons `--c-cobalt50`, `--p-corps-promi` ;
> JSON = CSS = Swift). **`?bleu=` est RETIRÉ.** `#1A52F0`, `#273CEB`, `#8ACBE8`, `#335382` sont morts pour ce rôle.
> **⚑ EXCEPTION NOMMÉE, décidée par Tom : le texte posé sur ce corps reste crème `#F7F0DE` — 3,70:1. Les petites mentions y sont sous
> 4,5:1, par décision.** Aucun juge ne doit « corriger » ce texte, aucune passe de lisibilité ne doit le repeindre.
> **Les deux dérivés suivent ce bleu, même teinte, éclaircis jusqu'à leur seuil** (méthode du v133, validée) : **« Ma Parole ! » = `#FED0C3`**
> (l'orange `#FB4C0D`, OKLCH h 36°, à 3,01:1 ; il ne garde qu'un quart de sa chroma) ; **la phrase lilas de la page + = `#F4EEFF`**.
> ⚠ **4,5:1 EST HORS D'ATTEINTE sur ce bleu en éclaircissant : le blanc pur n'y fait que 4,21:1.** La phrase lilas est portée au niveau
> de la crème (3,71:1), teinte gardée (h 302°) — Q403, à valider. ⚠ `window._teinte.ajuste` ASSOMBRIT dès que le fond dépasse 0,18 de
> luminance (ce bleu : 0,20) : appelée telle quelle elle rendait `#621600` et `#1C0035`. Les deux valeurs sont donc des jetons, calculées
> hors de l'app (`scratchpad/v134/bleu.py` : OKLCH, clarté montée, chroma réduite quand la couleur sort du gamut).
> **Les états sur ce corps, mesurés, rien retouché** (ΔE CIELAB · Δlum · contraste) : **à tenir `#DD4D23` 126,2 · 1,7 · 1,03:1** — le trait
> orange a la CLARTÉ du corps, c'est sa teinte seule qui le sépare (Q216 : un trait se juge en ΔE, seuil 15) ; en cours `#291547` 56,8 ·
> 77,4 · 3,86:1 ; tenu `#00341A` 97,2 · 67,2 · 3,31:1 ; trait Promi `#022140` 62,4 · 3,85:1 ; bande `#82AEF8` contre corps 36,1 · 1,88:1.
> **Le dossier de portage est écrit : `portage/`** (dix documents, C-021) — lecture et extraction, aucun changement du produit.

'''
ecrit('CLAUDE.md',C.replace(a,B+a))
Q=lit('QUESTIONS.md').rstrip('\n')+'''
- **Q399 — TRANCHÉE (Tom, v134)** : la méthode est validée — l'orange de « Ma Parole ! » et la phrase lilas suivent le bleu, même teinte,
  éclaircies jusqu'à leur seuil. Le bleu est `#0E78F2`, définitif ; le texte y reste crème (3,70:1), exception nommée.
- **Q403 — À VALIDER (C-050)** : sur `#0E78F2`, la phrase lilas de la page + ne peut PAS atteindre 4,5:1 en s'éclaircissant (le blanc pur :
  4,21:1). Posée à `#F4EEFF` (3,71:1, le niveau de la crème, teinte gardée). Autres voies : 4:1 = `#FBF9FF` (presque blanc), ou la crème.
  « Ma Parole ! » à 3:1 = `#FED0C3` : c'est un pêche très pâle (un quart de la chroma de l'orange) — à voir sur l'iPhone.
- **Q404 — À SAVOIR (C-050)** : sur `#0E78F2`, le trait « à tenir » `#DD4D23` n'a aucun écart de clarté avec le corps (Δlum 1,7 ; 1,03:1) ;
  il se lit par la teinte (ΔE 126). Rien n'a été retouché.
'''
ecrit('QUESTIONS.md',Q)
E=lit('ETAT-DES-LIEUX.md')
a=[l for l in E.split('\n') if l.startswith('- **v133 (6 oct.)**')][0]
E=E.replace(a,a+'''
- **v134 (6 oct.)** — le corps sombre d'un Promi est `#0E78F2`, définitif (C-050), `?bleu=` retiré ; « Ma Parole ! » `#FED0C3`, phrase lilas `#F4EEFF` (4,5:1 hors d'atteinte : Q403) ; **le dossier de portage `portage/`** (dix documents, C-021) — aucun changement du produit.''')
E=E.replace("| v133 | **Le bleu du corps sombre Promi (C-050) — à CHOISIR** |","| v133 | ~~Le bleu à choisir~~ *remplacé par la ligne v134 (`#0E78F2`)* |")
E=E.rstrip('\n')+'''
| v134 | Le bleu définitif `#0E78F2` (C-050) | `redteam_decisions` 85/85 · `redteam_couleurs_ref` | fiche Promi et page + en sombre : le texte crème et les petites mentions ; le trait orange « à tenir » sur ce bleu (Q404) ; un mur du Peaufiner (« Ma Parole ! » en `#FED0C3`) ; la phrase lilas de la page + (`#F4EEFF`, Q403) |
'''
ecrit('ETAT-DES-LIEUX.md',E)
