import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("--c-cobalt50:#273CEB;--c-lilas85:#DAC3FF;","--c-cobalt50:#1A52F0;--c-lilas85:#E8DAFF;")
L=S.split('\n'); assert L[2518].count('--p-corps-promi:#273CEB')==1; L[2518]=L[2518].replace('--p-corps-promi:#273CEB','--p-corps-promi:#1A52F0'); S='\n'.join(L)
rep("--c-orange-maparole-cobalt:#FF8664","--c-orange-maparole-cobalt:#FF9F84")
# le mur lit le bleu courant, plus une valeur figée
rep("""_cb=(Math.abs(_m[0]-39)+Math.abs(_m[1]-60)+Math.abs(_m[2]-235)<6); break; }""","""var _bl=(window._bleuPromi?window._bleuPromi():[26,82,240]); _cb=(Math.abs(_m[0]-_bl[0])+Math.abs(_m[1]-_bl[1])+Math.abs(_m[2]-_bl[2])<6); break; }""")
lot=r'''<script id="lot-V133-BLEU">
/* ⚑ v133 (Tom, 6 oct. 2026, C-050) — LE BLEU DU CORPS SOMBRE D'UN PROMI, CHOISI SUR SON IPHONE. « Sur son iPhone, #273CEB tire nettement au
   violet. Défaut provisoire : #1A52F0. Ajoute ?bleu=1…5, qui pose le corps sombre Promi en direct. La valeur s'affiche en petit en bas
   de l'écran. Tom choisit sur son téléphone, puis on fige et on retire le paramètre. »
   Le défaut (2) vit dans les jetons. Avec `?bleu=`, le jeton du corps est posé en direct, et ses deux dérivés DÉCIDÉS suivent la même
   règle qu'avant, calculée par `_teinte.ajuste` (OKLCH, la clarté seule) : « Ma Parole ! » = l'orange des murs éclairci jusqu'à 3:1 sur ce
   bleu ; la phrase lilas de la page + = le lilas éclairci jusqu'à 4,5:1. Aucune teinte n'est écrite ici hors des cinq bleus candidats. */
(function(){
  var BLEUS={1:'#1560E8', 2:'#1A52F0', 3:'#2046F2', 4:'#273CEB', 5:'#0A5CF5'};
  function rgb(s){ s=String(s||'').trim(); var m=/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(s); if(m) return [parseInt(m[1],16),parseInt(m[2],16),parseInt(m[3],16)]; m=s.match(/[\d.]+/g); return (m&&m.length>=3)?[+m[0],+m[1],+m[2]]:null; }
  function hex(c){ return '#'+c.map(function(v){ v=Math.max(0,Math.min(255,Math.round(v))); return (v<16?'0':'')+v.toString(16); }).join('').toUpperCase(); }
  var R=document.documentElement;
  window._bleuPromi=function(){ return rgb(getComputedStyle(R).getPropertyValue('--c-cobalt50'))||[26,82,240]; };
  var m=/[?&]bleu=([1-5])(?:&|$)/.exec(location.search); if(!m) return;
  var n=+m[1], h=BLEUS[n], cs=getComputedStyle(R), f=rgb(h);
  var orange=rgb(cs.getPropertyValue('--c-orange-maparole')), lilas=rgb(cs.getPropertyValue('--c-mauve75'));
  R.style.setProperty('--c-cobalt50', h); R.style.setProperty('--p-corps-promi', h);
  try{ if(window._teinte && orange) R.style.setProperty('--c-orange-maparole-cobalt', hex(window._teinte.ajuste(orange, f, 3)));
       if(window._teinte && lilas) R.style.setProperty('--c-lilas85', hex(window._teinte.ajuste(lilas, f, 4.5))); }catch(_){ }
  function etiquette(){ var d=document.getElementById('device'); if(!d || document.getElementById('bleuEtiq')) return; var e=document.createElement('div'); e.id='bleuEtiq'; e.setAttribute('aria-hidden','true');
    e.textContent='bleu '+n+' · '+h;
    e.style.cssText='position:absolute;left:0;right:0;bottom:3px;z-index:999;text-align:center;font:500 10px/12px var(--f-texte);letter-spacing:.04em;pointer-events:none;margin:0;padding:0';
    e.style.color='#F7F0DE'; e.style.webkitTextFillColor='#F7F0DE'; e.style.textShadow='none'; e.style.mixBlendMode='difference'; d.appendChild(e); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', etiquette); else etiquette();
  window._bleuChoisi={n:n, hex:h};
})();
</script>
</body>'''
assert S.count("</script>\n</body>")==1; S=S.replace("</script>\n</body>","</script>\n"+lot)
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('PROMI-TOKENS.json',encoding='utf-8').read()
for a,b in (('"--c-orange-maparole-cobalt": "#FF8664"','"--c-orange-maparole-cobalt": "#FF9F84"'),('"--c-cobalt50": "#273CEB"','"--c-cobalt50": "#1A52F0"'),('"--c-lilas85": "#DAC3FF"','"--c-lilas85": "#E8DAFF"'),('      "sombre": "#273CEB"','      "sombre": "#1A52F0"')):
    assert J.count(a)==1,a; J=J.replace(a,b)
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(J)
W=io.open('Promi+Design.swift',encoding='utf-8').read()
for a,b in (("/// clair #CFE5FE · sombre #273CEB (cobalt électrique — Tom, 5 oct. 2026, v131 ; Tropical Breeze écarté)","/// clair #CFE5FE · sombre #1A52F0 (PROVISOIRE — Tom, 6 oct. 2026, v133 : à choisir sur son iPhone parmi cinq bleus)"),
            ("s == .dark ? Color(red: 0.1529, green: 0.2353, blue: 0.9216) :","s == .dark ? Color(red: 0.1020, green: 0.3216, blue: 0.9412) :"),
            ("static let cobalt50 = Color(red: 0.1529, green: 0.2353, blue: 0.9216)   // #273CEB","static let cobalt50 = Color(red: 0.1020, green: 0.3216, blue: 0.9412)   // #1A52F0 (provisoire, v133)"),
            ("static let orangeMaParoleCobalt = Color(red: 1.0000, green: 0.5255, blue: 0.3922)   // #FF8664 — les mêmes, sur le corps cobalt d'un Promi (v131)","static let orangeMaParoleCobalt = Color(red: 1.0000, green: 0.6235, blue: 0.5176)   // #FF9F84 — les mêmes, sur le corps bleu d'un Promi (v133, suit le bleu choisi)")):
    assert W.count(a)==1,a; W=W.replace(a,b)
io.open('Promi+Design.swift','w',encoding='utf-8').write(W)
