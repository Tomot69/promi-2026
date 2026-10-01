# L'IDENTITÉ VERBALE DES TROIS NATURES — relevé + trois variantes par emplacement

> **⚑ TRANCHÉ PAR TOM, 17 septembre 2026 — POSÉ SUR `app-identite.html`, PAS SUR `app.html`.**
> Ses choix : 1.1 A · 1.2 Promi B · Chiche B · Nuée C · 2.1 A · 2.2 A · 2.3 A · 2.4 B · 2.5 A ·
> 2.6 A · 2.7 A · **2.8 de Tom** · 2.9 A · 3.1 B · 3.2 C · 3.3 C · 3.4 A · 3.5 C · 3.6 B ·
> **3.7 de Tom** · 3.8 B · 3.9 A · 4.1 A (+ « week-end » avec trait d'union) · 4.2 B · 4.3 B ·
> 4.4 B · **4.5 de Tom** · 5.1 A · 5.2 C · 5.3 B.
> **Les trois phrases de Tom**, qui ne figuraient dans aucune variante :
> 2.8 « une parole de plus sur ta Toile » · 3.7 « tu le lances — la dalle attend sa réponse » ·
> 4.5 « une Nuée, et chacun y plante la sienne ».
> **Les trois défauts du §0 sont réparés** : « brouillon » a quitté l'écran (D1), l'aide du Chiche
> dit désormais vrai (D2), et on LANCE un Chiche (D3).
> ⚠ **2.8 · 3.7 · 4.5 sont écrits, mais SANS PORTEUR** : `#csSub` et `#csH2` **n'existent plus dans
> le DOM** depuis le portage de la page + au moodboard — le cadre 17 ne montre que la question et
> les trois tuiles. Les trois phrases sont en place dans `setHead()` et s'afficheront si le
> sous-titre revient. **Je ne l'ai pas ressuscité : le §9 l'interdit sans décision.**
> ⚠ **Deux cotes serrées, mesurées** : 3.8 tient à **321,3 px dans 342** (20,7 de marge, Gilbert 22)
> et 4.3 à **235,8 px dans 240** (4,2 de marge).
>
> **Relevé du 17 septembre 2026**, fait dans `app.html`, emplacement par emplacement.
> Chaque ligne donne **le texte actuel**, son **adresse**, et **trois variantes**. Tom choisit.
> Registre demandé : celui des phrases du rejeu — « Tiens donc », « Comme d'habitude »,
> « Tu ne t'es pas fait prier ». **Lexique fermé** : Promi · Chiche · Nuée · Toile · dalle ·
> Noyau · planter · tenir · tracer · lancer. **Aucune injonction, aucun point d'exclamation.**
> Rien n'est intégré : ce document est une proposition.

---

## 0 · CE QUE LE RELEVÉ A TROUVÉ EN PASSANT — trois défauts, pas des propositions

| # | Défaut | Adresse |
|---|---|---|
| **D1** | **Le mot banni « brouillon » est À L'ÉCRAN, deux fois** : la ligne d'aide du gardé de côté (« tes brouillons se retrouvent dans l'Index ») et le libellé de nature d'une fiche (`dpType` → « Brouillon »). Le §2 l'interdit ; on dit **gardé de côté**. | `app.html:2577`, `app.html:3690` |
| **D2** | **L'aide sous la phrase MENT sur un Chiche.** Elle écrit « touche **Chiche** pour changer d'engagement » — or le code renvoie sans rien faire (`if(P.sens==='chiche') return;`) : la bascule ⇄ n'est même pas dessinée. | `app.html:5348` et `5361` |
| **D3** | **Le Chiche n'a ni geste ni bouton à lui** : il emprunte « glisse pour planter → » et « Planter le Promi » du Promi. Or **on lance un Chiche, on ne le plante pas** (lexique du §2). | `app.html:2569`, `app.html:9186` |

Les trois sont réparés par les choix ci-dessous ; **D1 est à corriger quel que soit le choix** (mot banni).

---

## 1 · L'ÉCRAN DES CHOIX — commun aux trois, c'est la porte

> Il porte la question, puis les trois tuiles. **C'est ici que les trois voix se séparent** :
> la question est commune, les sous-titres sont la première chose qui les distingue.

### 1.1 · La question — `app.html:2562`

**Actuel : « Qu'est-ce que tu promets ? »**

| | Variante |
|---|---|
| **A** | **Qu'est-ce que tu promets ?** *(inchangée — elle est au moodboard, cadre 17)* |
| **B** | **Qu'est-ce qu'on plante ?** |
| **C** | **Alors, qu'est-ce qu'on dit ?** |

> ⚠ **A est la seule sûre** : la question est dessinée au moodboard. B et C demandent un feu vert
> de dessin (la coupe de ligne change, §2.8 de la page +).

### 1.2 · Les trois sous-titres de tuile — `app.html:2563`

**Un Promi** — actuel : « à quelqu'un, ou à toi »

| | Variante |
|---|---|
| **A** | à quelqu'un, ou à toi *(inchangé)* |
| **B** | une parole qu'on donne |
| **C** | ce que tu tiendras |

**Un Chiche** — actuel : « un défi lancé »

| | Variante |
|---|---|
| **A** | un défi lancé *(inchangé)* |
| **B** | tu oses le lancer |
| **C** | à quelqu'un qui verra bien |

**Une Nuée** — actuel : « un groupe, un projet »

| | Variante |
|---|---|
| **A** | un groupe, un projet *(inchangé)* |
| **B** | à plusieurs, forcément |
| **C** | on s'y met ensemble |

---

## 2 · L'ÉCRAN DU PROMI — poétique, un peu décalé, jamais solennel

### 2.1 · L'exemple de la phrase, à SOI — `app.html:5289`

**Actuel (trois, qui tournent) : « reprendre la guitare » · « dormir avant minuit » · « ranger le garage »**

| | Les trois exemples |
|---|---|
| **A** | reprendre la guitare · dormir avant minuit · ranger le garage *(inchangés)* |
| **B** | rouvrir le piano · me coucher avant la nuit · finir ce livre |
| **C** | réapprendre à ne rien faire · rentrer avant les étoiles · vider ce tiroir |

### 2.2 · L'exemple de la phrase, à QUELQU'UN — `app.html:5291`

**Actuel : « aller voir la mer »** *(c'est celui de la planche, cadres 2 · 4 · 18 · 24 à 33)*

| | Variante |
|---|---|
| **A** | aller voir la mer *(inchangé — il est au moodboard)* |
| **B** | t'emmener voir la mer |
| **C** | aller jusqu'à la mer, un jour |

> ⚠ **A est la seule sans risque** : les 12 cadres de la planche l'écrivent.

### 2.3 · L'exemple de « promets-moi » — `app.html:5290`

**Actuel : « m'apprendre à nager » · « venir dimanche » · « me montrer tes photos »**

| | Les trois exemples |
|---|---|
| **A** | m'apprendre à nager · venir dimanche · me montrer tes photos *(inchangés)* |
| **B** | m'apprendre à nager · passer dimanche · me montrer tes photos |
| **C** | de m'apprendre enfin · de venir un dimanche · de me montrer ce que tu caches |

### 2.4 · L'aide sous la phrase — `app.html:5348`

**Actuel : « touche *Je promets* pour changer d'engagement »**

| | Variante |
|---|---|
| **A** | touche **Je promets** pour changer d'engagement *(inchangée)* |
| **B** | **Je promets** se retourne — touche-le |
| **C** | on peut aussi le demander — touche **Je promets** |

### 2.5 · Le libellé du chooser de l'objet — `app.html:5410`

**Actuel : « TU PROMETS QUOI »**

| | Variante |
|---|---|
| **A** | TU PROMETS QUOI *(inchangé)* |
| **B** | LA PAROLE |
| **C** | CE QUE TU DONNES |

### 2.6 · Le libellé du chooser du destinataire — `app.html:5410`

**Actuel : « À QUI »**

| | Variante |
|---|---|
| **A** | À QUI *(inchangé)* |
| **B** | À QUI TU LA DONNES |
| **C** | POUR QUI |

### 2.7 · Le champ du formulaire — `app.html:2565` et `9183-9185`

**Actuel : libellé « Le Promi », invite « ce que tu promets… » · en mode demande, « Le Promi que tu demandes » / « de m'appeler dimanche… »**

| | Variante |
|---|---|
| **A** | Le Promi / ce que tu promets… *(inchangé)* |
| **B** | Le Promi / ta parole, en clair… |
| **C** | Le Promi / dis-le comme tu le penses… |

### 2.8 · Le sous-titre de l'écran — `app.html:9189`

**Actuel : « un Promi, une dalle de plus sur ta Toile » · en demande, « tu demandes un Promi — la dalle apparaîtra chez la personne »**

| | Variante |
|---|---|
| **A** | un Promi, une dalle de plus sur ta Toile *(inchangé)* |
| **B** | une dalle de plus, et elle t'attend |
| **C** | ta Toile s'agrandit d'une dalle |

### 2.9 · Le geste et le bouton — `app.html:2569`

**Actuel : « glisse pour planter → » · « Planter le Promi » · « Demander ce Promi »**

| | Variante |
|---|---|
| **A** | glisse pour planter → / Planter le Promi *(inchangés)* |
| **B** | trace pour planter → / Planter le Promi |
| **C** | glisse, et c'est planté → / Planter le Promi |

> ⚠ Le verbe **planter** ne bouge pas (lexique fermé) ; seule l'invite du geste est ouverte.

---

## 3 · L'ÉCRAN DU CHICHE — audacieux, malin, taquin · complice, jamais séducteur

### 3.1 · L'exemple de la phrase — `app.html:5291` et `5318`

**Actuel : « courir dimanche »** *(un seul, il ne tourne pas — contrairement aux deux autres natures)*

| | Les trois exemples *(je propose d'en faire tourner trois, comme le Promi)* |
|---|---|
| **A** | courir dimanche · te lever avant moi · finir ton assiette |
| **B** | courir dimanche · lâcher ton téléphone un soir · dire oui pour une fois |
| **C** | **courir dimanche** seul *(inchangé)* |

### 3.2 · La pastille vide du défié — `app.html:5304`

**Actuel : « à [qui ?] »**

| | Variante |
|---|---|
| **A** | à **qui ?** *(inchangée)* |
| **B** | à **qui donc ?** |
| **C** | à **qui ose ?** |

### 3.3 · La pastille vide du compagnon — `app.html:5320`

**Actuel : « avec [qui ?] »**

| | Variante |
|---|---|
| **A** | avec **qui ?** *(inchangée)* |
| **B** | avec **qui suit ?** |
| **C** | avec **qui en est ?** |

### 3.4 · Le libellé du chooser du défié — `app.html:5411`

**Actuel : « QUI TU DÉFIES »**

| | Variante |
|---|---|
| **A** | QUI TU DÉFIES *(inchangé)* |
| **B** | À QUI TU LE LANCES |
| **C** | QUI VA VOIR |

### 3.5 · Le libellé du chooser du compagnon — `app.html:5410`

**Actuel : « AVEC QUI »**

| | Variante |
|---|---|
| **A** | AVEC QUI *(inchangé)* |
| **B** | QUI SUIT |
| **C** | QUI EN EST |

### 3.6 · L'aide sous la phrase — corrige **D2** — `app.html:5348`

**Actuel : « touche *Chiche* pour changer d'engagement » — et il ne se passe rien.**

| | Variante |
|---|---|
| **A** | *(rien — l'aide disparaît sur un Chiche)* |
| **B** | un Chiche se lance, il ne se retourne pas |
| **C** | celui-là ne se demande pas — il se lance |

> **D2 ne se répare pas en écrivant mieux** : il faut retirer l'aide, ou l'écrire vraie.
> **A** est la correction minimale ; **B** et **C** gardent une ligne à cet endroit.

### 3.7 · Le sous-titre de l'écran — `app.html:9189` *(aujourd'hui celui du Promi)*

**Actuel : « un Promi, une dalle de plus sur ta Toile » — le Chiche n'en a pas.**

| | Variante |
|---|---|
| **A** | un Chiche, et la dalle attend sa réponse |
| **B** | tu le lances — à lui de voir |
| **C** | une dalle de plus, et un défi avec |

### 3.8 · L'invite du champ — `app.html:5416`

**Actuel : le placeholder reprend l'exemple courant (« courir dimanche »).**

| | Variante — ce qu'on n'ose pas |
|---|---|
| **A** | *(l'exemple courant — inchangé)* |
| **B** | ce que tu n'as jamais osé lui lancer… |
| **C** | vas-y, lance-le… |

> **B est la phrase que Tom a citée.** Elle est plus longue que les autres invites
> (38 caractères contre 16 pour « courir dimanche ») — **sa largeur rendue n'est pas encore
> mesurée** ; je la mesure avant de l'intégrer, le champ fait 342 px.

### 3.9 · Le geste et le bouton — corrige **D3** — `app.html:2569` et `9186`

**Actuel : « glisse pour planter → » · « Planter le Promi » — empruntés au Promi.**

| | Variante |
|---|---|
| **A** | glisse pour lancer → / Lancer le Chiche |
| **B** | trace, et il part → / Lancer le Chiche |
| **C** | glisse pour le lancer → / Lancer le Chiche |

> Les trois disent **lancer**. **D3 est un défaut du lexique**, pas un goût : il se corrige.

---

## 4 · L'ÉCRAN DE LA NUÉE — chaleureuse et collective

### 4.1 · Le nom — `app.html:2572`

**Actuel : libellé « Le nom de la Nuée », invite « Weekend à Marseille… »**

| | Variante |
|---|---|
| **A** | Le nom de la Nuée / Weekend à Marseille… *(inchangé)* |
| **B** | Le nom de la Nuée / Le weekend à Marseille… |
| **C** | Comment on l'appelle / Weekend à Marseille… |

> ⚠ « Weekend » s'écrit sans trait d'union ici et **« Week-end à Lisbonne… »** avec, à
> `app.html:13689`. Une des deux graphies est à choisir — c'est le même champ, ailleurs.

### 4.2 · Les membres — `app.html:2572`

**Actuel : libellé « Avec qui », aide « ils recevront l'invitation au lancement », invite « un prénom… »**

| | Variante |
|---|---|
| **A** | Avec qui / ils recevront l'invitation au lancement *(inchangé)* |
| **B** | Avec qui / on les prévient quand tu lances |
| **C** | Qui en est / ils sauront, au lancement |

### 4.3 · Les premiers Promi — `app.html:2573`

**Actuel : libellé « Les Promi de la Nuée », aide « on peut en planter plusieurs avant de lancer », invite « je vous emmène tous à la mer… »**

| | Variante |
|---|---|
| **A** | Les Promi de la Nuée / on peut en planter plusieurs avant de lancer *(inchangé)* |
| **B** | Les Promi de la Nuée / on en plante autant qu'on veut, puis on lance |
| **C** | Ce qu'on se promet / plusieurs, si le cœur y est |

### 4.4 · Le geste et le bouton — `app.html:2573`

**Actuel : « glisse pour lancer → » · « Lancer la Nuée »**

| | Variante |
|---|---|
| **A** | glisse pour lancer → / Lancer la Nuée *(inchangés)* |
| **B** | trace le trait entier → / Lancer la Nuée |
| **C** | glisse, et tout le monde y est → / Lancer la Nuée |

> **B dit ce qui est vrai** : une Nuée se lance en traçant **le trait entier** (0 → 390, §4 de
> `CLAUDE.md`), là où un Promi et un Chiche n'en tracent que la moitié. C'est la seule des
> trois qui apprend quelque chose.

### 4.5 · Le sous-titre de l'écran — *(la Nuée n'en a pas aujourd'hui)*

| | Variante |
|---|---|
| **A** | une Nuée, et ses dalles sur la Toile de chacun |
| **B** | vous serez plusieurs à tenir |
| **C** | une Toile pour tout le monde |

---

## 5 · LE GARDÉ DE CÔTÉ — il n'a pas d'écran à lui, mais il a des mots

### 5.1 · L'aide du bas — corrige **D1** — `app.html:2577`

**Actuel : « tes brouillons se retrouvent dans l'Index, prêts à être plantés plus tard. »**
**⚠ « brouillons » est un mot banni (§2).**

| | Variante |
|---|---|
| **A** | ce que tu gardes de côté t'attend dans l'Index, prêt à planter. |
| **B** | c'est gardé de côté — l'Index s'en souvient. |
| **C** | l'Index le garde, tu le planteras quand tu voudras. |

### 5.2 · Le libellé de nature d'une fiche — corrige **D1** — `app.html:3690`

**Actuel : « Brouillon ». ⚠ mot banni.**

| | Variante |
|---|---|
| **A** | Gardé de côté |
| **B** | De côté |
| **C** | Gardé |

> ⚠ **A fait 14 caractères** là où « Promi » en fait 5 : la cote de largeur du libellé de
> nature est **écrite en dur** (`{'Promi':54,'Chiche':60,'Nuée':51}`, `app.html:18929`) parce
> que la police n'est pas chargée quand la carte se peint (§8). **B ou C évitent d'y toucher.**

### 5.3 · L'invite et le geste — `app.html:2575` et `2576`

**Actuel : « ce que tu mets de côté… » · « glisse pour mettre de côté → » · « Mettre de côté »**

| | Variante |
|---|---|
| **A** | *(inchangés)* |
| **B** | ce que tu gardes pour plus tard… / glisse pour garder de côté → / Garder de côté |
| **C** | pas encore prêt à être dit… / glisse pour le garder → / Garder de côté |

> **B aligne les trois sur le mot du §2 (« gardé de côté »)** ; A garde « mettre de côté »,
> qui n'est pas banni mais n'est pas le mot du document non plus.

---

## 6 · CE QUE JE RECOMMANDE, SI TU VEUX ALLER VITE

> Une seule ligne par emplacement, celle qui donne le plus de voix pour le moins de risque.

```
1.1 question          A   (elle est au moodboard)
1.2 sous-titres       Promi B · Chiche B · Nuée C
2.1 exemples à soi    A
2.2 exemple à l'autre A   (il est au moodboard)
2.3 exemples demande  A
2.4 aide              B
2.5 chooser objet     A
2.6 chooser à qui     A
2.7 champ             A
2.8 sous-titre        B
2.9 geste             A
3.1 exemples Chiche   B   (trois qui tournent, comme le Promi)
3.2 pastille défié    C
3.3 pastille avec     C
3.4 chooser défié     A
3.5 chooser avec      C
3.6 aide              A   ⚑ répare D2
3.7 sous-titre        B
3.8 invite du champ   B   ⚑ la phrase de Tom
3.9 geste et bouton   A   ⚑ répare D3
4.1 nom               A
4.2 membres           B
4.3 premiers Promi    B
4.4 geste             B   ⚑ il apprend le trait entier
4.5 sous-titre        A
5.1 aide du bas       A   ⚑ répare D1
5.2 libellé de nature B   ⚑ répare D1, sans toucher aux cotes en dur
5.3 invite et geste   B
```

**Rien n'est intégré.** Donne-moi une ligne par emplacement (ou « tout le recommandé »), et je pose le lot.
