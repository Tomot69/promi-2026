# Lot v17 — INGÉNU (ex-Avenant), la palette par défaut : la couleur d'une dalle DIT SA NATURE.
# Décision Tom, 21 sept. 2026 : « Dans cette palette seulement, la couleur d'une dalle dit sa nature : un Promi est
# bleu, un Chiche rose, une Nuée lilas. Le crème dalle peint les cellules neutres de la Toile. » Exception au §4,
# bornée à cette palette. Demande EXPLICITE de toucher à la Toile (§9) : trois retouches, rien d'autre.
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
def rep(a,b,n=1):
    global S; c=S.count(a); assert c==n,(c,a[:90]); S=S.replace(a,b)
rep("var PALS={signal:{name:'Avenant',", "var PALS={signal:{name:'Ingénu',")
# ① la couleur : le seul point où la Toile décide la teinte d'une dalle
rep("var to=s.ci!=null?(s.rgb||PALL()[s.ci][s.lit|0]):g0;",
    "var to=s.ci!=null?((palKey==='signal'&&s.nat!=null)?PALL()[s.nat][s.lit|0]:(s.rgb||PALL()[s.ci][s.lit|0])):g0;   /* ⚑ v17 INGÉNU : la couleur dit la nature — Promi 0 bleu, Chiche 1 rose, Nuée 2 lilas (Tom) */")
# ② la nature, posée sur la cellule là où la couleur figée l'est déjà (_dalleFigee) — la couleur figée n'est PAS touchée :
#    elle revient telle quelle dès qu'on quitte Ingénu
rep("  for(var k=0;k<seeds.length;k++){var s=seeds[k];if(s.kind==='gray'||s.pid==null)continue;var p=m[s.pid];if(!p)continue;\n",
    "  for(var k=0;k<seeds.length;k++){var s=seeds[k];if(s.kind==='gray'||s.pid==null)continue;var p=m[s.pid];if(!p)continue;\n    s.nat=p.chiche?1:0;   /* ⚑ v17 INGÉNU — lue par cOf seulement sous la palette par défaut */\n")
rep("  for(var n=0;n<seeds.length;n++){var t=seeds[n];if(t.kind!=='nuee'||!t.nuee||t.ci==null)continue;var d=ND[t.nuee];",
    "  for(var n=0;n<seeds.length;n++){var t=seeds[n];if(t.kind!=='nuee'||!t.nuee||t.ci==null)continue;t.nat=2;var d=ND[t.nuee];")
# ③ les cellules neutres : le crème dalle, sous Ingénu, dans les deux thèmes
rep("function grays(){return isLightM()?GLIGHT:TH[theme].g;}",
    "var GINGENU=[[239,227,199],[233,220,190],[244,233,208],[236,224,195],[241,230,203]];   /* ⚑ v17 : le crème dalle #EFE3C7 et quatre voisins */\nfunction grays(){return palKey==='signal'?GINGENU:(isLightM()?GLIGHT:TH[theme].g);}")
rep("setPalette:function(k){if(PALS[k]){palKey=k;hueShift=0;_palLit=null;lastChange=performance.now();",
    "setPalette:function(k){if(PALS[k]){var _av=palKey;palKey=k;hueShift=0;_palLit=null;lastChange=performance.now();if((_av==='signal')!==(k==='signal')){try{seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});}catch(e){}}")
rep("  var pal=isLightM()?GLIGHT:TH[w].g;\n  c.seeds.forEach(function(s){s.gray=pal[(Math.random()*5)|0];s.gc=null;});",
    "  var pal=palKey==='signal'?GINGENU:(isLightM()?GLIGHT:TH[w].g);\n  c.seeds.forEach(function(s){s.gray=pal[(Math.random()*5)|0];s.gc=null;});")
# À propos
io.open(F,'w',encoding='utf-8').write(S); print('ok')
