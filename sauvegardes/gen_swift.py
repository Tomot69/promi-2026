# -*- coding: utf-8 -*-
"""L'EXTENSION DE STYLES POUR LE PORTAGE — engendrée depuis PROMI-TOKENS.json, jamais écrite à la main."""
import json, io, re
J = json.load(io.open('PROMI-TOKENS.json', encoding='utf-8'))

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
L.append("// régénérer (scratchpad/gen_swift.py). Aucune vue n'écrit une couleur ni une police :")
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
        L.append(f"        /// clair {v['clair']} · sombre {v['sombre']}")
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
    n = camel(var.replace('--c-', ''))
    L.append(f"        static let {n} = {couleur(h)}   // {h}")
L.append("    }")
L.append("}")
io.open('Promi+Design.swift', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print("Promi+Design.swift écrit :", len(L), "lignes ·",
      len(J['roles']), "rôles ·", len(J['niveaux']), "niveaux ·", len(J['palette_fixe']), "couleurs fixes")
