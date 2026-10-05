import io
S=io.open('app.html',encoding='utf-8').read()
# 1 · la phrase des murs : « sur Tropical » se lit sur le FOND du mur (le Peaufiner d'une fiche tenue est Tropical, sa fiche est terre)
old="""    try{ var _trop=!!(mur && mur.closest && mur.closest('#detailPoster.corps-tropical, #createSheet.corps-tropical'));"""
new="""    try{ var _trop=!!(mur && window._tropicalSous && window._tropicalSous(mur));   /* le premier fond opaque SOUS le mur (le Peaufiner d'une fiche tenue est Tropical, sa fiche est terre) */"""
assert S.count(old)==1; S=S.replace(old,new)
# 2 · la passe : pas de sortie anticipée quand le Peaufiner est ouvert ; la classe suit ce que la passe a VU
old="""      var trop = sombre && ouvert && estTrop(fond(r));
      if(r.classList.contains('corps-tropical')!==trop) r.classList.toggle('corps-tropical', trop);
      if(!sombre || !ouvert){ [].forEach.call(r.querySelectorAll('[data-trop],[data-tropb]'), rend); return; }
      if(!estTrop(fond(r)) && !r.querySelector('[data-trop],[data-tropb]')) return;   /* un autre corps (terre, Chiche, Cercle) : rien à lire */"""
new="""      var peauf = r.classList.contains('s2-ouv') || r.classList.contains('pp-peauf');   /* le Peaufiner a SON corps : celui d'une fiche tenue est Tropical, la fiche est terre */
      var trop = sombre && ouvert && estTrop(fond(r)), vu=false;
      function classe(v){ if(r.classList.contains('corps-tropical')!==v) r.classList.toggle('corps-tropical', v); }
      if(!sombre || !ouvert){ classe(false); [].forEach.call(r.querySelectorAll('[data-trop],[data-tropb]'), rend); return; }
      if(!trop && !peauf && !r.querySelector('[data-trop],[data-tropb]')){ classe(false); return; }   /* un autre corps (terre, Chiche, Cercle) : rien à lire */"""
assert S.count(old)==1; S=S.replace(old,new)
old="""        var f=fond(txt?el:(el.parentNode||el)), ft=estTrop(f), fb=estTrop(fond(el.parentNode||el));"""
new="""        var f=fond(txt?el:(el.parentNode||el)), ft=estTrop(f), fb=estTrop(fond(el.parentNode||el)); if(ft||fb) vu=true;"""
assert S.count(old)==1; S=S.replace(old,new)
old="""            if(b && b[3]>0.05 && rap(b,TROP)<3 && !(bg && bg[3]>0.85 && rap(b,bg)<1.05)){ el.style.setProperty('border-color',ENCRE,'important'); el.setAttribute('data-tropb','1'); pris++; } }
        }
      });"""
new="""            if(b && b[3]>0.05 && rap(b,TROP)<3 && !(bg && bg[3]>0.85 && rap(b,bg)<1.05)){ el.style.setProperty('border-color',ENCRE,'important'); el.setAttribute('data-tropb','1'); pris++; } }
        }
      });
      classe(trop || vu);"""
assert S.count(old)==1; S=S.replace(old,new)
old="""  window._tropical=passe;"""
new="""  window._tropical=passe;
  window._tropicalSous=function(el){ var d=document.getElementById('device'); return !!d && !d.classList.contains('light') && estTrop(fond(el)); };"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
