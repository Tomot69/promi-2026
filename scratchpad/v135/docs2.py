import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
L=lit('CHANTIERS.md').rstrip('\n').split('\n')
MAJ={
'C-011':('OUVERT','v135 : NON REPRODUIT (trois ouvertures, deux thèmes, monde payant, glissements, RETOUR, noir et blanc) ; la capture n’est pas arrivée. Fait : la rangée de points était la pagination des mondes — remplacée par des barrettes (loi des points) ; le juge compte les teintes peintes de chaque pastille (sonde `vide` : il rougit ; sur l’état d’avant il ne rougit que sur les points).','redteam_palettes 58/58','attend la capture'),
'C-059':('EN COURS','v135 : tous les filets retirés (disques, Noyaux, trait, crête ; clair et sombre ; l’exception de v114 tombe). Sans filet, sur la terre : crête ΔE 51,3 · arc tenu 44,6 · arc en cours 24,0 (seuil 15). Le FOND n’a pas changé : Promi et Chiche tenus sont identiques (terre), un Cercle n’a pas d’état tenu — « pas le bon fond » : lequel ? (Q407). Planche `planche-v135/tenus`.','redteam_filets (liste blanche vide) · redteam_tonsurton','attend Q407'),
'C-060':('FAIT, EN ATTENTE DE TOM','v135 : le cadre traversé d’un trait (C) sur le bouton photo — fiche, page +, fiche d’un Cercle, deux thèmes ; VoiceOver inchangé ; « Importer une photo ».','redteam_photo_menu 20/20 · redteam_dessin','—'),
'C-062':('FAIT, EN ATTENTE DE TOM','v135 : `_AMP_MI` dans le moteur (force × (−0,07 + 0,40·u⁴)) : Esquille, Halin, Ritournelle 0,3 · Ramage, Guingois 0,6 · Mascaret, Chantourné, Volubilis 1 · Brouillamini, Chamade 1,5. CV avant → après à 20 / 40 dalles : tableau au rapport v135 ; objectif +15 % tenu sur une partie seulement (Q409). Bobinette : mesuré 0,46 / 0,57, non touché. Planches `planche-v135/tailles-1`, `-2`.','banc_rendu (refigé pour ces mondes) · redteam_rythme','—'),
'C-064':('FAIT, EN ATTENTE DE TOM','v135 : CLAUDE.md §7 → 2π/100 ; rôle `fond` sombre `#050302` (JSON, CSS, Swift, redteam_tokens) ; écran de l’offre « ou un design à l’unité — 2 € » (« 4 pour 3 € » retiré) ; aide de l’Aura : « la plus récente en premier » ; À propos : « Les sous-titres et les libellés sont en Gilbert », + « Les titres, eux, sont en PromiLate. » (Q410).','redteam_tokens 46/46','—'),
'C-065':('EN COURS','v135 : CLAUDE.md §12 — la grille telle que `portage/REGLES.md` la porte (32 règles reconstituées, mot pour mot). ⚠ « Les six critères disqualifiants et les six risques cumulés » n’existent nulle part dans le dépôt : texte de Tom attendu (Q406). Juge `redteam_lexique.py` : termes bannis et loi des points, à l’écran ; dette nommée `lexique-dette.json` (2).','redteam_lexique 3/3 (sondes terme, point)','attend Q406'),
'C-050':('FAIT, EN ATTENTE DE TOM','v135 : la phrase lilas reste `#F4EEFF` ; les libellés lilas du Peaufiner d’une fiche Promi la suivent (mesurés : `#C4A2F5` 1,97:1 → `#F4EEFF` 3,71:1) ; « Ma Parole ! » reste `#FED0C3`, Tom juge sur l’iPhone.','redteam_decisions · redteam_couleurs_ref','—'),
}
for i,l in enumerate(L):
    m=re.match(r'\| (C-\d+) \|',l)
    if m and m.group(1) in MAJ:
        c=l.split(' | '); assert len(c)==7,m.group(1)
        e,p,j,v=MAJ[m.group(1)]; c[3]=e; c[4]=c[4]+' '+p if m.group(1) in ('C-050',) else p; c[5]=j; c[6]=v+' |'; L[i]=' | '.join(c)
ecrit('CHANTIERS.md','\n'.join(L)+'\n')
E=lit('ETAT-DES-LIEUX.md')
a=[l for l in E.split('\n') if l.startswith('- **v134 (6 oct.)**')][0]
E=E.replace(a,a+'''
- **v135 (6 oct.)** — plus aucun filet (C-059) ; bouton photo = cadre traversé d'un trait (C-060) ; libellés lilas du Peaufiner Promi en `#F4EEFF` ; contradictions tranchées (Pelote 100 s, fond seiche dans les jetons, design 2 €, aide de l'Aura, À propos) ; grille au §12 de CLAUDE.md (reconstituée, Q406) + `redteam_lexique` ; pagination du Studio en barrettes ; ampleur à mi-force sous dix mondes (`_AMP_MI`). **Non reproduit : le menu des palettes vide (C-011). Non changé : le fond d'un Promi tenu (Q407).**''')
E=E.rstrip('\n')+'''
| v135 | Plus aucun filet (C-059) | `redteam_filets` · `redteam_tonsurton` ; planche `planche-v135/tenus` | un Promi tenu et un Chiche tenu, clair et sombre : la crête verte et l'anneau sans filet (l'arc « en cours » violet est le plus faible sur la terre) ; les Noyaux de l'Aura en sombre |
| v135 | Le bouton photo : le cadre traversé d'un trait (C-060) | `redteam_photo_menu` 20/20 | une fiche, la page +, la fiche d'un Cercle, clair et sombre |
| v135 | Les libellés lilas du Peaufiner sur le bleu (Q403) ; « Ma Parole ! » en `#FED0C3` | `redteam_decisions` | Peaufiner d'une fiche Promi en sombre ; un mur |
| v135 | Le Studio : la pagination en barrettes ; le menu des palettes (C-011, non reproduit) | `redteam_palettes` 58/58 | ouvrir, fermer, rouvrir, ouvrir le menu en sombre : si le menu est vide, une capture d'écran envoyée autrement (elles n'arrivent pas dans le message) |
| v135 | Un peu plus de diversité de tailles (C-062) | planches `planche-v135/tailles-1`, `-2` | sous Esquille, Halin, Brouillamini, Ramage, Guingois, Chantourné, Volubilis, Chamade, Ritournelle, Mascaret, avec vingt paroles et plus |
| v135 | L'écran de l'offre (« 2 € »), l'aide de l'Aura, À propos (C-064) | — | relire les trois textes |
'''
ecrit('ETAT-DES-LIEUX.md',E)
P=lit('portage/A-INTEGRER.md').rstrip('\n')+'''

## v135 (6 oct. 2026) — ce qui a changé APRÈS l'écriture du dossier, à reporter dans les dix documents

- **Plus aucun filet** (disques, Noyaux, trait, crête ; clair et sombre) : l'exception « terre d'une fiche tenue » de JETONS et de REGLES tombe.
- **Le bouton photo** porte le cadre traversé d'un trait (SPEC-ECRANS : fiche, page +, Cercle) ; VoiceOver inchangé.
- **Sur `#0E78F2`** : les libellés lilas du Peaufiner d'une fiche Promi sont `#F4EEFF` (JETONS).
- **Contradictions du README, tranchées** : Pelote = un tour en 100 s ; fond sombre = seiche `#050302` dans le rôle `fond` ; un design = 2 €
  (« 4 pour 3 € » retiré) ; aide de l'Aura = « la plus récente en premier » ; À propos = Gilbert pour sous-titres et libellés, PromiLate pour les titres.
- **Studio** : la pagination des mondes est une rangée de barrettes (10 × 4, la courante 18 × 4), plus des points.
- **Moteur** : `_AMP_MI` — ampleur à mi-force sous dix mondes (SPEC-RENDU §a) ; le banc de rendu est refigé pour eux.
- **La grille anti-coercition** est au §12 de `CLAUDE.md` (les trente-deux règles de REGLES §A) ; les six critères et les six risques de Tom manquent (Q406).
- **Juge neuf** : `redteam_lexique.py` (TESTS : termes bannis et loi des points ; se porte en test sur les chaînes et en revue des composants).
'''
ecrit('portage/A-INTEGRER.md',P)
R=lit('portage/README.md')
a="## Les contradictions trouvées en écrivant le dossier (à trancher avant de coder)"; assert R.count(a)==1
R=R.replace(a,"> **⚑ v135 (6 oct. 2026)** : les cinq premières contradictions ci-dessous sont TRANCHÉES par Tom (« la vérité est ce que Tom voit à l'écran ») et corrigées dans l'app et dans `CLAUDE.md` — voir `A-INTEGRER.md`, section v135. Les documents 1 à 10 n'ont pas été réécrits : la section v135 d'`A-INTEGRER.md` prime sur eux.\n\n"+a)
ecrit('portage/README.md',R)
MEM='/Users/macbookpro/.claude/projects/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/memory/'
ecrit(MEM+'captures-de-tom-n-arrivent-pas.md','''---
name: captures-de-tom-n-arrivent-pas
description: Les captures que Tom « joint » à ses lots collés n'arrivent pas dans la conversation — le dire en tête de lot
metadata:
  type: feedback
---

Sur les lots v133, v134 et v135 (6 oct. 2026), Tom a écrit « capture jointe » pour le Studio (C-057, C-011) et le bas des fiches (C-059) :
aucune image n'est arrivée avec ses messages collés. Trois défauts sont restés non reproduits faute de les voir.

**Why:** sans la capture, je corrige ce que je trouve, pas forcément ce qu'il voit — et il croit que j'ai vu.

**How to apply:** dès qu'un lot dit « capture jointe » et qu'aucune image n'est dans le message, le dire AU DÉBUT de la réponse et demander
qu'il la dépose dans le dossier du projet (je peux lire un fichier image par son chemin) ou la décrive. Voir [[point-de-reprise-6-oct-v135]].
''')
ecrit(MEM+'point-de-reprise-6-oct-v135.md','''---
name: point-de-reprise-6-oct-v135
description: État à la fin du lot v135 (6 oct. 2026) — filets retirés, symbole C, grille au §12, ampleur à mi-force ; ce qui attend Tom
metadata:
  type: project
---

Lot v135 (6 oct. 2026). Fait : plus aucun filet ; bouton photo = cadre traversé d'un trait ; libellés lilas du Peaufiner Promi `#F4EEFF` ;
Pelote 100 s, fond seiche dans les jetons, design 2 €, aide de l'Aura et À propos ; pagination du Studio en barrettes ; `_AMP_MI` (ampleur
à mi-force sous dix mondes) ; CLAUDE.md §12 (grille reconstituée) ; `redteam_lexique.py`.

Attend Tom : Q406 (les six critères disqualifiants et les six risques cumulés n'existent nulle part), Q407 (quel fond pour un Promi tenu),
Q408 / C-011 (menu des palettes vide non reproduit), Q409 (objectif de CV non tenable partout ; Bobinette), Q410.
Le dossier `portage/` n'est pas réécrit : la section v135 de `portage/A-INTEGRER.md` prime. Voir [[captures-de-tom-n-arrivent-pas]].
''')
I=lit(MEM+'MEMORY.md').rstrip('\n')+'\n- [Les captures de Tom n\'arrivent pas](captures-de-tom-n-arrivent-pas.md) — « capture jointe » sans image : le dire en tête, demander un fichier dans le dossier\n- [Point de reprise — 6 oct. (v135)](point-de-reprise-6-oct-v135.md) — filets retirés, symbole C, grille §12 reconstituée, ampleur mi-force ; attend Q406–Q410\n'
ecrit(MEM+'MEMORY.md',I)
