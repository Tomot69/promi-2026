#!/usr/bin/env python3
"""
redteam_cercle_tom.py — LA FICHE D'UN CERCLE, PAR LE CHEMIN DE TOM (v142, Tom, 11 oct. 2026 — C-096, DEUX RÉCIDIVES).

« Sur la fiche elle-même, ouverte depuis la Toile de l'accueil, Tom voit toujours le bandeau Peaufiner mal placé. […] bandeau tout en bas comme
sur toute fiche, “+ Planter dans le Cercle” 12 pt au-dessus, le fil qui défile dessous. Ton juge passait par un autre chemin : il doit passer
par celui-ci. » · « “Dissoudre le Cercle” a toujours son encart. Il prend exactement les éléments et le dessin de “Supprimer ce Promi”. »

POURQUOI LES JUGES DE v141 ÉTAIENT VERTS : `redteam_nuee` ouvre le Cercle du jeu de démonstration (neuf paroles) par `openNuee`, à l'échelle 1
(430 × 932). Tom crée son Cercle au +, l'ouvre en touchant sa dalle, et son appareil est RÉDUIT à l'écran : WebKit y colle un élément
`sticky` au bas de la zone visible comptée en points d'écran (le bandeau à 703 au lieu de 760). Et la règle de v141 sur « Dissoudre » ne
peignait rien (un style en ligne `!important` la battait) : aucune capture n'avait été regardée.

Banc « comme Tom » (banc_tom.py) : WebKit, 390 × 844 ×3 (appareil à 0,93), Toile vide, Cercle créé par le +, fiche ouverte au doigt sur sa
dalle. Cotes en points de l'appareil, EN DUR : bandeau 760 → 844 ; bouton 686 → 748 (12 pt au-dessus).

Usage : python3 redteam_cercle_tom.py [fichier.html] [--planche]
"""
import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
HIT = """(kind)=>{ let sx=0,sy=0,n=0; for(let y=110;y<700;y+=4)for(let x=4;x<386;x+=4){const h=Toile.hit(x,y); if(h&&(kind==='nuee'?h.kind==='nuee':h.pid!=null)){sx+=x;sy+=y;n++;}} return n?[sx/n,sy/n,n]:null; }"""
COTES = """()=>{ const dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [(r.top-dv.top)/k,(r.bottom-dv.top)/k]; };
  const cartes=[...document.querySelectorAll('#dpNueeFil .nf-item')].map(R);
  return {bandeau:R(document.getElementById('dpdTog')), bouton:R(document.getElementById('nfAdd')), cartes:cartes, n:cartes.length, scroll:document.getElementById('detailPoster').scrollTop}; }"""
STYLE = """(sel)=>{ const e=[...document.querySelectorAll(sel)].find(x=>x.getBoundingClientRect().height>0); if(!e) return null; const c=getComputedStyle(e), p=e.parentElement, cp=getComputedStyle(p), a=getComputedStyle(p,'::before'), dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390, r=e.getBoundingClientRect(), rp=p.getBoundingClientRect();
  const al=s=>{ const m=/rgba?\\(([^)]+)\\)/.exec(s); if(!m) return 1; const t=m[1].split(','); return t.length>3?parseFloat(t[3]):1; };
  return {taille:c.fontSize, graisse:c.fontWeight, chasse:c.letterSpacing, casse:c.textTransform, police:c.fontFamily.split(',')[0], couleur:c.color, contourVisible:(parseFloat(cp.borderTopWidth)>0&&al(cp.borderTopColor)>0.02), fondVisible:al(cp.backgroundColor)>0.02, corbeille:a.width+' '+a.backgroundColor, centre:Math.round(((r.left+r.right)/2-(rp.left+rp.right)/2)/k), texte:e.textContent.trim().toUpperCase()}; }"""
BAS = "()=>{ const P=document.getElementById('detailPoster'); P.scrollTop=99999; [...P.querySelectorAll('*')].forEach(e=>{ if(e.scrollHeight>e.clientHeight+20&&/(auto|scroll)/.test(getComputedStyle(e).overflowY)) e.scrollTop=99999; }); }"
def pres(a, b, tol=1.0): return a is not None and abs(a - b) <= tol
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        th = 'sombre' if sombre else 'clair'
        ctx = contexte(b, sombre=sombre); pg = ouvre(ctx, F)
        # le dessin de référence : « Supprimer ce Promi », sur la fiche d'un Promi planté au +
        plante(pg, 'boire un verre'); pg.wait_for_timeout(1200)
        h = pg.evaluate(HIT, 'promi'); tap(pg, h[0], h[1]); pg.wait_for_timeout(3000); tap(pg, 150, 812); pg.wait_for_timeout(1800); pg.evaluate(BAS); pg.wait_for_timeout(800)
        ref = pg.evaluate(STYLE, '#detailPoster .v16-danger .s2-lab')
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(800)
        # un Cercle créé au +, avec sa première parole
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{ const n=document.getElementById('nName'), f=document.getElementById('nFirst'), b=document.getElementById('addNuee'); n.value='le potager'; if(f) f.value='semer les radis'; b.click(); }"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(900)
        def ouvre_cercle():
            h = pg.evaluate(HIT, 'nuee')
            if not h: return False
            tap(pg, h[0], h[1]); pg.wait_for_timeout(3800); return True
        juge('[%s] la dalle du Cercle est sur la Toile de l\'accueil, et la toucher ouvre sa fiche' % th, ouvre_cercle() and 'show' in pg.evaluate("()=>document.getElementById('detailPoster').className"))
        c = pg.evaluate(COTES)
        if '--planche' in sys.argv: capture(pg, 'planche-v142/cercle-%s-%s-court.png' % (F.replace('.html', ''), th))
        juge('[%s] fil court (une parole) : le bandeau Peaufiner est tout en bas (760 → 844)' % th, c['bandeau'] and pres(c['bandeau'][0], 760) and pres(c['bandeau'][1], 844), 'bandeau %s' % (c['bandeau'] and [round(v, 1) for v in c['bandeau']]))
        juge('[%s] fil court : « + Planter dans le Cercle » est 12 pt au-dessus du bandeau' % th, c['bouton'] and c['bandeau'] and pres(c['bandeau'][0] - c['bouton'][1], 12), 'bouton %s' % (c['bouton'] and [round(v, 1) for v in c['bouton']]))
        # un fil LONG : six paroles de plus, plantées depuis la fiche
        for t in ['arroser les tomates', 'tailler la haie', 'pailler les fraisiers', 'récolter les courgettes', 'semer les fèves', 'ranger la serre']:
            pg.evaluate("()=>{ const b=document.getElementById('nfAdd'); b&&b.click(); }"); pg.wait_for_timeout(1500)
            pg.evaluate("a=>{document.getElementById('fTitle').value=a;window._csEnLair=true;window._csDueISO=null;document.getElementById('addPromi').click()}", t); pg.wait_for_timeout(2600)
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(500)
            ouvre_cercle()
        c = pg.evaluate(COTES)
        if '--planche' in sys.argv: capture(pg, 'planche-v142/cercle-%s-%s-long.png' % (F.replace('.html', ''), th))
        juge('[%s] fil long (%d paroles) : le bandeau est tout en bas (760 → 844)' % (th, c['n']), c['n'] >= 5 and c['bandeau'] and pres(c['bandeau'][0], 760) and pres(c['bandeau'][1], 844), 'bandeau %s' % (c['bandeau'] and [round(v, 1) for v in c['bandeau']]))
        juge('[%s] fil long : le bouton est 12 pt au-dessus du bandeau, et des cartes passent dessous' % th, c['bouton'] and pres(c['bandeau'][0] - c['bouton'][1], 12) and any(k and k[1] > c['bouton'][1] for k in c['cartes']), 'bouton %s' % (c['bouton'] and [round(v, 1) for v in c['bouton']]))
        # le fil défilé de 260 pt : le bandeau et le bouton ne bougent pas
        defile(pg, '#detailPoster', 260); pg.wait_for_timeout(1200)
        d = pg.evaluate(COTES)
        if '--planche' in sys.argv: capture(pg, 'planche-v142/cercle-%s-%s-defile.png' % (F.replace('.html', ''), th))
        juge('[%s] le fil défilé : le bandeau reste à 760 → 844 et le bouton 12 pt au-dessus' % th, d['bandeau'] and pres(d['bandeau'][0], 760) and pres(d['bandeau'][1], 844) and d['bouton'] and pres(d['bandeau'][0] - d['bouton'][1], 12), 'défilement %s · bandeau %s · bouton %s' % (d['scroll'], d['bandeau'] and [round(v, 1) for v in d['bandeau']], d['bouton'] and [round(v, 1) for v in d['bouton']]))
        # « Dissoudre le Cercle » : le dessin de « Supprimer ce Promi »
        tap(pg, 150, 802); pg.wait_for_timeout(2200); pg.evaluate(BAS); pg.wait_for_timeout(1000)
        ds = pg.evaluate(STYLE, '#npDiss .np-lab')
        if '--planche' in sys.argv: capture(pg, 'planche-v142/cercle-%s-%s-dissoudre.png' % (F.replace('.html', ''), th))
        juge('[%s] « Dissoudre le Cercle » n\'a ni contour ni fond' % th, ds and not ds['contourVisible'] and not ds['fondVisible'], str(ds and (ds['contourVisible'], ds['fondVisible'])))
        cles = ('taille', 'graisse', 'chasse', 'casse', 'police', 'couleur', 'corbeille')
        juge('[%s] « Dissoudre le Cercle » a le dessin de « Supprimer ce Promi » (police, taille, graisse, chasse, casse, couleur, corbeille), centré' % th,
             ds and ref and all(ds[k] == ref[k] for k in cles) and abs(ds['centre'] - ref['centre']) <= 8 and ds['texte'] == 'DISSOUDRE LE CERCLE',
             'écarts : %s' % (ds and ref and {k: (ds[k], ref[k]) for k in cles + ('centre',) if ds[k] != ref[k]}))
        if pg.erreurs: juge('[%s] aucune erreur de page' % th, False, str(pg.erreurs[:2]))
        ctx.close()
    b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
