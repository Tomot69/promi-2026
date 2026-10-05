import io
S=io.open('app.html',encoding='utf-8').read()
old="""        var txt=false; for(var k=el.firstChild;k;k=k.nextSibling){ if(k.nodeType===3 && k.nodeValue.trim()){ txt=true; break; } }"""
new="""        var txt=(tag==='INPUT'||tag==='TEXTAREA'); for(var k=el.firstChild;k&&!txt;k=k.nextSibling){ if(k.nodeType===3 && k.nodeValue.trim()){ txt=true; break; } }"""
assert S.count(old)==1; S=S.replace(old,new)
old="""      if(!sombre || !ouvert){ [].forEach.call(r.querySelectorAll('[data-trop],[data-tropb]'), rend); return; }"""
new="""      /* la classe dit « ce corps est Tropical Breeze » : elle sert aux seuls textes d'attente des champs (::placeholder), qu'aucun
         style en ligne n'atteint. On compare avant de la poser (§8). */
      var trop = sombre && ouvert && estTrop(fond(r));
      if(r.classList.contains('corps-tropical')!==trop) r.classList.toggle('corps-tropical', trop);
      if(!sombre || !ouvert){ [].forEach.call(r.querySelectorAll('[data-trop],[data-tropb]'), rend); return; }"""
assert S.count(old)==1; S=S.replace(old,new)
old="""<script id="lot-V130-TROPICAL">"""
new="""<style id="lot-V130-TROPICAL-css">
#device #detailPoster.corps-tropical input::placeholder,#device #detailPoster.corps-tropical textarea::placeholder,
#device #createSheet.corps-tropical input::placeholder,#device #createSheet.corps-tropical textarea::placeholder{color:var(--c-encre-attente)!important;-webkit-text-fill-color:var(--c-encre-attente)!important;opacity:1!important}
</style>
<script id="lot-V130-TROPICAL">"""
assert S.count(old)==1; S=S.replace(old,new)
old=""":root{--c-seiche10:#050302;--c-seiche21:#1F1611;--c-tropical78:#8ACBE8;"""
new=""":root{--c-seiche10:#050302;--c-seiche21:#1F1611;--c-tropical78:#8ACBE8;--c-encre-attente:rgba(32,25,8,.72);"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('PROMI-TOKENS.json',encoding='utf-8').read()
old='''    "--c-tropical78": "#8ACBE8",'''
assert J.count(old)==1; J=J.replace(old, old+'''\n    "--c-encre-attente": "rgba(32,25,8,.72)",''')
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(J)
