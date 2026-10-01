# -*- coding: utf-8 -*-
"""Fabrique du bloc lot-AURA-ORBITE.
   python3 fabrique.py            -> ecrit bloc.html + moteur.js (pour l'injection de dev)
   python3 fabrique.py --insere   -> insere le bloc dans app.html, AVANT </body>, motif assert==1
"""
import io, os, sys, hashlib
ICI = os.path.dirname(os.path.abspath(__file__))
APPDIR = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
SRC = os.path.join(APPDIR, 'sauvegardes', 'orbite-velours')
ORDRE = ['_m_base.js', '_v_moteur.js', '_v_iles.js', '_v_semis.js', '_v_peint.js']

def lit(p): return io.open(p, encoding='utf-8').read()
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

# ── la seule retouche : la source de dalle de batIles ──────────────────────────
OLD1 = """    var cv=document.createElement('canvas'), ok=false;
    try{ ok=Toile.dalleGeneree(cv,{monde:I.monde, palette:opt.palette||Toile.getPalette(),
          poly:P, site:[0,0], sp:g*1.05, ci:(_o_h(k*29+3)*4)|0,
          lit:(k*3)%5, ang:_o_h(k*47+9)*Math.PI,
          tone:[1.0,0.76,1.24,0.88,1.12][k%5], pad:10}); }catch(e){}
    if(!ok||!cv.width){ BRUT.push(null); continue; }"""
NEW1 = """    var cv=document.createElement('canvas'), ok=false, _kk=PXR/MAG*dpr, _sx=null, _sy=null;
    /* ⚑ PORTAGE DANS L'APP — 10 septembre 2026. `Toile.dalleGeneree` n'existe que dans
       la COPIE du moteur (scratchpad/toile-extrait.js) : l'ajouter a app.html, ce serait
       toucher le code de la Toile (§9). Dans l'app, une ile EST un Promi reel, qui a deja
       sa vraie dalle : l'appelant la fournit (`opt.dalle`), rendue par
       `Toile.dalleTrame(cv, id, 1, monde)` — la regle 1 du §4, dans le monde de SA
       plantation. Sans `opt.dalle`, le chemin de la planche reste tel quel. */
    if(opt.dalle){
      var _rd=null; try{ _rd=opt.dalle(k,I,g); }catch(e){}
      if(_rd&&_rd.cv&&_rd.cv.width){ cv=_rd.cv; ok=true; _sx=_rd.sx; _sy=_rd.sy;
        if(_rd.kk) _kk=_rd.kk; if(_rd.monde) I.monde=_rd.monde; }
    } else {
    try{ ok=Toile.dalleGeneree(cv,{monde:I.monde, palette:opt.palette||Toile.getPalette(),
          poly:P, site:[0,0], sp:g*1.05, ci:(_o_h(k*29+3)*4)|0,
          lit:(k*3)%5, ang:_o_h(k*47+9)*Math.PI,
          tone:[1.0,0.76,1.24,0.88,1.12][k%5], pad:10}); }catch(e){}
    }
    if(!ok||!cv.width){ BRUT.push(null); continue; }"""
OLD2 = """    BRUT.push({w:cv.width, h:cv.height, d:d,
               sx:cv.__site[0]*dpr, sy:cv.__site[1]*dpr,
               k:PXR/MAG*dpr});"""
NEW2 = """    BRUT.push({w:cv.width, h:cv.height, d:d,
               sx:(_sx!=null?_sx:cv.__site[0]*dpr), sy:(_sy!=null?_sy:cv.__site[1]*dpr),
               k:_kk});"""

# ── la seconde retouche : le peigne tourne AVEC l'objet ─────────────────────────
OLD3 = "  var u=nrmT(B[0],B[1],B[2],x,y,z);"
NEW3 = """  /* ⚑ PORTAGE DANS L'APP — 10 septembre 2026. Sur la planche, B est la direction
     horizontale de L'ÉCRAN, prise à la vue du moment où le cache se remplit : ses deux
     zéros tombent aux limbes gauche et droit. Mais dans l'app l'Orbite TOURNE TOUJOURS :
     un quart de tour plus tard (~41 s), un zéro — un épi, la « couronne » refusée —
     arrive au centre de la face ; et chaque caresse, qui refait le cache, recuisait le
     peigne à la vue du moment : toute la fourrure changeait d'orientation au lâcher.
     Sans B, le peigne est AZIMUTAL autour de l'axe de rotation (u = y × p). Au centre
     de la face il vaut exactement le B de la planche, même sens ; il ne dépend plus de
     la vue ; ses deux zéros sont aux pôles de l'axe, que la rotation lente ne ramène
     jamais de face (théorème de la boule chevelue : on choisit OÙ). */
  var u=B?nrmT(B[0],B[1],B[2],x,y,z):nrmT(z,0,-x,x,y,z);"""
OLD4 = "champPoil(x0,y0,z0,o.tflux||0,_CRN,o.traces)"
NEW4 = "champPoil(x0,y0,z0,o.tflux||0,o.peigneAxial?null:_CRN,o.traces)"
# ── la troisième : la clé du cache ne porte plus les caresses quand l'app les retouche ──
OLD5 = "          +'|t'+(o.traces?o.traces.length+':'+(o.traces[0]?o.traces[0].L.toFixed(3):'0'):'0')"
NEW5 = "          +'|t'+(o.tracesIncr?'i':(o.traces?o.traces.length+':'+(o.traces[0]?o.traces[0].L.toFixed(3):'0'):'0'))"
# ── la quatrième : l'empreinte s'éteint AVEC SA PROFONDEUR (Tom, 10 sept. : « la dernière étape
#    avant que la sphère ne redevienne lisse saute — ça fait cheap, saccadé, non fini ») ────────
#    Trois effets du contact ne dépendaient pas de la profondeur : le poil peigné en rosette
#    (100 %), l'ombre au fond du creux, le poil raccourci d'un cran. Ils restaient ENTIERS
#    jusqu'à la dernière image, puis disparaissaient ensemble. FE = la part d'effet : pleine
#    au-delà de 30 % de la profondeur maximale, puis proportionnelle à la profondeur jusqu'à 0.
PEINT_FE = [
  ("  if(E){\n    var ccx=E.c[0], ccy=E.c[1], ccz=E.c[2], ntch=0;",
   "  /* ⚑ PORTAGE — la part d'effet du contact suit sa PROFONDEUR (voir fabrique.py) */\n"
   "  var FE=E?Math.min(1,(E.d/(E.dmax||1))/0.3):0;\n"
   "  if(E){\n    var ccx=E.c[0], ccy=E.c[1], ccz=E.c[2], ntch=0;"),
  ("        nx=ccx; ny=ccy; nz=ccz; pl=1; rr=1; omb=c1.ombre;",
   "        /* le fond plat, sa normale : ils rejoignent la matière naturelle avec FE */\n"
   "        if(FE<1){ var q1=(1+ph0)*(1-FE); X=X*FE+x*q1; Y=Y*FE+y*q1; Z=Z*FE+z*q1; }\n"
   "        nx=nx*(1-FE)+ccx*FE; ny=ny*(1-FE)+ccy*FE; nz=nz*(1-FE)+ccz*FE;\n"
   "        var mF=nrm3(nx,ny,nz)||1; nx/=mF; ny/=mF; nz/=mF; pl=1; rr=1; omb=c1.ombre;"),
  ("      if(!pl){ X*=rr; Y*=rr; Z*=rr; }",
   "      pei*=FE;                         /* le poil peigné s'éteint avec le creux */\n"
   "      if(!pl){ X*=rr; Y*=rr; Z*=rr; }"),
  ("    if(dedans) lum*=0.20+0.62*lisse(-0.55,0.62,-dOM[i]);",
   "    if(dedans) lum*=1-FE*(1-(0.20+0.62*lisse(-0.55,0.62,-dOM[i])));   /* l'ombre du fond aussi */"),
  ("    if(mo && tai>0) tai--;",
   "    if(mo && tai>0 && (((i*2654435761)>>>0)%1024)/1024 < FE) tai--;   /* le poil raccourci, TRAMÉ */"),
]
# ── la cinquième : en thème clair, la PEAU s'éclaircit sous le poil (Tom, 10 sept. — Q182 : « sol clair,
#    poil sombre — le vrai négatif du thème sombre ; le champ garde sa couleur de nature, c'est la matière
#    qui s'adapte au corps »). `peau()` assombrit la couleur du lieu (× OMB) pour qu'en sombre chaque poil
#    se détache en clair. Avec `o.peauVers = [r, g, b, t]`, elle part vers une couleur claire — la teinte
#    claire de la nature (§1.2) — dans la part t, et chaque poil s'y détache en sombre. Absent : rien ne
#    change (le thème sombre est intact, au pixel).
PEINT_PEAU = [
  ("function peau(B,W,BLOC,OMB){", "function peau(B,W,BLOC,OMB,VERS){"),
  ("      var rr=(sr/sw*OMB)|0, gg=(sg/sw*OMB)|0, bb=(sb/sw*OMB)|0;",
   "      var rr, gg, bb;\n"
   "      if(VERS){ var tv=VERS[3]; rr=(sr/sw*(1-tv)+VERS[0]*tv)|0; gg=(sg/sw*(1-tv)+VERS[1]*tv)|0; bb=(sb/sw*(1-tv)+VERS[2]*tv)|0; }\n"
   "      else { rr=(sr/sw*OMB)|0; gg=(sg/sw*OMB)|0; bb=(sb/sw*OMB)|0; }   /* ⚑ PORTAGE — la peau claire (fabrique.py) */"),
  ("PK=peau(B,W,PB,o.omb);", "PK=peau(B,W,PB,o.omb,o.peauVers);"),
]
# ── l'addition : retoucher les caresses en place, sans refaire le cache ──────────────
RETOUCHE = r"""
/* ════════════════════════════════════════════════════════════════════════════
   ⚑ PORTAGE DANS L'APP — 10 septembre 2026. LA SEULE ADDITION AU MOTEUR.
   Mesuré au profileur : inscrire UNE caresse refaisait tout le cache statique des
   110 000 poils — le relief `phi` compris, qui ne dépend pas des caresses — soit 240 à
   340 ms d'image figée. `retoucheTraces` ne recalcule QUE les points proches des arcs
   qui entrent ou qui sortent, et l'écrit dans le cache compacté (`S.__st`), avec EXACTEMENT
   la logique de la passe statique : champ du poil (peigne azimutal + caresses), lustre de
   la main, sens de l'arc le plus proche au-delà de 0,12 de poli — et une île garde son épi.
   ════════════════════════════════════════════════════════════════════════════ */
function retoucheTraces(ST, anciennes, nouvelles){
  if(!ST) return 0;
  anciennes=anciennes||[]; nouvelles=nouvelles||[];
  var Q=ST.Q, CIX=ST.ci, POL=ST.po, EPW=ST.ew, N=ST.n, ch=[], k, i;
  function dans(L,g){ for(var z=0;z<L.length;z++) if(L[z]===g) return true; return false; }
  for(k=0;k<anciennes.length;k++) if(!dans(nouvelles,anciennes[k])) ch.push(anciennes[k]);
  for(k=0;k<nouvelles.length;k++) if(!dans(anciennes,nouvelles[k])) ch.push(nouvelles[k]);
  if(!ch.length) return 0;
  var CM=[], CR=[];
  for(k=0;k<ch.length;k++){ var g=ch[k], h=g.L/2, c=Math.cos(h), s=Math.sin(h);
    CM.push([g.a[0]*c+g.d[0]*s, g.a[1]*c+g.d[1]*s, g.a[2]*c+g.d[2]*s]);
    CR.push(Math.cos(Math.min(Math.PI, h+g.w+0.05))); }
  var n=0, T=nouvelles;
  for(i=0;i<N;i++){
    var qb=i*10, x0=Q[qb], y0=Q[qb+1], z0=Q[qb+2], pris=false;
    for(k=0;k<CM.length;k++) if(x0*CM[k][0]+y0*CM[k][1]+z0*CM[k][2]>=CR[k]){ pris=true; break; }
    if(!pris) continue;
    n++;
    var fl0=champPoil(x0,y0,z0,0,null,T), fm0=nrm3(fl0[0],fl0[1],fl0[2])||1;
    var fx=fl0[0]/fm0, fy=fl0[1]/fm0, fz=fl0[2]/fm0;
    EPW[i]=(_EPW*255)|0;
    var _po=T.length?m_poli(T,x0,y0,z0):0;
    if(_po>0.12){
      var _gg=null,_bd=9;
      for(var _q=0;_q<T.length;_q++){
        var _G=T[_q];
        var _t=Math.atan2(x0*_G.d[0]+y0*_G.d[1]+z0*_G.d[2], x0*_G.a[0]+y0*_G.a[1]+z0*_G.a[2]);
        if(_t<0)_t=0; else if(_t>_G.L)_t=_G.L;
        var _ct=Math.cos(_t),_st=Math.sin(_t);
        var _qx=_G.a[0]*_ct+_G.d[0]*_st,_qy=_G.a[1]*_ct+_G.d[1]*_st,_qz=_G.a[2]*_ct+_G.d[2]*_st;
        var _dp=x0*_qx+y0*_qy+z0*_qz; if(_dp>1)_dp=1;
        var _an=Math.acos(_dp);
        if(_an<_bd){_bd=_an;_gg=_G;}
      }
      if(_gg){
        var _pd=_gg.d[0]*x0+_gg.d[1]*y0+_gg.d[2]*z0;
        var _tx=_gg.d[0]-_pd*x0,_ty=_gg.d[1]-_pd*y0,_tz=_gg.d[2]-_pd*z0;
        var _tm=Math.hypot(_tx,_ty,_tz)||1;
        fx=_tx/_tm; fy=_ty/_tm; fz=_tz/_tm;
      }
    }
    POL[i]=(_po*255)|0;
    if(CIX[i]===0){ Q[qb+7]=fx; Q[qb+8]=fy; Q[qb+9]=fz; }   /* une île garde son épi */
  }
  return n;
}
"""

def moteur():
    parts = []
    for f in ORDRE:
        s = lit(os.path.join(SRC, f))
        if f == '_v_peint.js':
            assert s.count(OLD3) == 1, 'motif OLD3 absent ou multiple'
            s = s.replace(OLD3, NEW3)
            assert s.count(OLD4) == 1, 'motif OLD4 absent ou multiple'
            s = s.replace(OLD4, NEW4)
            assert s.count(OLD5) == 1, 'motif OLD5 absent ou multiple'
            s = s.replace(OLD5, NEW5)
            for o, nw in PEINT_FE:
                assert s.count(o) == 1, 'motif FE absent ou multiple : %r' % o[:50]
                s = s.replace(o, nw)
            for o, nw in PEINT_PEAU:
                assert s.count(o) == 1, 'motif PEAU absent ou multiple : %r' % o[:50]
                s = s.replace(o, nw)
            s = s + RETOUCHE
        if f == '_v_iles.js':
            assert s.count(OLD1) == 1, 'motif OLD1 absent ou multiple'
            s = s.replace(OLD1, NEW1)
            assert s.count(OLD2) == 1, 'motif OLD2 absent ou multiple'
            s = s.replace(OLD2, NEW2)
        parts.append('/* ──────── %s  (md5 source %s) ──────── */\n%s' % (f, md5(os.path.join(SRC, f)), s))
    corps = '\n'.join(parts)
    assert '</script' not in corps.lower()
    tete = ("/* ════════════════════════════════════════════════════════════════════════════\n"
            "   lot-AURA-ORBITE-MOTEUR — le moteur de l'Orbite (velours), porte tel quel.\n"
            "   Source : sauvegardes/orbite-velours/ — les cinq fichiers, dans l'ordre de la\n"
            "   planche : " + ', '.join(ORDRE) + ".\n"
            "   ⚑ ENFERME DANS UNE FONCTION. Ces fichiers definissent des noms generiques\n"
            "   (D, TAU, mix, hh, fr, peint, verse...) : poses tels quels a la racine d'app.html\n"
            "   ils ecraseraient des globales de l'app. Rien ne sort, sauf window.OrbiteMoteur.\n"
            "   ⚑ UNE SEULE RETOUCHE, dans batIles : la source de dalle (voir le commentaire\n"
            "   « PORTAGE DANS L'APP »). Le moteur de la Toile n'est PAS touche (§9).\n"
            "   ════════════════════════════════════════════════════════════════════════════ */\n")
    exp = ("\ntry{ window.OrbiteMoteur={atlasAlpha:atlasAlpha, GRAIN_POIL:GRAIN_POIL, ORI:ORI, NIVA:NIVA,\n"
           "  NVAR:NVAR, semisPavage:semisPavage, batIles:batIles, peint:peint, m_gestes:m_gestes,\n"
           "  retoucheTraces:retoucheTraces}; }catch(e){}\n")
    return tete + '(function(){\n' + corps + exp + '})();\n'

def bloc():
    css = lit(os.path.join(ICI, 'aura.css'))
    js = lit(os.path.join(ICI, 'aura.js'))
    mot = moteur()
    for x in (css, js): assert '</script' not in x.lower() and '</style' not in x.lower()
    return ('\n<style id="lot-AURA-ORBITE-CSS">\n' + css + '\n</style>\n'
            '<script id="lot-AURA-ORBITE-MOTEUR">\n' + mot + '</script>\n'
            '<script id="lot-AURA-ORBITE">\n' + js + '\n</script>\n')

if __name__ == '__main__':
    B = bloc()
    io.open(os.path.join(ICI, 'moteur.js'), 'w', encoding='utf-8').write(moteur())
    io.open(os.path.join(ICI, 'bloc.html'), 'w', encoding='utf-8').write(B)
    print('bloc : %d octets' % len(B.encode('utf-8')))
    if '--copie' in sys.argv:
        # une app insérée ÉCRITE AILLEURS — pour juger sans toucher à app.html
        dest = sys.argv[sys.argv.index('--copie') + 1]
        # la source : app.html s'il est nu ; sinon la SAUVEGARDE d'avant le lot, vérifiée à l'octet
        # (app.html peut porter une version insérée et verte qu'on ne touche pas pour juger la suivante)
        src = os.path.join(APPDIR, 'app.html')
        if 'lot-AURA-ORBITE' in lit(src):
            src = os.path.join(APPDIR, 'sauvegardes', 'app-avant-aura-orbite.html')
            assert md5(src) == '61280542751d0d0df5bce546f9a091b1', 'la sauvegarde a changé : %s' % md5(src)
        S = lit(src)
        assert 'lot-AURA-ORBITE' not in S, 'la source porte déjà le bloc'
        print('source de la copie :', os.path.relpath(src, APPDIR))
        old = '\n</body>\n'
        assert S.count(old) == 1, 'motif </body> absent ou multiple (%d)' % S.count(old)
        io.open(dest, 'w', encoding='utf-8').write(S.replace(old, '\n' + B + '\n</body>\n'))
        print('copie insérée :', dest, md5(dest))
    if '--insere' in sys.argv:
        app = os.path.join(APPDIR, 'app.html')
        S = lit(app)
        assert 'lot-AURA-ORBITE' not in S, 'le bloc est deja dans app.html'
        old = '\n</body>\n'
        assert S.count(old) == 1, 'motif </body> absent ou multiple (%d)' % S.count(old)
        S = S.replace(old, '\n' + B + '\n</body>\n')
        io.open(app, 'w', encoding='utf-8').write(S)
        print('insere. md5 app.html', md5(app))
