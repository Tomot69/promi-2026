#!/usr/bin/env python3
"""
redteam_bandeau.py — v175a (Tom, 1er nov. 2026, C-218) : PAGE + : AUCUN BANDEAU AUTOUR DU TRAIT VIDE.

« Page + du Promi, du Chiche et du Cercle : un bandeau horizontal parasite, de deux couleurs, au-dessus ou en dessous du trait vide. »
La cause : un passage en flaques 'couvre' reste à l'écran une fois fini ; à la plantation le retrait de l'invite partait, la page se fermait, `cache()` changeait le numéro
de la passe et les deux calques restaient dans la page +, pour toutes les ouvertures suivantes.

Banc comme Tom (WebKit, doigt), après une VRAIE plantation tracée au doigt (sans elle le défaut n'existe pas), pour chaque nature × thème × échelle (1 : 430 × 932 ; 0,79 : 330 × 714) :
  à chaque étape posée — ouverture, saisie (un champ ouvert), naissance du trait, retrait (la phrase effacée), réouverture —
  A · aucun calque de passage ne reste dans la page + (lu dans le DOM) ;
  B · sur l'IMAGE, de part et d'autre de la vague : au-dessus, le champ de la nature ; en dessous, le corps de la nature (colonne par colonne, hors dalle et hors éléments attendus).
Couleurs en dur : champs #82AEF8 · #FFB8D2 · #C9A8F5 ; corps #0E78F2 · #7C3F58 · #5D4978.
Rouge sur v174 (`git show aeeb479:app.html > zz-v174b.html` ; `--fichier=zz-v174b.html`). Safari iOS : voir le rapport du lot.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
CHAMP = {'promi': (0x82, 0xAE, 0xF8), 'chiche': (0xFF, 0xB8, 0xD2), 'nuee': (0xC9, 0xA8, 0xF5)}
CORPS = {'promi': (0x0E, 0x78, 0xF2), 'chiche': (0x7C, 0x3F, 0x58), 'nuee': (0x5D, 0x49, 0x78)}
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
CALQUES = "()=>[...document.querySelectorAll('#createSheet canvas.passage-flaques')].filter(c=>c.dataset.mode==='couvre'||+c.dataset.u>=1).map(c=>[c.style.top,c.style.height,c.dataset.u])"
def ouvre_nature(pg, k):
    pg.evaluate("()=>{ try{window._peaufSortie&&_peaufSortie();closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(750); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k)
    for _ in range(50):
        pg.wait_for_timeout(120)
        if pg.evaluate("k=>{var s=document.getElementById('createSheet');return !!(s&&s.classList.contains('pp-'+k)&&!s.classList.contains('pp-choix')&&!s.classList.contains('acc-passe'))}", k): break
    pg.wait_for_timeout(1400)
def remplit(pg, k, txt):
    pg.evaluate("a=>{const f=document.getElementById(a[0]==='nuee'?'nName':'fTitle');f.value=a[1];f.dispatchEvent(new Event('input',{bubbles:true}));if(window._ppTout)_ppTout()}", [k, txt])
def attend(pg, vrai, ms=6000):
    for _ in range(int(ms / 100)):
        if pg.evaluate("v=>{const e=window._ppInvite.etat();return e.visible===v&&!e.sortie&&!e.descend}", vrai): return True
        pg.wait_for_timeout(100)
    return False
def trace(pg):
    g = pg.evaluate("()=>{const e=_ppEcran(),y=_onde.onde(e.base,e.amp);return [50,100,150,195,235].map(x=>[x,y(x)])}")
    B.glisse(pg, g, pas=18, tenue=380)
def lit(pg, k, invite):
    """colonne par colonne : au-dessus de la vague le champ, en dessous le corps ; on saute la dalle (au-dessus) en ne gardant que l'étroite bande sous elle si elle descend,
    et ce qu'on attend près du trait quand il est là"""
    z = pg.evaluate("""()=>{const e=_ppEcran(),y=_onde.onde(e.base,e.amp),c=document.getElementById('createSheet'),D=c.getBoundingClientRect(),K=D.width/(c.offsetWidth||390);
      const T=document.querySelector('#createSheet .pp-trace'),r=T?T.getBoundingClientRect():null;
      const ph=document.getElementById(e.nat==='nuee'?'nueePhrase':'csPhrase'),hs=[...ph.querySelectorAll('.ph-txt > .ph-m, .ph-txt > .ph-b')].map(n=>n.getBoundingClientRect()).filter(q=>q.width).map(q=>(q.top-D.top)/K);
      const d=document.getElementById('csTrameCv').getAttribute('data-matiere');
      const fig=[...document.querySelectorAll('#createSheet .pp-photo,#createSheet [id*=hotoBtn]')].map(n=>n.getBoundingClientRect()).filter(q=>q.width).map(q=>[(q.left-D.left)/K,(q.top-D.top)/K,(q.right-D.left)/K,(q.bottom-D.top)/K]);
      return {w:[...Array(79)].map((_,i)=>y(i*5)), ph:hs.length?Math.min(...hs):844, lib:r&&r.width?[(r.left-D.left)/K,(r.top-D.top)/K,(r.right-D.left)/K,(r.bottom-D.top)/K]:null, base:e.base, ouvert:!!e.ouvert};}""")
    im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); ex = im.width / 390.0
    def px(x, y):
        return im.getpixel((min(im.width - 1, max(0, int(x * ex))), min(im.height - 1, max(0, int(y * ex)))))
    pres = lambda p, q, t=26: abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2]) < t
    faux = []
    marge = 15 if invite else 4
    for i, y in enumerate(z['w']):
        x = i * 5
        if not 8 <= x <= 382: continue
        if invite and x < 100: continue            # le départ, la pointe, la flèche d'invite
        for dy in (marge + 3, marge + 9):           # au-dessus de la vague : le champ (la dalle s'arrête plus haut, le bouton photo est exclu)
            p = px(x, y - dy)
            if 300 < x and y - dy > 150 and not pres(p, CHAMP[k]) and x > 320: continue
            if not pres(p, CHAMP[k]) and not (120 < x < 300): faux.append(('champ', x, round(y - dy), p))
        for dy in (marge + 3, marge + 7):           # en dessous de la vague : le corps
            yy = y + dy
            if yy >= z['ph'] - 2: continue
            if z['lib'] and z['lib'][0] - 4 <= x <= z['lib'][2] + 4 and z['lib'][1] - 4 <= yy <= z['lib'][3] + 4: continue
            if not pres(px(x, yy), CORPS[k]): faux.append(('corps', x, round(yy), px(x, yy)))
    return faux
def un(b, k, sombre, vw, vh, nom):
    T = '[%s · %s · %s]' % (k, 'sombre' if sombre else 'clair', nom)
    ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
    # la plantation tracée au doigt : c'est elle qui laissait les calques
    ouvre_nature(pg, 'promi'); remplit(pg, 'promi', 'courir un marathon'); attend(pg, True); trace(pg); pg.wait_for_timeout(3400)
    juge(T + ' après une plantation tracée : aucun calque ne reste', not pg.evaluate(CALQUES), pg.evaluate(CALQUES))
    ouvre_nature(pg, k)
    f = lit(pg, k, False); c = pg.evaluate(CALQUES)
    juge(T + ' OUVERTURE : aucun calque, le champ et le corps seuls autour de la vague', not c and not f, (c, f[:3]))
    remplit(pg, k, 'manger des radis'); attend(pg, True); pg.wait_for_timeout(1100)
    f = lit(pg, k, True); c = pg.evaluate(CALQUES)
    juge(T + ' TRAIT NÉ : aucun calque, rien de plus que le trait', not c and not f, (c, f[:3]))
    remplit(pg, k, ''); attend(pg, False); pg.wait_for_timeout(900)
    f = lit(pg, k, False); c = pg.evaluate(CALQUES)
    juge(T + ' RETRAIT : aucun calque, le champ et le corps seuls', not c and not f, (c, f[:3]))
    # le retrait coupé par la fermeture : le chemin court
    remplit(pg, k, 'manger des radis'); attend(pg, True); pg.wait_for_timeout(800); remplit(pg, k, ''); pg.wait_for_timeout(120)
    pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(500)
    ouvre_nature(pg, k)
    f = lit(pg, k, False); c = pg.evaluate(CALQUES)
    juge(T + ' FERMÉE PENDANT LE RETRAIT puis rouverte : rien ne reste', not c and not f, (c, f[:3]))
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for k in ('promi', 'chiche', 'nuee'):
            for s in ((False,) if VITE else (False, True)):
                try: un(b, k, s, vw, vh, nom)
                except Exception as e: juge('[%s %s %s] le chemin va au bout' % (k, s, nom), False, str(e)[:160])
    b.close()
print('  %s  %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res)))
