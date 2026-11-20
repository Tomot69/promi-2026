/**
 * L0 §3 — BANC_RENDU PORTÉ. Le banc de rendu de référence du portage (banc_rendu.py, CLAUDE.md : « c'est lui qui jugera le portage »)
 * rejoué dans la VRAIE APP, et comparé AU PIXEL à ses images figées (banc-rendu/ref/, 20 mondes × la Toile en clair et en sombre +
 * 4 dalles × 3 tailles) — la référence n'est pas recalculée : ce sont les images que le prototype a rendues et que le banc juge.
 *
 * Le même état (le jeu de démonstration que rend le banc : outils/banc_rendu_etat.py → etat-banc-rendu.json), le même hasard amorcé,
 * le même temps piloté (l'horloge de la vraie app en mode piloté, l'algorithme de PILOTE), le même protocole, ligne pour ligne :
 * le relevé des mondes neufs, puis pour chaque monde POSE (places oubliées, l'autre famille, la graine, `_chaOublie`), 6 × 40 images,
 * le rendu répété jusqu'à ce qu'il ne bouge plus, et la pose répétée jusqu'à deux rendus identiques (STABLE).
 * Fenêtre du banc : 430 × 932, densité 2 (le canevas du moteur est à la même densité à toutes les échelles : A3 est jugé par toile.spec).
 *
 * RAMAGE N'EST PAS JUGÉ EN L0 (A6) : ① sa référence est périmée (C-187 : le prototype ne la retrouve plus lui-même) ; ② comparé au rendu
 * du jour du prototype (`banc_rendu.py --monde=ramage`, déterministe sur deux passes), la vraie app en diffère sur des plumes entières
 * (52 199 px de la Toile). Cause PROBABLE, non prouvée : dans le prototype, la jauge du Studio prépare au repos de l'accueil la silhouette
 * de Ramage (`silhouettesAuRepos`, Q581) et ce premier rendu laisse un état dans le moteur (v160c : « son premier rendu laisse un état
 * dans le moteur ») ; la vraie app n'a pas encore de Studio. Ramage entre dans la comparaison au lot 7 (le Studio).
 */
import { test, expect, type Page } from '@playwright/test';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { AMORCE, AMORCE_MINUTEURS, GRAINE, PILOTE, T_FIGE, comparer } from './banc.ts';

const RACINE = join(import.meta.dirname, '..', '..', '..');
const REF = join(RACINE, 'banc-rendu', 'ref');
const RESULTATS = join(import.meta.dirname, 'resultats');
const ETAT = JSON.parse(readFileSync(join(import.meta.dirname, 'etat-banc-rendu.json'), 'utf8')) as {
  ls: Record<string, string>;
};
const KS = [0.5, 1, 2];
const PAROLES: Array<[string, string]> = [
  ['promi', 'nager le mardi'],
  ['chiche', 'courir dimanche'],
  ['tenu', 'planter un arbre'],
  ['cercle', 'arroser les tomates'],
];
const REF_ECARTEES = new Set(['ramage']);

interface Manifeste {
  mondes: Record<string, { stable: boolean; images: Record<string, { fichier?: string; fnv?: string; err?: string }> }>;
}

// banc_rendu.py, POSE et RENDU — à l'identique (la porte du moteur : window.Toile, comme le banc ; le test pilote le moteur directement)
const POSE = `(a)=>{ const [monde,graine,neufs]=a; const autre = neufs.indexOf(monde)>=0 ? 'encre' : 'esquille';
  const oublie=()=>{ try{ promises.forEach(p=>{ delete p.place; }); }catch(e){} try{ window.NUEPLACE={}; localStorage.removeItem('promi_nueplace'); }catch(e){} };
  oublie(); Toile.setTheme(autre); oublie(); window.__amorce(graine); try{ window._chaOublie&&window._chaOublie(); }catch(e){} Toile.setTheme(monde); return Toile.getTheme(); }`;
const RENDU = `(a)=>{ const [monde,T,KS,PAR]=a; const out={};
  const img=(cv)=>{ const g=cv.getContext('2d'); const d=g.getImageData(0,0,cv.width,cv.height).data;
    let h=0x811c9dc5; for(let i=0;i<d.length;i++){ h^=d[i]; h=Math.imul(h,16777619)>>>0; }
    return {w:cv.width,h:cv.height,fnv:h.toString(16),png:cv.toDataURL('image/png')}; };
  const lab=window._shLabels; window._shLabels=false;
  try{ for(const cl of [false,true]){ const cv=document.createElement('canvas');
    out['toile-'+(cl?'clair':'sombre')] = Toile.renderTo(cv,1,cl) ? img(cv) : null; } } finally { window._shLabels=lab; }
  const M={m:monde,p:Toile.getPalette(),h:Toile.getHue?Toile.getHue():0};
  for(const [nat,titre] of PAR){ const p=promises.find(x=>x.title===titre);
    for(const k of KS){ const nom='dalle-'+nat+'-k'+k; if(!p){ out[nom]={err:'parole introuvable'}; continue; }
      const cv=document.createElement('canvas'); let ok=false; try{ ok=Toile.dalleTrame(cv,p.id,k,M); }catch(e){ out[nom]={err:String(e)}; continue; }
      out[nom] = (ok&&cv.width) ? img(cv) : {err:'rien de rendu'}; } }
  return out; }`;

type Image = { w: number; h: number; fnv: string; png: string } | { err: string } | null;

type Cote = 'proto' | 'app';

async function images(page: Page, cote: Cote, n: number): Promise<void> {
  if (cote === 'proto')
    await page.evaluate((x) => {
      (window as unknown as { __images(n: number): void }).__images(x);
    }, n);
  else
    await page.evaluate((x) => {
      (window as unknown as { __promi: { horloge: { images(n: number): void } } }).__promi.horloge.images(x);
    }, n);
}

function stockage(x: { ls?: Record<string, string> } & Record<string, unknown>): Record<string, string> {
  const ls = (x.ls ?? x) as Record<string, string>;
  const r: Record<string, string> = {};
  for (const [k, v] of Object.entries(ls)) if (k !== 'setItem' && typeof v === 'string') r[k] = v;
  return r;
}

/** la vraie app, démarrée sur l'état `ls`, horloge pilotée */
async function ouvrirApp(page: Page, ls: Record<string, string>): Promise<void> {
  await page.addInitScript((a) => new Function(a)(), AMORCE);
  await page.goto(`http://127.0.0.1:5180/?banc=1&pilote=${T_FIGE}`);
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await page.evaluate(async (ls) => {
    const p = (window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } })
      .__promi;
    p.magasin.importer({ ls });
    await p.demarrer();
  }, ls);
}

/** le prototype, démarré comme banc_rendu.py démarre le sien : 8 s en temps réel, `closeAll`, `setPremium(true)`, PILOTE */
async function ouvrirPrototype(page: Page, ls: Record<string, string>): Promise<void> {
  await page.addInitScript(
    ([ls, a, m]) => {
      localStorage.clear();
      for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v);
      new Function(a)();
      new Function(m)();
    },
    [ls, AMORCE, AMORCE_MINUTEURS] as const,
  );
  await page.goto('http://127.0.0.1:8753/app.html');
  await page.waitForTimeout(8000);
  await page.evaluate('()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} }');
  await page.evaluate(`(${PILOTE})()`);
}

/** le protocole de banc_rendu.py, ligne pour ligne : le relevé des mondes neufs, puis chaque monde posé jusqu'à deux rendus identiques */
async function protocole(
  page: Page,
  cote: Cote,
  mondes: string[],
): Promise<Record<string, { stable: boolean; images: Record<string, Image> }>> {
  const neufs = (await page.evaluate(
    `(()=>{ const r=[]; for(const m of ${JSON.stringify(mondes)}){ Toile.setTheme(m); if(Toile.semisNeuf()) r.push(m); } return r; })()`,
  )) as string[];
  const out: Record<string, { stable: boolean; images: Record<string, Image> }> = {};
  for (const m of mondes) {
    let avant: string | null = null;
    let r: Record<string, Image> = {};
    let stable = false;
    for (let essai = 0; essai < 3; essai++) {
      await page.evaluate(`(${POSE})(${JSON.stringify([m, GRAINE, neufs])})`);
      for (let i = 0; i < 6; i++) {
        await images(page, cote, 40);
        await page.waitForTimeout(120);
      }
      let prec: string | null = null;
      let emp = '';
      for (let i = 0; i < 40; i++) {
        r = (await page.evaluate(`(${RENDU})(${JSON.stringify([m, T_FIGE, KS, PAROLES])})`)) as Record<string, Image>;
        emp = JSON.stringify(
          Object.fromEntries(Object.entries(r).map(([k, v]) => [k, v && 'fnv' in v ? v.fnv : null])),
        );
        if (emp === prec) break;
        prec = emp;
        await images(page, cote, 20);
        await page.waitForTimeout(250);
      }
      if (emp === avant) {
        stable = true;
        break;
      }
      avant = emp;
    }
    out[m] = { stable, images: r };
  }
  return out;
}

function ecrireDiff(nom: string, e: ReturnType<typeof comparer>): void {
  if (!e.diff) return;
  mkdirSync(RESULTATS, { recursive: true });
  writeFileSync(join(RESULTATS, `${nom}.png`), PNG.sync.write(e.diff));
}

test('banc_rendu porté : la vraie app rend les images figées du banc, au pixel', async ({ browser }) => {
  test.skip(!existsSync(join(REF, 'manifeste.json')), 'banc-rendu/ref absent');
  // les images figées ont été rendues par le WebKit du Mac (celui de l'iPhone) ; le WebKit de Linux rend autrement les bords et les
  // polices : en intégration continue, c'est le test suivant (le prototype vivant, sur la même machine) qui juge
  test.skip(process.platform !== 'darwin', 'images figées sur macOS');
  const ref = JSON.parse(readFileSync(join(REF, 'manifeste.json'), 'utf8')) as Manifeste;
  const ctx = await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 2 });
  const pg = await ctx.newPage();
  const erreurs: string[] = [];
  pg.on('pageerror', (e) => erreurs.push(String(e)));
  await ouvrirApp(pg, stockage(ETAT));
  const voulus = process.env['MONDES']?.split(',');
  const res = await protocole(pg, 'app', Object.keys(ref.mondes));
  const ecarts: string[] = [];
  let pareils = 0;
  for (const [m, R] of Object.entries(res)) {
    if (voulus && !voulus.includes(m)) continue;
    if (!R.stable) ecarts.push(`${m} : INSTABLE (deux poses ne rendent pas la même chose)`);
    if (REF_ECARTEES.has(m)) continue;
    for (const [nom, v] of Object.entries(ref.mondes[m]!.images)) {
      const a = R.images[nom];
      if (!v.fichier || !a || !('png' in a)) {
        if ((a && 'err' in a ? a.err : undefined) !== v.err) ecarts.push(`${m} ${nom} : absente`);
        continue;
      }
      if (a.fnv === v.fnv) {
        pareils++;
        continue;
      }
      const e = comparer('data:image/png;base64,' + readFileSync(join(REF, v.fichier)).toString('base64'), a.png);
      ecarts.push(`${m} ${nom} : ${e.pixels < 0 ? e.taille : e.pixels + ' px, écart max ' + e.max}`);
      ecrireDiff(`banc-${m}-${nom}`, e);
    }
  }
  console.log(`banc_rendu porté : ${pareils} image(s) identique(s) au pixel, ${ecarts.length} écart(s)`);
  await ctx.close();
  expect(erreurs, 'erreurs JavaScript de la vraie app').toEqual([]);
  expect(ecarts, ecarts.join('\n')).toEqual([]);
});

/**
 * LE MÊME PROTOCOLE, DES DEUX CÔTÉS, SUR LA MÊME MACHINE : le prototype vivant (démarré comme banc_rendu) contre la vraie app, sur l'état
 * du banc. C'est le juge de l'intégration continue (Linux), et un second témoin sur le Mac. Ramage : voir plus haut.
 */
test('banc_rendu porté : la vraie app contre le prototype vivant, même protocole, même machine, au pixel', async ({
  browser,
}) => {
  const ls = stockage(ETAT);
  const nouveau = (): ReturnType<typeof browser.newContext> =>
    browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 2 });
  const cp = await nouveau();
  const ca = await nouveau();
  const P = await cp.newPage();
  const A = await ca.newPage();
  const erreurs: string[] = [];
  A.on('pageerror', (e) => erreurs.push(String(e)));
  await Promise.all([ouvrirPrototype(P, ls), ouvrirApp(A, ls)]);
  const mondes = Object.keys((JSON.parse(readFileSync(join(REF, 'manifeste.json'), 'utf8')) as Manifeste).mondes);
  const [rp, ra] = await Promise.all([protocole(P, 'proto', mondes), protocole(A, 'app', mondes)]);
  const ecarts: string[] = [];
  let pareils = 0;
  for (const m of mondes) {
    if (REF_ECARTEES.has(m)) continue;
    if (!rp[m]!.stable) ecarts.push(`${m} : le prototype est INSTABLE`);
    if (!ra[m]!.stable) ecarts.push(`${m} : la vraie app est INSTABLE`);
    for (const [nom, a] of Object.entries(rp[m]!.images)) {
      const b = ra[m]!.images[nom];
      if (!a || !b || !('png' in a) || !('png' in b)) {
        if (JSON.stringify(a) !== JSON.stringify(b)) ecarts.push(`${m} ${nom} : absente`);
        continue;
      }
      if (a.fnv === b.fnv) {
        pareils++;
        continue;
      }
      const e = comparer(a.png, b.png);
      ecarts.push(`${m} ${nom} : ${e.pixels < 0 ? e.taille : e.pixels + ' px, écart max ' + e.max}`);
      ecrireDiff(`vivant-${m}-${nom}`, e);
    }
  }
  console.log(
    `la vraie app contre le prototype vivant : ${pareils} image(s) identique(s) au pixel, ${ecarts.length} écart(s)`,
  );
  await cp.close();
  await ca.close();
  expect(erreurs, 'erreurs JavaScript de la vraie app').toEqual([]);
  expect(ecarts, ecarts.join('\n')).toEqual([]);
});
