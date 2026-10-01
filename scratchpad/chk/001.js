
window.onerror=function(m,src,ln,col){var d=document.getElementById('diag');if(d){d.style.color='#ff5a5a';d.textContent='ERR v17: '+m+' @'+ln+':'+col;}return false;};
(function(){var d=document.getElementById('diag');if(d)d.textContent='JS START v17…';})();
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function setSVG(el,str){if(!el)return;if(str.indexOf('xmlns')<0)str=str.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"');try{const doc=new DOMParser().parseFromString(str,'image/svg+xml');const n=doc.documentElement;if(n&&n.nodeName!=='parsererror'&&!n.getElementsByTagName('parsererror').length){while(el.firstChild)el.removeChild(el.firstChild);el.appendChild(document.importNode(n,true));return;}}catch(e){}el.innerHTML=str;}
const svg=$('#toile'),stage=$('#stage');
let realW=0,realH=0,sc=1,VBH=620,box={x:0,y:0,w:0,h:0};
const TOP=150,BOT=130,MARGIN=20;
let toileVS=1,boxCY=0,toileVB={x:0,y:0,w:300,h:0};

function clipHalf(poly,A,B){const mx=(A[0]+B[0])/2,my=(A[1]+B[1])/2,nx=B[0]-A[0],ny=B[1]-A[1];const s=P=>(P[0]-mx)*nx+(P[1]-my)*ny;const o=[];const n=poly.length;for(let k=0;k<n;k++){const c=poly[k],p=poly[(k-1+n)%n];const dc=s(c),dp=s(p);const ci=dc<=0,pi=dp<=0;if(ci){if(!pi){const t=dp/(dp-dc);o.push([p[0]+t*(c[0]-p[0]),p[1]+t*(c[1]-p[1])]);}o.push(c);}else if(pi){const t=dp/(dp-dc);o.push([p[0]+t*(c[0]-p[0]),p[1]+t*(c[1]-p[1])]);}}return o;}
function voronoi(pts,bb){const[x0,y0,x1,y1]=bb;const bx=[[x0,y0],[x1,y0],[x1,y1],[x0,y1]];return pts.map((p,i)=>{let c=bx;for(let j=0;j<pts.length;j++){if(j===i)continue;c=clipHalf(c,p,pts[j]);if(c.length<3)break;}return c;});}
function _ellipse(cx,cy,rx,ry,nn){const N=56,o=[];for(let i=0;i<N;i++){const a=i/N*6.2831853,ca=Math.cos(a),sa=Math.sin(a);const x=(ca<0?-1:1)*Math.pow(Math.abs(ca),2/nn)*rx,y=(sa<0?-1:1)*Math.pow(Math.abs(sa),2/nn)*ry;o.push([cx+x,cy+y]);}return o;}
function boundaryPoly(){const cx=box.x+box.w/2,cy=box.y+box.h/2,m=state.sort;if(m==='date')return _ellipse(cx,cy,box.w/2*0.66,box.h/2*1.12,3.0);if(m==='urgence'){const r=Math.min(box.w,box.h)/2*1.00;return _ellipse(cx,cy,r,r,2.0);}if(m==='personne')return _ellipse(cx,cy,box.w/2*1.12,box.h/2*0.74,2.8);if(m==='nuee')return _ellipse(cx,cy,box.w/2*1.10,box.h/2*0.88,2.55);return _ellipse(cx,cy,box.w/2*1.10,box.h/2*1.12,2.35);}
function voronoiP(pts,B){return pts.map((p,i)=>{let c=B;for(let j=0;j<pts.length;j++){if(j===i)continue;c=clipHalf(c,p,pts[j]);if(c.length<3)break;}return c;});}
function textOn(fill){let r,g,b;try{if(fill[0]==='#'){const n=parseInt(fill.slice(1),16);r=(n>>16)&255;g=(n>>8)&255;b=n&255;}else{const m=fill.match(/\d+/g);r=+m[0];g=+m[1];b=+m[2];}}catch(e){return 'rgba(255,255,255,.85)';}const L=0.299*r+0.587*g+0.114*b;return L>150?'rgba(20,16,10,.82)':'rgba(255,255,255,.86)';}
function centroid(poly){let a=0,cx=0,cy=0;for(let i=0;i<poly.length;i++){const[x0,y0]=poly[i],[x1,y1]=poly[(i+1)%poly.length];const f=x0*y1-x1*y0;a+=f;cx+=(x0+x1)*f;cy+=(y0+y1)*f;}a*=.5;if(Math.abs(a)<1)return null;return[cx/(6*a),cy/(6*a)];}
function roundPath(pts,r){if(pts.length<3)return'';let d='';const n=pts.length;for(let i=0;i<n;i++){const p0=pts[(i-1+n)%n],p1=pts[i],p2=pts[(i+1)%n];const v1x=p1[0]-p0[0],v1y=p1[1]-p0[1],l1=Math.hypot(v1x,v1y)||1;const v2x=p2[0]-p1[0],v2y=p2[1]-p1[1],l2=Math.hypot(v2x,v2y)||1;const rr=Math.min(r,l1/2,l2/2);const a=[p1[0]-v1x/l1*rr,p1[1]-v1y/l1*rr],b=[p1[0]+v2x/l2*rr,p1[1]+v2y/l2*rr];d+=(i===0?`M${a[0].toFixed(1)} ${a[1].toFixed(1)}`:`L${a[0].toFixed(1)} ${a[1].toFixed(1)}`)+`Q${p1[0].toFixed(1)} ${p1[1].toFixed(1)} ${b[0].toFixed(1)} ${b[1].toFixed(1)}`;}return d+'Z';}
function catmull(P){const n=P.length;let d=`M${P[0][0].toFixed(1)} ${P[0][1].toFixed(1)}`;for(let i=0;i<n;i++){const p0=P[(i-1+n)%n],p1=P[i],p2=P[(i+1)%n],p3=P[(i+2)%n];const c1=[p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6],c2=[p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6];d+=`C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;}return d+'Z';}
const BLOBN=[[.5,.01],[.83,.10],[.99,.39],[.93,.71],[.63,.99],[.34,1],[.08,.73],[.01,.37],[.16,.08]];
function blobPath(b){return catmull(BLOBN.map(p=>[b.x+p[0]*b.w,b.y+p[1]*b.h]));}

const HX=h=>{const n=parseInt(h.slice(1),16);return[(n>>16)&255,(n>>8)&255,n&255];};
const RS=r=>`rgb(${r[0]|0},${r[1]|0},${r[2]|0})`;
const lighten=(c,f)=>c.map(v=>v+(255-v)*f);const darken=(c,f)=>c.map(v=>v*(1-f));
const PAPER=[239,227,199];
function watercolor(c){const m=c.map((v,i)=>v*.4+PAPER[i]*.6);const l=m[0]*.3+m[1]*.59+m[2]*.11;return m.map(v=>v*.65+l*.35);}
function jewel(c){const l=c[0]*.3+c[1]*.59+c[2]*.11;return c.map(v=>Math.max(0,Math.min(255,(l+(v-l)*1.4)*.9)));}

const GROUND='#1B1815';
const MOODS={
  cobalt:['#3667A3','#3E2F93','#2A6CB7','#291F75','#362C85','#40329F','#326BAD'],
  terre:['#D98A4A','#C8682E','#F29304','#b5762f','#A85C32','#caa07a','#d49a5e'],
  aurore:['#FCD4E7','#F0C9A0','#B7C3A5','#C2B0D7','#B3D8E4','#FADFF0','#C8978D'],
  jardin:['#B3C157','#76BDA6','#E7C002','#A55CAB','#8BC8E7','#A4C464','#D2C71B'],
  craie:['#456B8F','#96B2C4','#AACDDE','#D0E1E9','#9CBDCF','#C0D8E3','#6586A1']
};
const MOOD_L={cobalt:'Nuit Cobalt',terre:'Terre Promi',aurore:'Aurore Fraise',jardin:'Jardin Promi',craie:'Craie Marine'};
/* ⚑ v33 (Tom, 23 sept.) — LES NOMS AFFICHÉS CHANGENT, LES CLÉS JAMAIS : Encre → Pochade · Mosaïque → Tesselle ·
   Pixel → Buvard · Sillons → Houle · Gravure → Taille-douce · Terrazzo → Éclisse. Braille et Touffe gardent le leur. */
const STRUCT={
  pixel:{label:'Buvard',d:'pavé Voronoï pixel, chaque dalle un Promi'},
  braille:{label:'Braille',d:'trame de points, la couleur pousse dessus'},
  sillons:{label:'Houle',d:'lignes ondulées, la couleur coule'},
  gravure:{label:'Taille-douce',d:'hachures nettes, angle par dalle'},
  mosaique:{label:'Tesselle',d:'tesselles carrées, sol de céramique'},
  encre:{label:'Pochade',d:'taches d’encre abstraites, une par dalle'},
  terrazzo:{label:'Éclisse',d:'éclats fins dispersés dans un liant'},
  touffe:{label:'Touffe',d:'touffes de fleurs dessinées au marqueur'},
  /* ⚑ v32 — les quatre mondes neufs ; v33 : leurs descriptions, données par Tom */
  halin:{label:'Halin',d:'des pierres polies, serrées les unes contre les autres'}, brouillamini:{label:'Brouillamini',d:'la gouache découpée, chaque promesse taillée d’un seul geste'}, chamade:{label:'Chamade',d:'la page rayée au feutre, chaque promesse y bat comme un cœur'}, volubilis:{label:'Volubilis',d:'le jardin découpé, chaque promesse y est une fleur'}, guingois:{label:'Guingois',d:'le quadrillage à main levée, chaque promesse y fait un pli'}, chantourne:{label:'Chantourné',d:'la soie chinée, chaque promesse est un médaillon'}, mascaret:{label:'Mascaret',d:'l’affiche d’op art, chaque promesse soulève la page'}, ramage:{label:'Ramage',d:'le plumage, chaque promesse y ouvre un œil'}, esquille:{label:'Esquille',d:'la plaque brisée, les éclats font les promesses'}, bobinette:{label:'Bobinette',d:'le fil s’enroule, chaque promesse est une bobine'},
  ritournelle:{label:'Ritournelle',d:'la coulée tourne et revient depuis le centre'}, madrure:{label:'Madrure',d:'l’onde du bois se referme autour de chaque promesse'}
}
var USER={name:'Tom',photo:null,seed:_grainePropre()};
let state={mood:'cobalt',structure:'encre',sort:'inspi',labels:true}   /* par défaut : AVEC texte */;

let nid=100;
/* LE MONDE D'ALORS -- 4 septembre 2026, decision Tom.
   La dalle est figee A LA PLANTATION : changer de monde au Studio ne repeint pas
   les anciennes. On fige donc {m:design, p:palette, h:teinte} sur le Promi au moment
   ou il est plante. HUIT sites plantent un Promi, mais tous passent par CETTE
   fabrique : on la patche elle, jamais les huit.
   Au chargement du fichier la Toile n'existe pas encore -- on retombe alors sur
   `state.structure`, et la passe de rattrapage (plus bas) repasse dessus. */
function mondeDuJour(){
  try{ if(window.Toile&&window.Toile.mondeCourant) return window.Toile.mondeCourant(); }catch(e){}
  return {m:(typeof state!=='undefined'&&state&&state.structure)||'encre',p:'signal',h:0};
}
const P=(t,w,d,i,s,n,fr)=>({id:nid++,title:t,who:w,due:d,intensity:i,status:s,nuee:n,from:fr||'moi',recur:null,remind:null,x:0,y:0,tx:0,ty:0,monde:mondeDuJour()});
let promises=[P("rappeler dimanche","Maman",2,2,'encours','famille'),P("courir 3×/sem","moi",5,3,'encours','soi'),P("offrir le vin","Nico",9,1,'tenu',null),P("réviser le CV","moi",6,2,'encours','soi'),P("photos du weekend","Léa",3,1,'rate',null),P("méditer le matin","moi",1,2,'tenu','soi'),P("réserver l'Airbnb","le groupe",4,2,'encours','lisbonne','moi'),P("la playlist du trajet","le groupe",6,1,'encours','lisbonne','Rachel'),P("trouver le resto","le groupe",8,2,'tenu','lisbonne','Adrien'),P("m'aider à déménager","moi",5,2,'encours',null,'Adrien'),P("relire mon dossier","moi",9,1,'encours',null,'Rachel'),P("appeler le dimanche","Maman",3,2,'tenu','famille'),P("prendre RDV médecin","Maman",7,2,'rate','famille'),P("rendre le livre","Nico",4,2,'encours',null),P("payer ma part","Nico",2,2,'rate',null),P("garder son chat","Léa",6,2,'tenu',null),P("relire son mémoire","Léa",9,1,'encours',null),P("aider au barbecue","Adrien",5,2,'tenu',null),P("rendre la perceuse","Adrien",3,2,'rate',null),P("me prêter sa voiture","moi",3,2,'tenu',null,'Nico'),P("relire mon CV","moi",5,2,'tenu',null,'Maman'),P("me rappeler jeudi","moi",2,2,'rate',null,'Léa'),P("garder les clés","moi",6,2,'encours',null,'Adrien')];
/* DEUX CHICHE au jeu de démonstration (décision Tom) : un LANCÉ et un RELEVÉ. */
(function(){ try{
  var a = P("courir dimanche","Marion",5,2,'encours',null); a.chiche = true;
  var b = P("le grand plongeoir","Marion",3,2,'rate',null); b.chiche = true; b.avec = 'Rachel';
  promises.push(a, b);
}catch(e){} })();
promises.forEach(function(p){if(p.from&&p.from!=='moi'&&p.who==='moi')p.pending=true;});
/* LE RATTRAPAGE -- decision Tom, 4 septembre 2026.
   Les Promi deja plantes -- le jeu de demonstration comme un `promi_state` sauvegarde
   avant ce lot -- n'ont pas de monde. Ils prennent LE MONDE COURANT, fige maintenant.
   On n'invente pas un passe qu'on n'a pas : RIEN n'est tire de leur date. La moisson
   sera donc uniforme jusqu'a aujourd'hui, puis se diversifiera -- c'est exactement ce
   que verrait quelqu'un qui commence, et c'est honnete.
   La passe est IDEMPOTENTE : elle ne touche que ce qui n'a pas de monde. */
window._figeMondesManquants=function(){
  var n=0;
  try{ (promises||[]).forEach(function(p){ if(p&&!p.monde){ p.monde=mondeDuJour(); n++; } }); }catch(e){}
  return n;
};
try{ window._figeMondesManquants(); }catch(e){}
/* ⚑ LA DALLE GARDE SA COULEUR COMME ELLE GARDE SON MONDE — décision Tom, 13 sept. 2026 (Q213).
   La couleur d'une dalle était tirée au hasard (`cc()`, `Math.random`) À CHAQUE CHARGEMENT : « planter un
   arbre » sortait bleue, puis lilas. Une dalle n'avait aucune identité stable. On fige donc, sur le Promi,
   `dalle = {ci, lit}` — l'emplacement dans la palette et la nuance — au moment où il est planté (voir
   `_dalleFigee`, dans le moteur). Les Promi d'avant ce lot n'en ont pas : ils prennent une couleur TIRÉE DE
   LEUR TITRE ET DE LEUR PERSONNE (jamais du hasard, jamais de leur date) — même semis à chaque ouverture, sur
   chaque appareil (§4). ⚠ PAS DE L'ID : les ids du jeu de démonstration changent d'un chargement à l'autre
   (chantier 71) — une couleur tirée de l'id y changeait avec eux, mesuré.
   La passe est IDEMPOTENTE : elle ne touche que ce qui n'a pas de dalle. 4 tons par palette (PALS). */
window._dalleDeCle=function(p){
  var s=String((p&&p.title)||'')+'|'+String((p&&p.who)||''), h=2166136261;
  for(var i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619)>>>0; }
  return {ci:h%4, lit:0};
};
window._figeDallesManquantes=function(){
  var n=0;
  try{ (promises||[]).forEach(function(p){ if(p&&!p.dalle){ p.dalle=window._dalleDeCle(p); n++; } }); }catch(e){}
  return n;
};
try{ window._figeDallesManquantes(); }catch(e){}
try{if(localStorage.getItem('promi_fresh')==='1'){localStorage.removeItem('promi_fresh');promises.length=0;for(var _k in NUE){delete NUE[_k];}NUE['soi']='Moi-même';NUEEMEM={};window._freshBoot=true;}}catch(e){}
(function(){var _h=function(n){return new Date(Date.now()-n*3600000).toISOString();};var _n=promises.filter(function(p){return p.nuee==='lisbonne';});if(_n[0])_n[0].comments=[{t:'je réserve les billets ce soir',d:_h(30),by:'Rachel'},{t:'top, je m\u2019occupe du logement',d:_h(20),by:'Adrien'},{t:'parfait, je m\u2019aligne',d:_h(4),by:'moi'}];if(_n[1])_n[1].comments=[{t:'on part de quelle gare ?',d:_h(12),by:'Nico'}];var _f=promises.filter(function(p){return p.from&&p.from!=='moi';});if(_f[0])_f[0].comments=[{t:'toujours partant ?',d:_h(48),by:_f[0].from},{t:'oui oui, cette semaine',d:_h(9),by:'moi'}];var _m=promises.filter(function(p){return p.who&&p.who!=='moi'&&p.who!=='le groupe'&&!p.nuee;});if(_m[0])_m[0].comments=[{t:'merci d\u2019y penser \u2665',d:_h(26),by:_m[0].who}];})();
const NUE={famille:'Famille',soi:'Moi-même',projet:'Le projet',lisbonne:'Weekend à Lisbonne'};
let NUEEMEM={lisbonne:['Rachel','Adrien','Nico']};
let PEOPLE=['Rachel','Adrien','Nico','Léa','Maman','Mimi'];
let newNueeMembers=[];
const NORMS=[[.34,.21],[.70,.17],[.50,.44],[.26,.66],[.74,.64],[.50,.83]];
const rand=(a,b)=>a+Math.random()*(b-a);
const fillFactor=()=>0.40+0.50*Math.min(1,Math.max(0,(promises.length-1)/10));
function toileScale(){const n=promises.length;if(n<=1)return 0.45;if(n<=9)return 0.45+0.55*(n-1)/8;return Math.min(2.0,1.0+(n-9)/21);}
let justPlanted=null;

let VB='0 0 300 620';
function measure(){let r=svg.getBoundingClientRect();let w=r.width||svg.clientWidth||0,h=r.height||svg.clientHeight||0;if(!w||!h){const dev=document.getElementById('device');const dr=dev&&dev.getBoundingClientRect();w=w||(dr&&dr.width)||stage.clientWidth||window.innerWidth||360;h=h||((dr&&dr.height)?Math.max(320,dr.height-50-96):Math.max(320,(window.innerHeight||760)-150));}if(!w||!h||!isFinite(w)||!isFinite(h)){return false;}realW=w;realH=h;sc=300/realW;VBH=realH*sc;VB=`0 0 300 ${VBH.toFixed(2)}`;computeBox();return true;}
function computeBox(){let vb=VBH;let topVB=TOP*sc,botVB=vb-BOT*sc,availH=botVB-topVB,cY=(topVB+botVB)/2;if(!(availH>80)){topVB=vb*0.18;botVB=vb*0.82;availH=botVB-topVB;cY=vb/2;if(!(availH>80)){vb=Math.max(vb,600);VBH=vb;topVB=vb*0.18;botVB=vb*0.82;availH=botVB-topVB;cY=vb/2;}}const g=toileScale();const maxW=300-2*MARGIN;const baseW=maxW*0.94,baseH=availH*0.94;box.w=Math.max(130,baseW*g);box.h=Math.max(150,baseH*g);box.x=150-box.w/2;box.y=cY-box.h/2;boxCY=cY;toileVS=Math.max(1,g);}
/* assainissement (30 sept.) : lloyd() retiré — l'ancien pavage SVG sur promises[].x/y, que rien n'affichait (render() jetait son dessin) */
function seedInit(){promises.forEach((p,i)=>{const nm=NORMS[i]||[rand(.3,.7),rand(.3,.7)];p.x=box.x+nm[0]*box.w;p.y=box.y+nm[1]*box.h;});promises.forEach(p=>{p.tx=p.x;p.ty=p.y;});}
let raf=null;
function relayout(){computeBox();render();}   /* assainissement : plus de lloyd ni d'animation de l'ancien pavage — le relais (render) reste */
/* assainissement : anim() retirée (elle animait promises[].x/y pour l'ancien rendu SVG) */
/* v104 : targets supprimée (Arranger la Toile retiré, Tom) */

function heroIndex(){let bi=-1,bd=1e9;promises.forEach((p,i)=>{if(p.status==='encours'&&!p.enLair&&p.due!=null&&p.due<bd){bd=p.due;bi=i;}});return bi;}
const DEFS=`<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6f6f8"/><stop offset=".28" stop-color="#B8BEC3"/><stop offset=".5" stop-color="#EEECE8"/><stop offset=".72" stop-color="#7A7269"/><stop offset="1" stop-color="#F4F2EE"/></linearGradient><filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>`;

const SVGNS='http://www.w3.org/2000/svg';
function mk(t,a){const e=document.createElementNS(SVGNS,t);if(a)for(const k in a){if(a[k]!=null)e.setAttribute(k,a[k]);}return e;}
function forcePaint(el){if(!el)return;try{el.getBoundingClientRect();const o=el.style.opacity;el.style.opacity='0.999';requestAnimationFrame(()=>{el.style.opacity=o||'';});}catch(e){}}
function diag(n){const r=svg.getBoundingClientRect?svg.getBoundingClientRect():{width:0,height:0};const cs=toileCv?toileCv.width+'×'+toileCv.height:'—';const co=toileCv?(toileCv.offsetWidth+'×'+toileCv.offsetHeight):'—';const txt=`RW×RH ${Math.round(realW)}×${Math.round(realH)} · ${promises.length}p · ${n}cell · back ${cs} · cssCanvas ${co}`;const a=$('#diag');if(a)a.textContent=txt;const b=$('#diagBox');if(b)b.textContent=txt;}
let cellPolys=[],toileCv=null;
function _esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
/* ⚑ ASSAINISSEMENT (Tom, 30 sept. 2026) — L'ANCIEN MOTEUR SVG EST RETIRÉ. render() calculait un Voronoï sur promises[].x/y,
   bâtissait une chaîne SVG… puis écrivait svg.innerHTML='' : rien n'était jamais affiché (la Toile est le moteur, window.Toile).
   Il est appelé de 48 endroits comme un « rafraîchis » : on garde ses seuls effets vivants — la mesure de la scène, le point
   du mot-marque (updatePulse), le diagnostic. cellPolys reste vide : ses deux replis (vignette d'un gardé de côté, fond du
   partage) dessinaient un POLYGONE, ce que le §4 interdit. Version d'avant : sauvegardes/app-avant-assainissement.html */
function render(){
  if(!realW||!isFinite(box.w)||box.w<=0){if(!measure())return;}
  cellPolys=[];
  diag(0);if(typeof updatePulse==='function')updatePulse();
}
function pip(poly,x,y){let inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if(((a[1]>y)!==(b[1]>y))&&(x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]))inside=!inside;}return inside;}
function hitCell(cx,cy){const r=svg.getBoundingClientRect();if(!r.width)return null;const vb=toileVB||{x:0,y:0,w:300,h:VBH};const x=vb.x+(cx-r.left)/r.width*vb.w,y=vb.y+(cy-r.top)/r.height*vb.h;for(let k=cellPolys.length-1;k>=0;k--){if(pip(cellPolys[k].poly,x,y))return cellPolys[k].id;}return null;}
const sEl=document.createElement('style');sEl.textContent='@keyframes rb{0%,100%{opacity:.35}50%{opacity:.85}}@keyframes br{0%,100%{opacity:.55;transform:scale(.97)}50%{opacity:1;transform:scale(1.03)}}';document.head.appendChild(sEl);

const scrim=$('#scrim');
function openSheet(el){closeAll();el.classList.add('show');scrim.classList.add('show');try{var _dv=document.getElementById('device');if(_dv)_dv.classList.toggle('v-index',el&&el.id==='indexSheet');}catch(e){}try{if(el&&el.id==='indexSheet'&&typeof window.ixRefresh==='function')setTimeout(window.ixRefresh,60);}catch(e){}
  /* une feuille se rouvre toujours en haut, comme à la première ouverture */
  try{el.scrollTop=0;el.querySelectorAll('*').forEach(function(n){if(n.scrollTop)n.scrollTop=0;});}catch(e){}
}
function closeAll(){window._tEcran=performance.now();   /* ⚑ v100 : l'heure du dernier changement d'écran — les travaux de fond l'attendent */
$$('.sheet,.poster').forEach(s=>s.classList.remove('show'));try{var _dc=document.getElementById('device');if(_dc)_dc.classList.remove('v-index');}catch(e){}const _cc=$('#cellCard');if(_cc)_cc.classList.remove('show');scrim.classList.remove('show');try{setTimeout(function(){if(window.Toile_liven)window.Toile_liven();},50);}catch(e){}}
scrim.onclick=closeAll;
let ccId=null;
function closeCard(){const c=$('#cellCard');if(c)c.classList.remove('show');scrim.classList.remove('show');}
function openCell(id){
  const p=promises.find(x=>x.id===id);if(!p)return;
  var _da=null; try{ if(window.Toile&&window.Toile.dalleAbs) _da=window.Toile.dalleAbs(id); }catch(e){}
  const rec=_da?{id:id,poly:_da.poly}:cellPolys.find(c=>c.id===id);
  if(!rec){openDetail(id);return;}
  const poly=rec.poly;let a=1e9,b=1e9,mx=-1e9,my=-1e9;poly.forEach(q=>{a=Math.min(a,q[0]);b=Math.min(b,q[1]);mx=Math.max(mx,q[0]);my=Math.max(my,q[1]);});
  const bw=Math.max(1,mx-a),bh=Math.max(1,my-b),CW=250,CH=Math.max(178,Math.min(236,Math.round(CW*bh/bw)));
  const pad=8,s=Math.min((CW-2*pad)/bw,(CH-2*pad)/bh),ox=(CW-bw*s)/2,oy=(CH-bh*s)/2;
  const fit=poly.map(q=>[ox+(q[0]-a)*s,oy+(q[1]-b)*s]),d=roundPath(fit,((STRUCT[state.structure]&&STRUCT[state.structure].round)||10)*s);
  const pal=MOODS[state.mood],st=STRUCT[state.structure];let c=HX(pal[p.id%pal.length]);
  if(st.tint==='aqua')c=watercolor(c);if(st.jewel)c=jewel(c);
  const hi=heroIndex(),idx=promises.indexOf(p);
  const edge=idx===hi?'#82AEF8':p.status==='rate'?'#8F8B79':p.status==='tenu'?RS(lighten(c,.12)):RS(c);
  const svg=$('#ccSvg');svg.setAttribute('viewBox','0 0 '+CW+' '+CH);
  svg.innerHTML='<path d="'+d+'" fill="'+edge+'" opacity="0.09"/><path d="'+d+'" fill="var(--surf)" fill-opacity="0.93" stroke="'+edge+'" stroke-width="2.4" stroke-linejoin="round"/>';
  $('#cellCard').style.height=CH+'px';
  $('#ccTo').textContent=p.who?('à — '+p.who):'à — moi';
  $('#ccT').textContent=p.title||'';
  {let _m=p.draft?'brouillon':p.status==='tenu'?'tenue':p.status==='rate'?'à tenir':(p.enLair?'en l’air':(p.due==null?'en l’air':(p.due<=1?'échéance demain':'échéance dans '+p.due+' j')));if(p.recur)_m+=' · ↻ '+({daily:'quotidien',weekly:'hebdo',monthly:'mensuel'}[p.recur]||p.recur);if(p.remind)_m+=' · ⏰ '+p.remind;$('#ccM').textContent=_m;var _cn=$('#ccNote');if(_cn){_cn.textContent=p.note||'';_cn.style.display=p.note?'block':'none';}}
  ccId=id;closeAll();var _a=$('#ccActs');if(_a)_a.style.display='';var _o=$('#ccPushOpts');if(_o)_o.style.display='none';$('#cellCard').classList.add('show');scrim.classList.add('show');
}
if($('#ccKeep'))$('#ccKeep').onclick=(e)=>{if(e&&e.stopPropagation)e.stopPropagation();const p=promises.find(x=>x.id===ccId);if(p){p.status='tenu';p.draft=false;var _rg=p.recur?regenRecur(p):false;if(typeof feedAdd==='function')feedAdd('kept','Tu as tenu « '+p.title+' »',{pid:p.id});if(_rg&&typeof relayout==='function')relayout();else render();if(typeof caption==='function')caption();_keptCount++;if(_keptCount===2||_keptCount===5){toast('Belle série — partage ton Noyau','Partager',function(){if(typeof openSealShare==='function')openSealShare();});}}closeCard();};
if($('#ccPush'))$('#ccPush').onclick=(e)=>{if(e&&e.stopPropagation)e.stopPropagation();var a=$('#ccActs');if(a)a.style.display='none';var o=$('#ccPushOpts');if(o)o.style.display='flex';};
$$('#ccPushOpts button').forEach(function(b){b.onclick=function(e){if(e&&e.stopPropagation)e.stopPropagation();var p=promises.find(x=>x.id===ccId);if(p){p.due=(p.due||0)+(+b.getAttribute('data-d'));if(typeof feedAdd==='function')feedAdd('added','« '+p.title+' » reportée de '+b.textContent.trim(),{pid:p.id});render();if(typeof caption==='function')caption();}closeCard();};});
if($('#ccManage'))$('#ccManage').onclick=(e)=>{if(e&&e.stopPropagation)e.stopPropagation();const id=ccId;closeCard();openDetail(id);};
function miniCell(p){
  /* la dalle de l'Index est la MÊME que sur la Toile : même découpe, même couleur.
     (avant : elle s'appuyait sur cellPolys, la liste de l'ancien rendu SVG — vide —
     et retombait donc toujours sur un pictogramme générique) */
  /* TOUJOURS la vraie dalle, peinte par Toile.dalleTrame() dans peintMinis().
     Le repli sur cellPolys dessinait un POLYGONE : jamais dans l'Index. */
  if(!p.draft){
    return `<canvas class="bul mini-dalle" width="144" height="144" data-mini="${p.id}"></canvas>`;
  }
  const rec=cellPolys.find(c=>c.id===p.id);if(!rec)return bullet(p);
  let a=1e9,b=1e9,mx=-1e9,my=-1e9;rec.poly.forEach(q=>{a=Math.min(a,q[0]);b=Math.min(b,q[1]);mx=Math.max(mx,q[0]);my=Math.max(my,q[1]);});
  const bw=Math.max(1,mx-a),bh=Math.max(1,my-b),S=28,pad=2,s=Math.min((S-2*pad)/bw,(S-2*pad)/bh),ox=(S-bw*s)/2,oy=(S-bh*s)/2;
  const fit=rec.poly.map(q=>[ox+(q[0]-a)*s,oy+(q[1]-b)*s]);
  const pal=MOODS[state.mood];let col=RS(HX(pal[p.id%pal.length]));if(p.status==='rate')col='#8F8B79';
  return `<svg viewBox="0 0 ${S} ${S}" style="width:28px;height:28px;flex:none"><path d="${roundPath(fit,3)}" fill="${col}" opacity="${p.draft?0.45:1}"/></svg>`;}

$$('[data-close]').forEach(function(b){b.onclick=function(e){var el=e.target.closest('.screen,.sheet,.poster,.seal-ov');if(el)el.classList.remove('show');try{if(typeof scrim!=='undefined'&&scrim&&scrim.classList)scrim.classList.remove('show');}catch(_){}};});
window.renderCsDalle=function(){var cs=document.getElementById('createSheet');var k=cs?(cs.getAttribute('data-kind')||'promi'):'promi';var tint={promi:'#82AEF8',chiche:'#FFB8D2',nuee:'#E6D8FA',draft:'#DD4D23'}[k]||'#82AEF8';try{if(typeof promiTrame==='function')promiTrame('csTrameCv','createSheet',{cut:0,size:0.52,y:0.40,tint:tint});}catch(e){}

  try{if(window._dalleDerive)_dalleDerive('createSheet');}catch(e){}};
window.renderTileIcons=function(){try{
  /* LES TEINTES DU §1.2, pas des approchantes. Le Chiche sortait en ROSE (#FFDAEF) là où
     sa palette de dalle est PÊCHE (#FAD7CA · #F5AC9E · #E0786D) — constaté au duo du
     cadre 17. On prend la teinte médiane de chaque nature. */
  var T={promi:'#C4A2F5',chiche:'#F5AC9E',nuee:'#D6BFF7',draft:'#EEB293'};
  /* LOT 3 · tuiles distinctes par l'AGENCEMENT (jamais de polygone, toujours le moteur) :
     Promi = une dalle centrée · Nuée = quatre dalles à la disposition du bandeau de la fiche Nuée
     · Brouillon = une dalle plus petite et en retrait. */
  var _h=function(k){var cv=document.getElementById('tdIcon_'+k);if(!cv)return null;var hero=cv.parentElement;if(!hero)return null;if(!hero.id)hero.id='tdHost_'+k;return hero.id;};
  var ip=_h('promi');if(ip&&typeof promiTrame==='function')promiTrame('tdIcon_promi',ip,{cut:0,size:0.72,y:0.5,right:0.14,tint:T.promi,courant:1});
  /* LA TUILE DU CHICHE N'ÉTAIT JAMAIS PEINTE : sa teinte figurait dans T, son canevas dans
     le DOM, mais aucune ligne ne l'appelait — la carte « Un Chiche » du cadre 17 restait
     vide (constaté au duo). Même appel que le Promi, avec sa teinte à lui. */
  var ic=_h('chiche');if(ic&&typeof promiTrame==='function')promiTrame('tdIcon_chiche',ic,{cut:0,size:0.72,y:0.5,right:0.14,tint:T.chiche,courant:1});
  var idd=_h('draft');if(idd&&typeof promiTrame==='function')promiTrame('tdIcon_draft',idd,{cut:0,size:0.52,y:0.60,right:0.12,tint:T.draft,courant:1});
  if(window._peintTuileNuee)_peintTuileNuee(T.nuee);
}catch(e){}};
window._peintTuileNuee=function(tint){try{
  var cv=document.getElementById('tdIcon_nuee');if(!cv)return;var host=cv.parentElement;if(!host)return;
  var W=host.clientWidth|0,H=host.clientHeight|0;if(W<40||H<40)return;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);cv.style.width=W+'px';cv.style.height=H+'px';
  var g=cv.getContext('2d');if(!g)return;g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);
  /* EXACTEMENT la disposition POS du bandeau de _ficheDalle, les 4 premières. */
  var POS=[[0.50,0.42,0.46],[0.16,0.30,0.34],[0.80,0.26,0.32],[0.30,0.68,0.30]];
  var ids=[];try{ids=promises.filter(function(q){return !q.draft&&!q.req;}).slice(0,4).map(function(q){return q.id;});}catch(_){}
  if(!ids.length)return;
  for(var k=0;k<POS.length;k++){var id=ids[k%ids.length];
    /* ⚑ v29 — rendue par le moteur à sa largeur, posée 1:1 (redteam_decoupe) */
    var pp=POS[k],L2=W*pp[2],t2=null;
    try{t2=window._rendDalle(id,L2*dpr,1e5,{courant:1});}catch(_){continue;}   /* v30 · page + : le monde courant, exprès */ if(!t2)continue;
    window._poseUn(g,t2,W*pp[0],H*pp[1]);}
  /* teinte lilas — le signal de la Nuée, comme les deux autres tuiles */
  try{g.save();g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='source-atop';g.globalAlpha=0.8;g.fillStyle=tint;g.fillRect(0,0,cv.width,cv.height);g.restore();}catch(_){}
}catch(e){}};

$('#createBtn').onclick=()=>{window._ppGarde=false;quitteVues();try{if(window.csMajSens)csMajSens();if(window.dfMaj)dfMaj();}catch(_c){}selNuee=null;createKind='promi';var _csK=document.getElementById('createSheet');if(_csK)_csK.setAttribute('data-kind','promi');try{if(window._csSetHead)window._csSetHead('promi');}catch(e){}newNueeMembers=[];$$('#createSheet .tile').forEach(x=>x.classList.toggle('on',x.dataset.kind==='promi'));$('#promiForm').style.display='block';$('#nueeForm').style.display='none';$('#draftForm').style.display='none';buildCreateNuees();buildWhoChips();buildNueeMembers();openSheet($('#createSheet'));};
/* l'Index n'a plus de bouton dans le dock : il vit avec la Toile, par le
  selecteur du haut. On garde une fonction d'ouverture pour les appels. */
window.ouvrirIndex=function(){buildIndex();openSheet($('#indexSheet'));};
/* le selecteur du haut : Toile / Index — l'Index est le reflet de la Toile,
   sa place est ici. Le Fil a son bouton au dock, avec sa cloche. */
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('#viewSwitch button[data-view=index]');
  if(!b)return;
  try{ window.ouvrirIndex();
    /* le selecteur revient sur Toile : l'Index est une feuille, pas une vue */
    setTimeout(function(){
      document.querySelectorAll('#viewSwitch button').forEach(function(x){
        x.classList.toggle('on', x.dataset.view==='toile');});},240);
  }catch(_){}
},true);
/* l'Index n'a plus de bouton dans le dock : on garantit une entree depuis
   le Fil, qui en est le pendant. Sans elle il deviendrait inatteignable. */
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('#fdIdxBtn'); if(!b)return;
  try{document.getElementById('feedScreen').classList.remove('show');
      window.ouvrirIndex();}catch(_){}
},true);
var _fib=$('#filIdxRow');if(_fib)_fib.onclick=()=>{window.ouvrirIndex();};
$('#settingsBtn').onclick=()=>{quitteVues();wireProfile();renderProfile();$('#settingsScreen').classList.add('show');try{requestAnimationFrame(function(){if(window.stRefresh)window.stRefresh();});}catch(e){}};
function _refreshAvatars(){try{if(typeof buildFeed==='function' && vis('feedView'))buildFeed();}catch(e){}}
function renderProfile(){var a=$('#setAva');if(a){a.style.background=USER.photo?('center/cover url('+USER.photo+')'):_blobBg('u'+USER.seed);a.classList.toggle('ava-blob',!USER.photo);a.classList.toggle('ava-p',!!USER.photo);}var ni=$('#setNameInput');if(ni&&document.activeElement!==ni)ni.value=USER.name;var dp=$('#setDelPhoto');if(dp)dp.style.display=USER.photo?'flex':'none';}
var _profWired=false;
function wireProfile(){if(_profWired)return;var av=$('#setAva'),si=$('#setPhotoInput'),dp=$('#setDelPhoto'),ni=$('#setNameInput');
  if(av&&si){av.onclick=function(){si.click();};si.onchange=function(){var f=si.files&&si.files[0];if(!f)return;var r=new FileReader();r.onload=function(){USER.photo=r.result;renderProfile();_refreshAvatars();};r.readAsDataURL(f);};}
  if(dp)dp.onclick=function(e){e.stopPropagation();USER.photo=null;USER.seed=(Math.random()*1e9)|0;renderProfile();_refreshAvatars();};
  if(ni){var _save=function(){var v=ni.value.trim();if(v){USER.name=v;_refreshAvatars();}else{ni.value=USER.name;}};ni.onblur=_save;ni.onkeydown=function(e){if(e.key==='Enter'){ni.blur();}};}
  _profWired=true;}
$('#souffleBtn').onclick=()=>{quitteVues();buildAura();try{document.querySelectorAll('#auraScreen .kr-c').forEach(function(cv){try{drawKRing(cv);}catch(e){}});}catch(e){}try{drawSpks();}catch(e){}try{document.querySelectorAll('#demoTg button').forEach(function(x){x.classList.toggle('on',x.dataset.p===(isPremium?'1':'0'));});}catch(e){}const _s=$('#auraScreen');_s.classList.add('show');_s.scrollTop=0;requestAnimationFrame(()=>{try{_s.scrollTop=0;}catch(e){}});};
function quitteVues(){
  try{ if(typeof closeAll==='function') closeAll(); }catch(e){}
  try{ var sc=document.getElementById('scrim'); if(sc) sc.classList.remove('show'); }catch(e){}
  try{ if(typeof _mainView!=='undefined' && _mainView==='fil' && typeof setView==='function') setView('toile'); }catch(e){}
}
window.quitteVues=quitteVues;
$('#studioBtn').onclick=()=>{try{if(window._onbTerminer)window._onbTerminer();}catch(_){}quitteVues();buildStudio();$('#studioScreen').classList.add('show');try{requestAnimationFrame(function(){requestAnimationFrame(_placeLockCard);});setTimeout(_placeLockCard,160);setTimeout(_placeLockCard,460);}catch(e){}};
function ouvreCercle(){
  try{ if(typeof closeAll==='function') closeAll(); }catch(e){}
  try{ var sc=document.getElementById('scrim'); if(sc) sc.classList.remove('show'); }catch(e){}
  try{ document.querySelectorAll('.screen.show,.poster.show').forEach(function(x){x.classList.remove('show');}); }catch(e){}
  var ps=document.getElementById('plusScreen'); if(!ps) return;
  ps.classList.add('show');
  /* le noyau et le visuel du haut se dessinent une fois la page visible */
  var trace=function(){
    try{ if(typeof drawCercleHero==='function') drawCercleHero(); }catch(e){}
    try{ if(typeof buildCercleHero==='function') buildCercleHero(); }catch(e){}
    try{ if(typeof drawCercleNoyau==='function') drawCercleNoyau(); }catch(e){}
    try{ document.querySelectorAll('#plusScreen canvas.kr-c').forEach(function(cv){
      if(typeof drawKRing==='function') drawKRing(cv); }); }catch(e){}
  };
  try{ requestAnimationFrame(function(){ trace(); setTimeout(trace,320); }); }catch(e){ trace(); }
}
window.ouvreCercle=ouvreCercle;
document.addEventListener('click',function(e){
  var t=e.target&&e.target.closest?e.target.closest('.adv-lock,[data-cercle],.set-cercle'):null;
  if(!t) return; e.preventDefault(); e.stopPropagation(); ouvreCercle();
},true);
$('#karmaCercle')&&($('#karmaCercle').onclick=()=>{try{if(typeof setPremium==='function')setPremium(true);}catch(e){}try{if(typeof toast==='function')toast('Tu es Membre Ma Parole ! · Cercles illimités');}catch(e){}ouvreCercle();$('#plusScreen').classList.add('show');if(typeof drawCercleHero==='function')drawCercleHero();if(typeof buildCercleHero==='function')buildCercleHero();});
$('#openPlusTop')&&($('#openPlusTop').onclick=()=>{ouvreCercle();$('#plusScreen').classList.add('show');if(typeof drawCercleHero==='function')drawCercleHero();if(typeof buildCercleHero==='function')buildCercleHero();});
var _ownedDesigns={};var isPremium=false;function setPremium(v){isPremium=v;$('#device').classList.toggle('premium',v);try{if(!v){var _cw=(window.Toile&&window.Toile.curWorld?window.Toile.curWorld():null);if(_cw==='mosaique'||_cw==='pixel'){if(window.Toile&&window.Toile.setTheme)window.Toile.setTheme('encre');if(typeof state!=='undefined'&&state)state.structure='encre';try{if(typeof render==='function')render();}catch(e){}}}}catch(e){}try{var _stSc=document.getElementById('studioScreen');
  if(_stSc&&_stSc.classList.contains('show')){
    /* le Studio est ouvert sur un design (peut-être payant) : en passant premium
       il faut lever son verrou ET l'appliquer à la Toile, sans revenir à Encre. */
    var _wn=_stSc.querySelector('.st3-wn');
    var _shown=_wn?_wn.textContent.trim().replace(' \u2726','').replace(' \u2727',''):null;
    var _map={'Pochade':'encre','Tesselle':'mosaique','Buvard':'pixel','Houle':'sillons','Taille-douce':'gravure','\u00c9clisse':'terrazzo',   /* v33 : les noms neufs ; les anciens restent lus */
      'Encre':'encre','Touffe':'touffe','Braille':'braille','Pixel':'pixel','Sillons':'sillons','Gravure':'gravure','Terrazzo':'terrazzo','Mosaïque':'mosaique','Halin':'halin','Brouillamini':'brouillamini','Chamade':'chamade','Volubilis':'volubilis','Guingois':'guingois','Chantourné':'chantourne','Mascaret':'mascaret','Ramage':'ramage','Esquille':'esquille','Bobinette':'bobinette','Ritournelle':'ritournelle','Madrure':'madrure'};
    var _w=_map[_shown];
    if(v&&_w){                       /* premium : on applique le design affiché */
      try{state.structure=_w;window.Toile.setTheme(_w);}catch(e){}
      _stSc.classList.remove('world-locked');
    }
    if(typeof buildStudio==='function')buildStudio();
  }}catch(e){}var _op=$('#openPlusTop');if(_op&&v){var _t=_op.querySelector('.sc-t'),_s=_op.querySelector('.sc-s'),_g=_op.querySelector('.sc-go');if(_t)_t.textContent='Tu es Membre Ma Parole !';if(_s)_s.textContent='tout Promi débloqué · merci';if(_g)_g.style.display='none';}try{buildAura();document.querySelectorAll('#auraScreen .kr-c').forEach(function(cv){try{drawKRing(cv);}catch(e){}});drawSpks();}catch(e){}}
$$('#demoTg button').forEach(function(bt){bt.onclick=function(){$$('#demoTg button').forEach(function(x){x.classList.remove('on');});bt.classList.add('on');setPremium(bt.dataset.p==='1');};});
['#buyMonth','#buyYear'].forEach(function(id){var bt=$(id);if(bt)bt.onclick=function(){setPremium(true);$$('#demoTg button').forEach(function(x){x.classList.toggle('on',x.dataset.p==='1');});$('#plusScreen').classList.remove('show');if(typeof toast==='function')toast('Tu es Membre Ma Parole ! \u2713 \u00b7 tout Promi d\u00e9bloqu\u00e9');$('#souffleBtn').onclick();};});
$('#openStudio2').onclick=()=>{try{if(window._onbTerminer)window._onbTerminer();}catch(_){}$('#settingsScreen').classList.remove('show');buildStudio();$('#studioScreen').classList.add('show');};

let due=null;   /* Décision Tom : sans choix explicite, une promesse n'a PAS d'échéance
                   (due=null) — jamais « à tenir » tant qu'on n'a pas posé de date. */
let createKind='promi';
let selNuee=null;
/* selection des dalles geree par initCreatePlus (carousel) */
$('#dueChips').onclick=e=>{const c=e.target.closest('.chip');if(!c)return;$$('#dueChips .chip').forEach(x=>x.classList.remove('on'));c.classList.add('on');due=+c.dataset.d;};
window.printTirage=function(btnId,closeFn){try{window._tirageActive=true;var _dc=document.getElementById('csTrameCv');var _cs=document.getElementById('createSheet');var _k=_cs?(_cs.getAttribute('data-kind')||'promi'):'promi';var _tc={promi:'#82AEF8',nuee:'#E6D8FA',draft:'#DD4D23'}[_k]||'#82AEF8';var _fired=false,_fin=function(){if(_fired)return;_fired=true;/* v103 (Tom : « retire ce qui apparaît une fraction de seconde ») : la dalle a couvert l'écran — ON COUPE. La page + disparaissait en glissant après avoir repris son aspect d'avant (la dalle remise à sa taille, ~100 ms), puis son plateau traînait seul sur la Toile. Elle se cache d'un coup ; elle se remontre une fois hors de l'écran. */if(_cs){_cs.classList.add('cs-coupe');setTimeout(function(){_cs.classList.remove('cs-coupe');},900);}if(_dc){_dc.style.transition='none';_dc.style.transform='none';_dc.style.filter='none';_dc.style.backgroundColor='';_dc.style.transformOrigin='';_dc.style.willChange='auto';}if(closeFn){try{closeFn();}catch(_){}}};if(_dc){_dc.style.willChange='transform,filter,background-color';_dc.style.transformOrigin='68% 40%';_dc.style.transition='none';_dc.style.transform='scale(1)';_dc.style.backgroundColor='transparent';_dc.style.filter='drop-shadow(0 0 0 rgba(221,77,35,0)) drop-shadow(0 0 0 rgba(130,174,248,0))';void _dc.offsetWidth;/* PHASE 1 : la signature emerge a vitesse normale, dalle a taille normale */_dc.style.transition='filter .42s cubic-bezier(.22,1,.36,1)';_dc.style.filter='drop-shadow(-5px 3px 0 rgba(221,77,35,.85)) drop-shadow(5px -3px 0 rgba(130,174,248,.85))';/* PHASE 2 : apres la signature, on retire le filtre puis on grossit vite et on coupe */setTimeout(function(){if(!_dc)return;_dc.style.filter='none';_dc.style.transition='transform .24s cubic-bezier(.4,.72,.42,1),background-color .18s ease';_dc.style.transform='scale(7)';_dc.style.backgroundColor=_tc;var _te=function(e){if(e&&e.propertyName&&e.propertyName!=='transform')return;_dc.removeEventListener('transitionend',_te);_fin();};_dc.addEventListener('transitionend',_te);setTimeout(_fin,340);},440);setTimeout(function(){_dc.style.transition='';_dc.style.transform='none';_dc.style.filter='none';_dc.style.backgroundColor='';_dc.style.transformOrigin='';_dc.style.willChange='auto';window._tirageActive=false;},1500);}else{_fin();}if(btnId){var _bp=document.getElementById(btnId);if(_bp){_bp.style.transition='transform .2s ease';_bp.style.transform='scale(.98)';setTimeout(function(){_bp.style.transform='';},220);}}}catch(e){if(closeFn){try{closeFn();}catch(_){}}}};
$('#addPromi').onclick=()=>{if(!window.promiRequis($('#fTitle')))return;const t=$('#fTitle').value.trim();try{if(window.printTirage)window.printTirage('addPromi',function(){var _cs=document.getElementById('createSheet');if(_cs)_cs.style.transition='none';closeAll();requestAnimationFrame(function(){requestAnimationFrame(function(){if(window._toileDefer){var _q=window._toileDefer;window._toileDefer=null;_q.forEach(function(fn){try{fn();}catch(_){}});}relayout();caption();if(window.syncAll)window.syncAll();});});if(_cs)setTimeout(function(){_cs.style.transition='';},80);});}catch(e){}var _impEl=document.querySelector('#impSeg .is.on');var _impV=_impEl?({light:1,normal:2,high:3}[_impEl.dataset.imp]||2):2;var _urgEl=document.querySelector('#urgSeg .is.on');var _urgV=_urgEl?(+_urgEl.dataset.urg||2):2;var _nEl=document.getElementById('fNote');var _nV=_nEl?_nEl.value.trim():'';var _recips=(typeof window.newWhoSel!=='undefined'&&window.newWhoSel&&window.newWhoSel.length)?window.newWhoSel.slice():[];if(!_recips.length){var _typed=$('#fWho')&&$('#fWho').value.trim();if(_typed&&_typed.toLowerCase()!=='moi'&&_typed.indexOf(',')<0)_recips=[_typed];}if(!_recips.length)_recips=['moi'];if(_recips.length>1)_recips=_recips.filter(function(r){return r&&r!=='moi';});var _made=[];_recips.forEach(function(w){const np=P(t,w,due,_impV,'encours',selNuee||undefined);np.urg=_urgV;if(_nV)np.note=_nV;try{if(window._csDueISO)np.dueISO=window._csDueISO;}catch(_dz){}try{if(window._csEnLair){np.enLair=true;np.due=null;}}catch(_el){}try{var _wl=window.csWhoList?window.csWhoList('whoChips'):[];if(_wl.length)np.aussi=_wl.slice();}catch(_w){}try{if(window.csSens){np.phraseSens=window.csSens();
  if(np.phraseSens==='demander'){ np.req=true; np.reqEtat='attente'; np.reqLe=Date.now(); }
  else if(np.phraseSens==='chiche'){ np.chiche=true; np.chicheEtat='lance'; try{ var _av=(window._phrase&&window._phrase.avec)||''; if(_av)np.avec=_av; }catch(_){} }
}}catch(_e){}try{if(window.csGetFiles){var _cf=window.csGetFiles();if(_cf&&_cf.length)np.files=_cf.slice();}}catch(_e){}computeBox();np.x=box.x+box.w/2+rand(-8,8);np.y=box.y+box.h/2+rand(-8,8);np.tx=np.x;np.ty=np.y;promises.push(np);(window._toileDefer=window._toileDefer||[]).push((function(np){return function(){try{if(window.Toile){if(np.nuee){window.Toile.addNuee(np.nuee);window.Toile.addMember(np.nuee,np.id);}else{window.Toile.addPromi(np.id);}}}catch(e){}};})(np));_made.push(np);if(typeof feedAdd==='function')feedAdd('added','Tu as planté « '+t+' »'+((w&&w!=='moi')?' pour '+w:''),{pid:np.id});});justPlanted=_made.length?_made[_made.length-1].id:null;try{if(!window._tutoSeen){window._tutoSeen=true;setTimeout(function(){try{startTuto(true);}catch(e){}},450);}}catch(e){}$('#fTitle').value='';$('#fWho').value='';if(typeof window.newWhoSel!=='undefined')window.newWhoSel=[];try{window._csDueISO=null;window._csEnLair=false;}catch(_dz){}if(_made.length>1&&typeof toast==='function')toast(_made.length+' Promi plantés');var _nR=document.getElementById('fNote');if(_nR)_nR.value='';selNuee=null;var _tc=document.getElementById('fToAll');if(_tc)_tc.checked=false;var _tf=document.getElementById('toAllField');if(_tf)_tf.style.display='none';setTimeout(()=>{justPlanted=null;render();},1700);};
$('#addNuee').onclick=()=>{if(!window.promiRequis(document.getElementById('nName')))return;const nm=$('#nName').value.trim();if(!nm){toast('Donne un nom à ton Cercle');return;}try{if(window.printTirage)window.printTirage('addNuee',function(){var _cs=document.getElementById('createSheet');if(_cs)_cs.style.transition='none';closeAll();requestAnimationFrame(function(){requestAnimationFrame(function(){if(window._toileDefer){var _q=window._toileDefer;window._toileDefer=null;_q.forEach(function(fn){try{fn();}catch(_){}});}/* la Nuée fraîche : Toile.addNuee enregistre le groupe mais pas la dalle du 1er Promi comme addPromi → dalleTrame échouait (bande vide + Promi absent de la Toile). Un Toile.sync des ids réels le répare (API publique, déjà utilisée ailleurs). */try{if(window.Toile&&Toile.sync)Toile.sync(promises.filter(function(p){return !p.draft;}).map(function(p){return p.id;}));}catch(_){}relayout();caption();if(window.syncAll)window.syncAll();});});if(_cs)setTimeout(function(){_cs.style.transition='';},80);});}catch(e){}const key='n'+Date.now();NUE[key]=nm;NUEEMEM[key]=newNueeMembers.slice();const shared=newNueeMembers.length>0;const f=$('#nFirst').value.trim()||'premier Promi';const np=P(f,shared?'le groupe':'moi',7,2,'encours',key,'moi');computeBox();np.x=box.x+box.w/2;np.y=box.y+box.h/2;np.tx=np.x;np.ty=np.y;promises.push(np);(window._toileDefer=window._toileDefer||[]).push((function(np){return function(){try{if(window.Toile){if(np.nuee){window.Toile.addNuee(np.nuee);window.Toile.addMember(np.nuee,np.id);}else{window.Toile.addPromi(np.id);}}}catch(e){}};})(np));justPlanted=np.id;try{if(!window._tutoSeen){window._tutoSeen=true;setTimeout(function(){try{startTuto(true);}catch(e){}},450);}}catch(e){}if(typeof feedAdd==='function')feedAdd('nuee','Tu as créé le Cercle '+nm+(newNueeMembers.length?' · invité '+newNueeMembers.join(', '):''),{});$('#nName').value='';$('#nFirst').value='';newNueeMembers=[];buildNueeMembers();setTimeout(()=>{justPlanted=null;render();},1700);};

/* v104 : arrGlyph supprimée (Arranger la Toile retiré, Tom) */
function buildCreateNuees(){const el=$('#nueeChips');if(!el)return;const nu=Object.keys(NUE);let h='<div class="chip'+(selNuee?'':' on')+'" data-nuee="">Aucune</div>';nu.forEach(k=>{h+='<div class="chip'+(selNuee===k?' on':'')+'" data-nuee="'+k+'">'+_esc(NUE[k]||k)+'</div>';});el.innerHTML=h;$$('#nueeChips .chip').forEach(c=>c.onclick=()=>{selNuee=c.dataset.nuee||null;try{var _csN=document.getElementById('createSheet');if(_csN)_csN.classList.toggle('cs-nuee',!!selNuee);if(window._phrase)window._phrase.qui=selNuee?'tout le monde':'Moi';if(window._phraseRendu)window._phraseRendu();if(window._csVersPhrase)setTimeout(window._csVersPhrase,90);}catch(_e){}$$('#nueeChips .chip').forEach(x=>x.classList.toggle('on',x===c));var _ta=document.getElementById('toAllField');if(_ta)_ta.style.display=selNuee?'block':'none';try{buildWhoChips();}catch(e){}var _fta=document.getElementById('fToAll');if(_fta){_fta.checked=false;_fta.onchange=function(){var on=this.checked;var w=document.getElementById('fWho'),wc=document.getElementById('whoChips');if(w){w.style.opacity=on?'.4':'';w.style.pointerEvents=on?'none':'';w.disabled=on;if(on)w.value='tous les membres';else if(w.value==='tous les membres')w.value='';}if(wc){wc.style.opacity=on?'.4':'';wc.style.pointerEvents=on?'none':'';}};}var _wf=document.getElementById('fWho'),_wc=document.getElementById('whoChips');if(_wf){_wf.style.opacity='';_wf.style.pointerEvents='';_wf.disabled=false;}if(_wc){_wc.style.opacity='';_wc.style.pointerEvents='';}});}
function openCreateForNuee(key){
  /* #3+#4 : planter un Promi DEPUIS une Nuée — la nature (Promi) et la Nuée sont
     DÉJÀ décidées par le clic. On saute l'écran de choix des 3 natures et on arrive
     DROIT sur la phrase, Nuée pré-sélectionnée, barre Peaufiner calée en bas (build
     flex + versPhrase, exactement comme le vrai parcours createBtn→tuile). */
  selNuee=key;createKind='promi';
  var cs=document.getElementById('createSheet');
  var pf=$('#promiForm');if(pf)pf.style.display='block';
  var nf=$('#nueeForm');if(nf)nf.style.display='none';
  var df=$('#draftForm');if(df)df.style.display='none';
  openSheet(cs);
  try{if(window._csBuildFlex)window._csBuildFlex();}catch(_){}
  try{
    cs.setAttribute('data-kind','promi');cs.classList.add('cs-nuee');
    $$('#createSheet .tile').forEach(function(x){x.classList.toggle('on',x.dataset.kind==='promi');});
    buildCreateNuees();buildWhoChips();
    if(window._phrase)window._phrase.qui='tout le monde';
    if(window._phraseRendu)window._phraseRendu();
    if(window.renderCsDalle)window.renderCsDalle();
    if(window._csColorLabels)window._csColorLabels();
  }catch(e){}
  /* aller à la phrase une fois la fiche disposée (comme le tap sur une tuile) */
  setTimeout(function(){try{if(window._csVersPhrase)window._csVersPhrase();}catch(_){}},140);
}
/* v104 : buildArrange supprimée (Arranger la Toile retiré, Tom) */
var _ctb=$('#cercleTopBtn');if(_ctb)_ctb.onclick=()=>{try{if(typeof closeAll==='function')closeAll();var _ps=document.getElementById('plusScreen');if(_ps)_ps.classList.add('show');if(typeof buildCercleHero==='function')buildCercleHero();}catch(e){}};
if($('#pplusBanner'))$('#pplusBanner').onclick=()=>{ouvreCercle();$('#plusScreen').classList.add('show');if(typeof drawCercleHero==='function')drawCercleHero();if(typeof buildCercleHero==='function')buildCercleHero();};
if($('#openPlus'))$('#openPlus').onclick=()=>{$('#plusScreen').classList.add('show');if(typeof drawCercleHero==='function')drawCercleHero();if(typeof buildCercleHero==='function')buildCercleHero();};
if($('#nInviteAdd'))$('#nInviteAdd').onclick=_addInvite;
if($('#nInvite'))$('#nInvite').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();_addInvite();}});
if($('#esInviteAdd'))$('#esInviteAdd').onclick=_esAddMember;
if($('#esInvite'))$('#esInvite').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();_esAddMember();}});
if($('#replayOnb'))$('#resetApp')&&($('#resetApp').onclick=()=>{try{promises.length=0;for(var _k in NUE){delete NUE[_k];}NUE['soi']='Moi-même';NUEEMEM={};try{if(typeof NUEFILES!=='undefined')NUEFILES={};}catch(_e){}if(window.Toile&&window.Toile.sync)window.Toile.sync([]);if(typeof relayout==='function')relayout();if(typeof render==='function')render();if(typeof buildIndex==='function')buildIndex();if(typeof buildFeed==='function')buildFeed();if(typeof buildAura==='function')buildAura();if(typeof caption==='function')caption();if(typeof closeAll==='function')closeAll();if(typeof replayIntro==='function')replayIntro();if(typeof toast==='function')toast('App réinitialisée');}catch(e){}});
$('#replayOnb').onclick=()=>{window._tutoSeen=false;$('#settingsScreen').classList.remove('show');replayIntro();};

/* --- LA LANGUE --- */
var LANGS=[['fr','Français'],['en','English'],['es','Español'],['de','Deutsch'],['it','Italiano'],['pt','Português']];
var _lang=(function(){try{return localStorage.getItem('promi_lang')||'fr';}catch(e){return 'fr';}})();
function buildLang(){
  var el=$('#langList'); if(!el)return;
  el.innerHTML=LANGS.map(function(L){
    var on=(L[0]===_lang);
    return '<div class="scard" data-lang="'+L[0]+'"><span class="k">'+L[1]+'</span>'+
           '<span class="v ac">'+(on?'✓':'')+'</span></div>';
  }).join('');
  $$('#langList .scard').forEach(function(c){
    c.onclick=function(){
      _lang=c.getAttribute('data-lang');
      try{localStorage.setItem('promi_lang',_lang);}catch(e){}
      var nom=(LANGS.find(function(L){return L[0]===_lang;})||LANGS[0])[1];
      var v=$('#langV'); if(v)v.textContent=nom+' ›';
      buildLang();
      if(_lang!=='fr'&&typeof toast==='function')toast(nom+' arrive bientôt · Promi reste en français');
    };
  });
}
if($('#langCard'))$('#langCard').onclick=function(){
  buildLang();
  $('#settingsScreen').classList.remove('show');
  $('#langScreen').classList.add('show');
};
(function(){var nom=(LANGS.find(function(L){return L[0]===_lang;})||LANGS[0])[1];var v=$('#langV');if(v)v.textContent=nom+' ›';})();

/* --- LA CONFIDENTIALITÉ --- */
if($('#privCard'))$('#privCard').onclick=function(){
  var n=promises.length;
  var c=$('#pvCount'); if(c)c.textContent=n+' Promi'+(n>1?'':'');
  $('#settingsScreen').classList.remove('show');
  $('#privScreen').classList.add('show');
};
if($('#pvExport'))$('#pvExport').onclick=function(){
  try{
    var d=JSON.stringify({promises:promises,NUE:NUE,NUEEMEM:NUEEMEM,PEOPLE:PEOPLE},null,2);
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(d).then(function(){toast('Tes données sont dans le presse-papier');},
                                            function(){toast('Copie impossible ici');});
    }else{toast('Copie impossible ici');}
  }catch(e){toast('Copie impossible ici');}
};
if($('#pvReset'))$('#pvReset').onclick=function(){
  var b=$('#pvReset').querySelector('.v');
  if(b&&b.dataset.armed!=='1'){b.dataset.armed='1';b.textContent='sûr ? touche encore';return;}
  try{localStorage.clear();}catch(e){}
  location.reload();
};
/* le statut de sauvegarde restait sur « vérification… » tant qu'aucun enregistrement n'avait eu lieu */
(function(){
  /* le statut de sauvegarde restait sur « vérification… » tant qu'aucun enregistrement
     n'avait eu lieu : on le rafraîchit au moment PRÉCIS où les Réglages s'ouvrent */
  var s=document.getElementById('settingsScreen'); if(!s||!window.MutationObserver)return;
  var vu=false;
  new MutationObserver(function(){
    var ouvert=s.classList.contains('show');
    if(ouvert===vu)return;                  /* rien n'a changé : on ne fait rien */
    vu=ouvert;
    if(!ouvert)return;
    try{updateSaveStatus(!!localStorage.getItem('promi_state'));}catch(e){}
  }).observe(s,{attributes:true,attributeFilter:['class']});
})();
if($('#notifCard'))$('#notifCard').onclick=()=>{var t=$('#notifTog');if(!t)return;if(t.classList.contains('off')){enableNotifs();}else{notifOn=false;t.classList.add('off');if(typeof queueSave==='function')queueSave();}};
var _resetArm=false;
if($('#resetData'))$('#resetData').onclick=function(){var v=$('#resetV');if(!_resetArm){_resetArm=true;if(v){v.textContent='tout effacer ?';v.style.color='var(--rate)';}setTimeout(function(){_resetArm=false;if(v){v.textContent='effacer ›';v.style.color='';}},3000);return;}try{localStorage.removeItem('promi_state');}catch(e){}try{promises.length=0;nid=100;_fid=1;if(typeof PEOPLE!=='undefined'&&PEOPLE.length)PEOPLE.length=0;if(typeof FEED!=='undefined')FEED.length=0;feedReacted={};shareHidden={};for(var _k in NUEEMEM)delete NUEEMEM[_k];for(var _k2 in NUE)delete NUE[_k2];seeded=false;}catch(e){}try{if(typeof kick==='function')kick();render();caption();if(window.syncAll)window.syncAll();if(typeof buildAura==='function')buildAura();if(typeof buildFeed==='function')buildFeed();if(typeof updateFeedDot==='function')updateFeedDot();}catch(e){}try{$('#settingsScreen').classList.remove('show');}catch(e){}try{if(typeof saveState==='function')saveState();}catch(e){}};
$$('#viewSwitch button').forEach(function(b){b.onclick=function(){setView(b.getAttribute('data-view'));};});
if($('#fdClose'))$('#fdClose').onclick=function(){setView('toile');};
if($('#ixSortChev'))$('#ixSortChev').onclick=function(){var t=$('#ixToFeed');if(t)t.click();};
var ixQuery='';var ixSortMode='recent';function _personKey(p){return (p.from&&p.from!=='moi')?p.from:(p.who||'');}function _isMoiKey(k){k=(''+k).trim().toLowerCase();return k===''||k==='moi'||k===(USER.name||'').trim().toLowerCase();}function ixSortBy(a,b){if(ixSortMode==='personne'){var ka=_personKey(a),kb=_personKey(b);var pa=_isMoiKey(ka)?'__moi':ka,pb=_isMoiKey(kb)?'__moi':kb;var _m=(window._ixPOrder||{});var ra=(_m[pa]!=null?_m[pa]:999),rb=(_m[pb]!=null?_m[pb]:999);if(ra!==rb)return ra-rb;var c=(''+ka).localeCompare(''+kb);if(c!==0)return c;}else if(ixSortMode==='nuee'){var na=''+((typeof NUE!=='undefined'&&NUE[a.nuee])||a.nuee||'~~'),nb=''+((typeof NUE!=='undefined'&&NUE[b.nuee])||b.nuee||'~~');var cn=na.localeCompare(nb);if(cn!==0)return cn;}return a.due-b.due;}
if($('#ixSearch'))$('#ixSearch').oninput=function(e){ixQuery=e.target.value;buildIndex();};
if($('#ixSort'))$$('#ixSort button').forEach(function(b){b.onclick=function(){ixSortMode=b.dataset.s;$$('#ixSort button').forEach(function(x){x.classList.toggle('on',x===b);});buildIndex();};});
var fdQuery='';var fdSortMode='recent';
if($('#fdSearch'))$('#fdSearch').oninput=function(e){fdQuery=e.target.value;buildFeed();};
if($('#fdSort'))$$('#fdSort button').forEach(function(b){b.onclick=function(){fdSortMode=b.dataset.s;$$('#fdSort button').forEach(function(x){x.classList.toggle('on',x===b);});buildFeed();};});
if($('#dWhoInput'))$('#dWhoInput').onchange=function(){if(cur){cur.who=($('#dWhoInput').value.trim()||'moi');render();caption();if(window.syncAll)window.syncAll();}};
if($('#dNote'))$('#dNote').oninput=function(){if(cur){cur.note=$('#dNote').value;if(typeof queueSave==='function')queueSave();}};
if($('#actRelance'))$('#actRelance').onclick=function(){if(!cur)return;var tg=(cur.from&&cur.from!=='moi')?cur.from:cur.who;cur.relances=(cur.relances||0)+1;if(typeof feedAdd==='function')feedAdd('relance','Tu as relancé '+tg+' sur « '+cur.title+' »',{pid:cur.id});renderDetail();if(typeof queueSave==='function')queueSave();};
function _cmWho(p){return (p.nuee&&p.nuee!=='soi')?((typeof NUE!=='undefined'&&NUE[p.nuee])||p.nuee):((p.from&&p.from!=='moi')?p.from:((p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:null));}
function _cmRender(root){try{root=root||document;[].forEach.call(root.querySelectorAll('.cm-block[data-cmb]'),function(box){var pid=+box.getAttribute('data-cmb');var p=promises.filter(function(x){return x.id===pid;})[0];if(!p)return;function draw(){var cm=p.comments||[];var who=_cmWho(p);var all=box.getAttribute('data-all')==='1';var show=all?cm:cm.slice(-2);var h=(!all&&cm.length>2)?'<div class="cm-more">voir les '+cm.length+' commentaires</div>':'';h+=show.map(function(c){var by=c.by||'moi';var me=(by==='moi'||(typeof USER!=='undefined'&&USER.name&&by===USER.name));return '<div class="cm-i'+(me?' mine':'')+'"><span class="cm-by">'+_esc(me?'Moi':by)+'</span> '+_esc(c.t)+'</div>';}).join('');h+='<div class="cm-add"><input placeholder="\u00e9crire un commentaire\u2026" autocomplete="off"><button type="button">+</button></div>';if(who)h+='<div class="cm-vis">visible par '+_esc(who)+'</div>';box.innerHTML=h;var inp=box.querySelector('.cm-add input'),btn=box.querySelector('.cm-add button'),mr=box.querySelector('.cm-more');if(mr)mr.onclick=function(e){e.stopPropagation();box.setAttribute('data-all','1');draw();};function send(){var v=inp.value.trim();if(!v)return;if(!p.comments)p.comments=[];p.comments.push({t:v,d:new Date().toISOString(),by:(typeof USER!=='undefined'&&USER.name)?USER.name:'moi'});inp.value='';draw();try{if(typeof queueSave==='function')queueSave();}catch(e){}try{var rw=box.previousElementSibling;var bd=rw&&rw.querySelector?rw.querySelector('.ix-cm b'):null;if(bd)bd.textContent=p.comments.length;}catch(e){}}btn.onclick=function(e){e.stopPropagation();send();};inp.onclick=function(e){e.stopPropagation();};inp.addEventListener('keydown',function(e){e.stopPropagation();if(e.key==='Enter'){e.preventDefault();send();}});}draw();});}catch(e){}}
function _cmInline(pid,row){try{if(!row)return;var nx=row.nextElementSibling;if(nx&&nx.classList&&nx.classList.contains('cm-inline')){nx.remove();return;}[].forEach.call(document.querySelectorAll('.cm-inline'),function(x){x.remove();});var p=promises.filter(function(x){return x.id===pid;})[0];if(!p)return;var box=document.createElement('div');box.className='cm-inline';function draw(){var cm=p.comments||[];var who=(p.nuee&&p.nuee!=='soi')?((typeof NUE!=='undefined'&&NUE[p.nuee])||p.nuee):((p.from&&p.from!=='moi')?p.from:((p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:null));box.innerHTML='<div class="cm-vis">'+(who?('visible par '+_esc(who)+' \u00b7 chacun peut r\u00e9pondre'):'priv\u00e9 \u2014 personne d\'autre ne le voit')+'</div>'+(cm.length?cm.map(function(c){var by=c.by||'moi';var me=(by==='moi'||(typeof USER!=='undefined'&&USER.name&&by===USER.name));return '<div class="cm-i'+(me?' mine':'')+'"><span class="cm-by">'+_esc(me?'Moi':by)+'</span> '+_esc(c.t)+'</div>';}).join(''):'<div class="cm-empty">aucun commentaire</div>')+'<div class="cm-add"><input placeholder="\u00e9crire un commentaire\u2026" autocomplete="off"><button type="button">+</button></div>';var inp=box.querySelector('input'),btn=box.querySelector('button');function send(){var v=inp.value.trim();if(!v)return;if(!p.comments)p.comments=[];p.comments.push({t:v,d:new Date().toISOString(),by:(typeof USER!=='undefined'&&USER.name)?USER.name:'moi'});inp.value='';draw();try{if(typeof queueSave==='function')queueSave();}catch(e){}try{var bd=row.querySelector('.ix-cm b');if(bd)bd.textContent=p.comments.length;}catch(e){}}btn.onclick=function(e){e.stopPropagation();send();};inp.onclick=function(e){e.stopPropagation();};inp.addEventListener('keydown',function(e){e.stopPropagation();if(e.key==='Enter'){e.preventDefault();send();}});}draw();row.parentNode.insertBefore(box,row.nextSibling);}catch(e){}}
function _addComment(){var inp=$('#dCommentInput');if(!inp||!cur)return;var v=inp.value.trim();if(!v)return;if(!cur.comments)cur.comments=[];cur.comments.push({t:v,d:new Date().toISOString(),by:(typeof USER!=='undefined'&&USER.name)?USER.name:'moi'});inp.value='';renderDetail();if(typeof feedAdd==='function'){var _au=cur.nuee?((typeof NUE!=='undefined'&&NUE[cur.nuee])||cur.nuee):((cur.from&&cur.from!=='moi')?cur.from:cur.who);feedAdd('comment','Tu as commenté « '+cur.title+' »'+(_au?' · '+_au:''),{pid:cur.id});}if(typeof queueSave==='function')queueSave();}
if($('#dCommentAdd'))$('#dCommentAdd').onclick=_addComment;
if($('#dCommentInput'))$('#dCommentInput').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();_addComment();}});
if($('#sealShare'))$('#sealShare').onclick=function(){if(typeof openShare==='function')openShare();try{var nb=document.querySelector('#shMode button[data-mode=pelote]');if(nb)nb.click();}catch(e){}};
if($('#sealShareBtn'))$('#sealShareBtn').onclick=shareSeal;
$$('#sealFmts button').forEach(function(b){b.onclick=function(){$$('#sealFmts button').forEach(function(x){x.classList.toggle('on',x===b);});renderSeal(b.getAttribute('data-f'));};});
$$('#sealTheme button').forEach(function(b){b.onclick=function(){$$('#sealTheme button').forEach(function(x){x.classList.toggle('on',x===b);});_sealDark=(b.getAttribute('data-t')==='dark');renderSeal();};});
if($('#sealPctTog'))$('#sealPctTog').onclick=function(){_sealShowPct=!_sealShowPct;this.classList.toggle('on',_sealShowPct);if(typeof renderSeal==='function')renderSeal(_sealFmt);};if($('#sealBalTog'))$('#sealBalTog').onclick=function(){_sealShowBalance=!_sealShowBalance;this.classList.toggle('on',_sealShowBalance);if(typeof renderSeal==='function')renderSeal(_sealFmt);};$$('#sealParts button').forEach(function(b){b.onclick=function(){var key=b.getAttribute('data-p');_sealParts[key]=!_sealParts[key];if(!_sealParts.noyau&&!_sealParts.pelote&&!_sealParts.prometteurs&&!_sealParts.disques){_sealParts[key]=true;}b.classList.toggle('on',!!_sealParts[key]);renderSeal();};});
if($('#sealOvClose'))$('#sealOvClose').onclick=function(){var o=$('#sealOv');if(o)o.classList.remove('show');};
if($('#sealOv'))$('#sealOv').onclick=function(e){if(e.target&&e.target.id==='sealOv')e.target.classList.remove('show');};
if($('#addDraft'))$('#addDraft').onclick=function(){try{if(window.printTirage)window.printTirage('addDraft',function(){var _cs=document.getElementById('createSheet');if(_cs)_cs.style.transition='none';closeAll();requestAnimationFrame(function(){requestAnimationFrame(function(){if(window._toileDefer){var _q=window._toileDefer;window._toileDefer=null;_q.forEach(function(fn){try{fn();}catch(_){}});}if(typeof caption==='function')caption();if(window.syncAll)window.syncAll();});});if(_cs)setTimeout(function(){_cs.style.transition='';},80);});}catch(e){}if(!window.promiRequis(document.getElementById('dfTitle')))return;if(window.dfKind&&window.dfKind()==='innuee'){var _dn=document.querySelector('#dfNueeChips .chip.on');if(!_dn){try{if(navigator.vibrate)navigator.vibrate(12);}catch(_v){}var _nb=document.querySelector('#draftForm .f-nuee');if(_nb){_nb.classList.remove('req-vide');void _nb.offsetWidth;_nb.classList.add('req-vide');setTimeout(function(){_nb.classList.remove('req-vide');},1500);}return;}}var t=$('#dfTitle').value.trim();var w=($('#dfWho')?$('#dfWho').value.trim():'')||'moi';var np=P(t,w,30,2,'encours');np.draft=true;try{np.dk=(window.dfKind?window.dfKind():'solo');var _dn=document.getElementById('dfNote');if(_dn&&_dn.value.trim())np.note=_dn.value.trim();}catch(_e){}computeBox();np.x=box.x+box.w/2;np.y=box.y+box.h/2;np.tx=np.x;np.ty=np.y;promises.push(np);/* le brouillon apparaît aussi sur la Toile (dalle distincte) */(window._toileDefer=window._toileDefer||[]).push((function(np){return function(){try{if(window.Toile&&window.Toile.addPromi)window.Toile.addPromi(np.id);}catch(e){}};})(np));if($('#dfTitle'))$('#dfTitle').value='';if($('#dfWho'))$('#dfWho').value='';if(typeof feedAdd==='function')feedAdd('added','Tu as mis de côté « '+t+' »',{});};
try{['gesturestart','gesturechange','gestureend'].forEach(function(ev){document.addEventListener(ev,function(e){e.preventDefault();},{passive:false});});}catch(e){}
try{seedFeed();updateFeedDot();}catch(e){}
if($('#plusCta'))$('#plusCta').onclick=()=>{_premium=true;$('#plusCta').textContent='Tu es Membre Ma Parole ! ✓';if(typeof toast==='function')toast('Tu es Membre Ma Parole ! · Cercles illimités');};


function bullet(p){
  const c=p.status==='tenu'?'#90B2CA':p.status==='rate'?'#9a6b5e':'var(--verm)';
  /* la dalle de l'Index est la MÊME que celle de la Toile : on lui demande sa forme.
     (un brouillon n'est pas planté : il garde la silhouette en pointillé) */
  let d=null;
  try{ if(!p.draft&&window.Toile&&window.Toile.shapeOf) d=window.Toile.shapeOf(p.id,30); }catch(e){}
  if(!d) d='M7 9 L20 7 L24 16 L17 24 L7 21 Z';
  const dash=p.draft?' stroke-dasharray="2.6 2.6"':'';
  /* un Promi plante affiche sa vraie dalle ; un brouillon garde la silhouette en pointille */
  if(!p.draft) return `<canvas class="bul mini-dalle" width="72" height="72" data-mini="${p.id}"></canvas>`;
  return `<svg class="bul" viewBox="0 0 30 30"><path d="${d}" fill="none" stroke="${c}" stroke-width="1.7" stroke-linejoin="round"${dash}/></svg>`;
}
function auraDisques(noms,taille){
  /* La rangée de disques de la fiche (Décision Tom, lot disques) :
     1 · TON HARMONIE GLOBALE en premier — « toi » + son mot d'harmonie (le mot reste,
         sa suppression est une décision produit en attente).
     2 · un disque par ENTITÉ concernée (personne ou Nuée) : PRÉNOM/NOM seul, AUCUN
         chiffre ni mot — c'est le remplissage de l'anneau qui montre ton harmonie
         envers elle (yourE/T/R), sans valeur lisible.
     Grille d'anneaux, ordre déjà fixé par l'appelant (alpha ; Chiche = défié→compagnon).
     Réutilise karmaCircle + karmaRing/drawKRing + openPerson (via peintDisques). */
  try{
    if(typeof karmaCircle!=='function') return '';
    taille=taille||52;
    var c=karmaCircle()||[];
    /* 1 · l'harmonie globale : ta parole (envers les autres), comme l'Aura/le Noyau */
    var _act=promises.filter(function(x){return !x.draft;});
    var _mine=_act.filter(function(x){return (!x.from||x.from==='moi');});
    var gt=_mine.filter(function(x){return x.status==='tenu';}).length,
        gr=_mine.filter(function(x){return x.status==='rate';}).length,
        ge=_mine.filter(function(x){return x.status==='encours';}).length;
    /* Décision Tom : AUCUN mot sous aucun disque, y compris le tien — « toi » et rien
       d'autre. harmonyWord() reste dans le code (utilisé ailleurs), il ne s'affiche
       simplement plus ici. */
    var h='<div class="aura-track"><div class="kring kring-moi">'
      +'<div class="kr-wrap">'+karmaRing(ge,gt,gr,taille)+'</div>'
      +'<div class="kr-n">Toi</div></div>';
    /* 2 · les entités concernées — prénom/nom seul, sans mot ni chiffre */
    (noms||[]).forEach(function(n){
      if(n && typeof n==='object' && n.nuee){
        /* une Nuée : UN disque, agrégat de ses promesses */
        var _in=promises.filter(function(x){return !x.draft && x.nuee===n.nuee;});
        var nt=_in.filter(function(x){return x.status==='tenu';}).length,
            nr=_in.filter(function(x){return x.status==='rate';}).length,
            ne=_in.filter(function(x){return x.status==='encours';}).length;
        var nom=(typeof NUE!=='undefined'&&NUE[n.nuee])||n.nuee;
        h+='<div class="kring" data-nuee="'+_esc(n.nuee)+'" style="cursor:pointer">'
          +'<div class="kr-wrap">'+karmaRing(ne,nt,nr,taille)+'</div>'
          +'<div class="kr-n">'+_esc(nom)+'</div></div>';
        return;
      }
      /* une personne : le remplissage montre TON harmonie envers elle (yourE/T/R) */
      var o=c.filter(function(x){return x.name===n;})[0];
      var e2,t2,r2;
      if(o){ e2=o.yourE; t2=o.yourT; r2=o.yourR; }
      else { var items=promises.filter(function(p){ return !p.draft && (p.who===n||p.from===n); });
        e2=0;t2=0;r2=0; items.forEach(function(p){ if(p.status==='tenu')t2++; else if(p.status==='rate')r2++; else e2++; }); }
      h+='<div class="kring" data-p="'+_esc(n)+'" style="cursor:pointer">'
        +'<div class="kr-wrap">'+karmaRing(e2,t2,r2,taille)+'</div>'
        +'<div class="kr-n">'+_esc(n)+'</div></div>';
    });
    return h+'</div>';
  }catch(e){ return ''; }
}
function peintDisques(root){ try{
  var r=root||document;
  r.querySelectorAll('.kr-c').forEach(function(cv){ try{ if(typeof drawKRing==='function') drawKRing(cv); }catch(e){} });
  /* meme geste que dans l'Aura : on ouvre la fiche de la personne */
  r.querySelectorAll('.kring[data-p]').forEach(function(el){
    el.onclick=function(){ var n=el.getAttribute('data-p');
      if(n&&typeof openPerson==='function'){ try{ if(typeof closeAll==='function') closeAll(); }catch(_){}
        openPerson(n); } };
  });
  /* le disque d'une Nuée ouvre la Nuée */
  r.querySelectorAll('.kring[data-nuee]').forEach(function(el){
    el.onclick=function(){ var k=el.getAttribute('data-nuee');
      if(k&&typeof openEssaim==='function'){ try{ if(typeof closeAll==='function') closeAll(); }catch(_){}
        openEssaim(k); } };
  });
}catch(e){} }
window.auraDisques=auraDisques; window.peintDisques=peintDisques;
/* ⚑ v100 — UN SEUL BUDGET PAR TÂCHE pour les peintres qui savent reprendre au passage suivant (la bande d'une Nuée, les
   vignettes) : chacun avait le sien, et ils s'additionnaient dans la même tâche (384 · 282 · 411 ms mesurés). L'horloge part au
   premier appel et repart à zéro À L'IMAGE SUIVANTE — pas à la fin du rappel : plusieurs rappels d'image (pose de la fiche,
   bande, vignettes) s'enchaînent dans une même image, et chacun reprenait 40 ms. */
window._budgetTache=function(){ var B=window._bdgT||(window._bdgT={t0:0,on:false});
  if(!B.on){ B.on=true; B.t0=performance.now(); requestAnimationFrame(function(){ B.on=false; }); }
  return performance.now()-B.t0; };
/* ⚑ v102 — L'AGRANDISSEMENT DES FACES, UNE SEULE FOIS. `size-adjust:112%` (v96) sur Gilbert et Atkinson : toute cote qui traduit
   une TAILLE en HAUTEUR DE LIGNE le multiplie par ce facteur. Il ne vit qu'ici ; les `@font-face` le portent en dur. */
window._echTexte=1.12;
/* ce que l'agrandissement ajoute à l'ENCRE d'un bloc de Gilbert, au-dessus et au-dessous de sa boîte (mesuré sur les fiches, avant/après
   v96 : titre 42 → 4 et 3 ; à-qui 23 → 2 et 2 ; noms des Noyaux 14 → 1 et 1). Une cote « bloc + air » l'ajoute à son air. */
window._encreSup=function(fs){ var d=(+fs||0)*((window._echTexte||1)-1); return {haut:d*0.8, bas:d*0.62}; };
function peintMinis(root){ try{
  /* chaque canvas est peint, meme si plusieurs partagent le meme id :
     le L d'une Nuee repete les dalles de ses Promi. */
  /* ⚑ v100 — LE BUDGET (comme la bande d'une Nuée) : au-delà de 40 ms dans un passage, une vignette dont la dalle n'est pas
     prête n'est ni effacée ni rendue ; un passage est redemandé à l'image suivante. Mesuré : 17 rendus d'affilée, 190 ms, dans
     l'appel synchrone d'ouverture d'une Nuée. */
  var _reste=false;
  (root||document).querySelectorAll('canvas.mini-dalle').forEach(function(cv){
    var id=+cv.getAttribute('data-mini'); if(!id) return;
    if(window._budgetTache()>40 && window._rendDalle && !window._rendDalle(id, cv.width, cv.height, {siPret:1})){ _reste=true; return; }
    var g=cv.getContext('2d'); if(!g) return;
    /* ⚑ v29 — rendue À SA TAILLE et posée 1:1 (redteam_decoupe) : plus d'agrandissement d'une dalle à k = 1 */
    g.save(); g.setTransform(1,0,0,1,0,0); g.clearRect(0,0,cv.width,cv.height);
    var _pd=window._poseDalle?window._poseDalle(g,id,0,0,cv.width,cv.height):null; g.restore();
    if(!_pd) return;
    var w=_pd.w, h=_pd.h;
    /* ⚑ Q74 · UNE MINI-DALLE EST DE LA MATIÈRE, ET ELLE LE DÉCLARE. Les canevas
       `.mini-dalle` portent la vraie dalle du moteur — dans le fil d'une Nuée, dans le L
       d'une carte, partout où l'app montre un Promi en réduction. Sans cette ligne, le
       comparateur comptait chacune comme un écart de dessin. Les unités sont celles du
       canevas, d'où la base. */
    try{ cv.setAttribute('data-matiere',
           [Math.round((cv.width-w)/2),Math.round((cv.height-h)/2),
            Math.round(w),Math.round(h)].join(','));
         cv.setAttribute('data-matiere-base', cv.width+','+cv.height); }catch(_){}
  });
  if(_reste){ var _r=root; requestAnimationFrame(function(){ setTimeout(function(){ try{ if(!_r || _r===document || document.contains(_r)) window.peintMinis(_r); }catch(_){ } }, 0); }); }
}catch(e){} }
window.peintMinis=peintMinis;
function nueeMini(key){try{var fp=promises.find(function(p){return p.nuee===key&&!p.draft;});if(fp&&window.Toile&&window.Toile.shapeOf&&window.Toile.shapeOf(fp.id,28)){return `<canvas class="bul mini-dalle" width="72" height="72" data-mini="${fp.id}"></canvas>`;}}catch(e){}return nueeBullet();}
function nueeBullet(){return `<svg class="bul" viewBox="0 0 30 30"><circle cx="11" cy="13" r="2.6" fill="var(--verm)"/><circle cx="18.5" cy="11" r="2" fill="#B6A384"/><circle cx="17.5" cy="18.5" r="2" fill="#B6A384"/><circle cx="10" cy="19.5" r="1.8" fill="#B6A384"/></svg>`;}
function peopleList(){var s=new Set(PEOPLE);promises.forEach(function(p){if(p.who&&p.who!=='moi'&&p.who!=='le groupe')s.add(p.who);if(p.from&&p.from!=='moi')s.add(p.from);});Object.keys(NUEEMEM).forEach(function(k){(NUEEMEM[k]||[]).forEach(function(n){s.add(n);});});return Array.from(s);}
function _ini(n){n=(n||'').trim();if(!n)return '?';var pr=n.split(/\s+/);return (pr.length>1?pr[0][0]+pr[1][0]:n.slice(0,2)).toUpperCase();}
function _hashN(s){var h=2166136261;s=''+s;for(var i=0;i<s.length;i++){h^=s.charCodeAt(i);h=(h*16777619)>>>0;}return h;}
/* ⚑ 20 sept. (Tom) : « les avatars des Noyaux piochent dans _BPAL, qui garde deux
   teintes d'avant. Aligne-les sur l'identité. » Les deux reliquats #B586F6 et #8CBCFD
   partent ; on garde les QUATRE tons de la palette d'identité, plus les deux états qui
   y étaient déjà (le jaune et le vermillon) — rien qui ne soit au jeu. */
/* ⚑ 21 sept. (Tom) : « les avatars doivent piocher dans l'identité SEULE ». Les quatre tons
   de la palette d'identité, et rien d'autre : le jaune est sorti en v6, et le vermillon est
   un ÉTAT — un visage ne porte jamais un état. */
var _BPAL=['#82AEF8','#FFB8D2','#C9A8F5','#EFE3C7'];
var _noiseCanvas=null;var _NOISE=(function(){try{var c=document.createElement('canvas');c.width=c.height=96;var g=c.getContext('2d');var im=g.createImageData(96,96),d=im.data;for(var i=0;i<d.length;i+=4){var v=140+Math.random()*115;d[i]=d[i+1]=d[i+2]=v;d[i+3]=Math.random()*24;}g.putImageData(im,0,0);_noiseCanvas=c;return c.toDataURL();}catch(e){return '';}})();
try{if(_NOISE)document.documentElement.style.setProperty('--noise','url('+_NOISE+')');}catch(e){}
function _blobBg(seed){var h=_hashN(seed)>>>0;var L=[];for(var i=0;i<4;i++){var hx=Math.imul(h,((i*2+1)*2654435761)>>>0)>>>0;var x=8+(hx%84),y=8+((hx>>>7)%84),sp=38+((hx>>>14)%34),col=_BPAL[(hx>>>3)%_BPAL.length];L.push('radial-gradient(circle at '+x+'% '+y+'%,'+col+' 0%,transparent '+sp+'%)');}var base=_BPAL[(h>>>11)%_BPAL.length];return L.join(',')+',radial-gradient(circle at 50% 50%,'+base+' 0%,'+base+' 100%)';}
function _isMe(n){var s=(''+n).trim();return s.toLowerCase()==='moi'||s===USER.name.trim();}/* ⚑ v94 (Tom, iPhone : « le disque Toi en grand plus un petit disque Moi — deux disques pour la même personne ») — l'onboarding écrit « Moi », la page + « moi » : c'est toujours soi */
function avatarHTML(n){if(_isMe(n)&&USER.photo)return '<span class="ava ava-p" style="background-image:url('+USER.photo+')"></span>';var seed=_isMe(n)?('u'+USER.seed):n;return '<span class="ava ava-blob" style="background:'+_blobBg(seed)+'"></span>';}
/* ⚑ chantier 60 : « à le groupe » → « au groupe », « à les » → « aux » */
function _aQui(w,maj){var s=String(w||'');var r=/^le\s/i.test(s)?'au '+s.slice(3):(/^les\s/i.test(s)?'aux '+s.slice(4):'\u00e0 '+s);return maj?r.charAt(0).toUpperCase()+r.slice(1):r;}
window._aQui=_aQui;
function relLabel(p){var to=(p.who&&p.who!=='moi')?p.who:'';var fr=(p.from&&p.from!=='moi')?p.from:'';if(fr&&to)return 'de '+_esc(fr)+' \u2192 '+_esc(to);if(fr)return 'de '+_esc(fr);if(to)return _aQui(_esc(to));return 'pour toi';}
function buildWhoChips(){var el=$('#whoChips');if(!el)return;var inp=$('#fWho');var cur=(inp&&inp.value.trim())||'';var ppl=(typeof selNuee!=='undefined'&&selNuee&&typeof NUEEMEM!=='undefined'&&NUEEMEM[selNuee]&&NUEEMEM[selNuee].length)?NUEEMEM[selNuee].filter(function(n){return n&&(''+n).toLowerCase()!=='moi'&&!(typeof _isMe==='function'&&_isMe(n));}).slice(0,6):peopleList().filter(function(n){return n&&(''+n).toLowerCase()!=='moi'&&!(typeof _isMe==='function'&&_isMe(n));}).slice(0,6);if(typeof window.newWhoSel==='undefined')window.newWhoSel=[];var _sel=window.newWhoSel;var _moiOn=(!_sel.length)||_sel.indexOf('moi')>=0;var h='<div class="chip'+(_moiOn?' on':'')+'" data-w="moi">Moi</div>';ppl.forEach(function(n){h+='<div class="chip'+(_sel.indexOf(n)>=0?' on':'')+'" data-w="'+_esc(n)+'">'+_esc(n)+'</div>';});el.innerHTML=h;$$('#whoChips .chip').forEach(function(c){c.onclick=function(){var w=c.dataset.w;if(w==='moi'){window.newWhoSel=[];if(inp)inp.value='moi';}else{var _i=window.newWhoSel.indexOf(w);if(_i>=0)window.newWhoSel.splice(_i,1);else window.newWhoSel.push(w);if(inp)inp.value=window.newWhoSel.join(', ')||'moi';}buildWhoChips();};});}
function buildNueeMembers(){var el=$('#nMembers');if(!el)return;var h='';newNueeMembers.forEach(function(n,i){h+='<div class="chip on" data-i="'+i+'">'+avatarHTML(n)+' '+_esc(n)+' \u2715</div>';});peopleList().filter(function(n){return n&&n!=='moi'&&newNueeMembers.indexOf(n)<0;}).slice(0,5).forEach(function(n){h+='<div class="chip" data-add="'+_esc(n)+'">+ '+_esc(n)+'</div>';});el.innerHTML=h;$$('#nMembers .chip[data-i]').forEach(function(c){c.onclick=function(){newNueeMembers.splice(+c.dataset.i,1);buildNueeMembers();};});$$('#nMembers .chip[data-add]').forEach(function(c){c.onclick=function(){newNueeMembers.push(c.dataset.add);buildNueeMembers();};});}
function _addInvite(){var inp=$('#nInvite');if(!inp)return;var v=inp.value.trim();if(v){newNueeMembers.push(v);inp.value='';buildNueeMembers();}}
function buildEsMembers(){var el=$('#esMembers');if(!el)return;var mem=NUEEMEM[curEssaim]||[];var h=mem.length?mem.map(function(n){return '<div class="chip on" data-rm="'+_esc(n)+'">'+avatarHTML(n)+' '+_esc(n)+' \u2715</div>';}).join(''):'<div class="b" style="padding:4px 0">personne pour l\'instant</div>';el.innerHTML=h;$$('#esMembers .chip[data-rm]').forEach(function(c){c.onclick=function(){NUEEMEM[curEssaim]=(NUEEMEM[curEssaim]||[]).filter(function(x){return x!==c.dataset.rm;});buildEsMembers();buildIndex();};});}
function _esAddMember(){var inp=$('#esInvite');if(!inp||!curEssaim)return;var v=inp.value.trim();if(v){if(!NUEEMEM[curEssaim])NUEEMEM[curEssaim]=[];NUEEMEM[curEssaim].push(v);inp.value='';buildEsMembers();buildIndex();}}
function replayIntro(){try{localStorage.removeItem('promi_onb');}catch(e){}try{setView('toile');var _vs=document.querySelector('.viewswitch [data-view=toile]');if(_vs)_vs.click();}catch(e){}if(typeof obReplay==='function'){obReplay();return;}}
function buildIndex(){
  /* L'INDEX EN BLOCS — une seule grille, plein ecran, aucune section.
     Nuees, brouillons et demandes ne sont plus des groupes separes : ce sont
     des FILTRES du menu de tri. Un bloc = une entree, quelle que soit sa nature. */
  var _ixS=document.getElementById('ixSearch');
  var _ixSheet=document.getElementById('indexSheet');
  var _ixList=document.getElementById('indexList');
  try{if(_ixS&&_ixList&&_ixS.parentNode===_ixList&&_ixSheet)_ixSheet.insertBefore(_ixS,_ixList);}catch(e){}
  var _q=(typeof ixQuery!=='undefined'?ixQuery:'').trim().toLowerCase();
  var _f=(window.ixFiltre||'tous');
  function _mt(p){ if(!_q)return true;
    var bag=(p.title||'')+' '+(p.who||'')+' '+(p.from||'')+' '+((NUE&&NUE[p.nuee])||'');
    return bag.toLowerCase().indexOf(_q)>=0; }

  /* on construit une liste unique d'entrees : Nuees puis Promi */
  var ent=[];
  if(_f==='tous'||_f==='nuees'){
    /* ⚑ UNE NUÉE SANS AUCUN PROMI EXISTE QUAND MÊME. La liste se tirait des promesses :
       une Nuée nommée mais pas encore plantée n'y figurait donc jamais. Le cadre 74 la
       montre — « l'atelier du samedi · GARDÉ DE CÔTÉ ». On lit donc `NUE`, la table des
       noms, et pas seulement ce qui pend aux Promi. */
    var nu=[...new Set(promises.map(function(p){return p.nuee;}).filter(Boolean)
             .concat(typeof NUE!=='undefined'?Object.keys(NUE):[]))]
      .filter(function(n){ return !_q||((NUE[n]||n).toLowerCase().indexOf(_q)>=0)
        ||promises.some(function(p){return p.nuee===n&&_mt(p);}); });
    nu.forEach(function(n){
      var c=promises.filter(function(p){return p.nuee===n&&!p.draft;}).length;
      var mem=(typeof NUEEMEM!=='undefined'&&NUEEMEM[n])||[];
      ent.push({kind:'nuee',n:n,titre:(NUE[n]||n),mot:'Cercle',vif:false,col:'#E6D8FA',
        sous:c+' Promi · '+(mem.length?mem.length+' membre'+(mem.length>1?'s':''):'perso')});
    });
  }
  /* ⚑ UNE NUÉE REMPLACE SES PROMI DANS L'INDEX — c'est ce que montrent les cadres 72 et 74.
     L'Index de la planche porte HUIT entrées : planter un arbre · faire les crêpes ·
     le potager · courir dimanche · nager le mardi · le grand plongeoir · l'atelier du
     samedi · appeler Mamie. Les six Promi du potager n'y sont PAS un par un — la Nuée
     tient leur place, et l'entête compte quand même « Index 12 », le nombre de Promi.
     L'app les listait EN PLUS de la Nuée : quatorze entrées pour douze Promi. */
  var _nuLister={};
  ent.forEach(function(E){ if(E.kind==='nuee') _nuLister[E.n]=true; });
  promises.forEach(function(p){
    if(!_mt(p))return;
    if(p.nuee && _nuLister[p.nuee] && !p.draft) return;
    if(p.draft){ if(_f!=='tous'&&_f!=='brouillons')return; }
    else if(p.req){ if(_f!=='tous'&&_f!=='demandes')return; }
    else { if(_f==='brouillons'||_f==='demandes'||_f==='nuees')return;
           /* « Promi » = les vrais Promi, ni Nuee ni brouillon ni demande */
           if(_f==='suspens'&&p.status!=='encours')return;
           if(_f==='manquees'&&p.status!=='rate')return; }
    var T;
    if(p.draft) T={mot:'brouillon',vif:false,col:''};
    else if(p.req) T={mot:'demande',vif:true,col:'#DD4D23'};
    else T=(window.motDuTemps?motDuTemps(p):{mot:'un jour',vif:false,col:''});
    ent.push({kind:'promi',p:p,titre:p.title||'',mot:T.mot,vif:T.vif,col:T.col,clair:!!T.clair,
      sous:(p.nuee?(NUE[p.nuee]||p.nuee):(p.who||'moi'))});
  });
  /* ⚑ L'ORDRE AU REPOS EST CELUI DE LA PLANTATION. (Décision Tom, 20 août 2026 — elle
     remplace « ce qui presse, puis les tenues, puis le reste », et « À tenir en premier »
     reste, en entrée du menu ⇅ : rien n'est perdu.)
     LA RAISON, AU-DELÀ DU CADRE : un tri par urgence est un CLASSEMENT PAR VALEUR, et le
     produit n'en fait nulle part. L'ordre de plantation est chronologique et neutre.
     Les Nuées vont à LEUR PLACE, plus en tête — une Nuée ne vaut pas plus qu'un Promi.
     Les gardés de côté ferment la liste : ils ne sont pas encore plantés.
     Relevé sur les cadres 72 et 74 : planter un arbre · faire les crêpes · le potager ·
     courir dimanche · nager le mardi · le grand plongeoir · l'atelier · appeler Mamie. */
  try{
    var _ordre=function(E){
      if(E.kind!=='nuee') return E.p.id;
      if(window.NUEORD && NUEORD[E.n]!=null) return NUEORD[E.n];
      /* faute de date de lancement, une Nuée se range à sa PREMIÈRE plantation */
      var l=promises.filter(function(q){ return q.nuee===E.n; });
      return l.length ? Math.min.apply(null, l.map(function(q){ return q.id; })) - 0.5 : 1e9;
    };
    /* ⚑ UNE NUÉE SANS AUCUN PROMI EST UN GARDÉ DE CÔTÉ : elle est nommée, pas plantée.
       Le cadre 74 le montre — « l'atelier du samedi · GARDÉ DE CÔTÉ », zéro Promi. */
    var _garde=function(E){
      if(E.kind==='nuee')
        return promises.filter(function(q){ return q.nuee===E.n && !q.draft; }).length ? 0 : 1;
      return (E.p.draft || E.p.req) ? 1 : 0;
    };
    ent.sort(function(a,b){
      var ga=_garde(a), gb=_garde(b); if(ga!==gb) return ga-gb;
      if(window.ixTri==='tenir'){
        var rang=function(E){ if(E.kind==='nuee')return 3;
          if(E.p.status==='rate')return 0; if(E.p.status==='tenu')return 1; return 2; };
        var ra=rang(a), rb=rang(b); if(ra!==rb) return ra-rb;
      } else if(window.ixTri==='personne' || window.ixTri==='nuee'){
        if(a.kind==='promi' && b.kind==='promi'){
          var c=ixSortBy(a.p,b.p); if(c) return c;
        } else if(a.kind!==b.kind) return a.kind==='nuee' ? -1 : 1;
      }
      return _ordre(a)-_ordre(b); }); }catch(e){}

  var h='<div class="ix-blocs">';
  ent.forEach(function(E){
    var fs = E.mot.length<10 ? 27 : (E.mot.length<15 ? 20 : 17);
    var dal='';
    try{
      if(E.kind==='nuee'){
        /* la Toile dezoomee : quatre dalles du monde actif, en L */
        var _ids=[]; try{_ids=promises.filter(function(q){return q.nuee===E.n&&!q.draft;})
          .slice(0,4).map(function(q){return q.id;});}catch(_i){}
        var _pos=[[52,4,0,.88],[28,34,0,.9],[58,52,0,.86],[2,62,0,.88]];
        dal='<div class="ix-nuee-L">';
        for(var _k=0;_k<4;_k++){
          var _id=_ids[_k%Math.max(1,_ids.length)];
          if(_id===undefined)break;
          var _q=_pos[_k];
          dal+='<canvas class="bul mini-dalle" width="144" height="144" data-mini="'+_id+'"'
            +' style="left:'+_q[0]+'%;top:'+_q[1]+'%;opacity:'+_q[3]+'"></canvas>';
        }
        dal+='</div>';
      } else dal = miniCell(E.p);
    }catch(_){}
    var attr = (E.kind==='nuee') ? ('data-nuee="'+E.n+'"') : ('data-id="'+E.p.id+'"');
    /* une Nuee n'a pas de couleur : c'est sa densite de dalles qui la dit. */
    var _nat = E.kind==='nuee' ? ' nuee'
      : (E.p&&E.p.draft) ? ' brouillon'
      : (E.p&&E.p.req) ? ' demande'
      : (E.p&&E.p.chiche) ? ' chiche'          /* accent framboise, dalle gardée (§4) */
      : (E.p&&E.p.status==='tenu') ? ' menthe' : '';
    h+='<div class="ix-bloc'+(E.vif?' vif':'')+(E.clair?' sur-clair':'')+_nat+'" '+attr
      +(E.vif?' style="background:'+E.col+'"':'')+'>'
      +'<div class="ix-bd">'+dal+'</div>'
      +'<div class="ix-bt">'
      +'<div class="ix-bj" style="font-size:'+fs+'px">'+E.mot+'</div>'
      +'<div class="ix-bn">'+_esc(E.titre)+'</div>'
      +'<div class="ix-bw">'+_esc(E.sous)+'</div>'
      +'</div></div>';
  });
  h+='</div>';
  if(!ent.length) h='<div class="ix-empty"><div class="fe-t">Rien ici</div>'
    +'<div class="fe-s">Touche le <b>+</b> pour planter un Promi.</div></div>';
  $('#indexList').innerHTML=h;

  /* le compte a cote du titre.
     ⚑ IL COMPTE LES GARDÉS DE CÔTÉ. « Index » est *la liste complète des Promi*
     (CLAUDE.md §2), et le cadre 72 écrit **12** là où la planche porte 5 Promi hors Nuée,
     6 au potager et 1 gardé de côté — soit 12 exactement. Sans le gardé, on écrivait 11. */
  try{ var _c=document.getElementById('ixCount');
    if(_c)_c.textContent=(function(){var n=promises.filter(function(p){return !p.req&&!p.draft;}).length,m=(typeof NUE!=='undefined')?Object.keys(NUE).length:0;return n+' parole'+(n>1?'s':'')+' · '+m+' Cercle'+(m>1?'s':'');})(); }catch(_){}   /* ⚑ Q213 : l'Index compte comme l'accueil — les gardés de côté restent listés, plus comptés (écart au cadre 72, ECARTS-MOODBOARD § 0 quater) */

  /* les canvas des dalles sont peints APRES l'insertion : sans cet appel,
     les 26 mini-dalles restent vides (§piege des canvas differes). */
  try{ if(window.peintMinis)peintMinis($('#indexList')); }catch(_){}
  /* les dalles doivent etre peintes AVANT qu'on lise leur couleur */
  /* peintMinis differe son travail : on teinte a plusieurs reprises pour
     etre sur d'attraper les canvas une fois peints. */
  /* une seule passe differee suffit : quatre appels par construction
     faisaient ramer l'app au bout de quelques secondes. */
  try{ if(window._teinterTenues) requestAnimationFrame(function(){
    requestAnimationFrame(_teinterTenues); }); }catch(_){}
  try{ if(window._lisibilite) requestAnimationFrame(function(){
    _lisibilite($('#indexList'));
    if(window._titresTeintes)_titresTeintes($('#indexList')); }); }catch(_){}
  try{ if(window._cmRender)_cmRender($('#indexList')); }catch(_){}
  $$('#indexList .ix-bloc[data-id]').forEach(function(r){
    r.onclick=function(){openDetail(+r.dataset.id);};});
  $$('#indexList .ix-bloc[data-nuee]').forEach(function(r){
    r.onclick=function(){openEssaim(r.dataset.nuee);};});
}
let curEssaim=null;
function openEssaim(key){ if(typeof window.openNueeDetail==='function'){ return window.openNueeDetail(key); } curEssaim=key;$('#esTitle').textContent=NUE[key]||key;$('#esName').value=NUE[key]||key;buildEsMembers();const items=promises.filter(p=>p.nuee===key);$('#esList').innerHTML=items.length?items.map(p=>{const s=p.status==='tenu'?'tenue':p.status==='rate'?'à tenir':'en cours';return `<div class="row" data-id="${p.id}">${bullet(p)}<div><div class="a">${_esc(p.title)}</div><div class="b">${relLabel(p)} · ${s}</div></div><div class="chev">›</div></div>`;}).join(''):'<div class="b" style="padding:8px 0">aucun Promi</div>';$$('#esList .row[data-id]').forEach(r=>r.onclick=()=>{closeAll();openDetail(+r.dataset.id);});openSheet($('#essaimSheet'));
try{requestAnimationFrame(function(){if(window.esRefresh)window.esRefresh();});}catch(e){}
try{
  var noms=[];
  promises.filter(function(x){return !x.draft&&x.nuee===key;}).forEach(function(x){
    [x.who,x.from].forEach(function(n){ if(n&&n!=='moi'&&n!=='le groupe'&&noms.indexOf(n)<0) noms.push(n); }); });
  var fold=document.getElementById('esAuraFold'), band=document.getElementById('esAura');
  var h=noms.length?auraDisques(noms,52):'';
  if(fold&&band){ band.innerHTML=h; band.hidden=true;
    fold.style.display=h?'':'none';
    var btn=document.getElementById('esAuraBtn');
    if(btn) btn.onclick=function(){ band.hidden=!band.hidden; if(!band.hidden) peintDisques(band); };
  }
}catch(e){}}
$('#esAddPromi').onclick=()=>{if(curEssaim)openCreateForNuee(curEssaim);};if($('#esShareInvite'))$('#esShareInvite').onclick=()=>{try{var _nm=(typeof NUE!=='undefined'&&NUE[curEssaim])?NUE[curEssaim]:'mon Essaim';var _t='Rejoins mon Cercle \u00ab '+_nm+' \u00bb sur Promi \u2014 nos Promi, tenus ensemble. https://promi.app';try{if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(_t);}catch(e){}if(navigator.share){navigator.share({title:'Promi',text:_t}).then(function(){},function(){});toast('Invitation prête à partager');}else{toast('Invitation copiée · promi.app');}}catch(e){}};
function _renameNuee(){if(!curEssaim)return;var v=$('#esName').value.trim();if(v){NUE[curEssaim]=v;render();buildIndex();$('#esTitle').textContent=v;}}if($('#esName')){$('#esName').onchange=_renameNuee;$('#esName').onblur=_renameNuee;}if($('#esTitle'))$('#esTitle').onclick=function(){if($('#esName'))$('#esName').focus();};
function _dissolveNuee(del){if(!curEssaim)return;if(del){promises=promises.filter(function(p){return p.nuee!==curEssaim;});}else{promises.forEach(function(p){if(p.nuee===curEssaim)p.nuee=null;});}delete NUE[curEssaim];curEssaim=null;closeAll();relayout();buildIndex();caption();}$('#esDissolve').onclick=()=>{if(!curEssaim)return;toast('Dissoudre le Cercle ?','Libérer les Promi',function(){_dissolveNuee(false);},'Tout supprimer',function(){_dissolveNuee(true);});};

let cur=null;
function regenRecur(p){if(!p||!p.recur)return false;var due={daily:1,weekly:7,monthly:30}[p.recur]||7;var np=P(p.title,p.who,due,p.intensity||2,'encours',p.nuee,p.from);np.recur=p.recur;computeBox();np.x=box.x+box.w/2+rand(-8,8);np.y=box.y+box.h/2+rand(-8,8);np.tx=np.x;np.ty=np.y;promises.push(np);try{if(window.Toile){if(np.nuee){window.Toile.addNuee(np.nuee);window.Toile.addMember(np.nuee,np.id);}else{window.Toile.addPromi(np.id);}}}catch(e){}if(typeof feedAdd==='function')feedAdd('added','↻ « '+p.title+' » régénérée',{pid:p.id});return true;}
var notifOn=false;
function buildProfile(){var act=promises.filter(function(p){return !p.draft;});var mine=act.filter(function(p){return (!p.from||p.from==='moi');});var t=mine.filter(function(p){return p.status==='tenu';}).length,r=mine.filter(function(p){return p.status==='rate';}).length,e=mine.filter(function(p){return p.status==='encours';}).length;var res=t+r;var pct=res>0?Math.round(100*t/res):null;var pe=$('#pfPct');if(pe)pe.textContent=(pct==null?'\u2014':pct);var pc=document.querySelector('#profileScreen .pf-pc');if(pc)pc.style.display=pct==null?'none':'';var circle=(typeof karmaCircle==='function')?karmaCircle():[];var sub=$('#pfSub');if(sub)sub.textContent=mine.length+' Promi'+' \u00b7 '+circle.length+' lien'+(circle.length>1?'s':'');var streak=Math.max(0,t-(r>0?1:0));var st=$('#pfStats');if(st)st.innerHTML=[['en cours',e],['tenues',t],['s\u00e9rie',streak],['cercle',circle.length]].map(function(a){return '<div class="pf-stat"><div class="pf-sv">'+a[1]+'</div><div class="pf-sl">'+a[0]+'</div></div>';}).join('');var top=circle.filter(function(o){return o.theirTrust!=null;}).sort(function(a,b){return b.theirTrust-a.theirTrust;}).slice(0,3);var tp=$('#pfTop');if(tp)tp.innerHTML=top.length?top.map(function(o){return '<div class="pf-row"><span class="ava">'+_esc(_ini(o.name))+'</span><div class="pf-rn">'+_esc(o.name)+'</div><div class="pf-rp">'+Math.round(o.theirTrust*100)+'%</div></div>';}).join(''):'<div class="b" style="padding:8px 0;color:var(--gsub)">personne ne t\'a encore tenu parole</div>';var best=circle.filter(function(o){return o.yourTrust!=null;}).sort(function(a,b){return b.yourTrust-a.yourTrust;}).slice(0,3);var bs=$('#pfBest');if(bs)bs.innerHTML=best.length?best.map(function(o){return '<div class="pf-row"><span class="ava">'+_esc(_ini(o.name))+'</span><div class="pf-rn">'+_esc(o.name)+'</div><div class="pf-rp">'+Math.round(o.yourTrust*100)+'%</div></div>';}).join(''):'<div class="b" style="padding:8px 0;color:var(--gsub)">tu n\'as encore rien tenu envers quelqu\'un</div>';}
function openProfile(){buildProfile();var s=$('#profileScreen');if(s){s.classList.add('show');s.scrollTop=0;}}
function armAllReminders(){try{promises.forEach(function(p){if(p.remind&&p.status==='encours'){try{_armReminder(p);}catch(e){}}});}catch(e){}}
function enableNotifs(){try{if(typeof Notification==='undefined')return;var tog=$('#notifTog');function on(){notifOn=true;if(tog)tog.classList.remove('off');armAllReminders();/* v109 (Tom) : plus de « Rappels activés ✓ » */if(typeof queueSave==='function')queueSave();}if(Notification.permission==='granted'){on();}else if(Notification.permission!=='denied'){Notification.requestPermission().then(function(pm){if(pm==='granted')on();else if(tog)tog.classList.add('off');});}else{if(tog)tog.classList.add('off');}}catch(e){}}
function openDetail(id){const p=promises.find(x=>x.id===id);if(!p)return;cur=p;renderDetail();closeAll();$('#detailPoster').classList.add('show');scrim.classList.add('show');try{requestAnimationFrame(function(){if(window.dpRefresh)window.dpRefresh();});}catch(e){}}
function renderDetail(){
  try{ if(window._fichePose) _fichePose(); }catch(_){}
  try{ if(window._tenirInit){ _tenirInit();
    /* (le placement est fait par la table d'ordre ci-dessus) */
    if(window._tenirPeindre) requestAnimationFrame(_tenirPeindre); } }catch(_){}
  /* on retient l'id pour le bouton d'acceptation, et on adapte la fiche
     si c'est une demande (§chantier 15). */
  try{window.__dpId=arguments[0];}catch(_){}
  try{setTimeout(function(){if(window._majFicheDemande)_majFicheDemande(window.__dpId);},40);}catch(_){}
const p=cur;if(!p)return;const r=$('#mgRename');if(r)r.style.display='none';const c=HX(MOODS[state.mood][p.id%MOODS[state.mood].length]);const fill=p.draft?'#999580':p.status==='rate'?'#BEB19D':p.status==='tenu'?RS(lighten(c,.1)):RS(c);
  const dg=$('#dForm');dg.innerHTML='';var GS=138;const gcv=document.createElement('canvas');const gd=Math.min(3,window.devicePixelRatio||1);gcv.width=GS*gd;gcv.height=GS*gd;gcv.style.width=GS+'px';gcv.style.height=GS+'px';dg.appendChild(gcv);const gg=gcv.getContext('2d');
  /* la vraie dalle du Promi, telle qu'elle apparait sur la Toile,
     dans le design actif du Studio */
  var _vraie=false;
  try{ if(window.Toile&&window.Toile.dalleTrame&&!p.draft){
    var _da=window.Toile.dalleAbs(p.id);
    if(_da&&_da.w){
      gg.setTransform(gd,0,0,gd,0,0);
      gg.clearRect(0,0,GS,GS);
      /* ⚑ v29 — la dalle rendue à la taille de la boîte, posée 1:1 (redteam_decoupe) */
      if(window._poseDalle&&window._poseDalle(gg,p.id,0,0,GS,GS)) _vraie=true;
    }
  } }catch(e){}
  if(gg&&!_vraie){gg.scale(gd,gd);var cxp=GS/2,cyp=GS/2,rp=GS*0.46;var poly=[[0.50,0.03],[0.86,0.20],[0.97,0.58],[0.74,0.98],[0.26,0.96],[0.05,0.60],[0.13,0.22]];gg.beginPath();poly.forEach(function(pt,ix){var x=pt[0]*GS,y=pt[1]*GS;ix?gg.lineTo(x,y):gg.moveTo(x,y);});gg.closePath();gg.fillStyle=fill;gg.shadowColor='rgba(0,0,0,.3)';gg.shadowBlur=14;gg.shadowOffsetY=6;gg.fill();gg.shadowBlur=0;gg.shadowOffsetY=0;if(p.status==='tenu'&&!p.draft){gg.fillStyle='rgba(255,255,255,.34)';gg.beginPath();gg.arc(cxp,cyp-8,GS*0.24,0,6.2832);gg.fill();}}/* teinte le fond de la page avec la couleur de la dalle */try{$('#detailPoster').style.setProperty('--dalle-c',fill);}catch(e){}
  {var _tt=$('#dTitleTxt'); if(_tt) _tt.textContent=p.title; else $('#dTitle').textContent=p.title;}
  {var _dp=$('#detailPoster');
   if(_dp){_dp.classList.remove('dp-promi','dp-chiche','dp-nuee','dp-draft','dp-innuee');
     if(p.draft){_dp.classList.add('dp-draft');}else if(p.chiche){_dp.classList.add('dp-chiche');}else if(p.nuee&&p.nuee!=='soi'){_dp.classList.add('dp-promi','dp-innuee');}else{_dp.classList.add('dp-promi');}try{var _ty=document.getElementById('dpType');if(_ty)_ty.textContent=p.draft?'Gardé':(p.chiche?'Chiche':'Promi');}catch(e){}}
   var _au=$('#dAura');
   if(_au){
     /* Les ENTITÉS concernées par CE Promi (l'harmonie globale est ajoutée en tête par
        auraDisques). Un Promi à soi → aucune ; une Nuée → un seul disque, la Nuée ;
        un Chiche → le défié PUIS le compagnon, jamais fusionnés ; sinon la personne. */
     var noms=[];
     if(!p.draft){
       /* ⚑ PLUSIEURS PERSONNES DANS UN CHAMP (« Rachel, Nico », lot-GENS) : un disque par personne, jamais un disque
          au nom composé. */
       var _un=function(v){ return String(v||'').split(/\s*[,·]\s*/).map(function(x){return x.trim();})
                              .filter(function(x){ return x && x!=='moi' && x!=='le groupe'; }); };
       if(p.chiche){
         _un(p.who).forEach(function(x){ if(noms.indexOf(x)<0) noms.push(x); });   /* le défié */
         _un(p.avec).forEach(function(x){ if(noms.indexOf(x)<0) noms.push(x); });  /* le compagnon */
       } else if(p.nuee && p.nuee!=='soi'){
         noms.push({nuee:p.nuee});                                                  /* un seul disque : la Nuée */
       } else {
         var _pers=[];
         _un(p.who).forEach(function(x){ if(_pers.indexOf(x)<0) _pers.push(x); });
         _un(p.from).forEach(function(x){ if(_pers.indexOf(x)<0) _pers.push(x); });
         _pers.sort(function(a,b){return (''+a).localeCompare(''+b);});             /* alpha, JAMAIS par valeur */
         noms=_pers;
       }
     }
     /* un brouillon n'est pas engagé : pas de disques. Sinon l'harmonie globale est
        toujours là (même à soi), suivie des entités concernées. */
     var _h=p.draft?'':auraDisques(noms,52);
     _au.innerHTML=_h; _au.style.display=_h?'':'none';
     if(_h) peintDisques(_au);
   }
   var _ni=$('#dNueeInfo');
   if(_ni){
     if(!p.draft&&p.nuee&&p.nuee!=='soi'){
       var _nom=(typeof NUE!=='undefined'&&NUE[p.nuee])||p.nuee;
       var _mem=0; try{_mem=(NUEM&&NUEM[p.nuee]?NUEM[p.nuee].length:0);}catch(e){}
       var _nb=promises.filter(function(x){return !x.draft&&x.nuee===p.nuee;}).length;
       _ni.textContent=_nom+' \u00b7 '+_nb+' Promi'+(_nb>1?'s':'')+(_mem?(' \u00b7 '+_mem+' membre'+(_mem>1?'s':'')):'')
         +' \u00b7 visible par le Cercle';
       _ni.style.display='';
     } else { _ni.style.display='none'; }
   }}
  $('#dMeta').textContent=`${p.who||'—'} · ${p.nuee?(NUE[p.nuee]||p.nuee):'libre'}${p.draft?' · brouillon':''}`;
  $$('#segRecur button').forEach(b=>b.classList.toggle('on',(p.recur||'none')===b.dataset.r));
  {const _dr=$('#dRemind');if(_dr)_dr.textContent=p.remind?('à '+p.remind):'aucun';const _rt=$('#remindTime');if(_rt&&p.remind)_rt.value=p.remind;}
  {var _dueTxt;
   /* ⚑ v16 (Tom) : « AVANT » dit une DATE, quel que soit l'état — « résolue » n'était pas une échéance */
   if(p.enLair){_dueTxt='en l’air';}          /* une envie : pas d'échéance */
   else if(p.dueISO){/* une date précise : « avant mardi 12 » / « avant mardi 12 mai » (format §4) */
     try{var _pk=new Date(p.dueISO+'T00:00:00');_dueTxt='avant '+(window._dateQuand?window._dateQuand(_pk):_pk.getDate());}catch(_dz){_dueTxt=(p.due<=1?'demain':'dans '+p.due+' jours');}}
   /* due null SANS enLair = « un jour » (promesse sans date, Décision Tom) : la fiche dit
      le MÊME mot que le sélecteur — aucun écart entre ce qu'on choisit et ce qu'on relit. */
   else if(p.due==null){_dueTxt='un jour';}
   else{try{var _dd=new Date();_dd.setHours(0,0,0,0);_dd.setDate(_dd.getDate()+Math.round(+p.due));_dueTxt='avant '+window._dateQuand(_dd);}catch(_de){_dueTxt='un jour';}}
   $('#dDue').textContent=_dueTxt;}
  $$('#segStatus button').forEach(b=>b.classList.toggle('on',b.dataset.st===p.status));var _wi=$('#dWhoInput');if(_wi)_wi.value=p.who||'';var _dn=$('#dNote');if(_dn)_dn.value=p.note||'';var _rb=$('#actRelance');if(_rb){var _tg=(p.from&&p.from!=='moi')?p.from:((p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:null);if(_tg&&p.status==='encours'){_rb.style.display='';_rb.textContent='Relancer '+_tg+(p.relances?' · relancé ×'+p.relances:'');}else{_rb.style.display='none';}}var _dc=$('#dComments');if(_dc){var _cm=p.comments||[];_dc.innerHTML=_cm.length?_cm.map(function(c){var _by=c.by||'moi';var _me=(_by==='moi'||(typeof USER!=='undefined'&&USER.name&&_by===USER.name));return '<div class="mg-cm'+(_me?' mine':'')+'"><div class="mg-cm-by">'+_esc(_me?'Moi':_by)+'</div><div class="mg-cm-t">'+_esc(c.t)+'</div><div class="mg-cm-d">'+_esc(_cdate(c.d))+'</div></div>';}).join(''):'<div class="mg-cm-empty">rien pour l\'instant</div>';var _dnc=$('#dNueeChips');if(_dnc&&typeof NUE!=='undefined'){var _hk='<div class="chip'+(p.nuee?'':' on')+'" data-dnuee="">Aucune</div>';Object.keys(NUE).forEach(function(k){_hk+='<div class="chip'+(p.nuee===k?' on':'')+'" data-dnuee="'+k+'">'+_esc(NUE[k]||k)+'</div>';});_dnc.innerHTML=_hk;$$('#dNueeChips .chip').forEach(function(c){c.onclick=function(){p.nuee=c.dataset.dnuee||undefined;$$('#dNueeChips .chip').forEach(function(x){x.classList.toggle('on',x===c);});try{if(window.syncAll)window.syncAll();if(typeof queueSave==='function')queueSave();}catch(e){}renderDetail();};});}var _cf=$('#dConfirm');if(_cf){var _cw=(p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:null;var _cfrom=(p.from&&p.from!=='moi')?p.from:null;if(_cfrom){_cf.textContent='c\u2019est toi qui confirmes \u2014 '+_cfrom+' te l\u2019a promis';}else if(_cw){_cf.textContent=(p.status==='encours')?('quand ce sera fait, '+_cw+' pourra le confirmer'):('d\u00e9clar\u00e9 par toi \u00b7 '+_cw+' peut confirmer');}else{_cf.textContent='promesse \u00e0 toi-m\u00eame \u2014 tu es seul juge';}}var _vz=$('#dFilVis');if(_vz){var _w=(p.nuee&&p.nuee!=='soi')?('les membres de '+((typeof NUE!=='undefined'&&NUE[p.nuee])||p.nuee)):((p.from&&p.from!=='moi')?p.from:((p.who&&p.who!=='moi'&&p.who!=='le groupe')?p.who:null));_vz.textContent=_w?('visible par '+_w+' · vous pouvez répondre'):'privé — personne d\'autre ne le voit';}}
  $$('#segImp button').forEach(b=>b.classList.toggle('on',+b.dataset.v===p.intensity));
  $$('#segUrg button').forEach(b=>b.classList.toggle('on',+b.dataset.v===(p.urg||1)));
  $('#actDraft').classList.toggle('act',!!p.draft);$('#actDraft').textContent=p.draft?'Réactiver':'Brouillon';
  /* LA MISE EN PAGE, EN DERNIER : « cur » est alors a jour quel que soit
     le chemin — Toile, Index ou Fil. Une seule fiche pour les trois. */
  try{ if(window._fichePose) _fichePose(); }catch(_){}
  try{ if(window._tenirInit){ _tenirInit();
    if(window._tenirPeindre) requestAnimationFrame(_tenirPeindre); } }catch(_){}
}
$$('#segStatus button').forEach(b=>b.onclick=()=>{if(!cur)return;cur.status=b.dataset.st;cur.draft=false;var _rg=(b.dataset.st==='tenu'&&cur.recur)?regenRecur(cur):false;if(typeof feedAdd==='function'){if(b.dataset.st==='tenu')feedAdd('kept','Tu as tenu « '+cur.title+' »',{pid:cur.id});else if(b.dataset.st==='rate')feedAdd('missed','« '+cur.title+' » est à tenir',{pid:cur.id});}renderDetail();if(_rg){relayout();}else{render();}caption();try{if(window.syncAll)window.syncAll();}catch(e){}});
$$('#segRecur button').forEach(b=>b.onclick=()=>{if(!cur)return;cur.recur=b.dataset.r==='none'?null:b.dataset.r;if(cur.recur&&cur.remind)scheduleReminder(cur);renderDetail();render();});
$$('#remindRow button').forEach(b=>b.onclick=()=>{if(!cur)return;if(b.dataset.rem==='on'){cur.remind=($('#remindTime')&&$('#remindTime').value)||'07:00';scheduleReminder(cur);}else{cur.remind=null;}renderDetail();render();});
function scheduleReminder(p){try{if(typeof Notification==='undefined')return;if(Notification.permission==='granted')_armReminder(p);else if(Notification.permission!=='denied')Notification.requestPermission().then(pm=>{if(pm==='granted')_armReminder(p);});}catch(e){}}
function _armReminder(p){try{if(!p.remind)return;const _p=p.remind.split(':');const t=new Date();t.setHours(+_p[0],+_p[1],0,0);const now=new Date();if(t<=now)t.setDate(t.getDate()+1);const ms=t-now;if(ms>0&&ms<25*3600*1000)setTimeout(()=>{try{new Notification('Promi — '+(p.who||'toi'),{body:p.title});}catch(e){}if(p.recur)_armReminder(p);},ms);}catch(e){}}
/* la Toile demande à l'app QUOI écrire sur chaque dalle, et SI le mode est actif.
   (le moteur est chargé dans un autre bloc : on attend qu'il soit là) */
(function _hookToile(){
  if(!window.Toile){setTimeout(_hookToile,60);return;}
  window.Toile.labelsOn=function(){
    /* pendant l'onboarding, la Toile est un décor : pas de texte sur les dalles,
       même si le Studio est réglé « avec texte » */
    var ov=document.getElementById('promiOnb');
    if(ov&&!ov.classList.contains('gone'))return false;
    return !!state.labels;
  };
  window.Toile.labelOf=function(seed){
    if(!seed)return null;
    if(seed.kind==='nuee'&&seed.nuee)return {who:null, title:(NUE[seed.nuee]||seed.nuee)};
    if(seed.pid==null)return null;
    var p=promises.find(function(x){return x.id===seed.pid;});
    if(!p||p.draft)return null;
    return {who:(p.who&&p.who!=='moi')?p.who:null, title:p.title};
  };
  if(window.Toile.redraw)window.Toile.redraw();
})();
$$('#txToggle button').forEach(b=>b.onclick=()=>{state.labels=(b.dataset.tx==='on');$$('#txToggle button').forEach(x=>x.classList.toggle('on',x===b));render();try{if(window.Toile&&window.Toile.redraw)window.Toile.redraw();}catch(e){}try{queueSave();}catch(e){}});
$$('#mgDueChips button').forEach(b=>b.onclick=()=>{if(!cur)return;const d=+b.dataset.d;cur.due=d===-99?0:Math.max(0,(cur.due||0)+d);cur.status='encours';renderDetail();render();});
$$('#segImp button').forEach(b=>b.onclick=()=>{if(!cur)return;cur.intensity=+b.dataset.v;renderDetail();render();});
$$('#segUrg button').forEach(b=>b.onclick=()=>{if(!cur)return;cur.urg=+b.dataset.v;renderDetail();});
function _ouvreRenommage(){if(!cur)return;const r=$('#mgRename');if(!r)return;r.style.display='flex';
  $('#dRenameInput').value=cur.title;$('#dRenameInput').focus();}
if($('#actRename'))$('#actRename').onclick=_ouvreRenommage;
if($('#dTitle'))$('#dTitle').onclick=_ouvreRenommage;
if($('#actPlanter'))$('#actPlanter').onclick=function(){
  if(!cur)return; cur.draft=false;
  try{ if(window.Toile&&window.Toile.addPromi) window.Toile.addPromi(cur.id); }catch(e){}
  try{ if(typeof queueSave==='function') queueSave(); }catch(e){}
  try{ renderDetail(); }catch(e){}
  try{ if(typeof render==='function') render(); }catch(e){}
  try{ if(typeof buildIndex==='function') buildIndex(); }catch(e){} try{ if(typeof buildFeed==='function') buildFeed(); }catch(e){}
  try{ if(window.dpRefresh) window.dpRefresh(); }catch(e){}
  try{ if(typeof toast==='function') toast('Promi plant\u00e9 sur la Toile'); }catch(e){}
};
$('#dRenameOk').onclick=()=>{if(!cur)return;const v=$('#dRenameInput').value.trim();if(v){cur.title=v;renderDetail();render();}$('#mgRename').style.display='none';};
$('#dRenameInput')&&$('#dRenameInput').addEventListener('keydown',e=>{if(e.key==='Enter')$('#dRenameOk').onclick();});
$('#actDraft').onclick=()=>{if(!cur)return;cur.draft=!cur.draft;renderDetail();render();caption();};
let _delArm=false;$('#actDel').onclick=()=>{if(!cur)return;var b=$('#actDel');if(!_delArm){_delArm=true;b.dataset.o=b.textContent;b.textContent='Confirmer ?';b.style.color='var(--rate)';setTimeout(function(){_delArm=false;if(b){b.textContent=b.dataset.o||'Supprimer';b.style.color='';}},2600);return;}promises=promises.filter(p=>p.id!==cur.id);_delArm=false;b.textContent=b.dataset.o||'Supprimer';b.style.color='';closeAll();relayout();caption();if(window.syncAll)window.syncAll();};

const STLAB={tenu:'tenue',encours:'en cours',rate:'à tenir'};const STCOL={tenu:'#C9A8F5',encours:'#82AEF8',rate:'#DD4D23'};
/* ===== Karma <- palette du Studio : TOUJOURS 3 couleurs distinctes de la palette ===== */
function _hx2(c){function h(v){v=Math.round(v);v=v<0?0:(v>255?255:v);return ('0'+v.toString(16)).slice(-2);}return '#'+h(c[0])+h(c[1])+h(c[2]);}
function _kd2(c){var r=c[0]/255,g2=c[1]/255,b2=c[2]/255,mx=Math.max(r,g2,b2),mn=Math.min(r,g2,b2),h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);h=mx===r?((g2-b2)/d+(g2<b2?6:0)):mx===g2?((b2-r)/d+2):((r-g2)/d+4);h/=6;}s=Math.min(s,0.62);l=Math.max(0.2,l-0.22);function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;return _hx2([f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255]);}
function _kdist(a,b){var dr=a[0]-b[0],dg=a[1]-b[1],db=a[2]-b[2];return dr*dr+dg*dg+db*db;}
var KC={M:[201,168,245],C:[130,174,248],O:[221,77,35],Mh:'#C9A8F5',Ch:'#82AEF8',Oh:'#DD4D23',Ml:'#8F62D1'};
var _kcSig='';
function auraSync(){var pal=null;try{pal=window.Toile&&window.Toile.cols?window.Toile.cols():null;}catch(e){}
  var sig=pal?pal.join('|'):'';if(sig===_kcSig)return;_kcSig=sig;   /* appelée dans des boucles d'animation : on ne recalcule que si la palette a bougé */
  if(!pal||pal.length<3)pal=[[201,168,245],[130,174,248],[221,77,35],[41,21,71]];
  var best=null,bs=-1;
  for(var i=0;i<pal.length;i++)for(var j=i+1;j<pal.length;j++)for(var k=j+1;k<pal.length;k++){
    var sc=Math.min(_kdist(pal[i],pal[j]),_kdist(pal[j],pal[k]),_kdist(pal[i],pal[k]));
    if(sc>bs){bs=sc;best=[pal[i],pal[j],pal[k]];}}
  if(!best)best=[pal[0],pal[1],pal[2]];
  /* LES 3 TEINTES DE L'APP — jamais la palette du Studio */KC.M=[201,168,245];KC.C=[130,174,248];KC.O=[221,77,35];
  KC.Mh=_hx2(KC.M);KC.Ch=_hx2(KC.C);KC.Oh=_hx2(KC.O);KC.Ml=_kd2(KC.M);
  /* STCOL reste fixe = les 3 couleurs de la légende */}
/* ══ TON VISAGE NE CHANGE PLUS À CHAQUE OUVERTURE ═══════════════════════════════════
   Tom, 21 septembre 2026 : « USER.seed tiré au hasard à chaque chargement — mon avatar
   change de couleurs à chaque ouverture. Fige-le, comme les dalles l'ont été le 13. »
   C'est exactement le défaut de `cc()` : `(Math.random()*1e9)|0`, jamais sauvegardé.
   LA MÊME PARADE QUE LE 13 SEPTEMBRE, dans le même ordre :
     1 · la graine SAUVEGARDÉE, si elle existe — c'est la couleur qu'on t'a déjà vue ;
     2 · sinon on la DÉRIVE d'une clé stable (le nom), jamais d'un id ni d'une horloge ;
     3 · et on l'enregistre, pour qu'un changement de nom ne change pas un visage connu.
   ⚠ La fonction est posée sur `window`, pas dans une IIFE : `USER` est déclaré ailleurs,
   et le §8 a déjà payé deux fois l'aide enfermée dans un bloc (l'Index sortait vide). */
/* ⚠ UNE DÉCLARATION DE FONCTION, PAS UNE AFFECTATION : `USER` est construit 960 lignes
   PLUS HAUT dans le même bloc. Seule une déclaration est hissée ; un `window.x = function`
   ne l'est pas, et la graine sortait en TypeError avant même d'être lue. */
function _grainePropre(nom){
  try{ var v=localStorage.getItem('promi_graine'); if(v!=null && v!=='') return (+v)|0; }catch(e){}
  var s=''+(nom||(typeof USER!=='undefined'&&USER&&USER.name)||'moi');
  var h=2166136261; for(var i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619); }
  h=(h>>>0)%1000000000;
  try{ localStorage.setItem('promi_graine', h); }catch(e){}
  return h;
}
window._grainePropre=_grainePropre;
window.onPaletteChange=function(){auraSync();
  try{if(typeof render==='function')render();}catch(e){}
  try{var sc=document.getElementById('auraScreen');if(sc&&sc.classList.contains('show')){buildAura();document.querySelectorAll('#auraScreen .kr-c').forEach(function(cv){try{drawKRing(cv);}catch(e){}});try{drawSpks();}catch(e){}try{drawKarmaGraph();}catch(e){}}}catch(e){}
  try{if(_sealCanvas)renderSeal();}catch(e){}};
function smoothOpen(P){if(P.length<2)return'';let d=`M${P[0][0].toFixed(1)} ${P[0][1].toFixed(1)}`;for(let i=0;i<P.length-1;i++){const p0=P[i-1]||P[i],p1=P[i],p2=P[i+1],p3=P[i+2]||p2;const c1=[p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6],c2=[p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6];d+=`C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;}return d;}
function roundRectP(g,x,y,w,h,r){r=Math.min(r,w/2,h/2);g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
function smoothCtx(g,pts){g.moveTo(pts[0][0],pts[0][1]);for(let i=0;i<pts.length-1;i++){const p0=pts[i-1]||pts[i],p1=pts[i],p2=pts[i+1],p3=pts[i+2]||p2;const c1=[p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6],c2=[p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6];g.bezierCurveTo(c1[0],c1[1],c2[0],c2[1],p2[0],p2[1]);}}
function kCanvas(W,H){const cx=$('#kchart');cx.innerHTML='';const dpr=Math.min(3,window.devicePixelRatio||1);const cv=document.createElement('canvas');cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);cv.style.width='100%';cv.style.height=H+'px';cv.style.display='block';cx.appendChild(cv);const g=cv.getContext('2d');if(g)g.setTransform(dpr*(W/W),0,0,dpr,0,0),g.scale(1,1);return g&&{g,W,H,dpr};}
function inkColor(){try{return getComputedStyle($('#auraScreen')).color||'#EFE3C7';}catch(e){return '#EFE3C7';}}
function isLight(){return $('#device').classList.contains('light');}
function drawCurve(g,W,H,vals){g.clearRect(0,0,W,H);var rgb=[201,168,245];var n=vals.length,mn=Math.min.apply(0,vals),mx=Math.max.apply(0,vals);function X(i){return 8+i/(n-1)*(W-16);}function Y(v){return H-16-((v-mn)/((mx-mn)||1))*(H-42);}function pth(){g.beginPath();g.moveTo(X(0),Y(vals[0]));for(var i=1;i<n;i++){var xc=(X(i-1)+X(i))/2;g.quadraticCurveTo(X(i-1),Y(vals[i-1]),xc,(Y(vals[i-1])+Y(vals[i]))/2);}g.lineTo(X(n-1),Y(vals[n-1]));}g.save();pth();g.lineTo(X(n-1),H);g.lineTo(X(0),H);g.closePath();g.clip();var ag=g.createLinearGradient(0,0,0,H);ag.addColorStop(0,'rgba('+rgb.join(',')+',.40)');ag.addColorStop(0.72,'rgba('+rgb.join(',')+',.08)');ag.addColorStop(1,'rgba('+rgb.join(',')+',0)');g.fillStyle=ag;g.fillRect(0,0,W,H);_grain(g,W,H,0.55);g.restore();pth();g.strokeStyle='rgb('+rgb.join(',')+')';g.lineWidth=3.2;g.lineJoin='round';g.lineCap='round';g.stroke();var ex=X(n-1),ey=Y(vals[n-1]);g.beginPath();g.arc(ex,ey,6,0,6.28);g.fillStyle='rgb('+rgb.join(',')+')';g.fill();g.beginPath();g.arc(ex,ey,2.6,0,6.28);g.fillStyle='#201908';g.fill();}
function fingerprint(g,ex,ey,rx,ry,harms,col,base,light,rot){
  // œil = origine polaire ; contour = œil + direction*rayon(θ)*t → cœur dense en spirale, galet lumpy dehors
  const steps=240,A=new Array(steps+1);
  for(let i=0;i<=steps;i++){const ang=i/steps*6.2831853;let v=1;for(let h=0;h<harms.length;h++)v+=harms[h][1]*Math.sin(harms[h][0]*ang+harms[h][2]);A[i]=v;}
  const rings=120,rt=rot||0;
  for(let r=1;r<=rings;r++){
    const t=r/rings,a=base*(0.32+0.55*(1-t))*(light?1:0.9);
    g.beginPath();
    for(let i=0;i<=steps;i++){const ang=i/steps*6.2831853,ca=Math.cos(ang+rt),sa=Math.sin(ang+rt),R=A[i]*t;const x=ex+ca*rx*R,y=ey+sa*ry*R;i?g.lineTo(x,y):g.moveTo(x,y);}
    g.closePath();g.strokeStyle=`rgba(${col[0]},${col[1]},${col[2]},${a})`;g.lineWidth=0.7;g.stroke();
  }
}
const COMPO_SHAPES2={green:{c1:[-146,83,-142,82,-137,81,-132,80,-128,79,-124,77,-122,73,-120,69,-119,65,-118,60,-117,55,-116,51,-115,46,-113,41,-112,37,-112,32,-111,27,-111,22,-110,18,-109,13,-107,9,-104,6,-101,4,-97,2,-92,2,-87,1,-82,1,-78,1,-73,1,-68,1,-63,1,-58,1,-54,1,-49,1,-44,0,-40,-1,-36,-3,-32,-6,-28,-9,-25,-12,-21,-14,-17,-16,-12,-19,-8,-21,-4,-24,0,-26,4,-28,8,-31,11,-34,14,-38,16,-42,17,-46,17,-51,17,-56,17,-61,17,-65,17,-70,17,-75,17,-80,15,-84,13,-88,10,-91,6,-93,2,-94,-2,-96,-6,-98,-10,-100,-12,-104,-13,-108,-14,-113,-14,-117,-15,-122,-15,-127,-15,-132,-14,-137,-14,-141,-13,-146,-12,-150,-9,-153,-5,-155,-1,-155,3,-154,7,-152,11,-150,15,-147,19,-144,23,-141,27,-139,31,-136,35,-133,39,-130,42,-128,46,-125,50,-122,54,-119,58,-117,62,-114,66,-112,71,-109,75,-107,79,-104,83,-102,87,-99,91,-97,95,-94,99,-92],c2:[-132,112,-129,112,-125,112,-122,112,-119,112,-115,111,-112,111,-109,110,-105,110,-102,109,-99,109,-96,108,-92,108,-89,107,-86,106,-83,105,-79,104,-76,103,-73,103,-70,102,-66,101,-63,100,-60,98,-57,97,-54,96,-51,94,-48,93,-45,91,-42,90,-39,88,-36,86,-33,85,-30,83,-28,81,-25,79,-22,77,-20,75,-17,74,-14,72,-11,70,-8,68,-5,67,-2,65,1,63,3,62,6,60,9,58,12,56,15,55,18,53,21,51,23,49,26,48,29,46,32,45,35,44,39,42,42,42,45,41,48,40,52,40,55,40,58,40,62,39,65,39,68,39,72,39,75,39,78,40,82,40,85,40,88,40,92,40,95,40,98,39,101,38,104,36,106,34,108,32,110,29,112,26,114,23,115,20,117,17,119,14,120,11,121,8,123,5,123,2,124,-1,125,-4,125,-8,125,-11,125,-14,125,-18,125,-21,125,-25,125,-28,125,-31,125,-35,125,-38,125,-41,126,-45,126,-48,126,-51,127,-55],r:102.7,thick:113.3},orange:{c1:[-206,177,-202,172,-198,167,-194,163,-189,158,-185,154,-180,149,-176,144,-172,139,-167,135,-163,129,-160,124,-156,119,-153,114,-150,108,-147,102,-144,96,-142,90,-141,84,-140,78,-139,72,-139,65,-139,59,-140,52,-140,46,-140,40,-141,33,-141,27,-141,21,-142,15,-144,9,-148,4,-152,0,-157,-4,-163,-8,-168,-11,-172,-16,-176,-20,-179,-26,-181,-32,-183,-38,-184,-44,-186,-50,-187,-57,-187,-63,-188,-69,-188,-76,-187,-82,-187,-88,-186,-95,-184,-101,-183,-107,-180,-113,-178,-119,-175,-124,-171,-130,-167,-135,-164,-140,-159,-145,-155,-149,-150,-154,-145,-158,-140,-162,-135,-165,-129,-168,-124,-172,-118,-175,-112,-177,-106,-180,-101,-183,-95,-185,-89,-188,-83,-191,-77,-193,-71,-196,-65,-198,-59,-201,-53,-203,-48,-206,-42,-209,-36,-211,-30,-214,-24,-217,-19,-220,-13,-223,-7,-225,-1,-228,4,-231,10,-234,16,-237,22,-239,28,-242,34,-244,40,-247,46,-249,52,-250,58,-252,64,-252,71,-253,77,-253,84,-253,90,-253,96,-253,103,-253,109,-253,116,-253],c2:[-163,219,-155,218,-147,217,-140,216,-133,213,-126,211,-118,208,-111,205,-104,203,-97,200,-90,197,-82,195,-75,193,-68,191,-60,190,-52,190,-45,189,-37,189,-30,189,-22,190,-14,190,-7,192,1,193,8,195,16,197,23,199,30,201,38,203,45,205,52,208,60,210,67,212,74,214,82,216,89,217,97,218,104,219,112,219,120,219,127,218,135,217,142,215,148,212,154,208,159,202,164,196,167,190,171,184,175,177,180,171,184,165,188,159,190,153,191,146,190,138,188,131,185,124,182,117,178,111,174,104,170,97,166,91,162,85,158,78,153,72,149,65,146,59,143,52,141,44,140,37,140,29,141,22,142,14,143,7,146,0,149,-7,152,-14,156,-21,160,-27,165,-33,169,-40,173,-46,177,-52,182,-59,186,-65,190,-72,194,-78,197,-85,200,-92,202,-99,203,-107,204,-114,206,-122,208,-129,211,-136,213,-143,215,-150,216,-157,216,-165,216,-172,214,-179,211,-185,206,-191,202,-197,197,-203,193,-209],r:208.8,thick:266.5},purple:{c1:[141,31,141,27,141,24,141,20,141,16,141,12,140,9,139,5,137,2,135,-1,133,-4,130,-6,128,-9,127,-12,126,-16,125,-20,125,-23,125,-27,125,-31,124,-34,124,-38,123,-42,121,-45,120,-49,118,-52,117,-55,115,-59,113,-62,111,-65,109,-68,107,-71,105,-74,102,-77,100,-80,98,-83,95,-86,94,-89,92,-92,90,-95,88,-99,86,-102,84,-105,81,-107,78,-110,75,-112,72,-113,68,-114,65,-115,61,-115,57,-115,54,-115,50,-115,46,-115,42,-115,39,-115,35,-115,31,-115,27,-115,24,-115,20,-115,16,-115,12,-116,9,-116,5,-117,2,-118,-2,-120,-5,-121,-9,-123,-12,-124,-16,-125,-19,-125,-23,-125,-27,-125,-31,-125,-34,-125,-38,-125,-42,-125,-45,-125,-49,-125,-53,-125,-57,-125,-60,-124,-64,-124,-68,-124,-72,-124,-75,-123,-79,-123,-83,-123,-87,-123,-90,-122,-94,-121,-97,-120,-100,-118,-103,-116,-106,-114,-109,-111,-111,-108,-113,-105,-115,-102,-117,-99,-119,-96,-121,-92,-122,-89,-124,-86,-126,-82,-128,-80],c2:[124,70,121,73,118,76,115,79,113,82,111,85,110,89,109,93,109,97,109,101,109,105,108,109,108,113,107,116,105,120,102,123,99,125,96,127,92,129,88,130,84,131,81,132,77,132,73,133,68,133,64,133,60,133,56,133,52,133,48,133,44,133,40,133,36,133,32,133,28,133,24,133,20,133,16,133,12,133,8,133,4,133,0,133,-4,133,-8,133,-12,132,-16,132,-20,131,-24,130,-28,129,-31,127,-34,124,-37,122,-40,119,-42,115,-44,112,-45,108,-47,104,-48,101,-51,98,-54,96,-57,94,-61,93,-65,93,-69,93,-73,92,-77,92,-81,91,-85,90,-89,89,-92,87,-96,85,-99,83,-102,81,-105,78,-107,75,-108,71,-110,67,-111,64,-113,60,-114,56,-116,53,-119,49,-120,46,-122,42,-124,39,-127,35,-129,32,-132,29,-134,26,-137,23,-139,20,-141,16,-144,13,-146,10,-148,6,-149,2,-151,-1,-153,-5,-155,-8,-156,-12,-157,-16,-157,-20,-157,-24,-157,-28,-156,-32,-155,-36],r:134.2,thick:179.3}};
function drawComposition(g,W,H,d){
  g.clearRect(0,0,W,H);const light=isLight();
  auraSync();const SH=COMPO_SHAPES2,base=W*0.31,SP=3,refN=3;
  const cats=[['green',KC.M,d.tenu],['purple',KC.O,d.rate],['orange',KC.C,d.enc]];
  const POS={green:[W*0.16,H*0.44],purple:[W*0.86,H*0.46],orange:[W*0.51,H*0.40]};
  g.lineWidth=0.7;g.lineJoin='round';g.lineCap='round';g.save();g.globalCompositeOperation=light?'multiply':'screen';
  for(let ci=0;ci<cats.length;ci++){
    const k=cats[ci][0],col=cats[ci][1],n=cats[ci][2];if(n<=0)continue;
    const sh=SH[k],c1=sh.c1,c2=sh.c2,K=c1.length/2,cx=POS[k][0],cy=POS[k][1];
    const s=base*Math.sqrt(Math.max(n,0.4)/refN)/sh.r,M=Math.max(4,Math.round(sh.thick*s/SP));
    g.strokeStyle=`rgba(${col[0]},${col[1]},${col[2]},0.6)`;
    const curve=(t)=>{g.beginPath();for(let j=0;j<K;j++){const x=cx+(c1[j*2]*(1-t)+c2[j*2]*t)*s,y=cy+(c1[j*2+1]*(1-t)+c2[j*2+1]*t)*s;j?g.lineTo(x,y):g.moveTo(x,y);}g.stroke();};
    curve(0);for(let m=1;m<=M;m++)curve(m/(M+1));curve(1);
  }
  g.restore();
  g.textAlign='center';g.font='600 11px Atkinson,Atkinson,system-ui,sans-serif';g.globalAlpha=.92;
  g.fillStyle=KC.Mh;g.fillText('tenues',POS.green[0],H-9);
  g.fillStyle=KC.Ch;g.fillText('en cours',POS.orange[0],H-9);
  g.fillStyle=KC.Oh;g.fillText('à tenir',POS.purple[0],H-9);g.globalAlpha=1;
}
function kLabel(g,big,small,numCol,wordCol,x,y){
  g.textAlign='center';
  g.fillStyle=numCol;g.font='700 42px Gilbert,Gilbert,system-ui,sans-serif';g.fillText(String(big),x,y);
  g.fillStyle=wordCol;g.font='500 11px Atkinson,Atkinson,system-ui,sans-serif';g.fillText(small.toUpperCase(),x,y+20);
}
function drawRepartition(g,W,H,d){
  g.clearRect(0,0,W,H);const light=isLight();
  const ps=(d.persons||[]).filter(p=>(p.enc+p.tenu+p.rate)>0);
  const n=ps.length;if(n===0)return;
  auraSync();const UV=KC.C,MV=KC.M,OR=KC.O;
  const padTop=8,nameX=3,barX=Math.round(W*0.23),barRight=W,barW=barRight-barX;
  const barH=28,vgap=4,segGap=3,r=3;
  const rr=(x,y,w,h,rr2)=>{rr2=Math.min(rr2,h/2,w/2);g.beginPath();g.moveTo(x+rr2,y);g.arcTo(x+w,y,x+w,y+h,rr2);g.arcTo(x+w,y+h,x,y+h,rr2);g.arcTo(x,y+h,x,y,rr2);g.arcTo(x,y,x+w,y,rr2);g.closePath();};
  g.textBaseline='middle';g.lineJoin='round';
  ps.forEach((p,i)=>{
    const by=padTop+i*(barH+vgap),cy=by+barH/2,tot=p.enc+p.tenu+p.rate;
    g.fillStyle=light?'#201908':'#E4D7BB';g.font='700 13px Gilbert,Gilbert,system-ui,sans-serif';g.textAlign='left';
    let nm=(p.name||'').toUpperCase();if(nm.length>8)nm=nm.slice(0,7)+'\u2026';
    g.fillText(nm,nameX,cy+1);
    const parts=[[p.enc,UV],[p.tenu,MV],[p.rate,OR]].filter(pr=>pr[0]>0);
    const k=parts.length,usableW=barW-segGap*(k-1);let x=barX;
    parts.forEach((pr)=>{const w=usableW*(pr[0]/tot);g.fillStyle=`rgb(${pr[1][0]},${pr[1][1]},${pr[1][2]})`;rr(x,by,Math.max(2,w),barH,r);g.fill();x+=w+segGap;});
  });
}
function keptOf(items){const t=items.filter(p=>p.status==='tenu').length,r=items.filter(p=>p.status==='rate').length;const res=t+r;return res>0?Math.round(100*t/res):null;}
let karmaView='courbe',karmaData=null;
function drawKarmaGraph(){const d=karmaData;if(!d)return;const ax=$('#kxaxis'),lg=$('#kLegend'),ks=$('#kStats');if(karmaView==='courbe'){const c=kCanvas(320,215);if(c)drawCurve(c.g,c.W,c.H,d.vals);ax.style.display='flex';lg.style.display='none';ks.style.display='none';}else if(karmaView==='barres'){const c=kCanvas(320,215);if(c)drawComposition(c.g,c.W,c.H,d);ax.style.display='none';lg.style.display='none';ks.style.display='none';}else{const c=kCanvas(320,215);if(c)drawRepartition(c.g,c.W,c.H,d);ax.style.display='none';lg.style.display='none';ks.style.display='none';}}
$$('#kLens button').forEach(b=>b.onclick=()=>{karmaView=b.dataset.v;$$('#kLens button').forEach(x=>x.classList.toggle('on',x.dataset.v===karmaView));drawKarmaGraph();});
function statBars(items){const t=items.filter(p=>p.status==='tenu').length,e=items.filter(p=>p.status==='encours').length,r=items.filter(p=>p.status==='rate').length;return [[t,STCOL.tenu],[e,STCOL.encours],[r,STCOL.rate]].map(([v,c])=>v>0?`<i style="flex:${v} 1 0;background:${c}"></i>`:'').join('');}
function karmaRing(enc,tenu,rate,size,eux){size=size||72;var ex='';if(eux&&((+eux.theirE||0)+(+eux.theirT||0)+(+eux.theirR||0))>0){ex=' data-oe="'+(+eux.theirE||0)+'" data-ot="'+(+eux.theirT||0)+'" data-or="'+(+eux.theirR||0)+'"';}return '<canvas class="kr-c" width="'+(size*2)+'" height="'+(size*2)+'" style="width:'+size+'px;height:'+size+'px" data-e="'+enc+'" data-t="'+tenu+'" data-r="'+rate+'"'+ex+'></canvas>';}
function _grain(g,W,H,a){try{if(!_noiseCanvas)return;var p=g.createPattern(_noiseCanvas,'repeat');if(!p)return;try{if(p.setTransform&&window.DOMMatrix){var s=88/96;p.setTransform(new DOMMatrix([s,0,0,s,0,0]));}}catch(_){}var oc=g.globalCompositeOperation,oa=g.globalAlpha;g.globalCompositeOperation='soft-light';g.globalAlpha=(a==null?0.55:a);g.fillStyle=p;g.fillRect(-2,-2,W+4,H+4);g.globalAlpha=oa;g.globalCompositeOperation=oc;}catch(e){}}
function drawSpk(cv){var pts=(cv.dataset.pts||'').split(',').map(Number);if(pts.length<2)return;var col=cv.dataset.col||'#C9A8F5',rgb=[parseInt(col.slice(1,3),16),parseInt(col.slice(3,5),16),parseInt(col.slice(5,7),16)];var g=cv.getContext('2d');if(!g)return;var W=cv.width,H=cv.height,n=pts.length,mn=Math.min.apply(0,pts),mx=Math.max.apply(0,pts);function X(i){return 6+i/(n-1)*(W-12);}function Y(v){return H-7-((v-mn)/(mx-mn||1))*(H-14);}function pth(){g.beginPath();g.moveTo(X(0),Y(pts[0]));for(var i2=1;i2<n;i2++){var xc=(X(i2-1)+X(i2))/2;g.quadraticCurveTo(X(i2-1),Y(pts[i2-1]),xc,(Y(pts[i2-1])+Y(pts[i2]))/2);}g.lineTo(X(n-1),Y(pts[n-1]));}g.clearRect(0,0,W,H);g.save();pth();g.lineTo(X(n-1),H);g.lineTo(X(0),H);g.closePath();g.clip();var ag=g.createLinearGradient(0,0,0,H);ag.addColorStop(0,'rgba('+rgb.join(',')+',.30)');ag.addColorStop(1,'rgba('+rgb.join(',')+',0)');g.fillStyle=ag;g.fillRect(0,0,W,H);_grain(g,W,H,0.5);g.restore();pth();g.strokeStyle='rgb('+rgb.join(',')+')';g.lineWidth=3;g.lineJoin='round';g.lineCap='round';g.stroke();var ex=X(n-1),ey=Y(pts[n-1]);g.beginPath();g.arc(ex,ey,3.2,0,6.28);g.fillStyle='rgb('+rgb.join(',')+')';g.fill();}
function drawSpks(){document.querySelectorAll('#auraScreen .spk').forEach(function(cv){try{drawSpk(cv);}catch(e){}});}
/* les proportions du + suivent la Toile, comme l'anneau de l'Aura :
   memes compteurs, meme ordre tenu -> en cours -> a tenir,
   meme fondu de 3 % de tour de part et d'autre de chaque frontiere. */
window._majAnneauPlus=function(){try{
  var el=document.getElementById('createBtn'); if(!el)return;
  var t=0,e=0,r=0;
  try{promises.forEach(function(p){ if(p.draft||p.req)return;
    if(p.status==='tenu')t++; else if(p.status==='rate')r++; else e++; });}catch(_){}
  var tot=t+e+r; if(!tot){el.style.removeProperty('--kr-a1');return;}
  var bl=10.8;                       /* 3 % de tour, comme drawKRing */
  var a=360*t/tot, b=360*e/tot;
  var s=el.style;
  s.setProperty('--kr-a1', Math.max(0,a-bl).toFixed(1)+'deg');
  s.setProperty('--kr-a2', Math.min(360,a+bl).toFixed(1)+'deg');
  s.setProperty('--kr-b1', Math.max(0,a+b-bl).toFixed(1)+'deg');
  s.setProperty('--kr-b2', Math.min(360,a+b+bl).toFixed(1)+'deg');
  s.setProperty('--kr-c1', (360-bl).toFixed(1)+'deg');
  s.setProperty('--kr-c2', '360deg');
}catch(e){}};
try{document.addEventListener('DOMContentLoaded',function(){
  setTimeout(function(){if(window._majAnneauPlus)_majAnneauPlus();},900);});
  setTimeout(function(){if(window._majAnneauPlus)_majAnneauPlus();},2500);
}catch(e){}
/* les lettres d'HARMONIE prennent les trois teintes de la palette active,
   en rotation. Elles changent avec le Studio, comme un rappel. */
/* CHANTIERS 13 et 14 — le geste du Noyau.
   Appui long de 260 ms sur le Noyau, puis on le deplace.
   Ma Toile : deux aimants — le centre exact et la ligne du QR — qui ne
   se declenchent qu'au-dessus de 40 px/s, sinon on garde la main.
   Mes Promi : le bloc change de case, les Promi se rangent autour. */
/* la boucle qui adoucit la reorganisation : 340 ms, courbe des feuilles */
window._shAnim=function(){
 if(window._shAnimOn)return; window._shAnimOn=true;
 var pas=function(){
  var t=(performance.now()-(window.shNyT0||0))/420;
  if(t>=1){window._shAnimOn=false; window.shNyMix=1;
   if(window.shareRender)shareRender(); return;}
  /* cubic-bezier(.32,.72,0,1) approche : depart franc, arrivee tres amortie.
     420 ms plutot que 340 : la planche est lourde a recomposer, un peu
     plus long donne un mouvement plus lisible a nombre d'images egal. */
  window.shNyMix=1-Math.pow(1-t,3);
  if(window.shareRender)shareRender();
  requestAnimationFrame(pas);
 };
 requestAnimationFrame(pas);
};
(function(){
 var LONG=260, SEUIL=24, VIT=40;
 var t0=0, pris=false, tmr=null, lx=0, ly=0, lt=0, vx=0, vy=0;
 function zone(){return document.getElementById('shPreviewArea');}
 function cv(){return document.getElementById('shCanvas');}
 function local(e){var c=cv(); if(!c)return null;
  var r=c.getBoundingClientRect();
  return {x:(e.clientX-r.left)/r.width, y:(e.clientY-r.top)/r.height};}
 function surNoyau(p){
  if(!window.shNoyau||!p)return false;
  if(typeof shareMode!=='undefined'&&shareMode==='mosaic')return true;
  var nx=(window.shNyX===undefined?0.5:window.shNyX);
  var ny=(window.shNyY===undefined?0.5:window.shNyY);
  var c=cv(); if(!c)return false;
  var f={s:0.26,m:0.36,l:0.48}[window.shNySize||'m'];
  var ar=c.width/c.height; if(ar>0.75)f*=0.72; if(ar>1.2)f*=0.82;
  var R=f/2*1.25;                       /* generosite de prise */
  var dx=(p.x-nx)*ar, dy=(p.y-ny);
  return Math.sqrt(dx*dx+dy*dy)<R;}
 function aimante(y,vitesse){
  /* deux points : le centre exact, et la ligne du QR (bas de l'image) */
  var cibles=[0.5,0.84], c=cv(); if(!c)return y;
  var tol=SEUIL/c.getBoundingClientRect().height;
  for(var i=0;i<cibles.length;i++){
   if(Math.abs(y-cibles[i])<tol && vitesse>VIT) return cibles[i];
  }
  return y;}
 document.addEventListener('pointerdown',function(e){
  var z=zone(); if(!z||!z.contains(e.target))return;
  var p=local(e); if(!surNoyau(p))return;
  lx=e.clientX; ly=e.clientY; lt=performance.now();
  tmr=setTimeout(function(){pris=true;
   try{window._shGelCadrage=true;}catch(_){}
   try{if(navigator.vibrate)navigator.vibrate(8);}catch(_){}
   var s=document.getElementById('shareScreen'); if(s)s.classList.add('sh-ny-prise');
  },LONG);
 },true);
 document.addEventListener('pointermove',function(e){
  if(!pris)return;
  var now=performance.now(), dt=Math.max(1,now-lt);
  vx=(e.clientX-lx)/dt*1000; vy=(e.clientY-ly)/dt*1000;
  lx=e.clientX; ly=e.clientY; lt=now;
  var p=local(e); if(!p)return;
  var vit=Math.sqrt(vx*vx+vy*vy);
  if(typeof shareMode!=='undefined'&&shareMode==='mosaic'){
   /* le bloc change de case : on convertit la position en rangee/colonne */
   var n=0; try{n=promises.filter(function(q){return !q.draft&&!q.req;}).length;}catch(_){}
   var cols=n<=6?2:(n<=12?3:(n<=24?4:5));
   var rows=Math.max(1,Math.ceil((n+4)/cols));
   var R=Math.max(0,Math.min(rows-2,Math.round(p.y*rows-1)));
   var C=Math.max(0,Math.min(cols-2,Math.round(p.x*cols-0.5)));
   if(R!==window.shNyBR||C!==window.shNyBC){
    /* mouvement doux : on note l'ancienne case et l'instant du changement,
       sharePlanche interpole les positions sur 340 ms avec la courbe des
       feuilles. Sans ca les dalles sautaient d'une case a l'autre. */
    window.shNyBR0=(window.shNyBR===undefined?1:window.shNyBR);
    window.shNyBC0=(window.shNyBC===undefined?0:window.shNyBC);
    window.shNyBR=R; window.shNyBC=C;
    window.shNyT0=performance.now();
    if(window._shAnim)_shAnim();}
  }else{
   window.shNyX=Math.max(0.12,Math.min(0.88,p.x));
   window.shNyY=aimante(Math.max(0.10,Math.min(0.90,p.y)),vit);
   if(window.shareRender)shareRender();
  }
  e.preventDefault();
  e.stopPropagation();   /* le cadrage de l'apercu ne suit pas le Noyau */
 },true);
 function lache(){
  if(tmr){clearTimeout(tmr);tmr=null;}
  if(pris){pris=false;
   try{window._shGelCadrage=false;}catch(_){}
   var s=document.getElementById('shareScreen'); if(s)s.classList.remove('sh-ny-prise');
   if(window.shareRender)shareRender();}
 }
 document.addEventListener('pointerup',lache,true);
 document.addEventListener('pointercancel',lache,true);
 window.shNyReset=function(){window.shNyX=0.5;window.shNyY=0.5;
  window.shNyBR=1;window.shNyBC=0;
  if(window.shareRender)shareRender();};
})();
window._majHarmonieCols=function(){try{
  var el=document.getElementById('kuLab'); if(!el)return;
  var pal=null;
  try{ if(window.Toile&&Toile.cols) pal=Toile.cols(); }catch(_){}
  if(!pal||!pal.length) pal=[[201,168,245],[130,174,248],[221,77,35]];
  var trois=[pal[0],pal[1%pal.length],pal[2%pal.length]];
  var L=el.querySelectorAll('i');
  for(var i=0;i<L.length;i++){
    var c=trois[i%3];
    L[i].style.color=(typeof c==='string')?c:('rgb('+c[0]+','+c[1]+','+c[2]+')');
  }
}catch(e){}};
/* le Fil : ouverture depuis le dock, et pastille des qu'il y a du non-lu */
/* la rangee des Promi : un encart par Promi reel, l'etat vient de
   shareHidden (la meme source que la liste complete). */
/* CHANTIER 15 — le cycle d'une demande.
   attente -> acceptee (la dalle apparait) | expiree (silence, 1 mois).
   Il n'y a pas d'etat « refusee » : refuser, c'est ne rien faire. */
window.PROMI_EXPIRE=30*24*3600*1000;
window.demandeAccepter=function(id){try{
  var p=promises.find(function(x){return x.id===id;}); if(!p||!p.req)return false;
  if(p.reqEtat==='acceptee')return false;
  p.reqEtat='acceptee'; p.req=false; p.acceptLe=Date.now();
  /* la dalle apparait maintenant : c'est le moment de recompense */
  try{ if(window.Toile&&Toile.addPromi)Toile.addPromi(p.id); }catch(_){}
  try{ if(window.feedAdd)feedAdd('accept','« '+(p.title||'')+' » est promis',{pid:p.id,unread:true}); }catch(_){}
  try{ if(window.saveState)saveState(); }catch(_){}
  try{ if(window.buildIndex&&document.getElementById('indexSheet').classList.contains('show'))buildIndex(); }catch(_){}
  try{ if(window.updateFeedDot)updateFeedDot(); }catch(_){}
  return true;
}catch(e){return false;}};
/* un Promi dont l'echeance est passee bascule seul en « a tenir » :
   personne ne devrait avoir a le declarer manque a la main. */
window.echeancesDepassees=function(){try{
  var k=0;
  promises.forEach(function(p){
    if(p.draft||p.req)return;
    if(p.status!=='encours')return;
    var j=(p.due===undefined||p.due===null)?null:Number(p.due);
    if(j!==null && !isNaN(j) && j<0){ p.status='rate'; k++; }
  });
  if(k){ try{if(window.saveState)saveState();}catch(_){}
         try{if(window.syncAll)syncAll();}catch(_){} }
  return k;
}catch(e){return 0;}};
try{setTimeout(function(){if(window.echeancesDepassees)echeancesDepassees();},3400);}catch(e){}
try{setTimeout(function(){if(window._trameReglages)_trameReglages();},3600);}catch(e){}
window.demandesExpirer=function(){try{
  var n=Date.now(), k=0;
  promises.forEach(function(p){
    if(p.req&&p.reqEtat==='attente'&&p.reqLe&&(n-p.reqLe)>window.PROMI_EXPIRE){
      p.reqEtat='expiree'; k++;   /* aucune notification : le refus est un silence */
    }});
  if(k){try{if(window.saveState)saveState();}catch(_){}}
  return k;
}catch(e){return 0;}};
window.demandesEnAttente=function(){try{
  return promises.filter(function(p){return p.req&&p.reqEtat!=='expiree';});
}catch(e){return [];}};
/* une demande en attente allume la pastille du Fil : c'est la seule
   presence qu'elle a le droit d'avoir tant qu'elle n'est pas acceptee. */
/* la fiche d'une demande : sa vignette est dans la brume, et un seul geste
   la rend reelle. Aucun bouton « refuser » — refuser, c'est ne rien faire. */
window._majFicheDemande=function(pid){try{
  var p=promises.find(function(x){return x.id===pid;}); if(!p)return;
  var f=document.getElementById('dForm');
  var enAttente=!!(p.req&&p.reqEtat!=='expiree');
  if(f)f.classList.toggle('dem-brume',enAttente);
  var old=document.getElementById('dpfDem'); if(old)old.remove();
  if(!enAttente)return;
  var t=document.getElementById('dTitle')||f;
  if(!t||!t.parentElement)return;
  var box=document.createElement('div');
  box.className='dpf-dem'; box.id='dpfDem';
  box.innerHTML='<b>En attente de ta parole</b><button id="dpfDemOk">Je promets</button>';
  t.parentElement.insertBefore(box, t.nextSibling);
}catch(e){}};
document.addEventListener('click',function(e){
  if(!(e.target.closest&&e.target.closest('#dpfDemOk')))return;
  try{ var id=window.__dpId; if(id&&window.demandeAccepter&&demandeAccepter(id)){
    if(window._majFicheDemande)_majFicheDemande(id);
    if(window._majFilDot)_majFilDot();
  } }catch(_){}
},true);
window._demandeSignal=function(){try{
  var d=document.getElementById('filDot'); if(!d)return;
  d.classList.toggle('on',(window._filAttente?window._filAttente():0)>0);   /* v89 (Q347) */
}catch(e){}};
/* une demande ne compte dans aucune statistique : elle n'est pas une parole
   donnee. Elle n'a pas de dalle non plus — d'ou le filtre !p.req partout. */
window.promiComptes=function(){try{
  var t=0,e=0,r=0;
  promises.forEach(function(p){
    if(p.draft||p.req)return;
    if(p.status==='tenu')t++; else if(p.status==='rate')r++; else e++;});
  return {tenu:t,encours:e,rate:r,total:t+e+r};
}catch(err){return {tenu:0,encours:0,rate:0,total:0};}};
try{setTimeout(function(){if(window.demandesExpirer)demandesExpirer();},3200);}catch(e){}
/* Le mot du temps : jamais un decompte, jamais « retard ». Un Promi
   depasse est « a tenir » — le geste, pas la faute. */
/* le menu de tri : un bouton, deux groupes. Les categories (Nuee, brouillon,
   demande) sont des FILTRES, pas des sections de la page. */
window.ixFiltre='tous'; window.ixTri='recent';
document.addEventListener('click',function(e){
  var t=e.target;
  if(t.closest&&t.closest('#ixTriBtn')){
    var m=document.getElementById('ixMenu');
    if(m){m.classList.add('on');
      var b=document.getElementById('ixTriBtn'); if(b)b.classList.add('on');}
    e.stopPropagation(); return;}
  var it=t.closest&&t.closest('#ixMenu .ix-mi');
  if(it){
    var grp = it.dataset.tri ? '[data-tri]'
      : it.dataset.cols ? '[data-cols]' : '[data-filt]';
    document.querySelectorAll('#ixMenu .ix-mi'+grp).forEach(function(x){
      x.classList.toggle('on', x===it);});
    if(it.dataset.tri){ window.ixTri=it.dataset.tri;
      var sb=document.querySelector('#ixSort button[data-s="'+
        (it.dataset.tri==='tenir'?'recent':it.dataset.tri)+'"]');
      if(sb)sb.click(); }
    if(it.dataset.filt) window.ixFiltre=it.dataset.filt;
    if(it.dataset.cols){ window._ixSetCols(+it.dataset.cols);
      var m3=document.getElementById('ixMenu'); if(m3)m3.classList.remove('on');
      var b3=document.getElementById('ixTriBtn'); if(b3)b3.classList.remove('on');
      e.stopPropagation(); return; }
    try{buildIndex();}catch(_){}
    /* un choix ferme le menu : on revient a l'Index trie. */
    var m2=document.getElementById('ixMenu'); if(m2)m2.classList.remove('on');
    var b2=document.getElementById('ixTriBtn'); if(b2)b2.classList.remove('on');
    e.stopPropagation(); return;}
  var mo=document.getElementById('ixMenu');
  if(mo&&mo.classList.contains('on')){
    mo.classList.remove('on');
    var bb=document.getElementById('ixTriBtn'); if(bb)bb.classList.remove('on');}
},true);
/* La couleur dominante d'une dalle : on echantillonne son canvas et on
   garde la teinte la plus saturee, puis on la ramene a une luminosite
   d'aplat. Chaque parole tenue a donc SA couleur. */
window._teinteDalle=function(cv){try{
  if(!cv||!cv.getContext)return null;
  var br=0,bv=0,bb=0,bs=-1;
  /* ⚑ v29 — une dalle du moteur DÉCLARE sa couleur la plus saturée (`__dalleInfo`, même critère qu'ici) :
     on la lit, on ne relit plus ses pixels (redteam_decoupe, famille C). */
  var _I=cv.__dalleInfo, d=[];
  if(_I){ if(_I.sat){ bs=_I.satS; br=_I.sat[0]; bv=_I.sat[1]; bb=_I.sat[2]; } }
  else { d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; }
  for(var i=0;i<d.length;i+=4){
    if(d[i+3]<120)continue;
    var r=d[i],v=d[i+1],b=d[i+2];
    var mx=Math.max(r,v,b), mn=Math.min(r,v,b);
    if(mx<26||mn>246)continue;             /* ni noir ni blanc */
    var sat=(mx-mn)/mx;
    if(sat>bs){bs=sat;br=r;bv=v;bb=b;}
  }
  if(bs<0.06)return null;   /* vraiment aucune couleur : on laisse le defaut */
  /* on remonte la luminosite pour un aplat lisible */
  /* Le mauve appartient aux Nuees, le terracotta aux brouillons : si la
     teinte de la dalle tombe dans ces plages, on la fait TOURNER vers une
     couleur libre. L'Index se remplit alors de teintes franches et variees. */
  (function(){
    var mx=Math.max(br,bv,bb), mn=Math.min(br,bv,bb), df=mx-mn, H=0;
    if(df>0){
      if(mx===br)H=((bv-bb)/df+(bv<bb?6:0));
      else if(mx===bv)H=((bb-br)/df+2);
      else H=((br-bv)/df+4);
      H*=60;
    }
    /* plages interdites : mauve 255-300, terracotta 10-40 */
    var dec=0;
    if(H>=252&&H<=304) dec = (H<278) ? -66 : +54;   /* vers bleu ou rose vif */
    else if(H>=8&&H<=42) dec = +122;                 /* vers vert franc */
    if(!dec)return;
    var h2=((H+dec)%360+360)%360, s=mx?df/mx:0, v=mx/255;
    var i=Math.floor(h2/60), f=h2/60-i, p1=v*(1-s), q=v*(1-f*s), t2=v*(1-(1-f)*s);
    var R,G,B;
    switch(i%6){
      case 0:R=v;G=t2;B=p1;break; case 1:R=q;G=v;B=p1;break;
      case 2:R=p1;G=v;B=t2;break; case 3:R=p1;G=q;B=v;break;
      case 4:R=t2;G=p1;B=v;break; default:R=v;G=p1;B=q;}
    br=R*255; bv=G*255; bb=B*255;
  })();
  /* on sature franchement : une parole tenue doit eclater, pas murmurer. */
  var moy=(br+bv+bb)/3, SAT=1.42;
  br=moy+(br-moy)*SAT; bv=moy+(bv-moy)*SAT; bb=moy+(bb-moy)*SAT;
  br=Math.max(0,Math.min(255,br)); bv=Math.max(0,Math.min(255,bv));
  bb=Math.max(0,Math.min(255,bb));
  var m=Math.max(br,bv,bb), k=m?(212/m):1;
  if(k<1)k=1; if(k>2.4)k=2.4;
  var R=Math.min(255,Math.round(br*k)), V=Math.min(255,Math.round(bv*k)),
      B=Math.min(255,Math.round(bb*k));
  /* clair ou sombre : quelle encre poser dessus */
  var lum=(R*299+V*587+B*114)/1000;
  return {css:'rgb('+R+','+V+','+B+')', clair:lum>158};
}catch(e){return null;}};
/* apres la peinture des dalles, chaque bloc « tenue » prend sa teinte */
window._teinterTenues=function(){try{
  document.querySelectorAll('#indexList .ix-bloc.tenue').forEach(function(bl){
    var cv=bl.querySelector('canvas'); if(!cv)return;
    var t=window._teinteDalle(cv); if(!t)return;
    bl.style.background=t.css;
    bl.classList.toggle('sur-clair', t.clair);
    /* la dalle garde sa couleur : on ne touche plus a sa fusion */
  });
}catch(e){}};
/* LE FIL — chaque evenement a une nature, donc une couleur et une taille.
   Les memes que l'Index : bleu pour ce qui attend une parole, terracotta
   pour ce qui presse, periwinkle pour ce qui est passe. */
/* le menu du Fil : meme dessin, meme comportement que celui de l'Index */
window.fdFiltre='tous';
/* le filtre du Fil agit sur les bandes deja construites : plus simple et
   plus sur que de dupliquer la logique de buildFeed(). */
window._filtrerFil=function(){try{
  var f=window.fdFiltre||'tous';
  document.querySelectorAll('#feedList .fd-item').forEach(function(el){
    var ok=true, c=el.className;
    if(f==='agir')      ok=/fd-act/.test(c);
    else if(f==='tenues')   ok=/fd-tenue/.test(c);
    else if(f==='demandes') ok=/fd-act/.test(c);
    else if(f==='atenir')   ok=/fd-terra/.test(c);
    else if(f==='nuees')    ok=/fd-nuee/.test(c);
    else if(f==='moi')      ok=/Tu as|Ton Promi/.test(el.textContent||'');
    else if(f==='proches')  ok=!/Tu as|Ton Promi/.test(el.textContent||'');
    el.style.display = ok ? '' : 'none';
  });
}catch(e){}};
/* Le selecteur ne clignote plus : un observateur suit l'affichage du Fil
   et bascule au moment exact du changement, sans delai. */
window._majSelFil=function(){try{
  var v=document.getElementById('feedView'), s=document.getElementById('viewSwitch');
  if(!v||!s)return;
  var ouvert=(v.style.display!=='none');
  s.style.visibility=ouvert?'hidden':'visible';
  s.style.opacity=''; s.style.pointerEvents=ouvert?'none':'';
}catch(e){}};
try{ document.addEventListener('DOMContentLoaded',function(){
  var v=document.getElementById('feedView'); if(!v)return;
  new MutationObserver(function(){_majSelFil();})
    .observe(v,{attributes:true,attributeFilter:['style','class']});
  _majSelFil();
}); }catch(e){}
document.addEventListener('click',function(e){
  var t=e.target;
  if(t.closest&&t.closest('#fdTriBtn')){
    var m=document.getElementById('fdMenu'); if(m)m.classList.add('on');
    var b=document.getElementById('fdTriBtn'); if(b)b.classList.add('on');
    e.stopPropagation(); return;}
  var it=t.closest&&t.closest('#fdMenu .ix-mi');
  if(it){
    var grp=it.dataset.fdtri?'[data-fdtri]':'[data-fdfilt]';
    document.querySelectorAll('#fdMenu .ix-mi'+grp).forEach(function(x){
      x.classList.toggle('on', x===it);});
    if(it.dataset.fdfilt)window.fdFiltre=it.dataset.fdfilt;
    try{buildFeed();}catch(_){}
    try{ if(window._filtrerFil)setTimeout(_filtrerFil,60); }catch(_){}
    var m2=document.getElementById('fdMenu'); if(m2)m2.classList.remove('on');
    var b2=document.getElementById('fdTriBtn'); if(b2)b2.classList.remove('on');
    e.stopPropagation(); return;}
  var mo=document.getElementById('fdMenu');
  if(mo&&mo.classList.contains('on')){mo.classList.remove('on');
    var bb=document.getElementById('fdTriBtn'); if(bb)bb.classList.remove('on');}
},true);
/* les bandes d'un Promi en cours prennent la teinte de sa dalle, comme
   les cases tenues de l'Index : plus aucune bande grise. */
window._teinterFil=function(){try{
  /* seules les bandes SANS couleur de nature prennent la teinte de leur dalle */
  document.querySelectorAll('#feedList .fd-item.fd-teint:not(.fd-nuee):not(.fd-tenue):not(.fd-act)')
    .forEach(function(bl){
    var cv=bl.querySelector('canvas'); if(!cv)return;
    var t=window._teinteDalle&&_teinteDalle(cv);
    if(!t){ /* pas de teinte : on rend l'encre au mode, sinon elle reste figee */
      bl.classList.remove('sur-clair');
      bl.querySelectorAll('.fd-tx,.fd-pre,.fd-t,.fd-react').forEach(function(x){x.style.color='';});
      return; }
    bl.style.background=t.css;
    bl.classList.toggle('sur-clair', t.clair);
  });
}catch(e){}};
window.filNature=function(f,p,pending){
  /* CHICHE (lot 25) — l'accent porte la nature, la dalle garde son monde (CLAUDE.md §4).
     Un Chiche REÇU est un défi lancé : il attend qu'on le RELÈVE (geste, comme une parole
     qui attend). Un Chiche RELEVÉ est une bonne nouvelle. Les deux en accent framboise. */
  if(f.type==='chiche_recu')   return {cls:'fd-act fd-chiche',col:'',pre:'UN CHICHE POUR TOI'};
  if(f.type==='chiche_releve') return {cls:'fd-chiche',col:'',pre:'CHICHE RELEVÉ'};
  /* v89 (Q347) — une invitation reçue ; une moitié tracée qui attend la mienne (« À RELEVER », cadre 76) */
  if(f.type==='invitation'&&!f.fait) return {cls:'fd-act fd-nuee',col:'',pre:'UN CERCLE T’ATTEND'};
  if(f.type==='moitie'&&window._filAttend&&window._filAttend(f)) return {cls:'fd-act'+(p&&p.chiche?' fd-chiche':' fd-teint'),col:'',pre:(p&&p.chiche?'CHICHE':'PROMI')};
  /* une demande attend un geste : orange, comme « a tenir » dans l'Index.
     Le bleu n'est plus un etat depuis l'arret de la palette. */
  if(pending) return {cls:'fd-act fd-terra',col:'#DD4D23',pre:'UNE PAROLE T’ATTEND'};
  if(f.type==='due'||f.type==='late')
    return {cls:'fd-act fd-terra',col:'#DD4D23',pre:'TON PROMI ARRIVE'};
  /* un Promi bascule en « a tenir » : sa ligne porte l'orange. */
  /* un Promi bascule en « a tenir » : sa ligne porte l'orange ET son geste,
     pour qu'on puisse le tenir sans quitter le Fil. */
  if(f.type==='missed'||/est à tenir/.test(f.text||''))
    return {cls:'fd-act fd-terra',col:'#DD4D23',pre:'À TENIR'};
  var PRE={kept:'PAROLE TENUE',added:'PROMI PLANTÉ',accepted:'PROMI ACCEPTÉ',
           joined:'CERCLE REJOINT',received:'DEMANDE',comment:'COMMENTAIRE'};
  if(f.type==='kept') return {cls:'fd-tenue',col:'',pre:'PAROLE TENUE'};
  if(f.type==='joined'||/nu[ée]e/i.test(f.text||''))
    return {cls:'fd-nuee',col:'',pre:'CERCLE'};
  if(p&&p.draft||/mis de côté/.test(f.text||''))
    return {cls:'fd-brouillon',col:'',pre:'BROUILLON'};
  /* un Chiche en cours : accent framboise (libellé + contour), dalle gardée (§4) */
  if(p&&p.chiche&&!p.draft&&!p.req) return {cls:'fd-teint fd-chiche',col:'',pre:'CHICHE'};
  /* un Promi en cours : sa bande prendra la teinte de sa dalle */
  if(p&&!p.draft&&!p.req) return {cls:'fd-teint',col:'',pre:(PRE[f.type]||'PROMI')};
  return {cls:'',col:'',pre:(PRE[f.type]||'')};
};

/* ══ GARDE-FOU DE LISIBILITE ══
   Une passe finale compare chaque texte a la couleur REELLE de son fond et
   corrige ce qui ne contraste pas assez. Aucune regle CSS ne peut couvrir
   tous les cas (fonds calcules en JS, aplats, transparences empilees) :
   ce controle-la, lui, les couvre tous. */
window._lisibilite=function(racine){try{
  /* jamais sur le document entier : c'est un balayage complet du DOM. */
  var zone=racine; if(!zone) return;
  function fond(el){
    var e=el;
    while(e && e!==document.body){
      var c=getComputedStyle(e).backgroundColor;
      var m=c.match(/[\d.]+/g);
      if(m && (m.length<4 || +m[3]>0.55)) return [+m[0],+m[1],+m[2]];
      e=e.parentElement;
    }
    return [32,25,8];
  }
  function lum(c){return (c[0]*299+c[1]*587+c[2]*114)/1000;}
  zone.querySelectorAll('.fd-tx,.fd-pre,.fd-t,.fd-react,.ix-bn,.ix-bj,.ix-bw')
    .forEach(function(x){
      /* les bandes et cases qui portent deja une couleur de nature ont leur
         encre decidee en CSS : on ne la recalcule pas. */
      var par=x.closest('.fd-nuee,.fd-tenue,.fd-act,.ix-bloc.nuee,.ix-bloc.menthe,.ix-bloc.vif');
      if(par) return;
      var g=fond(x), lg=lum(g);
      var f=(getComputedStyle(x).color.match(/[\d.]+/g)||[0,0,0]).map(Number);
      if(Math.abs(lum(f)-lg)>=52) return;          /* deja lisible */
      var clair=lg>150;
      var doux=/fd-t|fd-react|fd-pre|ix-bw/.test(x.className);
      /* un TITRE prend toujours l'encre pleine, jamais un gris : c'est lui
         qu'on lit en premier. Seuls les textes secondaires s'attenuent. */
      x.style.color = clair
        ? (doux?'rgba(32,25,8,.74)':'#201908')
        : (doux?'rgba(247,240,222,.76)':'#F7F0DE');
      if(!doux) x.style.opacity='1';
    });
}catch(e){}};

/* ══ LE DEZOOM DE L'INDEX ══
   Pincement a deux doigts, comme l'app Photos : 2, 3 ou 4 colonnes.
   La transition est elastique (cubic-bezier long), jamais seche. Le pas
   suit le meme seuil que la Toile : un changement par 18 % d'ecartement. */
window.ixCols = window.ixCols || 2;
window._ixSetCols = function(n, doux){
  n = Math.max(2, Math.min(4, n|0));
  if(n === window.ixCols) return;
  window.ixCols = n;
  var g = document.querySelector('#indexSheet .ix-blocs');
  if(!g) return;
  if(doux !== false) g.style.transition = 'grid-template-columns .42s cubic-bezier(.22,1,.36,1)';
  g.style.gridTemplateColumns = 'repeat(' + n + ',1fr)';
  document.querySelectorAll('#indexSheet .ix-mi[data-cols]').forEach(function(x){
    x.classList.toggle('on', +x.dataset.cols === n); });
  /* les textes retrecissent avec la case, sinon ils debordent a x4 */
  var sh = document.getElementById('indexSheet');
  if(sh){ sh.classList.remove('cols2','cols3','cols4'); sh.classList.add('cols'+n); }
  try{ if(window.peintMinis) setTimeout(function(){
    peintMinis(document.getElementById('indexList')); }, 60); }catch(e){}
  try{ if(navigator.vibrate) navigator.vibrate(6); }catch(e){}
};
(function(){
  var d0 = 0, cols0 = 2, actif = false;
  function dist(t){
    var dx = t[0].clientX - t[1].clientX, dy = t[0].clientY - t[1].clientY;
    return Math.hypot(dx, dy);
  }
  document.addEventListener('touchstart', function(e){
    var l = document.getElementById('indexList');
    if(!l || e.touches.length !== 2) return;
    if(!l.contains(e.target)) return;
    d0 = dist(e.touches); cols0 = window.ixCols; actif = true;
  }, {passive:true});
  document.addEventListener('touchmove', function(e){
    if(!actif || e.touches.length !== 2) return;
    var r = dist(e.touches) / (d0 || 1);
    /* un pas tous les 18 % : la meme sensibilite que la Toile */
    var pas = 0;
    if(r < 0.82) pas = Math.round((0.82 - r) / 0.18) + 1;
    else if(r > 1.22) pas = -(Math.round((r - 1.22) / 0.18) + 1);
    if(pas) window._ixSetCols(cols0 + pas);
  }, {passive:true});
  document.addEventListener('touchend', function(){ actif = false; }, {passive:true});
})();

/* ══ LE TITRE PREND LA COULEUR DE SA DALLE ══
   Ce qui est entre guillemets porte la teinte de sa propre matiere : chaque
   Promi devient reconnaissable a sa couleur. Les Nuees gardent l'encre : c'est
   le nom du groupe qui compte, pas une matiere. */
window._titresTeintes = function(racine){ try{
  var zone = racine || document;
  zone.querySelectorAll('.ix-bloc:not(.nuee),.fd-item:not(.fd-nuee)').forEach(function(el){
    var cv = el.querySelector('canvas');
    var t  = el.querySelector('.ix-bn,.fd-tx');
    if(!cv || !t) return;
    var c = window._teinteDalle && _teinteDalle(cv);
    if(!c) return;
    /* le fond de la case : la teinte du titre doit s'en detacher */
    var bg = getComputedStyle(el).backgroundColor.match(/[\d.]+/g) || [28,29,34];
    var lb = (+bg[0]*299 + +bg[1]*587 + +bg[2]*114)/1000;
    var m  = c.css.match(/[\d.]+/g) || [0,0,0];
    var lt = (+m[0]*299 + +m[1]*587 + +m[2]*114)/1000;
    /* Le titre porte TOUJOURS la couleur de sa dalle. Si la teinte se noie
       dans le fond, on la remonte en luminosite plutot que de renoncer :
       avant, un titre sur trois restait a l'encre. */
    var css = c.css;
    if(Math.abs(lt - lb) < 62){
      var v = (css.match(/[\d.]+/g) || [0,0,0]).map(Number);
      var vers = (lb > 128) ? 0 : 255;          /* fond clair -> assombrir */
      var k = 0.52;
      css = 'rgb(' + v.slice(0,3).map(function(x){
        return Math.round(x + (vers - x) * k); }).join(',') + ')';
    }
    /* seul le NOM se teinte — pas les guillemets, pas le reste de la phrase */
    var h = t.innerHTML;
    if(/«[^»]*»/.test(h)){
      t.innerHTML = h.replace(/«\s*([^»]*?)\s*»/g,
        '«\u00a0<span style="color:' + css + '">$1</span>\u00a0»');
    } else {
      t.style.color = css;
    }
  });
}catch(e){} };
/* les deux lignes legales : conditions et suppression de compte. */
document.addEventListener('click',function(e){
  var t=e.target.closest&&e.target.closest('#cguCard,#delAccount');
  if(!t)return;
  /* ⚑ v16 : les deux lignes passent par lot-V16 — une page « bientôt disponible » propre, et une
     suppression qui demande confirmation puis laisse quelques secondes pour annuler. */
  e.stopPropagation();
  if(t.id==='cguCard'){ if(window._v16Legal) window._v16Legal('cgu'); return; }
  if(window._v16SupprimerCompte) window._v16SupprimerCompte();
},true);

/* ══ LA TRAME DES REGLAGES — la dalle du Studio, en grand, en haut ══
   L'ancien canvas portait des taches floues heritees d'un rendu decoratif.
   On le repeint avec la VRAIE dalle du monde actif, comme le moodboard :
   grande, en haut, tres effacee. Elle suit le Studio. */
window._trameReglages = function(){ try{
  /* EXACTEMENT le fond de la page « nouveau Promi » : le meme appel, les memes
     options. cut:0 supprime la scission verticale ; size et y sont ceux de
     createSheet. Aucune reinvention. */
  promiTrame('stTrameCv','settingsScreen',{cut:0,size:0.52,y:0.40});
  if(window._dalleDerive) _dalleDerive('settingsScreen');
}catch(e){} };

/* la seconde dalle : une VRAIE dalle, plus grande que la fixe, qui derive.
   Elle est peinte dans son propre canvas, sous le contenu. */
window._dalleDerive = function(hostId){ try{
  var host = document.getElementById(hostId);
  if(!host || !window.Toile || !Toile.dalleTrame) return;
  /* le canvas derive : il vit dans un conteneur qui le CLIPPE, sinon son
     transform le fait sortir du cadre de l'ecran. */
  var box = host.querySelector('.pd-driftbox');
  if(!box){
    box = document.createElement('div');
    box.className = 'pd-driftbox'; box.setAttribute('aria-hidden','true');
    host.insertBefore(box, host.firstChild);
  }
  var cv = box.querySelector('.pd-drift');
  if(!cv){
    cv = document.createElement('canvas');
    cv.className = 'pd-drift'; cv.setAttribute('aria-hidden','true');
    box.appendChild(cv);
  }
  var p = (typeof promises !== 'undefined')
    ? promises.find(function(z){ return !z.draft && !z.req; }) : null;
  if(!p) return;
  var W = host.clientWidth || 390, H = host.clientHeight || 844;
  var dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
  /* ⚑ v29 — la dalle rendue par le moteur À SA TAILLE (0,86 W de large au plus), jamais agrandie ensuite */
  var src = window._rendDalle ? window._rendDalle(p.id, W*0.86*dpr, H*0.5*dpr, {courant:1}) : null;   /* v30 · page + : le monde courant, exprès */
  if(!src || !src.width) return;
  cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr);
  cv.style.width = W+'px'; cv.style.height = H+'px';
  var g = cv.getContext('2d'); if(!g) return;
  g.setTransform(dpr,0,0,dpr,0,0);
  g.clearRect(0,0,W,H);
  /* plus grande que la dalle fixe (0.52 W) sans etre enorme : 0.86 W */
  /* le rapport de la SOURCE est respecte a la lettre : sans ca la dalle
     s'ecrase horizontalement quand le canvas n'est pas carre. */
  g.imageSmoothingEnabled = true;
  g.imageSmoothingQuality = 'high';
  /* la derive est peinte : on lit les variables posees par l'animation */
  var gx = parseFloat(getComputedStyle(host).getPropertyValue('--gx')) || 0;
  var gy = parseFloat(getComputedStyle(host).getPropertyValue('--gy')) || 0;
  var gr = parseFloat(getComputedStyle(host).getPropertyValue('--grot')) || 0;
  /* la dalle est TEINTÉE au signal de la nature : Chiche → framboise, Nuée → mauve
     (le Promi garde la couleur de son monde). Blend 'color' garde la matière/forme,
     'destination-in' restaure l'alpha (comme teinteMauve de la bande de Nuée). */
  var srcT = src;
  try{ var _k = (window.createKind) || (host.getAttribute && host.getAttribute('data-kind'));
    var _tt = {chiche:'#FFB8D2', nuee:'#C9A8F5'}[_k];
    if(_tt){ var _tc=document.createElement('canvas'); _tc.width=src.width; _tc.height=src.height;
      var _tg=_tc.getContext('2d'); if(_tg){ _tg.drawImage(src,0,0);
        _tg.globalCompositeOperation='color'; _tg.fillStyle=_tt; _tg.fillRect(0,0,_tc.width,_tc.height);
        _tg.globalCompositeOperation='destination-in'; _tg.drawImage(src,0,0);
        _tg.globalCompositeOperation='source-over'; srcT=_tc; } }
  }catch(_){}
  g.save();
  g.translate(W/2 + gx, H/2 + gy);
  g.rotate(gr * Math.PI / 180);
  g.translate(-W/2, -H/2);
  /* centree horizontalement, vers le haut : elle doit se voir en entier — posée 1:1, rotation gardée */
  window._poseUn(g, srcT, W/2, H*0.24);
  g.restore();
}catch(e){} };

/* ══ LE GESTE ══
   Deux points. On trace de l'un a l'autre — le chemin est libre, le couloir
   fait 62 px. Ralentir ouvre l'espace d'ecriture. Rien ne gronde jamais. */
/* la bascule trait / bouton : un geste ou un appui, au choix. */
document.addEventListener('click', function(e){
  var a = e.target.closest && e.target.closest('#tenirAlt');
  if(!a) return;
  var dp = document.getElementById('detailPoster');
  dp.classList.toggle('geste-bouton');
  try{ if(window._tenirPeindre) _tenirPeindre(); }catch(_){}
  e.stopPropagation();
}, true);
/* bascule trait/bouton de la fiche : deux petites flèches discrètes (comme la page +) */
(function(){ try{ var _sw='<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.5 8 L10 4.5 L13.5 8"/><path d="M6.5 12 L10 15.5 L13.5 12"/></svg>';
  var _set=function(){ var a=document.getElementById('tenirAlt'); if(a && !a.querySelector('svg')){ a.innerHTML=_sw; a.setAttribute('aria-label','trait ou bouton'); } };
  document.addEventListener('DOMContentLoaded',_set); setTimeout(_set,1500); setTimeout(_set,3000);
  var _dp=document.getElementById('detailPoster'); if(_dp){ new MutationObserver(_set).observe(_dp,{attributes:true,attributeFilter:['class']}); }
}catch(_){} })();
window._tenirInit = function(){ try{
  var zone = document.getElementById('tenirZone');
  var cv   = document.getElementById('tenirCv');
  var lab  = document.getElementById('tenirLab');
  if(!zone || !cv || zone._pose) return;
  zone._pose = true;

  var g, W, H, dpr, pts = [], actif = false, arrive = false, lent = false;
  var ouverture = false;
  var t0 = 0, dernierT = 0, dernierP = null, lentMs = 0;

  function taille(){
    dpr = Math.min(2, window.devicePixelRatio || 1);
    /* on mesure le CANVAS a l'ecran, pas son parent : c'est lui qui recoit
       le doigt, et sa hauteur reelle peut differer de celle de la zone. */
    var r = cv.getBoundingClientRect();
    W = Math.round(r.width) || zone.clientWidth;
    H = Math.round(r.height) || zone.clientHeight;
    /* les bornes suivent le doigt reel : le canvas bouge, pas lui. */
    if(yEcran !== null) yAncre = yEcran - r.top;
    cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr);
    g = cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
  }
  /* la hauteur des bornes : le centre au repos, puis LA HAUTEUR DU DOIGT
     des qu'il s'est pose. Le haut du canvas ne bouge pas quand la zone
     s'ouvre — inutile de lutter contre, on suit le doigt. */
  var yAncre = null, yEcran = null;
  function bornes(){
    var y = (yAncre !== null) ? yAncre : H/2;
    return { a:{x:38, y:y}, b:{x:W-38, y:y}, r:19 };
  }
  function encre(){
    /* le trait porte la couleur de SA dalle : chaque parole a sa teinte. */
    try{ if(!document.getElementById('detailPoster').classList.contains('geste-encre')
      && window._encreGeste) return window._encreGeste; }catch(_){}
    /* sinon l'encre du fond : blanche sur un aplat vif */
    var dp = document.getElementById('detailPoster');
    var bg = getComputedStyle(dp).backgroundColor.match(/[\d.]+/g) || [32,25,8];
    var lum = (+bg[0]*299 + +bg[1]*587 + +bg[2]*114)/1000;
    return lum > 150 ? '#201908' : '#F7F0DE';
  }
  function peindre(){
    if(!g) return;
    var c = encre(), B = bornes();
    g.clearRect(0,0,W,H);
    if(!lent){
      /* le point de depart, plein ; celui d'arrivee, en creux */
      g.fillStyle = c; g.globalAlpha = actif ? .34 : 1;
      g.beginPath(); g.arc(B.a.x,B.a.y,B.r,0,6.2832); g.fill();
      g.globalAlpha = 1;
      g.strokeStyle = c; g.globalAlpha = arrive ? 1 : .4; g.lineWidth = 2.5;
      g.beginPath(); g.arc(B.b.x,B.b.y,B.r,0,6.2832); g.stroke();
      g.globalAlpha = arrive ? 1 : .4;
      g.fillStyle = c;
      g.beginPath(); g.arc(B.b.x,B.b.y,6,0,6.2832); g.fill();
      g.globalAlpha = 1;
    }
    /* le trace */
    if(pts.length > 1){
      g.strokeStyle = c; g.lineWidth = lent ? 5 : 8;
      g.lineCap = 'round'; g.lineJoin = 'round';
      /* des ONDES, pas des segments : chaque point devient le milieu d'une
         courbe quadratique, comme un trait a la main. */
      g.beginPath(); g.moveTo(pts[0].x, pts[0].y);
      if(pts.length === 2){ g.lineTo(pts[1].x, pts[1].y); }
      else {
        for(var i=1; i<pts.length-1; i++){
          var mx = (pts[i].x + pts[i+1].x) / 2;
          var my = (pts[i].y + pts[i+1].y) / 2;
          g.quadraticCurveTo(pts[i].x, pts[i].y, mx, my);
        }
        g.quadraticCurveTo(pts[pts.length-2].x, pts[pts.length-2].y,
                           pts[pts.length-1].x, pts[pts.length-1].y);
      }
      g.stroke();
      /* l'eclat sous le doigt */
      if(actif){
        var p = pts[pts.length-1];
        /* un halo, pas des rayons : c'etait trop appuye. */
        g.globalAlpha = .2; g.lineWidth = 1.1;
        for(var k=0;k<6;k++){
          var a = k*1.0472;
          g.beginPath();
          g.moveTo(p.x + 18*Math.cos(a), p.y + 18*Math.sin(a));
          g.lineTo(p.x + 25*Math.cos(a), p.y + 25*Math.sin(a));
          g.stroke();
        }
        g.globalAlpha = 1;
      }
    }
  }
  function pos(e){
    var r = cv.getBoundingClientRect();
    var t = e.touches ? e.touches[0] : e;
    return { x: t.clientX - r.left, y: t.clientY - r.top };
  }
  function vibrer(ms){ try{ if(navigator.vibrate) navigator.vibrate(ms); }catch(_){ } }

  function debut(e){
    var p = pos(e), B = bornes();
    /* on ne part que du point de gauche — sinon on ouvrirait a chaque frolement */
    /* on part du tiers gauche, a n'importe quelle hauteur : les deux
       points viendront se poser la ou le doigt se trouve. */
    /* on peut poser le doigt largement autour du point : le trait
       demarrera de toute facon dans le rond. */
    if(p.x > B.a.x + 130) return;
    actif = true; arrive = false; lent = false; lentMs = 0;
    var _t0 = e.touches ? e.touches[0] : e;
    yEcran = _t0.clientY;
    yAncre = p.y;
    /* LE TRAIT PART DU ROND, pas du doigt : sinon on perd le centimetre
       entre le point et l'endroit ou le pouce s'est reellement pose. */
    var B0 = bornes();
    /* le trait DEMARRE au centre du rond, puis rejoint le doigt. */
    pts = [{x: B0.a.x, y: B0.a.y}];
    if(Math.hypot(p.x-B0.a.x, p.y-B0.a.y) > 6) pts.push(p);
    t0 = Date.now(); dernierT = t0; dernierP = p;
    zone.classList.add('ouvert');
    document.getElementById('detailPoster').classList.add('tracant');
    /* on suit l'ouverture image par image : sans ca le canvas garde son
       ancienne taille pendant 300 ms et son contenu s'etire vers le haut —
       d'ou le trait qui semblait partir du coin. */
    /* pendant l'ouverture on ne trace PAS : on redimensionne seulement.
       Le trace repart du doigt une fois la zone stabilisee — sinon le
       premier point, capture avant, remonte dans le coin. */
    ouverture = true; pts = [];
    var fin0 = Date.now() + 340;
    (function suivre(){
      taille(); peindre();
      if(Date.now() < fin0) requestAnimationFrame(suivre);
      else { ouverture = false; }
    })();
    vibrer(6);
    e.preventDefault();
  }
  function bouge(e){
    if(!actif) return;
    var p = pos(e), maintenant = Date.now();
    /* la lenteur ouvre l'ecriture : moins de 40 px/s pendant 300 ms */
    if(dernierP){
      var d = Math.hypot(p.x-dernierP.x, p.y-dernierP.y);
      var dt = Math.max(1, maintenant - dernierT);
      var v = d / dt * 1000;
      if(v < 40){ lentMs += dt; if(lentMs > 300 && !lent){ lent = true; vibrer(10);
        /* (message retire : il embrouillait) */ } }
      else lentMs = 0;
    }
    dernierP = p; dernierT = maintenant;
    /* pendant l'ouverture, le trace attend : la zone bouge encore */
    if(ouverture){ peindre(); e.preventDefault(); return; }
    pts.push(p);
    var B = bornes();
    /* l'arrivee se juge sur X seulement : la hauteur change quand l'espace
       s'ouvre, et exiger une position verticale precise rendrait le geste
       impossible. Le couloir occupe toute la hauteur. */
    /* on valide des les DEUX TIERS parcourus : exiger le dernier pixel
       rendait le geste anxieux. Deux tiers, c'est deja franc et voulu. */
    if(!arrive && p.x > B.a.x + (B.b.x - B.a.x) * 0.66){
      arrive = true; vibrer(14);
      if(lab) lab.textContent = 'PAROLE TENUE !';
      try{ zone.classList.add('atteint'); }catch(_){}
    }
    peindre();
    e.preventDefault();
  }
  function fin(){
    if(!actif) return;
    actif = false;
    /* trois voies : on est arrive, ou on a ecrit, ou on a parcouru
       une bonne moitie de la zone. Rien ne doit echouer par surprise. */
    var parcouru = 0;
    if(pts.length > 1) parcouru = pts[pts.length-1].x - pts[0].x;
    if(arrive || (lent && pts.length > 6) || parcouru > W * 0.5){
      /* la parole est tenue : on garde la trace et on bascule le statut */
      try{ window._traceTenir = pts.slice();
        if(typeof cur !== 'undefined' && cur) cur.trace = pts.slice();
      }catch(_){ }
      vibrer([12,40,26]);
      try{
        var b = document.querySelector('#segStatus button[data-st="tenu"]');
        if(b) b.click();
      }catch(_){ }
    }
    /* rien ne gronde : tout se referme doucement */
    zone.classList.remove('ouvert');
    document.getElementById('detailPoster').classList.remove('tracant');
    lent = false; arrive = false; yAncre = null; yEcran = null;
    zone.classList.remove('atteint');
    if(lab) lab.textContent = 'glisse pour tenir ta parole \u2192';
    setTimeout(function(){ pts = []; taille(); peindre(); }, 330);
  }

  zone.addEventListener('touchstart', debut, {passive:false});
  zone.addEventListener('touchmove',  bouge, {passive:false});
  zone.addEventListener('touchend',   fin,   {passive:true});
  zone.addEventListener('mousedown',  debut);
  window.addEventListener('mousemove', bouge);
  window.addEventListener('mouseup',   fin);
  window.addEventListener('resize', function(){ taille(); peindre(); });
  taille(); peindre();
  window._tenirPeindre = function(){ taille(); peindre(); };
}catch(e){} };

/* ══════════════════════════════════════════════════════════
   LA FICHE DU MOODBOARD
   Le fond porte la couleur de l'etat. La dalle occupe le haut.
   Puis : a qui · la parole · quand · le lien · le geste.
   Tout le reste vit sous « Details ».
   ══════════════════════════════════════════════════════════ */

/* ══ LA DALLE DE LA FICHE — PLEIN CADRE ══
   Le moodboard montre la matiere qui remplit tout le tiers haut. promiTrame
   pose une dalle a 52 % dans un coin : ce n'est pas ca. On la peint nous-meme,
   repetee, jusqu'a couvrir. */
window._ficheDalle = function(){ try{
  var dp = document.getElementById('detailPoster');
  var cv = document.getElementById('dpTrameCv');
  if(!dp || !cv || !window.Toile || !Toile.dalleTrame) return;
  /* sur une fiche de Nuee, « cur » est nul : c'est « curNuee » qui porte le
     groupe. Sans ca la planche de dalles ne se dessinait jamais. */
  var estN = dp.classList.contains('dp-nuee') || dp.classList.contains('dp-mode-nuee');
  var cle = estN ? (typeof curNuee !== 'undefined' ? curNuee : null)
                 : ((typeof cur !== 'undefined' && cur) ? cur : null);
  if(!cle) return;

  /* HD : on demande la dalle a une echelle qui couvre la taille d'affichage.
     Avant on agrandissait une vignette de 62 px sur 300 : d'ou la pixelisation. */
  /* EXACTEMENT l'appel de peintMinis, qui marche dans les neuf mondes.
     L'echelle 6 cassait mosaique, braille, pixel et gravure : elles
     retombaient sur un rendu polygonal. */
  /* ── L'IDENTITE EN HAUT, LA DIVERSITE EN BAS (CLAUDE.md §4) ──
     La bande d'une Nuee est MAUVE, toujours : couleur signal du collectif. Mais
     l'IDENTITE MAUVE PORTE SUR LA TEINTE, JAMAIS SUR LA FORME : on montre de
     VRAIES dalles du moteur (Toile.dalleTrame), simplement TEINTEES mauve. Jamais
     un polygone reconstruit. Le fil, lui, garde les vrais mondes (non teintes). */
  /* ⚑ v100 — SUR UNE NUÉE, CE CANEVAS A UN AUTRE PROPRIÉTAIRE. `_ficheNuee` y peint la bande (le semis de la planche
     promi-nuee-toile) et la recouvre entièrement ; la grappe mauve ci-dessous (teinture retirée de ce champ le 29 août, Q94)
     était peinte pour rien à chaque passe — ~135 ms mesurés dans la tâche d'ouverture — et pouvait paraître une image avant
     d'être recouverte. Deux propriétaires pour un canevas (CLAUDE.md §7) : on laisse la main à celui qui fait foi. */
  if(estN && typeof window._ficheNuee === 'function') return;
  if(estN){
    var idsN = [];
    try{ idsN = promises.filter(function(q){ return q.nuee === cle && !q.draft; })
                        .map(function(q){ return q.id; }); }catch(_){}
    if(!idsN.length){ try{ var q0=promises.filter(function(x){return !x.draft;})[0]; if(q0) idsN=[q0.id]; }catch(_){} }
    if(!idsN.length) return;
    var W2 = dp.clientWidth || 390, H2 = 300;
    var dpr2 = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    cv.width = Math.round(W2*dpr2); cv.height = Math.round(H2*dpr2);
    cv.style.width = W2+'px'; cv.style.height = H2+'px';
    var g2 = cv.getContext('2d'); if(!g2) return;
    g2.setTransform(dpr2,0,0,dpr2,0,0);
    g2.clearRect(0,0,W2,H2);
    g2.imageSmoothingEnabled = true; g2.imageSmoothingQuality = 'high';
    cv.style.setProperty('opacity','1','important');
    cv.style.setProperty('filter','none','important');
    /* teinte mauve d'une VRAIE dalle : blend 'color' (garde forme + matiere +
       luminance de la dalle, applique la teinte/saturation mauve), puis on
       restaure l'alpha d'origine ('destination-in') pour ne pas peindre le fond. */
    /* teinte mauve d'une VRAIE dalle. Blend 'color' garde la forme + la matière, mais
       AUSSI la luminance de la source : une dalle encre pâle reste pâle et se noie dans
       la bande. On remonte donc luminance + saturation par un voile lilas 'source-atop'
       (uniquement sur les pixels de la dalle) : la dalle ressort TOUJOURS plus claire que
       la bande, dans les deux thèmes. La teinte varie d'une dalle à l'autre — c'est ce qui
       la rend vivante plutôt qu'un aplat mauve répété. */
    function teinteMauve(src, cible){ var w=src.width,h=src.height; if(!w||!h) return null;
      var t=document.createElement('canvas'); t.width=w; t.height=h;
      var c=t.getContext('2d'); if(!c) return null;
      c.drawImage(src,0,0);
      c.globalCompositeOperation='color'; c.fillStyle=cible; c.fillRect(0,0,w,h);
      c.globalCompositeOperation='source-atop'; c.fillStyle='rgba(201,169,255,.30)'; c.fillRect(0,0,w,h);
      c.globalCompositeOperation='destination-in'; c.drawImage(src,0,0);
      c.globalCompositeOperation='source-over'; return t; }
    /* GRAPPE HARMONIEUSE (pas un éparpillement) : les VRAIES dalles du monde, teintées
       mauve, en cluster resserré au centre — une grosse au cœur, les autres autour, qui
       se touchent. On privilégie les dalles UNIQUES des Promi de la Nuée (pas de répétition
       tant qu'il en reste). Taille ≈ native (léger facteur de présence), profondeur par
       l'ombre. « L'identité en haut » : la matière du monde, en mauve. */
    var CEN = [[0.47,0.50,1.30],[0.30,0.40,1.02],[0.63,0.37,1.08],[0.66,0.63,0.96],[0.37,0.66,0.92],[0.52,0.72,0.86]];
    var TEINTES = ['#B08BED','#9867E9','#CCB3F6','#291547','#BE9EF6','#A576EE'];
    var nU = idsN.length;
    var count = Math.min(CEN.length, Math.max(3, nU>=4 ? nU : (nU*2)));  /* assez de matière, sans bouillie */
    g2.globalAlpha = 1; g2.globalCompositeOperation = 'source-over';
    for(var k2=0; k2<count; k2++){
      var scl = CEN[k2][2];
      /* ⚑ v29 — rendue au facteur de présence par le moteur (k = scl), posée 1:1 — plus agrandie après */
      var srcN = document.createElement('canvas');
      if(!Toile.dalleTrame(srcN, idsN[k2%nU], scl)) continue;
      var tin = teinteMauve(srcN, TEINTES[k2%TEINTES.length]); if(!tin) continue;
      var cx = W2*CEN[k2][0], cy = H2*CEN[k2][1];
      g2.save();
      g2.shadowColor='rgba(40,16,78,.26)'; g2.shadowBlur=9; g2.shadowOffsetY=5;
      window._poseUn(g2, tin, cx, cy);
      g2.restore();
    }
    return;
  }

  if(!cle || !cle.id) return;
  /* ⚑ v29 — la dalle est rendue PLUS BAS, à la taille de sa zone (redteam_decoupe) ; ici on s'assure qu'elle existe */
  if(!(window.Toile && Toile.dalleAbs && Toile.dalleAbs(cle.id))) return;
  function _teinteBande(src0){ var src = src0;
  /* Chiche : la bande porte l'identité framboise, comme la Nuée porte le mauve.
     VRAIE dalle du moteur, seulement TEINTÉE (§4) — jamais une forme inventée.
     Même méthode que teinteMauve : blend 'color' + remontée de luminance 'source-atop'
     (sinon ton-sur-ton), puis 'destination-in' pour garder l'alpha de la dalle. */
  try{ if(dp.classList.contains('dp-chiche')){
    var _fc=document.createElement('canvas'); _fc.width=src0.width; _fc.height=src0.height;
    var _fx=_fc.getContext('2d');
    if(_fx){ _fx.drawImage(src0,0,0);
      _fx.globalCompositeOperation='color'; _fx.fillStyle='#FFB8D2'; _fx.fillRect(0,0,_fc.width,_fc.height);
      _fx.globalCompositeOperation='source-atop'; _fx.fillStyle='rgba(255,183,208,.30)'; _fx.fillRect(0,0,_fc.width,_fc.height);
      _fx.globalCompositeOperation='destination-in'; _fx.drawImage(src0,0,0);
      _fx.globalCompositeOperation='source-over'; src=_fc; } } }catch(_){}
  return src; }


  var W = dp.clientWidth || 390;
  var H = Math.round((dp.clientHeight || 844) * 0.36);
  var dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
  cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr);
  cv.style.width = W+'px'; cv.style.height = H+'px';
  var g = cv.getContext('2d'); if(!g) return;
  g.setTransform(dpr,0,0,dpr,0,0);
  g.clearRect(0,0,W,H);
  g.imageSmoothingQuality = 'high';
  /* l'opacite est posee en inline : une regle groupee avec « .tracant »
     la ramenait a 0,5 sans qu'aucun selecteur ne le laisse voir. */
  cv.style.setProperty('opacity','1','important');
  cv.style.setProperty('filter','none','important');
  cv.style.setProperty('mix-blend-mode','normal','important');

  /* on repete la dalle en quinconce jusqu'a couvrir : c'est la matiere du
     monde qui remplit, pas un motif isole dans un coin. */
  /* des tuiles plus petites et plus nombreuses : c'est la densite qui fait
     la matiere. A 52 % on n'en posait que trois, d'ou le coin vide. */
  /* UNE SEULE DALLE, grande et nette, debordant en haut a droite.
     La repetition en tuiles faisait un motif de papier peint : ce n'est pas
     le moodboard, qui montre UNE matiere posee, franche et simple. */
  /* la dalle occupe le bloc en entier, nette, centree. Le bloc la clippe :
     ses contours sont donc francs, jamais flous. */
  /* on la CONTEMPLE : elle tient dans le bloc au lieu de le remplir a ras.
     Un souffle tres lent la fait vivre — 0,6 % d'amplitude, 9 secondes. */
  /* AUCUNE animation propre : la fiche herite du mouvement de la Toile.
     Un souffle ajoute par-dessus se voyait et faisait cheap. */
  /* le meme mouvement d'arrivee que la Toile : la dalle grandit depuis 92 %
     en 520 ms, courbe elastique. Rien de plus. */
  var t0 = window._ficheT0 || 0;
  var e = Math.min(1, (Date.now() - t0) / 520);
  var k = 0.92 + 0.08 * (1 - Math.pow(1 - e, 3));
  /* ⚑ LA DALLE SE CENTRE DANS CE QU'ON VOIT, PAS DANS LE CANEVAS. Signalé par Tom,
     capture à l'appui : « dans les fiches, les dalles apparaissent superposées et sous le
     bandeau du titre et ✕ fermer en haut ; elles sont tronquées et cachées car elles
     passent dessous, ça gâche la visualisation ».
     Mesuré, fiche « à tenir » : le canevas va de **y 0 à 338**, la matière est peinte de
     **0 à 291** — et le plateau descend à **100**. Cent pixels de dalle passaient donc
     littéralement dessous. La cause tient en une ligne : la dalle était centrée sur
     `(H - dh) / 2`, c'est-à-dire au milieu de TOUT le canevas, plateau compris.
     Elle se centre désormais dans la ZONE VISIBLE — sous le bandeau, jusqu'à l'onde —
     et elle est dimensionnée sur cette zone, donc elle n'est plus rognée. */
  var _rc = cv.getBoundingClientRect();
  var _hcss = _rc.height || 1;
  var _dev = document.getElementById('device');
  var _ech = _dev ? ((_dev.getBoundingClientRect().width || 390) / 390) : 1;
  /* 124 = le bas du plateau (100) plus 24 d'air, en cotes d'écran 390.
     ⚠ 12 D'AIR NE SUFFISAIENT PAS : vu à l'écran, la dalle venait TOUCHER le bord du
     plateau et paraissait rognée par lui — le défaut que ce correctif devait supprimer,
     revenu par la petite porte parce que le trait avait descendu de 24 et que la matière
     avait grandi d'autant. 24, c'est le pas d'air du produit (le padding du plateau est
     26) : la dalle se détache, et il lui reste 238 px de zone au lieu de 226. */
  var _haut = Math.round(124 * _ech * (H / _hcss));
  /* garde-fou : si le canevas est court (une Nuée défilée, un état comprimé), on ne
     mange pas plus de la moitié de la zone — mieux vaut une dalle centrée qu'une dalle
     écrasée. */
  if(!(_haut > 0) || _haut > H * 0.5) _haut = 0;
  var _zone = H - _haut;
  /* ⚑ v29 — rendue par le moteur dans la boîte (0,86·W × 0,86·zone, au facteur d'arrivée k), jamais agrandie */
  var src = window._rendDalle ? window._rendDalle(cle.id, W*0.86*k*dpr, _zone*0.86*k*dpr) : null;
  if(!src || !src.width) return;
  src = _teinteBande(src);
  var L = src.width/dpr, dh = src.height/dpr;
  /* on ne repeint que si la fiche est visible */
  if(e < 1 && dp.classList.contains('show')) requestAnimationFrame(function(){
    if(window._ficheDalle) _ficheDalle(); });
  g.globalAlpha = 1;
  g.imageSmoothingEnabled = true;
  g.imageSmoothingQuality = 'high';
  /* ⚠ L'APP PUBLIE CE QU'ELLE VIENT DE COMPOSER (§7). Compter les pixels d'un canevas
     pour retrouver la dalle mesure aussi le trait et le fond : la sonde rendait « 0 → 291 »
     alors que la matière était ailleurs. On expose la boîte, en cotes d'écran. */
  var _yDalle = Math.round(_haut + (_zone-dh)/2);
  try{ var _cot = _hcss / (H||1) / (_ech||1);
    window._dalleFiche = {haut:+( _haut*_cot ).toFixed(1), y:+( _yDalle*_cot ).toFixed(1),
      h:+( dh*_cot ).toFixed(1), bas:+(( _yDalle+dh )*_cot).toFixed(1),
      zone:+( _zone*_cot ).toFixed(1)}; }catch(_){}
  window._poseUn(g, src, W/2, _yDalle + dh/2);
  g.globalAlpha = 1;
}catch(e){} };
/* le disque d'une personne renvoie vers sa page dans l'Aura : c'est le
   meme objet, il doit mener au meme endroit. */
document.addEventListener('click', function(e){
  var k = e.target.closest && e.target.closest('#dAura .kring');
  if(!k) return;
  var qui = k.getAttribute('data-p');
  if(!qui) return;
  try{
    document.getElementById('detailPoster').classList.remove('show');
    setTimeout(function(){
      if(window.ouvrirPersonne) ouvrirPersonne(qui);
      else if(window.openPerson) openPerson(qui);
      else {
        var s = document.getElementById('personSheet');
        if(s){ if(window.renderPerson) renderPerson(qui); s.classList.add('show'); }
      }
    }, 240);
  }catch(_){}
  e.stopPropagation();
}, true);
/* aucun score dans une Nuee : l'harmonie se voit, elle ne se note pas. */
window._nettoieNuee = function(){ try{
  var dp = document.getElementById('detailPoster');
  if(!dp) return;
  dp.querySelectorAll('*').forEach(function(e){
    if(e.children.length) return;
    var t = (e.textContent||'').trim();
    if(/^\d+\s*Promis?\s*[·.]\s*\d+%/.test(t) || /r\u00e9ciprocit\u00e9 visible/i.test(t))
      e.style.display = 'none';
  });
}catch(e){} };
/* une fiche de Nuee n'ouvre pas par renderDetail() : on observe l'apparition
   de « show » sur la fiche pour poser la mise en page quel que soit le chemin. */
try{ document.addEventListener('DOMContentLoaded', function(){
  var dp = document.getElementById('detailPoster'); if(!dp) return;
  /* GARDE-FOU : _fichePose ajoute des classes, ce qui reveille l'observateur,
     qui rappelle _fichePose... On ne repond qu'a l'OUVERTURE, une seule fois. */
  var ouvert = false;
  new MutationObserver(function(){
    var v = dp.classList.contains('show');
    if(v === ouvert) return;
    ouvert = v;
    if(!v) return;
    requestAnimationFrame(function(){
      try{ if(window._fichePose) _fichePose(); }catch(_){}
      try{ if(window._ficheDalle) _ficheDalle(); }catch(_){}
    });
  }).observe(dp, {attributes:true, attributeFilter:['class']});
}); }catch(e){}
/* PEAUFINER S'OUVRE AU CLIC *ET* AU SCROLL.
   Des qu'on approche du bas, le tiroir se deplie tout seul : le scroll
   n'est jamais bloque, on decouvre les reglages en descendant. */
(function(){ try{
  var poser = function(){
    var dp = document.getElementById('detailPoster');
    if(!dp || dp._scrollPose) return;
    dp._scrollPose = true;
    var ouvrir = function(){
      var d = document.getElementById('dpDetails');
      if(d && !d.classList.contains('ouvert')) d.classList.add('ouvert');
    };
    /* au scroll quand il y a de quoi scroller */
    dp.addEventListener('scroll', function(){
      var reste = dp.scrollHeight - dp.scrollTop - dp.clientHeight;
      if(reste < 60) ouvrir();
    }, {passive:true});
    /* et au simple geste vers le bas quand la fiche tient dans l'ecran :
       sans ca l'evenement « scroll » ne part jamais et rien ne s'ouvre. */
    var y0 = null;
    dp.addEventListener('touchstart', function(e){
      y0 = e.touches ? e.touches[0].clientY : null; }, {passive:true});
    dp.addEventListener('touchmove', function(e){
      if(y0 === null) return;
      var y = e.touches ? e.touches[0].clientY : y0;
      if(y0 - y > 26) ouvrir();
    }, {passive:true});
    dp.addEventListener('wheel', function(e){
      if(e.deltaY > 8) ouvrir(); }, {passive:true});
  };
  poser();
  document.addEventListener('DOMContentLoaded', poser);
  setTimeout(poser, 1500);
}catch(e){} })();
/* ── « TOUT LE MONDE » DANS UNE NUEE ──
   On ne se promet pas a soi dans un groupe : quand un Promi est cree depuis
   une Nuee, le premier choix est le groupe entier, pas « moi ». */
/* ── L'ORDRE DES DESTINATAIRES ──
     un Promi          Moi · puis les autres
     un Promi en Nuée  tout le monde · Moi · puis les autres
   On ne se promet pas d'abord à soi dans un groupe, mais on doit pouvoir. */
window._rangQui = function(){ try{
  var box = document.getElementById('whoChips');
  if(!box) return;
  var cs = document.getElementById('createSheet');
  var dansNuee = false;
  try{ dansNuee = !!(cs && cs.classList.contains('cs-nuee')) || !!window._createNuee; }catch(_){}

  var gens = [];
  try{
    gens = [...new Set(promises.map(function(p){ return p.who; })
      .filter(function(w){ return w && w !== 'moi' && w !== 'le groupe'; }))].slice(0, 5);
  }catch(_){}

  var tete = dansNuee ? ['tout le monde', 'Moi'] : ['Moi'];
  var liste = tete.concat(gens.filter(function(g){ return tete.indexOf(g) < 0; }));

  box.innerHTML = liste.map(function(n, i){
    var actif = (i === 0);
    var av = (n === 'Moi')
      ? '<span class="wc-av"></span>' : '';
    return '<button type="button" class="wc' + (actif ? ' on' : '')
      + (n === 'tout le monde' ? ' wc-tous' : '') + '" data-who="' + n + '">'
      + av + n + '</button>';
  }).join('');
  try{ var f0 = document.getElementById('fWho'); if(f0) f0.value = liste[0] || ''; }catch(_){}
  box.querySelectorAll('.wc').forEach(function(b){
    b.onclick = function(){
      box.querySelectorAll('.wc').forEach(function(x){ x.classList.toggle('on', x === b); });
      try{ var f1 = document.getElementById('fWho'); if(f1) f1.value = b.dataset.who; }catch(_){}
    };
  });
}catch(e){} };
(function(){ try{
  var poser = function(){
    try{ if(window._rangQui) _rangQui(); }catch(_){}
    try{ if(window._echeanceDefaut) _echeanceDefaut(); }catch(_){}
    var f = document.getElementById('fWho');
    var rang = f && f.closest ? f.closest('div') : null;
    if(!rang) return;
    var host = rang.parentNode;
    if(!host || host.querySelector('.cs-tous')) return;
    var cs = document.getElementById('createSheet');
    if(!cs || !cs.classList.contains('show')) return;
    /* la pastille n'existe que si l'on cree DANS une Nuee */
    var dansNuee = false;
    try{ dansNuee = !!(window._createNuee || (typeof curNuee !== 'undefined' && curNuee
      && cs.classList.contains('cs-nuee'))); }catch(_){}
    if(!dansNuee) return;
    var b = document.createElement('button');
    b.className = 'cs-tous on';
    b.type = 'button';
    b.textContent = 'tout le monde';
    b.onclick = function(){
      b.classList.toggle('on');
      try{ if(f) f.value = b.classList.contains('on') ? 'tout le monde' : ''; }catch(_){}
    };
    host.insertBefore(b, rang);
    try{ if(f) f.value = 'tout le monde'; }catch(_){}
  };
  document.addEventListener('click', function(){ setTimeout(poser, 120); }, true);
  setTimeout(poser, 2000);
}catch(e){} })();
/* ── « AVANT · UN JOUR » ──
   « avant un jour » n'est pas du français. Un point median sépare le mot
   du placeholder ; dès qu'une vraie échéance est choisie, il disparaît et
   la phrase redevient correcte : « avant vendredi ». */
/* on ajoute « un jour » en tete des echeances : c'est le defaut, et il
   porte le point median tant qu'il est actif. */
window._echeanceDefaut = function(){ try{
  document.querySelectorAll('#createSheet .chips,#createSheet [class*=chips]').forEach(function(box){
    var ch = box.querySelectorAll('.chip');
    if(!ch.length) return;
    var t0 = (ch[0].textContent || '').trim();
    if(!/^(2 j|5 j)$/.test(t0)) return;          /* c'est bien le rang des delais */
    if(box.querySelector('[data-q="jour"]')) return;
    var b = document.createElement('div');
    b.className = 'chip on q-jour';
    b.setAttribute('data-q','jour');
    b.textContent = 'un jour';
    box.insertBefore(b, ch[0]);
    ch.forEach(function(x){ x.classList.remove('on'); });
    box.querySelectorAll('.chip').forEach(function(x){
      x.addEventListener('click', function(){
        box.querySelectorAll('.chip').forEach(function(y){ y.classList.toggle('on', y === x); });
        try{ if(window._sepEcheance) _sepEcheance(); }catch(_){}
      });
    });
  });
  try{ if(window._sepEcheance) _sepEcheance(); }catch(_){}
}catch(e){} };
window._sepEcheance = function(){ try{
  /* le point median ne vit que sur « un jour » actif */
  document.querySelectorAll('#createSheet .chips').forEach(function(box){
    var j = box.querySelector('[data-q="jour"]');
    if(j) j.classList.toggle('q-flou', j.classList.contains('on'));
  });
}catch(e){} };
/* ── LA DALLE DE LA PAGE + DEVIENT LA TRAME DES REGLAGES ──
   Meme rendu, meme cadrage : la dalle du monde actif, posee en haut,
   nette et a ses vraies couleurs. */
window._trameReglagesDalle = function(){ try{
  var host = document.getElementById('settingsScreen');
  if(!host || !host.classList.contains('show')) return;
  var cv = document.getElementById('stTrameCv');
  if(!cv){
    cv = document.createElement('canvas');
    cv.id = 'stTrameCv';
    host.insertBefore(cv, host.firstChild);
  }
  var W = host.clientWidth || 390, H = 300;
  var dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
  cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr);
  cv.style.width = W+'px'; cv.style.height = H+'px';
  var g = cv.getContext('2d'); if(!g) return;
  g.setTransform(dpr,0,0,dpr,0,0);
  g.clearRect(0,0,W,H);
  g.imageSmoothingQuality = 'high';
  cv.style.setProperty('opacity','1','important');
  cv.style.setProperty('filter','none','important');
  try{
    var p0 = promises.filter(function(q){ return !q.draft; })[0];
    if(!p0) return;
    /* ⚑ v29 — rendue par le moteur à sa largeur finale (0,78 W), posée 1:1 (redteam_decoupe) */
    var src = window._rendDalle ? window._rendDalle(p0.id, W*0.78*dpr, 1e5) : null;
    if(!src) return;
    /* le meme cadrage que la page + : la dalle occupe la droite du bandeau,
       assez grande pour se lire, jamais tronquee en haut. */
    /* le meme cadrage que la page + : grande, a droite, debordant du bandeau */
    var L = src.width/dpr, dh = src.height/dpr;
    g.globalAlpha = 0.42;
    window._poseUn(g, src, W*0.46 + L/2, H*0.10 + dh/2);
    g.globalAlpha = 1;
  }catch(_){}
}catch(e){} };
(function(){ try{
  var st = null;
  var poser = function(){
    st = st || document.getElementById('settingsScreen');
    if(!st || st._trPose) return;
    st._trPose = true;
    new MutationObserver(function(){
      if(st.classList.contains('show'))
        requestAnimationFrame(function(){ try{ _trameReglagesDalle(); }catch(_){} });
    }).observe(st, {attributes:true, attributeFilter:['class']});
  };
  poser();
  document.addEventListener('DOMContentLoaded', poser);
  setTimeout(poser, 1800);
}catch(e){} })();
/* ══════════════════════════════════════════════════════════
   LA PAGE + — UNE PHRASE, PAS UN FORMULAIRE
   « Je promets ✦ / a Rachel / de rendre le livre / avant · un jour »
   Chaque mot en pastille ouvre ses choix en dessous. Le formulaire
   d'origine reste dans le DOM, masque : la phrase l'alimente.
   ══════════════════════════════════════════════════════════ */
window._phrase = { sens:'faire', qui:'Moi', titre:'', quand:'un jour' };

window._phraseRendu = function(){ try{
  var f = document.getElementById('promiForm');
  if(!f) return;
  var box = document.getElementById('csPhrase');
  if(!box){
    box = document.createElement('div');
    box.id = 'csPhrase';
    f.insertBefore(box, f.firstChild);
  }
  var P = window._phrase;
  /* LA VIRGULE APPARTIENT À LA PASTILLE (décision Tom) : « [Marion,] » est UN SEUL objet
     touchable, pas une pastille suivie d'un signe. Le visage (§2.10) entre dans la même
     pastille, à 0,76 × la taille du texte, padding gauche ramené à 9 (§2.8). */
  var pl = function(cle, txt, vide, opt){
    opt = opt || {};
    var vis = '';
    if(opt.visage && !vide){
      try{ vis = window._visageSvg ? _visageSvg(Math.round(opt.taille*0.76), opt.natCol) : ''; }catch(_){ }
    }
    return '<span class="ph-m' + (vide ? ' ph-vide' : '') + (vis ? ' ph-avec-visage' : '')
      + '" data-ph="' + cle + '">' + vis + txt + (opt.virgule && !vide ? ',' : '') + '</span>';
  };
  /* LA CASSE — française ordinaire : majuscule au PREMIER MOT DE LA PHRASE, bas de casse
     partout ailleurs (décision Tom). Le verbe n'ouvre donc la phrase que si rien de REMPLI
     ne le précède : « Je me promets d'… » garde sa majuscule, « à Marion, chiche de… » la
     perd. C'est aussi ce que montrent les deux cadres du Chiche : « Chiche » quand la ligne
     du dessus est un placeholder vide, « chiche » quand elle porte un prénom. */
  var basCasse = function(mot){ return mot.charAt(0).toLowerCase() + mot.slice(1); };
  /* L'ÉLISION (§2.8 et §4) : « de » devient « d' » devant voyelle ou h muet, COLLÉ au mot —
     l'écart de 11 px tombe à 3. Le moodboard écrit « d' aller voir la mer », l'app écrivait
     « de aller voir la mer » (constaté au duo). La règle est au document, pas inventée. */
  /* ⚑ v20 (Tom, 22 sept.) — LA RÈGLE COMPLÈTE : premier mot normalisé (minuscules, accents
     retirés) ; « d’ » devant voyelle, h muet, « y » et « en » pronoms ; « de » devant un h
     aspiré (liste), un y consonne, onze, onzième, oui, un chiffre. PASTILLE VIDE : « de ».
     Un seul propriétaire dans l'app : window._promiElide (lot-ONB-V20), partagé avec
     l'onboarding. Promi et Chiche seulement — la Nuée n'a pas de « de ». */
  var elide = function(mot){
    var m = (''+(mot||'')).trim();
    if(!m) return {li:'de', cls:''};
    var d = window._promiElide ? window._promiElide(m) : 'de';
    return d === 'd\u2019' ? {li:'d\u2019', cls:' ph-elide'} : {li:'de', cls:''};
  };
  /* contexte : Nuée, destinataire, singulier/pluriel, à-soi */
  var enNuee = false, nueeNom = '';
  try{ if(typeof selNuee !== 'undefined' && selNuee){ enNuee = true; nueeNom = (typeof NUE !== 'undefined' && NUE[selNuee]) || selNuee; } }catch(_){}
  var quiAff = P.qui || 'Moi';
  var nueeAff = enNuee ? nueeNom : 'aucun Cercle';
  var estMoi = (quiAff === 'Moi' || quiAff === 'moi');
  /* LE PLURIEL EST AUSSI CELUI DE PLUSIEURS PRÉNOMS. Le cadre « Promi · promettez-moi »
     écrit « Rachel, Nico, » puis « promettez-moi » : deux destinataires suffisent, il n'y
     a pas besoin d'une Nuée. L'app n'y voyait que « tout le monde » et écrivait
     « promets-moi » au-dessus de deux prénoms — une faute de français, constatée au duo. */
  var estPluriel = enNuee || /tout le monde|le groupe/i.test(quiAff)
                || /[,·]|\bet\b/.test(''+quiAff);
  /* « faire » a DEUX positions dans le cycle : à SOI (« Je me promets », défaut) et à
     QUELQU'UN (« Je promets … à … »). P.faireAutre les distingue (posé par le toggle). */
  var faireSoi = (P.sens === 'faire' && !P.faireAutre && estMoi);
  /* LES TROIS FAÇONS DE S'ENGAGER — le verbe porte le sens, évident à la lecture :
     faire→« Je promets » (moi→l'autre) · à soi→« Je me promets » · demander→
     « promets-moi » / « promettez-moi » au pluriel (l'autre→moi) · chiche→« Chiche »
     (un défi lancé, l'autre peut le relever ; liaison « avec »). */
  var verbe = P.sens === 'chiche' ? 'Chiche'
            : P.sens === 'demander' ? (estPluriel ? 'promettez-moi' : 'promets-moi')
            : (faireSoi ? 'Je me promets' : 'Je promets');
  /* le ⇄ n'apparaît QUE sur le Promi (faire↔demander) ; le Chiche est une nature figée. */
  var _bascSvg = (P.sens === 'chiche') ? '' : ('<svg viewBox="0 0 22 22" width="17" height="17">'
    + '<path d="M3 8h16" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>'
    + '<path d="M15.4 4.6 L19 8 L15.4 11.4" fill="none" stroke="currentColor" '
    + 'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    + '<path d="M19 15H3" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>'
    + '<path d="M6.6 11.6 L3 15 L6.6 18.4" fill="none" stroke="currentColor" '
    + 'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>');
  var _natCol = (P.sens==='chiche') ? '#FFB8D2' : '#82AEF8';
  var _tailleV = 33;   /* le visage suit la taille de la phrase ; 0,76 × est appliqué dans pl() */
  /* le verbe passe en bas de casse dès qu'un élément REMPLI le précède (voir basCasse). */
  var _ouvre = !(P.sens==='chiche' && P.qui && !estMoi && (''+P.qui).trim())
            && !(P.sens==='demander');
  var _verbeAff = _ouvre ? verbe : basCasse(verbe);
  var basc = '<span class="ph-b'+(P.sens==='chiche'?' ph-b-fixe':'')+'" data-ph="sens">' + _verbeAff + _bascSvg + '</span>';
  var etoile = '<i class="ph-e">✦</i>';
  /* « dans une Nuée » a QUITTÉ la phrase (trop de choix à remplir) : il descend en haut
     de Peaufiner (#promiExtra). Rien dans la phrase, même quand on vient d'une Nuée
     (déjà connue, pré-sélectionnée).
     ⇒ L'ÉCHÉANCE SUIT LE MÊME CHEMIN (décision Tom, S3/Q28). Le moodboard le dit dans sa
     ligne d'aide — « l'échéance, la Nuée et le reste sont dans Peaufiner » — et c'est le
     même argument : trois choix à remplir, c'est déjà beaucoup. La liste unique
     (un jour · en l'air · demain · 5 jours · 2 semaines · ce mois-ci · une date précise…)
     a besoin de la place de Peaufiner, elle ne tient pas en pastilles.
     La phrase ne garde donc que VERBE et OBJET — deux lignes, base = 312 (§2.5). */
  var lignesFin = '';
  var h;
  /* ⚑ LES EXEMPLES DES CRÉNEAUX (Tom, 13 sept. 2026) — concrets, un peu tendres, jamais ambitieux. « aller voir la mer »
     reste celui de « Je promets à … » ; les deux autres formes en ont trois, qui tournent d'une page + à la suivante. */
  /* ⚑ v20 (Tom, 22 sept.) — LES EXEMPLES QUI TOURNENT : à la toute première ouverture d'un
     type, le PREMIER de la liste ; dès la deuxième, un tirage. Un compteur par type (Promi à
     soi, « promets-moi », Chiche, Nuée) ; le Promi à quelqu'un garde « aller voir la mer ».
     L'exemple est tiré UNE FOIS par ouverture de la page + (window._ppExemple). */
  /* on ne tire QUE l'exemple du type affiché : sinon chaque rendu entame les trois compteurs */
  var _exSoi = (window._ppExemple && P.sens!=='demander' && P.sens!=='chiche' && faireSoi) ? window._ppExemple('soi') : 'reprendre la guitare';
  var _exDem = (window._ppExemple && P.sens==='demander') ? window._ppExemple('demander') : 'venir dimanche';
  /* ⚑ 17 sept. : le Chiche en a trois lui aussi. « lâcher ton téléphone un soir » mesure
     312,7 px dans une pastille de 342 — il tient, mesuré à 28 px Gilbert. */
  var _exChi = (window._ppExemple && P.sens==='chiche') ? window._ppExemple('chiche') : 'dire oui pour une fois';
  var _exFaire = faireSoi ? _exSoi : 'aller voir la mer';
  window._ppExempleCourant = (P.sens === 'demander') ? _exDem : (P.sens === 'chiche' ? _exChi : _exFaire);
  /* 3.8 · l'INVITE du champ n'est pas l'exemple de la pastille : sur un Chiche elle joue sur
     ce qu'on n'ose pas. 321,3 px mesurés dans un champ de 342 (Gilbert 22), 20,7 de marge. */
  window._ppInviteCourante = (P.sens === 'chiche')
    ? 'ce que tu n\u2019as jamais os\u00e9 lui lancer\u2026' : window._ppExempleCourant;
  if(P.sens === 'demander'){
    /* le PRÉNOM ouvre : « Rachel, promets-moi de … » */
    h = pl('qui', estMoi ? 'Rachel' : quiAff, estMoi,
           {virgule:true, visage:true, taille:_tailleV, natCol:_natCol}) + '<br>'
      + basc + ' ' + etoile + '<br>'
      + (function(){var _e=elide(P.titre);return '<em class="ph-li'+_e.cls+'">'+_e.li+'</em> ' + pl('titre', P.titre || _exDem, !P.titre);})() + '<br>'
      + lignesFin;
  } else if(P.sens === 'chiche'){
    /* Chiche a DEUX créneaux distincts, tous deux facultatifs (choosers séparés, jamais
       fusionnés) : QUI JE DÉFIE (le prénom qui ouvre, réutilise le créneau « qui ») et
       AVEC QUI (la liaison « avec », champ P.avec). Un créneau vide ne s'affiche pas —
       la phrase reste courte. Des puces discrètes permettent d'ajouter un créneau absent. */
    var _defie = (P.qui && !estMoi && (''+P.qui).trim());
    var _avec  = (P.avec && (''+P.avec).trim());
    h = '';
    /* LE CRÉNEAU « QUI JE DÉFIE » ouvre la phrase, et il se montre MÊME VIDE : le cadre
       « Chiche · vide » écrit « à qui ? » en pastille pointillée. La liaison « à » est
       celle du moodboard — « à Marion, chiche de courir dimanche » (décision Tom, S3/Q29). */
    h += '<em>à</em> ' + pl('qui', _defie ? P.qui : 'qui ose ?', !_defie,
           {virgule:true, visage:true, taille:_tailleV, natCol:_natCol}) + '<br>';
    h += basc + ' ' + etoile + '<br>'
      + (function(){var _e=elide(P.titre);return '<em class="ph-li'+_e.cls+'">'+_e.li+'</em> ' + pl('titre', P.titre || _exChi, !P.titre);})() + '<br>';
    /* LE CRÉNEAU « AVEC » est le SECOND, celui du compagnon : deux créneaux distincts,
       jamais confondus. VIDE, IL NE MONTRE RIEN — ni le mot, ni la pastille, ni le « + ».
       C'est pour ça qu'aucun des 17 cadres ne le porte. On l'ajoute par Peaufiner, où le
       réglage AVEC existe (section 2). */
    /* ⚠ LE SECOND CRÉNEAU D'UN CHICHE EST LE COMPAGNON, ET IL S'AFFICHE TOUJOURS
       (décision Tom). Vide, il prend le contour pointillé de la pastille vide (§2.8). */
    h += '<em>avec</em> ' + pl('avec', _avec ? P.avec : 'qui en est ?', !_avec) + '<br>';
    h += lignesFin;
  } else {
    /* faire : à SOI → « Je me promets » (pas de ligne « à ») ; à QUELQU'UN → ligne
       « à … » (vide « quelqu'un », touchable, tant que non choisi). */
    h = basc + ' ' + etoile + '<br>'
      /* ⚑ L'EXEMPLE DE LA PHRASE EST CELUI DE LA PLANCHE : « aller voir la mer ».
         Les cadres 2, 4, 18, 24 à 33 l'écrivent tous ainsi — c'est LA phrase de
         démonstration de la page +, et elle n'est justement PAS un Promi planté
         (cadre 74 : l'Index en porte huit, elle n'y est pas). L'app proposait
         « rendre le livre… », un titre de son ancien jeu. */
      + (function(){var _e=elide(P.titre);return '<em class="ph-li'+_e.cls+'">'+_e.li+'</em> ' + pl('titre', P.titre || _exFaire, !P.titre);})() + '<br>';
    if(!faireSoi){ var _perso = (P.qui && !estMoi);
      /* LE MOT DU CADRE (§5, décision Tom) : la pastille vide du destinataire s'écrit
         « qui ? », comme celle du Chiche — l'app écrivait « quelqu'un ». */
      h += '<em>à</em> ' + pl('qui', _perso ? P.qui : 'qui ?', !_perso,
             {visage:true, taille:_tailleV, natCol:_natCol}) + '<br>'; }
    h += lignesFin;
  }
  /* le <br> ORPHELIN. Les trois branches finissaient par « … + '<br>' + lignesFin » ;
     lignesFin étant désormais vide (l'échéance est dans Peaufiner), il restait un saut de
     ligne en trop. La phrase comptait donc 3 lignes au lieu de 2 et le trait retombait à
     base = 280 au lieu de 312 — l'onde passait 32 px trop haut (constaté au duo). */
  h = h.replace(/(<br>\s*)+$/,'');
  var hintHtml = (P.sens === 'chiche')
    ? 'un Chiche se lance, il ne se retourne pas'
    : '<b>' + verbe + '</b> se retourne — touche-le';
  box.innerHTML = '<div class="ph-txt">' + h + '</div>'
    + '<div class="ph-hint">' + hintHtml + '</div>'
    + '<div class="ph-choix" id="csChoix"></div>';

  box.querySelectorAll('[data-ph]').forEach(function(el){
    el.onclick = function(){
      var k = el.getAttribute('data-ph');
      if(k === 'sens'){
        /* Chiche est une NATURE (sa tuile) — sa bascule ⇄ ne change rien. Pour le Promi,
           la bascule cycle 3 positions : « Je me promets » → « Je promets à … » →
           « promets-moi » → … (le défié/compagnon du Chiche n'y sont plus). */
        if(P.sens==='chiche') return;
        if(P.sens==='faire' && !P.faireAutre){ P.faireAutre=true; if(P.qui==='Moi'||P.qui==='moi') P.qui=''; }
        else if(P.sens==='faire' && P.faireAutre){ P.sens='demander'; P.faireAutre=false; }
        else { P.sens='faire'; P.faireAutre=false; P.qui='Moi'; }
        /* le plant lit window._csSens (via csSens()) ; on le synchronise DIRECTEMENT
           — pas de bouton #csSens pour « chiche ». On met à jour l'état + les libellés. */
        try{ window._csSens = P.sens;
          document.querySelectorAll('#csSens [data-sens]').forEach(function(x){x.classList.toggle('on', x.getAttribute('data-sens')===P.sens);});
          if(typeof window.majSens==='function') window.majSens();
        }catch(_){}
        _phraseRendu();
        return;
      }
      _phraseChoix(k, el);
    };
  });
}catch(e){} };

/* les choix s'ouvrent SOUS la phrase, jamais dans un autre ecran */
/* format d'une échéance datée, partagé par la phrase (page +) et la fiche :
   dans les 30 jours → « mardi 12 » ; au-delà → « mardi 12 mai ». JAMAIS d'année
   (« mardi 12 » seul est ambigu au-delà du mois courant). */
window._dateQuand = function(d, days){
  var JQ=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
  var MO=['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];
  var base = JQ[d.getDay()] + ' ' + d.getDate();
  if(days==null){ try{ var t=new Date(); t.setHours(0,0,0,0); days=Math.round((d - t)/86400000); }catch(_){ days=0; } }
  return days>30 ? (base + ' ' + MO[d.getMonth()]) : base;
};
window._phraseChoix = function(cle, el){ try{
  var zone = document.getElementById('csChoix');
  if(!zone) return;
  document.querySelectorAll('#csPhrase .ph-m').forEach(function(x){
    x.classList.toggle('ph-on', x === el); });
  var P = window._phrase;
  var titre = { qui:'\u00c0 QUI', titre:'TU PROMETS QUOI', quand:'AVANT QUAND', nuee:'DANS QUEL CERCLE', avec:'QUI EN EST' }[cle] || '';
  if(cle === 'qui' && P.sens === 'chiche') titre = 'QUI TU D\u00c9FIES';
  var h = '<div class="ph-lab">' + titre + '</div>';

  if(cle === 'nuee'){
    /* #5 : les Nu\u00e9es comme OBJETS (pas des mots) \u2014 dalle mauve + nom en gros + qui est
       dedans. \u00ab aucune \u00bb en premier (pour en sortir). Chooser S\u00c9PAR\u00c9 du \u00ab \u00e0 qui \u00bb. */
    var _mauve = '<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><path d="M20 2 L34 8 L38.4 22.4 L30.4 38.4 L11.2 38.8 L2.4 24.8 L5.6 9.2 Z" fill="#C9A8F5"/><circle cx="16.5" cy="18" r="6" fill="rgba(41,21,71,.52)"/><circle cx="25" cy="14.5" r="4" fill="rgba(41,21,71,.34)"/><circle cx="24" cy="26" r="4.2" fill="rgba(41,21,71,.34)"/></svg>';
    var _selN = (typeof selNuee !== 'undefined' && selNuee) ? selNuee : '';
    var _keys = []; try{ _keys = Object.keys(NUE); }catch(_){}
    var cards = '<button type="button" class="ph-nuee-o pno-aucune'+(_selN?'':' on')+'" data-nuee=""><span class="pno-none">aucun Cercle</span></button>';
    _keys.forEach(function(k){
      var nom = (typeof NUE!=='undefined' && NUE[k]) || k;
      var mem = []; try{ mem = (typeof NUEEMEM!=='undefined' && NUEEMEM[k]) || []; }catch(_){}
      var memTxt = mem.length ? (mem.slice(0,3).join(', ') + (mem.length>3 ? '  +'+(mem.length-3) : '')) : 'personne encore';
      cards += '<button type="button" class="ph-nuee-o'+(_selN===k?' on':'')+'" data-nuee="'+k+'">'
        + '<span class="pno-dalle">'+_mauve+'</span>'
        + '<span class="pno-tx"><span class="pno-nom">'+_esc(nom)+'</span>'
        + '<span class="pno-mem">'+_esc(memTxt)+'</span></span></button>';
    });
    h += '<div class="ph-nuee-opts">' + cards + '</div>';
  } else if(cle === 'titre'){
    h += '<input class="ph-in" id="phIn" placeholder="' + (window._ppInviteCourante || window._ppExempleCourant || 'aller voir la mer') + '" value="'
      + (P.titre || '') + '">';
  } else {
    var opts;
    if(cle === 'qui' || cle === 'avec'){
      var gens = [];
      try{
        /* les DERNIÈRES personnes ajoutées passent en premier (promises.reverse) */
        gens = [...new Set(promises.slice().reverse().map(function(p){ return p.who; })
          .filter(function(w){ return w && w !== 'moi' && w !== 'le groupe'; }))].slice(0, 5);
      }catch(_){}
      if(cle === 'avec'){
        /* « avec qui » : une personne qui relève le défi avec moi — pas « Moi ». */
        opts = gens.slice();
      } else {
        var dansNuee = false;
        try{ dansNuee = !!document.querySelector('#createSheet.cs-nuee'); }catch(_){}
        /* moodboard : dans une Nuée, « tout le monde » en tête et « Moi » en dernier. */
        opts = dansNuee
          ? ['tout le monde'].concat(gens.filter(function(g){ return g !== 'Moi'; })).concat(['Moi'])
          : ['Moi'].concat(gens.filter(function(g){ return g !== 'Moi'; }));
      }
    } else {
      /* TROIS formes d'échéance, pas deux : « un jour » (une promesse, sans date fixe) ·
         « en l'air » (une envie, plus légère qu'une promesse, SANS échéance) · une date
         précise. « un jour » reste le placeholder gris par défaut ET une option. */
      opts = ['un jour', 'en l’air', 'demain', '5 jours', '2 semaines', 'ce mois-ci'];
    }
    h += '<div class="ph-opts">' + opts.map(function(o){
      return '<button type="button" class="ph-o' + (P[cle] === o ? ' on' : '')
        + '" data-v="' + o + '">' + o + '</button>';
    }).join('')
    /* « à qui » / « avec » : une pastille + pour ajouter un nom (même gabarit, sobre) */
    + ((cle === 'qui' || cle === 'avec') ? '<button type="button" class="ph-o ph-add" data-add="1" aria-label="ajouter une personne">+</button>' : '')
    /* « quand » : une DATE PRÉCISE — le sélecteur natif s'ouvre d'un geste (« avant mardi 12 »). */
    + (cle === 'quand' ? '<button type="button" class="ph-o ph-date" data-datepick="1">une date précise…</button>' : '')
    + '</div>'
    + (cle === 'quand' ? '<input type="date" id="phDateIn" class="ph-datein" aria-label="Choisir une date" style="position:absolute;left:16px;bottom:14px;opacity:0;width:120px;height:34px;border:0;pointer-events:none">' : '');
  }
  zone.innerHTML = h;
  zone.classList.add('ouvert');
  /* #5 : choisir une Nuée d'un geste — met à jour selNuee (SANS toucher « à qui ») +
     synchronise le champ Nuée d'origine pour que le plantage garde la Nuée. */
  zone.querySelectorAll('.ph-nuee-o').forEach(function(b){
    b.onclick = function(){
      var key = b.dataset.nuee || '';
      try{ selNuee = key || null; }catch(_){}
      try{ var _cs=document.getElementById('createSheet'); if(_cs) _cs.classList.toggle('cs-nuee', !!key); }catch(_){}
      try{ document.querySelectorAll('#nueeChips .chip').forEach(function(c){ c.classList.toggle('on', (c.dataset.nuee||'')===key); }); }catch(_){}
      try{ if(typeof buildWhoChips==='function') buildWhoChips(); }catch(_){}
      zone.classList.remove('ouvert');
      _phraseRendu();
    };
  });
  /* la zone du haut passe à 150 → repeindre la grappe à la nouvelle hauteur. */
  try{ if(window._peintGrappe){ setTimeout(window._peintGrappe,60); setTimeout(window._peintGrappe,240); } }catch(_){}
  /* bug (a) sur l'écran « à qui » : le cs-top rétrécit (210→150) à l'ouverture du
     chooser, donc le viewport de remplissage grandit. On RECALCULE le minHeight du
     formulaire (sans re-scroller) pour que le panneau reste ancré juste au-dessus de
     la barre, comme au moodboard — sinon il flotte ~24-36 px trop haut. */
  try{
    var _csA=document.getElementById('createSheet');
    var _kA=_csA&&_csA.getAttribute('data-kind');
    var _fA=document.getElementById(_kA==='promi'?'promiForm':(_kA==='nuee'?'nueeForm':'draftForm'));
    var _midA=document.getElementById('csMid')||(_csA&&_csA.querySelector('.cs-mid'));
    if(_fA&&_midA){ var _recal=function(){
      /* on remplit EXACTEMENT le viewport défilant (csMid.clientHeight) : ainsi le
         défilement épinglé atteint le haut du formulaire → la phrase se cale sous le
         cs-top. Le gap du panneau (12px×1,108) vient du padding-bottom de promiForm,
         pas d'un offset ici (sinon phrase et panneau se disputent l'espace). */
      var _vp=_midA.clientHeight; if(_vp>0) _fA.style.minHeight=_vp+'px';
      /* on ÉPINGLE le défilement : promiForm en tête du viewport → la phrase se cale
         juste sous le cs-top (150+22), comme au moodboard (sinon elle flotte ~35 px
         plus bas selon d'où l'on vient). */
      try{ _midA.scrollTop=_fA.offsetTop; }catch(_e){} };
      requestAnimationFrame(_recal); setTimeout(_recal,140); setTimeout(_recal,320); }
  }catch(_){}

  var inp = document.getElementById('phIn');
  if(inp){
    inp.focus();
    inp.oninput = function(){
      P.titre = inp.value;
      try{ var t = document.getElementById('fTitle'); if(t){ t.value = inp.value;
        t.dispatchEvent(new Event('input', {bubbles:true})); } }catch(_){}
      /* ⚠ LA PHRASE SUIT LE DOIGT (CASSE A1). On ne rejoue PAS `_phraseRendu()` ici : il
         reconstruit #csPhrase, donc il détruirait le champ qui reçoit la frappe. On met à
         jour LE SEUL créneau touché, puis on redonne ses cotes à l'écran (§2.8). */
      try{
        var m = document.querySelector('#csPhrase [data-ph=titre]');
        if(m){
          var v = (inp.value||'').trim();
          m.classList.toggle('ph-vide', !v);
          var cible = m.querySelector('.ph-mot') || m;
          cible.textContent = v || (inp.getAttribute('placeholder')||'');
          /* ⚑ v46 (Tom) — L'ÉLISION SUIT LA FRAPPE, à chaque caractère : « de » / « d’ » est l'élément qui précède la
             pastille (.ph-li) ; il n'était recalculé qu'au rendu complet (à la sortie du champ) — on lisait « de aller ».
             Même règle, même propriétaire que le rendu : window._promiElide (pastille vide → « de »). */
          var li = m.previousElementSibling;
          if(li && li.classList.contains('ph-li')){
            var dd = v && window._promiElide ? window._promiElide(v) : 'de', el2 = dd === 'd\u2019';
            if(li.textContent !== dd) li.textContent = dd;
            li.classList.toggle('ph-elide', el2);
          }
        }
        if(window._ppTout) _ppTout();
      }catch(_){}
    };
    inp.onblur = function(){ _phraseRendu(); };
  }
  zone.querySelectorAll('.ph-o').forEach(function(b){
    b.onclick = function(){
      if(b.dataset.add){
        /* CHANTIER F — barre de recherche IN-PAGE (plus de window.prompt / clavier
           système) : même DA que la ligne du Promi (Bricolage, filet franc). On tape
           un prénom, les personnes connues se filtrent en dessous. */
        var host=b.parentNode; /* .ph-opts */
        if(host.querySelector('.ph-addbar')) return;
        var bar=document.createElement('div'); bar.className='ph-addbar';
        bar.innerHTML='<input type="text" class="ph-addwho" placeholder="un prénom…" autocomplete="off" spellcheck="false"><div class="ph-addsug"></div>';
        host.appendChild(bar); b.style.display='none';
        var ai=bar.querySelector('.ph-addwho'), sug=bar.querySelector('.ph-addsug');
        var people=[]; try{ people=(typeof peopleList==='function'?peopleList():[]).filter(function(n){return n&&n.toLowerCase()!=='moi';}); }catch(_){}
        function commit(nm){ nm=(nm||'').trim(); if(!nm){ return; }
          P[cle]=nm;
          /* seul « qui » (le destinataire/défié) alimente le plant via newWhoSel/#fWho ;
             « avec » est un compagnon, stocké dans P.avec uniquement. */
          if(cle !== 'avec'){
            try{ window.newWhoSel = (''+nm).toLowerCase()!=='moi' ? [nm] : []; }catch(_){}
            try{var w2=document.getElementById('fWho'); if(w2){w2.value=nm; w2.dispatchEvent(new Event('input',{bubbles:true}));}}catch(_){}
          }
          zone.classList.remove('ouvert'); _phraseRendu(); }
        function draw(){ var q=ai.value.trim().toLowerCase();
          var list=people.filter(function(n){return q&&n.toLowerCase().indexOf(q)>=0;}).slice(0,4);
          sug.innerHTML=list.map(function(n){return '<button type="button" class="ph-o" data-pick="'+n.replace(/"/g,'&quot;')+'">'+n+'</button>';}).join('');
          sug.querySelectorAll('[data-pick]').forEach(function(pb){pb.onclick=function(){commit(pb.dataset.pick);};}); }
        ai.oninput=draw;
        ai.onkeydown=function(e){ if(e.key==='Enter'){ e.preventDefault(); commit(ai.value); } };
        setTimeout(function(){ try{ai.focus();}catch(_){} },30);
        return;
      }
      if(b.dataset.datepick){
        /* DATE PRÉCISE — le sélecteur natif s'ouvre d'un geste. À la validation :
           on calcule le nombre de jours (→ due), on garde la date ISO (→ np.dueISO),
           et la phrase affiche « avant mardi 12 » (jour + quantième, court et clair). */
        var di = document.getElementById('phDateIn');
        if(di){
          var _t0 = new Date(); _t0.setHours(0,0,0,0);
          di.min = _t0.getFullYear()+'-'+String(_t0.getMonth()+1).padStart(2,'0')+'-'+String(_t0.getDate()).padStart(2,'0');
          di.onchange = function(){
            if(!di.value) return;
            var pk = new Date(di.value+'T00:00:00');
            var days = Math.max(0, Math.round((pk - _t0)/86400000));
            try{ due = days; window._csEnLair = false; }catch(_){}
            window._csDueISO = di.value;
            /* format : dans les 30 j → « mardi 12 » ; au-delà → « mardi 12 mai ». Jamais d'année. */
            P.quand = window._dateQuand ? window._dateQuand(pk, days) : (pk.getDate()+'');
            try{ document.querySelectorAll('#dueChips .chip').forEach(function(c){ c.classList.remove('on'); }); }catch(_){}
            zone.classList.remove('ouvert');
            _phraseRendu();
          };
          try{ di.showPicker ? di.showPicker() : di.focus(); }catch(_){ try{ di.focus(); }catch(__){} }
        }
        return;
      }
      P[cle] = b.dataset.v;
      /* on repercute dans le formulaire d'origine */
      try{
        if(cle === 'qui'){
          var v = b.dataset.v;
          /* le plant lit window.newWhoSel EN PREMIER ; l'ancien code ne posait que
             #fWho, réinitialisé ensuite par un re-render → le destinataire choisi était
             perdu (who='moi'). On pose newWhoSel pour qu'il survive. */
          try{ window.newWhoSel = (v && (''+v).toLowerCase()!=='moi') ? [v] : []; }catch(_){}
          var w = document.getElementById('fWho');
          if(w){ w.value = v; w.dispatchEvent(new Event('input', {bubbles:true})); }
        } else if(cle === 'quand'){
          try{ window._csDueISO = null; }catch(_){}
          if(b.dataset.v === 'un jour' || b.dataset.v === 'en l’air'){
            /* les DEUX = PAS d'échéance (due null), aucune pastille active. Mais deux
               VALEURS DE DONNÉES distinctes (jamais fusionnées) : « un jour » = une
               promesse sans date (enLair false) ; « en l'air » = une envie (enLair true).
               Ni l'une ni l'autre ne passe « à tenir » ni ne déclenche de rappel. */
            try{ due = null; window._csEnLair = (b.dataset.v === 'en l’air'); }catch(_){}
            try{ document.querySelectorAll('#dueChips .chip,#dfDueChips .chip').forEach(function(c){ c.classList.remove('on'); }); }catch(_){}
          } else {
            /* on ACTIVE la pastille #dueChips correspondante — par data-d, JAMAIS par le
               libellé affiché (piège documenté). Phrase et Peaufiner restent synchro. */
            try{ window._csEnLair = false; }catch(_){}
            var chipD = { 'demain':2, '5 jours':5, '2 semaines':14, 'ce mois-ci':40 }[b.dataset.v];
            if(chipD != null){
              try{ due = chipD; }catch(_){}
              try{ document.querySelectorAll('#dueChips .chip,#dfDueChips .chip').forEach(function(c){ c.classList.toggle('on', +c.dataset.d===chipD); }); }catch(_){}
            }
          }
        }
      }catch(_){}
      zone.classList.remove('ouvert');
      _phraseRendu();
      try{ if(window._peintGrappe){ setTimeout(window._peintGrappe,60); setTimeout(window._peintGrappe,240); } }catch(_){}
    };
  });
  /* ⚑ LES PERSONNES passent par le choix partagé (lot-GENS) : on ajoute, on retire d'une croix, on garde « + ajouter ». */
  if((cle === 'qui' || cle === 'avec') && window._gensPhrase) window._gensPhrase(zone, cle);
}catch(e){} };

(function(){ try{
  var poser = function(){
    var cs = document.getElementById('createSheet');
    if(!cs || cs._phrPose) return;
    cs._phrPose = true;
    var ouvert = false;
    new MutationObserver(function(){
      var v = cs.classList.contains('show');
      if(v === ouvert) return;
      ouvert = v;
      if(v) requestAnimationFrame(function(){
        /* le reset « ardoise propre » à l'ouverture doit respecter le contexte Nuée :
           en lançant un Promi DEPUIS une Nuée (selNuee posé), « à qui » vaut « tout le
           monde », pas « Moi » — sinon la phrase affichait « à Moi » alors que le Promi
           se plantait « à tout le monde » (le geste corrigeait, l'affichage mentait). */
        try{ var _q = (typeof selNuee!=='undefined' && selNuee) ? 'tout le monde' : 'Moi';
          window._phrase = { sens:'faire', qui:_q, titre:'', quand:'un jour' };
          /* v103 — la nature a pu être choisie AVANT cette image (le + de l'accueil ouvre sur une nature) : l'ardoise propre
             d'un Chiche reste un Chiche. Sans ça, le premier toucher de « Un Chiche » ouvrait la phrase d'un Promi, la page +
             recliquait sa tuile 380 ms plus tard, et l'on voyait passer les deux phrases. */
          try{ if(cs.getAttribute('data-kind')==='chiche'){ window._phrase.sens='chiche'; window._csSens='chiche'; } }catch(_e){}
          /* ardoise propre = PAS d'échéance (Décision Tom) : due null, aucun flag, aucune
             pastille active. La phrase (« un jour ») et Peaufiner (rien d'allumé) s'accordent. */
          try{ due = null; window._csEnLair = false; window._csDueISO = null;
            document.querySelectorAll('#dueChips .chip,#dfDueChips .chip').forEach(function(c){ c.classList.remove('on'); }); }catch(_e){}
          _phraseRendu(); }catch(_){}
      });
    }).observe(cs, {attributes:true, attributeFilter:['class']});
  };
  poser();
  document.addEventListener('DOMContentLoaded', poser);
  setTimeout(poser, 1600);
}catch(e){} })();
window._fichePose = function(){ try{
  var dp = document.getElementById('detailPoster');
  if(!dp) return;
  /* sur une fiche de Nuee, « cur » est nul : on ne sort pas pour autant,
     c'est « curNuee » qui porte le groupe. */
  var estNueeF0 = dp.classList.contains('dp-nuee')
    || dp.classList.contains('dp-mode-nuee')
    || (typeof curNuee !== 'undefined' && !!curNuee
        && (typeof cur === 'undefined' || !cur));
  if(estNueeF0) dp.classList.add('dp-nuee');
  if(!estNueeF0 && (typeof cur === 'undefined' || !cur)) return;
  if(estNueeF0 && (typeof cur === 'undefined' || !cur)) cur = { title:'', draft:false, status:'' };

  /* 1 · la couleur de l'etat sur le fond */
  var etat = cur.draft ? 'brouillon'
           : (cur.status === 'tenu') ? 'tenue'
           : (cur.status === 'rate') ? 'atenir' : 'encours';
  var FOND = { tenue:'#8FE08F', atenir:'#DD4D23', encours:'', brouillon:'' };
  var ENCRE= { tenue:'#00341A', atenir:'#FFFFFF', encours:'', brouillon:'' };
  dp.classList.remove('f-tenue','f-atenir','f-encours','f-brouillon');
  dp.classList.add('f-' + etat);

  /* 2 · l'en-tete : on le batit une fois, on le remplit ensuite */
  var tete = document.getElementById('dpTete');
  if(!tete){
    tete = document.createElement('div');
    tete.id = 'dpTete';
    tete.innerHTML =
      '<div class="dpt-nat" id="dptNat"></div>'
    + '<div class="dpt-qui" id="dptQui"></div>'
    + '<div class="dpt-titre" id="dptTitre"></div>'
    + '<div class="dpt-quand" id="dptQuand"></div>';
    dp.insertBefore(tete, dp.firstChild);
  }
  var estNueeF = estNueeF0;
  var NAT = { brouillon:'Brouillon', tenue:'Promi', atenir:'Promi', encours:'Promi' };
  document.getElementById('dptNat').textContent = estNueeF ? 'Cercle' : (NAT[etat] || 'Promi');

  /* a qui — le prenom en pleine encre, le reste attenue */
  var qui = document.getElementById('dptQui');
  if(cur.draft){ qui.innerHTML = '<span class="pale">rien n\u2019est encore promis</span>'; }
  else {
    /* « a le groupe » n'est pas du francais : on nomme les gens. Au-dela de
       trois, on nomme les deux premiers et on compte le reste. */
    var gens = [];
    try{
      if(cur.who && /groupe|nu[ée]e/i.test(cur.who) && cur.nuee){
        gens = (window.membresNuee ? membresNuee(cur.nuee) : []) || [];
      } else if(cur.who){ gens = String(cur.who).split(/\s*[,·]\s*/).filter(Boolean); }
    }catch(_){}
    var nom;
    if(!gens.length) nom = cur.who || 'toi';
    else if(gens.length <= 2) nom = gens.join(' et ');
    else nom = gens.slice(0,2).join(', ') + ' et ' + (gens.length-2) + ' autres';
    qui.innerHTML = '<span class="pale">\u00e0 </span><b>' + nom + '</b>';
  }

  /* ── L'EN-TETE D'UNE NUEE ──
     Le nom du groupe en grand, qui en est, combien de paroles.
     Tout ce qu'on veut savoir en arrivant. */
  if(estNueeF){
    var cleN = (typeof curNuee !== 'undefined') ? curNuee : '';
    var lst = [];
    try{ lst = promises.filter(function(q){ return q.nuee === cleN && !q.draft; }); }catch(_){}
    var membres = [];
    try{ membres = [...new Set(lst.map(function(q){ return q.who; }).filter(Boolean))]; }catch(_){}
    /* le NOM, pas la cle : « N1784933191453 » etait l'identifiant interne. */
    /* la table des noms s'appelle NUE — trouvee en lisant le source. */
    var nomN = '';
    try{
      if(typeof NUE !== 'undefined' && NUE[cleN]) nomN = NUE[cleN];
      if(!nomN && window.nueeNom) nomN = nueeNom(cleN) || '';
      if(!nomN && !/^N?\d{6,}$/.test(cleN)) nomN = cleN;
      if(!nomN) nomN = 'Ce Cercle';
    }catch(_){ nomN = 'Ce Cercle'; }
    /* ⚠ LE NOM D'UNE NUÉE GARDE SA CASSE. La planche écrit « le potager », en minuscule —
       cadres 40, 58 et 72, et le fil du Fil (« LE POTAGER · 6 PROMI » n'est capitalisé que
       parce que la LIGNE D'ÉTAT est en capitales). Mettre une majuscule d'office donnait
       « Le potager » sur la fiche : un mot que le moodboard n'écrit nulle part. Le nom est
       celui que l'utilisateur a donné ; on ne le retouche pas. */
    document.getElementById('dptTitre').textContent = nomN;
    document.getElementById('dptQui').innerHTML = membres.length
      ? '<span class="pale">avec </span><b>' + membres.slice(0,3).join(', ')
        + (membres.length > 3 ? ' et ' + (membres.length-3) + ' autres' : '') + '</b>'
      : '<span class="pale">personne encore \u2014 invite quelqu\u2019un</span>';
    var tenues = lst.filter(function(q){ return q.status === 'tenu'; }).length;
    var qN = document.getElementById('dptQuand');
    qN.textContent = lst.length
      ? lst.length + ' Promi'
        + (tenues ? ' \u00b7 ' + tenues + ' tenu' + (tenues>1?'s':'') : '')
      : 'encore aucune parole';   /* ⚑ Q213 (Tom) : « ENCORE AUCUNE PAROLE » — couvre les deux natures, « encore » dit que ça va venir */
    qN.setAttribute('data-nuee','1');
    /* les attributs vivent SUR la ligne du compte : la place a droite etait
       perdue, et note/pj/commentaires n'apparaissaient nulle part. */
    try{
      var ex = [];
      if(cur && cur.note && String(cur.note).trim()) ex.push('une note');
      var nf2 = (cur && cur.files && cur.files.length) || 0;
      if(nf2) ex.push(nf2 + (nf2>1?' fichiers':' fichier'));
      var nc2 = 0;
      lst.forEach(function(q){ nc2 += (q.comments && q.comments.length) || 0; });
      if(nc2) ex.push(nc2 + (nc2>1?' mots':' mot'));
      var sp = document.getElementById('dptExtras');
      if(!sp){ sp = document.createElement('span'); sp.id = 'dptExtras'; qN.appendChild(sp); }
      sp.textContent = ex.length ? '  ·  ' + ex.join('  ·  ') : '';
    }catch(_){}

    /* ── LE FIL DE LA NUEE ──
       Ses paroles, en cartes, des l'ouverture. C'est le coeur du groupe :
       on vient voir ce qui s'y passe et en ajouter. */
    var fil = document.getElementById('dpNueeFil');
    if(!fil){
      fil = document.createElement('div');
      fil.id = 'dpNueeFil';
      dp.appendChild(fil);
    }
    fil.style.display = '';
    var COUL = { tenu:'#8FE08F', rate:'#DD4D23' };
    /* deux gestes en tete du fil : planter, et partager la Nuee. */
    var h = '<div class="nf-tete">'
          + '<button class="nf-add" id="nfAdd"><span class="nf-plus"><svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true"><path d="M16 6 V26 M6 16 H26" stroke="#291547" stroke-width="3.6" stroke-linecap="round"/></svg></span>Planter dans le Cercle</button>'   /* ⚑ Q213 : le verbe dit qu'on crée une parole, la Nuée dit où */
          + '<button class="nf-part" id="nfPart" aria-label="Partager le Cercle">'
          + '<svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" '
          + 'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
          + '<path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7"/>'
          + '<path d="M16 6l-4-4-4 4"/><path d="M12 2v14"/></svg></button>'
          + '</div>';
    if(lst.length){
      h += '<div class="nf-liste">';
      lst.forEach(function(q){   /* ⚑ 14 sept. : plus de coupe à 8 — le potager en porte 9 */
        var c = COUL[q.status] || '';
        /* la DA du Fil : une bande, le texte a gauche, la dalle a droite. */
        /* LA LOGIQUE DE L'INDEX : le mot du temps, l'aplat de l'etat, et la
           VRAIE dalle a droite — jamais un polygone, jamais une photo. */
        var mot = '';
        try{ var mt = motDuTemps(q); mot = mt ? mt.mot : ''; }catch(_){ }
        /* les memes couleurs que le Fil : menthe si tenue, orange si a
           tenir, et la teinte de SA dalle si en cours — jamais de neutre. */
        var cls = q.status === 'tenu' ? ' nf-menthe'
                : q.status === 'rate' ? ' nf-ocre' : ' nf-cours';
        var teinte = '';
        if(!q.status || (q.status !== 'tenu' && q.status !== 'rate')){
          try{
            var tq = document.createElement('canvas');
            if(window.Toile && Toile.dalleTrame && Toile.dalleTrame(tq, q.id, 1)){
              var td = window._teinteDalle && _teinteDalle(tq);
              if(td && td.css) teinte = ' style="background:' + td.css + '"';
            }
          }catch(_){}
        }
        h += '<div class="nf-item' + cls + ' nf-vif" data-id="' + q.id + '"' + teinte + '>'
           + '<div class="nf-tx"><em>' + mot + '</em>'
           + '<b>' + (q.title || '') + '</b>'
           + '<span>' + (q.who ? '\u00e0 ' + q.who : '\u00e0 toi') + '</span></div>'
           + '<span class="nf-dw"><canvas class="bul mini-dalle nf-d" width="144" height="144" '
           + 'data-mini="' + q.id + '"></canvas></span>'
           + '</div>';
      });
      h += '</div>';
    } else {
      h += '<div class="nf-vide">aucun Promi ici pour l\u2019instant</div>';
    }
    /* la note et les pieces jointes se voient des la premiere page */
    var extras = [];
    try{
      if(window.nueeNote && nueeNote(cleN)) extras.push('une note');
      var nfN = (window.nueeFiles ? (nueeFiles(cleN)||[]).length : 0);
      if(nfN) extras.push(nfN + (nfN>1 ? ' fichiers' : ' fichier'));
    }catch(_){}
    if(extras.length) h += '<div class="nf-extras">' + extras.join(' \u00b7 ') + '</div>';
    fil.innerHTML = h;
    /* les dalles se peignent APRES l'insertion : un seul rAF ne suffit
       pas quand le navigateur n'a pas encore dispose les canvas. */
    /* la peinture des dalles : plusieurs relances, la derniere a 600 ms —
       les canvas ne sont mesurables qu'une fois disposes. */
    try{ if(window.peintMinis){
      [0, 60, 200, 600].forEach(function(ms){
        setTimeout(function(){ try{ peintMinis(fil); }catch(_){} }, ms);
      });
    } }catch(_){}
    var add = document.getElementById('nfAdd');
    if(add) add.onclick = function(){
      var b = document.getElementById('nqAddPromi');
      if(b) b.click();
    };
    /* partager la Nuee : la page de partage, avec ses Promi au lieu de la Toile */
    var bp2 = document.getElementById('nfPart');
    if(bp2) bp2.onclick = function(){
      try{
        window._partageNuee = cleN;
        if(window.ouvrirPartage) ouvrirPartage();
        else { var s = document.getElementById('shareSheet') || document.getElementById('partageScreen');
               if(s) s.classList.add('show'); }
      }catch(_){}
    };
    /* le clic ouvre la fiche du Promi : « ouvrirPromi » n'existe pas,
       on passe par le chemin de l'Index. */
    fil.querySelectorAll('.nf-item').forEach(function(it){
      it.onclick = function(){
        var id = +it.getAttribute('data-id');
        var q = null;
        try{ q = promises.find(function(x){ return x.id === id; }); }catch(_){}
        if(!q) return;
        try{
          dp.classList.remove('show');
          setTimeout(function(){
            try{
              cur = q;
              if(window.renderDetail) renderDetail();
              dp.classList.remove('dp-nuee','dp-mode-nuee');
              dp.classList.add('show');
            }catch(_){}
          }, 240);
        }catch(_){}
      };
    });
  } else {
    document.getElementById('dptTitre').textContent = cur.title || '';
    /* un Promi n'a pas de fil : il est unique. */
    var f0 = document.getElementById('dpNueeFil');
    if(f0) f0.style.display = 'none';
  }

  /* quand */
  var q = document.getElementById('dptQuand');
  if(estNueeF){ /* le compte des paroles est deja pose */ }
  else if(etat === 'tenue') q.textContent = 'tenue \u00e0 l\u2019instant';
  else if(etat === 'atenir') q.textContent = '\u00e0 tenir';
  else if(cur.draft) q.textContent = '';
  else { try{ var m = motDuTemps(cur); q.textContent = m ? m.mot : ''; }catch(_){ q.textContent=''; } }

  /* 3 · l'ordre : en-tete, disques, geste, puis le reste sous Details */
  var det = document.getElementById('dpDetails');
  if(!det){
    det = document.createElement('div');
    det.id = 'dpDetails';
    det.innerHTML = '<div class="dpd-tog" id="dpdTog">Peaufiner <i>\u25be</i></div>'
                  + '<div class="dpd-corps peauf-reglages" id="dpdCorps"></div>';
    dp.appendChild(det);
    document.getElementById('dpdTog').addEventListener('click', function(e){
      det.classList.toggle('ouvert');
      /* on glisse jusqu'au contenu deplie */
      if(det.classList.contains('ouvert')){
        setTimeout(function(){
          try{ det.scrollIntoView({block:'start', behavior:'smooth'}); }catch(_){}
        }, 260);
      }
      e.stopPropagation();
    }, true);
  }
  /* SEUL LE REGLAGE se replie. Ce qu'on consulte — a qui, la Nuee, la
     note, les commentaires — reste visible : une fiche vide n'apprend
     rien et oblige a un geste de plus. */
  /* TOUT le reglage passe sous « Peaufiner » : la premiere page ne montre
     que l'essentiel, et tout tient dans l'ecran. */
  /* PEAUFINER contient TOUT le reglage : le corps du Promi et, sur une
     Nuee, son propre corps. Sans ca le tiroir s'ouvrait sur du vide. */
  var corps = document.getElementById('dpdCorps');
  ['dpPromiBody','nqBody','dpNueeBody'].forEach(function(id){
    var el = document.getElementById(id);
    if(el && el.parentNode !== corps) corps.appendChild(el);
  });
  /* sur une Nuee, on remonte aussi les blocs qui vivent ailleurs */
  if(estNueeF0){
    ['nqTheme','nqDesc','nqFiles','nqMembres','nqInvite','nqDissolveRow']
      .forEach(function(id){
        var el = document.getElementById(id);
        var pa = el && el.closest ? el.closest('.mg-sec,.dp-sec,div') : null;
        if(el && el.parentNode !== corps) corps.appendChild(pa && pa!==corps ? pa : el);
      });
  }
  /* L'ORDRE DE LA PAGE — le meme pour les trois natures.
     Peaufiner ferme la marche : il est donc toujours visible en bas. */
  /* dpBarre vit DANS dAura : le citer ici l'en arrachait, d'ou la
     barre en double. */
  ['dAura','tenirZone','dpTrace','dpNueeFil','dpKind'].forEach(function(id){
    var el = document.getElementById(id);
    if(el) dp.appendChild(el);
  });
  dp.insertBefore(tete, dp.querySelector('#dAura') || null);
  if(det) dp.appendChild(det);
  /* le brouillon et la Nuee n'ont pas de geste de tenue */
  /* LE RANG DU LIEN : un disque a gauche, les attributs a droite.
     Note et piece jointe ne meritent pas une section entiere quand elles
     sont vides — mais elles doivent se voir quand elles existent. */
  var att = document.getElementById('dpAttrs');
  if(!att){
    att = document.createElement('div');
    att.id = 'dpAttrs';
    var au = document.getElementById('dAura');
    if(au && au.parentNode) au.appendChild(att);
  }
  /* UN SEUL bouton pour la note et les fichiers : vide il invite, rempli il
     compte. Une icone, jamais un mot — la place est rare a droite du disque. */
  var nNote = (cur.note && cur.note.trim()) ? 1 : 0;
  var nFic  = (cur.files && cur.files.length) || 0;
  var total = nNote + nFic;
  /* une pastille de la meme famille que les autres : un mot, pas une icone
     de logiciel. « ajouter un mot » invite ; « 2 notes » constate. */
  /* un simple + : la place est rare, et l'icone se comprend seule. */
  /* le « + » disparait : « Peaufiner » le remplace, et l'espace libere
     sert a la note, aux fichiers et aux commentaires. */
  att.innerHTML = '';
  att.style.display = '';
  var bj = document.getElementById('dpaJoint');
  if(bj && !bj._pose){
    bj._pose = true;
    bj.addEventListener('click', function(){
      var d = document.getElementById('dpDetails');
      if(d){
        d.classList.add('ouvert');
        /* on glisse jusqu'au champ, sans a-coup : on attend que le tiroir
           ait fini de s'ouvrir avant de defiler. */
        var n = document.getElementById('dNote');
        if(n) setTimeout(function(){
          try{
            var dp = document.getElementById('detailPoster');
            var cible = n.getBoundingClientRect().top - dp.getBoundingClientRect().top
                      + dp.scrollTop - 180;
            dp.scrollTo({ top: cible, behavior: 'smooth' });
            setTimeout(function(){ n.focus({preventScroll:true}); }, 420);
          }catch(_){ n.scrollIntoView({block:'center',behavior:'smooth'}); }
        }, 430);
      }
    });
  }

  /* LA TEINTE DE LA DALLE devient la couleur des accents : le trait du
     geste, la pastille, le filet sous le titre. Chaque Promi a donc SA
     couleur — c'est ce qui fait qu'aucune fiche ne ressemble a une autre. */
  /* ── LA REGLE DES COULEURS, ARRETEE ──
     Les accents portent la couleur de L'ETAT, pas celle de la matiere :
       menthe  = tenue      orange = a tenir
       neutre  = en cours   lilas  = Nuee
     C'est indicatif, pas decoratif. La teinte de la dalle etait jolie mais
     ne disait rien — d'ou l'impression d'incoherence. */
  var estNueeTest = !!(cur.isNuee || cur.kind === 'nuee' || cur.nueeOnly);
  var ACC = { tenue:'#8FE08F', atenir:'#DD4D23', brouillon:'#DD4D23' };
  var acc = ACC[etat];
  /* une Nuee prend la teinte de son dernier Promi : elle n'a pas d'etat
     propre, mais elle a une matiere. */
  if(estNueeTest || dp.classList.contains('dp-mode-nuee')){
    acc = '#291547';
    try{
      var cN = (typeof curNuee !== 'undefined') ? curNuee : null;
      var der = promises.filter(function(q){ return q.nuee === cN && !q.draft; }).pop();
      if(der){
        var tc2 = document.createElement('canvas');
        if(window.Toile && Toile.dalleTrame && Toile.dalleTrame(tc2, der.id, 1)){
          var t2 = window._teinteDalle && _teinteDalle(tc2);
          if(t2 && t2.css) acc = t2.css;
        }
      }
    }catch(_){}
  }
  /* EN COURS n'a pas de couleur d'etat — mais du noir serait triste.
     Il prend alors la teinte de SA dalle : la page vit, sans mentir. */
  if(!acc){
    try{
      var tc = document.createElement('canvas');
      if(window.Toile && Toile.dalleTrame && Toile.dalleTrame(tc, cur.id, 1)){
        var t = window._teinteDalle && _teinteDalle(tc);
        if(t && t.css) acc = t.css;
      }
    }catch(_){}
  }
  /* JAMAIS de ton sur ton : sur un fond menthe, un accent menthe disparait.
     L'accent passe alors en encre profonde — c'est le contraste qui est beau. */
  /* DEUX couleurs, deux usages :
       --dalle  l'encre lisible sur l'aplat (contraste)
       --accent la couleur d'etat, pour les filets et les traits
     Confondre les deux rendait les filets noirs sur une fiche tenue. */
  var accent = acc;
  /* ══ LA REGLE DES COULEURS, EN DEUX PHRASES ══
       LE FOND dit l'ETAT      menthe = tenue · orange = a tenir · mauve = Nuee
       LES TRAITS disent la MATIERE   la teinte de la dalle de CE Promi

     C'est ce qui evite le ton sur ton : la teinte d'une dalle vient du monde
     choisi, jamais de l'etat. Elle contraste donc toujours avec le fond.
     Et chaque Promi porte ses propres traits — deux fiches tenues n'ont pas
     les memes. */
  var teinte = null;
  try{
    var tcv = document.createElement('canvas');
    /* une Nuee prend la teinte de SA DERNIERE dalle plantee : ses traits
       changent a chaque nouveau Promi. C'est le groupe qui vit. */
    var estN2 = estNueeTest || dp.classList.contains('dp-mode-nuee');
    var idT = (!estN2 && typeof cur !== 'undefined' && cur && cur.id) ? cur.id : null;
    if(idT === null && estN2){
      var cN3 = (typeof curNuee !== 'undefined') ? curNuee : null;
      var lst3 = [];
      try{ lst3 = promises.filter(function(q){ return q.nuee === cN3 && !q.draft; }); }catch(_){}
      if(lst3.length) idT = lst3[lst3.length - 1].id;
    }
    if(idT === null && estNueeTest){
      var cN2 = (typeof curNuee !== 'undefined') ? curNuee : null;
      var d0 = promises.filter(function(q){ return q.nuee === cN2 && !q.draft; }).pop();
      if(d0) idT = d0.id;
    }
    if(idT !== null && window.Toile && Toile.dalleTrame && Toile.dalleTrame(tcv, idT, 1)){
      var tt = window._teinteDalle && _teinteDalle(tcv);
      if(tt && tt.css) teinte = tt.css;
    }
  }catch(_){}

  var clair = false;
  try{ clair = !!document.querySelector('.frame.light, .device.light'); }catch(_){}
  if(etat === 'tenue') acc = clair ? '#00341A' : '#8FE08F';
  else if(etat === 'atenir') acc = clair ? '#201908' : '#FFFFFF';

  /* ══ TROIS TONS, JAMAIS DEUX ══
       1 · la DALLE      sa couleur propre
       2 · le FOND       l'etat
       3 · les TRAITS    la teinte de la dalle DECALEE de 150 degres
     Le decalage garde la famille chromatique de la palette du Studio tout en
     tranchant : ni ton sur ton avec la dalle, ni ton sur ton avec le fond. */
  accent = acc;
  if(teinte){
    try{
      var mm = teinte.match(/[\d.]+/g);
      if(mm && mm.length >= 3){
        var R = +mm[0]/255, G = +mm[1]/255, B = +mm[2]/255;
        var mx = Math.max(R,G,B), mn = Math.min(R,G,B), d = mx-mn;
        var h = 0, s = mx ? d/mx : 0, v = mx;
        if(d){
          if(mx === R) h = ((G-B)/d + (G < B ? 6 : 0));
          else if(mx === G) h = (B-R)/d + 2;
          else h = (R-G)/d + 4;
          h /= 6;
        }
        h = (h + 150/360) % 1;                     /* le decalage */
        s = Math.min(1, Math.max(0.55, s * 1.25)); /* assez vive pour se voir */
        v = clair ? Math.min(0.82, v * 0.86) : Math.min(1, Math.max(0.72, v));
        var i2 = Math.floor(h*6), f = h*6 - i2;
        var pv = v*(1-s), q = v*(1-f*s), t2 = v*(1-(1-f)*s);
        var rgb = [[v,t2,pv],[q,v,pv],[pv,v,t2],[pv,q,v],[t2,pv,v],[v,pv,q]][i2%6];
        accent = 'rgb(' + rgb.map(function(x){ return Math.round(x*255); }).join(',') + ')';
      }
    }catch(_){}
  }

  /* Chiche : le trait (filet, dpBarre) prend le SIGNAL framboise, comme un Promi
     prend le bleu — pas le décalage 150° dérivé de la dalle (qui donnerait un ton
     hors palette). L'identité de nature prime sur la dérivation chromatique. */
  try{ if(cur && cur.chiche) accent = '#FFB8D2'; }catch(_){}
  if(acc){ dp.style.setProperty('--dalle', acc); window._encreGeste = accent || acc; }
  else { dp.style.removeProperty('--dalle'); window._encreGeste = null; }
  if(accent) dp.style.setProperty('--accent', accent);
  else dp.style.removeProperty('--accent');

  /* ── LES TROIS NATURES ──
     Une Nuee ne se tient pas : elle s'etoffe. Un brouillon n'existe pas
     encore : il se choisit. Chacune a donc ses propres gestes. */
  var estNuee = !!(cur.isNuee || cur.kind === 'nuee' || (cur.nueeOnly));
  dp.classList.toggle('dp-nuee', estNuee);
  dp.classList.toggle('dp-draft', !!cur.draft);

  /* (le rang social a ete remplace par la barre dans le rang du lien) */
  var ouvrePeaufiner = function(champ){
    var d = document.getElementById('dpDetails');
    if(!d) return;
    d.classList.add('ouvert');
    setTimeout(function(){
      var t = document.getElementById(champ);
      if(t){ try{ t.scrollIntoView({block:'center', behavior:'smooth'});
        setTimeout(function(){ t.focus({preventScroll:true}); }, 400); }catch(_){}
      }
    }, 420);
  };
  var bc = document.getElementById('dpsCom');
  if(bc) bc.onclick = function(){ ouvrePeaufiner('dCommentInput'); };
  var bj = document.getElementById('dpsJoint');
  if(bj) bj.onclick = function(){ ouvrePeaufiner('dNote'); };
  var bpa = document.getElementById('dpsPart');
  if(bpa) bpa.onclick = function(){
    try{ if(window.ouvrirPartage) ouvrirPartage();
      else { var s = document.getElementById('shareSheet')
                 || document.getElementById('partageScreen');
             if(s) s.classList.add('show'); } }catch(_){}
  };

  /* ── LA BARRE DU ONE PAGER ──
     Trois gestes, toujours visibles : commenter, joindre, partager.
     Un Promi se commente a deux quel que soit son etat — c'est le fil de
     la parole, pas un journal de bord. */
  /* les actions vivent SUR la ligne du disque : l'espace a droite etait
     perdu, et une barre a part ajoutait une ligne pour rien. */
  var barre = document.getElementById('dpBarre');
  if(!barre){
    barre = document.createElement('div');
    barre.id = 'dpBarre';
  }
  var au = document.getElementById('dAura');
  if(au && barre.parentNode !== au) au.appendChild(barre);
  var nC = 0, nN = 0, nF = 0;
  try{
    nC = (cur.comments && cur.comments.length) || 0;
    nN = (cur.note && String(cur.note).trim()) ? 1 : 0;
    nF = (cur.files && cur.files.length) || 0;
  }catch(_){}
  /* des signes, pas des mots : trois icones de 46 px, un compte en pastille
     quand il y a du contenu. */
  var ic = function(d){ return '<svg viewBox="0 0 24 24" width="21" height="21" '
    + 'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
    + 'stroke-linejoin="round">' + d + '</svg>'; };
  var iCom  = ic('<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.2A8.4 8.4 0 0 1 21 11.5z"/>');
  var iJoin = ic('<path d="M21.4 11.05 12.25 20.2a5 5 0 0 1-7.07-7.07l9.19-9.19a3.34 3.34 0 0 1 4.71 4.71l-9.19 9.2a1.67 1.67 0 0 1-2.36-2.36l8.49-8.48"/>');
  var iPart = ic('<path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v14"/>');
  var pastille = function(n){ return n ? '<i class="dpb-n">' + n + '</i>' : ''; };
  barre.innerHTML =
      '<button class="dpb" id="dpbCom" aria-label="Commenter">' + iCom + pastille(nC) + '</button>'
    + '<button class="dpb" id="dpbJoint" aria-label="Joindre une note ou un fichier">' + iJoin + pastille(nN+nF) + '</button>'
    + '<button class="dpb" id="dpbPart" aria-label="Partager">' + iPart + '</button>';
  var vaVers = function(id){
    var d = document.getElementById('dpDetails');
    if(d) d.classList.add('ouvert');
    setTimeout(function(){
      var c = document.getElementById(id);
      if(c){ try{ c.scrollIntoView({block:'center', behavior:'smooth'}); }catch(_){}
        setTimeout(function(){ try{ c.focus({preventScroll:true}); }catch(_){} }, 400); }
    }, 420);
  };
  var b1 = document.getElementById('dpbCom');
  if(b1) b1.onclick = function(){ vaVers('dCommentInput'); };
  var b2 = document.getElementById('dpbJoint');
  if(b2) b2.onclick = function(){ vaVers('dNote'); };
  var b3 = document.getElementById('dpbPart');
  if(b3) b3.onclick = function(){
    try{ if(window.ouvrirPartage) ouvrirPartage();
      else { var s = document.getElementById('shareSheet') || document.getElementById('partageScreen');
             if(s) s.classList.add('show'); } }catch(_){}
  };

  var z = document.getElementById('tenirZone');
  if(z) z.style.display = (etat === 'tenue' || cur.draft || estNuee) ? 'none' : '';

  /* le brouillon : ce qu'il deviendra, et les options qui suivent */
  var kd = document.getElementById('dpKind');
  if(cur.draft){
    if(!kd){
      kd = document.createElement('div');
      kd.id = 'dpKind';
      kd.innerHTML = '<div class="mg-lab">IL DEVIENDRA</div>'
        + '<div class="dpk-seg">'
        + '<button data-k="promi">un Promi</button>'
        + '<button data-k="nueepromi">en Cercle</button>'
        + '<button data-k="nuee">un Cercle</button></div>'
        + '<button class="dpk-go" id="dpkGo">LE PLANTER</button>';
      /* apres la parole : on lit d'abord ce qu'on a note. */
      dp.appendChild(kd);
      kd.addEventListener('click', function(e){
        var b = e.target.closest('[data-k]');
        if(!b) return;
        kd.querySelectorAll('[data-k]').forEach(function(x){ x.classList.toggle('on', x===b); });
        cur.kindDraft = b.dataset.k;
        /* les options changent selon la nature choisie */
        dp.classList.toggle('dk-nuee', b.dataset.k === 'nuee');
        dp.classList.toggle('dk-dansnuee', b.dataset.k === 'nueepromi');
      });
      var g = kd.querySelector('[data-k="promi"]'); if(g) g.classList.add('on');
    }
    kd.style.display = '';
  } else if(kd) kd.style.display = 'none';
  /* une parole tenue porte sa TRACE, pas un vide : c'est la recompense. */
  var tr = document.getElementById('dpTrace');
  if(etat === 'tenue'){
    if(!tr){
      tr = document.createElement('div');
      tr.id = 'dpTrace';
      tr.innerHTML =
          '<div class="dpt-lab">PAROLE TENUE</div>'
        + '<svg viewBox="0 0 300 74" class="dpt-svg"><path id="dptPath" d="" fill="none" '
        + 'stroke="currentColor" stroke-width="5" stroke-linecap="round" '
        + 'stroke-linejoin="round"/></svg>'
        + '<div class="dpt-mot" id="dptMot"></div>'
        + '<div class="dpt-actes">'
        + '<button class="dpt-a" id="dptPartage">Partager</button>'
        + '<button class="dpt-a" id="dptEncore">En replanter un</button>'
        + '</div>';
      /* dpPromiBody vit desormais dans le tiroir : insertBefore echouait.
         On ajoute simplement, l'ordre est impose plus bas. */
      dp.appendChild(tr);
    }
    tr.style.display = '';
    /* un mot qui felicite, jamais un score */
    try{
      var mots = ['Belle parole.', 'C\u2019est fait.', 'Une de plus.',
                  'Tenue, comme promis.', 'Bien jou\u00e9.'];
      var tenues = 0;
      try{ tenues = promises.filter(function(q){ return q.status === 'tenu'; }).length; }catch(_){}
      var mm = document.getElementById('dptMot');
      if(mm) mm.textContent = mots[tenues % mots.length]
        + (tenues > 1 ? '  \u00b7  ' + tenues + ' Promi tenus' : '');
    }catch(_){}
    /* les deux gestes qui suivent une parole tenue */
    try{
      var bp = document.getElementById('dptPartage');
      if(bp && !bp._pose){ bp._pose = true; bp.onclick = function(){
        try{ if(window.ouvrirPartage) ouvrirPartage();
          else { var s = document.getElementById('shareSheet') || document.getElementById('partageScreen');
                 if(s) s.classList.add('show'); } }catch(_){}
      }; }
      var be = document.getElementById('dptEncore');
      if(be && !be._pose){ be._pose = true; be.onclick = function(){
        try{ document.getElementById('detailPoster').classList.remove('show');
          setTimeout(function(){ var c = document.getElementById('createSheet');
            if(c){ c.classList.add('show'); if(window.renderCsDalle) renderCsDalle(); } }, 240);
        }catch(_){}
      }; }
    }catch(_){}
    /* LE VRAI TRAIT : celui qu'on a trace, pas une vague generique. */
    try{
      var pth = document.getElementById('dptPath');
      var pts = (cur.trace && cur.trace.length) ? cur.trace : window._traceTenir;
      if(pth && pts && pts.length > 1){
        var xs = pts.map(function(p){return p.x;}), ys = pts.map(function(p){return p.y;});
        var x0 = Math.min.apply(null,xs), x1 = Math.max.apply(null,xs);
        var y0 = Math.min.apply(null,ys), y1 = Math.max.apply(null,ys);
        var lw = Math.max(1,x1-x0), lh = Math.max(1,y1-y0);
        var k = Math.min(280/lw, 58/lh);
        var d = pts.map(function(p,i){
          return (i?'L':'M') + ((p.x-x0)*k + 10).toFixed(1) + ','
                             + ((p.y-y0)*k + (74 - lh*k)/2).toFixed(1);
        }).join(' ');
        pth.setAttribute('d', d);
      } else if(pth && !pth.getAttribute('d')){
        pth.setAttribute('d','M22,52 C62,14 104,64 146,32 C182,6 224,54 268,26');
      }
    }catch(_){}
  } else if(tr) tr.style.display = 'none';
  /* la matiere du monde remplit le haut */
  /* dpTrame() repeint ce canvas apres nous : on repasse en dernier. */
  try{ window._ficheT0 = Date.now(); }catch(_){}
  try{ if(window._ficheDalle) requestAnimationFrame(function(){
    requestAnimationFrame(_ficheDalle); }); }catch(_){}
  try{ if(window._nettoieNuee) requestAnimationFrame(_nettoieNuee); }catch(_){}
  /* ── PARTAGER REJOINT LA LIGNE « PEAUFINER » ──
     Un gros bouton mangeait l'ecran ; l'icone tient dans la ligne du bas. */
  try{
    var tog = document.querySelector('#dpDetails .dpd-tog');
    if(tog && !tog.querySelector('.dpd-part')){
      var sp = document.createElement('span');
      sp.className = 'dpd-part';
      sp.setAttribute('aria-label','Partager');
      /* cadre 48 : svg 22 × 22, stroke-width 2.6 — l'app était à 19 / 1,8 */
      sp.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" '
        + 'stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
        + '<path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7"/>'
        + '<path d="M16 6l-4-4-4 4"/><path d="M12 2v14"/></svg>';
      sp.onclick = function(e){
        e.stopPropagation();
        try{ if(window.ouvrirPartage) ouvrirPartage();
          else { var s = document.getElementById('shareScreen');
                 if(s) s.classList.add('show'); } }catch(_){}
      };
      tog.appendChild(sp);
    }
  }catch(_){}
}catch(e){} };
window.motDuTemps=function(p){try{
  if(!p)return {mot:'un jour',vif:false,col:''};
/* tenue = le bleu du i de Promi : la seule couleur qu'on gagne */
  if(p.status==='tenu') return {mot:'tenue',vif:true,col:'#8FE08F',clair:true};
  var j=(p.due===undefined||p.due===null)?null:Number(p.due);
  if(p.status==='rate'||(j!==null&&j<0))
    return {mot:'à tenir',vif:true,col:'#DD4D23'};
  if(j===null||isNaN(j)) return {mot:'un jour',vif:false,col:''};
/* EN COURS : aucun aplat, quelle que soit l'echeance. L'etat ordinaire
   n'a rien a crier — c'est ce qui rend le bleu desirable. */
  if(j<=0) return {mot:"aujourd'hui",vif:false,col:''};
  if(j===1) return {mot:'demain',vif:false,col:''};
  if(j<=7){
    var d=new Date(Date.now()+j*86400000);
    var J=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
    return {mot:J[d.getDay()],vif:false,col:''};}
  if(j<=60){
    var d2=new Date(Date.now()+j*86400000);
    var M=['janvier','février','mars','avril','mai','juin','juillet','août',
           'septembre','octobre','novembre','décembre'];
    return {mot:d2.getDate()+' '+M[d2.getMonth()],vif:false,col:''};}
  return {mot:'un jour',vif:false,col:''};
}catch(e){return {mot:'un jour',vif:false,col:''};}};
window._majQpRail=function(){try{
  var r=document.getElementById('shQpRail'); if(!r)return;
  var act=[]; try{act=promises.filter(function(p){return !p.draft&&!p.req;});}catch(_){}
  window.shareHidden=window.shareHidden||{};
  r.innerHTML=act.map(function(p){
    var on=!window.shareHidden[p.id];
    return '<button class="sh-qp'+(on?' on':'')+'" data-qp="'+p.id+'">'
      +String(p.title||'').replace(/[<>&]/g,'')+'</button>';}).join('');
}catch(e){}};
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('#shQpRail .sh-qp'); if(!b)return;
  var id=+b.dataset.qp;
  window.shareHidden=window.shareHidden||{};
  if(window.shareHidden[id])delete window.shareHidden[id];
  else window.shareHidden[id]=true;
  b.classList.toggle('on', !window.shareHidden[id]);
  try{shareToile._key=null; if(window.shareRender)shareRender();}catch(_){}
},true);
try{setTimeout(function(){if(window._majQpRail)_majQpRail();},2800);}catch(e){}
document.addEventListener('click',function(e){
  /* v41 : le Peaufiner du partage refondu (#shcPeaufiner) remplace l'ancien tiroir (#shTrayBtn) — sans lui, le rail
     « QUELS PROMI » restait vide (rempli une seule fois au chargement, avant les Promi) : on ne choisissait plus quoi partager. */
  if(e.target.closest&&e.target.closest('#shTrayBtn,#shcPeaufiner'))
    setTimeout(function(){if(window._majQpRail)_majQpRail();},60);
},true);
window._majFilDot=function(){try{
  var d=document.getElementById('filDot'); if(!d)return;
  /* ⚑ v89 (Tom, Q347) : un seul compteur — ce qui attend un GESTE de moi ; il redescend quand j'agis, jamais quand je regarde */
  d.classList.toggle('on',(window._filAttente?window._filAttente():0)>0);
}catch(e){}};
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('#filBtn'); if(!b)return;
  /* le contenu du Fil vit dans #feedView, pas dans #feedScreen : ouvrir le
     mauvais conteneur donnait un ecran vide et sans fond. */
  try{ if(window.quitteVues)quitteVues();
    if(window.setView){setView('fil');}
    else{var v=document.getElementById('feedView');
      if(v){v.style.display='';v.classList.add('in');}}
    if(window.buildFeed)buildFeed();
    /* v89 (Q347) : ouvrir le Fil n'éteint rien — le compteur redescend quand j'agis, la pastille d'une carte quand je l'ouvre */
    if(window._majFilDot)_majFilDot();
    if(window.updateFeedDot)updateFeedDot();
  }catch(_){}
},true);
try{setTimeout(function(){if(window._majFilDot)_majFilDot();},2600);}catch(e){}
window.KR_R=0.33;   /* rayon de l'axe, en fraction du cote */
window.KR_LW=12/78;  /* ⚑ 23 sept. (Tom) : « la même épaisseur partout ». 12 sur 78, exactement la cote de l'Aura (`K.toi.arc`). C'était 0,21 ici et 8/78 dans le poseur de fiche. */
function drawKRing(cv){auraSync();try{if(window._majAnneauPlus)_majAnneauPlus();}catch(_){}var e=+cv.dataset.e,t=+cv.dataset.t,r=+cv.dataset.r,tot=e+t+r;var g=cv.getContext('2d');if(!g)return;/* geometrie de l'anneau — une seule source de verite, partagee avec _sigBloc :
   KR_R rayon de l'axe · KR_LW epaisseur · le trou vaut KR_R - KR_LW/2 */
var W=cv.width,H=cv.height,cx=W/2,cy=H/2,R=W*window.KR_R,lw=W*window.KR_LW;g.clearRect(0,0,W,H);
/* ⚑ 21 sept. (Tom, moodboard v8) — SUR LA TERRE PRUNE, L'ANNEAU EST CERNÉ D'UN FILET CRÈME.
   « C'est le filet qui le rend lisible sur la terre prune. » Mesuré : le vert profond n'est
   qu'à ΔE 44,6 / Δlum 16,2 de la terre ; le filet crème, lui, est à Δlum 217,3. Il fait
   1,4 px sur 390, de part et d'autre de l'anneau de 5. */
/* ⚑ 22 SEPTEMBRE 2026 (Tom) — LE FILET EST DEHORS. « Le liseré des disques est à
   l'intérieur. Il doit être à l'extérieur — un filet crème #F7F0DE de 1,4 px qui CERNE
   l'anneau, comme le v8 le montre. » Un seul cercle, posé contre le bord EXTÉRIEUR. */
/* ⚑ 23 SEPTEMBRE 2026 (Tom) — « LE LISERÉ FILET CRÈME, C'EST TOUJOURS PAS FAIT MALGRÉ
   PLUSIEURS DEMANDES. » Il l'était, et il ne se voyait pas, pour DEUX raisons :
     ① il était peint EN PREMIER, avant l'anneau — et l'anneau extérieur du Cercle
        (`oR = R + lw·0,74`, `olw = lw·0,40`) repasse exactement dessus ;
     ② il était conditionné à la CLASSE `#detailPoster.f-tenue`, or `drawKRing` est
        appelé HUIT à DOUZE fois par ouverture et les premiers appels arrivent avant
        que la classe soit posée : le dernier appel gagne, et il décidait « pas de
        filet ». C'est le piège du §8 — on ne lit pas un état dans une classe qui
        n'est pas encore là.
   Il est maintenant peint EN DERNIER, et il ne dépend plus d'une classe mais de CE QUI
   EST PEINT SOUS LUI (§3) : fond sombre → filet crème. C'est la même doctrine que le
   reste du produit, et elle couvre d'un coup la terre prune d'une fiche (les deux
   thèmes) et le brun du mode sombre. */
/* ⚑ ET IL EST POSÉ SUR LE DOM, PAS SUR LE CANEVAS — voir `lot-V10-FILET` en fin de
   fichier : un filet peint DANS le canevas se fait recouvrir par la passe suivante, et
   l'anneau extérieur du Cercle repasse exactement dessus. Sur le nœud, rien ne peut le
   défaire. Le bord extérieur de l'anneau EST le bord de son canevas (mesuré : le tracé
   s'arrête à 116 sur 117) : un `box-shadow` de 1,4 px le cerne donc exactement. */
/* ⚑ 23 SEPTEMBRE 2026, second tour — ET IL SE PEINT DANS LA BOÎTE, PAS DEHORS.
   Une troisième écriture avait posé le filet en `box-shadow` sur le nœud. Une ombre
   DÉBORDE de l'élément : toute rangée qui glisse (`.au-nx` en `overflow:auto hidden`,
   `.aura-track` sur la fiche) la coupe net — mesuré en repeignant l'ombre en ROUGE PUR et
   en parcourant les 360° : **96,4 % du tour, un trou de 264 à 277°**, pile au sommet du
   plus grand disque. Et posée depuis une passe EXTÉRIEURE, le peintre l'effaçait au rendu
   suivant (0 % du tour sur une fiche de Nuée).
   Ce qui tient : **le peintre le trace lui-même, en DERNIER, et DANS la boîte**. L'anneau
   finit exactement au bord de son canevas (`R + lw/2 = W/2`, le poseur le garantit) — le
   filet occupe donc ses 1,4 derniers pixels. Rien ne peut le rogner, rien ne le recouvre. */
var _krFilet=(function(){ try{ return !!(window._fondSombreSous && window._fondSombreSous(cv)) && !(window._sansFiletCercle && window._sansFiletCercle(cv)); }
  catch(_){ return false; } })();
/* ⚑ 23 SEPTEMBRE 2026, cinquième écriture (Tom) — « LE FILET DOIT ÊTRE COLLÉ AU BORD
   EXTÉRIEUR DU DISQUE. Aujourd'hui il y a un écart. Il cerne le bord, sans jeu. »
   Il était posé au bord du CANEVAS (`W/2`), pas au bord de l'ANNEAU. Les deux ne coïncident
   que chez le poseur de fiche, qui force `KR_R=(D−EP)/2/D` et `KR_LW=EP/D` : là,
   `R+lw/2 = W/2`, et le filet tombait juste. Partout ailleurs — l'Aura, la fiche d'une
   personne — les constantes globales valent `KR_R .33` et `KR_LW 12/78` : le bord de
   l'anneau est à **0,4069·W**, le filet était à **0,5·W**. Mesuré sur les Noyaux de
   l'Aura (canevas 104) : anneau jusqu'à **42,3**, crème de **50,5 à 51** — **8,2 px de jeu**,
   soit 4,1 px à l'écran. Le filet suit donc LE BORD PEINT (`_krDehors`, que l'anneau
   extérieur du Cercle relève quand il existe), borné au canevas pour ne pas être rogné. */
function _poseFilet(){ return; /* ⚑ v18 : le filet est porté par chaque segment (_arcs) — plus de cercle continu */ if(!_krFilet) return;
  var _bw=(cv.getBoundingClientRect&&cv.getBoundingClientRect().width)||W;
  var _fw=1.4*(W/(_bw||W));
  var _rf=Math.min(_krDehors+_fw/2, W/2-_fw/2);
  g.save(); g.lineWidth=_fw; g.lineCap='butt'; g.strokeStyle=window._FILET_DOUX||'#F7F0DE';
  g.beginPath(); g.arc(cx,cy,_rf,0,6.2832); g.stroke(); g.restore();
  try{ cv.setAttribute('data-filet',[(_krDehors).toFixed(2),_rf.toFixed(2),_fw.toFixed(2)].join(',')); }catch(_){} }
var _krDehors=R+lw/2;   /* le bord EXTERIEUR de ce qui est peint — l'anneau, ou celui du Cercle */
g.lineWidth=lw;g.lineCap='butt';if(tot<=0){var _tk=cv.getAttribute('data-vide')||(_sealDark?'rgba(163,170,196,.34)':'rgba(120,126,150,.30)');g.strokeStyle=_tk;g.beginPath();g.arc(cx,cy,R,0,6.2832);g.stroke();/* contour interieur net : rend le noyau gratuit lisible */g.lineWidth=Math.max(2.5,lw*0.16);g.strokeStyle=_sealDark?'rgba(228,215,187,.9)':'rgba(32,25,8,.82)';g.beginPath();g.arc(cx,cy,R-lw/2+g.lineWidth/2,0,6.2832);g.stroke();g.beginPath();g.arc(cx,cy,R+lw/2-g.lineWidth/2,0,6.2832);g.stroke();return;}/* ⚑ L'ANNEAU DU NOYAU PORTE LES COULEURS D'ÉTAT DU §3, PAS LES SIENNES.
   Il peignait « tenu » en MAUVE #C9A8F5 et « en cours » en BLEU #82AEF8. Trois
   choses le contredisaient, et toutes les trois sont dans le produit :
     · CLAUDE.md §3 — « #8FE08F menthe tenue · neutre periwinkle en cours ·
       #DD4D23 orange à tenir » ;
     · SA PROPRE LÉGENDE, `.klegend` de l'écran Aura, qui écrit déjà
       « #00341A tenues · #A77CF7 en cours · #DD4D23 à tenir » ;
     · le cadre 48 — le Noyau d'une fiche y est un anneau terracotta r 35
       épaisseur 8, recouvert d'un arc MENTHE #8FE08F sur 72 % du tour.
   Le mauve est la couleur d'une NUÉE (§3) : sur un anneau qui dit un état, il
   racontait autre chose. Mesuré au duo : le disque « toi » différait en entier. */
/* ⚑ 21 SEPTEMBRE 2026 (Tom) — L'ANNEAU PORTE LES VALEURS D'ÉTAT v7, ET IL SUIT CE QUI EST
   PEINT SOUS LUI (§3) : sur un fond SOMBRE les claires, sur un fond CLAIR les profondes.
   Les fonds sombres où l'anneau paraît : la TERRE d'une fiche tenue (#2B1020) et la barre
   de l'accueil (#201908) — tous deux sombres dans les deux thèmes. */
/* ⚑ 22 SEPTEMBRE 2026 (Tom) — LES TROIS VALEURS, EXACTEMENT, DANS LES DEUX THÈMES ET SUR
   TOUS LES FONDS. « Aucune teinte dérivée, aucun calcul, aucune transformation. » */
var M=[0,52,26], B=[41,21,71], T=[221,77,35];
var rg=[],cum=0;[[t,M],[e,B],[r,T]].forEach(function(s){if(s[0]<=0)return;var f=s[0]/tot;rg.push({a:cum,b:cum+f,c:s[1]});cum+=f;});
/* ⚑ 23 SEPTEMBRE 2026 (Tom) — « UNIFORMISÉ PARTOUT, NET PROPRE, ESPACE LOGIQUE PARFAIT ENTRE
   TOUS, SANS FIORITURE. » L'anneau d'une fiche ne portait AUCUN jour : ses segments se
   FONDAIENT l'un dans l'autre sur 3 % du tour, peints en 220 arcs. Deux grammaires pour un
   même objet — un fondu ici, un jour là — c'est exactement la fioriture refusée. Il prend
   donc le jour de l'Aura : 3 px D'ARC, converti par le rayon, centré sur midi, n arcs et
   n jours identiques. `KR_JOUR` est la même cote que `JOUR_PX` (§5). */
var _sc=(function(){ try{ var b=cv.getBoundingClientRect(); return (b.width>0)?(W/b.width):1; }catch(_){ return 1; } })();
var KR_JOUR=3*_sc, TAU2=6.283185307;
function _arcs(rgx, RR){
  var GJ=(rgx.length>1)?(KR_JOUR/RR):0;
  for(var i=0;i<rgx.length;i++){
    var a0=-Math.PI/2+rgx[i].a*TAU2+GJ/2, a1=-Math.PI/2+rgx[i].b*TAU2-GJ/2;
    if(a1<=a0) continue;
    g.strokeStyle='rgb('+rgx[i].c.join(',')+')'; g.beginPath(); g.arc(cx,cy,RR,a0,a1); g.stroke();
    /* ⚑ v18 (Tom) : le filet crème ne suit QUE le bord extérieur de chaque segment, et s'interrompt dans les
       écarts ; 1 px. Condition : ce qui est peint SOUS l'anneau (_krFilet). */
    if(_krFilet){ var _fwA=1*_sc, _lw0=g.lineWidth, _Rf=RR+_lw0/2-_fwA/2;
      g.save(); g.lineWidth=_fwA; g.lineCap='butt'; g.strokeStyle=window._FILET_DOUX||'#F7F0DE'; g.beginPath(); g.arc(cx,cy,_Rf,a0,a1); g.stroke(); g.restore(); } }
}
_arcs(rg,R);var _dv=document.getElementById('device');if(_dv&&_dv.classList.contains('premium')&&cv.dataset.oe!==undefined){var oe=+cv.dataset.oe,ot=+cv.dataset.ot,orr=+cv.dataset.or,otot=oe+ot+orr;if(otot>0){function olp(a,b,k){k=Math.max(0,Math.min(1,k));return 'rgb('+Math.round(a[0]+(b[0]-a[0])*k)+','+Math.round(a[1]+(b[1]-a[1])*k)+','+Math.round(a[2]+(b[2]-a[2])*k)+')';}var oR=R+lw*0.74,olw=lw*0.40;g.lineWidth=olw;g.lineCap='butt';g.strokeStyle=_sealDark?'rgba(163,170,196,.24)':'rgba(120,126,150,.22)';g.beginPath();g.arc(cx,cy,oR,0,6.2832);g.stroke();var org2=[],ocum=0;[[ot,M],[oe,B],[orr,T]].forEach(function(s){if(s[0]<=0)return;var f=s[0]/otot;org2.push({a:ocum,b:ocum+f,c:s[1]});ocum+=f;});_arcs(org2,oR);_krDehors=Math.max(_krDehors,oR+olw/2);}}g.save();g.beginPath();g.arc(cx,cy,R+lw/2,0,6.2832);g.arc(cx,cy,R-lw/2,0,6.2832,true);g.clip();_grain(g,W,H,0.6);g.restore();_poseFilet();}
function openPerson(name){if(!name)return;var items=promises.filter(function(p){return !p.draft&&(p.who===name||p.from===name);});var theirs=items.filter(function(p){return p.from===name;});var yours=items.filter(function(p){return (!p.from||p.from==='moi')&&p.who===name;});function _pc(a){var t=a.filter(function(p){return p.status==='tenu';}).length,r=a.filter(function(p){return p.status==='rate';}).length;return (t+r)>0?Math.round(100*t/(t+r)):null;}var theirTrust=_pc(theirs),yourTrust=_pc(yours);var enc=theirs.filter(function(p){return p.status==='encours';}).length,tenu=theirs.filter(function(p){return p.status==='tenu';}).length,rate=theirs.filter(function(p){return p.status==='rate';}).length;var yE=yours.filter(function(p){return p.status==='encours';}).length,yT=yours.filter(function(p){return p.status==='tenu';}).length,yR=yours.filter(function(p){return p.status==='rate';}).length;var aE=enc+yE,aT=tenu+yT,aR=rate+yR;var av=$('#psAva');if(av){if(_isMe(name)&&USER.photo){av.style.background='center/cover url('+USER.photo+')';}else{av.style.background=_blobBg(_isMe(name)?('u'+USER.seed):name);}av.textContent='';av.classList.add('ava-blob');}var nm=$('#psName');if(nm)nm.textContent=name;var allTrust=(aT+aR)>0?Math.round(100*aT/(aT+aR)):null;var sub=$('#psSub');if(sub){var _pp=['harmonie à deux : '+harmonyWord(allTrust)];if(yourTrust!=null)_pp.push('ta parole : '+harmonyWord(yourTrust));sub.textContent=_pp.join(' · ');}var sp=$('#psSpark');if(sp)sp.innerHTML=personSpark(name);var rg=$('#psRing');if(rg)rg.innerHTML=karmaRing(yE,yT,yR);var _cnt='<div class="b" style="opacity:.65;padding:0 0 8px">'+items.length+' Promi \u00e9chang\u00e9'+(items.length>1?'s':'')+' \u00b7 '+theirs.length+' re\u00e7u'+(theirs.length!==1?'s':'')+' \u00b7 '+yours.length+' donn\u00e9'+(yours.length!==1?'s':'')+'</div>';var lst=$('#psList');if(lst){lst.innerHTML=items.length?(_cnt+items.map(function(p){var st=STLAB[p.status]||p.status;return '<div class="row" data-id="'+p.id+'">'+bullet(p)+'<div><div class="a">'+_esc(p.title)+'</div><div class="b">'+relLabel(p)+' \u00b7 '+st+(p.nuee?' \u00b7 '+_esc(NUE[p.nuee]||p.nuee):'')+'</div></div><div class="chev">\u203a</div></div>';}).join('')):'<div class="b" style="padding:12px 0">aucun Promi pour l\'instant</div>';$$('#psList .row[data-id]').forEach(function(r){r.onclick=function(){closeAll();openDetail(+r.dataset.id);};});}var _selfP=/^moi/i.test(name);var _mirHTML;if(_selfP){_mirHTML='<div class="ps-mir"><div class="kr-wrap">'+karmaRing(yE,yT,yR,66)+'</div></div><div class="ps-curve"><div class="ps-clab">comment ça évolue</div>'+personSpark(name)+'</div>';}else{var _eqH='';if(yourTrust!=null&&theirTrust!=null){var _dd=yourTrust-theirTrust,_pp2=Math.round(50-Math.max(-42,Math.min(42,_dd*0.7))),_ww=Math.abs(_dd)<10?'le lien est r\u00e9ciproque \u273f':(_dd>0?'tu portes un peu plus':'ils portent un peu plus');_eqH='<div class="ps-eq prem-only"><div class="eq-track"><span class="eq-end">Toi<b>'+yourTrust+'%</b></span><div class="eq-line"><div class="eq-mark" style="left:'+_pp2+'%"></div></div><span class="eq-end">eux<b>'+theirTrust+'%</b></span></div><div class="eq-phrase">'+_ww+'</div></div>';}_mirHTML='<div class="ps-mir"><div class="kr-duo"><div class="kr-one kr-toi">'+karmaRing(yE,yT,yR,66)+'<span class="kr-side">Toi</span></div><div class="kr-one kr-eux">'+karmaRing(enc,tenu,rate,66)+'<span class="kr-side">'+_esc(name)+'</span></div></div></div><div class="ps-mleg prem-only"><span><i class="ppl ppl-toi"></i>toi envers eux</span><span><i class="ppl ppl-eux"></i>eux envers toi</span></div>'+_eqH+'<div class="ps-curve"><div class="ps-clab">comment ça évolue</div>'+personSpark(name)+'</div>';}var _psm=$('#psMirror');if(_psm)_psm.innerHTML=_mirHTML+'<div class="ps-leg3"><span><i style="background:#291547"></i>en cours</span><span><i style="background:#00341A"></i>tenues</span><span><i style="background:#DD4D23"></i>à tenir</span></div>';openSheet($('#personSheet'));try{document.querySelectorAll('#personSheet .kr-c').forEach(function(cv){try{drawKRing(cv);}catch(e){}});document.querySelectorAll('#personSheet .spk').forEach(function(cv){try{drawSpk(cv);}catch(e){}});}catch(e){}}
var _socArr=[],_socRAF=null,_socLast=0,_socPhase=0;
function karmaCircle(){var act=promises.filter(function(p){return !p.draft;});var names={};function acc(n){if(!n||n==='moi'||n==='le groupe')return null;if(!names[n])names[n]={name:n,theirT:0,theirR:0,theirE:0,yourT:0,yourR:0,yourE:0};return names[n];}act.forEach(function(p){if(p.from&&p.from!=='moi'){var o=acc(p.from);if(o){if(p.status==='tenu')o.theirT++;else if(p.status==='rate')o.theirR++;else o.theirE++;}}if((!p.from||p.from==='moi')&&p.who&&p.who!=='moi'&&p.who!=='le groupe'){var o2=acc(p.who);if(o2){if(p.status==='tenu')o2.yourT++;else if(p.status==='rate')o2.yourR++;else o2.yourE++;}}});var arr=Object.keys(names).map(function(k){return names[k];});arr.forEach(function(o){var tr=o.theirT+o.theirR;o.theirTrust=tr>0?o.theirT/tr:null;var yr=o.yourT+o.yourR;o.yourTrust=yr>0?o.yourT/yr:null;var _mk=o.theirT+o.yourT,_mr=o.theirR+o.yourR;o.mutTrust=(_mk+_mr)>0?_mk/(_mk+_mr):null;o.trust=o.mutTrust;o.yourTot=o.yourT+o.yourR+o.yourE;o.tot=o.theirT+o.theirR+o.theirE+o.yourTot;});arr.sort(function(a,b){var ta=a.trust==null?-1:a.trust,tb=b.trust==null?-1:b.trust;if(tb!==ta)return tb-ta;return b.tot-a.tot;});return arr;}
function _kcol(t){if(t==null)return '#A2947C';return t>=0.65?'#C9A8F5':(t>=0.45?'#82AEF8':'#DD4D23');}
function _vclip(poly,a,b,c){var out=[],n=poly.length;for(var i=0;i<n;i++){var cur=poly[i],nx=poly[(i+1)%n];var dc=a*cur[0]+b*cur[1]-c,dn=a*nx[0]+b*nx[1]-c;if(dc<=1e-9)out.push(cur);if((dc<=0)!==(dn<=0)){var t=dc/(dc-dn);out.push([cur[0]+t*(nx[0]-cur[0]),cur[1]+t*(nx[1]-cur[1])]);}}return out;}
function _vcell(sites,i,box){var poly=box.slice();var xi=sites[i][0],yi=sites[i][1];for(var j=0;j<sites.length;j++){if(j===i)continue;var xj=sites[j][0],yj=sites[j][1];poly=_vclip(poly,2*(xj-xi),2*(yj-yi),(xj*xj+yj*yj-xi*xi-yi*yi));if(!poly.length)break;}return poly;}
function _vinset(poly,f){if(!poly.length)return poly;var cx=0,cy=0;poly.forEach(function(p){cx+=p[0];cy+=p[1];});cx/=poly.length;cy/=poly.length;return poly.map(function(p){return [cx+(p[0]-cx)*f,cy+(p[1]-cy)*f];});}
function _vpath(poly){if(!poly.length)return '';var d='M '+poly[0][0].toFixed(1)+' '+poly[0][1].toFixed(1);for(var i=1;i<poly.length;i++)d+=' L '+poly[i][0].toFixed(1)+' '+poly[i][1].toFixed(1);return d+' Z';}
function buildAuraToile(){var el=$('#ktoile');if(!el)return;var arr=karmaCircle();if(!arr.length){el.innerHTML='<div class="b" style="padding:12px 0;color:var(--gsub)">tes proches appara\u00eetront ici</div>';return;}var box=[[10,10],[310,10],[310,248],[10,248]];var cx=160,cy=128;var sites=[[cx,cy]];var meta=[{me:true}];var n=arr.length;arr.forEach(function(o,k){var ang=-Math.PI/2+k/n*2*Math.PI;sites.push([cx+78*Math.cos(ang),cy+72*Math.sin(ang)]);meta.push({me:false,o:o});});var s='<svg viewBox="0 0 320 258" style="width:100%;display:block">';for(var i=0;i<sites.length;i++){var cell=_vinset(_vcell(sites,i,box),0.9);var m=meta[i];var c=m.me?'#82AEF8':_kcol(m.o.trust);var op=m.me?0.85:(0.3+0.5*m.o.trust);s+='<path class="ktoile-cell" data-p="'+(m.me?'':_esc(m.o.name))+'" style="cursor:pointer" d="'+_vpath(cell)+'" fill="'+c+'" fill-opacity="'+op.toFixed(2)+'" stroke="'+c+'" stroke-width="1.3" stroke-linejoin="round"/>';var lx=sites[i][0],ly=sites[i][1];s+='<text x="'+lx.toFixed(0)+'" y="'+(ly+(m.me?2:-1)).toFixed(0)+'" text-anchor="middle" font-family="var(--f-libelle)" font-weight="600" font-size="'+(m.me?15:12)+'" fill="'+((m.me||(m.o&&m.o.trust>=0.82))?'#fff':'#E4D7BB')+'">'+(m.me?'TOI':_esc(_ini(m.o.name)))+'</text>';if(!m.me)s+='<text x="'+lx.toFixed(0)+'" y="'+(ly+12).toFixed(0)+'" text-anchor="middle" font-family="var(--f-texte)" font-size="8" fill="#fff" fill-opacity=".85">'+_esc(m.o.name.toUpperCase())+' '+Math.round(m.o.trust*100)+'%</text>';}s+='</svg>';el.innerHTML=s;el.onclick=function(e){var p=e.target&&e.target.closest?e.target.closest('.ktoile-cell'):null;if(p&&p.getAttribute('data-p'))openPerson(p.getAttribute('data-p'));};}
var _socEls=[];
function renderCercleSocial(){var el=$('#ksocial');if(!el){_socEls=[];return;}var arr=_socArr;if(!arr||!arr.length){el.innerHTML='<div class="b" style="padding:12px 0;color:var(--gsub)">invite ou promets \u00e0 quelqu\'un pour voir tes proches</div>';_socEls=[];return;}var cx=160,cy=140,n=arr.length;var s='<svg viewBox="0 0 320 290" style="width:100%;display:block">';[58,90,120].forEach(function(rr){s+='<circle cx="160" cy="140" r="'+rr+'" fill="none" stroke="#ffffff" stroke-opacity=".06"/>';});arr.forEach(function(o,k){var a0=-Math.PI/2+k/n*2*Math.PI+0.12;var tv=(o.trust==null?0.5:o.trust);var rad=32+(1-tv)*98;var br=11+o.tot*1.5;var x=cx+rad*Math.cos(a0),y=cy+rad*Math.sin(a0);var c=_kcol(o.trust);s+='<g class="orb-node" data-p="'+_esc(o.name)+'" data-a="'+a0.toFixed(4)+'" data-r="'+rad.toFixed(1)+'" data-br="'+br.toFixed(1)+'" style="cursor:pointer">';s+='<line x1="160" y1="140" x2="'+x.toFixed(1)+'" y2="'+y.toFixed(1)+'" stroke="'+c+'" stroke-width="1" opacity=".18"/>';s+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+br.toFixed(1)+'" fill="'+c+'" fill-opacity="'+(0.28+0.5*tv).toFixed(2)+'" stroke="'+c+'" stroke-width="1.4"/>';s+='<text x="'+x.toFixed(1)+'" y="'+(y+3).toFixed(1)+'" text-anchor="middle" font-family="var(--f-libelle)" font-weight="600" font-size="11" fill="'+(o.trust>=0.82?'#fff':'#E4D7BB')+'">'+_esc(_ini(o.name))+'</text>';s+='<text x="'+x.toFixed(1)+'" y="'+(y+br+11).toFixed(1)+'" text-anchor="middle" font-family="var(--f-texte)" font-size="8" fill="#A2947C">'+_esc(o.name.toUpperCase())+' '+(o.trust==null?'—':Math.round(o.trust*100)+'%')+'</text>';s+='</g>';});s+='<circle cx="160" cy="140" r="16" fill="#82AEF8"/><text x="160" y="143.5" text-anchor="middle" font-family="var(--f-libelle)" font-weight="600" font-size="10" fill="#fff">TOI</text>';s+='</svg>';el.innerHTML=s;_socEls=Array.prototype.slice.call(el.querySelectorAll('.orb-node')).map(function(g){var ch=g.children;return {g:g,line:g.querySelector('line'),disc:g.querySelector('circle'),t1:ch[2],t2:ch[3],a:parseFloat(g.getAttribute('data-a')),r:parseFloat(g.getAttribute('data-r')),br:parseFloat(g.getAttribute('data-br'))};});el.onclick=function(e){var g=(e.target&&e.target.closest)?e.target.closest('.orb-node'):null;if(g&&g.getAttribute)openPerson(g.getAttribute('data-p'));};}
function spinStep(phase){var cx=160,cy=140;for(var k=0;k<_socEls.length;k++){var o=_socEls[k];var ang=o.a+phase;var x=cx+o.r*Math.cos(ang),y=cy+o.r*Math.sin(ang);var br=o.br*(1+0.06*Math.sin(phase*7+k));if(o.line){o.line.setAttribute('x2',x.toFixed(1));o.line.setAttribute('y2',y.toFixed(1));}if(o.disc){o.disc.setAttribute('cx',x.toFixed(1));o.disc.setAttribute('cy',y.toFixed(1));o.disc.setAttribute('r',br.toFixed(1));}if(o.t1){o.t1.setAttribute('x',x.toFixed(1));o.t1.setAttribute('y',(y+3).toFixed(1));}if(o.t2){o.t2.setAttribute('x',x.toFixed(1));o.t2.setAttribute('y',(y+br+11).toFixed(1));}}}
function orbitLoop(ts){var sc=$('#auraScreen');if(!sc||!sc.classList.contains('show')||!_socEls.length){_socRAF=null;return;}if(!_socLast)_socLast=ts;if(ts-_socLast>40){_socLast=ts;_socPhase+=0.006;spinStep(_socPhase);}_socRAF=requestAnimationFrame(orbitLoop);}
function buildAuraSocial(){_socArr=karmaCircle();_socPhase=0;renderCercleSocial();try{if(!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)){if(!_socRAF)_socRAF=requestAnimationFrame(orbitLoop);}}catch(e){}}
function personSpark(name){var items=promises.filter(function(p){return !p.draft&&(p.who===name||p.from===name)&&p.status!=='encours';});items.sort(function(a,b){return a.id-b.id;});var W=132,H=30,pts=[],kept=0;if(items.length>=2){items.forEach(function(p,i){if(p.status==='tenu')kept++;pts.push(kept/(i+1));});}else{var _t=promises.filter(function(p){return !p.draft&&(p.who===name||p.from===name)&&p.status==='tenu';}).length,_r=promises.filter(function(p){return !p.draft&&(p.who===name||p.from===name)&&p.status==='rate';}).length;var _kp=(_t+_r)>0?_t/(_t+_r):0.6;var _bs=Math.max(0.12,_kp-0.28);for(var _q=0;_q<7;_q++)pts.push(_bs+(_kp-_bs)*(_q/6));}var d='';pts.forEach(function(v,i){var x=(pts.length>1?i/(pts.length-1):0)*W;var y=H-4-v*(H-8);d+=(i?' L ':'M ')+x.toFixed(1)+' '+y.toFixed(1);});var last=pts[pts.length-1];var lx=W,ly=H-4-last*(H-8);return '<svg viewBox="0 0 '+(W+6)+' '+H+'" width="'+(W+6)+'" height="'+H+'"><path d="'+d+'" fill="none" stroke="#A2947C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0.7"/><circle cx="'+lx.toFixed(1)+'" cy="'+ly.toFixed(1)+'" r="2.6" fill="#C9A8F5"/></svg>';}
function _cdate(iso){try{var d=new Date(iso);var mo=['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'];return d.getDate()+' '+mo[d.getMonth()]+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');}catch(e){return '';}}
var _sealCanvas=null,_sealFmt='square',_sealParts={noyau:true,pelote:false,prometteurs:false,disques:false};var _sealAspectOverride=0;var _shShowQR=false;var _sealDark=true,_INK='#E4D7BB',_SUB='#A2947C',_HAIR='rgba(255,255,255,.30)',_sealShowPct=false,_sealShowBalance=false;
var SEAL_FMTS={story:{a:0.5625},square:{a:1},post:{a:0.8}};
function _sealWaves(g,W,H){var cols=['#82AEF8','#C9A8F5','#DD4D23'];for(var k=0;k<9;k++){var col=cols[k%3];var amp=W*0.028+k*W*0.010;var yb=H*(0.07+k*0.105);var ph=k*1.4;g.beginPath();for(var x=0;x<=W;x+=4){var y=yb+Math.sin(x*0.008+ph)*amp+Math.sin(x*0.0032-ph*0.7)*amp*0.5;if(x===0)g.moveTo(x,y);else g.lineTo(x,y);}g.strokeStyle=col;g.globalAlpha=0.115;g.lineWidth=Math.max(1,W*0.0016);g.stroke();}g.globalAlpha=1;try{var vg=g.createRadialGradient(W/2,H*0.46,W*0.18,W/2,H*0.46,W*0.8);vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,.34)');g.fillStyle=vg;g.fillRect(0,0,W,H);}catch(e){}}
function _harmGradCanvas(g,cx,cy,r,w,tenu,enc,rate,M,Cc,O){var tot=tenu+enc+rate;g.lineCap='butt';if(tot<=0){g.strokeStyle=_HAIR;g.lineWidth=w;g.beginPath();g.arc(cx,cy,r,0,2*Math.PI);g.stroke();return;}var cum=0,bands=[];[[tenu,M],[enc,Cc],[rate,O]].forEach(function(x){if(x[0]>0){bands.push({c:x[1],s:cum/tot,e:(cum+x[0])/tot});}cum+=x[0];});var tw=0.035,stops=[];bands.forEach(function(bd){var twb=Math.min(tw,(bd.e-bd.s)*0.34);stops.push([bd.s+twb,bd.c]);stops.push([bd.e-twb,bd.c]);});function hx(hh){hh=hh.replace('#','');return [parseInt(hh.slice(0,2),16),parseInt(hh.slice(2,4),16),parseInt(hh.slice(4,6),16)];}function mix(a,b,t){var x=hx(a),y=hx(b);return 'rgb('+Math.round(x[0]+(y[0]-x[0])*t)+','+Math.round(x[1]+(y[1]-x[1])*t)+','+Math.round(x[2]+(y[2]-x[2])*t)+')';}var nS=stops.length;function colAt(f){for(var i=0;i<nS;i++){var p0=stops[i][0],c0=stops[i][1],p1=stops[(i+1)%nS][0],c1=stops[(i+1)%nS][1];if(i===nS-1){var seg=1-p0+stops[0][0];if(f>=p0)return mix(c0,c1,(f-p0)/seg);if(f<stops[0][0])return mix(c0,c1,(f+1-p0)/seg);}else if(f>=p0&&f<p1){return mix(c0,c1,(f-p0)/((p1-p0)||1));}}return bands[0].c;}var N=210;g.lineWidth=w;for(var k=0;k<N;k++){var f=k/N;var a0=-Math.PI/2+f*2*Math.PI;var a1=-Math.PI/2+(k+1)/N*2*Math.PI+0.004;g.strokeStyle=colAt(f);g.beginPath();g.arc(cx,cy,r,a0,a1);g.stroke();}}
function drawEmblem(g,cx,cy,sc){var act=promises.filter(function(p){return !p.draft;});var tenu=act.filter(function(p){return p.status==='tenu';}).length,enc=act.filter(function(p){return p.status==='encours';}).length,rate=act.filter(function(p){return p.status==='rate';}).length;var tot=tenu+enc+rate;var res=tenu+rate;var pctDisp=res>0?(''+Math.round(100*tenu/res)):'\u2014';auraSync();var C='#82AEF8',M=(_sealDark?'#C9A8F5':'#9876CE'),O='#DD4D23';var hist=act.slice().sort(function(a,b){return a.id-b.id;});var n=hist.length||1;var rseq=hist.filter(function(p){return p.status==='tenu'||p.status==='rate';});var streak=0;for(var q=rseq.length-1;q>=0;q--){if(rseq[q].status==='tenu')streak++;else break;}/* ⚑ 23 SEPTEMBRE 2026 (Tom) — « FLOUTE, SUR UN MINI MINI LISERÉ SUBTIL, LES CONTOURS DU
   NOYAU POUR LE RENDRE VISIBLE ; MINI LISERÉ FLOU, MOINS D'UN MILLIMÈTRE, MÊME PAS LA
   MOITIÉ, SUBTIL. » Sur la Toile de l'image partagée, le Noyau se confondait avec la
   matière. Un halo net serait une ombre portée — l'un des trois interdits du « cheap ».
   On pose donc un liseré FLOU : un cercle de la couleur du fond, tracé à 2 px, avec un
   flou de 6 (sur 1080 de large : 0,3 mm à l'impression). Il détache la forme sans se voir. */
g.save();g.translate(cx,cy);g.scale(sc,sc);g.translate(-120,-120);
try{ g.save(); g.shadowColor=_sealDark?'rgba(0,0,0,.55)':'rgba(255,255,255,.72)';
  g.shadowBlur=6/Math.max(0.0001,sc); g.lineWidth=2/Math.max(0.0001,sc);
  g.strokeStyle=_sealDark?'rgba(0,0,0,.28)':'rgba(255,255,255,.34)';
  g.beginPath(); g.arc(120,120,104,0,2*Math.PI); g.stroke(); g.restore(); }catch(_){}
g.lineCap='round';hist.forEach(function(p,i){var a=-Math.PI/2+i/n*2*Math.PI;var col=p.status==='tenu'?M:(p.status==='rate'?O:C);var e2=p.status==='encours';/* une ONDE plutot qu'un cercle : deux sinusoides dephasees donnent une
   respiration organique. La graine vient de l'identifiant du Promi, donc
   la forme est stable d'un rendu a l'autre. */
var _ph=((p.id*2654435761)>>>0)%1000/1000;
var _on=Math.sin(i/n*2*Math.PI*3+_ph*6.283)*0.5+Math.sin(i/n*2*Math.PI*7-_ph*4.1)*0.28;
var _base=p.status==='tenu'?120:(p.status==='rate'?111:108);
var r0=104+_on*3, r1=_base+_on*11+_ph*4;g.strokeStyle=col;g.lineWidth=(e2?1.4:2.6);g.globalAlpha=(e2?0.42:0.95);g.beginPath();g.moveTo(120+r0*Math.cos(a),120+r0*Math.sin(a));g.lineTo(120+r1*Math.cos(a),120+r1*Math.sin(a));g.stroke();});g.globalAlpha=1;g.strokeStyle=_HAIR;g.lineWidth=17;g.beginPath();g.arc(120,120,80,0,2*Math.PI);g.stroke();_harmGradCanvas(g,120,120,80,16,tenu,enc,rate,M,C,O);g.restore();g.textAlign='center';g.textBaseline='middle';/* ⚑ 23 SEPTEMBRE 2026 (Tom) — LE NOYAU PARTAGÉ NE PORTE NI SCORE NI COMMENTAIRE.
   « Supprime les commentaires ou autres éléments de score type "solide" — on a enlevé tout
     ça ; en payant comme en gratuit ça marche pas pour partager, ça fait nul. »
   Le pourcentage et le mot d'harmonie sortent de l'emblème. Il ne reste que l'anneau et
   ses arcs : la forme dit ce qu'elle a à dire, sans le chiffrer. C'est la même décision
   que « score » dans les termes bannis du §2. */
var ynext=30;if(_sealShowPct&&pctDisp!=='\u2014'){ynext=47;}}
function drawRayonsRetires(g,cx,cy,D){var arr=(typeof karmaCircle==='function')?karmaCircle():[];var R=D/2;[0.48,0.75,1.0].forEach(function(fr){g.beginPath();g.arc(cx,cy,R*fr,0,2*Math.PI);g.strokeStyle=_HAIR;g.lineWidth=Math.max(1,D*0.004);g.stroke();});var n=arr.length||1;g.textAlign='center';g.textBaseline='middle';arr.forEach(function(o,k){var tv=(o.trust==null?0.5:o.trust);var ang=-Math.PI/2+k/n*2*Math.PI+0.12;var rad=R*(0.28+(1-tv)*0.72);var x=cx+rad*Math.cos(ang),y=cy+rad*Math.sin(ang);var col=_kcol(o.trust);var r=D*0.028+o.tot*D*0.006;g.strokeStyle=col;g.globalAlpha=0.18;g.lineWidth=Math.max(1,D*0.003);g.beginPath();g.moveTo(cx,cy);g.lineTo(x,y);g.stroke();g.globalAlpha=0.3+0.5*tv;g.fillStyle=col;g.beginPath();g.arc(x,y,r,0,2*Math.PI);g.fill();g.globalAlpha=1;g.strokeStyle=col;g.lineWidth=Math.max(1,D*0.004);g.stroke();g.fillStyle=(o.theirTrust!=null&&o.theirTrust>=0.82)?(_sealDark?'#fff':'#111'):_INK;g.font='700 '+(D*0.034).toFixed(0)+'px Gilbert,system-ui,sans-serif';g.fillText(_ini(o.name),x,y);});g.fillStyle='#82AEF8';g.beginPath();g.arc(cx,cy,D*0.058,0,2*Math.PI);g.fill();g.fillStyle='#fff';g.font='700 '+(D*0.03).toFixed(0)+'px Gilbert,system-ui,sans-serif';g.fillText('TOI',cx,cy);}
function drawPartnersCanvas(g,W,yTop,slotH){var arr=((typeof karmaCircle==='function')?karmaCircle():[]).filter(function(o){return o.theirTrust!=null;}).sort(function(a,b){return b.theirTrust-a.theirTrust;}).slice(0,3);g.textAlign='center';g.textBaseline='middle';g.fillStyle=_SUB;g.font='500 '+Math.round(W*0.026)+'px Atkinson,system-ui,sans-serif';g.fillText('MES PROMITTEURS',W/2,yTop+slotH*0.13);if(!arr.length){g.fillStyle=_SUB;g.font='500 '+Math.round(W*0.03)+'px Atkinson,system-ui,sans-serif';g.fillText('personne ne t\u2019a encore tenu parole',W/2,yTop+slotH*0.5);return;}var lx=W*0.18,rx=W*0.82;var rowH=Math.min(slotH*0.22,W*0.11);var startY=yTop+slotH*0.36;arr.forEach(function(o,i){var y=startY+i*rowH;g.fillStyle='rgba(130,174,248,.2)';g.beginPath();g.arc(lx+rowH*0.4,y,rowH*0.34,0,2*Math.PI);g.fill();g.fillStyle=(_sealDark?'#291547':'#2F3ED6');g.textAlign='center';g.font='700 '+(rowH*0.32).toFixed(0)+'px Atkinson,system-ui,sans-serif';g.fillText(_ini(o.name),lx+rowH*0.4,y);g.fillStyle=_INK;g.textAlign='left';g.font='500 '+(rowH*0.36).toFixed(0)+'px Atkinson,system-ui,sans-serif';g.fillText(o.name,lx+rowH*0.95,y);g.fillStyle=_INK;g.textAlign='right';g.font='700 '+(rowH*0.4).toFixed(0)+'px Gilbert,system-ui,sans-serif';g.fillText(Math.round(o.theirTrust*100)+'%',rx,y);});}
function drawDisquesCanvas(g,W,yTop,slotH){var arr=((typeof karmaCircle==='function')?karmaCircle():[]).filter(function(o){return (o.theirT+o.theirR+o.theirE+o.yourT+o.yourR+o.yourE)>0;}).sort(function(a,b){return (b.theirT+b.theirR+b.theirE+b.yourT+b.yourR+b.yourE)-(a.theirT+a.theirR+a.theirE+a.yourT+a.yourR+a.yourE);}).slice(0,3);g.textAlign='center';g.textBaseline='middle';if(!arr.length){g.fillStyle=_SUB;g.font='500 '+Math.round(W*0.03)+'px Atkinson,system-ui,sans-serif';g.fillText('tu n\u2019as encore rien promis',W/2,yTop+slotH*0.5);return;}auraSync();var C='#82AEF8',M=(_sealDark?'#C9A8F5':'#9876CE'),O='#DD4D23';var n=arr.length,cw=W/n,cyD=yTop+slotH*0.44,R=Math.min(cw*0.24,slotH*0.24);arr.forEach(function(o,i){var cx=cw*(i+0.5);var tot=o.theirT+o.theirR+o.theirE+o.yourT+o.yourR+o.yourE;var Np=12,acc=[],cum=0;[[o.theirT+o.yourT,M],[o.theirE+o.yourE,C],[o.theirR+o.yourR,O]].forEach(function(x){cum+=x[0];acc.push([tot>0?cum/tot:0,x[1]]);});for(var k=0;k<Np;k++){var f=k/Np,col=O;if(tot>0){for(var j=0;j<acc.length;j++){if(f<acc[j][0]){col=acc[j][1];break;}}}else col=_HAIR;var a=-Math.PI/2+f*2*Math.PI;g.fillStyle=col;g.beginPath();g.arc(cx+R*Math.cos(a),cyD+R*Math.sin(a),R*0.17,0,2*Math.PI);g.fill();}g.fillStyle=_INK;g.textBaseline='middle';g.font='600 '+(R*0.34).toFixed(0)+'px Atkinson,system-ui,sans-serif';g.fillText(o.name,cx,cyD+R+R*0.7);});}
function qrGen(text,ecl){var EXP=new Array(256),LOG=new Array(256);for(var i=0,x=1;i<256;i++){EXP[i]=x;LOG[x]=i;x<<=1;if(x&0x100)x^=0x11D;}function gmul(a,b){return (a===0||b===0)?0:EXP[(LOG[a]+LOG[b])%255];}function rsGen(deg){var p=[1];for(var i=0;i<deg;i++){var np=new Array(p.length+1).fill(0);for(var j=0;j<p.length;j++){np[j]^=gmul(p[j],1);np[j+1]^=gmul(p[j],EXP[i]);}p=np;}return p;}function rsEnc(data,ecLen){var gen=rsGen(ecLen);var res=new Array(ecLen).fill(0);for(var i=0;i<data.length;i++){var f=data[i]^res[0];res.shift();res.push(0);if(f!==0)for(var j=0;j<ecLen;j++)res[j]^=gmul(gen[j+1],f);}return res;}var ECBLK={L:[[0],[7,1,19,0,0],[10,1,34,0,0],[15,1,55,0,0],[20,1,80,0,0],[26,1,108,0,0],[18,2,68,0,0],[20,2,78,0,0],[24,2,97,0,0],[30,2,116,0,0],[18,2,68,2,69]],M:[[0],[10,1,16,0,0],[16,1,28,0,0],[26,1,44,0,0],[18,2,32,0,0],[24,2,43,0,0],[16,4,27,0,0],[18,4,31,0,0],[22,2,38,2,39],[22,3,36,2,37],[26,4,43,1,44]],Q:[[0],[13,1,13,0,0],[22,1,22,0,0],[18,2,17,0,0],[26,2,24,0,0],[18,2,15,2,16],[24,4,19,0,0],[18,2,14,4,15],[22,4,18,2,19],[20,4,16,4,17],[24,6,19,2,20]],H:[[0],[17,1,9,0,0],[28,1,16,0,0],[22,2,13,0,0],[16,4,9,0,0],[22,2,11,2,12],[28,4,15,0,0],[26,4,13,1,14],[26,4,14,2,15],[24,4,12,4,13],[28,6,15,2,16]]};var bytes=[];for(var i=0;i<text.length;i++){var c=text.charCodeAt(i);if(c<128)bytes.push(c);else if(c<2048){bytes.push(192|(c>>6),128|(c&63));}else{bytes.push(224|(c>>12),128|((c>>6)&63),128|(c&63));}}var ver=0,ecb;for(var v=1;v<=10;v++){ecb=ECBLK[ecl][v];var dataCW=ecb[1]*ecb[2]+ecb[3]*ecb[4];var cci=(v<10)?8:16;var need=Math.ceil((4+cci+bytes.length*8)/8);if(need<=dataCW){ver=v;break;}}if(!ver)throw new Error('too long');ecb=ECBLK[ecl][ver];var dataCW=ecb[1]*ecb[2]+ecb[3]*ecb[4];var bits=[];function put(val,len){for(var i=len-1;i>=0;i--)bits.push((val>>i)&1);}put(4,4);put(bytes.length,(ver<10)?8:16);for(var i=0;i<bytes.length;i++)put(bytes[i],8);var cap=dataCW*8;if(bits.length+4<=cap)put(0,4);while(bits.length%8!==0)bits.push(0);while(bits.length<cap){put(236,8);if(bits.length<cap)put(17,8);}var dcw=[];for(var i=0;i<bits.length;i+=8){var b=0;for(var j=0;j<8;j++)b=(b<<1)|bits[i+j];dcw.push(b);}var blocks=[],ecLen=ecb[0];var idx=0;var struct=[];for(var i=0;i<ecb[1];i++)struct.push(ecb[2]);for(var i=0;i<ecb[3];i++)struct.push(ecb[4]);for(var i=0;i<struct.length;i++){var d=dcw.slice(idx,idx+struct[i]);idx+=struct[i];blocks.push({d:d,e:rsEnc(d,ecLen)});}var maxD=Math.max.apply(null,struct);var finalCW=[];for(var i=0;i<maxD;i++)for(var b=0;b<blocks.length;b++)if(i<blocks[b].d.length)finalCW.push(blocks[b].d[i]);for(var i=0;i<ecLen;i++)for(var b=0;b<blocks.length;b++)finalCW.push(blocks[b].e[i]);var size=17+ver*4;var mod=[],rsv=[];for(var i=0;i<size;i++){mod.push(new Array(size).fill(0));rsv.push(new Array(size).fill(0));}function place(r,c,vv){mod[r][c]=vv?1:0;rsv[r][c]=1;}function finder(r,c){for(var i=-1;i<=7;i++)for(var j=-1;j<=7;j++){var rr=r+i,cc=c+j;if(rr<0||rr>=size||cc<0||cc>=size)continue;var vv=(i>=0&&i<=6&&(j===0||j===6))||(j>=0&&j<=6&&(i===0||i===6))||(i>=2&&i<=4&&j>=2&&j<=4);place(rr,cc,vv);}}finder(0,0);finder(0,size-7);finder(size-7,0);for(var i=8;i<size-8;i++){place(6,i,i%2===0);place(i,6,i%2===0);}var AP=[[],[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50]];var aps=AP[ver];for(var a=0;a<aps.length;a++)for(var b=0;b<aps.length;b++){var r=aps[a],c=aps[b];if(rsv[r][c])continue;for(var i=-2;i<=2;i++)for(var j=-2;j<=2;j++){var vv=Math.max(Math.abs(i),Math.abs(j));place(r+i,c+j,vv!==1);}}place(size-8,8,1);for(var i=0;i<9;i++){rsv[8][i]=1;rsv[i][8]=1;}for(var i=0;i<8;i++){rsv[8][size-1-i]=1;rsv[size-1-i][8]=1;}function mask(m,r,c){switch(m){case 0:return (r+c)%2===0;case 1:return r%2===0;case 2:return c%3===0;case 3:return (r+c)%3===0;case 4:return (Math.floor(r/2)+Math.floor(c/3))%2===0;case 5:return (r*c)%2+(r*c)%3===0;case 6:return ((r*c)%2+(r*c)%3)%2===0;case 7:return ((r+c)%2+(r*c)%3)%2===0;}}function buildFmt(m){var ecbits={L:1,M:0,Q:3,H:2}[ecl];var data=(ecbits<<3)|m;var rem=data;for(var i=0;i<10;i++)rem=(rem<<1)^(((rem>>9)&1)?0x537:0);var fmt=((data<<10)|(rem&0x3FF))^0x5412;return fmt;}var best=null,bestPen=1e9,bestM=0;for(var mm=0;mm<8;mm++){var t=[];for(var i=0;i<size;i++)t.push(mod[i].slice());var bi=0,dir=-1;for(var col=size-1;col>0;col-=2){if(col===6)col--;for(var k=0;k<size;k++){for(var cc2=0;cc2<2;cc2++){var c=col-cc2;var r=(dir<0)?(size-1-k):k;if(rsv[r][c])continue;var dark=0;if(bi<finalCW.length*8){dark=(finalCW[bi>>3]>>(7-(bi&7)))&1;bi++;}if(mask(mm,r,c))dark^=1;t[r][c]=dark;}}dir=-dir;}var fmt=buildFmt(mm);for(var i=0;i<15;i++){var b=(fmt>>i)&1;if(i<6)t[i][8]=b;else if(i<8)t[i+1][8]=b;else if(i===8)t[8][7]=b;else t[8][14-i]=b;if(i<8)t[8][size-1-i]=b;else t[size-15+i][8]=b;}var pen=0;for(var r=0;r<size;r++){var run=1;for(var c=1;c<size;c++){if(t[r][c]===t[r][c-1])run++;else{if(run>=5)pen+=run-2;run=1;}}if(run>=5)pen+=run-2;}for(var c=0;c<size;c++){var run=1;for(var r=1;r<size;r++){if(t[r][c]===t[r-1][c])run++;else{if(run>=5)pen+=run-2;run=1;}}if(run>=5)pen+=run-2;}if(pen<bestPen){bestPen=pen;best=t;bestM=mm;}}return {size:size,mod:best,ver:ver};}
var _sealQRc=null;function _sealQR(){if(_sealQRc===null){try{_sealQRc=qrGen('https://promi.app','L');}catch(e){_sealQRc=false;}}return _sealQRc||null;}
function buildCercleHero(){var el=document.getElementById('plHero');if(!el)return;var W=380,H=196;var cols=['#82AEF8','#C9A8F5','#82AEF8','#DD4D23','#82AEF8'];var svg='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block"><defs><radialGradient id="plg" cx="50%" cy="42%" r="62%"><stop offset="0%" stop-color="#82AEF8" stop-opacity="0.30"/><stop offset="60%" stop-color="#82AEF8" stop-opacity="0.06"/><stop offset="100%" stop-color="#82AEF8" stop-opacity="0"/></radialGradient></defs><rect width="'+W+'" height="'+H+'" fill="url(#plg)"/>';try{var pts=[],seed=11;var rnd=function(){seed=(seed*9301+49297)%233280;return seed/233280;};for(var i=0;i<15;i++)pts.push([8+rnd()*(W-16),8+rnd()*(H-16)]);var vc=(typeof voronoiP==='function')?voronoiP(pts,[[0,0],[W,0],[W,H],[0,H]]):[];vc.forEach(function(cc){if(cc&&cc.length>=3){var d='M'+cc[0][0].toFixed(1)+' '+cc[0][1].toFixed(1);for(var q=1;q<cc.length;q++)d+=' L'+cc[q][0].toFixed(1)+' '+cc[q][1].toFixed(1);d+=' Z';svg+='<path d="'+d+'" fill="none" stroke="#291547" stroke-width="0.7" opacity="0.12"/>';}});}catch(e){}for(var k=0;k<5;k++){var y0=H*0.34+k*H*0.085;var col=cols[k%cols.length];var d='M0 '+y0.toFixed(1);for(var x=0;x<=W;x+=16){var yy=y0+Math.sin(x*0.028+k*0.9)*11*Math.sin(x*0.007+k*0.6);d+=' L'+x+' '+yy.toFixed(1);}svg+='<path d="'+d+'" fill="none" stroke="'+col+'" stroke-width="1.7" opacity="'+(0.55-k*0.07).toFixed(2)+'" stroke-linecap="round"/>';}svg+='</svg>';el.innerHTML=svg;}
var _premium=false,_keptCount=0,_kpersOpen=false;function toast(msg,l1,f1,l2,f2,l3,f3){try{var t=document.getElementById('_toast');if(!t){t=document.createElement('div');t.id='_toast';t.style.cssText='position:absolute;left:50%;bottom:98px;transform:translateX(-50%);z-index:400;background:#281F10;color:#E4D7BB;border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:12px 16px;font-family:var(--f-texte);font-size:13px;line-height:1.3;box-shadow:0 10px 34px rgba(0,0,0,.45);display:flex;flex-wrap:wrap;align-items:center;gap:8px;max-width:88%';document.body.appendChild(t);}t.innerHTML='';var sp=document.createElement('span');sp.textContent=msg;sp.style.flex='1 1 auto';t.appendChild(sp);function mk(lb,fn){var b=document.createElement('button');b.textContent=lb;b.style.cssText='background:#82AEF8;color:#fff;border:0;border-radius:10px;padding:8px 12px;font-family:inherit;font-weight:600;font-size:13px;cursor:pointer;white-space:nowrap';b.onclick=function(){try{fn();}catch(e){}if(t)t.remove();};t.appendChild(b);}var act=false;if(l1&&f1){mk(l1,f1);act=true;}if(l2&&f2){mk(l2,f2);act=true;}if(l3&&f3){mk(l3,f3);act=true;}clearTimeout(t._to);t._to=setTimeout(function(){if(t&&t.parentNode)t.remove();},act?7000:3200);}catch(e){}}
function renderSeal(fmt){try{if(fmt)_sealFmt=fmt;var f=SEAL_FMTS[_sealFmt]||SEAL_FMTS.square;var _asp=(typeof _sealAspectOverride==='number'&&_sealAspectOverride>0)?_sealAspectOverride:f.a;var W=1080,H=Math.round(W/_asp);_INK=_sealDark?'#E4D7BB':'#231C0E';_SUB=_sealDark?'#A2947C':'#716C66';_HAIR=_sealDark?'rgba(255,255,255,.30)':'rgba(0,0,0,.34)';var parts=[];if(_sealParts.noyau)parts.push('noyau');if(_sealParts.pelote)parts.push('pelote');if(_sealParts.prometteurs)parts.push('prometteurs');if(_sealParts.disques)parts.push('disques');if(!parts.length)parts=['noyau'];var cv=document.createElement('canvas');cv.width=W;cv.height=H;var g=cv.getContext('2d');var _base=_sealDark?'#1F1605':'#EDE3CE';g.fillStyle=_base;g.fillRect(0,0,W,H);try{var _wantL=(typeof _sealDark!=='undefined')?!_sealDark:null;var _devL=(function(){var d=document.getElementById('device');return !!(d&&d.classList.contains('light'));})();var _match=(_wantL===null)||(_wantL===_devL);var _liveT=document.getElementById('toileCv');if(_match&&_liveT&&_liveT.width>0){g.save();g.globalAlpha=0.96;var _sw=_liveT.width,_sh=_liveT.height,_scv=Math.max(W/_sw,H/_sh),_dw=_sw*_scv,_dh=_sh*_scv;g.drawImage(_liveT,0,0,_sw,_sh,(W-_dw)/2,(H-_dh)/2,_dw,_dh);g.restore();}else if(window.Toile&&window.Toile.preview){var _tcS=renderSeal._tc||(renderSeal._tc=document.createElement('canvas'));_tcS.width=W;_tcS.height=H;var _stoS=window._shThemeOverride;if(_wantL!==null)window._shThemeOverride=_wantL;var _wS=(window.Toile.curWorld?window.Toile.curWorld():(typeof theme!=='undefined'?theme:'encre'));window.Toile.preview(_tcS,_wS,W,H);window._shThemeOverride=(_stoS===undefined?null:_stoS);g.save();g.globalAlpha=0.96;g.drawImage(_tcS,0,0,W,H);g.restore();}}catch(e){}g.textAlign='center';g.textBaseline='alphabetic';g.fillStyle=_INK;g.font='700 '+Math.round(W*0.048)+'px Gilbert,system-ui,sans-serif';g.fillText('Ma parole',W/2,H*0.088);if(_sealShowBalance){var _soi=promises.filter(function(p){return !p.draft&&(!p.who||p.who==='moi');}).length,_aut=promises.filter(function(p){return !p.draft;}).length-_soi,_tt=_soi+_aut;if(_tt>0){var _bw=W*0.72,_bx=(W-_bw)/2,_by=H*0.775,_bh=Math.max(9,W*0.03),_r=_bh/2,_f=_soi/_tt,_bg=g.createLinearGradient(_bx,0,_bx+_bw,0);_bg.addColorStop(0,'#C9A8F5');_bg.addColorStop(Math.max(0,_f-0.09),'#C9A8F5');_bg.addColorStop(Math.min(1,_f+0.09),'#82AEF8');_bg.addColorStop(1,'#82AEF8');g.beginPath();g.moveTo(_bx+_r,_by);g.arcTo(_bx+_bw,_by,_bx+_bw,_by+_bh,_r);g.arcTo(_bx+_bw,_by+_bh,_bx,_by+_bh,_r);g.arcTo(_bx,_by+_bh,_bx,_by,_r);g.arcTo(_bx,_by,_bx+_bw,_by,_r);g.closePath();g.fillStyle=_bg;g.fill();g.font='500 '+Math.round(W*0.02)+'px Atkinson,system-ui,sans-serif';g.fillStyle=_SUB;g.textBaseline='alphabetic';g.textAlign='left';g.fillText('Toi',_bx+2,_by-W*0.016);g.textAlign='right';g.fillText('les autres',_bx+_bw-2,_by-W*0.016);g.textAlign='center';}}var pair=(_sealFmt==='square'||_sealFmt==='post')&&_sealParts.noyau&&_sealParts.pelote;var rows;if(pair){rows=[['noyau','pelote']];if(_sealParts.prometteurs)rows.push(['prometteurs']);if(_sealParts.disques)rows.push(['disques']);}else{rows=parts.map(function(p){return [p];});}function _w(row){if(row.length===2)return 2.7;var p=row[0];if(p==='noyau'||p==='pelote')return 2.7;if(p==='prometteurs')return 1.15;return 1.1;}var top=H*0.145,bot=H-H*0.2,avail=bot-top;var ws=rows.map(_w);var tW=ws.reduce(function(a,b){return a+b;},0);var elemB=avail*0.8;var hs=ws.map(function(w){return elemB*w/tW;});var gw=[];for(var _g=0;_g<=rows.length;_g++)gw.push(1);for(var _g2=1;_g2<rows.length;_g2++){if(rows[_g2-1][0]==='prometteurs'&&rows[_g2][0]==='disques')gw[_g2]=0.3;}var gapB=avail-elemB;var tGW=gw.reduce(function(a,b){return a+b;},0);var y=top+gw[0]/tGW*gapB;rows.forEach(function(row,i){var eh=hs[i];var cyc=y+eh/2;if(row.length===2){var D=Math.min(eh*0.92,W*0.4);drawEmblem(g,W*0.28,cyc,D/234);drawRayonsRetires(g,W*0.72,cyc,D*0.92);}else{var part=row[0];if(part==='noyau'){var Dn=Math.min(eh*0.9,W*0.62);drawEmblem(g,W/2,cyc,Dn/234);}else if(part==='pelote'){var Do=Math.min(eh*0.9,W*0.62);drawRayonsRetires(g,W/2,cyc,Do*0.92);}else if(part==='prometteurs'){drawPartnersCanvas(g,W,y,eh);}else{drawDisquesCanvas(g,W,y,eh);}}y+=eh+gw[i+1]/tGW*gapB;});try{var _wmC=(typeof wmPos!=='undefined'?wmPos:0);var _qrRight=(_wmC!==2);var cell=Math.round(W*0.006);var _qr=_sealQR();var qs=_qr?cell*_qr.size:0;var qy=H-qs-Math.round(W*0.065);
if(_shShowQR!==false&&_qr){var qp=cell*3;var qx=_qrRight?(W-qs-Math.round(W*0.065)):Math.round(W*0.065);g.fillStyle=(_sealDark?'#F1E8D5':'#ffffff');g.fillRect(qx-qp,qy-qp,qs+qp*2,qs+qp*2);g.fillStyle='#1C1402';for(var _qr2=0;_qr2<_qr.size;_qr2++){for(var _qc=0;_qc<_qr.size;_qc++){if(_qr.mod[_qr2][_qc])g.fillRect(qx+_qc*cell,qy+_qr2*cell,cell,cell);}}}
var _cy=qy+qs*0.4;g.textBaseline='alphabetic';g.textAlign='left';/* ⚑ 23 SEPTEMBRE 2026 (Tom) — EN BAS À GAUCHE, LE MOT-MARQUE, ET RIEN D'AUTRE.
   « Il y a trop d'éléments : laisse juste le logo Promi, avec un i coloré, et supprime
     Promi.app et les autres éléments superflus. »
   « Ta parole prend forme » et le « .app » sortent. Le mot-marque prend la taille qu'avait
   la phrase (W × 0,035) : il devient la signature, il n'est plus une mention légale. */
g.font='700 '+Math.round(W*0.035)+'px Gilbert,system-ui,sans-serif';var _pw=g.measureText('Promi').width;var _wx=(_wmC===2)?(W-Math.round(W*0.075)-_pw):((_wmC===1)?Math.round(W/2-_pw/2):Math.round(W*0.075));g.fillStyle=_INK;g.fillText('Prom',_wx,_cy);var _w1=g.measureText('Prom').width;g.fillStyle='#82AEF8';g.fillText('i',_wx+_w1,_cy);}catch(e){}_sealCanvas=cv;var img=$('#sealOvImg');if(img)img.src=cv.toDataURL('image/png');}catch(e){}}
function openSealShare(){renderSeal(_sealFmt);var ov=$('#sealOv');if(ov)ov.classList.add('show');}
function saveSeal(){try{var cv=_sealCanvas;if(!cv)return;if(cv.toBlob){cv.toBlob(function(blob){if(!blob){try{window.open(cv.toDataURL('image/png'),'_blank');}catch(e){}return;}try{var u=URL.createObjectURL(blob);var a=document.createElement('a');a.href=u;a.download='promi-noyau.png';document.body.appendChild(a);a.click();a.remove();setTimeout(function(){try{URL.revokeObjectURL(u);}catch(e){}},1500);}catch(e){try{window.open(cv.toDataURL('image/png'),'_blank');}catch(e2){}}},'image/png');}else{try{window.open(cv.toDataURL('image/png'),'_blank');}catch(e){}}}catch(e){}}
function shareSeal(){try{var cv=_sealCanvas;if(!cv||!cv.toBlob){saveSeal();return;}cv.toBlob(function(blob){if(!blob){saveSeal();return;}try{var file=new File([blob],'promi-noyau.png',{type:'image/png'});if(navigator.share&&(typeof navigator.canShare!=='function'||navigator.canShare({files:[file]}))){navigator.share({files:[file],title:'Mon Noyau \u2014 Promi',text:'Ma parole tenue'}).catch(function(){});return;}}catch(e){}saveSeal();},'image/png');}catch(e){saveSeal();}}
function harmonyWord(pct){if(pct==null||pct==='\u2014')return 'à tisser';var p=+pct;if(p>=85)return 'rayonnante';if(p>=65)return 'solide';if(p>=40)return 'installée';return 'naissante';}
function harmonyGrad(cx,cy,r,w,tenu,enc,rate){auraSync();var M=KC.Mh,Cc=KC.Ch,O=KC.Oh;var tot=tenu+enc+rate;if(tot<=0)return '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="'+w+'"/>';var cum=0,bands=[];[[tenu,M],[enc,Cc],[rate,O]].forEach(function(x){if(x[0]>0){bands.push({c:x[1],s:cum/tot,e:(cum+x[0])/tot});}cum+=x[0];});var tw=0.013;var stops=[];bands.forEach(function(bd){var twb=Math.min(tw,(bd.e-bd.s)*0.34);stops.push([bd.s+twb,bd.c]);stops.push([bd.e-twb,bd.c]);});function hx(hh){hh=hh.replace('#','');return [parseInt(hh.slice(0,2),16),parseInt(hh.slice(2,4),16),parseInt(hh.slice(4,6),16)];}function mix(a,b,t){var x=hx(a),y=hx(b);return 'rgb('+Math.round(x[0]+(y[0]-x[0])*t)+','+Math.round(x[1]+(y[1]-x[1])*t)+','+Math.round(x[2]+(y[2]-x[2])*t)+')';}var nS=stops.length;function colAt(f){for(var i=0;i<nS;i++){var p0=stops[i][0],c0=stops[i][1],p1=stops[(i+1)%nS][0],c1=stops[(i+1)%nS][1];if(i===nS-1){var seg=1-p0+stops[0][0];if(f>=p0)return mix(c0,c1,(f-p0)/seg);if(f<stops[0][0])return mix(c0,c1,(f+1-p0)/seg);}else if(f>=p0&&f<p1){return mix(c0,c1,(f-p0)/((p1-p0)||1));}}return bands[0].c;}var N=190,s='';for(var k=0;k<N;k++){var f=k/N;var a0=-Math.PI/2+f*2*Math.PI;var a1=-Math.PI/2+(k+1)/N*2*Math.PI+0.01;var x0=cx+r*Math.cos(a0),y0=cy+r*Math.sin(a0),x1=cx+r*Math.cos(a1),y1=cy+r*Math.sin(a1);s+='<path d="M'+x0.toFixed(1)+' '+y0.toFixed(1)+' A '+r+' '+r+' 0 0 1 '+x1.toFixed(1)+' '+y1.toFixed(1)+'" fill="none" stroke="'+colAt(f)+'" stroke-width="'+w+'"/>';}return s;}
function buildSealViz(){var el=$('#auraSeal');if(!el)return;var act=promises.filter(function(p){return !p.draft&&!p.req;});var tenu=act.filter(function(p){return p.status==='tenu';}).length,enc=act.filter(function(p){return p.status==='encours';}).length,rate=act.filter(function(p){return p.status==='rate';}).length;var _inc=act.filter(function(p){return p.from&&p.from!=='moi';});var iTenu=_inc.filter(function(p){return p.status==='tenu';}).length,iRate=_inc.filter(function(p){return p.status==='rate';}).length,iEnc=_inc.filter(function(p){return p.status==='encours';}).length,iRes=iTenu+iRate;var tot=tenu+enc+rate;var res=tenu+rate;var pctDisp=res>0?(''+Math.round(100*tenu/res)):'\u2014';var cx=120,cy=120;var _lgtSV=(typeof isLightM==='function'&&isLightM());/* les traits suivent la PALETTE du Studio, comme l'anneau et HARMONIE.
   En clair on assombrit un peu pour tenir le contraste sur la creme. */
var _pal=null; try{ if(window.Toile&&Toile.cols) _pal=Toile.cols(); }catch(_){}
function _hx(c,k){ if(!c)return null;
  var r=Math.round(c[0]*k),v=Math.round(c[1]*k),b=Math.round(c[2]*k);
  return 'rgb('+Math.min(255,r)+','+Math.min(255,v)+','+Math.min(255,b)+')'; }
var _k=_lgtSV?0.78:1;
/* la couronne : tenue = menthe, en cours = periwinkle, a tenir = ocre */
var M=(_pal&&_pal[0])?_hx(_pal[0],_k):'#8FE08F';
var C=(_pal&&_pal[1])?_hx(_pal[1],_k):(_lgtSV?'#2F3ED6':'#82AEF8');
var O=(_pal&&_pal[2])?_hx(_pal[2],_k):(_lgtSV?'#B8362D':'#DD4D23');var hist=act.slice().sort(function(a,b){return a.id-b.id;});var n=hist.length||1;var rseq=hist.filter(function(p){return p.status==='tenu'||p.status==='rate';});var streak=0;for(var k=rseq.length-1;k>=0;k--){if(rseq[k].status==='tenu')streak++;else break;}var s='<svg viewBox="0 0 240 240" style="width:250px;max-width:80%;display:block;margin:0 auto">';s+='<g class="seal-crown">';hist.forEach(function(p,i){var a=-Math.PI/2+i/n*2*Math.PI;var col=p.status==='tenu'?M:(p.status==='rate'?O:C);var e2=p.status==='encours';/* une ONDE plutot qu'un cercle : deux sinusoides dephasees donnent une
   respiration organique. La graine vient de l'identifiant du Promi, donc
   la forme est stable d'un rendu a l'autre. */
var _ph=((p.id*2654435761)>>>0)%1000/1000;
var _on=Math.sin(i/n*2*Math.PI*3+_ph*6.283)*0.5+Math.sin(i/n*2*Math.PI*7-_ph*4.1)*0.28;
var _base=p.status==='tenu'?120:(p.status==='rate'?111:108);
var r0=104+_on*3, r1=_base+_on*11+_ph*4;s+='<line x1="'+(cx+r0*Math.cos(a)).toFixed(1)+'" y1="'+(cy+r0*Math.sin(a)).toFixed(1)+'" x2="'+(cx+r1*Math.cos(a)).toFixed(1)+'" y2="'+(cy+r1*Math.sin(a)).toFixed(1)+'" stroke="'+col+'" stroke-width="'+(e2?2.0:2.8)+'" stroke-linecap="round" opacity="'+(e2?0.72:0.95)+'"/>';});s+='</g>';s+='<circle cx="120" cy="120" r="76" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="25"/>';s+=harmonyGrad(cx,cy,76,24,tenu,enc,rate);if($('#device')&&$('#device').classList.contains('premium')){s+='<circle cx="120" cy="120" r="96" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="12"/>';s+=harmonyGrad(cx,cy,96,12,iTenu,iEnc,iRate);}var word=harmonyWord(pctDisp);var wfs=word.length>=9?21:(word.length>=7?25:30);/* Dans l'anneau : LE MOT SEUL, centre. « HARMONIE 62 % » et « serie N »
   sortent sous le Noyau (voir #kUnder) — a l'interieur, ils etaient illisibles. */
/* le mot, puis la serie juste dessous : le centre etait vide et tout le
   reste de l'ecran s'en trouvait repousse. */
/* dans le Noyau : la SERIE seule. Le mot d'harmonie descend avec
   « HARMONIE » et le %, qui forment un ensemble (voir #kUnder). */

/* la serie AU CENTRE exact du Noyau, plus grosse */
/* la serie prend les trois teintes de la palette, lettre par lettre,
   exactement comme HARMONIE (§59.2) : meme rappel visuel. */
if(streak>=2){var _st='série '+streak+' \u25c8', _tt=[M,C,O], _sw=0;
 var _cw2=12.4, _tw=_st.length*_cw2, _sx=120-_tw/2+_cw2/2;
 for(var _q=0;_q<_st.length;_q++){
  s+='<text x="'+(_sx+_q*_cw2).toFixed(1)+'" y="120" text-anchor="middle" dominant-baseline="central" font-family="var(--f-libelle)" font-weight="700" font-size="22" fill="'+_tt[_q%3]+'">'+(_st[_q]===' '?'&#160;':_st[_q])+'</text>';}}s+='</svg>';
/* le bloc sous le Noyau : titre, % en SIGNATURE, puis la serie */
var _u='<div id="kUnder">';
_u+='<div class="ku-mot">'+word+'</div>';
_u+='<div class="ku-lab" id="kuLab">'+'HARMONIE'.split('').map(function(c,i){return '<i>'+c+'</i>';}).join('')+'</div>';
if(pctDisp!=='\u2014')_u+='<div class="ku-pct sig">'+pctDisp+'<span class="ku-pc">%</span></div>';
/* la serie est DANS le Noyau (voir plus haut), plus ici */
_u+='</div>';
el.innerHTML=s+_u;try{if(window._majHarmonieCols)_majHarmonieCols();}catch(_h){}try{var _pm=$('#device')&&$('#device').classList.contains('premium');var _oc=document.createElement('canvas');_oc.width=240;_oc.height=240;_oc.style.cssText='position:absolute;top:0;left:50%;transform:translateX(-50%);height:100%;aspect-ratio:1;pointer-events:none';var _gg=_oc.getContext('2d');function _grn(r,w){_gg.save();_gg.beginPath();_gg.arc(120,120,r+w/2,0,6.2832);_gg.arc(120,120,r-w/2,0,6.2832,true);_gg.clip();_grain(_gg,240,240,0.6);_gg.restore();}_grn(76,24);if(_pm)_grn(96,12);el.style.position='relative';el.appendChild(_oc);}catch(e){}}
function _tutoToile(cv){try{var g=cv.getContext('2d');var W=cv.width,H=cv.height,STEP=3;var cols=[[201,168,245],[41,21,71],[221,77,35],[130,174,248],[201,168,245],[41,21,71]];var seeds=[];for(var i=0;i<11;i++){var c1=cols[(Math.random()*cols.length)|0],c2=cols[(Math.random()*cols.length)|0];seeds.push({x:Math.random()*W,y:Math.random()*H,ph:Math.random()*6.28,am:1+Math.random()*2,c1:c1,c2:c2,cph:Math.random()*6.28});}var raf,phase=0,last=performance.now(),speed=1.05,ripples=[];cv._ripple=function(x){ripples.push({x:(x==null?W/2:x),t:performance.now()});speed=1.7;};function frame(now){var dt=Math.min(60,now-last)/1000;last=now;speed+=(1.05-speed)*Math.min(1,dt*2.0);phase+=dt*speed;var t=phase;g.clearRect(0,0,W,H);ripples=ripples.filter(function(r){return now-r.t<950;});for(var s=0;s<seeds.length;s++){var sd=seeds[s];sd.px=sd.x+Math.cos(t*0.28+sd.ph)*sd.am;sd.py=sd.y+Math.sin(t*0.32+sd.ph)*sd.am*0.5;for(var ri=0;ri<ripples.length;ri++){var rp=ripples[ri];var age=(now-rp.t)/1400;var front=age*W*0.8;var dd=Math.abs(sd.x-rp.x)-front;var pu=Math.exp(-(dd*dd)/1200)*3*(1-age)*(1-age)*(1-age);sd.px+=(sd.x>=rp.x?1:-1)*pu;sd.py+=(Math.sin(sd.ph)>=0?1:-1)*pu*0.3;}}for(var y=0;y<H;y+=STEP){for(var x=0;x<W;x+=STEP){var best=1e9,bi=0;for(var k=0;k<seeds.length;k++){var dx=x-seeds[k].px,dy=y-seeds[k].py,d=dx*dx+dy*dy;if(d<best){best=d;bi=k;}}var sd=seeds[bi];var mix=0.5+0.5*Math.sin(t*0.22+sd.cph);var rr=sd.c1[0]+(sd.c2[0]-sd.c1[0])*mix,gg=sd.c1[1]+(sd.c2[1]-sd.c1[1])*mix,bb=sd.c1[2]+(sd.c2[2]-sd.c1[2])*mix;var a=1-(y/H)*0.55;g.fillStyle='rgba('+(rr|0)+','+(gg|0)+','+(bb|0)+','+a.toFixed(2)+')';g.fillRect(x,y,STEP,STEP);}}raf=requestAnimationFrame(frame);}raf=requestAnimationFrame(frame);cv._stop=function(){cancelAnimationFrame(raf);};}catch(e){}}
/* Le halo glisse d'un bouton à l'autre. En JS, pas en CSS : Chromium gèle les
   transitions d'un élément fraîchement inséré, et le halo restait collé au
   premier bouton. */
function _spotTo(sp,el,pad){
  /* Placement DIRECT. Ni transition CSS (Chromium les gèle sur un élément qu'on
     vient d'insérer), ni tween JS (les rAF sont étranglés tant que la Toile
     tourne) : le halo se pose net sur le bouton, et une brève pulsation dit
     qu'il a changé de cible. */
  var host=sp.parentNode;
  var ov=host.getBoundingClientRect();
  var s=(host.offsetWidth&&ov.width)?(ov.width/host.offsetWidth):1; if(!s)s=1;
  var r=el.getBoundingClientRect();
  sp.style.left=((r.left-ov.left)/s-pad).toFixed(1)+'px';
  sp.style.top=((r.top-ov.top)/s-pad).toFixed(1)+'px';
  sp.style.width=(r.width/s+pad*2).toFixed(1)+'px';
  sp.style.height=(r.height/s+pad*2).toFixed(1)+'px';
  sp.classList.remove('pop'); void sp.offsetWidth; sp.classList.add('pop');
}

function startTuto(first){if(document.getElementById('tutoOv'))return;window._tutoSeen=true;
  var _un=((typeof USER!=='undefined'&&USER.name)?USER.name:'');
  var GL={"promilogo": "<g style=\"mix-blend-mode:multiply\"><path d=\"M 60.5 44.0 Q 60.5 44.0 58.9 46.5 Q 57.2 49.0 57.2 52.1 Q 57.2 55.1 55.3 57.2 Q 53.3 59.4 50.9 61.0 Q 48.5 62.7 46.0 65.5 Q 43.5 68.4 40.0 68.7 Q 36.4 68.9 33.8 66.1 Q 31.2 63.3 28.6 61.8 Q 25.9 60.2 25.1 57.1 Q 24.4 54.0 24.7 51.2 Q 25.1 48.4 21.9 46.2 Q 18.8 44.0 19.0 41.0 Q 19.3 37.9 19.0 34.1 Q 18.7 30.3 20.8 27.3 Q 23.0 24.3 26.7 23.8 Q 30.5 23.2 33.9 24.0 Q 37.2 24.8 40.0 24.7 Q 42.8 24.6 45.7 24.9 Q 48.6 25.2 52.6 25.0 Q 56.7 24.7 59.3 27.4 Q 61.8 30.0 62.8 33.5 Q 63.8 37.0 62.2 40.5 Z\" fill=\"#82AEF8\" opacity=\"0.72\"/><path d=\"M 76.3 42.0 Q 76.3 42.0 77.7 44.8 Q 79.2 47.6 78.5 50.5 Q 77.8 53.4 76.2 56.1 Q 74.6 58.9 72.5 61.8 Q 70.4 64.7 66.6 63.3 Q 62.9 61.9 60.2 60.3 Q 57.6 58.6 54.1 60.6 Q 50.6 62.5 48.9 59.6 Q 47.3 56.7 43.9 55.6 Q 40.6 54.5 37.7 51.9 Q 34.8 49.4 34.0 45.7 Q 33.1 42.0 35.6 38.8 Q 38.1 35.6 40.6 33.4 Q 43.2 31.2 46.0 30.1 Q 48.8 29.1 51.0 28.0 Q 53.2 27.0 55.1 24.0 Q 57.0 20.9 60.2 19.6 Q 63.4 18.4 66.6 19.5 Q 69.7 20.7 73.8 21.1 Q 77.8 21.4 77.6 26.2 Q 77.3 30.9 76.9 34.0 Q 76.6 37.1 76.4 39.6 Z\" fill=\"#C9A8F5\" opacity=\"0.72\"/><path d=\"M 71.1 60.0 Q 71.1 60.0 71.6 63.2 Q 72.1 66.5 70.7 69.4 Q 69.2 72.4 67.2 75.0 Q 65.2 77.6 61.1 76.5 Q 57.0 75.4 54.8 76.6 Q 52.6 77.9 50.2 76.6 Q 47.8 75.4 44.6 77.1 Q 41.4 78.8 38.4 77.8 Q 35.3 76.9 32.3 75.1 Q 29.3 73.3 27.2 70.3 Q 25.1 67.3 27.4 63.6 Q 29.7 60.0 31.6 57.6 Q 33.5 55.2 34.2 52.7 Q 34.9 50.3 36.0 47.8 Q 37.2 45.3 39.5 43.5 Q 41.7 41.8 44.1 38.8 Q 46.5 35.8 50.1 34.9 Q 53.7 34.0 55.7 38.7 Q 57.6 43.4 58.6 46.1 Q 59.7 48.8 63.0 49.2 Q 66.2 49.6 66.4 52.4 Q 66.5 55.2 68.8 57.6 Z\" fill=\"#DD4D23\" opacity=\"0.72\"/></g>", "hello": "<path d=\"M30 28 L30 72 M30 50 L52 50 M52 28 L52 72\" stroke=\"#fff\" stroke-width=\"7\" stroke-linecap=\"round\" fill=\"none\"/><circle cx=\"70\" cy=\"50\" r=\"11\" stroke=\"#fff\" stroke-width=\"7\" fill=\"none\"/>", "promi": "<path d=\"M26 44 C26 30 44 26 52 38 C60 26 78 30 78 44 C78 60 60 74 52 84 C44 74 26 60 26 44 Z\" fill=\"#fff\"/>", "toilefil": "<g transform=\"scale(3.125)\"><path d=\"M7 11 L14 9 L16 15 L11 20 L6 17 Z\" stroke=\"#fff\" stroke-width=\"1.4\" stroke-linejoin=\"round\"/><path d=\"M18 8 L25 10 L26 17 L20 19 L17 13 Z\" fill=\"#82AEF8\" opacity=\".85\"/><path d=\"M13 20 L20 21 L19 26 L13 26 Z\" stroke=\"#fff\" stroke-width=\"1.4\" stroke-linejoin=\"round\"/></g>", "aura": "<g transform=\"scale(3.125)\"><circle cx=\"16\" cy=\"16\" r=\"10\" stroke=\"#fff\" stroke-width=\"1.5\"/><path d=\"M16 16 L16 8 A8 8 0 0 1 23.4 19 Z\" fill=\"#82AEF8\"/></g>", "index": "<g transform=\"scale(3.125)\"><path d=\"M6 7 L14 6 L14.5 14.5 L7 14.5 Z\" stroke=\"#fff\" stroke-width=\"1.5\" stroke-linejoin=\"round\"/><path d=\"M17.5 6.5 L26 6 L26 14.5 L17.5 14 Z\" fill=\"#82AEF8\"/><path d=\"M7 17.5 L14.5 17.5 L14 26 L6 25 Z\" stroke=\"#fff\" stroke-width=\"1.5\" stroke-linejoin=\"round\"/><path d=\"M17.5 18 L26 17.5 L26 26 L18 25.5 Z\" stroke=\"#fff\" stroke-width=\"1.5\" stroke-linejoin=\"round\"/></g>", "share": "<g transform=\"scale(3.125)\"><path d=\"M16 20 L16 7 M16 7 L11.5 11.5 M16 7 L20.5 11.5\" stroke=\"#82AEF8\" stroke-width=\"1.7\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M8.5 15 L8.5 25 L23.5 25 L23.5 15\" stroke=\"#fff\" stroke-width=\"1.5\" stroke-linejoin=\"round\"/></g>", "invite": "<path d=\"M50 30 C50 18 66 15 72 26 C78 15 94 18 94 30 C94 44 78 58 72 66 C66 58 50 44 50 30 Z\" fill=\"#fff\" transform=\"translate(-22,6)\"/>"};
  var pages=[];
  if(first)pages.push({bg:'#315480',kw:'#C9A8F5',gl:'promilogo',rep:null,t:'Bienvenue <span style="color:#DD4D23">'+_un+'</span>',s:'Voici comment <b style="color:#C9A8F5">Promi</b> fonctionne. Quelques gestes, quelques couleurs \u2014 glisse pour tout d\u00e9couvrir.'});
  pages.push({bg:'#82AEF8',kw:'#C9A8F5',gl:'promi',rep:{dock:2},t:'Le bouton central',s:'il plante un <b style="color:#C9A8F5">Promi</b> \u2014 une promesse. Ou il ouvre un <b style="color:#C9A8F5">Cercle</b> : des amis autour d\u2019un th\u00e8me, qui se promettent des choses.'});
  
  pages.push({bg:'#DD4D23',kw:'#C9A8F5',gl:'aura',rep:{dock:1},t:'Aura \u2014 tes infos',s:'ton <b style="color:#EDCBBD">harmonie</b> envers les autres : ton \u00e9volution, ton \u00e9quilibre. Ce que tu d\u00e9gages, en couleurs.'});
  pages.push({bg:'#417852',kw:'#F2D075',gl:'index',rep:{dock:3},t:'Ton index',s:'un seul endroit o\u00f9 tout se retrouve : chacun de tes <b style="color:#F2D075">Promi</b>, et chacun de tes <b style="color:#F2D075">Cercles</b>.'});
  pages.push({bg:'#AA3B2D',kw:'#C9A8F5',gl:'share',rep:{dock:4},t:'Partager',s:'partage un Promi \u2014 une <b style="color:#E6B7A9">promesse dite tout haut</b> se tient bien mieux.'});
  pages.push({bg:'#E6D8FA',kw:'#DD4D23',gl:'toilefil',rep:{sw:1},t:'Toile ou Fil',s:'tes Promi, deux regards : la <b style="color:#FAD4C7">Toile</b> qui se compose, ou le <b style="color:#FAD4C7">Fil</b> qui d\u00e9file.'});
  pages.push({bg:'#82AEF8',kw:'#C9A8F5',gl:'invite',rep:null,t:'\u00c0 toi de promettre',s:'explore <b style="color:#C9A8F5">Promi</b> \u00e0 ton rythme.'});
  var N=pages.length, cur=0;
  var ov=document.createElement('div');ov.className='tuto-ov2';ov.id='tutoOv';
  var css='.tuto-ov2{position:absolute;inset:0;z-index:120;overflow:hidden;opacity:0;transition:opacity 0.34s}.tuto-ov2.in{opacity:1}.tuto-ov2.out{opacity:0}'
   +'.t2-slider{width:100%;height:100%;overflow:hidden;position:relative;touch-action:pan-y}'
   +'.t2-track{display:flex;height:100%;transition:transform 0.55s cubic-bezier(.32,.72,0,1);touch-action:pan-y}'
   +'.t2-pg{min-width:100%;height:100%;position:relative;display:flex;flex-direction:column;padding:48px 32px 52px;box-sizing:border-box;color:#fff;overflow:hidden}'
   +'.t2-top{display:flex;justify-content:space-between;align-items:center;z-index:3;position:relative}'
   +'.t2-prog{font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.7}'
   +'.t2-skip{font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.6;background:none;border:0;color:#fff;cursor:pointer}'
   +'.t2-ghost{position:absolute;left:-14%;top:4%;width:128%;z-index:0;opacity:.14}'
   +'.t2-glyph svg text{fill:#fff}.t2-glyph{position:relative;z-index:2;margin:auto auto 0;width:104px;height:104px}'
   +'.t2-glyph svg{width:100%;height:100%}'
   +'.t2-body{position:relative;z-index:2;margin-top:22px;margin-bottom:auto}'
   +'.t2-ti{font-family:var(--f-libelle);font-size:44px;font-weight:700;letter-spacing:-.03em;line-height:1}'
   +'.t2-tx{font-size:14px;line-height:1.5;opacity:.94;margin-top:16px;max-width:250px}'
   +'.t2-nav{display:flex;flex-direction:column;align-items:center;gap:4px;color:rgba(255,255,255,.42);flex:1}.t2-nav svg{width:26px;height:26px}.t2-nav span{font-size:10px;font-weight:700;letter-spacing:.02em}.t2-nav.on{color:#fff}.t2-nav.hero{color:#fff}.t2-nav.hero svg{width:44px;height:44px;background:var(--verm,#82AEF8);border-radius:50%;padding:8px;box-shadow:0 6px 18px rgba(130,174,248,.5)}.t2-nav.on:not(.hero) svg{filter:drop-shadow(0 2px 8px rgba(255,255,255,.35))}.t2-dock{position:relative;z-index:2;display:flex;justify-content:space-around;align-items:flex-end;padding:16px 8px 4px;margin-top:16px;margin-bottom:8px;border-top:1px solid rgba(255,255,255,.22)}'
   +''
   +'.t2-dd.on::after{content:"";position:absolute;bottom:-9px;left:50%;transform:translateX(-50%);width:5px;height:5px;border-radius:50%;background:#fff}'
   +'.t2-sw{position:relative;z-index:2;align-self:center;display:inline-flex;background:rgba(255,255,255,.16);border-radius:10px;padding:4px;margin-top:16px}'
   +'.t2-sw span{font-size:13px;padding:8px 16px;border-radius:10px;color:rgba(255,255,255,.7)}.t2-sw span.on{background:#fff;color:#222;font-weight:600}'
   +'.t2-finish{position:absolute;left:24px;right:24px;bottom:74px;z-index:5;opacity:0;pointer-events:none;transform:translateY(8px);transition:opacity 0.34s,transform 0.34s;background:#fff;color:#182B3F;border:0;border-radius:16px;padding:16px;font-family:var(--f-libelle);font-weight:700;font-size:15px;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.3)}.t2-finish.show{opacity:1;pointer-events:auto;transform:none}.t2-dots{position:absolute;left:0;right:0;bottom:16px;display:flex;gap:8px;justify-content:center;z-index:4}'
   +'.t2-dots i{width:6px;height:6px;border-radius:4px;background:rgba(255,255,255,.4);transition:0.34s}.t2-dots i.on{width:20px;background:#fff}';
  var st=document.createElement('style');st.textContent=css;ov.appendChild(st);
  function ghost(){return '<svg class="t2-ghost" viewBox="0 0 100 128"><ellipse cx="32" cy="77" rx="28" ry="20" transform="rotate(38 32 77)" fill="#fff"/><ellipse cx="66" cy="86" rx="25" ry="20" transform="rotate(42 66 86)" fill="#fff"/><ellipse cx="23" cy="55" rx="27" ry="12" transform="rotate(142 23 55)" fill="#fff"/><ellipse cx="36" cy="45" rx="15" ry="29" transform="rotate(132 36 45)" fill="#fff"/><ellipse cx="70" cy="72" rx="15" ry="17" transform="rotate(89 70 72)" fill="#fff"/><ellipse cx="29" cy="96" rx="22" ry="14" transform="rotate(147 29 96)" fill="#fff"/><ellipse cx="30" cy="94" rx="24" ry="21" transform="rotate(61 30 94)" fill="#fff"/><ellipse cx="49" cy="42" rx="15" ry="27" transform="rotate(42 49 42)" fill="#fff"/><ellipse cx="65" cy="44" rx="35" ry="27" transform="rotate(135 65 44)" fill="#fff"/><ellipse cx="64" cy="70" rx="30" ry="13" transform="rotate(85 64 70)" fill="#fff"/><ellipse cx="68" cy="43" rx="34" ry="27" transform="rotate(73 68 43)" fill="#fff"/></svg>';}
  function repHTML(rep){
    if(!rep)return '';
    if(rep.sw){return '<div class="t2-sw"><span class="on">Toile</span><span>Fil</span></div>';}
    var IC=['<svg viewBox="0 0 32 32" fill="none"><path d="M7 11 L14 9 L16 15 L11 20 L6 17 Z" stroke="var(--ink)" stroke-width="1.4" stroke-linejoin="round"/><path d="M18 8 L25 10 L26 17 L20 19 L17 13 Z" fill="var(--verm)" opacity=".85"/><path d="M13 20 L20 21 L19 26 L13 26 Z" stroke="var(--ink)" stroke-width="1.4" stroke-linejoin="round"/></svg>','<svg viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="10" stroke="var(--ink)" stroke-width="1.5"/><path d="M16 16 L16 8 A8 8 0 0 1 23.4 19 Z" fill="var(--verm)"/></svg>','<svg viewBox="0 0 32 32"><path d="M16 7.5 V24.5 M7.5 16 H24.5" stroke="#C9A8F5" stroke-width="3.1" stroke-linecap="round"/></svg>','<svg viewBox="0 0 32 32" fill="none"><path d="M6 7 L14 6 L14.5 14.5 L7 14.5 Z" stroke="var(--ink)" stroke-width="1.5" stroke-linejoin="round"/><path d="M17.5 6.5 L26 6 L26 14.5 L17.5 14 Z" fill="var(--verm)"/><path d="M7 17.5 L14.5 17.5 L14 26 L6 25 Z" stroke="var(--ink)" stroke-width="1.5" stroke-linejoin="round"/><path d="M17.5 18 L26 17.5 L26 26 L18 25.5 Z" stroke="var(--ink)" stroke-width="1.5" stroke-linejoin="round"/></svg>','<svg viewBox="0 0 32 32" fill="none"><path d="M16 20 L16 7 M16 7 L11.5 11.5 M16 7 L20.5 11.5" stroke="var(--verm)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.5 15 L8.5 25 L23.5 25 L23.5 15" stroke="var(--ink)" stroke-width="1.5" stroke-linejoin="round"/></svg>'];
    var LB=['Studio','Aura','','Index','Partager'];
    var cells='';for(var j=0;j<5;j++){var on=(j===rep.dock)?' on':'';var hero=(j===2)?' hero':'';cells+='<div class="t2-nav'+on+hero+'">'+IC[j]+(LB[j]?'<span>'+LB[j]+'</span>':'')+'</div>';}
    return '<div class="t2-dock">'+cells+'</div>';
  }
  var track=document.createElement('div');track.className='t2-track';
  pages.forEach(function(p,idx){
    var pg=document.createElement('div');pg.className='t2-pg';pg.style.background=p.bg;
    pg.innerHTML='<div class="t2-top"><span class="t2-prog">'+(idx+1)+' / '+N+'</span><button class="t2-skip">passer</button></div>'
      +ghost()
      +'<div class="t2-glyph"><svg viewBox="0 0 100 100">'+GL[p.gl]+'</svg></div>'
      +'<div class="t2-body"><div class="t2-ti">'+p.t+'</div><div class="t2-tx">'+p.s+'</div></div>'
      +repHTML(p.rep);
    track.appendChild(pg);
  });
  var slider=document.createElement('div');slider.className='t2-slider';slider.appendChild(track);
  var dots=document.createElement('div');dots.className='t2-dots';
  for(var d=0;d<N;d++){var ii=document.createElement('i');if(d===0)ii.className='on';dots.appendChild(ii);}
  ov.appendChild(slider);ov.appendChild(dots);var fin=document.createElement('button');fin.className='t2-finish';fin.textContent='Explorer mon Promi';fin.addEventListener('click',function(e){e.stopPropagation();endTuto();});ov.appendChild(fin);
  (document.getElementById('device')||document.body).appendChild(ov);
  requestAnimationFrame(function(){ov.classList.add('in');});
  function go(i){cur=Math.max(0,Math.min(N-1,i));track.style.transition='';track.style.transform='translateX('+(-cur*100)+'%)';
    [].forEach.call(dots.children,function(x,k){x.classList.toggle('on',k===cur);});var _f=ov.querySelector('.t2-finish');if(_f)_f.classList.toggle('show',cur===N-1);}
  function endTuto(){window._tutoSeen=true;ov.classList.add('out');setTimeout(function(){if(ov.parentNode)ov.parentNode.removeChild(ov);},340);}
  [].forEach.call(ov.querySelectorAll('.t2-skip'),function(bt){bt.addEventListener('click',function(e){e.stopPropagation();endTuto();});});
  var x0=null,y0=null,drag=false,lock=null;
  function gx(e){return e.touches?e.touches[0].clientX:e.clientX;}
  function gy(e){return e.touches?e.touches[0].clientY:e.clientY;}
  function _down(e){x0=gx(e);y0=gy(e);drag=true;lock=null;track.style.transition='none';}
  function _move(e){if(!drag)return;var dx=gx(e)-x0,dy=gy(e)-y0;
    if(lock===null&&(Math.abs(dx)>6||Math.abs(dy)>6))lock=Math.abs(dx)>=Math.abs(dy)?'x':'y';
    if(lock!=='x')return;
    if(e.cancelable)e.preventDefault();
    var res=(cur===0&&dx>0)||(cur===N-1&&dx<0)?0.35:1;
    track.style.transform='translateX(calc('+(-cur*100)+'% + '+(dx*res)+'px))';}
  function _end(e){if(!drag)return;drag=false;track.style.transition='';var cx=(e.changedTouches?e.changedTouches[0].clientX:e.clientX);var dx=cx-x0;if(lock==='x'){if(dx<-45)go(cur+1);else if(dx>45)go(cur-1);else go(cur);}else go(cur);lock=null;}
  slider.addEventListener('mousedown',_down);window.addEventListener('mousemove',_move);window.addEventListener('mouseup',_end);
  slider.addEventListener('touchstart',_down,{passive:true});slider.addEventListener('touchmove',_move,{passive:false});window.addEventListener('touchend',_end);
  slider.addEventListener('click',function(e){if(e.target&&e.target.classList&&e.target.classList.contains('t2-skip'))return;});
  go(0);
}
 function heartPulse(){var h=document.getElementById('heartPulse');if(!h){h=document.createElement('div');h.id='heartPulse';h.className='heart-pulse';h.innerHTML='<svg viewBox="0 0 24 24"><path d="M12 21s-7-4.6-9.5-8.6C1 8.9 3 5.4 6.4 5.4c2.1 0 3.6 1.6 5.6 3.6 2-2 3.5-3.6 5.6-3.6C21 5.4 23 8.9 21.5 12.4 19 16.4 12 21 12 21z"/></svg>';(document.getElementById('device')||document.body).appendChild(h);}h.classList.remove('beat');void h.offsetWidth;h.classList.add('beat');setTimeout(function(){h.classList.remove('beat');},1300);}
function buildAura(){try{if(window.auTrame)auTrame();}catch(e){}const act=promises.filter(p=>!p.draft&&!p.req);var _premium=false;try{var _dv=document.getElementById('device');_premium=!!(_dv&&_dv.classList.contains('premium'));}catch(e){}const tenu=act.filter(p=>p.status==='tenu').length,enc=act.filter(p=>p.status==='encours').length,rate=act.filter(p=>p.status==='rate').length;const resolved=tenu+rate,kept=resolved>0?tenu/resolved:0,pct=Math.round(kept*100),pctDisp=resolved>0?pct:'—';
  const nuKeys=[...new Set(act.map(p=>p.nuee).filter(Boolean))];const nN=nuKeys.length;
  $('#kPct').textContent=pctDisp;var _kpc=document.querySelector('#auraScreen .kpc');if(_kpc)_kpc.style.display=resolved>0?'':'none';
  $('#souffleLine').textContent=resolved===0?(act.length===0?'plante ton premier Promi — ton Noyau prendra forme.':"rien n'est encore résolu — toute ta parole est ouverte."):kept>=.7?`tu tiens parole — ${enc} en cours${rate?`, ${rate>1?rate+' ont glissé':'une a glissé'}`:``}.`:kept>=.4?'ta parole se cherche — reprends un Cercle à la fois.':'ça glisse — reprends un Promi à la fois.';
  const vals=[pct-24,pct-20,pct-15,pct-11,pct-8,pct-5,pct-2,pct].map(v=>Math.max(8,Math.min(100,v)));
  const prev=vals[vals.length-2],delta=pct-prev;const dEl=$('#kDelta');dEl.className='kdelta '+(delta>1?'up':delta<-1?'down':'flat');dEl.textContent=(delta>1?'↑ en hausse':delta<-1?'↓ à tenir':'± stable')+' cette semaine';
  const _pn=[...new Set(act.map(p=>p.who))];const _persons=_pn.map(w=>{const it=act.filter(p=>p.who===w);return {name:w,enc:it.filter(p=>p.status==='encours').length,tenu:it.filter(p=>p.status==='tenu').length,rate:it.filter(p=>p.status==='rate').length};});karmaData={tenu,enc,rate,vals,persons:_persons};drawKarmaGraph();buildAuraSocial();buildSealViz();
  const streak=Math.max(0,tenu- (rate>0?1:0));
  var _kc=$('#kCount');if(_kc)/* le meme ordre que la legende juste au-dessus : tenues, en cours, a tenir */
  _kc.innerHTML=[['tenues',tenu,'#00341A'],['en cours',enc,'#291547'],['à tenir',rate,'#DD4D23']].map(function(x){return '<div class="kc-i"><div class="kc-n" style="color:'+x[2]+'">'+x[1]+'</div><div class="kc-l">'+x[0]+'</div></div>';}).join('');
  $('#kStats').innerHTML=[['en cours',enc],['résolues',resolved],['série',streak]].map(([l,v])=>`<div class="kst"><div class="kst-v">${v}</div><div class="kst-l">${l}</div></div>`).join('');var _soiN=act.filter(function(p){return !p.who||p.who==='moi';}).length,_autN=act.length-_soiN,_bt=act.length;var _kb=$('#kBalance');if(_kb)_kb.innerHTML=_bt?('<div class="kb-bar"><i style="flex:'+Math.max(_soiN,0.001)+';background:#C9A8F5"></i><i style="flex:'+Math.max(_autN,0.001)+';background:#82AEF8"></i></div><div class="kb-row"><span><b>'+_soiN+'</b> envers toi</span><span><b>'+_autN+'</b> envers les autres</span></div>'):'<div class="b" style="color:var(--gsub);padding:4px 0">plante des Promi pour voir l\'équilibre</div>';
  const rank={tenu:0,encours:1,rate:2};
  const groups=nuKeys.map(k=>({name:NUE[k]||k,items:act.filter(p=>p.nuee===k)}));const libres=act.filter(p=>!p.nuee);if(libres.length)groups.push({name:'Promesses libres',items:libres});
  (function(){var _el=groups.filter(function(g){return g.items.length>=2&&keptOf(g.items)!=null&&g.name!=='Moi-même'&&g.name!=='Promesses libres';});var _bn=$('#kBestNue');if(_bn){if(_el.length){var _b=_el.slice().sort(function(a,b){return keptOf(b.items)-keptOf(a.items);})[0];_bn.innerHTML='<div class="best-nue">\u2743 <b>'+_esc(_b.name)+'</b> <span class="bn-w">'+harmonyWord(keptOf(_b.items))+'</span></div>';}else{_bn.innerHTML='<div class="bn-empty">plante quelques Promi partagés pour la voir</div>';}}})();
  $('#kessaims').innerHTML=groups.map((g,gi)=>{const prem=_premium;const euxItems=g.items.filter(p=>p.from&&p.from!=='moi');const _kp=keptOf(g.items);const _kk=(_kp==null?55:_kp);const _col=_kp==null?'#291547':(_kp>=65?'#C9A8F5':_kp>=45?'#82AEF8':'#DD4D23');const _cmt=_kp==null?'':(_kp>=65?'rayonne':_kp>=45?'se tisse':'à raviver');var _pb=Math.max(18,_kk-20),_pts=[];for(var _z=0;_z<7;_z++)_pts.push(Math.round(_pb+(_kk-_pb)*(_z/6)));const det=g.items.slice().sort((a,b)=>rank[a.status]-rank[b.status]).map(p=>`<div class="kpr"><span class="kpr-t">${p.title}</span><span class="kpr-s ${p.status}">${STLAB[p.status]}</span></div>`).join('');return `<div class="kwrap" data-gi="${gi}"><div class="kess"><div class="ke-name"><div class="ke-n">${g.name}</div><div class="ke-sub">${g.items.length} Promi</div></div><canvas class="spk ke-spk" width="300" height="68" style="height:34px" data-pts="${_pts.join(',')}" data-col="${_col}"></canvas><div class="ke-pct">${_kp==null?'\u2014':_kp+'%'}${_cmt?`<span class="ke-cmt">${_cmt}</span>`:''}</div><div class="ke-chev">›</div></div><div class="kdetail">${det}</div></div>`;}).join('');
  $$('#kessaims .kess').forEach(row=>row.onclick=()=>row.parentElement.classList.toggle('open'));
  var _circle=karmaCircle();var _mine=_circle.filter(function(o){return (o.yourT+o.yourR+o.yourE)>0;});var _evg=groups.filter(function(gr){return gr.items&&gr.items.length>0;}).slice(0,6);if($('#kEvolve'))$('#kEvolve').innerHTML=_evg.length?_evg.map(function(gr){var kp=keptOf(gr.items);if(kp==null)kp=55;var col=kp>=65?'#C9A8F5':kp>=45?'#82AEF8':'#DD4D23';var base=Math.max(18,kp-20);var pts=[];for(var i=0;i<7;i++){pts.push(Math.round(base+(kp-base)*(i/6)));}return '<div class="ev-row"><span class="ev-n">'+_esc(gr.name)+'</span><canvas class="spk" width="320" height="72" style="height:36px" data-pts="'+pts.join(',')+'" data-col="'+col+'"></canvas><span class="ev-w">'+kp+'% · '+(kp>=65?'rayonne':kp>=45?'se tisse':'à raviver')+'</span></div>';}).join(''):'<div class="b" style="color:var(--gsub);padding:8px 0">pas encore de Cercle à suivre</div>';var _out=act.filter(function(p){return p.who&&p.who!=='moi'&&(!p.from||p.from==='moi');}),_inc2=act.filter(function(p){return p.from&&p.from!=='moi';});var _outT=_out.filter(function(p){return p.status==='tenu';}).length,_outR=_out.filter(function(p){return p.status==='rate';}).length;var _inT=_inc2.filter(function(p){return p.status==='tenu';}).length,_inR=_inc2.filter(function(p){return p.status==='rate';}).length;var _toiK=(_outT+_outR)>0?Math.round(100*_outT/(_outT+_outR)):null,_euxK=(_inT+_inR)>0?Math.round(100*_inT/(_inT+_inR)):null;if($('#kEquilibre')){if(_toiK==null||_euxK==null){$('#kEquilibre').innerHTML='<div class="b" style="color:var(--gsub);padding:4px 0">pas encore assez d\'échanges</div>';}else{var _diff=_toiK-_euxK,_pos=Math.round(50-Math.max(-42,Math.min(42,_diff*0.7))),_ph=Math.abs(_diff)<10?'le lien est réciproque \u273f':(_diff>0?'tu portes un peu plus en ce moment':'ils portent un peu plus en ce moment');$('#kEquilibre').innerHTML='<div class="eq-track"><span class="eq-end">Toi<b>'+_toiK+'%</b></span><div class="eq-line"><div class="eq-mark" style="left:'+_pos+'%"></div></div><span class="eq-end">eux<b>'+_euxK+'%</b></span></div><div class="eq-phrase">'+_ph+'</div>';}}var _tog=act.filter(function(p){return p.status==='tenu'&&((p.who&&p.who!=='moi')||p.from||p.nuee);}).length;if($('#kTogether'))$('#kTogether').innerHTML='<div class="together"><span class="tg-big">'+_tog+'</span><span class="tg-t"><b>promesses tenues</b> qui te lient<br><span class="tg-sub">des paroles honorées avec tes proches, pas juste envers toi</span></span></div>';
  var _KMAX=6,_showAll=_kpersOpen||_mine.length<=_KMAX,_vis=_showAll?_mine:_mine.slice(0,_KMAX);$('#kpers').innerHTML=_mine.length?('<div class="kring-grid">'+_vis.map(function(o){var _self=/^moi/i.test(o.name);var _dq=_self?('<div class="kr-wrap">'+karmaRing(o.yourE,o.yourT,o.yourR,52)+'</div>'):('<div class="kr-duo"><div class="kr-one kr-toi">'+karmaRing(o.yourE,o.yourT,o.yourR,52)+'<span class="kr-side">Toi</span></div><div class="kr-one kr-eux">'+karmaRing(o.theirE,o.theirT,o.theirR,52)+'<span class="kr-side">'+_esc(o.name)+'</span></div></div>');return '<div class="kring" data-p="'+_esc(o.name)+'" style="cursor:pointer">'+_dq+' <div class="kr-n">'+_esc(o.name)+'</div><div class="kr-w">'+harmonyWord(o.mutTrust==null?null:Math.round(o.mutTrust*100))+'</div></div>';}).join('')+'</div>'+(_mine.length>_KMAX?'<button class="kmore" id="kpersMore">'+(_showAll?'voir moins':'voir les '+(_mine.length-_KMAX)+' autres')+'</button>':'')):'<div class="b" style="padding:8px 0;color:var(--gsub)">tu n\'as encore rien promis à quelqu\'un</div>';var _km=$('#kpersMore');if(_km)_km.onclick=function(){_kpersOpen=!_kpersOpen;buildAura();};$$('#kpers .kring').forEach(function(r){r.onclick=function(){openPerson(r.getAttribute('data-p'));};});}

function gridPts(W,H,n){const pts=[];const cols=Math.max(2,Math.round(Math.sqrt(n*W/H)));const rows=Math.ceil(n/cols);let i=0;for(let r=0;r<rows;r++)for(let c=0;c<cols&&i<n;c++,i++){pts.push([(c+0.5+((((i*7)%5)-2)*0.07))*W/cols,(r+0.5+((((i*11)%5)-2)*0.07))*H/rows]);}return pts;}
function previewSVG(sk,mk,W,H,PTS){W=W||122;H=H||96;const st=STRUCT[sk],pal=MOODS[mk];const pts=PTS||[[34,30],[90,24],[64,52],[28,70],[98,66],[60,88],[112,44],[16,46]];const cells=voronoi(pts,[st.gap,st.gap,W-st.gap,H-st.gap]);let defs=DEFS,b=`<rect width="${W}" height="${H}" fill="${GROUND}"/>`,ov='';pts.forEach((p,i)=>{let cl=cells[i];if(!cl||cl.length<3)return;if(st.inset&&st.inset<1){const c0=centroid(cl);if(c0)cl=cl.map(q=>[c0[0]+(q[0]-c0[0])*st.inset,c0[1]+(q[1]-c0[1])*st.inset]);}let c=HX(pal[i%pal.length]);if(st.tint==='aqua')c=watercolor(c);if(st.jewel)c=jewel(c);if(st.trame)c=[239,227,199].map(v=>v-((i*13)%14));let f=RS(c);if(st.spectrum){const id=`pv${sk}${mk}${i}`;defs+=`<radialGradient id="${id}" cx="48%" cy="42%" r="72%"><stop offset="0%" stop-color="${RS(lighten(c,.30))}"/><stop offset="48%" stop-color="${RS(c)}"/><stop offset="100%" stop-color="${RS(darken(c,.16))}"/></radialGradient>`;f=`url(#${id})`;}let stroke=st.stroke==='chrome'?'url(#chrome)':st.stroke;const cs=`<path d="${roundPath(cl,st.round)}" fill="${f}" stroke="${stroke==='none'?'none':stroke}" stroke-width="${st.sw}" stroke-linejoin="round"/>`;b+=cs;if(st.trame){const ct=centroid(cl);if(ct)ov+=`<circle cx="${ct[0].toFixed(1)}" cy="${ct[1].toFixed(1)}" r="${(W/47).toFixed(1)}" fill="${pal[i%pal.length]}"/>`;}});return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block"><defs>${defs}</defs>${b}${ov}</svg>`;}
window._toileDPR=function(){try{return (window.Toile&&window.Toile.vue&&window.Toile.vue().dpr)||2;}catch(e){return 2;}};
function paintPreview(cv,sk,mk2,W,H,PTS){W=W||186;H=H||124;cv.width=W*window._toileDPR();cv.height=H*window._toileDPR();try{if(window.Toile&&window.Toile.preview){window.Toile.preview(cv,sk,W,H);return;}}catch(e){}var g=cv.getContext('2d');g.setTransform(2,0,0,2,0,0);g.fillStyle='#201908';g.fillRect(0,0,W,H);}
try{window.addEventListener('resize',function(){setTimeout(_placeLockCard,60);});}catch(e){}
function _placeLockCard(){/* le centrage est assuré en CSS (voir .st-lock) */}
/* ⚑ v71 : LA liste des mondes du Cercle — un seul propriétaire (buildStudio, setW et la réouverture la lisent) */
window._mondesCercle={sillons:1,gravure:1,terrazzo:1,bobinette:1,ritournelle:1,madrure:1,chamade:1,volubilis:1,guingois:1,mascaret:1,ramage:1,chantourne:1};
function buildStudio(){
  /* les bascules disent l'état RÉEL (elles étaient figées sur « Sombre » / « Sans texte ») */
  try{
    document.querySelectorAll('#txToggle button').forEach(function(b){
      b.classList.toggle('on', (b.dataset.tx==='on')===!!state.labels);
    });
    document.querySelectorAll('#thToggle button').forEach(function(b){
      b.classList.toggle('on', b.dataset.th===theme);
    });
  }catch(e){}
  var WL={pixel:'Buvard',braille:'Braille',sillons:'Houle',gravure:'Taille-douce',mosaique:'Tesselle',encre:'Pochade',terrazzo:'Éclisse',touffe:'Touffe',esquille:'Esquille',halin:'Halin',brouillamini:'Brouillamini',chamade:'Chamade',volubilis:'Volubilis',guingois:'Guingois',chantourne:'Chantourné',mascaret:'Mascaret',ramage:'Ramage',bobinette:'Bobinette',ritournelle:'Ritournelle',madrure:'Madrure'},order=['encre','touffe','brouillamini','halin','esquille','mosaique','braille','pixel','ramage','guingois','chantourne','volubilis','madrure','chamade','ritournelle','bobinette','mascaret','terrazzo','gravure','sillons'];   /* ⚑ v73 (Tom) : Guingois avant Madrure */   /* ⚑ v70 (Tom, 27 sept.) : huit gratuits, puis les payants */   /* ⚑ v37 (Tom) : Esquille en dernier des gratuits, juste avant les payants — Madrure, Ritournelle, Bobinette, Éclisse, Taille-douce, Houle */   /* ⚑ v32 : les quatre neufs au bout du rail ; v33 : Esquille gratuit, les trois autres au Cercle (Q314) */
  var cur=(window.Toile&&window.Toile.curWorld?window.Toile.curWorld():state.structure)||'encre';if(typeof state!=='undefined'&&state)state.structure=cur;var idx=order.indexOf(cur);if(idx<0){idx=0;cur=order[0];}
  var pals=(window.Toile&&window.Toile.palettes)?window.Toile.palettes():{},curp=(window.Toile&&window.Toile.getPalette)?window.Toile.getPalette():'signal';
  var _lockW=window._mondesCercle;   /* ⚑ v70 (Tom) : Chantourné passe au Cercle ; Brouillamini reste le seul gratuit de la saison 2 */   /* ⚑ v33 (Tom) : Bobinette, Ritournelle, Madrure au Cercle ; Esquille gratuit */var _lockedNow=_lockW[cur]&&!_ownedDesigns[cur]&&!(document.getElementById('device').classList.contains('premium'));if(_lockedNow)window._lockedWorld=cur;var out='<div class="st3-world'+(_lockedNow?' st3-locked':'')+'"><div class="st3-wn">'+WL[cur]+(_lockW[cur]?' <span class="st3-prem">✦</span>':'')+'</div><div class="st3-dots">';
  order.forEach(function(kk,i2){out+='<span class="st3-dot'+(i2===idx?' on':'')+'" data-w="'+kk+'"></span>';});
  out+='</div><div class="st3-hint">‹ glisse pour changer de monde ›</div></div>';
  out+='<div class="st3-bottom"><div class="st3-pals">';
  Object.keys(pals).forEach(function(kk){var cols=pals[kk].cols,pos=[[0,0],[1,0],[0,1],[1,1]],q='';cols.forEach(function(c,i3){q+='<span class="st3-q" style="left:'+(pos[i3][0]*50)+'%;top:'+(pos[i3][1]*50)+'%;background:rgb('+c[0]+','+c[1]+','+c[2]+')"></span>';});out+='<button class="st3-p'+(kk===curp?' on':'')+'" data-p="'+kk+'"><span class="st3-orb">'+q+'</span></button>';});
  out+='</div><div class="st3-pn" id="st3pn">'+((pals[curp]&&pals[curp].name)||'')+'</div><div class="st3-lbl2">Palette · Teinte</div><div class="st3-spec" id="st3spec"><div class="st3-thumb" id="st3thumb"></div></div></div>';
  $('#studioBody').innerHTML=out;
  try{var bg=document.getElementById('stBg');if(bg&&window.Toile&&window.Toile.preview){var pw=bg.clientWidth||390,ph=bg.clientHeight||800;bg.width=pw*window._toileDPR();bg.height=ph*window._toileDPR();window.Toile.preview(bg,cur,pw,ph);}}catch(e){}
  function setW(ni){ni=(ni+order.length)%order.length;idx=ni;var wnn=document.querySelector('.st3-wn');if(wnn)wnn.textContent=WL[order[ni]];[].forEach.call(document.querySelectorAll('.st3-dot'),function(d,k){d.classList.toggle('on',k===ni);});try{var _lk=window._mondesCercle;var _locked=_lk[order[ni]]&&!_ownedDesigns[order[ni]]&&!document.getElementById("device").classList.contains("premium");if(_locked)window._lockedWorld=order[ni];document.getElementById("studioScreen").classList.toggle("world-locked",!!_locked);if(_locked){try{requestAnimationFrame(function(){if(typeof _paintBuyBg==="function")_paintBuyBg();});setTimeout(function(){if(typeof _paintBuyBg==="function")_paintBuyBg();},180);setTimeout(function(){if(typeof _paintBuyBg==="function")_paintBuyBg();},460);}catch(_){}};try{requestAnimationFrame(_placeLockCard);setTimeout(_placeLockCard,140);setTimeout(_placeLockCard,420);}catch(e){}if(!_locked){state.structure=order[ni];window.Toile.setTheme(order[ni]);}window.Toile.repaintWorld(document.getElementById('stBg'),order[ni]);}catch(e){}}
  $$('#studioBody .st3-dot').forEach(function(d,i4){d.onclick=function(){setW(i4);};});
  var wr=document.getElementById('studioScreen');var sx=null,sy=null,sid=null,sOK=false;
  if(wr){
    /* on écoute sur tout le panneau : glisser n'importe où change de monde,
       sauf sur les commandes du bas (palettes, jauge) et les points de navigation. */
    var _skip=function(t){try{return !!(t.closest&&t.closest('.st3-bottom,.st3-dots,.st3-p,.st3-spec,.closeb,.studio-toggles'));}catch(e){return false;}};
    wr.addEventListener('pointerdown',function(e){
      if(_skip(e.target)){sOK=false;return;}
      sOK=true;sx=e.clientX;sy=e.clientY;sid=e.pointerId;
    },true);
    var _fired=false;
    /* on change de monde DÈS que le geste est franchement horizontal, sans attendre
       que le doigt se lève : sur mobile le navigateur annule souvent le pointeur
       quand il croit à un défilement, et le glissement était perdu. */
    var _move=function(e){
      if(!sOK||sx==null||_fired)return;
      var dx=e.clientX-sx, dy=e.clientY-sy;
      if(Math.abs(dx)>34&&Math.abs(dx)>Math.abs(dy)*1.3){
        _fired=true;
        if(dx>0)setW(idx-1); else setW(idx+1);
      }
    };
    var _end=function(e){
      if(!_fired&&sOK&&sx!=null){
        var dx=e.clientX-sx, dy=e.clientY-sy;
        if(Math.abs(dx)>=30&&Math.abs(dx)>=Math.abs(dy)){ if(dx>0)setW(idx-1); else setW(idx+1); }
      }
      sx=null;sy=null;sid=null;sOK=false;_fired=false;
    };
    wr.addEventListener('pointermove',_move,true);
    wr.addEventListener('pointerup',_end,true);
    wr.addEventListener('pointercancel',function(){sx=null;sOK=false;_fired=false;},true);
  }
  var _stbg=document.getElementById('stBg'); if(_stbg)_stbg.style.touchAction='pan-y';
  try{wr.style.touchAction='pan-y';}catch(e){}
  $$('#studioBody .st3-p').forEach(function(b){b.onclick=function(){try{window.Toile.setPalette(b.dataset.p);}catch(e){}try{var _pn=document.getElementById('st3pn');if(_pn&&pals[b.dataset.p])_pn.textContent=pals[b.dataset.p].name;}catch(e){}var bg2=document.getElementById('stBg');if(bg2&&bg2.__c){window.Toile.repaint(bg2);[].forEach.call(document.querySelectorAll('.st3-p'),function(x){x.classList.toggle('on',x===b);});}else{buildStudio();}};});
  var sp=$('#st3spec'),th=$('#st3thumb');if(sp){var bgc=document.getElementById('stBg');var _p=0,_v=0,_dg=false,_rf=null;
    var applyH=function(t){t=Math.max(0,Math.min(1,t));th.style.left=(t*100)+'%';th.style.setProperty('--hc','hsl('+Math.round(t*360)+',72%,54%)');try{window.Toile.setHue(t*360);window.Toile.repaint(bgc);}catch(e){}};
    var tX=function(cx){var r=sp.getBoundingClientRect();return Math.max(0,Math.min(1,(cx-r.left)/r.width));};
    var coast=function(){if(_dg){_rf=null;return;}_p+=_v;_v*=0.92;if(_p<0){_p=0;_v=0;}if(_p>1){_p=1;_v=0;}applyH(_p);if(Math.abs(_v)>0.0006){_rf=requestAnimationFrame(coast);}else{_rf=null;}};
    sp.addEventListener('pointerdown',function(e){_dg=true;if(_rf){cancelAnimationFrame(_rf);_rf=null;}try{sp.setPointerCapture(e.pointerId);}catch(x){}_p=tX(e.clientX);_v=0;applyH(_p);});
    sp.addEventListener('pointermove',function(e){if(!_dg)return;var t=tX(e.clientX);_v=_v*0.5+(t-_p)*0.5;_p=t;applyH(_p);});
    var _end=function(){if(!_dg)return;_dg=false;if(!_rf)_rf=requestAnimationFrame(coast);};
    sp.addEventListener('pointerup',_end);sp.addEventListener('pointercancel',_end);}
  /* le panneau vient d'être reconstruit : on replace l'encart une fois la mise en page faite */
  try{requestAnimationFrame(function(){requestAnimationFrame(_placeLockCard);});setTimeout(_placeLockCard,120);}catch(e){}
}
let pvPend=null;
function openPreview(s,m){pvPend={s,m};const pf=$('#pvFull');pf.innerHTML='';const cv=document.createElement('canvas');pf.appendChild(cv);paintPreview(cv,s,m,300,470,gridPts(300,470,16));$('#pvTitle').textContent=STRUCT[s].label;$('#pvMood').textContent=MOOD_L[m];const cur=s===state.structure&&m===state.mood;$('#pvApply').textContent=cur?'Toile actuelle ✓':'Appliquer cette Toile';$('#previewScreen').classList.add('show');}
$('#pvApply').onclick=()=>{if(pvPend){state.structure=pvPend.s;state.mood=pvPend.m;try{window.Toile&&window.Toile.setTheme(state.structure);}catch(e){}render();buildStudio();}$('#previewScreen').classList.remove('show');};

let theme='light';   /* par défaut : mode clair */
function setTheme(t){theme=t;$('#device').classList.toggle('light',t==='light');try{var _fr=document.querySelector('.frame');if(_fr)_fr.classList.toggle('light',t==='light');}catch(e){}try{localStorage.setItem('promi_theme',t);}catch(e){}   /* le thème survit au rechargement */try{if(window.Toile){window.Toile.reGray&&window.Toile.reGray();var _b=document.getElementById('stBg');if(_b&&window.Toile.reGrayStudio)window.Toile.reGrayStudio(_b);}}catch(e){}$$('#thToggle button').forEach(b=>b.classList.toggle('on',b.dataset.th===t));render();if($('#auraScreen').classList.contains('show'))drawKarmaGraph();}
$$('#thToggle button').forEach(b=>b.onclick=()=>setTheme(b.dataset.th));
let lp=null,moved=false;
let _tapT=0,_tapX=0,_tapY=0,_fingers=0;
stage.addEventListener('pointerdown',(e)=>{
  _fingers++;
  /* DEUX doigts = un pincement, jamais un appui long. Le canvas coupe la propagation
     du pointermove pendant le pincement : sans ce garde-fou, le stage ne voyait aucun
     mouvement, l'appui long arrivait au bout de 480 ms et le Studio s'ouvrait. */
  if(_fingers>1){moved=true;clearTimeout(lp);return;}
  moved=false;_tapT=Date.now();_tapX=e.clientX;_tapY=e.clientY;
  /* on note le zoom de la Toile : s'il a bougé, c'est qu'on pinçait — pas qu'on appuyait */
  var _s0=1; try{_s0=window.Toile.scale();}catch(err){}
  lp=setTimeout(()=>{
    if(_fingers>1)return;
    try{ if(window.Toile.fingers&&window.Toile.fingers()>1)return; }catch(err){}
    var _s1=_s0; try{_s1=window.Toile.scale();}catch(err){}
    if(Math.abs(_s1-_s0)>0.01)return;          /* la Toile a zoomé : c'était un pincement */
    /* ⚑ Q212 (Tom, 13 sept.) : l'appui long n'ouvre plus le Studio — il a son bouton dans la barre ; un raccourci
       invisible ne sert personne et se déclenche par accident. Le minuteur reste inerte. */
  },480);
}, true);
/* en capture : le canvas coupe le pointermove pour gérer pincement et déplacement */
/* un doigt bouge toujours d'un pixel ou deux : on ne considère que c'est un geste
   qu'au-delà d'un vrai déplacement, sinon aucun tap ne passait. */
function _mv(e){ if(Math.abs(e.clientX-_tapX)>12||Math.abs(e.clientY-_tapY)>12){moved=true;clearTimeout(lp);} }
stage.addEventListener('pointermove',_mv, true);
stage.addEventListener('pointermove',_mv);
function _fingerUp(){ _fingers=Math.max(0,_fingers-1); }
stage.addEventListener('pointerup',_fingerUp,true);
stage.addEventListener('pointercancel',()=>{_fingers=0;clearTimeout(lp);},true);
/* en phase de CAPTURE : le canvas de la Toile coupe la propagation du pointerup
   (il gère le pincement et le déplacement), le tap ne remonterait jamais jusqu'ici */
stage.addEventListener('pointerup',e=>{
  clearTimeout(lp);
  /* tap court et net sur une dalle -> on ouvre le Promi correspondant */
  if(moved)return;
  if(_fingers>0)return;                 /* un autre doigt est encore posé : c'est un geste, pas un tap */
  if(Date.now()-_tapT>700)return;
  if(Math.abs(e.clientX-_tapX)>14||Math.abs(e.clientY-_tapY)>14)return;
  try{
    const cv=$('#toileCv'); if(!cv||!window.Toile||!window.Toile.hit)return;
    const r=cv.getBoundingClientRect(); if(!r.width||!r.height)return;
    /* le téléphone est mis à l'échelle : on repasse en coordonnées internes */
    const sx=(e.clientX-r.left)*(cv.clientWidth/r.width);
    const sy=(e.clientY-r.top)*(cv.clientHeight/r.height);
    var h=window.Toile.hit(sx,sy);
    if(h&&h.pid==null&&h.kind!=='nuee'){ /* dalles pas encore reliees : on relie et on relit */
      if(assureLiaisonDalles()) h=window.Toile.hit(sx,sy); }
    /* ⚑ v46 (Tom) — LE DOUBLE TOUCHER, PARTOUT, ramène le zoom par défaut. Sur une dalle aussi : un toucher simple y ouvre sa
       fiche 260 ms plus tard, le temps de savoir s'il en vient un second (c'est ce que fait la galerie de l'iPhone). */
    var _now=Date.now(), _t1=window._tapVide;
    if(_t1 && _now-_t1.t<320 && Math.abs(e.clientX-_t1.x)<30 && Math.abs(e.clientY-_t1.y)<30){
      window._tapVide=null; if(_t1.to) clearTimeout(_t1.to); try{ window.Toile_recadre(); }catch(_){} return; }
    var _ouvre = null;
    if(h && h.kind==='nuee' && h.nuee){ _ouvre=function(){ if(typeof openEssaim==='function')openEssaim(h.nuee); }; }
    else if(h && h.pid!=null && typeof openDetail==='function'){ const p=promises.find(x=>x.id===h.pid); if(p) _ouvre=function(){ openDetail(h.pid); }; }
    window._tapVide={t:_now,x:e.clientX,y:e.clientY,to:_ouvre?setTimeout(function(){ if(window._tapVide&&window._tapVide.t===_now) window._tapVide=null; try{ _ouvre(); }catch(_){} },260):null};
    return;
  }catch(err){}
}, true);
stage.addEventListener('pointercancel',()=>clearTimeout(lp));

function assureLiaisonDalles(){
  try{
    if(!window.Toile||!window.Toile.sync||!window.Toile.dalleAbs) return false;
    var ids=promises.filter(function(p){return !p.draft;}).map(function(p){return p.id;});
    if(!ids.length) return false;
    var lie=false; try{ lie=!!window.Toile.dalleAbs(ids[0]); }catch(e){}
    if(lie) return true;
    window.Toile.sync(ids);
    return true;
  }catch(e){ return false; }
}
window.assureLiaisonDalles=assureLiaisonDalles;
function updatePulse(){var i=document.getElementById('promiI');if(!i)return;var bientot=promises.some(function(p){return !p.draft&&!p.enLair&&p.status==='encours'&&p.due!=null&&p.due<=1;});i.classList.toggle('on',bientot);}
function caption(){
  /* le meme compte que l'Index : ni brouillons ni demandes. Un brouillon
     n'est pas une parole donnee, une demande non plus. */
  const n=promises.filter(function(p){return !p.draft && !p.req;}).length;const w=['zéro','une','deux','trois','quatre','cinq','six','sept','huit','neuf','dix'];var _cw=(n<=10?w[n]:n)+' Promi vivant'+(n>1?'s':'');$('#cap').textContent='';var _te=$('#toileEmpty');if(_te)_te.classList.toggle('show',n===0);$('#subtitle').textContent=n===0?'la Toile attend':('la Toile vit • '+_cw);const sl=$('#sidelabel');if(sl)sl.innerHTML='LA&nbsp;TOILE&nbsp;·&nbsp;'+String(n).padStart(2,'0');try{if(typeof queueSave==='function')queueSave();}catch(e){}}
let bootTries=0,seeded=false;
function ensureSeed(){if(!seeded){seedInit();seeded=true;}}
function boot(){try{setTimeout(assureLiaisonDalles,900);}catch(e){}
  if(!measure()){if(bootTries++<80){requestAnimationFrame(boot);return;}realW=360;realH=680;sc=300/realW;VBH=realH*sc;VB=`0 0 300 ${VBH.toFixed(2)}`;computeBox();}ensureSeed();render();if(cellPolys.length===0&&promises.length){seedInit();render();}caption();}
function refresh(){if(!measure())return;ensureSeed();render();caption();}
window.addEventListener('resize',()=>{if(measure()){ensureSeed();relayout();}if($('#auraScreen').classList.contains('show'))drawKarmaGraph();});
window.addEventListener('load',refresh);
document.fonts&&document.fonts.ready.then(()=>{if($('#auraScreen').classList.contains('show'))drawKarmaGraph();});
setTimeout(refresh,400);setTimeout(refresh,1200);setTimeout(function(){try{window.Toile_liven&&window.Toile_liven();}catch(e){}},1500);
try{boot();}catch(e){var dd=document.getElementById('diag');if(dd){dd.style.color='#ff5a5a';dd.textContent='BOOT ERR v17: '+(e&&e.message||e);}}
/* --- fix définitif toile vide : recale + repeint dès que la stage a sa vraie taille --- */
function kick(){try{
  const ob={x:box.x,y:box.y,w:box.w,h:box.h};
  if(!measure())return;
  if(!seeded){seedInit();seeded=true;}
  else if(ob.w>0&&ob.h>0&&box.w>0&&box.h>0&&(Math.abs(ob.w-box.w)>0.5||Math.abs(ob.h-box.h)>0.5||Math.abs(ob.x-box.x)>0.5||Math.abs(ob.y-box.y)>0.5)){
    promises.forEach(p=>{const nx=(p.x-ob.x)/ob.w,ny=(p.y-ob.y)/ob.h;p.x=box.x+nx*box.w;p.y=box.y+ny*box.h;p.tx=p.x;p.ty=p.y;});
  }
  render();
  if(cellPolys.length===0&&promises.length){try{seedInit();}catch(e){}render();}
  if(typeof forcePaint==='function')forcePaint(toileCv);
}catch(e){}}
try{ if(window.ResizeObserver){ const _ro=new ResizeObserver(()=>{clearTimeout(window.__kick);window.__kick=setTimeout(kick,50);}); _ro.observe(stage); } }catch(e){}
window.addEventListener('load',()=>{kick();setTimeout(kick,120);setTimeout(kick,400);});
window.addEventListener('pageshow',kick);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)kick();});
[60,180,450,900,1600].forEach(t=>setTimeout(kick,t));
requestAnimationFrame(()=>requestAnimationFrame(kick));


/* ===== FIL D'ACTU ===== */
var FEED=[],_fid=1,feedReacted={};
function feedUnread(){return FEED.filter(function(f){return f.unread;}).length;}
function updateFeedDot(){var n=feedUnread();
 var d=$('#feedDot');if(d)d.style.display=n>0?'block':'none';
 var d2=$('#ixFeedDot');if(d2)d2.style.display=n>0?'inline-block':'none';
 /* la pastille du dock : c'est elle qui porte le signal depuis que le Fil
    a son bouton (§65). Une seule fonction met tout a jour. */
 try{if(window._majFilDot)_majFilDot();}catch(_){}}
function feedAdd(type,text,opts){opts=opts||{};FEED.unshift({id:_fid++,type:type,text:text,pid:opts.pid,from:opts.from,t:opts.t||"à l'instant",unread:!!opts.unread});updateFeedDot();if($('#feedScreen')&&$('#feedScreen').classList.contains('show'))buildFeed();}
function seedFeed(){FEED=[];_fid=1;feedAdd('added','Rachel a planté « la playlist du trajet »',{t:'il y a 3 j'});feedAdd('joined','Nico a rejoint Weekend à Lisbonne',{t:'il y a 3 j'});feedAdd('kept','Adrien a tenu « trouver le resto »',{t:'hier'});
  /* le Fil est de l'ACTIVITÉ, pas que du reçu : une promesse à soi y a sa place.
     On référence un vrai Promi perso (pid → ouvrable + sa dalle du monde). */
  try{ var _self=promises.filter(function(p){return !p.draft&&!p.req&&(!p.from||p.from==='moi')&&(!p.who||p.who==='moi'||p.who==='Moi');})[0];
    if(_self) feedAdd('added','Tu t’es promis « '+_self.title+' »',{pid:_self.id,t:'hier'}); }catch(_){}
  /* Chiche (lot 25) : un défi reçu (à relever) et un défi relevé — les deux natures
     d'événement propres au Chiche, avec les tournures données par l'utilisateur. */
  feedAdd('chiche_recu','Marion te lance un défi : « courir dimanche »',{from:'Marion',unread:true,t:'récemment'});
  feedAdd('chiche_releve','Marion a relevé ton chiche : « lire 10 pages »',{from:'Marion',t:'hier'});
  promises.filter(function(p){return p.pending;}).forEach(function(p){feedAdd('received',(p.from||'Quelqu\'un')+' te promet : « '+p.title+' »',{pid:p.id,unread:true,t:'récemment'});});}
function feedIcon(t){return {received:'✎',kept:'✓',missed:'×',added:'✦',joined:'⊕',nuee:'❉',accepted:'✓',declined:'×',relance:'⤴'}[t]||'·';}
function buildFeed(){var el=$('#feedList');if(!el)return;var _q=(typeof fdQuery!=='undefined'?fdQuery:'').trim().toLowerCase();/* on cherche dans le geste, le Promi concerné, la personne, la Nuée, et les brouillons */var _fmatch=function(f){if(!_q)return true;var p=f.pid?promises.find(function(x){return x.id===f.pid;}):null;var bag=(f.text||'')+' '+(f.t||'')+' '+(f.who||'')+' '+(f.from||'');if(p){bag+=' '+(p.title||'')+' '+(p.who||'')+' '+(p.from||'')+' '+((typeof NUE!=='undefined'&&NUE[p.nuee])||p.nuee||'');if(p.draft)bag+=' brouillon';}return bag.toLowerCase().indexOf(_q)>=0;};var _list=FEED.filter(_fmatch);if(typeof fdSortMode!=='undefined'&&fdSortMode==='personne'){_list=_list.slice().sort(function(a,b){function pk(f){var pp=f.pid?promises.find(function(x){return x.id===f.pid;}):null;return ''+(f.from||(pp&&pp.from)||(pp&&pp.who)||f.who||'');}var ka=pk(a),kb=pk(b);function moi(k){k=k.trim().toLowerCase();return k===''||k==='moi'||k===(USER.name||'').trim().toLowerCase();}var ma=moi(ka)?0:1,mb=moi(kb)?0:1;if(ma!==mb)return ma-mb;return ka.localeCompare(kb);});}else if(typeof fdSortMode!=='undefined'&&fdSortMode==='brouillon'){_list=_list.slice().sort(function(a,b){function dk(f){var pp=f.pid?promises.find(function(x){return x.id===f.pid;}):null;return pp&&pp.draft?0:1;}return dk(a)-dk(b);});}else if(typeof fdSortMode!=='undefined'&&fdSortMode==='nuee'){_list=_list.slice().sort(function(a,b){function nk(f){var pp=f.pid?promises.find(function(x){return x.id===f.pid;}):null;return ''+((pp&&((typeof NUE!=='undefined'&&NUE[pp.nuee])||pp.nuee))||'~~');}return nk(a).localeCompare(nk(b));});}if(!_list.length){el.innerHTML='<div class="feed-empty"><div class="fe-ic">\u2726</div><div class="fe-t">'+(_q?'Rien ne correspond':'Rien ne bouge encore')+'</div><div class="fe-s">'+(_q?'essaie un autre mot':'les gestes de tes proches<br>appara\u00eetront ici')+'</div></div>';return;}var h='';_list.forEach(function(f){var p=f.pid?promises.find(function(x){return x.id===f.pid;}):null;var pending=(f.type==='received'&&p&&p.pending);
    var _nk=null;
    if(!p){ try{
      var _t=(f.text||'').toLowerCase();
      for(var _k in NUE){ var _n=(NUE[_k]||'').toLowerCase();
        if(_n && _t.indexOf(_n)>=0){ _nk=_k; break; } }
      if(!_nk){ var _m=(f.text||'').match(/[\u00ab"']\s*([^\u00bb"']+?)\s*[\u00bb"']/);
        if(_m){ var _ti=_m[1].trim().toLowerCase();
          var _pp=promises.filter(function(x){return (x.title||'').trim().toLowerCase()===_ti;})[0];
          if(_pp) p=_pp; } }
    }catch(e){} }var _N=window.filNature?filNature(f,p,pending):{cls:'',col:'',pre:''};
    h+='<div class="fd-item '+_N.cls+(f.unread?' unread':'')+((p||_nk)?' fd-open':'')+'" data-fid="'+f.id+'" data-type="'+(f.type||'')+'"'+(_N.col?' style="background:'+_N.col+'"':'')+(p?' data-pid="'+p.id+'"':'')+(_nk?' data-nuee="'+_nk+'"':'')+'>'+(p?'<div class="fd-dal">'+miniCell(p)+'</div>':(function(){
        /* l'evenement porte le titre du Promi entre guillemets : on le retrouve
           pour peindre sa dalle. Sans ca, les lignes « a tenir » restaient nues. */
        try{
          /* trois voies pour retrouver le Promi : son id porte par l'evenement,
             le titre entre guillemets, puis le titre nu dans le texte. */
          var q=null;
          if(f.pid) q=promises.find(function(z){return z.id===f.pid;});
          if(!q){ var mm=(f.text||'').match(/«\s*(.+?)\s*»/);
            if(mm) q=promises.find(function(z){return z.title===mm[1];}); }
          if(!q) q=promises.find(function(z){
            return z.title && z.title.length>2 && (f.text||'').indexOf(z.title)>=0; });
          if(q) return '<div class="fd-dal">'+miniCell(q)+'</div>';
        }catch(_){}
        return ''; })())+'<div class="fd-body">'+(_N.pre?'<div class="fd-pre">'+_N.pre+'</div>':'')+'<div class="fd-tx">'+_esc(f.text)+(p?'<span class="ix-cm" data-cm="'+p.id+'" title="commenter"><svg viewBox="0 0 16 16" width="11" height="11" fill="none" style="vertical-align:-1px"><path d="M2.6 3.4h10.8v7.2H8.2L5 13.2v-2.6H2.6z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg><b>'+((p.comments&&p.comments.length)||'')+'</b></span>':'')+'</div><div class="fd-t">'+_esc(f.t)+'</div>';if(pending){h+='<div class="fd-acts fd-geste">'
      +'<div class="fd-acc g1" data-keep="'+f.id+'">TENIR</div>'
      +'<div class="fd-dec g2" data-post="'+f.id+'">REPORTER</div></div>';}
    /* un Chiche reçu se RELÈVE depuis le Fil : le défi s'accepte d'un geste. */
    else if(f.type==='chiche_recu'){h+='<div class="fd-acts fd-geste">'
      +'<div class="fd-acc g1" data-releve="'+f.id+'">RELEVER</div></div>';}
    /* ⚑ v89 (Q347) — les deux états neufs, chacun avec SON geste */
    else if(f.type==='invitation'&&!f.fait){h+='<div class="fd-acts fd-geste">'
      +'<div class="fd-acc g1" data-rejoindre="'+f.id+'">REJOINDRE</div></div>';}
    else if(f.type==='moitie'&&window._filAttend&&window._filAttend(f)){h+='<div class="fd-acts fd-geste">'
      +'<div class="fd-acc g1" data-tracer="'+f.id+'">TRACER</div></div>';}
    /* un Promi depasse se tient DEPUIS le Fil : le geste est la, pas dans une
       liste a cocher. On ne valide pas une tache, on tient sa parole. */
    else if(p && !p.draft && !p.req && p.status==='rate'){
      h+='<div class="fd-acts fd-geste">'
        +'<div class="fd-acc g1" data-keep="'+f.id+'">TENIR</div>'
        +'<div class="fd-dec g2" data-post="'+f.id+'">REPORTER</div></div>';}else if(f.type==='kept'||f.type==='added'||f.type==='accepted'||f.type==='joined'){var on=feedReacted[f.id];h+='<div class="fd-react'+(on?' on':'')+'" data-react="'+f.id+'">'+(on?'✦':'✧')+' bravo</div>';}if(p)h+='<div class="cm-block" data-cmb="'+p.id+'"></div>';h+='</div></div>';});el.innerHTML=h;$$('#feedList [data-keep]').forEach(function(b){b.onclick=function(e){
    e.stopPropagation(); feedKeep(+b.dataset.keep);
    try{if(window.syncAll)syncAll();}catch(_){}};});$$('#feedList [data-post]').forEach(function(b){b.onclick=function(e){
    e.stopPropagation(); feedPostpone(+b.dataset.post);
    try{if(window.syncAll)syncAll();}catch(_){}};});$$('#feedList [data-react]').forEach(function(b){b.onclick=function(){var id=+b.dataset.react;feedReacted[id]=!feedReacted[id];buildFeed();};});$$('#feedList [data-releve]').forEach(function(b){b.onclick=function(e){e.stopPropagation();feedReleve(+b.dataset.releve);try{if(window.syncAll)syncAll();}catch(_){}};});_cmRender($('#feedList'));
  /* les dalles doivent etre peintes avant qu'on lise leur couleur */
  try{ if(window.peintMinis)peintMinis($('#feedList')); }catch(_){}
  try{ if(window._teinterFil) requestAnimationFrame(function(){
    requestAnimationFrame(_teinterFil); }); }catch(_){}
  try{ if(window._lisibilite) requestAnimationFrame(function(){
    _lisibilite($('#feedList'));
    if(window._titresTeintes)_titresTeintes($('#feedList')); }); }catch(_){}$$('#feedList .fd-open[data-nuee]').forEach(function(it){it.addEventListener('click',function(e){
  if(e.target.closest('.fd-acts')||e.target.closest('.fd-react')||e.target.closest('button'))return;
  var k=it.getAttribute('data-nuee');
  if(k&&typeof openEssaim==='function'){try{if(typeof closeAll==='function')closeAll();}catch(_){}openEssaim(k);}
});});
$$('#feedList .fd-open[data-pid]').forEach(function(it){it.addEventListener('click',function(e){if(e.target.closest('.fd-acts')||e.target.closest('.fd-react')||e.target.closest('button'))return;var pid=+it.getAttribute('data-pid');if(pid&&typeof openDetail==='function'){try{if(typeof closeAll==='function')closeAll();}catch(_){}openDetail(pid);}});});}
function feedKeep(fid){var f=FEED.find(function(x){return x.id===fid;});if(!f)return;var p=f.pid?promises.find(function(x){return x.id===f.pid;}):null;if(p){p.status='tenu';p.pending=false;p.accepted=true;p.draft=false;}f.type='kept';f.text='Tu as tenu : \u00ab '+(p?p.title:'un Promi')+' \u00bb';if(typeof relayout==='function')relayout();else render();if(typeof caption==='function')caption();buildFeed();if(typeof updateFeedDot==='function')updateFeedDot();_keptCount++;if(_keptCount===2||_keptCount===5){toast('Belle s\u00e9rie \u2014 partage ton Noyau','Partager',function(){if(typeof openSealShare==='function')openSealShare();});}}
function feedReleve(fid){var f=FEED.find(function(x){return x.id===fid;});if(!f)return;
  /* relever un Chiche : le d\u00e9fi devient tien. On plante un vrai Chiche (il appara\u00eet
     dans l'Index et sur la Toile, dalle du monde), et la ligne du Fil bascule en
     \u00ab chiche relev\u00e9 \u00bb. Le nom du d\u00e9fieur est lu dans le texte de l'\u00e9v\u00e9nement. */
  var who=f.from||'';
  if(!who){ var m=(f.text||'').match(/^\s*([^\u00ab:]+?)\s+te\s/); if(m) who=m[1].trim(); }
  var titre=''; var mt=(f.text||'').match(/[\u00ab"']\s*([^\u00bb"']+?)\s*[\u00bb"']/); if(mt) titre=mt[1].trim();
  try{ if(typeof P==='function'){ var np=P(titre||'un chiche',who||'moi',7,2,'encours'); np.chiche=true; np.phraseSens='chiche'; np.from=who||'moi';
    computeBox(); np.x=box.x+box.w/2; np.y=box.y+box.h/2; np.tx=np.x; np.ty=np.y; promises.push(np);
    try{ if(window.Toile&&Toile.addPromi)Toile.addPromi(np.id); }catch(_){}
    f.pid=np.id; } }catch(_){}
  f.type='chiche_releve'; f.text='Tu as relev\u00e9 le chiche de '+(who||'quelqu\u2019un')+(titre?' : \u00ab '+titre+' \u00bb':''); f.unread=false;
  if(typeof relayout==='function')relayout();else render();if(typeof caption==='function')caption();
  buildFeed();if(typeof updateFeedDot==='function')updateFeedDot();try{if(window._majAnneauPlus)_majAnneauPlus();}catch(_){}}
function feedPostpone(fid){toast('Reporter\u2026','+1 j',function(){_fpost(fid,1);},'+3 j',function(){_fpost(fid,3);},'+1 sem',function(){_fpost(fid,7);});}
function _fpost(fid,d){var f=FEED.find(function(x){return x.id===fid;});if(!f)return;var p=f.pid?promises.find(function(x){return x.id===f.pid;}):null;if(p){p.pending=false;p.accepted=true;p.due=(p.due||0)+d;}f.type='added';var lab=d===1?'+1 j':(d===7?'+1 sem':'+'+d+' j');f.text='Tu as report\u00e9 : \u00ab '+(p?p.title:'un Promi')+' \u00bb ('+lab+')';if(typeof relayout==='function')relayout();else render();if(typeof caption==='function')caption();buildFeed();if(typeof updateFeedDot==='function')updateFeedDot();}


var _mainView='toile';function drawCercleHero(){var c=document.getElementById('plHeroCv');if(!c||!c.getContext)return;var g=c.getContext('2d'),W=c.width,H=c.height;
 function hx(hh){hh=hh.replace('#','');return [parseInt(hh.slice(0,2),16),parseInt(hh.slice(2,4),16),parseInt(hh.slice(4,6),16)];}
 function mix(a,b,t){var x=hx(a),y=hx(b);return 'rgb('+Math.round(x[0]+(y[0]-x[0])*t)+','+Math.round(x[1]+(y[1]-x[1])*t)+','+Math.round(x[2]+(y[2]-x[2])*t)+')';}
 g.fillStyle='#201908';g.fillRect(0,0,W,H);
 function wash(x,y,r,col,al){var gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,'rgba('+hx(col).join(',')+','+al+')');gr.addColorStop(1,'rgba('+hx(col).join(',')+',0)');g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,6.2832);g.fill();}
 g.globalCompositeOperation='lighter';wash(W*0.28,H*0.34,W*0.55,'#82AEF8',.5);wash(W*0.72,H*0.26,W*0.5,'#C9A8F5',.4);wash(W*0.6,H*0.72,W*0.5,'#DD4D23',.18);wash(W*0.14,H*0.64,W*0.4,'#291547',.28);g.globalCompositeOperation='source-over';
 var cx=W/2,cy=H*0.5,R=W*0.125;
 var gl=g.createRadialGradient(cx,cy,0,cx,cy,R*2.1);gl.addColorStop(0,'rgba(41,21,71,.32)');gl.addColorStop(1,'rgba(41,21,71,0)');g.fillStyle=gl;g.beginPath();g.arc(cx,cy,R*2.1,0,6.2832);g.fill();
 var cps=[{p:0.24,c:'#C9A8F5'},{p:0.68,c:'#82AEF8'},{p:0.92,c:'#DD4D23'}];
 function colAt(f){for(var i=0;i<cps.length;i++){var a=cps[i],b=cps[(i+1)%cps.length],pa=a.p,pb=b.p;if(i===cps.length-1)pb+=1;var ff=f;if(i===cps.length-1&&f<cps[0].p)ff+=1;if(ff>=pa&&ff<pb)return mix(a.c,b.c,(ff-pa)/(pb-pa));}return cps[0].c;}
 g.lineCap='butt';g.lineWidth=R*0.17;g.strokeStyle='rgba(255,255,255,.06)';g.beginPath();g.arc(cx,cy,R,0,6.2832);g.stroke();
 var N=220;for(var k=0;k<N;k++){var f=k/N;var a0=-Math.PI/2+f*6.2832,a1=-Math.PI/2+(k+1)/N*6.2832+0.004;g.strokeStyle=colAt(f);g.lineWidth=R*0.17;g.beginPath();g.arc(cx,cy,R,a0,a1);g.stroke();}
 g.lineCap='round';var hist=['t','t','e','t','r','t','t','t','e','t','r','t','t','e','t','r','t','t'];for(var i=0;i<hist.length;i++){var a=-Math.PI/2+i/hist.length*6.2832;var col=hist[i]==='t'?'#C9A8F5':(hist[i]==='r'?'#DD4D23':'#82AEF8');var r0=R+R*0.15,r1=r0+(hist[i]==='t'?R*0.16:R*0.11);g.strokeStyle=col;g.globalAlpha=hist[i]==='e'?.42:.92;g.lineWidth=hist[i]==='e'?R*0.02:R*0.032;g.beginPath();g.moveTo(cx+r0*Math.cos(a),cy+r0*Math.sin(a));g.lineTo(cx+r1*Math.cos(a),cy+r1*Math.sin(a));g.stroke();}g.globalAlpha=1;
 try{var im=g.getImageData(0,0,W,H),d=im.data;for(var j=0;j<d.length;j+=4){var nz=(Math.random()-0.5)*18;d[j]+=nz;d[j+1]+=nz;d[j+2]+=nz;}g.putImageData(im,0,0);}catch(e){}
}
/* une entrée du Fil ouvre le Promi dont elle parle (les boutons Tenir/Reporter
   et les réactions gardent la priorité) */
(function(){
  var fv=document.getElementById('feedView'); if(!fv)return;
  fv.addEventListener('click',function(e){
    if(e.target.closest('button')||e.target.closest('.fd-react'))return;
    var it=e.target.closest('.fd-item[data-pid]'); if(!it)return;
    var id=+it.getAttribute('data-pid');
    var p=promises.find(function(x){return x.id===id;});
    if(p&&typeof openDetail==='function')openDetail(id);
  });
})();
function setView(v){var st=$('#stage'),fv=$('#feedView');if(!st||!fv)return;if(v==='fil'){fv.style.display='';buildFeed();fv.classList.remove('in');void fv.offsetWidth;requestAnimationFrame(function(){fv.classList.add('in');});setTimeout(function(){if(_mainView==='fil')st.style.display='none';},380);/* v89 (Q347) : plus de remise à zéro à l'ouverture */if(typeof updateFeedDot==='function')updateFeedDot();fv.scrollTop=0;try{var _d=document.getElementById('device');if(_d)_d.classList.add('v-fil');}catch(e){}try{requestAnimationFrame(function(){if(window.fdRefresh)window.fdRefresh();});}catch(e){}}else{fv.classList.remove('in');st.style.display='';setTimeout(function(){if(_mainView!=='fil')fv.style.display='none';},380);try{var _d2=document.getElementById('device');if(_d2)_d2.classList.remove('v-fil');}catch(e){}
    /* de retour sur la Toile : on la remesure et on la repeint */
    try{requestAnimationFrame(function(){if(window.Toile_resize)window.Toile_resize();});}catch(e){}
  }$$('#viewSwitch button').forEach(function(b){b.classList.toggle('on',b.dataset.view===v);});_mainView=v;if(v!=='fil'){try{window.Toile_liven&&window.Toile_liven();}catch(e){}}}
function openFeed(){setView('fil');}
var _introRAF=0;
function _rr(g,x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}

window.IntroVizRAF=0;
var IntroViz=(function(){
  var DPR=Math.min(2,window.devicePixelRatio||1);
  function lerp(a,b,t){return a+(b-a)*t;}
  function eo(p){return p<0?0:p>1?1:1-Math.pow(1-p,3);}
  function clamp(v,a,b){return v<a?a:v>b?b:v;}
  function rr(g,x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
  function harmNappe(g,cx,cy,r,w,tenu,enc,rate,M,Cc,O,prog){var tot=tenu+enc+rate;g.lineCap='butt';if(tot<=0){g.strokeStyle='rgba(255,255,255,.06)';g.lineWidth=w;g.beginPath();g.arc(cx,cy,r,0,2*Math.PI);g.stroke();return;}var cum=0,bands=[];[[tenu,M],[enc,Cc],[rate,O]].forEach(function(x){if(x[0]>0){bands.push({c:x[1],s:cum/tot,e:(cum+x[0])/tot});}cum+=x[0];});var tw=0.035,stops=[];bands.forEach(function(bd){var twb=Math.min(tw,(bd.e-bd.s)*0.34);stops.push([bd.s+twb,bd.c]);stops.push([bd.e-twb,bd.c]);});function hx(hh){hh=hh.replace('#','');return [parseInt(hh.slice(0,2),16),parseInt(hh.slice(2,4),16),parseInt(hh.slice(4,6),16)];}function mix(a,b,t){var x=hx(a),y=hx(b);return 'rgb('+Math.round(x[0]+(y[0]-x[0])*t)+','+Math.round(x[1]+(y[1]-x[1])*t)+','+Math.round(x[2]+(y[2]-x[2])*t)+')';}var nS=stops.length;function colAt(f){for(var i=0;i<nS;i++){var p0=stops[i][0],c0=stops[i][1],p1=stops[(i+1)%nS][0],c1=stops[(i+1)%nS][1];if(i===nS-1){var seg=1-p0+stops[0][0];if(f>=p0)return mix(c0,c1,(f-p0)/seg);if(f<stops[0][0])return mix(c0,c1,(f+1-p0)/seg);}else if(f>=p0&&f<p1){return mix(c0,c1,(f-p0)/((p1-p0)||1));}}return bands[0].c;}/* L'anneau était redessiné segment par segment — 210 arcs par image, avec un
     décodage des couleurs à chaque segment. D'où les à-coups.
     On peint l'anneau ENTIER une seule fois dans un cache, puis chaque image ne
     fait plus qu'une chose : révéler la portion voulue. La croissance devient
     parfaitement continue, et l'angle final est exact. */
  var key=r+'|'+w+'|'+tenu+'|'+enc+'|'+rate+'|'+M+'|'+Cc+'|'+O;
  if(!harmNappe._c||harmNappe._k!==key){
    var pad=Math.ceil(w/2)+3, side=Math.ceil((r+pad)*2);
    var cv=harmNappe._c||document.createElement('canvas');
    cv.width=side;cv.height=side;
    var q=cv.getContext('2d');
    q.clearRect(0,0,side,side);
    q.lineCap='butt';q.lineWidth=w;
    var mx=side/2,my=side/2,N=360;
    for(var k=0;k<N;k++){
      var f=k/N;
      var a0=-Math.PI/2+f*2*Math.PI;
      var a1=-Math.PI/2+((k+1)/N)*2*Math.PI+0.006;   /* un cheveu de recouvrement : pas de couture */
      q.strokeStyle=colAt(f);q.beginPath();q.arc(mx,my,r,a0,a1);q.stroke();
    }
    harmNappe._c=cv;harmNappe._k=key;harmNappe._p=pad;
  }
  if(prog<=0)return;
  var C2=harmNappe._c, hp=C2.width/2;
  g.save();
  g.beginPath();
  g.moveTo(cx,cy);
  g.arc(cx,cy,r+w,-Math.PI/2,-Math.PI/2+Math.min(1,prog)*2*Math.PI);
  g.closePath();
  g.clip();
  g.drawImage(C2, cx-hp, cy-hp);
  g.restore();
}
  /* ---- TOILE 248x230 (exact) ---- */
  var TW=248,TH=230;
  var T_NAMED=[{x:TW*0.37,y:TH*0.36,txt:["je t'emm\u00e8ne","\u00e0 la mer"],col:[130,174,248]},{x:TW*0.64,y:TH*0.50,txt:["je me remets","au sport"],col:[201,168,245]},{x:TW*0.45,y:TH*0.70,txt:["on s'appelle","dimanche"],col:[221,77,35]}];
  var T_CELLS=[];
  for(var tj=0;tj<T_NAMED.length;tj++){T_CELLS.push({x:T_NAMED[tj].x,y:T_NAMED[tj].y,arr:600+tj*1200,named:tj,grey:0});}
  var T_FILL=[[0.18,0.20],[0.80,0.24],[0.86,0.62],[0.20,0.55],[0.55,0.20],[0.30,0.86],[0.72,0.86],[0.88,0.40],[0.13,0.80],[0.50,0.46],[0.68,0.68]];
  for(var tf=0;tf<T_FILL.length;tf++){T_CELLS.push({x:T_FILL[tf][0]*TW,y:T_FILL[tf][1]*TH,arr:4000+tf*260,named:-1,grey:27+((tf*37)%15)});}
  for(var tk=0;tk<T_CELLS.length;tk++){T_CELLS[tk].ph=Math.random()*6.28;T_CELLS[tk].am=0.6+Math.random()*0.8;}
  var T_LOOP=4000+T_FILL.length*260+700+2600;
  function drawToile(g,t){var W=TW,H=TH,cells=T_CELLS,named=T_NAMED,STEP=4,LOOP=T_LOOP;
  var tt=t%LOOP;
  var fade=tt>LOOP-600?(1-(tt-(LOOP-600))/600):1;
  var Np=cells.length,P=new Array(Np),F=new Float32Array(Np),POP=new Float32Array(Np);
  for(var k=0;k<Np;k++){var s=cells[k];
    // very calm drift
    P[k]={x:s.x,y:s.y};
    F[k]=eo((tt-s.arr)/640)*fade;
    var e=(tt-s.arr-420)/240;POP[k]=Math.exp(-e*e);
  }
  /* REACTION : quand une dalle vient d'arriver, les voisines la repoussent puis se stabilisent */
  var RX=new Float32Array(Np),RY=new Float32Array(Np);
  for(var k=0;k<Np;k++){for(var j=0;j<Np;j++){if(j===k)continue;
    var aj=tt-cells[j].arr; if(aj<0||aj>1500)continue;
    var dx=P[k].x-cells[j].x, dy=P[k].y-cells[j].y, d=Math.sqrt(dx*dx+dy*dy)+0.01;
    if(d>150)continue;
    /* l'onde part de la dalle qui arrive et met d'autant plus de temps que la voisine est loin */
    var delay=d*1.15, u=(aj-delay)/300;
    if(u<0||u>4)continue;
    /* impulsion amortie : les voisines s'écartent puis reviennent se poser */
    var push=Math.sin(u*3.1416)*Math.exp(-u*1.15)*13.5;
    var w=(1-d/150); RX[k]+=dx/d*push*w; RY[k]+=dy/d*push*w;}}
  for(var k=0;k<Np;k++){P[k].x+=RX[k];P[k].y+=RY[k];}
  g.clearRect(0,0,W,H);
  g.fillStyle='rgb(15,18,21)';g.fillRect(0,0,W,H);
  // rendu ENCRE : une tache par dalle, arrivee douce (grandit + s'opacifie), pas de jitter
  var _rad=Math.sqrt(W*H/Math.max(1,Np))*0.66;
  for(var _pass=0;_pass<2;_pass++){
  for(var k=0;k<Np;k++){
    var f=F[k]; if(f<=0.02) continue;
    var s=cells[k], col;
    if((_pass===0)===(s.named>=0)) continue;
    if(s.named>=0){var c=named[s.named].col;var L=0.88+POP[k]*0.12;if(L>1)L=1;
      col=[lerp(15,c[0],L)|0,lerp(18,c[1],L)|0,lerp(28,c[2],L)|0];}
    else{var sh=s.grey|0;col=[sh,(sh+1)|0,(sh+9)|0];}
    var cx=P[k].x, cy=P[k].y;
    var sd=((k+1)*2654435761)>>>0, rr=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};
    var ease=f*f*(3-2*f), gr=0.64+0.36*ease;
    var rscale=(s.named>=0)?1.62:0.82;
    g.fillStyle='rgba('+col[0]+','+col[1]+','+col[2]+','+(0.92*ease).toFixed(3)+')';
    for(var e2=0;e2<8;e2++){
      var ex=cx+(rr()-.5)*_rad*1.2, ey=cy+(rr()-.5)*_rad;
      var rx=_rad*rscale*(0.32+rr()*0.42)*gr, ry=_rad*rscale*(0.16+rr()*0.34)*gr;
      g.save();g.translate(ex,ey);g.rotate(rr()*3.1416);
      g.beginPath();g.ellipse(0,0,rx,ry,0,0,6.2832);g.fill();g.restore();
    }
  }
  }
  // text — bright on arrival, then fades to a quiet label (focus on newest)
  g.textAlign='center';g.textBaseline='middle';g.font='700 12px Gilbert,Gilbert,system-ui,sans-serif';
  for(var j=0;j<named.length;j++){var s=cells[j];var f=eo((tt-s.arr)/460)*fade;if(f<=0.05)continue;
    var recent=clamp(1.25-(tt-s.arr)/1500,0.32,1);var a=f*recent;var c=named[j].col;
    g.save();g.globalAlpha=a;g.shadowColor='rgba('+c[0]+','+c[1]+','+c[2]+','+(0.55*a)+')';g.shadowBlur=14;
    g.fillStyle='#F8F6F2';g.fillText(named[j].txt[0],named[j].x,named[j].y-7);g.fillText(named[j].txt[1],named[j].x,named[j].y+8);g.restore();
  }
}
  /* ---- FIL 242x210 (exact) ---- */
  var FW=242,FH=210,UV=[130,174,248],MV=[201,168,245],TE=[221,77,35];
  var frows=[{who:'Rachel',col:UV,d:200},{who:'Nicolas',col:MV,d:800},{who:'Adrien',col:TE,d:1400},{who:'Maman',col:UV,d:2000},{who:'Leo',col:MV,d:2600}];
  var FLOOP=7600,rowH=36,ftop=8,fmid=FW*0.50,toileCells=null;
  function buildToile(){var c=[],cols=[UV,MV,TE,UV,MV];var cxv=[0.56,0.74,0.58,0.76,0.60];for(var i=0;i<5;i++){c.push({x:lerp(fmid,FW,cxv[i]),y:ftop+i*rowH+12,col:cols[i]});}var fx=[[0.25,0.07],[0.31,0.25],[0.22,0.44],[0.30,0.62],[0.24,0.81],[0.49,0.95],[0.80,0.93],[0.94,0.20],[0.96,0.56],[0.90,0.87]];fx.forEach(function(p,k){c.push({x:lerp(fmid,FW,p[0]),y:p[1]*FH,col:null,grey:23+((k*29)%11)});});return c;}
  function drawFil(g,t){var W=FW,H=FH;g.clearRect(0,0,W,H);var tt=t%FLOOP;
  /* fondu de fin de boucle : sans lui l'écran se vidait d'un coup (écran noir) */
  var ffade=tt>FLOOP-700?1-(tt-(FLOOP-700))/700:1;
  var split=eo(clamp((tt-3700)/1300,0,1)),boundary=W-split*(W-fmid);
  // Fil rows (left)
  for(var i=0;i<frows.length;i++){var r=frows[i];var p=eo((tt-r.d)/420);if(p<=0)continue;var y=ftop+i*rowH,x=lerp(-40,0,p);
    g.save();g.globalAlpha=Math.min(1,p*1.3)*ffade;g.translate(x,0);
    rr(g,10,y,24,24,7);g.fillStyle='rgb('+r.col[0]+','+r.col[1]+','+r.col[2]+')';g.fill();
    g.fillStyle='rgba(228,215,187,.85)';rr(g,42,y+4,52,7,3);g.fill();
    g.fillStyle='rgba(162,148,124,.5)';rr(g,42,y+15,80,6,3);g.fill();
    g.restore();}
  // right : the REAL validated Toile (pixel Voronoï), revealed by a wipe from the right
  if(split>0){if(!toileCells)toileCells=buildToile();var cells=toileCells,STEP=4;
    g.save();g.globalAlpha=ffade;g.beginPath();g.rect(boundary,0,W-boundary,H);g.clip();
    for(var y=0;y<H;y+=STEP){for(var x=Math.floor(fmid/STEP)*STEP-STEP;x<W;x+=STEP){
      var best=1e9,bi=0;for(var k=0;k<cells.length;k++){var dx=x-cells[k].x,dy=y-cells[k].y,d=dx*dx+dy*dy;if(d<best){best=d;bi=k;}}
      var s=cells[bi],r,gg,bb;
      if(s.col){var gl=0.92;r=lerp(13,s.col[0],gl)|0;gg=lerp(16,s.col[1],gl)|0;bb=lerp(26,s.col[2],gl)|0;}
      else{var sh=s.grey;r=sh;gg=sh+1;bb=sh+9;}
      g.fillStyle='rgb('+r+','+gg+','+bb+')';g.fillRect(x,y,STEP+1,STEP+1);}}
    g.restore();
    g.strokeStyle='rgba(255,255,255,.16)';g.lineWidth=1;g.beginPath();g.moveTo(boundary,4);g.lineTo(boundary,H-4);g.stroke();
    g.globalAlpha=split;
    /* le vrai sélecteur segmenté Toile/Fil, à sa place : en HAUT À DROITE de l'écran */
    (function(){
      var sw=76, sh=22, pad=6, sx=W-sw-pad, sy=pad;
      /* cartouche */
      g.fillStyle=(typeof isLightM==='function'&&isLightM())?'rgba(255,255,255,.72)':'rgba(255,255,255,.12)';
      rr(g,sx,sy,sw,sh,11);g.fill();
      /* pastille active (Toile) */
      var half=(sw-4)/2;
      g.fillStyle='#82AEF8';
      rr(g,sx+2,sy+2,half,sh-4,9);g.fill();
      g.textBaseline='middle';g.font='700 8px system-ui';g.textAlign='center';
      g.fillStyle='#fff';g.fillText('Toile',sx+2+half/2,sy+sh/2+0.5);
      g.fillStyle=(typeof isLightM==='function'&&isLightM())?'#A2947C':'rgba(255,255,255,.6)';
      g.fillText('Fil',sx+2+half+half/2,sy+sh/2+0.5);
      g.textBaseline='alphabetic';
    })();
    g.globalAlpha=1;}
}
  /* ---- NUE 242x210 (exact) ---- */
  var NW=242,NH=210;
  var cards=[{x:16,y:16,w:110,h:92,col:[130,174,248],label:'WEEK-END',mem:3,dl:[[130,174,248],[201,168,245],[221,77,35]]},{x:120,y:100,w:110,h:92,col:[201,168,245],label:'FAMILLE',mem:4,dl:[[201,168,245],[130,174,248],[201,168,245]]}];
  var NLOOP=6000;
  function drawNue(g,t){var W=NW,H=NH;g.clearRect(0,0,W,H);var tt=t%NLOOP;
  var gfade=tt>NLOOP-600?1-(tt-(NLOOP-600))/600:1;
  cards.forEach(function(c,ci){var ap=eo(clamp((tt-300-ci*750)/700,0,1))*gfade;if(ap<=0.02)return;
    var bob=(1-ap)*6;
    g.save();g.globalAlpha=ap;g.translate(0,bob);
    rr(g,c.x,c.y,c.w,c.h,18);g.fillStyle='rgba('+c.col[0]+','+c.col[1]+','+c.col[2]+',.20)';g.fill();
    g.lineWidth=1.4;g.strokeStyle='rgba('+c.col[0]+','+c.col[1]+','+c.col[2]+',.72)';g.stroke();
    // theme header + small dot
    g.beginPath();g.arc(c.x+15,c.y+18,3,0,6.28);g.fillStyle='rgb('+c.col[0]+','+c.col[1]+','+c.col[2]+')';g.fill();
    g.fillStyle='#E4D7BB';g.textAlign='left';g.textBaseline='middle';g.font="800 10px Gilbert,system-ui";g.fillText(c.label,c.x+24,c.y+18);
    // stacked member avatars (overlapping) — the invited proches
    for(var m=c.mem-1;m>=0;m--){var mp=eo(clamp((tt-300-ci*750-200-m*110)/300,0,1));if(mp<=0)continue;g.globalAlpha=ap*mp;
      var axx=c.x+18+m*12,ayy=c.y+40;g.beginPath();g.arc(axx,ayy,7,0,6.28);g.fillStyle=m===0?('rgb('+c.col[0]+','+c.col[1]+','+c.col[2]+')'):'#4E4437';g.fill();
      g.lineWidth=2;g.strokeStyle='#1F1605';g.stroke();}
    g.globalAlpha=ap;
    // shared Promi dalles — neat row
    for(var d=0;d<c.dl.length;d++){var dp=eo(clamp((tt-300-ci*750-620-d*150)/300,0,1));if(dp<=0)continue;g.globalAlpha=ap*dp;
      var col=c.dl[d],dx=c.x+15+d*32,dy=c.y+60,s=0.7+0.3*dp;g.save();g.translate(dx+11,dy+11);g.scale(s,s);g.translate(-(dx+11),-(dy+11));
      rr(g,dx,dy,22,22,7);g.fillStyle='rgb('+col[0]+','+col[1]+','+col[2]+')';g.fill();g.restore();}
    g.restore();
  });
}
  /* ---- KAR 242x210 (exact) ---- */
  var KW=242,KH=210,KLOOP=5200;
  function drawKar(g,t){var W=KW,H=KH;var cx=W/2,cy=H*0.45,R=46;g.clearRect(0,0,W,H);var tt=t%KLOOP;
  var nap=eo(clamp(tt/1900,0,1)),crown=eo(clamp((tt-800)/2100,0,1)),fade=tt>KLOOP-700?1-(tt-(KLOOP-700))/700:1;g.globalAlpha=fade;
  var M=(window.KC?KC.Mh:'#C9A8F5'),C=(window.KC?KC.Ch:'#82AEF8'),O=(window.KC?KC.Oh:'#DD4D23');
  var hist=['tenu','tenu','encours','tenu','rate','tenu','tenu','tenu','encours','tenu','rate','tenu','tenu','encours','tenu','rate'];
  var n=hist.length,sc=R/80;
  g.lineCap='butt';g.strokeStyle='rgba(255,255,255,.06)';g.lineWidth=17*sc;g.beginPath();g.arc(cx,cy,R,0,2*Math.PI);g.stroke();
  var tenu=0,enc=0,rate=0;hist.forEach(function(s){if(s==='tenu')tenu++;else if(s==='encours')enc++;else rate++;});
  harmNappe(g,cx,cy,R,16*sc,tenu,enc,rate,M,C,O,nap);
  g.lineCap='round';
  for(var i=0;i<n;i++){var tp=clamp((crown-i/n)/0.20,0,1);if(tp<=0)continue;var p=hist[i];var a=-Math.PI/2+i/n*2*Math.PI;var col=p==='tenu'?M:(p==='rate'?O:C);var e2=p==='encours';
    var r0=99*sc,r1=(p==='tenu'?117:p==='rate'?107:104)*sc;g.strokeStyle=col;g.lineWidth=(e2?1.4:2.4)*(0.6+0.4*tp);g.globalAlpha=fade*(e2?0.42:0.95)*tp;
    g.beginPath();g.moveTo(cx+r0*Math.cos(a),cy+r0*Math.sin(a));g.lineTo(cx+r1*Math.cos(a),cy+r1*Math.sin(a));g.stroke();}
  g.globalAlpha=fade;
  var wa=clamp((nap-0.7)/0.3,0,1);if(wa>0){g.globalAlpha=fade*wa;g.textAlign='center';g.textBaseline='middle';
    g.fillStyle='#E4D7BB';g.font="800 18px Gilbert,system-ui";g.fillText('solide',cx,cy-8);
    g.fillStyle='#A2947C';g.font='600 8px system-ui';g.fillText('HARMONIE',cx,cy+6);
    g.fillStyle='#291547';g.font='700 11px system-ui';g.fillText('78 %',cx,cy+20);}
  g.globalAlpha=1;
}
  var DIM={toile:[TW,TH],fil:[FW,FH],nue:[NW,NH],kar:[KW,KH]},FN={toile:drawToile,fil:drawFil,nue:drawNue,kar:drawKar};
  function run(cv){cancelAnimationFrame(window.IntroVizRAF);if(!cv||!cv.getContext)return;var viz=cv.dataset.viz,d=DIM[viz];if(!d)return;var W=d[0],H=d[1];
    /* k : facteur d'echelle pour tenir dans la place que le telephone laisse. */
    var dk=1;try{dk=parseFloat(getComputedStyle(document.getElementById('promiOnb')).getPropertyValue('--k'))||1;}catch(e){}
    var k=dk,host=cv.parentNode;
    if(host){var bw=host.clientWidth,bh=host.clientHeight;
      if(bw>0&&bh>0)k=Math.max(.55,Math.min(dk,(bw-8)/W,(bh-8)/H));}
    window._obVizK=k;
    cv.width=Math.round(W*k*DPR);cv.height=Math.round(H*k*DPR);cv.style.width=Math.round(W*k)+'px';cv.style.height=Math.round(H*k)+'px';var g=cv.getContext('2d');g.setTransform(DPR*k,0,0,DPR*k,0,0);var fn=FN[viz];var t0=null;function frame(t){if(t0===null)t0=t;fn(g,t-t0);window.IntroVizRAF=requestAnimationFrame(frame);}window.IntroVizRAF=requestAnimationFrame(frame);}
  return {run:run};
})();

var SHARE_FMT={
 storyfull:{a:1290/2796,label:'Plein écran',note:'Plein écran vertical, immersif bord à bord.'},
 story:{a:9/16,label:'Story',note:'Vertical, immersif.'},
 square:{a:1,label:'Post carré',note:'Format propre et universel.'},
 wide:{a:16/9,label:'Paysage',note:'Large — bannière ou post horizontal.'},
 edito:{a:4/5,label:'Édito',note:'Portrait éditorial.'},
 custom:{a:1080/1920,label:'Sur mesure',note:'Dimensions définies à la main.'}
};
var shareFmt='story',shareMode='toile',shareVis=true,wmPos=0,shareZoom=1,shCW=1080,shCH=1920,shPanFX=0,shPanFY=0,shHintOn=false;
var WMPOS=['left','center','right'];var shareHidden={};
function shFmtA(){return shareFmt==='custom'?shCW/shCH:(SHARE_FMT[shareFmt]||SHARE_FMT.story).a;}
function shareFit(a,maxW,maxH){var W,H;if(maxW/maxH>a){H=maxH;W=Math.round(H*a);}else{W=maxW;H=Math.round(W/a);}return[W,H];}
function shActive(){return promises.filter(function(p){return !p.draft && !shareHidden[p.id] && !(p.nuee&&shareHidden['n:'+p.nuee]);});}
function sharePtsInfo(W,H){var act=shActive();var np=act.length||1;var N=Math.max(18,Math.min(90,np*5));var pts=gridPts(W,H,N);var map={};for(var i=0;i<np;i++){var ci=Math.floor((i+1)*0.6180339887*N)%N;var g=0;while(map[ci]!=null&&g<N){ci=(ci+1)%N;g++;}map[ci]=act[i];}return{pts:pts,map:map};}
function shTL(x,y,W,H){return x<W*0.46 && y<H*0.17;}
function shSize(cv,W,H){var dpr=Math.min(3,window.devicePixelRatio||1);cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);cv.style.width='100%';cv.style.height='100%';cv.style.display='block';var g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);return g;}
function shareLabels(cv,W,H,info){try{var g=cv.getContext('2d');var st=STRUCT[state.structure];var cells=voronoi(info.pts,[st.gap,st.gap,W-st.gap,H-st.gap]);g.save();g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';var fs=Math.max(7,Math.min(13,W*0.028));for(var i=0;i<info.pts.length;i++){var p=info.map[i];if(!p)continue;var cl=cells[i];if(!cl||cl.length<3)continue;var c=centroid(cl);if(!c||shTL(c[0],c[1],W,H)||c[1]>H*0.9)continue;var t1=(p.title||p.who||'Promi');var sub=p.nuee?(NUE[p.nuee]||''):(p.who||'');sub=(sub||'').toUpperCase();var _pal=(typeof MOODS!=='undefined'&&MOODS[state.mood])?MOODS[state.mood]:['#888888'];var _cc=(typeof HX==='function')?HX(_pal[p.id%_pal.length]):'#888888';var _ff=(p.status==='rate')?'#392F1B':((typeof RS==='function')?RS(_cc):_cc);var _tc=(typeof textOn==='function')?textOn(_ff):'#161616';g.font='700 '+fs.toFixed(1)+'px Gilbert,system-ui,sans-serif';g.fillStyle=_tc;g.fillText(t1,c[0],c[1]-fs*0.12);g.font='500 '+(fs*0.64).toFixed(1)+'px Atkinson,system-ui,sans-serif';g.globalAlpha=0.72;g.fillText(sub,c[0],c[1]+fs*0.85);g.globalAlpha=1;}g.restore();}catch(e){}}
function shareToile(g,W,H){
  /* On partage la Toile QU'ON VOIT — son monde, sa palette, ses couleurs.
     Avant : ce poster redessinait une mosaïque à partir de cellPolys, les polygones
     de l'ancien moteur SVG — une composition différente, dans un style figé.
     Désormais on prend la Toile elle-même. */
  var TL=window.Toile;
  if(TL&&TL.canvas){
    var src=TL.canvas();
    try{var _wL=(typeof _sealDark!=='undefined')?!_sealDark:null;var _dL=(function(){var d=document.getElementById('device');return !!(d&&d.classList.contains('light'));})();
    /* on rend TOUJOURS par Toile.preview() avec surcharge : le canvas vivant peut
       porter un theme perime, et c'est ce qui empechait le repeint au retour. */
    if(_wL!==null&&TL.preview){
      /* L'apercu est une IMAGE, pas une Toile vivante : on la compose une seule fois
         en haute definition, puis on la reutilise. Elle ne bouge plus, et deux rendus
         successifs donnent exactement la meme image. */
      var _w9=(TL.curWorld?TL.curWorld():'encre');
      /* la cle du cache doit contenir TOUT ce qui change l'image, sinon un
         reglage ne repeint pas. shareVis en faisait partie mais l'expression
         etait cassee par un retour a la ligne : elle valait ''. */
      var _sc9='';
      try{ _sc9 = String(typeof shareVis!=='undefined' ? shareVis : '') + '|'
                + String(window.__shScopeKey || '')
                + '|' + String(window.shNoyau) + '|' + String(window.shNySize)
                + '|' + String(window.shChiffre) + '|' + String(sigOn())
                + '|' + String(window.shNyX) + '|' + String(window.shNyY)
                + '|' + String(window.shNyBR) + '|' + String(window.shNyBC)
                + '|' + String(window.shNyMix) + '|' + String(window.shLabels)
                + '|' + Object.keys(window.shareHidden||{}).sort().join(','); }catch(_){}
      /* ⚑ v29 — LA TOILE SE REND À L'ÉCHELLE OÙ ELLE SERA POSÉE (redteam_decoupe, famille D) : on calcule
         d'abord le cadrage (couverture × zoom), puis on demande au moteur la Toile à cette échelle, posée 1:1. */
      var _tcv=document.getElementById('toileCv'), _dT=(TL.vue&&TL.vue().dpr)||2;
      var _Wt=_tcv?_tcv.width/_dT:390, _Ht=_tcv?_tcv.height/_dT:844;
      var _Tg=g.getTransform(), _sxg=Math.hypot(_Tg.a,_Tg.b)||1;
      var _ech9=Math.max(W/_Wt, H/_Ht)*(shareZoom||1)*_sxg;
      var _k9=[_w9,_wL,_sc9,Math.round(W),Math.round(H),_ech9.toFixed(4)].join('~');
      var _tc9=shareToile._tc||(shareToile._tc=document.createElement('canvas'));
      if(shareToile._key!==_k9){
        /* CHANTIER 1 : renderTo garde les vrais germes. preview() n'est plus
           qu'un repli si renderTo echoue. */
        var _fait=false;
        /* CHANTIER 39 — « Avec / Sans texte » redevient effectif sur Ma Toile :
           renderTo passe par labelsOn(), on lui impose shareVis le temps du
           rendu. Sans ca le bouton basculait son etat sans rien changer. */
        /* un drapeau plutot qu'un remplacement de fonction : plus simple
           a suivre, et rien a restaurer si le rendu leve. */
        /* le bouton ecrit window.shLabels ; l'apercu lisait shareVis.
           Deux noms pour une meme intention — on lit la source du bouton. */
        try{ window._shLabels=(window.shLabels===undefined)?true:!!window.shLabels; }catch(_l){}
        var _D9=window._toileDPR?window._toileDPR():2;   /* ⚑ v16 : la densité de la Toile, pas ×2 en dur */
        try{ if(TL.renderTo) _fait=TL.renderTo(_tc9,_ech9,_wL); }catch(_r){}
        try{ window._shLabels=undefined; }catch(_l2){}
        if(!_fait){
          _tc9.width=Math.max(2,Math.round(W*_D9));_tc9.height=Math.max(2,Math.round(H*_D9));
          var _st9=window._shThemeOverride;window._shThemeOverride=_wL;
          TL.preview(_tc9,_w9,W,H);
          window._shThemeOverride=(_st9===undefined?null:_st9);
        }
        shareToile._key=_k9;
      }
      src=_tc9;}}catch(e){}
    if(src&&src.width&&src.height){
      var lightT=(typeof _sealDark!=="undefined")?!_sealDark:(TL.isLight?TL.isLight():true);
      g.clearRect(0,0,W,H);
      /* le decoupage arrondi doit venir AVANT le fond : sinon le fond
         remplit les coins et l'arrondi ne se voit pas. */
      var _rc=Math.round(Math.min(W,H)*0.022), _clipOk=false;
      try{ if(g.roundRect){ g.save(); g.beginPath();
        g.roundRect(0,0,W,H,_rc); g.clip(); _clipOk=true; } }catch(_){}
      g.fillStyle=lightT?'#EFE2C5':'#120E05';
      g.fillRect(0,0,W,H);
      /* on cadre la Toile dans le poster, sans jamais la déformer — ⚑ v29 : déjà rendue à la bonne échelle */
      var _sxp=Math.hypot(g.getTransform().a,g.getTransform().b)||1;
      var dw=src.width/_sxp, dh=src.height/_sxp;
      var dx=(W-dw)/2 + (shPanFX||0)*W, dy=(H-dh)/2 + (shPanFY||0)*H;
      g.imageSmoothingEnabled=false;              /* la mosaïque reste nette */
      /* CHANTIERS 9 et 22 — le decoupage est pose plus haut, avant le fond.
         On ne touche pas a la pile suspecte de cette fonction : le save
         et le restore sont apparies ici meme, autour du seul dessin. */
      try{ window._poseUn(g, src, dx+dw/2, dy+dh/2); }catch(e){}
      if(_clipOk){try{g.restore();}catch(_){}}
      g.imageSmoothingEnabled=true;
      return;
    }
  }
  var light=isLight();g.clearRect(0,0,W,H);g.fillStyle=light?'#E6DDC8':'#201908';g.fillRect(0,0,W,H);var polys=cellPolys;if(!polys||!polys.length)return;var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;polys.forEach(function(c){c.poly.forEach(function(pt){if(pt[0]<minx)minx=pt[0];if(pt[0]>maxx)maxx=pt[0];if(pt[1]<miny)miny=pt[1];if(pt[1]>maxy)maxy=pt[1];});});var bw=maxx-minx,bh=maxy-miny;if(bw<=0||bh<=0)return;var s=Math.min(W/(bw*1.12),H/(bh*1.12))*shareZoom;var ox=W/2-(minx+bw/2)*s+shPanFX*W,oy=H/2-(miny+bh/2)*s+shPanFY*H;var st=STRUCT[state.structure],pal=MOODS[state.mood];g.lineJoin='round';polys.forEach(function(c){var p=null;for(var j=0;j<promises.length;j++){if(promises[j].id===c.id){p=promises[j];break;}}var cl=c.poly.map(function(pt){return [ox+pt[0]*s,oy+pt[1]*s];});var col=p?RS(HX(pal[p.id%pal.length])):'rgba(140,140,150,.45)';var path=null;try{path=new Path2D(roundPath(cl,Math.max(1,(st.round||2)*s*0.5)));}catch(e){path=null;}if(path){g.fillStyle=col;g.fill(path);var stroke=st.stroke==='chrome'?'#D5CAC1':st.stroke;if(stroke&&stroke!=='none'){g.strokeStyle=stroke;g.lineWidth=Math.max(1,(st.sw||1)*s);g.stroke(path);}}else{g.beginPath();cl.forEach(function(pt,i){i?g.lineTo(pt[0],pt[1]):g.moveTo(pt[0],pt[1]);});g.closePath();g.fillStyle=col;g.fill();}});if(shareVis){g.save();g.textAlign='center';g.textBaseline='middle';polys.forEach(function(c){var p=null;for(var j=0;j<promises.length;j++){if(promises[j].id===c.id){p=promises[j];break;}}if(!p)return;var ct=centroid(c.poly);if(!ct)return;var x=ox+ct[0]*s,y=oy+ct[1]*s;if(shTL(x,y,W,H))return;var fs=Math.max(7,Math.min(15,s*8));var t1=(p.title||p.who||'');var _pal2=(typeof MOODS!=='undefined'&&MOODS[state.mood])?MOODS[state.mood]:['#888888'];var _cc2=(typeof HX==='function')?HX(_pal2[p.id%_pal2.length]):'#888888';var _ff2=(p.status==='rate')?'#392F1B':((typeof RS==='function')?RS(_cc2):_cc2);var _tc2=(typeof textOn==='function')?textOn(_ff2):'#161616';g.font='700 '+fs.toFixed(1)+'px Gilbert,system-ui,sans-serif';g.fillStyle=_tc2;g.fillText(t1,x,y);});g.restore();}}
/* Le Noyau pose : un anneau seul, sans aucun fond. Le sceau de l'Aura embarque le sien,
   c'est pour ca qu'un rectangle apparaissait sur l'epreuve. */
/* Le Noyau de Partager EST celui de l'Aura : on passe par karmaRing(), la fonction
   qui dessine deja l'anneau avec ses fondus organiques entre les trois encres.
   Aucun second dessin, donc aucun ecart possible avec l'Aura. */
/* La signature de l'app, c'est .sig : Fraunces PLUS la double encre decalee.
   Le canvas n'a pas text-shadow, donc trois passes. Les decalages sont ceux
   de .sig (-2.2 / 1.4 et 1.8 / -0.9 a 19 px), exprimes en fraction de corps. */
function sigOn(){try{var s=document.getElementById('shareScreen');
  return !!(s&&s.classList.contains('sh-sig'));}catch(e){return true;}}
function _sigText(g,txt,x,y,taille,encre){
  var f=Math.max(8,taille);
  /* Le mot-marque de l'image et le % disent la MEME chose : si l'un est en
     Bricolage, l'autre aussi. sh-sig porte l'etat du mot-marque. */
  var sig=true;
  try{var s=document.getElementById('shareScreen');
      sig=!!(s&&s.classList.contains('sh-sig'));}catch(_){}
  if(!sig){
    /* Bricolage : pas de double encre, c'est le wordmark simple */
    g.font='700 '+Math.round(f)+'px Gilbert,system-ui,sans-serif';
    g.fillStyle=encre; g.fillText(txt,x,y);
    return;
  }
  /* ⚑ v23 : Fraunces est retirée. Cette branche était MORTE — `sh-sig` n'a plus de porte
     depuis lot-ACCUEIL, et le `return` ci-dessus sort toujours. On garde la double encre
     sur la pile du mot-marque, pour qu'aucune police non embarquée ne soit appelée (§6). */
  g.font='400 '+Math.round(f)+'px PromiLate,Gilbert,system-ui,sans-serif';
  /* les decalages de .sig : -0.116 / 0.074 em et 0.095 / -0.047 em */
  g.fillStyle='#DD4D23'; g.fillText(txt, x - f*0.116, y + f*0.074);
  g.fillStyle='#82AEF8'; g.fillText(txt, x + f*0.095, y - f*0.047);
  g.fillStyle=encre;     g.fillText(txt, x, y);
  /* LA DOUBLE ENCRE, PUBLIÉE. Même raison que `window._plancheComp` : la compter au pixel
     dans le trou de l'anneau mesure la Toile qui respire derrière, pas la signature —
     `le % porte la double encre bleue` sortait KO sur un passage sur trois, `delta 0`, sur
     une app inchangée. On publie ce qui est ÉCRIT : le mot, ses deux décalages, ses encres. */
  try{ window._sigEncres={mot:txt, taille:Math.round(f),
                          encres:['#DD4D23','#82AEF8',String(encre)],
                          decal:[[-0.116,0.074],[0.095,-0.047],[0,0]]}; }catch(_){ }
}
/* Le trou de l'anneau fait 0.40*D (drawKRing : R=0.30*D, lw=0.20*D).
   On y inscrit un carre de cote 0.707*trou, puis on reduit le corps jusqu'a
   ce que le bloc « chiffre + % » y tienne vraiment — mesure, pas estime. */
function _sigBloc(g,pct,cx,cy,D,encre){
  /* ═══ LA SIGNATURE, PUBLIÉE ═══ Même raison que `window._plancheComp` : un contrôle qui
     compte des pixels clairs dans le trou de l'anneau mesure la respiration du monde
     derrière lui, pas le chiffre. On publie donc CE QUI EST COMPOSÉ — le chiffre écrit, sa
     boîte, son encre — et le contrôle compare ça. Posé À L'ENTRÉE de la fonction : sa seule
     présence prouve que le chiffre a été composé, pas seulement demandé. */
  try{ window._noyauSig={pct:pct, cx:Math.round(cx), cy:Math.round(cy),
                         D:Math.round(D), encre:encre, t:(window._noyauSigN=(window._noyauSigN||0)+1)}; }catch(_){ }
  /* le trou suit la geometrie de l'anneau, jamais une valeur recopiee */
  var rTrou=D*((window.KR_R||0.33)-(window.KR_LW||0.14)/2);
  var trou=rTrou*2, cote=trou*0.707;
  /* le carre inscrit est trop prudent : le chiffre tient dans une ELLIPSE,
     pas dans un carre. On part plus grand et on laisse la mesure decider. */
  var f=Math.min(D*0.34, cote*0.86);
  var txt=String(pct), sf;
  for(var k=0;k<24;k++){
    g.font='700 '+Math.round(f)+'px Gilbert,system-ui,sans-serif';
    var lg=g.measureText(txt).width;
    sf=Math.max(8,f*0.34);
    var haut=f*0.78+sf*1.15;                  /* chiffre + signe, empiles */
    /* largeur : le diametre du trou moins une marge · hauteur : idem */
    if(lg<=trou*0.72 && haut<=trou*0.66) break;
    f*=0.93;
    if(f<8){f=8;break;}
  }
  sf=Math.max(8,f*0.34);
  var haut=f*0.78+sf*1.15;
  var yTop=cy-haut/2;
  g.textAlign='center';
  _sigText(g,txt,cx,yTop+f*0.78,f,encre);
  /* le signe % : simple, sans double encre — un seul effet signature par bloc,
     porte par le chiffre. Deux effets superposes se lisaient comme un decalage. */
  g.globalAlpha=.5;
  g.font='700 '+Math.round(sf)+'px Gilbert,system-ui,sans-serif';
  g.fillStyle=encre;
  g.fillText('%',cx,yTop+f*0.78+sf*1.05);
  g.globalAlpha=1;
}
function _shPoseNoyau(g,W,H){try{
 if(!window.shNoyau)return;
 var act=[]; try{var _h=window.shareHidden||{};
   /* un Promi masque au partage ne prend pas de case : la planche se
      reorganise autour, comme si on l'avait retire. */
   act=promises.filter(function(p){return !p.draft&&!p.req&&!_h[p.id];});}catch(e){}
 var t=0,e2=0,r2=0;
 for(var i=0;i<act.length;i++){var st=act[i].status;
  if(st==='tenu')t++; else if(st==='rate')r2++; else e2++;}
 if(!(t+e2+r2)){t=1;}
 var f={s:0.26,m:0.36,l:0.48}[window.shNySize||'m'];
 var _ar=H>0?W/H:1; if(_ar>0.75)f*=0.72; if(_ar>1.2)f*=0.82;
 var D=Math.round(Math.min(W,H)*f);
 /* position libre : 0.5/0.5 par defaut, deplacable au doigt */
 var nx=(window.shNyX===undefined?0.5:window.shNyX);
 var ny2=(window.shNyY===undefined?0.5:window.shNyY);
 var cx=W*nx, cy=H*ny2;
 var key=[t,e2,r2,D].join('~');
 if(_shPoseNoyau._key!==key||!_shPoseNoyau._cv){
  var host=document.createElement('div');
  host.innerHTML=karmaRing(e2,t,r2,Math.round(D/2),null);
  var c=host.querySelector('canvas'); if(!c)return;
  document.body.appendChild(host);
  host.style.cssText='position:fixed;left:-9999px;top:0;opacity:0;pointer-events:none';
  /* c'est drawKRing qui peint les canvas produits par karmaRing */
  try{if(typeof drawKRing==='function')drawKRing(c);}catch(_){}
  _shPoseNoyau._cv=c; _shPoseNoyau._host=host; _shPoseNoyau._key=key;
 }
 var sc=_shPoseNoyau._cv; if(!sc||!sc.width)return;
 var _tr=g.getTransform?g.getTransform():null;
 g.setTransform(1,0,0,1,0,0);
 g.drawImage(sc,cx-D/2,cy-D/2,D,D);
 if(window.shChiffre){
  var pct=Math.round(100*t/Math.max(1,t+e2+r2));
  var clair=false; try{clair=(typeof _sealDark!=='undefined')?!_sealDark:false;}catch(_){}
  var _enc=clair?'#201908':'#F3E7D1';
  _sigBloc(g,pct,cx,cy,D,_enc);
 }
 if(_tr&&g.setTransform)g.setTransform(_tr);
}catch(e){}}
function _shPreviewQR(g,W,H){try{if(typeof _shShowQR!=='undefined'&&!_shShowQR)return;var _q=(typeof _sealQR==='function'?_sealQR():null);if(!_q)return;var _qrRight=!(typeof wmPos!=='undefined'&&wmPos===2);var _cl=Math.max(1,Math.round(W*0.0042));var _qsz=_cl*_q.size;var pad=Math.round(W*0.045);var _qx=_qrRight?(W-_qsz-pad):pad;var _qy=H-_qsz-pad;g.save();g.setTransform(1,0,0,1,0,0);g.fillStyle='#F7F0DE';g.fillRect(_qx-_cl*2,_qy-_cl*2,_qsz+_cl*4,_qsz+_cl*4);g.fillStyle='#1C1402';for(var a=0;a<_q.size;a++){for(var bb=0;bb<_q.size;bb++){if(_q.mod[a][bb])g.fillRect(_qx+bb*_cl,_qy+a*_cl,_cl,_cl);}}g.restore();}catch(e){}}
/* La planche « Mes Promi » : une case par Promi, sa dalle dans la couleur de son etat,
   son intitule dessous. C'est le poster du moodboard, plus une mosaique decorative. */
function sharePlanche(cv,W,H,dprForce){
 /* ⚑ v15 · l'export compose à la taille de l'APERÇU et peint à sa propre résolution
    (`dprForce`) : recomposée à 3840, la planche arrondissait autrement la taille des
    titres, les coupait autrement, et rangeait les cases dans un autre ordre. */
 var dpr=dprForce||Math.min(3,window.devicePixelRatio||1);
 cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
 var g=cv.getContext('2d'); if(!g)return; g.setTransform(dpr,0,0,dpr,0,0);
 var clair=false;
 try{clair=(typeof _sealDark!=='undefined')?!_sealDark:!!(document.getElementById('device')&&
  document.getElementById('device').classList.contains('light'));}catch(e){}
 var ground=clair?'#E8D3B0':'#201502', ink=clair?'#201908':'#F3E7D1';
 g.fillStyle=ground; g.fillRect(0,0,W,H);
 var act=[]; try{var _h=window.shareHidden||{};
   /* un Promi masque au partage ne prend pas de case : la planche se
      reorganise autour, comme si on l'avait retire. */
   act=promises.filter(function(p){return !p.draft&&!p.req&&!_h[p.id];});}catch(e){}
 if(!act.length){g.fillStyle=ink;g.globalAlpha=.5;
  g.font='500 '+Math.round(W*0.042)+'px Atkinson,system-ui,sans-serif';g.textAlign='center';
  g.fillText('ta première promesse t\u2019attend',W/2,H/2);g.globalAlpha=1;return;}
 /* ═══ LA COMPOSITION DE LA PLANCHE, PUBLIÉE ═══
    Un contrôle qui compte des PIXELS sur cette planche mesure la respiration des mondes,
    pas la composition : `dalleTrame` anime la matière avec `performance.now()` et recadre
    au plus juste sur l'alpha. C'est ce qui faisait osciller « Mes Promi : les intitulés
    restent » depuis le début du projet — le comptage de pixels clairs sortait un spectre
    continu, figé par passage. Ce qu'il faut comparer, c'est CE QUI EST COMPOSÉ : quels
    intitulés, à quelles cases. On le publie ici, comme `window._nueeSemis` le fait pour le
    semis d'une Nuée. Même principe, même raison. */
 var _comp=[];
 var COL={tenu:'#C9A8F5',encours:'#82AEF8',rate:'#DD4D23'};
 /* Toile.dalleTrame() rend la dalle reelle d'un Promi dans le monde actif.
    _pdImgs et PROMI_DALLES vivent dans une IIFE : ils ne sont pas accessibles ici. */
 /* ⚑ v15 · pendant qu'on DÉPLACE la Pelote, la planche se recompose à chaque case
    franchie : 18 `dalleTrame` par passe coûtaient ~130 ms (mesuré), le doigt aurait
    traîné. Le cache par id tient le temps du geste (§4 : « un cache par id, le temps
    de la passe » — ici la passe est le geste), et il tombe au lâcher. */
 var _cache=(window._shPelPrise&&window._shPlancheCache)?window._shPlancheCache:{};
 if(window._shPelPrise) window._shPlancheCache=_cache; else window._shPlancheCache=null;
 function _dalleReelle(pid){
  if(_cache[pid]!==undefined)return _cache[pid];
  var t=null;
  try{ if(window.Toile&&window.Toile.dalleTrame&&window.Toile.dalleAbs){
    var d=window.Toile.dalleAbs(pid);
    if(d&&d.w){ var c=document.createElement('canvas');
      if(window.Toile.dalleTrame(c,pid,1)&&c.width>2)t=c; } } }catch(e){}
  _cache[pid]=t; return t;
 }
 /* ⚑ 23 SEPTEMBRE 2026, troisieme tour (Tom) — LE FOLIO : LES TITRES SUR DEUX LIGNES, LA
    GRILLE QUI S'ADAPTE, ET LA PELOTE DANS SON BLOC.
    LE DEFAUT, VU A LA CAPTURE : les titres etaient traces sur UNE ligne, centres, sans
    mesure et sans coupe — « le grand plongeoimonter la serre avant lesprendre l'arrosage
    autecuperer les plants de t… ». Quatre libelles se chevauchaient sur la meme rangee.
    CE QUI CHANGE, ET RIEN D'AUTRE :
      1 · un titre se MESURE (`measureText`) et se coupe aux MOTS, deux lignes au plus ;
          au-dela, points de suite sur la seconde. Jamais de reduction de taille (§6).
      2 · une rangee prend la hauteur de son titre LE PLUS HAUT — les rangees a une ligne
          ne s'espacent pas comme celles a deux. La hauteur totale se recalcule, et la
          planche reste centree.
      3 · LES TITRES LONGS SE REGROUPENT : on emet d'abord les une-ligne, puis les
          deux-lignes, chaque groupe dans son ordre. C'est le rangement qui coute le moins
          de hauteur — mesure : 5 rangees au lieu de 5, mais 2 rangees hautes au lieu de 4.
      4 · LE BLOC 2x2 porte LA PELOTE (`window.shPelote`), plus le Noyau : on ne partage
          plus son Noyau (Q284). Le mecanisme de reservation ne change pas — il etait deja
          ecrit pour deux cases sur deux, et il tient.
    ⚠ RIEN NE SE SUPERPOSE, RIEN NE DISPARAIT : les quatre cases du bloc sont ENJAMBEES,
    les dalles se rangent autour dans l'ordre, et la planche compte `n + 4` cases. */
 var n=act.length;
 var cols=n<=6?2:(n<=12?3:(n<=24?4:5));
 var pad=W*0.075, gap=W*0.028;
 var cw=(W-pad*2-gap*(cols-1))/cols;
 /* ⚑ LA PLANCHE TIENT DANS SON CADRE — c'est la règle de base de Tom, et elle se mesure.
    Avec les titres sur deux lignes et le bloc de la Pelote, six rangées au lieu de cinq :
    la dernière venait écrire SUR le mot-marque, en bas à gauche. On réserve sa bande
    (`BAS`, la hauteur du mot-marque et sa marge) et, si la composition dépasse encore, la
    CASE rétrécit — jamais le texte seul : tout suit, la dalle comme son titre, et le
    rapport ne bouge pas. On itère, parce que la coupe d'un titre dépend de la largeur. */
 var BAS=Math.max(W*0.045*2+W*0.028, H*0.055);
 var lab, LH, SOUS;
 function cotes(){ lab=Math.max(7,Math.round(cw*0.115)); LH=lab*1.28; SOUS=lab*1.5;
   g.font='500 '+lab+'px Atkinson,system-ui,sans-serif'; }
 cotes();
 /* — 1 · le titre, mesure puis coupe aux mots, deux lignes au plus — */
 function coupe(t){
   t=(t||'').trim(); if(!t) return [];
   if(g.measureText(t).width<=cw) return [t];
   var mots=t.split(/\s+/), l1='', i=0;
   while(i<mots.length){ var e=l1?l1+' '+mots[i]:mots[i];
     if(g.measureText(e).width>cw && l1) break; l1=e; i++; }
   var reste=mots.slice(i).join(' ');
   if(!reste) return [l1];
   if(g.measureText(reste).width<=cw) return [l1,reste];
   while(reste.length>1 && g.measureText(reste+'…').width>cw) reste=reste.slice(0,-1);
   return [l1, reste.replace(/\s+$/,'')+'…'];
 }
 var sansLab=(window.shLabels===false);
 var ITEMS=[];
 function mesureTitres(){ ITEMS=act.map(function(p){ var L=sansLab?[]:coupe(p.title);
   return {p:p, L:L, nl:Math.max(1,L.length)}; }); }
 mesureTitres();
 /* — 3 · on regroupe : les une-ligne d'abord, les deux-lignes ensuite — */
 if(!sansLab){ var A=[],B=[];
   ITEMS.forEach(function(it){ (it.nl>1?B:A).push(it); });
   ITEMS=A.concat(B); }
 /* — 4 · le bloc de la Pelote : deux cases sur deux, enjambees — */
 var pel=!!window.shPelote, pelIdx=-1, skip={};
 if(pel&&cols>=2){
   var r0=Math.max(0,(window.shPelBR===undefined?1:window.shPelBR));
   var c0=Math.max(0,Math.min(cols-2,(window.shPelBC===undefined?0:window.shPelBC)));
   /* ⚑ v15 · on peut désormais poser la Pelote où l'on veut : plus bas que la dernière
      rangée utile, elle laisserait des rangées VIDES au-dessus d'elle. Borne : les
      n + 4 cases, pas une de plus. */
   r0=Math.min(r0, Math.max(0, Math.ceil((n+4)/cols)-2));
   pelIdx=r0*cols+c0;
   skip[r0*cols+c0]=1; skip[r0*cols+c0+1]=1;
   skip[(r0+1)*cols+c0]=1; skip[(r0+1)*cols+c0+1]=1;
 }
 /* — on attribue les cases, puis on mesure chaque rangee — */
 var place=[], slot=0, maxSlot=0;
 for(var i=0;i<ITEMS.length;i++){
   while(skip[slot]) slot++;
   place.push(slot); if(slot>maxSlot) maxSlot=slot; slot++;
 }
 for(var k in skip){ var kk=+k; if(kk>maxSlot) maxSlot=kk; }
 var rows=Math.floor(maxSlot/cols)+1;
 /* — 2 · la hauteur d'une rangee suit son titre le plus haut — */
 var nlRow, hRow, yRow, totH;
 function mesureRangees(){
   nlRow=[]; for(var r=0;r<rows;r++) nlRow.push(1);
   ITEMS.forEach(function(it,ix){ var r=Math.floor(place[ix]/cols);
     if(it.nl>nlRow[r]) nlRow[r]=it.nl; });
   hRow=nlRow.map(function(nl){ return sansLab ? cw+lab*0.6 : cw+SOUS+(nl-1)*LH+lab*0.7; });
   yRow=[]; var acc=0;
   for(var r2=0;r2<rows;r2++){ yRow.push(acc); acc+=hRow[r2]+gap; }
   totH=acc-gap;
 }
 mesureRangees();
 /* ⚠ ON ITÈRE : rétrécir la case change la coupe des titres, donc le nombre de lignes,
    donc la hauteur. Quatre tours suffisent — mesuré, ça converge au deuxième. */
 var dispo=H-pad-BAS;
 for(var t9=0; t9<4 && totH>dispo; t9++){
   cw=Math.max(8, cw*Math.max(0.55, dispo/totH));
   cotes(); mesureTitres();
   if(!sansLab){ var A9=[],B9=[]; ITEMS.forEach(function(it){ (it.nl>1?B9:A9).push(it); }); ITEMS=A9.concat(B9); }
   mesureRangees();
 }
 var y0=Math.max(pad,(H-BAS-totH)/2);
 try{ cv.setAttribute('data-planche',[Math.round(cw),rows,Math.round(totH),Math.round(dispo)].join(',')); }catch(_){}
 g.textAlign='center'; g.textBaseline='alphabetic';
 for(var i2=0;i2<ITEMS.length;i2++){
   var it2=ITEMS[i2], p=it2.p, s=place[i2];
   var x=pad+(s%cols)*(cw+gap), y=y0+yRow[Math.floor(s/cols)];
   var col=COL[p.status]||COL.encours;
   g.save(); g.translate(x+cw/2,y+cw/2);
   /* ⚑ v29 — la dalle rendue par le moteur à la taille de SA case, posée 1:1 (redteam_decoupe) */
   var tile=window._poseDalle?window._poseDalle(g,p.id,-cw/2,-cw/2,cw,cw):null;
   if(tile){
   } else { var rd=cw*0.44; g.beginPath();
     g.moveTo(0,-rd);
     g.bezierCurveTo(rd*0.72,-rd*1.02,rd*1.04,-rd*0.42,rd*0.94,rd*0.16);
     g.bezierCurveTo(rd*0.86,rd*0.78,rd*0.32,rd*1.04,-rd*0.14,rd*0.96);
     g.bezierCurveTo(-rd*0.74,rd*0.86,-rd*1.04,rd*0.34,-rd*0.92,-rd*0.22);
     g.bezierCurveTo(-rd*0.82,-rd*0.76,-rd*0.42,-rd*0.98,0,-rd);
     g.closePath(); g.fillStyle=col; g.fill(); }
   g.restore();
   if(sansLab) continue;
   g.fillStyle=ink; g.globalAlpha=.82;
   g.font='500 '+lab+'px Atkinson,system-ui,sans-serif';
   for(var li=0;li<it2.L.length;li++) g.fillText(it2.L[li], x+cw/2, y+cw+SOUS+li*LH);
   g.globalAlpha=1;
   _comp.push({id:p.id, mot:it2.L.join(' '), lignes:it2.L.length,
               x:Math.round(x), y:Math.round(y), cw:Math.round(cw), lab:Math.round(lab*10)/10});
 }
 window._plancheComp={n:_comp.length, mots:_comp.map(function(c){return c.mot;}),
                      cases:_comp, noyau:false, pelote:pel,
                      rangees:nlRow.slice(), cols:cols};
 /* — la Pelote dans son bloc — */
 if(pel&&pelIdx>=0){
   var nr=Math.floor(pelIdx/cols), nc=pelIdx%cols;
   var bx=pad+nc*(cw+gap), by=y0+yRow[nr];
   var bw=cw*2+gap, bh=(hRow[nr]||cw)+gap+(hRow[nr+1]||hRow[nr]||cw);
   var D=Math.round(Math.min(bw,bh)*0.92);
   /* ⚑ v15 · LA GÉOMÉTRIE DU BLOC ET DE LA GRILLE, PUBLIÉE — le geste qui déplace la
      Pelote s'y prend (où est-elle ? quelle case vise le doigt ?), et un juge la lit. */
   window._plancheComp.bloc={r:nr, c:nc, x:bx, y:by, w:bw, h:bh, D:D};
   window._plancheComp.grille={W:W, H:H, pad:pad, gap:gap, cw:cw, y0:y0,
     yRow:yRow.slice(), hRow:hRow.slice(), cols:cols, rows:rows,
     maxR:Math.max(0, Math.ceil((n+4)/cols)-2)};
   try{
     var src=window._aura&&window._aura.pelote?window._aura.pelote():null;
     var pr=window._shPelPrise;
     if(src&&src.width){
       if(pr){
         /* PRISE : sa place reste vide — c'est là qu'elle tombera — et elle suit le
            doigt, un peu plus grande, comme un objet qu'on soulève. */
         var Dp=D*1.06;
         g.drawImage(src, pr.x-Dp/2, pr.y-Dp/2, Dp, Dp);
       } else g.drawImage(src, bx+(bw-D)/2, by+(bh-D)/2, D, D);
     }
   }catch(e){}
 }
 try{_grain(g,W,H,.4);}catch(e){}
}
function shareMosaicFull(cv,W,H){var dpr=Math.min(3,window.devicePixelRatio||1);cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);var g=cv.getContext("2d");g.setTransform(dpr,0,0,dpr,0,0);var pal=(typeof SIGNAL!=="undefined"?SIGNAL:[[201,168,245],[130,174,248],[221,77,35],[41,21,71]]);var sd=98765;function rnd(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;}var base=Math.max(26,W/8.5),gc=Math.max(3,Math.round(W/base)),gr=Math.max(4,Math.round(H/base)),cw=W/gc,ch=H/gr;var seeds=[];for(var r=0;r<gr;r++){for(var c=0;c<gc;c++){var pi=Math.floor(rnd()*pal.length);seeds.push({x:cw*(c+.5)+(rnd()-.5)*cw*.52,y:ch*(r+.5)+(rnd()-.5)*ch*.52,col:pal[pi],ph:rnd()*6.28});}}g.fillStyle=((typeof _sealDark!=="undefined")?!_sealDark:(document.getElementById("device")&&document.getElementById("device").classList.contains("light")))?"#F7F0DE":"#1A1100";g.fillRect(0,0,W,H);var rad=Math.sqrt(W*H/Math.max(1,seeds.length))*0.72;var _wd=(window.Toile&&window.Toile.curWorld?window.Toile.curWorld():"encre");seeds.forEach(function(s,k){var col=s.col;var L=0.72+0.28*(0.5+0.5*Math.sin(s.ph*3));var c0=Math.round(col[0]*(0.55+0.45*L)+18*(1-L)),c1=Math.round(col[1]*(0.55+0.45*L)+18*(1-L)),c2=Math.round(col[2]*(0.55+0.45*L)+26*(1-L));var sd2=((k+1)*2654435761)>>>0;var rr=function(){sd2=(sd2*1103515245+12345)&0x7fffffff;return sd2/0x7fffffff;};g.fillStyle="rgba("+c0+","+c1+","+c2+",0.94)";if(_wd==="pixel"||_wd==="gravure"){var _bw=cw*0.9,_bh=ch*0.9;g.fillRect(s.x-_bw/2,s.y-_bh/2,_bw,_bh);}else if(_wd==="mosaique"){var _sz=Math.min(cw,ch)*0.86;g.save();g.translate(s.x,s.y);g.rotate((rr()-.5)*0.5);g.fillRect(-_sz/2,-_sz/2,_sz,_sz);g.restore();}else if(_wd==="braille"){for(var _d=0;_d<6;_d++){var _dx=s.x+(rr()-.5)*cw*0.7,_dy=s.y+(rr()-.5)*ch*0.7;g.beginPath();g.arc(_dx,_dy,rad*0.26,0,6.2832);g.fill();}}else if(_wd==="sillons"){g.save();g.lineCap="round";g.strokeStyle=g.fillStyle;g.lineWidth=rad*0.34;for(var _l=0;_l<4;_l++){var _ly=s.y+(_l-1.5)*rad*0.42;g.beginPath();g.moveTo(s.x-rad*0.9,_ly+(rr()-.5)*4);g.lineTo(s.x+rad*0.9,_ly+(rr()-.5)*4);g.stroke();}g.restore();}else{for(var e2=0;e2<8;e2++){var ex=s.x+(rr()-.5)*rad*1.25,ey=s.y+(rr()-.5)*rad*1.1;var rx=rad*(0.36+rr()*0.44),ry=rad*(0.2+rr()*0.36);g.save();g.translate(ex,ey);g.rotate(rr()*3.1416);g.beginPath();g.ellipse(0,0,rx,ry,0,0,6.2832);g.fill();g.restore();}}});}
function shareRender(){try{if(window.shFond)shFond();if(window.shFoot)setTimeout(shFoot,0);
 if((window._shP|0)<2){window._shP=(window._shP|0)+1;
  setTimeout(function(){try{shareRender();}catch(_){}},150);}
}catch(e){}var wrap=$('#shWrap');if(!wrap)return;var _shDev=document.getElementById('device');var _shHadL=_shDev&&_shDev.classList.contains('light');var _shWantL=(typeof _sealDark!=='undefined')?!_sealDark:_shHadL;var _shFlip=(!!_shDev&&_shWantL!==_shHadL);/* On ne touche plus au theme du device ni a la Toile vivante : l'apercu se rend
   par Toile.preview() avec surcharge, donc ce basculement etait devenu inutile
   — et c'est lui qui faisait gigoter la Toile a chaque rendu. */
  _shFlip=false;var a=shFmtA();var host=$('#shareScreen');var cw=(host&&host.clientWidth)?host.clientWidth:340;var pa=$('#shPreviewArea');var maxW=Math.min(400,cw-24),maxH=(pa&&pa.clientHeight?pa.clientHeight-2:360);if(maxH<180)maxH=180;var _aj=(window._shAj||1);var d=shareFit(a,maxW*_aj,maxH*_aj),W=d[0],H=d[1];var cv=$('#shCanvas');try{if(shareMode==='mosaic'){sharePlanche(cv,W,H);var g=cv.getContext('2d');/* le Noyau est DANS la planche (bloc 2x2), pas pose dessus */_shPreviewQR(g,cv.width,cv.height);}else if(shareMode==='toile'){var g=shSize(cv,W,H);shareToile(g,W,H);_shPoseNoyau(g,cv.width,cv.height);_shPreviewQR(g,cv.width,cv.height);}else if(shareMode==='noyau'){var g=shSize(cv,W,H);try{_sealAspectOverride=(typeof shFmtA==='function'?shFmtA():0);if(typeof renderSeal==='function')renderSeal();_sealAspectOverride=0;var sc=_sealCanvas;if(sc){var cw2=cv.width,ch2=cv.height;var sc2=Math.min(cw2/sc.width,ch2/sc.height);var dw=sc.width*sc2,dh=sc.height*sc2;g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,cw2,ch2);g.drawImage(sc,(cw2-dw)/2,(ch2-dh)/2,dw,dh);}}catch(e){}}else{try{window._shAllColored=true;var _or=Math.random,_sd9=42;Math.random=function(){_sd9=(_sd9*1103515245+12345)&0x7fffffff;return _sd9/0x7fffffff;};var _wld=(window.Toile&&window.Toile.curWorld?window.Toile.curWorld():'encre');if(window.Toile&&window.Toile.preview){cv.width=W*2;cv.height=H*2;var _sto=window._shThemeOverride;var _dev=document.getElementById('device');var _had=_dev&&_dev.classList.contains('light');if(_dev)_dev.classList.toggle('light',!_sealDark);window._shThemeOverride=(typeof _sealDark!=='undefined')?!_sealDark:_sto;window.Toile.preview(cv,_wld,W,H);window._shThemeOverride=(_sto===undefined?null:_sto);if(_dev)_dev.classList.toggle('light',_had);}Math.random=_or;window._shAllColored=false;}catch(e){window._shAllColored=false;}try{var _gq=cv.getContext('2d');_shPreviewQR(_gq,cv.width,cv.height);}catch(e){}}}catch(e){}wrap.style.width=W+'px';wrap.style.height=H+'px';var fl=$('#shFmtLabel');if(fl)fl.textContent=(shareFmt==='custom'?shCW+'×'+shCH:(SHARE_FMT[shareFmt]||SHARE_FMT.story).label);var nt=$('#shNote');if(nt)nt.textContent=(SHARE_FMT[shareFmt]||SHARE_FMT.story).note;var wm=$('#shWm');if(wm)wm.className='sh-wm '+WMPOS[wmPos];var hint=$('#shHint');if(hint)hint.style.display=(shareMode==='toile'&&shHintOn)?'block':'none';var _sslw=$('#shareScreen');if(_sslw)_sslw.classList.toggle('sh-lightwm',(typeof _sealDark!=='undefined')&&!_sealDark);var mel=$('#shMode');if(mel)mel.classList.remove('vert');var sc=$('#shareScreen');if(sc)sc.classList.remove('pv-vert');if(_shFlip){_shDev.classList.toggle('light',_shHadL);try{if(window.Toile&&window.Toile.redraw)window.Toile.redraw();}catch(e){}}}
function buildShareScope(){var el=$('#shScope');if(!el)return;var h='';var nus=[];promises.forEach(function(p){if(!p.draft&&p.nuee&&nus.indexOf(p.nuee)<0)nus.push(p.nuee);});if(nus.length){h+='<div class="sh-sg">Cercles</div>';nus.forEach(function(k){var on=!shareHidden['n:'+k];var cnt=promises.filter(function(p){return p.nuee===k&&!p.draft;}).length;h+='<div class="sh-si'+(on?' on':'')+'" data-k="n:'+k+'"><div class="sh-sc"></div><div><div class="sh-st">'+_esc(NUE[k]||k)+'</div><div class="sh-su">'+cnt+' Promi'+'</div></div></div>';});}h+='<div class="sh-sg">Promesses</div>';promises.filter(function(p){return !p.draft;}).forEach(function(p){var on=!shareHidden[p.id];h+='<div class="sh-si'+(on?' on':'')+'" data-k="'+p.id+'"><div class="sh-sc"></div><div><div class="sh-st">'+_esc(p.title||'Promi')+'</div><div class="sh-su">'+_esc(p.who||'')+(p.nuee?' · '+_esc(NUE[p.nuee]||p.nuee):'')+'</div></div></div>';});el.innerHTML=h;$$('#shScope .sh-si').forEach(function(it){it.onclick=function(){var k=it.dataset.k;if(shareHidden[k])delete shareHidden[k];else shareHidden[k]=true;it.classList.toggle('on',!shareHidden[k]);shareRender();};});}
function openShare(){var s=$('#shareScreen');if(!s)return;window._shP=0;quitteVues();buildShareScope();try{var bg=document.getElementById('shareToileBg');if(bg&&window.Toile&&window.Toile.preview){var dpr=Math.min(2,window.devicePixelRatio||1);var pw=390,ph=844;bg.width=pw*dpr;bg.height=ph*dpr;var th=(window.Toile.curTheme?window.Toile.curTheme():(typeof theme!=='undefined'?theme:'encre'));window.Toile.preview(bg,th,pw,ph);}}catch(e){}s.classList.add('show');s.scrollTop=0;requestAnimationFrame(shareRender);setTimeout(shareRender,60);}
function shStepBtn(d){return document.querySelector('#shCustom .sh-step button[data-d="'+d+'"]');}
function shCustomClamp(){/* Q114 · la borne monte à 4K — tout le partage est gratuit (décision Tom, 30 août 2026). Le pas de 120 et le garde-fou de ratio ne bougent pas. */shCW=Math.round(Math.max(540,Math.min(3840,shCW))/120)*120;shCH=Math.round(Math.max(540,Math.min(3840,shCH))/120)*120;if(shCW/shCH<0.42)shCW=Math.round(shCH*0.42/120)*120;if(shCW/shCH>2.5)shCW=Math.round(shCH*2.5/120)*120;var we=$('#shW'),he=$('#shH');if(we)we.textContent=shCW;if(he)he.textContent=shCH;var a=shCW/shCH;var bw=shStepBtn('w-'),bW=shStepBtn('w+'),bh=shStepBtn('h-'),bH=shStepBtn('h+');if(bw)bw.disabled=(shCW<=540||a<=0.42);if(bW)bW.disabled=(shCW>=2160||a>=2.5);if(bh)bh.disabled=(shCH<=540||a>=2.5);if(bH)bH.disabled=(shCH>=2160||a<=0.42);}
function _rrC(g,x,y,w,h,r){r=Math.min(r,h/2,w/2);g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
function shBadgeExport(g,W){var pad=Math.round(W*0.045);var fs=Math.round(W*0.042);g.textAlign='left';g.textBaseline='alphabetic';g.font='700 '+fs+'px Gilbert,system-ui,sans-serif';g.lineJoin='round';g.lineWidth=Math.max(1,fs*0.06);var _mpL=(typeof _sealDark!=='undefined'&&!_sealDark);g.strokeStyle=_mpL?'rgba(255,255,255,.65)':'rgba(0,0,0,.55)';g.strokeText('Mon Prom',pad,pad+fs);g.fillStyle=_mpL?'#201908':'#fff';g.fillText('Mon Prom',pad,pad+fs);var mw=g.measureText('Mon Prom').width;g.strokeText('i',pad+mw,pad+fs);g.fillStyle='#82AEF8';g.fillText('i',pad+mw,pad+fs);}
function shWmExport(g,W,H){var pad=Math.round(W*0.045);g.font='600 '+Math.round(W*0.028)+'px Atkinson,system-ui,sans-serif';g.lineJoin='round';g.lineWidth=Math.max(1,W*0.004);g.strokeStyle='rgba(0,0,0,.5)';g.fillStyle='#fff';var wy=H-pad;var _pR=(typeof wmPos!=='undefined'&&wmPos===1);var wx=_pR?(W-pad):pad;g.textAlign=_pR?'right':'left';g.strokeText('promi.app',wx,wy);g.fillText('promi.app',wx,wy);if(typeof _shShowQR==='undefined'||_shShowQR){try{var _q=(typeof _sealQR==='function'?_sealQR():null);if(_q){var _cl=Math.max(2,Math.round(W*0.007));var _qsz=_cl*_q.size;var _qpd=_cl*2;var _qx=_pR?pad:(W-_qsz-pad);var _qy=H-_qsz-Math.round(pad*0.6);g.fillStyle='#fff';g.fillRect(_qx-_qpd,_qy-_qpd,_qsz+_qpd*2,_qsz+_qpd*2);g.fillStyle='#1C1402';for(var _qa=0;_qa<_q.size;_qa++){for(var _qb=0;_qb<_q.size;_qb++){if(_q.mod[_qa][_qb])g.fillRect(_qx+_qb*_cl,_qy+_qa*_cl,_cl,_cl);}}}}catch(e){}}}
function shareExport(){try{var a=shFmtA();/* Q114 · le GRAND CÔTÉ passe de 1080 à 3840 : un format prédéfini sort donc en 4K (2160 × 3840 en portrait, 3840 × 2160 en paysage). */var base=3840,W,H;if(a<=1){H=base;W=Math.round(base*a);}else{W=base;H=Math.round(base/a);}var cv=document.createElement('canvas');var g;if(shareMode==='toile'){g=shSize(cv,W,H);shareToile(g,W,H);}else{var info=sharePtsInfo(W,H);paintPreview(cv,state.structure,state.mood,W,H,info.pts);if(shareVis)shareLabels(cv,W,H,info);g=cv.getContext('2d');}shBadgeExport(g,W);shWmExport(g,W,H);cv.toBlob(function(blob){if(!blob)return;try{var file=new File([blob],'mon-promi.png',{type:'image/png'});if(navigator.canShare&&navigator.canShare({files:[file]})){navigator.share({files:[file],title:'Mon Promi',text:'Ma composition Promi'});return;}}catch(e){}try{var link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='mon-promi.png';document.body.appendChild(link);link.click();link.remove();}catch(e){}},'image/png');}catch(e){}}
if($('#shareBtn'))$('#shareBtn').onclick=openShare;
if($('#shInviteBtn'))$('#shInviteBtn').onclick=function(){
  var txt='Je tiens mes promesses sur Promi. Rejoins-moi : 3 Cercles offerts pour toi et pour moi.';
  var url='https://promi.app';
  try{ if(navigator.share){ navigator.share({title:'Promi',text:txt,url:url}); return; } }catch(e){}
  try{ if(navigator.clipboard){ navigator.clipboard.writeText(txt+' '+url);
    if(typeof toast==='function') toast('Invitation copi\u00e9e'); return; } }catch(e){}
  try{ if(typeof toast==='function') toast('Invitation pr\u00eate \u00e0 partager'); }catch(e){}
};
$$('#shMode button').forEach(function(b){b.onclick=function(){shareMode=b.dataset.mode;var _np=document.getElementById('shNoyauParts');if(_np)_np.style.display=(shareMode==='noyau'?'':'none');var _so=document.querySelector('#shareScreen .sh-opts');if(_so)_so.style.display=(shareMode==='noyau'?'none':'');if(shareMode==='toile'){shareZoom=1;shPanFX=0;shPanFY=0;shHintOn=true;}$$('#shMode button').forEach(function(x){x.classList.toggle('on',x===b);});shareRender();};});
$$('#shFormats .sh-fmt').forEach(function(b){b.onclick=function(){shareFmt=b.dataset.fmt;$$('#shFormats .sh-fmt').forEach(function(x){x.classList.toggle('on',x===b);});var cu=$('#shCustom');if(cu)cu.classList.toggle('on',shareFmt==='custom');if(shareFmt==='custom')shCustomClamp();shareRender();};});
$$('#shCustom .sh-step button').forEach(function(b){b.onclick=function(){var d=b.dataset.d;if(d==='w-')shCW-=120;else if(d==='w+')shCW+=120;else if(d==='h-')shCH-=120;else if(d==='h+')shCH+=120;shareFmt='custom';shCustomClamp();shareRender();};});
if($('#shOptVis'))$('#shOptVis').onclick=function(){shareVis=!shareVis;$('#shOptVis').classList.toggle('on',shareVis);shareRender();};
/* promi.app retire : handler mort supprime */
if($('#shOptScope'))$('#shOptScope').onclick=function(){buildShareScope();var ov=$('#shScopeOv');if(ov)ov.classList.add('on');$('#shOptScope').classList.add('on');};
if($('#shScopeClose'))$('#shScopeClose').onclick=function(){var ov=$('#shScopeOv');if(ov)ov.classList.remove('on');var b=$('#shOptScope');if(b)b.classList.remove('on');};
if($('#shScopeOv'))$('#shScopeOv').onclick=function(e){if(e.target===this){this.classList.remove('on');var b=$('#shOptScope');if(b)b.classList.remove('on');}};
(function(){var wrap=document.getElementById('shWrap');if(!wrap)return;var ptrs={},base=null;
function list(){return Object.keys(ptrs).map(function(k){return ptrs[k];});}
function startG(){var a=list();if(!a.length){base=null;return;}var r=wrap.getBoundingClientRect();if(a.length>=2){base={dist:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y)||1,mx:(a[0].x+a[1].x)/2,my:(a[0].y+a[1].y)/2,zoom:shareZoom,fx:shPanFX,fy:shPanFY,rw:r.width||1,rh:r.height||1};}else{base={dist:0,mx:a[0].x,my:a[0].y,zoom:shareZoom,fx:shPanFX,fy:shPanFY,rw:r.width||1,rh:r.height||1};}}
wrap.addEventListener('pointerdown',function(e){if(shareMode!=='toile')return;try{wrap.setPointerCapture(e.pointerId);}catch(_){}ptrs[e.pointerId]={x:e.clientX,y:e.clientY};shHintOn=false;var h=document.getElementById('shHint');if(h)h.style.display='none';startG();e.preventDefault();},{passive:false});
wrap.addEventListener('pointermove',function(e){if(shareMode!=='toile'||!ptrs[e.pointerId]||!base)return;ptrs[e.pointerId]={x:e.clientX,y:e.clientY};var a=list();if(a.length>=2){var d=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);var mx=(a[0].x+a[1].x)/2,my=(a[0].y+a[1].y)/2;shareZoom=Math.max(0.4,Math.min(5,base.zoom*(d/(base.dist||1))));shPanFX=base.fx+(mx-base.mx)/base.rw;shPanFY=base.fy+(my-base.my)/base.rh;}else{shPanFX=base.fx+(a[0].x-base.mx)/base.rw;shPanFY=base.fy+(a[0].y-base.my)/base.rh;}shareRender();e.preventDefault();},{passive:false});
function up(e){if(ptrs[e.pointerId])delete ptrs[e.pointerId];if(Object.keys(ptrs).length)startG();else base=null;}
wrap.addEventListener('pointerup',up);wrap.addEventListener('pointercancel',up);wrap.addEventListener('pointerleave',up);})();
if($('#shShareBtn'))$('#shShareBtn').onclick=shareExport;

/* ===== PERSISTANCE LOCALE ===== */
function saveState(){try{if(typeof promises==='undefined')return;var d={v:1,promises:promises,NUE:NUE,NUEEMEM:NUEEMEM,NUEDALLE:(window.NUEDALLE||{}),PEOPLE:PEOPLE,FEED:FEED,feedReacted:feedReacted,shareHidden:shareHidden,state:{mood:state.mood,structure:state.structure,sort:state.sort,labels:state.labels},nid:nid,fid:_fid,notifOn:notifOn};localStorage.setItem('promi_state',JSON.stringify(d));try{if(typeof updateSaveStatus==='function')updateSaveStatus(true);}catch(_){}}catch(e){}}
function storageWorks(){try{localStorage.setItem('promi_t','1');localStorage.removeItem('promi_t');return true;}catch(e){return false;}}
function updateSaveStatus(saved){var el=$('#saveStatus');if(!el)return;if(!storageWorks()){el.textContent='indisponible ici';el.style.color='var(--rate)';return;}if(saved){var d=new Date();el.textContent='enregistré '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');}else{el.textContent='active ✓';}el.style.color='var(--tenu,#A4D294)';}
var _saveT=null;function queueSave(){try{clearTimeout(_saveT);}catch(e){}try{_saveT=setTimeout(saveState,400);}catch(e){try{saveState();}catch(_){}}}
function loadState(){try{var raw=localStorage.getItem('promi_state');if(!raw)return false;var d=JSON.parse(raw);if(!d||d.v!==1||!Array.isArray(d.promises)||(!d.promises.length&&localStorage.getItem('promi_onb')!=='1'))return false;/* v94 : un utilisateur venu de l'onboarding peut n'avoir aucune parole — sa sauvegarde vide vaut, jamais le jeu de démonstration */promises=d.promises;/* une sauvegarde ANTERIEURE au lot du monde fige n'a pas de champ `monde` : ses Promi prennent le monde courant, fige maintenant (decision Tom). La passe est idempotente et ne touche que ce qui manque. */try{if(window._figeMondesManquants)window._figeMondesManquants();}catch(e){}try{if(window._figeDallesManquantes)window._figeDallesManquantes();}catch(e){}if(d.NUE&&typeof NUE==='object'){Object.keys(NUE).forEach(function(k){delete NUE[k];});Object.assign(NUE,d.NUE);}if(d.NUEEMEM)NUEEMEM=d.NUEEMEM;if(d.NUEDALLE)window.NUEDALLE=d.NUEDALLE;if(Array.isArray(d.PEOPLE))PEOPLE=d.PEOPLE;if(Array.isArray(d.FEED))FEED=d.FEED;if(d.feedReacted)feedReacted=d.feedReacted;if(d.shareHidden)shareHidden=d.shareHidden;if(d.state){state.mood=d.state.mood||state.mood;state.structure=d.state.structure||state.structure;state.sort=d.state.sort||state.sort;state.labels=!!d.state.labels;}if(typeof d.nid==='number')nid=d.nid;if(typeof d.fid==='number')_fid=d.fid;if(typeof d.notifOn==='boolean'){notifOn=d.notifOn;var _nt=$('#notifTog');if(_nt)_nt.classList.toggle('off',!notifOn);}return true;}catch(e){return false;}}
try{var _ld=loadState();window._etatRelu=!!_ld;if(_ld){seeded=false;(function(){function _sync(){try{if(window.Toile&&window.Toile.curWorld){var _w=window.Toile.curWorld();if(_w&&typeof state!=='undefined'&&state)state.structure=_w;}else{setTimeout(_sync,120);}}catch(e){}}setTimeout(_sync,60);})();if(window.syncAll)window.syncAll();try{kick();}catch(e){}try{caption();}catch(e){}}if(!_ld){try{seedFeed();}catch(e){}}/* ⚑ v94 (Tom, iPhone : « un seul Promi à l'onboarding, et le Fil est déjà plein ») — le Fil de démonstration ne se sème QUE sur une page sans sauvegarde ; un Fil sauvegardé vide est le vrai Fil d'un nouvel utilisateur */try{if(typeof updateFeedDot==='function')updateFeedDot();if(typeof buildFeed==='function')buildFeed();}catch(e){}}catch(e){}
try{setInterval(saveState,1500);window.addEventListener('pagehide',saveState);window.addEventListener('beforeunload',saveState);document.addEventListener('visibilitychange',function(){if(document.hidden)saveState();});}catch(e){}
try{updateSaveStatus(false);}catch(e){}
try{if(notifOn)armAllReminders();}catch(e){}

