/* trace-lettres.js — LE TRACÉ DES LETTRES (C-125, Tom, oct. 2026). Sans dépendance.

   « Au départ aucun texte ; puis les lettres du premier mot SE TRACENT, puis celles du second. » Chaque lettre se dessine par un trait NET, comme un
   rouleau à bord franc : le front qui avance est une coupe perpendiculaire au chemin. Ni flèche, ni curseur, ni fondu, ni dégradé, ni contour.
   À la fin, c'est le texte RÉEL qui est posé (le nœud de texte d'origine, dans sa police) : la dernière image est le texte statique, au pixel près.

   LA POLICE N'EST PAS REDESSINÉE : chaque glyphe est rendu par la vraie police (fillText) et DÉVOILÉ le long de sa ligne médiane
   (variantes/trace-chemins-<police>.js, engendré par scratchpad/v146/trace/chemins.py). Pour chaque glyphe une « carte de temps » : chaque
   pixel plein reçoit l'abscisse curviligne du point de la ligne médiane dont la NORMALE passe par lui ; à l'instant t on montre les pixels
   d'abscisse ≤ t (un pixel d'anticrénelage au front, rien d'autre). Le modèle est celui d'un ROULEAU large comme le trait :
     · un trait possède ce qui est à moins d'une demi-largeur de sa ligne ; là où deux traits se recouvrent, la DROITE l'emporte (un fût garde
       toute sa largeur : la panse qui en naît sort de son bord, d'une coupe franche), puis le trait qui passe le premier ;
     · à un bout libre le trait part de rien, sur le bord de l'encre ; à un coin il va jusqu'au bord extérieur ; à un embranchement il s'arrête
       sur la ligne de l'autre trait ; à un sommet de la ligne le front pivote ;
     · un repassage (invisible) dure le dixième de sa longueur, un saut ne dure rien.
   Un seul glyphe s'anime à la fois, dans un canevas ; dès qu'il est fini, c'est le TEXTE RÉEL qui le montre (la découpe du texte avance).

   ── L'API ──
   TraceLettres.trace(cible, contenu, options) → controle
       cible    un élément bloc (ou inline-block) ; le texte y vit en vrai (lecteurs d'écran, sélection, mise en page du navigateur)
       contenu  null : on trace ce que l'élément contient déjà, avec ses styles (couleurs, polices, tailles des nœuds enfants)
                'une chaîne' : elle remplace le contenu (« \n » = retour à la ligne)
                [ {t:'Primo, un '}, {t:'Promi', couleur:'#82AEF8'}, {t:' …', police:'PromiLate', classe:'x', style:'…'} ] : des segments
       options  cps          caractères par seconde (50 ; Tom : 40 à 60)
                vitesse      multiplicateur (1 ; 0.25 et 0.05 pour regarder au ralenti)
                depart       'h' | 'b' : le côté où commence la toute première lettre (R3 ; 'h')
                espace       la pause d'une espace, en caractères (0.4)
                toutDeSuite  true : le texte est posé d'un coup (« Réduire les animations ») ; respecteReduire:false pour l'ignorer
                manuel       true : rien ne bouge seul — controle.va(p) rend l'état à p ∈ [0 ; 1] (les juges, les captures)
                attributs    {nom: valeur} posés sur le canevas (ex. {'data-eng':''}) ; z : son z-index (2)
                surFin       rappel de fin
       controle .fin         promesse, résolue quand le texte réel est posé ({interrompu: bool})
                .pret        promesse, résolue quand tout est mesuré (avant la première image)
                .stop()      arrête et pose le texte entier ; .finir() idem, sans « interrompu »
                .va(p)       (manuel) rend l'état à la fraction p de la durée ; .duree en ms ; .glyphes (liste : car, variante, côtés)
   TraceLettres.poseTout(cible)              retire un tracé en cours et montre le texte
   TraceLettres.glyphe(police, car)          les données brutes d'un glyphe (ou null)
   TraceLettres.parcours(police, car, v)     {traits:[{pts:[[x,y]…], R}], repassages:[[[x,y]…]], sauts:[[[x,y],[x,y]]], depart, arrivee, fin} en unités de police
   TraceLettres.dessineChemin(ctx, police, car, v, ox, oy, echelle, options)   dessine ce parcours (le mode « montre le chemin »)
   TraceLettres.reduit()                     vrai si l'appareil demande de réduire les animations

   ⚠ Quatre choses à savoir avant de brancher :
   ① le texte réel n'est jamais rendu transparent : il est DÉCOUPÉ (`clip-path`, posé en ligne sur la cible, rendu à la fin). Un glyphe en cours
     de tracé vit dans un canevas ; dès qu'il est fini, c'est le texte réel qui le montre. Il n'y a donc aucun échange à la fin : la dernière image
     EST le texte statique. La cible ne doit porter que du texte (un fond ou une bordure seraient découpés avec lui) ;
   ② le canevas est posé comme FRÈRE de la cible (juste après elle, en `position:absolute`) : la cible doit avoir un `offsetParent`
     (pas de `position:fixed` sur la cible elle-même, pas de `display:none`) ; la cible est un bloc ou un inline-block ;
   ③ un glyphe sans chemin (police inconnue, caractère absent) est dévoilé par un front vertical, de gauche à droite ;
   ④ le texte se lit de gauche à droite ; un `transform` posé sur un mot À L'INTÉRIEUR de la cible (le « Deuxio » penché) n'est pas suivi. */
(function (racine) {
  'use strict';
  var TL = { version: 1, defauts: { cps: 50, vitesse: 1, depart: 'h', espace: 0.4 }, mesures: { prep: [], image: [] } };
  var REPASSAGE = 0.1;      /* un repassage dure le dixième du temps qu'il aurait pris tracé : « un instant » */
  var PIVOT = 0.5;          /* à un sommet de la ligne, le front pivote : le temps du pivot, en part de l'arc extérieur */
  var doc = racine.document;

  function donnees(nom) { var T = racine.TraceLettresChemins || {}; return T[nom] || null; }
  function famille(ff) { return String(ff || '').split(',')[0].replace(/["']/g, '').trim(); }
  TL.glyphe = function (police, car) { var D = donnees(police); return D && D.g[car] || null; };
  TL.reduit = function () { try { return !!(racine.matchMedia && racine.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (e) { return false; } };

  /* ── le parcours d'un glyphe, en unités de police ── */
  function arete(g, ref) {
    var e = g.e[Math.abs(ref) - 1], n = (e.length - 1) >> 1, P = new Array(n), i;
    for (i = 0; i < n; i++) P[i] = [e[1 + 2 * i], e[2 + 2 * i]];
    if (ref < 0) P.reverse();
    return { pts: P, R: e[0] };
  }
  function longueur(P) { var L = 0, i; for (i = 1; i < P.length; i++) L += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); return L; }
  TL.parcours = function (police, car, v) {
    var D = donnees(police), g = D && D.g[car]; if (!g) return null;
    var V = g[v] ? v : (g.h ? 'h' : 'b'), var_ = g[V]; if (!var_) return null;
    var out = { variante: V, fin: var_.f, traits: [], repassages: [], sauts: [], ordre: [], mi: D.mi, upm: D.upm, boite: g.bo, chasse: g.a }, dern = null;
    var_.t.forEach(function (pas) {
      var k = pas[0], pts = [], R = 0, j, a;
      for (j = 1; j < pas.length; j++) { a = arete(g, pas[j]); R = Math.max(R, a.R); pts = pts.concat(j > 1 ? a.pts.slice(1) : a.pts); }
      if (k === 0) { if (out.sauteAvant && dern) out.sauts.push([dern, pts[0]]); out.sauteAvant = false; out.traits.push({ pts: pts, R: R, L: longueur(pts) }); out.ordre.push(['t', out.traits.length - 1]); dern = pts[pts.length - 1]; }
      else if (k === 1) { out.repassages.push(pts); out.ordre.push(['r', longueur(pts)]); }
      else { out.sauteAvant = true; out.ordre.push(['s', 0]); }
    });
    delete out.sauteAvant;
    /* la nature de chaque bout de trait : libre (le trait y finit seul, sur le bord de l'encre), coin (une autre arête en repart en faisant un angle),
       embranchement (au moins deux autres arêtes s'y joignent). Lu dans les arêtes : combien de bouts d'arête tombent sur ce point. */
    var bouts = []; g.e.forEach(function (e) { var n = (e.length - 1) >> 1; bouts.push([e[1], e[2]], [e[2 * n - 1], e[2 * n]]); });
    function nature(p) { var c = 0, i; for (i = 0; i < bouts.length; i++) if (Math.abs(bouts[i][0] - p[0]) <= 1.5 && Math.abs(bouts[i][1] - p[1]) <= 1.5) c++; return c <= 1 ? 'l' : (c === 2 ? 'c' : 'j'); }
    out.traits.forEach(function (t) { var a = t.pts[0], b = t.pts[t.pts.length - 1]; t.ferme = Math.abs(a[0] - b[0]) <= 1.5 && Math.abs(a[1] - b[1]) <= 1.5 && t.pts.length > 3; t.b0 = t.ferme ? 'f' : nature(a); t.b1 = t.ferme ? 'f' : nature(b); });
    out.depart = out.traits.length ? out.traits[0].pts[0] : null;
    var d = out.traits.length ? out.traits[out.traits.length - 1].pts : null; out.arrivee = d ? d[d.length - 1] : null;
    out.cote = out.depart ? (out.depart[1] >= D.mi ? 'h' : 'b') : V;
    out.longueur = out.traits.reduce(function (s, t) { return s + t.L; }, 0);
    out.repasse = out.repassages.reduce(function (s, p) { return s + longueur(p); }, 0);
    return out;
  };

  /* ── la carte de temps d'un glyphe : A = l'alpha du glyphe rendu (w × h), traits en pixels de cette image ──
     rend {T: Float32Array (temps de chaque pixel, en pixels de chemin), D: durée totale} */
  function carte(A, w, h, traits, moves) {
    var n = w * h, T = new Float32Array(n), own = new Int16Array(n), Tl = new Float32Array(n), k, i, x, y, p;
    for (p = 0; p < n; p++) { own[p] = -1; Tl[p] = Infinity; }
    var S = [];    /* par trait : segments {x,y,dx,dy,len,s,delta} */
    for (k = 0; k < traits.length; k++) {
      var P = traits[k].pts, segs = [], s = 0, m = P.length - 1;
      for (i = 0; i < m; i++) {
        var dx = P[i + 1][0] - P[i][0], dy = P[i + 1][1] - P[i][1], len = Math.hypot(dx, dy);
        if (len < 1e-6) continue;
        segs.push({ x: P[i][0], y: P[i][1], dx: dx / len, dy: dy / len, len: len, s: 0, delta: 0 });
      }
      for (i = 0; i < segs.length; i++) {
        segs[i].s = s; s += segs[i].len;
        if (i < segs.length - 1) { var c = segs[i].dx * segs[i + 1].dx + segs[i].dy * segs[i + 1].dy, th = Math.acos(Math.max(-1, Math.min(1, c))); segs[i].delta = PIVOT * traits[k].R * th; s += segs[i].delta; }
      }
      S.push(segs);
    }
    /* À QUI EST UN PIXEL que deux traits couvrent ? À la DROITE d'abord (un fût garde toute sa largeur, quel que soit l'ordre du tracé : la panse
       qui en naît sort de son bord, d'une coupe franche), puis au trait qui passe le premier. */
    var mins = [], maxs = [], rang = [], kk;
    for (k = 0; k < traits.length; k++) {
      var Pk = traits[k].pts, a0 = Pk[0], b0 = Pk[Pk.length - 1], Lk = Math.hypot(b0[0] - a0[0], b0[1] - a0[1]), ec = 0;
      for (i = 1; i < Pk.length - 1 && Lk > 0; i++) ec = Math.max(ec, Math.abs((Pk[i][0] - a0[0]) * (b0[1] - a0[1]) - (Pk[i][1] - a0[1]) * (b0[0] - a0[0])) / Lk);
      traits[k].droit = Lk > 0 && ec < 0.6; mins.push(Infinity); maxs.push(-Infinity);
    }
    for (k = 0; k < traits.length; k++) if (traits[k].droit) rang.push(k);
    for (k = 0; k < traits.length; k++) if (!traits[k].droit) rang.push(k);
    for (kk = 0; kk < rang.length; kk++) {
      k = rang[kk];
      var segs2 = S[k], R = traits[k].R, Rp = traits[k].droit ? R + 0.8 : R + 0.6, ns = segs2.length, tmin = Infinity, tmax = -Infinity;
      /* LES BOUTS. Un bout libre touche déjà le bord de l'encre : le trait part de rien, juste là. À un coin, le rouleau va jusqu'au bord extérieur.
         À un embranchement il s'arrête sur la ligne de l'autre trait : ce qui est au-delà appartient à cet autre trait. */
      var cap = function (n) { return n === 'c' ? (traits[k].droit ? 1.7 * R + 1.5 : R + 1.5) : (n === 'l' ? 2.5 : 0); }, cap0 = cap(traits[k].b0 || 'l'), cap1 = cap(traits[k].b1 || 'l'), fmax = Math.max(cap0, cap1);
      var d0 = ns ? [segs2[0].dx, segs2[0].dy] : [1, 0], d1 = ns ? [segs2[ns - 1].dx, segs2[ns - 1].dy] : [1, 0];
      for (i = 0; i < ns; i++) {
        var g = segs2[i], ex = g.x + g.dx * g.len, ey = g.y + g.dy * g.len, ext = Rp + ((i === 0 || i === ns - 1) ? fmax : 0);
        var x0 = Math.max(0, Math.floor(Math.min(g.x, ex) - ext)), x1 = Math.min(w - 1, Math.ceil(Math.max(g.x, ex) + ext));
        var y0 = Math.max(0, Math.floor(Math.min(g.y, ey) - ext)), y1 = Math.min(h - 1, Math.ceil(Math.max(g.y, ey) + ext));
        var g2 = i < ns - 1 ? segs2[i + 1] : null;
        for (y = y0; y <= y1; y++) {
          for (x = x0; x <= x1; x++) {
            p = y * w + x; if (!A[p]) continue; var o = own[p]; if (o !== -1 && o !== k) continue;
            var rx = x + 0.5 - g.x, ry = y + 0.5 - g.y, u = rx * g.dx + ry * g.dy, lat = ry * g.dx - rx * g.dy, cand = Infinity;
            if (lat <= Rp && lat >= -Rp && u >= 0 && u <= g.len) cand = g.s + u;
            if (cand === Infinity && i === 0 && cap0 > 0 && u < 0) { var us = rx * d0[0] + ry * d0[1], ls = ry * d0[0] - rx * d0[1]; if (us < 0 && us >= -cap0 && ls <= Rp && ls >= -Rp) cand = g.s + us; }
            if (cand === Infinity && i === ns - 1 && cap1 > 0 && u > g.len) { var ex2 = x + 0.5 - ex, ey2 = y + 0.5 - ey, ue = ex2 * d1[0] + ey2 * d1[1], le = ey2 * d1[0] - ex2 * d1[1]; if (ue > 0 && ue <= cap1 && le <= Rp && le >= -Rp) cand = g.s + g.len + ue; }
            if (g2 && u > g.len && cand === Infinity) {
              var qx = x + 0.5 - g2.x, qy = y + 0.5 - g2.y, u2 = qx * g2.dx + qy * g2.dy;
              if (u2 < 0 && qx * qx + qy * qy <= Rp * Rp) { var a = u - g.len, b = -u2; cand = g.s + g.len + g.delta * (a / (a + b + 1e-9)); }
            }
            if (cand < Tl[p]) { Tl[p] = cand; own[p] = k; }
          }
        }
      }
      for (p = 0; p < n; p++) if (own[p] === k) { if (Tl[p] < tmin) tmin = Tl[p]; if (Tl[p] > tmax) tmax = Tl[p]; }
      mins[k] = tmin; maxs[k] = tmax;
    }
    /* la suite des traits : chacun part quand le précédent a fini ; un repassage ne dure qu'un instant, un saut rien */
    var cur = 0, dep = [];
    for (k = 0; k < traits.length; k++) {
      cur += (moves[k] || 0) * REPASSAGE;
      if (mins[k] === Infinity) { dep.push(cur); continue; }
      dep.push(cur - mins[k]); cur += maxs[k] - mins[k];
    }
    for (p = 0; p < n; p++) T[p] = own[p] >= 0 ? dep[own[p]] + Tl[p] : -1;
    /* ce qui reste (le creux d'un embranchement, un empattement, la frange d'un bord) prend l'instant de son voisin déjà servi, de proche en proche :
       ni trou qui se boucherait plus tard, ni pixel isolé qui paraîtrait avant les autres */
    var reste = [], suiv, encore = true, garde = 0, vx, vy, q2, mt, mg2, gen = new Uint16Array(n);
    for (p = 0; p < n; p++) if (A[p] && own[p] === -1) reste.push(p);
    while (reste.length && encore && garde++ < 400) {
      suiv = []; encore = false; var poses = [];
      for (i = 0; i < reste.length; i++) {
        p = reste[i]; x = p % w; y = (p - x) / w; mt = Infinity; mg2 = 65535;
        /* le voisin servi le plus DIRECTEMENT par un trait (et non par un autre pixel resté) : sinon un instant précoce filerait le long d'un bord */
        for (vy = -1; vy <= 1; vy++) for (vx = -1; vx <= 1; vx++) { if (!vx && !vy) continue; var xx2 = x + vx, yy2 = y + vy; if (xx2 < 0 || yy2 < 0 || xx2 >= w || yy2 >= h) continue; q2 = yy2 * w + xx2;
          if (A[q2] && own[q2] !== -1 && (gen[q2] < mg2 || (gen[q2] === mg2 && T[q2] < mt))) { mg2 = gen[q2]; mt = T[q2]; } }
        if (mt < Infinity) { poses.push(p, mt, mg2 + 1); encore = true; } else suiv.push(p);
      }
      for (i = 0; i < poses.length; i += 3) { T[poses[i]] = poses[i + 1]; own[poses[i]] = -2; gen[poses[i]] = poses[i + 2]; }
      reste = suiv;
    }
    for (i = 0; i < reste.length; i++) { T[reste[i]] = 0; own[reste[i]] = -2; }
    /* un filtre médian (3 × 3, deux fois) sur la carte : plus une dent ni un pixel isolé à la frontière de deux traits — le front reste une marche */
    var v9 = new Float32Array(9), T2 = new Float32Array(n), tour, q, c9, a9, b9, t9;
    for (tour = 0; tour < 2; tour++) {
      for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
        p = y * w + x; if (!A[p]) { T2[p] = T[p]; continue; }
        c9 = 0;
        for (b9 = -1; b9 <= 1; b9++) { var yy = y + b9; if (yy < 0 || yy >= h) continue; for (a9 = -1; a9 <= 1; a9++) { var xx = x + a9; if (xx < 0 || xx >= w) continue; q = yy * w + xx; if (A[q]) v9[c9++] = T[q]; } }
        for (a9 = 1; a9 < c9; a9++) { t9 = v9[a9]; b9 = a9 - 1; while (b9 >= 0 && v9[b9] > t9) { v9[b9 + 1] = v9[b9]; b9--; } v9[b9 + 1] = t9; }
        T2[p] = c9 >= 5 ? v9[(c9 - 1) >> 1] : T[p];   /* la médiane basse : au bord, une rangée ne prend pas l'instant de la suivante */
      }
      T.set(T2);
    }
    for (p = 0; p < n; p++) if (!A[p]) T[p] = 0;
    if (TL._debug) TL._derniere = { T: T, own: own, w: w, h: h, dep: dep, mins: mins, maxs: maxs, droits: traits.map(function (t) { return t.droit; }) };
    return { T: T, D: Math.max(cur, 1) };
  }
  TL._carte = carte;

  /* ── la mesure : où le navigateur a posé chaque caractère ── */
  var bac = null, cacheAsc = {};
  function ascendante(st) {
    /* la distance du haut de la boîte du texte à la ligne de base, pour cette police, telle que le navigateur la pose (une sonde, hors écran) */
    var cle = st.fontStyle + '|' + st.fontWeight + '|' + st.fontSize + '|' + st.fontFamily;
    if (cacheAsc[cle] != null) return cacheAsc[cle];
    if (!bac) { bac = doc.createElement('div'); bac.setAttribute('aria-hidden', 'true'); bac.setAttribute('data-trace-sonde', ''); bac.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;pointer-events:none;white-space:nowrap;line-height:normal;letter-spacing:0'; doc.body.appendChild(bac); }
    bac.textContent = ''; var sp = doc.createElement('span'); sp.style.cssText = 'font-family:' + st.fontFamily + ';font-size:' + st.fontSize + ';font-weight:' + st.fontWeight + ';font-style:' + st.fontStyle + ';line-height:normal';
    sp.appendChild(doc.createTextNode('Hx')); var s0 = doc.createElement('span'); s0.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline'; sp.appendChild(s0); bac.appendChild(sp);
    var r = doc.createRange(); r.setStart(sp.firstChild, 0); r.setEnd(sp.firstChild, 1);
    var a = s0.getBoundingClientRect().bottom - r.getBoundingClientRect().top; bac.textContent = '';
    return (cacheAsc[cle] = a);
  }
  function remplit(cible, contenu) {
    cible.textContent = '';
    var segs = typeof contenu === 'string' ? [{ t: contenu }] : contenu;
    segs.forEach(function (sg) {
      var hote = cible, txt = String(sg.t == null ? '' : sg.t);
      if (sg.couleur || sg.police || sg.classe || sg.style || sg.taille) {
        hote = doc.createElement('span'); if (sg.classe) hote.className = sg.classe; if (sg.style) hote.style.cssText = sg.style;
        if (sg.couleur) { hote.style.color = sg.couleur; hote.style.webkitTextFillColor = sg.couleur; } if (sg.police) hote.style.fontFamily = sg.police; if (sg.taille) hote.style.fontSize = sg.taille;
        cible.appendChild(hote);
      }
      txt.split('\n').forEach(function (l, i) { if (i) hote.appendChild(doc.createElement('br')); if (l) hote.appendChild(doc.createTextNode(l)); });
    });
  }

  TL.poseTout = function (cible) { var c = cible && cible.__trace; if (c) c.stop(); };

  var VIDE = 'polygon(0px 0px,0px 0px,0px 0px)';
  TL.trace = function (cible, contenu, options) {
    var o = options || {}, cps = (o.cps || TL.defauts.cps) * (o.vitesse || TL.defauts.vitesse), esp = o.espace == null ? TL.defauts.espace : o.espace;
    if (cible.__trace) cible.__trace.stop();
    var ctl = { glyphes: [], duree: 0, canevas: null, fini: false }, resFin, resPret, raf = 0, mort = false;
    ctl.fin = new Promise(function (r) { resFin = r; }); ctl.pret = new Promise(function (r) { resPret = r; });
    cible.__trace = ctl;
    if (contenu != null) remplit(cible, contenu);
    var cv = null, G = [], L = [], total = 0, t0 = 0, ig = 0, jd = 0, tPrec = -1, clipAvant = null;
    var ctx, fin, fctx, brouillon, bctx, s = 1, dpr = 1, kech = 1, er = null, cr = null;

    function decoupe(v) { cible.style.setProperty('-webkit-clip-path', v, 'important'); cible.style.setProperty('clip-path', v, 'important'); }
    function range() {
      if (cv && cv.parentNode) cv.parentNode.removeChild(cv); cv = null;
      if (clipAvant) {
        cible.style.removeProperty('-webkit-clip-path'); cible.style.removeProperty('clip-path');
        if (clipAvant[0]) cible.style.setProperty('clip-path', clipAvant[0], clipAvant[1]); if (clipAvant[2]) cible.style.setProperty('-webkit-clip-path', clipAvant[2], clipAvant[3]);
        clipAvant = null;
      }
      if (cible.__trace === ctl) delete cible.__trace;
    }
    function termine(interrompu) {
      if (ctl.fini) return; ctl.fini = true; mort = true; if (raf) racine.cancelAnimationFrame(raf);
      range(); var r = { interrompu: !!interrompu }; if (o.surFin) { try { o.surFin(r); } catch (e) { } } resPret(ctl); resFin(r);
    }
    ctl.stop = function () { termine(true); }; ctl.finir = function () { termine(false); };

    if (o.toutDeSuite || (o.respecteReduire !== false && TL.reduit())) { Promise.resolve().then(function () { termine(false); }); return ctl; }
    /* le texte réel est là, mis en page, mais rien n'en paraît : il est DÉCOUPÉ (clip-path), pas rendu transparent — ce qui est dévoilé est le vrai texte */
    clipAvant = [cible.style.getPropertyValue('clip-path'), cible.style.getPropertyPriority('clip-path'), cible.style.getPropertyValue('-webkit-clip-path'), cible.style.getPropertyPriority('-webkit-clip-path')];
    decoupe(VIDE);
    var styles = [], noeuds = [];
    (function () {
      var w = doc.createTreeWalker(cible, 4 /* SHOW_TEXT */, null), nd, memo = [];
      while ((nd = w.nextNode())) {
        var par = nd.parentNode, st = null, i;
        for (i = 0; i < memo.length; i++) if (memo[i][0] === par) st = memo[i][1];
        if (!st) { var c = racine.getComputedStyle(par); st = { color: (c.webkitTextFillColor && c.webkitTextFillColor !== 'currentcolor' ? c.webkitTextFillColor : c.color), fontFamily: c.fontFamily, fontSize: c.fontSize, fontWeight: c.fontWeight, fontStyle: c.fontStyle, tt: c.textTransform, ls: c.letterSpacing }; memo.push([par, st]); }
        noeuds.push(nd); styles.push(st);
      }
    })();
    var polices = {}; styles.forEach(function (st) { polices[st.fontStyle + ' ' + st.fontWeight + ' ' + st.fontSize + ' ' + st.fontFamily] = 1; });
    var attente = [];
    try { if (doc.fonts && doc.fonts.load) Object.keys(polices).forEach(function (f) { attente.push(doc.fonts.load(f).catch(function () { })); }); } catch (e) { }
    Promise.all(attente).then(function () { return doc.fonts && doc.fonts.ready; }).catch(function () { }).then(function () {
      if (mort) return;
      try { mesure(); } catch (e) { if (racine.console) racine.console.error('TraceLettres', e); termine(true); return; }
      resPret(ctl); if (!G.length) { termine(false); return; }
      if (!o.manuel) { try { prepare(G[0]); } catch (e) { } /* le premier glyphe est prêt AVANT que l'horloge parte */ t0 = racine.performance.now(); raf = racine.requestAnimationFrame(image); }
    });

    function mesure() {
      /* tout se mesure en pixels de la FENÊTRE (ce que rend getClientRects) ; kech = l'échelle d'un ancêtre transformé (1 hors de l'app réduite) */
      er = cible.getBoundingClientRect(); kech = cible.offsetWidth ? er.width / cible.offsetWidth : 1; if (!(kech > 0)) kech = 1;
      dpr = racine.devicePixelRatio || 1; s = dpr * kech;
      var mctx = doc.createElement('canvas').getContext('2d'), rg = doc.createRange(), cote = o.depart === 'b' ? 'b' : 'h', k = kech;
      var xmin = Infinity, ymin = Infinity, xmax = -Infinity, ymax = -Infinity, ni, i;
      for (ni = 0; ni < noeuds.length; ni++) {
        var nd = noeuds[ni], st = styles[ni], txt = nd.nodeValue, fam = famille(st.fontFamily), D = donnees(fam), fs = parseFloat(st.fontSize) || 16;
        var spec = st.fontStyle + ' ' + st.fontWeight + ' ' + fs + 'px ' + st.fontFamily, asc = null, ls = parseFloat(st.ls) || 0;
        mctx.font = spec;
        /* 1 · les caractères RENDUS de ce nœud, rangés par boîte de ligne. WebKit rend des rectangles de Range arrondis au pixel entier :
               ils ne servent qu'à savoir sur quelle ligne tombe un caractère, et à ENCADRER l'origine de la boîte */
        var boites = [], bt = null;
        for (i = 0; i < txt.length; i++) {
          var cp = txt.codePointAt(i), lg = cp > 0xFFFF ? 2 : 1, car = String.fromCodePoint(cp);
          rg.setStart(nd, i); rg.setEnd(nd, i + lg); var rs = rg.getClientRects(); i += lg - 1;
          if (!rs.length || (rs[0].width <= 0 && rs[0].height <= 0)) continue;
          var rc = rs[0], blanc = /\s/.test(car), aff = blanc ? ' ' : (st.tt === 'uppercase' ? car.toUpperCase() : (st.tt === 'lowercase' ? car.toLowerCase() : car)); if (aff.length !== car.length) aff = car;
          if (!bt || Math.abs(rc.top - bt.top) > 0.5 || rc.left < bt.dernier - 0.5) { bt = { top: rc.top, cars: [], txt: '' }; boites.push(bt); }
          bt.cars.push({ c: aff, blanc: blanc, L: rc.left, n: aff.length }); bt.txt += aff; bt.dernier = rc.left;
        }
        if (boites.length) asc = ascendante(st);
        boites.forEach(function (B) {
          /* 2 · dans la boîte : l'abscisse d'un caractère = la chasse cumulée (crénage compris) + l'interlettrage, comme le navigateur la calcule */
          var pos = 0, lo = -Infinity, hi = Infinity, j;
          for (j = 0; j < B.cars.length; j++) {
            var c = B.cars[j]; pos += c.n; c.av = mctx.measureText(c.c).width; c.a = (mctx.measureText(B.txt.slice(0, pos)).width - c.av + j * ls) * k;
            lo = Math.max(lo, c.L - c.a); hi = Math.min(hi, c.L - c.a + 1);     /* le rectangle rendu est le plancher de l'abscisse vraie */
          }
          var X0 = (lo <= hi) ? (lo + hi) / 2 : B.cars[0].L, r3 = Math.round(X0 * dpr) / dpr;
          if (lo <= hi && r3 >= lo - 0.02 && r3 <= hi + 0.02) X0 = r3;            /* une boîte commence presque toujours sur un pixel de l'appareil */
          var BASE = B.top + asc * k;
          B.cars.forEach(function (c) {
            if (c.blanc) { if (G.length) G[G.length - 1].pause += esp; return; }
            var aff = c.c, x = X0 + c.a, y = BASE, gd = D && D.g[aff], V = null, sc, av = c.av;
            if (gd) { V = gd[cote] ? cote : (gd.h ? 'h' : (gd.b ? 'b' : null)); }
            var inst = { car: aff, x: x, y: y, spec: spec, coul: st.color, pause: 0, police: fam, fs: fs, av: av, var: V, exception: !!(gd && V && V !== cote), demande: cote };
            if (gd && V) {
              sc = (gd.a > 0 ? av / gd.a : fs / D.upm); inst.sc = sc; inst.g = gd; inst.fin = gd[V].f; cote = gd[V].f; var u = sc * k;
              inst.bx0 = x + gd.bo[0] * u; inst.bx1 = x + gd.bo[2] * u; inst.by0 = y - gd.bo[3] * u; inst.by1 = y - gd.bo[1] * u;
              var pc = TL.parcours(fam, aff, V); inst.pc = pc; inst.l = (pc.longueur + pc.repasse * REPASSAGE) * sc / fs;
            } else {
              /* pas de chemin : un front vertical, de gauche à droite */
              var mt = mctx.measureText(aff), ga = mt.actualBoundingBoxLeft || 0, dr = mt.actualBoundingBoxRight || av, ha = mt.actualBoundingBoxAscent || fs * 0.8, ba = mt.actualBoundingBoxDescent || fs * 0.25;
              inst.bx0 = x - ga * k; inst.bx1 = x + dr * k; inst.by0 = y - ha * k; inst.by1 = y + ba * k; inst.l = Math.max(0.2, (dr + ga) / fs); inst.sc = 0; inst.fin = cote;
            }
            xmin = Math.min(xmin, inst.bx0); xmax = Math.max(xmax, inst.bx1); ymin = Math.min(ymin, inst.by0); ymax = Math.max(ymax, inst.by1);
            G.push(inst);
          });
        });
      }
      ctl.glyphes = G.map(function (g) { return { car: g.car, variante: g.var, demande: g.demande, fin: g.fin, exception: g.exception, x: (g.x - er.left) / k, y: (g.y - er.top) / k, ech: g.sc, police: g.police }; });
      if (!G.length) { ctl.duree = 0; return; }
      /* 3 · les lignes (pour la découpe du texte réel) */
      G.forEach(function (g) { var l = L.length ? L[L.length - 1] : null; if (!l || Math.abs(g.y - l.y) > 1) { l = { y: g.y, haut: Infinity, bas: -Infinity, n: 0 }; L.push(l); } g.ligne = L.length - 1; l.haut = Math.min(l.haut, g.by0); l.bas = Math.max(l.bas, g.by1); l.n++; });
      /* 4 · le canevas : un FRÈRE de la cible (il n'est pas découpé avec elle), calé sur un pixel entier de la fenêtre */
      /* sa taille est un nombre ENTIER de pixels CSS : sinon le navigateur arrondit sa boîte (au 1/64) et rééchantillonne l'image — un flou d'une rangée */
      var mg = 3, W = Math.round((Math.ceil((xmax - xmin) / k) + 2 * mg + 2) * s), H = Math.round((Math.ceil((ymax - ymin) / k) + 2 * mg + 2) * s);
      cv = doc.createElement('canvas'); cv.width = W; cv.height = H; cv.setAttribute('data-trace', ''); cv.setAttribute('aria-hidden', 'true');
      if (o.attributs) Object.keys(o.attributs).forEach(function (a) { cv.setAttribute(a, o.attributs[a]); });
      var pl = cible.offsetLeft + (xmin - mg - er.left) / k, pt = cible.offsetTop + (ymin - mg - er.top) / k;
      cv.style.cssText = 'position:absolute!important;display:block!important;pointer-events:none!important;margin:0!important;padding:0!important;border:0!important;background:none!important;opacity:1!important;visibility:visible!important;transform:none!important;max-width:none!important;max-height:none!important;min-width:0!important;min-height:0!important;box-sizing:content-box!important;z-index:' + (o.z == null ? 2 : o.z);
      function place() { cv.style.setProperty('left', pl + 'px', 'important'); cv.style.setProperty('top', pt + 'px', 'important'); cv.style.setProperty('width', (W / s) + 'px', 'important'); cv.style.setProperty('height', (H / s) + 'px', 'important'); }
      place(); cible.parentNode.insertBefore(cv, cible.nextSibling);
      cr = cv.getBoundingClientRect();
      /* on le ramène là où il devait être, puis sur un pixel entier (un bloc englobant inattendu, une bordure, un défilement) */
      pl += (Math.floor(xmin - mg) - cr.left) / k; pt += (Math.floor(ymin - mg) - cr.top) / k; place(); cr = cv.getBoundingClientRect();
      ctx = cv.getContext('2d'); ctl.canevas = cv;
      fin = doc.createElement('canvas'); fin.width = W; fin.height = H; fctx = fin.getContext('2d');
      brouillon = doc.createElement('canvas'); bctx = brouillon.getContext('2d', { willReadFrequently: true });
      var bw = 8, bh = 8;
      G.forEach(function (g) {
        g.gx = (g.x - cr.left) * dpr; g.gy = (g.y - cr.top) * dpr;
        g.e0 = (g.bx0 - cr.left) * dpr; g.e1 = (g.bx1 - cr.left) * dpr;                       /* l'encre, en pixels du canevas */
        g.X0 = Math.floor(g.e0) - 2; g.Y0 = Math.floor((g.by0 - cr.top) * dpr) - 2; g.w = Math.ceil(g.e1) + 2 - g.X0; g.h = Math.ceil((g.by1 - cr.top) * dpr) + 2 - g.Y0;
        bw = Math.max(bw, g.w); bh = Math.max(bh, g.h);
      });
      L.forEach(function (l, i) { l.y0 = i === 0 ? 0 : Math.floor(((L[i - 1].bas + l.haut) / 2 - cr.top) * dpr); }); L.forEach(function (l, i) { l.y1 = i + 1 < L.length ? L[i + 1].y0 : H; });
      brouillon.width = bw; brouillon.height = bh;
      /* 5 · la durée : N caractères à cps par seconde, à vitesse de plume constante ; une espace = une courte pause */
      var somme = 0; G.forEach(function (g) { somme += g.l; });
      var v = somme / (G.length / cps) / 1000;   /* longueur par ms */
      total = 0; G.forEach(function (g) { g.t0 = total; g.d = g.l / v; total += g.d + g.pause * 1000 / cps; });
      ctl.duree = total;
    }

    function prepare(g) {
      /* le glyphe réel, rendu une fois ; sa carte de temps */
      var d0 = racine.performance.now();
      bctx.setTransform(1, 0, 0, 1, 0, 0); bctx.clearRect(0, 0, g.w, g.h);
      bctx.setTransform(s, 0, 0, s, g.gx - g.X0, g.gy - g.Y0); bctx.font = g.spec; bctx.fillStyle = g.coul; bctx.textBaseline = 'alphabetic'; bctx.fillText(g.car, 0, 0);
      bctx.setTransform(1, 0, 0, 1, 0, 0);
      var im = bctx.getImageData(0, 0, g.w, g.h), d = im.data, n = g.w * g.h, A = new Uint8ClampedArray(n), p;
      for (p = 0; p < n; p++) A[p] = d[4 * p + 3];
      var traits, moves = [], u = g.sc * s, ox = g.gx - g.X0, oy = g.gy - g.Y0;
      if (g.pc) {
        traits = g.pc.traits.map(function (t) { return { R: Math.max(t.R * u, 0.75), b0: t.b0, b1: t.b1, pts: t.pts.map(function (q) { return [ox + q[0] * u, oy - q[1] * u]; }) }; });
        var acc = 0; g.pc.ordre.forEach(function (st) { if (st[0] === 'r') acc += st[1] * u; else if (st[0] === 't') { moves.push(acc); acc = 0; } });
      } else { traits = [{ R: g.h, pts: [[1, g.h / 2], [g.w - 1, g.h / 2]] }]; moves = [0]; }
      var c = carte(A, g.w, g.h, traits, moves);
      g.im = im; g.A = A; g.T = c.T; g.D = c.D; g.pret = true;
      TL.mesures.prep.push(racine.performance.now() - d0); if (TL.mesures.prep.length > 4000) TL.mesures.prep.splice(0, 2000);
    }
    function pose(g) {
      /* le glyphe fini, dans le canevas, en attendant que le texte réel le prenne */
      fctx.setTransform(s, 0, 0, s, g.gx, g.gy); fctx.font = g.spec; fctx.fillStyle = g.coul; fctx.textBaseline = 'alphabetic'; fctx.fillText(g.car, 0, 0); fctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(g.X0, g.Y0, g.w, g.h); ctx.drawImage(fin, g.X0, g.Y0, g.w, g.h, g.X0, g.Y0, g.w, g.h);
      g.im = g.A = g.T = null; g.pret = false;
    }
    function partiel(g, frac) {
      if (!g.pret) prepare(g);
      var t = -0.5 + frac * (g.D + 1), d = g.im.data, A = g.A, T = g.T, n = g.w * g.h, p, m, a;
      for (p = 0; p < n; p++) { a = A[p]; if (!a) continue; m = t - T[p] + 0.5; d[4 * p + 3] = m <= 0 ? 0 : (m >= 1 ? a : Math.round(a * m)); }
      bctx.putImageData(g.im, 0, 0);
      ctx.clearRect(g.X0, g.Y0, g.w, g.h); ctx.drawImage(fin, g.X0, g.Y0, g.w, g.h, g.X0, g.Y0, g.w, g.h); ctx.drawImage(brouillon, 0, 0, g.w, g.h, g.X0, g.Y0, g.w, g.h);
    }
    function front() {
      /* LE TEXTE RÉEL PREND LES GLYPHES FINIS : dès qu'une coupe verticale franche existe entre le dernier glyphe fini et le suivant,
         la découpe du texte avance jusqu'à elle et le canevas rend ce qu'il montrait. À la fin il ne reste que le texte, tel qu'il est sans tracé. */
      var m = -1, j, coupe = 0, dmax;
      for (j = ig - 1; j >= jd; j--) {
        var nx = G[j + 1];
        if (!nx || nx.ligne !== G[j].ligne) { m = j; coupe = -1; break; }
        dmax = -Infinity; for (var q = j; q >= 0 && G[q].ligne === G[j].ligne; q--) dmax = Math.max(dmax, G[q].e1);
        var c = Math.floor(nx.e0) - 1; if (c >= Math.ceil(dmax) + 1) { m = j; coupe = c; break; }
      }
      if (m < 0) return;
      jd = m + 1;
      if (jd >= G.length) { decoupe('none'); ctx.clearRect(0, 0, cv.width, cv.height); fctx.clearRect(0, 0, cv.width, cv.height); return; }
      var l = L[G[jd].ligne], xc = coupe < 0 ? -1 : coupe, M = 4000;
      function lx(v) { return ((cr.left + v / dpr) - er.left) / kech; } function ly(v) { return ((cr.top + v / dpr) - er.top) / kech; }
      var X = xc < 0 ? -M : lx(xc), Y0 = G[jd].ligne === 0 ? -M : ly(l.y0), Y1 = G[jd].ligne === L.length - 1 ? M : ly(l.y1);
      decoupe('polygon(' + (-M) + 'px ' + (-M) + 'px,' + M + 'px ' + (-M) + 'px,' + M + 'px ' + Y0 + 'px,' + X + 'px ' + Y0 + 'px,' + X + 'px ' + Y1 + 'px,' + (-M) + 'px ' + Y1 + 'px)');
      [ctx, fctx].forEach(function (g2) { if (l.y0 > 0) g2.clearRect(0, 0, cv.width, l.y0); if (xc > 0) g2.clearRect(0, l.y0, xc, l.y1 - l.y0); });
    }
    function rend(t) {
      if (!cv) return;
      if (t < tPrec) { ctx.clearRect(0, 0, cv.width, cv.height); fctx.clearRect(0, 0, fin.width, fin.height); G.forEach(function (g) { g.pret = false; }); ig = 0; jd = 0; decoupe(VIDE); }
      tPrec = t;
      var avant = ig;
      while (ig < G.length && t >= G[ig].t0 + G[ig].d) { pose(G[ig]); ig++; }
      if (ig !== avant) front();
      if (ig < G.length && t > G[ig].t0) partiel(G[ig], (t - G[ig].t0) / G[ig].d);
    }
    function image(maintenant) {
      if (mort) return; var d0 = racine.performance.now(), t = maintenant - t0; if (t < 0) t = 0;
      rend(t); TL.mesures.image.push(racine.performance.now() - d0); if (TL.mesures.image.length > 8000) TL.mesures.image.splice(0, 4000);
      if (t >= total) { termine(false); return; }
      raf = racine.requestAnimationFrame(image);
    }
    ctl.va = function (p) { rend(Math.max(0, Math.min(1, p)) * total + (p >= 1 ? 1 : 0)); };
    ctl.etat = function () { return { glyphe: ig, texteReel: jd, total: G.length }; };
    return ctl;
  };

  /* ── le mode « montre le chemin » : la ligne médiane, l'ordre, le départ, l'arrivée, les repassages ── */
  TL.dessineChemin = function (ctx, police, car, v, ox, oy, ech, opt) {
    var pc = TL.parcours(police, car, v); if (!pc) return null; opt = opt || {};
    var coul = opt.couleurs || ['#D63031', '#0984E3', '#009464', '#E18700', '#8C46C8', '#0096A0', '#E63C96'], ep = opt.epaisseur || 2;
    function P(q) { return [ox + q[0] * ech, oy - q[1] * ech]; }
    function ligne(pts) { ctx.beginPath(); pts.forEach(function (q, i) { var p = P(q); if (i) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]); }); ctx.stroke(); }
    ctx.save(); ctx.lineCap = 'butt'; ctx.lineJoin = 'round';
    ctx.setLineDash([ep * 2, ep * 2]); ctx.lineWidth = ep * 0.75; ctx.strokeStyle = opt.repassage || '#888';
    pc.repassages.forEach(function (r) { ligne(r); });
    ctx.setLineDash([ep * 0.5, ep * 2.5]); pc.sauts.forEach(function (sa) { ligne(sa); });
    ctx.setLineDash([]); ctx.lineWidth = ep;
    pc.traits.forEach(function (t, i) {
      var c = coul[i % coul.length]; ctx.strokeStyle = c; ctx.fillStyle = c; ligne(t.pts);
      /* la pointe, au bout du trait : le sens */
      var n = t.pts.length, a = P(t.pts[n - 2]), b = P(t.pts[n - 1]), dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, T = ep * 3.2; dx /= l; dy /= l;
      ctx.beginPath(); ctx.moveTo(b[0], b[1]); ctx.lineTo(b[0] - dx * T - dy * T * 0.6, b[1] - dy * T + dx * T * 0.6); ctx.lineTo(b[0] - dx * T + dy * T * 0.6, b[1] - dy * T - dx * T * 0.6); ctx.closePath(); ctx.fill();
      if (opt.numeros !== false) { var d0 = P(t.pts[0]); ctx.font = '700 ' + Math.round(ep * 5.5) + 'px system-ui,sans-serif'; ctx.fillText(String(i + 1), d0[0] + ep * 2, d0[1] - ep * 2); }
    });
    if (pc.depart) { var d = P(pc.depart), a2 = P(pc.arrivee); ctx.lineWidth = ep; ctx.strokeStyle = opt.depart || '#009464'; ctx.beginPath(); ctx.arc(d[0], d[1], ep * 2.6, 0, 6.2832); ctx.stroke();
      ctx.strokeStyle = opt.arrivee || '#D63031'; ctx.strokeRect(a2[0] - ep * 2.2, a2[1] - ep * 2.2, ep * 4.4, ep * 4.4); }
    ctx.restore(); return pc;
  };

  racine.TraceLettres = TL;
})(typeof window !== 'undefined' ? window : this);
