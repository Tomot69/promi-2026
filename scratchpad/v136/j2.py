import io
def patch(f, pairs):
    S=io.open(f,encoding='utf-8').read()
    for a,b in pairs:
        assert S.count(a)==1,(f,a[:60],S.count(a)); S=S.replace(a,b)
    io.open(f,'w',encoding='utf-8').write(S)
patch('redteam_halo.py',[("const bt=document.getElementById('auPartPelote')||document.querySelector('#auraScreen .au-part');","const bt=document.getElementById('auPartage');")])
patch('releve-aura.py',[("    'ombre':               (391.22, 407.45),\n","    # ⚑ v136 (Tom, 7 oct. 2026, C-071) : « enlève tout ce qu'il y a comme effet autour de la Pelote […] ne masque pas, supprime » — l'ombre\n    #   (391,22 → 407,45) n'existe plus ; sa place reste dans la colonne, les autres cotes de B ne bougent pas. Original : sauvegardes/releve-aura-avant-v136.py\n")])
patch('redteam_corps.py',[("                if not h or not (abs((oh[2] - oc[2] + 180) % 360 - 180) <= 8 or oc[1] < 0.03 or oh[1] < 0.02):",
"                # ⚑ v136 (Tom, 7 oct. 2026, C-071) — CONTRAT RÉÉCRIT : « le halo c'est une mauvaise idée […] supprime ». Il n'y a plus de halo :\n                #   le contrôle 5 exige qu'AUCUN canevas de halo n'existe (original : sauvegardes/redteam_corps-avant-v136.py).\n                if h:"),
("t('5 · [%s] v125 : la teinte du halo est celle du corps (vingt ouvertures)' % pal","t('5 · [%s] v136 : aucun halo autour de la Pelote (vingt ouvertures)' % pal")])
