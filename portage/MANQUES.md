# MANQUES — ce qu'aucune décision ne couvre encore

> Dossier de portage (C-021), écrit le 6 oct. 2026 sur l'état v134. **Lecture et extraction seulement : rien n'est décidé ici.**
> Une section par sujet, toujours dans le même ordre : **ce que le prototype fait** (simulé ? absent ?) · **ce qui est décidé**
> (avec sa source) · **ce qui manque pour construire** · **les questions à poser à Tom**. Rien n'est proposé comme une valeur :
> là où le prototype porte un chiffre que personne n'a décidé, il est rapporté comme tel. Ce qui n'a été trouvé nulle part : **⚠ TROU**.
>
> Le prototype est une page web sans serveur : **tout ce qui demande un autre appareil, un autre compte, le système ou une
> boutique y est simulé ou absent.** C'est la matière de ce document.

**Sommaire** : 1 notifications · 2 vibrations · 3 Firebase · 4 StoreKit · 5 VoiceOver de la Toile · 6 pages légales · 7 numéro de
version · 8 polices · 9 page du trait partagé · 10 Zzz · 11 dégradation adaptative · 12 iPad, orientation, tailles d'écran ·
13 Dynamic Type · 14 localisation · 15 export et suppression du compte · 16 archive · 17 liste des trous.

---

## 1 · Les notifications

**Ce que le prototype fait** (`lot-V109-NOTIFS`, `app.html` l. ≈ 37276 ; juge `redteam_notifs`, 36 contrôles)
- Il calcule un **PLAN** (`window._notifPlan(maintenant)`) : pour chaque parole datée « en cours » qui est la mienne, la veille à
  l'heure choisie (si je l'ai vue avant) ou le jour même à l'heure choisie ; pour les paroles en l'air (Ma Parole ! seulement), une
  au plus tous les `LAIR_JOURS` = 7 jours. Jamais rien pour une date passée.
- Il **envoie page ouverte seulement** : un minuteur (toutes les 30 s, et au retour au premier plan) appelle `new Notification(…)`
  si la permission est accordée ; une par jour au plus (journal `promi_notifs_log`). Commentaire du code : « l'app fermée attend Firebase ».
- La **permission est simulée dans le juge** (« WebKit n'a pas d'API Notification hors écran d'accueil ») : on y compte les demandes et les envois.
- La page des Réglages : MES PAROLES DATÉES · MES PAROLES EN L’AIR · L’HEURE · CE QU’ON ME LANCE — cette dernière « visible,
  éteinte, sans prise » (« Chiches, invitations, réponses · bientôt »).

**Ce qui est décidé**
- Jamais de demande au lancement ; « Je te le rappelle ? » à la plantation d'une parole DATÉE, la demande au système seulement après
  « oui » ; deux « pas besoin » d'affilée puis on n'insiste plus ; rien quand la date est passée ; une notification par jour au plus ;
  « C’est aujourd’hui. » part à l'heure choisie (CLAUDE.md §7 ; Q356 validée v110 ; `redteam_notifs`).
- Les cinq textes, au caractère près (`SPEC-JUGES.md` §3) : veille à soi, veille à quelqu'un, veille d'un Chiche, le jour, en l'air.
- Gratuit : le mot de la veille. Ma Parole ! : la mémoire des paroles en l'air, le choix de l'heure (8 h · midi · 19 h ; 19 h au
  gratuit). Firebase : l'envoi app fermée, tout ce qui vient d'une autre personne (`ETAT-30-SEPTEMBRE-2026.md` l. 190).
- « Plus de “Rappels activés ✓” : activer n'envoie rien » (`redteam_notifs`, point 9).

**Ce qui manque pour construire**
- **La planification locale** : le PLAN est une fonction pure, elle se porte ; mais rien ne dit quand il se recalcule ni comment il
  devient des `UNNotificationRequest` (iOS n'en garde que 64 en attente par app) : à la plantation, à chaque changement d'une parole,
  à chaque ouverture ? Que devient une notification planifiée quand la parole est tenue, retirée, reportée, ou quand l'heure change ?
- **« Une par jour au plus »** est appliquée à l'ENVOI dans le prototype ; en local, elle doit l'être à la PLANIFICATION (choisir
  laquelle part, si deux paroles tombent le même jour) — aucun ordre de priorité n'est écrit au-delà du tri par date.
- **« Si je l'ai vue avant »** (`vuLe`) : le prototype n'envoie la veille que si la parole a été vue avant ce moment. Règle de produit
  ou artefact de la simulation ?
- **APNs** : rien n'existe. « Ce qu'on me lance » (un Chiche reçu, une invitation à un Cercle, une réponse, l'autre moitié d'un trait
  tracée) n'a ni mots, ni réglage fin, ni règle de fréquence.
- **La permission** : l'état « refusé au niveau du système » (l'utilisateur a dit oui dans l'app, non à iOS, ou l'a coupée dans
  Réglages) n'a pas d'écran. La permission provisoire d'iOS (livraison silencieuse) n'est pas évoquée.
- **Le toucher sur une notification** : où mène-t-il ? (la fiche de la parole est la lecture évidente ; elle n'est écrite nulle part.)
- Pastille sur l'icône, son, regroupement, actions rapides (« tenir », « reporter ») : rien.
- Deux valeurs sont marquées « à valider » dans le code même : les deux autres heures (8 h, midi) et `LAIR_JOURS` = 7.

**Questions à poser à Tom**
1. Les heures 8 h · midi · 19 h et « une parole en l'air par semaine » : validées telles quelles ?
2. Si deux paroles tombent le même jour, laquelle parle ? (la plus ancienne, celle promise à quelqu'un, la première plantée…)
3. Toucher une notification ouvre-t-il la fiche de la parole ?
4. « Ce qu'on me lance » : quels événements d'une autre personne méritent une notification, et avec quels mots ?
5. Que montre la page quand iOS a refusé la permission ?
6. C-022 prévoit une « conversation dédiée » aux vibrations et aux notifications : la tenir avant le premier lot Swift ?

---

## 2 · Les vibrations (haptique)

**Ce que le prototype fait**
- Onze appels à `navigator.vibrate` dans `app.html`, de 6 à 14 ms, et un motif `[12, 40, 26]` quand le trait est donné jusqu'au
  bout ; un autre à 14 ms quand le doigt passe les deux tiers du trait (l. ≈ 12743–12756).
- **Sur iPhone ils ne font rien** : Safari sur iOS n'expose pas cette API. Aucune vibration n'a donc jamais été éprouvée par Tom sur l'appareil.

**Ce qui est décidé** : **rien.** C-022 : « Vibrations et notifications (conversation dédiée) », REPORTÉ, « Core Haptics ». Aucun
bloc de CLAUDE.md, aucune question de QUESTIONS.md ne porte une décision sur l'haptique.

**Ce qui manque pour construire** : tout — la liste des moments qui vibrent, leur caractère (impact léger, moyen, succès, motif
continu qui suit le trait), le rapport à « Réduire les animations », au mode silencieux et au réglage du système, un éventuel
réglage dans l'app.

**Questions à poser à Tom**
1. Quels moments vibrent ? Candidats lus dans le prototype (des appels existants, pas des décisions) : le trait qui passe les deux
   tiers, le trait donné, un choix requis manquant, le geste de couleur du Studio qui s'arme, le zoom à sa borne.
2. Le trait vibre-t-il EN CONTINU sous le doigt (Core Haptics), ou seulement à son terme ?
3. La Pelote sous le doigt, la Toile au repos, POSER dans le dessin : vibrent-ils ?
4. Un réglage « vibrations » dans l'app, ou seulement celui du système ?

---

## 3 · Firebase — comptes, personnes, Cercles à plusieurs

**Ce que le prototype fait**
- **Tout est local** (`localStorage`) : paroles, Cercles, personnes, dessins, réglages. Les personnes (Rachel, Marion, Nico, Adrien…)
  sont un **jeu de démonstration** ; ce qu'elles « tiennent envers toi » est fabriqué.
- **Le compte** : après le premier trait, l'encart « Garder ta Toile » propose « Continuer avec Apple » / « Continuer avec Google » ;
  ils appellent `window.promiConnexion(k)` **s'il existe** — il n'existe pas ; l'app note `promi_compte = demande-<k>` ou `plus-tard`.
  « Se déconnecter » appelle `window.promiDeconnexion` s'il existe (`joignable-dette.json` : « point de branchement de Firebase : voulu »).
- **La moitié de trait de l'autre** : simulée. L'instant « l'autre moitié arrive » (cadres 96–101, `releve-S5-instant`) est joué
  localement ; personne ne trace de l'autre côté.
- **Un Cercle à plusieurs** : ses membres sont des noms ; son fil, ses Promi et son dessin (`localStorage promi_dessins_cercle`,
  un dessin PAR CERCLE) vivent sur un seul appareil.
- **Le masquage d'un dessin** : « pour soi seul, mémorisé par fiche » — sur cet appareil.
- **Inviter** : « Inviter sur Promi » (Réglages, écran Partager) ; rien ne part vers un serveur.
- **La ligne du membre** dans les Réglages : « À PRÉVOIR — le branchement viendra avec Firebase » (Q343).

**Ce qui est décidé**
- Le compte vient APRÈS le premier trait ; jamais avant (onboarding, 21 sept. ; `redteam_onboarding`). Au rejeu, le compte revient
  tant qu'il n'existe pas ; une porte permanente y mène (« Garder ta Toile », contrôles O21, O22).
- On peut payer sans compte, en étant prévenu deux fois (Q326, C-035 — mots « à valider »).
- **Une seule source de vérité : la liste des paroles** ; chaque écran s'y abonne (C-049 ; A-INTEGRER : « un seul modèle observable »).
- Un dessin est une liste de traits, jamais une image ; chaque trait garde sa couleur ; un dessin masqué n'est jamais emporté dans un
  partage (CLAUDE.md v132).
- Une parole promise à quelqu'un se tient à deux moitiés ; un Cercle se lance en traçant le trait ENTIER (CLAUDE.md §4, 19 août).
- « Tes Promi perso restent sur ton appareil. Privé par défaut, partagé quand tu le choisis. Pas de pub. » (texte des Réglages.)
- Le trait personnalisé (C-045), s'il est retenu, est une DONNÉE de la parole (A-INTEGRER).

**Ce qui manque pour construire**
- **Le modèle de données partagé** : rien n'écrit ce qu'est une parole côté serveur — qui la possède, qui la voit, qui peut la
  modifier, ce que voit le destinataire d'un Promi ou d'un Chiche (sa propre fiche ? la même ?), ce qui reste local (« tes Promi
  perso restent sur ton appareil » : alors quoi est synchronisé, et quand ?).
- **Les personnes** : comment un nom saisi (« + Ajouter quelqu'un ») devient un compte — contacts du téléphone, lien d'invitation,
  recherche par pseudo ? Que se passe-t-il quand je promets à quelqu'un qui n'a pas l'app ? Quand deux noms désignent la même personne ?
- **La moitié de l'autre** : comment l'autre est prévenu, où il trace, ce qui se passe s'il ne trace jamais, s'il trace avant moi, si
  nous traçons en même temps ; l'état « en cours » y est-il lié ? (C-023, la page du trait partagé, est le même manque : §9.)
- **Un Cercle à plusieurs** : rôles (qui invite, qui retire, qui dissout — « DISSOUDRE » existe pour un seul utilisateur), arrivée et
  départ d'un membre, ce que devient sa parole quand il part, la couleur du Cercle (un réglage de Ma Parole ! : payée par qui ?),
  le monde et la palette (chacun voit le Cercle dans SON Studio — « tout suit le Studio » — donc deux membres ne voient pas les mêmes dalles : voulu ?).
- **Le dessin commun d'un Cercle** : un seul dessin pour tous ? Qui peut dessiner, POSER, « Retirer le dessin » ? Deux membres qui
  dessinent en même temps : fusion des traits, dernier qui pose gagne ? « Après le premier POSER le fond est fixé » : par qui ?
- **Le masquage individuel** : « pour soi seul » — donc une donnée par membre et par fiche, à synchroniser entre ses appareils ?
- **Les invitations** : le lien, sa durée, ce que voit celui qui l'ouvre sans l'app, sans compte.
- **La synchronisation et le hors-ligne** : aucune règle de conflit, aucun écran d'attente, d'erreur ou de reprise (ETAT-DES-LIEUX
  cite « erreurs et chargement avec Firebase » comme suite à faire). Planter et tenir hors ligne : permis ? Comment se réconcilie un
  trait donné hors ligne des deux côtés ?
- **La réciprocité** (« Ce qu'on t'a tenu », les Noyaux, l'anneau à trois arcs « dans les deux sens ») repose aujourd'hui sur des
  données fabriquées : sa définition sur de vraies données est à écrire.
- **Plusieurs appareils** pour un même compte ; la migration d'une Toile locale vers un compte créé plus tard (« Garder ta Toile »).
- **La modération et le blocage** (exigés par l'App Store dès qu'il y a du contenu entre utilisateurs : dessins, photos, messages).
- Les fournisseurs de connexion : Apple et Google sont dessinés ; rien ne dit s'il y en a d'autres (courriel).

**Questions à poser à Tom** (les six premières bloquent le modèle de données)
1. Qu'est-ce qui quitte l'appareil ? Seulement ce qui est promis à quelqu'un et les Cercles, ou tout dès qu'il y a un compte ?
2. Promettre à quelqu'un qui n'a pas l'app : la parole part-elle (lien d'invitation), ou reste-t-elle chez moi jusqu'à ce qu'il arrive ?
3. La moitié de l'autre : où et quand la trace-t-il ? Que voit-on tant qu'il ne l'a pas fait ?
4. Dans un Cercle : qui peut inviter, retirer, dissoudre ? Chacun y garde-t-il son monde et sa palette ?
5. Le dessin d'un Cercle : un seul pour tous, ou un par membre ? Qui pose, qui retire ?
6. Hors ligne : peut-on planter, tenir, dessiner ? Que voit-on au retour du réseau ?
7. Bloquer et signaler une personne : où ?
8. Connexion : Apple et Google seulement ?

---

## 4 · StoreKit — Ma Parole ! et l'achat d'un design

**Ce que le prototype fait**
- **Ma Parole !** est un booléen local (`isPremium`, la classe `premium` sur l'appareil). Les juges le forcent ; rien n'est acheté.
- La page de l'offre (`#plusScreen`, table `MOTS`) : « Ma Parole ! » · « Retourne ta Toile » · trois arguments (« L’autre moitié de ta
  Toile », « Chaque parole se peaufine », « Ta Toile change de matière — Douze mondes de plus, les couleurs du dessin ») · **« 39 € /
  AN »**, « soit 3,25 €/mois » · « Sans engagement · résiliable à tout moment » · option « Bon, allez d’accord — 39 € / an » · « ou
  5,99 € par mois ». Les Réglages annoncent « essai 14 jours ».
- **L'achat d'un design** : au Studio, sur un monde payant, « Adopte ce design — 2 € », et « Ou débloque-les tous · Avec Ma Parole ! ».
- **Payer sans compte** (`lot-ACHAT-SANS-COMPTE`) : avant, « Avant d’acheter » · « Sans compte, ton achat reste sur ce téléphone : si
  tu en changes ou supprimes l’app, il est perdu. » · « Acheter sans compte » ; juste après, « Garder ton achat » · « Il est sur ce
  téléphone seulement. Garde ta Toile pour ne pas le perdre. »
- **Restaurer** : le mot n'existe nulle part dans `app.html`.

**Ce qui est décidé**
- L'annuel en avant à 39 €, le mois à 5,99 € en option (Tom, 14 sept. ; v16 ; v74 « AN » en capitales). « L'essai reste le bouton
  principal ; l'adhésion passe sur l'option, avec le prix annuel » (v107). Les mots : CLAUDE.md §2 (« Avec Ma Parole ! », « Tu es Membre
  Ma Parole ! », « Retourne ta Toile », « Bon, allez d’accord »).
- Un design s'adopte à 2 € (v118 ; 1 € avant). « 4 pour 3 € » est gelé (Q206).
- Ce que Ma Parole ! ouvre : douze mondes (les huit gratuits : Pochade, Touffe, Brouillamini, Halin, Esquille, Tesselle, Braille,
  Buvard) ; les cinq réglages d'une parole (récurrence, rappel, importance, mémoire, couleur) ; l'autre moitié de la Toile (ce que
  tes proches tiennent envers toi) ; les paroles en l'air et l'heure des notifications ; les couleurs du dessin (v133, C-061).
- Les murs : un flou de 4,8 px, une phrase, l'offre (CLAUDE.md v104–v105, v133).
- Un monde devenu payant reste à qui l'utilisait (Q339, fait en v73). Payer sans compte est permis, prévenu deux fois (Q326).

**Ce qui manque pour construire**
- **L'essai de 14 jours** : n'est écrit que comme une mention (« essai 14 jours ») et un bouton principal. Offre d'introduction
  StoreKit (gratuite 14 jours puis 39 € / an) ? Vaut-elle aussi pour le mensuel ? Que voit-on à J-2, à la fin, après un essai déjà
  consommé (StoreKit ne l'offre qu'une fois par groupe d'abonnement) ?
- **Les produits** : identifiants, groupe d'abonnement, passage du mensuel à l'annuel, prix hors zone euro (le texte « 39 € » et
  « soit 3,25 €/mois » est en dur : StoreKit rend un prix localisé — le « soit … /mois » doit être calculé).
- **Le design à 2 €** : achat non consommable par monde (douze produits) ? Que devient-il quand on prend Ma Parole ! ensuite, puis
  qu'on la quitte ? Peut-on en adopter plusieurs ? La palette est-elle comprise ?
- **La restauration** : obligatoire pour l'App Store ; ni bouton, ni mot, ni place.
- **Payer sans compte** (C-035) : avec StoreKit, un achat est lié à l'identifiant Apple, pas à l'app — il se restaure sur un autre
  téléphone du même identifiant. **Le texte « si tu en changes ou supprimes l'app, il est perdu » est alors faux** tel qu'écrit ; ce
  qui serait perdu, c'est la Toile (locale), pas l'achat. Les deux mots sont à reprendre avec ce fait.
- **La fin de l'abonnement** : que deviennent les paroles réglées avec des réglages payants (récurrence, couleur libre), les dalles
  plantées dans un monde payant (Q339 répond pour le monde ; pas pour les réglages), les traits de couleur d'un dessin ?
- **Les états d'achat** : en attente (Demander à acheter), échec, remboursement, période de grâce, partage familial — aucun écran.
- **L'écran de gestion** (« Tu es Membre Ma Parole ! ») : son contenu, le lien vers la gestion des abonnements.
- **Les mentions exigées près du bouton** (durée, renouvellement automatique, liens vers les conditions et la confidentialité) :
  la page porte « Sans engagement · résiliable à tout moment » seulement — et les deux pages légales sont « bientôt disponibles » (§6).
- **Un Cercle à plusieurs** : un réglage payant posé par un membre vaut-il pour les autres ?

**Questions à poser à Tom**
1. L'essai : 14 jours gratuits puis l'annuel, automatiquement ? Aussi sur le mensuel ?
2. Le design à 2 € : un achat par monde, gardé pour toujours ? Avec sa palette ?
3. Où vit « Restaurer mes achats » (Réglages, page de l'offre, les deux) et quels mots ?
4. À la fin de Ma Parole ! : les réglages déjà posés restent-ils (figés), ou s'éteignent-ils ?
5. « Payer sans compte » : réécrire les deux textes sachant que l'achat suit l'identifiant Apple ?
6. Les prix hors euro : laisser StoreKit décider par palier ?

---

## 5 · VoiceOver de la Toile

**Ce que le prototype fait**
- La Toile est UN canevas : une dalle n'est pas un nœud. On la touche par `Toile.hit(x, y)`, qui rend la parole sous un point.
  Pour un lecteur d'écran, la Toile est une image muette.
- 47 `aria-label` dans `app.html`, sur des boutons et des commandes ; le mot « VoiceOver » n'y figure que pour la vue d'une photo en entier.

**Ce qui est décidé** — des annonces ponctuelles, et un principe :
- « Mode nuit, activé / désactivé » (v118, coupé) ; « Voir la photo en entier » / « Voir le dessin en entier », seulement quand la
  bande porte une photo ou un dessin (C-051) ; « Quitter le dessin » (C-056) ; VoiceOver sur chaque outil du dessin (`redteam_dessin`, E).
- CLAUDE.md §11 : **VoiceOver ne se dégrade jamais** ; la lisibilité et Dynamic Type non plus.
- C-026 : « Avant Swift : […] VoiceOver de la Toile » — OUVERT, sans contenu.

**Ce qui manque pour construire**
- **Comment la Toile s'annonce** : rien. Faut-il un élément d'accessibilité par dalle (un `accessibilityElement` par cellule, avec sa
  forme pour le focus), dans quel ordre de lecture (la Toile n'a ni lignes ni colonnes : par date, par proximité, par état ?) ; que
  dit une dalle (titre, à qui, état, échéance, nature) ; que dit une cellule vide ; que dit la dalle d'un Cercle (« le potager, Cercle, 9 paroles ») ?
- **Les gestes** : le trait à tracer pour tenir une parole n'a pas d'équivalent accessible décidé (une action personnalisée « Tenir » ?
  c'est toucher au principe « un geste tracé, pas une case à cocher » — une décision de produit, pas de portage). Idem le zoom, le
  double toucher, l'appui long du Studio, le dessin, la caresse de la Pelote.
- **Les autres surfaces peintes** : la Pelote et ses îles (chaque île est une parole tenue, qui ouvre sa fiche au toucher), les Noyaux
  (un anneau à trois arcs : il porte des proportions), les dalles des cartes de l'Index et du Fil, le Folio, un dessin (une liste de traits).
- **Les murs** : un réglage flouté « sans explication » — que dit VoiceOver ? Et la phrase qui monte, puis l'offre qui s'ouvre ?
- **Ce qui bouge seul** : la vie au repos, le souffle de la Pelote — silencieux pour VoiceOver ? (« Réduire les animations » les fige, c'est décidé.)
- Les rotors, les intitulés des écrans, l'ordre du focus dans une fiche ; Contrôle de sélection, Contrôle vocal.

**Questions à poser à Tom**
1. Que dit une dalle ? (Proposition à lui faire valider mot pour mot, dans le lexique : nature, titre, à qui, état, date.)
2. Dans quel ordre VoiceOver parcourt-il la Toile ?
3. Tenir une parole sans tracer : une action « Tenir » pour VoiceOver seulement — oui ou non ?
4. Que dit un mur de Ma Parole ! ?
5. La Pelote : une seule annonce (« ta Pelote, n paroles tenues »), ou une par île ?

---

## 6 · Les pages légales

**Ce que le prototype fait** : dans les Réglages, le groupe « Légal » porte « Conditions d’utilisation », « Politique de
confidentialité » et « À propos ». Les deux premières ouvrent une page dont le texte est **« bientôt disponible »** (`_v16Legal`,
commentaire : « les deux textes légaux “bientôt disponibles” »). L'écran de connexion écrit « En continuant, tu acceptes les
Conditions et la Politique de confidentialité » — avec deux liens vides (`href="#"`). « À propos » est écrit (le texte de Tom, les
deux polices créditées).

**Ce qui est décidé** : les mentions légales de l'onboarding restent en Atkinson 12 px (v127). C-025 : « Avant publication :
PromiLate, Gilbert, pages légales, version » — OUVERT. Rien d'autre.

**Ce qui manque pour construire** : les deux textes ; l'éditeur (raison sociale, adresse, contact) ; l'âge minimal ; le droit
applicable ; la politique de confidentialité au sens du RGPD (données collectées, finalités, durée, sous-traitants : Firebase, Apple) ;
les « étiquettes de confidentialité » de l'App Store ; l'URL publique exigée par l'App Store pour chacune des deux pages ; le
consentement au suivi s'il y en a ; les conditions de l'abonnement (renouvellement, résiliation) ; ce que vaut « Pas de pub ».

**Questions à poser à Tom**
1. Qui rédige (un juriste est déjà attendu pour les polices, Q295) et pour quand ?
2. Les textes vivent-ils dans l'app, ou sur une page web ouverte depuis l'app ?
3. Âge minimal ?

---

## 7 · Le numéro de version

**Ce que le prototype fait** : `window.PROMI_VERSION = '0.16'`, affiché « Promi · 0.16 » dans « À propos ». Les lots, eux, se
numérotent v1 à v134 ; `serveur.py` rend le commit servi (`/version.json`).

**Ce qui est décidé** : rien. ETAT-DES-LIEUX : « à fixer — le numéro de version (“Promi · 0.16”) », Q294 ; C-025.

**Ce qui manque** : le schéma (version de mise en vente et numéro de build), le numéro de la première version publiée, ce que
montre l'app (la version seule, ou le build), et le lien entre un build et un chantier validé.

**Question à poser à Tom** : la première version publiée s'appelle-t-elle 1.0 ? Affiche-t-on le build ?

---

## 8 · Les polices

**Ce que le prototype fait** — trois polices, cinq faces (CLAUDE.md §6, 22 sept.) : Gilbert 700 · Atkinson Hyperlegible Next
400 · 500 · 700 · PromiLate 400. Métriques des faces calées par `ascent-override` / `descent-override` / `line-gap-override` ;
agrandissement de 12 % par `size-adjust` (v96). `✕ ✦ ● ‹ › →` viennent de la police du système. « À propos » crédite Atkinson
(Braille Institute) et Gilbert (Type With Pride, en hommage à Gilbert Baker).

**Ce qui est décidé**
- Gilbert : sous-titres, libellés, navigation, en capitales ; **CC BY-SA 4.0 — le crédit est OBLIGATOIRE dans « à propos », les
  glyphes ne peuvent pas être modifiés** (CLAUDE.md §6, 16 sept.). Le fichier dit CC BY-SA 4.0 en trois endroits (LICENSE.txt, README,
  table `name`) ; copyright Ogilvy & Mather ; version « Preview5 » ; **notre WOFF2 est une conversion à nous** (277 glyphes intacts).
- Atkinson : SIL OFL 1.1, © 2020, 2024 Braille Institute, noms réservés ; nos trois WOFF2 sont les officiels, octet pour octet ;
  l'OFL compte « changer de format » comme une modification — ne jamais reconvertir soi-même.
- PromiLate : titres d'écran, mot-marque, phrases du trait ; une seule graisse ; `font-synthesis:none`.
- Aucune graisse hors des faces embarquées : en Swift une face absente casse (`redteam_polices`).
- Les titres de page en capitales PromiLate, sauf « Le studio » (Q319).

**Ce qui manque pour construire**
- **PromiLate — les droits** : « PromiLate n'a aucune métadonnée de licence — d'où vient-elle, et sous quels droits ? » (Q295,
  « pour le juriste, avant publication » ; C-025). Sans réponse, l'app ne peut pas être publiée avec elle.
- **PromiLate — les capitales accentuées** : la police porte 66 glyphes — ni capitales accentuées, ni `à è ç ô`, ni `→`. Aujourd'hui :
  les É des titres sont COMPOSÉS (le E et l'apostrophe de PromiLate posée en accent, Q319) ; quatre phrases du trait ont été
  reformulées pour éviter un accent (Q291) ; « PARTAGER MA PELOTE » est écrite sans capitale accentuée ; **un prénom accentué tombe
  en Gilbert dans une phrase du trait** (vu, non réglé). En Swift, la substitution se fera vers une autre police de secours : le
  défaut changera de visage. Il faut ou des glyphes ajoutés (qui dessine ? avec quels droits ?), ou une règle de repli écrite.
- **Gilbert — le format** : il faut un `.otf`/`.ttf` dans le paquet iOS. Reprendre le fichier d'origine du zip (pas notre WOFF2) règle
  la question de la conversion. **Le chiffrement de l'App Store face au CC BY-SA** (pas de verrou technique ajouté à l'œuvre) est une
  question de juriste (Q295). « Preview5 » : une version finale existe-t-elle ?
- **Gilbert — le crédit** : il EXISTE dans le prototype, à reprendre mot pour mot — le texte d'« À propos » nomme Type With Pride et
  Gilbert Baker, et un bloc de licences (`app.html` l. ≈ 35861) porte le copyright Ogilvy & Mather, les dessinateurs (Robyn Makinson,
  Kazunori Shiina, Hayato Yamasaki) et la mention « Creative Commons Attribution – Partage dans les mêmes conditions » ; l'OFL
  d'Atkinson y est dépliable. Ce qui manque : sa place en Swift (dans « À propos », ou une page « Licences »), et l'avis du juriste.
- **Atkinson — le format** : prendre les `.otf`/`.ttf` officiels du même zip ; joindre le texte de l'OFL.
- **Les métriques** : `ascent-override`, `size-adjust` n'existent pas en UIKit / SwiftUI. Les cotes « à l'encre » du prototype
  supposent ces réglages : en Swift, la taille du point et l'interligne devront être recalculés face pour face (hauteur de capitale et
  largeur rendues, pas la taille déclarée — CLAUDE.md §8).
- **Les sept niveaux de texte** du JSON ne sont pas câblés (DETTE, F-01) : la table qui fait foi reste à écrire.
- **Les six symboles** `✕ ✦ ● ‹ › →` : tracés à soi ou symboles du système ?

**Questions à poser à Tom**
1. D'où vient PromiLate, qui l'a dessinée, sous quels droits ? Peut-on y ajouter les capitales accentuées et les minuscules manquantes ?
2. En attendant : un prénom accentué dans une phrase du trait — quelle police prend le relais ?
3. Le juriste a-t-il rendu son avis sur Gilbert (CC BY-SA dans une app chiffrée de l'App Store) ?
4. Le crédit de Gilbert : le texte complet dans « À propos », ou sur une page « Licences » à part ?

---

## 9 · La page du trait partagé (C-023)

**Ce que le prototype fait** : rien qui porte ce nom. Ce qui s'en approche : l'instant « l'autre moitié arrive » d'une parole
promise à quelqu'un (simulé, §3) ; le rond Partager d'une fiche, qui ouvre Mon Folio réduit à cette parole (v117) ; le concept du
trait de validation personnalisé (C-045, `TRAIT-PERSONNALISE-CONCEPT.md`, rien de construit, quatre décisions en attente).

**Ce qui est décidé** : rien. C-023 : « Page du trait partagé. » — OUVERT, sans preuve, sans juge, « à fixer » (liste de Tom, 4 oct.).

**Ce qui manque** : sa définition même. ⚠ TROU : aucun document du dépôt ne dit ce qu'est « la page du trait partagé » — la page où
l'autre trace sa moitié (dans l'app ? sur le web, pour quelqu'un qui n'a pas l'app ?), une page de partage du trait tracé, ou autre chose.

**Questions à poser à Tom**
1. Qu'est-ce que la page du trait partagé : là où l'autre trace sa moitié ? Vit-elle dans l'app, sur le web, les deux ?
2. Dépend-elle du trait personnalisé (C-045) ?

---

## 10 · Le Zzz (C-012)

**Ce que le prototype fait** : tout le mécanisme existe (`lot-V118-ZZZ`) et il est **coupé** : `COUPE=true` — ni thème de nuit, ni
cran de nuit, quels que soient le réglage mémorisé, `?zzz=1` ou `?nuit=1`. Le bouton « Zzz » n'a jamais été posé (`BOUTON_POSE`).
`redteam_nuit` est rouge par décision.

**Ce qui est décidé** (v118, puis coupé en v120 « jusqu'à nouvel ordre »)
- La raison : l'éblouissement, pas la teinte ; aucune permission de localisation (le soleil se calcule aux coordonnées de référence
  du fuseau ; inconnu : 22 h – 7 h). La table des cinq cas (premier lancement clair + Zzz activé ; clair + Zzz : sombre de nuit du
  coucher + 1 h au lever ; sombre + Zzz : le cran de nuit ; etc.). Jamais de bascule sous les yeux, pas de fondu. Le cran de nuit :
  neutres clairs à OKLCH L − 0,06, teinte gardée (`#F7F0DE` → `#E3DCCA`), le reste au hex près, contraste ≥ 7:1, aucun filtre.
- Le bouton s'écrit « Zzz », au Studio, au milieu de la ligne SOMBRE / AVEC TEXTE ; VoiceOver « Mode nuit, activé / désactivé ».
- **La casse du Studio qui a fait couper** (v120) : activé au premier lancement, la nuit l'app passait en sombre quel que soit le
  choix, les disques SOMBRE / CLAIR ne changeaient plus rien, et le disque allumé contredisait le choix.

**Ce qui manque pour construire**
- **La place du bouton** : la ligne ne reçoit pas un troisième disque sans écarter ses voisins (56 entre les paires, il en faudrait
  84 — Q369, planche `planche-v118/planche-zzz.png`).
- **L'interaction avec le choix SOMBRE / CLAIR** : c'est le défaut de v120 ; la règle qui le lève n'est pas écrite (que montre le
  disque quand la nuit a pris la main ? un choix fait de nuit s'applique-t-il tout de suite ?).
- **Le thème du téléphone** : v118 décide que l'app ne suit plus le thème du système (elle remplace Q301). À confirmer pour iOS, où
  l'utilisateur s'attend à ce qu'une app suive le mode sombre du système.
- « Au changement d'écran ou au retour au premier plan » : en SwiftUI, la définition d'un « changement d'écran » (une feuille, une
  couverture, un onglet) est à écrire.

**Questions à poser à Tom**
1. Le Zzz fait-il partie de la première version Swift, ou reste-t-il coupé ?
2. S'il revient : où tient le bouton, et que montre SOMBRE / CLAIR pendant la nuit ?
3. L'app ignore-t-elle le mode sombre du système, comme v118 le décide ?

---

## 11 · La dégradation adaptative

**Ce que le prototype fait** : un seul régulateur, celui de la Pelote — six paliers de densité (220 000 · 180 000 · 150 000 ·
110 000 · 90 000 · 75 000 poils ; v124), appliqués quand on quitte l'écran, jamais sous les yeux ; à 110 000 et en dessous le poil
reprend l'épaisseur et le reflet de la densité 1. Madrure a un secours processeur quand la carte graphique refuse. Deux planchers de
cadence assumés pendant une plantation (Chamade 51–52 images/s, Guingois 39–44 ; Q341).

**Ce qui est décidé** (CLAUDE.md §11, Tom, 30 sept. — « rien à implémenter »)
- Promi n'ajoute aucun plancher d'appareil (iOS 26 fixe le sien à l'iPhone 11) ; la qualité s'adapte.
- **Ne se dégrade jamais** : le geste (tous les `coalescedTouches`, le trait dans la trame du toucher, pleine résolution) · les
  couleurs (hex exacts) · la lisibilité (texte natif, contrastes, tailles, Dynamic Type) · la composition de la Toile (toutes les
  dalles, mêmes positions) · VoiceOver.
- **Peut se dégrader**, du moins visible au plus visible : le nombre de dalles animées, les transitions de navigation, la complexité
  des mondes, la densité de la Pelote.
- « L'ordre, les paliers et les seuils seront fixés par mesure Instruments sur appareil, au premier lot Toile du portage. **Aucun
  chiffre n'est décidé à ce jour : n'en invente pas, n'en implémente pas.** »
- « La fluidité passe avant la densité » (Q378, v124).

**Ce qui manque pour construire** : tout ce qui est chiffré — l'ordre exact des renoncements, les seuils qui déclenchent un palier
(temps par image ? état thermique ? mode économie d'énergie ?), l'hystérésis (quand remonte-t-on ?), ce qu'est « un monde moins
complexe » monde par monde (aucun des vingt n'a de version allégée décrite), la liste des appareils de mesure, la cadence visée
(60 ou 120 images/s sur un écran ProMotion — le rapport v125 avance « 8 ms à 120 Hz », ce n'est pas une décision).

**Questions à poser à Tom** : aucune avant la mesure — c'est la décision. À lui montrer ensuite : la table mesurée, pour qu'il
tranche l'ordre des renoncements à l'œil. Une seule question préalable : **quels iPhone a-t-on sous la main pour mesurer** (un iPhone 11
est le plancher ; Tom teste sur un iPhone 16e) ?

---

## 12 · L'iPad, l'orientation, les tailles d'écran

**Ce que le prototype fait** : un cadre fixe de **390 × 844** (`#device`), mis à l'échelle par transformation pour tenir dans la
fenêtre. Toutes les cotes sont absolues dans ce cadre. `redteam_marges` passe aussi 375 × 667 et un profil iPhone réduit — pour un
seul écran (les phrases suggérées). Les chiffres de l'Aura finissent à 782 sur 844 (composition B) : « un iPhone plus court que 844 pt la coupera » (ETAT-DES-LIEUX, liste « à valider sur iPhone », v123).

**Ce qui est décidé** : rien sur l'iPad, rien sur le paysage. Sur les tailles : « ces écrans ont été composés pour tenir en un
écran » (v102) ; l'Aura défile sous son plateau si l'air ne tient plus (§8) ; le mode dessin compte jusqu'au « bord bas utile »
(`SECU_BAS` 34 ; A-INTEGRER : `safeAreaInsets.bottom`).

**Ce qui manque pour construire**
- **La règle d'adaptation** : que devient une cote absolue de 390 × 844 sur un écran de 375 × 667 (iPhone SE), 393 × 852, 402 × 874,
  430 × 932, 440 × 956 ? Mise à l'échelle uniforme (comme le prototype — mais le texte rétrécit, contre Dynamic Type) ; cotes fixes et
  air qui absorbe ; ou une règle par écran ? Aucune n'est écrite. La Toile, elle, a une largeur de référence de 390 dans `banc_rendu`.
- **Les zones sûres** : encoche, île dynamique, indicateur d'accueil — le plateau est à y 40, la barre à 736 → 824 : calés sur
  quoi ? Une seule cote en parle (le dessin).
- **L'orientation** : rien. (Verrouiller en portrait est la lecture la plus sobre ; ce n'est écrit nulle part.)
- **L'iPad** : rien — ni « iPhone seulement », ni mise en page.
- Le clavier qui monte (la page + compte sur un écran entier), Split View, Stage Manager : rien.

**Questions à poser à Tom**
1. iPhone seulement, portrait seulement, pour la première version ?
2. Sur un écran plus petit ou plus grand que 390 × 844 : on met tout à l'échelle, ou on garde les tailles et on laisse l'air bouger ?
3. Le plus petit iPhone à tenir (iOS 26 : l'iPhone 11 en 414 × 896 ; les SE récents en 375 × 667) ?

---

## 13 · Dynamic Type

**Ce que le prototype fait** : rien. Les tailles sont en pixels fixes ; un plancher à 12 px (§6), relevé en ligne par `echelle()` à
13 ; un agrandissement général de 12 % (v96) a resserré 609 paires de textes et coûté les « pertes d'air assumées » de v102. Un essai
de facteur global (×1,08) avait resserré 156 paires (« grossir le texte = un plancher, jamais un facteur », mémoire du projet).
Plusieurs textes s'auto-dimensionnent pour tenir (la phrase de la page +, les titres des cartes, les titres d'écran).

**Ce qui est décidé** : CLAUDE.md §11 range Dynamic Type parmi ce qui **ne se dégrade jamais** — c'est sa seule mention. Rien en
dessous de 12 px, aucune opacité sous 72 % sur du texte lisible (§6). Les écrans de la page + ne défilent pas (v102).

**Ce qui manque pour construire** : la contradiction n'est pas levée — des écrans « composés pour tenir en un écran », en cotes
absolues, où 12 % de plus ont déjà coûté de l'air, face à un réglage système qui va jusqu'à +200 % et plus (tailles d'accessibilité).
Il faut : quels textes suivent Dynamic Type (tous ? le texte courant en Atkinson seulement, pas les titres PromiLate ni les libellés
Gilbert ?), jusqu'à quelle taille, ce qui cède quand ça ne tient plus (l'écran défile ? le texte passe à la ligne ? — la page + « ne
défile pas » par décision), et le sort des textes auto-dimensionnés et des textes peints dans un canevas (titres des dalles sur la Toile).

**Questions à poser à Tom**
1. Dynamic Type : pleinement (les écrans défilent quand il le faut), borné (jusqu'à une taille), ou sur le texte courant seulement ?
2. La page + peut-elle défiler aux grandes tailles, contre la décision de v102 ?

---

## 14 · La localisation (« La langue »)

**Ce que le prototype fait** : un écran « La langue » existe (`#langScreen` : « Promi te parle dans la langue que tu choisis. » ;
« Le vocabulaire de Promi — Promi, Toile, Cercle, Fil, Aura — ne se traduit pas : c'est le même partout. »). **Sa rangée dans les
Réglages est masquée** (`#langCard`, `hidden`, `display:none`). L'app est en français, les textes en dur dans le code ; les dates
(« mercredi 14 », « 3 AOÛT »), l'élision « de / d’ », les prix (« 39 € ») sont écrits pour le français.

**Ce qui est décidé** : le vocabulaire est invariable et ne se traduit pas (CLAUDE.md §2 ; le texte de l'écran). « Une application
mobile française » (§1). Rien sur une autre langue.

**Ce qui manque pour construire**
- ⚠ TROU : **pourquoi la rangée « Langue » est masquée** — la règle du §9 (« avant de démasquer, chercher pourquoi ») s'applique ;
  la décision qui l'a masquée n'a pas été retrouvée dans ce relevé.
- Français seulement à la sortie ? Si oui, l'écran « La langue » se porte-t-il ?
- Si d'autres langues : la phrase de la page + est une GRAMMAIRE française (« Je me promets de… », élision, « à Rachel ») ; les
  18 phrases des murs, les suggestions, les textes des notifications sont des jeux de mots français ; PromiLate n'a pas les glyphes
  accentués (§8). Rien n'est prêt pour une traduction.
- Le format des dates et des nombres (région du téléphone), l'accord (« TENU » / « TENUE »), le tutoiement.

**Questions à poser à Tom**
1. La première version est-elle en français seulement ? Alors l'écran « La langue » disparaît-il ?
2. Les dates suivent-elles la région du téléphone ou restent-elles en français ?

---

## 15 · L'export et la suppression du compte

**Ce que le prototype fait**
- **Supprimer mon compte** (`_v16SupprimerCompte`) : une confirmation « Supprimer ton compte ? · Tous tes Promi seront effacés de cet
  appareil. · Supprimer / Garder », puis `localStorage.clear()` et rechargement. Il n'y a pas de compte à supprimer : c'est un
  effacement local. La rangée est en `#DD4D23` (C-015).
- **Réinitialiser mes données · effacer** ; **Sauvegarde locale · vérification…** ; **Se déconnecter** (point de branchement vide).
- **Exporter** : rien. Les seules sorties sont des images (le partage : Ma Toile, Mon Folio, la Pelote).

**Ce qui est décidé** : les mots de la confirmation existent (Q294, « mots neufs » — à trancher). « Tes Promi perso restent sur ton
appareil. » Rien d'autre.

**Ce qui manque pour construire**
- **La suppression réelle** : l'App Store exige qu'un compte créé dans l'app puisse y être supprimé. Que deviennent, côté serveur, les
  paroles promises à d'autres, les moitiés de trait déjà données, ma place dans un Cercle, les dessins communs, mes photos ? Délai,
  confirmation, révocation du jeton « Se connecter avec Apple » ; l'abonnement n'est PAS résilié par la suppression (à dire à l'utilisateur).
- **La différence entre les trois rangées** (se déconnecter, réinitialiser mes données, supprimer mon compte) une fois qu'un vrai compte existe.
- **L'export** (droit à la portabilité, RGPD) : format, contenu (paroles, dates, états, Cercles, dessins en liste de traits, photos), où le demander.
- **La sauvegarde** : « Sauvegarde locale · vérification… » — que vérifie-t-elle en Swift ? iCloud (sauvegarde de l'appareil) suffit-il
  pour qui n'a pas de compte ?

**Questions à poser à Tom**
1. Supprimer son compte : que voit l'autre, pour une parole que je lui avais promise ?
2. Un export « mes paroles » : oui, sous quelle forme (un fichier lisible, une image, les deux) ?
3. Sans compte, la Toile est-elle sauvegardée par iCloud avec l'appareil ?

---

## 16 · L'archive (C-026)

**Ce que le prototype fait** : rien qui s'appelle « archive ». Une parole est à tenir, en cours, tenue, gardée de côté, ou retirée
(« Supprimer ce Promi »). Une parole tenue reste sur la Toile et dans « Ce que tu as tenu ». Un Cercle se dissout (« DISSOUDRE »).

**Ce qui est décidé** : rien. C-026 : « Avant Swift : archive, VoiceOver de la Toile, StoreKit, Firebase. » — OUVERT (liste de Tom,
4 oct.), un mot sans définition. Décisions voisines : une Toile tient un nombre illimité de paroles (v98) ; les titres s'effacent
sous 48 px à l'écran ; C-062 (les tailles deviennent monotones au-delà de 7 à 9 dalles) est en cours.

**Ce qui manque** : ⚠ TROU — aucun document ne dit ce qu'est « l'archive » : ranger les paroles tenues hors de la Toile ? ranger une
année ? un Cercle terminé ? la Toile d'avant un « Retourne ta Toile » ? Et ce que cela fait à l'Aura (la Pelote et ses îles sont les
paroles tenues), aux Noyaux, à la réciprocité, au partage.

**Questions à poser à Tom**
1. Qu'est-ce qu'on archive, et pourquoi (la Toile trop pleine, une page qu'on tourne) ?
2. Une parole archivée reste-t-elle une île de la Pelote ?

---

## 17 · Liste des trous

- ⚠ TROU (§1) : la règle « la veille seulement si la parole a été vue avant » — décision ou artefact du prototype.
- ⚠ TROU (§1) : aucune décision sur ce qu'ouvre le toucher d'une notification, ni sur l'état « permission refusée par iOS ».
- ⚠ TROU (§2) : aucune décision d'haptique, aucune vibration jamais éprouvée sur iPhone (l'API du prototype n'existe pas sur iOS).
- ⚠ TROU (§3) : aucun modèle de données partagé, aucune règle de conflit, aucun écran hors ligne ou d'erreur.
- ⚠ TROU (§3) : la modération et le blocage ne sont évoqués nulle part.
- ⚠ TROU (§4) : « Restaurer » n'existe nulle part ; l'essai de 14 jours n'a pas de mécanique ; le texte de l'achat sans compte contredit le fonctionnement de StoreKit.
- ⚠ TROU (§5) : rien n'écrit comment la Toile, la Pelote, un Noyau ou un dessin s'annoncent ; rien sur un équivalent accessible du trait.
- ⚠ TROU (§6) : les deux textes légaux n'existent pas ; aucun éditeur, aucun âge minimal.
- ⚠ TROU (§7) : aucun schéma de version.
- ⚠ TROU (§8) : l'origine et la licence de PromiLate ; l'avis du juriste sur Gilbert (CC BY-SA × chiffrement de l'App Store, Q295) ; les métriques des faces (`ascent-override`, `size-adjust` de 112 %) n'ont pas d'équivalent décidé en Swift.
- ⚠ TROU (§9) : « la page du trait partagé » n'est définie dans aucun document.
- ⚠ TROU (§10) : la règle qui lève la casse du Studio de v120 (Zzz contre SOMBRE / CLAIR) n'est pas écrite.
- ⚠ TROU (§11) : aucun chiffre, par décision ; aucune version allégée d'un monde n'est décrite.
- ⚠ TROU (§12) : aucune règle d'adaptation aux tailles d'écran, rien sur l'iPad ni sur l'orientation, les zones sûres ne sont cotées que pour le dessin.
- ⚠ TROU (§13) : Dynamic Type est déclaré intouchable sans une ligne sur sa mise en œuvre.
- ⚠ TROU (§14) : la raison du masquage de la rangée « Langue ».
- ⚠ TROU (§15) : la suppression d'un vrai compte, l'export.
- ⚠ TROU (§16) : « l'archive » n'est définie dans aucun document.
