/**
 * LOT 2c — LES JUGES DU 2c DEVENUS DES TESTS : les textes longs (C-244 §5.1, v46), les mots de liaison (C-278 ⑥, C-312), les deux changements secs
 * qui restaient (« + ajouter quelqu’un » ↔ « un prénom… », la taille de la phrase en entrant dans la saisie), le glissement continu de la phrase
 * (C-278 §4). Chacun porte sa décision EN DUR, avec sa source, et rougit sur sa sonde. La correspondance : promi/JUGES-TESTS.md, « Lot 2c ».
 */
import { test, expect, type Page } from '@playwright/test';
import { stockage, vraieApp, ouvrirPagePlus, P_, sonde } from './aides.ts';

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
/** plus aucun mouvement, plus aucun passage en flaques, plus aucun tracé */
const posee = (page: Page): Promise<unknown> =>
  page.waitForFunction(
    `!document.querySelector('#createSheet [data-flaques-mode]') && !${P_}.pagePlus().etat().mouvement && !window.TraceLettres?.actif() && !document.getAnimations().some(a => a.playState === 'running' && a.effect?.getTiming().iterations !== Infinity && a.effect?.target?.closest?.('#createSheet'))`,
    undefined,
    { timeout: 30000 },
  );
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
/** (l'heure d'une image est celle que donne `requestAnimationFrame` — celle que le mouvement lit —, jamais l'heure à laquelle le rappel de la
 *  sonde passe : sinon une image courte porte le pas d'une longue, et le relevé compte un saut qui n'est pas peint, §8)
 *  la sonde du prototype, relevée à chaque image dans la page : chaque mot de la phrase (sa place, ses liaisons), le haut de la phrase, sa
 *  taille VUE (police × `scale`), le rail du pinceau — ce qui est visible seulement ; jusqu'à 600 ms d'immobilité (6 s au plus) */
const SONDE = `(() => { const H = window.__P = []; const t0 = performance.now(); let calme = performance.now(), av = null; window.__Pfin = null;
  const cs = document.getElementById('createSheet');
  const vis = (e) => { for (let q = e; q && q.nodeType === 1; q = q.parentElement) { const c = getComputedStyle(q); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05 || q.hidden) return false; if (q === cs) break; } return true; };
  (function f(ts) { const d = document.getElementById('device').getBoundingClientRect(), k = d.width / 390, P = {};
    const y = (r) => Math.round(((r.top - d.top) / k) * 10) / 10, x = (r) => Math.round(((r.left - d.left) / k) * 10) / 10;
    if (!cs.hidden) { const t = cs.querySelector('.pp-phrase .ph-txt');
      if (t && vis(t)) { const T = t.getBoundingClientRect(); P.phrase = [x(T), y(T)]; const sc = parseFloat(getComputedStyle(t).scale) || 1; P.taille = [Math.round((parseFloat(t.style.fontSize) || 0) * sc * 10) / 10, 0]; const cnt = {};
        t.querySelectorAll('[data-ph],[data-np],em').forEach((e) => { if (e.tagName === 'EM' && e.closest('[data-ph],[data-np]')) return; const s = (e.textContent || '').trim(), n = (cnt[s] = (cnt[s] || 0) + 1), r = e.getBoundingClientRect(); if (!(r.width > 0) || !vis(e)) return;
          const kk = (e.dataset.ph || e.dataset.np) ? 'mot:' + (e.dataset.ph || e.dataset.np) : 'liaison:' + s + '#' + n; P[kk] = [x(r), y(r)]; }); }
      const rl = document.getElementById('csPinceau'); if (rl && vis(rl)) { const r = rl.getBoundingClientRect(); if (r.height > 0) P.rail = [x(r), y(r)]; } }
    const now = ts ?? performance.now(), s = JSON.stringify(P); H.push([Math.round(now - t0), P]);
    if (s !== av) { calme = now; av = s; }
    if (now - t0 < 6000 && !(now - calme > 600 && now - t0 > 800)) requestAnimationFrame(f); else window.__Pfin = now - t0; })(); })()`;
type Releve = [number, Record<string, [number, number]>][];
/** un SAUT : plus de 2 pt en une image (de 34 ms au plus), quand les images voisines vont trois fois moins VITE (le prototype, `sauts`) */
function sauts(H: Releve): [number, string, number][] {
  const out: [number, string, number][] = [];
  const cles = new Set(H.flatMap(([, P]) => Object.keys(P)));
  for (const c of cles) {
    const S = H.filter(([, P]) => c in P).map(([t, P]) => [t, P[c]!] as const);
    const d: [number, number, number][] = [];
    for (let i = 1; i < S.length; i++) {
      const [ta, a] = S[i - 1]!;
      const [tb, b] = S[i]!;
      d.push([tb, Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])), tb - ta]);
    }
    d.forEach(([t, v, dt], i) => {
      if (v <= 2 || dt > 34) return;
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
    H: (await page.evaluate('window.__P')) as Releve,
    fin: (await page.evaluate('window.__Pfin')) as number | null,
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
  const seq: [string, () => Promise<void>][] = [
    ['valider (Retour)', () => page.keyboard.press('Enter')],
    ["le sens : soi → à quelqu'un", () => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]')],
    ["le sens : à quelqu'un → promets-moi", () => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]')],
    ['le sens : promets-moi → soi', () => toucher(page, '#createSheet .pp-phrase [data-ph="sens"]')],
    [
      'le titre effacé (l’exemple revient)',
      async () => {
        await toucher(page, TITRE);
        await page.waitForTimeout(700);
        for (let i = 0; i < 4; i++) await page.keyboard.press('Backspace');
        await page.keyboard.press('Enter');
      },
    ],
  ];
  const rouges: string[] = [];
  let bougent = 0;
  for (const [nom, geste] of seq) {
    await posee(page);
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
    await page.evaluate(() => {
      const a = document.activeElement as HTMLInputElement;
      a.value = '';
      a.dispatchEvent(new Event('input', { bubbles: true }));
    });
    await page.keyboard.insertText(t300);
    const colle = await page.evaluate(() => (document.activeElement as HTMLInputElement).value.length);
    expect({ tape, colle }, 'la limite, tapée et collée (C-244 §5.3)').toEqual({ tape: lim, colle: lim });
    // P · la parole longue, validée : entière à l'écran, rien ne se recouvre, l'air du rail (C-240)
    await page.evaluate(() => {
      const a = document.activeElement as HTMLInputElement;
      a.value = '';
      a.dispatchEvent(new Event('input', { bubbles: true }));
    });
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
  const taille = async (geste: () => Promise<void>): Promise<{ vues: number[]; f0: number; f1: number }> => {
    await page.evaluate(() => {
      const w = window as unknown as { __T: number[] };
      w.__T = [];
      const t0 = performance.now();
      const f = (): void => {
        const t = document.querySelector<HTMLElement>('#createSheet .pp-phrase .ph-txt')!;
        w.__T.push(
          Math.round((parseFloat(t.style.fontSize) || 0) * (parseFloat(getComputedStyle(t).scale) || 1) * 10) / 10,
        );
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
    return { vues: (await page.evaluate('window.__T')) as number[], f0, f1 };
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
    const entre2 = r.vues.filter((v) => v > Math.min(r.f0, r.f1) + 0.3 && v < Math.max(r.f0, r.f1) - 0.3);
    expect(
      entre2.length,
      `${nom} : des tailles vues entre ${String(r.f0)} et ${String(r.f1)} (${JSON.stringify(r.vues.slice(0, 30))})`,
    ).toBeGreaterThanOrEqual(3);
  }
});
