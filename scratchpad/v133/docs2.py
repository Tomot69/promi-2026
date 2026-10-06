import io
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
C=lit('CLAUDE.md'); a="### ⚑ v132 (5 oct. 2026) — LE DESSIN EST CONSTRUIT DANS L'APP."; assert C.count(a)==1
B='''### ⚑ v133 (6 oct. 2026) — LES DIX-HUIT PHRASES DES MURS ; LE BLEU PROVISOIRE ; LE MODE DESSIN RÉGLÉ ; LE MENU DES PALETTES. (Décisions Tom.) Ce bloc CORRIGE les blocs v131 et v132 qui le suivent.
> **⚑ LES PHRASES DES MURS DE MA PAROLE ! SONT DIX-HUIT, RÉÉCRITES PAR TOM (C-063)** — mot pour mot, dans l'ordre, même rotation (v104). Elles
> vivent dans `lot-V104-MURS` (`TEXTES` : la phrase, puis SES mots en orange, cherchés dans l'ordre). **Dans chaque phrase, seuls les mots
> listés prennent l'orange de Ma Parole ! ; « ! » n'apparaît que dans « Ma Parole ! ».** `redteam_murs` (28) et `redteam_maparole` (14) portent
> le texte et les mots EN DUR. Les 21 phrases d'avant : `MA-PAROLE-PHRASES.md` (histoire).
> **⚑ LE CORPS SOMBRE D'UN PROMI EST PROVISOIREMENT `#1A52F0`** (C-050 : « sur son iPhone, #273CEB tire nettement au violet »). **`?bleu=1…5`**
> (`lot-V133-BLEU`) le pose en direct : 1 `#1560E8` · 2 `#1A52F0` · 3 `#2046F2` · 4 `#273CEB` · 5 `#0A5CF5` ; la valeur s'écrit au bas de
> l'écran ; Tom choisit, puis on fige et on RETIRE le paramètre. « Ma Parole ! » sur ce corps (3:1) et la phrase lilas de la page + (4,5:1)
> en sont DÉRIVÉES par `_teinte.ajuste` (au défaut : `#FF9F84`, `#E8DAFF`). Le mur lit le bleu par `window._bleuPromi()`.
> **⚑ LE MODE DESSIN (C-042, C-056, C-061)** — ① **un ✕ dans le contour de l'encart, à l'emplacement de « ✕ FERMER », sort sans poser** ; le
> dessin en cours est gardé ; « Quitter le dessin » ; c'est le seul nœud admis sur la surface. ② `ECART_DEPLOI` **16** ; **la rangée est
> centrée dans sa zone basse** : `MARGE_HAUT` 12 = `MARGE_BAS` 12, comptés jusqu'au bord bas utile (`SECU_BAS` 34) — la surface fait
> **390 × 742**. ③ **Les couleurs du dessin sont dans Ma Parole !** : sans elle, l'encre du mode sur le champ de la nature ; le panneau COULEUR
> est un MUR (`.dz-mur`, flou 4,8 px, rien ne s'y choisit, la phrase monte dessus, devant le mode — `#murPhrase.sur-dessin`) ; l'offre qui
> s'ouvre fait sortir du mode (dessin gardé). `redteam_dessin` 79, huit sondes.
> **⚑ LE MENU DES PALETTES DU STUDIO (C-057) — la cause** : `#studioScreen` ne perd jamais `.show` (§8) ; à chaque ouverture `buildStudio`
> rebâtit la rangée, le NOM (`#st3pn`) et la jauge, et `posePals` ne retirait du panneau que l'ancienne rangée et l'ancienne jauge : deux
> noms, et la rangée neuve rangée APRÈS le vieux. Il retire maintenant les trois et les repose dans l'ordre grille · nom · jauge.
> **Primesautier est la première pastille** (l'ordre des autres inchangé). Juge : **`redteam_palettes.py`** (deux thèmes, deux ouvertures,
> les 24 pastilles touchées une à une ; 22/28 sur l'état d'avant).
> **« Importer une image » devient « Importer une photo »** (C-060 ; le symbole du bouton attend le choix de Tom, `planche-v133/symboles`).
> ⚠ **OUVERTS** : la Toile sourde au doigt sous certains mondes n'est PAS reproduite (C-058, `redteam_toucher` 21/21, Q396) ; « le bas des
> fiches en clair » n'a rien changé — les trois corps sont déjà identiques en clair, aucun filet n'y est peint (C-059, Q397) ; la
> diversité des tailles : le coefficient de variation ne baisse pas avec le nombre de dalles (C-062, Q402).

'''
ecrit('CLAUDE.md',C.replace(a,B+a))
C=lit('CLAUDE.md')
a="python3 redteam_dessin.py      # 63 — v132 (C-042)"; assert C.count(a)==1
C=C.replace(a,'''python3 redteam_palettes.py    # 28 — v133 (C-057) : le menu des palettes du Studio, deux thèmes, deux ouvertures, les 24 pastilles touchées une à une ;
                               #   l'ordre en dur, Primesautier en tête. Rougit sur l'état d'avant (22/28).
python3 redteam_toucher.py     # 21 — v133 (C-058) : vingt mondes, trois dalles touchées au vrai doigt : la fiche de la bonne parole s'ouvre.
                               #   ⚠ VERT sur l'état d'avant : le défaut de Tom n'est pas reproduit.
python3 redteam_dessin.py      # 79 (v133 : ✕ de sortie, 16 pt, rangée centrée, mur des couleurs ; sondes quitter, centre, mur) — v132 (C-042)''')
ecrit('CLAUDE.md',C)
D=lit('DESSIN-INVENTAIRE.md').rstrip('\n')+'''

## v133 (6 oct. 2026) — réglages de Tom
- **Sortie sans poser** : `button.dz-quitter`, un ✕ de 18 dans une cible de 44, dans le contour de l'encart, calé sur le bord droit de
  « ✕ FERMER » ; « Quitter le dessin » ; le dessin en cours est gardé.
- **Mise en page** : `ECART_DEPLOI` 16 ; `SECU_BAS` 34, `MARGE_BAS` 12 = `MARGE_HAUT` 12 — la rangée est centrée entre le bas de la surface
  (742) et le bord bas utile (810) ; surface 390 × 742.
- **Ma Parole !** : sans elle, l'encre du mode sur le champ de la nature ; le panneau COULEUR est un mur (flou 4,8 px, phrase des murs).
- **Menu** : « Importer une photo ».
'''
ecrit('DESSIN-INVENTAIRE.md',D)
MEM='/Users/macbookpro/.claude/projects/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/memory/'
ecrit(MEM+'point-de-reprise-6-oct-v133.md','''---
name: point-de-reprise-6-oct-v133
description: État à la fin du lot v133 (6 oct. 2026) — ce qui est fait, ce qui attend Tom, ce qui est ouvert
metadata:
  type: project
---

Lot v133 (6 oct. 2026). Fait : les 18 phrases des murs (C-063), bleu provisoire #1A52F0 + `?bleu=1…5` (C-050, à figer puis retirer),
mode dessin (✕ de sortie, 16 pt, rangée centrée, couleurs dans Ma Parole !), menu des palettes du Studio à la 2e ouverture (C-057),
« Importer une photo ».

Ouverts, à reprendre en v134 : C-058 (Toile sourde au doigt : NON reproduit, il faut le chemin de Tom) ; C-059 (bas des fiches en clair :
rien à changer d'après la mesure, capture attendue) ; C-060 (Tom choisit A, B ou C sur `planche-v133/symboles`) ; C-062 (tailles : le CV
ne baisse pas ; prototype hors app) ; C-021 (dossier de portage, repoussé à v134).

**How to apply:** les captures jointes par Tom à ses messages n'arrivent pas toujours — le dire dès le début du lot. Voir [[registre-chantiers]].
''')
I=lit(MEM+'MEMORY.md').rstrip('\n')+'\n- [Point de reprise — 6 oct. (v133)](point-de-reprise-6-oct-v133.md) — 18 phrases des murs, bleu provisoire + ?bleu=, mode dessin réglé, palettes du Studio ; ouverts C-058, C-059, C-060, C-062\n'
ecrit(MEM+'MEMORY.md',I)
