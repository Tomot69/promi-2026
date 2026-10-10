### ⚑ v140 (10 oct. 2026) — LA FOURRURE D'AVANT LES ESSAIS ; LA TRACE DU VRAI GESTE ; DESSIN ↔ PHOTO ; L'ICÔNE ENREGISTRER ; LE + ; RITOURNELLE ; LE MUR DU STUDIO ; E2 ET E2bis. (Décisions Tom.) Ce bloc CORRIGE v139 (la Pelote, le +, Ritournelle, le dessin partagé), v120–v123 (la densité 3) et E1 / v129 (l'onboarding).
> **Q434 : rien à faire. Q435 : un dessin part ENTIER, photos importées comprises (« c'est une composition ») ; seule une photo posée seule dans la
> bande ne se partage jamais. Q437 : remplacé (Ritournelle, plus bas). Le dessin est COLLABORATIF (C-093) : écrit dans `portage/SPEC-DONNEES` §5 bis
> et `SPEC-ECRANS`, à construire avec Firebase — rien n'est construit.**
> **⚑ LA FOURRURE DE LA PELOTE (C-083, RÉCIDIVE « trop rase »). LA RÈGLE : LA FOURRURE EST CELLE D'AVANT LES ESSAIS DE HALO — DENSITÉ ×1 (110 000 →
> 90 000 → 75 000), POIL ×1, REFLET D'ORIGINE, POINTES LIBRES AU BORD. On ne touche plus ni à sa densité ni à l'épaisseur du poil pour régler autre
> chose (un bord, un halo, une cadence) : c'est `redteam_fourrure.py` qui la tient.** Référence : `sauvegardes/app-avant-v114.html`.
> *Pourquoi elle avait perdu sa longueur* : ① v120–v123, la « densité 3 » (`REG` : deux fois plus de poils, chacun ×0,7 d'épaisseur, reflet
> adouci) — des poils si fins qu'ils ne se lisent plus un à un : un aplat ; ② v139, la limite franche au rayon de la boule coupait net les
> pointes (jusqu'à 5 pt). *Ce qui est posé* : `REG={facteur:1, epaisseur:1, doux:false}` ; dans `FS2` le corps est plein jusqu'au rayon de la
> boule, et au-delà **les pointes** dessinent la silhouette (contour moyen 120,5 pt, de 118 à 124). Deux précautions mesurées sur des essais :
> la masse des poils de profil au-delà du corps est à demi transparente (un anneau pâle) → son opacité est resserrée (0,30 → 0,62) ; et ces
> pointes prennent la couleur de l'intérieur (poil SUR corps), sinon elles font un anneau d'une autre couleur (le corps a une autre teinte que
> le poil, v123). Le peintre de secours suit la même loi (une passe sur la couronne). Rien autour, sauf l'ombre, revenue à 391,224.
> Banc WebKit, carte graphique : p50 17 ms, p95 21 à 22 ms, 57 images/s à 110 000 poils. Juges : **`redteam_fourrure.py`** (réglages en dur,
> contour au-delà de la boule et dentelé, pas d'anneau, rien autour ; 9/9, 5/9 sur l'état d'avant — ⚠ son contrôle B, le grain, ne sépare pas
> les deux états : ce sont A, C et D qui mordent) ; `redteam_bord` F réécrit (des pointes sans frange pâle) ; `redteam_halo` (anneau 127–150).
> **⚑ L'EMPREINTE SUIT LE VRAI GESTE (C-083).** *La cause du « tampon »* : un arc de 24 pt était posé tous les 20 pt AU POINT TOUCHÉ — or la boule
> suit la main, ce point est toujours le même point de l'objet : dix arcs empilés, la même marque quel que soit le geste ; et un toucher posait
> toujours le même arc vers le bas. *Aujourd'hui* : le chemin du doigt est RELEVÉ à l'écran (un point tous les 8 pt, avec la largeur du contact) ;
> au lâcher la trace est posée le long de ce chemin, rapporté à la boule telle qu'elle est à cet instant — seize arcs au plus, chacun dans le
> sens du geste, large comme le contact (0,27 rad pour un pouce, de 0,12 à 0,42). **Un appui sans glisser pose une ÉTOILE** : huit branches du
> point vers l'extérieur ; leur longueur suit la taille du contact et la profondeur atteinte. `_aura.tracesGeo()` pour les juges. Juge :
> **`redteam_trace.py`** (8 : deux trajets, deux traces alignées et centrées sur eux, la longue ≥ 1,5 × la courte, la largeur suit le contact,
> l'étoile, deux appuis deux tampons ; 2/8 avant). ⚠ La trace paraît au REPOS (doigt levé, élan éteint), pas sous le doigt : c'est la règle
> de la saccade (v124). **Geste : Tom valide sur iPhone.**
> **⚑ DESSIN ↔ PHOTO : L'UN REMPLACE L'AUTRE (C-086, C-085).** *La cause de la « bande parasite »* : le dessin posé et la photo vivaient ensemble ;
> la couche du dessin recouvrait la photo, mais elle s'arrête 7 pt au-dessus de l'axe du trait (`BANDE_RETRAIT`) — dans cette lisière on voyait
> la photo ; et après un dessin, une photo importée restait dessous, invisible. **Poser un dessin retire la photo de la bande ; importer une
> photo retire le dessin posé (`window._photoImportee`)** — il n'en reste rien. ⚠ C'est un remplacement : le dessin (ou la photo) remplacé est
> PERDU (Q439). Les points de taille : **une cible de 44 pt chacun** (`CIBLE`), le point fait le diamètre du trait + 3 (`POINT_PLUS`) ; **le
> gros pinceau fait 22 pt** (2 · 6 · 22). Juge : **`redteam_remplace.py`** (18 : dessin → photo → dessin → photo, la bande comparée au pixel à
> la photo seule ; 8/18 avant).
> **⚑ UNE SEULE ICÔNE « ENREGISTRER » (C-091)** — la flèche qui descend dans son socle (le miroir de Partager), sans texte, VoiceOver
> « Enregistrer ». Où : ① la vue en entier d'une photo ; ② la vue en entier d'un dessin (`.ev-garde`) ; ③ le plateau de l'accueil, à gauche de
> Partager (`#enrToile`, `lot-V140-ENREGISTRER`) : l'image de la Toile rendue par le moteur (`Toile.renderTo`, 1170 × 2532), jamais une capture.
> Pas ailleurs : Partager a déjà son bouton, qui ouvre la feuille du téléphone (Q440).
> **⚑ LE + DE L'ACCUEIL (C-087)** : le disque passe de 33 à **45 pt**, l'anneau garde 13,5 → 72 pt ; **la barre fait 100 pt de haut (730 → 830)**,
> 12 pt d'air au-dessus et au-dessous de l'anneau ; le centre du +, la croix et les quatre entrées restent où ils étaient à l'écran.
> **⚑ RITOURNELLE, LE ZOOM DE DÉPART (C-088) — AMENDE v139.** Sous les douze mondes « faits de leurs seules paroles », tant qu'ils gardent le semis
> constant (moins de 9 paroles) : ① la parole neuve prend la cellule libre LA PLUS PROCHE des paroles déjà là (la première : du milieu du
> champ dégagé), sans décalage (`plantOne`) — tirées au hasard, deux paroles tombaient aux deux bouts de la Toile ; ② la vue cadre les dalles
> colorées avec 0,8 cellule de marge et un plafond de zoom de 3,6 (1,3 et 2 ailleurs) (`autoView`, `_serre`). Une parole : une dalle entière
> et un peu autour ; deux, trois, quatre : toutes entières, peu de cellules vides ; à neuf, la Toile faite de ses seules paroles.
> **⚑ LE MUR DU STUDIO (C-092)** — *la cause* : le panneau flouté du Studio est fait de quatre murs en bandes (tons 54 pt, libellés 19, disques 44,
> barrettes 4) ; la phrase se centrait dans la bande touchée, et une bande de moins de 40 pt la renvoyait sur l'appareil entier — au milieu
> de l'écran, sur le nom du monde. **Au Studio le mur est le PANNEAU** (la réunion de ses bandes floutées). Et le panneau des palettes, ouvert
> sur un monde de Ma Parole !, est lui-même un mur, flouté (2,4 px) : il recouvrait les quatre zones, qui restaient les murs. Juge :
> **`redteam_studio_mur.py`** (9 : sept zones touchées au doigt ; 3/9 avant). ⚠ Son amorce doit porter `decouvert:1`, sinon c'est « la toute
> première fois » et l'offre s'ouvre seule.
> **⚑ E2 — LE PREMIER PROMI (C-075) ET E2bis — L'INTERFACE SE DÉVOILE (C-076).** `lot-E2`, `ENGAGEMENT-E2.md` (le tableau garder / supprimer /
> remplacer, les textes, ce que chaque point est devenu). Après le prénom : **le principe** (un bouton, « Plus tard ») → **la VRAIE page +**
> (Promi à soi, une phrase fantôme parmi trois, un toucher la remplit ; ni Peaufiner, ni pinceau, ni photo, ni retournement, ni « garder de
> côté ») → la plantation réelle → **la fiche**, une ligne dessous, la main accompagne le trait → tenir → **la dernière ligne**, un toucher
> ferme, `ob_fini`, puis le compte. « Plus tard » à chaque étape : un toucher, tout est affiché, rien n'est redemandé. **L'écran « parole et
> trait » de l'onboarding, sa plantation simulée et le message de fin de v129 (« Primo… Deuxio… Tertio… ») ne sont plus joués.** « Revoir la
> présentation » rejoue le principe seul. Textes PROVISOIRES dans `TEXTES_ENGAGEMENT.e2`, sans impératif.
> **« TRACE POUR TENIR » et le trait** : le mot passe de 15 à **19 px** (fiche et page +), les points à tracer de Ø 9 à **Ø 12**, en
> grandissant vers le haut (`margin-top` négatif, centre des points remonté de 1,5) — rien ne bouge dessous.
> **E2bis** : `promi_devoile` (`{index, aura, studio, fil}` ou `'tout'`) ; la barre ne porte que ce qui est déjà apparu, chaque entrée À SA
> PLACE DÉFINITIVE, le fond (`#accBarreFond`) s'étire jusqu'à elle : le + seul → l'Index à la première plantation → l'Aura au premier tenu (la
> main la désigne : `aura-apparait` est BRANCHÉ) → le Studio au premier retour sur l'accueil après l'Aura, avec une ligne → le Fil à la
> première parole adressée ou reçue. Rien ne disparaît ; rangée « Tout afficher » aux Réglages. **Qui n'a pas fait ce parcours voit tout,
> comme avant** (le dévoilement commence au bouton du principe).
> Juges : **`redteam_e2.py`** (53 : le parcours au vrai doigt, clair et sombre, les quatre « Plus tard », R6, A2, A3, E2bis) ;
> `redteam_engagement` 11/11 (**R6 est VERT**, il passe par `redteam_e2 --r6`) ; `redteam_verrou_onboarding` réécrit (9/9) ;
> `redteam_onboarding` passe la main à `redteam_e2` ; `redteam_gestes` (onze gestes branchés).
> ⚠ **Du principe au premier tenu : 2 touchers et 2 TRAITS** (planter est un trait, tenir en est un autre) — la consigne disait « 1 trait » (Q442).
> ⚠ **Trois pièges du lot** : ① la main « planter » se montrait sur la pastille VIDE, partait au toucher qui la remplit, et ne revenait plus
> (son drapeau était posé) : elle attend que la phrase porte ses mots ; ② une ligne posée dans `#device` passe SOUS une fiche (z-index 80) ;
> ③ une pastille sur deux lignes a un creux au milieu de sa boîte : un juge touche son premier rectangle (`getClientRects()[0]`).
> **Trouvé en E2, corrigé** : ① après « tenir », la fiche disait « à moi » au lieu de sa phrase (l'instant réécrit la ligne, la signature
> `data-phrase` restait : on compare aussi le texte affiché) ; ② sur l'instant, un titre de DEUX lignes était recouvert par « TENUE · À
> L'INSTANT » (cote figée pour une ligne : elle descend de ce que le titre prend en plus).

