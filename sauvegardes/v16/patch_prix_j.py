import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
def rep(a,b,n=1):
    global S; c=S.count(a); assert c==n,(c,a[:90]); S=S.replace(a,b)
rep("    prix:['39 €','soit 3,25 €/mois'],", "    prix:['39 € / an','soit 3,25 €/mois'],   /* ⚑ v16 (Tom) : « 39 € » devient « 39 € / an » */\n   ")
rep("          et += ' · ' + Math.round(+p.due) + ' J';",
    "          et += ' · ' + (Math.round(+p.due)<=1 ? 'DEMAIN' : Math.round(+p.due) + ' JOURS');   /* ⚑ v16 : « 2 J » était du jargon */")
io.open(F,'w',encoding='utf-8').write(S); print('ok')
