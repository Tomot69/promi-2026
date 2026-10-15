# -*- coding: utf-8 -*-
"""v146 (C-132) — LES FICHES ET LA PAGE + SONT EN VERSION SOMBRE DANS LES DEUX MODES : la transformation de la feuille de style.
   ① tout sélecteur conditionné par `.light` gagne, sur son sujet, `:not(:where(SOMBRE))` (spécificité 0 : la cascade du clair ne bouge pas ailleurs) ;
   ② tout sélecteur conditionné par `:not(.light)` gagne un jumeau qui vaut en clair DANS la fiche (`.light` … sujet`:where(SOMBRE)`), même spécificité ;
   ③ les propriétés personnalisées posées sous `.light` reprennent leur valeur du sombre sur la racine de la fiche (bloc engendré).
   Idempotent : un sélecteur déjà traité (il porte `th-sombre`) est laissé. Usage : python3 p8_theme_css.py [--sec] (--sec : compte, n'écrit pas)"""
import io, re, sys
P = 'app.html'; S = io.open(P, encoding='utf-8').read()
SEC = '--sec' in sys.argv; VERB = '--dis' in sys.argv
OU = '#detailPoster,#detailPoster *,#createSheet,#createSheet *,.th-sombre,.th-sombre *'
HORS = ':not(:where(' + OU + '))'
DANS = ':where(' + OU + ')'
RE_L = re.compile(r'\.light(?![\w-])')
RE_NL = re.compile(r':not\(\s*\.light\s*\)')

def coupe(sel):
    """coupe une liste de sélecteurs à ses virgules de premier niveau"""
    out = []; p = 0; cur = ''; q = None; i = -1; N = len(sel)
    while i + 1 < N:
        i += 1; ch = sel[i]
        if q is None and sel.startswith('/*', i):          # un commentaire : ses virgules ne coupent rien
            j = sel.find('*/', i + 2); j = N if j < 0 else j + 2; cur += sel[i:j]; i = j - 1; continue
        if q:
            cur += ch
            if ch == q: q = None
            continue
        if ch in '"\'': q = ch; cur += ch; continue
        if ch in '([': p += 1
        elif ch in ')]': p -= 1
        if ch == ',' and p == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur); return out

def sujet_plus(sel, ajout):
    """ajoute `ajout` au SUJET (le dernier composé), avant un éventuel pseudo-élément"""
    s = sel.rstrip(); fin = sel[len(s):]
    # un pseudo-élément final : ::xxx, ou les quatre à un seul deux-points
    m = re.search(r'(::[\w-]+(\([^()]*\))?|:(before|after|first-line|first-letter))\s*$', s)
    if m: return s[:m.start()] + ajout + s[m.start():] + fin
    return s + ajout + fin

n1 = n2 = 0; vars_light = {}
def traite_css(css):
    global n1, n2
    out = []; i = 0; N = len(css); prof = 0
    # on parcourt en gardant les commentaires et les chaînes ; un « prélude » va du dernier `}` ou `{` (d'un bloc @) ou `;` de premier niveau jusqu'au `{`
    deb = 0
    while i < N:
        c = css[i]
        if css.startswith('/*', i):
            j = css.find('*/', i + 2); j = N if j < 0 else j + 2; i = j; continue
        if c in '"\'':
            j = i + 1
            while j < N and css[j] != c: j += 2 if css[j] == '\\' else 1
            i = j + 1; continue
        if c == '{':
            prelude = css[deb:i]
            brut = re.sub(r'/\*.*?\*/', '', prelude, flags=re.S).strip()
            j = i + 1; p = 1; conteneur = brut.startswith('@media') or brut.startswith('@supports') or brut.startswith('@layer') or brut.startswith('@container')
            if conteneur:
                out.append(css[deb:i + 1]); i += 1; deb = i; continue
            # un bloc ordinaire (ou @keyframes, @font-face…) : on va à son `}` apparié
            while j < N and p > 0:
                if css.startswith('/*', j):
                    k = css.find('*/', j + 2); j = N if k < 0 else k + 2; continue
                if css[j] in '"\'':
                    q = css[j]; j += 1
                    while j < N and css[j] != q: j += 2 if css[j] == '\\' else 1
                    j += 1; continue
                if css[j] == '{': p += 1
                elif css[j] == '}': p -= 1
                j += 1
            corps = css[i:j]
            if brut.startswith('@') or not brut:
                out.append(css[deb:j]); i = j; deb = i; continue
            sels = coupe(prelude); neufs = []; change = False
            _nu = lambda x: re.sub(r'\s+', '', re.sub(r'/\*.*?\*/', '', x, flags=re.S))
            jumeles = set(_nu(x) for x in sels if 'th-sombre' in x)
            for s in sels:
                nu = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
                if 'th-sombre' in nu or not RE_L.search(nu): neufs.append(s); continue
                sans = RE_NL.sub('', nu)
                if RE_L.search(sans) and RE_NL.search(nu): neufs.append(s); continue            # les deux à la fois : on n'y touche pas
                if RE_L.search(sans):                    # ① une règle du clair : hors de la fiche
                    neufs.append(sujet_plus(s, HORS)); n1 += 1; change = True
                    if VERB: print('  ①', nu.strip()[:150])
                    if re.match(r'^[#.\w]*\.light[.\w#-]*$|^(\.device|#device|\.frame)[.#\w-]*$', nu.strip()) or True:
                        for v, val in re.findall(r'(--[\w-]+)\s*:\s*([^;{}]+)', re.sub(r'/\*.*?\*/', '', corps, flags=re.S)): vars_light.setdefault(v, 0); vars_light[v] += 1
                else:                                    # ② une règle du sombre seul : elle vaut aussi en clair DANS la fiche
                    jumeau = sujet_plus(RE_NL.sub('.light', s), DANS)
                    if _nu(jumeau) in jumeles: neufs.append(s); continue          # déjà doublée (l'outil se rejoue sans rien ajouter)
                    if VERB: print('  ②', nu.strip()[:150])
                    neufs.append(s); neufs.append(jumeau if jumeau.startswith(('\n', ' ')) else ' ' + jumeau); n2 += 1; change = True
            out.append((','.join(neufs) if change else prelude) + corps); i = j; deb = i; continue
        if c == '}':
            out.append(css[deb:i + 1]); i += 1; deb = i; continue
        i += 1
    out.append(css[deb:]); return ''.join(out)

def bloc(m):
    return m.group(1) + traite_css(m.group(2)) + m.group(3)
T = re.sub(r'(<style[^>]*>)(.*?)(</style>)', bloc, S, flags=re.S)
print('① sélecteurs du clair mis hors de la fiche :', n1, '· ② sélecteurs du sombre doublés pour la fiche :', n2, '· propriétés personnalisées posées sous le clair :', len(vars_light))
io.open('scratchpad/v146/vars_light.txt', 'w', encoding='utf-8').write('\n'.join(sorted(vars_light)))
if not SEC:
    io.open(P, 'w', encoding='utf-8').write(T); print('écrit · %d → %d octets' % (len(S), len(T)))
