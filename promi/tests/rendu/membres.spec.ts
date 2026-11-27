/**
 * LE CHOIX DES PERSONNES DANS PEAUFINER, AU DOIGT (27 nov. 2026, vu sur l'iPhone de Tom : page + d'un Cercle, MEMBRES) — la vraie app :
 *  · RIEN NE BOUGE SANS UN GESTE : MEMBRES déplié, une pastille cochée, puis 30 s sans toucher — l'écran ne change pas (une image toutes les 3 s) ;
 *  · LE PRÉNOM : « + ajouter quelqu'un » touché, l'entrée reçoit le focus PENDANT le geste (iOS n'ouvre le clavier qu'ainsi) ; « Lou » tapé puis
 *    Retour : Lou est choisie ;
 *  · AUCUN CHEVAUCHEMENT : les pastilles et « + ajouter quelqu'un » sont DANS la rangée (ou la carte) MEMBRES, la suite commence sous elle ;
 *  · « Toi, pour l’instant » : Tom fait toujours partie de son Cercle ; seul, MEMBRES le dit.
 * Sur la page + d'un Cercle, la fiche d'un Cercle (le + des membres), Peaufiner d'un Promi (À QUI) et d'un Chiche (QUI OSE ?) — la même brique
 * (gens.ts). L'identité au pixel de MEMBRES déplié contre le prototype : page-plus.spec (« nuee, membres »).
 */
import { test, expect, type Page } from '@playwright/test';
import { vraieApp, stockage, ouvrirPagePlus, sonde } from './aides.ts';

type Ou = 'page +' | 'Cercle' | 'Promi' | 'Chiche';

/** le relevé du geste : un focus donné pendant un `pointerup`/`touchend` (avant que l'événement ait fini de passer) est « dans le geste » */
const GESTE = (): void => {
  const w = window as unknown as { __geste: boolean; __focus: Array<{ cls: string; dans: boolean }> };
  w.__geste = false;
  w.__focus = [];
  for (const t of ['pointerup', 'touchend', 'click'] as const) {
    window.addEventListener(
      t,
      () => {
        w.__geste = true;
      },
      true,
    );
    window.addEventListener(t, () => {
      w.__geste = false;
    });
  }
  document.addEventListener(
    'focusin',
    (ev) => {
      w.__focus.push({ cls: String((ev.target as Element).className), dans: w.__geste });
    },
    true,
  );
};

async function nouvellePage(browser: import('@playwright/test').Browser): Promise<Page> {
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    hasTouch: true,
    isMobile: true,
  });
  const pg = await ctx.newPage();
  await pg.addInitScript(GESTE);
  return pg;
}
/** un vrai toucher (les événements tactiles, puis ceux du pointeur et le clic que le navigateur en tire) au centre d'un élément */
async function doigt(pg: Page, sel: string, mot = ''): Promise<void> {
  const c = await pg.evaluate(
    ([sel, mot]) => {
      const e = [...document.querySelectorAll<HTMLElement>(sel!)].find(
        (x) => (x.textContent ?? '').includes(mot!) && x.getBoundingClientRect().width > 0,
      );
      if (!e) return null;
      const r = e.getBoundingClientRect();
      return [r.left + Math.min(30, r.width / 2), r.top + Math.min(20, r.height / 2)];
    },
    [sel, mot],
  );
  if (!c) throw new Error(`introuvable : ${sel} « ${mot} »`);
  await pg.touchscreen.tap(c[0]!, c[1]!);
  await pg.waitForTimeout(700);
}
/** la rangée des personnes dépliée (page + : `#csPeauf` ; fiche : `#dpdCorps` ; un Cercle : la carte `#npMemb`) */
const REG: Record<Ou, string> = {
  'page +': '#csPeauf .s2-reg.s2-ouv',
  Cercle: '#dpdCorps #npMemb.np-ouv',
  Promi: '#dpdCorps .s2-reg.s2-ouv',
  Chiche: '#dpdCorps .s2-reg.s2-ouv',
};

/** ouvre Peaufiner sur les personnes, dépliées (le doigt, comme Tom) */
async function ouvrirPersonnes(pg: Page, ou: Ou): Promise<void> {
  await vraieApp(pg, stockage());
  if (ou === 'page +') {
    await ouvrirPagePlus(pg, 'nuee');
    await doigt(pg, '#csBotBar');
    await pg.waitForTimeout(1200);
    await doigt(pg, '#csPeauf .s2-reg', 'MEMBRES');
  } else {
    await pg.evaluate(`(() => { const P = window.__promi; const e = P.magasin.etat();
      if (${JSON.stringify(ou)} === 'Cercle') { const k = P.magasin.creerCercle('Plage', [], Date.now()); P.fiche().ouvrirCercle(k); return; }
      const q = e.paroles.find((x) => !x.draft && !x.nuee && !!x.chiche === ${String(ou === 'Chiche')} && x.status !== 'tenu') ?? e.paroles.find((x) => !x.draft && !x.nuee);
      P.fiche().ouvrir(q.id); })()`);
    await pg.waitForFunction(() => {
      const f = document.getElementById('detailPoster');
      return !!f && !f.hidden && !f.classList.contains('fi-bas');
    });
    await pg.waitForTimeout(800);
    await doigt(pg, '.fi-plus-membres');
  }
  await pg.waitForFunction((s) => !!document.querySelector(s), REG[ou]);
  await pg.waitForTimeout(1200);
}

// les titres (les sondes les nomment) :
//   « page + : les personnes dans Peaufiner — … » (membres-saut, prenom-focus-perdu)
//   « Cercle : les personnes dans Peaufiner — … » (membres-hors-rangee)
//   « Promi : les personnes dans Peaufiner — … » (prenom-focus-tard)
//   « Chiche : les personnes dans Peaufiner — … »
for (const ou of ['page +', 'Cercle', 'Promi', 'Chiche'] as const) {
  test(`${ou} : les personnes dans Peaufiner — rien ne bouge 30 s sans geste ; le prénom, focus dans le geste ; aucun chevauchement ; « Toi, pour l’instant »`, async ({
    browser,
  }) => {
    test.setTimeout(120000);
    const pg = await nouvellePage(browser);
    const erreurs: string[] = [];
    pg.on('pageerror', (e) => erreurs.push(String(e)));
    // la sonde : un recalcul qui fait sauter l'écran tout seul, toutes les 5 s (le défaut vu sur l'iPhone)
    if (sonde('membres-saut'))
      await pg.addInitScript(() => {
        setInterval(() => {
          for (const c of document.querySelectorAll<HTMLElement>('#csPeauf, #dpdCorps'))
            c.scrollTop = c.scrollTop > 40 ? 0 : 160;
        }, 5000);
      });
    // la sonde : le focus du prénom donné APRÈS le geste (le clavier d'iOS ne s'ouvre pas)
    if (sonde('prenom-focus-tard'))
      await pg.addInitScript(() => {
        const f = HTMLElement.prototype.focus;
        HTMLElement.prototype.focus = function (this: HTMLElement, o?: FocusOptions) {
          if (this.classList.contains('gn-saisie')) setTimeout(() => f.call(this, o), 30);
          else f.call(this, o);
        };
      });
    // la sonde : le défaut de l'iPhone rejoué — le `mousedown` de compatibilité donne le focus à la zone, l'entrée du prénom le perd
    if (sonde('prenom-focus-perdu'))
      await pg.addInitScript(() => {
        document.addEventListener(
          'mousedown',
          (ev) => {
            (ev.target as Element).closest<HTMLElement>('.ph-add')?.focus();
          },
          true,
        );
      });
    // la sonde : la liste hors du flux de la rangée (le chevauchement vu sur l'iPhone)
    if (sonde('membres-hors-rangee'))
      await pg.addInitScript(() => {
        const s = document.createElement('style');
        s.textContent = '#csPeauf .gn, #dpdCorps .gn{position:absolute!important}';
        document.documentElement.appendChild(s);
      });
    await ouvrirPersonnes(pg, ou);
    const reg = REG[ou];

    // AUCUN CHEVAUCHEMENT : pastilles et « + ajouter quelqu'un » dans la rangée, la suite sous elle
    const geo = (await pg.evaluate((reg) => {
      const r = document.querySelector(reg)!;
      const R = r.getBoundingClientRect();
      const dedans = [...r.querySelectorAll('.ph-o')].map((e) => {
        const b = e.getBoundingClientRect();
        return {
          nom: (e.textContent ?? '').trim().slice(0, 16),
          ok: b.top >= R.top - 0.5 && b.bottom <= R.bottom + 0.5 && b.left >= R.left - 0.5 && b.right <= R.right + 0.5,
        };
      });
      // la rangée (ou la carte) suivante commence sous elle
      const suite = [...(r.parentElement?.children ?? [])].find(
        (x) => x !== r && x.getBoundingClientRect().top > R.top && x.getBoundingClientRect().height > 10,
      );
      const st = suite ? suite.getBoundingClientRect().top : Infinity;
      return {
        dedans,
        n: dedans.length,
        suiteSous: st >= R.bottom - 0.5,
        val: r.querySelector('.s2-val, .np-val')?.textContent,
      };
    }, reg)) as { dedans: Array<{ nom: string; ok: boolean }>; n: number; suiteSous: boolean; val: string | null };
    expect(geo.n, 'des pastilles et « + ajouter quelqu’un »').toBeGreaterThan(1);
    expect(
      geo.dedans.filter((x) => !x.ok).map((x) => x.nom),
      'chaque pastille DANS la rangée',
    ).toEqual([]);
    expect(geo.suiteSous, 'la suite commence sous la rangée').toBe(true);
    // « Toi, pour l’instant » : sur un Cercle seul (page + et fiche)
    if (ou === 'page +' || ou === 'Cercle') expect(geo.val?.trim(), 'seul, MEMBRES le dit').toBe('Toi, pour l’instant');

    // RIEN NE BOUGE SANS UN GESTE : une pastille cochée (sur un Cercle), puis 30 s sans toucher
    if (ou === 'page +' || ou === 'Cercle') {
      await doigt(pg, `${reg} .ph-o:not(.ph-add)`);
      await pg.waitForTimeout(2500);
    }
    const ref = await pg.screenshot();
    const changes: number[] = [];
    for (let t = 3; t <= 30; t += 3) {
      await pg.waitForTimeout(3000);
      if (!(await pg.screenshot()).equals(ref)) changes.push(t);
    }
    expect(changes, 'aucun changement d’écran sans geste (secondes où l’écran a changé)').toEqual([]);

    // LE PRÉNOM : focus dans le geste, puis le nom est choisi
    await pg.evaluate(() => {
      (window as unknown as { __focus: unknown[] }).__focus.length = 0;
    });
    await doigt(pg, `${reg} .ph-add`);
    await pg.waitForTimeout(300);
    const f = (await pg.evaluate(
      () => (window as unknown as { __focus: Array<{ cls: string; dans: boolean }> }).__focus,
    )) as Array<{
      cls: string;
      dans: boolean;
    }>;
    const saisie = f.find((x) => x.cls.includes('gn-saisie'));
    expect(saisie, 'l’entrée du prénom reçoit le focus').toBeTruthy();
    expect(saisie?.dans, 'le focus est donné DANS le geste (iOS : le clavier s’ouvre)').toBe(true);
    expect(
      await pg.evaluate(() => !!document.activeElement?.classList.contains('gn-saisie')),
      'l’entrée GARDE le focus après le geste (le clavier reste ouvert)',
    ).toBe(true);
    await pg.keyboard.type('Lou');
    await pg.keyboard.press('Enter');
    await pg.waitForTimeout(800);
    const pris = (await pg.evaluate((reg) => {
      const r = document.querySelector(reg);
      return [...(r?.querySelectorAll('.ph-o.on') ?? [])].map((b) => (b.textContent ?? '').trim());
    }, reg)) as string[];
    expect(
      pris.some((x) => x.includes('Lou')),
      `Lou choisie (${pris.join(', ')})`,
    ).toBe(true);
    expect(erreurs).toEqual([]);
  });
}
