# v118 §2 — Q363 tranchée : on retire le code des chemins de saisie remplacés (JS seulement ; le CSS ne se nettoie pas, §9)
import io
S=io.open('app.html',encoding='utf-8').read(); n0=len(S)
def coupe(debut, fin, remplace=''):
    global S
    assert S.count(debut)==1, ('début', S.count(debut), debut[:50])
    i=S.find(debut); j=S.find(fin, i+len(debut)); assert j>i, ('fin', fin[:50])
    morceau=S[i:j]; S=S[:i]+remplace+S[j:]; return morceau
def rep(old,new):
    global S
    assert S.count(old)==1, (S.count(old), old[:60]); S=S.replace(old,new)
# 1 · l'ancien champ « à qui » de la phrase (remplacé par le choix des gens, lot-GENS)
m=coupe("      if(b.dataset.add){\n        /* CHANTIER F", "      if(b.dataset.datepick){",
        "      /* v118 (Q363) : l'ancien champ « à qui » est retiré — le choix des gens (lot-GENS) le remplace */\n")
assert 'ai.focus' in m and m.rstrip().endswith('}') and m.count('{')==m.count('}'), (m.count('{'), m.count('}'))
rep("""    /* « à qui » / « avec » : une pastille + pour ajouter un nom (même gabarit, sobre) */
    + ((cle === 'qui' || cle === 'avec') ? '<button type="button" class="ph-o ph-add" data-add="1" aria-label="ajouter une personne">+</button>' : '')
""", "")
# 2 · la note depuis #dpaJoint (le nœud n'existe plus)
m=coupe("  var bj = document.getElementById('dpaJoint');\n  if(bj && !bj._pose){", "  /* LA TEINTE DE LA DALLE devient la couleur des accents", "")
assert m.count('{')==m.count('}') and 'dNote' in m
# 3 · #dpsCom / #dpsJoint / #dpsPart (les nœuds n'existent plus) et `ouvrePeaufiner`, qui ne servait qu'à eux
m=coupe("  /* (le rang social a ete remplace par la barre dans le rang du lien) */\n  var ouvrePeaufiner", "  /* ── LA BARRE DU ONE PAGER ──", "")
assert m.count('{')==m.count('}') and 'dpsPart' in m
# 4 · #dpBarre (masquée, 0 × 0) : commenter, joindre, partager — la barre Peaufiner porte le partage, le tiroir la note et les commentaires
m=coupe("  /* ── LA BARRE DU ONE PAGER ──", "  var z = document.getElementById('tenirZone');",
        "  /* v118 (Q363) : la barre #dpBarre (commenter · joindre · partager), masquée depuis le portage des fiches, est retirée */\n")
assert m.count('{')==m.count('}') and 'dpbCom' in m and 'vaVers' in m
# 5 · le pseudo de l'ancien onboarding : toPseudo et ses deux seuls appelants
m=coupe("function toPseudo(){", "function prefill(name)", "")
assert m.count('{')==m.count('}') and 'pseudoInput' in m
rep("function prefill(name){var el=document.getElementById('pseudoInput');if(el&&name){el.value=name;liveName(name);}}\n", "")
rep("document.getElementById('btnApple').onclick=function(){/* Firebase signInWithApple -> prénom Apple */prefill('Tom');toPseudo();};\n", "")
rep("document.getElementById('btnGoogle').onclick=function(){/* Firebase signInWithGoogle -> prénom Google */prefill('Tom');toPseudo();};\n", "/* v118 (Q363) : toPseudo, prefill et les deux boutons de l'ancien écran de compte sont retirés — l'onboarding v20 a son écran « Garder ta Toile » */\n")
io.open('app.html','w',encoding='utf-8').write(S); print('retiré : %d caractères' % (n0-len(S)))
import re
for n in ['ouvrePeaufiner','vaVers','toPseudo','prefill','dpsCom','dpsJoint','dpsPart','dpaJoint','dpbCom','dpbJoint','ai\\.focus','ph-addbar','dpBarre','dpbPart']:
    print('%-16s %d' % (n, len(re.findall(n,S))))
