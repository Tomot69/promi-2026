import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
# ── la photo de la bande
rep("      g.drawImage(im, b.x+b.w/2+pc.dx-dw/2, b.y+b.h/2+pc.dy-dh/2, dw, dh); }",
    "      /* ⚑ v141 (Tom, 10 oct. 2026, C-098) : « la photo se tourne à deux doigts ; l'angle est mémorisé » — `pc.a`, en radians, autour du centre de la photo */\n      if(pc.a){ g.save(); g.translate(b.x+b.w/2+pc.dx, b.y+b.h/2+pc.dy); g.rotate(pc.a); g.drawImage(im, -dw/2, -dh/2, dw, dh); g.restore(); }\n      else g.drawImage(im, b.x+b.w/2+pc.dx-dw/2, b.y+b.h/2+pc.dy-dh/2, dw, dh); }")
rep("d.photoCadre={z:_pc.z, dx:_pc.dx, dy:_pc.dy, n:_pc.n};", "d.photoCadre={z:_pc.z, dx:_pc.dx, dy:_pc.dy, a:(_pc.a||0), n:_pc.n};")
rep("  function milieu(t){ return {x:(t[0].clientX+t[1].clientX)/2, y:(t[0].clientY+t[1].clientY)/2, d:Math.hypot(t[0].clientX-t[1].clientX, t[0].clientY-t[1].clientY)||1}; }",
    "  function milieu(t){ return {x:(t[0].clientX+t[1].clientX)/2, y:(t[0].clientY+t[1].clientY)/2, d:Math.hypot(t[0].clientX-t[1].clientX, t[0].clientY-t[1].clientY)||1, g:Math.atan2(t[1].clientY-t[0].clientY, t[1].clientX-t[0].clientX)}; }\n  function tour(d){ while(d>Math.PI) d-=2*Math.PI; while(d<-Math.PI) d+=2*Math.PI; return d; }")
rep("G.mode='pince'; G.m0=m; G.z0=c.z; G.dx0=c.dx; G.dy0=c.dy; window._cadreT=performance.now();",
    "G.mode='pince'; G.m0=m; G.z0=c.z; G.dx0=c.dx; G.dy0=c.dy; G.a0=c.a||0; window._cadreT=performance.now();")
rep("      c.z=z; c.dx=(m.x+(cx0-G.m0.x)*f-G.r.left)/G.k-C.x; c.dy=(m.y+(cy0-G.m0.y)*f-G.r.top)/G.k-C.y;",
    "      /* ⚑ v141 (Tom, C-098) — ET ELLE TOURNE : l'angle de la photo suit l'angle des deux doigts (1:1) ; le point sous leur milieu y reste, le vecteur\n         (centre − milieu) tournant du même angle. */\n      var da=tour(m.g-G.m0.g), co=Math.cos(da), si=Math.sin(da), vx=(cx0-G.m0.x)*f, vy=(cy0-G.m0.y)*f;\n      c.z=z; c.a=G.a0+da; c.dx=(m.x+(vx*co-vy*si)-G.r.left)/G.k-C.x; c.dy=(m.y+(vx*si+vy*co)-G.r.top)/G.k-C.y;")
rep("return p ? {z:(p.photoCadre||{}).z||1, dx:(p.photoCadre||{}).dx||0, dy:(p.photoCadre||{}).dy||0, pose:",
    "return p ? {z:(p.photoCadre||{}).z||1, dx:(p.photoCadre||{}).dx||0, dy:(p.photoCadre||{}).dy||0, a:(p.photoCadre||{}).a||0, pose:")
# ── la photo importée dans un dessin
rep("g.drawImage(im, tr.x-tr.w/2, tr.y-tr.h/2, tr.w, tr.h); g.restore(); } return; }",
    "if(tr.a){ g.translate(tr.x, tr.y); g.rotate(tr.a); g.drawImage(im, -tr.w/2, -tr.h/2, tr.w, tr.h); } else g.drawImage(im, tr.x-tr.w/2, tr.y-tr.h/2, tr.w, tr.h);   /* v141 (C-098) : `a`, l'angle de la photo */ g.restore(); } return; }")
rep("PH.x0=PH.t.x; PH.y0=PH.t.y; PH.w0=PH.t.w; PH.h0=PH.t.h;\n    if(b){ PH.m0={x:(a.x+b.x)/2, y:(a.y+b.y)/2, d:Math.hypot(a.x-b.x, a.y-b.y)||1}; }",
    "PH.x0=PH.t.x; PH.y0=PH.t.y; PH.w0=PH.t.w; PH.h0=PH.t.h; PH.a0=PH.t.a||0;\n    if(b){ PH.m0={x:(a.x+b.x)/2, y:(a.y+b.y)/2, d:Math.hypot(a.x-b.x, a.y-b.y)||1, g:Math.atan2(b.y-a.y, b.x-a.x)}; }")
rep("      t.w=w; t.h=PH.h0*f; t.x=m.x+(PH.x0-PH.m0.x)*f; t.y=m.y+(PH.y0-PH.m0.y)*f; }",
    "      /* ⚑ v141 (Tom, C-098) : deux doigts la TOURNENT aussi — son angle suit celui des doigts, le point sous leur milieu y reste */\n      var da=Math.atan2(b.y-a.y, b.x-a.x)-PH.m0.g; while(da>Math.PI) da-=2*Math.PI; while(da<-Math.PI) da+=2*Math.PI; var co=Math.cos(da), si=Math.sin(da), vx=(PH.x0-PH.m0.x)*f, vy=(PH.y0-PH.m0.y)*f;\n      t.w=w; t.h=PH.h0*f; t.a=PH.a0+da; t.x=m.x+vx*co-vy*si; t.y=m.y+vx*si+vy*co; }")
rep("t.w=Math.round(t.w*10)/10; t.h=Math.round(t.h*10)/10; garde_(); rebatit(); }",
    "t.w=Math.round(t.w*10)/10; t.h=Math.round(t.h*10)/10; if(t.a) t.a=Math.round(t.a*1000)/1000; garde_(); rebatit(); }")
io.open('app.html','w',encoding='utf-8').write(S)
