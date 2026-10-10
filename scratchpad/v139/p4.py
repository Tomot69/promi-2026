import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""    EMP.comble+=G.COMBLE*V.om*dt;
    EMP.p=Math.max(0, p-EMP.comble);""",
"""    EMP.comble+=G.COMBLE*V.om*dt;
    /* ⚑ v139 (C-083) — LE COMBLEMENT NE COUPE PLUS : il était RETRANCHÉ de la pression, et la profondeur (p^(2/3)) tombait à zéro d'un coup
       quand la pression y arrivait (mesuré avec le retour lent : un pas de 15 % de la butée, par la seule rotation de repos). Il AMORTIT
       maintenant (× e^(−comblement / COMBLE_K)) : ce qui file par-dessus referme le creux d'autant plus vite qu'on lance fort, sans saut. */
    EMP.p=p*Math.exp(-EMP.comble/G.COMBLE_K);""")
rep("ENF_TAU:0.60, RETOUR_TAU:0.60, DOIGT_K:2.2,","ENF_TAU:0.60, RETOUR_TAU:0.60, COMBLE_K:0.15, DOIGT_K:2.2,")
io.open(f,'w',encoding='utf-8').write(S)
f='redteam_enfonce.py'; S=io.open(f,encoding='utf-8').read()
rep("all(V[k + 1] < V[k] for k in range(len(V) - 1)) and V[0] > 4 * V[6]","all(V[k + 1] < V[k] for k in range(9)) and all(V[k + 1] < V[k] + 0.004 for k in range(9, len(V) - 1)) and V[0] > 4 * V[6]")
rep("  B · sa vitesse DÉCROÎT (fenêtres de 150 ms successives, chacune plus lente que la précédente) ;","  B · sa vitesse DÉCROÎT (fenêtres de 150 ms successives, chacune plus lente que la précédente ; au-delà de 1,5 s, où une\n      fenêtre ne vaut plus qu'un pour cent, à 0,4 point près — le grain d'une image) ;")
io.open(f,'w',encoding='utf-8').write(S)
