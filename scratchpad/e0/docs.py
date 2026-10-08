import io
S=io.open('CHANTIERS.md',encoding='utf-8').read(); L=S.split('\n')
def ligne(num):
    for k,l in enumerate(L):
        if l.startswith('| %s |'%num): return k
    raise Exception(num)
def pose(num, dem=None, etat=None, av=None, juge=None, vise=None, prefixe=None):
    k=ligne(num); c=L[k].split(' | '); assert len(c)==7,(num,len(c))
    if dem: c[2]=dem
    if etat: c[3]=etat
    if av: c[4]=av
    if prefixe: c[4]=prefixe+' '+c[4]
    if juge: c[5]=juge
    if vise: c[6]=vise+' |'
    L[k]=' | '.join(c)
ORD="Ordre (A7) : E0 → E1 → E2 et E2bis → E3 → point d'arrêt → E4 → E5 → E6A → validation de Tom → E6B."
pose('C-073',"ENGAGEMENT — E0, « Garde-fous, avant tout autre lot » : ① le verrou de l'onboarding (stockage vierge → il s'affiche ; le terminer ; recharger deux fois → il ne s'affiche plus) ; ② créer `redteam_engagement.py` (R1 à R7) ; ③ Délier au registre. Amendements : A2 (aucune opacité < 1 ni fondu), A3 (aucun impératif, dans R1), A4 (liste de R1 = lexique de CLAUDE.md, « échéance » retiré si l'app l'emploie).",
 'FAIT, EN ATTENTE DE TOM',"E0 (9 oct.) : ① FAIT — `redteam_verrou_onboarding.py` 9/9 (sa sonde, qui retire le verrou, rougit 6/9) ; rien à corriger, le verrou tenait. ② FAIT — `redteam_engagement.py` : R1 (34 écrans, 774 textes, liste alignée sur le §2 de CLAUDE.md ; « échéance » RESTE dans la liste : l'app ne l'affiche sur aucun écran parcouru), A3, R2, R3, R5, R7 au vert ; R4 inactif avant E3 ; A2 inactif tant qu'aucun élément `data-eng` n'existe ; **R6 ROUGE : trois des quatre étapes de l'onboarding d'aujourd'hui n'ont aucune sortie visible** (le prénom, la parole et le trait, le message de fin) — c'est l'état du produit, E2 le refait avec « Plus tard ». La sonde (`--sonde`) fait rougir R1, A3, R2, R3, R5, R7 et A2. `TEXTES_ENGAGEMENT` posé, vide (`lot-ENGAGEMENT-TEXTES`). ③ FAIT — Délier : C-082. À SAVOIR : R3 est jugé dans le cadre de la Pelote ; ailleurs sur l'Aura, les trois chiffres de la légende portent des chiffres (v95).",
 'redteam_engagement, redteam_verrou_onboarding','Tom lit le rapport ; R6 attend E2')
pose('C-074',"ENGAGEMENT — E1, « Gestes appris en situation » : ① un seul composant `GesteFantome` (`montrer(idGeste, elementCible, chemin)`, `oublier(idGeste)`) ; ② il s'affiche après 600 ms d'inactivité, joue le geste deux fois au plus (pause 900 ms), disparaît au premier toucher, drapeau `geste_vu_<id>` dès la première apparition ; ③ inventaire de tous les gestes (tracer pour tenir, sa moitié de Chiche, appui long sur le Noyau, toucher la Pelote, gestes du dessin), chacun branché ; ④ le point d'entrée d'`obReplay` devient « Revoir les gestes » et efface les drapeaux — aucune autre entrée, rien au Studio ; ⑤ `prefers-reduced-motion` : main immobile au départ du geste, avec une flèche du trajet. A2 : la main est au trait plein, OPAQUE, à l'encre du mode (pas « crème à 60 % »).",
 None,"Inscrit, pas commencé. Preuve attendue : pour chaque geste, capture de la première apparition, rechargement → absent, rejeu → présent ; R1, R5, R6 au vert. "+ORD,'redteam_engagement','après E0, sur l’ordre de Tom')
pose('C-075',"ENGAGEMENT — E2, « Le premier Promi, tenu en une minute » : ① état des lieux de `OB[]` (garder / supprimer / remplacer ; garder l'identification et l'étape Studio) ; ② nouvelle séquence : un écran unique (titre, sous-titre, un bouton, une sortie « Plus tard ») → la vraie page + avec une phrase fantôme → plantation réelle → une ligne → tenir → dernière ligne, une fois, drapeau `ob_fini` ; ③ « Plus tard » à chaque étape, un tap, mène à la Toile vide ; le premier Promi n'est jamais redemandé ; ④ l'ordre de coloration progressive reste aux démonstrations. A3 : les textes à l'impératif du document (« Commence par… », « Allons-y », « Fais-le. Puis reviens le tenir. », « La prochaine, dis-la à quelqu'un. ») sont à réécrire. Touche au trait : validation de Tom sur son iPhone 16e.",
 None,"Inscrit, pas commencé. Preuve attendue : parcours Playwright stockage vierge jusqu'au tenu, au plus 5 taps + 1 trait après l'identification, `pid` présent, `ob_fini` posé, rechargement → aucun onboarding ; captures clair et sombre ; R1, R2, R5, R6 au vert. "+ORD,'redteam_engagement','après E1 (avec E2bis)')
pose('C-076',None,None,None,None,'avec E2')
pose('C-077',"ENGAGEMENT — E3, « Le moment "+'"tenir"'+" » : A1 PRIME — ni onde sur les dalles voisines, ni menthe de célébration (loi « aucun effet posé sur la Toile », vert de célébration écarté) ; le moment reste la transformation existante de la matière. On garde : ② l'invariance absolue (R4 : deux Promi qui diffèrent sur tout, durées à 16 ms près, aucune au-delà de 1000 ms) ; ④ le crochet `promiHaptique(nom)`, fonction vide documentée ; ⑤ aucune tâche longue > 50 ms pendant la séquence, sous le monde le plus coûteux. Touche au trait : validation de Tom sur iPhone.",
 None,"Inscrit, pas commencé. Les points ① (séquence menthe + onde) et ③ (mouvement réduit : menthe seule) du document sont SUPPRIMÉS par A1. Puis POINT D'ARRÊT : Tom fait repasser ses deux testeurs, rien ne démarre avant son retour. "+ORD,'redteam_engagement (R4)','après E2 et E2bis')
pose('C-078',"ENGAGEMENT — E4, « Écrans vides qui invitent, et phrases d'exemple à la page + » : ① inventaire de tous les états vides (Toile, Index, Cercle sans membre, Fil, liste des Chiche, recherche sans résultat…) ; ② chaque état vide reçoit deux lignes et un seul geste, jamais deux invitations ; un vide de recherche ne dit jamais la même chose qu'un vide de contenu ; ③ textes provisoires ; ④ page + : une phrase fantôme quand le champ est vide, jamais la même deux fois de suite, effacée à la première frappe. A3 : « Ajoute la première personne. », « Lance un Chiche. » sont à réécrire.",
 None,"Inscrit, pas commencé. Preuve attendue : tableau d'inventaire, capture de chaque état vide en clair et en sombre, un seul élément interactif d'invitation par état, non-répétition sur 50 ouvertures de la page + ; R1, R2 au vert. "+ORD,'redteam_engagement','après le point d’arrêt')
pose('C-079',"ENGAGEMENT — E5, « Phrases d'accueil » : ① un tableau unique `PHRASES_ACCUEIL` de `{id, texte, cible}` (creer, envoyer, chiche, studio, aucune) ; ② une phrase par lancement, à l'arrivée sur la Toile, jamais pendant l'onboarding, centrée au-dessus de la barre basse, sans cadre ni bouton ; elle disparaît au premier toucher, un toucher SUR elle ouvre sa cible ; ③ sélection par une fonction pure (jamais la précédente ; exclure une cible faite dans les 7 derniers jours ; exclure `studio` si l'action n'est pas gratuite ; rien sur l'absence, le temps écoulé, un destinataire qui attendrait) ; ④ corpus provisoire. A2 : OPAQUE, couleur de texte secondaire, apparaît et disparaît SANS FONDU (pas « opacité 0,6 », pas « fondu 300 ms »). A3 : « Lance un Chiche. », « Change de palette. » à réécrire.",
 None,"Inscrit, pas commencé. Preuve attendue : tests unitaires de la sélection, capture en clair et en sombre ; R1, R2 au vert. "+ORD,'redteam_engagement','après E4')
pose('C-080',"ENGAGEMENT — E6A, « La Pelote qui s'enrichit : maquette d'abord » (aucune intégration avant validation de Tom) : ① la Pelote est toujours pleine et belle à zéro ; ② pas de seuils de comptage ; ③ accrétion continue — chaque Promi tenu laisse une inclusion dont la forme dérive du trait réellement tracé, position tirée d'une graine `pid`, taille indépendante du Promi, rien ne se retire jamais ; ④ un fil par personne — A5 : montré SANS épaisseur cumulée, épaisseur constante, Tom tranche ; ⑤ premières fois : changements qualitatifs, une seule fois, jamais annoncés ni listés ; ⑥ rendu déterministe. Livrable : un HTML autonome, neuf états côte à côte, clair et sombre, avec une vignette réduite à 200 px de chacun.",
 None,"Inscrit, pas commencé. "+ORD,'—','après E5')
pose('C-081',"ENGAGEMENT — E6B, « Intégration (après validation de Tom seulement) ».",
 None,"Inscrit, pas commencé. Preuve attendue : monotonie (20 tenus un à un, les inclusions de l'état n incluses dans celles de n+1), déterminisme (deux rendus identiques au pixel), R3 au vert, 60 im/s sur 390 px. "+ORD,'redteam_engagement (R3)','après la validation de E6A par Tom')
pose('C-027',"« Après le portage : le relevé. » (« délier » a son chantier propre : C-082, depuis E0.)",None,"E0 (9 oct., Tom) : C-027 ne porte plus que le relevé ; Délier est en C-082. Après le portage Swift.")
pose('C-022',None,None,None,None,None,"E0 (ENGAGEMENT.md, E3 point 4, à noter pour ce chantier-ci) : **Safari iOS n'implémente pas `navigator.vibrate`** — sur l'iPhone de Tom le prototype ne vibre donc pas du tout, quel que soit le code ; c'est très probablement la cause du manque ressenti au premier test. Le rendu réel viendra de Core Haptics au portage Swift ; E3 n'écrit que le crochet `promiHaptique(nom)`.")
k=ligne('C-081')
L.insert(k+1,"| C-082 | 9 oct. · E0 point 3 (ENGAGEMENT.md) · demande de Tom | « Délier » (étude 2 : issue pour un Promi jamais tenu). *Ce chantier-ci augmente le nombre de Promi créés, donc le stock de dalles à tenir ; sans Délier, l'état « à tenir pour toujours » devient le critère 1 de la grille.* | OUVERT | E0 : chantier propre créé (il était mêlé au relevé dans C-027). Rien n'est conçu ni construit. | — | à fixer par Tom (avant ou avec le chantier d'engagement) |")
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
Q=io.open('QUESTIONS.md',encoding='utf-8').read().rstrip('\n')+"""

## E0 — le chantier d'engagement (9 oct. 2026)
- **Q420 — LEVÉE** : `ENGAGEMENT.md` est à la racine ; E0 est exécuté seul (C-073).
- **Q421 — À TRANCHER (R6)** : l'onboarding d'aujourd'hui n'a de sortie visible qu'à sa dernière étape (le compte : « plus tard »). R6 est donc ROUGE jusqu'à E2, qui le refait. Faut-il poser une sortie dès maintenant ?
- **Q422 — À TRANCHER (R3)** : « aucun chiffre sur la Pelote » est jugé dans le cadre de la Pelote. L'écran de l'Aura porte ailleurs les trois chiffres de la légende (tenues, en cours, à tenir — v95, R-015). Le document dit « sur l'écran de la Pelote » : la règle vise-t-elle aussi ces trois chiffres ?
- **Q423 — À SAVOIR (R1, A4)** : « échéance » n'est affiché sur aucun des 34 écrans parcourus ; il RESTE donc dans la liste interdite. Si un écran non parcouru l'emploie, le juge le dira.
- **Q424 — À SAVOIR** : `redteam_engagement` tourne sur le serveur du projet (127.0.0.1:8752), pas en `file://` comme l'écrit le document : c'est la règle du dépôt, et le moteur se charge depuis un second fichier.
"""
io.open('QUESTIONS.md','w',encoding='utf-8').write(Q+'\n')
E=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read(); LL=E.split('\n')
i=[k for k,l in enumerate(LL) if l.startswith('- **v138 (9 oct.)**')][0]
LL.insert(i+1,"- **E0 (9 oct.)** — le chantier d'engagement, lot E0 seul (C-073) : `redteam_verrou_onboarding` 9/9 ; `redteam_engagement` 8/9, R6 rouge (l'onboarding n'a de sortie visible qu'à sa dernière étape — E2 le refait), R4 et A2 inactifs ; `TEXTES_ENGAGEMENT` posé vide ; Délier a son chantier (C-082). E1 n'est pas commencé.")
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write('\n'.join(LL))
C=io.open('CLAUDE.md',encoding='utf-8').read()
def r(a,b):
    global C
    assert C.count(a)==1,(a[:60],C.count(a)); C=C.replace(a,b)
r("### ⚑ v138 (9 oct. 2026) — LE BORD DE LA PELOTE SUR LES DEUX RENDUS ;","""### ⚑ E0 (9 oct. 2026) — LE CHANTIER D'ENGAGEMENT : LES GARDE-FOUS. (`ENGAGEMENT.md` ; LES AMENDEMENTS A1 À A7, EN FIN DE DOCUMENT, PRIMENT.)
> **Le document est à la racine ; E0 est fait, seul (C-073). E1 n'est pas commencé.** Les lots : C-073 à C-081 ; **Délier : C-082** (C-027 ne
> porte plus que le relevé). Ordre (A7) : E0 → E1 → E2 et E2bis → E3 → **point d'arrêt** → E4 → E5 → E6A → validation de Tom → E6B.
> **Trois conventions posées en E0, à tenir dans tous les lots E** : ① tous les textes du chantier vivent dans **`window.TEXTES_ENGAGEMENT`**
> (`lot-ENGAGEMENT-TEXTES`, vide en E0), marqués `/* TEXTE PROVISOIRE — Tom */` ; ② **tout élément créé par le chantier porte `data-eng`** —
> c'est sur eux que le juge vérifie A2 (opacité 1 sur eux et leurs ancêtres, aucun fondu, aucune animation, aucun texte à demi transparent) ;
> ③ **aucun texte à l'impératif** (A3) : les textes provisoires du document qui en contiennent se réécrivent avant d'entrer dans l'objet.
> **`redteam_engagement.py` passe à la fin de CHAQUE lot E** (Chromium, serveur du projet) : R1 lexique (la liste = les termes bannis du §2 +
> badge, série, streak, niveau, classement, points, bravo, félicitations, record ; « échéance » y reste tant que l'app ne l'affiche pas —
> le juge le constate et le dit) et A3 · R2 absence et temps · R3 aucun chiffre dans le cadre de la Pelote · R4 (inactif avant E3) · R5 aucune
> clé nouvelle au stockage après trois « tenir » · R6 une sortie visible à chaque étape de l'onboarding · R7 aucun âge (« dans N jours » est un
> horizon, en liste blanche) · A2. **`--sonde` fait rougir R1, A3, R2, R3, R5, R7 et A2.** État à la naissance : 8/9 — **R6 ROUGE** (le
> prénom, la parole et le trait, le message de fin n'ont aucune sortie visible ; E2 refait l'onboarding avec « Plus tard » — Q421).
> **`redteam_verrou_onboarding.py`** : stockage vierge → l'onboarding s'affiche ; terminé par son vrai chemin ; deux rechargements → il ne
> revient pas ; 9/9 (`--sonde` retire le verrou : rouge). ⚠ Le message de fin n'accepte le toucher qu'après ses quatre secondes (v21) :
> un parcours automatique qui touche trop tôt le croit bloqué.

### ⚑ v138 (9 oct. 2026) — LE BORD DE LA PELOTE SUR LES DEUX RENDUS ;""")
r("python3 redteam_bord.py        # 8 — v137 (C-002)","""python3 redteam_engagement.py  # E0 (C-073) — la grille du chantier d'engagement : R1 lexique + A3 (aucun impératif), R2, R3, R4 (inactif avant E3), R5, R6, R7, A2. À PASSER À LA FIN DE CHAQUE LOT E. --sonde : il rougit. ⚠ 8/9 à la naissance : R6 rouge jusqu'à E2.
python3 redteam_verrou_onboarding.py # 9 — E0 : stockage vierge → l'onboarding s'affiche ; terminé ; deux rechargements → il ne revient pas. --sonde : il rougit.
python3 redteam_bord.py        # 8 — v137 (C-002)""")
io.open('CLAUDE.md','w',encoding='utf-8').write(C)
