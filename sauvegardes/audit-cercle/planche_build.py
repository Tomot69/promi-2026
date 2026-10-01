# LE CERCLE — ASSEMBLE LA PLANCHE AUTONOME (PLANCHE-CERCLE.html, à la racine du projet).
# Les six faces embarquées (planche-polices.css) et toutes les images sont DANS le fichier : la planche s'affiche pareil
# hors du serveur (leçon de la planche 4 de la fiche d'une personne).
# La page du Cercle est composée ici, cote par cote, avec les VALEURS DU BLOC DU §3.8 RELEVÉES DANS L'APP (audit.json :
# réglage 342 × 64, trait 2, rayon 32 ; libellé ApfelMid 500 / 13, .18em ; valeur Bricolage 700 / 18 ; encart 342 × 90,
# rayon 26, à +108 du haut du bloc ; titre 700 / 22, sous-titre 600 / 15). Les dalles sont celles du moteur
# (planche_captures.py). Le Studio et les Réglages sont des captures de l'app, libellés décidés posés le temps de la prise.
import base64, os, re
D = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(D, '..', '..'))
PL = os.path.join(D, 'planche'); EC = os.path.join(D, 'ecran')
def img(chemin):
    return 'data:image/png;base64,' + base64.b64encode(open(chemin, 'rb').read()).decode()
polices = open(os.path.join(RACINE, 'planche-polices.css'), encoding='utf-8').read()

T = {  # les deux thèmes — valeurs relevées dans l'app (Réglages, bloc du §3.8)
 'dk': dict(fond='#12142A', encre='#F4EEE1', lab='#CBAAFF', enc_fond='#F4EEE1', enc_tx='#AE86F2',
            second='#A8A396', btn_fond='#F4EEE1', btn_tx='#12142A', nom='#C9C4B4'),
 'lt': dict(fond='#F4EEE1', encre='#16171B', lab='#3A54FF', enc_fond='#16171B', enc_tx='#CBAAFF',
            second='#6B6658', btn_fond='#16171B', btn_tx='#F4EEE1', nom='#4A463C'),
}
REGS = [("C'EST IMPORTANT ?", '· ·· ···'), ('RÉCURRENCE', 'chaque semaine'), ('RAPPEL', 'la veille à 19:00'),
        ('LA MÉMOIRE', 'réveille tes « en l’air »')]
# un Promi différent par monde : la diversité des dalles vient des Promi (§4 — la dalle porte le monde), pas d'une teinte
MONDES = [('sillons', 'Sillons', 129), ('gravure', 'Gravure', 134), ('terrazzo', 'Terrazzo', 125)]
Y0 = 132          # haut du bloc du §3.8 (32 sous le plateau, qui finit à 100)
S_BAS = 150       # défilement du second cadre

def contenu(t):
    c = T[t]; h = []
    for i, (l, v) in enumerate(REGS):
        y = Y0 + i * 80
        h.append('<div class="reg" style="top:%dpx;border-color:%s;color:%s"><span class="rl" style="color:%s">%s</span>'
                 '<span class="rv">%s</span></div>' % (y, c['encre'], c['encre'], c['lab'], l, v))
    h.append('<div class="enc" style="top:%dpx;background:%s;color:%s"><span class="et">✦ Le Cercle</span>'
             '<span class="es">importance, récurrence, rappels, mémoire</span></div>' % (Y0 + 108, c['enc_fond'], c['enc_tx']))
    for i, (k, nom, pid) in enumerate(MONDES):
        x = 24 + i * 122
        h.append('<img class="dal" data-monde="%s" src="%s" style="left:%dpx;top:468px">' % (k, img(os.path.join(PL, 'dalle_%s_%d.png' % (k, pid))), x))
        h.append('<div class="nom" style="left:%dpx;top:574px;color:%s">%s</div>' % (x, c['nom'], nom))
    h.append('<div class="prix" style="top:612px">29 €</div>')
    h.append('<div class="sous" style="top:678px">soit 2,42 €/mois · −39 %</div>')
    h.append('<div class="btn" style="top:722px;background:%s;color:%s;border-color:%s">Prendre l’année</div>' % (c['btn_fond'], c['btn_tx'], c['btn_fond']))
    h.append('<div class="btn b2" style="top:800px;border-color:%s">Essayer 14 jours, puis 3,99 €/mois</div>' % c['encre'])
    h.append('<div class="note" style="top:884px;color:%s">Sans engagement · annulable en 2 taps, à tout moment.</div>' % c['second'])
    h.append('<div class="note" style="top:910px;color:%s">ou un design à l’unité — 1 €, ou 4 pour 3 €</div>' % c['second'])
    return ''.join(h)

def cadre_page(t, defile):
    c = T[t]
    inner = contenu(t)
    # le contenu défile SOUS le plateau et y est rogné (CLAUDE §8 : le conteneur qui défile commence sous le plateau)
    return ('<div class="fr" data-cadre="cercle_%s_%s" style="background:%s;color:%s">'
            '<div class="defil" style="top:112px;height:732px"><div class="pg" style="top:%dpx">%s</div></div>'
            '<div class="plat" style="background:%s;border-color:%s"><span class="t">Le Cercle</span><span class="c">✕ Fermer</span></div>'
            '</div>') % (t, 'bas' if defile else 'haut', c['fond'], c['encre'], -112 - (S_BAS if defile else 0), inner, c['fond'], c['encre'])

def fig(html, legende):
    return '<figure>%s<figcaption>%s</figcaption></figure>' % (html, legende)
def fig_img(chemin, legende, cls='cap'):
    return fig('<img class="%s" src="%s">' % (cls, img(chemin)), legende)

CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#0E0F12;color:#F4EEE1;font-family:Apfel,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.page{max-width:1780px;margin:0 auto;padding:44px 32px 120px}
h1{font-family:Bricolage;font-weight:700;font-size:38px;letter-spacing:-.02em;margin:0 0 6px}
h2{font-family:Bricolage;font-weight:700;font-size:27px;letter-spacing:-.02em;margin:52px 0 12px}
.lede,.pr{font-family:Apfel;font-size:15.5px;line-height:1.6;max-width:1040px;color:#C8C3B6;margin:0 0 22px}
.lede b,.pr b,td b,li b{color:#F4EEE1;font-family:ApfelMid;font-weight:500}
.row{display:flex;gap:26px;flex-wrap:wrap;align-items:flex-start;margin:0 0 8px}
figure{margin:0}
figcaption{font-family:ApfelMid;font-weight:500;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#8B8778;margin:10px 0 0;width:390px;line-height:1.5}
figcaption b{color:#F4EEE1;font-weight:500}
img.cap{width:390px;height:844px;border-radius:38px;display:block}
table.reg{border-collapse:collapse;font-family:Apfel;font-size:14px;line-height:1.5;color:#C8C3B6;max-width:1300px}
table.reg th,table.reg td{border-bottom:2px solid #2A2C34;padding:9px 12px;text-align:left;vertical-align:top}
table.reg th{font-family:Bricolage;font-weight:700;color:#F4EEE1}
.defile{overflow-x:auto;max-width:100%}
ul.l{font-family:Apfel;font-size:14.5px;line-height:1.62;color:#C8C3B6;max-width:1100px}
/* ─── le cadre : 390 × 844, exactement ─── */
.fr{position:relative;width:390px;height:844px;overflow:hidden;border-radius:38px;flex:none}
.fr *{position:absolute;margin:0}
.defil{left:0;width:390px;overflow:hidden}
.pg{left:0;width:390px;height:1000px}
.plat{left:24px;top:40px;width:342px;height:60px;border-radius:30px;border:2px solid;display:flex!important;align-items:center;justify-content:space-between;padding:0 22px 0 26px}
.plat>*{position:static!important}
.plat .t{font-family:Bricolage;font-weight:700;font-size:27px;letter-spacing:-.035em}
.plat .c{font-family:ApfelMid;font-weight:500;font-size:12px;letter-spacing:.2em;text-transform:uppercase}
/* le bloc du §3.8 — valeurs relevées dans l'app */
.reg{left:24px;width:342px;height:64px;border:2px solid;border-radius:32px;display:flex!important;align-items:center;justify-content:space-between;padding:0 22px;filter:blur(2.4px);pointer-events:none}
.reg>*{position:static!important}
.rl{font-family:ApfelMid;font-weight:500;font-size:13px;letter-spacing:.18em}
.rv{font-family:Bricolage;font-weight:700;font-size:18px}
.enc{left:24px;width:342px;height:90px;border-radius:26px;display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:5px}
.enc>*{position:static!important}
.et{font-family:Bricolage;font-weight:700;font-size:22px;letter-spacing:-.02em;line-height:1}
.es{font-family:Bricolage;font-weight:600;font-size:15px;line-height:1.1}
.dal{width:98px;height:98px;object-fit:contain}
.nom{width:98px;text-align:center;font-family:Bricolage;font-weight:600;font-size:13px;letter-spacing:-.01em}
.prix{left:24px;width:342px;text-align:center;font-family:Bricolage;font-weight:700;font-size:56px;letter-spacing:-.03em;line-height:1}
.sous{left:24px;width:342px;text-align:center;font-family:ApfelMid;font-weight:500;font-size:15px;line-height:1.15}
.btn{left:24px;width:342px;height:62px;border-radius:31px;border:2px solid;display:flex!important;align-items:center;justify-content:center;font-family:Bricolage;font-weight:700;font-size:19px;letter-spacing:-.01em}
.btn.b2{font-size:17px}
.note{left:24px;width:342px;text-align:center;font-family:Apfel;font-weight:400;font-size:14px;line-height:1.3}
"""

H = []
H.append('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="Cache-Control" content="no-store">')
H.append('<title>Promi — le Cercle · planche</title><style>%s\n%s</style></head><body><div class="page">' % (polices, CSS))
H.append('<h1>Le Cercle — planche</h1>')
H.append('<p class="lede"><b>Avant toute intégration.</b> Rien n’est écrit dans <code>app.html</code>. L’audit '
         '(<code>AUDIT-CERCLE.md</code>) a montré une page de vente qui dit au lieu de montrer, et qui en thème clair '
         'n’affiche ni ses prix ni ses boutons. Cette planche applique ta consigne — <b>on voit quoi, jamais combien</b> — avec '
         '<b>zéro mot neuf</b> : chaque libellé vient de la spec, de l’app ou de toi (tableau en bas). La matière est celle '
         'du moteur : les trois dalles sont peintes par <code>Toile.dalleTrame</code> à l’échelle 1, dans leur monde.</p>')

H.append('<h2>La page du Cercle — à l’ouverture, puis défilée jusqu’au bout</h2>')
H.append('<p class="pr"><b>Ce qu’il ouvre se voit :</b> les quatre réglages restent à leur place, <b>floutés à 2,4 px</b>, '
         'l’encart net posé dessus — le bloc du §3.8, à la cote près, la seule superposition du produit. Puis les '
         '<b>trois mondes</b>, en vraies dalles, nettes (une dalle qu’on montre ne se voile jamais, §4). Puis <b>le prix, '
         'dans ta forme</b>, et l’année comme choix premier. Le mois vient ensuite, avec l’essai. <b>Tout tient au-dessus '
         'du pli</b> jusqu’au bouton de l’année ; le reste se découvre en défilant, sous le plateau qui rogne.</p>')
H.append('<div class="row">%s%s%s%s</div>' % (
    fig(cadre_page('dk', False), 'sombre · <b>à l’ouverture</b>'),
    fig(cadre_page('dk', True), 'sombre · <b>défilée</b>'),
    fig(cadre_page('lt', False), 'clair · <b>à l’ouverture</b>'),
    fig(cadre_page('lt', True), 'clair · <b>défilée</b>')))
H.append('<p class="pr"><b>Aujourd’hui, pour comparer</b> — la même page dans l’app : en clair, « 29 € », « 3,99 €/mois » '
         'et le bouton d’essai sont crème sur crème (contraste 1,09 et 1,16).</p>')
H.append('<div class="row">%s%s</div>' % (
    fig_img(os.path.join(EC, 'dark_gratuit_plus_openPlusTop_haut.png'), 'aujourd’hui · sombre'),
    fig_img(os.path.join(EC, 'light_gratuit_plus_openPlusTop_bas.png'), 'aujourd’hui · clair · <b>les prix manquent</b>')))

H.append('<h2>Le Studio, sur un monde du Cercle — au repos, puis au doigt</h2>')
H.append('<p class="pr"><b>Q106 et Q117, tels qu’ils sont décidés :</b> au repos, rien que l’encart du §3.8 — « ✦ Le '
         'Cercle / sillons, gravure, terrazzo » ; le prix n’apparaît qu’au doigt, et il <b>nomme le monde</b> — « Adopte '
         'Terrazzo — 1 € » — au lieu de tirer un libellé au hasard. L’ombre de texte (le halo) est retirée (§6). Captures de '
         'l’app, libellés posés le temps de la prise. L’encart garde la largeur que l’app lui donne dans le panneau (302).</p>')
H.append('<div class="row">%s%s%s%s%s</div>' % (
    fig_img(os.path.join(EC, 'dark_gratuit_studio_terrazzo.png'), 'aujourd’hui · sombre'),
    fig_img(os.path.join(PL, 'studio_dark_repos.png'), 'sombre · <b>au repos</b>'),
    fig_img(os.path.join(PL, 'studio_dark_doigt.png'), 'sombre · <b>au doigt</b>'),
    fig_img(os.path.join(PL, 'studio_light_repos.png'), 'clair · <b>au repos</b>'),
    fig_img(os.path.join(PL, 'studio_light_doigt.png'), 'clair · <b>au doigt</b>')))

H.append('<h2>Les Réglages — l’encart dit ce qu’il ouvre</h2>')
H.append('<p class="pr">« débloque tout Promi · essai 14 jours » devient le sous-titre du §3.8 — <b>importance, '
         'récurrence, rappels, mémoire</b> : les quatre réglages qu’il recouvre. Halo retiré.</p>')
H.append('<div class="row">%s%s%s</div>' % (
    fig_img(os.path.join(EC, 'dark_gratuit_reglages.png'), 'aujourd’hui · sombre'),
    fig_img(os.path.join(PL, 'reglages_dark.png'), 'sombre'),
    fig_img(os.path.join(PL, 'reglages_light.png'), 'clair')))

H.append('<h2>Chaque libellé de la page, et d’où il vient</h2><div class="defile"><table class="reg">'
 '<tr><th>libellé</th><th>d’où il vient</th></tr>'
 '<tr><td>Le Cercle · ✕ Fermer</td><td>existant — le plateau (§3.1, écrans de dock)</td></tr>'
 '<tr><td>C’EST IMPORTANT ? · RÉCURRENCE · RAPPEL · LA MÉMOIRE, et leurs valeurs</td><td>existant — l’inventaire du §3.8</td></tr>'
 '<tr><td>✦ Le Cercle · importance, récurrence, rappels, mémoire</td><td>existant — l’encart du §3.8</td></tr>'
 '<tr><td>Sillons · Gravure · Terrazzo</td><td>existant — les noms des mondes (Studio)</td></tr>'
 '<tr><td>29 € · soit 2,42 €/mois · −39 %</td><td><b>ta forme, mot pour mot</b></td></tr>'
 '<tr><td>Prendre l’année</td><td>existant — <code>#buyYear</code></td></tr>'
 '<tr><td>Essayer 14 jours, puis 3,99 €/mois</td><td>existant — <code>#buyMonth</code></td></tr>'
 '<tr><td>Sans engagement · annulable en 2 taps, à tout moment.</td><td>existant — <code>.pl-note</code></td></tr>'
 '<tr><td>ou un design à l’unité — 1 €, ou 4 pour 3 €</td><td>existant — gardé pour ne pas perdre un revenu ; '
 '<b>« 4 pour 3 » n’a aucun achat derrière et il n’y a que trois mondes payants</b> (Q196.4)</td></tr>'
 '<tr><td><s>Essaie tout, sans t’engager.</s> · <s>Tout Promi pour 3,99 €/mois… près de cinq mois offerts</s> · '
 '<s>les cinq arguments et leurs glyphes</s></td><td><b>retirés, pas remplacés</b> — la forme de prix interdite ; « Nuées '
 'illimitées » est gratuit (A11) ; « Stats avancées », « Rappels intelligents », « Toiles signature » retirés par Q165</td></tr>'
 '</table></div>')

H.append('<h2>Ce que la planche ne dessine pas — et pourquoi</h2><ul class="l">'
 '<li><b>Les blocs d’Aura que le Cercle ouvre — graphes, évolution, réciprocité.</b> Ils n’existent pas sur l’Aura '
 'actuelle (l’Orbite ne connaît pas le Cercle). Les montrer voilés ici, ce serait inventer leur forme (§9) : ils se '
 'dessinent d’abord DANS l’Aura. <b>C’est la question de ce tour.</b></li>'
 '<li><b>Le chiffre d’harmonie</b> — « s’il revient » : il n’est pas sur l’Aura actuelle.</li>'
 '<li><b>L’écran d’un abonné</b> — où mène la porte de l’accueil quand on a payé (Q196.6).</li>'
 '<li><b>Le bloc sur le Peaufiner de la page +</b> (Q196.3), <b>les pinceaux et les codes couleur</b> (Q196.5).</li>'
 '<li><b>Le contraste de l’encart en sombre</b> — dessiné selon la spec (#AE86F2 sur crème, 2,42) : Q196.1.</li>'
 '<li><b>Ce qui n’est pas du dessin</b> et se corrige à l’intégration : les prix invisibles en clair, la fin '
 'd’abonnement qui garde le monde payant (et rend Encre à la place de Mosaïque), « Membre du Cercle » en gratuit, le '
 'verrou resservi à un abonné, l’achat qui mène à l’Aura, « Réinitialiser (test) » qui donne le Cercle, le visuel vide '
 '— <code>AUDIT-CERCLE.md</code> § E.</li></ul>')
H.append('</div></body></html>')
open(os.path.join(RACINE, 'PLANCHE-CERCLE.html'), 'w', encoding='utf-8').write(''.join(H))
print('écrit PLANCHE-CERCLE.html', sum(len(x) for x in H) // 1024, 'Ko')
