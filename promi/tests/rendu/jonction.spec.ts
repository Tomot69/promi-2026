/**
 * LOT 3a-3 — DÉFILER : LA JONCTION (banc_jonction, redteam_jonction, redteam_jonction_fiche, redteam_jonction_plat, redteam_points_plat,
 * redteam_trait_entier, redteam_repos_fiche, redteam_haut_fiche en partie). Une fiche qui porte trois mots (le jeu de banc_jonction : Marion,
 * Rachel, Nico) défile ; des deux côtés, l'horloge pilotée et les animations gelées, à chaque pas de défilement (0 → 120 → 0 par 3 pt, puis
 * jusqu'au bout et retour), l'écran ENTIER est comparé au pixel au prototype : la bande collée en haut, la vague qui monte puis passe dessous,
 * le trait plat qui se découvre sous elle à la jonction, les Noyaux, la phrase, le titre, « Les Mots » et leur liste qui montent sous la bande,
 * le plateau et la barre Peaufiner qui ne bougent pas. Exceptions : celles de fiche.spec.ts (M1 la matière, M2 le grain des anneaux, M3 le fondu),
 * et M4, le chevron de Peaufiner que le prototype retourne en bas de la fiche (Q626, ci-dessous).
 * Puis le geste accroché, les places sûres et les aimants, contre ce que le prototype déclare et fait.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import {
  fichesPilotees,
  images,
  ecart,
  sonde,
  stockageFiches,
  zonesFiche,
  masquerFiche,
  appareil,
  tracerPilote,
  P_,
} from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'jonction');
/** les mots de banc_jonction.py, datés du 1er au 3 nov. */
const MOTS = [
  ['Marion', 'On commence quand ?'],
  ['Rachel', 'Je m’occupe de la farine.'],
  ['Nico', 'Samedi matin, ça te va ?'],
] as const;
const CAS: ReadonlyArray<[number, string]> = [
  [144, 'Promi à soi'],
  [162, 'Chiche lancé à Adrien'],
  [146, 'Promi tenu'],
];

/** le stockage des fiches, la parole `id` portant les trois mots */
function avecMots(id: number, theme: 'sombre' | 'clair'): Record<string, string> {
  const ls: Record<string, string> = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
  const st = JSON.parse(ls['promi_state']!) as { promises: Array<{ id: number; comments?: unknown[] }> };
  const p = st.promises.find((q) => q.id === id)!;
  p.comments = MOTS.map(([by, t], i) => ({ t, by, d: `2026-11-0${String(i + 1)}T09:00:00Z`, vu: true }));
  ls['promi_state'] = JSON.stringify(st);
  return ls;
}

/** défile la fiche (le prototype : `#detailPoster` ; la vraie app : sa couche qui défile, `#dpDefile`) */
async function defiler(pg: Page, s: number): Promise<void> {
  await pg.evaluate((s) => {
    const d = document.getElementById('dpDefile') ?? document.getElementById('detailPoster')!;
    d.scrollTop = s;
  }, s);
  await images(pg, 2);
}

/**
 * la fiche POSÉE des deux côtés : défilée de 120 pt (« Les Mots » en vue), on laisse passer 400 ms réelles et 40 images, jusqu'à deux images
 * identiques de chaque côté — le prototype trace « Les Mots » (son ouvrier du tracé : le temps réel) et sa passe des polices attend la fin de
 * ce tracé (`lot-POLICES`) ; puis on revient en haut
 */
async function poser(P: Page, A: Page): Promise<void> {
  await Promise.all([defiler(P, 120), defiler(A, 120)]);
  let avant: Buffer[] = [];
  for (let k = 0; k < 20; k++) {
    await P.waitForTimeout(400);
    await Promise.all([images(P, 40), images(A, 40)]);
    const im = await Promise.all([image(P), image(A)]);
    if (avant.length && im.every((b, i) => b.equals(avant[i]!))) break;
    avant = im;
  }
  await Promise.all([defiler(P, 0), defiler(A, 0)]);
}

async function image(pg: Page): Promise<Buffer> {
  const clip = await appareil(pg);
  let a = await pg.screenshot({ clip });
  for (let k = 0; k < 4; k++) {
    const b = await pg.screenshot({ clip });
    if (b.equals(a)) return b;
    a = b;
  }
  return a;
}

const etatA = (
  A: Page,
): Promise<{ jonction: { s0: number; coupe: boolean; bornes: { a: number; z: number; m: number } | null } }> =>
  A.evaluate(`${P_}.fiche().etat()`);

/**
 * l'écran entier des deux côtés, comparé au pixel (les zones de fiche.spec.ts, et M4) : rend le nombre de pixels écartés de plus de 2 niveaux, et
 * garde les deux images quand il y en a
 */
async function comparer(P: Page, A: Page, nom: string): Promise<number> {
  const [ip, ia] = await Promise.all([image(P), image(A)]);
  // M4 : le chevron de Peaufiner. Le prototype le retourne (▴) dès que la fiche arrive à 60 pt du bas (le dépli de Peaufiner au défilement,
  // août : `#dpDetails.ouvert`), et Peaufiner ne s'ouvre plus par là depuis S2 — seul le chevron tourne, et reste tourné. La vraie app ne reprend
  // pas ce reste (un chevron qui dit « ouvert » sur un tiroir fermé) : question à Tom, Q626.
  const chev = (await P.evaluate(() => {
    const b = document.getElementById('dpDetails')!;
    if (!b.classList.contains('ouvert')) return null;
    const D = document.getElementById('device')!.getBoundingClientRect();
    const r = b.querySelector('.dpd-tog i')!.getBoundingClientRect();
    return [r.left - D.left - 4, r.top - D.top - 4, r.width + 8, r.height + 8];
  })) as [number, number, number, number] | null;
  // M1 sur sa copie : la bande recopie le haut du champ (0 → 112) — la dalle de l'instant y monte (y 91) ; défilée, cette copie reste en haut
  const copie = (await A.evaluate(() => {
    const d = document.getElementById('dpDefile')!;
    const v = document.querySelector('#detailPoster .fi-champ')?.getAttribute('data-matiere');
    if (!v || d.scrollTop < 0.5) return null;
    const [x, y, w] = v.split(',').map(Number) as [number, number, number];
    return y < 112 ? [x - 8, y - 8, w + 16, 112 - (y - 8)] : null;
  })) as [number, number, number, number] | null;
  const Z = [...(chev ? [chev] : []), ...(copie ? [copie] : []), ...(await zonesFiche(A, P))];
  const n = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
  const mp = masquerFiche(ip, Z, n);
  const ma = masquerFiche(ia, Z, n);
  const e = ecart(mp, ma);
  if (e.n) {
    mkdirSync(RES, { recursive: true });
    writeFileSync(join(RES, `${nom}-prototype.png`), mp);
    writeFileSync(join(RES, `${nom}-app.png`), ma);
  }
  return e.n;
}

for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas] of CAS)
    test(`identité au pixel : la jonction — ${cas}, ${theme}`, async ({ browser }) => {
      const { P, A, erreurs } = await fichesPilotees(browser, avecMots(id, theme), id);
      try {
        // la sonde (sur « identité au pixel : la jonction — Promi à soi, sombre ») : le trait plat de la vraie app posé 1 pt plus bas
        if (sonde('jonction-plat-decale'))
          await A.addStyleTag({ content: '#detailPoster #v195Plat{translate:0 1px!important}' });
        // la sonde (sur « identité au pixel : la jonction — Chiche lancé à Adrien, sombre ») : pas de bande — ce qui monte passe au-dessus du plateau, en vue
        if (sonde('jonction-sans-bande'))
          await A.addStyleTag({ content: '#detailPoster #v187Bande{display:none!important}' });
        const m = (await P.evaluate(() => {
          const d = document.getElementById('detailPoster')!;
          return d.scrollHeight - d.clientHeight;
        })) as number;
        const mA = (await A.evaluate(() => {
          const d = document.getElementById('dpDefile')!;
          return d.scrollHeight - d.clientHeight;
        })) as number;
        expect(mA, 'la même hauteur à défiler').toBe(m);
        await poser(P, A);
        // l'aller (0 → le bout, plus serré à la rencontre), puis le retour
        const aller = [
          0,
          3,
          30,
          60,
          90,
          120,
          123,
          126,
          129,
          132,
          135,
          138,
          141,
          144,
          150,
          160,
          180,
          210,
          240,
          m,
        ].filter((s) => s <= m);
        const pas = [...new Set(aller), ...[200, 140, 130, 60, 0].filter((s) => s <= m)];
        const ecarts: Array<[number, number]> = [];
        for (const s of pas) {
          await Promise.all([defiler(P, s), defiler(A, s)]);
          const n = await comparer(P, A, `${theme}-${String(id)}-${String(s)}`);
          if (n) ecarts.push([s, n]);
        }
        expect(erreurs).toEqual([]);
        expect(ecarts, 'pas de défilement où un pixel s’écarte de plus de 2 niveaux : [défilement, pixels]').toEqual(
          [],
        );
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });

test('le geste accroché ne prend plus le doigt ; décroché, il le reprend (Promi, Chiche)', async ({ browser }) => {
  for (const id of [144, 162]) {
    const { P, A } = await fichesPilotees(browser, avecMots(id, 'sombre'), id);
    try {
      // la sonde : le geste reste actif accroché
      if (sonde('jonction-geste'))
        await A.addStyleTag({ content: '#detailPoster #tenirZone{pointer-events:auto!important}' });
      const lit = (pg: Page): Promise<string> =>
        pg.evaluate(() => getComputedStyle(document.getElementById('tenirZone')!).pointerEvents);
      const s0 = (await etatA(A)).jonction.s0;
      for (const s of [0, Math.floor(s0), Math.ceil(s0 + 0.25) + 1, 200, 40]) {
        await Promise.all([defiler(P, s), defiler(A, s)]);
        // le prototype relit au doigt posé : un pointerdown hors de la zone (sur le plateau) des deux côtés
        for (const pg of [P, A])
          await pg.evaluate(() => {
            window.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
          });
        const [p, a] = await Promise.all([lit(P), lit(A)]);
        expect(a, `défilé de ${String(s)} : le geste ${p === 'none' ? 'coupé' : 'actif'} comme dans le prototype`).toBe(
          p,
        );
      }
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  }
});

test('les places sûres : les bornes et les aimants du prototype (Promi, Chiche)', async ({ browser }) => {
  for (const id of [144, 162]) {
    const { P, A } = await fichesPilotees(browser, avecMots(id, 'sombre'), id);
    try {
      const bp = (await P.evaluate('window._ficheRepos().bornes')) as { a: number; z: number; m: number };
      const ba = (await etatA(A)).jonction.bornes;
      expect(ba, 'les bornes a, z et le défilement possible').toEqual(bp);
      // un geste commence (le doigt posé) : les aimants du prototype — de 6 en 6 jusqu'à a, a, puis de z au bout
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const d = document.getElementById('dpDefile') ?? document.getElementById('detailPoster')!;
          d.dispatchEvent(new TouchEvent('touchstart', { bubbles: true }));
        });
      // la sonde : aucun aimant
      if (sonde('jonction-aimants'))
        await A.evaluate(() => {
          document.querySelector('#detailPoster .v203-aimants')?.remove();
        });
      const lit = (pg: Page): Promise<{ snap: string; pts: number[] }> =>
        pg.evaluate(() => {
          const d = document.getElementById('dpDefile') ?? document.getElementById('detailPoster')!;
          const b = d.querySelector('.v203-aimants');
          return {
            snap: getComputedStyle(d).scrollSnapType,
            pts: b ? [...b.querySelectorAll('i')].map((i) => parseFloat(i.style.top)) : [],
          };
        });
      const [p, a] = await Promise.all([lit(P), lit(A)]);
      expect(a.snap).toBe(p.snap);
      expect(a.pts, 'les aimants').toEqual(p.pts);
      expect(
        a.pts.some((t) => t > bp.a && t < bp.z),
        'aucun aimant entre a et z',
      ).toBe(false);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  }
});

test('tenir une fiche à mots défilée, puis défiler pendant que le vert est posé : comme le prototype (C-311, banc_apres_tenir)', async ({
  browser,
}) => {
  const { P, A, erreurs } = await fichesPilotees(browser, avecMots(144, 'sombre'), 144);
  try {
    // la sonde : la phrase de la célébration posée à sa cote d'écran, sans le défilement (le défaut de v211 : elle montait de 2s)
    if (sonde('celebration-defile'))
      await A.addStyleTag({ content: '#detailPoster #tenirMaree{translate:0 -40px!important}' });
    await poser(P, A);
    // une fiche à mots défile : 40 pt, puis le même geste des deux côtés, sur la vague remontée d'autant
    await Promise.all([defiler(P, 40), defiler(A, 40)]);
    await Promise.all([tracerPilote(P, 150, 360, 42, 303 - 40), tracerPilote(A, 150, 360, 42, 303 - 40)]);
    const ecarts: Array<[string, number]> = [];
    // le rideau posé (1,2 s après le lever), la phrase à sa place
    await Promise.all([images(P, 72), images(A, 72)]);
    let n = await comparer(P, A, 'tenir-40-pose');
    if (n) ecarts.push(['le rideau posé, défilé de 40', n]);
    // pendant que le vert est posé, la fiche défile jusqu'à 200 : il passe sous la bande, jamais au-dessus
    await Promise.all([defiler(P, 200), defiler(A, 200)]);
    n = await comparer(P, A, 'tenir-200-pose');
    if (n) ecarts.push(['le vert posé, défilé jusqu’à 200', n]);
    // « juste après », la fiche toujours défilée, puis revenue en haut : le trait de la fiche tenue à sa place
    await Promise.all([images(P, 180), images(A, 180)]);
    // M5 : au passage à « juste après », la hauteur du contenu du prototype retombe un instant (1 041 pt) et le navigateur y borne son défilement
    // (200 → 197) : un saut de 3 pt, sec (C-271) — la vraie app ne le reprend pas, elle reste où elle est ; on la pose ensuite où est le
    // prototype pour comparer le reste
    const sA = await A.evaluate(() => document.getElementById('dpDefile')!.scrollTop);
    expect(sA, 'la vraie app ne saute pas au passage à « juste après »').toBe(200);
    const sP = (await P.evaluate(() => document.getElementById('detailPoster')!.scrollTop)) as number;
    await defiler(A, sP);
    n = await comparer(P, A, 'tenir-200-apres');
    if (n) ecarts.push(['« juste après », défilé de 200', n]);
    await Promise.all([defiler(P, 0), defiler(A, 0)]);
    n = await comparer(P, A, 'tenir-0-apres');
    if (n) ecarts.push(['« juste après », revenue en haut', n]);
    expect(erreurs).toEqual([]);
    expect(ecarts, 'les instants où un pixel s’écarte de plus de 2 niveaux').toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
