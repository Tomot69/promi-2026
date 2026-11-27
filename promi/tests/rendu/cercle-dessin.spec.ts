/**
 * LE DESSIN D'UN CERCLE (C-042, v132 : « la fiche d'un Cercle reçoit son bouton photo (il ouvre « Dessiner ») » ; lot-V132-DESSIN `boutonCercle`,
 * `_photoMenu` d'un Cercle, `bande` ; le prototype garde le dessin par Cercle dans `promi_dessins_cercle`).
 *
 * Des deux côtés, la fiche du Cercle « Marseille », le même bouton photo → son menu (un Cercle ne porte pas de photo : « Dessiner » seul), le même
 * trait, POSER :
 *  · posé : le dessin REMPLACE les dalles du Cercle dans la bande, l'œil au coin bas gauche — au pixel ;
 *  · l'œil touché : masqué pour soi (les dalles reviennent) — au pixel ;
 *  · ce qui s'écrit : le dessin du Cercle (posé, son fond, masqué), comme le prototype ; et le menu rouvert porte « Retirer le dessin ».
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTIONS NOMMÉES : celles de la fiche d'un Cercle (cercle.spec : M1 la bande quand
 * elle porte les dalles, les mini-dalles du fil ; M2 le grain des anneaux).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, images, ecart, sonde, stockageCercles, masquerFiche, type Zone, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'cercle-dessin');

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
/** les mots du menu photo ouvert */
const menu = (pg: Page): Promise<string[]> =>
  pg.evaluate(() =>
    [...document.querySelectorAll('#detailPoster .ph-photo-menu button')]
      .filter((b) => b.getBoundingClientRect().width > 0)
      .map((b) => (b.textContent ?? '').trim()),
  );

async function zones(A: Page, P: Page, bande: boolean): Promise<{ Z: Zone[]; n: number }> {
  const z: Zone[] = [];
  for (const pg of [A, P])
    z.push(
      ...((await pg.evaluate((b) => {
        const D = document.getElementById('device')!.getBoundingClientRect();
        const k = D.width / 390 || 1;
        const out: number[][] = [];
        const cv = document.getElementById('dpTrameCv');
        const v = cv?.getAttribute('data-matiere');
        if (b && cv && v) {
          const c = cv.getBoundingClientRect();
          const [x, y, w, h] = v.split(',').map(Number) as [number, number, number, number];
          out.push([(c.left - D.left) / k + x - 8, (c.top - D.top) / k + y - 8, w + 16, h + 16]);
        }
        for (const d of document.querySelectorAll('#detailPoster .nf-d')) {
          const r = d.getBoundingClientRect();
          out.push([(r.left - D.left) / k - 8, (r.top - D.top) / k - 8, r.width / k + 16, r.height / k + 16]);
        }
        return out;
      }, bande)) as Zone[]),
    );
  const anneaux = (await A.evaluate(() => {
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    return [...document.querySelectorAll('#detailPoster.fiche canvas.kr-c')].map((c) => {
      const r = c.getBoundingClientRect();
      return [(r.left - D.left) / k, (r.top - D.top) / k, r.width / k, r.height / k];
    });
  })) as Zone[];
  return { Z: [...z, ...anneaux], n: anneaux.length };
}

// les titres (les sondes les nomment) :
//   « le dessin d'un Cercle, comme le prototype — … sombre » (dessin-cercle-absent)
for (const theme of ['sombre', 'clair'] as const)
  test(`le dessin d'un Cercle, comme le prototype — posé dans la bande à la place de ses dalles, masqué par l’œil (C-042), ${theme}`, async ({
    browser,
  }) => {
    const ls = { ...stockageCercles(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      // la sonde (sur « … , sombre ») : le dessin posé n'est pas peint dans la bande (les dalles y restent)
      if (theme === 'sombre' && sonde('dessin-cercle-absent'))
        await A.addStyleTag({ content: '#detailPoster .dz-bande{display:none!important}' });
      await P.evaluate(() => (window as unknown as { openNueeDetail(k: string): void }).openNueeDetail('n1'));
      await A.evaluate(`${P_}.fiche().ouvrirCercle('n1')`);
      for (let i = 0; i < 4; i++) await Promise.all([images(P, 40), images(A, 40)]);
      mkdirSync(RES, { recursive: true });
      const dv = await P.evaluate(() => {
        const r = document.getElementById('device')!.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height };
      });
      const juge = async (quoi: string, bande: boolean): Promise<void> => {
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        let Z: Zone[] = [];
        for (let i = 0; i < 20; i++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          const { Z: Z2, n } = await zones(A, P, bande);
          const ip2 = masquerFiche(await P.screenshot({ clip: dv }), Z2, n);
          const ia2 = masquerFiche(await A.screenshot(), Z2, n);
          const pose = i > 1 && ip2.equals(ip) && ia2.equals(ia);
          [Z, ip, ia] = [Z2, ip2, ia2];
          if (pose) break;
        }
        writeFileSync(join(RES, `${theme}-${quoi}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${quoi}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(
          { n: e.n, boite: e.boite },
          `${quoi} : pixels écartés de plus de 2 niveaux (zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      };
      // le bouton photo → son menu : « Dessiner » seul (un Cercle ne porte pas de photo)
      const menus: string[][] = [];
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .ph-photo-btn');
        await toucher(pg, x, y);
        await images(pg, 30);
        menus.push(await menu(pg));
        const [x2, y2] = await centre(pg, '#detailPoster .ph-photo-menu button', 'Dessiner');
        await toucher(pg, x2, y2);
        await images(pg, 60);
      }
      expect(menus[1], 'le menu d’un Cercle, comme le prototype').toEqual(menus[0]);
      expect(menus[1]).toEqual(['Dessiner']);
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
          for (let x = 80; x <= 300; x += 10) pts.push([x, 115 + Math.sin(x / 30) * 25]);
          const X = (x: number): number => r.x + x * r.k;
          const Y = (y: number): number => r.y + y * r.k;
          const cible = document.elementFromPoint(X(80), Y(115)) ?? document.body;
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
          ev('pointerdown', [80, 115]);
          for (const q of pts) ev('pointermove', q);
          ev('pointerup', pts[pts.length - 1]!);
        }, r);
        await images(pg, 20);
        const [x2, y2] = await centre(pg, '#dessinMode [data-outil="poser"], #dessinMode .dz-poser');
        await toucher(pg, x2, y2);
        await images(pg, 60);
      }
      await juge('pose', false);
      // l'œil : masqué pour soi (les dalles reviennent)
      for (const pg of [P, A]) {
        const [x, y] = await centre(pg, '#detailPoster .dz-oeil');
        await toucher(pg, x, y);
      }
      await Promise.all([images(P, 30), images(A, 30)]);
      await juge('masque', true);
      // ce qui s'écrit : le dessin du Cercle
      const p = (await P.evaluate(
        `JSON.stringify((d => [d.poses.length, d.fond, !!d.masque, d.pose])(JSON.parse(localStorage.getItem('promi_dessins_cercle')).n1))`,
      )) as string;
      const a = (await A.evaluate(
        `JSON.stringify((d => [d.poses.length, d.fond, !!d.masque, d.pose])(JSON.parse(${P_}.magasin.etat().autres.promi_dessins_cercle).n1))`,
      )) as string;
      expect(a, 'le dessin du Cercle posé, masqué, comme le prototype').toBe(p);
      // le menu rouvert : « Retirer le dessin »
      const [x, y] = await centre(A, '#detailPoster .ph-photo-btn');
      await toucher(A, x, y);
      await images(A, 30);
      expect(await menu(A), 'le menu, un dessin posé').toEqual(['Dessiner', 'Retirer le dessin']);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
