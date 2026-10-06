# portage/ — le dossier de portage de Promi (C-021, lot v134, 6 octobre 2026)

L'app Swift sera reconstruite à partir de zéro, **à partir de ce dossier seul**, sans relire `app.html`. Tout ici est **lu et extrait** du
prototype (`app.html`, `promi-moteur.js`), de ses juges et de ses documents de décision ; **rien n'a été modifié dans le produit**.
Rien n'y est inventé : ce qui manque est écrit « ⚠ TROU », avec ce qui a été cherché. Chaque affirmation porte sa source.

**Comment c'est fait, et sa limite.** Les dix documents ont été extraits par lecture de la source (recherches ciblées, extraction par
programme pour les tables) ; **aucun n'a été vérifié à l'écran**, et aucun juge n'a été relancé pour eux. Les numéros de ligne cités sont
ceux de la copie de travail du 6 octobre 2026 (v134) : ils servent à retrouver, pas à porter. En cas de désaccord, l'ordre des sources du
projet reste : `ETAT-30-SEPTEMBRE-2026.md` → `PROMI-TOKENS.json` → `CONTRAT-MONDE.md` → `SPEC-JUGES.md` → `CLAUDE.md` (les blocs datés
les plus récents corrigent les plus anciens).

## Table des matières

| n° | Document | Ce qu'il contient |
|---|---|---|
| 1 | `SPEC-DONNEES.md` · `SPEC-DONNEES.schema.json` | Chaque entité (Promi, Chiche, Cercle, personne, gardé de côté, dessin, photo, réglages, achats) : champs, états, transitions et leur déclencheur ; JSON Schema (27 définitions, `x-transitions`) ; ce qui ATTEND FIREBASE (§12), dont le dessin commun et le masquage individuel |
| 2 | `SPEC-ECRANS.md` | Vingt-six écrans : accès, éléments, actions, états vides et d'erreur, textes exacts |
| 3 | `SPEC-GESTE.md` | Planter, tenir, tracer sa moitié, dessiner, et les gestes de navigation : géométrie, seuils, horodatages ; ce qui doit être lu avec `UITouch.timestamp` et `coalescedTouches` (§7) |
| 4 | `SPEC-RENDU.md` | L'interdiction (jamais de capture de Toile à la place d'une dalle), la Toile, les vingt mondes (renvoi à `CONTRAT-MONDE.md`), la Pelote, la vie au repos (quatre mondes reportés à Swift), les paliers qu'on peut dégrader (principe, sans chiffre), le banc de rendu |
| 5 | `JETONS.json` · `JETONS.md` | Couleurs, typographie, espacements, rayons, palettes, seuils ; les 85 décisions de couleur de Tom (tableau de `redteam_decisions`) ; dix-huit exceptions nommées |
| 6 | `TEXTES.json` · `TEXTES.md` | 330 clés, 967 chaînes, variantes, gabarits, VoiceOver ; les dix-huit phrases des murs et leurs mots en orange ; 38 clés « à confirmer » |
| 7 | `REGLES.md` | Cent règles vérifiables (R-001 à R-100) : la grille anti-coercition (reconstituée), les lois du dessin (dont la loi des points et son exception), le lexique |
| 8 | `TESTS.md` | Les 89 juges traduits en critères d'acceptation pour Swift : ce qu'il vérifie, sur quoi, avec quel seuil ; onze ne se portent pas |
| 9 | `DETTE.md` | Code mort, dettes nommées, faux positifs, rouges permanents, incohérences assumées, jetons sans consommateur, chantiers et questions ouverts — une ligne chacun, avec ce qu'il faut décider |
| 10 | `MANQUES.md` | Ce qu'aucune décision ne couvre : notifications, vibrations, Firebase, StoreKit, VoiceOver de la Toile, pages légales, version, polices, page du trait partagé, Zzz, tailles d'écran, Dynamic Type, langue, compte, archive |

`A-INTEGRER.md` (les notes prises de v126 à v133) est intégré dans les documents 1 à 5 ; il reste là comme journal.

## Les contradictions trouvées en écrivant le dossier (à trancher avant de coder)

- **La rotation de la Pelote** : `2π/100` dans l'app et dans `releve-aura.py` ; `2π/120` dans `CLAUDE.md` §7 (Q405).
- **Le prix d'un design** : 2 € au Studio (v118) ; « 1 €, ou 4 pour 3 € » encore sur l'écran de l'offre et dans l'ÉTAT.
- **`ETAT-30-SEPTEMBRE-2026.md` est en retard** sur le bleu (`#0E78F2`) et sur ce prix : c'est pourtant la première source de l'ordre.
- **Le fond sombre** : `#100D0B` dans le jeu de jetons et dans `Promi+Design.swift` ; seiche `#050302` à l'écran (v116, v121).
- **Le trait sur le lilas d'un Cercle** : `#43291C` dans le code, `#291547` à deux endroits de `CLAUDE.md`.
- **« Tenu » sur fond sombre** : amande `#8FE08F` (`CLAUDE.md`, 23 sept.) ; deux juges portent encore `#33BA6C`.
- **L'aide de l'Aura** dit « dans l'ordre où tu les as tenues » ; depuis v132 la plus récente est en premier.
- **À propos** dit « Les titres sont en Gilbert » ; ils sont en PromiLate, qui n'est pas créditée.
- **`SPEC-JUGES.md`** écrit « 21 phrases » ; elles sont dix-huit.
- **« Quatre mondes neufs »** dans `CLAUDE.md` ; `_NEUFS` en compte douze.
- **La grille anti-coercition** est citée (« la grille l'interdit ») mais n'est écrite nulle part comme une liste.
