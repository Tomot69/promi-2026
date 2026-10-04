import io
def sub(f,a,b):
    S=io.open(f,encoding='utf-8').read(); assert S.count(a)==1,(f,a[:50],S.count(a)); io.open(f,'w',encoding='utf-8').write(S.replace(a,b))
sub('CLAUDE.md',"### ⚑ v128 (4 oct. 2026) — L'ONBOARDING (TEXTE, VOISINES VIDES)","""### ⚑ v129 (4 oct. 2026) — L'ONBOARDING, TEXTE FIGÉ ; « CERCLE » CENTRÉ ; LE MODE DESSIN LIBÈRE L'ÉCRAN. (Décisions Tom.)
> **La dernière diapositive (C-006), quatre paragraphes, mot pour mot** : « C’est planté. » · « Ton premier Promi, ta première dalle sur ta
> Toile. Plus qu’à le tenir. » · « Primo, un Promi, c’est ta parole donnée. Deuxio, un Chiche, c’est un coup de culot. Tertio, un Cercle,
> c’est tout cela à la fois, mais à plusieurs. » · « Le reste se découvre en traçant. La suite t’appartient. » **« Deuxio » est le seul
> mot penché : 3°** (`.onbv-deux`, `skewX(-3deg)`), même police, même graisse, même couleur. La taille et la disposition des voisines sont
> validées. `redteam_onboarding` porte le texte EN DUR (`TEXTE_FIN`) et l'inclinaison (O22 : 3° ± 0,5, aucune autre).
> **« CERCLE » dans son encart (C-046) — la cause n'était ni la police ni la ligne de base** : une règle de v100
> (`#detailPoster.dp-mode-nuee #dptNat{translate:none}`) retirait au Cercle le recentrage de v97 (+2,65), pour rendre à `redteam_nuee` sa
> cote d'avant. L'encre du mot est maintenant à la même hauteur pour les trois natures (58,7 → 81,3, milieu 70). Juge :
> **`redteam_motmarque.py`** (l'ENCRE, pas la boîte ; ± 0,5 pt ; 0/4 avant). `redteam_nuee` : la cote du mot passe de 52 à 55,7.
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — quatrième principe : LE MODE DESSIN LIBÈRE L'ÉCRAN.** Les disques et leurs noms
> disparaissent : la place va aux réglages du dessin. L'encart du haut (nature, ✕ FERMER) est masqué : il n'en reste que le CONTOUR, au
> trait fin, sans fond ni texte — jamais une transparence. Tout revient à POSER ou à la sortie du mode.
> **C-031** : Volubilis, Guingois, Ramage et Esquille restent immobiles au repos dans le prototype — REPORTÉ au portage Swift.
> **`redteam_couleurs_ref` (C-047)** : les « 2 écarts » de v128 étaient du JUGE — une mini-dalle du fil d'un Cercle défilé, peinte à la
> demande, était vide côté référence au moment du relevé (« ΔE 99 » face à rien). Un canevas vide d'un seul côté est compté et listé
> (« non peints »), dans les deux sens ; il n'est plus comparé à rien.
> **C-045 — le trait de validation personnalisé** : concept seul, `TRAIT-PERSONNALISE-CONCEPT.md` ; rien n'est construit.

### ⚑ v128 (4 oct. 2026) — L'ONBOARDING (TEXTE, VOISINES VIDES)""")
sub('CLAUDE.md',"python3 redteam_retour.py      # v127 (C-028)","""python3 redteam_motmarque.py   # 4 — v129 (C-046) : l'encre du mot de la nature (PROMI, CHICHE, CERCLE) est à la même hauteur dans son encart, ± 0,5 pt,
                               #   clair et sombre (capture @3x). Rougit sur sauvegardes/app-avant-v129.html (0/4 : CERCLE 2,7 pt trop haut).
python3 redteam_retour.py      # v127 (C-028)""")
L=io.open('CHANTIERS.md',encoding='utf-8').read().split('\n')
M={
'C-006':('FAIT, EN ATTENTE DE TOM'," v129 : TEXTE FIGÉ en quatre paragraphes (« C’est planté. » …), « Deuxio » penché de 3° (lui seul), porté en dur par `redteam_onboarding` (46/46 ; 42/46 sur v128). ⚠ Le « ! » isolé de la fin du texte dicté (« La suite t’appartient. ! ») n'est PAS posé — à confirmer.",None,'v129'),
'C-042':(None," v129 : quatrième principe inscrit — le mode dessin LIBÈRE l'écran (disques et noms masqués, l'encart du haut réduit à son contour au trait fin) ; planche `planche-v129/dessin-epure-*` (étapes 3 à 6, rangées A, B, C, fiche Promi et fiche Cercle, étape 6 en sombre).",None,None),
'C-045':('FAIT, EN ATTENTE DE TOM',"v129 : concept écrit, `TRAIT-PERSONNALISE-CONCEPT.md` — le parcours, les trois points à résoudre avec leurs options (couloir ou base qui bouge ; qui trace quelle moitié ; garde-fous du geste), quatre décisions à prendre avant toute planche. Rien n'est construit.",'—','v129 (concept)'),
'C-046':('FAIT, EN ATTENTE DE TOM',"v129 : CAUSE — une règle de v100 retirait au Cercle le recentrage de v97 (translate +2,65) ; ni la police ni la ligne de base. Encre de « CERCLE » : 56,0 → 78,3 avant, 58,7 → 81,0 après, comme « PROMI » (58,7 → 81,3) et « CHICHE ». `redteam_motmarque` 4/4 (0/4 avant) ; `redteam_nuee` mis à la cote décidée (52 → 55,7, original dans sauvegardes/).",'redteam_motmarque','v129'),
'C-047':('FAIT, EN ATTENTE DE TOM',"v129 : défaut du JUGE. Une mini-dalle du fil du Cercle défilé (« TENU arroser tous les… »), peinte à la demande, était vide côté référence au relevé : le juge comparait à rien (« ΔE 99 »). Reproduit 1 passage sur 3, en clair puis en sombre. Corrigé : un canevas vide d'un seul côté est compté et listé, plus comparé (dans les deux sens ; original dans sauvegardes/).",'redteam_couleurs_ref','v129'),
}
for i,l in enumerate(L):
    for k,(etat,plus,jg,lot) in M.items():
        if l.startswith('| '+k+' |'):
            c=l.split(' | '); assert len(c)==7,(k,len(c))
            if etat: c[3]=etat
            c[4]=(plus if c[4].strip() in ('—','') else c[4]+plus)
            if jg: c[5]=jg
            if lot: c[6]=lot+' |'
            L[i]=' | '.join(c)
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
S=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read().rstrip('\n').split('\n')
i=[k for k,l in enumerate(S) if l.startswith('- **v128 (4 oct.)**')][0]
S.insert(i+1,"- **v129 (4 oct.)** — **Onboarding** : texte figé en quatre paragraphes, « Deuxio » penché de 3° (C-006). **« CERCLE » centré dans son encart** (C-046, `redteam_motmarque`). **Outil de dessin** : le mode dessin libère l'écran (planche, C-042). **C-031** reporté au portage Swift. **`redteam_couleurs_ref`** : canevas non peints comptés, plus comparés à rien (C-047). **Trait personnalisé** : concept (C-045, `TRAIT-PERSONNALISE-CONCEPT.md`).")
S=[l.replace("| v128 | L'onboarding, dernière diapositive : le texte, les voisines en cellules vides (C-006) | planche `onboarding-fin` (diapositive et vraie Toile côte à côte) | une fenêtre privée, clair et sombre : les voisines se voient-elles assez en sombre ? |","| v128 | L'onboarding, dernière diapositive (C-006) | planche `onboarding-fin` | *remplacé par la ligne v129 (voisines validées par Tom)* |").replace("| v128 | L'outil de dessin (C-042) : PLANCHE en parcours — choisir la rangée (A, B, C), l'effilé (E1, E2), le symbole (S1, S2) | `planche-v128/dessin-parcours-*` | les planches, version téléphone |","| v128 | L'outil de dessin (C-042) : PLANCHE en parcours | `planche-v128/dessin-parcours-*` | *complété par la ligne v129* |") for l in S]
S+=["| v129 | L'onboarding : le texte figé, « Deuxio » penché de 3° (C-006) | `redteam_onboarding` 46/46 ; planche `planche-v129/onboarding-fin` | une fenêtre privée : le clin d'œil de « Deuxio » se voit-il juste assez ? |",
"| v129 | « CERCLE » centré dans son encart (C-046) | `redteam_motmarque` 4/4 | ouvrir un Cercle, puis un Promi et un Chiche |",
"| v129 | L'outil de dessin (C-042) : le mode dessin épuré — choisir la rangée (A, B, C), l'effilé (E1, E2), le symbole (S1, S2) | `planche-v129/dessin-epure-*` | les planches, version téléphone |",""]
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write('\n'.join(S))
io.open('portage/A-INTEGRER.md','a',encoding='utf-8').write("""- **C-045 · le trait de validation personnalisé (concept, v129)** : si Tom le retient, le chemin est une DONNÉE de la parole (une liste de
  points lissés), jamais une image — voir `TRAIT-PERSONNALISE-CONCEPT.md`.
""")
io.open('QUESTIONS.md','a',encoding='utf-8').write("""
## LOT v129 — 4 octobre 2026 (décisions dans CHANTIERS.md : C-006, C-031, C-042, C-045, C-046, C-047)

- **Tranché par Tom** : le texte de la dernière diapositive (quatre paragraphes, « Deuxio » penché de 3°) ; voisines validées ; C-031 reporté à Swift ; le mode dessin libère l'écran.
- **À confirmer** : le « ! » isolé à la fin du texte dicté (« La suite t’appartient. ! ») — non posé.
- **À trancher** : le trait personnalisé (C-045) — quatre décisions listées en fin de `TRAIT-PERSONNALISE-CONCEPT.md`.
""")
D=io.open('DESSIN-INVENTAIRE.md',encoding='utf-8').read()
D=D.replace("## Ce que montrent les planches (v127)","> ⚑ v129 : **le mode dessin libère l'écran** — les disques et leurs noms disparaissent, l'encart du haut ne garde que son contour au trait fin (sans fond ni texte, jamais une transparence) ; tout revient à POSER ou à la sortie du mode. Planche `planche-v129/dessin-epure-*`.\n\n## Ce que montrent les planches (v127)")
io.open('DESSIN-INVENTAIRE.md','w',encoding='utf-8').write(D)
m='/Users/macbookpro/.claude/projects/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/memory/'
io.open(m+'point-de-reprise-4-oct-v129.md','w',encoding='utf-8').write("""---
name: point-de-reprise-4-oct-v129
description: "v129 (4 oct. 2026) — onboarding texte figé (Deuxio penché), CERCLE centré, mode dessin épuré (planche), trait personnalisé (concept C-045), C-031 reporté à Swift"
metadata:
  type: project
---

v129 : texte de la dernière diapositive figé (`TEXTE_FIN` en dur dans redteam_onboarding, « Deuxio » skewX(-3deg)) ; « CERCLE » recentré (cause : règle v100 `translate:none`, juge `redteam_motmarque.py`) ; planche `planche-v129/dessin-epure-*` ; `TRAIT-PERSONNALISE-CONCEPT.md` (C-045) ; `portage/A-INTEGRER.md` (notes pour le dossier de portage, v130).

- `redteam_onboarding` et `redteam_nuee` ne prennent pas de fichier en argument : `APP_ONB=…` / `APP_NUEE=…` (URL servie) pour prouver sur une ancienne version.
- Dans un `python3 - <<EOF` : jamais de guillemets droits doubles dans une chaîne délimitée par des guillemets doubles (trois erreurs dans ce lot) — écrire le patch dans un fichier avec des triples guillemets.
- `redteam_couleurs_ref` : « ΔE 99 » = un canevas vide côté référence (mini-dalle peinte à la demande), défaut du juge, corrigé (non peints comptés).
- Ouverts : le « ! » isolé du texte de l'onboarding (non posé) ; choix du dessin (rangée, effilé, symbole) ; quatre décisions du trait personnalisé ; v130 = dossier de portage (C-021).

Voir [[point-de-reprise-4-oct-v128]].
""")
io.open(m+'MEMORY.md','a',encoding='utf-8').write("- [Point de reprise — 4 oct. (v129)](point-de-reprise-4-oct-v129.md) — onboarding figé (Deuxio 3°), CERCLE centré (redteam_motmarque), mode dessin épuré, concept du trait personnalisé (C-045), C-031 reporté à Swift\n")
