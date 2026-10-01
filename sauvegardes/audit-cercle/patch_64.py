# CHANTIER 64 — le bandeau et le rond photo du Peaufiner de la page + (Tom, 11 sept., nuit). Bloc neuf en fin de fichier.
import hashlib, io, os
F = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app.html'))
S = io.open(F, encoding='utf-8').read(); avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == 'b7a5bef103fd336b25ccbf54d6387247', avant
BLOC = """<style id="lot-CH64">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ CHANTIER 64 — LE BANDEAU ET LE ROND PHOTO DU PEAUFINER DE LA PAGE + (Tom, 11 sept. 2026, nuit).
   Relevé nœud par nœud (sauvegardes/audit-cercle/probe_haut_pp.py), Peaufiner ouvert (`#createSheet.pp-peauf`) :
     · le plateau de la page + (`.enh`, 342 × 60 à 24 / 40, z 9) reste peint PAR-DESSUS l'en-tête du Peaufiner (`.s2-tete`,
       « Promi » · « ✕ FERMER ») — son « FERMER », déplacé à x 52, tombe sur le titre ;
     · le rond photo (`.ph-photo-btn`, 34 × 34 à 332 / 230) reste peint sur la rangée AVANT.
   Le Peaufiner d'une fiche — la référence — ne porte que `.s2-tete`. On retire CES DEUX NŒUDS, nommément, et SEULEMENT dans
   l'état Peaufiner (la classe que le code pose) ; au repos de la page +, ils sont là comme avant. Le Peaufiner se ferme par son
   propre « ✕ FERMER » (`.s2-fermer`), comme sur une fiche.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
#device #createSheet.pp-peauf>.enh,.frame #createSheet.pp-peauf>.enh,
#device #createSheet.pp-peauf .ph-photo-btn,.frame #createSheet.pp-peauf .ph-photo-btn{visibility:hidden!important;pointer-events:none!important}
</style>
"""
old = "\n</body>"
assert S.count(old) == 1
S = S.replace(old, "\n" + BLOC + "</body>")
io.open(F, 'w', encoding='utf-8').write(S); print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
