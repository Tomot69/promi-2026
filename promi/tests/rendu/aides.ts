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
  await page.mouse.click(r[0]!, r[1]!);
  await page.waitForTimeout(500);
  // le menu s'ouvre en flaques (C-329) : son passage fini
  await page.waitForFunction(() => !document.querySelector('[data-flaques-mode]'), undefined, { timeout: 20000 });
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
      { timeout: 30000 },
    );
    await page.waitForTimeout(process.platform === 'darwin' ? 1500 : 4000);
  } else
    await page.waitForFunction(
      () => {
        const c = document.getElementById('createSheet');
        return !!c && !c.hidden && !c.classList.contains('pp-compose') && !!c.querySelector('.ph-txt .ph-m');
      },
      undefined,
      { timeout: 20000 },
    );
  await page.waitForTimeout(400);
}

/** la page + ouverte par une pilule (lot 2a) couvre l'accueil : son X la referme, on attend qu'elle soit partie (rien, si elle est fermée) */
export async function refermerPagePlus(page: Page): Promise<void> {
  const ouverte = await page.evaluate(() => {
    const c = document.getElementById('createSheet');
    return !!c && !c.hidden;
  });
  if (!ouverte) return;
  await page.waitForFunction(
    () => !document.getElementById('createSheet')?.classList.contains('pp-compose'),
    undefined,
    {
      timeout: 20000,
    },
  );
  const x = await page.evaluate(() => {
    const b = document.querySelector('#createSheet .closeb')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  });
  await page.mouse.click(x[0]!, x[1]!);
  await page.waitForFunction(() => !!document.getElementById('createSheet')?.hidden, undefined, { timeout: 20000 });
}

/**
 * ⚠ LOT 2a (PARTIEL) — la page + n'est PAS encore dans ECRANS_PORTES : ajoutée, le socle l'a jugée en partie (joignable et écrans : deux
 * défauts trouvés et corrigés — l'accueil restait visible sous elle, le rail ne déclarait pas qu'il glisse) ; les autres juges du socle n'ont
 * pas tourné sur elle avant l'arrêt du lot. `PAGES_PLUS` les y ajoutera (`...PAGES_PLUS`) au 2b, une fois le socle vert sur elles.
 */
export const PAGES_PLUS: EcranPorte[] = (['promi', 'chiche', 'nuee'] as const).map((n): EcranPorte => ({
  nom: `page +, ${n}`,
  ouvrir: (p) => ouvrirPagePlus(p, n),
  prototype: (p) => ouvrirPagePlus(p, n, true),
}));

export const ECRANS_PORTES: EcranPorte[] = [
  { nom: 'accueil', ouvrir: async () => {}, prototype: async () => {} },
  { nom: 'accueil, menu du + ouvert', ouvrir: ouvrirPlus, prototype: ouvrirPlus },
];
