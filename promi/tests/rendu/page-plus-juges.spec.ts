/**
 * LOT 2a — LES JUGES DE LA PAGE + DEVENUS DES TESTS (C-326). Chacun porte sa décision EN DUR, avec sa source, et rougit sur sa sonde.
 * La vraie app, ouverte par le vrai chemin (le + puis la pilule) ; les gestes au pointeur (la page lit le toucher lui-même : appui puis lever).
 * La correspondance juge → test → sonde : promi/JUGES-TESTS.md, « Lot 2a ».
 */
import { test, expect, type Page } from '@playwright/test';
import { stockage, vraieApp, ouvrirPlus, ouvrirPagePlus, P_, sonde } from './aides.ts';

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
          return !c.hidden && !c.classList.contains('pp-compose');
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
      await toucher(page, '#createSheet .closeb');
      await page
        .waitForFunction(() => !!(window as unknown as { __part: unknown }).__part, undefined, { timeout: 5000 })
        .catch(() => undefined);
      const part = ((await page.evaluate(() => (window as unknown as { __part: unknown }).__part)) ?? {
        classe: false,
        duree: '0s',
        prop: '',
      }) as { classe: boolean; duree: string; prop: string };
      expect(part.classe, 'la page + part (pp-part)').toBe(true);
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
  expect((await etat(page)).phrase.qui).toEqual([nom]);
  const l = await lignes(page);
  expect(
    l.slice(0, 2),
    'C-269 : « à Rachel, / chiche » (le prénom choisi, une virgule, « chiche » en bas de casse)',
  ).toEqual([`à ${nom},`, 'chiche']);
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
    return { vide: m.classList.contains('ph-vide'), bord: getComputedStyle(m).borderTopStyle };
  });
  expect(p).toEqual({ vide: false, bord: 'solid' });
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
