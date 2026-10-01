# LE CERCLE — PLANCHE 3 (PLANCHE-CERCLE-3.html, racine). Autonome : six faces et images embarquées.
# Les trois corrections de Tom (11 sept.) : l'ordre des réglages payants · le bandeau du Peaufiner de la page + (défauts
# du produit, masqués et déclarés) · les champs à trois lignes et plus (T, la consigne ; P, le panneau ; mesurés).
import base64, json, os
D = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.abspath(os.path.join(D, '..', '..'))
P3 = os.path.join(D, 'planche3'); P1 = os.path.join(D, 'planche')
def img(ch): return 'data:image/png;base64,' + base64.b64encode(open(ch, 'rb').read()).decode()
polices = open(os.path.join(RACINE, 'planche-polices.css'), encoding='utf-8').read()
COTES = json.load(open(os.path.join(P3, 'cotes.json'), encoding='utf-8'))
MES = json.load(open(os.path.join(P3, 'mesures.json'), encoding='utf-8'))

T = {'dk': dict(fond='#12142A', encre='#F4EEE1', lab='#CBAAFF', enc_fond='#F4EEE1', enc_tx='#AE86F2', second='#A8A396',
                btn_fond='#F4EEE1', btn_tx='#12142A', nom='#C9C4B4'),
     'lt': dict(fond='#F4EEE1', encre='#16171B', lab='#3A54FF', enc_fond='#16171B', enc_tx='#CBAAFF', second='#6B6658',
                btn_fond='#16171B', btn_tx='#F4EEE1', nom='#4A463C')}
# ⚑ L'ORDRE DE TOM : la récurrence d'abord — elle se comprend tout de suite et on en voit l'usage ; l'importance, la plus
# abstraite, en dernier.
REGS = [('RÉCURRENCE', 'chaque semaine'), ('RAPPEL', 'la veille à 19:00'), ('LA MÉMOIRE', 'réveille tes « en l’air »'),
        ("C'EST IMPORTANT ?", '· ·· ···')]
MONDES = [('sillons', 'Sillons', 129), ('gravure', 'Gravure', 134), ('terrazzo', 'Terrazzo', 125)]
Y0 = 132; S_BAS = 150

def ecran_qui_vend(t, variante, defile=False, ou=''):
    c = T[t]; h = []
    for i, (l, v) in enumerate(REGS):
        h.append('<div class="reg%s" style="top:%dpx;border-color:%s;color:%s"><span class="rl" style="color:%s">%s</span>'
                 '<span class="rv">%s</span></div>' % (' flou' if variante == 'B' else '', Y0 + i * 80, c['encre'], c['encre'], c['lab'], l, v))
    if variante == 'B':
        h.append('<div class="enc" style="top:%dpx;background:%s;color:%s"><span class="et">✦ Le Cercle</span></div>' % (Y0 + 108, c['enc_fond'], c['enc_tx']))
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
    return ('<div class="fr" data-cadre="vend_%s_%s_%s%s" style="background:%s;color:%s">'
            '<div class="defil" style="top:112px;height:732px"><div class="pg" style="top:%dpx">%s</div></div>'
            '<div class="plat" style="background:%s;border-color:%s"><span class="t">Le Cercle</span><span class="c">✕ Fermer</span></div></div>'
            ) % (variante, t, 'bas' if defile else 'haut', ('_' + ou) if ou else '', c['fond'], c['encre'], -112 - (S_BAS if defile else 0), ''.join(h), c['fond'], c['encre'])

def cap(nom, legende, doigt=None):
    extra = ''
    if doigt and COTES.get(doigt) and COTES[doigt].get('encart') and COTES[doigt]['encart']['vis']:
        e = COTES[doigt]['encart']; cx, cy = e['x'] + e['w'] * 0.82, e['y'] + e['h'] / 2
        extra = '<div class="doigt" style="left:%dpx;top:%dpx"></div>' % (cx - 32, cy - 32)
    return ('<figure><div class="capw"><img class="cap" src="%s">%s</div><figcaption>%s</figcaption></figure>'
            % (img(os.path.join(P3, nom + '.png')), extra, legende))
def fig(html, legende): return '<figure>%s<figcaption>%s</figcaption></figure>' % (html, legende)
FL = '<div class="fl">→</div>'

CSS = open(os.path.join(D, 'planche2_build.py'), encoding='utf-8').read().split('CSS = r"""')[1].split('"""')[0]
CSS += "\n.num{font-family:ApfelMid;font-weight:500;color:#F4EEE1} td.ko{color:#FFB08A} td.ok{color:#8FE3B8}\n"

H = ['<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="Cache-Control" content="no-store">',
     '<title>Promi — le Cercle · planche 3</title><style>%s\n%s</style></head><body><div class="page">' % (polices, CSS),
     '<h1>Le Cercle — planche 3 : tes trois corrections</h1>',
     '<p class="lede"><b>Rien n’est écrit dans <code>app.html</code>.</b> Tout ce qui diffère de l’app sur ces captures est '
     'posé dans la page le temps de la prise, et <b>déclaré ici</b> :</p><ul class="l">'
     '<li><b>1 · L’ordre des réglages payants</b> — RÉCURRENCE · RAPPEL · LA MÉMOIRE · C’EST IMPORTANT ? — partout où ils '
     'paraissent : le mur, l’état abonné, l’écran qui vend.</li>'
     '<li><b>2 · Le bandeau du Peaufiner de la page +</b> — <b>masqué</b> sur ces captures. Vérifié par un chemin utilisateur '
     'pur (des touchers, aucune retouche) : les deux défauts sont AU PRODUIT, aucun ne vient de la maquette — la pastille de '
     'la page + (<code>.enh</code>) reste peinte sous l’en-tête du Peaufiner, son « FERMER » tombe sur le titre (confirmé au '
     'doigt, deux thèmes) ; le rond photo de la page + (<code>.ph-photo-btn</code>) reste peint sur la rangée AVANT. '
     'Ils sont notés en chantier. Masqués, l’en-tête devient celui du Peaufiner d’une fiche.</li>'
     '<li><b>3 · Les champs à trois lignes</b> — la version <b>T</b> (ta consigne) est appliquée sur les captures du mur, du '
     'chemin et de l’état abonné ; la section 5 montre <b>T et P</b>, mesurés, et c’est la question de ce tour.</li></ul>']

H.append('<h2>1 · Le mur — gratuit</h2><p class="pr">La récurrence en tête. Quatre réglages floutés à 2,4 px et intouchables, '
         '« ✦ Le Cercle » net dessus. Sur la fiche il existe ; sur la page + et le gardé de côté il est posé en fin de liste.</p>')
for t, nom in (('dark', 'sombre'), ('light', 'clair')):
    H.append('<h3>%s</h3><div class="row">%s%s%s%s</div>' % (nom,
        cap('gratuit_fiche_promi_%s' % t, '%s · fiche d’un Promi' % nom), cap('gratuit_fiche_chiche_%s' % t, '%s · fiche d’un Chiche' % nom),
        cap('gratuit_pageplus_%s' % t, '%s · page +' % nom), cap('gratuit_garde_%s' % t, '%s · gardé de côté' % nom)))

H.append('<h2>2 · Le chemin</h2><p class="pr">La fiche → le mur, on touche l’encart → l’écran qui vend → après l’achat, '
         'retour au même Peaufiner, réglages nets. L’anneau blanc est une annotation de planche : le doigt.</p>')
for t, tt, nom in (('dark', 'dk', 'sombre'), ('light', 'lt', 'clair')):
    H.append('<h3>%s</h3><div class="row">%s%s%s%s%s%s%s</div>' % (nom,
        cap('fiche_promi_repos_%s' % t, '%s · <b>1</b> la fiche' % nom), FL,
        cap('gratuit_fiche_promi_%s' % t, '%s · <b>2</b> le mur · on touche l’encart' % nom, doigt='gratuit_fiche_promi_%s' % t), FL,
        fig(ecran_qui_vend(tt, 'A', ou='chemin'), '%s · <b>3</b> l’écran qui vend' % nom), FL,
        cap('abonne_fiche_promi_%s' % t, '%s · <b>4</b> après l’achat : nets' % nom)))

H.append('<h2>3 · L’écran qui vend — A ou B (toujours ouvert)</h2><p class="pr"><b>A</b> : les quatre réglages nets, en '
         'aperçu. <b>B</b> : le mur repris. Même bas pour les deux.</p>')
H.append('<div class="row">%s%s%s%s</div>' % (
    fig(ecran_qui_vend('dk', 'A'), 'sombre · <b>A</b>'), fig(ecran_qui_vend('lt', 'A'), 'clair · <b>A</b>'),
    fig(ecran_qui_vend('dk', 'B'), 'sombre · <b>B</b>'), fig(ecran_qui_vend('lt', 'B'), 'clair · <b>B</b>')))
H.append('<div class="row">%s%s</div>' % (fig(ecran_qui_vend('dk', 'A', True), 'sombre · défilé'), fig(ecran_qui_vend('lt', 'A', True), 'clair · défilé')))

H.append('<h2>4 · L’état abonné — net et touchable</h2>')
for t, nom in (('dark', 'sombre'), ('light', 'clair')):
    H.append('<h3>%s</h3><div class="row">%s%s%s</div>' % (nom, cap('abonne_fiche_promi_%s' % t, '%s · fiche' % nom),
        cap('abonne_pageplus_%s' % t, '%s · page +' % nom), cap('abonne_garde_%s' % t, '%s · gardé de côté' % nom)))

def ligne_mes(nom, m, ref):
    def cl(v): return 'ok' if v is not None and v >= ref - 0.5 else 'ko'
    return ('<tr><td>%s</td><td class="num">%s</td><td class="%s">%s</td><td class="%s">%s</td><td>%s</td></tr>'
            % (nom, m['lignes'], cl(m['premiere']), m['premiere'], cl(m['derniere']), m['derniere'], m['air_min']))
ref = MES['reference · dark']; cible = min(ref['premiere'], ref['derniere'])
H.append('<h2>5 · Les champs à trois lignes et plus — T ou P : la question de ce tour</h2>')
H.append('<p class="pr"><b>La mesure :</b> la distance entre le DÉBUT de la ligne (coin haut-gauche dans la moitié haute, '
         'bas-gauche dans la moitié basse) et la courbe intérieure du contour. <b>La norme</b> est celle que le produit tient déjà '
         'sur son champ à deux lignes (PIÈCES JOINTES de la fiche) : <b>%.1f / %.1f</b>, avec %.1f d’air entre ses deux lignes. '
         'Un réglage d’une ligne est à 21,9 : sa ligne est au milieu, loin des courbes.</p>' % (ref['premiere'], ref['derniere'], ref['air_min']))
H.append('<p class="pr"><b>Pourquoi l’interligne seul ne suffit pas.</b> Depuis la grammaire des contours (rayon = hauteur ÷ '
         '2), un champ de 118 est une pilule de rayon 59 : la courbe occupe toute la hauteur, la première et la dernière ligne la '
         'rencontrent forcément. Tenir 13 à trois lignes dans cette boîte ne laisse <b>aucun air</b> entre les lignes (mesuré : '
         '~0 px) ; dans la boîte de 104 d’une Nuée, les lignes <b>se chevauchent</b> ; à quatre lignes, c’est impossible. '
         '(Le §3.4 d’origine dessinait ces champs au rayon 22.)</p>'
         '<ul class="l"><li><b>T · ta consigne</b> — l’interligne resserré, jamais sous l’air du champ à deux lignes, le texte '
         'recentré ; la boîte et son rayon ne bougent pas.</li>'
         '<li><b>P · le panneau</b> — à trois lignes et plus, le champ prend le rayon 30 du grand panneau de la grammaire ; '
         'l’interligne ne bouge pas.</li>'
         '<li>Dans les deux : la carte PIÈCES JOINTES de la Nuée prend les places de celle de la fiche (même champ, il était à '
         '6,35).</li></ul>')
H.append('<div class="defile"><table class="reg"><tr><th>champ</th><th>lignes</th><th>début de la 1re</th><th>début de la dernière</th><th>air entre les lignes (min)</th></tr>')
H.append(ligne_mes('<b>référence</b> · PIÈCES JOINTES de la fiche', ref, cible))
for cas, lab in (('note3', 'NOTE · trois lignes'), ('note4', 'NOTE · quatre lignes (texte long)')):
    for v in ('avant', 'T', 'P'):
        H.append(ligne_mes('%s · <b>%s</b>' % (lab, v), MES['%s · %s · dark' % (cas, v)], cible))
for v in ('avant', 'T', 'P'):
    m = MES['nuee · %s · dark' % v]
    for k, lab in (('npDesc', 'Nuée · DESCRIPTION'), ('npComm', 'Nuée · COMMENTAIRES'), ('npFich', 'Nuée · PIÈCES JOINTES')):
        H.append(ligne_mes('%s · <b>%s</b>' % (lab, v), m[k], cible))
H.append('</table></div><p class="pr">Vert : au niveau de la référence (à 0,5 près). Orange : en dessous. Mesures en thème '
         'sombre ; la géométrie est la même en clair.</p>')
for t, nom in (('dark', 'sombre'), ('light', 'clair')):
    for cas, lab in (('note3', 'NOTE, trois lignes'), ('note4', 'NOTE, quatre lignes')):
        mt = MES.get('%s · T · %s' % (cas, t), {})
        legT = ('%s · <b>T</b> · sans effet : la boîte est pleine' % nom) if mt.get('sans_effet') else ('%s · <b>T</b> · la consigne' % nom)
        H.append('<h3>%s · %s</h3><div class="row">%s%s%s</div>' % (nom, lab,
            cap('lignes_%s_avant_%s' % (cas, t), '%s · <b>aujourd’hui</b>' % nom), cap('lignes_%s_T_%s' % (cas, t), legT),
            cap('lignes_%s_P_%s' % (cas, t), '%s · <b>P</b> · le panneau' % nom)))
    H.append('<h3>%s · le Peaufiner d’une Nuée</h3><div class="row">%s%s%s</div>' % (nom,
        cap('lignes_nuee_avant_%s' % t, '%s · <b>aujourd’hui</b>' % nom), cap('lignes_nuee_T_%s' % t, '%s · <b>T</b>' % nom),
        cap('lignes_nuee_P_%s' % t, '%s · <b>P</b>' % nom)))

H.append('<h2>Ce qui reste, et où</h2><ul class="l">'
 '<li><b>Chantier noté</b> : le bandeau du Peaufiner de la page + (pastille et « FERMER » sous le titre, rond photo sur '
 'AVANT) — au produit, masqués ici.</li>'
 '<li><b>Vu en mesurant, pas corrigé</b> : la carte LE TRAIT d’une Nuée (118, libellé + rail de pinceaux) a son libellé à '
 '5,3 de la courbe.</li>'
 '<li><b>Ce que font les quatre réglages une fois touchés</b> : rien encore — des fonctions à écrire.</li>'
 '<li><b>Les défauts d’état de l’audit</b> — <code>AUDIT-CERCLE.md</code> § E.</li></ul>')
H.append('</div></body></html>')
open(os.path.join(RACINE, 'PLANCHE-CERCLE-3.html'), 'w', encoding='utf-8').write(''.join(H))
print('écrit PLANCHE-CERCLE-3.html', sum(len(x) for x in H) // 1024, 'Ko')
