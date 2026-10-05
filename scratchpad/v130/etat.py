import io
S=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read()
old="\n## ⚑ À VALIDER SUR IPHONE — liste tenue à jour (ouverte en v123)"
assert S.count(old)==1
ligne="""- **v130 (5 oct.)** — **Trois récidives nommées et jugées** : les dalles seules sont ENGENDRÉES par le moteur, plus découpées dans la Toile (C-048, `redteam_decoupe` G2) ; la double zone de la Pelote après le Studio (C-002, canevas WebGL orphelin, `redteam_zone` C) ; les écrans suivent l'état réel (C-049, `window._paroles`, `redteam_reactif`). **Tropical Breeze `#8ACBE8`** : corps sombre d'un Promi, texte à l'encre (C-050). **Outil de dessin** : planche de la mise en page, rangée A, rien dans la bande (C-042). Q386–Q388.
"""
S=S.replace(old, ligne+old)
S=S.rstrip('\n')+"""
| v130 | Les dalles seules sous Buvard, Braille, Tesselle, Taille-douce, Houle (C-048) : contour réel, plus d'éclats des voisines | `redteam_decoupe` G2 | Studio sur Buvard puis une fiche de Cercle en sombre, l'Index, le Fil : les dalles ont leur vraie forme |
| v130 | La Pelote après deux ouvertures du Studio, en sombre (C-002) | `redteam_zone` 12/12 | Aura, Studio, Studio, Aura : un seul contour derrière la Pelote |
| v130 | Les écrans à jour tout de suite (C-049) | `redteam_reactif` 30/30 | tenir puis retirer une parole depuis la liste de l'Aura ; planter, puis l'Index et le Fil |
| v130 | Tropical Breeze, corps sombre d'un Promi (C-050) | `redteam_decisions` 81/81 ; planche `planche-v130/tropical-avant-apres` | fiche Promi et page + en sombre : la bande contre le corps (Q387), le Peaufiner, « Ma Parole ! » sur un mur (Q386) |
| v130 | L'outil de dessin (C-042) : la mise en page — choisir E1/E2, S1/S2, l'écart de 24 pt | `planche-v130/dessin-*` | les planches, version téléphone |
"""
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write(S)
