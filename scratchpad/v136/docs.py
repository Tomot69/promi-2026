import io,re
def lit(f): return io.open(f,encoding='utf-8').read()
def ecrit(f,s): io.open(f,'w',encoding='utf-8').write(s)
C=lit('CLAUDE.md'); a="### ⚑ v135 (6 oct. 2026) — PLUS AUCUN FILET"; assert C.count(a)==1
B='''### ⚑ v136 (7 oct. 2026) — LA FICHE TENUE EN CLAIR ; LA PHRASE COMPLÈTE ; LE PLEIN ÉCRAN DÈS LA PAGE + ; LE + ; L'AMPLEUR. (Décisions Tom.) Ce bloc CORRIGE v135, v124 (Q269) et v8 là où ils disent autre chose.
> **⚑ EN CLAIR, LE CORPS D'UNE FICHE TENUE (PROMI ET CHICHE) EST LA CRÈME `#F7F0DE`, comme toutes les fiches en clair (C-059). LA TERRE `#2B1020`
> NE VAUT PLUS QU'EN SOMBRE.** En clair la crête verte dit « tenu » et **la mention TENU est au vert d'état `#00341A`** (l'amande est illisible
> sur la crème) ; l'encre reste l'encre. Où ça vit : `lot-V7-CORPS-TENU` (tout le bloc sous `:not(.light)`), le poseur de la fiche (`encre`,
> `_colQd`), `_surTerre()`. Mesuré sur la crème (ΔE CIELAB, seuil 15) : crête `#0B4A2A` 73,1 · arc tenu 80,3 · arc en cours 93,5 · arc à
> tenir 81,7 ; la mention `#00341A` : 12,27:1. « Sur la terre, le tenu est l'amande, en clair aussi » (Q269, v124) est donc MORT en clair.
> **⚑ LA PHRASE COMPLÈTE DANS LES FICHES PROMI ET CHICHE (C-069, `lot-V136-PHRASE`, `window._phraseFiche`)** — dans les fiches seulement,
> jamais dans le Fil ni l'Index, jamais sur un Cercle. La ligne « À moi » / « À Rachel » disparaît : `#dptQui` porte le reste de la phrase,
> **le titre reste seul dans `#dptTitre`, le plus grand texte de la fiche**. Les formes sont celles de la page + : « Je me promets de » ·
> « Je promets à Rachel de » · « Je promets à Rachel, Marion et Nico de » · au-delà de TROIS « Je promets à Rachel, Marion + 4 personnes de »
> (toucher « + x personnes » déroule la liste, la phrase s'allonge, le titre descend) · reçue « Rachel me promet de » · demandée « Rachel,
> promets-moi de » / « promettez-moi de » · Chiche « À Marion · avec Rachel · chiche de » · « Chiche de » · reçu « Marion me lance : chiche
> de » (mot manquant, à valider — Q412). « de » s'élide (« d'aller »). ⚠ Tom citait « Je te promets de… », « Je vous promets de… » : ces
> formes ne nomment personne — j'ai pris celles de la page +, qui nomment (Q412). Juge : **`redteam_phrase_fiche.py`** (56 ; 36/56 avant).
> **⚑ LE PLEIN ÉCRAN DÈS LA PAGE + (C-067)** : toucher le dessin ou la photo dans la bande de la page + l'affiche en entier, un second
> toucher rend la page telle quelle. ⚠ Sur la page +, c'est `#promiForm` qui est sous le doigt dans la bande. `redteam_entier` 44 (38 avant).
> **⚑ LE + DE L'ACCUEIL FAIT 84 pt** (68 avant, × 1,235 ; C-070), centré au même point : il occupe la hauteur intérieure de la barre.
> **Son anneau n'a plus de filet** (il l'avait gardé en v135).
> **⚑ LA PELOTE, « LA DEUXIÈME COUCHE FLOUE » (C-002) — CE QUI EST PEINT AUTOUR D'ELLE** : le halo (`#auPeloteHalo`), l'ombre
> (`#auPeloteOmbre`), UN canevas de carte graphique (`#auBouleGL`) ; le canevas 2D dessous est vide. **Aucune couche en double, aucune
> couche décalée.** Deux choses peuvent se lire comme un second contour : ① le HALO, flou et dissymétrique par construction (plein du
> côté éclairé, nul sur le quart inférieur) — **`?halo=0` l'éteint, Tom compare et tranche** (`lot-V136-HALO0`, à retirer ensuite) ;
> ② LE LISERÉ DU BORD : sur les 8 derniers pour cent du rayon, la fourrure prend une autre couleur que l'intérieur (ΔE 15 à 31 mesuré,
> `scratchpad/v136/limbe.py`) — ce n'est pas une couche, c'est le poil lui-même au bord. Un essai (faire fondre le corps vers le poil au
> bord) n'a rien changé à la mesure : RETIRÉ. Rien n'est tranché (Q413).
> **⚑ L'AMPLEUR À MI-FORCE (C-062) : Esquille 0,3 · Ritournelle 0,3 · Halin 0,3 · Brouillamini 1,5 · Bobinette 0,3.** « Une arrivée de dalle
> jusqu'à 15 % plus longue est acceptée » : Halin +13 %, Brouillamini +13 %, les trois autres 0 % (`redteam_rythme`, ± 15 % à l'arrivée
> pour eux). Dehors : Guingois (+35 %), Chantourné (+38 %) ; Mascaret, Chamade, Volubilis (banc de rendu, accord de Tom attendu) ; **Ramage
> (C-066)**. L'ampleur se lit sur le monde CHOISI (`_ampMonde`), et d'un monde neuf à l'autre la Toile se ressème si l'ampleur est en jeu.
> **⚑ C-066 — L'ÉCART DE GUINGOIS AU BANC VENAIT DE L'AMPLEUR DE RAMAGE (v135).** Ce fichier disait « depuis avant ce lot » : c'était FAUX
> (mesure prise sur une référence salie). Prouvé en retirant Ramage seul : Guingois revient au pixel. Le mécanisme n'est pas nommé ;
> Ramage est retiré de l'ampleur. `banc_rendu` : 280/280 au pixel.
> **⚑ LA GRILLE ANTI-COERCITION DE TOM EST EN TÊTE DU §12** (six questions, six risques cumulés).
> ⚠ **NON FAIT : le partage du dessin (C-068)** — mention de la nature, logo, réglage, photo jamais partagée : rien n'est construit.

'''
ecrit('CLAUDE.md',C.replace(a,B+a))
C=lit('CLAUDE.md')
a="python3 redteam_lexique.py     # 3 —"; assert C.count(a)==1
C=C.replace(a,"python3 redteam_phrase_fiche.py # 56 — v136 (C-069) : chaque cas produit sa phrase (en dur), le titre est le plus grand texte, « + x personnes » se déroule au doigt, le Fil, l'Index et le Cercle sont sans phrase. 36/56 sur l'état d'avant.\n"+a)
ecrit('CLAUDE.md',C)
L=lit('CHANTIERS.md').rstrip('\n').split('\n')
def maj(n,etat,preuve,juge,vise):
    for i,l in enumerate(L):
        if l.startswith('| %s |'%n):
            c=l.split(' | '); assert len(c)==7; c[3]=etat; c[4]=preuve; c[5]=juge; c[6]=vise+' |'; L[i]=' | '.join(c); return
    raise Exception(n)
maj('C-065','FAIT, EN ATTENTE DE TOM','v136 : la grille de Tom (six questions, six risques cumulés, « la structure, jamais le nom ») est en tête du §12 de CLAUDE.md, mot pour mot ; les trente-deux règles reconstituées restent dessous comme détail. Juge des mots : redteam_lexique.','redteam_lexique 3/3','—')
maj('C-059','FAIT, EN ATTENTE DE TOM','v136 : en clair le corps d’une fiche tenue (Promi et Chiche) est la crème ; la terre ne vaut plus qu’en sombre ; mention TENU en `#00341A` en clair. Sur la crème : crête ΔE 73,1 · arc tenu 80,3 · en cours 93,5 · à tenir 81,7 ; mention 12,27:1. v135 : tous les filets retirés. Planche `planche-v136/tenus-clair`.','redteam_decisions · redteam_tonsurton · redteam_filets','—')
maj('C-062','FAIT, EN ATTENTE DE TOM','v136 : ampleur à mi-force sous Esquille 0,3 · Ritournelle 0,3 · Halin 0,3 · Brouillamini 1,5 · Bobinette 0,3. CV à 20 / 40 dalles : Esquille 0,40→0,46 / 0,60→0,66 · Ritournelle 0,46→0,52 / 0,59→0,67 · Halin 0,46→0,52 / 0,59→0,67 · Brouillamini 0,48→0,53 / 0,49→0,59 · Bobinette 0,46→0,52 / 0,57→0,64. Arrivée : Halin +13 %, Brouillamini +13 %, les autres 0 %. Dehors : Guingois (+35 %), Chantourné (+38 %), Ramage (C-066) ; Mascaret, Chamade, Volubilis attendent l’accord de Tom (planche `planche-v135/essai-dix-mondes-*`).','redteam_rythme 60/60 · banc_rendu 280/280','Tom : Mascaret, Chamade, Volubilis')
maj('C-066','FAIT, EN ATTENTE DE TOM','v136 : CAUSE — l’ampleur de RAMAGE (v135) déplaçait le rendu de Guingois au banc (14 images) ; prouvé en retirant Ramage seul. Ce que v135 écrivait (« depuis avant ce lot ») était faux. Ramage retiré de l’ampleur ; banc 280/280 au pixel, rien refigé pour Guingois. Le mécanisme (pourquoi Ramage touche Guingois) n’est pas nommé.','banc_rendu 280/280','—')
maj('C-002','EN COURS','v136 : couches isolées (planche `planche-v136/pelote-couches`) — halo, ombre, un canevas GL ; aucun double, aucun décalage de couche. Deux candidats au « second contour » : le halo (dissymétrique par construction) et le liseré du bord de la fourrure (ΔE 15–31 avec l’intérieur, `planche-v136/pelote-bord`). `?halo=0` posé : Tom compare et tranche. Essai sur le bord sans effet mesuré, retiré. v130 : canevas orphelin retiré.','redteam_zone','Tom tranche (Q413)')
maj('C-067','FAIT, EN ATTENTE DE TOM','v136 : `lot-V131-ENTIER` étendu à la page + (dessin et photo) ; un second toucher rend la page telle quelle.','redteam_entier 44/44 (38/44 avant)','—')
maj('C-068','OUVERT','v136 : NON FAIT. Aujourd’hui : le rond Partager d’une fiche ouvre Mon Folio réduit à la parole ; un dessin posé et non masqué remplace la dalle dans la case. Rien n’est construit pour la mention de la nature, le logo en bas à gauche, le réglage qui masque la mention, ni l’interdiction de partager une photo.','—','v137')
maj('C-069','FAIT, EN ATTENTE DE TOM','v136 : `window._phraseFiche` — huit formes (à soi, à une, à plusieurs, + x personnes dépliable, reçue, demandée, Chiche lancé, Chiche reçu), le titre seul dans son nœud. Planche `planche-v136/phrases`. Tom citait « Je te promets », « Je vous promets » : formes de la page + retenues (Q412).','redteam_phrase_fiche 56/56 (36/56 avant)','—')
maj('C-070','FAIT, EN ATTENTE DE TOM','v136 : le + passe de 68 à 84 pt, même centre ; son anneau perd son filet. Planche `planche-v136/plus`.','redteam_accueil','—')
ecrit('CHANTIERS.md','\n'.join(L)+'\n')
Q=lit('QUESTIONS.md').rstrip('\n')+'''
- **Q406, Q407, Q411 — TRANCHÉES (Tom, v136)** : la grille est donnée ; en clair une fiche tenue est sur la crème ; +15 % d'arrivée accepté.
- **Q412 — À VALIDER (C-069)** : les formes de la phrase. Tom citait « Je te promets de… », « Je vous promets de… » ; elles ne nomment
  personne, j'ai gardé celles de la page + (« Je promets à Rachel de »). Et « Marion me lance : chiche de » (Chiche reçu) est un mot manquant.
- **Q413 — OUVERTE (C-002)** : la « deuxième couche floue » autour de la Pelote — le halo (`?halo=0` pour comparer) ou le liseré du bord
  de la fourrure ? Aucune couche en double n'existe.
- **Q414 — OUVERTE (C-062)** : Mascaret, Chamade, Volubilis : l'essai est sur `planche-v135/essai-dix-mondes-*` ; rien n'est activé ni refigé.
  Ramage est retiré (son ampleur déplaçait Guingois au banc) : le garder dehors, ou chercher le mécanisme ?
'''
ecrit('QUESTIONS.md',Q)
E=lit('ETAT-DES-LIEUX.md')
a=[l for l in E.split('\n') if l.startswith('- **v135 (6 oct.)**')][0]
E=E.replace(a,a+'''
- **v136 (7 oct.)** — fiche tenue en clair sur la crème, TENU en `#00341A` (C-059) ; la phrase complète dans les fiches Promi et Chiche (`_phraseFiche`, C-069) ; plein écran dès la page + (C-067) ; le + à 84 pt (C-070) ; la grille de Tom au §12 ; ampleur sous cinq mondes, +15 % d'arrivée accepté (C-062) ; Guingois : la cause était l'ampleur de Ramage (C-066) ; Pelote : couches isolées, `?halo=0` (C-002). **Non fait : le partage du dessin (C-068).**''')
E=E.rstrip('\n')+'''
| v136 | La fiche tenue en clair, sur la crème (C-059) | `redteam_decisions` ; planche `planche-v136/tenus-clair` | un Promi tenu et un Chiche tenu en clair : la crête verte, la mention TENU en vert ; en sombre, la terre |
| v136 | La phrase complète dans la fiche (C-069) | `redteam_phrase_fiche` 56/56 | une fiche à soi, à quelqu'un, un Chiche ; à plus de trois personnes, toucher « + x personnes » |
| v136 | Le plein écran dès la page + (C-067) | `redteam_entier` 44/44 | page + : dessiner, POSER, toucher le dessin, toucher de nouveau |
| v136 | Le + de l'accueil à 84 pt (C-070) | planche `planche-v136/plus` | l'accueil, clair et sombre |
| v136 | La Pelote : avec et sans halo (C-002) | planche `planche-v136/pelote-couches` | `app.html` puis `app.html?halo=0`, l'Aura en clair et en sombre : est-ce le halo, ou le liseré du bord ? |
| v136 | L'ampleur sous Esquille, Ritournelle, Halin, Brouillamini, Bobinette (C-062) | `redteam_rythme` 60/60 | vingt paroles et plus sous ces cinq mondes ; l'arrivée d'une dalle sous Halin et Brouillamini |
'''
ecrit('ETAT-DES-LIEUX.md',E)
P=lit('portage/A-INTEGRER.md').rstrip('\n')+'''

## v136 (7 oct. 2026) — à reporter dans les dix documents

- **Fiche tenue** : en clair le corps est la crème, la mention TENU en `#00341A` ; la terre et l'amande ne valent plus qu'en sombre (JETONS, SPEC-ECRANS).
- **La phrase de la fiche** (`_phraseFiche`) : huit formes, le titre seul dans son nœud, « + x personnes » dépliable (SPEC-ECRANS, TEXTES).
- **Plein écran** : aussi sur la page + (SPEC-ECRANS, SPEC-GESTE). **Le +** : 84 pt (JETONS).
- **La grille anti-coercition** : le texte de Tom, `CLAUDE.md` §12 — il coiffe REGLES §A.
- **Ampleur** : Esquille, Ritournelle, Halin 0,3 · Brouillamini 1,5 · Bobinette 0,3 ; lue sur le monde choisi ; ressemis d'un monde neuf à l'autre si elle est en jeu (SPEC-RENDU).
- **Partage du dessin** (C-068) : décidé par Tom, PAS construit — mention de la nature et logo en bas à gauche par défaut, réglage qui masque la mention, une photo ne se partage jamais (MANQUES).
'''
ecrit('portage/A-INTEGRER.md',P)
MEM='/Users/macbookpro/.claude/projects/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/memory/'
ecrit(MEM+'point-de-reprise-7-oct-v136.md','''---
name: point-de-reprise-7-oct-v136
description: État à la fin du lot v136 (7 oct. 2026) — fait, non fait, ce qui attend Tom
metadata:
  type: project
---

Lot v136 (7 oct. 2026). Fait : fiche tenue en clair sur la crème ; phrase complète dans les fiches (`_phraseFiche`, redteam_phrase_fiche) ;
plein écran dès la page + ; + à 84 pt ; grille de Tom au §12 ; ampleur sous cinq mondes ; C-066 (Guingois : la cause était l'ampleur de Ramage).

NON FAIT : C-068, le partage du dessin (mention de la nature, logo en bas à gauche, réglage, photo jamais partagée) — à faire en v137.
Attend Tom : Q412 (formes de la phrase), Q413 (Pelote : `?halo=0` ou liseré du bord), Q414 (Mascaret, Chamade, Volubilis ; Ramage).

**How to apply:** avant d'écrire qu'un écart de banc « existait avant le lot », le prouver sur une référence propre (`git stash -- banc-rendu`) —
en v135 je l'ai affirmé à tort. Voir [[point-de-reprise-6-oct-v135]], [[registre-chantiers]].
''')
I=lit(MEM+'MEMORY.md').rstrip('\n').split('\n')
I=[l for l in I if 'point-de-reprise-13-sept.md' not in l and 'point-de-reprise-14-sept.md' not in l and 'ou-reprendre-2-sept.md' not in l]
I.append('- [Point de reprise — 7 oct. (v136)](point-de-reprise-7-oct-v136.md) — phrase des fiches, tenue en clair, + à 84 ; NON FAIT : partage du dessin (C-068)')
ecrit(MEM+'MEMORY.md','\n'.join(I)+'\n')
