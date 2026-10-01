# LE CERCLE — CARTE DE LECTURE (11 sept. 2026) — ⚠ LECTURE SEULE, RIEN N'EST ENCORE VÉRIFIÉ À L'ÉCRAN
Relevé par lecture du code (app.html, app `48b1a56b…`) et des documents, avant l'audit. Chaque ligne est une PISTE à
vérifier au doigt et à la capture — pas un constat. Numéros de ligne d'app.html au moment du relevé.

## 0 · Structure
`#device` l.2491–2685 ; hors `#device`, sous `.frame` : `#settingsScreen` (2715), `#studioScreen` (2729), **`#plusScreen`
(2734, la page du Cercle)**, `#personSheet` (2764)… → toute règle `#device …` / `.device.premium …` visant ces écrans est morte.

## A · Les écrans
- **A1 `#plusScreen`** (l.2734–2750) : « Le Cercle » · « Essaie tout, sans t'engager. » · « Tout Promi pour 3,99 €/mois,
  arrête quand tu veux. Ou prends l'année : 29 €, soit près de cinq mois offerts. » · 5 arguments (« La parole qu'on te
  tient », « Rappels intelligents », « Nuées illimitées », « Stats avancées », « Toiles signature ») · `#buyMonth` « Essayer
  14 jours, puis 3,99 €/mois » · `#buyYear` « Prendre l'année — 29 € » (« soit 2,42 €/mois · −39 % ») · « Sans engagement ·
  annulable en 2 taps » · « ou un design à l'unité — 1 €, ou 4 pour 3 € ». Visuel `#plHeroCv` (`drawCercleHero` l.6789).
  Ouverte par `ouvreCercle()` (l.3096). **Achat (l.3134) : `setPremium(true)`, toast, puis ouvre l'Aura — aucun paiement,
  aucune persistance.** Morts : `buildCercleHero` (vise `#plHero` absent), `drawCercleNoyau` (jamais définie).
- **A2 Réglages `#openPlusTop`** (l.2719) « ✦ Le Cercle / débloque tout Promi / essai 14 jours › » ; `cercleReglages()`
  (l.16427) : quatre réglages floutés (C'EST IMPORTANT ? · RÉCURRENCE chaque semaine · RAPPEL la veille à 19:00 · LA MÉMOIRE).
  Abonné : `cerclePaye()` (l.19955) masque l'encart → « ✦ Membre du Cercle ✓ » jamais visible ; réglages défloutés mais
  INERTES (`reg()` sans action). Aplat §3.8 écrit `#device #settingsScreen` → mort ; dégradé animé probable.
- **A3 Peaufiner d'un Promi / Chiche** : `cercle()` (l.16273) — « ✦ Le Cercle / importance, récurrence, rappels, mémoire »
  → `#openPlusTop.click()` → `ouvreCercle`. Pas sur une Nuée. Page + : CSS présent, montage JS non trouvé — à vérifier.
- **A4** ancien `.adv-prem` de `#dForm` (récurrence, rappel 07:00) sous `.adv-lock[data-cercle]` — probablement caché.
- **A5 Studio** : `#stLock` / `#stLockBuy` « Adopte ce design — 1 € » / `#stLockCta` « Ou débloque-les tous / avec Le
  Cercle » ; `world-locked` si `_lockW={sillons,gravure,terrazzo,eclats}` ∧ ¬`_ownedDesigns` ∧ ¬premium. Adoption 1 € :
  gratuite, non persistée. `_lockedWorld` jamais remis à zéro. Q117 (« ✦ Le Cercle / sillons, gravure, terrazzo »,
  « Adopte Terrazzo — 1 € ») NON appliqué.
- **A6** ancienne Aura (`#demoTg`, `prem-only`, `#karmaCercle` qui DONNE le Cercle) — masquée par `.au2` : morte.
- **A7 `#auraHelp`** (le « i » de l'Aura, vivant) : « Avec le Cercle » + `#ahCercleCta` + six cartes floutées à 7 px
  (double Noyau, proches, équilibre, disques, graphs par Nuée, Nuées illimitées & designs) — décrit l'ANCIENNE Aura (Q185).
- **A8** `.nqh-cercle` (Nuée) : mort (`#dpNuee` masqué). **A9 `#cercleTopBtn`** (barre du haut) : handler l.3177 ouvre la
  page SANS `ouvreCercle` ni `drawCercleHero` → visuel peut-être vide. **A10** fiche d'une personne : aucun mode Cercle.
- **A11** morts : `dp-cercle`, `#plusCta`, `#pplusBanner`, `#openPlus`, `.pplus-card`.

## B · Les portes (capture l.3113 sur `.adv-lock`, `[data-cercle]`, `.set-cercle` → `ouvreCercle`)
vivantes : `#cercleTopBtn` · `#openPlusTop` (Réglages) · `.s2-encart` (Peaufiner) · `#stLockCta` (Studio, monde verrouillé) ·
`#ahCercleCta` (aide « i ») · **`#resetApp` « Réinitialiser (test) » DONNE le Cercle**. Mortes : `#karmaCercle`, `#demoTg`,
`.nqh-cercle`, `#plusCta`, `#pplusBanner`, `#openPlus`. La nouvelle Aura n'a aucune porte vers le Cercle.

## C · Ce que le Cercle débloque, dans le code
`isPremium` / `setPremium` → `#device.premium` ; **rien en localStorage** (perdu au rechargement). Vivant : mondes
Sillons/Gravure/Terrazzo ; aide « i » floutée. Affichage seul : importance, récurrence, rappel, mémoire (Q16). Mort :
ancienne Aura, réciprocité de Nuée, fiche d'une personne. « comment ça évolue » : masqué pour tous (Q183 non appliqué).
Nuées illimitées : aucune limite dans le code. « 300 dalles au Cercle » (spec §10) : absent. `setPremium(false)` rétablit
Encre seulement depuis mosaïque/pixel (gratuits) ; l'onboarding propose sillons/gravure/terrazzo sans verrou.

## D · Les documents (à relire moi-même avant l'audit)
spec §2.9 (second anneau), **§3.8 (le bloc du Cercle, l.408–413)**, §5 (inventaire), §6 l.4688 (quatre choses : importance,
récurrence, rappels, mémoire), §10 (300 dalles) — pas de §7.2 ni §7.5 (cités par CHANTIERS 17 et 42), aucun prix. CLAUDE §2,
§4. CHANTIERS 17, 18, 26, 31, 42. QUESTIONS Q14, Q16, Q17, Q102, Q105 bis, Q106, Q113, **Q117**, Q128, **Q165 (les mots de la
page : « Ta parole, vue des deux côtés. », l'année en premier)**, Q167, Q176, Q183, Q184, Q185. ETAT l.886–889, l.5999–6066
(audit + trois partis + page du Cercle), l.7224, l.8449. **AUDIT-AURA-CERCLE.md** (§A–F). AUDIT-FICHE-PERSONNE.md. DECISIONS
A11 (Nuées illimitées en GRATUIT). PROMI-PRESENTATION §7. PARCOURS l.221–227 (« jamais flouté »). AUDIT-ORBITE l.88–89.
**Moodboard H : cadres 22, 24, 25 (le bloc du Cercle), 26 ; AUCUN cadre ne dessine la page d'abonnement `#plusScreen`.**
Planches non intégrées : PLANCHE-AURA-TROIS-PARTIS.html (« La page du Cercle — une seule, pour les trois »),
PLANCHE-FICHE-PERSONNE.html, PLANCHE-STUDIO.html.

## E · Contradictions relevées (à confirmer)
prix (mois d'abord et « près de cinq mois offerts » dans le code / l'année d'abord dans Q165 et la planche ; « 1 €, ou 4 pour
3 € » nulle part ; TTC, durée, reconduction absents) · **au moins sept listes de ce que le Cercle débloque** · « Nuées
illimitées » vendues mais gratuites (A11) · importance libre dans l'ancien code · trois ou quatre mondes (Éclats) · flou
(jamais / 2,4 / 6 / 7 px) · « Membre du Cercle » · Q117 et Q183 non appliqués · ETAT l.889 « rien du Cercle en gratuit »
(vrai pour l'Aura seulement) · l'abonné paie pour des réglages inertes · dégradés sur les Réglages (§6 les interdit).
