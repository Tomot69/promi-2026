import io
S=io.open('CLAUDE.md',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""### ⚑ v130 (5 oct. 2026) — TROIS RÉCIDIVES NOMMÉES ; TROPICAL BREEZE ; LE MODE DESSIN NE RECOUVRE JAMAIS LA BANDE. (Décisions Tom.)""",
"""### ⚑ v131 (5 oct. 2026) — LE COBALT REMPLACE TROPICAL BREEZE ; LA LISTE DE L'AURA EST COMPLÈTE ; VOIR UNE PHOTO EN ENTIER. (Décisions Tom.) Ce bloc CORRIGE le bloc v130 qui le suit.
> **⚑ LE CORPS SOMBRE D'UN PROMI EST LE COBALT ÉLECTRIQUE `#273CEB`** (jeton `--c-cobalt50` ; fiche Promi et page + d'un Promi, en sombre).
> **Tropical Breeze `#8ACBE8` est ÉCARTÉ** (« trop proche du bleu du champ »). **Le texte posé dessus redevient crème `#F7F0DE`** (6,30:1) :
> plus rien ne déclare un corps pastel, la passe `lot-V130-TROPICAL` est COUPÉE (ses portes restent, inertes). Mesuré : états contre le corps
> (ΔE CIELAB, seuil 15) — à tenir 141,9 · en cours `#291547` 72,9 · tenu 128,8 · trait Promi `#022140` 87,2 ; bande `#82AEF8` contre corps
> ΔE 76,3. **« Ma Parole ! » sur ce corps : `#FF8664`** (`--c-orange-maparole-cobalt`, la teinte OKLCH de `#FB4C0D`, h 36°, éclaircie jusqu'à
> 3,02:1 — `#FF7A55` n'y fait que 2,79:1) ; Chiche et Cercle gardent `#FF7A55`. La phrase lit le premier fond opaque sous le mur
> (`.sur-cobalt`). `redteam_maparole` porte les TROIS valeurs, `redteam_murs` 26/26. ⚠ Non retouché, mesuré : la phrase de la page + (lilas
> `#C4A2F5`) fait 3,35:1 sur le cobalt (3,85:1 sur l'ancien `#335382`) ; « SUPPRIMER CE PROMI » en `#DD4D23` y fait 1,76:1.
> **⚑ « CE QUE TU AS TENU » MONTRE TOUTES LES PAROLES TENUES, dans l'ordre chronologique, l'Aura défilant (C-052 — remplace Q187 : trois
> dalles, six dès cinq tenues).** La parole qu'on vient de tenir est la DERNIÈRE. `redteam_reactif` 31 contrôles (réécrit).
> **⚑ VOIR UNE PHOTO EN ENTIER (C-051, `lot-V131-ENTIER`).** Toucher la bande d'une fiche quand elle porte une PHOTO (jamais la dalle) l'ouvre
> en entier, par-dessus tout l'appareil, sur un fond PLEIN — la seiche, sans transparence, ni ombre, ni fondu ; l'image entière (`contain`) :
> on y voit ce que la bande recadrait. Un nouveau toucher, ✕ ou `closeAll` referme. La bande s'annonce « Voir la photo en entier » (rôle de
> commande) seulement quand elle porte une photo. Le dessin viendra avec l'outil (`source()`). **Trois faits à ne pas reperdre** : ① c'est
> `#dpMain` (la colonne) qu'on touche dans la bande, pas le canevas ; ② « dans la bande » se lit sur ce qui est PEINT (le canevas est opaque
> jusqu'à l'onde) ; ③ **« la fiche est intacte » se juge sur le RENDU** (place, couleur, police, texte de chaque nœud) : l'attribut `style`
> est réécrit par les passes de l'app à chaque toucher, la racine retire au sort `gsN` et `--ghost-ink`, l'invite du geste respire.
> Juge : **`redteam_entier.py`** (36 contrôles, au vrai doigt ; 16/36 sur v130).
> **⚑ C-048 — LA « DALLE À 3,11 % » ÉTAIT DU JUGE.** Reproduite en boucle (cinquante passages sur la copie de v130) : chaque prise est une
> dalle rendue avec une RAMPE (`opts.rampe`, Q30) — l'ombre des carreaux prend le ton sombre de la rampe, à plus de 48 du ton dominant. Ce
> sont ses couleurs. `redteam_decoupe` G2 ne compte plus une couleur qui tombe sur la rampe déclarée.
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — la mise en page corrigée par Tom** : **Promi et Chiche, tout reste à sa place** —
> les trois lignes ne descendent pas ; seule la rangée bouge, à **16 pt sous le trait** ; tailles et couleurs se déploient sous elle (le
> panneau des couleurs est compacté à 114 pt pour finir au-dessus de « À Rachel » : 383 → 497, le texte à 503). **Cercle : rien ne
> disparaît**, tout descend d'un bloc (166 pt sur la planche) et passe sous le bandeau Peaufiner, comme en défilant. Toujours aucun outil
> dans la bande. ⚠ Gardé de v129, non révoqué : en mode dessin les disques d'une fiche Promi et le plateau s'effacent (contour seul).

### ⚑ v130 (5 oct. 2026) — TROIS RÉCIDIVES NOMMÉES ; TROPICAL BREEZE ; LE MODE DESSIN NE RECOUVRE JAMAIS LA BANDE. (Décisions Tom.)""")
rep("""> **⚑ v130 — le corps sombre d'un PROMI est `#8ACBE8` (Tropical Breeze), texte à l'encre ; Chiche et Cercle ne bougent pas.**""",
"""> **⚑ v131 — le corps sombre d'un PROMI est le cobalt `#273CEB`, texte crème (Tropical Breeze, v130, est écarté) ; Chiche et Cercle ne bougent pas.**""")
rep("""python3 redteam_reactif.py     # 30 — v130 (C-049)""","""python3 redteam_entier.py      # 36 — v131 (C-051) : toucher une photo dans la bande l'ouvre en entier (fond seiche plein, image entière) ; un toucher, ✕ ou
                               #   closeAll referme, la fiche intacte ; une dalle n'ouvre rien ; VoiceOver. Au vrai doigt. Rougit sur v130 (16/36).
python3 redteam_reactif.py     # 31 (v131 : la liste de l'Aura = TOUTES les tenues) — v130 (C-049)""")
io.open('CLAUDE.md','w',encoding='utf-8').write(S)
D=io.open('DESSIN-INVENTAIRE.md',encoding='utf-8').read()
D+="""
## v131 (5 oct. 2026) — la mise en page corrigée par Tom (planche `planche-v131/dessin-*`, rien dans l'app)
- **La planche v130 ne suivait pas ses consignes.** **Fiche Promi et Chiche : tout reste à sa place.** Les trois lignes du bas ne
  descendent pas (mesuré sur la planche : 0,0 pt sur « À Rachel », le titre, l'échéance, Peaufiner et la bande). Seule la rangée bouge :
  à **16 pt sous le trait** (331 → 375). Les tailles se déploient sous elle (383 → 427), les couleurs aussi (383 → 497, panneau compacté
  à 114 pt) ; le premier texte est à 503.
- **Fiche Cercle : rien ne disparaît** — ni le titre, ni le fil, ni les disques. Tout descend d'un bloc (166 pt) pour laisser la place à
  la rangée (215 → 259) et à ses déploiements (267 → 381) ; ce qui dépasse passe sous le bandeau Peaufiner, comme en défilant.
- Toujours aucun outil dans la bande (20 cadres sur 20). Tout revient à POSER ou à la sortie.
- Gardé de v129 (non révoqué) : sur une fiche Promi, les disques et « TRACE POUR TENIR » s'effacent le temps du dessin ; le plateau ne
  garde que son contour.
- Restent au choix de Tom : **E1 ou E2**, **S1 ou S2**.
"""
io.open('DESSIN-INVENTAIRE.md','w',encoding='utf-8').write(D)
P=io.open('portage/A-INTEGRER.md',encoding='utf-8').read()
a="- **C-050 · le corps sombre d'un Promi** : Tropical Breeze `#8ACBE8` (Pantone 13-4307 TPG), texte à l'encre `#201908`."
assert P.count(a)==1
P=P.replace(a,"""- **C-050 · le corps sombre d'un Promi (v131)** : cobalt électrique `#273CEB`, texte crème `#F7F0DE` ; « Ma Parole ! » y vaut `#FF8664`.
  (Tropical Breeze, v130, est écarté.)
- **C-051 · voir une photo en entier (v131)** : toucher la bande qui porte une photo (ou un dessin), jamais une dalle ; fond plein seiche,
  image entière, un toucher ou ✕ referme ; VoiceOver « Voir la photo en entier ». En SwiftUI : `fullScreenCover` sans transparence.
- **C-052 · « Ce que tu as tenu » (v131)** : toutes les paroles tenues, dans l'ordre chronologique, l'Aura défile.""")
io.open('portage/A-INTEGRER.md','w',encoding='utf-8').write(P)
Q=io.open('QUESTIONS.md',encoding='utf-8').read()
Q+="""

## LOT v131 — 5 octobre 2026 (les décisions vivent dans CHANTIERS.md : C-042, C-048, C-050, C-051, C-052)

- **Tranché par Tom** : Tropical Breeze écarté, le corps sombre d'un Promi = cobalt `#273CEB`, texte crème (Q387 close) ; « Ma Parole ! »
  sur ce corps = la teinte de `#FB4C0D` éclaircie à 3:1 → `#FF8664` (Q386 close) ; la liste de l'Aura montre toutes les paroles tenues,
  ordre chronologique (Q388 close, Q187 remplacée) ; l'outil de dessin : Promi, seule la rangée bouge (16 pt) ; Cercle, tout descend d'un bloc.
- **Q389 — À REGARDER (Tom)** : sur le cobalt, deux textes que le lot n'a pas touchés sont sous 4,5:1 — la phrase de la page + en lilas
  `#C4A2F5` (3,35:1 ; elle faisait 3,85:1 sur l'ancien corps) et « SUPPRIMER CE PROMI » en `#DD4D23` (1,76:1).
- **Q390 — À CONFIRMER (Tom)** : « ordre chronologique » est posé du plus ancien au plus récent — la parole qu'on vient de tenir est la
  DERNIÈRE de la liste, donc sous le pli quand il y en a beaucoup. L'inverse (la plus récente d'abord) est une ligne.
- **Q391 — À CONFIRMER (Tom)** : en mode dessin sur une fiche Promi, les disques et « TRACE POUR TENIR » s'effacent toujours (principe de
  v129, non révoqué) — « tout reste à sa place » est lu comme « rien ne se déplace ». Si les disques doivent rester, les déploiements les
  recouvriraient (ils commencent à 376, la rangée finit à 375).
- **À CHOISIR (C-042)** : E1 ou E2, S1 ou S2.
"""
io.open('QUESTIONS.md','w',encoding='utf-8').write(Q)
print('docs ok')
