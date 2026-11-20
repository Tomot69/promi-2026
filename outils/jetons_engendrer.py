# -*- coding: utf-8 -*-
"""v207 (Tom, 17 nov. 2026 : « les jetons : UNE source, le JSON ; le CSS et le TypeScript en sont GÉNÉRÉS par un outil rangé dans le dépôt ; plus aucune
retouche à la main d'un fichier généré ») — LE GÉNÉRATEUR DES JETONS. Une source : PROMI-TOKENS.json. Trois sorties, jamais retouchées à la main :
  · Promi+Design.swift          l'extension de styles (était scratchpad/gen_swift.py) ;
  · promi/src/design/jetons.css  les variables de la vraie app : la palette fixe (--c-*), les rôles (--p-*) en clair et en sombre, les sept niveaux ;
  · promi/src/design/jetons.ts   les mêmes valeurs, typées, pour le TypeScript strict de la vraie app.
Le bloc `lot-TOKENS-css` du prototype n'est PAS réécrit (CLAUDE.md §9) : `redteam_tokens` vérifie qu'il dit la même chose que le JSON.
python3 outils/jetons_engendrer.py [--verifie]   (--verifie : n'écrit rien, rougit si une sortie diffère de ce qu'elle serait)"""
import json, io, re, sys, collections
J = json.load(io.open('PROMI-TOKENS.json', encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
VERIFIE = '--verifie' in sys.argv
SORTIES = {}

def camel(s):
    p = re.split(r'[-_]', s)
    return p[0] + ''.join(x.capitalize() for x in p[1:])

def couleur(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return f"Color(red: {r/255:.4f}, green: {g/255:.4f}, blue: {b/255:.4f})"

L = []
L.append("// Promi+Design.swift — LE JEU DE COULEURS ET DE POLICES DE PROMI.")
L.append("//")
L.append("// Engendré depuis PROMI-TOKENS.json le " + J['genere_le'] + ". Ne pas modifier à la main :")
L.append("// régénérer (outils/jetons_engendrer.py). Aucune vue n'écrit une couleur ni une police :")
L.append("// elles passent toutes par ce fichier, comme dans le prototype HTML.")
L.append("//")
L.append("// POLICES")
for k, v in J['polices'].items():
    L.append(f"//   {k:8} {v['fichier']}")
    L.append(f"//            {v['licence']}")
L.append("")
L.append("import SwiftUI")
L.append("")
L.append("// MARK: - Les rôles. Ils basculent avec le mode ; c'est ce qu'une vue emploie.")
L.append("extension Color {")
L.append("    enum Promi {")
for nom, v in J['roles'].items():
    n = camel(nom)
    if v['clair'] == v['sombre']:
        L.append(f"        /// {v['clair']}")
        L.append(f"        static let {n} = {couleur(v['clair'])}")
    else:
        L.append(f"        /// clair {v['clair']} · sombre {v['sombre']}" + (f" ({v['note']})" if v.get('note') else ''))
        L.append(f"        static func {n}(_ s: ColorScheme) -> Color {{")
        L.append(f"            s == .dark ? {couleur(v['sombre'])} : {couleur(v['clair'])}")
        L.append("        }")
L.append("    }")
L.append("}")
L.append("")
L.append("// MARK: - Les niveaux de texte. Un texte de l'app est toujours l'un des sept.")
L.append("extension Font {")
L.append("    enum Promi {")
NOMFACE = {'titre': '\"Fraunces\"', 'libelle': '\"Gilbert-Bold\"', 'texte': '\"AtkinsonHyperlegibleNext\"'}
for nom, d in J['niveaux'].items():
    n = camel(nom)
    L.append(f"        /// {d['taille']} pt · graisse {d['poids']}" +
             (" · CAPITALES" if d['capitales'] else "") +
             (f" · opacité {d['opacite']}" if d['opacite'] < 1 else ""))
    L.append(f"        static let {n} = Font.custom({NOMFACE[d['famille']]}, size: {d['taille']})")
L.append("        /// PromiLate — titres d'écran, mot-marque, phrases d'action du trait. Une seule graisse.")
L.append("        static func marque(_ taille: CGFloat) -> Font { Font.custom(\"PromiLate-Regular\", size: taille) }")
L.append("    }")
L.append("}")
L.append("")
L.append("// MARK: - Le style complet d'un niveau : la police, les capitales, l'opacité.")
L.append("struct NiveauPromi: ViewModifier {")
L.append("    let police: Font")
L.append("    let capitales: Bool")
L.append("    let opacite: Double")
L.append("    func body(content: Content) -> some View {")
L.append("        content.font(police)")
L.append("            .textCase(capitales ? .uppercase : nil)")
L.append("            .opacity(opacite)")
L.append("    }")
L.append("}")
L.append("")
L.append("extension View {")
for nom, d in J['niveaux'].items():
    n = camel(nom)
    L.append(f"    func promi{n[0].upper() + n[1:]}() -> some View {{")
    L.append(f"        modifier(NiveauPromi(police: .Promi.{n}, capitales: {str(d['capitales']).lower()}, opacite: {d['opacite']}))")
    L.append("    }")
L.append("}")
L.append("")
L.append("// MARK: - La palette FIXE. Une valeur par couleur, elle ne bascule jamais.")
L.append("// Une vue n'y touche pas : elle sert aux rôles ci-dessus et au report d'écrans")
L.append("// que le prototype peint encore avec une nuance sans rôle nommé.")
L.append("extension Color {")
L.append("    enum PalettePromi {")
for var, h in sorted(J['palette_fixe'].items()):
    n = J.get('noms_swift', {}).get(var) or camel(var.replace('--c-', ''))
    note = J.get('notes_palette', {}).get(var)
    L.append(f"        static let {n} = {couleur(h)}   // {h}" + ((' (' + note + ')') if note and var == '--c-cobalt50' else ((' — ' + note) if note else '')))
L.append("    }")
L.append("}")
SORTIES['Promi+Design.swift'] = '\n'.join(L) + '\n'
# ── le CSS de la vraie app : la palette fixe, les rôles (clair par défaut, sombre sous [data-theme="sombre"]), les niveaux ──
C = ['/* promi/src/design/jetons.css — GÉNÉRÉ depuis PROMI-TOKENS.json par outils/jetons_engendrer.py. Ne pas modifier à la main. */', ':root{']
C += ['  %s:%s;' % (k, v) for k, v in J['palette_fixe'].items()]
C += ['  --f-%s:%s;' % (k, v['css']) for k, v in J['polices'].items()]   # L0 : les familles, comme dans le prototype (lot-TOKENS-css)
C += ['  --p-%s:%s;' % (k, v['clair']) for k, v in J['roles'].items()]
M = J.get('mise_en_page')
if M:   # L0 (§2) : la grille et les ancrages — calculés depuis les cotes du prototype et les zones sûres de l'écran
    C += ['  --ref-largeur:%dpx;' % M['reference']['largeur'], '  --ref-hauteur:%dpx;' % M['reference']['hauteur'],
          '  --marge-g:calc(%dpx + env(safe-area-inset-left, 0px));' % M['marge_laterale'], '  --marge-d:calc(%dpx + env(safe-area-inset-right, 0px));' % M['marge_laterale'],
          '  --ancre-haut:max(calc(env(safe-area-inset-top, 0px) - %dpx), %dpx);' % (M['haut']['retrait_zone_sure'], M['haut']['cote_prototype'] + M['haut']['decalage_app']),
          '  --ancre-bas:max(env(safe-area-inset-bottom, 0px), %dpx);' % M['bas']['marge_prototype']]
C += ['}', '[data-theme="sombre"]{'] + ['  --p-%s:%s;' % (k, v['sombre']) for k, v in J['roles'].items()] + ['}']
for nom, d in J['niveaux'].items():
    C.append('.t-%s{font-family:var(--f-%s);font-weight:%s;font-size:%spx;%s%s}' % (nom, d['famille'], d['poids'], d['taille'], 'text-transform:uppercase;' if d['capitales'] else '', ('opacity:%s;' % d['opacite']) if d['opacite'] < 1 else ''))
SORTIES['promi/src/design/jetons.css'] = '\n'.join(C) + '\n'
# ── le TypeScript de la vraie app ──
T = ['// promi/src/design/jetons.ts — GÉNÉRÉ depuis PROMI-TOKENS.json par outils/jetons_engendrer.py. Ne pas modifier à la main.', '']
T.append('export const palette = ' + json.dumps(collections.OrderedDict((camel(k.replace('--c-', '')), v) for k, v in J['palette_fixe'].items()), ensure_ascii=False, indent=2) + ' as const;')
T.append('export type CouleurFixe = keyof typeof palette;')
T.append('export const familles = ' + json.dumps(collections.OrderedDict((k, v['css']) for k, v in J['polices'].items()), ensure_ascii=False, indent=2) + ' as const;')
T.append('export const roles = ' + json.dumps(collections.OrderedDict((camel(k), {'clair': v['clair'], 'sombre': v['sombre']}) for k, v in J['roles'].items()), ensure_ascii=False, indent=2) + ' as const;')
T.append('export type Role = keyof typeof roles;')
T.append('export const niveaux = ' + json.dumps(collections.OrderedDict((camel(k), v) for k, v in J['niveaux'].items()), ensure_ascii=False, indent=2) + ' as const;')
T.append('export type Niveau = keyof typeof niveaux;')
if J.get('mise_en_page'): T.append('export const miseEnPage = ' + json.dumps(collections.OrderedDict((k, v) for k, v in J['mise_en_page'].items() if k != 'note'), ensure_ascii=False, indent=2) + ' as const;')
SORTIES['promi/src/design/jetons.ts'] = '\n'.join(T) + '\n'
ecarts = 0
for chemin, texte in SORTIES.items():
    try: avant = io.open(chemin, encoding='utf-8').read()
    except FileNotFoundError: avant = None
    if VERIFIE:
        if avant != texte: ecarts += 1; print('✗', chemin, 'diffère de ce que le JSON engendre')
        else: print('✓', chemin)
    elif avant != texte:
        io.open(chemin, 'w', encoding='utf-8').write(texte); print('écrit :', chemin)
    else: print('inchangé :', chemin)
print(len(J['roles']), 'rôles ·', len(J['niveaux']), 'niveaux ·', len(J['palette_fixe']), 'couleurs fixes')
sys.exit(1 if ecarts else 0)
