import io
S=io.open('promi-moteur.js',encoding='utf-8').read()
old="window.Toile_autoView=function(){autoView();kick();};"
assert S.count(old)==1
S=S.replace(old, old+"\n/* v141 — lecture seule (juges) : la vue et les graines avec leur poids */\nwindow.Toile_lecture=function(){ return {W:W,H:H,vue:{s:view.s,ox:view.ox,oy:view.oy},cible:(vTarget?{s:vTarget.s,ox:vTarget.ox,oy:vTarget.oy}:null),graines:seeds.map(function(s){return {pid:(s.pid==null?null:s.pid),x:s.x,y:s.y,w:s.w,kind:s.kind};})}; };")
io.open('promi-moteur.js','w',encoding='utf-8').write(S)
