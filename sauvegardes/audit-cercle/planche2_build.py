# LE CERCLE — PLANCHE 2 (PLANCHE-CERCLE-2.html, racine). Autonome : six faces et images embarquées.
# Ce que Tom a demandé, 11 sept. : le mur qui garde vraiment · le chemin qui mène à l'écran qui vend · cet écran, avec
# « 29 € · soit 2,42 €/mois · −39 % » · l'état abonné, net et touchable. Deux thèmes.
# Le mur et l'état abonné sont des CAPTURES DE L'APP (planche2_captures.py) ; l'écran qui vend est composé ici, aux cotes
# du bloc du §3.8 relevées dans l'app. Décisions appliquées : Q201 (encart « ✦ Le Cercle » seul), Q200 (Studio inchangé).
import base64, json, os
D = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.abspath(os.path.join(D, '..', '..'))
P2 = os.path.join(D, 'planche2'); P1 = os.path.join(D, 'planche'); EC = os.path.join(D, 'ecran')
def img(ch): return 'data:image/png;base64,' + base64.b64encode(open(ch, 'rb').read()).decode()
polices = open(os.path.join(RACINE, 'planche-polices.css'), encoding='utf-8').read()
COTES = json.load(open(os.path.join(P2, 'cotes.json'), encoding='utf-8'))

T = {'dk': dict(fond='#12142A', encre='#F4EEE1', lab='#CBAAFF', enc_fond='#F4EEE1', enc_tx='#AE86F2', second='#A8A396',
                btn_fond='#F4EEE1', btn_tx='#12142A', nom='#C9C4B4'),
     'lt': dict(fond='#F4EEE1', encre='#16171B', lab='#3A54FF', enc_fond='#16171B', enc_tx='#CBAAFF', second='#6B6658',
                btn_fond='#16171B', btn_tx='#F4EEE1', nom='#4A463C')}
REGS = [("C'EST IMPORTANT ?", '· ·· ···'), ('RÉCURRENCE', 'chaque semaine'), ('RAPPEL', 'la veille à 19:00'),
        ('LA MÉMOIRE', 'réveille tes « en l’air »')]
MONDES = [('sillons', 'Sillons', 129), ('gravure', 'Gravure', 134), ('terrazzo', 'Terrazzo', 125)]
Y0 = 132; S_BAS = 150

def ecran_qui_vend(t, variante, defile=False, ou=''):
    """variante 'A' : les quatre réglages NETS, en aperçu (on lit ce qu'on obtient) ;
       variante 'B' : le mur repris tel quel — floutés 2,4, encart « ✦ Le Cercle » net dessus."""
    c = T[t]; h = []
    for i, (l, v) in enumerate(REGS):
        y = Y0 + i * 80
        h.append('<div class="reg%s" style="top:%dpx;border-color:%s;color:%s"><span class="rl" style="color:%s">%s</span>'
                 '<span class="rv">%s</span></div>' % (' flou' if variante == 'B' else '', y, c['encre'], c['encre'], c['lab'], l, v))
    if variante == 'B':
        h.append('<div class="enc" style="top:%dpx;background:%s;color:%s"><span class="et">✦ Le Cercle</span></div>'
                 % (Y0 + 108, c['enc_fond'], c['enc_tx']))
    for i, (k, nom, pid) in enumerate(MONDES):
        x = 24 + i * 122
        h.append('<img class="dal" src="%s" style="left:%dpx;top:468px">' % (img(os.path.join(P1, 'dalle_%s_%d.png' % (k, pid))), x))
        h.append('<div class="nom" style="left:%dpx;top:574px;color:%s">%s</div>' % (x, c['nom'], nom))
    h.append('<div class="prix" style="top:612px">29 €</div>')
    h.append('<div class="sous" style="top:678px">soit 2,42 €/mois · −39 %</div>')
    h.append('<div class="btn" style="top:722px;background:%s;color:%s;border-color:%s">Prendre l’année</div>' % (c['btn_fond'], c['btn_tx'], c['btn_fond']))
    h.append('<div class="btn b2" style="top:800px;border-color:%s">Essayer 14 jours, puis 3,99 €/mois</div>' % c['encre'])
    h.append('<div class="note" style="top:884px;color:%s">Sans engagement · annulable en 2 taps, à tout moment.</div>' % c['second'])
    h.append('<div class="note" style="top:910px;color:%s">ou un design à l’unité — 1 €, ou 4 pour 3 €</div>' % c['second'])
    # le nom du cadre est UNIQUE dans la planche (le même écran paraît dans le chemin et en section 3 : deux noms
    # identiques ont fait tomber le juge — sélecteur ambigu)
    return ('<div class="fr" data-cadre="vend_%s_%s_%s%s" style="background:%s;color:%s">'
            '<div class="defil" style="top:112px;height:732px"><div class="pg" style="top:%dpx">%s</div></div>'
            '<div class="plat" style="background:%s;border-color:%s"><span class="t">Le Cercle</span><span class="c">✕ Fermer</span></div></div>'
            ) % (variante, t, 'bas' if defile else 'haut', ('_' + ou) if ou else '', c['fond'], c['encre'], -112 - (S_BAS if defile else 0), ''.join(h), c['fond'], c['encre'])

def cap(nom, legende, doigt=None):
    """une capture de l'app ; `doigt` = clé de cotes.json : un anneau d'ANNOTATION (hors produit) sur l'encart"""
    extra = ''
    if doigt and COTES.get(doigt) and COTES[doigt].get('encart') and COTES[doigt]['encart']['vis']:
        # l'anneau se pose au quart droit de l'encart : centré, il masquait le « L » de « Le Cercle »
        e = COTES[doigt]['encart']; cx, cy = e['x'] + e['w'] * 0.82, e['y'] + e['h'] / 2
        extra = '<div class="doigt" style="left:%dpx;top:%dpx"></div>' % (cx - 32, cy - 32)
    return ('<figure><div class="capw"><img class="cap" src="%s">%s</div><figcaption>%s</figcaption></figure>'
            % (img(os.path.join(P2, nom + '.png')), extra, legende))
def fig(html, legende): return '<figure>%s<figcaption>%s</figcaption></figure>' % (html, legende)
FL = '<div class="fl">→</div>'

CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#0E0F12;color:#F4EEE1;font-family:Apfel,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.page{max-width:1900px;margin:0 auto;padding:44px 32px 120px}
h1{font-family:Bricolage;font-weight:700;font-size:38px;letter-spacing:-.02em;margin:0 0 6px}
h2{font-family:Bricolage;font-weight:700;font-size:27px;letter-spacing:-.02em;margin:56px 0 12px}
h3{font-family:Bricolage;font-weight:700;font-size:18px;margin:26px 0 10px;color:#C8C3B6}
.lede,.pr{font-family:Apfel;font-size:15.5px;line-height:1.6;max-width:1080px;color:#C8C3B6;margin:0 0 22px}
.lede b,.pr b,td b,li b{color:#F4EEE1;font-family:ApfelMid;font-weight:500}
.row{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start;margin:0 0 8px}
figure{margin:0}
figcaption{font-family:ApfelMid;font-weight:500;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#8B8778;margin:10px 0 0;width:390px;line-height:1.5}
figcaption b{color:#F4EEE1;font-weight:500}
.capw{position:relative;width:390px;height:844px}
img.cap{width:390px;height:844px;border-radius:38px;display:block}
.doigt{position:absolute;width:64px;height:64px;border-radius:50%;border:3px solid #F4EEE1;outline:3px solid #16171B}
.fl{font-family:Bricolage;font-weight:700;font-size:40px;color:#8B8778;align-self:center;margin-top:-40px}
table.reg{border-collapse:collapse;font-family:Apfel;font-size:14px;line-height:1.5;color:#C8C3B6;max-width:1300px}
table.reg th,table.reg td{border-bottom:2px solid #2A2C34;padding:9px 12px;text-align:left;vertical-align:top}
table.reg th{font-family:Bricolage;font-weight:700;color:#F4EEE1}
.defile{overflow-x:auto;max-width:100%}
ul.l{font-family:Apfel;font-size:14.5px;line-height:1.62;color:#C8C3B6;max-width:1100px}
.fr{position:relative;width:390px;height:844px;overflow:hidden;border-radius:38px;flex:none}
.fr *{position:absolute;margin:0}
.defil{left:0;width:390px;overflow:hidden}
.pg{left:0;width:390px;height:1000px}
.plat{left:24px;top:40px;width:342px;height:60px;border-radius:30px;border:2px solid;display:flex!important;align-items:center;justify-content:space-between;padding:0 22px 0 26px}
.plat>*{position:static!important}
.plat .t{font-family:Bricolage;font-weight:700;font-size:27px;letter-spacing:-.035em}
.plat .c{font-family:ApfelMid;font-weight:500;font-size:12px;letter-spacing:.2em;text-transform:uppercase}
.reg{left:24px;width:342px;height:64px;border:2px solid;border-radius:32px;display:flex!important;align-items:center;justify-content:space-between;padding:0 22px;pointer-events:none}
.reg.flou{filter:blur(2.4px)}
.reg>*{position:static!important}
.rl{font-family:ApfelMid;font-weight:500;font-size:13px;letter-spacing:.18em}
.rv{font-family:Bricolage;font-weight:700;font-size:18px}
.enc{left:24px;width:342px;height:90px;border-radius:26px;display:flex!important;align-items:center;justify-content:center}
.enc>*{position:static!important}
.et{font-family:Bricolage;font-weight:700;font-size:22px;letter-spacing:-.02em;line-height:1}
.dal{width:98px;height:98px;object-fit:contain}
.nom{width:98px;text-align:center;font-family:Bricolage;font-weight:600;font-size:13px;letter-spacing:-.01em}
.prix{left:24px;width:342px;text-align:center;font-family:Bricolage;font-weight:700;font-size:56px;letter-spacing:-.03em;line-height:1}
.sous{left:24px;width:342px;text-align:center;font-family:ApfelMid;font-weight:500;font-size:15px;line-height:1.15}
.btn{left:24px;width:342px;height:62px;border-radius:31px;border:2px solid;display:flex!important;align-items:center;justify-content:center;font-family:Bricolage;font-weight:700;font-size:19px;letter-spacing:-.01em}
.btn.b2{font-size:17px}
.note{left:24px;width:342px;text-align:center;font-family:Apfel;font-weight:400;font-size:14px;line-height:1.3}
"""
H = ['<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="Cache-Control" content="no-store">',
     '<title>Promi — le Cercle · planche 2</title><style>%s\n%s</style></head><body><div class="page">' % (polices, CSS),
     '<h1>Le Cercle — planche 2 : poser le mur là où il manque</h1>',
     '<p class="lede"><b>Rien n’est écrit dans <code>app.html</code>.</b> Le mur et l’état abonné sont des captures de l’app, '
     'avec la brique même de l’app (<code>cercle()</code>) accrochée là où elle manque, le temps de la prise. L’écran qui vend '
     'est composé aux cotes du bloc relevées dans l’app ; ses trois dalles sont peintes par le moteur, dans leur monde. '
     '<b>Tes décisions appliquées :</b> l’encart porte « ✦ Le Cercle », seul (Q201) ; le Studio garde ses libellés (Q200) — '
     'il n’est donc pas redessiné ici.</p>',
     '<p class="pr"><b>Ce qui a été mesuré avant de dessiner, pour que la planche repose sur le vrai :</b> sur une <b>fiche</b>, '
     'le mur existe déjà — un Promi planté à neuf le porte comme les autres (quatre réglages floutés, encart net, deux thèmes). '
     'Ce qui manque partout, c’est la <b>fonction</b> : les réglages ne font rien, même payés. Sur la <b>page +</b>, le mur '
     'n’existe pas. Un <b>gardé de côté</b> rouvre la page + : son Peaufiner s’ouvre bien (par la barre), mais sans le mur.</p>']

H.append('<h2>1 · Le mur qui garde vraiment — gratuit</h2>')
H.append('<p class="pr">Quatre réglages à leur place, <b>floutés à 2,4 px et intouchables</b> (le doigt n’y a pas prise), '
         'l’encart <b>net</b> posé dessus — la seule superposition du produit. Sur la fiche, il existe ; sur la page + et le '
         'gardé de côté, il est <b>posé</b> en fin de liste, après les pièces jointes.</p>')
for t, nom in (('dark', 'sombre'), ('light', 'clair')):
    H.append('<h3>%s</h3><div class="row">%s%s%s%s</div>' % (nom,
        cap('gratuit_fiche_promi_%s' % t, '%s · fiche d’un Promi · <b>existe</b>' % nom),
        cap('gratuit_fiche_chiche_%s' % t, '%s · fiche d’un Chiche · <b>existe</b>' % nom),
        cap('gratuit_pageplus_%s' % t, '%s · page + · <b>posé</b>' % nom),
        cap('gratuit_garde_%s' % t, '%s · gardé de côté · <b>posé</b>' % nom)))

H.append('<h2>2 · Le chemin qui mène à l’écran qui vend</h2>')
H.append('<p class="pr">La fiche → la barre Peaufiner → le mur → <b>on touche l’encart</b> → l’écran qui vend. Le même '
         'encart, au même geste, depuis la page + et le gardé de côté. <b>Après l’achat, on revient là où on était</b> — '
         'devant les quatre réglages, désormais nets : c’est là qu’on les a découverts, c’est là qu’on les voulait. '
         '(Aujourd’hui, l’achat mène à l’Aura.) L’anneau blanc est une annotation de planche : le doigt.</p>')
for t, tt, nom in (('dark', 'dk', 'sombre'), ('light', 'lt', 'clair')):
    H.append('<h3>%s</h3><div class="row">%s%s%s%s%s%s%s</div>' % (nom,
        cap('fiche_promi_repos_%s' % t, '%s · <b>1</b> la fiche, la barre en bas' % nom), FL,
        cap('gratuit_fiche_promi_%s' % t, '%s · <b>2</b> le mur · on touche l’encart' % nom, doigt='gratuit_fiche_promi_%s' % t), FL,
        fig(ecran_qui_vend(tt, 'A', ou='chemin'), '%s · <b>3</b> l’écran qui vend' % nom), FL,
        cap('abonne_fiche_promi_%s' % t, '%s · <b>4</b> après l’achat : même place, nets' % nom)))

H.append('<h2>3 · L’écran qui vend — deux variantes pour ce qu’il montre</h2>')
H.append('<p class="pr"><b>A · les quatre réglages nets</b>, en aperçu : on y lit ce qu’on obtient, puis les trois mondes, '
         'puis le prix. <b>B · le mur repris</b> tel qu’on vient de le toucher : floutés, « ✦ Le Cercle » dessus — mais '
         'l’encart y mène à l’écran où l’on est déjà. Le bas de l’écran est le même dans les deux. Rien n’y compte, rien ne '
         'dit « il vous reste » ; aucun mot neuf.</p>')
H.append('<div class="row">%s%s%s%s</div>' % (
    fig(ecran_qui_vend('dk', 'A'), 'sombre · <b>A</b> · à l’ouverture'), fig(ecran_qui_vend('lt', 'A'), 'clair · <b>A</b> · à l’ouverture'),
    fig(ecran_qui_vend('dk', 'B'), 'sombre · <b>B</b> · à l’ouverture'), fig(ecran_qui_vend('lt', 'B'), 'clair · <b>B</b> · à l’ouverture')))
H.append('<div class="row">%s%s</div>' % (
    fig(ecran_qui_vend('dk', 'A', True), 'sombre · défilé jusqu’au bout'), fig(ecran_qui_vend('lt', 'A', True), 'clair · défilé jusqu’au bout')))

H.append('<h2>4 · L’état abonné — tout redevient net et touchable</h2>')
H.append('<p class="pr">L’encart s’efface, les quatre réglages se lisent et se touchent — sur la fiche, sur la page +, sur '
         'le gardé de côté. C’est ce que l’app sait déjà faire (<code>_cerclePaye</code>) ; <b>ce qu’elle ne sait pas faire, '
         'c’est ce que ces réglages font une fois touchés</b> — voir plus bas.</p>')
for t, nom in (('dark', 'sombre'), ('light', 'clair')):
    H.append('<h3>%s</h3><div class="row">%s%s%s</div>' % (nom,
        cap('abonne_fiche_promi_%s' % t, '%s · fiche' % nom), cap('abonne_pageplus_%s' % t, '%s · page +' % nom),
        cap('abonne_garde_%s' % t, '%s · gardé de côté' % nom)))

H.append('<h2>Ce que la planche ne règle pas — à savoir avant d’intégrer</h2><ul class="l">'
 '<li><b>Ce que font les quatre réglages une fois touchés</b> (importance, récurrence, rappels, mémoire) : aujourd’hui '
 'rien — ce sont des fonctions à écrire (CHANTIERS 18), pas du dessin. Sans elles, l’état abonné est net mais vide.</li>'
 '<li><b>Le Peaufiner de la page + porte deux collisions préexistantes</b>, vues sur les captures : le titre et un second '
 '« ✕ FERMER » se chevauchent sous le plateau, et le rond de la photo tombe sur la rangée AVANT. Le mur y entre : elles '
 'se corrigent dans le même lot.</li>'
 '<li><b>Les défauts d’état de l’audit</b> (fin d’abonnement, « Membre du Cercle » en gratuit, verrou resservi après '
 'l’achat, prix invisibles en clair, achat qui mène à l’Aura) — <code>AUDIT-CERCLE.md</code> § E.</li>'
 '<li><b>L’écran qui vend, vu par un abonné</b> (la porte de l’accueil y mène encore) et <b>le paiement réel</b> — non dessinés.</li>'
 '<li><b>Les Réglages</b> portent le même mur : leur encart suivra « ✦ Le Cercle » (Q201) à l’intégration.</li></ul>')

H.append('<h2>Chaque libellé, et d’où il vient</h2><div class="defile"><table class="reg">'
 '<tr><th>libellé</th><th>d’où il vient</th></tr>'
 '<tr><td>✦ Le Cercle (l’encart du mur)</td><td><b>ta décision</b> (Q201) — il nomme l’offre, pas son contenu</td></tr>'
 '<tr><td>C’EST IMPORTANT ? · RÉCURRENCE · RAPPEL · LA MÉMOIRE, et leurs valeurs</td><td>existant — l’inventaire du §3.8</td></tr>'
 '<tr><td>Le Cercle · ✕ Fermer (plateau de l’écran qui vend)</td><td>existant</td></tr>'
 '<tr><td>Sillons · Gravure · Terrazzo</td><td>existant — les noms des mondes</td></tr>'
 '<tr><td>29 € · soit 2,42 €/mois · −39 %</td><td><b>ta forme, mot pour mot</b></td></tr>'
 '<tr><td>Prendre l’année · Essayer 14 jours, puis 3,99 €/mois · Sans engagement · annulable en 2 taps, à tout moment.</td><td>existant — la page d’aujourd’hui</td></tr>'
 '<tr><td>ou un design à l’unité — 1 €, ou 4 pour 3 €</td><td>existant, gardé pour ne pas perdre un revenu — « 4 pour 3 » n’a aucun achat derrière (Q196.4)</td></tr>'
 '</table></div>')
H.append('</div></body></html>')
open(os.path.join(RACINE, 'PLANCHE-CERCLE-2.html'), 'w', encoding='utf-8').write(''.join(H))
print('écrit PLANCHE-CERCLE-2.html', sum(len(x) for x in H) // 1024, 'Ko')
