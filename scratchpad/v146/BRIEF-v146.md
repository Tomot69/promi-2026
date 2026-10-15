

<pasted_content id="16af">
LOT v146 — RETOURS iPHONE DE TOM SUR v145

Nouvelle adresse iPhone : http://192.168.1.128:8752/app.html (avec la marque : ?mesure=1). La marque v145 · d18326d est validée par Tom. C-117 passe « validé ».

À inscrire dans CLAUDE.md, en tête des règles de design (C-130) :
RIEN DE CHEAP, RIEN DE BORING, TOUT ARTY. Chaque transition, chaque texte, chaque apparition est dessiné. Est refusé d'office : tout ce qui « arrive d'un coup » ; le flou, le dégradé ou le fondu comme moyen d'apparition ; toute forme géométrique parfaite qui se translate ; tout texte noir sur blanc sans hiérarchie.
JAMAIS de contour ni de liseré autour des lettres, nulle part.
Avant de livrer, une question : est-ce qu'un illustrateur le signerait ?
Ces chantiers forment la cohérence de l'app. Aucun n'est facultatif, aucun n'est reporté sans l'accord de Tom. Tous ses mots sont là pour une raison : chaque subtilité ci-dessous est une exigence.

Ordre : §1 → §2 → §3 → §4 → §5 → §6 → §7 → §8 → §9 → §10 → §11 → §12 → §13 → §14 → §15 → §16 → §17 → §18.
Les règles de travail du brief restent (R-A à R-F), y compris la preuve banc_tom et les pages de variantes pour le design.

════════════════════════════════
§1  C-122 (nouveau) — AJOUTER UNE PERSONNE, PAGE + ET FICHE (bug bloquant)
════════════════════════════════
Tom : toucher « ajouter une personne » ouvre un second encart de saisie, caché sous le clavier et laid. Surtout, il n'y a pas de validation : on tape le nom, on ne peut jamais l'ajouter. Tom n'a donc pas pu tester les parts (C-115).
- Supprime l'encart supplémentaire.
- Toucher la zone en pointillés ouvre le clavier dans cette zone même, comme pour les autres champs. Le texte s'écrit là, et nulle part ailleurs.
- Validation : un « + » (décision de Tom, pas un « v »), à droite du nom, sur la même ligne.
  - Il n'a pas d'encart.
  - Il est dans une couleur qui contraste, l'orange de l'app #FB4C0D (voir la règle de l'orange, §5), pour qu'il soit visible et qu'on le comprenne sans explication.
  - Il est en gras, et sa hauteur est celle des majuscules ou des lettres hautes du texte saisi.
  - Il paraît dès le premier caractère.
  - La touche Retour valide aussi.
- Le nom validé se pose dans la fiche, et une nouvelle ligne en pointillés s'offre pour la personne suivante.
- Rien ne passe sous le clavier : la fiche défile pour garder la ligne visible.
Juge : redteam_ajout_personne (toucher, taper, valider avec le + puis avec Retour ; 1, 2 et 4 personnes ; ligne visible au-dessus du clavier ; aucun second encart). Rejoue ensuite redteam_part sur ce vrai chemin, pas avec ?parts=1.

════════════════════════════════
§2  C-131 (nouveau) — MÊME TOILE EN CLAIR ET EN SOMBRE, DANS TOUS LES MONDES
════════════════════════════════
Tom a un doute : le moodboard montre une dalle différente selon qu'on est en clair ou en sombre.
La règle est absolue : c'est EXACTEMENT la même Toile en clair et en sombre (mêmes dalles, même disposition, mêmes formes, mêmes tailles, mêmes graines), dans les 20 mondes et partout où une Toile s'affiche (accueil, partage, moodboard, onboarding). Seules les couleurs du thème changent.
- Vérifie les 20 mondes, avec 1, 5, 25 et 50 paroles. Compare les géométries (positions des germes, polygones) et pas les pixels.
- Vérifie le moodboard en particulier. S'il diffère, dis d'où vient l'écart (une page de démonstration avec ses propres graines, ou un vrai défaut) et corrige.
Juge : redteam_clair_sombre (géométrie identique au point près). Rapport : un tableau monde par monde, pour rassurer Tom.

════════════════════════════════
§3  C-135 (nouveau) — L'AURA : LA SPHÈRE TARDE 1 À 2 SECONDES
════════════════════════════════
Quand on ouvre l'Aura, la place reste vide une à deux secondes avant que la Pelote paraisse. C'est un bug : il faut qu'elle soit là dès l'ouverture.
- Mesure d'abord sur banc_tom, et sur iPhone avec ?mesure=1 : création du contexte graphique, compilation des shaders, génération des poils.
- Pistes : préparer la Pelote quand l'app est au repos après le démarrage (sans gêner la Toile, C-112), garder le contexte en vie entre deux ouvertures, compiler les shaders d'avance.
Cible : la première image de la Pelote se dessine dans l'image même où l'Aura s'ouvre. À la première ouverture comme aux suivantes.
Juge : redteam_aura_latence (délai entre le toucher et la première image de Pelote ; 1re, 2e et 5e ouverture).

════════════════════════════════
§4  C-094 rouvert (2e récidive) — LE GUIDE : DES FLAQUES
════════════════════════════════
Tom, sur l'app : « Le flou au passage de l'icône Studio à l'icône +, c'est nul. Ça arrive tout d'un coup, puis ça se fixe sur le Studio et ça se translate sur un axe horizontal. »
Tom, sur promi-guide-variantes.html : « pourri de chez pourri ». Trois défauts : des contours colorés autour des lettres des phrases (à retirer, JAMAIS ça) ; des zones de flou qui ne sont pas sa demande ; un cercle parfait autour du Studio, qui montre l'Aura et une grande part de l'encart, si bien que le focus n'est pas clair. Même défaut sur le +.

Ce que Tom veut, étape par étape :
4.1 COUVERTURE (seul moment où tout l'écran est concerné). Des zones abstraites et aléatoires de flou paraissent, grossissent, se développent au hasard jusqu'à se rejoindre en se touchant, puis couvrent tout l'écran.
    Image de Tom : de l'eau qui monterait par en dessous dans du sable, vue du dessous. Des flaques naissent dans les creux, au hasard. Elles grossissent, leurs contours sont abstraits, elles se touchent quand elles sont pleines.
4.2 LA PHRASE paraît alors, sans aucun contour. Ses lettres se tracent selon les règles de §13 (C-125). Ses mots-clés suivent §11.7.
4.3 LE STUDIO. La zone nette autour de l'icône Studio paraît avec le MÊME effet de flaques, plus petit, sur le Studio seulement.
    Sa forme finale est un entourage LÉGÈREMENT imparfait : pas un cercle parfait, pas une forme déchiquetée. Il est serré sur l'icône Studio et son mot, et il les marque nettement.
    On ne doit voir ni l'Aura ni l'encart. Le focus est évident.
4.4 Puis cette zone DISPARAÎT sur elle-même, par le même effet joué à l'envers : les flaques nettes se résorbent.
4.5 LE + : la même chose (apparition en flaques, entourage légèrement imparfait serré sur le + seul, puis disparition en flaques à l'envers).
4.6 FIN (décision du chef de chantier, dans la logique de Tom) : le flou se retire de tout l'écran par l'effet de 4.1 joué à l'envers. Les flaques se vident.
Rythme : pas trop rapide, pour qu'on lise les flaques. Fluide, pas lent, plutôt vif. L'effet ne doit pas prendre l'attention, mais il doit être beau.
Départ à régler avec Tom : couverture entre 1,2 et 1,6 s, ouverture du Studio entre 0,6 et 0,8 s, fermeture idem, même chose pour le +.
Interdit : disque ou ellipse parfaits, translation, tout ce qui arrive d'un coup, contours sur les lettres.
Technique : garde l'accueil flouté à l'avance et le masque dessiné à chaque image. Le masque devient un champ de flaques : bruit seuillé qui monte, ou métaballes à graines aléatoires, avec un tirage par étape. L'entourage final de 4.3 et 4.5 se calcule à partir de la boîte de l'icône et de son mot, avec une marge régulière et une irrégularité de bord contenue.
Écris d'abord la cause de la récidive : la demande portait sur une matière vivante, aléatoire et ciblée ; la livraison a été une découpe géométrique trop large qui se déplace.
Livre-le dans l'app, avec une vue ralentie au quart : promi-guide-variantes.html?flaques=1. Supprime les anciennes variantes A, B et C de cette page.

════════════════════════════════
§5  C-121 (nouveau) — L'ORANGE : LE + DE L'ACCUEIL, ET UNE RÈGLE
════════════════════════════════
Tom : le + de l'accueil est central mais invisible.
Décision du chef de chantier : le signe + passe en orange #FB4C0D, en clair et en sombre. Le signe seul, sans fond ni cercle.
Règle à inscrire dans CLAUDE.md : l'orange marque les points de départ d'une action, et rien d'autre. Ce sont le + de l'accueil, le + de validation d'un nom (§1) et le départ de la flèche du trait sur toutes les fiches (§8). C'est ce qui l'empêche de passer pour de la décoration.

════════════════════════════════
§6  C-119 (nouveau) — SUPPRIMER « ENREGISTRER LA TOILE » DE L'ACCUEIL
════════════════════════════════
Tom ne l'avait pas demandé. Supprime de l'encart du haut de l'accueil le bouton, son icône et tout ce qui va avec : c'est du bruit.
On enregistre sa Toile depuis la page Partager : on va jusqu'au bout, et là il y a le choix des réseaux sociaux, enregistrer en fichier, en photo, etc. Vérifie que ce chemin enregistre bien (photo et fichier).

════════════════════════════════
§7  C-120 (nouveau) — NOMS DES ICÔNES DE L'ACCUEIL EN BLEU
════════════════════════════════
Studio, Aura, Index et Fil, sous les icônes, prennent le bleu FONCÉ du I clignotant de PROMI (la valeur la plus foncée de son clignotement ; lis-la dans le code).
En clair : appliqué. En sombre : vérifie le contraste. Applique si c'est lisible ; sinon garde l'actuel et montre-le à Tom avec une capture.

════════════════════════════════
§8  C-132 et C-133 (nouveaux) — LES FICHES : LA VERSION SOMBRE PARTOUT, LA FLÈCHE EN ORANGE
════════════════════════════════
C-132. Toutes les fiches (Promi, Chiche, Cercle) prennent en mode CLAIR exactement la version qu'elles ont en mode sombre. Tom la trouve plus belle. La fiche est donc la même dans les deux modes.
Cela remplace la règle « fiches en #F7F0DE » de CLAUDE.md : mets-la à jour.
- Promi : la fiche sombre, telle qu'elle est (voir la capture de Tom : haut en #82AEF8 avec les fleurs, trait en vague pointillée, fond du bas en #0E78F2 sous le trait).
- Chiche : même construction. Le FOND DU BAS, sous le trait et sa flèche, prend le corps sombre du Chiche, #7C3F58.
- Cercle : pareil, fond du bas en #5D4978.
- Vérifie que chaque fiche est identique en clair et en sombre : planter, tenir, tenue, reçue, à plusieurs.
C-133. Le départ de la flèche du trait (le chevron où l'on commence à tracer, entouré par Tom sur sa capture) passe en orange #FB4C0D. Sur TOUTES les fiches, en clair et en sombre, et quel que soit le design choisi dans Peaufiner.
Juge : redteam_fiches_theme (fiches identiques en clair et en sombre, fond du bas des trois natures, flèche orange dans toutes les combinaisons de design).

════════════════════════════════
§9  C-134 (nouveau) — PEAUFINER RESTE OUVERT
════════════════════════════════
Aujourd'hui, un choix fait dans Peaufiner (sur une fiche, ou à la création dans la page +) referme Peaufiner et ramène d'un coup à la Toile. C'est une erreur.
- Un choix dans Peaufiner s'applique sur place. Peaufiner reste ouvert : on est dans une page de réglages, on y coche et on y modifie des choses.
- On en sort par un glissement du haut vers le bas de l'écran. Peaufiner redescend dans son bandeau normal en bas, et on revient à la fiche (ou à la page +).
- Plus JAMAIS de retour à la Toile depuis Peaufiner.
Juge : redteam_peaufiner (plusieurs choix d'affilée sans fermeture ; glissement vers le bas ; retour à la fiche ou à la page + ; jamais à la Toile).

════════════════════════════════
§10  C-088 rouvert à la demande de Tom — RITOURNELLE : LA RÈGLE DES 75 %, LE BUG À 1 DALLE
════════════════════════════════
Tom : « À 1 dalle, la Toile est vide, il y a juste un texte qui flotte. » C'est un bug (déjà présent à l'origine selon ton rapport v145), à corriger.
« À 3 dalles, on ne voit même pas 10 % de chaque dalle. C'est joli, mais dézoome légèrement. »
Règle (Tom) :
- De 1 à 9 paroles, deux conditions :
  - chaque dalle de parole est visible sur au moins 75 % de sa surface ;
  - les dalles de paroles couvrent au moins 75 % de l'écran.
  Pas de couronne de dalles vides autour, comme dans la version « ultra dézoomée » refusée.
- À partir de 10, AUCUN saut : pas de « pof », pas de gros dézoom d'un coup. Le dézoom est progressif, parole après parole. Il part de l'échelle de 9 et continue d'appliquer la règle des 75 % autant que la place le permet.
- On garde le caractère arty du cadrage restauré (grandes formes, motifs). On dézoome juste assez pour respecter les 75 %.
Juge : redteam_ritournelle complété. Les deux cotes sont mesurées de 1 à 15 paroles, et l'écart d'échelle entre deux nombres de paroles consécutifs est borné, notamment entre 9 et 10. Planche de 1 à 15.
Q496 suit la décision de §17.

════════════════════════════════
§11  C-123 et C-124 (nouveaux) — L'ONBOARDING : DALLES ET TEXTES
════════════════════════════════
C-123 Les dalles colorées ne doivent pas arriver toutes d'un coup. Le rythme est vif, mais on voit une Toile organique qui évolue au fil des éléments, avec des dalles de tailles, de couleurs et de formes variées.
- Apparition : une à une ou par petits groupes. Le Voronoi se réorganise à chaque naissance, et les voisines se déforment pour faire place : une Toile vivante, pas un patchwork qui se remplit.
- Disparition : vive, avec le même effet organique. Le Voronoi se résorbe dalle par dalle.
- Interdit : flou, dégradé, fondu, tout ce qui arrive ou part d'un coup.
Vidéo ralentie et planche de 8 images.

C-124 Les mots de Tom restent les siens. La seule modification de texte est celle de 11.4, demandée par lui. Tu peux couper ses phrases en lignes et les hiérarchiser, sans changer un mot.
Les COULEURS de ce paragraphe valent en mode CLAIR seulement, le mode par défaut à la première ouverture. En SOMBRE, les couleurs actuelles restent, sinon ce serait illisible. Les tailles et la mise en page valent dans les deux modes.
11.1 « "Prénom", donc. » et, dessous, « Petite ou grande promesse, elle compte » (textes exacts du code).
     Grossis-les nettement, entre 75 et 85 % de la taille de la phrase de promesse. La phrase de promesse reste telle quelle, n'y touche pas. Plus gros deviendrait illisible : reste dans la plage.
     Les deux en violet foncé de l'app, #291547.
11.2 Page suivante : même traitement, plus gros, en violet foncé. Promi, Chiche et Cercle gardent leurs vraies couleurs, comme aujourd'hui : n'y touche pas.
11.3 Ce texte est long et ennuyeux. Rends-le vivant sans changer ses mots : lignes courtes, mots-clés dans la police Promilate (la police de titre de l'app ; vérifie le nom exact), une hiérarchie de tailles. Le noir sur blanc, c'est fini.
11.4 « C'est planté. » devient « Promi planté ! » (Tom : on célèbre sans gamification ; plus de « C'est »).
     C'est une exception nommée au « ! », à inscrire dans CLAUDE.md à côté de « Ma Parole ! ».
     « Promi » en gros, en bleu Promi (#0E78F2 en clair).
     Juste dessous, la phrase qui donne le ton (« ton premier promi sur la Toile », avec les mots exacts du code).
     Puis RIEN d'autre en dessous, pour l'instant : le reste vient au toucher, tracé (§13).
     Décision du chef de chantier : pas de « Bravo » en plus, « Promi planté ! » porte déjà la célébration.
11.5 Position : tout le bloc, de « Promi planté ! » jusqu'à « La suite t'appartient. », remonte d'au moins 1 cm réel (au moins 60 pt sur l'iPhone 16e). Il passe AU-DESSUS des dalles du dessous, qui sont parfaites, au lieu de les recouvrir comme aujourd'hui.
     Laisse un petit espace vide entre le bas du texte et le haut des dalles.
     Ne monte pas trop haut : on garde l'effet décalé du haut, qui est beau.
11.6 « La suite t'appartient. » reste. La phrase EN DESSOUS n'est pas claire selon Tom : montre-la-lui et inscris-la dans QUESTIONS.md, texte à réécrire par Tom. Tu ne la réécris pas.
11.7 Les deux phrases du guide (Studio et +) : plus grosses, sans aucun contour.
     Mots-clés en Promilate et en couleur : « Studio » et « monde » dans la phrase du Studio ; le mot qui nomme l'action dans la phrase du +. Montre le choix à Tom.
     En clair : texte en #291547, mots-clés en #0E78F2, mots de nature dans leur couleur.
Juge : redteam_onboarding_texte (tailles relatives ; couleurs en clair ; sombre inchangé ; aucun mot de Tom modifié hors 11.4 ; position au-dessus des dalles avec l'espace demandé ; aucun contour sur les lettres).

════════════════════════════════
§12  C-126 (nouveau) — LA PAGE DU PREMIER PROMI DANS L'ONBOARDING
════════════════════════════════
Demande de Tom, pour le mode clair :
- « Tracer pour planter » (en Promilate) en vert foncé #00341A ;
- le départ de la flèche en orange #FB4C0D ;
- les pointillés du trait non tracé en noir.
Ce que tranche le chef de chantier, en lien avec §8 :
- La flèche orange s'applique dans tous les cas (C-133).
- Pour le texte et les pointillés : si cette page utilise la fiche, qui est désormais la version sombre dans les deux modes, du vert foncé ou du noir sur le fond #0E78F2 deviendrait illisible. Dans ce cas, garde leurs couleurs actuelles, montre les deux versions à Tom en capture et inscris la question dans QUESTIONS.md.
- Si la page a un fond clair à elle, applique la demande telle quelle.

════════════════════════════════
§13  C-125 (nouveau) — LE TRACÉ DES LETTRES
     Module réutilisable. Tom décidera plus tard, avec une extrême parcimonie, où l'employer ailleurs (célébration d'une fiche, etc.).
════════════════════════════════
Usage immédiat :
- les textes de l'onboarding qui paraissent au toucher ;
- les phrases du guide (§4.2).
En clair comme en sombre : le mouvement vaut partout, seules les couleurs changent selon le mode.

Déclenchement : on touche n'importe où, simple et sans friction, et le passage suivant se trace. On ne fait plus « un paragraphe qui apparaît d'un bloc dans un flou ».
Au départ, il n'y a aucun texte. Puis les lettres du premier mot se tracent, puis celles du second, et ainsi de suite.

Le trait :
- Chaque lettre se dessine par un trait NET, comme un rouleau à bord franc. Le front qui avance est une coupe nette, perpendiculaire au chemin, même dans les arrondis.
- Pas de flèche, pas de curseur, pas de pointe : seules les lettres se tracent.
- Au ralenti extrême (enregistrement d'écran), on voit le trait partir de rien, avec des extrémités nettes. Exemple de Tom : un « l » minuscule part de rien par le bas ou par le haut, et son trait vertical est net à ses deux bouts.
- À la fin, la lettre est EXACTEMENT le glyphe de la police Gilbert de l'app (téléchargée), avec la couleur et la taille de l'app.
- Interdit : fondu, dégradé, opacité intermédiaire, trait effilé, apparition abstraite, onde de bas en haut ou de haut en bas, glitch à la Matrix, contour, tout le texte d'un coup.

Les chemins (analyse glyphe par glyphe dans le fichier Gilbert ; vectorise la police, par exemple avec opentype.js ; trace pour chaque glyphe une ligne médiane qui suit la logique d'un tracé ; le glyphe plein est dévoilé par un masque tracé le long de cette ligne, à bouts plats, plus large que le trait du glyphe) :
R1  On évite de revenir en arrière, sauf si c'est impossible. Un repassage sur une partie déjà tracée est invisible (rien de neuf ne paraît) et ne dure qu'un instant.
R2  Un mouvement vers la gauche est permis, et même beau (un arrondi, une droite), s'il s'enchaîne. Chaque lettre FINIT vers la droite, pour enchaîner sur la suivante ou sur le point final.
R3  Une lettre commence du côté où la précédente a fini : en haut si elle a fini en haut, en bas si elle a fini en bas. Quand le glyphe le permet, elle finit du côté opposé.
R4  Exemple de Tom, le « h » minuscule. D'abord la barre verticale, dans un sens ou dans l'autre. Il ne peut finir qu'en bas à droite, après le pont de droite.
    S'il commence en haut : il descend la barre, revient sur ses pas (invisible un instant) jusqu'à la naissance du pont, trace le pont puis descend la jambe droite.
    Un « H » majuscule peut finir en haut ou en bas : on choisit selon R3.
R5  Lettres en plusieurs morceaux (i, j, t, f, x, accents, cédille). Décision du chef de chantier : le saut d'un morceau à l'autre est instantané et invisible. L'ordre des morceaux est choisi pour que le dernier finisse à droite, du côté qu'exige R3.
Le résultat est arty mais logique, d'une logique Bauhaus. Il peut fasciner celui qui veut s'y laisser hypnotiser, sans jamais gêner la lecture de la lettre.

Vitesse : nettement plus rapide que quelqu'un qui survole le texte. Départ : 40 à 60 caractères par seconde, réglable, que Tom ajustera sur iPhone. Le texte n'apparaît jamais d'un bloc.

Livrables :
- promi-trace-lettres.html : tout l'alphabet (a–z, A–Z, é è ê ë à â ç ù û ô î ï, chiffres, . , ' ! ? « » …) ; vitesse ×1, ×0,25 et ×0,05 ; un mode qui montre le chemin de chaque glyphe (départ, arrivée, côté haut ou bas) ; les textes de l'onboarding tracés.
- Juge redteam_trace_lettres :
  - la dernière image est identique au texte statique, au pixel près ;
  - aucune opacité intermédiaire au front, hors anticrénelage ;
  - chaque glyphe finit à droite (R2) ;
  - R3 est respectée quand le glyphe le permet, avec la liste des exceptions ;
  - le repassage est minimal (R1).
Montre la page à Tom AVANT de brancher le module dans l'onboarding et le guide.

════════════════════════════════
§14  C-118 — TENIR : LA VARIANTE A, CORRIGÉE
════════════════════════════════
Tom choisit la variante 1 (A, « La marée ») pour le trait, avec ces corrections :
- Plus de liseré, de filet, ni de jour ouvert sous le trait.
- Le trait EST le fond du bas en mode célébration ; réduis-le si tu veux.
- Aucune séparation entre le trait et le vert de même couleur qui se remplit au-dessus : c'est une seule matière.
- Ce qui descend (le vert en rideau) avance EN FLAQUES, dans le langage de §4, mais vite, à la même vitesse que le rideau actuel, vers le bas.
L'instant reste à environ 2 s. Les interdits tiennent : ni fondu, ni transparence, ni dégradé ; la couleur avance par aplats en flaques.
Intègre-le dans l'app, pour Promi, Chiche et Cercle, sur la fiche sombre devenue commune (§8). Supprime les variantes B et C.
Juge : redteam_tenir (aucune séparation visible entre le trait et le vert ; durée ; flaques vers le bas ; pas de changement d'écran) et redteam_fluide (C-102) rejoué sur ce nouveau mécanisme.

════════════════════════════════
§15  C-116 (suite) et C-128 (nouveau) — COMMENTAIRES, NOMS, VISAGES
════════════════════════════════
15.1 Commentaires (C-116). Le texte du commentaire est l'important et il se lit mal : grossis-le. Il a la même taille que les noms. Regarde comment les réseaux sociaux affichent leurs commentaires, puis trouve le style propre à Promi.
15.2 Noms (C-128). La règle vaut PARTOUT où un nom apparaît, sauf dans le sélecteur, qui reste tel quel :
     - le pseudo en entier s'il tient ;
     - sinon coupé à 6 lettres et suivi d'un « . » ;
     - si deux personnes ou plus partagent le même début, on ajoute TOUJOURS les caractères suivants jusqu'au premier qui les distingue (Christo. / Christi.) ;
     - toucher un nom mène à la fiche de la personne.
15.3 Image de profil : petite, ronde, à gauche du nom, SANS cerclage, anneau ni bord (c'est du bruit). Sans photo, on garde le repli actuel, sans cerclage. Le texte est à droite.
15.4 Date : intelligente et sobre, dans le style de Promi. « à l'instant », « il y a 5 min », « hier », puis « 12 oct. ». Au-delà d'un an, l'année.
Juges : redteam_noms (abréviations, doublons, liens, sélecteur inchangé) ; redteam_commentaires complété (taille, image, date).

════════════════════════════════
§16  C-129 (nouveau) — PAS D'EMOJI DANS PROMI
════════════════════════════════
Les emojis sont bloqués partout où l'on écrit (paroles, noms, commentaires, prénom de l'onboarding, collages), SANS le dire et sans friction.
Le web ne peut pas retirer la touche emoji du clavier iOS. Donc un emoji tapé ou collé n'est tout simplement pas inséré : rien ne s'affiche, aucun message, rien n'est noté.
Filtre les pictogrammes étendus, les sélecteurs de variante, les jonctions (ZWJ), les teintes de peau, les drapeaux et les touches numérotées. Même filtre à l'enregistrement (portage/ et règles Firebase).
Juge : redteam_emoji (taper, coller, mélanger texte et emoji : le texte reste, l'emoji disparaît, aucun message).

════════════════════════════════
§17  DÉCISIONS DU CHEF DE CHANTIER SUR LES QUESTIONS DE v145
════════════════════════════════
- Q485 : accepté, planter à plusieurs plante UNE seule parole.
- Q486 : Chiche à plusieurs, chaque destinataire a sa part. Cercle, chaque membre engagé a sa part. Promi à plusieurs, seul l'auteur a la part, et les autres voient quand il a tenu.
- Q487 : sur la fiche, initiales seulement sous les parts TRACÉES ; les parts non tracées restent anonymes (grille, question 3). En touchant le trait, la liste montre tout le monde, avec une date pour ceux qui ont tracé, sans mention du genre « pas encore ».
- Q488 : « Un mot… » reste provisoire. C'est Tom qui écrit le texte.
- Q496 : on garde le cadrage de Ritournelle et on répare le déplacement sans y toucher. Si c'est impossible, le déplacement est désactivé dans ce cas, sans message.
- Fiche d'un Cercle : la ligne « Un mot… » se place juste au-dessus de « + Planter dans le Cercle ».
- CHANTIERS.md est à corriger :
  - C-105, C-106, C-107 et la trace de la Pelote (C-083) sont déjà validés par Tom ;
  - C-109 est remplacé par C-110 (validé) ;
  - C-108 est remplacé par C-115.

════════════════════════════════
§18  RESTES
════════════════════════════════
- C-112 (la Toile saccade) : Tom n'a pas encore mesuré sur sa Toile avec ?mesure=1. Il reste ouvert ; intègre la mesure dès qu'elle arrive.
- C-102 : rejoué avec le nouveau tenir (§14).

Rapport : comme d'habitude, avec une section par C-xxx, dans l'ordre de ce lot.
Vidéos ralenties pour C-094, C-118, C-123 et C-125.
Tableau monde par monde pour C-131.
Mesure de la latence avant / après pour C-135.
</pasted_content id="16af">
