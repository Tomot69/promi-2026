import io
L=io.open('CHANTIERS.md',encoding='utf-8').read().split('\n')
def maj(num, etat=None, ajoute=None, preuve=None, juge=None, lot=None):
    for i,l in enumerate(L):
        if l.startswith('| %s |'%num):
            c=l.split(' | '); assert len(c)==7,(num,len(c))
            if etat: c[3]=etat
            if preuve is not None: c[4]=preuve
            if ajoute: c[4]=c[4].rstrip()+' '+ajoute
            if juge: c[5]=juge
            if lot: c[6]=lot+' |'
            L[i]=' | '.join(c); return
    raise SystemExit('absent '+num)
maj('C-050','FAIT, EN ATTENTE DE TOM',ajoute="**Fait (v131)** : `#273CEB` posé (jeton `--c-cobalt50`, JSON = CSS = Swift) ; crème sur le corps 6,30:1 ; « Ma Parole ! » `#FF8664` (3,02:1, OKLCH h 36°) ; états contre le corps, ΔE CIELAB : à tenir 141,9 · en cours 72,9 · tenu 128,8 (seuil 15) ; bande contre corps ΔE 76,3. `redteam_decisions` 81/81, `redteam_murs` 26/26, `redteam_maparole` 12/12, `redteam_tonsurton` 26/26, `redteam_flash_etat` 10/10. Planche `planche-v131/cobalt.png`. Q389 : la phrase lilas de la page + (3,35:1) et « SUPPRIMER CE PROMI » (1,76:1), non retouchés.",juge='redteam_decisions 81/81 · redteam_murs 26/26')
maj('C-042',ajoute="**Planche v131 refaite** `planche-v131/dessin-{promi,cercle}-{clair,sombre}.png` : Promi — rangée à 16 pt sous le trait (331 → 375), tailles 383 → 427, couleurs 383 → 497 (panneau compacté à 114 pt), premier texte à 503, déplacement mesuré hors rangée 0,0 pt ; Cercle — rien ne disparaît, le bloc descend de 166 pt et passe sous Peaufiner ; 20 cadres sur 20 sans outil dans la bande. Q391 : les disques d'une fiche Promi s'effacent toujours en mode dessin (v129). Restent à choisir : E1/E2, S1/S2.",lot='v132')
maj('C-048','FAIT, EN ATTENTE DE TOM',ajoute="**Cause nommée (v131)** : cinquante passages en boucle sur la copie de v130 — 18 prises dans 15 passages (dont 3,11 % deux fois), TOUTES des dalles rendues avec une rampe (`opts.rampe`, les cartes de l'Index et du Fil) : l'ombre des carreaux prend le ton sombre de la rampe. C'était le JUGE. Corrigé : une couleur sur la rampe déclarée n'est pas « une autre couleur » ; rejouée sur les 18 prises, la mesure rend 0,00 %. `redteam_decoupe` 0 défaut ; preuve qu'il mord encore sur v129 : voir le rapport.",juge='redteam_decoupe (G2)')
maj('C-051','FAIT, EN ATTENTE DE TOM',preuve="`lot-V131-ENTIER` : toucher la bande d'une fiche qui porte une photo l'ouvre en entier (fond seiche plein, image entière), un toucher, ✕ ou `closeAll` referme, la fiche intacte ; une dalle n'ouvre rien ; VoiceOver « Voir la photo en entier ». Pour les photos (le dessin viendra avec l'outil). `redteam_entier` 36/36, au vrai doigt ; 16/36 sur v130.",juge='redteam_entier 36/36')
maj('C-052','FAIT, EN ATTENTE DE TOM',preuve="La liste montre toutes les paroles tenues, dans l'ordre où elles ont été tenues (la plus récente en dernier — Q390), l'Aura défile ; « Ce qu'on t'a tenu » suit dessous. `redteam_reactif` réécrit : 31/31 ; 23/31 sur v130. `releve-aura` : cotes B 0 écart.",juge='redteam_reactif 31/31')
maj('C-021',lot='v132')
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
