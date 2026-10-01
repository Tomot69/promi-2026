# OÙ LA PILULE MANGE-T-ELLE LE TEXTE — mesuré SUR L'ENCRE (11 sept. 2026).
# Le premier instrument du lot mesurait des BOÎTES de ligne, et il fusionnait le libellé de gauche avec la valeur de droite
# (« 0 fichier », à 23, donnait son haut à « PIÈCES JOINTES », à 26,4) : le coin mesuré n'était celui d'aucun texte.
# Ici : chaque champ à contour est capturé (écran 390, densité 2) ; l'encre = tout pixel intérieur qui s'écarte du fond du
# champ ; le contour réel est exclu analytiquement (1,5 px sous la courbe intérieure). L'analyse (seuil_encre_analyse.py)
# recalcule la distance de chaque pixel d'encre à la courbe intérieure pour TOUT rayon — l'encre ne dépend pas du rayon.
# Abonné pendant la mesure (le flou du mur n'est pas du texte) ; thème sombre.
import json, os, sys
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'lignes', 'encre'); os.makedirs(OUT, exist_ok=True)
L2 = "prévenir Rachel la veille, apporter le gâteau et les bougies"
L3 = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
TROUVE = r"""const trouve=(hote)=>{ const H=document.querySelector(hote); const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390; const out=[];
  H.querySelectorAll('*').forEach(c=>{ if(!c.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return; const cs=getComputedStyle(c), r=c.getBoundingClientRect();
    const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2);
    if(bw<=0 || r.height<40*s || R<20*s || r.width<300*s) return;
    const lab=(c.querySelector('.s2-lab,.np-lab')||c).textContent.replace(/\s+/g,' ').trim().slice(0,22);
    out.push({c, cle: lab+'|'+(c.id||String(c.className).split(' ').slice(0,3).join('.'))}); }); return out; };"""
LISTE = "(hote)=>{ " + TROUVE + " return trouve(hote).map(x=>x.cle); }"
PREP = "([hote,cle])=>{ " + TROUVE + " const x=trouve(hote).find(y=>y.cle===cle); if(!x) return false; x.c.scrollIntoView({block:'center'}); return true; }"
RECT = r"""([hote,cle])=>{ """ + TROUVE + r""" const x=trouve(hote).find(y=>y.cle===cle); if(!x) return null; const c=x.c, r=c.getBoundingClientRect(), cs=getComputedStyle(c);
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const vis = r.top>=dv.top+2 && r.bottom<=dv.bottom-2;
  return {x:r.left, y:r.top, w:r.width, h:r.height, s, bw:parseFloat(cs.borderTopWidth)/1, R:Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2), vis,
          fond:cs.backgroundColor, bord:cs.borderTopColor}; }"""
ECRANS = {
  'fiche': ('#detailPoster', [(BASE, 200), ("()=>openDetail(126)", 1400), ("()=>document.querySelector('#dpDetails .dpd-tog').click()", 1700)]),
  'page+': ('#createSheet', [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 600),
     ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
     ("()=>document.getElementById('csBotBar').click()", 1800)]),
  'Nuée': ('#detailPoster', [(BASE, 200), ("()=>openEssaim('potager')", 1500), ("()=>document.querySelector('#dpDetails .dpd-tog').click()", 1700)]),
}
ETATS = [('fiche', 'invite', None), ('fiche', 'note2', L2), ('fiche', 'note3', L3),
         ('page+', 'invite', None), ('page+', 'note2', L2), ('page+', 'note3', L3), ('Nuée', 'invite', None)]
META = {}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>setPremium(true)"); pg.wait_for_timeout(400)
    for ecran, etat, texte in ETATS:
        hote, steps = ECRANS[ecran]
        for js, w in steps: pg.evaluate(js); pg.wait_for_timeout(w)
        if texte:
            pg.evaluate("(t)=>{ const x=document.querySelector('%s .s2-zone textarea'); x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); }" % hote, texte); pg.wait_for_timeout(700)
        cles = pg.evaluate(LISTE, hote)
        if texte: cles = [k for k in cles if k.startswith('NOTE|')]
        for cle in cles:
            for essai in range(4):
                if not pg.evaluate(PREP, [hote, cle]): break
                pg.wait_for_timeout(300)
                r1 = pg.evaluate(RECT, [hote, cle])
                if not r1 or not r1['vis']: continue
                nom = '%s_%s_%s.png' % (ecran, etat, cle.split('|')[0].replace(' ', '_').replace("'", '').replace('?', '').replace('/', '_'))
                pg.screenshot(path=os.path.join(OUT, nom), clip={'x': r1['x'], 'y': r1['y'], 'width': r1['w'], 'height': r1['h']})
                r2 = pg.evaluate(RECT, [hote, cle])
                if r2 and abs(r2['h'] - r1['h']) < 0.5 and abs(r2['y'] - r1['y']) < 0.5:     # rien n'a bougé pendant la capture
                    META['%s · %s · %s' % (ecran, etat, cle)] = dict(r1, png=nom); break
            else:
                print('   ⚠ non capturé :', ecran, etat, cle)
        if texte or ecran == 'page+':
            pg.evaluate("()=>{ document.querySelectorAll('#dNote, #createSheet .s2-zone textarea').forEach(x=>{ x.value=''; x.dispatchEvent(new Event('input',{bubbles:true})); }); }")
        print('%-6s %-7s %d champ(s)' % (ecran, etat, sum(1 for k in META if k.startswith(ecran + ' · ' + etat))))
    br.close()
json.dump(META, open(os.path.join(OUT, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
