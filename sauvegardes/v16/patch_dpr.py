# Lot v16 — LA DENSITÉ 1×. Les peintres de la Toile posent `g.setTransform(DPR…)` avec LEUR DPR
# (min(2, devicePixelRatio)) ; les appelants taillaient le canevas à ×2 EN DUR. À 2× les deux
# coïncident ; à 1× la Toile se peignait dans le quart haut-gauche. On ne touche pas au code de la
# Toile (§9) : on taille le canevas à SA densité, qu'elle publie déjà (`Toile.vue().dpr`).
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
def rep(a,b,n=1):
    global S; c=S.count(a); assert c==n,(c,a[:90]); S=S.replace(a,b)
rep("function paintPreview(cv,sk,mk2,W,H,PTS){W=W||186;H=H||124;cv.width=W*2;cv.height=H*2;",
    "window._toileDPR=function(){try{return (window.Toile&&window.Toile.vue&&window.Toile.vue().dpr)||2;}catch(e){return 2;}};\nfunction paintPreview(cv,sk,mk2,W,H,PTS){W=W||186;H=H||124;cv.width=W*window._toileDPR();cv.height=H*window._toileDPR();")
rep("var pw=bg.clientWidth||390,ph=bg.clientHeight||800;bg.width=pw*2;bg.height=ph*2;window.Toile.preview(bg,cur,pw,ph);",
    "var pw=bg.clientWidth||390,ph=bg.clientHeight||800;bg.width=pw*window._toileDPR();bg.height=ph*window._toileDPR();window.Toile.preview(bg,cur,pw,ph);")
rep("try{ if(TL.renderTo) _fait=TL.renderTo(_tc9,2,_wL); }catch(_r){}",
    "var _D9=window._toileDPR?window._toileDPR():2;   /* ⚑ v16 : la densité de la Toile, pas ×2 en dur */\n        try{ if(TL.renderTo) _fait=TL.renderTo(_tc9,_D9,_wL); }catch(_r){}")
rep("_tc9.width=Math.max(2,Math.round(W*2));_tc9.height=Math.max(2,Math.round(H*2));",
    "_tc9.width=Math.max(2,Math.round(W*_D9));_tc9.height=Math.max(2,Math.round(H*_D9));")
rep("        bg.width=W*2; bg.height=H*2;\n        var av=window._shAllColored;",
    "        bg.width=W*window._toileDPR(); bg.height=H*window._toileDPR();   /* ⚑ v16 : la densité de la Toile */\n        var av=window._shAllColored;")
io.open(F,'w',encoding='utf-8').write(S); print('ok')
