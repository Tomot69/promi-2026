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
    st.textContent = '.frame{padding:0!important;--fit:1!important}#device{border-radius:0!important;box-shadow:none!important}';
    (document.head || document.documentElement).appendChild(st); })();
  function barre() { try { var S = P().StatusBar, d = document.getElementById('device'); if (!S) return; S.setOverlaysWebView({ overlay: true });
    var clair = !!(d && d.classList.contains('light')); S.setStyle({ style: clair ? 'LIGHT' : 'DARK' }); } catch (e) { } }
  window.addEventListener('load', function () { barre(); try { var d = document.getElementById('device'); if (d) new MutationObserver(barre).observe(d, { attributes: true, attributeFilter: ['class'] }); } catch (e) { } });
  /* ⚑ v207 — LA NOTIFICATION, VÉRIFIABLE : à chaque lancement, 8 s après, l'app envoie au Mac la permission, les notifications en attente et celles déjà
     REMISES (le centre de notifications les garde) ; au premier lancement de cette version, une notification est programmée à 1 minute (clé neuve). */
  function envoie(o) { try { fetch('mesure', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(o) }); } catch (e) { } }
  window.addEventListener('load', function () {
    var N = P().LocalNotifications; if (!N) return;
    try { if (!localStorage.getItem('preuve_notif2')) {
      N.requestPermissions().then(function (r) { envoie({ quoi: 'preuve-notif-permission', reponse: r });
        if (r.display !== 'granted') return null;
        return N.schedule({ notifications: [{ id: 2, title: 'Promi', body: 'La preuve : une notification programmée il y a une minute.', schedule: { at: new Date(Date.now() + 60000), allowWhileIdle: true } }] }); })
      .then(function (r) { localStorage.setItem('preuve_notif2', String(Date.now())); envoie({ quoi: 'preuve-notif', programmee: r ? new Date().toISOString() : null, resultat: r }); })
      .catch(function (e) { envoie({ quoi: 'preuve-notif', erreur: String(e) }); }); } } catch (e) { }
    setTimeout(function () { Promise.all([N.checkPermissions().catch(function (e) { return String(e); }), N.getPending().catch(function (e) { return String(e); }), N.getDeliveredNotifications().catch(function (e) { return String(e); })])
      .then(function (r) { envoie({ quoi: 'preuve-notif-etat', permission: r[0], enAttente: r[1], remises: r[2], programmee: localStorage.getItem('preuve_notif2'), programmeeV1: localStorage.getItem('preuve_notif') }); }); }, 8000);
  });
})();
