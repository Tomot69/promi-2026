import io
S=io.open('app.html',encoding='utf-8').read()
i=S.index("  var GLY='<svg viewBox=\"20 20 152 168\""); j=S.index("\n",i)
old=S[i:j]; assert S.count(old)==1
new="""  /* ⚑ v141 (Tom, C-099) : « ses trois pois enfreignent la loi des points » — quatre coins, au trait de 2, bouts ronds (la grammaire des icônes). */
  var GLY='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9V5.5A1.5 1.5 0 0 1 5.5 4H9"/><path d="M15 4h3.5A1.5 1.5 0 0 1 20 5.5V9"/><path d="M20 15v3.5a1.5 1.5 0 0 1-1.5 1.5H15"/><path d="M9 20H5.5A1.5 1.5 0 0 1 4 18.5V15"/></svg>';"""
S=S.replace(old,new)
old="#device .acc-recadre#accRecadre{top:660px!important}"
assert S.count(old)==1
S=S.replace(old,"#device .acc-recadre#accRecadre{top:654px!important}   /* v141 (C-099) : 12 pt d'air au-dessus de la barre (710) */\n#device .acc-recadre#accRecadre svg{width:22px!important;height:22px!important}")
io.open('app.html','w',encoding='utf-8').write(S)
