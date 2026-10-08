import io
S=io.open('CHANTIERS.md',encoding='utf-8').read(); L=S.split('\n')
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
maj('C-002',None,"v138 : le peintre de secours (sans WebGL 2) reçoit la même correction du bord (table pixel du bord → vis-à-vis intérieur, corps plein jusqu’à R) ; `redteam_bord` passe par les deux chemins : 16/16 (secours : 6/8 sur l’état d’avant).")
maj('C-072','FAIT, EN ATTENTE DE TOM',"v138 : CAUSE NOMMÉE — LE JUGE. La fin du creux était lue par une attente qui interroge la page toutes les 100 ms depuis Python, plus un aller-retour : une durée de 0,4 à 0,7 s mesurée à ± 0,1 s, allongée du même retard dans les deux cas (le rapport remontait vers le seuil). La fin se lit maintenant dans la page, à l’image près, trois passes, médiane : 53 %, 57 %, 45 % sur trois relevés. LE SEUIL (60 %) N’EST PAS TOUCHÉ, le produit non plus.",'releve-aura (acquis 6 réécrit)','—')
maj('C-013',None,"v138 : pris deux fois par `releve-aura` — « rapporter le livre » à ΔE 14,3 (plancher 15) en sombre, et le même tirage rend « 6 bis » indécidable (0,013 / 0,017). Défaut du tirage, ouvert.")
maj('C-027',None,"v138 : « Délier » figure bien au registre (ici) ; la phrase d’ENGAGEMENT.md n’a pas pu être vérifiée, le document n’étant pas arrivé.")
k=[i for i,l in enumerate(L) if l.startswith('| C-072 |')][0]
B="9 oct. · v138 §1 (ENGAGEMENT.md + amendements du chef de chantier, prioritaires)"
N=[("C-073","E0","« Exécute E0 seul, en tenant compte des amendements A2 à A4 dans redteam_engagement, et rends la sortie complète de redteam_engagement.py et du test de verrou de l'onboarding. »","A2 : aucune opacité < 1 ni fondu sur les éléments du chantier (contrôle) ; A3 : aucun texte à l'impératif (contrôle dans R1) ; A4 : la liste interdite de R1 s'aligne sur le lexique de CLAUDE.md, « échéance » retiré si l'app l'emploie ; R4 « inactif avant E3 ».","redteam_engagement (à écrire)"),
 ("C-074","E1","La main fantôme.","A2 : dessinée au trait plein, opaque, à l'encre du mode ; aucun fondu.","redteam_engagement"),
 ("C-075","E2","Le parcours E2 (contenu dans ENGAGEMENT.md).","A7 : E2 et E2bis ensemble.","redteam_engagement"),
 ("C-076","E2bis","« L'interface se dévoile » (A6, nouveau) : au premier lancement la barre du bas ne porte que le +, réduite à sa taille ; chaque élément apparaît à sa place définitive, à sa première fois et jamais à un compte — l'Index à la première plantation, l'Aura et sa Pelote au premier tenu (la main fantôme la désigne), le Studio juste après, le Fil dès qu'une chose arrive des autres ou à la première parole adressée à quelqu'un ; la barre s'élargit et reste asymétrique ; rien ne disparaît une fois apparu.","Garde-fous : « Plus tard » dans l'onboarding fait tout apparaître ; un réglage « Tout afficher » ; tout ce qui arrive des autres fait apparaître le Fil aussitôt. Juge : stockage vierge + parcours E2 complet → tout visible ; « Plus tard » → tout visible d'emblée ; aucun élément ne disparaît.","redteam_engagement"),
 ("C-077","E3","Le moment « tenir ».","A1 : SUPPRIMER l'onde sur les dalles voisines et la menthe de célébration (loi « aucun effet posé sur la Toile », vert de célébration écarté) ; « tenir » reste la transformation existante de la matière ; on garde l'invariance (R4), le crochet promiHaptique et la mesure des tâches longues. A7 : point d'arrêt après E3 (Tom fait repasser ses testeurs).","redteam_engagement (R4)"),
 ("C-078","E4","E4 (contenu dans ENGAGEMENT.md).","A7 : après le point d'arrêt.","redteam_engagement"),
 ("C-079","E5","La phrase d'accueil.","A2 : opaque, dans une couleur de texte secondaire, apparaît et disparaît sans fondu.","redteam_engagement"),
 ("C-080","E6A","La maquette du fil par personne.","A5 : montré sans épaisseur cumulée (un fil par personne, d'épaisseur constante) ; Tom tranche. A7 : validation de Tom avant E6B.","—"),
 ("C-081","E6B","E6B (contenu dans ENGAGEMENT.md).","A7 : seulement après la validation de E6A par Tom.","redteam_engagement")]
lignes=[]
for num,e,dem,am,juge in N:
    lignes.append("| %s | %s | LE CHANTIER D'ENGAGEMENT — %s : %s | OUVERT | v138 : INSCRIT, RIEN N'EST FAIT — ENGAGEMENT.md n'est pas arrivé (absent du dossier, de Téléchargements, du Bureau et de Documents) ; le contenu du lot n'est donc connu que par les amendements. %s Ordre (A7) : E0 → E1 → E2 et E2bis → E3 → point d'arrêt → E4 → E5 → E6A → validation de Tom → E6B. | %s | dès que le document est là |"%(num,B,e,dem,am,juge))
L[k+1:k+1]=lignes
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
Q=io.open('QUESTIONS.md',encoding='utf-8').read().rstrip('\n')+"""

## v138 (9 oct. 2026)
- **Q416, Q417, Q418 — VALIDÉES (Tom, 9 oct.)** : le libellé « Mention sur un dessin partagé », sa place aux Réglages, la mention au-dessus du logo ; « à » et « avec » fusionnés dans les Chiche.
- **Q419 — TRANCHÉE (Tom, 9 oct.)** : le peintre de secours reçoit la même correction du bord de la Pelote ; `redteam_bord` passe par les deux chemins.
- **Q420 — BLOQUANT (§1)** : `ENGAGEMENT.md` n'est pas arrivé. E0 n'est pas exécuté ; les neuf lots sont inscrits (C-073 à C-081) avec les amendements A1 à A7.
"""
io.open('QUESTIONS.md','w',encoding='utf-8').write(Q+'\n')
E=io.open('ETAT-DES-LIEUX.md',encoding='utf-8').read(); LL=E.split('\n')
i=[k for k,l in enumerate(LL) if l.startswith('- **v137 (8 oct.)**')][0]
LL.insert(i+1,"- **v138 (9 oct.)** — le bord de la Pelote corrigé aussi sur le peintre de secours (`redteam_bord` par les deux chemins, 16/16) ; C-072 : la cause était le juge (fin du creux lue toutes les 100 ms), `releve-aura` la lit dans la page, seuil inchangé ; le chantier d'engagement inscrit (C-073 à C-081, amendements A1 à A7) — **E0 NON EXÉCUTÉ : ENGAGEMENT.md n'est pas arrivé.**")
io.open('ETAT-DES-LIEUX.md','w',encoding='utf-8').write('\n'.join(LL))
C=io.open('CLAUDE.md',encoding='utf-8').read()
a="### ⚑ v137 (8 oct. 2026) — PLUS AUCUN EFFET AUTOUR DE LA PELOTE ;"
assert C.count(a)==1
C=C.replace(a,"""### ⚑ v138 (9 oct. 2026) — LE BORD DE LA PELOTE SUR LES DEUX RENDUS ; C-072 ; LE CHANTIER D'ENGAGEMENT INSCRIT. (Décisions Tom.)
> **Q416, Q417, Q418 validées** (le réglage « Mention sur un dessin partagé », sa place, la mention au-dessus du logo ; « à » et « avec »
> fusionnés dans les Chiche).
> **⚑ LE PEINTRE DE SECOURS (SANS WEBGL 2) A LA MÊME CORRECTION DU BORD (C-002)** — « pour que les deux rendus soient identiques ». Après sa
> composition, une passe remplace, au-delà de 0,90 R, la couleur de chaque pixel par celle de son vis-à-vis intérieur (même loi que `FS2` :
> repli autour de 0,92 R, fondu 0,90 → 0,93 R, opacité gardée) ; la table (cible, source, poids) est calculée une fois par taille (`cv.__bd`) ;
> le masque du corps plein va jusqu'à R (0,972 avant). **`redteam_bord` passe par les DEUX chemins** (`--gl`, `--secours` ; le secours est
> forcé par `window._peloteGL=false`, et le juge vérifie quel chemin a peint) : 16/16 ; le secours rougit sur l'état d'avant (6/8).
> **⚑ C-072 — « LE LANCER NE COMBLE PAS » FLOTTAIT À CAUSE DU JUGE.** La fin du creux était lue par `attends` (une question à la page toutes
> les 100 ms, depuis Python) puis par un second aller-retour : 0,4 à 0,7 s mesurées à ± 0,1 s, avec le même retard ajouté aux deux durées —
> le rapport remontait vers son seuil. La fin se lit maintenant DANS la page, à l'image près, trois passes, médiane (53 %, 57 %, 45 % sur
> trois relevés). **Le seuil (60 %) n'est pas touché, le produit non plus.** C'est le §8 : un instrument dont la cadence ne dépend pas de ce
> qu'il mesure ne mesure rien.
> **⚑ LE CHANTIER D'ENGAGEMENT EST AU REGISTRE (C-073 à C-081 : E0, E1, E2, E2bis, E3, E4, E5, E6A, E6B) avec les amendements A1 à A7 du chef
> de chantier, qui PRIMENT sur ENGAGEMENT.md.** À ne jamais reperdre : A1 — ni onde sur les dalles voisines ni menthe de célébration en E3 ;
> A2 — aucune transparence ni fondu (main fantôme au trait plein, phrase d'accueil opaque) ; A3 — aucun texte à l'impératif ; A4 — la liste
> interdite de R1 = le lexique du §2 ; A5 — fil par personne sans épaisseur cumulée ; A6 — E2bis, l'interface se dévoile ; A7 — l'ordre, et
> le point d'arrêt après E3. ⚠ **E0 N'EST PAS EXÉCUTÉ : `ENGAGEMENT.md` n'est pas arrivé** (Q420) ; rien n'a été inventé à sa place.

"""+a)
io.open('CLAUDE.md','w',encoding='utf-8').write(C)
