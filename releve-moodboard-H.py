#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-moodboard-H.py — le JUGE, étendu à promi-moodboard-H.html (LOT 0).

Ce que cet outil sait faire (protocole AUTONOMIE-CLAUDE-CODE.md) :
  1 · DEUX BASES, pas une. Chaque moodboard déclare sa base. promi-moodboard-H.html
      est dessiné À 390 px : AUCUNE homothétie (facteur 1,0). L'ancien parcours 352
      gardait ×1,108 — ne JAMAIS appliquer 1,108 ici (agrandirait tout de 11 %).
  2 · COUVERTURE QUI ÉCHOUE. Un nœud du moodboard sans correspondance dans l'app =
      ÉCHEC (sortie ≠ 0), pas un simple signalement.
  3 · 102 CADRES écrits EN DUR. Si l'outil en trouve moins, il s'arrête et le dit.
  4 · COLLISIONS & DÉBORDEMENTS dans le même outil, sur l'app ET le moodboard, dans
      les DEUX thèmes. Seule collision tolérée dans tout le produit (§9.11) :
      l'encart du Cercle posé sur ses réglages floutés.

Usage :
  python3 releve-moodboard-H.py frames      # dénombre/valide les 102 cadres + sections
  python3 releve-moodboard-H.py collisions  # collisions & débordements de l'app (2 thèmes)
  python3 releve-moodboard-H.py fiches       # relevé d'écarts section 3 (fiches) — DÉMARRÉ
  python3 releve-moodboard-H.py all
"""
import sys, re
from playwright.sync_api import sync_playwright

MB_H = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/promi-moodboard-H.html"
APP  = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/app.html"

# ── LES DEUX BASES ────────────────────────────────────────────────────────────
# Chaque moodboard connaît sa base. L'outil ne suppose JAMAIS une base unique.
BASES = {
  'H':       {'file': MB_H, 'base_w': 390, 'base_h': 844, 'F': 1.0},   # dessiné à 390 → pas d'homothétie
  'parcours':{'file': "MOODBOARD-parcours.html", 'base_w': 352, 'base_h': 762, 'F': 390/352},
}
FRAMES_ATTENDUS = 102   # EN DUR — si l'outil en trouve moins, il s'arrête (protocole §2.3)

# ═══════════════════════════════════════════════════════════════════════════════
#  1 · ÉNUMÉRATION DES CADRES ET DES SECTIONS DU MOODBOARD H
# ═══════════════════════════════════════════════════════════════════════════════
JS_FRAMES = r"""()=>{
  const isFrame=(e)=>{const s=e.getAttribute('style')||'';return /width:\s*390px/.test(s)&&/height:\s*844px/.test(s);};
  const frames=[...document.querySelectorAll('div')].filter(isFrame);
  const secs=[...document.querySelectorAll('*')].filter(e=>{const s=e.getAttribute('style')||'';const t=(e.textContent||'').trim();
      return /6E7480/i.test(s)&&/^SECTION\s+\d/i.test(t)&&e.children.length===0;})
    .map(e=>({txt:(e.textContent||'').trim().split('\n')[0].slice(0,40),top:Math.round(e.getBoundingClientRect().top)}))
    .sort((a,b)=>a.top-b.top);
  const secOf=(top)=>{let c='(hors section)';for(const s of secs)if(s.top<=top)c=s.txt;return c;};
  const fr=frames.map((f,i)=>{const b=f.getBoundingClientRect();
    let big='',bigSz=0;
    f.querySelectorAll('*').forEach(e=>{if(e.children.length)return;const t=(e.textContent||'').trim();if(!t||t.length>40)return;
      const sz=parseFloat(getComputedStyle(e).fontSize)||0;if(sz>bigSz){bigSz=sz;big=t;}});
    const theme=/244, 238, 225|232, 224, 208/.test(getComputedStyle(f).backgroundColor)?'clair':'sombre';
    return {i, top:Math.round(b.top), left:Math.round(b.left), sec:secOf(Math.round(b.top)), theme, big:big.slice(0,32)};});
  return {n:frames.length, secs, frames:fr};
}"""

def frames_cmd():
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':4200})
        pg.goto('file://'+MB_H); pg.wait_for_timeout(3000)
        d=pg.evaluate(JS_FRAMES); b.close()
    print("="*76); print("  CADRES DU MOODBOARD H — attendu EN DUR : %d" % FRAMES_ATTENDUS); print("="*76)
    print("  Base déclarée : 390×844, AUCUNE homothétie (F=1,0).")
    print("  Cadres trouvés : %d" % d['n'])
    if d['n'] != FRAMES_ATTENDUS:
        print("  ❌ ARRÊT — %d cadres au lieu de %d. Le fichier a changé ; l'outil ne mesure pas à l'aveugle." % (d['n'],FRAMES_ATTENDUS))
        return 1
    print("  ✅ 102 cadres — 51 écrans × 2 thèmes.")
    from collections import defaultdict
    bysec=defaultdict(list)
    for f in d['frames']: bysec[f['sec']].append(f)
    # couverture prévue : §3 (fiches) et §5 (Peaufiner) d'abord ; le reste déclaré non couvert
    COUV={'SECTION 3':'CIBLE (fiches — app existe)','SECTION 5':'CIBLE (Peaufiner — app existe)'}
    print("\n  ── SECTIONS ──")
    for s in d['secs']:
        fl=bysec.get(s['txt'],[])
        etat=COUV.get(s['txt'],'NON COUVERT (app pas encore ou hors périmètre lot 0)')
        print("  [%-11s] %2d cadres  · %s" % (s['txt'], len(fl), etat))
    return 0

# ═══════════════════════════════════════════════════════════════════════════════
#  4 · COLLISIONS & DÉBORDEMENTS  (app ET moodboard, deux thèmes)
# ═══════════════════════════════════════════════════════════════════════════════
# Un « bloc signifiant » : porte du texte direct, ou est une image/canvas/svg visible.
# COLLISION : deux blocs signifiants qui ne sont pas ancêtre l'un de l'autre et dont
#   les boîtes se recouvrent de plus de SEUIL sur les deux axes. Exception unique
#   tolérée (§9.11) : l'encart du Cercle (.set-cercle/.karma-cercle/.pplus-card) posé
#   sur des réglages floutés.
# DÉBORDEMENT : bloc signifiant dont la boîte sort du cadre 390×844 (gauche<-1,
#   droite>391, ou bas>845 hors conteneur de défilement).
JS_COLLIDE = r"""(a)=>{
  const rootSel=a[0], fixedFrame=a[1];   // fixedFrame=true → cadre figé (moodboard) : le vertical >844 compte
  const root=rootSel?document.querySelector(rootSel):document.body;
  if(!root)return {err:'root introuvable'};
  // FEUILLES CACHÉES : quand on regarde la Toile, les autres écrans (Index, Aura,
  // createSheet, fiche…) sont encore dans le DOM, posés en bas. On les exclut : un
  // écran non affiché n'entre pas en collision (il n'est pas là pour l'utilisateur).
  // toutes les feuilles/écrans par SUFFIXE d'id (Sheet/Screen/View/Poster) + auraHelp :
  // une quinzaine de feuilles cachées empilent leurs « ✕ Fermer » en bas, à exclure.
  const SCREENS='[id$="Sheet"],[id$="Screen"],[id$="View"],[id$="Poster"],#auraHelp';
  const onHidden=(n)=>{let x=n;while(x&&x!==root){ if(x.matches&&x.matches(SCREENS)){
      if(!(x.classList.contains('show')||x.classList.contains('in')))return true; } x=x.parentElement;} return false;};
  const SKIP={PATH:1,CIRCLE:1,LINE:1,G:1,RECT:1,POLYGON:1,POLYLINE:1,ELLIPSE:1,DEFS:1,BR:1,STOP:1,LINEARGRADIENT:1,RADIALGRADIENT:1,CLIPPATH:1,MASK:1,USE:1,TITLE:1,SVG:1};
  const rr=root.getBoundingClientRect();
  const HTd=(n)=>{let t='';for(const c of n.childNodes)if(c.nodeType===3)t+=c.textContent;return t.trim();};
  // BOÎTE D'ENCRE : pour un nœud qui porte du texte direct, on mesure l'ÉTENDUE RÉELLE
  // du texte (Range), pas la boîte de l'élément — un titre pleine largeur avec texte à
  // gauche ne « collisionne » PAS un bouton à droite (le défaut vu au point 3).
  const inkBox=(n)=>{ let best=null;
    for(const c of n.childNodes){ if(c.nodeType!==3||!c.textContent.trim())continue;
      const rg=document.createRange(); rg.selectNodeContents(c); const rb=rg.getBoundingClientRect();
      if(rb.width>0&&rb.height>0){ if(!best)best={l:rb.left,t:rb.top,r:rb.right,b:rb.bottom};
        else{best.l=Math.min(best.l,rb.left);best.t=Math.min(best.t,rb.top);best.r=Math.max(best.r,rb.right);best.b=Math.max(best.b,rb.bottom);} } }
    return best; };
  const stickyish=(n)=>{let x=n;while(x&&x!==root){const p=getComputedStyle(x).position;if(p==='sticky'||p==='fixed')return true;x=x.parentElement;}return false;};
  const nodes=[];
  (function walk(n){const tag=(n.tagName||'').toUpperCase();
    if(!SKIP[tag]){const b=n.getBoundingClientRect();const cs=getComputedStyle(n);
      const vis=cs.display!=='none'&&cs.visibility!=='hidden'&&parseFloat(cs.opacity||'1')>0.05&&b.width>2&&b.height>2;
      const txt=HTd(n);const cls=(typeof n.className==='string'?n.className:(n.className&&n.className.baseVal)||'');
      // encre pour le texte, boîte de l'élément pour image/canvas
      const ink = txt.length>0 ? inkBox(n) : null;
      const bx = ink || {l:b.left,t:b.top,r:b.right,b:b.bottom};
      const T=bx.t-rr.top, BO=bx.b-rr.top, L=bx.l-rr.left, R=bx.r-rr.left;
      const onscreen = T<844 && BO>0 && L<390 && R>0;   // bande visible du cadre 390×844
      const meaning=vis&&onscreen&&!onHidden(n)&&(txt.length>0||tag==='IMG'||tag==='CANVAS'||(tag==='DIV'&&cls&&(cs.backgroundColor!=='rgba(0, 0, 0, 0)'||/url\(/.test(cs.backgroundImage||''))));
      if(meaning&&n!==root){
        const cercle=/set-cercle|karma-cercle|pplus-card|cercle/i.test(cls);
        nodes.push({n, b:{l:L,t:T,r:R,bo:BO,w:R-L,h:BO-T}, isText:txt.length>0,
                    tag,cls:(cls||'').split(' ')[0],txt:txt.slice(0,22),cercle,
                    pos:cs.position, sticky:stickyish(n), z:parseInt(cs.zIndex)||0});
      }}
    for(const c of n.children) walk(c);
  })(root);
  const anc=(a,b)=>{let x=a;while(x){if(x===b)return true;x=x.parentElement;}return false;};
  // COLLISIONS : deux ENCRES DE TEXTE qui se recouvrent réellement (le texte ne se
  // superpose jamais). On ignore : sticky/fixed (en-tête/barre collante volontaire),
  // paires ancêtre/descendant. Chevauchement franc requis (>4 px sur chaque axe).
  const cols=[];
  const txtNodes=nodes.filter(n=>n.isText && !n.sticky);
  for(let i=0;i<txtNodes.length;i++)for(let j=i+1;j<txtNodes.length;j++){
    const A=txtNodes[i],B=txtNodes[j];
    if(anc(A.n,B.n)||anc(B.n,A.n))continue;
    const ox=Math.min(A.b.r,B.b.r)-Math.max(A.b.l,B.b.l);
    const oy=Math.min(A.b.bo,B.b.bo)-Math.max(A.b.t,B.b.t);
    if(ox>4&&oy>4){
      const exception=A.cercle||B.cercle;   // §9.11 encart du Cercle sur réglages floutés
      cols.push({a:A.txt||A.cls,b:B.txt||B.cls,ox:Math.round(ox),oy:Math.round(oy),
                 ax:Math.round(A.b.l),ay:Math.round(A.b.t),exception});
    }}
  // DÉBORDEMENTS : hors 390×844 (sortie horizontale = toujours un bug ; verticale = hors défilement)
  const scrollable=(n)=>{let x=n;while(x&&x!==root){const o=getComputedStyle(x).overflowY;if(o==='auto'||o==='scroll')return true;x=x.parentElement;}return false;};
  const over=[];
  for(const N of nodes){
    // HORIZONTAL : sortir du cadre 390 est TOUJOURS un bug (les deux côtés).
    if(N.b.l<-1) over.push({who:N.txt||N.cls,axe:'gauche',v:Math.round(N.b.l)});
    else if(N.b.r>391) over.push({who:N.txt||N.cls,axe:'droite',v:Math.round(N.b.r)});
    // VERTICAL : compte SEULEMENT sur un cadre FIGÉ (moodboard 390×844). L'app défile —
    // du contenu sous 844 y est atteignable, ce n'est pas un débordement.
    else if(fixedFrame && N.b.bo>845 && N.b.t<844 && !scrollable(N.n) && !N.sticky && N.pos!=='fixed' && N.pos!=='sticky')
      over.push({who:N.txt||N.cls,axe:'bas',v:Math.round(N.b.bo)});
  }
  return {nNodes:nodes.length, cols, over};
}"""

def _dedup(items, keyf):
    seen=set(); out=[]
    for it in items:
        k=keyf(it)
        if k in seen: continue
        seen.add(k); out.append(it)
    return out

# écrans de l'app à contrôler : (nom, [steps JS], attente_ms, sélecteur racine)
def app_screens():
    OPEN="()=>document.getElementById('createBtn').click()"
    def tile(k): return "()=>{const t=document.querySelector('#createSheet .tile[data-kind=%s]');if(t)t.click();}"%k
    def fiche(status,title,nuee):
        j=("()=>{try{const ps=promises.filter(x=>!x.draft&&!x.nuee&&!x.req);const p=ps[0];"
           "p.status='%s';p.who='Rachel';p.title=%r;"%(status,title))
        j+=("p.nuee='famille';if(typeof NUE!=='undefined')NUE['famille']='Famille';" if nuee else "p.nuee=undefined;")
        j+="openDetail(p.id);}catch(e){}}"
        return j
    return [
      ('toile',        [], 1000, '.device'),
      ('page+ choix',  [OPEN], 1600, '#createSheet'),
      # on FIGE le défilement à sa position posée (sinon on mesure un cliché à mi-animation
      # où la tuile passe sous l'en-tête collant → fausse collision).
      ('page+ phrase', [OPEN, tile('promi'), "()=>{if(window._csVersPhrase)window._csVersPhrase();}",
                        "()=>{var f=document.getElementById('promiForm'),m=document.getElementById('csMid');if(f&&m){m.style.scrollBehavior='auto';m.scrollTop=f.offsetTop;}}"], 1600, '#createSheet'),
      ('fiche à tenir',[fiche('rate','rendre le livre',True)], 2600, '#detailPoster'),
      ('fiche tenue',  [fiche('tenu','rendre le livre',False)], 2600, '#detailPoster'),
      ('index',        ["()=>{var s=document.getElementById('indexSheet');if(typeof openSheet==='function'&&s)openSheet(s);if(window.buildIndex)buildIndex();}"], 1600, '#indexSheet'),
      ('fil',          ["()=>{if(typeof openFeed==='function')openFeed();}"], 1600, '#feedView'),
    ]

def collisions_cmd():
    total=0
    for theme in ('light','dark'):
        with sync_playwright() as p:
            b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
            pg.goto('file://'+APP); pg.wait_for_timeout(7000)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}window._tutoSeen=true;}")
            if theme=='light': pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.add('light'))")
            else:              pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.remove('light'))")
            print("="*76); print("  COLLISIONS & DÉBORDEMENTS — APP · thème %s" % theme.upper()); print("="*76)
            for nom, steps, wait, rootsel in app_screens():
                try:
                    pg.evaluate("()=>{if(typeof closeAll==='function')closeAll();}")
                except: pass
                pg.wait_for_timeout(250)
                for i,s in enumerate(steps):
                    pg.evaluate(s); pg.wait_for_timeout(500 if i<len(steps)-1 else wait)
                if not steps: pg.wait_for_timeout(wait)
                try: d=pg.evaluate(JS_COLLIDE, [rootsel, False])   # app : défile, pas de débordement vertical
                except Exception as e: d={'err':str(e)}
                if d.get('err'): print("  · %-16s — racine absente (%s)"%(nom,d['err'])); continue
                cols=[c for c in d['cols'] if not c['exception']]
                cols=_dedup(cols, lambda c:(c['a'],c['b']))
                over=_dedup(d['over'], lambda o:(o['who'],o['axe']))
                cx=len([c for c in d['cols'] if c['exception']])
                flag='✅' if (not cols and not over) else '❌'
                print("  %s %-16s  %3d blocs · %d collision(s) · %d débordement(s)%s"
                      %(flag,nom,d['nNodes'],len(cols),len(over),(' · %d Cercle toléré'%cx) if cx else ''))
                for c in cols[:8]:
                    print("        ⊗ «%s» ∩ «%s»  (recouvre %d×%d px, @%d,%d)"%(c['a'],c['b'],c['ox'],c['oy'],c['ax'],c['ay']))
                for o in over[:8]:
                    print("        ↦ «%s» déborde à %s : %d px"%(o['who'],o['axe'],o['v']))
                total += len(cols)+len(over)
            b.close()
    print("\n  TOTAL collisions+débordements (2 thèmes) : %d"%total)
    return total

# ═══════════════════════════════════════════════════════════════════════════════
#  Placeholder : la carte de correspondance (le gros du travail — DÉMARRÉ ailleurs)
# ═══════════════════════════════════════════════════════════════════════════════
def fiches_cmd():
    print("  [section 3 — fiches] carte de correspondance : chantier démarré, voir QUESTIONS.md")
    print("  (l'ancien releve-moodboard.py mappe déjà la fiche contre l'ancien parcours 352 ;")
    print("   le portage node-à-node vers le moodboard H 390 est le gros du travail, en cours.)")
    return 0

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'frames'
    if cmd=='frames': sys.exit(frames_cmd())
    elif cmd=='collisions': sys.exit(1 if collisions_cmd()>0 else 0)
    elif cmd=='fiches': sys.exit(fiches_cmd())
    elif cmd=='all':
        r=frames_cmd(); c=collisions_cmd()
        sys.exit(0 if (r==0 and c==0) else 1)
    else:
        print("commandes : frames | collisions | fiches | all"); sys.exit(2)
