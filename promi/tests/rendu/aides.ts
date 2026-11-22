/**
 * LES AIDES COMMUNES DES TESTS DE RENDU (lot 1, C-326) : l'état importé (celui de Tom s'il est là, sinon celui du banc), le prototype et la
 * vraie app ouverts sur cet état, le menu du +, et l'écart au pixel (la règle de la vraie app : ≤ 2 niveaux ; Q616 hors du Mac).
 * Le prototype est servi tel quel (port 8753), la vraie app construite (`vite preview`, port 5180), dans le même WebKit.
 */
import type { Page } from '@playwright/test';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';

/**
 * LA SONDE (C-326 : « chaque test rougit sur une sonde ») : un test pose le défaut qu'il doit prendre quand `PROMI_SONDE` porte son nom —
 * `if (sonde('deplace-selection')) …`. Chaque sonde est inscrite dans `tests/rendu/sondes/<fichier>.json` ; `npm run sondes` rejoue chaque
 * test avec sa sonde et exige qu'il ROUGISSE (l'intégration continue aussi, à chaque commit). Une sonde ne se pose jamais sans la variable.
 */
export function sonde(nom: string): boolean {
  return process.env['PROMI_SONDE'] === nom;
}

/** la vraie app, en JavaScript dans la page : `window.__promi` (src/main.ts) */
export const P_ = 'window.__promi';

export const RACINE = join(import.meta.dirname, '..', '..', '..');
export const ETAT = process.env['PROMI_ETAT']
  ? join(RACINE, process.env['PROMI_ETAT'])
  : (() => {
      // l'état de Tom le plus récent s'il est là (hors dépôt), sinon celui du banc (l'intégration continue)
      const d = join(RACINE, 'etats');
      const tom = existsSync(d)
        ? readdirSync(d)
            .filter((f) => /^tom-\d{8}-\d{6}\.json$/.test(f))
            .sort()
            .pop()
        : undefined;
      return tom ? join(d, tom) : join(RACINE, 'banc-etats', 'etat-25.json');
    })();
export const RESULTATS = join(import.meta.dirname, 'resultats', 'accueil');

export function stockage(): Record<string, string> {
  const x = JSON.parse(readFileSync(ETAT, 'utf8')) as { ls?: Record<string, string> } & Record<string, unknown>;
  const ls: Record<string, string> = {};
  for (const [k, v] of Object.entries(x.ls ?? x)) if (k !== 'setItem' && typeof v === 'string') ls[k] = v;
  return pagePlusDeterministe(ls);
}

/**
 * La page + (lot 2a) des deux côtés sur la MÊME phrase : les exemples des pastilles vides sont tirés au hasard (`lot-EXEMPLES-V20`) ; on
 * pose leurs compteurs pour que le tirage soit écrit d'avance — Promi à soi et Cercle : leur première phrase (« me coucher le jour même »,
 * « Week-end à Marseille ») ; Chiche : le prototype tire DEUX fois à la première ouverture (défaut relevé au lot 2a), on lui donne donc un
 * sac où les deux tirages tombent sur le même rang (4, « choisir une ville au hasard »). Et les personnes connues : le prototype ajoute ses
 * personnes de démonstration (« Maman », « Mimi ») quand l'état n'en porte pas ; on les écrit dans l'état, la vraie app les lit.
 */
export function pagePlusDeterministe(ls: Record<string, string>): Record<string, string> {
  const o: Record<string, string> = {};
  for (const [k, v] of Object.entries(ls)) if (!k.startsWith('promi_ex')) o[k] = v;
  o['promi_ex_chiche'] = '1';
  o['promi_ex_sac_chiche'] = '[4,4]';
  o['promi_ex_der_chiche'] = '4';
  if (o['promi_state']) {
    const st = JSON.parse(o['promi_state']) as Record<string, unknown>;
    st['PEOPLE'] = ['Maman', 'Mimi'];
    o['promi_state'] = JSON.stringify(st);
  }
  return o;
}

export const GEL =
  '*,*::before,*::after{animation:none!important;transition:none!important}' +
  '#device#device#device #createBtn::before,#device#device#device #createBtn::after{animation:none!important;transform:none!important}' +
  '#device#device#device .acc-mm i{animation:none!important;opacity:1!important}' +
  '#stage{visibility:hidden!important}';

export async function prototype(page: Page, ls: Record<string, string>): Promise<void> {
  await page.addInitScript((ls) => {
    try {
      Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true });
    } catch {
      /* rien */
    }
    localStorage.clear();
    for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v);
  }, ls);
  await page.goto('http://127.0.0.1:8753/app.html');
  await page.waitForTimeout(9000);
  await page.evaluate(() => {
    const o = document.getElementById('promiOnb');
    if (o) {
      o.classList.add('gone');
      o.style.display = 'none';
    }
  });
}

export async function vraieApp(page: Page, ls: Record<string, string>): Promise<void> {
  await page.goto('http://127.0.0.1:5180/?banc=1');
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await page.evaluate(async (ls) => {
    const p = (window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } })
      .__promi;
    p.magasin.importer({ ls });
    await p.demarrer();
  }, ls);
  await page.waitForTimeout(1500);
}

export async function ouvrirPlus(page: Page): Promise<void> {
  const r = await page.evaluate(() => {
    const b = document.getElementById('createBtn')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  });
  const t0 = Date.now();
  await page.mouse.click(r[0]!, r[1]!);
  await page.waitForTimeout(500);
  // le menu s'ouvre en flaques (C-329) : son passage fini
  await page.waitForFunction(() => !document.querySelector('[data-flaques-mode]'), undefined, { timeout: 20000 });
  // ⚑ 2b (le juge « flash », instable sur la CI) : le menu reste à l'écran au moins 1 s avant qu'on touche une pilule, comme une personne qui
  // le lit — sous Linux le test touchait « Un Chiche » 0,6 s après l'ouverture du menu, que la page + recouvrait aussitôt : le menu (demandé,
  // puis quitté par le toucher) restait 791 ms à l'écran, sous les 800 ms du juge, qui mesurait alors la vitesse du test, pas un éclair de l'app
  await page.waitForTimeout(Math.max(0, 1000 - (Date.now() - t0)));
}

/**
 * Les pixels qui s'écartent de plus de 2 niveaux, hors des quatre coins du téléphone (30 pt). Sur le Mac (le WebKit de l'iPhone) : aucun.
 * Ailleurs (l'intégration continue, WebKit sous Linux), la règle de Q616 (Tom) : le lissage d'un BORD peut différer — un pixel situé sur un
 * bord de la référence (contraste de plus de 24 niveaux dans ses 5 × 5 pixels) et écarté de 12 niveaux au plus n'est pas compté ; hors
 * des bords, la règle reste aucun pixel. (Mesuré sur la CI le 20 nov. : 379 à 661 pixels, tous sur un bord, 8 niveaux au plus.)
 */
export function ecart(a: Buffer, b: Buffer): { n: number; boite: number[] | null; bords: number } {
  const A = PNG.sync.read(a);
  const B = PNG.sync.read(b);
  if (A.width !== B.width || A.height !== B.height) return { n: -1, boite: null, bords: 0 };
  const W = A.width;
  const H = A.height;
  const k = W / 390;
  const strict = process.platform === 'darwin';
  const lum = (x: number, y: number): number => {
    const i = (y * W + x) * 4;
    return 0.299 * A.data[i]! + 0.587 * A.data[i + 1]! + 0.114 * A.data[i + 2]!;
  };
  const surBord = (x: number, y: number): boolean => {
    let lo = 255;
    let hi = 0;
    for (let dy = -2; dy <= 2; dy++)
      for (let dx = -2; dx <= 2; dx++) {
        const xx = Math.min(W - 1, Math.max(0, x + dx));
        const yy = Math.min(H - 1, Math.max(0, y + dy));
        const l = lum(xx, yy);
        if (l < lo) lo = l;
        if (l > hi) hi = l;
      }
    return hi - lo > 24;
  };
  let n = 0;
  let bords = 0;
  let x0 = 1e9,
    y0 = 1e9,
    x1 = -1,
    y1 = -1;
  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++) {
      const coin = (x < 30 * k || x >= 360 * k) && (y < 30 * k || y >= 814 * k);
      if (coin) continue;
      const i = (y * W + x) * 4;
      const d = Math.max(
        Math.abs(A.data[i]! - B.data[i]!),
        Math.abs(A.data[i + 1]! - B.data[i + 1]!),
        Math.abs(A.data[i + 2]! - B.data[i + 2]!),
      );
      if (d <= 2) continue;
      if (!strict && d <= 12 && surBord(x, y)) {
        bords++;
        continue;
      }
      n++;
      x0 = Math.min(x0, x);
      y0 = Math.min(y0, y);
      x1 = Math.max(x1, x);
      y1 = Math.max(y1, y);
    }
  return { n, boite: n ? [x0 / k, y0 / k, x1 / k, y1 / k].map((v) => Math.round(v)) : null, bords };
}

/**
 * LES ÉCRANS PORTÉS (C-326) — ceux que les juges du socle transversal parcourent, dans la vraie app, ouverts par le vrai chemin depuis
 * l'accueil. CHAQUE LOT AJOUTE LES SIENS ICI : un juge du socle les couvre alors sans qu'on le touche. `prototype` ouvre le même écran
 * dans le prototype (pour une comparaison), une fois `prototype(page, ls)` chargé.
 */
export type EcranPorte = {
  nom: string;
  /** depuis l'accueil de la vraie app, ouverte par `vraieApp` */
  ouvrir(page: Page): Promise<void>;
  /** depuis l'accueil du prototype, ouvert par `prototype` */
  prototype(page: Page): Promise<void>;
};
/** le + puis la pilule d'une nature : la page + (lot 2a), composée (dans la vraie app : la page porte sa phrase ; le prototype : 3,5 s) */
export async function ouvrirPagePlus(page: Page, nat: 'promi' | 'chiche' | 'nuee', proto = false): Promise<void> {
  await ouvrirPlus(page);
  const r = await page.evaluate((k) => {
    const b = document.querySelector(`#accChoix .acc-pil[data-k="${k}"]`)!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  }, nat);
  await page.mouse.click(r[0]!, r[1]!);
  if (proto) {
    // le prototype : la page + est posée quand elle porte SA nature, montrée (`show`), sortie de sa composition cachée (`acc-passe`,
    // v103) — un temps fixe ne suffisait pas hors du Mac (une image dure 0,7 s : la page + n'était pas encore là) ; puis ses
    // minuteurs de composition (arme +60/+340, champ +240, encre +120/+420) ont fini
    await page.waitForFunction(
      (k) => {
        const s = document.getElementById('createSheet');
        return (
          !!s &&
          s.classList.contains('show') &&
          s.classList.contains('pp-' + k) &&
          !s.classList.contains('pp-choix') &&
          !s.classList.contains('acc-passe')
        );
      },
      nat,
      { timeout: 60000 },
    );
    await page.waitForTimeout(process.platform === 'darwin' ? 1500 : 4000);
  } else
    await page.waitForFunction(
      () => {
        const c = document.getElementById('createSheet');
        return (
          !!c &&
          !c.hidden &&
          !c.classList.contains('pp-compose') &&
          !c.classList.contains('pp-entre') &&
          !!c.querySelector('.ph-txt .ph-m')
        );
      },
      undefined,
      { timeout: 20000 },
    );
  await page.waitForTimeout(400);
}

/** la page + ouverte par une pilule (lot 2a) couvre l'accueil : son X la referme, on attend qu'elle soit partie (rien, si elle est fermée) */
/**
 * le centre d'un bouton, une fois que c'est LUI qui est sous le doigt (`elementFromPoint`). Hors du Mac (WebKit sous Linux), au point d'un bouton
 * posé à sa place, le navigateur ne trouve parfois AUCUN élément pendant un moment (ni le bouton, ni la page : `null`) — un toucher y est perdu.
 * On attend (15 s au plus) que le bouton soit atteignable ; s'il ne l'est jamais, on dit ce qu'il y a sous le doigt et l'état de la page.
 */
export async function xSousLeDoigt(page: Page, sel: string): Promise<[number, number]> {
  const lire = (): Promise<{ ok: boolean; x: number; y: number; diag: string }> =>
    page.evaluate((sel) => {
      const b = document.querySelector(sel)!;
      const r = b.getBoundingClientRect();
      const x = r.left + r.width / 2;
      const y = r.top + r.height / 2;
      const e = document.elementFromPoint(x, y);
      const nom = (n: Element | null): string =>
        n
          ? n.tagName.toLowerCase() +
            (n.id ? '#' + n.id : '') +
            (n.className && typeof n.className === 'string' ? '.' + n.className.trim().replace(/\s+/g, '.') : '')
          : '∅';
      const st = (n: Element | null): string => {
        if (!n) return '';
        const c = getComputedStyle(n);
        return `${nom(n)}[vis ${c.visibility} · pe ${c.pointerEvents} · op ${c.opacity} · disp ${c.display}]`;
      };
      const ancetres: string[] = [];
      for (let n: Element | null = b; n; n = n.parentElement) ancetres.push(st(n));
      const ailleurs = [
        [195, 422],
        [20, 20],
      ].map(([a, c]) => `(${String(a)},${String(c)}) ${nom(document.elementFromPoint(a!, c!))}`);
      return {
        ok: !!e && (e === b || b.contains(e)),
        x,
        y,
        diag: `sous le doigt (${String(Math.round(x))},${String(Math.round(y))}) : ${nom(e)} ; elementsFromPoint ${String(document.elementsFromPoint(x, y).length)} ; ailleurs ${ailleurs.join(' · ')} ; page ${document.visibilityState}, focus ${String(document.hasFocus())}, fenêtre ${String(innerWidth)} × ${String(innerHeight)}, visualViewport ${String(visualViewport?.width)} × ${String(visualViewport?.height)} + ${String(visualViewport?.offsetLeft)},${String(visualViewport?.offsetTop)} ; ${ancetres.join(' < ')}`,
      };
    }, sel);
  const t0 = Date.now();
  let l = await lire();
  while (!l.ok && Date.now() - t0 < 15000) {
    await page.waitForTimeout(250);
    l = await lire();
  }
  if (!l.ok) throw new Error(`${sel} n'est jamais sous le doigt (15 s) — ${l.diag}`);
  return [l.x, l.y];
}

export async function refermerPagePlus(page: Page): Promise<void> {
  const ouverte = await page.evaluate(() => {
    const c = document.getElementById('createSheet');
    return !!c && !c.hidden;
  });
  if (!ouverte) return;
  // la page + posée : ni montée (C-331), ni composition, ni passage en flaques, ni mouvement (hors du Mac une image dure 0,7 s : un toucher
  // pendant un passage tombait sur ce qu'il recouvre encore) ; puis le X, UNE fois — un X qui ne prend pas au premier toucher est un défaut
  await page.waitForFunction(
    `(() => { const c = document.getElementById('createSheet'); return !c?.classList.contains('pp-compose') && !c?.classList.contains('pp-entre')
      && !document.querySelector('#createSheet [data-flaques-mode]') && !${P_}.pagePlus?.()?.etat().mouvement; })()`,
    undefined,
    { timeout: 20000 },
  );
  const x = await xSousLeDoigt(page, '#createSheet .closeb');
  await page.mouse.click(x[0]!, x[1]!);
  const ok = await page
    .waitForFunction(() => !!document.getElementById('createSheet')?.hidden, undefined, { timeout: 20000 })
    .then(() => true)
    .catch(() => false);
  if (ok) return;
  // ce qui était sous le doigt et l'état de la page, pour nommer la cause
  const diag = await page.evaluate(
    ([x, y]) => {
      const c = document.getElementById('createSheet')!;
      const e = document.elementFromPoint(x!, y!);
      const nom = (n: Element | null): string =>
        n
          ? n.tagName.toLowerCase() +
            (n.id ? '#' + n.id : '') +
            (n.className && typeof n.className === 'string' ? '.' + n.className.trim().replace(/\s+/g, '.') : '')
          : '∅';
      const xb = document.querySelector('#createSheet .closeb')!.getBoundingClientRect();
      const d = (s: string): string => {
        const n = document.querySelector(s);
        return n ? `${s} ${String(Math.round(n.scrollTop))}/${String(Math.round(n.scrollLeft))}` : '';
      };
      return `sous le doigt : ${nom(e)} (parent ${nom(e?.parentElement ?? null)}) ; le X à ${String(Math.round(xb.left))},${String(Math.round(xb.top))} (fenêtre ${String(innerWidth)} × ${String(innerHeight)}, défilée ${String(scrollX)},${String(scrollY)}) ; défilements ${[d('html'), d('body'), d('#device'), d('#createSheet')].join(' · ')} ; actif ${nom(document.activeElement)} ; #createSheet : ${c.className}, hidden ${String(c.hidden)}`;
    },
    [x[0], x[1]],
  );
  throw new Error(`refermerPagePlus : le X touché une fois, posé, la page + ne s’est pas refermée — ${diag}`);
}

/** les trois pages + (lot 2a) : des écrans portés, jugés par tout le socle (ECRANS_PORTES) */
export const PAGES_PLUS: EcranPorte[] = (['promi', 'chiche', 'nuee'] as const).map((n): EcranPorte => ({
  nom: `page +, ${n}`,
  ouvrir: (p) => ouvrirPagePlus(p, n),
  prototype: (p) => ouvrirPagePlus(p, n, true),
}));

export const ECRANS_PORTES: EcranPorte[] = [
  { nom: 'accueil', ouvrir: async () => {}, prototype: async () => {} },
  { nom: 'accueil, menu du + ouvert', ouvrir: ouvrirPlus, prototype: ouvrirPlus },
  ...PAGES_PLUS,
];

/**
 * LES ÉCARTS ADMIS AU PROTOTYPE, décidés par Tom (les mêmes que les tests d'identité, `ECARTS_ADMIS`) — une propriété d'un texte :
 *  C-330 (22 nov. 2026) : « garder de côté » inactif à la teinte de sa nature (le prototype le sort bleu ou lilas selon une course).
 * Chacun a son test qui rougit si la décision est défaite (page-plus-juges.spec.ts « C-330, C-331 », sonde garder-teinte).
 */
export function ecartAdmis(nom: string, texte: string, prop: string): boolean {
  return nom.startsWith('page +') && texte === 'garder de côté' && (prop === 'color' || prop === 'webkitTextFillColor');
}
