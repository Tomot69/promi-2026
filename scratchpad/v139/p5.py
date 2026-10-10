import io
f='redteam_enfonce.py'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("ok = 0; ko = []\n","""ok = 0; ko = []
def plus_grand_pas(L, sens):
    # le pas d'une image, ramené à 16,7 ms ; deux relevés à moins de 12 ms l'un de l'autre sont une même image (le navigateur
    # rend parfois deux rappels coup sur coup) : on les réunit, sinon 4 ms d'écart gonflent le pas par quatre
    m = 0.0; i0 = 0
    for i in range(1, len(L)):
        dt = L[i][0] - L[i0][0]
        if dt < 12: continue
        m = max(m, sens * (L[i][1] - L[i0][1]) / dt * 16.7); i0 = i
    return m
""")
rep("pas = max((app[i][1] - app[i - 1][1]) / max(1.0, app[i][0] - app[i - 1][0]) * 16.7 for i in range(1, len(app))); pas = max(pas, app[0][1])","pas = max(plus_grand_pas(app, 1), app[0][1])")
rep("pr = max((ret[i - 1][1] - ret[i][1]) / max(1.0, ret[i][0] - ret[i - 1][0]) * 16.7 for i in range(1, len(ret)))","pr = plus_grand_pas([app[-1]] + ret, -1)")
io.open(f,'w',encoding='utf-8').write(S)
