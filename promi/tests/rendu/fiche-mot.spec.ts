/**
 * LOT 3b-2 — ÉCRIRE UN MOT SUR LA FICHE : IDENTITÉ AU PIXEL ET CE QUI S'ÉCRIT (redteam_commentaires, redteam_envoi_mot, redteam_retours ④).
 *
 * Des deux côtés, la même fiche (le banc : `etat-fiches.json`), le même toucher au doigt sur la ligne « Un mot… », la même frappe, puis Retour :
 *  · ouverte : le champ, son filet, « Un mot… » en surimpression, la flèche ;
 *  · un mot tapé (« Bravo ») : « Un mot… » parti ;
 *  · envoyé : le champ vide, « Un mot… » revenu, le mot en tête de la liste, « Les Mots » ; le mot signé du prénom, vu ; la ligne du Fil.
 * Clair et sombre. Tolérance : 2 niveaux, 0 pixel au-delà (Q616 hors du Mac).
 * EXCEPTIONS NOMMÉES : celles de la fiche (fiche.spec : M1, M2, M3) ; M5 (le second juge) : les mots vus à la fermeture de la fiche ; M4 (jonction.spec, Q626) — envoyé, la fiche glisse pour montrer le mot
 * et arrive à 60 pt de son bas : le prototype retourne le chevron de Peaufiner (▴, le dépli d'août), la vraie app non ; le CURSEUR du champ (il
 * clignote sans phase commune aux deux côtés) — caché des deux côtés le temps des captures.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fichesPilotees, images, ecart, sonde, stockageFiches, zonesFiche, masquerFiche, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-mot');

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
/** deux captures identiques à 40 images d'horloge d'écart, des deux côtés */
async function poses(P: Page, A: Page): Promise<{ ip: Buffer; ia: Buffer }> {
  let ip: Buffer = Buffer.alloc(0);
  let ia: Buffer = Buffer.alloc(0);
  for (let k = 0; k < 20; k++) {
    await Promise.all([images(P, 40), images(A, 40)]);
    // les exceptions de la fiche (fiche.spec : M1 la matière de la dalle, M2 le grain des anneaux, M3 le fondu des Noyaux)
    // M4 (Q626) : le chevron que le prototype retourne en bas de la fiche (`#dpDetails.ouvert`, sur un Peaufiner fermé)
    const chev = (await P.evaluate(() => {
      const b = document.getElementById('dpDetails')!;
      if (!b.classList.contains('ouvert') || document.getElementById('detailPoster')!.classList.contains('s2-ouv'))
        return null;
      const D = document.getElementById('device')!.getBoundingClientRect();
      const r = b.querySelector('.dpd-tog i')!.getBoundingClientRect();
      return [r.left - D.left - 4, r.top - D.top - 4, r.width + 8, r.height + 8];
    })) as [number, number, number, number] | null;
    const Z = [...(chev ? [chev] : []), ...(await zonesFiche(A, P))];
    const n = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
    const [p2, a2] = [masquerFiche(await image(P), Z, n), masquerFiche(await image(A), Z, n)];
    const pose = k > 1 && p2.equals(ip) && a2.equals(ia);
    [ip, ia] = [p2, a2];
    if (pose) break;
  }
  return { ip, ia };
}

for (const theme of ['sombre', 'clair'] as const)
  test(`écrire un mot sur la fiche, comme le prototype — ouverte, tapé, envoyé ; le mot, le Fil (C-116, C-260), ${theme}`, async ({
    browser,
  }) => {
    const id = 146;
    // un prénom posé (sans lui, le prototype signe « Tom », son prénom de démonstration — `USER.name` —, et la vraie app « Moi »)
    const ls = { ...stockageFiches(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
    try {
      // la sonde (sur « écrire un mot sur la fiche, comme le prototype — …, sombre ») : la ligne ouverte sans son filet
      if (sonde('mot-sans-filet'))
        await A.addStyleTag({
          content: '#detailPoster #cm5Ligne.cm5-ouvert{border-bottom-color:transparent!important}',
        });
      // la sonde (sur « écrire un mot sur la fiche, comme le prototype — …, clair ») : le mot signé « moi » au lieu du prénom
      if (sonde('mot-signe-moi'))
        await A.evaluate(() => {
          const m = (window as unknown as { __promi: { magasin: { ajouterMot(...a: unknown[]): void } } }).__promi
            .magasin;
          const f = m.ajouterMot.bind(m);
          m.ajouterMot = (id: unknown, t: unknown, _moi: unknown, n: unknown) => {
            f(id, t, 'moi', n);
          };
        });
      for (const pg of [P, A]) await pg.addStyleTag({ content: '#device input{caret-color:transparent!important}' });
      mkdirSync(RES, { recursive: true });
      const juge = async (quoi: string): Promise<void> => {
        const { ip, ia } = await poses(P, A);
        writeFileSync(join(RES, `${theme}-${quoi}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${quoi}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(
          { n: e.n, boite: e.boite },
          `${quoi} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      };
      await Promise.all([toucher(P, 100, 720), toucher(A, 100, 720)]);
      await Promise.all([images(P, 60), images(A, 60)]);
      await juge('ouverte');
      for (const pg of [P, A]) await pg.keyboard.type('Bravo');
      await Promise.all([images(P, 90), images(A, 90)]);
      await juge('tape');
      for (const pg of [P, A]) await pg.keyboard.press('Enter');
      await Promise.all([images(P, 120), images(A, 120)]);
      await juge('envoye');
      // ce qui s'écrit : le mot (texte, signé du prénom, vu), la ligne du Fil
      const p = (await P.evaluate(
        `JSON.stringify([cur.comments.map(c=>[c.t,c.by,c.vu]), FEED[0].type, FEED[0].text])`,
      )) as string;
      const a =
        (await A.evaluate(`(() => { const e = ${P_}.magasin.etat(); const q = e.paroles.find(x => x.id === ${String(id)});
        return JSON.stringify([q.comments.map(c=>[c.t,c.by,c.vu]), e.fil[0].type, e.fil[0].text]); })()`)) as string;
      expect(a, 'le mot et la ligne du Fil, comme le prototype').toBe(p);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

/** le centre d'un élément, en points de l'écran 390 */
async function centre(pg: Page, sel: string): Promise<[number, number]> {
  return pg.evaluate((s) => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    // la première qui se voit (le prototype porte plusieurs croix dans la fiche)
    const e = [...document.querySelectorAll(s)].find((x) => {
      const q = x.getBoundingClientRect();
      const c = getComputedStyle(x);
      return q.width > 0 && q.height > 0 && c.visibility !== 'hidden' && c.display !== 'none' && +c.opacity > 0;
    })!;
    const r = e.getBoundingClientRect();
    return [(r.left + r.width / 2 - D.left) / k, (r.top + r.height / 2 - D.top) / k] as [number, number];
  }, sel);
}
/** le défilement doux natif est fini : la fiche ne bouge plus d'une prise à l'autre (10 images d'horloge), 60 prises au plus */
async function pose(pg: Page): Promise<void> {
  let av = -1;
  for (let k = 0; k < 60; k++) {
    await images(pg, 10);
    const y = await pg.evaluate(
      () => (document.getElementById('dpDefile') ?? document.getElementById('detailPoster'))!.scrollTop,
    );
    if (y === av) return;
    av = y;
  }
}
/** ce que le juge compare : le haut du premier mot neuf (pt), la saisie ouverte, Peaufiner ouvert, la fiche ouverte */
async function lire(pg: Page): Promise<{ neuf: number; ouverte: boolean; peaufiner: boolean; fiche: boolean }> {
  return pg.evaluate(() => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const n = document.querySelector('#cm5Liste .cm5-un[data-neuf]')!.getBoundingClientRect();
    const dp = document.getElementById('detailPoster')!;
    return {
      neuf: Math.round(((n.top - D.top) / k) * 2) / 2,
      ouverte: document.getElementById('cm5Ligne')!.getAttribute('role') === 'group',
      peaufiner: dp.classList.contains('s2-ouv') || dp.classList.contains('dpd-corps-ouv'),
      fiche: !dp.hidden && getComputedStyle(dp).display !== 'none' && dp.getBoundingClientRect().top < D.bottom - 1,
    };
  });
}

test('le nombre de mots fait glisser la fiche jusqu’au premier mot neuf ; un toucher ailleurs referme la saisie, comme le prototype (C-257, C-116)', async ({
  browser,
}) => {
  const id = 144;
  // `promi_mots_v184` : la migration de v184 déjà passée (sans lui le prototype compte vus tous les mots d'avant, au chargement)
  const ls: Record<string, string> = {
    ...stockageFiches(),
    promi_prenom: 'Tom',
    promi_theme: 'dark',
    promi_mots_v184: '1',
  };
  // quatre mots de Rachel, les deux plus récents pas encore vus (« +2 » en orange)
  const st = JSON.parse(ls['promi_state']!) as { promises: { id: number; comments?: unknown[] }[] };
  const j = (h: number): string => new Date(Date.UTC(2026, 10, 20, h)).toISOString();
  st.promises.find((p) => p.id === id)!.comments = [
    { t: 'Tu l’as fini ?', d: j(8), by: 'Rachel', vu: true },
    { t: 'Garde-le encore un peu', d: j(9), by: 'Rachel', vu: true },
    { t: 'Je passe demain', d: j(10), by: 'Rachel', vu: false },
    { t: 'Ou samedi, plutôt', d: j(11), by: 'Rachel', vu: false },
  ];
  ls['promi_state'] = JSON.stringify(st);
  const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
  try {
    // la sonde (sur « le nombre de mots fait glisser… ») : la fiche refermée ne marque pas les mots vus
    if (sonde('mots-jamais-vus'))
      await A.evaluate(() => {
        const m = (window as unknown as { __promi: { magasin: { motsVus(): void } } }).__promi.magasin;
        m.motsVus = () => undefined;
      });
    // la sonde (sur « le nombre de mots fait glisser… ») : un toucher ailleurs ne referme pas la saisie
    if (sonde('mot-reste-ouvert'))
      await A.evaluate(() => {
        document.addEventListener('pointerdown', (e) => e.stopImmediatePropagation(), true);
      });
    const avant = await Promise.all([lire(P), lire(A)]);
    expect(avant[1].neuf, 'le premier mot neuf, à l’ouverture').toBe(avant[0].neuf);
    // le nombre touché : la fiche glisse (le défilement doux natif) jusqu'au premier mot neuf, 16 pt sous l'en-tête
    for (const pg of [P, A]) {
      const [x, y] = await centre(pg, '#cm5Ligne .cm5-nb');
      await toucher(pg, x, y);
    }
    await Promise.all([pose(P), pose(A)]);
    const glisse = await Promise.all([lire(P), lire(A)]);
    expect(glisse[0].neuf, 'le prototype a glissé').toBeLessThan(avant[0].neuf - 20);
    expect(glisse[1], 'après le nombre touché').toEqual(glisse[0]);
    // la ligne touchée ouvre la saisie ; un toucher ailleurs (le titre) la referme, et ne fait rien d'autre
    for (const pg of [P, A]) {
      const [x, y] = await centre(pg, '#cm5Ligne');
      await toucher(pg, x - 80, y);
    }
    await Promise.all([images(P, 30), images(A, 30)]);
    const ouverte = await Promise.all([lire(P), lire(A)]);
    expect(ouverte[0].ouverte, 'le prototype a ouvert la saisie').toBe(true);
    expect(ouverte[1], 'la saisie ouverte').toEqual(ouverte[0]);
    await Promise.all([toucher(P, 195, 300), toucher(A, 195, 300)]);
    await Promise.all([pose(P), pose(A)]);
    const fermee = await Promise.all([lire(P), lire(A)]);
    expect(fermee[0].ouverte, 'le prototype a refermé la saisie').toBe(false);
    expect(fermee[1], 'après un toucher ailleurs').toEqual(fermee[0]);
    // la fiche refermée par son X : les mots qu'elle a montrés sont vus (C-253) — ici les quatre, passés à l'écran pendant le glissement
    // (le toucher qui referme la saisie avale, dans le prototype, le clic des 450 ms qui suivent : on les laisse passer)
    await Promise.all([images(P, 40), images(A, 40)]);
    for (const pg of [P, A]) {
      const [x, y] = await centre(pg, '#detailPoster .closeb');
      await toucher(pg, x, y);
    }
    await Promise.all([images(P, 60), images(A, 60)]);
    // ÉCART NOMMÉ (M5) : le X du prototype referme la fiche sans passer par les rangeurs de `closeAll` (où vit `_motsVus`, lot-V184B-MOTS) — ses
    // mots ne sont marqués vus qu'à la fermeture générale suivante ; la vraie app les marque quand la fiche se ferme, comme le dit C-253
    // (« marqué à sa fermeture »). Côté prototype, on passe donc par sa fermeture générale.
    await P.evaluate('closeAll()');
    const vp = (await P.evaluate(
      `JSON.stringify(promises.find(q => q.id === ${String(id)}).comments.map(c => [c.t, !!c.vu]))`,
    )) as string;
    const va = (await A.evaluate(
      `JSON.stringify(${P_}.magasin.etat().paroles.find(q => q.id === ${String(id)}).comments.map(c => [c.t, !!c.vu]))`,
    )) as string;
    expect(vp, 'le prototype a vu les mots neufs').not.toContain('false');
    expect(va, 'les mots vus à la fermeture, comme le prototype').toBe(vp);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
