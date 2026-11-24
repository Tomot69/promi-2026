/**
 * LOT 2c — LES JUGES DU 2c DEVENUS DES TESTS : les textes longs (C-244 §5.1, v46), les mots de liaison (C-278 ⑥, C-312), les deux changements secs
 * qui restaient (« + ajouter quelqu’un » ↔ « un prénom… », la taille de la phrase en entrant dans la saisie), le glissement continu de la phrase
 * (C-278 §4). Chacun porte sa décision EN DUR, avec sa source, et rougit sur sa sonde. La correspondance : promi/JUGES-TESTS.md, « Lot 2c ».
 */
import { test, expect, type Page } from '@playwright/test';
import { stockage, vraieApp, ouvrirPagePlus, refermerPagePlus, P_, sonde } from './aides.ts';

type Nat = 'promi' | 'chiche' | 'nuee';

async function ouvrir(page: Page, nat: Nat): Promise<void> {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  await ouvrirPagePlus(page, nat);
}
/** un toucher au centre d'un élément (la page lit le toucher elle-même : appui puis lever) */
async function toucher(page: Page, sel: string): Promise<void> {
  await page.evaluate((s) => {
    const e = document.querySelector<HTMLElement>(s)!;
    const r = e.getClientRects()[0] ?? e.getBoundingClientRect();
    const o = {
      bubbles: true,
      clientX: r.left + Math.min(r.width / 2, 30),
      clientY: r.top + r.height / 2,
      pointerId: 31,
    };
    const c = document.elementFromPoint(o.clientX, o.clientY) ?? e;
    c.dispatchEvent(new PointerEvent('pointerdown', o));
    c.dispatchEvent(new PointerEvent('pointerup', o));
  }, sel);
  await page.waitForTimeout(150);
}
/** plus aucun mouvement, plus aucun passage en flaques, plus aucun tracé — au-delà de 30 s, le juge NOMME ce qui bouge encore */
const posee = async (page: Page): Promise<void> => {
  try {
    await page.waitForFunction(
      `!document.querySelector('#createSheet [data-flaques-mode]') && !${P_}.pagePlus().etat().mouvement && !window.TraceLettres?.actif() && !document.getAnimations().some(a => a.playState === 'running' && a.effect?.getTiming().iterations !== Infinity && a.effect?.target?.closest?.('#createSheet'))`,
      undefined,
      { timeout: 30000 },
    );
  } catch (e) {
    const d = await page.evaluate(
      `({ de: ${P_}.pagePlus().etat().mouvementDe, flaques: !!document.querySelector('#createSheet [data-flaques-mode]'), trace: !!window.TraceLettres?.actif(), anim: document.getAnimations().filter(a => a.playState === 'running' && a.effect?.getTiming().iterations !== Infinity && a.effect?.target?.closest?.('#createSheet')).map(a => (a.effect.target.className || a.effect.target.tagName) + ':' + (a.animationName || a.id || a.constructor.name)) })`,
    );
    throw new Error(`la page + n'est pas posée après 30 s : ${JSON.stringify(d)}`, { cause: e });
  }
};
const TITRE = '#createSheet .pp-phrase .ph-m[data-ph="titre"]';
const NOM = '#createSheet .pp-phrase .ph-m[data-np="nom"]';
/** la sonde « réduire les animations » posée en douce : tout change d'un coup */
async function sec(page: Page): Promise<void> {
  await page.evaluate(() => {
    const m = window.matchMedia.bind(window);
    window.matchMedia = (q: string) =>
      (/reduce/.test(q) ? { matches: true, media: q } : m(q)) as unknown as MediaQueryList;
  });
}

// ── redteam_page_plus_continu (v203, C-278 §4 : « la fin de chaque séquence arrive par un seul mouvement continu, sans saut ni recalage final ;
//    en passant à “promets-moi”, les mots changent de place d'un coup : ils glissent ») ──
/** (la place d'un mot est celle de sa PREMIÈRE ligne — sur deux lignes, sa boîte englobante part du début de la seconde, là où le mot ne commence
 *  pas : un exemple coupé qui revient y paraissait sauter de 57 pt)
 *  (l'heure d'une image est celle que donne `requestAnimationFrame` — celle que le mouvement lit —, jamais l'heure à laquelle le rappel de la
 *  sonde passe : sinon une image courte porte le pas d'une longue, et le relevé compte un saut qui n'est pas peint, §8)
 *  la sonde du prototype, relevée à chaque image dans la page : chaque mot de la phrase (sa place, ses liaisons), le haut de la phrase, sa
 *  taille VUE (police × `scale`), le rail du pinceau — ce qui est visible seulement ; jusqu'à 600 ms d'immobilité (6 s au plus) */
const SONDE = `(() => { const H = window.__P = []; const t0 = performance.now(); let calme = performance.now(), av = null; window.__Pfin = null;
  if (!window.__anOk) { window.__anOk = 1; window.__AN = []; const a0 = Element.prototype.animate;
    Element.prototype.animate = function (k, o) { const an = a0.call(this, k, o); const k0 = Array.isArray(k) ? k[0] : null;
      if (k0 && ('translate' in k0 || 'scale' in k0 || 'transform' in k0) && this.closest && this.closest('#createSheet .pp-phrase, #csPinceau')) {
        const d = typeof o === 'object' && o ? o.duration : o; queueMicrotask(() => window.__AN.push([an.playState, d])); }
      return an; }; }
  const cs = document.getElementById('createSheet');
  const vis = (e) => { for (let q = e; q && q.nodeType === 1; q = q.parentElement) { const c = getComputedStyle(q); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05 || q.hidden) return false; if (q === cs) break; } return true; };
  (function f(ts) { const d = document.getElementById('device').getBoundingClientRect(), k = d.width / 390, P = {};
    const y = (r) => Math.round(((r.top - d.top) / k) * 10) / 10, x = (r) => Math.round(((r.left - d.left) / k) * 10) / 10;
    if (!cs.hidden) { const t = cs.querySelector('.pp-phrase .ph-txt');
      if (t && vis(t)) { const T = t.getBoundingClientRect(); P.phrase = [x(T), y(T)]; const sc = parseFloat(getComputedStyle(t).scale) || 1; P.taille = [Math.round((parseFloat(t.style.fontSize) || 0) * sc * 10) / 10, 0]; const cnt = {};
        t.querySelectorAll('[data-ph],[data-np],em').forEach((e) => { if (e.tagName === 'EM' && e.closest('[data-ph],[data-np]')) return; const s = (e.textContent || '').trim(), n = (cnt[s] = (cnt[s] || 0) + 1), r = e.getClientRects()[0] || e.getBoundingClientRect(); if (!(r.width > 0) || !vis(e)) return;
          const kk = (e.dataset.ph || e.dataset.np) ? 'mot:' + (e.dataset.ph || e.dataset.np) : 'liaison:' + s + '#' + n; P[kk] = [x(r), y(r)]; }); }
      const rl = document.getElementById('csPinceau'); if (rl && vis(rl)) { const r = rl.getBoundingClientRect(); if (r.height > 0) P.rail = [x(r), y(r)]; } }
    const now = ts ?? performance.now(), s = JSON.stringify(P); H.push([Math.round(now - t0), P, Math.round(performance.now() - t0)]);
    if (s !== av) { calme = now; av = s; }
    if (now - t0 < 6000 && !(now - calme > 600 && now - t0 > 800)) requestAnimationFrame(f); else window.__Pfin = now - t0; })(); })()`;
/** [l'heure de l'image, les places, l'heure où le rappel de la sonde passe] */
type Releve = [number, Record<string, [number, number]>, number][];
/** un SAUT : plus de 2 pt en une image (de 34 ms au plus), quand les images voisines vont trois fois moins VITE (le prototype, `sauts`) */
function sauts(H: Releve): [number, string, number][] {
  const out: [number, string, number][] = [];
  const cles = new Set(H.flatMap(([, P]) => Object.keys(P)));
  for (const c of cles) {
    const S = H.filter(([, P]) => c in P).map(([t, P, n]) => [t, P[c]!, n] as const);
    const d: [number, number, number, number][] = [];
    for (let i = 1; i < S.length; i++) {
      const [ta, a, na] = S[i - 1]!;
      const [tb, b, nb] = S[i]!;
      d.push([tb, Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])), tb - ta, nb - na]);
    }
    d.forEach(([t, v, dt, dn], i) => {
      // une image se juge si elle est PROPRE : 34 ms au plus, à l'heure de l'image comme à l'heure du rappel, les deux d'accord à 8 ms près —
      // sinon le fil était occupé au milieu de l'image, et un mouvement mené par l'horloge y rattrape le temps perdu (un à-coup de la charge,
      // pas un changement sec)
      if (v <= 2 || dt > 34 || dn > 34 || Math.abs(dn - dt) > 8) return;
      // la vitesse des images voisines, longues comprises : une image courte entre deux longues (la machine chargée) n'est pas un saut si la
      // phrase allait déjà à cette vitesse ; un changement SEC, lui, a des voisines immobiles (le prototype ne jugeait que des voisines de
      // 34 ms au plus — entre deux longues, toute image courte d'un glissement y était un « saut »)
      const voisins = [i - 1, i + 1].filter((j) => j >= 0 && j < d.length).map((j) => d[j]![1] / Math.max(d[j]![2], 1));
      if (!voisins.length || v / Math.max(dt, 1) > 3 * Math.max(Math.max(...voisins), 0.5 / 16.7))
        out.push([t, c, Math.round(v * 10) / 10]);
    });
  }
  return out.sort((a, b) => a[0] - b[0]);
}
async function releve(page: Page, geste: () => Promise<void>): Promise<{ H: Releve; fin: number | null }> {
  await page.evaluate(SONDE);
  await geste();
  await page.waitForFunction('window.__Pfin != null', undefined, { timeout: 30000 }).catch(() => undefined);
  return {
    H: ((await page.evaluate('window.__P')) as Releve | undefined) ?? [],
    fin: (await page.evaluate('window.__Pfin ?? null')) as number | null,
  };
}
test('la phrase de la page + change de place par un seul mouvement continu : valider, le sens basculé trois fois, le titre effacé — aucun saut (redteam_page_plus_continu, C-278 §4)', async ({
  page,
}) => {
  test.setTimeout(240000);
  await ouvrir(page, 'promi');
  // la sonde : les glissements et la mise à l'échelle retirés (Web Animations sur `translate`, `transform`, `scale` rendues finies d'un coup)
  if (sonde('continu-saut'))
    await page.evaluate(() => {
      const a = Element.prototype.animate;
      Element.prototype.animate = function (
        this: Element,
        k: Keyframe[] | PropertyIndexedKeyframes | null,
        o?: number | KeyframeAnimationOptions,
      ) {
        const an = a.call(this, k, o);
        const k0 = Array.isArray(k) ? k[0] : null;
        if (k0 && ('translate' in k0 || 'scale' in k0 || 'transform' in k0) && !this.closest('#dessinMode'))
          an.finish();
        return an;
      };
    });
  await toucher(page, TITRE);
  await posee(page);
  await page.keyboard.type('lire', { delay: 50 });
  await page.waitForTimeout(400);
  // [nom, le geste (le chrono part avec lui), ce qui le prépare (hors du chrono)]
  const seq: [string, () => Promise<void>, (() => Promise<void>)?][] = [
    ['valider (Retour)', () => page.keyboard.press('Enter')],
    ["le sens : soi → à quelqu'un", () => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]')],
    ["le sens : à quelqu'un → promets-moi", () => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]')],
    ['le sens : promets-moi → soi', () => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]')],
    [
      'le titre effacé (l’exemple revient)',
      async () => {
        for (let i = 0; i < 4; i++) await page.keyboard.press('Backspace');
        await page.keyboard.press('Enter');
      },
      // ⚑ (CI Linux, 24 nov.) : le chrono des 4 s comptait le toucher du titre et l'attente de 700 ms du test (5,2 s relevées) — il part à
      // l'effacement, qui fait revenir l'exemple ; ouvrir la saisie se fait avant, la page posée
      async () => {
        await toucher(page, TITRE);
        await posee(page);
        await page.waitForTimeout(700);
      },
    ],
  ];
  const rouges: string[] = [];
  let bougent = 0;
  for (const [nom, geste, avant] of seq) {
    await posee(page);
    if (avant) await avant();
    await page.waitForTimeout(500);
    const { H, fin } = await releve(page, geste);
    const s = sauts(H);
    // au moins un élément a bougé pendant la séquence (sinon le relevé ne prouve rien)
    const k0 = H[0]?.[1] ?? {};
    const kN = H[H.length - 1]?.[1] ?? {};
    if (Object.keys(kN).some((k) => !k0[k] || Math.abs(kN[k]![0] - k0[k]![0]) + Math.abs(kN[k]![1] - k0[k]![1]) > 2))
      bougent++;
    if (s.length) rouges.push(`${nom} : ${JSON.stringify(s.slice(0, 4))}`);
    if (fin == null || fin > 4600) rouges.push(`${nom} : pas immobile en 4 s (${String(fin)})`);
  }
  expect(bougent, 'les séquences déplacent bien la phrase').toBeGreaterThanOrEqual(3);
  // LE MÉCANISME (il se juge à toute cadence ; hors du Mac une image dure 0,7 s, un glissement de 320 ms y tient dans une seule image) : chaque
  // glissement et chaque mise à l'échelle de la phrase COURENT dans la tâche où ils naissent (jamais finis d'un coup) et durent 300 ms au moins
  const AN = (await page.evaluate('window.__AN')) as [string, number][];
  expect(AN.length, 'des glissements et des mises à l’échelle sont nés').toBeGreaterThan(0);
  expect(
    AN.filter(([etat, d]) => etat === 'finished' || etat === 'idle' || !(d >= 300)),
    'chaque mouvement court, 300 ms au moins (jamais fini d’un coup)',
  ).toEqual([]);
  expect(rouges, 'aucun saut, immobile en ≤ 4 s (C-278 §4)').toEqual([]);
});

// ── redteam_liaison, lot-V203-LIAISONS (v203, C-278 ⑥ : « les mots de liaison neufs se tracent, ceux qui partent se détracent à leur place » ;
//    C-312 : « de » / « d’ ») ──
test('les mots de liaison : « à » qui arrive se trace, celui qui part se détrace à sa place ; « de » ↔ « d’ » de même (lot-V203-LIAISONS, C-278 ⑥, C-312)', async ({
  page,
}) => {
  test.setTimeout(120000);
  await ouvrir(page, 'promi');
  if (sonde('liaison-sec')) await sec(page);
  // le relevé, à chaque image : chaque mot de liaison de la phrase, s'il est découpé (son tracé : une découpe sur lui), et les copies qui partent
  await page.evaluate(() => {
    const w = window as unknown as { __L: { t: number; neufs: string[]; partent: string[] }[]; __Lvus: Set<string> };
    w.__L = [];
    const f = (): void => {
      const cs = document.getElementById('createSheet')!;
      const neufs: string[] = [];
      cs.querySelectorAll<HTMLElement>('.pp-phrase .ph-txt em').forEach((e) => {
        if (e.closest('[data-ph],[data-np]')) return;
        const cp = getComputedStyle(e).clipPath;
        if (cp && cp !== 'none') neufs.push((e.textContent ?? '').trim());
      });
      const partent = [...cs.querySelectorAll<HTMLElement>('.pp-part-li')].map((e) => (e.textContent ?? '').trim());
      w.__L.push({ t: performance.now(), neufs, partent });
      requestAnimationFrame(f);
    };
    f();
  });
  const vu = async (): Promise<{ neufs: string[]; partent: string[] }> => {
    const L = (await page.evaluate('window.__L.splice(0)')) as { neufs: string[]; partent: string[] }[];
    return { neufs: [...new Set(L.flatMap((x) => x.neufs))], partent: [...new Set(L.flatMap((x) => x.partent))] };
  };
  await posee(page);
  await vu();
  // soi → à quelqu'un : « à » arrive (« Je promets / de … / à qui ? »)
  await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  await posee(page);
  const a1 = await vu();
  // à quelqu'un → promets-moi → soi : « à » part
  await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  await posee(page);
  const a2 = await vu();
  await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  await posee(page);
  const a3 = await vu();
  a3.partent.push(...a2.partent);
  // « de » → « d’ » : « lire » posé, puis remplacé d'un coup par un titre qui commence par une voyelle (sans passer par l'exemple)
  await toucher(page, TITRE);
  await posee(page);
  await page.keyboard.type('lire', { delay: 60 });
  await page.keyboard.press('Enter');
  await posee(page);
  await toucher(page, TITRE);
  await posee(page);
  await vu();
  await page.keyboard.press('ControlOrMeta+a');
  await page.keyboard.insertText('aller');
  await page.keyboard.press('Enter');
  await posee(page);
  const a4 = await vu();
  expect(
    {
      arrive: a1.neufs.includes('à'),
      part: a3.partent.includes('à'),
      elide: a4.neufs.includes('d’'),
      deParti: a4.partent.includes('de'),
    },
    `les liaisons se tracent et se détracent (relevés : ${JSON.stringify([a1, a3, a4])})`,
  ).toEqual({ arrive: true, part: true, elide: true, deParti: true });
});

// ── redteam_textes_longs (v181b, C-244 §5.1, §5.3 : « 280 caractères pour une parole, 40 pour le nom d'un Cercle, à la saisie, collage compris » ;
//    la page + : rien ne se recouvre, la parole entière à l'écran), redteam_phrase_lignes (C-240 : 12 · 44 · 12 au-dessus de « garder de côté ») ──
const BASE =
  'courir le marathon de Paris avec toute la bande des copains du quartier puis fêter cela longtemps au bord du canal sous les lampions jusqu’au matin ' +
  'et recommencer l’année suivante avec encore plus de monde, des voisins, des cousins, des collègues et même le chien de la boulangère qui court vite ';
const LONGS: Record<Nat, string> = {
  promi: (BASE + BASE).slice(0, 280),
  chiche: (BASE + BASE).slice(0, 280),
  nuee: 'Les amis du grand jardin partagé du coin',
};
// (leurs titres : « les textes longs, promi : la limite (280) », « … chiche : la limite (280) », « … nuee : la limite (40) » ; la sonde
// long-deborde garde le titre à 30 pt)
for (const nat of ['promi', 'chiche', 'nuee'] as const)
  test(`les textes longs, ${nat} : la limite (${nat === 'nuee' ? 40 : 280}), tapée et collée ; la parole entière, rien ne se recouvre, le rail a son air (redteam_textes_longs, redteam_phrase_lignes, v46)`, async ({
    page,
  }) => {
    test.setTimeout(180000);
    await ouvrir(page, nat);
    const sel = nat === 'nuee' ? NOM : TITRE;
    const lim = nat === 'nuee' ? 40 : 280;
    await toucher(page, sel);
    await posee(page);
    // L · 20 de plus que la limite, tapés puis collés : la limite tient
    const t300 = (BASE + BASE + BASE).slice(0, lim + 20);
    await page.keyboard.type(t300.slice(0, lim + 20));
    const tape = await page.evaluate(() => (document.activeElement as HTMLInputElement).value.length);
    // collé par-dessus (tout sélectionné) : jamais un champ vide entre les deux — vidé, le texte se détracerait lettre à lettre (C-274)
    await page.keyboard.press('ControlOrMeta+a');
    await page.keyboard.insertText(t300);
    const colle = await page.evaluate(() => (document.activeElement as HTMLInputElement).value.length);
    expect({ tape, colle }, 'la limite, tapée et collée (C-244 §5.3)').toEqual({ tape: lim, colle: lim });
    // P · la parole longue, validée : entière à l'écran, rien ne se recouvre, l'air du rail (C-240)
    await page.keyboard.press('ControlOrMeta+a');
    await page.keyboard.insertText(LONGS[nat]);
    await page.keyboard.press('Enter');
    await posee(page);
    await page.waitForTimeout(800);
    // la sonde : le titre (le nom) gardé à 30 pt, sans réduction (C-244 §5.1 retiré) — la parole déborde sur le rail
    if (sonde('long-deborde'))
      await page.evaluate((s) => {
        const t = document.querySelector<HTMLElement>(s)!;
        t.style.setProperty('font-size', '30px', 'important');
        t.style.setProperty('line-height', '36px', 'important');
      }, sel);
    const g = await page.evaluate((s) => {
      const d = document.getElementById('device')!.getBoundingClientRect();
      const k = d.width / 390;
      const R = (r: DOMRect): number[] => [
        (r.left - d.left) / k,
        (r.top - d.top) / k,
        (r.right - d.left) / k,
        (r.bottom - d.top) / k,
      ];
      const t = document.querySelector<HTMLElement>('#createSheet .pp-phrase .ph-txt')!;
      const rg = document.createRange();
      rg.selectNodeContents(t);
      const lignes = [...rg.getClientRects()].filter((q) => q.width > 1 && q.height > 1).map(R);
      const bas = Math.max(...lignes.map((l) => l[3]!));
      const B: Record<string, number[]> = {};
      for (const [n, q] of [
        ['rail', '#csPinceau'],
        ['garder', '#createSheet .pp-garder'],
        ['trace', '#createSheet .pp-trace'],
        ['photo', '#createSheet .ph-photo-btn'],
      ] as const) {
        const e = document.querySelector<HTMLElement>(q);
        if (e && !e.hidden && e.getBoundingClientRect().height > 0) B[n] = R(e.getBoundingClientRect());
      }
      return { lignes, bas, B, texte: document.querySelector(s)!.textContent ?? '' };
    }, sel);
    const recouvre = (a: number[], b: number[]): boolean =>
      Math.min(a[2]!, b[2]!) - Math.max(a[0]!, b[0]!) > 1 && Math.min(a[3]!, b[3]!) - Math.max(a[1]!, b[1]!) > 1;
    const pb: string[] = [];
    for (const [n, b] of Object.entries(g.B)) for (const l of g.lignes) if (recouvre(l, b)) pb.push(`une ligne × ${n}`);
    for (const l of g.lignes)
      if (l[0]! < -0.5 || l[2]! > 390.5 || l[3]! > 844.5) pb.push(`une ligne hors de l’écran ${JSON.stringify(l)}`);
    // C-240 : 12 d'air, la rangée du pinceau (44), 12 d'air, puis « garder de côté »
    if (g.B['garder'] && g.bas + 12 + 44 + 12 > g.B['garder'][1]! + 0.5)
      pb.push(`l'air du rail : ${String(Math.round(g.B['garder'][1]! - g.bas))} pt sous la phrase`);
    expect(pb, 'rien ne se recouvre, rien ne sort, l’air du rail (C-240)').toEqual([]);
    expect(g.texte.replace(/\s+/g, ' ').trim(), 'la parole entière, sans « … » (C-244 §5.1)').toBe(
      LONGS[nat].replace(/\s+/g, ' ').trim(),
    );
  });

// ── les deux changements secs du 2c (C-271, AUDIT-SECS) : « + ajouter quelqu’un » ↔ « un prénom… » (v203 clôture §2, `_retour.remplace`,
//    `bascule`) ; la taille de la phrase en entrant dans la saisie (lot-V202A-TAILLE, C-273 : `scale`, 320 ms, jamais d'un coup) ──
test('« + ajouter quelqu’un » se détrace et « un prénom… » se trace ; « un prénom… » part et revient par le tracé (v203 clôture §2, C-271)', async ({
  page,
}) => {
  test.setTimeout(120000);
  await ouvrir(page, 'chiche');
  if (sonde('ajout-sec')) await sec(page);
  await toucher(page, '#createSheet .pp-phrase .ph-m[data-ph="qui"]');
  await posee(page);
  await page.evaluate(() => {
    const w = window as unknown as { __A: { copie: string[]; coupe: string[] }[] };
    w.__A = [];
    const f = (): void => {
      const cs = document.getElementById('createSheet')!;
      w.__A.push({
        copie: [...cs.querySelectorAll('.trace-copie')].map((e) => (e.textContent ?? '').trim()),
        coupe: [...cs.querySelectorAll<HTMLElement>('.ph-add .gn-ligne, .ph-add .gn-ph')]
          .filter((e) => {
            const c = getComputedStyle(e).clipPath;
            return !!c && c !== 'none';
          })
          .map((e) => e.className),
      });
      requestAnimationFrame(f);
    };
    f();
  });
  const lit = async (): Promise<{ copie: string[]; coupe: string[] }> => {
    const L = (await page.evaluate('window.__A.splice(0)')) as { copie: string[]; coupe: string[] }[];
    return { copie: [...new Set(L.flatMap((x) => x.copie))], coupe: [...new Set(L.flatMap((x) => x.coupe))] };
  };
  await lit();
  await toucher(page, '#createSheet .ph-add');
  await page.waitForTimeout(1500);
  const ouvre = await lit();
  await page.keyboard.type('L');
  await page.waitForTimeout(1200);
  const tape = await lit();
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(1200);
  const efface = await lit();
  expect(
    {
      ajouterPart: ouvre.copie.some((x) => /ajouter/.test(x)),
      ligneSeTrace: ouvre.coupe.includes('gn-ligne'),
      prenomPart: tape.copie.some((x) => /prénom/.test(x)),
      prenomRevient: efface.coupe.includes('gn-ph'),
    },
    `relevés : ${JSON.stringify([ouvre, tape, efface])}`,
  ).toEqual({ ajouterPart: true, ligneSeTrace: true, prenomPart: true, prenomRevient: true });
});

test('la taille de la phrase change en douceur en entrant dans la saisie et en la quittant : par sa mise à l’échelle, 320 ms, jamais d’un coup (lot-V202A-TAILLE, C-273)', async ({
  page,
}) => {
  test.setTimeout(120000);
  await ouvrir(page, 'promi');
  if (sonde('taille-seche')) await sec(page);
  await posee(page);
  type Vue = { v: number; t: number; anim: boolean };
  const taille = async (geste: () => Promise<void>): Promise<{ vues: Vue[]; f0: number; f1: number }> => {
    await page.evaluate(() => {
      const w = window as unknown as { __T: Vue[] };
      w.__T = [];
      const t0 = performance.now();
      const f = (ts?: number): void => {
        const t = document.querySelector<HTMLElement>('#createSheet .pp-phrase .ph-txt')!;
        w.__T.push({
          v: Math.round((parseFloat(t.style.fontSize) || 0) * (parseFloat(getComputedStyle(t).scale) || 1) * 10) / 10,
          t: ts ?? performance.now(),
          // sa mise à l'échelle en cours : une animation de `scale`, 320 ms (lot-V202A-TAILLE)
          anim: t.getAnimations().some((a) => {
            const k = (a.effect as KeyframeEffect | null)?.getKeyframes()[0];
            return a.playState === 'running' && !!k && 'scale' in k && a.effect?.getTiming().duration === 320;
          }),
        });
        if (performance.now() - t0 < 1500) requestAnimationFrame(f);
      };
      f();
    });
    const f0 = (await page.evaluate(
      "parseFloat(document.querySelector('#createSheet .pp-phrase .ph-txt').style.fontSize)",
    )) as number;
    await geste();
    await page.waitForTimeout(1700);
    const f1 = (await page.evaluate(
      "parseFloat(document.querySelector('#createSheet .pp-phrase .ph-txt').style.fontSize)",
    )) as number;
    return { vues: (await page.evaluate('window.__T')) as Vue[], f0, f1 };
  };
  const entre = await taille(() => toucher(page, TITRE));
  await posee(page);
  const sort = await taille(() => page.keyboard.press('Enter'));
  for (const [nom, r] of [
    ['entrer', entre],
    ['sortir', sort],
  ] as const) {
    // la taille change (36 → 30 en entrant : la règle du §2.8, un choix ouvert) ; la taille VUE passe par des valeurs intermédiaires
    expect(Math.abs(r.f1 - r.f0), `${nom} : la taille change`).toBeGreaterThan(1);
    // la mise à l'échelle a couru ; et, quand les images sont courtes (34 ms au plus : hors du Mac une image dure 0,7 s), la taille VUE passe
    // par des valeurs intermédiaires — jamais d'un coup
    expect(
      r.vues.some((x) => x.anim),
      `${nom} : la taille change par sa mise à l’échelle (${JSON.stringify(r.vues.slice(0, 20).map((x) => x.v))})`,
    ).toBe(true);
    const fen = r.vues.filter((x) => x.anim);
    const longues = r.vues.some((x, i) => i > 0 && x.anim && x.t - r.vues[i - 1]!.t > 34);
    const entre2 = r.vues.filter((x) => x.v > Math.min(r.f0, r.f1) + 0.3 && x.v < Math.max(r.f0, r.f1) - 0.3);
    if (!longues && fen.length >= 3)
      expect(
        entre2.length,
        `${nom} : des tailles vues entre ${String(r.f0)} et ${String(r.f1)} (${JSON.stringify(r.vues.slice(0, 30).map((x) => x.v))})`,
      ).toBeGreaterThanOrEqual(3);
  }
});

// ── redteam_moi_douceur, redteam_premiere, redteam_exemple_retour, redteam_retours (les places de la page +), redteam_secs2 — lot-V200-DOUCEUR
//    (C-271, C-269, C-274, C-279, C-282 : « l'encart en pointillés reste en place ; l'ancien texte se détrace ; l'encart s'adapte en douceur à la
//    largeur du nouveau mot ; puis il se trace » ; « à la première lettre, le texte d'exemple part en entier en 150 ms » ; « effacé, l'exemple
//    revient en se traçant ») ──
/** le relevé, à chaque image : pour chaque place de la phrase, sa largeur, sa découpe de tracé, ses flaques ; la copie de l'exemple qui part */
const RELEVE_PLACES = `(() => { const w = window; w.__R = []; w.__Ron = true;
  const f = (ts) => { const cs = document.getElementById('createSheet'); const o = { t: ts ?? performance.now(), n: performance.now(), p: {}, ex: [] };
    cs.querySelectorAll('.pp-phrase .ph-txt [data-ph],[data-np]').forEach((e) => { const k = e.dataset.ph || e.dataset.np; if (o.p[k]) return; const mt = e.querySelector(':scope > .ph-mt');
      const cp = (q) => { const c = q && getComputedStyle(q).clipPath; return !!c && c !== 'none'; };
      o.p[k] = { w: e.getBoundingClientRect().width, t: (e.textContent || '').trim(), coupe: cp(mt) || cp(e), fl: !!e.querySelector(':scope > canvas.passage-flaques'), vide: e.classList.contains('ph-vide'), wt: /width/.test(e.style.transition || '') }; });
    cs.querySelectorAll('.pp-ex-part > span').forEach((g) => o.ex.push(+getComputedStyle(g).opacity));
    o.part = cs.querySelectorAll('.pp-place-part').length;
    w.__R.push(o); if (w.__Ron) requestAnimationFrame(f); };
  f(); })()`;
type ImageR = {
  t: number;
  n: number;
  p: Record<string, { w: number; t: string; coupe: boolean; fl: boolean; vide: boolean; wt: boolean }>;
  ex: number[];
  part: number;
};
async function lire(page: Page): Promise<ImageR[]> {
  return (await page.evaluate('window.__R.splice(0)')) as ImageR[];
}
/** la largeur d'une place va en douceur : aucun pas d'une image ne fait plus de 40 % de la course (une course de plus de 12 pt) */
function largeurDouce(R: ImageR[], k: string): string | null {
  const V = R.filter((x) => (x.p[k]?.w ?? 0) > 0);
  if (V.length < 2) return null;
  const course = Math.abs(V[V.length - 1]!.p[k]!.w - V[0]!.p[k]!.w);
  if (course < 12) return null;
  for (let i = 1; i < V.length; i++) {
    const a = V[i - 1]!;
    const b = V[i]!;
    const pas = Math.abs(b.p[k]!.w - a.p[k]!.w);
    if (pas <= 0.4 * course) continue;
    // une image propre (34 ms au plus, les deux horloges d'accord) : un grand pas est un saut ; une image longue (hors du Mac, 0,7 s) : le
    // pas doit être porté par une transition de largeur en cours (le mécanisme), sinon il est sec
    const propre = b.t - a.t <= 34 && b.n - a.n <= 34 && Math.abs(b.n - a.n - (b.t - a.t)) <= 8;
    if (propre || !(a.p[k]!.wt || b.p[k]!.wt))
      return `${k} : un pas de ${pas.toFixed(1)} pt pour une course de ${course.toFixed(1)}${propre ? '' : ' (sans transition de largeur)'}`;
  }
  return null;
}
test('les places de la phrase changent en douceur : la première lettre (l’exemple part en 150 ms), l’exemple qui revient, une personne ajoutée, la bascule du sens (lot-V200-DOUCEUR, C-271, C-274, C-282)', async ({
  page,
}) => {
  test.setTimeout(180000);
  await ouvrir(page, 'chiche');
  if (sonde('places-seches')) await sec(page);
  await page.waitForTimeout(800);
  await page.evaluate(RELEVE_PLACES);
  const pb: string[] = [];
  // ① la première lettre (C-282) : l'exemple part en entier, sa copie s'efface image par image ; la lettre tapée est là tout de suite
  await toucher(page, TITRE);
  await posee(page);
  await lire(page);
  // l'instant de la frappe : celui de l'événement dans la page (jamais l'appel du test, qui y ajoute le trajet jusqu'au navigateur)
  await page.evaluate(
    "window.__tK = null; document.addEventListener('keydown', () => { window.__tK = window.__tK ?? performance.now(); }, { capture: true, once: true }); window.__R.length = 0",
  );
  await page.keyboard.type('x');
  await page.waitForTimeout(700);
  const tK = (await page.evaluate('window.__tK')) as number;
  const r1 = (await lire(page)).filter((x) => x.t >= tK);
  const ops = r1.flatMap((x) => (x.ex.length ? [x.ex[0]!] : []));
  const dernier = [...r1].reverse().find((x) => x.ex.length);
  // la lettre tapée est dans la première image après la frappe (Q620)
  if (!r1[0]?.p['titre']?.t.includes('x'))
    pb.push(
      `① la lettre tapée n’est pas dans la première image après la frappe (${JSON.stringify(r1[0]?.p['titre']?.t)})`,
    );
  if (!ops.length) pb.push('① aucune copie de l’exemple qui s’efface');
  else {
    if (!ops.some((o) => o > 0.02 && o < 0.98)) pb.push(`① l’exemple part d’un coup (${JSON.stringify(ops)})`);
    if (ops.some((o, i) => i && o > ops[i - 1]! + 0.001)) pb.push(`① l’opacité remonte (${JSON.stringify(ops)})`);
    // 150 ms (C-282) : jugé quand les images de la fenêtre durent 34 ms au plus ; sinon la charge du Mac, non jugé (C-227 §5)
    //   la fenêtre compte AUSSI l'attente de la première image après la frappe, et va jusqu'à l'image qui suit la dernière où la copie est là
    //   (sur l'intégration continue, une image dure 0,2 à 0,7 s : la première image vient déjà après 150 ms)
    const iD = dernier ? r1.indexOf(dernier) : -1;
    const fen = r1.slice(0, Math.min(r1.length, iD + 2));
    const longues =
      !fen.length ||
      fen[0]!.t - tK > 34 ||
      fen[0]!.n - tK > 34 ||
      fen.some((x, i) => i > 0 && (x.t - fen[i - 1]!.t > 34 || x.n - fen[i - 1]!.n > 34));
    if (dernier && !longues && dernier.t - tK > 150 + 34)
      pb.push(`① l’exemple encore là ${(dernier.t - tK).toFixed(0)} ms après la frappe (150 ms)`);
  }
  if (!r1.some((x) => x.p['titre']?.fl)) pb.push('① la pastille ne se remplit pas en flaques');
  // ② vidée (C-274) : le fond se retire en flaques, l'exemple revient en se traçant
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(2500);
  const r2 = await lire(page);
  if (!r2.some((x) => x.p['titre']?.fl)) pb.push('② le fond ne se retire pas en flaques');
  if (!r2.some((x) => x.p['titre']?.coupe && x.p['titre'].vide)) pb.push('② l’exemple ne revient pas en se traçant');
  await page.keyboard.type('nager');
  await page.keyboard.press('Enter');
  await posee(page);
  // ③ une personne ajoutée : l'encart va en douceur à la largeur du nom, la pastille se remplit en flaques, le nom se trace
  await toucher(page, '#createSheet .pp-phrase .ph-m[data-ph="qui"]');
  await posee(page);
  await toucher(page, '#createSheet .ph-add');
  await page.waitForTimeout(600);
  await page.keyboard.type('Bérénice');
  await lire(page);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);
  const r3 = await lire(page);
  const d3 = largeurDouce(r3, 'qui');
  if (d3) pb.push('③ ' + d3);
  if (!r3.some((x) => x.p['qui']?.fl)) pb.push('③ la pastille ne se remplit pas en flaques');
  if (!r3.some((x) => x.p['qui']?.coupe && x.p['qui'].t.includes('Bérénice'))) pb.push('③ le nom ne se trace pas');
  await page.evaluate('window.__Ron = false');
  expect(pb, 'les places changent en douceur').toEqual([]);
});
test('la bascule du sens : le verbe se détrace puis se trace, la place qui arrive se trace, celle qui part se détrace à sa place (lot-V200-DOUCEUR, C-271, C-296)', async ({
  page,
}) => {
  test.setTimeout(120000);
  await ouvrir(page, 'promi');
  if (sonde('sens-sec')) await sec(page);
  await page.waitForTimeout(800);
  await page.evaluate(RELEVE_PLACES);
  const pb: string[] = [];
  // soi → à quelqu'un : « Je me promets » → « Je promets », « à qui ? » arrive
  await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  await page.waitForTimeout(2500);
  const r1 = await lire(page);
  if (!r1.some((x) => x.p['sens']?.coupe)) pb.push('le verbe ne se détrace ni ne se trace');
  if (!r1.some((x) => x.p['qui']?.coupe)) pb.push('« à qui ? » paraît d’un coup');
  await posee(page);
  // à quelqu'un → promets-moi → soi : « à qui ? » part (sa copie se détrace là où elle était)
  await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  await posee(page);
  await lire(page);
  await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  await page.waitForTimeout(2500);
  const r3 = await lire(page);
  if (!r3.some((x) => x.part > 0)) pb.push('la place qui part disparaît d’un coup');
  await page.evaluate('window.__Ron = false');
  expect(pb, 'la bascule du sens, en douceur').toEqual([]);
});

// ── redteam_nature_plus (v177, C-224 : « un Cercle ouvert puis fermé par son X, puis un Promi, puis un Chiche : le trait plante à chaque fois, la
//    bonne nature, et un Cercle ensuite plante un Cercle ») ──
test('la page + lit sa nature : un Cercle fermé par son X, puis un Promi, un Chiche, un Cercle — chacun plante la bonne nature (redteam_nature_plus, C-224)', async ({
  page,
}) => {
  test.setTimeout(240000);
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // la sonde : la page + garde la nature de sa première ouverture (le défaut de v176 : `createKind` jamais remis)
  if (sonde('nature-collee'))
    await page.evaluate(
      `(() => { const pp = ${P_}.pagePlus(); const o = pp.ouvrir.bind(pp); let premiere = null; pp.ouvrir = (n) => { premiere = premiere || n; o(premiere); }; ${P_}.nav.poser('pagePlus', (n) => pp.ouvrir(n)); })()`,
    );
  const compte = (): Promise<{ promi: number; chiche: number; cercles: number }> =>
    page.evaluate(
      `(() => { const e = ${P_}.magasin.etat(); return { promi: e.paroles.filter((p) => !p.chiche && !p.draft).length, chiche: e.paroles.filter((p) => p.chiche).length, cercles: Object.keys(e.cercles).length }; })()`,
    ) as never;
  const planter = async (nat: Nat, titre: string): Promise<void> => {
    await ouvrirPagePlus(page, nat);
    await toucher(page, nat === 'nuee' ? NOM : TITRE);
    await posee(page);
    await page.keyboard.type(titre);
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
    for (let x = x0; x <= (nat === 'nuee' ? 340 : 200) * k; x += 8 * k) await page.mouse.move(x, y0);
    await page.mouse.up();
    await page.waitForFunction(() => !!document.getElementById('createSheet')?.hidden, undefined, { timeout: 15000 });
    await page.waitForTimeout(1500);
  };
  // un Cercle ouvert, puis fermé par son X
  await ouvrirPagePlus(page, 'nuee');
  await refermerPagePlus(page);
  const n0 = await compte();
  await planter('promi', 'lire');
  const n1 = await compte();
  await planter('chiche', 'nager');
  const n2 = await compte();
  await planter('nuee', 'Le potager');
  const n3 = await compte();
  expect(
    {
      promi: n1.promi - n0.promi,
      chicheApresPromi: n1.chiche - n0.chiche,
      chiche: n2.chiche - n1.chiche,
      cercle: n3.cercles - n2.cercles,
    },
    'chaque trait plante sa nature',
  ).toEqual({ promi: 1, chicheApresPromi: 0, chiche: 1, cercle: 1 });
});

// ── redteam_prenom_alterne (v211, C-309 : « l'exemple “promets-moi” alterne entre Bruno-Stanislas et Fabienne-Gudule : à chaque retour dans ce mode
//    après un autre mode, et à chaque fermeture puis réouverture de la page + ; le prénom qui change se détrace puis se trace ») ──
test('« promets-moi » : le prénom d’exemple alterne à chaque retour dans ce mode et à chaque réouverture (redteam_prenom_alterne, C-309)', async ({
  page,
}) => {
  test.setTimeout(180000);
  await ouvrir(page, 'promi');
  if (sonde('prenom-fige')) await page.evaluate(`(() => { ${P_}.magasin.avancerPrenom = () => 0; })()`);
  const sens = (): Promise<void> => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
  const prenom = async (): Promise<string> => {
    await posee(page);
    // la place a fini sa transition (« qui ? » détracé, le prénom tracé) : 10 s au plus, puis on lit ce qu'elle montre
    await page
      .waitForFunction(
        () => {
          const q = document.querySelector('#createSheet .pp-phrase [data-ph="qui"]');
          return (
            !!q && !q.querySelector('.ph-mt') && /^(Bruno-Stanislas|Fabienne-Gudule)/.test((q.textContent ?? '').trim())
          );
        },
        undefined,
        { timeout: 10000 },
      )
      .catch(() => undefined);
    return (await page.evaluate(
      "document.querySelector('#createSheet .pp-phrase [data-ph=\"qui\"]').textContent.trim().replace(/,$/, '')",
    )) as string;
  };
  const vus: string[] = [];
  // soi → à quelqu'un → promets-moi ; puis → soi → à quelqu'un → promets-moi
  await sens();
  await sens();
  vus.push(await prenom());
  for (let i = 0; i < 3; i++) await sens();
  vus.push(await prenom());
  // fermée, rouverte : deux entrées encore
  await refermerPagePlus(page);
  await ouvrirPagePlus(page, 'promi');
  await sens();
  await sens();
  vus.push(await prenom());
  for (let i = 0; i < 3; i++) await sens();
  vus.push(await prenom());
  for (const p of vus) expect(p, 'un des deux prénoms de C-309').toMatch(/^(Bruno-Stanislas|Fabienne-Gudule)$/);
  expect(
    vus.every((p, i) => i === 0 || p !== vus[i - 1]),
    `les prénoms alternent (${vus.join(' · ')})`,
  ).toBe(true);
});

// ── redteam_genese_nature (v203, C-278 : « la genèse en cours s'interrompt proprement et la nouvelle se fait entière, sans dalle en double ni
//    saut » — le sens basculé, puis une autre nature, pendant la genèse du trait) ──
test('la genèse du trait interrompue : le sens basculé à plusieurs instants, puis une autre nature — la genèse se refait entière, rien ne reste (redteam_genese_nature, C-278)', async ({
  page,
}) => {
  test.setTimeout(240000);
  await ouvrir(page, 'promi');
  // la sonde : le retrait de l'invite oublie son calque de passage (le défaut de C-218 : un bandeau reste)
  if (sonde('genese-reste'))
    await page.evaluate(() => {
      const r = Element.prototype.remove;
      Element.prototype.remove = function (this: Element) {
        if (this instanceof HTMLCanvasElement && this.classList.contains('passage-flaques')) return;
        r.call(this);
      };
    });
  const etatGenese = (): Promise<{ invite: boolean; passages: number; traits: number; dalles: number }> =>
    page.evaluate(`(() => { const cs = document.getElementById('createSheet'); const e = ${P_}.pagePlus().etat();
      return { invite: !!e.invite.visible, passages: cs.querySelectorAll('canvas.passage-flaques').length,
        traits: cs.querySelectorAll('#ppDepart').length, dalles: document.querySelectorAll('#ppNait').length }; })()`) as never;
  await toucher(page, TITRE);
  await posee(page);
  await page.keyboard.type('lire', { delay: 40 });
  const pb: string[] = [];
  for (const t of [0, 150, 400, 700, 1000, 1400, 2500]) {
    await page.keyboard.press('Enter').catch(() => undefined);
    await page.waitForTimeout(t);
    // pendant la genèse : le sens basculé, deux fois (le retour à soi garde la parole prête)
    await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
    await page.waitForTimeout(200);
    await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
    await toucher(page, '#createSheet .pp-phrase [data-ph="sens"]');
    await page
      .waitForFunction(`${P_}.pagePlus().etat().invite.visible`, undefined, { timeout: 30000 })
      .catch(() => undefined);
    await posee(page);
    // le passage en flaques de la genèse fini (hors du Mac il dure plusieurs secondes) ; un calque qui reste au-delà de 20 s est un défaut
    await page
      .waitForFunction(() => !document.querySelector('#createSheet canvas.passage-flaques'), undefined, {
        timeout: 20000,
      })
      .catch(() => undefined);
    await page.waitForTimeout(400);
    const e = await etatGenese();
    if (!e.invite || e.passages || e.dalles) pb.push(`à ${String(t)} ms : ${JSON.stringify(e)}`);
  }
  // une autre nature pendant la genèse : la page fermée par son X, rouverte en Chiche, puis en Cercle — page neuve, rien ne reste
  for (const nat of ['chiche', 'nuee'] as const) {
    await refermerPagePlus(page);
    await ouvrirPagePlus(page, nat);
    await posee(page);
    const e = await etatGenese();
    if (e.invite || e.passages || e.dalles) pb.push(`${nat}, page neuve : ${JSON.stringify(e)}`);
  }
  expect(pb, 'la genèse se refait entière, rien ne reste').toEqual([]);
});

// ── redteam_dalle_fixe (v179b, C-234 : « la dalle garde TOUJOURS la même taille, du début à la fin, pendant la frappe comme à la validation ; elle
//    se contente de DESCENDRE et de REMONTER avec l'horizon : 12 à 18 pt au plus, un mouvement doux ») ──
// (leurs titres : « la dalle de la page + ne zoome jamais, promi : … », « … chiche : … »)
for (const nat of ['promi', 'chiche'] as const)
  test(`la dalle de la page + ne zoome jamais, ${nat} : une seule taille de l’ouverture à la validation ; elle descend et remonte avec l’horizon, 18 pt au plus, en douceur (redteam_dalle_fixe, C-234)`, async ({
    page,
  }) => {
    test.setTimeout(120000);
    await ouvrir(page, nat);
    // chaque dalle POSÉE sur le champ de la page + est piégée : la taille et la place réellement peintes (1:1)
    // chaque peinture porte le numéro de l'IMAGE où elle a lieu (un compteur d'images) : un saut se juge image par image (la dernière place
    // peinte dans chaque image), jamais entre deux peintures d'une même image ni à l'horloge réelle (deux peintures à 10 ms de part et d'autre
    // d'une image faisaient un faux saut : CI du 23 nov.)
    await page.evaluate(`(() => { const f = ${P_}.facade; const p = f.poserUn.bind(f); window.__D = []; window.__F = 0;
      const compte = () => { window.__F++; requestAnimationFrame(compte); }; requestAnimationFrame(compte);
      f.poserUn = (g, cv, cx, cy) => { if (g.canvas.id === 'csTrameCv') { const d = window.devicePixelRatio || 1;
        window.__D.push({ f: window.__F, w: Math.round(cv.width / d * 10) / 10, h: Math.round(cv.height / d * 10) / 10, y: Math.round((cy - cv.height / d / 2) * 10) / 10 }); }
        return p(g, cv, cx, cy); }; })()`);
    // la sonde : la dalle demandée au moteur plus grande pendant la saisie (le défaut de v179 : elle remplissait le champ au plancher)
    if (sonde('dalle-zoom'))
      await page.evaluate(`(() => { const f = ${P_}.facade; const a = f.dalleAvenir.bind(f);
        f.dalleAvenir = (id, w, h, o) => document.querySelector('#createSheet.pp-ouvert') ? a(id, w * 1.4, h * 1.4, o) : a(id, w, h, o); })()`);
    // la sonde (sur « la dalle de la page + ne zoome jamais, promi : … ») : la dalle peinte 6 pt plus bas une image sur deux (un saut)
    if (sonde('dalle-saut'))
      await page.evaluate(
        `(() => { const f = ${P_}.facade; const p = f.poserUn; f.poserUn = (g, cv, cx, cy) => p(g, cv, cx, cy + (window.__F % 2 ? 6 : 0)); })()`,
      );
    await toucher(page, TITRE);
    await posee(page);
    await page.keyboard.type('nager au lac', { delay: 60 });
    await page.keyboard.press('Enter');
    await page.waitForFunction(`${P_}.pagePlus().etat().invite.visible`, undefined, { timeout: 30000 });
    await posee(page);
    const D = (await page.evaluate('window.__D')) as { f: number; w: number; h: number; y: number }[];
    expect(D.length, 'la dalle est peinte').toBeGreaterThan(3);
    const tailles = [...new Set(D.map((d) => `${String(Math.round(d.w))}×${String(Math.round(d.h))}`))];
    expect(tailles, 'une seule taille, de l’ouverture à la validation').toHaveLength(1);
    const ys = D.map((d) => d.y);
    expect(Math.max(...ys) - Math.min(...ys), 'elle descend et remonte de 18 pt au plus').toBeLessThanOrEqual(18.5);
    // en douceur : 3 pt au plus par image (jugé entre deux images qui se suivent ou à une image près : la place vue à la fin de chaque image)
    const parImage = new Map<number, number>();
    for (const d of D) parImage.set(d.f, d.y);
    const I = [...parImage.entries()].sort((a, b) => a[0] - b[0]);
    const sauts = I.slice(1)
      .map(([f, y], i) => ({ dy: Math.abs(y - I[i]![1]), df: f - I[i]![0] }))
      .filter((x) => x.df <= 2 && x.dy / x.df > 3);
    expect(sauts, 'aucun saut de la dalle').toEqual([]);
  });
