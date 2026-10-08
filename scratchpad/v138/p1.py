import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
r("""  og.putImageData(cv.__im,0,0);
  g.drawImage(cv.__off,0,0);
""","""  og.putImageData(cv.__im,0,0);
  g.drawImage(cv.__off,0,0);
  /* ⚑ v138 (Tom, 9 oct. 2026, C-002) — « Le peintre de secours (sans WebGL 2) reçoit la même correction du bord de la Pelote, pour que les
     deux rendus soient identiques. » La même loi que la passe de composition de la carte graphique (v137) : au-delà de 0,92 R la COULEUR d'un
     pixel est celle de son vis-à-vis à l'intérieur (même angle, rayon replié autour de 0,92 R, borné à 0,80 × 0,92 R), fondu de 0,90 à
     0,93 R ; son OPACITÉ reste la sienne. La table (pixel du bord → pixel de l'intérieur, poids) est calculée une fois par taille. */
  if(!o.sansPlein){
    var _B=cv.__bd;
    if(!_B || _B.W!==W || _B.R!==R){ var _rb=R*0.92, _a0=R*0.90, _a1=R*0.93, _rm=R*1.08, _x0=Math.max(0,Math.floor(CX-_rm)), _y0=Math.max(0,Math.floor(CY-_rm)),
          _x1=Math.min(W,Math.ceil(CX+_rm)), _y1=Math.min(W,Math.ceil(CY+_rm)), _bw=_x1-_x0, _bh=_y1-_y0, _Dn=[], _Sn=[], _Wn=[];
      for(var _by=_y0;_by<_y1;_by++) for(var _bx=_x0;_bx<_x1;_bx++){ var _dx=_bx+0.5-CX, _dy=_by+0.5-CY, _br=Math.hypot(_dx,_dy); if(_br<=_a0 || _br>_rm) continue;
        var _bw_=(_br-_a0)/(_a1-_a0); _bw_=_bw_>=1?1:_bw_*_bw_*(3-2*_bw_); var _rr=Math.max(2*_rb-_br, _rb*0.80), _sx=Math.floor(CX+_dx*_rr/_br)-_x0, _sy=Math.floor(CY+_dy*_rr/_br)-_y0;
        if(_sx<0||_sy<0||_sx>=_bw||_sy>=_bh) continue; _Dn.push((_by-_y0)*_bw+(_bx-_x0)); _Sn.push(_sy*_bw+_sx); _Wn.push(_bw_); }
      _B=cv.__bd={W:W, R:R, x:_x0, y:_y0, w:_bw, h:_bh, D:new Int32Array(_Dn), S:new Int32Array(_Sn), P:new Float32Array(_Wn), T:new Uint8Array(_Dn.length*3)}; }
    var _bi=g.getImageData(_B.x,_B.y,_B.w,_B.h), _bd=_bi.data, _bn=_B.D.length, _bT=_B.T, _bq, _bs, _bt, _bp;
    for(_bq=0;_bq<_bn;_bq++){ _bs=_B.S[_bq]*4; _bT[_bq*3]=_bd[_bs]; _bT[_bq*3+1]=_bd[_bs+1]; _bT[_bq*3+2]=_bd[_bs+2]; }   /* les sources d'abord : la bande 0,90–0,92 R est à la fois source et cible */
    for(_bq=0;_bq<_bn;_bq++){ _bt=_B.D[_bq]*4; if(!_bd[_bt+3]) continue; _bp=_B.P[_bq];
      _bd[_bt]+=(_bT[_bq*3]-_bd[_bt])*_bp; _bd[_bt+1]+=(_bT[_bq*3+1]-_bd[_bt+1])*_bp; _bd[_bt+2]+=(_bT[_bq*3+2]-_bd[_bt+2])*_bp; }
    g.putImageData(_bi,_B.x,_B.y);
  }
""")
r("_mi=_mg.createImageData(W,W), _md=_mi.data, _r0=R*0.972, _r1=R*1.012;","_mi=_mg.createImageData(W,W), _md=_mi.data, _r0=R*1.0 /* v138 : plein jusqu'au rayon de la boule, comme la carte graphique (0,972 avant) */, _r1=R*1.012;")
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('redteam_bord.py',encoding='utf-8').read()
def rj(a,b):
    global J
    assert J.count(a)==1,(a[:60],J.count(a)); J=J.replace(a,b)
rj("F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'",
   "F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'\n# ⚑ v138 (Tom, 9 oct. 2026) : « redteam_bord passe aussi par ce chemin » — le peintre de secours (sans WebGL 2), forcé par `window._peloteGL=false`.\nCHEMINS = [('carte graphique', ''), ('secours', 'window._peloteGL=false;')]\nif '--gl' in sys.argv: CHEMINS = CHEMINS[:1]\nif '--secours' in sys.argv: CHEMINS = CHEMINS[1:]")
rj("    for th in ('light', 'dark'):\n        for pal in PALETTES:","  for chemin, force in CHEMINS:\n    for th in ('light', 'dark'):\n        for pal in PALETTES:")
rj("""                ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")""","""                ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}" + force)""")
rj("""                g = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, document.getElementById('device').classList.contains('light')]}")""",
   """                g = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect(); const e=window._peloteGLEtat?window._peloteGLEtat():null; return [r.left+r.width/2, r.top+r.height/2, document.getElementById('device').classList.contains('light'), !!(e&&e.envois)]}")
                if g[3] != (chemin == 'carte graphique'): meds.append(98.0)   # le chemin jugé n'est pas celui qui a peint""")
rj("t('[%s · %s] bord ↔ intérieur voisin : ΔE médian ≤ %.0f' % ('clair' if th == 'light' else 'sombre', pal, SEUIL)","t('[%s · %s · %s] bord ↔ intérieur : ΔE médian ≤ %.0f' % (chemin, 'clair' if th == 'light' else 'sombre', pal, SEUIL)")
io.open('redteam_bord.py','w',encoding='utf-8').write(J)
