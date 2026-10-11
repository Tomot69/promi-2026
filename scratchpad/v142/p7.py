import io
f='promi-moteur.js'; S=io.open(f,encoding='utf-8').read()
def rep(old,new):
    global S
    assert S.count(old)==1, ('motif absent ou multiple', S.count(old), old[:70]); S=S.replace(old,new)
# 1 · le peintre : les cellules vides qu'on ne montre pas, et les boîtes de matière publiées
rep("""    var sp = _uGlobal(ix) * SP_U, RMAX = sp * 2.4;
    if (!env.trans && env.cible == null && env.vive) window._ritComp = [];""",
"""    var sp = _uGlobal(ix) * SP_U, RMAX = sp * 2.4;
    if (!env.trans && env.cible == null && env.vive) window._ritComp = [];
    /* ⚑ v142 (Tom, 11 oct. 2026, C-088) — sous neuf paroles, on ne montre que les dalles et QUELQUES cellules vides (aucune jusqu'à trois
       paroles) : les plus proches des paroles. Les autres ne sont pas peintes — elles bornent toujours les coulées (le semis ne change pas). */
    var VV = (env.cible == null && typeof env.videsVus === 'number') ? env.videsVus : null, VUS = null, BT2 = (!env.trans && env.cible == null && env.vive && VV != null) ? [] : null;
    if (VV != null) { var gx = 0, gy = 0, gn = 0, GR = [], iv;
      for (iv = 0; iv < P.length; iv++) { if (P[iv].s.kind !== 'gray') { if (P[iv].s.part == null) { gx += P[iv].x; gy += P[iv].y; gn++; } } else GR.push(P[iv]); }
      if (gn) { gx /= gn; gy /= gn; GR.sort(function (u, v) { return ((u.x - gx) * (u.x - gx) + (u.y - gy) * (u.y - gy)) - ((v.x - gx) * (v.x - gx) + (v.y - gy) * (v.y - gy)); }); }
      VUS = GR.slice(0, gn ? VV : 0).map(function (u) { return u.s; }); }""")
rep("""      if (env.cible != null && p.s.pid !== env.cible) continue;
      if (p.x < x0 - RMAX || p.x > x1 + RMAX || p.y < y0 - RMAX || p.y > y1 + RMAX) continue;
      var vois = ix.near(p, 10); if (!vois.length) continue;
      var HD = [];""",
"""      if (env.cible != null && p.s.pid !== env.cible) continue;
      if (VUS && p.s.kind === 'gray' && VUS.indexOf(p.s) < 0) continue;   /* v142 : une cellule vide qu'on ne montre pas */
      if (p.x < x0 - RMAX || p.x > x1 + RMAX || p.y < y0 - RMAX || p.y > y1 + RMAX) continue;
      var vois = ix.near(p, 10); if (!vois.length) continue;
      var HD = [];""")
rep("""      var RP = _rampe(p.s, now);
      // v43 : une dalle PARTIE (`part`, posé par le moteur) se retire dans sa cellule, du bord vers le centre""",
"""      /* v142 : la boîte de la MATIÈRE de chaque parole, telle qu'elle est peinte au repos (unités de la Toile) — le cadrage de départ la lit */
      if (BT2 && p.s.kind !== 'gray' && p.s.part == null) { var bx0 = 1e9, by0 = 1e9, bx1 = -1e9, by1 = -1e9;
        for (a = 0; a < NA; a++) { var qx = cx + cs[a] * sm[a], qy = cy + sn[a] * sm[a]; if (qx < bx0) bx0 = qx; if (qx > bx1) bx1 = qx; if (qy < by0) by0 = qy; if (qy > by1) by1 = qy; }
        BT2.push({ s: p.s, sx: p.x, sy: p.y, x0: bx0, y0: by0, x1: bx1, y1: by1 }); }
      var RP = _rampe(p.s, now);
      // v43 : une dalle PARTIE (`part`, posé par le moteur) se retire dans sa cellule, du bord vers le centre""")
rep("""      if (sm !== lim) { tmp = sm; } // les tampons tournent, rien à rendre
      lim = new Float64Array(NA);
    }
  }

  /* ---------- 5 · CABOCHON""",
"""      if (sm !== lim) { tmp = sm; } // les tampons tournent, rien à rendre
      lim = new Float64Array(NA);
    }
    if (BT2) { var sg = BT2.map(function (e) { return [e.x0, e.y0, e.x1, e.y1].map(function (v) { return Math.round(v / 2); }).join(','); }).join('|');
      window._ritBoites = BT2; if (sg !== window._ritBoitesSig) { window._ritBoitesSig = sg; try { if (env.boitesNeuves) env.boitesNeuves(); } catch (_) { } } }
  }

  /* ---------- 5 · CABOCHON""")
# 2 · le contexte
rep("""  get vive(){ return _transVive; },""",
"""  get vive(){ return _transVive; },
  /* ⚑ v142 (C-088) — Ritournelle sous neuf paroles : combien de cellules vides on montre (0 jusqu'à trois paroles, 2 à quatre et cinq, 3 à six et sept, 4 à huit) */
  get videsVus(){ if(theme!=='ritournelle'||!_transVive||_AP||_semisNeuf()) return null; var n=0; for(var i=0;i<seeds.length;i++){ if(seeds[i].kind!=='gray'&&seeds[i].part==null) n++; } return _videsVus(n); },
  boitesNeuves:function(){ if(window._vueMain) return; setTimeout(function(){ try{ if(!window._vueMain){ autoView(); kick(); } }catch(_){ } },0); },""")
rep("""function _boiteSerre(col){ try{""",
"""function _videsVus(n){ return n<=3?0:(n<=5?2:(n<=7?3:4)); }
/* ⚑ v142 (C-088) — la boîte de la MATIÈRE des paroles, telle que le peintre de Ritournelle vient de la peindre (`window._ritBoites`) ;
   null tant qu'une parole n'a pas été peinte à sa place d'aujourd'hui (on cadre alors ses cellules, puis le peintre publie et l'on recadre). */
function _boiteMatiere(col){ try{ var B=window._ritBoites; if(!B||!B.length) return null; var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  for(var i=0;i<col.length;i++){ var c=col[i], e=null; for(var k=0;k<B.length;k++){ if(B[k].s===c){ e=B[k]; break; } }
    if(!e || Math.abs(e.sx-c.x)>3 || Math.abs(e.sy-c.y)>3 || c.wAt) return null;
    if(e.x0<x0)x0=e.x0; if(e.y0<y0)y0=e.y0; if(e.x1>x1)x1=e.x1; if(e.y1>y1)y1=e.y1; }
  return (x1>x0&&y1>y0)?{x0:x0,y0:y0,x1:x1,y1:y1,matiere:1}:null; }catch(_){ return null; } }
function _boiteSerre(col){ try{""")
rep("""  var _bs=_serre?_boiteSerre(col):null;""",
"""  var _bs=_serre?_boiteSerre(col):null;
  /* ⚑ v142 (Tom, 11 oct. 2026, C-088 — RÉCIDIVE) — POURQUOI C'EST REVENU : la boîte des cellules (v141) n'est pas ce qu'on voit. Par le vrai
     chemin (une parole plantée au +), la cellule calculée faisait 234 unités pour 105 de matière : la dalle sortait à 44 % de la largeur ;
     après un rechargement la même parole sortait à 76 %. Le juge de v141 posait ses paroles par `Toile.sync` puis recadrait lui-même.
     On cadre maintenant la MATIÈRE PEINTE (publiée par le peintre), dans la zone visible entre le plateau et la barre. */
  var _bm=(_serre&&theme==='ritournelle')?_boiteMatiere(col):null; if(_bm) _bs=_bm;""")
rep("""  var availW=W*(_bs?(col.length===1?1.18:1.0):0.92), availH=Math.max(1,botB-topB);""",
"""  var availW=W*(_bm?(col.length===1?0.80:0.94):(_bs?(col.length===1?1.18:1.0):0.92)), availH=Math.max(1,botB-topB);""")
rep("""  s=Math.max(1.0, Math.min(s, _serre?(_bs?5.0:3.6):2.0));""","""  s=Math.max(1.0, Math.min(s, _serre?(_bm?7.0:(_bs?5.0:3.6)):2.0));""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
