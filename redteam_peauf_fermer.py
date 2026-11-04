#!/usr/bin/env python3
"""
redteam_peauf_fermer.py — PEAUFINER SE REFERME, SUR LES TROIS FICHES, PAR LES TROIS MOYENS (v177b, Tom, 4 nov. 2026 — C-228).
« Dans la FICHE d'un Cercle, quand Peaufiner s'ouvre, il reste bloqué : impossible de le refermer (ni le X, ni le glissement vers le bas,
  ni la barre). […] Vérifie aussi les fiches de Promi et de Chiche. Juge : Peaufiner s'ouvre puis se referme par chacun des trois moyens,
  sur les trois fiches. Il doit rougir sur v177a. »
Banc comme Tom (banc_tom : WebKit, 390 × 844 ×3, au doigt). Promi et Chiche plantés par l'app, un Cercle créé au +.
Pour chaque fiche (Promi, Chiche, Cercle) et chaque moyen (le X, la barre, le glissement vers le bas depuis le titre de Peaufiner) :
  ① la barre touchée ouvre Peaufiner ;
  ② le moyen le referme ;
  ③ il RESTE fermé : 2,5 s plus tard, et après une nouvelle pose de la fiche (`_ficheTout`, ce que l'app fait à chaque rendu) — la cause de
     C-228 : l'état « ouvert » d'un Cercle vivait aussi dans `#dpDetails.ouvert`, que la pose relisait et rouvrait.
  ④ la fiche est rendue telle qu'avant l'ouverture (l'image au-dessus de la barre, ≤ 2 % de pixels écartés — la dalle et les anneaux respirent) :
     refermé, le Peaufiner d'un Cercle laissait la fiche vide (le champ, le titre, le fil masqués, « Planter » à y −44 ; pris par `redteam_nuee`).
Preuve (§7) : `--fichier=zz-v177a.html` — rouge (la barre et le glissement sur un Cercle ; la pose rouvre après le X).
⚑ v178a (Tom, C-228 récidive : « tout buggé, des chevauchements en haut ») : ce juge forçait une pose de la fiche AVANT de comparer l'image — et c'est
la pose qui repliait le Peaufiner. Refermé par le X, le Peaufiner d'un Cercle restait affiché par-dessus la fiche (son titre sur le plateau « CERCLE »,
le bouton photo sur LE TRAIT) jusqu'à la pose suivante : le juge ne pouvait pas le voir. ⑤ l'image est lue JUSTE APRÈS la fermeture, sans rien forcer ;
⑥ aucun recouvrement : Peaufiner ouvert, aucun élément de la fiche (plateau, titre, anneaux, bouton photo) ne se voit ; refermé, aucun élément du
Peaufiner ; ⑦ aux échelles 1 (430 × 932) et 0,79 (330 × 714). Rouge sur v177b (`--fichier=zz-v177b.html`).
"""
import sys; sys.path.insert(0, '.')
import io
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
def img(pg):
    im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); k = im.width / 390.0
    return im.crop((0, 0, im.width, int(740 * k)))
def ecart(a, b):
    d = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > 30 else 0)
    return sum(1 for v in d.getdata() if v) / float(a.width * a.height)
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VUS = """(ouv)=>{const vis=e=>{if(!e)return false;const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return false;
  for(let q=e;q&&q.nodeType===1;q=q.parentElement){const c=getComputedStyle(q);if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05)return false}return true};
  const fiche=['#dptNat','#dptTitre','#dAura','#dptQui','#detailPoster .ph-photo-btn'], peauf=['#npTete','#npNom','#npFermer','#detailPoster .np-carte','#detailPoster .s2-liste'];
  const L=(ouv?fiche:peauf).flatMap(s=>[...document.querySelectorAll(s)]).filter(vis).map(e=>e.id||String(e.className).slice(0,24));
  return L;}"""
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-100s %s' % ('✅' if c else '❌', nom, str(d)[:200]), flush=True)
OUV = "()=>{const dp=document.getElementById('detailPoster');return dp.classList.contains('show')&&dp.classList.contains('s2-ouv')}"
VUE = "()=>document.getElementById('detailPoster').classList.contains('show')"
POS = """(s)=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;
  for(const e of document.querySelectorAll(s)){ const r=e.getBoundingClientRect(); if(r.width<4||r.height<4) continue;
    const cs=getComputedStyle(e); if(cs.visibility!=='visible') continue;
    const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); if(!h||!(e===h||e.contains(h)||h.contains(e)||(e.parentNode&&e.parentNode.contains(h)))) continue;
    return [(r.left+r.width/2-D.left)/k,(r.top+r.height/2-D.top)/k]; } return null; }"""
XG = """()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390, fer='#npFermer, .s2-fermer, .closeb, [data-close]';
  for(const e of document.querySelectorAll('#detailPoster .x157-g')){ const r=e.getBoundingClientRect(); if(r.width<4) continue; let ok=true;
    for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05){ok=false;break;} } if(!ok) continue;
    const rg=document.createRange(); rg.selectNodeContents(e); const t=rg.getBoundingClientRect(); const cx=t.left+t.width/2, cy=t.top+t.height/2;
    const h=document.elementFromPoint(cx,cy); if(!h) continue; const z=h.closest&&h.closest(fer);
    if(!(e.contains(h)||h.contains(e)||(z&&z.contains(e)))) continue;
    return [(cx-D.left)/k,(cy-D.top)/k, !!(z&&z.contains(e)), z?(z.id||z.className):(h.id||h.className)+'']; } return null; }"""
def barre(pg):
    b = pg.evaluate(POS, '#dpDetails .dpd-tog'); B.tap(pg, 120, b[1] if b else 802); pg.wait_for_timeout(1300)
def ouvre_fiche(pg, nat, cle):
    if nat == 'cercle': pg.evaluate("(k)=>{closeAll();openNueeDetail(k)}", cle)
    else: pg.evaluate("(t)=>{closeAll();const q=promises.filter(q=>q.title===t)[0];openDetail(q.id)}", cle)
    pg.wait_for_timeout(2600)
def passe(b, ech):
    vw, vh = (430, 932) if ech == 1 else (330, 714)
    ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
    B.plante(pg, 'boire un verre', nature=0); B.plante(pg, 'courir le marathon', 'Rachel', nature=1)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const n=document.getElementById('nName'), f=document.getElementById('nFirst'), b=document.getElementById('addNuee'); n.value='le potager'; if(f) f.value='semer les radis'; b.click(); }"); pg.wait_for_timeout(3500)
    pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(900)
    cle = pg.evaluate("()=>Object.keys(NUE).find(k=>NUE[k]==='le potager')")
    chiche = pg.evaluate("()=>{const q=promises.filter(q=>q.title==='courir le marathon')[0]; return q?!!(q.chiche||q.kind==='chiche'):null}")
    print('— échelle %s — Cercle %s · Chiche planté : %s' % (ech, cle, chiche))
    for nat, c in (('promi', 'boire un verre'), ('chiche', 'courir le marathon'), ('cercle', cle)):
        print('── la fiche %s' % nat)
        ouvre_fiche(pg, nat, c)
        for moyen in ('X', 'barre', 'glissement'):
            if not pg.evaluate(VUE): ouvre_fiche(pg, nat, c)
            pg.wait_for_timeout(600); avant = img(pg)
            barre(pg); o = pg.evaluate(OUV)
            if not o: barre(pg); o = pg.evaluate(OUV)
            juge('[%s · %s] la barre ouvre Peaufiner' % (nat, moyen), o)
            if moyen == 'X':
                v = pg.evaluate(VUS, True)
                juge('[%s · %s · %s] Peaufiner ouvert : aucun élément de la fiche ne se voit dessous' % (nat, moyen, ech), not v, v)
            if moyen == 'X':
                pg.wait_for_timeout(900)
                x = pg.evaluate(XG)   # le centre de l'ENCRE du X qu'on voit — là où le doigt se pose
                juge('[%s · X] le X se voit, et son centre est dans sa zone de toucher' % nat, x and x[2], x)
                if x: B.tap(pg, x[0], x[1])
            elif moyen == 'barre':
                barre(pg)
            else:
                pg.evaluate("()=>{const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=0}"); pg.wait_for_timeout(300)
                t = pg.evaluate(POS, '#detailPoster .s2-titre') or [120, 60]
                B.glisse(pg, B.droite([120, t[1]], [120, t[1] + 300], 16), pas=16)
            pg.wait_for_timeout(1300); f1 = not pg.evaluate(OUV) and pg.evaluate(VUE)
            juge('[%s · %s] le %s referme Peaufiner, la fiche reste' % (nat, moyen, moyen), f1)
            v = pg.evaluate(VUS, False)
            juge('[%s · %s · %s] refermé : aucun élément du Peaufiner ne reste (sans forcer de pose)' % (nat, moyen, ech), f1 and not v, v)
            e0 = ecart(avant, img(pg))
            juge('[%s · %s · %s] refermé : la fiche telle qu\'avant, lue juste après la fermeture (≤ 2 %%)' % (nat, moyen, ech), f1 and e0 <= 0.02, '%.2f %%' % (100 * e0))
            pg.wait_for_timeout(1200); pg.evaluate("()=>{try{(window._ficheTout||window._ficheNuee)()}catch(e){}}"); pg.wait_for_timeout(1200)
            juge('[%s · %s] il reste fermé (2,5 s, puis une nouvelle pose de la fiche)' % (nat, moyen), f1 and not pg.evaluate(OUV))
            e = ecart(avant, img(pg))
            juge('[%s · %s] la fiche est rendue telle qu\'avant l\'ouverture (≤ 2 %% de pixels écartés)' % (nat, moyen), f1 and e <= 0.02, '%.2f %%' % (100 * e))
            if pg.evaluate(OUV): pg.evaluate("()=>{try{window._s2Ouvre(false)}catch(e){}}"); pg.wait_for_timeout(400)
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for ech in (1, 0.79): passe(b, ech)
    b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res)))
sys.exit(0 if all(res) else 1)
