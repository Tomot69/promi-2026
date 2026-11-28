/**
 * LOT 4b — LA BRIQUE COMMUNE DES CHAMPS (C-271 ; le prototype : `_retour.champ` de lot-V203-RETOUR et le « … » du focus de lot-CURSEUR) — le texte
 * d'exemple d'un champ part et revient en se traçant :
 *  · au focus, « Rechercher » (ou « ajoute un mot, un contexte… », « présente le Cercle, son but… ») se détrace, puis « … » se trace ;
 *  · à la première lettre, « … » se détrace (la lettre paraît tout de suite) ;
 *  · tout effacé, « … » revient en se traçant ;
 *  · le champ quitté, « … » se détrace, puis le texte du repos se trace.
 * Chaque étape POSÉE : la zone du champ au pixel contre le prototype, et son texte d'exemple. PENDANT elle, la vraie app image par image : jamais
 * d'un coup (au moins trois images entre le départ et l'arrivée) ; tant qu'une copie se trace, le texte natif caché sous elle. (Image par image
 * contre le prototype, non : son ouvrier du tracé répond en temps réel, les deux tracés ne partent pas à la même image ; et le prototype laisse
 * le « … » natif visible sous la copie dans la recherche ouverte et la page + — sa règle de couleur bat `.v203-phx` : un « … » qui paraît d'un
 * coup, ce que C-271 interdit. ÉCART NOMMÉ : la vraie app le cache, partout.)
 * Les champs : la recherche de l'Index et du Fil (`ecran-liste.ts`, qui sert aussi la fiche d'une personne), la NOTE de Peaufiner (la brique `note`
 * de briques.ts, qui sert aussi la page +), la DESCRIPTION d'un Cercle. « Un mot… », « un prénom… » et « + ajouter quelqu'un » passent par la même
 * brique (`bascule`, `remplacer`) : leurs juges sont fiche-mot.spec, fiche-gens.spec, page-plus-2c.spec.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { deuxPilotes, fichesPilotees, images, sonde, stockageFiches, CERCLE, P_, ecart } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'champs');

/** la zone du champ (8 pt autour), en pt de l'appareil, lue sur la vraie app */
async function zone(A: Page, sel: string): Promise<[number, number, number, number]> {
  return (await A.evaluate((sel) => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const e = document.querySelector(sel)!;
    const r = e.getBoundingClientRect();
    // la NOTE de Peaufiner (Tom, 28 nov. 2026 : « comme le prototype, mais en douceur ») : toute sa zone, et la place où elle grandit (deux lignes
    // de plus) — la ligne d'aide qui descend est jugée ; une autre zone de texte (la DESCRIPTION d'un Cercle) : sa première ligne
    const z = e.closest('.s2-zone');
    if (z) {
      const q = z.getBoundingClientRect();
      return [(q.left - D.left) / k - 8, (q.top - D.top) / k - 8, q.width / k + 16, q.height / k + 2 * 22.5 + 16];
    }
    const h = e.tagName === 'TEXTAREA' ? (parseFloat(getComputedStyle(e).lineHeight) || 22) / 1 + 4 : r.height / k + 8;
    return [(r.left - D.left) / k - 8, (r.top - D.top) / k - 8, r.width / k + 16, h + 8];
  }, sel)) as [number, number, number, number];
}
async function prise(pg: Page, z: [number, number, number, number]): Promise<Buffer> {
  const clip = await pg.evaluate((z) => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    return { x: D.left + z[0] * k, y: D.top + z[1] * k, width: z[2] * k, height: z[3] * k };
  }, z);
  return pg.screenshot({ clip });
}
/** une image de la largeur d'un appareil, la prise posée à 100 pt du haut (pour `ecart`, qui compte en pt de 390 et excepte les quatre coins) */
function etendre(b: Buffer, z: [number, number, number, number]): Buffer {
  const s = PNG.sync.read(b);
  const k = s.width / z[2];
  const W = Math.round(390 * k);
  const out = new PNG({ width: W, height: Math.round(s.height + 200 * k) });
  out.data.fill(255);
  const x0 = Math.max(0, Math.round(z[0] * k));
  for (let j = 0; j < s.height; j++)
    for (let i = 0; i < s.width && x0 + i < W; i++) {
      const p = (j * s.width + i) * 4;
      const q = ((j + Math.round(100 * k)) * W + x0 + i) * 4;
      s.data.copy(out.data, q, p, p + 4);
    }
  return PNG.sync.write(out);
}

type Etape = 'focus' | 'lettre' | 'efface' | 'quitte';
async function agir(pg: Page, sel: string, e: Etape): Promise<void> {
  await pg.evaluate(
    ([sel, e]) => {
      const i = document.querySelector<HTMLInputElement>(sel!)!;
      if (e === 'focus') i.focus({ preventScroll: true });
      if (e === 'lettre' || e === 'efface') {
        i.value = e === 'lettre' ? 'a' : '';
        i.dispatchEvent(new Event('input', { bubbles: true }));
      }
      if (e === 'quitte') i.blur();
    },
    [sel, e],
  );
}

/** le tracé fini des deux côtés (le module ne trace plus, aucune copie posée) : l'ouvrier du tracé répond en temps réel — on alterne le temps
 *  réel et les images pilotées */
async function pose(P: Page, A: Page): Promise<void> {
  for (let k = 0; k < 60; k++) {
    await Promise.all([P.waitForTimeout(40), A.waitForTimeout(40)]);
    await Promise.all([images(P, 6), images(A, 6)]);
    const fini = await Promise.all(
      [P, A].map((pg) =>
        pg.evaluate(
          () =>
            !(window as unknown as { TraceLettres?: { actif(): boolean } }).TraceLettres?.actif() &&
            !document.querySelector('.ch-fantome, .v203-ph, .trace-copie'),
        ),
      ),
    );
    if (fini.every(Boolean) && k > 2) return;
  }
}
/** une image de la zone, et ce que l'app dit d'elle : une copie du texte d'exemple posée, le texte natif caché */
async function relever(
  A: Page,
  z: [number, number, number, number],
  sel: string,
): Promise<{ im: Buffer; copie: boolean; cache: boolean; zh: number }> {
  const im = await prise(A, z);
  const r = (await A.evaluate((sel) => {
    const e = document.querySelector(sel)!;
    const z = e.closest('.s2-zone');
    const k = document.getElementById('device')!.getBoundingClientRect().width / 390;
    return [
      !!document.querySelector('.ch-fantome'),
      e.classList.contains('ch-phx'),
      z ? Math.round((z.getBoundingClientRect().height / k) * 10) / 10 : 0,
    ];
  }, sel)) as [boolean, boolean, number];
  return { im, copie: r[0], cache: r[1], zh: r[2] };
}

/**
 * les quatre étapes : chacune, une fois posée, la zone du champ au pixel contre le prototype (et le texte d'exemple attendu) ; pendant elle, la
 * vraie app image par image (le temps réel pour l'ouvrier du tracé, puis une image) — jamais d'un coup : au moins trois images qui ne sont ni
 * le départ ni l'arrivée, et, tant qu'une copie se TRACE (le retour, l'échange), le texte natif caché sous elle (C-271 : rien ne paraît d'un coup)
 */
async function juger(P: Page, A: Page, sel: string, nom: string, repos: string): Promise<void> {
  mkdirSync(RES, { recursive: true });
  await pose(P, A);
  const z = await zone(A, sel);
  const attendu: Record<Etape, string> = { focus: '\u2026', lettre: '\u2026', efface: '\u2026', quitte: repos };
  for (const e of ['focus', 'lettre', 'efface', 'quitte'] as const) {
    const depart = await prise(A, z);
    await Promise.all([agir(P, sel, e), agir(A, sel, e)]);
    const fa: Array<{ im: Buffer; copie: boolean; cache: boolean; zh: number }> = [];
    for (let n = 0; n < 50; n++) {
      await A.waitForTimeout(25);
      await images(A, 1);
      fa.push(await relever(A, z, sel));
      if (n > 4 && !fa.at(-1)!.copie && fa.at(-1)!.im.equals(fa.at(-2)!.im)) break;
    }
    await pose(P, A);
    const [ip, ia] = await Promise.all([prise(P, z), prise(A, z)]);
    writeFileSync(join(RES, `${nom}-${e}-prototype.png`), ip);
    writeFileSync(join(RES, `${nom}-${e}-app.png`), ia);
    const d = ecart(etendre(ip, z), etendre(ia, z));
    expect(
      { n: d.n, boite: d.boite },
      `${nom}, ${e}, posé : la zone du champ au pixel (bords lissés hors macOS : ${String(d.bords)})`,
    ).toEqual({ n: 0, boite: null });
    // la NOTE qui grandit à la première lettre (et rapetisse tout effacé) : en douceur — sa hauteur passe par des valeurs intermédiaires (C-271)
    if (
      (e === 'lettre' || e === 'efface') &&
      (await A.evaluate((sel) => !!document.querySelector(sel)!.closest('.s2-zone'), sel))
    ) {
      const hs = new Set(fa.map((f) => f.zh));
      expect(
        [...hs].filter((x) => x > 118.5 && x < 140).length,
        `${nom}, ${e} : la zone de la NOTE glisse de 118 à 140,5 pt (hauteurs relevées : ${[...hs].join(', ')})`,
      ).toBeGreaterThanOrEqual(3);
    }
    const ph = await Promise.all(
      [P, A].map((pg) => pg.evaluate((sel) => document.querySelector(sel)!.getAttribute('placeholder'), sel)),
    );
    expect(ph, `${nom}, ${e} : le texte d'exemple (le prototype, la vraie app)`).toEqual([attendu[e], attendu[e]]);
    // jamais d'un coup
    const entre = fa.filter((f) => !f.im.equals(depart) && !f.im.equals(ia)).length;
    expect(entre, `${nom}, ${e} : des images de tracé entre le départ et l'arrivée`).toBeGreaterThanOrEqual(3);
    if (e !== 'lettre')
      expect(
        fa.filter((f) => f.copie && !f.cache).length,
        `${nom}, ${e} : tant que la copie se trace, le texte natif est caché sous elle`,
      ).toBe(0);
  }
}

// les titres (les sondes les nomment) :
//   « le texte d'exemple de la recherche de l'Index part et revient en se traçant, comme le prototype » (champ-sec)
//   « le texte d'exemple de la NOTE de Peaufiner part et revient en se traçant, comme le prototype » (champ-sans-curseur)
//   « le texte d'exemple de la recherche du Fil part et revient en se traçant, comme le prototype » (champ-natif-visible)
test("le texte d'exemple de la recherche de l'Index part et revient en se traçant, comme le prototype", async ({
  browser,
}) => {
  test.setTimeout(600000);
  // la sonde : le texte d'exemple change d'un coup (la brique ne trace plus)
  const avantA = sonde('champ-sec')
    ? (): void => {
        Object.defineProperty(window, 'matchMedia', {
          value: (q: string) => ({ matches: q.includes('reduce') }),
          configurable: true,
        });
      }
    : undefined;
  const { P, A, erreurs } = await deuxPilotes(browser, stockageFiches(), avantA ? { avantA } : {});
  try {
    await P.evaluate(() => (document.getElementById('indexBtn') as HTMLElement).click());
    await A.evaluate(`${P_}.index().ouvrir()`);
    for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
    await juger(P, A, '#ixSearch', 'index', 'Rechercher');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test("le texte d'exemple de la recherche du Fil part et revient en se traçant, comme le prototype", async ({
  browser,
}) => {
  test.setTimeout(600000);
  // la sonde : le texte natif laissé visible sous la copie qui se trace (le défaut du prototype dans la recherche ouverte)
  const avantA = sonde('champ-natif-visible')
    ? (): void => {
        const f = DOMTokenList.prototype.add;
        DOMTokenList.prototype.add = function (this: DOMTokenList, ...t: string[]) {
          f.apply(
            this,
            t.filter((x) => x !== 'ch-phx'),
          );
        };
      }
    : undefined;
  const { P, A, erreurs } = await deuxPilotes(browser, stockageFiches(), avantA ? { avantA } : {});
  try {
    await P.evaluate(() => (document.getElementById('filBtn') as HTMLElement).click());
    await A.evaluate(`${P_}.fil().ouvrir()`);
    for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
    await juger(P, A, '#fdSearch', 'fil', 'Rechercher');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

/** Peaufiner ouvert par sa barre, des deux côtés, le champ ramené à la même place */
async function peaufiner(P: Page, A: Page, sel: string): Promise<void> {
  // la barre touchée au doigt (son libellé, à gauche du ▾ : fiche-peaufiner.spec)
  for (const pg of [P, A]) {
    const r = await pg.evaluate(() => {
      const b = document.getElementById('device')!.getBoundingClientRect();
      return { x: b.left, y: b.top, k: b.width / 390 };
    });
    await pg.mouse.click(r.x + 80 * r.k, r.y + 802 * r.k);
  }
  for (let k = 0; k < 4; k++) await Promise.all([images(P, 30), images(A, 30)]);
  const top = await A.evaluate((sel) => {
    const c = document.getElementById('dpdCorps')!;
    const r = document.querySelector(sel)!.getBoundingClientRect();
    const D = document.getElementById('device')!.getBoundingClientRect();
    return Math.max(0, c.scrollTop + (r.top - D.top) / (D.width / 390) - 300);
  }, sel);
  for (const pg of [P, A])
    await pg.evaluate((top) => {
      document.getElementById('dpdCorps')!.scrollTop = top;
    }, top);
  for (let k = 0; k < 3; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

test("le texte d'exemple de la NOTE de Peaufiner part et revient en se traçant, comme le prototype", async ({
  browser,
}) => {
  test.setTimeout(600000);
  // la sonde : le champ focalisé garde son texte du repos (le « … » de lot-CURSEUR oublié)
  const avantA = sonde('champ-sans-curseur')
    ? (): void => {
        const f = Element.prototype.setAttribute;
        Element.prototype.setAttribute = function (this: Element, n: string, v: string) {
          if (n === 'placeholder' && v === '…') return;
          f.call(this, n, v);
        };
      }
    : undefined;
  const { P, A, erreurs } = await fichesPilotees(browser, stockageFiches(), 144, avantA ? { avantA } : {});
  try {
    await peaufiner(P, A, '#dNote');
    await juger(P, A, '#dNote', 'note', 'ajoute un mot, un contexte…');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test("le texte d'exemple de la DESCRIPTION d'un Cercle part et revient en se traçant, comme le prototype", async ({
  browser,
}) => {
  test.setTimeout(600000);
  const { P, A, erreurs } = await deuxPilotes(browser, stockageFiches());
  try {
    await CERCLE.donnee!(A);
    await A.evaluate(`(() => { const P = window.__promi; const e = P.magasin.etat();
      P.fiche().ouvrirCercle(Object.keys(e.cercles).find((c) => e.cercles[c] === 'Marseille')); })()`);
    await P.evaluate(`(() => { NUE.n1 = 'Marseille'; NUEEMEM.n1 = ['Rachel', 'Marion'];
      const L0 = promises.filter((x) => !x.draft && !x.nuee && !x.chiche);
      for (const q of L0.slice(0, Math.min(2, L0.length - 1))) q.nuee = 'n1';
      if (window.Toile && Toile.sync) Toile.sync(promises); openNueeDetail('n1'); })()`);
    for (let k = 0; k < 8; k++) await Promise.all([images(P, 30), images(A, 30)]);
    await peaufiner(P, A, '#nqNote');
    await juger(P, A, '#nqNote', 'description', 'présente le Cercle, son but…');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
