#!/usr/bin/env python3
"""
spec_juges_generer.py — ENGENDRE « SPEC-JUGES.md » (assainissement, lot 4, Tom, 30 sept. 2026).

Les règles qui n'existaient QUE dans les juges (Playwright, que le portage Swift ne reprendra pas) sont écrites ici en
spécification — et les VALEURS sont lues DANS les juges eux-mêmes (on exécute leurs constantes), jamais recopiées : un juge
qui change une valeur change la spécification au prochain passage de ce script.
Usage : python3 spec_juges_generer.py
"""
import io, os, re, json, datetime

ICI = os.path.dirname(os.path.abspath(__file__))


def constantes(fichier, noms):
    """lit les affectations de haut niveau nommées, dans l'arbre du juge (ast.literal_eval : des littéraux, rien n'est exécuté)."""
    import ast
    src = io.open(os.path.join(ICI, fichier), encoding='utf-8').read()
    ns = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                for nom in ([t] if isinstance(t, ast.Name) else list(getattr(t, 'elts', []))):
                    if isinstance(nom, ast.Name) and nom.id in noms:
                        try:
                            v = ast.literal_eval(n.value)
                            if isinstance(t, ast.Tuple): v = v[t.elts.index(nom)]
                            ns[nom.id] = v
                        except Exception as e: ns[nom.id] = 'illisible (%s)' % type(e).__name__
    return ns


def main():
    o = []; w = o.append
    w('# LES RÈGLES QUE PORTENT LES JUGES — spécification pour le portage')
    w('')
    w('> Engendré par `spec_juges_generer.py` le %s. **Les valeurs sont lues dans les juges eux-mêmes** : pour changer une valeur, '
      'on change le juge (sur une décision de Tom), puis on relance. Le portage Swift ne reprend pas Playwright : il reprend CES règles, '
      'et `banc_rendu.py` (280 images au pixel) pour la matière.' % datetime.date.today().isoformat())
    w('')
    # ── 1 · le rythme des mondes
    R = constantes('redteam_rythme.py', ['ATTENDU', 'TOLERANCE', 'CONSTANTES'])
    w('## 1 · Le rythme de chaque monde — `redteam_rythme.py`')
    w('')
    w('On juge **la fin du mouvement dans le moteur** (l\'image où la Toile cesse de bouger) à l\'arrivée d\'une parole et à son départ, '
      'à **± max(100 ms, 8 %)** sauf tolérance écrite. **Houle** (`sillons`) est l\'exception : elle reste PAR IMAGE, on juge son nombre '
      'd\'images (± max(3, 20 %)). La **cadence** ne tombe jamais sous 60 % de la cadence validée. Valeurs validées le 26 sept. 2026 '
      '(v60, vrai GPU), puis les décisions datées dans le juge.')
    w('')
    w('| Monde | Famille | Arrivée | Départ | Tolérance écrite |')
    w('|---|---|---|---|---|')
    T = R.get('TOLERANCE', {})
    for m, (fam, ((a, ai), (d, di))) in R.get('ATTENDU', {}).items():
        tol = ', '.join('%s ± %d %%' % (k[1], round(v * 100)) for k, v in T.items() if k[0] == m)
        w('| %s | %s | %s ms (%d images) | %s ms (%d images) | %s |' % (m, fam, a, ai, d, di, tol or '—'))
    w('')
    w('**Les constantes qui font ce rythme** (vérifiées dans le source, moteur compris) :')
    for nom, _ in R.get('CONSTANTES', []): w('- ' + nom)
    w('')
    # ── 2 · les murs
    M = constantes('redteam_murs.py', ['ABSENCE_JOURS', 'FLOU', 'LECTURE_MIN', 'LECTURE_MAX', 'RESTE_MS', 'DLUM', 'ENCRE'])
    w('## 2 · Les murs de Ma Parole ! — `redteam_murs.py`')
    w('')
    w('- flou d\'un réglage réservé : `%s` (le Studio garde les siens) ; aucun encart, aucune explication' % M.get('FLOU'))
    w('- la phrase se pose au centre du mur touché, sans fond ni trait, en 3 lignes au plus, une seule taille ; encre %s' % json.dumps(M.get('ENCRE'), ensure_ascii=False))
    w('- temps de lecture : 1,4 s + 60 ms par caractère, borné à [%s ; %s] ms ; elle est encore là à %s ms' % (M.get('LECTURE_MIN'), M.get('LECTURE_MAX'), M.get('RESTE_MS')))
    w('- la toute première fois l\'offre s\'ouvre à la fin de la lecture ; ensuite un toucher pendant la lecture l\'ouvre')
    w('- « Ma Parole ! » d\'une autre couleur que la phrase, les deux à Δlum ≥ %s du fond' % M.get('DLUM'))
    w('- compteur global, 21 phrases dans l\'ordre puis au hasard sans répéter la précédente ; remis à zéro après %s jours' % M.get('ABSENCE_JOURS'))
    w('')
    # ── 3 · les notifications
    N = constantes('redteam_notifs.py', ['MOTS', 'LIGNES', 'FLOU'])
    w('## 3 · Les notifications — `redteam_notifs.py`')
    w('')
    w('- jamais de demande de permission au lancement ; « Je te le rappelle ? » à la plantation d\'une parole datée, demande seulement après « oui »')
    w('- deux « pas besoin » d\'affilée, puis plus rien ; rien pour une parole en l\'air')
    w('- **rien quand la date est passée** ; une notification par jour au plus ; « C\'est aujourd\'hui » à l\'heure choisie')
    w('- la page : %s' % ' · '.join(N.get('LIGNES', [])))
    w('- les mots, au caractère près :')
    for k, (t, x) in N.get('MOTS', {}).items(): w('  - `%s` — titre « %s » · texte « %s »' % (k, t, x))
    w('')
    # ── 4 · le reste
    P = constantes('redteam_pelote_partage.py', ['LONG', 'TOL'])
    F = constantes('redteam_flash.py', ['COURT_MS', 'POINTS', 'INTERDITS'])
    G = constantes('redteam_studio_geste.py', ['MAINTIEN', 'COURSE', 'PAS_PAL'])
    A = constantes('redteam_air.py', ['TOL'])
    FI = constantes('redteam_filets.py', ['SANCTIONNES'])
    D = constantes('releve-design.py', ['PROPS', 'CIBLES', 'VARIABLES'])
    w('## 4 · Les gestes, l\'air, les filets, le contrat visuel')
    w('')
    w('- **Partager la Pelote** (`redteam_pelote_partage.py`) : appui long **%s ms**, tolérance de déplacement **%s px** ; seule, ou dans Mon Folio, déplaçable au doigt ; jamais dans « Ma Toile ».' % (P.get('LONG'), P.get('TOL')))
    w('- **Le geste de couleur du Studio** (`redteam_studio_geste.py`) : appui **%s ms**, course horizontale **%s px** = un tour de teinte, un pas vertical de **%s px** = une palette ; on revient exactement d\'où l\'on vient.' % (G.get('MAINTIEN'), G.get('COURSE'), G.get('PAS_PAL')))
    w('- **Rien ne paraît une fraction de seconde** (`redteam_flash.py`) : aucune couche de premier plan (grille 6 × 11, %s points au moins) ne vit moins de **%s ms**, ni au début ni à la fin ; jamais l\'ancien chrome %s ; la page + paraît composée dès sa première image ; une plantation coupe.' % (F.get('POINTS'), F.get('COURT_MS'), ', '.join('`%s`' % x for x in F.get('INTERDITS', ()))))
    w('- **L\'air entre les textes** (`redteam_air.py`) : aucune paire de textes ne se resserre de plus de **%s px** à l\'ENCRE contre la référence `air-reference.json` (ses paires sont la spécification : %s) ; un bloc annoncé centré entre deux voisins a des écarts égaux.' % (A.get('TOL'), _paires()))
    w('- **Les filets** (`redteam_filets.py`) : aucun trait horizontal hors de ceux que le moodboard porte : %s.' % ', '.join('`%s`' % x for x in FI.get('SANCTIONNES', ())))
    OR = constantes('redteam_origine.py', ['SEUIL', 'MARGE'])
    w('- **Ce qui se touche est joignable** (`redteam_joignable.py`, v118) : au centre de chaque élément interactif, `elementFromPoint` rend l\'élément ou un de ses descendants ; chaque gestionnaire n\'appelle que des fonctions qui existent, sur un nœud qui existe ; la dette est nommée dans `joignable-dette.json`.')
    w('- **La dalle d\'origine dans la bande haute** (`redteam_origine.py`, v118) : la couleur d\'origine, sauf si son écart au champ est sous **ΔE %s** (CIELAB) — alors la rampe de Q30 ; les cas à moins de %s du seuil ne sont jugés que sur la lisibilité.' % (OR.get('SEUIL'), OR.get('MARGE')))
    w('- **Le Zzz** (`redteam_nuit.py`, v118) : premier lancement en clair, Zzz activé ; nuit = coucher du soleil + 1 h → lever (NOAA, coordonnées du fuseau ; inconnu : 22 h – 7 h ; almanach de Paris à ± 3 min) ; aucune bascule sous les yeux, aucun fondu ; cran de nuit = neutres clairs à OKLCH L − 0,06 (± 0,006), tous les autres jetons au hex près, contraste ≥ 7 : 1.')
    w('- **Le contrat visuel** (`releve-design.py`, référence `design-reference.json`, figée le 30 sept.) : %d cibles × %d propriétés × 6 configurations ; '
      '⚠ les couleurs n\'y sont PAS comparées (%s) — elles vivent dans `PROMI-TOKENS.json` et `redteam_tokens`.' % (len(D.get('CIBLES', {})), len(D.get('PROPS', [])), ', '.join(sorted(D.get('VARIABLES', ())))))
    w('')
    w('## 5 · Ce que les juges ne portent PAS, et qu\'il faudra porter autrement')
    w('')
    w('- les deux références figées (`air-reference.json`, `design-reference.json`) photographient **l\'app**, pas une décision : elles '
      'disent « rien n\'a bougé », jamais « c\'est juste » ; ce qui est juste est dans `ETAT-30-SEPTEMBRE-2026.md` ;')
    w('- la matière d\'un monde : c\'est `banc_rendu.py` qui la juge, au pixel.')
    io.open(os.path.join(ICI, 'SPEC-JUGES.md'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
    print('écrit : SPEC-JUGES.md', len(o), 'lignes')


def _paires():
    try:
        d = json.load(open(os.path.join(ICI, 'air-reference.json')))
        return '%d paires sur %d écrans-thèmes' % (sum(len(v) for v in d.values()), len(d))
    except Exception: return 'référence absente'


if __name__ == '__main__':
    main()
