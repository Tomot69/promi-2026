import io,re
def patch(f, pairs):
    S=io.open(f,encoding='utf-8').read()
    for a,b in pairs:
        assert S.count(a)==1,(f,a[:60],S.count(a)); S=S.replace(a,b)
    io.open(f,'w',encoding='utf-8').write(S)
S=io.open('CLAUDE.md',encoding='utf-8').read()
i=S.index("> **⚑ LA PELOTE, « LA DEUXIÈME COUCHE FLOUE » (C-002)"); j=S.index("> **⚑ L'AMPLEUR À MI-FORCE (C-062) : Esquille 0,3")
S=S[:i]+"""> **⚑ AUTOUR DE LA PELOTE IL N'Y A PLUS RIEN — NI HALO NI OMBRE (C-002, C-071). Ce point CORRIGE v114 à v126 (halo, ombre, flaque).**
> Tom, 7 oct. : « Les contours ça fait flou, pas net ; le halo c'est une mauvaise idée en fait. […] Enlève tout ce qu'il y a comme effet
> autour de la Pelote pour le moment, ne masque pas, supprime. » `#auPeloteHalo` et `#auPeloteOmbre` **ne sont plus créés** ; la colonne de
> l'Aura garde les cotes B (la place de l'ombre reste vide). ⚠ Le code du peintre du halo (`halo()`, `window._haloPelote`) et les règles
> `.au-halo` / `.au-ombre` restent dans le fichier, MORTS : plus rien ne les appelle. **« La Pelote est le seul volume » (v114) reste la
> règle de `redteam_volume` : rien d'autre ne reçoit de halo ni d'ombre — elle non plus, pour le moment.** Les « points subtils, épars »
> que Tom évoquait ne sont PAS construits (ce serait une seconde exception à la loi des points, §5) : C-071 reste ouvert.
> Ce qui avait été isolé avant : halo, ombre, UN canevas de carte graphique — aucune couche en double. Reste, mesuré et non touché :
> LE LISERÉ DU BORD (sur les 8 derniers pour cent du rayon la fourrure prend une autre couleur que l'intérieur, ΔE 15 à 31,
> `scratchpad/v136/limbe.py`) — c'est le poil lui-même ; un essai (fondre le corps vers le poil au bord) n'a rien changé : RETIRÉ (Q413).
> Juges réécrits : **`redteam_halo`** (10 contrôles : aucun nœud, l'anneau 125–150 pt et la place de l'ombre sont le fond de la page au
> niveau près ; 2/10 sur l'état d'avant), `releve-aura` (plus de cote d'ombre), `redteam_corps` 5 (aucun halo).
"""+S[j:]
io.open('CLAUDE.md','w',encoding='utf-8').write(S)
S=io.open('CHANTIERS.md',encoding='utf-8').read()
L=S.split('\n')
for k,l in enumerate(L):
    if l.startswith('| C-002 |'):
        c=l.split(' | ')
        c[3]='FAIT, EN ATTENTE DE TOM'
        c[4]="v136 : couches isolées (planche `planche-v136/pelote-couches`) — halo, ombre, un canevas GL ; aucun double. Puis, sur l’ordre de Tom (« ne masque pas, supprime ») : HALO ET OMBRE SUPPRIMÉS, leurs nœuds ne sont plus créés ; `?halo=0` retiré. Reste, non touché : le liseré du bord de la fourrure (ΔE 15–31 avec l’intérieur, `planche-v136/pelote-bord`). v130 : canevas orphelin retiré."
        c[5]='redteam_halo (réécrit), redteam_zone'
        c[6]='Tom regarde l’Aura sur iPhone (Q413 : le liseré) |'
        assert len(c)==7; L[k]=' | '.join(c)
    if l.startswith('| C-071 |'):
        c=l.split(' | ')
        c[3]='EN COURS'
        c[4]="v136 : halo et ombre SUPPRIMÉS (« enlève tout ce qu'il y a comme effet autour de la Pelote pour le moment, ne masque pas, supprime »). Les points épars ne sont PAS construits : ce serait une seconde exception à la loi des points (§5) ; Tom : « oui tu as raison ». Rien d'autre autour de la Pelote pour le moment."
        c[5]='redteam_halo'
        c[6]='à reprendre quand Tom le décide |'
        assert len(c)==7; L[k]=' | '.join(c)
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
patch('QUESTIONS.md',[("- **Q413 — OUVERTE (C-002)** : la « deuxième couche floue » autour de la Pelote — le halo (`?halo=0` pour comparer) ou le liseré du bord\n  de la fourrure ? Aucune couche en double n'existe.",
"- **Q413 — OUVERTE (C-002)** : halo et ombre sont SUPPRIMÉS (Tom, 7 oct.). Reste le liseré du bord de la fourrure (ΔE 15–31 avec l'intérieur) :\n  la Pelote paraît-elle encore floue au bord, sans halo ? Aucune couche en double n'existe."),
("- **Q415 — OUVERTE (C-071)** : Tom veut retirer le halo de la Pelote et essayer « quelques points subtils, épars autour ». La loi des points\n  (§5) n'admet qu'une exception. Tom confirme-t-il une seconde exception, nominative, pour la Pelote ? Et le halo se retire-t-il tout de suite ?",
"- **Q415 — TRANCHÉE (C-071, Tom, 7 oct.)** : « oui tu as raison du coup enlève tout ce qu'il y a comme effet autour de la Pelote pour le moment,\n  ne masque pas, supprime. » Halo et ombre supprimés ; pas de points (la loi des points garde sa seule exception).")])
S=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read()
a="| v136 | La Pelote : avec et sans halo (C-002) | planche `planche-v136/pelote-couches` | `app.html` puis `app.html?halo=0`, l'Aura en clair et en sombre : est-ce le halo, ou le liseré du bord ? |"
assert S.count(a)==1
S=S.replace(a,"| v136 | La Pelote sans halo ni ombre (C-002, C-071) | `redteam_halo` 10/10 | l'Aura en clair et en sombre : plus rien autour de la Pelote ; le bord paraît-il encore flou (le liseré de la fourrure) ? |")
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write(S)
