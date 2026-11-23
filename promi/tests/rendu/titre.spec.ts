/**
 * LOT 3a-4 — LE TITRE MODIFIABLE (redteam_titre_fiche, redteam_titre_encart, redteam_renomme, redteam_textes_longs D). Des deux côtés, l'horloge
 * pilotée et les animations CSS gelées (aides.ts, `fichesPilotees`), le même toucher au même point du titre :
 *  · un titre coupé (« … ») se DÉPLIE au premier toucher — au pixel à mi-mouvement et à la fin (C-244) ;
 *  · le second toucher le MODIFIE (C-280) : le titre devient modifiable, et l'écran est celui du prototype en modification — aucun encart (§1) ;
 *  · taper puis Retour : le titre neuf, dans la parole et à l'écran comme dans le prototype ; la clé de plantation gardée, et la dalle n'a pas
 *    changé de forme (Q621) ; Échap, ou le titre vidé : l'ancien revient.
 * Le curseur clignote : il est rendu transparent des deux côtés pendant les captures (c'est le seul pixel qui clignote, C-280 §1).
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
  P_,
} from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'titre');
const LONG =
  'rendre le livre à Marion avant la fin du mois, avec un mot glissé dedans pour la remercier de me l’avoir prêté si longtemps, et lui dire ce que j’en ai pensé, chapitre après chapitre, sans rien oublier';

/** le stockage des fiches, la parole 144 sous un titre donné ; `monde` : le monde du Studio */
function stockage(titre: string | null, monde?: string): Record<string, string> {
  const ls: Record<string, string> = { ...stockageFiches(), promi_theme: 'dark' };
  if (monde) {
    // le monde du Studio, et la Toile « sans texte » : les titres écrits sur les dalles ne comptent pas dans la forme jugée (Q621)
    const st = JSON.parse(ls['promi_state']!) as { state: { structure: string; labels: boolean } };
    st.state.structure = monde;
    st.state.labels = false;
    ls['promi_state'] = JSON.stringify(st);
  }
  if (titre != null) {
    const st = JSON.parse(ls['promi_state']!) as { promises: Array<{ id: number; title: string; cle?: string }> };
    const p = st.promises.find((q) => q.id === 144)!;
    p.title = titre;
    p.cle = titre;
    ls['promi_state'] = JSON.stringify(st);
  }
  return ls;
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

async function comparer(P: Page, A: Page, nom: string): Promise<number> {
  const [ip, ia] = await Promise.all([image(P), image(A)]);
  const Z = await zonesFiche(A, P);
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

/** un toucher au point (x, y) du titre, exprimé en fraction de sa boîte : la souris, le même point des deux côtés */
async function toucherTitre(pg: Page, fx = 0.3, fy = 0.5): Promise<void> {
  const r = (await pg.evaluate(() => {
    const t = document.querySelector('#detailPoster .fi-titre') ?? document.getElementById('dptTitre')!;
    const b = t.getBoundingClientRect();
    return [b.left, b.top, b.width, Math.min(b.height, 60)];
  })) as [number, number, number, number];
  await pg.mouse.click(r[0] + r[2] * fx, r[1] + r[3] * fy);
}

const CURSEUR = '#detailPoster [contenteditable]{caret-color:transparent!important}';
type T = { title: string; cle: string | undefined };
const titreApp = (A: Page): Promise<T> =>
  A.evaluate(
    `(() => { const p = ${P_}.magasin.etat().paroles.find((q) => q.id === 144); return { title: p.title, cle: p.cle }; })()`,
  );
// dans le prototype, `promises` est une variable de script (pas une propriété de window) : lue par une expression
const titreProto = (P: Page): Promise<T> =>
  P.evaluate('(() => { const p = promises.find((q) => q.id === 144); return { title: p.title, cle: p.cle }; })()');
const edite = (pg: Page): Promise<boolean> =>
  pg.evaluate(() => {
    const t = document.querySelector<HTMLElement>('#detailPoster .fi-titre') ?? document.getElementById('dptTitre')!;
    return t.isContentEditable && document.activeElement === t;
  });

test('un titre coupé se déplie au premier toucher, comme le prototype — à mi-mouvement et posé (C-244)', async ({
  browser,
}) => {
  const { P, A, erreurs } = await fichesPilotees(browser, stockage(LONG), 144);
  try {
    // la sonde : le dépliage sans mouvement (posé d'un coup)
    if (sonde('titre-deplie-sec'))
      await A.evaluate(() => {
        window.matchMedia = ((q: string) => ({
          matches: q.includes('reduce'),
          media: q,
        })) as unknown as typeof matchMedia;
      });
    for (const pg of [P, A]) await pg.addStyleTag({ content: CURSEUR });
    const coupe = await A.evaluate(
      () => document.querySelector<HTMLElement>('#detailPoster .fi-titre')!.dataset['coupe'],
    );
    expect(coupe, 'le titre est coupé').toBe('1');
    await Promise.all([toucherTitre(P), toucherTitre(A)]);
    expect(await edite(A), 'le premier toucher déplie, il ne modifie pas').toBe(false);
    const ecarts: Array<[string, number]> = [];
    await Promise.all([images(P, 10), images(A, 10)]);
    let n = await comparer(P, A, 'deplie-mi');
    if (n) ecarts.push(['à mi-mouvement', n]);
    await Promise.all([images(P, 40), images(A, 40)]);
    n = await comparer(P, A, 'deplie-pose');
    if (n) ecarts.push(['posé', n]);
    expect(erreurs).toEqual([]);
    expect(ecarts).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('le second toucher modifie un titre coupé, sans aucun encart : l’écran du prototype en modification (C-280 §1)', async ({
  browser,
}) => {
  const { P, A, erreurs } = await fichesPilotees(browser, stockage(LONG), 144);
  try {
    for (const pg of [P, A]) await pg.addStyleTag({ content: CURSEUR });
    // la sonde : un contour autour du titre en modification (l'anneau de focus de WebKit)
    if (sonde('titre-encart'))
      await A.addStyleTag({ content: '#detailPoster .fi-titre.ti-edition{outline:2px solid #fff!important}' });
    await Promise.all([toucherTitre(P), toucherTitre(A)]);
    await Promise.all([images(P, 40), images(A, 40)]);
    await Promise.all([toucherTitre(P, 0.2, 0.3), toucherTitre(A, 0.2, 0.3)]);
    await Promise.all([images(P, 4), images(A, 4)]);
    expect([await edite(P), await edite(A)], 'en modification des deux côtés').toEqual([true, true]);
    expect(await comparer(P, A, 'edition'), 'pixels écartés en modification').toBe(0);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('Retour renomme comme le prototype : le titre neuf partout, la clé de plantation gardée, la dalle garde sa forme (C-280, Q621)', async ({
  browser,
}) => {
  // sous Brouillamini, l'un des onze mondes où la forme d'une dalle se tire de son titre (Q621) ; un titre court : la dalle est dans sa boîte
  const { P, A, erreurs } = await fichesPilotees(browser, stockage(null, 'brouillamini'), 144, {
    // la sonde : le moteur lit le titre au lieu de la clé de plantation (la dalle change de forme quand on renomme)
    ...(sonde('renomme-sans-cle') && {
      avantA: () => {
        let v: Array<Record<string, unknown>> = [];
        Object.defineProperty(window, 'promises', {
          configurable: true,
          get: () => v,
          set: (x: Array<Record<string, unknown>>) => {
            v = x.map((p) => ({ ...p, cle: undefined }));
          },
        });
      },
    }),
  });
  try {
    for (const pg of [P, A]) await pg.addStyleTag({ content: CURSEUR });
    // la Toile sous la fiche, posée : la vie au repos coupée (`_vivantOff`, comme le banc de rendu — sous Linux un mouvement de repos tombait
    // entre les deux captures), puis deux images identiques
    await A.evaluate(() => {
      (window as unknown as { _vivantOff: boolean })._vivantOff = true;
    });
    const toile = (): Promise<string> =>
      A.evaluate(() => (document.getElementById('toileCv') as HTMLCanvasElement).toDataURL());
    let d0 = await toile();
    for (let k = 0; k < 10; k++) {
      await images(A, 2);
      const d = await toile();
      if (d === d0) break;
      d0 = d;
    }
    const cle0 = (await titreApp(A)).cle;
    await Promise.all([toucherTitre(P), toucherTitre(A)]);
    await Promise.all([images(P, 4), images(A, 4)]);
    expect([await edite(P), await edite(A)], 'en modification au premier toucher (un titre entier)').toEqual([
      true,
      true,
    ]);
    for (const pg of [P, A]) {
      // le curseur à la fin du texte (« Fin » ne va qu'au bout de la ligne affichée)
      await pg.evaluate(() => {
        const t = document.activeElement!;
        const r = document.createRange();
        r.selectNodeContents(t);
        r.collapse(false);
        getSelection()!.removeAllRanges();
        getSelection()!.addRange(r);
      });
      await pg.keyboard.type(' demain');
      await pg.keyboard.press('Enter');
    }
    await Promise.all([images(P, 60), images(A, 60)]);
    const [tp, ta] = await Promise.all([titreProto(P), titreApp(A)]);
    expect(ta.title, 'le titre neuf, comme dans le prototype').toBe(tp.title);
    expect(ta.title.endsWith(' demain')).toBe(true);
    expect(ta.cle, 'la clé de plantation gardée (Q621)').toBe(cle0);
    // le renommage repeint la Toile (`Toile.redraw`) : sous Brouillamini, la forme et l'ampleur de la dalle se tiraient du titre — elles se
    // tirent de la clé de plantation, la Toile est la même au pixel
    expect(await toile(), 'la Toile n’a pas changé : la dalle garde sa forme (Q621)').toBe(d0);
    expect(await edite(A), 'sorti de la modification').toBe(false);
    expect(await comparer(P, A, 'renomme'), 'pixels écartés une fois renommée').toBe(0);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('Échap, ou le titre vidé : l’ancien revient ; un titre entier se modifie au premier toucher (C-280)', async ({
  browser,
}) => {
  const { P, A, erreurs } = await fichesPilotees(browser, stockage(null), 144);
  try {
    const avant = (await titreApp(A)).title;
    // la sonde : le titre entier pris pour un titre coupé (le premier toucher déplierait)
    if (sonde('titre-entier-deplie'))
      await A.evaluate(() => {
        document.querySelector<HTMLElement>('#detailPoster .fi-titre')!.dataset['coupe'] = '1';
      });
    // un titre entier : le premier toucher modifie
    await Promise.all([toucherTitre(P), toucherTitre(A)]);
    await Promise.all([images(P, 4), images(A, 4)]);
    expect([await edite(P), await edite(A)], 'en modification au premier toucher').toEqual([true, true]);
    for (const pg of [P, A]) {
      await pg.keyboard.type('xyz');
      await pg.keyboard.press('Escape');
    }
    await Promise.all([images(P, 30), images(A, 30)]);
    expect((await titreApp(A)).title, 'Échap : l’ancien titre').toBe(avant);
    expect((await titreProto(P)).title).toBe(avant);
    // vidé puis Retour : l'ancien revient (en se traçant)
    await Promise.all([toucherTitre(P), toucherTitre(A)]);
    await Promise.all([images(P, 4), images(A, 4)]);
    for (const pg of [P, A]) {
      await pg.evaluate(() => {
        const r = document.createRange();
        r.selectNodeContents(document.activeElement!);
        getSelection()!.removeAllRanges();
        getSelection()!.addRange(r);
      });
      await pg.keyboard.press('Backspace');
      await pg.keyboard.press('Enter');
    }
    await Promise.all([images(P, 120), images(A, 120)]);
    expect((await titreApp(A)).title, 'vidé : l’ancien titre').toBe(avant);
    expect((await titreProto(P)).title).toBe(avant);
    expect(await A.evaluate(() => document.querySelector('#detailPoster .fi-titre')!.textContent)).toBe(avant);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
