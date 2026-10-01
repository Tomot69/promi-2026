# ⚑ `opts()` DU LOT DE L'AURA N'ÉTAIT VRAI QUE POUR SON PROPRE ÉCRAN : il lit `D`, l'objet de données de l'Aura,
#    qui vaut null tant que cet écran n'a pas été ouvert. Un SECOND peintre le rencontre forcément (l'écran qui vend).
#    `peauVers()`, juste à côté, protège DÉJÀ `D` (`if(!clair() || !D) return null;`) : on applique la même prudence,
#    sans rien inventer — l'appelant impose `sol`, et `pousse` vaut 0 quand il n'y a pas encore de données.
import hashlib, io
F = 'scratchpad/app-vend-sphere.html'
S = io.open(F, encoding='utf-8').read()
def r(old, new, quoi):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple (%s) : %r' % (quoi, old)
    S = S.replace(old, new); print('  ✔', quoi)
r("sol:ORB.solR||NAT[D.nature], tailles:A.t",
  "sol:ORB.solR||NAT[(D&&D.nature)||'promi'], tailles:A.t", "opts() : le sol ne suppose plus D bâti")
r("pousse:Math.min(1, D.n/34)", "pousse:Math.min(1, (D?D.n:0)/34)", "opts() : la pousse ne suppose plus D bâti")
io.open(F, 'w', encoding='utf-8').write(S)
print('copie →', hashlib.md5(S.encode('utf-8')).hexdigest())
