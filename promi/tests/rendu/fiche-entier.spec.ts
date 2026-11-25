/**
 * LOT 3b-4 — LA PHOTO D'UNE FICHE EN ENTIER ET CADRÉE AU DOIGT (redteam_entier C-051, redteam_cadre C-085, redteam_tourne C-098, C-091).
 *
 * Des deux côtés, la même fiche et la même photo (posée par le bouton photo, comme fiche-photo.spec) :
 *  · un toucher sur la bande : la photo en entier, sur la seiche pleine, le X et « Enregistrer » — au pixel ;
 *  · un nouveau toucher : refermée, la fiche telle qu'elle était — au pixel ;
 *  · un glissement d'un doigt, puis un pincement de deux doigts qui écarte et tourne : le cadrage écrit (z, dx, dy, a) comme le prototype, à 0,01
 *    près, et la bande cadrée au pixel.
 * Les touchers à deux doigts sont des `touchstart` / `touchmove` / `touchend` posés dans la page (leurs `touches`), les mêmes des deux côtés.
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTIONS NOMMÉES : celles de la fiche (M2, M3 ; M1 n'est pas posé : la bande porte
 * la photo, pas de la matière).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fichesPilotees, images, ecart, sonde, stockageFiches, zonesFiche, masquerFiche, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-entier');

async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
}
/** un geste de doigts posé dans la page : chaque pas, la liste des doigts (en pt de l'écran 390) ; `touchstart` au premier, `touchend` à la fin */
async function doigts(pg: Page, pas: Array<Array<[number, number]>>): Promise<void> {
  await pg.evaluate((pas) => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const ev = (type: string, L: Array<[number, number]>, cible: Element): void => {
      const touches = L.map(([x, y], i) => ({
        identifier: i,
        clientX: D.left + x * k,
        clientY: D.top + y * k,
        target: cible,
      }));
      const e = new Event(type, { bubbles: true, cancelable: true });
      Object.defineProperty(e, 'touches', { value: touches });
      Object.defineProperty(e, 'changedTouches', { value: touches });
      cible.dispatchEvent(e);
    };
    const [x0, y0] = pas[0]![0]!;
    const cible = document.elementFromPoint(D.left + x0 * k, D.top + y0 * k) ?? document.body;
    let avant: Array<[number, number]> = [];
    for (const L of pas) {
      // un doigt de plus : un `touchstart` ; sinon un `touchmove`
      ev(L.length > avant.length ? 'touchstart' : 'touchmove', L, cible);
      avant = L;
    }
    ev('touchend', [], cible);
  }, pas);
}

for (const theme of ['sombre', 'clair'] as const)
  test(`la photo d’une fiche en entier, puis cadrée au doigt, comme le prototype (C-051, C-085, C-098), ${theme}`, async ({
    browser,
  }) => {
    const id = 144;
    const ls: Record<string, string> = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
    try {
      // la sonde (sur « la photo d'une fiche en entier … , sombre ») : la vue en entier sur un fond translucide (la fiche transparaît)
      if (sonde('entier-translucide'))
        await A.addStyleTag({ content: '#device #entierVue{background:rgba(5,3,2,.85)!important}' });
      // la sonde (sur « la photo d'une fiche en entier … , clair ») : le pincement ne tourne pas la photo
      if (sonde('pince-sans-tour'))
        await A.evaluate(() => {
          Math.atan2 = (): number => 0;
        });
      for (const pg of [P, A]) await pg.addStyleTag({ content: '#device input{caret-color:transparent!important}' });
      mkdirSync(RES, { recursive: true });
      const juge = async (quoi: string): Promise<void> => {
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 20; k++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          const photo = await A.evaluate(
            () => document.getElementById('dpTrameCv')?.getAttribute('data-photo') === '1',
          );
          const nM =
            ((await A.evaluate(
              () => !!document.querySelector('#detailPoster.fiche .fi-champ')?.getAttribute('data-matiere'),
            ))
              ? 1
              : 0) +
            ((await P.evaluate(() => !!document.getElementById('dpTrameCv')?.getAttribute('data-matiere'))) ? 1 : 0);
          const entier = await A.evaluate(() => !!document.querySelector('#entierVue.ouv'));
          const Z = entier ? [] : (await zonesFiche(A, P)).slice(photo ? nM : 0);
          const n = entier
            ? 0
            : await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
          const [p2, a2] = [masquerFiche(await image(P), Z, n), masquerFiche(await image(A), Z, n)];
          const pose = k > 1 && p2.equals(ip) && a2.equals(ia);
          [ip, ia] = [p2, a2];
          if (pose) break;
        }
        writeFileSync(join(RES, `${theme}-${quoi}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${quoi}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(
          { n: e.n, boite: e.boite },
          `${quoi} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      };
      // la photo, posée par le bouton photo (fiche-photo.spec)
      const png = Buffer.from(
        (
          (await A.evaluate(() => {
            const c = document.createElement('canvas');
            c.width = 300;
            c.height = 200;
            const g = c.getContext('2d')!;
            const C = ['#E4572E', '#29335C', '#F3A712', '#A8C686', '#669BBC', '#F0EAD6'];
            for (let i = 0; i < 6; i++)
              for (let j = 0; j < 4; j++) {
                g.fillStyle = C[(i + j) % 6]!;
                g.fillRect(i * 50, j * 50, 50, 50);
              }
            return c.toDataURL('image/png');
          })) as string
        ).split(',')[1]!,
        'base64',
      );
      await P.setInputFiles('#detailPoster .ph-photo-in', { name: 'photo.png', mimeType: 'image/png', buffer: png });
      await A.setInputFiles('#detailPoster .fi-photo-in', { name: 'photo.png', mimeType: 'image/png', buffer: png });
      await Promise.all([images(P, 60), images(A, 60)]);
      await juge('photo');
      // un toucher sur la bande (le cœur de la photo) : en entier
      await Promise.all([toucher(P, 195, 180), toucher(A, 195, 180)]);
      await Promise.all([images(P, 30), images(A, 30)]);
      // (hors du Mac de Tom, la vue s'ouvre quelques images plus tard : on l'attend, 5 s au plus)
      await expect
        .poll(() => A.evaluate(() => !!document.querySelector('#entierVue.ouv')), {
          message: 'la photo en entier',
          timeout: 5000,
        })
        .toBe(true);
      await juge('entier');
      // un nouveau toucher : refermée
      await Promise.all([toucher(P, 195, 420), toucher(A, 195, 420)]);
      await Promise.all([images(P, 30), images(A, 30)]);
      expect(await A.evaluate(() => !!document.querySelector('#entierVue.ouv')), 'refermée').toBe(false);
      await juge('refermee');
      // un glissement d'un doigt (40 pt vers la droite, 20 vers le bas), puis un pincement qui écarte et tourne
      const glisse: Array<Array<[number, number]>> = [[[195, 180]]];
      for (let i = 1; i <= 8; i++) glisse.push([[195 + 5 * i, 180 + 2.5 * i]]);
      const pince: Array<Array<[number, number]>> = [
        [[165, 170]],
        [
          [165, 170],
          [225, 190],
        ],
      ];
      for (let i = 1; i <= 8; i++) {
        const a = (i / 8) * 0.35;
        const d = 30 + i * 4;
        pince.push([
          [195 - d * Math.cos(a), 180 - d * Math.sin(a)],
          [195 + d * Math.cos(a), 180 + d * Math.sin(a)],
        ]);
      }
      for (const pg of [P, A]) {
        await doigts(pg, glisse);
        await images(pg, 40);
        await doigts(pg, pince);
      }
      await Promise.all([images(P, 60), images(A, 60)]);
      const cp = (await P.evaluate(
        `JSON.stringify((c => [c.z, c.dx, c.dy, c.a || 0].map(v => Math.round(v * 100) / 100))(promises.find(q => q.id === ${String(id)}).photoCadre))`,
      )) as string;
      const ca = (await A.evaluate(
        `JSON.stringify((c => [c.z, c.dx, c.dy, c.a || 0].map(v => Math.round(v * 100) / 100))(${P_}.magasin.etat().paroles.find(q => q.id === ${String(id)}).suite.photoCadre))`,
      )) as string;
      expect(JSON.parse(cp)[3], 'le prototype a tourné la photo').not.toBe(0);
      expect(ca, 'le cadrage écrit (z, dx, dy, a), comme le prototype').toBe(cp);
      await juge('cadree');
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
