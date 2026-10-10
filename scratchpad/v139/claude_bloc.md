### ⚑ v139 (9 oct. 2026) — RETOURS DE TOM SUR IPHONE : LA PELOTE (CONTOUR FRANC, OMBRE, TOUCHER), LE CRÈME DES FICHES, LA PHOTO AU PINCEMENT, LES PHOTOS DANS LE DESSIN, LE +, LA MAIN QUI TRACE, RITOURNELLE. (Décisions Tom.) Ce bloc CORRIGE v136–v138 (la Pelote), v136 (le +, le corps clair des fiches) et E1 (la main, « Revoir les gestes »).
> **Q426 : les DEUX rangées aux Réglages** — « Revoir la présentation » (`#replayPres`, elle relance la présentation) et « Revoir les gestes »
> (`#replayOnb`, elle efface les drapeaux). Q427 : rien de plus. Q428 validée. **E2 n'est pas commencé.**
> **⚑ LA PELOTE (C-083). ① LE CONTOUR EST UNE LIMITE FRANCHE** : rien au-delà du rayon de la boule (116 pt, `E.R`), un seul pixel de lissage — dans la
> passe de composition (`FS2` : `t=clamp(uR0−r+0,5)`, le corps plein partout en deçà) et dans le peintre de secours (découpe en disque après
> la composition). **Le repli de couleur de v137–v138 (vis-à-vis intérieur, table `cv.__bd`) est RETIRÉ** avec la frange qu'il corrigeait.
> ⚠ **Il n'y avait pas de « dernier bord net » dans l'historique** : mesurée sur l'opacité, la frange faisait 6,25 pt en v136, 4,25 en v138 (jusqu'à
> 7,5 : des poils de longueurs différentes) ; c'est la couleur sombre des poils de profil qui la faisait paraître nette en v136 — et c'était
> le liseré. Aujourd'hui : 0,5 pt, et ΔE 0,9 à 2,3 entre le bord et l'intérieur (pas de liseré). **La silhouette fait donc 116 pt, plus 121** (Q430).
> **② L'OMBRE REVIENT, dans les deux thèmes** (`#auPeloteOmbre`, `lot-V139-OMBRE-css`) : la géométrie de v121 (104,429 × 16,245), l'encre à 0,10 en
> clair, la crème à 0,105 en sombre, à 386,224 (la place de la composition B remontée de 5 pt avec le bas de la silhouette). **C'est la SEULE
> exception de la liste blanche de `redteam_volume`** (deux dégradés, pas un de plus). Ni halo, ni liseré, ni couronne.
> **③ LE TOUCHER** : la PROFONDEUR suit `q(t) = 1 − 1/(1 + t/0,60)²` (`G.ENF_TAU`) — sa vitesse ne fait que décroître dès la première image
> (5,6 % de la butée par image à 60 i/s ; l'ancienne loi en prenait 26 à 32 % à la première), elle tend vers la butée ; la pression est `p = q^1,5`
> (`d = dmax × p^(2/3)`). Au relâcher `q` décroît en 0,60 s (`G.RETOUR_TAU` ; 0,15 avant). On rappuie au même endroit : on repart de la
> profondeur en cours. **Le comblement par la rotation AMORTIT (`× e^(−comblement / COMBLE_K)`, 0,08), il ne retranche plus** : retranché, la
> profondeur tombait à zéro d'un coup (un pas de 15 %). **La forme du contact** : `radiusX`, `radiusY`, `rotationAngle` du toucher quand
> Safari les donne (`TCH`, lus sur `touchstart` / `touchmove`), sinon `width` / `height` du pointeur ; le demi-axe vaut `DOIGT_K` (2,2) × le
> rayon du contact, borné à [0,16 ; 0,46] rayon de boule — avant, borné entre l'index et le pouce (0,26–0,40), un vrai contact tombait
> toujours sur la borne basse : deux doigts donnaient la même empreinte. `?mesure=1` écrit le contact lu (pour étalonner `DOIGT_K` sur l'iPhone).
> ⚠ Une seule empreinte à la fois : toucher AILLEURS pendant qu'un creux revient le retire d'un coup (Q432).
> Juges : **`redteam_enfonce.py`** (14 : la profondeur croît à chaque image, sa vitesse décroît, aucun pas > 8 %, butée, deux tailles de contact
> → deux empreintes, contact allongé → empreinte allongée, retour lent ; 6/14 sur l'état d'avant) ; `redteam_bord` (+ F, la limite franche,
> par les deux chemins) ; `redteam_halo` et `redteam_volume` réécrits ; `releve-aura` acquis 4 (la loi en dur).
> ⚠ **Deux pièges** : ① `destination-in` avec le `fillStyle` laissé par le peintre (transparent) EFFACE TOUT — le secours ne peignait plus rien et
> l'ancien contrôle du bord était VERT (ΔE 0,0 entre deux zones vides) : c'est le contrôle neuf de la frange qui l'a pris ; ② deux relevés
> `requestAnimationFrame` à 4 ms l'un de l'autre gonflent un « pas par image » par quatre : on réunit les relevés à moins de 12 ms.
> **⚑ LE CRÈME DES FICHES EN CLAIR (C-084)** : le corps (sous le trait) et l'encart du haut passent de `#F7F0DE` à **`#EAD9B9`** (le fond de
> l'Index, `--c-creme90-2` ; `lot-V139-CREME-css`), dans les fiches seulement. **Les cartes du fil d'un Cercle et la carte du mot, qui étaient à
> `#E9D8B7`, passent en échange à `#F7F0DE`** (la paire de la page du Fil) : sinon elles se confondaient avec le corps. Mesuré sur `#EAD9B9` :
> encre 12,56:1 · tenu `#00341A` 10,04:1 · crête 7,46:1 · **à tenir `#DD4D23` 2,93:1 (3,58 avant)** · tous les ΔE d'état > 66. La page + ne bouge pas.
> **⚑ LA PHOTO D'UNE FICHE SE CADRE AU DOIGT (C-085, `lot-V139-CADRE`)** : deux doigts zooment dans le rapport de leur écart (1:1), le point sous
> leur milieu y reste ; un doigt déplace (la photo le rattrape après 10 pt) ; z de 0,3 à 8. Le cadrage vit sur ce qui porte la photo
> (`p.photoCadre = {z, dx, dy, n}`, points de l'écran 390 ; `_phrase.photoCadre` sur la page +, il suit la photo à la plantation) et se
> sauvegarde avec la parole. **Sans geste, la photo garde sa boîte ; cadrée, elle se dessine entière** (elle peut remplir tout le haut).
> Un toucher sans glisser ouvre toujours la photo en entier ; là, **le bouton « Enregistrer la photo »** (la feuille de partage du téléphone
> quand elle prend un fichier, sinon un téléchargement). Un Cercle ne porte pas de photo. ⚠ « Le partage le respecte » : une photo n'est
> jamais dans une image partagée (v137) — rien à respecter aujourd'hui (Q434). Juge : **`redteam_cadre.py`** (22, au vrai doigt ; 8/21 avant).
> **⚑ LE DESSIN (C-086)** : ① **les tailles : plume 2 · 6 · 14, gomme 8 · 18 · 36**, et les trois points du choix à l'échelle (1 pt pour 1 pt) ;
> ② **des photos dans le dessin** : le cinquième disque de la rangée, PHOTO (`PAS_OUTIL` 58 → 46). Une photo importée est UN ÉLÉMENT DE LA LISTE,
> à son rang parmi les traits : `{img, x, y, w, h}`. PHOTO choisie, un doigt déplace la photo touchée, deux doigts changent sa taille ;
> toucher de nouveau le disque en importe d'autres ; ANNULER la retire comme un trait ; POSER la pose avec le reste (la bande et la vue
> entière la montrent). **Le partage du dessin N'EMPORTE PAS les photos importées** (v137 : « jamais une photo importée ») — `entier(d, k, true)` ;
> à trancher par Tom (Q435). Juges : **`redteam_dessin_photo.py`** (15), `redteam_dessin` (les valeurs, six outils).
> **⚑ LE + DE L'ACCUEIL FAIT 60 pt** (84 en v136 ; C-087) : 12 pt d'air jusqu'au contour de la barre, même centre, l'anneau garde ses 13,5,
> le disque fait 33, la croix 27 de large (82 % du disque, 46 % avant), à 3 pt de l'anneau.
> **⚑ LA MAIN FANTÔME TRACE (C-074, Q429)** : × 1,5 (`GRAND`), 1,6 s pour le trajet d'un trait (`TRAJET`), trois passages (`TOURS`). `montrer(id,
> cible, chemin, trace)` : `trace = {de, col, ep, pointille}` — un trait plein, opaque, qui grandit sous le doigt et s'efface quand la main
> part. Pour « tenir » et « chiche » : la seconde moitié du trait (les pointillés de la fiche deviennent pleins), à la couleur de l'état.
> ⚠ **En E1 la main s'arrêtait au milieu du trait (30 → 195) : au vrai doigt ce tracé-là ne tient PAS la parole** (mesuré : 30 → 195 et
> 195 → 360 laissent « à tenir » ; 30 → 360 et 120 → 300 tiennent). Elle va maintenant jusqu'au bout.
> **⚑ RITOURNELLE (C-088), DEUX CAUSES NOMMÉES. ① « Trop zoomée »** : dans les douze mondes « faits de leurs seules paroles » (`_NEUFS`), à une
> parole UNE cellule couvrait tout l'écran (Ritournelle et Bobinette n'y peignaient plus rien), à trois ou six les coulées débordaient.
> **Tant que la Toile compte moins de `SEMIS_NEUF_MIN` = 9 paroles et Cercles, elle garde le semis constant des autres mondes** (cellules
> vides autour, recul cadré) ; à neuf elle redevient la Toile faite de ses seules paroles (v34) — elle se ressème une fois à ce passage.
> Les aperçus du Studio gardent la règle d'origine ; le banc de rendu et le rythme (19 paroles) ne changent pas. **Ce point AMENDE v34.**
> **② « Toucher une dalle n'ouvre pas sa fiche »** : la durée du toucher (700 ms au plus) était comptée à l'heure du TRAITEMENT (`Date.now()`).
> Sous Ritournelle une image peut durer plus d'une seconde (1,15 s au banc WebKit @3x) : tombée entre l'appui et le lever, elle faisait jeter
> le toucher. On compare maintenant les heures des deux ÉVÉNEMENTS (`e.timeStamp`). Juge : `redteam_toucher` (+ trois contrôles Ritournelle :
> 1 et 3 paroles, et trois touchers avec une image de 900 ms entre l'appui et le lever — 0 sur 3 avant).
> **Au registre, sans rien construire** : la façade animée (C-089, reportée à Swift) ; le prix de Ma Parole ! (C-090, décision de Tom).

