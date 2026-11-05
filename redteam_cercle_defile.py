#!/usr/bin/env python3
"""redteam_cercle_defile.py — ⚑ v180b (Tom, C-238) : « le fil d'un Cercle ne défile pas vers le bas : on ne voit ni ses commentaires, ni ses Promi et Chiche ».

Banc WebKit ×3, le Cercle « Le potager » (six paroles, trois mots), fenêtres 430 × 932 (échelle 1), 390 × 844 (0,933) et 330 × 714 (0,79) :
  A · le geste qui fait défiler (le doigt qui monte, 250 pt) ne déplie pas le Peaufiner du Cercle (§13 : il ne s'ouvre qu'en touchant sa barre) ;
  B · défilé jusqu'en bas : la dernière carte est entière et touchable, au-dessus du bloc collant (elementFromPoint à son bas) ; le Peaufiner reste fermé ;
  C · le bloc collant est plein : dans ses interstices (sous le dernier mot, entre « Un mot… » et « + Planter », sous le bouton jusqu'au bandeau), aucune carte ;
  D · les mots ouverts (« Un mot… » touché) : entre le fil des mots et la ligne, aucune carte ;
  E · la ligne « Un mot… » et le dernier mot ont le style de ceux d'une fiche Promi (police, taille, graisse).
Rouge sur v179b (`--fichier=zz-v179b.html`).
"""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B, io as _io
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
MOTS = json.dumps({'potager': [{'t': 'On sème les radis samedi ?', 'd': '2026-11-03T09:00:00Z', 'by': 'Rachel'}, {'t': 'Oui, je ramène les graines.', 'd': '2026-11-03T10:00:00Z', 'by': 'moi'}, {'t': 'Parfait, à samedi alors.', 'd': '2026-11-04T08:00:00Z', 'by': 'Marion'}]})
PEAUF = "()=>({dd:document.getElementById('dpDetails').classList.contains('ouvert'), s2:document.getElementById('detailPoster').classList.contains('s2-ouv')})"
CARTE_A = """(pts)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return pts.map(p=>{ const e=document.elementFromPoint(D.left+p[0]*k, D.top+p[1]*k); return !!(e && e.closest && e.closest('#dpNueeFil .nf-liste')); }); }"""
GEO = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, Y=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return r.height?[(r.top-D.top)/k,(r.bottom-D.top)/k]:null; };
  const cartes=[...document.querySelectorAll('#dpNueeFil .nf-liste > *')].filter(c=>c.getBoundingClientRect().height>20);
  return {der:Y(document.getElementById('cm5Dernier')), ligne:Y(document.getElementById('cm5Ligne')), btn:Y(document.getElementById('nfAdd')), fil:Y(document.getElementById('cm5Fil')), last:Y(cartes[cartes.length-1]), n:cartes.length}; }"""
STYLE = """()=>{ const s=e=>{ if(!e) return null; const t=e.querySelector('*')||e; const c=getComputedStyle(t); return [c.fontFamily.split(',')[0], c.fontSize, c.fontWeight]; }; return {ligne:s(document.getElementById('cm5Ligne')), der:s(document.getElementById('cm5Dernier'))}; }"""
def uni(pg, ys):
    """chaque rangée y (pt de l'appareil), de x 30 à 360, est d'une seule couleur (la carte qui passerait dessous y mettrait son texte ou sa dalle) — lu sur l'image"""
    D = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.width/390]; }")
    corps = pg.evaluate("()=>{ const v=(getComputedStyle(document.getElementById('detailPoster')).getPropertyValue('--nf-corps')||'#5D4978').trim(); const c=document.createElement('canvas').getContext('2d'); c.fillStyle=v; const h=c.fillStyle; return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)]; }")
    im = Image.open(_io.BytesIO(pg.screenshot())).convert('RGB'); sx = im.width / pg.viewport_size['width']; out = []
    for y in ys:
        px = [im.getpixel((int((D[0] + x * D[2]) * sx), int((D[1] + y * D[2]) * sx))) for x in range(30, 361, 3)]
        med = [sorted(c[i] for c in px)[len(px) // 2] for i in range(3)]
        dev = max(max(abs(c[i] - med[i]) for i in range(3)) for c in px)
        out.append((round(y, 1), dev, max(abs(med[i] - corps[i]) for i in range(3))))
    return out
def bas(pg):
    for _ in range(6):
        pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.scrollTop=d.scrollHeight; }"); pg.wait_for_timeout(450)
with sync_playwright() as p:
    b = p.webkit.launch(); ref = None
    for vw, vh, nom in ((430, 932, '1'), (390, 844, '0,933'), (330, 714, '0,79')):
        T = '[×%s]' % nom
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); ctx.add_init_script("localStorage.setItem('promi_cercle_mots', %s)" % json.dumps(MOTS))
        pg = B.ouvre(ctx, F)
        if ref is None:
            pg.evaluate("()=>{ const q=promises.find(x=>x.title==='rendre le livre'); q.comments=JSON.parse(localStorage.getItem('promi_cercle_mots')).potager; closeAll(); openDetail(q.id); }"); pg.wait_for_timeout(2600)
            ref = pg.evaluate(STYLE); pg.evaluate("()=>{ try{_peaufSortie()}catch(e){} closeAll(); }"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(2600)
        B.glisse(pg, B.droite([200, 620], [200, 370], 12), pas=20); pg.wait_for_timeout(1200)
        juge(T + ' A · le doigt qui monte ne déplie pas le Peaufiner du Cercle', not any(pg.evaluate(PEAUF).values()), pg.evaluate(PEAUF))
        pg.evaluate("()=>{ document.getElementById('dpDetails').classList.remove('ouvert'); }")
        bas(pg); g = pg.evaluate(GEO); pf = pg.evaluate(PEAUF)
        haut_bloc = min(x[0] for x in (g['der'], g['ligne'], g['btn']) if x)
        vu = g['last'] and pg.evaluate(CARTE_A, [[100, g['last'][1] - 6], [300, g['last'][1] - 6]])
        juge(T + ' B · défilé jusqu\'en bas : la dernière carte entière, touchable, au-dessus du bloc ; Peaufiner fermé', g['last'] and g['last'][1] <= haut_bloc - 4 and all(vu) and not any(pf.values()), (g, pf))
        trous = []
        if g['der'] and g['ligne']: trous.append((g['der'][1] + g['ligne'][0]) / 2)
        if g['ligne'] and g['btn']: trous.append((g['ligne'][1] + g['btn'][0]) / 2)
        if g['btn']: trous += [g['btn'][1] + 4, g['btn'][1] + 9]
        u = uni(pg, trous)
        juge(T + ' C · le bloc collant est plein : aucune carte dans ses interstices (lu sur l\'image)', trous and all(d <= 14 and e <= 14 for _, d, e in u), u)
        pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.scrollTop=0; }"); pg.wait_for_timeout(600)
        c = pg.evaluate("()=>{ const l=document.getElementById('cm5Ligne'); const r=l.getBoundingClientRect(); return [r.left+40, r.top+r.height/2]; }")
        pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(900); g2 = pg.evaluate(GEO)
        u = uni(pg, [g2['fil'][1] + 3, (g2['fil'][1] + g2['ligne'][0]) / 2]) if g2['fil'] and g2['ligne'] else None
        juge(T + ' D · les mots ouverts : aucune carte entre leur fil et la ligne (lu sur l\'image)', u and all(d <= 14 and e <= 14 for _, d, e in u), (u, g2['fil'], g2['ligne']))
        pg.evaluate("()=>{ try{ window._comm.ferme(); }catch(e){} }"); pg.wait_for_timeout(400)
        st = pg.evaluate(STYLE)
        juge(T + ' E · « Un mot… » et le dernier mot au style d\'une fiche Promi', st == ref, (st, ref))
        juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
