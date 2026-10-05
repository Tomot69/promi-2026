import io
S=io.open('app.html',encoding='utf-8').read()
old=""":root{--c-seiche10:#050302;--c-seiche21:#1F1611;--c-bleu35:#335382;"""
new=""":root{--c-seiche10:#050302;--c-seiche21:#1F1611;--c-tropical78:#8ACBE8;--c-bleu35:#335382;"""
assert S.count(old)==1; S=S.replace(old,new)
old="""#device.device:not(.light) #detailPoster,#device.device:not(.light) #createSheet{--c-ton07:var(--c-bleu35);"""
new="""#device.device:not(.light) #detailPoster,#device.device:not(.light) #createSheet{--c-ton07:var(--c-tropical78);"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('PROMI-TOKENS.json',encoding='utf-8').read()
old='''    "corps-promi": {
      "clair": "#CFE5FE",
      "sombre": "#335382"'''
assert J.count(old)==1; J=J.replace(old, old.replace('#335382','#8ACBE8'))
old='''    "--c-bleu35": "#335382",'''
assert J.count(old)==1; J=J.replace(old, '''    "--c-tropical78": "#8ACBE8",\n'''+old)
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(J)
