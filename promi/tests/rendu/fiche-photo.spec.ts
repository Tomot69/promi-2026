/**
 * LOT 3b-3 — LE BOUTON PHOTO D'UNE FICHE : IDENTITÉ AU PIXEL ET CE QUI S'ÉCRIT (redteam_photo_menu, redteam_origine, redteam_photo).
 *
 * Des deux côtés, la même fiche (le banc : `etat-fiches.json` ; la parole plantée sous Touffe, le Studio sous Encre — sa dalle d'origine n'est
 * pas celle du Studio), le même toucher sur le bouton photo, la même photo importée, les mêmes choix :
 *  · le menu ouvert : « Dessiner », « Importer une photo », « La dalle d'origine » (compact, à gauche du bouton) ;
 *  · la photo importée : elle remplace la dalle, en couverture, bornée par l'onde ; le bouton porte le signe du retour ;
 *  · « La dalle d'origine » : la photo retirée, la dalle dans le monde de sa plantation (sa couleur, ou la rampe de Q30 si elle se confond avec
 *    le champ, Q365) ; puis « La dalle du Studio » la rend.
 * Clair et sombre. Tolérance : 2 niveaux, 0 pixel au-delà (Q616 hors du Mac).
 * EXCEPTIONS NOMMÉES : celles de la fiche (fiche.spec : M1 la matière de la dalle, M2, M3) — la photo, posée dans la boîte de la dalle, est
 * jugée hors de M1 (elle n'est pas de la matière : M1 est retiré quand une photo est posée) ; « Dessiner », inactif dans la vraie app jusqu'au
 * 3b-5, est dessiné comme dans le prototype. La dalle d'origine, sous M1, est jugée par la décision que les deux côtés déclarent (Q365 : « origine »
 * ou « rampe », et le ΔE au champ) — c'est elle qui a pris la dalle de la fiche rendue en clair (C-132 : comme en sombre, dans les deux thèmes).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fichesPilotees, images, ecart, sonde, stockageFiches, zonesFiche, masquerFiche, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-photo');

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
/** les entrées du menu, telles qu'elles se voient : leur mot, leur boîte (au demi-point), leurs couleurs, leur police — M1 en recouvre une part */
async function entrees(pg: Page): Promise<string[]> {
  return pg.evaluate(() => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const r2 = (v: number): number => Math.round(v * 2) / 2;
    return [...document.querySelectorAll<HTMLElement>('#detailPoster .ph-photo-menu button')].map((b) => {
      const r = b.getBoundingClientRect();
      const c = getComputedStyle(b);
      return [
        (b.textContent ?? '').trim(),
        r2((r.left - D.left) / k),
        r2((r.top - D.top) / k),
        r2(r.width / k),
        r2(r.height / k),
        c.color,
        c.backgroundColor,
        c.borderTopColor,
        c.borderTopWidth,
        c.fontFamily.split(',')[0],
        c.fontSize,
        c.textTransform,
      ].join(' · ');
    });
  });
}
async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
}

for (const theme of ['sombre', 'clair'] as const)
  test(`le bouton photo d’une fiche, comme le prototype — le menu, la photo importée, la dalle d’origine (v117, Q365), ${theme}`, async ({
    browser,
  }) => {
    const id = 144;
    const ls: Record<string, string> = {
      ...stockageFiches(),
      promi_theme: theme === 'clair' ? 'light' : 'dark',
    };
    const st = JSON.parse(ls['promi_state']!) as { promises: { id: number; monde?: unknown }[] };
    st.promises.find((p) => p.id === id)!.monde = { m: 'touffe', p: 'signal', h: 0 };
    ls['promi_state'] = JSON.stringify(st);
    const { P, A, erreurs } = await fichesPilotees(browser, ls, id, {
      // la sonde (sur « le bouton photo d'une fiche … , clair ») : la dalle de la fiche rendue dans le thème de l'app, pas comme en sombre (C-132)
      ...(sonde('dalle-fiche-en-clair') && {
        avantA: () => {
          Object.defineProperty(window, '_shThemeOverride', {
            configurable: true,
            get: () => null,
            set: () => undefined,
          });
        },
      }),
    });
    try {
      // la sonde (sur « le bouton photo d'une fiche … , sombre ») : le menu n'est pas compact (44 pt par entrée au lieu de 33)
      if (sonde('menu-photo-large'))
        await A.addStyleTag({ content: '#detailPoster .ph-photo-menu button{height:44px!important}' });
      // la sonde (sur « le bouton photo d'une fiche … , clair ») : « La dalle d'origine » oublie la photo (elle reste posée)
      if (sonde('origine-garde-photo'))
        await A.evaluate(() => {
          const m = (window as unknown as { __promi: { magasin: { photo(...a: unknown[]): void } } }).__promi.magasin;
          const f = m.photo.bind(m);
          m.photo = (i: unknown, o: { origine?: boolean; photo?: unknown }) => {
            if (o.origine !== undefined) {
              const p = (
                window as unknown as {
                  __promi: { magasin: { etat(): { paroles: { id: unknown; suite?: Record<string, unknown> }[] } } };
                }
              ).__promi.magasin
                .etat()
                .paroles.find((q) => q.id === i);
              const ph = p?.suite?.['photo'];
              f(i, o);
              if (typeof ph === 'string') f(i, { photo: ph });
              return;
            }
            f(i, o);
          };
        });
      mkdirSync(RES, { recursive: true });
      const juge = async (quoi: string): Promise<void> => {
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 20; k++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          // les exceptions de la fiche ; la matière (M1) n'est masquée que quand la bande porte la dalle, pas une photo
          const photo = await A.evaluate(
            () => document.getElementById('dpTrameCv')?.getAttribute('data-photo') === '1',
          );
          // M1 : une zone par côté qui déclare sa matière (`data-matiere`), en tête de la liste
          const nM =
            ((await A.evaluate(
              () => !!document.querySelector('#detailPoster.fiche .fi-champ')?.getAttribute('data-matiere'),
            ))
              ? 1
              : 0) +
            ((await P.evaluate(() => !!document.getElementById('dpTrameCv')?.getAttribute('data-matiere'))) ? 1 : 0);
          const Z = (await zonesFiche(A, P)).slice(photo ? nM : 0);
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
      // le menu
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .ph-photo-btn');
        await toucher(pg, x, y);
      }
      await Promise.all([images(P, 40), images(A, 40)]);
      await juge('menu');
      expect(await entrees(A), 'le menu : ses entrées, comme le prototype').toEqual(await entrees(P));
      // la photo importée (la même image des deux côtés : un damier de couleurs pleines, sans lissage)
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
      // le menu se referme en touchant « Importer une photo » ; le sélecteur du téléphone : le fichier lui est donné
      await P.setInputFiles('#detailPoster .ph-photo-in', { name: 'photo.png', mimeType: 'image/png', buffer: png });
      await A.setInputFiles('#detailPoster .fi-photo-in', { name: 'photo.png', mimeType: 'image/png', buffer: png });
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .ph-photo-menu button', 'Importer une photo');
        await pg.evaluate(() => {
          // le clic sur le bouton ouvrirait le sélecteur du système : on le neutralise, le fichier est déjà donné
          HTMLInputElement.prototype.click = function () {
            /* rien */
          };
        });
        await toucher(pg, x, y);
      }
      await Promise.all([images(P, 60), images(A, 60)]);
      await juge('photo');
      // « La dalle d'origine » : la photo retirée, la dalle dans le monde de sa plantation
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .ph-photo-btn');
        await toucher(pg, x, y);
      }
      await Promise.all([images(P, 40), images(A, 40)]);
      await juge('menu-photo');
      expect(await entrees(A), 'le menu, une photo posée : ses entrées, comme le prototype').toEqual(await entrees(P));
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .ph-photo-menu button', 'La dalle d’origine');
        await toucher(pg, x, y);
      }
      await Promise.all([images(P, 60), images(A, 60)]);
      await juge('origine');
      // la dalle d'origine est sous M1 : sa décision (Q365, « origine » ou « rampe », et le ΔE au champ), déclarée des deux côtés, se compare
      const dp = await P.evaluate(() => document.getElementById('dpTrameCv')!.getAttribute('data-origine'));
      const da = await A.evaluate(() =>
        document.querySelector('#detailPoster.fiche .fi-champ')!.getAttribute('data-origine'),
      );
      expect(dp, 'le prototype déclare sa décision').toMatch(/^(origine|rampe)\|/);
      expect(da, 'la dalle d’origine : la même décision (Q365), le même ΔE').toBe(dp);
      // ce qui s'écrit : l'option, la photo retirée
      const p = (await P.evaluate(
        `JSON.stringify((p => [!!p.dalleOrigine, !!p.photo])(promises.find(q => q.id === ${String(id)})))`,
      )) as string;
      const a = (await A.evaluate(
        `JSON.stringify((p => [!!(p.suite||{}).dalleOrigine, !!(p.suite||{}).photo])(${P_}.magasin.etat().paroles.find(q => q.id === ${String(id)})))`,
      )) as string;
      expect(a, 'la dalle d’origine choisie, la photo retirée, comme le prototype').toBe(p);
      expect(p).toBe('[true,false]');
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
