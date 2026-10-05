import io
S=io.open('redteam_murs.py',encoding='utf-8').read()
old="""        ok9 = bool(f) and f['fond'] in ('rgba(0, 0, 0, 0)', 'transparent') and f['bord'] in ('0px',) and f['ombre'] in ('none',) and f['lignes'] <= 3 and f['taille'] == f['tailleMP'] and f['couleur'] == ENCRE[th] and f['dansMur']
        t('9 · la phrase posée sur le flou : centrée dans le mur, sans fond ni trait, ≤ 3 lignes, une taille, %s' % ('encre' if th == 'light' else 'crème'), ok9, str(f))"""
new="""        # ⚑ v130 — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_murs-avant-v130.py). La règle d'avant : « encre sur
        #   clair, crème sur sombre » se lisait sur le THÈME — vrai tant que le corps sombre d'un Promi était sombre. Tom (5 oct. 2026) :
        #   ce corps devient Tropical Breeze #8ACBE8, et « un fond pastel porte de l'encre ». La phrase suit donc CE QUI EST PEINT SOUS ELLE
        #   (§3) : l'encre #201908 sur le corps Tropical (valeur en dur), la crème sur un fond sombre, l'encre en clair.
        TROPICAL = 'rgb(138, 203, 232)'
        fond_mur = pg.evaluate(\"\"\"()=>{let n=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)'); while(n&&n.nodeType===1){const b=getComputedStyle(n).backgroundColor, m=b.match(/[\\\\d.]+/g); if(m&&(m.length<4||+m[3]>0.85)) return 'rgb('+m[0]+', '+m[1]+', '+m[2]+')'; n=n.parentNode;} return null}\"\"\")
        attendue = 'rgb(32, 25, 8)' if (th == 'light' or fond_mur == TROPICAL) else ENCRE[th]
        ok9 = bool(f) and f['fond'] in ('rgba(0, 0, 0, 0)', 'transparent') and f['bord'] in ('0px',) and f['ombre'] in ('none',) and f['lignes'] <= 3 and f['taille'] == f['tailleMP'] and f['couleur'] == attendue and f['dansMur']
        t('9 · la phrase posée sur le flou : centrée dans le mur, sans fond ni trait, ≤ 3 lignes, une taille, %s' % ('encre' if attendue == 'rgb(32, 25, 8)' else 'crème'), ok9, str(f) + ' · fond du mur ' + str(fond_mur))"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('redteam_murs.py','w',encoding='utf-8').write(S)
