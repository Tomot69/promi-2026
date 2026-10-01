# Le correctif `avec` PROUVÉ dans les deux sens (CLAUDE.md §7 : le contrôle se passe d'abord sur la version fautive).
# Sur la fiche de chaque personne : les rangées affichées doivent être EXACTEMENT les paroles où elle est `who`, `from`
# OU `avec`. L'app d'avant doit rater Rachel et Adrien ; la corrigée doit tout avoir, sans erreur, Marion inchangée.
import sys, json
from playwright.sync_api import sync_playwright
CAS = [('avant (sauvegarde)', 'http://127.0.0.1:8752/sauvegardes/app-avant-personne-avec.html', False),
       ('après (app.html)',   'http://127.0.0.1:8752/app.html', True)]
ok = True
with sync_playwright() as p:
    b = p.chromium.launch()
    for nom, url, doit in CAS:
        pg = b.new_page(viewport={'width': 430, 'height': 932}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.goto(url); pg.wait_for_timeout(6800)
        r = pg.evaluate("""()=>['Rachel','Marion','Adrien'].map(n=>{ closeAll(); openPerson(n);
            const vu=[...document.querySelectorAll('#psList .row .a')].map(e=>e.textContent);
            const attendu=promises.filter(p=>!p.draft&&(p.who===n||p.from===n||p.avec===n)).map(p=>p.title);
            return {n:n, vu:vu.length, attendu:attendu.length, manque:attendu.filter(t=>vu.indexOf(t)<0)}; })""")
        tout = all(x['vu'] == x['attendu'] and not x['manque'] for x in r)
        bon = (tout == doit) and not err; ok &= bon
        print('%-20s %s  →  %s   %s' % (nom, '; '.join('%s %d/%d%s' % (x['n'], x['vu'], x['attendu'], (' manque « %s »' % '», «'.join(x['manque'])) if x['manque'] else '') for x in r),
              'COMPLET' if tout else 'INCOMPLET', '✅' if bon else '❌'), ('erreurs : %s' % err[:2]) if err else '')
        pg.close()
    b.close()
print('✅  le correctif mord : l\'avant est pris, l\'après est complet' if ok else '❌  preuve ratée'); sys.exit(0 if ok else 1)
