# v151 : les lignes du registre — état, preuve, juge, lot
import io, re
S = io.open('CHANTIERS.md', encoding='utf-8').read(); L = S.split('\n')
MAJ = {
 'C-154': ('FAIT, EN ATTENTE DE TOM', "v151 : la vague de création revient au violet #291547 — une parole créée est « en cours » ; la fiche garde l'amande.", "redteam_ruban 36/36 (rouge sur v150 : B)", 'v151'),
 'C-160': ('FAIT, EN ATTENTE DE TOM', "v151 : l'échéance est une date (`p.ech.iso`), `due` recompté au lancement et à chaque retour au premier plan ; une parole « en cours » au jour passé devient « à tenir » ; REPORTER depuis une échéance passée compte depuis aujourd'hui et la remet « en cours » (Q551) ; ?jour=+N pour l'essai ; « un jour » ne passe jamais « à tenir ». Swift : portage/SPEC-DONNEES §1.12 (T3 fermé).", "redteam_echeance 11/11 (4/11 sur v150)", 'v151'),
 'C-157': ('FAIT, EN ATTENTE DE TOM', "v151 : « trace pour planter », « trace ta moitié », « trace pour lancer » (Cercle compris : même texte) en orange #FB4C0D, clair et sombre, au repos et pendant le geste ; les fiches ne bougent pas ; la règle de l'orange s'étend au libellé du départ. ⚠ 1,23:1 sur le corps du Promi, 2,27:1 sur ceux du Chiche et du Cercle (Q547).", "redteam_pages_plus 41/41, redteam_maparole, redteam_couleurs_ref E20", 'v151'),
 'C-149': ('FAIT, EN ATTENTE DE TOM', "v151 : « garder de côté » à 718 (712 + 6) dans les trois pages + ; inclinaison inchangée ; encre à 22,6 pt de la barre du bas et 22,1 pt du bord droit ; le rail du pinceau ne bouge pas.", "redteam_garder 48/48, redteam_pages_plus 41/41", 'v151'),
 'C-126': ('FAIT, EN ATTENTE DE TOM', "v151 : en sombre « trace pour planter » est crème #F7F0DE, 17,5:1 sur son fond réel #0B0908 — DÉJÀ le cas en v150 (mesuré WebKit et Chromium) : rien n'a été changé (Q549) ; le clair garde #00341A.", "redteam_onb_mots 52/52 (§5)", 'v151'),
 'C-124': ('FAIT, EN ATTENTE DE TOM', "v151 : en sombre Primo, Deuxio, Tertio dans le bleu du clair #0E78F2 (4,7:1 sur le fond réel) ; « La suite t'appartient. » 9 pt plus bas, toujours centrée (garde la crème en sombre : Q548).", "redteam_onb_mots 52/52 (§6, §7 rouges sur v150)", 'v151'),
 'C-159': ('FAIT, EN ATTENTE DE TOM', "v151 : au rejeu, si la Toile comptait au moins une dalle (parole ou Cercle) avant cette plantation : « Une nouvelle dalle sur ta Toile, félicitations. Plus qu'à le tenir. », mot pour mot ; premier lancement : le texte d'origine ; le reste inchangé. Aucune autre mention de « premier / première » dans l'onboarding (la phrase porte les deux). « félicitations » : exception nommée à R1 (Q550).", "redteam_onb_rejeu 10/10 (8/10 sur v150)", 'v151'),
}
n = 0
for i, l in enumerate(L):
    m = re.match(r'^\| (C-\d{3}) \|', l)
    if not m or m.group(1) not in MAJ: continue
    c = l.split(' | '); etat, preuve, juge, lot = MAJ[m.group(1)]
    c[3] = etat; c[4] = preuve + ' ' + c[4]; c[5] = juge; c[6] = lot + ' |'; L[i] = ' | '.join(c); n += 1
io.open('CHANTIERS.md', 'w', encoding='utf-8').write('\n'.join(L)); print(n, 'lignes')
