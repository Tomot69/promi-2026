import io
L=io.open('CHANTIERS.md',encoding='utf-8').read().split('\n')
def maj(num, etat=None, ajoute=None, juge=None, lot=None):
    for i,l in enumerate(L):
        if l.startswith('| %s |'%num):
            c=l.split(' | '); assert len(c)==7,(num,len(c))
            if etat: c[3]=etat
            if ajoute: c[4]=c[4].rstrip()+' '+ajoute
            if juge: c[5]=juge
            if lot: c[6]=lot+' |'
            L[i]=' | '.join(c); return i
    raise SystemExit('absent '+num)
maj('C-050','EN COURS',ajoute="**v131 (Tom, 5 oct.) : Tropical Breeze est ÉCARTÉ (« trop proche du bleu du champ »). Le corps sombre d'un Promi devient le cobalt électrique `#273CEB` ; le texte posé dessus redevient crème ; « Ma Parole ! » : la teinte OKLCH de `#FB4C0D` éclaircie jusqu'à 3:1.**",lot='v131')
maj('C-042',ajoute="**v131 (Tom) : la planche v130 ne suit pas ses consignes.** Promi et Chiche : tout reste à sa place, seule la rangée bouge (16 pt sous le trait) ; Cercle : rien ne disparaît, tout descend d'un bloc et passe sous le bandeau Peaufiner. Planche à refaire.",lot='v131')
i=maj('C-048','EN COURS',ajoute="**v131 (Tom) : faire tourner le juge en boucle (cinquante passages) jusqu'à reproduire la dalle à 3,11 %, nommer la cause, corriger.**",lot='v131')
j=maj('C-050')
L.insert(j+1,"| C-051 | 5 oct. · v131 §3 | « Voir un dessin ou une photo en entier. Dans toute fiche, toucher la bande quand elle porte un dessin ou une photo (jamais la dalle) l'affiche en entier, par-dessus le reste de l'écran. Le reste passe sur un fond sombre plein (la seiche, sans transparence). […] Un nouveau toucher, ou ✕, referme. VoiceOver : « Voir le dessin en entier » / « Voir la photo en entier ». Construis-le dans le prototype, pour les photos. » | EN COURS | — | redteam_entier | v131 |")
L.insert(j+2,"| C-052 | 5 oct. · v131 §0 | « La liste « Ce que tu as tenu » de l'Aura montre toutes les paroles tenues, dans l'ordre chronologique, l'Aura défilant. Plus de limite à 3 ou 6. redteam_reactif vérifie qu'elle est complète. » (remplace Q187) | EN COURS | — | redteam_reactif | v131 |")
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(L))
