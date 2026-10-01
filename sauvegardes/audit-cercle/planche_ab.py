# L'ÉCRAN QUI VEND — A ET B, DITS EN TOUTES LETTRES (Tom, 11 sept. : « montre-moi A et B, tu ne m'as pas dit ce qu'ils
# sont »). PLANCHE-CERCLE-AB.html, autonome. Même composition que la planche 3, l'ordre nouveau des réglages :
# récurrence · rappels · importance · mémoire.
import os, re
D = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.abspath(os.path.join(D, '..', '..'))
src = open(os.path.join(D, 'planche3_build.py'), encoding='utf-8').read()
# on reprend la composition de la planche 3 (ecran_qui_vend, T, MONDES, img…) sans rejouer son assemblage
tete = src.split("def cap(")[0]
tete = tete.replace("COTES = json.load(open(os.path.join(P3, 'cotes.json'), encoding='utf-8'))", "")
tete = tete.replace("MES = json.load(open(os.path.join(P3, 'mesures.json'), encoding='utf-8'))", "")
ns = {'__file__': os.path.join(D, 'planche3_build.py')}
exec(tete, ns)
ns['REGS'][:] = [('RÉCURRENCE', 'chaque semaine'), ('RAPPEL', 'la veille à 19:00'), ("C'EST IMPORTANT ?", '· ·· ···'),
                 ('LA MÉMOIRE', 'réveille tes « en l’air »')]
vend = ns['ecran_qui_vend']
CSS = open(os.path.join(D, 'planche2_build.py'), encoding='utf-8').read().split('CSS = r"""')[1].split('"""')[0]
polices = open(os.path.join(RACINE, 'planche-polices.css'), encoding='utf-8').read()
def fig(h, l): return '<figure>%s<figcaption>%s</figcaption></figure>' % (h, l)
H = ['<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="Cache-Control" content="no-store">',
     '<title>Promi — l’écran qui vend · A et B</title><style>%s\n%s</style></head><body><div class="page">' % (polices, CSS),
     '<h1>L’écran qui vend — A et B</h1>',
     '<p class="lede">C’est l’écran où mène l’encart « ✦ Le Cercle » du mur. Les deux versions ont <b>le même bas</b> : '
     'les trois mondes du Cercle en vraies dalles (Sillons, Gravure, Terrazzo), <b>29 € · soit 2,42 €/mois · −39 %</b>, '
     '« Prendre l’année » en premier, puis « Essayer 14 jours, puis 3,99 €/mois ». <b>Elles ne diffèrent que par le haut — '
     'la façon de montrer les quatre réglages qu’on achète.</b></p>',
     '<ul class="l">'
     '<li><b>A · les quatre réglages NETS, en aperçu.</b> On lit ce qu’on obtient — RÉCURRENCE chaque semaine, RAPPEL la '
     'veille à 19:00, C’EST IMPORTANT ?, LA MÉMOIRE — sans flou et sans encart. Ce n’est pas le mur : on vient de le toucher, '
     'ici on montre ce qu’il y a derrière. Ils ne se touchent pas (c’est un aperçu, pas un réglage). <b>Pour</b> : on sait '
     'ce qu’on paie. <b>Contre</b> : des pastilles nettes ressemblent à des réglages qu’on pourrait toucher.</li>'
     '<li><b>B · le mur repris.</b> Les quatre mêmes réglages, floutés à 2,4, « ✦ Le Cercle » net posé dessus — exactement '
     'ce qu’on vient de toucher dans Peaufiner. <b>Pour</b> : une seule grammaire, « c’est là, pas encore à toi ». '
     '<b>Contre</b> : on ne lit pas ce qu’on achète, et l’encart d’un écran qui s’appelle déjà « Le Cercle » ne mène nulle '
     'part (on y est).</li></ul>',
     '<h2>A · les réglages nets</h2><div class="row">%s%s</div>' % (fig(vend('dk', 'A'), 'sombre · <b>A</b>'), fig(vend('lt', 'A'), 'clair · <b>A</b>')),
     '<h2>B · le mur repris</h2><div class="row">%s%s</div>' % (fig(vend('dk', 'B'), 'sombre · <b>B</b>'), fig(vend('lt', 'B'), 'clair · <b>B</b>')),
     '<h2>Le bas, commun aux deux — défilé</h2><div class="row">%s%s</div>' % (fig(vend('dk', 'A', True), 'sombre'), fig(vend('lt', 'A', True), 'clair')),
     '<p class="pr">Aucun mot neuf. Le contraste de « ✦ Le Cercle » sur l’encart crème de B, en sombre, est celui de la spec '
     '(#AE86F2, 2,42 — Q196.1).</p></div></body></html>']
open(os.path.join(RACINE, 'PLANCHE-CERCLE-AB.html'), 'w', encoding='utf-8').write(''.join(H))
print('écrit PLANCHE-CERCLE-AB.html')
