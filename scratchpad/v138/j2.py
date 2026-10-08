import io
S=io.open('releve-aura.py',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:60],S.count(a)); S=S.replace(a,b)
r("""            r = pg.evaluate(LANCE, [cx, cy, 84 * sc if lance else 0, 6 if lance else 0, 16, 300])
            attends("()=>!_aura.etat().emp", 20000)
            return (pg.evaluate("()=>performance.now()") - r['t']) / 1000.0
        va, vb = vie(False), vie(True)""",
"""            r = pg.evaluate(LANCE, [cx, cy, 84 * sc if lance else 0, 6 if lance else 0, 16, 300])
            # ⚑ v138 (Tom, 9 oct. 2026, C-072) — LA CAUSE DU FLOTTEMENT ÉTAIT DANS LE JUGE : la fin du creux était lue par `attends`, qui
            #   interroge la page toutes les 100 ms depuis Python, puis par un second aller-retour pour l'heure — une durée de 0,4 à 0,7 s
            #   mesurée à ± 0,1 s près, et allongée du même retard dans les deux cas (ce qui remonte le rapport). La fin se lit maintenant
            #   DANS la page, à l'image près (§8 : un instrument dont la cadence dépend d'autre chose que de ce qu'il mesure ne mesure rien),
            #   et chaque cas est joué TROIS fois : on juge la médiane. LE SEUIL (60 %) N'EST PAS TOUCHÉ. Original : sauvegardes/releve-aura-avant-v138.py.
            return pg.evaluate("(t0)=>new Promise(res=>{ const lim=performance.now()+20000; (function f(){ if(!_aura.etat().emp || performance.now()>lim) res((performance.now()-t0)/1000); else requestAnimationFrame(f); })(); })", r['t'])
        vas, vbs = [], []
        for _k in range(3): vas.append(vie(False)); vbs.append(vie(True))
        va, vb = sorted(vas)[1], sorted(vbs)[1]
        VAL.append(('6 · les trois passes', 'sur place %s · lancé %s' % (' · '.join('%.2f' % v for v in vas), ' · '.join('%.2f' % v for v in vbs))))""")
io.open('releve-aura.py','w',encoding='utf-8').write(S)
