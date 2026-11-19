/* v207 §1 — LA COQUILLE DE LA PREUVE CAPACITOR. Rien de l'app n'est modifié : ce script passe AVANT elle, en tête de page.
   ① le relevé (`?releve=1`) est allumé, comme dans Safari ; ses envois (`releve`, `mesure`, `export`) partent au serveur du Mac (MAC, ci-dessous) par le
     client http natif de Capacitor (CapacitorHttp : sans contrainte d'origine) ;
   ② `promiHaptique('tenir')` est branché sur le module Haptics (l'app garde un crochet déjà posé : `window.promiHaptique = window.promiHaptique || …`) ;
   ③ une notification locale est programmée à 1 minute au premier lancement (l'essai : app fermée, elle doit arriver). */
(function () {
  var MAC = '__MAC__';   /* remplacé par construire.sh (l'adresse du Mac, relue par ipconfig) */
  try { if (!/[?&]releve=1/.test(location.search)) history.replaceState(null, '', location.pathname + (location.search ? location.search + '&' : '?') + 'releve=1' + location.hash); } catch (e) { }
  var f0 = window.fetch;
  window.fetch = function (u, o) {
    try { var s = String(u && u.url || u); var m = /^\/?(releve|mesure|export)(\?.*)?$/.exec(s); if (m) u = MAC + '/' + m[1] + (m[2] || ''); } catch (e) { }
    return f0.call(this, u, o);
  };
  function P() { return (window.Capacitor && window.Capacitor.Plugins) || {}; }
  window.promiHaptique = function (nom) { try { if (nom === 'tenir' && P().Haptics) P().Haptics.impact({ style: 'HEAVY' }); } catch (e) { } };
  window.__coquille = { mac: MAC, version: 'preuve-capacitor · __VERSION__' };
  /* la sonde : ce que voit l'app, envoyé au Mac 6 s après le chargement (les polices, l'écran, l'ouvrier du tracé) */
  window.addEventListener('load', function () { setTimeout(function () { try {
    var pol = []; document.fonts.forEach(function (f) { pol.push(f.family + ' ' + f.weight + ' ' + f.status); });
    fetch('mesure', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ quoi: 'preuve-sonde', coquille: window.__coquille.version, polices: pol,
      dpr: window.devicePixelRatio, ecran: [screen.width, screen.height, innerWidth, innerHeight], ouvrier: window.TraceLettres && window.TraceLettres.ouvrierEtat, ua: navigator.userAgent,
      capacitor: !!window.Capacitor, plateforme: window.Capacitor && window.Capacitor.getPlatform && window.Capacitor.getPlatform(), haptics: !!P().Haptics, notif: !!P().LocalNotifications }) });
  } catch (e) { } }, 6000); });
  /* ⚑ v207 (séance du 17 nov.) — LE PLEIN ÉCRAN : la page est en `viewport-fit=cover` (construire.sh) ; la barre d'état de Capacitor se pose PAR-DESSUS la page
     (l'app est dessinée pour 390 × 844 : ses cotes laissent déjà la place de la barre d'état, 47 pt, et de l'indicateur d'accueil, 34 pt), son texte suit le thème. */
  /* ⚑ v207 — LE TÉLÉPHONE EST L'ÉCRAN : dans Safari l'app dessine un cadre de téléphone (coins de 22 pt, ombre) réduit pour tenir dans la fenêtre avec 14 pt de
     marge (`fitDevice` : ×0,933 sur 390 × 844). Dans l'app native, l'écran EST le téléphone : ni marge, ni réduction, ni coins, ni ombre — l'appareil à 0, 0,
     390 × 844 (mesuré). Posé par la coquille seule : l'app n'est pas modifiée. */
  (function () { var st = document.createElement('style'); st.id = 'coquille-plein-ecran';
    st.textContent = '.frame{padding:0!important;--fit:1!important}#device{border-radius:0!important;box-shadow:none!important}'
      /* ⚑ v209 (Tom, C-299 annulé) — DANS L'APP SEULE, l'encart du haut de chaque page descend d'un demi-millimètre (3 pt). Rien d'autre ne bouge. */
      + '#device .enh,.frame .enh,#device #accPlat,#stpHaut,.dz-plateau{translate:0 3px!important}';
    (document.head || document.documentElement).appendChild(st); })();
  function barre() { try { var S = P().StatusBar, d = document.getElementById('device'); if (!S) return; S.setOverlaysWebView({ overlay: true });
    var clair = !!(d && d.classList.contains('light')); S.setStyle({ style: clair ? 'LIGHT' : 'DARK' }); } catch (e) { } }
  window.addEventListener('load', function () { barre(); try { var d = document.getElementById('device'); if (d) new MutationObserver(barre).observe(d, { attributes: true, attributeFilter: ['class'] }); } catch (e) { } });
  /* ⚑ v207 — LA NOTIFICATION, VÉRIFIABLE : à chaque lancement, 8 s après, l'app envoie au Mac la permission, les notifications en attente et celles déjà
     REMISES (le centre de notifications les garde).
     ⚑ v209 (Tom, §4 : « le test était mal monté ») — elle n'est plus programmée au lancement (remise pendant qu'on utilisait l'app) : elle l'est QUAND L'APP PASSE
     EN ARRIÈRE-PLAN (`appStateChange`, isActive faux), 60 s après ; si l'app revient au premier plan avant, elle est annulée. Chaque étape part au Mac. */
  function envoie(o) { try { fetch('mesure', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(o) }); } catch (e) { } }
  window.addEventListener('load', function () {
    var N = P().LocalNotifications; if (!N) return;
    setTimeout(function () { Promise.all([N.checkPermissions().catch(function (e) { return String(e); }), N.getPending().catch(function (e) { return String(e); }), N.getDeliveredNotifications().catch(function (e) { return String(e); })])
      .then(function (r) { envoie({ quoi: 'preuve-notif-etat', permission: r[0], enAttente: r[1], remises: r[2], programmee: localStorage.getItem('preuve_notif3') }); }); }, 8000);
    try { N.checkPermissions().then(function (r) { if (r.display !== 'granted') N.requestPermissions().then(function (q) { envoie({ quoi: 'preuve-notif-permission', reponse: q }); }); }); } catch (e) { }
    var A = P().App; if (!A) return;
    A.addListener('appStateChange', function (st) { try {
      if (!st.isActive) {
        var quand = new Date(Date.now() + 60000);
        N.schedule({ notifications: [{ id: 3, title: 'Promi', body: 'La preuve : une minute après avoir quitté l\u2019app.', schedule: { at: quand, allowWhileIdle: true } }] })
          .then(function (r) { localStorage.setItem('preuve_notif3', quand.toISOString()); envoie({ quoi: 'preuve-notif', ev: 'programmée', pour: quand.toISOString(), resultat: r }); })
          .catch(function (e) { envoie({ quoi: 'preuve-notif', ev: 'erreur', erreur: String(e) }); });
      } else {
        N.getPending().then(function (p) { var la = (p.notifications || []).some(function (n) { return n.id === 3; });
          if (la) N.cancel({ notifications: [{ id: 3 }] }).then(function () { envoie({ quoi: 'preuve-notif', ev: 'annulée (revenue au premier plan avant la minute)' }); });
          else N.getDeliveredNotifications().then(function (d) { envoie({ quoi: 'preuve-notif', ev: 'retour', remises: d, programmeePour: localStorage.getItem('preuve_notif3') }); }); });
      } } catch (e) { envoie({ quoi: 'preuve-notif', ev: 'erreur', erreur: String(e) }); } });
  });
  /* ⚑ v209 (Tom, C-300) — LA FORME RÉELLE DE L'ÉCRAN, pour la veille : la découpe de la caméra en pt de l'écran. iOS n'a pas d'API : une table par modèle
     (l'identifiant du module Device). Les cotes sont celles des découpes publiées, au pt près (à vérifier à l'œil sur chaque appareil). Modèle inconnu : la bande
     centrale de la zone sûre du haut (40 % de la largeur) ; une zone sûre du haut de 24 pt ou moins (iPhone SE, 8…) : aucune découpe. Android : DisplayCutout
     (`getBoundingRects`) par un petit module natif — décrit, pas construit (ARCHITECTURE.md). */
  var ENCOCHE_X = { w: 209, h: 30 }, ENCOCHE_XR = { w: 230, h: 33 }, ENCOCHE_12 = { w: 210, h: 32 }, ENCOCHE_12M = { w: 226, h: 35 },
      ENCOCHE_13 = { w: 162, h: 33 }, ENCOCHE_13M = { w: 175, h: 35 }, ILE = { w: 126, h: 37, y: 11 }, ILE16P = { w: 126, h: 37, y: 14 };
  var DECOUPES = { 'iPhone10,3': ENCOCHE_X, 'iPhone10,6': ENCOCHE_X, 'iPhone11,2': ENCOCHE_X, 'iPhone11,4': ENCOCHE_X, 'iPhone11,6': ENCOCHE_X, 'iPhone12,3': ENCOCHE_X, 'iPhone12,5': ENCOCHE_X,
    'iPhone11,8': ENCOCHE_XR, 'iPhone12,1': ENCOCHE_XR,
    'iPhone13,1': ENCOCHE_12M, 'iPhone13,2': ENCOCHE_12, 'iPhone13,3': ENCOCHE_12, 'iPhone13,4': ENCOCHE_12,
    'iPhone14,4': ENCOCHE_13M, 'iPhone14,5': ENCOCHE_13, 'iPhone14,2': ENCOCHE_13, 'iPhone14,3': ENCOCHE_13, 'iPhone14,7': ENCOCHE_13, 'iPhone14,8': ENCOCHE_13, 'iPhone17,5': ENCOCHE_13,
    'iPhone15,2': ILE, 'iPhone15,3': ILE, 'iPhone15,4': ILE, 'iPhone15,5': ILE, 'iPhone16,1': ILE, 'iPhone16,2': ILE,
    'iPhone17,3': ILE, 'iPhone17,4': ILE, 'iPhone17,1': ILE16P, 'iPhone17,2': ILE16P, 'iPhone18,1': ILE16P, 'iPhone18,2': ILE16P, 'iPhone18,3': ILE, 'iPhone18,4': ILE,
    'iPhone8,4': null, 'iPhone9,1': null, 'iPhone9,3': null, 'iPhone10,1': null, 'iPhone10,4': null, 'iPhone12,8': null, 'iPhone14,6': null };
  function hautSur() { try { var p = document.createElement('div'); p.style.cssText = 'position:fixed;top:0;left:0;height:0;visibility:hidden;padding-top:env(safe-area-inset-top)';
    document.documentElement.appendChild(p); var v = parseFloat(getComputedStyle(p).paddingTop) || 0; p.remove(); return v; } catch (e) { return 0; } }
  function forme(modele) { var W = window.innerWidth, d = DECOUPES.hasOwnProperty(modele) ? DECOUPES[modele] : undefined, hs = hautSur(), O = null, src = 'table';
    if (d) O = { x: (W - d.w) / 2, y: d.y || 0, w: d.w, h: d.h };
    else if (d === undefined) { src = 'inconnu'; if (hs > 24) O = { x: W * 0.3, y: 0, w: W * 0.4, h: hs }; }
    window.__ecranForme = { modele: modele, source: src, decoupe: O, ecran: [W, window.innerHeight], hautSur: hs };
    envoie({ quoi: 'preuve-forme', forme: window.__ecranForme }); }
  window.__ecranForme = { modele: null, source: 'attente', decoupe: null };
  window.addEventListener('load', function () { try { var Dv = P().Device; if (!Dv) { forme(null); return; } Dv.getInfo().then(function (i) { forme(i.model); }, function () { forme(null); }); } catch (e) { forme(null); } });
  /* ⚑ v209 (Tom, C-297) — LE RELEVÉ DE LA JONCTION, EN DIRECT. Pendant qu'une fiche est ouverte et qu'elle défile (ou qu'un doigt est posé), à chaque image :
     le défilement, la place à l'écran de la boîte collante (#v192Colle), du trait plat (#v195Plat), de la fenêtre (#v200Fenetre), de la bande (#v187Bande), de
     l'en-tête (.enh), et les classes de la fiche ; à chaque changement de classe (tenir), les styles calculés de la chaîne. Envoyé au Mac par paquets,
     1 s après la fin du défilement (`quoi: 'c297'`). Rien n'est modifié dans l'app. */
  (function () { var IDS = ['v192Colle', 'v195Plat', 'v200Fenetre', 'v187Bande', 'tenirMaree'], buf = [], dern = 0, doigt = false, clsAv = '', envoiT = null, n = 0;
    function R(e) { if (!e) return null; var r = e.getBoundingClientRect(); return [+r.top.toFixed(2), +r.bottom.toFixed(2), +r.left.toFixed(1), +r.width.toFixed(1)]; }
    function styles(D) { var o = {}; [D].concat(IDS.map(function (i) { return document.getElementById(i); })).concat([D && D.querySelector('.enh')]).forEach(function (e) {
      if (!e) return; var c = getComputedStyle(e); o[e.id || e.className.split(' ')[0]] = { pos: c.position, top: c.top, z: c.zIndex, disp: c.display, vis: c.visibility, op: c.opacity, tf: c.transform, tr: c.translate,
        wc: c.willChange, ov: c.overflowY, ord: c.order, mt: c.marginTop, mb: c.marginBottom, h: c.height, clip: (c.clipPath || '').slice(0, 60), cont: c.contain }; }); return o; }
    function part() { if (!buf.length) return; var b = buf; buf = []; envoie({ quoi: 'c297', n: ++n, images: b }); }
    addEventListener('touchstart', function () { doigt = true; dern = performance.now(); }, { capture: true, passive: true });
    addEventListener('touchend', function () { doigt = false; dern = performance.now(); }, { capture: true, passive: true });
    function image() { requestAnimationFrame(image); var D = document.getElementById('detailPoster'); if (!D || !D.classList.contains('show')) return;
      var cls = D.className, t = performance.now();
      if (cls !== clsAv) { buf.push({ t: Math.round(t), ev: 'classes', cls: cls, styles: styles(D) }); clsAv = cls; dern = t; }
      var s = D.scrollTop; if (s !== image.s) { dern = t; image.s = s; }
      if (t - dern > 1000 && !doigt) { if (buf.length) part(); return; }
      var f = { t: +t.toFixed(1), s: +s.toFixed(2), d: doigt ? 1 : 0, enh: R(D.querySelector('.enh')) };
      IDS.forEach(function (i) { var e = document.getElementById(i); f[i] = R(e); if (e && f[i] && i !== 'tenirMaree') { var c = getComputedStyle(e); f[i].push(c.visibility === 'hidden' || c.display === 'none' ? 0 : 1); } });
      buf.push(f); if (buf.length >= 240) part(); }
    requestAnimationFrame(image); })();
  /* ⚑ v211 (C-310) — « de » / « d’ » : le relevé que l'app tient (`window.__c310` : chaque changement et sa voie — le tracé, un détracé interrompu, d'un coup et pourquoi),
     envoyé au Mac toutes les 3 s s'il y a du neuf (`quoi: 'c310'`). Rien n'est modifié dans l'app. */
  (function () { var vu = 0, n = 0; setInterval(function () { try { var J = window.__c310 || []; if (J.length > vu) { var neuf = J.slice(vu); vu = J.length; envoie({ quoi: 'c310', n: ++n, ev: neuf, reduit: matchMedia('(prefers-reduced-motion: reduce)').matches }); } else if (J.length < vu) vu = J.length; } catch (e) { } }, 3000); })();
})();
