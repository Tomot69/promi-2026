#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_decoupe.py — UNE DALLE N'EST JAMAIS UNE IMAGE DÉCOUPÉE (décision Tom, 22 sept. 2026).

« Une dalle est peinte par le moteur, dans sa cellule, avec son propre contour, à sa taille
  finale. Jamais une image rognée, jamais un canevas recadré, jamais un morceau de Toile. »

Le contrôle ne lit pas le code : il PIÈGE LE CANEVAS À L'EXÉCUTION, écran par écran, deux thèmes.
Avant que l'app ne charge, on enveloppe `drawImage`, `getImageData`, `putImageData`,
`createPattern` et `toDataURL`, et l'on marque ce qui porte une dalle :

  · un canevas rendu par `Toile.dalleTrame`                       → DALLE
  · `#toileCv`, et tout canevas rendu par `Toile.renderTo`,
    `Toile.preview`, `Toile.repaint`, `Toile.repaintWorld`         → TOILE
  · tout canevas sur lequel on a posé l'un des deux                → PORTE (la marque se propage)

Hors du moteur (`app.html` entre `MOTEUR_DEBUT` et `MOTEUR_FIN`, le bloc de la Toile qu'on ne
touche pas, §9), chaque appel est jugé :

  A · DÉCOUPE        drawImage à NEUF arguments dont la source porte une dalle
  B · REDIMENSION    drawImage dont la taille RENDUE (cotes × transformation du contexte)
                     diffère de la source de plus d'un pixel
  C · PIXELS         getImageData / putImageData sur un canevas qui porte une dalle, ou un
                     ImageData qui en vient reposé ailleurs
  D · FRAGMENT       un canevas TOILE découpé ou redimensionné sur un autre canevas
  E · MOTIF / IMAGE  createPattern ou toDataURL d'un canevas qui porte une dalle (l'image
                     repart dans le DOM, où plus rien ne la surveille)
  F · PHOTO          drawImage d'une IMAGE de dalle déposée au projet (`PROMI_DALLES`, un webp
                     par monde) — « jamais une photo » (§4, règle 1)
  H · MONDE          une dalle peinte dans un autre monde que celui de SA plantation, sans le déclarer
                     (`opts.courant` : la page +, qui montre la dalle qu'on va planter ; les aperçus du Studio) — v30
  G · AFFICHAGE      un canevas qui porte une dalle, AFFICHÉ par le CSS à une autre taille que celle où il
                     a été peint (boîte × densité ≠ largeur du canevas, à 3 % près) — le navigateur le
                     redimensionne, c'est la même faute par un autre chemin (v29, 23 sept.)

Chaque prise est NOMMÉE par la ligne d'`app.html` qui l'a faite (pile d'appels), et par l'écran.

⚑ CE QUE LE MOTEUR FAIT CHEZ LUI EST RELEVÉ, PAS JUGÉ. `Toile.dalleTrame` découpe sa propre
  cellule (attribution pondérée pixel par pixel : getImageData/putImageData) puis se RECADRE au
  plus juste sur l'alpha (un drawImage à neuf arguments, 1 : 1). C'est le moteur qui trace son
  contour — le §9 interdit d'y toucher. Le compte est imprimé à part (« moteur »), jamais caché.

Preuve (§7) : `APP_DECOUPE=http://127.0.0.1:8752/sauvegardes/sonde-decoupe.html` — une copie de
l'app portant quatre défauts posés exprès (un par famille A-D). Le contrôle doit les PRENDRE,
chacun à sa ligne.

⚑ LA DETTE — CE QUE LE CONTRÔLE A TROUVÉ À SA NAISSANCE. Le premier passage (22 sept. 2026) a pris
  l'app en faute sur les quatre familles, à 23 lignes. Les corriger demande de toucher au moteur
  (CONTRAT-MONDE.md §10) : c'est un chantier, pas ce lot. Ces lignes sont FIGÉES dans
  `decoupe-dette.json`, reconnues par le TEXTE de leur ligne (jamais par son numéro), et imprimées
  à CHAQUE passage — le verdict reste « ❌ DETTE » tant qu'il en reste une. Le contrôle échoue
  (sortie 1) sur toute prise NOUVELLE : c'est ce qui garde les lots qui touchent une dalle.
  Une ligne de dette modifiée par un lot change d'empreinte : elle ressort NOUVELLE, et c'est voulu.

Usage :  python3 redteam_decoupe.py               (juge : sort 1 sur toute prise nouvelle)
         python3 redteam_decoupe.py --releve      (imprime tout, ne juge pas)
         python3 redteam_decoupe.py --figer-dette (réécrit la dette — seulement quand une ligne est CORRIGÉE)
"""
import os, sys, json, re
from collections import defaultdict
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_DECOUPE', "http://127.0.0.1:8752/app.html")
RELEVE = '--releve' in sys.argv
FIGER = '--figer-dette' in sys.argv
# ⚑ v32 — `--monde=esquille` : tous les Promi PLANTÉS dans ce monde (les quatre mondes neufs n'ont aucun Promi planté
#   chez eux dans le jeu de démonstration : sans cette option, le juge ne les peint jamais).
MONDE_OPT = next((a.split('=',1)[1] for a in sys.argv if a.startswith('--monde=')), None)
DETTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decoupe-dette.json')
# Le bloc du moteur de la Toile : `<script>` de la ligne 7745 au `})();` de la ligne 8604 (22 sept. 2026).
# ⚠ Il est RELU dans le fichier servi à chaque passe (repère : `var host=document.getElementById('toileCv')`
#   et le premier `})();` qui suit) — une ligne ajoutée plus haut ne le décale pas en silence.

PIEGE = r"""
(()=>{
  Error.stackTraceLimit = 40;
  const J = window.__decoupe = {log:[], moteur:{}, on:true, ecran:'chargement', lo:(window.__decoupeBornes||[0,0])[0], hi:(window.__decoupeBornes||[0,0])[1]};
  const P = CanvasRenderingContext2D.prototype;
  const ligne = () => {                       // première ligne d'app.html dans la pile, hors de ce piège
    const st = (new Error()).stack.split('\n');
    for (const f of st) { const mm = f.match(/promi-moteur[^\/:]*\.js:(\d+):\d+/); if (mm) return 1000000 + (+mm[1]);   // assainissement : le moteur vit dans promi-moteur.js
      const m = f.match(/app[^\/:]*\.html:(\d+):\d+/) || f.match(/sonde-[a-z]+\.html:(\d+):\d+/);
      if (m) return +m[1]; }
    return 0;
  };
  const dansMoteur = l => J.lo && l >= J.lo && l <= J.hi;
  const marque = c => { if (!c) return null; if (c.id === 'toileCv') return 'TOILE';
    return (c.__dalle || c.__enCours) ? 'DALLE' : c.__toile ? 'TOILE' : c.__porte ? 'PORTE' : null; };
  const note = (k, l, d) => { if (!J.on) return;
    if (dansMoteur(l)) { J.moteur[k] = (J.moteur[k]||0) + 1; return; }
    J.log.push(Object.assign({k:k, l:l, e:J.ecran}, d)); };
  const echelle = ctx => { try { const t = ctx.getTransform(); return [Math.hypot(t.a,t.b), Math.hypot(t.c,t.d)]; } catch(_) { return [1,1]; } };

  // F · une PHOTO de dalle : une image `<img>` tirée des dalles « déposées au projet » (PROMI_DALLES)
  let _photos = null;
  // ⚠ `PROMI_DALLES` vit dans une IIFE (≈ l. 9318) : `window.PROMI_DALLES` n'existe pas. On lit donc
  //   l'objet dans le TEXTE du script qui le déclare — jamais par son nom global.
  const photos = () => { if (_photos) return _photos; _photos = new Set();
    for (const s of document.scripts) { const t = s.textContent, i = t.indexOf('var PROMI_DALLES=');
      if (i < 0) continue; const j = t.indexOf('};', i);
      try { Object.values(JSON.parse(t.slice(i + 17, j + 1))).forEach(v => _photos.add(v)); } catch(_) {} }
    window.__decoupePhotos = _photos.size; return _photos; };
  const photo = im => { try { return (im instanceof HTMLImageElement) && photos().has(im.src); } catch(_) { return false; } };
  const dI = P.drawImage;
  P.drawImage = function(src){
    if (photo(src)) { const n = arguments.length, [ex, ey] = echelle(this);
      const dw = n >= 9 ? arguments[7] : n >= 5 ? arguments[3] : src.naturalWidth, dh = n >= 9 ? arguments[8] : n >= 5 ? arguments[4] : src.naturalHeight;
      note('F·photo', ligne(), {m:'PHOTO', n:n, src:[src.naturalWidth, src.naturalHeight], rendu:[+(dw*ex).toFixed(1), +(dh*ey).toFixed(1)],
        cible:String((this.canvas && (this.canvas.id || this.canvas.className)) || '?').slice(0,40)});
      if (this.canvas) this.canvas.__porte = 1; }
    const n = arguments.length, m = (src instanceof HTMLCanvasElement) ? marque(src) : null;
    if (m && this.canvas !== src) {
      const l = ligne(), sw = src.width, sh = src.height;
      let cw, ch, dw, dh;
      if (n >= 9) { cw = arguments[3]; ch = arguments[4]; dw = arguments[7]; dh = arguments[8]; }
      else if (n >= 5) { cw = sw; ch = sh; dw = arguments[3]; dh = arguments[4]; }
      else { cw = sw; ch = sh; dw = sw; dh = sh; }
      const [ex, ey] = echelle(this), rw = dw*ex, rh = dh*ey;
      const cible = (this.canvas && (this.canvas.id || this.canvas.className)) || '?';
      const d = {m:m, n:n, src:[sw,sh], coupe:[+(+cw).toFixed(1), +(+ch).toFixed(1)], rendu:[+rw.toFixed(1), +rh.toFixed(1)], cible:String(cible).slice(0,40)};
      const entiere = Math.abs(cw - sw) < 0.5 && Math.abs(ch - sh) < 0.5;
      const memeTaille = Math.abs(rw - cw) <= 1 && Math.abs(rh - ch) <= 1;
      if (m === 'TOILE' && (n >= 9 && !entiere || !memeTaille)) note('D·fragment', l, d);
      else if (n >= 9) note('A·découpe', l, d);
      else if (!memeTaille) note('B·redimension', l, d);
      else note('ok·pose', l, d);
      if (this.canvas && this.canvas.id !== 'toileCv') this.canvas.__porte = 1;
    }
    return dI.apply(this, arguments);
  };
  const gI = P.getImageData;
  P.getImageData = function(){
    const r = gI.apply(this, arguments), m = marque(this.canvas);
    if (m) { r.__dalle = 1; note('C·getImageData', ligne(), {m:m, cible:String(this.canvas.id||this.canvas.className||'?').slice(0,40)}); }
    return r;
  };
  const pI = P.putImageData;
  P.putImageData = function(im){
    const m = marque(this.canvas);
    if (m || (im && im.__dalle)) note('C·putImageData', ligne(), {m:m||'IMAGEDATA', cible:String(this.canvas.id||this.canvas.className||'?').slice(0,40)});
    return pI.apply(this, arguments);
  };
  const cP = P.createPattern;
  P.createPattern = function(src){
    const m = (src instanceof HTMLCanvasElement) ? marque(src) : null;
    if (m) note('E·motif', ligne(), {m:m});
    return cP.apply(this, arguments);
  };
  const tD = HTMLCanvasElement.prototype.toDataURL;
  HTMLCanvasElement.prototype.toDataURL = function(){
    const m = marque(this);
    if (m) note('E·image', ligne(), {m:m, src:[this.width,this.height]});
    return tD.apply(this, arguments);
  };

  // la Toile : on enveloppe ses peintres au moment où l'app les pose (window.Toile.x = function…)
  const PEINT = {dalleTrame:'__dalle', renderTo:'__toile', preview:'__toile', repaint:'__toile', repaintWorld:'__toile'};
  const enveloppe = (nom, f) => {
    if (typeof f !== 'function' || !PEINT[nom] || f.__env) return f;
    // pendant que le moteur peint, la cible EST une dalle : ses propres découpes sont comptées « moteur »
    const w = function(cv, pid){ let r; let avant = null; try { avant = (window.Toile && window.Toile.mondeCourant) ? window.Toile.mondeCourant() : null; } catch(_){}
                             try { if (cv && nom === 'dalleTrame') cv.__enCours = 1; r = f.apply(this, arguments); }
                             finally { try { if (cv) cv.__enCours = 0; } catch(_){} }
      // H · le monde — ⚑ v34 (Tom, 23 sept.) : « tout suit le Studio ; seule exception, l'Aura ». Hors de l'Aura une dalle se
      // peint dans le monde COURANT du Studio ; dans l'Aura (la Pelote, « Ce que tu as tenu »), dans celui de SA plantation.
      // Un aperçu qui montre EXPRÈS un autre monde (le rail du Studio, la Toile du Cercle) le déclare (`courant`) et sort.
      // (Avant v34 la règle était l'inverse : la plantation partout — original : sauvegardes/redteam_decoupe-avant-v34.py.)
      try { if (nom === 'dalleTrame' && r && cv.__dalleInfo && cv.__dalleInfo.monde && !cv.__dalleInfo.courant) {
          // ⚑ v50 : l'exception de l'Aura suit le PEINTRE, pas le nom de l'écran — l'Aura se bâtit aussi en arrière-plan
          // (l'export du Folio avec sa Pelote peint les îles et « Ce que tu as tenu »). Original : sauvegardes/redteam_decoupe-avant-v50.py.
          const pileA = String((new Error()).stack || '');
          // ⚑ v68 — le RÉCHAUFFAGE (`rechauffe`, v59) repeint en tâche de fond, pendant n'importe quel écran, des dalles d'AUTRES écrans
          // dans le monde courant : ce n'est pas un peintre de l'Aura (la règle v50 : l'exception suit le peintre). Original : sauvegardes/redteam_decoupe-avant-v68.py.
          const aura = (String((window.__decoupe || {}).ecran || '').indexOf('Aura') >= 0 && !/rechauffe/.test(pileA)) || /peintMoisson|Object\.pelote|batIles/.test(pileA);
          let q = null; for (const x of promises) { if (x.id === pid) { q = x; break; } }
          const M = cv.__dalleInfo.monde, C = aura ? (q && q.monde) : avant;
          if (C && (C.m !== M.m || C.p !== M.p || (+C.h || 0) !== (+M.h || 0)))
            note('H·monde', ligne(), {m:'MONDE', cible:(aura ? 'plantation ' : 'Studio ') + [C.m, C.p, +C.h || 0].join('/') + ' · peinte ' + [M.m, M.p, +M.h || 0].join('/')});
      } } catch(_){}
      try { if (cv && (nom !== 'dalleTrame' || r)) { cv[PEINT[nom]] = 1; if (nom === 'dalleTrame') { cv.__toile = 0; cv.__porte = 0; } } } catch(_){}
      return r; };
    w.__env = 1; return w;
  };
  let T;
  Object.defineProperty(window, 'Toile', { configurable:true,
    get(){ return T; },
    set(v){ if (v && typeof v === 'object') { for (const k in v) v[k] = enveloppe(k, v[k]);
              T = new Proxy(v, { set(o, k, f){ o[k] = enveloppe(k, f); return true; } }); }
            else T = v; } });
})();
"""


# G · on regarde chaque canevas VISIBLE qui porte une dalle : sa boîte affichée × densité doit valoir sa taille.
#   Le cadre vaut 390 px CSS dans une fenêtre de 430 (§8 : c'est la taille où #device est exactement 390).
AFFICHAGE = r"""()=>{ const J=window.__decoupe, dev=document.getElementById('device'); if(!dev) return;
  const D=dev.getBoundingClientRect(), sc=D.width/390, dpr=window.devicePixelRatio||1;
  document.querySelectorAll('canvas').forEach(c=>{
    if(!(c.__dalle||c.__porte) || c.id==='toileCv') return;
    const r=c.getBoundingClientRect(); if(r.width<6||r.height<6) return;
    if(r.right<D.left||r.left>D.right||r.bottom<D.top||r.top>D.bottom) return;
    let e=c, vu=true; while(e&&e!==document.body){ const s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden'||parseFloat(s.opacity)<0.05){vu=false;break;} e=e.parentElement; }
    if(!vu) return;
    const aff=r.width/sc*dpr, f=aff/c.width;
    if(Math.abs(f-1)>0.03){ const k=(c.id?'#'+c.id:'.'+String(c.className).split(' ')[0])+' '+c.width+'→'+Math.round(aff);
      J.aff=J.aff||{}; if(!J.aff[k]){ J.aff[k]=1; J.log.push({k:'G·affichage', l:0, e:J.ecran, m:'CSS', src:[c.width,c.height], rendu:[Math.round(aff),Math.round(r.height/sc*dpr)], cible:(c.id||String(c.className)).slice(0,40)}); } }
  }); }"""


MOTEUR_JS = []   # les lignes de promi-moteur.js (assainissement, 30 sept.) — une ligne y est notée 1 000 000 + son numéro


def bornes_moteur():
    """Le moteur (le bloc de la Toile) : dans app.html jusqu'au 30 sept., dans promi-moteur.js depuis l'assainissement.
    Même borne dans les deux cas : de `var host=document.getElementById('toileCv')` au premier `})();` qui suit — les
    blocs des mondes, qui le précèdent dans le fichier, restent HORS du moteur, comme avant."""
    import urllib.request
    src = urllib.request.urlopen(APP).read().decode('utf-8')
    L = src.split('\n')
    try:
        MOTEUR_JS[:] = urllib.request.urlopen(APP.rsplit('/', 1)[0] + '/promi-moteur.js').read().decode('utf-8').split('\n')
    except Exception:
        MOTEUR_JS[:] = []
    for base, T in ((0, L), (1000000, MOTEUR_JS)):
        lo = next((i for i, x in enumerate(T) if "var host=document.getElementById('toileCv')" in x), None)
        if lo is None: continue
        hi = next(i for i in range(lo, len(T)) if T[i].startswith('})();'))
        return base + lo, base + hi + 1, L  # lo = ligne de `(function(){` (1-indexé : i), hi = ligne du `})();` (1-indexé)
    raise SystemExit('moteur introuvable')


def empreinte(k, L, l):
    """Une prise se reconnaît au TEXTE de sa ligne, jamais à son numéro (qui bouge à chaque lot)."""
    import hashlib
    if isinstance(l, str): t = l          # G : l'élément affiché, pas une ligne
    elif l >= 1000000: t = re.sub(r'\s+', ' ', MOTEUR_JS[l - 1000001] if 0 < l - 1000000 <= len(MOTEUR_JS) else '').strip()
    else: t = re.sub(r'\s+', ' ', L[l - 1] if 0 < l <= len(L) else '').strip()
    return k.split('·')[0] + ':' + hashlib.sha1(t.encode('utf-8')).hexdigest()[:12]


def act(js):  # une action d'écran, bornée
    return "()=>{ try{ if(window.closeAll) closeAll(); }catch(e){} try{ " + js + " }catch(e){ window.__decoupe.log.push({k:'!·ouverture',l:0,e:window.__decoupe.ecran,err:String(e)}); } }"


ECRANS = [
    ('accueil · la Toile',   "setView('toile'); if(window.Toile&&Toile.sync){}", 1600),
    ('fiche tenue',          "const p=promises.filter(q=>q.title==='planter un arbre')[0]; openDetail(p.id);", 2200),
    ('fiche chiche',         "const p=promises.filter(q=>q.chiche&&!q.draft)[0]; openDetail(p.id);", 2200),
    ('fiche en cours',       "const p=promises.filter(q=>q.status==='encours'&&!q.chiche&&!q.draft)[0]; openDetail(p.id);", 2200),
    ('gardé de côté',        "const p=promises.filter(q=>q.draft)[0]; if(p) openDetail(p.id);", 2200),
    ('Nuée',                 "openEssaim('potager');", 2400),
    ('page +',               "document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);", 2400),
    ('Index',                "setView('toile'); ouvrirIndex();", 2400),
    ('Fil',                  "setView('fil');", 2600),
    ("l'instant",            "const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);", 3200),
    ('fiche personne',       "setView('toile'); openPerson('Rachel');", 2400),
    ('Aura · la Pelote',     "setView('toile'); document.getElementById('souffleBtn').click();", 3600),
    ('Studio',               "setView('toile'); document.getElementById('studioBtn').click();", 3000),
    ('Le Cercle',            "setView('toile'); if(window.ouvreCercle) ouvreCercle(); document.getElementById('plusScreen').classList.add('show'); if(window.drawCercleHero) drawCercleHero(); if(window.buildCercleHero) buildCercleHero();", 2600),
    ('Partager · Ma Toile',  "setView('toile'); openShare(); setTimeout(()=>{document.querySelector('#shMode [data-mode=toile]').click();},600);", 2800),
    ('Partager · Mon Folio', "setView('toile'); openShare(); setTimeout(()=>{document.querySelector('#shMode [data-mode=mosaic]').click();},600);", 2800),
    ('Partager · Folio + Pelote', "setView('toile'); openShare(); setTimeout(()=>{document.querySelector('#shMode [data-mode=mosaic]').click(); window.shPelote=true; shareRender();},600);", 3200),
    ('Partager · export Toile', "setView('toile'); openShare(); setTimeout(()=>{document.querySelector('#shMode [data-mode=toile]').click(); setTimeout(()=>{HTMLCanvasElement.prototype.toBlob=function(){}; (window._shExporteCanevas||window.shareExport)();},700);},600);", 4200),
    ('Partager · export Folio', "setView('toile'); openShare(); setTimeout(()=>{document.querySelector('#shMode [data-mode=mosaic]').click(); window.shPelote=true; setTimeout(()=>{HTMLCanvasElement.prototype.toBlob=function(){}; (window._shExporteCanevas||window.shareExport)();},900);},600);", 4600),
]


def main():
    lo, hi, L = bornes_moteur()
    tout = []; moteur = defaultdict(int); ouvertures = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for th in ['dark', 'light']:
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            ctx.add_init_script('window.__decoupeBornes=[%d,%d];' % (lo, hi))   # AVANT le chargement : le moteur peint dès le démarrage
            ctx.add_init_script(PIEGE)
            pg = ctx.new_page()
            pg.goto(APP); pg.evaluate("([a,b])=>{window.__decoupe.lo=a;window.__decoupe.hi=b;}", [lo, hi])
            pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(700)
            if MONDE_OPT: pg.evaluate("(w)=>{ window.__mondeOpt=w; }", MONDE_OPT)
            if MONDE_OPT:   # v34 : le STUDIO sur ce monde, les Promi plantés dans un autre — les deux règles sont exercées
                pg.evaluate("(w)=>{ const pl = (w === 'pixel') ? 'braille' : 'pixel'; promises.forEach(p=>{ p.monde=Object.assign({}, p.monde||Toile.mondeCourant(), {m:pl}); }); }", MONDE_OPT)
            # H : le monde COURANT doit différer du monde de plantation, sinon un oubli de monde ne se voit pas
            autre = pg.evaluate("""()=>{ const m=(promises.find(p=>p.monde&&!p.draft)||{}).monde||{}; 
                const w=(window.__mondeOpt)||['pixel','braille','mosaique','sillons','gravure','encre'].find(x=>x!==m.m); Toile.setTheme(w); return [m.m,w]; }""")
            pg.wait_for_timeout(900)
            for nom, js, att in ECRANS:
                pg.evaluate("(e)=>{window.__decoupe.ecran=e;}", th + ' · ' + nom)
                pg.evaluate(act(js)); pg.wait_for_timeout(att)
                pg.evaluate(AFFICHAGE)
            pg.evaluate("()=>{window.__decoupe.ecran='fin';}")
            J = pg.evaluate("()=>({log:window.__decoupe.log, moteur:window.__decoupe.moteur})")
            tout += J['log']
            for k, v in J['moteur'].items(): moteur[k] += v
            ctx.close()
        b.close()

    ouv = [x for x in tout if x['k'].startswith('!')]
    prises = [x for x in tout if not x['k'].startswith('ok') and not x['k'].startswith('!')]
    poses = [x for x in tout if x['k'].startswith('ok')]
    par = defaultdict(lambda: {'n': 0, 'ecrans': set(), 'ex': None})
    for x in prises:
        cle = (x['k'], x['l'] if x['l'] else 'CSS ' + str(x.get('cible', ''))); par[cle]['n'] += 1; par[cle]['ecrans'].add(x['e'].split(' · ', 1)[-1]); par[cle]['ex'] = x
    print('moteur de la Toile (l. %d–%d, relevé, non jugé) : %s' % (lo, hi, dict(moteur)))
    print('poses 1 : 1, à leur taille (autorisées) : %d' % len(poses))
    for x in ouv: print('⚠ ouverture en erreur :', x.get('e'), x.get('err'))
    print()
    familles = ['A·découpe', 'B·redimension', 'C·getImageData', 'C·putImageData', 'D·fragment', 'E·motif', 'E·image', 'F·photo', 'G·affichage', 'H·monde']
    for f in familles:
        lignes = sorted([(c, v) for c, v in par.items() if c[0] == f], key=lambda cv: str(cv[0][1]).zfill(8))
        print('%-16s %s' % (f, 'OK  aucune prise' if not lignes else 'KO  %d appels, %d lignes' % (sum(v['n'] for _, v in lignes), len(lignes))))
        for (k, l), v in lignes:
            ex = v['ex']; det = {kk: ex[kk] for kk in ('m', 'src', 'coupe', 'rendu', 'cible') if kk in ex}
            print('   l. %-6s ×%-4d %s   %s' % (l, v['n'], ', '.join(sorted(v['ecrans']))[:110], json.dumps(det, ensure_ascii=False)))
    for (k, l), v in par.items(): v['emp'] = empreinte(k, L, l)
    json.dump({'moteur': dict(moteur), 'prises': [dict(k=c[0], l=c[1], n=v['n'], emp=v['emp'], ecrans=sorted(v['ecrans'])) for c, v in par.items()]},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decoupe-releve.json'), 'w'), ensure_ascii=False, indent=1)
    if FIGER:
        import datetime
        json.dump({'date': datetime.date.today().isoformat(), 'pourquoi': "lignes connues du contrôle — chaque ligne est un chantier ouvert, pas une exemption. Née le 22 sept. 2026 (24 lignes), soldée en v29 (23 sept.)",
                   'lignes': sorted([dict(k=c[0], l=c[1], emp=v['emp']) for c, v in par.items()], key=lambda d: str(d['l']).zfill(8))},
                  open(DETTE, 'w'), ensure_ascii=False, indent=1)
        print('\ndette figée : %d lignes → %s' % (len(par), os.path.basename(DETTE)))
        return 0
    if RELEVE: return 0
    connues = set()
    try: connues = set(d['emp'] for d in json.load(open(DETTE))['lignes'])
    except Exception: pass
    neuves = [(c, v) for c, v in par.items() if v['emp'] not in connues]
    dette = [(c, v) for c, v in par.items() if v['emp'] in connues]
    print()
    for (k, l), v in sorted(neuves, key=lambda cv: str(cv[0][1]).zfill(8)):
        print('  ✗ NOUVELLE  %-15s l. %-6s ×%-4d %s' % (k, l, v['n'], ', '.join(sorted(v['ecrans']))[:100]))
    print('\n%s' % ('✅  AUCUNE DÉCOUPE NOUVELLE.' if not neuves else
                    '❌  %d LIGNE(S) NOUVELLE(S) découpent, redimensionnent ou relisent une dalle — régression.' % len(neuves)))
    if dette:
        print('❌  DETTE : %d lignes connues (%d appels) — la règle N’EST PAS tenue ; chantier ouvert, voir CONTRAT-MONDE.md §10.'
              % (len(dette), sum(v['n'] for _, v in dette)))
    else:
        print('✅  AUCUNE DÉCOUPE. Toute dalle est peinte par le moteur, à sa taille.')
    return 1 if neuves else 0

# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ⚑ v130 (Tom, C-048 — RÉCIDIVE) — FAMILLE G2 : UNE DALLE SEULE NE PORTE AUCUN MORCEAU DE LA TOILE.
#   « Dans les fiches, l'Index, le Fil et le fil d'un Cercle, on voit de nouveau des morceaux de Toile capturés dans un cadre, au lieu
#   de vraies dalles engendrées, avec leur forme et leur contour réels. […] redteam_decoupe doit couvrir tous ces écrans, Fil d'un
#   Cercle compris, et rougir sur l'état actuel. »
#   POURQUOI LES FAMILLES A–F NE LE VOYAIENT PAS : elles piègent ce que les ÉCRANS font d'une dalle (rogner, redimensionner, relire).
#   Ici la découpe était DANS le moteur : `dalleTrame` peignait la Toile autour de la dalle puis l'effaçait hors de la cellule.
#   CE QUE G2 MESURE : chaque dalle que le moteur rend seule (`Toile.dalleTrame`, piégé) pendant qu'on ouvre la fiche d'un Promi,
#   l'Index, le Fil, la fiche d'un Cercle et son fil défilé, sous les cinq mondes à trame, en clair et en sombre (palette Ingénu :
#   une dalle y a UNE couleur). Dans son canevas, la part des pixels opaques qui ne sont PAS de sa couleur — des éclats des voisines
#   ou du fond de la Toile — doit être nulle : décidé ≤ 0,3 % (l'anticrénelage), EN DUR.
#   Preuve : APP_DECOUPE=…/une copie servie avec le moteur d'avant v130 → ROUGE.
G2_MONDES = ['pixel', 'braille', 'mosaique', 'gravure', 'sillons']
G2_MAX = 0.3
G2_PIEGE = r"""()=>{ if(window.__g2) return; window.__g2=[]; const f=Toile.dalleTrame;
  Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
    if(monde&&monde.m&&monde.m!==Toile.getTheme()) return r;   /* une dalle rendue EXPRÈS dans un autre monde (les exemples) n'est pas de cette mesure */
    /* ⚠ et le monde RÉELLEMENT peint se lit sur ce que le moteur déclare (`__dalleInfo.monde`), jamais sur le thème supposé : l'app
       rend aussi des dalles dans le monde de son Studio (icônes de la page +, décor de l'Aura), qui n'est pas forcément celui que le
       juge vient de poser — vu : un cœur de Chamade compté comme « une autre couleur » sous Tesselle (1 passage sur 2). */
    try{ const mi=dcv.__dalleInfo&&dcv.__dalleInfo.monde; if(mi&&mi.m&&window.__g2m&&mi.m!==window.__g2m) return r; }catch(e){}
    try{ const g=dcv.getContext('2d'), w=dcv.width, h=dcv.height; if(w&&h){ const d=g.getImageData(0,0,w,h).data, H={}; let n=0;
        for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; n++; const q=(d[i]>>3)+','+(d[i+1]>>3)+','+(d[i+2]>>3); H[q]=(H[q]||0)+1; }
        let m=null,mc=0; for(const q in H) if(H[q]>mc){ mc=H[q]; m=q; }
        if(m&&n>60){ const c=m.split(',').map(v=>v*8+4); let au=0;
          /* ⚑ v131 (C-048) — LA « DALLE À 3,11 % » ÉTAIT DU JUGE. Reproduite en boucle (zz-v130, cinquante passages) : une dalle Tesselle
             rendue avec une RAMPE (`opts.rampe`, Q30 : la luminosité remappée sur les trois tons de la nature) — l'ombre de ses carreaux
             prend le ton sombre de la rampe, à plus de 48 du ton dominant. Ce sont SES couleurs, pas un morceau de voisine. Une couleur
             qui tombe sur la rampe déclarée (ses tons et leurs intermédiaires) n'est donc pas « une autre couleur ». */
          const RP=[]; try{ const cs=opts&&opts.rampe&&opts.rampe.cols; if(cs&&cs.length>1){ for(let a=0;a<cs.length-1;a++) for(let u=0;u<=12;u++){ const t=u/12; RP.push([cs[a][0]+(cs[a+1][0]-cs[a][0])*t, cs[a][1]+(cs[a+1][1]-cs[a][1])*t, cs[a][2]+(cs[a+1][2]-cs[a][2])*t]); } } }catch(e){}
          for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; if(Math.max(Math.abs(d[i]-c[0]),Math.abs(d[i+1]-c[1]),Math.abs(d[i+2]-c[2]))>48){
              let sur=false; for(let q=0;q<RP.length&&!sur;q++){ if(Math.max(Math.abs(d[i]-RP[q][0]),Math.abs(d[i+1]-RP[q][1]),Math.abs(d[i+2]-RP[q][2]))<=30) sur=true; }
              if(!sur) au++; } }
          const pp=(typeof promises!=='undefined')?promises.find(x=>x.id===pid):null, mi=dcv.__dalleInfo&&dcv.__dalleInfo.monde;
          window.__g2.push({pid:pid, monde:Toile.getTheme(), n:n, autres:+(100*au/n).toFixed(2), ecran:window.__g2e||'', qui:(pp?pp.title:'(pas une parole)')+' · '+w+'×'+h+' · monde peint '+(mi?mi.m:'non déclaré')+' · '+JSON.stringify(opts||{}).slice(0,60)}); } } }catch(e){}
    return r; }; }"""
G2_ECRANS = [('fiche Promi', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),
             ('Index', "()=>{closeAll(); setView('toile'); ouvrirIndex();}"),
             ('Fil', "()=>{closeAll(); document.getElementById('filBtn').click();}"),
             ('fiche Cercle et son fil', "()=>{closeAll(); openEssaim('potager');}"),
             ('fil du Cercle, défilé', "()=>{ const l=document.querySelector('#detailPoster .nf-liste, #detailPoster [class*=nf-]'); let n=l; while(n&&n.scrollHeight<=n.clientHeight+4) n=n.parentElement; if(n) n.scrollTop=n.scrollHeight; }")]

def famille_g2():
    from playwright.sync_api import sync_playwright
    ko = 0; total = 0
    print('\n— FAMILLE G2 (v130) · une dalle seule ne porte aucun morceau de la Toile — ≤ %.1f %% de pixels d\'une autre couleur —' % G2_MAX)
    with sync_playwright() as p:
        b = p.webkit.launch()
        for th in ('light', 'dark'):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
            pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{Toile.setPalette&&Toile.setPalette('signal')}catch(e){}}")
            pg.evaluate(G2_PIEGE)
            for m in G2_MONDES:
                pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m); window.__g2m=m; window.__g2.length=0;}", m); pg.wait_for_timeout(2500)
                vus = {}
                for nom, js in G2_ECRANS:
                    pg.evaluate("(n)=>{window.__g2e=n}", nom); pg.evaluate(js); pg.wait_for_timeout(2600)
                R = pg.evaluate("()=>window.__g2.filter(r=>r.monde===Toile.getTheme())")
                for nom, _ in G2_ECRANS:
                    L = [r for r in R if r['ecran'] == nom]
                    if not L: continue
                    pire = max(r['autres'] for r in L); total += 1; bon = pire <= G2_MAX
                    if not bon: ko += 1
                    print('  %s  %-9s %-5s %-26s %3d dalle(s) rendue(s) · au pire %.2f %% de pixels d\'une autre couleur' % ('OK' if bon else 'KO', m, th, nom, len(L), pire))
                    if not bon:      # un instrument NOMME ce qui rate (§8)
                        for r in sorted(L, key=lambda r: -r['autres'])[:3]:
                            if r['autres'] > G2_MAX: print('        ↳ %.2f %% · %s' % (r['autres'], r.get('qui', '')))
                ecr = set(r['ecran'] for r in R)
                if not R: ko += 1; print('  KO  %-9s %-5s aucune dalle rendue par le moteur : le piège n\'a rien vu' % (m, th))
            ctx.close()
        b.close()
    print('%s  G2 : %d écran(s) × monde × thème jugés, %d en défaut' % ('✅' if not ko else '❌', total, ko))
    return 1 if ko else 0

if __name__ == '__main__':
    _r1 = 0 if '--g2-seul' in sys.argv else main()
    _r2 = famille_g2()
    sys.exit(1 if (_r1 or _r2) else 0)
