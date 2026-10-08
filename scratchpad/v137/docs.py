import io
def lit(f): return io.open(f,encoding='utf-8').read()
def ecr(f,s): io.open(f,'w',encoding='utf-8').write(s)
# ── CHANTIERS
S=lit('CHANTIERS.md'); L=S.split('\n')
def maj(num, etat, ajout, juge=None, vise=None):
    for k,l in enumerate(L):
        if l.startswith('| %s |'%num):
            c=l.split(' | '); assert len(c)==7,(num,len(c))
            if etat: c[3]=etat
            c[4]=ajout+' '+c[4]
            if juge: c[5]=juge
            if vise: c[6]=vise+' |'
            L[k]=' | '.join(c); return
    raise Exception(num)
maj('C-002','FAIT, EN ATTENTE DE TOM',"v137 : LE LISERÉ DU BORD PART (Tom, 8 oct.) — au-delà de 0,92 R la couleur d’un pixel est celle de son vis-à-vis à l’intérieur, et le corps reste plein jusqu’au rayon de la boule (116 pt ; il finissait de s’effacer à 117,4, inchangé) : ΔE bord ↔ intérieur 0,2 à 0,6 sur quatre palettes × deux thèmes (5 à 6,5 avant). Code mort du halo et de l’ombre retiré.",'redteam_bord (neuf), redteam_halo, redteam_contour','Tom regarde l’Aura sur iPhone')
maj('C-011',None,"v137 : Tom vérifie sur iPhone, parade gardée.")
maj('C-062',None,"v137 (Tom, Q414) : Ramage reste hors de l’ampleur ; Mascaret, Chamade et Volubilis aussi, rien n’est refigé — clos de mon côté.",None,'—')
maj('C-068','FAIT, EN ATTENTE DE TOM',"v137 : CONSTRUIT. Le rond Partager d’une fiche (Promi, Chiche, Cercle) qui porte un dessin posé et non masqué partage LE DESSIN, entier, avec en bas à gauche le logo « Promi » et au-dessus la mention de la nature ; une rangée « Mention sur un dessin partagé » aux Réglages la masque (mémorisé) ; une photo n’est jamais dans l’image ; un dessin masqué n’est jamais emporté (Mon Folio réduit, avec la dalle). Mots du réglage à valider (Q416). Remplace :",'redteam_partage_dessin (34 ; 8/34 avant)','Tom essaie sur iPhone')
maj('C-069',None,"v137 (Tom, Q412) : formes nommées VALIDÉES ; les Chiche prennent « T’es pas chiche de » · « Marion, t’es pas chiche de » · « Marion et Rachel, vous êtes pas chiches de » · « Marion me dit : t’es pas chiche de » (redteam_phrase_fiche 74/74). Air sous la phrase mesuré à l’encre : inchangé (5,5 → 5,5 pt ; 5,3 sur une phrase de deux lignes).")
maj('C-071','FAIT, EN ATTENTE DE TOM',"v137 : décision de Tom inscrite — plus aucun effet autour de la Pelote ; le halo et l’ombre sortent de la liste blanche (redteam_volume : liste VIDE) ; leur code est retiré (peintre, trame, règles CSS). Les points épars : non construits, non demandés.",'redteam_volume (réécrit), redteam_halo, redteam_bord','—')
ecr('CHANTIERS.md','\n'.join(L))
# ── QUESTIONS
Q=lit('QUESTIONS.md').rstrip('\n')+"""

## v137 (8 oct. 2026)
- **Q412 — TRANCHÉE (Tom, 8 oct.)** : les formes nommées (« Je promets à Rachel de… ») sont validées. Chiche : à soi « T’es pas chiche de » ; lancé
  « Marion, t’es pas chiche de » (« Marion et Rachel, vous êtes pas chiches de », « … + x personnes » au-delà de trois) ; reçu « Marion me dit : t’es pas chiche de ».
- **Q413 — TRANCHÉE (Tom, 8 oct.)** : le liseré du bord de la Pelote part aussi ; ΔE ≤ 5 entre la bande du bord et l'intérieur voisin (`redteam_bord`).
- **Q414 — TRANCHÉE (Tom, 8 oct.)** : Ramage, Mascaret, Chamade et Volubilis restent hors de l'ampleur ; rien n'est refigé.
- **Q416 — À VALIDER (C-068)** : les mots du réglage — « Mention sur un dessin partagé », « affichée », « masquée » (les plus sobres, §2). Et la place :
  le groupe « Partager » des Réglages, sous « Inviter sur Promi ».
- **Q417 — À VALIDER (C-069)** : un Chiche lancé « à Marion, avec Rachel » : les deux sont interpellées dans une seule liste (« Marion et Rachel, vous
  êtes pas chiches de ») — la forme de Tom ne distingue pas « à » de « avec ».
- **Q418 — À VALIDER (C-068)** : sur l'image d'un dessin partagé, la mention est en capitales Gilbert AU-DESSUS du logo, tous deux en bas à gauche, à
  l'encre ou à la crème selon le fond du dessin ; le mot-marque du haut et le QR n'y sont pas. Le dessin entier (390 × 742) est posé « contenu » dans le format choisi.
- **Q419 — À SAVOIR (C-002)** : le bord corrigé vit dans le rendu par la carte graphique ; le peintre de secours (sans WebGL 2) garde l'ancien bord.
"""
ecr('QUESTIONS.md',Q+'\n')
# ── ETAT-DES-LIEUX
E=lit('ETAT-DES-LIEUX.md'); LL=E.split('\n')
i=[k for k,l in enumerate(LL) if l.startswith('- **v136 (7 oct.)**')][0]
LL.insert(i+1,"- **v137 (8 oct.)** — Chiche : « T’es pas chiche de » et ses formes (Q412) ; la Pelote : le liseré du bord part (`redteam_bord`), le code du halo et de l'ombre est retiré, liste blanche du volume VIDE (C-002, C-071) ; le partage du dessin construit — logo et mention en bas à gauche, réglage aux Réglages, photo jamais partagée (`redteam_partage_dessin`, C-068) ; air sous la phrase mesuré : inchangé.")
j=[k for k,l in enumerate(LL) if l.startswith('| v136 | L\'ampleur sous Esquille')][0]
LL[j+1:j+1]=["| v137 | Les Chiche : « T’es pas chiche de » (C-069) | `redteam_phrase_fiche` 74/74 | fiches « courir dimanche » et « le grand plongeoir » : la phrase se lit-elle bien ? |",
 "| v137 | La Pelote sans liseré au bord (C-002) | `redteam_bord` 8/8 ; `planche-v137/bord-*` | l'Aura en clair et en sombre : le bord est-il net, sans seconde couche ? |",
 "| v137 | Le partage du dessin (C-068) | `redteam_partage_dessin` 34/34 ; `planche-v137/partage-dessin-*` | dessiner sur une fiche, poser, toucher le rond Partager : le dessin, le logo, la mention ; Réglages → « Mention sur un dessin partagé » ; une fiche à photo : la photo ne part pas |"]
ecr('ETAT-DES-LIEUX.md','\n'.join(LL))
# ── portage
P=lit('portage/A-INTEGRER.md').rstrip('\n')+"""

## v137 (8 oct. 2026)
- **Phrases des Chiche** (Q412) : « T’es pas chiche de » · « {qui}, t’es pas chiche de » · « {liste}, vous êtes pas chiches de » · « {de} me dit : t’es pas chiche de » — remplacent « Chiche de », « À … · avec … · chiche de », « … me lance : chiche de » dans `TEXTES.md` et `ECRANS.md`.
- **La Pelote** : plus aucun effet autour (ni halo, ni ombre, ni liseré) ; au bord (> 0,92 R) la couleur est celle de l'intérieur (vis-à-vis replié autour de 0,92 R), le corps est plein jusqu'à R et s'efface de R à 1,012 R. `REGLES.md` : la liste blanche des volumes est vide ; seule exception restante, le flou des murs de Ma Parole !.
- **Partage du dessin** (C-068) : construit — remplace la ligne « PAS construit » ci-dessus. Sujet d'une fiche avec dessin posé et non masqué → image = le dessin entier sur son fond, logo « Promi » (PromiLate) en bas à gauche, mention de la nature (Gilbert, capitales) au-dessus ; réglage `promi_dessin_mention` ('0' = masquée) ; jamais de photo ; dessin masqué → Folio réduit, dalle.
"""
ecr('portage/A-INTEGRER.md',P+'\n')
