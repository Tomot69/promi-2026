/**
 * LOT 6 — LES COULEURS DE LA PELOTE (src/metier/pelote-couleurs.ts) : à entrées égales, ce que le PROTOTYPE rend (lot-AURA-PELOTE d'app.html,
 * ses fonctions `nouveauSol`, `corps`, `texteBouton`, `solIdxEff`, `fondSphere`, `lisibiliteIle`, `dalleLisible`, `iles`, et
 * `window._teinte`), relevé en faisant tourner ces fonctions elles-mêmes sur les mêmes entrées (le hasard : la même suite, mulberry32).
 * Les valeurs sont écrites en dur : un juge ne lit jamais la valeur qu'il vérifie (CLAUDE.md §7).
 */
import { describe, expect, it } from 'vitest';
import {
  cederIles,
  cessionIle,
  choixSol,
  contraste,
  corps,
  dE00,
  etatCouleursInitial,
  fondIleIngenu,
  fondPage,
  fondSphere,
  hauteurIngenu,
  kaki,
  lisibiliteIle,
  nouvelleOuverture,
  solEffectif,
  solIdxEff,
  texteBouton,
  type ContexteCouleurs,
  type Lab,
  type RGB,
  type StockageCouleurs,
} from '../../src/metier/pelote-couleurs.ts';

/* ── les entrées : la même suite au hasard que le relevé du prototype, un stockage en mémoire, la rampe du velours d'aujourd'hui (vingt
      marches, toutes le ton exact : v202a et v203, Q619) ── */
function hasard(graine: number): { h: () => number; n: () => number } {
  let a = graine >>> 0,
    n = 0;
  return {
    h: () => {
      n++;
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    },
    n: () => n,
  };
}
function stockage(init: Record<string, string> = {}): StockageCouleurs & { s: Record<string, string> } {
  const s = { ...init };
  return {
    s,
    lire: (k) => s[k] ?? null,
    ecrire: (k, v) => {
      s[k] = v;
    },
  };
}
const rampe = (b: RGB): RGB[] => Array.from({ length: 20 }, () => b);
const PALS: Record<string, RGB[]> = {
  signal: [
    [130, 174, 248],
    [255, 184, 210],
    [201, 168, 245],
    [239, 227, 199],
  ],
  candide: [
    [205, 180, 255],
    [255, 200, 162],
    [189, 224, 168],
    [255, 181, 200],
  ],
  irascible: [
    [255, 45, 26],
    [255, 138, 28],
    [184, 15, 46],
    [43, 10, 10],
  ],
  taciturne: [
    [11, 13, 79],
    [42, 42, 212],
    [143, 140, 255],
    [228, 226, 255],
  ],
  gouailleur: [
    [156, 74, 26],
    [224, 122, 31],
    [233, 184, 36],
    [125, 139, 46],
  ],
};
const PAGE: Record<'clair' | 'sombre', RGB> = { clair: [234, 217, 185], sombre: [5, 3, 2] };
const ctx = (pal: readonly RGB[], ingenu: boolean, clair: boolean, iles: (Lab | null)[] = []): ContexteCouleurs => ({
  palette: pal,
  ingenu,
  clair,
  page: PAGE[clair ? 'clair' : 'sombre'],
  iles,
  rampe,
});
const proche = (a: readonly number[], b: readonly number[]): void => {
  expect(a.length).toBe(b.length);
  a.forEach((v, i) => expect(v).toBeCloseTo(b[i]!, 3));
};
const T0 = 1e12;

describe('une ouverture de l’Aura, cinq palettes × deux thèmes', () => {
  const A = {
    'signal/clair': {
      solTire: 1,
      solVu: 0,
      poil: [130, 174, 248],
      corps: [255, 184, 210],
      corpsIdx: 1,
      corpsOrdre: [0, 2, 1],
      bouton: [96, 138, 209],
      boutonIdx: 0,
      texteOrdre: [0, 1, 3, 2],
      fond: [175.63, 199.74, 237.86],
      vue: '{"s":0,"k":1,"c":[171,177,236],"t":1000000000000,"p":null}',
      tirages: 6,
      dE: 31.996,
      kaki: false,
      contraste: 3.052,
    },
    'signal/sombre': {
      solTire: 1,
      solVu: 1,
      poil: [255, 184, 210],
      corps: [130, 174, 248],
      corpsIdx: 0,
      corpsOrdre: [0, 2, 1],
      bouton: [239, 227, 199],
      boutonIdx: 3,
      texteOrdre: [0, 1, 3, 2],
      fond: [255, 184, 210],
      vue: '{"s":1,"k":0,"c":[214,181,222],"t":1000000000000,"p":null}',
      tirages: 6,
      dE: 31.996,
      kaki: false,
      contraste: 16.154,
    },
    'candide/clair': {
      solTire: 2,
      solVu: 0,
      poil: [205, 180, 255],
      corps: [189, 224, 168],
      corpsIdx: 2,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [150, 126, 197],
      boutonIdx: 0,
      texteOrdre: [2, 0, 1, 3],
      fond: [221.38, 203.4, 242.13],
      vue: '{"s":0,"k":2,"c":[200,194,227],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 41.559,
      kaki: false,
      contraste: 3.035,
    },
    'candide/sombre': {
      solTire: 2,
      solVu: 2,
      poil: [189, 224, 168],
      corps: [255, 181, 200],
      corpsIdx: 3,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [205, 180, 255],
      boutonIdx: 0,
      texteOrdre: [2, 0, 1, 3],
      fond: [189, 224, 168],
      vue: '{"s":2,"k":3,"c":[210,210,178],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 45.368,
      kaki: false,
      contraste: 11.338,
    },
    'irascible/clair': {
      solTire: 2,
      solVu: 2,
      poil: [184, 15, 46],
      corps: [255, 138, 28],
      corpsIdx: 1,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [255, 45, 26],
      boutonIdx: 0,
      texteOrdre: [2, 0, 1, 3],
      fond: [208.57, 102.75, 114.64],
      vue: '{"s":2,"k":1,"c":[207,55,40],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 38.449,
      kaki: false,
      contraste: 3.274,
    },
    'irascible/sombre': {
      solTire: 2,
      solVu: 2,
      poil: [184, 15, 46],
      corps: [255, 138, 28],
      corpsIdx: 1,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [255, 45, 26],
      boutonIdx: 0,
      texteOrdre: [2, 0, 1, 3],
      fond: [184, 15, 46],
      vue: '{"s":2,"k":1,"c":[207,55,40],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 38.449,
      kaki: false,
      contraste: 5.53,
    },
    'taciturne/clair': {
      solTire: 2,
      solVu: 2,
      poil: [143, 140, 255],
      corps: [11, 13, 79],
      corpsIdx: 0,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [42, 42, 212],
      boutonIdx: 1,
      texteOrdre: [2, 0, 1, 3],
      fond: [183.56, 179, 242.13],
      vue: '{"s":2,"k":0,"c":[100,99,198],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 46.118,
      kaki: false,
      contraste: 7.761,
    },
    'taciturne/sombre': {
      solTire: 2,
      solVu: 2,
      poil: [143, 140, 255],
      corps: [11, 13, 79],
      corpsIdx: 0,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [53, 67, 233],
      boutonIdx: 1,
      texteOrdre: [2, 0, 1, 3],
      fond: [143, 140, 255],
      vue: '{"s":2,"k":0,"c":[100,99,198],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 46.118,
      kaki: false,
      contraste: 3.068,
    },
    'gouailleur/clair': {
      solTire: 2,
      solVu: 3,
      poil: [125, 139, 46],
      corps: [156, 74, 26],
      corpsIdx: 0,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [212, 111, 7],
      boutonIdx: 1,
      texteOrdre: [2, 0, 1, 3],
      fond: [172.58, 178.39, 114.64],
      vue: '{"s":3,"k":0,"c":[135,118,40],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 36.905,
      kaki: false,
      contraste: 3.04,
    },
    'gouailleur/sombre': {
      solTire: 2,
      solVu: 2,
      poil: [233, 184, 36],
      corps: [156, 74, 26],
      corpsIdx: 0,
      corpsOrdre: [0, 3, 1, 2],
      bouton: [224, 122, 31],
      boutonIdx: 1,
      texteOrdre: [2, 0, 1, 3],
      fond: [233, 184, 36],
      vue: '{"s":2,"k":0,"c":[208,148,33],"t":1000000000000,"p":null}',
      tirages: 7,
      dE: 39.302,
      kaki: false,
      contraste: 6.834,
    },
  } as const;
  for (const [cle, x] of Object.entries(A)) {
    it(cle, () => {
      const [nom, th] = cle.split('/') as [string, 'clair' | 'sombre'];
      const C = ctx(PALS[nom]!, nom === 'signal', th === 'clair'),
        e = etatCouleursInitial(),
        H = hasard(11),
        S = stockage();
      nouvelleOuverture(C, e, H.h, S, T0);
      expect(e.solTire).toBe(x.solTire);
      expect(solIdxEff(C, e)).toBe(x.solVu);
      expect(solEffectif(C, e)).toEqual(x.poil);
      const c = corps(C, e, H.h)!;
      expect(c).toEqual(x.corps);
      expect(e.corpsIdx).toBe(x.corpsIdx);
      expect(e.corpsOrdre).toEqual(x.corpsOrdre);
      const b = texteBouton(C, e, H.h);
      expect(b).toEqual({ rgb: x.bouton, idx: x.boutonIdx });
      expect(e.texteOrdre).toEqual(x.texteOrdre);
      proche(fondSphere(C, e), x.fond);
      expect(S.s['promi_pelote_vue']).toBe(x.vue);
      expect(H.n()).toBe(x.tirages);
      // les règles : le corps jamais kaki, à ΔE00 ≥ 15 du poil (v123) ; le bouton ≥ 3:1 sur son fond (v124)
      expect(kaki(c)).toBe(false);
      expect(dE00(c, x.poil)).toBeCloseTo(x.dE, 3);
      expect(dE00(c, x.poil)).toBeGreaterThanOrEqual(15);
      expect(contraste(b.rgb, fondPage(C))).toBeCloseTo(x.contraste, 3);
      expect(contraste(b.rgb, fondPage(C))).toBeGreaterThanOrEqual(3);
    });
  }
});

describe('trois ouvertures de suite : jamais le même poil ni le même corps (v125), le stockage gardé', () => {
  const B = {
    'signal/sombre': [
      {
        solTire: 0,
        solVu: 0,
        corps: [255, 184, 210],
        corpsIdx: 1,
        vue: '{"s":0,"k":1,"c":[171,177,236],"t":1000000000000,"p":null}',
        tirages: 6,
      },
      {
        solTire: 1,
        solVu: 1,
        corps: [130, 174, 248],
        corpsIdx: 0,
        vue: '{"s":1,"k":0,"c":[214,181,222],"t":1000000060000,"p":{"s":0,"k":1,"c":[171,177,236]}}',
        tirages: 45,
      },
      {
        solTire: 0,
        solVu: 0,
        corps: [255, 184, 210],
        corpsIdx: 1,
        vue: '{"s":0,"k":1,"c":[171,177,236],"t":1000000120000,"p":{"s":1,"k":0,"c":[214,181,222]}}',
        tirages: 84,
      },
      {
        solTire: 0,
        solVu: 0,
        corps: [255, 184, 210],
        corpsIdx: 1,
        vue: '{"s":0,"k":1,"c":[171,177,236],"t":1000000120200,"p":{"s":1,"k":0,"c":[214,181,222]}}',
        tirages: 123,
      },
    ],
    'candide/clair': [
      {
        solTire: 0,
        solVu: 0,
        corps: [189, 224, 168],
        corpsIdx: 2,
        vue: '{"s":0,"k":2,"c":[200,194,227],"t":1000000000000,"p":null}',
        tirages: 7,
      },
      {
        solTire: 3,
        solVu: 0,
        corps: [189, 224, 168],
        corpsIdx: 2,
        vue: '{"s":0,"k":2,"c":[200,194,227],"t":1000000060000,"p":{"s":0,"k":2,"c":[200,194,227]}}',
        tirages: 58,
      },
      {
        solTire: 1,
        solVu: 0,
        corps: [189, 224, 168],
        corpsIdx: 2,
        vue: '{"s":0,"k":2,"c":[200,194,227],"t":1000000120000,"p":{"s":0,"k":2,"c":[200,194,227]}}',
        tirages: 109,
      },
      {
        solTire: 3,
        solVu: 0,
        corps: [189, 224, 168],
        corpsIdx: 2,
        vue: '{"s":0,"k":2,"c":[200,194,227],"t":1000000120200,"p":{"s":0,"k":2,"c":[200,194,227]}}',
        tirages: 160,
      },
    ],
    'taciturne/sombre': [
      {
        solTire: 0,
        solVu: 1,
        corps: [228, 226, 255],
        corpsIdx: 3,
        vue: '{"s":1,"k":3,"c":[102,102,226],"t":1000000000000,"p":null}',
        tirages: 7,
      },
      {
        solTire: 3,
        solVu: 3,
        corps: [11, 13, 79],
        corpsIdx: 0,
        vue: '{"s":3,"k":0,"c":[157,157,198],"t":1000000060000,"p":{"s":1,"k":3,"c":[102,102,226]}}',
        tirages: 14,
      },
      {
        solTire: 1,
        solVu: 1,
        corps: [228, 226, 255],
        corpsIdx: 3,
        vue: '{"s":1,"k":3,"c":[102,102,226],"t":1000000120000,"p":{"s":3,"k":0,"c":[157,157,198]}}',
        tirages: 25,
      },
      {
        solTire: 0,
        solVu: 1,
        corps: [228, 226, 255],
        corpsIdx: 3,
        vue: '{"s":1,"k":3,"c":[102,102,226],"t":1000000120200,"p":{"s":3,"k":0,"c":[157,157,198]}}',
        tirages: 44,
      },
    ],
  } as const;
  const NOW = [T0, T0 + 60000, T0 + 120000, T0 + 120200];
  for (const [cle, suite] of Object.entries(B)) {
    it(
      cle + ' — un état neuf à chaque ouverture (la page rechargée) ; la quatrième repasse 200 ms après la troisième',
      () => {
        const [nom, th] = cle.split('/') as [string, 'clair' | 'sombre'];
        const C = ctx(PALS[nom]!, nom === 'signal', th === 'clair'),
          H = hasard(23),
          S = stockage();
        suite.forEach((x, i) => {
          const e = etatCouleursInitial();
          nouvelleOuverture(C, e, H.h, S, NOW[i]!);
          expect(e.solTire).toBe(x.solTire);
          expect(solIdxEff(C, e)).toBe(x.solVu);
          expect(corps(C, e, H.h)).toEqual(x.corps);
          expect(e.corpsIdx).toBe(x.corpsIdx);
          expect(S.s['promi_pelote_vue']).toBe(x.vue);
          expect(H.n()).toBe(x.tirages);
        });
      },
    );
  }
  const B2 = {
    'signal/sombre': [
      {
        solTire: 2,
        solVu: 2,
        corps: [130, 174, 248],
        corpsIdx: 0,
        bouton: [239, 227, 199],
        boutonIdx: 3,
        vue: '{"s":2,"k":0,"c":[178,170,246],"t":1000000000000,"p":null}',
        tirages: 6,
      },
      {
        solTire: 0,
        solVu: 0,
        corps: [255, 184, 210],
        corpsIdx: 1,
        bouton: [239, 227, 199],
        boutonIdx: 3,
        vue: '{"s":0,"k":1,"c":[171,177,236],"t":1000000060000,"p":{"s":2,"k":0,"c":[178,170,246]}}',
        tirages: 45,
      },
      {
        solTire: 1,
        solVu: 1,
        corps: [130, 174, 248],
        corpsIdx: 0,
        bouton: [201, 168, 245],
        boutonIdx: 2,
        vue: '{"s":1,"k":0,"c":[214,181,222],"t":1000000120000,"p":{"s":0,"k":1,"c":[171,177,236]}}',
        tirages: 84,
      },
    ],
    'irascible/clair': [
      {
        solTire: 2,
        solVu: 2,
        corps: [255, 138, 28],
        corpsIdx: 1,
        bouton: [43, 10, 10],
        boutonIdx: 3,
        vue: '{"s":2,"k":1,"c":[207,55,40],"t":1000000000000,"p":null}',
        tirages: 7,
      },
      {
        solTire: 1,
        solVu: 1,
        corps: [43, 10, 10],
        corpsIdx: 3,
        bouton: [255, 45, 26],
        boutonIdx: 0,
        vue: '{"s":1,"k":3,"c":[186,96,22],"t":1000000060000,"p":{"s":2,"k":1,"c":[207,55,40]}}',
        tirages: 14,
      },
      {
        solTire: 3,
        solVu: 3,
        corps: [255, 138, 28],
        corpsIdx: 1,
        bouton: [184, 15, 46],
        boutonIdx: 2,
        vue: '{"s":3,"k":1,"c":[112,52,16],"t":1000000120000,"p":{"s":1,"k":3,"c":[186,96,22]}}',
        tirages: 25,
      },
    ],
  } as const;
  for (const [cle, suite] of Object.entries(B2)) {
    it(cle + ' — le même état d’une ouverture à l’autre (comme dans l’app)', () => {
      const [nom, th] = cle.split('/') as [string, 'clair' | 'sombre'];
      const C = ctx(PALS[nom]!, nom === 'signal', th === 'clair'),
        H = hasard(5),
        S = stockage(),
        e = etatCouleursInitial();
      suite.forEach((x, i) => {
        nouvelleOuverture(C, e, H.h, S, NOW[i]!);
        expect(e.solTire).toBe(x.solTire);
        expect(solIdxEff(C, e)).toBe(x.solVu);
        expect(corps(C, e, H.h)).toEqual(x.corps);
        expect(e.corpsIdx).toBe(x.corpsIdx);
        expect(texteBouton(C, e, H.h)).toEqual({ rgb: x.bouton, idx: x.boutonIdx });
        expect(S.s['promi_pelote_vue']).toBe(x.vue);
        expect(H.n()).toBe(x.tirages);
      });
    });
  }
});

describe('le poil évite les îles (C-275, v203)', () => {
  const C0 = {
    'signal/clair': {
      solTire: 2,
      solEvite: -1,
      solVu: 0,
      solil: { i: 0, ecart: 1.1, force: false },
      corps: [255, 184, 210],
      tirages: 6,
    },
    'signal/sombre': {
      solTire: 2,
      solEvite: -1,
      solVu: 2,
      solil: { i: 2, ecart: 23.2, force: false },
      corps: [130, 174, 248],
      tirages: 6,
    },
    'candide/sombre/vue': {
      solTire: 0,
      solEvite: 0,
      solVu: 2,
      solil: { i: 2, ecart: 29.7, force: false },
      corps: [255, 181, 200],
      corpsIdx: 3,
      vue: '{"s":2,"k":3,"c":[210,210,178],"t":1000000000000,"p":{"s":0,"k":1,"c":[171,177,236]}}',
      tirages: 7,
    },
  } as const;
  it('Ingénu, deux îles, les deux thèmes', () => {
    const isl: Lab[] = [
      [71.5, 5.2, -42.1],
      [82.2, 24.6, -3.9],
    ];
    for (const th of ['clair', 'sombre'] as const) {
      const x = C0[`signal/${th}`];
      const C = ctx(PALS['signal']!, true, th === 'clair', isl),
        e = etatCouleursInitial(),
        H = hasard(3);
      nouvelleOuverture(C, e, H.h, stockage(), T0);
      expect(e.solTire).toBe(x.solTire);
      expect(e.solEvite).toBe(x.solEvite);
      expect(choixSol(C, e)).toEqual({ i: x.solil.i, ecart: x.solil.ecart, force: x.solil.force });
      expect(corps(C, e, H.h)).toEqual(x.corps);
      expect(H.n()).toBe(x.tirages);
    }
  });
  it('Candide sombre : le poil de l’ouverture d’avant (gardé) cède ; une dalle qui ne s’est pas rendue ne compte pas', () => {
    const x = C0['candide/sombre/vue'];
    const C = ctx(PALS['candide']!, false, false, [[75, 20, -30], null, [85, 8, 20]]),
      e = etatCouleursInitial(),
      H = hasard(9),
      S = stockage({ promi_pelote_vue: JSON.stringify({ s: 0, k: 1, c: [171, 177, 236], t: 1 }) });
    nouvelleOuverture(C, e, H.h, S, T0);
    expect(e.solTire).toBe(x.solTire);
    expect(e.solEvite).toBe(x.solEvite);
    expect(choixSol(C, e)).toEqual({ i: x.solil.i, ecart: x.solil.ecart, force: x.solil.force });
    expect(corps(C, e, H.h)).toEqual(x.corps);
    expect(e.corpsIdx).toBe(x.corpsIdx);
    expect(S.s['promi_pelote_vue']).toBe(x.vue);
    expect(H.n()).toBe(x.tirages);
  });
});

describe('une palette d’un seul ton : les replis du corps, l’encre du bouton', () => {
  const G = {
    'bleu/clair': {
      solTire: 0,
      solVu: 0,
      corps: [205, 223, 252],
      corpsIdx: 0,
      bouton: { rgb: [32, 25, 8], idx: -1 },
      vue: '{"s":0,"k":0,"c":[154,190,249],"t":1000000000000,"p":null}',
      tirages: 1,
    },
    'bleu/sombre': {
      solTire: 0,
      solVu: 0,
      corps: [205, 223, 252],
      corpsIdx: 0,
      bouton: { rgb: [247, 240, 222], idx: -1 },
      vue: '{"s":0,"k":0,"c":[154,190,249],"t":1000000000000,"p":null}',
      tirages: 1,
    },
    'kaki/clair': {
      solTire: 0,
      solVu: 0,
      corps: [194, 199, 167],
      corpsIdx: 0,
      bouton: { rgb: [32, 25, 8], idx: -1 },
      vue: '{"s":0,"k":0,"c":[144,152,95],"t":1000000000000,"p":null}',
      tirages: 1,
    },
    'kaki/sombre': {
      solTire: 0,
      solVu: 0,
      corps: [194, 199, 167],
      corpsIdx: 0,
      bouton: { rgb: [247, 240, 222], idx: -1 },
      vue: '{"s":0,"k":0,"c":[144,152,95],"t":1000000000000,"p":null}',
      tirages: 1,
    },
    'gris/clair': {
      solTire: 0,
      solVu: 0,
      corps: [179, 179, 179],
      corpsIdx: 0,
      bouton: { rgb: [32, 25, 8], idx: -1 },
      vue: '{"s":0,"k":0,"c":[145,145,145],"t":1000000000000,"p":null}',
      tirages: 1,
    },
    'gris/sombre': {
      solTire: 0,
      solVu: 0,
      corps: [179, 179, 179],
      corpsIdx: 0,
      bouton: { rgb: [247, 240, 222], idx: -1 },
      vue: '{"s":0,"k":0,"c":[145,145,145],"t":1000000000000,"p":null}',
      tirages: 1,
    },
  } as const;
  const PAL1: Record<string, RGB[]> = { bleu: [[130, 174, 248]], kaki: [[120, 130, 60]], gris: [[128, 128, 128]] };
  for (const [cle, x] of Object.entries(G)) {
    it(cle, () => {
      const [nom, th] = cle.split('/') as [string, 'clair' | 'sombre'];
      const C = ctx(PAL1[nom]!, false, th === 'clair'),
        e = etatCouleursInitial(),
        H = hasard(13),
        S = stockage();
      nouvelleOuverture(C, e, H.h, S, T0);
      expect(e.solTire).toBe(x.solTire);
      expect(solIdxEff(C, e)).toBe(x.solVu);
      expect(corps(C, e, H.h)).toEqual(x.corps);
      expect(e.corpsIdx).toBe(x.corpsIdx);
      expect(texteBouton(C, e, H.h)).toEqual(x.bouton);
      expect(S.s['promi_pelote_vue']).toBe(x.vue);
      expect(H.n()).toBe(x.tirages);
    });
  }
});

describe('la lisibilité d’une île, sur son masque (l’indice 0 est le sol)', () => {
  const D = {
    fond: [143, 140, 255],
    dE: 20.420454174909164,
    vide: null,
    clair: { fond: [183.56, 179, 242.13], dE: 6.452508790096655 },
  } as const;
  const masque = [0, 0, 1, 2, 2, 3, 0, 1, 5];
  const table: (RGB | null)[] = [null, [255, 184, 210], [40, 90, 200], [250, 250, 250]];
  for (const th of ['sombre', 'clair'] as const) {
    it(th, () => {
      const x = th === 'sombre' ? D : D.clair;
      const C = ctx(PALS['taciturne']!, false, th === 'clair'),
        e = etatCouleursInitial(),
        H = hasard(1);
      nouvelleOuverture(C, e, H.h, stockage(), T0);
      const F = fondSphere(C, e);
      proche(F, x.fond);
      expect(lisibiliteIle(masque, table, F)!.dE).toBeCloseTo(x.dE, 3);
      expect(lisibiliteIle([], [], F)).toBe(D.vide);
    });
  }
});

describe('la cession d’une île (chantier 59, hors Ingénu, en sombre)', () => {
  const E = {
    'irascible/1': { fond: [184, 15, 46], decale: { a: 16.8368328031656, b: 6.40984887106959 }, apres: 51.3 },
    'irascible/2': { fond: [184, 15, 46], decale: { a: 38.14395678131582, b: 70.39655641604932 }, apres: 46 },
    'taciturne/1': { fond: [143, 140, 255], decale: { a: 6.127297954119426, b: -13.790148988498974 }, apres: 49.1 },
    'candide/3': { fond: [189, 224, 168], decale: { a: 14.588479743532002, b: 26.49208350650982 }, apres: 36.2 },
  } as const;
  for (const [cle, x] of Object.entries(E)) {
    it(cle, () => {
      const [nom, rang] = cle.split('/') as [string, string];
      const C = ctx(PALS[nom]!, false, false),
        e = etatCouleursInitial();
      nouvelleOuverture(C, e, hasard(2).h, stockage(), T0);
      const F = fondSphere(C, e);
      proche(F, x.fond);
      const r = cessionIle(C.palette, F, Number(rang));
      expect(r && 'a' in r).toBe(true);
      if (!r || !('a' in r)) return;
      expect(r.a).toBeCloseTo(x.decale.a, 3);
      expect(r.b).toBeCloseTo(x.decale.b, 3);
      expect(Math.round(r.apres * 10) / 10).toBe(x.apres);
    });
  }
  it('rang 0 : rien ne cède ; aucun ton permis (amande, terracotta) : sans palette', () => {
    expect(cessionIle(PALS['irascible']!, [184, 15, 46], 0)).toBe(null);
    expect(
      cessionIle(
        [
          [0x8f, 0xe0, 0x8f],
          [0xdd, 0x4d, 0x23],
        ],
        [184, 15, 46],
        1,
      ),
    ).toEqual({ sansPalette: true });
  });
});

describe('la hauteur de rampe d’une île sous Ingénu', () => {
  const F0 = {
    'clair/vise': { fond: [171, 177, 236], h: 0.45, ecart: 30.2, tirages: 6 },
    'clair/max': { fond: [171, 177, 236], h: 0.45, ecart: 24.8, tirages: 6 },
    'clair/atteint': { fond: [171, 177, 236], h: 0.85, ecart: 120.8, tirages: 6 },
    'clair/trous': { fond: [171, 177, 236], h: 0.45, ecart: 20.9, tirages: 6 },
    'sombre/vise': { fond: [178, 170, 246], h: 0.45, ecart: 30.2, tirages: 6 },
    'sombre/max': { fond: [178, 170, 246], h: 1.1, ecart: 32.5, tirages: 6 },
    'sombre/atteint': { fond: [178, 170, 246], h: 0.85, ecart: 122.4, tirages: 6 },
    'sombre/trous': { fond: [178, 170, 246], h: 0.45, ecart: 25.9, tirages: 6 },
  } as const;
  const labDe: Record<string, (h: number) => Lab | null> = {
    vise: (h) => [40 + h * 10, 20 - h * 5, -30 + h * 8],
    max: (h) => [60 + h, 5, -10],
    atteint: (h) => (h === 0.85 ? [10, 60, 60] : [70, 5, -30]),
    trous: (h) => (h === 1.1 || h === 1.8 ? null : [50 + h * 12, 10, -20]),
  };
  for (const [cle, x] of Object.entries(F0)) {
    it(cle, () => {
      const [th, v] = cle.split('/') as ['clair' | 'sombre', string];
      const C = ctx(PALS['signal']!, true, th === 'clair'),
        e = etatCouleursInitial(),
        H = hasard(4);
      nouvelleOuverture(C, e, H.h, stockage(), T0);
      const fond = fondIleIngenu(C, e, H.h);
      expect(fond).toEqual(x.fond);
      expect(hauteurIngenu(th === 'clair', fond, labDe[v]!)).toEqual({ h: x.h, ecart: x.ecart });
      expect(H.n()).toBe(x.tirages);
    });
  }
  it('aucune hauteur ne se rend : la dalle reste telle quelle', () => {
    expect(hauteurIngenu(false, [130, 174, 248], () => null)).toBe(null);
  });
});

describe('la boucle de cession : seulement en sombre, trois tours au plus, un tour qui ne gagne rien est le dernier', () => {
  const H0 = {
    sombre: {
      cede: { '1|x/y/0': 1, '3|x/y/0': 2 },
      mesure: {
        tours: 2,
        restes: [2, 1, 1],
        plancher: 31,
        clair: false,
        iles: [
          { titre: 'a', dE: 61.9, rang: 1 },
          { titre: 'b', dE: 79.7, rang: 0 },
          { titre: 'c', dE: 2.1, rang: 2 },
        ],
      },
      fond: [143, 140, 255],
      posesRestantes: 1,
    },
    clair: {
      cede: {},
      mesure: {
        tours: 0,
        restes: [],
        plancher: 31,
        clair: true,
        iles: [
          { titre: 'a', dE: 22.6, rang: 0 },
          { titre: 'b', dE: 64.9, rang: 0 },
          { titre: 'c', dE: 22.7, rang: 0 },
        ],
      },
      fond: [183.56, 179, 242.13],
      posesRestantes: 3,
    },
  } as const;
  const mk = (cols: RGB[]): { m: number[][]; col: (RGB | null)[] } => ({
    m: [
      [0, 1, 1, 1],
      [0, 0, 2, 2],
      [3, 3, 3, 0],
    ],
    col: [null, ...cols],
  });
  const poses = [
    mk([
      [140, 140, 250],
      [20, 200, 20],
      [142, 141, 252],
    ]),
    mk([
      [30, 30, 30],
      [20, 200, 20],
      [144, 140, 250],
    ]),
    mk([
      [30, 30, 30],
      [20, 200, 20],
      [145, 141, 251],
    ]),
    mk([
      [30, 30, 30],
      [20, 200, 20],
      [146, 140, 250],
    ]),
  ];
  for (const th of ['sombre', 'clair'] as const) {
    it(th, () => {
      const x = H0[th];
      const C = ctx(PALS['taciturne']!, false, th === 'clair'),
        e = etatCouleursInitial();
      nouvelleOuverture(C, e, hasard(1).h, stockage(), T0);
      const F = fondSphere(C, e);
      proche(F, x.fond);
      let i = 0;
      const dE = (): (number | null)[] => poses[i]!.m.map((m) => lisibiliteIle(m, poses[i]!.col, F)?.dE ?? null);
      const cede: Record<string, number> = {};
      const r = cederIles(['1|x/y/0', '2|x/y/0', '3|x/y/0'], th === 'clair', cede, dE, () => {
        i++;
      });
      expect(r).toEqual({ tours: x.mesure.tours, restes: x.mesure.restes });
      expect(cede).toEqual(x.cede);
      expect(dE().map((v) => (v == null ? null : Math.round(v * 10) / 10))).toEqual(x.mesure.iles.map((q) => q.dE));
      expect(poses.length - 1 - i).toBe(x.posesRestantes);
    });
  }
});
