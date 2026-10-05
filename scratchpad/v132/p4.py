import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""  /* v132 (C-042) : un dessin posé et NON MASQUÉ remplace la dalle dans la case ; masqué, il n'est jamais emporté */
  try{ var _dz=window._dessinCase && window._dessinCase(pid); if(_dz){ _cache[pid]=_dz; return _dz; } }catch(e){}
""","")
rep("""   var tile=window._poseDalle?window._poseDalle(g,p.id,-cw/2,-cw/2,cw,cw):null;
   if(tile){""","""   /* ⚑ v132 (C-042) — un dessin posé et NON MASQUÉ remplace la dalle dans la case : le dessin ENTIER, rendu à partir de ses traits (ce
      n'est pas une dalle : rien n'est découpé dans la Toile) ; masqué, il n'est jamais emporté — la case rend la dalle. */
   var _dz=null; try{ _dz=window._dessinCase ? window._dessinCase(p.id) : null; }catch(_e){ _dz=null; }
   var tile=null;
   if(_dz && _dz.width){ var _k=Math.min(cw/_dz.width, cw/_dz.height), _w=_dz.width*_k, _h=_dz.height*_k; g.drawImage(_dz, -_w/2, -_h/2, _w, _h); tile=true; }
   else tile=window._poseDalle?window._poseDalle(g,p.id,-cw/2,-cw/2,cw,cw):null;
   if(tile){""")
io.open('app.html','w',encoding='utf-8').write(S)
