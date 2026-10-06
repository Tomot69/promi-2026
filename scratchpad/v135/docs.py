import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
C=lit('CLAUDE.md')
# rotation
a="(`AUTO_DECIDE = 2π/120`, avec la décision qui la fixe)"; assert C.count(a)==1
C=C.replace(a,"(`AUTO_DECIDE = 2π/100` — un tour en 100 s ; ⚑ v135, Tom : « 100 s, comme dans l'app » ; ce fichier écrivait 2π/120 —, avec la décision qui la fixe)")
# la grille : les énoncés R-001 à R-032 de portage/REGLES.md, mot pour mot
R=lit('portage/REGLES.md'); regles=re.findall(r'^\*\*(R-0(?:0[1-9]|[12]\d|3[0-2])) · (.*?)\*\*\s*$', R, re.M)
assert len(regles)==32, len(regles)
titres={1:'A1 · Ce n\'est pas un gestionnaire de tâches',7:'A2 · Rien ne note, rien ne classe'}
sec=dict((int(m.group(2)[2:]),m.group(1)) for m in re.finditer(r'^### (A\d · .*?)\n+\*\*(R-\d+)', R, re.M))
G='''
---

## 12. La grille anti-coercition (inscrite le 6 oct. 2026, v135 — C-065)

> **⚑ D'OÙ VIENT CE TEXTE.** Tom, 6 oct. 2026 : « La grille anti-coercition n'est écrite nulle part : inscris-la dans CLAUDE.md, mot pour mot
> depuis portage/REGLES (les six critères disqualifiants et les six risques cumulés). » **⚠ Ni « six critères disqualifiants » ni « six
> risques cumulés » n'existent dans `portage/REGLES.md`, ni ailleurs dans le dépôt** (cherché : « disqualifiant », « risques cumulés »,
> « coercition »). Ce qui suit est donc la grille telle que `portage/REGLES.md` §A la porte — **trente-deux règles RECONSTITUÉES** à partir
> des décisions écrites (les huit règles anti-notation de `AUDIT-AURA-CERCLE.md` §C, la « ligne rouge » de `BRIEF-ETUDE-PSYCHO.md`,
> `DECISIONS.md` A1, Q347, Q368, v104, v109), recopiées mot pour mot. Les sources, la façon de vérifier et le juge de chacune sont dans
> `portage/REGLES.md`. **Les six critères et les six risques attendent le texte de Tom (Q406) ; ils remplaceront ou coifferont cette liste.**
> Juge des mots : **`redteam_lexique.py`** (termes bannis, loi des points).
'''
for num,txt in regles:
    k=int(num[2:])
    if k in sec: G+='\n**'+sec[k]+'**\n'
    G+='- **'+num+'** · '+txt+'\n'
G+='''
**Trois tensions connues, qui ne sont pas des règles** (détail dans `portage/REGLES.md`) : « un seul chiffre, pas de pourcentage » face aux
trois chiffres de l'Aura (v95) et à la liste « Ce que tu as tenu » qui s'allonge (v131) ; « Ton meilleur Cercle » face à « aucun
superlatif » ; « REPORTER » dans le Fil face à « rien ne reproche ».
'''
C=C.rstrip('\n')+'\n'+G
a="### ⚑ v134 (6 oct. 2026) — LE CORPS SOMBRE D'UN PROMI EST `#0E78F2`, DÉFINITIF."; assert C.count(a)==1
B='''### ⚑ v135 (6 oct. 2026) — PLUS AUCUN FILET ; LE SYMBOLE DU BOUTON PHOTO ; LES CONTRADICTIONS TRANCHÉES ; L'AMPLEUR À MI-FORCE. (Décisions Tom.) Ce bloc CORRIGE v114 (le filet de la terre), v133, v134 et le §3 là où ils disent autre chose.
> **« La vérité est ce que Tom voit à l'écran. »** Quatre contradictions tranchées : **la Pelote fait un tour en 100 s** (`2π/100`, comme
> l'app et `releve-aura` ; ce fichier écrivait 120) ; **le fond sombre est la seiche `#050302`** dans le rôle `fond` des jetons (JSON, CSS,
> Swift — ils portaient encore `#100D0B`) ; **un design se vend 2 €** (l'écran de l'offre disait « 1 €, ou 4 pour 3 € » : « 4 pour 3 € »
> est RETIRÉ, Tom ne l'a pas redécidé) ; **l'aide de l'Aura et « À propos » disent l'app d'aujourd'hui** (« la plus récente en premier » ;
> « Les sous-titres et les libellés sont en Gilbert », « Les titres, eux, sont en PromiLate. »).
> **⚑ PLUS AUCUN FILET, NULLE PART (C-059).** « Retire le filet autour des disques et des Noyaux, et celui sous le trait et la crête, en clair
> comme en sombre. L'exception de v114 tombe. » `window._sansFilet` rend toujours vrai. Mesuré sans filet (ΔE CIELAB, seuil 15 de
> `redteam_tonsurton`) : sur la terre `#2B1020`, crête `#0B4A2A` 51,3 (Δlum 35,4) · arc tenu `#00341A` 44,6 (Δlum 16,2) · **arc en cours
> `#291547` 24,0 (Δlum 6,0)** — le plus faible, au-dessus du seuil ; sur la seiche, 31,8 à 40,7. `redteam_filets` : liste blanche VIDE.
> ⚠ **Le fond d'un Promi tenu n'a PAS changé** : Promi et Chiche tenus sont déjà identiques (terre, deux thèmes) ; un Cercle n'a pas
> d'état « tenu » (corps ordinaire). « Ce n'est pas le bon fond » attend de savoir lequel (Q407).
> **⚑ LE BOUTON PHOTO PORTE LE CADRE TRAVERSÉ D'UN TRAIT (C-060, choix C)** — fiche, page +, fiche d'un Cercle, deux thèmes ; VoiceOver
> inchangé. (L'appareil de l'avatar, aux Réglages, reste : il parle bien d'une photo.)
> **⚑ SUR `#0E78F2`, LES LIBELLÉS LILAS DU PEAUFINER D'UNE FICHE PROMI SONT `#F4EEFF`** comme la phrase de la page + (Q403 tranchée) —
> mesurés à l'écran : `#C4A2F5` y faisait 1,97:1. « Ma Parole ! » y reste `#FED0C3` (Tom juge sur l'iPhone).
> **⚑ LA PAGINATION DES MONDES AU STUDIO EST UNE RANGÉE DE BARRETTES** (10 × 4, la courante 18 × 4), plus des points : la loi des points
> (C-011). ⚠ **Le menu des palettes « vide, en sombre » n'est PAS reproduit** (trois ouvertures, deux thèmes, monde payant, glissements,
> retour) ; `redteam_palettes` (58) compte maintenant les teintes PEINTES de chaque pastille sur la capture (`--sonde=vide` : il rougit).
> **⚑ L'AMPLEUR À MI-FORCE SOUS DIX MONDES (C-062)** — `_AMP_MI` dans le moteur : à l'ampleur stable de chaque parole (titre et personne)
> s'ajoute `force × (−0,07 + 0,40·u⁴)` : Esquille, Halin, Ritournelle 0,3 · Ramage, Guingois 0,6 · Mascaret, Chantourné, Volubilis 1 ·
> Brouillamini, Chamade 1,5. Madrure, Bobinette et les huit anciens ne bougent pas. La taille ne porte toujours aucun sens.
> **⚑ LA GRILLE ANTI-COERCITION EST AU §12** (reconstituée ; les six critères et les six risques de Tom manquent — Q406).
> Juge neuf : **`redteam_lexique.py`** — termes bannis (liste du §2, en dur) et loi des points, à l'écran, 34 écrans × 2 thèmes × gratuit et
> Ma Parole ! ; dette nommée `lexique-dette.json` (la pastille du Fil `#filDot`, les pastilles de la légende de l'Aura) ; deux sondes.

'''
C=C.replace(a,B+a)
a="python3 redteam_palettes.py    # 32 —"; assert C.count(a)==1
C=C.replace(a,"python3 redteam_lexique.py     # 3 — v135 (C-065) : aucun terme banni affiché, aucun point nouveau hors de l'exception du dessin (dette : lexique-dette.json). --sonde=terme|point : il rougit.\npython3 redteam_palettes.py    # 58 (v135 : trois ouvertures, les teintes PEINTES de chaque pastille, la pagination en barrettes) —")
ecrit('CLAUDE.md',C)
Q=lit('QUESTIONS.md').rstrip('\n')+'''
- **Q403, Q405 — TRANCHÉES (Tom, v135)** : la phrase lilas reste `#F4EEFF`, et les libellés lilas du Peaufiner d'une fiche Promi la suivent ;
  la Pelote tourne en 100 s. Fond sombre = seiche dans les jetons ; un design = 2 €, « 4 pour 3 € » retiré.
- **Q406 — OUVERTE (C-065)** : « les six critères disqualifiants et les six risques cumulés » de la grille anti-coercition ne sont écrits
  nulle part dans le dépôt (ni dans `portage/REGLES.md`). CLAUDE.md §12 porte les trente-deux règles reconstituées. Il me faut le texte de Tom.
- **Q407 — OUVERTE (C-059)** : « ce n'est pas le bon fond » pour un Promi tenu en clair. Mesuré : Promi et Chiche tenus sont identiques
  (terre `#2B1020`, texte crème, deux thèmes) ; un Cercle n'a pas d'état tenu. Quel fond Tom attend-il ? Les filets, eux, sont retirés.
- **Q408 — OUVERTE (C-011)** : le menu des palettes vide en sombre n'est pas reproduit, et les captures jointes n'arrivent pas (quatre lots).
  Les points étaient la pagination des mondes : remplacés par des barrettes — à valider.
- **Q409 — À VALIDER (C-062)** : l'objectif « +15 % sans dépasser Pochade prototype (0,57 à 20, 0,67 à 40) » n'est pas tenable partout — à 40
  dalles, Esquille, Halin, Ritournelle et Mascaret étaient déjà à 0,59–0,60 (+15 % = 0,68–0,69), Ramage à 0,72. Volubilis ne répond pas
  (ses formes ont leur taille propre). Bobinette : mêmes chiffres que Halin et Ritournelle (0,46 / 0,57) — non touché, à dire.
- **Q410 — À VALIDER (C-064)** : « Les titres, eux, sont en PromiLate. » ajouté à « À propos » sans crédit (origine et licence de PromiLate
  inconnues, C-025). La dette de la loi des points : la pastille du Fil et les pastilles de la légende de l'Aura ; et la valeur « · ·· ··· »
  de « C'EST IMPORTANT ? » dans le Peaufiner payant.
'''
ecrit('QUESTIONS.md',Q)
