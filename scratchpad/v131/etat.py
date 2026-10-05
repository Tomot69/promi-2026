import io
S=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read()
old="\n## ⚑ À VALIDER SUR IPHONE — liste tenue à jour (ouverte en v123)"
assert S.count(old)==1
S=S.replace(old, """- **v131 (5 oct.)** — **Cobalt `#273CEB`** : corps sombre d'un Promi, texte crème, « Ma Parole ! » `#FF8664` (C-050 ; Tropical Breeze écarté). **« Ce que tu as tenu » montre toutes les paroles tenues** (C-052). **Voir une photo en entier** (C-051, `redteam_entier`). **C-048** : la dalle à 3,11 % était du juge (une rampe). **Outil de dessin** : planche corrigée (C-042). Q389–Q391.
"""+old)
for a,b in (("| v130 | Tropical Breeze, corps sombre d'un Promi (C-050) |","| v130 | ~~Tropical Breeze~~ *remplacé par la ligne v131 (cobalt)* (C-050) |"),
            ("| v130 | L'outil de dessin (C-042) : la mise en page — choisir E1/E2, S1/S2, l'écart de 24 pt |","| v130 | L'outil de dessin (C-042) — *remplacé par la ligne v131* |")):
    assert S.count(a)==1,a; S=S.replace(a,b)
S=S.rstrip('\n')+"""
| v131 | Le cobalt `#273CEB`, corps sombre d'un Promi (C-050) | `redteam_decisions` 81/81 · `redteam_murs` 26/26 ; planche `planche-v131/cobalt` | fiche Promi et page + en sombre ; le Peaufiner ; un mur (« Ma Parole ! » en `#FF8664`) ; la phrase lilas de la page + et « SUPPRIMER CE PROMI » (Q389) |
| v131 | « Ce que tu as tenu » : toutes les paroles tenues, l'Aura défile (C-052) | `redteam_reactif` 31/31 | tenir une septième parole : elle paraît en dernier (Q390 : ou en premier ?) |
| v131 | Voir une photo en entier (C-051) | `redteam_entier` 36/36 | une fiche avec photo : toucher la bande, puis toucher pour refermer, puis ✕ ; VoiceOver sur la bande |
| v131 | L'outil de dessin (C-042) : la mise en page corrigée — choisir E1/E2, S1/S2 | `planche-v131/dessin-*` | les planches, version téléphone ; Q391 (les disques d'une fiche Promi en mode dessin) |
"""
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write(S)
