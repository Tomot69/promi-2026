import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
# jetons
rep("--c-tropical78:#8ACBE8;--c-encre-attente:rgba(32,25,8,.72);--c-encre09:#201908;","--c-cobalt50:#273CEB;")
rep("--c-ton07:var(--c-tropical78);","--c-ton07:var(--c-cobalt50);")
L=S.split('\n'); assert L[2518].count('--p-corps-promi:#8ACBE8')==1; L[2518]=L[2518].replace('--p-corps-promi:#8ACBE8','--p-corps-promi:#273CEB'); S='\n'.join(L)
rep("--c-orange-maparole-corps:#FF7A55","--c-orange-maparole-corps:#FF7A55;--c-orange-maparole-cobalt:#FF8664")
# le poseur : plus de corps pastel
rep("""    if(!light && n==='promi' && !tenu){ e.corpsPastel=true; }""","""    /* ⚑ v131 (Tom, 5 oct. 2026) : Tropical Breeze est ÉCARTÉ (« trop proche du bleu du champ »). Le corps sombre d'un Promi est le
       cobalt #273CEB — un fond SOMBRE : le texte y redevient crème (6,30:1), comme avant v130. Plus rien ne déclare un corps pastel. */""")
# le rail du pinceau
rep("""    var encre  = (nat==='promi') ? '#201908' : corpsEncre();   /* v130 (C-050) : le corps d'un Promi est pastel dans les deux thèmes (crème, Tropical Breeze) — l'encre */""","""    var encre  = corpsEncre();   /* v131 : le corps sombre d'un Promi est le cobalt — la crème, comme avant v130 */""")
# la passe Tropical : coupée
rep("""(function(){
  var TROP=[138,203,232], ENCRE='#201908';""","""(function(){
  /* ⚑ v131 (Tom) — TROPICAL BREEZE EST ÉCARTÉ : cette passe n'a plus d'objet (aucun corps pastel en sombre). Elle est COUPÉE ; ses deux
     portes publiques restent, inertes, pour ceux qui les appellent. */
  window._tropical=function(){ return 0; }; window._tropicalSous=function(){ return false; }; if(true) return;
  var TROP=[138,203,232], ENCRE='#201908';""")
rep("""#device #detailPoster.corps-tropical input::placeholder,#device #detailPoster.corps-tropical textarea::placeholder,
#device #createSheet.corps-tropical input::placeholder,#device #createSheet.corps-tropical textarea::placeholder{color:var(--c-encre-attente)!important;-webkit-text-fill-color:var(--c-encre-attente)!important;opacity:1!important}
""","""/* v131 : Tropical Breeze écarté — la règle des textes d'attente est retirée avec lui */
""")
# la phrase des murs
rep("""#device:not(.light) #murPhrase.sur-tropical{color:var(--c-encre09);-webkit-text-fill-color:var(--c-encre09)}""","""/* ⚑ v131 (Tom) : sur le corps cobalt d'un Promi, « Ma Parole ! » est le même orange (OKLCH h 36°) éclairci jusqu'à 3:1 — #FF8664 (3,02:1 ;
   #FF7A55 n'y fait que 2,79:1). Chiche et Cercle gardent #FF7A55. */
#device:not(.light) #murPhrase.sur-corps.sur-cobalt{--orange-maparole:var(--c-orange-maparole-cobalt)}""")
rep("""      p.classList.toggle('sur-corps', !_trop && !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet'))); }catch(_){} var D=""","""      p.classList.toggle('sur-corps', !_trop && !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet')));
      /* v131 : le premier fond opaque SOUS le mur est-il le cobalt d'un Promi ? (le Peaufiner a son corps : on lit le fond, pas une classe) */
      var _cb=false, _n=mur; while(_n && _n.nodeType===1){ var _m=(getComputedStyle(_n).backgroundColor.match(/[\\d.]+/g)||[]).map(Number); if(_m.length>=3 && (_m.length<4 || _m[3]>0.85)){ _cb=(Math.abs(_m[0]-39)+Math.abs(_m[1]-60)+Math.abs(_m[2]-235)<6); break; } _n=_n.parentNode; }
      p.classList.toggle('sur-cobalt', _cb); }catch(_){} var D=""")
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('PROMI-TOKENS.json',encoding='utf-8').read()
a='''    "--c-tropical78": "#8ACBE8",\n    "--c-encre-attente": "rgba(32,25,8,.72)",\n    "--c-encre09": "#201908",'''; assert J.count(a)==1; J=J.replace(a,'''    "--c-cobalt50": "#273CEB",''')
a='''    "--c-orange-maparole-corps": "#FF7A55",'''; assert J.count(a)==1; J=J.replace(a,a+'''\n    "--c-orange-maparole-cobalt": "#FF8664",''')
a='''      "clair": "#CFE5FE",\n      "sombre": "#8ACBE8"'''; assert J.count(a)==1; J=J.replace(a,a.replace('#8ACBE8','#273CEB'))
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(J)
W=io.open('Promi+Design.swift',encoding='utf-8').read()
def rw(a,b):
    global W
    assert W.count(a)==1,a[:50]; W=W.replace(a,b)
rw("/// clair #CFE5FE · sombre #8ACBE8 (Tropical Breeze, Pantone 13-4307 TPG — Tom, 5 oct. 2026)","/// clair #CFE5FE · sombre #273CEB (cobalt électrique — Tom, 5 oct. 2026, v131 ; Tropical Breeze écarté)")
rw("s == .dark ? Color(red: 0.5412, green: 0.7961, blue: 0.9098) : Color(red: 0.8118, green: 0.8980, blue: 0.9961)","s == .dark ? Color(red: 0.1529, green: 0.2353, blue: 0.9216) : Color(red: 0.8118, green: 0.8980, blue: 0.9961)")
rw("        static let tropical78 = Color(red: 0.5412, green: 0.7961, blue: 0.9098)   // #8ACBE8","        static let cobalt50 = Color(red: 0.1529, green: 0.2353, blue: 0.9216)   // #273CEB")
rw("// #FF7A55 — les mêmes, sur les trois corps sombres de Peaufiner","// #FF7A55 — les mêmes, sur les corps sombres de Peaufiner (Chiche, Cercle)\n        static let orangeMaParoleCobalt = Color(red: 1.0000, green: 0.5255, blue: 0.3922)   // #FF8664 — les mêmes, sur le corps cobalt d'un Promi (v131)")
io.open('Promi+Design.swift','w',encoding='utf-8').write(W)
