
(function(){
  return;   /* ⚑ Q212 (Tom) : plus d'amorce du mode signature — « un réglage qui s'active sans qu'on le sache et reste enregistré, c'est un piège » */
  try{ if(localStorage.getItem('promi_sigdemo')==='1') return; }catch(e){}
  var tries=0;
  var iv=setInterval(function(){
    tries++;
    var ov=document.getElementById('promiOnb');
    var onbGone=(!ov)||ov.classList.contains('gone')||getComputedStyle(ov).display==='none';
    var tutoGone=!document.getElementById('tutoOv');
    var bb=document.getElementById('brandBtn'), dev=document.querySelector('.device');
    if(tries>60){clearInterval(iv);return;}
    if(onbGone && tutoGone && bb && dev){
      clearInterval(iv);
      try{localStorage.setItem('promi_sigdemo','1');}catch(e){}
      setTimeout(function(){
        var pi=document.getElementById('promiI');
        bb.classList.add('sig-on'); dev.classList.add('sigmode'); if(pi)pi.classList.remove('blink');
        bb.classList.remove('pulsing'); void bb.offsetWidth; bb.classList.add('pulsing');
        setTimeout(function(){
          bb.classList.remove('sig-on'); dev.classList.remove('sigmode'); if(pi)pi.classList.add('blink');
        }, 1250);
      }, 950);
    }
  }, 220);
})();
