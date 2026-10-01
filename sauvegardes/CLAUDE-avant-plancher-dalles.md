# CLAUDE.md — Promi

> Ce fichier est relu à chaque session. Il fait autorité sur tout le reste.
> Si une consigne de l'utilisateur contredit ce fichier, **demander avant d'agir**.

> ## ⚑ À CHAQUE NOUVELLE SESSION, AVANT TOUTE AUTRE CHOSE
> **Relancer le serveur et donner les trois adresses complètes, en tête du premier
> message, sans que Tom ait à le demander.**
>
> ```bash
> python3 -m http.server 8752 --bind 127.0.0.1
> ```
>
> - `http://127.0.0.1:8752/app.html`
> - `http://127.0.0.1:8752/promi-moodboard-H.html`
> - `http://127.0.0.1:8752/promi-nuee-toile.html`
>
> **`127.0.0.1`, jamais `localhost`** — il bascule en https et échoue.
> **Le port est 8752** : c'est celui que tous les outils (`redteam_*.py`, `releve-*.py`,
> `scratchpad/cap_*.py`) portent en dur. Un serveur sur un autre port ne les sert pas.
> Vérifier d'abord qu'il ne tourne pas déjà : `lsof -nP -iTCP:8752 -sTCP:LISTEN`
> (attention, le processus s'appelle **`Python`** avec une majuscule — un `grep python`
> ne le voit pas, et on en relance un pour rien).

> **LE MOODBOARD FAIT FOI. Une mesure prise sur l'app ne fait JAMAIS référence —
> elle constate un état, elle ne le valide pas.** Toute valeur de design se lit
> dans `MOODBOARD-VALEURS.md` (arbre complet des neuf écrans, extrait du moodboard).
> Prendre une mesure de l'app pour cible, c'est graver un bug : c'est ainsi que le
> panneau du geste de la fiche est resté à 176px/rayon 0 pendant que la page + était
> corrigée à 118px/rayon 26 — les deux écrans ont divergé. En cas de doute :
> `MOODBOARD-VALEURS.md` > `ECARTS-MOODBOARD.md` > toute mesure d'app.

> **RÉFÉRENCE DE DESIGN — `MOODBOARD-parcours.html`.**
> Ce fichier est la référence visuelle du parcours (les écrans de création,
> phrase, « à qui », fiche, tenue, corrections). `PARCOURS.md` n'en est qu'une
> **transcription** : en cas de conflit, il **cède devant le moodboard**.
> **À lire avant tout lot touchant à un écran du parcours.**

---

## 1. Ce qu'est Promi

Une application mobile française pour **tenir sa parole**. On y « plante » des
promesses — les **Promi** — qui deviennent des dalles colorées sur une **Toile**
personnelle. On tient sa parole par un **geste tracé au doigt**, pas par une case
à cocher.

Ce n'est **pas** une to-do list. Toute décision qui la rapproche d'un gestionnaire
de tâches est à rejeter, même si elle est fonctionnellement pratique.

**Public visé :** grand public, usage social et affectif. L'app doit provoquer une
émotion, pas de l'efficacité.

---

## 2. Vocabulaire — invariable

| Mot | Sens | Notes |
|---|---|---|
| **Promi** | une promesse, une dalle | invariable au pluriel : « trois Promi » |
| **dalle** | la forme colorée d'un Promi sur la Toile | synonyme de Promi |
| **Toile** | le canevas principal, Voronoï pondéré | **ne jamais modifier son code** |
| **Nuée** | un collectif de Promi (groupe, projet) | |
| **Brouillon** | un Promi non encore planté | |
| **Fil** | le flux d'activité | |
| **Aura** | l'écran de progression et d'analyse | anciennement « Karma » |
| **Studio** | le sélecteur de monde graphique | |
| **Le Cercle** | l'abonnement payant | |
| **Peaufiner** | le tiroir de réglages, en bas de chaque fiche | |
| **Index** | la liste complète des Promi | |
| **planter** | créer un Promi | |
| **tenir** | honorer sa parole | |

**Termes bannis** — ne jamais les employer, même en interne :
« Belle parole » comme bouton · « En replanter un » · « Dire un mot » comme gros
bouton · « tâche » · « to-do » · « objectif » · « échéance » comme libellé de champ ·
**« valider »** · **« urgent »** · **« score »** · **« brouillon »**.
On dit **tenir sa parole**, **tracer**, **planter**, **lancer**. Un « brouillon » est un
**gardé de côté**. (Liste complétée par Tom, 18 août 2026.)

### Un mot qui manque — on écrit le plus sobre, et on avance

**Le mot du moodboard d'abord**, toujours. Mais s'il n'existe **nulle part** — ni moodboard,
ni `PROMI-SPECIFICATIONS.md`, ni l'app — **on n'attend plus** : on écrit **le mot le plus
sobre possible, dans le lexique du produit**, on le note dans `QUESTIONS.md` avec la mention
**« à valider »**, et on continue. (Décision Tom, 18 août 2026.) Cela ne lève pas
l'interdiction d'inventer une FONCTION ni de trancher un point de produit : ça ne vaut que
pour un mot manquant.

---

## 3. Les couleurs — la règle des trois tons

Un écran de fiche porte **toujours trois couleurs distinctes** :

1. **La dalle** — sa couleur propre, issue du monde choisi au Studio
2. **Le fond** — l'état du Promi
3. **Les traits** — une troisième teinte, dérivée de la dalle

### Les couleurs signal — la nature de la chose regardée

Chaque nature a SA couleur signal. Elle ne dépend jamais du contenu (§4).
Le framboise du Chiche a été décalé vers le rouge (depuis un fuchsia #F0208A qui
frôlait le mauve en petit) pour se distinguer de la Nuée d'un coup d'œil.

```
bleu       #3A54FF   un Promi
framboise  #FA2258   un Chiche
mauve      #8A5CF0   une Nuée
terracotta #F07A2E   à tenir
menthe     #2BE88C   tenu
```

### Les couleurs d'état (fond)

```
#2BE88C   menthe       tenue
#F07A2E   orange       à tenir
#FA2258   framboise    Chiche
#E4CEFD   lilas        Nuée (clair)
#8A5CF0   mauve        Nuée (soutenu)
#3A54FF   bleu         création, Promi
neutre    periwinkle   en cours
#F4EEE1   crème        surface claire
#16171B   encre        surface sombre
```

### Les corps de fiche — la bande porte la NATURE, jamais l'état (direction Horizon)

> **⚠ RÈGLE CORRIGÉE (décision Tom, direction Horizon — le moodboard `promi-moodboard-H.html`
> fait foi et remplace l'ancienne règle « couleur d'état pleine »).**
> **La bande haute porte la couleur de la NATURE, jamais celle de l'état.**
> Promi **bleu #3A54FF** · Chiche **framboise #FA2258** · Nuée **mauve #8A5CF0** — quelle que
> soit l'échéance. **L'état vit dans la LIGNE (le trait), et nulle part ailleurs.** Raison : si
> la bande virait à l'orange quand l'échéance approche, la nature disparaîtrait de l'écran au
> moment où elle compte le plus. Le champ dit la nature, la ligne dit l'état — c'est la loi de
> tout le document, sans exception. **Seule exception, et elle dure une seconde :** à l'instant
> où une parole est tenue, le champ entier passe au **menthe**, la dalle se recompose plus
> grande, le mot tombe — puis retour à la couleur de nature (§6 du moodboard, règle 9 de sa §9).

Une fiche a **deux tons**. La **zone haute** (la bande) est en **couleur de NATURE pleine**.
Le **corps**, celui qui porte le contenu, est **plus clair**. C'est la respiration de la fiche :
la matière en haut, la parole en bas. Ce n'est **ni un voile ni un dégradé — deux aplats
francs**. La dalle du haut reste **nette, opacité 1**.

```
                bande (nature)   corps clair   corps sombre
Promi           #3A54FF          (à relever au moodboard H, §3)
Chiche          #FA2258          (à relever au moodboard H, §3)
Nuée            #8A5CF0          #F3E9FE       #1B1426
tenu (1 s)      #2BE88C = l'instant de la parole tenue, exception unique
```

**Le contenu du corps passe en encre** (le moodboard le pose en blanc sur couleur
pleine ; sur un corps clair ce serait illisible). C'est la conversion de **ph-8**
appliquée à **tous les états** :

```
texte du corps              #06231A (ou l'encre de l'état)
fond de la carte message    rgba(6,35,26,.1)    (au lieu de rgba(255,255,255,.15))
filet sous la carte         rgba(6,35,26,.2)    (au lieu de rgba(255,255,255,.24))
contour des pastilles       rgba(6,35,26,.26)   (au lieu de rgba(255,255,255,.34))
panneau du geste            rgba(6,35,26,.1)    (au lieu de rgba(255,255,255,.14))
filet de la barre           rgba(6,35,26,.24)   (au lieu de rgba(255,255,255,.3))
```

**La zone haute et ses éléments — mot-marque, FERMER — gardent le traitement du
moodboard sur couleur pleine (blanc).** Le bitonal est **la seule exclusion** au
« moodboard à la lettre » pour la fiche : tout le reste (structure, hauteurs,
tailles, carte message, pastilles, tracé) tombe à zéro.

### Les traits

Ils prennent la teinte de la dalle **décalée de 150° en teinte**, saturation
remontée à 55 % minimum. Cela garde la famille chromatique du monde choisi tout
en évitant le ton sur ton.

> **⚠ Point ouvert** — l'utilisateur juge ce décalage parfois hors palette.
> Une décision est attendue : soit conserver le décalage, soit piocher une
> couleur réelle de la palette du monde actif. **Ne pas trancher seul.**

### Le trait sur le champ — TRANCHÉ (Tom, 18 août 2026)

**Le trait posé sur un champ plein porte TOUJOURS la teinte claire de la nature, jamais sa
couleur pleine** — c'est le §2.1 bis de `PROMI-SPECIFICATIONS.md`, et il fait loi.

**Les cadres clairs du moodboard qui peignent le trait en couleur pleine sont une ERREUR DE
DESSIN, pas une règle.** Vu en clair : le trait y prend exactement la couleur de l'aplat et
**disparaît**. Ce n'était donc pas une question ouverte (ancienne Q4) — c'était un défaut
du moodboard, et le document avait raison contre lui.

**Le seuil est celui du §3 : 42 de luminosité entre le trait et le champ qui le porte.**
Il vaut pour TOUS les traits du produit — fiche, page +, carte d'Index, bandeau du Fil,
encart de Nuée, l'instant — et il est contrôlé par `redteam_tonsurton.py`.

**Une Nuée** prend la teinte de **sa dernière dalle plantée** — ses traits
changent à chaque nouveau Promi.

### La règle de la couleur qui gagne sa place

**Un élément coloré ne reste que s'il porte du SENS ou une ACTION.** S'il ne fait que
décorer, il dégage — même s'il est joli. (Ex. lot 17 : l'anneau Aura reste, sa couleur
DIT quelque chose — proportions tenu/en cours/à tenir ; le rose des boutons commenter/
joindre est parti, il ne disait rien.) Corollaire du cadre **ÉVIDENT → SIMPLE → BEAU** :
un écran se lit d'un coup d'œil ; beau ≠ chargé ; un seul trait coloré qui sert vaut mieux
que cinq qui bruitent.

> **⚠ UN CHAMP BLANC N'EXISTE JAMAIS.** (Décision Tom, 29 août 2026, **sans exception**.)
> **Le champ porte toujours sa couleur pleine de nature** — bleu `#3A54FF` pour un Promi,
> framboise `#FA2258` pour un Chiche, mauve `#8A5CF0` pour une Nuée — **dans les deux thèmes
> et sur TOUS les écrans** : fiche, page +, carte d'Index, bandeau du Fil, Nuée, **gardé de
> côté**. **La dalle se pose dessus, jamais à la place.**
> **Ce qui manque à un gardé de côté, c'est la MATIÈRE, jamais la couleur** — Q83 le disait
> dans la même phrase : *« sa carte d'Index garde le champ de nature en pointillé, sans
> matière »*. Les cadres qui le dessinent sur le corps nu (26/27, 74) sont des erreurs de
> dessin, de la même famille que les cadres clairs au trait invisible.
> Contrôlé par **`redteam_champ.py`** : au-dessus du trait, aucun pixel ne porte une couleur
> de corps, aucun champ n'est transparent, et **chaque peintre DÉCLARE ce qu'il a versé**
> (`data-champ`) — seul juge possible sur une Nuée vide, dont les graines crème du §10.6
> tombent pile sur la couleur du corps.

### Interdits absolus sur les couleurs

- **Jamais de trait neutre ou gris.** Un filet sans couleur est un défaut.
- **Jamais de ton sur ton.** Vérifier l'écart de luminosité, seuil 42.
- `-webkit-text-fill-color` doit **toujours** valoir la même chose que `color` —
  sinon le texte se peint dans la couleur du fond.
- Sur un aplat d'état, l'encre s'inverse : `#06231A` sur menthe, `#FFFFFF` sur
  orange.

---

## 4. Les dalles — règles absolues

**L'IDENTITÉ EN HAUT, LA DIVERSITÉ EN BAS.** La **bande du haut** porte l'identité
de la chose qu'on regarde — c'est une **couleur signal**, elle ne dépend JAMAIS du
contenu : une fiche de **Nuée** a une bande **mauve**, un **Promi** une bande **bleue**,
un **Brouillon** une bande **terracotta**. Le **fil**, lui, porte les Promi, et
**chaque Promi garde son monde** (dalles variées — c'est ce qui le rend vivant, comme
la v592). Les deux règles cohabitent : la bande de Nuée est donc mauve même si ses Promi
sont d'autres mondes ; les dalles du fil restent leurs vraies dalles. Idem sur la
**page + Nuée** : la bande de création est mauve.

> **⚠ L'IDENTITÉ MAUVE PORTE SUR LA TEINTE, JAMAIS SUR LA FORME.** La bande d'une
> Nuée montre de **vraies dalles du moteur** (`Toile.dalleTrame`), **teintées mauve**
> — jamais des polygones/hexagones reconstruits. Reconstruire une forme de dalle est
> une violation frontale de la règle 1 (c'est l'erreur du lot 15, corrigée au lot 16).

> **⚠ LA DALLE PORTE LE MONDE. L'ACCENT PORTE LA NATURE.** (Décidé lot 25, vaut pour
> les trois natures — Promi, Chiche, Nuée.) Une **dalle n'est JAMAIS teintée par sa
> nature** dans les **listes** (Index, Fil) ni sur la **Toile** : la dalle appartient
> au **monde** choisi au Studio, jamais à la nature — c'est la diversité des dalles qui
> rend la Toile vivante, pas une couleur par catégorie. La **nature se lit à l'ACCENT** :
> pastille, libellé, contour, badge — **en framboise pour un Chiche**, bleu pour un Promi,
> mauve pour une Nuée. Sur la **Toile : rien**, on n'y touche pas (interdit §9).
> **Seule exception (déjà actée) : la BANDE HAUTE d'une fiche** est teintée par la nature
> — c'est là que l'identité s'affirme. Fiche Nuée mauve, fiche Chiche framboise, fiche
> Promi bleue. Cette exception ne s'étend PAS aux listes ni à la Toile.

> **⚠ Q30 · LA TEINTURE EST BORNÉE À LA BANDE HAUTE.** (Décision Tom, 18 août 2026.)
> **Dans la bande haute d'une fiche et dans le champ de la page + — et NULLE PART
> AILLEURS — la dalle prend la palette de sa nature** (§1.2 de `PROMI-SPECIFICATIONS.md` :
> trois teintes par nature). Ce n'est pas une règle nouvelle : c'est **l'exception déjà
> prévue ci-dessus** — la bande haute est teintée par la nature, c'est là que l'identité
> s'affirme — poussée jusqu'à la dalle qu'elle porte.
> **Pourquoi c'est obligatoire là :** une dalle bleue sur un champ bleu est un **bug**, pas
> un parti pris. Mesuré sur les huit cadres à champ `#3A54FF` de la page + : écart de
> luminosité **16 en médiane**, là où le seuil est **42** (§3). Après remappage sur la
> rampe du §1.2 : **109**. Zéro ton sur ton dans la bande haute, sans exception.
> **Pourquoi c'est interdit partout ailleurs :** dans l'**Index**, le **Fil**, la **Toile**
> et l'**encart d'une Nuée**, la dalle garde **le monde, et rien d'autre**. Une dalle
> teintée dans une liste serait **un classement par nature** — exactement ce que le produit
> refuse. La règle du §4 (« LA DALLE PORTE LE MONDE, L'ACCENT PORTE LA NATURE ») reste
> entière : la teinture ne l'entame pas, elle vit dans son exception.
> **LA FORME NE BOUGE JAMAIS** — c'est toujours la vraie dalle du moteur (règle 1
> ci-dessus) ; on ne remappe que la LUMINOSITÉ sur les trois teintes de la nature. Aucun
> polygone n'est reconstruit.

> **⚠ LE VIDE EST UN DÉFAUT DU PLANCHER — PAS UN DÉFAUT GÉNÉRAL.**
> (Décision Tom, 19 août 2026, **corrigeant une première formulation trop large**.)
> **Ne remplis pas le champ partout. Lis ce paragraphe en entier avant de toucher au sujet.**
>
> **Ce qui est normal :** une fiche et une page + gardent **la boîte du §2.7** — dalle
> centrée, couleur de nature autour. C'est le moodboard, et il a raison. Relevé sur
> `promi-nuee-toile.html` : l'espace entre le bas des dalles et le trait est **correctement
> occupé jusqu'à trois éléments** (cadres 0 à 6).
>
> **Ce qui est un défaut :** **au PLANCHER**, un bandeau de couleur nue se creuse **dans les
> ventres de l'onde** (cadres 8 et 10 de la planche, « Quatre » et « Sept »). Là, la matière
> doit **descendre jusqu'à la vague, épouser ses creux**, et ne jamais laisser de couleur nue
> entre elle et le trait — découpée par le chemin de l'onde, la nature dessous.
>
> **Pourquoi c'est propre au plancher, et où chercher ailleurs :** au plancher, `base` cesse
> de descendre pendant que le NOMBRE d'éléments continue de monter. La Toile d'une Nuée tire
> sa taille de ce nombre : ses dalles rapetissent, la vague ne bouge plus, le vide se creuse.
> Sur une fiche et sur la page +, la boîte de la dalle est **calculée à partir de la base**
> (`dh = base − amp − 100`) : le rapport entre la matière et la vague ne se dégrade jamais.
> **Mesuré, pas supposé** — `scratchpad/mesure_vide.py`, deux thèmes, tous les écrans.
> Planchers : **196** pour une fiche et pour la page + (§2.5), **176** pour une Nuée (§9).
> Aucune base de fiche n'atteint le sien (262 · 372 · 376) ; la page + l'atteint sur un
> **choix ouvert** ; une Nuée l'atteint **à partir de quatre éléments**.
>
> **Trois exclusions, validées par Tom :** l'**instant** (la couleur du champ y EST le sujet —
> en couverture, le menthe disparaît ; Q58 **clos**), un **gardé de côté** (pas d'aplat, donc
> pas de champ à remplir), une fiche **à photo** (la photo remplace la matière et doit rester
> sous l'entête, Q53 ; Q57 **clos**).
> **Deux corollaires :** la bande haute **teinte** sa dalle (Q30, §4 ci-dessous — la fiche ne
> l'appliquait pas), et le **mot-marque a deux encres** (§10.6 généralisé : il suit ce qui est
> peint sous lui, crème ou encre, jamais un troisième ton ; Q59).

> **⚠ UNE NUÉE SE LANCE EN TRAÇANT LE TRAIT ENTIER.** (Décision Tom, 19 août 2026.)
> Pas une moitié : **0 → 390**, le **mode complet** du §2.6 — celui d'une parole tenue.
> Une Nuée n'est promise à personne ; **personne ne vient à sa rencontre**, donc une
> demi-courbe n'aurait aucun sens. Trait entier donné = ni chevron, ni points : plus rien ne
> manque. Un Promi et un Chiche gardent leur moitié — là, l'autre trace la sienne.

> **⚠ UN SEMIS EST DÉTERMINISTE — ET UNE DALLE SE REND UNE FOIS.** (Exigence Tom, 19 août 2026.)
> **1 · Même Nuée, même semis.** À chaque ouverture, dans les deux thèmes, sur n'importe quel
> appareil : **quelle dalle occupe quelle case, et où**, ne change jamais. Une Toile qui
> changerait de composition entre deux ouvertures ne serait plus la Toile de CETTE Nuée.
> Un placement se tire donc des **ids** et du nombre d'éléments — **jamais** de `Math.random`,
> jamais d'une horloge, jamais de la taille du canevas (les cotes sont en écran 390).
> Contrôlé par `scratchpad/semis_determin.py` : 3 ouvertures × 2 thèmes × 2 densités de pixels.
> **Ce qui RESPIRE, et qu'il ne faut pas confondre avec le semis :** `Toile.dalleTrame` rend
> la matière avec `performance.now()`, et il **recadre au plus juste sur l'alpha** — le format
> de la dalle bouge donc d'un rendu à l'autre, partout dans le produit. **Un contrôle qui
> compare les PIXELS, ou le rectangle peint, mesure la respiration du monde, pas le semis** —
> mesuré : 3 empreintes distinctes sur 3, sur douze configurations. On compare **la case**.
> **2 · Une dalle se rend une fois, pas une fois par case.** `dalleTrame` refait l'attribution
> pondérée **pixel par pixel**. L'appeler par case d'une grille, à chaque repeinte, a fait
> ramer l'app au point que `redteam_toile` **n'a pas rendu la main pendant dix minutes**, deux
> fois de suite — et que `releve-S5` a sorti un rouge sur un canevas pas fini de peindre.
> **Un cache par id, le temps de la passe** : mêmes pixels, un seul calcul. **Cette règle vaut
> pour tout rendu en grille** — elle reviendra sur l'Index et le Fil dès qu'ils afficheront
> beaucoup de dalles.

> **⚑ UNE DALLE EST FIGÉE À SA PLANTATION — POSÉ LE 4 septembre 2026 (feu vert Tom).**
> Un Promi porte `monde = {m:design, p:palette, h:teinte}`, figé par la fabrique `P()` au
> moment où il est planté. **`dalleTrame(cv, id, k, monde)` prend un 4ᵉ argument facultatif** :
> absent, elle se comporte exactement comme avant ; présent, elle peint la dalle dans le monde
> de SA plantation. Elle sauve et restaure `theme`, `palKey`, `hueShift` **et `_palLit`** —
> ce dernier est un **mémo** de la palette calculée : sans l'invalider à l'aller la palette de
> l'appelant fuit dans la dalle, sans le restaurer au retour celle de la dalle fuit dans la
> Toile. **`Toile.mondeCourant()`** rend `{m,p,h}` en lecture seule.
> **Les Promi d'avant ce lot** prennent le monde courant, figé à ce moment
> (`window._figeMondesManquants()`, idempotente) : **rien n'est tiré de leur date.**
> Preuve : `scratchpad/preuve_monde.py` — quatre contrats, dont **aucune fuite**.
> ⚠ **Rien n'est encore CÂBLÉ** : les six appels existants passent trois arguments, donc aucun
> pixel n'a bougé. Brancher les peintres est un lot à part.
>
> **⚠ Ce que ce paragraphe disait avant, et qui était vrai jusqu'au 4 septembre :**
> On a longtemps cru l'inverse. **C'est faux :** un Promi ne porte **aucun champ de monde**
> (`Object.keys(p)` n'en a pas), et `theme`, `palKey`, `hueShift` sont **trois variables de
> module, globales**. La même dalle repeinte dans trois mondes donne trois remplissages
> différents — 4289 · 3963 · 1912 sur la dalle 125, boîte et tons compris
> (`scratchpad/monde_fige.py`). **Changer de monde au Studio repeint TOUTE la Toile, les
> anciennes dalles comprises.**
> **Le figer est une DÉCISION DE PRODUIT non prise**, et elle touche le moteur (§9) :
> ne rien changer sans demande explicite. La forme minimale est écrite dans
> `ETAT-DES-LIEUX.md` — un 4ᵉ argument facultatif à `dalleTrame`, sur l'idiome de
> sauvegarde/restauration que la fonction porte déjà.

1. **Toujours la vraie dalle du moteur**, rendue par `Toile.dalleTrame(canvas, id, 1)`.
   Jamais un polygone, jamais un hexagone, jamais une photo, jamais une approximation.
   La bande de Nuée n'y échappe pas : ce sont de vraies dalles, seulement **teintées**
   mauve (la teinte porte l'identité, pas une forme inventée).
2. **L'échelle est toujours 1.** Les valeurs 6 ou plus cassent les mondes
   mosaïque, braille, pixel et gravure — ils retombent sur un rendu polygonal.
3. **La dalle est au premier plan.** `opacity: 1`, `filter: none`,
   `mix-blend-mode: normal`, `z-index` supérieur au voile de couleur.
   Le voile est le `background` du bloc, jamais un calque par-dessus.
4. **Aucun filtre, aucun voile, aucun masque** ne passe devant une dalle.
5. **Peindre après insertion.** Les canevas ne sont mesurables qu'une fois
   disposés : relancer `peintMinis()` à 0, 60, 200 et 600 ms.
6. **Jamais de dalle en fond animé** sur un écran qui montre des dalles de
   référence.

**Sujet contre ambiance — la nuance qui clôt le débat (lot 2B).** Les règles 3, 4
et 6 visent la **dalle-sujet** : celle qu'on montre et qu'on référence (dalle de
fiche, de tuile, de partage). Elle est à **opacité 1, sans voile ni masque, jamais**.
Un **fond d'ambiance** — une dalle décorative derrière un contenu qui **n'est pas
elle** (ex. la trame de la page +, où le sujet est **la phrase**) — **peut porter un
masque** : là, la **lisibilité du contenu prime**. Ne pas confondre les deux, ne pas
rouvrir le débat : sur la page +, la trame reste masquée (décidé au lot 2B).

**Les huit mondes :**
gratuits — Encre · Mosaïque · Touffe · Braille · Pixel
Cercle — Terrazzo · Gravure · Sillons

> **⚠ ÉCLATS N'EXISTE PAS AU STUDIO.** (Décision Tom, 29 août 2026 — Q102.) Ce fichier en
> listait **neuf**. `PROMI-SPECIFICATIONS §10.4` écrit l'inverse, noir sur blanc :
> *« `RD = {pixel, braille, sillons, gravure, mosaique, encre, terrazzo, touffe}`.
> **Éclats n'existe pas.** »* — et l'app ne le montre nulle part (`order` en compte huit).
> **Son code est conservé** (`WL`, `_lockW` le connaissent) ; **il n'apparaît pas au Studio.**
> Ne pas le remettre dans un rail « parce qu'il est dans la table ».

---

## 5. Les composants communs

Ces éléments sont **identiques sur tous les écrans**. Ne jamais en créer une
variante locale.

| Composant | Règle |
|---|---|
| **Le geste** | 118 px de haut, deux points, un trait. Toujours **entier**, jamais rogné ni superposé. Le trait part **du centre du rond gauche**, pas du doigt. Courbes quadratiques, jamais de segments droits. |
| **Peaufiner** | 62 px, en bas de chaque fiche. Même typographie, même filet, même place. Porte l'icône de partage à droite. |
| **✕ Fermer** | En haut à droite, `top: 50px`, avec le texte `FERMER`. |
| **Le mot-marque** | « Promi » en Fraunces, haut à gauche, 20 px. 15 px dans les images partagées. |
| **« Moi »** | Toujours **premier** de la liste des destinataires, avec son avatar dégradé. Dans une Nuée : « tout le monde » passe devant, « Moi » ensuite. |
| **Les boutons ronds** | Partager, commenter, joindre : **icône seule**, jamais de texte à côté. |

> **⚠ §13 · SUR UNE FICHE DE NUÉE, PEAUFINER NE S'OUVRE QU'EN TOUCHANT SA BARRE.**
> **Partout ailleurs c'est l'inverse.** C'est la règle unique du produit, et le document
> prévient : *« sans cette exception écrite, le comportement sera implémenté comme les autres
> écrans »*. Sur cette page, **le doigt qui descend fait défiler LE FIL, pas les réglages** :
> l'encart, les Noyaux, le titre remontent et disparaissent sous le trait, les Promi prennent
> toute la place, et il ne reste qu'une bande de Toile de **114 px** (base 58, amplitude 16).
> **Cet état est une CLASSE que le code pose, jamais une géométrie qu'il vient de produire**
> — c'est le piège du §8, payé deux fois sur la page +.
> **C'est aussi la butée du défilement, pas une valeur de la formule :** un contrôle qui
> vérifie `base = max(176, 460 − 86 n)` doit l'EXCLURE, sinon il le compte comme une erreur.
> Et **la Toile qu'on y voit est LA MÊME, simplement remontée** — jamais une seconde
> composition.

### ⚑ LA GRAMMAIRE DES TRAITS ET DES CONTOURS — UNE SEULE RÈGLE

> **Décision Tom, 2 septembre 2026.** *« Dans toute l'app revoir les traits et contours pour
> ne pas créer de décalages visuels avec les autres éléments, et que le cadre paraisse plus
> marqué que le reste — le reste s'y adapte donc. »*

**Trait de 2 px, couleur du corps, rayon = hauteur ÷ 2.** Relevé sur l'app et sur le Studio,
écran par écran : la règle existait déjà presque partout.

```
le plateau        342 × 60   trait 2   rayon 30      (= h ÷ 2)
la recherche      270 × 52   trait 2   rayon 26      (= h ÷ 2)
le tri             52 × 52   trait 2   rayon 26      (= h ÷ 2)
le sélecteur      167 × 44   trait 2   rayon 22      (= h ÷ 2)
Peaufiner         342 × 62   trait 2   rayon 31      (= h ÷ 2)
Inviter/Partager  168 × 62   trait 2   rayon 31      (= h ÷ 2)
le disque          44 × 44   trait 2   rayon 50 %
le grand panneau  342 × 253  trait 2   rayon 30      un panneau, pas une pilule
```

**Le cadre ne se soustrait pas : c'est le reste qui monte jusqu'à lui.** Quatre familles
s'en écartaient et faisaient paraître le plateau « à part » alors qu'il était le seul à la
règle — les sept rangées des Réglages à **3 px / rayon 22**, le tri du Fil et les boutons de
l'Aura dans une **seconde crème** (`231,229,223` au lieu de `244,238,225`), les rangées
d'Arranger avec un filet de **1 px à 13 %** large de **346 dans un cadre de 342**, et les
cinq pastilles du Cercle à **1 px / rayon 10** dans un bleu qui n'est la couleur d'aucun
autre contour. Contrôlé par un balayage qui vérifie les trois cotes sur dix écrans.

### ⚑ UN RÉGLAGE VIT LÀ OÙ VIT CE QU'IL RÈGLE

> **Décision Tom, 31 août 2026. Née du pinceau, elle vaut pour tout réglage à venir.**

**LE STUDIO NE PORTE QUE CE QUI EST VRAIMENT GLOBAL.** Ce qui appartient à **une** parole se
choisit **là où cette parole se fait** — jamais dans un écran de préférences.

Le test est simple et il se pose avant d'ajouter quoi que ce soit au Studio :
**est-ce que ce réglage a un sens différent d'un Promi à l'autre ?** Si oui, il n'a rien à
faire au Studio, quelle que soit la commodité.

```
AU STUDIO — global               le monde · la palette · l'écran (sombre/clair) · le texte
À LA PAGE +, à la création       ce qui appartient au Promi qu'on plante
DEPUIS LA FICHE, dans Peaufiner  on le reprend — Promi, Nuée, gardé de côté
```

**Le cas qui a fondé la règle — LE PINCEAU.** Le choix du trait avait été posé au Studio :
il s'appliquait donc **à toutes les fiches d'un coup**, ce qui interdisait exactement ce que
le produit veut — donner son trait à *ce* Promi, à *cette* Nuée. Il est passé à la **page +**,
à la création, et se reprend **depuis Peaufiner, haut de liste**.

**Corollaire de dessin, et il est grand :** un écran qui perd un réglage perd aussi ce qui
n'était là que pour le montrer. Le trait du §2.1 n'existait au Studio que pour porter le
pinceau qu'on essayait ; sans lui, **l'onde disparaît et la Toile prend tout l'écran**.
Ne pas garder une forme par habitude quand sa raison d'être est partie.

---

### ⚑ UN AJOUT VALIDÉ, HORS INVENTAIRE — et comment on l'écrit

> **Décision Tom, 20 août 2026. Elle clôt Q75.**

La méthode du portage est « **écrire chaque écran depuis son inventaire** ». Elle a un angle
mort : **un écran peut porter une FONCTION que son cadre ne montre pas.** Le moodboard dessine
un écran **au repos** — il ne dessine pas ce qu'un doigt fait apparaître.

**On ne supprime jamais une fonction parce que le cadre ne la montre pas.** On la sort du
repos, et on l'écrit comme **ajout validé, hors inventaire** :

1. **Le repos est celui du cadre**, au pixel. Rien de l'ajout n'y paraît, et l'ajout ne
   décale **aucune** cote du cadre.
2. **L'ajout apparaît AU BESOIN**, sur un geste, et il se referme.
3. **Il est nommé dans `ETAT-DES-LIEUX.md`** — ce qu'il est, ce qui le déclenche, et la
   décision qui l'a validé. Sans cette ligne, le portage suivant le prendra pour un résidu
   et le supprimera.
4. **Son contrat de test vise le GESTE, jamais le repos.** Un contrôle qui exige l'ajout
   visible au repos contredit le cadre : il se réécrit au niveau de la décision (§7).

**Le cas qui a fondé la règle — LE FIL.** Le **cadre 76** montre cinq bandeaux nus, 358 × 128,
de 140 en 140 : **aucune rangée « TENIR · REPORTER »**. Mais le Fil est **le seul endroit d'où
l'on tient une parole sans ouvrir une fiche**, et cette fonction ne se perd pas. Donc : le
bandeau au repos est **exactement celui du cadre**, et **le geste apparaît au besoin** —
un **appui maintenu** sur le bandeau déplie sa rangée, un toucher bref ouvre sa fiche.
Cet ajout est **validé, hors inventaire**.

---

## 6. La typographie

```
Bricolage Grotesque   titres, libellés de section   700/800
Apfel                 champs, interface
Fraunces              signature « Promi »
```

**Tailles minimales :** rien en dessous de 12 px. Aucune opacité sous 72 % sur du
texte lisible.

> **⚠ AUCUNE GRAISSE HORS DES FACES EMBARQUÉES.** (Lot du 19 août 2026.)
> En navigateur, une graisse absente se substitue **en silence** — la plus proche, ou une
> oblique synthétique. **En Swift, elle casse.** Le prototype étant la spécification du
> portage, tout couple demandé doit exister en `@font-face`. **Six faces, et six seulement :**
>
> ```
> Fraunces 600 normal · Fraunces 600 italique
> Bricolage 600 · Bricolage 700
> Apfel 400 · ApfelMid 500                    (aucune italique en Apfel ni ApfelMid)
> ```
>
> **LA TABLE DE REPORT** — chaque couple absent va sur le plus proche embarqué, **sans
> changer la hiérarchie visuelle** :
>
> ```
> Apfel 500 · 600 · 700 · 800  →  ApfelMid 500    la graisse existe, dans la famille qui la porte
> Apfel 400 italique           →  Apfel 400       l'oblique était synthétique
> ApfelMid 400                 →  Apfel 400       la graisse 400 existe, dans Apfel
> Bricolage 800                →  Bricolage 700   la plus grasse embarquée
> Bricolage 400                →  Bricolage 600   la plus légère embarquée
> ```
>
> Contrôlé par **`redteam_polices.py`**, qui lit les `@font-face` du fichier — si on embarque
> une face, le contrôle la connaît au passage suivant, sans qu'on touche au test.
> **Appliqué par le bloc `lot-POLICES`, en JavaScript et pas en CSS** : le couple dépend de
> DEUX déclarations qui vivent rarement dans la même règle (réécrire « 800 → 700 » à
> l'aveugle enverrait un `Apfel 800` sur `Apfel 700`, tout aussi absent), et le §9 interdit
> de nettoyer le CSS. **La passe se RELIT, elle ne fige pas** : sur un élément déjà touché
> elle retire d'abord son propre inline, relit ce que la cascade dit vraiment, puis décide.
> Sans quoi une graisse lue trop tôt reste gelée et **la hiérarchie change** — mesuré :
> « Peaufiner » figé à 600 au lieu de 700.
> ⚠ **Le document écrit « Apfel 500 » à plusieurs endroits** (§5, §12). C'est la graisse
> voulue, mais ce couple n'existe pas : c'est `ApfelMid 500`. Voir QUESTIONS.md · Q68.

---

## 7. Méthode de patch — obligatoire

### Avant toute modification

1. Lire le code existant **avant** de le modifier. Ne jamais deviner.
2. Vérifier qu'une règle CSS s'applique réellement : le fichier contient
   **2 400 règles dont 54 % sont mortes**. Une déclaration peut être écrasée
   par une règle postérieure sans que ce soit visible.

### La méthode

```python
# Toujours ce motif, jamais un replace aveugle
assert S.count(old) == 1, "motif absent ou multiple"
S = S.replace(old, new)
```

### Après toute modification

```bash
# 1 · vérifier la syntaxe JS
python3 -c "import re,io; S=io.open('app.html',encoding='utf-8').read();
io.open('check.js','w',encoding='utf-8').write(''.join(m.group(1)
for m in re.finditer(r'<script[^>]*>(.*?)</script>',S,re.S)))"
node --check check.js

# 2 · les batteries
python3 redteam_ecrans.py     # 142 contrôles — la principale
python3 redteam.py            # 15
python3 redteam2.py           # 10
python3 redteam3.py           # 18
python3 redteam_demande.py    # 19
python3 redteam_toile.py      # 16
python3 redteam_geste.py      # 13
python3 redteam_verbe.py      # 6 — la phrase montre TOUJOURS son verbe + bascule
python3 redteam_filets.py     # 0 filet parasite — AUCUN trait horizontal hors moodboard
python3 redteam_vide.py       # 61 — UN ÉCRAN N'EST JAMAIS VIDE, en enchaînant les écrans
python3 redteam_air.py        # 391 paires — L'AIR ENTRE LES TEXTES ne se resserre jamais
python3 redteam_champ.py      # 32 — UN CHAMP BLANC N'EXISTE JAMAIS, il porte toujours sa nature
```

**Aucune livraison si une batterie régresse.**

> **⚠ LES BATTERIES SE PASSENT EN SÉRIE, JAMAIS TOUTES EN PARALLÈLE.** (Mesuré, 20 août 2026.)
> Douze Playwright lancés d'un coup font ramer la machine, et **les rouges qu'on lit alors
> sont faux** : boîtes à 0 × 0, « 0 pastille trouvée », classes d'un écran qui bavent sur le
> suivant. Relevé : `champs` 11/21, `pastilles` 8/12, `enchaine` 17/24, `tonsurton` 23/26,
> `fonctions` 20/22 — **et 22/22, 12/12, 24/24, 26/26, 22/22 en les repassant une par une,
> sans toucher à une ligne.** C'est le même piège que le §8 (« l'app rame, les captures
> échouent ») : un contrôle qui mesure une machine saturée ne mesure pas le produit.
> **Deux ou trois à la fois au maximum.** Un rouge apparu dans une passe parallèle se
> reconfirme en série avant d'être cru.

> ### ⚠ UN CONTRÔLE QUI ENCODE UNE RÈGLE ABANDONNÉE SE MET À JOUR AU NIVEAU DE LA DÉCISION
> **Jamais en modifiant le comportement pour le faire passer.** (Décision Tom, 18 août 2026,
> à la livraison de la section 4.)
>
> Une batterie est un contrat. Mais un contrat peut être **périmé** : il arrive qu'un
> contrôle vérifie une règle que le produit a **abandonnée** depuis. Trois cas déjà vus —
> « sens », « quand », et « **seuls les urgents ont un aplat** », qui supposait que l'état
> vivait dans le FOND du bloc d'Index. **Il vit dans la LIGNE** : le champ dit la nature, la
> ligne dit l'état — c'est la loi du produit (§3). Le contrôle était périmé, pas l'écran.
>
> **La marche à suivre, dans cet ordre :**
> 1. **Nommer la règle** que le contrôle encode, et **la décision** qui l'a remplacée.
>    S'il n'y a pas de décision écrite, il n'y a pas de contrôle périmé : c'est une régression.
> 2. **Réécrire le contrôle au niveau de la nouvelle règle** — même intention, nouveau nœud,
>    nouvelle propriété. « Seuls les urgents ont un aplat » est devenu « aucune carte n'est
>    peinte d'une couleur d'état ». Le contrôle continue de protéger la même chose.
> 3. **Garder la version d'origine** à côté (`sauvegardes/redteam_*-avant-S*.py`).
> 4. **Le dire dans la livraison**, en propres termes : *j'ai réécrit un contrat de test*.
>
> **UNE BISSECTION NE VAUT QUE SI CHAQUE CORRECTIF EST RÉTABLI EN ENTIER.** (Décision Tom,
> 18 août 2026.) Un correctif en trois morceaux — une règle, un champ, un libellé — rétabli
> pour un tiers seulement **innocente un coupable**. Vécu : le retrait de « URGENT » faisait
> passer la section 2 de 0 à 212 écarts ; je n'ai rétabli que le réglage de Peaufiner, pas le
> champ du formulaire ni le mode de la Toile, et j'ai conclu qu'il n'y était pour rien. J'ai
> ensuite cherché ailleurs pendant cinq mesures. **On réapplique dans l'ordre, un correctif
> entier à la fois, et on mesure après chacun** — jamais par bissection sur des suspects.
>
> **⚠ UN CONTRÔLE QUI COMPTE DES PIXELS SUR UN CANEVAS MESURE LA RESPIRATION DU MONDE.**
> (Décision Tom, 19 août 2026.) `Toile.dalleTrame` anime la matière avec `performance.now()`
> **et recadre au plus juste sur l'alpha** : ni les pixels ni même le format d'une dalle ne
> se répètent d'un rendu à l'autre. **Un contrôle bâti dessus flotte, et son flottement n'est
> ni le hasard ni les polices : c'est le TEMPS.** Trois l'ont fait pendant tout le projet —
> « Mes Promi : les intitulés restent », « le % s'affiche », « le % porte la double encre ».
> **La parade : comparer LA COMPOSITION, pas la peinture.** L'app publie ce qu'elle vient de
> composer — `window._plancheComp`, `window._noyauSig`, `window._sigEncres`,
> `window._nueeSemis` — et le contrôle lit ça. La règle protégée ne bouge pas ; c'est le nœud
> visé qui devient le bon. Les trois sont stables sur trois passages depuis.
>
> ### ⚠ QUAND UN CORRECTIF NE TIENT PAS, CHERCHER QUI D'AUTRE ÉCRIT LA MÊME PROPRIÉTÉ
> **Décision Tom, 3 septembre 2026. Le motif est revenu QUATRE FOIS en deux jours.**
>
> **Corriger une seule passe ne suffit jamais quand deux passes écrivent la même chose.**
> Deux propriétaires se défont l'un l'autre selon le moment ; le symptôme ressemble à du
> flottement temporel, et on perd des heures à durcir la mauvaise passe.
>
> ```
> echelle() / etatsDeCarte()   un inline retiré par celui qui ne l'avait pas écrit
> #shMode                       repris dans #shcSujet par l'ancien lot du partage
> #shcBarre                     posée à 700 par un lot, à 746 par l'autre
> enteteLisible / encreUn       le second repeignait le plateau par-dessus le premier
> ```
>
> **Ce que ça a coûté à chaque fois :** sur `etatsDeCarte`, TROIS correctifs successifs —
> rendre la passe idempotente, envelopper le moteur de l'Index, poser un observateur de
> largeur — et aucun ne pouvait rien, puisque le défaut était dans la passe d'à côté. Sur
> le partage, deux sondes de contrôle ont été **avalées par le conflit** et m'ont fait
> croire pendant trois essais qu'un contrat ne mordait plus.
>
> **La marche à suivre :**
> 1. **Piéger le peintre, ne pas relire le code.** On enveloppe `style.setProperty` sur le
>    nœud et on journalise la pile d'appels. Le plateau vide de la page + a été trouvé en
>    une minute par là, après une demi-heure de lecture stérile.
> 2. **Nommer UN propriétaire, et lui donner LE DERNIER MOT.** L'ordre d'appel suffit
>    souvent : `etatsDeCarte()` déplacée de la tête à la fin de `echelle()` a réglé seule ce
>    que trois correctifs n'avaient pas su faire.
> 3. **N'exempter que le geste fautif, jamais le traitement.** Sortir `.s4-et` de tout
>    `echelle()` a fait passer `releve-S4` de 0 à 34 écarts : le plancher ne s'appliquait
>    plus. On saute le RETRAIT, pas la décision.
> 4. **Une sonde qui « n'est pas prise » peut être avalée, pas manquée.** Vérifier qu'elle
>    s'applique vraiment — mesurer le nœud — avant d'accuser le contrôle.

> ### ⚠ UN CONTRAT RÉÉCRIT SE PROUVE CONTRE UN VRAI DÉFAUT — SINON IL NE MESURE PLUS RIEN
> **Décision Tom, 2 septembre 2026, née du lot du pinceau.**
>
> Réécrire un contrôle au niveau de la décision ne suffit pas : **il faut prouver qu'il mord
> encore.** Un contrôle réécrit qui ne trouve plus rien peut être juste — ou éteint. Les deux
> se ressemblent exactement dans un rapport vert.
>
> **La marche à suivre : on fabrique le défaut que le contrôle est censé attraper, on le pose
> dans l'app, on relance, et on vérifie qu'il est PRIS.** Puis on retire la sonde.
>
> **Le cas qui a fondé la règle.** `releve-S3` vérifie que rien ne déborde du cadre. La rangée
> du pinceau la faisait rougir 112 fois — son rail fait 1070 de large dans un conteneur en
> `overflow:hidden` de 390. J'ai réécrit le contrôle pour qu'il « confirme AU DOIGT », comme le
> §8 le prescrit pour les recouvrements : rouge à zéro, tout paraissait réglé. **Le contrôle
> était mort.** `.frame` rogne tout : **rien n'est jamais visible hors de l'appareil**, donc
> `elementFromPoint` ne trouve jamais rien, quel que soit le débordement. Prouvé avec une sonde
> de 150 px posée à x 300 dans un cadre de 390, sans ancêtre rogné : **zéro prise**. La bonne
> réécriture exempte ce qui se DÉCLARE (`data-glisse`, la rangée glissante de Q128 §3) et
> **sous condition** — le conteneur doit tenir dans le cadre ET rogner ; la même sonde est
> alors prise sur les 28 cadres.
>
> **Corollaire : le piège du §8 a une portée.** « Un débordement se confirme au doigt » vaut
> pour les recouvrements **DANS** la page, où un ancêtre rogné peut mentir. À la **frontière de
> l'appareil**, c'est le rectangle qui dit vrai — sur un vrai téléphone il n'y a pas de `.frame`
> pour rattraper ce qui sort.

> ### ⚠ UN JUGE QUI LIT LA VALEUR QU'IL VÉRIFIE NE VÉRIFIE RIEN
> **Décision Tom, 10 septembre 2026.** Vécu au portage de l'Orbite : le juge comparait la vitesse de
> rotation à `_aura.G.AUTO` — la valeur que l'app DÉCLARE. Changer la vitesse dans l'app changeait donc
> la cible avec : il aurait accepté n'importe quelle vitesse. **Une valeur décidée s'écrit EN DUR dans
> le juge** (`AUTO_DECIDE = 2π/120`, avec la décision qui la fixe), et le juge vérifie AUSSI que l'app
> déclare bien cette valeur. Vaut pour toute cote, toute durée, toute couleur : le juge porte la
> décision, l'app la respecte — jamais l'inverse.
>
> ### ⚠ UN CONTRÔLE QUI NE PREND PAS LA VERSION FAUTIVE NE VAUT RIEN
> **Décision Tom, 10 septembre 2026.** Vécu le même jour : le retour de l'empreinte SAUTAIT à la
> fin (déformé → lisse d'un coup). J'ai écrit un contrôle du « dernier pas » — et avant de juger la
> correction, je l'ai passé sur la version FAUTIVE : **il était vert.** Il comptait la **part des
> pixels qui changent** d'une image à l'autre ; or un retour lisse en change déjà beaucoup, d'un
> rien, à chaque image (médiane 17 %), et le saut (44 %) passait dessous. **Une part de pixels ne
> voit pas une AMPLITUDE.** Réécrit en écart moyen, en niveaux : la version fautive est prise à
> 8,45 niveaux, la corrigée passe à 0,46.
> **La règle : tout contrôle neuf se passe D'ABORD sur la version fautive, et il doit y ROUGIR —
> avant de servir à valider quoi que ce soit.** Le défaut que Tom a vu est la sonde : si le
> contrôle ne le prend pas, c'est le contrôle qui est faux, pas la correction qui est juste. Et
> **choisir la grandeur qui a la forme du défaut** : un saut est une amplitude, un débordement une
> position, une traîne une durée — pas un comptage qui les mélange.

> **Ce qui reste interdit :** desserrer un seuil, retirer un contrôle, ou changer le
> comportement de l'app pour faire passer un test. Un simple **changement de nom de nœud**
> (`.ix-bloc` → `.s4-carte`) ne relève pas de cette procédure : c'est un renommage,
> l'intention est intacte — on le note, on ne délibère pas.

> **⚠ Contrôles à seuil de pixels non déterministes (comme la convention Toile).**
> Deux contrôles Playwright échantillonnent un **canevas animé** et **oscillent** — un
> échec isolé ne prouve **rien**, il faut relancer :
> - `redteam_toile` — « Mes Promi intitulés » (width/police) : oscille 14↔16/16.
> - `redteam_geste` — « **l'anneau est peint à sa nouvelle place** » : sonde pixel sur le
>   **fond Toile animé de l'écran Partage** (shCanvas, échantillons à 1,3 s). Oscille
>   12↔13/13. **12/13 se reconfirme en relançant ; deux échecs de suite ne suffisent PAS
>   à conclure à une régression** (le dessin de l'anneau, lui, est correct — sonde isolée
>   +1513 stable). *À réécrire :* comparer l'anneau à sa propre référence, comme pour la
>   Toile, au lieu d'un seuil absolu. Voir `CHANTIERS.md`.

### Vérification visuelle Playwright

```python
viewport = {'width': 390, 'height': 844}
device_scale_factor = 2
pg.wait_for_timeout(6800)   # minimum après navigation
pg.evaluate("()=>{var o=document.getElementById('promiOnb');
  if(o){o.classList.add('gone');o.style.display='none';}}")   # passer l'onboarding
```

Pour vérifier une couleur peinte dans un canevas, **échantillonner les pixels** —
c'est la seule méthode fiable :

```javascript
const d = g.getImageData(0,0,c.width,c.height).data;
for(let i=3; i<d.length; i+=300) if(d[i]>10) n++;
```

---

## 8. Les pièges connus — les relire avant de déboguer

| Symptôme | Cause réelle |
|---|---|
| Une règle CSS « ne marche pas » | Une règle postérieure l'écrase. Chercher **toutes** les occurrences du sélecteur. |
| Le texte est invisible | `-webkit-text-fill-color` diffère de `color`. |
| La dalle est délavée | `opacity` ou `filter` posé par une règle groupée avec `.tracant`. |
| La dalle est polygonale | `dalleTrame` appelé avec une échelle > 1. |
| Un canevas est vide | `peintMinis` appelé avant que le canevas soit disposé. |
| L'app rame, les captures échouent | Un `MutationObserver` qui s'auto-déclenche : la fonction observée modifie une classe, ce qui réveille l'observateur. **Toujours comparer l'état avant d'agir.** |
| Un bloc ne bouge pas | Le CSS ne déplace pas les blocs. Réordonner le DOM en JavaScript. |
| `cur` est nul | Sur une fiche de Nuée, c'est `curNuee` qui porte le groupe. |
| Un sélecteur ne correspond à rien | `personSheet` vit sous `.frame`, pas sous `.device`. |
| Le scroll est bloqué | Un `position: sticky` avec `bottom: 0` qui change de position en s'ouvrant. |
| Une règle `position`/`max-width`/`z-index` ignorée sur un enfant **direct** de `#createSheet` | `#createSheet>*:not(#csTrameCv):not(.closeb):not(.pd-drift)` (≈ l.9017) impose `position:relative;z-index:1;max-width:84%` — spécificité 2 id / 2 classes, bat un `#createSheet .x`. **Parade :** `!important` sur `position/top/left/max-width`, comme le fait déjà `.closeb` (l.9163). |
| Un canevas **sort du cadre par la droite** dès qu'on le range dans un bloc | **`#tenirCv`, le canevas du geste.** La section 1 le cloue en `width:390px!important · max-width:none` dans un `#tenirZone` en `position:absolute · left:0 · width:390` (≈ l. 14095). `left:0` se lit dans son **bloc englobant** : tant que c'est `#detailPoster` (padding 0), il part de x = 0 et tout va bien. Dès qu'un conteneur **positionné** (`position:relative/absolute`) ou **padé** de Peaufiner ou de la page + devient son ancêtre positionné, le canevas de 390 px repart de l'origine de CE bloc — mesuré à **x = 27, dépassement 27 px** — et « rien ne déborde » passe au rouge, un élément par thème. **Un correctif `box-sizing:border-box` empire**, il resserre la boîte sans toucher au canevas. **Parade : ne jamais faire entrer `#tenirZone` dans un conteneur de réglages.** Le geste reste là où la section 1 l'a posé. Voir QUESTIONS.md · S2/Q12. |
| **Un balai « hors inventaire » emporte un élément vivant** | **LE CRIBLE EN BLOC — deux fois.** Masquer une FAMILLE d'éléments (`#addPromi, #addNuee, …`, `#promiForm>*:not(…)`) emporte toujours quelque chose qu'un doigt ouvre : `#addPromi` est le bouton où mène la bascule du geste, `#csChoix` est le panneau des trois cadres « Choix ouvert ». `redteam_verbe` est tombé de 6/6 à 4/6 les deux fois. **Toute règle de balayage se vérifie ÉLÉMENT PAR ÉLÉMENT avant d'être posée** — on énumère les nœuds de CET écran, jamais un conteneur, jamais une famille. |
| **Une cote mesurée sur elle-même fait osciller l'écran** | **LA COTE SE CALCULE, ELLE NE SE MESURE JAMAIS SUR ELLE-MÊME — deux fois.** Décider d'une hauteur d'après une hauteur rendue crée une boucle : `choixOuvert()` testait `#csChoix.height > 40`, les cotes du §5 passaient ses éléments en absolu, le panneau retombait à 0, « ouvert » devenait faux, les cotes revenaient au repos, les éléments repassaient en flux, il remontait. Le mot de trace était relevé à 236 **et** la phrase à 392 dans le même passage. **L'état est la classe que le code pose** (`.ouvert`), jamais la géométrie qu'il vient de produire. |
| Un panneau qu'un geste ouvre fait **osciller** l'écran d'une passe à l'autre | **Un état ne se lit JAMAIS dans la hauteur rendue du panneau.** Sur la page +, `choixOuvert()` testait `#csChoix.height > 40` : dès que les cotes du §5 passent ses éléments en absolu, le panneau retombe à 0 de haut → « ouvert » devient faux → les cotes reviennent au repos → les éléments repassent en flux → il remonte. Le mot de trace était mesuré à 236 **et** la phrase à 392 dans le même relevé. **La classe posée par le code (`.ouvert`) EST l'état** — la géométrie ne l'est jamais. |
| La phrase de la page + sort trop grosse, toujours large de 342 | **L'estimation du §2.8 est la règle, la mesure navigateur n'est qu'un garde-fou.** C'est l'estimation `Σ(car × taille × 0,53) + 32/pastille + 11/écart` qui a composé le moodboard : elle redonne 29 · 29 · 31 · 36 · 35 · 33 · 29 · 30 au caractère près. La mesure seule remplit toujours les 342 px. **On prend la plus petite des deux** : l'estimation compose, la mesure empêche une ligne de casser (et une ligne qui passe à la ligne décale tout de 32 px, §2.5). |
| Un geste n'ouvre plus rien après un « nettoyage » d'écran | **Un crible posé EN BLOC casse ce qu'un geste ouvre.** Porter un écran depuis son inventaire veut dire : *ce que le §5 ne liste pas ne se peint pas*. Mais cette règle vaut pour **l'état AU REPOS de l'écran courant**, jamais pour les panneaux qu'un doigt déplie — qui sont eux-mêmes **des écrans de l'inventaire** (« Choix ouvert · écrire un mot / choisir une personne / l'échéance », cadres 18 à 23 ; les contrôles dépliés de Peaufiner). Fermer un conteneur d'un coup (`#promiForm>*:not(…)`, `#csPhrase>*:not(…)`) ferme aussi `#csChoix` : `redteam_verbe` tombe de 6/6 à 4/6 sur « la bascule mène à un vrai bouton » (`vis:false`, mesuré, deux thèmes). **La liste des nœuds autorisés se construit PAR ÉCRAN, nœud par nœud — jamais par conteneur.** C'est ainsi que Peaufiner a donné 7 sur 9 en un lot : la liste y était bâtie élément par élément depuis le §5. Voir QUESTIONS.md · S3. |
| **On grossit un texte et l'écran se resserre partout** | **UNE COTE DÉRIVÉE N'EST PAS UN ESPACE — C'EST « HAUTEUR DU BLOC + AIR ».** Monter une taille ne déplace aucun `top` : c'est la HAUTEUR qui grandit, vers le bas, et l'air se mange en silence dans toutes les cotes calculées pour l'ancienne taille. Aucun relevé de POSITIONS ne peut le voir. Vécu : l'à-qui passé de 21 à 23 a fait tomber `à qui → titre` de **6,9 à 4,7 px sur les cinq états de fiche**, et l'état de 12,5 à 13,5 a mangé 1,1 px sous chaque fiche et chaque Nuée. **La parade : écrire la cote dans la bonne unité** — `yTitre = yQui + quiFs × 1,10 + 6,9` redonne le 30 du moodboard à 21 px et garde l'air à 23. Contrôlé par **`redteam_air.py`**, qui mesure l'ESPACE RÉEL entre deux blocs de texte (bas de A → haut de B) sur 36 écrans et refuse tout resserrement. |
| **Un écran sort vide, ou porte les blocs d'un autre** | **RIEN NE SURVIT À `closeAll` — NI CE QU'UN ÉCRAN MASQUE, NI CE QU'IL POSE, NI CE QU'IL BÂTIT.** Trois couches, et il a fallu les trois. **1 ·** un `display:none` en ligne survit à l'écran qui l'a posé → on le marque (`data-masque`) et `closeAll` le rend. **2 ·** les propriétés posées en ligne survivent aussi : le Peaufiner d'une Nuée clouait `#dpdCorps` en `display:block!important; position:absolute; z-index:30`, et le tiroir d'origine (« le potager », MEMBRES, PIÈCES) se peignait **par-dessus le titre de la fiche suivante, tiroir fermé** → `pose()` note ce qu'il écrit (`data-pose`), `closeAll` retire exactement ça. **3 ·** les nœuds bâtis survivent → un écran qui bâtit **inscrit son rangeur** dans `window._rangeurs`, que `closeAll` passe tous. Contrôlé par **`redteam_vide.py`**, qui **enchaîne** les écrans sans recharger — les autres batteries ouvrent chaque écran sur une page fraîche et ne peuvent pas le voir (mesuré : 28/61 sur la version fautive, 61/61 après). |
| **Un nœud neuf est « masqué » alors qu'il est en `display:block`** | **LE CRIBLE D'UNE AUTRE SECTION.** À l'ouverture du Peaufiner, le poster prend `s2-ouv` — le crible de la SECTION 2, écrit pour une fiche de **promesse** : il passe en `visibility:hidden` tout ce que SON inventaire ne liste pas. Les cartes d'une Nuée n'y sont pas : mesurées à `display:block` **et** invisibles, sur les quatre écrans. **Parade : ne pas toucher au crible** (il protège sa section) — **déclarer les nouveaux nœuds visibles, nommément**. Un crible se pose nœud par nœud, et se lève de même. Voir QUESTIONS.md · Q66. |
| **Une cote de fond survit au moteur qui l'a remplacée** | **UNE BANDE FIGÉE.** `.device #detailPoster.dp-nuee::before` clouait la zone haute d'une Nuée à **232,67 px**, valeur d'un lot antérieur au moteur géométrique. Invisible tant que la boîte du champ était plus haute ; **elle dépasse dès que le champ se réduit** (114 px à l'état défilé → 118 px de rectangle à bord franc sous la vague). **Parade : la faire suivre la boîte, pas la supprimer** — elle est le fond sur lequel le canevas se pose. Variable `--nuee-bande`. |
| **Un `:not(#id)` pèse l'id qu'il contient** | **`#settingsScreen > :not(#stTrameCv){width:auto!important;max-width:none!important}`** compte **DEUX ids** — celui du sélecteur et celui du `:not`. Il bat donc `#device .enh`, qui n'en a qu'un, **à `!important` égal**. Le plateau retombait en largeur automatique dans un parent `flex`, donc à la largeur de son contenu ; le titre rétrécissait pour tenir, ce qui rétrécissait encore la boîte : **342 → 242,7 → 209,4**, titre **27 → 19**, d'une passe à l'autre. **Parade : la géométrie se pose EN LIGNE avec `important`** (ce que fait déjà `.closeb`), avec des CONSTANTES du §5 — jamais une mesure, sinon la boucle revient. |
| **Un `display:contents` ne cache rien** | `#shTray`, l'ancien tiroir du partage, est en `display:contents` : **il n'existe pas pour la mise en page**, donc le masquer ne masque pas ses enfants — ils remontent dans le flux du parent. `#shNyPctRow` (« % d'harmonie ») flottait ainsi **sur le plateau du titre**, à y 58 → 87, opacité 0,34, qu'aucune règle de rangement ne pouvait atteindre. **Chercher les orphelins d'un écran refondu par leur POSITION, jamais par leur conteneur.** |
| **Un balayage de collisions annonce « 0 » sur des cadres qu'il n'a pas regardés** | **`document.elementsFromPoint` travaille en coordonnées de FENÊTRE.** Une planche fait plusieurs milliers de pixels de haut : **les cadres hors de la fenêtre rendent une liste VIDE**, donc aucun recouvrement, jamais — et l'outil sort un vert parfait. Trouvé le 3 septembre 2026 en essayant de prouver une AUTRE correction : deux textes superposés à dessein dans un cadre du bas **n'étaient pas pris**. **Tous les « 0 recouvrement » antérieurs de ce projet sont donc PARTIELS.** **Parade : on amène chaque cadre dans la fenêtre** (`scroll_into_view_if_needed`) **avant de l'interroger, cadre par cadre** ; et un point hors `[0,innerWidth]×[0,innerHeight]` se déclare **« non confirmé »**, jamais « pas de collision ». Corollaire : **une marque posée sur sa surface n'est pas un recouvrement** (une dalle peinte sur la frise, un visage dans son anneau) — on n'exempte QUE la containment géométrique, et seulement sur un canevas ou un SVG ; un texte qui **déborde** d'un canevas reste pris. Preuve : `scratchpad/preuve_collisions.py`. |
| **`getBoundingClientRect` ignore le rognage d'un ancêtre** | Un balayage de collisions comptait un recouvrement de **48 × 17** entre le mot-marque de l'aperçu de partage et le sélecteur de sujet. Il n'y en avait aucun : la zone est en `overflow:hidden`, et `elementFromPoint` au centre du mot-marque rendait `shMode`. **Un contrôle de recouvrement ou de débordement se confirme AU DOIGT** (`elementFromPoint` / `elementsFromPoint`), jamais au rectangle seul. Corollaire : le vrai défaut, lui, était ailleurs — l'aperçu était **rogné de 65 px en bas**, parce que `shareRender()` le centrait pour l'ANCIENNE zone. |
| **Un padding ne fusionne pas, une marge si** | Aux Réglages, l'écart entre le plateau et le premier bloc valait **28** : le `margin-bottom:28` de l'encart **fusionnait** avec le `margin-top:18` de `.grouplab` (marges adjacentes, le plus grand gagne). Remplacé par un `padding-top:28`, il ne fusionne plus : 28 + 18 = **46**, et le bloc tombait à 146 au lieu de 128. **Un espace repris en padding se calcule en retirant la marge du premier bloc** (ici 10 + 18). Même famille que « une cote dérivée n'est pas un espace ». |
| **Un enfant absolu d'un conteneur qui défile DÉFILE** | Trois écrans sont leur propre conteneur de défilement (`#auraScreen`, `#auraHelp`, `#plusScreen`) : leur plateau part avec le doigt, et **✕ FERMER avec lui**. `position:fixed` n'y change rien (l'ancêtre transformé devient le bloc englobant). **La parade validée est celle de l'Index :** le conteneur qui défile COMMENCE sous le plateau (`#indexList{top:212px}`) et rogne — rien ne peut monter plus haut. Sans quoi le contenu remonte **dans la bande au-dessus du plateau** (mesuré aux Réglages : « RÉCURRENCE · chaque semaine » à y 9, « ✦ Le Cercle » à y 33). |
| Idem sur un enfant **direct** de `#shareScreen` | `#shareScreen>*:not(#shareToileBg)` (≈ l.102) — même piège de spécificité. Même parade `!important`. |
| La phrase de la page + cesse d'alimenter un champ après un simple changement de **libellé** | La liaison phrase→formulaire cible ses champs par id (`#fTitle`, `#fWho`, `#csSens`) **mais aussi par le TEXTE affiché** : le mot **quand** cherche la pastille d'échéance par son libellé `+ tard` (présent dans `#dueChips` ET `#dfDueChips`, ≈ l.4938), pas par un id. Renommer le libellé casse la liaison **en silence**. Couvert par `redteam_phrase.py` (chantier 56). |

| **Une carte d'Index a la vague d'une FICHE** | `onde(base,amp)` cloue **période 1,5** (§2.1, une fiche) et **normalise par 390**, la largeur d'une fiche. Une CARTE veut **période 1, sur SA largeur** (§3.9). Appelée telle quelle sur une carte de 165, l'abscisse n'atteint que t = 0,42 : on voit deux cinquièmes de la courbe, étirés sur toute la carte — creux à x = 68 au lieu de 41, **écart médian 2,85 px**. `onde` prend deux paramètres facultatifs, `per` et `larg` ; sans eux, la fiche ne bouge pas. |
| **Une cote de fond se voit dès que la vague monte** | `--nuee-bande` est le fond DERRIÈRE le canevas d'une Nuée. Le canevas n'est opaque que **jusqu'à l'onde** : au-delà du point le plus HAUT de la vague, la bande se voit là où le corps commence. Mesuré : boîte 256, vague à 140 → **116 px de mauve à bord franc**. La borner au **minimum de l'onde**, jamais à la boîte. |
| **Un bloc posé à `left:0` dans un `.screen` sort rogné de 16 px** | **UN `.screen` NE COÏNCIDE PAS AVEC `#device`.** Mesuré le 30 août 2026 : `#studioScreen` et `#shareScreen` font **422 px** de large et commencent **16 px à gauche ET 16 px au-dessus** de l'appareil. Les cotes du document sont en écran **390 × 844** : posées à `left:0` dans un `.screen`, elles manquent 16 px à droite — le champ et la barre du Studio sortaient rognés. **Aucun relevé de positions ne peut le voir** : le dump divise par l'échelle (`dev.width/390`) et le décalage disparaît dans la division. **Parade : poser UN CADRE de 390 × 844 mesuré sur `#device`** (`dx = (device.left − screen.left) / (device.width/390)`, idem en y) et ranger tout dedans — les cotes redeviennent celles du document, sans un seul `calc()`. C'est ce que font `#stcCadre` et `#shcCadre`. ⚠ Sur `#shareScreen`, s'ajoute le piège de spécificité de la ligne suivante : `!important` obligatoire sur `position/left/top`. |
| **Une mise en page posée par un lot est défaite sans qu'on y touche** | **LE MOTEUR DE L'ÉCRAN SE REDIMENSIONNE LUI-MÊME.** `shareRender()` pose une taille en ligne sur `#shWrap` ; `buildStudio()` reconstruit `#studioBody`. Un lot qui ne repose sa mise en page **qu'aux événements du doigt** perd la main dès qu'une de ces fonctions est appelée d'ailleurs. Mesuré : après un `shareRender()` extérieur, le canevas repassait de **218 × 388 à 341 × 607** et le geste du Noyau tombait à côté — `redteam_geste` de 13/13 à 12/13, sur un contrôle (« l'aimant de la ligne du QR ») qui ne ressemble pas du tout à sa cause. **Parade : ENVELOPPER la fonction** (`var _f=window.shareRender; window.shareRender=function(){var r=_f.apply(this,arguments); requestAnimationFrame(reposer); return r;};`), jamais se contenter d'écouter. Même motif pour un libellé qu'un rotateur réécrit au hasard (`#stBuyTx`) : un `MutationObserver` **qui compare avant d'agir**. |
| **Un comparateur d'images ment sur deux points** | **1 · Il redimensionne.** `.frame` se met à l'échelle pour tenir dans la fenêtre : à un viewport de 390 × 844, `#device` sort à **363,87 px**. Capturer là et remonter à 390 met chaque glyphe entre deux pixels — aucun écran ne peut tomber à zéro. **430 × 932 donne `#device` exactement 390 × 844.** **2 · Il capture trop tôt.** Le compte de nœuds visibles se stabilise AVANT que tout soit peint : à 2 000 ms, une fiche sort sans sa dalle ni sa barre Peaufiner. Il faut un **plancher de temps** ET deux relevés identiques. **Avant d'accuser le dessin, on vérifie l'instrument.** |
| **Un `data-` posé par un peintre est lu par un autre** | `#dpTrameCv` est partagé par la fiche et la Nuée. Une base d'échelle (`data-matiere-base`) laissée par un autre peintre faisait sortir la zone de matière d'une Nuée à **59 px de haut au lieu de 194**. **Une boîte et sa base s'écrivent ensemble, d'un seul geste**, ou pas du tout. |
| **Une animation fige tout le produit, alors qu'elle ne dessine que sur un écran** | **`offsetParent` NON NUL NE VEUT PAS DIRE VISIBLE.** Un écran fermé n'est pas en `display:none` : il est **glissé hors champ** (`translateY(100%)`, opacité 0) et **garde son `offsetParent`**. Toute boucle qui filtre « les écrans visibles » sur ce critère **écrit sur tout le produit**. Vécu le 10 septembre 2026 : `frame()` (ombre de dalle, ≈ l. 8917) écrit trois variables CSS **héritées** sur les **douze** écrans `.tuto-fond`, fermés compris, à chaque image — et sa propre lecture d'`offsetParent` à l'image suivante force le recalcul de style de milliers de nœuds cachés. **27 % du fil principal**, partout dans l'app ; l'élan de l'Aura en sortait figé (images de 267 ms). **Parade : un écran est visible s'il porte `.show`** (la classe que le code pose, §8 — jamais une géométrie). **Et au profileur, le temps de mise en page est attribué à la fonction qui LIT** (`offsetParent`, `getBoundingClientRect`), pas à celle qui a sali : chercher l'écriture ailleurs. → CHANTIERS.md, chantier prioritaire. |

> ### ⚠ UN ESPACEMENT QUI REVIENT POUR LA CINQUIÈME FOIS — CE QUI DOIT L'EMPÊCHER, ET LE CONTRÔLE QUI LE PREND
> **Décision Tom, 10 septembre 2026 : « c'est la quatrième fois qu'un espacement revient, ça ne doit plus
> arriver. »** Vécu sur l'Aura portée : la planche posait les Noyaux à **454**, calcul fait pour une phrase
> d'UNE ligne (27,3 pt d'air à l'encre). Deux des cinq phrases en font **DEUX** : l'air tombait à **3,7**.
> Et les libellés des dalles touchaient le bouton (**2,7** pt) dans tous les états — la planche l'avait déjà.
> **C'est le piège « une cote dérivée n'est pas un espace » (tableau ci-dessus), en plus sournois : le
> texte n'a pas grossi, il a passé à la ligne selon SES MOTS.** Aucun relevé fait sur une seule phrase
> ne pouvait le voir.
> **Les trois règles :**
> 1. **Sous un texte qui peut passer à la ligne, aucune cote n'est figée** : elle se dérive de son BAS
>    RÉEL + l'air (`place()` de l'Aura). Et l'air vient de la planche ou du rythme déclaré de l'écran,
>    jamais de l'œil.
> 2. **Un contrôle d'air couvre CHAQUE PAIRE DE BLOCS, texte ou non** — une phrase contre une rangée de
>    disques, des libellés contre un bouton. `redteam_air.py` ne mesure que des paires de textes : il
>    ne pouvait pas le voir. **Et il se joue sur TOUS les contenus qu'un bloc peut prendre** (les cinq
>    phrases), **aux boîtes ET à l'encre sur l'image rendue** (`releve-aura.py`, famille 9).
> 3. **Si l'air rendu ne tient plus dans l'écran, l'écran DÉFILE** (sous le plateau, qui rogne) — on ne
>    reprend jamais l'air pour faire tenir.

> ### ⚠ UNE SONDE DÉFAIT EXACTEMENT CE QU'ELLE A FAIT — ET UN INSTRUMENT NOMME CE QUI RATE
> **Décision Tom, 10 septembre 2026 : « une sonde qui modifie l'app doit défaire ce qu'elle a fait, sinon
> elle contamine tout ce qui suit. »** Vécu sur la preuve des contrats de l'Aura (`preuve_contrats.py`),
> trois fois dans la même passe — pas d'une passe à l'autre (chaque passe ouvre une page neuve) :
> 1. **Défaire ≠ retirer.** La sonde qui déplaçait la légende se « défaisait » par `removeProperty('top')`.
>    Or la cote était AUSSI écrite par l'app (`place()`, en ligne, `important`) : le retrait l'effaçait, la
>    légende retombait sur l'ancienne cote figée du CSS, et l'app ne la réécrivait pas (elle compare SA clé,
>    pas le DOM). **Une sonde note la valeur d'avant — et sa priorité — et la remet.**
> 2. **Remettre ≠ rétablir.** La sonde de la phrase remettait le texte, mais la colonne ne se recalcule qu'au
>    passage suivant de `place()` (jusqu'à 30 images) : entre les deux, les contrôles suivants mesuraient une
>    colonne décalée. **Après avoir remis, on force le recalcul** (`_aura.mot(null)`).
> 3. **Poser puis mesurer en deux appels laisse passer une image** : l'app se recalcule entre les deux et
>    avale la sonde — le contrat paraît éteint. **Sonde et mesure dans la même tâche.**
> **Et un instrument qui ne garde que ce qu'il filtre est aveugle** : une passe a donné « 1 contrat à
> reprendre » sans que je puisse dire lequel — mon filtre n'imprimait que la légende et le verdict, et le
> journal complet n'était pas gardé. **Le verdict NOMME les contrats qui ratent, et chaque passe garde son
> journal entier.** C'est le piège déjà payé deux fois : un contrôle qui passe au vert sans dire ce qu'il a
> mesuré (voir « un juge qui lit la valeur qu'il vérifie », §7).

> ### ⚑ SUR UN OBJET QUI TOURNE, ON COMPARE À L'ANGLE, JAMAIS À L'INSTANT
> **Décision Tom, 10 septembre 2026 : « sur un objet qui tourne, une mesure prise au même instant ne compare
> pas le même endroit. On mesure à l'angle, jamais au temps. »** Deux images d'un objet qui tourne, prises à
> deux moments, ne montrent pas le même lieu : comparer leurs pixels compare deux endroits différents — le
> contrôle peut passer au vert sur un défaut qui demeure, ou rougir sur un état parfait. **Une comparaison de
> pixels se prend à la même VUE** : rotation figée, vue remise au même angle (`_aura.fige(true)`,
> `_aura.vue(lac, tan)`) — ce que font déjà dans `releve-aura.py` le toucher, le retour, la trace et le
> relissage. **Une mesure qui ne lit pas de pixels** (une durée, un état — l'acquis 6, le comblement, mesure la
> vie du creux) **n'a pas d'angle à caler.** Vaut pour tout ce qui bouge : l'Orbite, la Toile qui respire, un
> canevas animé. (Vérifié le 10 septembre : aucun faux vert de cette espèce n'a été trouvé dans le juge ; la
> règle est posée pour qu'il n'y en ait jamais.)

> ### ⚑ UN MOUVEMENT SE CALCULE SUR LE TEMPS RÉEL, JAMAIS SUR LE COMPTE D'IMAGES
> **Décision Tom, 10 septembre 2026, au portage de l'Orbite.** Trois défauts de la même famille,
> invisibles sur le Mac du banc — on ne les aurait trouvés que sur un téléphone lent :
>
> | Symptôme | Cause | Parade |
> |---|---|---|
> | **L'élan est perdu quand les images ralentissent** | les mouvements du doigt horodatés à leur TRAITEMENT (`performance.now()`) : livrés groupés après une image lente, ils tombent « au même instant », la vitesse sort nulle | l'heure de l'ÉVÉNEMENT (`e.timeStamp`) et chacun des événements regroupés (`e.getCoalescedEvents()`) |
> | **La rotation ralentit quand les images ralentissent** | le pas de temps borné à 50 ms par image : à 130 ms par image, la rotation tombait au tiers | le temps réel ; la borne (100 ms) ne sert qu'à ne pas sauter après une pause |
> | **Une saccade au lâcher** | un travail lourd (le cache du peintre refait) déclenché pile quand l'élan est le plus fort | différer le travail lourd à un moment calme — la caresse s'inscrit au repos (Q171) |
>
> **La règle :** une vitesse, une décroissance, une durée se calculent sur le temps écoulé — jamais sur
> « une image = 16 ms ». **Et un juge qui mesure un mouvement lit le pas de temps de LA BOUCLE**, pas
> celui de son propre échantillonneur : les deux ne tombent pas toujours dans la même image (vécu : deux
> images de 130 ms lues comme une seule de 260 — une fausse saccade). **Corollaire :** Playwright ne sait
> pas lancer — face à un fil principal occupé, ses `mouse.move` arrivent à ~130 ms les uns des autres, le
> relâcher 129 ms après le dernier : un doigt qui s'arrête. Un lancer se joue DANS la page, cadencé.

**Noms de variables à connaître :**
`NUE` (table des noms de Nuée) · `curNuee` (clé de la Nuée ouverte) ·
`promises` (tous les Promi) · `Toile.dalleTrame` · `peintMinis` ·
`_teinteDalle` · `_fichePose` · `_ficheDalle`

---

## 8 bis. LE CONTRAT VISUEL — la règle qui prime sur toutes les autres

Le design de Promi est le fruit de **plusieurs centaines d'itérations**. Chaque
taille, chaque couleur, chaque marge a été arbitrée. **Rien n'est arbitraire.**

### Ne jamais réécrire — seulement patcher

**Interdit absolu :**
- réécrire un écran « proprement »
- refactoriser le CSS ou le JS
- remplacer un composant par une version « équivalente »
- normaliser des valeurs qui paraissent incohérentes

Si une valeur paraît étrange (un `-66px`, un `1.6px`, un `.42`), **elle est
étrange pour une raison**. Ne pas l'arrondir, ne pas la « corriger ».

### Le contrôle obligatoire

Avant et après chaque lot :

```bash
python3 releve-design.py
```

Le script relève **148 propriétés sur 26 éléments dans 6 configurations** et
compare à `design-reference.json`.

```
✅  AUCUN ÉCART. Le design est intact.        → on peut livrer
❌  N ÉCARTS avec la référence                 → régression, corriger
❌  N COULEURS FAUTIVES                        → un trait neutre est apparu
```

**Un écart non demandé par le lot est une régression.** Le corriger avant de
livrer, ou expliquer précisément pourquoi il était inévitable.

Après un lot **validé par l'utilisateur** :

```bash
python3 releve-design.py --figer
```

### Ce que le script ne voit pas

Il ne vérifie ni le placement relatif, ni les superpositions, ni le rendu réel
des dalles. **Les captures avant/après restent obligatoires.**

### ⚑ CE QUE « ZÉRO ÉCART » VEUT DIRE — LA MATIÈRE EST EXCEPTÉE

> **Décision Tom, 20 août 2026. Elle fait loi et elle définit la cible de tout le
> portage.** Elle clôt Q74.

**« Zéro écart » veut dire zéro sur la GÉOMÉTRIE, les MOTS, les COULEURS et les FORMES.
La MATIÈRE est exceptée.**

**Pourquoi, et ce n'est pas une facilité.** Une Toile est **engendrée par le moteur** —
graines, poids, monde tiré au Studio — et elle respire avec `performance.now()`. La planche,
elle, l'a **tracée à la main**, cadre par cadre. Les deux **ne peuvent pas coïncider**, et
**on n'abandonne pas le moteur** (§9 : « ne jamais toucher au code de la Toile », « les
formes viennent du moteur »). Sur une fiche de Nuée, où le champ occupe les deux tiers de
l'écran, la mesure donne **87 à 100 % de pixels différents** — et aucune correction de dessin
n'y changera un point.

**Ce que ça oblige :** **un comparateur exclut la zone de matière et mesure tout le reste.**
Il ne desserre rien ailleurs — hors de cette zone, la cible reste **zéro**, pas « peu ».
`scratchpad/duo_pixel.py` porte le masque ; `redteam_formes.py` compare la courbe peinte à
la loi extraite du cadre.

**Ce que ça n'autorise PAS :**
- **masquer plus que la matière.** La zone exclue se **déclare et se mesure** — le masque est
  publié dans le relevé, en pixels, avec sa part de l'écran. Un masque qui grandit pour faire
  baisser un chiffre est une fraude.
- **excepter la matière ailleurs que dans le comparateur pixel.** Une dalle reste soumise à
  tout le reste : sa **boîte**, sa **place**, sa **couleur de champ**, son **échelle 1**, la
  règle des trois tons, le seuil 42. C'est la peinture INTÉRIEURE de la dalle qui est exceptée,
  jamais ce qui l'entoure ni ce qui la cadre.
- **s'en servir pour un écran sans dalle.** L'Index, le Fil, la page +, Peaufiner et l'instant
  gardent des zones de matière **petites** : hors d'elles, zéro.

### ⚑ LA SECONDE EXCEPTION — LE DESSIN DES GLYPHES

> **Décision Tom, 29 août 2026. Elle clôt Q80 et se lit avec celle de la matière.**

**« Zéro écart » veut dire zéro HORS MATIÈRE et HORS GLYPHE.**

**Pourquoi.** La planche est composée en **Hanken Grotesk** et **Bricolage Grotesque**
(Google Fonts, variables). L'app porte ses **six faces embarquées** — Apfel, ApfelMid,
Bricolage, Fraunces — et le **§6 les impose** : aucune graisse hors d'elles, parce qu'en
Swift une face absente ne se substitue pas, elle casse. `Hanken Grotesk` **n'est pas**
`Apfel` : c'est une autre fonte, que la planche a prise comme doublure — le document la
transcrit d'ailleurs partout en « Apfel 500 ». **Les dessins de glyphes ne peuvent donc pas
coïncider, quoi qu'on corrige.**

**Ce qui, lui, doit coïncider, et que les juges mesurent à zéro : LA BOÎTE DU TEXTE** —
sa place, sa taille, sa graisse, sa couleur, et son mot. Rien n'est desserré : c'est le
DESSIN de la lettre qui est excepté, jamais ce qui la porte ni ce qui l'entoure.

**Ce que ça oblige :** l'app déclare ses boîtes de texte (`window._zonesTexte()`) comme elle
déclare sa matière, et le comparateur rend **deux chiffres** — « écart » (hors matière) et
« hors glyphe » (hors matière ET hors boîtes de texte). Les deux masques sont **peints sur
l'image de diff** : matière en bleu sourd, texte en vert sourd. Un masque qui grandit se voit.

**Et si un écran ne peut pas atteindre zéro hors matière et hors glyphe, on le DIT, avec la
raison mesurée.** Pas de pourcentage présenté comme une livraison, pas de « classé mais pas
corrigé ».

---

## 9. Ce qu'il ne faut jamais faire

- **Toucher au code de la Toile.** Elle est validée et fragile. Aucune
  modification sans demande explicite.
- **Nettoyer le CSS.** Cinq tentatives, cinq échecs documentés. L'ordre des
  769 règles du dernier bloc est significatif ; toute suppression casse le rendu.
  Voir `ETAT-DES-LIEUX.md § dette technique`.
- **Inventer une forme, un mot, ou une phrase.** C'est la faute la plus grave.
  **Les formes viennent du moteur** (`Toile.dalleTrame`) — jamais un polygone, un
  hexagone, un glyphe reconstruit. **Les mots et les phrases viennent de l'utilisateur
  ou du moodboard** — jamais un libellé, une nature de texte (« parole », « tout le
  monde s'y engage »…) ou une tournure inventée. **Si tu ne trouves pas, tu demandes.**
- **Inventer pendant un lot de correction.** Un lot corrige ce qui est décrit,
  rien d'autre. Les éléments d'identité arrivent par moodboard.
- **Rendre visible quelque chose qui était masqué, sans chercher pourquoi il l'était.**
  **C'est la vraie leçon du portage.** Un élément masqué peut être une **décision**, pas un
  oubli — et le porter au moodboard, c'est alors ressusciter ce que le produit avait
  enterré. Vécu : le réglage **« URGENT »** était masqué par `#createSheet .f-duo
  .field:has(#urgSeg){display:none}` avec, trois lignes plus haut, le commentaire
  *« Urgent supprimé (décision : on garde Important, comme la fiche) »*. Je l'ai remonté
  dans Peaufiner en le prenant pour un oubli de portage. **Avant de démasquer un élément :
  chercher la règle qui le masque, lire le commentaire qui l'accompagne, et grepper
  `QUESTIONS.md` et `DECISIONS.md` sur son nom.** Si rien n'explique le masquage, demander.
- **Livrer sans avoir vérifié.** Si le résultat n'est pas conforme, le dire.
  Une livraison fausse coûte plus qu'un tour perdu.
- **Enchaîner plusieurs chantiers dans un lot.** Un lot = un écran = un
  avant/après.

---

## 10. Le ton des réponses

L'utilisateur travaille en français, écrit vite, avec des fautes de frappe, et
dicte parfois à la voix. Il a une tolérance faible pour les régressions et pour
les affirmations non vérifiées.

- Annoncer ce qui a été **mesuré**, avec les chiffres.
- Dire clairement ce qui n'a **pas** été fait.
- Ne jamais prétendre qu'une chose est corrigée sans l'avoir vue.
- **Une question par tour, pas plus.** Quand une règle du projet suffit à trancher,
  l'appliquer sans attendre la réponse, noter le choix dans la livraison — l'utilisateur
  corrigera s'il n'est pas d'accord. Ne poser une question que pour un vrai fork non
  couvert par une règle.
- **Le test « ÉVIDENT »** après chaque écran : quelqu'un qui ne connaît pas l'app
  comprend-il en une seconde ce qu'il doit faire ? Si non, ce n'est pas fini — même si
  c'est beau.
