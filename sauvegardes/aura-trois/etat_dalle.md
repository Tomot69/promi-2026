## ⚑ UNE DALLE TENUE MÈNE À SA FICHE — `lot-DALLE-PORTE` · 11 septembre 2026

Tom : *« Trois défauts à vérifier sur l'Aura […] Mesure, ne suppose pas. »* Deux des trois n'en étaient pas — mesuré ;
le troisième était réel, il est corrigé — et en le prouvant au vrai doigt, un défaut plus large est apparu (le clic
fantôme, § 3 bis). Le chantier 63 suit dans le même passage (§ 3 ter). **app.html `faff6e93…` → `48b1a56b6b4b58f425dbd7a84e0b9f1f`**,
trois blocs neufs à la fin : `lot-DALLE-PORTE`, `lot-CHEMINS-PERSONNE`, `lot-CLIC-FANTOME` (sauvegarde
`sauvegardes/app-avant-dalle-porte.html`). Journaux entiers : `sauvegardes/aura-trois/`.

### 1 · « Ce que tu as tenu » porte-t-il les trois natures ? — OUI, déjà
Le peintre (`donnees()` → `mesPromi()` → `ordreTenus()`) ne filtre que « tenu » et « planté par moi » — aucune nature.
Au jeu de démonstration : **5 paroles tenues à moi — 2 Promi (125, 139), 1 Chiche (129), 2 Promi de Nuée (130, 134) — la
rangée porte les 5.** (132, tenue, est d'Adrien : ce n'est pas ma parole, elle n'y est pas — voulu.)
**Contrôle neuf** (`releve-aura`, données) : la règle écrite en dur (`TENUES_MIENNES`, sans filtre de nature) ; quand
toutes tiennent dans la rangée, toutes y sont. **Sonde `sans-chiche` PRISE** : « perd [129] — natures ['chiche'] », deux thèmes.

### 2 · Chaque dalle garde-t-elle son monde de plantation ? — OUI, pour l'Aura et « Tenu ensemble »
Mesuré par la SORTIE, pas par le code : Studio passé en terrazzo puis en pixel (l'appel du Studio, `Toile.setTheme`), les
dalles du jeu figées en encre. Chaque dalle peinte comparée dans la même page à deux rendus du moteur — sa plantation (A),
le monde courant (B) : **distance à la plantation 0,000 à 0,002, au monde courant 0,02 à 0,62**, sur les 6 dalles (5 de
l'Aura, 1 de la fiche de Rachel). Un piège sur `dalleTrame` : chaque appel de l'Aura et de la fiche reçoit bien « encre ».
⚠ Mon premier verdict automatique disait « monde courant » pour 7 dalles : l'histogramme des couleurs ne départage pas
(encre et terrazzo peignent ici la même teinte) ; c'est le taux de remplissage qui tranche. Corrigé dans le juge : une
distance composée, et une dalle dont les deux mondes ne se distinguent pas n'est pas jugée.
**Contrôle neuf 6 bis** (page neuve — le cache de l'Aura garderait un rendu d'avant le changement ; Studio en `pixel`) :
5 dalles jugées, distance plantation / courant 0,000–0,001 / 0,14–0,62. **Sonde `monde-courant` PRISE** (les dalles de l'Aura peintes sans leur 4ᵉ argument) : les 5 nommées, à 0,097–0,723 de
leur plantation et 0,000–0,007 du monde courant.
**Ce qui ne garde PAS son monde :** seuls l'Aura (l. 28081) et la fiche d'une personne (l. 28877) passent le 4ᵉ argument ;
les 24 autres appels de `dalleTrame` en passent trois — cartes d'Index, bandeaux du Fil, fiches, et donc les cartes « Ce
que vous partagez ». C'est le lot « brancher les peintres » (§4), toujours ouvert.
**Au jeu de démonstration la rangée est uniforme** : tous les Promi ont été figés dans le monde du jour au chargement
(le rattrapage du 4 septembre — « rien n'est tiré de leur date »). La diversité viendra des plantations nouvelles.

### 3 · Toucher une dalle ouvre-t-il sa fiche ? — NON, c'était le vrai manque. CORRIGÉ.
Relevé : `cellule(p)` (Aura) et les cellules de « Tenu ensemble » n'avaient **aucun gestionnaire**. Bloc neuf
**`lot-DALLE-PORTE`** : un écouteur délégué (les cellules sont rebâties à chaque ouverture) ; la porte est
**`openDetail(id)` — la même que la carte d'Index (l. 18932) et le bandeau du Fil (l. 19049)** ; l'Aura reste dessous et
**✕ y ramène** (mesuré). **Un glissement n'ouvre rien** : le toucher se juge comme celui des Noyaux — déplacement du doigt
PLUS défilement de la colonne, sous `G.TAP` (6 pt) ; au vrai doigt, le navigateur annule en plus le toucher dès que la
colonne défile.
**Preuves :** `releve-aura` sur l'app d'avant — **8 bis PRIS** (« toucher la dalle « rapporter le livre » n'ouvre pas SA
fiche ») ; sur l'app corrigée — vert (Promi 139 ouvert, attendu 139 ; ✕ → l'Aura). `releve-fiche-personne` sur l'app
d'avant — **2 écarts, la porte de « Tenu ensemble »** ; après — **258 / 258**. **Au vrai doigt** : § 3 bis — c'est là que la
première écriture est tombée.

### 3 bis · LE CLIC FANTÔME — trouvé au vrai doigt, et il cassait AUSSI la porte des Noyaux
La première écriture de la porte ouvrait au lever du doigt (`pointerup`). Les juges, joués à la souris, étaient verts.
**Au vrai doigt (événements tactiles CDP), la fiche s'ouvrait et se refermait aussitôt** : journal des événements —
`openDetail(139)` → `closeAll` ← `openDetail` → `touchend` → **`click` sur `#scrim`** → tout se referme. Après un toucher,
le navigateur synthétise un clic AU POINT DU DOIGT, après `touchend` : ouvrir avant lui, c'est lui donner la feuille neuve à
cliquer. **La porte des Noyaux de l'Aura (lot-AURA-ORBITE, d'origine) avait exactement le même défaut** : `openPerson(Marion)`
→ clic sur `#scrim` → l'Aura, rien d'ouvert. **Sur un téléphone, toucher un Noyau n'ouvrait donc rien de visible** — aucun
juge à la souris ne pouvait le voir. Deux parades :
- **la porte des dalles (et celle du 63) s'ouvre sur le CLIC** : le lever du doigt l'arme (même cellule, sous le seuil), le
  clic qui suit l'ouvre. `app.html` restauré à `faff6e93…` et le bloc réinséré réécrit (la version d'abord insérée,
  `7ca1cc98…`, est gardée : `sauvegardes/aura-trois/app-dalle-porte-pointerup-7ca1cc98.html`) ;
- **`lot-CLIC-FANTOME`** pour la porte des Noyaux, qu'on ne touche pas : un clic ISSU D'UN TOUCHER qui tombe sur une
  COUCHE OUVERTE PENDANT LE GESTE (sa couche `.show` n'existait pas quand le doigt s'est posé) est la queue du geste
  précédent — avalé. Jamais un clic de souris, jamais un clic de script, jamais un clic sur une couche déjà ouverte :
  ✕ FERMER et une carte d'Index, touchés au vrai doigt, marchent (contrôlé). ⚠ Une première écriture comparait l'élément
  touché à l'élément cliqué — elle aurait avalé un vrai toucher sur un bouton que l'app redessine sous le doigt, sans
  qu'aucune série à la souris ne le voie ; resserrée sur la forme exacte du défaut AVANT toute série (la chaîne arrêtée).
**Le défaut dort-il ailleurs ? (Tom : « confirme-le en balayant les autres ».)** Dans le CODE : **53 écouteurs de pose ou de
lever du doigt** (`pointerdown/up`, `touchstart/end`, `mousedown/up`, en `addEventListener` ou en attribut) ; **un seul
ouvre quelque chose — la porte des Noyaux de l'Aura** (l. 28578, `openPerson`). Le curseur de teinte du Studio écoute
`pointerup` mais n'ouvre rien. AU DOIGT (`balayage_fantome.py` : chaque élément touchable de douze écrans, touché au doigt
puis cliqué à la souris, écran rouvert à neuf ; une porte fantôme est une porte où le doigt et la souris ne finissent pas au
même endroit) : **en cours au moment d'écrire** — sur une copie SANS garde (`scratchpad/app-sans-garde.html`, `1cf70b18…`), il doit retrouver
les Noyaux ; sur l'app finale, zéro écart. Journaux : `sauvegardes/aura-trois/balayage_*.log` (résultat ajouté ci-dessous à
son retour).
**Preuves au vrai doigt (`doigt_defile.py`, événements tactiles CDP)** — sur la version d'abord insérée, sans garde :
**4 ratés sur 11** (les deux touchers de dalle de l'Aura, le Noyau de Marion, le nom « Rachel » d'une Nuée : ouverts puis
refermés). Sur l'app finale (`48b1a56b…`) : **13 / 13** —
- **un glissement vertical n'ouvre JAMAIS une fiche** : sur l'Aura, la colonne défile de 145 pt (course 150), aucune fiche ;
  sur « Tenu ensemble », 84 pt (toute la course), aucune fiche ;
- un toucher net, et un toucher qui tremble de 4 pt (sous le seuil de 6), ouvrent la fiche de la dalle (Promi 139), sur les
  deux écrans ;
- le Noyau de Marion, au doigt : SA fiche s'ouvre et **reste** ; le nom « Rachel » dans « Avec Rachel, Adrien, +3 » :
  SA fiche s'ouvre et reste ;
- les vrais touchers marchent toujours : ✕ FERMER referme la fiche, une carte d'Index ouvre son Promi ;
- un seul chemin : l'appel nu `openPerson` EST `window.openPerson`, la fiche refaite.
**La sonde « porte naïve »** (une porte qui ouvre à chaque doigt levé, même après un défilement) est **PRISE** au
glissement sur les deux écrans — sur l'app finale aussi (la sonde passe sous le garde : c'est bien le glissement que le contrôle juge).

### 3 ter · LE CHANTIER 63 — les noms écrits mènent à la personne (`lot-CHEMINS-PERSONNE`)
Bloc neuf `lot-CHEMINS-PERSONNE` (la porte commune, ouverte sur le clic). Le nom touché dans une ligne mène à SA fiche —
`openPerson`, le même chemin que les Noyaux et les disques ; le toucher lit le MOT sous le doigt et ne l'accepte que s'il est
une personne connue (`peopleList`). Aucune forme neuve, aucun nœud ajouté. **Preuve au doigt (`chemins63.py`)** — sur l'app
d'avant : **7 ratés sur 12** (tous les noms) ; sur l'app finale : **12 / 12** —
- fiche de Nuée « Avec Rachel, Adrien, +3 » : Rachel → la fiche de Rachel, Adrien → celle d'Adrien, **« +3 » → personne** ;
- Peaufiner de la Nuée « Rachel · Adrien · +3 » : de même ;
- fiche du Chiche « À Marion · avec Rachel » : Marion, Rachel ; fiche du Promi « À Rachel » : Rachel ;
- **la rangée « À QUI » du Peaufiner d'un Promi n'ouvre personne** — elle règle le destinataire (validé par Tom) ;
- un glissement de 30 pt sur un nom n'ouvre rien ; au vrai doigt, « Rachel » d'une Nuée ouvre SA fiche et elle reste.
**Reste ouvert du 63 :** « toi » (le mode « moi » n'a pas de fiche — décision de produit) ; les noms et visages DANS une carte
du Fil ou de l'Index (la carte entière ouvre sa parole — Q195).

### 4 · Un seul chemin de code
Une dalle mène à la fiche de SON Promi : `openDetail`, partout (carte d'Index, bandeau du Fil, dalle de l'Aura, « Tenu
ensemble »). Un Noyau, un disque, un nom mènent à la fiche de la personne : `openPerson` — et l'appel nu est
`window.openPerson`, la fiche refaite (mesuré : l'appel nu `openPerson` EST `window.openPerson`, et au doigt le Noyau de Marion, « Rachel » d'une Nuée, les noms du Peaufiner d'une Nuée et ceux de la ligne d'une fiche ouvrent tous `#psCadre[data-fiche=nom]` — la même fiche, jamais l'ancienne). Les seuls appels morts sont dans l'ancienne Aura masquée (l. 6320,
6322, 6510 — déjà relevés). ⚠ Mise au point : je n'ai trouvé **aucun** `openPerson` orphelin dans le Fil ni dans la fiche
d'un Promi.

### 5 · Contrôles
**Série complète, EN SÉRIE, sur `48b1a56b…`** (`sauvegardes/aura-trois/bat_apres14.log`, 03:27 → 03:55) — 18 batteries :
redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande 19/19 · redteam_toile 17/17 ·
redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite · redteam_vide 61/61 · redteam_air ✅ 442 paires ·
redteam_champ 32/32 · releve-design ✅ aucun écart · redteam_fonctions 22/22 · redteam_polices 0 couple absent ·
redteam_superpo 0 recouvrement · releve-fiche-personne ✅ 258 · **releve-aura : 4 écarts, tous dans la matière** —
« monter la serre » ΔE 7,8 / 9,0 et « arroser tous les soirs » 5,8 / 6,9 (sombre / clair) ; toutes ses autres familles à 0,
dont les trois contrôles neufs (natures, 6 bis, 8 bis). Les juges étendus ont d'abord été passés sur l'app d'avant (pris) et
sous deux sondes (prises), avant la série.
**`releve-aura` rougit sur la matière à chaque passage de ce lot** — « planter un arbre », « monter la serre », « arroser
tous les soirs », de ΔE 6,2 à 12,9 selon le tirage. **Règle de Tom (CLAUDE.md §7, 11 sept.) : c'est le défaut du chantier
59, PRIS à ces passages ; un relancer vert ne l'annulerait pas.** Ce lot ne touche pas la matière.
