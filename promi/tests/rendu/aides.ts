/**
 * LES AIDES COMMUNES DES TESTS DE RENDU (lot 1, C-326) : l'état importé (celui de Tom s'il est là, sinon celui du banc), le prototype et la
 * vraie app ouverts sur cet état, le menu du +, et l'écart au pixel (la règle de la vraie app : ≤ 2 niveaux ; Q616 hors du Mac).
 * Le prototype est servi tel quel (port 8753), la vraie app construite (`vite preview`, port 5180), dans le même WebKit.
 */
import type { Page } from '@playwright/test';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { AMORCE_MINUTEURS, PILOTE, T_FIGE } from './banc.ts';

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
/**
 * LE MAC DE TOM (le banc de référence : WebKit de macOS, une image en 16 ms, le rendu sur lequel les dettes et les cadences ont été relevées).
 * Une machine macOS de la CI n'en est pas un : son WebKit est celui de l'iPhone (le X de PromiLate y est exact), mais elle est plus lente (une
 * image jusqu'à 0,1 s) et lisse autrement les coins de l'appareil — ses durées fines, ses bords et ses dettes relevées s'y jugent comme hors du Mac.
 */
export const MAC_DE_TOM = process.platform === 'darwin' && !process.env['CI'];

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
    // la veille coupée sur le banc (CLAUDE.md, v161 : `promi_veille_off`, comme banc_tom) — un test qui attend plus de 75 s sans toucher la verrait
    localStorage.setItem('promi_veille_off', '1');
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
  // ⚑ 3a (le X, Q623) — PROTOCOLE NOMMÉ : le X du prototype a la taille du titre de l'Index (`_tailleX`), que `ajusteTitres` pose (29,5 :
  // `_ENCART.T`) une fois l'Index MONTRÉ ; avant, il rend 35. Selon la charge, une passe l'avait posé ou non (la CI : 596 px d'écart sur une
  // fiche, une fois sur trois). Montrer puis refermer l'Index réglait le prototype, mais sous Linux chargé il y fallait plus de 40 s par test (la
  // CI coupée à 60 min). Le banc pose donc sur le titre de l'Index la taille que le prototype lui donne dès qu'il l'a montré — 29,5, mesurée sur
  // le Mac et sur l'iPhone (le titre tient largement : 110 pt pour 246 de place) —, comme `ajusteTitres` la pose (en ligne, important), puis
  // vérifie que `_tailleX` la lit. Rien d'autre n'est touché.
  const x = await page.evaluate(() => {
    const w = window as unknown as { _tailleX(): number; _ENCART?: { T: number } };
    const t = document.querySelector<HTMLElement>('#indexSheet .scr-ti');
    if (t && w._ENCART) t.style.setProperty('font-size', `${String(w._ENCART.T)}px`, 'important');
    return [w._tailleX(), w._ENCART?.T];
  });
  if (x[0] !== x[1]) throw new Error(`le prototype : la taille du X n'est pas celle des titres (${JSON.stringify(x)})`);
}

export async function vraieApp(page: Page, ls: Record<string, string>, pilote?: number): Promise<void> {
  await page.goto(`http://127.0.0.1:5180/?banc=1${pilote != null ? `&pilote=${String(pilote)}` : ''}`);
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
  const strict = MAC_DE_TOM;
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
  const ecartDe = (x: number, y: number): number => {
    const i = (y * W + x) * 4;
    return Math.max(
      Math.abs(A.data[i]! - B.data[i]!),
      Math.abs(A.data[i + 1]! - B.data[i + 1]!),
      Math.abs(A.data[i + 2]! - B.data[i + 2]!),
    );
  };
  const isole = (x: number, y: number): boolean => {
    for (let dy = -1; dy <= 1; dy++)
      for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const xx = x + dx;
        const yy = y + dy;
        if (xx >= 0 && yy >= 0 && xx < W && yy < H && ecartDe(xx, yy) > 2) return false;
      }
    return true;
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
      // EXCEPTION NOMMÉE hors du Mac de Tom : un pixel ISOLÉ (aucun de ses huit voisins n'est écarté) de 8 niveaux au plus — la couture de la
      // tuile du grain de l'appareil (140 pt), lissée autrement par la machine (relevé sur la machine macOS de la CI : six pixels, 6 niveaux)
      if (!strict && d <= 8 && isole(x, y)) {
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
  /**
   * EXCEPTION NOMMÉE : dans le prototype l'écran vit HORS de `#device` (la fiche d'une personne, sous `.frame` : le piège du §8) — un relevé
   * fait dans `#device` ne le voit pas ; les juges qui comparent nœud à nœud au prototype le passent, il est jugé au pixel par son test.
   */
  horsAppareil?: true;
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
    await page.waitForTimeout(MAC_DE_TOM ? 1500 : 4000);
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

/**
 * la fiche (lot 3a-1) : celle de la première parole de l'état ni gardée de côté, ni d'un Cercle (lot 5), et sans mot (la liste des mots
 * sous la ligne « Un mot… » est au lot 3b) — à défaut, la première ; ouverte par la façade de chaque côté
 */
export const FICHE: EcranPorte = {
  nom: 'fiche',
  ouvrir: async (p) => {
    await p.evaluate(`(() => { const P = window.__promi; const L = P.magasin.etat().paroles.filter((x) => !x.draft && !x.nuee); const q = L.find((x) => !(x.comments || []).length) || L[0];
      if (q) P.fiche().ouvrir(q.id); })()`);
    // montée et posée (elle couvre l'accueil 420 ms après l'ouverture), sur une machine lente aussi
    await p.waitForFunction(() => !!document.querySelector('#detailPoster.couvre'), null, { timeout: 10000 });
    await p.waitForTimeout(500);
  },
  prototype: async (p) => {
    await p.evaluate(
      `(() => { const L = promises.filter((x) => !x.draft && !x.nuee); const q = L.find((x) => !(x.comments || []).length) || L[0]; if (q) openDetail(q.id); })()`,
    );
    await p.waitForTimeout(3500);
  },
};

/** l'Index, le Fil (lot 4) : ouverts par la façade, de l'autre côté par leur bouton de la barre ; la fiche d'une personne, par son nom */
const LISTE = (nom: string, feuille: string, app: string, proto: string, horsAppareil = false): EcranPorte => ({
  nom,
  ...(horsAppareil ? { horsAppareil: true as const } : {}),
  ouvrir: async (p) => {
    await p.evaluate(app);
    await p.waitForFunction((f) => !!document.querySelector(`#${f}.couvre`), feuille, { timeout: 10000 });
    await p.waitForTimeout(500);
  },
  prototype: async (p) => {
    await p.evaluate(proto);
    await p.waitForTimeout(2500);
  },
});
export const ECRANS_PORTES: EcranPorte[] = [
  { nom: 'accueil', ouvrir: async () => {}, prototype: async () => {} },
  { nom: 'accueil, menu du + ouvert', ouvrir: ouvrirPlus, prototype: ouvrirPlus },
  ...PAGES_PLUS,
  FICHE,
  LISTE('Index', 'indexSheet', `${P_}.index().ouvrir()`, `document.getElementById('indexBtn').click()`),
  LISTE('Fil', 'feedView', `${P_}.fil().ouvrir()`, `document.getElementById('filBtn').click()`),
  LISTE('fiche de Rachel', 'personSheet', `${P_}.personne().ouvrir('Rachel')`, `openPerson('Rachel')`, true),
];

/**
 * LES ÉCARTS ADMIS AU PROTOTYPE, décidés par Tom (les mêmes que les tests d'identité, `ECARTS_ADMIS`) — une propriété d'un texte :
 *  C-330 (22 nov. 2026) : « garder de côté » inactif à la teinte de sa nature (le prototype le sort bleu ou lilas selon une course).
 * Chacun a son test qui rougit si la décision est défaite (page-plus-juges.spec.ts « C-330, C-331 », sonde garder-teinte).
 */
export function ecartAdmis(nom: string, texte: string, prop: string): boolean {
  return nom.startsWith('page +') && texte === 'garder de côté' && (prop === 'color' || prop === 'webkitTextFillColor');
}

/** LOT 3a — l'état des fiches (`banc-etats/etat-fiches.json` : un cas par état de fiche) et ses cas */
export const ETAT_FICHES = join(RACINE, 'banc-etats', 'etat-fiches.json');

/** la parole d'un Cercle (« Marseille », Rachel et Marion) : plantée dans le prototype par sa page + (Peaufiner › DANS UN CERCLE), relevée telle quelle */
export const PAROLE_CERCLE = {
  id: 169,
  title: 'écrire le menu',
  who: 'tout le monde',
  due: null,
  intensity: 2,
  status: 'encours',
  nuee: 'n1',
  from: 'moi',
  recur: null,
  remind: null,
  monde: { m: 'encre', p: 'signal', h: 0 },
  urg: 2,
  phraseSens: 'faire',
  cle: 'écrire le menu',
  derAct: 1795483464391,
  place: [0.516, 0.5639, 0],
  dalle: { ci: 1, lit: 0 },
  trait: 'Plein',
  // sa liste de fichiers, vide : sans elle, le prototype y pose au chargement un fichier de DÉMONSTRATION (« photo-repere.jpg », app.html
  // ≈ l. 9674 : `_pf.files = _pf.files || […]`, sur la première parole d'un Cercle) — une donnée de démonstration, pas un comportement porté
  files: [],
};
/** `cercle` : le même état, plus un Cercle (« Marseille ») et sa parole (`PAROLE_CERCLE`) — pour la fiche d'un Promi d'un Cercle (lot 3a) */
export function stockageFiches(cercle = false): Record<string, string> {
  const x = JSON.parse(readFileSync(ETAT_FICHES, 'utf8')) as Record<string, unknown>;
  const ls: Record<string, string> = {};
  for (const [k, v] of Object.entries(x)) if (typeof v === 'string' && k !== 'setItem') ls[k] = v;
  if (cercle) {
    const st = JSON.parse(ls['promi_state']!) as { promises: unknown[]; NUE: unknown; NUEEMEM: unknown; nid: number };
    st.NUE = { n1: 'Marseille' };
    st.NUEEMEM = { n1: ['Rachel', 'Marion'] };
    st.promises.push(PAROLE_CERCLE);
    st.nid = Math.max(st.nid, PAROLE_CERCLE.id + 1);
    ls['promi_state'] = JSON.stringify(st);
  }
  return ls;
}

/**
 * LOT 5 — les Cercles : « Marseille » (n1, Rachel et Marion) porte cinq paroles — un Promi en cours, un tenu, un Chiche lancé, un Chiche tenu et
 * `PAROLE_CERCLE` ; « Atelier » (n2) est vide et sans membre.
 */
export function stockageCercles(): Record<string, string> {
  const ls = stockageFiches(true);
  const st = JSON.parse(ls['promi_state']!) as {
    promises: Array<{ id: number; nuee?: string; files?: unknown[] }>;
    NUE: Record<string, string>;
    NUEEMEM: Record<string, string[]>;
  };
  // leurs listes de fichiers, vides : sans elles, le prototype pose un fichier de DÉMONSTRATION sur la première parole d'un Cercle (PAROLE_CERCLE)
  for (const q of st.promises)
    if ([144, 146, 147, 152].includes(q.id)) {
      q.nuee = 'n1';
      q.files = [];
    }
  st.NUE['n2'] = 'Atelier';
  st.NUEEMEM['n2'] = [];
  ls['promi_state'] = JSON.stringify(st);
  return ls;
}

/** les cas : l'id de la parole dans `etat-fiches.json`, et ce qu'elle est */
export const CAS_FICHES: ReadonlyArray<[number, string]> = [
  [144, 'Promi en cours, à soi'],
  [148, 'Promi en cours, à Marion'],
  [163, 'Promi en cours, à cinq personnes'],
  [149, 'Promi en cours, date passée'],
  [160, 'Promi reçu de Nico'],
  [146, 'Promi tenu, à Rachel'],
  [147, 'Chiche lancé à soi'],
  [162, 'Chiche lancé à Adrien'],
  [156, 'Chiche à Rachel et Marion, une part tracée'],
  [157, 'Chiche reçu, à relever'],
  [152, 'Chiche tenu'],
  [167, 'Chiche tenu à deux'],
  [PAROLE_CERCLE.id, 'Promi d’un Cercle'],
];

/**
 * LOT 3a — depuis que la fiche est portée, toucher une dalle de la Toile OUVRE sa fiche par-dessus (comme le prototype) : un test de la Toile
 * qui touche plusieurs dalles d'affilée la referme entre deux touchers (sinon le toucher suivant tombe sur la fiche). Elle redescend (0,4 s).
 */
export async function fermerFiche(page: Page): Promise<void> {
  const ouverte = (await page.evaluate(`(() => { const f = document.getElementById('detailPoster');
    if (!f || f.hidden || f.classList.contains('fi-bas')) return false; ${P_}.fiche().fermer(); return true; })()`)) as boolean;
  if (ouverte) await page.waitForTimeout(450);
}

/**
 * LOT 4 — l'Index et le Fil ouverts par une porte de la barre couvrent l'accueil : un test qui touche ensuite l'accueil les referme (ils
 * redescendent ou repartent à droite, 0,4 s)
 */
export async function fermerIndex(page: Page): Promise<void> {
  const ouvert = (await page.evaluate(`(() => { let o = false;
    for (const [id, f] of [['indexSheet', ${P_}.index()], ['feedView', ${P_}.fil()]]) { const e = document.getElementById(id);
      if (e && !e.hidden && !e.classList.contains('ix-bas') && f) { f.fermer(); o = true; } }
    return o; })()`)) as boolean;
  if (ouvert) await page.waitForTimeout(450);
}

// ── la fiche (lots 3a) : les zones exceptées de l'identité au pixel (fiche.spec.ts M1, M2, M3), partagées par les tests de « tenir » ──
export type Zone = [number, number, number, number];

/** les zones exceptées, en pt de l'appareil : la matière (M1) et les bandes des anneaux (M2) */
export async function zonesFiche(A: Page, P: Page): Promise<Zone[]> {
  const z: Zone[] = [];
  for (const [pg, sel] of [
    [A, '#detailPoster.fiche .fi-champ'],
    [P, '#dpTrameCv'],
  ] as const) {
    const m = (await pg.evaluate((sel) => {
      const cv = document.querySelector(sel);
      const v = cv?.getAttribute('data-matiere');
      if (!cv || !v) return null;
      const D = (document.getElementById('device') ?? document.getElementById('detailPoster'))!.getBoundingClientRect();
      const k = D.width / 390 || 1;
      const c = cv.getBoundingClientRect();
      const [x, y, w, h] = v.split(',').map(Number) as [number, number, number, number];
      return [(c.left - D.left) / k + x, (c.top - D.top) / k + y, w, h];
    }, sel)) as Zone | null;
    if (m) z.push([m[0] - 8, m[1] - 8, m[2] + 16, m[3] + 16]);
  }
  const anneaux = (await A.evaluate(() => {
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    return [...document.querySelectorAll('#detailPoster.fiche canvas.kr-c')].map((c) => {
      const r = c.getBoundingClientRect();
      return [(r.left - D.left) / k, (r.top - D.top) / k, r.width / k, r.height / k];
    });
  })) as Zone[];
  // M3 : les 46 derniers pt de la rangée des Noyaux, quand elle déborde
  const fondu = (await A.evaluate(() => {
    const a = document.getElementById('dAura')!;
    if (a.scrollWidth <= a.clientWidth + 1) return null;
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    const r = a.getBoundingClientRect();
    return [(r.right - D.left) / k - 46, (r.top - D.top) / k, 46, r.height / k];
  })) as Zone | null;
  if (fondu) z.push(fondu);
  return [...z, ...anneaux];
}

/** masque les zones (en magenta), un anneau par sa BANDE seulement (le visage dedans reste jugé) */
export function masquerFiche(png: Buffer, Z: Zone[], nAnneaux: number): Buffer {
  const im = PNG.sync.read(png);
  const k = im.width / 390;
  Z.forEach(([x, y, w, h], i) => {
    const anneau = i >= Z.length - nAnneaux;
    const cx = (x + w / 2) * k;
    const cy = (y + h / 2) * k;
    const Rx = (w / 2) * k;
    const Ri = Rx * (w === 78 ? 27 / 39 : 20 / 29);
    // un anneau : sa bande, et 3 px de part et d'autre (WebKit compose la rangée au demi-point près, différemment des deux côtés)
    const m = anneau ? 3 : 0;
    for (let j = Math.max(0, Math.floor(y * k) - m); j < Math.min(im.height, Math.ceil((y + h) * k) + m); j++)
      for (let i2 = Math.max(0, Math.floor(x * k) - m); i2 < Math.min(im.width, Math.ceil((x + w) * k) + m); i2++) {
        if (anneau) {
          const d = Math.hypot(i2 + 0.5 - cx, j + 0.5 - cy);
          if (d < Ri - 3 || d > Rx + 3) continue;
        }
        const q = (j * im.width + i2) * 4;
        im.data[q] = 255;
        im.data[q + 1] = 0;
        im.data[q + 2] = 255;
      }
  });
  return PNG.sync.write(im);
}

/** le rectangle de l'appareil (`#device`) dans la fenêtre */
export async function appareil(pg: Page): Promise<{ x: number; y: number; width: number; height: number }> {
  return pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
}

/**
 * le geste d'une fiche, au doigt (la souris : les mêmes gestionnaires que le doigt, des deux côtés) — de x0 à x1 (pt de l'appareil) en `ms`, sur
 * la ligne y (303 : le milieu de la zone de 118 pt d'une fiche au repos, base 286) ; `maintien` : le doigt reste posé avant de partir (la zone
 * ouverte, puis `maintien` ms de la page)
 */
export async function tracerFiche(pg: Page, x0: number, x1: number, ms: number, y = 303, maintien = 0): Promise<void> {
  const d = await appareil(pg);
  const k = d.width / 390;
  const X = (x: number): number => d.x + x * k;
  await pg.mouse.move(X(x0), d.y + y * k);
  await pg.mouse.down();
  if (maintien) {
    // le doigt posé tant que la zone ne s'est pas ouverte, puis `maintien` ms de la page (la fenêtre de 340 ms du prototype avale des mouvements
    // livrés groupés : sous charge, un geste qui part tout de suite peut ne rien tenir — des deux côtés)
    await pg.waitForFunction(() => !!document.querySelector('#tenirZone.ouvert'), null, { timeout: 5000 });
    await pg.evaluate((ms) => new Promise((r) => setTimeout(r, ms)), maintien);
  }
  const t0 = Date.now();
  for (;;) {
    const u = Math.min(1, (Date.now() - t0) / Math.max(1, ms));
    await pg.mouse.move(X(x0 + (x1 - x0) * u), d.y + y * k);
    if (u >= 1) break;
    await pg.waitForTimeout(16);
  }
  await pg.mouse.up();
}

/** n images de l'horloge pilotée (la vraie app : son horloge unique ; le prototype : PILOTE de banc_rendu, `__images`) */
export async function images(pg: Page, n: number): Promise<void> {
  await pg.evaluate((n) => {
    const w = window as unknown as {
      __promi?: { horloge: { images(n: number): void } };
      __images?: (n: number) => void;
    };
    if (w.__promi) w.__promi.horloge.images(n);
    else w.__images!(n);
  }, n);
}

/**
 * le geste d'une fiche, au doigt, l'horloge PILOTÉE des deux côtés : le doigt posé (la zone ouverte), 400 ms (25 images, et 400 ms réelles pour la
 * fenêtre du prototype, comptée en `Date.now`), puis de x0 à x1 en `pas` mouvements, une image par mouvement, et le doigt levé
 */
export async function tracerPilote(pg: Page, x0: number, x1: number, pas: number, y = 303): Promise<void> {
  const d = await appareil(pg);
  const k = d.width / 390;
  const X = (x: number): number => d.x + x * k;
  await pg.mouse.move(X(x0), d.y + y * k);
  await pg.mouse.down();
  await pg.waitForFunction(() => !!document.querySelector('#tenirZone.ouvert'), null, { timeout: 5000 });
  await pg.waitForTimeout(400);
  await images(pg, 25);
  for (let i = 1; i <= pas; i++) {
    await pg.mouse.move(X(x0 + ((x1 - x0) * i) / pas), d.y + y * k);
    await images(pg, 1);
  }
  await pg.mouse.up();
}

/**
 * LA MÊME FICHE OUVERTE DES DEUX CÔTÉS, L'HORLOGE PILOTÉE (lot 3a) — le prototype démarré en temps réel (9 s), puis PILOTÉ (banc_rendu) ; la
 * vraie app pilotée depuis son départ ; les animations CSS gelées (GEL : la montée de 0,4 s est réelle) ; la fiche ouverte de chaque côté, puis
 * `n` images (3 s) : toutes les passes du prototype (le X reposé, l'encre du plateau, le « + » des membres) ont eu lieu, À TOUTE CHARGE —
 * attendre en temps réel « deux images identiques » ne le prouvait pas sur la CI (le prototype capturé en pleine composition).
 */
export async function fichesPilotees(
  browser: import('@playwright/test').Browser,
  ls: Record<string, string>,
  id: number,
  o: { echelle?: number; n?: number; avantA?: () => void } = {},
): Promise<{ P: Page; A: Page; erreurs: string[] }> {
  const { P, A, erreurs } = await deuxPilotes(browser, ls, o);
  await P.evaluate((id) => (window as unknown as { openDetail(i: number): void }).openDetail(id), id);
  await A.evaluate(`${P_}.fiche().ouvrir(${String(id)})`);
  await Promise.all([images(P, o.n ?? 180), images(A, o.n ?? 180)]);
  // ⚑ 3b (le X de la fiche sous Linux) — PROTOCOLE NOMMÉ : la croix du prototype garde une place calculée plus tôt (pendant l'ouverture de la
  // fiche) tant que la place juste en diffère de moins de 0,3 pt (`lot-V157-CROIX` : il ne réécrit pas une cote à moins de 0,3 de la sienne) ;
  // sous Linux, d'un test à l'autre, 6,18 puis 6,45 pt pour la même fiche (la vraie app : 6,11, relevé de la CI du 24 nov.) — un pixel de
  // l'écran, une fois sur deux. Une fois la fiche posée, le banc lui fait reposer sa croix (sa propre passe, `_croix.passe`), puis
  // vérifie qu'elle l'a reposée. Rien d'autre n'est touché.
  await reposerCroix(P);
  return { P, A, erreurs };
}

/** les deux pages démarrées, l'horloge pilotée des deux côtés, les animations CSS gelées — rien n'est encore ouvert (lot 4 : l'Index) */
export async function deuxPilotes(
  browser: import('@playwright/test').Browser,
  ls: Record<string, string>,
  o: { echelle?: number; avantA?: () => void } = {},
): Promise<{ P: Page; A: Page; erreurs: string[] }> {
  const P = await (
    await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: o.echelle ?? 3 })
  ).newPage();
  const A = await (
    await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: o.echelle ?? 3 })
  ).newPage();
  const erreurs: string[] = [];
  A.on('pageerror', (e) => erreurs.push(String(e)));
  // une sonde posée dans la vraie app avant son départ
  if (o.avantA) await A.addInitScript(o.avantA);
  await P.addInitScript((a) => new Function(a)(), AMORCE_MINUTEURS);
  await Promise.all([prototype(P, ls), vraieApp(A, ls, T_FIGE)]);
  await P.evaluate(`(${PILOTE})()`);
  for (const pg of [P, A]) await pg.addStyleTag({ content: GEL });
  return { P, A, erreurs };
}

/** le protocole nommé du X (ci-dessus) : la croix de la fiche du prototype reposée par sa propre passe, puis vérifiée — aussi après un
 *  changement de la fiche qui la laisse à sa place d'avant (l'instant « tenir », sous Linux : relevé de la CI du 24 nov.) */
export async function reposerCroix(P: Page): Promise<void> {
  await P.evaluate(() => {
    for (const x of document.querySelectorAll<HTMLElement>('#detailPoster .closeb'))
      x.style.setProperty('top', '-50px', 'important');
    (window as unknown as { _croix: { passe(): void } })._croix.passe();
  });
  await images(P, 30);
  const reposee = await P.evaluate(() =>
    [...document.querySelectorAll<HTMLElement>('#detailPoster .closeb')].every((x) => x.style.top !== '-50px'),
  );
  if (!reposee) throw new Error('le prototype : sa croix n’a pas été reposée par sa veille');
}
