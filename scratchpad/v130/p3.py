import io
S=io.open('redteam_decoupe.py',encoding='utf-8').read()
a="""  Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
    try{ const g=dcv.getContext('2d')"""
assert S.count(a)==1
S=S.replace(a,"""  Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
    if(monde&&monde.m&&monde.m!==Toile.getTheme()) return r;   /* une dalle rendue EXPRÈS dans un autre monde (les exemples) n'est pas de cette mesure */
    try{ const g=dcv.getContext('2d')""")
io.open('redteam_decoupe.py','w',encoding='utf-8').write(S)
