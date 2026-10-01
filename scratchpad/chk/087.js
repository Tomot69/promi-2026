
(function(){
  var GLY='<svg viewBox="20 20 152 168" fill="currentColor" aria-hidden="true"><path d="M40 34 Q80 24 94 56 Q102 90 66 98 Q30 102 26 68 Q22 40 40 34Z"/><path d="M120 62 Q160 56 166 92 Q170 126 132 132 Q100 134 100 100 Q100 70 120 62Z"/><path d="M58 122 Q96 116 106 148 Q110 178 74 182 Q42 184 40 152 Q40 128 58 122Z"/></svg>';
  function poser(){ var dv=document.getElementById('device'); if(!dv||document.getElementById('accRecadre')) return;
    var r=document.createElement('div'); r.id='accRecadre'; r.className='acc-recadre'; r.setAttribute('role','button'); r.setAttribute('aria-label','recadrer'); r.innerHTML=GLY;
    r.addEventListener('click', function(ev){ ev.stopPropagation(); try{ window.Toile_recadre(); }catch(_){} });
    dv.appendChild(r); }
  window._majRecadre=function(){ var r=document.getElementById('accRecadre');
    if(!r) return;
    var ecran=!!document.querySelector('#device .screen.show, #device .sheet.show, #device .poster.show, .frame .screen.show');
    var fil=false; try{ fil=document.getElementById('feedView').classList.contains('in'); }catch(_){}
    var v=!!window._vueMain && !ecran && !fil; if(r.classList.contains('vu')!==v) r.classList.toggle('vu', v); };
  if(document.readyState!=='loading') poser(); else document.addEventListener('DOMContentLoaded', poser);
  setTimeout(poser, 400); setInterval(function(){ try{ window._majRecadre(); }catch(_){} }, 300);
})();
