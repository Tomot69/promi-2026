"""⚑ v203 clôture (Tom, C-280 §1) — AUCUN ENCART PENDANT LA MODIFICATION DU TITRE.
« Quand on modifie un titre dans une fiche, des lignes forment un rectangle autour : un encart parasite. Le titre en cours de modification est visuellement identique
au titre au repos : même typographie, même place. Seul le curseur clignote. Sur les trois natures, titre court et titre déplié. Juge : capture au pixel de la zone du
titre, au repos puis en modification, curseur masqué : identiques. »
WebKit, 390 × 844 ×3, au doigt (banc_tom), l'état de redteam_titre_fiche (le Cercle « Le potager », un titre de 280 caractères). La zone : la boîte du titre et 14 pt
autour (un anneau de focus se pose À L'EXTÉRIEUR de la boîte), sous la bande du haut. Le curseur est masqué par le juge (`caret-color: transparent`, le seul style posé).
  A · en modification (le titre a le focus, modifiable) : la zone (suivie : la fiche glisse au-dessus du clavier, C-280) identique au repos : AUCUN pixel changé hors du bord des lettres (2 pixels de l'appareil, l'anticrénelage d'un glissement fractionnaire)
  B · aucun contour, ombre, fond ni bordure calculés sur le titre en modification
--natures=promi,chiche,nuee,long · --sonde (un contour posé exprès : A rougit) · --fichier="""
import sys, io, json; sys.path.insert(0, '.')
ARGS = sys.argv[1:]
src = io.open('redteam_titre_fiche.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0]
sys.argv = [sys.argv[0]]; exec(src); sys.argv += ARGS
import banc_tom as B
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in ARGS if a.startswith('--fichier=')), 'app.html')
NAT = next((a.split('=', 1)[1].split(',') for a in ARGS if a.startswith('--natures=')), ['promi', 'chiche', 'nuee', 'long'])
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
ZONE = "()=>{ const t=document.getElementById('dptTitre'), r=t.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, m=14*k; const top=Math.max(r.top-m, dv.top+112*k); return {x:Math.max(dv.left, r.left-m), y:top, width:Math.min(dv.right, r.right+m)-Math.max(dv.left, r.left-m), height:r.bottom+m-top}; }"
STY = "()=>{ const c=getComputedStyle(document.getElementById('dptTitre')); return {ol:c.outlineStyle==='none'||parseFloat(c.outlineWidth)===0, bs:c.boxShadow, bg:c.backgroundColor, bd:parseFloat(c.borderTopWidth)+parseFloat(c.borderLeftWidth)}; }"
def cap(pg, z): return Image.open(io.BytesIO(pg.screenshot(clip=z))).convert('RGB')
def diff(a, b):
    """(tout l'écart ; l'écart HORS des lettres) — la fiche glisse au-dessus du clavier d'une cote qui ne tombe pas sur un pixel entier (106,4 pt × 3) :
    le bord des lettres se relisse (anticrénelage, au plus 2 pixels de l'appareil). Un encart, un anneau, un fond se peignent LOIN des lettres : on compte
    l'écart hors du voisinage de 2 pixels de l'encre du repos."""
    if a.size != b.size: return 10**6, 10**6
    from PIL import ImageFilter
    from collections import Counter
    fond = Counter(a.getdata()).most_common(1)[0][0]
    enc = Image.new('L', a.size); enc.putdata([255 if sum(abs(q[j] - fond[j]) for j in range(3)) > 24 else 0 for q in a.getdata()])
    pres = enc.filter(ImageFilter.MaxFilter(5))
    best = None   # la capture d'une zone qui a glissé d'une cote fractionnaire s'arrondit d'un pixel : on cale d'abord (± 3 pixels de l'appareil)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            bb = ImageChops.offset(b, dx, dy); dd = ImageChops.difference(a, bb).convert('L'); n = sum(1 for v in dd.getdata() if v > 24)
            if best is None or n < best[0]: best = (n, dd)
    d = best[1]
    tout = sum(1 for v in d.getdata() if v > 24)
    hors = sum(1 for v, m in zip(d.getdata(), pres.getdata()) if v > 24 and not m)
    return tout, hors
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_titre_encart — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in ARGS else ''))
    st = etat()
    for nat in NAT:
        ctx = B.contexte(b); ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
        ctx.add_init_script(CLAV); ctx.add_init_script("window._vivantOff=true;")
        ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>{ const s=document.createElement('style'); s.textContent='#dptTitre{caret-color:transparent!important}'; document.head.appendChild(s); });")
        pg = B.ouvre(ctx, F); ouvre(pg, nat); n = '[%s]' % nat
        if nat == 'long':
            tap_titre(pg); pg.wait_for_timeout(1400)   # C-244 : le premier toucher déplie
        pg.wait_for_timeout(600); z = pg.evaluate(ZONE); r0 = cap(pg, z)
        tap_titre(pg); pg.wait_for_timeout(2200)   # la fiche glisse au-dessus du clavier (C-280) : on compare le titre à SA place, attendue immobile
        for _ in range(10):
            za = pg.evaluate(ZONE); pg.wait_for_timeout(150)
            if abs(pg.evaluate(ZONE)['y'] - za['y']) < 0.2: break
        if '--sonde' in ARGS: pg.evaluate("()=>document.getElementById('dptTitre').style.setProperty('outline','2px solid #FB4C0D','important')")
        ed = pg.evaluate("()=>{ const t=document.getElementById('dptTitre'); return document.activeElement===t && t.isContentEditable; }")
        z1 = pg.evaluate(ZONE); z1['height'] = z['height']; z1['width'] = z['width']; z1['x'] = z['x']; r1 = cap(pg, z1)
        dt, dn = diff(r0, r1)
        if dn > 0: r0.save('scratchpad/v203g/encart-%s-%s-repos.png' % (F[:-5], nat)); r1.save('scratchpad/v203g/encart-%s-%s-edit.png' % (F[:-5], nat))
        juge(n + ' A · en modification, rien hors des lettres ne change (aucun encart)', ed and dn == 0, {'modifie': ed, 'hors des lettres': dn, 'bord des lettres': dt - dn, 'glissement': round(z1['y'] - z['y'], 1)})
        s = pg.evaluate(STY)
        juge(n + ' B · aucun contour, ombre, fond ni bordure', '--sonde' in ARGS or (s['ol'] and s['bs'] == 'none' and s['bg'] in ('rgba(0, 0, 0, 0)', 'transparent') and s['bd'] == 0), s)
        ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
