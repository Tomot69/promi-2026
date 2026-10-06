# SPEC-DONNEES — le modèle de données de Promi, tel qu'il existe dans le prototype

> Dossier `portage/` · document 1 sur 10 · relevé le 6 octobre 2026 sur `app.html` (état de travail v134, 38 340 lignes) et
> `promi-moteur.js` (8 034 lignes). **Lecture et extraction seulement : rien n'est inventé.**
> Le schéma formel est `SPEC-DONNEES.schema.json` (JSON Schema 2020-12) ; ce fichier-ci l'explique.
>
> **Comment lire :**
> - chaque affirmation porte sa source — `app.html:ligne`, un nom de bloc `lot-…`, ou un document + section ;
> - **« ⚠ TROU »** : ce que le prototype ne dit pas, ou dit de deux façons. La liste complète est au §13 ;
> - **« ATTEND FIREBASE »** : ce qui est local aujourd'hui et devra être partagé ou tenu par un serveur. Résumé au §12 ;
> - **« (ancien) »** : un champ ou un chemin encore présent dans le code, écrit par l'interface d'origine, que les écrans d'aujourd'hui
>   ne montrent plus forcément. Il est listé parce qu'il est dans la sauvegarde ; **le portage ne le reprend pas sans décision de Tom**.
>
> **Lexique (CLAUDE.md §2)** : le code dit `nuee` / `NUE` / `curNuee`, l'écran dit **Cercle** ; le code dit `isPremium` / `.premium` /
> `ouvreCercle`, l'écran dit **Ma Parole !** ; le code dit `draft`, on dit **gardé de côté** ; le code dit `status:'rate'`, l'écran dit
> **« à tenir »**. Le code dit `promises` : ce sont les **paroles** (Promi et Chiche).

---

## 0. Vue d'ensemble — où vivent les données

**Une seule source de vérité : le tableau `promises` (et la table `NUE`)** — C-049, `app.html:37760` ; `portage/A-INTEGRER.md`.
`promises` est un `let` de module, **pas** une propriété de `window` (`app.html:2925`, piège noté `app.html:25083`).
`window._paroles = {signe, abonne, publie}` (`app.html:37774`) : `signe()` rend une signature de
`id, status, title, nuee, draft, req, who, from, due, chiche, pending` de chaque parole + les couples `clé=nom` de `NUE` (`app.html:37766`) ;
l'Index, le Fil, l'Aura et le fil d'un Cercle s'y abonnent et comparent avant d'agir. En SwiftUI : un seul modèle observable.

**La persistance est entièrement locale (`localStorage`)** — aucun serveur, aucun compte réel.

| Clé `localStorage` | Contenu | Écrit par | Source |
|---|---|---|---|
| `promi_state` | `{v:1, promises, NUE, NUEEMEM, NUEDALLE, PEOPLE, FEED, feedReacted, shareHidden, state:{mood,structure,sort,labels}, nid, fid, notifOn}` | `saveState()` — toutes les 1,5 s, à `pagehide`, `beforeunload`, `visibilitychange` ; `queueSave()` (400 ms) | `app.html:7644`, `7647`, `7650` |
| `promi_studio` | `{m, p, h, libre, acquis}` — monde, palette, teinte, « choisi gratuit », mondes acquis | `lot-V71-REOUVERTURE` (à chaque `setTheme`/`setPalette`/`setHue`/`setPremium`) | `app.html:36816–36846` |
| `promi_monde` | la clé du monde courant | `Toile.setTheme` | `promi-moteur.js` (dans `setTheme`) |
| `promi_theme` | `'light'` ou autre (sombre) — le CHOIX de thème | `setTheme(t)` de l'app | `app.html:6717` |
| `promi_zzz` | `'1'`/`'0'` — le Zzz. **COUPÉ depuis v120** (`COUPE=true`) | `lot-V118-ZZZ` | `app.html:36941–37055` ; CLAUDE.md bloc v120 |
| `promi_nb`, `promi_nb_j` | noir et blanc du Studio : actif (`'1'`), jauge 0–1 (défaut 0,3) | `window._promiNB` | `app.html:33813–33830` |
| `promi_lang` | langue, défaut `'fr'` | réglage Langue | `app.html:3237–3248` |
| `promi_onb` | `'1'` = onboarding fait | `terminer()` / `obFinish` | `app.html:8212`, `36541` |
| `promi_debut` | horodatage (ms) de la fin du premier onboarding | `terminer()` | `app.html:36541` |
| `promi_prenom` | le prénom saisi à l'onboarding → `USER.name` | onboarding | `app.html:36316`, `36388` |
| `promi_graine` | la graine du visage de l'utilisateur (entier) | `_grainePropre()` | `app.html:3844–3850` |
| `promi_compte` | `'demande-apple'`, `'demande-google'`, `'plus-tard'` ; `'fait…'` est LU mais jamais écrit | panneau « Garder ta Toile » | `app.html:36525–36526`, `36587` |
| `promi_rappel_n`, `_p`, `_t`, `_vu` | relances du panneau « Garder ta Toile » : nombre de refus, nombre de paroles et date au dernier refus | onboarding / compte | `app.html:36649–36661` |
| `promi_notifs2` | `{datees, lair, heure, refus, lairDepuis?, lairDernier?}` | `lot-V109-NOTIFS` | `app.html:37279–37285` |
| `promi_notifs_log` | journal des envois `{cle: horodatage, _jour}` | `tick()` | `app.html:37331–37336` |
| `promi_notifs` | `'1'`/`'0'` (ancien) — relu une fois pour amorcer `datees` | Réglages (ancien) | `app.html:35876–35881`, `37283` |
| `promi_murs` | `{n, t, der, decouvert}` — compteur des murs de Ma Parole ! | `lot-V104-MURS` | `app.html:37137`, `37151` |
| `promi_dessins_cercle` | `{cléDeCercle: dessin}` | `lot-V132-DESSIN` | `app.html:38065–38066` |
| `promi_pelote_vue` | `{s, k, c, t, p}` — sol et corps tirés à la dernière ouverture de l'Aura | Pelote | `app.html:29786–29799` |
| `promi_pelote_ordre` | `[id…]` — ordre d'apparition des paroles tenues | `ordreTenus()` | `app.html:29475–29483` |
| `promi_pelote_palier`, `_gl`, `_vus`, `_traces` | palier de densité, carte graphique vue, compte de tenues vues, caresses | Pelote | `app.html:30329`, `30724`, `30869`, `30969`, `30990` |
| `promi_studio_glisse` | `'1'` = l'invite de glissement du Studio a été vue | Studio | `app.html:22176–22185` |
| `promi_sig`, `promi_sigdemo` | mode signature du mot-marque (ancien) | `#brandBtn` | `app.html:12656–12672`, `32885` |
| `promi_ex_<t>`, `promi_ex_sac_<t>` | compteur et sac de tirage des phrases suggérées de la page + | `lot-EXEMPLES` | `app.html:36032–36052` |
| `promi_fresh` | `'1'` = repartir vide au prochain chargement | réinitialisation | `app.html:2966` |
| `promi_t` | clé d'essai (test d'écriture) | `storageWorks()` | `app.html:7645` |

**Effacement** : « tout effacer » et « supprimer le compte » font `localStorage.clear()` puis rechargent (`app.html:3282`, `35829`, `35903`) ;
`#resetData` retire `promi_state` et vide les tables en mémoire (`app.html:3301`).

**Chargement** : `loadState()` (`app.html:7648`) n'accepte qu'une sauvegarde `v===1` avec un tableau `promises` ; une sauvegarde VIDE ne vaut
que si `promi_onb==='1'` (v94) — sinon c'est le jeu de démonstration (`app.html:2925`, puis le « jeu de la planche », `app.html:≈21200–21345`).
Après lecture : `_figeMondesManquants()` et `_figeDallesManquantes()` (idempotentes, `app.html:2940–2965`).

> **⚠ Ce que `saveState` ne garde PAS** (donc perdu au rechargement — voir §13) : `isPremium`, `USER.photo`, le pinceau d'un Cercle (`NUEE`),
> `NUETHEME`, `NUENOTE`, `NUEFILES`, `NUECREATOR`, `NUEHT`, `NUEORD`.

---

## 1. La parole — Promi et Chiche (un élément de `promises`)

**Il n'y a qu'UNE structure** : un Chiche est une parole qui porte `chiche:true` ; un gardé de côté est une parole qui porte `draft:true` ;
une demande est une parole qui porte `req:true`. Le prototype n'a pas de champ « nature » : elle se déduit —
`chiche ? 'chiche' : 'promi'` (`app.html:38075`, `natureDe`).

**La fabrique unique** — `app.html:2924` :
```js
const P=(t,w,d,i,s,n,fr)=>({id:nid++,title:t,who:w,due:d,intensity:i,status:s,nuee:n,from:fr||'moi',
                            recur:null,remind:null,x:0,y:0,tx:0,ty:0,monde:mondeDuJour()});
```
« HUIT sites plantent un Promi, mais tous passent par CETTE fabrique » (`app.html:2913–2919`).

### 1.1 Champs posés par la fabrique

| Champ | Type | Valeurs · défaut | Qui l'écrit |
|---|---|---|---|
| `id` | entier | `nid++`, `nid` part de 100 et est sauvegardé (`app.html:2912`, `7644`). ⚠ Les ids du jeu de démonstration changent d'un chargement à l'autre (CLAUDE.md §4, chantier 71) : **jamais une clé stable**. | `P()` |
| `title` | chaîne | la phrase de la parole | `P()` ; renommage `#dRenameOk` (`app.html:3808`, `9271`) |
| `who` | chaîne | **à qui** : `'moi'` / `'Moi'` (soi), un prénom, plusieurs prénoms joints par `', '` (`app.html:32663`), ou `'le groupe'` (parole d'un Cercle à membres, `app.html:3196`). Défaut `'moi'`. | `P()` ; Peaufiner « À QUI » (`_gensFiche`, `app.html:32651–32664`) ; `#dWhoInput` (ancien, `app.html:3311`) |
| `due` | nombre ou `null` | **un nombre de JOURS**, relatif (1 demain · 5 · 14 · 30) ; `null` = « un jour » ou « en l'air ». Voir §1.4. | `P()` ; liste d'échéance (`app.html:16194–16199`) ; reports (`app.html:3044`, `6922`, `3791`) |
| `intensity` | entier 1–3 | importance : 1 `light`, 2 `normal` (défaut), 3 `high` (`app.html:3192`). Réglage de Ma Parole ! (ETAT §6). | `P()` ; `#segImp` (`app.html:3792`) |
| `status` | énuméré | `'encours'` · `'tenu'` · `'rate'` — voir §1.5 | voir transitions |
| `nuee` | chaîne, `null` ou `undefined` | la clé du Cercle qui porte la parole (une clé de `NUE`) ; absent = hors Cercle. `'soi'` est une clé réservée (« Moi-même », `app.html:2968`). | `P()` ; `#dNueeChips` (`app.html:3754`) ; dissolution (`app.html:3662`, `9248`) |
| `from` | chaîne | **qui promet** : `'moi'` (défaut) ou le prénom de l'autre (une parole qu'on ME fait : `from:'Rachel', who:'moi'`, `app.html:21292`) | `P()` ; relever un Chiche reçu (`app.html:6914`) |
| `recur` | `null` ou énuméré | `'daily'` · `'weekly'` · `'monthly'` (`app.html:3665`, `3765`). Défaut `null`. Ma Parole ! (ETAT §6). | `#segRecur` |
| `remind` | `null` ou `'HH:MM'` | (ancien) heure de rappel par parole, défaut `'07:00'` à l'activation (`app.html:3766`). Remplacé dans les faits par `lot-V109-NOTIFS` (§9). | `#remindRow` |
| `x`, `y`, `tx`, `ty` | nombres | (ancien) position dans l'ancien calque SVG. « Une fonction qui écrit dans un calque que plus personne n'affiche » (CLAUDE.md §8, Arranger). **Ne pas porter.** | plantation |
| `monde` | objet `{m, p, h}` | le monde de PLANTATION, figé : `m` clé de monde, `p` clé de palette, `h` teinte (`Toile.mondeCourant()`, `promi-moteur.js:7846`). Repli avant que la Toile existe : `{m: state.structure‖'encre', p:'signal', h:0}` (`app.html:2920–2923`). Depuis v34, seule l'Aura et « La dalle d'origine » le lisent (CLAUDE.md §3 bloc v34). | `P()` ; `_figeMondesManquants` |

### 1.2 Champs ajoutés après la fabrique

| Champ | Type | Sens · valeurs | Qui l'écrit |
|---|---|---|---|
| `dalle` | `{ci, lit, rgb?, choisi?}` | la COULEUR figée de la dalle : `ci` rang 0–3 dans la palette, `lit` nuance, `rgb` `[r,g,b]` = code libre, `choisi:1` = choisie à la main. | `_dalleFigee(vivant)` à `Toile.addPromi` (`promi-moteur.js:6105–6109`) ; repli `_dalleDeCle(p)` = FNV-1a de `title+'|'+who`, `{ci:h%4, lit:0}` (`app.html:2954–2964`) ; réglage COULEUR, `lot-CERCLE-COULEUR` (`app.html:33086–33097`, `33139–33144`) |
| `dalleOrigine` | booléen | `true` = la dalle de cette parole se peint dans `monde` (plantation) partout où elle paraît seule ; défaut absent = elle suit le Studio. | menu du bouton photo (`lot-V117-PHOTO-MENU`, `app.html:37509`) |
| `photo` | chaîne (data-URL) ou `null` | l'image importée ; elle remplace la dalle dans la bande. Voir §6. | `FileReader` (`app.html:20123–20126`) ; `(_phrase).photo` suit à la plantation (`app.html:20271–20278`) ; « Retirer la photo » |
| `dessin` | objet dessin | voir §5. Absent = pas de dessin (`delete`). | `lot-V132-DESSIN` (`app.html:38069`, `38317`) |
| `trait` | chaîne | le PINCEAU du trait : un des douze noms (§1.6). Absent = `'Plein'`. | marqué à la plantation (`app.html:25079–25093`) ; Peaufiner « LE TRAIT » (`_pinceauCible`, `app.html:25374`) |
| `trace` | tableau `[{x,y}…]` | les points du geste qui a tenu la parole, en coordonnées du canevas du geste. | fin du geste (`app.html:4768`) |
| `note` | chaîne | le mot joint à la parole | page + `#fNote` (`app.html:3192`), `#dNote` (`app.html:3312`), gardé de côté (`app.html:13612`) |
| `comments` | tableau `[{t, d, by}]` | commentaires : texte, date ISO, auteur (`USER.name` ou `'moi'`) | `app.html:3315–3317` |
| `files` | tableau `[{name, type, size, by}]` | pièces jointes (noms seulement dans le prototype) | page + (`app.html:3195`), fiche (`app.html:9267`) ; forme : `app.html:9120` |
| `relances` | entier | nombre de relances envoyées | `#actRelance` (`app.html:3313`) |
| `urg` | entier | (ancien, **MASQUÉ PAR DÉCISION** — « Urgent supprimé », CLAUDE.md §9 ; « urgent » est un terme banni §2). Encore écrit à la plantation (`app.html:3192`). **Ne pas porter.** | — |
| `dueISO` | chaîne `AAAA-MM-JJ…` | la date précise choisie (« une date précise… ») | page + (`window._csDueISO`, `app.html:3192`) |
| `enLair` | booléen | « en l'air » : `due=null` ET `enLair=true` | page + (`app.html:3192`), liste d'échéance (`app.html:16197`) |
| `dueChoisi` | booléen | `true` dès qu'un choix d'échéance a été fait sur la fiche (sert à distinguer « un jour » choisi de « rien choisi ») | `app.html:16198` |
| `aussi` | tableau de prénoms | autres destinataires cochés à la page + (`csWhoList('whoChips')`) — une seule écriture, aucune lecture trouvée | `app.html:3192` |
| `phraseSens` | énuméré | le verbe de la phrase de la page + : `'faire'` (je promets) · `'demander'` (je demande à l'autre) · `'chiche'` | `app.html:3192`, `6914`, `13611` |
| `chiche` | booléen | la parole est un **Chiche** | `app.html:3194`, `6914` |
| `chicheEtat` | énuméré | `'lance'` · `'releve'` — voir §2 | `app.html:3194` (`'lance'`) ; `'releve'` : **données de démonstration seulement** (`app.html:21239`, `21268`) |
| `avec` | chaîne | **avec qui** on relève le Chiche (prénoms joints par `', '`) ; `chiche && avec` ⇒ mode « duo » (`app.html:18994`) | page + (`app.html:3194`), Peaufiner « AVEC » (`app.html:32662`) |
| `req` | booléen | la parole est une **demande** en attente (pas de dalle tant qu'elle n'est pas acceptée) | `app.html:3193`, `4079` |
| `reqEtat` | énuméré | `'attente'` · `'acceptee'` · `'expiree'` — §1.7 | `app.html:3193`, `4079`, `4108` |
| `reqLe`, `acceptLe` | horodatages ms | date de la demande, date de l'acceptation | `app.html:3193`, `4079` |
| `pending` | booléen | une parole qu'on me fait (`from≠'moi'`, `who==='moi'`) et que je n'ai pas encore vue/acceptée dans le Fil | chargement du jeu (`app.html:2932`) ; remis à `false` par `feedKeep`, `_fpost` (`app.html:6906`, `6922`) |
| `accepted` | booléen | posé à `true` avec `pending=false` — aucune lecture trouvée hors CSS | `app.html:6906`, `6922` |
| `draft` | booléen | **gardé de côté** — §4 | §4 |
| `dk` | énuméré | nature du gardé de côté : `'solo'` · `'innuee'` · `'nuee'` | `app.html:3327`, `13603`, `13610` |
| `draftKind` | énuméré | (ancien) même chose, écrit par `#draftKindSeg` : `'solo'` · `'innuee'` · `'nuee'` | `app.html:9252`, `9259` |
| `kindDraft` | chaîne | (ancien) troisième nom du même réglage | `app.html:6137` |
| `nueeMembers` | tableau de prénoms | les membres d'un Cercle gardé de côté (`dk:'nuee'`) | `app.html:13604` |
| `rappel` | booléen | réponse à « Je te le rappelle ? » : `true` (oui) · `false` (pas besoin) ; absent = pas demandé | `lot-V109-NOTIFS` (`app.html:37363–37364`) |
| `rap` | `{due, base, vu}` | ancrage du rappel : `base` = minuit du jour où la parole a été vue avec cette `due`, `vu` = horodatage | `jourJ`, `vuLe` (`app.html:37309–37312`) |
| `rapLair` | horodatage ms | dernière relance « en l'air » envoyée pour cette parole | `app.html:37337` |
| `leJour` | chaîne | (démonstration) le mot du temps lu dans les cadres : `'12 mars'`, `'depuis le 4 avril'`… | jeu de la planche (`app.html:21331–21334`) |
| `ht` | nombre | (démonstration) « hauteur de trait figée à la plantation » (§2.5 de PROMI-SPECIFICATIONS), relevée dans les cadres : 201,8 à 310,9 | jeu de la planche (`app.html:21336–21338`) |

> **⚠ TROU T1** — `ht` (« elle appartient au PROMI… figée à la plantation », `app.html:21316`) n'est posée QUE pour six paroles du jeu de
> démonstration ; aucune plantation réelle ne l'écrit. La règle d'engendrement pour une parole neuve n'a pas été trouvée
> (cherché : `\.ht\s*=`, `NUEHT`). À demander — elle relève aussi de la spec des écrans (Index).
>
> **⚠ TROU T2** — **aucune date réelle** sur une parole : ni date de plantation, ni date de tenue (cherché : `tenuLe`, `keptAt`, `cree`,
> `created`). « L'app ne garde aucune date : elle n'a que des échéances en jours » (`app.html:21321`). `leJour` est un mot recopié des cadres.
> L'ordre « chronologique » des tenues de l'Aura (C-052) vient de `promi_pelote_ordre` : ordre d'APPARITION, à défaut tri par `id`
> (`app.html:29475–29483`). Le portage doit dater (plantation, tenue) — décision à prendre, car la ligne d'état (« TENUE · 12 MARS »,
> « EN COURS · DEPUIS LE 4 AVRIL ») en a besoin.

### 1.3 Champs dérivés (jamais stockés)

- **nature** : `chiche ? 'chiche' : 'promi'` (`app.html:38075`).
- **sens** : « ce que je tiens » = `!from || from==='moi'` ; « ce qu'on me tient » = `from!=='moi'` (`app.html:31076`, `37313`).
- **« mienne » pour un rappel** : `!draft && !req && status==='encours' && (!from || from==='moi')` (`app.html:37313`).
- **duo** (« TENU À DEUX ») : `status==='tenu' && chiche && avec` (`app.html:18994`).
- **personnes connues** : dérivées des paroles — §3.

### 1.4 L'échéance — quatre champs pour une seule idée

Liste unique (`ECHEANCE`, `app.html:16163–16171`, décision Tom S3/Q28) :

| Mot affiché | `due` | `enLair` | `dueISO` |
|---|---|---|---|
| un jour | `null` | `false` | — |
| en l'air | `null` | `true` | — |
| demain | 1 | `false` | — |
| 5 jours | 5 | `false` | — |
| 2 semaines | 14 | `false` | — |
| ce mois-ci | 30 | `false` | — |
| une date précise… | (inchangé) | — | la date |

« "un jour" et "en l'air" valent toutes deux due = null mais restent DEUX valeurs distinctes… Jamais fusionnées » (`app.html:16159–16160`).
Choisir une échéance chiffrée sur la fiche remet `status='encours'` (`app.html:16199`).
⚠ La fabrique des gardés de côté traduit « un jour » par **30** (`quandToDue`, `app.html:13598`) — contradiction avec `null`.

> **⚠ TROU T3** — `due` est un **nombre de jours sans date de référence, et rien ne le décrémente** (cherché : `due--`, `due-=`).
> `echeancesDepassees()` bascule `encours → rate` quand `due < 0` (`app.html:4090–4100`), ce qui ne peut arriver que par les données de
> démonstration. Seul le lot des notifications reconstruit un jour J (`rap.base + due × 24 h`, `app.html:37309`). **En Swift : stocker une
> DATE d'échéance** (plus « un jour » / « en l'air »), et dériver les mots ; à faire valider par Tom.

### 1.5 États d'une parole et transitions

**`status`** : `'encours'` (en cours) · `'tenu'` (tenu) · `'rate'` (affiché **« à tenir »** — `app.html:2678`, `3764`).
Il n'existe pas d'état « manqué » à l'écran : « un Promi dont l'échéance est passée bascule seul en "à tenir" : personne ne devrait avoir à le
déclarer manqué à la main » (`app.html:4088–4089`).
⚠ `p.status!=='kept'` est testé une fois (`app.html:33784`) mais `'kept'` n'est jamais écrit dans `status` (c'est un type d'événement du Fil).

| De | Vers | Déclencheur (geste · bouton · fonction) | Effets liés | Source |
|---|---|---|---|---|
| — | `encours` | **Planter** : tracer le trait de la page + → `#addPromi` (fabrique `P(t,w,due,imp,'encours',selNuee)`), UNE parole par destinataire choisi | `Toile.addPromi(id)` (ou `addNuee`+`addMember` si Cercle) ; `feedAdd('added',…)` ; `trait` marqué ; photo et dessin du brouillon suivent ; « Je te le rappelle ? » si datée | `app.html:3192–3195`, `25079`, `20271`, `38313–38317`, `37372–37377` |
| — | `encours` | Premier Promi de l'onboarding (`P(titre,'Moi',7,2,'encours',undefined,'moi')`) | `Toile.sync([id])` | `app.html:8053`, `36457` |
| — | `encours` | Créer un Cercle : son premier Promi (`#nFirst` ou « premier Promi », `due 7`) | §7 | `app.html:3196` |
| `encours` / `rate` | `tenu` | **Tracer le trait de la fiche** (`#tenirZone`) : validé si le doigt passe les 2/3 de la largeur, OU geste lent avec > 6 points, OU > 50 % de la largeur parcourue ; la fin du geste garde `cur.trace` puis **clique `#segStatus button[data-st="tenu"]`** | `draft=false` ; `regenRecur` si `recur` ; `feedAdd('kept','Tu as tenu « … »')` ; `syncAll()` ; l'instant de célébration (`_instantTenue`, armé en capture) | `app.html:4747–4774`, `3764`, `19956–19964` |
| `encours` / `rate` | `tenu` | Carte de la Toile, bouton `#ccKeep` (ancien) | idem | `app.html:3042` |
| `encours` (reçue, `pending`) | `tenu` | Fil : « TENIR » sur un bandeau (`feedKeep(fid)`) | `pending=false`, `accepted=true`, `draft=false` ; l'événement devient `kept` | `app.html:6906` |
| tout | `encours` / `rate` / `tenu` | (ancien) sélecteur d'état `#segStatus` (trois boutons « Tenue · En cours · À tenir ») — masqué sur un gardé de côté et sur un Cercle (`app.html:861`, `11080`) | `rate` → `feedAdd('missed','« … » est à tenir')` | `app.html:2678`, `3764` |
| `encours` | `rate` | **Automatique** : `echeancesDepassees()` au chargement (+3,4 s) quand `due < 0`, hors `draft` et `req` | `saveState`, `syncAll` | `app.html:4090–4101` |
| `rate` / autre | `encours` | Choisir une échéance chiffrée sur la fiche (Peaufiner, liste d'échéance) | `due`, `enLair`, `dueChoisi` | `app.html:16194–16199` |
| `tenu` (avec `recur`) | + une parole neuve `encours` | `regenRecur(p)` : même titre, même `who`, `nuee`, `from`, `recur` ; `due` = 1 / 7 / 30 | `feedAdd('added','↻ « … » régénérée')` | `app.html:3665` |
| tout | supprimée | Peaufiner « SUPPRIMER CE PROMI / CE CHICHE » → confirmation (« Supprimer » / « Garder ») → `_v16SupprimerPromi` ; **annulable** (« Promi supprimé », `restaure(instantané)`) | `Toile.sync(ids non gardés)` : la dalle part avec l'animation de son monde | `app.html:35813–35824`, `35791–35811`, `35905` |

> **⚠ TROU T4** — le chemin **`tenu → encours`** (défaire une parole tenue) n'existe que par l'ancien `#segStatus` ; aucune décision écrite
> ne dit s'il doit exister. Non porté tant que Tom ne tranche pas.
>
> **⚠ TROU T5** — **la moitié de trait** : la règle produit dit qu'un Promi fait à quelqu'un se trace à moitié et que « l'autre trace la
> sienne » (CLAUDE.md §4, « UNE NUÉE SE LANCE EN TRAÇANT LE TRAIT ENTIER »). Dans les données, **aucun champ ne dit quelle moitié est
> tracée ni par qui** : `status` passe à `tenu` d'un seul geste local. La moitié de l'autre n'existe que comme événement de démonstration du
> Fil (`type:'moitie'`, `app.html:21381`). **ATTEND FIREBASE** — à modéliser (ex. deux marques, une par personne) avec Tom.

### 1.6 Le pinceau du trait (`trait`)

Douze noms (`window._PINCEAU_META`, `app.html:24814`) — **libres** : `Plein` · `Coulé` · `Peigné` · `Sec` ; **« à 0,50 € »** : `Tressé` ·
`Frangé` · `Doublé` · `Fendu` · `Cranté` · `Vrillé` · `Semé` · `Perlé`. Les tracés sont des données (`_PINCEAU_TRACES`, `app.html:24813`).
Où vit le choix (`_pinceauCible`, `app.html:25338–25382`) : une parole plantée → `p.trait` ; un Cercle → table `NUEE[clé]` ;
un gardé de côté repris → `p.trait` de ce gardé ; une création en cours → `window._ppPinceau`.

> **⚠ TROU T6** — huit pinceaux sont libellés « — 0,50 € » (`app.html:25406`) mais **aucun état d'achat de pinceau n'existe** (cherché :
> `pinceauAcquis`, `_pinceauLibre`, `acquis` hors mondes). ETAT §6 ne cite pas les pinceaux dans l'offre. À trancher avant StoreKit.
>
> **⚠ TROU T7** — le pinceau d'un Cercle vit dans une variable locale `NUEE` (`app.html:25342`), **jamais sauvegardée**.
>
> **À INTÉGRER (C-045, `A-INTEGRER.md`)** — le trait de validation personnalisé est un CONCEPT (rien n'est construit) : s'il est retenu, le
> chemin sera une **donnée de la parole** (liste de points lissés), jamais une image — `TRAIT-PERSONNALISE-CONCEPT.md`.

### 1.7 La demande (`phraseSens:'demander'`)

« attente → acceptee (la dalle apparaît) | expiree (silence, 1 mois). Il n'y a pas d'état "refusee" : refuser, c'est ne rien faire »
(`app.html:4070–4073`).

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| — | `req:true, reqEtat:'attente', reqLe:now` | Planter avec le verbe « demander » | `app.html:3193` |
| `attente` | `reqEtat:'acceptee', req:false, acceptLe:now` | `demandeAccepter(id)` → `Toile.addPromi`, `feedAdd('accept','« … » est promis')` | `app.html:4075–4086` |
| `attente` | `expiree` | `demandesExpirer()` après `PROMI_EXPIRE` = 30 jours ; aucune notification | `app.html:4074`, `4103–4112` |

> **⚠ TROU T8** — **qui accepte ?** Dans le prototype c'est l'utilisateur lui-même qui appelle `demandeAccepter` (c'est l'AUTRE qui devrait).
> **ATTEND FIREBASE.** Le bouton exact qui l'appelle n'a pas été relevé (cherché : la définition seule).

---

## 2. Le Chiche — ce qui lui est propre

Un Chiche est une parole (`§1`) avec `chiche:true`, `phraseSens:'chiche'`, `who` = **qui je défie**, `avec` = **avec qui** (facultatif).

**`chicheEtat`** : `'lance'` · `'releve'`. « C'est `chicheEtat` qui dit s'il est relevé, pas l'état de la parole… Relever un chiche, c'est
l'accepter — c'est un fait du Chiche » (`app.html:15527–15531`). Libellés : `CHICHE LANCÉ` / `CHICHE RELEVÉ`
(relevé si `chicheEtat==='releve'` OU `status` vaut `tenu` ou `rate`, `app.html:15532–15534`).

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| — | `chiche:true, chicheEtat:'lance', status:'encours'` | Planter depuis la page + « Un Chiche » (tracer pour lancer) ; `avec` recopié de `_phrase.avec` | `app.html:3194` |
| (événement `chiche_recu` du Fil) | **une parole NEUVE** `chiche:true, phraseSens:'chiche', from:<défieur>, who:<défieur>, due:7, status:'encours'` | Fil : « RELEVER » sur un Chiche reçu — le titre et le défieur sont **lus dans le texte de l'événement** | `app.html:6908–6916` |
| `lance` | `releve` | **⚠ TROU T9** : aucune fonction ne l'écrit sur un Chiche que j'ai lancé ; seules les données de démonstration portent `'releve'` (`app.html:21239`, `21268`). C'est l'autre qui relève → **ATTEND FIREBASE**. | — |
| `encours`/`rate` | `tenu` (« TENU À DEUX » si `avec`) | le trait de la fiche, comme un Promi (§1.5) | `app.html:18994` |

États d'écran lus dans `app.html:14475–14497` : lancé (« elle tracera sa part si elle ose »), à tenir / relevé (« trace pour tenir »),
tenu à deux (mode `duo`).

---

## 3. La personne

**Il n'existe PAS d'entité « personne » : une personne est un PRÉNOM (une chaîne).** L'identité repose sur l'égalité de chaînes
(`p.who===name || p.from===name || p.avec===name`, `app.html:31076`, `31161`).

| Donnée | Forme | Source |
|---|---|---|
| `PEOPLE` | tableau de prénoms ; défaut de démonstration `['Rachel','Adrien','Nico','Léa','Maman','Mimi']` ; sauvegardé ; vidé par l'onboarding | `app.html:2970`, `7644`, `8166` |
| `peopleList()` | `PEOPLE` ∪ les `who` et `from` des paroles ∪ les membres de tous les Cercles | `app.html:3458` |
| `connus()` | les `who`, `from`, `avec` des paroles (les plus récentes d'abord) puis `peopleList()` ; « moi », « le groupe », « tout le monde » exclus | `app.html:32424–32434` |
| Valeurs réservées | `'moi'`/`'Moi'` (soi), `'le groupe'`, `'tout le monde'`, `'qui ?'`, `'personne'` (filtrées par `_gensListe`) | `app.html:32435–32436` |
| Le visage | un avatar engendré de la graine ; aucune photo ni graine stockée par personne | CLAUDE.md §3 bloc 21 sept. (`_BPAL`) |

**Ajouter quelqu'un** (« + ajouter quelqu'un », `lot-GENS`, `app.html:32479–32497`) : un champ « un prénom… », jusqu'à quatre suggestions
filtrées dans `connus()` ; valider ajoute le prénom **à la parole en cours** (`who`, `avec`) ou aux membres du Cercle.
⚠ Rien n'ajoute ce prénom à `PEOPLE` : une personne « existe » parce qu'une parole ou un Cercle la cite.

**L'utilisateur** — `var USER={name:'Tom', photo:null, seed:_grainePropre()}` (`app.html:2909`) :

| Champ | Type | Persistance | Écrit par |
|---|---|---|---|
| `name` | chaîne | `promi_prenom` | onboarding (`app.html:36388`, `8046`) |
| `photo` | data-URL ou `null` | **aucune** (⚠ TROU T10) | Réglages : avatar → fichier (`app.html:3131`) ; « retirer » → `null` + nouvelle graine, annulable (`app.html:3132`, `35907–35909`) |
| `seed` | entier | `promi_graine` — « la graine sauvegardée d'abord ; sinon dérivée du nom (FNV-1a mod 10⁹) ; et on l'enregistre » | `_grainePropre` (`app.html:3844–3850`) |

**Le compte** : le panneau « Garder ta Toile » propose Apple / Google / « Plus tard » ; il écrit `promi_compte` et appelle
`window.promiConnexion(k)` **qui n'est définie nulle part** (`app.html:36509`, `36525`). **ATTEND FIREBASE** : compte, identifiant de
personne, lien prénom ↔ compte réel, photo de profil partagée, `promiDeconnexion` (QUESTIONS.md l. 7387), la « ligne du membre » des Réglages (Q343).

---

## 4. Le gardé de côté

Une parole avec **`draft:true`** : « rien n'est promis ». Il n'a **pas de matière** mais garde le champ de sa nature (CLAUDE.md §3, « un champ
blanc n'existe jamais »). Il est exclu de la Toile vivante : partout `Toile.sync(promises.filter(p => !p.draft)…)` (`app.html:3196`, `35799`).
⚠ Mais les fabriques appellent aussi `Toile.addPromi(np.id)` pour lui (`app.html:13616`, `3327` : « le brouillon apparaît aussi sur la
Toile (dalle distincte) ») — **⚠ TROU T11** : les deux chemins se contredisent ; l'état à l'écran n'a pas été vérifié (pas de navigateur).

Champs propres : `dk` (`'solo'` hors Cercle · `'innuee'` dans un Cercle existant · `'nuee'` un Cercle entier gardé de côté),
`nueeMembers` (si `dk:'nuee'`), `phraseSens`, `note`, `trait`.

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| — | `draft:true, status:'encours'` | Page + : toucher **« garder de côté »** (`.garde-cote`, `data-gc`) → `_gardeCote(kind)` : titre et personne de la phrase (`_phrase.titre`, `_phrase.qui`), `due = quandToDue(quand)`, `dk`, `phraseSens`, `note` ; `feedAdd('added','Tu as gardé « … » de côté')` ; toast « gardé de côté — dans l'Index » | `app.html:13599–13623`, `13663` ; v119/v121 Q370 |
| — | `draft:true` | (ancien) formulaire `#addDraft` : `P(t,w,30,2,'encours')`, `dk = dfKind()` | `app.html:3327` |
| `draft:true` | page + rouverte (reprise) | Ouvrir un gardé de côté → `reprendreBrouillon(p)` : pose `window._ppGarde=true`, `_brouillonRepris=p.id`, recharge `_phrase` (ou `nName` + `newNueeMembers` pour un Cercle) | `app.html:13625–13661` |
| reprise | **parole plantée** (`draft` absent) + l'ancien gardé **supprimé** | Tracer le trait de la page + reprise → `#addPromi` / `#addNuee` plante une parole NEUVE, puis (120 ms) retire `promises[rid]` et `Toile.sync` | `app.html:13674–13683` |
| `draft:true` | `draft:false` (planté sur place) | (ancien) bouton `#actPlanter` de la fiche → `Toile.addPromi(cur.id)`, toast « Promi planté sur la Toile » | `app.html:3798–3807` |
| `draft` ↔ `!draft` | bascule | (ancien) `#actDraft` | `app.html:3810` |
| `draft:true` | supprimé | la suppression d'une parole (§1.5) | `app.html:35813` |

⚠ Planter par reprise **crée un nouvel `id`** : `dalle`, `monde`, `photo`, `dessin`, `trait` du gardé ne sont pas recopiés par ce chemin
(le pinceau est relu via `_ppGardeP`, `app.html:25378`). **⚠ TROU T12** : ce qui doit survivre à la conversion n'est écrit nulle part.

---

## 5. Le dessin

Source : `lot-V132-DESSIN` (`app.html:38022–38330`), CLAUDE.md blocs v132/v133, `A-INTEGRER.md` (C-042, v133).
**Un dessin est une LISTE DE TRAITS, jamais une image.**

```js
{ v:1, w:390, h:742,            // surface en points ; h = surfH() = 844 − 34 − 12 − 44 − 12 (app.html:38053, 38196)
  fond:'#82AEF8',               // un hex ; défaut : le champ de la nature (promi #82AEF8 · chiche #FFB8D2 · nuee #C9A8F5)
  traits:[ trait… ],            // le dessin EN COURS (gardé si l'on sort sans poser)
  poses:[ trait… ],             // ce que POSER a posé — seul montré par la bande, la vue entière et le partage
  pose:false,                   // true dès le premier POSER
  masque:false }                // le masquage « pour soi seul »
trait = { c:'#201908',          // la couleur, un hex FIGÉ à la création du trait ; '' pour la gomme
          t:4.5,                // la taille : plume 2,5 · 4,5 · 8 ; gomme 10 · 18 · 30 (app.html:38047–38048)
          g:0,                  // 1 = gomme (rendue en destination-out : elle rend le fond)
          pts:[x,y,t,p, x,y,t,p, …] }   // à plat, 4 nombres par point
```
Un point (`pt(e)`, `app.html:38257–38258`) : `x`, `y` en points de la surface arrondis au dixième ; `t` = horodatage de l'événement (ms,
entier) ; `p` = pression du stylet arrondie au centième, **`-1` pour un doigt**. Un point à moins de 0,3 pt du précédent est ignoré ;
un trait de moins d'un point complet n'est pas gardé (`app.html:38259`, `38269`).
⚠ Un dessin d'avant v133 peut porter `h:754` : à l'ouverture, `h` est ramené à `surfH()` sans perdre de trait (`app.html:38198`).
Le modèle de largeur (effilé E2, vitesse, pression, jamais sous 1 pt) est la fonction `largeurs` (`app.html:38090–38098`) — il relève du
document de rendu, pas des données.

**Où il est stocké — trois cibles** (`lit`/`ecrit`, `app.html:38067–38072`) :

| Cible | Emplacement | Persistance |
|---|---|---|
| une parole | `p.dessin` | avec `promi_state` |
| le brouillon de la page + | `window._phrase.dessin` | mémoire seulement ; suit la parole ou le Cercle à la plantation (`app.html:38313–38317`) |
| un Cercle | `promi_dessins_cercle[cléDuCercle]` | clé `localStorage` à part |

**États et transitions**

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| aucun | mode dessin ouvert, dessin neuf `{traits:[], poses:[], pose:false, masque:false, fond:champ de la nature}` | Bouton photo → menu → **« Dessiner »** (en tête ; fiche, page +, fiche d'un Cercle) → `ouvre(c)` | `app.html:38193–38208`, `38297` |
| en cours | en cours + 1 trait | lever du doigt/stylet sur la surface (`fin`) → `traits.push`, sauvegarde immédiate (`garde_`) | `app.html:38268–38270` |
| en cours | en cours − 1 trait | **ANNULER** (`traits.pop()`), désactivé s'il n'y a aucun trait | `app.html:38226`, `38254` |
| en cours (jamais posé) | fond changé | **COULEUR → onglet FOND** (Ma Parole ! seulement) ; si la couleur du trait égale le nouveau fond, elle change | `app.html:38238–38249` |
| en cours | **posé** : `poses = copie(traits)`, `pose:true`, `masque:false` | **POSER** (`sort(true)`) avec au moins un trait | `app.html:38273–38275` |
| en cours, aucun trait | **supprimé** (`ecrit(c, null)`) | **POSER** sans trait | `app.html:38275` |
| en cours | gardé tel quel (`traits` conservés, `poses` inchangés) ; supprimé s'il est vide et jamais posé | **Sortie sans poser** : ✕ « Quitter le dessin » (v133, Q392), touche Échap, ouverture de l'offre (`_cercleDessus`) | `app.html:38217`, `38276`, `38281–38282` |
| posé | rouvert : `traits` repris, **fond fixé** (plus d'onglet FOND), couleurs limitées à celles déjà présentes | « Dessiner » sur un dessin posé (`d.pose`) | `app.html:38190`, `38238` |
| posé, visible | posé, **masqué** (`masque:true`) et retour | bouton œil `button.dz-oeil` de la bande (« Masquer le dessin » / « Afficher le dessin ») ; masqué : la bande rend la dalle ou la photo | `app.html:38133–38143` |
| tout | supprimé | menu → **« Retirer le dessin »** (`retire`) | `app.html:38283`, `38296` |
| brouillon de la page + | `p.dessin` de la parole plantée, ou dessin du Cercle neuf | planter (`#addPromi` / `#addNuee`) | `app.html:38313–38317` |

**Règles de données**
- Chaque trait garde SA couleur : un changement de palette ne touche que les traits à venir (CLAUDE.md v132).
- Sans Ma Parole ! : on dessine à l'encre du mode sur le champ de la nature ; le panneau des couleurs est un mur (`app.html:38202`, `38237`).
- Visible = `poses.length > 0 && !masque` (`app.html:38080–38081`). **Un dessin masqué n'est jamais emporté dans un partage**
  (`window._dessinCase(pid)`, `app.html:38321`).
- Un Cercle ne porte pas de photo : son menu ne propose que le dessin (`app.html:38292`).

> **ATTEND FIREBASE — deux points nommés par Tom :**
> 1. **LE DESSIN COMMUN D'UN CERCLE.** Aujourd'hui `promi_dessins_cercle` est une table locale, un dessin par clé de Cercle, sur un seul
>    appareil. Côté serveur : le dessin d'un Cercle est un document PARTAGÉ entre ses membres (qui peut tracer, qui peut poser, comment deux
>    membres qui dessinent en même temps se concilient — **⚠ TROU T13 : rien n'est décidé**, le prototype n'a qu'un auteur).
> 2. **LE MASQUAGE INDIVIDUEL.** Aujourd'hui `masque` est un champ DU dessin lui-même (`dd.masque=!dd.masque`, `app.html:38136`) — et
>    POSER le remet à `false` pour tout le monde (`app.html:38275`). Or il est « pour soi seul ». Côté serveur, le masquage doit être une
>    préférence **par personne et par dessin** (hors du document partagé), y compris pour le dessin d'une parole que l'autre voit.

---

## 6. La photo

| Donnée | Forme | Source |
|---|---|---|
| `p.photo` | une **data-URL** (`FileReader.readAsDataURL`, champ `accept="image/*"`), ou `null` | `app.html:20118–20127` |
| `window._phrase.photo` | la photo du brouillon de la page + ; recopiée sur la dernière parole plantée si elle n'en a pas et n'est pas une demande | `app.html:20270–20278` |
| `p.dalleOrigine` | booléen — §1.2 ; choisir l'option retire la photo (`if(p.photo) p.photo=null`) | `app.html:37509` |

**Ce que montre la bande d'une fiche — une chose à la fois** (CLAUDE.md v128/v132) : le **dessin** s'il est posé et non masqué ; sinon la
**photo** ; sinon la **dalle** (du Studio, ou d'origine si `dalleOrigine`).

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| dalle | photo | menu du bouton photo → **« Importer une photo »** (v133 ; « Importer une image » avant) → sélecteur du système, ouvert DANS le geste | `app.html:37505`, `20121` |
| photo | dalle | **« Retirer la photo »** | `app.html:37511` |
| dalle du Studio ↔ dalle d'origine | bascule `dalleOrigine` (retire la photo) | **« La dalle d'origine »** / **« La dalle du Studio »** — proposé seulement si `p.monde.m` existe | `app.html:37506–37510` |
| photo ou dessin dans la bande | vue entière (aucune donnée changée) | toucher la bande (C-051) | CLAUDE.md v131 ; `A-INTEGRER.md` |

> **⚠ TROU T14** — la photo est une data-URL **dans `promi_state`** (quota `localStorage`, aucune réduction relevée) ; le cadrage
> (« on y voit ce que la bande recadrait ») n'a pas de donnée propre trouvée. En Swift : un fichier + une référence ; **ATTEND FIREBASE**
> pour qu'une photo soit vue par l'autre (stockage partagé).

---

## 7. Le Cercle (clé interne `nuee`)

**Un Cercle n'est pas un objet : c'est une CLÉ dans plusieurs tables parallèles.**

| Table | Forme | Sauvegardée | Rôle · écriture |
|---|---|---|---|
| `NUE` | `{clé: nom}` | oui | l'existence et le nom. Clé = `'n'+Date.now()` à la création (`app.html:3196`) ; `'soi'` → « Moi-même » est réservée. Renommage : `NUE[curNuee]=v` (`app.html:9271`) |
| `NUEEMEM` | `{clé: [prénoms]}` | oui | les membres (sans « moi »). Création (`newNueeMembers`), Peaufiner MEMBRES (`app.html:32660`), `addMem` (`app.html:9263`), retrait (`app.html:9190`), `filRejoindre` (`app.html:33793`) |
| `NUEDALLE` | `{clé: {ci, lit, rgb?, choisi?}}` | oui | la couleur de SA dalle sur la Toile (tirée de son nom, ou choisie — `lot-CERCLE-COULEUR`, `app.html:33087–33089`, `33159–33161` ; `promi-moteur.js:6110–6112`) |
| `promi_dessins_cercle` | `{clé: dessin}` | oui (clé à part) | §5 |
| `NUEE` (pinceau) | `{clé: nomDePinceau}` | **non** (T7) | `app.html:25342`, `25371` |
| `NUECREATOR` | `{clé: 'moi' ou prénom}` | **non** | qui l'a créé ; conditionne « dissoudre » et le retrait des pièces (`app.html:9112`, `9226–9227`) |
| `NUETHEME`, `NUENOTE` | `{clé: texte}` | **non** | (ancien) thème et note du Cercle (`app.html:9113–9114`, `9260–9261`) |
| `NUEFILES` | `{clé: [{name,type,size,by}]}` | **non** | pièces du Cercle (`app.html:9115`, `9183`) |
| `NUEHT`, `NUEORD` | `{clé: nombre}` | **non** | (démonstration) hauteur de trait figée et rang dans l'Index (`app.html:21339–21345`, `21197`) |

Les **paroles d'un Cercle** sont les `promises` dont `nuee === clé`. Sur la Toile, un Cercle nommé a SA dalle (`kind:'nuee'`,
`Toile.addNuee(clé)`, `Toile.addMember(clé, id)` — `promi-moteur.js:7109`).

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| — | Cercle créé : `NUE[clé]=nom`, `NUEEMEM[clé]=membres`, + son premier Promi (`who` = `'le groupe'` s'il a des membres, sinon `'moi'` ; `due 7`) | Page + « Un Cercle » : **tracer le trait ENTIER** (0 → 390) → `#addNuee` ; nom obligatoire (« Donne un nom à ton Cercle ») ; `feedAdd('nuee','Tu as créé le Cercle …')` ; la couleur choisie à la page + va à `NUEDALLE` ; le dessin du brouillon suit | `app.html:3196`, `33155–33163`, `38316` ; CLAUDE.md §4 |
| Cercle | + une parole | « Planter dans le Cercle » (dernière ligne du fil) → page + avec `selNuee` → `#addPromi` | `app.html:3192` (`selNuee`) ; `redteam_nuee_entree` (CLAUDE.md §7) |
| Cercle | renommé | fiche → renommage (`rinp` → `NUE[curNuee]`) | `app.html:9271` |
| Cercle | membre ajouté / retiré | Peaufiner MEMBRES (`_gensFiche('nuee')`) ; `.nqm-rm` | `app.html:32660`, `9190`, `9263` |
| Cercle | couleur changée | Peaufiner COULEUR (Ma Parole !) → `NUEDALLE[clé]` + `Toile.refigeCouleurs()` | `app.html:33087–33090` |
| parole | rattachée / détachée | `#dNueeChips` : `p.nuee = clé ‖ undefined` | `app.html:3754` |
| invitation reçue (événement `invitation` du Fil) | Cercle rejoint : `NUE[k]=nom`, `NUEEMEM[k]` + l'invitant ; événement → `joined` « Tu as rejoint « … » » | Fil → rejoindre (`filRejoindre(fid)`) | `app.html:33791–33796` |
| Cercle | **dissous**, paroles libérées (`p.nuee=null`) | « Dissoudre le Cercle ? » → « Libérer les Promi » (`_nqDissolve(key,false)`) ; visible seulement si `NUECREATOR[clé]==='moi'` | `app.html:9248–9249`, `9227`, `3662` |
| Cercle | **dissous**, paroles supprimées | « Tout supprimer » (`_nqDissolve(key,true)`) ; retire aussi `NUEEMEM`, `NUETHEME`, `NUENOTE`, `NUEFILES`, `NUECREATOR` | `app.html:9248–9249` |

⚠ La dissolution ne retire ni `NUEDALLE[clé]` ni `promi_dessins_cercle[clé]` (non listés à `app.html:9249`).

> **ATTEND FIREBASE** : un Cercle à plusieurs (identité des membres, invitation réelle, qui est le créateur), les paroles plantées par les
> autres, le fil d'un Cercle, le dessin commun (§5), la dissolution pour tous. Aujourd'hui les membres sont des prénoms tapés ; l'invitation
> n'existe que comme événement de démonstration (`app.html:21383`).
>
> **⚠ TROU T15** — « Cercles illimités » fait partie de l'offre (ETAT §6, `app.html:2786`), mais **aucune limite au gratuit n'a été trouvée**
> dans le code (cherché : `limiteNuee`, `MAX_NUEE`, « illimit »). Le nombre de Cercles du gratuit est à demander.

---

## 8. Le Fil (le journal `FEED`)

Le Fil n'est pas demandé comme entité, mais il porte des **transitions** (relever, rejoindre, tenir) : il est décrit ici pour elles.
`FEED` est un tableau, le plus récent en tête ; sauvegardé avec `_fid` (`app.html:6828`, `6836`).

Événement : `{id, type, text, pid?, from?, t, unread, fait?, nuee?, nom?, ev?}` — `t` est un MOT (« à l'instant », « hier », « il y a 3 j »),
pas une date (`app.html:6836`).
Types rencontrés : `added` · `kept` · `missed` · `nuee` · `relance` · `comment` · `accept` · `joined` · `received` · `chiche_recu` ·
`chiche_releve` · `invitation` · `moitie` (`app.html:3042–3764`, `4082`, `6837–6846`, `21381–21383`).
`feedReacted` `{idÉvénement: booléen}` : la réaction posée sur un événement (`app.html:6893`). **Ce qui attend un geste de moi**
(`_filAttend`, `app.html:33780–33785`) : `chiche_recu` ; `received` si la parole est `pending` ; `invitation` non faite ; `moitie` non faite
et parole non tenue. Le Fil ne montre jamais une parole qui n'existe plus (C-049). ⚠ Le texte est une phrase toute faite stockée — le titre
y est recopié (et relu par expression régulière pour relever un Chiche, `app.html:6911–6913`).

**ATTEND FIREBASE** : tout événement venant d'un autre (`received`, `chiche_recu`, `chiche_releve`, `invitation`, `moitie`, `joined`) n'existe
aujourd'hui que dans le Fil de démonstration (`seedFeed`, `app.html:6837`, semé seulement sans sauvegarde — v94).

---

## 9. Les réglages

### 9.1 Le Studio — global (CLAUDE.md §5, « un réglage vit là où vit ce qu'il règle »)

| Réglage | Donnée | Valeurs · défaut | Source |
|---|---|---|---|
| le monde | `promi_studio.m` (+ `promi_monde`, `state.structure`) | 20 clés (`order`, `app.html:6651`) : gratuits `encre` (Pochade, défaut) · `touffe` · `brouillamini` · `halin` · `esquille` · `mosaique` (Tesselle) · `braille` · `pixel` (Buvard) ; Ma Parole ! (`_mondesCercle`, `app.html:6640`) `ramage` · `guingois` · `chantourne` · `volubilis` · `madrure` · `chamade` · `ritournelle` · `bobinette` · `mascaret` · `terrazzo` (Éclisse) · `gravure` (Taille-douce) · `sillons` (Houle) | ETAT §4 |
| la palette | `promi_studio.p` | 24 clés ; défaut `signal` (Ingénu) | ETAT §5 ; `app.html:2922` |
| la teinte | `promi_studio.h` | nombre, défaut 0 | `app.html:36826` |
| sombre / clair | `promi_theme` | `'light'` ou sombre. ⚠ défaut au premier lancement : v118 dit « clair » (Zzz), mais le Zzz est coupé (v120) — **TROU T16** : le défaut actuel n'a pas été vérifié à l'écran | `app.html:6717`, `8295` |
| avec texte / sans texte | `state.labels` | booléen, défaut `true` | `app.html:2910`, `3790`, `8914` |
| noir et blanc | `promi_nb`, `promi_nb_j` | actif, jauge 0–1 (0,3) | `app.html:33813` |
| Zzz | `promi_zzz` | **COUPÉ** (v120) — ne pas porter sans décision | CLAUDE.md v120 |
| (ancien) | `state.mood` (`'cobalt'`), `state.sort` (`'inspi'`) | sauvegardés, hérités | `app.html:2910` |

`promi_studio.libre` : le monde était-il gratuit QUAND on l'a choisi. Règle v73 (Q339) : « on ne reprend pas ce qui a été donné » — un monde
payant en usage quand Ma Parole ! prend fin devient **acquis** (`app.html:36831–36844`).

### 9.2 Les réglages d'une parole (Peaufiner) — ils sont des champs de la parole

`who` (À QUI) · `avec` (AVEC) · échéance (`due`/`enLair`/`dueISO`) · `trait` (LE TRAIT) · `dalle` (COULEUR — Ma Parole !) · `recur`
(récurrence — Ma Parole !) · `intensity` (importance — Ma Parole !) · `note` · `files` · `nuee` · suppression. Ceux d'un Cercle : son nom,
ses MEMBRES, son TRAIT, sa COULEUR (§7). La page + porte les mêmes sur le brouillon (`window._phrase`, `_ppPinceau`, `_couleurAPlanter`,
`newNueeMembers`, `selNuee`, `_csDueISO`, `_csEnLair` — tous en mémoire, remis à zéro après plantation, `app.html:3195`).

Le brouillon de la page + : `window._phrase = {sens:'faire', qui:'Moi', titre:'', quand:'un jour', avec?, photo?, dessin?, faireAutre?}`
(`app.html:5236`, `5664`, `8358–8359`).

### 9.3 Les notifications — `promi_notifs2` (`lot-V109-NOTIFS`, `app.html:37276–37420` ; ETAT §7)

| Champ | Type · défaut | Sens |
|---|---|---|
| `datees` | booléen · `false` | « Mes paroles datées — un petit mot la veille » (gratuit) |
| `lair` | booléen · `false` | « Mes paroles en l'air » (Ma Parole !) — une par semaine au plus (`LAIR_JOURS=7`, « à valider ») |
| `heure` | 8 · 12 · 19 · défaut 19 | « L'heure » (Ma Parole ! ; 19 h au gratuit) |
| `refus` | entier · 0 | nombre de « pas besoin » ; à 2, la question ne revient plus |
| `lairDepuis`, `lairDernier` | horodatages | activation et dernier envoi « en l'air » |

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| `datees:false` | question affichée 12 s | 1,9 s après la plantation (`#addPromi`) d'une parole **datée** et « mienne » ; jamais pendant l'onboarding, jamais si `refus≥2` ou permission refusée | `app.html:37350–37377` |
| question | `datees:true, refus:0`, `p.rappel=true`, **demande de permission système** | « oui » | `app.html:37363` |
| question | `refus+1`, `p.rappel=false` | « pas besoin » (la disparition seule après 12 s ne compte pas) | `app.html:37364`, `37368` |
| réglage | bascule `datees` / `lair` / heure suivante (8 → 12 → 19) | page Notifications des Réglages (`data-nt`) ; `lair` et `heure` sans effet au gratuit (mur) | `app.html:37396–37401` |

Envoi : seulement page ouverte, une notification par jour au plus, rien quand la date est passée (`plan`, `tick`, `app.html:37316–37339`).
« Ce qu'on me lance — Chiches, invitations, réponses · bientôt » est visible, éteint. **ATTEND FIREBASE** : l'envoi app fermée et tout ce
qui vient d'une autre personne. (ancien) `notifOn`, `remind`, `armAllReminders` (`app.html:3666–3669`) : l'ancien système, encore sauvegardé.

### 9.4 Divers

Langue `promi_lang` (défaut `fr`) · le partage : `shareHidden` `{idDeParole: true}` = parole écartée de « Mon Folio » (`app.html:6270–6282`,
sauvegardé) ; les autres options du partage (Pelote seule ou dans le Folio, sans texte…) sont en mémoire (`window.shPelote`, `app.html:37600`) ·
la Pelote : §0 (clés `promi_pelote_*`) · onboarding : `promi_onb`, `promi_debut`.

---

## 10. Les achats

**Rien n'est réellement acheté dans le prototype : aucun paiement, aucun reçu.** Tout est un drapeau local.

### 10.1 Ma Parole ! (l'abonnement — clé interne `isPremium`)

`var isPremium=false; function setPremium(v)` (`app.html:3166`) : pose `isPremium` et la classe `.premium` sur `#device`.
Enveloppée par v73 (`app.html:36842–36844`).

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| gratuit | **Membre Ma Parole !** | écran de l'offre : `#buyMonth` (« Essayer 14 jours ») ou `#buyYear` (« ou prendre l'année — 39 € ») → `setPremium(true)`, toast « Tu es Membre Ma Parole ! ✓ · tout Promi débloqué » | `app.html:3182`, `31573–31579`, `2790–2791` |
| gratuit ↔ payé | bascule de démonstration | `#demoTg` | `app.html:3181` |
| payé | gratuit | `setPremium(false)` : si le monde courant est payant et non acquis, il devient **acquis** (v73) | `app.html:36842–36844` |

Prix (ETAT §6) : **39 € / an** (3,25 €/mois) · **5,99 € / mois** · **essai 14 jours** · sans engagement.
Ce qu'elle ouvre (ETAT §6) : ce qu'on te tient (l'autre moitié), la récurrence, le rappel à l'heure choisie, l'importance, la mémoire des
paroles en l'air, la couleur de la dalle, douze mondes, les Cercles illimités ; + les teintes du dessin (v133, C-061).
Compteur des murs `promi_murs` : `{n, t, der, decouvert}` — rang de la phrase, date du dernier mur, dernière phrase, « déjà découvert » ;
remis à zéro après `ABSENCE` = 14 jours (« à valider », `app.html:37135`, `37151`). Dix-huit phrases (`TEXTES`, `app.html:37115` ; ETAT §6).

> **⚠ TROU T17** — `isPremium` **n'est sauvegardé nulle part** (absent de `saveState`, `app.html:7644`) : l'abonnement est perdu au
> rechargement. Ni durée d'essai, ni date de fin, ni formule choisie (mois / année) ne sont stockées : « Essayer 14 jours » et « l'année »
> font exactement la même chose. **ATTEND StoreKit + FIREBASE** (C-026) : droit d'accès, essai, expiration, restauration.

### 10.2 Un design à l'unité (un monde)

`var _ownedDesigns={}` (`app.html:3166`) — `{cléDeMonde: true}` ; persisté dans `promi_studio.acquis` (`app.html:36824–36829`).

| De | Vers | Déclencheur | Source |
|---|---|---|---|
| monde verrouillé | **acquis** + appliqué (`Toile.setTheme(w)`) | Studio, sur un monde payant : bouton `#stLockBuy` **« Adopte ce design — 2 € »** → `_ownedDesigns[_lockedWorld]=true` | `app.html:2774`, `8567`, `22410` |
| monde payant en usage | **acquis** (gardé) | fin de Ma Parole ! pendant l'usage, ou monde devenu payant depuis (v71/v73, Q339) | `app.html:36831–36844` |

> **⚠ TROU T18** — **le prix d'un design** : `2 €` au Studio (v118, CLAUDE.md), mais l'écran de l'offre écrit encore « un design à l'unité —
> 1 €, ou 4 pour 3 € » (`app.html:2794`) et ETAT §6 « un monde à l'unité 1 € ». Le lot de quatre n'a aucun état. À trancher avant StoreKit.
> (Voir aussi T6 : les pinceaux à 0,50 €.)

---

## 11. Ce que le moteur de la Toile tient (hors modèle, pour mémoire)

Le moteur (`promi-moteur.js`) garde des **graines** (`seeds`) : `kind` `'promi'` · `'nuee'` · `'gray'` (cellule vide), `pid` (l'id de la
parole), `nuee` (la clé du Cercle), `ci`/`lit`/`rgb`/`choisi` (recopiés de `p.dalle` ou `NUEDALLE`), `nat` (0 Promi · 1 Chiche · 2 Cercle,
lue sous la palette Ingénu seulement) — `promi-moteur.js:6105–6112`, `7109`. Ce n'est **pas** une donnée à sauvegarder : la Toile se
resynchronise depuis les paroles (`Toile.sync(ids)`), et « un semis est déterministe » (CLAUDE.md §4). Le détail relève de `CONTRAT-MONDE.md`.

---

## 12. ATTEND FIREBASE — récapitulatif

| Sujet | Aujourd'hui (local) | À faire côté serveur |
|---|---|---|
| **Compte** | `promi_compte` = une intention ; `promiConnexion` non définie | authentification Apple / Google, « Garder ta Toile », suppression de compte, déconnexion (§3) |
| **Personnes réelles** | un prénom = une chaîne ; identité par égalité de texte | identifiant de personne, lien avec un compte, visage / photo partagés (§3) |
| **Paroles entre deux personnes** | `from`/`who` sont des prénoms ; `pending`, `accepted` viennent du jeu de démonstration | envoi, réception, acceptation d'une parole qu'on me fait (§1.2) |
| **La moitié de trait tracée par l'autre** | aucun champ ; un événement `moitie` de démonstration | deux marques de tracé, une par personne, et l'état « tenu » qui en découle (T5) |
| **La demande** | `demandeAccepter` appelée localement | l'acceptation par l'autre, l'expiration à 30 jours côté serveur (§1.7) |
| **Le Chiche** | `chicheEtat:'releve'` jamais écrit par un geste | relever par l'autre, « tenu à deux » (§2, T9) |
| **Cercles à plusieurs** | tables locales, membres = prénoms tapés | membres réels, invitation, créateur, paroles des autres, dissolution pour tous (§7) |
| **LE DESSIN COMMUN d'un Cercle** | `promi_dessins_cercle[clé]`, un seul auteur | document partagé, règles d'écriture à plusieurs (§5, T13) |
| **LE MASQUAGE INDIVIDUEL d'un dessin** | `masque` dans le dessin lui-même | préférence par personne et par dessin, hors du document partagé ; jamais dans un partage (§5) |
| **Photos** | data-URL dans `promi_state` | stockage de fichiers, visibilité par l'autre (§6) |
| **Le Fil** | journal local, textes tout faits | événements venus des autres (§8) |
| **Notifications** | page ouverte seulement | envoi app fermée ; « Ce qu'on me lance » (§9.3) |
| **Achats** | drapeaux en mémoire | StoreKit + droit d'accès serveur, essai, restauration (§10) |
| **Commentaires, relances, pièces jointes** | locaux, `by` = un prénom | partagés entre les personnes de la parole |

---

## 13. Les TROUS — liste

| N° | Trou | Cherché |
|---|---|---|
| T1 | `ht` (hauteur de trait figée à la plantation) n'est posée que sur le jeu de démonstration ; règle d'engendrement absente | `\.ht\s*=`, `NUEHT` |
| T2 | Aucune date de plantation ni de tenue ; `leJour` est un mot de démonstration ; l'ordre des tenues = ordre d'apparition (`promi_pelote_ordre`) | `tenuLe`, `keptAt`, `cree`, `created` |
| T3 | `due` = jours relatifs sans date de référence, jamais décrémenté ; « à tenir » automatique inatteignable hors démonstration ; « un jour » vaut `null` ou 30 selon le chemin | `due--`, `due-=`, `quandToDue` |
| T4 | Défaire une parole tenue (`tenu → encours`) : seulement l'ancien `#segStatus`, aucune décision | `\.status\s*=` (6 écritures) |
| T5 | La moitié de trait de l'autre : aucun champ | `moitie`, `trace` |
| T6 | Pinceaux « à 0,50 € » : aucun état d'achat, absents de l'offre | `_PINCEAU_META`, `acquis` |
| T7 | Pinceau d'un Cercle (`NUEE`) non sauvegardé ; `NUETHEME`, `NUENOTE`, `NUEFILES`, `NUECREATOR`, `NUEHT`, `NUEORD` non plus | `saveState` (`app.html:7644`) |
| T8 | Qui accepte une demande, et par quel bouton (`demandeAccepter` : appelant non relevé) | définition seule |
| T9 | `chicheEtat:'releve'` n'est écrit par aucun geste ; relever un Chiche reçu crée une parole neuve sans `chicheEtat` | `chicheEtat` (7 occurrences) |
| T10 | `USER.photo` non sauvegardée | `saveState`, `USER\.photo` |
| T11 | Un gardé de côté est-il sur la Toile ? `addPromi` l'y met, `sync(!draft)` l'en retire | `draft`, `Toile.sync` |
| T12 | Reprise d'un gardé de côté : la parole plantée a un NOUVEL id ; ce qui doit survivre (photo, dessin, couleur) n'est pas écrit | `_brouillonRepris` |
| T13 | Dessin commun d'un Cercle : règles à plusieurs non décidées | `lot-V132-DESSIN` |
| T14 | Photo : data-URL sans réduction ni donnée de cadrage | `p\.photo` |
| T15 | Limite du nombre de Cercles au gratuit : introuvable | `illimit`, `MAX_NUEE`, `limiteNuee` |
| T16 | Thème par défaut au premier lancement depuis que le Zzz est coupé : non vérifié (pas de navigateur) | `promi_theme`, `app.html:8295` |
| T17 | `isPremium` non sauvegardé ; ni essai, ni formule, ni échéance d'abonnement | `setPremium(` (7 occurrences) |
| T18 | Prix d'un design : 2 € (Studio, v118) contre « 1 €, ou 4 pour 3 € » (écran de l'offre) et « 1 € » (ETAT §6) | `€` |
| T19 | Trois noms pour la nature d'un gardé de côté : `dk`, `draftKind`, `kindDraft` ; lequel fait foi (le chemin vivant écrit `dk`) | `dk`, `draftKind`, `kindDraft` |
| T20 | `aussi` (autres destinataires) : écrit, jamais lu ; `accepted` : écrit, jamais lu | `\.aussi\b`, `\.accepted\b` |
| T21 | Plusieurs destinataires : la plantation crée UNE parole par personne (`app.html:3192`), mais Peaufiner écrit plusieurs prénoms dans un seul `who` (`', '`, `app.html:32663`) — deux modèles | `_recips`, `l.join` |
| T22 | La dissolution d'un Cercle laisse `NUEDALLE[clé]` et `promi_dessins_cercle[clé]` | `app.html:9249` |
| T23 | `promi_compte` : la valeur `'fait…'` est lue, jamais écrite | `promi_compte` |

*Limites de ce relevé : aucun navigateur n'a été lancé (consigne) — les champs viennent de la lecture du code, pas d'une sauvegarde réelle
relue. Un champ écrit par une variable au nom inattendu a pu échapper au recensement (recherche par motif d'affectation sur les noms relevés).*
