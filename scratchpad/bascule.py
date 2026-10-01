# -*- coding: utf-8 -*-
"""LA BASCULE — palette et polices, en une passe, sur une COPIE.
   1 · la VALEUR de chaque couleur (hex et rgb) passe à celle du jeu
   2 · les polices passent par des variables de famille
   3 · un bloc de tokens est inséré : faces embarquées, palette fixe, rôles clair/sombre, niveaux de texte
   4 · dans les <style>, plus aucune couleur en dur : tout passe par une variable FIXE
       (fixe, jamais un rôle : une règle qui peint la crème en sombre et l'encre en clair
        serait inversée par un rôle qui suit le mode — le piège serait invisible)"""
import sys, re, io, json, collections
sys.path.insert(0,'scratchpad')
from couleurs_lab import *
from table_palette import table as _bascule
from jeu_tokens import ROLES, TYPO, FAMILLES, clair, sombre, B as BJEU

SRC = 'sauvegardes/app-avant-PALETTE-16sept.html'   # la version d'AVANT : la bascule se rejoue toujours depuis elle
DST = sys.argv[1] if len(sys.argv)>1 else 'app-palette.html'

S = io.open(SRC, encoding='utf-8').read()

# ── on met les base64 à l'abri ────────────────────────────────────────────────
COFFRE = []
def _garde(m):
    COFFRE.append(m.group(0)); return f"\x00B64_{len(COFFRE)-1}\x00"
S = re.sub(r'base64,[A-Za-z0-9+/=]+', _garde, S)

# ── 1 · la table de valeurs ───────────────────────────────────────────────────
T = dict(BJEU)                       # avant → après (hex majuscules)
def norm(h):
    h = h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    return '#'+h.upper()

nb_hex = 0
def _sub_hex(m):
    global nb_hex
    h = norm(m.group(0))
    if h in T and T[h]!=h:
        nb_hex += 1
        return T[h]
    return m.group(0)
S = re.sub(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', _sub_hex, S)

# ⚑ UNE MÊME VALEUR, DEUX RÔLES — #12142A. Le fichier l'emploie pour deux choses :
#   « LE CORPS DU THÈME — #F4EEE1 en clair, #12142A en sombre » (les plateaux, la recherche,
#   le tri, les écrans Langue · Confidentialité · Cercle, le partage) ET le corps de fiche
#   d'un Promi en sombre (§3). Le premier est un FOND : il devient le brun. Le second est une
#   NATURE : il ne bouge pas. On les sépare au sélecteur, pas à la valeur.
FICHE_PROMI = ('dp-promi','pp-promi','dpd-corps')
def _desambigue(txt):
    out=[]; i=0; n=0
    for m in re.finditer(r'#12142A', txt, re.I):
        amont = txt[max(0,m.start()-260):m.start()]
        garde = any(k in amont for k in FICHE_PROMI)
        out.append(txt[i:m.start()]); out.append(m.group(0) if garde else '#201908')
        if not garde: n+=1
        i=m.end()
    out.append(txt[i:])
    return ''.join(out), n
S, nb_desa = _desambigue(S)

# les mêmes couleurs écrites en rgb()/rgba()
TRIP = {}
for a,b in T.items():
    if a==b: continue
    TRIP[hex2rgb(a)] = hex2rgb(b)
nb_rgb = 0
def _sub_rgb(m):
    global nb_rgb
    r,g,bl = int(m.group(2)),int(m.group(3)),int(m.group(4))
    if (r,g,bl) in TRIP:
        nr,ng,nb_ = TRIP[(r,g,bl)]
        nb_rgb += 1
        return f"{m.group('f')}({nr},{ng},{nb_}{m.group('rest')})"
    return m.group(0)
S = re.sub(r'(?P<f>rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?P<rest>[^)]*)\)', _sub_rgb, S)

# ── 2 · les polices ───────────────────────────────────────────────────────────
POL = [
 ("Fraunces,Georgia,serif",        "var(--f-titre)"),
 ("Fraunces",                      "var(--f-titre)"),
 ("ApfelMid,Apfel,system-ui,sans-serif", "var(--f-texte)"),
 ("ApfelMid,system-ui,sans-serif", "var(--f-texte)"),
 ("ApfelMid,sans-serif",           "var(--f-texte)"),
 ("ApfelMid",                      "var(--f-texte)"),
 ("Apfel,system-ui,sans-serif",    "var(--f-texte)"),
 ("Apfel",                         "var(--f-texte)"),
 ("Bricolage,system-ui,sans-serif","var(--f-libelle)"),
 ("Bricolage,sans-serif",          "var(--f-libelle)"),
 ("Bricolage",                     "var(--f-libelle)"),
]
# ⚠ LES @font-face NE SONT PAS DES VUES. Mettre `font-family:var(--f-titre)` DANS une
#   déclaration de face la détruit : une custom property n'y est pas valide, et la face
#   disparaît en silence. Mesuré : les six faces d'origine effacées, Fraunces tombée sur
#   Georgia, et `redteam_polices` n'en voyait plus que quatre. On les met au coffre.
# ⚑ LA PREMIÈRE FAMILLE DÉCIDE. Une liste s'écrit de dix façons — `Bricolage,system-ui,sans-serif`,
#   `'Bricolage',-apple-system,…`, `'Bricolage Grotesque',Bricolage,…`, `'Fraunces',Bricolage,serif` —
#   et une liste d'égalités en rate toujours une : au premier essai, 217 mentions avaient survécu,
#   dont les avatars d'une Nuée et tout l'onboarding. On lit donc la PREMIÈRE famille de la liste.
VERS = {
  'fraunces':'var(--f-titre)',
  'bricolage':'var(--f-libelle)', 'bricolage grotesque':'var(--f-libelle)',
  'apfel':'var(--f-texte)', 'apfelmid':'var(--f-texte)', 'apfel grotezk':'var(--f-texte)',
}
def _pol_valeur(v):
    tete = v.strip().split(',')[0].strip().strip('\'"').lower()
    return VERS.get(tete)
COFFRE_FACE = []
def _garde_face(m):
    COFFRE_FACE.append(m.group(0)); return f"\x00FACE_{len(COFFRE_FACE)-1}\x00"
S = re.sub(r'@font-face\{[^}]*\}', _garde_face, S)

nb_pol = 0
def _sub_pol(m):
    global nb_pol
    val = m.group('v').strip()
    imp = ''
    if val.endswith('!important'):
        val = val[:-len('!important')].strip(); imp='!important'
    ap = _pol_valeur(val)
    if ap is None: return m.group(0)
    nb_pol += 1
    return f"{m.group('p')}font-family:{ap}{imp}"
# ⚠ la valeur peut contenir des guillemets — `font-family:'Fraunces',Georgia,serif`. Un motif
#   qui les EXCLUT s'arrête avant et ne voit rien : 31 appels avaient survécu à ce titre
#   (le mot-marque, la signature, le grand chiffre de l'Aura, tout l'onboarding).
S = re.sub(r"""(?P<p>)font-family\s*:\s*(?P<v>(?:'[^']*'|"[^"]*"|[^;}'"])+)""", _sub_pol, S)

# ⚠ ET LA FORME OBJET JS : `pose(el, {'font-family':'Bricolage,system-ui,sans-serif', …})`.
#   La clé est entre guillemets, donc le motif « font-family: » ne la voit pas. C'est par là
#   que le Peaufiner d'une Nuée gardait ses 22 éléments en Bricolage et ApfelMid.
def _sub_obj(m):
    global nb_pol
    ap = _pol_valeur(m.group(2))
    if ap is None: return m.group(0)
    nb_pol += 1
    return f"{m.group(1)}font-family{m.group(1)}:{m.group(1)}{ap}{m.group(1)}"
S = re.sub(r"""(['"])font-family\1\s*:\s*\1([^'"]+)\1""", _sub_obj, S)

# ⚠ ET LE CANVAS : `g.font='700 42px Bricolage,system-ui,sans-serif'`. Un canvas ne lit pas
#   une variable CSS — on y pose donc la PILE en clair (le grand chiffre de l'Aura, le sceau
#   du partage et les barres du Noyau y sont peints).
PILE_CANVAS = {'var(--f-titre)':'Fraunces,Georgia,serif',
               'var(--f-libelle)':'Gilbert,Bricolage,system-ui,sans-serif',
               'var(--f-texte)':'Atkinson,Apfel,system-ui,sans-serif'}
def _sub_cnv(m):
    global nb_pol
    ap = _pol_valeur(m.group(2))
    if ap is None: return m.group(0)
    nb_pol += 1
    return m.group(1) + PILE_CANVAS[ap]
S = re.sub(r"((?:\d+\s+)?[\d.]+px\s+)((?:Fraunces|Bricolage|Apfel|ApfelMid)[^'\"]*)", _sub_cnv, S)

# ⚠ TROIS AUTRES FAÇONS D'APPELER UNE POLICE, et le relevé les a trouvées toutes les trois :
#   · l'attribut SVG `font-family="…"` (10 nœuds : les avatars de la Nuée)
#   · le raccourci `font:700 13px/1 Bricolage,system-ui`
#   · une liste écrite avec des espaces après les virgules
def _sub_attr(m):
    global nb_pol
    ap = _pol_valeur(m.group(2))
    if ap is None: return m.group(0)
    nb_pol += 1
    return f'font-family={m.group(1)}{ap}{m.group(1)}'
S = re.sub(r"""font-family\s*=\s*(["'])([^"']+)\1""", _sub_attr, S)
def _sub_racc(m):
    global nb_pol
    tete, fam = m.group(1), m.group(2)
    ap = _pol_valeur(fam)
    if ap is None: return m.group(0)
    nb_pol += 1
    return f"font:{tete}{ap}"
S = re.sub(r"font\s*:\s*((?:\d+\s+)?[\d.]+px(?:/[\d.]+)?\s+)([A-Za-z][^;}\"')]*)", _sub_racc, S)

S = re.sub(r'\x00FACE_(\d+)\x00', lambda m: COFFRE_FACE[int(m.group(1))], S)

# ── 3 · le bloc de tokens ─────────────────────────────────────────────────────
# toutes les couleurs présentes dans les <style>, après bascule
styles = re.findall(r'<style[^>]*>(.*?)</style>', S, re.S)
def sans_commentaires(css): return re.sub(r'/\*.*?\*/','',css,flags=re.S)
hexs = collections.Counter(); trips = collections.Counter()
for b in styles:
    c = sans_commentaires(b)
    for x in re.findall(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', c): hexs[norm(x)]+=1
    for m in re.finditer(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)[^)]*\)', c):
        trips[(int(m.group(1)),int(m.group(2)),int(m.group(3)))]+=1

def famille(h):
    L,C,hh = lch(h)
    if C < 2:
        if L>96: return 'blanc'
        if L<4:  return 'noir'
        return 'gris'
    if L>=70 and C<26 and 40<=hh<=115: return 'creme'
    if 22<L<78 and C<22 and 40<=hh<=115: return 'beige'
    if L<=26 and 40<=hh<=115: return 'brun'
    if 25<=hh<=62 and C>=30: return 'orange'
    if 0<=hh<35 or hh>=340: return 'framboise'
    if 120<=hh<=200: return 'menthe'
    if 280<=hh<300 and C>=25: return 'bleu'
    if 300<=hh<340: return 'mauve'
    if 255<=hh<280: return 'periwinkle'
    return 'ton'

NOM = {}; pris=set()
for h,_ in sorted(hexs.items(), key=lambda kv:(-kv[1],kv[0])):
    L = lch(h)[0]
    base = f"--c-{famille(h)}{int(round(L)):02d}"
    n = base; k=1
    while n in pris: k+=1; n=f"{base}-{k}"
    pris.add(n); NOM[h]=n
NOMT = {}
for t,_ in sorted(trips.items(), key=lambda kv:-kv[1]):
    h = rgb2hex(*t)
    if h in NOM: NOMT[t] = NOM[h]+'-rgb'
    else:
        L = lch(h)[0]
        base = f"--c-{famille(h)}{int(round(L)):02d}"
        n=base; k=1
        while n in pris: k+=1; n=f"{base}-{k}"
        pris.add(n); NOM[h]=n; NOMT[t]=n+'-rgb'

decl = []
for h,n in sorted(NOM.items(), key=lambda kv: kv[1]):
    decl.append(f"{n}:{h}")
for t,n in sorted(NOMT.items(), key=lambda kv: kv[1]):
    decl.append(f"{n}:{t[0]},{t[1]},{t[2]}")

def role_css(mode):
    out=[]
    for nom,v in ROLES.items():
        val = clair(v) if mode=='clair' else sombre(v)
        out.append(f"--p-{nom}:{val}")
    return ';'.join(out)

import base64, os
# ⚑ LES MÉTRIQUES DES FACES NEUVES SONT CALÉES SUR CELLES QU'ELLES REMPLACENT.
#   Sans cela le changement de police déplace les cotes : la boîte de Gilbert fait 1,250 em
#   là où Bricolage fait 1,188 — mesuré, 9 paires de textes resserrées de 1 à 2 px
#   (redteam_air), dont la phrase d'un gardé de côté et les libellés de dalles de l'Aura.
#   C'est le piège du §8 : « une cote dérivée n'est pas un espace ».
#   On ne touche AUCUN glyphe (la licence de Gilbert l'interdit) : ascent/descent/line-gap
#   sont des métriques de mise en page, lues par le moteur de texte, pas des dessins.
#     Bricolage  hhea 930 / −270 / gap 0     upm 1000
#     Apfel      hhea 932 / −280 / gap 70    upm 1000
METRIQUES = {
  'Gilbert' : 'ascent-override:93%;descent-override:27%;line-gap-override:0%;',   # comme Bricolage
  'Atkinson': 'ascent-override:93.2%;descent-override:28%;line-gap-override:7%;', # comme Apfel
}
def _face(fam, poids, fichier):
    d = base64.b64encode(io.open(os.path.join('polices',fichier),'rb').read()).decode()
    return ("@font-face{font-family:%s;font-weight:%d;font-style:normal;font-display:swap;%s"
            "src:url(data:font/woff2;base64,%s) format('woff2')}" % (fam,poids,METRIQUES[fam],d))
FACES = "\n".join([
  _face('Gilbert',700,'Gilbert-Bold.woff2'),
  _face('Atkinson',400,'Atkinson-Regular.woff2'),
  _face('Atkinson',500,'Atkinson-Medium.woff2'),
  _face('Atkinson',700,'Atkinson-Bold.woff2'),
])

niveaux = []
for nom,d in TYPO.items():
    f = FAMILLES[d['famille']]
    niveaux.append(f"--t-{nom}-taille:{d['taille']}px")
    niveaux.append(f"--t-{nom}-poids:{d['poids']}")
classes = []
for nom,d in TYPO.items():
    maj = 'text-transform:uppercase;' if d['capitales'] else ''
    op  = f"opacity:{d['opacite']};" if d['opacite']<1 else ''
    fam = '--f-libelle' if d['famille']=='libelle' else ('--f-titre' if d['famille']=='titre' else '--f-texte')
    classes.append(f".t-{nom}{{font-family:var({fam});font-weight:{d['poids']};font-size:{d['taille']}px;{maj}{op}}}")

BLOC = f"""<style id="lot-TOKENS-css">
/* ⚑ LE JEU DE COULEURS ET DE POLICES — source unique (Tom, 16 septembre 2026).
   Aucune vue n'appelle une police ni un hexadécimal en dur : tout passe par ce bloc.
   Généré depuis PROMI-TOKENS.json — ne pas modifier à la main, régénérer.

   POLICES · Gilbert Bold (CC BY-SA 4.0, Ogilvy & Mather / Type With Pride — crédit obligatoire
   dans « à propos », glyphes non modifiables) pour les sous-titres, libellés et la navigation,
   en capitales. Atkinson Hyperlegible Next (SIL OFL 1.1, Braille Institute of America) pour tout
   le texte. Les titres gardent Fraunces — elle sera remplacée plus tard.

   COULEURS · deux niveaux, et l'ordre compte :
   · --c-*  la palette FIXE, une valeur par couleur. C'est ce que les règles emploient.
   · --p-*  les RÔLES, qui basculent avec le mode. C'est ce que le portage Swift emploie.
   Une règle ne doit jamais employer un rôle à la place d'une valeur fixe : le produit peint
   souvent la crème en mode sombre et l'encre en mode clair — un rôle les inverserait. */
{FACES}
:root{{
  --f-titre:{FAMILLES['titre']['css']};
  --f-libelle:{FAMILLES['libelle']['css']};
  --f-texte:{FAMILLES['texte']['css']};
  {';'.join(niveaux)};
  {';'.join(decl)};
  {role_css('sombre')}
}}
#device.light,.device.light,.frame.light,.light{{ {role_css('clair')} }}
{chr(10).join(classes)}
</style>
"""

# insertion juste après le dernier @font-face d'origine
m = list(re.finditer(r"@font-face\{[^}]*\}", S))[-1]
pos = S.index('</style>', m.end())
S = S[:pos+len('</style>')] + "\n" + BLOC + S[pos+len('</style>'):]

# ── 4 · dans les <style>, plus aucune couleur en dur ──────────────────────────
nb_var = 0
def var_css(bloc):
    global nb_var
    # on laisse les commentaires tels quels
    parts = re.split(r'(/\*.*?\*/)', bloc, flags=re.S)
    for i in range(0,len(parts),2):
        def _h(m):
            global nb_var
            h = norm(m.group(0))
            if h in NOM: nb_var += 1; return f"var({NOM[h]})"
            return m.group(0)
        parts[i] = re.sub(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', _h, parts[i])
        def _r(m):
            global nb_var
            t=(int(m.group(2)),int(m.group(3)),int(m.group(4)))
            if t in NOMT:
                nb_var += 1
                return f"{m.group(1)}(var({NOMT[t]}){m.group(5)})"
            return m.group(0)
        parts[i] = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)([^)]*)\)', _r, parts[i])
    return ''.join(parts)

def _style(m):
    tete, corps = m.group(1), m.group(2)
    if 'lot-TOKENS-css' in tete: return m.group(0)
    return tete + var_css(corps) + '</style>'
S = re.sub(r'(<style[^>]*>)(.*?)</style>', _style, S, flags=re.S)
S_APP = S

# ── 5 · la table de report du §6 suit les nouvelles faces ────────────────────
AV_FACES = """  var FACES = {
    'fraunces|600|normal':1, 'fraunces|600|italic':1,
    'bricolage|600|normal':1, 'bricolage|700|normal':1,
    'apfel|400|normal':1, 'apfelmid|500|normal':1
  };
  var NOTRE = {fraunces:1, bricolage:1, apfel:1, apfelmid:1};"""
AP_FACES = """  var FACES = {
    'fraunces|600|normal':1, 'fraunces|600|italic':1,
    'gilbert|700|normal':1,
    'atkinson|400|normal':1, 'atkinson|500|normal':1, 'atkinson|700|normal':1,
    'bricolage|600|normal':1, 'bricolage|700|normal':1,
    'apfel|400|normal':1, 'apfelmid|500|normal':1
  };
  var NOTRE = {fraunces:1, gilbert:1, atkinson:1, bricolage:1, apfel:1, apfelmid:1};"""
assert S_APP.count(AV_FACES)==1, "bloc FACES du lot-POLICES introuvable"
S_APP = S_APP.replace(AV_FACES, AP_FACES)

AV_REP = """  function report(fam, w, st){
    if(fam === 'apfel'){"""
AP_REP = """  function report(fam, w, st){
    /* ⚑ 16 sept. 2026 — Gilbert Bold (une seule graisse) porte les sous-titres, les libellés
       et la navigation ; Atkinson Hyperlegible porte tout le texte, en 400 · 500 · 700.
       Aucune italique n'est embarquée dans ces deux familles : l'oblique était déjà
       synthétique en Apfel, et le report la retirait — il la retire pareillement ici. */
    if(fam === 'gilbert')  return ['Gilbert', 700, 'normal'];
    if(fam === 'atkinson'){
      if(st === 'italic') return ['Atkinson', 400, 'normal'];
      if(w >= 600)        return ['Atkinson', 700, 'normal'];
      if(w >= 450)        return ['Atkinson', 500, 'normal'];
      return ['Atkinson', 400, 'normal'];
    }
    if(fam === 'apfel'){"""
assert S_APP.count(AV_REP)==1, "bloc report du lot-POLICES introuvable"
S_APP = S_APP.replace(AV_REP, AP_REP)

# ⚑ LA GRAISSE NE CHANGE PAS. L'ancienne table écrasait Apfel 500·600·700·800 sur ApfelMid 500,
#   faute de plus gras dans la famille. Atkinson, elle, EMBARQUE un 700 : rendue telle quelle,
#   la table aurait fait passer en gras tout ce qui demandait 700 dans la feuille — « libellé du
#   geste » et « pastille » mesurés à 500 → 700 au contrat visuel. Le lot change la POLICE, pas
#   la hiérarchie : Atkinson 500 reçoit donc tout ce que ApfelMid 500 recevait. La face 700 reste
#   embarquée pour le niveau « accentué » du jeu (.t-accent), où elle est demandée nommément.
AV_ATK = """      if(w >= 600)        return ['Atkinson', 700, 'normal'];
      if(w >= 450)        return ['Atkinson', 500, 'normal'];"""
AP_ATK = """      if(w >= 450)        return ['Atkinson', 500, 'normal'];   /* comme ApfelMid 500 hier : la hiérarchie ne bouge pas */"""
assert S_APP.count(AV_ATK)==1
S_APP = S_APP.replace(AV_ATK, AP_ATK)

# ⚑ LES COTES DE LIBELLÉ SONT RELEVÉES, PAS MESURÉES AU MOMENT DE PEINDRE (§8). Elles servent à
#   décaler la dalle d'une carte d'Index sous son libellé de nature. Gilbert est plus étroit que
#   Bricolage : relevé police chargée, Promi 64,48 → 53,63 · Chiche 71,86 → 59,67 · Nuée 59,03 → 50,84.
AV_COTE = "var W={'Promi':65,'Chiche':72,'Nuée':60};"
AP_COTE = "var W={'Promi':54,'Chiche':60,'Nuée':51};"
assert S_APP.count(AV_COTE)==3, S_APP.count(AV_COTE)
S_APP = S_APP.replace(AV_COTE, AP_COTE)

# ⚑ DEUX PROPRIÉTAIRES POUR UNE MÊME PROPRIÉTÉ (§7) — et il a fallu le mesurer pour le voir.
#   `pose()` écrit un style EN LIGNE sur le Peaufiner d'une Nuée, font-family comprise.
#   `lot-POLICES` retire son PROPRE inline avant de relire la cascade — mais il retirait aussi
#   celui de `pose()`, qui vit sur la même propriété. Tant que la feuille demandait
#   « Bricolage 600 », la face existait et le lot ne touchait à rien. Avec « Gilbert 600 »,
#   qui n'existe pas (Gilbert n'a qu'une graisse), il reporte, pose, puis DÉTRUIT l'inline
#   de `pose()` au passage suivant : l'élément retombait sur la police héritée.
#   Mesuré : `.np-bas` rendu en Atkinson 14 (boîte 18) au lieu de Gilbert 14 (boîte 17) —
#   d'où trois paires de textes resserrées d'un pixel au Peaufiner d'une Nuée.
#   Parade : on défait EXACTEMENT ce qu'on a fait — la valeur d'avant est notée avant d'écrire,
#   et remise avant de relire. (Même leçon que « une sonde défait exactement ce qu'elle a fait ».)
AV_RETIRE = """        if(e.getAttribute && e.getAttribute('data-pol') === '1'){
          e.style.removeProperty('font-family');
          e.style.removeProperty('font-weight');
          e.style.removeProperty('font-style');
        }"""
AP_RETIRE = """        if(e.getAttribute && e.getAttribute('data-pol') === '1'){
          _rendre(e);
        }"""
assert S_APP.count(AV_RETIRE)==1, "bloc de retrait du lot-POLICES introuvable"
S_APP = S_APP.replace(AV_RETIRE, AP_RETIRE)

AV_RETIRE2 = """          if(e.getAttribute && e.getAttribute('data-pol') === '1'){
            e.style.removeProperty('font-family'); e.style.removeProperty('font-weight');
            e.style.removeProperty('font-style'); e.removeAttribute('data-pol');
          }"""
AP_RETIRE2 = """          if(e.getAttribute && e.getAttribute('data-pol') === '1'){
            _rendre(e); e.removeAttribute('data-pol');
          }"""
assert S_APP.count(AV_RETIRE2)==1, "second bloc de retrait introuvable"
S_APP = S_APP.replace(AV_RETIRE2, AP_RETIRE2)

AV_POSE = """        var r = report(fam, w, st); if(!r) continue;
        e.style.setProperty('font-family', PILE[r[0]], 'important');"""
AP_POSE = """        var r = report(fam, w, st); if(!r) continue;
        _garder(e);
        e.style.setProperty('font-family', PILE[r[0]], 'important');"""
assert S_APP.count(AV_POSE)==1, "bloc de pose introuvable"
S_APP = S_APP.replace(AV_POSE, AP_POSE)

AV_DECL = """  var PILE = {Apfel:"""
AP_DECL = """  /* ⚑ on note ce qu'il y avait AVANT de l'écraser, et on le remet avant de relire :
     une autre passe (`pose()`, sur le Peaufiner d'une Nuée) écrit sur les mêmes propriétés. */
  function _garder(e){
    if(e.getAttribute('data-pol-av') !== null && e.getAttribute('data-pol-av') !== undefined) return;
    e.setAttribute('data-pol-av', JSON.stringify([
      e.style.getPropertyValue('font-family'), e.style.getPropertyPriority('font-family'),
      e.style.getPropertyValue('font-weight'), e.style.getPropertyPriority('font-weight'),
      e.style.getPropertyValue('font-style'),  e.style.getPropertyPriority('font-style')]));
  }
  function _rendre(e){
    var s = e.getAttribute('data-pol-av');
    e.style.removeProperty('font-family'); e.style.removeProperty('font-weight'); e.style.removeProperty('font-style');
    if(s == null) return;
    try{ var v = JSON.parse(s);
      if(v[0]) e.style.setProperty('font-family', v[0], v[1]);
      if(v[2]) e.style.setProperty('font-weight', v[2], v[3]);
      if(v[4]) e.style.setProperty('font-style',  v[4], v[5]);
    }catch(_){}
    e.removeAttribute('data-pol-av');
  }

  var PILE = {Apfel:"""
assert S_APP.count(AV_DECL)==1, "déclaration PILE introuvable"
S_APP = S_APP.replace(AV_DECL, AP_DECL)

# ⚑ QUAND LA BUTÉE DE 12 PX NE SUFFIT PLUS, ON RESSERRE L'INTERLETTRE — JAMAIS LE PLANCHER.
#   `etatsDeCarte()` ajuste l'état d'une carte d'Index « par pas de 0,5 jusqu'à ce que le mot
#   tienne, butée à 12, le minimum absolu du §6 ». Atkinson est 2,6 % plus large qu'ApfelMid :
#   « 9 PROMI · 3 TENUS » mesure 144,2 px d'encre pour 140 de boîte À LA BUTÉE — le S sortait,
#   coupé par l'`overflow:hidden` de la ligne (vu à l'œil sur la planche ; aucune batterie ne
#   pouvait le prendre, la boîte, elle, ne déborde pas).
#   Le vrai coût est l'interlettre : `.18em` fait 2,16 px × 16 intervalles = 34,6 px, soit 24 %
#   de la ligne. On prolonge donc le MÊME arbitrage sur la seule autre variable disponible,
#   par pas de 0,01em et **bornée à .12em** — en deçà, un libellé espacé cesse d'en être un.
#   Le §6 n'est pas touché : la taille ne descend jamais sous 12.
AV_FIT = """      var g = 0;
      while(n.scrollWidth > n.clientWidth + 1 && t > 12 && g++ < 16){
        t -= 0.5;
        n.style.setProperty('font-size', t + 'px', 'important');
      }
      n.setAttribute('data-fit', '1');"""
AP_FIT = """      var g = 0;
      while(n.scrollWidth > n.clientWidth + 1 && t > 12 && g++ < 16){
        t -= 0.5;
        n.style.setProperty('font-size', t + 'px', 'important');
      }
      /* ⚑ 16 sept. 2026 — la butée de 12 est le plancher du §6 : on ne descend pas dessous.
         S'il faut encore gagner, c'est l'INTERLETTRE qui cède, par pas de 0,01em, bornée à
         .12em. Relevé : « 9 PROMI · 3 TENUS » en Atkinson, 144,2 px d'encre pour 140 de boîte. */
      if(n.scrollWidth > n.clientWidth + 1){
        var em = parseFloat(getComputedStyle(n).letterSpacing) / t;
        if(!isFinite(em)) em = 0.18;
        var h = 0;
        while(n.scrollWidth > n.clientWidth + 1 && em > 0.12 && h++ < 12){
          em -= 0.01;
          n.style.setProperty('letter-spacing', em.toFixed(3) + 'em', 'important');
        }
        n.setAttribute('data-fit-ls', '1');
      }
      n.setAttribute('data-fit', '1');"""
assert S_APP.count(AV_FIT)==1, "boucle d'ajustement de etatsDeCarte introuvable"
S_APP = S_APP.replace(AV_FIT, AP_FIT)

# et la passe se relit : elle doit aussi rendre l'interlettre avant de redécider
AV_REL = """      if(n.hasAttribute('data-fit')){ n.style.removeProperty('font-size'); n.removeAttribute('data-fit');
        if(!n.clientWidth) return; }"""
AP_REL = """      if(n.hasAttribute('data-fit')){ n.style.removeProperty('font-size'); n.removeAttribute('data-fit');
        if(n.hasAttribute('data-fit-ls')){ n.style.removeProperty('letter-spacing'); n.removeAttribute('data-fit-ls'); }
        if(!n.clientWidth) return; }"""
assert S_APP.count(AV_REL)==1, "garde de relecture introuvable"
S_APP = S_APP.replace(AV_REL, AP_REL)

AV_PILE = """  var PILE = {Apfel:"Apfel,system-ui,sans-serif", ApfelMid:"ApfelMid,Apfel,system-ui,sans-serif",
              Bricolage:"Bricolage,system-ui,sans-serif", Fraunces:"Fraunces,Georgia,serif"};"""
AP_PILE = """  var PILE = {Apfel:"Apfel,system-ui,sans-serif", ApfelMid:"ApfelMid,Apfel,system-ui,sans-serif",
              Bricolage:"Bricolage,system-ui,sans-serif", Fraunces:"Fraunces,Georgia,serif",
              Gilbert:"Gilbert,Bricolage,system-ui,sans-serif",
              Atkinson:"Atkinson,Apfel,system-ui,sans-serif"};"""
assert S_APP.count(AV_PILE)==1, "bloc PILE du lot-POLICES introuvable"
S_APP = S_APP.replace(AV_PILE, AP_PILE)
S = S_APP

# ── on ressort les base64 ─────────────────────────────────────────────────────
S = re.sub(r'\x00B64_(\d+)\x00', lambda m: COFFRE[int(m.group(1))], S)
io.open(DST,'w',encoding='utf-8').write(S)

print(f"{DST} écrit")
print(f"  couleurs hex basculées      : {nb_hex}")
print(f"  couleurs rgb() basculées    : {nb_rgb}")
print(f"  #12142A rendus au fond brun : {nb_desa}  (les corps de fiche Promi gardent le bleu)")
print(f"  font-family centralisées    : {nb_pol}")
print(f"  couleurs du CSS en variable : {nb_var}")
print(f"  variables déclarées         : {len(decl)}  ({len(NOM)} couleurs, {len(NOMT)} triplets)")
print(f"  rôles                       : {len(ROLES)}")

# le jeu, pour le portage
jeu = {
 'genere_le':'2026-09-16',
 'note':"Source unique du design de Promi. Les rôles basculent avec le mode ; la palette fixe ne bascule jamais.",
 'polices': FAMILLES,
 'niveaux': TYPO,
 'roles': {k:{'clair':clair(v),'sombre':sombre(v)} for k,v in ROLES.items()},
 'palette_fixe': {NOM[h]:h for h in sorted(NOM)},
}
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(json.dumps(jeu,ensure_ascii=False,indent=2))
print("  PROMI-TOKENS.json écrit")
