import io
S=io.open('CLAUDE.md',encoding='utf-8').read()
old="""> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — cinquième principe : AUCUNE SUPERPOSITION SUR L'ESPACE DE DESSIN.**"""
new="""> ⚠ **Deux pièges du lot** : ① **une passe accrochée à un `MutationObserver` ne lit jamais les styles dans la micro-tâche de la
> mutation** — chaque `getComputedStyle` y force le recalcul des styles de tout le document (la première image d'une fiche passait de
> 450 à 600 ms) ; elle se demande pour l'image qui vient (`requestAnimationFrame`, avant la peinture). ② **le Peaufiner a SON corps** :
> celui d'une fiche Promi TENUE est Tropical alors que la fiche est terre — « sur quel fond suis-je » se lit sur le premier fond opaque
> sous le nœud (`window._tropicalSous`), jamais sur une classe de la fiche.
> **Juges réécrits au niveau de la décision** (originaux dans `sauvegardes/*-avant-v130.py`) : `redteam_flash_etat` (la première image à
> l'encre, plus à la crème), `redteam_murs` contrôle 9 (la phrase suit le fond du mur), `redteam_decisions`, `redteam_couleurs_ref` (E8).
> ⚠ **OUVERT (Q386)** : « Ma Parole ! » ne tient pas 3:1 sur Tropical (`#FB4C0D` : 1,9:1) — `redteam_murs` 25/26, rouge par décision à prendre.
> `banc_rendu` REFIGÉ : les 60 images de dalles des cinq mondes à trame ont changé (c'est la correction) ; les 220 autres sont au pixel.
> **⚑ L'OUTIL DE DESSIN (C-042, toujours une PLANCHE) — cinquième principe : AUCUNE SUPERPOSITION SUR L'ESPACE DE DESSIN.**"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('CLAUDE.md','w',encoding='utf-8').write(S)
L=io.open('CHANTIERS.md',encoding='utf-8').read()
a="`banc_rendu` : voir le rapport."; assert L.count(a)==1
L=L.replace(a,"`banc_rendu` refigé : les 60 images de dalles de ces cinq mondes ont changé (taille et contour : la dalle n'est plus rognée), les 220 autres images sont au pixel. ⚠ Pris 2 fois sur 9 passages, non reproduit seul : Tesselle, Index en clair, une dalle à 3,11 % d'une autre couleur — le juge NOMME désormais la dalle (parole, taille, monde peint) ; à surveiller.")
a="⚠ « Ma Parole ! » (mur du Peaufiner d'un Promi en sombre) n'atteint plus 3:1 sur ce corps."; assert L.count(a)==1
L=L.replace(a,"⚠ Q386 : « Ma Parole ! » (mur du Peaufiner d'un Promi en sombre) n'atteint plus 3:1 sur ce corps (`#FB4C0D` : 1,9:1) — `redteam_murs` 25/26 tant que Tom n'a pas décidé ; la phrase, elle, passe à l'encre. `redteam_couleurs_ref` : 0 écart, exception E8 nommée (199 propriétés). `redteam_flash_etat` 10/10 (contrat réécrit : l'encre dès la première image).")
io.open('CHANTIERS.md','w',encoding='utf-8').write(L)
