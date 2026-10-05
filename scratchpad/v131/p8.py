import io
J=io.open('redteam_entier.py',encoding='utf-8').read()
old="""  const s=dp.className.replace(/\\bgs\\d+\\b/g,'')+'|'+(dp.getAttribute('style')||'')+'|'+L.join('\\n');"""
new="""  /* et `--ghost-ink` : le décor d'encre de l'écran, retiré au sort lui aussi à chaque toucher (une variable de la racine) */
  const st=[]; for(let i=0;i<dp.style.length;i++){ const k=dp.style[i]; if(k.indexOf('--')!==0) st.push(k+':'+dp.style.getPropertyValue(k)+'!'+dp.style.getPropertyPriority(k)); }
  const s=dp.className.replace(/\\bgs\\d+\\b/g,'')+'|'+st.join(';')+'|'+L.join('\\n');"""
assert J.count(old)==1; J=J.replace(old,new)
io.open('redteam_entier.py','w',encoding='utf-8').write(J)
