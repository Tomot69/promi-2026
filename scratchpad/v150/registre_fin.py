# v150 : les lignes du registre — état, preuve, juge, lot
import io, re
S = io.open('CHANTIERS.md', encoding='utf-8').read(); L = S.split('\n')
MAJ = {
 'C-154': ('FAIT, EN ATTENTE DE TOM', "v150 : la vague de création (le ruban de la page +) en #DD4D23, l'orange de « à tenir » ; jamais #FB4C0D ; la fiche garde l'amande.", "redteam_ruban 36/36", 'v150'),
 'C-157': ('FAIT, EN ATTENTE DE TOM', "v150 : dans la page + d'un Promi (« trace pour planter », « trace ta moitié » — Q545) et d'un Chiche (« trace pour lancer »), le mot du trait descend de 7,5 pt et va 3 pt à droite ; le Cercle ne bouge pas ; les fiches Promi et Chiche identiques au pixel à v149 (au-dessus des coins arrondis du bas, deux thèmes). Trouvé et corrigé en chemin : la BASCULE des lignes de la phrase (34 pt → cinq lignes, 30 pt → quatre) laissait le mot à la cote de l'autre composition, sur les points (v149 : 1 ouverture sur 8 ; 3 sur 8 avant correction) — figée à la deuxième bascule. Capture : planche-v150/page-plus-chiche.png.", "redteam_pages_plus 35/35 (rouge sur v149)", 'v150'),
 'C-158': ('FAIT, EN ATTENTE DE TOM', "v150 : la phrase de la page + d'un Chiche remonte de 10 pt ; celle d'un Cercle se pose exactement sur elle (encre de la première ligne à 315,5, même boîte : −41 pt, une ligne de moins par défaut) ; le rail du pinceau et « garder de côté » (hors ses 4 pt) ne bougent pas. Conséquence mesurée : sur la page + d'un Cercle, 17 pt d'air entre « trace pour lancer » et la phrase (58 avant).", "redteam_pages_plus 35/35 (rouge sur v149)", 'v150'),
 'C-149': ('FAIT, EN ATTENTE DE TOM', "v150 : « garder de côté » à 712 (708 + 4 pt) dans les trois pages + ; inclinaison inchangée (validée).", "redteam_garder 48/48, redteam_pages_plus", 'v150'),
 'C-124': ('FAIT, EN ATTENTE DE TOM', "v150 : « Tout le monde promet. Toi, tu tiens parole. », alignée à droite, en deux lignes égales (« … promet. / Toi, tu tiens parole. » — Q546) ; « La suite t'appartient. » centrée.", "redteam_onb_mots 46/46, redteam_onboarding 46/46, redteam_onboarding_texte 47/47", 'v150'),
 'C-126': ('FAIT, EN ATTENTE DE TOM', "v150 : en sombre aussi, toute la flèche du premier Promi (la traîne, l'amorce, la part tracée) en #FB4C0D ; les points non tracés gardent la couleur du mode.", "redteam_onboarding_texte 47/47", 'v150'),
}
n = 0
for i, l in enumerate(L):
    m = re.match(r'^\| (C-\d{3}) \|', l)
    if not m or m.group(1) not in MAJ: continue
    c = l.split(' | '); etat, preuve, juge, lot = MAJ[m.group(1)]
    c[3] = etat; c[4] = preuve + ' ' + c[4]; c[5] = juge; c[6] = lot + ' |'; L[i] = ' | '.join(c); n += 1
io.open('CHANTIERS.md', 'w', encoding='utf-8').write('\n'.join(L)); print(n, 'lignes')
