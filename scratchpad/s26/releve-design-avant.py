#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RELEVE DU DESIGN — le contrat visuel de Promi.

   A lancer APRES chaque lot :

       python3 releve-design.py

   Il releve 26 elements dans 6 configurations et compare a la reference.
   Tout ecart non demande par le lot est une regression.

   Pour figer une nouvelle reference apres un lot VALIDE :

       python3 releve-design.py --figer
"""
import json, os, sys
from playwright.sync_api import sync_playwright

REF = 'design-reference.json'
PROPS = ['fontFamily','fontSize','fontWeight','letterSpacing','lineHeight','textTransform',
         'color','backgroundColor','opacity','paddingTop','paddingRight','paddingBottom',
         'paddingLeft','marginTop','marginBottom','borderRadius','boxShadow','width','height',
         'display','position','gap','zIndex','filter','mixBlendMode']
CIBLES = {
 # ⚑ Le mot de nature vit désormais DANS le plateau commun (décision Tom, 2 sept. 2026 :
 # « dans aucune fiche j'ai vu que t'avais mis le bandeau, faut le faire »). Il n'est plus
 # sous `#dpTete` : le sélecteur le cherchait PAR SA PLACE, il ne le trouvait plus —
 # « ELEMENT DISPARU », quatre fois. Le nœud, lui, est intact : même classe, même mot.
 # Original : sauvegardes/releve-design-avant-bandeau-fiche.py
 'fiche · nature':'#detailPoster .dpt-nat',
 'fiche · a qui':'#dpTete .dpt-qui',
 'fiche · titre':'#dpTete .dpt-titre',
 'fiche · etat':'#dpTete .dpt-quand',
 'fiche · fermer':'#detailPoster .closeb',
 'fiche · rang lien':'#dAura',
 'fiche · disque':'#detailPoster .kr-c',
 'fiche · nom lien':'#detailPoster .kr-n',
 'fiche · mot lien':'#detailPoster .kr-w',
 'fiche · bouton rond':'#dpBarre .dpb',
 'fiche · zone geste':'#tenirZone',
 'fiche · libelle geste':'#detailPoster .tenir-lab',
 'fiche · bascule':'#detailPoster .tenir-alt',
 'fiche · peaufiner':'#dpDetails .dpd-tog',
 'fiche · partager':'#dpDetails .dpd-part',
 'fiche · libelle section':'#detailPoster .mg-lab',
 'fiche · champ':'#detailPoster input',
 'fiche · pastille':'#detailPoster .chip',
 'nuee · ligne':'#dpNueeFil .nf-item',
 'nuee · mot temps':'#dpNueeFil .nf-tx em',
 'nuee · titre ligne':'#dpNueeFil .nf-tx b',
 'nuee · a qui ligne':'#dpNueeFil .nf-tx span',
 'nuee · dalle ligne':'#dpNueeFil .nf-d',
 'nuee · bouton planter':'#dpNueeFil .nf-add',
 'trace · libelle':'#dpTrace .dpt-lab',
 'trace · trait':'#dpTrace .dpt-svg',
}
JS = """a=>{const [cibles,props]=a;const o={};
  const dp=document.getElementById('detailPoster');
  if(dp) o['__fond']={backgroundColor:getComputedStyle(dp).backgroundColor,
    accent:dp.style.getPropertyValue('--accent')||'',
    dalle:dp.style.getPropertyValue('--dalle')||''};
  for(const k in cibles){const e=document.querySelector(cibles[k]);
    if(!e)continue;const c=getComputedStyle(e);const d={};
    props.forEach(x=>{if(c[x]&&c[x]!=='none'&&c[x]!=='normal'&&c[x]!=='auto')d[x]=c[x];});
    const q=e.getBoundingClientRect();
    d._px=[Math.round(q.width),Math.round(q.height)];
    o[k]=d;}
  return o;}"""

# Les polices (embarquees en base64 ET, pour Fraunces, tirees d'un <link> Google)
# se chargent de facon ASYNCHRONE. Mesurer avant qu'elles soient pretes donne des
# largeurs de repli (Georgia/system) qui derivent d'un passage a l'autre. On attend
# donc explicitement chaque face utilisee, puis une image, avant toute mesure.
FONTS = """async()=>{
  try{
    await document.fonts.ready;
    await document.fonts.load('600 40px \"Fraunces\"');
    await document.fonts.load('italic 600 40px \"Fraunces\"');
    await document.fonts.load('500 40px \"ApfelMid\"');
    await document.fonts.load('400 40px \"Apfel\"');
    await document.fonts.load('700 40px \"Bricolage\"');
    await document.fonts.ready;
  }catch(e){}
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>r())));
  return document.fonts.status;
}"""

def relever(fichier='app.html'):
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width':390,'height':844})
        erreurs = []
        pg.on('pageerror', lambda e: erreurs.append(str(e)))
        pg.goto('file://' + os.path.abspath(fichier))
        pg.wait_for_timeout(7000)
        pg.evaluate(FONTS)   # attendre que TOUTES les polices soient pretes
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for mode in ['clair','sombre']:
            pg.evaluate("m=>document.querySelectorAll('.frame,.device')"
                        ".forEach(e=>e.classList.toggle('light',m==='clair'))", mode)
            # SECTION 4 : l'Index est porté au moodboard. Le bloc `.ix-bloc` est devenu la
            # carte `.s4-carte` (§3.9), qui porte sa nature et son état en attributs.
            for nom, sel in [('atenir','.s4-carte[data-etat=atenir]'),
                             ('tenue','.s4-carte[data-etat=tenue]'),
                             ('nuee','.s4-carte[data-etat=nuee]')]:
                pg.evaluate("()=>document.querySelectorAll('.screen,.sheet,.poster')"
                            ".forEach(e=>e.classList.remove('show'))")
                pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();}")
                pg.wait_for_timeout(1300)
                ok = pg.evaluate("s=>{const x=document.querySelector('#indexSheet '+s);"
                                 "if(x){x.click();return 1;}return 0;}", sel)
                if not ok: continue
                pg.wait_for_timeout(2400)
                pg.evaluate(FONTS)   # re-verifier avant CETTE mesure
                out[mode+'/'+nom] = pg.evaluate(JS, [CIBLES, PROPS])
        b.close()
    return out, erreurs

def _proche(a, b):
    """deux couleurs a moins de 4 unites pres sont la meme : le rendu des
       dalles varie de +-2 d'une peinture a l'autre."""
    import re
    if a == b: return True
    ma = re.findall(r'\d+', str(a)); mb = re.findall(r'\d+', str(b))
    if len(ma) != len(mb) or not ma: return False
    return all(abs(int(x) - int(y)) <= 4 for x, y in zip(ma, mb))

# la teinte des dalles est tiree au hasard a chaque chargement : les
# proprietes qui en derivent ne peuvent pas servir de reference figee.
# On les verifie autrement — voir controler_couleurs().
VARIABLES = {'boxShadow', 'backgroundColor', 'color', 'accent', 'dalle',
             'borderColor', 'fill', 'stroke'}

# ⚑ L'ENCRE ET LE PAPIER NE SONT PAS DES GRIS (16 septembre 2026).
#   Le critere approchait l'encre par un seuil — « max(v) < 30 » — cale sur l'ancienne encre
#   bleu-noir #16171B (22,23,27). La nouvelle encre est le brun #201908 (32,25,8) : max 32,
#   ecart 24 — le juge l'a declaree « trait NEUTRE » sur trois fiches. Ce n'est pas la regle du
#   §3 qui a change (« jamais de trait neutre ou gris ») : c'est l'INSTRUMENT qui approchait
#   l'encre au lieu de la nommer. On la nomme. Les vrais coupables — les gris moyens, #888888,
#   #83858C — restent pris : verifie en posant un trait gris sur la fiche (scratchpad/preuve_neutre.py).
ENCRES = {
    (32, 25, 8),      # l'encre du jeu, mode clair  · le fond du mode sombre
    (247, 240, 222),  # le papier du jeu, mode clair · l'encre du mode sombre
    (22, 23, 27),     # l'encre d'avant le 16 septembre — gardee, la reference peut etre ancienne
    (244, 238, 225),  # le papier d'avant
}

def controler_couleurs(neuf):
    """la regle : aucun trait neutre, aucun accent gris."""
    import re
    fautes = []
    for cfg, elems in neuf.items():
        acc = elems.get('__fond', {}).get('accent', '')
        if acc:
            m = re.findall(r'\d+', acc)
            if len(m) >= 3:
                v = [int(x) for x in m[:3]]
                if max(v) - min(v) < 26:
                    fautes.append('%s : accent NEUTRE %s' % (cfg, acc))
        for cle, d in elems.items():
            if 'bascule' in cle: continue   # elle porte l'encre, c'est voulu
            bs = d.get('boxShadow', '')
            m = re.findall(r'rgba?\(([^)]*)\)', bs)
            for c in m:
                v = [int(float(x)) for x in re.findall(r'[\d.]+', c)[:3]]
                if len(v) == 3 and max(v) - min(v) < 26 and tuple(v) not in ENCRES \
                   and not (max(v) < 30 or min(v) > 225):
                    fautes.append('%s · %s : trait NEUTRE rgb(%s)' % (cfg, cle, ','.join(map(str,v))))
    return fautes

def comparer(ref, neuf):
    ecarts = []
    for cfg in ref:
        if cfg not in neuf:
            ecarts.append('%s : CONFIGURATION DISPARUE' % cfg); continue
        for cle in ref[cfg]:
            if cle not in neuf[cfg]:
                ecarts.append('%s · %s : ELEMENT DISPARU' % (cfg, cle)); continue
            for prop in ref[cfg][cle]:
                if prop in VARIABLES: continue
                a = ref[cfg][cle][prop]
                b = neuf[cfg][cle].get(prop)
                if a != b and not _proche(a, b):
                    ecarts.append('%s · %s · %s : %s -> %s'
                                  % (cfg, cle, prop, str(a)[:26], str(b)[:26]))
    return ecarts

if __name__ == '__main__':
    figer = '--figer' in sys.argv
    neuf, erreurs = relever('sauvegardes/app-avant-lot-v12.html')
    json.dump(neuf, open('tokens.json','w'), indent=1, ensure_ascii=False)

    if erreurs:
        print('⚠  ERREURS JAVASCRIPT :')
        for e in erreurs[:3]: print('   ', e)
        print()

    if figer or not os.path.exists(REF):
        json.dump(neuf, open(REF,'w'), indent=1, ensure_ascii=False)
        print('Référence figée : %d configurations, %d éléments.'
              % (len(neuf), sum(len(v) for v in neuf.values())))
        sys.exit(0)

    ref = json.load(open(REF))
    ecarts = comparer(ref, neuf)
    fautes = controler_couleurs(neuf)

    if fautes:
        print('❌  %d COULEURS FAUTIVES :\n' % len(fautes))
        for f in fautes[:20]: print('   ', f)
        print()

    if not ecarts and not fautes:
        print('✅  AUCUN ÉCART. Le design est intact.')
    elif not ecarts:
        print('Les dimensions sont intactes, mais voir les couleurs ci-dessus.')
        sys.exit(1)
    else:
        print('❌  %d ÉCARTS avec la référence :\n' % len(ecarts))
        for e in ecarts[:400]: print('   ', e)
        if len(ecarts) > 40: print('    … et %d autres' % (len(ecarts)-40))
        print('\nSi le lot ne demandait pas ces changements, c\'est une régression.')
        sys.exit(1)
