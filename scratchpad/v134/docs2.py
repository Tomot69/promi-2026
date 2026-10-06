import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
ecrit('portage/README.md','''# portage/ — le dossier de portage de Promi (C-021, lot v134, 6 octobre 2026)

L'app Swift sera reconstruite à partir de zéro, **à partir de ce dossier seul**, sans relire `app.html`. Tout ici est **lu et extrait** du
prototype (`app.html`, `promi-moteur.js`), de ses juges et de ses documents de décision ; **rien n'a été modifié dans le produit**.
Rien n'y est inventé : ce qui manque est écrit « ⚠ TROU », avec ce qui a été cherché. Chaque affirmation porte sa source.

**Comment c'est fait, et sa limite.** Les dix documents ont été extraits par lecture de la source (recherches ciblées, extraction par
programme pour les tables) ; **aucun n'a été vérifié à l'écran**, et aucun juge n'a été relancé pour eux. Les numéros de ligne cités sont
ceux de la copie de travail du 6 octobre 2026 (v134) : ils servent à retrouver, pas à porter. En cas de désaccord, l'ordre des sources du
projet reste : `ETAT-30-SEPTEMBRE-2026.md` → `PROMI-TOKENS.json` → `CONTRAT-MONDE.md` → `SPEC-JUGES.md` → `CLAUDE.md` (les blocs datés
les plus récents corrigent les plus anciens).

## Table des matières

| n° | Document | Ce qu'il contient |
|---|---|---|
| 1 | `SPEC-DONNEES.md` · `SPEC-DONNEES.schema.json` | Chaque entité (Promi, Chiche, Cercle, personne, gardé de côté, dessin, photo, réglages, achats) : champs, états, transitions et leur déclencheur ; JSON Schema (27 définitions, `x-transitions`) ; ce qui ATTEND FIREBASE (§12), dont le dessin commun et le masquage individuel |
| 2 | `SPEC-ECRANS.md` | Vingt-six écrans : accès, éléments, actions, états vides et d'erreur, textes exacts |
| 3 | `SPEC-GESTE.md` | Planter, tenir, tracer sa moitié, dessiner, et les gestes de navigation : géométrie, seuils, horodatages ; ce qui doit être lu avec `UITouch.timestamp` et `coalescedTouches` (§7) |
| 4 | `SPEC-RENDU.md` | L'interdiction (jamais de capture de Toile à la place d'une dalle), la Toile, les vingt mondes (renvoi à `CONTRAT-MONDE.md`), la Pelote, la vie au repos (quatre mondes reportés à Swift), les paliers qu'on peut dégrader (principe, sans chiffre), le banc de rendu |
| 5 | `JETONS.json` · `JETONS.md` | Couleurs, typographie, espacements, rayons, palettes, seuils ; les 85 décisions de couleur de Tom (tableau de `redteam_decisions`) ; dix-huit exceptions nommées |
| 6 | `TEXTES.json` · `TEXTES.md` | 330 clés, 967 chaînes, variantes, gabarits, VoiceOver ; les dix-huit phrases des murs et leurs mots en orange ; 38 clés « à confirmer » |
| 7 | `REGLES.md` | Cent règles vérifiables (R-001 à R-100) : la grille anti-coercition (reconstituée), les lois du dessin (dont la loi des points et son exception), le lexique |
| 8 | `TESTS.md` | Les 89 juges traduits en critères d'acceptation pour Swift : ce qu'il vérifie, sur quoi, avec quel seuil ; onze ne se portent pas |
| 9 | `DETTE.md` | Code mort, dettes nommées, faux positifs, rouges permanents, incohérences assumées, jetons sans consommateur, chantiers et questions ouverts — une ligne chacun, avec ce qu'il faut décider |
| 10 | `MANQUES.md` | Ce qu'aucune décision ne couvre : notifications, vibrations, Firebase, StoreKit, VoiceOver de la Toile, pages légales, version, polices, page du trait partagé, Zzz, tailles d'écran, Dynamic Type, langue, compte, archive |

`A-INTEGRER.md` (les notes prises de v126 à v133) est intégré dans les documents 1 à 5 ; il reste là comme journal.

## Les contradictions trouvées en écrivant le dossier (à trancher avant de coder)

- **La rotation de la Pelote** : `2π/100` dans l'app et dans `releve-aura.py` ; `2π/120` dans `CLAUDE.md` §7 (Q405).
- **Le prix d'un design** : 2 € au Studio (v118) ; « 1 €, ou 4 pour 3 € » encore sur l'écran de l'offre et dans l'ÉTAT.
- **`ETAT-30-SEPTEMBRE-2026.md` est en retard** sur le bleu (`#0E78F2`) et sur ce prix : c'est pourtant la première source de l'ordre.
- **Le fond sombre** : `#100D0B` dans le jeu de jetons et dans `Promi+Design.swift` ; seiche `#050302` à l'écran (v116, v121).
- **Le trait sur le lilas d'un Cercle** : `#43291C` dans le code, `#291547` à deux endroits de `CLAUDE.md`.
- **« Tenu » sur fond sombre** : amande `#8FE08F` (`CLAUDE.md`, 23 sept.) ; deux juges portent encore `#33BA6C`.
- **L'aide de l'Aura** dit « dans l'ordre où tu les as tenues » ; depuis v132 la plus récente est en premier.
- **À propos** dit « Les titres sont en Gilbert » ; ils sont en PromiLate, qui n'est pas créditée.
- **`SPEC-JUGES.md`** écrit « 21 phrases » ; elles sont dix-huit.
- **« Quatre mondes neufs »** dans `CLAUDE.md` ; `_NEUFS` en compte douze.
- **La grille anti-coercition** est citée (« la grille l'interdit ») mais n'est écrite nulle part comme une liste.
''')
A=lit('portage/A-INTEGRER.md')
if 'INTÉGRÉ' not in A[:300]: ecrit('portage/A-INTEGRER.md','> **⚑ v134 (6 oct. 2026) — INTÉGRÉ** dans `SPEC-DONNEES`, `SPEC-ECRANS`, `SPEC-GESTE`, `SPEC-RENDU` et `JETONS`. Ce fichier reste comme journal ; le corps sombre d\'un Promi y est encore « provisoire » : il est `#0E78F2`, définitif.\n\n'+A)
C=lit('CHANTIERS.md'); L=C.split('\n')
MAJ={'C-050':('FAIT, EN ATTENTE DE TOM','v134 : `#0E78F2`, définitif (« choisi en connaissance de cause »), jetons JSON = CSS = Swift, `?bleu=` retiré ; texte crème 3,70:1 (exception nommée) ; « Ma Parole ! » `#FED0C3` (3,01:1) ; phrase lilas `#F4EEFF` (3,71:1 — 4,5:1 hors d’atteinte, le blanc fait 4,21:1 : Q403) ; à tenir `#DD4D23` sur ce corps : ΔE 126,2 · Δlum 1,7 (Q404).','redteam_decisions 85/85 · redteam_couleurs_ref · redteam_tokens 46/46','—'),
     'C-021':('FAIT, EN ATTENTE DE TOM','v134 : `portage/` — dix documents (README + SPEC-DONNEES, SPEC-ECRANS, SPEC-GESTE, SPEC-RENDU, JETONS, TEXTES, REGLES, TESTS, DETTE, MANQUES), 4 900 lignes de Markdown et trois JSON ; extraits de la source, NON vérifiés à l’écran ; trous et contradictions listés dans chaque document et au README.','—','—')}
for i,l in enumerate(L):
    m=re.match(r'\| (C-\d+) \|',l)
    if m and m.group(1) in MAJ:
        c=l.split(' | '); assert len(c)==7
        e,p,j,v=MAJ[m.group(1)]; c[3]=e; c[4]=p; c[5]=j; c[6]=v+' |'; L[i]=' | '.join(c)
ecrit('CHANTIERS.md','\n'.join(L))
Q=lit('QUESTIONS.md').rstrip('\n')+'''
- **Q405 — OUVERTE (portage)** : la rotation lente de la Pelote est `2π/100` (un tour en 100 s) dans l'app et dans `releve-aura.py`, `2π/120` dans
  `CLAUDE.md` §7. Laquelle fait foi pour Swift ? Les autres contradictions trouvées en écrivant le dossier : `portage/README.md`.
'''
ecrit('QUESTIONS.md',Q)
MEM='/Users/macbookpro/.claude/projects/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/memory/'
ecrit(MEM+'point-de-reprise-6-oct-v134.md','''---
name: point-de-reprise-6-oct-v134
description: État à la fin du lot v134 (6 oct. 2026) — bleu définitif et dossier de portage
metadata:
  type: project
---

Lot v134 (6 oct. 2026). Le corps sombre d'un Promi est `#0E78F2`, définitif (texte crème 3,70:1, exception nommée) ; « Ma Parole ! » `#FED0C3`,
phrase lilas `#F4EEFF` (Q403 : 4,5:1 hors d'atteinte sur ce bleu). `?bleu=` retiré. Le dossier `portage/` est écrit (dix documents + README),
extrait de la source par six agents en parallèle, non vérifié à l'écran.

En attente de Tom, ne rien toucher : C-057 (capture du Studio), C-058 (contexte de la Toile sourde), C-059 (capture du bas des fiches en clair),
C-060 (symbole A, B ou C), C-062 (tailles). Contradictions à trancher : `portage/README.md`, Q405.

**How to apply:** `window._teinte.ajuste` ASSOMBRIT quand le fond dépasse 0,18 de luminance — pour « éclaircir jusqu'au seuil », calculer hors de
l'app (`scratchpad/v134/bleu.py`). Voir [[registre-chantiers]], [[point-de-reprise-6-oct-v133]].
''')
I=lit(MEM+'MEMORY.md').rstrip('\n')+'\n- [Point de reprise — 6 oct. (v134)](point-de-reprise-6-oct-v134.md) — bleu définitif #0E78F2 (Q403 lilas), dossier portage/ écrit ; en attente de Tom : C-057 à C-060, C-062\n'
ecrit(MEM+'MEMORY.md',I)
