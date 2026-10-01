#!/usr/bin/env python3
"""
redteam_clavier.py — iOS N'OUVRE LE CLAVIER QUE SI focus() EST APPELÉ DANS LE GESTE (v114, Tom). Contrôle STATIQUE.

Il relève chaque appel à focus() de app.html et le classe : SYNCHRONE (dans le gestionnaire) ou DIFFÉRÉ (dans un setTimeout /
requestAnimationFrame — hors du geste, Safari iOS donne le focus SANS clavier). Un différé n'est accepté que s'il est précédé,
dans les 400 caractères, d'un focus synchrone sur le même champ (le différé n'est alors qu'un secours).
LE CERCLE (#nueeNomIn) EST EXIGÉ SYNCHRONE — c'est le défaut du 30 sept. Les autres différés connus sont NOMMÉS dans
DIFFERES_CONNUS (l'audit v114), à corriger sur décision ; tout différé NOUVEAU fait échouer.
Rougi : python3 redteam_clavier.py sauvegardes/app-avant-v114.html
"""
import io, os, re, sys
ICI=os.path.dirname(os.path.abspath(__file__))
F=next((a for a in sys.argv[1:] if not a.startswith('--')), os.path.join(ICI,'app.html'))
S=io.open(F,encoding='utf-8').read()
# l'audit v114 : le champ, et pourquoi il attend (motif de 60 caractères autour du focus)
DIFFERES_CONNUS={
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
    diff.append((m.start(), S[max(0,m.start()-600):m.end()], m.group(2), m.group(3)))
tous=len(re.findall(r"\.focus\(", S)); print('focus() : %d, dont %d différé(s)' % (tous, len(diff)))
ok=True
for pos,ctx,corps,ms in diff:
    lig=S.count('\n',0,pos)+1
    avant=ctx[:-len(corps)-40]
    secours = ('activeElement' in corps) and re.search(r"\.focus\(\{preventScroll:true\}\);", avant[-500:]) is not None
    if secours: print('  secours · l.%d (précédé d\'un focus synchrone dans le geste)' % lig); continue
    if 'nueeNomIn' in avant:
        print('  ✗ LE CERCLE — le nom est focalisé %s ms APRÈS le geste · l.%d' % (ms, lig)); ok=False; continue
    nom=next((v for k,v in DIFFERES_CONNUS.items() if k in ctx), None)
    if nom: print('  connu (audit v114, non corrigé) · l.%d · %s' % (lig, nom))
    else: print('  ✗ DIFFÉRÉ NOUVEAU · l.%d · %s' % (lig, re.sub(r'\s+',' ',ctx[-160:]))); ok=False
print('✅ le clavier s\'ouvre au geste' if ok else '❌ un focus hors du geste')
sys.exit(0 if ok else 1)
