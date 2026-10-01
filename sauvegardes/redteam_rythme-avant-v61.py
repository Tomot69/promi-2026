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
# ⚠ Pas un écart moyen sur toute la Toile : un départ en semis constant ne change qu'UNE dalle (son fondu), et une
# moyenne sur 390 × 844 le fait passer sous n'importe quel seuil — la durée mesurée devenait celle du seuil.
#
# LES VALEURS ATTENDUES SONT ÉCRITES EN DUR (§7 : un juge qui lit la valeur qu'il vérifie ne vérifie rien) — voir ATTENDU,
# et la grandeur jugée dépend du monde (durée ou nombre d'images, plus la cadence). Relevés : sauvegardes/rythme-v60/.
# Prouvé contre deux versions qui dérivent : app-derive-ressort.html (le ressort ralenti) et app-derive-latence.html
# (AUCUNE constante touchée : 28 ms de travail par image pendant 1,2 s après chaque plantation ou départ).
#
# Les constantes qui font ce rythme sont AUSSI vérifiées dans le source (durées de transition, fondu de couleur, ressorts).
#
# python3 redteam_rythme.py [--app=fichier] [--mondes=a,b] [--sans-reel]
# ⚠ Seul, jamais en parallèle d'une autre batterie (§7) : il mesure des images.
import sys, re, io
from playwright.sync_api import sync_playwright

APP = next((a.split('=')[1] for a in sys.argv if a.startswith('--app=')), 'app.html')
TOUS = 'encre,touffe,mosaique,braille,pixel,halin,esquille,madrure,ritournelle,bobinette,terrazzo,gravure,sillons'
MONDES = (next((a.split('=')[1] for a in sys.argv if a.startswith('--mondes=')), None) or TOUS).split(',')

# ⚑ LES DURÉES VALIDÉES — celebration-mondes.html, 26 sept. 2026 (ms). Ne se modifient que sur une décision de Tom.
# ⚑ DEUX FAMILLES, ET CE QUI EST FIXE N'EST PAS LA MÊME GRANDEUR (mesuré, 26 sept. 2026).
#  · TEMPS  — le mouvement suit l'horloge : Pochade et Touffe (ressort calé sur le temps, v56), et les mondes qui déclarent
#    `transDur`. On juge la DURÉE.
#  · IMAGES — le ressort avance de 0,17 PAR IMAGE : Tesselle, Braille, Buvard, Éclisse, Taille-douce, Houle. Leur durée
#    dépend de la vitesse de la machine (Taille-douce : 795 à 1 003 ms selon la passe, pour 34 à 40 images) ; ce qui est
#    fixe, c'est le NOMBRE D'IMAGES. On juge les images.
#  · TOUS   — la CADENCE (images par seconde) ne tombe pas sous 60 % de la cadence validée : c'est elle qui prend une passe
#    lourde en plein mouvement (Braille varie déjà de 40 à 55 i/s d'une passe à l'autre ; Houle tourne à ~30 i/s).
# Valeurs : médianes des passes sur celebration-mondes.html et sur l'app par le même appel moteur (la page EST l'app dans
# un cadre ; relevé : les deux concordent monde par monde) — Toile semée, Chromium, machine au repos.
# Départ de Madrure : une passe sur la page avait un accroc de 129 ms (3 188 ms), écartée.
ATTENDU = {
  # monde:        famille    ((arrivée ms, images), (départ ms, images))
  'encre':       ('temps',  ((796, 40), (334, 14))),
  'touffe':      ('temps',  ((795, 46), (250, 13))),
  'mosaique':    ('images', ((786, 48), (263, 16))),
  'braille':     ('images', ((783, 41), (313, 16))),
  'pixel':       ('images', ((842, 40), (299, 16))),
  'halin':       ('temps',  ((2407, 148), (2847, 167))),
  'esquille':    ('temps',  ((1400, 79), (1400, 77))),
  'madrure':     ('temps',  ((2369, 133), (2350, 136))),
  'ritournelle': ('temps',  ((1928, 113), (1943, 119))),
  'bobinette':   ('temps',  ((2090, 117), (2110, 101))),
  'terrazzo':    ('images', ((796, 48), (328, 20))),
  'gravure':     ('images', ((803, 40), (345, 17))),
  'sillons':     ('images', ((982, 34), (482, 17))),
}

# ⚑ LES CONSTANTES QUI FONT LE RYTHME — écrites en dur, lues dans le source.
CONSTANTES = [
  ('Ritournelle, transition 1 900 ms', r'Rrit\.transDur\s*=\s*1900\b'),
  ('Esquille, transition 1 400 ms',    r'Resq\.transDur\s*=\s*1400\b'),
  ('Bobinette, transition 2 400 ms',   r'Rbob\.transDur\s*=\s*2400\b'),
  ('Madrure, transition 2 400 ms',     r'Rmad\.transDur\s*=\s*2400\b'),
  ('Halin, transition 1 800 ms',       r'Rhal\.transDur\s*=\s*1800\b'),
  ('Halin, retrait 900 ms',            r'Rhal\.partDur\s*=\s*900\b'),
  ('ressort du moteur 0,17 / 0,22',    r'var _kW=0\.17, _kX=0\.22;'),
  ('ressort Pochade/Touffe 0,838 / 0,79', r'_kW=1-Math\.pow\(0\.838,_dtf\); _kX=1-Math\.pow\(0\.79,_dtf\);'),
  ('fondu de départ 760 ms',           r'var pO=ease\(\(now-s\.tOut\)/760\)'),
  ('fondu d\'arrivée 760 ms',          r'var p=ease\(\(now-s\.t0\)/760\)'),
]

ENREG = r"""()=>{ const W=window; W.__R=[]; W.__T0=null; W.__fin=false; const gen=W.__gen=(W.__gen||0)+1;
  if(!W.__envAdd){ W.__envAdd=1; const f=W.Toile.addPromi; W.Toile.addPromi=function(){ if(W.__T0==null) W.__T0=performance.now();
      let s=12345; W.Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; return f.apply(this,arguments); };
    const g=W.Toile.sync; W.Toile.sync=function(){ if(W.__arme==='sync'&&W.__T0==null) W.__T0=performance.now(); return g.apply(this,arguments); }; }
  const cv=W.document.getElementById('toileCv'), w=Math.round(cv.width/4), h=Math.round(cv.height/4);
  const c=W.document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d',{willReadFrequently:true});
  function img(){ x.drawImage(cv,0,0,w,h); return x.getImageData(0,0,w,h).data; }
  let prev=img(); const B=8, bw=Math.ceil(w/B), bh=Math.ceil(h/B);
  (function f(){ if(W.__fin||W.__gen!==gen) return; const cur=img(); const acc=new Float32Array(bw*bh);
    for(let y=0;y<h;y++) for(let xx=0;xx<w;xx++){ const i=(y*w+xx)*4; acc[((y/B)|0)*bw+((xx/B)|0)]+=Math.abs(cur[i]-prev[i])+Math.abs(cur[i+1]-prev[i+1])+Math.abs(cur[i+2]-prev[i+2]); }
    let m=0; for(const a of acc) if(a>m) m=a; W.__R.push([performance.now(), m/(B*B*3)]); prev=cur; W.requestAnimationFrame(f); })(); }"""
LIT = r"""()=>{ const W=window; W.__fin=true; const T0=W.__T0; if(T0==null) return null;
  const R=W.__R.filter(r=>r[0]>=T0).map(r=>[r[0]-T0,r[1]]); let fin=0; for(const r of R) if(r[1]>0.5) fin=r[0];
  const F=R.filter(r=>r[0]<=fin+1); return {duree:Math.round(fin), images:F.length}; }"""

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
        pg.mouse.up(); pg.wait_for_timeout(4200)
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

print('— les constantes du rythme, dans le source (%s)' % APP)
S = io.open(APP, encoding='utf-8').read()
for nom, motif in CONSTANTES:
    juge(nom, len(re.findall(motif, S)) == 1)

manque = [m for m in MONDES if m not in ATTENDU]
if manque: print('⚠ durées attendues non écrites pour', manque); sys.exit(2)

chemins = ['moteur'] + ([] if '--sans-reel' in sys.argv else ['reel'])
with sync_playwright() as p:
    b = p.chromium.launch()
    for chemin in chemins:
        print('— chemin :', chemin)
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/' + APP); pg.wait_for_timeout(9000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
        pg.wait_for_timeout(1500)
        for m in MONDES:
            r = mouvement(pg, m, chemin)
            for i, sens in enumerate(('arrivee', 'depart')):
                fam, ref = ATTENDU[m]; att, img = ref[i]; mes = r.get(sens); nom = '%s · %s · %s' % (m, chemin, sens)
                if not mes or not mes['duree']: juge(nom, False, 'rien mesuré'); continue
                d = mes['duree']; n = mes['images']
                cad = (n / d) / (img / att)            # cadence mesurée / cadence validée
                if fam == 'temps':
                    tol = max(100, att * 0.15); bon = abs(d - att) <= tol
                    quoi = '%d ms (attendu %d ± %d)' % (d, att, tol)
                else:
                    tol = max(3, img * 0.2); bon = abs(n - img) <= tol
                    quoi = '%d images (attendu %d ± %d)' % (n, img, tol)
                juge(nom, bon and cad >= 0.6, '%s · cadence %d %% · [%d ms, %d images]' % (quoi, round(cad * 100), d, n))
        pg.close()
    b.close()
print('\n%d / %d' % (ok, ok + ko))
sys.exit(1 if ko else 0)
