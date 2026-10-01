# redteam_rythme.py — LE RYTHME D'UN MONDE NE DÉRIVE PAS (v60, Tom, 26 sept. 2026)
#
# « Les mouvements dans l'app sont-ils identiques à ceux de celebration-mondes.html ? C'est là que je les ai validés.
#   Écris un contrôle qui le vérifie désormais — la durée d'une animation de monde, en dur, prouvée contre une version
#   où elle dérive. »
#
# Pour chacun des treize mondes, une parole ARRIVE puis PART, par deux chemins :
#   moteur : appel direct (Toile.addPromi / Toile.sync) — ce que joue celebration-mondes.html
#   reel   : le vrai chemin — la page +, le tracé au doigt (impression, closeAll, passes) ; la fiche, « Supprimer », « Oui »
# Pour chaque mouvement : sa DURÉE — la dernière image où UN BLOC de la Toile bouge encore (blocs de 32 px, écart moyen
# > 0,5 niveau ; au repos la Toile est immobile, 0 exactement) — et son NOMBRE D'IMAGES.
# ⚑ v61 — et ce changement est une VITESSE : ramené à 16,67 ms (× 16,67 / durée de l'image). Une image deux fois plus longue
# porte deux fois plus de changement : sans cela la queue d'un mouvement ralenti restait au-dessus du seuil plus longtemps,
# et la durée mesurée grandissait avec la charge alors que le mouvement, lui, ne bougeait pas. À 60 i/s : identique.
# ⚠ Pas un écart moyen sur toute la Toile : un départ en semis constant ne change qu'UNE dalle (son fondu), et une
# moyenne sur 390 × 844 le fait passer sous n'importe quel seuil — la durée mesurée devenait celle du seuil.
#
# LES VALEURS ATTENDUES SONT ÉCRITES EN DUR (§7 : un juge qui lit la valeur qu'il vérifie ne vérifie rien) — voir ATTENDU,
# et la grandeur jugée dépend du monde (durée ou nombre d'images, plus la cadence). Relevés : sauvegardes/rythme-v60/.
# Prouvé contre deux versions qui dérivent, rangées dans sauvegardes/rythme-v61/ (les recopier à la RACINE le temps de la
# preuve : elles lisent les polices en chemin relatif) : app-derive-ressort.html (le ressort ralenti) et app-derive-latence.html
# (AUCUNE constante touchée : 28 ms de travail par image pendant 1,2 s après chaque plantation ou départ).
#
# Les constantes qui font ce rythme sont AUSSI vérifiées dans le source (durées de transition, fondu de couleur, ressorts).
#
# python3 redteam_rythme.py [--app=fichier] [--mondes=a,b] [--sans-reel]
# ⚠ Seul, jamais en parallèle d'une autre batterie (§7) : il mesure des images.
import sys, re, io
from playwright.sync_api import sync_playwright
GPU = ['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']

APP = next((a.split('=')[1] for a in sys.argv if a.startswith('--app=')), 'app.html')
TOUS = 'encre,touffe,mosaique,braille,pixel,halin,esquille,madrure,ritournelle,bobinette,terrazzo,gravure,sillons,brouillamini,chamade,volubilis,guingois,chantourne,mascaret,ramage'
# ⚑ v72 (Tom, 27 sept. 2026) — LA SAISON 2 ENTRE DANS LE JUGE. Ses durées ne s'écrivent qu'après validation de Tom (§7 : un juge ne
#   lit pas la valeur qu'il vérifie). Tant qu'un monde n'a pas sa ligne dans ATTENDU, il est RELEVÉ (`--releve-saison2`), jamais jugé,
#   et la passe le dit. ⚠ Ramage et Volubilis construisent leur état d'arrivée hors de l'image (tranches, Worker) : le moment où le
#   mouvement COMMENCE dépend de la machine ; sa durée, elle, suit l'horloge (fondu 900 ms, glissement 1 200 ms).
SAISON2 = 'brouillamini,chamade,volubilis,guingois,chantourne,mascaret,ramage'.split(',')
RELEVE2 = '--releve-saison2' in sys.argv
MONDES = (next((a.split('=')[1] for a in sys.argv if a.startswith('--mondes=')), None) or (','.join(SAISON2) if RELEVE2 else TOUS)).split(',')

# ⚑ LES DURÉES VALIDÉES — celebration-mondes.html, 26 sept. 2026 (ms). Ne se modifient que sur une décision de Tom.
# ⚑ v61 — CE QUI EST FIXE, ET CE QU'ON JUGE (Tom, 26 sept. : « passe les six mondes à l'horloge, sauf Houle » ;
#   « la durée ne doit pas dépendre de la charge »).
#  · HORLOGE — tous les mondes sauf Houle : le mouvement suit le temps. On juge LA FIN DU MOUVEMENT DANS LE MOTEUR (l'image
#    où la Toile cesse de bouger, `Toile_state().running`), ± max(100 ms, 8 %). Pas la fin VISIBLE : sur les mondes neufs les
#    derniers centièmes changent à peine l'image, et le seuil tombe avant ou après d'une page à l'autre (Madrure : vue 1 807 à
#    2 433 ms, moteur 2 426 à 2 440 — mesuré en A/B sur v60 et v61, trois pages chacune).
#  · IMAGES  — HOULE seule, EXCEPTION ÉCRITE : elle reste par image (à l'horloge elle deviendrait plus rapide que ce que Tom a
#    validé : elle tourne à ~30 i/s sur la page). On juge le NOMBRE D'IMAGES, ± max(3, 20 %).
#  · TOUS    — la CADENCE ne tombe pas sous 60 % de la cadence validée : c'est elle qui prend une passe lourde en plein geste.
# Valeurs : médianes relevées le 26 sept. 2026 sur la version VALIDÉE (app v60 = ce que charge celebration-mondes.html),
# vrai GPU, Chromium, deux pages fraîches par monde, Toile semée (sauvegardes/rythme-v60/reference-v60-gpu.txt).
ATTENDU = {
  # monde:        famille     ((arrivée, images), (départ, images))   — ms : fin du mouvement (horloge) ; images (Houle)
  'encre':       ('horloge', ((872, 33), (851, 32))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'touffe':      ('horloge', ((812, 48), (791, 48))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'mosaique':    ('horloge', ((792, 47), (780, 47))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'braille':     ('horloge', ((865, 44), (786, 40))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'pixel':       ('horloge', ((817, 46), (784, 44))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'halin':       ('horloge', ((2483, 147), (2995, 170))),   # 4 pages · ⚑ v61 : 2 378 / 2 848 (les accrocs comptent leur temps vrai)
  'esquille':    ('horloge', ((1437, 82), (1426, 73))),
  'madrure':     ('horloge', ((2432, 132), (2431, 133))),
  'ritournelle': ('horloge', ((1945, 113), (2040, 116))),   # 4 pages (une passe à 2 pages avait pris 2 322)
  'bobinette':   ('horloge', ((2462, 57), (2463, 70))),
  'terrazzo':    ('horloge', ((799, 45), (820, 46))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'gravure':     ('horloge', ((793, 48), (797, 45))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  'sillons':     ('images', ((1313, 36), (950, 29))),   # ⚑ v76 : le REPLI (Tom, 27 sept. : départs 780–870 ms validés)
  # ⚑ v73 (Tom, 27 sept. 2026 : « valide-les toutes, telles que relevées ») — la saison 2, relevée en v72 (deux pages, moteur et
  #   vrai chemin, vrai GPU) : moyenne des quatre relevés ; Ramage au milieu de sa plage (sa préparation dépend de la machine).
  'brouillamini':('horloge', ((1742, 70), (2046, 92))),
  'chamade':     ('horloge', ((1668, 44), (1946, 44))),
  'volubilis':   ('horloge', ((2711, 132), (2045, 92))),
  'guingois':    ('horloge', ((1722, 30), (1865, 31))),
  'chantourne':  ('horloge', ((1677, 16), (1849, 36))),
  'mascaret':    ('horloge', ((1674, 20), (1834, 32))),
  'ramage':      ('horloge', ((1690, 83), (2620, 149))),   # ⚑ v82 (Tom, 28 sept.) : l'arrivée sans fondu — le plumage se construit (1 681–1 702 ms)   # v73 : relevé APRÈS le plancher des tranches (100 tracés) — 2 213–2 950 · 2 282–2 957
}
# ⚑ v64 (Tom, 27 sept. 2026) — « Halin : élargis sa tolérance plutôt que de le laisser rougir au hasard — un contrôle qui oscille ne
#   protège rien. » Son départ varie avec le semis (tiré au hasard à chaque page) : mesuré 2 655 à 3 124 ms, sur v61 comme sur v63.
#   ± 15 % (au lieu de 8 %) couvre cette variation ; la preuve qu'il prend encore une vraie dérive est dans l'état des lieux (v64).
TOLERANCE = {('halin', 'depart'): 0.15,
  # ⚑ v73 (Tom) — « une tolérance large pour Ramage et Volubilis, dont la marge vient de la préparation » : le plumage d'arrivée se
  #   peint par tranches, le jardin d'arrivée se construit dans un Worker — le mouvement COMMENCE quand ils sont prêts. Relevé :
  #   Ramage 2 213–2 950 (arrivée) · 2 282–2 957 (départ), après le plancher des tranches de v73 ; Volubilis 2 608–2 832 · 1 963–2 161.
  # ⚑ v74 (Tom) — « un contrôle qui rougira au prochain semis ne protège rien » : le départ de Guingois est sorti à 2 012 ms
  #   (relevés 1 783 à 2 012) pour 1 865 ± 149 — à 2 ms de sa limite. ± 15 %.
  ('guingois', 'depart'): 0.15,
  # ⚑ v74 (Tom) — « un contrôle qui rougit une fois sur trois ne protège rien » : l'arrivée de Ramage par le vrai chemin est sortie à
  #   3 384 ms en série (2 850 et 2 912 seul). ± 33 % : la borne couvre 3 400 ms (2 580 + 851 = 3 431).
  ('ramage', 'arrivee'): 0.33, ('ramage', 'depart'): 0.33, ('volubilis', 'arrivee'): 0.15, ('volubilis', 'depart'): 0.15}
# la fin VISIBLE et les images validées — pour la cadence
VUE_REF = {'brouillamini': (1729, 2046), 'chamade': (1276, 1276), 'volubilis': (2697, 2037), 'guingois': (1701, 1712), 'chantourne': (1065, 1849), 'mascaret': (1047, 1618), 'ramage': (1690, 2620), 'encre': (869, 850), 'touffe': (808, 791), 'mosaique': (789, 780), 'braille': (858, 786), 'pixel': (813, 784), 'halin': (2466, 2992), 'esquille': (1374, 1216), 'madrure': (2252, 2279), 'ritournelle': (1928, 2034), 'bobinette': (2156, 2124), 'terrazzo': (796, 820), 'gravure': (791, 797), 'sillons': (1311, 950)}
IMG_REF = {'brouillamini': (70, 92), 'chamade': (44, 44), 'volubilis': (132, 92), 'guingois': (30, 31), 'chantourne': (16, 36), 'mascaret': (20, 32), 'ramage': (83, 149), 'encre': (33, 32), 'touffe': (48, 48), 'mosaique': (47, 47), 'braille': (44, 40), 'pixel': (46, 44), 'halin': (144, 170), 'esquille': (82, 73), 'madrure': (132, 133), 'ritournelle': (110, 116), 'bobinette': (57, 70), 'terrazzo': (45, 46), 'gravure': (48, 45), 'sillons': (36, 29)}

# ⚑ LES CONSTANTES QUI FONT LE RYTHME — écrites en dur, lues dans le source.
CONSTANTES = [
  ('Ritournelle, transition 1 900 ms', r'Rrit\.transDur\s*=\s*1900\b'),
  ('Esquille, transition 1 400 ms',    r'Resq\.transDur\s*=\s*1400\b'),
  ('Bobinette, transition 2 400 ms',   r'Rbob\.transDur\s*=\s*2400\b'),
  ('Madrure, transition 2 400 ms',     r'Rmad\.transDur\s*=\s*2400\b'),
  ('Halin, transition 1 800 ms',       r'Rhal\.transDur\s*=\s*1800\b'),
  ('Halin, retrait 900 ms',            r'Rhal\.partDur\s*=\s*900\b'),
  ('ressort du moteur 0,17 / 0,22',    r'var _kW=0\.17, _kX=0\.22, _redem=frame\._redem;'),
  ('v61 · cinq mondes à l\'horloge, 0,83 / 0,78 (= 0,17 / 0,22 à 60 i/s)',
   r"else if\(theme==='mosaique'\|\|theme==='braille'\|\|theme==='pixel'\|\|theme==='terrazzo'\|\|theme==='gravure'\)\{ if\(_redem\) _dtf=1; _kW=1-Math\.pow\(0\.83,_dtf\); _kX=1-Math\.pow\(0\.78,_dtf\); \}"),
  ('v61 · un redémarrage de boucle fait UN pas',  r'function kick\(\)\{if\(!running\)\{running=true;frame\._redem=1;'),
  ('v61 · mondes neufs : temps vrai en sous-pas de 1/60 s', r'if\(frame\._redem\|\|_rdt>0\.25\)_rdt=1/60; \}'),
  ('ressort Pochade/Touffe 0,838 / 0,79', r'_kW=1-Math\.pow\(0\.838,_dtf\); _kX=1-Math\.pow\(0\.79,_dtf\);'),
  # ⚑ v76 (Tom, 27 sept.) — « le fondu de départ ne mesure plus rien » : dans tous les mondes à semis constant, une dalle qui part se
  #   REPLIE (700 ms, les voisines la recouvrent) ; l'extinction vers le gris n'est plus le départ. Contrôle retiré (sauvegardes/redteam_rythme-avant-v76.py).
  ('fondu d\'arrivée 760 ms',          r'var p=ease\(\(now-s\.t0\)/760\)'),
  # ⚑ v72 — la saison 2 : ses constantes de transition, lues dans le source (celles du portage, v62–v68)
  ('Brouillamini, transition 1 600 ms · retrait 900 ms', r'Rbro\.transDur = 1600; Rbro\.douce = true; Rbro\.partDur = 900;'),
  ('Chamade, transition 1 600 ms · retrait 900 ms',      r'Rcha\.transDur = 1600; Rcha\.douce = true; Rcha\.partDur = 900;'),
  ('Volubilis, transition 1 600 ms · retrait 900 ms',    r'Rvol\.transDur = 1600; Rvol\.douce = true; Rvol\.partDur = 900;'),
  ('Guingois, transition 1 600 ms · retrait 900 ms',     r'Rgui\.transDur = 1600; Rgui\.douce = true; Rgui\.partDur = 900;'),
  ('Chantourné, transition 1 600 ms · retrait 900 ms',   r'Rchi\.transDur = 1600; Rchi\.douce = true; Rchi\.partDur = 900;'),
  ('Mascaret, transition 1 600 ms · retrait 900 ms',     r'Rmas\.transDur = 1600; Rmas\.douce = true; Rmas\.partDur = 900;'),
  ('Ramage, transition 1 600 ms · retrait 900 ms',       r'Rram\.transDur = 1600; Rram\.douce = true; Rram\.partDur = 900;'),
  ('v72 · Ramage : le fondu du plumage d\'arrivée = ARR 900 ms', r'var g, W, H, seeds, cOf, avg, L3 = 300;\n  function _sync\(\) \{[^\n]*\}\n  var UPL = 53\.55, ARR = 900, RET = 760;'),
]

ENREG = r"""()=>{ const W=window; W.__R=[]; W.__T0=null; W.__fin=false; const gen=W.__gen=(W.__gen||0)+1;
  if(!W.__envAdd){ W.__envAdd=1; const f=W.Toile.addPromi; W.Toile.addPromi=function(){ if(W.__T0==null) W.__T0=performance.now();
      let s=12345; W.Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; return f.apply(this,arguments); };
    const g=W.Toile.sync; W.Toile.sync=function(){ if(W.__arme==='sync'&&W.__T0==null) W.__T0=performance.now(); return g.apply(this,arguments); }; }
  const cv=W.document.getElementById('toileCv'), w=Math.round(cv.width/4), h=Math.round(cv.height/4);
  const c=W.document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d',{willReadFrequently:true});
  function img(){ x.drawImage(cv,0,0,w,h); return x.getImageData(0,0,w,h).data; }
  W.__tp=0; W.__bout=null; let prev=img(); const B=8, bw=Math.ceil(w/B), bh=Math.ceil(h/B);
  (function f(){ if(W.__fin||W.__gen!==gen) return; const cur=img(); const acc=new Float32Array(bw*bh);
    for(let y=0;y<h;y++) for(let xx=0;xx<w;xx++){ const i=(y*w+xx)*4; acc[((y/B)|0)*bw+((xx/B)|0)]+=Math.abs(cur[i]-prev[i])+Math.abs(cur[i+1]-prev[i+1])+Math.abs(cur[i+2]-prev[i+2]); }
    let m=0; for(const a of acc) if(a>m) m=a; const tn=performance.now(), dt=W.__tp?tn-W.__tp:16.667; W.__tp=tn; W.__R.push([tn, m/(B*B*3)*16.667/Math.max(8,dt)]); prev=cur; if(W.__T0!=null && W.__bout==null && tn-W.__T0>50 && W.Toile_state && !W.Toile_state().running) W.__bout=tn-W.__T0; W.requestAnimationFrame(f); })(); }"""
LIT = r"""()=>{ const W=window; W.__fin=true; const T0=W.__T0; if(T0==null) return null;
  const R=W.__R.filter(r=>r[0]>=T0).map(r=>[r[0]-T0,r[1]]); let fin=0; for(const r of R) if(r[1]>0.5) fin=r[0];
  const F=R.filter(r=>r[0]<=fin+1); return {duree:Math.round(fin), images:F.length, boucle:W.__bout==null?null:Math.round(W.__bout)}; }"""

def centre(pg, sel):
    return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}", sel)

def mouvement(pg, monde, chemin):
    # le semis d'un monde neuf est retiré au changement de famille (Math.random) : on le sème, pour mesurer le même
    # mouvement sur la même Toile — sans quoi Esquille varie de 1 063 à 1 479 ms d'une page à l'autre (le contenu, pas le rythme)
    pg.evaluate("m=>{ let s=777; Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; Toile.setTheme(m); }", monde); pg.wait_for_timeout(3000)
    out = {}
    pg.evaluate(ENREG); pg.evaluate("()=>{ window.__arme='add'; }")
    if chemin == 'reel':
        pg.mouse.click(*centre(pg, '#createBtn')); pg.wait_for_timeout(600)
        pg.mouse.click(*centre(pg, '#accChoix .acc-pil[data-k=promi]')); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ const t=document.getElementById('fTitle'); t.value='mesure du rythme'; t.dispatchEvent(new Event('input',{bubbles:true})); }")
        pg.evaluate(ENREG)
        z = pg.evaluate("()=>{ const r=document.getElementById('planterZone').getBoundingClientRect(); return [r.left, r.top+r.height/2, r.width]; }")
        pg.mouse.move(z[0]+12, z[1]); pg.mouse.down()
        for i in range(1, 26): pg.mouse.move(z[0]+12+(z[2]-24)*i/25, z[1]); pg.wait_for_timeout(12)
        pg.mouse.up(); pg.wait_for_timeout(1500)
        # v73 — on attend que le moteur S'ARRÊTE (8 s au plus) : Ramage prépare son plumage d'arrivée avant son fondu, et un délai
        # fixe de 4,2 s lisait « rien » quand la préparation traînait. Le juge lit la fin du mouvement ; il faut la laisser venir.
        for _ in range(65):
            if not pg.evaluate("()=>Toile_state().running"): break
            pg.wait_for_timeout(100)
        pg.wait_for_timeout(300)
    else:
        pg.evaluate("()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }")
        pg.wait_for_timeout(3500)
    out['arrivee'] = pg.evaluate(LIT); pg.wait_for_timeout(1500)
    pg.evaluate(ENREG); pg.evaluate("()=>{ window.__arme='sync'; }")
    if chemin == 'reel':
        pg.evaluate("()=>{ const p=promises.find(p=>p.title==='mesure du rythme'); openDetail(p.id); }"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ window._v16SupprimerPromi(cur); }"); pg.wait_for_timeout(700)
        pg.evaluate(ENREG); pg.evaluate("()=>{ window.__arme='sync'; }")
        pg.mouse.click(*centre(pg, '#v16Conf .v16-oui'))
    else:
        pg.evaluate("()=>{ const P=window.eval('promises'); const i=P.findIndex(p=>p.title==='mesure du rythme'); if(i>=0) P.splice(i,1); Toile.sync(P.filter(p=>!p.draft).map(p=>p.id)); }")
    pg.wait_for_timeout(3500)
    out['depart'] = pg.evaluate(LIT); pg.evaluate("()=>{ window.__arme=null; }"); pg.wait_for_timeout(1200)
    if chemin == 'reel': pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(600)
    return out

ok = ko = 0
def juge(nom, cond, detail=''):
    global ok, ko
    if cond: ok += 1; print('  ✓', nom, detail)
    else: ko += 1; print('  ✗', nom, detail)

BR = next((float(a.split('=')[1]) for a in sys.argv if a.startswith('--bride=')), 1)
print('— les constantes du rythme, dans le source (%s)' % APP)
S = io.open(APP, encoding='utf-8').read()
for nom, motif in CONSTANTES:
    juge(nom, len(re.findall(motif, S)) == 1)
# ⚑ v61 — EXCEPTION ÉCRITE : Houle (sillons) reste PAR IMAGE (Tom : « l'horloge la rendrait plus rapide que ce que j'ai validé »)
_l = next((l for l in S.split('\n') if 'var _kW=0.17, _kX=0.22' in l), '')
juge("v61 · Houle reste par image (exception)", "theme==='sillons'" not in _l.split('/*')[0])

manque = [m for m in MONDES if m not in ATTENDU and m not in SAISON2]
if manque: print('⚠ durées attendues non écrites pour', manque); sys.exit(2)
attente = [m for m in MONDES if m in SAISON2 and m not in ATTENDU]
if attente: print('⚠ EN ATTENTE DE VALIDATION (Tom) — relevés, jamais jugés :', ', '.join(attente))

chemins = ['moteur'] + ([] if '--sans-reel' in sys.argv else ['reel'])
with sync_playwright() as p:
    b = p.chromium.launch(args=GPU)   # le vrai GPU, comme le Chrome de Tom : sans lui Madrure prend son chemin de SECOURS (processeur)
    for chemin in chemins:
        print('— chemin :', chemin)
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/' + APP); pg.wait_for_timeout(9000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
        pg.wait_for_timeout(1500)
        if BR != 1: pg.context.new_cdp_session(pg).send('Emulation.setCPUThrottlingRate', {'rate': BR}); print('   processeur bridé ×%g' % BR)
        for m in MONDES:
            r = mouvement(pg, m, chemin)
            if m not in ATTENDU:   # la saison 2, avant validation : relevé seulement
                for sens in ('arrivee', 'depart'):
                    mes = r.get(sens) or {}
                    print('  · RELEVÉ %s · %s · %s — fin du mouvement (moteur) %s ms · vu %s ms · %s images' % (m, chemin, sens, mes.get('boucle'), mes.get('duree'), mes.get('images')))
                continue
            for i, sens in enumerate(('arrivee', 'depart')):
                fam, ref = ATTENDU[m]; att, img = ref[i]; mes = r.get(sens); nom = '%s · %s · %s' % (m, chemin, sens)
                if not mes or not mes['duree']: juge(nom, False, 'rien mesuré'); continue
                d = mes['duree']; n = mes['images']; bo = mes.get('boucle')
                cad = (n / d) / (IMG_REF[m][i] / VUE_REF[m][i])     # cadence mesurée / cadence validée (sur la fin visible)
                if fam == 'horloge':
                    tl = max(100, att * TOLERANCE.get((m, sens), 0.08))
                    bon = bo is not None and abs(bo - att) <= tl
                    quoi = 'fin du mouvement %s ms (attendu %d ± %d)' % (bo, att, tl)
                else:
                    tol = max(3, img * 0.2); bon = abs(n - img) <= tol
                    quoi = '%d images (attendu %d ± %d)' % (n, img, tol)
                if BR != 1:   # sous bridage VOULU la cadence tombe par construction : on ne juge que la DURÉE (horloge) ;
                              # Houle, exception par image, s'étire sous charge par décision — rapportée, pas jugée
                    if fam == 'horloge': juge(nom + ' (×%g)' % BR, bon, '%s · [vu %d ms, %d images]' % (quoi, d, n))
                    else: print('  · %s (×%g) — exception par image, non jugée : %d images, vu %d ms' % (nom, BR, n, d))
                    continue
                juge(nom, bon and cad >= 0.6, '%s · cadence %d %% · [vu %d ms, %d images]' % (quoi, round(cad * 100), d, n))
        pg.close()
    b.close()
print('\n%d / %d' % (ok, ok + ko))
sys.exit(1 if ko else 0)
