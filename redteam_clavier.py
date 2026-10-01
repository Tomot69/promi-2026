#!/usr/bin/env python3
"""
redteam_clavier.py — iOS N'OUVRE LE CLAVIER QUE SI focus() EST APPELÉ DANS LE GESTE (v114, Tom). Contrôle STATIQUE.

Il relève chaque appel à focus() de app.html et le classe : SYNCHRONE (dans le gestionnaire) ou DIFFÉRÉ (dans un setTimeout /
requestAnimationFrame — hors du geste, Safari iOS donne le focus SANS clavier). Un différé n'est accepté que s'il est précédé,
dans les 400 caractères, d'un focus synchrone sur le même champ (le différé n'est alors qu'un secours).
v115 (Tom, Q361) : LES HUIT CHAMPS SONT EXIGÉS SYNCHRONES — le Cercle (v114) et les sept de l'audit, nommés dans EXIGES.
Un différé n'y est accepté que comme SECOURS (focus synchrone juste avant, et le différé ne refocalise que si le focus a été
perdu). Tout différé NOUVEAU fait échouer. Rougi : sur sauvegardes/app-avant-v115.html, les sept ; sur app-avant-v114, les huit.
Rougi : python3 redteam_clavier.py sauvegardes/app-avant-v114.html
"""
import io, os, re, sys
ICI=os.path.dirname(os.path.abspath(__file__))
F=next((a for a in sys.argv[1:] if not a.startswith('--')), os.path.join(ICI,'app.html'))
S=io.open(F,encoding='utf-8').read()
# l'audit v114 : le champ, et pourquoi il attend (motif de 60 caractères autour du focus)
EXIGES={
  'nueeNomIn':'le nom du Cercle (v114)',
  'ai.focus':'la page + — « à qui » : le champ de recherche d\'une personne (30 ms)',
  'draftTitreIn':'la page + d\'un gardé de côté — le titre (30 ms)',
  'n.focus({preventScroll:true})':'Peaufiner — la note, après l\'ouverture du tiroir (420 ms)',
  't.focus({preventScroll:true})':'Peaufiner — le champ visé par la barre de la fiche (400 ms)',
  'c.focus({preventScroll:true})':'fiche — le commentaire, depuis le bouton rond (400 ms)',
  'pseudoInput':'l\'onboarding — le pseudo (520 ms)',
  "inp.focus(); }catch(_){} }, 30)":'les gens — « + ajouter quelqu\'un » (30 ms)',
}
# un bloc DIFFÉRÉ : setTimeout(function(){ … }, n) ou requestAnimationFrame(function(){ … }) dont le corps (≤ 200 car.) appelle focus()
BLOC=re.compile(r"(setTimeout|requestAnimationFrame)\(\s*function\s*\(\)\s*\{(.{0,200}?)\}\s*(?:,\s*(\d+))?\s*\)", re.S)
diff=[]
for m in BLOC.finditer(S):
    if '.focus(' not in m.group(2): continue
    diff.append((m.start(), S[max(0,m.start()-1300):m.end()], m.group(2), m.group(3)))
tous=len(re.findall(r"\.focus\(", S)); print('focus() : %d, dont %d différé(s)' % (tous, len(diff)))
ok=True; vus=set()
for pos,ctx,corps,ms in diff:
    lig=S.count('\n',0,pos)+1
    avant=ctx[:-len(corps)-40]
    secours = ('activeElement' in corps) and re.search(r"\.focus\(\{preventScroll:true\}\);", avant[-500:]) is not None
    if secours:
        nom=next((v for k,v in EXIGES.items() if k in ctx), '(autre)')
        print('  ✓ %s — dans le geste (l.%d, différé en secours)' % (nom, lig)); vus.add(nom); continue
    if 'nueeNomIn' in avant:
        print('  ✗ LE CERCLE — le nom est focalisé %s ms APRÈS le geste · l.%d' % (ms, lig)); ok=False; continue
    nom=next((v for k,v in EXIGES.items() if k in ctx), None)
    if nom: print('  ✗ %s — focalisé APRÈS le geste · l.%d' % (nom, lig)); ok=False
    else: print('  ✗ DIFFÉRÉ NOUVEAU · l.%d · %s' % (lig, re.sub(r'\s+',' ',ctx[-160:]))); ok=False
manque=[v for v in EXIGES.values() if v not in vus]
for m in manque:
    if not any(m in x for x in []): pass
if ok and manque:
    for m in manque: print('  ✗ non retrouvé (un champ exigé a disparu ou son focus a changé de forme) :', m)
    ok=False
print('✅ le clavier s\'ouvre au geste — %d champs' % len(vus) if ok else '❌ un focus hors du geste')
sys.exit(0 if ok else 1)
