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
  window.__coquille = { mac: MAC, version: 'preuve-capacitor · v205' };
  /* la sonde : ce que voit l'app, envoyé au Mac 6 s après le chargement (les polices, l'écran, l'ouvrier du tracé) */
  window.addEventListener('load', function () { setTimeout(function () { try {
    var pol = []; document.fonts.forEach(function (f) { pol.push(f.family + ' ' + f.weight + ' ' + f.status); });
    fetch('mesure', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ quoi: 'preuve-sonde', coquille: window.__coquille.version, polices: pol,
      dpr: window.devicePixelRatio, ecran: [screen.width, screen.height, innerWidth, innerHeight], ouvrier: window.TraceLettres && window.TraceLettres.ouvrierEtat, ua: navigator.userAgent,
      capacitor: !!window.Capacitor, plateforme: window.Capacitor && window.Capacitor.getPlatform && window.Capacitor.getPlatform(), haptics: !!P().Haptics, notif: !!P().LocalNotifications }) });
  } catch (e) { } }, 6000); });
  window.addEventListener('load', function () {
    try { var N = P().LocalNotifications; if (!N || localStorage.getItem('preuve_notif')) return;
      N.requestPermissions().then(function (r) { if (r.display !== 'granted') return;
        return N.schedule({ notifications: [{ id: 1, title: 'Promi', body: 'La preuve : une notification programmée il y a une minute.', schedule: { at: new Date(Date.now() + 60000), allowWhileIdle: true } }] });
      }).then(function () { localStorage.setItem('preuve_notif', String(Date.now())); try { fetch('mesure', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ quoi: 'preuve-notif', programmee: new Date().toISOString() }) }); } catch (e) { } }).catch(function () { });
    } catch (e) { }
  });
})();
