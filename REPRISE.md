# REPRISE — pour une session neuve (15 nov. 2026, clôture du chapitre v197–v203)

À lire avec `CLAUDE.md` (il fait autorité), `CHANTIERS.md` (le registre) et `QUESTIONS.md`. En tête de chaque session : `python3 serveur.py` (port 8752, IP relue par `ipconfig getifaddr en0`), donner les trois adresses.

## a) L'état

- **Branche `main`, v203** — commit `__HASH__` (fusion de `v197` ; étiquettes `avant-fusion-v203`, `avant-q621`). Le serveur sert `main` ; `?diag=1` affiche la version en haut de chaque écran.
- **Le relevé des images ne tourne plus par défaut** : `?releve=1` (ou `?mesure=1`) le rallume ; `python3 resume_releve.py <fichier>` le lit (`mesures/`).
- **Le moteur (`promi-moteur.js`) reste en lecture seule.** Seule exception de ce chapitre, autorisée par Tom : Q621 (deux lectures du titre remplacées par la clé de plantation `p.cle`).
- **Validé par Tom dans ce chapitre** : le haut des fiches et la jonction du trait (C-255, C-259, C-263 à C-267), la page + et sa genèse (C-269, C-270, C-277, C-278), un seul langage de tracé (C-279), le guide (C-268, C-277), l'exemple qui revient (C-274 suite), le titre long de l'Index (C-276), le titre modifié dans l'Index et le Fil (C-280, en partie), Mascaret (C-272), l'Aura et la Pelote aux couleurs exactes (C-275), PromiLate gardé tel quel.
- **Livré à la clôture, à voir par Tom** : aucun encart pendant la modification d'un titre (C-280 §1), la dalle garde sa forme quand on renomme (Q621), les lettres qui clignotent en #82AEF8 exact (C-281).

## b) Ouvert ou reporté, par importance pour le produit (une ligne chacun)

1. **Fluidité sur l'iPhone** — une lettre tracée coûte ≈ 100 ms au fil principal (11 au banc) : vérifier l'ouvrier du tracé (`R.tl` dans le relevé, `?releve=1`) ; la préparation de la Pelote fait des blocs de 650 à 780 ms ; le flou d'« Adopte ce design » 571 ms. Objectif par animation : p95 < 16,7 ms, aucune image > 33 ms (non atteint).
2. **C-262** — la page s'est figée une fois après « tenir » (titre de cinq lignes, défilé puis revenu) : jamais reproduit ; la boîte noire (`promi_boite_noire`) est là pour le prendre.
3. **C-241** — sous Esquille et Tesselle, la dalle de la page + n'a pas la forme de la dalle vivante (le moteur pose la dalle par relâchement) : lot moteur.
4. **Q573, Q575** — Mascaret au Studio et le ressemis entre familles de semis : le coût est dans le moteur (lot moteur, après les testeurs).
5. **La référence de Ramage au banc de rendu** (C-187) — attend l'œil de Tom avant d'être refigée ; `banc_rendu` reste rouge sur Ramage seul.
6. **Q618 à Q620** — la Pelote en clair sous Ingénu (îles sous le plancher ΔE 15), la lumière du velours, la première lettre de la saisie : décisions de Tom.

## c) Les grands sujets pas commencés (ce qui dépend de quoi)

1. **Portage Swift** (`portage/`, dix documents, `PROMI-TOKENS.json` → `Promi+Design.swift`) — le socle de tout le reste. Avant lui : C-026 (archive, VoiceOver de la Toile, StoreKit, Firebase) et le banc de rendu comme référence au pixel.
2. **Invitations réelles par Firebase** (C-023, le Cercle et les parts à plusieurs, `p.parts`, `p.vuTenue`) — dépend du portage (comptes, réseau) ; le dessin collaboratif (C-093) en dépend aussi.
3. **Notifications et vibrations** (C-022) — le crochet `promiHaptique` est posé, vide ; Core Haptics et les notifications locales viennent avec Swift (Safari iOS ne vibre pas). La règle des notifications (§12, R-020 à R-026) est déjà écrite et jugée.
4. **Engagement E5 et E6** (C-079 phrases d'accueil ; C-080 E6A la Pelote qui s'enrichit, maquette d'abord ; C-081 E6B intégration après validation) — indépendants du portage, faisables dans le prototype ; C-082 « Délier » (issue d'un Promi jamais tenu) doit venir avant ou avec eux (la grille anti-coercition, critère 1).
5. **Android** — rien d'écrit : il suit le portage Swift (mêmes spécifications `portage/`, mêmes jetons).
6. **Avant publication** (C-025, C-090) — licences des polices (Gilbert CC BY-SA : crédit obligatoire), pages légales, prix de Ma Parole !.
7. **Dégradation adaptative** (CLAUDE.md §11) — à étalonner sur appareil, au premier lot Toile du portage.

## d) Les 143 chantiers « faits, en attente de Tom », par écran (pour les valider en bloc)

(Le registre en comptait 187 non validés : 143 faits et en attente, le reste ouvert, en cours ou reporté — section b et `CHANTIERS.md`.)

- **Onboarding et guide** : C-006, C-043, C-073, C-074, C-075, C-095, C-123, C-124, C-126, C-136, C-138, C-159, C-162, C-165, C-169, C-208, C-209, C-211, C-212, C-266.
- **Page +** : C-045, C-054, C-067, C-078, C-140, C-149, C-150, C-152, C-154, C-157, C-184, C-192, C-196, C-201, C-223, C-264, C-269.
- **Fiches, tenir, trait, commentaires** : C-007, C-046, C-048, C-050, C-051, C-059, C-069, C-077, C-084, C-085, C-091, C-096, C-098, C-101, C-111, C-118, C-128, C-160, C-189, C-193, C-194, C-197, C-199, C-207, C-210, C-242, C-246, C-248, C-253, C-254, C-255, C-257, C-280, C-281.
- **Toile, accueil et mondes** : C-009, C-016, C-028, C-049, C-058, C-062, C-070, C-087, C-099, C-119, C-121, C-131, C-187, C-188.
- **Aura et Pelote** : C-001, C-002, C-003, C-005, C-008, C-029, C-052, C-064, C-071, C-072, C-120.
- **Studio, Ma Parole !, achat** : C-004, C-010, C-055, C-057, C-061, C-063, C-092, C-100, C-170, C-175, C-190, C-198.
- **Index et Fil** : C-151, C-191, C-200, C-250, C-251, C-252, C-256.
- **Partager, dessin, photo** : C-042, C-056, C-060, C-068, C-086, C-097.
- **Réglages, veille, effacer** : C-104, C-195, C-249, C-258.
- **Règles et méthode (rien à voir à l'écran)** : C-015, C-021, C-030, C-044, C-047, C-053, C-065, C-066, C-102, C-103, C-114, C-130, C-137, C-178, C-179, C-202, C-204, C-206.
