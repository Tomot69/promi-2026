/**
 * LOT 3b-5 — LE DESSIN SUR LA FICHE (redteam_dessin C-042, C-056, C-061 ; redteam_remplace C-086, C-085).
 *
 * Des deux côtés, la même fiche, le même menu photo → « Dessiner », le même trait à la souris (la plume, à l'encre du mode), POSER :
 *  · posé : le dessin REMPLACE la dalle dans la bande (son fond, ses traits, calés en haut, découpés 7 pt au-dessus du trait), l'œil au coin bas
 *    gauche — au pixel ;
 *  · l'œil touché : masqué pour soi (la dalle revient, l'œil barré) — au pixel ;
 *  · ce qui s'écrit : le dessin de la parole (un trait posé, son fond, masqué), comme le prototype.
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTIONS NOMMÉES : celles de la fiche (M1 quand la bande porte la dalle ; M2, M3).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fichesPilotees, images, ecart, sonde, stockageFiches, zonesFiche, masquerFiche, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-dessin');

async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
/** le centre d'un élément qui se voit (sélecteur, et le texte qu'il porte), en pt de l'écran 390 */
async function centre(pg: Page, sel: string, texte?: string): Promise<[number, number]> {
  return pg.evaluate(
    ([s, t]) => {
      const D = document.getElementById('device')!.getBoundingClientRect();
      const k = D.width / 390;
      const e = [...document.querySelectorAll(s!)].find((x) => {
        const q = x.getBoundingClientRect();
        return q.width > 0 && q.height > 0 && (!t || (x.textContent ?? '').trim() === t);
      })!;
      const r = e.getBoundingClientRect();
      return [(r.left + r.width / 2 - D.left) / k, (r.top + r.height / 2 - D.top) / k] as [number, number];
    },
    [sel, texte ?? ''] as const,
  );
}
async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
}

for (const theme of ['sombre', 'clair'] as const)
  test(`le dessin sur une fiche, comme le prototype — posé dans la bande, masqué par l’œil (C-042, C-086), ${theme}`, async ({
    browser,
  }) => {
    const id = 144;
    const ls: Record<string, string> = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
    try {
      // la sonde (sur « le dessin sur une fiche … , sombre ») : le dessin posé n'est pas peint dans la bande (la dalle y reste)
      if (sonde('dessin-fiche-absent'))
        await A.addStyleTag({ content: '#detailPoster .dz-bande{display:none!important}' });
      // la sonde (sur « le dessin sur une fiche … , clair ») : l'œil ne masque rien
      if (sonde('oeil-sourd'))
        await A.addStyleTag({ content: '#detailPoster .dz-oeil{pointer-events:none!important}' });
      mkdirSync(RES, { recursive: true });
      const juge = async (quoi: string): Promise<void> => {
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 20; k++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          // M1 n'est masqué que quand la bande montre la dalle (pas un dessin)
          const dessin = await A.evaluate(() => !!document.querySelector('#detailPoster .dz-bande'));
          const nM =
            ((await A.evaluate(
              () => !!document.querySelector('#detailPoster.fiche .fi-champ')?.getAttribute('data-matiere'),
            ))
              ? 1
              : 0) +
            ((await P.evaluate(() => !!document.getElementById('dpTrameCv')?.getAttribute('data-matiere'))) ? 1 : 0);
          const Z = (await zonesFiche(A, P)).slice(dessin ? nM : 0);
          const n = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
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
      // le menu photo → « Dessiner »
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .ph-photo-btn');
        await toucher(pg, x, y);
        await images(pg, 30);
        const [x2, y2] = await centre(pg, '#detailPoster .ph-photo-menu button', 'Dessiner');
        await toucher(pg, x2, y2);
        await images(pg, 60);
      }
      // un trait à la plume (la souris), puis POSER
      for (const pg of [P, A]) {
        const r = await pg.evaluate(() => {
          const b = document.getElementById('device')!.getBoundingClientRect();
          return { x: b.left, y: b.top, k: b.width / 390 };
        });
        // le trait : des événements de pointeur posés dans la page, d'un seul bloc — les mêmes points des deux côtés, sans dépendre de la charge
        // de la machine (le trait s'affine avec la vitesse du geste, lue sur `timeStamp` : à la souris, elle variait d'un côté à l'autre)
        await pg.evaluate((r) => {
          const pts: Array<[number, number]> = [];
          for (let x = 80; x <= 300; x += 10) pts.push([x, 200 + Math.sin(x / 30) * 30]);
          const X = (x: number): number => r.x + x * r.k;
          const Y = (y: number): number => r.y + y * r.k;
          const cible = document.elementFromPoint(X(80), Y(200)) ?? document.body;
          const ev = (type: string, [x, y]: [number, number]): void => {
            cible.dispatchEvent(
              new PointerEvent(type, {
                bubbles: true,
                cancelable: true,
                composed: true,
                clientX: X(x),
                clientY: Y(y),
                pointerId: 1,
                pointerType: 'mouse',
                isPrimary: true,
                buttons: type === 'pointerup' ? 0 : 1,
              }),
            );
          };
          ev('pointerdown', [80, 200]);
          for (const q of pts) ev('pointermove', q);
          ev('pointerup', pts[pts.length - 1]!);
        }, r);
        await images(pg, 20);
        const [x2, y2] = await centre(pg, '#dessinMode [data-outil="poser"], #dessinMode .dz-poser');
        await toucher(pg, x2, y2);
        await images(pg, 60);
      }
      await juge('pose');
      // l'œil : masqué pour soi
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .dz-oeil');
        await toucher(pg, x, y);
      }
      await Promise.all([images(P, 30), images(A, 30)]);
      await juge('masque');
      // ce qui s'écrit : le dessin de la parole
      const p = (await P.evaluate(
        `JSON.stringify((d => [d.poses.length, d.fond, !!d.masque, d.pose])(promises.find(q => q.id === ${String(id)}).dessin))`,
      )) as string;
      const a = (await A.evaluate(
        `JSON.stringify((d => [d.poses.length, d.fond, !!d.masque, d.pose])(${P_}.magasin.etat().paroles.find(q => q.id === ${String(id)}).suite.dessin))`,
      )) as string;
      expect(a, 'le dessin posé, masqué, comme le prototype').toBe(p);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
