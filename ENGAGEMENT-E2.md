# ENGAGEMENT — E2 et E2bis : compte rendu (v140, 10 oct. 2026)

> Chantiers C-075 (E2) et C-076 (E2bis). `ENGAGEMENT.md` corrigé par les amendements A2, A3, A6 et par les retours des testeurs de Tom
> (lot v140 §8). Juge : `redteam_e2.py`. **C'est un geste : la validation de Tom sur iPhone est obligatoire.**

## 1 · L'état des lieux de l'onboarding (E2, point 1)

| Étape d'avant (v20 → v139) | Décision | Ce qu'il en est aujourd'hui |
|---|---|---|
| Le prénom (« Toi, c'est … ? ») | **GARDER** (identification) | Inchangé. Il reçoit une sortie « Plus tard » (R6). |
| La parole et le trait, dans un écran propre à l'onboarding (« Je me promets de … », « trace pour planter ») | **REMPLACER** | La VRAIE page +, sur un Promi à soi, avec une phrase fantôme. |
| La plantation simulée (une dalle qui vole vers la Toile, la Toile « décor ») | **REMPLACER** | La plantation réelle : la parole a son id, elle compte partout. |
| Le message de fin (« C'est planté. » · « Ton premier Promi… » · « Primo… Deuxio… Tertio… » · « Le reste se découvre en traçant… ») | **SUPPRIMER** du parcours (c'est une étape qui explique) | Remplacé par l'étape du principe, AVANT le premier Promi, et par une ligne sur la fiche. ⚠ Ce texte avait été figé par Tom en v129 : il n'est plus affiché nulle part ; il reste dans `sauvegardes/app-avant-v140.html` et dans le bloc v129 de `CLAUDE.md`. |
| Le compte (« Garder ta Toile » · Apple · Google · « Plus tard ») | **GARDER** | Inchangé, proposé après la dernière ligne. |
| L'étape Studio | — | Il n'y en avait pas dans l'onboarding. |
| L'ancien tutoriel (`startTuto`, `OB[]`, `renderOb`) | — | Déjà retiré avant ce lot (`window._tutoSeen=true`, « l'app se découvre à l'usage »). |

Le code de l'écran « parole et trait » et du message de fin reste dans `lot-ONB-V20` (on ne nettoie pas) : plus rien ne l'appelle quand
`lot-E2` est chargé.

## 2 · Le parcours (E2, point 2)

| N° | Étape | Ce qu'on voit | Sortie |
|---|---|---|---|
| 0 | Le prénom | inchangé | « Plus tard » |
| 1 | **Le principe** | le titre, trois lignes, une ligne plus petite, un bouton | « Plus tard » |
| 2 | **La vraie page +** | « Je me promets de » + la phrase fantôme en pastille ; le trait ; rien d'autre (ni Peaufiner, ni pinceau, ni photo, ni retournement, ni « garder de côté ») | « Plus tard », ✕ Fermer |
| 3 | La plantation | l'animation existante ; la parole est réelle | — |
| 4 | **La fiche** | la fiche ouverte, une ligne dessous ; la main fantôme accompagne le trait | « Plus tard », ✕ Fermer |
| 5 | Tenir | le moment existant (E3 n'est pas livré) | — |
| 6 | **La dernière ligne** | une ligne, une fois ; un toucher n'importe où ferme ; `ob_fini` | ✕ Fermer, un toucher |
| 7 | Le compte | « Garder ta Toile » | « Plus tard » |

Compté par le juge, du principe au premier tenu : **2 touchers** (le bouton, la phrase fantôme) **et 2 traits** (celui qui plante, celui qui
tient). ⚠ La consigne dit « au plus 5 touchers et 1 trait » : dans Promi on plante en traçant, il y a donc deux traits — voir Q442.

## 3 · Les textes — TOUS PROVISOIRES, dans `TEXTES_ENGAGEMENT.e2` (`lot-E2`)

| Clé | Texte | D'où il vient |
|---|---|---|
| `titre` | Promi garde ta parole. | ENGAGEMENT.md, tel quel |
| `principe` (3) | Une promesse s'écrit en une phrase. · Elle se plante sur ta Toile, d'un trait du doigt. · Quand elle est tenue, un second trait le dit. | **écrit pour ce lot** (« une étape qui dit le principe simplement et clairement ») |
| `sous` | Une toute petite pour commencer, tenable tout de suite. | ENGAGEMENT.md « Commence par une toute petite… », réécrit sans impératif (A3) |
| `bouton` | C'est parti | ENGAGEMENT.md « Allons-y », réécrit (A3) |
| `plusTard` | Plus tard | ENGAGEMENT.md |
| `fantomes` (3) | boire un verre d'eau · ouvrir la fenêtre · m'étirer trente secondes | ENGAGEMENT.md |
| `fiche` | C'est planté. Une fois la chose faite, un trait suffit pour la tenir. | ENGAGEMENT.md « Fais-le. Puis reviens le tenir. », réécrit (A3 ; et « reviens » est un mot de R2) |
| `fin` | Tenu. La prochaine peut se dire à quelqu'un. | ENGAGEMENT.md « La prochaine, dis-la à quelqu'un. », réécrit (A3) |
| `studio` | Ta Toile peut changer de matière, au Studio. | **écrit pour ce lot** (« des invitations douces […] changer de monde au Studio ») |
| `toutAfficher` | Tout afficher · afficher › | A6 (« un réglage “Tout afficher” existe ») |

## 4 · E2bis — l'interface se dévoile (A6)

| Entrée de la barre | Paraît… | Vérifié par le juge |
|---|---|---|
| le + | toujours — seul au départ, dans un rond de 100 pt | oui |
| l'Index | à la première plantation | oui |
| l'Aura | au premier tenu ; la main fantôme la désigne (`aura-apparait`) | oui |
| le Studio | « juste après » : au premier retour sur l'accueil une fois l'Aura visitée (ou au lancement suivant) ; une ligne l'accompagne jusqu'au prochain toucher | oui |
| le Fil | à la première parole adressée à quelqu'un, ou reçue | oui |

Chaque entrée paraît **à sa place définitive** ; le fond de la barre s'étire jusqu'à elle (asymétrique tant que tout n'est pas là). Rien ne
disparaît. « Plus tard », à n'importe quelle étape, affiche tout. Un réglage « Tout afficher » (Réglages, au-dessus de « Revoir la
présentation ») tant que tout n'est pas affiché. **Qui n'a pas fait ce parcours — toute personne déjà installée — voit tout, comme avant** :
le dévoilement ne commence qu'au bouton du principe.

## 5 · Ce que chaque point de la consigne est devenu

| Point | État |
|---|---|
| E2 · 1 — état des lieux, tableau | **fait** (§1) |
| E2 · 2 — la nouvelle séquence | **fait** (§2) ; le moment « tenir » est celui d'aujourd'hui (E3 non livré) |
| E2 · 3 — « Plus tard » à chaque étape, un toucher, la Toile vide ; jamais redemandé | **fait** ; « l'écran vide de E4 » n'existe pas encore : c'est l'accueil d'aujourd'hui |
| E2 · 4 — la coloration progressive reste aux démonstrations | **fait** (ce parcours ne s'en sert pas) |
| v140 — une étape avant le premier Promi qui dit le principe | **fait**, texte provisoire |
| v140 — « TRACE POUR TENIR » et le trait plus visibles | **fait** : le mot passe de 15 à 19 px, les points à tracer de Ø 9 à Ø 12, vers le haut ; fiche et page + |
| v140 — des invitations douces (changer de monde au Studio…) | **fait pour le Studio** ; aucune autre invitation n'est écrite (E4 et E5 les portent) |
| v140 — une sortie « Plus tard » à chaque étape : R6 au vert | **fait** — `redteam_engagement` 11/11 |
| v140 — la main fantôme accompagne le premier trait | **fait** (planter, puis tenir) |
| A6 — E2bis | **fait** (§4) |
| Preuve : captures de chaque étape, clair et sombre | `planche-e2/`, `planche-v140/PLANCHE-8-e2-*.png` |
| Validation de Tom sur iPhone, parcours chronométré | **à faire par Tom** |
