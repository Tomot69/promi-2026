# -*- coding: utf-8 -*-
"""LE JEU DE COULEURS NOMMÉES — source unique. Rôles d'abord, variantes ensuite.
   Deux variantes par rôle quand le rôle dépend du mode ; une seule sinon."""
import sys; sys.path.insert(0,'scratchpad')
from couleurs_lab import *
from table_palette import table as _bascule

B = _bascule()
def nv(h):
    """la valeur d'APRÈS pour une couleur d'AVANT"""
    return B.get(h.upper(), h.upper())

# ⚑ deux ajustements EXPLICITES, pas des transports : le fond sombre devient brun, donc les
#    deux corps bruns sombres devaient s'en écarter pour rester lisibles (§7, plancher ΔE 15).
B['#2E1C13'] = '#401E17'    # corps sombre « à tenir »  (ΔE au fond : 15,1 avant → 16,6)
B['#2A1912'] = '#3A1B15'    # corps sombre gardé de côté (ΔE au fond : 13,3 avant → 14,7)
#    Et le corps sombre d'une carte de Nuée : le mauve passant de L*51 à L*12, le corps
#    (#271B45, L*13,5) tombait à ΔE 6,2 de son propre champ — redteam_champ l'a vu sur la
#    carte d'Index et sur le bandeau du Fil, dans les deux thèmes. Descendre en clarté ne
#    suffit pas (ΔE 13,7 au mieux à teinte égale) : il faut SOURDIR. On prend donc la valeur
#    que CLAUDE.md §3 donne déjà au corps sombre d'une Nuée — #1B1426, C* 14 contre 36 pour
#    le champ : ΔE 22,4 du champ, 22,9 du fond brun. Une seule valeur pour un seul rôle.
B['#271B45'] = '#1B1426'

# ── LES RÔLES ────────────────────────────────────────────────────────────────────
# nom : (valeur en mode CLAIR, valeur en mode SOMBRE)  ·  une seule valeur = les deux modes
ROLES = {
  # les deux surfaces, et l'encre : les deux modes s'échangent (Tom, 16 sept. 2026)
  'fond'            : ('#F7F0DE', '#201908'),
  'encre'           : ('#201908', '#F7F0DE'),
  'surface'         : (nv('#F7F3EA'), nv('#17181F')),
  'surface-haute'   : (nv('#FDFBF6'), nv('#1C1D22')),
  'sous-texte'      : (nv('#6E685C'), nv('#7E83A0')),
  'grip'            : (nv('#C7C0B2'), nv('#3A3C4C')),
  # la surface d'exception (entrante)
  'exception'       : '#00341A',
  # les natures — la bande haute d'une fiche, l'accent d'une carte
  'promi'           : '#3A54FF',
  'chiche'          : '#FA2258',
  'nuee'            : '#291547',
  'garde-de-cote'   : nv('#B8552B'),
  # les états — ils vivent dans la LIGNE (§3)
  'tenu'            : '#2BE88C',
  'a-tenir'         : '#DD4D23',
  'en-cours'        : '#8FA0FF',
  'encre-sur-tenu'  : '#06231A',
  # les teintes claires des natures (le trait sur un champ plein, §2.1 bis)
  'promi-clair'     : '#CBAAFF',
  'chiche-clair'    : nv('#FFC0A8'),
  'nuee-clair'      : '#E4CEFD',
  'lilas'           : '#E4CEFD',
  'mauve-clair'     : '#D0B0FF',
  # les corps de fiche, par nature
  'corps-promi'     : ('#DCE1FF', '#12142A'),
  'corps-chiche'    : ('#FCE9EE', '#25101A'),
  'corps-nuee'      : ('#F3E9FE', '#1B1426'),
  'corps-tenu'      : ('#AEE5CE', '#0C2B1F'),
  'corps-a-tenir'   : (nv('#F1DBCF'), B['#2E1C13']),
  'corps-garde'     : (nv('#F1DBCF'), B['#2A1912']),
  # les absolus
  'blanc'           : '#FFFFFF',
  'noir'            : '#000000',
}

# ── LES NIVEAUX DE TEXTE ─────────────────────────────────────────────────────────
#  titre = la police actuelle (Fraunces), elle sera remplacée plus tard (Tom)
TYPO = {
  'titre'      : dict(famille='titre',     poids=600, taille=36, capitales=False, opacite=1.0),
  'sous-titre' : dict(famille='libelle',   poids=700, taille=22, capitales=True,  opacite=1.0),
  'texte'      : dict(famille='texte',     poids=400, taille=16, capitales=False, opacite=1.0),
  'accent'     : dict(famille='texte',     poids=700, taille=16, capitales=False, opacite=1.0),
  'petit'      : dict(famille='texte',     poids=400, taille=14, capitales=False, opacite=1.0),
  'meta'       : dict(famille='texte',     poids=400, taille=13, capitales=False, opacite=0.65),
  'libelle'    : dict(famille='libelle',   poids=700, taille=15, capitales=True,  opacite=1.0),
}
FAMILLES = {
  'titre'   : dict(css="Fraunces,Georgia,serif",        fichier="Fraunces (embarquée)", licence="—"),
  'libelle' : dict(css="Gilbert,Bricolage,system-ui,sans-serif", fichier="Gilbert-Bold.woff2",
                   licence="CC BY-SA 4.0 — Ogilvy & Mather / Type With Pride. Crédit obligatoire, glyphes non modifiables."),
  'texte'   : dict(css="Atkinson,Apfel,system-ui,sans-serif", fichier="Atkinson-{Regular,Medium,Bold}.woff2",
                   licence="SIL Open Font License 1.1 — Braille Institute of America."),
}

def clair(v): return v[0] if isinstance(v,tuple) else v
def sombre(v): return v[1] if isinstance(v,tuple) else v
