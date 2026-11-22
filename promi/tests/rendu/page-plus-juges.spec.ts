/**
 * LOT 2a — LES JUGES DE LA PAGE + DEVENUS DES TESTS (C-326). Chacun porte sa décision EN DUR, avec sa source, et rougit sur sa sonde.
 * La vraie app, ouverte par le vrai chemin (le + puis la pilule) ; les gestes au pointeur (la page lit le toucher lui-même : appui puis lever).
 * La correspondance juge → test → sonde : promi/JUGES-TESTS.md, « Lot 2a ».
 */
import { test, expect, type Page } from '@playwright/test';
import { stockage, vraieApp, ouvrirPlus, ouvrirPagePlus, P_, sonde, xSousLeDoigt } from './aides.ts';

type Nat = 'promi' | 'chiche' | 'nuee';

async function ouvrir(page: Page, nat: Nat, ls: Record<string, string> = stockage()): Promise<void> {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, ls);
  await ouvrirPagePlus(page, nat);
}
/** un toucher au centre d'un élément (la souris de Playwright : pointerdown puis pointerup) */
async function toucher(page: Page, sel: string): Promise<void> {
  const r = await page.evaluate((s) => {
    const b = document.querySelector(s)!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  }, sel);
  await page.mouse.click(r[0]!, r[1]!);
  await page.waitForTimeout(150);
  // le choix qui s'ouvre ou se ferme est un mouvement (Q598) : on touche la suite une fois tout posé (hors du Mac une image dure 0,7 s)
  await posee(page);
}
const etat = (
  page: Page,
): Promise<{
  phrase: { nat: Nat; sens: string; titre: string; qui: string[]; avec: string[]; pinceau: string; moi: boolean };
  base: number;
  hz: number;
  taille: number;
  choix: string | null;
  gardeActif: boolean;
  exemples: Record<string, string>;
}> => page.evaluate(`${P_}.pagePlus().etat()`) as never;
/** le texte rendu de la phrase, ligne par ligne (les <br>) */
const lignes = (page: Page): Promise<string[]> =>
  page.evaluate(() => {
    const t = document.querySelector('#createSheet .ph-txt')!;
    const h = t.innerHTML.replace(/<br>/g, '\n').replace(/<[^>]+>/g, '');
    const d = document.createElement('textarea');
    d.innerHTML = h;
    return d.value.split('\n').map((l) => l.replace(/\s+/g, ' ').trim());
  });

// ── redteam_menu_plus, redteam_tuiles (C-152 : « l'encart Cercle ouvre la page + au doigt, à chaque fois » ; v148 C-142 ; SPEC-ECRANS §3) ──
test('le menu du + : chaque pilule ouvre SA page +, à chaque fois ; le X la referme en glissant (redteam_menu_plus, redteam_tuiles)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // la sonde : la pilule ouvre toujours la page + d'un Promi (la tuile touchée ne décide plus — le défaut du carrousel d'avant, 13 sept.)
  if (sonde('menu-nature'))
    await page.evaluate(
      `(() => { const n = ${P_}.nav; const pp = ${P_}.pagePlus(); n.poser('pagePlus', () => pp.ouvrir('promi')); })()`,
    );
  const MOT: Record<Nat, string> = { promi: 'PROMI', chiche: 'CHICHE', nuee: 'CERCLE' };
  for (const tour of [1, 2])
    for (const nat of ['nuee', 'chiche', 'promi'] as const) {
      await ouvrirPlus(page);
      await toucher(page, `#accChoix .acc-pil[data-k="${nat}"]`);
      await page.waitForFunction(
        () => {
          const c = document.getElementById('createSheet')!;
          return !c.hidden && !c.classList.contains('pp-compose') && !c.classList.contains('pp-entre');
        },
        undefined,
        { timeout: 20000 },
      );
      const r = await page.evaluate(() => {
        const c = document.getElementById('createSheet')!;
        const m = c.querySelector<HTMLElement>('.cs-mark')!;
        return { cls: c.className, mot: m.innerText.replace(/\s+/g, '') };
      });
      expect(r.cls, `tour ${String(tour)}, ${nat}`).toContain('pp-' + nat);
      expect(r.mot, `le mot du plateau dit la nature (tour ${String(tour)})`).toBe(MOT[nat]);
      // le X : la page part en glissant vers le bas (une transition, jamais d'un coup — C-271), puis l'accueil
      // la classe se relève DANS la page, à la mutation (sous charge, la lecture d'après pouvait tomber après la fin du glissement)
      await page.evaluate(() => {
        const c = document.getElementById('createSheet')!;
        const w = window as unknown as { __part: unknown };
        w.__part = null;
        const o = new MutationObserver(() => {
          if (c.classList.contains('pp-part') && !w.__part) {
            const s = getComputedStyle(c);
            w.__part = { classe: true, duree: s.transitionDuration, prop: s.transitionProperty };
            o.disconnect();
          }
        });
        o.observe(c, { attributes: true, attributeFilter: ['class'] });
      });
      // la page posée (aucun passage, aucun mouvement), puis le X — et ce qu'il y a sous le doigt, pour nommer une cause s'il ne prend pas
      await posee(page);
      const xx = await xSousLeDoigt(page, '#createSheet .closeb');
      const sous = await page.evaluate(
        ([x, y]) => {
          const e = document.elementFromPoint(x!, y!);
          return `${e ? e.tagName.toLowerCase() + '.' + String(e.className) : '∅'} ; #createSheet.${document.getElementById('createSheet')!.className}`;
        },
        [xx[0], xx[1]],
      );
      await page.mouse.click(xx[0], xx[1]);
      await page
        .waitForFunction(() => !!(window as unknown as { __part: unknown }).__part, undefined, { timeout: 5000 })
        .catch(() => undefined);
      const part = ((await page.evaluate(() => (window as unknown as { __part: unknown }).__part)) ?? {
        classe: false,
        duree: '0s',
        prop: '',
      }) as { classe: boolean; duree: string; prop: string };
      expect(part.classe, `la page + part (pp-part) — sous le doigt : ${sous}`).toBe(true);
      expect(part.prop).toContain('transform');
      expect(parseFloat(part.duree)).toBeGreaterThanOrEqual(0.4);
      await page.waitForFunction(() => document.getElementById('createSheet')!.hidden, undefined, { timeout: 20000 });
    }
});

// ── redteam_pilules (v115 : « les trois pilules du + se lisent », ≥ 4,5:1, deux thèmes) ──
for (const theme of ['sombre', 'clair'] as const)
  test(`les trois pilules du menu du + se lisent, ≥ 4,5:1, ${theme} (redteam_pilules)`, async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await vraieApp(page, { ...stockage(), promi_theme: theme === 'clair' ? 'light' : 'dark' });
    await ouvrirPlus(page);
    // la sonde : le texte des pilules prend la couleur de leur fond
    if (sonde('pilules-illisibles'))
      await page.addStyleTag({
        content: '#accChoix .acc-pil *{color:#8a6f6f!important;-webkit-text-fill-color:#8a6f6f!important}',
      });
    const L = await page.evaluate(() => {
      const lum = (c: string): number => {
        const v = (c.match(/[\d.]+/g) ?? ['0', '0', '0']).slice(0, 3).map((x) => +x / 255);
        const f = (x: number): number => (x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4);
        return 0.2126 * f(v[0]!) + 0.7152 * f(v[1]!) + 0.0722 * f(v[2]!);
      };
      const fond = (e: Element): string => {
        for (let q: Element | null = e; q; q = q.parentElement) {
          const b = getComputedStyle(q).backgroundColor;
          if (b && !/rgba\(.*,\s*0\)$/.test(b) && b !== 'transparent') return b;
        }
        return 'rgb(0,0,0)';
      };
      const out: Array<[string, number]> = [];
      for (const e of document.querySelectorAll('#accChoix .acc-pil *')) {
        if (![...e.childNodes].some((n) => n.nodeType === 3 && (n.textContent ?? '').trim())) continue;
        const a = lum(getComputedStyle(e).color);
        const b = lum(fond(e));
        out.push([(e.textContent ?? '').trim(), (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)]);
      }
      return out;
    });
    expect(L.length).toBeGreaterThanOrEqual(6);
    for (const [t, r] of L) expect(r, `« ${t} »`).toBeGreaterThanOrEqual(4.5);
  });

// ── redteam_phrase, redteam_verbe, redteam_demande (SPEC-ECRANS §3 « la phrase, nature par nature » ; le cycle du verbe) ──
test('la phrase de chaque nature, et le cycle du verbe d’un Promi : à soi → à quelqu’un → promets-moi → à soi (redteam_phrase, redteam_verbe, redteam_demande)', async ({
  page,
}) => {
  await ouvrir(page, 'promi');
  // la sonde : le verbe ne répond plus au toucher (le défaut que redteam_verbe prend : « la bascule mène à un vrai bouton »)
  if (sonde('verbe-sourd')) await page.addStyleTag({ content: '#createSheet .ph-b{pointer-events:none!important}' });
  expect(await lignes(page)).toEqual(['Je me promets', 'de me coucher', 'le jour même']);
  await toucher(page, '#createSheet .ph-b[data-ph="sens"]');
  const l2 = await lignes(page);
  expect(l2[0], 'à quelqu’un : « Je promets »').toBe('Je promets');
  expect(l2.at(-1), '« à qui ? » ferme la phrase').toBe('à qui ?');
  expect((await etat(page)).exemples['faire'], 'l’exemple de « je te promets »').toBe(
    't’emmener voir la mer / vous emmener voir la mer',
  );
  await toucher(page, '#createSheet .ph-b[data-ph="sens"]');
  const l3 = await lignes(page);
  expect(l3[0], 'promets-moi : la place du prénom en tête, l’exemple de v211 (C-309)').toMatch(
    /^(Bruno-Stanislas|Fabienne-Gudule)$/,
  );
  expect(l3[1]).toBe('promets-moi');
  await toucher(page, '#createSheet .ph-b[data-ph="sens"]');
  expect((await lignes(page))[0], 'retour à soi').toBe('Je me promets');
  // le Chiche et le Cercle : un verbe fixe, sans ⇄
  await page.evaluate(`${P_}.pagePlus().ouvrir('chiche')`);
  expect(await lignes(page)).toEqual(
    ['à qui ose ?', 'Chiche', 'de choisir une ville', 'au hasard', 'avec qui en est ?']
      .slice(0, 2)
      .concat((await lignes(page)).slice(2)),
  );
  const lc = await lignes(page);
  expect(lc.slice(0, 2)).toEqual(['à qui ose ?', 'Chiche']);
  expect(lc.at(-1)).toBe('avec qui en est ?');
  expect(
    await page.evaluate(() => document.querySelectorAll('#createSheet .ph-b svg').length),
    'le Chiche n’a pas de ⇄',
  ).toBe(0);
  await page.evaluate(`${P_}.pagePlus().ouvrir('nuee')`);
  const ln = await lignes(page);
  expect(ln[0]).toBe('Je lance un Cercle');
  expect(ln.join(' ')).toContain('nommé Week-end à Marseille');
  expect(ln.at(-1)).toBe('avec tout le monde');
});

// ── redteam_suggestions (v115, v179b), C-312 (la liaison d'une place vide est celle de son exemple) ──
test('les exemples des pastilles vides : la phrase 1, puis la 2, puis tirées sans remise ; la liaison est celle de l’exemple (redteam_suggestions, C-312)', async ({
  page,
}) => {
  const ls = stockage();
  await ouvrir(page, 'promi', ls);
  // la sonde : le tirage rend toujours la première phrase
  if (sonde('exemple-fige')) await page.evaluate(`${P_}.magasin.tirerExemple = () => 0`);
  const vus: string[] = [];
  for (let i = 0; i < 4; i++) {
    if (i) await page.evaluate(`${P_}.pagePlus().ouvrir('promi')`);
    const e = await etat(page);
    vus.push(e.exemples['soi']!);
    const l = await page.evaluate(() => document.querySelector('#createSheet em.ph-li')!.textContent);
    // la règle de « de » / « d’ » (liaison_regle.py, en dur) : voyelle → d’, sinon de
    expect(l, `la liaison de « ${e.exemples['soi']!} »`).toBe(
      /^[aeiouéèêh]/i.test(e.exemples['soi']!) && !/^h(a|u)/i.test(e.exemples['soi']!) ? 'd’' : 'de',
    );
  }
  expect(vus[0], 'ouverture 1 : la phrase 1 de Tom').toBe('me coucher le jour même');
  expect(vus[1], 'ouverture 2 : la phrase 2').toBe('finir ce livre avant d’en ouvrir trois');
  expect(new Set(vus).size, 'aucune phrase ne revient (sans remise)').toBe(4);
  const a = (await page.evaluate(`${P_}.magasin.etat().autres`)) as Record<string, string>;
  expect(a['promi_ex_soi'], 'le compteur est gardé (clé du prototype)').toBe('4');
});

// ── redteam_marges (v115 : « marge droite = marge gauche, retour à la ligne plutôt que réduction ») ──
test('la phrase tient dans ses marges : l’exemple passe à la ligne plutôt que de réduire la phrase sous 28 (redteam_marges)', async ({
  page,
}) => {
  await ouvrir(page, 'chiche');
  // la sonde : la phrase décalée de 40 pt (sa marge droite n'est plus celle de gauche : elle sort par la droite)
  if (sonde('marges-deborde')) await page.addStyleTag({ content: '#createSheet .pp-phrase{translate:40px 0}' });
  for (const nat of ['chiche', 'promi', 'nuee'] as const) {
    await page.evaluate(`${P_}.pagePlus().ouvrir('${nat}')`);
    await page.waitForTimeout(100);
    const r = await page.evaluate(() => {
      const t = document.querySelector('#createSheet .ph-txt')!;
      let droite = 0;
      for (const q of t.getClientRects()) droite = Math.max(droite, q.right);
      for (const e of t.querySelectorAll('*'))
        for (const q of e.getClientRects()) if (q.width > 0) droite = Math.max(droite, q.right);
      return { droite, taille: parseFloat(getComputedStyle(t).fontSize), coupe: t.classList.contains('ph-coupe') };
    });
    expect(r.droite, `${nat} : la marge droite (366 = 390 − 24)`).toBeLessThanOrEqual(366.5);
    if (r.coupe) expect(r.taille, `${nat} : coupée, la phrase reste ≥ 28`).toBeGreaterThanOrEqual(28);
  }
});

// ── redteam_gens, redteam_ajouter, redteam_moi_toucher (lot-GENS ; v116 ; C-304) ──
test('le choix des personnes : « moi » à la place touchée, ajouter et retirer au toucher, « + ajouter quelqu’un » au-dessus de Peaufiner (redteam_gens, redteam_ajouter, redteam_moi_toucher)', async ({
  page,
}) => {
  await ouvrir(page, 'chiche');
  // la sonde : une personne touchée n'est plus prise
  if (sonde('gens-sourd'))
    await page.addStyleTag({ content: '#createSheet .gn .ph-o[data-v]{pointer-events:none!important}' });
  await toucher(page, '#createSheet .ph-m[data-ph="qui"]');
  expect((await etat(page)).choix).toBe('qui');
  expect((await lignes(page))[0], 'C-304 : la place passe à « moi »').toBe('à moi');
  const tete = await page.evaluate(() => document.querySelector('#createSheet .gn .ph-o')!.textContent);
  expect(tete, '« Moi » en tête, choisi').toBe('MMoi');
  const nom = await page.evaluate(
    () => document.querySelector<HTMLElement>('#createSheet .gn .ph-o[data-v]')!.dataset['v']!,
  );
  await toucher(page, `#createSheet .gn .ph-o[data-v="${nom}"]`);
  // C-332 (Tom, 22 nov. 2026) : « Moi » reste à côté de la personne ajoutée (avant : elle le remplaçait)
  expect((await etat(page)).phrase.qui).toEqual(['Moi', nom]);
  const l = await lignes(page);
  expect(
    l.slice(0, 2),
    'C-269, C-332, Q624 : « à Rachel et moi, / chiche » (ce qui est coché, « moi » en dernier, une virgule, « chiche » en bas de casse)',
  ).toEqual([`à ${nom} et moi,`, 'chiche']);
  await toucher(page, `#createSheet .gn .ph-o[data-v="${nom}"] .ppo-x`);
  expect((await etat(page)).phrase.qui, 'sa croix la retire').toEqual([]);
  const b = await page.evaluate(() => {
    const a = document.querySelector('#createSheet .gn .ph-add')!.getBoundingClientRect();
    const l = document.querySelector('#createSheet .gn .gn-liste')!.getBoundingClientRect();
    const p = document.getElementById('csBotBar')!.getBoundingClientRect();
    return { a: [a.top, a.bottom], l: l.bottom, p: p.top };
  });
  expect(b.a[0], '« + ajouter quelqu’un » sous la liste, sur sa ligne').toBeGreaterThan(b.l);
  expect(b.p - b.a[1]!, '16 pt d’air au-dessus de Peaufiner (v116)').toBeGreaterThanOrEqual(16);
  // un toucher ailleurs referme le choix
  await page.mouse.click(195, 150);
  await page.waitForTimeout(150);
  expect((await etat(page)).choix).toBeNull();
});

// ── redteam_garder (C-149 v148, v151) ──
test('« garder de côté » : inactif tant que rien n’a changé ; actif, il garde la page entière dans le magasin et la referme (redteam_garder)', async ({
  page,
}) => {
  await ouvrir(page, 'chiche');
  // la sonde : le toucher ne garde rien
  if (sonde('garder-rien')) await page.evaluate(`${P_}.magasin.garderDeCote = () => 0`);
  const g0 = await page.evaluate(() => {
    const g = document.querySelector('#createSheet .pp-garder')!;
    const r = g.getBoundingClientRect();
    const c = document.getElementById('createSheet')!.getBoundingClientRect();
    return {
      inactif: g.classList.contains('inactif'),
      couleur: getComputedStyle(g).color,
      bas: r.bottom,
      // le bord droit de sa boîte (avant l'inclinaison de 5,5°, dont l'origine est son coin bas droit)
      droite: c.width - parseFloat(getComputedStyle(g).right),
      skew: getComputedStyle(g).transform,
      td: getComputedStyle(g).textDecorationLine,
    };
  });
  expect(g0.inactif, 'inactif à l’ouverture').toBe(true);
  expect(g0.td, 'jamais souligné (v149)').toBe('none');
  // la place décidée : à droite (son bord à 24 pt), 718 + 2 (C-149, v151, v163)
  expect(Math.round(g0.droite)).toBe(366);
  expect(g0.skew, 'penché de 5,5° (v149)').toBe('matrix(1, 0, -0.096289, 1, 0, 0)');
  expect(Math.round(g0.bas), 'son bas à 736 (718 + 2, sa hauteur 16)').toBe(736);
  const n0 = (await page.evaluate(`${P_}.magasin.etat().paroles.length`)) as number;
  await toucher(page, '#createSheet .pp-garder');
  expect(await page.evaluate(() => document.getElementById('createSheet')!.hidden), 'inactif, il ne fait rien').toBe(
    false,
  );
  await toucher(page, '#createSheet .pc-t[data-t="Coulé"]');
  expect((await etat(page)).gardeActif, 'un changement le rend actif').toBe(true);
  await toucher(page, '#createSheet .pp-garder');
  const e = (await page.evaluate(`${P_}.magasin.etat()`)) as {
    paroles: Array<{ draft?: boolean; chiche?: boolean; brouillon?: { nat: string; pinceau?: string } }>;
    fil: Array<{ text: string }>;
  };
  expect(e.paroles.length, 'un gardé de côté de plus').toBe(n0 + 1);
  const g = e.paroles.at(-1)!;
  expect([g.draft, g.chiche, g.brouillon?.nat, g.brouillon?.pinceau]).toEqual([true, true, 'chiche', 'Coulé']);
  expect(e.fil[0]!.text).toContain('de côté');
  await page.waitForFunction(() => document.getElementById('createSheet')!.hidden, undefined, { timeout: 20000 });
});

// ── redteam_pinceau_rail (C-196, v163b) ──
test('le rail du pinceau glisse ; les traits de Ma Parole ! sont un mur, flou, que le toucher ne choisit pas (redteam_pinceau_rail)', async ({
  page,
}) => {
  await ouvrir(page, 'promi');
  // la sonde : le rail ne glisse plus (le défaut de v163a : on n'atteignait pas les douze traits)
  if (sonde('rail-fige'))
    await page.addStyleTag({ content: '#csPinceau{overflow:hidden!important;touch-action:none!important}' });
  const r = await page.evaluate(() => {
    const p = document.getElementById('csPinceau')!;
    const s = getComputedStyle(p);
    p.scrollLeft = 200;
    const gl = p.scrollLeft;
    p.scrollLeft = 0;
    return {
      ox: s.overflowX,
      ta: s.touchAction,
      deborde: p.scrollWidth - p.clientWidth,
      glisse: gl,
      n: p.querySelectorAll('.pc-t').length,
      murs: [...p.querySelectorAll('.pc-t.pc-mur')].map((b) => getComputedStyle(b).filter),
    };
  });
  expect(r.ox).toBe('auto');
  expect(r.ta).toBe('pan-x');
  expect(r.deborde).toBeGreaterThan(0);
  expect(r.glisse).toBe(200);
  expect(r.n, 'douze traits').toBe(12);
  expect(r.murs, 'huit murs, flous de 4,8 px').toEqual(Array(8).fill('blur(4.8px)'));
  expect((await etat(page)).phrase.pinceau).toBe('Plein');
  await toucher(page, '#createSheet .pc-t[data-t="Peigné"]');
  expect((await etat(page)).phrase.pinceau, 'un trait libre se choisit').toBe('Peigné');
  await page.evaluate(() => {
    document.getElementById('csPinceau')!.scrollLeft = 300;
  });
  await toucher(page, '#createSheet .pc-t[data-t="Tressé"]');
  expect((await etat(page)).phrase.pinceau, 'un mur ne se choisit pas').toBe('Peigné');
});

// ── redteam_clavier (v114 : le clavier s'ouvre DANS le geste) ; la saisie du titre ──
test('la saisie : le clavier s’ouvre dans le geste, la frappe remplit la pastille, Retour valide (redteam_clavier)', async ({
  page,
}) => {
  await ouvrir(page, 'promi');
  // la sonde : le champ prend le focus hors du geste (plus tard : iOS n'ouvre alors pas le clavier)
  if (sonde('clavier-differe'))
    await page.evaluate(() => {
      const f = HTMLElement.prototype.focus;
      HTMLElement.prototype.focus = function (this: HTMLElement, o?: FocusOptions) {
        void Promise.resolve().then(() => {
          setTimeout(() => f.call(this, o), 50);
        });
      };
    });
  const pt = await page.evaluate(() => {
    const b = document.querySelector('#createSheet .ph-m[data-ph="titre"]')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  });
  // le focus lu DANS la tâche du lever du doigt
  await page.evaluate(() => {
    const w = window as unknown as { __focus: string };
    w.__focus = '';
    window.addEventListener('pointerup', () => queueMicrotask(() => (w.__focus = document.activeElement?.id ?? '')), {
      capture: false,
    });
  });
  await page.mouse.click(pt[0]!, pt[1]!);
  expect(await page.evaluate('window.__focus'), 'le champ a le focus dans la tâche du geste').toBe('phIn');
  await page.keyboard.type('appeler Lou');
  await page.waitForTimeout(100);
  expect((await lignes(page)).slice(1).join(' '), 'la frappe remplit la pastille, la liaison suit (« d’ »)').toBe(
    'd’ appeler Lou',
  );
  await page.keyboard.press('Enter');
  await page.waitForTimeout(100);
  expect(await page.evaluate(() => document.activeElement?.id ?? ''), 'Retour valide (le clavier se ferme)').not.toBe(
    'phIn',
  );
  const p = await page.evaluate(() => {
    const m = document.querySelector('#createSheet .ph-m[data-ph="titre"]')!;
    return {
      vide: m.classList.contains('ph-vide'),
      bord: getComputedStyle(m).borderTopStyle,
      fond: getComputedStyle(m).backgroundColor,
    };
  });
  // contrat remis au niveau du prototype rendu (fin du 2a : « remplie = crème / encre ; vide = 3 px pointillé ») — il attendait un contour plein
  expect(p).toEqual({ vide: false, bord: 'none', fond: 'rgb(247, 240, 222)' });
  expect((await etat(page)).gardeActif, 'la page a changé : « garder de côté » actif').toBe(true);
});

// ── C-213, C-229 : à l'ouverture, RIEN du trait ; l'horizon est BAS (40 pt), jamais à moins de 12 pt de l'encre de la phrase ──
test('à l’ouverture, rien du trait et l’horizon bas (C-213, C-229)', async ({ page }) => {
  await ouvrir(page, 'promi');
  // la sonde : le mot du trait paraît dès l'ouverture (la page + d'avant v172)
  if (sonde('trait-ouverture'))
    await page.evaluate(() => {
      const d = document.createElement('div');
      d.className = 'pp-trace';
      d.textContent = 'trace pour planter';
      d.style.cssText = 'position:absolute;left:85px;top:330px;z-index:9;color:#fff';
      document.getElementById('createSheet')!.appendChild(d);
    });
  for (const nat of ['promi', 'chiche', 'nuee'] as const) {
    await page.evaluate(`${P_}.pagePlus().ouvrir('${nat}')`);
    const r = await page.evaluate(() => {
      const c = document.getElementById('createSheet')!;
      const txt = [...c.querySelectorAll('*')].filter((e) => {
        const r = e.getBoundingClientRect();
        return r.width > 0 && getComputedStyle(e).visibility !== 'hidden' && /trace|continue/.test(e.textContent ?? '');
      });
      return txt.map((e) => e.textContent);
    });
    expect(r, `${nat} : aucun mot du trait`).toEqual([]);
    const e = await etat(page);
    expect(e.hz, `${nat} : l’horizon est bas (0 à 40 pt plus bas que sa place)`).toBeGreaterThan(0);
    expect(e.hz).toBeLessThanOrEqual(40);
  }
});

// ── C-330 et C-331 (Tom, 22 nov. 2026) — « garder de côté » inactif à la teinte de SA nature ; la page + MONTE à l'ouverture, le mouvement
//    exact de sa fermeture à l'envers (même courbe, même durée). Deux écarts admis au prototype (page-plus.spec.ts, ECARTS_ADMIS). ──
test('C-330, C-331 : « garder de côté » inactif à la teinte de sa nature ; la page + monte en glissant à l’ouverture, comme elle descend à la fermeture', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // les sondes : la teinte du prototype (le bleu du Promi sur les trois natures) ; l'ouverture d'un coup (la transition retirée)
  if (sonde('garder-teinte'))
    await page.addStyleTag({ content: '#createSheet .pp-garder.inactif{color:#AFCBFB!important}' });
  if (sonde('ouverture-seche')) await page.addStyleTag({ content: '#createSheet.pp-entre{transition:none!important}' });
  const TEINTE: Record<Nat, string> = {
    promi: 'rgb(130, 174, 248)',
    chiche: 'rgb(255, 184, 210)',
    nuee: 'rgb(201, 168, 245)',
  };
  const fautes: string[] = [];
  for (const nat of ['promi', 'chiche', 'nuee'] as const) {
    await ouvrirPlus(page);
    // l'ouverture relevée dans la page, à chaque image : la transition posée, et la place de la page (sa translation)
    await page.evaluate(() => {
      const c = document.getElementById('createSheet')!;
      const w = window as unknown as { __entre: { duree: string; prop: string; ty: number[]; fin: boolean } | null };
      w.__entre = null;
      const ty = (): number => new DOMMatrix(getComputedStyle(c).transform).m42;
      const o = new MutationObserver(() => {
        if (c.classList.contains('pp-entre') && !w.__entre) {
          const s = getComputedStyle(c);
          const e = { duree: s.transitionDuration, prop: s.transitionProperty, ty: [ty()], fin: false };
          w.__entre = e;
          const pas = (): void => {
            e.ty.push(ty());
            if (c.classList.contains('pp-entre')) requestAnimationFrame(pas);
            else e.fin = true;
          };
          requestAnimationFrame(pas);
        }
      });
      o.observe(c, { attributes: true, attributeFilter: ['class'] });
    });
    await toucher(page, `#accChoix .acc-pil[data-k="${nat}"]`);
    await page.waitForFunction(
      () => {
        const w = window as unknown as { __entre: { fin: boolean } | null };
        return !!w.__entre?.fin;
      },
      undefined,
      { timeout: 20000 },
    );
    const e = (await page.evaluate(() => (window as unknown as { __entre: unknown }).__entre)) as {
      duree: string;
      prop: string;
      ty: number[];
    };
    if (!e.prop.includes('transform') || Math.abs(parseFloat(e.duree) - 0.46) > 0.01)
      fautes.push(`${nat} : l'ouverture n'a pas la transition de la fermeture (${e.prop} ${e.duree})`);
    const H = 844;
    if (process.platform === 'darwin' && !e.ty.some((y) => y > 1 && y < H - 1))
      fautes.push(`${nat} : aucune image entre le bas et sa place (${JSON.stringify(e.ty.map(Math.round))})`);
    if (Math.abs(e.ty.at(-1)!) > 0.5)
      fautes.push(`${nat} : la page n'est pas à sa place à la fin (${String(e.ty.at(-1))})`);
    const g = await page.evaluate(() => {
      const x = document.querySelector('#createSheet .pp-garder')!;
      return { inactif: x.classList.contains('inactif'), couleur: getComputedStyle(x).color };
    });
    if (!g.inactif) fautes.push(`${nat} : « garder de côté » actif à l'ouverture`);
    if (g.couleur !== TEINTE[nat])
      fautes.push(`${nat} : « garder de côté » inactif ${g.couleur}, décidé ${TEINTE[nat]}`);
    await toucher(page, '#createSheet .closeb');
    await page.waitForFunction(() => document.getElementById('createSheet')!.hidden, undefined, { timeout: 20000 });
  }
  expect(fautes).toEqual([]);
});

// ══════════════════════════════════════ FIN DU 2a ══════════════════════════════════════

/** un toucher au doigt (appui puis lever, sans souris) au centre d'un élément */
async function doigt(page: Page, sel: string): Promise<void> {
  await page.evaluate((s) => {
    const e = document.querySelector<HTMLElement>(s)!;
    const r = e.getBoundingClientRect();
    const o = { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2, pointerId: 31 };
    e.dispatchEvent(new PointerEvent('pointerdown', o));
    e.dispatchEvent(new PointerEvent('pointerup', o));
  }, sel);
  await page.waitForTimeout(150);
}
/** plus aucun mouvement de la page, plus aucun passage en flaques */
const posee = (page: Page): Promise<unknown> =>
  page.waitForFunction(
    `!document.querySelector('#createSheet [data-flaques-mode]') && !document.querySelector('#createSheet .ph-mt') && !${P_}.pagePlus?.()?.etat().mouvement`,
    undefined,
    { timeout: 20000 },
  );

// ── redteam_gens (le Cercle), redteam_moi_toucher (C-304) — le choix d'un Cercle est celui du prototype (lot-GENS) : la place « avec » passe
//    à « moi », « Moi » en tête et choisi (avec sa croix), un membre ajouté se met à côté (C-332), retiré seul il revient ; Gilbert 23,1, « Moi » au
//    mauve profond #291547 (`#nueePhrase .gn .ph-o.on{background:var(--c-mauve12)}`), 25 pt sous la phrase (`#nueeChoix .gn{margin-top:25px}`) ──
test('le choix d’un Cercle : « avec moi », « Moi » en tête et choisi, au mauve profond, Gilbert 23,1 ; un membre se met à côté (C-332), retiré seul il revient (redteam_gens, C-304)', async ({
  page,
}) => {
  await ouvrir(page, 'nuee');
  // la sonde : les pastilles d'un Cercle à la taille de celles d'un Chiche (le défaut d'avant : le choix d'un Chiche à la place)
  if (sonde('cercle-chiche'))
    await page.addStyleTag({
      content: '#createSheet.pp-nuee .gn .ph-o{font-size:16px!important;line-height:16px!important}',
    });
  await doigt(page, '#createSheet .ph-m[data-np="avec"]');
  await posee(page);
  const r = await page.evaluate(() => {
    const ph = document.querySelector('#createSheet .ph-txt')!;
    const b = [...document.querySelectorAll<HTMLElement>('#createSheet .gn .ph-o:not(.ph-add)')];
    const t = b[0]!;
    const s = getComputedStyle(t);
    const g = document.querySelector('#createSheet .gn')!.getBoundingClientRect();
    return {
      avec: (ph.textContent ?? '').replace(/\s+/g, ' ').trim(),
      tete: t.textContent,
      on: t.classList.contains('on'),
      croix: !!t.querySelector('.ppo-x'),
      fond: s.backgroundColor,
      taille: s.fontSize,
      air: g.top - ph.getBoundingClientRect().bottom,
    };
  });
  expect(r.avec, 'la place « avec » passe à « moi » (C-304)').toMatch(/avec moi$/);
  expect([r.tete, r.on, r.croix], '« Moi » en tête, choisi, avec sa croix').toEqual(['MMoi', true, true]);
  expect(r.fond, '« Moi » choisi au mauve profond #291547').toBe('rgb(41, 21, 71)');
  expect(r.taille, 'Gilbert 23,1 (le prototype : `#createSheet .ph-o{font-size:23.1px}`)').toBe('23.1px');
  expect(Math.round(r.air), '25 pt sous la phrase').toBe(25);
  await doigt(page, '#createSheet .gn .ph-o[data-v="Maman"]');
  const e1 = await etat(page);
  expect((e1.phrase as unknown as { membres: string[] }).membres, 'un membre ajouté, « Moi » à côté (C-332)').toEqual([
    'Moi',
    'Maman',
  ]);
  expect(
    await page.evaluate(() => document.querySelector('#createSheet .gn .ph-o[data-gn-tete]')!.classList.contains('on')),
    '« Moi » reste choisi (C-332 : un membre ne le remplace plus)',
  ).toBe(true);
  await doigt(page, '#createSheet .gn .ph-o[data-v="Maman"] .ppo-x');
  await doigt(page, '#createSheet .gn .ph-o[data-gn-tete] .ppo-x');
  const fin = await page.evaluate(() => ({
    tete: document.querySelector('#createSheet .gn .ph-o[data-gn-tete]')!.classList.contains('on'),
    avec: (document.querySelector('#createSheet .ph-txt')!.textContent ?? '').replace(/\s+/g, ' ').trim(),
  }));
  expect(fin, 'retiré seul, « Moi » revient ; la place dit « moi »').toEqual({
    tete: true,
    avec: expect.stringMatching(/avec moi$/) as unknown as string,
  });
});

// ── redteam_invite_page_plus (C-209, C-213, C-229) — à l'ouverture et pendant la saisie, RIEN du trait ; la parole validée (Retour), l'horizon
//    REMONTE d'abord, PUIS le trait naît (en flaques), le libellé se TRACE, le départ clignote en phase avec le I de PROMI jusqu'au premier
//    toucher ; la parole effacée, tout repart (en flaques, le libellé détracé) et l'horizon redescend ──
const INVITE: Record<Nat, string> = {
  promi:
    'l’invite à tracer, promi : rien avant la validation ; l’horizon remonte, puis le trait naît, le libellé se trace, le départ clignote avec le I ; effacée, tout repart (redteam_invite_page_plus)',
  chiche:
    'l’invite à tracer, chiche : rien avant la validation ; l’horizon remonte, puis le trait naît, le libellé se trace, le départ clignote avec le I ; effacée, tout repart (redteam_invite_page_plus)',
  nuee: 'l’invite à tracer, nuee : rien avant la validation ; l’horizon remonte, puis le trait naît, le libellé se trace, le départ clignote avec le I ; effacée, tout repart (redteam_invite_page_plus)',
};
for (const nat of ['promi', 'chiche', 'nuee'] as const)
  test(INVITE[nat], async ({ page }) => {
    await ouvrir(page, nat);
    // les sondes : le libellé paraît d'un coup (aucun tracé) ; le départ ne clignote pas
    if (sonde('invite-sec'))
      await page.evaluate(() => {
        const P = (window as unknown as { __promi: { chargerTrace(): unknown } }).__promi;
        P.chargerTrace();
        const w = window as unknown as {
          TraceLettres: { trace: (c: unknown, t: unknown, o?: { surFin?: (r: unknown) => void }) => unknown };
        };
        w.TraceLettres.trace = (_c: unknown, _t: unknown, o?: { surFin?: (r: unknown) => void }) => {
          setTimeout(() => o?.surFin?.({ interrompu: false }), 0);
          return { stop() {}, etat: () => ({}) };
        };
      });
    if (sonde('invite-fixe')) await page.addStyleTag({ content: '#ppDepart.clignote{animation:none!important}' });
    const lire = (): Promise<{ vis: boolean; haut: boolean; hz: number; depart: string | null; lib: boolean }> =>
      page.evaluate(`(() => { const e = ${P_}.pagePlus().etat(); return { vis: e.invite.visible, haut: e.invite.haut, hz: e.hz,
        depart: document.getElementById('csTrameCv').getAttribute('data-depart'), lib: !document.querySelector('#createSheet .pp-trace').hidden }; })()`);
    const r0 = await lire();
    expect([r0.vis, r0.depart, r0.lib], 'à l’ouverture : rien du trait (ni départ, ni libellé)').toEqual([
      false,
      null,
      false,
    ]);
    expect(r0.hz, 'à l’ouverture : l’horizon est plus bas que sa place').toBeGreaterThan(0);
    const titre = nat === 'nuee' ? '#createSheet .ph-m[data-np="nom"]' : '#createSheet .ph-m[data-ph="titre"]';
    await doigt(page, titre);
    await posee(page);
    await page.keyboard.type('appeler Lou');
    await page.waitForTimeout(400);
    expect((await lire()).vis, 'pendant la saisie : rien du trait (C-229)').toBe(false);
    // ce qui se passe, image par image, de Retour à la naissance du trait
    await page.evaluate(`(() => { const w = window; w.__inv = []; const f = () => { const e = ${P_}.pagePlus().etat(); const l = document.querySelector('#createSheet .pp-trace');
      w.__inv.push({ hz: e.hz, vis: e.invite.visible, anim: e.invite.anim, clip: !l.hidden && !!(l.style.clipPath || l.style.getPropertyValue('-webkit-clip-path')) });
      if (w.__inv.length < 2000) requestAnimationFrame(f); }; requestAnimationFrame(f); })()`);
    await page.keyboard.press('Enter');
    await page.waitForFunction(
      `(() => { const e = ${P_}.pagePlus().etat(); return e.invite.visible && !document.querySelector('#createSheet canvas.passage-flaques') && !window.TraceLettres?.actif(); })()`,
      undefined,
      { timeout: 30000 },
    );
    const S = (await page.evaluate('window.__inv')) as { hz: number; vis: boolean; anim: boolean; clip: boolean }[];
    const premier = S.findIndex((x) => x.vis);
    expect(premier, 'le trait naît').toBeGreaterThanOrEqual(0);
    expect(S[premier]!.hz, 'le trait naît l’horizon remonté (C-229 : d’abord l’horizon, puis le trait)').toBe(0);
    if (process.platform === 'darwin')
      expect(
        S.slice(0, premier).some((x) => x.anim),
        'l’horizon remonte d’un mouvement (360 ms), jamais d’un coup',
      ).toBe(true);
    expect(
      S.some((x) => x.vis && x.clip),
      'le libellé « trace pour … » se trace (découpé par le tracé), jamais d’un coup',
    ).toBe(true);
    const r1 = await lire();
    expect([r1.vis, r1.lib, !!r1.depart], 'le trait né : le départ et le libellé').toEqual([true, true, true]);
    // le départ clignote avec le I de PROMI (la même animation, la même phase)
    const ph = (await page.evaluate(() => {
      const f = (n: Element | null): number | null => {
        const a = n?.getAnimations().find((x) => (x as CSSAnimation).animationName === 'promiBlink');
        return a?.currentTime != null ? Number(a.currentTime) : null;
      };
      return [f(document.getElementById('ppDepart')), f(document.querySelector('.acc-mm i'))];
    })) as (number | null)[];
    expect(ph[0], 'le départ clignote (promiBlink)').not.toBeNull();
    if (ph[1] != null) {
      const d = Math.abs(((ph[0]! - ph[1]) % 1150) + 1150) % 1150;
      expect(Math.min(d, 1150 - d), 'en phase avec le I de PROMI (± 60 ms)').toBeLessThan(60);
    }
    // le premier toucher du trait : le départ cesse de clignoter
    const pt =
      (await page.evaluate(`(() => { const e = ${P_}.pagePlus().etat(); const cs = document.getElementById('createSheet'); const C = cs.getBoundingClientRect();
      const k = C.width / cs.offsetWidth; const h = parseFloat(getComputedStyle(cs).getPropertyValue('--pp-h')) || 0; const [x, y] = document.getElementById('csTrameCv').getAttribute('data-depart').split(',').map(Number);
      return [C.left + x * k, C.top + (y + h) * k]; })()`)) as number[];
    await page.evaluate(
      ([x, y]) => {
        const t = document.elementFromPoint(x!, y!) ?? document.getElementById('createSheet')!;
        t.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, clientX: x!, clientY: y!, pointerId: 51 }));
        t.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, clientX: x!, clientY: y!, pointerId: 51 }));
      },
      [pt[0], pt[1]],
    );
    expect(
      await page.evaluate(() => document.getElementById('ppDepart')!.classList.contains('clignote')),
      'le premier toucher du trait : le départ reste orange, fixe',
    ).toBe(false);
    // la parole effacée : tout repart, puis l'horizon redescend
    await doigt(page, titre);
    await posee(page);
    for (let i = 0; i < 12; i++) await page.keyboard.press('Backspace');
    await page.keyboard.press('Enter');
    await page.waitForFunction(
      `(() => { const e = ${P_}.pagePlus().etat(); return !e.invite.visible && !e.invite.sortie && e.invite.haut && !e.invite.anim; })()`,
      undefined,
      { timeout: 30000 },
    );
    const r2 = await lire();
    expect([r2.vis, r2.lib, r2.depart], 'effacée : le trait et le libellé partis').toEqual([false, false, null]);
    expect(r2.hz, 'puis l’horizon redescend').toBeGreaterThan(0);
  });

// ── redteam_moitie, redteam_plantation_durable, redteam_dalle_unique (C-237, C-226, C-241) — planter, c'est tracer la MOITIÉ du trait (un Cercle :
//    le trait entier, au lever) : lâché avant, rien n'est planté et le trait revient ; arrivé au milieu, la parole est écrite tout de suite
//    (avant le lever, avant toute animation), donnée au moteur, la page part sous la dalle qui naît et vole ; une seule dalle à la fois ;
//    rechargée, la parole est là ──
const PLANTER: Record<Nat, string> = {
  promi:
    'planter, promi : lâché avant la moitié rien n’est planté ; au milieu la parole est écrite, la dalle naît et vole, la page part ; rechargée, elle est là (redteam_moitie, redteam_plantation_durable)',
  chiche:
    'planter, chiche : lâché avant la moitié rien n’est planté ; au milieu la parole est écrite, la dalle naît et vole, la page part ; rechargée, elle est là (redteam_moitie, redteam_plantation_durable)',
  nuee: 'planter, nuee : lâché avant la moitié rien n’est planté ; au milieu la parole est écrite, la dalle naît et vole, la page part ; rechargée, elle est là (redteam_moitie, redteam_plantation_durable)',
};
for (const nat of ['promi', 'chiche', 'nuee'] as const)
  test(PLANTER[nat], async ({ page }) => {
    test.setTimeout(120000);
    await ouvrir(page, nat);
    // les sondes : la parole jamais écrite ; la parole jamais donnée au moteur
    if (sonde('plante-sans-ecrire'))
      await page.evaluate(
        `(() => { const m = ${P_}.magasin; m.planter = () => m.etat().compteurs.nid; m.creerCercle = () => 'n0'; })()`,
      );
    if (sonde('plante-sans-toile'))
      await page.evaluate(`(() => { const f = ${P_}.facade; f.planterUne = () => {}; f.planterCercle = () => {}; })()`);
    const titre = nat === 'nuee' ? '#createSheet .ph-m[data-np="nom"]' : '#createSheet .ph-m[data-ph="titre"]';
    await doigt(page, titre);
    await posee(page);
    await page.keyboard.type('appeler Lou');
    await page.keyboard.press('Enter');
    await page.waitForFunction(`${P_}.pagePlus().etat().invite.visible`, undefined, { timeout: 30000 });
    await page.waitForFunction(() => !document.querySelector('#createSheet canvas.passage-flaques'), undefined, {
      timeout: 20000,
    });
    const compte = (): Promise<{ n: number; c: number; g: number }> =>
      page.evaluate(`(() => { const e = ${P_}.magasin.etat(); return { n: e.paroles.length, c: Object.keys(e.cercles).length,
        g: window.Toile_lecture ? window.Toile_lecture().graines.filter((x) => x.pid != null || x.kind === 'nuee').length : -1 }; })()`);
    const n0 = await compte();
    const depart =
      (await page.evaluate(`(() => { const cs = document.getElementById('createSheet'); const C = cs.getBoundingClientRect();
      const k = C.width / cs.offsetWidth; const h = parseFloat(getComputedStyle(cs).getPropertyValue('--pp-h')) || 0;
      const [x, y] = document.getElementById('csTrameCv').getAttribute('data-depart').split(',').map(Number); return [C.left + x * k, C.top + (y + h) * k, k]; })()`)) as number[];
    const [x0, y0, k] = depart as [number, number, number];
    const trace = async (jusqua: number): Promise<void> => {
      await page.mouse.move(x0, y0);
      await page.mouse.down();
      for (let x = x0; x <= jusqua * k; x += 8 * k) await page.mouse.move(x, y0);
    };
    // 1 · lâché avant la moitié (un Cercle : avant 60 pt d'avancée, C-107 — il se lance au lever dès qu'ils sont tracés) : rien n'est
    //     planté, le trait revient
    await trace(nat === 'nuee' ? 80 : 150);
    await page.mouse.up();
    await page.waitForTimeout(600);
    expect(await compte(), 'lâché avant la moitié : rien n’est planté').toEqual(n0);
    expect(
      await page.evaluate(`(() => { const e = ${P_}.pagePlus(); return e.ouverte() && e.etat().invite.visible; })()`),
      'la page reste, le trait revenu',
    ).toBe(true);
    // 2 · arrivé au milieu (un Cercle : au bout, puis le lever) : écrite tout de suite
    await trace(nat === 'nuee' ? 340 : 200);
    if (nat === 'nuee') await page.mouse.up();
    const n1 = await compte();
    if (nat === 'nuee') expect(n1.c, 'le Cercle est créé au lever, dans la tâche du trait (C-226)').toBe(n0.c + 1);
    else expect(n1.n, 'la parole est écrite au milieu, avant le lever (C-237, C-226)').toBe(n0.n + 1);
    if (nat !== 'nuee') {
      // C-241 : une seule dalle à la fois — la page + ne peint plus la sienne, celle qui naît est là
      const r = await page.evaluate(() => ({
        nait: !!document.querySelector('#ppNait canvas:last-child'),
        haut: document.getElementById('csTrameCv')!.hasAttribute('data-matiere'),
      }));
      expect(r.nait, 'la dalle naît au trait').toBe(true);
      await page.mouse.up();
    }
    await page.waitForFunction(
      `(() => document.getElementById('createSheet').hidden && !document.getElementById('ppNait'))()`,
      undefined,
      { timeout: 8000 },
    );
    expect((await compte()).g, 'le moteur a reçu la parole (une graine de plus)').toBe(n0.g + 1);
    // 3 · rechargée : elle est là (écrite dans le stockage au trait)
    await page.reload();
    await page.waitForFunction(`!!${P_}?.magasin`, undefined, { timeout: 20000 });
    const n2 = await compte();
    if (nat === 'nuee') expect(n2.c, 'rechargée, le Cercle est là').toBe(n0.c + 1);
    else expect(n2.n, 'rechargée, la parole est là').toBe(n0.n + 1);
  });

// ── C-332 (Tom, 22 nov. 2026) — « MOI » SE COCHE ET SE DÉCOCHE COMME N'IMPORTE QUELLE PERSONNE : on peut toujours le remettre, il coexiste avec
//    les autres, le toucher ne retire jamais quelqu'un d'autre, la liste n'est jamais vide ; la phrase dit exactement ce qui est coché, par le
//    détracé puis le tracé (C-279) — la place neuve ne paraît jamais avant que l'ancienne soit partie ──
const MOI_TITRES: Record<Nat, string> = {
  promi:
    'le choix des personnes, promi : « Moi » se coche et se décoche, coexiste, revient quand la liste se vide ; la phrase change par détracé puis tracé (C-332)',
  chiche:
    'le choix des personnes, chiche : « Moi » se coche et se décoche, coexiste, revient quand la liste se vide ; la phrase change par détracé puis tracé (C-332)',
  nuee: 'le choix des personnes, nuee : « Moi » se coche et se décoche, coexiste, revient quand la liste se vide ; la phrase change par détracé puis tracé (C-332)',
};
for (const nat of ['promi', 'chiche', 'nuee'] as const)
  test(MOI_TITRES[nat], async ({ page }) => {
    await ouvrir(page, nat);
    // les sondes : l'ancien défaut (toucher « Moi » retire les autres) ; un changement sec (la place change sans tracé)
    if (sonde('moi-exclusif'))
      await page.evaluate(() =>
        document.addEventListener(
          'pointerup',
          (e) => {
            if (!(e.target as Element).closest?.('[data-gn-tete]')) return;
            setTimeout(() => {
              for (const x of document.querySelectorAll<HTMLElement>('#createSheet .gn .ph-o.on[data-v] .ppo-x')) {
                const r = x.getBoundingClientRect();
                const o = {
                  bubbles: true,
                  clientX: r.left + r.width / 2,
                  clientY: r.top + r.height / 2,
                  pointerId: 41,
                };
                x.dispatchEvent(new PointerEvent('pointerdown', o));
                x.dispatchEvent(new PointerEvent('pointerup', o));
              }
            }, 0);
          },
          true,
        ),
      );
    if (sonde('moi-sec'))
      await page.evaluate(() => {
        // (le module chargé d'abord : la page le charge au premier usage, et le chargement poserait le vrai par-dessus)
        const P = (window as unknown as { __promi: { chargerTrace(): unknown } }).__promi;
        P.chargerTrace();
        const w = window as unknown as {
          TraceLettres: { trace: (c: unknown, t: unknown, o?: { surFin?: (r: unknown) => void }) => unknown };
        };
        w.TraceLettres.trace = (_c: unknown, _t: unknown, o?: { surFin?: (r: unknown) => void }) => {
          setTimeout(() => o?.surFin?.({ interrompu: false }), 0);
          return { stop() {}, etat: () => ({}) };
        };
      });
    const place = nat === 'nuee' ? '#createSheet .ph-m[data-np="avec"]' : '#createSheet .ph-m[data-ph="qui"]';
    if (nat === 'promi') {
      await doigt(page, '#createSheet .ph-b[data-ph="sens"]');
      await posee(page);
    }
    await doigt(page, place);
    await posee(page);
    // ce que montre la place, à chaque mutation de la phrase : son texte, et s'il est découpé par le tracé (en cours de détracé ou de tracé)
    await page.evaluate((sel) => {
      const w = window as unknown as { __moi: { t: string; env: boolean }[] };
      w.__moi = [];
      const txt = document.querySelector('#createSheet .ph-txt')!;
      new MutationObserver(() => {
        const e = document.querySelector(sel);
        // découpé : le texte est sous la découpe du tracé (le module la pose en ligne, `clip-path`)
        const env = e?.querySelector<HTMLElement>('.ph-mt');
        const clip = !!env && !!(env.style.clipPath || env.style.getPropertyValue('-webkit-clip-path'));
        w.__moi.push({ t: (e?.textContent ?? '').replace(/\s+/g, ' ').trim(), env: clip });
      }).observe(txt, { subtree: true, childList: true, attributes: true, characterData: true });
    }, place);
    const calme = (): Promise<unknown> =>
      page.waitForFunction(
        () =>
          !(window as unknown as { TraceLettres?: { actif(): boolean } }).TraceLettres?.actif() &&
          !document.querySelector('#createSheet .ph-mt'),
        undefined,
        { timeout: 30000 },
      );
    const lire = (): Promise<{ moi: boolean; on: string[]; place: string }> =>
      page.evaluate(
        (sel) => ({
          moi: !!document.querySelector('#createSheet .gn .ph-o.on[data-gn-tete]'),
          on: [...document.querySelectorAll<HTMLElement>('#createSheet .gn .ph-o.on[data-v]')].map(
            (b) => b.dataset['v']!,
          ),
          place: (document.querySelector(sel)?.textContent ?? '').replace(/\s+/g, ' ').trim(),
        }),
        place,
      );
    const [autre, autre2] = (await page.evaluate(() =>
      [...document.querySelectorAll<HTMLElement>('#createSheet .gn .ph-o[data-v]')]
        .slice(0, 2)
        .map((b) => b.dataset['v']!),
    )) as [string, string];
    const sep = nat === 'nuee' ? ' · ' : ', ';
    const fin = nat === 'chiche' ? ',' : '';
    const tete = '#createSheet .gn .ph-o[data-gn-tete]';
    const moiSeul = { moi: true, on: [], place: 'moi' };
    // ⚑ Q624 (Tom) : « moi » en dernier, après « et » — « à Maman et moi », « à Maman, Rachel et moi », « avec Maman et moi »
    const avecMoi = { moi: true, on: [autre], place: `${autre} et moi${fin}` };
    const pas: { nom: string; sel: string; attendu: { moi: boolean; on: string[]; place: string } }[] = [
      { nom: 'retirer Moi, seul : il revient (la liste n’est jamais vide)', sel: tete, attendu: moiSeul },
      {
        nom: `ajouter ${autre} : « Moi » reste, en dernier`,
        sel: `#createSheet .gn .ph-o[data-v="${autre}"]`,
        attendu: avecMoi,
      },
      {
        nom: `ajouter ${autre2} : « ${autre}${sep}${autre2} et moi »`,
        sel: `#createSheet .gn .ph-o[data-v="${autre2}"]`,
        attendu: { moi: true, on: [autre, autre2], place: `${autre}${sep}${autre2} et moi${fin}` },
      },
      { nom: `retirer ${autre2}`, sel: `#createSheet .gn .ph-o[data-v="${autre2}"] .ppo-x`, attendu: avecMoi },
      { nom: `retirer Moi : ${autre} reste`, sel: tete, attendu: { moi: false, on: [autre], place: `${autre}${fin}` } },
      { nom: `remettre Moi : à côté de ${autre}, en dernier`, sel: tete, attendu: avecMoi },
      {
        nom: `retirer ${autre} : « Moi » seul`,
        sel: `#createSheet .gn .ph-o[data-v="${autre}"] .ppo-x`,
        attendu: moiSeul,
      },
      { nom: 'tout retirer (Moi, le dernier) : il revient', sel: tete, attendu: moiSeul },
    ];
    let avant = 'moi';
    for (const p of pas) {
      await page.evaluate(() => ((window as unknown as { __moi: unknown[] }).__moi = []));
      await doigt(page, p.sel);
      await calme();
      expect(await lire(), p.nom).toEqual(p.attendu);
      if (p.attendu.place !== avant) {
        // C-279 : l'ancienne place se détrace (son texte, découpé), puis la neuve se trace ; elle ne paraît jamais sans sa découpe
        const s = (await page.evaluate(() => (window as unknown as { __moi: { t: string; env: boolean }[] }).__moi))!;
        const i = s.findIndex((x) => x.t === avant && x.env);
        const j = s.findIndex((x) => x.t === p.attendu.place);
        expect(i, `${p.nom} : « ${avant} » se détrace d’abord`).toBeGreaterThanOrEqual(0);
        expect(j, `${p.nom} : « ${p.attendu.place} » paraît après le détracé`).toBeGreaterThan(i);
        expect(s[j]!.env, `${p.nom} : « ${p.attendu.place} » paraît en se traçant, jamais d’un coup`).toBe(true);
      }
      avant = p.attendu.place;
    }
  });

// ── redteam_clavier_doux (Q598, v177a), C-234 (v180b), redteam_je (C-303, v210) — la saisie ouvre la page « montée » d'un MOUVEMENT, la
//    fermeture du clavier la rend à sa place d'un mouvement : 360 ms (décidé : 300 à 400), jamais d'un coup ; « DÉJÀ PROMIS » paraît en
//    flaques et, à la validation, sa copie descend : rien ne disparaît d'un coup ──
/** les titres écrits en toutes lettres (outils/sondes.ts retrouve le test d'une sonde par son titre) */
const SAISIE: Record<Nat, string> = {
  promi:
    'la saisie, promi : la page monte et revient d’un mouvement de 360 ms, jamais d’un coup ; rien ne part d’un coup (redteam_clavier_doux, redteam_je)',
  chiche:
    'la saisie, chiche : la page monte et revient d’un mouvement de 360 ms, jamais d’un coup ; rien ne part d’un coup (redteam_clavier_doux, redteam_je)',
  nuee: 'la saisie, nuee : la page monte et revient d’un mouvement de 360 ms, jamais d’un coup ; rien ne part d’un coup (redteam_clavier_doux, redteam_je)',
};
for (const nat of ['promi', 'chiche', 'nuee'] as const)
  test(SAISIE[nat], async ({ page }) => {
    await ouvrir(page, nat);
    // la sonde : « Réduire les animations » posé en douce — la page se pose d'un coup
    if (sonde('saisie-seche'))
      await page.evaluate(() => {
        const m = window.matchMedia.bind(window);
        window.matchMedia = (q: string) =>
          (/reduce/.test(q) ? { matches: true, media: q } : m(q)) as unknown as MediaQueryList;
      });
    // la sonde : la copie de « DÉJÀ PROMIS » ne descend pas, elle est retirée d'un coup
    if (sonde('deja-sec')) await page.addStyleTag({ content: '#createSheet .ppo-copie{display:none!important}' });
    const avant = await page.evaluate(() => {
      const c = document.getElementById('createSheet')!.getBoundingClientRect();
      return document.querySelector('#createSheet .pp-phrase')!.getBoundingClientRect().top - c.top;
    });
    // le relevé, à chaque image : la place de la phrase et de la barre ; ce qui peint et part (redteam_je)
    await page.evaluate(() => {
      const w = window as unknown as {
        __m: Array<{ ph: number; barre: number; t: number }>;
        __partis: string[];
        __on: boolean;
      };
      w.__m = [];
      w.__partis = [];
      w.__on = true;
      const cs = document.getElementById('createSheet')!;
      const vus = new Map<Element, { nom: string; sel: string; r: number[]; flaques: boolean; hors: boolean }>();
      const peint = (s: CSSStyleDeclaration): boolean =>
        (s.borderTopStyle !== 'none' && parseFloat(s.borderTopWidth) > 0.5) ||
        !/rgba\(.*,\s*0\)$|transparent/.test(s.backgroundColor) ||
        false;
      const f = (): void => {
        const C = cs.getBoundingClientRect();
        const r = (sel: string): number => {
          const e = cs.querySelector(sel);
          return e && (e as HTMLElement).offsetParent ? e.getBoundingClientRect().top - C.top : NaN;
        };
        w.__m.push({ ph: r('.pp-phrase'), barre: r('#csBotBar'), t: performance.now() });
        const ici = (e: Element): boolean => {
          const s = getComputedStyle(e);
          return !(s.display === 'none' || s.visibility === 'hidden' || (e as HTMLElement).closest('[hidden]'));
        };
        for (const [e, o] of vus) {
          if (e.isConnected && ici(e)) continue;
          vus.delete(e);
          if (o.flaques || o.hors) continue;
          // un nœud rebâti à sa place (même rôle, même coin à 2 pt : « DÉJÀ PROMIS » se recompose à chaque frappe ; sa copie prend sa
          // place dans la tâche de la validation) n'est pas un départ
          const remplace = [...cs.querySelectorAll(o.sel)].some((x) => {
            if (!ici(x)) return false;
            const q = x.getBoundingClientRect();
            return Math.abs(q.left - o.r[0]!) <= 2 && Math.abs(q.top - o.r[1]!) <= 2;
          });
          if (!remplace) w.__partis.push(o.nom);
        }
        // (la phrase elle-même se recompose — ses mots qui changent : C-271, au 2c ; on juge ici ce que ce lot fait paraître et partir)
        for (const e of cs.querySelectorAll('.ppo-dejas *, .ppo-copie *, #csPinceau, .pp-garder, #csBotBar')) {
          const s = getComputedStyle(e);
          if (s.display === 'none' || s.visibility === 'hidden' || (e as HTMLElement).closest('[hidden]')) continue;
          if (!peint(s) && !(e.textContent ?? '').trim()) continue;
          const b = e.getBoundingClientRect();
          vus.set(e, {
            nom: `${e.className || e.id} « ${(e.textContent ?? '').trim().slice(0, 20)} »`,
            sel: e.id ? '#' + e.id : '.' + String(e.className).trim().split(/\s+/)[0]!,
            r: [b.left, b.top],
            flaques: !!(e as HTMLElement).closest('[data-flaques-mode="couvre"]'),
            hors: b.top > C.bottom - 1 || !b.height,
          });
        }
        if (w.__on) requestAnimationFrame(f);
      };
      requestAnimationFrame(f);
    });
    const champ = nat === 'nuee' ? '#createSheet .ph-m[data-np="nom"]' : '#createSheet .ph-m[data-ph="titre"]';
    await page.evaluate(() => {
      for (const s of ['#csPinceau', '#createSheet .pp-garder']) {
        const e = document.querySelector<HTMLElement>(s);
        if (e && !e.hidden && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden')
          e.dataset['avant'] = '1';
      }
    });
    // le toucher (appui puis lever, comme le doigt) — et, DANS SA TÂCHE, le mouvement part de la place d'avant : la mesure ne dépend pas
    // de la cadence des images (hors du Mac une image dure 0,7 s, le mouvement de 360 ms y tient dans une seule)
    const auToucher = (await page.evaluate(
      ([s, P]) => {
        const e = document.querySelector<HTMLElement>(s as string)!;
        const b = e.getBoundingClientRect();
        const o = { bubbles: true, clientX: b.left + b.width / 2, clientY: b.top + b.height / 2, pointerId: 21 };
        e.dispatchEvent(new PointerEvent('pointerdown', o));
        e.dispatchEvent(new PointerEvent('pointerup', o));
        const c = document.getElementById('createSheet')!.getBoundingClientRect();
        // ce qui part (le rail, « garder de côté » ; la barre pour un titre) : dans la tâche du toucher il est encore à l'écran — en flaques
        // ou en train de glisser —, jamais retiré d'un coup
        const ici = (e: Element | null): boolean =>
          !!e &&
          !(e as HTMLElement).hidden &&
          getComputedStyle(e).display !== 'none' &&
          getComputedStyle(e).visibility !== 'hidden';
        const secs: string[] = [];
        for (const s of ['#csPinceau', '#createSheet .pp-garder']) {
          const e = document.querySelector(s);
          if (e && (e as HTMLElement).dataset['avant'] === '1' && !ici(e)) secs.push(s);
        }
        return {
          mv: (new Function(`return ${P as string}.pagePlus().etat().mouvement`) as () => boolean)(),
          ph: document.querySelector('#createSheet .pp-phrase')!.getBoundingClientRect().top - c.top,
          secs,
          barre: ici(document.getElementById('csBotBar')),
        };
      },
      [champ, P_] as const,
    )) as { mv: boolean; ph: number; secs: string[]; barre: boolean };
    await posee(page);
    const ouvert = (await page.evaluate(
      () => (window as unknown as { __m: Array<{ ph: number; barre: number }> }).__m,
    )) as Array<{
      ph: number;
      barre: number;
      t: number;
    }>;
    const e1 = await etat(page);
    expect(e1.base, 'la page montée : l’onde à 144 (cadres 18 à 23)').toBe(144);
    // la place posée se lit sur la page (hors du Mac la dernière image relevée peut précéder la fin du mouvement)
    const phPosee = await page.evaluate(() => {
      const c = document.getElementById('createSheet')!.getBoundingClientRect();
      return document.querySelector('#createSheet .pp-phrase')!.getBoundingClientRect().top - c.top;
    });
    expect(Math.abs(phPosee - 230), 'la phrase à 230 (228 + le pas du trait ×1,3), ± 1').toBeLessThanOrEqual(1);
    // le mouvement d'ouverture part dans la tâche du toucher, de la place d'avant (jamais d'un coup) — sur toute machine
    expect(auToucher.mv, 'au toucher, un mouvement commence').toBe(true);
    expect(Math.abs(auToucher.ph - avant), 'au toucher, la phrase est encore à sa place d’avant').toBeLessThanOrEqual(
      1,
    );
    expect(
      auToucher.secs,
      'au toucher, ce qui part est encore à l’écran (en flaques), jamais retiré d’un coup (redteam_je)',
    ).toEqual([]);
    expect(auToucher.barre, 'au toucher, la barre est encore là : elle descend (§2.11), jamais d’un coup').toBe(true);
    const course = Math.abs(avant - phPosee);
    // les images intermédiaires : sur le Mac seulement (hors du Mac une image dure 0,7 s, le mouvement entier tient dans une)
    if (process.platform === 'darwin') {
      const i0 = ouvert.findIndex((m) => Math.abs(m.ph - avant) > 0.5);
      expect(i0, 'la phrase quitte sa place').toBeGreaterThanOrEqual(0);
      expect(
        Math.abs(ouvert[i0]!.ph - phPosee),
        'la première image qui bouge n’est pas la place finale',
      ).toBeGreaterThan(course * 0.3);
      const pas = Math.max(...ouvert.slice(i0).map((m, k, a) => (k ? Math.abs(m.ph - a[k - 1]!.ph) : 0)));
      expect(pas, `aucun pas au-delà de 35 % de la course (${course.toFixed(0)} pt)`).toBeLessThanOrEqual(
        course * 0.35 + 0.5,
      );
    }
    if (nat !== 'nuee') {
      const d = await page.evaluate(() => {
        const l = document.querySelector('#createSheet .ppo-deja');
        return { lab: l?.textContent ?? '', pastilles: document.querySelectorAll('#createSheet .ppo-d').length };
      });
      expect(d.lab, '« DÉJÀ PROMIS » pendant la saisie d’un titre').toBe('DÉJÀ PROMIS');
      expect(d.pastilles, 'les paroles déjà promises (deux au plus)').toBeGreaterThanOrEqual(1);
      expect(
        await page.evaluate(() => document.getElementById('csBotBar')!.hidden),
        '§2.11 : la barre Peaufiner se cache pendant la saisie',
      ).toBe(true);
    }
    await page.keyboard.type('nager');
    // la page posée avant Retour (la phrase qui change de lignes glisse, C-278 ; hors du Mac une image dure 0,7 s)
    await posee(page);
    await page.evaluate(() => {
      (window as unknown as { __m: unknown[] }).__m = [];
    });
    const t0 = await page.evaluate(() => performance.now());
    // Retour (la touche, sur le champ qui a le focus) — et, dans sa tâche, le mouvement de retour part de la place de saisie
    const auRetour = (await page.evaluate((P) => {
      const c = document.getElementById('createSheet')!.getBoundingClientRect();
      const ph0 = document.querySelector('#createSheet .pp-phrase')!.getBoundingClientRect().top - c.top;
      const ici = (e: Element | null): boolean =>
        !!e &&
        !(e as HTMLElement).hidden &&
        getComputedStyle(e).display !== 'none' &&
        getComputedStyle(e).visibility !== 'hidden';
      const dejaAvant = ici(document.querySelector('#createSheet .ppo-dejas'));
      document.activeElement!.dispatchEvent(
        new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }),
      );
      // C-303 : « DÉJÀ PROMIS » descend avec le clavier — sa copie est posée DANS la tâche de la validation, visible
      const copie = document.querySelector('#createSheet .ppo-copie');
      return {
        ph0,
        mv: (new Function(`return ${P}.pagePlus().etat().mouvement`) as () => boolean)(),
        ph: document.querySelector('#createSheet .pp-phrase')!.getBoundingClientRect().top - c.top,
        deja: !dejaAvant || ici(copie),
      };
    }, P_)) as { ph0: number; mv: boolean; ph: number; deja: boolean };
    await posee(page);
    await page.waitForTimeout(300);
    const R = (await page.evaluate(() => {
      const w = window as unknown as { __m: unknown; __partis: string[]; __on: boolean };
      w.__on = false;
      return { m: w.__m, partis: w.__partis };
    })) as { m: Array<{ ph: number; barre: number; t: number }>; partis: string[] };
    const e2 = await etat(page);
    expect(e2.base, 'revenue : l’onde à sa place').toBeGreaterThan(144);
    // le retour part dans la tâche de Retour, de la place de saisie (jamais d'un coup) — sur toute machine
    expect(auRetour.mv, 'à Retour, un mouvement commence').toBe(true);
    expect(
      Math.abs(auRetour.ph - auRetour.ph0),
      'à Retour, la phrase est encore à la place de saisie',
    ).toBeLessThanOrEqual(1);
    expect(auRetour.deja, 'C-303 : à Retour, la copie de « DÉJÀ PROMIS » est là, elle descend (jamais d’un coup)').toBe(
      true,
    );
    // les images et la durée : sur le Mac seulement (hors du Mac une image dure 0,7 s)
    if (process.platform === 'darwin') {
      const fin = R.m.at(-1)!;
      const p0 = R.m[0]!.ph;
      const j0 = R.m.findIndex((m) => Math.abs(m.ph - p0) > 0.5);
      expect(j0, 'la phrase quitte la place de saisie').toBeGreaterThanOrEqual(0);
      expect(
        Math.abs(R.m[j0]!.ph - fin.ph),
        'la première image n’est pas la place finale (jamais d’un coup)',
      ).toBeGreaterThan(Math.abs(fin.ph - p0) * 0.3);
      const jFin = R.m.findIndex((m, k) => k > j0 && Math.abs(m.ph - fin.ph) < 0.5);
      const duree = R.m[jFin]!.t - Math.max(t0, R.m[Math.max(0, j0 - 1)]!.t);
      expect(duree, 'la durée (360 ms ; décidé 300 à 400)').toBeLessThanOrEqual(460);
      expect(duree, 'la durée (360 ms ; décidé 300 à 400)').toBeGreaterThanOrEqual(250);
    }
    // image par image : sur le Mac (hors du Mac le mouvement entier tient dans une image de 0,7 s — tout y « part d'un coup »)
    if (process.platform === 'darwin')
      expect(R.partis, 'rien de ce qui peint ne part d’un coup (redteam_je)').toEqual([]);
    expect(
      await page.evaluate(
        () =>
          [
            ...document.querySelectorAll<HTMLElement>(
              '#createSheet .pp-phrase, #createSheet .ph-photo-btn, #csBotBar, #csPinceau, .pp-garder',
            ),
          ]
            .map((e) => e.style.translate)
            .filter(Boolean).length + document.querySelectorAll('#createSheet .ppo-copie').length,
      ),
      'à la fin : aucune transformation restée, aucune copie',
    ).toBe(0);
  });

// ── la saisie : la place remplie est crème à l'encre, « d’ » colle à elle, le curseur clignote après ce qu'on tape (lot-CURSEUR) ──
test('la saisie d’un titre : la place remplie crème, à l’encre, sans contour ; le curseur de 3 pt, 0,82 em, clignote après la frappe (lot-CURSEUR)', async ({
  page,
}) => {
  await ouvrir(page, 'chiche');
  // la sonde : la place remplie garde son pointillé (le défaut d'avant)
  if (sonde('place-pointillee'))
    await page.addStyleTag({
      content:
        '#createSheet .ph-txt .ph-m:not(.ph-vide){border:3px dashed currentColor!important;background:transparent!important}',
    });
  await doigt(page, '#createSheet .ph-m[data-ph="titre"]');
  await page.keyboard.type('appeler Lou');
  await posee(page);
  const r = await page.evaluate(() => {
    const m = document.querySelector<HTMLElement>('#createSheet .ph-m[data-ph="titre"]')!;
    const s = getComputedStyle(m);
    const c = m.querySelector('.ph-caret')!;
    const cs = getComputedStyle(c);
    const li = m.previousElementSibling!;
    return {
      fond: s.backgroundColor,
      encre: s.color,
      bord: s.borderTopStyle,
      caret: [
        cs.width,
        (parseFloat(cs.height) / parseFloat(s.fontSize)).toFixed(2),
        cs.animationName,
        cs.animationDuration,
      ],
      dernier: m.lastElementChild === c,
      li: getComputedStyle(li).marginRight,
    };
  });
  expect([r.fond, r.encre, r.bord], 'remplie : crème #F7F0DE, encre #050302, sans contour').toEqual([
    'rgb(247, 240, 222)',
    'rgb(5, 3, 2)',
    'none',
  ]);
  expect(r.caret, 'le curseur : 3 pt, 0,82 em, clignote (1,06 s)').toEqual(['3px', '0.82', 'phCaret', '1.06s']);
  expect(r.dernier, 'le curseur après ce qu’on tape').toBe(true);
  expect(r.li, '« d’ » colle à sa place (`em.ph-li.ph-elide{margin-right:0}`)').toBe('0px');
});

// ── redteam_ajout_personne (C-122, v146) — la zone en pointillés EST le champ ; le « + » orange #FB4C0D, à la hauteur des capitales du nom,
//    paraît dès la première lettre et valide (Retour aussi) ; un nom connu garde son écriture ; la zone se propose pour le suivant ; rien ne
//    passe sous le clavier (14 pt d'air ; 8 exigés — clavier simulé : 336 pt, celui d'un iPhone) ──
test('ajouter une personne : la zone en pointillés est le champ, le « + » orange valide, Retour aussi ; la ligne reste au-dessus du clavier (redteam_ajout_personne, C-122)', async ({
  page,
}) => {
  await ouvrir(page, 'chiche');
  // la sonde : le « + » ne prend plus le doigt
  if (sonde('plus-sourd')) await page.addStyleTag({ content: '#createSheet .gn-plus{pointer-events:none!important}' });
  await doigt(page, '#createSheet .ph-m[data-ph="qui"]');
  await posee(page);
  await doigt(page, '#createSheet .gn .ph-add');
  const z0 = await page.evaluate(() => {
    const z = document.querySelector('#createSheet .gn .ph-add')!;
    return {
      edit: z.classList.contains('gn-edit'),
      focus: document.activeElement?.id,
      attente: z.querySelector('.gn-ph')?.textContent,
      bord: getComputedStyle(z).borderTopStyle,
      encarts: document.querySelectorAll('#createSheet .gn .gn-barre, #createSheet .gn input:not(.gn-saisie)').length,
    };
  });
  expect(z0, 'la zone même s’écrit (aucun second encart), le clavier ouvert, « un prénom… »').toEqual({
    edit: true,
    focus: 'gnSaisie',
    attente: 'un prénom…',
    bord: 'dashed',
    encarts: 0,
  });
  await page.keyboard.type('maman');
  await page.waitForTimeout(300);
  const p = await page.evaluate(() => {
    const pl = document.querySelector('#createSheet .gn-plus')!;
    const sv = pl.querySelector('svg')!;
    const t = document.querySelector('#createSheet .gn-txt')!;
    const g = document.createElement('canvas').getContext('2d')!;
    const s = getComputedStyle(t);
    g.font = `${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
    const cap = g.measureText('H').actualBoundingBoxAscent;
    const a = pl.getBoundingClientRect();
    const b = t.getBoundingClientRect();
    return {
      couleur: getComputedStyle(sv.querySelector('path')!).stroke,
      haut: parseFloat(sv.getAttribute('height')!),
      cap,
      ligne: Math.abs(a.top + a.height / 2 - (b.top + b.height / 2)) < b.height,
      droite: a.left > b.right,
    };
  });
  expect(p.couleur, 'le « + » à l’orange du départ d’une action #FB4C0D').toBe('rgb(251, 76, 13)');
  expect(Math.abs(p.haut - p.cap), 'à la hauteur des capitales du nom (± 1 pt)').toBeLessThanOrEqual(1);
  expect([p.ligne, p.droite], 'à droite du nom, sur sa ligne').toEqual([true, true]);
  // (un vrai toucher, qui passe par le test du point : le « + » doit prendre le doigt)
  const pp = await page.evaluate(() => {
    const b = document.querySelector('#createSheet .gn-plus')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  });
  await page.mouse.click(pp[0]!, pp[1]!);
  await page.waitForTimeout(150);
  let e = await etat(page);
  expect(e.phrase.qui, 'le « + » valide ; un nom connu garde son écriture (« maman » → « Maman »)').toEqual([
    'Moi',
    'Maman',
  ]);
  expect(
    await page.evaluate(() => [
      document.activeElement?.id,
      document.querySelector('#createSheet .gn .ph-add')!.classList.contains('gn-edit'),
    ]),
    'la zone se propose pour le suivant, le clavier reste',
  ).toEqual(['gnSaisie', true]);
  await page.keyboard.type('Zoé');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(200);
  e = await etat(page);
  expect(e.phrase.qui, 'Retour valide aussi').toEqual(['Moi', 'Maman', 'Zoé']);
  // le clavier (simulé : la fenêtre visible réduite de 336 pt, ce que l'app lit) : la ligne reste 14 pt au-dessus de lui (8 exigés) — lue
  // la page posée (la page glisse en 300 ms ; hors du Mac une image dure 0,7 s : on attend sa place, 5 s au plus)
  await posee(page);
  await page.evaluate(() => {
    const vv = window.visualViewport!;
    const h = window.innerHeight - 336;
    Object.defineProperty(vv, 'height', { get: () => h, configurable: true });
    vv.dispatchEvent(new Event('resize'));
  });
  await page
    .waitForFunction(
      () =>
        window.innerHeight - 336 - document.querySelector('#createSheet .gn .ph-add')!.getBoundingClientRect().bottom >=
        8,
      undefined,
      { timeout: 5000 },
    )
    .catch(() => undefined);
  await posee(page);
  const air = await page.evaluate(
    () => window.innerHeight - 336 - document.querySelector('#createSheet .gn .ph-add')!.getBoundingClientRect().bottom,
  );
  expect(air, 'la ligne au-dessus du clavier (8 pt au moins)').toBeGreaterThanOrEqual(8);
});

// ── redteam_peaufiner (C-134), redteam_peauf_x (C-220) — la barre ouvre Peaufiner (ses rangées, nature par nature, en dur) ; un choix s'y fait
//    sur place et il reste ouvert ; un glissement de 60 pt ne le referme pas, un de 220 le referme ; son X le referme ; refermé, rien de lui ne
//    reste à l'écran et la page est celle d'avant ; il paraît et part en flaques (C-271) ; les murs de Ma Parole ! sont flous (4,8 px) ──
const RANGEES: Record<Nat, string[]> = {
  promi: [
    'AVANT',
    'DANS UN CERCLE',
    'NOTE',
    'PIÈCES JOINTES',
    'RÉCURRENCE',
    'RAPPEL',
    "C'EST IMPORTANT ?",
    'LA MÉMOIRE',
    'LA COULEUR',
  ],
  chiche: ['AVANT', 'NOTE', 'PIÈCES JOINTES', 'RÉCURRENCE', 'RAPPEL', "C'EST IMPORTANT ?", 'LA MÉMOIRE', 'LA COULEUR'],
  nuee: ['MEMBRES', 'RÉCURRENCE', 'RAPPEL', "C'EST IMPORTANT ?", 'LA MÉMOIRE', 'LA COULEUR'],
};
const PEAUF: Record<Nat, string> = {
  promi:
    'Peaufiner, promi : la barre l’ouvre, il reste ouvert, un glissement de 220 pt ou son X le referment, il n’en reste rien (redteam_peaufiner, redteam_peauf_x)',
  chiche:
    'Peaufiner, chiche : la barre l’ouvre, il reste ouvert, un glissement de 220 pt ou son X le referment, il n’en reste rien (redteam_peaufiner, redteam_peauf_x)',
  nuee: 'Peaufiner, nuee : la barre l’ouvre, il reste ouvert, un glissement de 220 pt ou son X le referment, il n’en reste rien (redteam_peaufiner, redteam_peauf_x)',
};
for (const nat of ['promi', 'chiche', 'nuee'] as const)
  test(PEAUF[nat], async ({ page }) => {
    await ouvrir(page, nat);
    // la sonde : refermé, le tiroir reste affiché (C-220 : la règle « fermée » battue par une autre)
    if (sonde('peauf-reste')) {
      await page.addStyleTag({ content: '#csPeauf[hidden]{display:block!important}' });
      await page.evaluate(() => {
        const p = document.getElementById('csPeauf')!;
        const rc = p.replaceChildren.bind(p);
        p.replaceChildren = (...a: Array<Node | string>) => {
          if (a.length) rc(...a);
        };
      });
    }
    const textes = (): Promise<Record<string, number>> =>
      page.evaluate(() => {
        const o: Record<string, number> = {};
        const c = document.getElementById('createSheet')!;
        const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT);
        let n: Node | null;
        while ((n = w.nextNode())) {
          const t = (n.textContent ?? '').trim();
          if (!t || n.parentElement!.closest('#csPeauf')) continue;
          const s = getComputedStyle(n.parentElement!);
          if (s.visibility !== 'visible' || n.parentElement!.closest('[hidden]')) continue;
          const R = document.createRange();
          R.selectNodeContents(n);
          const r = R.getBoundingClientRect();
          if (r.width >= 1) o[t] = Math.round(r.top * 2) / 2;
        }
        return o;
      });
    const tiroir = (): Promise<string[]> =>
      page.evaluate(() => {
        const o: string[] = [];
        const c = document.getElementById('csPeauf')!;
        const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT);
        let n: Node | null;
        while ((n = w.nextNode())) {
          const t = (n.textContent ?? '').trim();
          if (!t) continue;
          const R = document.createRange();
          R.selectNodeContents(n);
          const r = R.getBoundingClientRect();
          if (r.width >= 1 && getComputedStyle(n.parentElement!).visibility === 'visible') o.push(t);
        }
        return o;
      });
    const av = await textes();
    // l'ouverture : en flaques
    await page.evaluate(() => {
      const w = window as unknown as { __fl: string[] };
      w.__fl = [];
      const o = new MutationObserver(() => {
        const p = document.getElementById('csPeauf')!;
        if (p.dataset['flaquesMode']) w.__fl.push(p.dataset['flaquesMode']);
      });
      o.observe(document.getElementById('csPeauf')!, { attributes: true, attributeFilter: ['data-flaques-mode'] });
    });
    await doigt(page, '#csBotBar');
    await posee(page);
    const labs = await page.evaluate(() =>
      [...document.querySelectorAll('#csPeauf .s2-lab')].map((e) => e.textContent),
    );
    expect(labs, 'ses rangées, telles que le prototype les montre').toEqual(RANGEES[nat]);
    expect(
      await page.evaluate(() => [
        document.querySelector('#csPeauf .s2-titre')!.textContent,
        document.querySelector('#csBotBar .cbb-chev')!.textContent,
      ]),
    ).toEqual([{ promi: 'Promi', chiche: 'Chiche', nuee: 'Cercle' }[nat], '▴']);
    expect(
      await page.evaluate(() =>
        [...document.querySelectorAll('#csPeauf .s2-cercle .s2-reg')].map((e) => getComputedStyle(e).filter),
      ),
      'les réglages de Ma Parole ! sont des murs, flous de 4,8 px (leur phrase : lot 8)',
    ).toEqual(Array(5).fill('blur(4.8px)'));
    if (nat !== 'nuee') {
      // un choix sur place : la note s'écrit, Peaufiner reste ouvert, la page a changé (« garder de côté » actif)
      await doigt(page, '#fNote');
      await page.locator('#fNote').fill('un mot');
      await page.waitForTimeout(200);
      const e = await etat(page);
      expect(
        [(e.phrase as unknown as { note: string }).note, e.gardeActif],
        'la note s’écrit, la page a changé',
      ).toEqual(['un mot', true]);
      await page.locator('#fNote').blur();
    }
    expect((await etat(page)) as unknown as { peauf: boolean }, 'Peaufiner reste ouvert').toMatchObject({
      peauf: true,
    });
    // un glissement de 60 pt ne referme rien ; un de 220 referme
    const glisse = async (d: number): Promise<void> => {
      await page.mouse.move(195, 300);
      await page.mouse.down();
      for (let k = 1; k <= 10; k++) await page.mouse.move(195, 300 + (d * k) / 10);
      await page.mouse.up();
      await page.waitForTimeout(150);
    };
    await glisse(60);
    expect(((await etat(page)) as unknown as { peauf: boolean }).peauf, '60 pt : il reste ouvert').toBe(true);
    await glisse(220);
    await posee(page);
    expect(((await etat(page)) as unknown as { peauf: boolean }).peauf, '220 pt : il se referme').toBe(false);
    expect(await tiroir(), 'C-220 : refermé, aucun texte du tiroir à l’écran').toEqual([]);
    const ap = await textes();
    for (const [t, y] of Object.entries(av)) expect(ap[t] ?? NaN, `« ${t} » à sa place d’avant`).toBeCloseTo(y, 0);
    // rouvert par la barre, refermé par son X
    await doigt(page, '#csBotBar');
    await posee(page);
    expect((await tiroir()).length, 'rouvert : ses rangées reviennent').toBeGreaterThanOrEqual(6);
    await doigt(page, '#csPeauf .s2-fermer');
    await posee(page);
    expect(((await etat(page)) as unknown as { peauf: boolean }).peauf, 'son X le referme').toBe(false);
    expect(await tiroir()).toEqual([]);
    expect(
      await page.evaluate(() => (window as unknown as { __fl: string[] }).__fl),
      'C-271 : il paraît et part en flaques',
    ).toEqual(expect.arrayContaining(['ouvre', 'couvre']));
  });

// ── PEAUFINER, SES CHOIX (lot-S2, C-197 ; le prototype : `.s2-reg.s2-ouv`, `#dueChips`, `#nueeChips`, `buildCreateNuees`) — une rangée se déplie
//    au toucher (ses choix dessous, la rangée grandit, rayon 30), un choix la replie et s'écrit dans sa valeur ; aucune pastille cochée tant
//    qu'on n'a rien choisi ; « une date… » ouvre le calendrier ; un Cercle choisi : « Je promets … à tout le monde », l'exemple au pluriel, la
//    pastille porte son visage, la barre prend l'écriture d'un Cercle, « aucune » rend « Je me promets » ; les pièces jointes s'ajoutent ;
//    planter emporte l'échéance et le Cercle ; un Cercle : un membre coché reste coché, sa rangée ouverte ──
test('Peaufiner, ses choix : l’échéance, le Cercle (la phrase à tout le monde), les pièces jointes, les membres ; planter les emporte', async ({
  page,
}) => {
  test.setTimeout(150000);
  const ls = stockage();
  const st = JSON.parse(ls['promi_state']!) as Record<string, unknown>;
  st['NUE'] = { n1: 'Marseille' };
  ls['promi_state'] = JSON.stringify(st);
  await ouvrir(page, 'promi', ls);
  // les sondes : les pastilles ne prennent plus le doigt ; planter perd l'échéance et le Cercle
  if (sonde('peauf-choix-sourd')) await page.addStyleTag({ content: '#csPeauf .chip{pointer-events:none!important}' });
  if (sonde('peauf-choix-perdus'))
    await page.evaluate(
      `(() => { const m = ${P_}.magasin; const f = m.planter.bind(m); m.planter = (p, t) => f({ ...p, due: null, dueISO: null, cercle: null }, t); })()`,
    );
  const ph = (): Promise<{
    due: number | null;
    dueISO: string | null;
    cercle: string | null;
    sens: string;
    qui: string[];
    fichiers: string[];
  }> => page.evaluate(`${P_}.pagePlus().etat().phrase`) as never;
  const toucheRangee = async (lab: string): Promise<void> => {
    await page.evaluate((lab) => {
      const r = [...document.querySelectorAll<HTMLElement>('#csPeauf .s2-reg')].find(
        (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === lab,
      )!;
      const b = r.getBoundingClientRect();
      const o = { bubbles: true, clientX: b.left + 30, clientY: b.top + 20, pointerId: 32 };
      const e = document.elementFromPoint(o.clientX, o.clientY)!;
      e.dispatchEvent(new PointerEvent('pointerdown', o));
      e.dispatchEvent(new PointerEvent('pointerup', o));
      e.dispatchEvent(new MouseEvent('click', o));
    }, lab);
    await page.waitForTimeout(250);
  };
  const lit = (
    lab: string,
  ): Promise<{ ouv: boolean; val: string; chips: string[]; on: string[]; h: number; rayon: string }> =>
    page.evaluate((lab) => {
      const r = [...document.querySelectorAll<HTMLElement>('#csPeauf .s2-reg')].find(
        (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === lab,
      )!;
      const ch = [...r.querySelectorAll('.chip')];
      return {
        ouv: r.classList.contains('s2-ouv'),
        val: (r.querySelector('.s2-val')?.textContent ?? '').trim(),
        chips: ch.map((c) => (c.textContent ?? '').trim()),
        on: ch.filter((c) => c.classList.contains('on')).map((c) => (c.textContent ?? '').trim()),
        h: r.getBoundingClientRect().height / (r.getBoundingClientRect().width / r.offsetWidth),
        rayon: getComputedStyle(r).borderTopLeftRadius,
      };
    }, lab);
  const pastilleDe = async (lab: string, mot: string): Promise<void> => {
    const xy = await page.evaluate(
      ([lab, mot]) => {
        const r = [...document.querySelectorAll<HTMLElement>('#csPeauf .s2-reg')].find(
          (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === lab,
        )!;
        const c = [...r.querySelectorAll<HTMLElement>('.chip')].find((x) => (x.textContent ?? '').trim() === mot)!;
        const b = c.getBoundingClientRect();
        return [b.left + b.width / 2, b.top + b.height / 2];
      },
      [lab, mot] as const,
    );
    await page.mouse.click(xy[0]!, xy[1]!);
    await page.waitForTimeout(300);
  };
  await doigt(page, '#csBotBar');
  await posee(page);
  // 1 · AVANT : se déplie, ses cinq choix dessous, aucun coché (« un jour » est le défaut, pas un choix)
  await toucheRangee('AVANT');
  let a = await lit('AVANT');
  expect([a.ouv, a.chips, a.on, a.rayon], 'dépliée : ses choix, aucun coché, rayon 30').toEqual([
    true,
    ['demain', '1 sem.', '1 mois', 'une date…', 'un jour'],
    [],
    '30px',
  ]);
  expect(a.h, 'la rangée grandit : 18 + 12 + 19,8 + 14 + deux rangées de pastilles (33, 8) + 18').toBeCloseTo(159.8, 0);
  await pastilleDe('AVANT', '1 sem.');
  a = await lit('AVANT');
  expect([a.ouv, a.val, (await ph()).due], 'un choix la replie et s’écrit').toEqual([false, '1 sem.', 7]);
  expect((await etat(page)).gardeActif, 'la page a changé').toBe(true);
  await toucheRangee('AVANT');
  expect((await lit('AVANT')).on, 'rouverte : son choix coché').toEqual(['1 sem.']);
  // « une date… » : le calendrier (une date dans 10 jours) — la valeur dit le jour
  const iso = await page.evaluate(() => {
    const d = new Date();
    d.setDate(d.getDate() + 10);
    return `${String(d.getFullYear())}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  });
  await page.evaluate((iso) => {
    const i = document.querySelector<HTMLInputElement>('#dueChips .due-datein')!;
    i.value = iso;
    i.dispatchEvent(new Event('change', { bubbles: true }));
  }, iso);
  await page.waitForTimeout(300);
  a = await lit('AVANT');
  expect([(await ph()).due, (await ph()).dueISO], 'une date : dans 10 jours').toEqual([10, iso]);
  expect(a.val, 'la valeur dit le jour (« lundi 12 »)').toMatch(
    /^(dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi) \d+$/,
  );
  // 2 · DANS UN CERCLE : « aucune » coché, puis Marseille — la phrase passe à « Je promets … à tout le monde »
  await toucheRangee('DANS UN CERCLE');
  const c = await lit('DANS UN CERCLE');
  expect([c.chips, c.on], 'aucune, puis les Cercles').toEqual([['aucune', 'Marseille'], ['aucune']]);
  await pastilleDe('DANS UN CERCLE', 'Marseille');
  const p1 = await ph();
  expect([p1.cercle, p1.sens, p1.qui], 'le Cercle choisi : à tout le monde').toEqual([
    'n1',
    'faire',
    ['tout le monde'],
  ]);
  expect((await lit('DANS UN CERCLE')).val).toBe('Marseille');
  await doigt(page, '#csPeauf .s2-fermer');
  await posee(page);
  const l1 = await lignes(page);
  expect(l1[0], 'le verbe').toBe('Je promets');
  expect(l1[l1.length - 1], 'à tout le monde').toBe('à tout le monde');
  expect(
    await page.evaluate(() => ({
      ex: document.querySelector('#createSheet .ph-m[data-ph="titre"]')!.getAttribute('data-plein'),
      vis: !!document.querySelector('#createSheet .ph-m[data-ph="qui"] .pp-visage'),
      barre: getComputedStyle(document.querySelector('#csBotBar .cbb-lab')!).color,
    })),
    'l’exemple au pluriel, le visage dans la pastille, la barre à l’écriture d’un Cercle',
  ).toEqual({ ex: expect.stringMatching(/^vous /) as unknown as string, vis: true, barre: 'rgb(243, 231, 209)' }); // --c-creme95-2, #F3E7D1 (le prototype)
  // 3 · PIÈCES JOINTES : le sélecteur de fichiers dans le geste ; deux fichiers
  await doigt(page, '#csBotBar');
  await posee(page);
  const pj = await page.evaluate(() => {
    const r = [...document.querySelectorAll<HTMLElement>('#csPeauf .s2-reg')].find(
      (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === 'PIÈCES JOINTES',
    )!;
    const b = r.getBoundingClientRect();
    return [b.left + 40, b.top + 30];
  });
  const [chooser] = await Promise.all([
    page.waitForEvent('filechooser', { timeout: 5000 }),
    page.mouse.click(pj[0]!, pj[1]!),
  ]);
  await chooser.setFiles([
    { name: 'billet.pdf', mimeType: 'application/pdf', buffer: Buffer.from('a') },
    { name: 'plan.png', mimeType: 'image/png', buffer: Buffer.from('b') },
  ]);
  await page.waitForTimeout(300);
  expect([(await ph()).fichiers, (await lit('PIÈCES JOINTES')).val]).toEqual([
    ['billet.pdf', 'plan.png'],
    '2 fichiers',
  ]);
  // « aucune » rend « Je me promets »
  await toucheRangee('DANS UN CERCLE');
  await pastilleDe('DANS UN CERCLE', 'aucune');
  expect([(await ph()).cercle, (await ph()).sens, (await ph()).qui]).toEqual([null, 'soi', []]);
  await toucheRangee('DANS UN CERCLE');
  await pastilleDe('DANS UN CERCLE', 'Marseille');
  await doigt(page, '#csPeauf .s2-fermer');
  await posee(page);
  // 4 · planter emporte l'échéance, le Cercle et les pièces jointes (la parole écrite au milieu du trait, C-237)
  await doigt(page, '#createSheet .ph-m[data-ph="titre"]');
  await posee(page);
  await page.keyboard.type('appeler Lou');
  await page.keyboard.press('Enter');
  await page.waitForFunction(`${P_}.pagePlus().etat().invite.visible`, undefined, { timeout: 30000 });
  await page.waitForFunction(() => !document.querySelector('#createSheet canvas.passage-flaques'), undefined, {
    timeout: 20000,
  });
  const [x0, y0, k] =
    (await page.evaluate(`(() => { const cs = document.getElementById('createSheet'); const C = cs.getBoundingClientRect();
      const k = C.width / cs.offsetWidth; const h = parseFloat(getComputedStyle(cs).getPropertyValue('--pp-h')) || 0;
      const [x, y] = document.getElementById('csTrameCv').getAttribute('data-depart').split(',').map(Number); return [C.left + x * k, C.top + (y + h) * k, k]; })()`)) as [
      number,
      number,
      number,
    ];
  await page.mouse.move(x0, y0);
  await page.mouse.down();
  for (let x = x0; x <= 200 * k; x += 8 * k) await page.mouse.move(x, y0);
  await page.mouse.up();
  const pa = (await page.evaluate(
    `(() => { const L = ${P_}.magasin.etat().paroles; const p = L[L.length - 1]; return { t: p.title, due: p.due, iso: p.suite?.dueISO ?? null, nuee: p.nuee ?? null, files: p.suite?.files ?? [] }; })()`,
  )) as { t: string; due: number | null; iso: string | null; nuee: string | null; files: string[] };
  expect(pa, 'la parole porte son échéance, son Cercle, ses pièces jointes').toEqual({
    t: 'appeler Lou',
    due: 10,
    iso,
    nuee: 'n1',
    files: ['billet.pdf', 'plan.png'],
  });
});

test('Peaufiner d’un Cercle : MEMBRES se déplie, un membre coché reste coché et sa rangée ouverte, décoché il part', async ({
  page,
}) => {
  await ouvrir(page, 'nuee');
  if (sonde('peauf-membres-sourds'))
    await page.addStyleTag({ content: '#csPeauf .s2-reg .gn-liste{pointer-events:none!important}' });
  await doigt(page, '#csBotBar');
  await posee(page);
  const membres = async (): Promise<{ ouv: boolean; val: string; on: string[] }> =>
    page.evaluate(() => {
      const r = [...document.querySelectorAll<HTMLElement>('#csPeauf .s2-reg')].find(
        (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === 'MEMBRES',
      )!;
      return {
        ouv: r.classList.contains('s2-ouv'),
        val: (r.querySelector('.s2-val')?.textContent ?? '').trim(),
        on: [...r.querySelectorAll('.ph-o.on')].map((b) => (b.textContent ?? '').trim()),
      };
    });
  const touche = async (sel: string, mot: string): Promise<void> => {
    const xy = await page.evaluate(
      ([sel, mot]) => {
        const e = [...document.querySelectorAll<HTMLElement>(sel)].find((x) =>
          (x.textContent ?? '').trim().startsWith(mot),
        )!;
        const b = e.getBoundingClientRect();
        return [b.left + 30, b.top + Math.min(20, b.height / 2)];
      },
      [sel, mot] as const,
    );
    await page.mouse.click(xy[0]!, xy[1]!);
    await page.waitForTimeout(300);
  };
  await touche('#csPeauf .s2-reg', 'MEMBRES');
  expect((await membres()).ouv, 'dépliée').toBe(true);
  await touche('#csPeauf .s2-reg .ph-o', 'M');
  const m1 = await membres();
  expect([m1.ouv, m1.on.length, m1.val.length > 0], 'un membre coché : la rangée reste ouverte').toEqual([
    true,
    1,
    true,
  ]);
  const nom = m1.on[0]!.replace(/^.\s*/, '');
  expect(((await etat(page)).phrase as unknown as { membres: string[] }).membres, 'il est membre').toContain(
    nom.replace(/×$/, '').trim(),
  );
  await touche('#csPeauf .s2-reg .ph-o.on', m1.on[0]!.charAt(0));
  expect((await membres()).on, 'décoché : il part').toEqual([]);
});

// ── redteam_photo_menu (v117, v132 : la page +) — le bouton photo ouvre le menu (« Dessiner » en tête ; « Importer une photo » sauf sur un
//    Cercle, C-199), en flaques ; « Importer une photo » ouvre le sélecteur de fichiers DANS le geste ; la photo remplace la dalle ; « Retirer
//    la photo » la retire ; un toucher ailleurs referme le menu ──
const PNG_ROUGE =
  'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAAEklEQVR4nGP4z8CAFWEXHbQSACj/P8Fu7N9hAAAAAElFTkSuQmCC';
test('le menu du bouton photo : « Dessiner », « Importer une photo » (le sélecteur dans le geste), la photo remplace la dalle, « Retirer la photo » ; un Cercle : « Dessiner » seul (redteam_photo_menu)', async ({
  page,
}) => {
  await ouvrir(page, 'promi');
  // la sonde : le bouton photo ne prend plus le doigt
  if (sonde('photo-sourd'))
    await page.addStyleTag({ content: '#createSheet .ph-photo-btn{pointer-events:none!important}' });
  const menu = (): Promise<string[]> =>
    page.evaluate(() =>
      [...document.querySelectorAll('#createSheet .ph-photo-menu button')].map((b) => b.textContent!),
    );
  await toucher(page, '#createSheet .ph-photo-btn');
  expect(await menu(), 'le menu (v132 : « Dessiner » en tête)').toEqual(['Dessiner', 'Importer une photo']);
  expect(
    await page.evaluate(
      () => getComputedStyle(document.querySelector('#createSheet .ph-photo-menu button')!).textTransform,
    ),
  ).toBe('uppercase');
  await posee(page);
  // un toucher ailleurs le referme
  // (au-dessus du menu : sa boîte, comme dans le prototype, prend le doigt sur toute sa largeur)
  await page.mouse.click(60, 130);
  await posee(page);
  expect(await menu(), 'un toucher ailleurs le referme').toEqual([]);
  await toucher(page, '#createSheet .ph-photo-btn');
  await posee(page);
  const [chooser] = await Promise.all([
    page.waitForEvent('filechooser', { timeout: 5000 }),
    toucher(page, '#createSheet .ph-photo-menu button:nth-child(2)'),
  ]);
  await chooser.setFiles({ name: 'photo.png', mimeType: 'image/png', buffer: Buffer.from(PNG_ROUGE, 'base64') });
  await page.waitForFunction(`!!${P_}.pagePlus().etat().phrase.photo`, undefined, { timeout: 5000 });
  await posee(page);
  const rouge = (): Promise<number> =>
    page.evaluate(() => {
      const c = document.getElementById('csPhotoCv') as HTMLCanvasElement;
      const d = c.getContext('2d')!.getImageData(0, 0, c.width, c.height).data;
      let n = 0;
      for (let i = 0; i < d.length; i += 4) if (d[i]! > 200 && d[i + 1]! < 60 && d[i + 3]! > 200) n++;
      return n;
    });
  expect(await rouge(), 'la photo est posée dans la bande (sa couche)').toBeGreaterThan(1000);
  expect((await etat(page)).gardeActif, 'la page a changé').toBe(true);
  await toucher(page, '#createSheet .ph-photo-btn');
  await posee(page);
  expect(await menu()).toEqual(['Dessiner', 'Importer une photo', 'Retirer la photo']);
  await toucher(page, '#createSheet .ph-photo-menu button:nth-child(3)');
  await posee(page);
  expect(await rouge(), '« Retirer la photo » la retire').toBe(0);
  await page.evaluate(`${P_}.pagePlus().ouvrir('nuee')`);
  await page.waitForFunction(() => !document.getElementById('createSheet')!.classList.contains('pp-entre'));
  await toucher(page, '#createSheet .ph-photo-btn');
  expect(await menu(), 'un Cercle ne porte pas de photo (C-199)').toEqual(['Dessiner']);
});

// ── A3 (CLAUDE.md, porte de qualité : « toute mesure de mise en page à l'échelle 1 ET à l'échelle 0,79 ») — la vraie app s'adapte à l'écran
//    (L0 §2) : dans la fenêtre de Safari à 0,79 (330 × 714), la page + dans chacun de ses états. Trouvé en le jugeant (lot 2a) : le choix
//    d'un Cercle sortait de l'écran (deux colonnes de 162 fixes), ses noms coupés net, le X de Peaufiner hors de l'écran (posé à 304 pt). ──
const ETATS_A3: Array<{ nat: Nat; etat: string }> = [
  { nat: 'promi', etat: 'repos' },
  { nat: 'chiche', etat: 'choix' },
  { nat: 'nuee', etat: 'choix' },
  { nat: 'chiche', etat: 'prenom' },
  { nat: 'promi', etat: 'saisie' },
  { nat: 'nuee', etat: 'saisie' },
  { nat: 'promi', etat: 'peauf' },
  { nat: 'nuee', etat: 'peauf' },
  { nat: 'promi', etat: 'photo' },
];
test('A3, à 0,79 (330 × 714) : la page + dans chacun de ses états — rien ne sort de l’écran, aucun nom coupé net, le X de Peaufiner atteignable', async ({
  page,
}) => {
  const fautes: string[] = [];
  for (const { nat, etat } of ETATS_A3) {
    await page.setViewportSize({ width: 330, height: 714 });
    await vraieApp(page, stockage());
    await ouvrirPagePlus(page, nat);
    // la sonde : le choix d'un Cercle à ses deux colonnes de 162 fixes (le défaut trouvé)
    if (sonde('a3-fixe'))
      await page.addStyleTag({
        content:
          '#createSheet.pp-nuee .gn{width:336px!important}#createSheet .gn-liste{grid-template-columns:162px 162px!important}#createSheet .ph-o:not(.ph-add){width:162px!important}',
      });
    const titre = nat === 'nuee' ? '#createSheet .ph-m[data-np="nom"]' : '#createSheet .ph-m[data-ph="titre"]';
    const place = nat === 'nuee' ? '#createSheet .ph-m[data-np="avec"]' : '#createSheet .ph-m[data-ph="qui"]';
    if (etat === 'choix' || etat === 'prenom') await toucher(page, place);
    if (etat === 'prenom') {
      await toucher(page, '#createSheet .ph-add');
      await page.keyboard.type('Bruno-Stanislas');
      await posee(page);
    }
    if (etat === 'saisie') {
      await toucher(page, titre);
      await page.keyboard.type('appeler Lou au sujet des vacances de printemps');
      await posee(page);
    }
    if (etat === 'peauf') await toucher(page, '#csBotBar');
    if (etat === 'photo') await toucher(page, '#createSheet .ph-photo-btn');
    await page.waitForTimeout(400);
    const r = (await page.evaluate(() => {
      const W = innerWidth;
      const out: string[] = [];
      const vis = (e: Element): boolean => {
        for (let x: Element | null = e; x; x = x.parentElement) {
          const s = getComputedStyle(x);
          if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity < 0.05) return false;
        }
        return true;
      };
      const cs = document.getElementById('createSheet')!;
      // D : un texte visible qui sort de l'écran (une valeur qui s'arrête par « … » est rognée par sa boîte : on lit la boîte qui rogne ;
      // le rail du pinceau défile et le déclare, data-glisse)
      const w = document.createTreeWalker(cs, NodeFilter.SHOW_TEXT);
      let t: Node | null;
      while ((t = w.nextNode())) {
        const e = t.parentElement!;
        if (!(t.nodeValue ?? '').trim() || !vis(e) || e.closest('[data-glisse]')) continue;
        const rg = document.createRange();
        rg.selectNodeContents(t);
        let q = rg.getBoundingClientRect();
        if (!q.width) continue;
        for (let x: Element | null = e; x && x !== cs; x = x.parentElement)
          if (getComputedStyle(x).overflowX !== 'visible') {
            const b = x.getBoundingClientRect();
            q = new DOMRect(
              Math.max(q.left, b.left),
              q.top,
              Math.min(q.right, b.right) - Math.max(q.left, b.left),
              q.height,
            );
            break;
          }
        if (q.left < -1 || q.right > W + 1)
          out.push(
            `sort de l’écran : « ${(t.nodeValue ?? '').trim().slice(0, 30)} » ${String(Math.round(q.left))} → ${String(Math.round(q.right))}`,
          );
      }
      // une boîte qui se touche (une personne, « + ajouter », une rangée de Peaufiner) entière à l'écran
      for (const b of cs.querySelectorAll('.ph-o, .s2-reg, .s2-fermer, .ph-photo-menu > *')) {
        if (!vis(b)) continue;
        const q = b.getBoundingClientRect();
        if (q.width && (q.left < -1 || q.right > W + 1))
          out.push(
            `hors de l’écran : ${b.className || b.tagName} ${String(Math.round(q.left))} → ${String(Math.round(q.right))}`,
          );
      }
      // un nom coupé net (sans « … »)
      for (const n of cs.querySelectorAll<HTMLElement>('.ppo-nom'))
        if (vis(n) && n.scrollWidth > n.clientWidth + 1 && getComputedStyle(n).textOverflow !== 'ellipsis')
          out.push(`nom coupé net : « ${n.textContent ?? ''} »`);
      return out;
    })) as string[];
    for (const f of r) fautes.push(`${nat}, ${etat} : ${f}`);
  }
  expect(fautes).toEqual([]);
});
