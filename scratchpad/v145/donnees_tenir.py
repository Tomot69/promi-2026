#!/usr/bin/env python3
"""v145 (C-118) — variantes/tenir-donnees.js : la fiche AVANT le geste et la fiche TENUE, relevées sur l'app (extrait_fiche.py), rangées par élément."""
import json, io, re, os, base64
D = json.load(io.open('scratchpad/v145/extrait/fiches.json', encoding='utf-8'))
def hexa(c):
    m = re.findall(r'[\d.]+', c or ''); return '#%02X%02X%02X' % tuple(int(float(x)) for x in m[:3]) if len(m) >= 3 else c
def cles(els):
    """une clé STABLE d'un état à l'autre : l'id, sinon la première classe et son rang ; un svg ou un span sans classe prend le nom de ce qui le précède"""
    vus = {}; out = []; prec = None
    for e in els:
        if e['tag'] == 'b': out.append(dict(e, k='b')); continue
        base = e['id'] or ((e['cls'].split() or [''])[0])
        if not base:
            k = '%s@%s' % (e['tag'], prec or '')
        else:
            n = vus.get(base, 0); vus[base] = n + 1; k = base if e['id'] else '%s~%d' % (base, n)
        if base: prec = k
        out.append(dict(e, k=k))
    return out
def allege(e, html_b=None):
    o = {'k': e['k'], 'r': e['r'], 'tag': e['tag']}
    if 'txt' in e:
        f = e['f']; o['t'] = e['txt']; o['f'] = [f['fam'].split(',')[0].strip().strip('"\''), f['fs'], f['fw'], f['ls'], f['tt'], f['ta'], hexa(f['col'])]
    for a in ('bg',):
        if a in e: o['bg'] = e['bg'] if 'rgba' in e['bg'] else hexa(e['bg'])
    if 'bd' in e: o['bd'] = [round(e['bd'][0], 2), e['bd'][1] if 'rgba' in e['bd'][1] else hexa(e['bd'][1])]
    if 'br' in e: o['br'] = e['br']
    if 'svg' in e: o['svg'] = re.sub(r'\s+', ' ', e['svg']); o['col'] = hexa(e.get('col'))
    if 'img' in e and e['k'] not in ('dpTrameCv', 'tenirCv'): o['img'] = e['img']
    return o
OUT = {}
for cle, E in D.items():
    nat = cle.split('-')[0]; o = {'champ': None, 'etats': {}}
    for etat in ('avant', 'instant', 'tenue'):
        els = cles(E[etat]['els']); L = []; tr = None
        for i, e in enumerate(els):
            if e['k'] == 'dpTrameCv':
                t = e.get('data-trait', '').split(','); tr = {'base': float(t[0]), 'amp': float(t[1]), 'col': t[2], 'mode': t[3]}; o['champ'] = e.get('data-champ'); continue
            if e['k'] in ('detailPoster', 'tenirCv', 'dpDetails', 'cm5Fil', 'cm5Dernier') or e['k'].startswith('svg@cm5') or e['k'].startswith('cm5-va') or e['k'].startswith('cm5-saisie'): continue
            # v145 (C-116) : la ligne de commentaire a remplacé le champ « écris un mot » — la page de variantes garde ses deux clés
            if e['k'] == 'cm5Ligne': e = dict(e, k='dpMsg')
            elif e['k'].startswith('cm5-mot'): e = dict(e, k='span@dpMsg')
            a = allege(e)
            # la phrase : le prénom en gras est un enfant — on recompose la ligne
            if e['k'] == 'dptQui':
                enfants = [x for x in els[i + 1:i + 3] if x['tag'] == 'b' and 'txt' in x]
                if enfants:
                    b = enfants[0]['txt']; t = e['txt']
                    a['h'] = ('<b>%s</b>%s' % (b, t)) if t.startswith(',') else re.sub(r'  ', ' <b>%s</b> ' % b, t, 1) if '  ' in t else t + ' <b>%s</b>' % b
            if e['tag'] == 'b': continue
            L.append(a)
        o['etats'][etat] = {'corps': hexa(E[etat]['corps']), 'trait': tr, 'els': L}
    dl = E['avant'].get('dalle') or {}
    o['dalle'] = {'img': dl.get('img'), 'A': [127, 124, 136, 114], 'I': [81, 70, 228, 190], 'B': [105, 89, 180, 150]}
    OUT[cle] = o
os.makedirs('variantes', exist_ok=True)
js = '/* Promi — la fiche avant le geste, l\'instant et la fiche tenue, relevés sur l\'app réelle (v145, banc_tom WebKit @3x) : places, polices, couleurs, canevas.\n   Engendré par scratchpad/v145/donnees_tenir.py — ne pas écrire à la main. */\nwindow.TENIR=' + json.dumps(OUT, ensure_ascii=False, separators=(',', ':')) + ';\n'
io.open('variantes/tenir-donnees.js', 'w', encoding='utf-8').write(js)
print(len(js), 'octets')
for cle in OUT:
    for et in OUT[cle]['etats']:
        print(cle, et, OUT[cle]['etats'][et]['corps'], OUT[cle]['etats'][et]['trait'], [e['k'] for e in OUT[cle]['etats'][et]['els']][:40])
    break
print([ (e['k'], e.get('h') or e.get('t'), e.get('f')) for e in OUT['promi-clair']['etats']['avant']['els'] if 'f' in e][:14])
print([ (e['k'], e.get('h') or e.get('t'), e.get('f')) for e in OUT['chiche-sombre']['etats']['tenue']['els'] if 'f' in e][:14])
