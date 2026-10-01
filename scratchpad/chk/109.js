
(function(){ var sc=document.getElementById('studioScreen'); if(!sc) return; var vu=sc.classList.contains('show'), t=null;
  function fin(){ sc.classList.remove('st-entre'); clearTimeout(t); }
  sc.addEventListener('transitionend', function(e){ if(e.target===sc) fin(); });
  new MutationObserver(function(){ var o=sc.classList.contains('show'); if(o===vu) return; vu=o;
    if(o){ sc.classList.add('st-entre'); clearTimeout(t); t=setTimeout(fin,700); } else fin(); })
    .observe(sc,{attributes:true,attributeFilter:['class']}); })();
