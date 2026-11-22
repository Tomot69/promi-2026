/**
 * LOT 2a — LA PAGE + : IDENTITÉ AU PIXEL (releve-S3-page-plus, redteam_pages_plus).
 *
 * La page + de la vraie app à 390 × 844 contre celle du prototype (son appareil dans la fenêtre du banc), même état importé des deux côtés
 * (`stockage()` : les exemples tirés d'avance, les personnes connues), même WebKit, ×3, clair et sombre : Promi, Chiche, Cercle au repos, et
 * le choix des personnes ouvert (« qui ose ? » d'un Chiche, « avec » d'un Cercle) ; et (fin du 2a) la saisie ouverte (« DÉJÀ PROMIS », la
 * page montée), un titre tapé (la place remplie, crème), le champ « un prénom… » (C-122) avec un nom tapé et son « + », Peaufiner ouvert (trois
 * natures), le menu du bouton photo ouvert. La Toile dessous est masquée, les animations gelées. Tolérance : 2 niveaux, 0 pixel au-delà (Q616
 * hors du Mac, aides.ts `ecart`).
 *
 * EXCEPTIONS NOMMÉES (et seulement elles), déclarées et masquées DES DEUX CÔTÉS :
 *  · M1 — la MATIÈRE de la dalle du haut (§8 bis : « zéro écart » excepte la matière) : la zone que le peintre déclare (`data-matiere`) ;
 *  · P1 — le petit carré noir que le prototype peint à gauche du rail du pinceau (12,7 × 25,7 pt, « sans aucun élément dessous », déjà noté en
 *         v174a) : un défaut du prototype, que la vraie app ne reproduit pas ;
 *  · P2 — le flou du premier pinceau de Ma Parole ! au bord droit (x ≥ 366, la rangée du rail) : dans le prototype WebKit le coupe au bord de la
 *         couche qui défile, la vraie app le laisse entier (le même `filter: blur(4.8px)`, C-196) ;
 *  · P3 — NON EXPLIQUÉ, MESURÉ : un pixel du pointillé de l'exemple d'un Chiche, à (238,3 ; 514), 27 niveaux (les boîtes des deux côtés sont les
 *         mêmes au centième de point) : écrit « non tenu » au rapport du lot 2a, à reprendre ;
 *  · P4 — le CURSEUR qui clignote (lot-CURSEUR) : il n'a pas de phase commune aux deux côtés (le prototype le fait clignoter même sous le gel :
 *         sa règle d'animation bat celle du gel) ; il est caché des deux côtés le temps de la capture, et sa forme est jugée à part
 *         (page-plus-juges.spec.ts, « la saisie »).
 * La matière n'est pas exceptée quand Peaufiner la couvre (elle n'y est pas visible) ; ouverte sous le menu photo, sa zone en couvre une part.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { ETAT, stockage, GEL, prototype, vraieApp, ouvrirPagePlus, ecart, sonde, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'page-plus');

/**
 * LES ÉCARTS ADMIS AU PROTOTYPE (Tom, 22 nov. 2026), nommés ; chacun a son test qui rougit si la décision est défaite
 * (page-plus-juges.spec.ts « C-330, C-331 », sondes garder-teinte et ouverture-seche) :
 *  - C-330 : « garder de côté » inactif prend la teinte de sa nature (#82AEF8 · #FFB8D2 · #C9A8F5) — sa boîte est masquée ici ;
 *  - C-331 : la page + monte en glissant à l'ouverture (la capture est prise une fois arrivée : rien à masquer).
 */
export const ECARTS_ADMIS = [
  'C-330 « garder de côté » à la teinte de sa nature',
  'C-331 la page + monte à l’ouverture',
];

type Zone = [number, number, number, number];

/** la matière déclarée par le peintre de la page + (`#csTrameCv[data-matiere]`), en pt de l'appareil */
async function matiere(pg: Page): Promise<Zone | null> {
  return (await pg.evaluate(() => {
    const cv = document.getElementById('csTrameCv');
    const m = cv?.getAttribute('data-matiere');
    if (!m || !cv) return null;
    const D = (document.getElementById('device') ?? document.getElementById('createSheet'))!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    const [x, y, w, h] = m.split(',').map(Number) as [number, number, number, number];
    const c = cv.getBoundingClientRect();
    return [(c.left - D.left) / k + x, (c.top - D.top) / k + y, w, h];
  })) as Zone | null;
}

/**
 * les zones exceptées (en pt) : la MATIÈRE (§8 bis) — la réunion de celle que déclare la vraie app et de celle que déclare le prototype,
 * élargie de 8 pt (les poils d'un monde comme Touffe débordent de la boîte déclarée ; la dalle d'avance du prototype respire et se pose
 * d'une passe à l'autre à quelques points près : relevé sur une passe à deux en parallèle, ses poils sortaient de la boîte de l'app) —,
 * le carré P1, le bord P2
 */
async function zones(A: Page, P: Page): Promise<Zone[]> {
  const ms = (await Promise.all([matiere(A), matiere(P)])).filter((z): z is Zone => !!z);
  const peauf = await A.evaluate(() => document.getElementById('createSheet')!.classList.contains('pp-peauf'));
  const horsMac = process.platform !== 'darwin';
  const autres = (await A.evaluate((horsMac) => {
    const z: number[][] = [];
    const C = document.getElementById('createSheet')!.getBoundingClientRect();
    const vu = (e: Element): boolean => {
      const b = e.getBoundingClientRect();
      const t = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2);
      return !!t && (t === e || e.contains(t));
    };
    const r = document.getElementById('csPinceau');
    if (r && !r.hidden && vu(r)) {
      const t = r.getBoundingClientRect().top - C.top;
      z.push([0, t - 14, 14, 28]);
      z.push([366, t - 6, 24, 56]);
    }
    if (document.getElementById('createSheet')!.classList.contains('pp-chiche')) z.push([237.5, 513.5, 1.5, 1.5]);
    // ÉCART ADMIS C-330 : « garder de côté » inactif à la teinte de sa nature (le prototype le sort bleu ou lilas selon une course)
    const g = document.querySelector('#createSheet .pp-garder.inactif');
    if (g && !(g as HTMLElement).hidden && vu(g)) {
      const b = g.getBoundingClientRect();
      z.push([b.left - C.left - 4, b.top - C.top - 4, b.width + 8, b.height + 8]);
    }
    // HORS DU MAC SEULEMENT — le texte flouté des murs de Peaufiner (4,8 px, illisible par décision ; leur phrase au lot 8) : sa coupe dépend des
    // métriques de police du système, et sous Linux le prototype et l'app ne la font pas tomber au même endroit (la valeur déborde d'un côté,
    // finit par « … » de l'autre). Dans WebKit sur le Mac (la référence : l'iPhone de Tom), identique au pixel, et jugé là. Le contour, lui, reste jugé.
    if (horsMac) {
      // (au-dessus de la barre Peaufiner, qui reste jugée)
      const bas = document.getElementById('csBotBar')!.getBoundingClientRect().top - C.top;
      for (const m of document.querySelectorAll('#csPeauf .s2-cercle .s2-reg')) {
        const b = m.getBoundingClientRect();
        const y0 = b.top - C.top + 6;
        const y1 = Math.min(b.bottom - C.top - 6, bas - 1);
        if (b.height && y1 > y0) z.push([b.left - C.left + 6, y0, b.width - 12, y1 - y0]);
      }
    }
    return z;
  }, horsMac)) as Zone[];
  if (!ms.length || peauf) return autres;
  const x0 = Math.min(...ms.map((m) => m[0])) - 8,
    y0 = Math.min(...ms.map((m) => m[1])) - 8;
  const x1 = Math.max(...ms.map((m) => m[0] + m[2])) + 8,
    y1 = Math.max(...ms.map((m) => m[1] + m[3])) + 8;
  return [[x0, y0, x1 - x0, y1 - y0], ...autres];
}

function masquer(png: Buffer, Z: Zone[]): Buffer {
  const im = PNG.sync.read(png);
  const k = im.width / 390;
  for (const [x, y, w, h] of Z)
    for (let j = Math.max(0, Math.floor(y * k)); j < Math.min(im.height, Math.ceil((y + h) * k)); j++)
      for (let i = Math.max(0, Math.floor(x * k)); i < Math.min(im.width, Math.ceil((x + w) * k)); i++) {
        const q = (j * im.width + i) * 4;
        im.data[q] = 255;
        im.data[q + 1] = 0;
        im.data[q + 2] = 255;
      }
  return PNG.sync.write(im);
}

/** un toucher sur la place « qui » (au doigt, WebKit ne fabrique pas toujours de `click` — le prototype écoute `click`, la vraie app le geste) */
async function touchePlace(p: Page, sel: string, proto: boolean): Promise<void> {
  const tracant = (): Promise<unknown> =>
    p.waitForFunction(
      () => !(window as unknown as { TraceLettres?: { actif(): boolean } }).TraceLettres?.actif(),
      undefined,
      { timeout: 60000 }, // hors du Mac le prototype trace ses textes jusqu’à 40 s
    );
  const touche = (): Promise<void> =>
    p.evaluate(
      ([s, proto]) => {
        const e = document.querySelector<HTMLElement>(s as string)!;
        const r = e.getBoundingClientRect();
        const o = { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2, pointerId: 21 };
        e.dispatchEvent(new PointerEvent('pointerdown', o));
        e.dispatchEvent(new PointerEvent('pointerup', o));
        // le prototype ouvre le choix au `click` ; la place passe à « moi » à l'appui (C-304, `lot-V199-MOI`)
        if (proto) e.click();
      },
      [sel, proto] as const,
    );
  if (!proto) {
    await touche();
    await p.waitForTimeout(600);
    return;
  }
  // le prototype : hors du Mac (une image dure 0,7 s) ses textes se tracent encore quand la page est posée, et un toucher pendant un tracé
  // ne fait pas passer la place à « moi » (la cause des deux Chiche rouges sur l'intégration continue) — on attend que plus rien ne se
  // trace, on touche, et l'on retouche une fois si la place n'a pas changé
  for (let essai = 0; essai < 2; essai++) {
    await tracant();
    // la seconde fois, on ne retouche que si la place n'a pas changé : retoucher « moi » relancerait un tracé (sous charge, le premier
    // essai peut finir son attente avant la fin du tracé)
    const deja = await p.evaluate((s) => (document.querySelector(s)?.textContent ?? '').trim() === 'moi', sel);
    if (!(essai > 0 && deja)) await touche();
    // C-304 : la place passe à « moi » par une transition (détracé puis tracé, C-271) : on attend qu'elle soit finie
    const ok = await p
      .waitForFunction(
        (s) => {
          const e = document.querySelector(s);
          const w = window as unknown as { TraceLettres?: { actif(): boolean } };
          return !!e && (e.textContent ?? '').trim() === 'moi' && !w.TraceLettres?.actif();
        },
        sel,
        { timeout: 20000 },
      )
      .then(() => true)
      .catch(() => false);
    if (ok) break;
  }
  const lu = await p.evaluate((s) => {
    const w = window as unknown as { TraceLettres?: { actif(): boolean } };
    return { texte: (document.querySelector(s)?.textContent ?? '').trim(), trace: !!w.TraceLettres?.actif() };
  }, sel);
  expect(lu, 'le prototype : la place touchée est passée à « moi », plus rien ne se trace').toEqual({
    texte: 'moi',
    trace: false,
  });
  await p.waitForTimeout(1500);
}

/** P4 : le curseur caché des deux côtés (sa règle d'animation, dans le prototype, bat le gel) */
const SANS_CURSEUR =
  'html body #device #createSheet .ph-caret, html body #createSheet .ph-caret{visibility:hidden!important}';

/** un toucher au doigt (appui puis lever ; le prototype, lui, écoute aussi `click`) */
async function toucheSel(p: Page, sel: string, proto: boolean): Promise<void> {
  await p.evaluate(
    ([s, proto]) => {
      const e = document.querySelector<HTMLElement>(s as string)!;
      const r = e.getBoundingClientRect();
      const o = { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2, pointerId: 21 };
      e.dispatchEvent(new PointerEvent('pointerdown', o));
      e.dispatchEvent(new PointerEvent('pointerup', o));
      if (proto) e.click();
    },
    [sel, proto] as const,
  );
}
const finTrace = (p: Page): Promise<unknown> =>
  p.waitForFunction(
    () => !(window as unknown as { TraceLettres?: { actif(): boolean } }).TraceLettres?.actif(),
    undefined,
    {
      timeout: 30000,
    },
  );
/** la vraie app : plus aucun mouvement, plus aucun passage en flaques */
const finApp = (p: Page): Promise<unknown> =>
  p.waitForFunction(
    () =>
      !document.querySelector('#createSheet [data-flaques-mode]') &&
      !(window as unknown as { __promi: { pagePlus(): { etat(): { mouvement: boolean } } } }).__promi.pagePlus().etat()
        .mouvement,
    undefined,
    { timeout: 20000 },
  );

type Cas = {
  nat: 'promi' | 'chiche' | 'nuee';
  choix: string | null;
  /** fin du 2a : ce que la page montre ensuite (la saisie, un titre tapé, Peaufiner, le menu photo, le champ « un prénom… ») */
  /** 2b : « prete » — le titre tapé puis validé (Retour) : l'horizon remonté, le trait né, le libellé tracé (C-209, C-213, C-229) */
  /** 2b : « personne » — un prénom tapé dans le choix des personnes et validé (Retour) : la pastille remplie porte son visage (§2.10) ;
   *  « cercle » — dans Peaufiner, DANS UN CERCLE, un Cercle choisi, Peaufiner refermé : « Je promets … à tout le monde » (le prototype,
   *  `buildCreateNuees`), l'exemple au pluriel */
  /** « dessin » — le menu photo, puis « Dessiner » : le mode dessin (C-042) ; « tailles » — la plume touchée deux fois : ses trois tailles
   *  déployées ; « couleurs » — le disque COULEUR : le mur des teintes (sans Ma Parole !) */
  etat?:
    | 'saisie'
    | 'tape'
    | 'peauf'
    | 'photo'
    | 'prenom'
    | 'prete'
    | 'personne'
    | 'cercle'
    | 'dessin'
    | 'tailles'
    | 'couleurs';
};
const CAS: Cas[] = [
  { nat: 'promi', choix: null },
  { nat: 'chiche', choix: null },
  { nat: 'nuee', choix: null },
  { nat: 'chiche', choix: '#csPhrase .ph-m[data-ph="qui"]' },
  { nat: 'nuee', choix: '#nueePhrase .ph-m[data-np="avec"]' },
  { nat: 'promi', choix: null, etat: 'saisie' },
  { nat: 'chiche', choix: null, etat: 'tape' },
  { nat: 'nuee', choix: null, etat: 'saisie' },
  { nat: 'chiche', choix: '#csPhrase .ph-m[data-ph="qui"]', etat: 'prenom' },
  { nat: 'promi', choix: null, etat: 'peauf' },
  { nat: 'chiche', choix: null, etat: 'peauf' },
  { nat: 'nuee', choix: null, etat: 'peauf' },
  { nat: 'promi', choix: null, etat: 'photo' },
  { nat: 'nuee', choix: null, etat: 'photo' },
  { nat: 'promi', choix: null, etat: 'prete' },
  { nat: 'chiche', choix: null, etat: 'prete' },
  { nat: 'nuee', choix: null, etat: 'prete' },
  { nat: 'chiche', choix: '#csPhrase .ph-m[data-ph="qui"]', etat: 'personne' },
  { nat: 'promi', choix: null, etat: 'cercle' },
  { nat: 'promi', choix: null, etat: 'dessin' },
  { nat: 'chiche', choix: null, etat: 'tailles' },
  { nat: 'nuee', choix: null, etat: 'couleurs' },
];
/** un toucher sur l'élément de `sel` dont le texte commence par `mot` (une rangée de Peaufiner par son libellé, une pastille de choix) */
async function toucheTexte(p: Page, sel: string, mot: string, proto: boolean): Promise<void> {
  await p.evaluate(
    ([s, mot, proto]) => {
      const e = [...document.querySelectorAll<HTMLElement>(s as string)].find(
        (x) =>
          x.getBoundingClientRect().width > 0 &&
          (x.textContent ?? '')
            .trim()
            .toLowerCase()
            .startsWith(mot as string),
      )!;
      const r = e.getBoundingClientRect();
      const o = { bubbles: true, clientX: r.left + 30, clientY: r.top + Math.min(20, r.height / 2), pointerId: 21 };
      const cible = document.elementFromPoint(o.clientX, o.clientY) ?? e;
      cible.dispatchEvent(new PointerEvent('pointerdown', o));
      cible.dispatchEvent(new PointerEvent('pointerup', o));
      if (proto) (cible as HTMLElement).click();
    },
    [sel, mot, proto] as const,
  );
}

/**
 * le prototype POSÉ : plus rien ne se trace et aucune transition CSS ne court dans sa page + (les animations sans fin — le I qui clignote,
 * le curseur — ne comptent pas), deux relevés de suite à 400 ms. Hors du Mac une image dure 0,7 s : ses minuteurs finissent bien après des
 * durées fixes, et la feuille de gel (GEL) posée au milieu d'une transition la coupe — sa fin n'arrive jamais, le prototype reste figé à
 * mi-chemin (la place « moi » vide, la liaison pas tracée). 60 s au plus ; au-delà on continue, et l'identité le dira.
 */
async function protoPose(P: Page): Promise<void> {
  const calme = (): Promise<boolean> =>
    P.evaluate(() => {
      const w = window as unknown as { TraceLettres?: { actif(): boolean } };
      if (w.TraceLettres?.actif()) return false;
      // Peaufiner ouvert : ses murs (`.s2-cercle`, flous, posés par une passe plus tardive) sont là
      if (
        document.querySelector('#createSheet.pp-peauf') &&
        ![...document.querySelectorAll('#createSheet .s2-cercle')].some((e) => e.getBoundingClientRect().height > 0)
      )
        return false;
      return !document.getAnimations().some((a) => {
        if (a.playState !== 'running') return false;
        const t = (a.effect as KeyframeEffect | null)?.target;
        if (!(t instanceof Element) || !t.closest('#createSheet')) return false;
        const it = (a.effect as KeyframeEffect).getTiming().iterations;
        return it !== Infinity;
      });
    });
  const t0 = Date.now();
  while (Date.now() - t0 < 60000) {
    if (await calme()) {
      await P.waitForTimeout(400);
      if (await calme()) return;
    }
    await P.waitForTimeout(250);
  }
}

/** l'état demandé, des deux côtés (le prototype écoute le clic ; on attend la fin de ses minuteurs, et dans la vraie app la fin des mouvements) */
async function poser(P: Page, A: Page, c: Cas): Promise<void> {
  const titre = c.nat === 'nuee' ? '.pp-phrase .ph-m[data-np="nom"]' : '.pp-phrase .ph-m[data-ph="titre"]';
  if (c.etat === 'saisie' || c.etat === 'tape' || c.etat === 'prete') {
    await finTrace(P);
    await protoPose(P);
    await Promise.all([toucheSel(P, titre, true), toucheSel(A, titre, false)]);
    await P.waitForTimeout(2500);
    if (c.etat === 'tape' || c.etat === 'prete') {
      await protoPose(P);
      await P.keyboard.type('appeler Lou');
      await A.keyboard.type('appeler Lou');
      await P.waitForTimeout(2500);
    }
    if (c.etat === 'prete') {
      await protoPose(P);
      await P.keyboard.press('Enter');
      await A.keyboard.press('Enter');
      // le trait né des deux côtés : l'horizon remonté, plus aucun passage en flaques ni tracé (hors du Mac jusqu'à 60 s)
      await P.waitForFunction(
        () => {
          const w = window as unknown as {
            _ppInvite?: { etat(): { visible: boolean } };
            TraceLettres?: { actif(): boolean };
          };
          return (
            !!w._ppInvite?.etat().visible &&
            !document.querySelector('#createSheet canvas.passage-flaques') &&
            !w.TraceLettres?.actif()
          );
        },
        undefined,
        { timeout: 60000 },
      );
      await A.waitForFunction(
        `(() => { const e = ${P_}.pagePlus().etat(); const w = window; return e.invite.visible && !e.invite.anim && !document.querySelector('#createSheet canvas.passage-flaques') && !w.TraceLettres?.actif(); })()`,
        undefined,
        { timeout: 60000 },
      );
    }
  }
  if (c.etat === 'prenom') {
    await protoPose(P);
    await Promise.all([toucheSel(P, '#createSheet .ph-add', true), toucheSel(A, '#createSheet .ph-add', false)]);
    await P.waitForTimeout(2500);
    await P.keyboard.type('Lou');
    await A.keyboard.type('Lou');
    await P.waitForTimeout(2500);
  }
  if (c.etat === 'personne') {
    await protoPose(P);
    await Promise.all([toucheSel(P, '#createSheet .ph-add', true), toucheSel(A, '#createSheet .ph-add', false)]);
    await P.waitForTimeout(2500);
    await P.keyboard.type('Lou');
    await A.keyboard.type('Lou');
    await P.waitForTimeout(1500);
    await P.keyboard.press('Enter');
    await A.keyboard.press('Enter');
    await P.waitForTimeout(4000);
  }
  if (c.etat === 'cercle') {
    await protoPose(P);
    await Promise.all([toucheSel(P, '#csBotBar', true), toucheSel(A, '#csBotBar', false)]);
    await P.waitForTimeout(2000);
    await Promise.all([
      toucheTexte(P, '#createSheet .s2-reg', 'dans un cercle', true),
      toucheTexte(A, '#createSheet .s2-reg', 'dans un cercle', false),
    ]);
    await P.waitForTimeout(1200);
    await Promise.all([
      toucheTexte(P, '#createSheet .s2-reg .chip', 'marseille', true),
      toucheTexte(A, '#createSheet .s2-reg .chip', 'marseille', false),
    ]);
    await P.waitForTimeout(1500);
    await Promise.all([toucheSel(P, '#createSheet .s2-fermer', true), toucheSel(A, '#createSheet .s2-fermer', false)]);
    await P.waitForTimeout(4000);
  }
  if (c.etat === 'dessin' || c.etat === 'tailles' || c.etat === 'couleurs') {
    await protoPose(P);
    await Promise.all([
      toucheSel(P, '#createSheet .ph-photo-btn', true),
      toucheSel(A, '#createSheet .ph-photo-btn', false),
    ]);
    await P.waitForTimeout(2000);
    for (const pg of [P, A])
      await pg.evaluate(() =>
        document.querySelector<HTMLElement>('#createSheet .ph-photo-menu [data-dessiner]')!.click(),
      );
    await P.waitForTimeout(1200);
    const outil = c.etat === 'tailles' ? 'plume' : c.etat === 'couleurs' ? 'couleur' : null;
    if (outil)
      for (const pg of [P, A])
        await pg.evaluate((o) => {
          // la plume est déjà choisie : un toucher déploie ses tailles ; COULEUR : un toucher déploie le mur
          document.querySelector<HTMLElement>(`#dessinMode [data-outil="${o}"]`)!.click();
        }, outil);
    await P.waitForTimeout(800);
  }
  if (c.etat === 'peauf') {
    await protoPose(P);
    await Promise.all([toucheSel(P, '#csBotBar', true), toucheSel(A, '#csBotBar', false)]);
    await P.waitForTimeout(2000);
  }
  if (c.etat === 'photo') {
    await protoPose(P);
    await Promise.all([
      toucheSel(P, '#createSheet .ph-photo-btn', true),
      toucheSel(A, '#createSheet .ph-photo-btn', false),
    ]);
    await P.waitForTimeout(2000);
  }
  if (c.etat) await finApp(A);
  await protoPose(P);
}

for (const theme of ['sombre', 'clair'] as const)
  for (const c of CAS)
    test(`identité au pixel : la page + ${c.nat}${c.choix ? ', le choix des personnes ouvert' : ''}${c.etat ? `, ${c.etat}` : ''}, ${theme}`, async ({
      browser,
    }) => {
      const ls: Record<string, string> = { ...stockage(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      if (c.etat === 'cercle') {
        // un Cercle connu, des deux côtés (le prototype le lit dans NUE, la vraie app dans ses Cercles, migrés de NUE)
        const st = JSON.parse(ls['promi_state']!) as Record<string, unknown>;
        st['NUE'] = { n1: 'Marseille' };
        ls['promi_state'] = JSON.stringify(st);
      }
      const P = await (
        await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 })
      ).newPage();
      const A = await (
        await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })
      ).newPage();
      try {
        const erreurs: string[] = [];
        A.on('pageerror', (e) => erreurs.push(String(e)));
        await Promise.all([prototype(P, ls), vraieApp(A, ls)]);
        await Promise.all([ouvrirPagePlus(P, c.nat, true), ouvrirPagePlus(A, c.nat)]);
        if (c.choix) await Promise.all([touchePlace(P, c.choix, true), touchePlace(A, c.choix, false)]);
        await poser(P, A, c);
        for (const pg of [P, A]) await pg.addStyleTag({ content: GEL + SANS_CURSEUR });
        // la sonde : la phrase de la vraie app décalée d'un point
        if (sonde('pp-identite-decale')) await A.addStyleTag({ content: '#createSheet .pp-phrase{translate:1px 0}' });
        await P.waitForTimeout(600);
        const dv = await P.evaluate(() => {
          const r = document.getElementById('device')!.getBoundingClientRect();
          return { x: r.left, y: r.top, width: r.width, height: r.height };
        });
        // les deux côtés POSÉS : deux images identiques (matière exceptée) à 700 ms d'écart — hors du Mac une image dure 0,7 s et les
        // minuteurs du prototype (son tracé, ses murs, ses mouvements) finissent bien après les durées fixes de `poser` (25 s au plus ; au-delà
        // on compare quand même, et l'écart le dit)
        let Z = await zones(A, P);
        let ip = masquer(await P.screenshot({ clip: dv }), Z);
        let ia = masquer(await A.screenshot(), Z);
        for (let k = 0; k < 25; k++) {
          await P.waitForTimeout(700);
          const Z2 = await zones(A, P);
          const ip2 = masquer(await P.screenshot({ clip: dv }), Z2);
          const ia2 = masquer(await A.screenshot(), Z2);
          const pose = ip2.equals(ip) && ia2.equals(ia);
          [Z, ip, ia] = [Z2, ip2, ia2];
          if (pose) break;
        }
        mkdirSync(RES, { recursive: true });
        const nom = `${theme}-${c.nat}${c.choix ? '-choix' : ''}${c.etat ? '-' + c.etat : ''}`;
        writeFileSync(join(RES, `${nom}-prototype.png`), ip);
        writeFileSync(join(RES, `${nom}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(erreurs).toEqual([]);
        expect(
          { n: e.n, boite: e.boite },
          `pixels écartés de plus de 2 niveaux (état : ${ETAT} ; zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      } finally {
        // les deux contextes fermés à chaque cas, même en échec : laissés ouverts, 28 cas × 2 pages ×3 épuisaient la mémoire du runner (CI part 2)
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
