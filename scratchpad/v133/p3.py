import io,re
S=io.open('app.html',encoding='utf-8').read()
i=S.index("  var PHRASES=['Eh non"); j=S.index("  var ABSENCE=14*24*3600*1000;")
new=r"""  /* ⚑ v133 (Tom, 5 oct. 2026, C-063) — LES PHRASES DES MURS, RÉÉCRITES PAR TOM : dix-huit phrases, mot pour mot, dans cet ordre, avec le
     mécanisme de rotation d'avant (compteur global, puis hasard sans répéter). Dans chaque phrase, SEULS les mots listés prennent l'orange
     de Ma Parole ! ; le point d'exclamation n'apparaît que dans « Ma Parole ! ». Chaque entrée : [la phrase, les mots en orange, dans
     l'ordre où ils paraissent]. Les espaces avant « ! » et « ? » sont insécables. */
  var N=' ';
  var TEXTES=[
    ['Eh non. Mais avec Ma Parole'+N+'!, oui.', ['Ma Parole'+N+'!']],
    ['La solution commence par Ma et finit par Parole'+N+'!', ['Ma','Parole'+N+'!']],
    ['Toujours non. Ma Parole'+N+'!, toujours oui.', ['Ma Parole'+N+'!','oui']],
    ['Je vois bien que ça te titille. Ma Parole'+N+'! aussi.', ['Ma Parole'+N+'!']],
    ['Tiens tiens, on dirait que ça commence à t’intéresser…', []],
    ['Tiens tiens. Vous ici.', []],
    ['Tu sais où trouver Ma Parole'+N+'! maintenant.', ['Ma Parole'+N+'!']],
    ['On maintient cette position officielle, alors'+N+'?', ['officielle']],
    ['Allons bon. Nous y voilà à nouveau.', []],
    ['Entre nous, le mystère s’amenuise.', ['mystère']],
    ['Les pourparlers se prolongent, je vois.', ['pourparlers']],
    ['Tu peux continuer. Je tiens le registre.', ['registre']],
    ['Ici, tout restera entre nous.', []],
    ['Je commence à soupçonner une stratégie.', ['stratégie']],
    ['On pourrait presque en faire une tradition.', ['tradition']],
    ['Regarde-nous, avec nos petites habitudes.', ['habitudes']],
    ['Dis donc, tu viendrais presque pour moi.', ['moi']],
    ['On se retrouve ici tout à l’heure'+N+'?', []]];
  var PHRASES=TEXTES.map(function(x){ return x[0]; });
"""
S=S[:i]+new+S[j:]
a=S.index("  var ACCENT={'Tu connais déjà la solution"); b=S.index("  function suivante(){ var o=lit(), now=Date.now();")
new2=r"""  var ACCENT={}; TEXTES.forEach(function(x){ ACCENT[x[0]]=x[1]; });
  window._murAccents=ACCENT;
  window._murAccentDe=function(t){ return ACCENT[t]||[]; };
  /* les mots en orange sont cherchés DANS L'ORDRE, chacun après le précédent (« Ma » puis « Parole ! » ; « Ma Parole ! » puis « oui ») */
  function peint(t){ var p=el(); p.textContent=''; var L=ACCENT[t]||[], pos=0;
    L.forEach(function(mot){ var k=t.indexOf(mot, pos); if(k<0) return; if(k>pos) p.appendChild(document.createTextNode(t.slice(pos,k)));
      var m=document.createElement('span'); m.className='mp'; m.textContent=mot; p.appendChild(m); pos=k+mot.length; });
    if(pos<t.length) p.appendChild(document.createTextNode(t.slice(pos))); }
"""
S=S[:a]+new2+S[b:]
io.open('app.html','w',encoding='utf-8').write(S)
