/**
 * LE BANC COMMUN AUX DEUX CÔTÉS — le hasard amorcé, le temps piloté, la Toile lue en PNG. Le pilotage du prototype est celui de
 * banc_rendu.py (le banc de rendu de référence), à l'identique ; la vraie app, elle, a son horloge en mode piloté (`?pilote=`).
 */
import type { Page } from '@playwright/test';
import { PNG } from 'pngjs';

export const GRAINE = 0x5eed2026;
export const T_FIGE = 123456.0;

/** le hasard amorcé (mulberry32), la vie au repos coupée, et — pour le prototype — ses minuteurs de démarrage notés */
export const AMORCE = `(()=>{ let a=${GRAINE}>>>0; window.__amorce=function(s){ a=s>>>0; };
  Math.random=function(){ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1);
  t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; };
  window._vivantOff=true;
})();`;

/** pour le prototype seulement : ses minuteurs réels du démarrage, repris ensuite en temps piloté (banc_rendu.py, AMORCE) */
export const AMORCE_MINUTEURS = `(()=>{ if(location.port!=='8753') return;
  const rST=window.setTimeout, rSI=window.setInterval, rCT=window.clearTimeout, rCI=window.clearInterval; window.__reels=new Map(); let n=0;
  window.setTimeout=function(cb,ms,...a){ const k=++n; const id=rST(function(){ window.__reels.delete(id); if(typeof cb==='function') cb(...a); },ms); window.__reels.set(id,{k,cb,ms:+ms||0,a,rep:0}); return id; };
  window.setInterval=function(cb,ms,...a){ const k=++n; const id=rSI(cb,ms,...a); window.__reels.set(id,{k,cb,ms:+ms||0,a,rep:Math.max(16,+ms||0)}); return id; };
  window.clearTimeout=function(i){ window.__reels.delete(i); return rCT(i); }; window.clearInterval=function(i){ window.__reels.delete(i); return rCI(i); };
  window.__reelsCoupe=function(){ const L=[...window.__reels.entries()].sort((x,y)=>x[1].k-y[1].k); for(const [id] of L){ rCT(id); rCI(id); } window.__reels.clear(); return L.map(x=>x[1]); };
})();`;

/** banc_rendu.py, PILOTE — à l'identique */
export const PILOTE = `()=>{ if(window.__vt!=null) return; window.__vt=${T_FIGE};
  performance.now=()=>window.__vt; window.__q=[]; let id=1;
  window.requestAnimationFrame=cb=>{ window.__q.push([id,cb]); return id++; };
  window.cancelAnimationFrame=i=>{ window.__q=window.__q.filter(x=>x[0]!==i); };
  const T=[]; let tid=1e6;
  for(const e of (window.__reelsCoupe?window.__reelsCoupe():[])){ if(typeof e.cb!=='function') continue; T.push({i:tid++,at:window.__vt+(e.rep||Math.max(0,e.ms)),cb:e.cb,a:e.a||[],rep:e.rep||0}); }
  window.setTimeout=(cb,ms,...a)=>{ if(typeof cb!=='function') return 0; const i=tid++; T.push({i,at:window.__vt+Math.max(0,+ms||0),cb,a}); return i; };
  window.setInterval=(cb,ms,...a)=>{ if(typeof cb!=='function') return 0; const i=tid++; T.push({i,at:window.__vt+Math.max(16,+ms||0),cb,a,rep:Math.max(16,+ms||0)}); return i; };
  window.clearTimeout=window.clearInterval=i=>{ for(let k=T.length-1;k>=0;k--) if(T[k].i===i) T.splice(k,1); };
  window.requestIdleCallback=(cb,o)=>window.setTimeout(()=>cb({didTimeout:false,timeRemaining:()=>50}),1);
  window.cancelIdleCallback=i=>window.clearTimeout(i);
  const minuteurs=()=>{ for(let garde=0;garde<500;garde++){ let m=-1; for(let k=0;k<T.length;k++) if(T[k].at<=window.__vt&&(m<0||T[k].at<T[m].at||(T[k].at===T[m].at&&T[k].i<T[m].i))) m=k;
      if(m<0) return; const t=T[m]; if(t.rep){ t.at+=t.rep; } else T.splice(m,1); try{ t.cb(...t.a); }catch(e){} } };
  window.__images=n=>{ for(let i=0;i<n;i++){ window.__vt+=1000/60; minuteurs(); const q=window.__q; window.__q=[]; for(const [,cb] of q){ try{ cb(window.__vt); }catch(e){} } } }; }`;

/** la Toile, lue de deux façons : le rendu entier sans titres (comme banc_rendu), et le canevas qu'on voit */
export const LIRE = `(clair)=>{ const png=cv=>cv.toDataURL('image/png');
  const lab=window._shLabels; window._shLabels=false; const cv=document.createElement('canvas'); let entier=null;
  let premier=null; try{ premier = Toile.renderTo(cv,1,clair) ? png(cv) : null; const cv2=document.createElement('canvas'); entier = Toile.renderTo(cv2,1,clair) ? png(cv2) : null; } finally { window._shLabels=lab; }
  const vu=document.getElementById('toileCv');
  return { entier, premierDiffere: premier!==entier, vu: png(vu), monde: Toile.getTheme(), vue: Toile_lecture().vue, graines: JSON.stringify(Toile_graines()), etat: JSON.stringify([Toile.getPalette(), Toile.getHue(), Toile_lecture().cible]), paroles: JSON.stringify(promises.map(p=>[p.id,p.place,p.dalle,p.status,p.cle])) }; }`;

export function decoder(dataUrl: string): PNG {
  return PNG.sync.read(Buffer.from(dataUrl.split(',', 2)[1]!, 'base64'));
}

export interface Ecart {
  pixels: number;
  total: number;
  max: number;
  taille?: string;
  diff?: PNG;
}

export function comparer(a: string, b: string): Ecart {
  const A = decoder(a);
  const B = decoder(b);
  if (A.width !== B.width || A.height !== B.height)
    return { pixels: -1, total: 0, max: 255, taille: `${A.width}×${A.height} ≠ ${B.width}×${B.height}` };
  let n = 0;
  let mx = 0;
  const D = new PNG({ width: A.width, height: A.height });
  for (let i = 0; i < A.data.length; i += 4) {
    let d = 0;
    for (let c = 0; c < 4; c++) d = Math.max(d, Math.abs(A.data[i + c]! - B.data[i + c]!));
    if (d) n++;
    if (d > mx) mx = d;
    D.data[i] = d ? 255 : A.data[i]! >> 2;
    D.data[i + 1] = d ? 0 : A.data[i + 1]! >> 2;
    D.data[i + 2] = d ? 0 : A.data[i + 2]! >> 2;
    D.data[i + 3] = 255;
  }
  return { pixels: n, total: A.width * A.height, max: mx, diff: D };
}

export async function images(page: Page, cote: 'proto' | 'app', n: number): Promise<void> {
  for (let k = 0; k < n; k += 40) {
    const m = Math.min(40, n - k);
    if (cote === 'proto')
      await page.evaluate((x) => (window as unknown as { __images(n: number): void }).__images(x), m);
    else
      await page.evaluate(
        (x) => (window as unknown as { __promi: { horloge: { images(n: number): void } } }).__promi.horloge.images(x),
        m,
      );
  }
}
