# L'ÉCRAN QUI VEND — UNE SEULE VERSION, CORRIGÉE (Tom, 11 sept.). Patch sur app.html, motif unique, bloc en fin de fichier.
import hashlib, io, os
RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = os.path.join(RACINE, 'app.html')
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '76a419a18d30c1c27cadc1795248071d', 'app.html a changé depuis le patch du seuil : ' + avant

def remplace(old, new):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple : ' + old[:90]
    S = S.replace(old, new)

# 1 · la forme du prix (Tom, 11 sept. : « Le prix s'écrit 29 € · soit 2,42 €/mois · −39 %, jamais « 2 mois offerts » »).
#     La seule phrase du fichier qui écrit « mois offerts ». Rien d'autre n'y change.
remplace("""Ou prends l'année : <b>29&nbsp;€</b>, soit près de cinq mois offerts.</div>""",
         """Ou prends l'année : <b>29&nbsp;€</b> · soit 2,42&nbsp;€/mois · −39&nbsp;%.</div>""")

# 2 · les couleurs et la marge — un bloc neuf, en fin de fichier
BLOC = """<style id="lot-CERCLE-VEND-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — UNE SEULE VERSION (Tom, 11 sept. 2026) : « L'écran qui vend est cercleScreen, celui qui porte le
   prix et le bouton — c'est celui-là que les murs doivent atteindre, et il n'y a qu'une version. » C'est `#plusScreen` :
   les murs y mènent déjà (fiche, page +, gardé de côté, par-dessus ; Réglages, Studio, accueil). RIEN N'Y EST REDESSINÉ.
   On corrige ce qui l'empêchait de vendre — mesuré le 11 sept. (sauvegardes/audit-cercle/vend_avant.py, AUDIT-CERCLE A1) :
     · en CLAIR, le prix et les boutons ne se lisaient pas : « Prendre l'année — 29 € » 1,09 · « Essayer 14 jours, puis
       3,99 €/mois » 1,16 (blanc sur crème) · les deux montants de la phrase 1,09 · « ta », « l'inverse » 1,09 ;
     · en SOMBRE, « soit 2,42 €/mois · −39 % » bleu sur encre : 3,36 — du ton sur ton (§3, écart de luminosité < 42) ;
     · titre, phrase et liste à x 6 de l'appareil, pour une marge de 24 : l'écran vit hors de `#device`, décalé de 16
       (CLAUDE §8), et son padding de 22 est compté depuis le bord de l'ÉCRAN. Les boutons, centrés, tombaient déjà à 24.
   L'encre suit le fond (§3), et `-webkit-text-fill-color` vaut toujours `color` (§3).
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
.frame.light #plusScreen #buyMonth,.frame.light #plusScreen #buyYear,
#device.light #plusScreen #buyMonth,#device.light #plusScreen #buyYear,
.frame.light #plusScreen .pl-sub b,.frame.light #plusScreen .pl-fd b,
#device.light #plusScreen .pl-sub b,#device.light #plusScreen .pl-fd b{color:#16171B!important;-webkit-text-fill-color:#16171B!important}
.frame:not(.light) #plusScreen #buyYear span,#device:not(.light) #plusScreen #buyYear span{color:#F4EEE1!important;-webkit-text-fill-color:#F4EEE1!important}
#plusScreen>.pl-h,#plusScreen>.pl-sub,#plusScreen>.pl-feat{margin-left:18px!important;margin-right:18px!important}
</style>
"""
remplace("""</script>

</body>""", """</script>
""" + BLOC + """
</body>""")

io.open(F, 'w', encoding='utf-8').write(S)
print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
