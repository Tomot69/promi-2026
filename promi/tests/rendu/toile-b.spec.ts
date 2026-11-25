/**
 * LOT 1, GROUPE B (C-326) — LES JUGES DE LA TOILE VIVANTE ET DE L'ACCUEIL, PORTÉS SUR LA VRAIE APP.
 *
 * Chaque test porte la décision EN DUR, avec sa source (le bloc daté de CLAUDE.md, le chantier, la docstring du juge Python d'origine), et
 * rougit sur au moins une sonde (`sondes/toile-b.json`, `npm run sondes`). Ce qui n'existe pas encore dans la vraie app (fiche, page +, Index,
 * Fil, Aura, Studio, Partager : lots 2 à 9) n'est pas inventé : toucher une dalle, une entrée, une pilule y NOTE une demande dans la
 * navigation (`window.__promi.nav`), et c'est cette demande qu'on juge.
 *
 * L'intégration continue tourne sous Linux, WebKit sans carte graphique (une image de la Toile toutes les 0,7 s environ) : aucune durée n'est
 * prise à l'horloge de Playwright ; une durée se lit dans la page, et une durée fine n'est JUGÉE que sur macOS, machine calme (charge < 4) —
 * sinon une annotation « non jugé ». Les COMPTES (combien de rendus, de recadrages, de touchers justes) se jugent partout.
 */
import { test, expect, type Browser, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { loadavg } from 'node:os';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { ETAT, RACINE, refermerPagePlus, sonde, stockage, fermerFiche, MAC_DE_TOM } from './aides.ts';

type Ls = Record<string, string>;

/** une Toile du banc (`banc-etats/etat-<n>.json`, le format d'export : importable par la vraie app) */
function etatBanc(n: number): Ls {
  const x = JSON.parse(readFileSync(join(RACINE, 'banc-etats', `etat-${String(n)}.json`), 'utf8')) as {
    ls?: Ls;
  } & Record<string, unknown>;
  const ls: Ls = {};
  for (const [k, v] of Object.entries(x.ls ?? x)) if (typeof v === 'string') ls[k] = v;
  return ls;
}

/** le bandeau « Garder ta Toile » (C-200 ①) fini : il couvre la Toile de 114 à 166 pt, et un juge qui touche la Toile y tomberait (les
 *  juges Python le coupaient de même : `promi_rappel_n`) — il est jugé à part (accueil.spec.ts, tests/unitaires/accueil.test.ts) */
function sansBandeau(ls: Ls): Ls {
  return { ...ls, promi_rappel_fin: '1' };
}

/** les vingt mondes, dans l'ordre du Studio (redteam_toucher.py, redteam_clair_sombre.py : EN DUR) */
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

/** une durée fine ne se juge que sur le Mac (le WebKit de l'iPhone), machine calme */
function calme(): boolean {
  return MAC_DE_TOM && (loadavg()[0] ?? 99) < 4;
}
function nonJuge(quoi: string): void {
  test.info().annotations.push({ type: 'non jugé', description: quoi });
}

/** l'app ouverte sur un état ; `avant` : du code posé dans la page AVANT le démarrage (le moteur n'est pas encore chargé) */
async function ouvrir(page: Page, ls: Ls, o: { avant?: string; vivant?: boolean } = {}): Promise<void> {
  await page.goto('http://127.0.0.1:5180/?banc=1');
  await page.waitForFunction('!!window.__promi');
  if (o.avant) await page.evaluate(o.avant);
  await page.evaluate(
    `(async () => { if (!${String(!!o.vivant)}) window._vivantOff = true; const p = window.__promi; p.magasin.importer({ ls: ${JSON.stringify(ls)} }); await p.demarrer(); })()`,
  );
  await suivreDemandes(page);
  await posee(page);
}

/** rouvrir l'app (rechargée) sur ce que le magasin a gardé dans le stockage — rien n'est importé */
async function rouvrir(page: Page): Promise<void> {
  await page.reload();
  await page.waitForFunction('!!window.__promi');
  await page.evaluate('(async () => { window._vivantOff = true; await window.__promi.demarrer(); })()');
  await suivreDemandes(page);
  await posee(page);
}

/**
 * les demandes de la navigation, toutes (le journal de l'app n'en garde que 100) : chaque `nav.ouvrir` est noté, à l'horloge de l'app.
 * C'est ce que l'app DEMANDE — l'écran demandé n'existe pas encore au lot 1.
 */
async function suivreDemandes(page: Page): Promise<void> {
  await page.evaluate(`(() => { const n = window.__promi.nav; if (n.__suivi) return; n.__suivi = 1; window.__dem = [];
    const o = n.ouvrir.bind(n); n.ouvrir = (v, a) => { window.__dem.push({ vers: v, arg: a, t: window.__promi.horloge.maintenant() }); return o(v, a); }; })()`);
}
type Dem = { vers: string; arg?: string | number; t: number };
const demandes = async (page: Page): Promise<Dem[]> => (await page.evaluate('window.__dem.slice()')) as Dem[];

/**
 * la Toile POSÉE : rien ne bouge (graines, poids, vue) depuis 600 ms et le moteur a arrêté sa boucle ; ou rien ne bouge depuis 2,5 s
 * (un monde qui garde sa boucle). Lu dans la page, à son horloge ; 60 s au plus (sur la CI une image toutes les 0,7 s).
 */
async function posee(page: Page, max = 60000): Promise<boolean> {
  return (await page.evaluate(`(async () => {
    const sig = () => { const L = Toile_lecture(); return JSON.stringify([L.vue.s.toFixed(4), L.vue.ox.toFixed(2), L.vue.oy.toFixed(2),
      L.graines.map((g) => [g.pid, g.kind, Math.round(g.x * 100), Math.round(g.y * 100), Math.round(g.w * 1000)])]); };
    const t0 = performance.now(); let a = sig(), depuis = performance.now();
    while (performance.now() - t0 < ${String(max)}) {
      await new Promise((f) => setTimeout(f, 150));
      const b = sig(); if (b !== a) { a = b; depuis = performance.now(); continue; }
      if (!Toile_state().running && performance.now() - depuis >= 600) return true;
      if (performance.now() - depuis >= 2500) return true;
    }
    return false; })()`)) as boolean;
}

/** l'état du magasin, avec une parole de plus (le seul chemin de plantation au lot 1 : l'import ; la page + est au lot 2) */
async function etatAvec(page: Page, titre: string): Promise<{ etat: unknown; id: number }> {
  return (await page.evaluate(`(() => { const e = JSON.parse(JSON.stringify(window.__promi.magasin.etat()));
    const base = e.paroles.find((p) => !p.draft) || e.paroles[0]; const id = Math.max(0, ...e.paroles.map((p) => p.id)) + 1;
    const q = JSON.parse(JSON.stringify(base)); q.id = id; q.title = ${JSON.stringify(titre)}; q.status = 'encours';
    for (const k of ['place', 'dalle', 'cle', 'ech', 'comments', 'parts', 'vuTenue', 'derAct']) delete q[k];
    if (q.suite) for (const k of ['place', 'dalle']) delete q.suite[k];
    e.paroles.push(q); return { etat: e, id }; })()`)) as { etat: unknown; id: number };
}
async function importer(page: Page, etat: unknown): Promise<void> {
  await page.evaluate((e) => {
    (window as unknown as { __promi: { magasin: { importer(x: unknown): void } } }).__promi.magasin.importer(e);
  }, etat);
}
async function etatActuel(page: Page): Promise<unknown> {
  return page.evaluate('JSON.parse(JSON.stringify(window.__promi.magasin.etat()))');
}

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_evol (v144, C-112) et redteam_pleine (v145, C-112 récidive) — UNE DALLE QUI ARRIVE OU PART NE FAIT RIEN TRAVAILLER D'AUTRE.
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

/**
 * Le profileur : chaque rappel de l'horloge (la seule de l'app : les minuteurs et les images du moteur comme de l'app passent par elle) est
 * chronométré, avec son ORIGINE lue dans la pile au moment où il est posé (le moteur : `promi-moteur.js` ; sinon l'app) ; une boucle d'images
 * relève la cadence ; les peintres de dalle du moteur sont comptés quand un code HORS du moteur les appelle. Posé avant le démarrage.
 */
const PROFILEUR = `(() => {
  window.__repris = new RegExp(location.origin.replace(/[.]/g, '\\\\.') + '/(\\\\?[^:\\\\s]*)?:\\\\d+:\\\\d+');
  const h = window.__promi.horloge; const R = window.__R = { on: false, rap: [], img: [], rendus: [] };
  const om = h.minuteur.bind(h), oi = h.intervalle.bind(h), oim = h.image.bind(h);
  const origine = () => (window.__repris.test(String(new Error().stack)) ? 'moteur' : 'app');
  const env = (cb, typ) => { if (typeof cb !== 'function') return cb; const o = origine();
    let nom = ''; try { nom = (cb.name || '') + ' · ' + String(cb).replace(/\\s+/g, ' ').slice(0, 110); } catch (e) {}
    return function () { if (!R.on) return cb.apply(this, arguments); const t = performance.now();
      try { return cb.apply(this, arguments); } finally { const d = performance.now() - t; if (d >= 1) R.rap.push([t, d, typ, o, nom]); else if ((o === 'moteur' && typ === 'image' && /^frame/.test(nom)) || /autoView/.test(nom)) R.rap.push([t, d, typ, o, nom]); /* les images du moteur et chaque recadrage sont comptés, même brefs */ } }; };
  h.minuteur = (cb, ms, ...a) => om(env(cb, 'minuteur'), ms, ...a);
  h.intervalle = (cb, ms, ...a) => oi(env(cb, 'intervalle'), ms, ...a);
  h.image = (cb) => oim(env(cb, 'image'));
  const boucle = () => { if (!R.on) { R.boucle = false; return; } R.img.push(performance.now()); oim(boucle); };
  window.__Ron = (v) => { R.on = v; if (v) { R.rap.length = 0; R.img.length = 0; R.rendus.length = 0; R.t0 = performance.now(); if (!R.boucle) { R.boucle = true; oim(boucle); } } };
})()`;
/** après le démarrage : les peintres de dalle du moteur, comptés quand ils sont appelés hors du moteur */
const RENDUS = `(() => { const R = window.__R; for (const k of ['dalleTrame', 'renderTo', 'preview', 'repaint', 'repaintWorld']) {
  const f = Toile[k]; if (typeof f !== 'function' || f.__compte) continue;
  const w = function () { const hors = !window.__repris.test(String(new Error().stack)); const t = performance.now(); const r = f.apply(this, arguments);
    if (R.on && hors) R.rendus.push([t, performance.now() - t, k]); return r; }; w.__compte = 1; Toile[k] = w; } })()`;

type Releve = {
  fin: number;
  app: number[];
  moteur: Array<[number, number, string]>;
  frames: number[];
  images: number[];
  recadrages: number;
  rendus: number;
};
/** le relevé du mouvement : du geste (t0) à la dernière image du moteur (au moins 1,6 s, comme redteam_pleine) */
async function releve(page: Page): Promise<Releve> {
  return (await page.evaluate(`(() => { const R = window.__R, t0 = R.t0; window.__Ron(false);
    const P = R.rap.map((e) => [e[0] - t0, e[1], e[2], e[3], e[4]]).filter((e) => e[0] >= 0);
    const fr = P.filter((e) => e[3] === 'moteur' && e[2] === 'image' && /^frame/.test(e[4]));
    const fin = Math.max(1600, fr.length ? Math.max(...fr.map((e) => e[0])) + 20 : 1600);
    const dans = P.filter((e) => e[0] <= fin);
    const im = R.img.map((t) => t - t0).filter((t) => t >= 0 && t <= fin); const images = []; for (let i = 1; i < im.length; i++) images.push(im[i] - im[i - 1]);
    return { fin, app: dans.filter((e) => e[3] === 'app').map((e) => e[1]),
      moteur: dans.filter((e) => e[3] === 'moteur' && !(e[2] === 'image' && /^frame/.test(e[4]))).map((e) => [e[0], e[1], e[4].slice(0, 60)]),
      frames: dans.filter((e) => e[3] === 'moteur' && e[2] === 'image' && /^frame/.test(e[4])).map((e) => e[1]),
      images, recadrages: dans.filter((e) => /autoView/.test(e[4])).length,
      rendus: R.rendus.filter((x) => x[0] - t0 >= 0 && x[0] - t0 <= fin).length }; })()`)) as Releve;
}

// les valeurs décidées, EN DUR (redteam_evol.py, v144 ; redteam_pleine.py, v145) :
const TRAVAIL_MAX = 20; // ms : aucun rappel au-delà, pendant le mouvement (« cible : aucune image au-delà de 20 ms »)
const IMAGE_MAX = 80; // ms : aucune image au-delà (evol 2)
const RECADRES_MAX = 6; // le recadrage ne passe pas à chaque image (evol 3)
const MOTEUR_P95 = 20; // la boucle du moteur : p95 ≤ 20 ms, jamais deux images
const DEUX_IMAGES = 33.4;
const LONGUES_MAX = 3; // pleine E : au plus 3 images au-delà de deux images
/** hors du Mac calme, le travail de l'app se juge à une borne large (un rappel de l'app ne dessine rien : il ne dépend pas de la carte graphique) */
const TRAVAIL_APP_LARGE = 100;

/** la sonde pendant le mouvement — posée juste après le geste */
async function sondesMouvement(page: Page, id: number): Promise<void> {
  if (sonde('evol-recadre'))
    // la régression de v142 : le recadrage refait à chaque image de l'apparition (20 fois)
    await page.evaluate('for (let i = 0; i < 20; i++) setTimeout(function () { Toile_autoView(); }, 30 * i)');
  if (sonde('evol-travail'))
    // un travail lourd de l'app tombé dans le mouvement (la passe de lisibilité, une tâche de fond : v144) — 250 ms
    await page.evaluate(
      'setTimeout(function () { const t = performance.now(); while (performance.now() - t < 250) {} }, 60)',
    );
  if (sonde('pleine-rendu'))
    // la cause de C-112 : les vignettes d'un écran fermé repeintes pendant que la dalle grandit (`peintMinis` → `_rendDalle`)
    await page.evaluate(
      `for (let i = 0; i < 4; i++) setTimeout(function () { Toile.dalleTrame(document.createElement('canvas'), ${String(id)}, 1); }, 120 * i)`,
    );
}

async function juger(
  page: Page,
  mondes: string[],
  ls: Ls,
  plante: string,
  quoi: string,
  imagesMax: 'evol' | 'pleine',
): Promise<string[]> {
  await ouvrir(page, ls, { avant: PROFILEUR });
  await page.evaluate(RENDUS);
  const fautes: string[] = [];
  const nonJuges: string[] = [];
  for (const m of mondes) {
    await page.evaluate((m) => {
      (window as unknown as { __promi: { magasin: { choisirMonde(m: string): void } } }).__promi.magasin.choisirMonde(
        m,
      );
    }, m);
    await posee(page);
    const n0 = (await page.evaluate('Toile_lecture().graines.filter((g) => g.pid != null).length')) as number;
    const avant = await etatActuel(page);
    const { etat, id } = await etatAvec(page, plante);
    for (const geste of ['planter', 'retirer'] as const) {
      const c0 = calme();
      await page.evaluate('window.__Ron(true)');
      await importer(page, geste === 'planter' ? etat : avant);
      await sondesMouvement(page, id);
      await page.waitForTimeout(400);
      await posee(page);
      await page.waitForTimeout(300);
      const r = await releve(page);
      const n1 = (await page.evaluate('Toile_lecture().graines.filter((g) => g.pid != null).length')) as number;
      const T = `[${m}, ${geste}]`;
      // les durées : jugées seulement sur le Mac, machine calme avant ET après le geste (redteam_pleine : « charge < 4 avant ET après »)
      const juge = c0 && calme();
      if (!juge) nonJuges.push(T);
      if (n1 !== n0 + (geste === 'planter' ? 1 : 0))
        fautes.push(
          `${T} la Toile porte ${String(n1)} paroles (attendu ${String(n0 + (geste === 'planter' ? 1 : 0))})`,
        );
      if (r.rendus) fautes.push(`${T} ${String(r.rendus)} rendu(s) de dalle hors du moteur pendant le mouvement`);
      if (geste === 'planter' && r.recadrages > RECADRES_MAX)
        fautes.push(`${T} le recadrage est passé ${String(r.recadrages)} fois (au plus ${String(RECADRES_MAX)})`);
      const appMax = Math.max(0, ...r.app);
      const borne = juge ? TRAVAIL_MAX : TRAVAIL_APP_LARGE;
      if (appMax > borne)
        fautes.push(
          `${T} un rappel de l'app de ${appMax.toFixed(1)} ms pendant le mouvement (au plus ${String(borne)})`,
        );
      if (juge) {
        const mo = r.moteur.filter((e) => !(e[0] < 60));
        const pire = mo.reduce((a, e) => (e[1] > a[1] ? e : a), [0, 0, ''] as [number, number, string]);
        if (pire[1] > TRAVAIL_MAX)
          fautes.push(
            `${T} un rappel du moteur de ${pire[1].toFixed(1)} ms à ${String(Math.round(pire[0]))} ms (${pire[2]})`,
          );
        const f = [...r.frames].sort((a, b) => a - b);
        const p95 = f.length ? f[Math.min(f.length - 1, Math.floor(f.length * 0.95))]! : 0;
        if (p95 > MOTEUR_P95 || (f.at(-1) ?? 0) > DEUX_IMAGES)
          fautes.push(`${T} la boucle du moteur : p95 ${p95.toFixed(1)} ms, pire ${(f.at(-1) ?? 0).toFixed(1)} ms`);
        const pireImage = Math.max(0, ...r.images);
        if (imagesMax === 'evol' && pireImage > IMAGE_MAX)
          fautes.push(`${T} une image de ${pireImage.toFixed(0)} ms (au plus ${String(IMAGE_MAX)})`);
        const longues = r.images.filter((x) => x > DEUX_IMAGES).length;
        if (imagesMax === 'pleine' && longues > LONGUES_MAX)
          fautes.push(`${T} ${String(longues)} images au-delà de 33,4 ms (au plus ${String(LONGUES_MAX)})`);
      }
    }
  }
  if (nonJuges.length)
    nonJuge(
      `${quoi} : les durées (travail du moteur, cadence des images) de ${nonJuges.join(' ')} — machine chargée ou hors du Mac`,
    );
  return fautes;
}

test("une dalle arrive puis part, cinq mondes (C-112) : aucun travail de l'app ni recadrage à chaque image pendant le mouvement", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // redteam_evol.py : trois paroles, puis une quatrième plantée et retirée, sous Pochade, Touffe, Tesselle, Ritournelle, Brouillamini (en dur)
  const ls = etatBanc(25);
  const st = JSON.parse(ls['promi_state']!) as { promises: unknown[] };
  st.promises = st.promises.slice(0, 3);
  ls['promi_state'] = JSON.stringify(st);
  const fautes = await juger(
    page,
    ['encre', 'touffe', 'mosaique', 'ritournelle', 'brouillamini'],
    ls,
    'courir dimanche',
    'evol',
    'evol',
  );
  expect(fautes).toEqual([]);
});

test('sur une Toile pleine (25 paroles relues de la sauvegarde), une dalle arrive puis part : aucun rendu de dalle hors du moteur', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // redteam_pleine.py : 25 paroles (banc-etats/etat-25.json), sous Pochade, Touffe, Ritournelle (en dur) — A les comptes, D et E les durées
  const fautes = await juger(page, ['encre', 'touffe', 'ritournelle'], etatBanc(25), 'tenir bon', 'pleine', 'pleine');
  expect(fautes).toEqual([]);
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_decoupe (Tom, 22 sept. 2026 ; v29, v34) — « Une dalle est peinte par le moteur, dans sa cellule, avec son propre contour, à sa
 * taille finale. Jamais une image rognée, jamais un canevas recadré, jamais un morceau de Toile. »
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

/** le moteur : le bloc de la Toile dans promi-moteur.js, de `var host=document.getElementById('toileCv')` au premier `})();` qui suit (les
 *  blocs des mondes, avant lui, restent HORS du moteur : redteam_decoupe.py, `bornes_moteur`). Lu sur le fichier repris, octet pour octet. */
const MOTEUR = readFileSync(
  join(import.meta.dirname, '..', '..', 'src', 'moteur', 'repris', 'promi-moteur.js'),
  'utf8',
).split('\n');
const MOTEUR_LO = MOTEUR.findIndex((l) => l.includes("var host=document.getElementById('toileCv')")) + 1;
const MOTEUR_HI = MOTEUR.findIndex((l, i) => i >= MOTEUR_LO - 1 && l.startsWith('})();')) + 1;

/**
 * Le piège (redteam_decoupe.py, PIEGE) : `drawImage`, `getImageData`, `putImageData`, `createPattern`, `toDataURL` enveloppés avant que l'app
 * ne charge ; un canevas rendu par `Toile.dalleTrame` porte une DALLE, `#toileCv` et ce que rendent `renderTo`, `preview`, `repaint`,
 * `repaintWorld` la TOILE, et ce sur quoi l'un d'eux est posé les PORTE. Dans WebKit, le moteur (injecté en ligne) paraît dans la pile sous
 * l'adresse de la page : `http://127.0.0.1:5180/:<ligne>:<colonne>`, aux lignes du fichier repris.
 */
const PIEGE_DECOUPE = (lo: number, hi: number): string => `(() => {
  const J = window.__decoupe = { log: [], moteur: {}, on: true, ecran: 'chargement' };
  const RE = new RegExp(location.origin.replace(/[.]/g, '\\\\.') + '/(?:\\\\?[^:\\\\s]*)?:(\\\\d+):\\\\d+');
  const ligne = () => { for (const f of String(new Error().stack).split('\\n')) { const m = f.match(RE); if (m) return +m[1]; if (/\\/assets\\//.test(f)) return -1; } return 0; };
  const dansMoteur = (l) => l >= ${String(lo)} && l <= ${String(hi)};
  const marque = (c) => { if (!c) return null; if (c.id === 'toileCv') return 'TOILE'; return (c.__dalle || c.__enCours) ? 'DALLE' : c.__toile ? 'TOILE' : c.__porte ? 'PORTE' : null; };
  const note = (k, l, d) => { if (!J.on) return; if (dansMoteur(l)) { J.moteur[k] = (J.moteur[k] || 0) + 1; return; } J.log.push(Object.assign({ k, l, e: J.ecran }, d)); };
  const echelle = (ctx) => { try { const t = ctx.getTransform(); return [Math.hypot(t.a, t.b), Math.hypot(t.c, t.d)]; } catch (_) { return [1, 1]; } };
  const P = CanvasRenderingContext2D.prototype;
  const dI = P.drawImage;
  P.drawImage = function (src) {
    const n = arguments.length, m = (src instanceof HTMLCanvasElement) ? marque(src) : null;
    if (m && this.canvas !== src) {
      const l = ligne(), sw = src.width, sh = src.height; let cw, ch, dw, dh;
      if (n >= 9) { cw = arguments[3]; ch = arguments[4]; dw = arguments[7]; dh = arguments[8]; } else if (n >= 5) { cw = sw; ch = sh; dw = arguments[3]; dh = arguments[4]; } else { cw = sw; ch = sh; dw = sw; dh = sh; }
      const [ex, ey] = echelle(this), rw = dw * ex, rh = dh * ey;
      const d = { m, n, src: [sw, sh], coupe: [+cw, +ch], rendu: [+rw.toFixed(1), +rh.toFixed(1)], cible: String((this.canvas && (this.canvas.id || this.canvas.className)) || '?').slice(0, 40) };
      const entiere = Math.abs(cw - sw) < 0.5 && Math.abs(ch - sh) < 0.5, memeTaille = Math.abs(rw - cw) <= 1 && Math.abs(rh - ch) <= 1;
      if (m === 'TOILE' && ((n >= 9 && !entiere) || !memeTaille)) note('D·fragment', l, d); else if (n >= 9) note('A·découpe', l, d); else if (!memeTaille) note('B·redimension', l, d); else note('ok·pose', l, d);
      if (this.canvas && this.canvas.id !== 'toileCv') this.canvas.__porte = 1;
    }
    return dI.apply(this, arguments);
  };
  const gI = P.getImageData; P.getImageData = function () { const r = gI.apply(this, arguments), m = marque(this.canvas); if (m) { r.__dalle = 1; note('C·getImageData', ligne(), { m }); } return r; };
  const pI = P.putImageData; P.putImageData = function (im) { const m = marque(this.canvas); if (m || (im && im.__dalle)) note('C·putImageData', ligne(), { m: m || 'IMAGEDATA' }); return pI.apply(this, arguments); };
  const cP = P.createPattern; P.createPattern = function (src) { const m = (src instanceof HTMLCanvasElement) ? marque(src) : null; if (m) note('E·motif', ligne(), { m }); return cP.apply(this, arguments); };
  const tD = HTMLCanvasElement.prototype.toDataURL; HTMLCanvasElement.prototype.toDataURL = function () { const m = marque(this); if (m) note('E·image', ligne(), { m }); return tD.apply(this, arguments); };
  const PEINT = { dalleTrame: '__dalle', renderTo: '__toile', preview: '__toile', repaint: '__toile', repaintWorld: '__toile' };
  const env = (nom, f) => { if (typeof f !== 'function' || !PEINT[nom] || f.__env) return f;
    const w = function (cv) { let r; let avant = null; try { avant = window.Toile && window.Toile.mondeCourant ? window.Toile.mondeCourant() : null; } catch (_) {}
      try { if (cv && nom === 'dalleTrame') cv.__enCours = 1; r = f.apply(this, arguments); } finally { try { if (cv) cv.__enCours = 0; } catch (_) {} }
      // H · le monde (v34) : « tout suit le Studio » — hors de l'Aura (lot 5), une dalle se peint dans le monde COURANT, sauf un aperçu qui le déclare (« courant »)
      try { if (nom === 'dalleTrame' && r && cv.__dalleInfo && cv.__dalleInfo.monde && !cv.__dalleInfo.courant && avant) { const M = cv.__dalleInfo.monde;
        if (avant.m !== M.m || avant.p !== M.p || (+avant.h || 0) !== (+M.h || 0)) note('H·monde', ligne(), { m: 'MONDE', cible: 'Studio ' + [avant.m, avant.p, +avant.h || 0].join('/') + ' · peinte ' + [M.m, M.p, +M.h || 0].join('/') }); } } catch (_) {}
      try { if (cv && (nom !== 'dalleTrame' || r)) { cv[PEINT[nom]] = 1; if (nom === 'dalleTrame') { cv.__toile = 0; cv.__porte = 0; } } } catch (_) {}
      return r; };
    w.__env = 1; return w; };
  let T; Object.defineProperty(window, 'Toile', { configurable: true, get() { return T; },
    set(v) { if (v && typeof v === 'object') { for (const k in v) v[k] = env(k, v[k]); T = new Proxy(v, { set(o, k, f) { o[k] = env(k, f); return true; } }); } else T = v; } });
})()`;
/** G · un canevas visible qui porte une dalle, affiché par le CSS à une autre taille que celle où il a été peint (3 % près) */
const AFFICHAGE = `(() => { const J = window.__decoupe, D = document.getElementById('device').getBoundingClientRect(), sc = D.width / 390, dpr = window.devicePixelRatio || 1;
  for (const c of document.querySelectorAll('canvas')) { if (!(c.__dalle || c.__porte) || c.id === 'toileCv') continue; const r = c.getBoundingClientRect(); if (r.width < 6 || r.height < 6) continue;
    if (r.right < D.left || r.left > D.right || r.bottom < D.top || r.top > D.bottom) continue;
    let e = c, vu = true; while (e && e !== document.body) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) { vu = false; break; } e = e.parentElement; }
    if (!vu) continue; const aff = (r.width / sc) * dpr; if (Math.abs(aff / c.width - 1) > 0.03) J.log.push({ k: 'G·affichage', l: 0, e: J.ecran, src: [c.width, c.height], rendu: [Math.round(aff)], cible: (c.id || String(c.className)).slice(0, 40) }); } })()`;

test("une dalle n'est jamais une image découpée (22 sept., v29) : hors du moteur, aucun canevas de dalle ou de Toile n'est rogné, redimensionné, relu", async ({
  browser,
}) => {
  expect(MOTEUR_LO, 'le bloc du moteur est trouvé dans le fichier repris').toBeGreaterThan(1000);
  expect(MOTEUR_HI).toBeGreaterThan(MOTEUR_LO);
  const prises: Array<Record<string, unknown>> = [];
  let moteur: Record<string, number> = {};
  for (const theme of ['clair', 'sombre'] as const) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await ctx.addInitScript(PIEGE_DECOUPE(MOTEUR_LO, MOTEUR_HI));
    const page = await ctx.newPage();
    await ouvrir(page, { ...etatBanc(25), promi_theme: theme === 'clair' ? 'light' : 'dark' });
    const ecran = (e: string): Promise<unknown> =>
      page.evaluate(`window.__decoupe.ecran = ${JSON.stringify(theme + ' · ' + e)}`);
    // H : le monde COURANT diffère du monde de plantation (les paroles du banc sont plantées sous Pochade), sinon un oubli ne se voit pas
    await page.evaluate("window.__promi.magasin.choisirMonde('pixel')");
    await posee(page);
    await ecran('accueil');
    await page.waitForTimeout(800);
    if (sonde('decoupe-fragment'))
      // un fragment de Toile recopié hors du moteur (la faute D du juge)
      await page.evaluate(
        "(() => { const c = document.createElement('canvas'); c.width = 100; c.height = 100; c.getContext('2d').drawImage(document.getElementById('toileCv'), 0, 0, 200, 200, 0, 0, 100, 100); })()",
      );
    if (sonde('decoupe-affichage'))
      // une dalle seule affichée par le CSS à une autre taille que celle où elle a été peinte (la faute G, v29)
      await page.evaluate(`(() => { const c = document.createElement('canvas'); const p = Toile_lecture().graines.find((g) => g.pid != null);
        Toile.dalleTrame(c, p.pid, 1); c.style.cssText = 'position:absolute;left:20px;top:200px;z-index:99;width:' + (c.width * 2) + 'px;height:' + (c.height * 2) + 'px';
        document.getElementById('device').appendChild(c); })()`);
    await page.evaluate(AFFICHAGE);
    await ecran('menu du +');
    const plus = (await page.evaluate(
      "(() => { const b = document.getElementById('createBtn').getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; })()",
    )) as [number, number];
    await page.mouse.click(plus[0], plus[1]);
    await page.waitForTimeout(600);
    await page.evaluate(AFFICHAGE);
    await page.mouse.click(plus[0], plus[1]);
    await ecran('la vue glissée, le symbole « recadrer »');
    await page.mouse.move(195, 420);
    await page.mouse.down();
    await page.mouse.move(150, 380, { steps: 8 });
    await page.mouse.up();
    await page.waitForTimeout(900);
    await page.evaluate(AFFICHAGE);
    await page.evaluate('window.__promi.facade.recadrer()');
    await ecran('une parole plantée puis retirée');
    const avant = await etatActuel(page);
    await importer(page, (await etatAvec(page, 'tenir bon')).etat);
    await posee(page);
    await page.evaluate(AFFICHAGE);
    await importer(page, avant);
    await posee(page);
    await ecran('un autre monde, puis le thème basculé');
    await page.evaluate("window.__promi.magasin.choisirMonde('touffe')");
    await posee(page);
    await page.evaluate(
      `window.__promi.magasin.choisirTheme(${JSON.stringify(theme === 'clair' ? 'sombre' : 'clair')})`,
    );
    await page.waitForTimeout(800);
    await page.evaluate(AFFICHAGE);
    const J = (await page.evaluate('({ log: window.__decoupe.log, moteur: window.__decoupe.moteur })')) as {
      log: Array<Record<string, unknown>>;
      moteur: Record<string, number>;
    };
    prises.push(...J.log.filter((x) => !String(x['k']).startsWith('ok')));
    moteur = { ...moteur, ...J.moteur };
    await ctx.close();
  }
  // ce que le moteur fait chez lui est relevé, pas jugé (sa propre cellule : getImageData, putImageData, le recadrage 1:1)
  test.info().annotations.push({ type: 'moteur (relevé)', description: JSON.stringify(moteur) });
  expect(
    prises,
    'aucune prise hors du moteur (familles A à H ; la dette est soldée depuis v29 : decoupe-dette.json vide)',
  ).toEqual([]);
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_dalle_figee (Q213, 13 sept. 2026) — « une dalle garde sa couleur comme elle garde son monde ».
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

/** les couleurs des dalles, par TITRE ET PERSONNE (jamais par id : redteam_dalle_figee.py), une fois stables (deux lectures égales) */
async function couleurs(page: Page): Promise<Record<string, string | null>> {
  return (await page.evaluate(`(async () => { const lit = () => { const o = {}; for (const p of promises) if (!p.draft && !p.req) o[p.title + '|' + p.who] = Toile.colorOf(p.id); return JSON.stringify(o); };
    let a = lit(); for (let i = 0; i < 40; i++) { await new Promise((f) => setTimeout(f, 250)); const b = lit(); if (b === a) return JSON.parse(b); a = b; } return JSON.parse(a); })()`)) as Record<
    string,
    string | null
  >;
}

// la couleur se lit sous une palette où elle dépend de la dalle (sous Ingénu, la palette par défaut, elle dit la nature : v17) — Irascible
const PALETTE_FIGEE = 'irascible';
async function ouvrirFigee(
  browser: Browser,
  ls: Ls,
  theme: string,
  avant = '',
): Promise<{ page: Page; c: Record<string, string | null> }> {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  await ouvrir(page, { ...ls, promi_theme: theme }, avant ? { avant } : {});
  // la palette passe à la Toile par l'import (au lot 1 la Toile ne suit pas `choisirPalette` seule : le Studio, qui l'appellera, est au lot 7)
  await page.evaluate(`window.__promi.magasin.choisirPalette(${JSON.stringify(PALETTE_FIGEE)}, 0)`);
  await importer(page, await etatActuel(page));
  await posee(page);
  expect(await page.evaluate('Toile.getPalette()'), 'la Toile est sous Irascible').toBe(PALETTE_FIGEE);
  return { page, c: await couleurs(page) };
}

test('une dalle garde sa couleur (Q213) : la même à chaque ouverture (3 pages × 2 thèmes), et après une resynchronisation', async ({
  browser,
}) => {
  const ls = etatBanc(25);
  const hasard = sonde('dalle-hasard');
  // la sonde : la version d'avant Q213 — la couleur d'une dalle tirée au hasard à chaque chargement (`cc()`, `Math.random`)
  const tirage = (l: Ls): Ls => {
    const st = JSON.parse(l['promi_state']!) as { promises: Array<Record<string, unknown>> };
    for (const p of st.promises) p['dalle'] = { ci: Math.floor(Math.random() * 4), lit: Math.floor(Math.random() * 3) };
    return { ...l, promi_state: JSON.stringify(st) };
  };
  // A · trois pages neuves × deux thèmes : la même couleur pour chaque parole
  const releves: Array<[string, Record<string, string | null>]> = [];
  for (const th of ['light', 'dark'])
    for (let k = 0; k < 3; k++) {
      const lsx = hasard ? tirage(ls) : ls;
      const { page, c } = await ouvrirFigee(browser, lsx, th);
      releves.push([`${th}·${String(k)}`, c]);
      if (th === 'light' && k === 0) {
        // C · après une resynchronisation (`Toile.sync`, qui refait toutes les dalles) : les mêmes couleurs
        await page.evaluate('window.__promi.facade.planterTout()');
        await posee(page);
        releves.push(['resynchronisée', await couleurs(page)]);
      }
      await page.context().close();
    }
  const ref = releves[0]![1];
  const ecarts: string[] = [];
  for (const [nom, c] of releves.slice(1))
    for (const [k, v] of Object.entries(c))
      if (ref[k] !== v) ecarts.push(`${nom} ${k} : ${String(ref[k])} ≠ ${String(v)}`);
  expect(Object.keys(ref).length, 'au moins dix dalles').toBeGreaterThanOrEqual(10);
  expect(
    Object.entries(ref).filter(([, v]) => v == null),
    'chaque dalle a une couleur',
  ).toEqual([]);
  expect(ecarts, 'la même couleur à chaque ouverture (3 × 2 thèmes) et après une resynchronisation').toEqual([]);
});

test('une dalle plantée garde sa couleur (Q213), sauvée puis rechargée', async ({ browser }) => {
  // CORRIGÉ (C-326, 20 nov. 2026) : la façade rend au magasin la couleur que le moteur fige (`p.dalle`, `NUEDALLE`) avec la place, et pose
  // `_dalleDeCle` (la couleur tirée du titre et de la personne, la règle du prototype, app.html ≈ l. 3308). Au rechargement, la couleur
  // retirée tombe parfois sur la même (le tirage du moteur est amorcé) : le test lit aussi ce que garde le magasin.
  const { page } = await ouvrirFigee(browser, etatBanc(25), 'light');
  // la sonde : la version d'avant la correction — la couleur figée n'est pas rendue au magasin
  if (sonde('dalle-perdue'))
    await page.evaluate(() => {
      type Pl = Array<{ id: number; place: unknown; dalle?: unknown }>;
      const m = (window as unknown as { __promi: { magasin: { noterPlaces(p: Pl, d?: unknown): void } } }).__promi
        .magasin;
      const f = m.noterPlaces.bind(m);
      m.noterPlaces = (p: Pl) => {
        f(p.map((x) => ({ id: x.id, place: x.place })));
      };
    });
  const { etat } = await etatAvec(page, 'juge dalle figée');
  await importer(page, etat);
  await posee(page);
  const c1 = (await couleurs(page))['juge dalle figée|moi'];
  expect(c1, 'la parole plantée a une couleur').toBeTruthy();
  // la couleur que le moteur vient de figer (`p.dalle`, sur la parole qu'il lit) est GARDÉE par le magasin, donc sauvée avec la parole (Q213)
  const figee = (await page.evaluate(
    `(() => { const q = promises.find((p) => p.title === 'juge dalle figée'); const m = window.__promi.magasin.etat().paroles.find((p) => p.title === 'juge dalle figée');
      return { moteur: q && q.dalle ? JSON.stringify(q.dalle) : null, magasin: m && (m.dalle || (m.suite && m.suite.dalle)) ? JSON.stringify(m.dalle || m.suite.dalle) : null }; })()`,
  )) as { moteur: string | null; magasin: string | null };
  expect(figee.moteur, 'le moteur a figé la couleur de la parole plantée').not.toBeNull();
  expect(figee.magasin, 'le magasin garde la couleur figée').toBe(figee.moteur);
  await rouvrir(page);
  const c3 = (await couleurs(page))['juge dalle figée|moi'];
  expect(c3, 'plantée, sauvée puis rechargée : la même couleur').toBe(c1);
  await page.context().close();
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_clair_sombre (v146, C-131) — « EXACTEMENT la même Toile en clair et en sombre (mêmes dalles, même disposition, mêmes formes,
 * mêmes tailles, mêmes graines), dans les 20 mondes […]. Seules les couleurs du thème changent. » On compare la GÉOMÉTRIE.
 * Le Studio (D) et Partager (E) : au lot 7 et au lot 8.
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

const TOL_CS = 0.001; // « identique au point près » : le millième de point (redteam_clair_sombre.py, TOL)
type Lecture = {
  vue: number[];
  g: Array<[number | null, string, number, number, number, string | null]>;
  carte: string;
  rangs: string | null;
  clair: boolean;
  monde: string;
};
/** la géométrie de la Toile : graines (parole, place, poids, boîte), vue, la carte du toucher (à qui appartient chaque point d'une grille de 6 pt), le rang de gris de chaque cellule vide */
const LIT_CS = `(() => { const L = Toile_lecture(), r = (v) => Math.round(v * 10000) / 10000;
  const g = L.graines.map((s) => [s.pid, s.kind, r(s.x), r(s.y), r(s.w), s.boite ? JSON.stringify(s.boite, (k, v) => (typeof v === 'number' ? r(v) : v)) : null]);
  const cv = document.getElementById('toileCv'); let carte = '';
  for (let y = 3; y < cv.clientHeight; y += 6) for (let x = 3; x < cv.clientWidth; x += 6) { let h = null; try { h = Toile.hit(x, y); } catch (e) {} carte += (h ? (h.pid != null ? 'p' + h.pid : 'n' + (h.nuee || '')) : '.') + ','; }
  let rangs = null; try { rangs = window.Toile_grisRangs ? Toile_grisRangs().join(',') : null; } catch (e) {}
  return { vue: [r(L.vue.s), r(L.vue.ox), r(L.vue.oy)], g, carte, rangs, clair: document.getElementById('device').classList.contains('light'), monde: Toile.getTheme() }; })()`;
/** deux boîtes de dalle (le JSON du moteur), comparées au millième de point (comme les graines) */
function memeBoite(a: string | null, b: string | null): boolean {
  if (a === b) return true;
  if (a == null || b == null) return false;
  const nombres = (t: string): number[] => (t.match(/-?\d+(?:\.\d+)?(?:e-?\d+)?/g) ?? []).map(Number);
  const A = nombres(a);
  const B = nombres(b);
  return (
    a.replace(/-?\d+(?:\.\d+)?(?:e-?\d+)?/g, '#') === b.replace(/-?\d+(?:\.\d+)?(?:e-?\d+)?/g, '#') &&
    A.every((v, i) => Math.abs(v - B[i]!) <= TOL_CS)
  );
}
function ecartCs(a: Lecture, b: Lecture): string | null {
  if (a.g.length !== b.g.length) return `graines ${String(a.g.length)} / ${String(b.g.length)}`;
  let m = 0;
  let boites = 0;
  for (let i = 0; i < a.g.length; i++) {
    const x = a.g[i]!;
    const y = b.g[i]!;
    if (x[0] !== y[0] || x[1] !== y[1])
      return `ordre ${JSON.stringify(x.slice(0, 2))} / ${JSON.stringify(y.slice(0, 2))}`;
    m = Math.max(m, Math.abs(x[2] - y[2]), Math.abs(x[3] - y[3]), Math.abs(x[4] - y[4]));
    if (!memeBoite(x[5], y[5])) boites++;
  }
  const vue = Math.max(...a.vue.map((v, i) => Math.abs(v - b.vue[i]!)));
  const ca = a.carte.split(',');
  const cb = b.carte.split(',');
  const carte = ca.length === cb.length ? ca.filter((v, i) => v !== cb[i]).length : -1;
  const gris =
    a.rangs != null && b.rangs != null ? a.rangs.split(',').filter((v, i) => v !== b.rangs!.split(',')[i]).length : -1;
  if (m <= TOL_CS && vue <= TOL_CS && boites === 0 && carte === 0 && gris === 0) return null;
  return `graines ${m.toFixed(4)} · vue ${vue.toFixed(4)} · boîtes ${String(boites)} · carte ${String(carte)} · gris ${String(gris)}`;
}
/** la Toile VRAIMENT posée : on relance le moteur jusqu'à ce qu'une relance ne change plus rien (redteam_clair_sombre.py, `pose_ferme`) */
async function poseeFerme(page: Page): Promise<Lecture> {
  // la vie au repos (C-028) coupée le temps de lire : un mouvement de repos change une boîte pendant une ou deux secondes, et la lecture
  // juge la GÉOMÉTRIE de la Toile (clair contre sombre), pas sa respiration (le banc de rendu le fait de même, `_vivantOff`, C-114)
  await page.evaluate('window._vivantOff = true');
  await posee(page);
  let a = (await page.evaluate(LIT_CS)) as Lecture;
  for (let i = 0; i < 4; i++) {
    await page.evaluate('Toile.redraw()');
    await posee(page);
    const b = (await page.evaluate(LIT_CS)) as Lecture;
    if (!ecartCs(a, b)) return b;
    a = b;
  }
  return a;
}
const theme = (page: Page, t: 'clair' | 'sombre'): Promise<unknown> =>
  page.evaluate(`window.__promi.magasin.choisirTheme(${JSON.stringify(t)})`);

for (const n of [1, 5, 25, 50])
  test(`la même Toile en clair et en sombre (C-131), ${String(n)} parole(s) : à la bascule, dans les vingt mondes, ni une graine, ni la vue, ni une boîte, ni la carte du toucher, ni un gris ne changent`, async ({
    page,
  }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await ouvrir(page, { ...etatBanc(n), promi_theme: 'light' });
    if (sonde('cs-bascule'))
      // la Toile dépend du thème : en sombre, l'app replante la Toile sans sa première parole (et la rend entière au retour en clair :
      // le témoin clair → clair reste juste, c'est la bascule qui est fausse)
      await page.evaluate(`(() => { const tout = Toile_lecture().graines.filter((g) => g.pid != null).map((g) => g.pid);
        window.__promi.magasin.abonner((e, a) => { if (a !== 'choisirTheme') return; Toile.sync(e.reglages.theme === 'sombre' ? tout.slice(1) : tout); }); })()`);
    expect(await page.evaluate('promises.filter((p) => !p.draft).length'), 'la Toile relue porte ses paroles').toBe(n);
    const mauvais: string[] = [];
    for (const m of MONDES) {
      await page.evaluate(`window.__promi.magasin.choisirMonde(${JSON.stringify(m)})`);
      const c1 = await poseeFerme(page);
      await theme(page, 'sombre');
      await posee(page);
      const s = (await page.evaluate(LIT_CS)) as Lecture;
      await theme(page, 'clair');
      await posee(page);
      const c2 = (await page.evaluate(LIT_CS)) as Lecture;
      const e1 = ecartCs(c1, s);
      const e2 = ecartCs(c1, c2);
      // le témoin (clair → clair) varie lui-même : la Toile de ce monde ne se répète pas sur cette machine (l'intégration continue,
      // WebKit sans carte graphique) — non jugé, nommé ; sinon le moindre écart clair → sombre est une faute
      if (e2) {
        test
          .info()
          .annotations.push({ type: 'non jugé', description: `${m} : le témoin clair/clair varie (${String(e2)})` });
        continue;
      }
      if (!c1.clair || s.clair || c1.monde !== m || e1)
        mauvais.push(
          `${m} : clair/sombre ${String(e1)} · clair/clair ${String(e2)} (monde ${c1.monde}, ${c1.clair ? 'clair' : 'sombre'} → ${s.clair ? 'clair' : 'sombre'})`,
        );
      if (mauvais.length && process.env['PROMI_SONDE']) break; // sous une sonde, le premier monde pris suffit
    }
    expect(mauvais).toEqual([]);
  });

test("la même Toile en clair et en sombre (C-131) : l'app ouverte en sombre montre la Toile de l'app ouverte en clair (5 et 25 paroles, le monde sauvé et Ritournelle)", async ({
  browser,
}) => {
  const ouverture = async (n: number, t: 'light' | 'dark', monde: string | null): Promise<Lecture> => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    await ouvrir(page, { ...etatBanc(n), promi_theme: t });
    if (sonde('cs-ouverture') && t === 'dark')
      // l'app ouverte en sombre plante une autre Toile (sans sa première parole)
      await page.evaluate(
        'Toile.sync(Toile_lecture().graines.filter((g) => g.pid != null).map((g) => g.pid).slice(1))',
      );
    if (monde) await page.evaluate(`window.__promi.magasin.choisirMonde(${JSON.stringify(monde)})`);
    const l = await poseeFerme(page);
    await ctx.close();
    return l;
  };
  const mauvais: string[] = [];
  for (const n of [5, 25])
    for (const monde of [null, 'ritournelle']) {
      const c = await ouverture(n, 'light', monde);
      const s = await ouverture(n, 'dark', monde);
      const e = ecartCs(c, s);
      if (e) {
        // les témoins : une seconde ouverture en clair, une seconde en sombre ; si l'une ne se répète pas, la Toile ne se répète pas sur
        // cette machine (hors du Mac, 25 paroles ne se posent pas toujours au même point) — non jugé, nommé ; les deux se répètent et
        // diffèrent l'une de l'autre : c'est la faute
        const c2 = await ouverture(n, 'light', monde);
        const t = ecartCs(c, c2);
        const s2 = t ? null : await ouverture(n, 'dark', monde);
        const u = s2 ? ecartCs(s, s2) : null;
        if (t || u) {
          test.info().annotations.push({
            type: 'non jugé',
            description: `${String(n)} paroles, ${monde ?? c.monde} : le témoin ${t ? 'clair/clair' : 'sombre/sombre'} varie (${String(t ?? u)})`,
          });
          continue;
        }
      }
      if (!c.clair || s.clair || e) mauvais.push(`${String(n)} paroles, ${monde ?? c.monde} : ${String(e)}`);
    }
  expect(mauvais).toEqual([]);
});

test('la même Toile en clair et en sombre (C-131) : une dalle rendue seule a la même silhouette, dans les vingt mondes (3 paroles chacun)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await ouvrir(page, { ...etatBanc(5), promi_theme: 'light' });
  if (sonde('cs-dalle'))
    // en sombre, la dalle seule est rendue plus petite (sa silhouette dépend du thème)
    await page.evaluate(`(() => { const o = Toile.dalleTrame; Toile.dalleTrame = function (cv, id, k, ...a) {
      return o.call(this, cv, id, document.getElementById('device').classList.contains('light') ? k : k * 0.9, ...a); }; })()`);
  const mauvais: string[] = [];
  for (const m of MONDES) {
    await page.evaluate(`window.__promi.magasin.choisirMonde(${JSON.stringify(m)})`);
    await posee(page);
    // horloge figée le temps des trois rendus (redteam_clair_sombre.py, C) ; le thème passe par le magasin, comme l'app le fait
    const r =
      (await page.evaluate(`(() => { const ids = promises.filter((p) => !p.draft).slice(0, 3).map((p) => p.id), T = performance.now(), vrai = performance.now; const out = [];
      const masque = (id) => { const cv = document.createElement('canvas'); try { Toile.dalleTrame(cv, id, 1); } catch (e) { return null; }
        if (!cv.width || !cv.height) return { w: 0, h: 0, a: null }; const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data, a = new Uint8Array(cv.width * cv.height); let n = 0;
        for (let i = 0; i < a.length; i++) if (d[i * 4 + 3] > 32) { a[i] = 1; n++; } return { w: cv.width, h: cv.height, a, n }; };
      const iou = (p, q) => { if (!p || !q || !p.a || !q.a || p.w !== q.w || p.h !== q.h) return 0; let i = 0, u = 0; for (let k = 0; k < p.a.length; k++) { if (p.a[k] && q.a[k]) i++; if (p.a[k] || q.a[k]) u++; } return u ? i / u : 1; };
      const M = window.__promi.magasin;
      try { performance.now = () => T;
        for (const id of ids) { const c1 = masque(id); M.choisirTheme('sombre'); const s = masque(id); M.choisirTheme('clair'); const c2 = masque(id);
          out.push({ id, clair: c1 && [c1.w, c1.h], sombre: s && [s.w, s.h], cs: iou(c1, s), cc: iou(c1, c2) }); }
      } finally { performance.now = vrai; }
      return out; })()`)) as Array<{
        id: number;
        clair: number[] | null;
        sombre: number[] | null;
        cs: number;
        cc: number;
      }>;
    const cs = Math.min(...r.map((x) => x.cs));
    const cc = Math.min(...r.map((x) => x.cc));
    // la même silhouette : mêmes dimensions, un recouvrement au moins celui du témoin clair/clair (à 0,5 % près), et 0,985 au moins
    const ok =
      r.length === 3 &&
      r.every((x) => x.clair && x.sombre && x.clair[0] === x.sombre[0] && x.clair[1] === x.sombre[1]) &&
      cs >= Math.min(cc, 1) - 0.005 &&
      cs >= 0.985;
    if (!ok)
      mauvais.push(
        `${m} : clair/sombre ${cs.toFixed(4)} (témoin ${cc.toFixed(4)}) ${JSON.stringify(r.map((x) => [x.clair, x.sombre]))}`,
      );
  }
  expect(mauvais).toEqual([]);
});

/** la part (en %) des pixels de la Toile (y 110 → 700) qui changent de plus de 12 niveaux (somme des trois canaux) entre deux captures */
function partChangee(a: Buffer, b: Buffer): number {
  const A = PNG.sync.read(a);
  const B = PNG.sync.read(b);
  if (A.width !== B.width || A.height !== B.height) return 100;
  const k = A.width / 390;
  let n = 0;
  let t = 0;
  for (let y = Math.round(110 * k); y < Math.round(700 * k); y++)
    for (let x = 0; x < A.width; x++) {
      const i = (y * A.width + x) * 4;
      t++;
      if (
        Math.abs(A.data[i]! - B.data[i]!) +
          Math.abs(A.data[i + 1]! - B.data[i + 1]!) +
          Math.abs(A.data[i + 2]! - B.data[i + 2]!) >
        12
      )
        n++;
    }
  return (100 * n) / t;
}

test('la même Toile en clair et en sombre (C-131) : après un aller-retour clair → sombre → clair, la Toile est la même image, cellules vides comprises (dix mondes)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await ouvrir(page, { ...etatBanc(5), promi_theme: 'light' });
  if (sonde('cs-image'))
    // la bascule change les couleurs de la Toile pour de bon (la version d'avant : les gris retirés au hasard, `reGray`)
    await page.evaluate(
      `window.__promi.magasin.abonner((e, a) => { if (a === 'choisirTheme') Toile.setHue((Toile.getHue() + 40) % 360); })`,
    );
  // le plateau et la barre ne comptent pas : on ne regarde que la Toile (y 110 → 700)
  const mauvais: string[] = [];
  for (const m of [
    'encre',
    'touffe',
    'mosaique',
    'braille',
    'pixel',
    'terrazzo',
    'gravure',
    'sillons',
    'chamade',
    'halin',
  ]) {
    await page.evaluate(`window.__promi.magasin.choisirMonde(${JSON.stringify(m)})`);
    await poseeFerme(page);
    const c1 = await page.screenshot();
    await page.waitForTimeout(600);
    const temoin = partChangee(c1, await page.screenshot());
    await theme(page, 'sombre');
    await posee(page);
    const s1 = await page.screenshot();
    await theme(page, 'clair');
    await posee(page);
    const c2 = await page.screenshot();
    await theme(page, 'sombre');
    await posee(page);
    const s2 = await page.screenshot();
    await theme(page, 'clair');
    await posee(page);
    const dc = partChangee(c1, c2);
    const ds = partChangee(s1, s2);
    if (dc > temoin + 0.5 || ds > temoin + 0.5)
      mauvais.push(`${m} : clair ${dc.toFixed(1)} % · sombre ${ds.toFixed(1)} % (témoin ${temoin.toFixed(1)} %)`);
  }
  expect(mauvais).toEqual([]);
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_toucher (v133, C-058 ; v139, C-088) — « Sous chaque monde, toucher une dalle ouvre sa fiche. Vingt mondes, trois dalles par
 * monde. » La fiche est au lot 3a : on juge que la vraie app DEMANDE la fiche de CETTE parole, et rien d'autre.
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

/** les trois dalles de parole les plus « au cœur » : `Toile.hit` n'est qu'un POINTEUR (où toucher) — le verdict est la demande de l'app */
const POINTS = `(() => { const cv = document.getElementById('toileCv'), r = cv.getBoundingClientRect(), dv = document.getElementById('device').getBoundingClientRect(), kx = cv.clientWidth / r.width, ky = cv.clientHeight / r.height;
  const G = {}, pas = 6;
  for (let y = dv.top + 130; y < dv.bottom - 150; y += pas) for (let x = dv.left + 12; x < dv.right - 12; x += pas) { let h = null; try { h = Toile.hit((x - r.left) * kx, (y - r.top) * ky); } catch (e) {} if (h && h.pid != null) (G[h.pid] = G[h.pid] || []).push([x, y]); }
  const out = []; for (const pid of Object.keys(G)) { const L = G[pid]; if (L.length < 12) continue; const set = new Set(L.map((p) => p[0] + ',' + p[1]));
    let best = null, bs = -1; for (const p of L) { let s = 0; for (let a = -3; a <= 3; a++) for (let b = -3; b <= 3; b++) if (set.has(p[0] + a * pas + ',' + (p[1] + b * pas))) s++; if (s > bs) { bs = s; best = p; } }
    if (promises.some((q) => q.id === +pid)) out.push({ pid: +pid, x: best[0], y: best[1], coeur: bs }); }
  out.sort((a, b) => b.coeur - a.coeur); return { pts: out.slice(0, 3), theme: Toile.getTheme() }; })()`;
/** toucher (souris : un pointeur, comme le doigt pour l'app), puis la demande notée dans les 3 s, ou rien */
async function toucherEtLire(page: Page, x: number, y: number, attendre?: string): Promise<Dem[]> {
  const n0 = (await page.evaluate('window.__dem.length')) as number;
  await page.mouse.click(x, y);
  await page
    .waitForFunction(attendre ?? `window.__dem.length > ${String(n0)}`, undefined, { timeout: 3000 })
    .catch(() => {});
  await page.waitForTimeout(450); // ni un second toucher (moins de 320 ms : le double toucher), ni une demande en retard
  const d = ((await demandes(page)) as Dem[]).slice(n0);
  await fermerFiche(page);
  return d;
}

test('toucher une dalle demande SA fiche, sous les vingt mondes (C-058) : trois dalles chacun, rien ne couvre la Toile au point touché', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await ouvrir(page, sansBandeau(etatBanc(25)));
  const fautes: string[] = [];
  for (const m of MONDES) {
    await page.evaluate(`window.__promi.magasin.choisirMonde(${JSON.stringify(m)})`);
    await posee(page);
    const P = (await page.evaluate(POINTS)) as { pts: Array<{ pid: number; x: number; y: number }>; theme: string };
    if (P.theme !== m || P.pts.length < 3) {
      fautes.push(`${m} : monde ${P.theme}, ${String(P.pts.length)} dalle(s) à toucher`);
      continue;
    }
    if (sonde('toucher-mauvaise'))
      // la mauvaise fiche : le toucher lit la parole d'à côté
      await page.evaluate(
        '(() => { const o = Toile.hit; Toile.hit = function (x, y) { const h = o.call(this, x, y); return h && h.pid != null ? { ...h, pid: h.pid + 1 } : h; }; })()',
      );
    for (const q of P.pts) {
      const dessus = (await page.evaluate(
        `(document.elementFromPoint(${String(q.x)}, ${String(q.y)}) || {}).id`,
      )) as string;
      const d = await toucherEtLire(page, q.x, q.y);
      if (dessus !== 'toileCv') fautes.push(`${m} : au point touché, « ${dessus} » couvre la Toile`);
      if (d.length !== 1 || d[0]!.vers !== 'fiche' || d[0]!.arg !== q.pid)
        fautes.push(`${m} : la dalle ${String(q.pid)} demande ${JSON.stringify(d)}`);
    }
  }
  expect(fautes).toEqual([]);
});

test("une image longue (900 ms) entre l'appui et le lever ne fait pas perdre le toucher (v139) : la durée se lit à l'heure des ÉVÉNEMENTS", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await ouvrir(page, sansBandeau(etatBanc(25)));
  await page.evaluate("window.__promi.magasin.choisirMonde('ritournelle')");
  await posee(page);
  if (sonde('toucher-heure'))
    // la version d'avant v139 : la durée du toucher comptée à l'heure du TRAITEMENT
    await page.evaluate(
      "Object.defineProperty(Event.prototype, 'timeStamp', { configurable: true, get() { return performance.now(); } })",
    );
  const P = (await page.evaluate(POINTS)) as { pts: Array<{ pid: number; x: number; y: number }> };
  expect(P.pts.length, 'trois dalles de Ritournelle à toucher').toBe(3);
  const ratees: string[] = [];
  for (const q of P.pts) {
    const n0 = (await page.evaluate('window.__dem.length')) as number;
    // un appui et un lever à 80 ms d'écart (leurs heures d'événement), livrés de part et d'autre d'une image de 900 ms (ce que fait Ritournelle
    // sur un téléphone) — on ne peut pas dater les événements de Playwright : on les fabrique, datés à leur création
    await page.evaluate(
      async ([x, y]: [number, number]) => {
        const cv = document.getElementById('toileCv')!;
        const o = {
          bubbles: true,
          cancelable: true,
          composed: true,
          clientX: x,
          clientY: y,
          pointerId: 7,
          isPrimary: true,
          pointerType: 'touch',
          button: 0,
        };
        const bas = new PointerEvent('pointerdown', { ...o, buttons: 1 });
        await new Promise((f) => {
          window.setTimeout(f, 80);
        });
        const haut = new PointerEvent('pointerup', { ...o, buttons: 0 });
        cv.dispatchEvent(bas);
        const t = performance.now();
        while (performance.now() - t < 900) {
          /* l'image longue */
        }
        cv.dispatchEvent(haut);
      },
      [q.x, q.y] as [number, number],
    );
    await page
      .waitForFunction((n) => (window as unknown as { __dem: unknown[] }).__dem.length > n, n0, { timeout: 3000 })
      .catch(() => {});
    const d = ((await demandes(page)) as Dem[]).slice(n0);
    if (d.length !== 1 || d[0]!.vers !== 'fiche' || d[0]!.arg !== q.pid)
      ratees.push(`${String(q.pid)} → ${JSON.stringify(d)}`);
    await page.waitForTimeout(450);
  }
  expect(ratees, 'trois touchers sur trois').toEqual([]);
});

test("Ritournelle, une puis trois paroles (C-088, v145) : la Toile n'a que ses paroles — autant de cellules que de paroles", async ({
  browser,
}) => {
  const comptes: string[] = [];
  for (const n of [1, 3]) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    // un compte qui débute : n paroles, sans place gardée (redteam_toucher.py : « un vrai départ »)
    const ls = etatBanc(5);
    const st = JSON.parse(ls['promi_state']!) as { promises: Array<Record<string, unknown>> };
    st.promises = st.promises.filter((p) => !p['draft'] && !p['nuee']).slice(0, n);
    for (const p of st.promises) delete p['place'];
    await ouvrir(page, { ...ls, promi_state: JSON.stringify(st), promi_nueplace: '{}' });
    // la sonde : l'app n'applique pas le monde choisi (la Toile garde le semis constant des anciens mondes, la version d'avant C-088)
    if (!sonde('ritournelle-monde')) await page.evaluate("window.__promi.magasin.choisirMonde('ritournelle')");
    await posee(page);
    const g = (await page.evaluate(
      '({ total: Toile.graines().total, paroles: Toile_lecture().graines.filter((s) => s.pid != null).length, monde: Toile.getTheme() })',
    )) as {
      total: number;
      paroles: number;
      monde: string;
    };
    comptes.push(`${String(n)} → ${g.monde} : ${String(g.total)} cellule(s), ${String(g.paroles)} parole(s)`);
    await ctx.close();
  }
  expect(comptes).toEqual([
    '1 → ritournelle : 1 cellule(s), 1 parole(s)',
    '3 → ritournelle : 3 cellule(s), 3 parole(s)',
  ]);
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_toucher_tolerant (v181a, C-239 ; C-323) — « un toucher ouvre la dalle de parole la plus proche si elle est à 22 pt ou moins du
 * doigt. Si deux dalles sont à égale distance, aucune ne s'ouvre. Rien ne change à l'écran ; le moteur n'est pas touché. » La vraie app est
 * identique au prototype : la tolérance vaut aussi pour une grande dalle (C-323, décision de Tom) ; le juge ne touche hors d'elles que les
 * petites (le plus grand carré qu'elles contiennent < 44 pt).
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

const CARTE_TOL = `(() => { const cv = document.getElementById('toileCv'), r = cv.getBoundingClientRect(), f = cv.clientWidth / r.width;
  const cle = (h) => (!h ? null : h.kind === 'nuee' && h.nuee ? 'n:' + h.nuee : h.pid != null ? 'p:' + h.pid : null); const G = {}, V = [];
  for (let y = 110; y <= 700; y += 2) for (let x = 4; x <= 386; x += 2) { const c = cle(Toile.hit((x - r.left) * f, (y - r.top) * f)); if (c) (G[c] = G[c] || []).push([x, y]); else V.push([x, y]); }
  const out = {}, bords = {};
  for (const c in G) { const P = G[c], S = new Set(P.map((p) => p[0] + ',' + p[1]));
    const mx = P.reduce((a, p) => a + p[0], 0) / P.length, my = P.reduce((a, p) => a + p[1], 0) / P.length; let best = P[0], bd = 1e9;
    for (const p of P) { const d = Math.hypot(p[0] - mx, p[1] - my); if (d < bd) { bd = d; best = p; } }
    let sq = 0; for (const p of P) { let a = sq + 2; for (;;) { let ok = true; for (let yy = p[1]; yy <= p[1] + a && ok; yy += 2) for (let xx = p[0]; xx <= p[0] + a; xx += 2) if (!S.has(xx + ',' + yy)) { ok = false; break; } if (!ok) break; sq = a; a += 2; } }
    out[c] = { mil: best, carre: sq }; bords[c] = P.filter((p) => !S.has(p[0] + 2 + ',' + p[1]) || !S.has(p[0] - 2 + ',' + p[1]) || !S.has(p[0] + ',' + (p[1] + 2)) || !S.has(p[0] + ',' + (p[1] - 2))); }
  const vides = []; for (let i = 0; i < V.length; i += 2) { const v = V[i];
    const ds = Object.keys(bords).map((c) => { let m = 1e9; for (const p of bords[c]) { const d = Math.hypot(p[0] - v[0], p[1] - v[1]); if (d < m) m = d; } return [m, c]; }).sort((a, b) => a[0] - b[0]);
    vides.push([v[0], v[1], ds[0] || null, ds[1] || null]); }
  return { dalles: out, vides }; })()`;
type Vide = [number, number, [number, string] | null, [number, string] | null];

/** l'état exporté de Tom s'il est là (redteam_toucher_tolerant.py : « juge sur mon état exporté »), et toujours la Toile de 25 paroles du banc */
const ETATS_TOL: Array<[string, Ls]> = [
  ...(/[\\/]tom-[^\\/]*\.json$/.test(ETAT) ? ([["l'état de Tom", stockage()]] as Array<[string, Ls]>) : []),
  ['le banc (25 paroles)', etatBanc(25)],
];
for (const [nomEtat, lsTol] of ETATS_TOL)
  test(`le toucher tolérant (C-239), ${nomEtat} : chaque dalle s’ouvre en son milieu ; une petite dalle, touchée à 6 – 18 pt d’elle ; à égale distance ou à plus de 28 pt, rien`, async ({
    page,
  }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await ouvrir(page, sansBandeau(lsTol));
    if (sonde('tolerant-rayon'))
      // la version d'avant C-239 : seul le point exact du doigt est lu (aucune dalle cherchée autour)
      await page.evaluate(`(() => { let px = -1e9, py = -1e9; window.addEventListener('pointerdown', (e) => { px = e.clientX; py = e.clientY; }, true);
      const o = Toile.hit; Toile.hit = function (x, y) { if (Math.hypot(x - px, y - py) > 0.75) return null; return o.call(this, x, y); }; })()`);
    // Touffe forcé, vue recadrée (redteam_toucher_tolerant.py)
    await page.evaluate("window.__promi.magasin.choisirMonde('touffe')");
    await posee(page);
    await page.evaluate('window.__promi.facade.recadrer()');
    await posee(page);
    const C = (await page.evaluate(CARTE_TOL)) as {
      dalles: Record<string, { mil: [number, number]; carre: number }>;
      vides: Vide[];
    };
    const ouvre = (d: Dem[]): string | null =>
      d.length === 1
        ? d[0]!.vers === 'fiche'
          ? `p:${String(d[0]!.arg)}`
          : d[0]!.vers === 'cercle'
            ? `n:${String(d[0]!.arg)}`
            : '?'
        : d.length
          ? '?'
          : null;
    const cles = Object.keys(C.dalles);
    expect(cles.length, 'des dalles de parole sur la Toile').toBeGreaterThan(0);
    // A · chaque dalle touchée en son milieu (le témoin)
    const A: string[] = [];
    for (const c of cles) {
      const o = ouvre(await toucherEtLire(page, ...C.dalles[c]!.mil));
      if (o !== c) A.push(`${c} → ${String(o)}`);
    }
    expect(A, 'A · chaque dalle de parole s’ouvre touchée en son milieu').toEqual([]);
    // B · chaque petite dalle (< 44 pt) touchée HORS d'elle, sur une case vide à 6 – 18 pt où elle est seule la plus proche (la seconde à 6 pt plus loin)
    const petites = cles.filter((c) => C.dalles[c]!.carre < 44);
    const B: string[] = [];
    for (const c of petites) {
      const cand = C.vides
        .filter((v) => v[2] && v[2][1] === c && v[2][0] >= 6 && v[2][0] <= 18 && (!v[3] || v[3][0] - v[2][0] >= 6))
        .sort((a, b) => b[2]![0] - a[2]![0]);
      const v = cand[0];
      if (!v) continue;
      const o = ouvre(await toucherEtLire(page, v[0], v[1]));
      if (o !== c) B.push(`${c} à ${v[2]![0].toFixed(1)} pt → ${String(o)}`);
    }
    if (!petites.length)
      test.info().annotations.push({ type: 'non jugé', description: 'B : aucune petite dalle sur cette Toile' });
    expect(B, 'B · chaque petite dalle s’ouvre touchée à 6 – 18 pt d’elle').toEqual([]);
    // C · à égale distance de deux dalles (± 0,5 pt), à 4 – 18 pt : rien
    const eg = C.vides
      .filter((v) => v[2] && v[3] && v[3][0] - v[2][0] <= 0.5 && v[2][0] <= 18 && v[2][0] >= 4)
      .slice(0, 3);
    const Cc: string[] = [];
    for (const v of eg) {
      const o = ouvre(await toucherEtLire(page, v[0], v[1]));
      if (o != null) Cc.push(`(${String(v[0])}, ${String(v[1])}) → ${o}`);
    }
    expect(Cc, 'C · à égale distance de deux dalles, rien ne s’ouvre').toEqual([]);
    // D · à plus de 28 pt de toute dalle : rien
    const loin = C.vides.filter((v) => !v[2] || v[2][0] > 28);
    const D: string[] = [];
    for (const v of loin.filter((_, i) => i % Math.max(1, Math.floor(loin.length / 3)) === 0).slice(0, 3)) {
      const o = ouvre(await toucherEtLire(page, v[0], v[1]));
      if (o != null) D.push(`(${String(v[0])}, ${String(v[1])}) → ${o}`);
    }
    expect(D, 'D · à plus de 28 pt de toute dalle, rien ne s’ouvre').toEqual([]);
    // E · le moteur n'est pas touché : le fichier repris est celui du prototype, octet pour octet
    expect(
      readFileSync(join(RACINE, 'promi-moteur.js')).equals(
        readFileSync(join(import.meta.dirname, '..', '..', 'src', 'moteur', 'repris', 'promi-moteur.js')),
      ),
      'E · le moteur de la vraie app est celui du prototype',
    ).toBe(true);
  });

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_accueil (direction B, Q212 · Q213 ; v95, v96, v136, v139, v140 C-087) — l'accueil à ses cotes, au doigt.
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

const GEO_ACC = `(() => { const D = document.getElementById('device').getBoundingClientRect(), k = D.width / 390;
  const B = (e) => { if (!e) return null; const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden') return null; const r = e.getBoundingClientRect(); if (r.width < 2) return null; return { x: (r.left - D.left) / k, y: (r.top - D.top) / k, w: r.width / k, h: r.height / k }; };
  const ink = (e) => { const rg = document.createRange(); rg.selectNodeContents(e); const r = rg.getBoundingClientRect(); return { x0: (r.left - D.left) / k, x1: (r.right - D.left) / k, y0: (r.top - D.top) / k, y1: (r.bottom - D.top) / k }; };
  const ent = ['studioBtn', 'souffleBtn', 'indexBtn', 'filBtn'].map((i) => { const e = document.getElementById(i); const l = e && e.querySelector('.l'); return { i, b: B(e), lab: l ? ink(l) : null, fs: l ? getComputedStyle(l).fontSize : null }; });
  const vis = (s) => { const e = document.querySelector(s); if (!e) return false; const c = getComputedStyle(e), r = e.getBoundingClientRect(); return c.display !== 'none' && c.visibility !== 'hidden' && +c.opacity > 0.05 && r.width > 2 && r.height > 2; };
  const flou = [...document.querySelectorAll('#accPlat, #accBarre, #accBarre *, #accPlat *')].filter((e) => { const c = getComputedStyle(e); return (c.backdropFilter && c.backdropFilter !== 'none') || (c.webkitBackdropFilter && c.webkitBackdropFilter !== 'none'); }).length;
  return { plat: B(document.getElementById('accPlat')), barre: B(document.getElementById('accBarre')), plus: B(document.getElementById('createBtn')), ent,
    parti: ['#device .statusbar', '#viewSwitch', '#cercleTopBtn', '#sidelabel', '.stage-fade-b', '.stage-fade-t', '#accLigne'].filter(vis), flou }; })()`;
type Boite = { x: number; y: number; w: number; h: number } | null;
type GeoAcc = {
  plat: Boite;
  barre: Boite;
  plus: Boite;
  ent: Array<{
    i: string;
    b: Boite;
    lab: { x0: number; x1: number; y0: number; y1: number } | null;
    fs: string | null;
  }>;
  parti: string[];
  flou: number;
};
const centre = (page: Page, sel: string): Promise<[number, number]> =>
  page.evaluate(
    `(() => { const b = document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; })()`,
  ) as Promise<[number, number]>;

for (const th of ['clair', 'sombre'] as const)
  test(`l'accueil (direction B), ${th} : plateau, barre et + à leurs cotes, les six portes et les trois natures au doigt, l'appui long n'ouvre pas le Studio`, async ({
    page,
  }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await ouvrir(page, {
      ...etatBanc(25),
      promi_theme: th === 'clair' ? 'light' : 'dark',
      promi_sig: '1',
      promi_sigdemo: '1',
    });
    if (sonde('accueil-cote'))
      // la barre descendue de 6 pt (v96 : « aligne » — à 40 du bas, comme le plateau l'est du haut)
      await page.addStyleTag({ content: '#accBarre{transform:translateY(6px)!important}' });
    await page.waitForTimeout(300);
    const g = (await page.evaluate(GEO_ACC)) as GeoAcc;
    const pl = g.plat!;
    const br = g.barre!;
    const pu = g.plus!;
    // 1 · les cotes, EN DUR (redteam_accueil.py) : plateau 24 · 40 · 342 × 60 (v95) ; barre 24 · 710 · 342 × 100 (v140, C-087) ; + 72 × 72 à
    //     159 · 724, son centre à 760, 12 pt d'air au moins jusqu'au contour de la barre
    const pres = (a: number, b: number, t = 1): boolean => Math.abs(a - b) <= t;
    expect(
      {
        plat: [pl.x, pl.y, pl.w, pl.h].map(Math.round),
        barre: [br.x, br.y, br.w, br.h].map(Math.round),
        plus: [pu.x, pu.y, pu.w, pu.h].map(Math.round),
      },
      'les cotes',
    ).toEqual({ plat: [24, 40, 342, 60], barre: [24, 710, 342, 100], plus: [159, 724, 72, 72] });
    expect(
      pres(pl.x, 24) &&
        pres(pl.y, 40) &&
        pres(br.y, 710) &&
        pres(pu.y + pu.h / 2, 760, 0.6) &&
        pu.y - (br.y + 2) >= 11.5 &&
        br.y + br.h - 2 - (pu.y + pu.h) >= 11.5,
      `l'air autour du + (${JSON.stringify({ pl, br, pu })})`,
    ).toBe(true);
    // les entrées centrées 70 · 124 | 266 · 320, sur la ligne du + (écart de centre ≤ 1) ; libellés 12 px ; aucune paire sous 8 pt
    const cent = g.ent.map((e) => (e.b ? Math.round((e.b.x + e.b.w / 2) * 10) / 10 : null));
    expect(
      cent.every((c, i) => c != null && pres(c, [70, 124, 266, 320][i]!, 1.5)) &&
        g.ent.every((e) => e.b && pres(e.b.y + e.b.h / 2, pu.y + pu.h / 2, 1)),
      `entrées centrées 70 · 124 | 266 · 320, sur la ligne du + (${JSON.stringify(cent)})`,
    ).toBe(true);
    const L = g.ent.map((e) => e.lab!);
    const airs = [
      L[1]!.x0 - L[0]!.x1,
      L[3]!.x0 - L[2]!.x1,
      L[0]!.x0 - (br.x + 2),
      br.x + br.w - 2 - L[3]!.x1,
      br.y + br.h - 2 - Math.max(...L.map((l) => l.y1)),
    ];
    expect(
      g.ent.map((e) => e.fs),
      'libellés à 12 px',
    ).toEqual(['12px', '12px', '12px', '12px']);
    expect(
      Math.min(...airs),
      `aucune paire sous 8 pt (${airs.map((a) => a.toFixed(1)).join(' · ')})`,
    ).toBeGreaterThanOrEqual(8);
    // 4, 6 · ce qui part : barre d'état, Toile/Index, rond du Cercle, libellé vertical, voiles, flous du chrome ; la ligne « N paroles » (Q347)
    expect(g.parti, 'rien de ce qui est parti').toEqual([]);
    expect(g.flou, 'aucun flou dans le plateau ni la barre').toBe(0);
    // 5 · un mode signature enregistré ne se rallume pas au chargement (promi_sig posé)
    expect(await page.evaluate("document.getElementById('device').classList.contains('sigmode')")).toBe(false);
    // 2 · les six portes, au doigt — elles DEMANDENT leur écran (les écrans sont aux lots 4 à 8)
    const portes: Array<[string, string]> = [
      ['#studioBtn', 'studio'],
      ['#souffleBtn', 'aura'],
      ['#indexBtn', 'index'],
      ['#filBtn', 'fil'],
      ['#shareBtn', 'partager'],
      ['#settingsBtn', 'reglages'],
    ];
    const mortes: string[] = [];
    for (const [sel, vers] of portes) {
      const d = await toucherEtLire(page, ...(await centre(page, sel)));
      if (d.length !== 1 || d[0]!.vers !== vers) mortes.push(`${sel} → ${JSON.stringify(d)}`);
    }
    expect(mortes, 'les six portes demandent leur écran').toEqual([]);
    // 3 · le + s'ouvre SUR PLACE : il ne demande aucun écran, il reste un + ; chaque nature demande SA page +, dans trois ordres
    const d0 = await toucherEtLire(
      page,
      ...(await centre(page, '#createBtn')),
      "document.getElementById('accChoix').classList.contains('ouvert')",
    );
    const st = (await page.evaluate(
      "({ ouvert: document.getElementById('accChoix').classList.contains('ouvert'), tr: getComputedStyle(document.querySelector('#createBtn svg')).transform })",
    )) as { ouvert: boolean; tr: string };
    expect({ ...st, demandes: d0 }, 'le + ouvre les natures sur place').toEqual({
      ouvert: true,
      tr: 'none',
      demandes: [],
    });
    await page.evaluate("document.getElementById('accChoix').classList.remove('ouvert')");
    const ratees: string[] = [];
    for (const ordre of [
      ['promi', 'chiche', 'nuee'],
      ['nuee', 'promi', 'chiche'],
      ['chiche', 'nuee', 'promi'],
    ])
      for (const k of ordre) {
        if (!(await page.evaluate("document.getElementById('accChoix').classList.contains('ouvert')")))
          await toucherEtLire(
            page,
            ...(await centre(page, '#createBtn')),
            "document.getElementById('accChoix').classList.contains('ouvert')",
          );
        const d = await toucherEtLire(page, ...(await centre(page, `.acc-pil[data-k="${k}"]`)));
        if (d.length !== 1 || d[0]!.vers !== 'pagePlus' || d[0]!.arg !== k) ratees.push(`${k} → ${JSON.stringify(d)}`);
        // lot 2a : la pilule OUVRE la page + (elle couvre l'accueil) — son X la referme avant la nature suivante
        await refermerPagePlus(page);
      }
    expect(ratees, 'chaque nature demande SA page +').toEqual([]);
    // 5 · l'appui long sur la Toile (0,9 s) n'ouvre pas le Studio
    const n0 = (await page.evaluate('window.__dem.length')) as number;
    await page.mouse.move(195, 440);
    await page.mouse.down();
    await page.waitForTimeout(900);
    await page.mouse.up();
    await page.waitForTimeout(900);
    expect(
      ((await demandes(page)) as Dem[]).slice(n0).filter((d) => d.vers === 'studio'),
      "l'appui long n'ouvre pas le Studio",
    ).toEqual([]);
  });

/** redteam_accueil 7 (scratchpad/accueil_audit.py, MASK_JS et REACH_JS) : toute dalle reste atteignable sous le chrome, à dix zooms */
const MASQUE = `(() => { const D = document.getElementById('device').getBoundingClientRect(), k = D.width / 390, cv = document.getElementById('toileCv'); const rows = [];
  for (let y = 0; y < 844; y += 4) { let row = ''; for (let x = 0; x < 390; x += 4) row += document.elementFromPoint(D.left + (x + 2) * k, D.top + (y + 2) * k) === cv ? '1' : '0'; rows.push(row); } return rows; })()`;
const ATTEINTE = `((rows) => { const zooms = [0.4, 0.48, 0.6, 0.8, 1.0, 1.25, 1.5, 2, 3, 5];
  const cv = document.getElementById('toileCv'), W = cv.clientWidth, H = cv.clientHeight, D = document.getElementById('device').getBoundingClientRect(), k = D.width / 390, cvr = cv.getBoundingClientRect();
  const offx = (cvr.left - D.left) / k, offy = (cvr.top - D.top) / k;
  const libre = (sx, sy) => { const X = Math.floor((sx + offx) / 4), Y = Math.floor((sy + offy) / 4); return Y >= 0 && Y < rows.length && X >= 0 && X < rows[0].length && rows[Y][X] === '1'; };
  const v0 = Toile.vue(), ids = promises.filter((p) => !p.draft && !p.req).map((p) => p.id), polys = {};
  for (const id of ids) { const a = Toile.dalleAbs(id); if (a) polys[id] = a; }
  const res = { n: Object.keys(polys).length, inatteignables: {} };
  for (const s of zooms) { const lx0 = Math.min(0, W - W * s), hx0 = Math.max(0, W - W * s), ly0 = Math.min(0, H - H * s), hy0 = Math.max(0, H - H * s), NP = 12, un = [];
    for (const id of Object.keys(polys)) { const a = polys[id]; let ok = false; const pts = [];
      for (let i = 1; i < 8; i++) for (let j = 1; j < 8; j++) pts.push([a.minx + (a.w * i) / 8, a.miny + (a.h * j) / 8]);
      const good = pts.filter(([lx, ly]) => { const h = Toile.hit(v0.ox + v0.s * lx, v0.oy + v0.s * ly); return h && h.pid == +id; });
      for (let pi = 0; pi <= NP && !ok; pi++) for (let pj = 0; pj <= NP && !ok; pj++) { const ox = lx0 + ((hx0 - lx0) * pi) / NP, oy = ly0 + ((hy0 - ly0) * pj) / NP;
        for (const [lx, ly] of good) if (libre(ox + s * lx, oy + s * ly)) { ok = true; break; } }
      if (!ok) un.push(+id); }
    if (un.length) res.inatteignables[s] = un; }
  return res; })`;

test("l'accueil (direction B) : toute dalle reste atteignable sous le plateau et la barre, à dix zooms, clair et sombre", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const th of ['light', 'dark']) {
    await ouvrir(page, { ...etatBanc(25), promi_theme: th });
    if (sonde('accueil-atteinte'))
      // une couche transparente qui prend le doigt sur la Toile, entre le plateau et la barre
      await page.evaluate(
        "(() => { const e = document.createElement('div'); e.style.cssText = 'position:absolute;left:0;top:100px;width:390px;height:610px;z-index:40'; document.getElementById('device').appendChild(e); })()",
      );
    const rows = (await page.evaluate(MASQUE)) as string[];
    const A = (await page.evaluate(`${ATTEINTE}(${JSON.stringify(rows)})`)) as {
      n: number;
      inatteignables: Record<string, number[]>;
    };
    expect(A.n, `${th} : des dalles`).toBeGreaterThan(10);
    expect(A.inatteignables, `${th} : aucune dalle inatteignable`).toEqual({});
  }
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_barre (v143, C-106) — « toucher STUDIO ouvre parfois l'Aura » : cinquante touchers par entrée, répartis sur TOUT ce qu'on en voit
 * (son icône et son mot, 3 pt de marge), chacun demande la bonne page. 50 sur 50, EN DUR.
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

test("la barre (C-106) : cinquante touchers sur ce qu'on voit de chaque entrée (et du +) demandent sa page, cinquante sur cinquante", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // CORRIGÉ (C-326, 20 nov. 2026) : la zone de chaque entrée est sa largeur (54 pt), toute la hauteur intérieure de la barre ; STUDIO déborde
  // de 5 pt sur l'AURA et passe devant, INDEX de 3 pt sur le FIL (accueil.css, le prototype app.html ≈ l. 34842). Mesuré avant : STUDIO 46
  // sur 50, INDEX 49 sur 50.
  // la sonde : la zone de l'AURA qui déborde de 36 pt sur STUDIO et passe devant (la cause de C-106, v143)
  if (sonde('barre-chevauche'))
    await page.addInitScript(() => {
      const st = document.createElement('style');
      st.textContent = '#souffleBtn{z-index:5!important}#souffleBtn::after{left:-36px!important}';
      document.addEventListener('DOMContentLoaded', () => document.head.appendChild(st));
    });
  await ouvrir(page, sansBandeau(etatBanc(25)));
  const N = 50;
  let graine = 143;
  const alea = (): number => (graine = (graine * 1103515245 + 12345) % 2147483648) / 2147483648;
  const ATTENDU: Record<string, string> = {
    studioBtn: 'studio',
    souffleBtn: 'aura',
    createBtn: 'plus',
    indexBtn: 'index',
    filBtn: 'fil',
  };
  const faux: string[] = [];
  const rang = (await page.evaluate(
    "[document.getElementById('studioBtn').getBoundingClientRect().left, document.getElementById('filBtn').getBoundingClientRect().right]",
  )) as [number, number];
  for (const [id, vers] of Object.entries(ATTENDU)) {
    // ce qu'on voit de l'entrée : la réunion de son icône et de son MOT — le texte rendu (un Range), jamais la boîte de son nœud, qui prend
    // toute la largeur de l'entrée (le + : son disque)
    const bx =
      (await page.evaluate(`(() => { const e = document.getElementById(${JSON.stringify(id)}); let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
      for (const n of ${JSON.stringify(id)} === 'createBtn' ? [e] : [...e.querySelectorAll('svg, .l')]) { let r = n.getBoundingClientRect(); if (n.classList && n.classList.contains('l')) { const g = document.createRange(); g.selectNodeContents(n); r = g.getBoundingClientRect(); } if (r.width < 2) continue; x0 = Math.min(x0, r.left); x1 = Math.max(x1, r.right); y0 = Math.min(y0, r.top); y1 = Math.max(y1, r.bottom); }
      return [x0, x1, y0, y1]; })()`)) as [number, number, number, number];
    let ok = 0;
    for (let i = 0; i < N; i++) {
      let x: number;
      let y: number;
      if (id === 'createBtn') {
        const a = alea() * 6.283;
        const r = 30 * Math.sqrt(alea());
        x = (bx[0] + bx[1]) / 2 + r * Math.cos(a);
        y = (bx[2] + bx[3]) / 2 + r * Math.sin(a);
      } else {
        // 3 pt de marge autour de ce qu'on voit, mais jamais hors de la rangée des zones (v143 : 43 → 347 à 390 de large) — à gauche de
        // STUDIO et à droite de FIL, le doigt tombe sur la barre elle-même, hors de toute entrée, dans le prototype comme dans l'app
        x = Math.min(rang[1], Math.max(rang[0], bx[0] - 3 + alea() * (bx[1] - bx[0] + 6)));
        y = bx[2] - 3 + alea() * (bx[3] - bx[2] + 6);
      }
      const d = await toucherEtLire(
        page,
        x,
        y,
        id === 'createBtn' ? "document.getElementById('accChoix').classList.contains('ouvert')" : undefined,
      );
      const ouvert = (await page.evaluate(
        "document.getElementById('accChoix').classList.contains('ouvert')",
      )) as boolean;
      const vu =
        id === 'createBtn'
          ? ouvert && !d.length
            ? 'plus'
            : JSON.stringify(d)
          : d.length === 1
            ? d[0]!.vers
            : JSON.stringify(d);
      if (vu === vers) ok++;
      else faux.push(`${id} (${x.toFixed(0)}, ${y.toFixed(0)}) → ${vu}`);
      if (ouvert) await page.evaluate("document.getElementById('accChoix').classList.remove('ouvert')");
    }
    expect.soft(ok, `${id} : ${String(N)} touchers sur ${String(N)} (${faux.slice(-6).join(' · ')})`).toBe(N);
  }
  // les zones voisines ne se chevauchent pas (STUDIO / AURA, INDEX / FIL)
  const Z = (await page.evaluate(
    "['studioBtn', 'souffleBtn', 'indexBtn', 'filBtn'].map((i) => { const r = document.getElementById(i).getBoundingClientRect(); return [r.left, r.right]; })",
  )) as Array<[number, number]>;
  expect(Z[0]![1] <= Z[1]![0] + 0.5 && Z[2]![1] <= Z[3]![0] + 0.5, `zones ${JSON.stringify(Z)}`).toBe(true);
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_recadre_bouton (v163, C-188) — « Aucun encart ni fond : un symbole seul, à l'encre du mode, ≈ 22 pt, une zone de toucher
 * invisible de 44 pt ; en bas à droite, juste au-dessus de la barre. Il paraît quand on a déplacé ou zoomé la vue, et disparaît de lui-même
 * après 4 s sans toucher, en flaques rapides (≈ 300 ms), jamais d'un coup. » (Les 4 s, le retour au glissé suivant, le toucher qui recadre
 * et le double toucher : accueil.spec.ts.)
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

/** le passage en flaques du symbole : chaque canevas `.passage-flaques` posé dans #accRecadre, son heure d'arrivée et de départ (dans la
 *  page), et, à chaque image de l'horloge, la part de ses pixels peints */
const SUIVI_PASSAGE = `(() => { const r = document.getElementById('accRecadre'); const P = window.__pass = [];
  new MutationObserver((ms) => { for (const m of ms) { for (const n of m.addedNodes) if (n.classList && n.classList.contains('passage-flaques')) P.push({ cv: n, mode: r.classList.contains('cache') && r.classList.contains('vu') ? (window.__etatRc ? window.__etatRc() : '?') : '?', t0: performance.now(), t1: null, parts: [] });
    for (const n of m.removedNodes) for (const p of P) if (p.cv === n && p.t1 == null) p.t1 = performance.now(); } }).observe(r, { childList: true });
  const h = window.__promi.horloge; const b = () => { for (const p of P) if (p.t1 == null && p.cv.width) { try { const d = p.cv.getContext('2d').getImageData(0, 0, p.cv.width, p.cv.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 8) n++; p.parts.push(n); } catch (e) {} } h.image(b); }; h.image(b);
  window.__etatRc = () => window.__promi.accueil().etatRecadre().etat; })()`;
type Passage = { mode: string; t0: number; t1: number | null; parts: number[] };
const lirePassages = async (page: Page): Promise<Passage[]> =>
  (await page.evaluate(
    'window.__pass.map((p) => ({ mode: p.mode, t0: p.t0, t1: p.t1, parts: p.parts }))',
  )) as Passage[];
async function glisseVue(page: Page, de: [number, number], vers: [number, number]): Promise<void> {
  await page.mouse.move(de[0], de[1]);
  await page.mouse.down();
  await page.mouse.move(vers[0], vers[1], { steps: 10 });
  await page.mouse.up();
}

/** le symbole lu sur l'IMAGE (redteam_recadre_bouton.py, C) : la même vue avec et sans lui, la Toile cachée (elle peut encore glisser entre
 *  deux captures) ; rend la boîte de son encre (en pt de l'écran) et la couleur du pixel le plus écarté */
async function encreRecadre(
  page: Page,
): Promise<{ b: { x0: number; y0: number; x1: number; y1: number } | null; encre: number[] }> {
  await page.addStyleTag({ content: '#stage{visibility:hidden!important}' });
  await page.waitForTimeout(150);
  const zb = (await page.evaluate(
    // le cadre de lecture, borné à la fenêtre (une capture hors de la fenêtre est rognée, et l'échelle se lirait mal)
    "(() => { const q = document.getElementById('accRecadre').getBoundingClientRect(); const x = Math.max(0, q.left - 30), y = Math.max(0, q.top - 30); return { x, y, width: Math.min(innerWidth, q.right + 30) - x, height: Math.min(innerHeight, q.bottom + 30) - y }; })()",
  )) as { x: number; y: number; width: number; height: number };
  const avec = PNG.sync.read(await page.screenshot({ clip: zb }));
  await page.evaluate("document.getElementById('accRecadre').style.setProperty('visibility', 'hidden', 'important')");
  await page.waitForTimeout(150);
  const sans = PNG.sync.read(await page.screenshot({ clip: zb }));
  await page.evaluate("document.getElementById('accRecadre').style.removeProperty('visibility')");
  const k = avec.width / zb.width;
  let x0 = 1e9;
  let y0 = 1e9;
  let x1 = -1;
  let y1 = -1;
  let pire = 0;
  let encre: number[] = [];
  for (let y = 0; y < avec.height; y++)
    for (let x = 0; x < avec.width; x++) {
      const i = (y * avec.width + x) * 4;
      const d = Math.max(...[0, 1, 2].map((c) => Math.abs(avec.data[i + c]! - sans.data[i + c]!)));
      if (d > 24) {
        x0 = Math.min(x0, x);
        y0 = Math.min(y0, y);
        x1 = Math.max(x1, x);
        y1 = Math.max(y1, y);
      }
      if (d > pire) {
        pire = d;
        encre = [avec.data[i]!, avec.data[i + 1]!, avec.data[i + 2]!];
      }
    }
  await page.addStyleTag({ content: '#stage{visibility:visible!important}' });
  if (x1 < 0) return { b: null, encre };
  return { b: { x0: zb.x + x0 / k, y0: zb.y + y0 / k, x1: zb.x + (x1 + 1) / k, y1: zb.y + (y1 + 1) / k }, encre };
}

for (const th of ['clair', 'sombre'] as const)
  test(`le symbole « recadrer » (C-188), ${th} : il naît et part en flaques, 22 pt d'encre seule à l'encre du mode, sur la marge, une zone de 44 pt`, async ({
    browser,
  }) => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    const page = await ctx.newPage();
    await ouvrir(page, { ...etatBanc(10), promi_theme: th === 'clair' ? 'light' : 'dark' });
    await page.evaluate(SUIVI_PASSAGE);
    if (sonde('recadre-rond'))
      // la version d'avant C-188 : un rond plein sous le symbole
      await page.addStyleTag({ content: '#accRecadre{background:#7A4E35!important;border-radius:50%!important}' });
    // A · au repos, rien
    expect(
      await page.evaluate("document.getElementById('accRecadre').classList.contains('vu')"),
      'A · au repos, rien',
    ).toBe(false);
    // B · un glissé : il naît par un passage en flaques (« couvre »), puis le symbole est là, net
    await glisseVue(page, [200, 420], [150, 390]);
    await page.waitForFunction("window.__promi.accueil().etatRecadre().etat === 'la'", undefined, { timeout: 15000 });
    const nait = (await lirePassages(page))[0];
    expect(nait, 'B · il naît par un passage en flaques').toBeTruthy();
    expect(nait!.t1, 'B · le passage est fini, le symbole est là').not.toBeNull();
    if (calme())
      expect(
        Math.abs(nait!.t1! - nait!.t0 - 300),
        `B · le passage dure 300 ms (± 60) : ${String(Math.round(nait!.t1! - nait!.t0))} ms`,
      ).toBeLessThanOrEqual(60);
    else nonJuge('B · la durée du passage (300 ms) — machine chargée ou hors du Mac');
    // C · le symbole lu sur l'IMAGE
    const { b: bb, encre } = await encreRecadre(page);
    expect(bb, "C · le symbole est à l'image").not.toBeNull();
    const b = bb!;
    const ENCRE = th === 'clair' ? [32, 25, 8] : [247, 240, 222]; // #201908 · #F7F0DE (C-188 : « à l'encre du mode »)
    expect(
      { large: b.x1 - b.x0 >= 20 && b.x1 - b.x0 <= 24, haut: b.y1 - b.y0 >= 20 && b.y1 - b.y0 <= 24 },
      `C · l'encre fait 20 à 24 pt (${(b.x1 - b.x0).toFixed(1)} × ${(b.y1 - b.y0).toFixed(1)})`,
    ).toEqual({ large: true, haut: true });
    // (son bas à 12 pt de la barre : le test suivant, rouge — un défaut de la vraie app)
    expect(
      Math.abs(390 - b.x1 - 24),
      `C · son bord droit à 24 pt du bord (± 1,5 : ${(390 - b.x1).toFixed(1)})`,
    ).toBeLessThanOrEqual(1.5);
    expect(
      Math.max(...ENCRE.map((v, i) => Math.abs(v - encre[i]!))),
      `C · à l'encre du mode (${JSON.stringify(encre)})`,
    ).toBeLessThanOrEqual(6);
    // D · la zone de 44 pt : ses quatre coins (à 3 pt du bord) recadrent
    const coins: string[] = [];
    for (const [fx, fy] of [
      [3, 3],
      [41, 3],
      [3, 41],
      [41, 41],
    ] as const) {
      if (!(await page.evaluate("document.getElementById('accRecadre').classList.contains('vu')"))) {
        await glisseVue(page, [200, 420], [150 + fx, 390]);
        await page.waitForFunction("window.__promi.accueil().etatRecadre().etat === 'la'", undefined, {
          timeout: 15000,
        });
      }
      const q = (await page.evaluate(
        "(() => { const q = document.getElementById('accRecadre').getBoundingClientRect(); return [q.left, q.top, q.width]; })()",
      )) as number[];
      expect(q[2], 'D · une zone de 44 pt').toBe(44);
      await page.mouse.click(q[0]! + fx, q[1]! + fy);
      await page.waitForTimeout(300);
      if (await page.evaluate('window.__promi.facade.vueALaMain()')) coins.push(`(${String(fx)}, ${String(fy)})`);
      await page.waitForFunction("window.__promi.accueil().etatRecadre().etat === 'absent'", undefined, {
        timeout: 15000,
      });
    }
    expect(coins, 'D · les quatre coins de la zone recadrent').toEqual([]);
    // E · 4 s sans toucher : il PART par un passage en flaques (« ouvre »), jamais d'un coup — on lit la part peinte de son canevas à chaque image
    await glisseVue(page, [200, 420], [250, 470]);
    await page.waitForFunction("window.__promi.accueil().etatRecadre().etat === 'la'", undefined, { timeout: 15000 });
    const n0 = (await lirePassages(page)).length;
    await page.waitForFunction("window.__promi.accueil().etatRecadre().etat === 'absent'", undefined, {
      timeout: 120000,
    });
    const part = (await lirePassages(page)).slice(n0).at(-1);
    expect(part, 'E · il part par un passage en flaques').toBeTruthy();
    const pl = part!.parts.filter((n) => n > 0);
    const max = Math.max(0, ...part!.parts);
    if (part!.parts.length >= 3) {
      expect(max, 'E · le passage peint le symbole').toBeGreaterThan(0);
      expect(
        pl.some((n) => n > 0.05 * max && n < 0.95 * max) || part!.parts.some((n) => n === 0),
        `E · à mi-passage, il en reste une partie (parts ${JSON.stringify(part!.parts)})`,
      ).toBe(true);
    } else
      nonJuge(
        `E · « jamais d'un coup » : ${String(part!.parts.length)} image(s) pendant le passage (une image toutes les 0,7 s hors du Mac)`,
      );
    await ctx.close();
  });

test('le symbole « recadrer » (C-188) : le bas de son encre est à 12 pt au-dessus de la barre (± 1,5)', async ({
  browser,
}) => {
  // CORRIGÉ (C-326, 20 nov. 2026) : la zone du symbole 665 → 709 comme dans le prototype (accueil.css, `bottom: calc(var(--ancre-bas) +
  // 101px)`) ; avant, 2 pt plus bas (le bas de l'encre à 10 pt de la barre).
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
  const page = await ctx.newPage();
  await ouvrir(page, etatBanc(10));
  // la sonde : le symbole 2 pt plus bas (la version d'avant la correction)
  if (sonde('recadre-bas'))
    await page.addStyleTag({ content: '.acc-recadre{bottom:calc(var(--ancre-bas) + 99px)!important}' });
  await glisseVue(page, [200, 420], [150, 390]);
  await page.waitForFunction("window.__promi.accueil().etatRecadre().etat === 'la'", undefined, { timeout: 15000 });
  const { b } = await encreRecadre(page);
  expect(b, "le symbole est à l'image").not.toBeNull();
  expect(
    Math.abs(710 - b!.y1 - 12),
    `son bas à 12 pt de la barre (± 1,5 : ${(710 - b!.y1).toFixed(1)})`,
  ).toBeLessThanOrEqual(1.5);
  await ctx.close();
});

/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * redteam_deplace (v142, C-101 ; v146, Q496) — « Un appui de 0,8 s sur une dalle la détache ; elle suit le doigt, les voisines se
 * réorganisent ; au lâcher elle reste où on l'a posée, sa place est gardée ; jamais sous la barre du bas. » Cinq mondes, EN DUR.
 * (L'appui long dans Safari d'iOS — la sélection de texte, C-324 — et la place dans le magasin : accueil.spec.ts.)
 * ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */

/** chaque parole à l'écran (grille de 6 pt, y 110 → 706) : centre, nombre de points, et sa place DANS la Toile (le point ramené par la vue) */
const OU = `(() => { const G = {}; for (let y = 110; y < 706; y += 6) for (let x = 8; x < 384; x += 6) { let h = null; try { h = Toile.hit(x, y); } catch (e) {} if (h && h.pid != null) { const g = G[h.pid] = G[h.pid] || { n: 0, x: 0, y: 0 }; g.n++; g.x += x; g.y += y; } }
  const v = Toile_vueLue(), o = {}; for (const p in G) { const X = G[p].x / G[p].n, Y = G[p].y / G[p].n; o[p] = [X, Y, G[p].n, (X - v.ox) / v.s, (Y - v.oy) / v.s]; } return { o, s: v.s }; })()`;
type Ou = { o: Record<string, [number, number, number, number, number]>; s: number };
async function tenirEtGlisser(
  page: Page,
  de: [number, number],
  vers: [number, number],
  tenue: number,
): Promise<number> {
  await page.evaluate(
    'window.__tire = 0; clearInterval(window.__it); window.__it = setInterval(() => { if (Toile_tire()) window.__tire++; }, 30)',
  );
  await page.mouse.move(de[0], de[1]);
  await page.mouse.down();
  await page.waitForTimeout(tenue);
  await page.mouse.move(vers[0], vers[1], { steps: 14 });
  const n = (await page.evaluate('window.__tire')) as number;
  await page.mouse.up();
  return n;
}

test('déplacer une dalle (C-101) sous cinq mondes : attrapée à 0,8 s, posée sous le doigt, aucune fiche, gardée au rechargement, jamais sous la barre', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const fautes: string[] = [];
  for (const m of ['encre', 'touffe', 'mosaique', 'ritournelle', 'bobinette']) {
    // trois paroles, sans place gardée (redteam_deplace.py : « Toile de ses seules paroles, plantées par l'app »)
    const ls = etatBanc(5);
    const st = JSON.parse(ls['promi_state']!) as { promises: Array<Record<string, unknown>> };
    st.promises = st.promises.filter((p) => !p['draft'] && !p['nuee']).slice(0, 3);
    for (const p of st.promises) delete p['place'];
    await ouvrir(page, sansBandeau({ ...ls, promi_state: JSON.stringify(st), promi_nueplace: '{}' }));
    if (sonde('deplace-place-perdue'))
      // la place notée par le moteur n'est pas gardée par le magasin
      await page.evaluate('window.__promi.magasin.noterPlaces = () => {}');
    await page.evaluate(`window.__promi.magasin.choisirMonde(${JSON.stringify(m)})`);
    await posee(page);
    expect(await page.evaluate('Toile_tireRegle.MS'), '6 · la règle déclarée : 800 ms').toBe(800);
    let G = (await page.evaluate(OU)) as Ou;
    const pids = Object.keys(G.o).sort((a, b) => G.o[b]![2] - G.o[a]![2]);
    if (pids.length < 3) {
      fautes.push(`${m} : ${String(pids.length)} parole(s) visibles sur 3`);
      continue;
    }
    const a = pids[0]!;
    const cible = (o: [number, number, number, number, number]): [number, number] => {
      const d = Math.hypot(195 - o[0], 400 - o[1]) || 1;
      return d >= 60 ? [o[0] + ((195 - o[0]) / d) * 110, o[1] + ((400 - o[1]) / d) * 110] : [o[0] + 90, o[1] + 90];
    };
    const n0 = (await page.evaluate('window.__dem.length')) as number;
    // 3 · un glissé SANS attendre (0,15 s) ne détache rien
    const sansAttendre = await tenirEtGlisser(page, [G.o[a]![0], G.o[a]![1]], [G.o[a]![0] + 40, G.o[a]![1] + 50], 150);
    await page.waitForTimeout(900);
    if (sansAttendre || (await page.evaluate('window.__tire')))
      fautes.push(`${m} : 3 · un glissé sans attendre a détaché la dalle`);
    await posee(page);
    G = (await page.evaluate(OU)) as Ou;
    const o0 = G.o[a]!;
    const [x1, y1] = cible(o0);
    const prise = await tenirEtGlisser(page, [o0[0], o0[1]], [x1, y1], 950);
    if (m === 'ritournelle') {
      // Q496 (v146) : sous Ritournelle l'appui long n'attrape rien, la dalle reste, aucune fiche, aucun message ; un toucher bref ouvre la fiche
      await page.waitForTimeout(1200);
      await posee(page);
      const o = ((await page.evaluate(OU)) as Ou).o[a];
      const msg = (await page.evaluate(
        "[...document.querySelectorAll('.toast,[role=alert],[role=status]')].filter((e) => e.getBoundingClientRect().width > 0 && e.textContent.trim()).length",
      )) as number;
      if (
        prise ||
        !o ||
        Math.hypot(o[0] - o0[0], o[1] - o0[1]) > 20 ||
        msg ||
        !(await page.evaluate('!!(window.Toile_tireNon && Toile_tireNon.ritournelle)'))
      )
        fautes.push(`${m} : Q496 · attrapée ${String(prise)} · ${JSON.stringify(o)} · messages ${String(msg)}`);
      if (((await demandes(page)) as Dem[]).slice(n0).length) fautes.push(`${m} : Q496 · une fiche demandée`);
      const d = o ? await toucherEtLire(page, o[0], o[1]) : [];
      if (d.length !== 1 || d[0]!.vers !== 'fiche' || String(d[0]!.arg) !== a)
        fautes.push(`${m} : Q496 · le toucher bref demande ${JSON.stringify(d)}`);
      continue;
    }
    if (prise < 3) fautes.push(`${m} : 1 · la dalle n'est pas attrapée pendant le geste (${String(prise)})`);
    // 1 · elle finit sous le doigt (≤ 50 pt du lâcher) — la Toile se repose (sur la CI, une image toutes les 0,7 s)
    await page
      .waitForFunction(
        ([pid, x, y]) => {
          const L = (
            window as unknown as {
              Toile_lecture(): {
                graines: Array<{ pid: number | null; x: number; y: number }>;
                vue: { s: number; ox: number; oy: number };
              };
            }
          ).Toile_lecture();
          const g = L.graines.find((q) => q.pid === pid);
          return !!g && Math.hypot(g.x * L.vue.s + L.vue.ox - x!, g.y * L.vue.s + L.vue.oy - y!) <= 50;
        },
        [+a, x1, y1],
        { timeout: 60000 },
      )
      .catch(() => {});
    await posee(page);
    const G2 = (await page.evaluate(OU)) as Ou;
    const ou = G2.o[a];
    if (!ou || Math.hypot(ou[0] - x1, ou[1] - y1) > 50 || Math.hypot(ou[0] - o0[0], ou[1] - o0[1]) < 60)
      fautes.push(
        `${m} : 1 · départ (${o0[0].toFixed(0)}, ${o0[1].toFixed(0)}), lâcher (${x1.toFixed(0)}, ${y1.toFixed(0)}), dalle ${JSON.stringify(ou?.slice(0, 2).map(Math.round))}`,
      );
    // 2 · aucune fiche ; les trois paroles toujours là ; la vue (le zoom) n'a pas changé
    if (((await demandes(page)) as Dem[]).slice(n0).length) fautes.push(`${m} : 2 · une fiche demandée au lâcher`);
    if (!pids.slice(0, 3).every((p) => G2.o[p]))
      fautes.push(`${m} : 2 · ${String(Object.keys(G2.o).length)} paroles visibles`);
    if (Math.abs(G2.s - G.s) > 1e-6)
      fautes.push(`${m} : 2 · le zoom a changé (${G.s.toFixed(4)} → ${G2.s.toFixed(4)})`);
    // 4 · après rechargement, la dalle est où on l'a posée DANS LA TOILE (≤ 30 pt de Toile), plus à son départ (≥ 15) — la vue se recadre
    await rouvrir(page);
    const G3 = (await page.evaluate(OU)) as Ou;
    const o3 = G3.o[a];
    if (!o3 || !ou || Math.hypot(o3[3] - ou[3], o3[4] - ou[4]) > 30 || Math.hypot(o3[3] - o0[3], o3[4] - o0[4]) < 15)
      fautes.push(
        `${m} : 4 · départ ${JSON.stringify(o0.slice(3).map(Math.round))} · posée ${JSON.stringify(ou?.slice(3).map(Math.round))} · relue ${JSON.stringify(o3?.slice(3).map(Math.round))}`,
      );
    if (!o3) continue;
    // 5 · lâchée sous la barre (y 800) : elle reste atteignable au-dessus (centre < 710)
    await tenirEtGlisser(page, [o3[0], o3[1]], [195, 800], 950);
    await page.waitForTimeout(1600);
    await posee(page);
    const o4 = ((await page.evaluate(OU)) as Ou).o[a];
    if (!o4 || o4[1] >= 710 || o4[2] < 12)
      fautes.push(`${m} : 5 · lâchée sous la barre, la dalle est ${JSON.stringify(o4?.map(Math.round))}`);
    // 3 · un toucher bref ouvre toujours la fiche
    if (o4) {
      const d = await toucherEtLire(page, o4[0], o4[1]);
      if (d.length !== 1 || d[0]!.vers !== 'fiche' || String(d[0]!.arg) !== a)
        fautes.push(`${m} : 3 · le toucher bref demande ${JSON.stringify(d)}`);
    }
  }
  expect(fautes).toEqual([]);
});
