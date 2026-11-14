#!/usr/bin/env python3
"""v202a (Tom, C-272, C-273, C-275) — RÉSUMÉ D'UN RELEVÉ D'IMAGES DE L'iPHONE (`?mesure=1`, mesures/AAAA-MM-JJ-HHMM.jsonl).

Par écran, par animation, et par couple écran × animation : le nombre d'images, le p50, le p95, le max, et les images au-dessus de 16,7 et de 33 ms.
Une image = l'intervalle entre deux requestAnimationFrame ; elle est attribuée à l'écran et à l'animation notés à sa fin.

    python3 resume_releve.py                     le relevé le plus récent
    python3 resume_releve.py mesures/2026-11-14-1530.jsonl
    python3 resume_releve.py --min=30            n'affiche que les lignes d'au moins 30 images (défaut 20)
    python3 resume_releve.py --json              sortie JSON (pour un juge)
"""
import glob, json, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))


def quantile(v, q):
    if not v: return 0.0
    v = sorted(v); i = q * (len(v) - 1); a = int(i); b = min(a + 1, len(v) - 1)
    return v[a] + (v[b] - v[a]) * (i - a)


def stats(v):
    return {'n': len(v), 'p50': round(quantile(v, .5), 1), 'p95': round(quantile(v, .95), 1), 'max': round(max(v) if v else 0, 1),
            'sup16': sum(1 for d in v if d > 16.7), 'sup33': sum(1 for d in v if d > 33.4)}


def lit(chemin):
    images = []; meta = {}
    for ligne in open(chemin, encoding='utf-8'):
        try: d = json.loads(ligne)
        except Exception: continue
        if d.get('quoi') != 'releve': continue
        tags = d.get('tags') or []
        meta = {k: d.get(k) for k in ('seance', 'debut', 'version', 'etat', 'ecran', 'ua', '_de')}
        for t, dur, e, a in d.get('images') or []:
            images.append((t, dur, tags[e] if e < len(tags) else '?', tags[a] if a < len(tags) else '?'))
    images.sort()
    return images, meta


def resume(images):
    par = {'ecran': {}, 'animation': {}, 'couple': {}}
    for _, dur, e, a in images:
        par['ecran'].setdefault(e, []).append(dur)
        for x in a.split('+'): par['animation'].setdefault(x, []).append(dur)
        par['couple'].setdefault(e + ' | ' + a, []).append(dur)
    return {k: {n: stats(v) for n, v in d.items()} for k, d in par.items()}, stats([d for _, d, _, _ in images])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    mini = 20
    for a in sys.argv[1:]:
        m = re.match(r'--min=(\d+)', a)
        if m: mini = int(m.group(1))
    if args: chemin = args[0]
    else:
        f = sorted(glob.glob(os.path.join(ICI, 'mesures', '20??-??-??-????*.jsonl')), key=os.path.getmtime)
        if not f: print('aucun relevé dans mesures/'); return 1
        chemin = f[-1]
    images, meta = lit(chemin)
    R, tout = resume(images)
    if '--json' in sys.argv:
        print(json.dumps({'fichier': chemin, 'meta': meta, 'tout': tout, 'par': R}, ensure_ascii=False, indent=1)); return 0
    print('relevé :', os.path.relpath(chemin, ICI))
    print('version :', meta.get('version'), '· début :', meta.get('debut'), '· écran :', meta.get('ecran'))
    print('état :', meta.get('etat'))
    dureeS = (images[-1][0] - images[0][0]) / 1000 if images else 0
    print('%d images sur %.0f s — p50 %.1f · p95 %.1f · max %.1f ms · > 16,7 : %d · > 33 : %d' % (tout['n'], dureeS, tout['p50'], tout['p95'], tout['max'], tout['sup16'], tout['sup33']))
    for titre, cle in (('PAR ÉCRAN', 'ecran'), ('PAR ANIMATION', 'animation'), ('ÉCRAN × ANIMATION', 'couple')):
        print('\n' + titre)
        print('  %-52s %6s %6s %6s %7s %6s %6s' % ('', 'images', 'p50', 'p95', 'max', '>16,7', '>33'))
        for nom, s in sorted(R[cle].items(), key=lambda kv: -kv[1]['p95']):
            if s['n'] < mini: continue
            print('  %-52s %6d %6.1f %6.1f %7.1f %6d %6d' % (nom[:52], s['n'], s['p50'], s['p95'], s['max'], s['sup16'], s['sup33']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
