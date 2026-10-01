# CHANTIER 67 — les pastilles de LE TRAIT d'une Nuée (Tom, 11 sept., nuit). Bloc neuf en fin de fichier.
import hashlib, io, os
F = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app.html'))
S = io.open(F, encoding='utf-8').read(); avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '34c2c4556270566791a1cfe7ae42b054', avant
BLOC = """<style id="lot-CH67">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ CHANTIER 67 — LES PASTILLES DE « LE TRAIT » D'UNE NUÉE (Tom, 11 sept. 2026, nuit).
   La rangée de pinceaux (`.pc-glisse`, 44 de haut) était clouée à `bottom:14px` — une cote prise quand la carte était une
   pilule de rayon 59. Depuis la bascule du rayon (Q203) la carte a le rayon 30, et le coin bas-gauche de la première pastille
   tombait à ~10 de la courbe intérieure (encre mesurée à 11,1 à l'écran, contre 15,19 pour l'air d'un champ ouvert).
   LA COTE SE CALCULE : pour tenir 15,19 au coin (centre de l'arrondi à 30 / 88, trait 2, pastille à x 22), il faut
   bottom ≥ 20 ; on prend 22 — l'air du LIBELLÉ en haut de la carte (`top:22px`) : le contenu de la carte devient symétrique.
   La règle d'origine (≈ l. 24447) n'est pas touchée : celle-ci vient après et gagne par l'ordre, à poids égal.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
#device #detailPoster #npTrait .pc-glisse,.frame #detailPoster #npTrait .pc-glisse{bottom:22px!important}
</style>
"""
old = "\n</body>"
assert S.count(old) == 1
S = S.replace(old, "\n" + BLOC + "</body>")
io.open(F, 'w', encoding='utf-8').write(S); print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
