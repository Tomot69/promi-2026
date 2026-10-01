/* Diagnostic — ouvert seulement par app.html?mesure=madrure. Mesure l'aperçu du Studio dans le navigateur de Tom et envoie
   un RÉSUMÉ CHIFFRÉ au serveur local (une adresse /diag?… que le journal du serveur garde). Aucune donnée de Promi n'est envoyée.
   Les réglages enregistrés (localStorage) sont remis tels quels à la fin. */
(function(){
  var monde=(location.search.match(/mesure=([a-z]+)/)||[])[1]||'madrure';
  var avant={}; try{ for(var i=0;i<localStorage.length;i++){ var k=localStorage.key(i); avant[k]=localStorage.getItem(k); } }catch(_){}
  function remet(){ try{ Object.keys(localStorage).forEach(function(k){ if(!(k in avant)) localStorage.removeItem(k); }); Object.keys(avant).forEach(function(k){ if(localStorage.getItem(k)!==avant[k]) localStorage.setItem(k,avant[k]); }); }catch(_){} }
  function envoie(o){ var s=JSON.stringify(o); fetch('/diag?'+encodeURIComponent(s)).catch(function(){}); var p=document.createElement('pre'); p.textContent='MESURE FAITE — fais une capture de ce cadre si l’envoi échoue.\n\n'+s.slice(0,1400); p.style.cssText='position:fixed;left:8px;right:8px;top:8px;z-index:99999;background:#fff;color:#000;font:15px/1.4 monospace;padding:12px;border:4px solid #c00;white-space:pre-wrap;max-height:70vh;overflow:auto'; document.body.appendChild(p); }
  function attend(ms){ return new Promise(function(r){ setTimeout(r,ms); }); }
  (async function(){
    var ban=document.createElement('div'); ban.textContent='Mesure de Madrure en cours — 20 s, ne touche à rien'; ban.style.cssText='position:fixed;left:8px;right:8px;top:8px;z-index:99999;background:#c00;color:#fff;font:bold 15px system-ui;padding:10px;text-align:center';
    document.addEventListener('DOMContentLoaded',function(){ document.body.appendChild(ban); }); if(document.body) document.body.appendChild(ban);
    await attend(6500);
    try{ if(window._onbTerminer) _onbTerminer(); }catch(_){}
    var sb=document.getElementById('studioBtn'); if(sb) sb.click(); await attend(1500);
    var d=[].slice.call(document.querySelectorAll('#studioBody .st3-dot')).filter(function(x){ return x.dataset.w===monde; })[0]; if(d) d.click(); await attend(800);
    var cv=document.getElementById('stBg'); var s=document.createElement('canvas'); s.width=cv.width/4|0; s.height=cv.height/4|0; var x=s.getContext('2d',{willReadFrequently:true});
    var AI=window.Toile.apercuImage, tAI=[]; window.Toile.apercuImage=function(){ var t=performance.now(); var r=AI.apply(this,arguments); tAI.push(performance.now()-t); return r; };
    var prev=null, out=[], t0=performance.now(), l=t0, gpuN=0, lastG=null, ph=[], k0=window._apPhase;
    await new Promise(function(res){ (function f(){ var t=performance.now(); x.drawImage(cv,0,0,s.width,s.height); var D=x.getImageData(0,0,s.width,s.height).data, a=0; if(prev){ for(var i=0;i<D.length;i+=4) a+=Math.abs(D[i]-prev[i])+Math.abs(D[i+1]-prev[i+1])+Math.abs(D[i+2]-prev[i+2]); a=a/(D.length/4)/3; } prev=D;
      var g=window._madGPU; if(g&&g.t!==lastG){ gpuN++; lastG=g.t; } if(window._apPhase!==k0){ ph.push(Math.round(t-t0)); k0=window._apPhase; }
      out.push([Math.round(t-l), Math.round(a*10)/10]); l=t; if(t-t0<10000) requestAnimationFrame(f); else res(); })(); });
    window.Toile.apercuImage=AI;
    var dts=out.slice(1).map(function(z){ return z[0]; }).sort(function(a,b){ return a-b; }), ai=tAI.slice().sort(function(a,b){ return a-b; });
    var gl=null; try{ var c2=document.createElement('canvas').getContext('webgl2'); var e=c2&&c2.getExtension('WEBGL_debug_renderer_info'); gl=c2?(e?c2.getParameter(e.UNMASKED_RENDERER_WEBGL):'ok'):'pas de webgl2'; }catch(_){}
    var o={ protocole:location.protocol, adresse:location.host, monde:monde, images:out.length, dtMed:dts[dts.length>>1], dtP90:dts[Math.floor(dts.length*.9)], dt25:dts.filter(function(v){return v>25;}).length, dt40:dts.filter(function(v){return v>40;}).length,
      apercuMed:+(ai[ai.length>>1]||0).toFixed(1), apercuP90:+(ai[Math.floor(ai.length*.9)]||0).toFixed(1), imagesGPU:gpuN, glErr:window._madGLerr||null, evenements:ph,
      dpr:devicePixelRatio, fen:[innerWidth,innerHeight], stBg:[cv.width,cv.height,Math.round(cv.getBoundingClientRect().width),Math.round(cv.getBoundingClientRect().height)],
      clair:document.getElementById('device').classList.contains('light'), nb:!!(window._promiNB&&window._promiNB.on), paroles:(typeof promises!=='undefined'?promises.length:null), gpu:gl, ua:navigator.userAgent.slice(0,120),
      serie:out.slice(1,260).map(function(z){ return z[0]+'/'+z[1]; }).join(' ') };
    remet(); if(ban.parentNode) ban.parentNode.removeChild(ban); envoie(o);
  })();
})();
