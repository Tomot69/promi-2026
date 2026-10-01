#!/usr/bin/env python3
"""
etat_generer.py — ENGENDRE « ETAT-30-SEPTEMBRE-2026.md » DEPUIS LA SOURCE VIVANTE (assainissement, lot 3, Tom, 30 sept. 2026).

Ce qui est ENGENDRÉ (jamais recopié à la main) :
  · couleurs, polices, niveaux de texte    ← PROMI-TOKENS.json (la source unique ; redteam_tokens vérifie JSON = CSS = Swift)
  · les 20 mondes, leurs noms affichés, leur accès, leur famille de semis, leurs réglages déclarés
                                           ← l'app EN MARCHE (order, WL, _mondesCercle, Toile.semisNeuf, Toile_reglages)
  · les 24 palettes et la palette par défaut ← l'app en marche (Toile.palettes, Toile.getPalette)
  · les 21 phrases des murs                 ← l'app en marche (window._murPhrases)
Ce qui est ÉCRIT (les décisions en vigueur) est tenu dans ce fichier, en clair, avec la date de chaque décision : c'est la
seule partie à relire à la main quand une décision change.

Usage : python3 etat_generer.py            (le serveur 8752 doit tourner)
"""
import json, io, os, datetime
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, 'ETAT-30-SEPTEMBRE-2026.md')
URL = 'http://127.0.0.1:8752/app.html'

VIVANT = """()=>{ const src=[...document.scripts].map(s=>s.textContent).join('\\n');
  const order=/order=\\[([^\\]]+)\\]/.exec(src)[1].replace(/['"\\s]/g,'').split(',');
  const WL=(()=>{ const m=/var WL=(\\{[^}]+\\})/.exec(src); return eval('('+m[1]+')'); })();
  const neuf={}; const t0=Toile.getTheme(); for(const m of order){ Toile.setTheme(m); neuf[m]=Toile.semisNeuf(); } Toile.setTheme(t0);
  const pals=Toile.palettes(); const P=[]; for(const k in pals) P.push({cle:k,name:pals[k].name,cols:pals[k].cols.map(c=>'#'+c.map(v=>v.toString(16).padStart(2,'0')).join('').toUpperCase())});
  const R={}; for(const m of order) R[m]=Toile_reglages(m);
  return {order, WL, cercle:window._mondesCercle, neuf, pals:P, palDefaut:Toile.getPalette(), reglages:R,
          murs:window._murPhrases||[], version:window.PROMI_VERSION}; }"""


def vivant():
    with sync_playwright() as p:
        b = p.webkit.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932})
        pg.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg.goto(URL); pg.wait_for_timeout(7000)
        d = pg.evaluate(VIVANT); b.close(); return d


def main():
    T = json.load(open(os.path.join(ICI, 'PROMI-TOKENS.json'), encoding='utf-8'))
    V = vivant()
    R = T['roles']; out = []
    w = out.append
    w('# ÉTAT AU 30 SEPTEMBRE 2026 — CE QUI EST VRAI AUJOURD\'HUI')
    w('')
    w('> **Le document de référence du portage.** Engendré par `etat_generer.py` le %s depuis la source vivante : '
      '`PROMI-TOKENS.json` et l\'app en marche (version %s). **Ne pas l\'éditer à la main** : on corrige la source, puis on relance.'
      % (datetime.date.today().isoformat(), V['version']))
    w('> Les valeurs de ce document priment sur tout autre document. `PROMI-SPECIFICATIONS.md`, `PARCOURS.md` et '
      '`MOODBOARD-VALEURS.md` sont des **archives** (valeurs antérieures au 16 septembre 2026) : ils disent la géométrie et '
      'l\'intention d\'août, jamais une couleur, une police ni un libellé à porter.')
    w('')
    w('**Ordre des sources, en cas de doute :** ce document → `PROMI-TOKENS.json` (couleurs, polices) → `CONTRAT-MONDE.md` '
      '(ce qu\'un monde doit faire) → `SPEC-JUGES.md` (les règles que les juges portent) → `CLAUDE.md` (méthode, pièges, '
      'décisions datées) → les moodboards (géométrie d\'origine) → une mesure de l\'app (jamais une référence).')
    w('')
    # ── 1 · lexique
    w('## 1 · Le lexique — ce qui s\'affiche, et sa clé interne')
    w('')
    w('Les clés internes **ne changent jamais** quand un nom affiché change (décision du 30 sept. 2026, v106).')
    w('')
    w('| Affiché | Clé interne | Genre, notes |')
    w('|---|---|---|')
    for a, c, n in [
        ('Promi', '`promi`', 'invariable : « trois Promi » — une promesse, une dalle'),
        ('Chiche', '`chiche` (`p.chiche`)', 'un défi lancé ; on LANCE un Chiche, on ne le plante pas'),
        ('**Cercle**', '`nuee` (`NUE`, `curNuee`, `.dp-nuee`…)', '**masculin** : « un Cercle », « le Cercle ». Était « Nuée » jusqu\'au 30 sept.'),
        ('**Ma Parole !**', '`ouvreCercle`, `.s2-cercle`, `isPremium`, `#plusScreen`', 'l\'offre payante. Était « Le Cercle ». Espace insécable avant « ! »'),
        ('gardé de côté', '`draft`', '« brouillon » est banni'),
        ('Toile', '`window.Toile` (promi-moteur.js)', 'le canevas des dalles, Voronoï pondéré'),
        ('Fil', '`#feedView`', 'le flux d\'activité'),
        ('Index', '`#indexSheet`', 'la liste des Promi'),
        ('Aura', '`#auraScreen`', 'l\'écran de progression (ex-« Karma »)'),
        ('Pelote', '`_aura`', 'la boule de l\'Aura — « sphère » et « Orbite » sont bannis'),
        ('Studio', '`#studioScreen`', 'le monde et la palette'),
        ('Peaufiner', '`.s2-*`, `#dpDetails`', 'le tiroir de réglages d\'une fiche'),
        ('Folio', '`#shMode [data-mode=mosaic]`', 'ce qu\'on partage de ses dalles'),
        ('Noyau', '`.kring`, `.au-nb`', 'un anneau à trois arcs'),
    ]: w('| %s | %s | %s |' % (a, c, n))
    w('')
    w('**Termes bannis** (écran, code, documents) : « tâche », « to-do », « objectif », « échéance » comme libellé, « valider », '
      '« urgent », « score », « brouillon », « Orbite », « la sphère », « Belle parole » comme bouton, « En replanter un ». '
      'On dit **tenir sa parole, tracer, planter, lancer**.')
    w('')
    # ── 2 · couleurs
    w('## 2 · Les couleurs — engendrées de `PROMI-TOKENS.json` (%s)' % T.get('genere_le', ''))
    w('')
    w('Un rôle vaut deux valeurs (mode clair · mode sombre). **Une règle CSS emploie la palette FIXE (`--c-*`), jamais un rôle** '
      '(un rôle inverserait en silence la crème et l\'encre). Le portage Swift emploie les rôles (`Promi+Design.swift`).')
    w('')
    w('| Rôle | Clair | Sombre |')
    w('|---|---|---|')
    for k, v in R.items():
        if isinstance(v, dict) and 'clair' in v: w('| `%s` | `%s` | `%s` |' % (k, v['clair'], v['sombre']))
    w('')
    w('**Les règles qui font lire ces couleurs** (décisions en vigueur) :')
    w('- **Le champ dit la nature, la ligne dit l\'état.** Champ : Promi `#82AEF8` · Chiche `#FFB8D2` · Cercle `#C9A8F5` '
      '(le lilas est le CHAMP d\'un Cercle, le violet `#291547` est ce qu\'on pose dessus). Un champ blanc n\'existe jamais.')
    w('- **Trois états, trois arcs, jamais plus** : à tenir `#DD4D23` · en cours `#291547` · tenu `#00341A`. Un état suit '
      'CE QUI EST PEINT SOUS LUI : sur la terre `#2B1020` d\'une fiche tenue, le tenu passe à l\'amande `#8FE08F` ; sur un fond clair il reste `#00341A`.')
    w('- **L\'amande `#8FE08F`** ne peint que la célébration (la seconde dalle qui apparaît, se décale, disparaît) et la mention « TENU(E) ».')
    w('- **Tout suit le Studio (monde et palette), sauf l\'Aura** (v34) : la Pelote et « Ce que tu as tenu » gardent le monde de plantation. '
      'Les ÉTATS ne suivent jamais rien.')
    w('- **Ingénu, la palette par défaut, dit la nature** (v17) : sous Ingénu seulement, un Promi est bleu, un Chiche rose, un Cercle lilas.')
    w('- **Un trait sur un aplat coloré se juge en ΔE (plancher 15), du texte sur un fond en luminance (seuil 42).**')
    w('')
    # ── 3 · polices
    w('## 3 · Les polices et les niveaux de texte — trois polices, cinq faces')
    w('')
    w('| Famille | Pile CSS | Fichier | Licence |')
    w('|---|---|---|---|')
    for k, v in T['polices'].items(): w('| %s | `%s` | %s | %s |' % (k, v.get('css', ''), v.get('fichier', ''), v.get('licence', '')))
    w('')
    w('| Niveau | Famille | Graisse | Taille | Capitales | Opacité |')
    w('|---|---|---|---|---|---|')
    for k, v in T['niveaux'].items(): w('| %s | %s | %s | %s px | %s | %s |' % (k, v['famille'], v['poids'], v['taille'], 'oui' if v['capitales'] else 'non', v['opacite']))
    w('')
    w('Cinq faces embarquées et cinq seulement : **Gilbert 700 · Atkinson 400 / 500 / 700 · PromiLate 400**. Une graisse absente '
      'se reporte (table de `CLAUDE.md` §6). PromiLate n\'a ni « ! » ni espace insécable : ils viennent de Gilbert. '
      'Rien sous 12 px ; aucune opacité sous 72 % sur un texte à lire. ⚠ Les tailles ont grandi en v96 (`size-adjust:112 %`) : '
      'l\'air se mesure à l\'ENCRE, jamais à la boîte.')
    w('')
    # ── 4 · mondes
    w('## 4 · Les %d mondes — engendrés de l\'app en marche' % len(V['order']))
    w('')
    w('Dans l\'ordre du Studio. **« Semis »** : *constant* = les huit anciens (≈ 68 cellules, les paroles colorent des cellules) ; '
      '*grandit* = la Toile est faite de ses seules paroles (v35). Le semis est amorcé par la clé de la Toile (assainissement, 30 sept.) : '
      'même Toile à chaque ouverture. **Réglages** : ce que le monde déclare au moteur (`REGLAGES_MONDE`, promi-moteur.js).')
    w('')
    w('| # | Affiché | Clé | Accès | Semis | Réglages déclarés |')
    w('|---|---|---|---|---|---|')
    for i, m in enumerate(V['order'], 1):
        rg = V['reglages'].get(m) or {}
        w('| %d | %s | `%s` | %s | %s | %s |' % (i, V['WL'].get(m, m), m, 'Ma Parole !' if V['cercle'].get(m) else 'gratuit',
                                                'grandit' if V['neuf'].get(m) else 'constant',
                                                ', '.join('`%s`' % (k if v in (1, True) else '%s %s' % (k, json.dumps(v))) for k, v in rg.items()) or '—'))
    w('')
    w('Le contrat d\'un monde (ce qu\'il reçoit, ce qu\'il doit rendre, son budget) : `CONTRAT-MONDE.md`. Ce qui juge un monde au pixel : '
      '`banc_rendu.py` (20 mondes × Toile + 4 dalles × 3 tailles, référence `banc-rendu/ref/`). Éclats n\'existe plus (retiré le 30 sept.).')
    w('')
    # ── 5 · palettes
    w('## 5 · Les %d palettes du Studio — engendrées de l\'app en marche' % len(V['pals']))
    w('')
    d0 = next((p['name'] for p in V['pals'] if p['cle'] == V['palDefaut']), V['palDefaut'])
    w('Palette par défaut : **%s** (clé `%s`). Quatre tons, dans l\'ordre de leur poids (≈ 34 · 28 · 23 · 15 %%).' % (d0, V['palDefaut']))
    w('')
    w('| Nom | Clé | Tons |')
    w('|---|---|---|')
    for p in V['pals']: w('| %s | `%s` | %s |' % (p['name'], p['cle'], ' · '.join('`%s`' % c for c in p['cols'])))
    w('')
    # ── 6 · l'offre
    w('## 6 · Ma Parole ! — l\'offre')
    w('')
    w('- **Prix** : 39 € / an (soit 3,25 €/mois) · ou 5,99 € par mois · essai 14 jours · un monde à l\'unité 1 €. Sans engagement.')
    w('- **L\'écran qui vend** : titre « MA PAROLE ! », sous-titre « Retourne ta Toile », bouton principal « Essayer 14 jours », '
      'option « Bon, allez d\'accord — 39 € / an », en petit « ou 5,99 € par mois ».')
    w('- **Réglages** : la porte « Ma Parole ! » ouvre l\'offre (ce n\'est pas un mur) ; au payé « Tu es Membre Ma Parole ! », sans lien.')
    w('- **Ce qu\'elle ouvre** : l\'autre moitié de la Toile (ce qu\'on te tient), la récurrence, le rappel à l\'heure choisie, '
      'l\'importance, la mémoire des paroles en l\'air, la couleur de la dalle, douze mondes, les Cercles illimités.')
    w('- **Les murs** : un réglage réservé est flouté à **4,8 px**, sans explication (sauf le Studio, qui garde les siens). '
      'Au toucher, une phrase paraît au centre du mur (Gilbert, encre `#201908` sur clair, crème `#F7F0DE` sur sombre, ≤ 3 lignes, '
      '1,4 s + 60 ms par caractère, entre 3 et 5,5 s). La toute première fois, l\'offre s\'ouvre à la fin de la lecture ; ensuite, '
      'un toucher pendant la lecture l\'ouvre. Compteur global, remis à zéro après 14 jours sans mur.')
    w('- **Les %d phrases, dans l\'ordre** (puis au hasard sans répéter la précédente) :' % len(V['murs']))
    for i, ph in enumerate(V['murs'], 1): w('  %d. %s' % (i, ph))
    w('')
    # ── 7 · notifications
    w('## 7 · Les notifications (v109–v110)')
    w('')
    w('- Jamais au lancement. « **Je te le rappelle ?** · oui · pas besoin » paraît 1,9 s après la plantation d\'une parole DATÉE '
      '(sous le plateau de l\'accueil) ; la permission n\'est demandée qu\'après « oui ». Deux « pas besoin » d\'affilée, puis plus rien. '
      'Elle part seule au bout de 12 s. Un « oui » vaut pour toutes les paroles datées.')
    w('- **Gratuit** : le mot de la veille d\'une parole datée. **Ma Parole !** : la mémoire des paroles en l\'air (une par semaine au plus), '
      'le choix de l\'heure (8 h · midi · 19 h ; 19 h au gratuit). **Firebase** : l\'envoi app fermée, tout ce qui vient d\'une autre personne.')
    w('- **Les mots** : « Demain, c\'est « {titre} ». » · « « {titre} » — Tu as promis ça à {Prénom}. Demain. » · « Ton Chiche à {Prénom} arrive demain. » · '
      '« « {titre} » — C\'est aujourd\'hui. » (à l\'heure choisie, si la veille était passée à la plantation) · « « {titre} » flotte toujours. Un de ces jours ? »')
    w('- **Rien quand la date est passée.** Une notification par jour au plus. Aucune qui reproche, ni série, ni score.')
    w('')
    # ── 8 · invariants
    w('## 8 · Les invariants du dessin — ce qui ne se négocie pas')
    w('')
    for x in [
        'Une dalle est TOUJOURS la vraie dalle du moteur (`Toile.dalleTrame`), rendue à sa taille finale et posée 1 : 1 — jamais une image découpée, redimensionnée, un polygone, une photo.',
        'La bande haute d\'une fiche porte la NATURE (et teinte sa dalle sur la rampe de la nature, Q30) ; nulle part ailleurs une dalle n\'est teintée par sa nature (hors Ingénu).',
        'Un anneau (Noyau) a trois arcs au plus, jours de 3 px d\'arc, filet crème de 1 px sur le seul bord extérieur quand il est posé sur du sombre.',
        'Les composants communs sont identiques partout : le geste (118 px, deux points, un trait), Peaufiner (62 px), « ✕ FERMER » en haut à droite, le plateau (342 × 60, trait 2, rayon 30).',
        'Grammaire des contours : trait 2 px, couleur du corps, rayon = hauteur ÷ 2 jusqu\'à 94,5 px de haut, 30 au-delà.',
        'L\'air entre deux textes ne se resserre jamais ; il se mesure à l\'encre.',
        'Rien ne paraît une fraction de seconde (ouverture, fermeture, plantation).',
        'Un mouvement se calcule sur le temps réel (sauf Houle, par image, par décision).',
    ]: w('- ' + x)
    w('')
    w('---')
    w('*Engendré. Pour corriger : la source (`PROMI-TOKENS.json`, l\'app, ou la partie écrite de `etat_generer.py`), puis relancer.*')
    io.open(SORTIE, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('écrit :', SORTIE, len(out), 'lignes')


if __name__ == '__main__':
    main()
