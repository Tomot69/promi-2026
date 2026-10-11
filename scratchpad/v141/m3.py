import io
S=io.open('promi-moteur.js',encoding='utf-8').read()
old="graines:seeds.map(function(s){return {pid:(s.pid==null?null:s.pid),x:s.x,y:s.y,w:s.w,kind:s.kind};})}; };"
assert S.count(old)==1
S=S.replace(old,"graines:seeds.map(function(s){ var b=null; try{ if(s.kind!=='gray' && _MN && _MN.boite) b=_MN.boite(theme,s); }catch(_){ b=null; } return {pid:(s.pid==null?null:s.pid),x:s.x,y:s.y,w:s.w,kind:s.kind,boite:b};})}; };")
io.open('promi-moteur.js','w',encoding='utf-8').write(S)
