/**
 * LES EXEMPLES DES PASTILLES VIDES (`lot-EXEMPLES-V20` du prototype ; v115, v179b — E4 point 4). Une fonction pure : elle reçoit le compteur,
 * le sac et la dernière phrase sortie (les clés de l'appareil du prototype, gardées par le magasin) et rend le tirage et ce qu'il faut écrire.
 *  · ouverture 1 → la phrase 1 ; ouverture 2 → la phrase 2 (le Chiche : une seule fixe) ;
 *  · ensuite, un SAC des phrases suivantes, tiré SANS REMISE et gardé d'une ouverture à l'autre ; vide, il se remplit à nouveau ;
 *  · la dernière phrase sortie n'est jamais retirée juste après elle-même, même quand le sac repart de zéro (v179b).
 * Un tirage par ouverture de la page + (la page le garde le temps qu'elle est ouverte).
 */
export interface EtatTirage {
  /** `promi_ex_<type>` : le nombre d'ouvertures déjà servies */
  n: number;
  /** `promi_ex_sac_<type>` : les rangs qui restent dans le sac (null : pas encore de sac) */
  sac: number[] | null;
  /** `promi_ex_der_<type>` : le rang de la dernière phrase sortie */
  der: number | null;
}

export interface Tirage {
  rang: number;
  suivant: EtatTirage;
}

export function tirer(longueur: number, fixes: number, e: EtatTirage, alea: () => number): Tirage {
  const { n, der } = e;
  if (n < fixes && n < longueur && n !== der) return { rang: n, suivant: { n: n + 1, sac: e.sac, der: n } };
  let sac = Array.isArray(e.sac) ? e.sac.filter((x) => x >= fixes && x < longueur) : null;
  if (!sac || !sac.length) {
    sac = [];
    for (let k = fixes; k < longueur; k++) sac.push(k);
  }
  if (!sac.length) return { rang: 0, suivant: { n: n + 1, sac, der: 0 } };
  let pool = sac.filter((x) => x !== der);
  if (!pool.length) pool = sac;
  const pris = pool[Math.floor(alea() * pool.length)]!;
  const reste = sac.slice();
  reste.splice(reste.indexOf(pris), 1);
  return { rang: pris, suivant: { n: n + 1, sac: reste, der: pris } };
}

/** « A / B » : la variante plurielle quand il y a plusieurs personnes (`_ppVar`) */
export function variante(s: string, pluriel: boolean): string {
  const k = s.split(' / ');
  return pluriel && k[1] ? k[1] : k[0]!;
}
