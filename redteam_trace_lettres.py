#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_trace_lettres.py — LE TRACÉ DES LETTRES (C-125, Tom, oct. 2026).

« Au départ aucun texte ; puis les lettres du premier mot SE TRACENT, puis celles du second. » Le trait est NET, comme un rouleau à bord franc ; à la
fin la lettre est EXACTEMENT le glyphe de la police. INTERDIT : fondu, dégradé, opacité intermédiaire (hors anticrénelage d'un pixel), tout le texte
d'un coup. Les chemins suivent R1 (pas de retour en arrière ; un repassage est invisible), R2 (chaque lettre finit vers la droite), R3 (une lettre
commence du côté où la précédente a fini), R5 (les sauts d'un morceau à l'autre sont invisibles).

Ce que ce juge porte EN DUR :
  ① la dernière image est le texte statique, au pixel près (tracé pas à pas, tracé en temps réel, clair et sombre) ; il ne reste ni canevas ni découpe ;
  ② aucune opacité intermédiaire hors du front : sur des images prises en cours de tracé, les pixels dont la couleur n'est ni celle du fond ni une
     des encres pleines (le texte, les trois natures) ne forment jamais une plage — seulement des lisérés d'un ou deux pixels (l'anticrénelage du
     contour des lettres, celui du front) ; le texte statique sert de témoin (il n'en forme pas non plus) ;
  ③ R2 : chaque glyphe de l'alphabet de la page finit dans la moitié droite de son encre (abscisse d'arrivée ≥ 40 % de sa largeur ; un glyphe étroit —
     une seule barre — n'a pas de droite) ; les exceptions sont NOMMÉES ici (IMPOSSIBLE_R2) : une exception nouvelle rougit ;
  ④ R3 : dans les six textes, chaque lettre commence du côté où la précédente a fini, sauf les glyphes qui n'ont pas ce tracé (UN_SEUL_TRACE, nommés
     ici avec leur raison) ; le côté est RECALCULÉ ici depuis la géométrie (milieu de la hauteur d'encre lue dans la police), il n'est pas lu dans les données ;
  ⑤ R1 : la longueur repassée / la longueur tracée, par glyphe ; aucun tracé au-delà de 70 %, la médiane ≤ 25 % ; les pires sont listés ;
  ⑥ jamais tout le texte d'un coup : le nombre de pixels dévoilés part de zéro, ne recule jamais, et aucune des 40 étapes n'en apporte plus de 15 % ;
     en temps réel aussi (captures pendant un tracé à ×0,25).
Le verdict de ①, ② et ⑥ vient de CAPTURES (WebKit, 390 × 844, échelle 3 — banc_tom) ; celui de ③, ④, ⑤ de la géométrie des chemins que le module
rend (TraceLettres.parcours), confrontée à la police elle-même (fontTools) — jamais d'une valeur que les données déclarent sur elles-mêmes.

⚑ v153 (Tom, C-125, RÉCIDIVE : « les lettres font pof, elles apparaissent l'une après l'autre ; ce n'est pas le tracé demandé ; AUCUN flou, AUCUN dégradé,
AUCUNE zone abstraite ») — CE JUGE N'AVAIT RIEN VU, et voici pourquoi : il ne regardait le tracé qu'en PAS À PAS (`va(p)`, 40 étapes) ou en temps réel
à 50 caractères par seconde sans compter les images ; or à 50 car/s une lettre durait ≈ 20 ms, une image à 60 Hz : elle paraissait d'un coup. Et il ne
mesurait la forme du front que par « pas de plage d'alpha intermédiaire » — un coin découpé en triangles (le « g » d'Atkinson) y passait. Ajouté :
  ⑦ LA VITESSE, DANS L'APP (banc comme Tom, le vrai onboarding) : 20 à 25 caractères par seconde (Tom ; défaut 22), mesurée sur l'écran ; `?cps=12` la
     règle (≈ 12) ;
  ⑧ PAS DE « POF » : en temps réel, chaque lettre est EN COURS de tracé pendant 30 ms au moins (médiane ≥ 40 ms) — on la voit se constituer ;
  ⑨ LA GÉOMÉTRIE, image par image, sur o, s, g, en Gilbert ET en Atkinson (les deux polices affichées) — lue sur les pixels du canevas, confrontée au
     chemin de la lettre (TraceLettres.parcours, lissé comme une plume) : la partie dévoilée est toujours un PRÉFIXE CONTINU du chemin (aucun trou
     derrière le front, rien d'avance devant), à l'intérieur du glyphe (aucun pixel hors de la lettre) ; le front, à l'intérieur d'un trait, est
     PERPENDICULAIRE au chemin à ± 10° ; aucune valeur d'alpha intermédiaire hors du bord (un pixel partiel touche toujours l'encre pas encore tracée) ;
  ⑩ `--captures` : une capture fixe dans l'app, à ×0,05 (`?tlv=0.05`), au milieu d'un « o ».
`--sonde=fondu` remplace le tracé par un fondu d'opacité, `--sonde=bloc` par une apparition d'un coup : le juge DOIT rougir (② ou ⑥).
`--fichier=zz-av152.html` (avec le module d'avant : `--module=sauvegardes/trace-lettres-avant-v153.js`) : il DOIT rougir (⑦, ⑧, ⑨).
⚑ v154 (Tom, C-125) — « à 22 car/s on s'endort ; à 50 c'était presque juste, mais une lettre durait une image et sautait. Juste un peu plus lent
qu'à 50 ; le débit et la durée d'une lettre séparés ; au plus trois lettres en cours, de gauche à droite ; AUCUNE onde. » Ce juge porte EN DUR :
  ④ AUCUNE ONDE (remplace R3, retiré par Tom) : chaque lettre prend son tracé naturel — la variante qui part du haut quand le glyphe l'a —, quelle que
     soit la lettre d'avant ; le côté du départ est RECALCULÉ ici depuis la géométrie ;
  ⑪ EN TEMPS DE PLUME, pas à pas à la milliseconde (ne dépend pas de la charge) : le débit des départs 38 à 42 caractères par seconde (une espace compte
     0,4) ; chaque lettre en cours de 60 à 90 ms ; au plus 3 lettres en cours ; elles partent strictement dans l'ordre, de gauche à droite sur une ligne ;
     ET sur les pixels : au moment où le module dit trois lettres en cours, le canevas montre trois lettres partiellement tracées ;
  ⑦ le débit À L'ÉCRAN (le vrai onboarding, horloge du navigateur) : 38 à 42 ; ⑧ chaque lettre en cours sur 4 images au moins — ces deux-là sont des
     cadences : jugées sous une charge de 4 seulement (C-137), sinon « non jugé » avec la valeur ;
  ⑩ `--captures` : une capture fixe dans l'app, à ×0,05, quand deux ou trois lettres sont en cours.
`--module=sauvegardes/trace-lettres-avant-v154.js` : il DOIT rougir (④, ⑪).
⚑ v170 (Tom, C-125 suite : « en PromiLate, l'apparition des lettres n'est pas fluide ni clean » ; Gilbert et Atkinson validés, on n'y touche pas) — ⑫ PROMILATE :
  ⑫a toutes les lettres des textes PromiLate tracés (TEXTES_PL, en dur, avec leur taille de l'échelle), plus À et É composés (v35, v166) et l'apostrophe,
     à leur taille × 1 (la plus grande où elles paraissent) et × 0,79 (la plus petite, réduite comme dans Safari) : les mêmes mesures que ⑨ — préfixe
     continu, aucun éclat, aucune valeur intermédiaire loin du front ; « au bout » (la dernière rangée d'un trait qui finit SUR le bord de la lettre, dans la
     zone de son bout : ce qui reste à tracer est dans le pixel lui-même) est compté à part et rapporté ; le front perpendiculaire se mesure sur l'ensemble
     des lettres (PromiLate est gras : la plupart de ses traits sont plus courts que 2,5 fois leur demi-largeur, ils ne se mesurent pas un à un) ;
  ⑫b la dernière image du tracé d'une lettre TRANSFORMÉE (l'accent retourné du « À », l'accent de l'« É », « Deuxio » penché) est la lettre telle qu'elle
     est à l'écran : pas plus de pixels « grossiers » (encre d'un côté, fond de l'autre) que le témoin, un mot sans transformation (« S’EXPLORE ») ;
  `--chemins-pl=sauvegardes/trace-chemins-promilate-avant-v170.js --module=sauvegardes/trace-lettres-avant-v170.js` (v169b) : il DOIT rougir. `--pl` : ⑫ seul.
Usage : python3 redteam_trace_lettres.py [--port=8752] [--sonde=fondu|bloc] [--captures] [--pl]
"""
import sys, io, json, math, zipfile; sys.path.insert(0, '.')
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
PORT = arg('port', '8752'); SONDE = arg('sonde', ''); CAPT = '--captures' in sys.argv; APP = arg('fichier', 'app.html'); MODULE = arg('module', '')
CPS_MIN, CPS_MAX = 38.0, 42.0     # ⚑ v154 (Tom, C-125) : « juste un peu plus lent qu'à 50 » — 38 à 42, départ à 40 (v153 : 20 à 25)
DUREE_MIN, DUREE_MAX, ACTIVES_MAX, IMAGES_MIN = 60.0, 90.0, 3, 4   # ⚑ v154 : une lettre en cours 60 à 90 ms, au moins 4 images ; 3 lettres en cours au plus
EN_COURS_MIN, EN_COURS_MED = 30.0, 40.0   # ms : une lettre est en cours de tracé assez longtemps pour se voir constituer (à 60 Hz : 2 images et plus)
ANGLE_MAX = 10.0                  # degrés : le front, à l'intérieur d'un trait, perpendiculaire au chemin
PAGE = 'promi-trace-lettres.html'
# ── les exceptions NOMMÉES (une exception qui n'est pas ici fait rougir) ──
IMPOSSIBLE_R2 = {   # le dernier trait ne peut pas finir à droite : la panse se referme sur le fût, à gauche
    'b': 'la panse se referme sur le fût', 'p': 'la panse se referme sur le fût', 'P': 'la panse se referme sur le fût', 'D': 'la panse se referme sur le fût',
    '3': 'ses deux bouts sont à gauche', '7': 'son pied est à gauche (30 % de sa largeur)',
}
UN_SEUL_TRACE = {   # le glyphe n'a qu'un tracé qui finisse à droite (ou il vit tout en haut / tout en bas de la ligne)
    's': 'depuis le haut il finit en bas à gauche', 'S': 'comme le s', 'z': 'depuis le bas : 71 % de repassage', 'Z': 'comme le z',
    'J': 'depuis le haut il finit sur sa crosse, à gauche', 'A': "aucun point de départ dans sa moitié haute (l'arche n'a pas de bout)",
    'Q': 'comme le A : la queue et la panse partent du bas', '6': 'depuis le bas il finit en haut à gauche',
    '1': 'depuis le bas il finit sur son drapeau, à gauche', '8': 'ses deux boucles se nouent au milieu : un seul départ',
    '7': 'depuis le bas il finit en haut à gauche', '2': 'depuis le bas : 76 % de repassage',
    '.': 'tout en bas de la ligne', ',': 'tout en bas de la ligne', '…': 'tout en bas de la ligne', "'": 'tout en haut de la ligne', '’': 'tout en haut de la ligne',
}
R1_MAX, R1_MEDIANE = 0.70, 0.25
# ⚑ v170 — les textes PromiLate que l'onboarding et le guide TRACENT, à leur taille de l'échelle (CLAUDE.md, v148–v151 ; en capitales à l'écran)
TEXTES_PL = [('PROMI', 52), ('PLANTÉ', 42), ('LA SUITE T’APPARTIENT', 32), ('STUDIO', 32.2), ('MONDE COMMENCE TOILE PARTAGE LA', 29),
             ('LE RESTE S’EXPLORE À TON RYTHME', 29), ('PRIMO DEUXIO TERTIO', 25), ('TRACE POUR PLANTER', 19)]
ECH_SAFARI = 0.79
GRAVE = '<span class="v35-e">A<span class="v35-acc" aria-hidden="true" style="top:-.06em;transform:translateX(-70%) scaleX(-1)">\u2019</span></span>'   # le « À » de la phrase 2 (v166)
AIGU = '<span class="v35-e">E<span class="v35-acc" aria-hidden="true">\u2019</span></span>'   # l'« É » de v35
PENCHE = '<span style="display:inline-block;transform:skewX(-3deg)">DEUXIO</span>'   # « Deuxio » (C-124)
CHEMINS_PL = arg('chemins-pl', ''); PL_SEUL = '--pl' in sys.argv
ECHELLES_PL = [0.7466, 0.79]   # ⚑ v170b : la fenêtre de Tom (390 × 651 : l'app réduite à 0,7466) et l'échelle de Safari de la porte de qualité
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:420]), flush=True)

# ── la police, lue dans son archive : la boîte d'encre et la mi-hauteur d'x (le juge ne les demande pas aux données) ──
def police():
    z = zipfile.ZipFile('Polices Promi/gilbert.zip'); nom = next(n for n in z.namelist() if n.endswith('.otf') and 'Color' not in n)
    return TTFont(io.BytesIO(z.read(nom)))
F = police(); CM = F.getBestCmap(); GS = F.getGlyphSet(); MI = (getattr(F['OS/2'], 'sxHeight', 0) or 440) / 2.0
def boite(car):
    bp = BoundsPen(GS); GS[CM[ord(car)]].draw(bp); return bp.bounds
def seuil(bo): return -1e9 if bo[1] >= MI else (1e9 if bo[3] <= MI else (bo[1] + bo[3]) / 2.0)
def cote(y, bo): return 'h' if y >= seuil(bo) else 'b'
def lg(P): return sum(math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]) for i in range(1, len(P)))

SCENE = """(sombre)=>{ document.getElementById('page').style.display='none'; document.getElementById('barre').style.display='none'; let s=document.getElementById('jScene'); if(s) s.remove();
  s=document.createElement('div'); s.id='jScene'; s.style.cssText='position:fixed;left:0;top:0;width:390px;height:520px;z-index:50;background:'+(sombre?'#050302':'#F7F0DE')+';color:'+(sombre?'#F7F0DE':'#291547');
  s.innerHTML='<div id="jBloc" style="position:absolute;left:24px;top:24px;width:342px"><div id="jT" style="font:700 35px/44px Gilbert;letter-spacing:-1.05px;min-height:44px"></div>'+
    '<div id="jP" style="font:700 16px/23px Gilbert;letter-spacing:.01em;margin-top:33px;min-height:23px"></div><div id="jG" style="font:700 30px/1.16 Gilbert;text-align:center;margin-top:30px"></div></div>';
  document.body.appendChild(s); window.JC={}; }"""
# les deux versions fautives : un fondu, une apparition d'un coup (même interface que le module)
SONDES = {
 'fondu': """()=>{ const vrai=TraceLettres.trace; TraceLettres.trace=function(el, segs, o){ o=o||{}; if(o.toutDeSuite) return vrai(el, segs, o); if(segs!=null) vrai(el, segs, {toutDeSuite:true});
     const c={glyphes:[...el.textContent].filter(x=>x.trim()).map(x=>({car:x,variante:'h'})), duree:1500, fini:false}; let fin; c.fin=new Promise(r=>fin=r); c.pret=Promise.resolve(c); el.style.opacity='0';
     c.va=p=>{ el.style.opacity=String(Math.max(0,Math.min(1,p))); }; c.finir=c.stop=()=>{ el.style.opacity=''; c.fini=true; fin({}); }; c.etat=()=>({});
     if(!o.manuel){ const t0=performance.now(), d=c.duree/((o.vitesse||1)); (function f(){ const p=(performance.now()-t0)/d; if(p>=1){ c.finir(); return; } c.va(p); requestAnimationFrame(f); })(); } return c; }; }""",
 'bloc': """()=>{ const vrai=TraceLettres.trace; TraceLettres.trace=function(el, segs, o){ o=o||{}; if(o.toutDeSuite) return vrai(el, segs, o); if(segs!=null) vrai(el, segs, {toutDeSuite:true});
     const c={glyphes:[...el.textContent].filter(x=>x.trim()).map(x=>({car:x,variante:'h'})), duree:1500, fini:false}; let fin; c.fin=new Promise(r=>fin=r); c.pret=Promise.resolve(c); el.style.visibility='hidden';
     c.va=p=>{ el.style.visibility=p>=0.5?'':'hidden'; }; c.finir=c.stop=()=>{ el.style.visibility=''; c.fini=true; fin({}); }; c.etat=()=>({});
     if(!o.manuel){ const t0=performance.now(), d=c.duree/((o.vitesse||1)); (function f(){ const p=(performance.now()-t0)/d; if(p>=1){ c.finir(); return; } c.va(p); requestAnimationFrame(f); })(); } return c; }; }""",
}
CLIP = {'x': 0, 'y': 0, 'width': 390, 'height': 520}
def img(pg): return np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=CLIP))).convert('RGB')).astype(np.int16)
def ecart(a, b): return np.abs(a - b).max(2)
ENCRES = [(0x29, 0x15, 0x47), (0x82, 0xAE, 0xF8), (0xFF, 0xB8, 0xD2), (0xC9, 0xA8, 0xF5)]      # le texte en clair, Promi, Chiche, Cercle
def intermediaire(m, vide, tol=26):
    """les pixels qui ne sont ni le fond ni une encre pleine : une couverture partielle (anticrénelage) — ou un fondu"""
    i = ecart(m, vide) > tol
    for c in ENCRES: i &= np.abs(m - np.array(c, np.int16)).max(2) > tol
    return i
def erode(m):
    """un pixel reste s'il est entouré de huit pixels du masque : une plage, pas un liséré"""
    o = m.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1): o &= np.roll(np.roll(m, dy, 0), dx, 1)
    return o

NGEO = 36
GEO = """async a=>{ const [pol,gr,car,N]=a, fz=a[4]||150, html=a[5]||null; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
  const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:60px;top:60px;width:300px;font:'+gr+' '+fz+'px/'+(fz*1.2)+'px '+pol+';color:#291547;background:none;z-index:60'; if(html) el.innerHTML=html; else el.textContent=car; document.body.appendChild(el);
  await document.fonts.load(gr+' '+fz+'px '+pol); await document.fonts.ready;
  const C=TraceLettres.trace(el, null, {manuel:true, respecteReduire:false}); await C.pret; const cv=C.canevas; if(!cv||!C.va){ try{C.stop()}catch(e){} el.remove(); return null; }
  const W=cv.width, H=cv.height, n=W*H, g2=cv.getContext('2d'); const lit=()=>{ const d=g2.getImageData(0,0,W,H).data, o=new Uint8Array(n); for(let i=0;i<n;i++) o[i]=d[4*i+3]; return o; };
  C.va(0.99999); const ref=lit(); const R=new Uint8Array(n).fill(255), isl=new Uint8Array(n), age=new Uint8Array(n); let hors=0, loin=0, part=0, ilots=0, ilotMax=0; const LP=[];
  for(let i=1;i<N;i++){ C.va(i/N); const cur=lit(); let pi=0; const unr=new Uint8Array(n);
    for(let p=0;p<n;p++){ if(ref[p]>127 && cur[p]<=10) unr[p]=1; if(cur[p]>ref[p]+10) hors++; if(ref[p]>200 && cur[p]>=ref[p]-10 && R[p]===255) R[p]=i; }
    /* un pixel partiel est AU BORD du dévoilement s'il touche (à 2 px) un pixel d'encre vierge ou MOINS teint que lui ; un point gris entouré de pixels
       pleins ne l'est pas */
    let li=0; for(let y=0;y<H;y++) for(let x=0;x<W;x++){ const p=y*W+x; if(!(ref[p]>0 && cur[p]>10 && cur[p]<ref[p]-10)) continue; pi++; let v=false; const rp=cur[p]/ref[p];
      for(let dy=-2;dy<=2&&!v;dy++) for(let dx=-2;dx<=2&&!v;dx++){ const xx=x+dx, yy=y+dy; if(xx<0||yy<0||xx>=W||yy>=H) continue; const q=yy*W+xx; if(unr[q] || (ref[q]>127 && cur[q]/ref[q] < rp-0.05)) v=true; } if(!v){ li++; if(LP.length<4000){ let bd=false; for(let dy=-2;dy<=2&&!bd;dy++) for(let dx=-2;dx<=2&&!bd;dx++){ const xx=x+dx, yy=y+dy; if(xx<0||yy<0||xx>=W||yy>=H||ref[yy*W+xx]<=127) bd=true; } LP.push([i,x,y,bd?1:0]); } } }
    loin=Math.max(loin,li); part=Math.max(part,pi);
    /* les ÎLOTS : des morceaux d'encre pas encore tracée, petits (12 px à 1,5 % de la lettre) et séparés du reste, pendant qu'il en reste plus de 10 %
       — un éclat qui attend la fin pendant que la lettre avance (le coin du « g » d'Atkinson, v152) */
    let nu=0, tot=0; for(let p=0;p<n;p++){ if(ref[p]>200){ tot++; if(cur[p]<=10) nu++; } }
    if(nu>0.10*tot){ const lab=new Int32Array(n), st=[]; let nl=0;
      for(let p0=0;p0<n;p0++){ if(lab[p0]||!(ref[p0]>200&&cur[p0]<=10)) continue; nl++; let sz=0; st.push(p0); lab[p0]=nl;
        while(st.length){ const p=st.pop(); sz++; const x=p%W, y=(p-x)/W; for(let dy=-1;dy<=1;dy++) for(let dx=-1;dx<=1;dx++){ const xx=x+dx, yy=y+dy; if(xx<0||yy<0||xx>=W||yy>=H) continue; const q=yy*W+xx; if(!lab[q] && ref[q]>200 && cur[q]<=10){ lab[q]=nl; st.push(q); } } }
        if(sz>=12 && sz<=0.015*tot){ for(let p=0;p<n;p++) if(lab[p]===nl) isl[p]=1; } } }
    /* un ÉCLAT est un îlot qui RESTE en arrière : le même pixel isolé trois images de suite (le bout d'un trait juste devant le front ne dure qu'une image) */
    for(let p=0;p<n;p++){ age[p]=isl[p]?age[p]+1:0; if(age[p]>=3){ ilots++; ilotMax=Math.max(ilotMax, age[p]); } isl[p]=0; } }
  const b64=u=>{ let s=''; for(let i=0;i<u.length;i+=8192) s+=String.fromCharCode.apply(null, u.subarray(i,i+8192)); return btoa(s); };
  const cr=cv.getBoundingClientRect(), er=el.getBoundingClientRect(), d=devicePixelRatio, TR=[];
  /* v170 : les traits de TOUS les glyphes (un « À » composé en a deux), sous la matrice de leur élément (l'accent retourné) */
  C.glyphes.forEach(gl=>{ if(!gl.ech) return; const pc=TraceLettres.parcours(pol, gl.car, gl.variante); if(!pc) return; const M=gl.mat||[1,0,0,1], o2=gl.xo||[gl.x,gl.y], gx=(er.left+o2[0]-cr.left)*d, gy=(er.top+o2[1]-cr.top)*d, u=gl.ech*d;
    pc.traits.forEach(t=>TR.push({R:t.R*u, pts:t.pts.map(q=>[gx+(M[0]*q[0]-M[2]*q[1])*u, gy+(M[1]*q[0]-M[3]*q[1])*u])})); });
  C.stop(); el.remove();
  return {w:W, h:H, N:N, ref:b64(ref), R:b64(R), hors, loin, part, ilots, ilotMax, LP, traits:TR}; }"""
ENREG = """()=>{ window.__TL=[]; window.__CTL=[]; const T=window.TraceLettres; const tr=T.trace; T.trace=function(c, ct, o){ if(o && o.preparer) return tr.apply(this, arguments);   /* v170d : une préparation d'avance ne montre rien — ce n'est pas un texte tracé */
    const ctl=tr.apply(this, arguments); const k=window.__CTL.push(ctl)-1;
    const txt=(c.textContent||''); const r={id:c.id||'', k:k, ctl:true, n:[...txt].filter(x=>x.trim()).length, esp:(txt.trim().match(/\\s+/g)||[]).length, images:[]}; window.__TL.push(r);
    ctl.pret.then(()=>{ r.debut=performance.now(); (function f(){ if(ctl.fini){ r.fin=r.fin||performance.now(); return; } const e=ctl.etat(); r.images.push([performance.now(), e.actives || [e.glyphe]]); requestAnimationFrame(f); })(); });
    ctl.fin.then(()=>{ r.fin=performance.now(); }); return ctl; }; }"""
def b64u8(s, w, h):
    import base64
    return np.frombuffer(base64.b64decode(s), np.uint8).reshape(h, w).astype(float)
def chaikin(P):
    a0, b0 = P[0], P[-1]; Lk = math.hypot(b0[0] - a0[0], b0[1] - a0[1]); ec = 0
    for q in P[1:-1]:
        if Lk > 0: ec = max(ec, abs((q[0] - a0[0]) * (b0[1] - a0[1]) - (q[1] - a0[1]) * (b0[0] - a0[0])) / Lk)
    if len(P) < 3 or (Lk > 0 and ec < 0.6): return P
    for _ in range(2):
        Q = [P[0]]
        for j in range(len(P) - 1):
            u0, u1 = P[j], P[j + 1]
            if j > 0: Q.append([0.75 * u0[0] + 0.25 * u1[0], 0.75 * u0[1] + 0.25 * u1[1]])
            if j < len(P) - 2: Q.append([0.25 * u0[0] + 0.75 * u1[0], 0.25 * u0[1] + 0.75 * u1[1]])
        Q.append(P[-1]); P = Q
    return P
def projette(T, w, h):
    ys, xs = np.mgrid[0:h, 0:w]; px = xs + 0.5; py = ys + 0.5
    best = np.full((h, w), np.inf); S_ = np.zeros((h, w)); K = np.full((h, w), -1); s0 = 0.0; bornes = []
    for k, t in enumerate(T):
        P = t['pts']; acc = 0.0
        for i in range(len(P) - 1):
            ax, ay = P[i]; bx, by = P[i + 1]; vx, vy = bx - ax, by - ay; L = math.hypot(vx, vy)
            if L < 1e-9: continue
            u = np.clip(((px - ax) * vx + (py - ay) * vy) / (L * L), 0, 1); dx = px - (ax + u * vx); dy = py - (ay + u * vy); d2 = dx * dx + dy * dy
            m = d2 < best; best[m] = d2[m]; S_[m] = s0 + acc + u[m] * L; K[m] = k; acc += L
        bornes.append((s0, s0 + acc)); s0 += acc
    return S_, np.sqrt(best), K, bornes
def point(P, s):
    acc = 0.0
    for i in range(len(P) - 1):
        L = math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
        if acc + L >= s and L > 0: u = (s - acc) / L; return (P[i][0] + u * (P[i + 1][0] - P[i][0]), P[i][1] + u * (P[i + 1][1] - P[i][1]))
        acc += L
    return tuple(P[-1])
def geo_analyse(r):
    """la géométrie du tracé d'une lettre, lue sur les pixels : préfixe du chemin, alpha franc, front perpendiculaire (à l'intérieur des traits)"""
    w, h, N = r['w'], r['h'], r['N']; ref = b64u8(r['ref'], w, h); R = b64u8(r['R'], w, h); T = r['traits']
    for t in T: t['pts'] = chaikin(t['pts'])
    S_, dist, K, bornes = projette(T, w, h); Rm = max(t['R'] for t in T)
    autre = np.full((h, w), np.inf)
    if len(T) > 1:
        for kk in range(len(T)):
            _, dx_, _, _ = projette([t for j, t in enumerate(T) if j != kk], w, h); m_ = (K == kk); autre[m_] = dx_[m_]
    ys, xs = np.mgrid[0:h, 0:w]; amb = np.zeros((h, w), bool)
    for t in T:
        for q in (t['pts'][0], t['pts'][-1]): amb |= np.hypot(xs + 0.5 - q[0], ys + 0.5 - q[1]) < 2.6 * t['R'] + 3   # la zone d'un bout (un coin, une tête de fût que le chemin ne parcourt pas) : la règle du coin, pas celle du préfixe
    core = ref > 200; out = {'ilots': r['ilots'], 'ilotMax': r['ilotMax'], 'hors': r['hors'], 'loin': r['loin'], 'partiels': r['part'], 'trous': 0, 'avance': 0, 'pas': 0, 'angles': []}
    # ⚑ v170b (Tom) : la définition « au bout » de v170 est REFUSÉE — un pixel partiel qui ne touche pas l'encre non tracée est « loin », partout.
    for i in range(1, N):
        rev = core & (R <= i); unr = core & (R > i)
        if rev.sum() < 30 or unr.sum() < 30: continue
        out['pas'] += 1; tol = Rm + 3; zone = core & ~amb & (dist < Rm * 1.6)
        Sz = S_[zone]; Rz = rev[zone]; o_ = np.argsort(Sz); lab = Rz[o_]
        err = np.concatenate([[0], np.cumsum(~lab)]) + np.concatenate([np.cumsum(lab[::-1])[::-1], [0]]); j = int(np.argmin(err))
        sf = float(Sz[o_][min(j, len(o_) - 1)]) if len(o_) else 0
        out['trous'] = max(out['trous'], int((zone & ~rev & (S_ < sf - tol)).sum())); out['avance'] = max(out['avance'], int((zone & rev & (S_ > sf + tol)).sum()))
        for k, (a, b2) in enumerate(bornes):
            if not (a <= sf <= b2): continue
            Rk = T[k]['R']
            if min(sf - a, b2 - sf) < 2.5 * Rk: break
            p0 = point(T[k]['pts'], max(0, sf - a - Rk)); p1 = point(T[k]['pts'], min(b2 - a, sf - a + Rk)); tx, ty = p1[0] - p0[0], p1[1] - p0[1]; tl = math.hypot(tx, ty) or 1; tx /= tl; ty /= tl
            pad = np.pad(unr, 1); vu = np.zeros_like(unr)
            for dy in (0, 1, 2):
                for dx in (0, 1, 2): vu |= pad[dy:dy + h, dx:dx + w]
            bord = rev & vu & (np.abs(S_ - sf) <= tol) & (K == k) & (autre > Rk * 2.5)
            yy, xx = np.nonzero(bord)
            if len(xx) < max(6, 0.8 * Rk): break
            sc = float(np.median(S_[bord]))   # la tangente se prend LÀ OÙ EST le front (son milieu sur le chemin), pas à l'abscisse de la coupe
            if min(sc - a, b2 - sc) < 2.5 * Rk: break
            p0 = point(T[k]['pts'], max(0, sc - a - Rk)); pm = point(T[k]['pts'], sc - a); p1 = point(T[k]['pts'], min(b2 - a, sc - a + Rk)); tx, ty = p1[0] - p0[0], p1[1] - p0[1]; tl = math.hypot(tx, ty) or 1; tx /= tl; ty /= tl
            # hors des COUDES : là où le chemin tourne de plus de 20° sur une largeur de trait, le front PIVOTE en éventail (la règle du module) — on ne le mesure pas
            ua = math.atan2(pm[1] - p0[1], pm[0] - p0[0]); ub = math.atan2(p1[1] - pm[1], p1[0] - pm[0]); dv = abs((math.degrees(ub - ua) + 180) % 360 - 180)
            if dv > 20: out['coudes'] = out.get('coudes', 0) + 1; break
            pts = np.stack([xx, yy], 1).astype(float); pts -= pts.mean(0); _, _, vt = np.linalg.svd(pts, full_matrices=False); d = vt[0]
            out['angles'].append(round(90 - math.degrees(math.acos(min(1, abs(d[0] * tx + d[1] * ty)))), 1)); break
    return out

def section_pl(b, err):
    """⑫ (v170b) : PromiLate, mesuré sur l'ÉCRAN (captures), à la fenêtre de Tom — 390 × 651, l'app réduite à 0,7466 — et à 0,79, en WebKit.
    Depuis v170b le tracé de PromiLate dévoile le texte réel par une découpe vectorielle : il n'y a plus de canevas à lire, on lit les pixels de l'écran."""
    for ech in ECHELLES_PL:
        ctxp = B.contexte(b, vw=390, vh=651); pgp = ctxp.new_page(); pgp.on('pageerror', lambda e: err.append(str(e)[:200]))
        pgp.goto('http://127.0.0.1:%s/%s' % (PORT, APP)); pgp.wait_for_timeout(7000)
        pgp.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }")
        pgp.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
        if CHEMINS_PL: pgp.add_script_tag(url='http://127.0.0.1:%s/%s' % (PORT, CHEMINS_PL))
        if MODULE: pgp.add_script_tag(url='http://127.0.0.1:%s/%s' % (PORT, MODULE))
        pgp.wait_for_timeout(300)
        if SONDE: pgp.evaluate(SONDES[SONDE])
        E = '%s' % ('0,7466 (Tom)' if abs(ech - 0.7466) < 1e-3 else str(ech).replace('.', ','))
        tailles = {}
        for t, fz in TEXTES_PL:
            for c in t.replace(' ', ''): tailles.setdefault(c, set()).add(round(fz))
        CAS = [(c, c, fz) for c in sorted(tailles) if c not in 'ÀÉ' for fz in sorted(tailles[c])] + [('À', GRAVE, 29), ('É', AIGU, 42), ('Deuxio penché', PENCHE, 25)]
        angles, nres, pires = [], [], {}
        for nom, html, fz in CAS:
            o = geo_ecran(pgp, html, fz, ech)
            lib = '⑫a PromiLate « %s » à %d pt (échelle %s)' % (nom, fz, E)
            if not o: juge(lib + ' : le tracé se mesure', False, 'aucune mesure'); continue
            simple = html == nom
            angles += o['angles'] if simple else []
            juge(lib + ' — %s aucun éclat, aucun creux qui reste (fente, entaille, marche), aucune valeur intermédiaire loin du front' % ('préfixe continu,' if simple else 'rien hors de la lettre,'),
                 o['hors'] == 0 and (not simple or (o['trous'] <= 30 and o['avance'] <= 30)) and o['ilots'] == 0 and o['creux'] == 0 and o['loin'] <= 3 and o['pas'] >= 12,
                 'hors %d ; trou %d ; avance %d ; éclats %d (le plus long %d images) ; creux qui restent %d px ; loin %d ; %d images' % (o['hors'], o['trous'], o['avance'], o['ilots'], o['ilotMax'], o['creux'], o['loin'], o['pas']))
            juge(lib + ' — la dernière image du tracé est le texte réel, au pixel', o['fin'] == 0, '%d pixel(s) différent(s) à 99,999 %% du tracé' % o['fin'])
            nres.append(o['reso'])
        juge('⑫c résolution (échelle %s) — le canevas du tracé a exactement la taille de l\'écran : largeur et hauteur = taille CSS affichée × DPR, calé sur un pixel de l\'appareil' % E,
             nres and all(r['ok'] for r in nres), [r for r in nres if not r['ok']][:2] or ('%d tracés, DPR %s' % (len(nres), nres[0]['dpr'] if nres else '?')))
        juge('⑫a PromiLate (échelle %s) — le front, à l\'intérieur d\'un trait, est perpendiculaire au chemin (± %d°), sur l\'ensemble des lettres (3 mesures au moins)' % (E, ANGLE_MAX),
             len(angles) >= 3 and max(map(abs, angles)) <= ANGLE_MAX, '%d mesures ; pire %.1f°' % (len(angles), max(map(abs, angles)) if angles else -1))
        ctxp.close()

GEO_ECRAN = """async a=>{ const [html,fz,ech,f]=a; let w=document.getElementById('gW'); if(!w){ w=document.createElement('div'); w.id='gW'; w.style.cssText='position:fixed;left:20px;top:20px;transform-origin:0 0;z-index:60;background:#fff'; document.body.appendChild(w); }
  w.style.transform='scale('+ech+')'; if(f==='pose'){ w.innerHTML=''; const el=document.createElement('div'); el.id='gEl'; el.style.cssText='width:300px;font:400 '+fz+'px/1.25 PromiLate;color:#291547;padding:8px 12px'; el.innerHTML=html; w.appendChild(el);
    await document.fonts.load('400 '+fz+'px PromiLate'); await document.fonts.ready; const r=w.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; }
  const el=document.getElementById('gEl');
  if(f==='arme'){ const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret; window.__CG=C; const cv=C.canevas, d=devicePixelRatio;
    let reso={ok:true,dpr:d}; if(cv){ const q=cv.getBoundingClientRect(); reso={ok: Math.abs(cv.width-q.width*d)<0.6 && Math.abs(cv.height-q.height*d)<0.6 && Math.abs(q.left*d-Math.round(q.left*d))<0.05 && Math.abs(q.top*d-Math.round(q.top*d))<0.05, W:cv.width, w:+(q.width*d).toFixed(2), H:cv.height, h:+(q.height*d).toFixed(2), x:+(q.left*d).toFixed(3), y:+(q.top*d).toFixed(3), dpr:d}; }
    const er=el.getBoundingClientRect(), k=er.width/el.offsetWidth, TR=[];
    C.glyphes.forEach(gl=>{ if(!gl.ech) return; const pc=TraceLettres.parcours('PromiLate', gl.car, gl.variante); if(!pc) return; const M=gl.mat||[1,0,0,1], o2=gl.xo||[gl.x,gl.y], gx=(er.left+o2[0]*k)*d, gy=(er.top+o2[1]*k)*d, u=gl.ech*k*d;
      pc.traits.forEach(t=>TR.push({R:t.R*u, pts:t.pts.map(q=>[gx+(M[0]*q[0]-M[2]*q[1])*u, gy+(M[1]*q[0]-M[3]*q[1])*u])})); });
    /* v170b : la boîte d'encre de chaque glyphe (pour savoir, à chaque pas, quelles lettres ont commencé) */
    const GB=C.glyphes.map(gl=>{ if(!gl.ech) return null; const pc=TraceLettres.parcours('PromiLate', gl.car, gl.variante); if(!pc) return null; const M=gl.mat||[1,0,0,1], o2=gl.xo||[gl.x,gl.y], gx=(er.left+o2[0]*k)*d, gy=(er.top+o2[1]*k)*d, u=gl.ech*k*d, b=pc.boite;
      const P=[[b[0],b[1]],[b[2],b[1]],[b[0],b[3]],[b[2],b[3]]].map(q=>[gx+(M[0]*q[0]-M[2]*q[1])*u, gy+(M[1]*q[0]-M[3]*q[1])*u]); return [Math.min(...P.map(q=>q[0])), Math.min(...P.map(q=>q[1])), Math.max(...P.map(q=>q[0])), Math.max(...P.map(q=>q[1]))]; });
    return {reso, TR, GB}; }
  window.__CG.va(f); const e=window.__CG.etat(); return {ig:e.glyphe, act:e.actives||[]}; }"""

def geo_ecran(pg, html, fz, ech, N=NGEO):
    """les mêmes mesures que ⑨, lues sur les CAPTURES de l'écran (l'encre = la couleur du texte sur le blanc), plus les creux qui restent"""
    r = pg.evaluate(GEO_ECRAN, [html, fz, ech, 'pose']); pg.wait_for_timeout(60)
    clip = {'x': r['x'], 'y': r['y'], 'width': r['w'], 'height': r['h']}
    def lit():
        im = np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(float)
        return np.clip((255 - im) / (255 - 24.0) * 255, 0, 255)   # #291547 sur blanc : luminance ≈ 24
    ref = lit()
    A = pg.evaluate(GEO_ECRAN, [html, fz, ech, 'arme'])
    h, w = ref.shape; d = 3.0; X0, Y0 = clip['x'] * d, clip['y'] * d
    for t in A['TR']: t['pts'] = [[p[0] - X0, p[1] - Y0] for p in t['pts']]
    GB = [None if g is None else [g[0] - X0, g[1] - Y0, g[2] - X0, g[3] - Y0] for g in A.get('GB', [])]
    Rm = np.full((h, w), 255, np.uint8); age = np.zeros((h, w), np.uint8); pinc = np.zeros((h, w), np.uint8)
    out = {'hors': 0, 'loin': 0, 'ilots': 0, 'ilotMax': 0, 'creux': 0, 'reso': A['reso']}
    def composantes(m):
        """les composantes (8-connexes) d'un masque : une liste de (taille, masque)"""
        vu = np.zeros_like(m); res_ = []; H_, W_ = m.shape; pts = np.argwhere(m)
        for y0, x0 in pts:
            if vu[y0, x0]: continue
            st = [(y0, x0)]; vu[y0, x0] = True; mem = []
            while st:
                y_, x_ = st.pop(); mem.append((y_, x_))
                for dy_ in (-1, 0, 1):
                    for dx_ in (-1, 0, 1):
                        yy, xx = y_ + dy_, x_ + dx_
                        if 0 <= yy < H_ and 0 <= xx < W_ and m[yy, xx] and not vu[yy, xx]: vu[yy, xx] = True; st.append((yy, xx))
            res_.append(mem)
        return res_
    core = ref > 200; tot = int(core.sum())
    def dec(m, dx, dy):
        o = np.zeros_like(m); ys = slice(max(0, dy), h + min(0, dy)); yd = slice(max(0, -dy), h + min(0, -dy)); xs = slice(max(0, dx), w + min(0, dx)); xd = slice(max(0, -dx), w + min(0, -dx)); o[yd, xd] = m[ys, xs]; return o
    for i in range(1, N):
        et = pg.evaluate(GEO_ECRAN, [html, fz, ech, i / N]); cur = lit()
        commencees = set(range(et['ig'])) | set(et['act']) if isinstance(et, dict) else set(range(len(GB)))
        out['hors'] += int((cur > ref + 12).sum())
        if i == N - 1: pass
        Rm[(core) & (cur >= ref - 10) & (Rm == 255)] = i
        unr = (ref > 127) & (cur <= 10)
        part = (ref > 0) & (cur > 10) & (cur < ref - 10); rp = np.where(ref > 0, cur / np.maximum(ref, 1), 0)
        voisin = np.zeros((h, w), bool)
        moins = (ref > 127)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                voisin |= dec(unr, dx, dy) | (dec(moins, dx, dy) & (dec(rp, dx, dy) < rp - 0.05))
        out['loin'] = max(out['loin'], int((part & ~voisin).sum()))
        # les éclats : de l'encre non tracée, petite et isolée, laissée en arrière trois images ou plus
        nu = int((core & (cur <= 10)).sum()); isl = np.zeros((h, w), bool)
        if nu > 0.10 * tot:
            for mem in composantes(core & (cur <= 10)):
                # ⚑ v170b (Tom) — UNE ENCRE QUI APPARTIENT À UNE LETTRE PAS ENCORE COMMENCÉE (l'accent du « À », glyphe suivant) N'EST PAS UN ÉCLAT LAISSÉ EN ARRIÈRE.
                cy_ = sum(m[0] for m in mem) / len(mem); cx_ = sum(m[1] for m in mem) / len(mem)
                dans = lambda g: g is not None and g[0] - 1 <= cx_ <= g[2] + 1 and g[1] - 1 <= cy_ <= g[3] + 1
                cand = [(abs((g[2] - g[0]) * (g[3] - g[1])), j) for j, g in enumerate(GB) if dans(g)]   # la plus petite boîte qui la contient : sa lettre
                if cand and min(cand)[1] not in commencees: continue
                if 12 <= len(mem) <= 0.015 * tot:
                    for y_, x_ in mem: isl[y_, x_] = True
        age = np.where(isl, age + 1, 0).astype(np.uint8); out['ilots'] += int((age >= 3).sum()); out['ilotMax'] = max(out['ilotMax'], int(age.max()))
        # ⚑ v170b — LES CREUX QUI RESTENT : de l'encre non dévoilée PINCÉE entre deux parts déjà dévoilées (à 3 px de part et d'autre, dans une même
        # direction) — une fente, une entaille, une marche ; le front qui avance n'a d'encre dévoilée que d'un côté. Compté s'il reste deux images de suite
        # (un front qui referme un écart ne pince un pixel qu'un instant).
        rev = (ref > 127) & (cur >= ref * 0.9); nd = (ref > 200) & (cur < ref * 0.5); pin = np.zeros((h, w), bool)
        for dx, dy in ((1, 0), (0, 1), (1, 1), (1, -1)):
            a1 = np.zeros((h, w), bool); a2 = np.zeros((h, w), bool)
            for s_ in (1, 2, 3): a1 |= dec(rev, dx * s_, dy * s_); a2 |= dec(rev, -dx * s_, -dy * s_)
            pin |= nd & a1 & a2
        pinc = np.where(pin, pinc + 1, 0).astype(np.uint8); out['creux'] = max(out['creux'], int((pinc >= 2).sum()))
    pg.evaluate(GEO_ECRAN, [html, fz, ech, 0.99999]); fin = lit(); out['fin'] = int((np.abs(fin - ref) > 12).sum())
    pg.evaluate("()=>{ if(window.__CG){ window.__CG.stop(); window.__CG=null; } }")
    # le préfixe et l'angle : l'analyse de ⑨, sur la carte des instants lue à l'écran
    import base64
    rr = {'w': w, 'h': h, 'N': N, 'ref': base64.b64encode(ref.astype(np.uint8).tobytes()).decode(), 'R': base64.b64encode(Rm.tobytes()).decode(),
          'hors': out['hors'], 'loin': out['loin'], 'part': 0, 'ilots': out['ilots'], 'ilotMax': out['ilotMax'], 'traits': A['TR']}
    g = geo_analyse(rr)
    for k_ in ('trous', 'avance', 'pas', 'angles', 'coudes'): out[k_] = g.get(k_, 0)
    return out

with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); err = []
    if PL_SEUL:
        section_pl(b, err); b.close(); n_ok = sum(1 for _, c in res if c); print('\n%d / %d' % (n_ok, len(res))); sys.exit(0 if n_ok == len(res) else 1)
    pg.on('pageerror', lambda e: err.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%s/%s' % (PORT, PAGE)); pg.wait_for_timeout(1500)
    if MODULE: pg.add_script_tag(url='http://127.0.0.1:%s/%s' % (PORT, MODULE)); pg.wait_for_timeout(300); print('— MODULE « %s » —' % MODULE)
    if SONDE: pg.evaluate(SONDES[SONDE]); print('— SONDE « %s » : le tracé est remplacé par une version fautive —' % SONDE)
    P = pg.evaluate("()=>PASSAGES.map(p=>p.segs)"); ALPHA = pg.evaluate("()=>ALPHABET.join('')")
    T, P2, G1 = P[0], P[2], P[4]
    def pose(sombre=False):
        pg.evaluate(SCENE, sombre); pg.wait_for_timeout(120); vide = img(pg)
        pg.evaluate("a=>{ TraceLettres.trace(document.getElementById('jT'), a[0], {toutDeSuite:true}); TraceLettres.trace(document.getElementById('jP'), a[1], {toutDeSuite:true}); TraceLettres.trace(document.getElementById('jG'), a[2], {toutDeSuite:true}); }", [T, P2, G1])
        pg.wait_for_timeout(200); stat = img(pg); return vide, stat
    def arme(vitesse=None):
        """relance les trois blocs en pas à pas (ou en temps réel si une vitesse est donnée) ; rend les durées"""
        o = "{manuel:true, respecteReduire:false}" if vitesse is None else "{vitesse:%s, respecteReduire:false, cps:50}" % vitesse
        return pg.evaluate("async a=>{ for(const [id,s] of [['jT',a[0]],['jP',a[1]],['jG',a[2]]]){ JC[id]=TraceLettres.trace(document.getElementById(id), s, %s); await JC[id].pret; } return Object.keys(JC).map(k=>[k, JC[k].duree, JC[k].glyphes.length]); }" % o, [T, P2, G1])
    def va(f): pg.evaluate("f=>{ for(const k in JC) JC[k].va(f); }", f); pg.wait_for_timeout(45)

    # ── ① la dernière image est le texte statique ──
    for sombre in (False, True):
        vide, stat = pose(sombre); nom = 'sombre' if sombre else 'clair'
        encre = int((ecart(stat, vide) > 24).sum())
        arme(); va(1.0); pg.wait_for_timeout(80); d = ecart(img(pg), stat)
        reste = pg.evaluate("()=>[document.querySelectorAll('canvas[data-trace]').length, ['jT','jP','jG'].map(i=>getComputedStyle(document.getElementById(i)).clipPath).join('|')]")
        pg.evaluate("()=>{ for(const k in JC) JC[k].finir(); }"); pg.wait_for_timeout(80); d2 = ecart(img(pg), stat)
        juge('① %s — tracé pas à pas mené au bout : la dernière image est le texte statique, au pixel près' % nom, int((d > 0).sum()) == 0 and int((d2 > 0).sum()) == 0 and encre > 20000,
             'pixels différents : %d au dernier pas, %d après la fin ; %d pixels d\'encre' % (int((d > 0).sum()), int((d2 > 0).sum()), encre))
        juge('① %s — au dernier pas le canevas ne montre plus rien et la découpe est levée' % nom, reste[1].replace('none', '').replace('|', '') == '' and (SONDE or True), reste)
        if not sombre:
            arme(vitesse=6); pg.evaluate("()=>Promise.all(Object.keys(JC).map(k=>JC[k].fin))"); pg.wait_for_timeout(120); d3 = ecart(img(pg), stat)
            n_cv = pg.evaluate("()=>document.querySelectorAll('canvas[data-trace]').length")
            juge('① clair — tracé en temps réel : la dernière image est le texte statique, il ne reste aucun canevas', int((d3 > 0).sum()) == 0 and n_cv == 0, 'pixels différents : %d ; canevas restants : %d' % (int((d3 > 0).sum()), n_cv))

    # ── ② aucune opacité intermédiaire hors du front ; ⑥ jamais tout d'un coup (pas à pas) ──
    vide, stat = pose(False); plein = ecart(stat, vide) > 24; total = int(plein.sum())
    temoin = int(erode(intermediaire(stat, vide)).sum())
    durees = arme(); N = 40; comptes = []; pire_plage = 0; pire_lisere = 0; mi_trace = 0; vus = 0; ou = ''
    for i in range(N + 1):
        f = i / N; va(f); m = img(pg)
        rev = (ecart(m, vide) > 24); comptes.append(int(rev.sum()))
        if 0 < i < N:
            inter = intermediaire(m, vide); n_i = int(inter.sum()); n_p = int(erode(inter).sum())
            if n_p > pire_plage:
                ys, xs = np.nonzero(erode(inter)); ou = 'étape %d, autour de x %d–%d, y %d–%d (pixels de capture)' % (i, xs.min(), xs.max(), ys.min(), ys.max())
                if CAPT: Image.fromarray(m[max(0, ys.min() - 40):ys.max() + 40, max(0, xs.min() - 60):xs.max() + 60].astype(np.uint8)).resize((4 * (xs.max() - max(0, xs.min() - 60) + 60), 4 * (ys.max() - max(0, ys.min() - 40) + 40)), Image.NEAREST).save('scratchpad/v146/trace/juge-plage.png')
            pire_plage = max(pire_plage, n_p); pire_lisere = max(pire_lisere, n_i); vus += 1; mi_trace += 1 if 0 < comptes[-1] < total else 0
            if CAPT and i in (7, 19, 31): Image.fromarray(m.astype(np.uint8)).save('scratchpad/v146/trace/juge-etape-%02d.png' % i)
    juge('② aucune opacité intermédiaire hors du front : sur %d images en cours de tracé, les pixels de couverture partielle ne forment aucune plage' % vus, pire_plage == 0 and temoin == 0 and mi_trace >= vus - 2,
         'plus grande plage : %d pixels%s (témoin, le texte statique : %d) ; plus grand liséré : %d pixels (anticrénelage des contours et du front) ; images réellement à mi-tracé : %d' % (pire_plage, (' — ' + ou) if ou else '', temoin, pire_lisere, mi_trace))
    pas = [comptes[i + 1] - comptes[i] for i in range(N)]
    juge('⑥ pas à pas : le texte part de rien et ne recule jamais', comptes[0] == 0 and min(pas) >= -total * 0.002 and comptes[-1] >= total * 0.995, 'départ %d, fin %d sur %d pixels ; plus petite étape %+d' % (comptes[0], comptes[-1], total, min(pas)))
    juge('⑥ pas à pas : jamais tout d\'un coup — aucune des %d étapes n\'apporte plus de 15 %% du texte' % N, max(pas) <= 0.15 * total and sum(1 for x in pas if x > 0) >= 30,
         'plus grande étape : %.1f %% ; étapes qui apportent de l\'encre : %d sur %d' % (100.0 * max(pas) / max(total, 1), sum(1 for x in pas if x > 0), N))
    pg.evaluate("()=>{ for(const k in JC) JC[k].finir(); }")
    # ⑥ en temps réel : des captures pendant un tracé à ×0,25
    pose(False); arme(vitesse=0.25); serie = []
    for _ in range(14): serie.append(int((ecart(img(pg), vide) > 24).sum())); pg.wait_for_timeout(120)
    pg.evaluate("()=>{ for(const k in JC) JC[k].finir(); }")
    cr = [serie[i + 1] - serie[i] for i in range(len(serie) - 1)]
    juge('⑥ temps réel (×0,25) : l\'encre croît de capture en capture, sans à-coup', min(cr) >= 0 and len(set(serie)) >= 10 and max(cr) <= 0.2 * total, 'pixels dévoilés : %s' % serie)

    # ── les chemins : ③ R2, ⑤ R1 (l'alphabet de la page) ; ④ R3 (les six textes) ──
    PC = pg.evaluate("""a=>{ const o={}; for(const c of a){ o[c]={}; for(const v of ['h','b']){ const p=TraceLettres.parcours('Gilbert', c, v); if(p && p.variante===v) o[c][v]={dep:p.depart, arr:p.arrivee, traits:p.traits.map(t=>t.pts), rep:p.repassages, R:Math.max.apply(null,p.traits.map(t=>t.R))}; } } return o; }""", ALPHA)
    absents = [c for c in ALPHA if not PC.get(c) or not PC[c]]
    juge('les %d glyphes de l\'alphabet de la page ont un chemin' % len(ALPHA), not absents, 'sans chemin : %s' % ' '.join(absents))
    gauche = {}; ratios = []; oppose = 0; nvar = 0
    for c in ALPHA:
        bo = boite(c); larg = bo[2] - bo[0]
        for v, d in PC.get(c, {}).items():
            nvar += 1; xf = (d['arr'][0] - bo[0]) / max(larg, 1); etroit = larg <= 1.25 * 2 * d['R']
            if not etroit and xf < 0.40: gauche.setdefault(c, []).append('%s : %.2f' % (v, xf))
            tr = sum(lg(t) for t in d['traits']); rp = sum(lg(r) for r in d['rep']); ratios.append((rp / max(tr, 1), c, v))
            oppose += 1 if cote(d['dep'][1], bo) != cote(d['arr'][1], bo) else 0
            if cote(d['dep'][1], bo) != v: gauche.setdefault(c + ' (départ du mauvais côté)', []).append(v)
    neuves = [c for c in gauche if c not in IMPOSSIBLE_R2]
    juge('③ R2 — chaque glyphe finit à droite ; les seules exceptions sont celles que ce juge nomme (%s)' % ' '.join(sorted(IMPOSSIBLE_R2)), not neuves,
         'finissent à gauche : %s%s' % (' · '.join('%s (%s)' % (c, ', '.join(x)) for c, x in sorted(gauche.items())), (' — NON NOMMÉS : ' + ' '.join(neuves)) if neuves else ''))
    ratios.sort(reverse=True); med = sorted(r[0] for r in ratios)[len(ratios) // 2]
    juge('⑤ R1 — repassage : aucun tracé au-delà de %d %% de sa longueur, médiane ≤ %d %%' % (R1_MAX * 100, R1_MEDIANE * 100), ratios[0][0] <= R1_MAX and med <= R1_MEDIANE,
         'médiane %.0f %% sur %d tracés ; sans repassage : %d ; les pires : %s' % (med * 100, len(ratios), sum(1 for r in ratios if r[0] < 0.005), ' · '.join('%s/%s %.0f %%' % (c, v, r * 100) for r, c, v in ratios[:8])))
    # ④ R3 sur les six textes, le côté recalculé ici
    pose(False); G = pg.evaluate("""async P=>{ const out=[]; for(const s of P){ const el=document.getElementById('jP'); const c=TraceLettres.trace(el, s, {manuel:true, respecteReduire:false}); await c.pret; out.push(c.glyphes.map(g=>[g.car, g.variante])); c.stop(); } return out; }""", P)
    # ⚑ v154 — ④ AUCUNE ONDE : chaque lettre part de son tracé naturel (« h » quand le glyphe l'a), le départ recalculé ici depuis la géométrie
    trans = 0; faux = []; sans_chemin = []; bas = 0
    for texte in G:
        for car, v in texte:
            if v is None: sans_chemin.append(car); continue
            d = PC[car][v] if (car in PC and v in PC[car]) else pg.evaluate("a=>{ const p=TraceLettres.parcours('Gilbert', a[0], a[1]); return p?{dep:p.depart, arr:p.arrivee}:null; }", [car, v])
            if d is None: sans_chemin.append(car); continue
            trans += 1; a_h = car in PC and 'h' in PC[car]
            if a_h and v != 'h': faux.append('%s (variante %s)' % (car, v))
            if v != 'h': bas += 1
    juge('④ AUCUNE ONDE (v154) — dans les six textes, chaque lettre prend son tracé naturel (« h » quand elle l\'a), quelle que soit la précédente', not faux and not sans_chemin and trans > 250,
         '%d lettres ; %d sans variante « h » (elles n\'en ont pas d\'autre)%s%s' % (trans, bas, (' — FAUTES : ' + ' ; '.join(faux[:6])) if faux else '', (' — SANS CHEMIN : ' + ' '.join(sorted(set(sans_chemin)))) if sans_chemin else ''))
    # ⚑ v154 — ⑪ EN TEMPS DE PLUME, pas à pas à la milliseconde (indépendant de la charge), puis sur les pixels
    pose(False)
    PL = pg.evaluate("""async a=>{ const el=document.getElementById('jP'); const c=TraceLettres.trace(el, a, {manuel:true, respecteReduire:false}); await c.pret; const D=c.duree; const dep={}, fin={}; let max=0, t3=null;
        for(let t=0;t<=D+2;t+=1){ c.va(Math.min(1,t/D)); const e=c.etat(), A=e.actives||(e.glyphe<e.total?[e.glyphe]:[]); if(A.length>max) max=A.length; if(t3===null && A.length===3) t3=t; A.forEach(j=>{ if(!(j in dep)) dep[j]=t; fin[j]=t; }); }
        let pix=null; if(t3!==null){ const cv=document.querySelector('canvas[data-trace]'); if(cv){ const cx=cv.getContext('2d'); c.va(0); c.va((t3+4)/D); const n3=c.etat().actives.length; const A=cx.getImageData(0,0,cv.width,cv.height).data; c.va((t3+7)/D); const Bq=cx.getImageData(0,0,cv.width,cv.height).data;
          const col=new Array(cv.width).fill(0); for(let i=3;i<A.length;i+=4) if(Math.abs(A[i]-Bq[i])>8) col[((i-3)/4)%cv.width]++;
          let runs=0, gap=99; for(let x=0;x<cv.width;x++){ if(col[x]>0){ if(gap>3) runs++; gap=0; } else gap++; } pix={actives:n3, fronts:runs}; } }
        const txt=el.textContent; const gl=c.glyphes.map(g=>[g.car, g.x, g.y]); c.stop(); return {D, dep, fin, max, t3, pix, gl, esp:(txt.trim().match(/\\s+/g)||[]).length}; }""", P2)
    js = sorted(int(k) for k in PL['dep']); dep = [PL['dep'][str(j)] for j in js]; dur = [PL['fin'][str(j)] - PL['dep'][str(j)] + 1 for j in js]
    rate = (len(js) - 1 + 0.4 * PL['esp']) / max((dep[-1] - dep[0]) / 1000.0, 1e-3) if len(js) > 1 else 0
    juge('⑪ temps de plume — le débit des départs : %d à %d caractères par seconde (une espace compte 0,4)' % (CPS_MIN, CPS_MAX), CPS_MIN <= rate <= CPS_MAX and len(js) >= 15, '%.1f car/s (%d lettres, %d espaces)' % (rate, len(js), PL['esp']))
    juge('⑪ temps de plume — chaque lettre est en cours de %d à %d ms' % (DUREE_MIN, DUREE_MAX), dur and min(dur) >= DUREE_MIN and max(dur) <= DUREE_MAX, 'de %d à %d ms (médiane %d)' % (min(dur), max(dur), sorted(dur)[len(dur) // 2]) if dur else 'aucune')
    juge('⑪ temps de plume — au plus %d lettres en cours, et trois à la fois au fil du tracé' % ACTIVES_MAX, PL['max'] == ACTIVES_MAX, 'au plus %d en même temps' % PL['max'])
    juge('⑪ sur les pixels — quand le module dit trois lettres en cours, le canevas montre trois fronts qui avancent (trois zones qui changent, séparées)', bool(PL['pix']) and PL['pix']['actives'] == 3 and PL['pix']['fronts'] == 3, str(PL['pix']))
    gl = PL['gl']; desordre = [j for a, j in zip(js, js[1:]) if not (PL['dep'][str(j)] > PL['dep'][str(a)] and (abs(gl[j][2] - gl[a][2]) > 1 or gl[j][1] > gl[a][1]))]
    juge('⑪ temps de plume — les lettres partent strictement dans l\'ordre, de gauche à droite sur une ligne ; la suivante avant la fin de la précédente, jamais avant elle', not desordre and all(PL['dep'][str(j)] < PL['fin'][str(a)] for a, j in zip(js, js[1:]) if abs(gl[j][2] - gl[a][2]) <= 1),
         'hors d\'ordre : %s' % desordre[:6] if desordre else '%d départs dans l\'ordre' % len(js))
    un_seul = sorted(c for c in ALPHA if len(PC.get(c, {})) == 1)
    juge('④ R3 — les glyphes à un seul tracé sont ceux que ce juge nomme', all(c in UN_SEUL_TRACE for c in un_seul), 'un seul tracé : %s ; finissent du côté opposé au départ : %d tracés sur %d' % (' '.join(un_seul), oppose, nvar))

    # ── ⑨ v153 : la géométrie, image par image, o · s · g en Gilbert et en Atkinson ──
    pg.add_script_tag(url='http://127.0.0.1:%s/variantes/trace-chemins-atkinson.js' % PORT); pg.wait_for_timeout(300)
    if MODULE: pg.add_script_tag(url='http://127.0.0.1:%s/%s' % (PORT, MODULE)); pg.wait_for_timeout(300)
    if SONDE: pg.evaluate(SONDES[SONDE])
    pg.evaluate("()=>{ const s=document.getElementById('jScene'); if(s) s.remove(); }")
    GEOS = []
    for pol, gr, car in [('Gilbert', '700', 'o'), ('Gilbert', '700', 's'), ('Gilbert', '700', 'g'), ('Atkinson', '500', 'o'), ('Atkinson', '500', 's'), ('Atkinson', '500', 'g')]:
        r = pg.evaluate(GEO, [pol, gr, car, NGEO])
        if not r: juge('⑨ %s « %s » : le tracé se mesure (canevas de tracé présent)' % (pol, car), False, 'aucun canevas : le tracé n\'a pas eu lieu'); continue
        GEOS.append((pol, car, geo_analyse(r)))
    for pol, car, o in GEOS:
        juge('⑨ %s « %s » — préfixe continu du chemin : rien hors de la lettre, aucun trou derrière le front, rien d\'avance devant' % (pol, car),
             o['hors'] == 0 and o['trous'] <= 30 and o['avance'] <= 30 and o['pas'] >= NGEO // 2, 'pixels hors de la lettre %d ; trou derrière le front %d px ; avance %d px (au pire, sur %d images)' % (o['hors'], o['trous'], o['avance'], o['pas']))
        juge('⑨ %s « %s » — aucun éclat : pas d\'îlot d\'encre non tracée, petit et isolé, laissé en arrière (3 images et plus) pendant que la lettre avance' % (pol, car), o['ilots'] == 0, '%d pixel(s)·image(s) laissés en arrière trois images ou plus ; le plus long : %d images' % (o['ilots'], o['ilotMax']))
        juge('⑨ %s « %s » — aucune valeur d\'alpha intermédiaire hors du bord (un pixel partiel touche l\'encre non tracée)' % (pol, car), o['loin'] <= 3, 'pixels partiels loin du bord : %d au pire (partiels par image : %d au plus)' % (o['loin'], o['partiels']))
        A = o['angles']
        juge('⑨ %s « %s » — le front, à l\'intérieur d\'un trait, est perpendiculaire au chemin (± %d°)' % (pol, car, ANGLE_MAX), len(A) >= 5 and max(map(abs, A)) <= ANGLE_MAX,
             '%d mesures ; écart au perpendiculaire : médiane %.1f°, pire %.1f° (%d images dans un coude, non mesurées)' % (len(A), float(np.median(np.abs(A))) if A else -1, max(map(abs, A)) if A else -1, o.get('coudes', 0)))

    section_pl(b, err)

    # ── ⑦ ⑧ v153 : la vitesse et le « pof », DANS L'APP, en temps réel (banc comme Tom, le vrai onboarding) ──
    def onboarding_reel(q=''):
        ctx2 = B.contexte(b, onb=False, guide=False); pg2 = B.ouvre(ctx2, APP, attente=7000, q=q)
        if MODULE: pg2.add_script_tag(url='http://127.0.0.1:%s/%s' % (PORT, MODULE)); pg2.wait_for_timeout(200)
        pg2.evaluate(ENREG)
        B.tap_sel(pg2, '#onbPh'); pg2.wait_for_timeout(500); pg2.keyboard.type('Camille', delay=30); pg2.keyboard.press('Enter')
        for _ in range(60):
            pg2.wait_for_timeout(250)
            if pg2.evaluate("()=>window.__TL.filter(r=>r.fin).length>=3"): break
        L = pg2.evaluate("()=>window.__TL"); ctx2.close(); return L
    L = onboarding_reel()
    CALME = B.charge() < 4
    def debit(LL):
        n = 0; dt = 0.0
        for r in LL:
            st = {}
            for t, a in (r.get('images') or []):
                for j in a: st.setdefault(j, t)
            if len(st) > 1: ks = sorted(st); n += len(ks) - 1 + 0.4 * r['esp']; dt += st[ks[-1]] - st[ks[0]]
        return n / max(dt / 1000.0, 1e-3)
    cps = debit(L); ch = B.charge()
    juge('⑦ le débit À L\'ÉCRAN (le vrai onboarding : « Camille, donc. », « Quid… », « Petite ou grande… ») : %d à %d caractères par seconde%s' % (CPS_MIN, CPS_MAX, '' if CALME else ' — NON JUGÉ (charge ≥ 4)'), CALME is False or CPS_MIN <= cps <= CPS_MAX,
         '%.1f car/s ; charge %.1f' % (cps, ch))
    imgs = []
    for r in L:
        for j in range(r['n']):
            k = sum(1 for t, a in (r.get('images') or []) if j in a)
            if k: imgs.append(k)
    imgs.sort(); peu = sum(1 for x in imgs if x < IMAGES_MIN)
    juge('⑧ chaque lettre est en cours sur %d images au moins, à l\'écran%s' % (IMAGES_MIN, '' if CALME else ' — NON JUGÉ (charge ≥ 4)'), CALME is False or (len(imgs) >= 20 and peu == 0),
         '%d lettres ; images par lettre : min %d, médiane %d ; %d sous %d ; charge %.1f' % (len(imgs), imgs[0] if imgs else 0, imgs[len(imgs) // 2] if imgs else 0, peu, IMAGES_MIN, ch))
    L2 = onboarding_reel('?cps=12')
    cps2 = debit(L2)
    juge('⑦ le débit se règle : `?cps=12` → environ 12 caractères par seconde', 10.5 <= cps2 <= 13.5, '%.1f car/s' % cps2)
    if CAPT:
        ctx3 = B.contexte(b, onb=False, guide=False); pg3 = B.ouvre(ctx3, APP, attente=7000, q='?tlv=0.05')
        pg3.wait_for_function("()=>!document.querySelector('canvas[data-trace]') && !!document.getElementById('onbPh') && getComputedStyle(document.getElementById('onbPh')).visibility==='visible'", timeout=90000); pg3.wait_for_timeout(300)   # à ×0,05 la page du prénom se trace vingt fois plus lentement
        pg3.evaluate(ENREG); B.tap_sel(pg3, '#onbPh'); pg3.wait_for_timeout(500); pg3.keyboard.type('Camille', delay=30); pg3.keyboard.press('Enter')
        info = None
        for _ in range(600):
            pg3.wait_for_timeout(50)
            info = pg3.evaluate("()=>{ const r=window.__TL.find(x=>x.id==='onbDit'); if(!r) return null; const c=window.__CTL[r.k]; if(!c||c.fini) return null; const e=c.etat(); if((e.actives||[]).length<3) return null; return {a:e.actives, g:e.actives.map(j=>c.glyphes[j].car)}; }")
            if info: break
        e = pg3.evaluate("()=>{ const cv=document.querySelector('canvas[data-trace]'); const q=(cv||document.getElementById('onbDit')).getBoundingClientRect(); return [q.left, q.top, q.width, q.height]; }")
        pg3.screenshot(path='scratchpad/v154/trace-x005.png', clip={'x': e[0], 'y': e[1], 'width': e[2], 'height': e[3]}); ctx3.close()
        print('INFO  capture : scratchpad/v154/trace-x005.png (×0,05, « Camille, donc. », lettres en cours : %s)' % (info and ' · '.join(info['g'])))

    # ── le coût (information) : un tracé en temps réel à ×1, ce que le module mesure lui-même ──
    pose(False)
    cout = pg.evaluate("""async a=>{ TraceLettres.mesures.image.length=0; TraceLettres.mesures.prep.length=0; const t0=performance.now();
       const c=TraceLettres.trace(document.getElementById('jP'), a, {respecteReduire:false}); await c.fin; const q=(m,p)=>{ m=m.slice().sort((x,y)=>x-y); return m.length?m[Math.min(m.length-1,Math.floor(m.length*p))]:0; };
       const im=TraceLettres.mesures.image, pr=TraceLettres.mesures.prep; return {duree:Math.round(performance.now()-t0), prevue:Math.round(c.duree||0), lettres:(c.glyphes||[]).length, images:im.length, image_p50:q(im,.5), image_p95:q(im,.95), image_max:q(im,1), prep_n:pr.length, prep_p50:q(pr,.5), prep_max:q(pr,1)}; }""", P2)
    print('INFO  coût (WebKit, ce Mac, charge %.1f) : %s' % (B.charge(), json.dumps(cout, ensure_ascii=False)))
    if err: print('INFO  erreurs de page :', err[:3])
    b.close()
n_ok = sum(1 for _, c in res if c)
print('\n%d / %d%s' % (n_ok, len(res), '   (sonde « %s » : le juge doit rougir)' % SONDE if SONDE else ''))
sys.exit(0 if n_ok == len(res) else 1)
