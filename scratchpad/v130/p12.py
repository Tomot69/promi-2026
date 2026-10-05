import io
S=io.open('app.html',encoding='utf-8').read()
# 1 · à la source : le poseur de la fiche
old="""      e.col=clair; e.colTexte=(light?ENCOURS:CREMEETAT); e.trace='trace pour tenir'; e.champ=true;
    }
"""
new="""      e.col=clair; e.colTexte=(light?ENCOURS:CREMEETAT); e.trace='trace pour tenir'; e.champ=true;
    }
    /* ⚑ v130 (Tom, 5 oct. 2026, C-050) — LE CORPS SOMBRE D'UN PROMI EST TROPICAL BREEZE #8ACBE8 : un fond pastel porte de l'ENCRE
       (§3 : une marque suit ce qui est peint sous elle). Posé ICI, à la source, dès la première image (Q374) : titre, à-qui,
       échéance, mention du trait, contour de la carte du mot. Une fiche tenue garde la terre, un Chiche son corps. */
    if(!light && n==='promi' && !tenu){ e.colTexte=ENCRE; e.corpsPastel=true; }
"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    var encre = e.light ? ENCRE : CREME;
    /* ⚑ v7 — LE CORPS D'UNE FICHE TENUE EST LE BRUN SURFACE"""
new="""    var encre = (e.light || e.corpsPastel) ? ENCRE : CREME;   /* v130 : sur Tropical Breeze, l'encre */
    /* ⚑ v7 — LE CORPS D'UNE FICHE TENUE EST LE BRUN SURFACE"""
assert S.count(old)==1; S=S.replace(old,new)
lot=r'''<script id="lot-V130-TROPICAL">
/* ⚑ v130 (Tom, 5 oct. 2026, C-050) — « Le texte posé sur ce corps passe à l'encre #201908 […] puisqu'un fond pastel porte de l'encre. »
   Le titre, l'à-qui, l'échéance et la mention du trait sont posés à la source (le poseur de la fiche). Le reste de ce qui vit sur le
   corps d'un Promi en sombre (noms des disques, « écris un mot », la phrase de la page +, sa consigne, les noms des pinceaux) était
   écrit pour un corps SOMBRE, par une dizaine de règles. UN SEUL PROPRIÉTAIRE ICI : tout texte dont le premier fond opaque est
   Tropical Breeze et qui n'y tient pas 4,5:1 passe à l'encre ; tout contour qui n'y tient pas 3:1 aussi. Rien d'autre n'est touché :
   ni un autre fond, ni une couleur d'état qui se lit. La passe se relit (elle rend ce qu'elle a posé avant de relire la cascade) et
   compare avant d'écrire (§8). */
(function(){
  var TROP=[138,203,232], ENCRE='#201908';
  function col3(v){ var m=String(v||'').match(/[\d.]+/g); return (m&&m.length>=3)?[+m[0],+m[1],+m[2],(m.length>3?+m[3]:1)]:null; }
  function lin(c){ c/=255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); }
  function Y(c){ return 0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]); }
  function rap(a,b){ var x=Y(a), y=Y(b); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05); }
  function fond(el){ var n=el; while(n && n.nodeType===1){ var c=col3(getComputedStyle(n).backgroundColor); if(c && c[3]>0.85) return c; n=n.parentNode; } return null; }
  function estTrop(f){ return !!f && Math.abs(f[0]-TROP[0])+Math.abs(f[1]-TROP[1])+Math.abs(f[2]-TROP[2])<6; }
  function rend(el){
    if(el.getAttribute('data-trop')!=null){ var c=col3(el.style.getPropertyValue('color'));
      if(c && c[0]===32 && c[1]===25 && c[2]===8){ el.style.removeProperty('color'); el.style.removeProperty('-webkit-text-fill-color'); }
      el.removeAttribute('data-trop'); }
    if(el.getAttribute('data-tropb')!=null){ el.style.removeProperty('border-color'); el.removeAttribute('data-tropb'); } }
  function passe(){
    var d=document.getElementById('device'); if(!d) return 0;
    var sombre=!d.classList.contains('light'), pris=0;
    ['detailPoster','createSheet'].forEach(function(id){
      var r=document.getElementById(id); if(!r) return;
      var ouvert=r.classList.contains('show');
      if(!sombre || !ouvert){ [].forEach.call(r.querySelectorAll('[data-trop],[data-tropb]'), rend); return; }
      if(!estTrop(fond(r)) && !r.querySelector('[data-trop],[data-tropb]') && id==='detailPoster') return;
      [].forEach.call(r.querySelectorAll('*'), function(el){
        var tag=el.tagName; if(tag==='CANVAS'||tag==='SVG'||tag==='svg'||tag==='SCRIPT'||tag==='STYLE') return;
        var txt=false; for(var k=el.firstChild;k;k=k.nextSibling){ if(k.nodeType===3 && k.nodeValue.trim()){ txt=true; break; } }
        var cs=getComputedStyle(el), bw=parseFloat(cs.borderTopWidth)||0;
        var avT=el.getAttribute('data-trop')!=null, avB=el.getAttribute('data-tropb')!=null;
        if(!txt && bw<1 && !avT && !avB) return;
        if(cs.display==='none'){ return; }
        var f=fond(txt?el:(el.parentNode||el)), ft=estTrop(f), fb=estTrop(fond(el.parentNode||el));
        if(txt||avT){
          if(avT && !(ft&&txt)){ rend(el); }
          else if(ft && txt && !avT){ var c=col3(cs.webkitTextFillColor)||col3(cs.color);
            if(c && rap(c,TROP)<4.5){ el.style.setProperty('color',ENCRE,'important'); el.style.setProperty('-webkit-text-fill-color',ENCRE,'important'); el.setAttribute('data-trop','1'); pris++; } }
          else if(ft && txt && avT){ var c2=col3(cs.webkitTextFillColor)||col3(cs.color);
            if(c2 && rap(c2,TROP)<4.5){ el.style.setProperty('color',ENCRE,'important'); el.style.setProperty('-webkit-text-fill-color',ENCRE,'important'); pris++; } }
        }
        if(bw>=1 || avB){
          if(avB && !fb){ el.style.removeProperty('border-color'); el.removeAttribute('data-tropb'); }
          else if(fb && !avB && cs.borderTopStyle!=='none'){ var b=col3(cs.borderTopColor); var bg=col3(cs.backgroundColor);
            if(b && b[3]>0.05 && rap(b,TROP)<3 && !(bg && bg[3]>0.85 && rap(b,bg)<1.05)){ el.style.setProperty('border-color',ENCRE,'important'); el.setAttribute('data-tropb','1'); pris++; } }
        }
      });
    });
    return pris; }
  window._tropical=passe;
  var prevu=false; function demande(){ if(prevu) return; prevu=true; requestAnimationFrame(function(){ prevu=false; try{ passe(); }catch(e){} }); }
  /* derrière les poseurs (on ENVELOPPE, §8) : dans la même tâche que la pose, donc avant que l'image soit peinte */
  ['_lisibiliteCorps','_phraseRendu','_fichePose'].forEach(function(nom){ var f=window[nom];
    if(typeof f==='function' && !f.__trop){ var g=function(){ var r=f.apply(this,arguments); try{ passe(); }catch(e){} return r; }; g.__trop=true; for(var k in f){ try{ g[k]=f[k]; }catch(e){} } window[nom]=g; } });
  function arme(){ ['detailPoster','createSheet','device'].forEach(function(id){ var n=document.getElementById(id); if(!n) return;
      try{ new MutationObserver(demande).observe(n, id==='device'?{attributes:true,attributeFilter:['class']}:{attributes:true,attributeFilter:['class','style','data-kind'],childList:true,subtree:true}); }catch(e){} });
    demande(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',arme); else arme();
})();
</script>
</body>'''
assert S.count("</script>\n</body>")==1
S=S.replace("</script>\n</body>", "</script>\n"+lot)
io.open('app.html','w',encoding='utf-8').write(S)
