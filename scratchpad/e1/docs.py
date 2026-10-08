import io
S=io.open('CHANTIERS.md',encoding='utf-8').read(); L=S.split('\n')
for k,l in enumerate(L):
    if l.startswith('| C-074 |'):
        c=l.split(' | '); assert len(c)==7
        c[3]='FAIT, EN ATTENTE DE TOM'
        c[4]=("E1 (10 oct.) : ① FAIT — un seul composant `GesteFantome` (`montrer`, `oublier`), `lot-E1-GESTES` ; la main est au trait plein, opaque, à l'encre du mode, sans fondu, et porte `data-eng` (A2) ; elle se pose au-dessus de l'écran, ne prend aucun toucher, aucune dalle ne bouge (A1). ② FAIT — 600 ms sans toucher, deux passages au plus, 900 ms de pause, part au premier toucher, drapeau `geste_vu_<id>` dès l'apparition ; un seul geste par passage sur un écran. ③ FAIT — inventaire de 14 gestes : DIX branchés (tenir, chiche, planter, pelote, noyau, fil, studio-monde, studio-couleur, bande, dessin), QUATRE recensés non branchés avec leur raison (aura-apparait : réservé à E2bis ; pelote-folio : place non publiée ; toile-pince : deux doigts, sur la Toile ; défilement du fil d'un Cercle). ④ FAIT — la rangée « Revoir la présentation » des Réglages devient « Revoir les gestes » : elle efface les drapeaux et NE RELANCE PLUS la présentation (aucune autre entrée, rien au Studio) ; `redteam_onboarding` O19 réécrit. ⑤ FAIT — « Réduire les animations » : la main immobile au départ, la flèche du trajet. Preuve : `redteam_gestes` (116 contrôles ; captures `planche-e1/`), `redteam_engagement` 10/11 (A2 ARMÉ sur la main ; R6 rouge jusqu'à E2, décidé). Textes du lot (trois, dans `TEXTES_ENGAGEMENT`) : provisoires. Tom valide la main au doigt sur iPhone.")
        c[5]='redteam_gestes (neuf), redteam_engagement'; c[6]='Tom regarde la main sur iPhone |'
        L[k]=' | '.join(c)
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
Q=io.open('QUESTIONS.md',encoding='utf-8').read().rstrip('\n')+"""

## E1 — les gestes appris en situation (10 oct. 2026)
- **Q421 — TRANCHÉE (Tom)** : R6 reste rouge jusqu'à E2, rien n'est ajouté avant. **Q422 — TRANCHÉE (Tom)** : R3 vise le cadre de la Pelote ; les chiffres de la légende relèvent de C-036.
- **Q425 — À VALIDER** : les trois textes du lot (« Revoir les gestes », « revoir › », « c’est remis › »), provisoires, dans `TEXTES_ENGAGEMENT`.
- **Q426 — À SAVOIR** : « Revoir les gestes » ne relance plus la présentation (E1 point 4 : la rangée « devient »). La présentation n'a donc plus d'entrée à l'écran ; sa fonction (`obReplay`) existe toujours. Le panneau du compte reste joignable par sa porte des Réglages (« Garder ta Toile »).
- **Q427 — À TRANCHER** : quatre gestes sont recensés sans être branchés. Deux pourraient l'être si Tom le veut : la Pelote déplacée dans Mon Folio (il faudrait que le Folio publie sa place), et le pincement de la Toile (deux doigts — et la main passerait au-dessus de la Toile).
- **Q428 — À VALIDER (un choix de ma part)** : un seul geste est montré par passage sur un écran ; le suivant (au Studio : la couleur après le monde) attend le prochain toucher.
- **Q429 — À VALIDER** : le dessin de la main (un index tendu, 40 × 52 pt) et sa place — le bout du doigt sur le trajet.
"""
io.open('QUESTIONS.md','w',encoding='utf-8').write(Q+'\n')
E=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read(); LL=E.split('\n')
i=[k for k,l in enumerate(LL) if l.startswith('- **E0 (9 oct.)**')][0]
LL.insert(i+1,"- **E1 (10 oct.)** — les gestes appris en situation (C-074) : `GesteFantome` (une main au trait plein, opaque, au-dessus de l'écran), dix gestes branchés, quatre recensés ; « Revoir les gestes » aux Réglages (ajout validé, hors inventaire : la main ne paraît qu'au besoin, une fois, et ne décale aucune cote) ; `redteam_gestes`, `redteam_engagement` 10/11 (A2 armé, R6 rouge jusqu'à E2). E2 et E2bis ne sont pas commencés.")
j=[k for k,l in enumerate(LL) if l.startswith('| v137 | Le partage du dessin')][0]
LL.insert(j+1,"| E1 | La main fantôme sur « tracer pour tenir » (C-074) | `redteam_gestes` ; `planche-e1/tenir-*` | ouvrir une fiche à tenir sans toucher : la main paraît, suit le trait deux fois, part au premier toucher ; Réglages → « Revoir les gestes » la fait revenir ; idem page +, Aura, Fil, Studio, mode dessin |")
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write('\n'.join(LL))
C=io.open('CLAUDE.md',encoding='utf-8').read()
def r(a,b):
    global C
    assert C.count(a)==1,(a[:60],C.count(a)); C=C.replace(a,b)
r("### ⚑ E0 (9 oct. 2026) — LE CHANTIER D'ENGAGEMENT : LES GARDE-FOUS.","""### ⚑ E1 (10 oct. 2026) — LES GESTES APPRIS EN SITUATION : LA MAIN FANTÔME. (ENGAGEMENT.md E1, corrigé par A1, A2, A3 ; C-074.)
> **Fait, et arrêté là : E2 et E2bis viennent sur l'ordre de Tom.** Q421 (R6 reste rouge jusqu'à E2) et Q422 (R3 = le cadre de la Pelote ; les
> chiffres de la légende relèvent de C-036) sont tranchées.
> **⚑ UN SEUL COMPOSANT, `window.GesteFantome`** (`lot-E1-GESTES`) : `montrer(idGeste, elementCible, chemin)` · `oublier(idGeste)` ·
> `oublierTout()` · `inventaire()` · `etat()`. La main paraît après **600 ms** sans toucher sur l'écran concerné, joue le geste **deux fois
> au plus** (**900 ms** de pause), part **au premier toucher** n'importe où ; le drapeau `geste_vu_<id>` est posé **dès l'apparition** ;
> **un seul geste par passage sur un écran** (le suivant attend le prochain toucher).
> **⚑ CE QUI PRIME** : A2 — la main est **au trait plein, opaque, à l'encre du mode** (encre `#201908` sur fond crème en clair, crème sur
> seiche en sombre), **sans aucun fondu** : elle paraît et disparaît en une image ; elle porte `data-eng`. Le mouvement est écrit en
> JavaScript (un `transform` par image), jamais une transition ni une animation CSS — sinon A2 rougit. A1 — la couche `#gesteFantome` est
> posée dans `#device`, AU-DESSUS de l'écran, `pointer-events:none` : rien sur la Toile, aucune dalle ne bouge. « Réduire les animations » :
> la main immobile au départ du geste, avec une flèche du trajet.
> **⚑ L'INVENTAIRE (dans le lot, `GESTES`)** — dix BRANCHÉS : `tenir` (fiche d'un Promi pas encore tenu : le trait suit l'onde déclarée par
> `#dpTrameCv[data-trait]`) · `chiche` · `planter` (page +, onde de `_ppEcran()`) · `pelote` (Aura) · `noyau` (Partager, quand `shNoyau`) ·
> `fil` (appui maintenu sur un bandeau) · `studio-monde` puis `studio-couleur` · `bande` (photo ou dessin dans la bande) · `dessin` (surface
> vide du mode dessin). Quatre RECENSÉS, non branchés, avec leur raison : **`aura-apparait` (réservé à E2bis, ne pas le brancher avant)**,
> `pelote-folio`, `toile-pince`, `fiche-cercle-defile`. Un geste neuf = une ligne dans `GESTES` et sa mise en situation dans le juge.
> **⚑ « REVOIR LES GESTES »** : la rangée `#replayOnb` des Réglages (l'ancienne « Revoir la présentation ») efface les drapeaux `geste_vu_*`
> et **ne relance plus la présentation** — aucune autre entrée, rien au Studio. `redteam_onboarding` O19 réécrit (original en sauvegarde).
> **Juges** : **`redteam_gestes.py`** (116 contrôles : pour chaque geste branché, apparition, A2, A1, drapeau, départ d'elle-même, départ au
> toucher, absente après rechargement, de retour après le rejeu au doigt ; mouvement réduit ; sombre ; la Toile inchangée ; captures dans
> `planche-e1/` ; `--sonde` rougit A2 ; `--seul=<id>`) ; **`redteam_engagement`** : A2 est ARMÉ sur la main affichée (10/11, R6 rouge).
> ⚠ **Trois pièges du lot** : ① le Studio et le partage mettent plusieurs secondes à se bâtir : un juge qui attend 4 s y croit la main
> absente ; ② le Studio garde `.show` (§8) : « ouvrir les Réglages » depuis lui touche le Studio ; ③ **tout juge ouvre l'app sur un stockage
> neuf : la main paraît donc dans SES captures** (Aura, fiche, page +) pendant ses quatre premières secondes.

### ⚑ E0 (9 oct. 2026) — LE CHANTIER D'ENGAGEMENT : LES GARDE-FOUS.""")
r("python3 redteam_engagement.py  # E0 (C-073)","python3 redteam_gestes.py      # 116 — E1 (C-074) : la main fantôme, geste par geste (apparition, A2, A1, drapeau, rechargement, « Revoir les gestes » au doigt, mouvement réduit). ≈ 25 min ; --seul=<id> ; --sonde rougit.\npython3 redteam_engagement.py  # E0 (C-073)")
io.open('CLAUDE.md','w',encoding='utf-8').write(C)
