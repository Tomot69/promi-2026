/**
 * LE COMPTEUR DU FIL (v89, Q347) — ce qui attend un GESTE de moi : un Chiche reçu, un Promi qu'on me fait et que je n'ai pas accepté, une
 * invitation à un Cercle, une moitié tracée qui attend la mienne, une demande en attente. Il redescend quand on a agi, jamais parce qu'on a
 * regardé. La pastille du Fil de l'accueil s'allume s'il est au-dessus de zéro. (`_filAttend`, `_filAttente`, `demandesEnAttente`.)
 */
import type { Etat, EvenementFil, Parole } from '../donnees/schema.ts';

type Plat = Record<string, unknown>;

function plat(o: { suite?: Record<string, unknown> }): Plat {
  const { suite, ...connus } = o;
  return { ...connus, ...(suite ?? {}) };
}

export function filAttend(f: EvenementFil, paroles: readonly Parole[]): boolean {
  const e = plat(f);
  const p = e['pid'] == null ? null : (paroles.find((x) => x.id === e['pid']) ?? null);
  const q = p ? plat(p) : null;
  switch (e['type']) {
    case 'chiche_recu':
      return true;
    case 'received':
      return !!(q && q['pending']);
    case 'invitation':
      return !e['fait'];
    case 'moitie':
      return !e['fait'] && !!q && q['status'] !== 'tenu' && q['status'] !== 'kept';
    default:
      return false;
  }
}

export function filAttente(e: Readonly<Etat>): number {
  let n = 0;
  for (const f of e.fil) if (filAttend(f, e.paroles)) n++;
  for (const p of e.paroles) {
    const q = plat(p);
    if (q['req'] && q['reqEtat'] !== 'expiree') n++;
  }
  return n;
}

/** l'anneau du + : les paroles tenues et en cours (ni gardées de côté, ni demandées) */
export function compteAnneau(e: Readonly<Etat>): { tenues: number; enCours: number } {
  let tenues = 0;
  let enCours = 0;
  for (const p of e.paroles) {
    const q = plat(p);
    if (q['draft'] || q['req']) continue;
    if (q['status'] === 'tenu') tenues++;
    else enCours++;
  }
  return { tenues, enCours };
}

/**
 * UNE LIGNE DU FIL, telle que le prototype l'écrit (`feedAdd`, et `insecable` qui l'enveloppe, l. 38296) : les guillemets insécables (« et le mot
 * qui le suit ne se séparent jamais), « à l'instant » (l'apostrophe droite du prototype), `unread` posé, l'heure (`ts`, v181b).
 */
export function ligneFil(
  id: number,
  type: string,
  texte: string,
  maintenant: number,
  o: { pid?: number; unread?: boolean } = {},
): EvenementFil {
  const NB = '\u00a0';
  const text = texte.replace(/«\s*/g, '«' + NB).replace(/\s*»/g, NB + '»');
  const l: EvenementFil = { id, type, text, t: "à l'instant", unread: !!o.unread, ts: maintenant };
  if (o.pid != null) l.pid = o.pid;
  return l;
}
