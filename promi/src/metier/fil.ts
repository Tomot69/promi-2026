/**
 * LE COMPTEUR DU FIL (v89, Q347) — ce qui attend un GESTE de moi : un Chiche reçu, un Promi qu'on me fait et que je n'ai pas accepté, une
 * invitation à un Cercle, une moitié tracée qui attend la mienne, une demande en attente. Il redescend quand on a agi, jamais parce qu'on a
 * regardé. La pastille du Fil de l'accueil s'allume s'il est au-dessus de zéro. (`_filAttend`, `_filAttente`, `demandesEnAttente`.)
 */
import type { Etat, EvenementFil, Parole } from '../donnees/schema.ts';

type Plat = Record<string, unknown>;
/** une valeur de l'état lue comme un texte (rien, si ce n'en est pas un) */
const ch = (v: unknown): string => (typeof v === 'string' ? v : '');

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

// ── LE FIL À L'ÉCRAN (lot 4 ; le prototype : `buildFeed`, `_filTrieFiltre` de v163b C-191, `_derAct.cleFil` de v181b C-245, `_s4Fil` de lot-S4) ──

export type TriFil = 'recent' | 'personne' | 'nuee';
export type FiltreFil = 'tous' | 'agir' | 'tenues' | 'demandes' | 'nuees' | 'moi' | 'proches';
/** un geste du Fil (C-189 : une parole se tient par le trait — TRACER ouvre la fiche ; REPORTER, RELEVER, REJOINDRE) */
export type Geste = 'tracer' | 'post' | 'releve' | 'rejoindre';
export interface EntreeFil {
  f: EvenementFil;
  p: Parole | null;
  /** le Cercle dont parle l'événement (son nom dans le texte), quand aucune parole n'est trouvée */
  nk: string | null;
  gestes: Geste[];
}

const MOTS_GESTE: Record<Geste, string> = {
  tracer: 'TRACER',
  post: 'REPORTER',
  releve: 'RELEVER',
  rejoindre: 'REJOINDRE',
};
export const motGeste = (g: Geste): string => MOTS_GESTE[g];

/** la parole d'un événement : son id, sinon le titre entre guillemets ; sinon, le Cercle nommé dans le texte (`buildFeed`) */
function resoudre(f: EvenementFil, e: Readonly<Etat>): { p: Parole | null; nk: string | null } {
  let p = f.pid != null ? (e.paroles.find((x) => x.id === f.pid) ?? null) : null;
  if (p) return { p, nk: null };
  const t = (f.text || '').toLowerCase();
  for (const [k, n] of Object.entries(e.cercles)) if (n && t.includes(n.toLowerCase())) return { p: null, nk: k };
  const m = /[«"']\s*([^»"']+?)\s*[»"']/.exec(f.text || '');
  if (m) {
    const ti = m[1]!.trim().toLowerCase();
    p = e.paroles.find((x) => (x.title || '').trim().toLowerCase() === ti) ?? null;
  }
  return { p, nk: null };
}

/** les gestes d'un événement (`buildFeed`, sans TENIR : C-189) */
function gestes(f: EvenementFil, p: Parole | null, paroles: readonly Parole[]): Geste[] {
  const g = plat(f);
  const q = p ? plat(p) : null;
  if (g['type'] === 'received' && q && q['pending']) return ['post'];
  if (g['type'] === 'chiche_recu') return ['releve'];
  if (g['type'] === 'invitation' && !g['fait']) return ['rejoindre'];
  if (g['type'] === 'moitie' && filAttend(f, paroles)) return ['tracer'];
  // v173 (C-210) : une parole en cours dont la date est passée
  if (p && q && !p.draft && !q['req'] && p.status === 'encours' && p.due != null && +p.due < 0)
    return ['tracer', 'post'];
  return [];
}

export function entreesFil(
  e: Readonly<Etat>,
  q = '',
  filtre: FiltreFil = 'tous',
  tri: TriFil = 'recent',
  moi = 'Moi',
): EntreeFil[] {
  const Q = q.trim().toLowerCase();
  const nomC = (k: string | null | undefined): string => (k ? e.cercles[k] || k : '');
  const parole = (f: EvenementFil): Parole | null =>
    f.pid != null ? (e.paroles.find((x) => x.id === f.pid) ?? null) : null;
  const sac = (f: EvenementFil): string => {
    const g = plat(f);
    const p = parole(f);
    let b = [f.text || '', f.t || '', ch(g['who']), ch(g['from'])].join(' ');
    if (p)
      b += ' ' + [p.title || '', p.who || '', p.from || '', nomC(p.nuee)].join(' ') + (p.draft ? ' brouillon' : '');
    return b.toLowerCase();
  };
  let L = e.fil.filter((f) => !Q || sac(f).includes(Q));
  // le premier tri, celui de `buildFeed` (`fdSortMode`) : « Par personne » met « moi » d'abord, puis l'ordre des noms ; « Par Cercle », l'ordre des noms
  const estMoi = (k: string): boolean => {
    const x = k.trim().toLowerCase();
    return x === '' || x === 'moi' || x === moi.trim().toLowerCase();
  };
  if (tri === 'personne') {
    const pk = (f: EvenementFil): string => {
      const p = parole(f);
      return ch(plat(f)['from']) || p?.from || p?.who || ch(plat(f)['who']);
    };
    L = L.slice().sort((a, b) => {
      const ka = pk(a);
      const kb = pk(b);
      const ma = estMoi(ka) ? 0 : 1;
      const mb = estMoi(kb) ? 0 : 1;
      return ma !== mb ? ma - mb : ka.localeCompare(kb);
    });
  } else if (tri === 'nuee') {
    const nk = (f: EvenementFil): string => nomC(parole(f)?.nuee) || '~~';
    L = L.slice().sort((a, b) => nk(a).localeCompare(nk(b)));
  }
  let E: EntreeFil[] = L.map((f) => {
    const r = resoudre(f, e);
    return { f, p: r.p, nk: r.nk, gestes: gestes(f, r.p, e.paroles) };
  });
  // le filtre et le second tri (`_filTrieFiltre`)
  const ok: Record<FiltreFil, (x: EntreeFil) => boolean> = {
    tous: () => true,
    agir: (x) => x.gestes.length > 0,
    tenues: (x) => !!(x.p && x.p.status === 'tenu' && x.f.type === 'kept'),
    demandes: (x) => !!(x.p && plat(x.p)['req']) || /demand/i.test(x.f.type || ''),
    nuees: (x) => !!(x.nk || x.p?.nuee),
    moi: (x) => /Tu as|Ton Promi/.test(x.f.text || ''),
    proches: (x) => !/Tu as|Ton Promi/.test(x.f.text || ''),
  };
  E = E.filter(ok[filtre]);
  const actP = (p: Parole): number => (p.derAct != null ? +p.derAct : +p.id || 0);
  const cle =
    tri === 'personne'
      ? (x: EntreeFil): string => {
          const w = ch(plat(x.f)['from']) || x.p?.who || '';
          const l = w.toLowerCase();
          return !l || l === 'moi' ? '￿' : l;
        }
      : tri === 'nuee'
        ? (x: EntreeFil): string => {
            const n = nomC(x.nk || x.p?.nuee);
            return n ? n.toLowerCase() : '￿';
          }
        : null;
  const I = E.map((x, i) => ({ x, i }));
  if (cle) I.sort((a, b) => (cle(a.x) < cle(b.x) ? -1 : cle(a.x) > cle(b.x) ? 1 : a.i - b.i));
  else {
    // C-245 : la dernière action d'abord (la parole, le Cercle, l'heure de l'événement) ; rien de daté : l'ordre du Fil tel quel
    const k = (x: EntreeFil, i: number): number => {
      let a = x.p ? actP(x.p) : 0;
      if (x.nk) for (const p of e.paroles) if (p.nuee === x.nk && !p.draft) a = Math.max(a, actP(p));
      if (x.f.ts) a = Math.max(a, +x.f.ts);
      return a > 1e12 ? a : -i;
    };
    const K = I.map(({ x, i }) => ({ x, i, k: k(x, i) }));
    K.sort((a, b) => b.k - a.k || a.i - b.i);
    return K.map((o) => o.x);
  }
  return I.map((o) => o.x);
}

/** la ligne de l'événement : son texte sans le titre entre guillemets (`_s4Fil`) */
export function evenementSansTitre(texte: string): string {
  return texte
    .replace(/«[^»]*»/, '')
    .replace(/[:·]\s*$/, '')
    .replace(/\s*:\s*$/, '')
    .replace(/\s+/g, ' ')
    .trim();
}
