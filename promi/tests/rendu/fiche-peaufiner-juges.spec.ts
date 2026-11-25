/**
 * LOT 3b-1 — PEAUFINER SUR LA FICHE : SES JUGES, hors de l'identité au pixel (fiche-peaufiner.spec.ts) — redteam_peaufiner (C-134),
 * redteam_peauf_x (C-220), redteam_peauf_rangees (C-192), redteam_effacer (v187), redteam_echeance (C-160).
 *  · la barre l'ouvre (au doigt), un choix le laisse ouvert ; un glissement de 60 pt vers le bas non, de 220 pt le referme ; son X aussi — la
 *    fiche reste, il n'en reste rien ;
 *  · un choix s'écrit et se relit : AVANT (« 1 sem. »), DANS UN CERCLE, la NOTE — l'app rechargée, ils sont là ; la ligne d'état de la fiche
 *    dit la date ;
 *  · SUPPRIMER : la feuille ; « Garder » ne fait rien ; « Supprimer » efface la parole (la fiche se ferme), sa pierre tombale est posée et
 *    survit au rechargement ; « Annuler » la rend.
 */
import { test, expect, type Page } from '@playwright/test';
import { vraieApp, sonde, stockageFiches, PAROLE_CERCLE } from './aides.ts';

type Promi = {
  __promi: {
    fiche(): { ouvrir(i: number): void; etat(): { id: number | null } };
    magasin: {
      etat(): {
        paroles: Array<{
          id: number;
          title: string;
          due: number | null;
          nuee?: string | null;
          suite?: Record<string, unknown>;
        }>;
        effacees: string[];
      };
    };
  };
};

/** un toucher au doigt au point de l'appareil (x, y), en pt */
async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
/** un toucher au centre de l'élément `sel` dont le texte commence par `mot` */
async function toucherMot(pg: Page, sel: string, mot: string): Promise<void> {
  const c = await pg.evaluate(
    ([sel, mot]) => {
      const e = [...document.querySelectorAll<HTMLElement>(sel!)].find((x) =>
        (x.textContent ?? '').trim().startsWith(mot!),
      );
      if (!e) return null;
      e.scrollIntoView({ block: 'center' });
      const b = e.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    },
    [sel, mot],
  );
  if (!c) throw new Error(`introuvable : ${sel} « ${mot} »`);
  await pg.mouse.click(c[0]!, c[1]!);
}
async function ouvrirFiche(pg: Page, id: number): Promise<void> {
  await pg.evaluate((id) => {
    (window as unknown as Promi).__promi.fiche().ouvrir(id);
  }, id);
  // la fiche posée : montée du bas et sa transition finie (sur la CI une image dure 0,7 s : un délai fixe touchait la barre en route)
  await pg.waitForFunction(
    () => {
      const f = document.getElementById('detailPoster');
      return (
        !!f && !f.hidden && !f.classList.contains('fi-bas') && f.getAnimations().every((a) => a.playState !== 'running')
      );
    },
    undefined,
    { timeout: 10000 },
  );
  await pg.waitForTimeout(300);
}
/** toucher la barre Peaufiner et attendre qu'il soit ouvert (rien, s'il ne s'ouvre pas : le test le juge ensuite) */
async function ouvrirPeauf(pg: Page): Promise<void> {
  await toucher(pg, 80, 802);
  await pg
    .waitForFunction(
      () => {
        const c = document.getElementById('dpdCorps');
        return !!c && !c.hidden && [...c.querySelectorAll('.s2-reg')].length > 0;
      },
      undefined,
      { timeout: 5000 },
    )
    .catch(() => undefined);
  await pg.waitForTimeout(600);
}
const ouvert = (pg: Page): Promise<boolean> =>
  pg.evaluate(() => {
    const c = document.getElementById('dpdCorps');
    return !!c && !c.hidden;
  });
const parole = (
  pg: Page,
  id: number,
): Promise<Promi['__promi']['magasin'] extends { etat(): { paroles: Array<infer P> } } ? P | undefined : never> =>
  pg.evaluate((id) => (window as unknown as Promi).__promi.magasin.etat().paroles.find((p) => p.id === id), id);

/** l'app rechargée, son stockage gardé (le vrai chemin : rien n'est réimporté) */
async function recharger(pg: Page): Promise<void> {
  await pg.reload();
  await pg.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await pg.evaluate(async () => {
    await (window as unknown as { __promi: { demarrer(): Promise<void> } }).__promi.demarrer();
  });
  await pg.waitForTimeout(1500);
}

test('Peaufiner sur la fiche : la barre l’ouvre, un choix le laisse ouvert, 60 pt de glissement non, 220 pt et son X le referment, la fiche reste (C-134, C-220)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockageFiches());
  // la sonde : la barre sourde au doigt
  if (sonde('peauf-fiche-sourd')) await page.addStyleTag({ content: '#dpdTog{pointer-events:none!important}' });
  await ouvrirFiche(page, 144);
  await ouvrirPeauf(page);
  expect(await ouvert(page), 'la barre l’ouvre').toBe(true);
  // un choix (AVANT → « 1 sem. ») : il reste ouvert
  await toucherMot(page, '#dpdCorps .s2-reg', 'AVANT');
  await page.waitForTimeout(300);
  await toucherMot(page, '#dueChips .chip', '1 sem.');
  await page.waitForTimeout(600);
  expect(await ouvert(page), 'un choix le laisse ouvert').toBe(true);
  // un glissement vers le bas, la page en haut : 60 pt non, 220 pt oui
  const glisse = async (d: number): Promise<void> => {
    const r = await page.evaluate(() => {
      const b = document.getElementById('device')!.getBoundingClientRect();
      return { x: b.left, y: b.top, k: b.width / 390 };
    });
    await page.evaluate(() => {
      document.getElementById('dpdCorps')!.scrollTop = 0;
    });
    await page.mouse.move(r.x + 200 * r.k, r.y + 200 * r.k);
    await page.mouse.down();
    for (let i = 1; i <= 10; i++) await page.mouse.move(r.x + 200 * r.k, r.y + (200 + (d * i) / 10) * r.k);
    await page.mouse.up();
    await page.waitForTimeout(600);
  };
  await glisse(60);
  expect(await ouvert(page), '60 pt : il reste ouvert').toBe(true);
  await glisse(220);
  // il se referme en flaques, `hidden` à la fin (sous Linux une image dure jusqu'à 0,7 s : on attend la fin, 5 s au plus)
  await expect.poll(() => ouvert(page), { message: '220 pt : il se referme', timeout: 5000 }).toBe(false);
  // le X
  await ouvrirPeauf(page);
  const x = await page.evaluate(() => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const b = document.querySelector('#dpdCorps .s2-fermer')!.getBoundingClientRect();
    const k = D.width / 390;
    return [(b.left - D.left) / k + b.width / k / 2, (b.top - D.top) / k + b.height / k / 2];
  });
  await toucher(page, x[0]!, x[1]!);
  await expect.poll(() => ouvert(page), { message: 'son X le referme', timeout: 5000 }).toBe(false);
  await page.waitForTimeout(300);
  expect(
    await page.evaluate(() => ({
      fiche: (window as unknown as Promi).__promi.fiche().etat().id,
      reste: document.querySelectorAll('#dpdCorps *').length,
      chevron: document.getElementById('detailPoster')!.classList.contains('dpd-ouv'),
    })),
    'la fiche reste ouverte, Peaufiner n’en laisse rien, le ▾ revenu',
  ).toEqual({ fiche: 144, reste: 0, chevron: false });
});

test('Peaufiner sur la fiche, ses choix : AVANT, DANS UN CERCLE, la NOTE s’écrivent et se relisent après rechargement ; la ligne d’état dit la date (C-160)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockageFiches(true));
  // la sonde : rien ne s'écrit (l'action du magasin sans effet)
  if (sonde('peauf-fiche-choix-perdus'))
    await page.evaluate(() => {
      (window as unknown as { __promi: { magasin: { peaufiner(): void } } }).__promi.magasin.peaufiner = () =>
        undefined;
    });
  await ouvrirFiche(page, 144);
  await ouvrirPeauf(page);
  await toucherMot(page, '#dpdCorps .s2-reg', 'AVANT');
  await page.waitForTimeout(300);
  await toucherMot(page, '#dueChips .chip', '1 sem.');
  await page.waitForTimeout(900);
  await toucherMot(page, '#dpdCorps .s2-reg', 'DANS UN CERCLE');
  await page.waitForTimeout(300);
  const cercle = await page.evaluate(() => {
    const c = [...document.querySelectorAll<HTMLElement>('#nueeChips .chip')][1];
    return c?.textContent ?? null;
  });
  expect(cercle, 'un Cercle à choisir').toBeTruthy();
  await toucherMot(page, '#nueeChips .chip', cercle!);
  await page.waitForTimeout(900);
  await page.locator('#dNote').fill('une note');
  await page.waitForTimeout(300);
  const lu = async (): Promise<unknown> => {
    const p = await parole(page, 144);
    return { due: p?.due, choisi: p?.suite?.['dueChoisi'], cercle: p?.nuee, note: p?.suite?.['note'] };
  };
  const attendu = { due: 7, choisi: true, cercle: PAROLE_CERCLE.nuee, note: 'une note' };
  expect(await lu(), 'écrits').toEqual(attendu);
  expect(
    await page.evaluate(() => document.querySelector('#dpdCorps .s2-reg:nth-of-type(2) .s2-val')?.textContent),
    'la valeur d’AVANT est la date',
  ).not.toBe('en l’air');
  await recharger(page);
  expect(await lu(), 'relus après rechargement').toEqual(attendu);
});

test('SUPPRIMER : la feuille ; « Garder » ne fait rien ; « Supprimer » efface la parole et pose sa pierre tombale, qui survit au rechargement ; « Annuler » la rend (v187, C-258)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockageFiches());
  // la sonde : l'effacement sans pierre tombale (la parole revient au rechargement)
  if (sonde('supprimer-sans-tombe'))
    await page.evaluate(() => {
      const m = (window as unknown as { __promi: { magasin: { effacer(id: number): unknown } } }).__promi.magasin;
      const f = m.effacer.bind(m);
      m.effacer = (id: number) => {
        const r = f(id);
        const e = JSON.parse(localStorage.getItem('promi.etat.v1') ?? '{}') as Record<string, unknown>;
        localStorage.setItem('promi.etat.v1', JSON.stringify({ ...e, effacees: [] }));
        return r;
      };
    });
  const supprimer = async (): Promise<void> => {
    await ouvrirPeauf(page);
    await toucherMot(page, '#dpdCorps .s2-reg', 'SUPPRIMER');
    await page.waitForTimeout(600);
  };
  await ouvrirFiche(page, 147);
  await supprimer();
  expect(await page.locator('#v16Conf .v16-conf-t').textContent(), 'la feuille').toBe('Supprimer ce Chiche ?');
  await toucherMot(page, '#v16Conf button', 'Garder');
  await page.waitForTimeout(700);
  expect(await parole(page, 147), '« Garder » : la parole est là').toBeTruthy();
  await page.waitForFunction(() => !document.getElementById('v16Conf'), undefined, { timeout: 3000 });
  // « Supprimer », puis « Annuler »
  await page.evaluate(() => {
    document.getElementById('dpdCorps')!.scrollTop = 0;
  });
  await toucherMot(page, '#dpdCorps .s2-reg', 'SUPPRIMER');
  await page.waitForTimeout(600);
  await toucherMot(page, '#v16Conf button', 'Supprimer');
  await page.waitForTimeout(800);
  expect(await parole(page, 147), '« Supprimer » : la parole est effacée').toBeUndefined();
  expect(
    await page.evaluate(() => document.getElementById('detailPoster')!.classList.contains('fi-bas')),
    'la fiche se ferme',
  ).toBe(true);
  expect(await page.locator('#v16Toast span').textContent(), 'le bandeau').toBe('Chiche supprimé');
  await toucherMot(page, '#v16Toast button', 'Annuler');
  await page.waitForTimeout(600);
  expect((await parole(page, 147))?.title, '« Annuler » : la parole est revenue').toBe('courir dimanche');
  // « Supprimer » sans annuler : la pierre tombale survit au rechargement
  await ouvrirFiche(page, 147);
  await supprimer();
  await toucherMot(page, '#v16Conf button', 'Supprimer');
  await page.waitForTimeout(800);
  await recharger(page);
  expect(await parole(page, 147), 'rechargée : la parole ne revient pas').toBeUndefined();
  expect(
    await page.evaluate(() =>
      (window as unknown as Promi).__promi.magasin.etat().effacees.includes('147|courir dimanche'),
    ),
    'sa pierre tombale',
  ).toBe(true);
});
