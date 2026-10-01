# Budget des mondes de la saison 2 — tenu à jour à chaque monde

Méthode du contrat (§12 ter) : dix canevas distincts, `renderTo(c, 2)` + relecture d'un pixel (dessin forcé) ; l'écran (Toile repeinte à
chaque image) ; les images réelles pendant une plantation. Chromium avec le vrai GPU, WebKit. Budget : **16,7 ms**. Témoin dans les
mêmes passes : Pochade, dessin 19–20 ms Chromium, 9–10 ms WebKit.

| monde | promesses | dessin Chromium · WebKit (ms) | écran Chromium · WebKit | plantation (pire image) | tient ? |
|---|---|---|---|---|---|
| Brouillamini (v62) | 3 · 6 · 20 · 40 | 10,8–15,5 · 6,6–7,6 | 16,7 · 16,7 | 33 (Chr., 40) · 30 (WK, 40) | **oui** |
| Chamade (v63) | 3 · 6 | 18–20 · 13,6–15 | 16,7 · 16,7 | 33 | oui (écran) |
| | 20 | 23,6 · 12,3 | **18,8** · 16,6 | p90 33 | **non en Chromium (+2,1 ms)** |
| | 40 | 31,2 · 20,7 | **25,5 · 20,7** | 33 | **non (+8,8 Chr., +4 WK)** |
| Volubilis (v64) | 3 · 6 · 20 · 40 | 11,9–14,6 · 6,2–8,2 | 16,7 · 16,7 | **733–1 283 (Chr.) · 535–975 (WK)** | **au repos oui ; à la plantation non** : un jardin se construit en une fois (0,5 à 1,3 s, une image gelée) |
| Guingois (v65) | 3 · 6 | 50–51 · 26–28 | **43–44 · 29–30** | méd. 117–133 (Chr.) · 91–102 (WK) | **non (+27 ms Chr., +13 WK à l'écran)** |
| | 20 · 40 | 52–54 · 27 | **47–50 · 31** | méd. 267–400 (Chr.) · 164–242 (WK) | **non (+33 Chr., +14 WK)** — et la transition tourne à ~6 images/s : tout se recalcule à chaque image |
| Chantourné (v66) | 3 · 6 · 20 · 40 | 21,5–24,6 · 11,7–13 | 16,7 / **18,5 / 17,5 / 21,5** · 16,7 | méd. 17–50 (Chr.) · 17–39 (WK) | **WebKit oui au repos ; Chromium +0,8 à +4,8 ms à l'écran ; plantation non** (le tissage se refait à chaque image : ~18 images/s) |
| Mascaret (v67) | 3 · 6 · 20 | 14,6–18,9 · 10,9–11,6 | 16,7 · 16,7 | méd. 17–33, p90 50–167 (Chr.) · p90 22–118 (WK) | **au repos oui (Chromium à la limite : dessin 15–19) ; plantation non** |
| | 40 | 23,1 · 9,5 | **156 · 103** | p90 500 (Chr.) · 346 (WK) | **non** : tout se reconstruit dès que les graines bougent (400–500 ms la construction à 40) ; sous repeinture forcée le moteur ne se pose pas à 40 promesses |
| Ramage (v68) | 3 · 6 | 255–262 · 182–189 | **229–254 · 1 040–1 151** | méd. 250–267 (Chr.) · 1 047–1 171 (WK) | **non (+212 à +237 ms Chr., +1 s WK)** |
| | 20 · 40 | 393–505 · 302–432 | **445–583 · 2 053–3 122** | méd. 550–583 (Chr.) · 2 023–4 736 (WK) | **non** — le plumage de la planche pose une plume tous les ~10 px sur tout l'écran : 29 929 tracés rejoués à chaque image à 3 promesses, 48 923 à 20. Le plumage est en cache (il ne se reconstruit pas) : c'est le REJEU qui coûte, et WebKit le paie quatre fois plus cher |

---

## v72 (27 sept. 2026) — LA PASSE DE BUDGET. Avant → après, mêmes bancs, même machine

Banc de la session (`banc2.py`) : Chromium avec le vrai GPU (`--use-angle=metal`), WebKit (processus GPU). Pour chaque monde et chaque
nombre de promesses : l'**écran** (Toile repeinte à chaque image, repos) ; la **plantation** (images réelles pendant 2,6 s après
`addPromi`) — images/seconde et p90. Le « dessin » du §12 ter (dix canevas neufs, `renderTo` à chaque fois) mesure l'export et les
aperçus : il ne profite d'aucun calque, il est rapporté à part.
⚠ La colonne « avant » est remesurée sur ces bancs (GPU compris) : elle diffère du tableau du portage, mesuré autrement.

```
                 écran (repos), ms                 plantation, images/s (p90 ms)                          
                 Chromium        WebKit            Chromium                     WebKit
                 avant → après   avant → après     avant → après                avant → après
Ramage     3     211 → 16,7      906 → 17          4,6 → 55 (443 → 19)          1,5 → 60 (1 292 → 21)
          40     568 → 16,7    2 945 → 16          1,9 → 60 (709 → 19)          0,8 → 58 (3 309 → 22)
Guingois   3    22,4 → 16,7       16 → 16         33,5 → 50 (57 → 27)          36 → 56 (47 → 24)
          40    24,5 → 17,2       17 → 16         21,9 → 44 (154 → 30)         25 → 39 (117 → 38)
Mascaret   3    16,7 → 16,7       17 → 16           60 → 60                    60 → 60
          40    17,7 → 16         17 → 17         18,8 → 55 (max 461 → 45)     19 → 56 (313 → 21)
Chamade   20    19,3 → 16,6       17 → 17         54,6 → 60                    61 → 61
          40    26,9 → 16,8       24 → 17           45 → 51 (28 → 24)          50 → 52 (26 → 22)
Volubilis 20    16,7 → 17         17 → 17         20,8 → 60 (max 1 326 → 19)   29 → 60 (max 909 → 27)
          40    16,6 → 16,7       17 → 17         38,8 → 60 (max 955 → 20)     46 → 60 (max 640 → 20)
Chantourné 20   16,6 → 16,7       17 → 17         46,9 → 59 (46 → 19)          48 → 60 (40 → 21)
          40    17,5 → 17         17 → 17         42,7 → 58 (68 → 19)          45 → 59 (57 → 19)
Brouillamini    16,6 (40)         17               60 (non touché)               60
```
**Au repos : les sept tiennent 16,7 ms, dans les deux moteurs.** **Pendant une plantation, cinq tiennent ~60 images/s** (Ramage,
Volubilis, Chantourné, Mascaret à 3–20, Brouillamini) ; **Mascaret à 40 : 55–56** ; **Chamade à 40 : 51–52** ; **Guingois : 39–44 à 40,
50–56 à 3** — ses planchers sont écrits dans QUESTIONS (Q341) : aller plus bas demande de changer ce qu'on voit en mouvement.
**Le dessin forcé (export, aperçus) ne bouge pas** : Ramage 247–505 ms (Chromium) et 151–388 ms (WebKit) par Toile exportée ; les
autres 10–34 ms. Une Toile exportée de Ramage coûte donc toujours un quart à une demi-seconde.

**La transition de Ramage change d'aspect** (fondu du plumage d'arrivée, Q340, à valider) ; celle de Volubilis part quand le Worker
a rendu le jardin (~0,9 s en Chromium) au lieu de geler l'image. Le rythme des sept est relevé, pas encore écrit dans le juge (Q342).

**v74** — Zoom de Ramage : net 0,4–0,5 s après le lâcher en Chromium (était ~2,2 s), 0,85–1,6 s en WebKit ; geste à 60 i/s. Chamade :
calque par cœur essayé, gain nul, retiré. **Planchers assumés (Tom, Q341) : Guingois 39–44 i/s et Chamade 51–52 i/s en plantation à 40.**
