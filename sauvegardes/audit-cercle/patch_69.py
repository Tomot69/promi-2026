# CHANTIER 69 — le pinceau n'est jamais gardé : lot-PINCEAU lisait `window.promises`, qui n'existe pas (`let promises`). Patch, motifs uniques.
import hashlib, io, os
F = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app.html'))
S = io.open(F, encoding='utf-8').read(); avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '3cbc06b92669392e80a2e6e34603229e', avant
def remplace(old, new):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple : ' + old[:80]
    S = S.replace(old, new)
remplace("""      var avant = {};
      try{ (window.promises||[]).forEach(function(p){ avant[p.id]=1; }); }catch(_){}""",
"""      var avant = {};
      /* ⚑ CHANTIER 69 (11 sept., nuit) : le jeu est un `let promises` — il n'est PAS sur `window`. `window.promises` valait
         undefined : aucun Promi n'était vu « avant », aucun n'était marqué « né » — et aucun ne gardait son pinceau. */
      var _liste = function(){ try{ return (typeof promises !== 'undefined' && promises) || window.promises || []; }catch(_){ return window.promises || []; } };
      try{ _liste().forEach(function(p){ avant[p.id]=1; }); }catch(_){}""")
remplace("""        try{ (window.promises||[]).forEach(function(p){
               if(!avant[p.id] && !p.trait) p.trait = t; }); }catch(_){}""",
"""        try{ _liste().forEach(function(p){
               if(!avant[p.id] && !p.trait) p.trait = t; }); }catch(_){}""")
io.open(F, 'w', encoding='utf-8').write(S); print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
