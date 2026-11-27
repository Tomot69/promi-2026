/**
 * L'AURA (lot 6, SPEC-ECRANS §10) — ce qu'elle DIT, sans rien peindre : mes paroles, les tenues dans l'ordre où elles sont apparues (les îles de la
 * Pelote poussent par accrétion : une ancienne ne bouge jamais), la nature la plus tenue (le sol), les parts d'un anneau (deux états, C-210),
 * les personnes (ordre alphabétique, jamais par valeur, §2.9), ce qu'on te tient (Q215), la phrase sous la Pelote et les deux chiffres (R-015).
 * Le prototype : `mesPromi`, `ordreTenus`, `natureMaj`, `parts`, `personnes`, `envers`, `gensRecip`, `donnees`, `remplit`, `comptes`
 * (lot-AURA-PELOTE) — les formes et les textes sont les siens, au caractère près ; les tests les portent en dur (tests/unitaires/aura.test.ts).
 */
import type { Parole } from '../donnees/schema.ts';

export type NatureAura = 'promi' | 'chiche' | 'nuee';

/** la phrase sous la Pelote : tirée du NOMBRE de paroles tenues (elle change en faisant plus, jamais au hasard d'une ouverture) */
export const MOTS_AURA = [
  'Rien de ce qui est ici n’a été dit à la légère.',
  'Tout ça, tu l’as dit. Et tu l’as fait.',
  'On ne dirait pas comme ça, mais c’est du solide.',
  'Il y en a, des paroles tenues.',
  'Et dire que tout ça, c’est toi.',
] as const;
/** E4 (v178c) : aucune parole — la ligne 2 mène à la page + */
export const VIDE_AURA = ['La première parole laissera sa trace ici.', 'Tout commence par une parole donnée.'] as const;
/** E4 (v178c) : des paroles, rien de tenu — la ligne 2 mène à l'Index */
export const ZERO_AURA = ['Rien de tenu pour l’instant.', 'Une parole tenue prendra place ici.'] as const;

const champ = (p: Parole, k: string): unknown => (p as unknown as Record<string, unknown>)[k] ?? p.suite?.[k];

/** soi : « moi » (l'onboarding écrit « Moi », la page + « moi ») ou mon prénom (`_isMe`) */
export function estMoi(n: unknown, moi: string): boolean {
  const s = (typeof n === 'string' ? n : '').trim();
  return s.toLowerCase() === 'moi' || (!!moi.trim() && s === moi.trim());
}

/** ce que JE promets : ni un gardé de côté, ni une demande, ni la parole d'un autre */
export function mesParoles(paroles: readonly Parole[]): Parole[] {
  return paroles.filter((p) => !p.draft && !champ(p, 'req') && (!p.from || p.from === 'moi'));
}

/**
 * L'ORDRE DES TENUES EST CELUI OÙ ELLES SONT APPARUES — il ne se recalcule jamais : l'ordre gardé (`promi_pelote_ordre`), sans les paroles qui ne
 * sont plus tenues, puis les nouvelles par id. Rend la liste et l'ordre à garder.
 */
export function ordreTenus(P: readonly Parole[], garde: readonly number[]): { tenus: Parole[]; ordre: number[] } {
  const par = new Map<number, Parole>();
  for (const p of P) if (p.status === 'tenu') par.set(p.id, p);
  const ordre = garde.filter((id) => par.has(id));
  for (const p of [...par.values()].filter((q) => !ordre.includes(q.id)).sort((a, b) => a.id - b.id)) ordre.push(p.id);
  return { tenus: ordre.map((id) => par.get(id)!), ordre };
}

export function natureDe(p: Parole): NatureAura {
  return p.chiche ? 'chiche' : p.nuee ? 'nuee' : 'promi';
}
/** la nature la plus présente parmi ce qui est tenu ; égalité : Promi, puis Chiche, puis Cercle ; zéro : Promi */
export function natureMaj(T: readonly Parole[]): NatureAura {
  const c = { promi: 0, chiche: 0, nuee: 0 };
  for (const p of T) c[natureDe(p)]++;
  let b: NatureAura = 'promi';
  if (c.chiche > c[b]) b = 'chiche';
  if (c.nuee > c[b]) b = 'nuee';
  return b;
}
/** les parts d'un anneau : [tenues, en cours] (deux états, deux arcs — C-210) */
export function parts(L: readonly Parole[]): [number, number] {
  let t = 0;
  let e = 0;
  for (const p of L) {
    if (p.status === 'tenu') t++;
    else e++;
  }
  const s = t + e;
  return s ? [t / s, e / s] : [0, 0];
}

export interface PersonneAura {
  nom: string;
  /** l'anneau : ce qui se promet entre vous, dans les deux sens, une fois (Q215, 22 sept.) ; null : rien */
  parts: [number, number] | null;
  /** ce qu'elle te tient (« Ce qu'on t'a tenu ») */
  recu: [number, number] | null;
  nRecu: number;
}

const coupeQui = (w: string): string[] =>
  w
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean);

/** ce qu'on te tient (Q215) : ce qu'une personne te promet, sa moitié d'un Chiche relevé avec toi, ce qu'elle promet à un de tes Cercles */
export function envers(
  paroles: readonly Parole[],
  moi: string,
  cercles: Readonly<Record<string, string>>,
): Array<{ nom: string; p: Parole }> {
  const out: Array<{ nom: string; p: Parole }> = [];
  for (const p of paroles) {
    if (p.draft || champ(p, 'req')) continue;
    const de = p.from && p.from !== 'moi' && !estMoi(p.from, moi) ? p.from : null;
    const aMoi = !p.who || p.who === 'moi' || estMoi(p.who, moi);
    const avec = champ(p, 'avec');
    if (de && (aMoi || (p.nuee && cercles[p.nuee]))) out.push({ nom: de, p });
    else if (
      !de &&
      p.chiche &&
      champ(p, 'chicheEtat') === 'releve' &&
      typeof avec === 'string' &&
      avec &&
      !estMoi(avec, moi)
    )
      out.push({ nom: avec, p });
  }
  return out;
}

/** la rangée des personnes : à qui je promets, et qui me promet sans que je lui promette — ordre alphabétique, jamais par valeur */
export function personnes(
  P: readonly Parole[],
  E: ReadonlyArray<{ nom: string; p: Parole }>,
  moi: string,
): PersonneAura[] {
  const lst = new Map<string, Parole[]>();
  for (const p of P)
    for (const w of coupeQui(String(p.who || ''))) {
      if (w === 'moi' || w === 'le groupe' || estMoi(w, moi)) continue;
      const l = lst.get(w) ?? [];
      l.push(p);
      lst.set(w, l);
    }
  const r = new Map<string, Parole[]>();
  for (const x of E) {
    if (x.nom === 'le groupe') continue;
    const l = r.get(x.nom) ?? [];
    l.push(x.p);
    r.set(x.nom, l);
  }
  const noms = [...lst.keys(), ...[...r.keys()].filter((n) => !lst.has(n))].sort((a, b) => a.localeCompare(b, 'fr'));
  return noms.map((nom) => {
    const tout = [...(lst.get(nom) ?? []), ...(r.get(nom) ?? [])];
    const rn = r.get(nom);
    return { nom, parts: tout.length ? parts(tout) : null, recu: rn ? parts(rn) : null, nRecu: rn?.length ?? 0 };
  });
}

export interface DonneesAura {
  /** mes paroles */
  P: Parole[];
  /** les tenues, dans l'ordre où elles sont apparues */
  T: Parole[];
  ordre: number[];
  n: number;
  nature: NatureAura;
  toi: [number, number];
  gens: PersonneAura[];
  recu: [number, number] | null;
  /** ce qu'on t'a tenu, par id */
  RT: Parole[];
  /** la phrase sous la Pelote (et sa seconde ligne, qui se touche — E4), ou rien */
  phrase: { l1: string; l2: string | null; mene: 'plus' | 'index' | null };
  /** « Ce que tu as tenu » : toutes les tenues, la plus récente en premier (C-052, v132) */
  moisson: Parole[];
  /** « Ce qu'on t'a tenu » : les trois dernières, la plus récente en premier */
  moisson2: Parole[];
  /** les deux chiffres sous la légende : tenues, en cours (R-015) */
  chiffres: [number, number];
}

export function donneesAura(
  paroles: readonly Parole[],
  o: { moi: string; cercles: Readonly<Record<string, string>>; ordre: readonly number[] },
): DonneesAura {
  const P = mesParoles(paroles);
  const { tenus: T, ordre } = ordreTenus(P, o.ordre);
  const E = envers(paroles, o.moi, o.cercles);
  const RT = E.filter((x) => x.p.status === 'tenu')
    .map((x) => x.p)
    .sort((a, b) => a.id - b.id);
  const vide = P.length === 0;
  const phrase = vide
    ? { l1: VIDE_AURA[0], l2: VIDE_AURA[1], mene: 'plus' as const }
    : T.length > 0
      ? { l1: MOTS_AURA[T.length % MOTS_AURA.length]!, l2: null, mene: null }
      : { l1: ZERO_AURA[0], l2: ZERO_AURA[1], mene: 'index' as const };
  let t = 0;
  for (const p of P) if (p.status === 'tenu') t++;
  return {
    P,
    T,
    ordre,
    n: T.length,
    nature: natureMaj(T),
    toi: parts(P),
    gens: personnes(P, E, o.moi),
    recu: E.length ? parts(E.map((x) => x.p)) : null,
    RT,
    phrase,
    moisson: vide ? [] : T.slice().reverse(),
    moisson2: vide ? [] : RT.slice(-3).reverse(),
    chiffres: [t, P.length - t],
  };
}
