# v118 §5 (le bouton sous l'ombre), §6 (l'écho décalé), §7 (?mesure=1)
import io
S=io.open('app.html',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:70]); S=S.replace(old,new)
# ── §5 · les cotes
rep("  K.AIR = 28;\n  K.PLI = 844;",
"""  K.AIR = 28;
  /* ⚑ v118 (Tom, Q367 tranchée) — « PARTAGER MA PELOTE » REMONTE SOUS L'OMBRE. « Le bouton se place juste sous l'ombre de la
     Pelote, à G2 = 56 du bas de l'ombre. La phrase et ce qui suit se placent ensuite, à 56 sous le bouton. L'ombre garde ses
     60 pt, l'air ne se reprend pas. » L'ombre : la cote de lot-V114-PELOTE-css (haut 453,224, haut. 16,245 → bas 469,469).
     Le bouton : 525,469 → 585,469. La phrase : son ENCRE à 56 sous le bouton (elle commence 1,671 au-dessus de sa boîte). */
  K.ombre = {y:453.224, h:16.245};
  K.G2 = 56;
  K.MOT_ENCRE = 1.671;
  K.btY = K.ombre.y + K.ombre.h + K.G2;                                  /* 525,469 */
  K.motY2 = K.btY + K.bt.h + K.G2 + K.MOT_ENCRE;                         /* 643,140 */
  K.PLI = 844;""")
rep("""    if(CAD.classList.contains('au-vide')){
      c={nx:K.nx.y, lg:K.lgY, bt:K.lgY+K.lgH+K.AIR};
      c.mo=c.bt+K.bt.h+K.AIR;
    } else {
      var nx=K.motY+MOT.offsetHeight+K.AIR_MOT, d=nx-K.nx.y;""",
"""    if(CAD.classList.contains('au-vide')){
      /* v118 : le bouton sous l'ombre ; l'invite à 56 sous le bouton (rien d'autre ne paraît sur une Aura vide) */
      c={nx:K.nx.y, lg:K.lgY, bt:K.btY, inv:K.btY+K.bt.h+K.G2};
      c.mo=c.inv;
    } else {
      var nx=K.motY2+MOT.offsetHeight+K.AIR_MOT, d=nx-K.nx.y;""")
rep("""      c.bt = c.cpt + K.cptH + K.AIR + K.cptINK;          /* le bouton, sous les chiffres : l'air À L'ENCRE est égal au-dessus du groupe « légende + chiffres » et en dessous */
      c.mo = c.bt + K.bt.h + K.AIR;                      /* puis « ce que tu as tenu » */""",
"""      c.bt = K.btY;                                      /* v118 : le bouton est sous l'ombre, il ne dépend plus de la colonne */
      c.mo = c.cpt + K.cptH + K.AIR + K.moINK;           /* « ce que tu as tenu » suit les chiffres, du même air (28) à l'encre */""")
rep("""    var k=[c.nx,c.lg,c.cpt,c.mo,c.mo2,c.bt,c.fin].map(function(v){ return v.toFixed(2); }).join('|');""",
"""    c.mot=K.motY2; if(c.inv==null) c.inv=c.bt+K.bt.h+K.G2;
    var k=[c.nx,c.lg,c.cpt,c.mo,c.mo2,c.bt,c.fin,c.mot,c.inv].map(function(v){ return v.toFixed(2); }).join('|');""")
rep("""    [[NX,c.nx],[LG,c.lg],[CPT,c.cpt],[MO,c.mo],[MO2,c.mo2],[BT,c.bt],[FIN,c.fin-1]].forEach(function(a){ if(!a[0]) return;""",
"""    [[NX,c.nx],[LG,c.lg],[CPT,c.cpt],[MO,c.mo],[MO2,c.mo2],[BT,c.bt],[FIN,c.fin-1],[MOT,c.mot],[INV,c.inv]].forEach(function(a){ if(!a[0]) return;""")
rep("  K.lgY = K.nx.y + K.nx.h + (K.mo.y - (K.nx.y + K.nx.h) - K.lgH) / 2 + K.lgINK;\n",
    "  K.lgY = K.nx.y + K.nx.h + (K.mo.y - (K.nx.y + K.nx.h) - K.lgH) / 2 + K.lgINK;\n  K.moINK = 0;   /* v118 : l'écart boîte ↔ encre du titre « Ce que tu as tenu » sous les chiffres — relevé sur l'image rendue */\n")
rep("""    else LG.setAttribute('data-centre-entre', '.au-nx|#auPartage|'+(K.lgINK-K.cptINK)+'|.au-cpt');""",
    """    else LG.setAttribute('data-centre-entre', '.au-nx|.au-mo|'+(K.lgINK-K.moINK)+'|.au-cpt');   /* v118 : le voisin du bas n'est plus le bouton (remonté sous l'ombre), c'est « Ce que tu as tenu » */""")
# ── §6 · l'écho décalé
rep("""    OMBRE=el('div','au-ombre'); OMBRE.id='auPeloteOmbre'; CAD.appendChild(OMBRE);""",
"""    /* ⚑ v118 (Tom, Q368 → A) : L'ÉCHO DÉCALÉ — une copie PLATE de la silhouette, dans un autre ton de la palette, décalée de 11 ;
       c'est la célébration, citée. Aucun flou, aucun dégradé : il reste plat. Il n'existe QUE sous la Pelote (redteam_volume). */
    ECHO=window._echoPelote(CAD, K.bo.x+K.bo.d/2, K.bo.y+K.bo.d/2, 121, 11);
    OMBRE=el('div','au-ombre'); OMBRE.id='auPeloteOmbre'; CAD.appendChild(OMBRE);""")
rep("""  function place(){
    if(!CAD) return;
    try{ reteintSiBesoin(); }catch(e){}""",
"""  function echoTeinte(){ try{ if(!ECHO) return; var P=window.Toile.cols(), c=P[(SOL_IDX+2)%P.length], v='rgb('+c[0]+','+c[1]+','+c[2]+')';
      if(ECHO.getAttribute('data-ton')!==v){ ECHO.setAttribute('data-ton',v); ECHO.style.setProperty('background-color',v,'important'); } }catch(_){} }
  function place(){
    if(!CAD) return;
    echoTeinte();
    try{ reteintSiBesoin(); }catch(e){}""")
rep("""#auraScreen.au2 .au-bo{z-index:1}
</style>""",
"""#auraScreen.au2 .au-bo{z-index:1}
/* ⚑ v118 (Tom, Q368 → A) — L'ÉCHO DÉCALÉ : un disque PLAT (aucun flou, aucun dégradé), le rayon de la silhouette (121), décalé de
   11 vers le bas et la droite, dans un autre ton de la palette (posé par le code : le ton dominant + 2). Liste blanche
   NOMINATIVE de la Pelote : `.au-echo` et `window._echoPelote` ne vivent qu'ici et dans le lot de l'Aura. */
#auraScreen.au2 .au-echo{position:absolute!important;margin:0!important;border-radius:50%!important;pointer-events:none;z-index:0;
  box-shadow:none!important;filter:none!important;opacity:1!important}
</style>
<script id="lot-V118-PELOTE">
/* ⚑ v118 — l'écho décalé de la Pelote. Un seul peintre, nommé : le poser ailleurs (une dalle, une carte) fait rougir redteam_volume. */
window._echoPelote=function(hote, cx, cy, r, dec){
  var e=document.createElement('div'); e.className='au-echo'; e.id='auPeloteEcho';
  e.style.setProperty('left',(cx+dec-r)+'px','important'); e.style.setProperty('top',(cy+dec-r)+'px','important');
  e.style.setProperty('width',(2*r)+'px','important'); e.style.setProperty('height',(2*r)+'px','important');
  hote.appendChild(e); return e;
};
</script>""")
# ── §7 · le relevé ?mesure=1 (et le diagnostic du Studio ne se lance plus que sur un NOM de monde)
rep("if(location.search.indexOf('mesure=')>=0){ var _dg=document.createElement('script'); _dg.src='diag-studio.js';",
    "if(/[?&]mesure=[a-z]/.test(location.search)){ /* v118 : ?mesure=1 est le relevé de la Pelote, pas ce diagnostic */ var _dg=document.createElement('script'); _dg.src='diag-studio.js';")
rep("""  function souffle(){
    try{ if(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return SOUFFLE.MAX*0.5; }catch(_){}""",
"""  function souffle(){
    if(MES && MES.phase===2) return 0;                 /* v118 · ?mesure=1 : la seconde moitié du relevé coupe la respiration */
    try{ if(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return SOUFFLE.MAX*0.5; }catch(_){}""")
rep("""  var SOUFFLE={MAX:0.55, MONTE:4, DESCEND:6, DEPART:0.6};""",
"""  var SOUFFLE={MAX:0.55, MONTE:4, DESCEND:6, DEPART:0.6};
  /* ⚑ v118 (Tom) — LE COÛT DE LA RESPIRATION, MESURÉ SUR L'APPAREIL : visible SEULEMENT avec `?mesure=1`. Dix secondes
     respiration active (un cycle entier), dix secondes respiration coupée : le temps PAR IMAGE (l'écart entre deux images
     peintes, au temps réel) p50 et p95, et le temps de peinture seul. Rien n'est envoyé ; on lit le cadre. Toucher le cadre relance. */
  var MES=null;
  try{ if(/[?&]mesure=1(?:&|$)/.test(location.search)) MES={phase:0, t:0, A:{dt:[],ms:[]}, B:{dt:[],ms:[]}, el:null, DUREE:10, CHAUFFE:2}; }catch(_){}
  function mesCentile(L,p){ if(!L.length) return 0; var s=L.slice().sort(function(a,b){return a-b;}); return s[Math.min(s.length-1, Math.floor(p*s.length))]; }
  function mesLigne(nom,X){ var n=X.dt.length, tot=0; for(var i=0;i<n;i++) tot+=X.dt[i];
    var f=function(v){ return (Math.round(v*10)/10).toFixed(1).replace('.',','); };
    return nom+'\\n  image  p50 '+f(mesCentile(X.dt,.5))+' ms · p95 '+f(mesCentile(X.dt,.95))+' ms · '+(n?f(1000*n/tot):'0')+' images/s\\n  peinture  p50 '+f(mesCentile(X.ms,.5))+' ms · p95 '+f(mesCentile(X.ms,.95))+' ms · '+n+' images'; }
  function mesAffiche(txt){ if(!MES) return;
    if(!MES.el){ var e=document.createElement('div'); e.id='auMesure';
      e.style.cssText='position:absolute;left:24px;right:24px;top:108px;z-index:60;padding:10px 12px;border:2px solid #201908;border-radius:14px;background:#F7F0DE;color:#201908;-webkit-text-fill-color:#201908;font:500 13px/1.35 Atkinson,system-ui,sans-serif;white-space:pre-wrap;cursor:pointer';
      e.addEventListener('click', function(ev){ ev.stopPropagation(); MES.phase=0; MES.t=0; MES.A={dt:[],ms:[]}; MES.B={dt:[],ms:[]}; PEL.souffleT=null; });
      SC.appendChild(e); MES.el=e; }
    if(MES.el.textContent!==txt) MES.el.textContent=txt; }
  function mesImage(dtR, ms){ if(!MES) return;
    if(dtR>0.5) return;                                /* une pause (onglet caché) n'est pas une image */
    MES.t+=dtR;
    if(MES.phase===0){ mesAffiche('MESURE DE LA PELOTE — ne touche à rien (≈ '+(MES.CHAUFFE+2*MES.DUREE)+' s)\\nmise en route…'); if(MES.t>=MES.CHAUFFE){ MES.phase=1; MES.t=0; PEL.souffleT=0; } return; }
    if(MES.phase===1){ MES.A.dt.push(dtR*1000); MES.A.ms.push(ms); mesAffiche('MESURE DE LA PELOTE — ne touche à rien\\nrespiration ACTIVE… '+Math.ceil(MES.DUREE-MES.t)+' s'); if(MES.t>=MES.DUREE){ MES.phase=2; MES.t=0; } return; }
    if(MES.phase===2){ MES.B.dt.push(dtR*1000); MES.B.ms.push(ms); mesAffiche('MESURE DE LA PELOTE — ne touche à rien\\nrespiration COUPÉE… '+Math.ceil(MES.DUREE-MES.t)+' s'); if(MES.t>=MES.DUREE){ MES.phase=3; MES.t=0;
        var d=mesCentile(MES.A.dt,.95)-mesCentile(MES.B.dt,.95), dp=mesCentile(MES.A.ms,.95)-mesCentile(MES.B.ms,.95), f=function(v){ return (v>=0?'+':'−')+(Math.round(Math.abs(v)*10)/10).toFixed(1).replace('.',','); };
        MES.txt='MESURE DE LA PELOTE — '+MES.DUREE+' s + '+MES.DUREE+' s · palier '+PALIERS[PEL.palier]+' poils\\n'+mesLigne('respiration ACTIVE',MES.A)+'\\n'+mesLigne('respiration COUPÉE',MES.B)+'\\nla respiration ajoute au p95 : image '+f(d)+' ms · peinture '+f(dp)+' ms\\n(toucher ce cadre relance la mesure)';
        window._peloteMesure={A:MES.A, B:MES.B, texte:MES.txt}; } return; }
    mesAffiche(MES.txt); }""")
rep("""    var ms=performance.now()-t0;
    PEL.dernier=ms; PEL.peints=(PEL.peints||0)+1;""",
"""    var ms=performance.now()-t0;
    if(MES) mesImage(dtR, ms);
    PEL.dernier=ms; PEL.peints=(PEL.peints||0)+1;""")
io.open('app.html','w',encoding='utf-8').write(S); print('ok')
