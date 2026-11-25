/**
 * LE SOCLE TRANSVERSAL, PARTIE 2 (C-326) — les juges du prototype portés en tests de la VRAIE APP, rejoués à chaque lot.
 *
 * Chaque test porte sa décision EN DUR, avec sa source, et rougit sur une sonde (`tests/rendu/sondes/socle-2.json`, `npm run sondes`).
 * Les juges qui parcourent des écrans parcourent `ECRANS_PORTES` (aides.ts) : chaque lot y ajoute les siens et ces tests les couvrent
 * sans qu'on les touche. Ce qu'un juge du prototype exige d'un écran pas encore porté est écrit « s'étend au lot N » à son test.
 *
 *   redteam_tokens        → « les jetons font autorité… »                (statique)
 *   redteam_polices       → « aucune graisse hors des cinq faces… »
 *   redteam_lettres_bleu  → « les lettres qui clignotent… »
 *   redteam_kaki          → « jamais de kaki : la source… » (statique) et « jamais de kaki : la Toile des vingt mondes… »
 *   releve-design         → « le contrat visuel… »
 *   redteam_croix         → « × FERMER est un seul X… »
 *   redteam_vide          → « un écran n'est jamais vide… »
 *   redteam_enchaine      → « enchaîner deux écrans… »
 *   redteam_app           → « la red team de l'app… » (trois vues)
 *   redteam_fonctions     → « l'inventaire des fonctions… »
 *   redteam_champs        → « le contrôle qui remplit… »
 *   redteam_pastilles     → « le contrôle qui touche… »
 *   redteam_secs2         → « aucun changement sec : le symbole recadrer… »
 */
import { test, expect, type Browser, type Page } from '@playwright/test';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { PNG } from 'pngjs';
import {
  ECRANS_PORTES,
  P_,
  RACINE,
  prototype,
  refermerPagePlus,
  sonde,
  stockage,
  vraieApp,
  type EcranPorte,
  ecartAdmis,
  MAC_DE_TOM,
  fermerIndex,
} from './aides.ts';
import { AMORCE, GRAINE, T_FIGE } from './banc.ts';

const SRC = join(RACINE, 'promi', 'src');
type Theme = 'sombre' | 'clair';
const THEMES: Theme[] = ['sombre', 'clair'];
const REF = { width: 390, height: 844 };

// ───────────────────────────────────────────────────────────── aides de ce fichier ──

function fichiers(d: string, ext: RegExp): string[] {
  const out: string[] = [];
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) out.push(...fichiers(p, ext));
    else if (ext.test(f)) out.push(p);
  }
  return out;
}
const lire = (p: string): string => readFileSync(p, 'utf8');
const sansCommentaires = (s: string): string =>
  s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:'"\\])\/\/[^\n]*/g, '$1');
const hex = (s: string): string => s.toUpperCase();

/** OKLCH depuis sRGB (la formule de oklch.py, celle de redteam_kaki) */
function oklch(r: number, g: number, b: number): [number, number, number] {
  const lin = (c: number): number => {
    const x = c / 255;
    return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4;
  };
  const R = lin(r);
  const G = lin(g);
  const B = lin(b);
  const l = Math.cbrt(0.4122214708 * R + 0.5363325363 * G + 0.0514459929 * B);
  const m = Math.cbrt(0.2119034982 * R + 0.6806995451 * G + 0.1073969566 * B);
  const s = Math.cbrt(0.0883024619 * R + 0.2817188376 * G + 0.6299787005 * B);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
  const a = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
  const bb = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  return [L, Math.hypot(a, bb), ((Math.atan2(bb, a) * 180) / Math.PI + 360) % 360];
}
/** L* CIELAB (redteam_tokens, l'escalier des bruns) */
function lstar(h: string): number {
  const v = [1, 3, 5].map((k) => parseInt(h.slice(k, k + 2), 16) / 255);
  const f = (c: number): number => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const Y = 0.2126 * f(v[0]!) + 0.7152 * f(v[1]!) + 0.0722 * f(v[2]!);
  return 116 * (Y > 0.008856 ? Math.cbrt(Y) : 7.787 * Y + 16 / 116) - 16;
}

/** une page neuve de la vraie app, à cette taille, ce thème, cet écran ouvert par le vrai chemin depuis l'accueil */
async function ouvrirEcran(
  browser: Browser,
  ecran: EcranPorte,
  o: { theme?: Theme; vue?: { width: number; height: number }; dsf?: number; ls?: Record<string, string> } = {},
): Promise<{ page: Page; erreurs: string[]; fermer(): Promise<void> }> {
  const ctx = await browser.newContext({ viewport: o.vue ?? REF, deviceScaleFactor: o.dsf ?? 2 });
  const page = await ctx.newPage();
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  page.on('console', (m) => {
    if (m.type() === 'error') erreurs.push('console : ' + m.text());
  });
  await vraieApp(page, { ...(o.ls ?? stockage()), promi_theme: (o.theme ?? 'sombre') === 'clair' ? 'light' : 'dark' });
  await ecran.ouvrir(page);
  await page.waitForTimeout(400);
  return { page, erreurs, fermer: () => ctx.close() };
}

/**
 * LE RETOUR À L'ACCUEIL, sans recharger (le `closeAll` du prototype, par le doigt) : la croix « Fermer » visible du dessus si un écran en
 * porte une (C-173 : chaque écran se ferme par son X, `aria-label="Fermer"`) ; sinon, le menu du + ouvert, un toucher sur le plateau hors
 * de ses boutons (v165 : un toucher ailleurs referme le menu). Rend faux si aucun chemin n'est trouvé.
 */
async function retourAccueil(page: Page): Promise<boolean> {
  for (let essai = 0; essai < 4; essai++) {
    // rien ne bouge encore : la page + qui monte ou descend (C-331), un passage en flaques (C-329) — hors du Mac une image dure 0,7 s, et
    // un toucher pendant le mouvement tombe à côté de la croix
    await page.waitForFunction(
      () => !document.querySelector('#createSheet.pp-entre, #createSheet.pp-part, [data-flaques-mode]'),
      undefined,
      { timeout: 20000 },
    );
    const p = (await page.evaluate(() => {
      const vu = (e: Element): boolean => {
        const r = e.getBoundingClientRect();
        if (r.width < 4 || r.height < 4) return false;
        const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return !!h && (h === e || e.contains(h));
      };
      const x = [...document.querySelectorAll('[aria-label="Fermer"]')].find(vu);
      if (x) {
        const r = x.getBoundingClientRect();
        return [r.left + r.width / 2, r.top + r.height / 2];
      }
      if (document.getElementById('accChoix')?.classList.contains('ouvert')) {
        const pl = document.getElementById('accPlat')!.getBoundingClientRect();
        for (let f = 0.5; f < 0.66; f += 0.03) {
          const X = pl.left + pl.width * f;
          const Y = pl.top + pl.height / 2;
          if (document.elementFromPoint(X, Y)?.id === 'accPlat') return [X, Y];
        }
      }
      return null;
    })) as [number, number] | null;
    if (!p) return true;
    await page.mouse.click(p[0], p[1]);
    await page.waitForTimeout(400);
  }
  return false;
}

/** l'empreinte d'un écran (redteam_vide, redteam_enchaine) : ce qui est VISIBLE et à l'écran, rien de ce qui est translaté hors champ */
type Empreinte = { mots: string[]; noeuds: string[]; cls: Record<string, string>; canevas: Record<string, number> };
const EMPREINTE = `(() => { const W = innerWidth, H = innerHeight;
  const vis = (e) => { for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = getComputedStyle(x);
      if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; }
    const r = e.getBoundingClientRect(); return r.width >= 4 && r.height >= 4 && r.bottom > 0 && r.top < H && r.right > 0 && r.left < W; };
  const cle = (e) => { const p = e.closest('[id]'); return (p ? '#' + p.id : '') + ' ' + e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\\s+/).sort().join('.') : ''); };
  // les exemples des pastilles vides de la page + (et la liaison qui les précède, « de » / « d’ ») sont TIRÉS SANS REMISE à chaque
  // ouverture (redteam_suggestions, C-312) : leur texte change par décision, ils se lisent comme « ⟨exemple⟩ »
  const ex = (x) => x.classList && x.classList.contains('ph-vide'), li = (x) => x.tagName === 'EM' && !!x.className && x.nextElementSibling && ex(x.nextElementSibling);
  const texte = (e) => { if (e.closest('.ph-vide')) return '⟨exemple⟩'; if (li(e)) return '⟨liaison⟩'; if (!e.querySelector('.ph-vide')) return e.textContent || '';
    const c = e.cloneNode(true); for (const x of [...c.querySelectorAll('*')]) { if (li(x)) x.textContent = '⟨liaison⟩'; } for (const x of c.querySelectorAll('.ph-vide')) x.textContent = '⟨exemple⟩';
    return c.textContent || ''; };
  const mots = new Set(), noeuds = new Set(), cls = {}, canevas = {};
  const dv = document.getElementById('device'); if (dv) cls['#device'] = [...dv.classList].sort().join(' ');
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('.passage-flaques')) continue;
    if (!vis(e)) continue;
    if (e.id) { noeuds.add(e.id); cls['#' + e.id] = [...e.classList].filter((c) => !/^gs\\d+$/.test(c)).sort().join(' '); }
    if (e.tagName === 'CANVAS' && !e.classList.contains('passage-flaques')) { let n = 0;
      try { const d = e.getContext('2d').getImageData(0, 0, e.width, e.height).data; for (let i = 3; i < d.length; i += 4 * 53) if (d[i] > 200) n++; } catch (_) { n = -1; }
      canevas[cle(e)] = n; }
    if ([...e.children].some((x) => !['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) continue;
    const t = texte(e).trim().replace(/\\s+/g, ' '); if (t) mots.add(t.slice(0, 40)); }
  return { mots: [...mots].sort(), noeuds: [...noeuds].sort(), cls, canevas }; })()`;

/** lit l'image d'une zone (en pt de la page) : les pixels RGBA, et le facteur pt → pixel */
async function zone(page: Page, x: number, y: number, w: number, h: number): Promise<PNG> {
  return PNG.sync.read(await page.screenshot({ clip: { x, y, width: w, height: h } }));
}

// ─────────────────────────────────────────────────────────────── redteam_tokens ──

/**
 * redteam_tokens (16 sept. 2026, Tom : « Centralise tout […] pour qu'aucune vue n'appelle une police ou un hexadécimal en dur ») — porté
 * sur la vraie app. Les valeurs décidées sont écrites EN DUR (CLAUDE.md §7), avec la décision qui les fixe ; le test lit `jetons.css`
 * (engendré depuis PROMI-TOKENS.json : PROMI-TOKENS.json n'est pas dans l'extraction des tests de rendu de la CI). Ce qui est DÉJÀ jugé
 * ailleurs n'est pas refait : « le bloc et le JSON disent la même chose » et « l'extension Swift porte les mêmes rôles » =
 * `npm run jetons:verifie` (outils/jetons_engendrer.py --verifie, à chaque commit, job « verifier » de la CI).
 */
const DECIDE: Record<string, [string, string]> = {
  // [rôle, valeur] en clair — redteam_tokens, DECIDE (planche des correspondances, v7, v8, 22 sept., v135)
  promi: ['--p-promi', '#82AEF8'], // « champ — une promesse »
  chiche: ['--p-chiche', '#FFB8D2'], // « champ — un défi lancé »
  nuee: ['--p-nuee', '#C9A8F5'], // 17 sept. : le lilas est le CHAMP d'un Cercle
  tenu: ['--p-tenu', '#00341A'], // v7 « vert profond » ; 22 sept. : une seule valeur par état
  amande: ['--p-amande', '#8FE08F'], // v8 : la célébration seule
  'en-cours': ['--p-en-cours', '#291547'], // v7 « violet Promi, retenu »
  'en-cours-clair': ['--p-en-cours-clair', '#291547'], // 22 sept. : plus de clair dérivé
  'tenu-clair': ['--p-tenu-clair', '#00341A'], // 22 sept.
  exception: ['--p-exception', '#2B1020'], // v8, la terre
  crete: ['--p-crete', '#0B4A2A'], // v8, la ligne d'horizon
  'brun-encre': ['--p-brun-encre', '#43291C'], // v7, trait et texte sur champ lilas
  'fond-clair': ['--p-fond', '#F7F0DE'], // « le clair devient #F7F0DE »
};
const FOND_SOMBRE = '#050302'; // v135 (Tom, 6 oct. 2026) : « Fond sombre : seiche #050302 »
const ENCRE_CLAIR = '#201908'; // v7 : « L'encre du mode clair est arrêtée : #201908 »
const BRUNS: Array<[string, string]> = [
  ['encre du clair', '#201908'],
  ['brun encre', '#43291C'],
]; // v7 : l'escalier, ≥ 8 de L* par marche
const ENCRES_SOMBRE: Record<string, string> = {
  // redteam_tokens, ENCRES (17 sept., v7, 22 sept.) — la valeur du mode sombre ; la bascule en clair s'étend au lot 3a (la fiche)
  '--c-bleu45-txt': '#82AEF8',
  '--c-framboise54-txt': '#FFB8D2',
  '--c-mauve77-txt': '#C9A8F5',
  '--c-menthe67-txt': '#00341A',
  '--c-mauve63-txt': '#291547',
};
const RETIRES: Array<[string, string]> = [
  ['FFD447', 'le jaune, retiré en v6'],
  ['8FA0FF', 'le périwinkle'],
];
/** CLAUDE.md §6 (22 sept. 2026) : « trois polices, cinq faces, rien d'autre » */
const FACES = [
  'gilbert 700 normal',
  'atkinson 400 normal',
  'atkinson 500 normal',
  'atkinson 700 normal',
  'promilate 400 normal',
];
const FAMILLES = ['gilbert', 'atkinson', 'promilate'];

function facesEmbarquees(css: string): string[] {
  const out: string[] = [];
  for (const m of css.matchAll(/@font-face\s*\{([^}]*)\}/g)) {
    const d = m[1]!;
    const fam = /font-family:\s*['"]?([A-Za-z][A-Za-z ]*?)['"]?\s*;/.exec(d)?.[1];
    if (!fam) continue;
    const w = /font-weight:\s*(\d+)/.exec(d)?.[1] ?? '400';
    const st = /font-style:\s*(italic|normal)/.exec(d)?.[1] ?? 'normal';
    out.push(`${fam.trim().toLowerCase()} ${w} ${st}`);
  }
  return out.sort();
}

test('les jetons font autorité : les valeurs décidées, aucune couleur ni police en dur dans la vraie app (redteam_tokens)', () => {
  let jetons = lire(join(SRC, 'design', 'jetons.css'));
  let polices = lire(join(SRC, 'design', 'polices.css'));
  const sources = new Map<string, string>();
  for (const f of fichiers(SRC, /\.(css|ts)$/)) {
    const r = relative(SRC, f);
    if (r.includes('repris/')) continue; // les pièces reprises octet pour octet (moteur, tracé, flaques) : §9, on n'y touche pas
    sources.set(r, lire(f));
  }
  if (sonde('tokens-valeur')) jetons = jetons.replace('--p-promi:#82AEF8', '--p-promi:#8AB0F0');
  if (sonde('tokens-couleur-dur'))
    sources.set('ecrans/accueil/accueil.css', sources.get('ecrans/accueil/accueil.css') + '\n.acc-x{color:#123456}');
  if (sonde('tokens-police-dur'))
    sources.set(
      'ecrans/accueil/accueil.css',
      sources.get('ecrans/accueil/accueil.css') + '\n.acc-y{font-family:Georgia,serif}',
    );
  if (sonde('tokens-face')) polices = polices.replace(/@font-face\{font-family:Atkinson;font-weight:500[^}]*\}/, '');

  const racine = /:root\s*\{([\s\S]*?)\}/.exec(jetons)?.[1] ?? '';
  const sombre = /\[data-theme="sombre"\]\s*\{([\s\S]*?)\}/.exec(jetons)?.[1] ?? '';
  const val = (bloc: string, v: string): string =>
    hex(new RegExp(`(?:^|[;\\s])${v.replace(/[-]/g, '\\-')}:(#[0-9A-Fa-f]{6})`).exec(bloc)?.[1] ?? '(absent)');
  // 1 · les valeurs décidées
  for (const [nom, [v, attendu]] of Object.entries(DECIDE))
    expect.soft(val(racine, v), `la valeur décidée « ${nom} » (${v}) vaut ${attendu}`).toBe(attendu);
  expect.soft(val(sombre, '--p-fond'), `le fond du mode sombre vaut ${FOND_SOMBRE}`).toBe(FOND_SOMBRE);
  for (const [v, attendu] of Object.entries(ENCRES_SOMBRE))
    expect.soft(val(racine, v), `l'encre ${v} vaut ${attendu} (mode sombre)`).toBe(attendu);
  // 2 · v7 : l'échange abandonné côté fond, gardé côté encre
  expect.soft(val(racine, '--p-encre'), "l'encre du mode clair est arrêtée à #201908").toBe(ENCRE_CLAIR);
  expect.soft(val(sombre, '--p-fond'), "le fond du mode sombre n'est plus l'encre du mode clair").not.toBe(ENCRE_CLAIR);
  expect
    .soft(val(sombre, '--p-encre'), "l'encre du mode sombre est le fond du mode clair")
    .toBe(val(racine, '--p-fond'));
  // 2 bis · l'escalier des bruns, et le jeu les porte
  for (let k = 0; k + 1 < BRUNS.length; k++)
    expect
      .soft(
        lstar(BRUNS[k + 1]![1]) - lstar(BRUNS[k]![1]),
        `${BRUNS[k + 1]![0]} au-dessus de ${BRUNS[k]![0]} (≥ 8 de L*)`,
      )
      .toBeGreaterThanOrEqual(8);
  const fixes = new Set([...racine.matchAll(/--c-[a-z0-9-]+:(#[0-9A-Fa-f]{6})/g)].map((m) => hex(m[1]!)));
  for (const [n, h] of BRUNS) expect.soft(fixes.has(h), `le jeu porte le brun « ${n} » ${h}`).toBe(true);
  // 2 quater · les valeurs retirées ne reviennent nulle part, sous aucune de leurs trois formes (hexadécimal, %23, triplet) — §8
  const tout = [...sources.values()].join('\n') + jetons + lire(join(SRC, 'moteur', 'repris', 'promi-moteur.js'));
  for (const [h, quoi] of RETIRES) {
    const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
    const n =
      (tout.match(new RegExp(h, 'gi')) ?? []).length +
      (tout.match(new RegExp(`(?<![\\d.])${String(r)}\\s*,\\s*${String(g)}\\s*,\\s*${String(b)}(?![\\d.])`, 'g')) ?? [])
        .length;
    expect.soft(n, `#${h} ne revient nulle part — ${quoi}`).toBe(0);
  }
  // 3 · aucune couleur en dur : dans toute feuille de style (hors jetons.css, engendré) et dans toute VUE (src/ecrans, src/textes)
  const dur: string[] = [];
  for (const [r, s] of sources) {
    if (/design\/jetons\.(css|ts)$/.test(r)) continue;
    if (!r.endsWith('.css') && !/^(ecrans|textes)\//.test(r)) continue;
    const corps = sansCommentaires(s.replace(/url\("data:[^"]*"\)/g, 'url()'));
    for (const m of corps.matchAll(/#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+[^)]*\)/g))
      dur.push(`${r} : ${m[0]}`);
  }
  expect.soft(dur, 'aucune couleur en dur (tout passe par les jetons)').toEqual([]);
  // 4 · aucune police appelée en dur (liste blanche : les jetons --f-*, inherit, et les trois familles) — CSS et TypeScript
  const PERMIS = ['var(--f-', 'inherit', 'initial', ...FAMILLES];
  const pol: string[] = [];
  for (const [r, s] of sources) {
    if (/design\/(jetons\.(css|ts)|polices\.css)$/.test(r)) continue;
    const T = sansCommentaires(s.replace(/@font-face\s*\{[^}]*\}/g, ''));
    for (const m of T.matchAll(/font-?family['"]?\s*[:=]\s*['"]?([^;}'"),]+)/gi)) {
      const tete = m[1]!.trim().toLowerCase();
      if (!PERMIS.some((p) => tete.startsWith(p))) pol.push(`${r} : ${m[0].slice(0, 44)}`);
    }
  }
  expect.soft(pol, 'aucune police appelée en dur').toEqual([]);
  // 6 · les faces annoncées sont embarquées : les cinq, et elles seules
  expect.soft(facesEmbarquees(polices), 'les cinq faces embarquées (CLAUDE.md §6)').toEqual([...FACES].sort());
});

// ────────────────────────────────────────────────────────────── redteam_polices ──

/**
 * redteam_polices (19 août 2026 ; v59, 22 sept. : trois polices) — « en navigateur, une graisse absente se substitue en silence ; en Swift,
 * elle casse ». Sur chaque écran porté, clair et sombre, chaque élément qui porte du texte à l'écran demande un couple police | graisse |
 * style ; il doit exister en @font-face. Les faces sont LUES dans polices.css (le juge : « jamais recopiées ici ») ; la famille doit être
 * l'une des trois (CLAUDE.md §6 : rien d'autre).
 */
test('aucune graisse hors des cinq faces embarquées, sur chaque écran porté, clair et sombre (redteam_polices)', async ({
  browser,
}) => {
  const ok = new Set(facesEmbarquees(lire(join(SRC, 'design', 'polices.css'))));
  const fautes: string[] = [];
  let n = 0;
  for (const ecran of ECRANS_PORTES)
    for (const theme of THEMES) {
      const E = await ouvrirEcran(browser, ecran, { theme });
      if (sonde('polices-graisse'))
        await E.page.addStyleTag({ content: '#device .acc-entree .l{font-weight:600!important}' });
      await E.page.evaluate(() => document.fonts.ready);
      const rel = (await E.page.evaluate(`(() => { const out = []; const W = innerWidth, H = innerHeight;
        for (const e of document.querySelectorAll('body *')) { const c = getComputedStyle(e);
          if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) continue;
          let t = ''; e.childNodes.forEach((x) => { if (x.nodeType === 3) t += x.nodeValue; }); if (!t.trim()) continue;
          const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2 || r.right < 2 || r.left > W - 2 || r.bottom < 2 || r.top > H - 2) continue;
          const fam = (c.fontFamily || '').split(',')[0].replace(/["']/g, '').trim().toLowerCase();
          out.push([fam + ' ' + (parseInt(c.fontWeight, 10) || 400) + ' ' + (c.fontStyle.indexOf('italic') >= 0 ? 'italic' : 'normal'),
            (e.id ? '#' + e.id : e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]) + ' « ' + t.trim().slice(0, 18) + ' »']); }
        return out; })()`)) as Array<[string, string]>;
      for (const [cle, ou] of rel) {
        n++;
        if (!ok.has(cle) || !FAMILLES.includes(cle.split(' ')[0]!))
          fautes.push(`${ecran.nom}, ${theme} : ${cle} — ${ou}`);
      }
      await E.fermer();
    }
  expect(n, 'des textes relevés').toBeGreaterThan(10);
  expect(fautes, 'couples demandés mais absents (casseraient en Swift)').toEqual([]);
});

// ─────────────────────────────────────────────────────────── redteam_lettres_bleu ──

/**
 * redteam_lettres_bleu (v203 clôture, Tom, C-281) — « ces lettres clignotent dans le bleu clair EXACT de la palette de base […] Au sommet du
 * clignotement, la couleur exacte, à pleine opacité : aucun filtre, aucun mode de fusion, aucune opacité qui ternit. Le même code de
 * clignotement partout (C-247). Juge : valeur des pixels de chaque lettre au sommet du clignotement, égale à la couleur de la palette à 1,5
 * près, sur les deux thèmes ». Transversal : TOUTE lettre qui porte `promiBlink` à l'écran, sur chaque écran porté ; le I de PROMI de
 * l'accueil y est exigé. Le R de PARTAGER, le S de RÉGLAGES : s'étendent au lot 8 ; l'apostrophe de l'Aura (C-308) : lot 6 ;
 * l'onboarding : lot 9 — sans rien toucher ici (le relevé les prend dès qu'ils clignotent).
 */
const BLEU: [number, number, number] = [0x82, 0xae, 0xf8]; // #82AEF8, PALS.signal.cols[0] (Ingénu, la palette de base)
const PROMI_BLINK = { duree: 1150, pas: 'steps(1' }; // promiBlink 1,15 s steps(1,end) — le même code partout (C-247)

test('les lettres qui clignotent : au sommet, le bleu exact #82AEF8, sur chaque écran porté, deux thèmes (redteam_lettres_bleu, C-281)', async ({
  browser,
}) => {
  // la palette de base le déclare (le moteur repris, octet pour octet) et le jeton aussi
  const m = /signal:\{name:'Ingénu',cols:\[\[(\d+),(\d+),(\d+)\]/.exec(
    lire(join(SRC, 'moteur', 'repris', 'promi-moteur.js')),
  );
  expect(m?.slice(1).map(Number), 'PALS.signal déclare #82AEF8 en premier ton').toEqual(BLEU);
  expect(/--c-bleu45:#82AEF8;/i.test(lire(join(SRC, 'design', 'jetons.css'))), 'le jeton --c-bleu45 vaut #82AEF8').toBe(
    true,
  );
  for (const ecran of ECRANS_PORTES)
    for (const theme of THEMES) {
      const E = await ouvrirEcran(browser, ecran, { theme, dsf: 3 });
      if (sonde('bleu-terni'))
        await E.page.evaluate(() => {
          document.querySelector<HTMLElement>('.acc-mm i')!.style.setProperty('opacity', '.9', 'important');
        });
      const L = (await E.page.evaluate(`(() => { const out = [];
        for (const e of document.querySelectorAll('body *')) {
          const a = (e.getAnimations ? e.getAnimations() : []).find((x) => x.animationName === 'promiBlink'); if (!a) continue;
          const r = e.getBoundingClientRect(); if (r.width < 1 || r.top < 0 || r.bottom > innerHeight) continue;
          const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); if (!h || !(h === e || e.contains(h))) continue;
          a.pause(); a.currentTime = 0;
          let op = 1; const tern = []; for (let q = e; q; q = q.parentElement) { const k = getComputedStyle(q); op *= +k.opacity;
            if (k.filter !== 'none') tern.push('filtre'); if (k.mixBlendMode !== 'normal') tern.push('fusion'); }
          if (getComputedStyle(e).textShadow !== 'none') tern.push('ombre');
          out.push({ sel: e.matches('.acc-mm i') ? '.acc-mm i' : (e.id || e.className || e.tagName), x: r.left - 4, y: r.top - 2, w: r.width + 8, h: r.height + 4,
            duree: a.effect.getTiming().duration, pas: getComputedStyle(e).animationTimingFunction, op, tern }); }
        return out; })()`)) as Array<{
        sel: string;
        x: number;
        y: number;
        w: number;
        h: number;
        duree: number;
        pas: string;
        op: number;
        tern: string[];
      }>;
      await E.page.waitForTimeout(120);
      if (ecran.nom.startsWith('accueil'))
        expect(
          L.map((l) => l.sel),
          `${ecran.nom}, ${theme} : le I de PROMI clignote à l'écran`,
        ).toContain('.acc-mm i');
      for (const l of L) {
        const im = await zone(E.page, l.x, l.y, l.w, l.h);
        const px = (x: number, y: number): [number, number, number] => {
          const i = (y * im.width + x) * 4;
          return [im.data[i]!, im.data[i + 1]!, im.data[i + 2]!];
        };
        const compte = new Map<string, number>();
        const bord: string[] = [];
        for (let x = 0; x < im.width; x++) bord.push(px(x, 0).join(), px(x, im.height - 1).join());
        for (let y = 0; y < im.height; y++) bord.push(px(0, y).join(), px(im.width - 1, y).join());
        for (const b of bord) compte.set(b, (compte.get(b) ?? 0) + 1);
        const fond = [...compte.entries()]
          .sort((a, b) => b[1] - a[1])[0]![0]
          .split(',')
          .map(Number);
        const encre = new Map<string, number>();
        for (let y = 0; y < im.height; y++)
          for (let x = 0; x < im.width; x++) {
            const p = px(x, y);
            if (Math.abs(p[0] - fond[0]!) + Math.abs(p[1] - fond[1]!) + Math.abs(p[2] - fond[2]!) > 60)
              encre.set(p.join(), (encre.get(p.join()) ?? 0) + 1);
          }
        const coeur = [...encre.entries()]
          .sort((a, b) => b[1] - a[1])[0]?.[0]
          .split(',')
          .map(Number);
        const ou = `${ecran.nom}, ${theme}, ${l.sel}`;
        expect(coeur, `${ou} : de l'encre`).toBeTruthy();
        expect
          .soft(
            Math.max(...coeur!.map((v, j) => Math.abs(v - BLEU[j]!))),
            `${ou} : le cœur ${coeur!.join(',')} = #82AEF8 à 1,5 près`,
          )
          .toBeLessThanOrEqual(1.5);
        expect.soft(Math.abs(l.duree - PROMI_BLINK.duree), `${ou} : promiBlink 1,15 s`).toBeLessThan(1);
        expect.soft(l.pas.replace(/\s/g, ''), `${ou} : steps(1,end)`).toContain(PROMI_BLINK.pas);
        expect.soft({ op: l.op, tern: l.tern }, `${ou} : rien qui ternit`).toEqual({ op: 1, tern: [] });
      }
      await E.fermer();
    }
});

// ───────────────────────────────────────────────────────────────── redteam_kaki ──

/**
 * redteam_kaki (Tom, v114 : « jamais de kaki », règle absolue ; v115 : « le crème et les jaunes vifs ne sont pas du kaki ») — EST KAKI toute
 * couleur de teinte OKLCH 78°–140°, de chroma 0,015–0,10 ET de luminance 0,20–0,80. Interdit sur toute dalle et toute matière vide produite
 * par l'app. La vraie app ne peint ses dalles que par le moteur repris (octet pour octet) : on juge ce qu'il porte et ce qu'il rend, et on
 * NOMME À PART la dette du prototype (ses rouges, relevés par redteam_kaki le 8 nov. 2026, kaki-coupables.json ; la vraie app les rejoue au
 * dixième de point, mesuré le 20 nov.) : ce qu'elle produit de NEUF fait échouer — une Toile hors de la dette au-delà de 0,5 %, ou la dette
 * qui grandit ; la dette elle-même est annotée et ne se décide pas ici (Tom). L'interface (plateau, barre : l'encre brune #201908 est h 87°)
 * n'est pas de la matière (CLAUDE.md §3, v114 : « hors périmètre, c'est une page »).
 */
const KAKI = { hMin: 78, hMax: 140, cMin: 0.015, cMax: 0.1, lMin: 0.2, lMax: 0.8 }; // décision Tom, v115
const SEUIL_PART = 0.005; // 0,5 % des pixels opaques d'une image (redteam_kaki)
const kakiCache = new Map<number, boolean>();
function estKaki(r: number, g: number, b: number): boolean {
  const k = (r << 16) | (g << 8) | b;
  let v = kakiCache.get(k);
  if (v === undefined) {
    const [L, C, h] = oklch(r, g, b);
    v = h >= KAKI.hMin && h <= KAKI.hMax && C >= KAKI.cMin && C <= KAKI.cMax && L >= KAKI.lMin && L <= KAKI.lMax;
    kakiCache.set(k, v);
  }
  return v;
}
/** la dette du prototype, nommée (redteam_kaki --rendu, 8 nov. 2026) : monde · vue → part kaki relevée */
const DETTE_KAKI: Record<string, number> = {
  'encre toile-sombre': 0.008,
  'touffe toile-clair': 0.108,
  'touffe toile-sombre': 0.011,
  'esquille toile-sombre': 0.007,
  'braille toile-sombre': 0.033,
  'ramage toile-clair': 0.049,
  'guingois toile-clair': 0.076,
  'chantourne toile-clair': 0.074,
  'volubilis toile-clair': 0.024,
  'chamade toile-clair': 0.06,
  'bobinette toile-sombre': 0.02,
  'mascaret toile-clair': 0.054,
  'terrazzo toile-sombre': 0.008,
  'gravure toile-sombre': 0.056,
  'sillons toile-sombre': 0.066,
};
const MONDES = [
  'encre',
  'touffe',
  'brouillamini',
  'halin',
  'esquille',
  'mosaique',
  'braille',
  'pixel',
  'ramage',
  'guingois',
  'chantourne',
  'volubilis',
  'madrure',
  'chamade',
  'ritournelle',
  'bobinette',
  'mascaret',
  'terrazzo',
  'gravure',
  'sillons',
];

test('jamais de kaki : la source du moteur repris — palettes du Studio, rampes des cellules vides, fond de la Toile (redteam_kaki A)', () => {
  let M = lire(join(SRC, 'moteur', 'repris', 'promi-moteur.js'));
  if (sonde('kaki-palette'))
    M = M.replace(
      "signal:{name:'Ingénu',cols:[[130,174,248]",
      "signal:{name:'Ingénu',cols:[[130,122,106],[130,174,248]",
    );
  const nomC = (c: number[]): string => {
    const [L, C, h] = oklch(c[0]!, c[1]!, c[2]!);
    return `rgb(${c.join(',')}) (h ${h.toFixed(0)}°, C ${C.toFixed(3)}, L ${L.toFixed(2)})`;
  };
  const coupables: string[] = [];
  let n = 0;
  for (const m of M.matchAll(/(\w+):\{name:'([^']+)',cols:(\[\[[\d,[\] ]+\]\])/g))
    for (const c of JSON.parse(m[3]!) as number[][]) {
      n++;
      if (estKaki(c[0]!, c[1]!, c[2]!)) coupables.push(`palette ${m[2]!} ${nomC(c)}`);
    }
  for (const m of M.matchAll(/\b(G(?:PIX|BRA|LI|MOS|ENC|LIGHT))\s*=\s*(\[\[[\d,[\] ]+\]\])/g))
    for (const c of JSON.parse(m[2]!) as number[][]) {
      n++;
      if (estKaki(c[0]!, c[1]!, c[2]!)) coupables.push(`rampe des vides ${m[1]!} ${nomC(c)}`);
    }
  const f = /function _fondVifDesc[^}]*\}/.exec(M);
  expect(f, 'le fond de la Toile (_fondVifDesc) est lu').toBeTruthy();
  for (const h of f![0].matchAll(/'#([0-9A-Fa-f]{6})'/g)) {
    const c = [0, 2, 4].map((i) => parseInt(h[1]!.slice(i, i + 2), 16));
    n++;
    if (estKaki(c[0]!, c[1]!, c[2]!)) coupables.push(`fond de la Toile ${nomC(c)}`);
  }
  expect(n, 'les 24 palettes, les rampes et le fond sont lus').toBeGreaterThan(24 * 4);
  // la dette du prototype côté source est VIDE (redteam_kaki --source, 20 nov. 2026 : « AUCUN KAKI ») : tout coupable est neuf
  expect(coupables, 'aucun kaki dans la source').toEqual([]);
});

const POSE_KAKI = `(a)=>{ const [monde,graine,neufs]=a; const autre = neufs.indexOf(monde)>=0 ? 'encre' : 'esquille';
  const oublie=()=>{ try{ promises.forEach(p=>{ delete p.place; }); }catch(e){} try{ window.NUEPLACE={}; localStorage.removeItem('promi_nueplace'); }catch(e){} };
  oublie(); Toile.setTheme(autre); oublie(); window.__amorce(graine); try{ window._chaOublie&&window._chaOublie(); }catch(e){} Toile.setTheme(monde); return Toile.getTheme(); }`;

test('jamais de kaki : la Toile des vingt mondes rendue par la vraie app, clair et sombre — rien de neuf hors de la dette du prototype (redteam_kaki B)', async ({
  browser,
}) => {
  if (process.env['CI']) test.setTimeout(30 * 60 * 1000);
  const etat = JSON.parse(lire(join(import.meta.dirname, 'etat-banc-rendu.json'))) as { ls: Record<string, string> };
  const ctx = await browser.newContext({ viewport: REF, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  // l'état, le hasard et le temps du banc de rendu (banc_rendu.py : c'est sur lui que la dette a été relevée)
  await page.addInitScript((a) => new Function(a)(), AMORCE);
  await page.goto(`http://127.0.0.1:5180/?banc=1&pilote=${String(T_FIGE)}`);
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await page.evaluate(async (ls) => {
    const p = (
      window as unknown as {
        __promi: { magasin: { importer(x: unknown): void }; demarrer(o?: { accueil?: boolean }): Promise<void> };
      }
    ).__promi;
    p.magasin.importer({ ls });
    await p.demarrer({ accueil: false });
  }, etat.ls);
  const neufs = (await page.evaluate(
    `(()=>{ const r=[]; for(const m of ${JSON.stringify(MONDES)}){ Toile.setTheme(m); if(Toile.semisNeuf()) r.push(m); } return r; })()`,
  )) as string[];
  const neuf: string[] = [];
  const dette: string[] = [];
  for (const m of MONDES) {
    await page.evaluate(`(${POSE_KAKI})(${JSON.stringify([m, GRAINE, neufs])})`);
    for (let i = 0; i < 6; i++) await page.evaluate(`${P_}.horloge.images(40)`);
    const im = (await page.evaluate(
      `(() => { const lab = window._shLabels; window._shLabels = false; const out = {};
        try { for (const cl of [true, false]) { const cv = document.createElement('canvas');
          out[cl ? 'toile-clair' : 'toile-sombre'] = Toile.renderTo(cv, 1, cl) ? (${String(sonde('kaki-rendu'))} ? (() => {
            const g = cv.getContext('2d'); g.fillStyle = 'rgb(130,122,106)'; g.fillRect(0, 0, cv.width, cv.height * 0.05); return cv; })() : cv).toDataURL('image/png') : null; } }
        finally { window._shLabels = lab; } return out; })()`,
    )) as Record<string, string | null>;
    for (const [vue, url] of Object.entries(im)) {
      const cle = `${m} ${vue}`;
      if (!url) {
        neuf.push(`${cle} : pas de rendu`);
        continue;
      }
      const P = PNG.sync.read(Buffer.from(url.split(',', 2)[1]!, 'base64'));
      let k = 0;
      let t = 0;
      for (let i = 0; i < P.data.length; i += 4) {
        if (P.data[i + 3]! <= 200) continue;
        t++;
        if (estKaki(P.data[i]!, P.data[i + 1]!, P.data[i + 2]!)) k++;
      }
      const part = t ? k / t : 0;
      // la dette ne grandit pas : sa part relevée (arrondie au dixième de point) + l'arrondi — jugé sur le Mac (le WebKit de l'iPhone), où
      // la dette a été relevée ; sous Linux le lissage des bords la fait grandir de 1 à 1,5 point (Q616) : non jugé, comme les images figées
      if (cle in DETTE_KAKI && MAC_DE_TOM && part > DETTE_KAKI[cle]! + 0.0005)
        neuf.push(
          `${cle} : la dette grandit — ${(100 * part).toFixed(2)} % kaki (relevé : ${(100 * DETTE_KAKI[cle]!).toFixed(1)} %)`,
        );
      if (cle in DETTE_KAKI)
        dette.push(
          `${cle} ${(100 * part).toFixed(1)} % (relevé du prototype : ${(100 * DETTE_KAKI[cle]!).toFixed(1)} %)`,
        );
      else if (part > SEUIL_PART) neuf.push(`${cle} : ${(100 * part).toFixed(1)} % kaki`);
    }
  }
  test
    .info()
    .annotations.push({ type: 'dette du prototype (nommée, à décider par Tom)', description: dette.join(' · ') });
  console.log(`kaki — la dette du prototype, rejouée par la vraie app : ${dette.join(' · ')}`);
  await ctx.close();
  expect(erreurs).toEqual([]);
  expect(neuf, 'du kaki NEUF, hors de la dette nommée du prototype').toEqual([]);
});

// ──────────────────────────────────────────────────────────────── releve-design ──

/**
 * releve-design (le contrat visuel, CLAUDE.md §8 bis : « 148 propriétés sur 26 éléments […] un écart non demandé par le lot est une
 * régression ») — porté contre la référence d'aujourd'hui, le PROTOTYPE (reference-v205 ; design-reference.json décrit la fiche d'août et
 * ses 26 éléments sont ceux de la fiche et du Cercle : ils s'étendent aux lots 3a et 5, où `CIBLES` ci-dessous les trouvera). Sur chaque écran
 * porté, clair et sombre, chaque élément qui porte un id dans les deux, chaque texte (rangé sous l'id qui le porte), visible des deux côtés — et
 * chaque cible de releve-design —, relève les
 * 25 propriétés du juge (PROPS, en dur) : elles sont égales, à 4 unités près pour une couleur seulement (`_proche`). Et « aucun trait neutre » : aucun
 * `box-shadow` gris (max − min < 26) hors de l'encre et du papier, ni dans l'app ni dans les cibles.
 */
const PROPS = [
  'fontFamily',
  'fontSize',
  'fontWeight',
  'letterSpacing',
  'lineHeight',
  'textTransform',
  'color',
  'backgroundColor',
  'opacity',
  'paddingTop',
  'paddingRight',
  'paddingBottom',
  'paddingLeft',
  'marginTop',
  'marginBottom',
  'borderRadius',
  'boxShadow',
  'width',
  'height',
  'display',
  'position',
  'gap',
  'zIndex',
  'filter',
  'mixBlendMode',
];
const CIBLES = [
  '#detailPoster .dpt-nat',
  '#dpTete .dpt-qui',
  '#dpTete .dpt-titre',
  '#dpTete .dpt-quand',
  '#detailPoster .closeb',
  '#dAura',
  '#detailPoster .kr-c',
  '#detailPoster .kr-n',
  '#detailPoster .kr-w',
  '#tenirZone',
  '#detailPoster .tenir-lab',
  '#detailPoster .tenir-alt',
  '#dpDetails .dpd-tog',
  '#dpDetails .dpd-part',
  '#detailPoster .mg-lab',
  '#detailPoster input',
  '#detailPoster .chip',
  '#dpNueeFil .nf-item',
  '#dpNueeFil .nf-tx em',
  '#dpNueeFil .nf-tx b',
  '#dpNueeFil .nf-tx span',
  '#dpNueeFil .nf-d',
  '#dpNueeFil .nf-add',
  '#dpTrace .dpt-lab',
  '#dpTrace .dpt-svg',
];
const ENCRES_TRAIT = ['32,25,8', '247,240,222', '22,23,27', '244,238,225']; // releve-design, ENCRES : l'encre et le papier ne sont pas des gris
const RELEVE_DESIGN = `(a) => { const [props, cibles] = a; const out = {};
  /* les animations à leur début, des deux côtés (le I qui clignote : l'opacité d'un instant n'est pas le contrat ; son clignotement est jugé à part) */
  for (const x of document.getAnimations()) { x.pause(); x.currentTime = 0; }
  const dv = document.getElementById('device'); const D = dv.getBoundingClientRect();
  const vu = (e) => { for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = getComputedStyle(x);
      if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; }
    const r = e.getBoundingClientRect(); return r.width >= 1 && r.height >= 1 && r.bottom > D.top && r.top < D.bottom && r.right > D.left && r.left < D.right; };
  const prendre = (cle, e) => { const c = getComputedStyle(e); const d = {}; for (const p of props) d[p] = c[p]; const r = e.getBoundingClientRect(); d._px = [Math.round(r.width), Math.round(r.height)];
    d._texte = [...e.childNodes].some((x) => x.nodeType === 3 && x.nodeValue.trim()); out[cle] = d; };
  for (const e of dv.querySelectorAll('[id]')) if (vu(e)) prendre('#' + e.id, e);
  for (const e of dv.querySelectorAll('*')) { if (e.id || !vu(e)) continue; let t = ''; e.childNodes.forEach((x) => { if (x.nodeType === 3) t += x.nodeValue; });
    t = t.trim().replace(/\\s+/g, ' '); const p = e.parentElement && e.parentElement.closest('[id]'); if (t && p) prendre('#' + p.id + ' « ' + t.slice(0, 30) + ' »', e); }
  for (const s of cibles) { const e = document.querySelector(s); if (e && vu(e)) prendre(s, e); }
  return out; }`;
function proche(a: string, b: string): boolean {
  if (a === b) return true;
  const ma = a.match(/[\d.]+/g) ?? [];
  const mb = b.match(/[\d.]+/g) ?? [];
  if (!ma.length || ma.length !== mb.length || a.replace(/[\d.]+/g, '') !== b.replace(/[\d.]+/g, '')) return false;
  return ma.every((x, i) => Math.abs(+x - +mb[i]!) <= 4);
}

/**
 * Ce qui se compare : ce qui SE VOIT. La vraie app est écrite de zéro (une autre arborescence que le prototype) : la façon dont une boîte est
 * posée — `display`, `position`, `z-index`, et la largeur et la hauteur CALCULÉES, qui dépendent de `box-sizing` — n'est pas le contrat :
 * la taille qu'on voit est la boîte RENDUE (`_px`, comparée), l'ordre des calques est jugé au pixel par accueil.spec ; les propriétés
 * du texte ne se voient que sur un élément qui PORTE du texte (une boîte vide n'affiche aucune police : le juge des polices le dit déjà).
 */
/** releve-design, `_proche` : « deux couleurs à moins de 4 unités près sont la même » — pour une couleur seulement */
const COULEURS = new Set(['color', 'backgroundColor', 'boxShadow']);
const DE_POSE = new Set(['display', 'position', 'zIndex', 'width', 'height']);
const DU_TEXTE = new Set([
  'fontFamily',
  'fontSize',
  'fontWeight',
  'letterSpacing',
  'lineHeight',
  'textTransform',
  'color',
]);

test('le contrat visuel : les 25 propriétés de chaque élément porté égales à celles du prototype, et aucun trait neutre (releve-design)', async ({
  browser,
}) => {
  const ecarts: string[] = [];
  const neutres: string[] = [];
  let compares = 0;
  for (const theme of THEMES)
    for (const ecran of ECRANS_PORTES) {
      const ls = { ...stockage(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const cp = await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 1 });
      const P = await cp.newPage();
      const [, E] = await Promise.all([prototype(P, ls), ouvrirEcran(browser, ecran, { theme, dsf: 1 })]);
      if (sonde('design-ecart'))
        await E.page.addStyleTag({ content: '#device #studioBtn .l{letter-spacing:1px!important}' });
      if (sonde('design-neutre'))
        await E.page.addStyleTag({ content: '#device #accPlat{box-shadow:0 0 0 2px rgb(136,136,136)!important}' });
      await ecran.prototype(P);
      await P.waitForTimeout(400);
      const [rp, ra] = (await Promise.all([
        P.evaluate(`(${RELEVE_DESIGN})(${JSON.stringify([PROPS, CIBLES])})`),
        E.page.evaluate(`(${RELEVE_DESIGN})(${JSON.stringify([PROPS, CIBLES])})`),
      ])) as Array<Record<string, Record<string, unknown>>>;
      for (const [cle, d] of Object.entries(ra!)) {
        const bs = String(d['boxShadow'] ?? '');
        for (const c of bs.matchAll(/rgba?\(([^)]*)\)/g)) {
          const v = (c[1]!.match(/[\d.]+/g) ?? []).slice(0, 3).map((x) => Math.round(+x));
          if (
            v.length === 3 &&
            Math.max(...v) - Math.min(...v) < 26 &&
            !ENCRES_TRAIT.includes(v.join()) &&
            !(Math.max(...v) < 30 || Math.min(...v) > 225)
          )
            neutres.push(`${ecran.nom}, ${theme} · ${cle} : trait NEUTRE rgb(${v.join(',')})`);
        }
        const p = rp![cle];
        if (!p) continue;
        compares++;
        for (const k of [...PROPS, '_px']) {
          if (DE_POSE.has(k) || (DU_TEXTE.has(k) && !(d['_texte'] || p['_texte']))) continue;
          const a = JSON.stringify(p[k]);
          const b = JSON.stringify(d[k]);
          if (
            a !== b &&
            !(COULEURS.has(k) && proche(a, b)) &&
            !ecartAdmis(ecran.nom, cle.includes('« garder de côté »') ? 'garder de côté' : '', k)
          )
            ecarts.push(`${ecran.nom}, ${theme} · ${cle} · ${k} : ${a} → ${b}`);
        }
      }
      await E.fermer();
      await cp.close();
    }
  expect(compares, 'des éléments comparés').toBeGreaterThan(8);
  expect(neutres, 'aucun trait neutre').toEqual([]);
  expect(ecarts, 'écarts au prototype').toEqual([]);
});

// ──────────────────────────────────────────────────────────────── redteam_croix ──

/**
 * redteam_croix (v157, Tom, C-173 : « Partout, “× FERMER” devient un seul “X”, sans mot » ; v158, C-173 récidive : « Le MÊME X partout :
 * PromiLate, même taille, même couleur de rôle ; sa taille est EXACTEMENT celle du “X” du mot “INDEX” ») — sur chaque écran porté, à deux
 * échelles (390 × 844 et 330 × 714, la fenêtre de Safari), deux thèmes : A aucun texte « FERMER » visible ; B chaque fermeture
 * (`aria-label="Fermer"` ou `.closeb`) dit « X » en PromiLate, 29,5 px (`_tailleX`, le X de « INDEX », v158 ; la taille commune des titres, v211
 * C-307 et Q623 acceptée), son encre lue sur l'image = celle d'un « X » de PromiLate 29,5 px posé par le juge et lu de la même façon, ± 0,5 pt ; C sa couleur = celle du titre de sa rangée, à pleine opacité ; D sa zone de toucher
 * ≥ 44 × 44, centrée sur l'encre (± 1,5 pt), prise par le doigt à ses quatre coins (± 20 pt). L'accueil n'a aucune fermeture (A seul) ;
 * B, C, D mordent dès qu'un écran porté en porte une (lots 3a, 4, 6, 7, 8).
 */
/** l'encre d'un élément, lue sur l'image : peint, puis sa couleur rendue transparente (le fond, la Toile figée en dessous, ne compte pas) */
async function encreLue(
  pg: Page,
  sel: string,
): Promise<{ boite: [number, number, number, number]; encre: [number, number]; centre: [number, number] } | null> {
  // un fond uni, contrasté, posé le temps de la lecture : le bord d'une lettre ne dépend plus de ce qui est dessous
  const r = (await pg.evaluate((s) => {
    const e = document.querySelector<HTMLElement>(s)!;
    const m = /(\d+)\D+(\d+)\D+(\d+)/.exec(getComputedStyle(e).color);
    const lum = m ? 0.299 * +m[1]! + 0.587 * +m[2]! + 0.114 * +m[3]! : 255;
    e.style.setProperty('background', lum > 128 ? '#000' : '#fff', 'important');
    const b = e.getBoundingClientRect();
    return [b.left, b.top, b.width, b.height];
  }, sel)) as [number, number, number, number];
  const cl = { x: Math.max(0, r[0] - 6), y: Math.max(0, r[1] - 6), w: r[2] + 12, h: r[3] + 12 };
  const avec = await zone(pg, cl.x, cl.y, cl.w, cl.h);
  await pg.evaluate((s) => {
    document.querySelector<HTMLElement>(s)!.style.setProperty('color', 'transparent', 'important');
  }, sel);
  const sans = await zone(pg, cl.x, cl.y, cl.w, cl.h);
  await pg.evaluate((s) => {
    const e = document.querySelector<HTMLElement>(s)!;
    e.style.removeProperty('color');
    e.style.removeProperty('background');
  }, sel);
  const k = avec.width / cl.w;
  let x0 = 1e9;
  let y0 = 1e9;
  let x1 = -1;
  let y1 = -1;
  for (let y = 0; y < avec.height; y++)
    for (let x = 0; x < avec.width; x++) {
      const j = (y * avec.width + x) * 4;
      if (Math.max(...[0, 1, 2].map((c) => Math.abs(avec.data[j + c]! - sans.data[j + c]!))) <= 24) continue;
      x0 = Math.min(x0, x);
      y0 = Math.min(y0, y);
      x1 = Math.max(x1, x);
      y1 = Math.max(y1, y);
    }
  if (x1 < 0) return null;
  return {
    boite: r,
    encre: [(x1 - x0 + 1) / k, (y1 - y0 + 1) / k],
    centre: [cl.x + (x0 + x1 + 1) / 2 / k, cl.y + (y0 + y1 + 1) / 2 / k],
  };
}

const TAILLE_X = 29.5; // px — v158 (C-173) : la taille du X de « INDEX » (`window._tailleX`) ; v211 (C-307) : la taille commune des titres, 29,5 ; Q623 (v212) : Tom garde le lien

test('× FERMER est un seul X : aucun « FERMER », le X en PromiLate 29,5 px, la couleur du titre, 44 pt de zone (redteam_croix, C-173)', async ({
  browser,
}) => {
  const fautes: string[] = [];
  for (const vue of [REF, { width: 330, height: 714 }])
    for (const ecran of ECRANS_PORTES)
      for (const theme of THEMES) {
        const E = await ouvrirEcran(browser, ecran, { theme, vue, dsf: 3 });
        const pg = E.page;
        if (sonde('croix-fermer'))
          await pg.evaluate(() => {
            const b = document.createElement('div');
            b.className = 'closeb';
            b.setAttribute('aria-label', 'Fermer');
            b.setAttribute('role', 'button');
            b.style.cssText =
              'position:absolute;right:40px;top:58px;z-index:99;font:400 14px PromiLate;color:#F7F0DE;padding:14px';
            b.textContent = '✕ FERMER';
            document.getElementById('device')!.appendChild(b);
          });
        if (sonde('croix-taille'))
          await pg.evaluate(() => {
            const b = document.createElement('div');
            b.setAttribute('aria-label', 'Fermer');
            b.setAttribute('role', 'button');
            b.style.cssText =
              'position:absolute;right:40px;top:150px;z-index:99;font:400 42px PromiLate;color:#82AEF8;width:44px;height:44px;display:grid;place-items:center';
            b.textContent = 'X';
            document.getElementById('device')!.appendChild(b);
          });
        const ou = `${ecran.nom}, ${theme}, ${String(vue.width)} × ${String(vue.height)}`;
        // A · aucun « FERMER » visible
        const mots =
          (await pg.evaluate(`(() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let t;
          while ((t = w.nextNode())) { if (!/fermer/i.test(t.nodeValue)) continue; const e = t.parentElement; const rg = document.createRange(); rg.selectNodeContents(t);
            const r = rg.getBoundingClientRect(); if (r.width < 1 || r.bottom < 0 || r.top > innerHeight) continue;
            let v = true; for (let x = e; x; x = x.parentElement) { const c = getComputedStyle(x); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) v = false; }
            if (v) out.push(t.nodeValue.trim()); } return out; })()`)) as string[];
        for (const m of mots) fautes.push(`${ou} : A · « ${m} » à l'écran`);
        // B, C, D · chaque fermeture visible
        const X = (await pg.evaluate(`(() => { const out = [];
          for (const e of document.querySelectorAll('[aria-label="Fermer"], .closeb')) { const r = e.getBoundingClientRect();
            if (r.width < 1 || r.bottom < 0 || r.top > innerHeight) continue; const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden') continue;
            const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); if (!h || !(h === e || e.contains(h))) continue;
            e.setAttribute('data-croix', String(out.length));
            let op = 1; for (let q = e; q; q = q.parentElement) op *= +getComputedStyle(q).opacity;
            const cy = r.top + r.height / 2; let titre = null, fs = 0;
            for (const t of document.querySelectorAll('body *')) { if (t === e || e.contains(t) || t.contains(e)) continue;
              let s = ''; t.childNodes.forEach((x) => { if (x.nodeType === 3) s += x.nodeValue; }); if (!s.trim()) continue;
              const q = t.getBoundingClientRect(); if (q.right > r.left || Math.abs(q.top + q.height / 2 - cy) > 20) continue;
              const k = getComputedStyle(t); if (k.visibility === 'hidden' || k.display === 'none') continue; const f = parseFloat(k.fontSize); if (f > fs) { fs = f; titre = k.color; } }
            out.push({ i: out.length, texte: (e.textContent || '').trim(), fam: c.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase(), fs: parseFloat(c.fontSize),
              couleur: c.color, titre, op, r: [r.left, r.top, r.width, r.height] }); }
          return out; })()`)) as Array<{
          i: number;
          texte: string;
          fam: string;
          fs: number;
          couleur: string;
          titre: string | null;
          op: number;
          r: [number, number, number, number];
        }>;
        // le X de référence : « X » en PromiLate 29,5 px (le X de « INDEX », v158), à la couleur de la fermeture, lu sur l'image de la même façon
        // (posé à la même phase dans le pixel que le texte de la fermeture : le lissage d'un bord en dépend)
        const refX = async (couleur: string, i: number): Promise<[number, number] | null> => {
          await pg.evaluate(
            ([c, t, i]) => {
              const e = document.querySelector(`[data-croix="${String(i)}"]`)!;
              const rg = document.createRange();
              rg.selectNodeContents(e);
              const q = rg.getBoundingClientRect();
              const s = document.createElement('span');
              s.id = 'croixTemoin';
              s.textContent = 'X';
              s.style.cssText = `position:absolute;left:${String(110 + q.left - Math.floor(q.left))}px;top:${String(290 + q.top - Math.floor(q.top))}px;z-index:99;font:400 ${String(t)}px PromiLate;line-height:${String(q.height)}px;padding:10px;color:${String(c)}`;
              (e.parentElement ?? document.body).appendChild(s);
            },
            [couleur, TAILLE_X, i] as const,
          );
          const e = await encreLue(pg, '#croixTemoin');
          await pg.evaluate(() => document.getElementById('croixTemoin')!.remove());
          return e ? e.encre : null;
        };
        for (const x of X) {
          const q = `${ou} · fermeture ${String(x.i)}`;
          if (x.texte !== 'X' || x.fam !== 'promilate' || Math.abs(x.fs - TAILLE_X) > 0.25)
            fautes.push(
              `${q} : B · « ${x.texte} » en ${x.fam} ${String(x.fs)} px (X, PromiLate ${String(TAILLE_X)} px)`,
            );
          if (x.titre && x.couleur !== x.titre) fautes.push(`${q} : C · ${x.couleur} ≠ le titre ${x.titre}`);
          if (x.op < 0.999) fautes.push(`${q} : C · opacité ${x.op.toFixed(2)}`);
          // l'encre, lue sur l'image : la croix peinte, puis effacée — contre le X de référence, lu de la même façon
          const [l, t, w, h] = x.r;
          const lu = await encreLue(pg, `[data-croix="${String(x.i)}"]`);
          const ref = await refX(x.couleur, x.i);
          if (!lu || !ref) {
            fautes.push(`${q} : B · aucune encre lue`);
            continue;
          }
          // EXCEPTION NOMMÉE (Tom, 25 nov. 2026) : le juge exact tourne sur macOS (le WebKit de l'iPhone) ; hors macOS, le rendu des polices de la
          // machine (Linux) dessine le X de PromiLate 24,3 × 21,3 pour 25,0 × 21,7 — l'encre y est jugée à 1 pt près
          const TOL_X = process.platform === 'darwin' ? 0.5 : 1;
          if (Math.abs(lu.encre[0] - ref[0]) > TOL_X || Math.abs(lu.encre[1] - ref[1]) > TOL_X)
            fautes.push(
              `${q} : B · encre ${lu.encre.map((v) => v.toFixed(1)).join(' × ')} ≠ le X de PromiLate ${String(TAILLE_X)} px ${ref.map((v) => v.toFixed(1)).join(' × ')}`,
            );
          // D · la zone de toucher
          const [cx, cy] = lu.centre;
          if (w < 44 || h < 44) fautes.push(`${q} : D · zone ${w.toFixed(0)} × ${h.toFixed(0)} (≥ 44 × 44)`);
          if (Math.abs(l + w / 2 - cx) > 1.5 || Math.abs(t + h / 2 - cy) > 1.5)
            fautes.push(`${q} : D · zone décentrée de l'encre`);
          const prise = (await pg.evaluate(
            ([i, cx, cy]) => {
              const e = document.querySelector(`[data-croix="${String(i)}"]`)!;
              return [
                [-20, -20],
                [20, -20],
                [-20, 20],
                [20, 20],
              ].every(([dx, dy]) => {
                const h = document.elementFromPoint(cx! + dx!, cy! + dy!);
                return !!h && (h === e || e.contains(h));
              });
            },
            [x.i, cx, cy],
          )) as boolean;
          if (!prise) fautes.push(`${q} : D · le doigt ne la prend pas à ± 20 pt du centre`);
        }
        await E.fermer();
      }
  expect(fautes).toEqual([]);
});

// ───────────────────────────────────────────────────────── redteam_vide, redteam_enchaine ──

function comparerEmpreintes(ref: Empreinte, e: Empreinte): string[] {
  const out: string[] = [];
  const perdus = ref.mots.filter((m) => !e.mots.includes(m));
  if (perdus.length) out.push(`mots perdus : ${perdus.slice(0, 6).join(' · ')}`);
  const trop = e.mots.filter((m) => !ref.mots.includes(m));
  if (trop.length) out.push(`mots en trop : ${trop.slice(0, 6).join(' · ')}`);
  const np = ref.noeuds.filter((n) => !e.noeuds.includes(n));
  if (np.length) out.push(`nœuds perdus : ${np.join(' · ')}`);
  const nt = e.noeuds.filter((n) => !ref.noeuds.includes(n));
  if (nt.length) out.push(`nœuds d'un autre écran : ${nt.join(' · ')}`);
  for (const [k, v] of Object.entries(ref.cls))
    if (e.cls[k] !== undefined && e.cls[k] !== v) out.push(`classes de ${k} : « ${e.cls[k]} » au lieu de « ${v} »`);
  for (const [k, n] of Object.entries(ref.canevas)) {
    const m = e.canevas[k];
    if (m === undefined) out.push(`canevas ${k} absent`);
    else if (n >= 200 && m < 200) out.push(`canevas ${k} PAS PEINT (${String(m)})`);
  }
  return out;
}

async function references(browser: Browser, themes: Theme[]): Promise<Record<string, Empreinte>> {
  const ref: Record<string, Empreinte> = {};
  for (const theme of themes)
    for (const ecran of ECRANS_PORTES) {
      const E = await ouvrirEcran(browser, ecran, { theme });
      await E.page.waitForTimeout(600);
      ref[`${theme} · ${ecran.nom}`] = (await E.page.evaluate(EMPREINTE)) as Empreinte;
      await E.fermer();
    }
  return ref;
}

/**
 * redteam_vide (« UN ÉCRAN N'EST JAMAIS VIDE » : il ENCHAÎNE les écrans comme un doigt, sans jamais recharger, deux tours, deux thèmes ; après
 * chacun, l'écran porte ce qu'il DOIT porter — ses éléments, son canevas PEINT — et rien d'un autre écran). Ce que chaque écran doit porter,
 * c'est lui-même ouvert sur une page fraîche : ses mots, ses nœuds, ses canevas peints (≥ 200 échantillons opaques, comme le juge) ; tout ce
 * qui manque, tout nœud d'un autre écran, fait échouer. Le thème se change dans l'app (le magasin), comme aux Réglages. Les listes en dur du
 * juge (fiche, page +, Index, Fil, Cercle, l'instant) : chacune s'étend à son lot par ECRANS_PORTES.
 */
test("un écran n'est jamais vide : les écrans portés enchaînés sans recharger, deux tours, deux thèmes (redteam_vide)", async ({
  browser,
}) => {
  const ref = await references(browser, THEMES);
  const E = await ouvrirEcran(browser, ECRANS_PORTES[0]!, { theme: 'sombre' });
  const pg = E.page;
  if (sonde('vide-reste'))
    await pg.evaluate(() => {
      const ch = document.getElementById('accChoix')!;
      let ouvert = false;
      new MutationObserver(() => {
        if (ch.classList.contains('ouvert')) ouvert = true;
        else if (ouvert) document.getElementById('studioBtn')!.style.setProperty('display', 'none', 'important');
      }).observe(ch, { attributes: true });
    });
  const fautes: string[] = [];
  for (const tour of [1, 2])
    for (const theme of THEMES) {
      await pg.evaluate((t) => {
        (window as unknown as { __promi: { magasin: { choisirTheme(t: string): void } } }).__promi.magasin.choisirTheme(
          t,
        );
      }, theme);
      await pg.waitForTimeout(500);
      for (const ecran of ECRANS_PORTES) {
        expect(await retourAccueil(pg), "retour à l'accueil").toBe(true);
        await ecran.ouvrir(pg);
        await pg.waitForTimeout(1000);
        const e = (await pg.evaluate(EMPREINTE)) as Empreinte;
        for (const f of comparerEmpreintes(ref[`${theme} · ${ecran.nom}`]!, e))
          fautes.push(`tour ${String(tour)}, ${theme}, ${ecran.nom} : ${f}`);
      }
    }
  await E.fermer();
  expect(E.erreurs, 'aucune erreur JS').toEqual([]);
  expect(fautes).toEqual([]);
});

/**
 * redteam_enchaine (« LE CONTRÔLE QUI ENCHAÎNE » : on enchaîne deux écrans, et on compare le second à LUI-MÊME ouvert proprement : mêmes
 * classes, rien en trop, rien de perdu). Tous les couples d'écrans portés (le second ouvert après le retour à l'accueil, comme le doigt).
 * Les couples du juge (page + → page +, fiche → fiche, Index → fiche, Fil → fiche…) : s'étendent aux lots 2 à 4 par ECRANS_PORTES.
 */
test('enchaîner deux écrans : le second est lui-même — mêmes classes, rien en trop, rien de perdu (redteam_enchaine)', async ({
  browser,
}) => {
  const ref = await references(browser, ['sombre']);
  const fautes: string[] = [];
  for (const a of ECRANS_PORTES)
    for (const b of ECRANS_PORTES) {
      const E = await ouvrirEcran(browser, a, { theme: 'sombre' });
      if (sonde('enchaine-classe'))
        await E.page.evaluate(() => {
          const ch = document.getElementById('accChoix')!;
          new MutationObserver(() => {
            if (!ch.classList.contains('ouvert')) document.getElementById('accBarre')!.classList.add('pp-ouvert');
          }).observe(ch, { attributes: true });
        });
      await E.page.waitForTimeout(400);
      expect(await retourAccueil(E.page), "retour à l'accueil").toBe(true);
      await b.ouvrir(E.page);
      await E.page.waitForTimeout(1000);
      const e = (await E.page.evaluate(EMPREINTE)) as Empreinte;
      for (const f of comparerEmpreintes(ref[`sombre · ${b.nom}`]!, e)) fautes.push(`${a.nom} → ${b.nom} : ${f}`);
      expect(E.erreurs).toEqual([]);
      await E.fermer();
    }
  expect(fautes).toEqual([]);
});

// ────────────────────────────────────────────────────────────────── redteam_app ──

/**
 * redteam_app (v202a, Tom, C-276 : « LA RED TEAM DE TOUTE L'APP, SANS INDULGENCE ») — sur chaque écran porté, deux thèmes, trois vues (l'échelle
 * 1 : 390 × 844 ; la fenêtre de Safari, 0,79 : 330 × 714 ; la fenêtre de Tom : 390 × 651) : E aucune erreur JavaScript ; D aucun texte visible
 * qui sort de l'écran (au-delà de 1 pt) ; C aucun texte coupé par une boîte qui rogne sans « … » voulu ; R aucun recouvrement de deux textes
 * visibles (plus de 30 % de la plus petite encre), hors d'un même mot. Le juge était un relevé jugé à l'œil (RED-TEAM.md) : ici la cible est
 * zéro, et un recouvrement VOULU s'écrit nommément dans RECOUVREMENTS_VOULUS (aucun sur l'accueil).
 * D excuse un texte d'une rangée qui DÉFILE et le déclare (`data-glisse`, C-196 : le rail du pinceau de la page +) : il sort de l'écran
 * par construction, on l'atteint en glissant (la même exception que joignable et redteam_ecrans).
 */
const RECOUVREMENTS_VOULUS: string[] = [];
/**
 * LES COUPES DU PROTOTYPE, reprises à l'identique (le contrat visuel exige ses propriétés) — nommées, une à une : la boîte de police d'un prénom
 * sous un Noyau de la fiche dépasse de 2 à 3 pt le bas de la rangée qui défile (`#dAura`, 103 pt de haut, `overflow: auto hidden`) ; son ENCRE,
 * elle, est entière (le prototype a la même rangée, au pixel : fiche.spec). [élément, conteneur qui rogne]
 */
const COUPES_DU_PROTOTYPE: Array<[RegExp, RegExp]> = [[/^dAura › (div\.kr-n|span\.nom-lien)/, /^div#dAura$/]];
const RELEVE_APP = `(() => { const W = innerWidth, H = innerHeight, out = { D: [], C: [], R: [] };
  const vis = (e) => { for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const s = getComputedStyle(x); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity < 0.05) return false; } return true; };
  const nom = (e) => { let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id; else if (e.className && typeof e.className === 'string') s += '.' + e.className.trim().split(/\\s+/).slice(0, 2).join('.'); const p = e.closest('[id]'); return (p && p !== e ? p.id + ' › ' : '') + s; };
  const T = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let t;
  while ((t = w.nextNode())) { const v = t.nodeValue.trim(); if (!v) continue; const e = t.parentElement; if (!e) continue;
    const rg = document.createRange(); rg.selectNodeContents(t); const rs = [...rg.getClientRects()].filter((q) => q.width > 1 && q.height > 1); if (!rs.length) continue;
    const r = rg.getBoundingClientRect(); if (r.bottom < 0 || r.top > H || r.right < 0 || r.left > W) continue;
    const hit = document.elementFromPoint(Math.min(W - 1, Math.max(1, r.left + r.width / 2)), Math.min(H - 1, Math.max(1, r.top + r.height / 2)));
    if (!hit || !(hit === e || e.contains(hit) || hit.contains(e))) continue;
    if (!vis(e)) continue; const it = { e, v: v.slice(0, 40), r, rs }; T.push(it);
    if ((r.left < -1 || r.right > W + 1 || r.top < -1 || r.bottom > H + 1) && !e.closest('[data-glisse]')) out.D.push([nom(e), it.v, Math.round(r.left), Math.round(r.right), Math.round(r.top)]);
    for (let x = e; x && x !== document.body; x = x.parentElement) { const s = getComputedStyle(x); if ((s.overflow + s.overflowX + s.overflowY).indexOf('hidden') < 0) continue; const xr = x.getBoundingClientRect();
      if (r.right > xr.right + 2 || r.left < xr.left - 2 || r.bottom > xr.bottom + 2 || r.top < xr.top - 2) { if (!/…$/.test(v) && s.textOverflow !== 'ellipsis') out.C.push([nom(e), it.v, nom(x)]); }
      break; } }
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) { const a = T[i], b = T[j]; if (a.e === b.e || a.e.contains(b.e) || b.e.contains(a.e)) continue;
    let inter = 0; for (const p of a.rs) for (const q of b.rs) { const w2 = Math.min(p.right, q.right) - Math.max(p.left, q.left), h2 = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top); if (w2 > 0 && h2 > 0) inter += w2 * h2; }
    if (!inter) continue; const sa = a.rs.reduce((s, q) => s + q.width * q.height, 0), sb = b.rs.reduce((s, q) => s + q.width * q.height, 0);
    if (inter > 0.3 * Math.min(sa, sb)) out.R.push([nom(a.e), a.v, nom(b.e), b.v, Math.round((100 * inter) / Math.min(sa, sb))]); }
  out.n = T.length; return out; })()`;

for (const [vnom, vue] of [
  ['échelle 1, 390 × 844', REF],
  ['échelle 0,79, 330 × 714', { width: 330, height: 714 }],
  ['la fenêtre de Tom, 390 × 651', { width: 390, height: 651 }],
] as const)
  test(`la red team de l'app : aucune erreur, rien qui sort, rien de coupé, rien qui se recouvre — ${vnom} (redteam_app, C-276)`, async ({
    browser,
  }) => {
    const fautes: string[] = [];
    let n = 0;
    for (const ecran of ECRANS_PORTES)
      for (const theme of THEMES) {
        const E = await ouvrirEcran(browser, ecran, { theme, vue });
        if (sonde('app-recouvre'))
          await E.page.addStyleTag({ content: '#device #studioBtn .l{transform:translate(24px,0)!important}' });
        if (sonde('app-erreur'))
          await E.page.evaluate(() => {
            setTimeout(() => {
              throw new Error('sonde : une erreur de la page');
            }, 0);
          });
        await E.page.waitForTimeout(300);
        const r = (await E.page.evaluate(RELEVE_APP)) as { D: unknown[][]; C: unknown[][]; R: unknown[][]; n: number };
        n += r.n;
        const ou = `${ecran.nom}, ${theme}`;
        for (const e of E.erreurs) fautes.push(`${ou} : E ${e.slice(0, 160)}`);
        for (const d of r.D) fautes.push(`${ou} : D ${JSON.stringify(d)}`);
        for (const c of r.C)
          if (!COUPES_DU_PROTOTYPE.some(([e, x]) => e.test(String(c[0])) && x.test(String(c[2]))))
            fautes.push(`${ou} : C ${JSON.stringify(c)}`);
        for (const x of r.R) {
          const s = JSON.stringify(x);
          if (!RECOUVREMENTS_VOULUS.some((v) => s.includes(v))) fautes.push(`${ou} : R ${s}`);
        }
        await E.fermer();
      }
    expect(n, 'des textes relevés').toBeGreaterThan(10);
    expect(fautes).toEqual([]);
  });

// ──────────────────────────────────────────────────────────── redteam_fonctions ──

/**
 * redteam_fonctions (« L'INVENTAIRE DES FONCTIONS : aucune refonte, aucun portage n'a le droit de faire disparaître une de ces lignes. Chaque
 * ligne dit : le geste, et ce qui doit en résulter DANS LA DONNÉE »). Les lignes du lot 1, en dur, au doigt (le vrai toucher), et leur
 * résultat lu dans la donnée de l'app (le journal de la navigation, le magasin) — la porte du mot PROMI (C-316 : « en gratuit, toucher le mot
 * PROMI de l'accueil ouvre Ma Parole ! »), Partager, Réglages, les quatre entrées de la barre (« les écrans du dock », C-106), le + et ses
 * trois natures (« le + ouvre la page de création »), « Garder ta Toile » (v52). Toucher une dalle → sa fiche, déplacer une dalle → sa place,
 * « Plus tard » → noté : accueil.spec. Les lignes du juge qui exigent un écran destinataire (planter au geste, tenir au geste, le Fil, chercher
 * et trier, Peaufiner, « l'écran s'ouvre ») : s'étendent aux lots 2, 3a, 3b, 4, 8 ; le membre de Ma Parole ! (PROMI ne fait rien) : lot 8.
 */
const INVENTAIRE: Array<{ geste: string; sel: string; vers: string; arg?: string; avant?: string }> = [
  { geste: 'toucher le mot PROMI', sel: '#accPlat .acc-mm', vers: 'offre' },
  { geste: 'toucher Partager', sel: '#shareBtn', vers: 'partager' },
  { geste: 'toucher Réglages', sel: '#settingsBtn', vers: 'reglages' },
  { geste: 'toucher STUDIO', sel: '#studioBtn', vers: 'studio' },
  { geste: 'toucher AURA', sel: '#souffleBtn', vers: 'aura' },
  { geste: 'toucher INDEX', sel: '#indexBtn', vers: 'index' },
  { geste: 'toucher FIL', sel: '#filBtn', vers: 'fil' },
  {
    geste: 'le +, puis « Un Cercle »',
    sel: '#accChoix .acc-pil[data-k="nuee"]',
    vers: 'pagePlus',
    arg: 'nuee',
    avant: '#createBtn',
  },
  {
    geste: 'le +, puis « Un Chiche »',
    sel: '#accChoix .acc-pil[data-k="chiche"]',
    vers: 'pagePlus',
    arg: 'chiche',
    avant: '#createBtn',
  },
  {
    geste: 'le +, puis « Un Promi »',
    sel: '#accChoix .acc-pil[data-k="promi"]',
    vers: 'pagePlus',
    arg: 'promi',
    avant: '#createBtn',
  },
  { geste: '« Garder ta Toile »', sel: '#accRappel [data-r="oui"]', vers: 'compte' },
];

async function toucher(page: Page, sel: string): Promise<boolean> {
  const r = (await page.evaluate((s) => {
    const e = document.querySelector(s);
    if (!e) return null;
    if (e.closest('[data-glisse]')) e.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    const b = e.getBoundingClientRect();
    if (b.width < 4 || b.height < 4) return null;
    const x = b.left + b.width / 2;
    const y = b.top + b.height / 2;
    const h = document.elementFromPoint(x, y);
    return h && (h === e || e.contains(h)) ? [x, y] : null;
  }, sel)) as [number, number] | null;
  if (!r) return false;
  await page.mouse.click(r[0], r[1]);
  await page.waitForTimeout(150);
  return true;
}

test("l'inventaire des fonctions de l'accueil : chaque geste a son résultat dans la donnée (redteam_fonctions)", async ({
  browser,
}) => {
  // un état où le bandeau « Garder ta Toile » est dû (après le troisième Promi : accueil.spec, C-200 ①)
  const ls: Record<string, string> = {
    ...stockage(),
    promi_onb: '1',
    promi_compte: '',
    promi_rappel_n: '',
    promi_rappel_non: '',
    promi_rappel_fin: '',
    promi_rappel_vu: '',
  };
  const E = await ouvrirEcran(browser, ECRANS_PORTES[0]!, { ls });
  const pg = E.page;
  if (sonde('fonction-perdue'))
    await pg.evaluate(() => {
      for (const t of ['pointerdown', 'pointerup', 'click'])
        window.addEventListener(
          t,
          (ev) => {
            if ((ev.target as Element | null)?.closest('#shareBtn')) ev.stopImmediatePropagation();
          },
          true,
        );
    });
  const fautes: string[] = [];
  for (const f of INVENTAIRE) {
    if (f.avant && !(await toucher(pg, f.avant))) fautes.push(`${f.geste} : ${f.avant} n'est pas touchable`);
    await pg.waitForTimeout(200);
    const n0 = (await pg.evaluate(`${P_}.nav.journal().length`)) as number;
    const a0 = JSON.stringify(await pg.evaluate(`${P_}.magasin.etat().autres`));
    if (!(await toucher(pg, f.sel))) {
      fautes.push(`${f.geste} : ${f.sel} absent, ou pas touchable au doigt`);
      continue;
    }
    await pg.waitForTimeout(150);
    const j = ((await pg.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string; arg?: string }>).slice(n0);
    const voulu = f.arg ? { vers: f.vers, arg: f.arg } : { vers: f.vers };
    if (j.length !== 1 || j[0]!.vers !== voulu.vers || (f.arg && j[0]!.arg !== f.arg))
      fautes.push(`${f.geste} : la navigation a reçu ${JSON.stringify(j)} au lieu de ${JSON.stringify(voulu)}`);
    // lot 2a : une pilule OUVRE la page + (elle couvre l'accueil) — son X la referme avant le geste suivant
    if (f.vers === 'pagePlus') await refermerPagePlus(pg);
    // lot 4 : INDEX ouvre l'Index, FIL le Fil (ils couvrent l'accueil) — refermés avant le geste suivant
    if (f.vers === 'index' || f.vers === 'fil') await fermerIndex(pg);
    if (f.vers === 'compte') {
      const a1 = (await pg.evaluate(`${P_}.magasin.etat().autres`)) as Record<string, string>;
      if (a1['promi_rappel_n'] !== String((+(JSON.parse(a0) as Record<string, string>)['promi_rappel_n']! || 0) + 1))
        fautes.push(`${f.geste} : la réponse n'est pas notée (promi_rappel_n ${String(a1['promi_rappel_n'])})`);
    }
  }
  await E.fermer();
  expect(E.erreurs).toEqual([]);
  expect(fautes).toEqual([]);
});

// ─────────────────────────────────────────────────────────────── redteam_champs ──

/**
 * redteam_champs (« LE CONTRÔLE QUI REMPLIT » : un champ est bon quand 1 il est ATTEIGNABLE — visible, non nul, dans le cadre ; 2 il ACCEPTE le
 * texte ; 3 la DONNÉE le reçoit ; 4 l'ÉCRAN le montre). Sur chaque écran porté, chaque champ de saisie à l'écran est rempli au clavier ; la
 * donnée est le magasin (l'état unique). L'accueil n'en porte aucun : le test mord dès la page + (lot 2 : la phrase, le nom d'un Cercle),
 * la fiche (lot 3a : le titre ; 3b : « Un mot… »), l'Index et le Fil (lot 4 : la recherche) — sans qu'on le touche.
 */
test("le contrôle qui remplit : chaque champ des écrans portés est atteignable, accepte, la donnée le reçoit, l'écran le montre (redteam_champs)", async ({
  browser,
}) => {
  const fautes: string[] = [];
  for (const ecran of ECRANS_PORTES) {
    const E = await ouvrirEcran(browser, ecran);
    const pg = E.page;
    if (sonde('champ-sourd'))
      await pg.evaluate(() => {
        const i = document.createElement('input');
        i.type = 'text';
        i.style.cssText = 'position:absolute;left:40px;top:300px;width:200px;height:40px;z-index:99';
        document.getElementById('device')!.appendChild(i);
      });
    const champs = (await pg.evaluate(() => {
      const out: Array<{ i: number; ok: boolean; quoi: string }> = [];
      const L = document.querySelectorAll<HTMLElement>(
        'input:not([type=hidden]):not([type=file]):not([type=checkbox]):not([type=radio]), textarea, [contenteditable=""], [contenteditable="true"]',
      );
      L.forEach((e, i) => {
        const c = getComputedStyle(e);
        // un champ d'un écran fermé (un ancêtre en display:none — la page + avant le lot 2b) n'est pas à l'écran : aucune boîte rendue
        if (c.display === 'none' || e.getClientRects().length === 0) return;
        e.setAttribute('data-champ', String(i));
        // un champ caché qui DÉCLARE sa porte (`data-porte` : la phrase de la page + est la saisie, C-004) s'atteint par elle : c'est la
        // porte qui doit être visible et prise au doigt
        const porte = e.getAttribute('data-porte')
          ? document.querySelector<HTMLElement>(e.getAttribute('data-porte')!)
          : null;
        if (porte) porte.setAttribute('data-porte-de', String(i));
        // (la porte est une pastille qui peut passer à la ligne : on vise sa première ligne)
        const r = porte ? porte.getClientRects()[0]! : e.getBoundingClientRect();
        const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        out.push({
          i,
          ok:
            c.visibility !== 'hidden' &&
            r.width >= 4 &&
            r.height >= 4 &&
            r.left >= 0 &&
            r.right <= innerWidth &&
            r.top >= 0 &&
            r.bottom <= innerHeight &&
            !!h &&
            (h === (porte ?? e) || (porte ?? e).contains(h)),
          quoi: (e.id ? '#' + e.id : e.tagName.toLowerCase()) + ' ' + Math.round(r.width) + '×' + Math.round(r.height),
        });
      });
      return out;
    })) as Array<{ i: number; ok: boolean; quoi: string }>;
    for (const ch of champs) {
      const q = `${ecran.nom} · ${ch.quoi}`;
      if (!ch.ok) {
        fautes.push(`${q} : 1 · pas atteignable`);
        continue;
      }
      const sel = `[data-champ="${String(ch.i)}"]`;
      const avant = JSON.stringify(await pg.evaluate(`${P_}.magasin.etat()`));
      const v0 = (await pg.evaluate((s) => {
        const e = document.querySelector<HTMLInputElement>(s)!;
        return 'value' in e ? e.value : (e as HTMLElement).textContent;
      }, sel)) as string;
      const porte = await pg.$(`[data-porte-de="${String(ch.i)}"]`);
      if (porte) await porte.click();
      else await pg.click(sel);
      await pg.keyboard.type(' essai', { delay: 20 });
      const v1 = (await pg.evaluate((s) => {
        const e = document.querySelector<HTMLInputElement>(s)!;
        return 'value' in e ? e.value : (e as HTMLElement).textContent;
      }, sel)) as string;
      if (v1 === v0) fautes.push(`${q} : 2 · il n'accepte pas le texte`);
      await pg.keyboard.press('Enter');
      await pg.waitForTimeout(600);
      // la donnée : le magasin — ou, pour la phrase de la page +, l'état de la page (la parole en cours lui appartient jusqu'à ce
      // qu'elle soit plantée, lot 2b ; page-plus.ts : « l'état de la page n'appartient qu'à elle »)
      const apres = JSON.stringify(await pg.evaluate(`${P_}.magasin.etat()`));
      const enCours = JSON.stringify(
        await pg.evaluate(
          `(() => { const p = ${P_}.pagePlus && ${P_}.pagePlus(); return p && p.ouverte() ? p.etat().phrase : null; })()`,
        ),
      );
      if (apres === avant && !apres.includes('essai') && !enCours.includes('essai'))
        fautes.push(`${q} : 3 · la donnée ne le reçoit pas`);
      const montre = (await pg.evaluate(() => {
        const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let t: Node | null;
        while ((t = w.nextNode())) if ((t.nodeValue ?? '').includes('essai')) return true;
        return [...document.querySelectorAll<HTMLInputElement>('input, textarea')].some(
          (e) => e.value.includes('essai') && e.getBoundingClientRect().width > 4,
        );
      })) as boolean;
      if (!montre) fautes.push(`${q} : 4 · l'écran ne le montre pas`);
    }
    await E.fermer();
  }
  expect(fautes).toEqual([]);
});

// ──────────────────────────────────────────────────────────── redteam_pastilles ──

/**
 * redteam_pastilles (« LE CONTRÔLE QUI TOUCHE » : une pastille est bonne quand 1 elle est ATTEIGNABLE — visible, non nulle, dans le cadre,
 * le doigt la prend — et 2 elle a un EFFET : l'état de l'app n'est plus le même après). Sur chaque écran porté : chaque commande à l'écran
 * (`role="button"`, `button`, les rôles de choix, `.chip`) est touchée au doigt ; l'effet se lit sur l'écran (ses mots, ses classes), la
 * donnée (le magasin) ou la navigation (une demande d'écran : au lot 1 aucun écran destinataire n'existe, la demande EST l'effet).
 * Les réglages de Peaufiner (un à un) et la phrase de la page + : s'étendent aux lots 2 et 3b par ECRANS_PORTES.
 */
const COMMANDES =
  '[role="button"], button, [role="tab"], [role="switch"], [role="checkbox"], [role="radio"], [role="option"], .chip';
const SIGNATURE = `(() => { const W = innerWidth, H = innerHeight; const mots = [], cls = [];
  for (const e of document.querySelectorAll('body *')) { const c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.3) continue; const r = e.getBoundingClientRect();
    if (r.width < 4 || r.height < 4 || r.bottom < 0 || r.top > H) continue;
    if (e.id) cls.push(e.id + ':' + [...e.classList].sort().join('.'));
    let t = ''; e.childNodes.forEach((x) => { if (x.nodeType === 3) t += x.nodeValue; }); if (t.trim()) mots.push(Math.round(r.top) + ':' + t.trim().slice(0, 24)); }
  for (const e of document.querySelectorAll('[data-cmd]')) cls.push('cmd' + e.getAttribute('data-cmd') + ':' + [...e.classList].sort().join('.') + ':' + (e.getAttribute('aria-pressed') || ''));
  return mots.sort().join('|') + '##' + cls.sort().join('|') + '##' + ${P_}.nav.journal().length + '##' + JSON.stringify(${P_}.magasin.etat()); })()`;

test('le contrôle qui touche : chaque commande des écrans portés est atteignable au doigt et a un effet (redteam_pastilles)', async ({
  browser,
}) => {
  const fautes: string[] = [];
  let touchees = 0;
  for (const ecran of ECRANS_PORTES) {
    let E = await ouvrirEcran(browser, ecran);
    const sondeMorte = async (pg: Page): Promise<void> => {
      if (sonde('pastille-morte'))
        await pg.evaluate(() => {
          for (const t of ['pointerdown', 'pointerup', 'click'])
            window.addEventListener(
              t,
              (ev) => {
                if ((ev.target as Element | null)?.closest('#indexBtn')) ev.stopImmediatePropagation();
              },
              true,
            );
        });
    };
    await sondeMorte(E.page);
    const liste = (await E.page.evaluate((sel) => {
      const out: Array<{ cle: string; quoi: string; ok: boolean }> = [];
      document.querySelectorAll<HTMLElement>(sel).forEach((e, i) => {
        const c = getComputedStyle(e);
        let v = true;
        for (let x: HTMLElement | null = e; x; x = x.parentElement) {
          const k = getComputedStyle(x);
          if (k.display === 'none' || k.visibility === 'hidden' || +k.opacity < 0.3) v = false;
        }
        // une rangée qui DÉFILE et le déclare (`data-glisse`, C-196 : le rail du pinceau) : ce qui est hors de sa vue s'atteint en glissant
        if (e.closest('[data-glisse]')) e.scrollIntoView({ block: 'nearest', inline: 'nearest' });
        const r = e.getBoundingClientRect();
        if (!v || r.width < 1 || r.bottom < 0 || r.top > innerHeight) return;
        const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        out.push({
          cle: e.id ? '#' + e.id : `${sel.split(',')[0]!}:nth(${String(i)})`,
          quoi:
            (e.id ? '#' + e.id : e.tagName.toLowerCase()) +
            ' « ' +
            (e.getAttribute('aria-label') ?? e.textContent ?? '').trim().slice(0, 20) +
            ' »',
          ok:
            c.pointerEvents !== 'none' &&
            r.width >= 6 &&
            r.height >= 6 &&
            r.left >= -1 &&
            r.right <= innerWidth + 1 &&
            !!h &&
            (h === e || e.contains(h)),
        });
        e.setAttribute('data-cmd', String(i));
      });
      return out.map((o, k) => ({ ...o, i: k }));
    }, COMMANDES)) as Array<{ cle: string; quoi: string; ok: boolean; i: number }>;
    const sels = (await E.page.evaluate(() =>
      [...document.querySelectorAll('[data-cmd]')].map((e) => e.getAttribute('data-cmd')),
    )) as string[];
    for (const [k, c] of liste.entries()) {
      const q = `${ecran.nom} · ${c.quoi}`;
      if (!c.ok) {
        fautes.push(`${q} : 1 · pas atteignable au doigt`);
        continue;
      }
      const sel = `[data-cmd="${sels[k]!}"]`;
      const av = (await E.page.evaluate(SIGNATURE)) as string;
      // un choix DÉJÀ FAIT (aria-pressed) ou une commande INACTIVE (aria-disabled : « garder de côté » tant que rien n'a changé, C-149) n'a rien
      // à changer ; un MUR de Ma Parole ! (le pinceau payant, C-196) a pour effet sa phrase de
      // mur, qui vient au lot 8 (PLAN-APP) — exception nommée, retirée au lot 8
      const sans = (await E.page.evaluate((s) => {
        const e = document.querySelector(s);
        return (
          !!e &&
          (e.getAttribute('aria-pressed') === 'true' ||
            e.getAttribute('aria-disabled') === 'true' ||
            e.classList.contains('pc-mur'))
        );
      }, sel)) as boolean;
      if (!(await toucher(E.page, sel))) {
        fautes.push(`${q} : 1 · le doigt ne la prend pas`);
        continue;
      }
      // l'effet est attendu jusqu'à 3 s (un passage en flaques de 300 ms dure plusieurs images de 0,7 s hors du Mac : le menu du + qui se
      // referme n'a changé l'écran qu'à la fin de son passage) — la règle ne change pas : aucun effet en 3 s, c'est une faute
      let ap = av;
      for (let t = 0; t < 3000 && ap === av; t += 150) {
        await E.page.waitForTimeout(150);
        ap = (await E.page.evaluate(SIGNATURE)) as string;
      }
      await E.page.waitForFunction(
        () => !document.querySelector('[data-flaques-mode], #createSheet.pp-entre'),
        undefined,
        {
          timeout: 20000,
        },
      );
      // l'écran d'arrivée, relu une fois tout mouvement fini : c'est lui qui décide si l'on repart d'un écran neuf
      if (ap !== av) ap = (await E.page.evaluate(SIGNATURE)) as string;
      touchees++;
      if (ap === av && !sans) fautes.push(`${q} : 2 · aucun effet`);
      // l'écran a changé : on repart d'un écran neuf (les commandes sont rendues dans le même ordre)
      if (
        ap.split('##').slice(0, 2).join() !== av.split('##').slice(0, 2).join() ||
        ap.split('##')[3] !== av.split('##')[3]
      ) {
        await E.fermer();
        E = await ouvrirEcran(browser, ecran);
        await sondeMorte(E.page);
        await E.page.evaluate((sel) => {
          document.querySelectorAll(sel).forEach((e, i) => e.setAttribute('data-cmd', String(i)));
        }, COMMANDES);
      }
    }
    await E.fermer();
  }
  expect(touchees, 'des commandes touchées').toBeGreaterThan(8);
  expect(fautes).toEqual([]);
});

// ──────────────────────────────────────────────────────────────── redteam_secs2 ──

/**
 * redteam_secs2 (v202a, Tom, C-271 : « AUCUN CHANGEMENT SEC À L'ÉCRAN, NULLE PART […] Rien n'apparaît ni ne disparaît d'une image à l'autre »)
 * — son instrument porté : chaque image relevée APRÈS la peinture (une tâche postée depuis l'image, `MessageChannel`), et le verdict « jamais de
 * 0 à 1 d'un coup : ≥ 3 images entre les deux ». La seule apparition du lot 1 est le symbole « recadrer » (C-188 : il naît en flaques, 300 ms,
 * et part en flaques) : le canevas du passage se couvre (ou se vide) sur ≥ 3 images, et le symbole n'est jamais net avant. Le juge disait
 * « une image de plus de 80 ms : non jugé » ; ici l'horloge est PILOTÉE (une image = 1/60 s, quelle que soit la machine) : jugé partout, la CI
 * comprise — la durée en millisecondes réelles, elle, n'est pas jugée (accueil.spec : la classe ; Tom sur l'iPhone : l'œil).
 * Les contrats A à G du juge s'étendent : A « Les Mots » (lot 3b), B C la pastille « pas encore vu » d'une carte (lot 4), D une valeur des
 * Réglages et E le toast (lot 8), F « à qui ? » et G le titre effacé (lot 2). ⚠ Restent secs, IDENTIQUES AU PROTOTYPE (validés avant C-271) :
 * le menu du + (C-142, « parfait : on fige »), le bandeau « Garder ta Toile », la pastille du Fil — à trancher par Tom.
 */
const ETAT_RECADRE = `() => { const e = document.getElementById('accRecadre'); if (!e || getComputedStyle(e).display === 'none') return 'absent';
  const s = e.querySelector('svg'); const net = !!s && getComputedStyle(s).visibility !== 'hidden';
  const cv = [...e.querySelectorAll('canvas.passage-flaques')].find((c) => getComputedStyle(c).display !== 'none');
  let n = -1; if (cv) { n = 0; const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data; for (let i = 3; i < d.length; i += 4) if (d[i] > 40) n++; }
  return (net ? 'net' : 'cache') + ':' + n; }`;
/** dans la page, image par image (l'horloge pilotée : une image = 1/60 s, quelle que soit la machine) : l'état du symbole après chaque image */
const PAS_A_PAS = `(a) => { const [f, fin, max] = a; const p = window.__promi; const lit = new Function('return (' + f + ')')();
  const arret = new Function('p', 's', 'return (' + fin + ')'); const L = [];
  for (let i = 0; i < max; i++) { p.horloge.images(1); const s = lit(); L.push(s); if (arret(p, s)) break; }
  for (let i = 0; i < 6; i++) { p.horloge.images(1); L.push(lit()); } return L; }`;

test("aucun changement sec : le symbole « recadrer » naît et part en flaques, jamais de 0 à 1 d'une image à l'autre (redteam_secs2, C-271)", async ({
  browser,
}) => {
  const ctx = await browser.newContext({ viewport: REF, deviceScaleFactor: 2 });
  const pg = await ctx.newPage();
  const erreurs: string[] = [];
  pg.on('pageerror', (e) => erreurs.push(String(e)));
  await pg.goto(`http://127.0.0.1:5180/?banc=1&pilote=${String(T_FIGE)}`);
  await pg.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await pg.evaluate(async (ls) => {
    const p = (window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } })
      .__promi;
    p.magasin.importer({ ls });
    await p.demarrer();
  }, stockage());
  await pg.evaluate(`${P_}.horloge.images(120)`);
  if (sonde('secs-recadre'))
    await pg.addStyleTag({
      content:
        '#accRecadre canvas.passage-flaques{display:none!important} #accRecadre.cache svg{visibility:visible!important}',
    });
  // il naît : la main bouge la vue (le moteur lit le doigt ; les images de l'horloge font le reste) — son état relevé dès la PREMIÈRE image du geste
  // (sur une machine lente, la naissance commençait pendant le geste et ses premières images n'étaient pas relevées : CI du 23 nov.)
  await pg.mouse.move(195, 420);
  await pg.mouse.down();
  const pendant: string[] = [];
  for (let k = 1; k <= 10; k++) {
    await pg.mouse.move(195 - 5.5 * k, 420 - 4 * k);
    pendant.push((await pg.evaluate(`(() => { ${P_}.horloge.images(1); return (${ETAT_RECADRE})(); })()`)) as string);
  }
  await pg.mouse.up();
  const nait = [
    ...pendant,
    ...((await pg.evaluate(
      `(${PAS_A_PAS})(${JSON.stringify([ETAT_RECADRE, "p.accueil().etatRecadre().etat === 'la'", 600])})`,
    )) as string[]),
  ];
  // il part : 4 s sans toucher, comptées depuis le dernier mouvement de la vue (elle revient seule dans ses bornes)
  const part = (await pg.evaluate(
    `(${PAS_A_PAS})(${JSON.stringify([ETAT_RECADRE, "p.accueil().etatRecadre().etat === 'absent'", 4000])})`,
  )) as string[];
  await ctx.close();
  const partiels = (L: string[]): number => {
    const n = L.map((x) => (x === 'absent' ? -1 : +x.split(':')[1]!));
    const max = Math.max(1, ...n);
    return L.filter((x, i) => x.startsWith('cache') && n[i]! > 0.02 * max && n[i]! < 0.95 * max).length;
  };
  const resume = (L: string[]): string => L.join(' ').slice(0, 400);
  const premier = nait.find((x) => x !== 'absent') ?? '';
  expect(erreurs).toEqual([]);
  expect(premier.startsWith('net'), `il ne paraît jamais net d'emblée : ${resume(nait)}`).toBe(false);
  expect(
    partiels(nait),
    `il naît en flaques : ≥ 3 images couvertes en partie (${resume(nait)})`,
  ).toBeGreaterThanOrEqual(3);
  expect(nait.at(-1)!.startsWith('net'), 'puis il est net').toBe(true);
  expect(
    partiels(part),
    `il part en flaques : ≥ 3 images vidées en partie (${resume(part.slice(-60))})`,
  ).toBeGreaterThanOrEqual(3);
  expect(part.at(-1), 'puis il est absent').toBe('absent');
});
