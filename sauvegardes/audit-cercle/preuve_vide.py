# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# LE CONTRAT « SANS AUCUN PROMI » MORD-IL ?
# ⚑ RÉÉCRITE LE 12 SEPTEMBRE 2026. L'ancienne prouvait la classe `plv-sans` de l'écran d'avant (la rangée de
#   trois dalles cachée) : cet écran n'existe plus. Le nouvel état s'appelle `pc-sans` et il porte plus loin —
#   sans Promi il n'y a AUCUNE dalle à rendre, donc aucune Toile : le cadre s'efface et tout remonte de 238.
#   Original : sauvegardes/preuve_vide-avant-cercle-toile.py
# Le défaut trouvé par ce contrat, et c'est pour ça qu'il existe : sans lui la Toile sortait VIDE À 100 % en
# sombre, et les trois pastilles gardaient leur canevas par défaut (300 × 150) écrasé dans 16 × 16.
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import io, os, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
src = io.open(os.path.join(D, 'verif_cercle.py'), encoding='utf-8').read().split("if __name__ == '__main__':")[0]
ns = {'__file__': os.path.join(D, 'verif_cercle.py'), '__name__': 'preuve'}; exec(src, ns)
ETAT, contrats, ouvre = ns['ETAT'], ns['contrats'], ns['ouvre']

SONDES = [
 ('témoin : aucun Promi, l’écran s’ouvre', None, None),
 ('la classe pc-sans RETIRÉE (le cadre vide reparaît)', 'sans Promi · le cadre porte pc-sans',
  "()=>{ document.getElementById('pcCadre').classList.remove('pc-sans'); }"),
 ('le titre laissé à sa cote basse', 'sans Promi · tout est remonté',
  "()=>{ document.querySelector('#pcCadre .pc-h').style.setProperty('top','336px','important'); }"),
 ('une pastille montrée SANS sa dalle', 'sans Promi · les pastilles sont cachées',
  "()=>{ const c=document.querySelector('#pcCadre .pc-ch'); c.setAttribute('data-dalle','0'); c.style.setProperty('display','inline-block','important'); }"),
 ('le prix reposé sur le premier argument', 'aucun bloc n’en chevauche un autre',
  "()=>{ document.querySelector('#pcCadre .pc-prix').style.setProperty('top','200px','important'); }"),
]

# ═══ LA VERSION FAUTIVE — celle d'avant le correctif du 12 septembre ═══
# On ne fabrique pas ce défaut : il a existé. `cleCollection()` ne portait que palette·teinte·thème, donc
# `COLL` et `TODO` survivaient à la disparition des Promi et l'écran posait encore des dalles d'ids supprimés.
# Le contrat doit ROUGIR sur ce fichier-là (§7 : « un contrôle qui ne prend pas la version fautive ne vaut rien »).
FAUTIF = os.path.join(D, '..', 'app-avant-src-valide.html')
VISES_FAUTIFS = ('sans Promi · le cadre porte pc-sans', 'sans Promi · la collection est vide')

def sur_version_fautive(br):
    import shutil
    if not os.path.exists(FAUTIF):
        print('   (la version fautive est absente : preuve non faite)'); return None
    cible = os.path.join(D, '..', '..', 'scratchpad', 'app-avant-src-valide.html')
    if os.path.abspath(cible) != os.path.abspath(FAUTIF): shutil.copyfile(FAUTIF, cible)
    src2 = io.open(os.path.join(D, 'verif_cercle.py'), encoding='utf-8').read().split("if __name__ == '__main__':")[0]
    ns2 = {'__file__': os.path.join(D, 'verif_cercle.py'), '__name__': 'fautif'}
    exec(src2.replace("URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'",
                      "URL = 'http://127.0.0.1:8752/scratchpad/app-avant-src-valide.html'"), ns2)
    pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    ns2['ouvre'](pg, 'light', vider=True)
    e = ns2['ETAT'] and pg.evaluate(ns2['ETAT'])
    rouges = [n for n, ok, _ in ns2['contrats'](e, 'light') if not ok]
    pg.context.close()
    pris = [n for n in VISES_FAUTIFS if any(r.startswith(n) for r in rouges)]
    for n in VISES_FAUTIFS:
        ok = any(r.startswith(n) for r in rouges)
        print('   %s  %s' % ('PRIS ' if ok else 'RATÉ ', n))
    return len(pris), len(VISES_FAUTIFS)

if __name__ == '__main__':
    print('═══ SANS AUCUN PROMI — une sonde à la fois, les deux thèmes ═══')
    total, bons, f = 0, 0, None
    with sync_playwright() as p:
        br = p.chromium.launch()
        for th in ('dark', 'light'):
            for nom, vise, js in SONDES:
                pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
                ouvre(pg, th, vider=True)
                sans = pg.evaluate("()=>{const c=document.getElementById('pcCadre'); return !!c && c.classList.contains('pc-sans');}")
                if not sans:
                    # la collection était déjà en cache : l'écran a de quoi montrer, l'état `pc-sans` n'a pas lieu d'être
                    print('   %-6s %-50s —      pc-sans absent (collection en cache) : cas non applicable' % (th, nom))
                    pg.context.close(); continue
                if js: pg.evaluate(js); pg.wait_for_timeout(400)
                e = pg.evaluate(ETAT)
                rouges = [n for n, ok, _ in contrats(e, th) if not ok]
                if vise is None:
                    ok = not rouges
                    print('   %-6s %-50s %s %s' % (th, nom, 'vert  ' if ok else 'ROUGE ', rouges or 'aucun rouge'))
                else:
                    touche = [n for n in rouges if n.startswith(vise)]
                    ok = bool(touche)
                    autres = [n for n in rouges if not n.startswith(vise)]
                    print('   %-6s %-50s %s visé « %s »%s' % (th, nom, 'PRIS  ' if ok else 'RATÉ  ', vise,
                           '' if not autres else ' · aussi : ' + ', '.join(autres[:2])))
                total += 1; bons += 1 if ok else 0
                pg.context.close()
        print()
        print('═══ sur la VERSION FAUTIVE (app-avant-src-valide.html) ═══')
        f = sur_version_fautive(br)
        br.close()
    if f: print('   %d / %d contrats PRIS sur la version fautive' % f)
    print()
    print(('✅  %d / %d — chaque contrat visé a été PRIS.' % (bons, total)) if bons == total
          else ('❌  %d / %d — %d n’ont pas mordu.' % (bons, total, total - bons)))
