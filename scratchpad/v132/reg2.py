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
    raise SystemExit(num)
maj('C-042','FAIT, EN ATTENTE DE TOM',ajoute="**CONSTRUIT (v132)** : `lot-V132-DESSIN` — mode dessin plein écran (surface 390 × 754, rangée A en bas, déploiements au-dessus, encart au contour), trait façon stylet E2, plume et gomme à trois tailles, ANNULER, COULEUR (S2, onglets TRAIT et FOND, palette du Studio en cours, fond grisé pour le trait), POSER ; couleurs figées trait par trait, dessin en cours gardé, fond fixé au premier POSER ; le dessin remplace la dalle ou la photo dans la bande, « Retirer le dessin » ; masquage par fiche, jamais dans un partage ; vue entière (C-051) ; VoiceOver ; entrées sur la fiche, la page + (Promi, Chiche, Cercle) et la fiche d'un Cercle. `redteam_dessin` 63/63 ; cinq sondes de version fautive, il rougit sur chacune. Q392 : pas de bouton de sortie sans poser. **Validation au doigt sur iPhone obligatoire.**",juge='redteam_dessin 63/63')
maj('C-052','FAIT, EN ATTENTE DE TOM',ajoute="**Fait (v132)** : la plus récente en premier ; `redteam_reactif` 31/31 (la parole tenue est la première, visible sans défiler).")
maj('C-053','FAIT, EN ATTENTE DE TOM',preuve="Dans le Peaufiner d'une fiche, le libellé et sa corbeille : crème `#F7F0DE` en sombre, encre `#201908` en clair (Q393) — plus jamais `#DD4D23`. Les Réglages gardent l'orange (C-015). `redteam_decisions` 85/85.",juge='redteam_decisions 85/85')
maj('C-054','FAIT, EN ATTENTE DE TOM',preuve="`#DAC3FF` (jeton `--c-lilas85`) : la teinte OKLCH de `#C4A2F5` (h −58°) éclaircie jusqu'à 4,51:1 sur `#273CEB` — la phrase et la consigne de la page + d'un Promi, en sombre. `redteam_decisions` 85/85.",juge='redteam_decisions 85/85')
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
