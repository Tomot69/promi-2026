# v162b §9 (C-187) — Ramage sans rosace : à appliquer APRÈS le commit v162a. Tout reste dans `_parure` (le Worker du film en reçoit le texte).
import io, sys
P = 'promi-moteur.js'
S = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global S
    assert S.count(a) == 1, a[:90]
    S = S.replace(a, b)
# 1 · chaque œil reçoit sa FORME (trois harmoniques tirées de sa clé), son tourbillon et le décalage de ses bandes
rep("""    const ez = new Map(S.pr.map(p => [p, 0.78 + 0.5 * _lcg((p.h ^ 0xe7e) >>> 0)()]));""",
"""    const ez = new Map(S.pr.map(p => [p, 0.78 + 0.5 * _lcg((p.h ^ 0xe7e) >>> 0)()]));
    /* ⚑ v162 (Tom, C-187) — « Ramage dispose ses plumages parfaitement en cercle autour du centre des dalles : un effet rosace qui ne va pas. » Chaque
       œil a maintenant SA forme, tirée de sa clé (la Toile reste la même d'une ouverture à l'autre) : son contour n'est plus un cercle (trois harmoniques,
       15 à 40 % d'écart), ses plumes ne partent plus en rayons droits (elles tournent d'un tourbillon propre, de sens et de force tirés), ses bandes de
       couleur ne sont plus à égale distance (chacune décalée) ; son cœur n'est plus une spirale régulière (angle, rayon, taille et nombre de feuilles
       variés). Rien d'autre ne change : le même plumage, les mêmes couleurs, la même encre. */
    const fo = new Map(S.pr.map(p => { const q = _lcg((p.h ^ 0xf07a) >>> 0);
      return [p, { a1: 0.10 + 0.16 * q(), f1: q() * 6.2832, a2: 0.05 + 0.10 * q(), f2: q() * 6.2832, a3: 0.02 + 0.07 * q(), f3: q() * 6.2832, tor: (q() < 0.5 ? -1 : 1) * (0.35 + 0.75 * q()),
        bj: [(q() - 0.5) * 0.09, (q() - 0.5) * 0.09, (q() - 0.5) * 0.08, (q() - 0.5) * 0.08, (q() - 0.5) * 0.06], dg: (q() - 0.5) * 0.06, el: 0.80 + 0.32 * q(), ea: q() * 3.1416, m: 130 + Math.floor(q() * 130), ta: 0.75 + 0.5 * q() }]; }));
    const forme = (p, th) => { const P = fo.get(p); return 1 + P.a1 * Math.cos(th - P.f1) + P.a2 * Math.cos(2 * th - P.f2) + P.a3 * Math.cos(3 * th - P.f3); };""")
# 2 · la distance normalisée suit la forme de l'œil ; la direction tourne
rep("""        const dx = x - p.x, dy = y - p.y, d = Math.hypot(dx, dy) || 1e-6, t = d / (p.R * ez.get(p));""",
"""        const dx = x - p.x, dy = y - p.y, d = Math.hypot(dx, dy) || 1e-6, t = d / (p.R * ez.get(p) * forme(p, Math.atan2(dy, dx)));""")
rep("""        vx += dx / d * w; vy += dy / d * w;""",
"""        { const sw = fo.get(p).tor * Math.exp(-t * 0.9), cs = Math.cos(sw), sn = Math.sin(sw), ux = dx / d, uy = dy / d; vx += (ux * cs - uy * sn) * w; vy += (ux * sn + uy * cs) * w; }   /* v162 : un tourbillon, plus des rayons */""")
# 3 · les bandes, décalées par œil
rep("""    const bands = t => t < 0.22 ? 1 : t < 0.42 ? 0 : t < 0.58 ? 2 : t < 0.8 ? 0 : t < 0.9 ? 2 : -1;""",
"""    const bands = (t, p) => { const j = p ? fo.get(p).bj : [0, 0, 0, 0, 0]; return t < 0.22 + j[0] ? 1 : t < 0.42 + j[1] ? 0 : t < 0.58 + j[2] ? 2 : t < 0.8 + j[3] ? 0 : t < 0.9 + j[4] ? 2 : -1; };""")
rep("""      const b = f.p ? bands(f.t + (f.r2 - 0.5) * 0.05) : -1;""",
"""      const b = f.p ? bands(f.t + (f.r2 - 0.5) * 0.05, f.p) : -1;""")
# 4 · le cœur : plus une spirale d'or régulière
rep("""      const q = _lcg((p.h ^ 0xc0e) >>> 0), Rc = p.R * ez.get(p) * (0.5 + 0.08 * q()), m = 200 + Math.floor(q() * 40), a0 = q() * 6.283;""",
"""      const PF = fo.get(p), q = _lcg((p.h ^ 0xc0e) >>> 0), Rc = p.R * ez.get(p) * (0.5 + 0.08 * q()), m = PF.m, a0 = q() * 6.283;""")
rep("""        const t = k / m, r = Rc * Math.pow(t, 0.72) * 0.92, a = a0 + k * 2.39996;
        const d = a + (q() - 0.5) * 0.18, L = sp * (0.24 + 1.45 * t) * (0.65 + 0.7 * q()) * tS, Wd = L * (0.52 + 0.14 * q()), back = t < 0.35 ? 0.42 : 0.3;""",
"""        const a = a0 + k * (2.39996 + PF.dg) + (q() - 0.5) * 0.55, t = k / m, ce = Math.cos(a - PF.ea), se = Math.sin(a - PF.ea),
          r = Rc * Math.pow(t, 0.72) * 0.92 * forme(p, a) * (0.86 + 0.28 * q()) * Math.hypot(ce * PF.el, se / PF.el);   /* v162 : un cœur ovale, irrégulier */
        const d = a + (q() - 0.5) * 0.42 + PF.tor * 0.35 * t, L = sp * (0.24 + 1.45 * t) * (0.55 + 0.9 * q()) * PF.ta * tS, Wd = L * (0.48 + 0.2 * q()), back = t < 0.35 ? 0.42 : 0.3;""")
io.open(P, 'w', encoding='utf-8').write(S)
print('appliqué')
