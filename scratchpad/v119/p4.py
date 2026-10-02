# v119 §4 — le cran de nuit, couverture complète
import io
S=io.open('app.html',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:80]); S=S.replace(old,new)
# le filet de l'anneau (du +, des fiches, du trait) passe par le jeton
n=S.count("window._FILET_DOUX||'#F7F0DE'")+S.count("window._FILET_DOUX || '#F7F0DE'")
S=S.replace("window._FILET_DOUX||'#F7F0DE'","window._FILET_DOUX||window._cremeJeton()").replace("window._FILET_DOUX || '#F7F0DE'","window._FILET_DOUX||window._cremeJeton()")
assert n==7, n
rep("""  /* pour ce qui se peint en canevas : le même cran, sur une couleur donnée ([r,g,b]) — sans effet hors de la nuit */
  window._zzzTon=function(c){ return Z.cran ? cran(c) : c; };""",
"""  /* pour ce qui se peint en canevas : le même cran, sur une couleur donnée ([r,g,b]) — sans effet hors de la nuit */
  window._zzzTon=function(c){ return Z.cran ? cran(c) : c; };
  /* la crème du JETON, telle qu'elle vaut à l'instant (le filet des anneaux et du trait la prend ici, plus en dur) */
  window._cremeJeton=function(){ return Z.cran ? hex(cran([247,240,222])) : '#F7F0DE'; };

  /* ⚑ v119 (Tom) — LE CRAN DE NUIT, COUVERTURE COMPLÈTE. Bien des encres ne passent pas par les jetons : le code les pose EN LIGNE,
     en dur (`color: rgb(247, 240, 222)` sur le mot-marque et les textes d'une fiche, sur les cartes de l'Index et du Fil, les
     attributs `fill` / `stroke` des anneaux en SVG…). La nuit — et la nuit seulement — une passe les ramène à la valeur de nuit
     de LEUR jeton, et un observateur reprend ce que les peintres réécrivent ensuite ; au jour, tout est rendu. On compare avant
     d'écrire, et un nœud qu'un peintre réécrit sans cesse est lâché après vingt reprises en deux secondes (§8). */
  var PASSE={re:null, inv:null, tab:null, tabInv:null, obs:null, cpt:null};
  function tablesNuit(){ if(PASSE.tab) return; PASSE.tab={}; PASSE.tabInv={}; var J=[], N=[];
    neutres().forEach(function(k){ var a=k.de.join(', '), b=k.a.join(', '); if(PASSE.tab[a]) return; PASSE.tab[a]=b; PASSE.tabInv[b]=a; J.push(a.replace(/, /g,', ?')); N.push(b.replace(/, /g,', ?'));
      PASSE.tab[hex(k.de)]=hex(k.a); PASSE.tabInv[hex(k.a)]=hex(k.de); });
    PASSE.re=new RegExp('(rgba?\\\\()('+J.join('|')+')(?=[,)])','g'); PASSE.inv=new RegExp('(rgba?\\\\()('+N.join('|')+')(?=[,)])','g'); }
  function norme(v){ return v.replace(/,\\s*/g,', '); }
  function passeUn(e, sens){
    var re=sens?PASSE.re:PASSE.inv, T=sens?PASSE.tab:PASSE.tabInv, s=e.getAttribute('style'), n=0;
    if(s && s.indexOf('rgb')>=0){ re.lastIndex=0; var t=s.replace(re, function(m,p,v){ var q=T[norme(v)]; return q ? p+q : m; }); if(t!==s){ e.setAttribute('style', t); n++; } }
    ['fill','stroke','stop-color'].forEach(function(a){ var v=e.getAttribute(a); if(!v) return; var u=v.trim().toUpperCase(), q=T[u];
      if(!q && v.indexOf('rgb')>=0){ re.lastIndex=0; var w=v.replace(re, function(m,p,x){ var z=T[norme(x)]; return z ? p+z : m; }); if(w!==v){ e.setAttribute(a,w); n++; } return; }
      if(q){ e.setAttribute(a,q); n++; } });
    return n;
  }
  function passeTout(sens){ tablesNuit(); var fr=document.querySelector('.frame'); if(!fr) return;
    var L=fr.querySelectorAll('[style],[fill],[stroke],[stop-color]'); for(var i=0;i<L.length;i++) passeUn(L[i], sens); }
  function passeNuit(on){
    tablesNuit(); var fr=document.querySelector('.frame'); if(!fr) return;
    if(PASSE.obs){ PASSE.obs.disconnect(); PASSE.obs=null; }
    passeTout(on);
    if(!on) return;
    PASSE.cpt=new WeakMap();
    PASSE.obs=new MutationObserver(function(L){ var t=Date.now();
      for(var i=0;i<L.length;i++){ var e=L[i].target; if(L[i].type==='childList'){ var A=L[i].addedNodes; for(var j=0;j<A.length;j++){ var x=A[j]; if(x.nodeType!==1) continue; passeUn(x,true); var Q=x.querySelectorAll?x.querySelectorAll('[style],[fill],[stroke]'):[]; for(var q=0;q<Q.length;q++) passeUn(Q[q],true); } continue; }
        var c=PASSE.cpt.get(e); if(c && c.n>=20 && t-c.t<2000) continue;
        if(passeUn(e,true)){ if(!c || t-c.t>=2000) PASSE.cpt.set(e,{n:1,t:t}); else c.n++; } } });
    PASSE.obs.observe(fr, {attributes:true, attributeFilter:['style','fill','stroke'], childList:true, subtree:true});
  }""")
rep("    if(c.cran!==avant) poseCran(c.cran);", "    if(c.cran!==avant) poseCran(c.cran);\n    var _cranChange=(c.cran!==avant);")
rep("    requestAnimationFrame(function(){ requestAnimationFrame(function(){ [dv,fr].forEach(function(e){ if(e) e.classList.remove('zzz-coupe'); }); }); });\n    Z.bascules=(Z.bascules||0)+1;",
    "    if(_cranChange){ try{ passeNuit(c.cran); }catch(_){} }                /* après le repeint du thème : ce que le code a posé en ligne */\n    requestAnimationFrame(function(){ requestAnimationFrame(function(){ [dv,fr].forEach(function(e){ if(e) e.classList.remove('zzz-coupe'); }); }); });\n    Z.bascules=(Z.bascules||0)+1;")
io.open('app.html','w',encoding='utf-8').write(S); print('ok')
