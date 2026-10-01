/* ════════════════════════════════════════════════════════════════════════════
   LA FORME D'ABORD. La silhouette se COMPOSE — elle ne se subit pas.
   Trois familles, toutes à symétrie assumée :
     · LA RÉVOLUTION   un profil dessiné, tourné autour d'un axe. La silhouette EST
                       la courbe. Rien ne peut être bancal.
     · LE LOBE         une harmonique PURE d'ordre n : n bosses régulières.
     · LA DALLE        le contour d'une vraie dalle du moteur, donné en volume.
   Aucune somme d'ondes tirée au hasard : c'était ça, l'ovale irrégulier.
   ════════════════════════════════════════════════════════════════════════════ */

/* ── LE PROFIL DE RÉVOLUTION : r en fonction de la latitude seule ─────────── */
function profGalet(y){ var t=Math.abs(y); return Math.pow(1-Math.pow(t,2.6),0.42); }
function profLentille(y){ var t=Math.abs(y); return Math.pow(1-t*t,0.30); }
function profGoutte(y){ var s=(y+1)/2; return Math.pow(1-s,0.62)*Math.pow(s,0.30)*2.05; }
function profTore(y){ var t=Math.abs(y)*1.35; if(t>1)return 0; return 0.60+0.40*Math.sqrt(1-t*t); }
/* ⚑ L'ONDE DE PROMI, DONNÉE EN VOLUME.
   C'est la courbe du geste — deux bosses, jamais un segment — tournée autour de son
   axe. La silhouette de l'Aura devient littéralement le trait qu'on trace pour tenir
   sa parole. Ça n'appartient qu'à ce produit. */
function profOnde(y){
  var t=(y+1)/2;                       /* 0 → 1 le long de l'axe */
  var env=Math.sin(Math.PI*t);         /* elle se ferme aux deux bouts, comme le trait */
  return 0.30+0.70*env*(0.72+0.28*Math.sin(t*1.5*6.2832));
}

/* ── LE CONTOUR D'UNE VRAIE DALLE, relevé au pixel ────────────────────────── */
function contourDalle(pid, N){
  var S=128, cv=document.createElement('canvas'); cv.width=S; cv.height=S;
  try{ window.Toile && Toile.dalleTrame(cv, pid, 1); }catch(e){}
  var d=cv.getContext('2d').getImageData(0,0,S,S).data, R=new Float32Array(N);
  for(var i=0;i<N;i++){
    var a=i/N*6.2832, cx=S/2, cy=S/2, best=0;
    for(var r=S/2-1;r>2;r-=0.5){
      var x=(cx+Math.cos(a)*r)|0, y=(cy+Math.sin(a)*r)|0;
      if(x<0||y<0||x>=S||y>=S) continue;
      if(d[(y*S+x)*4+3]>90){ best=r/(S/2); break; }
    }
    R[i]=best||0.55;
  }
  /* on lisse à peine : le contour d'une dalle est franc, on ne l'arrondit pas */
  var L=new Float32Array(N);
  for(i=0;i<N;i++) L[i]=(R[(i-1+N)%N]+R[i]*2+R[(i+1)%N])/4;
  return L;
}

/* ── LA FORME : elle rend le point déformé ET sa normale ──────────────────── */
function forme(kind, par){
  var prof=null, C=null;
  if(kind==='galet') prof=profGalet;
  if(kind==='lentille') prof=profLentille;
  if(kind==='goutte') prof=profGoutte;
  if(kind==='tore') prof=profTore;
  if(kind==='onde') prof=profOnde;
  if(kind==='dalle') C=par.contour;
  var lob=par.lobes||0, lamp=par.lampl||0, ep=par.ep||1;
  return function(x,y,z){
    var rr=1, X,Y,Z;
    if(prof){ rr=prof(y); }
    if(lob){ rr*= 1 + lamp*Math.cos(lob*Math.atan2(z,x)) * (1-y*y); }
    if(C){
      /* ⚠ LA DALLE VIT DANS LE PLAN DE L'ÉCRAN, pas à plat. Posée dans le plan XZ,
         elle était HORIZONTALE : de face on n'en voyait que la tranche — une lentille
         écrasée, jamais une dalle. Son contour est ici la section Z = 0, et
         l'épaisseur part vers le regard. De face, la silhouette EST la dalle. */
      var a=Math.atan2(y,x); if(a<0)a+=6.2832;
      var rad=C[((a/6.2832*C.length)|0)%C.length];
      return [x*rad, y*rad, z*ep];
    }
    var hh=Math.sqrt(Math.max(0,1-y*y))||1e-6;
    return [x/hh*rr*hh, y*ep, z/hh*rr*hh];
  };
}
