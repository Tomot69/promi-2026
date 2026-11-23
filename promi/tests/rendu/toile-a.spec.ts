/**
 * LOT 1 — LA TOILE VIVANTE, GROUPE A (C-326) : les juges du prototype redteam_rythme, redteam_vivant, redteam_retour, redteam_zoom,
 * redteam_toile_stable, redteam_toile_vide, redteam_ritournelle, redteam_ramage_onde, portés sur la VRAIE APP.
 *
 * LE TEMPS EST PILOTÉ (`?pilote=` : l'horloge unique en mode piloté, +1000/60 ms par image ; tous les minuteurs et toutes les images de la
 * page passent par elle, le moteur repris compris). Une durée du moteur se lit donc à l'horloge de la page, image par image, la même sur le
 * Mac et sur l'intégration continue (WebKit sans carte graphique, une image toutes les 0,7 s en temps réel) : ce qu'elle mesure ne dépend
 * pas de la machine. Le hasard est amorcé (comme banc_rendu) : un passage est reproductible. Les CADENCES (ce que dure une image en temps
 * réel) ne sont pas jugées ici — elles appartiennent au relevé de l'iPhone (`?releve=1`) et à redteam_evol / redteam_pleine.
 *
 * Les mondes : un échantillon nommé sur l'intégration continue et, pour les juges longs, sur le Mac ; tous, et les durées du juge d'origine
 * (3 min de repos par monde, cent mouvements, cinq tailles de Toile), avec PROMI_COMPLET=1.
 */
import { test, expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { sonde, ETAT, fermerFiche } from './aides.ts';

const ICI = import.meta.dirname;
const RACINE = join(ICI, '..', '..', '..');
const COMPLET = process.env['PROMI_COMPLET'] === '1';
const CI = !!process.env['CI'];
const T0 = 123456;

function lireEtat(f: string): Record<string, string> {
  const x = JSON.parse(readFileSync(f, 'utf8')) as { ls?: Record<string, string> } & Record<string, unknown>;
  const ls: Record<string, string> = {};
  for (const [k, v] of Object.entries(x.ls ?? x)) if (k !== 'setItem' && typeof v === 'string') ls[k] = v;
  return ls;
}
/** le jeu de démonstration du prototype (celui que rend le banc de rendu) : la Toile sur laquelle les durées de v60 ont été relevées */
const DEMO = lireEtat(join(ICI, 'etat-banc-rendu.json'));
/** une Toile de n paroles relue de la sauvegarde (banc-etats/), l'onboarding fait, le bandeau « Garder ta Toile » déjà refusé */
const banc = (n: number): Record<string, string> => ({
  ...lireEtat(join(RACINE, 'banc-etats', `etat-${String(n)}.json`)),
  promi_onb: '1',
  promi_rappel_n: '9',
});
const studio = (m: string): string => JSON.stringify({ m, p: 'signal', h: 0, libre: true, acquis: {} });
const MOTEUR = readFileSync(join(ICI, '..', '..', 'src', 'moteur', 'repris', 'promi-moteur.js'), 'utf8');

/**
 * La bibliothèque posée dans la page AVANT l'app : les minuteurs natifs (gardés avant que l'horloge prenne leur place), le hasard amorcé
 * (mulberry32), les pas d'horloge, et la Toile « posée » (redteam_toile_stable, POSE : la boucle du moteur arrêtée et la vue sur sa cible).
 */
const LIB = `(() => { const w = window; const st = w.setTimeout.bind(w);
  let a = (w.__graineTA >>> 0);
  Math.random = () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  w.__ta = {
    dors: (ms) => new Promise((f) => st(f, ms)),
    lcg(s) { Math.random = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; }; },
    async pas(n, reel) { for (let i = 0; i < n; i++) { w.__promi.horloge.images(1); if (reel != null) await w.__ta.dors(reel); } },
    async pose(max, reel) { let ok = 0; for (let i = 0; i < (max || 1500); i++) { w.__promi.horloge.images(1); if (reel != null) await w.__ta.dors(reel);
        const s = w.Toile_state(), l = w.Toile_lecture(), c = l.cible || l.vue;
        ok = (!s.running && Math.abs(c.s - l.vue.s) < 0.0005 && Math.abs(c.ox - l.vue.ox) < 0.3 && Math.abs(c.oy - l.vue.oy) < 0.3) ? ok + 1 : 0;
        if (ok >= 3) return i; } return -1; },
  }; })();`;

interface Ouverture {
  graine?: number;
  /** la vie au repos (coupée par défaut, comme banc_rendu) */
  vivant?: boolean;
  /** un script posé avant l'app (une sonde, un crochet du moteur) */
  avant?: string;
  /** ne pas importer : la vraie app relit ce qu'elle a enregistré (une réouverture) */
  relire?: boolean;
}

/** la vraie app, construite, horloge pilotée, démarrée sur l'état `ls` (ou relue de son stockage) ; l'accueil monté */
async function ouvrir(page: Page, ls: Record<string, string>, o: Ouverture = {}): Promise<void> {
  const avant = `window.__graineTA=${String(o.graine ?? 0x5eed2026)};${o.vivant ? '' : 'window._vivantOff=true;'}${o.avant ?? ''}`;
  await page.addInitScript({ content: avant + LIB });
  await page.goto(`http://127.0.0.1:5180/?banc=1&pilote=${String(T0)}`);
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await page.evaluate(
    async ([ls, relire]) => {
      const p = (
        window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } }
      ).__promi;
      if (!relire) p.magasin.importer({ ls });
      await p.demarrer();
    },
    [ls, !!o.relire] as const,
  );
}

async function poser(page: Page, max = 1500): Promise<number> {
  return (await page.evaluate(`window.__ta.pose(${String(max)})`)) as number;
}
async function pas(page: Page, n: number): Promise<void> {
  await page.evaluate(`window.__ta.pas(${String(n)})`);
}
async function choisirMonde(page: Page, m: string): Promise<void> {
  await page.evaluate((m) => {
    (window as unknown as { __promi: { magasin: { choisirMonde(m: string): void } } }).__promi.magasin.choisirMonde(m);
  }, m);
}

/** un geste au doigt sur la Toile, en événements de pointeur sur son canevas (le moteur les y écoute), une image d'horloge par pas */
async function geste(page: Page, doigts: Array<Array<[number, number]>>): Promise<void> {
  await page.evaluate(`(async (D) => { const cv = document.getElementById('toileCv'); const r = cv.getBoundingClientRect();
    const ev = (t, id, p) => cv.dispatchEvent(new PointerEvent(t, { pointerId: id, isPrimary: id === 1, pointerType: 'touch', bubbles: true, cancelable: true, clientX: r.left + p[0], clientY: r.top + p[1] }));
    const n = D[0].length;
    D.forEach((c, i) => { ev('pointerdown', i + 1, c[0]); });
    for (let k = 1; k < n; k++) { D.forEach((c, i) => ev('pointermove', i + 1, c[k])); window.__promi.horloge.images(1); }
    D.forEach((c, i) => ev('pointerup', i + 1, c[n - 1])); })(${JSON.stringify(doigts)})`);
}
/** deux doigts de part et d'autre de (195, 440), leur écart de d0 à d1 en 14 pas (redteam_zoom, `pince`) */
function pince(d0: number, d1: number): Array<Array<[number, number]>> {
  const a: Array<[number, number]> = [];
  const b: Array<[number, number]> = [];
  for (let i = 0; i <= 14; i++) {
    const d = d0 + ((d1 - d0) * i) / 14;
    a.push([195 - d / 2, 440]);
    b.push([195 + d / 2, 440]);
  }
  return [a, b];
}
/** le menu du + ouvert puis refermé par un toucher ailleurs (la seule « page » de l'accueil au lot 1) */
async function menuPlus(page: Page): Promise<void> {
  const r = (await page.evaluate(
    `(() => { const b = document.getElementById('createBtn').getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; })()`,
  )) as [number, number];
  await page.mouse.click(r[0], r[1]);
  await pas(page, 40);
  await page.mouse.click(195, 300);
  await pas(page, 40);
  // le toucher qui referme le menu tombe sur la Toile : la fiche de la dalle dessous s'ouvre (comme dans le prototype) — on la referme
  // (sa descente : 420 ms à l'horloge, pilotée ici)
  await fermerFiche(page);
  await pas(page, 30);
}

/*
 * LES TESTS QUE LES SONDES VISENT (tests/rendu/sondes/toile-a.json ; leurs titres sont bâtis dans une boucle, les voici en toutes lettres) :
 *  le rythme de « encre » (v60/v61) : une parole arrive puis part, le mouvement finit à la durée validée
 *  la vie au repos sous « encre » (C-028) : une ou deux dalles bougent 1 à 2 s, toutes les 5 à 15 s, jamais périodique, puis reviennent
 *  le retour exact sous « touffe » (C-028, v127) : après chaque mouvement de repos, 0 pixel d'écart sur toute la Toile
 *  le zoom (v46–v47), sombre : dézoom jusqu'à la Toile entière (0,72) et encarts effacés, zoom avant à 5, le double toucher, planter et retirer ramènent le défaut
 *  le zoom (v46–v47), clair : dézoom jusqu'à la Toile entière (0,72) et encarts effacés, zoom avant à 5, le double toucher, planter et retirer ramènent le défaut
 */

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_rythme — LE RYTHME D'UN MONDE NE DÉRIVE PAS (v60, Tom, 26 sept. 2026 ; v61 : à l'horloge, Houle par image)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/**
 * LES DURÉES VALIDÉES — redteam_rythme.py, ATTENDU (celebration-mondes.html, 26 sept. 2026, et les validations de Tom citées), en ms :
 * la fin du mouvement DANS LE MOTEUR (l'image où sa boucle s'arrête), arrivée puis départ ; Houle (`sillons`) : le NOMBRE D'IMAGES.
 */
const ATTENDU: Record<string, ['horloge' | 'images', [number, number], [number, number]]> = {
  encre: ['horloge', [872, 33], [851, 32]], // v76 : le repli (Tom, 27 sept. : départs 780–870 ms validés)
  touffe: ['horloge', [812, 48], [791, 48]],
  mosaique: ['horloge', [792, 47], [780, 47]],
  braille: ['horloge', [865, 44], [786, 40]],
  pixel: ['horloge', [817, 46], [784, 44]],
  halin: ['horloge', [2270, 135], [2995, 170]], // v111 (Tom, 30 sept.) : « accepte 2 267 ms »
  esquille: ['horloge', [1437, 82], [1426, 73]],
  madrure: ['horloge', [2432, 132], [2431, 133]],
  ritournelle: ['horloge', [1945, 113], [2040, 116]],
  bobinette: ['horloge', [2462, 57], [2463, 70]],
  terrazzo: ['horloge', [799, 45], [820, 46]],
  gravure: ['horloge', [793, 48], [797, 45]],
  sillons: ['images', [1313, 36], [950, 29]], // v61 : Houle, EXCEPTION ÉCRITE, par image
  brouillamini: ['horloge', [1742, 70], [2046, 92]], // v73 (Tom : « valide-les toutes, telles que relevées »)
  chamade: ['horloge', [1668, 44], [1946, 44]],
  volubilis: ['horloge', [3178, 155], [1940, 119]], // v93 (V92 du juge) : le départ par le chemin « moteur », 1 940 ms
  guingois: ['horloge', [1722, 30], [1865, 31]],
  chantourne: ['horloge', [1677, 16], [1849, 36]],
  // ⚑ C-328 (Tom, 21 nov. 2026) : le départ de Mascaret à 2 000 ms — ce que fait le prototype validé (1 834 avant, relevé en temps réel)
  mascaret: ['horloge', [1674, 20], [2000, 32]],
  ramage: ['horloge', [1690, 83], [2620, 149]], // v82 (Tom) : l'arrivée sans fondu
};
/** redteam_rythme.py, TOLERANCE : ± max(100 ms, 8 %), sauf ces lignes (v64, v74, v105, v136 — chacune une décision de Tom) */
const TOLERANCE: Record<string, number> = {
  'halin depart': 0.15,
  'halin arrivee': 0.15,
  'brouillamini arrivee': 0.15,
  'bobinette arrivee': 0.15,
  'esquille arrivee': 0.15,
  'ritournelle arrivee': 0.15,
  'guingois depart': 0.15,
  'ramage arrivee': 0.33,
  'ramage depart': 0.33,
  'volubilis arrivee': 0.15,
  'volubilis depart': 0.15,
  'chantourne depart': 0.33,
};
/** Houle : ± max(3, 20 %) images ; ± 30 % au départ (v93, Tom) */
const TOL_IMG: Record<string, number> = { 'sillons depart': 0.3 };
/**
 *  · le départ de Ramage — ligne RETIRÉE du juge d'origine (v93, Tom : « un contrôle qui ne protège rien est pire que pas de contrôle ») ;
 *  · l'arrivée de Volubilis — sa durée validée (v92–v93 : 1 890 ms) suppose l'arrivée PRÉPARÉE par la page + (`_simPrepare`, dans l'app) ;
 *    sans elle le moteur attend le jardin de son Worker : au lot 2 (la page +).
 */
const NON_JUGE: Record<string, string> = {
  'ramage depart': 'ligne retirée du juge d’origine (v93, Tom)',
  'volubilis arrivee': 'la durée validée (1 890 ms) suppose l’arrivée préparée par la page + (v92–v93) : au lot 2',
};
/** les mondes dont l'arrivée se construit hors de l'image (Worker, tranches) : la page rend la main au navigateur entre deux images */
const PREPARENT = new Set(['ramage', 'volubilis']);
/**
 * Houle se juge à 30 images par seconde (une image du moteur toutes les deux images d'horloge) : c'est la cadence à laquelle Tom l'a
 * validée (v61 : « elle tourne à ~30 i/s sur la page validée ») ; ses images se comptent comme le juge d'origine (la dernière image où un
 * bloc de 32 px change de plus de 0,5 niveau, ramené à 16,67 ms). Les autres mondes : 60 i/s, la cadence de celebration-mondes.
 */
const CADENCE: Record<string, number> = { sillons: 2 };
const RYTHME_CI = ['encre', 'halin', 'esquille', 'sillons', 'chamade'];

/**
 * redteam_rythme.py, `mouvement` (chemin « moteur ») : le monde posé (hasard amorcé à 777), puis une parole arrive (`Toile.addPromi`, le
 * hasard réamorcé à 12345) et part (`Toile.sync`) ; pour chacun, la fin du mouvement dans le moteur (à l'horloge) et ses images.
 */
const MESURE = `async ([m, k, reel]) => { const w = window, h = w.__promi.horloge;
  w.__ta.lcg(777); w.__promi.magasin.choisirMonde(m); await w.__ta.pas(180, reel ? 8 : null); await w.__ta.pose(1500, reel ? 8 : null);
  if (!w.__rafO) w.__rafO = w.requestAnimationFrame; const o = w.__rafO;
  w.requestAnimationFrame = k === 1 ? o : (cb) => { let n = k; const f = (t) => { if (--n > 0) o(f); else cb(t); }; return o(f); };
  const cv = document.getElementById('toileCv'), c = document.createElement('canvas'); c.width = Math.round(cv.width / 4); c.height = Math.round(cv.height / 4);
  const x = c.getContext('2d', { willReadFrequently: true }); const img = () => { x.drawImage(cv, 0, 0, c.width, c.height); return x.getImageData(0, 0, c.width, c.height).data; };
  const B = 8, bw = Math.ceil(c.width / B), bh = Math.ceil(c.height / B);
  const chg = (a, b) => { const acc = new Float32Array(bw * bh); for (let y = 0; y < c.height; y++) for (let xx = 0; xx < c.width; xx++) { const i = (y * c.width + xx) * 4;
      acc[((y / B) | 0) * bw + ((xx / B) | 0)] += Math.abs(a[i] - b[i]) + Math.abs(a[i + 1] - b[i + 1]) + Math.abs(a[i + 2] - b[i + 2]); }
    let mm = 0; for (const v of acc) if (v > mm) mm = v; return mm / (B * B * 3) / k; };
  const P = w.promises;
  const mesure = async (g) => { let prev = img(); const t0 = h.maintenant(); g(); let fin = 0, im = 0, bout = null;
    for (let n = 0; n < 900; n++) { h.images(k); if (reel) await w.__ta.dors(8); const cur = img(); const v = chg(prev, cur); prev = cur; im++; const t = h.maintenant() - t0;
      if (v > 0.5) fin = im; if (bout == null && t > 50 && !w.Toile_state().running) bout = t; if (bout != null && t > bout + 300) break; }
    return { boucle: bout == null ? null : Math.round(bout), images: fin }; };
  const arrivee = await mesure(() => { P.push(Object.assign({}, P[0], { id: 97001, title: 'mesure du rythme', nuee: null })); w.__ta.lcg(12345); w.Toile.addPromi(97001); });
  await w.__ta.pas(90, reel ? 8 : null);
  const depart = await mesure(() => { const i = P.findIndex((p) => p.id === 97001); if (i >= 0) P.splice(i, 1); w.Toile.sync(P.filter((p) => !p.draft).map((p) => p.id)); });
  w.requestAnimationFrame = o; return { arrivee, depart, monde: w.Toile.getTheme() }; }`;

test('le rythme (v60–v93) : les constantes qui font le rythme sont dans le moteur, et Houle reste par image', () => {
  // redteam_rythme.py, CONSTANTES : écrites en dur, lues dans le moteur repris (la copie octet pour octet du prototype)
  let S = MOTEUR;
  // la sonde : une constante qui dérive (la transition de Ritournelle raccourcie)
  if (sonde('rythme-constante')) S = S.replace('Rrit.transDur = 1900', 'Rrit.transDur = 1700');
  const CONSTANTES: Array<[string, RegExp]> = [
    ['Ritournelle, transition 1 900 ms', /Rrit\.transDur\s*=\s*1900\b/g],
    ['Esquille, transition 1 400 ms', /Resq\.transDur\s*=\s*1400\b/g],
    ['Bobinette, transition 2 400 ms', /Rbob\.transDur\s*=\s*2400\b/g],
    ['Madrure, transition 2 400 ms', /Rmad\.transDur\s*=\s*2400\b/g],
    ['Halin, transition 1 800 ms', /Rhal\.transDur\s*=\s*1800\b/g],
    ['Halin, retrait 900 ms', /Rhal\.partDur\s*=\s*900\b/g],
    ['ressort du moteur 0,17 / 0,22', /var _kW=0\.17, _kX=0\.22, _redem=frame\._redem;/g],
    [
      "v61 · cinq mondes à l'horloge, 0,83 / 0,78",
      /terrazzo: \{ressort:\[0\.83,0\.78,1\][\s\S]*mosaique: \{ressort:\[0\.83,0\.78,1\][\s\S]*braille: {2}\{ressort:\[0\.83,0\.78,1\][\s\S]*pixel: {4}\{ressort:\[0\.83,0\.78,1\][\s\S]*gravure: {2}\{ressort:\[0\.83,0\.78,1\][\s\S]*var _rs=_rg\('ressort'\); if\(_rs\)\{ if\(_rs\[2\]&&_redem\) _dtf=1; _kW=1-Math\.pow\(_rs\[0\],_dtf\); _kX=1-Math\.pow\(_rs\[1\],_dtf\); \}/g,
    ],
    ['v61 · un redémarrage de boucle fait UN pas', /function kick\(\)\{if\(!running\)\{running=true;frame\._redem=1;/g],
    ['v61 · mondes neufs : temps vrai en sous-pas de 1/60 s', /if\(frame\._redem\|\|_rdt>0\.25\)_rdt=1\/60; \}/g],
    [
      'ressort Pochade/Touffe 0,838 / 0,79',
      /encre: {4}\{ressort:\[0\.838,0\.79,0\][^\n]*\n {2}touffe: {3}\{ressort:\[0\.838,0\.79,0\]/g,
    ],
    ["fondu d'arrivée 760 ms", /var p=ease\(\(now-s\.t0\)\/760\)/g],
    ['Brouillamini 1 600 · 900', /Rbro\.transDur = 1600; Rbro\.douce = true; Rbro\.partDur = 900;/g],
    ['Chamade 1 600 · 900', /Rcha\.transDur = 1600; Rcha\.douce = true; Rcha\.partDur = 900;/g],
    ['Volubilis 1 600 · 900', /Rvol\.transDur = 1600; Rvol\.douce = true; Rvol\.partDur = 900;/g],
    ['Guingois 1 600 · 900', /Rgui\.transDur = 1600; Rgui\.douce = true; Rgui\.partDur = 900;/g],
    ['Chantourné 1 600 · 900', /Rchi\.transDur = 1600; Rchi\.douce = true; Rchi\.partDur = 900;/g],
    ['Mascaret 1 600 · 900', /Rmas\.transDur = 1600; Rmas\.douce = true; Rmas\.partDur = 900;/g],
    ['Ramage 1 600 · 900', /Rram\.transDur = 1600; Rram\.douce = true; Rram\.partDur = 900;/g],
    [
      "v72 · Ramage : le fondu du plumage d'arrivée = ARR 900 ms",
      /var g, W, H, seeds, cOf, avg, L3 = 300;\n {2}function _sync\(\) \{[^\n]*\}\n {2}var UPL = 53\.55, ARR = 900, RET = 760;/g,
    ],
  ];
  const r = CONSTANTES.map(([nom, re]) => [nom, (S.match(re) ?? []).length]);
  expect(r, 'chaque constante, une fois').toEqual(CONSTANTES.map(([nom]) => [nom, 1]));
  // v61 — EXCEPTION ÉCRITE : Houle (sillons) reste PAR IMAGE
  const l = S.split('\n').find((x) => x.includes('var _kW=0.17, _kX=0.22')) ?? '';
  expect(l.split('/*')[0]!.includes("theme==='sillons'"), 'Houle reste par image (exception écrite)').toBe(false);
});

for (const m of Object.keys(ATTENDU))
  test(`le rythme de « ${m} » (v60/v61) : une parole arrive puis part, le mouvement finit à la durée validée`, async ({
    page,
  }) => {
    test.skip(CI && !COMPLET && !RYTHME_CI.includes(m), `intégration continue : l'échantillon ${RYTHME_CI.join(', ')}`);
    await page.setViewportSize({ width: 390, height: 844 });
    const erreurs: string[] = [];
    page.on('pageerror', (e) => erreurs.push(String(e)));
    await ouvrir(page, { ...DEMO, promi_theme: 'dark' });
    // la sonde : le ressort ralenti (la version qui dérive du juge d'origine, sauvegardes/rythme-v61/app-derive-ressort.html)
    if (sonde('rythme-ressort'))
      await page.evaluate(() => {
        const R = (window as unknown as { Toile_reglages(m: string): { ressort: number[] } }).Toile_reglages('encre');
        R.ressort = [0.93, 0.9, 0];
      });
    await poser(page);
    const r = (await page.evaluate(`(${MESURE})(${JSON.stringify([m, CADENCE[m] ?? 1, PREPARENT.has(m)])})`)) as {
      arrivee: { boucle: number | null; images: number };
      depart: { boucle: number | null; images: number };
      monde: string;
    };
    expect(r.monde, 'le monde est posé').toBe(m);
    const [fam, arr, dep] = ATTENDU[m]!;
    const ko: string[] = [];
    for (const [sens, ref, mes] of [
      ['arrivee', arr, r.arrivee],
      ['depart', dep, r.depart],
    ] as const) {
      const cle = `${m} ${sens}`;
      if (NON_JUGE[cle]) {
        test.info().annotations.push({
          type: 'non jugé',
          description: `${cle} : ${NON_JUGE[cle]!} (relevé ${JSON.stringify(mes)})`,
        });
        continue;
      }
      if (fam === 'horloge') {
        const tl = Math.max(100, ref[0] * (TOLERANCE[cle] ?? 0.08));
        if (!(mes.boucle != null && Math.abs(mes.boucle - ref[0]) <= tl))
          ko.push(`${sens} : fin du mouvement ${String(mes.boucle)} ms, attendu ${String(ref[0])} ± ${String(tl)}`);
      } else {
        const tol = Math.max(3, ref[1] * (TOL_IMG[cle] ?? 0.2));
        if (Math.abs(mes.images - ref[1]) > tol)
          ko.push(`${sens} : ${String(mes.images)} images à 30 i/s, attendu ${String(ref[1])} ± ${String(tol)}`);
      }
    }
    test.info().annotations.push({
      type: 'non jugé',
      description:
        'la cadence (≥ 60 % de la validée) : une propriété du temps réel — le relevé de l’iPhone (?releve=1)',
    });
    expect(ko, JSON.stringify(r)).toEqual([]);
    expect(erreurs).toEqual([]);
  });

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_vivant — LA TOILE VIT AU REPOS (v126, Tom, 4 oct. 2026, C-028)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/**
 * Les valeurs décidées, en dur (redteam_vivant.py, docstring, INT_MIN…) : intervalle ≥ 5 s (de la fin d'un mouvement au début du
 * suivant) et ≤ 15 s (+ 1 s de lectures) ; un mouvement dure 1 à 2 s (± 0,35 s de lectures) ; au plus 2 dalles ; au plus 6 % des pixels
 * de la Toile ; après un mouvement, la Toile revenue à l'image d'avant (≤ 0,02 %) ; jamais de motif périodique (les intervalles
 * s'étalent sur plus de 3 s) ; entre deux mouvements, la boucle du moteur arrêtée. Les mondes qui vivent : ceux du juge ; Esquille,
 * Volubilis, Guingois, Ramage n'ont pas encore leur manière (`_VIV_NON`) : ils restent IMMOBILES.
 */
const INT_MIN = 5.0;
const INT_MAX = 15.0;
const DUR_MIN = 1.0;
const DUR_MAX = 2.0;
const DALLES_MAX = 2;
const PART_MAX = 6.0;
const VIVENT = [
  'encre',
  'touffe',
  'mosaique',
  'braille',
  'pixel',
  'halin',
  'ritournelle',
  'bobinette',
  'gravure',
  'sillons',
  'brouillamini',
];
const IMMOBILES = ['volubilis', 'guingois', 'ramage', 'esquille'];
const VIVANT_ECH = CI ? ['encre', 'touffe'] : ['encre', 'touffe', 'sillons', 'brouillamini'];
/** la durée de repos simulée par monde : 3 min (le juge d'origine) avec PROMI_COMPLET ; 90 s sur le Mac ; 45 s sur la CI */
const DUREE_VIVANT = COMPLET ? 180 : CI ? 45 : 90;

/** redteam_vivant.py, JS : le canevas lu toutes les 100 ms (6 images d'horloge) ; un mouvement = une suite de lectures où des pixels changent */
const REPOS = `async (duree) => { const w = window, h = w.__promi.horloge;
  const cv = document.getElementById('toileCv'); const o = document.createElement('canvas'); o.width = 390; o.height = Math.round(390 * cv.height / cv.width);
  const g = o.getContext('2d', { willReadFrequently: true });
  const lit = () => { g.drawImage(cv, 0, 0, o.width, o.height); return g.getImageData(0, 0, o.width, o.height).data; };
  const dif = (x, y) => { let n = 0; for (let i = 0; i < x.length; i += 4) { if (Math.max(Math.abs(x[i] - y[i]), Math.abs(x[i + 1] - y[i + 1]), Math.abs(x[i + 2] - y[i + 2])) > 10) n++; } return 100 * n / (x.length / 4); };
  let repos = lit(), av = repos, E = [], cur = null, t0 = h.maintenant(), boucleEntre = 0, lectures = 0;
  while (h.maintenant() - t0 < duree * 1000) { h.images(6); const t = (h.maintenant() - t0) / 1000, d = lit(), p = dif(av, d); lectures++;
    if (p > 0.004) { if (!cur) { cur = { t0: t, max: 0, repos }; E.push(cur); } cur.t1 = t; cur.max = Math.max(cur.max, dif(cur.repos, d)); cur.calme = 0; }
    else if (cur) { if (++cur.calme >= 4) { cur.retour = dif(cur.repos, d); delete cur.repos; cur = null; repos = d; } }
    else { if (w.Toile.vivant.boucle()) boucleEntre++; }
    av = d; }
  E.forEach((e) => { delete e.repos; });
  return { E, lectures, boucleEntre, journal: w.Toile.vivant.journal().map((j) => Object.assign({}, j, { ts: (j.t - t0) / 1000 })).filter((j) => j.ts >= -0.5) }; }`;

interface Mvt {
  t0: number;
  t1: number;
  max: number;
  retour?: number;
}
interface Repos {
  E: Mvt[];
  lectures: number;
  boucleEntre: number;
  journal: Array<{ ts: number; n: number; d: number }>;
}

async function auRepos(page: Page, m: string, duree: number): Promise<Repos> {
  await choisirMonde(page, m);
  // 7 s, comme le juge, puis la boucle du moteur arrêtée une seconde (v128 : la référence de repos se prend sur une Toile posée)
  await pas(page, 420);
  await page.evaluate(
    `(() => { let calme = 0, n = 0; while (calme < 60 && n++ < 9000) { window.__promi.horloge.images(1); calme = window.Toile.vivant.boucle() ? 0 : calme + 1; } })()`,
  );
  return (await page.evaluate(`(${REPOS})(${String(duree)})`)) as Repos;
}

function jugeVivant(m: string, r: Repos, duree: number): string[] {
  const J = r.journal;
  // un mouvement de la vie au repos = une suite de lectures qui commence quand le moteur a tiré (le journal RECONNAÎT l'épisode ; ce qu'on
  // en juge — durée, étendue, retour — est lu sur les pixels) ; ce qui bouge sans tirage est compté à part
  // un mouvement encore en cours à la fin de la fenêtre (sans retour lu) n'est pas jugé : la mesure l'a coupé
  const E = r.E.filter((e) => e.retour != null && J.some((j) => e.t0 - j.ts >= -0.35 && e.t0 - j.ts <= 0.6));
  const autres = r.E.filter((e) => e.retour != null && !E.includes(e));
  const durs = E.map((e) => e.t1 - e.t0 + 0.1);
  const ints = E.slice(1).map((e, i) => e.t0 - E[i]!.t1);
  const debuts = E.slice(1).map((e, i) => e.t0 - E[i]!.t0);
  const ko: string[] = [];
  const v = (nom: string, c: boolean, d: string): void => {
    if (!c) ko.push(`[${m}] ${nom} — ${d}`);
  };
  const fx = (a: number[]): string => JSON.stringify(a.map((x) => +x.toFixed(2)));
  const nmin = Math.max(2, Math.floor(duree / 30));
  v(
    `la Toile bouge au repos (au moins ${String(nmin)} mouvements en ${String(duree)} s)`,
    E.length >= nmin,
    `${String(E.length)}`,
  );
  v('jamais moins de 5 s entre deux mouvements', !ints.length || Math.min(...ints) >= INT_MIN - 0.25, fx(ints));
  v('jamais plus de 15 s sans mouvement', !ints.length || Math.max(...ints) <= INT_MAX + 1.0, fx(ints));
  v(
    'aucun motif périodique (les intervalles s’étalent sur plus de 3 s)',
    debuts.length < 3 || Math.max(...debuts) - Math.min(...debuts) > 3.0,
    fx(debuts),
  );
  v(
    'un mouvement dure 1 à 2 s',
    durs.length > 0 && Math.min(...durs) >= DUR_MIN - 0.35 && Math.max(...durs) <= DUR_MAX + 0.35,
    fx(durs),
  );
  v(
    `jamais toute la Toile : au plus ${String(PART_MAX)} % des pixels`,
    E.length > 0 && Math.max(...E.map((e) => e.max)) <= PART_MAX,
    fx(E.map((e) => e.max)),
  );
  v(
    'jamais plus de deux dalles (le tirage du moteur)',
    J.length > 0 && Math.max(...J.map((j) => j.n)) <= DALLES_MAX,
    '',
  );
  v(
    'après un mouvement, la Toile revenue à l’image d’avant (≤ 0,02 %)',
    E.length > 0 && Math.max(...E.map((e) => e.retour ?? 0)) <= 0.02,
    fx(E.map((e) => e.retour ?? 0)),
  );
  v('rien d’autre ne bouge sur la Toile au repos', !autres.length, JSON.stringify(autres.slice(0, 3)));
  v(
    'coût nul entre deux mouvements : la boucle du moteur arrêtée',
    r.boucleEntre <= Math.max(2, E.length * 3),
    `${String(r.boucleEntre)} lectures sur ${String(r.lectures)}`,
  );
  return ko;
}

for (const m of VIVENT)
  test(`la vie au repos sous « ${m} » (C-028) : une ou deux dalles bougent 1 à 2 s, toutes les 5 à 15 s, jamais périodique, puis reviennent`, async ({
    page,
  }) => {
    test.skip(
      !COMPLET && !VIVANT_ECH.includes(m),
      `l'échantillon ${VIVANT_ECH.join(', ')} (tous avec PROMI_COMPLET=1)`,
    );
    // PRÉEXISTANT (C-327, 20 nov. 2026) : sous Touffe, pendant un mouvement de repos, 6 à 11 % de toute la Toile change (pour 6 % au plus
    // décidés) — DANS LE PROTOTYPE AUSSI, mesuré par le même protocole quand Touffe est le monde au chargement (6,7 %) : les calques des
    // fleurs, refaits pendant le mouvement, se superposent autrement. (Touffe choisi longtemps après le chargement : 0,3 à 1,4 %.) Le retour,
    // lui, est exact. Trouvé en chemin et corrigé : la vraie app ne faisait pas frémir la Toile 1,5 s après le chargement (app.html ≈ l. 7271).
    test.setTimeout(10 * 60 * 1000);
    await page.setViewportSize({ width: 390, height: 844 });
    const erreurs: string[] = [];
    page.on('pageerror', (e) => erreurs.push(String(e)));
    // la sonde : un intervalle FIXE de 6 s (le crochet du moteur `_vivantFixe` — la preuve du juge d'origine, `--fixe`)
    await ouvrir(page, banc(25), { vivant: true, avant: sonde('vivant-fixe') ? 'window._vivantFixe=6000;' : '' });
    const r = await auRepos(page, m, DUREE_VIVANT);
    let ko = jugeVivant(m, r, DUREE_VIVANT);
    // C-327 : sous Touffe, l'étendue (« jamais toute la Toile ») dépasse aussi dans le prototype — nommée, pas jugée, en attendant Tom ;
    // tout le reste du juge (durée, intervalles, retour exact, boucle arrêtée) l'est
    if (m === 'touffe') {
      const pre = ko.filter((k) => k.includes('jamais toute la Toile'));
      ko = ko.filter((k) => !pre.includes(k));
      if (pre.length) test.info().annotations.push({ type: 'préexistant (C-327)', description: pre.join(' · ') });
    }
    expect(ko, JSON.stringify({ E: r.E, journal: r.journal })).toEqual([]);
    expect(erreurs).toEqual([]);
  });

test('la vie au repos : les mondes qui n’ont pas encore leur manière restent immobiles (Volubilis, Guingois, Ramage, Esquille)', async ({
  page,
}) => {
  test.setTimeout(10 * 60 * 1000);
  await page.setViewportSize({ width: 390, height: 844 });
  // la sonde : tous les mondes tirés (le crochet du moteur `_vivTous`) — un monde immobile se met à bouger
  await ouvrir(page, banc(25), { vivant: true, avant: sonde('vivant-tous') ? 'window._vivTous=true;' : '' });
  const duree = COMPLET ? 180 : 30;
  const ko: string[] = [];
  for (const m of CI && !COMPLET ? ['ramage', 'esquille'] : IMMOBILES) {
    const r = await auRepos(page, m, duree);
    if (r.E.length || r.journal.length)
      ko.push(`[${m}] ${String(r.E.length)} mouvement(s), ${String(r.journal.length)} tirage(s) en ${String(duree)} s`);
  }
  expect(ko).toEqual([]);
});

test('la vie au repos : avec « Réduire les animations », la Toile reste immobile (24 s)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // la sonde : la page ignore le réglage du téléphone
  if (!sonde('vivant-reduit')) await page.emulateMedia({ reducedMotion: 'reduce' });
  await ouvrir(page, banc(25), { vivant: true });
  const r = await auRepos(page, 'encre', 24);
  expect({ mouvements: r.E.length, tirages: r.journal.length }).toEqual({ mouvements: 0, tirages: 0 });
});
// Non porté : « hors écran (l'Index ouvert par-dessus, 22 s) : aucun mouvement tiré » — au lot 4 (l'Index). La condition (le centre de la
// Toile libre, `_vivLibre`) est vérifiée sur l'accueil par accueil.spec (« la Toile vit au repos »).

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_retour — LA VIE AU REPOS : LE RETOUR EST EXACT (v127, Tom, C-028)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/** « Cent mouvements, zéro pixel d'écart au retour » — la valeur décidée : 0 pixel, à l'égalité stricte, sur le canevas ENTIER */
const RESTE_DECIDE = 0;
const MONDES_RETOUR = [
  'encre',
  'touffe',
  'mosaique',
  'braille',
  'pixel',
  'sillons',
  'gravure',
  'halin',
  'bobinette',
  'ritournelle',
  'madrure',
  'terrazzo',
  'chamade',
  'chantourne',
  'brouillamini',
  'mascaret',
];
const RETOUR_CI = ['touffe', 'encre', 'chamade'];
/** sept mouvements par monde (112, « cent mouvements ») avec PROMI_COMPLET ; trois sinon (48 sur le Mac) */
const N_RETOUR = COMPLET ? 7 : 3;
/** redteam_retour.py, JS : avant chaque mouvement forcé (`Toile.vivant.force()`) le canevas entier ; pendant, des pixels changent ; après, 0 */
const RETOUR = `async (N) => { const w = window, h = w.__promi.horloge; const cv = document.getElementById('toileCv');
  const o = document.createElement('canvas'); o.width = cv.width; o.height = cv.height; const g = o.getContext('2d', { willReadFrequently: true });
  const lit = () => { g.globalCompositeOperation = 'copy'; g.drawImage(cv, 0, 0); return g.getImageData(0, 0, o.width, o.height).data; };
  const ecart = (a, b) => { let n = 0; for (let i = 0; i < a.length; i += 4) if (a[i] !== b[i] || a[i + 1] !== b[i + 1] || a[i + 2] !== b[i + 2]) n++; return n; };
  const out = [];
  for (let k = 0; k < N; k++) { let e = 0; while (w.Toile.vivant.boucle() && e++ < 3000) h.images(1); h.images(15);
    const av = lit(); const n0 = w.Toile.vivant.journal().length; w.Toile.vivant.force(); let j = w.Toile.vivant.journal(); if (j.length === n0) { out.push({ rate: 1 }); continue; } j = j[j.length - 1];
    let mx = 0; const fin = h.maintenant() + j.d + 200;
    for (let im = 1; h.maintenant() < fin; im++) { h.images(1); if (im % 5 === 0) { const n = ecart(lit(), av); if (n > mx) mx = n; } }
    e = 0; while (w.Toile.vivant.boucle() && e++ < 3000) h.images(1); h.images(12);
    out.push({ pendant: mx, reste: ecart(lit(), av) }); }
  return out; }`;

for (const m of MONDES_RETOUR)
  test(`le retour exact sous « ${m} » (C-028, v127) : après chaque mouvement de repos, 0 pixel d'écart sur toute la Toile`, async ({
    page,
  }) => {
    test.skip(CI && !COMPLET && !RETOUR_CI.includes(m), `intégration continue : l'échantillon ${RETOUR_CI.join(', ')}`);
    await page.setViewportSize({ width: 390, height: 844 });
    const erreurs: string[] = [];
    page.on('pageerror', (e) => erreurs.push(String(e)));
    // aucun mouvement spontané pendant la mesure (le juge d'origine : `_vivantFixe=600000`)
    let avant = 'window._vivantFixe=600000;';
    // la sonde : la version d'avant v127 — la Toile n'est plus rendue à l'image gardée au tirage (`_vivRendre`, `_vivImage` : la copie
    // ENTIÈRE, 1:1, d'un canevas hors du document sur celui de la Toile)
    if (sonde('retour-sans-rendu'))
      avant += `(() => { const d = CanvasRenderingContext2D.prototype.drawImage; CanvasRenderingContext2D.prototype.drawImage = function (s, ...a) {
        if (s instanceof HTMLCanvasElement && !s.isConnected && this.canvas.id === 'toileCv' && this.globalCompositeOperation === 'copy' && a.length === 2) return;
        return d.call(this, s, ...a); }; })();`;
    await ouvrir(page, banc(25), { vivant: true, avant });
    await choisirMonde(page, m);
    await pas(page, 420);
    await poser(page);
    const R = (await page.evaluate(`(${RETOUR})(${String(N_RETOUR)})`)) as Array<{
      rate?: number;
      pendant?: number;
      reste?: number;
    }>;
    const joues = R.filter((r) => !r.rate);
    expect(joues.length, `les mouvements sont joués (${String(N_RETOUR)} demandés)`).toBeGreaterThanOrEqual(
      N_RETOUR - 1,
    );
    expect(
      joues.filter((r) => (r.pendant ?? 0) > 0).length,
      `des pixels changent pendant le mouvement (${JSON.stringify(R)})`,
    ).toBeGreaterThanOrEqual(Math.max(1, joues.length - 2));
    expect(
      joues.map((r) => r.reste),
      `retour : ${String(RESTE_DECIDE)} pixel d'écart`,
    ).toEqual(joues.map(() => RESTE_DECIDE));
    expect(erreurs).toEqual([]);
  });

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_zoom — LE ZOOM DE LA TOILE, AU DOIGT (v46–v47, Tom)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/** redteam_zoom.py : ZMIN 0,72 (la Toile entière) · ZMAX 5 · défaut(n) = n ≥ 20 → 1 (v47, Tom : « la Toile prend tout l'écran par défaut ») */
const ZMIN = 0.72;
const ZMAX = 5.0;
const DEFAUT = (n: number): number | null => (n >= 20 ? 1.0 : null);

for (const theme of ['sombre', 'clair'] as const)
  test(`le zoom (v46–v47), ${theme} : dézoom jusqu'à la Toile entière (0,72) et encarts effacés, zoom avant à 5, le double toucher, planter et retirer ramènent le défaut`, async ({
    page,
  }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    const erreurs: string[] = [];
    page.on('pageerror', (e) => erreurs.push(String(e)));
    await ouvrir(page, { ...banc(25), promi_theme: theme === 'clair' ? 'light' : 'dark' });
    // la sonde : l'accueil ne s'efface pas quand la Toile est entière (sa règle `.toile-entiere` défaite)
    if (sonde('zoom-encarts'))
      await page.addStyleTag({
        content:
          '#device.toile-entiere .acc-plat,#device.toile-entiere .acc-barre{visibility:visible!important;opacity:1!important;pointer-events:auto!important}',
      });
    // la sonde : le double toucher ne recadre plus
    if (sonde('zoom-double'))
      await page.evaluate(() => {
        (window as unknown as { Toile_recadre(): void }).Toile_recadre = () => {};
      });
    await poser(page);
    const vue = async (): Promise<{ s: number; ox: number; oy: number }> =>
      (await page.evaluate('Toile.vue()')) as { s: number; ox: number; oy: number };
    const nb = async (): Promise<number> => (await page.evaluate('Toile.count()')) as number;
    const ko: string[] = [];
    const t = (nom: string, c: boolean, d: string): void => {
      if (!c) ko.push(`${nom} — ${d}`);
    };
    // 1 · dézoom : pincé loin, relâché → 0,72 ; la Toile ENTIÈRE dans l'écran ; les encarts effacés et hors du doigt
    await geste(page, pince(320, 40));
    await poser(page);
    const v1 = await vue();
    const entiere = v1.ox >= -0.5 && v1.oy >= -0.5 && v1.ox + 390 * v1.s <= 390.5;
    const enc = (await page.evaluate(
      `['accPlat','accBarre'].map(i => { const c = getComputedStyle(document.getElementById(i)); return [+c.opacity, c.visibility, c.pointerEvents]; })`,
    )) as Array<[number, string, string]>;
    const efface = enc.every(([o, v, p]) => (o < 0.05 || v === 'hidden') && (p === 'none' || v === 'hidden'));
    t(
      '1 · dézoom relâché à 0,72, Toile entière, encarts effacés et hors du doigt',
      Math.abs(v1.s - ZMIN) < 0.01 && entiere && efface,
      `${JSON.stringify(v1)} ${JSON.stringify(enc)}`,
    );
    // 4 · zoom avant : pincé au-delà, relâché → 5 (l'élastique revient à la borne)
    for (let i = 0; i < 3; i++) {
      await geste(page, pince(40, 330));
      await pas(page, 24);
    }
    await poser(page);
    const v4 = await vue();
    t("4 · zoom avant : l'élastique revient à 5", Math.abs(v4.s - ZMAX) < 0.01, `${String(v4.s)}`);
    // 3 · le symbole « recadrer » est là quand la main a posé la vue — lu À L'ÉCRAN (visible, dans l'appareil)
    const rond = (await page.evaluate(`(() => { const e = document.getElementById('accRecadre'); if (!e) return false;
      const r = e.getBoundingClientRect(), s = getComputedStyle(e), d = document.getElementById('device').getBoundingClientRect();
      return r.width > 8 && s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0.5 && r.left >= d.left && r.right <= d.right && r.top >= d.top && r.bottom <= d.bottom; })()`)) as boolean;
    t('3 · le symbole « recadrer » est là', rond, '');
    // 2 · le zoom persiste : le menu du + ouvert puis refermé (la fiche et l'Index du juge d'origine : aux lots 3 et 4)
    await menuPlus(page);
    await poser(page);
    const v2 = await vue();
    t(
      '2 · le zoom persiste (le menu du + ouvert puis refermé)',
      Math.abs(v2.s - v4.s) < 0.005 && Math.abs(v2.ox - v4.ox) < 0.5,
      `${String(v4.s)} → ${String(v2.s)}`,
    );
    // 5 · le double toucher, sur une dalle, ramène au défaut et ne demande aucune fiche
    await geste(page, pince(330, 99)); // ×1,5 : des dalles entières dans l'écran
    await poser(page);
    const cible =
      (await page.evaluate(`(() => { const L = Toile_lecture(); const cv = document.getElementById('toileCv').getBoundingClientRect();
      for (const g of L.graines) { if (g.kind === 'gray' || g.pid == null) continue; const x = g.x * L.vue.s + L.vue.ox, y = g.y * L.vue.s + L.vue.oy;
        if (x < 20 || x > 370 || y < 150 || y > 700) continue; const h = Toile.hit(x, y); if (!h || h.pid !== g.pid) continue;
        const e = document.elementFromPoint(cv.left + x, cv.top + y); if (e && e.id === 'toileCv') return [cv.left + x, cv.top + y, g.pid]; } return null; })()`)) as
        [number, number, number] | null;
    const j0 = (await page.evaluate('window.__promi.nav.journal().length')) as number;
    if (cible) {
      // les deux touchers dans la page, dans la même tâche : l'écart se lit à l'heure des ÉVÉNEMENTS (moins de 320 ms) ; deux clics de
      // Playwright arrivent à la page à plus de 320 ms l'un de l'autre sur l'intégration continue (une image toutes les 0,7 s)
      await page.evaluate(([x, y]) => {
        const cv = document.getElementById('toileCv')!;
        for (const id of [21, 22])
          for (const t of ['pointerdown', 'pointerup'])
            cv.dispatchEvent(
              new PointerEvent(t, {
                pointerId: id,
                isPrimary: true,
                pointerType: 'touch',
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y,
              }),
            );
      }, cible);
      await pas(page, 60);
    }
    await poser(page);
    const v5 = await vue();
    const n5 = await nb();
    const demandes = ((await page.evaluate('window.__promi.nav.journal()')) as Array<{ vers: string }>).slice(j0);
    const d5 = DEFAUT(n5);
    t(
      '5 · double toucher sur une dalle → défaut, aucune fiche',
      !!cible && d5 != null && Math.abs(v5.s - d5) < 0.01 && !demandes.some((x) => x.vers === 'fiche'),
      `${String(v5.s)} (défaut ${String(d5)} pour ${String(n5)}) · ${JSON.stringify(demandes)}`,
    );
    // 6 · un toucher simple demande la fiche : accueil.spec (« toucher une dalle demande SA fiche »)
    // 7 · planter ramène le défaut (le chemin « moteur » ; la page + vient au lot 2)
    await geste(page, pince(300, 90));
    await poser(page);
    await page.evaluate(
      `(() => { const P = window.promises; const q = Object.assign({}, P[0], { id: 97101, title: 'juge zoom', nuee: null }); delete q.place; P.push(q); Toile.addPromi(97101); })()`,
    );
    await poser(page);
    const v7 = await vue();
    const d7 = DEFAUT(await nb());
    t(
      '7 · planter ramène le défaut',
      d7 != null && Math.abs(v7.s - d7) < 0.01,
      `${String(v7.s)} (défaut ${String(d7)})`,
    );
    // 8 · retirer ramène le défaut
    await geste(page, pince(300, 90));
    await poser(page);
    await page.evaluate(
      `(() => { const ids = window.promises.filter(q => !q.draft).map(q => q.id); Toile.sync(ids.slice(0, -1)); })()`,
    );
    await poser(page);
    const v8 = await vue();
    const d8 = DEFAUT(await nb());
    t(
      '8 · retirer ramène le défaut',
      d8 != null && Math.abs(v8.s - d8) < 0.01,
      `${String(v8.s)} (défaut ${String(d8)})`,
    );
    expect(ko).toEqual([]);
    expect(erreurs).toEqual([]);
  });

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_toile_stable — LES DALLES NE BOUGENT PAS, NE S'ENTASSENT PAS (v159–v160, Tom, C-177)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/**
 * En dur (redteam_toile_stable.py) : chaque dalle revient à sa place À L'ÉCRAN à 1 pt près, les graines à 0,5 pt, le zoom à 1 %, le
 * même nombre de cellules ; aucune paire de dalles « entassée » (moins de 0,3 × l'écart moyen des cellules) ; des places valides (dans
 * [0, 1], finies, pas (0, 0)) et distinctes (pas deux à 0,003 près dans une même famille) ; sur trois réouvertures, les mêmes places, les
 * graines à 1 pt, la vue à 4 pt.
 */
const GEO = `(() => { const c = Toile_cellules(), v = c.view; return { v: [v.s, v.ox, v.oy], n: c.c.length, th: Toile.getTheme(),
  g: c.c.filter(s => s.kind !== 'gray').map(s => [s.pid == null ? ('n' + s.kind) : s.pid, s.x, s.y, s.x * v.s + v.ox, s.y * v.s + v.oy]) }; })()`;
const ENTASSE = `(() => { const c = Toile_cellules(), v = c.view, col = c.c.filter(s => s.kind !== 'gray'), P = col.map(s => [s.x * v.s + v.ox, s.y * v.s + v.oy]);
  const seuil = 0.3 * Math.sqrt(390 * 844 / Math.max(1, c.c.length)) * v.s, pr = []; let dm = 1e9;
  for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) { const d = Math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1]); dm = Math.min(dm, d); if (d < seuil) pr.push(+d.toFixed(1)); }
  return { n: P.length, seuil: +seuil.toFixed(1), dmin: +dm.toFixed(1), paires: pr }; })()`;
/** les places que la vraie app ENREGISTRE (son magasin, relu de son stockage à la réouverture) */
const PLACES = `window.__promi.magasin.etat().paroles.filter(p => !p.draft).map(p => [p.id, p.place == null ? null : p.place])`;
type Geo = {
  v: [number, number, number];
  n: number;
  th: string;
  g: Array<[number | string, number, number, number, number]>;
};
type Places = Array<[number, unknown]>;

function placesOk(pl: Places): string | null {
  const bonne = (p: unknown): p is number[] =>
    Array.isArray(p) &&
    p.length >= 2 &&
    p.length <= 3 &&
    p.every((x) => typeof x === 'number' && Number.isFinite(x)) &&
    p[0] >= 0 &&
    p[0] <= 1 &&
    p[1] >= 0 &&
    p[1] <= 1 &&
    !(p[0] === 0 && p[1] === 0);
  const bad = pl.filter(([, p]) => p != null && !bonne(p));
  if (bad.length) return `places invalides ${JSON.stringify(bad.slice(0, 2))}`;
  const v = pl.map(([, p]) => p).filter((p): p is number[] => bonne(p));
  for (let i = 0; i < v.length; i++)
    for (let j = i + 1; j < v.length; j++)
      if (
        (v[i]![2] ?? 0) === (v[j]![2] ?? 0) &&
        Math.abs(v[i]![0]! - v[j]![0]!) < 0.003 &&
        Math.abs(v[i]![1]! - v[j]![1]!) < 0.003
      )
        return `une place prise deux fois ${JSON.stringify([v[i], v[j]])}`;
  return null;
}
function ecartGeo(a: Geo, b: Geo, ecran = 1.0, graines = 0.5): string | null {
  const A = new Map(a.g.map((x) => [x[0], x]));
  const B = new Map(b.g.map((x) => [x[0], x]));
  if (A.size !== B.size || [...A.keys()].some((k) => !B.has(k))) return `dalles ${String(A.size)} → ${String(B.size)}`;
  let gr = 0;
  let ec = 0;
  for (const [k, x] of A) {
    const y = B.get(k)!;
    gr = Math.max(gr, Math.abs(x[1] - y[1]), Math.abs(x[2] - y[2]));
    ec = Math.max(ec, Math.abs(x[3] - y[3]), Math.abs(x[4] - y[4]));
  }
  const z = Math.abs(a.v[0] - b.v[0]) / a.v[0];
  if (ec <= ecran && gr <= graines && z <= 0.01 && a.n === b.n && a.th === b.th) return null;
  return `à l'écran ${ec.toFixed(1)} pt · graines ${gr.toFixed(1)} · zoom ${a.v[0].toFixed(3)} → ${b.v[0].toFixed(3)} · cellules ${String(a.n)} → ${String(b.n)} · monde ${a.th} → ${b.th}`;
}
async function entasse(page: Page): Promise<string | null> {
  const e = (await page.evaluate(ENTASSE)) as { n: number; seuil: number; dmin: number; paires: number[] };
  return e.paires.length
    ? `${String(e.n)} dalles · écart mini ${String(e.dmin)} pt (seuil ${String(e.seuil)}) · paires ${JSON.stringify(e.paires.slice(0, 6))}`
    : null;
}
/** trois réouvertures (la vraie app relit son stockage) : les mêmes places, les graines à 1 pt, la vue à 4 pt, rien d'entassé */
async function reouvre(page: Page): Promise<string[]> {
  const a = { pl: JSON.stringify(await page.evaluate(PLACES)), geo: (await page.evaluate(GEO)) as Geo };
  const d: string[] = [];
  for (let k = 0; k < 3; k++) {
    await page.goto('about:blank');
    await ouvrir(page, {}, { relire: true });
    await poser(page);
    if (JSON.stringify(await page.evaluate(PLACES)) !== a.pl)
      d.push(`ouverture ${String(k + 2)} : les places ont changé`);
    const e = ecartGeo(a.geo, (await page.evaluate(GEO)) as Geo, 4.0, 1.0);
    if (e) d.push(`ouverture ${String(k + 2)} : ${e}`);
    const en = await entasse(page);
    if (en) d.push(`ouverture ${String(k + 2)} : ${en}`);
  }
  return d;
}
/**
 * LA SONDE COMMUNE : la relecture qui ne répare pas — les places de la sauvegarde, abîmées ou empilées, rendues au moteur telles quelles
 * (la cause de C-177 : six paroles à la même place [0.42, 0.74], que le moteur rendait côte à côte).
 */
async function sansReparer(page: Page, places: (i: number) => unknown): Promise<void> {
  await page.evaluate(
    (pl) => {
      const w = window as unknown as {
        promises: Array<Record<string, unknown>>;
        Toile: { sync(ids: unknown[]): void };
        __promi: { magasin: { noterPlaces(p: Array<{ id: number; place: unknown }>): void } };
      };
      w.promises.forEach((q, i) => {
        q['place'] = pl[i];
      });
      w.Toile.sync(w.promises.filter((q) => !q['draft']).map((q) => q['id']));
      w.__promi.magasin.noterPlaces(w.promises.map((q, i) => ({ id: q['id'] as number, place: pl[i] })));
    },
    Array.from({ length: 60 }, (_, i) => places(i)),
  );
}

test("la Toile stable (C-177) · T : l'état de Tom — à l'ouverture rien d'entassé, des places valides et distinctes, trois réouvertures identiques", async ({
  page,
}) => {
  test.setTimeout(6 * 60 * 1000);
  await page.setViewportSize({ width: 390, height: 844 });
  await ouvrir(page, lireEtat(ETAT));
  // la sonde : les paroles empilées à la même place, sans réparation (la donnée de C-177)
  if (sonde('stable-empile')) await sansReparer(page, () => [0.42, 0.74]);
  await poser(page);
  const ko: string[] = [];
  const e = await entasse(page);
  if (e) ko.push(`à l'ouverture : ${e}`);
  const p = placesOk((await page.evaluate(PLACES)) as Places);
  if (p) ko.push(p);
  ko.push(...(await reouvre(page)));
  expect(ko, `état : ${ETAT}`).toEqual([]);
});

const ABIMES: Array<[string, number, (i: number) => unknown]> = [
  ['empilées', 5, () => [0.42, 0.74]],
  ['à zéro', 5, () => [0, 0]],
  [
    'hors de [0, 1]',
    5,
    (i) =>
      [
        [1.7, -0.4],
        [-0.2, 0.5],
        [0.5, 3],
        [9, 9],
        [0.3, 1.2],
      ][i % 5],
  ],
  ['non numériques', 5, (i) => [['a', 'b'], [null, 0.5], [0.5], [0.1, 0.2, 7], 'x'][i % 5]],
  ['empilées, 25 paroles', 25, () => [0.5, 0.5, 0]],
];
test('la Toile stable (C-177) · X : des places abîmées exprès sont réparées à l’ouverture — rien d’entassé, places valides et distinctes, stables', async ({
  page,
}) => {
  test.setTimeout(12 * 60 * 1000);
  await page.setViewportSize({ width: 390, height: 844 });
  const ko: string[] = [];
  const cas = CI && !COMPLET ? [ABIMES[0]!, ABIMES[3]!] : ABIMES;
  for (const [nom, n, f] of cas)
    for (const m of CI && !COMPLET ? ['encre'] : ['encre', 'mascaret']) {
      const ls: Record<string, string> = { ...banc(n), promi_studio: studio(m) };
      const S = JSON.parse(ls['promi_state']!) as { promises: Array<Record<string, unknown>> };
      S.promises.forEach((q, i) => {
        q['place'] = f(i);
      });
      ls['promi_state'] = JSON.stringify(S);
      await page.goto('about:blank');
      await ouvrir(page, ls);
      // la sonde : la relecture ne répare plus (les places abîmées rendues au moteur et au magasin telles quelles)
      if (sonde('stable-abimees')) await sansReparer(page, f);
      await poser(page);
      const e = await entasse(page);
      const p = placesOk((await page.evaluate(PLACES)) as Places);
      const r = await reouvre(page);
      if (e || p || r.length) ko.push(`[${nom} · ${m}] ${[e, p, ...r].filter(Boolean).join(' ; ')}`);
    }
  expect(ko).toEqual([]);
});

test('la Toile stable (C-177) · S : une Toile saine — rien n’est réparé, les places enregistrées sont celles de la sauvegarde', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const ko: string[] = [];
  for (const n of [5, 25])
    for (const m of ['encre', 'mascaret']) {
      const ls: Record<string, string> = { ...banc(n), promi_studio: studio(m) };
      await page.goto('about:blank');
      await ouvrir(page, ls);
      // la sonde : l'app « répare » une place saine (la première parole déplacée au centre)
      if (sonde('stable-saine')) await sansReparer(page, (i) => (i === 0 ? [0.5, 0.5, 0] : undefined));
      await poser(page);
      const av = (
        JSON.parse(ls['promi_state']!) as { promises: Array<{ id: number; place?: unknown; draft?: boolean }> }
      ).promises
        .filter((q) => !q.draft)
        .map((q) => [q.id, q.place ?? null]);
      const pl = (await page.evaluate(PLACES)) as Places;
      if (JSON.stringify(pl) !== JSON.stringify(av))
        ko.push(`[${String(n)} paroles · ${m}] les places ont changé : ${JSON.stringify(pl.slice(0, 3))}`);
    }
  // « les graines identiques au prototype à 0,5 pt » (le juge d'origine) : entrees.spec (les mêmes graines que le prototype, sur l'état réel)
  expect(ko).toEqual([]);
});

const M_MONDES = COMPLET
  ? [
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
    ]
  : CI
    ? ['encre', 'esquille']
    : ['encre', 'esquille', 'ritournelle', 'mascaret', 'terrazzo'];
const M_N = COMPLET ? [1, 5, 9, 25, 50] : CI ? [5, 25] : [1, 5, 25];
test(`la Toile stable (C-177) · M : à froid rien d'entassé ; le menu du + ouvert puis refermé, chaque dalle à sa place à 1 pt`, async ({
  page,
}) => {
  test.setTimeout(14 * 60 * 1000);
  await page.setViewportSize({ width: 390, height: 844 });
  const ko: string[] = [];
  for (const n of M_N)
    for (const m of M_MONDES) {
      let ls = banc(n === 9 ? 10 : n);
      if (n === 9) {
        const S = JSON.parse(ls['promi_state']!) as { promises: unknown[] };
        S.promises = S.promises.slice(0, -1);
        ls['promi_state'] = JSON.stringify(S);
      }
      ls = { ...ls, promi_studio: studio(m) };
      delete ls['promi_theme'];
      await page.goto('about:blank');
      await ouvrir(page, ls);
      await poser(page);
      const th = (await page.evaluate('Toile.getTheme()')) as string;
      if (th !== m) {
        ko.push(`[${String(n)} · ${m}] le monde posé à l'ouverture : ${th}`);
        continue;
      }
      const e = await entasse(page);
      if (e) ko.push(`[${String(n)} · ${m}] à froid : ${e}`);
      const a = (await page.evaluate(GEO)) as Geo;
      // la seule « page » du lot 1 : le menu du + (les sept pages du juge d'origine — Studio, Aura, Index, Fil, Réglages, fiche, page + —
      // viennent avec leurs lots, 2 à 8)
      await menuPlus(page);
      // la sonde : refermer le menu recadre la Toile sur une dalle (le Studio de C-177 : la vue d'un autre cadrage, rendue en revenant)
      if (sonde('stable-menu'))
        await page.evaluate(
          `(() => { const g = Toile_lecture().graines.find(q => q.pid != null && q.kind !== 'gray'); if (g) Toile.vueVers(g.pid, 0.3); })()`,
        );
      await poser(page);
      const d = ecartGeo(a, (await page.evaluate(GEO)) as Geo);
      if (d) ko.push(`[${String(n)} · ${m}] menu du + : ${d}`);
    }
  expect(ko, `${String(M_MONDES.length)} monde(s) × {${M_N.join(', ')}} paroles`).toEqual([]);
});

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_toile_vide — UNE TOILE SANS PAROLE EST VIDE, À CHAQUE INSTANT DU CHARGEMENT (v147, Tom, C-136)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/** la règle, en dur : 0 cellule colorée (`Toile.colored()`, l'état réel du semis) à chaque relevé, de la première image à 9 s */
const VIDE_MS = 9000;
const N_VIDE = COMPLET ? 15 : CI ? 3 : 5;
test('la Toile vide (C-136) : des chargements sans parole, aucune cellule colorée à aucun instant (un relevé toutes les 40 ms, 9 s)', async ({
  browser,
}) => {
  test.setTimeout(10 * 60 * 1000);
  const ko: string[] = [];
  for (let i = 0; i < N_VIDE; i++) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    const page = await ctx.newPage();
    const erreurs: string[] = [];
    page.on('pageerror', (e) => erreurs.push(String(e)));
    // en TEMPS RÉEL (le chargement de l'iPhone) ; les minuteurs natifs gardés avant que l'horloge de l'app prenne leur place
    await page.addInitScript({
      content: `(() => { const st = window.setTimeout.bind(window), now = performance.now.bind(performance); window.__tl = [];
      (function arme() { const T = window.Toile; if (!T || !T.colored) return st(arme, 5); let der = -2;
        (function tic() { let c = -1; try { c = T.colored(); } catch (e) {} if (c !== der) { window.__tl.push([now() | 0, c]); der = c; } st(tic, 40); })(); })();
      ${
        // la sonde : l'ancien remplissage de l'onboarding (C-136 : `obFill`, 420 ms après le chargement, toute la Toile colorée)
        sonde('vide-colore')
          ? `(function col() { const T = window.Toile; if (!T || !T.plantOne) return st(col, 5); st(() => { for (let k = 0; k < 69; k++) T.plantOne(); }, 420); })();`
          : ''
      } })();`,
    });
    await page.goto('http://127.0.0.1:5180/?banc=1');
    await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
    // onboarding déjà fait, aucune sauvegarde (le cas B du juge ; le premier lancement, A, passe par l'onboarding : au lot 9)
    await page.evaluate(async () => {
      const p = (
        window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } }
      ).__promi;
      p.magasin.importer({ ls: { promi_onb: '1' } });
      await p.demarrer();
    });
    await page.waitForFunction(
      (ms) => {
        const tl = (window as unknown as { __tl: Array<[number, number]> }).__tl;
        return tl.length > 0 && performance.now() - tl[0]![0] >= ms;
      },
      VIDE_MS,
      { timeout: 60000 },
    );
    const e = (await page.evaluate(
      `({ n: window.__promi.magasin.etat().paroles.filter(p => !p.draft).length, c: Toile.colored(), tot: Toile.cells(), tl: window.__tl })`,
    )) as { n: number; c: number; tot: number; tl: Array<[number, number]> };
    const vus = e.tl.filter(([, c]) => c > 0).map(([, c]) => c);
    if (e.n !== 0 || e.c !== 0 || vus.length || e.tot === 0 || erreurs.length)
      ko.push(
        `chargement ${String(i + 1)} : ${String(e.n)} parole(s), ${String(e.c)} colorée(s) à 9 s sur ${String(e.tot)} cellules, jusqu'à ${String(Math.max(0, ...vus))} pendant le chargement ${JSON.stringify(e.tl.slice(0, 6))} ${erreurs.join(' ')}`,
      );
    await ctx.close();
  }
  expect(ko, `${String(N_VIDE)} chargements`).toEqual([]);
});
// Non porté : A (le premier lancement, onboarding compris) — au lot 9 ; C (le jeu de démonstration que le prototype pose sous navigateur
// piloté, puis que l'onboarding retire) — la vraie app n'a pas de jeu de démonstration. Remplaçant sur l'appareil : VALIDATION #4 (Tout
// effacer, puis six rechargements).

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_ritournelle — RITOURNELLE : LA RÈGLE DES 75 % (v146, Tom, 14 oct. 2026, C-088)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/**
 * En dur (redteam_ritournelle.py) : de 1 à 9 paroles, chaque coulée visible à ≥ 75 % de sa surface et les coulées couvrent ≥ 75 % de la
 * zone visible (du bas du plateau, y 100, au haut de la barre, y 710) ; de 10 à 15, 70 % et 70 % ; aucun saut — l'échelle change de ≤ 8 %
 * d'une parole à la suivante, la surface moyenne d'une coulée baisse au plus de 15 points de plus que le partage attendu (n/(n+1)) ; une
 * parole seule peint sa coulée (≥ 75 % de la zone hors du fond #DFCAA4, lu sur l'image) ; toucher une dalle demande sa fiche.
 */
const ZONE = [0, 100, 390, 710] as const;
const VIS = 0.75;
const COUV = 0.75;
const VIS10 = 0.7;
const COUV10 = 0.7;
const PAS_ECHELLE = 0.08;
const BAISSE = 0.15;
const TITRES = [
  'rendre le livre',
  'écrire à Lou',
  'arroser le ficus',
  'courir dimanche',
  'appeler mamie',
  'finir la maquette',
  'ranger le garage',
  'faire les crêpes',
  'réparer le vélo',
  'trier les photos',
  'semer les radis',
  'nager le mardi',
  'lire Proust',
  'planter un arbre',
  'écrire à Paul',
];
const NMAX = COMPLET || !CI ? 15 : 10;

type Forme = { pid: number; pts: number[] };
function dedans(P: Array<[number, number]>, x: number, y: number): boolean {
  let c = false;
  for (let i = 0, j = P.length - 1; i < P.length; j = i++) {
    const [xi, yi] = P[i]!;
    const [xj, yj] = P[j]!;
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c;
  }
  return c;
}
/**
 * La part VISIBLE de chaque coulée — dans la zone ET non recouverte par une coulée peinte après elle (l'ordre du peintre) —, la couverture
 * de la zone par leur union, et l'aire moyenne d'une coulée (pt²). Échantillonné à 2 points par point sur [-30, 420] × [50, 760], comme le juge.
 */
function formes(vue: [number, number, number], F: Forme[]): { vis: number[]; couv: number; aire: number } {
  const [s, ox, oy] = vue;
  const P = F.map((f) => {
    const q: Array<[number, number]> = [];
    for (let i = 0; i < f.pts.length; i += 2) q.push([ox + s * f.pts[i]!, oy + s * f.pts[i + 1]!]);
    const xs = q.map((p) => p[0]);
    const ys = q.map((p) => p[1]);
    return { q, b: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)] as const };
  });
  const K = 2;
  const tot = P.map(() => 0);
  const vu = P.map(() => 0);
  let couv = 0;
  let zone = 0;
  for (let yy = 50 * K; yy < 760 * K; yy++)
    for (let xx = -30 * K; xx < 420 * K; xx++) {
      const x = (xx + 0.5) / K;
      const y = (yy + 0.5) / K;
      const dansZ = x >= ZONE[0] && x < ZONE[2] && y >= ZONE[1] && y < ZONE[3];
      if (dansZ) zone++;
      let haut = -1;
      for (let k = 0; k < P.length; k++) {
        const { q, b } = P[k]!;
        if (x < b[0] || x > b[2] || y < b[1] || y > b[3]) continue;
        if (dedans(q, x, y)) {
          tot[k]!++;
          haut = k;
        }
      }
      if (dansZ && haut >= 0) {
        couv++;
        vu[haut]!++;
      }
    }
  const aire = tot.reduce((a, b) => a + b, 0) / (K * K) / Math.max(1, tot.length);
  return { vis: tot.map((t, k) => (t ? vu[k]! / t : 0)), couv: couv / zone, aire };
}

test('Ritournelle (C-088, v146) : de 1 à 15 paroles plantées une à une, chaque coulée visible à 75 %, la zone couverte à 75 %, aucun saut, toucher demande la fiche', async ({
  page,
}) => {
  test.setTimeout(14 * 60 * 1000);
  await page.setViewportSize({ width: 390, height: 844 });
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  const modele = (JSON.parse(banc(1)['promi_state']!) as { promises: Array<Record<string, unknown>> }).promises[0]!;
  // une Toile vide, en clair (le fond #DFCAA4 que juge l'image), sous Ritournelle. Les quinze paroles sont dans le magasin, GARDÉES DE CÔTÉ
  // (aucune n'est plantée) : toucher une dalle ne demande la fiche que d'une parole que le magasin connaît (src/ecrans/toile.ts)
  const gardees = TITRES.slice(0, NMAX).map((t, i) => {
    const p: Record<string, unknown> = {
      ...modele,
      id: 98001 + i,
      title: t,
      cle: t,
      who: 'moi',
      status: 'encours',
      draft: true,
    };
    delete p['place'];
    delete p['dalle'];
    return p;
  });
  await ouvrir(page, {
    promi_onb: '1',
    promi_theme: 'light',
    promi_studio: studio('ritournelle'),
    promi_state: JSON.stringify({ v: 1, promises: gardees, NUE: {}, NUEEMEM: {}, NUEDALLE: {} }),
  });
  await poser(page);
  expect(await page.evaluate('Toile.getTheme()')).toBe('ritournelle');
  expect(await page.evaluate('Toile.count()'), 'la Toile est vide au départ').toBe(0);
  const ko: string[] = [];
  const L: Array<{ n: number; s: number; aire: number }> = [];
  for (let i = 0; i < NMAX; i++) {
    // planter : le chemin « moteur » (la parole quitte le côté et `Toile.addPromi`) — la page + vient au lot 2, où ce juge se rejoue
    // par le vrai chemin
    await page.evaluate((id) => {
      const w = window as unknown as {
        promises: Array<Record<string, unknown>>;
        Toile: { addPromi(id: number): void };
      };
      const p = w.promises.find((q) => q['id'] === id)!;
      p['draft'] = false;
      delete p['place'];
      w.Toile.addPromi(id);
    }, 98001 + i);
    await pas(page, 312);
    await poser(page);
    // la sonde : le cadrage serré (une Toile vue de trop près, posée par la main : les coulées sortent de l'écran)
    if (sonde('ritournelle-serre')) {
      await geste(page, pince(100, 250));
      await poser(page);
    }
    const e = (await page.evaluate(
      `(() => { const v = Toile.vue(); return { vue: [v.s, v.ox, v.oy], formes: (window._ritFormes || []).slice(), g: Toile_graines(), neuf: Toile.semisNeuf ? Toile.semisNeuf() : null, n: window.promises.filter(p => !p.draft).length }; })()`,
    )) as {
      vue: [number, number, number];
      formes: Forme[];
      g: Array<[number | null, number, number, string]>;
      neuf: boolean | null;
      n: number;
    };
    const n = e.n;
    const f = e.formes.length ? formes(e.vue, e.formes) : { vis: [0], couv: 0, aire: 0 };
    const mat =
      (await page.evaluate(`(() => { const cv = document.getElementById('toileCv'), k = cv.width / 390, d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
      let n = 0, t = 0; for (let y = ${String(ZONE[1])}; y < ${String(ZONE[3])}; y += 3) for (let x = ${String(ZONE[0])}; x < ${String(ZONE[2])}; x += 3) {
        const i = (Math.floor(y * k) * cv.width + Math.floor(x * k)) * 4; t++; if (Math.abs(d[i] - 223) + Math.abs(d[i + 1] - 202) + Math.abs(d[i + 2] - 164) > 30) n++; } return n / t; })()`)) as number;
    L.push({ n, s: e.vue[0], aire: f.aire });
    const v = (nom: string, c: boolean, d: string): void => {
      if (!c) ko.push(`${String(n)} parole(s) · ${nom} — ${d}`);
    };
    v(
      'A · la Toile n’a que ses paroles (aucune cellule vide, pas de couronne)',
      n === i + 1 && e.g.length === n && e.neuf === true && e.g.every((g) => g[3] !== 'gray'),
      `${String(e.g.length)} graine(s)`,
    );
    const [v0, c0] = n <= 9 ? [VIS, COUV] : [VIS10, COUV10];
    v(
      `B · chaque coulée visible à ≥ ${String(v0 * 100)} %, la zone couverte à ≥ ${String(c0 * 100)} %`,
      e.formes.length === n && Math.min(...f.vis) >= v0 && f.couv >= c0,
      `la moindre ${(100 * Math.min(...f.vis)).toFixed(0)} % · couverture ${(100 * f.couv).toFixed(0)} % · échelle ${e.vue[0].toFixed(3)} · ${String(e.formes.length)} coulée(s)`,
    );
    v(
      `C · sur l'image, la matière couvre ≥ ${String(c0 * 100)} % de la zone`,
      mat >= c0,
      `${(100 * mat).toFixed(0)} %`,
    );
    if (n === 1)
      v('D · une parole seule PEINT sa coulée (≥ 75 % de la zone)', mat >= 0.75, `${(100 * mat).toFixed(0)} %`);
    if (n === 6 || n === 12) {
      // F · toucher une dalle demande sa fiche, au point (à l'écran) de chaque graine visible
      let ouvertes = 0;
      let essais = 0;
      for (const g of e.g) {
        const x = g[1] * e.vue[0] + e.vue[1];
        const y = g[2] * e.vue[0] + e.vue[2];
        if (!(y > 120 && y < 690 && x > 12 && x < 378)) continue;
        essais++;
        const j0 = (await page.evaluate('window.__promi.nav.journal().length')) as number;
        await page.mouse.click(x, y);
        await pas(page, 40);
        const j = (
          (await page.evaluate('window.__promi.nav.journal()')) as Array<{ vers: string; arg?: unknown }>
        ).slice(j0);
        if (j.some((q) => q.vers === 'fiche' && q.arg === g[0])) ouvertes++;
        await pas(page, 30);
      }
      v(
        'F · toucher une dalle demande SA fiche',
        essais >= 2 && ouvertes === essais,
        `${String(ouvertes)} sur ${String(essais)}`,
      );
    }
  }
  for (let k = 1; k < L.length; k++) {
    const a = L[k - 1]!;
    const c = L[k]!;
    const ech = a.s ? Math.abs(c.s / a.s - 1) : 9;
    const baisse = a.aire ? 1 - c.aire / a.aire : 1;
    const att = 1 - a.n / c.n;
    if (!(ech <= PAS_ECHELLE && baisse <= att + BAISSE))
      ko.push(
        `E · ${String(a.n)} → ${String(c.n)} : échelle ${a.s.toFixed(3)} → ${c.s.toFixed(3)} · coulée moyenne ${a.aire.toFixed(0)} → ${c.aire.toFixed(0)} pt²`,
      );
  }
  expect(ko, `${String(NMAX)} paroles`).toEqual([]);
  expect(erreurs).toEqual([]);
});

// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// redteam_ramage_onde — RAMAGE : NI DISQUE NI SAUT (v126–v127, Tom, C-009)
// ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
/**
 * v127 (Tom) : « Le disque est supprimé. […] Elle apparaît d'un coup, sans animation. Aucun anneau, aucun saut. » En dur : sur la vraie
 * Toile, une plume plantée paraît (≥ 1 image de changement de plus de 0,5 % des pixels) ; au plus UNE image change plus de 2 % des pixels
 * sur plus de 60 % de la Toile ; au plus 3 images de changement en tout.
 */
const SAUT_MAX = 2.0;
test('Ramage (C-009, v127) : une plume plantée sur la Toile paraît d’un coup — une seule image de changement d’ensemble, ni disque qui grandit, ni saut', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  await ouvrir(page, { ...banc(25), promi_studio: studio('ramage') });
  // la sonde : la plume qui pousse dans un DISQUE qui grandit (la version de v126 : le film de la pousse, puis le saut). Le film du moteur
  // (`_ramFilmOn`) ne joue plus qu'au Studio — mesuré : sur la Toile la plume arrive en une image avec ou sans lui ; la sonde le peint donc
  // elle-même : l'image d'avant gardée hors d'un disque qui grandit, 24 images, autour du centre de la Toile
  if (sonde('ramage-film'))
    await page.evaluate(`(() => { const T = window.Toile, f = T.addPromi; T.addPromi = function (...a) {
      const cv = document.getElementById('toileCv'), av = document.createElement('canvas'); av.width = cv.width; av.height = cv.height; av.getContext('2d').drawImage(cv, 0, 0);
      const r = f.apply(this, a); let k = 0, n = 0; const g = cv.getContext('2d'), A = av.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
      const change = () => { const d = g.getImageData(0, 0, cv.width, cv.height).data; let m = 0, t = 0; for (let i = 0; i < d.length; i += 4 * 97) { t++; if (Math.abs(d[i] - A[i]) > 12) m++; } return m > t * 0.05; };
      const disque = () => { if (n++ > 900) return; if (!k && !change()) { requestAnimationFrame(disque); return; } if (++k > 24) return;
        g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.beginPath(); g.rect(0, 0, cv.width, cv.height);
        g.arc(cv.width / 2, cv.height / 2, Math.hypot(cv.width, cv.height) / 2 * k / 24, 0, 7); g.clip('evenodd'); g.drawImage(av, 0, 0); g.restore(); requestAnimationFrame(disque); };
      requestAnimationFrame(disque); return r; }; })()`);
  await page.evaluate('window.__ta.pas(360, 8)');
  await page.evaluate('window.__ta.pose(1500, 8)');
  expect(await page.evaluate('Toile.getTheme()')).toBe('ramage');
  // la page rend la main au navigateur entre deux images (8 ms) : le plumage d'arrivée se calcule dans un Worker
  const im =
    (await page.evaluate(`(async () => { const w = window, h = w.__promi.horloge; const cv = document.getElementById('toileCv'); const o = document.createElement('canvas');
    const k = Math.min(1, 400 / cv.width); o.width = Math.round(cv.width * k); o.height = Math.round(cv.height * k); const g = o.getContext('2d', { willReadFrequently: true });
    const lit = () => { g.drawImage(cv, 0, 0, o.width, o.height); return g.getImageData(0, 0, o.width, o.height).data; }; let av = lit(); const im = []; const t0 = h.maintenant();
    const P = w.promises; const q = Object.assign({}, P[0], { id: 97001, title: 'onde', nuee: null }); delete q.place; P.push(q); w.Toile.addPromi(97001);
    while (h.maintenant() - t0 < 6000) { h.images(1); await w.__ta.dors(8); const d = lit(); let n = 0, x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1;
      for (let i = 0; i < d.length; i += 4) { if (Math.max(Math.abs(d[i] - av[i]), Math.abs(d[i + 1] - av[i + 1]), Math.abs(d[i + 2] - av[i + 2])) > 12) { n++; const p = i / 4, x = p % o.width, y = (p / o.width) | 0; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } }
      const part = 100 * n / (d.length / 4), boite = n ? 100 * ((x1 - x0 + 1) * (y1 - y0 + 1)) / (d.length / 4) : 0; if (part > 0.5) im.push([+part.toFixed(2), +boite.toFixed(1)]); av = d; }
    return im; })()`)) as Array<[number, number]>;
  expect(im.length, 'la plume plantée paraît').toBeGreaterThanOrEqual(1);
  const grandes = im.filter(([p, b]) => b > 60 && p > SAUT_MAX);
  expect(
    { ensemble: grandes.length <= 1, images: im.length <= 3 },
    `une seule image de changement d'ensemble (${JSON.stringify(im.slice(0, 12))})`,
  ).toEqual({ ensemble: true, images: true });
  expect(erreurs).toEqual([]);
});
// Non porté : le déclencheur au Studio (l'arrivée qui joue sur l'aperçu `#stBg`, deux ouvertures) — au lot 7 (le Studio).
