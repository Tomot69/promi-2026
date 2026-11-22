/**
 * L0 §2 et §3 — LA VRAIE APP DONNE AU MOTEUR EXACTEMENT CE QUE LE PROTOTYPE LUI DONNE, sur l'état de Tom.
 *
 * Le moteur est le même (une copie octet pour octet, tests/unitaires/repris.test.ts) ; le rendu au pixel est prouvé par banc_rendu porté
 * (banc-rendu.spec.ts). Ce qui reste à prouver sur l'état RÉEL de Tom (A2), c'est que la vraie app nourrit le moteur comme le prototype :
 * après l'import de l'export et le démarrage, des deux côtés, les mêmes paroles (tous leurs champs, passes de relecture comprises), les
 * mêmes Cercles, le même monde, la même palette, la même teinte, la même graine, le même thème, le même « avec texte », et les mêmes graines
 * (nature et parole de chacune). Et la vue de départ de la vraie app est EXACTEMENT celle que l'iPhone de Tom avait relevée dans son
 * export (`toile.vue`) — le prototype, démarré en temps réel, ne la retrouve pas toujours (la course de C-177 : mesuré 1,0044 à 1,0071).
 *
 * Pourquoi pas le pixel du prototype vivant sur l'état de Tom (A6) : démarré en temps réel, le prototype n'est pas reproductible d'une
 * passe à l'autre sur ces états (mesuré le 20 nov. : sa vue de départ varie, et le protocole du banc y est INSTABLE des deux côtés).
 * L'export du 23 oct. (six paroles à la même place, C-177) n'est pas jugé ici : la relecture efface cinq places (`reparerPlaces`) et le
 * moteur en choisit de nouvelles au moment où il les note — un moment de temps réel dans le prototype (mesuré : 5 places différentes) ;
 * il est jugé, sans perte, par l'import (tests/unitaires/import.test.ts).
 * Les exports de Tom (etats/) sont hors dépôt : en intégration continue, deux états du banc (banc-etats/) les remplacent.
 */
import { test, expect, type Page } from '@playwright/test';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { AMORCE, T_FIGE } from './banc.ts';

const RACINE = join(import.meta.dirname, '..', '..', '..');
// les exports de Tom (etats/, hors dépôt) qui portent des paroles — tous, sauf celui du 23 oct. (voir plus haut) — et deux états du banc
const ETATS = [
  ...(existsSync(join(RACINE, 'etats'))
    ? readdirSync(join(RACINE, 'etats'))
        .filter((f) => f.endsWith('.json') && f !== 'tom-20261023-125022.json')
        .map((f) => 'etats/' + f)
        .filter((f) => {
          const x = JSON.parse(readFileSync(join(RACINE, f), 'utf8')) as { ls?: Record<string, string> };
          return (
            (JSON.parse(x.ls?.['promi_state'] ?? '{"promises":[]}') as { promises: unknown[] }).promises.length > 0
          );
        })
    : []),
  'banc-etats/etat-25.json',
  'banc-etats/etat-cercle.json',
].filter((f) => existsSync(join(RACINE, f)));

/**
 * Hors de la comparaison, et seulement eux : `x, y, tx, ty`, l'ancien calque SVG du prototype (`render()`, `targets()`), que le moteur ne
 * lit pas (CLAUDE.md §8 : « Arranger marche et rien ne bouge ») ; `files`, la pièce jointe DE DÉMONSTRATION que le prototype colle à la
 * première parole d'un Cercle au démarrage (app.html ≈ l. 9642, « pour que la fonctionnalité soit visible d'emblée ») — une donnée inventée
 * par le prototype, que la vraie app ne reprend pas.
 */
const HORS = ['x', 'y', 'tx', 'ty', 'files'];
/**
 * Exception nommée de la vue : l'export du 1er nov. à 19 h 54 a relevé la vue d'un démarrage pris dans la course de C-177 (zoom 1,0070) ;
 * le même état, exporté à 20 h 55, a relevé 1,00446 — celle que la vraie app retrouve. Les entrées du moteur, elles, y sont jugées.
 */
const VUE_PENDANT_LA_COURSE = new Set(['etats/tom-20261101-195418.json']);

const LIRE = `()=>{ const HORS=${JSON.stringify(HORS)}; return ({
  paroles: JSON.stringify(promises.map(p=>{ const o={}; for(const k of Object.keys(p).sort()) if(!HORS.includes(k)) o[k]=p[k]; return o; })),
  cercles: JSON.stringify(window.NUE||NUE), dallesCercles: JSON.stringify(window.NUEDALLE||{}),
  monde: Toile.getTheme(), palette: Toile.getPalette(), teinte: Toile.getHue(), cle: Toile.cle(),
  clair: document.getElementById('device').classList.contains('light'), texte: Toile.labelsOn(),
  graines: JSON.stringify(Toile_graines().map(g=>[g[0],g[3]])), vue: Toile_lecture().vue }); }`;

/**
 * L0 §2 (Tom) : la vraie app S'ADAPTE à l'écran ; elle est identique au prototype à la taille de RÉFÉRENCE, 390 × 844. Le prototype, lui,
 * est jugé dans la fenêtre du banc (son appareil y fait 390 × 844) et dans celle de Safari à 0,79 (330 × 714 : réduit, toujours 390 × 844
 * pour le moteur) — A3. Les autres tailles d'écran de la vraie app : tests/rendu/ecrans.spec.ts.
 */
const ECHELLES = [
  { nom: '1', viewport: { width: 430, height: 932 } },
  { nom: '0,79', viewport: { width: 330, height: 714 } },
];

for (const f of ETATS)
  for (const ech of ECHELLES)
    test(`les entrées du moteur : « ${f} », échelle ${ech.nom}`, async ({ browser }) => {
      const x = JSON.parse(readFileSync(join(RACINE, f), 'utf8')) as {
        ls?: Record<string, string>;
        toile?: { vue?: unknown };
      };
      const ls: Record<string, string> = {};
      for (const [k, v] of Object.entries(x.ls ?? (x as Record<string, string>)))
        if (k !== 'setItem' && typeof v === 'string') ls[k] = v;
      const ctx = (): ReturnType<typeof browser.newContext> =>
        browser.newContext({ viewport: ech.viewport, deviceScaleFactor: 3 });
      const P: Page = await (await ctx()).newPage();
      // la vraie app à la taille de référence (L0 §2) : le moteur s'y mesure sur 390 × 844, comme dans l'appareil du prototype
      const A: Page = await (
        await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })
      ).newPage();
      try {
        const erreurs: string[] = [];
        A.on('pageerror', (e) => erreurs.push(String(e)));
        await P.addInitScript((ls) => {
          localStorage.clear();
          for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v);
        }, ls);
        await A.addInitScript((a) => new Function(a)(), AMORCE);
        await Promise.all([
          (async () => {
            await P.goto('http://127.0.0.1:8753/app.html');
            await P.waitForTimeout(9000);
          })(),
          (async () => {
            await A.goto(`http://127.0.0.1:5180/?banc=1&pilote=${T_FIGE}`);
            await A.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
            await A.evaluate(async (ls) => {
              const p = (
                window as unknown as {
                  __promi: {
                    magasin: { importer(x: unknown): void };
                    demarrer(o?: { accueil?: boolean }): Promise<void>;
                    horloge: { images(n: number): void };
                  };
                }
              ).__promi;
              p.magasin.importer({ ls });
              await p.demarrer({ accueil: false });
              p.horloge.images(540);
            }, ls);
          })(),
        ]);
        type Lu = Record<string, unknown> & { vue: unknown };
        const p = (await P.evaluate(`(${LIRE})()`)) as Lu;
        const a = (await A.evaluate(`(${LIRE})()`)) as Lu;
        const differents = Object.keys(p).filter((k) => k !== 'vue' && JSON.stringify(p[k]) !== JSON.stringify(a[k]));
        // le détail, champ par champ, des paroles qui diffèrent
        const pp = JSON.parse(p['paroles'] as string) as Array<Record<string, unknown>>;
        const aa = JSON.parse(a['paroles'] as string) as Array<Record<string, unknown>>;
        const detail: string[] = [];
        pp.forEach((x, i) => {
          const y = aa[i] ?? {};
          for (const k of new Set([...Object.keys(x), ...Object.keys(y)]))
            if (JSON.stringify(x[k]) !== JSON.stringify(y[k]))
              detail.push(`parole ${String(x['id'])} ${k} : ${JSON.stringify(x[k])} ≠ ${JSON.stringify(y[k])}`);
        });
        if (detail.length) console.log(detail.slice(0, 30).join('\n'));
        expect(erreurs, 'erreurs JavaScript de la vraie app').toEqual([]);
        expect(
          differents,
          differents
            .map((k) => `${k} :\n  prototype ${String(p[k]).slice(0, 400)}\n  vraie app ${String(a[k]).slice(0, 400)}`)
            .join('\n'),
        ).toEqual([]);
        if (x.toile?.vue && !VUE_PENDANT_LA_COURSE.has(f))
          expect(a.vue, "la vue de départ = celle que l'iPhone de Tom a relevée").toEqual(x.toile.vue);
      } finally {
        // les deux contextes fermés à chaque cas, même en échec : laissés ouverts, ils s'accumulent et épuisent la mémoire du runner
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
