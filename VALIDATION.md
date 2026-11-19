# VALIDATION — ce qui reste à voir sur l'iPhone (v207, 17 nov. 2026)

**Validés en bloc par Tom (17 nov.)** : les 68 chantiers « validés par l'usage » et les 20 de méthode, et C-288, C-289 — 90 au registre.
**Devenus des spécifications de tests automatiques de la vraie app** : 42 chantiers d'états rares (ARCHITECTURE.md, « Les tests ») — marqués au registre.
**Reste : les points à vérifier par Tom** (11 à 14 : la séance du 17 nov. ; 16, 17 et 19 à 24 : v210, dans l'app « Promi preuve » ; 15 et 18 validés le 18 nov.), une ligne chacun (13 chantiers : trois lignes en portent deux). Adresse : `http://<IP>:8752/app.html`.

| # | Chantier | Comment y arriver | Ce qu'on doit voir |
|---|---|---|---|
| 1 | C-282 | Page +, toucher le titre, taper la première lettre aussitôt (même pendant que l'exemple se trace) | l'exemple part en 150 ms, jamais un éclair de l'exemple entier |
| 2 | C-258 | Planter une parole, l'effacer aussitôt (Peaufiner › Supprimer), recharger | elle ne revient pas |
| 3 | C-160 | `?jour=+30`, ouvrir une parole datée | « EN COURS · 12 OCT. », la date seule ; REPORTER (Fil) compte depuis aujourd'hui |
| 4 | C-136 | Réglages › Tout effacer, puis recharger six fois | la Toile vide n'est jamais toute colorée |
| 5 | C-195 | Réglages › Tout effacer | la feuille, puis l'aplat de l'onboarding, « Toi, c'est … ? » |
| 6 | C-101 | Sur la Toile, appui de 0,8 s sur une dalle, glisser, lâcher, recharger | la dalle suit le doigt, sa place est gardée |
| 7 | C-051, C-091 | Bouton photo d'une fiche › Importer une photo, puis toucher la bande | la photo en entier sur fond plein, une seule icône « Enregistrer » |
| 8 | C-042, C-056 | Bouton photo › Dessiner | la rangée d'outils en bas, ✕ sort sans poser, le dessin en cours est gardé |
| 9 | C-170, C-190 | Studio › un monde payant › « Adopte ce design » › « Plus tard », puis l'achat simulé | « Plus tard » ferme sans rien acheter ; après l'achat, le Studio net, aucune ancienne Toile |
| 10 | C-249 | Ne plus toucher l'iPhone pendant 75 s | la veille part à 75 s, pas avant |
| 11 | C-296 | Page +, toucher le verbe trois fois (« Je me promets » → « Je promets à qui ? » → « qui ?, promets-moi » → « Je me promets ») | aucun rectangle pointillé ne reste sur « Je » : le filet de « qui ? » s'amincit pendant qu'il part |
| 12 | C-297 | Tenir une parole, puis faire défiler la fiche aussitôt (pendant le vert) | la fiche défile au doigt, le vert remonte, rien ne passe sur l'en-tête |
| 13 | C-298 | L'Aura, regarder la Pelote 10 s | elle tourne 1,5 fois plus vite (un tour en 67 s) |
| 14 | C-294 | L'Aura, en clair | « PARTAGER MA PELOTE » sur le même fond crème que l'encart « Aura · X » |
| 15 | C-299 | Dans « Promi preuve », ouvrir chaque page (accueil, une fiche, l'Index, le Fil, l'Aura, le Studio, les Réglages, Partager, la page +) | tout est comme avant v208 ; seul l'encart du haut est un demi-millimètre (3 pt) plus bas |
| 16 | C-300 | Dans « Promi preuve », ne plus toucher l'iPhone pendant 75 s, regarder la veille quelques minutes | le fond couvre tout l'écran ; le logo va jusqu'aux bords et aux coins du bas, rebondit sous l'encoche sans jamais la traverser |
| 17 | C-297 | Dans « Promi preuve », tenir une parole, attendre la fin du vert, défiler la fiche lentement puis d'un coup, vers le bas puis vers le haut | le trait s'accroche sous le bandeau et s'aplatit, jamais au-dessus ni en dessous (le relevé part au Mac) |
| 18 | §4 | Dans « Promi preuve », quitter l'app (retour à l'écran d'accueil de l'iPhone) et attendre une minute | la notification arrive ; revenu avant la minute, elle n'arrive pas |
| 19 | C-301 | Ouvrir l'Index, le Fil, l'Aura, les Réglages, Partager, le Studio | le même encart partout (hauteur, marges, titre, X à la même place) ; l'Index exactement comme le Fil, sans compteur ; le « i » de l'Aura centré |
| 20 | C-300 | La veille quelques minutes, en clair et en sombre | le logo 1,5 fois plus rapide, toujours aux couleurs vives exactes de la palette |
| 21 | C-302 | L'Aura, regarder la Pelote une minute ou deux | la direction de rotation change, toujours en douceur, jamais d'un coup |
| 22 | C-303 | Page + d'un Chiche, taper un texte puis Retour | aucun rectangle ne paraît ni ne disparaît d'un coup ; « DÉJÀ PROMIS » descend avec le clavier |
| 23 | C-304 | Page + (Chiche, Promi « à qui ? », Cercle), toucher la place du destinataire | pendant que le menu se déroule, la phrase passe à « moi » ; fermé sans rien changer, elle reste « moi » ; une personne ajoutée, son nom |
| 24 | C-305, §6 | Page + d'un Promi en « promets-moi » ; taper « haïr », « honte », « aller », « oui » puis effacer | « Bruno-Stanislas, promets-moi de … » tient ; « de » / « d’ » juste à chaque mot, en se détraçant puis se traçant |
| 25 | C-297 | Dans « Promi preuve » v211, tenir une parole (Promi, puis un Chiche), attendre la fin du vert, défiler jusqu'en bas en TIRANT au-delà du bout (le rebond), puis remonter | le trait reste accroché à plat sous le bandeau, même au rebond ; jamais au-dessus ni en dessous (le relevé part au Mac) |
| 26 | C-306 | Créer un Cercle (le +, Cercle, un nom, tracer) | un seul Cercle, une seule dalle, une ligne au Fil — plus de « premier Promi » |
| 27 | C-307 | Ouvrir l'accueil, l'Index, le Fil, l'Aura, les Réglages, Partager, le Studio, Vie privée, Ma Parole !, une fiche, la page + | tous les titres des encarts à la même taille, sur une ligne avant le X |
| 28 | C-308 | Ouvrir l'Aura | l'apostrophe de L'AURA en bleu, qui clignote avec le I de PROMI |
| 29 | C-309 | Page + d'un Promi, passer en « promets-moi », en sortir, y revenir ; fermer, rouvrir, y revenir | Bruno-Stanislas, Fabienne-Gudule, Bruno-Stanislas… le prénom se détrace puis se trace |
| 30 | C-310 | Page + (Promi, Chiche) et onboarding : taper « aller », « haïr », « oui » puis effacer, à son rythme | « de » / « d’ » se détrace puis se trace, jamais d'un coup (chaque changement est relevé et part au Mac) |
| 31 | C-311 | Dans « Promi preuve » v212, ouvrir une parole SANS mot et la tenir ; puis une parole avec un mot, une avec plusieurs (Promi, Chiche, un Promi d'un Cercle) — défilée un peu avant de tracer, puis non | « Parole tenue ! » (« Défi relevé ! ») à la même place dans tous les cas ; il ne monte jamais |
| 32 | C-312 | Page + : ouvrir plusieurs fois « Je me promets », « Je promets à … », « promets-moi », un Chiche ; et l'onboarding | chaque exemple avec sa liaison juste dès qu'il paraît : « d’apprendre… », « d’arroser… », « d’aller voter », « d’y aller en stop », « de me coucher… » ; à la bascule du verbe, « de » / « d’ » change avec l'exemple, jamais avant |
| 33 | C-313 | Réglages → Soutenir Promi : toucher « Autre montant », puis encore, puis un palier | les paliers se déroulent et se replient en douceur, rien ne saute ; le merci paraît |
| 34 | C-314 | Réglages et Ma Parole !, en clair puis en sombre ; comparer à l'Index et à l'Aura | le même fond ; les encarts gardent leur crème |
| 35 | C-315 | Réglages, l'encart du haut | « Découvre Ma Parole ! », « Découvre » d'une autre couleur |
