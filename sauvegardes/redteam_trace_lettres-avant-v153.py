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

`--sonde=fondu` remplace le tracé par un fondu d'opacité, `--sonde=bloc` par une apparition d'un coup : le juge DOIT rougir (② ou ⑥).
Usage : python3 redteam_trace_lettres.py [--port=8752] [--sonde=fondu|bloc] [--captures]
"""
import sys, io, json, math, zipfile; sys.path.insert(0, '.')
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
PORT = arg('port', '8752'); SONDE = arg('sonde', ''); CAPT = '--captures' in sys.argv
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

with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); err = []
    pg.on('pageerror', lambda e: err.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%s/%s' % (PORT, PAGE)); pg.wait_for_timeout(1500)
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
    trans = 0; ok = 0; exc = {}; faux = []; sans_chemin = []
    for texte in G:
        prec = 'h'
        for car, v in texte:
            if v is None or car not in PC or v not in PC[car]:
                d = pg.evaluate("a=>{ const p=TraceLettres.parcours('Gilbert', a[0], a[1]||'h'); return p?{dep:p.depart, arr:p.arrivee}:null; }", [car, v])
                if d is None: sans_chemin.append(car); continue
            else: d = PC[car][v]
            bo = boite(car); dep = cote(d['dep'][1], bo); trans += 1
            if dep == prec: ok += 1
            else:
                a_lautre = pg.evaluate("a=>{ const g=TraceLettres.glyphe('Gilbert', a[0]); return !!(g && g[a[1]]); }", [car, prec])
                if a_lautre or car not in UN_SEUL_TRACE: faux.append('%s (attendu %s, parti %s)' % (car, prec, dep))
                else: exc[car] = exc.get(car, 0) + 1
            prec = cote(d['arr'][1], bo)
    juge('④ R3 — dans les six textes, chaque lettre commence du côté où la précédente a fini (hors glyphes à un seul tracé, nommés)', not faux and not sans_chemin and trans > 250,
         '%d lettres, %d dans la règle, %d exceptions : %s%s%s' % (trans, ok, sum(exc.values()), ' · '.join('%s ×%d (%s)' % (c, n, UN_SEUL_TRACE[c]) for c, n in sorted(exc.items(), key=lambda x: -x[1])),
                                                                   (' — FAUTES : ' + ' ; '.join(faux[:6])) if faux else '', (' — SANS CHEMIN : ' + ' '.join(sorted(set(sans_chemin)))) if sans_chemin else ''))
    un_seul = sorted(c for c in ALPHA if len(PC.get(c, {})) == 1)
    juge('④ R3 — les glyphes à un seul tracé sont ceux que ce juge nomme', all(c in UN_SEUL_TRACE for c in un_seul), 'un seul tracé : %s ; finissent du côté opposé au départ : %d tracés sur %d' % (' '.join(un_seul), oppose, nvar))

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
