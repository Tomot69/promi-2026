"""⚑ v203 clôture (Tom, C-281) — LES LETTRES QUI CLIGNOTENT : LE BLEU CLAIR VRAI DE LA PALETTE DE BASE.
« Le I de PROMI à l'accueil, le R de PARTAGER, le S de RÉGLAGES, et partout dès l'onboarding pour PROMI : ces lettres clignotent dans le bleu clair EXACT de la
palette de base, vif, jamais terne. Au sommet du clignotement, la couleur exacte, à pleine opacité : aucun filtre, aucun mode de fusion, aucune opacité qui ternit.
Le même code de clignotement partout (C-247). Juge : valeur des pixels de chaque lettre au sommet du clignotement, égale à la couleur de la palette à 1,5 près,
sur les deux thèmes, dès l'onboarding. »
La couleur est écrite EN DUR (#82AEF8, la palette de base Ingénu, `PALS.signal.cols[0]` du moteur) et le juge vérifie AUSSI que le moteur la déclare.
WebKit, 390 × 844 ×3. Pour chaque thème : l'onboarding (stockage vierge, la page du prénom), l'accueil, Partager, Réglages. La lettre est mise au SOMMET de son
clignotement (son animation `promiBlink` arrêtée à 0 ms : opacité 1, la valeur de la règle), puis lue sur l'image :
  A · le cœur de la lettre (la couleur la plus fréquente de son encre) = #82AEF8 à 1,5 près, sur chaque canal
  B · son animation est `promiBlink` 1,15 s steps(1,end) (le même code partout), et rien sur elle ni ses ancêtres ne ternit (opacité 1, aucun filtre, aucune fusion)
Aura (apostrophe) : v211, C-308. --sonde (la lettre de l'accueil ternie à 0,9 : A rougit) · --fichier="""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from collections import Counter
from PIL import Image
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
BLEU = (0x82, 0xAE, 0xF8)
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
SOMMET = r"""(sel)=>{ const e=[...document.querySelectorAll(sel)].find(x=>{ const r=x.getBoundingClientRect(), c=getComputedStyle(x); return r.width>0 && c.visibility!=='hidden' && r.top>=0 && r.bottom<=innerHeight; }); if(!e) return null;
  const a=(e.getAnimations?e.getAnimations():[]).filter(x=>x.animationName==='promiBlink')[0]; if(a){ a.pause(); a.currentTime=0; }
  const c=getComputedStyle(e); let op=1, tern=[]; for(let q=e;q;q=q.parentElement){ const k=getComputedStyle(q); op*=+k.opacity; if(k.filter!=='none') tern.push('filtre'); if(k.mixBlendMode!=='normal') tern.push('fusion'); }
  if(c.textShadow!=='none') tern.push('ombre');
  const r=e.getBoundingClientRect(); return {x:r.left-4, y:r.top-2, w:r.width+8, h:r.height+4, anim:a?[a.effect.getTiming().duration, c.animationTimingFunction, c.animationIterationCount]:null, op:op, tern:tern}; }"""
def coeur(pg, z):
    im = Image.open(io.BytesIO(pg.screenshot(clip={'x': z['x'], 'y': z['y'], 'width': z['w'], 'height': z['h']}))).convert('RGB'); px = list(im.getdata())
    W, H = im.size; bord = [im.getpixel((x, y)) for x in range(W) for y in (0, H - 1)] + [im.getpixel((x, y)) for y in range(H) for x in (0, W - 1)]
    fond = Counter(bord).most_common(1)[0][0]   # le fond se lit sur le BORD de la boîte (une lettre étroite remplit sa boîte)
    encre = [q for q in px if sum(abs(q[j] - fond[j]) for j in range(3)) > 60]
    if not encre: return None, 0
    return Counter(encre).most_common(1)[0][0], len(encre)
LIEUX = (('onboarding', '#onbV .onbv-mm i', None), ('accueil (I de PROMI)', '.acc-mm i', None),
         ('Partager (R)', '#shareScreen .ti-x.blink', "()=>{ try{ ouvrirPartage(); }catch(e){ const b=document.querySelector('#shareBtn'); if(b) b.click(); } }"),
         ('Réglages (S)', '#settingsScreen h1.scr-ti .ti-x.blink', "()=>{ const b=document.querySelector('#settingsBtn'); if(b) b.click(); }"),
         ('Aura (apostrophe)', '#auraScreen .ti-apo', "()=>{ const b=document.querySelector('#souffleBtn'); if(b) b.click(); }"))   # v211 (C-308)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_lettres_bleu — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in A_ else ''))
    for sombre in (False, True):
        th = 'sombre' if sombre else 'clair'
        for nom, sel, ouvre in LIEUX:
            ctx = B.contexte(b, sombre=sombre, onb=(nom != 'onboarding'))
            pg = B.ouvre(ctx, F)
            if nom == 'accueil (I de PROMI)' and th == 'clair' and not hasattr(sys, '_bleuDecl'):
                import re; m = re.search(r"signal:\{name:'Ingénu',cols:\[\[(\d+),(\d+),(\d+)\]", io.open('promi-moteur.js', encoding='utf-8').read()); d = [int(x) for x in m.groups()] if m else None; sys._bleuDecl = 1
                juge('la palette de base déclare #82AEF8 (promi-moteur.js, PALS.signal, premier ton)', d == list(BLEU), d)
            if ouvre: pg.evaluate(ouvre); pg.wait_for_timeout(1800)
            if '--sonde' in A_ and nom.startswith('accueil'): pg.evaluate("()=>document.querySelector('.acc-mm i').style.setProperty('opacity','.9','important')")
            if nom.startswith('Aura'):   # v211 (C-308) : C · le même clignotement, SYNCHRONISÉ sur le I de l'accueil (la phase, à une image près)
                ph = pg.evaluate("()=>{ const f=s=>{ const e=document.querySelector(s); const a=e&&e.getAnimations?e.getAnimations().filter(x=>x.animationName==='promiBlink')[0]:null; return a?a.currentTime:null; }; return [f('#device .acc-mm i'), f('#auraScreen .ti-apo')]; }")
                dph = None if None in ph else abs((ph[0] - ph[1] + 575) % 1150 - 575)
                juge('[%s · %s] C · en phase avec le I de l\'accueil (écart %s ms)' % (th, nom, dph if dph is None else round(dph)), dph is not None and dph <= 17, ph)
            z = pg.evaluate(SOMMET, sel); pg.wait_for_timeout(120)
            if not z:
                juge('[%s · %s] A · la lettre est à l\'écran' % (th, nom), False, sel); ctx.close(); continue
            if nom.startswith('Aura'): z = dict(z, x=z['x'] + 4, w=z['w'] - 8)   # v211 : un glyphe de 6 pt — la boîte exacte en largeur (les 4 pt de marge prenaient le L et le a voisins)
            c, n = coeur(pg, z)
            juge('[%s · %s] A · au sommet, la lettre est #82AEF8 à 1,5 près' % (th, nom), c is not None and max(abs(c[j] - BLEU[j]) for j in range(3)) <= 1.5, {'cœur': ('#%02X%02X%02X' % c) if c else None, 'pixels d\'encre': n})
            juge('[%s · %s] B · promiBlink 1,15 s steps(1,end), rien qui ternit' % (th, nom), z['anim'] and abs(z['anim'][0] - 1150) < 1 and 'steps(1' in z['anim'][1].replace(' ', '') and z['op'] > 0.999 and not z['tern'], {'anim': z['anim'], 'opacité': round(z['op'], 3), 'ternit': z['tern']})
            ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
