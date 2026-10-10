import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:70]); S=S.replace(o,n)
# 1 · la fourrure d'avant les essais de halo : densité ×1, poil ×1, reflet d'origine
rep("  var REG={densite:3, halo:3, facteur:2, epaisseur:0.7, doux:true, haloRas:14, haloExt:0.12};",
"""  /* ⚑ v140 (Tom, 10 oct. 2026, C-083 — RÉCIDIVE « la Pelote trop rase ») — « la fourrure telle qu'elle était avant les essais de halo :
     douce et soyeuse, avec la longueur, la densité et la souplesse d'alors. » Référence : sauvegardes/app-avant-v114.html. Ce qui l'avait
     rasée : ① v120–v123, la « densité 3 » — deux fois plus de poils, chacun ×0,7 d'épaisseur, reflet adouci : des poils si fins qu'ils
     ne se lisent plus un à un, la boule devient un aplat ; ② v139, la limite franche au rayon de la boule : les pointes des poils (jusqu'à
     5 pt au-delà) coupées net. On revient à la fourrure d'alors : densité ×1 (110 000 → 90 000 → 75 000), poil ×1, reflet d'origine,
     pointes libres au bord (voir `FS2`). */
  var REG={densite:1, halo:3, facteur:1, epaisseur:1, doux:false, haloRas:14, haloExt:0.12};""")
# 2 · la composition du bord, carte graphique
rep("""    '  float fa=uA>0.5 ? 1.0 : f.a; vec3 pm=f.rgb*f.a+uCorps*uA*(1.0-f.a);',
    '  o=vec4(pm*t, fa*t); }'].join('\\n');""",
"""    /* ⚑ v140 (Tom, 10 oct. 2026, C-083) — LES POINTES REVIENNENT, SANS LISERÉ. Le corps est plein jusqu'au rayon de la boule (`t`) ; au-delà,
       seules les pointes des poils dessinent la silhouette, comme avant v114. Deux précautions, mesurées sur des essais : ① la masse des
       poils de profil au-delà du corps est à demi transparente (un anneau pâle) : son opacité est resserrée (0,30 → 0,62) — pleine
       jusqu'aux pointes, puis les pointes ; ② ces pointes prennent la couleur de l'intérieur (poil SUR corps), pas celle du poil seul :
       sinon elles font un anneau d'une autre couleur. Rien d'autre autour. */
    '  float mc=step(0.5,uA), tb=t*mc; float a2=mix(f.a, smoothstep(0.30,0.62,f.a), mc); float al=a2+tb*(1.0-a2);',
    '  vec3 c=f.rgb*f.a+uCorps*mc*(1.0-f.a); float ac=mix(f.a,1.0,mc);',
    '  o=vec4(c*(al/max(ac,0.0001)), al); }'].join('\\n');""")
# 3 · le peintre de secours : la même loi, pixel par pixel sur la couronne
rep("""    g.save(); g.setTransform(1,0,0,1,0,0); g.globalAlpha=1; g.globalCompositeOperation='destination-in'; g.fillStyle='#000000'; g.beginPath(); g.arc(CX,CY,R*(window._peloteBord||1.0),0,6.283185307); g.fill(); g.restore();""",
"""    /* ⚑ v140 (C-083) — la même loi que `FS2` : au-delà du rayon de la boule, l'opacité des pointes est resserrée (0,30 → 0,62) et leur
       couleur est celle de l'intérieur (poil sur corps moyen). La liste des pixels de la couronne est calculée une fois par taille. */
    try{
      if(!cv.__cr || cv.__crW!==W){ var _L=[], _ra=R+0.5, _rb=R*1.09; for(var _yy=0;_yy<W;_yy++) for(var _xx=0;_xx<W;_xx++){ var _rr=Math.hypot(_xx+0.5-CX,_yy+0.5-CY); if(_rr>_ra) _L.push(_rr<_rb ? (_yy*W+_xx) : -(_yy*W+_xx)-1); } cv.__cr=new Int32Array(_L); cv.__crW=W; }
      var _id=g.getImageData(0,0,W,W), _dd=_id.data, _cl=cv.__cr, _mo=cv.__moy||0, _mr=_mo&255, _mgn=(_mo>>>8)&255, _mb=(_mo>>>16)&255;
      for(var _ci=0;_ci<_cl.length;_ci++){ var _k=_cl[_ci]; if(_k<0){ _dd[(-_k-1)*4+3]=0; continue; } _k*=4; var _a=_dd[_k+3]/255; if(_a<=0) continue;
        var _u=(_a-0.30)/0.32; _u=_u<0?0:(_u>1?1:_u); _u=_u*_u*(3-2*_u);
        _dd[_k]=_dd[_k]*_a+_mr*(1-_a); _dd[_k+1]=_dd[_k+1]*_a+_mgn*(1-_a); _dd[_k+2]=_dd[_k+2]*_a+_mb*(1-_a); _dd[_k+3]=Math.round(255*_u); }
      g.putImageData(_id,0,0);
    }catch(_){}""")
rep("""      var _moy=_sn ? ((((_sb/_sn)|0)<<16)|(((_sg/_sn)|0)<<8)|((_sr/_sn)|0)) : 0;""",
"""      var _moy=_sn ? ((((_sb/_sn)|0)<<16)|(((_sg/_sn)|0)<<8)|((_sr/_sn)|0)) : 0; cv.__moy=_moy;""")
io.open('app.html','w',encoding='utf-8').write(S)
