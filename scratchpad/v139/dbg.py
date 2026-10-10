import re,io
S=io.open('redteam_enfonce.py',encoding='utf-8').read()
S=S.replace("        juge('H · le retour n\\'a pas de saut non plus'","        print([(round(ret[i][0]-t1), round(ret[i][1],3)) for i in range(0,min(len(ret),200),1) if i<6 or (ret[i-1][1]-ret[i][1])/max(1.0,ret[i][0]-ret[i-1][0])*16.7>0.03])\n        juge('H · le retour n\\'a pas de saut non plus'")
S=S.replace("    # ── E : à l'écran","    b.close(); sys.exit()\n    # ── E : à l'écran")
exec(compile(S,'x','exec'))
