# AUDIT — LE CHANTIER DE L'ORBITE (Aura)

> Écrit le 6 septembre 2026, à la demande de Tom, pour clore un chat saturé et en
> ouvrir un neuf sans reperdre ce qui a été acquis.
> **`app.html` n'a jamais été modifié pendant tout ce chantier** — md5
> `61280542751d0d0df5bce546f9a091b1`, inchangé depuis le lot du moteur (4 septembre).

---

## 1 · CE QUI EST VALIDÉ — à ne plus rediscuter

Chaque ligne a été validée explicitement par Tom, en propres termes.

| Acquis | Sa formulation |
|---|---|
| Le **rayon dit la date** de la dernière parole tenue | « bien vu d'avoir refusé de corriger le rayon pour arranger le dessin — la donnée ne se sacrifie pas à la mise en page » |
| La **vitesse est commune** à tous | posé au lot de la gravitation |
| La **lune terracotta** est binaire | idem |
| La **couleur d'un disque dit la Nuée** | idem |
| **Rien ne passe devant ton Noyau** | règle absolue, garantie par l'ordre de tracé (rang 40 contre 32) |
| Les **prénoms restent droits et lisibles** | jamais de perspective sur un mot |
| Le **cisaillement des bandes** (rotation différentielle) | « le cisaillement des bandes est juste » |
| La **teinte encre** : on garde la FORME de la dalle, pas ses couleurs | « tes deux arguments tiennent — le terracotta d'un monde est exactement *à tenir*, et la matière ne doit pas parler le langage des états » |
| Le **centre appartient à ton Noyau** — la matière s'y raréfie | « là c'est illisible si un truc au centre » |
| Le **contour reste sphérique** — on doit pouvoir tracer un cercle parfait autour | « meme s'il y a des reliefs sur la surface, ça doit rester globalement sphérique » |
| Le **relief est de SURFACE**, jamais de forme | conséquence directe : haute fréquence (6 à 40 tours), 2 à 7 % d'amplitude |
| **Le toucher doit être mou** et réagir « comme si c'était en vrai » | |
| Les **reflets ne sont pas des rayures parallèles** | |
| Le grain **tissu / fil** (proposition 11) est la seule matière retenue | « le 11 est à complexifier en finesse des points » |

### Décision produit à intégrer
L'orbite sera **partageable et payante**, comme les mondes du Studio. **Une gratuite
par défaut, et elle doit être belle** — pas fade pour pousser à l'achat. Les autres à
1 €, incluses dans le Cercle. Elle doit donc **tenir dans une image partagée**, en deux
formes : intégrée au partage d'un Promi (en écartant les autres éléments), ou seule en
composition. Corollaire de dessin : **les silhouettes à relief fin disparaissent à 200 px** —
il faut une forme lisible en petit.

---

## 2 · CE QUI A ÉTÉ REJETÉ — et pourquoi, pour ne pas y revenir

| Rejeté | La raison, dans ses mots |
|---|---|
| L'orbite à six anneaux plats, en cercle | « ennuyeuse parce qu'elle est plate » |
| Les traînées en arc dégradé | « pas arty du tout », « un CRM maquillé » |
| Les trois directions « tout en matière » | « on ne comprend rien », la matière tuait la lecture |
| Le rejeu du temps | « un écran qui a besoin d'une légende est raté » |
| L'image fixe (orbite qui ne tourne pas) | ne bouge pas assez |
| Le **liquide au centre** | met de la matière là où vivent le Noyau et les six |
| Les **formes non convexes** (goutte, onde en volume, dalle en volume) | « le contour extérieur est toujours très laid », « des ovales irréguliers » |
| La **teinte du monde** (dalles colorées) | aplatit la sphère, et son terracotta EST « à tenir » |
| L'**iridescence d'essence** telle que faite | « rend illisible », mange le relief, et produit des **rayures parallèles** |
| Les **formes plates** (Toile, spirale, cernes, tissage, champ) | écartées d'emblée : « non on revient à la sphère » |
| Le **squircle / ovoïde / lentille / capsule** | « boring et vu et revu » |

**Le motif de fond de tous ces rejets :** je proposais des *variations de rendu* alors
que Tom rejetait le *parti pris*. Quinze séries, aucune retenue entière — jusqu'à ce
qu'on isole une seule variable à la fois (le grain, puis la loi de contact).

---

## 3 · LES BUGS TROUVÉS — les leçons techniques à ne pas repayer

### ⚠ Trois bugs qui produisaient « c'est dix fois la même image »

1. **L'empreinte du doigt était derrière la sphère.** Elle était donnée dans le repère
   de l'OBJET ; avec une vue tournée de 2,9 rad, son centre tombait à z = −0,91, et
   `dosCache` la supprimait. **Le doigt appuyait sur la face cachée.** Correctif : la
   donner FACE À NOUS et appliquer la rotation inverse. *Payé pendant quatre séries.*
2. **Les grains faisaient 2 à 3 pixels.** À cette taille un rond, un carré, une croix et
   un losange donnent **exactement les mêmes pixels** : la forme n'existait pas, seule la
   densité se voyait. Correctif : 6 à 14 px, et quatre fois moins de grains.
3. **Le profil de forme était élevé au carré.** J'écrivais `x/h*rr*h = x*rr`, ce qui
   multiplie le profil par le rayon de la sphère. `(1−|y|⁴)^¼` devenait une forme à
   pointes et flancs droits. **La forme dessinée n'était jamais celle que je croyais.**

### ⚠ Les pièges d'instrument (mesures fausses)

4. **Un banc qui chronomètre les appels canvas ne mesure rien** — le canvas 2D EMPILE
   les ordres. Mon premier banc annonçait 0,25 ms pour 4 000 traits ; l'écran tournait à
   12 images/s. **Mesurer l'intervalle réel entre deux images.**
5. **Un banc sur page nue ne parle pas de l'écran complet** : le même `fillRect` tenait
   34 000 points sur une page vide et plafonnait à **13 000** dans la planche.
6. **Une capture prend 100 à 300 ms** : photographier « pendant » un lancer, c'est
   photographier après — l'élan est amorti et l'image ne montre rien alors que le code
   dessine 67 000 tampons. **Entretenir la vitesse pendant la capture.**
7. **Une fenêtre de mesure fixe compare deux scènes** quand la sphère tourne. Arrêter la
   rotation, ou restaurer la vue avant de photographier.
8. **`toile-extrait.js` vieillit en silence** : la copie du moteur datait d'avant le lot
   du monde figé, `dalleTrame` **ignorait son 4ᵉ argument sans erreur**, et les « quatre
   mondes » rendaient tous la même sphère. **Vérifier ce que la copie sait faire**
   (`!!(Toile.mondeCourant)`), jamais le supposer, et re-extraire après tout lot.

---

## 4 · CE QUI EST MESURÉ — la technique, acquise

```
LE TAMPON DE GRAIN gagne, et de loin (intervalle RÉEL entre deux images, 4 toiles)
   drawImage par grain   20 000 → 48,6 ms   34 000 → 80,4    ← hors budget ×3
   fillRect              20 000 → 16,8 ms   34 000 → 16,8   48 000 → 24,4
   TAMPON pré-rendu      20 000 → 16,8 ms   34 000 → 16,7   48 000 → 16,7   64 000 → 16,8
LA MÉTHODE : un Uint32Array par tranche de profondeur, un putImageData, et des tampons
   stockés en LISTE DE DÉCALAGES (pas en boîte) — 11,1 → 8,6 ms par image en rotation.
LE COÛT FIXE (vider quatre tampons + les verser) : 1,25 ms seulement.
LE PLAFOND RÉEL sur l'écran complet : ~39 500 DALLES (3-6 px) pour 60 im/s propres ;
   46 000 tient à 17,3 ms. Une dalle coûte 2 à 4 fois un grain rond.
LES QUATRE TRANCHES de profondeur, chacune au z-index que la formule des anneaux lui
   donnerait (20 + z/10) : c'est ce qui met les six DEDANS et pas dessus.
```

---

## 5 · CE QUI RESTE FAUX — et que le prochain chat doit régler

### ⚠ L'empreinte n'est pas crédible : ce n'est pas un doigt

Mon modèle est une **cloche gaussienne** sur une ellipse : `(1 − k·e²)·e^(−λ·e²)`.
Un vrai doigt ne fait pas ça. **La pulpe est molle et s'aplatit contre la surface** :
la zone de contact devient **plate**, avec un **bord net**, et la matière chassée forme
un bourrelet **juste à l'extérieur de ce plateau**. Il faut donc :

- un **profil à plateau** (fond plat sur toute la zone de contact), pas une pointe ;
- un **bord franc** au lieu d'une décroissance douce ;
- une **empreinte qui grandit avec la pression** (plus on appuie, plus la surface de
  contact s'élargit — c'est ça qui « fait doigt ») ;
- l'**orientation** et l'**asymétrie** (la pulpe appuie plus que le bout).

### Autres points ouverts
- La **couleur** : tout ce qui a été essayé (essence, rampes de l'app, bruit spatial) a
  été rejeté. Rien n'est validé au-delà de « la forme de la dalle dans l'encre ».
- L'**animation** n'a jamais été jugée sur les nouvelles matières : tout est fixe depuis
  la série des planches.
- Le **partage** (image seule / intégrée) n'a jamais été maquetté.

---

## 6 · L'ÉTAT DES FICHIERS

```
app.html                     INCHANGÉ (md5 61280542751d0d0df5bce546f9a091b1)
PLANCHE-AURA-SPHERE.html     la dernière version ANIMÉE (dérive, doigt, cratère, dalles)
PLANCHE-TISSU.html           la dernière planche fixe — le tissu affiné, empreinte corrigée
PLANCHE-ORBITES*.html        les quinze séries, dans l'ordre
scratchpad/_orb*.js          les fragments (moteur, formes, peintre, séries)
scratchpad/toile-extrait.js  la copie du moteur — À JOUR depuis le 5 septembre
sauvegardes/                 avant chaque lot risqué
ETAT-DES-LIEUX.md            les chapitres de chaque lot, en tête
```

---

## 7 · LE PROMPT POUR LE NOUVEAU CHAT

> À copier tel quel dans un chat neuf.

```
Nouveau chantier sur Promi, et uniquement celui-là : L'ORBITE DE L'AURA.

Avant tout : relance le serveur et donne-moi les trois adresses en tête de ton
premier message. Puis lis CLAUDE.md, AUDIT-ORBITE.md EN ENTIER (il fait foi) et
le chapitre en tête d'ETAT-DES-LIEUX.md. Tu ne touches pas à app.html.

L'audit contient quinze séries déjà rejetées, avec la raison de chaque rejet.
Ne me les repropose pas. Il contient aussi les acquis : tu pars de là, pas de
zéro. Et il contient huit bugs déjà payés — ne les repaie pas.

CE QUE JE VEUX, ET LE NIVEAU
Un CHEF-D'OEUVRE GRAPHIQUE DIGITAL, au même titre que la Toile. C'est l'écran
signature, celui qu'on montrera, et il sera partageable et payant — donc il doit
tenir dans une image et donner envie de l'acheter.
Le critère est simple et il n'est pas négociable : ARTY, FASCINANT, on doit
avoir envie d'y revenir et de jouer avec pendant des heures — la pousser, la
voir réagir, recommencer. Si en la manipulant deux minutes toi-même tu n'as pas
envie de continuer, ce n'est pas fini : dis-le-moi plutôt que de me livrer du
correct.

CE QU'ELLE EST
Elle est GLOBALEMENT SPHÉRIQUE — on doit pouvoir tracer un cercle parfait
autour — avec du relief DE SURFACE, jamais de forme. Au centre, mon Noyau ;
autour, six disques qui gravitent, et leur rayon dit la date de leur dernière
parole tenue. La matière se raréfie au centre pour leur laisser la place.
Elle est MOLLE : quand on la touche, elle réagit comme une vraie matière.

TROIS CHOSES À RÉGLER, DANS CET ORDRE
1 · L'EMPREINTE. Le modèle actuel est une cloche gaussienne : ce n'est pas un
    doigt. Une pulpe molle s'APLATIT contre la surface — la zone de contact
    devient PLATE, avec un bord net, et le bourrelet naît juste à l'extérieur de
    ce plateau. Et l'empreinte GRANDIT avec la pression. Refais-la, et
    prouve-la en pixels sur l'image rendue.
2 · LA MATIÈRE. Le seul grain retenu est le TISSU / FIL. Pousse-le en finesse et
    en variété — mais fais varier le GRAIN et la LOI DE CONTACT, pas seulement
    la couleur : c'est l'erreur qui a coûté dix séries. Isole une variable à la
    fois.
3 · LA COULEUR. Rien n'est validé, sauf « la forme de la dalle peinte dans
    l'encre de l'écran ». L'iridescence a été rejetée deux fois : illisible, et
    elle produisait des rayures parallèles. Propose autre chose, dans la palette
    de l'app.

MA MÉTHODE, ET ELLE A FAIT SES PREUVES
- Des PLANCHES FIXES, plein cadre, fond d'encre, une ligne sous chacune. Pas de
  mesures dans la planche, pas de tableaux, pas de texte long.
- Tu ne me livres JAMAIS un chiffre que l'écran ne confirme pas. Une mesure
  prise dans ton code, sur un écran où rien ne bouge, est pire que pas de
  mesure : elle te fait croire que c'est fait.
- Quand quelque chose n'arrive pas à l'écran, tu cherches POURQUOI avant
  d'ajuster des valeurs. Les cinq pièges d'instrument sont dans l'audit.
- Si tu tournes en rond, tu me le dis au lieu de me livrer une série de plus.
- Une seule contrainte technique : tenable à 60 images par seconde. La technique
  est acquise (tampons pré-rendus versés dans un tampon de pixels) et les
  plafonds sont mesurés dans l'audit — respecte-les, ne les remesure pas.
```
