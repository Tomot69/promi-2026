/**
 * L'HORLOGE — la seule de l'app (règle de la vraie app : « une seule horloge d'animation, aucune minuterie dispersée »).
 *
 * Elle possède le temps (`maintenant`), les images (`image`), les minuteurs (`minuteur`, `intervalle`) et les rappels « quand le fil
 * est libre » (`quandLibre`). Notre code ne les demande qu'à elle (la règle de lint `no-restricted-globals` l'impose).
 *
 * Les pièces reprises du prototype (le moteur, le tracé, les flaques) appellent `requestAnimationFrame`, `setTimeout` et
 * `performance.now` par leur nom global : `installer()` pose l'horloge À LEUR PLACE, avant qu'elles soient chargées. Ainsi tout ce qui
 * s'anime dans l'app passe par une seule boucle d'images et un seul échéancier.
 *
 * Deux modes :
 *  · « réel »   — une boucle d'images native (une seule) tant qu'on en demande, un minuteur natif (un seul) pour l'échéance la plus proche ;
 *  · « piloté » — le temps n'avance que quand on le demande (`images(n)`), exactement comme le banc de rendu du prototype
 *                 (banc_rendu.py, PILOTE) : +1000/60 ms, puis les minuteurs échus (par échéance, puis par ordre de pose), puis les images.
 *                 C'est ce mode que les tests de rendu emploient, des deux côtés (prototype et vraie app), pour comparer au pixel.
 */

export type RappelImage = (t: number) => void;
type Rappel = (...a: unknown[]) => void;

interface Echeance {
  id: number;
  at: number;
  cb: Rappel;
  a: unknown[];
  rep: number; // 0 : un délai ; > 0 : un intervalle
}

export interface Horloge {
  readonly mode: 'reel' | 'pilote';
  maintenant(): number;
  image(cb: RappelImage): number;
  annuleImage(id: number): void;
  minuteur(cb: Rappel, ms?: number, ...a: unknown[]): number;
  intervalle(cb: Rappel, ms?: number, ...a: unknown[]): number;
  annuleMinuteur(id: number): void;
  quandLibre(cb: (d: { didTimeout: boolean; timeRemaining: () => number }) => void): number;
  /** mode piloté seulement : avance de n images (n × 1000/60 ms) */
  images(n: number): void;
}

interface Natifs {
  raf: (cb: FrameRequestCallback) => number;
  st: (cb: () => void, ms?: number) => number;
  ct: (id: number) => void;
  now: () => number;
}

const PAS = 1000 / 60;

export function creerHorloge(mode: 'reel' | 'pilote', natifs: Natifs, t0 = 0): Horloge {
  let vt = t0;
  let prochainId = 1;
  let file: Array<[number, RappelImage]> = [];
  const echeances: Echeance[] = [];
  let boucleNative = false;
  let minuteurNatif: number | null = null;
  let echeanceNative = Infinity;

  const maintenant = mode === 'pilote' ? () => vt : natifs.now;

  /** passe les minuteurs échus, dans l'ordre (échéance, puis ordre de pose) — l'algorithme du banc, à l'identique */
  function minuteursEchus(): void {
    const t = maintenant();
    for (let garde = 0; garde < 500; garde++) {
      let m = -1;
      for (let k = 0; k < echeances.length; k++) {
        const e = echeances[k]!;
        const best = m >= 0 ? echeances[m]! : null;
        if (e.at <= t && (!best || e.at < best.at || (e.at === best.at && e.id < best.id))) m = k;
      }
      if (m < 0) return;
      const e = echeances[m]!;
      if (e.rep) e.at += e.rep;
      else echeances.splice(m, 1);
      try {
        e.cb(...e.a);
      } catch (err) {
        signaler(err);
      }
    }
  }

  function passeImages(t: number): void {
    const q = file;
    file = [];
    for (const [, cb] of q) {
      try {
        cb(t);
      } catch (err) {
        signaler(err);
      }
    }
  }

  // ── mode réel : une seule boucle native, un seul minuteur natif ──
  function armerBoucle(): void {
    if (mode !== 'reel' || boucleNative || !file.length) return;
    boucleNative = true;
    natifs.raf((t) => {
      boucleNative = false;
      passeImages(t);
      armerBoucle();
    });
  }
  function armerMinuteur(): void {
    if (mode !== 'reel') return;
    let prochaine = Infinity;
    for (const e of echeances) if (e.at < prochaine) prochaine = e.at;
    if (prochaine === echeanceNative) return;
    if (minuteurNatif != null) natifs.ct(minuteurNatif);
    minuteurNatif = null;
    echeanceNative = prochaine;
    if (prochaine === Infinity) return;
    minuteurNatif = natifs.st(
      () => {
        minuteurNatif = null;
        echeanceNative = Infinity;
        minuteursEchus();
        armerMinuteur();
      },
      Math.max(0, prochaine - natifs.now()),
    );
  }

  function poser(cb: Rappel, ms: number | undefined, a: unknown[], intervalle: boolean): number {
    if (typeof cb !== 'function') return 0;
    const id = 1e6 + prochainId++;
    const rep = intervalle ? Math.max(16, +(ms ?? 0) || 0) : 0;
    echeances.push({ id, at: maintenant() + (intervalle ? rep : Math.max(0, +(ms ?? 0) || 0)), cb, a, rep });
    armerMinuteur();
    return id;
  }

  return {
    mode,
    maintenant,
    image(cb) {
      const id = prochainId++;
      file.push([id, cb]);
      armerBoucle();
      return id;
    },
    annuleImage(id) {
      file = file.filter((x) => x[0] !== id);
    },
    minuteur: (cb, ms, ...a) => poser(cb, ms, a, false),
    intervalle: (cb, ms, ...a) => poser(cb, ms, a, true),
    annuleMinuteur(id) {
      for (let k = echeances.length - 1; k >= 0; k--) if (echeances[k]!.id === id) echeances.splice(k, 1);
      armerMinuteur();
    },
    quandLibre(cb) {
      return poser(
        () => {
          cb({ didTimeout: false, timeRemaining: () => 50 });
        },
        1,
        [],
        false,
      );
    },
    images(n) {
      if (mode !== 'pilote') throw new Error("horloge : images() n'existe qu'en mode piloté");
      for (let i = 0; i < n; i++) {
        vt += PAS;
        minuteursEchus();
        passeImages(vt);
      }
    },
  };
}

let erreurs: (e: unknown) => void = (e) => {
  console.error(e);
};
function signaler(e: unknown): void {
  erreurs(e);
}
export function surErreur(f: (e: unknown) => void): void {
  erreurs = f;
}

let courante: Horloge | null = null;

/**
 * Pose l'horloge à la place des minuteurs du navigateur. Appelée UNE fois, au démarrage, avant de charger les pièces reprises.
 * Les pièces reprises ne testent pas l'existence de requestIdleCallback de la même façon partout : dans Safari il n'existe pas, et on ne
 * l'ajoute pas (le comportement doit rester celui que Tom a validé) ; en mode piloté on le pose, comme le banc du prototype.
 */
export function installer(mode: 'reel' | 'pilote', t0 = 0): Horloge {
  if (courante) return courante;
  const w = window as unknown as Record<string, unknown>;
  const perf = performance;
  const natifs: Natifs = {
    raf: window.requestAnimationFrame.bind(window),
    st: window.setTimeout.bind(window),
    ct: window.clearTimeout.bind(window),
    now: perf.now.bind(perf),
  };
  const h = creerHorloge(mode, natifs, t0);
  w['requestAnimationFrame'] = (cb: FrameRequestCallback) => h.image(cb);
  w['cancelAnimationFrame'] = (id: number) => {
    h.annuleImage(id);
  };
  w['setTimeout'] = (cb: Rappel, ms?: number, ...a: unknown[]) => h.minuteur(cb, ms, ...a);
  w['setInterval'] = (cb: Rappel, ms?: number, ...a: unknown[]) => h.intervalle(cb, ms, ...a);
  w['clearTimeout'] = (id: number) => {
    h.annuleMinuteur(id);
  };
  w['clearInterval'] = (id: number) => {
    h.annuleMinuteur(id);
  };
  if (mode === 'pilote' || 'requestIdleCallback' in window) {
    w['requestIdleCallback'] = (cb: Parameters<Horloge['quandLibre']>[0]) => h.quandLibre(cb);
    w['cancelIdleCallback'] = (id: number) => {
      h.annuleMinuteur(id);
    };
  }
  if (mode === 'pilote') perf.now = () => h.maintenant();
  courante = h;
  return h;
}

export function horloge(): Horloge {
  if (!courante) throw new Error("horloge : installer() n'a pas été appelée");
  return courante;
}
