<script>
(function(){
var host=document.getElementById('toileCv'); if(!host)return;
var SIGNAL=[[255,214,10],[255,122,162],[0,95,115],[255,244,194]];
/* ⚑ v36 (Tom, 24 sept.) — « les filets autour des disques et sous le trait sont trop marqués, trop clairs : ça dénote ».
   Même crème que le contour des plateaux et l'anneau du bouton de tri (#F7F0DE, mesuré identique au pixel), mais à 55 % :
   un filet est une aide discrète de différenciation, pas un élément. Une seule valeur pour tous les peintres. */
window._FILET_DOUX='rgba(247,240,222,.55)';
var PALS={signal:{name:'Ingénu',cols:[[130,174,248],[255,184,210],[201,168,245],[239,227,199]]},primesautier:{name:'Primesautier',cols:[[255,214,10],[255,122,162],[0,95,115],[255,244,194]]},candide:{name:'Candide',cols:[[205,180,255],[255,200,162],[189,224,168],[255,181,200]]},gouailleur:{name:'Gouailleur',cols:[[156,74,26],[224,122,31],[233,184,36],[125,139,46]]},alangui:{name:'Alangui',cols:[[196,166,159],[125,106,138],[221,203,176],[140,151,171]]},irascible:{name:'Irascible',cols:[[255,45,26],[255,138,28],[184,15,46],[43,10,10]]},hurluberlu:{name:'Hurluberlu',cols:[[200,255,0],[123,47,247],[255,61,154],[43,20,0]]},beat:{name:'Béat',cols:[[31,79,209],[255,194,26],[255,255,255],[224,103,63]]},minaudier:{name:'Minaudier',cols:[[255,159,200],[224,17,95],[255,224,236],[181,242,255]]},chafouin:{name:'Chafouin',cols:[[169,180,31],[230,163,190],[108,70,117],[63,167,214]]},frivole:{name:'Frivole',cols:[[255,113,206],[1,205,254],[5,255,161],[255,251,150]]},cajoleur:{name:'Cajoleur',cols:[[159,230,207],[75,43,31],[255,240,212],[226,62,87]]},allegre:{name:'Allègre',cols:[[31,179,106],[126,200,255],[14,94,74],[239,251,234]]},lunatique:{name:'Lunatique',cols:[[43,196,196],[217,162,27],[194,24,91],[30,27,58]]},flegmatique:{name:'Flegmatique',cols:[[207,232,255],[111,168,220],[74,90,106],[255,179,167]]},narquois:{name:'Narquois',cols:[[255,154,90],[122,31,162],[255,232,214],[255,47,109]]},truculent:{name:'Truculent',cols:[[255,62,0],[0,229,255],[86,0,214],[246,255,0]]},petulant:{name:'Pétulant',cols:[[255,138,0],[104,0,224],[0,200,90],[255,170,200]]},fantasque:{name:'Fantasque',cols:[[0,255,140],[230,0,115],[0,64,255],[255,247,222]]},fielleux:{name:'Fielleux',cols:[[26,20,0],[90,51,0],[255,230,0],[179,143,0]]},sibyllin:{name:'Sibyllin',cols:[[10,10,31],[42,27,77],[94,44,165],[0,224,255]]},veneneux:{name:'Vénéneux',cols:[[20,0,20],[74,0,51],[255,0,122],[192,192,192]]},atrabilaire:{name:'Atrabilaire',cols:[[10,46,54],[27,111,128],[255,158,0],[242,242,242]]},taciturne:{name:'Taciturne',cols:[[11,13,79],[42,42,212],[143,140,255],[228,226,255]]}};
var palKey='signal',hueShift=0;   /* ⚑ 20 sept. (Tom) : la palette par défaut est celle de l'identité */
function rotc(c,deg){var r=c[0]/255,gg=c[1]/255,bb=c[2]/255,mx=Math.max(r,gg,bb),mn=Math.min(r,gg,bb),l=(mx+mn)/2,hh,s,d=mx-mn;if(d===0){hh=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);hh=mx===r?((gg-bb)/d+(gg<bb?6:0)):mx===gg?((bb-r)/d+2):((r-gg)/d+4);hh/=6;}hh=(hh+deg/360)%1;if(hh<0)hh+=1;function h2(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}var q=l<0.5?l*(1+s):l+s-l*s,pp=2*l-q;return [Math.round(h2(pp,q,hh+1/3)*255),Math.round(h2(pp,q,hh)*255),Math.round(h2(pp,q,hh-1/3)*255)];}
function curPAL(){var base=PALS[palKey].cols;return hueShift?base.map(function(c){return rotc(c,hueShift);}):base;}
var PAL=SIGNAL;
var GPIX=[[53,42,29],[61,50,37],[48,38,24],[68,57,44],[59,47,33]], GBRA=[[40,30,14],[48,36,23],[37,26,8],[53,41,26],[45,33,19]], GLI=[[68,57,43],[76,65,52],[63,51,37],[82,70,58],[72,61,48]];var GMOS=[[71,60,46],[80,69,54],[65,53,38],[86,75,61],[76,65,50]], GENC=[[34,25,3],[41,31,14],[33,21,1],[46,36,20],[39,28,10]];
var TON=[1.0,0.76,1.24,0.88,1.12];
/* LUMIERE sur les dalles colorees : lift de clarte en HSL -> teinte et saturation STRICTEMENT preservees.
   LITS[0]=0 -> le code couleur exact de la palette est toujours present. Aucun assombrissement. */
var LITS=[0,0.10,0.04,0.14,0.07];
function _r2h(c){var r=c[0]/255,g2=c[1]/255,b2=c[2]/255,mx=Math.max(r,g2,b2),mn=Math.min(r,g2,b2),h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);h=mx===r?((g2-b2)/d+(g2<b2?6:0)):mx===g2?((b2-r)/d+2):((r-g2)/d+4);h/=6;}return [h,s,l];}
function _h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}if(s===0){var v=l*255;return [v,v,v];}var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
var _palLit=null;
function PALL(){if(_palLit)return _palLit;var base=curPAL(),out=[];for(var i=0;i<base.length;i++){var hs=_r2h(base[i]),row=[];for(var k=0;k<LITS.length;k++){row.push(LITS[k]===0?[base[i][0],base[i][1],base[i][2]]:_h2r(hs[0],hs[1],Math.min(0.965,hs[2]+LITS[k]*(1-hs[2]))));}out.push(row);}_palLit=out;return out;}
/* OMBRE sur les dalles grises : assombrit vers le noir, eclaire vers le blanc — jamais d'ecretage. */
function _shadeG(c,tone,shade){
  var t=(tone||1)-1, sh=shade||1, o=[0,0,0];
  var clair=isLightM();
  /* En clair, les dalles vides sont une crème CHAUDE : le ton ne les assombrit
     qu'à peine (sinon elles virent au gris terne), et ce qu'il enlève, il l'enlève
     surtout au bleu — l'ombre reste chaude au lieu de devenir cendreuse. */
  if(clair){
    /* le ton module doucement — assez pour qu'on voie la mosaïque, jamais assez
       pour la ternir. Et ce qu'il enlève, il l'enlève surtout au bleu : l'ombre
       reste chaude, elle ne vire pas à la cendre. */
    var d=(t<0)?(1+t*0.30):(1+t*0.12);
    var chaud=[1.0,0.985,0.958];
    for(var i=0;i<3;i++){
      var v=c[i]*d*(1+(sh-1)*0.5);
      if(t<0)v*=chaud[i];
      o[i]=v<0?0:(v>255?255:v);
    }
    return o;
  }
  for(var i=0;i<3;i++){var v=c[i];v=(t<0)?v*(1+t*0.9):(v+(255-v)*(t*0.35));v*=sh;o[i]=v<0?0:(v>255?255:v);}
  return o;
}
var TH={pixel:{g:GPIX},braille:{g:GBRA},sillons:{g:GLI},gravure:{g:GLI},mosaique:{g:GMOS},encre:{g:GENC},eclats:{g:GMOS},terrazzo:{g:GENC},touffe:{g:GENC}};
/* ⚑ v32 — les rampes de matière des quatre mondes neufs (CONTRAT-MONDE §4 bis) : Esquille prend celle d'Encre (demande de
   Tom), Madrure aussi (ses cellules vides ne se peignent jamais : l'onde a ses trois tons de palette) ; Bobinette, un fil,
   prend celle des lignes (Sillons, Gravure) ; Ritournelle, des coulées qui remplissent, celle de Mosaïque. Toutes brunes. */
TH.esquille={g:GENC};TH.bobinette={g:GLI};TH.ritournelle={g:GMOS};TH.madrure={g:GENC};TH.halin={g:GMOS};TH.brouillamini={g:GPIX};TH.chamade={g:GENC};TH.volubilis={g:GENC};TH.guingois={g:GENC};TH.chantourne={g:GPIX};TH.mascaret={g:GENC};TH.ramage={g:GPIX};   /* v68 : le plumage « dans le ton du papier » : la rampe de Brouillamini (Q330) */    /* v66 : les flammes de fond dans les tons de la rampe — celle de Brouillamini (Q330) */    /* v63 : Chamade ne peint aucune cellule vide (sa page est à l'encre) ; la rampe n'y sert qu'au moteur */    /* v62 : la rampe dont l'écart au fond (ΔE 11,2) est le plus proche de celui de la planche (8,4) */   /* v48 : Halin, des aplats qui remplissent, comme Ritournelle */
/* ⚑ v29 (Tom, 23 sept.) — L'UNITÉ D'UN MONDE. `UK` vaut 1 sur la Toile et `k` pendant `dalleTrame(…, k)` : tout pas de
   trame s'écrit « valeur de référence × UK ». À k = 1 rien ne bouge ; à k ≠ 1 la dalle est la MÊME image, plus grande. */
var UK=1;
var theme='encre', g,W,H,DPR, seeds=[], lastChange=0, running=false, lastNuee=null, view={s:1,ox:0,oy:0}, _qT0=0;
/* ⚑ v43 (Tom, 24 sept. 2026) — LA TRANSITION D'UN MONDE. Le moteur garde LE MOMENT où une dalle arrive (ou part) et
   son lieu ; un monde le lit par `env.trans` — seulement sur la Toile vivante (`frame`), jamais dans une dalle, un export ou
   un aperçu (§1 amendé du CONTRAT-MONDE). Un monde qui anime son arrivée déclare sa durée : `RD[monde].transDur` (ms) ;
   le moteur tourne tant qu'elle court. Le numéro `n` rend la transition déterministe (tiré avec la clé de la Toile). */
var _trans=null, _transN=0, _transVive=false, PART_DUR=620;
var _REPLI={encre:1,touffe:1,mosaique:1,braille:1,pixel:1,terrazzo:1,sillons:1,gravure:1}, REPLI_DUR=700;   /* Houle et Taille-douce suivent (Tom, 27 sept. : « tous les mondes pareil ») */   /* la durée d'un repli, sur le temps (le poids avançait de 25 % par image : 0,15 s, invisible) */   /* v76 : les six mondes où une dalle qui part se replie (Tom) */
/* le poids d'une cellule repliée : 1,8 écart entre graines — sous ~1 écart, la cellule garde un îlot autour de son centre (mesuré à −45 : il en restait un) */
function _repliW(){ return -avg()*1.8; }
/* ⚑ v83 (Tom : « dans l'onboarding, c'est illisible quand il y a des dalles sous les éléments — on ne sait ni quoi lire ni où tracer ;
   écarte les dalles des éléments, en clair comme en sombre ; la Toile reste fournie sauf sous les éléments ») — `Toile.ecarte(rects)` :
   une graine VIDE (jamais une parole) dont la tache toucherait un rectangle (marge : 0,7 écart entre graines) se replie comme une
   dalle qui part (REPLI_DUR) ; le rectangle parti, elle regrandit. */
var _ecZ=null, _ecActif=false;
function _ecDans(s){ var m=avg()*0.7; for(var i=0;i<_ecZ.length;i++){ var r=_ecZ[i]; if(s.x>r.x-m&&s.x<r.x+r.w+m&&s.y>r.y-m&&s.y<r.y+r.h+m) return true; } return false; }
function _replie(s,now){ s.part=now; s.rT0=now; s.rW0=s.w; s.wt=s.wFin=_repliW(); s.wAt=0; }
/* v76 — Éclisse et Touffe ne pavent pas : ils posent des éclats, des fleurs, AUTOUR de la graine, sans lire le poids. Leur repli est
   une échelle tirée du poids : 1 dès qu'il est positif, 0 quand la cellule est repliée — elle rétrécit au départ, regrandit à l'arrivée. */
function _repliF(s){ var w=(s.w!=null?s.w:0); if(w>=0) return 1; return Math.max(0,Math.min(1,1-w/_repliW())); }
/* ⚑ v66 — LE FOND DE LA TOILE VIVANTE, un seul propriétaire : `frame()` le peint, et un monde qui « découpe » en papier (Ramage,
   Mascaret) le REPREND par `env.papier`, recalé dans son repère (la vue) — un aplat ferait des traits d'une autre teinte sur le dégradé. */
/* v92 : les deux tons du fond vif, lus aussi par le Worker de Ramage (un dégradé ne passe pas un postMessage : on lui en envoie la description) */
function _fondVifDesc(xa,ya,xb,yb){ var l=isLightM(); return {l:[xa,ya,xb,yb],a:l?'#E6D1AE':'#221702',b:l?'#D8C29A':'#150D00'}; }
function _fondVif(gg,xa,ya,xb,yb){ var bg=gg.createLinearGradient(xa,ya,xb,yb); if(isLightM()){
    /* le fond se creuse d'un ton : sans cela, les dalles vides — crème, très claires —
       se noyaient dedans, et les mondes braille/sillons/gravure ne dessinaient plus rien.
       En sombre, on ne touche à rien : c'est déjà juste. */
    }var q=_fondVifDesc(xa,ya,xb,yb); bg.addColorStop(0,q.a);bg.addColorStop(1,q.b); return bg; }

/* ⚑ v47 — OÙ LES GRAINES VONT SE POSER. Au début d'une transition, le moteur rejoue son propre écartement (`relax`, même
   formule) avec les poids FINAUX jusqu'à l'équilibre : un monde qui préfère se recomposer une fois plutôt que suivre le glissé
   (Esquille) lit ces places par `env.finale`. Calculé une fois par transition. */
var _finC=null;
function _semisFinal(){ var h=2166136261, _lc=_relaxLocal();
  /* ⚑ v54 (Bobinette) — pendant une transition locale, l'état final se calcule UNE FOIS (par transition, sur le poids d'arrivée) :
     les graines y vont (relax pose leurs cibles dessus) et la trame s'y lit — la Toile s'arrête exactement là où la trame
     l'annonçait, rien ne se rattrape après coup. */
  if(_lc){ var hl=(_trans.n*2654435761)>>>0, nz=0; for(var zl=0;zl<seeds.length;zl++){ var sl=seeds[zl]; if(sl.part!=null) continue; hl^=Math.round(((sl.wAt&&sl.wFin!=null)?sl.wFin:(sl.wt!=null?sl.wt:sl.w))*2)+(nz++)*31; hl=Math.imul(hl,16777619)>>>0; }
    if(_finC&&_finC.hl===hl) return _finC.m; }   /* la clé ignore la dalle qui part (le moteur la retire en cours de route : rien ne doit se recalculer) */
  else if(_lc){ h^=Math.round(_lc.x)*7+Math.round(_lc.y)*13; h=Math.imul(h,16777619)>>>0; } for(var z=0;z<seeds.length;z++){ var sz=seeds[z]; var tz=[Math.round(sz.x),Math.round(sz.y),Math.round(((sz.wAt&&sz.wFin!=null)?sz.wFin:(sz.wt!=null?sz.wt:sz.w))*2)]; for(var q=0;q<3;q++){ h^=(tz[q]|0); h=Math.imul(h,16777619)>>>0; } }
  if(_finC&&_finC.h===h&&_finC.len===seeds.length) return _finC.m;   /* v47 : un point fixe par semis (au pixel près), pas par transition */
  /* ⚑ v57 — en mode local, les graines éloignées partent de leur place FINALE d'avant (pas de leur place courante, qui n'est qu'à peu
     près au point fixe) : sinon toutes bougeaient d'un rien, et dans Esquille chaque promesse qui franchissait une cassure
     changeait d'éclat — la plaque se recomposait d'un coup sur tout l'écran. */
  var _fp=(_lc&&_finPrev&&theme==='esquille')?_finPrev:null;   /* Esquille seul lit la finale à chaque image au repos : ailleurs elle serait périmée */
  var S2=seeds.filter(function(s){ return s.part==null; }).map(function(s){ var w=(s.wAt&&s.wFin!=null)?s.wFin:(s.wt!=null?s.wt:s.w); var q=_fp&&_fp.get(s); return {s:s,x:q?q[0]:s.x,y:q?q[1]:s.y,w:w}; });   /* une dalle qui part ne compte plus */
  var ac=avg();
  for(var it=0;it<50;it++){ var mx=0, T=[];
    for(var i=0;i<S2.length;i++){ var a=S2[i],fx=0,fy=0; for(var j=0;j<S2.length;j++){ if(j===i)continue; var o=S2[j],dx=a.x-o.x,dy=a.y-o.y,d=Math.sqrt(dx*dx+dy*dy),wr=ac*(0.92+a.w*0.026+o.w*0.026); if(d<wr&&d>0.01){ var f=(wr-d)/d*0.16; fx+=dx*f; fy+=dy*f; } }
      var _B=_bornes(); T.push([Math.max(_B[0],Math.min(_B[1],a.x+fx)),Math.max(_B[2],Math.min(_B[3],a.y+fy))]); }
    for(i=0;i<S2.length;i++){ if(_lc&&Math.hypot(S2[i].s.x-_lc.x,S2[i].s.y-_lc.y)>_lc.r) continue; mx=Math.max(mx,Math.abs(T[i][0]-S2[i].x)+Math.abs(T[i][1]-S2[i].y)); S2[i].x=T[i][0]; S2[i].y=T[i][1]; }
    if(mx<0.05) break; }
  var m=new Map(); S2.forEach(function(q){ m.set(q.s,[q.x,q.y]); }); _finC={h:h,hl:(_lc?hl:null),len:seeds.length,m:m}; if(!_lc) _finPrev=m; return m; }
function _transPose(kind,x,y){ _trans={t0:performance.now(), kind:kind, x:x, y:y, n:++_transN}; if(_qT0 && performance.now()-_qT0<150) _qT0=0; }
/* ⚑ v60 (rythme) — LE MOMENT DE L'ARRIVÉE EST PROTÉGÉ. Les passes qui corrigent l'interface après un clic (polices, plateau,
   titres, couleurs sur fond sombre) tombaient pile pendant l'impression et l'arrivée de la dalle : par le vrai chemin, l'arrivée
   dans Pochade comptait 31 images au lieu de 42–48 (celle que Tom a validée). Pendant ce moment, elles sont reportées — de
   2 s au plus, comptées depuis la demande : un écran ouvert juste après ne reste jamais longtemps sans elles. */
window._apresMouvement=function(fn){ var t0=performance.now(); (function essaie(){ var occupe=!!window._tirageActive || (window._arriveeEnCours&&window._arriveeEnCours());
  if(occupe && performance.now()-t0<((_apVu&&_apVu.vif)?5000:2000)) setTimeout(essaie, 120); else fn(); })(); };   /* v75 : au Studio, on attend le REPOS de l'aperçu (il vient à chaque tour, entre l'arrivée et le départ) */
window._arriveeEnCours=function(){ var t=performance.now(); return !!((_trans&&t-_trans.t0<900) || (window._tPlante&&t-window._tPlante<900) || (window._tMouv&&t-window._tMouv<900) || (_apVu&&_apVu.vif&&_apVu.encore&&t-_apVu.tImg<200)); };   /* v75 : l'aperçu vivant du Studio, tant qu'il bouge */
window._trans_en_cours=function(){ var t=performance.now(); return !!(_trans&&RD[theme]&&RD[theme].transDur&&t-_trans.t0<RD[theme].transDur+300) || (t-lastChange<1200); };   /* v59 : le réchauffage des dalles attend que la Toile soit posée */
function isLightM(){if(typeof window!=='undefined'&&window._shThemeOverride!=null)return window._shThemeOverride;var d=document.getElementById('device');return d&&d.classList.contains('light');}
/* mode clair : du CRÈME, pas du gris. La Toile doit respirer, pas ternir. */
var GLIGHT=[[253,235,205],[250,243,229],[248,226,194],[254,238,212],[250,230,199]];
function grays(){return isLightM()?GLIGHT:TH[theme].g;}
function size(){
  var st=host.parentNode;
  var w=st.clientWidth, h=st.clientHeight;
  /* la Toile est cachée (on est dans le Fil) : on ne touche à RIEN.
     Sans ce garde-fou, un redimensionnement pendant le Fil — la barre d'URL du
     téléphone qui bouge au scroll, par exemple — mettait le canvas à 0x0
     et la Toile ne revenait jamais. */
  if(!w||!h)return;
  DPR=Math.min(2,window.devicePixelRatio||1);
  W=w; H=h; host.width=W*DPR; host.height=H*DPR;
  g=host.getContext('2d'); if(!seeds.length)seedGray(); kick();
}
window.Toile_resize=size;
function mk(x,y,k){return {x:x,y:y,tx:x,ty:y,gray:grays()[(Math.random()*5)|0],gc:null,ci:null,c:null,t0:0,kind:k||'gray',w:0,wt:0,tone:TON[(Math.random()*TON.length)|0],lit:0,shade:0.96+Math.random()*0.08,ang:Math.random()*Math.PI,ph:Math.random()*6.28,am:0.6+Math.random()*0.7};}
var _nAvg=null, _WT=null;   /* ⚑ v29 — pendant dalleTrame, le NOMBRE de graines de la Toile (les voisines seules sont passées au monde) */
function avg(){return Math.sqrt(W*H/Math.max(1,_nAvg||seeds.length));}
function seedGray(){seeds=[];var base=72,gc=Math.max(2,Math.round(W/base)),gr=Math.max(3,Math.round(H/base)),cw=W/gc,ch=H/gr;for(var r=0;r<gr;r++)for(var c=0;c<gc;c++){if(Math.random()<0.14)continue;seeds.push(mk(cw*(c+.5)+(Math.random()-.5)*cw*.55,ch*(r+.5)+(Math.random()-.5)*ch*.55));}var ex=Math.round(gc*gr*0.28);for(var e=0;e<ex;e++)seeds.push(mk(Math.random()*W,Math.random()*H));}
function nbU(s){var u={},l=avg()*1.6;l*=l;for(var j=0;j<seeds.length;j++){var o=seeds[j];if(o===s||o.ci==null)continue;var dx=s.x-o.x,dy=s.y-o.y;if(dx*dx+dy*dy<l)u[o.ci]=true;}return u;}
function iposNuee(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();if(!col.length)return ipos();var cx=0,cy=0;col.forEach(function(s){cx+=s.x;cy+=s.y;});cx/=col.length;cy/=col.length;var topB=H*0.17,botB=H*0.84;for(var t=0;t<40;t++){var a=Math.random()*6.28,r=(1.7+Math.random()*0.7)*ac;var x=Math.max(8,Math.min(W-8,cx+Math.cos(a)*r)),y=Math.max(8,Math.min(H-8,cy+Math.sin(a)*r));if(col.length<15&&(y<topB||y>botB))continue;var ok=true;for(var j=0;j<col.length;j++){var dx=x-col[j].x,dy=y-col[j].y;if(dx*dx+dy*dy<(ac*1.45)*(ac*1.45)){ok=false;break;}}if(ok)return {x:x,y:y};}return {x:Math.max(8,Math.min(W-8,cx+(Math.random()-.5)*ac*2)),y:Math.max(topB,Math.min(botB,cy+(Math.random()-.5)*ac*2))};}
function ipos(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();var few=col.length<15,topB=H*0.17,botB=H*0.84;function danger(x,y){if(!few)return false;if(y<topB||y>botB)return true;if(x>W*0.6&&y<H*0.2)return true;return false;}if(!col.length)return {x:W/2+(Math.random()-.5)*ac,y:H*0.5+(Math.random()-.5)*ac};var an=col[(Math.random()*col.length)|0];for(var t=0;t<12;t++){var sp=(Math.random()<0.72)?(0.95+Math.random()*0.22):(1.45+Math.random()*0.7);var a=Math.random()*6.28,r=ac*sp;var x=Math.max(8,Math.min(W-8,an.x+Math.cos(a)*r)),y=Math.max(8,Math.min(H-8,an.y+Math.sin(a)*r));if(!danger(x,y))return {x:x,y:y};}return {x:Math.max(8,Math.min(W-8,an.x+(Math.random()-.5)*ac)),y:Math.max(topB,Math.min(botB,an.y+(Math.random()-.5)*ac))};}
function cc(s){var u=nbU(s),av=[];for(var p=0;p<PAL.length;p++)if(!u[p])av.push(p);return av.length?av[(Math.random()*av.length)|0]:((Math.random()*PAL.length)|0);}
function tones(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();for(var i=0;i<col.length;i++)col[i].lit=null;for(var i=0;i<col.length;i++){var s=col[i],u={};for(var j=0;j<col.length;j++){if(j===i)continue;var o=col[j];if(o.lit==null)continue;var dx=s.x-o.x,dy=s.y-o.y;if(dx*dx+dy*dy<(ac*1.5)*(ac*1.5))u[o.lit]=true;}var pk=0;for(var t=0;t<LITS.length;t++){if(!u[t]){pk=t;break;}}s.lit=pk;}_dalleFigee();}
/* ⚑ LA COULEUR FIGÉE (Q213) — une dalle reliée à un Promi reprend SA couleur, `p.dalle`. Un Promi sans couleur
   figée la reçoit ici : PLANTÉ À L'INSTANT (`vivant`, depuis `addPromi`), il garde celle que la Toile vient de
   tirer pour lui, loin de ses voisines ; sinon (jeu de démonstration reconstruit après le démarrage, sauvegarde
   ancienne), celle de sa clé — jamais un nouveau tirage. */
function _dalleFigee(vivant){try{if(typeof promises==='undefined')return;var m={};for(var i=0;i<promises.length;i++)m[promises[i].id]=promises[i];
  for(var k=0;k<seeds.length;k++){var s=seeds[k];if(s.kind==='gray'||s.pid==null)continue;var p=m[s.pid];if(!p)continue;
    s.nat=p.chiche?1:0;   /* ⚑ v17 INGÉNU — lue par cOf seulement sous la palette par défaut */
    if(p.dalle&&p.dalle.ci!=null&&p.dalle.ci<PAL.length){if(s.ci!==p.dalle.ci){s.ci=p.dalle.ci;s.c=PAL[s.ci];s.gc=null;}s.lit=(p.dalle.lit|0)%LITS.length;s.rgb=(p.dalle.rgb&&p.dalle.rgb.length===3)?[+p.dalle.rgb[0],+p.dalle.rgb[1],+p.dalle.rgb[2]]:null;s.choisi=p.dalle.choisi?1:0;}
    else if(s.ci!=null){if(vivant){p.dalle={ci:s.ci,lit:(s.lit|0)};}else if(window._dalleDeCle){p.dalle=window._dalleDeCle(p);s.ci=p.dalle.ci;s.c=PAL[s.ci];s.gc=null;s.lit=p.dalle.lit;}}}
  /* ⚑ LA DALLE D'UNE NUÉE (Tom, 13 sept.) : sa couleur est à ELLE (`NUEDALLE[clé]`), tirée de son nom comme un Promi l'est de son titre ; le code du Cercle y passe. */
  var ND=window.NUEDALLE||(window.NUEDALLE={});
  for(var n=0;n<seeds.length;n++){var t=seeds[n];if(t.kind!=='nuee'||!t.nuee||t.ci==null)continue;t.nat=2;var d=ND[t.nuee];
    if(!(d&&d.ci!=null&&d.ci<PAL.length)){d=ND[t.nuee]=window._dalleDeCle?window._dalleDeCle({title:(typeof NUE!=='undefined'&&NUE[t.nuee])||t.nuee,who:'nuee'}):{ci:t.ci,lit:0};}
    if(t.ci!==d.ci){t.ci=d.ci;t.c=PAL[t.ci];t.gc=null;}t.lit=(d.lit|0)%LITS.length;t.rgb=(d.rgb&&d.rgb.length===3)?[+d.rgb[0],+d.rgb[1],+d.rgb[2]]:null;t.choisi=d.choisi?1:0;}
  }catch(e){}}
/* ---------- LE RECUL ----------
   Une Toile de 70 cellules avec un seul Promi, vue en entier, c'est un écran vide
   et triste. On se rapproche donc des premières dalles — puis, à CHAQUE dalle
   plantée, la vue RECULE d'un cran. Les proportions ne changent jamais : c'est le
   cadrage qui s'ouvre, à mesure que la Toile se remplit de couleur.
   Au-delà d'une dizaine de Promi, on voit la Toile entière : elle se suffit. */
var vTarget=null;
/* ⚑ v46 (Tom, 24 sept. 2026) — LE ZOOM « COMME UNE PHOTO SUR L'IPHONE ». Fluide, sans à-coup, vectoriel (la Toile se
   repeint à chaque image dans sa transformation : les contours restent nets même très zoomés). On dézoome jusqu'à voir la
   Toile ENTIÈRE (ZMIN), et à ce niveau les encarts du haut et du bas s'effacent. Le zoom PERSISTE d'une page à l'autre ; il
   ne revient au défaut qu'à la fermeture de l'app, à la création ou à la suppression d'une dalle — en douceur. Le défaut
   dépend du nombre de dalles : plus il y en a, plus la vue recule. Un double toucher y ramène.
   Au-delà des bornes la Toile résiste (élastique), au lâcher le glissé garde son élan, puis tout revient dans les bornes par
   un ressort calé sur le TEMPS (§8), jamais par image. */
var ZMIN=0.72, ZMAX=5, _inert=null, _pan=null;
function _zDef(n){ return n<20 ? Math.min(1.1, 1+(20-n)*0.005) : 1; }   /* ⚑ v47 (Tom) : « par défaut la Toile prend tout l'écran, angles compris, aucun fond autour — c'est ENSUITE qu'on zoome ou dézoome ». Jamais sous 1 ; plus zoomée quand il y a peu de dalles */
function _vueDefaut(){ window._vueMain=false; window._recadreDemande=true; _inert=null; autoView(); kick(); try{ if(window._majRecadre) window._majRecadre(); }catch(_){} }
function _borne(){ var s=Math.max(ZMIN,Math.min(ZMAX,view.s)), cx=W/2, cy=H/2, ox=view.ox, oy=view.oy;
  if(s!==view.s){ ox=cx-(cx-view.ox)*(s/view.s); oy=cy-(cy-view.oy)*(s/view.s); }
  if(s<1){ ox=(W-W*s)/2; oy=(H-H*s)/2; } else { ox=Math.max(W-W*s,Math.min(0,ox)); oy=Math.max(H-H*s,Math.min(0,oy)); }
  if(Math.abs(s-view.s)<1e-4&&Math.abs(ox-view.ox)<0.05&&Math.abs(oy-view.oy)<0.05) return null; return {s:s,ox:ox,oy:oy}; }
var _voileAv=-1;
function _voile(){ var a=Math.max(0,Math.min(1,(view.s-0.74)/(0.88-0.74))); a=Math.round(a*50)/50; if(a===_voileAv) return; _voileAv=a;
  try{ var dv=document.getElementById('device'); if(!dv) return; dv.style.setProperty('--toile-voile', String(a)); dv.classList.toggle('toile-recul', a<1); dv.classList.toggle('toile-entiere', a<0.05); }catch(_){} }
function _rub(v,lo,hi){ return v<lo ? lo-(lo-v)*0.35 : v>hi ? hi+(v-hi)*0.35 : v; }
/* le champ clair : la barre du haut (titre + bascule Toile/Fil) et le dock */
var HAUT_LIBRE=176, BAS_LIBRE=138;
function autoView(){
  /* ⚑ Q212 (Tom) : « la vue qui revient à 1 à chaque plantation » est un défaut. Une vue posée par la main n'est reprise
     que par le recadrage (le rond, ou le double toucher sur une case vide). */
  if(window._vueMain && !window._recadreDemande) return;
  window._recadreDemande=false;
  /* Zoom intelligent : on cadre les dalles COLOREES (pas toute la Toile),
     en gardant une marge et en plafonnant le zoom pour ne jamais tomber
     dans le vide ni grossir betement une seule dalle. Beaucoup de dalles
     => Toile entiere (elle se suffit). Barre du haut et dock evites. */
  var col=seeds.filter(function(s){return s.kind!=='gray'||s.compagnon;});   /* v97 : les deux cellules compagnes de Halin se cadrent avec la parole */
  if(!col.length){ vTarget={s:1,ox:0,oy:0}; return; }
  /* ⚑ v34 — sans cellule vide, la Toile EST ses promesses : on la montre entière, il n'y a rien à cadrer */
  if(col.length===seeds.length){ var s0=_zDef(col.length); vTarget={s:s0,ox:(W-W*s0)/2,oy:(H-H*s0)/2}; return; }   /* v46 : plus il y a de dalles, plus la vue recule */
  var n=col.length;
  if(n>=20){ var s1=_zDef(n); vTarget={s:s1,ox:(W-W*s1)/2,oy:(H-H*s1)/2}; return; }   /* Toile bien remplie : Toile entière, et elle recule à mesure qu'elle se remplit (v46) */
  /* bounding-box de TOUTES les dalles colorees -> on les cadre toutes a l'ecran */
  var minX=1e9,maxX=-1e9,minY=1e9,maxY=-1e9;
  col.forEach(function(s){if(s.x<minX)minX=s.x;if(s.x>maxX)maxX=s.x;if(s.y<minY)minY=s.y;if(s.y>maxY)maxY=s.y;});
  var pad=avg()*1.3;                        /* marge d'une dalle autour */
  minX-=pad;maxX+=pad;minY-=pad;maxY+=pad;
  var bw=Math.max(1,maxX-minX), bh=Math.max(1,maxY-minY);
  var topB=HAUT_LIBRE, botB=H-BAS_LIBRE;    /* zone utile (barre haut + dock evites) */
  var availW=W*0.92, availH=Math.max(1,botB-topB);
  var s=Math.min(availW/bw, availH/bh);
  s=Math.max(1.0, Math.min(s, 2.0));        /* jamais plus loin que la Toile entiere, plafond 2.0 */
  var cx=(minX+maxX)/2, cy=(minY+maxY)/2, scx=W/2, scy=(topB+botB)/2;
  var _ox=scx-cx*s, _oy=scy-cy*s;
  /* clamp : les bords de la Toile restent colles aux bords de l ecran (jamais de vide) */
  _ox=Math.max(W-W*s, Math.min(0, _ox));
  _oy=Math.max(H-H*s, Math.min(0, _oy));
  vTarget={ s:s, ox:_ox, oy:_oy };
}
window.Toile_autoView=function(){autoView();kick();};
/* ⚑ Q212 · REVENIR AU CADRAGE DE DÉPART — le rond « recadrer » et le double toucher y mènent tous deux. */
window.Toile_recadre=function(){ window._recadreDemande=true; window._vueMain=false; autoView(); kick(); try{ if(window._majRecadre) window._majRecadre(); }catch(_){} };
/* ⚑ v54 (Bobinette, Tom : « les fils se tirent pour redéfinir la Toile LÀ OÙ C'EST NÉCESSAIRE. Localement, pas partout ») —
   mesuré au repos, avant et après une plantation : 556 arcs sur 1 156 changeaient, 358 à plus de 3 pas de la dalle — parce que
   CHAQUE graine de la Toile se redistribuait. Pendant une transition de Bobinette, seules les graines proches de la dalle qui
   arrive ou qui part bougent (1,25 pas moyen : ses voisines directes) ; les autres restent en place, et poussent toujours leurs voisines. */
var _finPrev=null;
function _relaxLocal(){ if((theme!=='bobinette'&&theme!=='esquille')||!_trans||_trans.x==null) return null;   /* v57 : Esquille aussi — chaque plantation redistribuait toute la Toile, des éclats changeaient de couleur loin de la dalle */ var d=(RD[theme]&&RD[theme].transDur||0)+4000; if(performance.now()-_trans.t0>d) return null;   /* la fenêtre dure au-delà de la transition : un relâchement tardif (les poids qui finissent de se poser) redevenait global — 58 arcs sautaient après coup */ return {x:_trans.x,y:_trans.y,r:avg()*1.5}; }   /* v56 : 2 → 1,5 pas, les fils bougent maintenant vraiment · v55 (Tom : « trop loin dans le local, c'est devenu ennuyeux ») : 1,25 → 2 pas moyens */
/* ⚑ v89 (Tom : « la parole neuve posée dans un coin, à moitié hors de l'écran ») — sur une Toile faite de ses paroles, la relaxation
   chassait une graine jusqu'au cran de 6 px du bord : mesuré (384, 6), sous le plateau du titre. Le CENTRE d'une dalle (son œil, son
   titre) reste désormais dans la zone utile : 13 % de la largeur sur les côtés (la demi-largeur d'un titre), 17 % de la hauteur en haut
   (sous le plateau), 15 % en bas (la barre). Les cellules vont toujours jusqu'au bord. Les huit anciens (semis constant) gardent le cran d'origine. */
function _bornes(){ if(!_semisNeuf()||(window._apImage&&!(window._apercuClair||{})[theme])) return [6,W-6,6,H-6];   /* v92 : un aperçu en grille (Madrure) couvre tout le canevas, comme les anciens mondes — pas de marges */ var mx=W*0.13, mt=H*0.17, mb=H*0.15; return [mx,W-mx,mt,H-mb]; }
function relax(){var ac=avg(),_dx=!!(RD[theme]&&RD[theme].douce),_lc=_relaxLocal();if(_lc){var _fm=_semisFinal();for(var _fi=0;_fi<seeds.length;_fi++){var _fs=seeds[_fi],_fp=_fm.get(_fs);if(_fp){_fs.tx=_fp[0];_fs.ty=_fp[1];}else{_fs.tx=_fs.x;_fs.ty=_fs.y;}}return;}/* ⚑ v54 (Halin) : une dalle qui part ne pousse plus personne — ses voisines visent tout de suite leur place finale, en même temps qu'elle se retire */for(var i=0;i<seeds.length;i++){var s=seeds[i],fx=0,fy=0;if(_dx&&s.part!=null){s.tx=s.x;s.ty=s.y;continue;}if(_lc&&Math.hypot(s.x-_lc.x,s.y-_lc.y)>_lc.r){s.tx=s.x;s.ty=s.y;continue;}for(var j=0;j<seeds.length;j++){if(j===i)continue;var o=seeds[j];if(_dx&&o.part!=null)continue;var dx=s.x-o.x,dy=s.y-o.y,d=Math.sqrt(dx*dx+dy*dy);var w=ac*(0.92+s.w*0.026+o.w*0.026);if(d<w&&d>0.01){var f=(w-d)/d*0.16;fx+=dx*f;fy+=dy*f;}}var _B=_bornes();s.tx=Math.max(_B[0],Math.min(_B[1],s.x+fx));s.ty=Math.max(_B[2],Math.min(_B[3],s.y+fy));}
}
/* ⚑ v53 (Tom, 25 sept. 2026) — LE VERT DE CÉLÉBRATION EST ABANDONNÉ, PARTOUT. « Une dalle qui naît est déjà un événement : la
   Toile bouge, une forme apparaît. Une couleur par-dessus souligne ce qui se voit déjà. La célébration, c'est le mouvement
   lui-même. » (Six passes, v47 → v52 ; code d'avant : sauvegardes/app-avant-v53.html.) */
function ease(p){return p<0?0:p>1?1:p*p*(3-2*p);}
function kick(){if(!running){running=true;frame._redem=1;requestAnimationFrame(frame);}}   /* v61 : la boucle repart — la première image fait UN pas, comme avant l'horloge */
/* ⚑ v60 (Tom : « les mouvements dans l'app sont-ils identiques à ceux de celebration-mondes.html ? ») — NON, mesuré : fermer
   un écran (`closeAll`) fait frémir toute la Toile (7 à 11 px, ~1 s) — et une plantation ou une suppression ferment un écran.
   Le frémissement se superposait donc au mouvement du monde, que Tom a validé SANS lui. Une arrivée ou un départ prend la
   main : pendant l'impression d'une plantation (`_tirageActive`) la Toile ne frémit pas, et un départ ou une arrivée posé
   dans les 150 ms d'un frémissement l'annule (même geste : aucune image ne l'a encore dessiné). */
function liven(){ if(window._tirageActive || (window._tMouv && performance.now()-window._tMouv<900)) { kick(); return; } _qT0=performance.now();kick();}   /* v60 : pendant qu'une parole arrive ou part, le frémissement ne se superpose pas à son mouvement */window.Toile_liven=liven;window.Toile_probe=function(){var o=[];for(var i=0;i<seeds.length;i++){if(seeds[i].kind!=='gray'){var s=seeds[i];o.push([Math.round(((s.px==null?s.x:s.px)-s.x)*10)/10,Math.round(((s.py==null?s.y:s.py)-s.y)*10)/10]);}}return o;};window.Toile_state=function(){return {running:running,qt:_qT0,theme:theme};};window.Toile_graines=function(){return seeds.map(function(s){return [s.pid==null?null:s.pid,Math.round(s.x),Math.round(s.y),s.kind];});};   /* v89 : lecture (bancs) */window.Toile_previewLive=function(pcv,th,pw,ph){
  if(!pcv||!pcv.getContext)return;
  th=(th&&TH[th])?th:'encre';
  var dpr=Math.min(2,window.devicePixelRatio||1);
  pcv.width=Math.round(pw*dpr);pcv.height=Math.round(ph*dpr);pcv.style.width=pw+'px';pcv.style.height=ph+'px';
  if(!pcv.__pls||pcv.__plth!==th||Math.abs((pcv.__plpw||0)-pw)>2){
    try{window.Toile.preview(pcv,th,pw,ph);}catch(e){}
    var src=(pcv.__c&&pcv.__c.seeds)?pcv.__c.seeds:[];
    var tpl=null;for(var _i=0;_i<src.length;_i++){if(src[_i].kind!=='gray'){tpl=src[_i];break;}}
    tpl=tpl||src[0]||{ci:0,c:null,tone:1,lit:0,shade:1,ang:0,w:0};
    pcv.__pls=src.map(function(o){return {x:o.x,y:o.y,gray:false,gc:null,ci:tpl.ci,c:tpl.c,kind:'promi',tone:tpl.tone,lit:tpl.lit,shade:tpl.shade,ang:o.ang,w:o.w,t0:-99999};});
    var im=(typeof _pdImgs!=='undefined'&&_pdImgs[th])?_pdImgs[th]:null;
    var iw=(im&&im.naturalWidth)||420, ih=(im&&im.naturalHeight)||420;
    var TAR=pw*0.52, kk=TAR/Math.max(iw,ih), bw=iw*kk, bh=ih*kk;
    var bL=pw-Math.round(pw*0.03)-bw, bT=Math.round(ph*0.40)-bh/2;
    pcv.__box={cx:bL+bw/2, cy:bT+bh/2, rx:bw/2, ry:bh/2};
    var N=48, pts=[];for(var _a=0;_a<N;_a++){pts.push({ang:_a/N*6.2832, ph:Math.random()*6.28, fr:1.4+Math.random()*1.9});}
    pcv.__cpts=pts;
    pcv.__plth=th;pcv.__plpw=pw;pcv.__plph=ph;
  }
  pcv.__plqt=performance.now();
  if(pcv.__plraf)cancelAnimationFrame(pcv.__plraf);
  var _d=pcv.width/pw;
  function step(){
    var age=performance.now()-pcv.__plqt, DUR=1300, quiv=age<DUR, env=Math.exp(-age/430);
    var box=pcv.__box, pts=pcv.__cpts;
    var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};
    try{
      g=pcv.getContext('2d');W=pw;H=ph;theme=th;view={s:1,ox:0,oy:0};seeds=pcv.__pls;
      g.setTransform(_d,0,0,_d,0,0);g.clearRect(0,0,pw,ph);
      var AMP=quiv?(box.rx*0.05)*env+2.5*env:0;
      var P=[];
      for(var i=0;i<pts.length;i++){
        var pt=pts[i];
        var wob=Math.sin(age*0.004*pt.fr+pt.ph)*AMP + Math.sin(age*0.0026+pt.ang*3+pt.ph)*AMP*0.55;
        P.push([box.cx+Math.cos(pt.ang)*(box.rx+wob), box.cy+Math.sin(pt.ang)*(box.ry+wob)]);
      }
      g.save();g.beginPath();
      var n=P.length, mx=(P[n-1][0]+P[0][0])/2, my=(P[n-1][1]+P[0][1])/2;
      g.moveTo(mx,my);
      for(var j=0;j<n;j++){var c=P[j], nnx=(P[j][0]+P[(j+1)%n][0])/2, nny=(P[j][1]+P[(j+1)%n][1])/2;g.quadraticCurveTo(c[0],c[1],nnx,nny);}
      g.closePath();g.clip();
      RD[theme](performance.now(),0,0,pw,ph);
      g.restore();
    }catch(e){}
    g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;
    if(quiv)pcv.__plraf=requestAnimationFrame(step);else pcv.__plraf=0;
  }
  step();
};
/* ⚑ v30 (Tom, 23 sept. 2026) — LA GRAINE PROPRIÉTAIRE SE CHERCHE PARMI LES VOISINES, PAS PARMI TOUTES.
   Cinq mondes (Pixel, Braille, Mosaïque, Gravure, Sillons) cherchaient, pour chaque échantillon, la graine qui minimise
   |p−k| − w_k en parcourant TOUTES les graines : Gravure coûtait 440 ms par Toile (1,9 s à ×4). Cet index range les graines
   dans une grille de pas `avg()` et parcourt des anneaux de cases autour du point ; il s'arrête dès qu'aucune case
   restante ne peut faire mieux : une graine hors des r premiers anneaux est à ≥ r·pas du point, donc son score est
   ≥ r·pas − w_max. **Même graine gagnante, au pixel près** (à égalité, la plus petite, comme la boucle d'origine).
   Construit une fois par passe de peinture ; retombe sur la boucle complète si la grille serait démesurée. */
function _grilleProp(){
  var n=seeds.length; if(n<24) return null;
  var cs=Math.max(8,avg()), X=new Float64Array(n), Y=new Float64Array(n), Wt=new Float64Array(n), mw=0, x0=1e18,y0=1e18,x1=-1e18,y1=-1e18;
  for(var k=0;k<n;k++){ var s=seeds[k]; X[k]=s.px==null?s.x:s.px; Y[k]=s.py==null?s.y:s.py; Wt[k]=s.w||0; if(Wt[k]>mw) mw=Wt[k];
    if(X[k]<x0)x0=X[k]; if(X[k]>x1)x1=X[k]; if(Y[k]<y0)y0=Y[k]; if(Y[k]>y1)y1=Y[k]; }
  var gx0=Math.floor(x0/cs), gy0=Math.floor(y0/cs), gw=Math.floor(x1/cs)-gx0+1, gh=Math.floor(y1/cs)-gy0+1;
  if(!(gw>0&&gh>0) || gw*gh>40000) return null;
  var C=new Array(gw*gh); for(var q=0;q<C.length;q++) C[q]=[];
  for(k=0;k<n;k++) C[(Math.floor(Y[k]/cs)-gy0)*gw + (Math.floor(X[k]/cs)-gx0)].push(k);
  var rmax=gw+gh+2, res={bi:0,bd:1e18,bd2:1e18};
  function prop(x,y){
    var ci=Math.floor(x/cs)-gx0, cj=Math.floor(y/cs)-gy0, bd=1e18, bd2=1e18, bi=-1;
    var rmin=Math.max(0, -ci, -cj, ci-(gw-1), cj-(gh-1));   /* le premier anneau qui touche la grille */
    for(var r=0;r<=rmax+rmin;r++){
      for(var j=cj-r;j<=cj+r;j++){ if(j<0||j>=gh) continue;
        var pas=(j===cj-r||j===cj+r)?1:2*r;
        for(var i=ci-r;i<=ci+r;i+=(pas||1)){ if(i<0||i>=gw) continue;
          var L=C[j*gw+i];
          for(var m=0;m<L.length;m++){ var kk=L[m], dx=x-X[kk], dy=y-Y[kk], d=Math.sqrt(dx*dx+dy*dy)-Wt[kk];
            if(d<bd || (d===bd && kk<bi)){ bd2=bd; bd=d; bi=kk; } else if(d<bd2) bd2=d; } } }
      if(r>=rmin && bd2 <= r*cs - mw) break;                 /* aucune case restante ne peut faire mieux, ni le second */
    }
    res.bi=bi<0?0:bi; res.bd=bd; res.bd2=bd2; return res;
  }
  return {prop:prop, X:X, Y:Y, Wt:Wt};   /* v38 : les coordonnées et poids que `prop` compare — Gravure s'en sert pour écarter un point sans requête */
}
function cAt(x,y){var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=x-_kx,dy=y-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}return seeds[bi];}
function cOf(s,now){var g0=s.gc||(s.gc=_shadeG(s.gray,s.tone,s.shade));if(s.tOut!=null&&s.cOut){var pO=ease(Math.max(0,(now-s.tOut)/760));if(pO<1)return [s.cOut[0]+(g0[0]-s.cOut[0])*pO,s.cOut[1]+(g0[1]-s.cOut[1])*pO,s.cOut[2]+(g0[2]-s.cOut[2])*pO];s.tOut=null;s.cOut=null;}   /* ⚑ v55 : une dalle qui part (semis constant) éteint sa couleur vers son gris, en 760 ms comme elle l'a allumée */if(s.kind==='gray'&&(s.t0===0||now-s.t0>760))return g0;var p=ease((now-s.t0)/760);var to=s.ci!=null?(s.rgb||((palKey==='signal'&&!s.apercu&&!s.choisi)?PALL()[s.nat!=null?s.nat:3][s.lit|0]:PALL()[s.ci][s.lit|0])):g0;   /* ⚑ v27 (Tom, Q307 tranché) : « sous Ingénu, un ton de palette CHOISI À LA MAIN passe devant la nature, comme le code libre le fait déjà. Ingénu colore par nature PAR DÉFAUT ; un choix explicite prime toujours. » */   /* ⚑ v17 INGÉNU (Tom) : la couleur dit la nature — Promi 0 bleu, Chiche 1 rose, Nuée 2 lilas ; une cellule sans parole prend le crème dalle (3) ; un code libre du Cercle, choisi à la main, passe toujours devant */   /* ⚑ Cercle · LA COULEUR (Tom 13 sept.) : un code libre passe devant la palette — jamais sur une dalle masquée (ci nul) */var c=[g0[0]+(to[0]-g0[0])*p,g0[1]+(to[1]-g0[1])*p,g0[2]+(to[2]-g0[2])*p];for(var q=0;q<3;q++){if(c[q]>255)c[q]=255;if(c[q]<0)c[q]=0;}return c;}
/* ⚑ v89 (Tom, Q348) — LE NOIR ET BLANC. La Toile passe au ton de la Toile vide : en sombre, du crème sur le fond sombre ; en clair,
   l'inverse. Chaque couleur de dalle (et de graine vide) est ramenée à ce ton ; il ne reste qu'une légère différence de clarté, que la
   JAUGE dose (0 : les dalles ne se distinguent plus des vides ; 1 : des tons francs). L'agencement, le monde, rien d'autre ne change.
   Une seule décision de teinte (cOf) : tous les mondes, la Toile et les aperçus, la suivent. */
var _cOfBrut=cOf;
cOf=function(s,now){ var c=_cOfBrut(s,now); var nb=window._promiNB; if(!nb||!nb.on||!c) return c;
  var lt=isLightM(), base=lt?[32,25,8]:[239,227,199], fond=lt?[241,236,217]:[32,25,8], L=(0.2126*c[0]+0.7152*c[1]+0.0722*c[2])/255, j=nb.j;
  var k=0.05+j*0.62*(lt?L:(1-L)); if(k<0)k=0; if(k>0.72)k=0.72;
  return [base[0]+(fond[0]-base[0])*k, base[1]+(fond[1]-base[1])*k, base[2]+(fond[2]-base[2])*k]; };
function RpixDirect(now,x0,y0,x1,y1){var STEP=5*UK,_G=_grilleProp();g.setTransform(DPR,0,0,DPR,0,0);for(var sy=0;sy<H;sy+=STEP){for(var sx=0;sx<W;sx+=STEP){var lx=(sx+STEP/2-view.ox)/view.s,ly=(sy+STEP/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H)continue;var bi=0;if(_G){bi=_G.prop(lx,ly).bi;}else{var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx,sy,STEP+UK,STEP+UK);}}}
/* ⚑ v39 (perf) — BUVARD FUSIONNE LES CARRÉS VOISINS DE MÊME COULEUR. ~13 000 `fillRect` de STEP+UK, opaques, sur des cotes de la grille : une suite de n carrés de la même couleur sur une rangée devient UN rectangle de n·STEP+UK — même surface couverte, même couleur, rien en transparence. La couleur n'est reposée que si elle change. `_perfAncien` = l'ancien. */
function Rpix(now,x0,y0,x1,y1){if(window._perfAncien)return RpixDirect(now,x0,y0,x1,y1);var _rs=null,_rx=0,_rn=0,_ry=0,_ps=null;function _rv(){if(_rs===null)return;if(_rs!==_ps){g.fillStyle=_rs;_ps=_rs;}g.fillRect(_rx,_ry,_rn*STEP+UK*_vv,STEP+UK*_vv);_rs=null;}var _vv=(g.canvas&&g.canvas.id==='toileCv')?view.s:1,_gx=(g.canvas&&g.canvas.id==='toileCv')?view.ox:0,_gy=(g.canvas&&g.canvas.id==='toileCv')?view.oy:0;   /* ⚑ v46 : la grille est celle de la Toile, à la taille du zoom — à l'échelle 1, exactement celle d'avant */
  var STEP=5*UK*_vv,_G=_grilleProp();g.setTransform(DPR,0,0,DPR,0,0);var _sy0=_gy-Math.ceil(_gy/STEP)*STEP,_sx0=_gx-Math.ceil(_gx/STEP)*STEP;for(var sy=_sy0;sy<H;sy+=STEP){for(var sx=_sx0;sx<W;sx+=STEP){var lx=(sx+STEP/2-view.ox)/view.s,ly=(sy+STEP/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H){_rv();continue;}var bi=0;if(_G){bi=_G.prop(lx,ly).bi;}else{var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var sb=seeds[bi],c=cOf(sb,now),col='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';if(col===_rs&&_ry===sy&&Math.abs(_rx+_rn*STEP-sx)<1e-9){_rn++;}else{_rv();_rs=col;_rx=sx;_ry=sy;_rn=1;}}_rv();}}
function Rbra(now,x0,y0,x1,y1){var _G=_grilleProp(),DOT=9*UK,sx=Math.floor(x0/DOT)*DOT+DOT*.5,sy=Math.floor(y0/DOT)*DOT+DOT*.5;for(var y=sy;y<y1;y+=DOT){for(var x=sx;x<x1;x+=DOT){var bd=1e18,bd2=1e18,bi=0;if(_G){var _P=_G.prop(x,y);bi=_P.bi;bd=_P.bd;bd2=_P.bd2;}else{for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=x-_kx,dy=y-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd2=bd;bd=d;bi=k;}else if(d<bd2)bd2=d;}}var s=seeds[bi],c=cOf(s,now),ed=(bd2-bd)<5*UK,rad=((s.kind==='gray')?2:(ed?2:2.9))*UK;g.beginPath();g.arc(x,y,rad,0,6.2832);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fill();}}}
function RsilDirect(now,x0,y0,x1,y1){var _G=_grilleProp();g.lineCap='round';g.lineJoin='round';var SP=6*UK,AMP=4.5*UK,WL=0.018/UK,LS=6*UK;function wv(xx,ln){return AMP*Math.sin(xx*WL+ln*.55)+AMP*.62*Math.sin(xx*WL*2.4-ln*.42+1.2);}var li=Math.floor(y0/SP);for(var bY=li*SP+SP*.5;bY<y1;bY+=SP,li++){var sX=Math.max(0,x0),run=[],rk=null,rcl=false;function flush(){if(run.length>1){g.beginPath();g.strokeStyle='rgb('+rk+')';g.lineWidth=(rcl?1.5:0.85)*UK;g.moveTo(run[0][0],run[0][1]);for(var q=1;q<run.length;q++)g.lineTo(run[q][0],run[q][1]);g.stroke();}}for(var x=sX;x<=x1;x+=LS){var y=bY+wv(x,li);var s=_G?seeds[_G.prop(x,bY).bi]:cAt(x,bY),c=cOf(s,now),key=(c[0]|0)+','+(c[1]|0)+','+(c[2]|0);if(rk!==null&&key!==rk){var last=run[run.length-1];flush();run=[last];}run.push([x,y]);rk=key;rcl=(s.kind!=='gray');}flush();}}
/* ⚑ v39 (perf) — HOULE : LES ONDES SONT FIXES, SEULES LEURS COULEURS DÉPENDENT DU SEMIS. On calcule à chaque image la suite
   exacte des morceaux (couleur, épaisseur, points) — le même calcul que `RsilDirect` — et sa signature ; si elle n'a pas
   changé (ni la transformation ni la taille du canevas), on repose le calque 1:1, sinon on le repeint avec LES MÊMES
   tracés, dans le même ordre. Tracer ~9 000 segments fins coûtait 16 ms à chaque image. `_perfAncien` = l'ancien. */
var _silCal=null;
function Rsil(now,x0,y0,x1,y1){var cv0=g&&g.canvas;if(window._perfAncien||DPR>3||!cv0||!g.getTransform||_cibleDalle||!(cv0.id==='toileCv'||cv0===_rtCible))return RsilDirect(now,x0,y0,x1,y1);
  var _G=_grilleProp(),SP=6*UK,AMP=4.5*UK,WL=0.018/UK,LS=6*UK,R=[],sig=[];
  function wv(xx,ln){return AMP*Math.sin(xx*WL+ln*.55)+AMP*.62*Math.sin(xx*WL*2.4-ln*.42+1.2);}
  var li=Math.floor(y0/SP);
  for(var bY=li*SP+SP*.5;bY<y1;bY+=SP,li++){var sX=Math.max(0,x0),run=[],rk=null,rcl=false;
    var flush=function(){if(run.length>1){R.push([rk,rcl,run]);sig.push(rk+(rcl?'#':'.')+run.length+'@'+run[0][0]);}};
    for(var x=sX;x<=x1;x+=LS){var y=bY+wv(x,li);var s=_G?seeds[_G.prop(x,bY).bi]:cAt(x,bY),c=cOf(s,now),key=(c[0]|0)+','+(c[1]|0)+','+(c[2]|0);
      if(rk!==null&&key!==rk){var last=run[run.length-1];flush();run=[last];}run.push([x,y]);rk=key;rcl=(s.kind!=='gray');}
    flush();}
  var M=g.getTransform(),k=[M.a,M.b,M.c,M.d,M.e,M.f,cv0.width,cv0.height,UK,x0,y0,x1,y1,sig.join(';')].join('|'),C=_silCal;
  if(!C||C.k!==k){var sc=(C&&C.cv)||document.createElement('canvas');sc.width=cv0.width;sc.height=cv0.height;
    var G=sc.getContext('2d');G.setTransform(M.a,M.b,M.c,M.d,M.e,M.f);G.lineCap='round';G.lineJoin='round';
    for(var i=0;i<R.length;i++){var r=R[i],p=r[2];G.beginPath();G.strokeStyle='rgb('+r[0]+')';G.lineWidth=(r[1]?1.5:0.85)*UK;G.moveTo(p[0][0],p[0][1]);for(var q=1;q<p.length;q++)G.lineTo(p[q][0],p[q][1]);G.stroke();}
    C=_silCal={k:k,cv:sc};}
  g.save();g.setTransform(1,0,0,1,0,0);g.drawImage(C.cv,0,0);g.restore();g.lineCap='round';g.lineJoin='round';}
function RgraDirect(now,x0,y0,x1,y1){g.lineCap='round';g.lineJoin='round';var HS=8*UK,SS=5*UK,ac=avg(),_G=_grilleProp();for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=(cl?2:1.05)*UK;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0;if(_G){bi=_G.prop(qx,qy).bi;}else{for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,ex=qx-_kx,ey=qy-_ky,d=Math.sqrt(ex*ex+ey*ey)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var ins=(bi===ci)&&qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins&&!run){run=true;g.beginPath();g.moveTo(qx,qy);}else if(ins){g.lineTo(qx,qy);}else if(run){g.stroke();run=false;}}if(run)g.stroke();}}}
/* ⚑ v38 (perf) — UN POINT DE HACHURE HORS DE SA CELLULE S'ÉCARTE SANS REQUÊTE. Le propriétaire du point précédent (`_der`) est comparé à la graine qui trace, par LA MÊME formule que `prop` (mêmes coordonnées X/Y/Wt, même règle d'égalité : l'indice le plus bas gagne) : s'il est strictement meilleur, la graine ne possède pas le point — la décision est celle de `prop`, exactement. Sinon la requête complète. Le cadre est testé AVANT (l'ordre ne change pas le résultat). L'ancien chemin reste pour la preuve (`_perfAncien`). */
function Rgra(now,x0,y0,x1,y1){if(window._perfAncien)return RgraDirect(now,x0,y0,x1,y1);g.lineCap='round';g.lineJoin='round';var HS=8*UK,SS=5*UK,ac=avg(),_G=_grilleProp(),_GX=_G&&_G.X,_GY=_G&&_G.Y,_GW=_G&&_G.Wt,_der=-1,_lx=null,_ly=0;for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=(cl?2:1.05)*UK;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0,ins=qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins){if(_G){var _ex=qx-_GX[ci],_ey=qy-_GY[ci],_dc=Math.sqrt(_ex*_ex+_ey*_ey)-_GW[ci],_ecarte=false;if(_der>=0&&_der!==ci){var _fx=qx-_GX[_der],_fy=qy-_GY[_der],_dl=Math.sqrt(_fx*_fx+_fy*_fy)-_GW[_der];_ecarte=(_dl<_dc||(_dl===_dc&&_der<ci));}if(_ecarte)ins=false;else{bi=_G.prop(qx,qy).bi;_der=bi;ins=(bi===ci);}}else{for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,ex=qx-_kx,ey=qy-_ky,d=Math.sqrt(ex*ex+ey*ey)-seeds[k].w;if(d<bd){bd=d;bi=k;}}ins=(bi===ci);}}if(ins&&!run){run=true;g.beginPath();g.moveTo(qx,qy);_lx=null;}else if(ins){_lx=qx;_ly=qy;}else if(run){if(_lx!==null)g.lineTo(_lx,_ly);g.stroke();run=false;}}if(run){if(_lx!==null)g.lineTo(_lx,_ly);g.stroke();}}}}   /* v38 : une hachure est une DROITE — ses points intermédiaires, alignés, n'ajoutaient que des sommets au traceur ; on va du premier au dernier */
function Rmos(now,x0,y0,x1,y1){var _vv=(g.canvas&&g.canvas.id==='toileCv')?view.s:1,_gx=(g.canvas&&g.canvas.id==='toileCv')?view.ox:0,_gy=(g.canvas&&g.canvas.id==='toileCv')?view.oy:0;   /* ⚑ v46 : la grille est celle de la Toile, à la taille du zoom */
  var T=11*UK*_vv,_G=_grilleProp();g.setTransform(DPR,0,0,DPR,0,0);var _sy0=_gy-Math.ceil(_gy/T)*T,_sx0=_gx-Math.ceil(_gx/T)*T;for(var sy=_sy0;sy<H;sy+=T){for(var sx=_sx0;sx<W;sx+=T){var lx=(sx+T/2-view.ox)/view.s,ly=(sy+T/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H)continue;var bi=0;if(_G){bi=_G.prop(lx,ly).bi;}else{var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx+UK*_vv,sy+UK*_vv,T-2*UK*_vv,T-2*UK*_vv);}}}
function Renc(now,x0,y0,x1,y1){g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);var px=_sx*view.s+view.ox,py=_sy*view.s+view.oy;var rad=sp*0.6*view.s;if(px<-rad*2.5||px>W+rad*2.5||py<-rad*2.5||py>H+rad*2.5)continue;var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);g.save();g.translate(px,py);if(_rf<0.999)g.scale(_rf,_rf);   /* v76 : le repli */if(s.drot)g.rotate(s.drot);if(s.dsx)g.scale(s.dsx,s.dsy);g.fillStyle='rgba('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+',.9)';var sd=((k+1)*2654435761)>>>0,rnd=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};for(var b=0;b<9;b++){var _ex=(rnd()-.5)*rad*1.2,_ey=(rnd()-.5)*rad,_rx=rad*(.32+rnd()*.42),_ry=rad*(.16+rnd()*.32),_ea=rnd()*3.14;if(s.dw){var _wp=s.ph+b*1.7;_ex+=Math.sin(now*0.006+_wp)*rad*0.22*s.dw;_ey+=Math.cos(now*0.0072+_wp)*rad*0.18*s.dw;_rx*=1+Math.sin(now*0.0085+_wp)*0.26*s.dw;_ry*=1+Math.cos(now*0.0079+_wp)*0.26*s.dw;_ea+=Math.sin(now*0.005+_wp)*0.6*s.dw;}g.beginPath();g.ellipse(_ex,_ey,_rx,_ry,_ea,0,6.3);g.fill();}g.restore();}}
function Rblok(now,x0,y0,x1,y1){if(!(g.canvas&&g.canvas.id==='toileCv'))g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var c=cOf(s,now);var h=((s.x*13.1+s.y*7.7)%100+100)%100/100;var bw=sp*(0.74+h*0.32),bh=sp*(0.74+(1-h)*0.32);var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);g.save();g.translate(_sx,_sy);g.rotate((h-0.5)*0.36);g.fillStyle="rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";g.beginPath();var rr=Math.min(bw,bh)*0.14;var xx=-bw/2,yy=-bh/2;g.moveTo(xx+rr,yy);g.arcTo(xx+bw,yy,xx+bw,yy+bh,rr);g.arcTo(xx+bw,yy+bh,xx,yy+bh,rr);g.arcTo(xx,yy+bh,xx,yy,rr);g.arcTo(xx,yy,xx+bw,yy,rr);g.closePath();g.fill();g.restore();}}

function Rterr(now,x0,y0,x1,y1){if(!(g.canvas&&g.canvas.id==='toileCv'))g.setTransform(DPR,0,0,DPR,0,0);   /* ⚑ v46 : sur la Toile vivante, la vue (le zoom) est gardée */var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);var sd=((k+1)*2654435761)>>>0;var rr=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};g.fillStyle="rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";for(var e=0;e<7;e++){var a=rr()*6.2832,rd=rr()*sp*0.46*_rf;var ex=_sx+Math.cos(a)*rd,ey=_sy+Math.sin(a)*rd;var w2=sp*(0.11+rr()*0.19)*_rf,h2=sp*(0.08+rr()*0.15)*_rf;   /* v76 : _rf, le repli */g.save();g.translate(ex,ey);g.rotate(rr()*3.1416);g.beginPath();var sides=4+((rr()*3)|0);for(var s2=0;s2<sides;s2++){var an=s2/sides*6.2832;var px=Math.cos(an)*w2*(0.7+rr()*0.5),py=Math.sin(an)*h2*(0.7+rr()*0.5);s2?g.lineTo(px,py):g.moveTo(px,py);}g.closePath();g.fill();g.restore();}}}
function _tfInk(){return isLightM()?[34,28,21]:[246,241,231];}
function _tfHand(g,pts,jit,rnd){g.beginPath();var n=pts.length;for(var i=0;i<=n;i++){var A=pts[i%n],B=pts[(i+1)%n];var ax=A[0]+(rnd()-.5)*jit, ay=A[1]+(rnd()-.5)*jit;if(i===0){g.moveTo(ax,ay);continue;}var mx=(A[0]+B[0])/2+(rnd()-.5)*jit*1.3, my=(A[1]+B[1])/2+(rnd()-.5)*jit*1.3;g.quadraticCurveTo(mx,my,ax,ay);}g.closePath();}
function _tfStroke(g,w,col,alpha){g.lineJoin="round";g.lineCap="round";g.strokeStyle="rgba("+(col[0]|0)+","+(col[1]|0)+","+(col[2]|0)+","+(alpha==null?1:alpha)+")";g.lineWidth=w;g.stroke();}
function _tfFill(g,col,rnd,off){g.save();g.translate((rnd()-.5)*off,(rnd()-.5)*off);g.fillStyle="rgb("+(col[0]|0)+","+(col[1]|0)+","+(col[2]|0)+")";g.fill();g.restore();}
function _tfPetal(g,len,wid,bend,rnd,jit){var j=function(){return (rnd()-.5)*jit;};g.beginPath();g.moveTo(j(),j());g.bezierCurveTo(wid+j(), len*0.3+j(), wid*0.72+bend+j(), len*0.8+j(), j()*0.6, len+j());g.bezierCurveTo(-wid*0.72+bend+j(), len*0.8+j(), -wid+j(), len*0.3+j(), j(), j());g.closePath();}
function _tfPetalR(g,len,wid,bend,rnd,jit){var j=function(){return (rnd()-.5)*jit;};var tw=wid*0.3;g.beginPath();g.moveTo(j(),j());g.bezierCurveTo(wid+j(), len*0.3+j(), wid*0.72+bend+j(), len*0.82, tw+bend+j(), len*0.95);g.quadraticCurveTo(bend+j(), len*1.0, -tw+bend+j(), len*0.95);g.bezierCurveTo(-wid*0.72+bend+j(), len*0.82+j(), -wid+j(), len*0.3+j(), j(), j());g.closePath();}
function RtoufDirect(now,x0,y0,x1,y1){var _viv=(g.canvas&&g.canvas.id==='toileCv');if(!_viv)g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));var ink=_tfInk();for(var i=0;i<seeds.length;i++){var s=seeds[i];var sx=(s.px!=null?s.px:s.x),sy=(s.py!=null?s.py:s.y);if(_viv&&(sx<x0-sp*1.3||sx>x1+sp*1.3||sy<y0-sp*1.3||sy>y1+sp*1.3))continue;   /* ⚑ v46 : très zoomé, on ne peint que ce qui se voit */var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);var _sd=((i+1)*2654435761)>>>0;var rnd=function(){_sd=(_sd*1103515245+12345)&0x7fffffff;return _sd/0x7fffffff;};var heart=[c[0]+(ink[0]-c[0])*0.45,c[1]+(ink[1]-c[1])*0.45,c[2]+(ink[2]-c[2])*0.45];   /* ⚑ v29 (Tom) : le cœur était #DD4D23, la couleur « à tenir » — un monde ne porte jamais une couleur d'état. Il est désormais la couleur de SA cellule, poussée vers l'encre du contour : une nuance de cOf, rien d'inventé. */var n=3+((rnd()*3)|0);for(var f2=0;f2<n;f2++){var ox=sx+(rnd()-.5)*sp*0.86, oy=sy+(rnd()-.5)*sp*0.8;var R=sp*(0.13+rnd()*0.2);var stage=rnd();g.strokeStyle="rgba("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+",0.6)";g.lineWidth=Math.max(1.2,R*0.2);g.lineCap="round";g.beginPath();g.moveTo(ox+(rnd()-.5)*5,oy+sp*0.5);g.quadraticCurveTo(ox+(rnd()-.5)*R,oy+sp*0.2,ox,oy);g.stroke();g.save();g.translate(ox,oy);g.rotate(rnd()*6.2832);if(stage<0.24){var bp=[[-R*0.4,R*0.3],[-R*0.34,-R*0.4],[0,-R*0.72],[R*0.34,-R*0.4],[R*0.4,R*0.3]];_tfHand(g,bp,R*0.08,rnd);_tfFill(g,c,rnd,R*0.08);_tfHand(g,bp,R*0.08,rnd);_tfStroke(g,Math.max(1.1,R*0.17),ink,0.9);}else{var np=6+((rnd()*3)|0);for(var k=0;k<np;k++){if(stage>0.8&&rnd()<0.2)continue;g.save();g.rotate(k/np*6.2832+(rnd()-.5)*0.34);var len=R*(0.85+rnd()*0.6), wid=R*(0.26+rnd()*0.16);var _rd=(((i*13+f2*7+k*5)%10)<2);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfFill(g,c,rnd,R*0.09);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfStroke(g,Math.max(1,R*0.16),ink,0.88);g.restore();}g.beginPath();g.arc((rnd()-.5)*R*0.12,(rnd()-.5)*R*0.12,R*0.3,0,6.2832);g.fillStyle="rgb("+heart[0]+","+heart[1]+","+heart[2]+")";g.fill();_tfStroke(g,Math.max(1,R*0.15),ink,0.85);}g.restore();}}}
function _toufGraine(g,i,c,sx,sy,sp,ink){var _sd=((i+1)*2654435761)>>>0;var rnd=function(){_sd=(_sd*1103515245+12345)&0x7fffffff;return _sd/0x7fffffff;};var heart=[c[0]+(ink[0]-c[0])*0.45,c[1]+(ink[1]-c[1])*0.45,c[2]+(ink[2]-c[2])*0.45];   /* ⚑ v29 (Tom) : le cœur était #DD4D23, la couleur « à tenir » — un monde ne porte jamais une couleur d'état. Il est désormais la couleur de SA cellule, poussée vers l'encre du contour : une nuance de cOf, rien d'inventé. */var n=3+((rnd()*3)|0);for(var f2=0;f2<n;f2++){var ox=sx+(rnd()-.5)*sp*0.86, oy=sy+(rnd()-.5)*sp*0.8;var R=sp*(0.13+rnd()*0.2);var stage=rnd();g.strokeStyle="rgba("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+",0.6)";g.lineWidth=Math.max(1.2,R*0.2);g.lineCap="round";g.beginPath();g.moveTo(ox+(rnd()-.5)*5,oy+sp*0.5);g.quadraticCurveTo(ox+(rnd()-.5)*R,oy+sp*0.2,ox,oy);g.stroke();g.save();g.translate(ox,oy);g.rotate(rnd()*6.2832);if(stage<0.24){var bp=[[-R*0.4,R*0.3],[-R*0.34,-R*0.4],[0,-R*0.72],[R*0.34,-R*0.4],[R*0.4,R*0.3]];_tfHand(g,bp,R*0.08,rnd);_tfFill(g,c,rnd,R*0.08);_tfHand(g,bp,R*0.08,rnd);_tfStroke(g,Math.max(1.1,R*0.17),ink,0.9);}else{var np=6+((rnd()*3)|0);for(var k=0;k<np;k++){if(stage>0.8&&rnd()<0.2)continue;g.save();g.rotate(k/np*6.2832+(rnd()-.5)*0.34);var len=R*(0.85+rnd()*0.6), wid=R*(0.26+rnd()*0.16);var _rd=(((i*13+f2*7+k*5)%10)<2);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfFill(g,c,rnd,R*0.09);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfStroke(g,Math.max(1,R*0.16),ink,0.88);g.restore();}g.beginPath();g.arc((rnd()-.5)*R*0.12,(rnd()-.5)*R*0.12,R*0.3,0,6.2832);g.fillStyle="rgb("+heart[0]+","+heart[1]+","+heart[2]+")";g.fill();_tfStroke(g,Math.max(1,R*0.15),ink,0.85);}g.restore();}}
function Rtouf(now,x0,y0,x1,y1){
  /* ⚑ v38 (perf) — CHAQUE GRAINE PEINT SES FLEURS UNE FOIS, dans un calque à sa taille finale, posé 1:1 ensuite.
     Le dessin est le MÊME (`_toufGraine` est le corps d'origine, recopié) ; la fraction de pixel de la graine est
     intégrée au calque, qui se pose donc sur une cote ENTIÈRE : aucun rééchantillonnage. Le calque se refait si sa
     couleur, son pas, l'encre ou la densité changent — et, s'il a bougé, dès qu'il est posé (pendant le mouvement il se
     pose à la cote entière la plus proche : ≤ ½ pixel d'appareil). Touffe ignore la vue (setTransform(DPR)) et ses fleurs
     ne dépendent pas des voisines : c'est ce qui rend le calque exact. Le chemin direct garde les dalles (`_cibleDalle`),
     les aperçus et l'export (DPR > 3). Mesuré au dessin forcé : 61 → voir CONTRAT-MONDE §8.4. */
  var cv0=g&&g.canvas;
  if(window._perfAncien||_cibleDalle||DPR>3||!cv0||!(cv0.id==='toileCv'||cv0===_rtCible))return RtoufDirect(now,x0,y0,x1,y1);
  /* ⚑ v46 (Tom : « le zoom dans tous les mondes, comme une photo ») — Touffe ignorait la vue : ses fleurs ne grossissaient
     jamais. Les calques sont désormais posés à la place ET à la taille du zoom. Pendant un geste (pincement, élan, retour),
     un calque dont l'échelle a changé de moins d'un tiers est seulement mis à l'échelle (fluide) ; il se redessine net dès
     que le zoom se pose. Au-delà de ×1,3 le chemin direct (vectoriel, et qui ne peint que ce qui se voit) prend le relais. */
  var vs=(cv0.id==='toileCv')?view.s:1, vox=(cv0.id==='toileCv')?view.ox:0, voy=(cv0.id==='toileCv')?view.oy:0;
  var mouv=!!(pinch||_inert||_pan||vTarget&&Math.abs(vTarget.s-view.s)>0.0015);
  if(vs>1.3&&!mouv)return RtoufDirect(now,x0,y0,x1,y1);   /* posé et très zoomé : les vecteurs, nets */
  var sv=Math.min(vs,1.3);   /* un calque ne se bâtit jamais plus grand que ×1,3 */
  var sp=Math.sqrt(W*H/Math.max(1,seeds.length)),ink=_tfInk(),B=Math.ceil(1.1*sp*DPR*sv)+4,T=2*B+2;
  g.save();g.setTransform(1,0,0,1,0,0);
  for(var i=0;i<seeds.length;i++){var s=seeds[i];var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);var sx=(s.px!=null?s.px:s.x),sy=(s.py!=null?s.py:s.y);
    var X=(sx*vs+vox)*DPR,Y=(sy*vs+voy)*DPR,k=i+'|'+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+'|'+(+c[0]).toFixed(3)+','+(+c[1]).toFixed(3)+','+(+c[2]).toFixed(3)+'|'+sp+'|'+ink[0]+'|'+DPR,C=s.__tf;
    var Bv=B*vs/sv; if(X<-Bv||Y<-Bv||X>cv0.width+Bv||Y>cv0.height+Bv)continue;
    var fx=X-Math.floor(X),fy=Y-Math.floor(Y),pose=(s.__tfX===X&&s.__tfY===Y);s.__tfX=X;s.__tfY=Y;
    if(C&&C.k===k&&C.vs!==vs&&mouv){var r=vs/C.vs;g.drawImage(C.cv,X-(C.B+C.fx)*r,Y-(C.B+C.fy)*r,C.T*r,C.T*r);continue;}   /* en mouvement : mis à l'échelle, redessiné net quand le zoom se pose */
    if(!C||C.k!==k||C.vs!==sv||(pose&&(C.fx!==fx||C.fy!==fy))){
      if(!C){C=s.__tf={cv:document.createElement('canvas')};}
      if(C.cv.width!==T||C.cv.height!==T){C.cv.width=T;C.cv.height=T;}
      var G=C.cv.getContext('2d');G.setTransform(1,0,0,1,0,0);G.clearRect(0,0,T,T);G.setTransform(DPR*sv,0,0,DPR*sv,B+fx,B+fy);
      _toufGraine(G,i,c,0,0,sp,ink);C.k=k;C.fx=fx;C.fy=fy;C.vs=sv;C.B=B;C.T=T;}
    if(_rf<0.999){ g.drawImage(C.cv,X-(C.B+C.fx)*_rf*vs/C.vs,Y-(C.B+C.fy)*_rf*vs/C.vs,C.T*_rf*vs/C.vs,C.T*_rf*vs/C.vs); continue; }   /* v76 : le temps de son repli (ou de sa repousse), la fleur suit l'échelle */
    if(C.vs===vs) g.drawImage(C.cv,Math.round(X-C.fx)-C.B,Math.round(Y-C.fy)-C.B);
    else { var r2=vs/C.vs; g.drawImage(C.cv,X-(C.B+C.fx)*r2,Y-(C.B+C.fy)*r2,C.T*r2,C.T*r2); }}
  g.restore();g.setTransform(DPR,0,0,DPR,0,0);}
var RD={pixel:Rpix,braille:Rbra,sillons:Rsil,gravure:Rgra,mosaique:Rmos,encre:Renc,eclats:Rblok,terrazzo:Rterr,touffe:Rtouf};
/* ⚑ v32 — LES QUATRE MONDES NEUFS. `creerMondes` (bloc lot-V32-MONDES) reçoit le moteur par ACCESSEURS : g, W, H, seeds,
   view sont relus à chaque appel, donc un monde neuf suit les échanges de globales des cinq chemins (§1 du contrat).
   · cOf(s, 0) rendait le GRIS de départ d'une dalle colorée (l'animation part de t0) : le carnet des mondes l'appelle à 0,
     il reçoit donc la couleur posée.  · `_dalleDeCle(pid)` : l'entier stable du titre et de la personne (jamais l'id).
   · `rampe` : aucune — la rampe v29 ne vaut que pour une dalle, jamais sur la Toile (§12 ter, Q3).
   · `cleToile` : Toile.cle() (v31).  · `fondToile()` : le fond du moteur, un seul propriétaire (v26).
   · `relance` : Madrure repeint l'onde d'avant tant que le semis bouge ; le moteur doit revenir la construire. */
var _cleVue={}; var _envM=null; var _MN=null, _MNLIB={esquille:1,bobinette:1,madrure:1}, _cibleDalle=null, _bordsDalle=null; var _rtCible=null;
try{ if(window.creerMondes){ _MN=window.creerMondes(_envM={
  get g(){return g;}, get W(){return W;}, get H(){return H;}, get DPR(){return DPR;}, get seeds(){return seeds;}, get view(){return view;},
  cOf:function(s,now){ return cOf(s, now||performance.now()); },
  avg:avg, cAt:cAt, isLightM:isLightM, curPAL:curPAL, rampe:null,
  _dalleDeCle:function(pid){ try{ for(var i=0;i<promises.length;i++){ if(promises[i].id===pid){ var p=promises[i], t=String(p.title||'')+'|'+String(p.who||''), h=2166136261;
    for(var j=0;j<t.length;j++){ h^=t.charCodeAt(j); h=Math.imul(h,16777619)>>>0; } _cleVue[pid]=h; return h; } } }catch(e){} return _cleVue[pid]!=null?_cleVue[pid]:null; },   /* ⚑ v43 : la dernière clé vue — une parole supprimée garde la sienne le temps de partir */
  get cleToile(){ try{ return (window.Toile&&window.Toile.cle)?window.Toile.cle():undefined; }catch(e){ return undefined; } },
  fondToile:function(){ return window.Toile.fondToile(); },
  relance:function(){ lastChange=performance.now(); kick(); },
  get cible(){ return _cibleDalle; },
  get bords(){ return _bordsDalle; },
  /* ⚑ v34 — l'unité de matière à la densité historique de la Toile (68 cellules), indépendante du nombre de promesses */
  get uMat(){ var a=_WT?_WT[0]*_WT[1]:W*H; return Math.sqrt(Math.max(1,a)/68)*UK; },   /* v63 : dans dalleTrame, W×H est la boîte de la cellule — l'unité reste celle de la Toile */
  get ingenu(){ return palKey==='signal'; },
  /* ⚑ v43 — la transition en cours, sur la Toile vivante seulement ; null partout ailleurs */
  get trans(){ if(!_transVive||!_trans||window._transCoupe) return null; var d=RD[theme]&&RD[theme].transDur; return (d&&performance.now()-_trans.t0<d)?_trans:null; },   /* v44 : éteinte à la fin de SA durée ; `_transCoupe` = preuve (la Toile sans transition) */
  get vive(){ return _transVive; },
  /* v66 — le papier : sur la Toile vivante, le dégradé même du fond, dans le repère de la vue ; ailleurs le fond du moteur */
  papierDesc:function(){ return (_transVive&&!_AP)?_fondVifDesc((0-view.ox)/view.s,(0-view.oy)/view.s,(W*0.55-view.ox)/view.s,(H-view.oy)/view.s):null; },
  papier:function(){ if(_transVive&&!_AP) return _fondVif(g,(0-view.ox)/view.s,(0-view.oy)/view.s,(W*0.55-view.ox)/view.s,(H-view.oy)/view.s); var c=window.Toile.fondToile(); return typeof c==='string'?c:'rgb('+c[0]+','+c[1]+','+c[2]+')'; },
  get finale(){ try{ return _semisFinal(); }catch(_){ return null; } }   /* v47 : l'équilibre de la Toile (point fixe de relax), partout */
});
  RD.esquille=_MN.esquille; RD.bobinette=_MN.bobinette; RD.ritournelle=_MN.ritournelle; RD.madrure=_MN.madrure; RD.halin=_MN.halin; } }catch(e){ _MN=null; }
/* ⚑ v62 — BROUILLAMINI (bloc lot-V62-BROUILLAMINI) : sa propre fabrique, le même environnement, plus la rampe de matière du
   monde (`rampeMat` = grays() : TH[monde].g en sombre, GLIGHT en clair). Monde LIBRE : ses dalles débordent la cellule, elles
   se peignent, se découpent et se touchent sur ce qu'il a peint ; `_MN` lui passe la main pour son nom. */
try{ if(_MN&&_envM&&window.creerBrouillamini){ var _MB=window.creerBrouillamini(Object.create(_envM,{rampeMat:{get:function(){ return grays(); }}}));
  RD.brouillamini=_MB.brouillamini; _MNLIB.brouillamini=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='brouillamini'?_MB[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v63 — CHAMADE (bloc lot-V63-CHAMADE), même patron ; en plus : l'ENCRE du produit (`_tfInk`, le précédent de Touffe) pour ses
   bandes et le trait de ses cœurs, et le fond du moteur (`fondToile`) pour le papier de sa dalle seule. */
try{ if(_MN&&_envM&&window.creerChamade){ var _MC=window.creerChamade(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.chamade=_MC.chamade; _MNLIB.chamade=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='chamade'?_MC[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v64 — VOLUBILIS (bloc lot-V64-VOLUBILIS), même patron, même encre du produit (Q331). */
try{ if(_MN&&_envM&&window.creerVolubilis){ var _MV=window.creerVolubilis(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.volubilis=_MV.volubilis; _MNLIB.volubilis=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='volubilis'?_MV[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v65 — GUINGOIS (bloc lot-V65-GUINGOIS), même patron, même encre. */
try{ if(_MN&&_envM&&window.creerGuingois){ var _MG=window.creerGuingois(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.guingois=_MG.guingois; _MNLIB.guingois=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='guingois'?_MG[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v66 — CHANTOURNÉ (bloc lot-V66-CHANTOURNE) : l'encre du produit, et la rampe de matière (ses flammes de fond). */
try{ if(_MN&&_envM&&window.creerChantourne){ var _MH=window.creerChantourne(Object.create(_envM,{encre:{get:function(){ return _tfInk; }},rampeMat:{get:function(){ return grays(); }}}));
  RD.chantourne=_MH.chantourne; _MNLIB.chantourne=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='chantourne'?_MH[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v67 — MASCARET (bloc lot-V67-MASCARET) : l'encre du produit ; son papier est celui du moteur (env.papier). */
try{ if(_MN&&_envM&&window.creerMascaret){ var _MS=window.creerMascaret(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.mascaret=_MS.mascaret; _MNLIB.mascaret=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='mascaret'?_MS[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v68 — RAMAGE (bloc lot-V68-RAMAGE) : l'encre du produit, la rampe de matière (son plumage), le papier du moteur. */
try{ if(_MN&&_envM&&window.creerRamage){ var _MR=window.creerRamage(Object.create(_envM,{encre:{get:function(){ return _tfInk; }},rampeMat:{get:function(){ return grays(); }}}));
  RD.ramage=_MR.ramage; _MNLIB.ramage=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='ramage'?_MR[f]:o).apply(null,arguments); }; }); } }catch(e){}

/* --- LES ÉTIQUETTES, sur la Toile elle-même ---
   L'app fournit le texte (window.Toile.labelOf) et dit si le mode est actif
   (window.Toile.labelsOn). L'encre est choisie par dalle : claire sur une
   dalle sombre, sombre sur une dalle claire — jamais de contour, jamais de voile. */
function _lum(c){
  function l(v){v/=255;return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4);}
  return 0.2126*l(c[0])+0.7152*l(c[1])+0.0722*l(c[2]);
}
function _fit(gg,txt,max){
  if(gg.measureText(txt).width<=max)return txt;
  var t=txt;
  while(t.length>1&&gg.measureText(t+'…').width>max)t=t.slice(0,-1);
  return t+'…';
}
function _labels(now){
  /* pendant l'onboarding, la Toile est un décor : pas de texte sur les dalles,
     même si le Studio est réglé « avec texte » */
  var _ob=document.getElementById('promiOnb');
  if(_ob&&!_ob.classList.contains('gone'))return;
  var T=window.Toile;
  if(!T||typeof T.labelsOn!=='function'||!T.labelsOn())return;
  if(typeof T.labelOf!=='function')return;
  g.setTransform(DPR,0,0,DPR,0,0);
  g.textAlign='center';g.textBaseline='middle';
  var ac=avg();                                  /* écart moyen entre dalles */
  if(ac*view.s<48) return;                       /* v98 : aucune dalle n'a la place de porter son titre (voir plus bas) */
  for(var i=0;i<seeds.length;i++){
    var s=seeds[i];
    if(s.kind==='gray')continue;
    /* un Promi masque au partage n'affiche pas son texte non plus */
    if(window._shLabels!==undefined&&s.pid!=null&&(window.shareHidden||{})[s.pid])continue;
    var L=null;try{L=T.labelOf(s);}catch(e){}
    if(!L||!L.title)continue;
    /* la dalle est dessinée à px/py (position réellement occupée) : l'étiquette doit suivre,
       sinon le texte reste à côté de sa dalle. */
    var _lx=(s.px!=null?s.px:s.x), _ly=(s.py!=null?s.py:s.y), _la=null;
    /* ⚑ v63 — un monde qui DÉPLACE sa dalle (Chamade écarte ses cœurs) déclare où il l'a posée, et sa largeur : le titre y va */
    if(RD[theme]&&RD[theme].ancre){ try{ _la=RD[theme].ancre(s); }catch(_e){ _la=null; } if(_la){ _lx=_la[0]; _ly=_la[1]; } }
    var sx=_lx*view.s+view.ox, sy=_ly*view.s+view.oy;
    if(sx<-60||sy<-40||sx>W+60||sy>H+40)continue;
    /* ⚑ v98 (Tom, 29 sept. : « illisibles à 200-500 paroles, c'est normal, on zoome pour lire — mais vérifie qu'ils disparaissent
       proprement plutôt que de s'empiler en bouillie ») — le titre ne se pose que si la dalle, À L'ÉCRAN, a la place de le porter :
       écart moyen × zoom ≥ 48 px (la taille de lettre y vaut 7,5, le plancher d'origine) ; il s'efface sur les 8 px au-dessous
       du plafond de 56. On zoome : les titres reviennent. Avant : bornés à 28 px de large et 7,5 px de haut, ils se chevauchaient
       — et `_fit` les rognait lettre à lettre (8 700 mesures de texte par image à 500, 1,4 s en WebKit). */
    var _ecr=ac*view.s; if(_ecr<48) continue; var _lab=Math.min(1,(_ecr-48)/8);
    var wmax=Math.max(28, ac*view.s*0.86);       /* on reste DANS la dalle */
    if(_la&&_la[2]) wmax=Math.max(28, Math.min(wmax, _la[2]*view.s*0.8));
    var col=cOf(s,now);
    var ink=(_lum(col)>0.179)?'#1E1301':'#FFFFFF';
    /* ⚑ v33 (Tom) — l'encre se choisit sur ce qui est PEINT dessous. Un monde qui sait ce qu'il a peint le dit
       (`RD[theme].sous`, Madrure) : cinq points le long du titre, luminance moyenne. Les autres gardent la cellule. */
    if(RD[theme]&&RD[theme].sous){ var _sm=0,_sn=0; for(var _k=-2;_k<=2;_k++){ var _c=null;
        try{ _c=RD[theme].sous(_lx+_k*wmax*0.2/view.s, _ly+fs*0.34/view.s); }catch(_e){}
        if(_c){ _sm+=_lum(_c); _sn++; } }
      if(_sn) ink=((_sm/_sn)>0.179)?'#1E1301':'#FFFFFF'; }
    var fs=Math.max(7.5, Math.min(13, ac*view.s*0.155));
    g.fillStyle=ink;
    if(L.who){
      g.font='600 '+(fs*0.68).toFixed(1)+'px Atkinson,system-ui,sans-serif';
      g.globalAlpha=0.72*_lab;
      g.fillText(_fit(g,String(L.who).toUpperCase(),wmax), sx, sy-fs*0.72);
      g.globalAlpha=1;
    }
    g.font='500 '+fs.toFixed(1)+'px Atkinson,system-ui,sans-serif';
    if(_lab<1) g.globalAlpha=_lab;
    g.fillText(_fit(g,L.title,wmax), sx, sy+fs*0.34);
    g.globalAlpha=1;
  }
}

/* --- LA FORME RÉELLE D'UNE DALLE ---
   Pour que l'Index montre la MÊME dalle que la Toile, et non un pictogramme.
   On découpe le cadre par les bissectrices, exactement comme le rendu. */
function _cellPoly(s){
  var poly=[[0,0],[W,0],[W,H],[0,H]];
  for(var k=0;k<seeds.length;k++){
    var o=seeds[k]; if(o===s)continue;
    var dx=o.x-s.x, dy=o.y-s.y;
    var d=Math.sqrt(dx*dx+dy*dy); if(d<0.001)continue;
    var nx=dx/d, ny=dy/d;
    /* la frontière se décale du côté de la dalle la plus « lourde » */
    var m=d/2 + ((s.w||0)-(o.w||0))/2;
    var px=s.x+nx*m, py=s.y+ny*m;
    var out=[],n=poly.length;
    for(var i=0;i<n;i++){
      var A=poly[i], B=poly[(i+1)%n];
      var da=(A[0]-px)*nx+(A[1]-py)*ny;
      var db=(B[0]-px)*nx+(B[1]-py)*ny;
      if(da<=0)out.push(A);
      if((da<0&&db>0)||(da>0&&db<0)){
        var t=da/(da-db);
        out.push([A[0]+(B[0]-A[0])*t, A[1]+(B[1]-A[1])*t]);
      }
    }
    poly=out; if(poly.length<3)return null;
  }
  return poly;
}
var LIVE={encre:1,terrazzo:1,touffe:1,eclats:1};
function frame(now){if(!g){running=false;return;}var _ss=document.getElementById('studioScreen');if(!_AP&&_ss&&_ss.classList.contains('show')){requestAnimationFrame(frame);return;}var _stg=document.getElementById('stage');if(!_AP&&_stg&&_stg.style.display==='none'){running=false;return;}   /* ⚑ v75 : `_AP` — la même image, pour un aperçu du Studio (voir Toile.apercuImage) */
  /* ⚑ v43 — une dalle partie se retire au bout de PART_DUR ; tant qu'il en reste une, la Toile tourne */
  var _parts=false;for(var _pq=seeds.length-1;_pq>=0;_pq--){if(seeds[_pq].part!=null){if(performance.now()-seeds[_pq].part>(seeds[_pq].rT0!=null?REPLI_DUR+60:((RD[theme]&&RD[theme].partDur)||PART_DUR))){var _po=seeds[_pq];if(!_semisNeuf()&&(_REPLI[theme]||_AP)){var _pv=mk(_po.x,_po.y,'gray');_pv._b=_po._b;_pv.tx=_po.tx;_pv.ty=_po.ty;_pv.px=_po.px;_pv.py=_po.py;_pv.w=_pv.wt=_pv.wFin=_po.w;_pv.wAt=0;_pv.gray=_po.gray;_pv.tone=_po.tone;_pv.shade=_po.shade;_pv.ang=_po.ang;_pv.ph=_po.ph;_pv.am=_po.am;seeds[_pq]=_pv;}else seeds.splice(_pq,1);relax();}   /* v76 : repliée, elle reste au semis constant (grise, invisible) */else _parts=true;}}
  /* une dalle qui vient de se planter GRANDIT : elle pousse ses voisines, et la
     Toile entière se réajuste autour d'elle tant que la place n'est pas faite. */
  /* ⚑ v44 (Tom, 24 sept.) — DANS LES QUATRE MONDES NEUFS, LA TOILE BOUGE COMME UN RESSORT, SUR LE TEMPS RÉEL. « Tout doux,
     logique, puis se stabilise ; là ça saute. » Le mouvement d'origine avançait de 22 % de la distance À CHAQUE IMAGE : vitesse
     maximale dès la première image (un à-coup), traîne exponentielle coupée net au seuil de 0,6 px, et une vitesse qui dépend
     de la cadence (§8 : un mouvement se calcule sur le temps). Ici : un ressort à amortissement critique (position ET poids),
     vitesse nulle au départ, pas de rebond, posé en ~0,7 s ; il ne s'arrête que quand position ET vitesse sont sous le
     dixième de pixel. Les huit anciens mondes gardent leur mouvement d'origine, au pixel. */
  if(!_AP&&(_ecZ||_ecActif)){ var _ecN=0; for(var _ei=0;_ei<seeds.length;_ei++){ var _es=seeds[_ei]; if(_es.pid!=null||_es.kind==='nuee'||_es.part!=null) continue; var _ed=!!(_ecZ&&_ecDans(_es));
      if(_ed&&!_es._ec){ _es._ec=1; _es._ecW=(_es.wt!=null?_es.wt:_es.w)||0; _es.rT0=now; _es.rW0=_es.w||0; _es.wt=_es.wFin=_repliW(); _es.wAt=0; }
      else if(!_ed&&_es._ec){ _es._ec=0; _es.rT0=now; _es.rW0=_es.w||0; _es.wt=_es.wFin=_es._ecW; _es.wAt=0; }
      if(_es._ec) _ecN++; } _ecActif=_ecN>0; }   /* v83 : l'écartement (Toile.ecarte) — voir plus bas */
  var _ressort=_semisNeuf(), _rdt=0;
  if(_ressort){ _rdt=Math.max(0,(now-(frame._t||now))/1000); if(frame._redem||_rdt>0.25)_rdt=1/60; }   /* ⚑ v61 (Tom : « la durée ne doit pas dépendre de la charge ») — le pas était plafonné à 50 ms, et toute image de plus de 100 ms comptait pour 1/60 s : sur un appareil lent le ressort perdait du temps. Il intègre maintenant le temps VRAI, en sous-pas de 1/60 s au plus (stable) ; seul un redémarrage de la boucle (ou un trou de plus de 250 ms) compte pour une image, comme avant. À 60 i/s : un sous-pas, identique. */ var _nsub=_ressort?Math.max(1,Math.ceil(_rdt*60-1e-6)):1, _h=_rdt/_nsub;   /* au redémarrage de la boucle (pause), un pas d'une image : sinon le premier pas ferait 20 % du chemin */
  frame._t=now;
  var grow=false;
  if(!_ressort){
  for(var q=0;q<seeds.length;q++){
    var sq=seeds[q];
    if(sq.rT0!=null){ var _ra=Math.min(1,(now-sq.rT0)/REPLI_DUR); var _re=_ra*_ra*(3-2*_ra); sq.w=sq.rW0+(sq.wt-sq.rW0)*_re; grow=true; if(_ra>=1&&sq.part==null){ sq.w=sq.wt; sq.rT0=null; } continue; }   /* v76 : le repli, sur le temps */
    if(sq.wt==null)sq.wt=sq.w;
    if(Math.abs(sq.wt-sq.w)>0.04){ sq.w+=(sq.wt-sq.w)*0.13; grow=true; }
    else if(sq.w!==sq.wt){ sq.w=sq.wt; grow=true; }
  }
  if(grow)relax();
  }
  var mv=false,grow=false;
  /* ⚑ v54 (Pochade, Touffe) — ces mondes avancent d'une FRACTION FIXE du chemin restant à chaque image : le mouvement est le
     plus rapide à son tout premier instant — « trop sec, trop soudain ». Le pas monte en 300 ms après une plantation, puis
     reprend son rythme exact. */
  /* ⚑ v55 (Tom : « une fois lent, une fois rapide ») — ces pas étaient une fraction fixe du chemin PAR IMAGE : chaque image un
     peu plus longue ou plus courte changeait la vitesse (mesuré sur Touffe : 1,5 · 2,9 · 1,8 · 2,4 d'une image à l'autre). Dans
     Pochade et Touffe ils se calculent sur le TEMPS écoulé — les mêmes 0,17 et 0,22 à 60 images par seconde. */
  var _kW=0.17, _kX=0.22, _redem=frame._redem; frame._redem=0; var _dtf=frame._tp?Math.min(4,Math.max(0.2,(now-frame._tp)/16.667)):1; if(theme==='encre'||theme==='touffe'){ _kW=1-Math.pow(0.838,_dtf); _kX=1-Math.pow(0.79,_dtf); } else if(theme==='mosaique'||theme==='braille'||theme==='pixel'||theme==='terrazzo'||theme==='gravure'){ if(_redem) _dtf=1; _kW=1-Math.pow(0.83,_dtf); _kX=1-Math.pow(0.78,_dtf); }   /* ⚑ v61 (Tom : « ce n'est pas un changement de rythme : à 60 images par seconde, rien ne bouge ») — Tesselle, Braille, Buvard, Éclisse, Taille-douce passent à l'HORLOGE : à 16,67 ms par image ce sont exactement 0,17 et 0,22 ; sur une image lente le pas grandit, la durée validée tient. ⚑ EXCEPTION : HOULE (sillons) RESTE PAR IMAGE — elle tourne à ~30 i/s sur la page validée ; à l'horloge elle deviendrait plus rapide que ce que Tom a validé. */   /* v56 (Tom : « très très peu, à peine perceptible, mais ça fera la diff ») : 0,17 → 0,162 et 0,22 → 0,21 par image */ frame._tp=now;
  var _amo=1; if((theme==='encre'||theme==='touffe')&&window._tPlante){ var _ta=(now-window._tPlante)/360;   /* v56 : 300 → 360 ms */ if(_ta<1){ _ta=Math.max(0.04,_ta); _amo=_ta*_ta*(3-2*_ta); } }
  var OMX=(RD[theme]&&RD[theme].omx)||9, OMW=(RD[theme]&&RD[theme].omw)||8;   /* rad/s — position, poids (v50 : un monde peut demander un ressort plus doux) */
  for(var i=0;i<seeds.length;i++){
    var s=seeds[i];
    /* la poussée retombe : la dalle s'est fait sa place, elle se détend */
    if(s.wAt&&now>=s.wAt){s.wt=s.wFin;s.wAt=0;}
    if(_ressort){
      if(s.wt==null)s.wt=s.w; if(s.vw==null)s.vw=0; if(s.vx==null){s.vx=0;s.vy=0;}
      var ew=s.wt-s.w, ex=s.tx-s.x, ey=s.ty-s.y;
      for(var _q=0;_q<_nsub;_q++){ var _ew=s.wt-s.w; s.vw+=(OMW*OMW*_ew-2*OMW*s.vw)*_h; s.w+=s.vw*_h;
        var _ex=s.tx-s.x, _ey=s.ty-s.y; s.vx+=(OMX*OMX*_ex-2*OMX*s.vx)*_h; s.vy+=(OMX*OMX*_ey-2*OMX*s.vy)*_h; s.x+=s.vx*_h; s.y+=s.vy*_h; }
      if(Math.abs(ew)>0.02||Math.abs(s.vw)>0.05)grow=true; else {s.w=s.wt;s.vw=0;}
      if(Math.abs(ex)+Math.abs(ey)>0.1||Math.abs(s.vx)+Math.abs(s.vy)>0.5)mv=true; else {s.x=s.tx;s.y=s.ty;s.vx=0;s.vy=0;}
      continue;
    }
    if(s.rT0==null&&s.wt!==undefined&&Math.abs(s.wt-s.w)>0.04){s.w+=(s.wt-s.w)*_kW*_amo;grow=true;}
    s.x+=(s.tx-s.x)*_kX*_amo;s.y+=(s.ty-s.y)*_kX*_amo;
    if(Math.abs(s.tx-s.x)+Math.abs(s.ty-s.y)>.6)mv=true;
  }
  /* tant qu'une dalle grandit, la Toile entière se recalcule autour d'elle */
  /* la poussée se propage de proche en proche : toute la Toile réagit */
  if(grow){relax();relax();relax();mv=true;}
  if(grow)mv=true;var an=mv;for(i=0;i<seeds.length;i++)if(seeds[i].kind!=='gray'&&now-seeds[i].t0<760)an=true;if(!_AP&&!Object.keys(ptrs).length){
    /* ⚑ v46 — l'élan du glissé, puis le retour dans les bornes (ou vers le cadrage demandé) : un ressort sur le TEMPS */
    var _dv=(now-(frame._tv||0))/1000; if(!(_dv>0)||_dv>0.1) _dv=1/60; frame._tv=now;
    if(_inert){ view.ox+=_inert.vx*_dv; view.oy+=_inert.vy*_dv; var _dk=Math.exp(-_dv*4.2); _inert.vx*=_dk; _inert.vy*=_dk; an=true;
      var _bi=_borne(); if(_bi&&(Math.abs(_bi.ox-view.ox)>0.5||Math.abs(_bi.oy-view.oy)>0.5)){ var _dk2=Math.exp(-_dv*16); _inert.vx*=_dk2; _inert.vy*=_dk2; }
      if(Math.abs(_inert.vx)+Math.abs(_inert.vy)<12) _inert=null; }
    var _tg=_inert?null:(vTarget||_borne());
    if(_tg){ var _kz=1-Math.exp(-_dv*7.5), ds=_tg.s-view.s, dx=_tg.ox-view.ox, dy=_tg.oy-view.oy;
      if(Math.abs(ds)>0.0015||Math.abs(dx)>0.3||Math.abs(dy)>0.3){ view.s+=ds*_kz; view.ox+=dx*_kz; view.oy+=dy*_kz; an=true; }
      else { view.s=_tg.s; view.ox=_tg.ox; view.oy=_tg.oy; } }
  }g.setTransform(DPR,0,0,DPR,0,0);g.clearRect(0,0,W,H);var bg=_AP?window.Toile.fondToile():_fondVif(g,0,0,W*0.55,H);   /* v75 : un aperçu garde le fond de l'aperçu */   /* v66 : le fond, un seul propriétaire (_fondVif) */
  g.fillStyle=bg;g.fillRect(0,0,W,H);
  g.setTransform(view.s*DPR,0,0,view.s*DPR,view.ox*DPR,view.oy*DPR);var x0=Math.max(0,(-view.ox)/view.s),y0=Math.max(0,(-view.oy)/view.s),x1=Math.min(W,(-view.ox)/view.s+W/view.s),y1=Math.min(H,(-view.oy)/view.s+H/view.s);var rr=14;g.save();g.beginPath();g.moveTo(rr,0);g.arcTo(W,0,W,H,rr);g.arcTo(W,H,0,H,rr);g.arcTo(0,H,0,0,rr);g.arcTo(0,0,W,0,rr);g.closePath();var _clipA=!!window._perfAncien;if(_clipA)g.clip();var _isG=(theme==='pixel'||theme==='mosaique'||theme==='braille'||theme==='sillons'||theme==='gravure');var _dur=_isG?850:1100;var _qa=performance.now()-_qT0,_quiv=(_qT0>0&&_qa>=0&&_qa<_dur);for(var _pi=0;_pi<seeds.length;_pi++){var _ps=seeds[_pi];if(_ps.kind==='gray'){_ps.px=_ps.x;_ps.py=_ps.y;continue;}if(_ps.ph==null){_ps.ph=Math.random()*6.28;_ps.am=0.6+Math.random()*0.7;}if(_quiv){var _LA=(typeof window!=='undefined'&&window._liveAmp!=null)?window._liveAmp:1;var _env=Math.exp(-_qa/(_isG?300:380));var _pa=_isG?11:7,_pay=_isG?8:5;_ps.px=_ps.x+Math.sin(_qa*0.0092+_ps.ph)*_pa*_ps.am*_env*_LA;_ps.py=_ps.y+Math.cos(_qa*0.0096+_ps.ph)*_pay*_ps.am*_env*_LA;_ps.dsx=1+Math.sin(_qa*0.0100+_ps.ph)*0.09*_env*_LA;_ps.dsy=1+Math.cos(_qa*0.0112+_ps.ph*1.2)*0.09*_env*_LA;_ps.drot=Math.sin(_qa*0.0085+_ps.ph*0.7)*0.08*_env*_LA;_ps.dw=_env*_LA;}else{_ps.px=_ps.x;_ps.py=_ps.y;_ps.dsx=1;_ps.dsy=1;_ps.drot=0;_ps.dw=0;}}if(seeds.length){_transVive=true;try{window._mondeEncore=false;RD[theme](now,x0,y0,x1,y1);}finally{_transVive=false;}}g.restore();if(!_clipA&&!_AP){g.beginPath();g.moveTo(rr,0);g.arcTo(W,0,W,H,rr);g.arcTo(W,H,0,H,rr);g.arcTo(0,H,0,0,rr);g.arcTo(0,0,W,0,rr);g.closePath();g.setTransform(DPR,0,0,DPR,0,0);g.rect(0,0,W,H);g.fillStyle=bg;g.fill('evenodd');}   /* ⚑ v38 (perf) — LE COIN ARRONDI N'EST PLUS UN clip() : on peint la matière sans découpage, puis le fond (même dégradé) autour du rectangle arrondi. Mêmes pixels (le clip antialiasé et l'aplat du complément ont la même couverture) ; WebKit faisait payer le clip à CHAQUE tracé — Touffe 205 → 51 ms par image, Gravure 56 → 33. `_perfAncien` rend l'ancien chemin (preuve). */
  if(!_AP){_voile();
  try{_labels(now);}catch(e){}}var _trv=!!(_trans&&RD[theme]&&RD[theme].transDur&&now-_trans.t0<RD[theme].transDur);   /* ⚑ v43 */
  if(_AP){_AP.encore=!!(an||now-lastChange<170||_quiv||_trv||_parts||window._mondeEncore);return;}   /* v75 : l'aperçu tient sa propre boucle */
  if(an||now-lastChange<170||_quiv||_trv||_parts||window._mondeEncore)requestAnimationFrame(frame);else running=false;}
function addP(k){
  /* ⚑ v34/v35 — monde neuf : on ne ressème pas le semis vide, il s'efface ; monde ancien : le code d'origine */
  if(_semisNeuf()) _sansGris(); else if(!seeds.length) seedGray();
  var p=(k==='nuee')?iposNuee():ipos();
  var s=mk(p.x,p.y,k||'promi');
  s.ci=cc(s);s.c=PAL[s.ci];s.t0=performance.now();
  /* Elle naît minuscule, POUSSE pour se faire une place — les voisines s'écartent —
     puis se détend jusqu'à sa taille de croisière. C'est le geste : une dalle s'insère,
     la Toile entière se réajuste autour d'elle, puis se repose. */
  s.w=-22; s.wt=(k==='nuee')?18:12;
  s.wFin=(k==='nuee')?14:3.4; s.wAt=performance.now()+380;
  seeds.push(s);
  if(k==='nuee'){lastNuee=s;}
  /* ⚑ v47 (Tom : « un frémissement, pas un séisme ») — un monde qui DÉCLARE `sansPoussee` (Esquille) : la dalle naît à sa
     taille finale. La poussée (naître à 12, repousser les voisines, retomber à 3,4) faisait deux vagues — l'aller et le
     retour — sur une plaque dont les éclats sont fixes : deux vagues de recoloration. Ici les voisines glissent UNE fois. */
  if(RD[theme]&&RD[theme].sansPoussee){ s.w=s.wFin; s.wt=s.wFin; s.wAt=0; }
  if(RD[theme]&&RD[theme].douce){ s.wt=s.wFin; s.wAt=0; }   /* v50 : Halin grandit sans pousser ses voisines */
  _transPose('arrive',s.x,s.y);
  window._vueMain=false; window._recadreDemande=true;   /* v46 : une dalle créée ramène le zoom par défaut */   /* ⚑ v43 — le moment où la dalle arrive */
  relax();tones();lastChange=s.t0;var te=document.getElementById('toileEmpty');if(te)te.style.display='none';kick();return s;}
/* ⚑ v34 — les graines grises (le semis de la Toile VIDE, §10.6) s'effacent dès qu'une vraie parole arrive. */
/* ⚑ v35 — la famille du monde courant : les quatre neufs ont le semis qui grandit, les huit anciens le semis constant */
var _NEUFS={esquille:1,bobinette:1,ritournelle:1,madrure:1,halin:1,brouillamini:1,chamade:1,volubilis:1,guingois:1,chantourne:1,mascaret:1,ramage:1}, _semisDe=null;   /* v48 : Halin est une Toile faite de ses paroles */
function _semisNeuf(){ return !!_NEUFS[theme]; }
/* ⚑ v98 (Tom, 29 sept. : « Ajoute des cellules aux huit anciens. Une parole qui n'apparaît pas est inacceptable — la décision
   v35 valait pour l'aspect, pas pour perdre des paroles. Garde leur semis constant tant qu'il y a de la place, et n'ajoute que
   lorsqu'il est plein. ») — dans un monde ancien, `plantOne` rend null quand il n'y a plus de cellule vide : la parole restait
   sans dalle. On pose alors une cellule DE PLUS, au plus grand vide (`_auVide`, tiré de la clé de la Toile), déjà posée
   (poids de croisière) : le relâchement final de `sync` la fait sa place. Au-dessous du plein, rien ne change. */
function _celluleEnPlus(k,i){ var p=_auVide(i), s=mk(p.x,p.y,k); s.ci=cc(s); s.c=PAL[s.ci]; s.t0=performance.now()-900;
  s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; seeds.push(s); window.Toile.paintOrder=null; return s; }
/* ⚑ v45 (Tom, 24 sept.) — « IL EN FAUT DE TAILLES UN PEU DIFFÉRENTES, COMME DANS LE PDF ; sinon il paraît trop régulier et on
   perd son côté esthétique. » Dans les quatre mondes neufs toutes les paroles avaient le MÊME poids (3,4) : cellules égales,
   coulées égales. Chaque parole reçoit désormais son AMPLEUR, stable (tirée de son titre et de sa personne, jamais de l'id
   ni du hasard) : un poids de −0,09 à +0,22 × l'écart moyen entre graines (réparti vers le haut : quelques
   grandes coulées, aucune écrasée — ±0,3 donnait des coulées minuscules et des étiquettes qui se chevauchent). Le toucher,
   les étiquettes, la dalle d'une fiche lisent la même règle pondérée : ils suivent sans rien changer. Une Nuée garde sa
   base plus large (14). Les huit anciens mondes ne sont pas touchés. */
function _ampleur(s){ var t='', h=2166136261, j;
  if(s.pid!=null){ try{ for(j=0;j<promises.length;j++){ if(promises[j].id===s.pid){ t=String(promises[j].title||'')+'|'+String(promises[j].who||''); break; } } }catch(_){ } if(!t) t='p'+s.pid; }
  else if(s.nuee) t='n'+s.nuee; else return null;
  for(j=0;j<t.length;j++){ h^=t.charCodeAt(j); h=Math.imul(h,16777619)>>>0; }
  h^=h>>>15; h=Math.imul(h,2246822507)>>>0; h^=h>>>13;
  var u=(h%10007)/10006; return -0.09+0.31*u*u; }   /* de −0,09 à +0,22 × l'écart moyen : plus de grandes que de petites, aucune écrasée */
function _amplifie(){ if(!_semisNeuf()) return; var a=avg();
  for(var i=0;i<seeds.length;i++){ var s=seeds[i]; if(s.part!=null) continue; var d=_ampleur(s); if(d==null) continue;
    var base=(s.kind==='nuee')?14:3.4, f=base+d*a; s.wFin=f; if(!s.wAt){ s.wt=f; if(s._amp==null) s.w=f; } s._amp=1; } }
function _sansGris(){ var n=seeds.length; seeds=seeds.filter(function(s){ return s.kind!=='gray'; }); if(seeds.length!==n){ window.Toile.paintOrder=null; } }
/* ⚑ v34 — le plus grand vide, tiré de la clé de la Toile et du rang : 24 candidats, on garde le plus loin des graines. */
function _auVide(i){ var cle=0; try{ cle=(window.Toile&&window.Toile.cle)?window.Toile.cle():0; }catch(_){ }
  var sd=((cle^Math.imul(i+1,2654435761))>>>0)||1, r=function(){ sd=(Math.imul(sd,1103515245)+12345)&0x7fffffff; return sd/0x7fffffff; };
  var best=null, bd=-1;
  for(var c=0;c<24;c++){ var x=W*(0.1+0.8*r()), y=H*(0.1+0.8*r()), d=1e18;
    for(var k=0;k<seeds.length;k++){ var dx=x-seeds[k].x, dy=y-seeds[k].y, dd=dx*dx+dy*dy; if(dd<d) d=dd; }
    if(d>bd){ bd=d; best={x:x,y:y}; } }
  return best||{x:W/2,y:H/2}; }
var nueeCells={};window.Toile={addPromi:function(id){/* ⚑ v34/v35 — dans un monde neuf une plantation AJOUTE sa cellule ; dans un ancien elle colore une cellule du semis */var s=null;if(_semisNeuf()){_sansGris();s=addP('promi');}else{s=window.Toile.plantOne();if(!s)s=addP('promi');}if(s&&id!=null){s.pid=id;_dalleFigee(true);}if(s&&_semisNeuf()){_amplifie();relax();}return s;},
  /* la dalle sous le doigt : même métrique que le rendu, au pixel près */
  hit:function(cx,cy){
    if(!seeds.length)return null;
    var lx=(cx-view.ox)/view.s, ly=(cy-view.oy)/view.s;
    /* ⚑ v34 — la Toile n'a plus de case vide dès sa première parole : HORS de son rectangle (vue reculée), c'est le vide —
       le double toucher y recadre (Q212), et un toucher n'y ouvre aucune dalle. */
    if(lx<0||ly<0||lx>W||ly>H) return null;
    /* ⚑ v32 — un monde libre neuf se touche sur la dalle qu'il a PEINTE ; hors d'elle, la règle de la cellule reprend. */
    if(_MN&&_MNLIB[theme]){ try{ var _tt=_MN.toucher(theme,lx,ly); if(_tt&&_tt.kind!=='gray') return {pid:(_tt.pid!=null?_tt.pid:null), kind:_tt.kind, nuee:_tt.nuee||null}; }catch(_e){}
      if(RD[theme]&&RD[theme].toucheStrict) return null; }   /* v62 : Brouillamini se touche sur le contour peint, jamais sur la cellule */
    var bd=1e18,bs=null;
    for(var k=0;k<seeds.length;k++){
      var dx=lx-seeds[k].x, dy=ly-seeds[k].y;
      var d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;
      if(d<bd){bd=d;bs=seeds[k];}
    }
    if(!bs||bs.kind==='gray')return null;
    return {pid:(bs.pid!=null?bs.pid:null), kind:bs.kind, nuee:bs.nuee||null};
  },
  /* remet la Toile en accord avec les Promi réels : 1 Promi = 1 dalle */
  sync:function(list){
    /* ⚑ v35 (Tom, 23 sept.) — LE SEMIS QUI GRANDIT EST UNE EXCEPTION DES QUATRE MONDES NEUFS. Pochade, Tesselle, Touffe,
       Braille, Buvard, Houle, Taille-douce et Éclisse gardent le semis CONSTANT d'origine et leur aspect d'origine ; seuls
       Esquille, Bobinette, Ritournelle et Madrure ont une Toile faite de ses seules promesses. Incohérence assumée (voir
       CLAUDE.md) : les anciens mondes ont été dessinés, réglés et validés sur le semis constant. Le code d'origine suit,
       tel quel ; un semis venu de l'autre famille est d'abord ressemé. */
    /* ⚑ v46 — une dalle CRÉÉE ou SUPPRIMÉE ramène le zoom par défaut (les autres synchronisations — changer de monde,
       rafraîchir — le laissent où la main l'a mis) */
    try{ var _avP={}, _nA=0, _chg=false; for(var _zi=0;_zi<seeds.length;_zi++){ var _zs=seeds[_zi]; if(_zs.kind!=='gray'&&_zs.pid!=null&&_zs.part==null){ _avP[_zs.pid]=1; _nA++; } }
      var _nL=0; (list||[]).forEach(function(id){ _nL++; if(!_avP[id]) _chg=true; }); if(_nL!==_nA) _chg=true;
      if(_chg){ window._vueMain=false; window._recadreDemande=true; _inert=null; if(_qT0 && performance.now()-_qT0<150) _qT0=0; window._tMouv=performance.now(); } }catch(_z){}   /* v60 : une parole qui part ou arrive prend la main sur le frémissement du même geste, et son moment est protégé */
    _semisDe=_semisNeuf()?'neuf':'ancien';
    if(_semisDe==='ancien'){
      if(seeds.length && !seeds.some(function(s){ return s.kind==='gray'; })){ seeds=[]; }
    if(!seeds.length)seedGray();
      /* Les dalles REDEVIENNENT des cellules vides — on ne les SUPPRIME pas.
         Avant, sync() les arrachait du tableau : quand l'onboarding laissait une
         Toile pleine de couleur (donc zéro cellule vide), il ne restait qu'une
         poignée de cellules. La Toile paraissait alors monstrueusement zoomée. */
      /* ⚑ v55 (Tom : « Pochade et Touffe — adoucis le départ, 24,8 et 47,4 d'écart, c'est brutal ») — chaque synchronisation
         remettait TOUTES les dalles en cellules grises puis replantait chaque parole sur une cellule grise TIRÉE AU HASARD : au
         retrait d'une seule, toutes les autres sautaient ailleurs, et les grises prenaient une allure neuve. Sur une Toile déjà
         peuplée : les dalles qui restent GARDENT leur place et leur allure ; celle qui part redevient une cellule grise AU MÊME
         ENDROIT, de la même forme, sa couleur s'éteignant vers son gris ; seules les paroles nouvelles se plantent. */
      var _garde={}, _gardeN={}, _tn=performance.now(), _dejaCol=false;
      for(var _li=0;_li<list.length;_li++) _garde[list[_li]]=1;
      try{ if(typeof NUE!=='undefined'){ for(var _nk0 in NUE){ if(_nk0!=='soi') _gardeN[_nk0]=1; } } }catch(_e){}
      for(var i=0;i<seeds.length;i++){ if(seeds[i].kind!=='gray'){ _dejaCol=true; break; } }
      var _restent={}, _restentN={};
      for(var i=0;i<seeds.length;i++){
        var s=seeds[i];
        if(s.kind!=='gray'){
          if(_dejaCol && s.kind!=='nuee' && s.pid!=null && _garde[s.pid] && !_restent[s.pid]){ _restent[s.pid]=s; continue; }
          if(_dejaCol && s.kind==='nuee' && s.nuee && _gardeN[s.nuee] && !_restentN[s.nuee]){ _restentN[s.nuee]=s; continue; }
          if(s.part!=null) continue;   /* v76 : une dalle qui se replie finit de se replier */
          /* ⚑ v76 (Tom) — « un trou noir à la place de la dalle supprimée, pas un recouvrement par les dalles autour qui se
             rapprochent ». Dans ces six mondes la dalle qui part RESTE une dalle, de sa couleur, pendant que son poids descend
             et que ses voisines la recouvrent (le départ `part` de v43) ; recouverte, elle redevient une cellule grise REPLIÉE,
             gardée au semis (densité constante, v35), qu'une plantation reprend d'abord et fait regrandir — l'inverse exact. */
          if(_REPLI[theme]&&_dejaCol&&s.kind!=='nuee'){ s.partPid=s.pid; s.pid=null; _replie(s,_tn); continue; }
          var v=mk(s.x,s.y,'gray');
          v.px=s.px; v.py=s.py; v.tx=s.tx; v.ty=s.ty; v.gray=s.gray; v.gc=s.gc; v.tone=s.tone; v.shade=s.shade; v.ang=s.ang; v.ph=s.ph; v.am=s.am;
          if(_dejaCol){ try{ v.cOut=cOf(s,_tn); v.tOut=_tn; }catch(_c){} }
          v.w=s.w; v.wt=0; v.wFin=0; v.wAt=0;
          /* ⚑ v76 (Tom) — « un trou noir à la place de la dalle supprimée, pas un recouvrement par les dalles autour qui se
             rapprochent ». Dans ces six mondes, la dalle qui part se REPLIE : sa couleur s'éteint (cOut) pendant que son poids
             descend, et ses voisines la recouvrent. La cellule reste au semis, repliée : une plantation la reprend d'abord
             (plantOne), et elle regrandit en poussant — l'inverse exact. La densité du semis ne bouge pas (v35). */
          seeds[i]=v;
        }
      }
      nueeCells={};
      /* chaque Promi reprend sa place parmi les cellules vides : le nombre de
         cellules ne bouge pas, la Toile garde ses proportions */
      for(var j=0;j<list.length;j++){
        if(_restent[list[j]]) continue;
        var np=window.Toile.plantOne(true);
        if(!np) np=_celluleEnPlus('promi',j);   /* ⚑ v98 (Tom) — « une parole qui n'apparaît pas est inacceptable » : semis plein, on ajoute */
        if(np)np.pid=list[j];
      }
      /* ⚑ UNE NUÉE A SA DALLE (Tom, 13 sept. 2026) — sync l'effaçait à chaque plantation : une Nuée était invisible sur la
         Toile, même portant neuf paroles. Une dalle par Nuée nommée (« soi » n'est pas une Nuée), à la taille de dalle de Nuée
         que le moteur donne déjà (`addP('nuee')` : wFin 14). */
      try{ if(typeof NUE!=='undefined'){ for(var _nk in NUE){ if(_nk==='soi')continue;
        if(_restentN[_nk]){ nueeCells[_nk]=_restentN[_nk]; lastNuee=_restentN[_nk]; continue; }
        var _ns=window.Toile.plantOne(true); if(!_ns)_ns=_celluleEnPlus('nuee',list.length+_nk.length);
        _ns.kind='nuee'; _ns.nuee=_nk; _ns.w=14; _ns.wt=14; _ns.wFin=14; nueeCells[_nk]=_ns; lastNuee=_ns; } } }catch(_e){}
      relax();tones();lastChange=performance.now();
      autoView();
      kick();
      return;
    }
    var nk=[]; try{ if(typeof NUE!=='undefined'){ for(var _nk in NUE){ if(_nk!=='soi') nk.push(_nk); } } }catch(_e){}
    if(!list.length && !nk.length){ seeds=[]; seedGray(); nueeCells={}; relax();tones();lastChange=performance.now();autoView();kick(); return; }
    var avant={}; for(var i=0;i<seeds.length;i++){ var s0=seeds[i]; if(s0.kind==='gray') continue;
      if(s0.pid!=null) avant['p'+s0.pid]=s0; else if(s0.kind==='nuee'&&s0.nuee) avant['n'+s0.nuee]=s0; }
    var now=performance.now(); seeds=[]; nueeCells={};
    for(var j=0;j<list.length;j++){ var s=avant['p'+list[j]];
      if(!s){ var p=_auVide(j); s=mk(p.x,p.y,'promi'); s.ci=cc(s); s.c=PAL[s.ci]; s.t0=now-900; s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; }
      s.pid=list[j]; seeds.push(s); }
    for(var q=0;q<nk.length;q++){ var t=avant['n'+nk[q]];
      if(!t){ var p2=_auVide(list.length+q); t=mk(p2.x,p2.y,'nuee'); t.ci=cc(t); t.c=PAL[t.ci]; t.t0=now-900; }
      t.kind='nuee'; t.nuee=nk[q]; t.w=14; t.wt=14; t.wFin=14; t.wAt=0; seeds.push(t); nueeCells[nk[q]]=t; lastNuee=t; }
    /* ⚑ v43 — LE DÉPART D'UNE DALLE. Dans un monde qui anime ses transitions (`transDur`), la dalle qui part ne disparaît
       pas d'une image à l'autre : elle reste le temps de se retirer (`part` = l'heure du départ, sans pid — plus rien ne la
       touche ni ne l'étiquette), ses voisines prennent sa place, et le moteur la retire au bout de PART_DUR. Une ou deux
       dalles seulement : au-delà, c'est une resynchronisation (changement de famille, réinitialisation), pas un départ. */
    try{ if(RD[theme]&&RD[theme].transDur){ var _pris={}; for(var _k2=0;_k2<seeds.length;_k2++) _pris[seeds[_k2].pid!=null?'p'+seeds[_k2].pid:'n'+seeds[_k2].nuee]=1;
      var _dep=[]; for(var _ak in avant){ if(!_pris[_ak]&&!avant[_ak].part) _dep.push(avant[_ak]); }
      if(_dep.length&&_dep.length<=2){ for(var _d=0;_d<_dep.length;_d++){ var _g=_dep[_d]; _g.part=now; _g.partPid=_g.pid; _g.partNuee=_g.nuee; _g.pid=null; _g.nuee=null; _g.wt=_g.w-30; _g.wFin=_g.wt; _g.wAt=0; if(RD[theme].sansPoussee) _g.w=_g.wt; seeds.push(_g); }
        _transPose('depart',_dep[0].x,_dep[0].y); } } }catch(_e){}
    _amplifie();   /* v45 */
    relax();relax();relax();tones();lastChange=performance.now();
    autoView();
    kick();
  },
  /* --- completion : on colore les cellules DEJA en place, dans un ordre fixe --- */
  paintOrder:null,
  /* la forme EXACTE de la dalle d'un Promi, ramenée dans un carré de côté `box`
     (l'Index montre ainsi la même dalle que la Toile, pas un pictogramme) */
  dalleAbs:function(pid){
    var s=null;for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){s=seeds[i];break;}}
    if(!s)return null;var poly=null;try{poly=_cellPoly(s);}catch(e){}
    if(!poly||poly.length<3)return null;
    var st=null;try{st=STRUCT[state.structure];}catch(e){}
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var j=0;j<poly.length;j++){if(poly[j][0]<minx)minx=poly[j][0];if(poly[j][0]>maxx)maxx=poly[j][0];if(poly[j][1]<miny)miny=poly[j][1];if(poly[j][1]>maxy)maxy=poly[j][1];}
    return {poly:poly,minx:minx,miny:miny,w:maxx-minx,h:maxy-miny,round:(st&&st.round)||2,stroke:(st&&st.stroke)||'none',sw:(st&&st.sw)||1};
  },
  roundPathOf:function(pts,r){try{return roundPath(pts,r);}catch(e){return null;}},
  shapeOf:function(pid,box){
    box=box||30;
    var s=null;
    for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){s=seeds[i];break;}}
    if(!s)return null;
    var poly=null; try{poly=_cellPoly(s);}catch(e){}
    if(!poly||poly.length<3)return null;
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var j=0;j<poly.length;j++){
      if(poly[j][0]<minx)minx=poly[j][0]; if(poly[j][0]>maxx)maxx=poly[j][0];
      if(poly[j][1]<miny)miny=poly[j][1]; if(poly[j][1]>maxy)maxy=poly[j][1];
    }
    var w=maxx-minx, h=maxy-miny; if(w<=0||h<=0)return null;
    var pad=box*0.12, inner=box-pad*2;
    var k=Math.min(inner/w, inner/h);
    var ox=pad+(inner-w*k)/2, oy=pad+(inner-h*k)/2;
    var d='';
    for(var q=0;q<poly.length;q++){
      var X=(ox+(poly[q][0]-minx)*k).toFixed(1), Y=(oy+(poly[q][1]-miny)*k).toFixed(1);
      d+=(q?'L':'M')+X+' '+Y+' ';
    }
    return d+'Z';
  },
  reserved:[],
  /* L'onboarding plante de VRAIES dalles : elles s'insèrent entre les autres,
     qui s'écartent. Le même geste que dans l'app — plus aucun fondu. */
  plantOne:function(dejaPosee){
    var gris=[];
    for(var i=0;i<seeds.length;i++)if(seeds[i].kind==='gray')gris.push(seeds[i]);
    if(!gris.length)return null;
    /* le champ clair : ni sous la barre du haut, ni sous le dock. Une dalle plantée
       là serait illisible — on préfère toujours une cellule dégagée. */
    var libres=gris.filter(function(s){return s.y>HAUT_LIBRE && s.y<H-BAS_LIBRE;});
    /* v76 — une cellule REPLIÉE (une dalle partie) est reprise d'abord : la nouvelle dalle regrandit d'où l'autre s'est retirée */
    if(_REPLI[theme]){ var _rw=_repliW()/2, _rp=gris.filter(function(s){return (s.wt!=null?s.wt:s.w)<_rw;}); if(_rp.length) libres=_rp; }
    var pool=libres.length?libres:gris;
    var cible=pool[(Math.random()*pool.length)|0];
    var a=avg();
    var jx=(Math.random()-.5)*a*0.5, jy=(Math.random()-.5)*a*0.5;
    var s=mk(Math.max(8,Math.min(W-8,cible.x+jx)), Math.max(8,Math.min(H-8,cible.y+jy)), 'promi');
    s.ci=cc(s);s.c=PAL[s.ci];
    s.t0=performance.now();      /* la dalle se REMPLIT (gris -> couleur) en prenant sa place */
    if(dejaPosee){ s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; s.t0=performance.now()-900; }
    else { s.w=-22; s.wt=12; s.wFin=3.4; s.wAt=performance.now()+380; if(RD[theme]&&RD[theme].douce){ s.wt=3.4; s.wAt=0; } }
    var k=seeds.indexOf(cible);      /* la cellule grise qui l'accueille s'efface : densite constante */
    /* ⚑ v54 (Tom : « Pochade et Touffe — le début du mouvement est trop sec, trop soudain ») — mesuré : à la première image,
       écart 6,7 (Pochade) et 28,2 (Touffe), puis ~1 et ~4. La cellule grise était retirée et la dalle neuve ajoutée EN FIN DE
       LISTE, ailleurs (décalée au hasard), minuscule (poids −22), avec un autre gris : trois ruptures à l'image zéro — et dans
       Touffe le rang changé redessinait d'autres fleurs. Dans ces deux mondes, la dalle neuve PREND LA PLACE de la cellule
       grise : même rang, même lieu, même poids, même allure ; elle ne fait qu'ENSUITE son mouvement (sa place décalée, sa
       poussée, sa couleur). Les autres mondes ne changent pas. */
    if(k>=0&&(theme==='encre'||theme==='touffe')&&!dejaPosee){
      window._tPlante=performance.now();
      s.tx=s.x; s.ty=s.y; s.x=cible.x; s.y=cible.y; s.px=cible.px; s.py=cible.py;
      s.gray=cible.gray; s.gc=cible.gc; s.tone=cible.tone; s.shade=cible.shade; s.ang=cible.ang; s.ph=cible.ph; s.am=cible.am;
      s.w=cible.w||0; seeds[k]=s;
    } else {
      seeds.push(s);
      if(k>=0)seeds.splice(k,1);
    }
    window.Toile.paintOrder=null;
    relax();tones();lastChange=performance.now();
    window._vueMain=false; window._recadreDemande=true;   /* v46 : une dalle créée ramène le zoom par défaut */
    autoView();      /* la vue recule d'un cran */
    kick();
    return s;
  },
  unplantOne:function(){
    for(var i=seeds.length-1;i>=0;i--){
      if(seeds[i].kind==='promi'&&seeds[i].pid==null){
        var s=seeds[i];
        var g=mk(s.x,s.y,'gray'); g.w=-9; g.wt=0;
        seeds.splice(i,1,g);
        window.Toile.paintOrder=null;
        relax();tones();lastChange=performance.now();kick();
        return true;
      }
    }
    return false;
  },
  colored:function(){var n=0;for(var i=0;i<seeds.length;i++)if(seeds[i].kind!=='gray')n++;return n;},
  scale:function(){return view.s;},       /* le zoom courant : sert à distinguer un pincement d'un appui long */
  fingers:function(){return Object.keys(ptrs).length;},
  /* la Toile s'eclaircit sous les blocs de texte : a reappliquer des qu'elle bouge */
  applyReserve:function(){
    var R=window.Toile.reserved; if(!R||!R.length||!seeds.length)return;
    var lite=0,bl=-1;
    for(var p=0;p<PAL.length;p++){
      var c=PAL[p], L=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
      if(L>bl){bl=L;lite=p;}
    }
    for(var z=0;z<R.length;z++){
      var rz=R[z];
      for(var py=rz.y-4;py<=rz.y+rz.h+4;py+=6){
        for(var px=rz.x-4;px<=rz.x+rz.w+4;px+=6){
          var bd=1e18,bs=null;
          for(var m=0;m<seeds.length;m++){
            var sm=seeds[m];
            var dd=Math.sqrt((px-sm.x)*(px-sm.x)+(py-sm.y)*(py-sm.y))-sm.w;
            if(dd<bd){bd=dd;bs=sm;}
          }
          if(bs&&bs.kind!=='gray'&&bs.kind!=='nuee'&&bs.pid==null&&bs.ci!==lite){bs.ci=lite;bs.c=PAL[lite];bs.gc=null;}/* ⚑ Q213 : une dalle reliée à un Promi garde SA couleur — la réserve de l'onboarding n'est jamais vidée après lui, elle repeignait en lilas toute dalle passée sous ses anciens textes */
        }
      }
    }
  },
  /* NB : window.Toile.repaint est déjà pris par le Studio — d'où un autre nom */
  redraw:function(){lastChange=performance.now();kick();},
  /* la Toile elle-même : Partager s'en sert pour poster CE QU'ON VOIT.
     Ces deux méthodes étaient appelées par shareToile() mais n'existaient pas :
     le poster retombait sur un vieux rendu mosaïque figé, en « pixel ». */
  canvas:function(){return host;},
  isLight:function(){return isLightM();},
  /* la Toile telle qu'elle est, à l'instant : c'est elle qu'on partage */
  canvas:function(){return host;},
  isLight:function(){return isLightM();},
  /* la couleur EXACTE qu'a la dalle en ce moment sur la Toile */
  colorOf:function(pid){
    for(var i=0;i<seeds.length;i++){
      var s=seeds[i];
      if(s.pid===pid&&s.kind!=='gray'){
        var c=cOf(s,performance.now());
        return 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';
      }
    }
    return null;
  },
  reserve:function(rects){window.Toile.reserved=rects||[];},
  ecarte:function(rects){ _ecZ=(rects&&rects.length)?rects:null; lastChange=performance.now(); kick(); },
  cells:function(){if(!seeds.length)seedGray();return seeds.length;},
  paint:function(n){
    if(!seeds.length)seedGray();
    var T=window.Toile;
    if(!T.paintOrder||T.paintOrder.length!==seeds.length){
      var o=[];for(var i=0;i<seeds.length;i++)o.push(i);
      for(var j=o.length-1;j>0;j--){var r=(Math.random()*(j+1))|0;var t=o[j];o[j]=o[r];o[r]=t;}
      T.paintOrder=o;
    }
    /* la teinte la plus CLAIRE de la palette : c'est elle qui passe sous le texte */
    function _lightest(){
      var best=0,bl=-1;
      for(var p=0;p<PAL.length;p++){
        var c=PAL[p];
        var L=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
        if(L>bl){bl=L;best=p;}
      }
      return best;
    }
    var ord=T.paintOrder,now=performance.now(),changed=0;
    n=Math.max(0,Math.min(ord.length,n|0));
    for(var q=0;q<ord.length;q++){
      var s=seeds[ord[q]];if(!s)continue;
      if(q<n){                                   /* doit etre coloree */
        if(s.kind==='gray'){
          s.kind='promi';s.ci=cc(s);s.c=PAL[s.ci];s.gc=null;
          s.t0=now-900;                 /* sa couleur est là tout de suite : aucun fondu */
          s.w=-9; s.wt=3.4;             /* elle arrive minuscule, puis prend sa place */
          changed++;
        }
      }else{                                     /* doit revenir au gris */
        if(s.kind==='promi'){s.kind='gray';s.gray=grays()[(Math.random()*5)|0];s.ci=null;s.t0=0;s.gc=null;s.w=0;s.wt=0;changed++;}
      }
    }
    /* la Toile RÉAGIT à l'arrivée des dalles puis se stabilise — exactement comme dans l'app */
    /* toute la Toile se réajuste, puis se stabilise — comme dans l'app */
    if(changed){relax();relax();relax();}
    /* aucune dalle bleue ne doit recouvrir les accents bleus du texte (le « i » de Promi,
       le libellé « Promi… ») : leur couleur, elle, ne s'adapte pas. On échantillonne
       vraiment la zone — le centre d'une grande dalle peut être loin tout en la couvrant. */
    /* LA TOILE FAIT DE LA PLACE AU TEXTE : toute dalle qui passe sous un bloc de
       texte prend la teinte la plus claire de la palette. L'encre sombre est alors
       lisible partout, sans jamais rien recalculer. On échantillonne vraiment la
       zone : le centre d'une grande dalle peut être loin d'elle tout en la couvrant. */
    var R=window.Toile.reserved;
    if(R&&R.length){
      var lite=_lightest();
      for(var z=0;z<R.length;z++){
        var rz=R[z];
        for(var py=rz.y-4;py<=rz.y+rz.h+4;py+=5){
          for(var px=rz.x-4;px<=rz.x+rz.w+4;px+=5){
            var bd2=1e18,bs=null;
            for(var m=0;m<seeds.length;m++){
              var sm=seeds[m];
              var dd=Math.sqrt((px-sm.x)*(px-sm.x)+(py-sm.y)*(py-sm.y))-sm.w;
              if(dd<bd2){bd2=dd;bs=sm;}
            }
            if(bs&&bs.kind!=='gray'&&bs.kind!=='nuee'&&bs.pid==null&&bs.ci!==lite){bs.ci=lite;bs.c=PAL[lite];bs.gc=null;}/* ⚑ Q213 : une dalle reliée à un Promi garde SA couleur — la réserve de l'onboarding n'est jamais vidée après lui, elle repeignait en lilas toute dalle passée sous ses anciens textes */
          }
        }
      }
    }
    tones();lastChange=now;kick();
  },
  removePromi:function(){for(var i=seeds.length-1;i>=0;i--){if(seeds[i].kind==='promi'){seeds.splice(i,1);relax();tones();lastChange=performance.now();kick();break;}}},cols:function(){return curPAL();},addNuee:function(key){if(key&&nueeCells[key]&&seeds.indexOf(nueeCells[key])>=0)return nueeCells[key];/* ⚑ 14 sept. : une Nuée qui a déjà sa dalle n'en reçoit pas une seconde */var s=addP('nuee');if(key){nueeCells[key]=s;s.nuee=key;}if(key)nueeCells[key]=s;return s;},addMember:function(key,id){/* ⚑ 14 sept. (Tom) : la dalle d'un Promi planté dans une Nuée est RELIÉE à ce Promi — sans `pid` elle n'avait ni fiche au doigt, ni couleur figée, ni boîte pour sa fiche */var an=(key&&nueeCells[key])?nueeCells[key]:lastNuee;if(!an){var s0=addP('promi');if(s0&&id!=null){s0.pid=id;_dalleFigee(true);}return s0;}var a=Math.random()*6.28,r=avg()*.9;var s=mk(an.x+Math.cos(a)*r,an.y+Math.sin(a)*r,'promi');s.ci=cc(s);s.c=PAL[s.ci];s.t0=performance.now();seeds.push(s);_transPose('arrive',s.x,s.y);if(id!=null)s.pid=id;relax();tones();if(id!=null)_dalleFigee(true);lastChange=s.t0;_vueDefaut();kick();return s;},setTheme:function(t){if(!TH[t])return;var _famAv=_semisNeuf();theme=t;/* ⚑ v35 — changer de FAMILLE de monde ressème la Toile, avec les mêmes promesses */if(_famAv!==_semisNeuf()&&_semisDe){try{var _ids=[];for(var _qi=0;_qi<seeds.length;_qi++){if(seeds[_qi].pid!=null&&seeds[_qi].kind!=='gray')_ids.push(seeds[_qi].pid);}window.Toile.sync(_ids);}catch(_e){}}/* le fond des pages suit le design choisi */try{setTimeout(function(){(window._apresMouvement||function(f){f();})(function(){if(window.auTrame)window.auTrame();if(window.shTrame)window.shTrame();if(window.csDalles)window.csDalles();if(window.shFond)window.shFond();if(window.ixTrame)window.ixTrame();if(window.fdRefresh)window.fdRefresh();if(window.stRefresh)window.stRefresh();if(window.dpRefresh)window.dpRefresh();if(window.esRefresh)window.esRefresh();/* les miniatures de l'Index suivent le design choisi */if(window.peintMinis)window.peintMinis(document.getElementById('indexList'));});},60);}catch(e){}   /* ⚑ v75 : ~400 ms de dalles pour des écrans cachés — ils attendent que le mouvement se pose (l'arrivée de l'aperçu du Studio en est un) */try{localStorage.setItem('promi_monde',t);}catch(e){}   /* le MONDE, pas le mode clair/sombre : deux choses distinctes */seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});lastChange=performance.now();kick();},getTheme:function(){return theme;},setPalette:function(k){if(PALS[k]){palKey=k;hueShift=0;_palLit=null;lastChange=performance.now();try{window.onPaletteChange&&window.onPaletteChange();}catch(e){}kick();}},setHue:function(d){hueShift=+d||0;_palLit=null;lastChange=performance.now();try{window.onPaletteChange&&window.onPaletteChange();}catch(e){}kick();},getPalette:function(){return palKey;},getHue:function(){return hueShift;},   /* ⚑ 20 sept. : le geste de couleur a besoin de LIRE la teinte, pas seulement de l'écrire */palettes:function(){return PALS;},count:function(){return seeds.filter(function(s){return s.kind!=='gray'&&s.part==null;}).length;}};
window.Toile.repaintWorld=function(pcv,w){
  var c=pcv&&pcv.__c; if(!c||!TH[w])return;
  /* ⚑ v69 (Tom, 27 sept.) — ON RESSÈME QUAND ON CHANGE DE FAMILLE. Garder les graines est le geste doux voulu (v25) — mais entre deux
     familles de semis ce n'est plus la même Toile : un monde neuf atteint depuis Encre héritait de la grille de 72 cellules, et
     l'aperçu clairsemé (v55) ne paraissait QUE si le Studio s'ouvrait sur lui. Mesuré : 72 graines sur les vingt mondes du rail. */
  var _AC=window._apercuClair||{};
  if(_apFam(w)!==_apFam(c.th)&&pcv.__vif){ var _F=pcv.__fam||(pcv.__fam={}); _F[_apFam(c.th)]=c; var _gd=_F[_apFam(w)]; if(_gd&&_gd.pw===c.pw&&_gd.ph===c.ph){ pcv.__c=c=_gd; } }   /* v75 : on retrouve le semis de cette famille */
  if(_apFam(w)!==_apFam(c.th)&&window.Toile.preview){ var _av=window._shAllColored; window._shAllColored=true; try{ window.Toile.preview(pcv,w,c.pw,c.ph); }finally{ window._shAllColored=_av; } return; }
  c.th=w;
  /* les gris du monde suivent le THÈME de l'app : en mode clair ce sont les crèmes.
     On prenait la palette sombre du monde quoi qu'il arrive — d'où un Pixel sombre
     alors que le sélecteur affichait Clair. */
  var pal=isLightM()?GLIGHT:TH[w].g;
  c.seeds.forEach(function(s){s.gray=pal[(Math.random()*5)|0];s.gc=null;});
  if(pcv.__vif&&c.vif){ try{ window.Toile.apercuImage(pcv); }catch(_){} return; }   /* v75 : l'aperçu vivant passe au monde suivant dès cette image — son arrivée démarre tout de suite */
  window.Toile.repaint(pcv);
};
/* ⚑ v75 (Tom, 27 sept. 2026) — LES APERÇUS DU STUDIO S'ANIMENT. « Une dalle s'ajoute, une dalle se retire, en boucle, au même
   rythme » que `celebration-mondes.html` : arrivée à 0, départ à 2,4 s, nouvelle arrivée à 4,4 s. Rien d'autre ne change — la vue
   reste entière (1:1), le semis est celui de l'aperçu, le fond celui de l'aperçu.
   ⚑ UN SEUL MOTEUR. L'aperçu n'a pas de copie du mouvement : `Toile.apercuImage` échange l'état du moteur (les graines, la vue, la
   transition, l'horloge du ressort — le patron de `preview`, `repaint`, `renderTo`), fait passer `frame()` UNE image en mode aperçu
   (`_AP`), puis rend l'état de la Toile tel quel. Ressort, poussée, arrivée, départ, `env.trans` : le code de la Toile, au pixel.
   ⚑ LE CYCLE EST PÉRIODIQUE. Une dalle neuve (monde à semis qui grandit) ou une cellule qui se colore (monde à semis constant) arrive
   toujours au même endroit, de la même couleur ; après son départ, les voisines reviennent à leur place (ressort du moteur), et
   chaque arrivée repart de la composition d'origine, exacte. Même Toile à chaque tour : mêmes dalles, même composition. */
var _AP=null, _apVu=null;   /* _apVu : le dernier aperçu vivant (et l'heure de sa dernière image) */
function _apLit(){ return {g:g,W:W,H:H,DPR:DPR,seeds:seeds,theme:theme,view:view,_trans:_trans,_finC:_finC,_finPrev:_finPrev,lastChange:lastChange,_qT0:_qT0,_inert:_inert,vTarget:vTarget,lastNuee:lastNuee,nueeCells:nueeCells,
  ft:frame._t,ftp:frame._tp,fr:frame._redem,ftv:frame._tv,tP:window._tPlante,tM:window._tMouv,me:window._mondeEncore,vm:window._vueMain,rd:window._recadreDemande}; }
function _apPose(e){ g=e.g;W=e.W;H=e.H;DPR=e.DPR;seeds=e.seeds;theme=e.theme;view=e.view;_trans=e._trans;_finC=e._finC;_finPrev=e._finPrev;lastChange=e.lastChange;_qT0=e._qT0;_inert=e._inert;vTarget=e.vTarget;lastNuee=e.lastNuee;nueeCells=e.nueeCells;
  frame._t=e.ft;frame._tp=e.ftp;frame._redem=e.fr;frame._tv=e.ftv;window._tPlante=e.tP;window._tMouv=e.tM;window._mondeEncore=e.me;window._vueMain=e.vm;window._recadreDemande=e.rd; }
/* ⚑ v76 (Tom, 27 sept.) — « Il faut aléatoirement plusieurs ajouts et plusieurs suppressions, sinon la boucle est lassante ; et le
   mouvement plus lent et plus espacé. » L'aperçu ne rejoue plus un aller-retour : chaque dalle de la composition a son EMPLACEMENT
   (sa place et sa couleur de repos), et trois emplacements de plus attendent dans un semis qui grandit. Des événements tirés au hasard
   retirent une dalle présente ou en ramènent une absente, en restant entre −3 et +3 autour de la composition (dans un semis constant,
   jamais au-delà : la densité ne grandit pas). Espacés de 1,8 à 3,2 s de temps d'aperçu, parfois deux presque ensemble. Tout le temps
   de l'aperçu s'écoule à ×0,6 (AP_LENT) : ressort, poussée, transitions des mondes — le même mouvement, plus lent.
   Après chaque événement, quand il s'est posé, les dalles reviennent à leur emplacement : la composition ne dérive pas. */
var AP_LENT=1, AP_ECART=[3000,5300], AP_SERRE=[800,1500], AP_POSE=2300;   /* ⚑ v83 (Tom : « les mouvements au Studio sont devenus lents, comme s'ils chargeaient ») — le ralenti ×0,6 de v76 retiré : les mondes y ont leur rythme validé ; l'espacement réel des événements est gardé (3 à 5,3 s) */
function _apCle(x,y){ var t='v\u0000'+Math.round(x)+'\u0000'+Math.round(y), h=0x811c9dc5; for(var i=0;i<t.length;i++){ h^=t.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return h>>>0; }   /* la clé de repli des mondes neufs, prise UNE fois, au repos */
function _apCopie(s){ var o={}; for(var k in s) if(Object.prototype.hasOwnProperty.call(s,k)) o[k]=s[k]; return o; }
function _apRemet(c){ c.prochain=null;   /* la composition d'origine, exacte ; les gris restent ceux du monde affiché (repaintWorld les tire) */
  var gr={}; seeds.forEach(function(s){ if(s._b!=null) gr[s._b]=[s.gray,s.gc]; });
  var out=c.base.map(function(b){ var s=_apCopie(b); var q=gr[s._b]; if(q){ s.gray=q[0]; s.gc=q[1]; } else { s.gray=grays()[(Math.random()*5)|0]; s.gc=null; } s.px=s.x; s.py=s.y; return s; });
  seeds.length=0; Array.prototype.push.apply(seeds,out); _trans=null; _finC=null; _finPrev=null; }
/* les trois emplacements de plus d'un semis qui grandit : tirés une fois, sur la composition d'origine */
function _apExtras(c){ if(c.extras) return c.extras; c.extras=[];
  for(var i=0;i<3;i++){ var p=ipos(), s=mk(p.x,p.y,'promi'); seeds.push(s); var ci=cc(s); seeds.pop(); c.extras.push({pos:[p.x,p.y],ci:ci,w:3.4,cle:_apCle(p.x,p.y)}); }
  return c.extras; }
function _apPresent(s){ return s.kind!=='gray'&&s.part==null; }
function _apMasque(c){ var B=c.base.length, m=[], i; for(i=0;i<B;i++) m.push('0'); var X=[0,0,0];
  seeds.forEach(function(s){ if(!_apPresent(s)) return; if(s._b!=null) m[s._b]='1'; else if(s._x!=null) X[s._x]=1; });
  return m.join('')+(_semisNeuf()?X.join(''):''); }
function _apMasqueBase(c){ var m=''; for(var i=0;i<c.base.length;i++) m+='1'; return m+(_semisNeuf()?'000':''); }
/* une dalle arrive à son emplacement : `b` (la composition) ou `x` (un emplacement de plus) */
function _apAjoute(c,sl,now){ var s;
  if(_semisNeuf()){
    var P=sl.x!=null?c.extras[sl.x]:null, b=sl.b!=null?c.base[sl.b]:null, pos=P?P.pos:[b.x,b.y];
    s=mk(pos[0],pos[1],'promi'); s.ci=P?P.ci:b.ci; s.c=PAL[s.ci]; s.t0=now; s.apercu=1; s._cleAp=P?P.cle:b._cleAp;
    if(P) s._x=sl.x; else s._b=sl.b;
    var wf=P?P.w:b.w; s.w=-22; s.wt=Math.max(12,wf); s.wFin=wf; s.wAt=now+380;
    if(RD[theme]&&RD[theme].sansPoussee){ s.w=s.wFin; s.wt=s.wFin; s.wAt=0; }
    if(RD[theme]&&RD[theme].douce){ s.wt=s.wFin; s.wAt=0; }
    seeds.push(s); _transPose('arrive',s.x,s.y);
  } else {   /* Toile.plantOne : la cellule repliée regrandit à sa place, de sa couleur d'origine, en poussant ses voisines */
    var k=-1, i; for(i=0;i<seeds.length;i++) if(seeds[i]._b===sl.b){ k=i; break; } if(k<0) return;
    var v=seeds[k], bb=c.base[sl.b];
    s=mk(v.x,v.y,'promi'); s._b=sl.b; s.apercu=1; s.ci=bb.ci; s.c=bb.c; s.t0=now; s.w=v.w; s.wt=12; s.wFin=bb.w||0; s.wAt=now+380; s.tx=bb.x; s.ty=bb.y;
    if(RD[theme]&&RD[theme].douce){ s.wt=s.wFin; s.wAt=0; }
    s.gray=v.gray; s.gc=v.gc; s.tone=v.tone; s.shade=v.shade; s.ang=v.ang; s.ph=v.ph; s.am=v.am; s.px=v.px; s.py=v.py;
    if(theme==='encre'||theme==='touffe') window._tPlante=now;
    seeds[k]=s;   /* au rang de la cellule : un motif tiré du rang ne se rebat pas */
  }
  relax(); tones(); lastChange=now; }
/* une dalle présente s'en va : dans un semis qui grandit elle se retire (v43) ; dans un semis constant elle se replie (v76) */
function _apRetire(c,s,now){ var k=seeds.indexOf(s); if(k<0) return;
  if(_semisNeuf()){
    if(RD[theme]&&RD[theme].transDur){ s.part=now; s.partPid=null; s.partNuee=null; s.wt=s.w-30; s.wFin=s.wt; s.wAt=0; if(RD[theme].sansPoussee) s.w=s.wt; _transPose('depart',s.x,s.y); }
    else seeds.splice(k,1);
  } else { _replie(s,now); }   /* au Studio, tout semis constant replie (Houle et Taille-douce compris) */
  relax(); relax(); relax(); tones(); lastChange=now; }
/* quand l'événement s'est posé : chaque dalle retourne à son emplacement */
function _apRetourne(c){ var ex=c.extras||[];
  seeds.forEach(function(s){ if(s.part!=null) return; var q=s._b!=null?c.base[s._b]:(s._x!=null?ex[s._x]:null); if(!q) return;
    var x=q.x!=null?q.x:q.pos[0], y=q.y!=null?q.y:q.pos[1]; s.tx=x; s.ty=y; if(s.kind!=='gray'){ s.wt=s.wFin=(q.w!=null?q.w:3.4); s.wAt=0; } });
  lastChange=performance.now(); }
function _apEvenement(c,now,premier){ var neuf=_semisNeuf(), B=c.base.length; if(neuf) _apExtras(c);
  var pres=[], abs=[], vus={}, i;
  seeds.forEach(function(s){ if(s._b!=null) vus['b'+s._b]=s; else if(s._x!=null) vus['x'+s._x]=s; if(_apPresent(s)) pres.push(s); });
  var nds=(theme==='madrure');   /* v79 : dans Madrure seuls les nœuds font l'onde */
  if(nds) pres=pres.filter(function(s){ return s._nd||s._x!=null; });
  for(i=0;i<B;i++){ if(nds&&!c.base[i]._nd) continue; var sb=vus['b'+i]; if(!sb||(!neuf&&sb.kind==='gray')) abs.push({b:i}); }
  if(neuf) for(i=0;i<3;i++) if(!vus['x'+i]) abs.push({x:i});
  var Bn=nds?10:B, n=pres.length, min=Bn-3, max=neuf?Bn+3:Bn, peutA=abs.length&&n<max, peutR=pres.length&&n>min;
  /* la première, tout de suite : un semis qui grandit reçoit son premier emplacement de plus (celui que Ramage et Volubilis
     préparent d'avance) ; un semis constant replie une dalle */
  if(premier){ if(neuf&&peutA){ _apAjoute(c,{x:0},now); c.prochain={th:theme,D:_apTire(c)}; return; } if(peutR){ _apRetire(c,pres[(Math.random()*pres.length)|0],now); c.prochain={th:theme,D:_apTire(c)}; return; } }
  /* ⚑ v89 — l'événement suivant est TIRÉ D'AVANCE (c.prochain), juste après celui-ci : un monde qui prépare son arrivée (Ramage) la
     prépare pendant le repos, et l'événement ne vient qu'une fois elle prête — il glisse dès sa première image, dans sa vraie forme. */
  var D=(c.prochain&&c.prochain.th===theme)?c.prochain.D:_apTire(c); c.prochain=null;
  if(D&&D.a){ var e=D.a; if(!(e.b!=null&&neuf&&vus['b'+e.b])&&!(e.x!=null&&vus['x'+e.x]&&_apPresent(vus['x'+e.x]))) _apAjoute(c,e,now); }
  else if(D&&D.r){ var sr=vus[D.r]; if(sr&&_apPresent(sr)&&pres.indexOf(sr)>=0) _apRetire(c,sr,now); }
  c.prochain={th:theme,D:_apTire(c)}; }
function _apTire(c){ var neuf=_semisNeuf(), B=c.base.length, pres=[], abs=[], vus={}, i;
  seeds.forEach(function(s){ if(s._b!=null) vus['b'+s._b]=s; else if(s._x!=null) vus['x'+s._x]=s; if(_apPresent(s)) pres.push(s); });
  var nds=(theme==='madrure'); if(nds) pres=pres.filter(function(s){ return s._nd||s._x!=null; });
  for(i=0;i<B;i++){ if(nds&&!c.base[i]._nd) continue; var sb=vus['b'+i]; if(!sb||(!neuf&&sb.kind==='gray')) abs.push({b:i}); }
  if(neuf) for(i=0;i<3;i++) if(!vus['x'+i]) abs.push({x:i});
  var Bn=nds?10:B, n=pres.length, min=Bn-3, max=neuf?Bn+3:Bn, peutA=abs.length&&n<max, peutR=pres.length&&n>min;
  if(peutA&&(!peutR||Math.random()<0.5)) return {a:abs[(Math.random()*abs.length)|0]};
  if(peutR){ var s=pres[(Math.random()*pres.length)|0]; return {r:s._b!=null?'b'+s._b:'x'+s._x}; }
  return null; }
var _apSemN=0;
function _apBase(c){ if(c.base) return; c.semId=++_apSemN;
  c.seeds.forEach(function(s){ s._cleAp=_apCle(s.x,s.y); });
  var nd=c.seeds.slice().sort(function(a,b){ return a._cleAp-b._cleAp; }).slice(0,10); nd.forEach(function(s){ s._nd=1; });   /* v79 : les dix nœuds d'un aperçu de Madrure (v40) */
  c.base=c.seeds.map(function(s,i){ s._b=i; if(s.tx==null){ s.tx=s.x; s.ty=s.y; } if(s.wt==null) s.wt=s.w||0; if(s.wFin==null) s.wFin=s.wt; s.wAt=0; s.w=s.w||0; return _apCopie(s); }); }
/* ⚑ v92 (Tom, 28 sept. : « feu vert pour préparer le film avant le geste. Tu peux toucher au moteur pour tirer la couleur et la place
   à l'avance ») — LA PLANTATION SIMULÉE. Sur des COPIES des graines, avec un tirage semé (`g0`), on joue la plantation (ou le retrait)
   telle que le vrai geste la jouera, et le monde prépare ce qu'il lui faut (Ramage : le film de la pousse). Tout l'état du moteur est
   rendu à l'identique (`_apLit`/`_apPose`, `_transN`, la couleur figée des paroles). Le tirage est GARDÉ : la vraie plantation, si la
   Toile n'a pas bougé entre-temps (`_simSig`), tire la même place et la même couleur — sinon elle tire comme avant, et le monde
   retombe sur sa lecture progressive. */
var _simRand=null;
function _lcgSim(g0){ var s=(g0>>>0)||1; return function(){ s=(Math.imul(s,1103515245)+12345)&0x7fffffff; return s/0x7fffffff; }; }
function _simSig(){ var h=2166136261; for(var i=0;i<seeds.length;i++){ var s=seeds[i]; h^=(Math.round(s.x*2)*7+Math.round(s.y*2)*13+((s.ci|0)+1)*17+(s.part!=null?991:0)+(s.pid!=null?(s.pid|0)%9973:0))|0; h=Math.imul(h,16777619)>>>0; } return h+':'+seeds.length+':'+theme; }
window.Toile.simule=function(ajouts,retraits,fn){
  if(!_semisNeuf()||!g||_AP||window._simOff) return false;
  var M=_apLit(), tn=_transN, mr=Math.random, sig=_simSig(), faux=[], dal=[], r=false;
  var g0=(_simRand&&_simRand.sig===sig&&_simRand.used===0&&_simRand.n===(ajouts?ajouts.length:0))?_simRand.g0:((mr()*2147483600)|0)+1;   /* la Toile n'a pas bougé : le MÊME tirage (un film déjà préparé reste juste) */
  var copie=seeds.map(function(s){ var c={}; for(var k in s) c[k]=s[k]; return c; });
  try{
    promises.forEach(function(p){ dal.push([p,p.dalle]); });
    _apPose(Object.assign({},M,{seeds:copie,view:{s:M.view.s,ox:M.view.ox,oy:M.view.oy},nueeCells:Object.assign({},M.nueeCells)}));
    if(ajouts&&ajouts.length){ Math.random=_lcgSim(g0);
      ajouts.forEach(function(a,i){ var id=a.id; if(id==null){ var f={id:-(9e8+i),title:a.title||'',who:a.who||'moi',chiche:!!a.chiche,draft:false}; promises.push(f); faux.push(f); id=f.id; } _addPromiNu(id); });
      Math.random=mr; }
    if(retraits&&retraits.length) window.Toile.sync(promises.filter(function(q){ return !q.draft&&retraits.indexOf(q.id)<0; }).map(function(q){ return q.id; }));
    var tv=_transVive; _transVive=true; try{ r=fn?fn():true; } finally{ _transVive=tv; }   /* comme pendant une image de la Toile : le monde est vivant (places gardées, papier de la Toile) */
  }catch(e){ window._simErr=String(e&&e.stack||e); r=false; }
  finally{ Math.random=mr; for(var fi=promises.length-1;fi>=0;fi--) if(faux.indexOf(promises[fi])>=0) promises.splice(fi,1); dal.forEach(function(d){ d[0].dalle=d[1]; }); _apPose(M); _transN=tn; }
  if(ajouts&&ajouts.length) _simRand={f:_lcgSim(g0),g0:g0,sig:sig,n:ajouts.length,used:0,t:performance.now()};
  return r; };
window.Toile.ancrePid=function(pid){ var s=null; for(var i=0;i<seeds.length;i++) if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){ s=seeds[i]; break; } if(!s) return null; var a=null; try{ a=(RD[theme]&&RD[theme].ancre)?RD[theme].ancre(s):null; }catch(_){ } return a?[a[0],a[1]]:[s.x,s.y]; };   /* v93 : pour les juges — où le monde pose la parole (l'œil de Ramage, la fleur de Volubilis) */
/* ⚑ v97 (Tom, iPhone : « Halin avec une seule dalle : elle prend tout l'écran, on ne comprend rien. Il en faut au moins deux autres, non
   choisies, pour qu'on voie la structure. À partir de deux paroles, le principe reprend ») — la Toile de Halin est faite de ses paroles :
   à une parole, une seule cellule. On lui adjoint DEUX cellules neutres (des graines grises, que Halin sait peindre — la Toile vide du
   §10.6), au plus grand vide (`_auVide`, tiré de la clé de la Toile : même Toile, même place), au poids d'une parole. Leur aspect vient de
   leur rang, jamais du hasard. Dès deux paroles, elles partent. Zéro parole : le semis de la Toile vide reste tel quel. */
function _compagnonsHalin(){
  if(theme!=='halin'||_AP) return false;
  var n=0, comp=[]; for(var i=0;i<seeds.length;i++){ var s=seeds[i]; if(s.compagnon) comp.push(s); else if(s.kind!=='gray'&&s.part==null) n++; }
  if(n===1){ if(comp.length===2) return false;
    seeds=seeds.filter(function(s){ return !s.compagnon; });
    for(var k=0;k<2;k++){ var q=_auVide(90+k), g=mk(q.x,q.y,'gray'); g.compagnon=1; g.gray=grays()[(k*2+1)%grays().length]; g.tone=TON[(k+1)%TON.length]; g.shade=1; g.ang=0.9+1.7*k; g.ph=1.3+2.1*k; g.am=1;
      g.w=3.4; g.wt=3.4; seeds.push(g); }
    window.Toile.paintOrder=null; try{ relax(); }catch(_){ } kick(); return true; }
  if(comp.length){ seeds=seeds.filter(function(s){ return !s.compagnon; }); window.Toile.paintOrder=null; try{ relax(); }catch(_){ } kick(); return true; }
  return false; }
window._compagnonsHalin=_compagnonsHalin;
(function(){ ['addPromi','sync','setTheme','removePromi'].forEach(function(nom){ var f=window.Toile[nom]; if(typeof f!=='function') return;
  window.Toile[nom]=function(){ var r=f.apply(this,arguments); try{ _compagnonsHalin(); }catch(_){ } return r; }; }); })();
window._simOublie=function(){ var a=!!_simRand; _simRand=null; return a; };   /* pour les juges : le tirage oublié, la prédiction manquée */
var _addPromiNu=window.Toile.addPromi;
window.Toile.addPromi=function(id){ var R=_simRand;
  if(R&&R.used===0&&(R.sig!==_simSig()||performance.now()-R.t>120000)) R=_simRand=null;
  if(!R) return _addPromiNu.apply(this,arguments);
  var mr=Math.random; Math.random=R.f; try{ return _addPromiNu.apply(this,arguments); } finally{ Math.random=mr; if(++R.used>=R.n) _simRand=null; } };
/* les trois moments où l'on sait ce qui va arriver : la phrase qui s'écrit (pause de 700 ms), le trait de la plantation, la
   confirmation d'une suppression. Ramage et Volubilis : les deux mondes dont l'arrivée se calcule. */
(function(){
  function ramage(){ return !!(RD[theme]&&RD[theme].prepareToile); }   /* v92 : Ramage et Volubilis — les mondes qui savent préparer */
  function prepare(ajouts,retraits){ if(!ramage()) return false; var th=theme; return window.Toile.simule(ajouts,retraits,function(){ return RD[th].prepareToile(); }); }
  window._simPrepare=prepare;
  function formulaire(){ var t=((document.getElementById('fTitle')||{}).value||'').trim(); if(!t) return null;
    var rc=(typeof window.newWhoSel!=='undefined'&&window.newWhoSel&&window.newWhoSel.length)?window.newWhoSel.slice():[];
    if(!rc.length){ var ty=((document.getElementById('fWho')||{}).value||'').trim(); if(ty&&ty.toLowerCase()!=='moi'&&ty.indexOf(',')<0) rc=[ty]; }
    if(!rc.length) rc=['moi']; if(rc.length>1) rc=rc.filter(function(r){ return r&&r!=='moi'; });
    var ch=!!(window._phrase&&window._phrase.sens==='chiche');
    return rc.map(function(w){ return {title:t,who:w,chiche:ch}; }); }
  var tmr=null, der='';
  function planifie(){ clearTimeout(tmr); tmr=setTimeout(function(){ var cs=document.getElementById('createSheet'); if(!cs||!cs.classList.contains('show')||!ramage()) return;
      if((cs.getAttribute('data-kind')||'promi')!=='promi'||(typeof selNuee!=='undefined'&&selNuee)) return;
      var A=formulaire(); if(!A) return; var cle=JSON.stringify(A); if(cle===der&&_simRand) return;
      if(RD[theme].filmEnCours&&RD[theme].filmEnCours()){ planifie(); return; }   /* un film déjà en calcul : on attend qu'il finisse */
      der=cle; prepare(A,null); },700); }
  document.addEventListener('input',function(e){ if(e.target&&(e.target.id==='fTitle'||e.target.id==='fWho')) planifie(); },true);
  document.addEventListener('pointerup',function(e){ if(e.target&&e.target.closest&&e.target.closest('#createSheet')) planifie(); },true);
  /* le trait : les paroles viennent d'être créées (promises), la Toile ne les a pas encore — on prépare avec les VRAIES */
  function enveloppe(){ if(window.printTirage&&window.printTirage.__sim) return; var pt=window.printTirage; if(typeof pt==='function'){ window.printTirage=function(){ var r=pt.apply(this,arguments);
    setTimeout(function(){ try{ if(!ramage()) return; var sur={}; seeds.forEach(function(s){ if(s.pid!=null) sur[s.pid]=1; });
      var A=promises.filter(function(p){ return !p.draft&&!p.nuee&&!sur[p.id]; }).map(function(p){ return {id:p.id}; }); if(A.length) prepare(A,null); }catch(_){ } },0);
    return r; }; window.printTirage.__sim=true; }
  var sp=window._v16SupprimerPromi; if(typeof sp==='function'&&!sp.__sim){ window._v16SupprimerPromi=function(p){ var r=sp.apply(this,arguments);
    try{ var q=p||(typeof cur!=='undefined'?cur:null); if(q&&!q.draft) prepare(null,[q.id]); }catch(_){ } return r; }; window._v16SupprimerPromi.__sim=true; } }
  window.addEventListener('load',function(){ setTimeout(enveloppe,0); });   /* les deux portes sont définies plus loin dans le fichier */
}());   /* ⚑ jamais « })(); » en début de ligne ici : redteam_decoupe y lit la fin du moteur */
function _apCycle(c,now){ var cy=c.cy;
  if(!cy||cy.th!==c.th){   /* un monde neuf à l'écran : la composition d'origine, et le premier événement TOUT DE SUITE */
    if(cy) _apRemet(c);
    cy=c.cy={th:c.th,suiv:now+60,pose:0,n:0};
    /* ⚑ v90 — Ramage : son premier événement (un emplacement de plus) est tiré d'avance comme les suivants — il attend son plumage
       et le film de sa pousse, 4 s au plus comme les suivants (la composition au repos, comme entre deux événements), puis part comme avant */
    if(c.th==='ramage'&&_semisNeuf()&&!window._ramFilmOff){ c.prochain={th:'ramage',D:{a:{x:0}}}; cy.n=1; cy.prem=now; } }   /* v80 : une image de la composition d'abord — un monde qui anime ses éclats (Esquille) doit savoir d'où ils partent */
  if(theme==='ramage'&&window._apOccupe&&now>=cy.suiv){ cy.suiv=now+120; return; }
  if(theme==='volubilis'&&window._volBouge&&now>=cy.suiv){ cy.suiv=now+60; return; }   /* v91 : Volubilis finit son tissage avant l'événement suivant */   /* v87 : Ramage finit son glissé avant l'événement suivant */
  if(theme==='ramage'&&now>=cy.suiv&&c.prochain&&c.prochain.th==='ramage'&&(!c.prochain.pret||(window._ramPret&&!window._ramPret(c.prochain.K)))){ if(!cy.att) cy.att=now; if(now-cy.att<8000){ cy.suiv=now+(cy.prem&&cy.n===1?30:60); return; } }   /* v90 : on attend le film (8 s au plus) plutôt que de pousser par étapes */   /* v89 : l'événement tiré d'avance n'est pas encore prêt */
  if(now>=cy.suiv) cy.att=0;
  if(now>=cy.suiv){ _apEvenement(c,now,cy.n===0); cy.n++; cy.pose=now+AP_POSE;
    var serre=Math.random()<0.3, E=serre?AP_SERRE:AP_ECART; cy.suiv=now+E[0]+Math.random()*(E[1]-E[0]); if(cy.suiv<cy.pose&&!serre) cy.pose=cy.suiv; return; }
  if(cy.pose&&now>=cy.pose){ cy.pose=0; _apRetourne(c); } }
/* une image de l'aperçu vivant — rend vrai tant qu'il reste du mouvement (il en reste toujours : le cycle ne s'arrête pas) */
var _pnVrai=performance.now.bind(performance);
window.Toile.apercuImage=function(pcv){ var c=pcv&&pcv.__c; if(!c||!RD[c.th]) return false;
  /* v76 — l'aperçu a sa propre horloge, à ×0,6 (AP_LENT) : TOUT ce qui se lit dans l'image (performance.now, le ressort, les
     transitions des mondes) avance moins vite. Une image de plus de 250 ms (une pause) ne compte que pour une image. */
  var rv=_pnVrai(); if(c.vt==null){ c.vt=rv; c.rt=rv; } var dr=rv-c.rt; if(dr>250) dr=16.7; c.vt+=dr*AP_LENT; c.rt=rv; var vt0=c.vt, rt0=rv;
  performance.now=function(){ return vt0+(_pnVrai()-rt0)*AP_LENT; };
  var now=vt0;   /* une seule horloge : l'heure d'une image (rAF) peut précéder celle du clic qui a changé de monde */
  var M=_apLit(), ok=false;
  try{
    if(!c.etat||c.etat.seeds!==c.seeds||c.etat.g.canvas!==pcv){
      _apBase(c);
      c.etat={g:pcv.getContext('2d'),W:c.pw,H:c.ph,DPR:pcv.width/c.pw,seeds:c.seeds,theme:c.th,view:{s:1,ox:0,oy:0},_trans:null,_finC:null,_finPrev:null,lastChange:0,_qT0:0,_inert:null,vTarget:null,lastNuee:null,nueeCells:{},
        ft:undefined,ftp:undefined,fr:1,ftv:undefined,tP:0,tM:0,me:false,vm:false,rd:false}; }
    c.etat.theme=c.th; c.etat.seeds=c.seeds; c.etat.view={s:1,ox:0,oy:0};
    _apPose(c.etat); _AP=c; c.vif=true; var _rtA=_rtCible; _rtCible=pcv; window._apImage=true;   /* la Toile entière, vue 1:1 : les calques de Touffe et de Houle s'y posent (le patron de renderTo) */
    _apCycle(c,now); window._apPhase=c.semId+'|'+_apMasque(c); window._apPhaseBase=c.semId+'|'+_apMasqueBase(c);   /* l'état de l'aperçu : quelles dalles sont là */
    frame(now); ok=true; _apVu=c; c.tImg=rt0;
  }catch(e){ window._apErreur=String(e&&e.stack||e); }
  finally{ performance.now=_pnVrai; _AP=null; window._apImage=false; if(typeof _rtA!=='undefined') _rtCible=_rtA; try{ c.etat=_apLit(); c.seeds=c.etat.seeds; }catch(_){ } _apPose(M); }
  return ok; };
/* ⚑ v75 — LA PRÉPARATION À L'AVANCE (Ramage, Volubilis). Deux mondes ne savent pas montrer leur arrivée tout de suite : Ramage peint
   son plumage d'arrivée par tranches (0,9 à 1 s), Volubilis construit son jardin (0,5 à 1,3 s, d'un bloc à la première image). Tant que
   l'aperçu montre un autre monde du même semis, on leur fait préparer, par petites tranches et sur un canevas caché de la même taille,
   les deux états que leur arrivée lira : le repos (la composition d'origine) et l'arrivée (la dalle neuve à sa place). Même état du
   moteur que l'arrivée réelle — mêmes graines, même dalle neuve, même transition — donc mêmes signatures : à l'arrivée, ils trouvent
   ce qu'ils cherchent. Un monde qui n'a pas `RD[m].prepare` n'a rien à préparer. */
var _apPrepCv=null;
function _apFam(th){ return (window._apercuClair&&window._apercuClair[th])?'clair':'grille'; }
window.Toile.apercuPrepare=function(pcv,monde,budget){
  if(!RD[monde]||!RD[monde].prepare) return true;
  var F=pcv.__fam||{}, cc0=pcv.__c, c=(cc0&&_apFam(cc0.th)===_apFam(monde))?cc0:F[_apFam(monde)]; if(!c) return false;
  var cle=monde+'|'+_apFam(monde)+'|'+palKey+'|'+hueShift+'|'+isLightM(); c.prep=c.prep||{};   /* une autre palette, un autre thème : d'autres couleurs, on reprépare */ if(c.prep[cle]) return true;
  if(!_apPrepCv) _apPrepCv=document.createElement('canvas');
  if(_apPrepCv.width!==pcv.width) _apPrepCv.width=pcv.width; if(_apPrepCv.height!==pcv.height) _apPrepCv.height=pcv.height;
  var M=_apLit(), fini=false, now=performance.now(), tv=_transVive, rt=_rtCible;
  try{
    _apBase(c);
    var pal=isLightM()?GLIGHT:TH[monde]?TH[monde].g:null;
    var sb=c.base.map(function(b){ var s=_apCopie(b); s.px=s.x; s.py=s.y; return s; });
    var e={g:_apPrepCv.getContext('2d'),W:c.pw,H:c.ph,DPR:_apPrepCv.width/c.pw,seeds:sb,theme:monde,view:{s:1,ox:0,oy:0},_trans:null,_finC:null,_finPrev:null,lastChange:0,_qT0:0,_inert:null,vTarget:null,lastNuee:null,nueeCells:{},ft:undefined,ftp:undefined,fr:1,ftv:undefined,tP:0,tM:0,me:false,vm:false,rd:false};
    _apPose(e); _AP=c; _transVive=true; _rtCible=_apPrepCv; window._apImage=true;
    g.setTransform(DPR,0,0,DPR,0,0);
    var d=null; if(_semisNeuf()){ var X0=_apExtras(c)[0]; d={x:X0.pos[0],y:X0.pos[1]}; }
    _transPose('arrive',d?d.x:c.pw/2,d?d.y:c.ph/2);   /* le repos se lit comme à l'arrivée réelle : transition en cours, sans la dalle neuve */
    window._apPhase=window._apPhaseBase=c.semId+'|'+_apMasqueBase(c); var t0=performance.now(), a=RD[monde].prepare(now,budget,1), b=false;
    if(a&&d&&performance.now()-t0<budget){ _apAjoute(c,{x:0},now); _finC=null; window._apPhase=c.semId+'|'+_apMasque(c); b=RD[monde].prepare(now,Math.max(1,budget-(performance.now()-t0)),2); }
    fini=!!(a&&(b||!d));
  }catch(err){ window._apErreur=String(err&&err.stack||err); fini=true; }
  finally{ _AP=null; window._apImage=false; _transVive=tv; _rtCible=rt; _apPose(M); }
  if(fini) c.prep[cle]=true;
  return fini; };
/* ⚑ v89 — préparer L'ÉVÉNEMENT TIRÉ D'AVANCE du monde affiché (Ramage), sur une copie des graines : son plumage d'arrivée se construit
   pendant le repos ; le monde en prépare ensuite la matière et les empreintes (son propre repos). */
window.Toile.apercuPrepareProchain=function(pcv,budget){ var c=pcv&&pcv.__c; if(!c||!c.vif||!c.base||!RD[c.th]||!RD[c.th].prepare) return true;
  var P=c.prochain; if(!P||!P.D||P.th!==c.th||P.pret) return true;
  if(!_apPrepCv) _apPrepCv=document.createElement('canvas');
  if(_apPrepCv.width!==pcv.width) _apPrepCv.width=pcv.width; if(_apPrepCv.height!==pcv.height) _apPrepCv.height=pcv.height;
  var M=_apLit(), fini=false, now=performance.now(), tv=_transVive, rt=_rtCible, ph=window._apPhase, phb=window._apPhaseBase;
  try{
    var sb=c.seeds.map(function(s){ var q=_apCopie(s); if(q.px==null) q.px=q.x; if(q.py==null) q.py=q.y; return q; }), vus={};
    sb.forEach(function(s){ if(s._b!=null) vus['b'+s._b]=s; else if(s._x!=null) vus['x'+s._x]=s; });
    var e={g:_apPrepCv.getContext('2d'),W:c.pw,H:c.ph,DPR:_apPrepCv.width/c.pw,seeds:sb,theme:c.th,view:{s:1,ox:0,oy:0},_trans:null,_finC:null,_finPrev:null,lastChange:0,_qT0:0,_inert:null,vTarget:null,lastNuee:null,nueeCells:{},ft:undefined,ftp:undefined,fr:1,ftv:undefined,tP:0,tM:0,me:false,vm:false,rd:false};
    _apPose(e); _AP=c; _transVive=true; _rtCible=_apPrepCv; window._apImage=true; g.setTransform(DPR,0,0,DPR,0,0);
    if(!P.fait){ if(P.D.a&&P.D.a.x!=null&&_semisNeuf()) _apExtras(c);   /* v90 : le premier événement (x:0) lit les emplacements de plus */
      if(P.D.a) _apAjoute(c,P.D.a,now); else if(P.D.r&&vus[P.D.r]) _apRetire(c,vus[P.D.r],now); _finC=null; P.K=c.semId+'|'+_apMasque(c); P.seeds=sb; P.e=e; P.fait=true; }
    else { _apPose(P.e); }
    window._apPhase=P.K; window._apPhaseBase=phb;
    fini=RD[c.th].prepare(now,budget,2,true);
    P.e=_apLit();
  }catch(err){ window._apErreur=String(err&&err.stack||err); fini=true; }
  finally{ _AP=null; window._apImage=false; _transVive=tv; _rtCible=rt; _apPose(M); window._apPhase=ph; window._apPhaseBase=phb; }
  if(fini) P.pret=true;
  return fini; };
/* le semis de l'autre famille, composé d'avance (sans rien peindre) : un doigt qui saute d'une famille à l'autre retrouve un semis préparé */
window.Toile.apercuCompose=function(pcv,monde){ var F=pcv.__fam||(pcv.__fam={}), f=_apFam(monde); if(F[f]) return F[f];
  var cv=document.createElement('canvas'); cv.width=pcv.width; cv.height=pcv.height; cv.__compose=true;
  var av=window._shAllColored; window._shAllColored=true; try{ window.Toile.preview(cv,monde,pcv.__c?pcv.__c.pw:390,pcv.__c?pcv.__c.ph:844); }finally{ window._shAllColored=av; }
  if(cv.__c){ F[f]=cv.__c; } return F[f]||null; };
function _apMasqueLu(c){ var B=c.base?c.base.length:0, m=[], X=[0,0,0], i; for(i=0;i<B;i++) m.push('0'); c.seeds.forEach(function(s){ if(s.kind==='gray'||s.part!=null) return; if(s._b!=null) m[s._b]='1'; else if(s._x!=null) X[s._x]=1; }); return m.join('')+'·'+X.join(''); }
/* l'aperçu cesse de vivre : `repaint` peint de nouveau (fixe) */
window.Toile.apercuArret=function(pcv){ var c=pcv&&pcv.__c; if(c) c.vif=false; };
/* lecture seule, pour les juges : où en est le cycle */
window.Toile.apercuEtat=function(pcv){ var c=pcv&&pcv.__c; if(!c||!c.cy) return null; var n=0; c.seeds.forEach(function(s){ if(s.kind!=='gray') n++; });
  return {monde:c.th, tour:c.cy.n, masque:_apMasqueLu(c), graines:c.seeds.length, colorees:n, base:c.base?c.base.length:0, vif:!!c.vif}; };
window.Toile.resetView=function(){view={s:1,ox:0,oy:0};vTarget=null;};
/* ⚑ Cercle · LA COULEUR (Tom 13 sept.) — relire les couleurs choisies, et donner les quatre tons d'une palette du Studio (teinte comprise). */
window.Toile.refigeCouleurs=function(){_dalleFigee(false);lastChange=performance.now();kick();};
window.Toile.colorOfNuee=function(k){for(var i=0;i<seeds.length;i++){var s=seeds[i];if(s.kind==='nuee'&&s.nuee===k){var c=cOf(s,performance.now());return 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';}}return null;};   /* lecture seule */
window.Toile.tonsDe=function(k,h){var b=(PALS[k]||PALS[palKey]).cols;h=+h||0;return b.map(function(c){return h?rotc(c,h):[c[0],c[1],c[2]];});};
/* CHANTIER 1 — rend la VRAIE Toile hors ecran : memes germes, memes positions,
   meme monde. Contrairement a preview(), qui regenere une grille aleatoire.
   Meme patron que repaint() : on echange les globales, on peint, on restaure. */
window.Toile.renderTo=function(cv,ech,clair){
  if(!cv||!cv.getContext)return false;
  if(!seeds.length){try{seedGray();}catch(e){}}
  ech=ech||2;
  var _g=g,_W=W,_H=H,_v={s:view.s,ox:view.ox,oy:view.oy};
  var _ov=window._shThemeOverride;
  var ok=false;
  /* ⚑ v29 — `DPR` VAUT `ech` LE TEMPS DU RENDU. Six mondes remplacent la transformation par `setTransform(DPR…)`
     (CONTRAT-MONDE §11) : tant que renderTo n'était appelé qu'à la densité de la Toile, ça ne se voyait pas. Rendue
     à l'échelle exacte de l'export (redteam_decoupe, famille D), la Toile se peignait à la densité 2 dans un canevas
     de densité 5,5 — petite, dans un coin. Mesuré : écart export/aperçu 112 niveaux. */
  var _dpr0=DPR;
  try{
    DPR=ech;
    cv.width=Math.max(2,Math.round(W*ech));
    cv.height=Math.max(2,Math.round(H*ech));
    g=cv.getContext('2d'); if(!g)throw 0;
    if(clair!=null)window._shThemeOverride=!!clair;
    view={s:1,ox:0,oy:0};                 /* Toile entiere, sans cadrage */
    g.setTransform(ech,0,0,ech,0,0);
    g.clearRect(0,0,W,H);
    /* ⚑ v26 — même fond que la vraie Toile (voir `Toile.preview`) : sur Braille et Touffe,
       les deux tiers de la surface SONT ce fond, et `#120E05` s'y lisait comme un voile. */
    g.fillStyle=(clair!=null?clair:isLightM())?'#EFE2C5':'#201908';
    g.fillRect(0,0,W,H);
    /* ⚑ v44 — LA COMPOSITION DU RENDU EST PUBLIÉE (§7 : un juge compare la composition, jamais un pixel d'une matière
       texturée). Ce sont les graines que le monde VA recevoir — publiées juste avant l'appel, jamais après (une publication faite après ne voit pas ce qui a été fait pendant). */
    try{ window._renduComp={W:W,H:H,ech:ech,monde:theme,graines:seeds.filter(function(s){return s.pid!=null;}).map(function(s){return {pid:s.pid,x:(s.px!=null?s.px:s.x),y:(s.py!=null?s.py:s.y),w:s.w};})}; }catch(_){ }   /* v38 : `_rtCible` — le rendu entier de la Toile peut se servir des calques de Touffe */

    _rtCible=cv; try{ RD[theme](performance.now(),0,0,W,H); }finally{ _rtCible=null; }  /* les VRAIS germes */    /* CHANTIER 39 — le texte des dalles : frame() appelle _labels apres
       RD[theme], renderTo ne le faisait pas. Sans lui « Avec / Sans texte »
       n'avait aucun effet sur l'image partagee. */
    if(window._shLabels!==false){
      try{ if(typeof _labels==='function')_labels(performance.now()); }catch(_l){}
    }
    /* les Promi masques au partage : leur dalle revient au gris du fond.
       On repeint par-dessus plutot que de retirer le germe, ce qui
       changerait le pavage entier. */
    try{ var _hid=window.shareHidden||{};
      if(Object.keys(_hid).length){
        for(var _i=0;_i<seeds.length;_i++){
          var _s=seeds[_i];
          if(_s.pid==null||!_hid[_s.pid])continue;
          var _sv={ci:_s.ci,kind:_s.kind,gc:_s.gc};
          _s.ci=null; _s.kind='gray'; _s.gc=null;
          _s.__sv=_sv;
        }
        g.setTransform(ech,0,0,ech,0,0);
        RD[theme](performance.now(),0,0,W,H);
        for(var _j=0;_j<seeds.length;_j++){
          var _t=seeds[_j]; if(!_t.__sv)continue;
          _t.ci=_t.__sv.ci; _t.kind=_t.__sv.kind; _t.gc=_t.__sv.gc; delete _t.__sv;
        }
        if(window._shLabels!==false){
          try{ if(typeof _labels==='function')_labels(performance.now()); }catch(_l2){}
        }
      } }catch(_h){}
    ok=true;
  }catch(e){}
  g=_g;W=_W;H=_H;view=_v;window._shThemeOverride=_ov;DPR=_dpr0;
  return ok;
};
/* ⚑ v26 — LE FOND D'UNE TOILE, NOMMÉ UNE FOIS. Trois fonctions le peignaient chacune de
   son côté (`preview`, `repaintWorld`, `repaint`) : corriger l'une ne changeait rien,
   car `repaint` repasse à chaque frémissement. §7 — un seul propriétaire. */
window.Toile.fondToile=function(clair){ return (clair!=null?clair:isLightM())
  ? (window._shAllColored?'#DDD2B8':'#F1ECD9') : '#201908'; };
window.Toile.repaint=function(pcv){var c=pcv&&pcv.__c;if(!c)return;if(c.vif)return;   /* v75 : l'aperçu vivant se peint dans sa boucle */var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};try{g=pcv.getContext('2d');W=c.pw;H=c.ph;seeds=c.seeds;theme=c.th;view={s:1,ox:0,oy:0};var dpr=pcv.width/c.pw;g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,c.pw,c.ph);g.fillStyle=window.Toile.fondToile();g.fillRect(0,0,c.pw,c.ph);RD[c.th](performance.now(),0,0,c.pw,c.ph);}catch(e){}g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;};
window.Toile.reGray=function(){seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});lastChange=performance.now();kick();};
window.Toile.reGrayStudio=function(pcv){var c=pcv&&pcv.__c;if(!c)return;c.seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});window.Toile.repaint(pcv);};
window.Toile.curWorld=function(){return theme;};
window.Toile.taille=function(){return {w:W,h:H};};   /* v34 · lecture seule */
window.Toile.semisNeuf=function(){ return _semisDe==='neuf'; };   /* v35 · la famille du semis EN PLACE */
/* ⚑ v34 — le semis, en lecture seule : toutes les graines, les colorées, les vides. */
window.Toile.graines=function(){ var c=0; for(var i=0;i<seeds.length;i++) if(seeds[i].kind!=='gray') c++; return {total:seeds.length, colorees:c, vides:seeds.length-c}; };
/* ⚑ v32 — la nature de la dalle seule d'un monde libre neuf (Madrure : 'oeil' · 'fermee' · 'cercle') et son contour peint. */
window.Toile.natureDalle=function(pid,m){ var t=m||theme; if(!_MN||!_MNLIB[t])return null; for(var i=0;i<seeds.length;i++){ if(seeds[i].pid===pid&&seeds[i].kind!=='gray') return _MN.nature(t,seeds[i]); } return null; };
window.Toile.contourDalle=function(pid,m){ var t=m||theme; if(!_MN||!_MNLIB[t])return null; for(var i=0;i<seeds.length;i++){ if(seeds[i].pid===pid&&seeds[i].kind!=='gray') return _MN.contour(t,seeds[i]); } return null; };
window.Toile._madrure=function(inv){ if(inv&&_MN&&_MN.madrure) _MN.madrure.invalider(); return (_MN&&_MN.madrure)?{derniere:_MN.madrure.derniere||null, constructions:_MN.madrure.constructions||0}:null; };
window.Toile.dalleCapture=function(dcv,pid,ech){
  try{
    var D=window.Toile.dalleAbs(pid); if(!D||!D.w||!D.h) return false;
    var cv=document.getElementById('toileCv'); if(!cv) return false;
    var tgt=null;
    for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){tgt=seeds[i];break;}}
    if(!tgt) return false;
    /* marge : encre, terrazzo et touffe debordent de leur cellule */
    var LIBRE=(theme==='encre'||theme==='terrazzo'||theme==='touffe');
    var sp=Math.sqrt(W*H/Math.max(1,seeds.length));
    var mar=LIBRE?sp*0.85:sp*0.10;
    var lx0=D.minx-mar, ly0=D.miny-mar, lw=D.w+2*mar, lh=D.h+2*mar;
    var sx=(lx0*view.s+view.ox)*DPR, sy=(ly0*view.s+view.oy)*DPR;
    var sw=lw*view.s*DPR, sh=lh*view.s*DPR;
    /* si la marge sort du cadre, on rogne au bord plutot que de renoncer */
    var rx0=Math.max(0,sx), ry0=Math.max(0,sy);
    var rx1=Math.min(cv.width,sx+sw), ry1=Math.min(cv.height,sy+sh);
    if(rx1-rx0<8||ry1-ry0<8) return false;
    lx0=lx0+(rx0-sx)/(view.s*DPR); ly0=ly0+(ry0-sy)/(view.s*DPR);
    lw=(rx1-rx0)/(view.s*DPR); lh=(ry1-ry0)/(view.s*DPR);
    sx=rx0; sy=ry0; sw=rx1-rx0; sh=ry1-ry0;
    ech=ech||1;
    var dw=Math.max(1,Math.round(sw*ech)), dh=Math.max(1,Math.round(sh*ech));
    dcv.width=dw; dcv.height=dh;
    var gg=dcv.getContext('2d'); if(!gg) return false;
    gg.setTransform(1,0,0,1,0,0); gg.clearRect(0,0,dw,dh);
    gg.imageSmoothingQuality='high';
    gg.drawImage(cv, sx, sy, sw, sh, 0, 0, dw, dh);
    /* on ne garde que les pixels de CETTE dalle, avec la regle exacte du moteur */
    var im=gg.getImageData(0,0,dw,dh), d2=im.data, ns=seeds.length;
    for(var yy=0;yy<dh;yy++){
      var ly=ly0+(yy+0.5)*lh/dh;
      for(var xx=0;xx<dw;xx++){
        var lx=lx0+(xx+0.5)*lw/dw, bd=1e18, bs=null;
        for(var q=0;q<ns;q++){var s2=seeds[q];
          var ex=lx-s2.x, ey=ly-s2.y;
          var dq=Math.sqrt(ex*ex+ey*ey)-(s2.w||0);
          if(dq<bd){bd=dq;bs=s2;}}
        var o4=(yy*dw+xx)*4;
        if(bs!==tgt){ d2[o4+3]=0; }
        else {
          /* le fond de la Toile devient transparent, la matiere reste pleine */
          var r=d2[o4],g2=d2[o4+1],b2=d2[o4+2];
          var mx=Math.max(r,g2,b2), mn=Math.min(r,g2,b2);
          if((mx-mn)<26 && mx>150) d2[o4+3]=0;
        }
      }
    }
    gg.putImageData(im,0,0);
    /* recadrage au plus juste */
    var x0=dw,y0=dh,x1=-1,y1=-1;
    for(var y3=0;y3<dh;y3++)for(var x3=0;x3<dw;x3++){
      if(d2[(y3*dw+x3)*4+3]>8){if(x3<x0)x0=x3;if(x3>x1)x1=x3;if(y3<y0)y0=y3;if(y3>y1)y1=y3;}}
    if(x1>x0&&y1>y0){
      var tw=x1-x0+1, th=y1-y0+1;
      var tp=document.createElement('canvas'); tp.width=tw; tp.height=th;
      tp.getContext('2d').drawImage(dcv,x0,y0,tw,th,0,0,tw,th);
      dcv.width=tw; dcv.height=th;
      var g3=dcv.getContext('2d'); g3.setTransform(1,0,0,1,0,0); g3.drawImage(tp,0,0);
    }
    return true;
  }catch(e){ return false; }
};
window.Toile.vue=function(){return {s:view.s,ox:view.ox,oy:view.oy,dpr:DPR};};
window.Toile.dalleTrame=function(dcv,pid,k,monde,opts){
  /* ⚑ v29 (Tom, 23 sept.) — DEUX AJOUTS AU MOTEUR, ET RIEN D'AUTRE.
     1 · `k` agrandit AUSSI les pas de trame (`UK`, voir plus haut) : une dalle se rend À SA TAILLE FINALE et se
         pose 1:1. Plus aucun appelant ne redimensionne (redteam_decoupe, famille B).
     2 · `opts` (facultatif) — ce que les appelants faisaient APRÈS le moteur, sur les pixels, le moteur le peint :
         · opts.rampe  = {cols:[[r,g,b]…], haut:h}  la clarté remappée sur une rampe (Q30 : haut 2 ; Q297 : 0,9 ou
                          la hauteur choisie). MÊME formule que `teinteDalle` et `_ingenuTeinte`, au pixel près.
         · opts.decale = {a:ca, b:cb}               la teinte déplacée en Lab, clarté gardée (chantier 59).
         · opts.donnees = true                       le moteur rend aussi SES pixels (`dcv.__dalleDonnees`) —
                          la Pelote en fait une fourrure, elle ne pose pas d'image.
     Et le moteur DÉCLARE ce qu'il a peint (`dcv.__dalleInfo`) : couleur la plus saturée, clarté moyenne, Lab
     moyen, part pleine — ce que les appelants relisaient au pixel (§7 : on lit la composition publiée). */
  /* Peint la matiere du design actif pour LA dalle du Promi demande,
     decoupee sur sa vraie cellule. Meme mecanique que Toile.repaint.

     LE MONDE D'ALORS -- 4 septembre 2026, decision Tom.
     `monde` est FACULTATIF : {m:design, p:palette, h:teinte}. Absent, la fonction se
     comporte EXACTEMENT comme avant -- les six appels existants ne bougent pas.
     Present, elle peint la dalle dans le monde de SA PLANTATION et non dans le monde
     courant : une dalle est figee au jour ou on l'a plantee, et changer de monde au
     Studio ne repeint pas les anciennes.
     On sauve et on restaure sur l'idiome que la fonction porte deja pour g/W/H/seeds/view.
     ATTENTION _palLit est un MEMO de la palette calculee : il doit etre invalide a
     l'aller (sinon la palette de l'appelant fuit dans la dalle) et restaure au retour
     (sinon celle de la dalle fuit dans la Toile). */
  var _g=g,_W=W,_H=H,_s=seeds,_v={s:view.s,ox:view.ox,oy:view.oy},ok=false;
  var _th=theme,_pk=palKey,_hs=hueShift,_pl=_palLit,_uk=UK; _WT=[_W,_H];
  /* ⚑ v30 (Tom, 23 sept.) — « UNE DALLE GARDE SON MONDE PARTOUT. » Sans monde fourni, la dalle se peint dans celui
     de SA PLANTATION (`p.monde`), jamais dans le monde courant du Studio : 22 appels sur 29 l'oubliaient. Seuls ceux
     qui montrent le monde courant EXPRÈS le passent eux-mêmes et le déclarent (`opts.courant`) — la page +, qui montre
     la dalle qu'on va planter, et les aperçus du Studio. Le monde réellement employé est publié (`__dalleInfo.monde`). */
  /* ⚑ v34 (Tom, 23 sept.) — LA RÈGLE S'INVERSE : « tout suit le Studio — le Fil, l'Index, la Toile, la Toile du Cercle, les
     fiches, la page +, Partager. Seule exception : l'Aura » (la Pelote et « Ce que tu as tenu » gardent le monde et la couleur
     de plantation — elles le passent EXPRÈS). Le monde de plantation n'est donc plus le défaut : il se demande (`opts.plantation`). */
  if(!monde && opts && opts.plantation){ try{ for(var _qi=0;_qi<promises.length;_qi++){ if(promises[_qi].id===pid){ if(promises[_qi].monde) monde=promises[_qi].monde; break; } } }catch(_){ } }
  try{
    if(monde){
      if(monde.m&&RD[monde.m])theme=monde.m;
      if(monde.p&&PALS[monde.p])palKey=monde.p;
      if(monde.h!=null)hueShift=+monde.h||0;
      _palLit=null;
    }
    var D=window.Toile.dalleAbs(pid); if(!D||!D.w||!D.h) throw 0;
    k=k||1;
    /* ⚑ v32 — Esquille, Bobinette, Madrure peignent EUX-MÊMES leur dalle seule (`seule`), en vecteurs, à sa taille finale :
       leur matière naît de toute la Toile, un découpage pondéré la trahirait. */
    if(_MN&&_MNLIB[theme]){ _dalleNeuve(dcv,pid,k,opts); } else {
    /* Sur la Toile, encre / terrazzo / touffe DEBORDENT de leur cellule :
       les decouper dessus les tronquait. On leur laisse une marge et aucun
       decoupage ; les mondes a trame restent contenus dans leur cellule. */
    var LIBRE=(theme==='encre'||theme==='terrazzo'||theme==='touffe');
    var spReal=Math.sqrt(_W*_H/Math.max(1,_s.length))*k;
    var pad=Math.round(spReal*(LIBRE?0.85:0.30));   /* marge : la vraie cellule ponderee peut deborder du polygone */
    /* Les motifs a trame sont ancres sur les coordonnees absolues de la Toile
       (points tous les 9, tesselles tous les 11, carres tous les 5, sillons tous les 6).
       En deplacant la cellule il faut donc translater d'un multiple de la periode,
       sinon le motif ne retombe pas au meme endroit que sur la Toile. */
    var PER=({braille:9,mosaique:11,pixel:5,sillons:6}[theme]||0)*k;   /* ⚑ v29 : le pas suit k (UK) */
    var padX=pad, padY=pad;
    if(PER){
      /* alignement EXACT, fractions comprises : un arrondi suffit a decaler un motif a gros pas.
         ⚑ v29 : a tout k — la grille de la Toile (multiples de PER) tombe sur celle de la dalle (multiples de PER·k). */
      padX=pad+((D.minx*k-pad)%PER+PER)%PER;
      padY=pad+((D.miny*k-pad)%PER+PER)%PER;
    }
    var dw=Math.ceil(D.w*k+2*padX), dh=Math.ceil(D.h*k+2*padY);
    dcv.width=Math.round(dw*DPR); dcv.height=Math.round(dh*DPR);
    seeds=_s.map(function(s){var o={};for(var q in s)o[q]=s[q];
      o.x=(s.x-D.minx)*k+padX; o.y=(s.y-D.miny)*k+padY;
      o.px=(s.px!=null)?((s.px-D.minx)*k+padX):null;
      o.py=(s.py!=null)?((s.py-D.miny)*k+padY):null;
      o.w=(s.w||0)*k; return o;});
    W=dw; H=dh; view={s:1,ox:0,oy:0};
    if(LIBRE){
      var ti=-1;
      for(var z=0;z<seeds.length;z++){if(seeds[z].pid===pid&&seeds[z].kind!=='gray'){ti=z;break;}}
      if(ti>=0){
        for(var z2=0;z2<seeds.length;z2++){ if(z2===ti) continue;
          seeds[z2].x=-1e7; seeds[z2].y=-1e7; seeds[z2].px=null; seeds[z2].py=null; }
        /* sp doit valoir celui de la Toile : sp = racine(W*H / nombre de graines) */
        var nn=Math.max(1,seeds.length);
        W=spReal*Math.sqrt(nn); H=W;
      }
    }
    /* ⚑ v29 — LES VOISINES SEULES. Rendue à sa taille finale, une dalle a beaucoup de pixels ; chercher leur graine
       propriétaire parmi TOUTES les graines coûtait 1,9 s pour une dalle Pixel de 200 px (mesuré). Or une graine k ne
       peut posséder AUCUN point du canevas si |t−k| ≥ 2·Rmax + w_k − w_t (Rmax : la distance de la graine t au coin le
       plus lointain) — inégalité triangulaire. On ne passe donc au monde et au masque que les graines sous cette borne :
       l'appartenance à LA cellule est exacte, au pixel. `avg()` garde le nombre de graines de la Toile. */
    if(!LIBRE){
      var _tg=null; for(var z3=0;z3<seeds.length;z3++){ if(seeds[z3].pid===pid&&seeds[z3].kind!=='gray'){ _tg=seeds[z3]; break; } }
      if(_tg){
        var _Rm=0; [[0,0],[dw,0],[0,dh],[dw,dh]].forEach(function(c){ _Rm=Math.max(_Rm, Math.hypot(c[0]-_tg.x, c[1]-_tg.y), Math.hypot(c[0]-(_tg.px!=null?_tg.px:_tg.x), c[1]-(_tg.py!=null?_tg.py:_tg.y))); });
        var _cand=seeds.filter(function(s){ if(s===_tg) return true;
          var dd=Math.min(Math.hypot(s.x-_tg.x, s.y-_tg.y), Math.hypot((s.px!=null?s.px:s.x)-(_tg.px!=null?_tg.px:_tg.x), (s.py!=null?s.py:s.y)-(_tg.py!=null?_tg.py:_tg.y)));
          return dd < 2*_Rm + (s.w||0) - (_tg.w||0) + 2; });
        _nAvg=seeds.length; seeds=_cand;
      }
    }
    g=dcv.getContext('2d',{willReadFrequently:true}); if(!g) throw 0;   /* ⚑ v100 — la dalle est RELUE trois fois (masque exact, recadrage, finition) : déclarée dès la création, elle vit en mémoire processeur et chaque relecture cesse d'être un rapatriement depuis la carte graphique. Mesuré : 1re ouverture d'une Nuée, 2 à 3 s de gel dont 2 s de getImageData. */
    g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,dw,dh);
    g.save();
    var _bT=[(0-D.minx)*k+padX,(0-D.miny)*k+padY,(_W-D.minx)*k+padX,(_H-D.miny)*k+padY];
    UK=k; _cibleDalle=pid; _bordsDalle=_bT;
    try{ RD[theme](performance.now(),0,0,dw,dh); }finally{ _cibleDalle=null; _bordsDalle=null; } UK=_uk;   /* ⚑ v34 : et les bords de la Toile, dans le repère de la dalle */   /* ⚑ v32 : la graine de la dalle, nommée au monde (Ritournelle ne peint qu'elle) */
    g.restore();
    if(!LIBRE){
      /* Le moteur attribue chaque pixel a la graine la plus proche AU SENS PONDERE
         (distance moins poids). Le polygone de _cellPoly n'en est qu'une approximation :
         des que les poids different, la vraie frontiere est courbe. On refait donc
         l'attribution pixel par pixel, avec la regle exacte du moteur. */
      var tg2=null;
      for(var z2=0;z2<seeds.length;z2++){if(seeds[z2].pid===pid&&seeds[z2].kind!=='gray'){tg2=seeds[z2];break;}}
      if(tg2){
        var img2=g.getImageData(0,0,dcv.width,dcv.height), dd=img2.data;
        var iw=dcv.width, ih=dcv.height, sx2=dw/iw, sy2=dh/ih, ns=seeds.length;
        /* ⚑ v29 — MÊME RÈGLE, MÊME RÉSULTAT, moins de calcul. Un point p appartient à la cible t sauf si une graine k
           y fait mieux : |p−k|−w_k < |p−t|−w_t. Comme |p−k| ≥ |t−k|−|p−t|, seule une graine avec
           |t−k| − w_k + w_t < 2·|p−t| peut gagner. On range les autres graines sur cette clé : pour chaque pixel on
           s'arrête à la première qui ne peut plus gagner — au cœur de la cellule, il n'y en a presque aucune. */
        var _tw=(tg2.w||0), _ord=[];
        for(var q2=0;q2<ns;q2++){ var sq0=seeds[q2]; if(sq0===tg2) continue;
          _ord.push({s:sq0, e:Math.hypot(sq0.x-tg2.x, sq0.y-tg2.y)-(sq0.w||0)+_tw}); }
        _ord.sort(function(a,b){ return a.e-b.e; });
        var _no=_ord.length;
        for(var yy=0;yy<ih;yy++){
          var ly=(yy+0.5)*sy2;
          for(var xx=0;xx<iw;xx++){
            var o4=(yy*iw+xx)*4;
            if(dd[o4+3]===0) continue;
            var lx=(xx+0.5)*sx2, ex0=lx-tg2.x, ey0=ly-tg2.y, r0=Math.sqrt(ex0*ex0+ey0*ey0), dt=r0-_tw, lim=2*r0, perd=false;
            /* ⚑ v34 — une cellule du BORD n'a pas de fin : sa dalle s'arrête au bord de la Toile, là où l'écran l'arrête, et plus
               au hasard de la marge du canevas (depuis que la Toile n'est faite que de promesses, presque toutes touchent le bord). */
            if(lx<_bT[0]||lx>_bT[2]||ly<_bT[1]||ly>_bT[3]){ dd[o4+3]=0; continue; }
            for(var q3=0;q3<_no;q3++){ var oq=_ord[q3]; if(oq.e>=lim) break; var sq=oq.s;
              var ex=lx-sq.x, ey=ly-sq.y;
              if(Math.sqrt(ex*ex+ey*ey)-(sq.w||0)<dt){ perd=true; break; } }
            if(perd) dd[o4+3]=0;
          }
        }
        g.putImageData(img2,0,0);
      }
    }
    /* on recadre au plus juste sur la matiere : plus aucune marge morte */
    try{
      var im=g.getImageData(0,0,dcv.width,dcv.height).data;
      var x0=dcv.width,y0=dcv.height,x1=-1,y1=-1;
      for(var yy=0;yy<dcv.height;yy++)for(var xx=0;xx<dcv.width;xx++){
        if(im[(yy*dcv.width+xx)*4+3]>8){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(yy<y0)y0=yy;if(yy>y1)y1=yy;}}
      if(x1>x0&&y1>y0){
        var tw=x1-x0+1, th=y1-y0+1;
        var tmp=document.createElement('canvas'); tmp.width=tw; tmp.height=th;
        tmp.getContext('2d').drawImage(dcv,x0,y0,tw,th,0,0,tw,th);
        dcv.width=tw; dcv.height=th;
        var g2=dcv.getContext('2d'); g2.setTransform(1,0,0,1,0,0); g2.clearRect(0,0,tw,th);
        g2.drawImage(tmp,0,0);
      }
    }catch(e){}
    try{ _dalleFinit(dcv, opts||null); dcv.__dalleInfo.monde={m:theme,p:palKey,h:hueShift}; dcv.__dalleInfo.courant=!!(opts&&opts.courant); }catch(e){}
    }
    ok=true;
  }catch(e){}
  g=_g;W=_W;H=_H;seeds=_s;view=_v;UK=_uk;_nAvg=null;_WT=null;
  theme=_th;palKey=_pk;hueShift=_hs;_palLit=_pl;
  return ok;
};
/* ⚑ v100 (Tom : « deux à trois secondes où l'app se fige ») — LE MOTEUR RETIENT SES RENDUS UN INSTANT. À l'ouverture d'une Nuée,
   la fiche, son fil et ses vignettes se reposent deux à trois fois en 200 ms, et leurs peintres appellent `dalleTrame` en
   direct, sans cache : les MÊMES dalles (même id, même k, même taille) étaient rendues deux à trois fois — 130 ms par passe,
   mesuré. Même rendu demandé dans les 1,5 s — même dalle, même k, même monde, mêmes options, même palette, même thème, même
   boîte au demi-pixel, même couleur — : l'image est RECOPIÉE 1:1 dans le canevas demandé, avec ce que le moteur déclare
   (`__dalleInfo`). Rien n'est redimensionné ni découpé. La Pelote (`opts.donnees`) lit les données du rendu : elle passe
   toujours par le moteur. Le délai court borne ce que la clé ne voit pas (la matière respire). */
(function(){
  var _dt=window.Toile.dalleTrame, MEMO={}, ORD=[];
  function cleM(pid,k,monde,opts){
    var D=null, C='', M={}; try{ D=Toile.dalleAbs(pid); C=String(Toile.colorOf?Toile.colorOf(pid):''); M=Toile.mondeCourant()||{}; }catch(_){ }
    var clair=!!(document.getElementById('device')&&document.getElementById('device').classList.contains('light'));
    return [pid, Math.round((+k||1)*1000), JSON.stringify(monde||null), JSON.stringify(opts||null), M.m, M.p, M.h, clair,
            D?[D.minx,D.miny,D.w,D.h].map(function(v){ return Math.round(v*2); }).join(','):'', C, window.devicePixelRatio||1].join('|');
  }
  window.Toile.dalleTrame=function(dcv,pid,k,monde,opts){
    if(!dcv || (opts && opts.donnees)) return _dt.apply(this,arguments);
    var c; try{ c=cleM(pid,k,monde,opts); }catch(_){ return _dt.apply(this,arguments); }
    var m=MEMO[c], t=performance.now();
    if(m && t-m.t<1500){
      try{ dcv.width=m.cv.width; dcv.height=m.cv.height;
           var gx=dcv.getContext('2d',{willReadFrequently:true}); gx.setTransform(1,0,0,1,0,0); gx.clearRect(0,0,dcv.width,dcv.height);
           gx.drawImage(m.cv,0,0);
           var inf={}; for(var q in (m.info||{})) inf[q]=m.info[q]; dcv.__dalleInfo=inf; return true; }catch(_){ }
    }
    var r=_dt.apply(this,arguments);
    try{ if(r && dcv.width && dcv.height){
      var cp=document.createElement('canvas'); cp.width=dcv.width; cp.height=dcv.height; cp.getContext('2d').drawImage(dcv,0,0);
      if(!MEMO[c]) ORD.push(c); MEMO[c]={cv:cp, info:dcv.__dalleInfo||null, t:t}; if(ORD.length>40) delete MEMO[ORD.shift()]; } }catch(_){ }
    return r;
  };
}());   /* (fermée ainsi, et non par « })(); » en début de ligne : redteam_decoupe borne le moteur à la première ligne qui commence par là) */
/* ⚑ v32 — LA DALLE SEULE D'UN MONDE LIBRE NEUF. Le canevas prend la boîte RÉELLEMENT peinte (`boite`, bobines et liserés
   compris) à l'échelle k, plus un pixel ; `seule` y cale la boîte du contour. Aucune image lue, aucune découpe : on appelle
   le monde sur la Toile même (graines vraies, W et H vrais), seul le contexte change. Échoue (throw) si le monde n'a pas de
   dalle pour cette graine — `dalleTrame` rend alors false. */
function _dalleNeuve(dcv,pid,k,opts){
  var ts=null; for(var q=0;q<seeds.length;q++){ if(seeds[q].pid===pid&&seeds[q].kind!=='gray'){ ts=seeds[q]; break; } }
  if(!ts) throw 0;
  var B=_MN.boite(theme,ts); if(!B) throw 0;
  /* la marge suit k : fixe (1 px), elle rendait la taille non proportionnelle à k, et la seconde passe de `_rendDalle`
     tombait 4 px court — l'Aura (`width:auto`, plafond 64) étirait alors la dalle de 3 % (redteam_decoupe, famille G). */
  var pd=0.5*k, dw=(B.x1-B.x0)*k+2*pd, dh=(B.y1-B.y0)*k+2*pd;   /* arrondi au pixel d'APPAREIL : au pixel CSS, 2 px d'écart de plus */
  dcv.width=Math.max(1,Math.ceil(dw*DPR)); dcv.height=Math.max(1,Math.ceil(dh*DPR)); dw=dcv.width/DPR; dh=dcv.height/DPR;
  g=dcv.getContext('2d'); if(!g) throw 0;
  g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,dw,dh);
  var cx=((B.fx0+B.fx1)/2-B.x0)*k+pd, cy=((B.fy0+B.fy1)/2-B.y0)*k+pd, taille=Math.max(B.fx1-B.fx0,B.fy1-B.fy0)*k;
  if(!_MN.seule(theme,ts,performance.now(),cx,cy,taille)) throw 0;
  /* ⚑ v55 (Tom) — l'œil de Madrure garde les couleurs EXACTES de la Toile, fini sur son trait sombre : la teinture de Q30
     (rampe de la nature) rabattait ses strates voisines sur un même ton et éclaircissait le trait (mesuré : une dalle de Chiche
     sortait en disque uni). C'est le trait sombre qui la détache du champ. */
  _dalleFinit(dcv, (theme==='madrure'&&opts)?{donnees:opts.donnees}:(opts||null));
  dcv.__dalleInfo.monde={m:theme,p:palKey,h:hueShift}; dcv.__dalleInfo.courant=!!(opts&&opts.courant);
  dcv.__dalleInfo.nature=(theme==='madrure')?_MN.nature(theme,ts):'dalle';
}
/* ⚑ v29 — LA FIN D'UNE DALLE, DANS LE MOTEUR : la rampe ou le décalage (opts), puis ce qu'il déclare avoir peint. */
function _dLin(v){ v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4); }
function _dFl(t){ return t>0.008856?Math.pow(t,1/3):7.787*t+16/116; }
function _dLab(r,g2,b){ r=_dLin(r); g2=_dLin(g2); b=_dLin(b);
  var X=(0.4124*r+0.3576*g2+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g2+0.0722*b, Z=(0.0193*r+0.1192*g2+0.9505*b)/1.08883;
  var fx=_dFl(X), fy=_dFl(Y), fz=_dFl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; }
function _dFi(t){ var t3=t*t*t; return t3>0.008856?t3:(t-16/116)/7.787; }
function _dO(v){ v=v<=0.0031308?12.92*v:1.055*Math.pow(Math.max(0,v),1/2.4)-0.055; return v<0?0:(v>1?255:Math.round(v*255)); }
function _dRgb(L,a,b){ var fy=(L+16)/116, fx=fy+a/500, fz=fy-b/200;
  var X=_dFi(fx)*0.95047, Y=_dFi(fy), Z=_dFi(fz)*1.08883;
  return [_dO(3.2406*X-1.5372*Y-0.4986*Z), _dO(-0.9689*X+1.8758*Y+0.0415*Z), _dO(0.0557*X-0.2040*Y+1.0570*Z)]; }
function _dalleFinit(dcv, o){
  var gg=dcv.getContext('2d'); if(!gg||!dcv.width||!dcv.height) return;
  var im=gg.getImageData(0,0,dcv.width,dcv.height), d=im.data, i, L;
  if(o && o.rampe && o.rampe.cols && o.rampe.cols.length>1){
    /* la clarté normalisée par l'étendue de la dalle, puis t = min(2, L·haut)/2 · (n−1) sur la rampe */
    var pal=o.rampe.cols, h=(o.rampe.haut!=null?o.rampe.haut:2), mn=255, mx=0;
    /* ⚑ v34 — l'étendue se lit entre les centiles 5 et 95 : quelques pixels de bord (0,3 % sur une dalle Pixel) suffisaient
       à étirer mn–mx et à rabattre toute la dalle sur le premier ton. */
    /* (les centiles servent SEULEMENT à reconnaître une dalle d'une couleur ; la normalisation reste le min–max d'origine —
       la changer déplaçait la clarté des îles de la Pelote, mesuré par releve-aura : ΔE 13 au lieu de 27 en sombre) */
    var HL=new Uint32Array(256), nL=0;
    for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; L=0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2]; HL[L|0]++; nL++; if(L<mn) mn=L; if(L>mx) mx=L; }
    var cum=0, q5=nL*0.05, q95=nL*0.95, p5=-1, p95=0; for(var bi=0;bi<256;bi++){ cum+=HL[bi]; if(p5<0&&cum>=q5) p5=bi; if(cum>=q95){ p95=bi+1; break; } } if(p5<0) p5=0;
    var et=(mx-mn)||1, uni=(p95-p5)<12 && h>=2;   /* seulement les bandes de Q30 (rampe pleine, haut 2) : la Pelote (0,85) y perdait ses îles, ΔE 7 */   /* ⚑ v34 — une dalle d'UNE couleur (Pixel, Mosaïque…) n'a pas d'étendue de clarté : normalisée,
       elle tombait toute sur le PREMIER ton de la rampe — le plus proche du champ (lilas sur lilas : `(194,164,247)` sur `#C9A8F5`, vu
       sur « + Nuée »). Elle prend le ton le plus haut, celui qui se détache du champ (Q30 : zéro ton sur ton). */
    for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue;
      L=uni?1:(0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2]-mn)/et;
      var t=Math.min(2,L*h)/2*(pal.length-1), kk=Math.min(pal.length-2,Math.floor(t)), f=Math.min(1,t-kk), a=pal[kk], z=pal[kk+1];
      d[i]=a[0]+(z[0]-a[0])*f; d[i+1]=a[1]+(z[1]-a[1])*f; d[i+2]=a[2]+(z[2]-a[2])*f; }
    gg.putImageData(im,0,0);
  } else if(o && o.decale && o.decale.a!=null){
    /* chaque pixel garde sa CLARTÉ et son écart de teinte au centre du nuage ; le nuage va en (a, b) */
    var n=0, sa=0, sb=0, q;
    for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; q=_dLab(d[i],d[i+1],d[i+2]); n++; sa+=q[1]; sb+=q[2]; }
    if(n){ var ma=sa/n, mb=sb/n;
      for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; q=_dLab(d[i],d[i+1],d[i+2]);
        var e=_dRgb(q[0], o.decale.a+(q[1]-ma), o.decale.b+(q[2]-mb)); d[i]=e[0]; d[i+1]=e[1]; d[i+2]=e[2]; }
      gg.putImageData(im,0,0); }
  }
  /* ce que le moteur a peint — lu par les appelants à la place des pixels.
     Le Lab moyen coûte (trois puissances par pixel) : il n'est calculé que pour qui demande les données (la Pelote). */
  var _avecLab=!!(o&&o.donnees);
  var bs=-1, sr=0, sv=0, sb2=0, nL=0, sL=0, nb=0, lL=0, la=0, lb=0, tot=d.length/4;
  for(i=0;i<d.length;i+=4){
    var r=d[i], v=d[i+1], b=d[i+2], al=d[i+3];
    if(al>=120){ var M=Math.max(r,v,b), m=Math.min(r,v,b); if(M>=26&&m<=246){ var s=(M-m)/M; if(s>bs){ bs=s; sr=r; sv=v; sb2=b; } } }
    if(al>200 && (i/4)%11===0){ nL++; sL+=0.2126*r+0.7152*v+0.0722*b; }
    if(_avecLab && al>=24 && (i/4)%4===0){ var q2=_dLab(r,v,b); nb++; lL+=q2[0]; la+=q2[1]; lb+=q2[2]; }
  }
  var pleins=0; for(i=3;i<d.length;i+=4) if(d[i]>=24) pleins++;
  dcv.__dalleInfo={sat:bs>=0?[sr,sv,sb2]:null, satS:bs, lum:nL>40?sL/nL:null, lab:nb?[lL/nb,la/nb,lb/nb]:null, plein:pleins/tot};
  dcv.__dalleDonnees=(o&&o.donnees)?new Uint8ClampedArray(d):null;
}
/* le monde courant, en LECTURE SEULE : ce qu'on fige sur un Promi a sa plantation */
window.Toile.mondeCourant=function(){return {m:theme,p:palKey,h:hueShift};};
/* ⚑ v69 (Tom, 27 sept.) — UN APERÇU DU STUDIO DONNE ENVIE : peu de dalles, des tailles franchement différentes. Les mondes de la
   saison 2 tirent la taille d'une dalle de SA CLÉ (la place R de la planche) et ignorent le poids : sur un aperçu, rien ne variait.
   Un seul propriétaire : une graine d'APERÇU (`s.apercu`) porte un facteur tiré de son poids ; toute graine de la vraie Toile rend 1,
   au pixel près. */
window._tailleApercu=function(s){ if(!s||!s.apercu||!(s.w>0)) return 1; var k=Math.max(0.55,Math.min(1.9,Math.sqrt(s.w/8)));
  /* ⚑ v94 (Tom, iPhone : « la Toile aléatoire : les fleurs de Volubilis prennent tout l'écran. Mets-y uniquement des petites fleurs — une
     exception à Volubilis ») — au Studio seulement (une graine d'aperçu), l'écart de taille gardé, ramené aux petites fleurs */
  return theme==='volubilis'?Math.max(0.32,Math.min(0.62,k*0.5)):k; };
window._apercuClair={ritournelle:1,halin:1,brouillamini:1,chamade:1,volubilis:1,guingois:1,chantourne:1,mascaret:1,ramage:1,esquille:1,bobinette:1};   /* tous les mondes neufs — ⚑ v92 (Tom : « remets l'animation de la toute première intégration ») : Madrure revient à son exception d'origine (v75–v82), la grille de 72 graines dont 10 nœuds font l'onde ; le semis clairsemé (v83) retournait tout le champ à chaque événement */
/* ⚑ v83 (Tom : « Madrure ne s'anime toujours pas au Studio ») — son aperçu était une grille de 72 cellules dont DIX seulement font l'onde
   (v40) : une arrivée poussait ses voisines immédiates — presque toujours des cellules sans effet sur l'onde. Seule une petite bosse
   montait ; le reste ne bougeait pas (vu à l'écran, par le vrai chemin, en Chromium et en WebKit). Son aperçu prend le semis clairsemé des
   mondes neufs : une dizaine de dalles, TOUTES des nœuds — l'exception de v40 (« quelques nœuds, beaucoup de lignes ») est gardée, et la
   poussée déplace maintenant des nœuds : l'onde entière se réécoule, comme sur la vraie Toile. L'écartement des lignes ne dépend pas du
   nombre de cellules (l'unité de la Toile, `env.uMat`). */
window.Toile.preview=function(pcv,th,pw,ph){if(!TH[th])th='pixel';var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};try{g=pcv.getContext('2d');W=pw;H=ph;theme=th;view={s:1,ox:0,oy:0};var dpr=pcv.width/pw;seeds=[];var base=Math.max(20,pw/5.5),gc=Math.max(2,Math.round(pw/base)),gr=Math.max(2,Math.round(ph/base)),cw=pw/gc,ch=ph/gr;for(var r=0;r<gr;r++)for(var c=0;c<gc;c++)seeds.push(mk(cw*(c+.5)+(Math.random()-.5)*cw*.42,ch*(r+.5)+(Math.random()-.5)*ch*.42));/* ⚑ v55 (Tom : « au Studio, les aperçus de Ritournelle et Halin sont trop chargés et trop réguliers — toutes les dalles font la
   même taille ; ce n'est pas fidèle à la Toile ») — une grille à peine bousculée, poids tous nuls. Ces deux mondes ont une Toile
   faite de ses paroles : leur aperçu en pose une comme la vraie — le nombre de cellules d'une Toile d'une vingtaine de paroles,
   semées librement, de poids variés (surtout des paroles, quelques moyennes, de rares grandes comme une Nuée). */
if(window._apercuClair&&window._apercuClair[th]){ seeds=[]; var _AP=window._apercuSemis||{n:10,w:[[0.2,34],[0.5,12],[1,2]],d:0.55};   /* v69 : ~10 dalles à plein écran (21 avant), un cinquième de grandes, un tiers de moyennes, le reste petites */ var _na=Math.max(6,Math.round(pw*ph/(390*844)*_AP.n)), _dm=Math.sqrt(pw*ph/_na)*_AP.d, _tr=0;
  while(seeds.length<_na&&_tr<4000){ _tr++; var _x=pw*(0.03+Math.random()*0.94), _y=ph*(0.03+Math.random()*0.94), _ok=true;
    for(var _q=0;_q<seeds.length;_q++){ if(Math.hypot(seeds[_q].x-_x,seeds[_q].y-_y)<_dm){ _ok=false; break; } }
    if(!_ok) continue; var _sa=mk(_x,_y), _rw=Math.random(); var _wv=_AP.w[_AP.w.length-1][1]; for(var _wi=0;_wi<_AP.w.length;_wi++){ if(_rw<_AP.w[_wi][0]){ _wv=_AP.w[_wi][1]; break; } } _sa.w=_sa.wt=_sa.wFin=_wv*(0.85+Math.random()*0.3); seeds.push(_sa); } }   /* ⚠ pas `_s` : c'est la réserve des graines de la vraie Toile */var cx=pw*(0.28+Math.random()*0.44),cy=ph*(0.34+Math.random()*0.26);var cen=seeds.filter(function(s){return s.y>ph*0.2&&s.y<ph*0.72&&s.x>pw*0.06&&s.x<pw*0.94;});cen.forEach(function(s){s._sc=((s.x-cx)*(s.x-cx)+(s.y-cy)*(s.y-cy))*(0.35+Math.random()*1.6);});cen.sort(function(a,b){return a._sc-b._sc;});var nc=11+(Math.random()*2|0);   /* 5 dalles colorées de plus dans le Studio */for(var i=0;i<nc&&i<cen.length;i++){var s=cen[i];s.ci=cc(s);s.c=PAL[s.ci];s.kind='promi';s.t0=-99999;}var far=cen.slice(Math.floor(cen.length*0.55));var det=1+(Math.random()*2|0);for(var f=0;f<det&&far.length;f++){var ss2=far[(Math.random()*far.length)|0];if(ss2&&ss2.ci==null){ss2.ci=cc(ss2);ss2.c=PAL[ss2.ci];ss2.kind='promi';ss2.t0=-99999;}}if(window._shAllColored){for(var _ac=0;_ac<seeds.length;_ac++){var _sac=seeds[_ac];if(_sac.ci==null){_sac.ci=cc(_sac);_sac.c=PAL[_sac.ci];_sac.kind='promi';_sac.t0=-99999;}}}
/* ⚑ v25 (Tom, 22 sept.) — UN APERÇU N'EST PAS UNE TOILE DE PAROLES, ET IL SE DÉCLARE.
   L'exception Ingénu (v17) fait dire la NATURE à la couleur : `cOf` lit `s.nat`, et une
   cellule sans nature prend le crème dalle — la règle juste pour la vraie Toile (« une
   cellule colorée qui ne porte aucune parole »). Mais l'aperçu du Studio n'a AUCUNE parole :
   toutes ses cellules tombaient sur le crème, et le fond du Studio est devenu beige uni.
   Mesuré par bissection : 47,9 % de pixels colorés avant le lot v17, 11,4 % après.
   On marque donc les graines d'aperçu ; `cOf` leur rend la rotation de la palette. */
for(var _ap=0;_ap<seeds.length;_ap++) seeds[_ap].apercu=1;
tones();try{pcv.__c={seeds:seeds.map(function(s){return {x:s.x,y:s.y,gray:s.gray,gc:null,ci:s.ci,c:s.c,kind:s.kind,tone:s.tone,lit:s.lit,shade:s.shade,ang:s.ang,w:s.w,apercu:1,t0:-99999};}),th:th,pw:pw,ph:ph};}catch(e){}g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,pw,ph);/* ⚑ v26 (Tom, 22 sept.) — LE FOND D'UN APERÇU EST CELUI DE LA VRAIE TOILE.
   Il était peint en `#120E05` (l'encre profonde) alors que la Toile de l'accueil laisse
   voir le fond du mode, `#201908` — 16 niveaux de luminance plus clair. Sur Encre,
   Pixel ou Mosaïque on ne le voit jamais : la matière couvre tout. Sur BRAILLE, dont
   les pois ne couvrent que **34,9 %** de la surface (pas 9 px, rayon 2,9 — mesuré,
   inchangé depuis le lot v14), les 65 % restants SONT ce fond : il se lisait comme un
   voile sombre, et les pois paraissaient petits et ternes. Même remarque pour Touffe. */
g.fillStyle=isLightM()?(window._shAllColored?'#DDD2B8':'#F1ECD9'):'#201908';g.fillRect(0,0,pw,ph);if(!pcv.__vif&&!pcv.__compose)RD[th](performance.now(),0,0,pw,ph);}catch(e){}g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;if(pcv.__vif&&!pcv.__compose){try{window.Toile.apercuImage(pcv);}catch(_){}}};   /* v75 : un aperçu VIVANT ne peint pas d'image fixe — sa première image vivante, tout de suite, dans la même tâche */

var ptrs={},pinch=null;function cp(){var mx=0,my=0;var lx=Math.min(0,W-W*view.s),hx=Math.max(0,W-W*view.s);view.ox=Math.max(lx-mx,Math.min(hx+mx,view.ox));var ly=Math.min(0,H-H*view.s),hy=Math.max(0,H-H*view.s);view.oy=Math.max(ly-my,Math.min(hy+my,view.oy));}
host.style.touchAction='none';
/* ⚑ v46 — LES DOIGTS, EN COORDONNÉES DE LA TOILE : l'appareil peut être réduit (la fenêtre de l'app, mesuré à 0,72) — pris en
   pixels d'écran, le zoom glissait sous les doigts. Pincement élastique au-delà des bornes, glissé élastique aux bords,
   élan au lâcher (vitesse des 100 dernières ms, à l'heure de l'événement), retour dans les bornes par ressort (frame). */
function _loc(e){ var r=host.getBoundingClientRect(), f=r.width?W/r.width:1; return {x:(e.clientX-r.left)*f, y:(e.clientY-r.top)*f, t:e.timeStamp||performance.now()}; }
function _bornesPan(){ var s=view.s; return s>=1 ? [W-W*s,0,H-H*s,0] : [(W-W*s)/2,(W-W*s)/2,(H-H*s)/2,(H-H*s)/2]; }
host.addEventListener('pointerdown',function(e){e.stopPropagation();try{host.setPointerCapture(e.pointerId);}catch(_){}vTarget=null;_inert=null;window._panMain=0;   /* le doigt reprend la main : le cadrage automatique lâche prise */
  ptrs[e.pointerId]=_loc(e);var k=Object.keys(ptrs);
  if(k.length===2){var a=ptrs[k[0]],b=ptrs[k[1]];pinch={d:Math.hypot(a.x-b.x,a.y-b.y)||1,s:view.s,cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,ox:view.ox,oy:view.oy};_pan=null;}
  else if(k.length===1){_pan={ox:view.ox,oy:view.oy,h:[[ptrs[k[0]].t,ptrs[k[0]].x,ptrs[k[0]].y]]};}
  kick();});
host.addEventListener('pointermove',function(e){if(!ptrs[e.pointerId])return;e.stopPropagation();var pr=ptrs[e.pointerId],L=_loc(e);ptrs[e.pointerId]=L;var k=Object.keys(ptrs);
  if(k.length===2&&pinch){var a=ptrs[k[0]],b=ptrs[k[1]];var d=Math.hypot(a.x-b.x,a.y-b.y);var raw=pinch.s*d/pinch.d;
    var ns=raw<ZMIN?ZMIN*Math.pow(raw/ZMIN,0.3):(raw>ZMAX?ZMAX*Math.pow(raw/ZMAX,0.3):raw);   /* au-delà des bornes, la Toile résiste */
    var cx=(a.x+b.x)/2,cy=(a.y+b.y)/2;view.ox=cx-(pinch.cx-pinch.ox)*(ns/pinch.s);view.oy=cy-(pinch.cy-pinch.oy)*(ns/pinch.s);view.s=ns;kick();window._vueMain=true;}
  else if(k.length===1&&_pan){var dx=L.x-pr.x,dy=L.y-pr.y;_pan.ox+=dx;_pan.oy+=dy;var B=_bornesPan();view.ox=_rub(_pan.ox,B[0],B[1]);view.oy=_rub(_pan.oy,B[2],B[3]);
    _pan.h.push([L.t,L.x,L.y]);while(_pan.h.length>2&&L.t-_pan.h[0][0]>100)_pan.h.shift();kick();
    window._panMain=(window._panMain||0)+Math.abs(dx)+Math.abs(dy);if(window._panMain>10)window._vueMain=true;}   /* ⚑ Q212 : la vue appartient à la main dès qu'elle la déplace vraiment — jamais sur un toucher */
});
function pu(e){e.stopPropagation();var L=ptrs[e.pointerId];delete ptrs[e.pointerId];var k=Object.keys(ptrs);
  if(k.length<2)pinch=null;
  if(k.length===1){var r1=ptrs[k[0]];_pan={ox:view.ox,oy:view.oy,h:[[r1.t,r1.x,r1.y]]};}   /* du pincement au glissé, sans saut */
  else if(!k.length){ if(_pan&&_pan.h.length>1&&window._panMain>10){var h0=_pan.h[0],h1=_pan.h[_pan.h.length-1],dt=(h1[0]-h0[0])/1000;
      if(dt>0.008){var vx=(h1[1]-h0[1])/dt,vy=(h1[2]-h0[2])/dt,vm=Math.hypot(vx,vy);if(vm>2400){vx*=2400/vm;vy*=2400/vm;}if(vm>60)_inert={vx:vx,vy:vy};}}
    _pan=null;kick();}}
host.addEventListener('pointerup',pu);host.addEventListener('pointercancel',pu);
window.addEventListener('resize',size);
setTimeout(size,60);
})();
</script>
