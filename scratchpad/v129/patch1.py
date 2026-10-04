import io
S=io.open('redteam_nuee.py',encoding='utf-8').read()
a="""            out.append(('mot-marque', '#dptNat', 52, 52.0, None, 36, None))"""
assert S.count(a)==1
S=S.replace(a,"""            # ⚑ v129 (Tom, C-046) — CONTRAT MIS À LA DÉCISION (original : sauvegardes/redteam_nuee-avant-v129.py). « CERCLE » était trop haut dans
            #   son encart ; Tom : il est centré exactement comme « PROMI » et « CHICHE ». La boîte du mot est donc à 55,7 (celle de « PROMI »
            #   sur une fiche Promi : le recentrage de v97, +2,65), plus à 52. Le juge de l'ENCRE : redteam_motmarque.py.
            out.append(('mot-marque', '#dptNat', 52, 55.7, None, 36, None))""")
io.open('redteam_nuee.py','w',encoding='utf-8').write(S)
S=io.open('redteam_couleurs_ref.py',encoding='utf-8').read()
a="""                q = min(pareils, key=pire)
                for col in c['dom']:"""
assert S.count(a)==1
S=S.replace(a,"""                q = min(pareils, key=pire)
                # ⚑ v129 (Tom, C-047) — LES « 2 ÉCARTS » DE v128 ÉTAIENT DU JUGE. Une mini-dalle du fil d'un Cercle défilé (« TENU arroser tous
                #   les… », la dernière carte, au bord du pli) est peinte À LA DEMANDE : selon le moment, elle est peinte d'un côté et encore VIDE
                #   de l'autre. Vide côté app, le juge ne disait rien (aucune couleur à comparer) ; vide côté référence, il comparait à rien et
                #   sortait « ΔE 99 ». Mesuré : 1 passage sur 3, tantôt en clair, tantôt en sombre, jamais deux fois de suite. Un canevas vide
                #   d'un côté n'est pas une couleur fausse : il est COMPTÉ et listé (« non peints »), dans les deux sens, et n'est pas jugé ici
                #   (qu'un canevas soit peint, c'est redteam_vide et redteam_apercus qui le jugent).
                if not q['dom'] or not c['dom']:
                    if bool(q['dom']) != bool(c['dom']): non_peints.append((cle, k, 'réf' if not q['dom'] else 'app'))
                    continue
                for col in c['dom']:""")
a="""        global ecarts, orphelins, compares, cv_ecarts, exceptions
        ecarts = []; orphelins = 0; compares = 0; cv_ecarts = [];"""
assert S.count(a)==1
S=S.replace(a,"""        global ecarts, orphelins, compares, cv_ecarts, exceptions, non_peints
        ecarts = []; orphelins = 0; compares = 0; cv_ecarts = []; non_peints = [];""")
a="""if ER[0] or ER[1]: print('erreurs de page"""
assert S.count(a)==1
S=S.replace(a,"""try:
    if non_peints: print('canevas non peints d\\'un côté (comptés, non jugés) : %d — %s' % (len(non_peints), ' · '.join('%s[%s] vide côté %s' % (e[0][0], e[0][1][0], e[2]) for e in non_peints[:6])))
except NameError: pass
if ER[0] or ER[1]: print('erreurs de page""")
io.open('redteam_couleurs_ref.py','w',encoding='utf-8').write(S)
