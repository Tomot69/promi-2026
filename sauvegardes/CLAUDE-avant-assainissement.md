# CLAUDE.md — Promi

> Ce fichier est relu à chaque session. Il fait autorité sur tout le reste.
> Si une consigne de l'utilisateur contredit ce fichier, **demander avant d'agir**.

> ## ⚑ À CHAQUE NOUVELLE SESSION, AVANT TOUTE AUTRE CHOSE
> **Relancer le serveur et donner les trois adresses complètes, en tête du premier
> message, sans que Tom ait à le demander.**
>
> ```bash
> python3 -m http.server 8752 --bind 0.0.0.0
> ```
>
> - `http://127.0.0.1:8752/app.html`
> - `http://127.0.0.1:8752/promi-moodboard-H.html`
> - `http://127.0.0.1:8752/promi-nuee-toile.html`
> - iPhone, sur le même réseau : `http://192.168.1.133:8752/app.html` — ⚠ l'adresse du Mac CHANGE (.132 le 27 sept.,
>   .133 le 29) : la relire à chaque session avec `ipconfig getifaddr en0`
>   (Tom, 27 sept. 2026 : le serveur écoute sur `0.0.0.0` pour le téléphone ; sur le Mac, les outils gardent `127.0.0.1`.)
>
> **`127.0.0.1`, jamais `localhost`** — il bascule en https et échoue.
> **Le port est 8752** : c'est celui que tous les outils (`redteam_*.py`, `releve-*.py`,
> `scratchpad/cap_*.py`) portent en dur. Un serveur sur un autre port ne les sert pas.
> Vérifier d'abord qu'il ne tourne pas déjà : `lsof -nP -iTCP:8752 -sTCP:LISTEN`
> (attention, le processus s'appelle **`Python`** avec une majuscule — un `grep python`
> ne le voit pas, et on en relance un pour rien).

> **⚑ CE QUI EST VRAI AUJOURD'HUI : `ETAT-30-SEPTEMBRE-2026.md`.** (Assainissement, Tom, 30 sept. 2026.)
> Engendré depuis la source vivante par `etat_generer.py` — on corrige la source, jamais le document.
> **L'ordre des sources, en cas de doute :** `ETAT-30-SEPTEMBRE-2026.md` → `PROMI-TOKENS.json` (couleurs,
> polices) → `CONTRAT-MONDE.md` (un monde) → `SPEC-JUGES.md` (les règles que portent les juges) → ce fichier
> (méthode, pièges, décisions datées) → les moodboards (géométrie d'origine) → une mesure de l'app.
> **Une mesure prise sur l'app ne fait JAMAIS référence** — elle constate un état, elle ne le valide pas
> (c'est ainsi que le panneau du geste de la fiche est resté à 176 px / rayon 0 pendant que la page + était
> corrigée à 118 / 26).
> **`PROMI-SPECIFICATIONS.md`, `PARCOURS.md` et `MOODBOARD-VALEURS.md` sont des ARCHIVES** : ils décrivent
> août 2026 — géométrie et intention d'origine, jamais une couleur, une police ni un libellé à porter.
> Les moodboards (`promi-moodboard-H.html`, `MOODBOARD-parcours.html`, `promi-nuee-toile.html`) restent la
> référence de la GÉOMÉTRIE d'un écran ; leurs couleurs et leurs polices sont celles d'août.

> **⚑ DANS CE FICHIER, LES BLOCS DATÉS « ⚑ » EN TÊTE D'UNE SECTION CORRIGENT CE QUI LES SUIT.** Le socle des
> §3 à §6 a été repris le 30 sept. pour dire les valeurs d'aujourd'hui ; ce qui est resté d'avant porte
> la mention *(historique)*. Ce fichier nomme **« Nuée »** ce que l'app affiche **« Cercle »** (la clé interne
> reste `nuee`), et **« le Cercle »** (au sens de l'offre) ce qu'elle affiche **« Ma Parole ! »** (v106) :
> dans les blocs datés d'avant le 30 sept., lire « Nuée » = un Cercle, « le Cercle » = l'offre.

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
| **Cercle** | un collectif de Promi (groupe, projet) — **affiché « Cercle » depuis le 30 sept. 2026 (v106)**, anciennement « Nuée » | **masculin** : « un Cercle », « le Cercle ». Clés internes inchangées (`nuee`, `NUE`, `curNuee`) — `RENOMMAGE-LEXIQUE.md` |
| **Brouillon** | un Promi non encore planté | |
| **Fil** | le flux d'activité | |
| **Aura** | l'écran de progression et d'analyse | anciennement « Karma » |
| **Studio** | le sélecteur de monde graphique | |
| **Ma Parole !** | l'abonnement payant — **anciennement « Le Cercle »** (v106) | « Avec Ma Parole ! » · « Tu es Membre Ma Parole ! » · « Retourne ta Toile » · bouton « Bon, allez d'accord ». Espace insécable avant « ! ». Clés internes inchangées (`ouvreCercle`, `.s2-cercle`, `isPremium`) |
| **Peaufiner** | le tiroir de réglages, en bas de chaque fiche | |
| **Index** | la liste complète des Promi | |
| **Pelote** | la boule de l'Aura — le sol, les îles, la fourrure | **« sphère » et « Orbite » sont morts** |
| **Folio** | ce qu'on partage quand on partage SES DALLES — la planche des dalles, une case par Promi | « Mon Folio » au partage ; **« mes dalles » reste le nom de la Toile** |
| **planter** | créer un Promi | |
| **tenir** | honorer sa parole | |

**Termes bannis** — ne jamais les employer, même en interne :
« Belle parole » comme bouton · « En replanter un » · « Dire un mot » comme gros
bouton · « tâche » · « to-do » · « objectif » · « échéance » comme libellé de champ ·
**« valider »** · **« urgent »** · **« score »** · **« brouillon »** · **« Orbite »** · **« la sphère »** (23 sept. 2026 : la boule de l'Aura s'appelle **la Pelote** ; « Orbite » est un nom fossile du système planétaire abandonné, retiré des écrans, du code et des documents).
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
mauve      #291547   une Nuée
terracotta #DD4D23   à tenir
menthe     #2BE88C   tenu
```

> **⚑ 22 SEPTEMBRE 2026 — UN ANNEAU NE PORTE QUE TROIS ARCS.**
> (Décision Tom. *« Un anneau ne peut avoir que trois arcs : à tenir, en cours, tenu. S'il y en a
> davantage, le système est cassé. »*)
>
> **D'OÙ VENAIENT LES SEGMENTS EN TROP, MESURÉ** (`scratchpad/anneaux.py`) : le lot de la
> réciprocité (Q215, 14 sept.) peignait **deux moitiés** — à gauche ce que tu tiens, à droite ce
> qu'on te tient — soit 3 états × 2 moitiés = **jusqu'à six arcs**. Relevé : « toi » 6, Marion 5,
> Rachel 4. **Et pour Adrien et Nico, seule la moitié DROITE existait** : leur anneau ne montrait
> que ce qu'ON te tient, présenté comme si c'était ta parole. C'est là qu'était la logique cassée.
>
> **L'ANNEAU PORTE MAINTENANT LES TROIS ÉTATS DE CE QUI SE PROMET ENTRE VOUS, DANS LES DEUX SENS,
> UNE FOIS.** On concatène les LISTES avant d'en faire des parts : la pondération se fait par le
> **nombre de paroles**, jamais à parts égales entre les deux directions. La réciprocité garde sa
> rangée « Ce qu'on t'a tenu ».
>
> ⚠ **ET LE VOILE D'OPACITÉ QUITTE LES ARCS.** Le `opacity:.5` du gratuit portait sur la moitié
> droite : c'est LUI qui délavait les trois couleurs d'état sur la capture. Les couleurs rendues
> sont désormais **exactement** `#DD4D23` · `#291547` · `#00341A`, et leurs claires en sombre.
>
> **⚑ L'AMANDE `#8FE08F` NE PEINT QUE L'ANIMATION DE CÉLÉBRATION.** *« Quand une parole est tenue,
> une seconde dalle apparaît sous la première, de la même forme, en vert amande. Elle se décale,
> puis disparaît. L'amande ne peint jamais un état, ni un arc, ni un texte, ni une valeur claire. »*
> Balayé sur 8 écrans × 2 thèmes (`scratchpad/amande.py`) : **0 surface en amande hors animation**.
> Les deux dernières étaient le verbe de la phrase (repli, passé à la nature) et l'icône « Les
> Noyaux » de l'aide, qui dépeint des arcs et porte donc les valeurs d'état.
>
> **⚑ LE SOL DE LA SPHÈRE GARDE LA COULEUR DE LA PALETTE, PAS SEULEMENT SA TEINTE.** Il prenait
> bien le ton dominant — mais les deux transformations de Q210 écrasaient sa chroma :
> ```
> le ton dominant        C* 41,6
> × SOL_CLAIR 0,38       C* 18,8
> + 39 % vers le crème   C*  6,4     ← la teinte survit, la COULEUR non
> ```
> On garde la CLARTÉ (c'est elle qui rend les îles lisibles) et **on RESSATURE à 0,72 × la chroma
> du ton dominant** — exactement ce que fait déjà la rampe de velours. ⚠ **Et la ressaturation va
> dans `solEffectif`, pas dans `fondSphere`** : c'est LE POIL qui fait la couleur de la sphère, pas
> la peau ; posée sur la peau seule, elle ne bougeait rien sur une palette peu chromatique.

> **⚑ 21 SEPTEMBRE 2026 (soir) — LE PAYSAGE D'UNE FICHE, ET LES ÉTATS QUI BASCULENT.**
> (Moodboard des correspondances **v8** + décisions Tom. **Corrige les deux blocs qui suivent.**)
>
> **1 · L'AMANDE N'EST PAS LA VALEUR CLAIRE DE « TENU ».** *« Ma consigne était fausse. Elle sert
> uniquement à l'animation de célébration : une seconde forme de la dalle apparaît sous la
> première, se décale, puis disparaît — en vert amande. Rien d'autre. »*
> Le « tenu » a donc **sa** claire, comme l'« en cours » : **`#33BA6C`**, obtenue par le MÊME
> transport que le couple validé (`#291547` → `#A77CF7` : ΔL +49, ΔC +34, teinte gardée) — et,
> comme lui, **à ΔE 60 de son plein**. ΔE aux trois natures : **102 · 92 · 90**.
>
> **2 · LES ÉTATS BASCULENT AVEC CE QUI EST PEINT SOUS EUX.**
> ```
> à tenir    #DD4D23  partout — il se lit des deux côtés (Δlum 65 / 65)
> en cours   #291547 sur fond clair   ·  #A77CF7 sur fond sombre
> tenu       #00341A sur fond clair   ·  #33BA6C sur fond sombre
> ```
> La colonne de l'Aura (légende, arcs des Noyaux) est posée **sur la page** : elle bascule.
> L'anneau du **+** de l'accueil est posé **sur la barre sombre**, dans les deux thèmes : il
> garde les claires. C'est la même règle, appliquée à deux fonds différents.
> ⚠ **Et un état qui bascule se REPEINT quand le thème change** : `eta()` est lue à la
> construction. Sans repeinture, un changement de thème laisse les valeurs de l'ancien mode.
>
> **3 · LE PAYSAGE D'UNE FICHE TENUE (v8).** L'ocre est abandonné, le brun `#6B4630` aussi.
> ```
> terre    #2B1020   prune sombre — le SOL d'une fiche, dans les deux thèmes
> crête    #0B4A2A   la ligne d'horizon, posée sur la terre  (ΔE 51,3 · Δlum 35,4)
> anneau   #00341A   5 px, CERNÉ D'UN FILET CRÈME #F7F0DE de 1,4 px
> ```
> **Le filet n'est pas un ornement, il est la condition de lisibilité** : le vert profond n'est
> qu'à **ΔE 44,6 · Δlum 16,2** de la terre ; le filet crème est à **Δlum 217,3**.
> Sur la terre (L* 8,9) le texte passe **crème** (15,42 : 1) et les marques d'état prennent le
> **clair de « tenu »** `#33BA6C` (Δlum 128,8).

> **⚑ 21 SEPTEMBRE 2026 — LE JAUNE SORT, ET LE CLAIR D'« EN COURS » EST UN VIOLET.**
> (Décision Tom : *« Le jaune sort. C'était ma consigne, elle était mauvaise. #FFD447 a été retiré
> en v6, il ne doit revenir nulle part. »* **Corrige le bloc du 20 septembre qui suit.**)
>
> ```
> en cours          #291547   le champ plein — inchangé
> en cours, clair   #A77CF7   le violet que le jeu PORTAIT DÉJÀ : --c-mauve63
> ```
> **Rien de neuf n'entre dans la palette** : `--c-mauve63` y était. Mesuré : **ΔE 30 du lilas
> Nuée, 41 du bleu Promi, 58 du rose Chiche**, Δlum 113 au pire fond sombre.
>
> **⚠ ET LA RÈGLE QUE J'AVAIS ÉCRITE ÉTAIT FAUSSE.** « Le clair d'un état est la valeur qu'il
> remplace » marchait pour l'amande, par coïncidence ; elle ramenait ici une couleur **retirée**.
> **La règle juste : le clair d'un état est de LA FAMILLE de son état, et il s'écarte des trois
> natures d'au moins ΔE 25.**
>
> **⚠ ET LA DIRECTION BLEU-VIOLET EST FERMÉE, C'EST MESURÉ.** Entre le bleu Promi (h 277) et le
> lilas (h 308) il n'y a que **31°** : dans le registre du produit (L* 70-84, C* 45-62) l'écart au
> lilas n'y dépasse **jamais 24**. Le seul bleu-violet qui passe ΔE 25 tombe à **ΔE 3 à 11 du
> périwinkle #8FA0FF** — la valeur que la v6 avait retirée. Une teinte décalée vers le rouge-violet
> passe, mais à ΔE 25 du lilas **on est déjà dans le magenta** ; garder la teinte et descendre en
> clarté donne le même écart **en restant un violet**. C'est ce qui a été retenu.
>
> **⚑ LES AVATARS DES NOYAUX PIOCHENT DANS L'IDENTITÉ SEULE.** `_BPAL` = les quatre tons de la
> palette d'identité, et rien d'autre : **un visage ne porte jamais un état.**
>
> **⚑ ET TON VISAGE NE CHANGE PLUS À CHAQUE OUVERTURE.** `USER.seed` était `(Math.random()*1e9)|0`,
> jamais sauvegardé — exactement le défaut de `cc()` corrigé le 13 septembre sur les dalles. Même
> parade, même ordre : **la graine sauvegardée d'abord ; sinon dérivée d'une clé stable (le nom),
> jamais d'un id ni d'une horloge ; et on l'enregistre.** (`_grainePropre`, `promi_graine`.)
> ⚠ **Et c'est une DÉCLARATION de fonction, pas une affectation** : `USER` est construit 960 lignes
> plus haut dans le même bloc — seule une déclaration est hissée.
>
> **⚑ LE SOL DE LA SPHÈRE SE DÉCALE JUSQU'À SE DÉTACHER DE LA PAGE.** *« Si le sol ne se détache
> pas assez de la page, il se décale jusqu'à passer le seuil. »* Seuil : **42**, celui du §3 — déjà
> le plancher du contour dans le juge de l'Aura. **Le décalage garde la teinte** (on mélange vers le
> blanc ou vers le noir, jamais vers une autre couleur) et **s'éloigne du côté où l'on est déjà**.
> ⚠ **On vise 44, pas 42, et la marge est MESURÉE** : le garde-fou agit sur la COULEUR, ce qu'on
> voit est le RENDU, que la fourrure assombrit — il en coûte jusqu'à 0,7. Balayé sur les 21 palettes
> × 2 thèmes : **0 sous le seuil sur 42 mesures**, la plus faible Taciturne sombre à **43,0** (elle
> était à **10,4** sans garde-fou). Sonde : `scratchpad/balaye20.py`.

> **⚑ 20 SEPTEMBRE 2026 — LE MOODBOARD DES CORRESPONDANCES v7 FAIT FOI.**
> (Décision Tom, sur la planche v7 + son message. **Il remplace le bloc du 17 septembre qui suit, gardé pour l'histoire.**)
>
> **1 · L'ENCRE DU MODE CLAIR EST ARRÊTÉE À `#201908`, ET LE PRINCIPE D'ÉCHANGE DE LA v4 EST
> ABANDONNÉ** — *« un fond et une encre n'ont pas les mêmes contraintes »*. Le fond du mode
> sombre descend donc à **`#100D0B`** (« café noir subtil ») ; l'encre du clair ne bouge plus.
> Contraste mesuré : **15,34 : 1** sur la crème, exactement le 15,3 annoncé.
>
> **2 · LES TROIS BRUNS S'ÉTAGENT** — et la marche du bas a été creusée à la demande de Tom :
> ```
> encre du clair   #201908   L*  9,2    le texte du mode clair
> brun encre       #43291C   L* 19,5    trait et texte sur champ lilas  (était #3A241A, L* 16,7)
> brun surface     #6B4630   L* 33,4    corps d'une fiche tenue
> ```
> Marches : **10,3** puis **13,9** de L* (avec `#3A241A` la première ne valait que 7,5).
> Le **violet quitte le rôle d'encre** (le brun encre le prend, 6,62 : 1 sur le lilas) et le
> **vert quitte le rôle de surface** (le brun surface le prend — c'est la surface qui manquait
> au §3, Q217 : *« déclarée, pas encore employée »*). Sur le brun surface, crème Δlum **163,9**,
> amande **124,7**, encre 51,0 seulement : **l'encre s'inverse**, le corps d'une fiche tenue
> porte du crème et ses marques d'état l'amande, **dans les deux thèmes** (une surface
> d'exception ne bascule pas).
>
> **3 · « EN COURS » ET « TENU » DEVIENNENT SOMBRES, ET CHACUN GAGNE SA VALEUR CLAIRE.**
> ```
> en cours    #291547   (violet Promi, retenu)     ·  son clair : #FFD447
> tenu        #00341A   (vert profond)             ·  son clair : #8FE08F  (l'amande)
> à tenir     #DD4D23   inchangé — il lit dans les deux modes
> ```
> **Pourquoi il faut les deux :** le trait borne le CHAMP et le CORPS. Sur `#100D0B`, `#291547`
> et `#00341A` donnent **Δlum 15 et 26** — la moitié basse du trait s'éteint. L'amande le
> faisait déjà pour le tenu ; **il manquait l'équivalent pour l'en cours.**
> **Ce clair n'est pas inventé : c'est, dans les deux cas, LA VALEUR QUE L'ÉTAT REMPLACE.**
> L'amande `#8FE08F` était le « tenu » du 17 septembre ; le jaune `#FFD447` était l'« en cours ».
> Mesuré sur `#100D0B` : jaune **Δlum 197,5 · ΔE 108,5** · amande **187,4 · 94,1**. Et aucune
> collision : le jaune est à ΔE 109 du lilas, 114 du bleu, 80 du rose.
> ⚠ **Un transport fidèle du violet vers le clair était impossible** : `#291547` et le lilas
> Nuée `#C9A8F5` ont **exactement la même teinte** (309,4° contre 308,3°) — le transport donnait
> `#B9B0FF`, à **ΔE 8** du lilas, c'est-à-dire la Nuée.
>
> **4 · OÙ ÇA VIT DANS LE CODE.** Les deux clairs passent par les bascules `-txt` qui existaient
> déjà : `:root` = sombre (l'amande, le jaune), `.light` = clair (`#00341A`, `#291547`). Une
> règle qui peint un **aplat** prend la valeur fixe ; une règle qui peint une **marque d'état**
> prend le `-txt`. ⚠ **Et une marque suit CE QUI EST PEINT SOUS ELLE, pas le thème** : les
> pastilles de légende de l'Aura sont posées sur un plateau `#201908` **dans les deux modes** —
> elles gardent l'amande et le jaune en clair aussi.
>
> **5 · LA PALETTE PAR DÉFAUT EST LA PALETTE D'IDENTITÉ** — « Signal », vingt-et-unième et
> première du rail : bleu `#82AEF8` · rose `#FFB8D2` · lilas `#C9A8F5` · **crème dalle
> `#EFE3C7`** en quatrième (*« c'est une surface, pas un état, aucune règle ne s'y oppose »*).
> Primesautier reste dans les vingt. `_BPAL`, qui teinte les avatars des Noyaux, perd ses deux
> reliquats `#B586F6` et `#8CBCFD` et prend les quatre tons d'identité.

> **⚑ 17 SEPTEMBRE 2026 — LA PALETTE CHANGE DE VALEURS, ET LA NUÉE CHANGE DE RÔLE.**
> (Décision Tom, sur sa **planche des correspondances** et le **PDF des vingt palettes du Studio** —
> les deux font foi et remplacent les valeurs ci-dessous.) **Le bloc du 16 septembre qui suit reste
> pour l'histoire ; c'est celui-ci qui vaut.**
>
> ```
> LES NATURES — le champ dit la nature
>   bleu Promi      #3A54FF → #82AEF8
>   rose Chiche     #FA2258 → #FFB8D2
>   lilas Nuée      #D0B0FF → #C9A8F5     ⚑ C'EST LE CHAMP D'UNE NUÉE (voir ci-dessous)
> LES ÉTATS — la ligne dit l'état
>   à tenir         #DD4D23              (inchangé depuis le 16 sept.)
>   en cours        #8FA0FF → #FFD447     le périwinkle passe au JAUNE
>   tenu            #2BE88C → #8FE08F
> FONDS, ENCRE, SURFACES
>   fond clair      #F7F0DE              (inchangé)
>   fond sombre     #201908              (inchangé) — et c'est l'encre du mode clair
>   violet Nuée     #291547              ⚑ TRAIT ET TEXTE SUR CHAMP LILAS (voir ci-dessous)
>   encre profonde  #120E05              le FOND D'ÉCRAN sombre — distinct du fond du mode
>   vert profond    #06231A → #00341A     corps d'une fiche tenue, surface d'exception
>   orange d'origine          → #F07A2E   accent secondaire, célébration
>   crème panneau   #F3E7D1 · crème bordure #E4D7BB · crème dalle #EFE3C7
>   gris texte sombre #A2947C · gris chaud clair #6E6350 · lavande pâle #E6D8FA
> ```
>
> **⚑ LA NUÉE : LE LILAS EST LE CHAMP, LE VIOLET EST CE QU'ON POSE DESSUS.** (Tom, 17 sept. 2026 :
> *« Les trois natures sont des pastels : la Nuée ne peut pas être la seule avec un champ sombre.
> Et le violet garde son rôle — il est au lilas ce que l'encre est au bleu et au rose. »*)
> **C'est un échange de RÔLE, pas une valeur qui bouge.** Ce document écrivait l'inverse — « mauve
> #291547 une Nuée », et la table des corps de fiche donnait la bande d'une Nuée en violet.
> **Lire désormais : bande et champ d'une Nuée = lilas `#C9A8F5` ; trait et texte posés dessus =
> violet `#291547`.** Le corps clair (`#F3E9FE`) et le corps sombre (`#1B1426`) ne bougent pas.
> ⚠ **La barre Peaufiner d'une Nuée n'est PAS posée sur son champ** : elle prend le corps mauve
> `#291547` (chantier G), dans les deux thèmes — son texte y reste crème (Δlum 79,7 ; le violet y
> donnerait 0). Mesuré, pas supposé.
>
> **⚑ LE TEXTE POSÉ SUR UN CHAMP PASSE À L'ENCRE `#201908`.** (Tom, 17 sept. 2026.) Les champs sont
> devenus pastels : le crème y tombe à **Δlum 12,9** sur le Chiche et **24,2** sur le Promi, là où le
> §3 exige 42. Avec l'encre : **72,8** et **61,6**. Ça vise le mot-marque, le ✕ FERMER, la barre
> Peaufiner, **tout ce qui se pose sur un champ**. Contrôlé par `scratchpad/sonde_champ.py`, qui ne
> devine aucun sélecteur : il remonte au premier fond opaque depuis chaque texte.
> ⚠ **Le revers n'est PAS réglé :** le texte écrit **en couleur de nature sur le corps crème** tombe
> lui aussi sous 42 (31 textes mesurés, mode clair seulement) — QUESTIONS · **Q221**.
>
> **⚑ LES VINGT PALETTES DU STUDIO REMPLACENT LES DIX.** Quinze claires, cinq sombres, l'ordre
> C1 ≈ 34 % → C2 ≈ 28 % → C3 ≈ 23 % → C4 ≈ 15 %. Primesautier · Candide · Gouailleur · Alangui ·
> Irascible · Hurluberlu · Béat · Minaudier · Chafouin · Frivole · Cajoleur · Allègre · Lunatique ·
> Flegmatique · Narquois · Fielleux · Sibyllin · Vénéneux · Atrabilaire · Taciturne.
> **⚑ 23 SEPT. 2026 — TROIS DE PLUS, ET LA GRILLE SE FERME** (Tom : *« il reste la place pour trois
> palettes »*) : **Truculent** `#FF3E00 #00E5FF #5600D6 #F6FF00` · **Pétulant** `#FF8A00 #6800E0
> #00C85A #FFAAC8` · **Fantasque** `#00FF8C #E60073 #0040FF #FFF7DE` — pop, fluo, posées avec les
> claires (avant Fielleux). 24 pastilles = **quatre rangées de six**. Mesurées comme les autres
> (ΔE 2000) : écart interne **48,3 · 38,0 · 28,5** (le jeu : 13,0 à 37,8) ; distance à la plus
> proche **17,1 · 17,8 · 16,6** (le jeu : 9,2 à 20,7, médiane 16,9) ; entre elles **20,5 à 23,5**.
> Garde-fou du sol repassé : **0 sous 42 sur 48 mesures**. Q278. Leur nom paraît
> sous la rangée, en Gilbert 12 px capitales (vingt noms sous des orbes de 40 px ne tiendraient qu'en
> 9 px — sous le plancher du §6). Défaut : **Primesautier**, à la place de « Signal ».
>
> **⚑ ET CE QU'AUCUNE PASSE HEXADÉCIMALE NE VOIT : LES TABLEAUX DE TRIPLETS.** 47 tableaux `[r,g,b]`
> en JavaScript — `NAT` (la Pelote), `SPECTRE`, `GPIX·GBRA·GLI·GMOS·GENC·GLIGHT` (les
> rampes de fond de la Toile), `SIG`, `ETATS`, `KC`, les grappes. Ils portaient encore l'ancienne
> identité **un mois après sa bascule** : c'est ce qu'on voyait « sur la sphère et sur les dalles ».
> **Une bascule de palette se termine par un audit qui cherche chaque ancienne valeur en hexadécimal,
> EN TRIPLET et en `rgb()`** — sans quoi la conversion est fausse et paraît juste.

> **⚑ LA PALETTE A CHANGÉ DE VALEURS LE 16 SEPTEMBRE 2026 — AUCUNE SYMBOLIQUE N'A BOUGÉ.**
> (Décision Tom, avec sa planche des deux modes.) *« Chaque couleur garde son rôle, seule sa
> valeur bouge. »* Cinq mouvements, et deux entrantes :
>
> ```
> l'orange      #F07A2E → #DD4D23   même fonction d'accent, pastilles et états.
>                                   ⚠ À ÉVITER POUR DU TEXTE (mesuré : Δlum 42 sur la crème,
>                                   43 sur le brun — il est AU seuil, jamais au-dessus).
> le clair      #F4EEE1 → #F7F0DE   le FOND du mode clair
> le mauve      #8A5CF0 → #291547   symbolique inchangée (mais il est devenu SOMBRE, L* 12)
> le brun       (entrant) #201908   le fond du mode SOMBRE — c'est l'encre du mode clair :
>                                   les deux modes s'échangent, rien d'autre ne bouge
> le vert       (entrant) #00341A   surface d'exception — DÉCLARÉE, pas encore employée
>                                   (aucune surface ne lui a été donnée : QUESTIONS · Q217)
> ```
>
> **Les dérivés suivent leur ancre**, transportés en CIELAB : la teinte suit en plein, la
> clarté et la chroma à proportion de la proximité (sans ce poids, le corps sombre « à tenir »
> #2E1C13 tombait à L* 1 — noir). **Trois valeurs sont des ajustements EXPLICITES, pas des
> transports**, parce que le fond sombre est devenu brun et le mauve très sombre :
> `#2E1C13 → #401E17` (corps sombre « à tenir », ΔE au fond 15,1 → 16,6) ·
> `#2A1912 → #3A1B15` (gardé de côté, 13,3 → 14,7) ·
> `#271B45 → #1B1426` (corps sombre d'une carte de Nuée : il tombait à **ΔE 6,2 de son propre
> champ** — descendre en clarté ne suffit pas à teinte égale, il faut SOURDIR ; on prend donc
> le corps sombre de Nuée que ce document donne déjà).
>
> **⚠ DEUX RÔLES SOUS UNE MÊME VALEUR — #12142A.** Le fichier l'employait pour « le CORPS DU
> THÈME — #F4EEE1 en clair, #12142A en sombre » (plateaux, recherche, tri, Langue,
> Confidentialité, Cercle, partage) **et** pour le corps de fiche d'un Promi. Le premier est un
> FOND : il est passé au brun. Le second est une NATURE : il n'a pas bougé. **On sépare au
> sélecteur, jamais à la valeur.**
>
> **⚠ CE QUE LA NOUVELLE VALEUR A CASSÉ, ET QUI EST OUVERT.** La ligne « à tenir » posée sur un
> champ PLEIN de nature tombe sous le seuil du §3 : **Δ14 sur le champ Promi** (elle était à
> Δ51), **Δ21 sur le champ Chiche** (elle était à 58). Mesuré sur la fiche, la carte d'Index, le
> bandeau du Fil et l'instant, dans les deux thèmes — `redteam_tonsurton` le prend 8 fois.
> **Ce n'est ni un bug de juge ni une erreur de bascule : c'est la valeur décidée qui rencontre
> la règle des 42.** En ΔE l'orange reste franc sur le bleu (140) ; c'est la LUMINANCE qui
> manque. Rien n'a été touché : QUESTIONS · **Q216**.

### ⚑ 23 SEPTEMBRE 2026 (v34) — TOUT SUIT LE STUDIO, SAUF L'AURA. (Décision Tom — elle RENVERSE le « figé à la création » ci-dessous.)
> *« Tout suit le Studio — le Fil, l'Index, la Toile, la Toile du Cercle, les fiches, la page +, Partager. Ils prennent le monde
> et la palette sélectionnés. Seule exception : l'Aura. La Pelote et la liste sous « Ce que tu as tenu » gardent le monde et la
> couleur de plantation. »* Dans le moteur, le monde de plantation n'est plus le défaut de `dalleTrame` : il se DEMANDE
> (4ᵉ argument explicite, ou `opts.plantation`) — seule l'Aura le fait. La palette qui décide d'Ingénu est celle du Studio
> (`_ingenuRampe(id, haut, plantation)`). Juges réécrits au niveau de la décision : `redteam_decoupe` famille H,
> `redteam_dalle_figee` D (originaux `sauvegardes/*-avant-v34.py`). Les ÉTATS, eux, ne suivent toujours rien.

### ⚑ 27 SEPTEMBRE 2026 (v61) — UN MOUVEMENT DE MONDE SUIT L'HORLOGE. EXCEPTION : HOULE.
> (Décision Tom.) *« Ce n'est pas un changement de rythme : à 60 images par seconde, rien ne bouge. C'est ce qui garantit que
> la durée validée tient sur un iPhone lent. »* Tesselle, Braille, Buvard, Éclisse, Taille-douce rejoignent Pochade et Touffe :
> leur ressort est calculé sur le temps (`1 − 0,83^dt`, `1 − 0,78^dt` = 0,17 et 0,22 à 16,67 ms). Les mondes neufs (Madrure,
> Halin, Esquille, Ritournelle, Bobinette) intègrent le temps VRAI en sous-pas de 1/60 s (ils plafonnaient à 50 ms et
> comptaient toute image de plus de 100 ms pour 1/60 s). Un redémarrage de la boucle fait toujours UN pas (`frame._redem`).
> **⚑ EXCEPTION ÉCRITE — HOULE (`sillons`) RESTE PAR IMAGE** : elle tourne à ~30 i/s sur la page validée ; à l'horloge elle
> deviendrait plus rapide que ce que Tom a validé. Elle s'étire sous charge, par décision. `redteam_rythme` le vérifie.
> **Ce qui a bougé à 60 i/s, et seulement ça : Halin, −105 ms à l'arrivée, −147 au départ** — ses propres accrocs (images de
> 100 ms et plus) lui faisaient perdre du temps en v60. Tous les autres : identiques (A/B, pages fraîches, vrai GPU).
> ⚠ **Madrure a deux chemins** : le GPU (Chrome, iPhone) et un SECOURS processeur (construction par tranches) quand WebGL refuse
> (`failIfMajorPerformanceCaveat`) — c'est ce que tous les bancs mesuraient jusqu'ici. **Un banc Chromium se lance avec le vrai
> GPU** (`--use-angle=metal --enable-gpu --ignore-gpu-blocklist`) ; WebKit l'a déjà.

### ⚑ 30 SEPTEMBRE 2026 (v102) — L'AGRANDISSEMENT DES TEXTES (v96) : PERTES D'AIR ASSUMÉES, AVEC LEURS VALEURS.
> (Décision Tom : *« On accepte la perte d'air. Ne fais pas défiler la page +, et n'agrandis aucun bloc à hauteur fixe. Ces écrans ont été
> composés pour tenir en un écran, et quelques pixels valent mieux qu'un défilement sur l'écran où l'on plante. »*) Mesuré à l'ENCRE
> contre la référence d'avant v96 (`sauvegardes/air-encre-avant-v96.json`) ; ces écarts sont VOULUS — ne pas les « corriger » :
> ```
> rail du pinceau (règle du mi-chemin)   page + : consigne → rail −8,5 · rail → barre −10,5
>                                        page + d'une Nuée : phrase → rail −10 · rail → barre −13   (vu à l'œil : lisible, rien ne se touche)
>                                        gardé de côté : mot → rail −6 · rail → « garder » −7 · rail → barre −8 · « garder » → barre −4
> cartes de l'Index et du Fil            sur-titre → titre, titre → état : −3 à −4 (un titre passé à deux lignes : « faire les crêpes »)
> cartes du Peaufiner d'une Nuée         libellé → aide −2,7 · aide → note −3,2 · note → libellé suivant −4
> tête du Peaufiner                      titre → « LE TRAIT » −3 · « ✕ FERMER » → valeur −2
> Réglages                               une rangée → la suivante −2 à −3,5 · « ✦ Le Cercle » → « Le Studio » −3
> Partager                               « Ma Toile · Story » → « Inviter » −3,5
> plateaux                               « ✕ FERMER » → tri (Index, Fil) −1,5
> ```
> **Décisions, pas des dérives** : le titre du Fil (−3,6, recentrage v97), l'aide de l'Aura (−4,1) et la page + d'un Chiche / d'une Nuée
> (−3) — même recentrage des titres ; les valeurs des Réglages (−1,5, v98). **Rendu, lui** (v101–v102) : colonnes des fiches, de
> l'instant et de la Nuée, cartes du fil d'une Nuée, consigne et phrase de la page +.

### ⚑ 30 SEPTEMBRE 2026 (v104) — LES MURS DU CERCLE : UN FLOU, PAS D'EXPLICATION, UNE PHRASE QUI MONTE.
> **⚑ v105 (Tom, le même jour) — LA PHRASE EST REPRISE :** plus de plateau (*« pas dans la DA, ça fait bon marché »*) ; elle s'affiche **au
> centre du mur touché, sur le flou, seule** — pas d'encart, pas de bandeau, pas de fond, pas de cadre ; **en gros** (34 px, réduite jusqu'à
> tenir en **trois lignes** et dans la hauteur visible du mur), **encre `#201908` sur clair, crème `#F7F0DE` sur sombre**, une seule taille ;
> elle reste **le temps d'être lue** (1,4 s + 60 ms par caractère, entre 3 et 5,5 s) puis s'efface ; la toute première fois l'offre s'ouvre
> à la fin de cette lecture. Le flou : **4,8 px partout** (Aura, aide, Réglages, les trois Peaufiner) — *« on ne donne pas ce qu'on vend »* ;
> **le Studio garde le sien** (*« on doit voir le monde pour avoir envie de l'acheter »*). La porte des Réglages s'appelle **« Ma Parole ! »**.
> **« Arranger la Toile » est SUPPRIMÉ** (v105, Tom : *« on n'en veut pas »*) — la pastille, l'icône, la fonction, la feuille ; le moteur
> de la Toile est rendu à l'identique.
> (Décision Tom.) *« Les encarts qui disent LE CERCLE disparaissent. Un réglage verrouillé est simplement flouté, sans explication. Quand
> on touche un mur, une phrase monte du bas et reste. Ensuite, toucher n'importe où ouvre la page de l'offre. Sauf la toute première
> fois : la page s'ouvre automatiquement. »* Et : *« deux fois plus flou — on veut plutôt illisible »* → **un seul flou pour tous les
> murs du gratuit : 4,8 px**, **SAUF LE STUDIO, qu'on ne touche pas** (ses flous et son « Adopte ce design — 1 € » restent).
> Les 21 phrases (lot-V104-MURS, `window._murPhrases`) s'enchaînent dans l'ordre sur un compteur **GLOBAL** (`promi_murs`, toutes zones,
> par personne), puis au hasard sans répéter la précédente ; remise à zéro après 14 jours sans mur (Q352, à valider). **« Ma Parole ! »**
> est le nom neuf de l'offre — **seules ces phrases l'emploient** (renommage complet : un lot à venir) ; il y porte l'orange d'accent
> secondaire, le reste de la phrase la couleur d'accent. La porte des Réglages (« ✦ Le Cercle ») n'est pas un mur : elle reste.

### ⚑ 29 SEPTEMBRE 2026 (v98) — UNE TOILE TIENT UN NOMBRE ILLIMITÉ DE PAROLES, ANCIENS MONDES COMPRIS. (Décision Tom.)
> *« Une parole qui n'apparaît pas est inacceptable — la décision v35 valait pour l'aspect, pas pour perdre des paroles. »* Les huit anciens
> gardent leur semis constant TANT QU'IL Y A UNE CELLULE VIDE ; plein, `sync` ajoute une cellule (`_celluleEnPlus`). Leur aspect ne change
> qu'au-delà (~50 paroles). **Les titres sur la Toile s'effacent quand la dalle n'a pas 48 px à l'écran** — on zoome pour lire (Tom : « illisibles
> à 200-500, c'est normal ; vérifie qu'ils disparaissent proprement »). Banc : `scratchpad/infini.py`, `ligne500.py` (WebKit).

### ⚑ 23 SEPTEMBRE 2026 (v35) — INCOHÉRENCE ASSUMÉE : LE SEMIS QUI GRANDIT NE VAUT QUE POUR LES QUATRE MONDES NEUFS.
> (Décision Tom, qui **corrige** le bloc v34 ci-dessous : « c'était une exception pour les quatre neufs seulement ».)
> **Pochade, Tesselle, Touffe, Braille, Buvard, Houle, Taille-douce, Éclisse** gardent le semis CONSTANT d'origine
> (≈ 68 cellules, les promesses colorent des cellules du semis, le recul cadre les colorées) et leur aspect d'origine.
> **Esquille, Bobinette, Ritournelle, Madrure** ont une Toile faite de ses seules promesses.
> **La raison** : les huit anciens ont été dessinés, réglés et validés sur le semis constant (leurs taches, fleurs et
> éclats se règlent sur l'écart entre graines — à 6 promesses la Touffe faisait des fleurs énormes) ; les quatre neufs ont
> été conçus pour une Toile qui grandit (PDF « la toile grandit »).
> **Ce que ça coûte, et il faut le savoir :** changer de FAMILLE au Studio ressème la Toile (`setTheme` → `sync`) ; une
> dalle peinte dans un monde de l'autre famille (l'Aura, qui garde le monde de plantation) est calculée sur le semis EN
> PLACE, pas sur celui de sa famille ; la rampe des îles de la Pelote dépend du semis en place (0,85 / 1,4).
> Où ça vit : `_NEUFS`, `_semisNeuf()`, `_semisDe`, `Toile.semisNeuf()`.

### ⚑ 23 SEPTEMBRE 2026 (v34) — LE SEMIS GRANDIT AVEC LES PROMESSES. (Décision Tom.)
> *« Une Toile à six promesses a six cellules, pas quarante dont trente-quatre seraient vides. »* Mesuré avant : **68 graines
> à 6, 20 et 40 promesses** — un semis fixe dont les cellules se coloraient, cadré par le recul. Désormais la Toile est faite
> de ses promesses et de ses Nuées (`sync`, `addPromi`, `_auVide` : une graine neuve au plus grand vide, tirée de
> `Toile.cle()`), vue entière. **Seule la Toile SANS promesse garde le semis de graines du §10.6.** Conséquences : la matière
> d'un monde ne peut plus se régler sur l'écart entre graines (`env.uMat`, unité fixe — CONTRAT-MONDE §15.6) ; presque toutes
> les cellules touchent le bord, leur dalle s'arrête au bord de la Toile. `Toile.graines()` rend le compte.

### ⚑ LA FRONTIÈRE STUDIO / ÉTAT — ce qui suit la palette, et ce qui ne la suit jamais

> **Décision Tom, 20 septembre 2026.** *« La sphère rejoint ce qui suit la palette du Studio,
> avec les dalles de la Toile et la Toile de l'écran du Cercle. Son sol prend la palette. Mais
> les dalles gardent leur monde et leur couleur de plantation […]. Une dalle est figée à sa
> création, partout où elle paraît. Et la légende, les arcs des Noyaux et les traits d'état ne
> suivent jamais le Studio. Ce sont des états : le vert n'est « tenu » que parce qu'il est
> toujours vert. »*

**Trois familles, et elles ne se mélangent pas :**

```
SUIT LE STUDIO — ce sont des SURFACES
   la Toile · la Toile de l'écran du Cercle · LE SOL DE LA SPHÈRE (le ton dominant, C1)

FIGÉ À LA CRÉATION — une dalle porte SON monde et SA couleur, partout où elle paraît
   les dalles de la Toile · les ÎLES de la sphère · les dalles de « Ce que tu as tenu »
   (et celles de l'Index, du Fil, des fiches : c'est déjà la règle du §4)

NE SUIT JAMAIS RIEN — ce sont des ÉTATS, et un état qui change cesse d'être un signal
   la légende de l'Aura · les arcs des Noyaux · les traits et les libellés d'état
```

**Comment on le VÉRIFIE, et c'est une mesure, pas une lecture :** on rend l'écran sous deux
palettes très éloignées et **on regarde ce qui bouge**. Ce qui doit suivre bouge, le reste est
identique au pixel. Relevé le 20 septembre, Signal contre Irascible contre Allègre :
le sol bouge de **ΔE 42 et 33** ; les pastilles, les arcs et les empreintes des dalles rendent
**une seule valeur distincte sur trois palettes**. Sonde : `scratchpad/frontiere.py`.

**⚠ CE QUE LA DÉCISION COÛTE, ET IL FAUT LE SAVOIR AVANT DE TOUCHER AU SOL.** L'écart boule ↔
page n'est plus une constante : il devient une **conséquence de la palette**. Balayé sur huit
palettes (`scratchpad/balaye_sol.py`), en mode sombre il va de **10,4** (Taciturne) à **156,2**
(Primesautier) — sous les deux palettes les plus sombres, **la boule se fond dans la page**.
La calibration de Q210 (`SOL_CLAIR` 0,38, `SOL_CREME` 0,39, plancher des îles ΔE 15) avait été
mesurée sur le bleu de la nature : elle ne garantit plus rien sur les vingt autres palettes.

> **⚑ 23 SEPTEMBRE 2026 — SUR UN FOND SOMBRE, LE TENU EST L'AMANDE.** (Décision Tom, elle
> **corrige** les blocs du 22 septembre.) *« Les textes en vert sombre sur les Promi et Chiches
> tenus ne se lisent pas sur le pourpre du fond. Tout ce qui est en vert sombre sur pourpre, tu
> le mets dans le vert amande — mode clair comme sombre, puisque le fond pourpre ne change pas. »*
> Mesuré : `#00341A` sur la terre `#2B1020` → **Δlum 11,3** ; l'amande `#8FE08F` → **190,6**.
> **Ce n'est pas « l'amande revient partout »** — c'est la doctrine du §3 appliquée : une marque
> suit **ce qui est peint SOUS elle**. Sur un fond clair, le tenu reste `#00341A`.
> **Et « TENUE » se marque en amande** — *« ce vert amande est beau et rare, donc célèbre »*.
> ⚠ **« Un peu gras » ne peut pas être une graisse** : Gilbert n'en a qu'une (§6). On appuie par
> la chasse et la taille, jamais par un `font-weight` qui ne peindrait rien.
>
> **⚑ 21 SEPTEMBRE 2026 (v18, Tom) — LE FILET NE SUIT QUE LE BORD EXTÉRIEUR DE CHAQUE SEGMENT, ET S'INTERROMPT DANS
> LES ÉCARTS. 1 px.** Jamais le bord intérieur, jamais les bouts, jamais un cercle continu — partout où un disque paraît,
> l'anneau du + compris (segments nets, plus de fondu). Les paragraphes qui suivent décrivent l'état d'avant. QUESTIONS · Q298.
> **Et la mention TENU est en amande** (« TENUE », « TENU À DEUX · 3 AOÛT ») : c'est l'autre usage de l'amande, avec la célébration.
>
> **⚑ ET UN FILET CRÈME CERNE CE QUI EST SOMBRE SUR DU SOMBRE.** Un filet de **1,4 px `#F7F0DE`**
> cerne **tout anneau posé sur un fond sombre** (la terre d'une fiche dans les deux thèmes, le brun
> du mode sombre dans l'Aura) **et court sous le trait d'une parole tenue**, à la jonction de la
> crête `#0B4A2A` et de la terre — mesuré Δlum **15,7**, sous le seuil du §3.
> **⚑ 23 SEPTEMBRE 2026, CINQUIÈME ÉCRITURE — LE FILET SE COLLE AU BORD DE L'ANNEAU, PAS À CELUI
> DE SA BOÎTE.** (Tom : *« il y a un écart — sur le Noyau autour du + de l'accueil, et partout
> ailleurs. Il cerne le bord, sans jeu. »*) **Deux fois la même faute : une cote calculée sur une
> géométrie qui n'est pas celle de l'objet.** ① l'`outline-offset:3px` du **+** avait été pris sur
> `.dhero::before{inset:-3px}`, la règle GÉNÉRALE — mais sur l'accueil `#device .acc-barre
> #createBtn::before{inset:0!important}` gagne : offset **0**. ② `drawKRing` posait le sien à `W/2`,
> le bord du CANEVAS ; avec les constantes globales l'anneau s'arrête à **0,4069·W** — mesuré sur un
> Noyau de 104 : **8,2 px de jeu**, ramenés à **0,5**. Le filet suit désormais le bord PEINT
> (`_krDehors`), borné au canevas.
> ⚠ **Et la passe `_filetsDisques` était un SECOND PROPRIÉTAIRE** (§7) : elle repassait au bord du
> canevas après le peintre. Elle lit maintenant la cote que le peintre **déclare** (`data-filet`).
> **Les Noyaux SVG (`.au-nb`) ne bougent pas** : leur filet est à `D/2 − 0,7`, l'arc finit à `D/2`
> — jeu **−1,4**, il occupe les 1,4 derniers pixels de l'anneau. Zéro jeu, et il reste DANS la
> boîte, seule écriture qui survive à `.au-nx`. Sonde : `scratchpad/s26/disques.py`.
>
> > ⚠ **Le filet d'un anneau vit sur le NŒUD, jamais dans le canevas** : peint dans le canevas il se
> fait recouvrir par la passe suivante, et il ne peut pas dépendre d'une CLASSE (`drawKRing` est
> appelé 8 à 12 fois par ouverture, les premiers appels précèdent la pose de la classe). Le bord
> extérieur d'un anneau EST le bord de sa boîte : un `box-shadow` le cerne au pixel.

### Les couleurs d'état (fond)

```
#2BE88C   menthe       tenue
#DD4D23   orange       à tenir
#FA2258   framboise    Chiche
#E4CEFD   lilas        Nuée (clair)
#291547   mauve        Nuée (soutenu)
#3A54FF   bleu         création, Promi
neutre    periwinkle   en cours
#F7F0DE   crème        surface claire  ·  le FOND du mode clair
#201908   brun         surface sombre  ·  le FOND du mode sombre, et l'encre du clair
#00341A   vert         surface d'exception (déclarée, pas encore employée — Q217)
```

> **⚑ TOUT PASSE PAR LE JEU — `PROMI-TOKENS.json`.** (Tom, 16 septembre 2026 : *« Centralise
> tout : un jeu de couleurs nommées avec variantes claire et sombre, et une extension de styles
> pour qu'aucune vue n'appelle une police ou un hexadécimal en dur. C'est ce qui servira au
> portage Swift. »*) **Trois fichiers, et ils se régénèrent, ils ne s'écrivent pas :**
>
> ```
> PROMI-TOKENS.json      la source unique — 28 rôles, 7 niveaux de texte, 234 couleurs fixes
> app.html · lot-TOKENS-css   le bloc que l'app lit — mêmes valeurs, engendré depuis le JSON
> Promi+Design.swift     l'extension de styles du portage — engendrée depuis le même JSON
> ```
>
> **DEUX NIVEAUX DE VARIABLES, ET L'ORDRE COMPTE :**
> `--c-*` la palette **FIXE**, une valeur par couleur : **c'est ce que les règles emploient**.
> `--p-*` les **RÔLES**, qui basculent avec le mode : c'est ce que le portage Swift emploie.
> **Une règle ne doit JAMAIS employer un rôle à la place d'une valeur fixe** : le produit peint
> souvent la crème en mode sombre et l'encre en mode clair (`.acc-plat` en donne l'exemple), et
> un rôle les inverserait — en silence, sur des dizaines d'écrans.
>
> Contrôlé par **`redteam_tokens.py`** (19 contrôles, sans navigateur) : les valeurs décidées
> sont écrites EN DUR dans le juge, les deux modes s'échangent vraiment, **aucune couleur en dur
> dans un `<style>`** (0 sur 3 292), aucune police appelée en dur, et le JSON, le bloc CSS et
> l'extension Swift disent la même chose.

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

### ⚑ UN TRAIT SUR UN APLAT COLORÉ SE JUGE EN ΔE, PAS EN LUMINANCE — Q216, tranché

> **Décision Tom, 18 septembre 2026 :** *« Juge en ΔE, pas en Δlum, comme le §7 le fait déjà pour
> la Pelote. Sur un aplat coloré, c'est l'écart de couleur qui compte. »*

**Le seuil de 42 en LUMINANCE garde son objet — du TEXTE sur un fond.** Il ne vaut plus pour une
LIGNE posée sur un aplat de couleur : là, le plancher est **ΔE 15** (celui de la Pelote, §7).

**Pourquoi, et c'est mesuré, pas supposé.** Depuis que les champs sont pastels, **aucune ligne d'état
n'atteint 42 en luminance sur aucun champ** — et elles se voient toutes :

```
                    Δlum      ΔE                          Δlum      ΔE
  à tenir / Promi   18,0    107,8      à tenir / Chiche   29,2     67,5
  tenu    / Promi   11,7     87,2      tenu    / Chiche    0,5     78,3
  en cours/ Promi   15,7    114,0      à tenir / Nuée     21,5     93,4
```

**Le cas qui tranche, relevé sur l'image rendue** (`redteam_tonsurton`, les deux thèmes) : le trait
menthe `#8FE08F` d'une parole tenue sur le champ rose `#FFB8D2` d'un Chiche — **Δlum 0, ΔE 78,3**.
Même clarté exacte, teintes opposées. On le voit sans effort sur toute capture de l'Index ; un seuil
de luminance seul l'aurait déclaré ton sur ton.
**La luminance n'est pas abandonnée : elle est REPORTÉE à côté**, parce qu'elle attrape autre chose —
un trait juste en teinte mais noyé en clarté. Elle ne fait plus échouer seule.

### Les traits

Ils prennent la teinte de la dalle **décalée de 150° en teinte**, saturation
remontée à 55 % minimum. Cela garde la famille chromatique du monde choisi tout
en évitant le ton sur ton.

> **⚠ Point ouvert** — l'utilisateur juge ce décalage parfois hors palette.
> Une décision est attendue : soit conserver le décalage, soit piocher une
> couleur réelle de la palette du monde actif. **Ne pas trancher seul.**

### ⚑ §2.1 bis CORRIGÉ — SUR UN CHAMP PASTEL, LA TEINTE QUI SE LIT EST SOMBRE

> **Décision Tom, 18 septembre 2026 :** *« Les teintes claires du §2.1 bis sont mortes — Δlum 1,6 sur
> le Promi, 5,0 sur le Chiche. Ce sont des compagnons dessinés pour des champs saturés qui n'existent
> plus. Recalcule-les sur les champs pastel. »*

**La règle ne bouge pas : le trait posé sur un champ plein porte une TEINTE DE SA NATURE, jamais la
couleur pleine du champ. Ce qui change, c'est le sens de l'écart.** Sur un champ saturé, la teinte
qui se lisait était plus CLAIRE ; sur un champ pastel, elle est plus SOMBRE.

```
            champ       avant  →  après       Δlum            ΔE
  Promi     #82AEF8   #C4A2F5  →  #022140    1,6 → 58,3    24,2 → 61,2
  Chiche    #FFB8D2   #F5AC9E  →  #3D0F23    5,0 → 69,6    21,8 → 69,8
  Nuée      #C9A8F5   #C9A8F5  →  #291547      0 → 61,8       0 → 62,3
```

**LA NUÉE MONTRAIT DÉJÀ LA RÉPONSE** — sa « teinte claire » était le VIOLET, un ton sombre. Et sa
valeur déclarée était `#C9A8F5`, **c'est-à-dire le champ lui-même** : le trait d'une Nuée avait
exactement la couleur du fond qu'il traverse.

⚠ **DEUX RÔLES VIVAIENT SOUS UN SEUL NOM.** `NATCLAIR` servait **le trait** (les deux thèmes) **et**
les libellés posés sur le corps SOMBRE. Le second a toujours besoin d'une teinte claire ; le premier,
de l'inverse. **On sépare au NOM, jamais à la valeur** — `NATTRAIT` est né, `NATCLAIR` garde les
libellés. C'est le même piège que `#12142A` au §3 et que les deux propriétaires du §7.

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
> **Câblé depuis le 13 septembre** : les peintres de l'Index, du Fil, de la Pelote et de l'écran qui vend passent le
> monde de plantation en 4ᵉ argument (voir le paragraphe suivant).
>
> **⚑ ET SA COULEUR AUSSI — posé le 13 septembre 2026 (feu vert Tom, Q213, pour cette raison seule).**
> La couleur d'une dalle était **tirée au hasard à chaque chargement** (`cc()`, `Math.random`) : une dalle
> n'avait aucune identité stable. Un Promi porte maintenant `dalle = {ci, lit}` — l'emplacement dans la palette et
> la nuance —, figé par `_dalleFigee(vivant)` au moment où `Toile.addPromi` le relie (la couleur que la Toile
> vient de tirer, loin de ses voisines). Un Promi sans `dalle` (jeu de démonstration, sauvegarde ancienne) la
> reçoit de **son titre et sa personne** (`_dalleDeCle`) — **jamais de l'id**, qui change d'un chargement à
> l'autre sur le jeu (chantier 71). `tones()` la respecte à chaque passe. **Les peintres des cartes (Index, Fil)
> reçoivent le monde de plantation** en 4ᵉ argument. Contrôlé par `redteam_dalle_figee.py`.
> **Une Nuée a SA dalle** (Tom, 13 sept. 2026) : `Toile.sync()` plante une dalle par Nuée nommée (`kind:'nuee'`), sa couleur est
> figée par Nuée (`NUEDALLE[clé]`, tirée de son nom), et le code du Cercle y passe — jamais sur ses Promi. Avant, `sync` l'effaçait à
> chaque plantation : une Nuée de neuf paroles était invisible sur la Toile. Contrôlé par `redteam_nuee_dalle.py`.
>
> **⚠ Ce que ce paragraphe disait avant, et qui était vrai jusqu'au 4 septembre :**
> On a longtemps cru l'inverse. **C'est faux :** un Promi ne porte **aucun champ de monde**
> (`Object.keys(p)` n'en a pas), et `theme`, `palKey`, `hueShift` sont **trois variables de
> module, globales**. La même dalle repeinte dans trois mondes donne trois remplissages
> différents — 4289 · 3963 · 1912 sur la dalle 125, boîte et tons compris
> (`scratchpad/monde_fige.py`). **Changer de monde au Studio repeint TOUTE la Toile, les
> anciennes dalles comprises.**
> *(Décision prise depuis : le monde est figé le 4 septembre, la couleur le 13 — paragraphes ci-dessus.)*

> **⚑ 21 SEPTEMBRE 2026 — L'EXCEPTION INGÉNU : DANS LA PALETTE PAR DÉFAUT, LA COULEUR D'UNE DALLE DIT SA NATURE.**
> (Décision Tom.) La palette par défaut s'appelle **Ingénu** (ex-« Avenant », ex-« Signal » ; clé `signal`) et garde ses
> quatre tons : bleu `#82AEF8` · rose `#FFB8D2` · lilas `#C9A8F5` · crème dalle `#EFE3C7`. **Sous Ingénu seulement,
> un Promi est bleu, un Chiche rose, une Nuée lilas, et le crème dalle peint les cellules neutres** (les cellules
> colorées qui ne portent aucune parole). *« La couleur ne ment plus, elle dit la vérité. »*
> **C'est une exception au « la dalle porte le monde, l'accent porte la nature » — elle ne vaut QUE pour Ingénu.**
> Sous toute autre palette, la dalle garde sa couleur figée (`p.dalle.ci`), qui n'est pas effacée : elle revient telle
> quelle dès qu'on quitte Ingénu. Où ça vit : `cOf()` (la seule décision de teinte du moteur) lit `s.nat`, posé par
> `_dalleFigee`. **Les douze autres palettes qui portent une couleur signal restent telles quelles** : choisir une
> palette est un geste délibéré. QUESTIONS · Q292, Q297.

1. **Toujours la vraie dalle du moteur**, rendue par `Toile.dalleTrame(canvas, id, 1)`.
   Jamais un polygone, jamais un hexagone, jamais une photo, jamais une approximation.
   La bande de Nuée n'y échappe pas : ce sont de vraies dalles, seulement **teintées**
   mauve (la teinte porte l'identité, pas une forme inventée).
2. **⚑ v29 (Tom, 23 sept. 2026) — UNE DALLE SE REND À SA TAILLE FINALE ET SE POSE 1:1.** Jamais rendue
   à la taille de la Toile puis agrandie, réduite, rognée, relue en pixels ; jamais une photo ; jamais un
   morceau de Toile. On passe par **`window._poseDalle(g, id, x, y, w, h, o)`** (ou `_rendDalle` + `_poseUn`) :
   le moteur rend la dalle au `k` de la boîte, et depuis v29 **`k` agrandit aussi les pas de trame
   (`UK`)** — la même dalle à 40 px et à 200 px est la même image. Ce que les appelants retouchaient
   (Q30, Q297, chantier 59) est peint PAR LE MOTEUR (`opts.rampe`, `opts.decale`) ; ce qu'ils relisaient,
   le moteur le DÉCLARE (`cv.__dalleInfo`). Contrôlé à chaque lot qui touche une dalle par
   **`redteam_decoupe.py`**. Le contrat d'un monde : **`CONTRAT-MONDE.md`**.
   *(Avant v29 : « l'échelle est toujours 1 » — les valeurs ≥ 6 cassaient les mondes à trame, dont les pas
   étaient en pixels. C'est `UK` qui a levé la contrainte.)*
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

> **⚑ UN JOUR D'ANNEAU SE DONNE EN PIXELS D'ARC, JAMAIS EN POURCENTAGE DU TOUR.**
> (Tom, 23 septembre 2026 : *« les espaces entre les segments sont inégaux et irréguliers —
> uniformisé partout, net, espace logique parfait entre tous, sans fioriture »*.)
> **Le jour vaut 3 px d'arc, et il se convertit par anneau** (`3/r` en radians). Donné en ANGLE,
> le même écart sort inégal d'un disque à l'autre : 0,8 % du tour faisait **1,00 px** sur « Toi »
> (Ø 78) et **0,76** sur une personne (Ø 58).
> **n arcs, n jours identiques, le jour centré sur midi** — pas d'ouverture supplémentaire en
> haut, pas de fondu entre deux segments (l'anneau d'une fiche en avait un de 3 % du tour : deux
> grammaires pour un même objet, c'est la fioriture qu'on refuse).
> ⚠ **Et un seul état ne peut pas faire 360° PILE** : un arc SVG dont le départ et l'arrivée sont
> le MÊME point **ne dessine rien**. On laisse un dixième de degré, sinon un Noyau qui n'a qu'un
> état sort SANS ANNEAU.
>
> **⚑ LA PILULE CÈDE À 94,5 DE HAUT — rayon 30 au-delà.** (Tom, 11 septembre 2026, QUESTIONS · Q203.)
> *« La loi du §2 tient là où elle a du sens, et cède seulement là où elle produit un défaut. »* Au-delà d'une certaine
> hauteur, rayon = hauteur ÷ 2 **mange le texte** : la courbe vient serrer le début de la première et de la dernière ligne
> (NOTE de 118 en pilule : encre à 6,3 du contour ; à 163 la courbe coupe la ligne). **Le seuil est MESURÉ, pas un nombre
> de lignes** : 94,5 est la hauteur où la pilule la plus serrée à deux rangées passe sous l'air d'un champ ouvert au rayon
> 30 (C = 15,19, mesuré sur l'encre). **Donc : h ≤ 94,5 → rayon h ÷ 2 ; h > 94,5 → rayon 30** — c'est le « grand panneau »
> du tableau ci-dessus, qui était déjà la règle. Un seul propriétaire dans l'app : `rayon()` (`lot-CERCLE-MUR`,
> `window._seuilPilule`) ; les juges portent 94,5 EN DUR (§7).

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
Gilbert Bold          sous-titres, libellés, navigation — EN CAPITALES        700
Atkinson Hyperlegible tout le texte                                    400 · 500 · 700
Fraunces              titres et signature « Promi »                           600
```

> **⚑ 18 SEPTEMBRE 2026 — LES TITRES SONT LA POLICE PromiLate** (`Polices Promi/PromiLate-Regular.otf`,
> jeton `--f-marque`, `lot-TITRES-POLICE`). Elle remplace les huit dessins ci-dessous (Q234). 27 px (cap 18,9),
> 29 sur la page + ; une seule graisse, `font-synthesis:none`. Aussi les phrases d'action DU TRAIT, et rien d'autre.
> Le bloc suivant reste pour l'histoire.
>
> **⚑ 17 SEPTEMBRE 2026 — LES TITRES NE SONT PLUS UNE POLICE : CE SONT HUIT DESSINS.**
> (Décision Tom, assumée : *« huit dessins, pas une police. Si un écran change de nom un jour, il
> faudra un nouveau dessin — c'est le prix, et il est acceptable. »*) Faute de fichier de fonte,
> les titres sont **vectorisés depuis la planche du lexique** (`~/Downloads/promi-lexique.png`) :
> **Promi · Le studio · L'aura · Fil · Index · Partager · Toile · Noyau**.
>
> **UN SEUL `<path>` PAR MOT, `fill:currentColor`, AUCUN BITMAP.** Le dessin suit donc toutes les
> règles de couleur déjà posées, sans en ajouter une. **Seule exception : « Promi » a DEUX chemins**
> — le mot, et son **« i »**, qui garde sa couleur d'accent. Le « i » est reconnu **à sa place**
> (tout contour dont le bord gauche passe 0,82 × la largeur), jamais à un indice.
>
> **DEUX CHOSES À NE JAMAIS REPERDRE, si on refait la vectorisation :**
> · **on suréchantillonne le NIVEAU DE GRIS avant de seuiller.** L'anticrénelage de la source porte
>   l'information sous-pixel ; le jeter d'abord donne un escalier. C'est ce qui fait tenir une source
>   de 760 px à **0,34 px d'écart moyen au bord, à 2×** — sous le pixel.
> · **le marching squares doit être ORIENTÉ** (l'encre toujours à gauche du sens de marche), sinon le
>   chaînage rend des fragments : **50 contours pour « Promi » au lieu de 8**.
> Outil : `scratchpad/vecto_lexique.py`. Planche : `planche-lexique.html`.
>
> **LE DESSIN SE MET À L'ÉCHELLE SUR LA HAUTEUR DE CAPITALE, et cette cote est DÉCLARÉE** (§8 : une
> cote se calcule, elle ne se mesure jamais). Relevé police chargée : Gilbert 27 → **18,9** ·
> Fraunces 27 → 18,9 · Fraunces 29 → **20,3**. Au premier jet je lisais `fontSize` au moment de
> poser : le mot-marque de l'accueil sortait à **28 px au lieu de 119**.
> ⚠ **Et la cote se pose EN LIGNE avec `important`** : les plateaux portent des règles d'icône
> (`.acc-plat svg{width:22px}`) qui écrasent l'attribut `width` d'un SVG.
> ⚠ **On MASQUE le texte d'origine, on ne le supprime jamais** : `.ti-x` porte le dernier caractère
> et il CLIGNOTE sur « Réglages ». Rien ne se perd (§5).
>
> **SIX TITRES SUR HUIT SONT POSÉS** (`lot-TITRES-DESSINS`) : le mot-marque de l'accueil et celui de
> la page +, l'Index, le Fil, Partager, Le studio, L'aura. **« Toile » et « Noyau » n'ont aucun titre
> d'écran à eux aujourd'hui** — ils n'existent que dans « Arranger la Toile », « Ma Toile » et les
> libellés de l'Aura. Leurs dessins sont prêts et attendent une place. **Les titres restants (Nuée,
> Réglages, La langue, La confidentialité) gardent Gilbert** : la planche ne les porte pas, et le §9
> interdit d'inventer une forme.
>
> **⚑ LES DEUX POLICES ONT CHANGÉ LE 16 SEPTEMBRE 2026** (Tom, avec sa planche du lexique).
> **Gilbert Bold** — *Type With Pride*, Ogilvy & Mather — porte les **sous-titres, les libellés
> et la navigation, en capitales**. **CC BY-SA 4.0 : le crédit est OBLIGATOIRE dans l'écran
> « à propos », et les glyphes ne peuvent pas être modifiés.** **Atkinson Hyperlegible Next** —
> Braille Institute of America, SIL OFL 1.1, libre — porte **tout le texte**. **Les titres
> gardent Fraunces** : elle sera remplacée plus tard.
>
> **LES SEPT NIVEAUX** (ils vivent dans `PROMI-TOKENS.json`, et nulle part ailleurs) :
> ```
> titre        Fraunces 600   36 px
> sous-titre   Gilbert  700   22 px   CAPITALES
> texte        Atkinson 400   16 px
> accentué     Atkinson 700   16 px
> petit texte  Atkinson 400   14 px
> métadonnée   Atkinson 400   13 px   opacité .65
> libellé      Gilbert  700   15 px   CAPITALES
> ```
>
> **MESURÉ AVANT DE BASCULER, parce que Tom l'a demandé :**
> · **la barre du bas, cinq entrées à 12 px en capitales.** Gilbert est plus ÉTROIT que ce qui
>   était là : STUDIO **40,50** px contre 45,83 · AURA 29,83 contre 33,45 · INDEX 34,31 contre
>   37,17 · FIL 18,47 contre 17,94. L'air entre STUDIO et AURA **monte de 14,36 à 18,84 px**.
>   Ce n'était donc pas serré — ça respire mieux qu'avant.
> · **le plancher de 12 px tient.** À **13 px**, la hauteur d'x RENDUE d'Atkinson est de **7 px**
>   — exactement celle d'Apfel et d'ApfelMid. À 12 px, 6 px de part et d'autre. La métadonnée
>   réelle « tenu · il y a 2 jours · Quentin » passe de 163,39 à **167,97 px** (+2,8 %).
>   Rien ne perd en hauteur d'œil ; **le §6 n'a pas à bouger**.
>
> **⚠ LES MÉTRIQUES DES FACES NEUVES SONT CALÉES SUR CELLES QU'ELLES REMPLACENT.** Sans cela le
> changement de police déplace les cotes : la boîte de Gilbert fait 1,250 em là où Bricolage
> fait 1,188 — **9 paires de textes resserrées de 1 à 2 px**, mesurées par `redteam_air`, dont
> la phrase d'un gardé de côté. `ascent-override` / `descent-override` / `line-gap-override`
> dans le `@font-face` les font coïncider **à toutes les tailles employées** (relevé de 11,5 à
> 29 px : zéro écart). **Aucun glyphe n'est touché** — la licence de Gilbert l'interdit ; ce
> sont des métriques de mise en page, pas des dessins.
>
> **⚠ ET LA GRAISSE NE CHANGE PAS NON PLUS.** L'ancienne table écrasait Apfel 500·600·700·800
> sur ApfelMid 500, faute de plus gras dans la famille. Atkinson EMBARQUE un 700 : rendue telle
> quelle, la table aurait mis en gras tout ce qui demandait 700 dans la feuille (mesuré : le
> libellé du geste et les pastilles, 500 → 700). **Atkinson 500 reçoit donc tout ce que
> ApfelMid 500 recevait** ; la face 700 ne sert qu'au niveau « accentué », demandé nommément.
> **Seule exception, et elle est inévitable : Gilbert n'a qu'une graisse.** Ce qui était
> Bricolage 600 passe en Gilbert 700 — le contrat visuel le voit, c'est attendu.
>
> **⚑ 22 SEPTEMBRE 2026 — IL N'Y A PLUS QUE TROIS POLICES : Gilbert, Atkinson, PromiLate.**
> (Décision Tom. *« En Swift elles n'existeront pas : autant le voir maintenant que pendant le
> portage. »*) **Fraunces, Bricolage Grotesque et Apfel Grotezk sont RETIRÉES** — six faces,
> **161,9 Ko**, et leurs crédits avec elles. Les piles sont `PromiLate,Gilbert,system-ui`,
> `Gilbert,system-ui`, `Atkinson,system-ui`.
>
> **⚠ ET LA NOTE QUI ÉTAIT ICI ÉTAIT FAUSSE.** Elle disait que Bricolage et Apfel restaient pour
> `✕`, `✦`, `→`, `←` et `●`. **Mesuré** (CDP `CSS.getPlatformFontsForNode`, qui rend les polices
> de plateforme et le NOMBRE de glyphes peints, 11 écrans × 2 thèmes) :
> ```
> ✕ ✦ ●   viennent DÉJÀ du système (Zapf Dingbats, 40 glyphes) — jamais de Bricolage ni d'Apfel
> ‹ ›     Bricolage en peignait 60 : le Studio et les rangées des Réglages
> →       Apfel en peignait 6 : « CHOISIR → » de la page +
> ```
> Ces trois caractères tombent maintenant sur la police du système, **comme ✕ ✦ ● le faisaient
> déjà**. Relevé après le retrait : la HAUTEUR du glyphe ne bouge que de **+9 %** (elle passe de
> 82-84 % à 89-92 % de la hauteur de capitale du texte voisin) ; c'est la CHASSE qui s'élargit —
> `→` +51 %, `‹ ›` +81 à +84 % —, et la seule boîte qui grandit est « CHOISIR → », de **124,1 à
> 129,6** px à x 42. Rien à reprendre : les chevrons étaient sous-dimensionnés, ils se lisent
> mieux. Sondes : `scratchpad/polices_rendues.py`, `scratchpad/chevrons.py`.
>
> **⚠ LA PREMIÈRE FAMILLE DÉCIDE — une liste d'égalités en rate toujours une.** Une police
> s'appelle de dix façons : `Bricolage,system-ui,sans-serif`, `'Bricolage',-apple-system,…`,
> `'Bricolage Grotesque',Bricolage,…`, `'Fraunces',Bricolage,serif`, l'attribut SVG
> `font-family="…"`, le raccourci `font:700 13px/1 Bricolage,…`, la clé d'objet JS
> `{'font-family':'…'}`, et `g.font` sur un canevas. **Au premier essai, 217 appels avaient
> survécu** — les avatars d'une Nuée, tout l'onboarding, le grand chiffre de l'Aura. On lit donc
> la PREMIÈRE famille de la liste, jamais la liste entière. ⚠ **Et un `@font-face` n'est pas une
> vue** : y poser `font-family:var(--f-titre)` DÉTRUIT la face (une custom property n'y est pas
> valide) — les six faces d'origine ont disparu en silence au premier passage, Fraunces tombant
> sur Georgia.

**Tailles minimales :** rien en dessous de 12 px. Aucune opacité sous 72 % sur du
texte lisible.

> **⚠ AUCUNE GRAISSE HORS DES FACES EMBARQUÉES.** (Lot du 19 août 2026.)
> En navigateur, une graisse absente se substitue **en silence** — la plus proche, ou une
> oblique synthétique. **En Swift, elle casse.** Le prototype étant la spécification du
> portage, tout couple demandé doit exister en `@font-face`.
> **Cinq faces depuis le 22 septembre 2026, et cinq seulement :**
>
> ```
> Gilbert 700                                      sous-titres, libellés, navigation
> Atkinson 400 · Atkinson 500 · Atkinson 700       tout le texte
> PromiLate 400                                    titres d'écran, mot-marque, phrases du trait
> ```
>
> **LA TABLE DE REPORT :** `gilbert` toute graisse → **Gilbert 700** (il n'en a qu'une) ·
> `atkinson` italique → **Atkinson 400** (aucune italique embarquée), ≥ 450 → **Atkinson 500**,
> sinon **400** · `fraunces` et `promilate` → **PromiLate 400**. Les familles retirées n'ont plus
> de report : elles ne sont plus demandées nulle part (`redteam_polices` : 0 couple absent).
>
> **⚠ ET IL A FALLU CORRIGER `lot-POLICES` LUI-MÊME.** Il retirait son propre style en ligne
> avant de relire la cascade — mais `pose()`, sur le Peaufiner d'une Nuée, écrit sur LES MÊMES
> propriétés. Tant que la feuille demandait « Bricolage 600 », la face existait et le lot ne
> touchait à rien ; avec « Gilbert 600 », qui n'existe pas, il reportait, posait, puis
> **détruisait l'inline de `pose()` au passage suivant** — 22 éléments retombaient sur la police
> héritée (`.np-bas` rendu en Atkinson 14, boîte 18, au lieu de Gilbert 14, boîte 17 : trois
> paires de textes resserrées). **C'est le piège « deux propriétaires pour une même propriété »
> du §7, et la parade est celle de la sonde : on note la valeur d'avant — et sa priorité — avant
> d'écrire, et on la remet avant de relire** (`data-pol-av`).
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
python3 redteam_gens.py       # 38 — le choix des personnes, AU DOIGT (ajout · croix · « + ajouter » · au-dessus de Peaufiner)
python3 redteam_tuiles.py     # 64 — l'écran des choix de la page +, AU DOIGT : la tuile touchée ouvre SA nature
python3 redteam_dalle_figee.py # 4 — une dalle garde sa couleur et son monde (par titre, jamais par id)
python3 redteam_reperage.py   # 16 — Promi · Chiche · Nuée lisibles sur chaque carte et ligne ; Nuée = petite Toile
python3 redteam_nuee_entree.py # 24 — « Planter dans la Nuée », dernière ligne du fil, au doigt ; la règle du trait tient
python3 redteam_accueil.py    # 22 — l'accueil B : plateau, barre 5 entrées, le + sur place, portes cachées fermées, dalles atteignables
python3 redteam_zoom.py       # 16 — le dézoom tient, planter ne reprend pas la vue, recadrer (rond et double toucher)
python3 redteam_cercle_couleur.py # 34 — LA COULEUR, 5e réglage du Cercle : bloc 384/encart 147, ton de palette et code libre jusqu'à la Toile, page + à la plantation
python3 redteam_tokens.py      # 19 — LE JEU FAIT AUTORITÉ : les valeurs décidées, les deux modes qui s'échangent,
                               #      zéro couleur et zéro police en dur dans les <style>, JSON = bloc CSS = Swift.
                               #      Sans navigateur : il ne flotte pas, et il se passe en une seconde.
python3 redteam_studio_geste.py # 13 — LE GESTE DE COULEUR DU STUDIO, au vrai doigt (CDP) :
                               #      appui 480 ms, horizontale = teinte, verticale = palette,
                               #      on revient exactement d'où l'on vient (Q125), et le
                               #      glissement de MONDE garde la main. Constantes en dur.
python3 redteam_apercus.py     # 8 — UN APERÇU DE TOILE PORTE TOUJOURS DE LA MATIÈRE COLORÉE :
                               #     le fond du Studio, les cinq mondes gratuits, et la DEUXIÈME
                               #     ouverture (buildStudio repeint sans `_shAllColored`, et le
                               #     semis juste est accroché à `.show`, que #studioScreen ne perd
                               #     jamais). On compte les pixels FRANCS ET FROIDS — un seuil de
                               #     saturation seul compte les crèmes et passe au vert sur un
                               #     écran mort. Plancher PAR MONDE, relevé sur la référence.
python3 redteam_nuee_dalle.py  # 38 — (+ un Promi planté dans une Nuée a sa dalle reliée) — une Nuée a SA dalle sur la Toile (au doigt, après plantation, couleur figée) et son bloc du Cercle ; sa couleur ne touche pas ses Promi
python3 redteam_rythme.py      # LE RYTHME D'UN MONDE NE DÉRIVE PAS (Tom, 26 sept.) — 13 mondes, arrivée et départ, par le
                               #   moteur ET par le vrai chemin, contre les valeurs EN DUR de la version validée (v60) :
                               #   fin du mouvement dans le moteur (tous à l'horloge depuis v61) ; HOULE = EXCEPTION, par image,
                               #   on juge ses images ; + cadence ≥ 60 %. Lancé avec le VRAI GPU (sans lui, Madrure prend son
                               #   chemin de secours). `--bride=3` prouve que la durée ne dépend pas de la charge.
                               #   Seul (≈ 8 min ; --sans-reel ≈ 4). ⚑ DANS LA SÉRIE À CHAQUE LOT QUI TOUCHE UN MONDE OU UNE LATENCE.
python3 redteam_decoupe.py     # UNE DALLE N'EST JAMAIS UNE IMAGE DÉCOUPÉE (Tom, 23 sept.) — piège drawImage/
                               #   getImageData/putImageData/createPattern/toDataURL à l'exécution, 19 écrans × 2 thèmes,
                               #   six familles (découpe · redimension · pixels · fragment de Toile · motif · PHOTO).
                               #   Échoue sur toute ligne NOUVELLE ; la dette de naissance (24 lignes) est SOLDÉE en v29,
                               #   `decoupe-dette.json` est vide. À PASSER À CHAQUE LOT QUI TOUCHE UNE DALLE.
                               #   Le contrat d'un monde : CONTRAT-MONDE.md.
python3 redteam_flash.py       # 32 — RIEN NE PARAÎT UNE FRACTION DE SECONDE (Tom, 30 sept. : « la deuxième fois qu'ils
                               #   reviennent »). Image par image, WebKit ET Chromium, au doigt : l'ouverture, le + → les trois
                               #   natures, planter les trois. Premier plan (grille 6×11, opacité ≥ .12) : aucune couche < 800 ms
                               #   ni au début ni à la fin, jamais l'ancien chrome ; la page + paraît COMPOSÉE dès sa première
                               #   image (nature, plateau à l'encre finale, phrase à sa mise en page finale) ; une plantation
                               #   COUPE, la page + ne reprend pas son aspect d'avant. Prouvé : 9/32 sur app-avant-v103b.
                               #   ⚑ À PASSER À CHAQUE LOT QUI TOUCHE UNE OUVERTURE, UNE FERMETURE OU UN MINUTEUR DE COMPOSITION.
python3 banc_rendu.py          # 280 images AU PIXEL — LE BANC DE RENDU DE RÉFÉRENCE (assainissement, 30 sept.) : 20 mondes × Toile
                               #   (clair, sombre, sans titres) + 4 dalles × 3 tailles ; hasard amorcé, horloge et images pilotées.
                               #   `--deux` prouve le déterminisme, `--figer` pose la référence (banc-rendu/ref/). C'est lui qui juge
                               #   le portage. ⚑ À PASSER À CHAQUE LOT QUI TOUCHE LE MOTEUR OU UN MONDE.
python3 redteam_notifs.py      # 36 — LES NOTIFICATIONS (v109), WebKit, permission simulée : jamais au lancement ; « Je te le rappelle ? »
                               #   à la plantation d'une parole DATÉE, demande seulement après « oui » ; deux « pas besoin » puis plus rien ;
                               #   RIEN QUAND LA DATE EST PASSÉE ; les mots EN DUR ; une par jour ; « C'est aujourd'hui » à l'heure choisie ; la page (mur Ma Parole !).
python3 redteam_murs.py        # 26 — LES MURS DU CERCLE (v104–v105), au doigt, deux thèmes : aucun encart, flou 4,8 px ; la phrase
                               #   POSÉE SUR LE FLOU (centrée dans le mur, sans fond ni trait, ≤ 3 lignes, une taille, encre/crème),
                               #   le temps d'être lue (3 à 5,5 s) puis elle s'efface ; la 1re fois l'offre s'ouvre à la fin de la
                               #   lecture ; pendant qu'elle est là un toucher n'importe où ouvre l'offre ; compteur GLOBAL, 21 phrases
                               #   EN DUR puis hasard sans répétition, 14 jours, rien au Cercle payé. 20/26 sur app-avant-v105.
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
> **Décision Tom, 10 septembre 2026.** Vécu au portage de la Pelote : le juge comparait la vitesse de
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

> ### ⚠ UNE DALLE SE LIT PAR SA TEINTE — UN SEUIL DE LUMINANCE SEUL MENT DANS LES DEUX SENS
> **Décision Tom, 10 septembre 2026, au juge de la Pelote :** *« Deux couleurs de même clarté et de teintes
> opposées se distinguent parfaitement ; un seuil de luminance seul déclarera illisible ce qui se lit et lisible
> ce qui ne se lit pas. »* Mesuré sur les îles de la sphère, à vue figée : une dalle ORANGE sur la sphère bleue
> se lit franchement à **21,7** d'écart de luminosité ; une dalle pâle en clair ne se lit presque plus à
> **22,6** — l'ordre est inversé. En écart de COULEUR (ΔE, CIELAB, couleurs moyennes au cœur de l'île, avec et
> sans elle) : **84 contre 11**. Et le 42 du §3 aurait condamné une dalle blanche parfaitement lisible (25 à 39).
> **La règle :** la lisibilité d'une matière colorée — une dalle, une île — se mesure en **ΔE** ; le seuil de
> luminance du §3 garde son objet (un TRAIT sur un aplat) et ne se transpose pas. **Un critère de luminance peut
> s'AJOUTER** — il attrape autre chose : une dalle juste en teinte mais noyée en clarté. Plancher de la Pelote :
> **ΔE 15** (Q192). **Corollaire de l'instrument :** chaque objet se mesure LÀ OÙ LE MOTEUR LE POSE, jamais dans
> un masque seuillé — le masque fragmente l'objet pâle, un filtre de taille en jette les morceaux, et le plus
> illisible sort de la mesure par construction (voir la ligne du §8).

> **Ce qui reste interdit :** desserrer un seuil, retirer un contrôle, ou changer le
> comportement de l'app pour faire passer un test. Un simple **changement de nom de nœud**
> (`.ix-bloc` → `.s4-carte`) ne relève pas de cette procédure : c'est un renommage,
> l'intention est intacte — on le note, on ne délibère pas.

> ### ⚠ UN CONTRÔLE QUI PREND UN DÉFAUT ALÉATOIRE N'EST PAS INSTABLE — IL FAIT SON TRAVAIL
> **Décision Tom, 11 septembre 2026 :** *« un contrôle qui prend un défaut aléatoire une fois sur trois n'est pas
> instable, il fait son travail. Un relancer vert ne l'annule pas. »* Né du chantier 59 : la couleur d'une dalle est
> tirée au hasard à chaque chargement (`cc()`, `Math.random`), et quand le tirage tombe près du sol de la sphère la
> dalle ne se lit plus. `releve-aura` le prend en nommant la dalle — mesuré : **6 chargements sur 10** portent au moins
> une dalle sous le plancher (ΔE 15) ; dans la série du 11 septembre, « planter un arbre » à ΔE 12,2.
> **La règle :** quand le rouge nomme un défaut RÉEL que le produit tire au hasard, **le rouge est le résultat** ; le
> vert d'un nouveau chargement dit seulement que le tirage est tombé ailleurs. On ne l'écrit jamais « reconfirmé
> vert » : on écrit **« défaut du chantier n, pris à ce passage »**, et le défaut reste ouvert jusqu'à sa correction.
> **Ce que ce n'est pas — la distinction à faire AVANT de relancer :** le paragraphe suivant vise un INSTRUMENT qui
> oscille (il mesure la respiration d'un canevas, pas un défaut : le dessin est juste, c'est la sonde qui flotte). Ici
> c'est le PRODUIT qui varie, et le contrôle le voit. **Le test :** le rouge nomme-t-il une chose fausse à l'écran, qu'on
> peut regarder ? Si oui, c'est un défaut, aléatoire ou non — relancer ne sert qu'à mesurer sa fréquence.

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
| **Un écran rouvert n'est plus celui de la première fois — et rien ne rougit** | **⚑ `#studioScreen` ET `#auraScreen` NE PERDENT JAMAIS LEUR CLASSE `.show`.** (Nommé le 22 sept. 2026, après la TROISIÈME fois qu'elle casse quelque chose.) `closeAll()` les ferme autrement — en les glissant hors champ — mais la classe reste posée. **Tout ce qui est accroché à un `MutationObserver` sur `.show` ne se réveille donc QU'UNE FOIS, au tout premier passage.** Les trois : ① le régulateur de densité de la Pelote n'appliquait jamais sa vise (seul un rechargement la faisait mordre) ; ② l'anneau des Noyaux ; ③ le semis du Studio — `buildStudio` repeint `#stBg` sans `_shAllColored`, `poseToile(true)` devait réparer, et ne rejouait jamais : **première ouverture juste, toutes les suivantes à 14 cellules colorées sur 72**. **Parades, dans cet ordre :** on n'observe JAMAIS une classe sans avoir vérifié qu'elle se RETIRE (une mesure, pas une lecture : `classList.contains('show')` après `closeAll`) ; ce qui doit se rejouer à chaque ouverture s'accroche à la FONCTION qui ouvre (on l'ENVELOPPE, §8) et non à un état ; et ce qui doit s'appliquer « quand personne ne regarde » s'accroche à `closeAll` et à `visibilitychange`. ⚠ **Et le symptôme ne ressemble jamais à sa cause** : un écran qui sort à moitié peint la deuxième fois, un réglage qui « ne prend qu'au rechargement ». Devant l'un des deux, chercher la classe AVANT le reste. |
| **Une animation fige tout le produit, alors qu'elle ne dessine que sur un écran** | **`offsetParent` NON NUL NE VEUT PAS DIRE VISIBLE.** Un écran fermé n'est pas en `display:none` : il est **glissé hors champ** (`translateY(100%)`, opacité 0) et **garde son `offsetParent`**. Toute boucle qui filtre « les écrans visibles » sur ce critère **écrit sur tout le produit**. Vécu le 10 septembre 2026 : `frame()` (ombre de dalle, ≈ l. 8917) écrit trois variables CSS **héritées** sur les **douze** écrans `.tuto-fond`, fermés compris, à chaque image — et sa propre lecture d'`offsetParent` à l'image suivante force le recalcul de style de milliers de nœuds cachés. **27 % du fil principal**, partout dans l'app ; l'élan de l'Aura en sortait figé (images de 267 ms). **Parade : un écran est visible s'il porte `.show`** (la classe que le code pose, §8 — jamais une géométrie). **Et au profileur, le temps de mise en page est attribué à la fonction qui LIT** (`offsetParent`, `getBoundingClientRect`), pas à celle qui a sali : chercher l'écriture ailleurs. → CHANTIERS.md, chantier prioritaire. |
| **Une mesure de dalles perd justement la plus illisible** | **UN MASQUE FRAGMENTE UN OBJET PÂLE, ET UN FILTRE DE TAILLE EN JETTE LES MORCEAUX.** Le juge de la Pelote retrouvait les dalles dans un masque « avec − sans » (seuil 12) et ne gardait que les composantes de 300 cellules : une dalle bleue sur bleu s'y découpe en morceaux de 1 à 274 cellules — **la dalle la plus illisible sortait de la mesure**, et « la plus faible » rapportée était la suivante (10 sept. 2026, Q192). **Parade : mesurer chaque objet LÀ OÙ LE MOTEUR LE POSE** (son centre, recoupé avec ce que l'app publie), jamais le retrouver dans un masque. **Et une dalle se lit par sa TEINTE** : la luminance confond l'orange qui se lit (Δlum 18) et le bleu sur bleu qui ne se lit pas (13) ; l'écart de couleur (ΔE, CIELAB) les sépare — 84 contre 9. |
| **Une porte s'ouvre et se referme aussitôt — au doigt seulement** | **LE CLIC FANTÔME.** Après un toucher, le navigateur synthétise mousedown / mouseup / click **au point du doigt, APRÈS `touchend`**. Une porte qui ouvre au lever du doigt (`pointerup`) ouvre AVANT ce clic — et le clic tombe sur ce qui vient de s'ouvrir : `#scrim`, dont le clic referme tout. Vécu le 11 sept. 2026 : la porte des dalles de l'Aura (`openDetail(139)` → clic sur `#scrim` → rien d'ouvert) **et la porte des Noyaux de l'Aura, d'origine** — sur un téléphone, toucher un Noyau n'ouvrait rien de visible. **Les juges jouaient à la SOURIS : à la souris ce clic arrive sur l'élément de départ, tout est vert.** **Parades :** une porte s'ouvre sur le `click` (le lever du doigt l'arme : même élément, sous le seuil) — `_porteAuDoigt` de lot-DALLE-PORTE ; et `lot-CLIC-FANTOME` avale un clic issu d'un toucher qui tombe sur une COUCHE OUVERTE PENDANT LE GESTE (sa couche `.show` n'était pas ouverte quand le doigt s'est posé) — jamais un clic de souris ni de script, jamais un clic sur une couche déjà ouverte. ⚠ Une première écriture comparait l'élément touché à l'élément cliqué : elle aurait avalé un vrai toucher sur un bouton redessiné sous le doigt, et aucune série (souris) ne l'aurait vu — **un garde se borne à la forme exacte du défaut**. **Toute porte se prouve AUSSI au vrai doigt** (`Input.dispatchTouchEvent`, contexte `has_touch`) : `sauvegardes/aura-trois/doigt_defile.py` (une porte), `balayage_fantome.py` (tout un écran, doigt contre souris). |
| **Un composant réutilisé sort sans sa mise en page** | **SON CSS EST RATTACHÉ À `#device`, ET LA FEUILLE VIT SOUS `.frame`.** La carte d'Index (lot-S4) est stylée par `#device .s4-carte` ; la fiche d'une personne vit sous `.frame`, hors de `#device` (le §8 le dit déjà pour `personSheet`). Ses vraies cartes, bâties par le moteur de l'Index, s'y **empilaient en colonne à x = 0**, sans aucune erreur (11 sept. 2026). **Parade : re-rattacher LES MÊMES VALEURS au conteneur qui accueille le composant, et l'écrire** — si le composant change à sa source, il doit changer là aussi. Et un moteur enfermé dans un lot se réutilise par SA porte publique (`_s4Index`, prêtée le temps d'un appel, tout rendu à l'identique) — jamais par une copie de la carte. |
| **Un bouton intercepté casse tout ce qui l'ouvre par programme** | **UN CLIC SCRIPTÉ N'EST PAS UN DOIGT.** Le + de l'accueil ouvre maintenant les trois natures sur place ; intercepter TOUT clic sur `#createBtn` a fait tomber `redteam_vide`, `pastilles`, `gens`, `tuiles` et fait planter `aveugle` (13 sept. 2026) — ils ouvrent la page + par `createBtn.click()`. **Parade :** un comportement de geste ne vise que `ev.isTrusted` ; un appel par script garde le chemin d'avant. Et **une commande déplacée garde ses gestionnaires** : on DÉPLACE `#createBtn`, `#filBtn`… dans le nouveau chrome, on ne les recrée jamais. |
| **Un libellé posé sur un canevas se mesure trop tôt** | **LA POLICE N'EST PAS ENCORE LÀ QUAND LA CARTE SE PEINT.** Le libellé « Promi » d'une carte d'Index mesurait **53** au moment de `peintCarte` et **64,5** ensuite : la dalle, décalée d'après la première mesure, passait 3,5 px SOUS le libellé (§4). Et en densité « 3 par ligne » (carte de 106), le décalage mangeait toute la largeur : **la dalle n'était plus peinte du tout** — seul `releve-S4` l'a vu. **Parades :** la largeur d'un libellé est une COTE relevée police chargée (Promi 65 · Chiche 72 · Nuée 60), jamais une mesure au moment de peindre (§8, « la cote se calcule ») ; sur une carte étroite la dalle descend sous le libellé. ⚠ Et **un peintre déclare la boîte qu'il a VRAIMENT peinte** (`data-matiere`, `data-matieres` pour une petite Toile) : la boîte d'avant décalage restait déclarée, et un contrôle qui ne lit que la déclaration ne voit pas une dalle écrasée à 0 — `redteam_reperage` compte donc aussi les pixels. |
| **On trie 41 règles à la main, et 37 ne peignaient rien** | **UNE RÈGLE QUI DÉCLARE UNE COULEUR NE LA PEINT PAS FORCÉMENT — ON TRIE LES SURFACES, JAMAIS LES RÈGLES.** Vécu le 17 septembre 2026 en finissant l'échange de rôle de la Nuée : **41 règles CSS déclaraient un aplat en `#291547`**, et il a fallu décider pour chacune si elle peignait un CHAMP ou un ACCENT — un tri long, à l'œil, sur 41 sélecteurs. **En mesurant le RENDU plutôt que les règles : quatre surfaces.** Les 37 autres étaient écrasées par une règle postérieure ou par le JS — le §7 le dit depuis le début (« 2 400 règles dont 54 % sont mortes »), mais on l'oublie dès qu'on lit une feuille de style. **Parade : on parcourt le DOM écran par écran, on lit le `backgroundColor` CALCULÉ, et on ne garde que ce qui se peint** (`scratchpad/surfaces_mauve.py`). Le tri tombe alors de 41 décisions à 4, et chacune se regarde vraiment. ⚠ **Et une classification automatique se trompe** : « grande surface qui porte du contenu = champ » sortait la barre Peaufiner en CHAMP et ratait qu'elle EST un champ pour une autre raison (elle porte la couleur de champ de sa nature sur les deux autres). **Le critère se décide à l'œil, la mesure ne fait que réduire la liste.** |
| **Un écran sort VIDE, et la console ne dit RIEN** | **UNE FONCTION ENFERMÉE DANS UNE IIFE, APPELÉE DEPUIS UNE AUTRE, SORT EN `ReferenceError` — ET LE `try/catch` DU MOTEUR L'AVALE.** Vécu le 17 septembre 2026 : un traducteur de couleur `_nt()` posé dans l'IIFE de `NATCOL`, appelé par les deux peintres de carte, qui vivent dans un AUTRE bloc. **L'Index sortait vide — zéro carte — sans une seule erreur en console**, parce que son moteur enveloppe chaque carte dans un `try/catch`. ⚠ **Et la sonde était VERTE** : elle mesurait le contraste des textes présents, et il n'y en avait plus aucun. **Seule la CAPTURE l'a vu.** **Parades :** une aide partagée entre deux blocs se pose sur `window`, jamais dans une IIFE — et **tout lot qui touche à un peintre se termine par une capture REGARDÉE**, plus un comptage du nombre d'éléments rendus (`#indexList .s4-carte` → 12, pas 0). Un contrôle qui ne compte que la qualité de ce qui est peint ne voit pas l'absence. |
| **Une flèche a un trait qui lui sort par la pointe** | **UN BOUT ROND DÉPASSE DE LA MOITIÉ DE SA LARGEUR.** Un trait qui s'arrête AU point d'arrivée le déborde de `lineWidth/2` quand `lineCap` vaut `round` — et si ce point est la POINTE d'un chevron, le trait sort par le V. Vécu le 23 sept. 2026 sur les deux flèches de la page + : le ruban du trait finissait à `cx + ep·0,6`, c'est-à-dire exactement où `chevron` pose sa pointe (`6·k`, `k = ep/10`) ; et la flèche d'invite du §2.4 finissait à `B` avec un cap de 4,5, donc 2,25 px au-delà de sa propre tête. **Parade : le trait s'arrête EN DEÇÀ** — sous les branches arrière du V pour le premier, de `lineWidth/2` pour le second — et c'est son bout rond qui vient tomber pile là où la tête se referme. |
| **On change de police et tous les textes auto-dimensionnés rétrécissent** | **UNE CONSTANTE DE LARGEUR MOYENNE EST CELLE D'UNE POLICE, PAS UNE LOI.** Le §2.8 estime une ligne par `Σ(caractères × taille × 0,53)`, et **0,53 a été relevé sur la police de la planche**. Depuis Gilbert (16 sept.), le coefficient réel est **0,44** (mesuré sur les mots réels, `scratchpad/coef_phrase.py`) : l'estimation sur-contraignait de 20 %, et la phrase de la page + sortait à **25 px là où la planche en compose 35**. Rien dans le code ne le disait ; seul l'œil de Tom l'a vu (« quand on avait l'ancienne police c'était pas aussi petit justement »). **Parade : toute constante qui traduit des CARACTÈRES en PIXELS se remesure au changement de police** — et on cherche ses sœurs (le 32 par pastille et le 11 par écart, eux, sont des px : ils ne bougent pas). |
| **Un filet posé en `box-shadow` est tronqué, et rien ne le recouvre** | **UNE OMBRE DÉBORDE DE L'ÉLÉMENT — DONC TOUTE BOÎTE QUI ROGNE LA COUPE.** `elementsFromPoint` ne trouve rien par-dessus (normal, rien n'y est) : c'est la RANGÉE qui clipe. `.au-nx` et `.aura-track` portent `overflow:auto hidden` parce qu'elles glissent. Mesuré en repeignant l'ombre **en rouge pur** et en parcourant les 360° : **96,4 % du tour, trou de 264 à 277°**, au sommet du plus grand disque. Rembourrer la rangée ne suffit pas (90,0 → 94,7 %) et déplace la composition. **Parade : ce qui doit cerner se peint DANS la boîte, et par le peintre lui-même, en DERNIER** — l'anneau finit exactement au bord de son canevas (`R + lw/2 = W/2`), le filet occupe ses 1,4 derniers pixels. Ce qui est dans la boîte ne peut être rogné ; ce que le peintre trace en dernier ne peut être recouvert par lui-même. ⚠ Et une passe EXTÉRIEURE qui peint dans un canevas est effacée au rendu suivant (mesuré : 0 % du tour). |
| **Deux titres à la même taille en pixels n'ont pas la même taille à l'œil** | **LA TAILLE EN PIXELS NE DIT RIEN SANS LA POLICE.** Mesuré à 27 px, police chargée : **PromiLate** cap 19,9 et « Réglages » large de **163,8** ; **Gilbert** cap 18,9 et large de **101,7** — une fois et demie plus étroit. Un relevé qui compare des `font-size` conclut « tous pareils » là où l'œil voit deux familles. **Parade : comparer la HAUTEUR DE CAPITALE et la LARGEUR RENDUES** (`measureText`, `actualBoundingBox*`), jamais la seule cote déclarée. |
| **Un texte auto-dimensionné reste coupé, et la boucle qui devait le réduire « tourne »** | **ELLE POSE SANS `important`.** Le titre d'une carte d'Index rétrécit tant qu'il déborde — `t.style.fontSize = fs+'px'` — mais `#device .s4-ti{font-size:24px!important}`, posée plus bas, gagne : la boucle tourne huit fois, `scrollHeight` ne bouge jamais, et le titre reste coupé (mesuré : « planter un arbre » rendait 33 px de haut pour 48 de texte). C'est « la taille qu'on LIT n'est écrite par aucune règle » (ligne plus bas), vu de l'autre bord : ici c'est NOTRE écriture qui est écrasée. **Parade : `setProperty(..., 'important')`, et vérifier que la mesure bouge d'un pas à l'autre.** |
| **Un bloc bâti après le poseur reste à y 0 et recouvre l'entête** | **L'ORDRE, PAS LA COTE.** Le fil d'une Nuée est placé par `_ficheCotes` — mais il est BÂTI APRÈS elle : sur une Nuée pleine il rendait à **y 0** sur 862 de haut, sous l'encart, le titre et la méta (mesuré sur 9 Promi). ⚠ **Et les deux parades évidentes sont fausses** : rappeler le poseur entier sans son contexte renvoie toute la fiche hors de l'écran (tout à y ≥ 844) ; tester « le `top` n'est pas posé » non plus (le poseur écrit 30, une valeur posée ET fausse). **Le seul critère juste est LA FORME DU DÉFAUT — le recouvrement** : on n'intervient que si le bloc passe au-dessus du bas de ce qui le précède. Un juge le confirme : `redteam_nuee` doit rester à son chiffre d'avant. |
| **Une sonde d'air « à l'encre » rend 0 sur une phrase, et 28 sur la suivante** | **ELLE PART DANS L'ENCRE.** Une sonde qui remonte puis descend depuis une cote jusqu'au premier pixel peint rend **0 si la cote tombe déjà sur de l'encre** — et c'est ce qui arrive quand on lui donne le bas d'une **boîte de ligne** : le **jambage** d'un « g » ou d'un « p » descend dessous. Vécu le 22 sept. 2026 : `ENCRE_GAP` rendait 0,0 pt sous « …à la légère. », 28,0 sous la phrase d'à côté, dans les deux thèmes — un faux rouge parfaitement reproductible, donc crédible. **Parade : sortir de l'encre par le bas AVANT de scanner** (0,0 → 26,5). Même famille que « un contrôle qui compte des pixels mesure la respiration du monde » : avant d'accuser le dessin, on vérifie l'instrument. |
| **Un balayage de couleurs ne voit pas un écran FERMÉ, même en `display:block`** | **UN ÉCRAN FERMÉ EST GLISSÉ HORS CHAMP** (§8, `translateY(100%)`), et un balayage qui filtre sur `visibility`/`display`/`opacity` le garde — tandis qu'un balayage qui filtre sur le rectangle de l'appareil le PERD. Vécu le 22 sept. : la dernière surface en amande du produit vivait dans l'aide de l'Aura, **à y 1603**. Les balayages d'avant, qui n'ouvraient pas cet écran, la déclaraient absente. **Parade : on OUVRE chaque écran, un par un, et on borne au rectangle de `#device`** — jamais « tous les nœuds du document ». |
| **Une bascule de palette paraît faite, et l'ancienne identité reste** | **UNE COULEUR PEUT VIVRE EN TRIPLET JS — `[58,84,255]` — ET AUCUNE PASSE TEXTUELLE NE LA VOIT.** Ni `#3A54FF`, ni `rgb(58,84,255)` : trois chiffres dans un tableau. **47 tableaux** en portaient : `NAT` (la Pelote), `SPECTRE`, `GPIX·GBRA·GLI·GMOS·GENC·GLIGHT` (les rampes de fond de la Toile), `SIG`, `ETATS`, `KC`, les grappes de l'onboarding et de la page +. Ils ont traversé **deux** lots de palette intacts, et c'est ce qu'on voyait « encore sur la sphère et sur les dalles ». ⚠ Et le motif `[[r,g,b],…]` n'en attrape que la moitié : **30 triplets vivent SEULS** (`nuee:[41,21,71]`, `var mauve=[…]`), il faut une seconde passe. **Parade : une bascule se TERMINE par un audit qui cherche chaque ancienne valeur sous SES TROIS FORMES — hexadécimal, triplet, `rgb()`.** Sans cet audit, la conversion est fausse et paraît juste. |
| **Une dalle change de couleur sans que personne ne l'ait repeinte** | **DEUX VOLEURS DE COULEUR.** 1 · `cc()` tirait la couleur au hasard à chaque chargement (corrigé : couleur figée, §4). 2 · **la réserve de l'onboarding n'est jamais vidée** : `Toile.reserve()` n'est posée que par l'onboarding, et `applyReserve` éclaircit ensuite au ton le plus clair de la palette (le lilas en Signal) **toute dalle qui passe sous ses anciens textes**, pour toujours. Vécu le 13 sept. 2026 : une fois la couleur figée, 2 à 4 dalles par chargement sortaient encore lilas, à des places différentes. **Parade :** la réserve n'éclaircit plus une dalle reliée à un Promi (`bs.pid==null`) **ni une dalle de Nuée** (`kind:'nuee'`, qui n'a pas de `pid` — elle sortait lilas puis bleue, pris par `redteam_nuee_dalle`). ⚠ Et un contrôle qui compare des Promi d'un chargement à l'autre les compare **par titre et personne, jamais par id** : les ids du jeu de démonstration changent (chantier 71) — le premier juge de ce lot comparait deux Promi différents. |
| **Au doigt, la tuile « Un Chiche » ouvre un Promi — à la souris tout est juste** | **UN ANCIEN CARROUSEL ÉCOUTE ENCORE LE DOIGT.** L'écran des choix de la page + (`pp-choix`) empile les trois tuiles, mais le carrousel horizontal d'origine (≈ l. 8805) écoutait toujours `touchstart`/`touchend` : au lever du doigt, `up()` rejouait `goTo(cur)` — la tuile d'AVANT —, l'écran passait à la phrase de cette nature SOUS le doigt, et le clic synthétisé tombait sur le geste. Vécu le 13 sept. 2026 : **sur un téléphone on ne pouvait pas lancer un Chiche depuis le +, et après une Nuée la tuile Promi gardait `data-kind="nuee"`.** Aucune batterie ne le voyait : **elles jouaient toutes à la souris.** Pris au piège par `scratchpad/acc_chiche_piege.py`. **Parade :** le carrousel ne s'arme pas sur `pp-choix`, et un toucher qui ne franchit pas le seuil ne change jamais de tuile. **Toute porte, tout choix se prouve AU DOIGT** (`Input.dispatchTouchEvent`, contexte `has_touch`) — `redteam_tuiles.py`, `redteam_gens.py`. ⚠ Au-delà d'environ 10 px de déplacement, ni Chromium ni iOS ne font un toucher : un contrat « qui glisse de 20 px » ne juge pas un toucher. |
| **On grossit un jeton de taille et RIEN ne bouge** | **UN JETON DÉCLARÉ N'EST PAS UN JETON CÂBLÉ.** `--t-titre-taille`, `--t-sous-titre-taille` et `--t-libelle-taille` sont déclarés dans `lot-TOKENS-css` — et ils ont **ZÉRO consommateur** : `var(--t-…-taille)` n'apparaît nulle part dans les 32 000 lignes. Le bloc `:root{--t-sous-titre-taille:27px;--t-libelle-taille:18px}` du lot des neuf points ne peignait donc **rien** ; le facteur ×1,217 n'a agi que par les règles explicites posées à côté (43 · 36 · 33 · 28 · 24). **Parade : avant de changer un jeton, compter ses consommateurs** (`grep -c "var(--jeton)"`). Un jeton à zéro consommateur se câble ou se laisse — on ne le repose pas en croyant peindre. (Le JSON garde ses sept niveaux : c'est le câblage qui manque, et il compte pour le portage Swift.) |
| **La taille qu'on LIT n'est écrite par aucune règle** | **`echelle()` EST LE PLANCHER DU §6, ET IL ÉCRIT EN LIGNE.** Mesuré aux Réglages : les libellés rendaient **13 px** alors qu'aucune règle du fichier ne dit 13 — le CSS les pose à **11,5** (`#device #settingsScreen .s2-cercle .s2-lab`, 2 ids + 2 classes, `important`) et `echelle()` (≈ l. 23533) les relève au plancher de 13, **inline, `important`, avec `data-ech`**. Un correctif écrit à 2 ids + 1 classe ne peint alors rien, et il le fait **en silence** : `.grouplab` (qui n'avait pas de règle forte) bougeait, `.s2-lab` et `.k` non. **Parade : piéger le peintre** (§7, on enveloppe `setProperty` et on lit la pile — 1 202 écritures de « 13px » trouvées en une passe), **corriger LA SOURCE** à une spécificité qui la bat (id doublé), et **ne jamais toucher au plancher lui-même** — le monter globalement avait resserré 156 paires d'air. |
| **Une capture d'élément sort ENTIÈREMENT NOIRE** | **LE NŒUD PORTE UNE ANIMATION.** `locator.screenshot()` sur un élément qui joue une animation CSS infinie (ici l'éclat qui traverse le bouton d'achat) rend une image **noire de bout en bout** — libellé compris. Rien n'est cassé dans le produit : vécu le 12 sept. 2026, les pixels du canevas sous-jacent étaient justes (moyenne 188/182/228, zéro pixel transparent), et j'ai d'abord conclu à un défaut de dessin. **Parade : ne jamais croire une capture d'élément sur un nœud animé — MESURER les pixels** (`getImageData` sur le canevas, ou la couleur moyenne du nœud), **et recapturer le CONTENEUR** (un `clip` sur la page entière) plutôt que l'élément. Même famille que « un comparateur d'images ment sur deux points » : avant d'accuser le dessin, on vérifie l'instrument. |

| **Un ancien écran paraît une fraction de seconde — et revient après chaque correction** | **UN ÉCRAN QUI SE COMPOSE PAR MINUTEURS SE MONTRE AVANT D'ÊTRE FINI.** (v103, 30 sept. 2026, la deuxième fois.) Trois formes mesurées image par image : ① **à l'ouverture**, une règle qui cache l'ancien chrome vit 37 000 lignes plus bas — le navigateur PEINT avant de la lire (`.topbar`, `.footer` 250 à 400 ms en WebKit) → la règle se double dans `<head>` ; ② **entre le + et la nature**, la page + était montrée dès sa nature posée, puis se composait sous l'œil (champ à +240, phrase par `arme` à +60/+340, encre du plateau à +120/+420 ; et `pose()` refusait de bâtir le plateau d'une feuille cachée) → elle reste cachée jusqu'à 450 ms après le DERNIER déclencheur et deux images identiques, plateau bâti ; son fondu d'entrée est retiré (Chromium y montrait la feuille telle qu'il l'avait peinte la dernière fois) ; ③ **à la plantation**, la page + reprenait son aspect d'avant (~100 ms) avant de glisser → on COUPE. **Deux images identiques ne prouvent rien : entre deux minuteurs, rien ne bouge.** Et **le voile d'un écran caché est un état lui aussi** : il grisait l'accueil pendant l'attente. Juge : `redteam_flash.py`. |
| **Un toucher sur le Peaufiner ne déclenche rien — à la souris tout marche** | **LE PEAUFINER NE PRODUIT AUCUN `click` AU DOIGT** (v104, mesuré en WebKit) : ses propres écouteurs annulent la fin du geste, le navigateur ne synthétise pas de clic. Un écouteur de `click` n'y voit donc JAMAIS un toucher. **Parade : lire le toucher lui-même** — appui puis lever sans glisser (`pointerdown`/`pointerup`, < 10 px, < 600 ms) — et avaler le clic qui pourrait suivre. Et un réglage flouté est en `pointer-events:none` : le doigt ne l'atteint pas, **un mur se reconnaît à sa GÉOMÉTRIE** (le point tombe dans son rectangle). |
| **On retire une fonction et l'app ne démarre plus — `node --check` est vert** | **UNE FONCTION SUR PLUSIEURS LIGNES, RETIRÉE PAR SA PREMIÈRE.** (v105, retrait d'Arranger.) `targets()` faisait huit lignes ; en retirant la première, les sept autres sont restées au niveau du script — des instructions VALIDES (`if(mode==='inspi')…`), que `node --check` accepte, mais qui lèvent `mode is not defined` au chargement : le script s'arrête, `let theme` n'est jamais initialisé, et TOUT l'app tombe (`Cannot access 'theme' before initialization`). **Parade : après un retrait, charger la page et lire `pageerror`** (`scratchpad/errs.py`), pas seulement la syntaxe ; et comparer la structure à la sauvegarde (la ligne qui suit la fonction retirée doit être celle qui la suivait). |
| **Arranger « marche » et rien ne bouge** | **L'ANCIEN CALQUE.** `targets()` rangeait `promises[].x/y`, que seul l'ancien SVG de `render()` lisait ; la Toile du moteur (les graines) l'ignorait. Une fonction qui écrit dans un calque que plus personne n'affiche paraît vivante au code et morte à l'écran : **on le mesure en regardant ce qui est PEINT (les graines, `Toile_graines`), jamais ce que la fonction écrit.** |
| **Un monde tient 60 i/s au banc Chromium, et rame sur l'iPhone** | **UN DÉCOUPAGE (`clip()`) SE PAIE À CHAQUE TRACÉ SUR LE MOTEUR DE SAFARI — ET CHROMIUM NE LE DIT PAS.** (v38, 24 sept. 2026.) Le coin arrondi de la Toile vivante était un `g.clip()` posé dans `frame()` avant la matière : en **WebKit** (CoreGraphics, le moteur de l'iPhone), Touffe passait de **51 à 205 ms par image** (154 ms pour un coin !), Taille-douce de 33 à 56 ; en Chromium, 14 ms et 5 ms seulement. Chromium headless peint le canevas en logiciel (Skia) et n'y fait presque pas payer un clip. **Parades :** ① on ne découpe pas la matière — on la peint, puis on repeint le FOND autour de la forme (pair-impair : un rectangle et la forme) ; ② **toute mesure de rendu se fait AUSSI en WebKit** (`p.webkit.launch()`, installé ; pas de bridage CPU : on mesure ×1) — un banc Chromium seul valide ce que l'iPhone ne tiendra pas. Outils : `sauvegardes/perf-v38/`. |
| **Un monde tient 60 i/s au banc Chromium, et rame sur l'iPhone** | **UN DÉCOUPAGE (`clip()`) SE PAIE À CHAQUE TRACÉ SUR LE MOTEUR DE SAFARI — ET LE BANC CHROMIUM NE LE DIT PAS.** (v38, 24 sept. 2026.) Le coin arrondi de la Toile vivante était un `g.clip()` posé dans `frame()` avant la matière : en **WebKit** (le moteur de Safari, donc de l'iPhone), Touffe passait de **51 à 205 ms par image — 154 ms pour un coin** —, Taille-douce de 33 à 56 ; en Chromium, 14 et 5 ms seulement (il peint le canevas en logiciel, Skia, et n'y fait presque pas payer un clip). **Parades :** ① ne pas découper la matière : la peindre, puis repeindre le FOND autour de la forme (pair-impair : un rectangle et la forme) ; ② **toute mesure de rendu se fait AUSSI en WebKit** (`p.webkit.launch()`, installé ; pas de bridage CPU, on mesure à ×1) — un banc Chromium seul valide ce que l'iPhone ne tiendra pas. Outils : `sauvegardes/perf-v38/`, CONTRAT-MONDE §8.4. |
| **Une dalle rendue « à sa taille » coûte dix fois plus, ou la Toile exportée sort petite dans un coin** | **v29, 23 sept. 2026.** ① `dalleTrame` cherchait la graine de chaque pixel parmi TOUTES les graines : à 200 px, 1,9 s pour une dalle Pixel. Parade exacte : ne passer que les graines qui PEUVENT gagner (\|t−k\| < 2·Rmax + w_k − w_t), et, par pixel, s'arrêter à la première qui ne peut plus (tri). ② `renderTo(cv, ech)` : six mondes font `setTransform(DPR…)` — si `ech ≠ DPR` la Toile se peint à la mauvaise densité ; `DPR = ech` le temps du rendu. ③ Un cache de rendu qui expire à l'horloge refait 120 ms de dalle à chaque toucher et fait perdre des touchers (`redteam_gens`, `redteam_verbe`) : la clé porte tout ce dont l'image dépend (taille, options, monde, thème, boîte de la cellule, couleur), rien d'autre ne l'expire. |
| **Un cache se reconstruit à CHAQUE image, et l'app gèle au moment de planter** | **UNE SIGNATURE DE CACHE PRISE SUR UN ÉTAT QUI BOUGE SE RECONSTRUIT À CHAQUE IMAGE.** (Tom, 23 sept. 2026.) Le cache de Madrure signait le semis (positions de repos, poids) — juste en apparence : à la plantation, le moteur fait GRANDIR la dalle et relâche toute la Toile pendant ~1 s, poids et positions changent à chaque image. Mesuré : **25 constructions pour une seule plantation** (×1) ; à ×4, **une par image, 830 ms chacune — 12 s figées**. Aucun banc « à semis fixe » ne pouvait le voir. **Parades :** tant que la signature d'une surface change d'une image à l'autre, on repeint l'état d'avant ; on reconstruit quand elle est POSÉE (deux images identiques), et on relance le moteur pour qu'il le voie ; la construction elle-même se fait PAR TRANCHES, l'ancien état restant affiché (v33 : ×4, pire image 450 ms au lieu de 1,4 s de gel). **Devant tout cache à signature : mesurer le nombre de constructions PENDANT une plantation, pas sur un semis au repos.** Et une signature se prend à la précision que l'œil voit (½ px), jamais au 1/16 : un relâchement qui converge sans fin la change encore dix images plus tard. |
| **Un titre rétrécit chez Tom, jamais au banc** | **DEUX UNITÉS DANS UNE MÊME COMPARAISON.** `ajusteTitres` comparait `scrollWidth` (pixels de MISE EN PAGE) à une place lue par `getBoundingClientRect` (pixels d'ÉCRAN, mise à l'échelle comprise). Au banc, l'appareil est à l'échelle 1 ; dans une fenêtre plus petite que le téléphone (le panneau de l'app de Tom), il est réduit — mesuré à 0,72 : Index, Réglages, L'aura à 23 px au lieu de 35 · 29 · 30. **Parade : ramener toute mesure à l'unité du titre** (`r.width / offsetWidth`) ; et **passer un banc à une échelle ≠ 1** (viewport 300 × 650) dès qu'une boucle compare des largeurs. |
| **Une page tourne à 100 % du processeur pendant des heures** | **UN OBSERVATEUR DU DOCUMENT QUI RÉÉCRIT DU TEXTE.** Le composeur des É (v35) observait chaque mutation du `body` et réécrivait le compte « Nuées » sous l'Index — que l'app réécrit à son tour : ping-pong sans fin, `redteam_ecrans` bloqué 2 h 46. **Parades :** une passe au plus par image (`requestAnimationFrame`), ne toucher que ce qui en a besoin (ici, le texte réellement en capitales), et un plafond par nœud (20 réécritures en 2 s → on renonce). **Et une série de batteries se lance avec une limite de temps par batterie** : un blocage ne doit jamais geler toute la série sans que personne le voie. |
| **Un régulateur mesure, vise… et n'applique JAMAIS** | **LA CLASSE QU'ON OBSERVE NE SE RETIRE JAMAIS.** Le régulateur de densité de la Pelote appliquait sa vise dans `prepare()`, appelé quand `#auraScreen` GAGNE `.show`. Or **`closeAll()` ne retire pas cette classe** : l'observateur ne se réveillait plus jamais, et la vise n'était appliquée **de toute la séance**. Mesuré : sous bridage ×8, vise 75 000, palier resté 110 000 ; à la réouverture, toujours 110 000. Le seul chemin qui la faisait mordre était le RECHARGEMENT, par le stockage — d'où « il descend et garde le palier ». **Parades :** on n'observe pas une classe sans avoir vérifié qu'elle se RETIRE ; et ce qui doit s'appliquer « quand personne ne regarde » s'accroche au moment où l'on QUITTE (on ENVELOPPE `closeAll`, §8) et à `visibilitychange`, jamais à l'ouverture seule. **Corollaire :** on ne persiste que ce qui a été APPLIQUÉ — persister la vise laissait un pic de trois secondes empoisonner tous les chargements suivants. |
| **Un flou de 2,4 px sur un trait de 6 px n'est pas un flou, c'est un halo** | **L'INSTRUMENT EST FAUX, PAS L'INTENTION.** Le voile du gratuit floutait la moitié droite des Noyaux de l'Aura : sur un bloc large (`.au-gr2`) ça floute ; sur un ARC de 6 px ça double sa largeur et pose une auréole sur le fond, entre les disques. `overflow:hidden` n'y peut rien — le halo est DANS le dessin, pas en dehors (et le lot avait justement posé `overflow:visible` « pour que le flou ne se coupe pas »). **Parade : garder le signal, changer le moyen, et prendre le moyen QUI EXISTE DÉJÀ SUR CET ÉCRAN** — `#ksocial` et `.ah-locked` disent « c'est le Cercle » avec une opacité (.5 et .6). On ne remplace jamais une décision écrite par une invention ; on lui emprunte son autre forme. |
| **Un contrôle d'air reste vert pendant que l'air disparaît** | **⚑ ON MESURE TOUJOURS L'ENCRE, JAMAIS LA BOÎTE** (Tom, 30 sept. 2026 : *« la trouvaille la plus importante du lot »*). `redteam_air` mesurait le rectangle des ÉLÉMENTS : l'agrandissement des faces (v96, `size-adjust:112%`) a grossi l'encre DANS des boîtes qui ne bougeaient pas — **609 paires resserrées, et il n'a pas rougi une fois** ; la fiche de Nuée est passée à 0 d'air sous « Avec » au vert. **Parade : l'air se mesure entre les rectangles du TEXTE** (`Range.selectNodeContents(e).getBoundingClientRect()`, ascendantes et descendantes de la police) — jamais `e.getBoundingClientRect()`. Même piège sous un autre nom : un juge qui dit « à l'encre » et lit une boîte (`redteam_nuee_entree` lisait le bas des Noyaux sur leur boîte, pas sur l'encre de leurs noms — 2 px de faux). Et **un juge ne voit que les écrans qu'il ouvre** : `redteam_air` en ouvrait 19 sur 34 ; un écran qui garde `.show` (Studio, Partager, l'Aura, son aide) se fait mesurer à la place du suivant si le juge ne repart pas d'un état vierge. |
| **Une preuve est verte sur un monde qui n'existe plus** | **UN `// commentaire` GLISSÉ DANS UNE FONCTION ÉCRITE SUR UNE LIGNE commente la fin de la ligne** — le bloc entier ne se charge plus, la fabrique du monde est absente, et le moteur retombe sans rien dire. Vécu en v72 : « Ramage vivant = 0 pixel d'écart » alors que Ramage n'existait plus. **Parade : après CHAQUE patch, `node --check` sur chaque `<script>` séparément** (un seul fichier joint peut encore passer), et une preuve relève aussi ce qu'elle a mesuré (le nombre de tracés, l'état), pas seulement l'écart. ⚠ **Revenu le jour même (v74), et cette fois `node --check` ne pouvait RIEN voir** : le commentaire avait avalé une affectation (`_vS = …`), la ligne restait syntaxiquement juste, et le calque net n'était jamais posé. **Règle : dans une ligne de code existante, on n'écrit JAMAIS `//` — seulement `/* … */`.** |
| **Le même dessin, peint en deux fois, sort différent — en Chromium seulement** | **CHROMIUM SUR GPU ANTICRÉNÈLE UN MÊME TRACÉ SELON L'ENDROIT OÙ IL VIDE SON LOT.** Mesuré en v72 : un plumage peint d'un bloc, puis par tranches (une relecture de pixel entre deux) → 7,3 % des pixels différents, sur les BORDS seulement ; WebKit : 0. **Avant d'accuser un calque ou une construction par tranches, mesurer ce témoin** — sinon on cherche un défaut de contenu qui n'existe pas. |

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
> vie du creux) **n'a pas d'angle à caler.** Vaut pour tout ce qui bouge : la Pelote, la Toile qui respire, un
> canevas animé. (Vérifié le 10 septembre : aucun faux vert de cette espèce n'a été trouvé dans le juge ; la
> règle est posée pour qu'il n'y en ait jamais.)

> ### ⚠ UN INSTRUMENT QUI RALENTIT AVEC LA MACHINE FABRIQUE DES FAUX CHANTIERS
> **Constaté le 12 septembre 2026 : DEUX chantiers du carnet, ouverts sur des mesures qui ne tenaient pas.**
>
> | Le chantier | Ce que je croyais mesurer | Ce que je mesurais |
> |---|---|---|
> | **n° 75** — la page + rend des hauteurs nulles en sombre | un défaut du produit, « antérieur au lot » | **mes propres Playwright concurrents.** Machine au repos : 6/6 sur QUATRE versions, dont celle sur laquelle j'avais « prouvé » que le défaut préexistait. Et 8/8 sous bridage CPU ×1 à ×10. |
> | **n° 73** — l'élan de la sphère tombe à 0 dès 100 ms par image | le produit qui perd l'élan sous charge | **mon lancer, joué dans la page et cadencé par `setTimeout`** — qui se dilate avec le bridage. Le DOIGT ralentissait avec la machine : 100 ms de balayage devenus 474 ms, livrés en UN mouvement. Au doigt CDP horodaté : 11 rad/s à ×1 comme à ×10, sur les deux versions. |
>
> **La règle : un instrument dont la cadence dépend du fil principal qu'il mesure ne mesure rien.** `setTimeout`,
> `requestAnimationFrame`, `page.mouse.move`, une seconde batterie qui tourne à côté — tous se dilatent avec la
> charge. **Un geste s'injecte par le CDP, avec un horodatage explicite par événement**
> (`Input.dispatchMouseEvent`, `Input.dispatchTouchEvent`) : il part du processus navigateur, donc sa vitesse ne
> dépend pas de la page. Et **une batterie qui rougit se repasse SEULE avant d'écrire quoi que ce soit** — le §7 le
> disait déjà pour les rouges ; il vaut aussi, et surtout, pour les CHANTIERS qu'on en tire.
>
> **Corollaire, et c'est la moitié utile de l'histoire : corriger l'instrument n'efface pas toujours le défaut, il
> le déplace.** Le n° 75 a disparu ; le n° 73 est devenu plus précis ET plus grave — l'élan ne dépend pas de la
> charge mais de **l'écart entre deux `pointermove`** (0,00 rad/s dès 120 ms d'écart, sur neuf essais), parce que la
> fenêtre était figée à 90 ms. **Quand une mesure s'effondre, on ne referme pas le dossier : on cherche la grandeur
> qui a la forme du défaut** (§7, « choisir la grandeur qui a la forme du défaut »).
>
> **Et Chromium peut CACHER le défaut de la cible.** Il regroupe les mouvements (`getCoalescedEvents`) et rend le
> paquet avec les horodatages d'origine. **Safari n'a pas cette API** : sur iOS, l'app ne voit qu'un mouvement par
> appel. Toute mesure de geste destinée à l'iPhone se fait donc **regroupement éteint**
> (`PointerEvent.prototype.getCoalescedEvents = function(){ return []; }`) — sans quoi on valide un comportement
> que le téléphone n'aura pas.

> ### ⚑ UN MOUVEMENT SE CALCULE SUR LE TEMPS RÉEL, JAMAIS SUR LE COMPTE D'IMAGES
> **Décision Tom, 10 septembre 2026, au portage de la Pelote.** Trois défauts de la même famille,
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
