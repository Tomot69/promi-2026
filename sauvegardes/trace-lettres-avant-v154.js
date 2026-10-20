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
       options  cps          caractères par seconde (22 ; v153, Tom : 20 à 25 au départ, réglable ; `?cps=` dans l'adresse)
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
  var TL = { version: 2, defauts: { cps: 22, vitesse: 1, depart: 'h', espace: 0.4 }, mesures: { prep: [], image: [], cache: 0 }, _cache: {}, _cacheN: 0 };
  /* ⚑ v153 (Tom, C-125, récidive : « les lettres font pof ») — LA CAUSE, mesurée au banc WebKit : le module traçait bien (chemins trouvés pour Gilbert,
     Atkinson et PromiLate, cartes calculées dans le Worker), mais à 50 caractères par seconde une lettre durait ≈ 20 ms — à peine plus d'une image à
     60 Hz : elle paraissait d'un coup, puis la suivante. Tom : « PLUS LENT, 20 à 25 caractères par seconde au départ, réglable ». Défaut : 22.
     `?cps=N` (5 à 80) règle la vitesse de toute la page ; `?tlv=0.05` la ralentit (×0,05 : pour regarder une lettre se constituer). Jamais mémorisés. */
  try { var _q = (racine.location && racine.location.search) || '', _m = /[?&]cps=([\d.]+)/.exec(_q), _v = /[?&]tlv=([\d.]+)/.exec(_q);
    if (_m && +_m[1] > 0) TL.defauts.cps = Math.max(5, Math.min(80, +_m[1])); if (_v && +_v[1] > 0) TL.defauts.vitesse = Math.max(0.01, Math.min(4, +_v[1])); } catch (e) { }
  var REPASSAGE = 0.1;      /* un repassage dure le dixième du temps qu'il aurait pris tracé : « un instant » */
  var PIVOT = 0.5;          /* à un sommet de la ligne, le front pivote : le temps du pivot, en part de l'arc extérieur */
  var doc = racine.document;

  function donnees(nom) { var T = racine.TraceLettresChemins || {}; return T[nom] || null; }
  /* l'ouvrier : ce même fichier, chargé dans un Worker, n'y fait que des cartes */
  var SRC = (doc && doc.currentScript && doc.currentScript.src) || null; TL._nId = 0; TL._attente = {};
  function ouvrier() {
    if (TL._ouvrier !== undefined) return TL._ouvrier;
    TL._ouvrier = null;
    try {
      if (!SRC || !racine.Worker || !racine.Blob || !racine.URL || TL.sansOuvrier) return null;
      var code = 'importScripts(' + JSON.stringify(SRC) + ');onmessage=function(e){var d=e.data,r=self.TraceLettres._carte(d.A,d.w,d.h,d.traits,d.moves);postMessage({id:d.id,T:r.T,D:r.D},[r.T.buffer]);};';
      var w = new racine.Worker(racine.URL.createObjectURL(new racine.Blob([code], { type: 'application/javascript' })));
      w.onmessage = function (e) { var f = TL._attente[e.data.id]; delete TL._attente[e.data.id]; if (f) f(e.data.T, e.data.D); };
      w.onerror = function () { TL._ouvrier = null; var at = TL._attente; TL._attente = {}; Object.keys(at).forEach(function (k) { try { at[k](null); } catch (e) { } }); };
      TL._ouvrier = w;
    } catch (e) { TL._ouvrier = null; }
    return TL._ouvrier;
  }
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
    /* ⚑ v147 (Tom, C-125 : « les barres du t et du f ») — UNE BARRE QUI TRAVERSE UN FÛT. Le chemin d'une barre droite part de l'axe du fût (un
       embranchement, « j ») ; la part de la barre qui dépasse DE L'AUTRE CÔTÉ du fût n'avait aucun chemin : ses pixels prenaient l'instant de leurs
       voisins du fût et paraissaient d'un coup, en morceau, pendant que le fût descendait. On la rend à sa barre : depuis l'embranchement, on suit
       l'encre vers l'extérieur ; si elle continue au-delà d'une demi-largeur de fût (1,12 R + 2 px), la barre est prolongée jusqu'au bord de l'encre et ce
       bout devient libre. Seulement pour une barre DROITE (une courbe qui rejoint une panse ne traverse rien). */
    function encre(px, py) { var xi = Math.floor(px), yi = Math.floor(py); return xi >= 0 && yi >= 0 && xi < w && yi < h && A[yi * w + xi] > 127; }
    function suit(px, py, dx, dy, max) { var L = 0; while (L < max && encre(px + dx * (L + 0.5), py + dy * (L + 0.5))) L += 0.5; return L; }
    traits.forEach(function (t) {
      var P = t.pts, m = P.length - 1; if (m < 1) return;
      var a0 = P[0], b0 = P[m], Lk = Math.hypot(b0[0] - a0[0], b0[1] - a0[1]), ec = 0, j;
      for (j = 1; j < m && Lk > 0; j++) ec = Math.max(ec, Math.abs((P[j][0] - a0[0]) * (b0[1] - a0[1]) - (P[j][1] - a0[1]) * (b0[0] - a0[0])) / Lk);
      if (!(Lk > 0 && ec < 0.6)) return;
      var dx = (b0[0] - a0[0]) / Lk, dy = (b0[1] - a0[1]) / Lk, L;
      /* le bout prolongé doit être une BARRE : près de son extrémité, l'encre en travers fait la largeur du trait (pas un autre trait traversé de
         biais — la barre penchée du « e » rejoint la panse, elle ne la traverse pas) */
      function barre(px, py) { var e = suit(px, py, -dy, dx, 6 * t.R) + suit(px, py, dy, -dx, 6 * t.R); return e <= 2 * t.R + 4; }
      if (Math.abs(dy) > 0.17) return;   /* une barre HORIZONTALE seulement (celles du « t » et du « f ») — la barre penchée du « e » rejoint sa panse */
      if (t.b0 === 'j') { L = suit(a0[0], a0[1], -dx, -dy, 8 * t.R); if (L > 1.12 * t.R + 2 && barre(a0[0] - dx * (L - 2), a0[1] - dy * (L - 2))) { P.unshift([a0[0] - dx * (L - 0.5), a0[1] - dy * (L - 0.5)]); t.b0 = 'l'; t.prolonge = (t.prolonge || 0) + L; } }
      if (t.b1 === 'j') { L = suit(b0[0], b0[1], dx, dy, 8 * t.R); if (L > 1.12 * t.R + 2 && barre(b0[0] + dx * (L - 2), b0[1] + dy * (L - 2))) { P.push([b0[0] + dx * (L - 0.5), b0[1] + dy * (L - 0.5)]); t.b1 = 'l'; t.prolonge = (t.prolonge || 0) + L; } }
    });
    var faible = new Uint8Array(n), Dl = new Float32Array(n), parBout = new Uint8Array(n);   /* v153 : 1 = pris par l'extension du BOUT d'un trait (pas dans sa longueur) */   /* v147 : un pixel pris par le BOUT LIBRE d'un trait, là où ce bout court DANS un autre trait */
    for (p = 0; p < n; p++) { own[p] = -1; Tl[p] = Infinity; Dl[p] = Infinity; }
    /* ⚑ v147 (C-125 : « les dents du g ») — la ligne d'un trait COURBE est adoucie (deux passes de Chaikin, extrémités gardées) : le chemin tiré du
       squelette de la police a des coudes (la fin de la panse du « g » file d'un coup vers la jonction) ; la bande d'un trait suit ses segments,
       et chaque coude faisait une marche dans son bord. */
    traits.forEach(function (t) { var P = t.pts; if (P.length < 3) return;
      var a0 = P[0], b0 = P[P.length - 1], Lk = Math.hypot(b0[0] - a0[0], b0[1] - a0[1]), ec = 0, j;
      for (j = 1; j < P.length - 1 && Lk > 0; j++) ec = Math.max(ec, Math.abs((P[j][0] - a0[0]) * (b0[1] - a0[1]) - (P[j][1] - a0[1]) * (b0[0] - a0[0])) / Lk);
      if (Lk > 0 && ec < 0.6) return;
      for (var pas = 0; pas < 2; pas++) { var Q = [P[0]]; for (j = 0; j < P.length - 1; j++) { var u0 = P[j], u1 = P[j + 1];
          if (j > 0) Q.push([0.75 * u0[0] + 0.25 * u1[0], 0.75 * u0[1] + 0.25 * u1[1]]);
          if (j < P.length - 2) Q.push([0.25 * u0[0] + 0.75 * u1[0], 0.25 * u0[1] + 0.75 * u1[1]]); }
        Q.push(P[P.length - 1]); P = Q; }
      t.pts = P; });
    /* ⚑ v153 (Tom, C-125 : « aucune zone abstraite ») — LES COINS FRANCS. Deux traits qui se rejoignent par un bout en faisant un ANGLE (plus de 40°
       entre leurs directions : le fût et la panse du « g » d'Atkinson, en haut à droite) ne se partagent plus l'encre par la bissectrice de leurs lignes
       — elle coupait le coin en triangles, l'un paraissant avec le premier trait, l'autre avec le dernier, comme des éclats. Près d'un coin franc, le
       trait tracé LE PREMIER garde toute sa largeur (le coin naît avec lui, d'une coupe nette) ; l'autre s'arrête sur son bord. Une jonction DOUCE
       (deux traits qui se continuent : la panse et la queue du « g » de Gilbert) garde la bissectrice. */
    var coins = [];
    (function () { var a, b, ea, eb;
      function dirAu(t, fin) { var P = t.pts, m = P.length - 1, i0 = fin ? m : 0, i1 = fin ? Math.max(0, m - 1) : Math.min(m, 1), dx = P[i0][0] - P[i1][0], dy = P[i0][1] - P[i1][1], l = Math.hypot(dx, dy) || 1; return [dx / l, dy / l]; }
      /* seulement une FERMETURE : un trait qui vient finir là où un trait d'avant a COMMENCÉ (la panse du « g » qui revient au haut du fût). Au tournant
         d'un trait vers le suivant (la fin de l'un, le départ de l'autre : « m », « x », « k »), la coupe en onglet est celle d'une plume qui tourne : elle tient. */
      for (a = 0; a < traits.length; a++) for (b = a + 1; b < traits.length; b++) for (ea = 0; ea < 1; ea++) for (eb = 1; eb < 2; eb++) {
        var Pa = traits[a].pts, Pb = traits[b].pts; if (Pa.length < 2 || Pb.length < 2) continue;
        var qa = ea ? Pa[Pa.length - 1] : Pa[0], qb = eb ? Pb[Pb.length - 1] : Pb[0];
        if (Math.hypot(qa[0] - qb[0], qa[1] - qb[1]) > 2 + 0.15 * Math.min(traits[a].R, traits[b].R)) continue;
        var da = dirAu(traits[a], ea), db = dirAu(traits[b], eb), c = Math.abs(da[0] * db[0] + da[1] * db[1]);
        if (c > Math.cos(40 * Math.PI / 180)) continue;   /* une jonction douce : la bissectrice tient */
        coins.push({ x: (qa[0] + qb[0]) / 2, y: (qa[1] + qb[1]) / 2, r: 2.6 * Math.max(traits[a].R, traits[b].R) + 2, a: a, b: b });   /* la tête entière d'un fût (deux demi-largeurs, et sa marge) */
      } })();
    /* (un trait DROIT garde sa règle : il l'emporte toujours — le fût du « a » de Gilbert ; la règle du coin ne vaut qu'entre deux traits courbes) */
    function premierAuCoin(p1, p2, px, py) { if (traits[p1].droit || traits[p2].droit) return -1; for (var ci = 0; ci < coins.length; ci++) { var C = coins[ci]; if (((C.a === p1 && C.b === p2) || (C.a === p2 && C.b === p1)) && Math.hypot(px - C.x, py - C.y) <= C.r) return Math.min(p1, p2); } return -1; }
    function coinDe(px, py) { for (var ci = 0; ci < coins.length; ci++) { var C = coins[ci]; if (traits[C.a].droit || traits[C.b].droit) continue; if (Math.hypot(px - C.x, py - C.y) <= C.r) return C; } return null; }
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
    /* ⚑ v147 (C-125) — la longueur d'un BOUT (libre, ou un embranchement) qui court DANS un autre trait : depuis l'extrémité, tant que la ligne du trait reste à moins
       d'une demi-largeur (+1) de la ligne d'un autre trait. Ces pixels-là reviennent à l'autre trait (voir plus bas). */
    function dSeg(px, py, Q) { var best = Infinity, ii; for (ii = 0; ii < Q.length - 1; ii++) { var ax = Q[ii][0], ay = Q[ii][1], bx = Q[ii + 1][0], by = Q[ii + 1][1], vx = bx - ax, vy = by - ay, l2 = vx * vx + vy * vy, tt = l2 > 0 ? Math.max(0, Math.min(1, ((px - ax) * vx + (py - ay) * vy) / l2)) : 0, ddx = px - ax - vx * tt, ddy = py - ay - vy * tt, dd = ddx * ddx + ddy * ddy; if (dd < best) best = dd; } return Math.sqrt(best); }
    function dedans(kk2, deb) { var Pt = traits[kk2].pts, Q = deb ? Pt : Pt.slice().reverse(), s0 = 0, ii, jj;
      for (ii = 0; ii < Q.length - 1; ii++) { var sx = Q[ii][0], sy = Q[ii][1], vx = Q[ii + 1][0] - sx, vy = Q[ii + 1][1] - sy, ll = Math.hypot(vx, vy);
        for (var st = 0; st < ll; st += 1) { var px = sx + vx * st / ll, py = sy + vy * st / ll, dans = false;
          for (jj = 0; jj < traits.length && !dans; jj++) if (jj !== kk2 && dSeg(px, py, traits[jj].pts) <= traits[jj].R + 1) dans = true;
          if (!dans) return s0 + st; }
        s0 += ll; }
      return s0; }
    for (k = 0; k < traits.length; k++) { traits[k].in0 = (traits[k].b0 || 'l') !== 'c' ? dedans(k, true) : 0; traits[k].in1 = (traits[k].b1 || 'l') !== 'c' ? dedans(k, false) : 0; }   /* un bout libre ou un embranchement ; jamais un coin */
    /* ⚑ v153 (Tom, C-125 : « aucune zone abstraite ») — LES ERGOTS. Un trait droit plus court que 1,6 largeur, accolé par un bout au trait courbe qui le
       suit (au départ) ou qui le précède (à la fin), n'est pas un geste : c'est le chemin qui rejoint le coin d'un bout biseauté (le départ du « s »
       d'Atkinson, le bout de la queue de son « g »). Tracé à part, il paraissait en bloc, et la pointe du biseau après lui. Son encre PROLONGE le trait
       voisin : elle se dévoile par le même front (la passe de la ligne la plus proche, avec le prolongement du bout). */
    function memePoint(p1, p2, Rr) { return Math.hypot(p1[0] - p2[0], p1[1] - p2[1]) <= 2 + 0.15 * Rr; }
    for (k = 0; k < traits.length; k++) { var tk = traits[k], Lk2 = 0; if (!tk.droit || tk.pts.length < 2) continue;
      for (i = 1; i < tk.pts.length; i++) Lk2 += Math.hypot(tk.pts[i][0] - tk.pts[i - 1][0], tk.pts[i][1] - tk.pts[i - 1][1]);
      if (Lk2 >= 1.6 * tk.R) continue;
      var suiv2 = traits[k + 1], prec2 = traits[k - 1];
      var auDepart = suiv2 && !suiv2.droit && memePoint(tk.pts[tk.pts.length - 1], suiv2.pts[0], tk.R) && !(prec2 && memePoint(prec2.pts[prec2.pts.length - 1], tk.pts[0], tk.R));
      var aLaFin = prec2 && !prec2.droit && memePoint(tk.pts[0], prec2.pts[prec2.pts.length - 1], tk.R) && !(suiv2 && memePoint(tk.pts[tk.pts.length - 1], suiv2.pts[0], tk.R));
      if (auDepart || aLaFin) tk.ergot = 1; }   /* (au départ : rien n'y arrive ; à la fin : rien n'en repart — sinon c'est un vrai tronçon du geste) */
    for (k = 0; k < traits.length; k++) if (traits[k].droit && !traits[k].ergot) rang.push(k);
    for (k = 0; k < traits.length; k++) if (!traits[k].droit && !traits[k].ergot) rang.push(k);
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
            p = y * w + x; if (!A[p]) continue; var o = own[p]; if (o !== -1 && o !== k && !faible[p] && (traits[o].droit || traits[k].droit) && !(coins.length && premierAuCoin(o, k, x + 0.5, y + 0.5) === k)) continue;
            var rx = x + 0.5 - g.x, ry = y + 0.5 - g.y, u = rx * g.dx + ry * g.dy, lat = ry * g.dx - rx * g.dy, cand = Infinity;
            if (lat <= Rp && lat >= -Rp && u >= 0 && u <= g.len) cand = g.s + u;
            var dl = Math.abs(lat);
            var parCap = false;
            if (cand === Infinity && i === 0 && cap0 > 0 && u < 0) { var us = rx * d0[0] + ry * d0[1], ls = ry * d0[0] - rx * d0[1]; if (us < 0 && us >= -cap0 && ls <= Rp && ls >= -Rp) cand = g.s + us; parCap = true; }
            if (cand === Infinity && i === ns - 1 && cap1 > 0 && u > g.len) { var ex2 = x + 0.5 - ex, ey2 = y + 0.5 - ey, ue = ex2 * d1[0] + ey2 * d1[1], le = ey2 * d1[0] - ex2 * d1[1]; if (ue > 0 && ue <= cap1 && le <= Rp && le >= -Rp) cand = g.s + g.len + ue; parCap = true; }
            if (g2 && u > g.len && cand === Infinity) {
              var qx = x + 0.5 - g2.x, qy = y + 0.5 - g2.y, u2 = qx * g2.dx + qy * g2.dy;
              if (u2 < 0 && qx * qx + qy * qy <= Rp * Rp) { var a = u - g.len, b = -u2; cand = g.s + g.len + g.delta * (a / (a + b + 1e-9)); }
            }
            /* ⚑ v147 (Tom, C-125 : « la fente au départ du é ») — LE BOUT LIBRE D'UN TRAIT CÈDE au milieu d'un autre. La barre du « e » part, libre,
               DANS le trait de la panse : elle passait la première et prenait ce morceau de panse, qui paraissait avec elle, fendu de biais. Un pixel
               pris par un bout libre, là où ce bout court DANS un autre trait (`in0`, `in1`), revient au trait qui le traverse en plein. */
            if (cand !== Infinity) {
              var fin0 = segs2[ns - 1].s + segs2[ns - 1].len, bout = (traits[k].in0 > 0 && cand < traits[k].in0) || (traits[k].in1 > 0 && fin0 - cand < traits[k].in1);
              /* ⚑ v147 (C-125 : « les dents du g ») — entre deux traits COURBES qui se recouvrent (la fin de la panse et le départ de son autre moitié,
                 à la jonction de la queue du « g »), le pixel va au trait dont la LIGNE est la plus proche : la frontière suit la bissectrice des
                 deux lignes, une courbe lisse. L'ordre du tracé la découpait selon les rectangles des segments du chemin — en dents. Un fût garde sa
                 priorité (règle du trait droit). */
              var pc0 = (o !== -1 && o !== k) ? premierAuCoin(o, k, x + 0.5, y + 0.5) : -1;
              /* v153 : au coin franc, l'encre que les deux traits couvrent va au premier tracé (la tête du fût du « g » d'Atkinson naît avec lui) */
              if (pc0 >= 0) { if (pc0 === k) { Tl[p] = cand; own[p] = k; faible[p] = 0; Dl[p] = dl; parBout[p] = parCap ? 1 : 0; } }
              else if (o !== -1 && o !== k) { if ((faible[p] && !bout) || (!traits[o].droit && !traits[k].droit && dl < Dl[p] - 0.5 && !bout)) { Tl[p] = cand; own[p] = k; faible[p] = 0; Dl[p] = dl; } }
              else if (cand < Tl[p]) { Tl[p] = cand; own[p] = k; faible[p] = bout ? 1 : 0; Dl[p] = dl; parBout[p] = parCap ? 1 : 0; }
            }
          }
        }
      }
      for (p = 0; p < n; p++) if (own[p] === k) { if (Tl[p] < tmin) tmin = Tl[p]; if (Tl[p] > tmax) tmax = Tl[p]; }
      mins[k] = tmin; maxs[k] = tmax;
    }
    /* ⚑ v147 (Tom, C-125 : « les dents du g ») — LES TRAITS COURBES SE PARTAGENT L'ENCRE PAR LA LIGNE LA PLUS PROCHE. Avant, chaque trait ne prenait
       que la bande de ses segments (une demi-largeur de part et d'autre) : là où un chemin coupe en biais vers un embranchement (la fin de la panse
       du « g », qui file vers la jonction de la queue), le bord du trait n'était pas couvert — ces pixels allaient au trait suivant, qui passe plus
       tard, et la panse se dessinait avec des dents. Tout pixel d'encre qu'AUCUNE bande ne couvre va au trait
       courbe dont la ligne est la plus proche ; son instant est celui du point de cette ligne où il se projette. La frontière entre deux traits
       est alors la bissectrice de leurs lignes : une courbe lisse. */
    /* v153 — au coin franc, l'encre qui PROLONGE le départ du premier tracé (au-delà de son bout, dans sa largeur) lui revient, quel que soit le trait
       qui l'a prise : la tête biseautée d'un fût se dévoile avec lui, d'une coupe plate, avant son corps */
    coins.forEach(function (C) { var kf = Math.min(C.a, C.b), sg = S[kf]; if (!sg || !sg.length || traits[kf].b0 !== 'c' || traits[C.a].droit || traits[C.b].droit) return;
      var G0 = sg[0]; if (Math.hypot(G0.x - C.x, G0.y - C.y) > 2 + 0.15 * traits[kf].R) return;
      /* de quel côté de sa ligne arrive l'autre trait : de ce côté la tête s'arrête à une demi-largeur (+1,5) ; de l'autre, son bord d'anticrénelage compris (+3) */
      var ko = C.a === kf ? C.b : C.a, Po = traits[ko].pts, cxo = 0, cyo = 0; Po.forEach(function (q) { cxo += q[0]; cyo += q[1]; }); cxo /= Po.length; cyo /= Po.length;
      var cote0 = ((cyo - G0.y) * G0.dx - (cxo - G0.x) * G0.dy) >= 0 ? 1 : -1;
      var xa = Math.max(0, Math.floor(C.x - C.r)), xb = Math.min(w - 1, Math.ceil(C.x + C.r)), ya = Math.max(0, Math.floor(C.y - C.r)), yb = Math.min(h - 1, Math.ceil(C.y + C.r)), xx, yy, q;
      for (yy = ya; yy <= yb; yy++) for (xx = xa; xx <= xb; xx++) { q = yy * w + xx; if (!A[q]) continue;
        var u0 = (xx + 0.5 - G0.x) * G0.dx + (yy + 0.5 - G0.y) * G0.dy, ls0 = (yy + 0.5 - G0.y) * G0.dx - (xx + 0.5 - G0.x) * G0.dy, l0 = Math.abs(ls0);
        var lim0 = traits[kf].R + ((ls0 >= 0 ? 1 : -1) === cote0 ? 1.5 : 4.5), dansC = Math.hypot(xx + 0.5 - C.x, yy + 0.5 - C.y) <= C.r;
        if (u0 < 0 && l0 <= lim0 && dansC) { own[q] = kf; Tl[q] = u0; Dl[q] = l0; faible[q] = 0; }
        else if (u0 >= 0 && u0 <= G0.len && own[q] === ko && (ls0 >= 0 ? 1 : -1) !== cote0 && l0 <= lim0 && dansC) { own[q] = kf; Tl[q] = G0.s + u0; Dl[q] = l0; faible[q] = 0; } } });   /* le bord du fût, du côté opposé */
    for (k = 0; k < traits.length; k++) { var tn0 = Infinity, tx0 = -Infinity; for (p = 0; p < n; p++) if (own[p] === k) { if (Tl[p] < tn0) tn0 = Tl[p]; if (Tl[p] > tx0) tx0 = Tl[p]; } if (tn0 < Infinity) { mins[k] = tn0; maxs[k] = tx0; } }
    var courbes = []; for (k = 0; k < traits.length; k++) if (!traits[k].droit && S[k].length) courbes.push(k);
    if (courbes.length) {
      for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
        p = y * w + x; if (!A[p]) continue; var o2 = own[p]; if (o2 >= 0 && !faible[p]) continue;   /* seulement l'encre qu'aucune bande ne couvre (et les bouts qui cèdent) : là où deux bandes se recouvrent, l'ordre du tracé tient */
        var px2 = x + 0.5, py2 = y + 0.5, best = Infinity, bk = -1, bt = 0, ci, si;
        for (ci = 0; ci < courbes.length; ci++) { var kc = courbes[ci], sg = S[kc];
          for (si = 0; si < sg.length; si++) { var G = sg[si], rx2 = px2 - G.x, ry2 = py2 - G.y, uu = rx2 * G.dx + ry2 * G.dy, ul = uu < 0 ? 0 : (uu > G.len ? G.len : uu), ex3 = rx2 - G.dx * ul, ey3 = ry2 - G.dy * ul, dd2 = ex3 * ex3 + ey3 * ey3;
            if (dd2 < best) { best = dd2; bk = kc; bt = G.s + ul + (uu < 0 && si === 0 ? uu : 0) + (uu > G.len && si === sg.length - 1 ? uu - G.len : 0); } } }
        if (bk < 0) continue;
        var Cc = coins.length ? coinDe(px2, py2) : null;
        if (Cc) { var kf = Math.min(Cc.a, Cc.b), sgf = S[kf];   /* v153 : au coin franc, l'encre libre va au premier tracé, à l'instant de sa projection */
          if (sgf && sgf.length) { var bf = Infinity, tf = 0; for (si = 0; si < sgf.length; si++) { var Gf = sgf[si], rxf = px2 - Gf.x, ryf = py2 - Gf.y, uf = rxf * Gf.dx + ryf * Gf.dy, ulf = uf < 0 ? 0 : (uf > Gf.len ? Gf.len : uf), exf = rxf - Gf.dx * ulf, eyf = ryf - Gf.dy * ulf, df = exf * exf + eyf * eyf;
              if (df < bf) { bf = df; tf = Gf.s + ulf + (uf < 0 && si === 0 ? uf : 0) + (uf > Gf.len && si === sgf.length - 1 ? uf - Gf.len : 0); } }
            /* dans le corps du premier tracé : à moins de 1,25 R de sa ligne — ou de son PROLONGEMENT avant son départ (la tête biseautée d'un fût, que
               le chemin ne parcourt pas : elle se dévoile d'une coupe plate juste avant lui) */
            var G0 = sgf[0], u0 = (px2 - G0.x) * G0.dx + (py2 - G0.y) * G0.dy, l0 = Math.abs((py2 - G0.y) * G0.dx - (px2 - G0.x) * G0.dy);
            var dCorps = (u0 < 0 && traits[kf].b0 === 'c') ? l0 : Math.sqrt(bf);
            if (dCorps <= ((u0 < 0 && traits[kf].b0 === 'c') ? traits[kf].R + 1.5 : 1.25 * traits[kf].R + 1)) { if (u0 < 0 && traits[kf].b0 === 'c') tf = u0; if (o2 !== kf) { own[p] = kf; Tl[p] = tf; Dl[p] = Math.sqrt(bf); faible[p] = 0; } continue; } } }   /* dans le corps du premier tracé seulement ; ailleurs, la ligne la plus proche */
        if (o2 >= 0 && !traits[o2].droit && o2 !== bk && Math.sqrt(best) > Dl[p] - 0.5) continue;   /* à distance égale, l'ordre d'avant */
        if (o2 === bk) continue;
        own[p] = bk; Tl[p] = bt; Dl[p] = Math.sqrt(best); faible[p] = 0;
      }
      for (k = 0; k < traits.length; k++) { var tn = Infinity, tx = -Infinity; for (p = 0; p < n; p++) if (own[p] === k) { if (Tl[p] < tn) tn = Tl[p]; if (Tl[p] > tx) tx = Tl[p]; } mins[k] = tn; maxs[k] = tx; }
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
    var reste = [], suiv, encore = true, garde = 0, vx, vy, q2, mt, mg2, gen = new Uint16Array(n), tr = new Int16Array(n);
    for (p = 0; p < n; p++) tr[p] = own[p];
    for (p = 0; p < n; p++) if (A[p] && own[p] === -1) reste.push(p);
    /* ⚑ v147 (Tom, C-125 : « une bosse sur les fûts ») — un pixel resté prend l'instant du TRAIT LE PLUS PROCHE parmi ses voisins servis (la
       distance à la ligne de chaque trait) : la frange du bord d'un fût suit le fût, le creux d'un embranchement suit l'arche qui en sort. Avant, il
       prenait l'instant le plus précoce de ses voisins : le creux de l'arche du « h » paraissait avec le fût (une bosse), et la frange d'un fût
       près d'une barre prenait l'instant de la barre. */
    while (reste.length && encore && garde++ < 400) {
      suiv = []; encore = false; var poses = [];
      for (i = 0; i < reste.length; i++) {
        p = reste[i]; x = p % w; y = (p - x) / w; mg2 = 65535; var kb = -1, db = Infinity; mt = -Infinity;
        for (vy = -1; vy <= 1; vy++) for (vx = -1; vx <= 1; vx++) { if (!vx && !vy) continue; var xx2 = x + vx, yy2 = y + vy; if (xx2 < 0 || yy2 < 0 || xx2 >= w || yy2 >= h) continue; q2 = yy2 * w + xx2;
          if (A[q2] && own[q2] !== -1 && gen[q2] < mg2) mg2 = gen[q2]; }
        if (mg2 === 65535) { suiv.push(p); continue; }
        for (vy = -1; vy <= 1; vy++) for (vx = -1; vx <= 1; vx++) { if (!vx && !vy) continue; var xx3 = x + vx, yy3 = y + vy; if (xx3 < 0 || yy3 < 0 || xx3 >= w || yy3 >= h) continue; q2 = yy3 * w + xx3;
          if (!(A[q2] && own[q2] !== -1 && gen[q2] === mg2) || tr[q2] < 0) continue;
          var kq = tr[q2], dq = kq === kb ? db : dSeg(x + 0.5, y + 0.5, traits[kq].pts);
          if (dq < db - 1e-6 || (kq === kb && T[q2] > mt)) { if (kq !== kb) mt = -Infinity; kb = kq; db = dq; if (T[q2] > mt) mt = T[q2]; } }
        if (kb < 0) { for (vy = -1; vy <= 1; vy++) for (vx = -1; vx <= 1; vx++) { var xx4 = x + vx, yy4 = y + vy; if (xx4 < 0 || yy4 < 0 || xx4 >= w || yy4 >= h) continue; q2 = yy4 * w + xx4; if (A[q2] && own[q2] !== -1 && gen[q2] === mg2 && T[q2] > mt) mt = T[q2]; } }
        poses.push(p, mt, mg2 + 1, kb); encore = true;
      }
      for (i = 0; i < poses.length; i += 4) { T[poses[i]] = poses[i + 1]; own[poses[i]] = -2; gen[poses[i]] = poses[i + 2]; tr[poses[i]] = poses[i + 3]; }
      reste = suiv;
    }
    for (i = 0; i < reste.length; i++) { T[reste[i]] = 0; own[reste[i]] = -2; }
    /* ⚑ v147 (C-125 : « les dents du g ») — la frange servie de proche en proche peut ALTERNER entre deux traits également proches (le creux de la
       jonction panse / queue du « g ») : une dent sur deux paraissait avec l'un, l'autre avec l'autre. Deux passes de VOTE : un pixel de frange prend
       le trait le plus représenté autour de lui, et l'instant le plus tardif de ce trait parmi ses voisins. */
    for (var vote = 0; vote < 2; vote++) {
      var nvT = new Float32Array(T), nvR = new Int16Array(tr);
      for (p = 0; p < n; p++) { if (!A[p] || own[p] !== -2) continue; x = p % w; y = (p - x) / w; var cpt = {}, bestK = -1, bestN = 0;
        for (vy = -1; vy <= 1; vy++) for (vx = -1; vx <= 1; vx++) { if (!vx && !vy) continue; var x5 = x + vx, y5 = y + vy; if (x5 < 0 || y5 < 0 || x5 >= w || y5 >= h) continue; q2 = y5 * w + x5; if (!A[q2] || tr[q2] < 0) continue; cpt[tr[q2]] = (cpt[tr[q2]] || 0) + 1; }
        for (var kv in cpt) if (cpt[kv] > bestN) { bestN = cpt[kv]; bestK = +kv; }
        if (bestK < 0 || bestK === tr[p]) continue; var tm = -Infinity;
        for (vy = -1; vy <= 1; vy++) for (vx = -1; vx <= 1; vx++) { if (!vx && !vy) continue; var x6 = x + vx, y6 = y + vy; if (x6 < 0 || y6 < 0 || x6 >= w || y6 >= h) continue; q2 = y6 * w + x6; if (A[q2] && tr[q2] === bestK && T[q2] > tm) tm = T[q2]; }
        nvR[p] = bestK; nvT[p] = tm; }
      T.set(nvT); tr.set(nvR);
    }
    /* un filtre médian (3 × 3, deux fois) sur la carte : plus une dent ni un pixel isolé à la frontière de deux traits — le front reste une marche */
    /* ⚑ v147 (Tom, C-125 : « une bosse sur les fûts ») — la médiane ne prend que les voisins DU MÊME TRAIT : près d'un embranchement, les pixels
       de l'arche du « h » (ou de la barre du « f ») prenaient l'instant, plus précoce, du fût voisin, et paraissaient avec lui — une bosse. */
    var rf = 1;
    var v9 = new Float32Array((2 * rf + 1) * (2 * rf + 1)), T2 = new Float32Array(n), tour, q, c9, a9, b9, t9;
    for (tour = 0; tour < 2; tour++) {
      for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
        p = y * w + x; if (!A[p]) { T2[p] = T[p]; continue; }
        c9 = 0;
        var op = tr[p];
        for (b9 = -rf; b9 <= rf; b9++) { var yy = y + b9; if (yy < 0 || yy >= h) continue; for (a9 = -rf; a9 <= rf; a9++) { var xx = x + a9; if (xx < 0 || xx >= w) continue; q = yy * w + xx; if (A[q] && (op < 0 || tr[q] === op || tr[q] < 0)) v9[c9++] = T[q]; } }
        for (a9 = 1; a9 < c9; a9++) { t9 = v9[a9]; b9 = a9 - 1; while (b9 >= 0 && v9[b9] > t9) { v9[b9 + 1] = v9[b9]; b9--; } v9[b9 + 1] = t9; }
        T2[p] = c9 >= 5 ? v9[(c9 - 1) >> 1] : T[p];   /* la médiane basse : au bord, une rangée ne prend pas l'instant de la suivante */
      }
      T.set(T2);
    }
    for (p = 0; p < n; p++) if (!A[p]) T[p] = 0;
    if (TL._debug) TL._derniere = { T: T, own: own, w: w, h: h, dep: dep, mins: mins, maxs: maxs, droits: traits.map(function (t) { return t.droit; }), coins: coins, bouts: traits.map(function (t) { var P = t.pts; return [P[0], P[1], P[P.length - 2], P[P.length - 1], t.R]; }) };
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
    var o = options || {}, cps = (o.cps || TL.defauts.cps) * (o.vitesse || TL.defauts.vitesse),   /* v153 : l'app ne passe plus `cps` — la vitesse décidée vit ici (22, ou `?cps=`) */ esp = o.espace == null ? TL.defauts.espace : o.espace;
    if (cible.__trace) cible.__trace.stop();
    var ctl = { glyphes: [], duree: 0, canevas: null, fini: false }, resFin, resPret, raf = 0, mort = false;
    ctl.fin = new Promise(function (r) { resFin = r; }); ctl.pret = new Promise(function (r) { resPret = r; });
    cible.__trace = ctl;
    if (contenu != null) remplit(cible, contenu);
    var cv = null, G = [], L = [], total = 0, t0 = 0, ig = 0, jd = 0, tPrec = -1, clipAvant = null, tAbs = 0, tPlume = 0;
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
      if (!o.manuel) { try { demande(G[0]); } catch (e) { } /* la première lettre est demandée AVANT que l'horloge parte ; la plume l'attend */ t0 = racine.performance.now(); tAbs = 0; tPlume = 0; raf = racine.requestAnimationFrame(image); }
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

    /* ⚑ v147 — LA CARTE D'UNE LETTRE SE CALCULE HORS DU FIL PRINCIPAL. Mesuré au banc (27 pt ×3, la phrase du Studio) : une carte coûtait 9 à 204 ms
       (WebKit), calculée au moment où le front atteignait la lettre — une image de 143 à 194 ms par lettre dans le guide. Le fil principal ne fait plus
       que DESSINER la lettre (le texte réel, puis à 2× pour la carte : 1 à 2 ms) ; la carte part à un Worker (`ouvrier`), qui la rend ; la plume
       attend sa lettre si elle n'est pas prête (elle marque un temps, l'image n'est jamais bloquée). Une carte déjà faite (même lettre, taille,
       couleur, décalage sous le pixel) est reprise du cache. Sans Worker (ou en mode `manuel`, les juges), le calcul reste sur place. */
    function cleDe(g) { return g.spec + '|' + g.car + '|' + g.coul + '|' + s.toFixed(3) + '|' + g.w + 'x' + g.h + '|' + Math.round(((g.gx - g.X0) % 1) * 4) + ',' + Math.round(((g.gy - g.Y0) % 1) * 4); }
    function depuisCache(g) { var C0 = TL._cache[cleDe(g)]; if (!C0) return false;
      g.im = new ImageData(new Uint8ClampedArray(C0.im), g.w, g.h); g.A = C0.A; g.T = C0.T; g.T1 = C0.T1; g.sup = C0.sup; g.D = C0.D; g.pret = true; g.attente = false; TL.mesures.cache++; return true; }
    function rendGlyphe(g) {
      /* le glyphe réel, rendu une fois (son image à 1×, son encre à `sup`×) ; les chemins de ses traits, à la même échelle */
      bctx.setTransform(1, 0, 0, 1, 0, 0); bctx.clearRect(0, 0, g.w, g.h);
      bctx.setTransform(s, 0, 0, s, g.gx - g.X0, g.gy - g.Y0); bctx.font = g.spec; bctx.fillStyle = g.coul; bctx.textBaseline = 'alphabetic'; bctx.fillText(g.car, 0, 0);
      bctx.setTransform(1, 0, 0, 1, 0, 0);
      var im = bctx.getImageData(0, 0, g.w, g.h), d = im.data, n = g.w * g.h, A = new Uint8ClampedArray(n), p;
      for (p = 0; p < n; p++) A[p] = d[4 * p + 3];
      /* ⚑ v147 (Tom, C-125 : « dents du g, fente au départ du é, barres du t et du f, bosse sur les fûts ») — LA CARTE DE TEMPS SE CALCULE EN
         SURÉCHANTILLONNÉ (×2 au plus, `TL.supMax` : à ×4 une lettre coûtait 48 ms en médiane, 204 au pire). Chaque pixel de l'appareil garde
         l'instant de son premier et de son dernier sous-pixel d'encre : le front le traverse en anticrénelage. */
      var traits, moves = [], u = g.sc * s, ox = g.gx - g.X0, oy = g.gy - g.Y0, Rmax = 0;
      if (g.pc) g.pc.traits.forEach(function (t) { Rmax = Math.max(Rmax, t.R * u); });
      var sup = g.pc ? Math.max(1, Math.min(TL.supMax || 2, Math.ceil((TL.supDemi || 16) / Math.max(1, Rmax)))) : 1, W2 = g.w * sup, H2 = g.h * sup, A2 = A;
      if (sup > 1) {
        if (!TL._sur) { TL._sur = doc.createElement('canvas'); TL._surCtx = TL._sur.getContext('2d', { willReadFrequently: true }); }
        var sc2 = TL._sur, x2 = TL._surCtx; if (sc2.width < W2) sc2.width = W2; if (sc2.height < H2) sc2.height = H2;
        x2.setTransform(1, 0, 0, 1, 0, 0); x2.clearRect(0, 0, W2, H2);
        x2.setTransform(s * sup, 0, 0, s * sup, (g.gx - g.X0) * sup, (g.gy - g.Y0) * sup); x2.font = g.spec; x2.fillStyle = '#000'; x2.textBaseline = 'alphabetic'; x2.fillText(g.car, 0, 0);
        x2.setTransform(1, 0, 0, 1, 0, 0);
        var d2 = x2.getImageData(0, 0, W2, H2).data; A2 = new Uint8ClampedArray(W2 * H2); for (p = 0; p < W2 * H2; p++) A2[p] = d2[4 * p + 3];
      }
      if (g.pc) {
        traits = g.pc.traits.map(function (t) { return { R: Math.max(t.R * u * sup, 0.75), b0: t.b0, b1: t.b1, pts: t.pts.map(function (q) { return [(ox + q[0] * u) * sup, (oy - q[1] * u) * sup]; }) }; });
        var acc = 0; g.pc.ordre.forEach(function (st) { if (st[0] === 'r') acc += st[1] * u * sup; else if (st[0] === 't') { moves.push(acc); acc = 0; } });
      } else { traits = [{ R: g.h, pts: [[1, g.h / 2], [g.w - 1, g.h / 2]] }]; moves = [0]; }
      return { im: im, A: A, A2: A2, W2: W2, H2: H2, sup: sup, traits: traits, moves: moves, cle: cleDe(g) };
    }
    function finit(g, R, T, D) {
      var n = g.w * g.h, T0 = new Float32Array(n), T1 = new Float32Array(n), A = R.A, A2 = R.A2, W2 = R.W2, sup = R.sup, p;
      if (sup === 1) { T0.set(T); T1.set(T); }
      else {
        var xx, yy, a2, b2, mn, mx, qq;
        for (yy = 0; yy < g.h; yy++) for (xx = 0; xx < g.w; xx++) { p = yy * g.w + xx; if (!A[p]) continue; mn = Infinity; mx = -Infinity;
          for (b2 = 0; b2 < sup; b2++) for (a2 = 0; a2 < sup; a2++) { qq = (yy * sup + b2) * W2 + xx * sup + a2; if (A2[qq]) { var tv = T[qq]; if (tv < mn) mn = tv; if (tv > mx) mx = tv; } }
          if (mn === Infinity) { mn = mx = D; } T0[p] = mn; T1[p] = mx; }
      }
      /* ⚑ v153 (C-125) — UN PIXEL NE SE TEINT PAS APRÈS TOUS SES VOISINS : un pixel de bord dont l'instant dépasse celui de tous ses voisins d'encre
         (une frange servie par un trait plus tardif) paraissait seul, plus tard, un point qui s'allume loin du front. Il prend l'instant de ses voisins. */
      (function () { var w = g.w, hh = g.h, xx, yy, q, M; var T0b = new Float32Array(T0);
        for (yy = 0; yy < hh; yy++) for (xx = 0; xx < w; xx++) { p = yy * w + xx; if (!A[p]) continue; M = -Infinity;
          for (var dy = -1; dy <= 1; dy++) for (var dx = -1; dx <= 1; dx++) { if (!dx && !dy) continue; var x2 = xx + dx, y2 = yy + dy; if (x2 < 0 || y2 < 0 || x2 >= w || y2 >= hh) continue; q = y2 * w + x2; if (A[q] && T0b[q] > M) M = T0b[q]; }
          if (M > -Infinity && T0b[p] > M + 2 * sup) { T0[p] = M; if (T1[p] < M) T1[p] = M; } } })();
      g.im = R.im; g.A = A; g.T = T0; g.T1 = T1; g.sup = sup; g.D = D; g.pret = true; g.attente = false;
      if (TL._cacheN > 600) { TL._cache = {}; TL._cacheN = 0; }
      TL._cache[R.cle] = { im: new Uint8ClampedArray(R.im.data), A: A, T: T0, T1: T1, sup: sup, D: D }; TL._cacheN++;
      if (TL._debug) (TL._bas = TL._bas || []).push({ car: g.car, w: g.w, h: g.h, T0: T0, T1: T1, D: D, sup: sup, A: A });
    }
    function prepare(g) {
      /* sur place (le mode manuel, ou sans Worker) */
      var d0 = racine.performance.now();
      if (depuisCache(g)) return;
      var R = rendGlyphe(g), c = carte(R.A2, R.W2, R.H2, R.traits, R.moves); finit(g, R, c.T, c.D);
      TL.mesures.prep.push(racine.performance.now() - d0); if (TL.mesures.prep.length > 4000) TL.mesures.prep.splice(0, 2000);
    }
    function demande(g) {
      /* hors du fil principal : on dessine la lettre ici, sa carte se calcule dans le Worker */
      if (g.pret || g.attente) return;
      if (depuisCache(g)) return;
      var w = o.manuel ? null : ouvrier();
      if (!w) { prepare(g); return; }
      var d0 = racine.performance.now(), R = rendGlyphe(g), id = ++TL._nId; g.attente = true;
      TL._attente[id] = function (T, D) { if (mort) return; if (!T) { g.attente = false; try { prepare(g); } catch (e) { } return; } finit(g, R, T, D); };
      try { w.postMessage({ id: id, A: R.A2, w: R.W2, h: R.H2, traits: R.traits, moves: R.moves }); } catch (e) { delete TL._attente[id]; g.attente = false; prepare(g); return; }
      TL.mesures.prep.push(racine.performance.now() - d0); if (TL.mesures.prep.length > 4000) TL.mesures.prep.splice(0, 2000);
    }
    function pose(g) {
      /* le glyphe fini, dans le canevas, en attendant que le texte réel le prenne */
      fctx.setTransform(s, 0, 0, s, g.gx, g.gy); fctx.font = g.spec; fctx.fillStyle = g.coul; fctx.textBaseline = 'alphabetic'; fctx.fillText(g.car, 0, 0); fctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(g.X0, g.Y0, g.w, g.h); ctx.drawImage(fin, g.X0, g.Y0, g.w, g.h, g.X0, g.Y0, g.w, g.h);
      g.im = g.A = g.T = g.T1 = null; g.pret = false;
    }
    function partiel(g, frac) {
      if (!g.pret) prepare(g);
      var sp = g.sup || 1, t = -0.5 * sp + frac * (g.D + sp), d = g.im.data, A = g.A, T = g.T, T1 = g.T1 || g.T, n = g.w * g.h, p, m, a;
      /* le front traverse le pixel entre l'instant de son premier et celui de son dernier sous-pixel d'encre (un pixel d'anticrénelage) */
      /* ⚑ v153 (Tom, C-125 : « aucune opacité intermédiaire hors l'anticrénelage d'un pixel ») — la rampe d'un pixel est BORNÉE à deux sous-pixels de
         chemin : un pixel dont les sous-pixels appartiennent à deux traits (une jonction) restait à demi teint tout le temps qui sépare ces deux
         traits — un point gris, loin du front. Il se teint maintenant au passage du front, en entier. */
      for (p = 0; p < n; p++) { a = A[p]; if (!a) continue; m = (t - T[p] + 0.5 * sp) / (Math.min(T1[p] - T[p], 2 * sp) + sp); d[4 * p + 3] = m <= 0 ? 0 : (m >= 1 ? a : Math.round(a * m)); }
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
        var c = Math.floor(nx.e0) - 2; if (c >= Math.ceil(dmax) + 2) { m = j; coupe = c; break; }   /* v147 (C-125) : deux pixels de marge de chaque côté — à un pixel, la colonne d'anticrénelage du fût SUIVANT paraissait avant lui (un fil sur toute sa hauteur) */
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
      if (mort) return; var d0 = racine.performance.now();
      /* le temps de la plume : il avance du temps de l'image, SAUF si la lettre où il arrive n'a pas encore sa carte — la plume marque un temps */
      var dt = tAbs ? Math.min(100, maintenant - tAbs) : 0; tAbs = maintenant;
      var t = tPlume + dt;
      for (var jx = ig; jx < G.length && G[jx].t0 < t; jx++) if (!G[jx].pret) { demande(G[jx]); if (!G[jx].pret) { t = Math.max(tPlume, G[jx].t0); break; } }
      tPlume = t;
      rend(t);
      /* ⚑ v147 — D'AVANCE : le temps qui reste dans l'image (jusqu'à 7 ms de travail) prépare les lettres qui viennent — la lettre suivante n'attend
         plus sa carte au moment où le front l'atteint (une image de 143 à 194 ms à chaque lettre, au banc, avant). */
      for (var ja = ig, na = 0; ja < G.length && na < 14 && racine.performance.now() - d0 < 6; ja++, na++) if (!G[ja].pret && !G[ja].attente) { try { demande(G[ja]); } catch (e) { } }
      TL.mesures.image.push(racine.performance.now() - d0); if (TL.mesures.image.length > 8000) TL.mesures.image.splice(0, 4000);
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
