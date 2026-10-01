#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_tokens.py — LE JEU FAIT AUTORITÉ, ET AUCUNE VUE N'APPELLE UNE COULEUR NI UNE POLICE EN DUR.

C'est le contrôle du lot du 16 septembre 2026 (Tom) : « Centralise tout : un jeu de couleurs
nommées avec variantes claire et sombre, et une extension de styles pour qu'aucune vue n'appelle
une police ou un hexadécimal en dur. C'est ce qui servira au portage Swift. »

Sept contrôles, tous lus dans les fichiers — aucun navigateur, donc aucun flottement :

  1 · les quatre valeurs décidées par Tom sont celles du jeu       (elles sont ÉCRITES ICI, §7)
  2 · les deux couleurs entrantes sont déclarées
  3 · aucune couleur en dur dans les <style>            (hors le bloc de tokens et les commentaires)
  4 · aucune police d'origine appelée en dur             (Fraunces reste, par les titres — var(--f-titre))
  5 · le bloc de tokens de app.html et PROMI-TOKENS.json disent la même chose
  6 · les faces annoncées par le jeu sont embarquées en @font-face
  7 · l'extension Swift est à jour avec le jeu

⚠ §7 de CLAUDE.md : un juge qui lit la valeur qu'il vérifie ne vérifie rien. Les quatre valeurs
  décidées et les deux entrantes sont donc écrites EN DUR ci-dessous, avec la décision qui les fixe ;
  le juge vérifie que l'app les respecte — jamais l'inverse.
"""
import io, json, re, sys

RACINE = '/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'

# ── LA DÉCISION, ÉCRITE EN DUR ───────────────────────────────────────────────────────────
#  ⚑ REPRIS AU NIVEAU DE LA DÉCISION le 17 septembre 2026 (§7). La planche des correspondances
#    et le PDF des vingt palettes ont remplacé les valeurs du 16 septembre ; le juge porte les
#    NOUVELLES, avec la phrase de Tom qui fixe chacune. Version d'avant :
#    sauvegardes/redteam_tokens-avant-IDENTITE.py
DECIDE = {
    # les trois natures — « le champ dit la nature », et les trois sont des PASTELS
    'promi'     : '#82AEF8',   # planche des correspondances, « champ — une promesse »
    'chiche'    : '#FFB8D2',   # planche, « champ — un défi lancé »
    'nuee'      : '#C9A8F5',   # planche, « champ — un groupe ». ⚑ 17 sept. : le lilas est le CHAMP,
                               #   le violet #291547 est « trait et texte sur champ lilas ».
                               #   « Les trois natures sont des pastels : la Nuée ne peut pas être
                               #    la seule avec un champ sombre. » (Tom)
    # les états — « la ligne dit l'état »
    'a-tenir'   : '#DD4D23',   # inchangé depuis le 16 septembre
    'tenu'      : '#8FE08F',   # planche, « bande pleine en pied — amande saturée »
    'en-cours'  : '#FFD447',   # planche, « ligne, deux traits » — le périwinkle passe au jaune
    # les fonds et les surfaces
    'fond-clair': '#F7F0DE',   # « le clair devient #F7F0DE — fond du mode clair »
    'fond-sombre': '#201908',  # « le fond du mode sombre devient ce brun. C'est l'encre du mode clair »
    'exception' : '#00341A',   # « le vert #00341A comme surface d'exception »
}
# ⚑ LES ENCRES DE NATURE ET D'ÉTAT (Tom, 17 septembre 2026) — elles BASCULENT avec le mode :
#   sombre = le pastel, clair = le compagnon sombre. Dérivées de la paire de la planche
#   (lilas → violet : ΔL −61,8, chroma ×0,83, teinte tenue).
ENCRES = {
    '--c-bleu45-txt'     : ('#022140', '#82AEF8'),   # (clair, sombre)
    '--c-framboise54-txt': ('#3D0F23', '#FFB8D2'),
    '--c-mauve77-txt'    : ('#291547', '#C9A8F5'),
    # « la couleur d'état vit dans la ligne, pas dans le mot » : sur le corps clair, le mot d'état
    # passe à l'encre ; le mode sombre garde la couleur d'état.
    '--c-menthe82-txt'   : ('#201908', '#8FE08F'),
    '--c-bleu68-txt'     : ('#201908', '#FFD447'),
    '--c-orange53-txt'   : ('#201908', '#DD4D23'),
}
# les six faces que le jeu annonce
FACES_ATTENDUES = {('gilbert', 700), ('atkinson', 400), ('atkinson', 500), ('atkinson', 700)}
# ce qui a le droit de rester écrit en clair : les palettes du moteur (§9, on n'y touche pas),
# les couleurs d'une marque tierce, et les gris purs — dette d'avant ce lot, pas son objet.
TOLERE = re.compile(r'(PALS|SIGNAL|MOODS|NUEDALLE)\s*=')


def lire(nom):
    return io.open(RACINE + '/' + nom, encoding='utf-8').read()


def sans_base64(S):
    return re.sub(r'base64,[A-Za-z0-9+/=]+', 'base64,X', S)


def controles():
    S = sans_base64(lire('app.html'))
    J = json.load(io.open(RACINE + '/PROMI-TOKENS.json', encoding='utf-8'))
    SW = lire('Promi+Design.swift')
    R, roles = [], J['roles']

    # 1 · les quatre valeurs décidées
    cas = [('promi', roles['promi']['clair']),
           ('chiche', roles['chiche']['clair']),
           ('nuee', roles['nuee']['clair']),
           ('a-tenir', roles['a-tenir']['clair']),
           ('tenu', roles['tenu']['clair']),
           ('en-cours', roles['en-cours']['clair']),
           ('fond-clair', roles['fond']['clair']),
           ('fond-sombre', roles['fond']['sombre']),
           ('exception', roles['exception']['clair'])]
    for nom, valeur in cas:
        R.append((f"la valeur décidée « {nom} » vaut {DECIDE[nom]}",
                  valeur.upper() == DECIDE[nom], f"le jeu dit {valeur}"))
    # ⚑ 17 sept. : les encres de nature et d'état basculent, et dans LE BON SENS.
    import re as _re
    _i = S.find('<style id="lot-TOKENS-css">'); _j = S.find('</style>', _i)
    _bloc = S[_i:_j]
    _rac = _re.search(r':root\{(.*?)\}', _bloc, _re.S).group(1)
    _cl  = _re.search(r'#device\.light[^{]*\{(.*?)\}', _bloc, _re.S).group(1)
    _som = dict(_re.findall(r'(--c-[a-z0-9-]+):(#[0-9A-Fa-f]{6})', _rac))
    _lum = dict(_re.findall(r'(--c-[a-z0-9-]+):(#[0-9A-Fa-f]{6})', _cl))
    for jeton,(cl,som) in ENCRES.items():
        a_som = (_som.get(jeton) or '').upper()
        R.append((f"l'encre {jeton} vaut {som} en sombre",
                  a_som == som.upper(), f"le jeu dit {a_som or '(absent)'}"))
        a_cla = (_lum.get(jeton) or '').upper()
        R.append((f"l'encre {jeton} vaut {cl} en clair",
                  a_cla == cl.upper(), f"le mode clair dit {a_cla or '(absent)'}"))

    # 2 · l'encre du mode clair EST le fond du mode sombre, et réciproquement (« les deux modes s'échangent »)
    R.append(("les deux modes s'échangent : encre claire = fond sombre",
              roles['encre']['clair'].upper() == roles['fond']['sombre'].upper(),
              f"{roles['encre']['clair']} vs {roles['fond']['sombre']}"))
    R.append(("les deux modes s'échangent : encre sombre = fond clair",
              roles['encre']['sombre'].upper() == roles['fond']['clair'].upper(),
              f"{roles['encre']['sombre']} vs {roles['fond']['clair']}"))

    # 3 · aucune couleur en dur dans les <style>
    dur = []
    for m in re.finditer(r'<style([^>]*)>(.*?)</style>', S, re.S):
        if 'lot-TOKENS-css' in m.group(1):
            continue
        corps = re.sub(r'/\*.*?\*/', '', m.group(2), flags=re.S)
        for mm in re.finditer(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+[^)]*\)', corps):
            dur.append(mm.group(0))
    R.append(("aucune couleur en dur dans les <style>", not dur,
              f"{len(dur)} restante(s) : {dur[:5]}"))

    # 4 · aucune police d'origine appelée en dur
    T = re.sub(r'@font-face\{[^}]*\}', '', S)
    pol = []
    for mm in re.finditer(r"""font-family['"]?\s*[:=]\s*['"]?([^;}'"),]+)""", T):
        tete = mm.group(1).strip().strip('\'"').lower()
        if tete in ('fraunces', 'bricolage', 'apfel', 'apfelmid', 'bricolage grotesque'):
            pol.append(mm.group(0)[:50])
    R.append(("aucune police appelée en dur (tout passe par --f-*)", not pol,
              f"{len(pol)} restante(s) : {pol[:3]}"))

    # 5 · le bloc de tokens et le JSON disent la même chose
    bloc = re.search(r'<style id="lot-TOKENS-css">(.*?)</style>', S, re.S)
    ecarts = []
    if not bloc:
        ecarts.append('bloc absent')
    else:
        b = bloc.group(1)
        for nom, v in roles.items():
            if f"--p-{nom}:{v['sombre']}" not in b:
                ecarts.append(f"--p-{nom} sombre")
            if f"--p-{nom}:{v['clair']}" not in b:
                ecarts.append(f"--p-{nom} clair")
        for var, h in J['palette_fixe'].items():
            if f"{var}:{h}" not in b:
                ecarts.append(var)
    R.append(("le bloc de tokens et PROMI-TOKENS.json sont d'accord", not ecarts,
              f"{len(ecarts)} écart(s) : {ecarts[:5]}"))

    # 6 · les faces annoncées sont embarquées
    faces = set()
    for m in re.finditer(r'@font-face\{([^}]*)\}', S):
        d = m.group(1)
        fam = re.search(r"font-family:\s*['\"]?([A-Za-z][A-Za-z ]*?)['\"]?\s*;", d)
        wt = re.search(r'font-weight:\s*(\d+)', d)
        if fam:
            faces.add((fam.group(1).strip().lower(), int(wt.group(1)) if wt else 400))
    manque = FACES_ATTENDUES - faces
    R.append(("les faces neuves sont embarquées (Gilbert 700 · Atkinson 400/500/700)",
              not manque, f"manque {sorted(manque)}"))

    # 7 · l'extension Swift est à jour
    swi = []
    for nom, v in roles.items():
        for val in {v['clair'], v['sombre']}:
            h = val.lstrip('#')
            r, g, bb = (int(h[i:i+2], 16) for i in (0, 2, 4))
            if f"{r/255:.4f}" not in SW:
                swi.append(nom)
                break
    R.append(("l'extension Swift porte les mêmes rôles", not swi,
              f"{len(swi)} rôle(s) absent(s) : {swi[:4]}"))
    for niveau in J['niveaux']:
        n = niveau.split('-')[0] + ''.join(x.capitalize() for x in niveau.split('-')[1:])
        R.append((f"l'extension Swift porte le niveau « {niveau} »",
                  f"static let {n} = Font.custom" in SW, "absent"))
    return R


if __name__ == '__main__':
    R = controles()
    ok = 0
    for lib, bon, detail in R:
        print(('  ✓ ' if bon else '  ✗ ') + lib + ('' if bon else '   → ' + detail))
        ok += bon
    print(f"\n{ok}/{len(R)}")
    sys.exit(0 if ok == len(R) else 1)
