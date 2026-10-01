/* Diagnostic — ouvert seulement par app.html?chemin. Affiche en permanence, en haut de l'écran, le chemin que prend Madrure
   (GPU ou processeur), et pour chaque essai de contexte WebGL la RAISON EXACTE que donne le navigateur quand il refuse
   (événement webglcontextcreationerror). N'envoie rien, ne change aucun réglage. */
(function(){
  function essai(type,opt){ var msg=null; try{ var cv=document.createElement('canvas');
      cv.addEventListener('webglcontextcreationerror',function(e){ msg=(e&&e.statusMessage)||'(le navigateur ne donne pas de message)'; });
      var c=cv.getContext(type,opt); if(!c) return 'refusé — '+(msg||'(aucun événement d’erreur)');
      var e=c.getExtension('WEBGL_debug_renderer_info'); var r=e?c.getParameter(e.UNMASKED_RENDERER_WEBGL):'?'; var l=c.getExtension('WEBGL_lose_context'); if(l) l.loseContext(); return 'ok · '+r; }catch(x){ return 'exception : '+x; } }
  var L=[
    ['webgl2 exigeant (Madrure)', essai('webgl2',{failIfMajorPerformanceCaveat:true})],
    ['webgl2 sans exigence', essai('webgl2',{})],
    ['webgl (v1)', essai('webgl',{})],
    ['experimental-webgl', essai('experimental-webgl',{})]];
  var ctx='page '+location.protocol+'//'+location.host+(window.top!==window?' · DANS UN CADRE (iframe)':'')+' · contexte sécurisé : '+(window.isSecureContext?'oui':'non')+' · cœurs '+(navigator.hardwareConcurrency||'?');
  var b=document.createElement('div');
  b.style.cssText='position:fixed;left:6px;right:6px;top:6px;z-index:99999;background:#000;color:#fff;font:600 12px/1.35 system-ui;padding:8px 10px;border-radius:10px;border:2px solid #fff;pointer-events:none;white-space:pre-wrap;max-height:60vh;overflow:hidden';
  function maj(){ var ch=window._madChemin||'(Madrure pas encore peint — ouvre-le au Studio)';
    b.style.background=/^GPU/.test(ch)?'#063':(/^PROC/.test(ch)?'#900':'#000');
    b.textContent='MADRURE : '+ch+(window._madGLerr?'\nRaison donnée à Madrure : '+window._madGLerr:'')+'\n'+L.map(function(x){ return x[0]+' : '+x[1]; }).join('\n')+'\n'+ctx+'\n'+navigator.userAgent.replace(/^Mozilla\/5.0 /,'').slice(0,140); }
  function pose(){ if(document.body&&!b.parentNode) document.body.appendChild(b); maj(); }
  document.addEventListener('DOMContentLoaded',pose); setInterval(pose,500);
})();
