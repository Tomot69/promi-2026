# v118 §10 — le Zzz : la nuit, l'app se repose (le moteur de la règle ; le bouton du Studio attend — voir le rapport)
import io
S=io.open('app.html',encoding='utf-8').read()
F=io.open('scratchpad/v118/fuseaux.txt',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:70]); S=S.replace(old,new)
# premier lancement : thème CLAIR (remplace Q301, « le thème suit celui du téléphone »)
rep("""        /* v20 (Q301) : sans choix mémorisé, le thème suit celui du téléphone */
        if(!th){try{th=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';}catch(e){th='light';}}""",
"""        /* ⚑ v118 (Tom, le Zzz) : sans choix mémorisé, le thème est CLAIR (remplace Q301 — il ne suit plus le téléphone) */
        if(!th){ th='light'; }""")
rep("""    /* le thème du premier lancement suit celui du téléphone (Q301) */
    var th=LS.g('promi_theme');
    if(!th){ try{ th=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light'; }catch(_){ th='light'; } }""",
"""    /* ⚑ v118 (Tom, le Zzz) : le premier lancement est en CLAIR (remplace Q301) */
    var th=LS.g('promi_theme');
    if(!th){ th='light'; }""")
LOT = r"""<style id="lot-V118-ZZZ-css">
/* ⚑ v118 — le Zzz : un changement de thème se fait d'un coup, sans fondu */
#device.zzz-coupe,#device.zzz-coupe *,.frame.zzz-coupe,.frame.zzz-coupe *{transition:none!important}
</style>
<script id="lot-V118-ZZZ">
/* ⚑ v118 (Tom, 2 oct. 2026) — LE Zzz : LA NUIT, L'APP SE REPOSE. (CLAUDE.md §3.)
   · le CHOIX de thème (clair / sombre, `promi_theme`) et le Zzz (`promi_zzz`) sont deux réglages mémorisés ;
   · clair + Zzz : du coucher du soleil + 1 h au lever, l'app passe en SOMBRE DE NUIT ; au lever elle revient au clair ;
   · sombre + Zzz : le CRAN DE NUIT s'applique sur les mêmes heures ; Zzz éteint : clair ou sombre ordinaire, toujours ;
   · le soleil se CALCULE (algorithme NOAA) aux coordonnées de RÉFÉRENCE du fuseau horaire de l'appareil — aucune
     permission de localisation ; fuseau inconnu : 22 h – 7 h ;
   · un changement ne se fait JAMAIS sous les yeux : seulement à un changement d'écran ou au retour au premier plan, sans fondu ;
   · le cran de nuit : seuls les NEUTRES CLAIRS (les jetons crème et blanc — texte et surfaces) baissent de 0,06 de luminance
     OKLCH, teinte et chroma gardées. Les natures, les états, les dalles et l'amande ne bougent pas. Ni filtre, ni voile. */
(function(){
  var FUSEAUX={}; '@@F@@'.split(';').forEach(function(l){ var p=l.split(','); FUSEAUX[p[0]]=[+p[1],+p[2]]; });
  /* ⚠ LE BOUTON « Zzz » N'EST PAS POSÉ (v118) : la ligne SOMBRE / AVEC TEXTE du Studio ne reçoit pas un troisième bouton sans
     déplacer ses voisins (cotes au rapport). Tant qu'il manque, le Zzz ne s'allume pas tout seul : on ne livre pas un réglage
     qu'on ne peut pas éteindre. Quand le bouton sera posé : BOUTON_POSE = true, et le premier lancement l'aura activé. */
  var BOUTON_POSE=false, DELTA_L=-0.06, H=3600000;
  function lsG(k){ try{ return localStorage.getItem(k); }catch(_){ return null; } }
  function lsS(k,v){ try{ localStorage.setItem(k,v); }catch(_){} }
  var Z={choix:null, zzz:null, theme:null, cran:false, force:null};
  try{ var q=/[?&]zzz=([01])(?:&|$)/.exec(location.search); if(q) lsS('promi_zzz', q[1]);
       q=/[?&]nuit=([01])(?:&|$)/.exec(location.search); if(q) Z.force=(q[1]==='1'); }catch(_){}
  Z.zzz=(lsG('promi_zzz')===null) ? BOUTON_POSE : lsG('promi_zzz')==='1';

  function maintenant(){ return typeof window._zzzMaintenant==='function' ? +window._zzzMaintenant() : Date.now(); }
  function fuseau(){ if(typeof window._zzzFuseau==='string') return window._zzzFuseau;
    try{ return Intl.DateTimeFormat().resolvedOptions().timeZone||''; }catch(_){ return ''; } }
  /* NOAA — lever et coucher, en minutes UTC du jour (y, m, d) ; null si le soleil ne se lève ou ne se couche pas */
  function soleil(y,m,d,lat,lon){
    var R=Math.PI/180, a=y, b=m; if(b<=2){ a-=1; b+=12; }
    var A=Math.floor(a/100), B=2-A+Math.floor(A/4);
    var JD=Math.floor(365.25*(a+4716))+Math.floor(30.6001*(b+1))+d+B-1524.5+0.5, T=(JD-2451545)/36525;
    var L0=(280.46646+T*(36000.76983+T*0.0003032))%360, M=357.52911+T*(35999.05029-0.0001537*T), e=0.016708634-T*(0.000042037+0.0000001267*T);
    var C=Math.sin(M*R)*(1.914602-T*(0.004817+0.000014*T))+Math.sin(2*M*R)*(0.019993-0.000101*T)+Math.sin(3*M*R)*0.000289;
    var om=125.04-1934.136*T, lam=L0+C-0.00569-0.00478*Math.sin(om*R);
    var eps=23+(26+((21.448-T*(46.815+T*(0.00059-T*0.001813))))/60)/60+0.00256*Math.cos(om*R);
    var dec=Math.asin(Math.sin(eps*R)*Math.sin(lam*R)), yy=Math.tan(eps*R/2); yy*=yy;
    var eot=4*(yy*Math.sin(2*L0*R)-2*e*Math.sin(M*R)+4*e*yy*Math.sin(M*R)*Math.cos(2*L0*R)-0.5*yy*yy*Math.sin(4*L0*R)-1.25*e*e*Math.sin(2*M*R))/R;
    var ch=Math.cos(90.833*R)/(Math.cos(lat*R)*Math.cos(dec))-Math.tan(lat*R)*Math.tan(dec);
    if(!(ch>=-1 && ch<=1)) return null;
    var ha=Math.acos(ch)/R, midi=720-4*lon-eot;
    return {lever:midi-4*ha, coucher:midi+4*ha};
  }
  /* le lever et le coucher du jour LOCAL de l'instant donné, en millisecondes */
  function fenetre(ms){
    var d=new Date(ms), c=FUSEAUX[fuseau()];
    if(c){ var s=soleil(d.getFullYear(), d.getMonth()+1, d.getDate(), c[0], c[1]);
      if(s){ var b=Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()); return {lever:b+s.lever*60000, coucher:b+s.coucher*60000, source:'soleil'}; } }
    /* fuseau inconnu (ou soleil de minuit) : 22 h – 7 h, c'est-à-dire un « coucher » à 21 h */
    return {lever:new Date(d.getFullYear(),d.getMonth(),d.getDate(),7,0,0).getTime(), coucher:new Date(d.getFullYear(),d.getMonth(),d.getDate(),21,0,0).getTime(), source:'22h-7h'};
  }
  function nuit(ms){
    if(Z.force!==null) return Z.force;
    var f=fenetre(ms);
    if(ms>=f.coucher+H) return true;
    if(ms<f.lever){ var h=fenetre(ms-24*H); return ms>=h.coucher+H; }     /* avant le lever : la nuit d'hier a-t-elle commencé ? */
    return false;
  }
  function cible(){ var n=!!(Z.zzz && nuit(maintenant())); return {theme:(Z.choix==='dark'||n)?'dark':'light', cran:n}; }

  /* ── le cran de nuit : OKLCH, L − 0,06 ── */
  function versOk(r,g,b){ function l(c){ c/=255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); } r=l(r); g=l(g); b=l(b);
    var x=Math.cbrt(0.4122214708*r+0.5363325363*g+0.0514459929*b), y=Math.cbrt(0.2119034982*r+0.6806995451*g+0.1073969566*b), z=Math.cbrt(0.0883024619*r+0.2817188376*g+0.6299787005*b);
    return [0.2104542553*x+0.7936177850*y-0.0040720468*z, 1.9779984951*x-2.4285922050*y+0.4505937099*z, 0.0259040371*x+0.7827717662*y-0.8086757660*z]; }
  function deOk(L,a,b){ var x=L+0.3963377774*a+0.2158037573*b, y=L-0.1055613458*a-0.0638541728*b, z=L-0.0894841775*a-1.2914855480*b; x=x*x*x; y=y*y*y; z=z*z*z;
    function g(c){ c=c<=0.0031308?12.92*c:1.055*Math.pow(c,1/2.4)-0.055; return Math.max(0,Math.min(255,Math.round(c*255))); }
    return [g(4.0767416621*x-3.3077115913*y+0.2309699292*z), g(-1.2684380046*x+2.6097574011*y-0.3413193965*z), g(-0.0041960863*x-0.7034186147*y+1.7076147010*z)]; }
  function cran(c){ var o=versOk(c[0],c[1],c[2]); return deOk(Math.max(0,o[0]+DELTA_L), o[1], o[2]); }
  var NEUTRES=null;
  function neutres(){
    if(NEUTRES) return NEUTRES; NEUTRES=[];
    try{ var st=document.getElementById('lot-TOKENS-css'), t=st?st.textContent:'', re=/(--c-(?:creme|blanc)[\w-]*?)\s*:\s*#([0-9a-fA-F]{6})\b/g, m, vu={};
      while((m=re.exec(t))){ if(vu[m[1]]||/-rgb$/.test(m[1])) continue; vu[m[1]]=1;
        var c=[parseInt(m[2].slice(0,2),16),parseInt(m[2].slice(2,4),16),parseInt(m[2].slice(4,6),16)];
        if(versOk(c[0],c[1],c[2])[0]<0.80) continue;                     /* un neutre CLAIR */
        NEUTRES.push({n:m[1], de:c, a:cran(c)}); } }catch(_){}
    return NEUTRES;
  }
  function hex(c){ return '#'+c.map(function(v){ return (v<16?'0':'')+v.toString(16).toUpperCase(); }).join(''); }
  function poseCran(on){
    var R=document.documentElement;
    neutres().forEach(function(k){
      if(on){ R.style.setProperty(k.n, hex(k.a)); R.style.setProperty(k.n+'-rgb', k.a.join(',')); }
      else { R.style.removeProperty(k.n); R.style.removeProperty(k.n+'-rgb'); } });
    ['device'].forEach(function(i){ var e=document.getElementById(i); if(e) e.classList.toggle('zzz-nuit', !!on); });
    var fr=document.querySelector('.frame'); if(fr) fr.classList.toggle('zzz-nuit', !!on);
  }
  /* pour ce qui se peint en canevas : le même cran, sur une couleur donnée ([r,g,b]) — sans effet hors de la nuit */
  window._zzzTon=function(c){ return Z.cran ? cran(c) : c; };

  var base=null;
  function applique(c){
    if(!base || (c.theme===Z.theme && c.cran===Z.cran)) return false;
    var dv=document.getElementById('device'), fr=document.querySelector('.frame');
    [dv,fr].forEach(function(e){ if(e) e.classList.add('zzz-coupe'); });
    var avant=Z.cran; Z.cran=c.cran;
    if(c.cran!==avant) poseCran(c.cran);
    if(c.theme!==Z.theme || c.cran!==avant){ Z.theme=c.theme; try{ base(c.theme); }catch(_){} if(Z.choix) lsS('promi_theme', Z.choix); }
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ [dv,fr].forEach(function(e){ if(e) e.classList.remove('zzz-coupe'); }); }); });
    Z.bascules=(Z.bascules||0)+1;
    return true;
  }
  function evalue(){ try{ return applique(cible()); }catch(_){ return false; } }

  function branche(){
    if(typeof window.setTheme!=='function' || typeof window.closeAll!=='function') return false;
    base=window.setTheme;
    /* un CHOIX de thème (le Studio, le démarrage) : il se mémorise, et il s'applique tout de suite — c'est un geste */
    window.setTheme=function(t){ Z.choix=(t==='light')?'light':'dark'; lsS('promi_theme', Z.choix); Z.theme=null; evalue(); };
    try{ setTheme=window.setTheme; }catch(_){}
    var ca=window.closeAll;
    window.closeAll=function(){ var r=ca.apply(this, arguments); evalue(); return r; };
    try{ closeAll=window.closeAll; }catch(_){}
    /* un écran qui s'ouvre : `.show` qui se POSE sur un écran, une feuille ou une fiche (on compare avec l'état d'avant, §8) */
    try{ var fr=document.querySelector('.frame')||document.body;
      new MutationObserver(function(L){ for(var i=0;i<L.length;i++){ var e=L[i].target;
          if(e.classList && e.classList.contains('show') && !/(^|\s)show(\s|$)/.test(L[i].oldValue||'') && /(^|\s)(screen|sheet|poster)(\s|$)/.test(e.className)){ evalue(); return; } } })
        .observe(fr, {attributes:true, attributeFilter:['class'], attributeOldValue:true, subtree:true}); }catch(_){}
    document.addEventListener('visibilitychange', function(){ if(!document.hidden) evalue(); });
    window.addEventListener('pageshow', function(){ evalue(); });
    var th=lsG('promi_theme'); Z.choix=(th==='dark')?'dark':'light';
    return true;
  }
  (function essaie(n){ if(!branche() && n<100) setTimeout(function(){ essaie(n+1); }, 50); })(0);

  window._zzz={
    etat:function(){ var f=fenetre(maintenant()); return {choix:Z.choix, zzz:Z.zzz, theme:Z.theme, cran:Z.cran, nuit:nuit(maintenant()), fuseau:fuseau(), source:f.source, lever:f.lever, coucher:f.coucher, bascules:Z.bascules||0, bouton:BOUTON_POSE}; },
    regle:function(b){ Z.zzz=!!b; lsS('promi_zzz', Z.zzz?'1':'0'); Z.theme=null; evalue(); },     /* le geste sur le bouton : tout de suite */
    nuit:nuit, fenetre:fenetre, soleil:soleil, evalue:evalue, cran:cran, neutres:function(){ return neutres().map(function(k){ return {n:k.n, de:hex(k.de), a:hex(k.a)}; }); },
    fuseaux:Object.keys(FUSEAUX).length, DELTA_L:DELTA_L
  };
})();
</script>
"""
LOT=LOT.replace('@@F@@',F)
old="<style id=\"lot-V104-MURS-css\">"
assert S.count(old)==1
S=S.replace(old, LOT+old)
io.open('app.html','w',encoding='utf-8').write(S); print('ok', len(LOT))
