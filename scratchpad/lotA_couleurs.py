# -*- coding: utf-8 -*-
"""LOT A — LA PALETTE v7 (moodboard des correspondances v7 + décisions Tom du 20 sept. 2026).

  · l'encre du mode clair est ARRÊTÉE à #201908 — le principe d'échange de la v4 est abandonné :
    le fond du mode sombre descend à #100D0B, l'encre ne bouge pas.
  · les trois bruns s'étagent : encre #201908 (L* 9,2) · brun encre #43291C (19,5) · brun surface #6B4630 (33,4)
  · « en cours » = #291547 · « tenu » = #00341A — et chacun gagne SA valeur claire pour le mode sombre :
    l'amande #8FE08F pour le tenu (elle le faisait déjà), le jaune #FFD447 pour l'en cours.
    Ce n'est pas une invention : c'est, dans les deux cas, LA VALEUR QUE L'ÉTAT REMPLACE.
"""
import io, re, sys

F='app.html'
S=io.open(F,encoding='utf-8').read()
N0=len(S)
J=[]
def rep(old,new,n=1,quoi=''):
    global S
    c=S.count(old)
    assert c==n, "«%s» : %d occurrences, %d attendues"%(quoi or old[:60], c, n)
    S=S.replace(old,new)
    J.append('  ✓ %-58s ×%d'%(quoi or old[:58], n))

# ─────────────────────────────────────────────────────────────────────────────
# 1 · LES JETONS FIXES NEUFS
# ─────────────────────────────────────────────────────────────────────────────
rep('--c-brun05:#171000;',
    '--c-brun03:#100D0B;--c-brun05:#171000;', 1,
    'jeton --c-brun03 #100D0B (le FOND du mode sombre)')
rep('--c-brun19-2:#3B2924;',
    '--c-brun19-2:#3B2924;--c-brun19-3:#43291C;', 1,
    'jeton --c-brun19-3 #43291C (le brun ENCRE, sur champ lilas)')
rep('--c-beige26:#453C32;',
    '--c-beige26:#453C32;--c-brun33:#6B4630;', 1,
    'jeton --c-brun33 #6B4630 (le brun SURFACE, corps d\'une fiche tenue)')
# les variantes rgb, à côté des autres
rep('--c-noir03-rgb:11,12,15;',
    '--c-brun03-rgb:16,13,11;--c-brun19-3-rgb:67,41,28;--c-brun33-rgb:107,70,48;--c-noir03-rgb:11,12,15;', 1,
    'les trois -rgb correspondants')

# ─────────────────────────────────────────────────────────────────────────────
# 2 · LE FOND DU MODE SOMBRE : #201908 → #100D0B
#     (l'ENCRE du mode clair, elle, reste #201908 : deux rôles, on sépare au NOM)
# ─────────────────────────────────────────────────────────────────────────────
rep('--ground:var(--c-brun09)', '--ground:var(--c-brun03)', 2,
    'le fond sombre --ground → #100D0B')

# ─────────────────────────────────────────────────────────────────────────────
# 3 · LES BASCULES D'ÉTAT — « la moitié basse du trait ne s'éteint plus »
#     :root = SOMBRE (l'amande, le jaune) · .light = CLAIR (le vert profond, le violet)
# ─────────────────────────────────────────────────────────────────────────────
rep('--c-menthe82-txt:#201908;--c-bleu68-txt:#201908;',
    '--c-menthe82-txt:#00341A;--c-bleu68-txt:#291547;', 1,
    'en clair : tenu → #00341A, en cours → #291547')

# ─────────────────────────────────────────────────────────────────────────────
# 4 · LE BRUN ENCRE SUR LE CHAMP LILAS — le violet quitte le rôle d'encre
# ─────────────────────────────────────────────────────────────────────────────
rep("var NATTRAIT={promi:'#022140',chiche:'#3D0F23',nuee:'#291547'};",
    "var NATTRAIT={promi:'#022140',chiche:'#3D0F23',nuee:'#43291C'};", 1,
    'NATTRAIT.nuee → #43291C')
rep("window._NATTXT = {promi:'#022140', chiche:'#3D0F23', nuee:'#291547'};",
    "window._NATTXT = {promi:'#022140', chiche:'#3D0F23', nuee:'#43291C'};", 1,
    '_NATTXT.nuee → #43291C')
rep("var CLA={promi:'#022140',chiche:'#3D0F23',nuee:'#291547'};",
    "var CLA={promi:'#022140',chiche:'#3D0F23',nuee:'#43291C'};", 1,
    'CLA.nuee (partage) → #43291C')
rep('--c-mauve77-txt:#291547;--c-mauve12-txt:#291547;',
    '--c-mauve77-txt:#43291C;--c-mauve12-txt:#43291C;', 1,
    'les -txt du lilas en mode clair → #43291C')

# ─────────────────────────────────────────────────────────────────────────────
# 5 · LE TRAIT ET LES LIBELLÉS D'ÉTAT, EN JS — ils basculent avec le thème
# ─────────────────────────────────────────────────────────────────────────────
rep("var TERRA='#DD4D23', MENTHE='#8FE08F', CREME='#F7F0DE', ENCRE='#201908';",
    "var TERRA='#DD4D23', MENTHE='#8FE08F', CREME='#F7F0DE', ENCRE='#201908';\n"
    "  /* ⚑ v7 — LES DEUX ÉTATS SOMBRES ET LEURS CLAIRS. Le trait borne le champ et le corps :\n"
    "     sur un corps sombre il prend le clair, sur un corps clair il prend le sombre. */\n"
    "  var TENU='#00341A', AMANDE='#8FE08F', ENCOURS='#291547', JAUNE='#FFD447';\n"
    "  function etatTrait(k,light){return light?(k==='encours'?ENCOURS:TENU):(k==='encours'?JAUNE:AMANDE);}", 1,
    'TENU/AMANDE/ENCOURS/JAUNE + etatTrait()')
rep("      e.base=396; e.amp=36; e.mode='duo'; e.col=MENTHE; e.colTexte=(light?ENCRE:MENTHE);   /* 372 + 24 */",
    "      e.base=396; e.amp=36; e.mode='duo'; e.col=etatTrait('tenu',light); e.colTexte=etatTrait('tenu',light);   /* 372 + 24 */", 1,
    'fiche tenue (duo) : trait et libellés basculent')
rep("      e.mode='complet'; e.col=MENTHE; e.colTexte=(light?ENCRE:MENTHE);",
    "      e.mode='complet'; e.col=etatTrait('tenu',light); e.colTexte=etatTrait('tenu',light);", 1,
    'fiche tenue (complet) : trait et libellés basculent')
rep("                NATCOL:NATCOL, NATCLAIR:NATCLAIR, NATTRAIT:NATTRAIT, TERRA:TERRA, MENTHE:MENTHE,",
    "                NATCOL:NATCOL, NATCLAIR:NATCLAIR, NATTRAIT:NATTRAIT, TERRA:TERRA, MENTHE:MENTHE,\n"
    "                TENU:TENU, AMANDE:AMANDE, ENCOURS:ENCOURS, JAUNE:JAUNE, etatTrait:etatTrait,", 1,
    'les quatre valeurs et etatTrait() publiées sur O')

# ─────────────────────────────────────────────────────────────────────────────
# 6 · L'ORBITE : DEUX TRIPLETS PÉRIMÉS (#2BE88C et #F07A2E, palette d'avant le 16 sept.)
# ─────────────────────────────────────────────────────────────────────────────
rep("  ETAT_MENTHE=_lab(0x2B,0xE8,0x8C); ETAT_TERRA=_lab(0xF0,0x7A,0x2E);",
    "  /* ⚑ v7 — c'étaient encore #2BE88C et #F07A2E, la palette d'AVANT le 16 sept. (§8, les triplets). */\n"
    "  ETAT_MENTHE=_lab(0x8F,0xE0,0x8F); ETAT_TERRA=_lab(0xDD,0x4D,0x23);", 1,
    'Orbite : ETAT_MENTHE/ETAT_TERRA remis à la palette courante')

# ─────────────────────────────────────────────────────────────────────────────
# 7 · LES RÔLES --p-* (la source du portage Swift)
# ─────────────────────────────────────────────────────────────────────────────
SOM_AV=('--p-fond:#201908;--p-encre:#F7F0DE;--p-surface:#211B05;--p-surface-haute:#251F11;'
        '--p-sous-texte:#928166;--p-grip:#493D28;--p-exception:#00341A;')
SOM_AP=('--p-fond:#100D0B;--p-encre:#F7F0DE;--p-surface:#211B05;--p-surface-haute:#251F11;'
        '--p-sous-texte:#928166;--p-grip:#493D28;--p-exception:#6B4630;--p-brun-encre:#43291C;')
rep(SOM_AV, SOM_AP, 1, 'rôles sombres : fond #100D0B, exception #6B4630, + brun-encre')
CLA_AV=('--p-fond:#F7F0DE;--p-encre:#201908;--p-surface:#F7EBD6;--p-surface-haute:#FAF4E8;'
        '--p-sous-texte:#6E6350;--p-grip:#C8BAA4;--p-exception:#00341A;')
CLA_AP=('--p-fond:#F7F0DE;--p-encre:#201908;--p-surface:#F7EBD6;--p-surface-haute:#FAF4E8;'
        '--p-sous-texte:#6E6350;--p-grip:#C8BAA4;--p-exception:#6B4630;--p-brun-encre:#43291C;')
rep(CLA_AV, CLA_AP, 1, 'rôles clairs : exception #6B4630, + brun-encre')
rep('--p-tenu:#8FE08F;--p-a-tenir:#DD4D23;--p-en-cours:#FFD447;',
    '--p-tenu:#00341A;--p-amande:#8FE08F;--p-a-tenir:#DD4D23;--p-en-cours:#291547;--p-en-cours-clair:#FFD447;',
    2, 'rôles d\'état : tenu #00341A + amande, en cours #291547 + clair')
rep('--p-corps-tenu:#132B1B;', '--p-corps-tenu:#6B4630;', 1, 'corps d\'une fiche tenue (sombre) → brun surface')
rep('--p-corps-tenu:#C1E3CC;', '--p-corps-tenu:#6B4630;', 1, 'corps d\'une fiche tenue (clair) → brun surface')

io.open(F,'w',encoding='utf-8').write(S)
print('\n'.join(J))
print('\n%d → %d octets'%(N0,len(S)))
