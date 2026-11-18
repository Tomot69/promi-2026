# VALIDATION — ce qui reste à voir sur l'iPhone (v207, 17 nov. 2026)

**Validés en bloc par Tom (17 nov.)** : les 68 chantiers « validés par l'usage » et les 20 de méthode, et C-288, C-289 — 90 au registre.
**Devenus des spécifications de tests automatiques de la vraie app** : 42 chantiers d'états rares (ARCHITECTURE.md, « Les tests ») — marqués au registre.
**Reste : 18 points à vérifier par Tom** (11 à 14 : la séance du 17 nov. ; 15 à 18 : v209, dans l'app « Promi preuve »), une ligne chacun (13 chantiers : trois lignes en portent deux). Adresse : `http://<IP>:8752/app.html`.

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
