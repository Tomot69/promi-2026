# -*- coding: utf-8 -*-
"""L'AIR ENTRE LES TEXTES — deux blocs ne se rapprochent jamais.

   POURQUOI CE CONTRÔLE EXISTE (décision Tom, 29 août 2026, au soir)
   ─────────────────────────────────────────────────────────────────
   « Tu as grossi les textes sans reprendre les écarts. » Monter une taille — 21→23,
   38→42, 12,5→13,5 — ne déplace AUCUN `top` : c'est la HAUTEUR des blocs qui grandit,
   vers le bas. L'air se mange donc en silence, partout où la cote suivante avait été
   calculée pour l'ancienne taille. Mesuré à la livraison : `à qui → titre` était tombé
   de 6,9 à 4,7 px sur les CINQ états de fiche, et le mot d'un gardé de côté n'avait plus
   que 9 px sous sa pastille là où le cadre 26 en donne 23.

   Aucun relevé de POSITIONS ne pouvait le voir : les tops n'avaient pas bougé.
   On mesure donc L'ESPACE RÉEL — bas du bloc A → haut du bloc B — entre deux textes qui
   se recouvrent horizontalement, sur chaque écran, dans les deux thèmes.

   LA RÈGLE : deux blocs de texte ne sont jamais à moins de leur écart d'origine.
   La référence est `air-reference.json`, figée après le lot qui l'a corrigée — comme
   `releve-design.py` fige la sienne. `--figer` la réécrit, et RIEN D'AUTRE ne la réécrit.

   ⚠ CE QU'ON NE MESURE PAS, ET POURQUOI
   · Les nœuds des AUTRES écrans. Le DOM les garde ; ils ne sont pas « à côté » de ce qu'on
     regarde. On se scope donc à LA FEUILLE DU DESSUS — celle qui couvre au moins 55 % de
     l'appareil — exactement comme le balayage de collisions.
   · La barre Peaufiner (`#dpdTog`), qui est COLLANTE : un fil défile dessous, c'est le
     dessin. Un écart négatif avec elle ne dit rien.
   · Les conteneurs : on ne garde que la feuille du dessus qui porte des mots, sinon on
     mesurerait un bloc contre son propre enfant.
"""
import sys, json, os
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_AIR', "http://127.0.0.1:8752/app.html")
REF = 'air-reference.json'
TOL = 0.6          # le bruit de rendu : en dessous, ce n'est pas un resserrement

ECRANS = [
 ('fiche tenue',   "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche à tenir', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours',"()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche chiche',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('chiche lancé',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; if(p)openDetail(p.id);}"),
 ('gardé de côté', "()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"),
 ('page +',        "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('Peaufiner',     "()=>{closeAll(); const p=promises.filter(q=>!q.draft)[0]; openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('Index 2',       "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
 ('Index 3',       "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}"),
 ('Fil',           "()=>{closeAll(); setView('fil');}"),
 ('Nuée',          "()=>{closeAll(); openEssaim('potager');}"),
 ('Nuée vide',     "()=>{closeAll(); openEssaim('atelier');}"),
 ('Peaufiner Nuée',"()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ("l'instant arrive",  "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);}}"),
 ("l'instant referme", "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('referme');}catch(e){}},900);}}"),
 ("l'instant après",   "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},900);}}"),
 ('Réglages',      "()=>{closeAll(); document.getElementById('settingsBtn').click();}"),
 # ⚑ L'AURA ENTRE DANS LA LISTE — 10 septembre 2026, au portage de l'Orbite. C'est ce qui
 #   fait MORDRE le contrôle du bloc centré : la légende se déclare `data-centre-entre`,
 #   et un contrôle qui n'ouvre jamais l'écran ne la mesure jamais. Ses paires de textes
 #   n'ont pas encore de référence : elles n'entrent dans `air-reference.json` qu'au
 #   `--figer` qui suivra la validation du lot (rien d'autre ne réécrit la référence).
 #   Original : sauvegardes/redteam_air-avant-aura-orbite.py
 ('Aura',          "()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('souffleBtn').click();}"),
]

MESURE = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(), sc=dev.width/390;
  const EN_LIGNE=['B','I','EM','STRONG','SPAN','SMALL','BR','U','A','CODE','SUP','SUB'];
  /* LA FEUILLE DU DESSUS : celle qui couvre au moins 55 % de l'appareil, la dernière dans
     l'ordre du document. Sans ce cadrage, on compare le titre d'une fiche au bouton de
     l'Aura, qui vit sur un autre écran — le DOM les garde tous. */
  let hote=document.getElementById('device'), best=-1;
  document.querySelectorAll('#device .sheet, #device .poster, #device .scr, #device [id]')
    .forEach(e=>{ const c=getComputedStyle(e);
      if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.5) return;
      const r=e.getBoundingClientRect();
      const part=(r.width*r.height)/(dev.width*dev.height);
      if(part>=0.55 && part<=1.02){ const z=+c.zIndex||0;
        const rang=z*1000 + [...document.querySelectorAll('*')].indexOf(e)/1e6;
        if(rang>=best){ best=rang; hote=e; } } });
  const COLLANT=['dpdTog','dpDetails'];      /* la barre Peaufiner : un fil défile dessous */
  const bl=[];
  hote.querySelectorAll('*').forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return;
    for(let n=e; n && n!==hote; n=n.parentNode)
      if(n.id && COLLANT.includes(n.id)) return;
    const t=(e.textContent||'').trim(); if(!t) return;
    for(const k of e.children){ if(!EN_LIGNE.includes(k.tagName) && (k.textContent||'').trim()) return; }
    const r=e.getBoundingClientRect();
    const x=(r.x-dev.x)/sc, y=(r.y-dev.y)/sc, w=r.width/sc, h=r.height/sc;
    if(w<12||h<6||y<-40||y>884) return;
    /* ⚑ ON IDENTIFIE UNE CARTE PAR SON TITRE, JAMAIS PAR SON RANG — Tom, 18 septembre 2026.
       « On compare par titre et personne, jamais par position. C'est déjà au §8 pour les ids. »
       Sans ça, plusieurs cartes d'Index donnent la MÊME clé (`.s4-natlab«Promi»` revient sur
       chacune) : les paires se télescopent, la référence garde celle qui passait en premier, et
       l'ordre du jeu de démonstration changeant d'un chargement à l'autre, le juge comparait
       DEUX CARTES DIFFÉRENTES. Mesuré : 48 px au gel, 26 px à la passe suivante, sur la même
       clé — et l'air réel, lui, stable à 105 px sur quatre passes d'une même session.
       Version d'avant : sauvegardes/redteam_air-avant-CARTE.py */
    let carte='';
    for(let n=e; n && n!==hote; n=n.parentNode){
      if(n.classList && (n.classList.contains('s4-carte') || n.classList.contains('ix-bloc')
                      || n.classList.contains('fd-item') || n.classList.contains('nf-item'))){
        const ti=n.querySelector('.s4-ti,.ix-t,.fd-t,.nf-tx,.s4-titre');
        const qui=n.querySelector('.s4-eb,.ix-qui,.fd-pre');
        carte='['+((ti&&(ti.textContent||'').trim().slice(0,22))||'?')
             +'·'+((qui&&(qui.textContent||'').trim().slice(0,14))||'?')+']';
        break;
      }
    }
    bl.push({cle:carte+(e.id? '#'+e.id : '.'+(''+e.className).split(' ').filter(Boolean).slice(0,2).join('.')),
             mot:t.slice(0,20), x, y, w, h});
  });
  bl.sort((a,b)=>a.y-b.y);
  const paires=[];
  for(let i=0;i<bl.length;i++){
    let best=null;
    for(let j=0;j<bl.length;j++){
      if(i===j) continue;
      const a=bl[i], b=bl[j];
      if(b.y < a.y+a.h-0.5) continue;
      const rec=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x);
      if(rec < Math.min(a.w,b.w)*0.34) continue;
      const g=b.y-(a.y+a.h);
      if(!best || g<best.g) best={g:g, b:b};
    }
    if(best && best.g<200)
      paires.push([bl[i].cle+'«'+bl[i].mot+'»', best.b.cle+'«'+best.b.mot+'»',
                   Math.round(best.g*10)/10]);
  }
  return paires;
}"""

# ⚑ v21 — les exemples de la page + TOURNENT (Tom, 22 sept.) : chaque relevé repart des compteurs à zéro, donc du
#   PREMIER exemple de chaque liste — sans quoi l'air mesuré dépendrait du tirage. Original : sauvegardes/redteam_air-avant-v21.py
RAZ_EX = "()=>{try{['soi','demander','chiche','nuee'].forEach(function(k){localStorage.removeItem('promi_ex_'+k);}); if(window._ppExempleRaz) window._ppExempleRaz();}catch(e){}}"

def releve(pg, js):
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
    pg.evaluate(RAZ_EX)
    try: pg.evaluate(js)
    except Exception: pass
    pg.wait_for_timeout(2000)
    prec, stable = None, 0
    for _ in range(20):
        pg.wait_for_timeout(250)
        n = pg.evaluate("()=>[...document.querySelectorAll('#device *')]"
                        ".filter(e=>{const r=e.getBoundingClientRect();return r.width>4&&r.height>4;}).length")
        stable = stable + 1 if n == prec else 0
        prec = n
        if stable >= 2: break
    pg.wait_for_timeout(250)
    return pg.evaluate(MESURE)

def passe():
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate('()=>{var o=document.getElementById("promiOnb");'
                    'if(o){o.classList.add("gone");o.style.display="none";}}')
        for th in ('dark','light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for nom, js in ECRANS:
                out['%s [%s]' % (nom, th)] = releve(pg, js)
        b.close()
    return out

def ecarts_centres():
    """Relève, sur chaque écran, les blocs qui se déclarent centrés entre deux
       voisins, et rend ceux dont les deux écarts diffèrent de plus d'un pixel.
       Le contrôle est SILENCIEUX tant qu'aucun nœud ne se déclare : il ne
       coûte rien aux écrans qui n'en ont pas."""
    from playwright.sync_api import sync_playwright
    mauvais = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for nom, ouvre in ECRANS:
            pg.evaluate(RAZ_EX)
            try: pg.evaluate(ouvre)
            except Exception: continue
            pg.wait_for_timeout(700)
            try:
                out = pg.evaluate("""()=>{
                  var res=[];
                  document.querySelectorAll('[data-centre-entre]').forEach(function(el){
                    if(!el.getClientRects().length) return;
                    var p=el.getAttribute('data-centre-entre').split('|');
                    var sc=el.closest('.screen')||document;
                    var A=sc.querySelector(p[0]), B=sc.querySelector(p[1]);
                    if(!A||!B) return;
                    var a=A.getBoundingClientRect(), e=el.getBoundingClientRect(),
                        c=B.getBoundingClientRect();
                    /* v95 : un 4e champ nomme ce qui FERME le bloc centré (l'Aura : « légende + chiffres ») */
                    if(p.length>3){ var Z=sc.querySelector(p[3]); if(Z){ var z=Z.getBoundingClientRect(); e={top:e.top, bottom:Math.max(e.bottom,z.bottom)}; } }
                    res.push([el.getAttribute('data-centre-entre'),
                              +(e.top-a.bottom).toFixed(2), +(c.top-e.bottom).toFixed(2),
                              p.length>2 ? +p[2] : 0]);
                  });
                  return res;}""")
            except Exception:
                continue
            # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (Tom, 22 sept. : « l'air au-dessus et en dessous
            #   doit être égal, À L'ENCRE » ; 23 sept. : le voisin du bas de la légende devient LE
            #   BOUTON, dont le contour commence plus haut dans sa boîte qu'une encre de titre).
            #   L'égalité à l'encre ne se lit donc plus dans des BOÎTES égales : l'écart de boîte
            #   attendu est celui que l'écran DÉCLARE, troisième champ de `data-centre-entre`.
            #   L'égalité d'encre elle-même se mesure sur l'IMAGE, dans `releve-aura` (« air de la
            #   colonne »). Original : sauvegardes/redteam_air-avant-v13.py
            for sel, av, ap, dec in out:
                if abs((av-ap) - dec) > 1.0:
                    mauvais.append((nom, sel, av, ap))
    return mauvais


if __name__ == '__main__':
    r = passe()
    if '--figer' in sys.argv:
        json.dump(r, open(REF,'w'), ensure_ascii=False)
        print('Référence figée : %d écrans, %d paires de textes.'
              % (len(r), sum(len(v) for v in r.values())))
        sys.exit(0)
    if not os.path.exists(REF):
        print('Aucune référence. Lance : python3 redteam_air.py --figer'); sys.exit(1)
    ref = json.load(open(REF))
    perdu = []
    for ecr in sorted(r):
        R = {(a,b): g for a,b,g in ref.get(ecr, [])}
        for a,b,g in r[ecr]:
            if (a,b) in R and g < R[(a,b)] - TOL:
                perdu.append((round(R[(a,b)]-g,1), ecr, a, b, R[(a,b)], g))
    perdu.sort(reverse=True)
    n = sum(len(v) for v in r.values())

    # ══════════════════════════════════════════════════════════════════════
    # ⚑ UN BLOC ANNONCÉ CENTRÉ ENTRE DEUX VOISINS A DES ÉCARTS ÉGAUX.
    #   Décision Tom, 10 septembre 2026, après TROIS demandes sur la même
    #   légende de l'Aura : je la « rapprochais à l'œil » au lieu de mesurer
    #   une fois. Relevé du défaut : 8 px au-dessus, 40 en dessous.
    #   Le bloc se DÉCLARE (`data-centre-entre="selHaut|selBas"`) — un contrôle
    #   qui devinerait les voisins se tromperait de nœud ; c'est l'écran qui
    #   sait. Tolérance : 1 px, la moitié d'un pixel d'appareil.
    # ══════════════════════════════════════════════════════════════════════
    centre = ecarts_centres()
    print()
    if centre:
        print("  ❌  %d BLOC(S) ANNONCÉ(S) CENTRÉ(S) NE LE SONT PAS" % len(centre))
        print("      « un bloc centré entre deux voisins a des écarts égaux »\n")
        for e, sel, a, b in centre:
            print('   %-22s %-26s  au-dessus %6.1f   en dessous %6.1f   écart %5.1f'
                  % (e, sel[:26], a, b, abs(a-b)))
        sys.exit(1)

    print()
    if perdu:
        print("  ❌  %d PAIRE(S) DE TEXTES SE SONT RAPPROCHÉES" % len(perdu))
        print("      « deux blocs de texte ne doivent jamais être à moins de leur écart"
              " d'origine »\n")
        for d, e, a, b, av, ap in perdu[:40]:
            print('   −%-5s %-24s %-34s → %-30s  (%s → %s)'
                  % (d, e, a[:34], b[:30], av, ap))
        if len(perdu) > 40: print('   … et %d autres.' % (len(perdu)-40))
        print("\n  Si le lot demandait ce resserrement, refige : python3 redteam_air.py --figer")
        sys.exit(1)
    print("  ✅  L'AIR EST INTACT — %d paires de textes, %d écrans, deux thèmes."
          % (n, len(r)))
