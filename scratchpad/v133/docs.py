import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
# ── CHANTIERS
C=lit('CHANTIERS.md'); L=C.split('\n')
MAJ={
'C-056':('FAIT, EN ATTENTE DE TOM','v133 : `button.dz-quitter` dans le contour de l’encart, calé sur le bord droit de « ✕ FERMER » (44 pt, ✕ de 18), sort par `sort(false)` — le dessin en cours est gardé ; « Quitter le dessin ». Sonde `--sonde=quitter` : 77/79.','redteam_dessin 79/79','—'),
'C-057':('FAIT, EN ATTENTE DE TOM','v133 : cause nommée — à la 2e ouverture du Studio, `buildStudio` rebâtit le nom de la palette (`#st3pn`) et `posePals` ne retirait que l’ancienne rangée et l’ancienne jauge : deux noms, la rangée neuve rangée APRÈS le vieux nom. Primesautier en tête, ordre des autres inchangé. ⚠ La capture de Tom n’est pas arrivée : c’est le défaut que j’ai trouvé, pas forcément celui qu’il a vu.','redteam_palettes 28/28 (22/28 sur l’état d’avant)','—'),
'C-058':('OUVERT','v133 : NON REPRODUIT. Vingt mondes × trois dalles au vrai doigt : 21/21 sur l’état actuel (le juge ne rougit pas). Essayé aussi : chemin Studio → Ramage → fermer, avec et sans Ma Parole !, après plantation, après « tenir », après 20 s de repos, appui tenu, pincement. Deux pistes non prouvées : le compteur `_fingers` resté > 0 si un `pointerup` ne revient pas à `#stage` ; le seuil de 700 ms lu sur l’heure de traitement.','redteam_toucher 21/21','v134 (il me faut le chemin exact)'),
'C-059':('OUVERT','v133 : RIEN MODIFIÉ, arrêté. Mesuré en clair : les trois fiches ont déjà le même corps (crème `#F7F0DE`, barre Peaufiner à la couleur de la nature, Peaufiner ouvert identique) et aucun filet n’est peint autour des disques ni sous le trait (hors la terre d’une fiche tenue, exception v114). Seules différences : l’anneau du rond Partager (crème sur Promi et Cercle, encre sur Chiche) et « Peaufiner » en violet sur le Cercle. Je ne vois pas ce que Tom voit : capture demandée.','—','v134'),
'C-060':('EN COURS','v133 : « Importer une photo » posé (app et juges). Planche des trois symboles `planche-v133/symboles` (A le feutre, B la plume sur le cadre, C le cadre et le trait), clair et sombre : Tom choisit, puis on remplace.','redteam_photo_menu 20/20','v134'),
'C-061':('FAIT, EN ATTENTE DE TOM','v133 : sans Ma Parole !, encre du mode sur le champ de la nature ; le panneau COULEUR est un mur (flou 4,8 px, rien ne s’y choisit, la phrase des murs monte dessus, devant le mode) ; à l’ouverture de l’offre on sort du mode, le dessin en cours gardé. Ajouté à la page de l’offre : « Douze mondes de plus, les couleurs du dessin ». Sonde `--sonde=mur` : 73/79.','redteam_dessin 79/79','—'),
'C-062':('EN COURS','v133 : ① la taille ne porte AUCUN sens d’importance ni d’ancienneté — seul un Cercle est plus grand (base 14 contre 3,4) ; dans les douze mondes neufs une « ampleur » stable tirée du titre et de la personne. ② Mesuré (quatre Toiles par effectif, 3 à 60) : le coefficient de variation NE BAISSE PAS — Pochade 0,35–0,49 partout, Madrure 0,31 → 0,65, Esquille 0,43 → 0,61. ③ Prototype hors app (l’ampleur étendue aux anciens mondes) : planche `planche-v133/tailles`. Rien d’intégré.','—','v134 (décision de Tom)'),
'C-063':('FAIT, EN ATTENTE DE TOM','v133 : les dix-huit phrases dans `lot-V104-MURS` (`TEXTES`), mots en orange cherchés dans l’ordre ; rotation inchangée. Captures `planche-v133/murs`.','redteam_murs 28/28 · redteam_maparole 14/14','—'),
'C-050':('EN COURS','v133 : défaut provisoire `#1A52F0` (jetons, JSON = CSS = Swift) ; `?bleu=1…5` pose le corps en direct (1 `#1560E8` · 2 `#1A52F0` · 3 `#2046F2` · 4 `#273CEB` · 5 `#0A5CF5`), valeur affichée en bas ; « Ma Parole ! » (3:1) et la phrase lilas (4,5:1) recalculées pour chaque candidat. Tom choisit sur l’iPhone, puis on fige et on retire le paramètre.','redteam_decisions · redteam_tokens 46/46','v134'),
'C-042':('FAIT, EN ATTENTE DE TOM','v133 : déploiements à 16 pt au-dessus de la rangée ; rangée centrée dans sa zone basse (12 pt au-dessus, 12 pt jusqu’au bord bas utile, 844 − 34) — la surface passe de 754 à 742 pt ; ✕ de sortie (C-056) ; couleurs dans Ma Parole ! (C-061). v132 : construit (`lot-V132-DESSIN`).','redteam_dessin 79/79 (sondes : quitter, centre, mur + les cinq de v132)','—'),
}
for i,l in enumerate(L):
    m=re.match(r'\| (C-\d+) \|',l)
    if m and m.group(1) in MAJ:
        c=l.split(' | '); assert len(c)==7,(m.group(1),len(c))
        e,p,j,v=MAJ[m.group(1)]; c[3]=e; c[4]=p; c[5]=j; c[6]=v+' |'; L[i]=' | '.join(c)
ecrit('CHANTIERS.md','\n'.join(L))
# ── QUESTIONS
Q=lit('QUESTIONS.md').rstrip('\n')+'''
- **Q392 — TRANCHÉE (Tom, v133)** : sortir du mode dessin sans poser = un ✕ dans le contour de l'encart, à l'emplacement de « ✕ FERMER » ;
  le dessin en cours est gardé ; « Quitter le dessin ». Q394 et Q395 : validées (gomme 10 · 18 · 30, fond par défaut, Index et Fil gardent la dalle,
  le dessin d'un Cercle hors de son partage).
- **Q396 — OUVERTE (C-058, bloquant)** : la Toile qui ne répond plus au doigt n'est PAS reproduite (vingt mondes, trois dalles, vrai doigt :
  21/21). Il me faut le chemin : quel monde, à quel zoom, avec ou sans Ma Parole !, après quel geste (retour du Studio, pincement, plantation).
- **Q397 — OUVERTE (C-059)** : « le bas des fiches en clair » — mesuré, Promi, Chiche et Cercle ont déjà le même corps en clair, et aucun
  filet n'y est peint autour des disques ni sous le trait. Une capture de ce que Tom voit est nécessaire. Rien n'a été modifié.
- **Q398 — OUVERTE (C-057)** : la capture du Studio jointe au lot v133 n'est pas arrivée. Le défaut trouvé et corrigé : à la deuxième ouverture,
  le nom de la palette passait au-dessus de la grille et un second nom restait dessous. Est-ce celui-là ?
- **Q399 — À VALIDER (C-050)** : `?bleu=N` recalcule aussi « Ma Parole ! » (3:1) et la phrase lilas (4,5:1) sur le bleu choisi — les deux règles
  décidées en v131 et v132, appliquées. Sans cela elles tombaient sous leur seuil sur quatre candidats sur cinq.
- **Q400 — À VALIDER (C-042)** : la rangée centrée coûte 12 pt à la surface de dessin (754 → 742). Un dessin d'avant garde tous ses traits.
- **Q401 — À VALIDER (C-061)** : la ligne ajoutée à la page de l'offre, « Douze mondes de plus, les couleurs du dessin », passe à deux lignes ;
  sur le mur du dessin, les teintes floutées sont celles de la palette (l'encre, floutée, faisait une tache sous la phrase).
- **Q402 — OUVERTE (C-062)** : le coefficient de variation ne baisse pas avec le nombre de dalles. Ce que Tom voit comme monotone est peut-être
  la taille ABSOLUE (à 40 dalles, toutes petites) ou le monde (Pochade : des taches de même famille). À dire avant de choisir un mécanisme.
'''
ecrit('QUESTIONS.md',Q)
# ── ETAT-DES-LIEUX
E=lit('ETAT-DES-LIEUX.md')
a=[l for l in E.split('\n') if l.startswith('- **v132 (5 oct.)**')][0]
E=E.replace(a,a+'''
- **v133 (6 oct.)** — Studio : le menu des palettes à la 2e ouverture (`posePals`, `redteam_palettes`), Primesautier en tête ; les 18 phrases des murs (C-063) ; bleu provisoire `#1A52F0` et `?bleu=1…5` (C-050) ; mode dessin : ✕ de sortie, 16 pt, rangée centrée, couleurs dans Ma Parole ! (`redteam_dessin` 79/79) ; « Importer une photo » ; planches `planche-v133/` (symboles, tailles, murs). **Non reproduit : la Toile sourde au doigt (C-058). Non modifié : le bas des fiches en clair (C-059).**''')
E=E.rstrip('\n')+'''
| v133 | **Le bleu du corps sombre Promi (C-050) — à CHOISIR** | `redteam_decisions` ; tableau des contrastes au rapport | `app.html?bleu=1` … `?bleu=5` : fiche Promi et page + d'un Promi en sombre, le Peaufiner, un mur ; la valeur est écrite en bas de l'écran |
| v133 | Le menu des palettes du Studio (C-057) | `redteam_palettes` 28/28 | ouvrir le Studio, le fermer, le rouvrir, ouvrir les palettes : la grille, puis le nom, puis la jauge ; Primesautier en premier |
| v133 | La Toile au doigt sous les vingt mondes (C-058) — NON REPRODUIT | `redteam_toucher` 21/21 | sous Ramage, toucher trois dalles ; si rien ne s'ouvre, noter ce qu'on venait de faire (Q396) |
| v133 | Le mode dessin (C-042, C-056, C-061) | `redteam_dessin` 79/79 | ✕ en haut à droite : on sort, le dessin est gardé ; tailles et couleurs à 16 pt de la rangée ; la rangée centrée en bas ; sans Ma Parole ! : COULEUR floutée, la phrase monte |
| v133 | Les dix-huit phrases des murs (C-063) | `redteam_murs` 28/28 · `redteam_maparole` 14/14 | toucher un mur dix-huit fois : les phrases dans l'ordre, les mots en orange |
| v133 | « Importer une photo » ; les trois symboles (C-060) | `redteam_photo_menu` 20/20 ; `planche-v133/symboles` | le menu du bouton photo ; la planche : A, B ou C |
'''
ecrit('ETAT-DES-LIEUX.md',E)
# ── portage
P=lit('portage/A-INTEGRER.md').rstrip('\n')+'''
- **v133** : le corps sombre d'un Promi est PROVISOIRE (`#1A52F0`, C-050 — Tom choisit sur l'iPhone par `?bleu=`) : ne pas le figer en Swift
  avant son choix ; « Ma Parole ! » sur ce corps et la phrase lilas en dérivent (3:1 et 4,5:1, même teinte OKLCH). Mode dessin : surface
  390 × 742, rangée centrée entre la surface et le bord bas utile (`safeAreaInsets.bottom`), déploiements à 16 pt ; un ✕ « Quitter le dessin »
  dans le contour ; les teintes du trait et du fond sont dans Ma Parole ! (sans elle : l'encre du mode sur le champ de la nature). Les murs :
  dix-huit phrases, chacune avec sa liste de mots en orange (`TEXTES` dans `lot-V104-MURS`).
'''
ecrit('portage/A-INTEGRER.md',P)
# ── MA-PAROLE-PHRASES
M=lit('MA-PAROLE-PHRASES.md')
T=[('Eh non. Mais avec Ma Parole !, oui.','« Ma Parole ! »'),('La solution commence par Ma et finit par Parole !','« Ma » et « Parole ! »'),('Toujours non. Ma Parole !, toujours oui.','« Ma Parole ! » et « oui »'),('Je vois bien que ça te titille. Ma Parole ! aussi.','« Ma Parole ! »'),('Tiens tiens, on dirait que ça commence à t’intéresser…','aucun'),('Tiens tiens. Vous ici.','aucun'),('Tu sais où trouver Ma Parole ! maintenant.','« Ma Parole ! »'),('On maintient cette position officielle, alors ?','« officielle »'),('Allons bon. Nous y voilà à nouveau.','aucun'),('Entre nous, le mystère s’amenuise.','« mystère »'),('Les pourparlers se prolongent, je vois.','« pourparlers »'),('Tu peux continuer. Je tiens le registre.','« registre »'),('Ici, tout restera entre nous.','aucun'),('Je commence à soupçonner une stratégie.','« stratégie »'),('On pourrait presque en faire une tradition.','« tradition »'),('Regarde-nous, avec nos petites habitudes.','« habitudes »'),('Dis donc, tu viendrais presque pour moi.','« moi »'),('On se retrouve ici tout à l’heure ?','aucun')]
bloc='''> **⚑ v133 (6 oct. 2026) — CETTE LISTE EST REMPLACÉE.** Tom a réécrit les phrases (C-063) : dix-huit, mot pour mot, dans cet ordre, avec la
> même rotation (dans l'ordre, puis au hasard sans répéter la précédente ; 14 jours). Les 21 phrases ci-dessous sont l'état de v132, gardé
> pour l'histoire. Un mur de plus depuis v133 : les teintes du mode dessin, sans Ma Parole ! (C-061).
>
> | n° | la phrase (v133) | en orange |
> |---|---|---|
'''+'\n'.join('> | %d | %s | %s |'%(i+1,p,o) for i,(p,o) in enumerate(T))+'\n\n'
k=M.index('\n',M.index('# MA-PAROLE-PHRASES.md'))+1
ecrit('MA-PAROLE-PHRASES.md',M[:k]+'\n'+bloc+M[k:])
