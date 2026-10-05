import io
S=io.open('redteam_reactif.py',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""MOISSON_PETIT, MOISSON_GRAND, SEUIL = 3, 6, 5          # Q187, en dur""","""# ⚑ v131 (Tom, 5 oct. 2026, C-052) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_reactif-avant-v131.py). La règle d'avant (Q187) : trois
#   dalles, six dès cinq tenues, les plus récentes d'abord. La décision qui la remplace : « la liste montre TOUTES les paroles tenues, dans
#   l'ordre chronologique, l'Aura défilant. Plus de limite à 3 ou 6. » La parole qu'on vient de tenir est donc la DERNIÈRE.""")
rep("""        t=e['tenus']; n=MOISSON_GRAND if len(t)>=SEUIL else MOISSON_PETIT; return min(len(t), n)""","""        return len(e['tenus'])""")
rep("""            ok('%s · Aura : la liste est complète (%d dalles attendues)'%(lab,n), len(e['moisson'])==n and all(t in e['tenus'] for t in e['moisson']), 'rendu %s'%e['moisson'])
            if etat=='tenu' and present: ok('%s · Aura : la parole tenue est en tête de la liste'%lab, e['moisson'][:1]==[T], 'tête %s'%e['moisson'][:1])""",
"""            ok('%s · Aura : la liste est complète — TOUTES les paroles tenues (%d)'%(lab,n), len(e['moisson'])==n and sorted(e['moisson'])==sorted(e['tenus']), 'rendu %s'%e['moisson'])
            if etat=='tenu' and present: ok('%s · Aura : la parole tenue est la dernière de la liste (ordre chronologique)'%lab, e['moisson'][-1:]==[T], 'fin %s'%e['moisson'][-1:])""")
rep("""décidée EN DUR (Q187 : trois dalles, six dès cinq tenues — les plus récentes d'abord).""","""décidée EN DUR (v131 : TOUTES les paroles tenues, dans l'ordre chronologique — plus de limite à 3 ou 6).""")
# le juge tient d'abord deux paroles de plus : la liste doit dépasser l'ancienne borne de six
rep("""    # ── 1 · PLANTER dans le Cercle""","""    # ── 0 · on dépasse l'ancienne borne (6) : deux paroles de plus sont tenues par le vrai bouton, AVANT le reste
    for ti in ('nager le mardi','tailler la vigne'):
        accueil(); pg.evaluate("(t)=>openDetail(promises.find(p=>p.title===t).id)", ti); pg.wait_for_timeout(2000)
        pg.evaluate("()=>document.querySelector('#segStatus button[data-st=tenu]').click()"); pg.wait_for_function("()=>!window._tenirAnime", timeout=ANIME_MAX); pg.wait_for_timeout(600)
    accueil(); pg.evaluate(OUVRE['Aura']); e0=lire()
    ok("Aura : sept paroles tenues, sept dalles (l'ancienne borne était six)", len(e0['tenus'])==7 and len(e0['moisson'])==7, '%d tenues · %d dalles'%(len(e0['tenus']),len(e0['moisson'])))
    # ── 1 · PLANTER dans le Cercle""")
io.open('redteam_reactif.py','w',encoding='utf-8').write(S)
