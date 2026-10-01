# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# LES CONTRATS DE L'ÉCRAN QUI VEND MORDENT-ILS, UN PAR UN ?
# ⚑ RÉÉCRITE LE 12 SEPTEMBRE 2026. L'ancienne version prouvait les contrats de l'écran d'avant (la rangée de
#   trois dalles, « 29 € », la classe `plv-sans`) : cet écran n'existe plus, `lot-CERCLE-VEND` est retiré, et
#   elle passait donc au vert sur du vide. Original : sauvegardes/preuve_vend-avant-cercle-toile.py
# La règle (CLAUDE §7) : on fabrique le défaut que le contrôle est censé attraper, on le pose, et on vérifie
# qu'il est PRIS — et lui seul, autant que possible. Une page neuve par sonde : rien ne contamine la suivante.
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import io, os, re, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
src = io.open(os.path.join(D, 'verif_cercle.py'), encoding='utf-8').read().split("if __name__ == '__main__':")[0]
ns = {'__file__': os.path.join(D, 'verif_cercle.py'), '__name__': 'preuve'}; exec(src, ns)
ETAT, contrats, ouvre, BASE = ns['ETAT'], ns['contrats'], ns['ouvre'], ns['BASE']

SONDES = [
 ('rien (témoin)', None, None),
 ('le prix réécrit à 49 €', 'le prix est celui décidé',
  "()=>{ document.querySelector('#pcCadre .pc-prix b').textContent='49 €'; }"),
 ('« Cercle » repeint en encre', '« Cercle » est en mauve',
  "()=>{ const e=document.querySelector('#pcCadre .pc-h2'); e.style.setProperty('color','#1A1613','important'); e.style.setProperty('-webkit-text-fill-color','#1A1613','important'); }"),
 ('l’essai poussé hors de l’écran', 'l’essai est visible sans défiler',
  "()=>{ document.getElementById('buyMonth').style.setProperty('top','900px','important'); }"),
 ('la Toile effacée', 'le fond ne paraît pas',
  "()=>{ const c=document.querySelector('#pcCadre .pc-toile canvas'); c.getContext('2d').clearRect(0,0,c.width,c.height); }"),
 ('un monde retiré des poses', 'les huit mondes sont présents',
  "()=>{ const v=window._vendToile; delete v.matieres.gravure; }"),
 ('la Touffe poussée à 80 %', 'la Touffe domine sans tout manger',
  "()=>{ const v=window._vendToile; const t=Object.values(v.matieres).reduce((a,b)=>a+b,0); v.matieres.touffe=Math.round(4*t); }"),
 ('une pastille redimensionnée', 'aucune pastille n’est redimensionnée',
  "()=>{ const c=document.querySelector('#pcCadre .pc-ch'); c.style.setProperty('width','44px','important'); c.style.setProperty('height','44px','important'); }"),
 ('une pastille sans sa dalle', 'les pastilles suivent les données',
  "()=>{ document.querySelector('#pcCadre .pc-ch').removeAttribute('data-dalle'); }"),
 ('le ✕ FERMER masqué', 'le ✕ FERMER est celui du produit',
  "()=>{ document.querySelector('#plusScreen .closeb').style.setProperty('display','none','important'); }"),
 ('le légal descendu sous le pli', 'rien ne descend sous le pli',
  "()=>{ document.querySelector('#pcCadre .pc-legal').style.setProperty('top','860px','important'); }"),
 ('le prix posé SUR le premier argument', 'aucun bloc n’en chevauche un autre',
  "()=>{ document.querySelector('#pcCadre .pc-prix').style.setProperty('top','440px','important'); }"),
 ('l’écran rendu défilant', 'l’écran ne défile pas',
  # ⚠ 400 px ne suffisaient pas : tout le contenu de l'écran est en ABSOLU, son flux est quasi vide, et
  #   `scrollHeight` restait sous les 876 du conteneur. La sonde était faible, pas le contrat.
  "()=>{ const d=document.createElement('div'); d.style.cssText='position:relative;height:1400px'; document.getElementById('plusScreen').appendChild(d); }"),
 ('un libellé repassé en Apfel', 'les libellés sont en Bricolage 600',
  "()=>{ document.querySelector('#pcCadre .pc-arg b').style.setProperty('font-family','Apfel','important'); }"),
 ('le CTA repeint en bleu', 'le CTA est en framboise',
  "()=>{ document.getElementById('buyMonth').style.setProperty('background','#3A54FF','important'); }"),
 ('la collection vidée', 'la Toile est faite de vraies dalles',
  "()=>{ window._vendToile.collection=0; window._vendToile.poses=0; }"),
]

def statique_fautive():
    """⚑ LA FAMILLE STATIQUE SE PROUVE SUR UN FICHIER FAUTIF — on ne peut pas la sonder à l'écran.
       On écrit une copie de l'app où le lot porte une DÉCOUPE (drawImage à 9 arguments) et un getImageData,
       et on vérifie que les contrats statiques rougissent."""
    APP = os.path.join(D, '..', '..', 'app.html')
    S = io.open(APP, encoding='utf-8').read()
    old = "    g.drawImage(d.cv, -d.w/2, -d.h/2, d.w, d.h);"
    if S.count(old) != 1: return [('la sonde statique s’applique', False, 'motif introuvable')]
    faux = S.replace(old, "    g.drawImage(d.cv, 2, 2, d.cv.width-4, d.cv.height-4, -d.w/2, -d.h/2, d.w, d.h);\n"
                          "    try{ d.cv.getContext('2d').getImageData(0,0,1,1); }catch(_){ }")
    tmp = os.path.join(D, '..', '..', 'scratchpad', 'app-preuve-decoupe.html')
    io.open(tmp, 'w', encoding='utf-8').write(faux)
    ns2 = {'__file__': os.path.join(D, 'verif_cercle.py'), '__name__': 'preuve2'}
    exec(src.replace("APP = os.path.join(D, '..', '..', 'app.html')",
                     "APP = os.path.join(D, '..', '..', 'scratchpad', 'app-preuve-decoupe.html')"), ns2)
    out = ns2['statique']()
    os.remove(tmp)
    return out

if __name__ == '__main__':
    print('═══ LA FAMILLE STATIQUE, SUR UN FICHIER FAUTIF (une découpe posée dans le lot) ═══')
    pris = 0
    for nom, ok, dit in statique_fautive():
        vise = nom in ('aucune découpe d’image (drawImage à 9 arguments)', 'aucun choix de pixels (getImageData)')
        etat = 'PRIS  ' if (vise and not ok) else ('vert  ' if ok else 'rouge ')
        if vise and not ok: pris += 1
        print('   %-52s %s %s' % (nom, etat, dit))
    print('   → %d / 2 contrats statiques PRIS sur le fichier fautif' % pris)
    print()
    print('═══ LES CONTRATS DE L’ÉCRAN, UNE SONDE À LA FOIS (thème clair, avec Promi) ═══')
    total, bons = 0, 0
    with sync_playwright() as p:
        br = p.chromium.launch()
        for nom, vise, js in SONDES:
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            ouvre(pg, 'light')
            if js:
                pg.evaluate(js); pg.wait_for_timeout(400)
            e = pg.evaluate(ETAT)
            C = contrats(e, 'light')
            rouges = [n for n, ok, _ in C if not ok]
            if vise is None:
                ok = not rouges
                print('   %-42s %s  %s' % (nom, 'vert  ' if ok else 'ROUGE ', rouges or 'aucun rouge'))
                total += 1; bons += 1 if ok else 0
            else:
                touche = [n for n in rouges if n.startswith(vise)]
                ok = bool(touche)
                autres = [n for n in rouges if not n.startswith(vise)]
                print('   %-42s %s  visé « %s »%s' % (nom, 'PRIS  ' if ok else 'RATÉ  ', vise,
                       ('' if not autres else ' · aussi : ' + ', '.join(autres[:2]))))
                total += 1; bons += 1 if ok else 0
            pg.context.close()
        br.close()
    print()
    print(('✅  %d / %d' % (bons, total)) + ' — chaque contrat visé a été PRIS sur son défaut.' if bons == total
          else ('❌  %d / %d — %d contrat(s) n’ont pas mordu.' % (bons, total, total - bons)))
